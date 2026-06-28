# Méthodos Reference Implementation

**Identifier:** RI-003

**Title:** Redis Coordination Fabric Reference Implementation

**Version:** 0.1.0

**Status:** Draft

**Implements:** Coordination Fabric

**Depends Upon:** MTH-000 through MTH-022

---

# Abstract

This document defines Redis as the reference implementation of the Méthodos Coordination Fabric.

Redis provides fast, transient coordination between Participants.

Redis is not the authoritative repository for institutional knowledge.

---

# Architectural Intent

Coordinate Participants through transient shared state.

---

# Purpose

Redis exists to:

* advertise available work;
* coordinate Task ownership;
* provide short-lived leases;
* distribute event notifications;
* publish heartbeats;
* enable low-latency collaboration.

Redis does not preserve institutional memory.

---

# Responsibilities

Redis SHALL:

* advertise executable Tasks;
* coordinate Task claiming;
* maintain execution leases;
* publish coordination Events;
* expose worker heartbeats;
* facilitate distributed execution.

---

# Non-Responsibilities

Redis SHALL NOT:

* be the authoritative source for Goals;
* permanently store Tasks;
* store canonical Events;
* store Evidence;
* store Decisions;
* preserve institutional Knowledge.

---

# Recommended Key Structure

```text
queue:tasks:ready

task:{task_id}

lease:{task_id}

worker:{worker_id}:heartbeat

event:stream

notification:{participant_id}

locks:{resource}
```

Implementations MAY extend this structure.

---

# Coordination Patterns

## Task Queue

OpenClaw publishes executable Tasks.

Hermes consumes available Tasks.

---

## Task Lease

Hermes creates a lease before execution.

Leases SHALL expire automatically.

Expired leases MAY return Tasks to the ready queue.

---

# Reference Lease Defaults

The reference Redis implementation SHOULD use the following defaults unless overridden by local deployment policy:

- Task lease duration: 15 minutes
- Heartbeat interval: 60 seconds
- Missed heartbeat threshold: 3
- Requeue condition: lease expired or three consecutive missed heartbeats
- Lease renewal: permitted while the Executor is actively progressing

Executors SHOULD renew leases before expiration.

Orchestrators SHOULD requeue Tasks only after reconciling against the Knowledge Repository to confirm that the Task has not already reached a terminal state.

---

## Heartbeats

Workers SHOULD publish heartbeats periodically.

Missing heartbeats MAY indicate worker failure.

---

## Event Notifications

Redis MAY publish Event notifications.

The notification SHALL reference the canonical Event stored in the Knowledge Repository.

---

# Failure Recovery

Redis SHOULD permit:

* lease expiration
* task requeueing
* worker recovery
* duplicate detection

Implementations SHOULD prefer idempotent operations.

---

# Conformance

A conforming Redis implementation:

* coordinates work,
* maintains leases,
* supports heartbeats,
* enables recovery,
* avoids becoming institutional storage.

---

# Design Rationale

Redis excels at transient coordination.

Institutional knowledge belongs elsewhere.

This separation permits Redis to remain small, fast, and disposable.

---

# Revision History

| Version | Date          | Notes             |
| ------- | ------------- | ----------------- |
| 0.1.0   | Initial draft | First publication |
