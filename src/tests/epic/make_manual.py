"""Writes the manual-only fixtures for SPEC-004 VER-13 (docs/runbooks/epic-ver-13-checks.md) as
src/tests/epic/manual/<name>/scaffold.sh. Every fixture is a variant of make_evals.py's shared fixture and is
validated against src/schemas/ first, as the eval cases are. Run from the repository root:

    python3 src/tests/epic/make_manual.py
"""
import importlib.util
import os
from pathlib import Path

spec = importlib.util.spec_from_file_location("make_evals", Path(__file__).with_name("make_evals.py"))
ev = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ev)

OUT = Path("src/tests/epic/manual")
P_ARCH2 = "docs/specs/arch/ARCH-002.md"


def arch2(*, supersedes):
    """ARCH-002: the same architecture written again as a separate document (VER-13 (c) and (j))."""
    text = ev.ARCH.replace("ARCH-001", "ARCH-002").replace(
        'system: "Riverside Food Bank volunteer shift sign-up"',
        'system: "Riverside Food Bank volunteer shift sign-up (second description)"')
    if supersedes:
        text = ev.replace(text, "supersedes: []", "supersedes: [ARCH-001]")
    return text


# (c) Two active ARCHs cite PRD-001 at its version: the skill lists both and asks.
TWO_ARCHS = dict(ev.SHARED, **{P_ARCH2: arch2(supersedes=False)})

# (j) ARCH-001 is superseded by ARCH-002, which cites PRD-001 at its version: the skill uses ARCH-002 without asking.
ARCH1_SUPERSEDED = ev.replace(ev.ARCH, "status: approved", "status: superseded")
ARCH1_SUPERSEDED = ev.replace(ARCH1_SUPERSEDED, "superseded_by: null", "superseded_by: ARCH-002")
SUPERSEDED_ARCH = dict(ev.SHARED, **{ev.P_ARCH: ARCH1_SUPERSEDED, P_ARCH2: arch2(supersedes=True)})

# (k) POL-001 v2 changes SET-01's platform; ARCH-001 still links SET-01 at version 1 and records the old platform.
NEW_PLATFORM = "Network-hosted mail service (HTTPS API)"
POL_CHANGED = ev.policy("active", version=2).replace(f'platform: "{ev.MAIL_PLATFORM}"', f'platform: "{NEW_PLATFORM}"')
POL_CHANGED = ev.replace(POL_CHANGED, "| Added SET-02 (testing.coverage_threshold) | SET-02 |",
                         "| SET-01 moves to the network-hosted mail service; added SET-02 | SET-01, SET-02 |")
PLATFORM_CHANGED = dict(ev.SHARED, **{ev.P_POL: POL_CHANGED})

# (i) PRD-001 v3 changes only FR-004's priority (could to should): ARCH-001 still cites v2, so the skill stops (ERR-03)
# until the architecture skill records a reuse review against v3.
PRD_V3 = ev.replace(ev.PRD, "status: approved\nversion: 2", "status: approved\nversion: 3")
PRD_V3 = ev.replace(PRD_V3, "updated: 2026-09-18", "updated: 2026-09-26")
PRD_V3 = ev.replace(PRD_V3, "approved_on: 2026-09-18", "approved_on: 2026-09-26")
PRD_V3 = ev.replace(
    PRD_V3, "phone's calendar.\"\n    priority: could", "phone's calendar.\"\n    priority: should")
PRD_V3 = ev.replace(PRD_V3, "| 2 | 2026-09-18 | Priya Nair | Approved | status |\n",
                    "| 2 | 2026-09-18 | Priya Nair | Approved | status |\n"
                    "| 3 | 2026-09-26 | Priya Nair | FR-004's priority from could to should | FR-004 |\n"
                    "| 3 | 2026-09-26 | Priya Nair | Approved | status |\n")
# The eval ARCH breaks the architecture skill's self-checks on purpose (DEC-03 resolved by the superseded ADR-002,
# DEC-05 by the missing ADR-004, no DEC for FR-009's marker), so a reuse review would fail validation and clear
# ARCH-001's approval. (i) needs an ARCH the architecture skill accepts: those questions open, a DEC for each
# marker, and the evidence classified as its inspection rules say. The eligible set stays FR-002, FR-003, FR-004,
# FR-012 and NFR-001.
ARCH_CLEAN = ev.arch(2, extra_dec=ev.dec(
    "08", "How is the volunteer list imported from the coordinator's spreadsheet and kept in step with it?", "open",
    "[]", "FR-009") + ev.dec("09", "Which payment provider takes membership fees?", "open", "[]", "FR-010"))
ARCH_CLEAN = ev.replace(ARCH_CLEAN, "state: resolved\n    resolved_by: [ADR-002]", "state: open\n    resolved_by: []")
ARCH_CLEAN = ev.replace(ARCH_CLEAN, "state: resolved\n    resolved_by: [ADR-004]", "state: open\n    resolved_by: []")
ARCH_CLEAN = ev.replace(
    ARCH_CLEAN, 'finding: "Version 1, status accepted: reminders go through the on-premises SMS modem."\n'
                "    classification: decided",
    'finding: "Version 1, status superseded by ADR-003: reminders went through the on-premises SMS modem."\n'
    "    classification: context")
ARCH_CLEAN = ev.replace(ARCH_CLEAN, ev.evd(
    "05", "ADR-004", "adr", "Version 1, status accepted: monthly hours are uploaded as a CSV file to the "
    "regional network's portal.", "decided"), "")
PRD_PRIORITY_CHANGE = dict(ev.SHARED, **{ev.P_PRD: PRD_V3, ev.P_ARCH: ARCH_CLEAN})

MANUAL = {
    "two-archs": ("VER-13 (c): two active ARCHs cite PRD-001 v2.", TWO_ARCHS),
    "superseded-arch": ("VER-13 (j): ARCH-001 superseded by ARCH-002, both citing PRD-001 v2.", SUPERSEDED_ARCH),
    "platform-changed": ("VER-13 (k): POL-001 v2 changes SET-01's platform; ARCH-001 links v1.", PLATFORM_CHANGED),
    "prd-priority-change": ("VER-13 (i): PRD-001 v3 changes only FR-004's priority; ARCH-001 cites v2.",
                            PRD_PRIORITY_CHANGE),
}

CHECKS = [("ARCH2", arch2(supersedes=False), "arch.schema.json"),
          ("ARCH1_SUPERSEDED", ARCH1_SUPERSEDED, "arch.schema.json"),
          ("ARCH2_SUPERSEDES", arch2(supersedes=True), "arch.schema.json"),
          ("POL_CHANGED", POL_CHANGED, "policy.schema.json"),
          ("PRD_V3", PRD_V3, "prd.schema.json"),
          ("ARCH_CLEAN", ARCH_CLEAN, "arch.schema.json")]


def premises():
    """Each fixture holds the premise its check names."""
    a1 = ev.validate("ARCH1_SUPERSEDED", ARCH1_SUPERSEDED, "arch.schema.json")["frontmatter"]
    a2 = ev.validate("ARCH2_SUPERSEDES", arch2(supersedes=True), "arch.schema.json")["frontmatter"]
    assert (a1["status"], a1["superseded_by"], a2["status"], a2["supersedes"]) == (
        "superseded", "ARCH-002", "approved", ["ARCH-001"])
    assert [(u["id"], u["version"]) for u in a2["upstream"]] == [("PRD-001", 2)]
    new = ev.setting(POL_CHANGED, "SET-01")["value"]
    assert new["platform"] == NEW_PLATFORM and new["capability"] == ev.MAIL_CAPABILITY
    assert ev.validate("POL_CHANGED", POL_CHANGED, "policy.schema.json")["frontmatter"]["version"] == 2
    assert ev.MAIL_ENTRY in ev.last_resolution(ev.ARCH)  # ARCH-001 still records the old platform
    old = {r["id"]: (r["priority"], r["release"]) for r in
           ev.validate("PRD", ev.PRD, "prd.schema.json")["functional_requirements"]}
    new_frs = {r["id"]: (r["priority"], r["release"]) for r in
               ev.validate("PRD_V3", PRD_V3, "prd.schema.json")["functional_requirements"]}
    assert {k for k in old if old[k] != new_frs[k]} == {"FR-004"} and new_frs["FR-004"] == ("should", "current")
    # ARCH_CLEAN passes the architecture skill's self-checks 9 and 10: every resolver exists and counts, and every
    # NEEDS ADR marker (FR-001, FR-009, FR-010) has a DEC citing its requirement.
    decs = {d["id"]: d for d in ev.validate("ARCH_CLEAN", ARCH_CLEAN, "arch.schema.json")["decisions"]}
    assert {k: decs[k]["state"] for k in ("DEC-03", "DEC-05", "DEC-08", "DEC-09")} == dict.fromkeys(
        ("DEC-03", "DEC-05", "DEC-08", "DEC-09"), "open")
    resolvers = {r for d in decs.values() for r in d["resolved_by"]}
    assert resolvers == {"ADR-001", "ADR-003", "POL-001#SET-01"}, resolvers
    assert "ADR-004" not in ARCH_CLEAN
    cited = {u["item"] for d in decs.values() for u in d["upstream"]}
    assert {"FR-001", "FR-009", "FR-010"} <= cited
    ev3 = {e["id"]: e for e in ev.validate("ARCH_CLEAN", ARCH_CLEAN, "arch.schema.json")["evidence"]}
    assert ev3["EVD-03"]["classification"] == "context" and "EVD-05" not in ev3


def main():
    for label, text, schema in CHECKS:
        ev.validate(label, text, schema)
    premises()
    for name, (comment, files) in MANUAL.items():
        d = OUT / name
        d.mkdir(parents=True, exist_ok=True)
        (d / "scaffold.sh").write_text(ev.scaffold(f"Seeds the manual fixture for SPEC-004 {comment}", files))
        os.chmod(d / "scaffold.sh", 0o755)
    print("validated", len(CHECKS), "fixtures; wrote", len(MANUAL), "manual scaffolds")


if __name__ == "__main__":
    main()
