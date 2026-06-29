# Méthodos Specification

**Identifier:** MTH-014

**Title:** Artifact Object

**Version:** 0.1.0

**Status:** Draft

**Category:** Kernel

**Depends Upon:** MTH-000 through MTH-012

---

# Abstract

This specification defines the Artifact Object.

Artifacts are durable outputs produced during the execution of work.

Artifacts preserve the products of execution independently of the Participants that created them.

---

# Architectural Intent

Preserve the durable products of execution.

---

# Purpose

Artifacts capture what execution produced.

Unlike Events, which record that something occurred, Artifacts represent the actual outputs of work.

Artifacts form the raw material from which Evidence may later be constructed.

---

# Definition

An Artifact is a durable Object created during or as a result of execution.

Artifacts SHALL remain available after execution completes unless explicitly removed according to a retention policy outside the scope of this specification.

Artifacts do not by themselves prove correctness.

---

# Required Properties

Every Artifact SHALL contain:

* Identifier
* Artifact Type
* Title
* Creator
* Creation Timestamp
* Storage Location
* Content Reference
* Related Object Identifier
* Metadata

---

# Artifact Types

Typical Artifact types include:

* Source Code
* Patch
* Document
* Report
* Log
* Test Result
* Screenshot
* Image
* Audio
* Video
* Dataset
* Configuration
* Transcript

Implementations MAY define additional Artifact types.

---

# Relationships

Artifacts MAY be produced by:

* Tasks
* Participants
* Sessions

Artifacts MAY contribute to:

* Evidence
* Decisions
* Knowledge

Artifacts SHALL reference at least one related Object.

---

# Ownership

Artifacts have a Creator.

Administrative ownership MAY be assigned according to implementation requirements.

Artifacts become part of the institutional Knowledge Repository.

---

# Lifecycle

Artifacts SHALL occupy one of the following States:

* Created
* Stored
* Referenced
* Archived

Implementations MAY define additional non-conflicting States.

---

# Durability

Artifacts SHALL be durable.

Temporary execution files that are discarded before becoming institutional knowledge are not Artifacts.

---

# Accessibility

Artifacts SHOULD remain retrievable through stable references.

Implementations MAY relocate physical storage provided references remain valid.

---

# Invariants

The following SHALL always remain true:

* Every Artifact has one Identifier.
* Every Artifact has one Creator.
* Every Artifact references at least one Object.
* Every Artifact possesses a durable representation.
* Every Artifact remains independently retrievable.

---

# Conformance

An implementation conforms to this specification if every Artifact:

* possesses the required properties,
* has a durable representation,
* references one or more related Objects,
* and remains independently retrievable.

---

# Normative Requirements

**MTH-014-REQ-001**

Every Artifact SHALL have a stable Identifier.

**MTH-014-REQ-002**

Every Artifact SHALL reference at least one related Object.

**MTH-014-REQ-003**

Artifacts SHALL possess a durable representation.

**MTH-014-REQ-004**

Artifacts SHALL remain independently retrievable.

**MTH-014-REQ-005**

Artifacts SHALL NOT be treated as Evidence without explicit evaluation.

---

# Anti-Patterns

The following behaviors are non-conforming or discouraged:

* Treating transient execution files as Artifacts.
* Assuming every Artifact proves correctness.
* Embedding institutional knowledge solely in execution logs.
* Creating Artifacts that cannot be referenced.
* Deleting Artifacts required by active Goals.

---

# Design Rationale

Artifacts preserve the products of execution.

They intentionally remain distinct from Events, which record occurrences, and Evidence, which supports claims.

This separation allows implementations to retain execution outputs without prematurely asserting correctness.

---

# Future Directions

Future specifications will define:

* Artifact Protocol
* Artifact Storage
* Artifact Versioning
* Artifact Retention
* Artifact Indexing

---

# Revision History

| Version | Date          | Notes             |
| ------- | ------------- | ----------------- |
| 0.1.0   | Initial draft | First publication |
