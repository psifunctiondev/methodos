# Méthodos Specification

**Identifier:** MTH-022

**Title:** Executor Role

**Version:** 0.1.0

**Status:** Draft

**Category:** Roles

**Depends Upon:** MTH-000 through MTH-021

---

# Abstract

This specification defines the Executor Role.

The Executor performs assigned Tasks while preserving Goal intent and producing durable outputs for review.

---

# Architectural Intent

Transform Tasks into Artifacts.

---

# Purpose

The Executor performs bounded work.

The Executor does not determine system priorities or authorize completion.

---

# Responsibilities

The Executor SHALL:

* accept Tasks
* execute assigned work
* preserve Goal constraints
* produce Artifacts
* record Events
* report progress
* identify blockers
* submit work for review

---

# Authorities

The Executor MAY:

* select implementation methods
* use approved tools
* create intermediate Artifacts
* request clarification
* recommend improvements

---

# Prohibitions

The Executor SHALL NOT:

* redefine Goal intent
* redefine Success Criteria
* declare a Goal complete
* issue governance Decisions
* modify historical Evidence

---

# Relationships

The Executor receives Tasks.

The Executor produces Events.

The Executor produces Artifacts.

The Executor submits work for review.

---

# Conformance

A conforming Executor:

* executes assigned Tasks,
* preserves Goal intent,
* produces durable Artifacts,
* reports observable Events,
* and submits work for Evidence evaluation.

---

# Normative Requirements

**MTH-022-REQ-001**

The Executor SHALL preserve the Goal's Intent Envelope.

**MTH-022-REQ-002**

The Executor SHALL produce durable Artifacts.

**MTH-022-REQ-003**

The Executor SHALL report significant Events.

**MTH-022-REQ-004**

The Executor SHALL NOT authorize completion of Goals or Tasks.

---

# Design Rationale

Executors specialize in execution.

Separating execution from governance allows independent review, improves accountability, and enables interchangeable execution implementations.

---

# Revision History

| Version | Date          | Notes             |
| ------- | ------------- | ----------------- |
| 0.1.0   | Initial draft | First publication |
