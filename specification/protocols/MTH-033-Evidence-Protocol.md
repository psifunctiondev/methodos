# Méthodos Specification

**Identifier:** MTH-033

**Title:** Evidence Protocol

**Version:** 0.1.0

**Status:** Draft

**Category:** Protocols

**Depends Upon:** MTH-014 Evidence, MTH-032 Artifact Protocol, MTH-035 Event Protocol

---

# Abstract

This specification defines the Evidence Protocol.

The Evidence Protocol governs the construction, validation, review, and preservation of Evidence supporting claims within a Méthodos deployment.

Evidence connects observable Artifacts to explicit Claims through reproducible reasoning.

Evidence SHALL NOT itself authorize state changes.

---

# Architectural Intent

Provide a transparent, reviewable justification for conclusions while separating observation from governance.

---

# Participants

| Participant  | Responsibility                    |
| ------------ | --------------------------------- |
| Orchestrator | Assembles Evidence                |
| Executor     | Produces supporting Artifacts     |
| Reviewer     | Validates Evidence                |
| Principal    | Reviews Evidence when appropriate |

---

# Evidence Characteristics

Evidence SHALL be:

* attributable;
* traceable;
* reproducible where practical;
* reviewable;
* linked to supporting Artifacts.

Evidence represents an argument.

Evidence SHALL distinguish facts from conclusions.

---

# Confidence Model

Confidence represents the degree to which a Claim is substantiated by available Evidence.

Confidence SHALL NOT represent a subjective belief or statistical probability.

The canonical confidence levels are:

Low
    Preliminary evidence exists.

Moderate
    Evidence is internally consistent and references supporting Artifacts.

High
    Evidence has undergone independent review.

Verified
    The Claim has been independently reproduced, measured, or validated according to an approved verification method.

Implementations MAY define additional metadata describing the verification method but SHALL preserve the canonical confidence ordering.

Only independent review or independent verification MAY increase confidence beyond Moderate.

---

# Evidence Lifecycle

```text
Draft
    │
    ▼
Assembled
    │
    ▼
Reviewed
    │
    ▼
Accepted
    │
    ▼
Archived
```

Evidence SHALL remain immutable after acceptance except through supersession.

---

# Protocol

## Step 1 — Identify the Claim

Evidence SHALL support one or more explicit Claims.

Examples:

* Task Success Criteria satisfied.
* Performance requirement achieved.
* Security requirement met.
* Constraint preserved.

Claims SHOULD be specific and testable.

---

## Step 2 — Gather Supporting Artifacts

The Orchestrator identifies relevant Artifacts.

Supporting Artifacts SHOULD be:

* durable;
* attributable;
* traceable;
* accessible.

Missing Artifacts SHALL be identified.

---

## Step 3 — Validate

The Orchestrator or Reviewer evaluates whether the Artifacts support the stated Claim.

Validation methods MAY include:

* automated testing;
* inspection;
* comparison;
* measurement;
* human review;
* external verification.

The validation method SHALL be recorded.

---

## Step 4 — Assess Confidence

Evidence SHALL state a confidence level.

Suggested levels:

* Low
* Moderate
* High
* Verified

Confidence SHALL include justification.

---

## Step 5 — Publish

Accepted Evidence becomes a durable Object.

Publication SHOULD generate an Event.

---

## Step 6 — Reference

Decisions MAY reference Evidence.

Tasks and Goals MAY reference Evidence.

Evidence MAY reference additional Evidence.

Circular references SHOULD be avoided.

---

# Validation Principles

Evidence SHALL distinguish:

* observations;
* interpretations;
* conclusions.

Observations SHOULD be directly supported by Artifacts.

Conclusions SHOULD identify the reasoning connecting observations to Claims.

---

# Traceability

Evidence SHALL be traceable to:

* supporting Artifacts;
* originating Tasks;
* related Goals;
* resulting Decisions.

Complete traceability SHOULD be possible.

---

# Failure Handling

Evidence SHALL remain incomplete when:

* required Artifacts are unavailable;
* validation cannot be reproduced;
* confidence cannot be justified.

Incomplete Evidence SHALL NOT justify Decisions.

---

# Relationship to Other Objects

Evidence references Artifacts.

Evidence supports Decisions.

Evidence SHALL NOT:

* replace Artifacts;
* authorize completion;
* redefine Goals.

---

# Completion Conditions

Evidence SHALL be considered complete when:

* one or more explicit Claims are identified;
* supporting Artifacts are referenced;
* validation is documented;
* confidence is assessed;
* traceability is preserved.

---

# Conformance

A conforming implementation SHALL:

* identify explicit Claims;
* reference supporting Artifacts;
* preserve traceability;
* distinguish observation from conclusion;
* record confidence.

---

# Normative Requirements

**MTH-033-REQ-001**

Evidence SHALL support explicit Claims.

**MTH-033-REQ-002**

Evidence SHALL reference supporting Artifacts.

**MTH-033-REQ-003**

Evidence SHALL identify its validation method.

**MTH-033-REQ-004**

Evidence SHALL record confidence.

**MTH-033-REQ-005**

Evidence SHALL NOT authorize state transitions.

---

# Design Rationale

Evidence is the bridge between execution and governance.

Rather than relying upon assertions that work has been completed, Méthodos requires explicit reasoning linking observable Artifacts to verifiable Claims.

This separation allows multiple independent reviewers to evaluate the same Artifacts while preserving transparency and reproducibility.

---

# Revision History

| Version | Date          | Notes             |
| ------- | ------------- | ----------------- |
| 0.1.0   | Initial draft | First publication |
