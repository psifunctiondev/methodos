# Méthodos Specification

**Identifier:** MTH-000

**Title:** Vision and Scope

**Version:** 0.1.0

**Status:** Draft

**Category:** Foundational

---

# Abstract

Méthodos is an implementation-independent framework for collaborative, goal-directed intelligence.

It defines the principles, roles, objects, and protocols required for independent participants—human or computational—to cooperate toward shared objectives while maintaining transparency, accountability, and continuity.

Méthodos is not a software product.

It is not a programming framework.

It is not an agent implementation.

It is a specification.

Implementations that conform to the Méthodos Specification share a common architecture for representing goals, coordinating work, preserving institutional knowledge, and producing verifiable outcomes.

The first reference implementation of Méthodos consists of:

* A human Principal
* An Orchestrator
* One or more Executors
* A Coordination Fabric
* A Knowledge Repository
* An Inference Router
* One or more Inference Engines

The specification intentionally defines roles rather than technologies.

---

# Purpose

The purpose of Méthodos is to enable complex work to be performed collaboratively by independent participants while preserving:

* clarity of intent,
* continuity of execution,
* accountability,
* explainability,
* evidence,
* and human authority.

The framework recognizes that successful goal pursuit requires more than inference.

It requires planning, delegation, execution, validation, communication, documentation, and institutional memory.

Méthodos provides a common language for these activities.

---

# Scope

The Méthodos Specification defines:

* architectural principles;
* normative terminology;
* object models;
* participant roles;
* communication protocols;
* lifecycle definitions;
* governance mechanisms;
* evidence requirements;
* and interoperability contracts.

The specification intentionally avoids prescribing implementation technologies except where required for interoperability.

---

# Non-Goals

Méthodos does not attempt to define:

* machine learning algorithms;
* language model architectures;
* prompt engineering techniques;
* user interface design;
* programming languages;
* deployment platforms;
* hardware;
* networking protocols;
* inference optimization;
* benchmarking methodologies.

These are implementation concerns.

---

# Vision

The long-term vision of Méthodos is to make collaborative intelligence as disciplined as modern software engineering.

Participants should be able to:

* delegate work confidently,
* resume interrupted work,
* replace individual components,
* audit historical decisions,
* understand why actions occurred,
* verify completed work,
* and improve the system incrementally without redesigning its foundations.

No participant should possess unique knowledge that cannot be recovered from the shared system.

---

# Guiding Philosophy

Méthodos adopts the following philosophical assumptions.

## Goals are primary.

Every meaningful activity exists in service of an explicit goal.

## Knowledge is shared.

Important information belongs to the system rather than any individual participant.

## Roles are contractual.

Participants are defined by responsibilities rather than identities.

## Evidence is mandatory.

Assertions are weaker than evidence.

Completion requires evidence.

## Coordination precedes execution.

Work should be organized before it is performed.

## Humans remain principals.

Authority originates with human participants.

Automation expands capability but does not replace responsibility.

---

# Initial Normative Requirements

**MTH-000-REQ-001**

A conforming implementation MUST maintain an explicit representation of every active Goal.

**MTH-000-REQ-002**

Every Task MUST belong to exactly one parent Goal.

**MTH-000-REQ-003**

Every Task MUST have exactly one current owner.

**MTH-000-REQ-004**

Completion claims MUST be supported by evidence.

**MTH-000-REQ-005**

Participants MUST communicate through documented contracts rather than implicit assumptions.

**MTH-000-REQ-006**

Institutional knowledge MUST survive the replacement of individual participants.

---

# Success Criteria

Méthodos succeeds when:

* participants can cooperate without ambiguity;
* work survives interruption;
* historical reasoning remains understandable;
* independent implementations remain interoperable;
* and replacing one implementation does not require redesigning the framework.

---

# Future Directions

Future versions of the specification may define:

* federated orchestration,
* distributed executor pools,
* self-improving planning,
* learning protocols,
* capability marketplaces,
* and formal verification of execution.

These topics are intentionally deferred until the foundational architecture is stable.

---

# Revision History

| Version | Date          | Notes             |
| ------- | ------------- | ----------------- |
| 0.1.0   | Initial draft | First publication |
