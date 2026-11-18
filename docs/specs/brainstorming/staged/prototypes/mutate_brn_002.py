import os, re, subprocess, sys, tempfile, shutil
HERE = os.path.dirname(os.path.abspath(__file__))
SCRIPT = os.path.join(HERE, "validate_brn_iv_bv.py")
EX = os.path.join(HERE, "..", "examples", "brainstorm-brownfield")
BASE = open(os.path.join(EX, "BRN-002.md"), encoding="utf-8").read()
OLD = open(os.path.join(EX, "BRN-001.md"), encoding="utf-8").read()

def run(text, flags=(), name="BRN-002.md"):
    d = tempfile.mkdtemp(); f = os.path.join(d, "docs/specs/brainstorm"); os.makedirs(f)
    p = os.path.join(f, name); open(p, "w", encoding="utf-8").write(text)
    r = subprocess.run([sys.executable, "-B", *flags, SCRIPT, p], capture_output=True, text=True)
    shutil.rmtree(d, ignore_errors=True)
    return [l.replace(d, "T") for l in r.stdout.splitlines()]

def sub(t, a, b, count=1):
    assert a in t, a
    return t.replace(a, b, count)

CASES = []
def case(name, text, *expect):
    CASES.append((name, text, expect))

# kind
case("kind-unknown-value", sub(BASE, "Project kind: brownfield", "Project kind: both"), "the first line of section 1 must be 'Project kind: greenfield'")
case("kind-not-first", sub(BASE, "Project kind: brownfield\n\n", "Some words first.\n\nProject kind: brownfield\n\n"), "the first line of section 1 must be")
case("kind-wrong-case", sub(BASE, "Project kind: brownfield", "Project Kind: brownfield"), "the first line of section 1 must be")
case("kind-no-blank-line", sub(BASE, "Project kind: brownfield\n\n", "Project kind: brownfield\n"), "the Project kind line must be followed by a blank line")
case("kind-twice", sub(BASE, "### Existing product", "Project kind: brownfield\n\n### Existing product"), "more than one 'Project kind' line")
case("kind-needs-form-passes", sub(BASE, "Project kind: brownfield", "Project kind: [NEEDS CLARIFICATION: greenfield or brownfield]"))
case("kind-greenfield-with-c02", sub(BASE, "Project kind: brownfield", "Project kind: greenfield"), "'### Existing product' is for a brownfield BRN; this one says greenfield")
no_kind = sub(BASE, "Project kind: brownfield\n\n", "")
case("shape-heading-without-kind", no_kind, "'### Existing product' needs a 'Project kind:' line as the first line of section 1")
# old BRN: passes
case("old-brn-passes", OLD)  # name fixed below
# sources
case("sources-no-kind", sub(BASE, '  - "data: ClinicCore booking source report', '  - "ClinicCore booking source report'), "sources entry 4 must read")
case("sources-unknown-kind", sub(BASE, '  - "data: ClinicCore booking source report', '  - "email: ClinicCore booking source report'), "sources entry 4 must read")
case("sources-duplicate", sub(BASE, '  - "data: ClinicCore booking source report, October 2026"\n', '  - "data: ClinicCore booking source report, October 2026"\n  - "data: ClinicCore attendance report, October 2026"\n'), "sources entry 5 repeats entry 3")
case("sources-bad-escape", sub(BASE, 'booking source report, October 2026"\n---', 'booking source \\q report, October 2026"\n---'), "sources entry 4: a backslash may only be followed by")
# evidence
case("evidence-uncited", sub(BASE, '"[NEEDS CLARIFICATION: how many freed slots go unfilled each month]"\n    severity: medium', '"Staff say it happens a lot"\n    severity: medium'), "PRB-02: evidence must be a [NEEDS CLARIFICATION: ...] marker or quote one entry of sources")
case("evidence-partial-source", sub(BASE, "(data: ClinicCore attendance report, October 2026)\"\n    severity: high", "(data: ClinicCore attendance report)\"\n    severity: high"), "PRB-01: evidence must be")
# section 3
case("s3-missing", re.sub(r"## 3\. Target users\n\n\|.*?\n\n(?=## 4)", "## 3. Target users\n\nReturning patients.\n\n", BASE, flags=re.S), "section 3 holds only the Target users table", "section 3 must hold the Target users table with the header")
case("s3-wrong-header", sub(BASE, "| Persona | Job to be done | Current workaround | Pain |", "| Persona | Job | Workaround | Pain |"), "section 3: the table must start with the header")
case("s3-missing-persona", sub(BASE, "| Front-desk staff | Keep every hour of the day filled | [NEEDS CLARIFICATION: what staff do today with a freed slot] | An hour that is freed on the day stays empty |\n", ""), "section 3 must have one row per distinct who of the active problems, in order of first appearance: Returning patient; Front-desk staff (found: Returning patient)")
case("s3-extra-persona", sub(BASE, "| Front-desk staff |", "| Dentist | a | b | c |\n| Front-desk staff |"), "section 3 must have one row per distinct who")
case("s3-empty-cell", sub(BASE, "| Keep a check-up booked weeks ahead and turn up |", "|  |"), "section 3: a table cell is empty")
case("s3-three-cells", sub(BASE, "| Returning patient | Keep a check-up booked weeks ahead and turn up | The day-before text and the patient's own calendar | Forgets the date, loses the slot and sometimes the clinic's goodwill |", "| Returning patient | Keep a check-up booked weeks ahead and turn up | Forgets the date |"), "section 3: a table row must have 4 cells")
case("who-with-pipe", sub(BASE, 'who: "Front-desk staff"', 'who: "Front desk | staff"'), "PRB-02: who must not contain '|'")
# deprecated problem not counted
dep = sub(BASE, "  - id: PRB-02\n    status: active", "  - id: PRB-02\n    status: deprecated")
dep = sub(dep, "| Front-desk staff | Keep every hour of the day filled | [NEEDS CLARIFICATION: what staff do today with a freed slot] | An hour that is freed on the day stays empty |\n", "")
dep = sub(dep, "  - id: IDEA-03\n    status: active", "  - id: IDEA-03\n    status: deprecated")
case("deprecated-problem-not-counted", dep)
# section 8
case("s8-none-passes", re.sub(r"(## 8\. Candidate success signals\n\n).*?(\n## Change Log)", r"\1- None.\n\2", BASE, flags=re.S))
case("s8-free-bullet", sub(BASE, "- IDEA-03: more freed slots filled before the visit; baseline [NEEDS CLARIFICATION: share of freed slots filled today]", "- Fewer missed visits."), "section 8 must be the line '- None.' or one bullet per first-release idea")
case("s8-unknown-idea", sub(BASE, "- IDEA-03: more", "- IDEA-09: more"), "section 8: IDEA-09 is not a defined idea")
case("s8-order", sub(BASE, "- IDEA-03: more", "- IDEA-01: more"), "section 8: bullets must be in ID order, once each (IDEA-01 after IDEA-01)")
case("s8-baseline-uncited", sub(BASE, "baseline 12% of October 2026 visits missed (data: ClinicCore attendance report, October 2026)", "baseline 12% of visits missed"), "section 8: baseline of IDEA-01 must be")
case("s8-no-baseline", sub(BASE, "; baseline [NEEDS CLARIFICATION: share of freed slots filled today]", ""), "section 8 must be the line '- None.' or one bullet")
case("s8-none-and-bullet", sub(BASE, "## 8. Candidate success signals\n\n", "## 8. Candidate success signals\n\n- None.\n"), "section 8 must be the line '- None.' or one bullet")
# brownfield
case("bf-missing-c02", re.sub(r"### Existing product\n\n.*?\n\n(?=## 2)", "", BASE, flags=re.S), "a brownfield BRN needs '### Existing product' in section 1")
case("bf-no-document-line", re.sub(r"(### Existing product\n\n).*?\n\n(?=## 2)", r"\1No document was found in the project.\n\n", BASE, flags=re.S).replace('  - {id: PRD-001, relation: informed_by, version: 3, hash: null}\n  - {id: BRN-001, relation: informed_by, version: 1, hash: null}\n', '  - {id: ADR-009, relation: informed_by, version: 1, hash: null}\n') , "upstream links ADR-009, which has no row in '### Existing product'")
case("bf-c02-own-id", sub(BASE, "| BRN-001 | 1 |", "| BRN-002 | 1 |"), "Document 'BRN-002' must be")
case("bf-c02-version", sub(BASE, "| PRD-001 | 3 |", "| PRD-001 | v3 |"), "PRD-001: Version must be a positive integer")
case("bf-c02-order", sub(sub(BASE, "| PRD-001 | 3 | Online booking for returning patients (FR-001 to FR-006; NFR-001 to NFR-002) |\n| BRN-001 | 1 | Earlier brainstorm: Online appointment booking for returning patients (IDEA-01 to IDEA-06; ASM-01 to ASM-02) |", "| BRN-001 | 1 | Earlier brainstorm: Online appointment booking for returning patients (IDEA-01 to IDEA-06; ASM-01 to ASM-02) |\n| PRD-001 | 3 | Online booking for returning patients (FR-001 to FR-006; NFR-001 to NFR-002) |"), "x", "x") if False else sub(BASE, "| PRD-001 | 3 | Online booking for returning patients (FR-001 to FR-006; NFR-001 to NFR-002) |\n| BRN-001 | 1 | Earlier brainstorm: Online appointment booking for returning patients (IDEA-01 to IDEA-06; ASM-01 to ASM-02) |", "| BRN-001 | 1 | Earlier brainstorm: Online appointment booking for returning patients (IDEA-01 to IDEA-06; ASM-01 to ASM-02) |\n| PRD-001 | 3 | Online booking for returning patients (FR-001 to FR-006; NFR-001 to NFR-002) |"), "C-02 rows go PRD, BRN, ARCH, EPIC, ADR")
case("bf-c02-sources-entry", sub(BASE, '  - "document: docs/specs/prd/PRD-001.md v3"\n', ''), 'PRD-001: sources must hold the entry "document: docs/specs/prd/PRD-001.md v3"')
case("bf-c02-upstream-missing", sub(BASE, "  - {id: BRN-001, relation: informed_by, version: 1, hash: null}\nsupersedes", "supersedes"), "BRN-001: upstream must hold {id: BRN-001, relation: informed_by, version: 1, hash: null}")
case("bf-c02-upstream-wrong-version", sub(BASE, "{id: PRD-001, relation: informed_by, version: 3,", "{id: PRD-001, relation: informed_by, version: 2,"), "PRD-001: upstream must hold")
v2 = sub(sub(BASE, "version: 1\ncreated", "version: 2\ncreated"), "  - {id: BRN-001, relation: informed_by, version: 1, hash: null}\nsupersedes", "supersedes")
v2 = sub(v2, "| 1 | 2026-11-18 | claude-code (session example-session) | Brownfield brainstorm on PRD-001 v3 and BRN-001 |", "| 1 | 2026-11-18 | claude-code (session example-session) | x |\n| 2 | 2026-11-19 | claude-code (session example-session) | y |")
case("bf-extension-may-omit-upstream", v2)
case("bf-missing-c06", re.sub(r"### Already covered\n\n.*?(?=### Previously decided)", "", BASE, flags=re.S), "a BRN with '### Existing product' also needs '### Already covered' in section 6")
case("bf-covered-by", sub(BASE, "| Text reminders before a visit | PRD-001#FR-003 |", "| Text reminders before a visit | PRD-009#FR-003 |"), "Covered by 'PRD-009#FR-003' must be")
case("bf-covered-by-none", re.sub(r"(### Already covered\n\n).*?(?=### Previously decided)", r"\1None.\n\n", BASE, flags=re.S))
case("bf-decision", sub(BASE, "| parked | BRN-001#IDEA-04 |", "| deferred | BRN-001#IDEA-04 |"), "Previously decided rows need Decision rejected or parked")
case("bf-where-unknown-brn", sub(BASE, "| rejected | BRN-001#IDEA-06 |", "| rejected | BRN-007#IDEA-06 |"), "Previously decided rows need")
case("bf-where-order", sub(sub(BASE, "| parked | BRN-001#IDEA-04 |", "| parked | BRN-001#IDEA-09 |"), "x", "x") if False else sub(BASE, "BRN-001#IDEA-04 |", "BRN-001#IDEA-07 |"), "Previously decided rows go in the order of Where")
case("bf-update-change", sub(BASE, "open to validated", "open to confirmed"), "Change must be 'open to validated' or 'open to invalidated'")
case("bf-update-evidence", sub(BASE, "62% of October 2026 bookings were made online (data: ClinicCore booking source report, October 2026)", "62% of bookings were made online"), "Evidence must quote one entry of sources")
case("bf-update-status", sub(BASE, "| confirmed by Dana on 2026-11-18 |", "| confirmed |"), "Status must be 'proposed, not confirmed' or 'confirmed by NAME on YYYY-MM-DD'")
case("bf-update-proposed-passes", sub(BASE, "| confirmed by Dana on 2026-11-18 |", "| proposed, not confirmed |"))
case("bf-update-unknown-brn", sub(BASE, "| BRN-001#ASM-01 | open", "| BRN-005#ASM-01 | open"), "Earlier assumption 'BRN-005#ASM-01' must be")
case("bf-section6-order", sub(sub(BASE, "### Previously decided", "### Zzz"), "x","x") if False else BASE.replace("### Already covered", "### TMP").replace("### Previously decided", "### Already covered").replace("### TMP", "### Previously decided"), "section 6 order is Already covered, Previously decided, Assumption updates")

# the BV-02 heading gate (a BRN written by build 2 with kind brownfield and none of the four headings stays valid)
bare = re.sub(r"### Existing product\n\n.*?\n\n(?=## 2)", "", BASE, flags=re.S)
bare = re.sub(r"### Already covered\n\n.*?(?=## 7)", "", bare, flags=re.S)
bare = bare.replace("  - {id: PRD-001, relation: informed_by, version: 3, hash: null}\n  - {id: BRN-001, relation: informed_by, version: 1, hash: null}\n", "").replace("upstream:\nsupersedes", "upstream: []\nsupersedes")
case("bv02-gate-brownfield-with-no-brownfield-heading-passes", bare)
case("bv02-gate-one-heading-only-fails", bare.replace("## 7. Assumptions", "### Already covered\n\nNone.\n\n## 7. Assumptions", 1), "a brownfield BRN needs '### Existing product' in section 1")
case("kind-gate-needs-the-colon", sub(BASE, "Project kind: brownfield\n\n", "Project kinds vary.\n\n"), "'### Existing product' needs a 'Project kind:' line as the first line of section 1")
# extra rows required by the spec's test tables
gf = BASE.replace("Project kind: brownfield", "Project kind: greenfield")
gf = re.sub(r"### Existing product\n\n.*?\n\n(?=## 2)", "", gf, flags=re.S)
gf = re.sub(r"### Already covered\n\n.*?(?=## 7)", "", gf, flags=re.S)
case("greenfield-without-brownfield-regions-passes", gf)
nd = re.sub(r"(### Existing product\n\n).*?\n\n(?=## 2)", r"\1No document was found in the project.\n\n", BASE, flags=re.S)
nd = nd.replace("upstream:\n  - {id: PRD-001, relation: informed_by, version: 3, hash: null}\n  - {id: BRN-001, relation: informed_by, version: 1, hash: null}\n", "upstream: []\n")
nd = re.sub(r"(### Already covered\n\n).*?(?=### Previously decided)", r"\1None.\n\n", nd, flags=re.S)
nd = re.sub(r"(### Previously decided\n\n).*?(?=### Assumption updates)", r"\1None.\n\n", nd, flags=re.S)
nd = re.sub(r"(### Assumption updates\n\n).*?(?=## 7)", r"\1None.\n\n", nd, flags=re.S)
case("no-document-line-with-none-tables-passes", nd)
nr = re.sub(r"(### Existing product\n\n).*?\n\n(?=## 2)", r"\1No document was found in the project.\n\n", BASE, flags=re.S)
case("upstream-record-without-row", nr, "upstream links PRD-001, which has no row in '### Existing product'")

bad = 0
for name, text, expect in CASES:
    outs = {}
    for flags in ((), ("-S",)):
        outs[flags] = run(text, flags, "BRN-001.md" if name == "old-brn-passes" else "BRN-002.md")
    same = (outs[()][-1].startswith("OK")) == (outs[("-S",)][-1].startswith("OK"))
    out = outs[()]
    if not expect:
        ok = out and out[-1].startswith("OK:")
    else:
        ok = all(any(e in l for l in out) for e in expect) and not out[-1].startswith("OK:")
    if not ok or not same:
        bad += 1
        print("FAIL", name, "same-with/without" if same else "DIFF", "\n   ", "\n    ".join(out[:12]))
    else:
        print("ok  ", name, "|", (out[0] if expect else out[-1])[:150])
print("failures:", bad)
