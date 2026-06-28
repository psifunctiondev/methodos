# Méthodos Specification

**Identifier:** MTH-011

**Title:** Task Object

**Version:** 0.1.0

**Status:** Draft

**Category:** Kernel

**Depends Upon:** MTH-000 through MTH-010

---

# Abstract

This specification defines the Task Object.

A Task is the smallest unit of independently assignable work within Méthodos.

Tasks preserve the Goal's intent while allowing execution to be delegated to a Participant.

---

# Architectural Intent

Represent bounded, independently executable work.

---

# Purpose

Tasks allow complex Goals to be decomposed into work that can be:

* assigned,
* executed,
* validated,
* resumed,
* audited,
* and completed

without losing the Goal's original intent.

---

# Definition

A Task is a bounded unit of work that contributes to exactly one Goal.

Tasks describe **what work shall be performed**, not **who performs it** nor **how it is implemented**.

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
* Success Criteria
* Constraints
* Dependencies
* Assigned Participant (optional)
* Created Timestamp
* Modified Timestamp

---

# Ownership

A Task SHALL have exactly one Owner.

Ownership MAY transfer through a documented Protocol.

Only one Participant MAY actively own a Task at a time.

---

# Relationships

Every Task SHALL belong to exactly one Goal.

A Task MAY:

* depend on other Tasks
* produce Artifacts
* produce Events
* produce Evidence
* reference Decisions

A Task SHALL NOT belong to multiple Goals.

---

# Lifecycle

A Task SHALL occupy exactly one of the following States:

* Draft
* Ready
* Queued
* Claimed
* Executing
* Waiting
* Blocked
* Review
* Complete
* Cancelled
* Archived

---

# State Definitions

## Draft

The Task exists but is incomplete.

## Ready

The Task is sufficiently defined for scheduling.

## Queued

The Task is available for assignment.

## Claimed

A Participant has accepted responsibility.

## Executing

Work is actively occurring.

## Waiting

Execution is paused awaiting an external condition.

## Blocked

Execution cannot continue.

## Review

Execution has finished and awaits acceptance.

## Complete

Success Criteria have been satisfied.

## Cancelled

The Task will not be executed.

## Archived

The Task is retained for historical purposes.

---

# Success Criteria

Every Task SHALL define observable Success Criteria.

Completion SHALL be determined by those criteria rather than subjective judgment.

---

# Dependencies

Tasks MAY depend upon other Tasks.

Dependent Tasks SHALL NOT enter Executing until required dependencies have reached Complete unless explicitly authorized.

Circular dependencies SHOULD be avoided.

---

# Constraints

Tasks inherit Constraints from their parent Goal.

Tasks MAY introduce additional Constraints provided they do not contradict Goal Constraints.

---

# Evidence

A Task SHALL produce sufficient Evidence to justify entering the Complete State.

Completion without Evidence is non-conforming.

---

# Invariants

The following SHALL always remain true:

* Every Task has one parent Goal.
* Every Task has one Owner.
* Every Task has one State.
* Every Task preserves Goal intent.
* Every completed Task references Evidence.

---

# Conformance

An implementation conforms to this specification if every Task:

* possesses the required properties,
* belongs to exactly one Goal,
* maintains a valid lifecycle,
* preserves Goal intent,
* produces Evidence upon completion,
* and maintains observable ownership.

---

# Normative Requirements

**MTH-011-REQ-001**

Every Task SHALL have exactly one parent Goal.

**MTH-011-REQ-002**

Every Task SHALL have exactly one current Owner.

**MTH-011-REQ-003**

Every Task SHALL occupy exactly one State.

**MTH-011-REQ-004**

Tasks SHALL preserve the Intent Envelope of their parent Goal.

**MTH-011-REQ-005**

A Task SHALL NOT enter Complete without associated Evidence.

**MTH-011-REQ-006**

Only one Participant MAY actively own a Task at any point in time.

---

# Anti-Patterns

The following behaviors are non-conforming or discouraged:

* Tasks without Success Criteria.
* Tasks belonging to multiple Goals.
* Multiple active Owners.
* Completing Tasks based solely on assertion.
* Embedding implementation-specific details that belong to the executing Participant.
* Creating Tasks so large they cannot be independently completed or validated.

---

# Design Rationale

The Task Object is the primary contract between planning and execution.

It is intentionally implementation-independent. Any conforming Participant capable of understanding the Task and satisfying its Success Criteria may execute it.

This separation enables interchangeable Executors, distributed execution, recovery after interruption, and independent validation.

---

# Future Directions

Future specifications will define:

* Task Protocol
* Task Assignment Protocol
* Task State Machine
* Task Templates
* Dependency Resolution

---

# Revision History

| Version | Date          | Notes             |
| ------- | ------------- | ----------------- |
| 0.1.0   | Initial draft | First publication |
