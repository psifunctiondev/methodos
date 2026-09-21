#!/usr/bin/env python3
"""methodos-backlog: resequence User Story WPs in a project.

Usage:
    op_resequence.py --project ID --order "wp_id1,wp_id2,wp_id3,..."
    op_resequence.py --project ID --order-file path/to/list.txt
    op_resequence.py --project ID --by-subject --order "subject 1,subject 2,..."
    op_resequence.py --project ID --order "..." --dry-run

Order values are WP ids by default. With `--by-subject`, each value must
be the EXACT subject of a User Story in the project (unambiguous match;
errors out if any subject has zero or multiple matches).

Output: a before/after table plus a one-line summary. With `--dry-run`,
no PATCHes are sent — only the plan is printed.
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

# Make sibling package importable when run from anywhere.
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from methodos_op import (
    current_sequences,
    resequence,
    list_stories_with_sequences,
)
from methodos_op.display import resolve_display_id


def _resolve_subject(project_id: int, subject: str) -> int:
    """Find a User Story in the project whose subject matches `subject`
    EXACTLY. Errors on zero or multiple matches."""
    matches = [
        wid for wid, _seq, subj in list_stories_with_sequences(project_id)
        if subj == subject
    ]
    if len(matches) == 0:
        raise SystemExit(f"no User Story with subject {subject!r} in project {project_id}")
    if len(matches) > 1:
        raise SystemExit(
            f"subject {subject!r} is ambiguous in project {project_id}: "
            f"{len(matches)} matches (wp ids: {matches[:5]})"
        )
    return matches[0]


def _parse_order(value: str, by_subject: bool, project_id: int) -> list[int]:
    """Parse the comma-separated --order string into a list of WP ids.

    Each part can be a raw WP id, a display_id (e.g., 'e2-s3' or 'e2'),
    or (with --by-subject) a subject name.
    """
    parts = [p.strip() for p in value.split(",") if p.strip()]
    if not parts:
        raise SystemExit("--order is empty")
    if by_subject:
        return [_resolve_subject(project_id, p) for p in parts]
    out: list[int] = []
    for p in parts:
        # Detect display_id format (e.g., "e2-s3" or "e2")
        if p.startswith("e") and ("-" in p or p[1:].isdigit()):
            wid = resolve_display_id(project_id, p)
            if wid is None:
                raise SystemExit(
                    f"could not resolve display_id {p!r} in project {project_id}.\n"
                    f"  This usually means the project hasn't been auto-numbered yet — run:\n"
                    f"    python3 -m methodos_op.numbering --project {project_id}\n"
                    f"  Or use raw WP ids instead of display_ids."
                )
            out.append(wid)
            continue
        try:
            out.append(int(p))
        except ValueError:
            raise SystemExit(f"non-integer WP id in --order: {p!r} (use --by-subject for subject names)")
    return out


def _read_order_file(path: str) -> list[int]:
    """Read WP ids from a file, one per line."""
    p = Path(path)
    if not p.exists():
        raise SystemExit(f"--order-file not found: {path}")
    out: list[int] = []
    for raw in p.read_text().splitlines():
        s = raw.strip()
        if not s or s.startswith("#"):
            continue
        try:
            out.append(int(s))
        except ValueError:
            raise SystemExit(f"non-integer WP id in --order-file: {s!r}")
    if not out:
        raise SystemExit(f"--order-file is empty: {path}")
    return out


def _render_before_after(before: list[tuple[int, int | None, str]],
                         after: list[tuple[int, int | None, str]],
                         actions: list[dict]) -> None:
    print("=== BEFORE ===")
    print(f"{'Seq':>4}  {'WP':>5}  Subject")
    print("─" * 70)
    for wid, seq, subj in before:
        print(f"{seq if seq is not None else '—':>4}  {wid:>5}  {subj[:60]}")
    print()
    print("=== ACTIONS ===")
    if not actions:
        print("  (no changes)")
    for a in actions:
        print(f"  #{a['wp_id']:>5}: {a['from']} -> {a['to']}")
    print()
    print("=== AFTER ===")
    print(f"{'Seq':>4}  {'WP':>5}  Subject")
    print("─" * 70)
    for wid, seq, subj in after:
        print(f"{seq if seq is not None else '—':>4}  {wid:>5}  {subj[:60]}")


def main() -> None:
    p = argparse.ArgumentParser(description="Resequence User Stories in a project (methodos-backlog)")
    p.add_argument("--project", type=int, required=True, help="OP project id")
    src = p.add_mutually_exclusive_group(required=True)
    src.add_argument("--order", help='Comma-separated WP ids (or subjects with --by-subject)')
    src.add_argument("--order-file", help="Path to a file with one WP id per line")
    p.add_argument("--by-subject", action="store_true", help="Interpret --order values as subject names")
    p.add_argument("--dry-run", action="store_true", help="Print the plan without applying any PATCH")
    args = p.parse_args()

    if args.order:
        ordered_ids = _parse_order(args.order, args.by_subject, args.project)
    else:
        ordered_ids = _read_order_file(args.order_file)

    result = resequence(args.project, ordered_ids, dry_run=args.dry_run)

    _render_before_after(result["before"], result["after"], result["actions"])

    if result["errors"]:
        print()
        print(f"✗ {len(result['errors'])} error(s) during PATCH:")
        for e in result["errors"]:
            print(f"  wp #{e['wp_id']}: status={e['status']} body={e['body']}")
        sys.exit(1)

    if args.dry_run:
        print()
        print("(dry-run — no PATCHes sent)")
    elif result["changed"]:
        print()
        print(f"✓ Resequenced {len(ordered_ids)} User Stories in project {args.project}.")
    else:
        print()
        print(f"✓ Project {args.project} already in the requested order — no changes.")


if __name__ == "__main__":
    main()
