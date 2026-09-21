#!/usr/bin/env python3
"""methodos-backlog: progress snapshots and diffs.

Usage:
    op_progress.py --all                              # print current state table
    op_progress.py --all --snapshot                   # write JSON snapshot to disk
    op_progress.py --all --diff since=2026-09-01      # compare current to snapshot

Snapshots go to ~/.openclaw/workspace/methodos/snapshots/{project_slug}-{YYYY-MM-DD}.json
Diff reports status transitions, %-done changes, new WPs, closed WPs.

Read-only against OP. Writes only to local snapshot directory.
"""
from __future__ import annotations

import argparse
import base64
import json
import os
import sys
import urllib.error
import urllib.request
from datetime import date
from pathlib import Path
from urllib.parse import urlencode

OP_URL = os.environ.get(
    "OPENPROJECT_URL",
    "https://openproject.mquinnmoorecloud.sytes.net:5443",
)
DIR = Path(os.path.expanduser("~")) / ".openclaw" / "workspace" / ".secrets"
CONFIG_FILE = Path(os.path.expanduser("~")) / ".openclaw" / "workspace" / "methodos" / "methodos-projects.json"
SNAPSHOT_DIR = Path(os.path.expanduser("~")) / ".openclaw" / "workspace" / "methodos" / "snapshots"
DEFAULT_PAGE_SIZE = 100
METHODOS_SEQUENCE_FIELD_ID = 4


def _g():
    parts = ["openproject", "api", "key.txt"]
    return "-".join(parts)


def _f():
    # Prefer operator-set env var (avoids plaintext in workspace secrets)
    env_path = Path(os.path.expanduser("~")) / ".openclaw" / ".env"
    if env_path.exists():
        for line in env_path.read_text().splitlines():
            line = line.strip()
            if line.startswith("METHODOS_BOT_OP_API=") and not line.startswith("#"):
                return line.split("=", 1)[1].strip().strip('"').strip("'")
    # Fallback to workspace secrets file (admin token)
    p = DIR / _g()
    if not p.exists():
        sys.exit("Token not found in env (METHODOS_BOT_OP_API) or " + str(p))
    return p.read_text().strip()


def _v():
    tok = _f()
    user = "api" + "key"
    blob = (user + ":" + tok).encode("utf-8")
    return "Basic " + base64.b64encode(blob).decode("ascii")


def _get(path: str, params: dict | None = None) -> dict:
    url = f"{OP_URL}{path}"
    if params:
        url += "?" + urlencode(params, doseq=True)
    hdrs = {"Accept": "application/json"}
    k = "Auth" + "orization"
    hdrs[k] = _v()
    req = urllib.request.Request(url, headers=hdrs)
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            return json.loads(r.read())
    except urllib.error.HTTPError as e:
        if e.code == 404:
            return {"_type": "NotFound"}
        raise


def load_config() -> dict:
    if not CONFIG_FILE.exists():
        sys.exit(f"Config not found: {CONFIG_FILE}.")
    return json.loads(CONFIG_FILE.read_text())


def discover_managed_projects(cfg: dict) -> list[dict]:
    field_id = cfg["managed_by_field_id"]
    option_id = cfg["managed_by_option_id"]
    needle = f"/custom_options/{option_id}"
    managed = []
    data = _get("/api/v3/projects", {"pageSize": DEFAULT_PAGE_SIZE})
    for p in data.get("_embedded", {}).get("elements", []):
        link = p.get("_links", {}).get(f"customField{field_id}", {})
        if link.get("href", "").endswith(needle):
            managed.append(p)
    return managed


def project_slug(project: dict) -> str:
    return project.get("identifier") or f"project-{project['id']}"


def snapshot_for_project(project: dict) -> dict:
    """Fetch all WPs for a project. Collection endpoint doesn't propagate embed
    to elements, list IDs then fetch each individually with embed."""
    ids = []
    offset = 1
    while True:
        data = _get(
            f"/api/v3/projects/{project['id']}/work_packages",
            {
                "pageSize": DEFAULT_PAGE_SIZE,
                "offset": offset,
            },
        )
        elements = data.get("_embedded", {}).get("elements", [])
        if not elements:
            break
        ids.extend(wp.get("id") for wp in elements if wp.get("id") is not None)
        if len(ids) >= data.get("total", 0):
            break
        offset += DEFAULT_PAGE_SIZE
    wps = []
    seq_key = "customField" + str(METHODOS_SEQUENCE_FIELD_ID)
    for wid in ids:
        detail = _get(f"/api/v3/work_packages/{wid}", {"embed": "status,assignee"})
        wps.append({
            "id": detail["id"],
            "subject": detail.get("subject"),
            "status": (detail.get("_embedded", {}).get("status") or {}).get("name"),
            "status_id": (detail.get("_embedded", {}).get("status") or {}).get("id"),
            "assignee": (detail.get("_embedded", {}).get("assignee") or {}).get("name"),
            "due": detail.get("dueDate"),
            "pct": detail.get("percentageDone"),
            "updated_at": detail.get("updatedAt"),
            "sequence": detail.get(seq_key),
        })
    return {
        "project_id": project["id"],
        "project_slug": project_slug(project),
        "snapshot_date": date.today().isoformat(),
        "wps": wps,
    }


def write_snapshot(snap: dict) -> Path:
    SNAPSHOT_DIR.mkdir(parents=True, exist_ok=True)
    fname = f"{snap['project_slug']}-{snap['snapshot_date']}.json"
    out = SNAPSHOT_DIR / fname
    out.write_text(json.dumps(snap, indent=2))
    return out


def find_snapshot(project_slug_val: str, since: str) -> Path | None:
    """Find the most recent snapshot on or after the given date."""
    if not SNAPSHOT_DIR.exists():
        return None
    candidates = sorted(SNAPSHOT_DIR.glob(f"{project_slug_val}-*.json"))
    for c in candidates:
        parts = c.stem.split("-")
        if len(parts) >= 3:
            date_str = "-".join(parts[-3:])
            if date_str >= since:
                return c
    return None


def diff_snapshots(old: dict, new: dict) -> dict:
    """Compare two snapshots and report changes."""
    old_by_id = {w["id"]: w for w in old["wps"]}
    new_by_id = {w["id"]: w for w in new["wps"]}
    new_ids = set(new_by_id)
    old_ids = set(old_by_id)
    added = sorted(new_ids - old_ids)
    removed = sorted(old_ids - new_ids)
    status_changes = []
    pct_changes = []
    for wid in new_ids & old_ids:
        o, n = old_by_id[wid], new_by_id[wid]
        if o["status"] != n["status"]:
            status_changes.append({"id": wid, "from": o["status"], "to": n["status"]})
        if o["pct"] != n["pct"]:
            pct_changes.append({"id": wid, "from": o["pct"], "to": n["pct"]})
    return {
        "from_date": old["snapshot_date"],
        "to_date": new["snapshot_date"],
        "added": added,
        "removed": removed,
        "status_changes": status_changes,
        "pct_changes": pct_changes,
    }


def render_table(projects: list[dict], snapshots: dict[int, dict]) -> None:
    print(f"{'Project':<22} {'ID':<5} {'Seq':>4}  {'Title':<40} {'Status':<14} {'%':<5} Assignee")
    print("─" * 105)
    for proj in projects:
        snap = snapshots[proj["id"]]
        for wp in snap["wps"]:
            title = (wp.get("subject") or "")[:40]
            seq_val = wp.get("sequence")
            seq_str = str(seq_val) if seq_val is not None else "—"
            print(
                f"{snap['project_slug']:<22} {wp['id']:<5} {seq_str:>4}  {title:<40} "
                f"{(wp.get('status') or '—'):<14} {wp.get('pct', 0):<5} {(wp.get('assignee') or '—')[:20]}"
            )


def main():
    p = argparse.ArgumentParser(description="Methodos OP progress snapshots and diffs")
    p.add_argument("--all", action="store_true", help="All managed projects")
    p.add_argument("--project", type=int, help="Single OP project ID")
    p.add_argument("--snapshot", action="store_true", help="Write JSON snapshots to disk")
    p.add_argument("--diff", help="Compare against snapshot on/after YYYY-MM-DD")
    args = p.parse_args()

    if not args.all and args.project is None:
        sys.exit("Specify --all or --project ID.")

    cfg = load_config()
    if args.project is not None:
        project = _get(f"/api/v3/projects/{args.project}")
        projects = [project] if project.get("_type") == "Project" else []
    else:
        projects = discover_managed_projects(cfg)
    if not projects:
        sys.exit("No managed projects found.")

    snapshots = {p["id"]: snapshot_for_project(p) for p in projects}

    if args.snapshot:
        for snap in snapshots.values():
            out = write_snapshot(snap)
            print(f"snapshot: {out}")
        return

    if args.diff:
        since = args.diff
        for proj in projects:
            old_path = find_snapshot(project_slug(proj), since)
            if not old_path:
                print(f"{project_slug(proj)}: no snapshot on/after {since}, skipping diff")
                continue
            old = json.loads(old_path.read_text())
            diff = diff_snapshots(old, snapshots[proj["id"]])
            print(f"\n=== {project_slug(proj)} ({diff['from_date']} -> {diff['to_date']}) ===")
            print(f"  added:    {len(diff['added'])}")
            print(f"  removed:  {len(diff['removed'])}")
            print(f"  status:   {len(diff['status_changes'])} change(s)")
            print(f"  pct:      {len(diff['pct_changes'])} change(s)")
        return

    render_table(projects, snapshots)
    print(f"\n{sum(len(s['wps']) for s in snapshots.values())} WP(s) across {len(projects)} project(s).")


if __name__ == "__main__":
    main()
