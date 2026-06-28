# Méthodos Specification

**Identifier:** MTH-031

**Title:** Task Protocol

**Version:** 0.1.0

**Status:** Draft

**Category:** Protocols

**Depends Upon:** MTH-011 Task, MTH-021 Orchestrator, MTH-022 Executor, MTH-030 Goal Protocol

---

# Abstract

This specification defines the Task Protocol.

The Task Protocol governs the creation, delegation, execution, review, completion, and archival of Tasks.

Tasks are the fundamental unit of delegation within Méthodos.

The Task Protocol defines how Orchestrators and Executors collaborate while preserving Goal intent and maintaining accountability.

---

# Architectural Intent

Provide a deterministic protocol for delegating bounded work between Participants.

---

# Participants

| Participant  | Responsibility                                  |
| ------------ | ----------------------------------------------- |
| Orchestrator | Creates, assigns, coordinates and reviews Tasks |
| Executor     | Executes assigned Tasks                         |
| Reviewer     | Reviews work when required                      |

---

# Ownership

The Orchestrator owns:

* Task definition
* Task objective
* Success Criteria
* Constraints
* Assignment
* Lifecycle
* Review

The Executor owns:

* Execution strategy
* Execution notes
* Produced Artifacts
* Progress reporting

The Executor SHALL NOT modify the Task Objective or Success Criteria.

---

# Task State Machine

Tasks SHALL progress through the following lifecycle.

```text
Draft
  │
  ▼
Ready
  │
  ▼
Assigned
  │
  ▼
Executing
  │
  ├────────────► Blocked
  │                  │
  │                  ▼
  │              Executing
  │
  ▼
Ready for Review
  │
  ├────────────► Executing
  │
  ▼
Accepted
  │
  ▼
Closed
```

The canonical lifecycle SHALL be preserved.

---

# State Definitions

## Draft

The Task is incomplete.

It SHALL NOT be executed.

---

## Ready

The Task is executable.

The Orchestrator MAY assign it.

---

## Assigned

The Task has been delegated to an Executor.

The Executor SHALL validate that sufficient information exists before beginning execution.

---

## Executing

The Executor is actively performing work.

The Executor SHOULD publish progress Events.

---

## Blocked

Execution cannot continue.

The Executor SHALL provide:

* blocker description
* reason
* recommended next action

---

## Ready for Review

Execution has concluded.

The Executor believes the Task satisfies its Success Criteria.

The Executor SHALL provide:

* Artifacts
* execution summary
* status report

The Task SHALL NOT be considered complete.

---

## Accepted

The Orchestrator has reviewed the work.

Evidence has been assembled.

A governing Decision has been recorded.

---

## Closed

The Task has reached a terminal state.

Historical information SHALL remain discoverable.

---

# Preconditions

Before assigning a Task, the Orchestrator SHALL ensure the Task includes:

* Parent Goal
* Objective
* Success Criteria
* Constraints
* Expected Deliverables
* Reporting Requirements

Tasks missing these elements SHOULD remain in Draft.

---

# Protocol

## Step 1 — Task Creation

The Orchestrator creates a Task.

Initial State:

```text
Draft
```

---

## Step 2 — Task Validation

The Orchestrator verifies that the Task is executable.

State:

```text
Ready
```

---

## Step 3 — Assignment

The Task is delegated to an Executor.

State:

```text
Assigned
```

The assignment SHALL preserve the Goal's Intent Envelope.

---

## Step 4 — Acceptance

The Executor SHALL verify that:

* Success Criteria are clear;
* Constraints are understood;
* Required context exists.

If clarification is required, the Executor SHALL report:

```text
needs_clarification
```

The Executor SHALL NOT silently expand the Task scope.

---

## Step 5 — Execution

The Executor MAY use internal autonomous execution mechanisms (such as `/goal`) to accomplish the assigned Task.

Such mechanisms SHALL remain scoped to the delegated Task.

The Executor SHALL NOT reinterpret the parent Goal.

State:

```text
Executing
```

---

## Step 6 — Reporting

Upon completion of execution, the Executor SHALL report one of:

* ready_for_review
* blocked
* waiting
* failed
* needs_clarification

Supporting Artifacts SHALL accompany a `ready_for_review` report.

---

## Step 7 — Review

The Orchestrator SHALL:

* inspect Artifacts;
* assemble Evidence;
* determine whether Success Criteria have been met.

Executor reports SHALL NOT constitute Evidence.

---

## Step 8 — Acceptance

If the Task satisfies its Success Criteria:

* Evidence SHALL be assembled.
* A governing Decision SHALL be recorded.

State:

```text
Accepted
```

Otherwise the Task MAY return to:

```text
Executing
```

with additional work requested.

---

## Step 9 — Closure

Accepted Tasks MAY be closed.

Closed Tasks SHALL remain discoverable.

---

# Failure Handling

The Task SHALL enter Blocked when:

* dependencies are unavailable;
* execution cannot continue safely;
* clarification is required;
* required infrastructure is unavailable.

Blocked Tasks SHALL retain all historical information.

---

# Scope Preservation

The Executor SHALL treat the delegated Task as the maximum authorized scope of autonomous execution.

Expanding scope SHALL require Orchestrator authorization.

---

# Completion Conditions

A Task SHALL NOT transition to Accepted unless:

* Success Criteria have been evaluated;
* required Artifacts exist;
* supporting Evidence exists;
* a governing Decision exists.

---

# Conformance

A conforming implementation SHALL:

* delegate bounded Tasks;
* preserve Goal intent;
* respect Ownership Domains;
* require Evidence before acceptance;
* preserve traceability;
* maintain Task history.

---

# Normative Requirements

**MTH-031-REQ-001**

Tasks SHALL be the unit of delegation.

**MTH-031-REQ-002**

Executors SHALL execute only delegated Tasks.

**MTH-031-REQ-003**

Executors SHALL preserve the Goal Intent Envelope.

**MTH-031-REQ-004**

Executors SHALL NOT expand Task scope without authorization.

**MTH-031-REQ-005**

Executor reports SHALL NOT constitute Evidence.

**MTH-031-REQ-006**

Task acceptance SHALL require a governing Decision.

---

# Design Rationale

The Task Protocol separates delegation from execution.

The Orchestrator defines *what* bounded work is required.

The Executor determines *how* to accomplish that work within the defined constraints.

This separation enables autonomous execution while preserving accountability, governance, and alignment with the parent Goal.

---

# Revision History

| Version | Date          | Notes             |
| ------- | ------------- | ----------------- |
| 0.1.0   | Initial draft | First publication |
