# Méthodos Specification

**Identifier:** MTH-001

**Title:** Terminology

**Version:** 0.1.0

**Status:** Draft

**Category:** Foundational

**Depends Upon:** MTH-000

---

# Abstract

This document defines the normative vocabulary used throughout the Méthodos Specification.

The purpose of this document is to establish precise meanings for recurring concepts and to eliminate ambiguity between specifications.

Unless explicitly stated otherwise, capitalized terms appearing throughout the Méthodos Specification SHALL carry the meanings defined in this document.

---

# Purpose

Collaborative systems fail as often through inconsistent language as through incorrect implementation.

Méthodos therefore adopts a single, normative vocabulary.

Every specification, implementation, and participant SHOULD use these definitions consistently.

---

# Normative Definitions

## Principal

The human or organization that establishes Goals and retains ultimate authority over them.

A Principal MAY delegate responsibility but never ownership of intent.

---

## Participant

Any entity that performs a defined Role within a Méthodos implementation.

Participants MAY be human or computational.

---

## Role

A contractual definition of responsibilities and interfaces.

Roles define behavior independently of any specific implementation.

---

## Responsibility Naming

Méthodos SHALL use responsibility-specific fields rather than a generic `owner` field.

- `principal` identifies the authority that owns and authorizes intent.
- `orchestrator` identifies the Participant responsible for Goal-level coordination.
- `executor` identifies the Participant currently responsible for performing a Task.
- `reviewer` identifies the Participant responsible for review.
- `steward` or `maintainer` MAY identify ongoing custody of an Artifact or system component.

The term `owner` SHALL NOT be used without an explicitly defined domain-specific meaning.

---

## Implementation

A concrete realization of one or more Roles.

Example:

OpenClaw is an implementation of the Orchestrator Role.

---

## Goal

A desired outcome established by a Principal.

A Goal defines **what** should be achieved but does not prescribe **how** it will be achieved.

Goals exist independently of Tasks.

---

## Intent Envelope

The Principal-owned semantic core of a Goal.

The Intent Envelope defines the Objective, Success Criteria, Constraints, and Acceptance Criteria that must be preserved through planning, delegation, execution, review, and archival.

See `MTH-011 Intent Envelope`.

---

## Task

A bounded unit of work created in pursuit of a single Goal.

Every Task SHALL belong to exactly one parent Goal.

---

## Capability

A defined ability that may be exercised by a Participant.

Examples include planning, execution, reasoning, summarization, or software compilation.

Capabilities describe what a Participant can do.

They do not prescribe when those abilities should be used.

---

## Artifact

A durable product generated during execution.

Artifacts include:

* documents
* source code
* logs
* reports
* diagrams
* datasets
* screenshots

Artifacts SHALL be recoverable after execution has completed.

---

## Evidence

Information supporting the claim that a Task has achieved its intended outcome.

Evidence MAY include one or more Artifacts.

Completion without Evidence SHALL be considered incomplete.

---

## Decision

A durable governance Object that records an authoritative outcome.

Decisions authorize or reject state transitions, approvals, completions, supersessions, and other governance-relevant conclusions.

Final Decisions are immutable and may only be changed through superseding Decisions.

See `MTH-016 Decision`.

---

## Protocol

A documented contract governing communication between Participants.

Protocols define message structure, expectations, and permissible state transitions.

---

## Contract

A documented agreement defining responsibilities between Roles.

Contracts are normative.

Implementations SHALL conform to their applicable Contracts.

---

## State

A well-defined condition occupied by an Object at a particular time.

State transitions SHALL be explicit.

---

## Knowledge Repository

A durable system responsible for preserving institutional knowledge.

Knowledge Repositories outlive individual Participants.

---

## Coordination Fabric

A communication substrate responsible for coordinating Participants.

The Coordination Fabric SHALL NOT become the permanent repository of institutional knowledge.

---

## Inference Engine

A system capable of generating decisions or outputs through reasoning.

Méthodos intentionally remains agnostic regarding implementation.

---

## Execution

The process of performing work in pursuit of a Task.

Execution begins after planning.

Execution concludes only when Evidence has been produced or the Task has entered another terminal State.

---

## Lifecycle

The sequence of States through which an Object progresses.

Every lifecycle SHALL be explicitly documented.

---

# Naming Conventions

Throughout the Méthodos Specification:

* Capitalized terms refer to normative definitions contained within this document.
* Lowercase usage retains ordinary English meaning.

Example:

> "The Task entered the Blocked State."

uses two defined concepts.

Whereas

> "The task became difficult."

does not.

---

# Normative Requirements

**MTH-001-REQ-001**

Specifications SHALL use the normative terminology defined within this document.

**MTH-001-REQ-002**

New normative terms SHALL be introduced only within this document or an approved extension specification.

**MTH-001-REQ-003**

Implementations SHOULD avoid introducing synonymous terminology for existing defined concepts.

---

# Future Directions

Future revisions may define additional concepts including:

* Policy
* Resource
* Session
* Constraint
* Objective Metric
* Risk
* Dependency

These concepts are intentionally deferred until later specifications establish their context.

---

# Revision History

| Version | Date          | Notes                                                                                     |
| ------- | ------------- | ----------------------------------------------------------------------------------------- |
| 0.1.0   | Initial draft | First publication                                                                          |
| 0.1.1   | Round 3       | Added `Intent Envelope` and `Decision` to Normative Definitions (moved from round-3 diff) |
