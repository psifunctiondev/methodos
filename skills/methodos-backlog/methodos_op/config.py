"""Config loader for methodos-backlog.

Reads `~/.openclaw/workspace/methodos/methodos-projects.json` at module
import and exposes its fields as module-level constants. If the config
file is missing, import fails fast with a clear error — that's a
deployment error, surface early.

Field IDs:
- managed_by_field_id, managed_by_option_id: existing Phase-1/Phase-2
  project-level tag for fleet membership
- methodos_sequence_field_id: integer field on User Story WPs for
  priority rank within a project (id 4)
- discord_thread_id_field_id: string field on Projects, opt-in, holds
  the Discord thread id that "owns" the project (id 5)
- methodos_epic_number_field_id: integer field on Epic WP type, set
  once by numbering.py to compose display_id (id 6)
- methodos_story_number_field_id: integer field on User Story WP
  type, set once by numbering.py to compose display_id (id 7)
"""
from __future__ import annotations

import json
import os
import sys
from pathlib import Path

CONFIG_FILE = Path(os.path.expanduser("~")) / ".openclaw" / "workspace" / "methodos" / "methodos-projects.json"

OP_URL = os.environ.get(
    "OPENPROJECT_URL",
    "https://openproject.mquinnmoorecloud.sytes.net:5443",
)

if not CONFIG_FILE.exists():
    sys.exit(f"methodos-projects.json not found: {CONFIG_FILE}")

_CONFIG = json.loads(CONFIG_FILE.read_text())


def _require(name: str):
    if name not in _CONFIG:
        sys.exit(f"methodos-projects.json missing required key: {name!r}")
    return _CONFIG[name]


MANAGED_BY_FIELD_ID = _require("managed_by_field_id")
MANAGED_BY_OPTION_ID = _require("managed_by_option_id")
METHODOS_SEQUENCE_FIELD_ID = _require("methodos_sequence_field_id")
DISCORD_THREAD_ID_FIELD_ID = _require("discord_thread_id_field_id")
METHODOS_EPIC_NUMBER_FIELD_ID = _require("methodos_epic_number_field_id")
METHODOS_STORY_NUMBER_FIELD_ID = _require("methodos_story_number_field_id")

DEFAULT_SORT = _CONFIG.get(
    "default_sort",
    [["priority", "desc"], ["dueDate", "asc"], ["id", "asc"]],
)


def load_config() -> dict:
    """Re-export the loaded config dict (for callers that need all keys,
    e.g. notes field, or to introspect at runtime)."""
    return dict(_CONFIG)
