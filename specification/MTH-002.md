# Méthodos Specification

**Identifier:** MTH-002

**Title:** Foundational Principles

**Version:** 0.1.0

**Status:** Draft

**Category:** Foundational

**Depends Upon:** MTH-000, MTH-001

---

# Abstract

This document defines the foundational principles governing all conforming Méthodos implementations.

Unlike implementation requirements, these principles describe the architectural values from which subsequent specifications derive.

Where implementation choices are ambiguous, these principles SHALL take precedence.

---

# Purpose

Distributed collaboration succeeds when every Participant shares the same assumptions regarding authority, coordination, knowledge, and evidence.

These principles establish those assumptions.

---

# Principle 1 — Intent is Conserved

Goals originate with the Principal.

Participants MAY refine execution strategies.

Participants SHALL NOT redefine intent without explicit authorization.

Intent flows downward.

Authority flows upward.

---

# Principle 2 — Knowledge is Shared

Information required for future work belongs to the system rather than any individual Participant.

Institutional knowledge SHALL be durable.

The departure or replacement of any Participant SHALL NOT result in irreversible knowledge loss.

---

# Principle 3 — Coordination Precedes Execution

Execution without coordination introduces unnecessary risk.

Planning SHOULD occur before execution whenever practical.

Participants SHALL prefer coordinated action over independent optimization.

---

# Principle 4 — Evidence Over Assertion

Claims are not completion.

Completion requires Evidence.

Assertions unsupported by Evidence SHOULD be treated as incomplete.

---

# Principle 5 — Roles Define Responsibility

Responsibilities belong to Roles rather than implementations.

Implementations MAY change.

Role contracts remain stable.

---

# Principle 6 — State is Explicit

Objects SHALL occupy well-defined States.

Transitions SHALL be observable.

Implicit state is prohibited.

---

# Principle 7 — Communication Occurs Through Contracts

Participants communicate through documented Protocols.

Behavior based upon undocumented assumptions is non-conforming.

---

# Principle 8 — Transparency Exceeds Cleverness

Participants SHOULD prefer behavior that is understandable over behavior that is merely efficient.

Reasoning SHOULD be recoverable.

Decisions SHOULD be explainable.

---

# Principle 9 — Continuity is Mandatory

Interrupted work SHALL remain resumable.

Participants SHALL preserve sufficient context for another Participant to continue execution.

---

# Principle 10 — Replaceability

Every implementation SHOULD be replaceable by another conforming implementation without requiring architectural redesign.

The specification values interchangeable Roles over permanent implementations.

---

# Normative Requirements

**MTH-002-REQ-001**

Conforming implementations SHALL preserve Goal intent throughout execution.

**MTH-002-REQ-002**

Institutional knowledge SHALL survive Participant replacement.

**MTH-002-REQ-003**

Completion SHALL require Evidence.

**MTH-002-REQ-004**

Participants SHALL communicate using documented Protocols.

**MTH-002-REQ-005**

Every Object SHALL possess an explicit State.

---

# Design Consequences

These principles intentionally favor:

* durability over convenience,
* transparency over opacity,
* coordination over autonomy,
* interoperability over specialization,
* architecture over implementation.

Implementations MAY optimize behavior provided these principles remain satisfied.

---

# Future Directions

Future specifications will refine these principles into concrete contracts governing Goals, Tasks, Protocols, Participants, and Evidence.

---

# Revision History

| Version | Date          | Notes             |
| ------- | ------------- | ----------------- |
| 0.1.0   | Initial draft | First publication |
