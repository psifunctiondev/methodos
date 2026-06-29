# Méthodos

> **A framework for collaborative, goal-directed intelligence.**

Méthodos is an open architectural framework for building systems in which humans and autonomous participants collaborate to accomplish complex goals while preserving intent, producing verifiable evidence, and accumulating institutional knowledge.

Rather than defining a particular AI agent, model, or implementation, Méthodos defines the contracts that allow many independent participants to work together.

The framework separates **intent**, **coordination**, **execution**, **governance**, and **knowledge**, allowing implementations to evolve without changing the surrounding architecture.

---

# Core Principles

Méthodos is founded on three guiding principles:

* **Preserve Intent** — The Principal's objectives remain authoritative throughout delegation and execution.
* **Produce Evidence** — Completion is justified through explicit, reviewable evidence rather than assertion.
* **Maintain Institutional Knowledge** — Knowledge survives individual participants and remains durable, discoverable, and reusable.

---

# Architectural Overview

Méthodos models collaborative work as a sequence of durable objects:

```text
Principal
    │
    ▼
Goal
    │
    ▼
Task
    │
    ▼
Execution
    │
    ▼
Artifacts
    │
    ▼
Evidence
    │
    ▼
Decision
    │
    ▼
Knowledge
```

Each object has a formal specification, a lifecycle, and defined relationships to the other objects in the system.

---

# Repository Structure

```text
specification/    Normative Méthodos specifications (MTH)

reference/        Reference implementations (RI)

schemas/          Canonical object schemas

diagrams/         Architecture and protocol diagrams

dossier/          Canonical Goal Dossier template

examples/         Example workflows

experiments/      Prototype implementations

notes/            Working notes
```

---

# Specifications

The framework is organized into several specification families.

| Family     | Purpose                                          |
| ---------- | ------------------------------------------------ |
| Foundation | Vision, terminology and architectural principles |
| Kernel     | Core object definitions                          |
| Roles      | Participant contracts                            |
| Protocols  | Operational behavior                             |
| Governance | Lifecycle, compliance and evolution              |
| Appendix   | Reference material                               |

---

# Reference Implementations

The current reference implementations include:

* OpenClaw (Orchestrator)
* Hermes (Executor)
* Redis (Coordination Fabric)
* Obsidian (Knowledge Repository)
* LiteLLM (Inference Router)
* Open WebUI

These implementations demonstrate one possible realization of the Méthodos architecture.

They are not normative.

---

# Goal Dossiers

A Goal Dossier is the complete institutional record for accomplishing a single Goal.

A dossier typically contains:

```text
METHODOS.md

Goals/
Tasks/
Events/
Artifacts/
Evidence/
Decisions/

Architecture/
Research/
Meetings/
Daily Notes/

Templates/
```

A deployment may maintain many Goal Dossiers within a single Knowledge Repository.

---

# Design Philosophy

Méthodos deliberately separates concerns.

* The **Principal** defines intent.
* The **Orchestrator** coordinates work.
* The **Executor** performs work.
* The **Inference Router** provides reasoning capabilities.
* The **Knowledge Repository** preserves durable knowledge.
* The **Coordination Fabric** enables transient collaboration.

This separation allows implementations to remain modular, replaceable, and independently evolvable.

---

# Current Status

Méthodos is under active development.

The architecture is currently focused on defining the core specifications and validating them through real-world implementations using OpenClaw and Hermes.

---

# Getting Started

If you are new to the project, begin with:

1. `specification/foundation/MTH-000-Vision-and-Scope.md`
2. `specification/foundation/MTH-003-Architecture.md`
3. `specification/kernel/MTH-010-Goal.md`
4. `specification/kernel/MTH-011-Task.md`
5. `reference/RI-001-OpenClaw/`
6. `reference/RI-002-Hermes/`

---

# Vision

Méthodos seeks to become an implementation-independent standard for collaborative, goal-directed systems in which humans and autonomous participants cooperate through explicit contracts rather than implicit assumptions.

The framework is designed to remain applicable as models, tools, and execution environments evolve.

---

## Project Status

**Version:** 0.1 (Foundation)

The architecture is stabilizing and the first reference implementations are under active development.

Contributions, discussion, experimentation, and implementation feedback are welcome.
