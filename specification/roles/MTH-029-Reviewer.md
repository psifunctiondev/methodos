# Méthodos Specification

**Identifier:** MTH-029

**Title:** Reviewer

**Version:** 0.1.0

**Status:** Draft

**Category:** Roles

**Depends Upon:** MTH-014 through MTH-016, MTH-036 Approval Protocol

---

# Abstract

This specification defines the Reviewer Role.

A Reviewer independently evaluates work products, Evidence, and proposed Decisions to determine whether they satisfy defined requirements.

Reviewers improve quality and governance while remaining independent of execution.

---

# Architectural Intent

Provide independent assessment before significant state transitions occur.

---

# Purpose

The Reviewer evaluates whether completed work satisfies the Principal's Intent Envelope and the applicable Success Criteria.

Review focuses on quality, correctness, completeness, compliance, and risk.

---

# Responsibilities

A Reviewer MAY:

* inspect Artifacts;
* evaluate Evidence;
* assess Success Criteria;
* recommend acceptance;
* recommend rejection;
* request additional work;
* request additional Evidence;
* provide Approval where authorized.

---

# Non-Responsibilities

A Reviewer SHALL NOT:

* execute Tasks;
* redefine Goals;
* modify the Intent Envelope;
* produce implementation Artifacts on behalf of Executors;
* assume Orchestrator responsibilities unless explicitly delegated.

---

# Review Outcomes

A review SHOULD result in one of:

* Accepted
* Accepted with Recommendations
* Rework Required
* Rejected
* Needs More Evidence
* Needs Clarification

Review outcomes SHOULD be attributable.

---

# Relationships

The Reviewer primarily interacts with:

* Artifacts
* Evidence
* Decisions
* Approval Protocol
* Goal Protocol
* Task Protocol

---

# Conformance

A conforming Reviewer SHALL:

* perform independent assessment;
* preserve traceability;
* distinguish Evidence from Decisions;
* preserve object ownership boundaries.

---

# Normative Requirements

**MTH-029-REQ-001**

Reviewers SHALL evaluate work against the Intent Envelope and applicable Success Criteria.

**MTH-029-REQ-002**

Reviewers SHALL distinguish observations from recommendations.

**MTH-029-REQ-003**

Reviewers SHALL NOT modify canonical Objects outside their authority.

**MTH-029-REQ-004**

Reviewer recommendations SHALL NOT constitute Final Decisions unless explicitly authorized.

---

# Design Rationale

Execution and evaluation are intentionally separated.

Independent review improves quality, reduces confirmation bias, and strengthens governance by ensuring that work is assessed against objective criteria rather than solely by its producer.

---

# Reference Implementation Notes

Possible Reviewer implementations include:

* architecture reviewers;
* code review agents;
* security reviewers;
* compliance reviewers;
* quality assurance agents;
* human subject-matter experts.

---

# Revision History

| Version | Date          | Notes             |
| ------- | ------------- | ----------------- |
| 0.1.0   | Initial draft | First publication |
