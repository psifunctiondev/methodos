# Méthodos Specification

**Identifier:** MTH-023

**Title:** Knowledge Repository Role

**Version:** 0.1.0

**Status:** Draft

**Category:** Roles

**Depends Upon:** MTH-000 through MTH-022

---

# Abstract

This specification defines the Knowledge Repository Role.

The Knowledge Repository is the authoritative, durable store of institutional knowledge within a Méthodos deployment.

It preserves the Objects that describe goals, execution, governance, and historical reasoning independently of any individual Participant.

---

# Architectural Intent

Preserve institutional knowledge across time, Participants, and implementations.

---

# Purpose

The Knowledge Repository exists to ensure that knowledge survives:

* individual Participants;
* execution sessions;
* infrastructure failures;
* implementation changes;
* personnel changes.

It provides a shared, durable understanding of the system's history and current state.

---

# Role Definition

A Knowledge Repository is a service responsible for storing and preserving canonical Méthodos Objects.

The repository SHALL act as the authoritative source of institutional knowledge.

Participants SHALL treat the repository as canonical unless an explicit protocol specifies otherwise.

---

# Responsibilities

The Knowledge Repository SHALL:

* preserve canonical Objects;
* maintain object relationships;
* preserve historical state;
* support traceability;
* support discoverability;
* preserve governance records;
* retain historical context;
* support human and autonomous Participants.

---

# Canonical Objects

The following Objects SHALL be considered canonical when stored within the repository:

* Goal
* Task
* Event
* Artifact (or stable reference)
* Evidence
* Decision

Implementations MAY preserve additional Objects.

---

# Durability

Knowledge stored within the repository SHALL be durable.

Knowledge SHALL survive:

* Participant termination;
* process restart;
* infrastructure replacement;
* implementation upgrades.

---

# Traceability

The repository SHALL preserve relationships among Objects.

Implementations SHOULD permit traversal such as:

```text
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

Historical relationships SHALL remain recoverable.

---

# Ownership Domains

The repository SHALL preserve Ownership Domains defined by canonical Objects.

Participants SHALL NOT modify content outside their ownership domains except through authorized Protocols.

---

# Discoverability

Participants SHOULD be able to discover:

* active Goals;
* related Tasks;
* supporting Evidence;
* governing Decisions;
* associated Artifacts;
* historical Events.

Knowledge SHOULD remain navigable by both humans and autonomous Participants.

---

# Version History

Implementations SHOULD preserve historical revisions.

Historical versions SHOULD remain recoverable.

Deletion SHOULD be exceptional rather than routine.

---

# Non-Responsibilities

The Knowledge Repository SHALL NOT:

* coordinate execution;
* maintain distributed locks;
* schedule work;
* manage leases;
* provide transient messaging;
* perform inference routing.

Those responsibilities belong to other Roles.

---

# Separation from the Coordination Fabric

The Knowledge Repository preserves durable knowledge.

The Coordination Fabric manages transient operational state.

The two Roles SHALL remain logically distinct even if implemented by the same technology.

---

# Dossiers

A Knowledge Repository MAY organize work into Dossiers.

A Dossier is a collection of related Objects supporting a single Goal or closely related set of Goals.

A repository MAY contain many Dossiers.

Participants SHOULD treat each Dossier as an independent body of institutional knowledge.

---

# Conformance

A conforming Knowledge Repository:

* preserves canonical Objects;
* maintains traceability;
* preserves history;
* supports discoverability;
* respects Ownership Domains;
* remains independent of execution infrastructure.

---

# Normative Requirements

**MTH-023-REQ-001**

The Knowledge Repository SHALL be the authoritative source of institutional knowledge.

**MTH-023-REQ-002**

Canonical Objects SHALL be durable.

**MTH-023-REQ-003**

Participants SHALL treat repository contents as authoritative unless an applicable Protocol specifies otherwise.

**MTH-023-REQ-004**

The repository SHALL preserve traceability among canonical Objects.

**MTH-023-REQ-005**

The repository SHALL preserve Ownership Domains.

**MTH-023-REQ-006**

The repository SHALL remain logically separate from the Coordination Fabric.

---

# Design Rationale

Institutional knowledge is one of the central concepts of Méthodos.

By separating durable knowledge from transient execution state, Participants may coordinate through fast operational infrastructure while preserving an auditable, human-readable history of goals, execution, evidence, and decisions.

This separation enables implementations to evolve independently while maintaining continuity of knowledge.

---

# Reference Implementation Notes

Obsidian is the initial reference implementation of the Knowledge Repository Role.

Other implementations may use databases, document stores, version-controlled repositories, enterprise knowledge systems, or future technologies, provided they satisfy the normative requirements of this specification.

---

# Future Directions

Future specifications may define:

* Repository synchronization
* Distributed repositories
* Cross-repository references
* Repository federation
* Repository discovery
* Repository migration

---

# Revision History

| Version | Date          | Notes             |
| ------- | ------------- | ----------------- |
| 0.1.0   | Initial draft | First publication |
