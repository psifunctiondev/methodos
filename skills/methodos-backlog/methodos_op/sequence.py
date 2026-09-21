"""methodos_sequence (Integer custom field on User Story WPs).

The `methodos_sequence` field is the integer priority rank within a project.
It is set via the **flat** payload shape `{"lockVersion": N, "customField4": <int>}`,
NOT via the `_links.customField4.href` pattern used by option-based fields.

Verified end-to-end against methodos-recycling (project id 11) on 2026-09-17.
"""
from __future__ import annotations

from typing import Iterable

from .client import get, fetch_full_wp
from .config import METHODOS_SEQUENCE_FIELD_ID

# Key under which the sequence value lives on a WP payload.
# Kept as a module-level constant so resequence/prioritize can use the
# same key without re-deriving it.
SEQUENCE_KEY = "customField" + str(METHODOS_SEQUENCE_FIELD_ID)


def get_sequence(wp: dict) -> int | None:
    """Return the current methodos_sequence for a WP payload, or None if unset.

    Accepts a full WP payload (or any dict with the customField{N} key).
    """
    val = wp.get(SEQUENCE_KEY)
    if val is None:
        return None
    try:
        return int(val)
    except (TypeError, ValueError):
        return None


def set_sequence(wp_id: int, value: int) -> tuple[int, dict | None]:
    """Set methodos_sequence on a single WP. Fetches lockVersion then PATCHes.

    Payload shape (verified working):
        {"lockVersion": N, "customField4": <int>}

    Returns (status_code, response_body). Caller inspects status (200/204
    = success). 409 means lockVersion mismatch — re-fetch and retry.
    """
    detail = fetch_full_wp(wp_id)
    if detail is None or detail.get("_type") == "NotFound":
        return 404, {"_type": "NotFound"}
    lock_version = detail.get("lockVersion", 0)
    from .client import patch  # local import to avoid cycle (patch is in client.py)

    return patch(
        f"/api/v3/work_packages/{wp_id}",
        {"lockVersion": lock_version, SEQUENCE_KEY: int(value)},
    )


def list_user_stories(project_id: int) -> list[dict]:
    """Return full WP payloads for every User Story in a project.

    Iterates the project WP collection, then re-fetches each WP individually
    because the OP 16.6.3 collection endpoint does not propagate `embed` to
    elements — type info has to be fetched per-WP.
    """
    ids: list[int] = []
    offset = 1
    page_size = 100
    while True:
        data = get(
            f"/api/v3/projects/{project_id}/work_packages",
            {"pageSize": page_size, "offset": offset},
        )
        if data is None or data.get("_type") == "NotFound":
            break
        elements = data.get("_embedded", {}).get("elements", [])
        if not elements:
            break
        ids.extend(int(wp["id"]) for wp in elements if wp.get("id") is not None)
        total = data.get("total", 0)
        if len(ids) >= total:
            break
        offset += page_size
    enriched: list[dict] = []
    for wid in ids:
        detail = fetch_full_wp(wid, embed="type")
        if detail and detail.get("_type") != "NotFound":
            enriched.append(detail)
    return enriched


def list_stories_with_sequences(project_id: int) -> list[tuple[int, int | None, str]]:
    """Convenience: return (wp_id, sequence_or_None, subject) for each User Story.

    Sorted by sequence ascending; stories without a sequence go to the end.
    Useful for `current_sequences()` in resequence.py and for bootstrap.
    """
    from .client import USER_STORY_TYPE_NAME

    stories = []
    for wp in list_user_stories(project_id):
        wp_type = (wp.get("_embedded", {}).get("type") or {}).get("name", "")
        if wp_type != USER_STORY_TYPE_NAME:
            continue
        stories.append(
            (int(wp["id"]), get_sequence(wp), wp.get("subject") or "")
        )
    stories.sort(key=lambda r: (r[1] is None, r[1] if r[1] is not None else 0, r[0]))
    return stories


def wp_ids_in_priority_order(project_id: int) -> list[int]:
    """Bootstrap order: priority DESC, createdAt ASC.

    Returns just the WP IDs (in the priority+createdAt order). Used by
    bootstrap.py for initial sequencing of unsequenced projects.
    """
    from .client import fetch_full_wp

    ids: list[int] = []
    offset = 1
    page_size = 100
    while True:
        data = get(
            f"/api/v3/projects/{project_id}/work_packages",
            {
                "pageSize": page_size,
                "offset": offset,
                "sortBy": '[["priority","desc"],["createdAt","asc"]]',
            },
        )
        if data is None or data.get("_type") == "NotFound":
            break
        elements = data.get("_embedded", {}).get("elements", [])
        if not elements:
            break
        ids.extend(int(wp["id"]) for wp in elements if wp.get("id") is not None)
        total = data.get("total", 0)
        if len(ids) >= total:
            break
        offset += page_size

    # Filter to User Story type only — requires per-WP fetch (see list_user_stories).
    from .client import USER_STORY_TYPE_NAME

    user_story_ids: list[int] = []
    for wid in ids:
        detail = fetch_full_wp(wid, embed="type")
        if detail and (detail.get("_embedded", {}).get("type") or {}).get("name") == USER_STORY_TYPE_NAME:
            user_story_ids.append(wid)
    return user_story_ids
