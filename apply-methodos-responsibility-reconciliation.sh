#!/usr/bin/env bash
set -euo pipefail

ROOT="${1:-.}"
cd "$ROOT"

python3 <<'PY'
from pathlib import Path

def replace(path, old, new):
    p = Path(path)
    text = p.read_text()
    if old not in text:
        raise SystemExit(f"Expected text not found in {path}:\n{old}")
    p.write_text(text.replace(old, new))

# MTH-004 — remove universal ownership and define object-specific responsibility semantics.
p = "specification/foundation/MTH-004-Object-Model.md"
replace(p,
"Every Object possesses identity, ownership, state, relationships, and lifecycle.",
"Every Object possesses identity, state, relationships, and lifecycle.")
replace(p,
"""* Identifier
* Object Type
* Owner
* Current State""",
"""* Identifier
* Object Type
* Current State""")
replace(p,
"""# Ownership

Every Object SHALL possess exactly one current Owner.

Ownership MAY change through documented Protocols.

Ownership SHALL remain observable.""",
"""# Responsibility and Provenance

Méthodos Objects SHALL use object-specific responsibility and provenance semantics.

An Object specification SHALL identify the Roles, Participants, or provenance fields required to interpret authority and responsibility for that Object.

Responsibility-specific concepts include Principal, Orchestrator, Executor assignment, Reviewer, Creator, Steward, and Maintainer.

No universal `owner` property is implied by the Object Model.

Applicable responsibility assignments and provenance SHALL remain observable.""")
replace(p,
"""New Objects SHALL:

* define ownership,
* define lifecycle,""",
"""New Objects SHALL:

* define responsibility and provenance semantics where applicable,
* define lifecycle,""")
replace(p,
"""**MTH-004-REQ-002**

Every Object SHALL possess exactly one Owner.""",
"""**MTH-004-REQ-002**

Every Object specification SHALL explicitly define applicable responsibility and provenance semantics.""")
replace(p,
"* explicit ownership,",
"* explicit responsibility boundaries and provenance,")

# MTH-010 — Goal responsibility belongs to the Orchestrator; retain "ownership domains"
# only as a concept, but rename them responsibility domains.
p = "specification/kernel/MTH-010-Goal.md"
replace(p, "* Owner\n* Principal", "* Orchestrator\n* Principal")
replace(p,
"""# Ownership

Every Goal SHALL have exactly one Owner.

The Owner is responsible for maintaining the Goal's current status and ensuring that its Success Criteria remain coherent.

The Principal retains authority over intent even when operational ownership is delegated.""",
"""# Responsibility

Every Goal SHALL identify exactly one Orchestrator.

The Orchestrator is responsible for Goal lifecycle coordination, planning, Task decomposition, status maintenance, review preparation, and authorized Goal state transitions.

The Principal retains authority over the Intent Envelope. Assignment of an Orchestrator does not transfer authority over intent.""")
replace(p,
"""**MTH-010-REQ-002**

Every Goal SHALL have exactly one Owner.""",
"""**MTH-010-REQ-002**

Every Goal SHALL identify exactly one Orchestrator.""")
replace(p,
"Every durable Goal representation SHALL define ownership domains.",
"Every durable Goal representation SHALL define responsibility domains.")
replace(p, "owner:\nstate:", "orchestrator:\nstate:")
replace(p,
"By requiring explicit Success Criteria, ownership, constraints, and Evidence, Méthodos ensures that Goals remain actionable, reviewable, and recoverable.",
"By requiring explicit Success Criteria, responsibility boundaries, Constraints, and Evidence, Méthodos ensures that Goals remain actionable, reviewable, and recoverable.")
replace(p, "# Ownership Domains", "# Responsibility Domains")
replace(p,
"""A Goal SHALL define ownership domains for its durable representation.

Ownership domains identify which Participants are authorized to modify specific portions of a Goal.

Typical ownership domains include:""",
"""A Goal SHALL define responsibility domains for its durable representation.

Responsibility domains identify which Participants are authorized to modify specific portions of a Goal.

Typical responsibility domains include:""")
replace(p,
"""Participants SHALL NOT modify content outside their ownership domain except through an explicit Protocol.

Ownership domains protect Goal intent while allowing collaborative maintenance of operational state.""",
"""Participants SHALL NOT modify content outside their responsibility domain except through an explicit Protocol.

Responsibility domains protect Goal intent while allowing collaborative maintenance of operational state.""")

# MTH-012 — make Orchestrator mandatory, assignment optional, Executor a Role.
p = "specification/kernel/MTH-012-Task.md"
replace(p,
"""* Current State
* Executor
* Priority""",
"""* Current State
* Orchestrator
* Priority""")
replace(p,
"""* Assigned Participant
* Artifacts""",
"""* Assigned To
* Artifacts""")
replace(p,
"""A Task MAY be assigned to one Participant for execution.

`executor` identifies the Participant currently responsible for performing the Task. Assignment MAY change through the Task Protocol without changing the Task’s Orchestrator.""",
"""A Task MAY be assigned to one Participant acting as Executor.

`assigned_to` identifies the Participant currently responsible for performing the Task as Executor. Assignment MAY change through the Task Protocol without changing the Task's Orchestrator.""")
replace(p,
"* maintains observable ownership and traceability.",
"* maintains observable responsibility, assignment, and traceability.")
replace(p,
"* Multiple active Owners.",
"* Multiple simultaneous active Executors or claim holders for the same Task.")

# MTH-013 — Creator is provenance, not an ownership comparison.
p = "specification/kernel/MTH-013-Event.md"
replace(p,
"""# Ownership

Events have a Creator but not an Owner.

Once recorded, Events become part of the shared institutional history.

No Participant owns an Event after creation.""",
"""# Creator Provenance

Every Event SHALL preserve Creator provenance.

The Creator identifies the Participant or system component that recorded the occurrence.

Once recorded, Events become part of the shared institutional history.

Creator provenance does not grant authority to modify an Event.""")

# Decision template — explicit responsibility naming.
p = "dossier/Templates/decision.md"
replace(p,
"""| Action | Owner |
| ------ | ----- |""",
"""| Action | Responsible Participant |
| ------ | ----------------------- |""")

# Security spacing typos found by the audit.
p = Path("specification/governance/MTH-043-Security.md")
if p.exists():
    text = p.read_text()
    text = text.replace("aSecret Reference", "a Secret Reference")
    text = text.replace("thatSecret Material", "that Secret Material")
    p.write_text(text)
PY

echo
echo "Ownership/responsibility reconciliation applied."
echo
echo "Running checks..."
git diff --check

grep -RIn --exclude-dir=.git \
  '\bowner\b\|\bOwner\b\|\bowners\b\|\bOwners\b' \
  specification dossier schemas reference || true

for f in schemas/*.schema.json; do
  python3 -m json.tool "$f" >/dev/null || exit 1
done

echo "schemas valid"
echo
echo "Review with:"
echo "  git diff --stat"
echo "  git diff -- specification/foundation/MTH-004-Object-Model.md \\"
echo "    specification/kernel/MTH-010-Goal.md \\"
echo "    specification/kernel/MTH-012-Task.md \\"
echo "    specification/kernel/MTH-013-Event.md \\"
echo "    dossier/Templates/decision.md \\"
echo "    specification/governance/MTH-043-Security.md"
