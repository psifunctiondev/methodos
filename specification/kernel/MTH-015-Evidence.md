# Méthodos Specification

**Identifier:** MTH-014

**Title:** Evidence Object

**Version:** 0.1.0

**Status:** Draft

**Category:** Kernel

**Depends Upon:** MTH-000 through MTH-013

---

# Abstract

This specification defines the Evidence Object.

Evidence is a structured, durable argument supporting a claim regarding one or more Objects within a Méthodos implementation.

Evidence is constructed from one or more Artifacts and provides the basis for validation, acceptance, and decision-making.

---

# Architectural Intent

Provide verifiable justification for claims.

---

# Purpose

Evidence enables Participants to determine whether assertions regarding Goals, Tasks, Artifacts, or Decisions are supported by observable facts.

Evidence transforms execution outputs into trustworthy conclusions.

---

# Definition

Evidence is a structured argument supported by one or more Artifacts.

Evidence is not itself an Artifact.

Evidence references Artifacts while expressing one or more claims that those Artifacts support.

---

# Required Properties

Every Evidence Object SHALL contain:

* Identifier
* Claim
* Supporting Artifact References
* Related Object Identifier
* Creator
* Creation Timestamp
* Confidence
* Validation Method
* Summary

---

# Claims

Every Evidence Object SHALL make one or more explicit claims.

Examples include:

* Success Criteria satisfied.
* Test suite passed.
* Performance target achieved.
* Constraint preserved.
* Failure reproduced.
* Requirement violated.

Claims SHALL be observable.

Claims SHOULD be independently reviewable.

---

# Supporting Artifacts

Every Evidence Object SHALL reference one or more Artifacts.

Evidence without supporting Artifacts is non-conforming.

Multiple Evidence Objects MAY reference the same Artifact.

---

# Relationships

Evidence MAY support:

* Goals
* Tasks
* Decisions
* Approvals
* Reviews

Evidence SHALL reference at least one related Object.

---

# Ownership

Evidence has a Creator.

Evidence becomes part of the institutional Knowledge Repository.

Subsequent Participants MAY reference existing Evidence but SHALL NOT modify it.

If additional support becomes available, a new Evidence Object SHALL be created.

---

# Lifecycle

Evidence SHALL occupy one of the following States:

* Draft
* Submitted
* Accepted
* Superseded
* Archived

Evidence SHALL remain durable.

---

# Validation

Evidence SHALL describe how the supporting claim was evaluated.

Validation methods MAY include:

* automated testing
* human review
* measurement
* comparison
* inspection
* external verification

Implementations MAY define additional validation methods.

---

# Confidence

Evidence SHOULD include an assessment of confidence.

Typical values MAY include:

* Low
* Moderate
* High
* Verified

The confidence assessment SHALL NOT replace supporting Artifacts.

---

# Invariants

The following SHALL always remain true:

* Every Evidence Object has one Identifier.
* Every Evidence Object makes at least one Claim.
* Every Evidence Object references one or more Artifacts.
* Every Evidence Object references at least one related Object.
* Evidence SHALL remain independently reviewable.

---

# Conformance

An implementation conforms to this specification if every Evidence Object:

* contains explicit Claims,
* references supporting Artifacts,
* identifies a validation method,
* and remains independently reviewable.

---

# Normative Requirements

**MTH-014-REQ-001**

Every Evidence Object SHALL contain at least one explicit Claim.

**MTH-014-REQ-002**

Evidence SHALL reference one or more supporting Artifacts.

**MTH-014-REQ-003**

Evidence SHALL identify a validation method.

**MTH-014-REQ-004**

Evidence SHALL reference at least one related Object.

**MTH-014-REQ-005**

Evidence SHALL remain durable.

**MTH-014-REQ-006**

Evidence SHALL NOT be modified after acceptance.

Additional supporting information SHALL be represented by a new Evidence Object.

---

# Anti-Patterns

The following behaviors are non-conforming or discouraged:

* Treating Artifacts as Evidence.
* Claims without supporting Artifacts.
* Confidence without validation.
* Assertions that cannot be independently reviewed.
* Editing accepted Evidence.

---

# Design Rationale

Méthodos distinguishes between:

Events
→ what happened.

Artifacts
→ what was produced.

Evidence
→ what can be concluded.

This separation enables independent validation, review, auditing, and long-term institutional learning.

Participants are free to produce different Artifacts while still constructing equivalent Evidence.

---

# Future Directions

Future specifications will define:

* Evidence Protocol
* Evidence Templates
* Review Workflow
* Evidence Correlation
* Acceptance Process

---

# Revision History

| Version | Date          | Notes             |
| ------- | ------------- | ----------------- |
| 0.1.0   | Initial draft | First publication |
