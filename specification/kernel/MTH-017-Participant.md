# Méthodos Specification

**Identifier:** MTH-017

**Title:** Participant

**Status:** Draft

## Abstract

A Participant is any autonomous or directed actor capable of participating in a Méthodos Session.

Participants perform Roles, possess Capabilities, and interact with other Participants through Protocols.

## Principles

- Identity is stable.
- Roles are assumed and released.
- Capabilities may change over time.
- Participants are implementation-independent.

## Properties

- Identifier
- Display Name
- Participant Type
- Current Roles
- Capabilities
- Status
- Metadata

## Examples

- Human
- OpenClaw
- Hermes
- External Service
- Scheduled Automation

## Normative Requirements

- MTH-017-REQ-001: Every Participant SHALL have a stable Identifier.
- MTH-017-REQ-002: Participants SHALL possess zero or more Capabilities.
- MTH-017-REQ-003: Participants MAY perform multiple Roles.
- MTH-017-REQ-004: Participant identity SHALL be independent of Role.
