# Méthodos Specification

**Identifier:** MTH-039

**Title:** Observability Protocol

**Version:** 0.1.0

**Status:** Draft

**Category:** Protocols

**Depends Upon:** MTH-030 through MTH-038

---

# Abstract

This specification defines the Observability Protocol.

The Observability Protocol governs how Participants, operators, and external systems observe the state, health, and progress of a Méthodos deployment.

Observability enables understanding.

Observability SHALL NOT modify canonical state.

---

# Architectural Intent

Provide sufficient visibility to explain the current state, historical evolution, and operational health of a Méthodos deployment.

---

# Participants

| Participant          | Responsibility                          |
| -------------------- | --------------------------------------- |
| Principal            | Observes Goal progress                  |
| Orchestrator         | Publishes operational status            |
| Executor             | Publishes execution status              |
| Observer             | Consumes observability information      |
| Knowledge Repository | Provides historical observability       |
| Coordination Fabric  | Provides live operational observability |

---

# Observability Principles

Observability SHALL answer:

* What is happening?
* Why is it happening?
* What has happened?
* What should happen next?

Observability SHALL preserve traceability.

Observability SHALL NOT alter system behavior.

---

# Observable Domains

A conforming implementation SHOULD expose observability for:

* Goals;
* Tasks;
* Events;
* Artifacts;
* Evidence;
* Decisions;
* Participants;
* Infrastructure Roles.

---

# Protocol

## Step 1 — Publish Status

Participants SHOULD publish their operational status.

Examples:

* idle
* planning
* executing
* blocked
* recovering
* reviewing

Status publication SHOULD generate Events where appropriate.

---

## Step 2 — Observe

Observers discover:

* active Goals;
* active Tasks;
* blocked work;
* participant health;
* infrastructure health;
* pending approvals.

Observation SHALL remain read-only.

---

## Step 3 — Correlate

Observability SHOULD permit correlation among:

* Goals;
* Tasks;
* Artifacts;
* Evidence;
* Decisions;
* Events.

Implementations SHOULD support end-to-end traceability.

---

## Step 4 — Diagnose

Participants SHOULD be able to determine:

* why work is blocked;
* why a Decision was made;
* why a Goal is incomplete;
* why recovery occurred.

Diagnosis SHOULD rely upon canonical Objects.

---

## Step 5 — Report

Implementations MAY produce:

* dashboards;
* summaries;
* health reports;
* progress reports;
* audit reports.

Reports SHALL be derived from canonical Objects whenever practical.

---

# Operational Metrics

Implementations MAY expose metrics including:

* active Goals;
* completed Goals;
* Task throughput;
* Task latency;
* recovery count;
* blocked Tasks;
* Decision rate;
* approval latency;
* participant availability.

Metrics SHALL remain implementation-specific.

---

# Traceability

Observability SHALL support traversal across canonical Objects.

Typical navigation:

```text id="nh8opb"
Goal
    ↓
Task
    ↓
Artifact
    ↓
Evidence
    ↓
Decision
```

Historical traceability SHOULD remain available.

---

# Health

Participants SHOULD expose operational health.

Examples:

* available;
* degraded;
* unavailable.

Infrastructure Roles SHOULD expose health independently of Participant health.

---

# Failure Handling

Loss of observability SHALL NOT affect canonical state.

Observability failures SHOULD generate Events.

Historical observability SHOULD remain recoverable after infrastructure restoration.

---

# Completion Conditions

Observability is considered sufficient when Participants can determine:

* current operational state;
* historical state;
* governing Decisions;
* supporting Evidence;
* outstanding work;
* system health.

---

# Conformance

A conforming implementation SHALL:

* preserve traceability;
* expose operational state;
* distinguish historical and live state;
* avoid modifying canonical Objects during observation.

---

# Normative Requirements

**MTH-039-REQ-001**

Observability SHALL be read-only.

**MTH-039-REQ-002**

Observability SHALL preserve traceability.

**MTH-039-REQ-003**

Historical state SHALL remain observable.

**MTH-039-REQ-004**

Observability SHALL distinguish canonical state from transient operational state.

**MTH-039-REQ-005**

Observability failures SHALL NOT alter canonical Objects.

---

# Design Rationale

Autonomous systems require more than execution—they require explainability.

The Observability Protocol enables Participants and operators to understand not only the current state of the system, but also the reasoning, evidence, and governance that produced that state.

By treating observability as an architectural concern rather than an implementation feature, Méthodos enables interchangeable dashboards, monitoring systems, and operational tooling without changing the underlying behavioral contracts.

---

# Revision History

| Version | Date          | Notes             |
| ------- | ------------- | ----------------- |
| 0.1.0   | Initial draft | First publication |
