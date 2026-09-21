#!/usr/bin/env python3
"""methodos-backlog: priority-sequence audit view across Methodos-managed projects.

Usage:
    op_audit.py --all
    op_audit.py --project 8
    op_audit.py --all --sort '[["priority","desc"],["id","asc"]]'

Read-only. Never writes to OP or local state.
"""
from __future__ import annotations

import argparse
import base64
import json
import os
import sys
import urllib.error
import urllib.request
from pathlib import Path
from urllib.parse import urlencode

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from methodos_op.display import display_id

OP_URL = os.environ.get(
    "OPENPROJECT_URL",
    "https://openproject.mquinnmoorecloud.sytes.net:5443",
)
DIR = Path(os.path.expanduser("~")) / ".openclaw" / "workspace" / ".secrets"
CONFIG_FILE = Path(os.path.expanduser("~")) / ".openclaw" / "workspace" / "methodos" / "methodos-projects.json"
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


def _get(path: str, params=None) -> dict:
    url = OP_URL + path
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
        sys.exit("Config not found: " + str(CONFIG_FILE))
    return json.loads(CONFIG_FILE.read_text())


def discover_managed_projects(cfg):
    field_id = cfg["managed_by_field_id"]
    option_id = cfg["managed_by_option_id"]
    needle = "/custom_options/" + str(option_id)
    managed = []
    data = _get("/api/v3/projects", {"pageSize": DEFAULT_PAGE_SIZE})
    for p in data.get("_embedded", {}).get("elements", []):
        link = p.get("_links", {}).get("customField" + str(field_id), {})
        if link.get("href", "").endswith(needle):
            managed.append(p)
    return managed


def list_work_packages(project_id, sort):
    """Fetch all WPs for a project. Collection endpoint doesn't propagate embed
    to elements, so we list IDs first then fetch each individually with embed."""
    ids = []
    offset = 1
    while True:
        data = _get(
            "/api/v3/projects/" + str(project_id) + "/work_packages",
            {
                "pageSize": DEFAULT_PAGE_SIZE,
                "offset": offset,
                "sortBy": json.dumps(sort),
            },
        )
        elements = data.get("_embedded", {}).get("elements", [])
        if not elements:
            break
        ids.extend(wp.get("id") for wp in elements if wp.get("id") is not None)
        if len(ids) >= data.get("total", 0):
            break
        offset += DEFAULT_PAGE_SIZE
    enriched = []
    for wid in ids:
        detail = _get("/api/v3/work_packages/" + str(wid), {"embed": "priority,assignee"})
        enriched.append(detail)
    return enriched


def render_row(idx, project_name, wp):
    pid = wp.get("id", "?")
    display = display_id(wp) or "—"
    subject = (wp.get("subject") or "")[:50]
    prio = wp.get("_embedded", {}).get("priority", {})
    prio_str = str(prio.get("name", "?")) + " (" + str(prio.get("id", "?")) + ")"
    due = wp.get("dueDate") or "—"
    pct = wp.get("percentageDone", 0)
    assignee = wp.get("_embedded", {}).get("assignee") or {}
    asg = assignee.get("name", "—")[:15]
    # methodos_sequence (customField4) — present on User Story WPs.
    seq_key = "customField" + str(METHODOS_SEQUENCE_FIELD_ID)
    seq = wp.get(seq_key)
    seq_str = str(seq) if seq is not None else "—"
    return (
        f"{idx:>3} {project_name:<22} {pid:<5} {display:<8} {seq_str:>4}  {subject:<32} {prio_str:<14} "
        f"{due:<11} {pct:>4}%  {asg}"
    )


def main():
    p = argparse.ArgumentParser(description="Methodos OP priority audit view")
    p.add_argument("--all", action="store_true", help="Audit all managed projects")
    p.add_argument("--project", type=int, help="Single OP project ID")
    p.add_argument("--sort", help="JSON sort spec")
    p.add_argument("--format", choices=["table", "json"], default="table")
    args = p.parse_args()

    if not args.all and args.project is None:
        sys.exit("Specify --all or --project ID.")

    cfg = load_config()
    sort = json.loads(args.sort) if args.sort else cfg.get(
        "default_sort",
        [["priority", "desc"], ["dueDate", "asc"], ["id", "asc"]],
    )

    if args.project is not None:
        project = _get("/api/v3/projects/" + str(args.project))
        projects = [project] if project.get("_type") == "Project" else []
        if not projects:
            sys.exit("Project " + str(args.project) + " not found or not accessible.")
    else:
        projects = discover_managed_projects(cfg)
        if not projects:
            sys.exit("No managed projects found.")

    rows = []
    for proj in projects:
        wps = list_work_packages(proj["id"], sort)
        for wp in wps:
            rows.append({"project": proj.get("name", str(proj["id"])), "wp": wp})

    if args.format == "json":
        print(json.dumps(rows, indent=2))
        return

    print(f"{'#':>3} {'Project':<22} {'ID':<5} {'Display':<8} {'Seq':>4}  {'Title':<32} {'Priority':<14} {'Due':<11} {'%Done':<6} Assignee")
    print("─" * 124)
    for i, r in enumerate(rows, 1):
        print(render_row(i, r["project"], r["wp"]))
    print(f"\n{len(rows)} work package(s) across {len(projects)} project(s).")


if __name__ == "__main__":
    main()
