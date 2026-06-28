# Méthodos Specification

**Identifier:** MTH-028

**Title:** Observer

**Version:** 0.1.0

**Status:** Draft

**Category:** Roles

**Depends Upon:** MTH-023 through MTH-027

---

# Abstract

This specification defines the Observer Role.

An Observer monitors the state, progress, health, and history of a Méthodos deployment without modifying canonical state.

Observers provide situational awareness, reporting, auditing, and operational insight.

---

# Architectural Intent

Enable transparent observation of system behavior while preserving separation between observation and execution.

---

# Purpose

The Observer exists to answer questions such as:

* What Goals are active?
* What Tasks are blocked?
* What changed recently?
* What Decisions have been made?
* What requires attention?

The Observer provides understanding rather than execution.

---

# Responsibilities

An Observer MAY:

* discover canonical Objects;
* inspect Goal progress;
* inspect Task state;
* inspect Events;
* inspect Artifacts;
* inspect Evidence;
* inspect Decisions;
* generate reports;
* generate dashboards;
* summarize system state.

---

# Non-Responsibilities

An Observer SHALL NOT:

* create Goals;
* create Tasks;
* execute Tasks;
* modify canonical Objects;
* issue Decisions;
* approve work.

Observation is read-only.

---

# Relationships

The Observer primarily interacts with:

* Knowledge Repository
* Coordination Fabric
* Observability Protocol
* Discovery Protocol

---

# Conformance

A conforming Observer SHALL:

* remain read-only;
* preserve traceability;
* distinguish canonical and transient state;
* avoid modifying execution.

---

# Normative Requirements

**MTH-028-REQ-001**

Observers SHALL NOT modify canonical Objects.

**MTH-028-REQ-002**

Observers SHALL rely upon canonical Objects for historical reporting.

**MTH-028-REQ-003**

Observers MAY consume transient operational information provided it is not treated as authoritative.

---

# Design Rationale

Separating observation from execution enables independent reporting, auditing, dashboards, analytics, and operational awareness without affecting system behavior.

---

# Reference Implementation Notes

Possible Observer implementations include:

* operational dashboards;
* executive reporting agents;
* audit systems;
* monitoring platforms;
* analytics services.

---

# Revision History

| Version | Date          | Notes             |
| ------- | ------------- | ----------------- |
| 0.1.0   | Initial draft | First publication |
