#!/usr/bin/env python3
"""methodos-backlog: post a status update as a comment to a project's
most-recently-active in-progress work package.

Usage:
    methodos_status_update.py --project 12 --message "..."
    methodos_status_update.py --thread 1549497582001070090 --message "..."
    echo "..." | methodos_status_update.py --project 12 --message -
    methodos_status_update.py --project 12 --message "..." --dry-run
    methodos_status_update.py --project 12 --updated-by "Quinn" --message "..."

Required: either --project or --thread (mutually exclusive). The message
can be passed via --message or piped on stdin (use "-" as the value).

The message is a free-form status body. The script wraps it in the
standard comment format:

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

A literal "## Changes since last update" header in the message body
becomes the changes section; everything else falls into "Blockers" (none
explicit if missing) and "Next steps" (defaults to a placeholder).

Output: the OP comment URL and a one-line recap.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from methodos_op import (
    OP_URL,
    build_status_comment_body,
    find_in_progress_wp,
    find_project_by_thread_id,
    one_line_recap,
    post_status_comment,
    project_display_name,
)


def _read_message(args: argparse.Namespace) -> str:
    if args.message is None:
        raise SystemExit("either --message or stdin is required")
    if args.message == "-":
        return sys.stdin.read()
    return args.message


def _split_message_sections(message: str) -> tuple[str, str, str]:
    """Split a free-form message body into (changes, blockers, next_steps).

    Sections are detected by '## Changes', '## Blockers', '## Next steps'
    headers (case-insensitive). Anything before the first header is folded
    into changes. Missing sections are filled with '(none)' placeholders.
    """
    lines = message.splitlines()
    sections = {"changes": [], "blockers": [], "next_steps": []}
    current = "changes"
    found_any_header = False
    for line in lines:
        ls = line.strip().lower()
        if ls.startswith("## changes"):
            current = "changes"
            found_any_header = True
            continue
        if ls.startswith("## blocker"):
            current = "blockers"
            found_any_header = True
            continue
        if ls.startswith("## next"):
            current = "next_steps"
            found_any_header = True
            continue
        sections[current].append(line)

    def fmt(bucket: list[str], fallback: str) -> str:
        body = "\n".join(bucket).rstrip()
        return body if body else fallback

    if not found_any_header:
        # Whole message treated as the "changes" body; blockers and
        # next_steps get explicit "none" placeholders.
        return fmt(["- " + message.strip()], "- (see changes above)"), fmt([], "- None."), fmt([], "- TBD.")

    changes_body = "\n".join(sections["changes"]).rstrip()
    if not changes_body:
        changes_body = "- (none)"
    elif not any(l.strip().startswith("- ") for l in changes_body.splitlines() if l.strip()):
        # No bullet marker — wrap the whole thing as one bullet.
        changes_body = "- " + changes_body.replace("\n", " ").strip()
    return (
        changes_body,
        fmt(sections["blockers"], "- None."),
        fmt(sections["next_steps"], "- TBD."),
    )


def _project(args: argparse.Namespace) -> dict:
    if args.project is not None:
        from methodos_op import get
        p = get(f"/api/v3/projects/{args.project}")
        if p is None or p.get("_type") == "NotFound":
            raise SystemExit(f"project {args.project} not found or not accessible")
        return p
    if args.thread is not None:
        p = find_project_by_thread_id(args.thread, managed_only=False)
        if p is None:
            raise SystemExit(f"no project with discord_thread_id={args.thread!r}")
        return p
    raise SystemExit("either --project or --thread is required")


def main() -> None:
    p = argparse.ArgumentParser(description="Post a methodos status update to a project's most-recently-active in-progress WP")
    p.add_argument("--project", type=int, help="OP project id")
    p.add_argument("--thread", help="Discord thread id (resolves to a project via the discord_thread_id custom field)")
    p.add_argument("--message", help='Free-form status body, or "-" to read from stdin')
    p.add_argument("--updated-by", default="Doxa", help="Display name to record in the comment (default: Doxa)")
    p.add_argument("--dry-run", action="store_true", help="Compose the comment and print it without POSTing")
    args = p.parse_args()

    project = _project(args)
    project_id = int(project["id"])
    project_name = project.get("name", f"#{project_id}")
    wp = find_in_progress_wp(project_id)
    if wp is None:
        raise SystemExit(f"project {project_id} ({project_name}) has no in-progress WP")

    message = _read_message(args)
    changes, blockers, next_steps = _split_message_sections(message)
    body = build_status_comment_body(
        project_name=project_name,
        project_id=project_id,
        updated_by=args.updated_by,
        changes=changes,
        blockers=blockers,
        next_steps=next_steps,
    )

    if args.dry_run:
        print(f"--- dry-run: would POST to WP #{wp['id']} ---")
        print(body)
        print(f"--- end (no PATCH/POST sent) ---")
        return

    status, resp = post_status_comment(wp["id"], body)
    if status not in (200, 201):
        raise SystemExit(f"POST failed ({status}): {resp}")

    # The activity endpoint returns a 201 with the activity payload — link via _links.activity.href or self.
    comment_url = None
    if isinstance(resp, dict):
        comment_url = (resp.get("_links", {}) or {}).get("self", {}).get("href") if (resp.get("_links", {}) or {}).get("self") else None
        if not comment_url:
            activity = (resp.get("_links", {}) or {}).get("activity", {})
            if activity.get("href"):
                comment_url = activity["href"]
        if not comment_url:
            comment_url = (resp.get("_links", {}) or {}).get("comment", {}).get("href")
    full_url = (OP_URL + comment_url) if comment_url and comment_url.startswith("/") else comment_url

    recap = one_line_recap(body)
    print(f"✓ Posted to OP: {full_url or '(no URL returned)'}")
    print(f"  recap: {recap}")
    print(f"  WP: #{wp['id']} — {wp.get('subject')!r}")


if __name__ == "__main__":
    main()
