# Méthodos Specification

**Identifier:** MTH-025

**Title:** Inference Router Role

**Version:** 0.1.0

**Status:** Draft

**Category:** Roles

**Depends Upon:** MTH-000 through MTH-016, MTH-020 through MTH-022

---

# Abstract

This specification defines the Inference Router Role.

The Inference Router provides Participants with access to inference capabilities while insulating them from provider-specific implementation details, model availability, fallback behavior, routing policy, and operational configuration.

The Inference Router is a shared service. Multiple Participants may independently consume the same Inference Router without routing requests through one another.

---

# Architectural Intent

Separate requested reasoning capability from concrete model implementation.

---

# Purpose

The Inference Router exists to let Participants request inference by capability rather than by provider or model identity.

It enables:

* shared model access;
* capability-based routing;
* provider abstraction;
* fallback;
* cost management;
* operational telemetry;
* model replacement;
* experimental routing;
* local and remote inference unification.

The Inference Router allows the system to evolve its model stack without requiring architectural changes to Participants.

---

# Role Definition

An Inference Router is a Participant-facing service that receives inference requests, applies routing policy, selects an appropriate inference implementation, and returns results through a consistent interface.

The Inference Router does not own Goals, Tasks, Evidence, Decisions, or institutional Knowledge.

---

# Responsibilities

The Inference Router SHALL:

* expose a consistent inference interface;
* route requests to appropriate Inference Engines;
* abstract provider-specific APIs;
* support capability-based request patterns;
* support model aliasing;
* support fallback where configured;
* expose operational telemetry;
* preserve caller independence;
* maintain routing configuration outside individual Participants.

---

# Non-Responsibilities

The Inference Router SHALL NOT:

* create Goals;
* decompose Goals into Tasks;
* execute Tasks;
* assemble Evidence;
* issue Decisions;
* preserve institutional Knowledge;
* replace the Coordination Fabric;
* replace the Knowledge Repository.

---

# Shared Service Model

The Inference Router SHALL be treated as shared infrastructure.

The Orchestrator and Executor MAY both consume the same Inference Router directly.

The Orchestrator SHALL NOT be required to proxy inference requests for the Executor.

The Executor SHALL NOT be required to proxy inference requests for the Orchestrator.

This preserves peer independence between Participants.

---

# Capability-Based Routing

Participants SHOULD request inference by capability.

Examples of capabilities include:

* planning;
* orchestration;
* execution;
* coding;
* summarization;
* vision;
* classification;
* embedding;
* translation;
* review;
* long-context reasoning;
* low-latency response;
* low-cost response.

Implementations MAY map capabilities to aliases, tiers, models, providers, or routing policies.

---

# Alias-Based Routing

An Inference Router MAY expose stable aliases.

Aliases SHOULD represent durable intent rather than transient provider choices.

Examples include:

* `tier/heartbeat`
* `tier/nano`
* `tier/fast`
* `tier/general`
* `tier/code`
* `tier/code-big`
* `tier/vision`
* `tier/smart`
* `tier/genius`

Aliases SHOULD remain stable even when their backing providers change.

---

# Provider Abstraction

The Inference Router MAY route requests to:

* local inference engines;
* cloud inference providers;
* frontier model APIs;
* serverless endpoints;
* specialized model services;
* wildcard provider routes;
* future inference systems.

Participants SHOULD NOT contain provider-specific routing logic.

---

# Fallback

The Inference Router SHOULD support fallback where practical.

Fallback policies MAY account for:

* provider availability;
* model errors;
* latency;
* cost;
* context length;
* tool support;
* capability match;
* caller requirements.

Fallback SHALL preserve the requested capability as closely as possible.

Fallback SHALL NOT silently change semantics in a way that violates caller constraints.

---

# Context and Capability Metadata

The Inference Router SHOULD maintain metadata describing capabilities and constraints of available inference implementations.

Metadata MAY include:

* context window;
* maximum input tokens;
* maximum output tokens;
* tool support;
* vision support;
* reasoning behavior;
* streaming support;
* provider identity;
* expected latency;
* cost class;
* local or remote execution.

Metadata SHOULD reflect operational reality rather than aspirational limits.

---

# Endpoint Semantics

The Inference Router MAY expose multiple protocol surfaces.

Examples include:

* OpenAI-compatible chat completions;
* Anthropic-compatible messages;
* embedding endpoints;
* provider-specific compatibility surfaces.

Participants SHOULD use the endpoint semantics required by the requested capability.

Implementations SHALL document endpoint requirements when incorrect endpoint usage changes behavior.

---

# Routing Policy

Routing policy MAY consider:

* requested capability;
* caller identity;
* task type;
* cost;
* latency;
* context length;
* tool-use requirements;
* model availability;
* reliability;
* privacy;
* local-first preference;
* explicit Principal policy.

Routing policy SHOULD be externalized from Participants.

---

# Telemetry

The Inference Router SHOULD expose telemetry sufficient for operations and review.

Telemetry MAY include:

* selected route;
* provider used;
* latency;
* token counts;
* fallback attempts;
* errors;
* retries;
* cache behavior;
* cost estimates.

Telemetry is operational information.

Telemetry SHALL NOT replace institutional Knowledge.

---

# Configuration Management

Inference Router configuration SHOULD be version controlled.

Configuration changes SHOULD be reviewable.

Configuration changes affecting major routing behavior SHOULD be recorded as Events or Decisions when they materially affect Goals or Tasks.

---

# Security

The Inference Router SHOULD centralize provider credentials.

Participants SHOULD NOT require direct access to provider credentials unless explicitly justified.

The Inference Router SHOULD support access controls appropriate to the deployment.

---

# Invariants

The following SHALL always remain true:

* Participants request inference through documented interfaces.
* Provider details remain abstracted from Participants.
* Routing policy is external to individual Participants.
* The Inference Router does not own Goals or Tasks.
* The Inference Router does not issue Decisions.
* Multiple Participants may independently consume the same router.

---

# Conformance

An implementation conforms to this specification if it:

* provides a consistent inference interface;
* routes requests to appropriate inference implementations;
* abstracts provider-specific details;
* supports stable aliases or capability mappings;
* supports shared use by multiple Participants;
* and remains separate from orchestration, execution, and institutional Knowledge.

---

# Normative Requirements

**MTH-025-REQ-001**

The Inference Router SHALL abstract provider-specific inference details from Participants.

**MTH-025-REQ-002**

The Inference Router SHALL NOT own Goals, Tasks, Evidence, or Decisions.

**MTH-025-REQ-003**

The Inference Router SHALL support shared use by independent Participants.

**MTH-025-REQ-004**

Participants SHOULD request inference by capability or stable alias rather than hardcoded provider identity.

**MTH-025-REQ-005**

Routing policy SHOULD be externalized from Participants.

**MTH-025-REQ-006**

Fallback SHALL preserve requested capability as closely as possible.

**MTH-025-REQ-007**

Operational metadata SHOULD reflect observed deployment constraints.

---

# Anti-Patterns

The following behaviors are non-conforming or discouraged:

* Hardcoding provider-specific model names inside Participants.
* Routing Executor inference through the Orchestrator unnecessarily.
* Treating the Inference Router as the Coordination Fabric.
* Treating inference telemetry as institutional Knowledge.
* Allowing fallback to silently violate requested capability.
* Maintaining stale context-window or capability metadata.
* Mixing orchestration policy with provider-specific configuration.

---

# Design Rationale

Méthodos separates reasoning capability from reasoning implementation.

This allows Participants such as Orchestrators and Executors to request the kind of reasoning they require without depending on a specific provider, model, endpoint, or deployment topology.

The same Participant may use different capabilities for different work.

The same capability may be fulfilled by different implementations over time.

This separation supports local-first inference, cloud fallback, frontier model routing, experimentation, cost control, and future model replacement without changing the surrounding architecture.

---

# Reference Implementation Notes

LiteLLM is the first reference implementation of this Role.

The current reference implementation demonstrates:

* stable `tier/*` aliases;
* local Ollama routing;
* cloud fallback;
* frontier model access;
* OpenRouter-backed compatibility aliases;
* endpoint-specific model behavior;
* provider wildcard routes;
* per-model context metadata;
* cache behavior for supported providers;
* fallback chains;
* shared use by both Orchestrator and Executor implementations.

These details belong to the LiteLLM Reference Implementation and SHALL NOT be treated as normative requirements of the Inference Router Role.

---

# Future Directions

Future specifications may define:

* Capability Registry;
* Inference Request Object;
* Inference Result Object;
* Routing Policy Object;
* Provider Health Protocol;
* Model Evaluation Protocol;
* Cost Governance Protocol;
* Inference Audit Protocol.

---

# Revision History

| Version | Date          | Notes             |
| ------- | ------------- | ----------------- |
| 0.1.0   | Initial draft | First publication |
