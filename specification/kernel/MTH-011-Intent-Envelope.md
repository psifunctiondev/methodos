# Méthodos Specification

**Identifier:** MTH-011

**Title:** Intent Envelope

**Version:** 0.1.0

**Status:** Draft

**Category:** Kernel

**Depends Upon:** MTH-000 through MTH-010

---

# Abstract

This specification defines the Intent Envelope.

The Intent Envelope is the canonical representation of the Principal's intent for a Goal. It is the portion of a Goal that must be preserved through planning, delegation, execution, review, and archival.

The Intent Envelope exists to prevent intent drift.

---

# Architectural Intent

Preserve the Principal's intended outcome across delegation and execution.

---

# Purpose

The Intent Envelope provides a stable, explicit representation of what the Principal wants to achieve and under what conditions the outcome should be considered acceptable.

It separates intent from implementation.

Participants may plan, decompose, execute, retry, and review work in many different ways, but they SHALL preserve the Intent Envelope unless explicitly authorized to change it.

---

# Definition

An Intent Envelope is a Kernel Object contained by a Goal.

It defines the Principal-owned semantic core of that Goal.

The Intent Envelope answers:

> What outcome is desired, and what conditions must remain true while pursuing it?

---

# Required Properties

Every Intent Envelope SHALL contain:

* Objective
* Success Criteria
* Constraints
* Acceptance Criteria
* Principal
* Created Timestamp
* Modified Timestamp

An Intent Envelope MAY contain:

* Priority
* Assumptions
* Out of Scope
* Background Context
* Risk Tolerance
* Approval Requirements

---

# Ownership

The Principal owns the Intent Envelope.

The Orchestrator SHALL preserve it.

The Executor SHALL preserve it.

No Participant SHALL modify the Intent Envelope unless explicitly authorized by the Principal or by an applicable Protocol.

---

# Relationship to Goal

Every active Goal SHALL contain exactly one Intent Envelope.

A Goal manages lifecycle, coordination, Evidence, Decisions, and history.

The Intent Envelope preserves the Principal's intent.

---

# Relationship to Task

Tasks SHALL inherit the relevant portions of the parent Goal's Intent Envelope.

A Task SHALL NOT redefine the Intent Envelope.

A Task MAY narrow the applicable portion of the Intent Envelope for bounded execution, provided it does not contradict the parent Goal.

---

# Relationship to Evidence and Decision

Evidence evaluates whether work satisfies claims derived from the Intent Envelope.

Decisions may authorize state transitions based on Evidence relative to the Intent Envelope.

A Goal SHALL NOT be completed unless the Intent Envelope's Success Criteria and Acceptance Criteria have been evaluated.

---

# Mutability

The Intent Envelope SHOULD be stable after the Goal leaves Draft state.

After a Goal enters Ready state, changes to the Intent Envelope SHALL require explicit Principal authorization.

Changes SHOULD generate Events.

Material changes MAY require replanning.

---

# Inheritance

When a Task is created from a Goal, the Orchestrator SHALL include sufficient Intent Envelope context for the Executor to preserve the parent Goal's intent.

The inherited context SHOULD include:

* Relevant Objective
* Relevant Success Criteria
* Relevant Constraints
* Acceptance Criteria where applicable
* Out-of-scope boundaries where applicable

---

# Invariants

The following SHALL always remain true:

* Every active Goal has exactly one Intent Envelope.
* The Principal owns the Intent Envelope.
* Tasks inherit but do not redefine the Intent Envelope.
* Executors preserve but do not modify the Intent Envelope.
* Goal completion is evaluated against the Intent Envelope.

---

# Conformance

A conforming implementation SHALL:

* represent the Intent Envelope explicitly;
* preserve it through delegation;
* prevent unauthorized modification;
* include relevant inherited context in Tasks;
* evaluate completion against it.

---

# Normative Requirements

**MTH-011-REQ-001**

Every active Goal SHALL contain exactly one Intent Envelope.

**MTH-011-REQ-002**

The Principal SHALL own the Intent Envelope.

**MTH-011-REQ-003**

Participants SHALL NOT modify the Intent Envelope without Principal authorization.

**MTH-011-REQ-004**

Tasks SHALL inherit relevant Intent Envelope context from their parent Goal.

**MTH-011-REQ-005**

Executors SHALL preserve inherited Intent Envelope context during execution.

**MTH-011-REQ-006**

Goal completion SHALL be evaluated against the Intent Envelope.

---

# Anti-Patterns

The following behaviors are non-conforming or discouraged:

* Treating implementation plans as intent.
* Allowing Executors to reinterpret Success Criteria.
* Creating Tasks without inherited intent context.
* Modifying Constraints silently during execution.
* Completing Goals without evaluating the Intent Envelope.
* Storing intent only in conversational context.

---

# Design Rationale

Intent drift is one of the central risks in delegated work.

As Goals are decomposed into Tasks and Tasks are assigned to Executors, the system may optimize locally while drifting away from the Principal's actual desired outcome.

The Intent Envelope prevents this by making intent explicit, durable, owned, and protected.

---

# Revision History

| Version | Date          | Notes             |
| ------- | ------------- | ----------------- |
| 0.1.0   | Initial draft | First publication |
