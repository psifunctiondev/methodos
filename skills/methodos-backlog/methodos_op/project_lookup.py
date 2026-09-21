"""Project lookups by Discord thread id and display-name helpers.

`discord_thread_id` is a String custom field on Project type (id 5 in
the current install). Its value is stored flat on the project payload
as `customField5: "<thread-id>"`. Verified against SAZB2026 Site Build
(id 12) on 2026-09-17 — value reads as `customField5: '1549497582001070090'`.
"""
from __future__ import annotations

from .client import get
from .config import DISCORD_THREAD_ID_FIELD_ID, MANAGED_BY_FIELD_ID, MANAGED_BY_OPTION_ID

THREAD_ID_KEY = "customField" + str(DISCORD_THREAD_ID_FIELD_ID)


def _iter_all_projects() -> list[dict]:
    """Return all OP projects as a list of project payloads."""
    data = get("/api/v3/projects", {"pageSize": 100})
    if data is None or data.get("_type") == "NotFound":
        return []
    return data.get("_embedded", {}).get("elements", []) or []


def find_project_by_thread_id(thread_id: str, managed_only: bool = True) -> dict | None:
    """Find an OP project by its discord_thread_id custom field value.

    Iterates all projects (paginated once, pageSize=100) and matches
    the `customField5` flat value. If `managed_only=True`, also filters
    to projects whose `managed_by` tag matches the configured option id.
    """
    thread_id = str(thread_id).strip()
    needle_link = f"/custom_options/{MANAGED_BY_OPTION_ID}"
    for p in _iter_all_projects():
        if managed_only:
            mgmt = (p.get("_links", {}) or {}).get(
                f"customField{MANAGED_BY_FIELD_ID}", {}
            )
            if not mgmt.get("href", "").endswith(needle_link):
                continue
        if str(p.get(THREAD_ID_KEY, "")).strip() == thread_id:
            return p
    return None


def project_display_name(project: dict | int) -> str:
    """Return a friendly display name for a project (id or payload)."""
    if isinstance(project, int):
        data = get(f"/api/v3/projects/{project}")
        if data is None or data.get("_type") == "NotFound":
            return f"#{project}"
        project = data
    name = project.get("name")
    if name:
        return f"{name} (id={project.get('id', '?')})"
    return f"#{project.get('id', '?')}"
