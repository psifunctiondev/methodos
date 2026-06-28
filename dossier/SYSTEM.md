# Méthodos Vault System Definition

**Vault:** Méthodos Canonical Knowledge Repository

**Framework Version:** 0.1

**Status:** Active

---

# Purpose

This vault is the canonical Knowledge Repository for a Méthodos deployment.

It contains the durable Objects, architecture, specifications, and operational history required for collaborative goal-directed work.

Participants SHALL treat this vault as the authoritative source of institutional knowledge.

Transient operational coordination occurs outside this vault.

---

# Operating Principles

This vault implements the Méthodos framework.

Participants SHALL operate in accordance with the applicable MTH specifications.

When specification documents conflict with local content, the specification SHALL take precedence unless an explicit local governance policy states otherwise.

---

# Canonical Knowledge

The following Objects are canonical when represented in this vault:

* Goals
* Tasks
* Events
* Artifacts (or stable references)
* Evidence
* Decisions

Participants SHALL preserve the integrity of these Objects.

---

# Repository Layout

```
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
Daily Notes/
```

Participants SHOULD store Objects only in their canonical locations.

---

# Object Creation

New Objects SHALL be created from the corresponding template within:

```
Templates/
```

Participants SHOULD NOT invent alternative object formats.

---

# Ownership Domains

Durable Objects define ownership domains.

Participants SHALL respect ownership boundaries.

In particular:

* The Principal owns Goal intent.
* The Orchestrator owns coordination.
* The Executor owns execution records.
* Governance Objects become immutable when finalized.

Participants SHALL NOT modify content outside their ownership domain except through an authorized Protocol.

---

# Goal Lifecycle

Goals normally progress through:

```
Draft
↓
Ready
↓
Planning
↓
Active
↓
Review
↓
Complete
↓
Archived
```

Participants SHALL respect Goal state transitions defined by the applicable protocols.

---

# Coordination

This vault is **not** the Coordination Fabric.

Short-lived operational state, leases, queues, and heartbeats belong outside this repository.

Participants SHALL NOT treat transient coordination state as institutional knowledge.

---

# Knowledge Preservation

Knowledge stored within this vault is expected to outlive any individual Participant.

Participants SHOULD preserve:

* traceability;
* rationale;
* supporting evidence;
* historical decisions;
* reusable knowledge.

Deletion SHOULD be avoided unless governed by an explicit retention policy.

---

# Evidence and Decisions

Artifacts are not Evidence.

Evidence is not a Decision.

Participants SHALL preserve the following chain:

```
Task
    ↓
Artifact
    ↓
Evidence
    ↓
Decision
```

State transitions SHOULD be traceable to a governing Decision.

---

# Version Control

This repository SHOULD remain under version control.

History SHOULD be preserved.

Meaningful changes SHOULD remain reviewable.

---

# Participant Startup Sequence

Before performing work, Participants SHOULD:

1. Read this document.
2. Determine the supported Méthodos version.
3. Review applicable specifications.
4. Discover active Goals.
5. Discover assigned Tasks.
6. Synchronize operational state.
7. Begin work.

---

# Local Deployment

This vault intentionally avoids implementation-specific assumptions.

Coordination, inference routing, authentication, storage backends, and deployment topology are defined by the corresponding Reference Implementations.

---

# Design Philosophy

Méthodos is founded on three principles:

* Preserve intent.
* Produce evidence.
* Maintain institutional knowledge.

Every durable Object within this vault exists to support one or more of these principles.
