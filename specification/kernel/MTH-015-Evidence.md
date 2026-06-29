# Méthodos Specification

**Identifier:** MTH-015

**Title:** Evidence

**Version:** 0.2.0

**Status:** Draft

**Category:** Kernel

**Depends Upon:** MTH-000 through MTH-014

---

# Abstract

This specification defines the Evidence Object.

Evidence is a structured, durable argument supporting one or more explicit Claims regarding canonical Objects within a Méthodos implementation.

Evidence is constructed from one or more Artifacts and provides the basis for review, acceptance, governance, and decision-making.

---

# Architectural Intent

Represent verifiable justification for Claims while separating observation from governance.

---

# Purpose

Evidence enables Participants to determine whether assertions regarding Goals, Tasks, Artifacts, or other canonical Objects are adequately supported by observable facts.

Evidence transforms execution outputs into reviewable, traceable justification.

---

# Definition

Evidence is a structured argument supported by one or more Artifacts.

Evidence is **not** an Artifact.

Evidence references Artifacts while expressing one or more Claims that those Artifacts support.

Evidence SHALL distinguish:

* observations;
* interpretations;
* conclusions.

---

# Required Properties

Every Evidence Object SHALL contain:

* Identifier
* Title
* Current State
* Creator
* Creation Timestamp
* Modified Timestamp
* One or more Claims
* Supporting Artifact References
* Related Object References
* Validation Method
* Confidence
* Summary

An Evidence Object MAY additionally contain:

* Confidence Basis
* Verification Method
* Reviewer
* Verified By
* Tags
* Implementation-specific metadata

---

# Claims

Every Evidence Object SHALL contain one or more explicit Claims.

Examples include:

* Success Criteria satisfied.
* Performance requirement achieved.
* Constraint preserved.
* Test suite passed.
* Failure reproduced.
* Requirement violated.

Claims SHALL be specific and independently reviewable.

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
* Reviews
* Approvals

Evidence SHALL reference at least one related canonical Object.

---

# Ownership

Evidence has exactly one Creator.

Accepted Evidence becomes part of the institutional Knowledge Repository.

Accepted Evidence SHALL NOT be modified.

Additional observations SHALL be represented by a new Evidence Object or by superseding Evidence.

---

# Lifecycle

An Evidence Object SHALL occupy exactly one of the following canonical States:

* Draft
* Assembled
* Reviewed
* Accepted
* Superseded
* Archived

---

# State Definitions

## Draft

Evidence is incomplete.

---

## Assembled

Supporting Artifacts have been collected and one or more Claims have been documented.

---

## Reviewed

Evidence has undergone independent review.

---

## Accepted

Evidence has been accepted for governance purposes.

---

## Superseded

A newer Evidence Object replaces this Evidence while preserving historical traceability.

---

## Archived

Evidence is retained for historical reference.

---

# Validation

Every Evidence Object SHALL identify the Validation Method used to evaluate its Claims.

Validation methods MAY include:

* automated testing;
* measurement;
* comparison;
* inspection;
* independent review;
* independent execution;
* external verification.

Implementations MAY define additional validation methods.

---

# Confidence

Every Evidence Object SHALL include a Confidence assessment.

Confidence represents the degree to which the stated Claims are substantiated by the available Evidence.

Confidence SHALL NOT represent subjective belief or statistical probability.

Canonical confidence levels are:

### Low

Preliminary supporting information exists.

### Moderate

Supporting Artifacts exist and internally substantiate the Claims.

### High

The Claims have undergone independent review.

### Verified

The Claims have been independently reproduced, measured, executed, or otherwise validated through an approved verification method.

Only independent review or independent verification MAY increase Confidence beyond Moderate.

---

# Traceability

Every Evidence Object SHALL be traceable to:

* supporting Artifacts;
* originating Tasks;
* related Goals;
* resulting Decisions.

Traceability SHALL remain preserved throughout the Evidence lifecycle.

---

# Immutability

Accepted Evidence SHALL be immutable.

Corrections or additional support SHALL be represented through new or superseding Evidence Objects.

Historical Evidence SHALL remain discoverable.

---

# Invariants

The following SHALL always remain true:

* Every Evidence Object has exactly one Identifier.
* Every Evidence Object contains one or more Claims.
* Every Evidence Object references one or more Artifacts.
* Every Evidence Object references at least one related canonical Object.
* Accepted Evidence remains immutable.
* Evidence remains independently reviewable.

---

# Conformance

A conforming implementation SHALL ensure that every Evidence Object:

* contains explicit Claims;
* references supporting Artifacts;
* identifies a Validation Method;
* records a Confidence assessment;
* preserves traceability;
* remains independently reviewable.

---

# Normative Requirements

**MTH-015-REQ-001**

Every Evidence Object SHALL contain one or more explicit Claims.

**MTH-015-REQ-002**

Evidence SHALL reference one or more supporting Artifacts.

**MTH-015-REQ-003**

Evidence SHALL identify a Validation Method.

**MTH-015-REQ-004**

Evidence SHALL reference at least one related canonical Object.

**MTH-015-REQ-005**

Every Evidence Object SHALL record a Confidence assessment.

**MTH-015-REQ-006**

Accepted Evidence SHALL be immutable.

**MTH-015-REQ-007**

Only independent review or independent verification MAY increase Confidence beyond Moderate.

---

# Anti-Patterns

The following behaviors are non-conforming or discouraged:

* Treating Artifacts as Evidence.
* Claims without supporting Artifacts.
* Confidence without documented validation.
* Assertions that cannot be independently reviewed.
* Editing Accepted Evidence.
* Using Confidence as a substitute for supporting Artifacts.

---

# Design Rationale

Méthodos deliberately separates:

* **Events** — what happened.
* **Artifacts** — what was produced.
* **Evidence** — what the Artifacts substantiate.
* **Decisions** — what is authorized based upon that Evidence.

This separation enables independent validation, transparent governance, reproducible reasoning, and long-term institutional learning.

Multiple Participants may construct independent Evidence from the same Artifacts while arriving at different conclusions. Such disagreement is resolved through review and governance rather than by modifying the underlying Artifacts.

---

# Future Directions

Future specifications may define:

* Evidence composition;
* Evidence packages;
* Automated verification;
* Cross-Goal Evidence reuse;
* Confidence calibration profiles.

---

# Revision History

| Version | Date           | Notes                                                                 |
| ------- | -------------- | --------------------------------------------------------------------- |
| 0.2.0   | First revision | Aligned with MTH-033 Evidence Protocol and canonical confidence model |
