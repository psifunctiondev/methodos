"""Promote/demote a single User Story to a new sequence rank."""
from __future__ import annotations

from .sequence import (
    SEQUENCE_KEY,
    get_sequence,
    set_sequence,
    list_stories_with_sequences,
)


def prioritize(
    wp_id: int,
    new_rank: int,
    cascade: bool = False,
    dry_run: bool = False,
) -> dict:
    """Move a single WP to a new sequence rank within its project.

    Without `cascade`: simply PATCHes the WP's sequence to `new_rank`.
    This may collide with an existing rank — caller accepts that risk.

    With `cascade`: first shifts every OTHER WP at rank >= new_rank
    up by one (highest-first to avoid transient collisions), then sets
    the target to new_rank. The result is a contiguous block ending at
    max(existing_max, new_rank) with target at the requested slot.

    If the target is already at `new_rank`, returns early with
    `changed=False`.

    Args:
        wp_id: OP WP id of the target.
        new_rank: 1-indexed desired new sequence position.
        cascade: if True, push other WPs at >=new_rank out of the way.
        dry_run: if True, return the plan without applying any PATCH.

    Returns:
        dict with keys:
            - changed (bool)
            - target_wp_id (int)
            - new_rank (int)
            - actions ([{"wp_id": int, "from": int|None, "to": int}, ...])
            - errors  ([{"wp_id": int, "status": int, "body": ...}, ...])
    """
    from .client import get

    target_detail = get(f"/api/v3/work_packages/{wp_id}")
    if target_detail is None or target_detail.get("_type") == "NotFound":
        raise ValueError(f"WP {wp_id} not found")
    project_link = (target_detail.get("_links", {}).get("project") or {}).get("href", "")
    if not project_link.startswith("/api/v3/projects/"):
        raise ValueError(f"WP {wp_id} has no resolvable project link")
    project_id = int(project_link.rsplit("/", 1)[-1])

    stories = list_stories_with_sequences(project_id)
    target_seq = next((s for wid, s, _ in stories if wid == wp_id), None)
    if target_seq is None:
        # Target has no sequence yet — treat it as "off the bottom".
        # For cascade logic, treat its rank as +infinity.
        target_seq = 10**9

    if target_seq == new_rank and target_seq != 10**9:
        return {
            "changed": False,
            "target_wp_id": wp_id,
            "new_rank": new_rank,
            "actions": [],
            "errors": [],
        }

    actions: list[dict] = []

    if cascade:
        # Find OTHER stories with rank >= new_rank; shift them up by 1
        # in descending order to avoid transient collisions.
        to_shift = [
            (wid, seq)
            for wid, seq, _ in stories
            if wid != wp_id and seq is not None and seq >= new_rank
        ]
        to_shift.sort(key=lambda r: -r[1])  # highest first
        for wid, seq in to_shift:
            actions.append({"wp_id": wid, "from": seq, "to": seq + 1})

    actions.append({"wp_id": wp_id, "from": target_seq if target_seq != 10**9 else None, "to": new_rank})

    if dry_run:
        return {
            "changed": False,
            "target_wp_id": wp_id,
            "new_rank": new_rank,
            "actions": actions,
            "errors": [],
        }

    errors: list[dict] = []
    for action in actions:
        wid = action["wp_id"]
        target = action["to"]
        for attempt in (1, 2):
            status, body = set_sequence(wid, target)
            if status in (200, 204):
                break
            if status == 409 and attempt == 1:
                continue
            errors.append({"wp_id": wid, "status": status, "body": body})
            break

    return {
        "changed": bool(actions) and not errors,
        "target_wp_id": wp_id,
        "new_rank": new_rank,
        "actions": actions,
        "errors": errors,
    }
