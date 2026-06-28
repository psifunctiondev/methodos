# Méthodos Specification

**Identifier:** MTH-003

**Title:** Architecture

**Version:** 0.1.0

**Status:** Draft

**Category:** Foundational

**Depends Upon:** MTH-000, MTH-001, MTH-002

---

# Abstract

This document defines the architectural model of Méthodos.

The architecture is expressed in terms of responsibilities, ownership, information flow, and coordination rather than software components.

Implementations MAY differ in technology while remaining conformant to this architecture.

---

# Purpose

The purpose of the Méthodos architecture is to separate concerns in a manner that promotes replaceability, transparency, and reliable collaboration.

Architecture defines relationships.

Implementations define mechanisms.

---

# Architectural Overview

Méthodos consists of five interacting planes.

Each plane owns a distinct category of responsibility.

No plane SHALL assume the responsibilities of another except through documented Protocols.

---

# Plane 1 — Intent

The Intent Plane represents why work exists.

It contains:

* Goals
* Priorities
* Constraints
* Success Criteria
* Human authority

Intent originates exclusively from the Principal.

Intent SHALL NOT originate from Executors.

---

# Plane 2 — Knowledge

The Knowledge Plane preserves institutional memory.

It contains:

* documentation
* decisions
* artifacts
* evidence
* historical execution
* architecture

Knowledge MUST survive replacement of individual Participants.

---

# Plane 3 — Coordination

The Coordination Plane transforms Goals into executable work.

Responsibilities include:

* planning
* decomposition
* delegation
* scheduling
* dependency management
* lifecycle management
* progress tracking

Coordination SHALL NOT directly perform execution except where explicitly permitted.

---

# Plane 4 — Execution

The Execution Plane performs Tasks.

Responsibilities include:

* reasoning
* tool use
* validation
* artifact generation
* evidence collection

Execution SHALL preserve Goal intent.

Execution SHALL report outcomes.

---

# Plane 5 — Inference

The Inference Plane provides computational reasoning capability.

Responsibilities include:

* model selection
* inference
* retrieval
* embedding
* summarization
* generation

The Inference Plane SHALL remain replaceable.

Architectural behavior SHALL NOT depend upon a specific inference implementation.

---

# Information Flow

Information flows primarily in one direction.

Intent

↓

Coordination

↓

Execution

↓

Evidence

↓

Knowledge

Knowledge then informs future Intent.

This creates a continuous improvement cycle.

---

# Authority Flow

Authority flows downward.

The Principal authorizes Goals.

Goals authorize Tasks.

Tasks authorize Execution.

Execution does not authorize Goals.

---

# Evidence Flow

Evidence flows upward.

Execution produces Evidence.

Evidence informs Coordination.

Coordination informs the Principal.

Evidence becomes institutional Knowledge.

---

# Replaceability

Every implementation SHOULD be replaceable without modifying the architectural model.

Replacing an implementation SHALL NOT require redefining Roles, Objects, or Protocols.

---

# Normative Requirements

**MTH-003-REQ-001**

Implementations SHALL preserve separation between architectural planes.

**MTH-003-REQ-002**

Intent SHALL originate only from the Principal.

**MTH-003-REQ-003**

Execution SHALL produce Evidence.

**MTH-003-REQ-004**

Knowledge SHALL remain durable.

**MTH-003-REQ-005**

Architectural behavior SHALL remain independent of specific implementation technologies.

---

# Design Rationale

Separating architecture into planes rather than implementations ensures that:

* implementations remain replaceable,
* technologies evolve independently,
* responsibilities remain clear,
* collaboration remains stable despite technological change.

---

# Future Directions

Subsequent specifications define:

* Objects
* Roles
* Protocols
* Lifecycles
* Implementations

Each SHALL conform to the architectural model defined herein.

---

# Revision History

| Version | Date          | Notes             |
| ------- | ------------- | ----------------- |
| 0.1.0   | Initial draft | First publication |
