# Méthodos Specification

**Identifier:** MTH-035

**Title:** Event Protocol

**Version:** 0.1.0

**Status:** Draft

**Category:** Protocols

**Depends Upon:** MTH-012 Event

---

# Abstract

This specification defines the Event Protocol.

The Event Protocol governs the publication, propagation, consumption, and persistence of Events within a Méthodos deployment.

Events communicate that something has occurred.

Events SHALL NOT themselves alter canonical state.

---

# Architectural Intent

Provide a uniform mechanism for communicating significant occurrences among Participants while preserving a durable audit trail.

---

# Participants

| Participant          | Responsibility              |
| -------------------- | --------------------------- |
| Any Participant      | Publish Events              |
| Orchestrator         | Consume and react to Events |
| Knowledge Repository | Persist durable Events      |
| Coordination Fabric  | Distribute transient Events |

---

# Event Characteristics

Events SHALL be:

* immutable;
* timestamped;
* attributable;
* traceable;
* append-only.

Events describe facts.

Events SHALL NOT express intent or authorization.

---

# Event Classes

Implementations MAY define additional Event types.

Typical classes include:

* Goal Events
* Task Events
* Artifact Events
* Evidence Events
* Decision Events
* Participant Events
* System Events
* Error Events

---

# Event Lifecycle

```text id="6n1v0l"
Occurred
    │
    ▼
Published
    │
    ▼
Observed
    │
    ▼
Processed
    │
    ▼
Archived
```

Events SHALL remain immutable throughout their lifecycle.

---

# Protocol

## Step 1 — Occurrence

A Participant observes or causes a significant occurrence.

Examples:

* Task assigned
* Task blocked
* Artifact created
* Goal completed
* Worker started
* Review requested

---

## Step 2 — Publication

The Participant publishes an Event.

The Event SHOULD contain:

* Event ID
* Timestamp
* Publisher
* Event Type
* Related Objects
* Summary

Publication SHOULD occur promptly after the occurrence.

---

## Step 3 — Distribution

The Coordination Fabric MAY distribute Events to interested Participants.

Distribution MAY be transient.

Failure of distribution SHALL NOT invalidate the Event.

---

## Step 4 — Observation

Participants MAY subscribe to Events relevant to their responsibilities.

Examples:

OpenClaw observes:

* Task status changes
* Executor reports
* Blockers
* Decision requests

Hermes observes:

* newly assigned Tasks
* cancellations
* dependency resolution

---

## Step 5 — Processing

Participants MAY react to Events.

Examples:

* claim a Task
* update progress
* assemble Evidence
* initiate Recovery
* request Approval

Processing SHALL remain deterministic.

---

## Step 6 — Persistence

Events representing durable operational history SHOULD be stored within the Knowledge Repository.

Transient notification Events MAY expire after operational usefulness ends.

---

# Event Ordering

Implementations SHOULD preserve chronological ordering where practical.

Consumers SHALL NOT assume perfect global ordering across distributed systems.

Participants SHOULD rely upon object state rather than Event ordering when conflicts arise.

---

# Idempotency

Consumers SHOULD tolerate duplicate Events.

Processing the same Event more than once SHOULD NOT corrupt system state.

---

# Failure Handling

If Event publication fails:

* the originating operation MAY continue;
* publication SHOULD be retried;
* durable Events SHOULD eventually be preserved.

Loss of transient notification SHALL NOT invalidate canonical Objects.

---

# Relationship to Canonical Objects

Events SHALL NOT replace:

* Goals
* Tasks
* Artifacts
* Evidence
* Decisions

Events merely describe that something happened.

Canonical state SHALL remain within canonical Objects.

---

# Completion Conditions

An Event is complete when:

* published;
* assigned a unique identifier;
* attributed;
* timestamped;
* linked to relevant Objects.

No approval is required.

---

# Conformance

A conforming implementation SHALL:

* publish immutable Events;
* preserve attribution;
* preserve timestamps;
* support traceability;
* distinguish transient distribution from durable preservation.

---

# Normative Requirements

**MTH-035-REQ-001**

Events SHALL be immutable.

**MTH-035-REQ-002**

Events SHALL describe occurrences rather than intent.

**MTH-035-REQ-003**

Events SHALL NOT constitute Decisions.

**MTH-035-REQ-004**

Events SHALL NOT replace canonical Objects.

**MTH-035-REQ-005**

Durable Events SHALL remain attributable and traceable.

---

# Design Rationale

Events provide loose coupling among Participants.

Rather than polling for state changes, Participants observe Events and respond appropriately.

By separating Events from canonical Objects, Méthodos permits high-frequency operational coordination while preserving a durable, auditable history of significant occurrences.

---

# Revision History

| Version | Date          | Notes             |
| ------- | ------------- | ----------------- |
| 0.1.0   | Initial draft | First publication |
