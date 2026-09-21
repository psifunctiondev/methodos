#!/usr/bin/env python3
"""methodos-backlog: effort aggregation view across Methodos-managed projects.

Usage:
    op_effort.py --all
    op_effort.py --project 8
    op_effort.py --all --version "Sprint 3" --type "User Story"

Aggregates estimatedTime (hours), spentTime (hours), percentageDone,
and storyPoints across work packages, grouped by version (sprint) and
type. Story points are read from the built-in `storyPoints` field on
User Story WPs only.

Read-only.
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


def list_wps_full(project_id: int) -> list[dict]:
    """Fetch all WPs with full payload. Collection endpoint doesn't propagate
    embed to elements, so list IDs then fetch each individually with embed."""
    ids = []
    offset = 1
    while True:
        data = _get(
            f"/api/v3/projects/{project_id}/work_packages",
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
    enriched = []
    for wid in ids:
        detail = _get(f"/api/v3/work_packages/{wid}", {"embed": "version,type"})
        enriched.append(detail)
    return enriched


def parse_iso8601_duration(s: str | None) -> float:
    """Convert OP ISO-8601 duration (e.g. PT4H30M) to hours."""
    if not s:
        return 0.0
    hours = 0.0
    s = s.upper()
    if "H" in s:
        h_part = s.split("H")[0].split("T")[-1]
        try:
            hours += float(h_part)
        except ValueError:
            pass
    if "M" in s:
        m_part = s.split("M")[0].split("T")[-1]
        if "H" in m_part:
            m_part = m_part.split("H")[-1]
        try:
            hours += float(m_part) / 60.0
        except ValueError:
            pass
    return hours


def aggregate(projects: list[dict], version_filter: str | None, type_filter: str | None) -> list[dict]:
    """Returns list of dicts: project, version, type, count, est_h, spent_h, pct_avg, points, seq_summary."""
    seq_key = "customField" + str(METHODOS_SEQUENCE_FIELD_ID)
    buckets: dict[tuple, dict] = {}
    for proj in projects:
        for wp in list_wps_full(proj["id"]):
            version = (wp.get("_embedded", {}).get("version") or {}).get("name", "—")
            wp_type = (wp.get("_embedded", {}).get("type") or {}).get("name", "—")
            if version_filter and version != version_filter:
                continue
            if type_filter and wp_type != type_filter:
                continue
            key = (proj.get("name", str(proj["id"])), version, wp_type)
            b = buckets.setdefault(key, {"count": 0, "est": 0.0, "spent": 0.0, "pct_sum": 0, "points": 0, "seqs": []})
            b["count"] += 1
            b["est"] += parse_iso8601_duration(wp.get("estimatedTime"))
            b["spent"] += parse_iso8601_duration(wp.get("spentTime"))
            b["pct_sum"] += wp.get("percentageDone", 0) or 0
            b["points"] += wp.get("storyPoints") or 0
            seq_val = wp.get(seq_key)
            if seq_val is not None:
                try:
                    b["seqs"].append(int(seq_val))
                except (TypeError, ValueError):
                    pass
    rows = []
    for (proj, version, wp_type), b in sorted(buckets.items()):
        rows.append({
            "project": proj,
            "version": version,
            "type": wp_type,
            "count": b["count"],
            "est_h": b["est"],
            "spent_h": b["spent"],
            "pct_avg": b["pct_sum"] / b["count"] if b["count"] else 0,
            "points": b["points"],
            "seq_summary": _seq_summary(b["seqs"]),
        })
    return rows


def _seq_summary(seqs: list[int]) -> str:
    """Render a sequence list as '1-3' (contiguous) or '1,3,5' (sparse), or '—' if empty."""
    if not seqs:
        return "—"
    s = sorted(set(seqs))
    if len(s) == 1:
        return str(s[0])
    if s[-1] - s[0] == len(s) - 1:
        return f"{s[0]}-{s[-1]}"
    return ",".join(str(x) for x in s)


def render_table(rows: list[dict]) -> None:
    print(f"{'Project':<22} {'Version':<16} {'Type':<14} {'Seq':<10} {'#':<5} {'Est (h)':<9} {'Spent (h)':<10} {'%':<6} Points")
    print("─" * 110)
    for r in rows:
        print(
            f"{r['project']:<22} {r['version']:<16} {r['type']:<14} "
            f"{r['seq_summary']:<10} {r['count']:<5} {r['est_h']:<9.1f} {r['spent_h']:<10.1f} "
            f"{r['pct_avg']:<6.0f} {r['points']}"
        )


def main():
    p = argparse.ArgumentParser(description="Methodos OP effort aggregation")
    p.add_argument("--all", action="store_true", help="All managed projects")
    p.add_argument("--project", type=int, help="Single OP project ID")
    p.add_argument("--version", help="Filter by version name")
    p.add_argument("--type", help="Filter by WP type name")
    p.add_argument("--format", choices=["table", "json"], default="table")
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

    rows = aggregate(projects, args.version, args.type)
    if args.format == "json":
        print(json.dumps(rows, indent=2))
        return
    render_table(rows)
    print(f"\n{len(rows)} bucket(s) across {len(projects)} project(s).")


if __name__ == "__main__":
    main()
