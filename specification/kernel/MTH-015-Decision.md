# Méthodos Specification

**Identifier:** MTH-015

**Title:** Decision Object

**Version:** 0.1.0

**Status:** Draft

**Category:** Kernel

**Depends Upon:** MTH-000 through MTH-014

---

# Abstract

This specification defines the Decision Object.

A Decision is a durable authorization that changes the state of one or more Objects within a Méthodos implementation.

Decisions provide accountable governance over state transitions.

---

# Architectural Intent

Authorize state transitions through explicit, reviewable judgment.

---

# Purpose

Execution produces work.

Evidence supports claims.

Decisions determine whether those claims are sufficient to authorize change.

A Decision answers the question:

> **"Given the available Evidence, what should change?"**

---

# Definition

A Decision is a durable Object representing an explicit judgment regarding one or more related Objects.

A Decision SHALL reference the Evidence upon which it is based.

---

# Required Properties

Every Decision SHALL contain:

* Identifier
* Decision Type
* Decision Maker
* Creation Timestamp
* Related Object Identifier
* Evidence References
* Decision Outcome
* Rationale
* Metadata

---

# Decision Types

Typical Decision types include:

* Accept
* Reject
* Approve
* Escalate
* Cancel
* Retry
* Archive
* Defer

Implementations MAY define additional Decision types.

---

# Outcomes

Typical Decision outcomes include:

* Goal Accepted
* Task Complete
* Task Rejected
* Additional Work Required
* Human Approval Required
* Retry Authorized
* Goal Archived

---

# Relationships

A Decision SHALL reference:

* one or more Evidence Objects
* one or more related Objects

A Decision MAY reference:

* Goals
* Tasks
* Participants
* Artifacts
* Events
* Sessions

---

# Ownership

A Decision has a Decision Maker.

Decision authority is determined by the applicable Role and Protocol.

Decisions become part of the institutional Knowledge Repository.

---

# Lifecycle

A Decision SHALL occupy one of the following States:

* Draft
* Proposed
* Final
* Superseded
* Archived

Once Final, a Decision SHALL NOT be modified.

Subsequent changes SHALL be represented by new Decisions.

---

# Authority

Only authorized Participants MAY issue Decisions affecting an Object.

Authority SHALL be determined by applicable Role specifications and governance Protocols.

This specification intentionally does not define authorization policy.

---

# State Transitions

A Decision MAY authorize state transitions.

State transitions SHALL reference the Decision that authorized them.

State transitions without an associated Decision are non-conforming unless explicitly permitted by another specification.

---

# Invariants

The following SHALL always remain true:

* Every Decision has one Identifier.
* Every Decision references Evidence.
* Every Decision references at least one related Object.
* Every Final Decision is immutable.
* Every authorized state transition references its governing Decision.

---

# Conformance

An implementation conforms to this specification if every Decision:

* references supporting Evidence,
* identifies a Decision Maker,
* records an explicit Outcome,
* and authorizes any resulting state transition.

---

# Normative Requirements

**MTH-015-REQ-001**

Every Decision SHALL reference one or more Evidence Objects.

**MTH-015-REQ-002**

Every Decision SHALL identify its Decision Maker.

**MTH-015-REQ-003**

Every Decision SHALL record an explicit Outcome.

**MTH-015-REQ-004**

Final Decisions SHALL be immutable.

**MTH-015-REQ-005**

Authorized state transitions SHALL reference the Decision that permitted them.

**MTH-015-REQ-006**

Decisions SHALL remain independently reviewable.

---

# Anti-Patterns

The following behaviors are non-conforming or discouraged:

* Completing work without an associated Decision.
* Decisions lacking supporting Evidence.
* Editing Final Decisions.
* State transitions with no accountable Decision Maker.
* Decisions based solely on assertion.

---

# Design Rationale

Méthodos separates execution from governance.

Executors perform work.

Evidence supports claims.

Decision Makers determine whether those claims justify changing the system.

This separation preserves accountability, enables independent review, and prevents Participants from unilaterally authorizing their own success.

---

# Future Directions

Future specifications will define:

* Decision Protocol
* Approval Workflow
* Decision Authorities
* Governance Policies
* Multi-party Decisions

---

# Revision History

| Version | Date          | Notes             |
| ------- | ------------- | ----------------- |
| 0.1.0   | Initial draft | First publication |
