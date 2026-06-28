# Méthodos Specification

**Identifier:** MTH-005

**Title:** Design Principles

**Version:** 0.1.0

**Status:** Draft

**Category:** Foundational

**Depends Upon:** MTH-000 through MTH-004

---

# Abstract

This document defines the design principles that guide the evolution of the Méthodos Specification.

Unlike normative requirements, these principles are intended to guide architectural judgment when multiple conforming implementations are possible.

Future specifications SHOULD remain consistent with these principles unless explicitly justified.

---

# Purpose

A specification cannot anticipate every future technology, implementation, or use case.

Design principles provide stable guidance where detailed requirements do not yet exist.

They help preserve coherence as Méthodos evolves.

---

# DP-01 — Preserve Intent

The purpose of collaboration is to achieve the Principal's intent.

Every architectural decision SHOULD maximize the fidelity with which intent survives planning, delegation, execution, interruption, and review.

---

# DP-02 — Make State Explicit

Hidden state is a source of ambiguity.

Participants SHOULD prefer explicit state transitions over inferred state.

Observable systems are easier to understand, debug, and extend.

---

# DP-03 — Prefer Contracts Over Convention

Behavior should arise from documented contracts rather than unwritten expectations.

When conventions become essential, they SHOULD be promoted into specifications.

---

# DP-04 — Separate Responsibility From Implementation

Responsibilities belong to Roles.

Technologies implement Roles.

This distinction permits implementations to evolve independently of architecture.

---

# DP-05 — Preserve Institutional Memory

Information that may become valuable in the future SHOULD be recorded.

Participants should leave the system in a state where another Participant can continue work without reconstructing context.

---

# DP-06 — Optimize for Collaboration

Local optimization SHOULD NOT reduce overall system effectiveness.

The success of the system is measured by collective outcomes rather than individual efficiency.

---

# DP-07 — Prefer Replaceability

Implementations should be replaceable.

Architectural dependencies on specific technologies SHOULD be minimized.

---

# DP-08 — Produce Evidence Continuously

Evidence should be generated as work progresses rather than reconstructed after completion.

Continuous evidence improves transparency, validation, and recovery.

---

# DP-09 — Fail Recoverably

Failure is expected.

Designs SHOULD minimize irreversible failure.

Participants should preserve sufficient information to resume execution after interruption.

---

# DP-10 — Human Judgment Remains Authoritative

Automation expands human capability.

It does not replace human responsibility.

Architectures SHOULD preserve meaningful human oversight over goals, priorities, and irreversible decisions.

---

# DP-11 — Optimize for Understanding

Architectures SHOULD be understandable before they are clever.

Complexity is acceptable only when it provides corresponding value.

Future contributors should be able to understand the system without access to undocumented assumptions.

---

# DP-12 — Design for Evolution

The architecture should anticipate change.

Specifications SHOULD favor extension over modification.

Backward compatibility SHOULD be preserved whenever practical.

---

# Relationship to Requirements

Requirements describe what implementations MUST do.

Design Principles describe how architects SHOULD think.

When a future implementation satisfies all requirements but violates the spirit of these principles, the architecture SHOULD be reconsidered.

---

# Design Review Questions

Architects are encouraged to evaluate proposed changes by asking:

* Does this preserve the Principal's intent?
* Does this reduce or increase hidden state?
* Does this strengthen or weaken role boundaries?
* Does this improve replaceability?
* Does this preserve institutional knowledge?
* Does this improve recoverability?
* Does this make the system easier to understand?
* Does this improve collaboration rather than merely optimizing one component?

---

# Future Directions

Future versions of this document may introduce additional principles as new architectural patterns emerge.

New principles SHOULD remain concise, durable, and implementation-independent.

---

# Revision History

| Version | Date          | Notes             |
| ------- | ------------- | ----------------- |
| 0.1.0   | Initial draft | First publication |
