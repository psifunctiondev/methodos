# Méthodos Specification

**Identifier:** MTH-031

**Title:** Task Protocol

**Version:** 0.2.0

**Status:** Draft

**Category:** Protocols

**Depends Upon:** MTH-011 Intent Envelope, MTH-012 Task, MTH-016 Decision, MTH-030 Goal Protocol

---

# Abstract

This specification defines the Task Protocol.

The Task Protocol governs the creation, delegation, execution, review, acceptance, cancellation, and archival of Tasks.

Tasks are the primary unit of delegation within Méthodos.

The protocol defines how bounded work is assigned, executed, reviewed, and accepted while preserving the parent Goal's Intent Envelope.

---

# Architectural Intent

Provide a deterministic protocol for delegating bounded work between Participants while preserving governance and traceability.

---

# Participants

| Participant  | Responsibility                                     |
| ------------ | -------------------------------------------------- |
| Orchestrator | Creates, delegates, coordinates, and governs Tasks |
| Executor     | Executes delegated Tasks                           |
| Reviewer     | Reviews completed work when required               |
| Principal    | Approves outcomes when governance requires         |

---

# Ownership

The Orchestrator owns:

* Task definition;
* assignment;
* lifecycle;
* review coordination.

The Executor owns:

* execution strategy;
* execution progress;
* produced Artifacts.

The Executor SHALL preserve the inherited Intent Envelope.

The Executor SHALL NOT redefine:

* Objective;
* Success Criteria;
* Constraints.

---

# Task Lifecycle

A Task SHALL occupy exactly one canonical State:

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
  ├────────────► Waiting
  │                   │
  │                   ▼
  │               Executing
  │
  ├────────────► Blocked
  │                   │
  │                   ▼
  │               Executing
  │
  ▼
Ready for Review
  │
  ├────────────► Executing
  │
  ▼
Accepted
  │
  ├────────────► Archived
  │
  └────────────► Cancelled
```

Operational scheduling mechanisms such as queues, leases, claims, reservations, or heartbeats are implementation-specific and SHALL NOT introduce additional canonical Task States.

---

# State Definitions

## Draft

The Task is incomplete.

Execution SHALL NOT begin.

---

## Ready

The Task is complete enough for assignment.

---

## Assigned

Responsibility has been delegated to an Executor.

---

## Executing

The Executor is actively performing work.

---

## Waiting

Execution is temporarily paused awaiting an external dependency or condition.

---

## Blocked

Execution cannot continue without intervention.

---

## Ready for Review

Execution has completed.

Artifacts have been produced.

The Executor asserts that execution is complete.

The Task has **not** yet been accepted.

---

## Accepted

The Task has satisfied its Success Criteria.

Supporting Evidence exists.

A Final Decision authorizing acceptance exists.

---

## Cancelled

Execution has been intentionally terminated.

---

## Archived

The Task is retained for historical reference.

---

# Preconditions

Before assigning a Task, the Orchestrator SHALL ensure the Task contains:

* Parent Goal;
* Objective;
* Success Criteria;
* Constraints;
* inherited Intent Envelope context.

Tasks lacking these properties SHALL remain in Draft.

---

# Protocol

## Step 1 — Task Creation

The Orchestrator creates the Task.

Initial State:

```text
Draft
```

---

## Step 2 — Validation

The Orchestrator validates that the Task:

* is internally complete;
* preserves the parent Goal's Intent Envelope;
* is independently executable;
* has observable Success Criteria.

If validation succeeds:

```text
Draft → Ready
```

---

## Step 3 — Assignment

The Orchestrator delegates the Task to an Executor.

State:

```text
Assigned
```

The delegated Task SHALL include sufficient inherited Intent Envelope context for correct execution.

---

## Step 4 — Acceptance by Executor

Before beginning execution, the Executor SHALL verify that:

* the Task is understandable;
* required context exists;
* Success Criteria are achievable;
* Constraints are understood.

If clarification is required, execution SHALL NOT begin.

The Executor SHALL report the condition through implementation-defined mechanisms.

---

## Step 5 — Execution

The Executor performs the delegated work.

The Executor MAY employ autonomous planning or internal execution mechanisms, provided they remain entirely within the Task's authorized scope.

The Executor SHALL NOT expand scope or reinterpret the inherited Intent Envelope.

State:

```text
Executing
```

---

## Step 6 — Completion

When execution is complete, the Executor SHALL:

* publish required Artifacts;
* publish completion Events;
* provide sufficient information for review.

The Task transitions to:

```text
Ready for Review
```

Executor reports SHALL NOT constitute Evidence.

---

## Step 7 — Review

The Orchestrator or Reviewer SHALL:

* inspect Artifacts;
* assemble Evidence;
* evaluate Success Criteria;
* determine whether additional work is required.

If deficiencies exist:

```text
Ready for Review → Executing
```

Otherwise proceed.

---

## Step 8 — Acceptance

The Task SHALL transition to Accepted only when:

* Success Criteria have been satisfied;
* supporting Evidence exists;
* a Final Decision conforming to MTH-034 exists;
* required Approvals have been obtained.

---

## Step 9 — Archival

Accepted Tasks MAY transition to Archived.

Archival SHALL preserve:

* Artifacts;
* Events;
* Evidence;
* Decisions;
* complete traceability.

---

# Failure Handling

A Task SHALL transition to Waiting or Blocked when execution cannot continue.

Recovery SHALL conform to MTH-037.

Task history SHALL remain preserved.

---

# Scope Preservation

The delegated Task defines the maximum authorized execution scope.

Expanding scope SHALL require Orchestrator authorization.

The inherited Intent Envelope SHALL remain preserved throughout execution.

---

# Completion Conditions

A Task SHALL NOT transition to Accepted unless:

* every Success Criterion has been evaluated;
* required Artifacts exist;
* supporting Evidence exists;
* a Final Decision exists;
* required Approvals exist.

---

# Conformance

A conforming implementation SHALL:

* delegate bounded Tasks;
* preserve the inherited Intent Envelope;
* implement the canonical Task lifecycle;
* require Evidence before acceptance;
* require a Final Decision before acceptance;
* preserve historical traceability.

---

# Normative Requirements

**MTH-031-REQ-001**

Tasks SHALL be the canonical unit of delegation.

**MTH-031-REQ-002**

Executors SHALL execute only delegated Tasks.

**MTH-031-REQ-003**

Executors SHALL preserve the inherited Intent Envelope.

**MTH-031-REQ-004**

Executors SHALL NOT expand Task scope without Orchestrator authorization.

**MTH-031-REQ-005**

Executor completion reports SHALL NOT constitute Evidence.

**MTH-031-REQ-006**

Task acceptance SHALL require supporting Evidence.

**MTH-031-REQ-007**

Task acceptance SHALL require a Final Decision conforming to MTH-034.

**MTH-031-REQ-008**

Operational scheduling mechanisms SHALL NOT introduce additional canonical Task States.

---

# Design Rationale

The Task Protocol separates delegation, execution, review, and governance into distinct responsibilities.

The Orchestrator defines **what** bounded work is required.

The Executor determines **how** that work is accomplished within the delegated scope.

The Reviewer evaluates the resulting work.

Governance is completed through Evidence, Approval, and a Final Decision.

This separation enables autonomous execution while preserving accountability, reproducibility, and alignment with the parent Goal's Intent Envelope.

---

# Revision History

| Version | Date           | Notes                                                                    |
| ------- | -------------- | ------------------------------------------------------------------------ |
| 0.2.0   | First revision | Aligned with Intent Envelope, canonical Task model, and governance chain |
