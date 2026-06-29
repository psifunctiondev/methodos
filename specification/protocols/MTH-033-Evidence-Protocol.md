# Méthodos Specification

**Identifier:** MTH-033

**Title:** Evidence Protocol

**Version:** 0.2.0

**Status:** Draft

**Category:** Protocols

**Depends Upon:** MTH-014 Artifact, MTH-015 Evidence, MTH-016 Decision, MTH-032 Artifact Protocol

---

# Abstract

This specification defines the Evidence Protocol.

The Evidence Protocol governs the construction, validation, review, acceptance, supersession, and archival of Evidence within a Méthodos implementation.

Evidence transforms observable Artifacts into structured, reviewable arguments supporting explicit Claims.

Evidence SHALL inform governance but SHALL NOT itself authorize state transitions.

---

# Architectural Intent

Provide a deterministic process for constructing and evaluating Evidence while separating execution, review, and governance.

---

# Participants

| Participant  | Responsibility                                 |
| ------------ | ---------------------------------------------- |
| Executor     | Produces Artifacts supporting potential Claims |
| Orchestrator | Assembles Evidence and coordinates review      |
| Reviewer     | Independently evaluates Evidence               |
| Principal    | Reviews Evidence when governance requires      |

---

# Evidence Principles

Evidence SHALL:

* support one or more explicit Claims;
* reference supporting Artifacts;
* distinguish observations from conclusions;
* preserve traceability;
* remain independently reviewable.

Evidence is a structured argument.

Evidence is not merely documentation.

---

# Confidence Model

Confidence expresses the degree to which the stated Claims are substantiated by available Evidence.

Confidence SHALL NOT represent subjective belief or statistical probability.

The canonical confidence levels are:

| Level    | Meaning                                                                                              |
| -------- | ---------------------------------------------------------------------------------------------------- |
| Low      | Preliminary supporting information exists.                                                           |
| Moderate | Supporting Artifacts substantiate the Claims but independent review has not occurred.                |
| High     | Independent review has concluded that the Claims are adequately supported.                           |
| Verified | Independent reproduction, measurement, execution, or approved verification has confirmed the Claims. |

Only independent review or independent verification MAY increase Confidence beyond Moderate.

---

# Evidence Lifecycle

Evidence SHALL occupy exactly one canonical State:

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
  ├────────────► Superseded
  │                   │
  │                   ▼
  └────────────── Archived
```

Accepted Evidence SHALL remain immutable.

---

# Protocol

## Step 1 — Identify Claims

The Orchestrator identifies one or more explicit Claims requiring support.

Claims SHOULD be:

* observable;
* testable;
* independently reviewable.

Claims SHALL distinguish facts from conclusions.

---

## Step 2 — Gather Supporting Artifacts

Relevant Artifacts SHALL be identified.

Supporting Artifacts SHOULD be:

* attributable;
* durable;
* traceable;
* accessible.

Evidence lacking supporting Artifacts SHALL remain incomplete.

---

## Step 3 — Assemble Evidence

The Orchestrator constructs an Evidence Object containing:

* Claims;
* supporting Artifacts;
* related Objects;
* validation method;
* initial Confidence assessment.

State:

```text
Draft → Assembled
```

---

## Step 4 — Validation

The stated Claims SHALL be evaluated using one or more documented validation methods.

Validation methods MAY include:

* automated testing;
* measurement;
* inspection;
* comparison;
* human review;
* external verification.

The validation method SHALL be recorded.

Validation demonstrates whether the available Artifacts substantiate the stated Claims.

---

## Step 5 — Independent Review

A Reviewer independently evaluates:

* the Claims;
* supporting Artifacts;
* reasoning;
* validation method;
* assigned Confidence.

The Reviewer MAY:

* accept the Evidence;
* request additional Evidence;
* request clarification;
* reject the Evidence.

State:

```text
Assembled → Reviewed
```

Only independent review MAY raise Confidence to High.

---

## Step 6 — Acceptance

Evidence SHALL transition to Accepted only when:

* Claims are adequately substantiated;
* supporting Artifacts exist;
* validation is documented;
* review is complete;
* Confidence has been recorded.

Accepted Evidence becomes part of the institutional Knowledge Repository.

Accepted Evidence SHALL be immutable.

---

## Step 7 — Verification

Where required, an independent verification process MAY be performed.

Verification MAY include:

* independent execution;
* independent measurement;
* independent reproduction;
* formal proof;
* cryptographic verification.

Only successful independent verification MAY assign Confidence:

```text
Verified
```

Verification SHALL identify the verification method and verifying Participant.

---

## Step 8 — Supersession

When newer or more complete Evidence replaces existing Evidence:

```text
Accepted → Superseded
```

The superseding Evidence SHALL reference the superseded Evidence.

Historical traceability SHALL remain preserved.

---

## Step 9 — Archival

Superseded or obsolete Evidence MAY transition to Archived.

Archival SHALL preserve:

* Claims;
* supporting Artifacts;
* Confidence history;
* related Decisions;
* complete traceability.

---

# Validation Principles

Evidence SHALL distinguish:

* observations;
* interpretations;
* conclusions.

Observations SHALL be directly supported by Artifacts.

Interpretations SHALL identify the reasoning connecting observations to Claims.

Conclusions SHALL remain independently reviewable.

---

# Traceability

Every Evidence Object SHALL remain traceable to:

* supporting Artifacts;
* originating Tasks;
* related Goals;
* resulting Decisions.

Complete historical reconstruction SHOULD be possible.

---

# Failure Handling

Evidence SHALL remain incomplete when:

* supporting Artifacts are unavailable;
* Claims cannot be validated;
* validation is undocumented;
* Confidence cannot be justified.

Incomplete Evidence SHALL NOT support acceptance or completion Decisions.

---

# Relationship to Other Objects

Artifacts provide observations.

Evidence constructs arguments.

Decisions authorize state transitions.

Evidence SHALL NOT:

* replace Artifacts;
* redefine Goals;
* authorize completion;
* substitute for Decisions.

---

# Completion Conditions

Evidence SHALL be considered complete when:

* one or more explicit Claims exist;
* supporting Artifacts are referenced;
* validation is documented;
* Confidence is recorded;
* traceability is preserved;
* review is complete.

---

# Conformance

A conforming implementation SHALL:

* identify explicit Claims;
* reference supporting Artifacts;
* document validation methods;
* record Confidence;
* preserve traceability;
* distinguish validation from verification;
* preserve Accepted Evidence as immutable.

---

# Normative Requirements

**MTH-033-REQ-001**

Evidence SHALL support one or more explicit Claims.

**MTH-033-REQ-002**

Evidence SHALL reference supporting Artifacts.

**MTH-033-REQ-003**

Evidence SHALL identify its validation method.

**MTH-033-REQ-004**

Evidence SHALL record a Confidence assessment.

**MTH-033-REQ-005**

Only independent review or independent verification MAY increase Confidence beyond Moderate.

**MTH-033-REQ-006**

Accepted Evidence SHALL be immutable.

**MTH-033-REQ-007**

Evidence SHALL NOT authorize state transitions.

---

# Design Rationale

The Evidence Protocol separates execution from governance.

Executors produce Artifacts.

Orchestrators assemble Evidence.

Reviewers evaluate the resulting argument.

Decisions act upon that evaluated Evidence.

This separation enables independent validation, reproducible reasoning, transparent governance, and long-term institutional learning while preserving a clear distinction between observations, arguments, and authorized outcomes.

---

# Revision History

| Version | Date           | Notes                                                                             |
| ------- | -------------- | --------------------------------------------------------------------------------- |
| 0.2.0   | First revision | Aligned with canonical Evidence model, confidence semantics, and governance chain |
