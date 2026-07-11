# Méthodos Dossier System Definition

**Dossier Type:** Goal Dossier  
**Framework Version:** 0.1  
**Status:** Active

---

# Purpose

This dossier is the canonical institutional record for a single Méthodos Goal or closely related Goal set.

It contains durable Objects, operational history, Evidence, Decisions, and related knowledge required to understand and govern work.

Transient coordination belongs outside this dossier.

---

# Canonical Locations

```text
Inbox/
Templates/
Goals/
Tasks/
Events/
Artifacts/
Evidence/
Decisions/
Architecture/
Research/
Meetings/
Daily-Notes/
```

Objects SHOULD be stored in their canonical locations.

---

# Canonical Goal States

```text
Draft
Ready
Planning
Active
Blocked
Review
Complete
Archived
```

`Ready` is the explicit Principal-to-Orchestrator handoff.

A Goal SHALL NOT be planned merely because it exists.

---

# Canonical Task States

```text
Draft
Ready
Assigned
Executing
Waiting
Blocked
Ready for Review
Accepted
Cancelled
Archived
```

Queues, claims, leases, reservations, and heartbeats are coordination mechanics and SHALL NOT be treated as canonical Task States.

---

# Canonical Evidence States

```text
Draft
Assembled
Reviewed
Accepted
Superseded
Archived
```

Accepted Evidence is immutable.

Corrections require new or superseding Evidence.

---

# Responsibility Domains

The Principal owns the Intent Envelope.

The Orchestrator is responsible for planning, coordination, Evidence planning, review preparation, and lifecycle management.

The Executor is responsible for execution notes and produced Artifacts.

The Reviewer is responsible for assigned review.

Participants SHALL NOT modify content outside their responsibility domain except through authorized Protocols.

---

# Intent Envelope Guidance

The Objective defines the desired end state.

Success Criteria define observable conditions of success.

Constraints define conditions that SHALL remain true.

Acceptance Criteria define observable validation conditions for closure and SHOULD support Evidence planning.

Assumptions identify propositions on which planning or execution relies.

Suggested Approaches are non-binding Principal guidance. They SHOULD NOT use `MUST`, `SHALL`, or `REQUIRED` to imply mandatory behavior.

Domain Definitions establish Goal-specific terminology, taxonomies, classifications, identifiers, or qualification rules.

The Orchestrator SHALL evaluate material Assumptions during Planning.

---

# Secret Handling

Secret Material SHALL NOT be stored in this Dossier.

This includes passwords, API keys, access tokens, session cookies, private keys, recovery codes, and other authentication credentials.

Objects MAY state that protected access is available and MAY identify an approved secret-management or delegated authentication mechanism.

Secret values SHALL NOT be copied into Goals, Tasks, Events, Artifacts intended as institutional records, Evidence, Decisions, templates, or this file.

If a secret is discovered in the Dossier:

1. do not reproduce or propagate it;
2. record the exposure without including the secret value;
3. notify the Principal or applicable security authority;
4. treat the credential as potentially compromised;
5. rotate or revoke it when appropriate.

Removing a secret from the current file does not guarantee removal from Git history, synchronization history, backups, logs, or indexes.

See `MTH-043 Security`.

---

# Evidence and Decisions

Artifacts are not Evidence.

Evidence is not a Decision.

Acceptance Criteria SHOULD seed Evidence Claims and validation planning.

State transitions requiring governance SHALL be traceable to a Final Decision.

---

# Coordination

This dossier is not the Coordination Fabric.

Short-lived state, including leases, queues, claims, reservations, and heartbeats, belongs outside this dossier.

---

# Startup Rule

Participants SHOULD read this file before acting within the dossier.
