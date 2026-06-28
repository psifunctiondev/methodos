# Méthodos Specification

**Identifier:** MTH-034

**Title:** Decision Protocol

**Version:** 0.1.0

**Status:** Draft

**Category:** Protocols

**Depends Upon:** MTH-015 Decision, MTH-033 Evidence Protocol, MTH-035 Event Protocol

---

# Abstract

This specification defines the Decision Protocol.

The Decision Protocol governs the creation, review, authorization, publication, supersession, and preservation of Decisions within a Méthodos deployment.

Decisions establish authoritative outcomes.

Decisions SHALL be supported by Evidence.

---

# Architectural Intent

Provide explicit, auditable governance for state transitions and significant conclusions.

---

# Participants

| Participant          | Responsibility                         |
| -------------------- | -------------------------------------- |
| Orchestrator         | Proposes Decisions                     |
| Reviewer             | Reviews Decisions when required        |
| Principal            | Makes or delegates governing Decisions |
| Knowledge Repository | Preserves Decisions                    |

---

# Decision Characteristics

Decisions SHALL be:

* attributable;
* traceable;
* reviewable;
* durable;
* immutable after finalization.

Decisions authorize outcomes.

Decisions SHALL NOT replace Evidence.

---

# Decision Lifecycle

```text id="jj0ty8"
Draft
    │
    ▼
Proposed
    │
    ▼
Final
    │
    ▼
Superseded
    │
    ▼
Archived
```

A Final Decision SHALL NOT be modified.

Changes SHALL be represented by a new Decision.

---

# Protocol

## Step 1 — Identify the Question

A Decision SHALL answer a specific governance question.

Examples:

* Is the Goal complete?
* Is the Task accepted?
* Should execution continue?
* Should deployment proceed?
* Should the Goal be archived?

Questions SHOULD be explicit.

---

## Step 2 — Assemble Supporting Evidence

Before proposing a Decision, the responsible Participant SHALL identify supporting Evidence.

The Decision SHALL reference one or more Evidence objects.

If sufficient Evidence does not exist, the Decision SHOULD remain in Draft or Proposed.

---

## Step 3 — Proposal

A Decision is created.

State:

```text id="vqum4u"
Proposed
```

The Decision SHALL include:

* outcome;
* rationale;
* authority;
* supporting Evidence.

---

## Step 4 — Review

Where required by governance policy, a Reviewer or Principal evaluates the proposed Decision.

Review MAY:

* approve;
* reject;
* defer;
* request additional Evidence.

---

## Step 5 — Finalization

When approved, the Decision becomes:

```text id="ddoqu5"
Final
```

A Final Decision becomes authoritative.

Publication SHOULD generate an Event.

---

## Step 6 — State Transition

Canonical Objects MAY transition state only after an applicable Final Decision exists.

Examples:

* Task → Accepted
* Goal → Complete
* Goal → Archived

---

## Step 7 — Supersession

If circumstances change, a new Decision MAY supersede an existing Final Decision.

The original Decision SHALL remain preserved.

The superseding relationship SHALL be recorded.

---

# Authority

Every Decision SHALL identify:

* decision maker;
* authority;
* delegation (if applicable).

Implementations SHOULD make authority explicit.

---

# Traceability

Every Decision SHALL be traceable to:

* supporting Evidence;
* related Tasks;
* related Goals;
* resulting state transitions.

Historical Decisions SHALL remain discoverable.

---

# Immutability

Final Decisions SHALL NOT be modified.

Corrections SHALL be represented through superseding Decisions.

Historical Decisions SHALL remain available for audit.

---

# Failure Handling

A Decision SHALL NOT become Final when:

* required Evidence is missing;
* authority is absent;
* governance requirements are unmet.

Such Decisions SHOULD remain Proposed.

---

# Relationship to Other Objects

Decisions:

* reference Evidence;
* authorize state transitions;
* govern canonical Objects.

Decisions SHALL NOT:

* replace Evidence;
* replace Goals;
* replace Tasks;
* replace Artifacts.

---

# Completion Conditions

A Decision SHALL be considered complete when:

* finalized by authorized authority;
* supported by Evidence;
* attributable;
* traceable;
* published.

---

# Conformance

A conforming implementation SHALL:

* require Evidence;
* preserve traceability;
* preserve Decision history;
* prevent modification of Final Decisions;
* support supersession.

---

# Normative Requirements

**MTH-034-REQ-001**

Every Final Decision SHALL reference supporting Evidence.

**MTH-034-REQ-002**

Final Decisions SHALL be immutable.

**MTH-034-REQ-003**

Canonical state transitions SHALL require an applicable Final Decision.

**MTH-034-REQ-004**

Superseding Decisions SHALL preserve historical traceability.

**MTH-034-REQ-005**

Every Decision SHALL identify its governing authority.

---

# Design Rationale

Governance requires explicit authorization.

By separating Decisions from Evidence, Méthodos distinguishes between **what is believed** and **what is authorized**.

This separation enables transparent governance while preserving historical accountability.

---

# Revision History

| Version | Date          | Notes             |
| ------- | ------------- | ----------------- |
| 0.1.0   | Initial draft | First publication |
