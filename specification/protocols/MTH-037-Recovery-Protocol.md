# Méthodos Specification

**Identifier:** MTH-037

**Title:** Recovery Protocol

**Version:** 0.1.0

**Status:** Draft

**Category:** Protocols

**Depends Upon:** MTH-030 through MTH-036

---

# Abstract

This specification defines the Recovery Protocol.

The Recovery Protocol governs how Participants recover from interruptions, failures, inconsistencies, and loss of transient operational state.

Recovery SHALL preserve canonical state and SHALL NOT compromise Goal intent.

---

# Architectural Intent

Enable safe continuation of work following failures while preserving correctness, traceability, and governance.

---

# Participants

| Participant          | Responsibility                        |
| -------------------- | ------------------------------------- |
| Orchestrator         | Coordinates recovery                  |
| Executor             | Recovers execution state              |
| Coordination Fabric  | Re-establishes transient coordination |
| Knowledge Repository | Provides canonical state              |

---

# Recovery Principles

Recovery SHALL be based upon canonical Objects rather than transient operational state.

Participants SHALL assume that transient state may be incomplete, duplicated, delayed, or lost.

The Knowledge Repository SHALL remain authoritative.

---

# Recovery Triggers

Recovery MAY be initiated by:

* process restart;
* Participant failure;
* infrastructure outage;
* lease expiration;
* network partition;
* duplicate execution;
* inconsistent operational state;
* explicit operator request.

---

# Recovery Lifecycle

```text id="cjlwmc"
Failure Detected
        │
        ▼
Assessment
        │
        ▼
Reconciliation
        │
        ▼
Recovery Plan
        │
        ▼
Resume
        │
        ▼
Verification
```

Recovery SHALL preserve historical traceability.

---

# Protocol

## Step 1 — Detect Failure

A Participant detects an interruption or inconsistency.

Detection SHOULD generate an Event.

---

## Step 2 — Assess

The recovering Participant SHALL determine:

* current Goal state;
* current Task states;
* assigned ownership;
* available Artifacts;
* available Evidence;
* outstanding Decisions.

Transient coordination data SHALL be treated as advisory.

---

## Step 3 — Reconcile

The Participant SHALL reconcile transient operational state against canonical repository state.

Where conflicts exist:

The Knowledge Repository SHALL take precedence.

---

## Step 4 — Build Recovery Plan

The Orchestrator determines how work should continue.

Recovery actions MAY include:

* reclaim Task;
* reassign Task;
* restart execution;
* continue execution;
* request clarification;
* abandon incomplete work.

---

## Step 5 — Resume

Execution resumes only after reconciliation is complete.

Participants SHALL avoid duplicating completed work where practical.

---

## Step 6 — Verify

The recovering Participant SHALL verify:

* consistency;
* ownership;
* traceability;
* expected state.

Recovery completion SHOULD generate an Event.

---

# Duplicate Execution

Implementations SHOULD tolerate duplicate execution.

Participants SHOULD determine completion by inspecting canonical Objects rather than assuming work has not already been performed.

Idempotent execution is RECOMMENDED.

---

# Partial Completion

Recovery SHALL preserve partially completed work.

Existing:

* Artifacts;
* Events;
* Evidence;
* Decisions

SHALL be reused where appropriate.

Participants SHOULD avoid recreating durable Objects unnecessarily.

---

# Coordination Fabric Failure

Loss of the Coordination Fabric SHALL NOT result in loss of institutional knowledge.

Participants SHOULD reconstruct operational coordination from canonical repository contents.

---

# Knowledge Repository Failure

If the Knowledge Repository is unavailable:

* Participants SHOULD avoid irreversible state transitions.
* Recovery SHALL resume after repository availability is restored.

Canonical state SHALL NOT be reconstructed solely from transient coordination state.

---

# Failure Handling

Recovery itself MAY fail.

Repeated failures SHOULD be escalated.

Blocked Goals or Tasks MAY remain blocked until human intervention occurs.

---

# Completion Conditions

Recovery is complete when:

* canonical state has been reconciled;
* ownership is established;
* execution may safely continue;
* consistency has been verified.

---

# Conformance

A conforming implementation SHALL:

* recover from transient failures;
* reconcile against canonical state;
* preserve traceability;
* avoid unauthorized state transitions.

---

# Normative Requirements

**MTH-037-REQ-001**

Recovery SHALL treat the Knowledge Repository as authoritative.

**MTH-037-REQ-002**

Transient operational state SHALL NOT override canonical Objects.

**MTH-037-REQ-003**

Recovery SHALL preserve traceability.

**MTH-037-REQ-004**

Participants SHOULD reuse existing durable Objects whenever practical.

**MTH-037-REQ-005**

Recovery completion SHOULD generate an Event.

---

# Design Rationale

Distributed systems experience failures.

Rather than attempting to preserve every aspect of transient operational state, Méthodos treats durable knowledge as the foundation from which execution can always be reconstructed.

This approach permits implementations to recover predictably while preserving accountability and institutional knowledge.

---

# Revision History

| Version | Date          | Notes             |
| ------- | ------------- | ----------------- |
| 0.1.0   | Initial draft | First publication |
