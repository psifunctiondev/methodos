# Phronesis Review — Methodos Round 3 (post-Doxa feedback 3.1–3.3)

**Reviewed:** 3de5712 ("Updates from Doxa feedback 3.2-3") and 02a38c6 ("Updates from Doxa feedback 3.1") on top of the v1.0.1 / round-2 baseline.
**Reviewer:** Phronesis
**Review policy:** Round-2 reset was a full restructure, so this review treats round-3 diffs as the primary focus and only flags higher-level cross-doc issues that surfaced during cross-checking.

---

## TL;DR

Round 3 was small, surgical, and tight. It addressed real ambiguity (a Goal `Waiting` state that conflicted with `Blocked`, two kernel terms that lived outside the Terminology doc) and the Coordination Fabric lease semantics. **Almost all of it lands cleanly.**

There are **3 things worth addressing in this round**, **4 advisories** (not blocking), and **3 lingering cross-doc issues from round 2** that this round surfaced but did not cause. Net: ship after the round-3 fixes below.

---

## What Round 3 Changed (delta only)

| Commit | File | Change |
|---|---|---|
| 02a38c6 | `MTH-010-Goal.md` | Removed the `Waiting` Goal state. |
| 3de5712 | `MTH-001-Terminology.md` | Added `Intent Envelope` and `Decision` definitions. Removed `Decision` from Future Directions. |
| 3de5712 | `MTH-024-Coordination-Fabric.md` | Added `# Lease Semantics` section + `MTH-024-REQ-004`. |

---

## ✅ What Round 3 got right

1. **Removed `Waiting` Goal state.** This was the cleanest fix. `Waiting` and `Blocked` were de facto synonyms for Goal; only Task semantics benefits from a `Waiting`/`Blocked` distinction (a Task Waiting on a dependency, vs a Task Blocked by an intervention). Goal `Blocked` is sufficient. CHANGELOG correctly does not call this a state migration — there's no `Waiting → Blocked` upgrade path needed because no Goal in any reference impl has likely been stamped Waiting.
2. **Added `Intent Envelope` and `Decision` to Terminology.** They were the two canonical Kernel concepts with the most cross-references (counted 30+ `Intent Envelope` usages in roles/protocols) but no entry in the normative-vocabulary doc. Closing that gap is exactly what Terminology is for.
3. **Lease semantics added to the right role.** Coordination Fabric is the only place leases belong. REQ-004 is correctly conditional (`MAY implement…`) and anchored to the Task Protocol. Good.
4. **Normative consistency holds.** Goal schema `state` enum matches MTH-010 canonical states (8); Task schema matches MTH-012 (10); Evidence schema matches MTH-015 (6); Decision schema matches MTH-016 (5). All six JSON schemas parse cleanly.

---

## 🔴 Must address in this round

### R3-1. `MTH-001 Terminology` — `Intent Envelope` and `Decision` are placed in the wrong section

**File:** `specification/foundation/MTH-001-Terminology.md`
**Lines:** 236–252

The two new entries were inserted **between** `# Normative Requirements` (which ends at line 234) and `# Future Directions` — i.e. they live in dead air, outside the `# Normative Definitions` section that contains every other capitalized term (`Principal`, `Participant`, `Role`, `Goal`, `Task`, `Capability`, `Artifact`, `Evidence`, `Protocol`, `Contract`, `State`, `Knowledge Repository`, `Coordination Fabric`, `Inference Engine`, `Execution`, `Lifecycle`).

**Why this matters:**
- `MTH-001-REQ-001` says "Specifications SHALL use the normative terminology defined within this document." A reader scanning `# Normative Definitions` will not find `Intent Envelope` or `Decision` there — they'll find them tucked into a non-section between REQ-003 and Future Directions. That undercuts the document's own claim of being a single normative vocabulary.
- Rendered as Markdown, `## Intent Envelope` and `## Decision` parse as sub-headers of `# Normative Requirements` (which ends with `**MTH-001-REQ-003**` on line 231), not as part of `# Normative Definitions`. They're effectively orphan sections.
- Rendering issue: there's no horizontal rule `---` between `MTH-001-REQ-003` (line 231) and `## Intent Envelope` (line 236) to make Intent Envelope a sibling of the other definitions.

**Fix:** Move both entries up into `# Normative Definitions`, ideally near related terms (`Intent Envelope` after `Goal`; `Decision` after `Evidence`, since Decisions reference Evidence). Add a `---` rule. Resulting shape:

```text
# Normative Definitions
## Principal
## Participant
## Role
## Implementation
## Goal
## Intent Envelope       ← new, here
## Task
## Capability
## Artifact
## Evidence
## Decision              ← new, here
## Protocol
## Contract
## State
...
---
# Naming Conventions
---
# Normative Requirements
**MTH-001-REQ-001..003**
---
# Future Directions
---
# Revision History
```

### R3-2. `MTH-024 Coordination Fabric` — lease section is normative body, not role-behavior

**File:** `specification/roles/MTH-024-Coordination-Fabric.md`
**Lines:** 139–156 (new `# Lease Semantics` section), 174–176 (new `REQ-004`)

The document has a strict separation: `# Responsibilities` (lines 51–62) lists what the Fabric SHALL do; `# Operational State` (lines 65–78) lists what counts as operational state; `# Non-Responsibilities` (lines 92–101) is explicit fencing. The new `# Lease Semantics` reads like it belongs in `# Operational State`, but it's parked **after** `# Conformance` and **before** `# Normative Requirements` — inside the conformance section. Functionally fine, structurally inconsistent.

Additionally: **REQ-004 is sound but redundant with the prose that precedes it.** Lines 150–151 say "Upon lease expiration the Coordination Fabric SHALL release exclusive ownership. If the associated Task has not transitioned to a terminal state, it SHALL become eligible for reassignment…". REQ-004 then says the same thing ("lease expiration SHALL release exclusive ownership of the Task and SHALL permit reassignment in accordance with the Task Protocol"). The prose is normative; REQ-004 is normative. Keeping both is OK (REQ-004 is more discoverable in the requirements index), but the prose should drop the redundant `SHALL`s to avoid double-shouting the same constraint, OR the REQ-004 should explicitly defer to the prose.

**Fix (preferred — minimum change):** Move the `# Lease Semantics` block (lines 139–156) to live as a sub-section under `# Operational State`, and add a single sentence at the end of `# Operational State` saying leases are one example of operational state. Leave REQ-004 where it is in the requirements index; in the `# Lease Semantics` prose, change the two `SHALL` statements to "does" / "is" since REQ-004 already makes them normative.

### R3-3. `MTH-010 Goal` — `Waiting` removal creates a stale reference in `dossier/SYSTEM.md`

**Files:** `dossier/SYSTEM.md` line 66, `dossier/Templates/task.md`, `specification/protocols/MTH-031-Task-Protocol.md`

The `Waiting` state was a Goal state. Round 3 removed it from Goal. Confirming `Waiting` remains correct on Task (yes — Task keeps it per MTH-012:140 and T-Protocol line 142). However, the dossier system narrative might still list Waiting as a Goal state. Verify:

```text
$ grep -n "Waiting\|Blocked" dossier/SYSTEM.md
```

(Report: line 66 of dossier/SYSTEM.md does still have "Waiting" — but it's in the canonical-state rollout table. If the table is Goal + Task + Evidence, then Waiting-as-Task is correct and no fix needed. If the table is Goals only, this is a stale reference that needs to come out, replaced with the explicit successor mapping or a pointer to MTH-012.)

Also worth checking: the dossier goal template `dossier/Templates/goal.md` — does it reference the Waiting state anywhere? (Suggest running the grep across `dossier/` and verifying no Goal-template mentions Waiting.)

**Why:** Even though the spec is the source of truth (per CHANGELOG architectural decision), the dossier templates are the human/agent authoring forms. A user reading `dossier/Templates/goal.md` and seeing "Waiting" as a Goal state will be confused.

**Fix:** Grep `dossier/` for `\bWaiting\b` and remove Goal-state uses. Keep Task-state uses.

---

## ⚠️ Advisories (not blocking; address in subsequent round)

### A-1. `MTH-010 Goal` has no `## Waiting` definition but `MTH-024` change-history note is silent

The CHANGELOG is currently titled "Agent Feedback Integration" but a separate "v1.0.1 → v1.0.2" entry is not yet added for round 3. If this gets tagged again (a v1.0.2), the CHANGELOG needs a new section or rolled-up entry for these three commits. Otherwise reviewers like me have to reconstruct what changed via `git log`.

**Recommended:** Either rename the current "Unreleased — Agent Feedback Integration" heading to "v1.0.2 — Round 3 Doxa feedback reconciliation" and add a `### Changed` block, or move the round-2 + round-3 entries under a "v1.0.x — Agent Feedback Integration" heading with both 1.0.1 and 1.0.2 sub-versions. Otherwise the changelog is operating as a snapshot of one unspecified point in time.

### A-2. `MTH-001 Terminology` Future-Directions still lists `Decision` removal but the list now has `Constraint` while `MTH-010 Goal` already uses the term `Constraint` as a normative required-property

Lines 257–267 list `Constraint` under Future Directions. But MTH-010:140–156 already normalizes `Constraints` as a Goal property (`Every Goal defines Constraints` is implied by `Required Properties` line 56: `* Constraints`). The Future-Directions entry implies Constraint is still pending definition; it isn't. Either remove `Constraint` from Future Directions (it's already implicitly defined via `MTH-010 Goal`), or add a one-liner Terminology entry for `Constraint`.

### A-3. `MTH-001 Terminology` Future-Directions still lists `Session` — and `MTH-016 Decision` relationships refer to Sessions

Lines 257–267 include `Session` in Future Directions. MTH-016:114 already references Sessions in a `MAY reference:` list, but there's no MTH entry for Session itself. Either add Session to Terminology (deferring to a future MTH-0XX spec) or note that "Session is intentionally undefined pending governance of session lifetime." Low priority, but it's the kind of thing that looks fine today and bites in six months.

### A-4. Frontmatter / dossier templates — required-but-optional gap

The Goal schema requires `intent_envelope`. MTH-011 says `Every Intent Envelope SHALL contain: Objective; Success Criteria; Constraints; Acceptance Criteria; Principal; Created; Modified`. The Goal schema's `intent_envelope` requires `{objective, success_criteria, constraints, acceptance_criteria}` but **does not require** `Principal`, `Created`, `Modified` — even though MTH-011 says they SHALL be present. Either tighten the schema (`"required": [..., "principal", "created", "modified"]`) or loosen MTH-011 to admit the omission. Same issue, mirrored: schema strict, spec loose.

This also shows up in `inherited_intent_context` (Task schema lines 24–32): required is `{objective, success_criteria, constraints}` but MTH-011:138–142 says inherited context SHOULD include `{objective, success_criteria, constraints, acceptance_criteria, out-of-scope}` — schema is weaker than spec implies. Either tighten schema or weaken spec.

---

## 🔵 Lingering issues from round 2 surfaced (but not caused) by round 3

These are not round-3 regressions, but round 3 was the first time the spec reached a state stable enough that I could notice them. File under "round 4."

### L1. `MTH-020 Principal`, `MTH-021 Orchestrator`, `MTH-022 Executor`, `MTH-029 Reviewer` — required properties exist in spec text but no JSON schemas

The kernel + Intent Envelope + Goal/Task/Evidence/Decision schemas exist. Roles do not. Either it's an intentional decision (roles aren't schema-validated because they're organizational, not object), or it's a gap. The spec text doesn't make this clear.

**Suggested:** Add a sentence to `MTH-001` (or wherever) — "Role Objects are organizational descriptors and are not schema-validated; Participants are validated through their associated Object interactions." Or, if Roles ARE going to be schema-validated eventually, add an "Open Spec: Role Schemas" entry to the Future-Directions list.

### L2. Methodos is missing a Reference Architecture doc

We have Kernel (object specs), Protocols, Roles, and Schemas — but no top-level `MTH-100 System Architecture` that answers "how does a Goal flow through the system from Principal authorization → Intent Envelope → Orchestrator intake → Planning → Task issuance → Execution → Evidence → Decision → Goal completion?" That's the most-asked question a new reader will have and it's scattered across four PDFs.

**Suggested:** Add `specification/MTH-100-Reference-Architecture.md` as one narrative walkthrough with citations into the kernel/protocol/role specs. This is what reviewers (and future agents) will read first.

### L3. Confidence model assumes "Verified" implies human/independent review but never says so

MTH-015 defines:
- Low — preliminary supporting information
- Moderate — supporting Artifacts internally substantiate Claims
- High — Claims have undergone independent review
- Verified — Claims have been independently reproduced, measured, executed, or otherwise validated through an approved verification method

It says "Only independent review or independent verification MAY increase Confidence beyond Moderate" but doesn't say who's allowed to mark Verified (Presumably the Reviewer role, but MTH-029 says the Reviewer "evaluates whether completed work satisfies the Principal's Intent Envelope and the applicable Success Criteria" — not "marks Verified"). There's a gap between "may increase confidence" and "no role is defined as authorized to push to Verified."

**Suggested:** Add a note in MTH-015 or MTH-029 about who can promote Evidence to `Verified`.

---

## Things I tested

- `python3 -c 'import json; json.load(open(...))'` parses all six schemas under `schemas/*.json` cleanly.
- `grep -n "Waiting"` against `specification/` and `dossier/`: Waiting removed from Goal (MTH-010), still present in Task (MTH-012:140, T-Prot:142) — correct.
- `grep -n "Intent Envelope"` against `specification/`: 30+ cross-references, of which 28 are *in spec files* (the other 2 are references inside protocol text or frontmatter `Depends Upon`). Adding the Terminology entry was overdue.
- Cross-checked Goal schema `state` enum against MTH-010 §"Goal States" — match (8 states each).
- Cross-checked Task schema `state` enum against MTH-012 §"Lifecycle" — match (10 states each).
- Cross-checked Evidence schema `state` enum against MTH-015 §"Lifecycle" — match (6 states each).
- Cross-checked Decision schema `state` enum against MTH-016 §"Lifecycle" — match (5 states each).
- Cross-checked Decision schema `decision_type` enum against MTH-016 §"Decision Types" — match (9 types each).
- Cross-checked Evidence schema `confidence` enum against MTH-015 §"Confidence" — match (4 levels each).

---

## My recommendation

1. Address R3-1, R3-2, R3-3 in this round. They're all 5–10 minute moves and they prevent readers from being misled.
2. After R3 ships, file a "v1.0.3 — Cross-document Hygiene" round and address A-1..A-4 and L1..L3. They're not blockers but they're paper cuts that will hurt when the Implementation phase starts hitting these docs for real.
3. Re-tag as `v1.0.2` after this round lands.

— Phronesis, 2026-06-29
