# Méthodos Specification

**Identifier:** MTH-024

**Title:** Coordination Fabric Role

**Version:** 0.1.0

**Status:** Draft

**Category:** Roles

**Depends Upon:** MTH-000 through MTH-023

---

# Abstract

This specification defines the Coordination Fabric Role.

The Coordination Fabric provides transient coordination among Participants.

It enables distributed execution while remaining independent of durable institutional knowledge.

---

# Architectural Intent

Coordinate work without becoming the system of record.

---

# Purpose

The Coordination Fabric exists to support the operational collaboration of Participants.

It provides low-latency communication, task coordination, leases, notifications, and other transient operational state required during execution.

---

# Role Definition

A Coordination Fabric is a shared service responsible for transient operational coordination.

Participants exchange operational state through the Coordination Fabric.

The Coordination Fabric SHALL NOT be treated as the authoritative source of institutional knowledge.

---

# Responsibilities

The Coordination Fabric SHALL:

* advertise executable work;
* coordinate task ownership;
* maintain transient leases;
* support distributed execution;
* publish operational notifications;
* expose worker liveness;
* facilitate recovery from transient failures.

---

# Operational State

Examples of operational state include:

* task queues;
* execution leases;
* worker heartbeats;
* notifications;
* transient locks;
* scheduling hints;
* retry requests.

Operational state is expected to change frequently.

---

# Durability

Operational state MAY be durable for fault tolerance.

Operational durability SHALL NOT imply institutional authority.

If conflicts arise, the Knowledge Repository SHALL be considered authoritative.

---

# Non-Responsibilities

The Coordination Fabric SHALL NOT:

* preserve Goals;
* preserve Decisions;
* preserve Evidence;
* preserve historical Events;
* replace the Knowledge Repository;
* route inference requests.

---

# Failure Recovery

The Coordination Fabric SHOULD support:

* lease expiration;
* worker recovery;
* duplicate detection;
* retry coordination;
* transient fault recovery.

Recovery SHALL preserve consistency with the Knowledge Repository.

---

# Separation from the Knowledge Repository

The Coordination Fabric manages execution.

The Knowledge Repository preserves history.

These responsibilities SHALL remain logically distinct.

---

# Conformance

A conforming Coordination Fabric:

* coordinates Participants;
* manages transient operational state;
* supports distributed execution;
* remains independent of institutional knowledge.

---

# Lease Semantics

A Coordination Fabric MAY implement Task assignment using renewable leases.

A lease:

* grants exclusive execution authority to one Participant;
* has a finite lifetime;
* MAY be renewed through periodic heartbeats;
* expires automatically if renewal ceases.

Upon lease expiration the Coordination Fabric SHALL release exclusive ownership.

If the associated Task has not transitioned to a terminal state, it SHALL become eligible for reassignment according to implementation policy.

Lease duration, heartbeat cadence, expiration timeout, and reassignment strategy are implementation-specific.

Reference implementations MAY define recommended defaults.

---

# Normative Requirements

**MTH-024-REQ-001**

The Coordination Fabric SHALL coordinate Participants through transient operational state.

**MTH-024-REQ-002**

The Coordination Fabric SHALL NOT become the authoritative source of institutional knowledge.

**MTH-024-REQ-003**

Participants SHALL reconcile operational state with the Knowledge Repository.

**MTH-024-REQ-004**

If a Coordination Fabric implements Task leasing, lease expiration SHALL release exclusive ownership of the Task and SHALL permit reassignment in accordance with the Task Protocol.

---

# Design Rationale

Separating operational coordination from institutional knowledge permits the Coordination Fabric to prioritize performance, responsiveness, and recovery while preserving an auditable history elsewhere.

---

# Reference Implementation Notes

Redis is the initial reference implementation of the Coordination Fabric Role.

Other messaging systems, distributed queues, event buses, or coordination services MAY satisfy this Role provided they conform to the normative requirements.

---

# Revision History

| Version | Date          | Notes             |
| ------- | ------------- | ----------------- |
| 0.1.0   | Initial draft | First publication |
