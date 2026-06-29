# Méthodos Specification

**Identifier:** MTH-010

**Title:** Goal Object

**Version:** 0.1.0

**Status:** Draft

**Category:** Core Domain

**Depends Upon:** MTH-000 through MTH-005

---

# Abstract

This document defines the Goal Object within Méthodos.

A Goal represents a desired outcome established by a Principal. Goals preserve intent, authorize Tasks, define success criteria, and provide the primary organizing structure for coordinated work.

---

# Purpose

Goals are the origin point of meaningful activity in Méthodos.

The purpose of the Goal Object is to preserve the Principal's intent across planning, delegation, execution, interruption, review, and completion.

---

# Definition

A Goal is a durable Object representing a desired outcome.

A Goal defines **what** should be achieved.

A Goal SHALL NOT prescribe the complete method by which it must be achieved unless the Principal explicitly includes such constraints.

---

# Required Properties

Every Goal SHALL include:

* Identifier
* Title
* Owner
* Principal
* Current State
* Created Timestamp
* Modified Timestamp
* Description
* Success Criteria
* Constraints
* Priority
* Related Tasks
* Evidence References
* Decision References
* Status History

---

# Goal States

A Goal SHALL occupy exactly one State at a time.

The standard Goal States are:

* Draft
* Ready
* Planning
* Active
* Blocked
* Review
* Complete
* Archived

---

# State Definitions

## Draft

The Goal exists but is not ready for planning.

## Ready

The Goal has sufficient definition for planning.

## Planning

An Orchestrator is decomposing the Goal into Tasks.

## Active

One or more Tasks are executing in pursuit of the Goal.

## Waiting

The Goal is paused pending external input, dependency, or timing.

## Blocked

Progress cannot continue without intervention.

## Review

Execution is complete, but final acceptance has not occurred.

## Complete

The Goal has satisfied its Success Criteria.

## Archived

The Goal is no longer active and is retained for institutional memory.

---

# Ownership

Every Goal SHALL have exactly one Owner.

The Owner is responsible for maintaining the Goal's current status and ensuring that its Success Criteria remain coherent.

The Principal retains authority over intent even when operational ownership is delegated.

---

# Success Criteria

Every Ready, Planning, Active, Review, or Complete Goal SHALL contain Success Criteria.

Success Criteria SHOULD be observable.

Success Criteria SHOULD distinguish completion from mere activity.

A Goal SHOULD NOT enter Complete State unless its Success Criteria are satisfied by Evidence.

---

# Constraints

Constraints define limits on acceptable execution.

Constraints MAY include:

* budget
* time
* tooling
* security boundaries
* approval requirements
* implementation preferences
* excluded approaches

Participants SHALL preserve constraints unless explicitly authorized to modify them.

---

# Relationship to Tasks

A Goal MAY contain zero or more Tasks.

Every Task SHALL belong to exactly one parent Goal.

Tasks exist to advance Goals.

Tasks SHALL NOT redefine Goal intent.

---

# Relationship to Evidence

A Goal MAY reference Evidence.

A Goal SHOULD enter Complete State only when sufficient Evidence supports completion.

Evidence MAY be produced by one or more Tasks.

---

# Relationship to Decisions

A Goal MAY reference Decisions.

Decisions affecting intent, scope, constraints, or success criteria SHALL be recorded.

---

# Normative Requirements

**MTH-010-REQ-001**

Every Goal SHALL have a stable Identifier.

**MTH-010-REQ-002**

Every Goal SHALL have exactly one Owner.

**MTH-010-REQ-003**

Every Goal SHALL identify its Principal.

**MTH-010-REQ-004**

Every Ready, Planning, Active, Review, or Complete Goal SHALL define Success Criteria.

**MTH-010-REQ-005**

A Goal SHALL NOT enter Complete State without Evidence.

**MTH-010-REQ-006**

Tasks SHALL NOT redefine Goal intent.

**MTH-010-REQ-007**

Changes to Goal intent SHALL be authorized by the Principal.

**MTH-010-REQ-008**

Every durable Goal representation SHALL define ownership domains.

---

# Recommended Obsidian Representation

A Goal MAY be represented as a Markdown document.

Recommended front matter:

```yaml
id:
type: goal
title:
principal:
owner:
state:
priority:
created:
modified:
success_criteria:
constraints:
related_tasks:
evidence:
decisions:
```

Recommended sections:

```markdown
# Goal

## Description

## Success Criteria

## Constraints

## Current Status

## Related Tasks

## Evidence

## Decisions

## Progress Log

## Open Questions
```

---

# Design Rationale

The Goal Object exists to preserve intent.

Without a durable Goal representation, downstream Participants may optimize locally while drifting away from the Principal's desired outcome.

By requiring explicit Success Criteria, ownership, constraints, and Evidence, Méthodos ensures that Goals remain actionable, reviewable, and recoverable.

---

# Anti-Patterns

The following behaviors are non-conforming or discouraged:

* Treating a vague wish as an Active Goal.
* Completing a Goal without Evidence.
* Allowing an Executor to redefine intent.
* Splitting related work into disconnected Goals without rationale.
* Using Tasks as substitutes for Goals.
* Maintaining Goal state only in conversational context.

---

# Future Directions

Future specifications will define:

* Goal Protocol
* Task Object
* Evidence Object
* Approval Protocol
* Obsidian Goal Template
* Redis Goal Indexing

---

# Ownership Domains

A Goal SHALL define ownership domains for its durable representation.

Ownership domains identify which Participants are authorized to modify specific portions of a Goal.

Typical ownership domains include:

- Principal-owned
- Orchestrator-owned
- Shared
- System-generated

Participants SHALL NOT modify content outside their ownership domain except through an explicit Protocol.

Ownership domains protect Goal intent while allowing collaborative maintenance of operational state.

---

# Revision History

| Version | Date          | Notes             |
| ------- | ------------- | ----------------- |
| 0.1.0   | Initial draft | First publication |
