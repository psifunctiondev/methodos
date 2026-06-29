# Méthodos Dossier System Definition

**Dossier Type:** Goal Dossier  
**Framework Version:** 0.1  
**Status:** Active

---

# Purpose

This dossier is the canonical institutional record for a single Méthodos Goal or closely related Goal set.

It contains durable Objects, operational history, Evidence, Decisions, and related knowledge required to understand and govern work.

Transient coordination belongs outside this dossier.

---

# Canonical Locations

```text
Inbox/
Templates/
Goals/
Tasks/
Events/
Artifacts/
Evidence/
Decisions/
Architecture/
Research/
Meetings/
Daily-Notes/
```

Objects SHOULD be stored in their canonical locations.

---

# Canonical Goal States

```text
Draft
Ready
Planning
Active
Blocked
Review
Complete
Archived
```

`Ready` is the explicit Principal-to-Orchestrator handoff.

A Goal SHALL NOT be planned merely because it exists.

---

# Canonical Task States

```text
Draft
Ready
Assigned
Executing
Waiting
Blocked
Ready for Review
Accepted
Cancelled
Archived
```

Queues, claims, leases, reservations, and heartbeats are coordination mechanics and SHALL NOT be treated as canonical Task States.

---

# Canonical Evidence States

```text
Draft
Assembled
Reviewed
Accepted
Superseded
Archived
```

Accepted Evidence is immutable.

Corrections require new or superseding Evidence.

---

# Ownership Domains

The Principal owns the Intent Envelope.

The Orchestrator owns planning, coordination, review preparation, and lifecycle management.

The Executor owns execution notes and produced Artifacts.

Participants SHALL NOT modify content outside their ownership domain except through authorized Protocols.

---

# Evidence and Decisions

Artifacts are not Evidence.

Evidence is not a Decision.

State transitions requiring governance SHALL be traceable to a Final Decision.

---

# Coordination

This dossier is not the Coordination Fabric.

Short-lived state, including leases, queues, claims, reservations, and heartbeats, belongs outside this dossier.

---

# Startup Rule

Participants SHOULD read this file before acting within the dossier.
