# Méthodos Specification

**Identifier:** MTH-012

**Title:** Task

**Version:** 0.1.0

**Status:** Draft

**Category:** Kernel

**Depends Upon:** MTH-000 through MTH-011

---

# Abstract

This specification defines the Task Object.

A Task is the smallest unit of independently assignable work within Méthodos.

Tasks preserve the parent Goal's Intent Envelope while allowing bounded work to be delegated to a Participant.

---

# Architectural Intent

Represent bounded, independently executable work while preserving the Intent Envelope.

---

# Purpose

Tasks allow complex Goals to be decomposed into work that can be:

* assigned;
* executed;
* paused;
* resumed;
* validated;
* audited;
* completed;

without altering the Principal's intended outcome.

---

# Definition

A Task is a bounded unit of work contributing to exactly one Goal.

A Task specifies **what** work shall be performed.

It does not specify **how** the work is performed.

Execution strategy remains the responsibility of the assigned Executor.

---

# Required Properties

Every Task SHALL contain:

* Identifier
* Parent Goal Identifier
* Title
* Description
* Current State
* Owner
* Priority
* Objective
* Success Criteria
* Constraints
* Inherited Intent Context
* Dependencies
* Created Timestamp
* Modified Timestamp

A Task MAY additionally contain:

* Assigned Participant
* Artifacts
* Evidence
* Decisions
* Events
* Tags
* Implementation-specific metadata

---

# Ownership

Every Task SHALL have exactly one Owner.

Ownership MAY transfer only through a defined Protocol.

Only one Participant MAY actively own a Task at any point in time.

Assignment and ownership are distinct concepts.

An assigned Task remains owned by its Owner until ownership is explicitly transferred.

---

# Relationships

Every Task SHALL belong to exactly one Goal.

A Task MAY:

* depend upon other Tasks;
* produce Artifacts;
* produce Events;
* contribute Evidence;
* reference Decisions.

A Task SHALL NOT belong to multiple Goals.

---

# Intent Preservation

Every Task SHALL inherit the relevant Intent Envelope from its parent Goal.

The inherited Intent Context SHALL include sufficient information for an Executor to perform the Task without redefining the Principal's intent.

A Task SHALL NOT modify or reinterpret the parent Goal's Intent Envelope.

---

# Lifecycle

A Task SHALL occupy exactly one of the following canonical States:

* Draft
* Ready
* Assigned
* Executing
* Waiting
* Blocked
* Ready for Review
* Accepted
* Cancelled
* Archived

Operational scheduling states (such as queues, leases, claims, or reservations) are implementation-specific and SHALL NOT be represented as canonical Task States.

---

# State Definitions

## Draft

The Task exists but is incomplete.

---

## Ready

The Task satisfies the required definition and is eligible for assignment.

---

## Assigned

Responsibility for execution has been delegated to a Participant.

---

## Executing

The assigned Participant is actively performing work.

---

## Waiting

Execution is temporarily paused awaiting an external dependency or condition.

---

## Blocked

Execution cannot proceed without intervention.

---

## Ready for Review

Execution is complete and supporting Artifacts have been produced.

The Task awaits review and governance.

---

## Accepted

The Task has been accepted following review.

Required Evidence and governing Decisions exist.

---

## Cancelled

Execution has been intentionally terminated.

The Task contributes no further work toward the Goal.

---

## Archived

The Task is retained for historical reference.

---

# Success Criteria

Every Task SHALL define observable Success Criteria.

Task completion SHALL be determined against those Success Criteria rather than subjective judgment.

---

# Dependencies

Tasks MAY depend upon other Tasks.

A Task SHOULD NOT enter Executing until required dependencies have reached Accepted unless explicitly authorized.

Circular dependencies SHOULD be avoided.

---

# Constraints

Tasks inherit Constraints from the parent Goal's Intent Envelope.

Tasks MAY introduce additional Constraints provided they do not contradict inherited Constraints.

---

# Evidence

Completion of a Task SHALL result in sufficient Evidence to support review.

Acceptance without supporting Evidence is non-conforming.

---

# Invariants

The following SHALL always remain true:

* Every Task belongs to exactly one Goal.
* Every Task has exactly one Owner.
* Every Task occupies exactly one canonical State.
* Every Task preserves the parent Goal's Intent Envelope.
* Every Accepted Task references supporting Evidence.

---

# Conformance

A conforming implementation SHALL ensure that every Task:

* possesses the required properties;
* belongs to exactly one Goal;
* preserves the Intent Envelope;
* follows the canonical lifecycle;
* produces Evidence supporting acceptance;
* maintains observable ownership and traceability.

---

# Normative Requirements

**MTH-012-REQ-001**

Every Task SHALL belong to exactly one Goal.

**MTH-012-REQ-002**

Every Task SHALL have exactly one Owner.

**MTH-012-REQ-003**

Every Task SHALL occupy exactly one canonical State.

**MTH-012-REQ-004**

Every Task SHALL preserve the inherited Intent Envelope.

**MTH-012-REQ-005**

A Task SHALL NOT transition to Accepted without supporting Evidence and an applicable Final Decision.

**MTH-012-REQ-006**

Operational scheduling mechanisms SHALL NOT introduce additional canonical Task States.

---

# Anti-Patterns

The following behaviors are non-conforming or discouraged:

* Tasks without Success Criteria.
* Tasks belonging to multiple Goals.
* Multiple active Owners.
* Reinterpreting the inherited Intent Envelope.
* Completing Tasks based solely on assertion.
* Embedding implementation-specific scheduling semantics into the canonical object.
* Creating Tasks that cannot be independently reviewed or validated.

---

# Design Rationale

The Task Object is the primary contract between planning and execution.

It intentionally separates semantic work definition from operational scheduling.

This distinction allows different implementations to use queues, leases, reservations, distributed schedulers, or other coordination mechanisms while preserving a stable, implementation-independent Task model.

---

# Future Directions

Future specifications may define:

* task dependency graphs;
* execution policies;
* scheduling strategies;
* lease semantics;
* workload balancing.

These behaviors are intentionally excluded from the canonical Task Object.

---

# Revision History

| Version | Date             | Notes                                                     |
| ------- | ---------------- | --------------------------------------------------------- |
| 0.2.0   | Initial revision | Reconciled with Intent Envelope and canonical state model |
