
# Méthodos Repository Structure (v0.1)

```text
methodos/
│
├── README.md
├── LICENSE
├── CHANGELOG.md
├── ROADMAP.md
├── CONTRIBUTING.md
│
├── specification/
│   ├── foundation/
│   ├── kernel/
│   ├── roles/
│   ├── protocols/
│   ├── governance/
│   └── appendix/
│
├── reference/
│   ├── RI-001-OpenClaw/
│   ├── RI-002-Hermes/
│   ├── RI-003-Redis/
│   ├── RI-004-Obsidian/
│   ├── RI-005-LiteLLM/
│   └── RI-006-OpenWebUI/
│
├── schemas/
│
├── diagrams/
│   ├── topology/
│   ├── sequence/
│   ├── state-machines/
│   └── object-model/
│
├── vault/
│   ├── SYSTEM.md
│   │
│   ├── Inbox/
│   │
│   ├── Templates/
│   │
│   ├── Goals/
│   ├── Tasks/
│   ├── Events/
│   ├── Artifacts/
│   ├── Evidence/
│   ├── Decisions/
│   │
│   ├── Architecture/
│   ├── Research/
│   ├── Meetings/
│   └── Daily Notes/
│
├── examples/
│
├── experiments/
│
└── notes/
```

## Purpose of Top-Level Directories

| Directory        | Purpose                                                                             |
| ---------------- | ----------------------------------------------------------------------------------- |
| `specification/` | Normative Méthodos standard (MTH documents).                                        |
| `reference/`     | Reference implementations (RI documents).                                           |
| `schemas/`       | JSON/YAML schemas for canonical objects.                                            |
| `diagrams/`      | Architecture, topology, sequence and state-machine diagrams.                        |
| `vault/`         | Canonical Méthodos Knowledge Repository structure.                                  |
| `examples/`      | Worked examples and sample workflows.                                               |
| `experiments/`   | Prototypes and exploratory work outside the specification.                          |
| `notes/`         | Temporary design notes and working material not yet incorporated into the standard. |

This directory structure is considered **frozen for Méthodos v0.1** and should remain stable unless implementation experience demonstrates a compelling need for change.
