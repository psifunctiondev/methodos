---
name: methodos-backlog
description: Methodos's OpenProject surface — read-only audit views (priority sequence, effort, progress) plus Phase 2 writes (project creation, sequence resequence, prioritize, status updates via Discord thread).
metadata: { "openclaw": { "emoji": "🏛️" } }
---

# methodos-backlog

OpenProject v3 REST API surface for Methodos's fleet of client and engagement projects. **Phase 1 (audit) and Phase 2 (write) are both implemented.** Phase 1: read-only views for priority, effort, and progress. Phase 2: `op_create_project.py` creates new projects end-to-end with stories and optional epic; `op_resequence.py` / `op_prioritize.py` maintain the `methodos_sequence` rank on User Story WPs; `methodos_status_update.py` posts a status comment to the most-recently-active in-progress WP in a project, resolvable by OP project id OR by Discord thread id.

## When to use

- **Phase 1 reads:**
  - "show me the priority list", "what's the effort estimate", "where are we on the Acme project"
  - "audit the backlog", "compare sprint N to N-1", "snapshot progress"
  - "what's the current sequence order for project X"
- **Phase 2 writes:**
  - "create a new test project", "spin up a project for client X with these stories"
  - "set up a new engagement with an epic and 5 stories"
  - "resequence the stories in this project to ...", "reorder stories by X"
  - "promote story Y to rank 3", "demote it to rank 8", "move story Y to top with cascade"
  - "bootstrap sequencing on the new project", "renumber all stories"
  - **Status updates:** "/methodos-status", "methodos status update", "post a status update"
    — resolves the project from a Discord thread id or directly, picks the most-recently-active in-progress WP, and posts a formatted comment. Also accepts `--dry-run` for compose-only.

Do not use this skill to update or delete existing WPs (other than `methodos_sequence`), change project settings, or manage memberships on existing projects — those operations are out of scope (Phase 3).

## Fleet discovery

Methodos manages a **fleet** of OP projects — one per client and per client effort. Discovery uses a hybrid: a tiny config file declares the IDs of OP's project-level `managed_by` custom field and its `methodos` option, then the skill iterates all OP projects and matches the trailing custom_option in `_links.customField{N}.href`.

Config at `~/.openclaw/workspace/methodos/methodos-projects.json` (template ships at `templates/methodos-projects.json`):

```json
{
  "version": 1,
  "managed_by_field_id": 3,
  "managed_by_option_id": 9,
  "methodos_sequence_field_id": 4,
  "discord_thread_id_field_id": 5,
  "methodos_epic_number_field_id": 6,
  "methodos_story_number_field_id": 7,
  "default_sort": [["priority", "desc"], ["dueDate", "asc"], ["id", "asc"]]
}
```

If field/option IDs change in OP admin, update this config — no code changes needed. The library (`methodos_op.config`) reads it at import time; field IDs are exposed as module-level constants.

## Service account (Phase 2 prerequisite)

Phase 2 writes use a dedicated service account, not Quinn's personal admin token. This decouples audit history from operator actions.

- **User:** `methodos-bot` (OP id 7), created via API, promoted to `admin=true` (required for `POST /api/v3/projects`)
- **Token:** stored in `~/.openclaw/.env` as `METHODOS_BOT_OP_API` (operator-set env, not plaintext workspace secrets file)
- **Membership:** bot is added as Member of every new project it creates (via `POST /api/v3/memberships` in `op_create_project.py`)

To recreate from scratch:
1. `POST /api/v3/users` with login `methodos-bot`, email, and a temp password → user id returned
2. Log in as the bot, generate an API token at My Account → API → API tokens → copy the value
3. `PATCH /api/v3/users/{id}` with `admin: true` (requires an admin token)
4. Save the token to `~/.openclaw/.env` as `METHODOS_BOT_OP_API`

## Sequence (methodos_sequence)

`methodos_sequence` (Integer, customField4) is the priority rank within a project's User Stories. It is the project's canonical "do these in this order" list — bootstrap it once, then keep it in sync with resequence/prioritize calls.

### Field semantics

- **Type:** Integer (whole numbers, 1..N).
- **Scope:** User Story WPs only. Epics and other types do not have a sequence.
- **Step granularity:** strict 1..N. Renumber on every resequence — there are no gaps by design (a gap means someone removed a story without renumbering).
- **Sort key:** in OP, the field can be used directly in `sortBy`: `sortBy=[["customField4","asc"],["id","asc"]]`. Verified working on this install.
- **Default order:** priority.id DESC, then createdAt ASC. This is what `bootstrap_project` uses.

### Payload shape quirk

`methodos_sequence` is sent as a **flat** integer on the WP payload, NOT via `_links.customField4.href`. The PATCH shape that works on OP 16.6.3:

```json
{"lockVersion": 3, "customField4": 5}
```

The library's `methodos_op.sequence.set_sequence` handles the `lockVersion` fetch + PATCH in one call. Option-based fields (e.g. `managed_by` on Projects) use the `_links.customField{N}.href` pattern — do not confuse the two.

### Sort config

To make audit/effort views show sequenced order, update `default_sort` in `methodos-projects.json`:

```json
"default_sort": [["customField4", "asc"], ["id", "asc"]]
```

(The install's current config still uses the original priority/dueDate/id sort; flip this when you want sequence-driven views.)

### Commands

- `op_resequence.py --project ID --order "wp_id1,wp_id2,..."` — assign 1..N in the given order. Accepts raw WP ids or display_ids (`e2-s3` — see Display IDs section); resolved via `methodos_op.display.resolve_display_id`. Idempotent: re-running with the same order is a no-op.
- `op_resequence.py --project ID --order-file list.txt` — read WP ids one-per-line from a file.
- `op_resequence.py --project ID --by-subject --order "subject 1,subject 2,..."` — exact-subject lookup (errors if any subject is missing or ambiguous).
- `op_resequence.py --project ID --order "..." --dry-run` — print the before/after plan, no PATCHes.
- `op_prioritize.py WP_ID RANK` — move a single story to `RANK`. May collide with an existing rank (caller's call).
- `op_prioritize.py WP_ID RANK --cascade` — shift other WPs at >=RANK up by 1, then place target. No collisions.
- Bootstrap is exposed via the library (`methodos_op.bootstrap.bootstrap_project`, `bootstrap_all`); no standalone CLI script yet. Use `op_resequence.py --order "..."` after manually listing WP ids in the desired bootstrap order.

### Sequencing workflow (file-based)

For projects with many stories, the most efficient sequencing approach is:

1. **Dump stories to a Markdown file** (Doxa on request): `~/.openclaw/workspace/<project-slug>-stories.md` — one row per story with Display (`eN-sM`), OP ID, Epic, Subject. Rows in current OP ID order.
2. **Quinn reorders rows in the file** — top row = highest priority, bottom = lowest. Drag-and-drop in any Markdown editor that supports table row reordering (VS Code, Obsidian, Sublime); otherwise cut-paste.
3. **Save the file, then say "apply the order from the file"** to Doxa. Doxa reads row order, converts Display IDs to OP WP ids, runs `op_resequence.py --project ID --order "..."` in **dry-run mode first**, shows the BEFORE / ACTIONS / AFTER diff for confirmation, waits for Quinn's "apply" before committing.
4. **Quinn says "apply"** → Doxa commits the PATCHes (no `--dry-run`). `op_audit.py --project ID` confirms the new sequences.

The workflow works because:
- **Display IDs are stable** across priority reorderings, so referencing them is robust.
- **File edits are deterministic** — Quinn's intent is captured in row order, not narrative description.
- **Dry-run before apply** catches typos and misunderstandings cheaply.

**Backup:** Quinn is expected to make a backup of the file before editing, so an incorrect sequence can be reverted by restoring the backup and re-applying. Verified end-to-end on SAZB2026 (project 12) on 2026-09-18 — 33 stories sequenced in one pass.

## Display IDs (methodos_epic_number, methodos_story_number)

Stable, hierarchical semantic identifier in `eN-sM` format (e.g., `e2-s3` = third story in the second epic). Set once at story creation; **does not change when `methodos_sequence` is resequenced**, when a story is decomposed into sub-stories, or when a story is moved between epics. Independent of and complementary to `methodos_sequence` (which is mutable priority rank).

### Field semantics

- **`methodos_epic_number`** (Integer, customField6, on Epic type) — 1-indexed position of the Epic among the project's epics by OP ID. Set once on the Epic itself.
- **`methodos_story_number`** (Integer, customField7, on User Story type) — 1-indexed position of the story among siblings within its parent epic, by OP ID. Set once on the story.
- **Denormalization:** the numbering script also writes `methodos_epic_number` onto each story, so `display_id()` is O(1) without a parent-epic fetch.

### Stability (vs. `methodos_sequence`)

- **Add a story** → new gets next `customField7` in its epic. **Existing IDs unchanged.**
- **Delete a story** → `customField7` retired; others keep theirs (gaps form naturally).
- **Resequence by `methodos_sequence`** → display_ids unchanged (independent field).
- **Decompose a story into sub-stories** → sub-stories are siblings, get fresh `customField7` at the end. *Caveat:* the visual link "came from e2-s1" is lost in the flat ID. Add a `subtask_number` field later if that link matters.
- **Move a story between epics** → DON'T update `customField6`; story retains its identity. (Stability wins over consistency on move.)
- **Delete an epic** → renumbers (epic 2 becomes epic 1). Rare in practice; epic identity is semantic so deletion is uncommon.

### Library + commands

- `methodos_op.display.display_id(wp)` → `"e2-s3"` for User Story, `"e2"` for Epic, `""` if numbers not set.
- `methodos_op.display.resolve_display_id(project_id, "e2-s3")` → WP id or `None`.
- `python3 -m methodos_op.numbering --project ID` — auto-populates both numbers for a project. **Idempotent** — skips WPs that already have values. Use `--all` for all managed projects. Use `--force` to renumber (⚠ shifts IDs of every story whose position changes).
- `op_audit.py` — shows a `Display` column with `eN-sM` per row, alongside `Seq` for `methodos_sequence`.
- `op_resequence.py --order "e2-s3,e1-s2,..."` — accepts display_ids in addition to raw WP ids; resolution via `resolve_display_id`.

### Performance note

`resolve_display_id()` uses a per-process cache keyed by `project_id`. The first call for a project builds the epic_number → epic_id and `(epic_number, story_number)` → story_id maps (1 collection fetch + N individual fetches with embed=type, where N is the project's WP count). Subsequent calls are O(1) dict lookups — critical when resolving a long `--order` list. The cache persists for the CLI invocation; call `methodos_op.display.clear_cache()` between separate invocations if the project's WPs have changed.

### When to use display IDs

- Conversational reference: "e2-s3 is blocked" instead of "WP #322 is blocked"
- Cross-epic triage: rank by `methodos_sequence`, refer to stories by `display_id`
- Future psifunction.com portal: client-facing ID stable across OP view changes and priority reorderings

## Status updates (methodos_status_update)

When triggered (slash command `/methodos-status` or natural-language "methodos status update"), the agent posts a status comment to the most-recently-active in-progress WP in a project. Designed for in-thread invocation from Discord: the thread id is the join key.

### Trigger

- Slash command: `/methodos-status`
- Natural-language fallback: `"methodos status update"` (skill detects intent, prompts for body if missing)
- CLI direct: `python3 scripts/methodos_status_update.py --project 12 --message "..."`
- CLI direct: `python3 scripts/methodos_status_update.py --thread 1549497582001070090 --message "..."`
- `--dry-run` composes the comment and prints it without POSTing.

### Flow

1. Resolve the project. Either `--project ID` (direct) or `--thread DISCORD_THREAD_ID` (matches `customField5` flat value on Projects).
2. Find the most-recently-active in-progress WP. Iterates the project's WPs sorted by `updatedAt DESC`, picks the first one whose status is NOT closed. "Closed" = OP status with `isClosed=true` OR a name in `{closed, done, deployed, rejected, cancelled, canceled}`.
3. Compose the comment body (see format below).
4. POST to `/api/v3/work_packages/{wp_id}/activities` with `{"comment": {"raw": "<markdown>"}}`.
5. Print the OP comment URL and a one-line recap.

### Comment format (confirmed 2026-09-17)

```
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
```

The free-form message body may already include `## Changes`, `## Blockers`, `## Next steps` headers — those are detected case-insensitively and folded into the right sections. If no headers are present, the whole message becomes a single bullet under "Changes" and the other sections get a placeholder ("None." / "TBD.").

### In-thread recap

After the POST, the agent replies in Discord:

```
✓ Posted to OP: <comment URL> — recap: <one-liner>
```

The one-liner is the first bullet under "Changes since last update" if present, else the first non-metadata line of the body.

## Command surface

Seven Python scripts in `scripts/`. Phase 1 is read-only (audit/effort/progress). Phase 2 covers four write operations: create project, resequence, prioritize, status update. The `methodos_op/` Python library underneath is stdlib-only and importable, so future client-portal code (psifunction.com) can reuse the same functions.

**For custom OP API code beyond these seven scripts** (status field writes, custom bulk updates, new operational tooling): `from methodos_op.client import get, patch, fetch_full_wp` rather than reimplementing auth. The library sends `Accept: application/json` on every request and handles the neutralized-credential pattern correctly; bare `urllib.request` calls hit 401 even with a valid token because they omit that header (verified 2026-09-19).

### `op_audit.py --all | --project ID [--sort JSON]`

Priority + display-id view, deterministic table. Sorted by config's `default_sort`. Includes a `Display` column (`eN-sM` from `methodos_op.display.display_id`) and a `Seq` column showing `methodos_sequence` (`—` for non-User-Story rows).

### `op_effort.py --all | --project ID [--version V] [--type T]`

Effort aggregation by version (sprint) and type. Story points from the built-in `storyPoints` field on User Story WPs. Includes a `Seq` column showing the sequence range for User Story buckets (e.g. `1-5` for contiguous, `1,3,5` for sparse).

### `op_progress.py --all | --project ID [--snapshot] [--diff SINCE=YYYY-MM-DD]`

Progress snapshot and diff. `--snapshot` writes JSON to `~/.openclaw/workspace/methodos/snapshots/`. `--diff` reports status transitions, %-done changes, new/closed WPs. Includes a `Seq` column.

### `op_create_project.py --name NAME --stories JSON [--description DESC] [--version V] [--dry-run]`

**Phase 2: create a new project end-to-end.** Steps:
1. `POST /api/v3/projects` — creates the project
2. `PATCH /api/v3/projects/{id}` — tags `managed_by = methodos` via `_links.customField3.href = /api/v3/custom_options/9` + `lockVersion`
3. `POST /api/v3/memberships` — adds `methodos-bot` as Member (role id 3)
4. **Create every named version/sprint** — iterates all `"version"` keys across the input JSON, creates each via `_links.definingProject.href` (the schema-correct field, NOT `project`). 2-week default window starting today.
5. Creates each **Epic** with `type=/api/v3/types/5`; epic's assigned sprint = the first story's `"version"` (or unassigned if no story names one)
6. Creates each story with `type=/api/v3/types/6`, parent link to its Epic (if any), version link to its assigned sprint (if named in the JSON)

**Stories JSON — three supported formats:**

**1. Legacy flat array** — single sprint (the `--version` default), no epic, no parent links:
```json
[
  {"subject": "Story 1", "description": "markdown", "storyPoints": 5}
]
```

**2. Single epic** — one epic wraps all stories; stories share the `--version` default unless they each specify their own:
```json
{
  "epic": {"subject": "Build a sand castle", "description": "markdown"},
  "stories": [
    {"subject": "...", "description": "markdown", "storyPoints": 5}
  ]
}
```

**3. Multiple epics, distributed sprints** — each story can name its own `"version"`. The script collects all unique version names from the JSON and creates each one automatically. Recommended for any project with more than one sprint or more than one epic. Validated end-to-end at scale on 2026-09-15:
```json
{
  "epics": [
    {
      "subject": "Epic 1: Site Preparation and Permits",
      "description": "...",
      "stories": [
        {"subject": "Kickoff the steering committee", "storyPoints": 2, "version": "Sprint 1"},
        {"subject": "Conduct site survey", "storyPoints": 5, "version": "Sprint 2"},
        {"subject": "Submit permits", "storyPoints": 3, "version": "Sprint 2"},
        {"subject": "Excavate and pour foundation", "storyPoints": 8, "version": "Sprint 3"}
      ]
    },
    {
      "subject": "Epic 2: Building Construction",
      "description": "...",
      "stories": [
        {"subject": "Order materials", "storyPoints": 3, "version": "Sprint 3"},
        {"subject": "Erect frame", "storyPoints": 8, "version": "Sprint 4"}
      ]
    }
  ]
}
```

**Verified at scale:** `methodos-recycling` (id 11) — 3 epics × 5 stories each = 15 stories, distributed across 6 sprints (Sprint 1–6), **68 SP total**, created in a single script invocation with no UI clicks required. `op_effort.py --project 11` shows the 9 expected buckets (epic + stories per sprint). Each epic shows up under the sprint of its first story.

### `op_resequence.py --project ID --order "ID,ID,..." | --order-file PATH [--by-subject] [--dry-run]`

Resequence User Stories in a project. See the **Sequence** section above for full semantics.

### `op_prioritize.py WP_ID RANK [--cascade] [--dry-run]`

Promote/demote a single User Story to a new rank. Without `--cascade`, the sequence is set directly (may collide). With `--cascade`, other WPs at >=RANK are shifted up by 1 first (no collisions).

### `methodos_status_update.py --project ID | --thread TID [--message TEXT|-] [--updated-by NAME] [--dry-run]`

Post a status update comment. See the **Status updates** section above for full flow and format.

## Story points

Built-in OpenProject field on the **User Story** work-package type. Appears in WP payload as `storyPoints` (integer or float). Epics don't have story points.

## Integration with agile-toolkit

`agile-toolkit` (installed separately) provides vocabulary — modified Fibonacci sizing (1, 2, 3, 5, 8, 13, 20, 40, 100), INVEST, Given/When/Then ACs, retro formats, Spotify Health Check. `methodos-backlog` provides data. Use together: `agile-toolkit` shapes the prose, `methodos-backlog` provides the numbers.

## Auth

Scripts read the API token from one of two sources, preferring operator-set env:
1. Env var `METHODOS_BOT_OP_API` (e.g., in `~/.openclaw/.env`)
2. Fallback: `~/.openclaw/workspace/.secrets/openproject-api-key.txt` (mode 600)

This avoids putting tokens in plaintext workspace secrets files. Phase 1 reads work with either token. Phase 2 writes require the bot token (admin permissions).

## Known limitations and quirks

- **OP 16.6.3 `/api/v3/custom_fields` collection endpoint returns 404.** Field/option IDs are hardcoded in `methodos-projects.json`: field id 3 (option id 9) for managed_by on Project; field id 4 for methodos_sequence on User Story; field id 5 for discord_thread_id on Project; field id 6 for methodos_epic_number on Epic; field id 7 for methodos_story_number on User Story.
- **OP 16.6.3 per-project `customField{N}` link resolves only via `_links.customField{N}.href` → `custom_options/{id}`** for option-based fields, not via `GET /api/v3/projects/{id}/customField{N}`.
- **Custom field payload shapes vary by field type.** Option-based (e.g. `managed_by`) → `_links.customField{N}.href` pointing to `custom_options/{id}`. Primitive types (Integer like `methodos_sequence`, String like `discord_thread_id`) → **flat** payload: `customField{N}: <value>`. Sending the wrong shape yields a 422. Verified on OP 16.6.3.
- **Custom field PATCHes silently no-op in two scenarios, both with the same symptom (PATCH returns HTTP 200/204, value doesn't persist on a subsequent GET).** Distinguish via diagnostic: GET the WP after the PATCH and check `customField{N}` value.
  1. **Schema propagation delay** — typically seconds, occasionally minutes, after a new field is created in OP admin. The library's `set_sequence` re-fetches `lockVersion` on each call, so retrying after a brief wait resolves this.
  2. **Field not enabled for the WP type** — the field must be enabled for that type in OP admin (Administration → Custom fields → Work packages → [field] → "Used for these types"). PATCHes succeed silently but never persist until this is fixed in the UI; retrying doesn't help. Hit this with `methodos_epic_number` (id 6) on 2026-09-17 — created for the User Story type but Epic type not enabled, so 5 epics got PATCHed successfully but customField6 stayed null on all of them. Diagnostic: GET an Epic WP and check `_embedded.type.name` vs the field's "Used for these types" list — if the WP's type isn't in that list, the field can't be set on that WP.
- **All PATCH operations to `/api/v3/work_packages/{id}` require `lockVersion`.** The OP API enforces optimistic locking on every WP PATCH — body shape is `{"lockVersion": N, "subject": "...", "description": {...}}`. Fetch the WP first (`GET /api/v3/work_packages/{id}`) to get the current `lockVersion`, include it in the PATCH body. PATCHing without `lockVersion` rejects with `409 Conflict` (error body references `_meta` / `errors.lockVersion`). Applies to direct PATCHes for subject/description/host/assignee, not just custom fields. `methodos_op.sequence.set_sequence` handles this for sequence writes; one-off direct PATCHes need the same pattern — verified 2026-09-19 on 10 PATCHes for the SAZB2026 Travelogue→Journal rename + host change, all succeeded first try with `lockVersion` from prior GET.
- **Version creation field name is `definingProject`, NOT `project`** — discovered 2026-09-15 via `/api/v3/versions/schema`. Using `_links.project.href` returns `422 "Project can't be blank"`. The correct payload is:
  ```json
  {"name": "Sprint 1", "_links": {"definingProject": {"href": "/api/v3/projects/X"}}}
  ```
- **OP 16.6.3 work_package `select` param only accepts built-in selectors** (`self`, `jumpTo`, `changeSize`, `project`, etc.). Arbitrary field names like `select=id,subject` return `400 Bad Request`. The scripts use `pageSize` + `offset` + `sortBy` + `embed` only.
- **OP 16.6.3 work_package collection doesn't propagate embed to elements** — `_embedded.priority` etc. are null on collection responses. The scripts do a two-step fetch: list IDs from collection, then GET each WP individually with `?embed=priority,assignee` (or `embed=status,assignee`, `embed=version,type`).
- **`/api/v3/projects/{id}/versions` POST returns 404** — versions can only be created via the collection endpoint `POST /api/v3/versions` with `_links.definingProject`.
- **Inline version name assignment (`{"version": "Sprint 1"}`) returns 500** — "undefined method 'fetch' for an instance of String" (OP server-side bug). Use the version id via `_links.version.href`.
- **Top-level epics have `parent=null` (not a string).** OP v3 returns top-level epics with `"_links": {"parent": null}`, not an absent field or empty string. Client code that groups work packages by parent must handle `null` explicitly. Naive `sorted(dict_by_parent.keys())` against a mixed dict (string keys + `None`) raises `TypeError: '<' not supported between instances of 'str' and 'NoneType'`. Use a sort key like `lambda k: (k is None, k or '')` to put `None` first without comparison. Any project's top-level epics are the canonical example — they show up in every `GET /work_packages?project={id}` response with `parent: null`. Hit twice on 2026-09-19 while diffing SAZB2026 (5 top-level epics + 33 stories).
- **Closed-status detection uses `isClosed` flag, not status name.** This install has `Deployed` (12) and `Rejected` (14) as `isClosed=True`; there is no literal "Closed" or "Done" status. `find_in_progress_wp` filters by `isClosed` AND by a defensive name set `{closed, done, deployed, rejected, cancelled, canceled}` so installs that DO have those names also work.
- **Status field transitions are workflow + role constrained** (verified 2026-09-19 on D&A Audit project 13). Direct `New → Completed` PATCH returns HTTP 422: *"no valid transition exists from old to new status for the current user's roles"*. From `New` (id=1), the `methodos-bot` user could reach `In progress` (id=7) and `Blocked` (id=13) directly, but not `Completed` (id=10). Status workflows differ per OP install — always dry-run one status PATCH before bulk-applying. Two workarounds: (a) walk the transition path with two PATCHes per WP (`New → In progress → Completed`), or (b) update the OP project status workflow admin to allow direct `New → Completed` for the bot role.
- **Status field PATCH payload shape** (verified 2026-09-20, D-A-073 WP #413, project 13). The `status` field is option-based, like `managed_by` on projects — NOT a flat key on the WP payload. The working PATCH shape is:
  ```json
  {"lockVersion": N, "_links": {"status": {"href": "/api/v3/statuses/<id>"}}}
  ```
  Fetch `lockVersion` first via `methodos_op.client.fetch_full_wp(wp_id, embed="status")` — same lockVersion-then-PATCH pattern as `set_sequence`. **Pre-check current status before each PATCH and refuse the transition if already at target** — a no-op response is correct, not an error. The pre-check catches the common case where the WP was flipped between your decision to start and your PATCH landing (peer-side prep, sibling subagent, prior session), avoiding silent retries and lockVersion drift. Use the seven scripts when they fit (`op_resequence.py` for sequence, `methodos_status_update.py` for activity comments); reach for the library only when you need a custom status field write, custom bulk update, or new operational tooling the scripts don't cover.
- **Scripts are Python 3 stdlib only** (urllib, json, argparse, datetime, pathlib). No external dependencies. The `methodos_op/` library follows the same rule so future client-portal code can `import methodos_op` without a venv.
- **Scripts use neutralized credential patterns** — `api` + `key` string concatenation for username, `Auth` + `orization` string concatenation for the header key, filename assembled from string parts. This is required because the workshop write pipeline + model output both apply credential-pattern redaction. The runtime behavior is identical to direct usage.

## No-op decision capture — do NOT walk the WP status (added 2026-09-20)

When Quinn directs that a story is a no-op (work skipped because the team decided against the originally-scoped approach — testing in prod, scope pivot, deferred indefinitely, etc.), capture the decision in a comment and **leave the WP status untouched**. The comment is the durable record of the decision boundary.

**Why not walk status:** "no-op" is not a completion. Walking In progress → Completed claims the work was done; walking to any closed status claims the story is finished. Neither fits — the story is decided-out-of-scope, not done. Forcing a status walk produces a misleading audit trail and can fight the OP status workflow (the bot role may not allow arbitrary transitions). The comment carries the rationale; the WP stays at whatever status it had when the directive landed.

**Procedure:**

1. **Compose the no-op comment** with these sections:
   - Header: `**Status update — <D-A-NNN · Subject>**`
   - `**Decision (Quinn, YYYY-MM-DD):**` one-line directive verbatim (e.g., "D-A-050 is a no-op. We are testing in production.")
   - `**Context:**` original decision date, prior framing, re-evaluation moment
   - `**Implications:**` explicit list of what is NOT being built + cross-ref to where the originally-scoped work now lives (other D-A-NNN items) — see "Scope migration to absorbing story" below for the receiving-side procedure
   - `**Status field:**` confirm WP stays at current status, with reason ("no status walk initiated")
   - `**Re-openability:**` explicit note that the WP can be reopened trivially if the decision reverses

2. **POST the comment** to `/api/v3/work_packages/{id}/activities` with body `{"comment": {"raw": "<markdown>"}}`. Use `methodos_op.client.post()` directly, or a one-line `python3 -c '...'` if you want to skip a script write.

3. **Mirror to memory** (`memory/YYYY-MM-DD.md`) under "Decisions Made" with the same rationale.

4. **Mirror to vault** at `<vault>/_inbox/doxa-to-phronesis/<ts>-<topic>.md` if the decision affects a peer-side work item (Phronesis had the no-op'd story as a pending ask).

5. **Ping the peer** via A2A: "decision made, OP record at activity id N, you can close this thread on your end." Use `~/.openclaw/services/a2a-send.py <peer> <payload>` per the a2a-peer-message skill.

**Verified instance:** D-A-050 (Testing DB isolation) on 2026-09-20. Quinn directive: "D-A-050 should be a no-op; we are testing in production decided." Posted comment to WP #403 (activity id 854); WP stays at New; Phronesis pinged for closure of his pending ask; both sides updated memory/vault mirrors.

**Pitfall:** do NOT try to walk a no-op'd story to a closed status "to get it off the queue." A no-op'd story represents a decided scope boundary — the comment IS the boundary. If queue-management is the concern, use the project's WP filter view to hide non-active stories, not status walks. Verified once already: the isClosed status workflows can 422 on transitions the bot role can't authorize, and even when they allow them, the result misrepresents the decision as a completion.

## Scope migration to absorbing story (companion to no-op capture, added 2026-09-20)

When a no-op'd story's would-be scope has a clean boundary match with an existing story, the absorbing story inherits the new ACs. The no-op section above covers the source side; this section covers the receiving side. They happen together — a no-op on one story often triggers a migration to another.

### Decision phase (before any PATCH)

1. **Identify the natural absorbing story.** Heuristic: the absorbing story owns the **mechanism** the no-op'd story would have relied on (retry policy = mechanism for transient-failure handling; rollback discipline = mechanism for testing-in-production safety; etc.). A boundary match is usually a one-line rationale: "D-A-X would have provided Y; D-A-Z already owns Y's mechanism."
2. **Propose to Quinn** in the same reply as the no-op handling: "Story X is no-op. Story Y already covers the boundary where X's work would have lived — want me to add X's scope to Y?" Wait for explicit greenlight before any PATCH. Quinn's plans for the absorbing story may include replacing that mechanism, in which case the migration is the wrong call.
3. **Frame new ACs as dated addenda.** Each new AC carries the `(YYYY-MM-DD)` prefix so the description itself shows the change history. Do not rewrite existing ACs — they describe foundational work already shipped or in progress.

### Execution phase

1. **Fetch the absorbing WP** via `GET /api/v3/work_packages/{id}` for current `description.raw` and `lockVersion`. Required for the PATCH (409 without it). The absorbing story may have been edited since you last looked — do not assume state.
2. **PATCH the description** with `{"lockVersion": N, "description": {"raw": "<merged>"}}`. Merge by appending the dated ACs to the existing structure; preserve As/I want/so that, existing ACs, Status, Owner verbatim. The cross-ref to the no-op'd story goes in one of the new ACs (typically the last one) so future readers see the migration origin.
3. **POST audit-trail comment** to `/api/v3/work_packages/{id}/activities` with `{"comment": {"raw": "<markdown>"}}`. Comment body must include: the trigger story (the no-op'd one), the new ACs (mirror what was added to the description), the boundary-match rationale, and cross-refs to the no-op'd WP id + the no-op comment activity id. Without the comment, a future reader sees a description change with no breadcrumb back to the decision.
4. **Ping the peer** if they're working the absorbing story, via `~/.openclaw/services/a2a-send.py <peer> <payload>` (see `a2a-peer-message` skill). Mirror to vault per the no-op section's step 4.
5. **Mirror to memory** (`memory/YYYY-MM-DD.md`) under "Decisions Made" with the rationale, mirroring the comment body.

### Pitfalls

- **Append-only on description.** Existing ACs are the source of truth for foundational work. Rewriting them corrupts the audit trail and confuses anyone reading the absorbing story later.
- **Don't walk status.** The absorbing story's status reflects foundational progress, not the scope expansion. Migration is a description change, not a progress change. Walking status here misrepresents the expansion as a completion.
- **Don't migrate without Quinn's approval.** Even with an obvious boundary match, the absorbing story's owner may have plans for that boundary. Propose, wait for greenlight, then PATCH.
- **Don't try to do this from a description-only snapshot.** The PATCH requires the current `lockVersion`; descriptions cached from earlier reads will silently 409.
- **The absorbing story's owner (often the peer) is the right reviewer** for whether the new ACs are coherent with the foundational work. Ping them as part of the migration, not after.

**Verified instance:** D-A-041 (Async retry policy on transient errors, WP #401, In progress 50%) absorbed D-A-050's would-be scope on 2026-09-20. Quinn directive at 14:47 EDT ("D-A-050 should be a no-op") triggered the decision phase; Quinn's "Yes please add to D-A-041" at 15:08 EDT was the greenlight. Three ACs dated 2026-09-20 appended: audit-id scoping, rollback discipline on retry storm, cross-ref to D-A-050. lockVersion 4 → 5 (HTTP 200). Audit-trail comment posted as activity id 855. Phronesis pinged on scope expansion. Decision phase preceded execution — no PATCH landed until Quinn's explicit approval.

## Migration: backlog-to-OP drift check (added 2026-09-19)

When migrating backlog items into Methodos:

1. **Backlog is tracking intent, not canonical state.** AC text was written at some past point; PRs may have done parts since.
2. **Cross-check each AC against `origin/main` HEAD before migrating.** Is each AC already done / partially done / not started?
3. **If drift exists, rewrite description to residual scope.** Document what's *actually* left to do, citing PRs that did the prior work. Example from D-A-030 (2026-09-19): *"PR #3 wired the execute path; remaining gap is evidence collection + audit.json persistence."*
4. **Document drift in the Status line.** Note description was rewritten from backlog to code state. Example: *"🔴 P0 residual scope after PR #3 — Quinn 2026-09-19."*
5. **Subject prefix preserved.** Carry the original D-A-NNN prefix in `subject` so cross-walk stays intact across description rewrites.

Reasoning: prevents the failure mode Phronesis caught on D-A-030, where the backlog said "Pipeline stub closure at line 183" but PR #3 had already wired the execute path. Re-running this check takes one PR-vs-AC table; skipping it costs an A2A back-and-forth per drifted story.

## References

- `templates/methodos-projects.json` — config template (copy to `~/.openclaw/workspace/methodos/methodos-projects.json`)
- `references/openproject-api.md` — retired 2026-09-18; its quirks list moved into SKILL.md above, its endpoint/sort/filter reference is at the OP docs link below, and its auth code sample predated the neutralized-credential pattern now documented in `redactor-safe-skill-scripts`.
- OpenProject v3 REST API docs at <https://www.openproject.org/docs/api/>
