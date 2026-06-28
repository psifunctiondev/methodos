# Méthodos Reference Implementation

**Identifier:** RI-004

**Title:** Obsidian Knowledge Repository Reference Implementation

**Version:** 0.1.0

**Status:** Draft

**Implements:** Knowledge Repository

**Depends Upon:** MTH-000 through MTH-022

---

# Abstract

This document defines Obsidian as the reference implementation of the Méthodos Knowledge Repository.

Obsidian stores the durable Objects that constitute the institutional memory of the system.

---

# Architectural Intent

Preserve institutional knowledge independently of individual Participants.

---

# Purpose

Obsidian provides a durable, human-readable, version-controlled repository for:

* Goals
* Tasks
* Events
* Artifacts
* Evidence
* Decisions
* Architecture
* Documentation

---

# Responsibilities

Obsidian SHALL:

* preserve Goal definitions;
* preserve Task definitions;
* preserve Event history;
* preserve Evidence;
* preserve Decisions;
* preserve architectural documentation;
* preserve execution history.

---

# Non-Responsibilities

Obsidian SHALL NOT:

* coordinate execution;
* maintain leases;
* provide distributed locking;
* perform scheduling;
* replace Redis.

---

# Recommended Vault Structure

```text
Goals/

Tasks/

Events/

Artifacts/

Evidence/

Decisions/

Architecture/

Specifications/

Reference/

Daily Notes/

Templates/
```

---

# Canonical Objects

The following Objects SHALL be considered canonical when stored within Obsidian:

* Goal
* Task
* Event
* Evidence
* Decision

Artifacts MAY be stored externally provided stable references exist.

---

# Knowledge Flow

Principal creates Goal

↓

OpenClaw creates Tasks

↓

Hermes produces Artifacts

↓

OpenClaw assembles Evidence

↓

OpenClaw records Decisions

↓

Goal updated

All durable Objects remain discoverable through the vault.

---

# Human Collaboration

Obsidian SHALL permit:

* manual Goal authoring;
* collaborative review;
* architectural discussion;
* historical inspection;
* independent auditing.

Human edits SHOULD generate corresponding Events when appropriate.

---

# Version Control

The vault SHOULD be version controlled.

Every meaningful change SHOULD remain recoverable.

Git is the recommended reference implementation.

---

# Linking

Objects SHOULD use stable identifiers.

Relationships SHOULD be represented through bidirectional links where practical.

Knowledge SHOULD remain navigable.

---

# Conformance

A conforming Obsidian implementation:

* preserves institutional knowledge;
* maintains durable Objects;
* supports human review;
* supports version history;
* remains independent of execution infrastructure.

---

# Design Rationale

Markdown provides durable, portable, inspectable knowledge.

Obsidian adds linking, visualization, and human collaboration without coupling Méthodos to proprietary infrastructure.

---

# Revision History

| Version | Date          | Notes             |
| ------- | ------------- | ----------------- |
| 0.1.0   | Initial draft | First publication |
