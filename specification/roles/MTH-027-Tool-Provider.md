# Méthodos Specification

**Identifier:** MTH-027

**Title:** Tool Provider

**Status:** Draft

## Abstract

A Tool Provider realizes one or more Capabilities through concrete tools, APIs, services, or implementations.

## Architectural Intent

Separate implementation from semantics.

Capabilities describe *what* may be done.

Tool Providers describe *how* it is accomplished.

## Examples

Capability: filesystem.write

Providers:
- OpenClaw write_file()
- Claude Write Tool
- Human text editor

## Normative Requirements

- MTH-027-REQ-001: Tool Providers SHALL advertise supported Capabilities.
- MTH-027-REQ-002: Multiple Tool Providers MAY realize the same Capability.
- MTH-027-REQ-003: Tasks SHALL depend upon Capabilities, not Tool Providers.
- MTH-027-REQ-004: Tool Providers SHALL remain replaceable without changing Task semantics.
