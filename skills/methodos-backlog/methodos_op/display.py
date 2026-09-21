"""Display ID computation: eN-sM format from methodos_epic_number + methodos_story_number.

Set once (by numbering.py), stable across priority reorder, decomposition,
and most other lifecycle events. Composed at display time, not stored.

Performance: resolve_display_id() uses a per-process cache of project WP
maps (epic_number -> epic_id, (epic_number, story_number) -> story_id) so
each resolve is O(1) instead of O(N). First call per project builds the
maps (1 + N API calls); subsequent calls are pure dict lookups. Cache
persists for the CLI invocation; call clear_cache() between separate
invocations if the project's WPs have changed.
"""
from __future__ import annotations

import re
from typing import Optional

from .client import fetch_full_wp, get
from .config import (
    METHODOS_EPIC_NUMBER_FIELD_ID,
    METHODOS_STORY_NUMBER_FIELD_ID,
)

EPIC_NUM_KEY = "customField" + str(METHODOS_EPIC_NUMBER_FIELD_ID)
STORY_NUM_KEY = "customField" + str(METHODOS_STORY_NUMBER_FIELD_ID)
DEFAULT_PAGE_SIZE = 100

# Pattern matches: e2, e2-s3, and nested forms like e2-s3-t1.
DISPLAY_ID_RE = re.compile(r"^e(\d+)(?:-([a-z]+\d+))*$")

# Per-process caches: project_id -> map. Populated lazily on first resolve.
# Populated lazily on first resolve for a project; persists for the
# CLI invocation lifetime. Use clear_cache() if WPs change between runs.
_EPIC_MAP_CACHE: dict[int, dict[int, int]] = {}
_STORY_MAP_CACHE: dict[int, dict[tuple[int, int], int]] = {}


def display_id(wp: dict) -> str:
    """Return 'eN' for an Epic, 'eN-sM' for a User Story, '' otherwise.

    Numbers come from methodos_epic_number (id 6) and methodos_story_number (id 7).
    Set once via numbering.py; doesn't change with priority reorder.
    """
    epic_num = wp.get(EPIC_NUM_KEY)
    if epic_num is None:
        return ""
    story_num = wp.get(STORY_NUM_KEY)
    if story_num is None:
        return f"e{int(epic_num)}"
    return f"e{int(epic_num)}-s{int(story_num)}"


def resolve_display_id(project_id: int, display_id_str: str) -> Optional[int]:
    """Resolve 'e2-s3' (or 'e2' for an epic) to a WP id in the project.

    Returns None if not found. First call per project builds the maps
    (O(N) API calls, cached for the process lifetime); subsequent calls
    are O(1) lookups.

    Ambiguous displays (multiple matches) is impossible since epic_number
    and story_number are unique within their scope.
    """
    m = DISPLAY_ID_RE.match((display_id_str or "").strip())
    if not m:
        return None
    epic_num = int(m.group(1))

    # Build cache on first call for this project
    if project_id not in _EPIC_MAP_CACHE:
        _build_project_maps(project_id)

    # Look for the story segment (supports nested forms like e2-s3-t1 later)
    story_num = None
    for seg in display_id_str.split("-"):
        if seg.startswith("s") and seg[1:].isdigit():
            story_num = int(seg[1:])
            break

    epic_map = _EPIC_MAP_CACHE.get(project_id, {})
    story_map = _STORY_MAP_CACHE.get(project_id, {})

    if story_num is None:
        return epic_map.get(epic_num)
    return story_map.get((epic_num, story_num))


def _build_project_maps(project_id: int) -> None:
    """Build and cache the epic + story maps for a project.

    Cost: 1 collection fetch + N individual fetches with embed=type.
    Result is cached at module level for the process lifetime.
    """
    ids: list[int] = []
    offset = 1
    while True:
        data = get(
            f"/api/v3/projects/{project_id}/work_packages",
            {"pageSize": DEFAULT_PAGE_SIZE, "offset": offset},
        )
        if data is None or data.get("_type") == "NotFound":
            break
        elements = data.get("_embedded", {}).get("elements", [])
        if not elements:
            break
        ids.extend(int(w["id"]) for w in elements if w.get("id") is not None)
        if len(ids) >= data.get("total", 0):
            break
        offset += DEFAULT_PAGE_SIZE

    epic_map: dict[int, int] = {}
    story_map: dict[tuple[int, int], int] = {}

    for wid in ids:
        wp = fetch_full_wp(wid, embed="type")
        if wp is None or wp.get("_type") == "NotFound":
            continue

        wp_type = (wp.get("_embedded", {}).get("type") or {}).get("name")
        epic_num = wp.get(EPIC_NUM_KEY)
        story_num = wp.get(STORY_NUM_KEY)

        if wp_type == "Epic" and epic_num is not None:
            epic_map[int(epic_num)] = int(wid)
        elif wp_type == "User story" and epic_num is not None and story_num is not None:
            story_map[(int(epic_num), int(story_num))] = int(wid)

    _EPIC_MAP_CACHE[project_id] = epic_map
    _STORY_MAP_CACHE[project_id] = story_map


def clear_cache() -> None:
    """Clear the display_id lookup cache. Use between separate invocations
    if the project's WPs have changed (e.g., new stories added, numbering re-run)."""
    _EPIC_MAP_CACHE.clear()
    _STORY_MAP_CACHE.clear()
