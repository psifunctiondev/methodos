# Méthodos Specification

**Identifier:** MTH-019

**Title:** Capability

**Status:** Draft

## Abstract

A Capability is an implementation-independent ability possessed by a Participant and potentially required by a Task.

Capabilities are contracts. Tool Providers realize those contracts.

## Example Capabilities

- filesystem.read
- filesystem.write
- shell.execute
- git.read
- git.write
- llm.reason
- llm.code
- web.search
- redis.publish
- tool.invoke

## Normative Requirements

- MTH-019-REQ-001: Capabilities SHALL be implementation-independent.
- MTH-019-REQ-002: Tasks MAY require Capabilities.
- MTH-019-REQ-003: Participants MAY possess Capabilities.
- MTH-019-REQ-004: Tool Providers SHALL realize Capabilities.
