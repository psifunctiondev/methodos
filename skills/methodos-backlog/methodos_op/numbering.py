"""Auto-populate methodos_epic_number and methodos_story_number.

Walks each managed project's WPs:
- Epics get methodos_epic_number = position by OP ID (1, 2, 3, ...)
- User Stories get methodos_story_number = position by OP ID within their parent epic
- Stories also get methodos_epic_number denormalized onto them (so display_id()
  is O(1) without needing to fetch the parent epic)

Idempotent: only fills fields that are unset. Re-running doesn't shift
existing values. With --force, re-numbers everything (use carefully — this
shifts IDs of stories whose position in the project changes).

Stories without a parent epic are skipped (and reported), since the numbering
scheme requires a parent for story_number assignment.

Usage:
    python3 -m methodos_op.numbering --project 12
    python3 -m methodos_op.numbering --all
    python3 -m methodos_op.numbering --project 12 --force  # shifts numbers
"""
from __future__ import annotations

import argparse
import sys
from typing import Optional

from .client import fetch_full_wp, get, patch
from .config import (
    MANAGED_BY_FIELD_ID,
    MANAGED_BY_OPTION_ID,
    METHODOS_EPIC_NUMBER_FIELD_ID,
    METHODOS_STORY_NUMBER_FIELD_ID,
)

EPIC_TYPE_NAME = "Epic"
USER_STORY_TYPE_NAME = "User story"
EPIC_NUM_KEY = "customField" + str(METHODOS_EPIC_NUMBER_FIELD_ID)
STORY_NUM_KEY = "customField" + str(METHODOS_STORY_NUMBER_FIELD_ID)
DEFAULT_PAGE_SIZE = 100


def _parent_id(wp: dict) -> Optional[int]:
    parent_link = wp.get("_links", {}).get("parent") or {}
    href = parent_link.get("href", "")
    if not href:
        return None
    try:
        return int(href.rstrip("/").split("/")[-1])
    except (ValueError, IndexError):
        return None


def _list_project_wp_ids(project_id: int, page_size: int = DEFAULT_PAGE_SIZE) -> list[int]:
    """List all WP ids in a project (collection endpoint, no embed)."""
    ids: list[int] = []
    offset = 1
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
        ids.extend(int(w["id"]) for w in elements if w.get("id") is not None)
        if len(ids) >= data.get("total", 0):
            break
        offset += page_size
    return ids


def number_project(project_id: int, force: bool = False, verbose: bool = True) -> dict:
    """Assign epic_number to epics and story_number + epic_number to user stories."""
    summary = {
        "project_id": project_id,
        "epics_assigned": 0,
        "epics_skipped": 0,
        "stories_assigned": 0,
        "stories_skipped": 0,
        "stories_no_parent": [],
        "errors": [],
    }
    wp_ids = _list_project_wp_ids(project_id)
    if not wp_ids:
        return summary
    if verbose:
        print(f"  {len(wp_ids)} WPs to inspect")
    # Fetch each with embed=type to know type
    full_wps = []
    for wid in wp_ids:
        wp = fetch_full_wp(wid, embed="type")
        if wp and wp.get("_type") != "NotFound":
            full_wps.append(wp)
    # Partition by type, sorted by OP ID
    epics = sorted(
        [w for w in full_wps if (w.get("_embedded", {}).get("type") or {}).get("name") == EPIC_TYPE_NAME],
        key=lambda w: int(w["id"]),
    )
    user_stories = sorted(
        [w for w in full_wps if (w.get("_embedded", {}).get("type") or {}).get("name") == USER_STORY_TYPE_NAME],
        key=lambda w: int(w["id"]),
    )
    # Assign epic_number
    for i, epic in enumerate(epics, 1):
        if not force and epic.get(EPIC_NUM_KEY) is not None:
            summary["epics_skipped"] += 1
            continue
        status, body = patch(
            f"/api/v3/work_packages/{epic['id']}",
            {"lockVersion": epic["lockVersion"], EPIC_NUM_KEY: i},
        )
        if status == 200:
            summary["epics_assigned"] += 1
            if verbose:
                print(f"  epic #{epic['id']}: {EPIC_NUM_KEY}={i} ({epic.get('subject', '')[:50]})")
        else:
            summary["errors"].append(f"epic #{epic['id']}: status {status}, body={body}")
    # Build epic_id -> epic_number map
    epic_number_by_id: dict[int, int] = {}
    for i, epic in enumerate(epics, 1):
        epic_number_by_id[int(epic["id"])] = i
    # Group stories by parent epic
    stories_by_epic: dict[int, list[dict]] = {}
    for story in user_stories:
        parent = _parent_id(story)
        if parent is None or parent not in epic_number_by_id:
            summary["stories_no_parent"].append({
                "wp_id": story["id"],
                "subject": story.get("subject", ""),
                "parent_id": parent,
            })
            continue
        stories_by_epic.setdefault(parent, []).append(story)
    # Sort each epic's children by OP ID, assign story_number AND denormalize epic_number
    # (so display_id() doesn't need a parent fetch — the story carries both numbers itself)
    for epic_id, children in stories_by_epic.items():
        epic_num = epic_number_by_id[epic_id]
        children.sort(key=lambda w: int(w["id"]))
        for j, story in enumerate(children, 1):
            updates = {"lockVersion": story["lockVersion"]}
            needs_update = False
            if force or story.get(STORY_NUM_KEY) is None:
                updates[STORY_NUM_KEY] = j
                needs_update = True
            if force or story.get(EPIC_NUM_KEY) is None:
                updates[EPIC_NUM_KEY] = epic_num
                needs_update = True
            if not needs_update:
                summary["stories_skipped"] += 1
                continue
            status, body = patch(
                f"/api/v3/work_packages/{story['id']}",
                updates,
            )
            if status == 200:
                summary["stories_assigned"] += 1
                if verbose:
                    print(f"    story #{story['id']} (in epic {epic_id}): {STORY_NUM_KEY}={j}, {EPIC_NUM_KEY}={epic_num} ({story.get('subject', '')[:50]})")
            else:
                summary["errors"].append(f"story #{story['id']}: status {status}, body={body}")
    return summary


def discover_managed_projects() -> list[int]:
    needle = f"/custom_options/{MANAGED_BY_OPTION_ID}"
    data = get("/api/v3/projects", {"pageSize": 100})
    if data is None or data.get("_type") == "NotFound":
        return []
    out: list[int] = []
    for p in data.get("_embedded", {}).get("elements", []):
        link = p.get("_links", {}).get(f"customField{MANAGED_BY_FIELD_ID}", {})
        if link.get("href", "").endswith(needle):
            out.append(int(p["id"]))
    return out


def main() -> int:
    p = argparse.ArgumentParser(description="Auto-populate methodos_epic_number + methodos_story_number")
    p.add_argument("--project", type=int, help="Single project ID")
    p.add_argument("--all", action="store_true", help="All managed projects")
    p.add_argument("--force", action="store_true", help="Re-assign even if set (shifts numbers)")
    args = p.parse_args()
    if not args.all and not args.project:
        sys.exit("specify --project ID or --all")
    if args.project:
        project_ids = [args.project]
    else:
        project_ids = discover_managed_projects()
        print(f"Discovered {len(project_ids)} managed project(s): {project_ids}\n")
    summaries = []
    for pid in project_ids:
        print(f"=== Project {pid} ===")
        s = number_project(pid, force=args.force)
        print(f"  epics:    {s['epics_assigned']} assigned, {s['epics_skipped']} skipped")
        print(f"  stories:  {s['stories_assigned']} assigned, {s['stories_skipped']} skipped")
        if s["stories_no_parent"]:
            print(f"  WARNING {len(s['stories_no_parent'])} User Story(s) without parent epic (skipped):")
            for x in s["stories_no_parent"][:10]:
                print(f"      wp #{x['wp_id']} (parent_id={x['parent_id']}): {x['subject'][:60]}")
            if len(s["stories_no_parent"]) > 10:
                print(f"      ... and {len(s['stories_no_parent']) - 10} more")
        if s["errors"]:
            print(f"  ERROR {len(s['errors'])} error(s)")
            for e in s["errors"][:5]:
                print(f"      {e}")
        summaries.append(s)
        print()
    return 0


if __name__ == "__main__":
    sys.exit(main())
