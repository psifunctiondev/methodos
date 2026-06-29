# Changelog

## v1.0.2 — Round 3 Cross-Document Hygiene

### Fixed

- Corrected `MTH-001 Terminology`: moved `Intent Envelope` and `Decision` definitions into `# Normative Definitions` (with `Intent Envelope` adjacent to `Goal` and `Decision` adjacent to `Evidence`). They were previously orphan sections between `# Normative Requirements` and `# Future Directions`.
- Corrected `MTH-024 Coordination Fabric`: moved `# Lease Semantics` under `# Operational State` and made the prose descriptive (deferring normative wording to `MTH-024-REQ-004`) instead of duplicating the same `SHALL`s.
- Verified `dossier/` templates contain no Goal-state `Waiting` references; the only remaining `Waiting` reference (`dossier/SYSTEM.md:66`) is correctly under *Task* states. No fix required.

## Unreleased — Agent Feedback Integration

### Added

- Added `MTH-011 Intent Envelope` as a first-class Kernel object.
- Added explicit Principal-to-Orchestrator Goal intake semantics.
- Added Goal intake validation requirements before `Ready → Planning`.
- Added atomic Task claim/assignment requirement to `MTH-031 Task Protocol`.
- Added reference lease defaults to the Redis implementation model:
  - 15-minute Task lease
  - 60-second heartbeat
  - 3 missed heartbeats before requeue
- Added canonical Evidence confidence semantics:
  - `Low`
  - `Moderate`
  - `High`
  - `Verified`
- Added distinction between Evidence confidence and probability/subjective belief.
- Added distinction between validation and independent verification.
- Added drafts for:
  - `MTH-017 Participant`
  - `MTH-018 Role`
  - `MTH-019 Capability`
  - `MTH-027 Tool Provider`

### Changed

- Renumbered Kernel objects after adding `Intent Envelope`.
- Standardized canonical Goal states:
  - `Draft`
  - `Ready`
  - `Planning`
  - `Active`
  - `Blocked`
  - `Review`
  - `Complete`
  - `Archived`
- Standardized canonical Task states:
  - `Draft`
  - `Ready`
  - `Assigned`
  - `Executing`
  - `Waiting`
  - `Blocked`
  - `Ready for Review`
  - `Accepted`
  - `Cancelled`
  - `Archived`
- Standardized canonical Evidence states:
  - `Draft`
  - `Assembled`
  - `Reviewed`
  - `Accepted`
  - `Superseded`
  - `Archived`
- Rewrote:
  - `MTH-012 Task`
  - `MTH-015 Evidence`
  - `MTH-030 Goal Protocol`
  - `MTH-031 Task Protocol`
  - `MTH-033 Evidence Protocol`
- Updated schemas to align with canonical object states.
- Updated dossier templates to align with canonical states and Intent Envelope terminology.
- Replaced `vault/` terminology with canonical `dossier/` terminology.
- Clarified distinction between:
  - Knowledge Repository
  - Dossier
  - METHODOS.md
  - dossier/SYSTEM.md
- Renamed root `SYSTEM.md` to `METHODOS.md`.

### Removed

- Removed stale `Submitted` Evidence state.
- Removed stale `vault/` terminology.
- Removed obsolete `target-structure.md`.
- Removed duplicate/root-level `SYSTEM.md` ambiguity.

### Fixed

- Fixed stale internal MTH identifiers after Kernel renumbering.
- Fixed stale `Depends Upon` references across Kernel, Role, and Protocol specifications.
- Fixed stale `MTH-012 Event` reference in `MTH-035 Event Protocol`.
- Fixed `Ddossier` typo.
- Fixed state divergence among Object specs, Protocols, Schemas, and Dossier templates.

### Architectural Decisions

- Object specifications are the source of truth for canonical states.
- Protocols define legal transitions and participant responsibilities.
- Schemas validate canonical object structure.
- Templates provide human/agent authoring forms.
- Reference implementations define operational mechanics.
- Task queues, leases, claims, reservations, and heartbeats are Coordination Fabric mechanics, not canonical Task states.
