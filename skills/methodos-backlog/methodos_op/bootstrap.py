"""Bootstrap methodos_sequence on a project's User Stories.

First-run sequencing: order by priority DESC, createdAt ASC, assign 1..N.
Idempotent — re-running on an already-bootstrapped project is a no-op
unless `force=True`.
"""
from __future__ import annotations

from .client import get
from .sequence import (
    SEQUENCE_KEY,
    get_sequence,
    set_sequence,
    list_stories_with_sequences,
    wp_ids_in_priority_order,
)


def bootstrap_project(project_id: int, force: bool = False, dry_run: bool = False) -> dict:
    """Set methodos_sequence on every User Story that lacks one.

    Sort key: priority.id DESC, createdAt ASC. Assigns 1..N to WPs
    without a sequence (idempotent unless `force=True`, in which case
    every WP is renumbered in the priority order).

    Args:
        project_id: OP project id.
        force: if True, renumber every WP, not just unsequenced ones.
        dry_run: if True, return the plan without applying any PATCH.

    Returns:
        dict with keys:
            - changed (bool)
            - actions ([{"wp_id": int, "from": int|None, "to": int}, ...])
            - errors  ([{"wp_id": int, "status": int, "body": ...}, ...])
    """
    stories = list_stories_with_sequences(project_id)
    ordered_ids = wp_ids_in_priority_order(project_id)
    # Preserve priority order in the action list.
    ordered_set = list(ordered_ids)

    existing = {wid: seq for wid, seq, _ in stories}
    actions: list[dict] = []
    for i, wid in enumerate(ordered_set, 1):
        frm = existing.get(wid)
        if frm is None or force:
            actions.append({"wp_id": wid, "from": frm, "to": i})

    if not actions:
        return {"changed": False, "actions": [], "errors": []}

    if dry_run:
        return {"changed": False, "actions": actions, "errors": []}

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
        "actions": actions,
        "errors": errors,
    }


def bootstrap_all(cfg: dict, force: bool = False, dry_run: bool = False) -> list[dict]:
    """Bootstrap every managed project (iterates all OP projects, filters
    via the managed_by_field_id+managed_by_option_id pattern).

    Returns a list of result dicts — one per managed project.
    """
    from .client import get

    field_id = cfg["managed_by_field_id"]
    option_id = cfg["managed_by_option_id"]
    needle = f"/custom_options/{option_id}"
    data = get("/api/v3/projects", {"pageSize": 100})
    if data is None or data.get("_type") == "NotFound":
        return []
    managed: list[dict] = []
    for p in data.get("_embedded", {}).get("elements", []):
        link = (p.get("_links", {}) or {}).get(f"customField{field_id}", {})
        if link.get("href", "").endswith(needle):
            managed.append(p)

    results = []
    for proj in managed:
        r = bootstrap_project(int(proj["id"]), force=force, dry_run=dry_run)
        r["project_id"] = proj["id"]
        r["project_name"] = proj.get("name", str(proj["id"]))
        results.append(r)
    return results
