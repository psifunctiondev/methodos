# Méthodos Specification

**Identifier:** MTH-038

**Title:** Discovery Protocol

**Version:** 0.1.0

**Status:** Draft

**Category:** Protocols

**Depends Upon:** MTH-023 Knowledge Repository, MTH-024 Coordination Fabric

---

# Abstract

This specification defines the Discovery Protocol.

The Discovery Protocol governs how Participants discover Goals, Tasks, Events, Artifacts, Evidence, Decisions, and other canonical Objects relevant to their responsibilities.

Discovery enables autonomous Participants to identify work, monitor progress, and maintain situational awareness without relying upon implementation-specific mechanisms.

---

# Architectural Intent

Provide deterministic, implementation-independent discovery of work and knowledge.

---

# Participants

| Participant          | Responsibility                              |
| -------------------- | ------------------------------------------- |
| Principal            | Discovers Goal progress                     |
| Orchestrator         | Discovers Goals, Tasks, and execution state |
| Executor             | Discovers assigned or available Tasks       |
| Reviewer             | Discovers pending reviews                   |
| Observer             | Discovers system state                      |
| Knowledge Repository | Provides canonical discovery                |
| Coordination Fabric  | Provides transient discovery hints          |

---

# Discovery Principles

Discovery SHALL be based upon canonical Objects.

Participants SHOULD discover only Objects relevant to their authority, responsibilities, and capabilities.

Discovery SHALL NOT modify canonical state.

---

# Discovery Sources

Participants MAY discover Objects from:

* Knowledge Repository;
* Coordination Fabric;
* implementation-specific indexes;
* local caches.

Where conflicts exist:

The Knowledge Repository SHALL be authoritative.

---

# Discovery Lifecycle

```text id="2rjlwm"
Need Identified
        │
        ▼
Discover
        │
        ▼
Filter
        │
        ▼
Prioritize
        │
        ▼
Select
        │
        ▼
Act
```

Discovery MAY occur repeatedly during execution.

---

# Protocol

## Step 1 — Identify Discovery Context

The Participant determines:

* role;
* capabilities;
* current assignments;
* current Goals;
* authority.

Discovery SHOULD be context-aware.

---

## Step 2 — Enumerate Candidate Objects

The Participant discovers candidate Objects.

Examples:

OpenClaw:

* Ready Goals
* Active Goals
* Blocked Goals
* Ready Tasks requiring assignment

Hermes:

* Assigned Tasks
* Ready Tasks matching capabilities
* Tasks awaiting clarification

Reviewer:

* Decisions awaiting review
* Evidence awaiting validation

---

## Step 3 — Filter

The Participant filters discovered Objects.

Typical filters include:

* ownership;
* state;
* capabilities;
* priority;
* dependencies.

Participants SHOULD ignore Objects outside their authority.

---

## Step 4 — Prioritize

The Participant prioritizes remaining Objects.

Implementations MAY consider:

* Goal priority;
* dependency ordering;
* deadlines;
* resource availability;
* implementation-specific policies.

Prioritization SHALL remain deterministic where practical.

---

## Step 5 — Select

The Participant selects one or more Objects for action.

Selection SHOULD avoid duplicate work.

The Coordination Fabric MAY assist through leases or reservations.

---

## Step 6 — Refresh

Participants SHOULD repeat discovery periodically or upon receiving relevant Events.

Discovery SHOULD be inexpensive and repeatable.

---

# Capability Matching

Executors SHOULD select only Tasks compatible with their declared capabilities.

Capability matching MAY consider:

* required tools;
* required models;
* required permissions;
* implementation-specific constraints.

---

# Goal Discovery

Orchestrators SHOULD discover:

* newly Ready Goals;
* blocked Goals;
* Goals requiring review;
* Goals awaiting completion.

Goal discovery SHOULD initiate the Goal Protocol.

---

# Task Discovery

Executors SHOULD discover:

* assigned Tasks;
* executable Tasks;
* blocked Tasks requiring recovery.

Task discovery SHOULD initiate the Task Protocol.

---

# Coordination Fabric Integration

The Coordination Fabric MAY advertise discovery hints.

Examples:

* newly available Tasks;
* expired leases;
* worker availability.

Discovery SHALL NOT depend exclusively upon transient coordination.

Participants SHALL be capable of reconstructing discovery from canonical state.

---

# Failure Handling

If discovery fails:

Participants SHOULD:

* retry;
* consult the Knowledge Repository;
* ignore stale operational hints;
* report failures through Events.

Discovery failure SHALL NOT corrupt canonical Objects.

---

# Completion Conditions

Discovery completes when:

* candidate Objects have been identified;
* filtering has completed;
* prioritization has completed;
* one or more Objects have been selected or no eligible Objects remain.

---

# Conformance

A conforming implementation SHALL:

* discover canonical Objects;
* respect authority;
* preserve deterministic selection;
* tolerate stale transient coordination;
* remain independent of implementation-specific mechanisms.

---

# Normative Requirements

**MTH-038-REQ-001**

Discovery SHALL identify canonical Objects relevant to the Participant.

**MTH-038-REQ-002**

Participants SHALL respect authority and Ownership Domains during discovery.

**MTH-038-REQ-003**

The Knowledge Repository SHALL be the authoritative discovery source.

**MTH-038-REQ-004**

The Coordination Fabric MAY provide discovery hints but SHALL NOT be authoritative.

**MTH-038-REQ-005**

Participants SHALL be capable of reconstructing discovery from canonical Objects.

---

# Design Rationale

Autonomous Participants must continuously determine what work requires attention.

By separating canonical discovery from transient operational coordination, Méthodos allows implementations to optimize responsiveness while preserving correctness.

Participants remain capable of discovering work even after infrastructure failures or process restarts.

---

# Revision History

| Version | Date          | Notes             |
| ------- | ------------- | ----------------- |
| 0.1.0   | Initial draft | First publication |
