# Méthodos Specification

**Identifier:** MTH-020

**Title:** Principal Role

**Version:** 0.1.0

**Status:** Draft

**Category:** Roles

**Depends Upon:** MTH-000 through MTH-015

---

# Abstract

This specification defines the Principal Role.

The Principal is the authoritative source of intent within a Méthodos implementation.

Only the Principal may establish, redefine, or retire Goals.

---

# Architectural Intent

Provide authoritative intent.

---

# Purpose

The Principal establishes why work exists.

The Principal defines desired outcomes without prescribing implementation details unless explicitly required.

---

# Responsibilities

The Principal SHALL:

* establish Goals
* define Success Criteria
* define Constraints
* establish Priorities
* review outcomes
* approve changes to Goal intent

---

# Authorities

The Principal MAY:

* create Goals
* modify Goal intent
* retire Goals
* authorize exceptional actions
* delegate operational authority

Delegation SHALL NOT transfer ownership of intent.

---

# Prohibitions

The Principal SHALL NOT:

* directly execute Tasks solely by virtue of this Role
* bypass governance protocols
* redefine historical Evidence or Decisions

A Participant may simultaneously fulfill the Principal Role and another Role, provided the responsibilities remain logically distinct.

---

# Relationships

The Principal establishes Goals.

The Principal receives Decisions.

The Principal authorizes changes to Goal intent.

---

# Conformance

A conforming Principal Role:

* originates Goal intent,
* defines Success Criteria,
* retains authority over Goal intent,
* reviews outcomes,
* and delegates execution without surrendering authority.

---

# Normative Requirements

**MTH-020-REQ-001**

Goal intent SHALL originate from a Principal.

**MTH-020-REQ-002**

Changes to Goal intent SHALL require Principal authorization.

**MTH-020-REQ-003**

Delegation SHALL NOT transfer ownership of intent.

---

# Design Rationale

Separating intent from execution preserves accountability while allowing execution to scale across many Participants.

---

# Revision History

| Version | Date          | Notes             |
| ------- | ------------- | ----------------- |
| 0.1.0   | Initial draft | First publication |
