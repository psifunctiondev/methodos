# Méthodos Specification

**Identifier:** MTH-012

**Title:** Event Object

**Version:** 0.1.0

**Status:** Draft

**Category:** Kernel

**Depends Upon:** MTH-000 through MTH-011

---

# Abstract

This specification defines the Event Object.

An Event is an immutable record that describes something that has occurred within a Méthodos implementation.

Events provide an observable history of system activity and enable auditing, recovery, coordination, and institutional learning.

---

# Architectural Intent

Capture immutable facts about system activity.

---

# Purpose

Events record observable changes within the system.

Unlike transient communication between Participants, Events are durable records that become part of the institutional history of the system.

Events answer one question:

> **"What happened?"**

They do not explain why it happened or whether it was correct.

---

# Definition

An Event is an immutable Object describing an occurrence at a specific point in time.

Once created, an Event SHALL NOT be modified.

Corrections SHALL be represented by subsequent Events.

---

# Required Properties

Every Event SHALL contain:

* Identifier
* Event Type
* Timestamp
* Source Participant
* Related Object Identifier
* Related Object Type
* Summary
* Metadata

---

# Event Categories

Typical Event categories include:

* Goal
* Task
* Assignment
* State Transition
* Execution
* Artifact Creation
* Evidence Submission
* Decision
* Approval
* Error
* Warning
* Recovery

Implementations MAY define additional Event categories.

---

# Relationships

Events MAY reference:

* Goals
* Tasks
* Participants
* Artifacts
* Evidence
* Decisions
* Sessions

Events SHALL reference at least one Object.

---

# Ownership

Events have a Creator but not an Owner.

Once recorded, Events become part of the shared institutional history.

No Participant owns an Event after creation.

---

# Lifecycle

Events possess no operational lifecycle.

They transition directly from:

Created

↓

Recorded

Events SHALL NOT be edited.

Events SHALL NOT be deleted except through administrative retention policies outside the scope of this specification.

---

# Immutability

Immutability is a fundamental property of Events.

If additional information becomes available, a new Event SHALL be created.

Historical Events SHALL remain unchanged.

---

# Ordering

Events SHOULD preserve chronological ordering.

Implementations MAY use sequence identifiers where timestamps alone are insufficient.

Ordering SHALL remain deterministic within a single implementation.

---

# Relationships to Other Objects

Tasks generate Events.

Goal state transitions generate Events.

Artifact creation generates Events.

Evidence submission generates Events.

Decision approval generates Events.

Future specifications define these relationships in greater detail.

---

# Invariants

The following SHALL always remain true:

* Every Event has one Identifier.
* Every Event has one Timestamp.
* Every Event references at least one Object.
* Every Event is immutable.
* Every Event records an occurrence that has already happened.

---

# Conformance

An implementation conforms to this specification if every Event:

* is immutable,
* possesses the required properties,
* references at least one Object,
* records a timestamp,
* and remains durable after creation.

---

# Normative Requirements

**MTH-012-REQ-001**

Every Event SHALL have a stable Identifier.

**MTH-012-REQ-002**

Every Event SHALL contain a Timestamp.

**MTH-012-REQ-003**

Every Event SHALL reference at least one Object.

**MTH-012-REQ-004**

Events SHALL be immutable.

**MTH-012-REQ-005**

Implementations SHALL preserve Event history.

**MTH-012-REQ-006**

Corrections SHALL be represented by new Events rather than modification of existing Events.

---

# Anti-Patterns

The following behaviors are non-conforming or discouraged:

* Editing historical Events.
* Deleting Events during normal operation.
* Using Events as a communication queue.
* Storing implementation state exclusively within Events.
* Creating Events that cannot be associated with an Object.

---

# Design Rationale

Events provide the observable history of a Méthodos implementation.

Because Events are immutable, they enable reliable auditing, replay, debugging, recovery, and historical analysis.

Separating Events from transient communication ensures that durable institutional knowledge remains distinct from operational messaging.

---

# Future Directions

Future specifications will define:

* Event Protocol
* Event Taxonomy
* Event Correlation
* Event Streaming
* Event Retention Policies

---

# Revision History

| Version | Date          | Notes             |
| ------- | ------------- | ----------------- |
| 0.1.0   | Initial draft | First publication |
