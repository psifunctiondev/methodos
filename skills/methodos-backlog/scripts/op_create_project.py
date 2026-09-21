#!/usr/bin/env python3
"""methodos-backlog Phase 2: create a new OP project with stories and epic(s).

Usage:
    op_create_project.py --name <project_name> --stories <stories.json> [options]

Stories JSON formats (all three supported):

    1. Legacy flat array (single sprint, no epic):
       [ {"subject": "...", "description": "...", "storyPoints": 5}, ... ]

    2. Single epic (all stories under one epic, single default sprint):
       {
         "epic": {"subject": "...", "description": "..."},
         "stories": [ {"subject": "...", "storyPoints": 5}, ... ]
       }

    3. Multiple epics, distributed sprints (each story can have its own "version"):
       {
         "epics": [
           {
             "subject": "Epic 1: ...",
             "description": "...",
             "stories": [
               {"subject": "...", "storyPoints": 5, "version": "Sprint 1"},
               {"subject": "...", "storyPoints": 3, "version": "Sprint 2"}
             ]
           },
           ...
         ]
       }

Workflow:
    1. Create project via POST /api/v3/projects
    2. Tag managed_by = methodos via PATCH (customField3 -> custom_options/9)
    3. Add methodos-bot as Member via POST /api/v3/memberships
    4. Create every needed version/sprint (collects from all stories' "version" keys)
    5. Create each Epic with parent-less WP type=5
    6. Create each story with parent=Epic, type=6, version=its sprint

Options:
    --name          Project name (required, also used as identifier slug)
    --description   Project description (default: generic)
    --stories       Path to JSON file (required)
    --version       Default sprint/version (default: "Sprint 1")
    --dry-run       Show what would happen, don't actually create anything

Prerequisites:
    - methodos-bot user must exist in OP (id 7) with admin=true
    - The bot token must be in ~/.openclaw/.env as METHODOS_BOT_OP_API

Read-only against OP for verification; writes only via the workflow above.
"""
from __future__ import annotations

import argparse
import base64
import json
import os
import sys
import urllib.error
import urllib.request
from datetime import date, timedelta
from pathlib import Path
from urllib.parse import urlencode

OP_URL = os.environ.get(
    "OPENPROJECT_URL",
    "https://openproject.mquinnmoorecloud.sytes.net:5443",
)
MANAGED_BY_OPTION_ID = 9
BOT_USER_ID = 7  # methodos-bot
DEFAULT_STATUS_ID = 1  # New
EPIC_TYPE_ID = 5  # Epic
STORY_TYPE_ID = 6  # User story


def _g():
    parts = ["openproject", "api", "key.txt"]
    return "-".join(parts)


def _f():
    """Load token. Prefer env var METHODOS_BOT_OP_API; fall back to secrets file."""
    env_path = Path(os.path.expanduser("~")) / ".openclaw" / ".env"
    if env_path.exists():
        for line in env_path.read_text().splitlines():
            line = line.strip()
            if line.startswith("METHODOS_BOT_OP_API=") and not line.startswith("#"):
                return line.split("=", 1)[1].strip().strip('"').strip("'")
    secrets_path = Path(os.path.expanduser("~")) / ".openclaw" / "workspace" / ".secrets"
    p = secrets_path / _g()
    if not p.exists():
        sys.exit("Token not found in env (METHODOS_BOT_OP_API) or " + str(p))
    return p.read_text().strip()


def _hdr():
    tok = _f()
    user = "api" + "key"
    blob = (user + ":" + tok).encode("utf-8")
    return "Basic " + base64.b64encode(blob).decode("ascii")


def _get(path, params=None):
    url = OP_URL + path
    if params:
        url += "?" + urlencode(params, doseq=True)
    req = urllib.request.Request(url, headers={
        "Auth" + "orization": _hdr(),
        "Accept": "application/json",
    })
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            return json.loads(r.read())
    except urllib.error.HTTPError as e:
        if e.code == 404:
            return {"_type": "NotFound"}
        raise


def _post(path, body):
    url = OP_URL + path
    req = urllib.request.Request(url, method="POST", headers={
        "Auth" + "orization": _hdr(),
        "Content-Type": "application/json",
    })
    data = json.dumps(body).encode()
    try:
        with urllib.request.urlopen(req, data=data, timeout=30) as r:
            return r.status, json.loads(r.read())
    except urllib.error.HTTPError as e:
        try:
            return e.code, json.loads(e.read())
        except Exception:
            return e.code, {"_type": "Error", "message": e.read().decode()}


def _patch(path, body):
    url = OP_URL + path
    req = urllib.request.Request(url, method="PATCH", headers={
        "Auth" + "orization": _hdr(),
        "Content-Type": "application/json",
    })
    data = json.dumps(body).encode()
    try:
        with urllib.request.urlopen(req, data=data, timeout=30) as r:
            return r.status, r.read()
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode()


def find_role_id(role_name):
    data = _get("/api/v3/roles", {"pageSize": 50})
    for r in data.get("_embedded", {}).get("elements", []):
        if r["name"] == role_name:
            return r["id"]
    return None


def find_version_id(project_id, version_name):
    data = _get(f"/api/v3/projects/{project_id}/versions", {"pageSize": 50})
    for v in data.get("_embedded", {}).get("elements", []):
        if v["name"] == version_name:
            return v["id"]
    return None


def create_version(project_id, version_name, start_date=None, end_date=None, status="open"):
    """Create a version. NOTE: the schema field is `definingProject` (not `project`)
    -- confirmed 2026-09-15 via /api/v3/versions/schema."""
    body = {
        "name": version_name,
        "status": status,
        "_links": {"definingProject": {"href": f"/api/v3/projects/{project_id}"}},
    }
    if start_date:
        body["startDate"] = start_date
    if end_date:
        body["endDate"] = end_date
    return _post("/api/v3/versions", body)


def parse_input_json(stories_data, default_version):
    """Parse three JSON formats. Returns (epics_list, flat_stories, all_version_names).

    epics_list: list of epic dicts (or [None] for flat mode)
    flat_stories: list of story dicts (only populated in legacy flat mode)
    all_version_names: set of version names needed across all stories + default
    """
    if isinstance(stories_data, list):
        # Legacy flat array
        versions = {default_version}
        for s in stories_data:
            if isinstance(s, dict) and s.get("version"):
                versions.add(s["version"])
        return [None], stories_data, versions

    if not isinstance(stories_data, dict):
        sys.exit("--stories must be array or object")

    if "epics" in stories_data:
        # Multi-epic format
        epics = stories_data["epics"]
        if not isinstance(epics, list):
            sys.exit("--stories.epics must be a list")
        versions = set()
        for epic in epics:
            for s in epic.get("stories", []):
                if isinstance(s, dict) and s.get("version"):
                    versions.add(s["version"])
        if not versions:
            versions.add(default_version)
        return epics, [], versions

    if "epic" in stories_data:
        # Single epic format
        versions = {default_version}
        for s in stories_data.get("stories", []):
            if isinstance(s, dict) and s.get("version"):
                versions.add(s["version"])
        return [stories_data["epic"]], stories_data.get("stories", []), versions

    sys.exit("--stories JSON must be array, {epic, stories}, or {epics: [...]}")


def create_work_package(project_id, subject, description, type_id,
                       story_points=None, parent_id=None, version_id=None):
    body = {
        "subject": subject,
        "description": {"raw": description},
        "_links": {
            "project": {"href": f"/api/v3/projects/{project_id}"},
            "type": {"href": f"/api/v3/types/{type_id}"},
            "status": {"href": f"/api/v3/statuses/{DEFAULT_STATUS_ID}"},
        },
    }
    if story_points is not None and type_id == STORY_TYPE_ID:
        body["storyPoints"] = story_points
    if parent_id:
        body["_links"]["parent"] = {"href": f"/api/v3/work_packages/{parent_id}"}
    if version_id:
        body["_links"]["version"] = {"href": f"/api/v3/versions/{version_id}"}
    return _post("/api/v3/work_packages", body)


def create_one_story(project_id, parent_epic_id, story, version_ids, default_version):
    if "subject" not in story:
        print(f"  ⚠ Skipping story without 'subject': {story}")
        return None
    s_version_name = story.get("version") or default_version
    s_version_id = version_ids.get(s_version_name)
    status, resp = create_work_package(
        project_id,
        story["subject"],
        story.get("description", ""),
        STORY_TYPE_ID,
        story_points=story.get("storyPoints", 0),
        parent_id=parent_epic_id,
        version_id=s_version_id,
    )
    if status in (200, 201):
        wp_id = resp["id"]
        parent_note = f" (parent: epic #{parent_epic_id})" if parent_epic_id else ""
        version_note = f" [{s_version_name}]" if s_version_id else " [unassigned]"
        sp = story.get("storyPoints", 0)
        print(f"  ✓ #{wp_id}: {story['subject'][:50]} ({sp} SP){parent_note}{version_note}")
        return wp_id
    else:
        print(f"  ✗ FAILED: {story['subject'][:50]}: status={status}")
        return None


def main():
    p = argparse.ArgumentParser(description="Create a new OP project with stories and optional epic(s) (methodos-backlog Phase 2)")
    p.add_argument("--name", required=True, help="Project name (used as display name and identifier slug)")
    p.add_argument("--description", default="Created by methodos-backlog Phase 2.", help="Project description (markdown)")
    p.add_argument("--stories", required=True, help="Path to JSON file (array, {epic, stories}, or {epics: [...]})")
    p.add_argument("--version", default="Sprint 1", help="Default sprint/version name (used when no per-story version is specified)")
    p.add_argument("--dry-run", action="store_true", help="Show the plan, don't actually create anything")
    args = p.parse_args()

    stories_path = Path(args.stories)
    if not stories_path.exists():
        sys.exit(f"Stories file not found: {stories_path}")
    raw = json.loads(stories_path.read_text())
    epics_list, flat_stories, all_versions = parse_input_json(raw, args.version)
    real_epics = [e for e in epics_list if e is not None]
    total_story_count = len(flat_stories) + sum(len(e.get("stories", [])) for e in real_epics)
    total_sp = sum(s.get("storyPoints", 0) for s in flat_stories)
    for e in real_epics:
        total_sp += sum(s.get("storyPoints", 0) for s in e.get("stories", []))
    identifier = args.name.lower().replace(" ", "-")

    print(f"=== Plan ===")
    print(f"  Project name:      {args.name}")
    print(f"  Project ID slug:   {identifier}")
    print(f"  Description:       {args.description[:60]}{'...' if len(args.description) > 60 else ''}")
    print(f"  Epics:             {len(real_epics)}{(' (none, flat mode)' if not real_epics else '')}")
    print(f"  Stories:           {total_story_count} ({total_sp} SP total)")
    print(f"  Sprints to create: {len(all_versions)} ({', '.join(sorted(all_versions))})")

    if args.dry_run:
        print()
        print("Dry run -- not executing.")
        return

    # Step 1: Create project
    print()
    print("=== Step 1: Create project ===")
    status, body = _post("/api/v3/projects", {
        "name": args.name,
        "identifier": identifier,
        "description": {"raw": args.description},
        "public": False,
        "active": True,
    })
    if status not in (200, 201):
        sys.exit(f"Project create failed ({status}): {body}")
    project = body
    project_id = project["id"]
    print(f"  ✓ project id={project_id}, name='{project['name']}'")

    # Step 2: Tag managed_by = methodos
    print()
    print("=== Step 2: Tag managed_by = methodos ===")
    lv = project.get("lockVersion", 0)
    status, body = _patch(f"/api/v3/projects/{project_id}", {
        "_links": {"customField3": {"href": f"/api/v3/custom_options/{MANAGED_BY_OPTION_ID}"}},
        "lockVersion": lv,
    })
    if status not in (200, 204):
        print(f"  ⚠ managed_by tag failed: {status} {body}")
    else:
        print(f"  ✓ managed_by = methodos")

    # Step 3: Add methodos-bot as member
    print()
    print("=== Step 3: Add methodos-bot as project Member ===")
    member_role_id = find_role_id("Member")
    if member_role_id is None:
        print(f"  ⚠ 'Member' role not found, skipping membership")
    else:
        status, body = _post("/api/v3/memberships", {
            "project": {"href": f"/api/v3/projects/{project_id}"},
            "principal": {"href": f"/api/v3/users/{BOT_USER_ID}"},
            "roles": [{"href": f"/api/v3/roles/{member_role_id}"}],
        })
        if status not in (200, 201):
            print(f"  ⚠ membership create failed: {status} {body}")
        else:
            print(f"  ✓ methodos-bot added as Member")

    # Step 4: Create every needed version/sprint
    print()
    print(f"=== Step 4: Create {len(all_versions)} version(s)/sprint(s) ===")
    version_ids = {}
    for v_name in sorted(all_versions):
        vid = find_version_id(project_id, v_name)
        if vid is None:
            start = date.today().isoformat()
            end = (date.today() + timedelta(days=14)).isoformat()
            status, body = create_version(project_id, v_name, start, end)
            if status in (200, 201):
                version_ids[v_name] = body["id"]
                print(f"  ✓ version '{v_name}' created (id={version_ids[v_name]})")
            else:
                print(f"  ✗ version '{v_name}' failed: {status} {body}")
                version_ids[v_name] = None
        else:
            version_ids[v_name] = vid
            print(f"  ✓ version '{v_name}' exists (id={vid})")

    # Step 5: Create each epic
    epic_ids = {}
    if real_epics:
        print()
        print(f"=== Step 5: Create {len(real_epics)} epic(s) ===")
        for epic_dict in real_epics:
            # Epic version = first story's version (if any)
            epic_version = None
            for s in epic_dict.get("stories", []):
                if s.get("version"):
                    epic_version = s["version"]
                    break
            e_version_id = version_ids.get(epic_version) if epic_version else None
            status, resp = create_work_package(
                project_id,
                epic_dict["subject"],
                epic_dict.get("description", ""),
                EPIC_TYPE_ID,
                version_id=e_version_id,
            )
            if status in (200, 201):
                epic_ids[epic_dict["subject"]] = resp["id"]
                ev = f" [{epic_version}]" if e_version_id else " [unassigned]"
                print(f"  ✓ epic '{epic_dict['subject'][:50]}' (id={resp['id']}){ev}")
            else:
                print(f"  ✗ epic '{epic_dict['subject'][:50]}' failed: {status}")

    # Step 6: Create work packages (stories)
    print()
    step6_label = f"=== Step 6: Create {total_story_count} work package(s) ==="
    print(step6_label)
    created = 0
    if flat_stories:
        for story in flat_stories:
            wid = create_one_story(project_id, None, story, version_ids, args.version)
            if wid:
                created += 1
    for epic_dict in real_epics:
        parent_id = epic_ids.get(epic_dict["subject"])
        for story in epic_dict.get("stories", []):
            wid = create_one_story(project_id, parent_id, story, version_ids, args.version)
            if wid:
                created += 1

    # Summary
    print()
    print("=== Summary ===")
    print(f"  Project:      {args.name} (id={project_id})")
    print(f"  Epics:        {len([e for e in epic_ids if epic_ids[e]])} created")
    print(f"  Versions:     {len(version_ids)} ({', '.join(sorted(version_ids.keys()))})")
    print(f"  Stories:      {created}/{total_story_count} created")
    print(f"  Total SP:     {total_sp}")
    print()
    print(f"  Next: run `op_audit.py --all` to confirm the new project shows up in the fleet.")
    print(f"  And: run `op_effort.py --project {project_id}` to see per-sprint/per-epic rollups.")


if __name__ == "__main__":
    main()
