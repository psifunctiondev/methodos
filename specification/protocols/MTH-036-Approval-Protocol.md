# Méthodos Specification

**Identifier:** MTH-036

**Title:** Approval Protocol

**Version:** 0.1.0

**Status:** Draft

**Category:** Protocols

**Depends Upon:** MTH-034 Decision Protocol

---

# Abstract

This specification defines the Approval Protocol.

The Approval Protocol governs how Participants express authorization for actions, state transitions, and Decisions.

Approvals provide explicit authorization.

Approvals SHALL NOT themselves constitute Decisions.

---

# Architectural Intent

Provide transparent, accountable authorization while separating governance from execution.

---

# Participants

| Participant  | Responsibility                          |
| ------------ | --------------------------------------- |
| Principal    | Approves when required                  |
| Orchestrator | Requests and records approvals          |
| Reviewer     | Provides delegated approval             |
| Executor     | Requests approval but does not grant it |

---

# Approval Characteristics

Approvals SHALL be:

* attributable;
* explicit;
* traceable;
* durable where governance requires.

Approvals represent authorization by a Participant.

Approvals SHALL NOT replace Evidence or Decisions.

---

# Approval Lifecycle

```text id="7ssjlwm"
Not Required
      │
      ▼
Requested
      │
      ▼
Pending
      │
      ├────────────► Rejected
      │
      ▼
Approved
      │
      ▼
Consumed
```

Once consumed, an Approval remains part of the historical record.

---

# Protocol

## Step 1 — Determine Requirement

The Orchestrator determines whether approval is required.

Approval MAY be required for:

* Goal completion;
* deployment;
* production changes;
* archival;
* security-sensitive operations;
* governance actions.

---

## Step 2 — Request Approval

The Orchestrator creates an approval request.

The request SHOULD identify:

* subject;
* supporting Evidence;
* proposed Decision;
* approving authority.

Publication SHOULD generate an Event.

---

## Step 3 — Review

The approving Participant reviews:

* Goal;
* Task;
* Artifacts;
* Evidence;
* proposed Decision.

Additional information MAY be requested.

---

## Step 4 — Response

The approving Participant SHALL respond with one of:

* Approved
* Rejected
* Deferred
* Needs More Evidence

The response SHALL be attributable.

---

## Step 5 — Record Approval

The approval response SHALL be preserved.

Approval MAY reference:

* Evidence;
* Decisions;
* Goals;
* Tasks.

---

## Step 6 — Final Decision

An Approval MAY permit a Decision to become Final.

Approval itself SHALL NOT change canonical state.

Only a Final Decision SHALL authorize state transitions.

---

# Delegation

Approval authority MAY be delegated.

Delegation SHOULD identify:

* delegating authority;
* delegate;
* scope;
* duration (if applicable).

Delegation SHALL remain traceable.

---

# Multiple Approvals

Implementations MAY require multiple approvals.

Examples include:

* Principal approval;
* Security review;
* Architecture review;
* Compliance approval.

The required approval policy is implementation-specific.

---

# Traceability

Approvals SHALL be traceable to:

* approving Participant;
* supporting Evidence;
* resulting Decision.

Historical Approvals SHALL remain discoverable.

---

# Failure Handling

Approval SHALL remain Pending when:

* required Evidence is incomplete;
* authority cannot be verified;
* additional review is requested.

Rejected approvals SHALL preserve rationale.

---

# Relationship to Other Objects

Approvals:

* authorize Decisions;
* reference Evidence;
* support governance.

Approvals SHALL NOT:

* replace Decisions;
* replace Evidence;
* modify Goals directly.

---

# Completion Conditions

An Approval is complete when:

* an authorized Participant responds;
* the response is recorded;
* traceability is preserved.

---

# Conformance

A conforming implementation SHALL:

* preserve approval history;
* identify approving authority;
* distinguish Approval from Decision;
* preserve traceability.

---

# Normative Requirements

**MTH-036-REQ-001**

Approvals SHALL be attributable.

**MTH-036-REQ-002**

Approvals SHALL identify approving authority.

**MTH-036-REQ-003**

Approvals SHALL NOT themselves authorize canonical state transitions.

**MTH-036-REQ-004**

Final Decisions MAY depend upon one or more Approvals.

**MTH-036-REQ-005**

Approval history SHALL be preserved.

---

# Design Rationale

Approvals represent participant authorization.

Decisions represent governance.

Separating these concepts allows Méthodos to support simple deployments where one Participant performs both roles, as well as complex governance workflows involving multiple independent approvers, while preserving accountability and auditability.

---

# Revision History

| Version | Date          | Notes             |
| ------- | ------------- | ----------------- |
| 0.1.0   | Initial draft | First publication |
