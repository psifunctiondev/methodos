"""Resequence User Story WPs in a project: 1..N in caller-provided order."""
from __future__ import annotations

from typing import Iterable

from .sequence import (
    SEQUENCE_KEY,
    get_sequence,
    set_sequence,
    list_stories_with_sequences,
)


def current_sequences(project_id: int) -> list[tuple[int, int | None, str]]:
    """Return [(wp_id, current_sequence_or_None, subject), ...] sorted by
    current sequence ascending; unsequenced go last. Wrapper around
    sequence.list_stories_with_sequences — named for the resequence idiom.
    """
    return list_stories_with_sequences(project_id)


def resequence(
    project_id: int,
    ordered_wp_ids: Iterable[int],
    dry_run: bool = False,
) -> dict:
    """Resequence the project's User Stories to the given order.

    Given an ordered list of WP IDs, assigns 1..N to the matching WPs.
    Idempotent: if the current sequence order already matches the
    requested order, returns early with `changed=False`. Otherwise,
    sets each WP's sequence in ascending order.

    Args:
        project_id: OP project id.
        ordered_wp_ids: WP ids in the desired new sequence order.
        dry_run: if True, return the plan without applying any PATCH.

    Returns:
        dict with keys:
            - changed (bool): whether any PATCHes were applied
            - before ([(wp_id, sequence_or_None, subject), ...])
            - after  ([(wp_id, sequence, subject), ...])
            - actions ([{"wp_id": int, "from": int|None, "to": int}, ...])
            - errors  ([{"wp_id": int, "status": int, "body": ...}, ...])
    """
    ordered = [int(w) for w in ordered_wp_ids]
    before = current_sequences(project_id)

    # Build a set of currently-tracked story ids for sanity-checking the input.
    known_ids = {wid for wid, _, _ in before}
    unknown = [w for w in ordered if w not in known_ids]
    if unknown:
        raise ValueError(
            f"ordered_wp_ids contains {len(unknown)} WP(s) not found among "
            f"the project's User Stories: {unknown[:5]}"
            + ("..." if len(unknown) > 5 else "")
        )

    # Build the desired-after mapping (sequence -> wp_id), then compare to current.
    desired_after = [
        (wid, i + 1, next((s for wid_, _, s in before if wid_ == wid), ""))
        for i, wid in enumerate(ordered)
    ]
    current_order_by_seq = [(wid, seq) for wid, seq, _ in before if seq is not None]
    requested_pairs = [(wid, i + 1) for i, wid in enumerate(ordered)]
    if current_order_by_seq == requested_pairs:
        return {
            "changed": False,
            "before": before,
            "after": desired_after,
            "actions": [],
            "errors": [],
        }

    # Compute the actions: {wp_id: (from, to)}.
    from_map = {wid: seq for wid, seq, _ in before}
    actions = []
    for i, wid in enumerate(ordered, 1):
        frm = from_map.get(wid)
        actions.append({"wp_id": wid, "from": frm, "to": i})

    if dry_run:
        return {
            "changed": False,
            "before": before,
            "after": desired_after,
            "actions": actions,
            "errors": [],
        }

    # Apply in order 1..N. If a PATCH collides (lockVersion mismatch from
    # parallel edits), retry once after re-fetching.
    errors: list[dict] = []
    for action in actions:
        wid = action["wp_id"]
        target = action["to"]
        for attempt in (1, 2):
            status, body = set_sequence(wid, target)
            if status in (200, 204):
                break
            if status == 409 and attempt == 1:
                # lockVersion mismatch — re-fetch (set_sequence already does)
                continue
            errors.append({"wp_id": wid, "status": status, "body": body})
            break

    # Re-read after-state for the report.
    after = current_sequences(project_id)
    # Re-build the after tuple to match the requested order.
    after_ordered = [
        (wid, i + 1, next((s for wid_, _, s in after if wid_ == wid), ""))
        for i, wid in enumerate(ordered)
    ]

    return {
        "changed": True,
        "before": before,
        "after": after_ordered,
        "actions": actions,
        "errors": errors,
    }
