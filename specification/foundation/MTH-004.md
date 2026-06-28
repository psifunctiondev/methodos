# Méthodos Specification

**Identifier:** MTH-004

**Title:** Object Model

**Version:** 0.1.0

**Status:** Draft

**Category:** Foundational

**Depends Upon:** MTH-000, MTH-001, MTH-002, MTH-003

---

# Abstract

This document defines the fundamental Objects that comprise the Méthodos domain model.

All Participants, Protocols, and Implementations SHALL operate upon these Objects.

Future specifications MAY extend this model but SHALL NOT contradict it.

---

# Purpose

The Object Model establishes a common vocabulary for the entities manipulated by conforming implementations.

Every Object possesses identity, ownership, state, relationships, and lifecycle.

---

# Universal Object Properties

Every Méthodos Object SHALL possess:

* Identifier
* Object Type
* Owner
* Current State
* Creation Timestamp
* Modification Timestamp
* Relationships
* Metadata

Implementations MAY add additional attributes.

---

# Core Objects

## Goal

Represents a desired outcome established by a Principal.

Goals authorize Tasks.

Goals define intent.

---

## Task

Represents a bounded unit of work.

Tasks pursue exactly one Goal.

Tasks produce Evidence.

---

## Participant

Represents an entity capable of fulfilling one or more Roles.

Participants MAY be human or computational.

---

## Role

Represents a contractual definition of responsibility.

Participants perform Roles.

Implementations realize Roles.

---

## Capability

Represents an ability available to a Participant.

Capabilities are reusable.

Capabilities are not work.

---

## Artifact

Represents a durable product of execution.

Artifacts preserve institutional knowledge.

Artifacts MAY become Evidence.

---

## Evidence

Represents information supporting assertions regarding execution.

Evidence SHALL reference one or more Artifacts.

---

## Decision

Represents an explicit choice affecting future execution.

Decisions SHALL be durable.

---

## Event

Represents a recorded occurrence within the system.

Events describe change.

Events SHALL be immutable.

---

## Resource

Represents something consumed or utilized during execution.

Examples include:

* time
* storage
* compute
* credentials
* external services

---

## Session

Represents a bounded context for collaboration.

Sessions group related execution and communication.

---

## Protocol

Represents a documented communication contract.

Protocols define interactions rather than work.

---

# Relationships

Objects form a directed graph.

Examples include:

Goal

→ Task

Task

→ Artifact

Artifact

→ Evidence

Evidence

→ Decision

Decision

→ Goal

Participants

→ Roles

Roles

→ Capabilities

Sessions

→ Participants

Protocols

→ Participants

No restriction is placed upon additional relationships provided semantic integrity is preserved.

---

# Ownership

Every Object SHALL possess exactly one current Owner.

Ownership MAY change through documented Protocols.

Ownership SHALL remain observable.

---

# Identity

Object identifiers SHALL remain stable for the lifetime of the Object.

Identifiers SHALL NOT be reused.

---

# State

Every Object SHALL possess an explicit State.

State transitions SHALL be documented.

Future specifications define object-specific lifecycles.

---

# Extensibility

Implementations MAY introduce new Object types.

New Objects SHALL:

* define ownership,
* define lifecycle,
* define relationships,
* define normative behavior.

---

# Normative Requirements

**MTH-004-REQ-001**

Every Object SHALL possess a stable identifier.

**MTH-004-REQ-002**

Every Object SHALL possess exactly one Owner.

**MTH-004-REQ-003**

Every Object SHALL possess an explicit State.

**MTH-004-REQ-004**

Relationships between Objects SHALL remain observable.

**MTH-004-REQ-005**

Object lifecycles SHALL be explicitly documented.

---

# Design Rationale

Representing the Méthodos domain as interconnected Objects provides:

* implementation independence,
* replaceability,
* explicit ownership,
* graph-based reasoning,
* consistent lifecycle management,
* protocol interoperability.

---

# Future Directions

Future specifications define the detailed lifecycle, protocol interactions, and schema for each Object.

---

# Revision History

| Version | Date          | Notes             |
| ------- | ------------- | ----------------- |
| 0.1.0   | Initial draft | First publication |
