"""methodos status updates — pick the most-recently-active in-progress WP
in a project and POST a formatted comment to its activity log.

Closed-status detection uses the OP `isClosed` flag on each status (the
16.6.3 install has Deployed (12) and Rejected (14) as closed; "Closed"
or "Done" do not exist literally). For installs that DO have literal
"Closed" or "Done" status names, those will be filtered too.
"""
from __future__ import annotations

import json
from datetime import date
from typing import Optional

from .client import get, post, fetch_full_wp

# Fallback filter: status names that ALWAYS count as "closed" even if
# the OP install doesn't mark them `isClosed=True`. Most installs use
# "Closed" or "Done"; we filter them defensively.
DEFAULT_CLOSED_STATUS_NAMES = {"closed", "done", "deployed", "rejected", "cancelled", "canceled"}


def _load_status_index() -> dict[int, dict]:
    """Return {status_id: status_obj} for the OP install."""
    data = get("/api/v3/statuses")
    if data is None or data.get("_type") == "NotFound":
        return {}
    return {
        int(s["id"]): s
        for s in (data.get("_embedded", {}).get("elements", []) or [])
    }


def _is_closed_status(status_obj: dict | None, status_name: str | None) -> bool:
    if status_obj and status_obj.get("isClosed"):
        return True
    if status_name and status_name.strip().lower() in DEFAULT_CLOSED_STATUS_NAMES:
        return True
    return False


def find_in_progress_wp(project_id: int) -> Optional[dict]:
    """Return the most-recently-updated User Story / task WP whose status
    is NOT closed (i.e. is still actionable).

    Filters: any WP type, any priority. Excludes statuses where
    isClosed=True OR the status name matches `DEFAULT_CLOSED_STATUS_NAMES`.

    Sort: updatedAt DESC. Returns the WP payload (full, with status embed).
    """
    status_index = _load_status_index()
    ids: list[int] = []
    offset = 1
    page_size = 100
    while True:
        data = get(
            f"/api/v3/projects/{project_id}/work_packages",
            {"pageSize": page_size, "offset": offset, "sortBy": '[["updatedAt","desc"]]'},
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

    for wid in ids:
        wp = fetch_full_wp(wid, embed="status")
        if wp is None or wp.get("_type") == "NotFound":
            continue
        st = (wp.get("_embedded", {}).get("status") or {})
        st_id = st.get("id")
        st_name = st.get("name") or ""
        if _is_closed_status(status_index.get(int(st_id)) if st_id is not None else None, st_name):
            continue
        return wp
    return None


def build_status_comment_body(
    project_name: str,
    project_id: int,
    updated_by: str,
    changes: str,
    blockers: str,
    next_steps: str,
    today: str | None = None,
) -> str:
    """Compose the standard status-update comment body.

    Format (confirmed 2026-09-17):
        ---
        [YYYY-MM-DD] Status update
        Project: <name> (id=<N>)
        Updated by: <name>

        ## Changes since last update
        - ...

        ## Blockers
        - ...

        ## Next steps
        - ...
    """
    stamp = today or date.today().isoformat()
    return (
        "---\n"
        f"[{stamp}] Status update\n"
        f"Project: {project_name} (id={project_id})\n"
        f"Updated by: {updated_by}\n"
        "\n"
        "## Changes since last update\n"
        f"{changes.rstrip()}\n"
        "\n"
        "## Blockers\n"
        f"{blockers.rstrip()}\n"
        "\n"
        "## Next steps\n"
        f"{next_steps.rstrip()}\n"
    )


def post_status_comment(
    wp_id: int,
    body_markdown: str,
) -> tuple[int, dict | None]:
    """POST a comment to a WP's activity log.

    Endpoint: POST /api/v3/work_packages/{id}/activities
    Payload:  {"comment": {"raw": "<markdown>"}}
    """
    return post(
        f"/api/v3/work_packages/{wp_id}/activities",
        {"comment": {"raw": body_markdown}},
    )


def one_line_recap(body_markdown: str) -> str:
    """Build a one-line recap from a status-update body. Picks the first
    non-empty bullet under "Changes since last update" if present,
    otherwise the first non-empty line of the body.
    """
    in_changes = False
    for line in body_markdown.splitlines():
        s = line.strip()
        if s.startswith("## "):
            in_changes = s.lower().startswith("## changes")
            continue
        if in_changes and s.startswith("- ") and len(s) > 2:
            return s[2:].rstrip(".")
    # fallback: first non-empty line that isn't metadata
    for line in body_markdown.splitlines():
        s = line.strip()
        if not s or s.startswith("---") or s.startswith("["):
            continue
        if s.startswith("Project:") or s.startswith("Updated by:"):
            continue
        if s.startswith("##"):
            continue
        return s[:120]
    return "(no summary)"
