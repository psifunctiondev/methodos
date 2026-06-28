# Méthodos Specification

**Identifier:** MTH-032

**Title:** Artifact Protocol

**Version:** 0.1.0

**Status:** Draft

**Category:** Protocols

**Depends Upon:** MTH-013 Artifact, MTH-031 Task Protocol, MTH-035 Event Protocol

---

# Abstract

This specification defines the Artifact Protocol.

The Artifact Protocol governs the creation, identification, publication, management, and preservation of Artifacts produced during Goal execution.

Artifacts are durable outputs of execution.

Artifacts SHALL NOT themselves constitute Evidence or Decisions.

---

# Architectural Intent

Provide a consistent protocol for managing durable execution outputs while preserving traceability and implementation independence.

---

# Participants

| Participant          | Responsibility                           |
| -------------------- | ---------------------------------------- |
| Executor             | Produces Artifacts                       |
| Orchestrator         | References Artifacts                     |
| Knowledge Repository | Preserves Artifacts or stable references |
| Reviewer             | Inspects Artifacts                       |

---

# Artifact Characteristics

Artifacts SHALL be:

* durable;
* attributable;
* uniquely identifiable;
* traceable;
* immutable after publication where practical.

Artifacts represent outputs, not conclusions.

---

# Artifact Classes

Implementations MAY define additional Artifact types.

Typical examples include:

* source code
* documentation
* configuration
* test reports
* benchmark results
* logs
* shell transcripts
* images
* datasets
* models

---

# Artifact Lifecycle

```text id="9hny3g"
Created
    │
    ▼
Published
    │
    ▼
Referenced
    │
    ▼
Preserved
    │
    ▼
Archived
```

Artifacts SHOULD remain available for future inspection.

---

# Protocol

## Step 1 — Creation

An Executor or Participant produces an Artifact during execution.

The Artifact SHOULD receive:

* Artifact ID
* creator
* timestamp
* type
* originating Task

---

## Step 2 — Publication

The Artifact becomes available to other Participants.

Publication MAY consist of:

* storing the Artifact;
* publishing a stable reference;
* recording a content hash;
* recording a repository location.

---

## Step 3 — Notification

Publication SHOULD generate an Event.

The Event announces that an Artifact exists.

The Event SHALL NOT replace the Artifact.

---

## Step 4 — Reference

Tasks, Evidence, Decisions, and other Objects MAY reference the Artifact.

References SHOULD remain stable over time.

---

## Step 5 — Preservation

Artifacts SHOULD remain accessible throughout the lifetime of related Goals.

Historical Artifacts SHOULD remain recoverable.

---

## Step 6 — Archival

Artifacts MAY be archived after operational usefulness ends.

Archival SHALL preserve:

* identity;
* attribution;
* traceability;
* historical references.

---

# Artifact Integrity

Implementations SHOULD preserve Artifact integrity.

Suitable mechanisms include:

* content hashes;
* immutable storage;
* version control;
* digital signatures.

Integrity verification SHOULD be possible.

---

# Traceability

Every Artifact SHOULD be traceable to:

* originating Task;
* producing Participant;
* related Goal.

Evidence SHOULD reference Artifacts rather than duplicating their contents.

---

# Failure Handling

Artifact publication MAY fail.

Participants SHOULD:

* retry publication;
* preserve local copies where practical;
* report failures through Events.

Loss of an Artifact SHALL prevent dependent Evidence from being considered complete.

---

# Relationship to Other Objects

Artifacts are execution outputs.

Artifacts SHALL NOT:

* authorize completion;
* establish truth;
* replace Decisions.

Artifacts become useful when referenced by Evidence.

---

# Completion Conditions

An Artifact is considered complete when:

* published or stably referenced;
* uniquely identifiable;
* attributable;
* traceable to its originating Task.

No approval is required.

---

# Conformance

A conforming implementation SHALL:

* uniquely identify Artifacts;
* preserve traceability;
* support stable references;
* distinguish Artifacts from Evidence;
* preserve attribution.

---

# Normative Requirements

**MTH-032-REQ-001**

Artifacts SHALL represent durable execution outputs.

**MTH-032-REQ-002**

Artifacts SHALL NOT constitute Evidence.

**MTH-032-REQ-003**

Artifacts SHALL NOT constitute Decisions.

**MTH-032-REQ-004**

Artifacts SHALL remain traceable to their originating Task.

**MTH-032-REQ-005**

Evidence SHOULD reference Artifacts rather than duplicate them.

---

# Design Rationale

Artifacts preserve the products of execution.

By separating Artifacts from Evidence, Méthodos enables multiple independent Evidence packages to evaluate the same execution outputs while maintaining a clear distinction between observation and conclusion.

---

# Revision History

| Version | Date          | Notes             |
| ------- | ------------- | ----------------- |
| 0.1.0   | Initial draft | First publication |
