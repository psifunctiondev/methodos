#!/usr/bin/env python3
"""methodos-backlog: promote/demote a single User Story to a new rank.

Usage:
    op_prioritize.py WP_ID RANK [--cascade] [--dry-run]

With `--cascade`, every OTHER WP at rank >= RANK is shifted up by one
(highest-first to avoid collisions) before the target is set. Without
it, the WP's sequence is set to RANK directly — may collide with an
existing rank; caller accepts that risk.

Output: the resulting action list + the new lockVersion for the target.
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from methodos_op import prioritize, fetch_full_wp


def main() -> None:
    p = argparse.ArgumentParser(description="Promote/demote a User Story to a new sequence rank (methodos-backlog)")
    p.add_argument("wp_id", type=int, help="Target WP id")
    p.add_argument("rank", type=int, help="Desired new sequence position (1-indexed)")
    p.add_argument("--cascade", action="store_true", help="Shift other WPs at >=rank up by 1 first")
    p.add_argument("--dry-run", action="store_true", help="Print the plan without applying any PATCH")
    args = p.parse_args()

    result = prioritize(args.wp_id, args.rank, cascade=args.cascade, dry_run=args.dry_run)

    if result["errors"]:
        print(f"✗ {len(result['errors'])} error(s):")
        for e in result["errors"]:
            print(f"  wp #{e['wp_id']}: status={e['status']} body={e['body']}")
        sys.exit(1)

    print(f"=== Plan for WP #{args.wp_id} → rank {args.rank} ({'with cascade' if args.cascade else 'no cascade'}) ===")
    if not result["actions"]:
        print("  (no changes — target already at this rank)")
    for a in result["actions"]:
        print(f"  #{a['wp_id']:>5}: {a['from']} -> {a['to']}")

    if args.dry_run:
        print()
        print("(dry-run — no PATCHes sent)")
        return

    if not result["changed"]:
        print()
        print("(no changes applied)")
        return

    # Re-fetch target's lockVersion for confirmation.
    wp = fetch_full_wp(args.wp_id)
    if wp:
        print()
        print(f"✓ Applied. Target WP #{args.wp_id} is now at sequence {args.rank} (lockVersion={wp.get('lockVersion')}).")


if __name__ == "__main__":
    main()
