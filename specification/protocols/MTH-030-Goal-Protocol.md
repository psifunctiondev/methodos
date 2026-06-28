# Méthodos Specification

**Identifier:** MTH-030

**Title:** Goal Protocol

**Version:** 0.1.0

**Status:** Draft

**Category:** Protocols

**Depends Upon:** MTH-010 Goal, MTH-020 Principal, MTH-021 Orchestrator

---

# Abstract

This specification defines the Goal Protocol.

The Goal Protocol governs the lifecycle of a Goal from its creation by the Principal through planning, execution, review, completion, and archival.

The Goal Protocol defines state transitions, participant responsibilities, and the conditions under which a Goal may progress.

---

# Architectural Intent

Provide a deterministic lifecycle for Goal execution while preserving the Principal's Intent Envelope.

---

# Participants

The following Participants participate in the Goal Protocol:

| Participant  | Responsibility               |
| ------------ | ---------------------------- |
| Principal    | Defines and owns Goal intent |
| Orchestrator | Manages Goal lifecycle       |
| Executor     | Executes delegated Tasks     |
| Reviewer     | Reviews work when required   |

---

# Ownership

The Principal owns:

* Objective
* Success Criteria
* Constraints
* Acceptance Criteria

The Orchestrator owns:

* Planning
* Task decomposition
* Goal status
* Progress tracking
* Evidence assembly
* Recommendations

The Executor SHALL NOT modify Goal intent.

---

# Goal State Machine

Goals SHALL progress through the following lifecycle:

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
  ├──────────────► Blocked
  │                    │
  │                    ▼
  │                Active
  │
  ▼
Review
  │
  ├──────────────► Active
  │
  ▼
Complete
  │
  ▼
Archived
```

Implementations MAY define additional transient states provided the canonical state progression is preserved.

---

# State Definitions

## Draft

The Goal is under construction.

Only the Principal SHOULD modify Goal intent.

The Orchestrator SHALL NOT create Tasks.

---

## Ready

The Goal is considered complete enough for planning.

The Orchestrator MAY begin analysis.

---

## Planning

The Orchestrator analyzes the Goal.

Typical activities include:

* decomposition
* dependency analysis
* Task creation
* risk identification
* scheduling

The Goal SHALL NOT enter Active until at least one executable Task exists.

---

## Active

The Goal is being executed.

The Orchestrator SHALL:

* monitor progress
* coordinate Executors
* assemble Evidence
* update Goal status

---

## Blocked

Execution cannot continue.

The Orchestrator SHALL record:

* blocker description
* affected Tasks
* recommended actions

The Goal MAY return to Active after the blocking condition is resolved.

---

## Review

Execution is complete.

The Orchestrator assembles Evidence.

Completion SHALL NOT be determined solely by Executor reports.

---

## Complete

The Principal or delegated authority accepts that the Goal's Success Criteria have been satisfied.

A Completion Decision SHALL exist.

---

## Archived

The Goal is no longer active.

Historical information SHALL remain discoverable.

---

# Protocol

## Step 1 — Goal Creation

The Principal creates a Goal.

The Goal SHALL contain:

* Objective
* Success Criteria
* Constraints
* Acceptance Criteria

Initial State:

```text
Draft
```

---

## Step 2 — Goal Authorization

The Principal marks the Goal:

```text
Ready
```

This authorizes the Orchestrator to begin planning.

The `Ready` state is the explicit Principal-to-Orchestrator handoff.

A Goal SHALL NOT be considered ready for planning merely because it exists.

When a Principal sets a Goal to `Ready`, the Orchestrator SHALL validate that the Goal contains a complete Intent Envelope before transitioning the Goal to `Planning`.

If validation fails, the Orchestrator SHALL record the deficiency and return the Goal to `Draft` or mark it `Blocked`, according to local policy.

---

## Step 3 — Planning

The Orchestrator:

* validates Goal completeness
* analyzes dependencies
* creates Tasks
* records planning decisions

State:

```text
Planning
```

---

## Step 4 — Execution

The Orchestrator publishes executable Tasks.

Execution begins after at least one Task has been accepted by an Executor.

State:

```text
Active
```

---

## Step 5 — Monitoring

During execution the Orchestrator SHALL:

* monitor Task state
* collect Events
* collect Artifacts
* identify risks
* identify blockers
* update Goal progress

---

## Step 6 — Review

After all required Tasks are complete, the Orchestrator SHALL:

* assemble Evidence
* evaluate Success Criteria
* prepare completion recommendation

State:

```text
Review
```

---

## Step 7 — Completion

Completion SHALL require:

* Goal Success Criteria satisfied
* supporting Evidence
* governing Decision

State:

```text
Complete
```

---

## Step 8 — Archival

Completed Goals MAY be archived.

Archival SHALL preserve:

* history
* Decisions
* Evidence
* Artifacts
* traceability

---

# Failure Handling

The Goal SHALL enter Blocked when:

* critical Tasks cannot continue;
* dependencies fail;
* Principal clarification is required;
* required infrastructure becomes unavailable.

The Goal SHALL NOT be marked Complete while Blocked.

---

# Ownership Domain Rules

The Orchestrator SHALL respect Ownership Domains.

The Principal's Intent Envelope SHALL NOT be modified during execution except through explicit authorization.

---

# Completion Conditions

A Goal SHALL NOT transition to Complete unless:

* all required Success Criteria have been evaluated;
* supporting Evidence exists;
* a governing Decision exists;
* required approvals have been obtained.

---

# Conformance

A conforming implementation SHALL:

* preserve Goal intent;
* implement the canonical lifecycle;
* respect Ownership Domains;
* require Evidence before completion;
* preserve traceability;
* maintain historical state.

---

# Normative Requirements

**MTH-030-REQ-001**

Goals SHALL progress through the canonical lifecycle.

**MTH-030-REQ-002**

Only the Principal MAY modify Goal intent unless an applicable Protocol authorizes otherwise.

**MTH-030-REQ-003**

The Orchestrator SHALL manage Goal lifecycle.

**MTH-030-REQ-004**

Completion SHALL require supporting Evidence.

**MTH-030-REQ-005**

Completion SHALL require a governing Decision.

**MTH-030-REQ-006**

Archived Goals SHALL remain discoverable.

---

# Design Rationale

The Goal Protocol separates ownership of intent from ownership of execution.

The Principal defines *what* should be achieved.

The Orchestrator determines *how* the Goal progresses through its lifecycle.

This separation permits autonomous execution while preserving accountability, governance, and institutional knowledge.

---

# Revision History

| Version | Date          | Notes             |
| ------- | ------------- | ----------------- |
| 0.1.0   | Initial draft | First publication |
