# Méthodos Reference Implementation

**Identifier:** RI-001

**Title:** OpenClaw Orchestrator Reference Implementation

**Version:** 0.1.0

**Status:** Draft

**Implements:** MTH-021 Orchestrator Role

**Depends Upon:** MTH-000 through MTH-022

---

# Abstract

This document defines how OpenClaw implements the Méthodos Orchestrator Role.

OpenClaw is responsible for receiving Goals, preserving the Principal's Intent Envelope, decomposing Goals into Tasks, coordinating execution through the Coordination Fabric, assembling Evidence from Artifacts, issuing Decisions within delegated authority, and updating institutional Knowledge.

---

# Implementation Role

OpenClaw implements the **Orchestrator** Role.

OpenClaw SHALL NOT be treated as the Principal.

OpenClaw SHALL NOT be treated as the Executor.

OpenClaw coordinates work; it does not perform long-running execution.

---

# Responsibilities

OpenClaw SHALL:

* monitor the Knowledge Repository for new or updated Goals;
* validate that each Goal has an Intent Envelope;
* decompose Ready Goals into Tasks;
* publish executable Tasks to the Coordination Fabric;
* monitor Task state;
* consume Events and Artifact references;
* assemble Evidence from Artifacts;
* issue Decisions within delegated authority;
* update Goal and Task state in the Knowledge Repository;
* escalate ambiguity, risk, or blocked work to the Principal.

---

# Non-Responsibilities

OpenClaw SHALL NOT:

* redefine Goal intent without Principal authorization;
* execute Tasks that belong to the Executor Role;
* treat Redis messages as durable institutional Knowledge;
* accept completion claims without Evidence;
* allow Executors to authorize their own completion;
* silently discard failed or blocked Tasks.

---

# Operational Loop

OpenClaw SHOULD operate according to the following loop:

1. Discover Goals.
2. Validate Goal completeness.
3. Plan Tasks.
4. Publish Tasks.
5. Monitor execution.
6. Collect Events and Artifacts.
7. Assemble Evidence.
8. Issue Decisions.
9. Update Knowledge Repository.
10. Continue until Goal reaches Complete, Blocked, or Archived.

---

# Goal Intake

OpenClaw SHALL treat the Knowledge Repository as the authoritative intake location for Goals.

For the current reference implementation, Goals MAY be represented as Markdown files in a shared Obsidian vault.

OpenClaw SHOULD only plan Goals whose State is `Ready`.

Goals in `Draft` SHOULD be left untouched except for optional advisory comments.

---

# Task Creation

For each Goal, OpenClaw SHOULD create bounded Tasks.

Each Task SHALL:

* reference exactly one parent Goal;
* preserve the Goal's Intent Envelope;
* contain observable Success Criteria;
* contain inherited Constraints;
* define Dependencies where known;
* be small enough for an Executor to complete independently.

OpenClaw SHALL NOT create Tasks that require the Executor to infer the Principal's intent from missing context.

OpenClaw SHOULD NOT use internal `/goal` mechanisms for long-running execution. If OpenClaw uses `/goal`, it SHOULD be limited to planning, decomposition, review, or specification analysis. Execution work SHOULD be delegated to Executors through Tasks.

---

# Delegating Tasks to Hermes `/goal`

OpenClaw MAY delegate execution to Hermes by creating a Task that Hermes can safely convert into an internal `/goal`.

OpenClaw SHALL NOT send Hermes an unbounded parent Goal unless Hermes has explicitly been assigned full execution responsibility for that Goal.

A Hermes-bound Task SHOULD include:

- Task Identifier
- Parent Goal Identifier
- Task Objective
- Relevant Goal Intent Envelope
- Success Criteria
- Constraints
- Dependencies
- Allowed Tools or Capabilities
- Disallowed Actions
- Required Artifacts
- Reporting Requirements
- Expected terminal statuses

OpenClaw SHOULD phrase the delegated work as a bounded execution objective.

Good delegation:

> Complete Task T-20260628-004. Implement the Redis lease heartbeat check described in the Task Objective. Preserve the parent Goal constraints. Produce a patch, execution log, and test result artifact. Report `ready_for_review`, `blocked`, `waiting`, `failed`, or `needs_clarification`.

Bad delegation:

> Finish the whole Redis integration.

OpenClaw SHALL NOT ask Hermes to:

- redefine Goal intent;
- change Success Criteria;
- reprioritize the parent Goal;
- issue Decisions;
- mark Tasks or Goals complete;
- modify Principal-owned Goal content.

OpenClaw SHOULD require Hermes to return:

```json
{
  "task_id": "",
  "parent_goal_id": "",
  "status": "ready_for_review",
  "summary": "",
  "artifacts": [],
  "events": [],
  "blockers": [],
  "questions": [],
  "recommendations": []
}

---

# Redis Coordination

Redis is the Coordination Fabric in this reference implementation.

OpenClaw SHALL use Redis for transient coordination, not durable Knowledge.

Recommended Redis structures:

```text
queue:tasks:ready
task:{task_id}
lease:{task_id}
event:stream
worker:{worker_id}:heartbeat
```

OpenClaw SHOULD publish Tasks to `queue:tasks:ready`.

OpenClaw SHOULD monitor Events and Task status updates.

OpenClaw SHALL NOT rely on Redis as the only durable record of Goal, Task, Artifact, Evidence, or Decision state.

---

# Evidence Assembly

OpenClaw SHALL assemble Evidence from Artifacts produced by Executors.

Evidence SHALL include:

* an explicit Claim;
* supporting Artifact references;
* validation method;
* related Goal or Task;
* confidence assessment;
* summary.

OpenClaw SHALL NOT treat Artifacts as Evidence without evaluation.

---

# Decision Authority

OpenClaw MAY issue Decisions when authority has been delegated.

Typical Decisions include:

* Task Complete;
* Task Rejected;
* Additional Work Required;
* Retry Authorized;
* Human Approval Required;
* Goal Review Ready.

OpenClaw SHALL escalate to the Principal when:

* Goal intent is ambiguous;
* Success Criteria conflict;
* Constraints conflict;
* irreversible actions are required;
* risk exceeds delegated authority;
* human approval is explicitly required.

---

# Required Outputs

OpenClaw SHALL maintain:

* Goal status;
* Task list;
* Task state;
* Event references;
* Artifact references;
* Evidence Objects;
* Decision Objects;
* progress summaries.

---

# Minimum Viable Behavior

A minimally conforming OpenClaw implementation can:

1. Read a Goal from the Knowledge Repository.
2. Create one or more Tasks.
3. Publish Tasks to Redis.
4. Observe Executor results.
5. Assemble Evidence.
6. Issue a Decision.
7. Update the Goal status.

---

# Anti-Patterns

OpenClaw SHOULD avoid:

* executing its own delegated Tasks;
* hiding plans in conversational context only;
* treating Executor summaries as sufficient Evidence;
* creating vague Tasks;
* overwriting historical Events;
* allowing Redis state to become canonical Knowledge.

---

# Reference Flow

```text
Principal writes Goal
        ↓
OpenClaw reads Goal
        ↓
OpenClaw creates Tasks
        ↓
OpenClaw publishes Tasks to Redis
        ↓
Hermes claims and executes Tasks
        ↓
Hermes produces Events and Artifacts
        ↓
OpenClaw assembles Evidence
        ↓
OpenClaw issues Decision
        ↓
OpenClaw updates Knowledge Repository
```

---

# Conformance Mapping

OpenClaw conforms to MTH-021 if it:

* preserves Goal intent;
* coordinates rather than executes;
* creates valid Tasks;
* tracks Task state;
* assembles Evidence before completion;
* issues Decisions with accountability;
* updates durable Knowledge.

---

# Revision History

| Version | Date          | Notes             |
| ------- | ------------- | ----------------- |
| 0.1.0   | Initial draft | First publication |
