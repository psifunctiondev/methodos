# methodos-backlog

This is the OpenProject integration skill for the Methodos framework.

## Lifecycle

The skill's **canonical working copy is this directory** (inside the methodos repo). The workshop-installed copy at `~/.openclaw/agents/main/agent/workshop-skills/methodos-backlog/` is a working mirror that Doxa uses for day-to-day edits — it's periodically synced with this repo via commit + push.

### When Doxa improves the skill:
1. Edit in the workshop mirror (`~/.openclaw/agents/main/agent/workshop-skills/methodos-backlog/`) for day-to-day workflow.
2. Doxa mirrors the changes into this repo (`skills/methodos-backlog/`) and commits + pushes.
3. Phronesis (or any other agent with repo access) can pull to see the improvements.

### When this repo changes (Phronesis or another contributor):
1. Doxa pulls the changes.
2. Doxa mirrors them into the workshop skill directory.
3. Doxa continues using the workshop mirror as the active working copy.

### Why this structure?
- Workshop pipeline still works (skill lives at the expected path).
- Methodos framework content (METHODOS.md, schemas/, specification/, etc.) is referenceable from the skill's directory.
- Phronesis can audit skill improvements via git log.
- Methodos repo is the single source of truth for both framework and tooling.

## What's in here

- `methodos_op/` — Python library for the OP v3 REST API surface
- `scripts/` — CLI wrappers (op_audit, op_resequence, op_prioritize, etc.)
- `SKILL.md` — skill documentation
- `templates/methodos-projects.json` — config template (copy to `~/.openclaw/workspace/methodos/methodos-projects.json`)
- `references/` — additional reference docs (some retired)

## See also

- `../../METHODOS.md` — framework overview
- `../../specification/` — Methodos specifications
- `../../schemas/` — Methodos schemas
- `../../reference/RI-001-OpenClaw.md` — OpenClaw runtime reference
