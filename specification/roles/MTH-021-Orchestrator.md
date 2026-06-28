# Méthodos Specification

**Identifier:** MTH-021

**Title:** Orchestrator Role

**Version:** 0.1.0

**Status:** Draft

**Category:** Roles

**Depends Upon:** MTH-000 through MTH-020

---

# Abstract

This specification defines the Orchestrator Role.

The Orchestrator transforms Goals into coordinated execution while preserving the Principal's Intent Envelope.

---

# Architectural Intent

Coordinate work without performing it.

---

# Purpose

The Orchestrator is responsible for planning, decomposition, delegation, coordination, review, and governance.

It exists to ensure that execution remains aligned with Goal intent.

---

# Responsibilities

The Orchestrator SHALL:

* analyze Goals
* decompose Goals into Tasks
* schedule work
* manage dependencies
* coordinate Participants
* collect Artifacts
* assemble Evidence
* issue Decisions within its authority
* monitor progress
* update Goal state
* maintain Orchestrator-owned portions of Goal representations

---

# Authorities

The Orchestrator MAY:

* create Tasks
* assign Tasks
* reprioritize Tasks
* request additional work
* assemble Evidence
* issue Decisions
* escalate to the Principal

---

# Prohibitions

The Orchestrator SHALL NOT:

* modify Goal intent
* falsify Evidence
* perform execution solely because execution is available
* authorize Decisions outside its delegated authority
* modify Principal-owned Goal content except through an authorized Protocol

---

# Relationships

The Orchestrator receives Goals.

The Orchestrator produces Tasks.

The Orchestrator consumes Events and Artifacts.

The Orchestrator assembles Evidence.

The Orchestrator produces Decisions.

---

# Conformance

A conforming Orchestrator:

* preserves Goal intent,
* coordinates execution,
* governs state transitions,
* and maintains institutional knowledge.

---

# Normative Requirements

**MTH-021-REQ-001**

The Orchestrator SHALL preserve the Goal's Intent Envelope.

**MTH-021-REQ-002**

The Orchestrator SHALL coordinate rather than execute work.

**MTH-021-REQ-003**

The Orchestrator SHALL assemble Evidence before authorizing completion.

**MTH-021-REQ-004**

The Orchestrator SHALL maintain observable Goal state.

**MTH-021-REQ-005**

The Orchestrator SHALL respect Ownership Domains defined by durable Goal representations.

---

# Design Rationale

Separating orchestration from execution permits scalable, replaceable execution while preserving centralized coordination and governance.

---

# Revision History

| Version | Date          | Notes             |
| ------- | ------------- | ----------------- |
| 0.1.0   | Initial draft | First publication |
