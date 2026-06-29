# Méthodos Specification

**Identifier:** MTH-030

**Title:** Goal Protocol

**Version:** 0.2.0

**Status:** Draft

**Category:** Protocols

**Depends Upon:** MTH-010 Goal, MTH-011 Intent Envelope, MTH-016 Decision, MTH-020 Principal, MTH-021 Orchestrator

---

# Abstract

This specification defines the Goal Protocol.

The Goal Protocol governs the lifecycle of a Goal from its creation by the Principal through planning, execution, review, completion, and archival.

The protocol defines participant responsibilities, state transitions, and the governance required before a Goal may progress.

---

# Architectural Intent

Provide a deterministic lifecycle for Goal execution while preserving the Principal's Intent Envelope.

---

# Participants

| Participant  | Responsibility                                 |
| ------------ | ---------------------------------------------- |
| Principal    | Defines the Goal and owns the Intent Envelope  |
| Orchestrator | Plans, coordinates, and governs Goal execution |
| Executor     | Executes delegated Tasks                       |
| Reviewer     | Reviews work when required                     |

---

# Ownership

The Principal owns the Intent Envelope.

The Orchestrator owns:

* planning;
* Task decomposition;
* Goal coordination;
* progress tracking;
* Evidence assembly;
* completion recommendations.

Executors SHALL NOT modify the Intent Envelope.

---

# Goal Lifecycle

A Goal SHALL occupy exactly one canonical State:

```text
Draft
  │
  ▼
Ready
  │
  ▼
Planning
  │
  ▼
Active
  │
  ├────────────► Blocked
  │                 │
  │                 ▼
  └────────────── Active
  │
  ▼
Review
  │
  ├────────────► Active
  │
  ▼
Complete
  │
  ▼
Archived
```

---

# State Definitions

## Draft

The Goal is under construction.

Only the Principal SHOULD modify the Intent Envelope.

No planning occurs.

---

## Ready

The Principal has explicitly requested planning.

Ready represents the formal handoff from Principal to Orchestrator.

---

## Planning

The Orchestrator validates the Goal and constructs the execution plan.

Planning MAY include:

* decomposition;
* dependency analysis;
* Task creation;
* risk analysis;
* sequencing.

---

## Active

One or more executable Tasks exist.

The Orchestrator coordinates execution.

---

## Blocked

Execution cannot continue.

The blocking condition SHALL be recorded.

---

## Review

Execution is complete.

Evidence is assembled and evaluated.

Completion is assessed against the Intent Envelope.

---

## Complete

The Goal has satisfied its Success Criteria.

Required governance has occurred.

---

## Archived

The Goal is retained for historical reference.

---

# Protocol

## Step 1 — Goal Creation

The Principal creates a Goal.

The Goal SHALL contain:

* Intent Envelope;
* Owner;
* Priority.

Initial State:

```text
Draft
```

---

## Step 2 — Goal Authorization

The Principal explicitly changes the Goal State to:

```text
Ready
```

This SHALL be the only mechanism that authorizes planning.

A Goal SHALL NOT be planned merely because it exists.

---

## Step 3 — Goal Intake

Upon observing a Goal in the Ready state, the Orchestrator SHALL validate that the Goal contains a complete Intent Envelope.

The validation SHALL confirm:

* Objective;
* Success Criteria;
* Constraints;
* Acceptance Criteria;
* Principal;
* Priority.

If validation succeeds:

```text
Ready → Planning
```

If validation fails:

The Orchestrator SHALL:

* generate an Event;
* record the validation deficiencies;
* return the Goal to Draft or transition it to Blocked according to implementation policy.

---

## Step 4 — Planning

During Planning the Orchestrator SHALL:

* analyze dependencies;
* decompose the Goal into Tasks;
* assign ownership;
* identify risks;
* preserve the Intent Envelope.

The Goal SHALL NOT enter Active until at least one executable Task exists.

---

## Step 5 — Execution

The Goal transitions to:

```text
Active
```

The Orchestrator SHALL:

* coordinate Executors;
* monitor Task progress;
* collect Events;
* collect Artifacts;
* assemble Evidence;
* monitor risks.

---

## Step 6 — Blocked Goals

A Goal SHALL transition to Blocked when progress cannot continue because of:

* unresolved dependencies;
* missing information;
* infrastructure failures;
* unavailable Participants;
* required Principal clarification.

Blocked Goals SHALL preserve all existing state.

---

## Step 7 — Review

When all required Tasks reach Accepted, the Orchestrator SHALL:

* assemble Evidence;
* evaluate Success Criteria;
* evaluate Acceptance Criteria;
* prepare a completion recommendation.

The Goal transitions to:

```text
Review
```

---

## Step 8 — Completion

A Goal SHALL transition to Complete only when:

* the Intent Envelope has been satisfied;
* supporting Evidence exists;
* required Approvals have been obtained;
* a Final Decision conforming to MTH-034 exists.

---

## Step 9 — Archival

Completed Goals MAY transition to:

```text
Archived
```

Archival SHALL preserve:

* Intent Envelope;
* Tasks;
* Events;
* Artifacts;
* Evidence;
* Decisions;
* traceability.

---

# Failure Handling

Goals SHALL transition to Blocked when required progress cannot continue.

The Goal SHALL NOT transition to Complete while Blocked.

Recovery SHALL conform to MTH-037.

---

# Completion Conditions

A Goal SHALL NOT transition to Complete unless:

* every Success Criterion has been evaluated;
* Acceptance Criteria have been satisfied;
* supporting Evidence exists;
* a Final Decision exists;
* required Approvals exist.

---

# Conformance

A conforming implementation SHALL:

* preserve the Intent Envelope;
* implement the canonical lifecycle;
* perform Goal intake validation;
* require Evidence before completion;
* require a Final Decision before completion;
* preserve historical traceability.

---

# Normative Requirements

**MTH-030-REQ-001**

Goals SHALL follow the canonical lifecycle defined by MTH-010.

**MTH-030-REQ-002**

The Ready state SHALL be the explicit Principal-to-Orchestrator handoff.

**MTH-030-REQ-003**

The Orchestrator SHALL validate the Intent Envelope before entering Planning.

**MTH-030-REQ-004**

The Orchestrator SHALL NOT modify the Intent Envelope.

**MTH-030-REQ-005**

Goal completion SHALL require supporting Evidence.

**MTH-030-REQ-006**

Goal completion SHALL require a Final Decision conforming to MTH-034.

**MTH-030-REQ-007**

Archived Goals SHALL remain fully traceable.

---

# Design Rationale

The Goal Protocol separates intent, planning, execution, review, and governance into distinct responsibilities.

The Principal defines **what** shall be accomplished through the Intent Envelope.

The Orchestrator determines **how** execution proceeds while preserving that Intent Envelope.

This separation allows autonomous Participants to collaborate while maintaining accountability, reproducibility, and institutional knowledge.

---

# Revision History

| Version | Date           | Notes                                                                            |
| ------- | -------------- | -------------------------------------------------------------------------------- |
| 0.2.0   | First revision | Added explicit Goal intake, Intent Envelope validation, and governance alignment |
