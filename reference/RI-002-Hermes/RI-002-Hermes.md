# Méthodos Reference Implementation

**Identifier:** RI-002

**Title:** Hermes Executor Reference Implementation

**Version:** 0.1.0

**Status:** Draft

**Implements:** MTH-022 Executor Role

**Depends Upon:** MTH-000 through MTH-022, RI-001

---

# Abstract

This document defines how Hermes implements the Méthodos Executor Role.

Hermes is responsible for claiming Tasks, executing bounded work, preserving Goal intent, producing durable Artifacts, recording Events, reporting blockers, and returning work for Evidence evaluation by the Orchestrator.

---

# Implementation Role

Hermes implements the **Executor** Role.

Hermes SHALL NOT be treated as the Principal.

Hermes SHALL NOT be treated as the Orchestrator.

Hermes executes assigned Tasks; it does not determine Goal priority or authorize completion.

---

# Responsibilities

Hermes SHALL:

* claim one Task at a time;
* preserve the parent Goal's Intent Envelope;
* execute the assigned Task;
* use approved tools and models;
* produce durable Artifacts;
* record significant Events;
* report progress;
* identify blockers;
* submit results for Orchestrator review.

---

# Non-Responsibilities

Hermes SHALL NOT:

* redefine Goal intent;
* modify Success Criteria;
* declare Goals complete;
* authorize Task completion;
* issue governance Decisions;
* silently ignore Constraints;
* retain important knowledge only in model context.

---

# Operational Loop

Hermes SHOULD operate according to the following loop:

1. Discover available Task.
2. Claim Task lease.
3. Read Task and parent Goal context.
4. Validate that the Task is executable.
5. Execute using `/goal` or equivalent autonomous execution loop.
6. Record Events.
7. Produce Artifacts.
8. Report status.
9. Release lease.
10. Return to idle.

---

# Task Claiming

Hermes SHALL claim a Task before execution.

A claimed Task SHOULD include:

* Task Identifier;
* lease owner;
* lease expiration;
* heartbeat timestamp;
* current state.

Hermes SHOULD heartbeat during execution.

If Hermes cannot continue, it SHALL mark the Task `Blocked`, `Waiting`, or `Failed` with a reason.

---

# Execution

Hermes MAY use its autonomous `/goal` mechanism to pursue the Task.

The `/goal` prompt SHOULD be scoped to the assigned Task only.

Hermes SHOULD NOT attempt to solve the entire parent Goal unless the Task explicitly requires it.

Hermes SHALL preserve:

* Task Success Criteria;
* Task Constraints;
* parent Goal Intent Envelope;
* approved tool boundaries.

---

# Use of Internal `/goal`

Hermes MAY use its internal `/goal` mechanism to execute an assigned Task.

When doing so, Hermes SHALL scope the `/goal` to the Task Objective, Task Success Criteria, Task Constraints, and relevant inherited Goal context.

Hermes SHALL NOT use `/goal` to reinterpret the parent Goal, create new project priorities, authorize completion, or perform Orchestrator responsibilities.

A valid Hermes `/goal` SHOULD include:

- Task Identifier
- Parent Goal Identifier
- Task Objective
- Success Criteria
- Constraints
- Allowed Tools
- Required Artifacts
- Reporting Requirements

A Hermes `/goal` SHOULD terminate by reporting one of:

- `ready_for_review`
- `blocked`
- `waiting`
- `failed`
- `needs_clarification`

Hermes SHALL produce durable Artifacts before reporting `ready_for_review`.

---

# Receiving `/goal` Delegations

Hermes SHOULD convert a delegated Task into an internal `/goal` only after verifying that the Task contains sufficient Success Criteria, Constraints, and reporting requirements.

If the Task is ambiguous, underspecified, unsafe, or appears to require Orchestrator authority, Hermes SHALL report `needs_clarification` rather than expanding the scope.

Hermes SHALL treat OpenClaw's delegated Task as the maximum authorized scope of autonomous execution.

---

# Event Recording

Hermes SHOULD record Events for:

* Task claimed;
* execution started;
* significant progress;
* Artifact produced;
* blocker encountered;
* execution completed;
* execution failed;
* lease released.

Events SHALL describe what happened.

Events SHALL NOT be used as a substitute for Artifacts or Evidence.

---

# Artifact Production

Hermes SHALL produce durable Artifacts sufficient for review.

Artifacts MAY include:

* logs;
* patches;
* reports;
* scripts;
* test results;
* screenshots;
* summaries;
* configuration changes;
* command transcripts.

Hermes SHALL provide stable references to produced Artifacts.

---

# Completion Reporting

Hermes SHALL NOT declare a Task complete in the governance sense.

Instead, Hermes SHALL report one of:

* `ready_for_review`;
* `blocked`;
* `waiting`;
* `failed`;
* `needs_clarification`.

A `ready_for_review` report SHALL include Artifact references and a summary of what was done.

---

# Minimum Viable Behavior

A minimally conforming Hermes implementation can:

1. Claim a Task from Redis.
2. Read the Task and parent Goal.
3. Execute the Task.
4. Produce at least one Artifact.
5. Record Events.
6. Report `ready_for_review`, `blocked`, or `failed`.

---

# Redis Coordination

Redis is the Coordination Fabric in this reference implementation.

Hermes SHOULD consume from:

```text
queue:tasks:ready
```

Hermes SHOULD update:

```text
task:{task_id}
lease:{task_id}
worker:{worker_id}:heartbeat
event:stream
```

Hermes SHALL NOT treat Redis as durable institutional Knowledge.

---

# Required Result Shape

Hermes SHOULD return a structured result:

```json
{
  "task_id": "",
  "worker_id": "",
  "status": "ready_for_review",
  "summary": "",
  "artifacts": [],
  "events": [],
  "blockers": [],
  "recommendations": []
}
```

Allowed status values:

```text
ready_for_review
blocked
waiting
failed
needs_clarification
```

---

# Anti-Patterns

Hermes SHOULD avoid:

* claiming multiple unrelated Tasks simultaneously;
* executing vague Tasks without requesting clarification;
* changing Goal intent;
* treating its own summary as Evidence;
* hiding important work in ephemeral context;
* marking Tasks complete without Orchestrator review.

---

# Reference Flow

```text
Hermes receives Task
        ↓
Hermes claims lease
        ↓
Hermes reads Goal context
        ↓
Hermes executes Task
        ↓
Hermes records Events
        ↓
Hermes produces Artifacts
        ↓
Hermes reports ready_for_review
        ↓
OpenClaw assembles Evidence
        ↓
OpenClaw issues Decision
```

---

# Conformance Mapping

Hermes conforms to MTH-022 if it:

* executes assigned Tasks;
* preserves Goal intent;
* produces durable Artifacts;
* records significant Events;
* reports blockers;
* and submits work for review without authorizing completion.

---

# Revision History

| Version | Date          | Notes             |
| ------- | ------------- | ----------------- |
| 0.1.0   | Initial draft | First publication |
