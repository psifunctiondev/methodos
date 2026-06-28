# Méthodos Reference Implementation

**Identifier:** RI-005

**Title:** LiteLLM Inference Router Reference Implementation

**Version:** 0.1.0

**Status:** Draft

**Implements:** Inference Router

**Depends Upon:** MTH-000 through MTH-022

---

# Abstract

This document defines LiteLLM as the reference implementation of the Méthodos Inference Router.

LiteLLM provides a unified interface to heterogeneous inference providers while abstracting model selection, routing, fallback, and provider-specific implementation details from other Participants.

---

# Architectural Intent

Separate inference capability from inference implementation.

---

# Purpose

The Inference Router exists to provide Participants with reasoning capabilities without coupling them to specific language models or providers.

Participants request capabilities.

The router selects implementations.

---

# Responsibilities

LiteLLM SHALL:

* expose a unified inference API;
* route requests to appropriate providers;
* abstract provider-specific interfaces;
* perform model selection;
* support fallback;
* expose consistent authentication;
* provide inference telemetry.

---

# Non-Responsibilities

LiteLLM SHALL NOT:

* orchestrate Goals;
* execute Tasks;
* preserve institutional Knowledge;
* issue Decisions;
* coordinate Participants.

---

# Architectural Position

LiteLLM occupies the Inference Plane.

It is consumed by:

* OpenClaw
* Hermes
* future Participants

It does not consume Goals or Tasks directly.

---

# Capability-Based Routing

Participants SHOULD request capabilities rather than specific models.

Examples include:

* Planning
* Coding
* Vision
* Summarization
* Embedding
* Translation
* OCR
* Reasoning

The Inference Router SHALL resolve capabilities to available implementations.

---

# Provider Abstraction

Implementations MAY include:

* frontier APIs;
* local inference servers;
* Ollama;
* vLLM;
* serverless endpoints;
* future providers.

Participants SHALL remain unaware of provider-specific details.

---

# Routing Policies

Routing MAY consider:

* capability;
* latency;
* cost;
* model availability;
* context window;
* reliability;
* user preference;
* organizational policy.

Implementations MAY define additional routing policies.

---

# Fallback

When an inference provider is unavailable, LiteLLM SHOULD select an alternative capable provider whenever practical.

Fallback SHALL preserve requested capability whenever possible.

---

# Telemetry

LiteLLM SHOULD expose:

* request latency;
* provider selection;
* token usage;
* failures;
* retries;
* routing decisions.

Telemetry SHOULD support operational analysis without becoming institutional Knowledge.

---

# Configuration

Routing configuration SHOULD remain external to Participants.

Participants SHOULD NOT contain provider-specific logic.

---

# Conformance

A conforming LiteLLM implementation:

* provides capability-based routing;
* abstracts providers;
* supports fallback;
* exposes a unified API;
* remains independent of orchestration logic.

---

# Design Rationale

Separating inference routing from Participants allows the system to evolve independently of individual models.

OpenClaw and Hermes become consumers of reasoning capabilities rather than consumers of particular language models.

This enables provider replacement, experimentation, optimization, and cost management without architectural change.

---

# Shared Service

LiteLLM is a shared infrastructure service.

OpenClaw and Hermes are independent clients of the Inference Router.

Neither Participant proxies inference requests on behalf of the other.

Both SHOULD use the same routing policies, capability definitions, authentication mechanisms, and telemetry infrastructure.

OpenClaw and Hermes are independent LiteLLM clients; LiteLLM is shared infrastructure, not a bridge between them.

---

# Future Directions

Future versions may include:

* dynamic capability negotiation;
* policy-driven routing;
* semantic caching;
* distributed routing;
* multi-model ensembles;
* confidence-based routing.

---

# Revision History

| Version | Date          | Notes             |
| ------- | ------------- | ----------------- |
| 0.1.0   | Initial draft | First publication |
