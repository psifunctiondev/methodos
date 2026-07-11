# Méthodos Specification

**Identifier:** MTH-011

**Title:** Intent Envelope

**Version:** 0.2.0

**Status:** Draft

**Category:** Kernel

**Depends Upon:** MTH-000 through MTH-010

---

# Abstract

This specification defines the Intent Envelope.

The Intent Envelope is the canonical representation of the Principal's intent for a Goal. It is the portion of a Goal that must be preserved through planning, delegation, execution, review, and archival.

The Intent Envelope exists to prevent intent drift while permitting the Orchestrator and Executors to choose implementation strategies.

---

# Architectural Intent

Preserve the Principal's intended outcome across delegation and execution while separating required intent from non-binding implementation guidance.

---

# Purpose

The Intent Envelope provides a stable, explicit representation of:

* the outcome the Principal wants to achieve;
* the observable conditions that define success;
* the conditions that must remain true;
* the validation conditions required for acceptance;
* material propositions currently assumed to be true;
* explicit boundaries on scope;
* optional implementation guidance;
* Goal-specific definitions required for consistent interpretation.

It separates intent from implementation.

Participants may plan, decompose, execute, retry, and review work in many different ways, but they SHALL preserve the Intent Envelope unless explicitly authorized to change it.

---

# Definition

An Intent Envelope is a Kernel Object contained by a Goal.

It defines the Principal-owned semantic core of that Goal.

The Intent Envelope answers:

> What outcome is desired, what conditions define success and acceptance, and what semantic boundaries must be preserved while pursuing it?

---

# Canonical Properties

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
* Suggested Approaches
* Domain Definitions
* Background Context
* Risk Tolerance
* Approval Requirements

---

# Property Semantics

## Objective

The Objective defines the desired end state.

It answers:

> What should become true?

The Objective SHOULD describe the outcome rather than the execution plan.

The Objective SHOULD NOT prescribe Task decomposition, sequencing, tools, providers, or implementation mechanics unless the prescribed method is itself part of the Principal's intent or a Constraint.

---

## Success Criteria

Success Criteria define observable conditions indicating that the Goal has succeeded.

They answer:

> What conditions mean the desired outcome has been achieved?

Success Criteria SHOULD be specific enough to evaluate.

A Success Criterion SHOULD describe an outcome or resulting condition rather than merely state that an activity occurred.

---

## Constraints

Constraints define conditions that SHALL remain true during execution or in the resulting state.

They answer:

> What boundaries may planning and execution not violate?

Constraints MAY govern:

* permitted or prohibited methods;
* storage or output requirements;
* security conditions;
* resource limits;
* compatibility requirements;
* legal or policy boundaries;
* required formats or naming conventions.

A mandatory implementation method SHALL be expressed as a Constraint rather than a Suggested Approach.

---

## Acceptance Criteria

Acceptance Criteria define observable validation conditions required for closure.

They answer:

> What must be demonstrated before the Principal may accept completion?

Acceptance Criteria SHOULD be written so that Evidence Claims and validation activities can be derived from them.

Acceptance Criteria SHOULD identify observable or inspectable conditions wherever practical.

Acceptance Criteria do not replace Success Criteria. Success Criteria define success; Acceptance Criteria define the validation threshold for accepting that success.

---

## Assumptions

Assumptions are propositions treated as true for planning or execution but not guaranteed by the Intent Envelope.

Material Assumptions SHOULD be explicit.

The Orchestrator SHALL evaluate material Assumptions during Planning and SHALL record any Assumption whose failure would block, materially alter, or invalidate the execution plan.

An invalid material Assumption SHALL trigger replanning, clarification, or a Blocked condition as appropriate.

---

## Out of Scope

Out of Scope defines explicit boundaries around work that the Goal does not authorize or require.

Out-of-scope boundaries SHALL be preserved during Task decomposition.

---

## Suggested Approaches

Suggested Approaches are non-binding implementation guidance supplied by the Principal.

They preserve useful prior experience, preferences, remembered workflows, and possible execution strategies without converting them into Constraints.

The Orchestrator MAY use, modify, combine, or reject a Suggested Approach.

Suggested Approaches SHOULD NOT use `MUST`, `SHALL`, `REQUIRED`, or equivalent normative language to express non-binding guidance.

If the Principal requires a particular method or condition, that requirement SHALL be represented as a Constraint or another applicable normative field.

---

## Domain Definitions

Domain Definitions establish Goal-specific terms, taxonomies, classification rules, identifiers, thresholds, or semantic distinctions required to interpret the Goal consistently.

Domain Definitions MAY include:

* category definitions;
* naming codes;
* qualification rules;
* domain-specific meanings;
* classification boundaries.

Participants SHALL preserve applicable Domain Definitions when planning Tasks, executing work, constructing Evidence, and performing review.

Domain Definitions SHALL NOT silently introduce requirements that contradict the Objective, Success Criteria, Constraints, or Acceptance Criteria.

---

# Ownership

The Principal owns the Intent Envelope.

The Orchestrator SHALL preserve it.

The Executor SHALL preserve inherited Intent Envelope context.

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

Inherited context SHOULD include applicable Domain Definitions and Constraints.

---

# Relationship to Evidence and Decision

Evidence evaluates Claims derived from Success Criteria, Acceptance Criteria, Constraints, and other validation-relevant Intent Envelope properties.

Acceptance Criteria SHOULD seed Evidence planning.

The Orchestrator SHOULD identify required Evidence Claims and validation activities during Planning rather than reconstructing them only after execution.

Decisions may authorize state transitions based on Evidence relative to the Intent Envelope.

A Goal SHALL NOT be completed unless its Success Criteria and Acceptance Criteria have been evaluated.

---

# Canonical Serialization and Dossier Projection

The canonical serialized Goal Object MAY represent the Intent Envelope as a structured nested object.

A Dossier MAY project the same semantic content into human- and agent-readable Markdown sections.

The Dossier projection is not required to mirror the canonical JSON property layout one-to-one.

A conforming projection SHALL preserve the semantics and cardinality required by the canonical Object model.

Schemas validate canonical serialized Objects unless a schema explicitly states that it validates a Dossier projection or front matter.

---

# Mutability

The Intent Envelope SHOULD be stable after the Goal leaves Draft State.

After a Goal enters Ready State, changes to the Intent Envelope SHALL require explicit Principal authorization.

Changes SHOULD generate Events.

Material changes MAY require replanning.

---

# Inheritance

When a Task is created from a Goal, the Orchestrator SHALL include sufficient Intent Envelope context for the Executor to preserve the parent Goal's intent.

The inherited context SHOULD include:

* relevant Objective;
* relevant Success Criteria;
* relevant Constraints;
* applicable Acceptance Criteria;
* material Assumptions;
* applicable Out-of-Scope boundaries;
* applicable Domain Definitions;
* relevant Suggested Approaches, when useful and clearly identified as non-binding.

---

# Invariants

The following SHALL always remain true:

* Every active Goal has exactly one Intent Envelope.
* The Principal owns the Intent Envelope.
* Tasks inherit but do not redefine the Intent Envelope.
* Executors preserve but do not modify inherited Intent Envelope context.
* Constraints remain distinguishable from Suggested Approaches.
* Goal completion is evaluated against the Intent Envelope.

---

# Conformance

A conforming implementation SHALL:

* represent the Intent Envelope explicitly;
* preserve it through delegation;
* prevent unauthorized modification;
* distinguish mandatory Constraints from non-binding Suggested Approaches;
* include relevant inherited context in Tasks;
* evaluate material Assumptions during Planning;
* evaluate completion against Success Criteria and Acceptance Criteria;
* preserve semantic equivalence between canonical serialization and Dossier projections.

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

**MTH-011-REQ-007**

Suggested Approaches SHALL remain non-binding unless the same requirement is separately represented as a Constraint or other normative requirement.

**MTH-011-REQ-008**

The Orchestrator SHALL evaluate material Assumptions during Planning.

**MTH-011-REQ-009**

Acceptance Criteria SHOULD support the derivation of Evidence Claims and validation activities.

**MTH-011-REQ-010**

Dossier projections of an Intent Envelope SHALL preserve the semantics required by the canonical Object model.

---

# Anti-Patterns

The following behaviors are non-conforming or discouraged:

* Treating implementation plans as the Objective.
* Hiding mandatory requirements inside Suggested Approaches.
* Using normative language to imply that non-binding guidance is mandatory.
* Allowing Executors to reinterpret Success Criteria.
* Creating Tasks without inherited intent context.
* Modifying Constraints silently during execution.
* Ignoring material Assumptions during Planning.
* Inventing Evidence expectations only after execution is complete.
* Completing Goals without evaluating the Intent Envelope.
* Storing intent only in conversational context.
* Treating a Markdown projection and canonical JSON serialization as semantically unrelated records.

---

# Design Rationale

Intent drift is one of the central risks in delegated work.

As Goals are decomposed into Tasks and Tasks are assigned to Executors, the system may optimize locally while drifting away from the Principal's actual desired outcome.

At the same time, Principals often possess useful implementation knowledge that should be preserved without unnecessarily constraining the Orchestrator.

The Intent Envelope prevents drift by making intent explicit, durable, owned, and protected while distinguishing required boundaries from non-binding guidance.

Evidence-oriented Acceptance Criteria and explicit material Assumptions allow planning and review to occur against the same semantic contract.

---

# Revision History

| Version | Date | Notes |
|---|---|---|
| 0.1.0 | Initial draft | First publication |
| 0.2.0 | 2026-07-11 | Defined canonical field semantics, Suggested Approaches, Domain Definitions, assumption validation, Evidence planning, and serialization/projection distinction |
