"""Generates evals/context/<case>/ for the context skill (SPEC-011 §9, QR-03, VER-26): prompts, graders,
case.yaml and an inline scaffold per case.

Every fixture is built once here from the example set (src/staging/examples/context-cli-service-rdbms/) and
the documents this generator writes (PRD-001, STORY-001 to STORY-004, POL-001, AMB-001's ENT-03). Each
scaffold is run in a temporary folder, and each document it writes is validated against src/schemas/ with a
format checker, except a document the case marks as expected to be invalid, which must fail exactly where
the case says. Policy fixtures also go through the shared validate_policy.py.

Graders are JavaScript regular expressions (the harness's engine). SPEC-011 §9 writes whole-content anchors
as \\A…\\Z; JavaScript has neither, so they are written ^…$ with no m flag, which anchors at the start and
end of the input (Bryan, 2026-10-01). Each grader's name starts with the VER item it grades.

The context_check.py pass over the seeded context documents (§9, "The script on the fixtures") is off
until §11 step 6 builds the script: RUN_CONTEXT_CHECK.

Run from the repository root, under the normal HOME (it imports referencing, from the user site):
    PYTHONDONTWRITEBYTECODE=1 python3 src/tests/context/make_evals.py
"""
import json
import re
import shutil
import subprocess
import sys
import tempfile
from dataclasses import dataclass, field
from pathlib import Path

import yaml
from jsonschema import Draft202012Validator, FormatChecker
from referencing import Registry, Resource

ROOT = Path("src/claude/DevForgeAI/evals/context")
SCHEMAS = Path("src/schemas")
EXAMPLE = Path("src/staging/examples/context-cli-service-rdbms/docs/specs")
CONTEXT_CHECK = Path("src/claude/DevForgeAI/skills/context/scripts/context_check.py")
RUN_CONTEXT_CHECK = False  # SPEC-011 §11 step 6 switches this on, once context_check.py exists
POLICY_SCRIPT = Path("src/claude/DevForgeAI/skills/prd/scripts/validate_policy.py")
TOOLS = "[Skill, Read, Glob, Grep, Write, Edit, Bash]"
WRITING_LIMITS = (100, 1800)  # §9: a case that writes documents; also the stop-early cases (Bryan, 2026-10-01)
SHORT_LIMITS = (15, 300)      # §9: the negative case and the trigger cases
CTX = "docs/specs/context"

# --------------------------------------------------------------------------------------------------------
# The document set (§4)

IDS = {"index": "CTX-001", "architecture": "CTX-002", "tech-stack": "CTX-003", "source-tree": "CTX-004",
       "testing": "CTX-005", "front-end": "CTX-011", "middle-tier": "CTX-012", "back-end": "CTX-013",
       "api": "CTX-014", "rdbms": "CTX-015", "datastore": "CTX-016", "ui-mockups": "CTX-017"}
TITLES = {"index": "project context index", "architecture": "architecture overview", "tech-stack": "tech stack",
          "source-tree": "source tree", "testing": "testing", "front-end": "front end",
          "middle-tier": "middle tier", "back-end": "back end", "api": "api", "rdbms": "relational database",
          "datastore": "data store", "ui-mockups": "ui mockups"}
SHARED_SET = ["index", "architecture", "tech-stack", "source-tree", "testing", "front-end", "ui-mockups",
              "middle-tier", "rdbms"]
EXAMPLE_DOCS = ["index", "architecture", "tech-stack", "source-tree", "testing", "front-end", "middle-tier",
                "rdbms", "ui-mockups"]

# The Change Log line every document written in a no-policy run ends with (VER-19), and with VER-15's policy.
RESOLUTION = ("Policy resolution: interview.max_calls=8 (default); architecture.mandated_platforms=none (default); "
              "quality.required_categories=floor only (default); testing.method=tdd (default); "
              "testing.coverage_metric=line (default); testing.coverage_threshold=none (default); "
              "testing.coverage_scope=code roots (default); testing.coverage_exclusions=generated,tests,fixtures "
              "roots (default); testing.exception_approvers=story owner (default)")
RESOLUTION_POL = RESOLUTION.replace("testing.coverage_threshold=none (default)",
                                    "testing.coverage_threshold=90 (POL-001#SET-01)")

# Sections whose template has a Convention placeholder or a Basis column, and that nothing decides in the
# shared fixture (VER-04; Bryan's default 10, 2026-10-01). "table" marks a section whose rows carry a Basis.
PROPOSED_SECTIONS = {
    "architecture": ["Error handling", "Logging", "Configuration", "Security basics"],
    "tech-stack": ["Upgrades"],
    "source-tree": ["Layout conventions", "Generated files"],
    "testing": [("Test levels", "table"), "Naming", "Fixtures and test data", ("Running the tests", "table")],
    "front-end": ["Framework and structure", "State", "Interaction and output", "Accessibility", "Design system"],
    "middle-tier": ["Domain structure", "Boundaries within a component", "Orchestration", "Validation",
                    "Transactions"],
    "rdbms": ["Naming", "Migrations", "Indexing", "Transactions"],
    "ui-mockups": ["Design system"],
}


def replace(text, old, new):
    assert text.count(old) == 1, f"expected exactly one {old!r}"
    return text.replace(old, new)


# --------------------------------------------------------------------------------------------------------
# Fixtures

ARCH = (EXAMPLE / "arch/ARCH-001.md").read_text()
ADR_1 = (EXAMPLE / "adr/ADR-001.md").read_text()
ADR_2 = (EXAMPLE / "adr/ADR-002.md").read_text()
AMB = (EXAMPLE / "ambiguities/AMB-001.md").read_text()
CONTEXT = {name: (EXAMPLE / f"context/{name}.md").read_text() for name in EXAMPLE_DOCS}
MIGRATIONS = (EXAMPLE / "context/rdbms/migrations.md").read_text()
FIXTURE_SESSION = "00000000-0000-0000-0000-000000000000"

PRD = f"""\
---
id: PRD-001
type: prd
title: "shiftlog: record work shifts and report weekly hours"
status: approved
version: 1
created: 2026-09-28
updated: 2026-09-28
owner: "Example Owner"
authors: ["Example Owner", "claude-code"]
generated_by:
  tool: "claude-code"
  model: "claude-opus-5-5"
  session: "{FIXTURE_SESSION}"
reviewed_by: []
approved_by: "Example Owner"
approved_on: 2026-09-28
upstream: []
supersedes: []
superseded_by: null
blocked_by: []
# --- prd-specific ---
target_release: "1.0"
stage: mvp
operating_context: internal
stakeholders: ["Example Owner"]
---

# PRD-001 — shiftlog: record work shifts and report weekly hours

## 1. Summary

A command-line tool, `shiftlog`, with which one person records work shifts and sees the hours worked
each week.

## 2. Functional requirements

```yaml items
functional_requirements:
  - id: FR-001
    status: active
    statement: "A user installs shiftlog with one command on a laptop, then starts, stops and lists shifts from the command line."
    priority: must
    release: current
    notes: ""
  - id: FR-002
    status: active
    statement: "A user sees the total hours worked in each week."
    priority: must
    release: current
    notes: ""
```

## 3. Non-functional requirements

```yaml items
non_functional_requirements:
  - id: NFR-001
    status: active
    category: privacy
    statement: "Shift records stay on the user's own machine; nothing is sent over the network."
    priority: must
    release: current
```

## Change Log

| Version | Date | Author | Change | Items affected |
|---|---|---|---|---|
| 1 | 2026-09-28 | claude-code (session {FIXTURE_SESSION}) | Initial draft | all |
| 1 | 2026-09-28 | Example Owner | Approved | status |
"""


def story(num, title, version, upstream, scope_line, created="2026-09-29", updated="2026-09-30"):
    links = "".join(f"\n  - {link}" for link in upstream) if upstream else " []"
    return f"""\
---
id: STORY-{num:03d}
type: story
title: "{title}"
status: ready
version: {version}
created: {created}
updated: {updated}
owner: "Example Owner"
authors: ["Example Owner", "claude-code"]
generated_by:
  tool: "claude-code"
  model: "claude-opus-5-5"
  session: "{FIXTURE_SESSION}"
reviewed_by: []
approved_by: ""
approved_on: null
upstream:{links}
supersedes: []
superseded_by: null
blocked_by: []
# --- story-specific ---
estimate: null
spec_mode: separate
---

# STORY-{num:03d} — {title}

## 1. User story

As a **shift worker**, I want **{title[0].lower() + title[1:]}**, so that **my hours are right**.

## 2. Context

Part of PRD-001.

## 3. Scope

**In scope**
- {title}.

**Out of scope**
- Anything else.

{scope_line}

## 4. Acceptance criteria

```yaml items
acceptance_criteria:
  - id: AC-01
    status: active
    name: "{title}"
    given:
      - "a recorded shift"
    when:
      - "I run the command"
    then:
      - "the shift is shown"
    upstream:
      - {{id: PRD-001, item: FR-001, relation: satisfies, version: 1, hash: null}}
```

## 5. Specification

GENERATED: the SPEC that specifies this story cites it.

## 6. Definition of Done

- [ ] Every AC is verified by at least one test that cites it (`STORY-{num:03d}#AC-NN`)

## 7. Open questions

None.

## Change Log

| Version | Date | Author | Change | AC affected |
|---|---|---|---|---|
| 1 | {created} | claude-code (session {FIXTURE_SESSION}) | Initial draft | all |
""" + (f"| {version} | {updated} | claude-code (session {FIXTURE_SESSION}) | Recorded the approved design | — |\n"
       if version > 1 else "")


STORY_1 = story(1, "List recorded shifts", 2, ["{id: CTX-003, relation: constrains, version: 2, hash: null}"],
                "- **Approved design:** `shiftlog list` output; docs/specs/story/design/STORY-001/list-output.png; "
                "approved 2026-09-29; bundle none")
STORY_2 = story(2, "Add a shift by prompt", 2, [],
                "- **Approved design:** `shiftlog add` prompt; docs/specs/story/design/STORY-002/add-prompt.png; "
                "approved 2026-09-30; bundle none", created="2026-09-30")
STORY_3 = story(3, "Edit a shift", 2, [], "Design approved: docs/specs/story/design/STORY-003/edit.png (2026-09-30)",
                created="2026-09-30")
STORY_4 = story(4, "Delete a shift", 1, [],
                "Design draft: docs/specs/story/design/STORY-004/edit.png, awaiting review", created="2026-09-30",
                updated="2026-09-30")

POLICY = """\
---
id: POL-001
type: policy
title: "Example organization engineering policy (vendored)"
status: approved
version: 1
created: 2026-09-15
updated: 2026-09-15
owner: "Example platform council"
authors: ["Example platform council"]
reviewed_by: []
approved_by: "Example CTO"
approved_on: 2026-09-15
upstream: []
supersedes: []
superseded_by: null
blocked_by: []
# --- policy-specific ---
scope: organization
source: {repository: "git.example.org/policy", ref: "v1.0.0"}
---

# POL-001 — Example organization engineering policy (vendored)

## 1. Scope and ownership

Every product of the example organization.

## 2. Settings

```yaml items
settings:
  - id: SET-01
    status: active
    key: testing.coverage_threshold
    class: organizational_policy
    value: 90
    overridable_by: []
    rationale: "Every product keeps line coverage at or above 90%"
```
"""
POLICY_BAD_DATE = replace(POLICY, "updated: 2026-09-15", "updated: 2026-13-45")

# VER-07: a fourth component whose transport, a message broker, nothing decides. Its responsibility and
# interacts_with leave the broker as the only undecided significant choice (Bryan's default 2).
CMP_REMINDER = """\
  - id: CMP-04
    status: active
    name: "Reminder worker"
    kinds:
      - "platform"
    responsibility: "Sends reminders for shifts left running, from jobs the Shift service queues for it, on the user's machine"
    owns_data: []
    interacts_with:
      - "CMP-02"
    deployment: "A background process; the message broker is undecided"
    upstream:
      - {id: PRD-001, item: FR-001, relation: informed_by, version: 1, hash: null}
"""
CMP_EXPORT = """\
  - id: CMP-04
    status: active
    name: "Export API"
    kinds:
      - "api"
    responsibility: "Exports a week's shifts as CSV for other tools"
    owns_data: []
    interacts_with:
      - "CMP-02"
    deployment: "Runs in the shiftlog Python package"
    upstream:
      - {id: PRD-001, item: FR-002, relation: informed_by, version: 1, hash: null}
"""
END_OF_COMPONENTS = ("    deployment: \"SQLite file under the user's data folder\"\n    upstream:\n"
                     "      - {id: PRD-001, item: NFR-001, relation: informed_by, version: 1, hash: null}\n```")


def add_component(arch, cmp, mermaid):
    arch = replace(arch, END_OF_COMPONENTS, END_OF_COMPONENTS[:-3] + cmp + "```")
    return replace(arch, "--> CMP03[(CMP-03 Local database)]\n", "--> CMP03[(CMP-03 Local database)]\n" + mermaid)


ARCH_REMINDER = add_component(ARCH, CMP_REMINDER, "    CMP02 --> CMP04[CMP-04 Reminder worker]\n")
ARCH_V2 = add_component(ARCH, CMP_EXPORT, "    CMP04[CMP-04 Export API] --> CMP02\n")
ARCH_V2 = replace(ARCH_V2, "version: 1\ncreated: 2026-09-29\nupdated: 2026-09-29",
                  "version: 2\ncreated: 2026-09-29\nupdated: 2026-09-30")
ARCH_V2 = replace(ARCH_V2, "approved_on: 2026-09-29", "approved_on: 2026-09-30")
ARCH_V2 = ARCH_V2 + (
    f"| 2 | 2026-09-30 | claude-code (session {FIXTURE_SESSION}) | Added CMP-04, Export API, for PRD-001 v1. Policy "
    "resolution: interview.max_calls=8 (default); architecture.mandated_platforms=none (default); "
    "quality.required_categories=floor only (default) | CMP-04 |\n"
    "| 2 | 2026-09-30 | Example Owner | Approved | — |\n")
ARCH_NO_KINDS = replace(ARCH, '    kinds:\n      - "service"\n', "")

ENT_03 = f"""\
  - id: ENT-03
    status: active
    date: 2026-09-30
    recorded_by: "claude-code (session {FIXTURE_SESSION})"
    question: "Commit the lock file with this dependency change?"
    checked:
      - "docs/specs/context/tech-stack.md (CTX-003 v2), section 2"
    action: "Committed the lock file with the dependency change"
    reverse: "Remove the lock file from the commit"
    impact: "Repository hygiene only; no behaviour changes"
    resolve_before: "PR review"
    relates_to:
      - "CTX-003"
    state: accepted
    decided_by: "Example Owner"
    decided_on: 2026-09-30
    resolution: ""
"""
AMB_3 = replace(AMB, '    resolution: ""\n```\n', '    resolution: ""\n' + ENT_03 + "```\n")
AMB_3 = replace(AMB_3, "updated: 2026-09-29", "updated: 2026-09-30")
FOLD_ALREADY = "folded into CTX-003 v3: already stated"
FOLD_NEW = "folded into CTX-003 v3"

PYPROJECT = """\
[project]
name = "shiftlog"
version = "0.1.0"
dependencies = [
    "typer==0.12.3",
]

[project.optional-dependencies]
test = [
    "pytest>=8,<9",
]
"""

SHARED = {"docs/specs/prd/PRD-001.md": PRD, "docs/specs/arch/ARCH-001.md": ARCH,
          "docs/specs/adr/ADR-001.md": ADR_1, "docs/specs/adr/ADR-002.md": ADR_2}
NO_ARCH = {k: v for k, v in SHARED.items() if not k.startswith("docs/specs/arch/")}
EXAMPLE_PROJECT = dict(SHARED, **{f"{CTX}/{n}.md": CONTEXT[n] for n in EXAMPLE_DOCS},
                       **{f"{CTX}/rdbms/migrations.md": MIGRATIONS, "docs/specs/story/STORY-001.md": STORY_1})
CODE = {"pyproject.toml": PYPROJECT, "src/shiftlog/cli/main.py": '"""shiftlog command-line entry point."""\n',
        "tests/service/test_rules.py": '"""Tests for the shift rules."""\n'}

SHARED_PROMPT = """\
Write the project context documents. I confirm these conventions: Typer 0.12.x for the shiftlog CLI;
Alembic 1.13.x for the Local database; pytest 8.x for every component; and dependency updates go in
their own pull request. None of these is hard to reverse or shared by several epics: each can be
replaced inside the components that use it. Don't inspect any code. Proceed without questions."""

# --------------------------------------------------------------------------------------------------------
# Regex builders (JavaScript syntax). Q is an optional YAML quote.

Q = "[\"']?"
FM_LINE = r"(?:(?!---[ \t]*\n)[^\n]*\n)"
EOL = r"[ \t]*(?:#[^\n]*)?\n"
ITEM_LINE = r"(?:(?![ \t]*(?:- id:[ \t]*" + Q + r"(?:TEC|SRC|ENT)-\d|```))[^\n]*\n)"
STMT_BODY = r"(?:(?!\n[ \t]*- |\n##|\n[ \t]*\n)[\s\S])*?"
DATE = r"\d{4}-\d{2}-\d{2}"
UUID = r"[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}"


def esc(text):
    """Escapes text for a JavaScript RegExp source, with newlines written \\n so a pattern stays one line."""
    out = []
    for ch in text:
        if ch in "\\^$.|?*+()[]{}":
            out.append("\\" + ch)
        elif ch == "\n":
            out.append("\\n")
        elif ch == "\t":
            out.append("\\t")
        else:
            out.append(ch)
    return "".join(out)


def ci(word):
    return "".join(f"[{c.upper()}{c.lower()}]" if c.isalpha() else esc(c) for c in word)


def whole(text):
    """The file's whole content, anchored at both ends (SPEC-011 §9's \\A…\\Z)."""
    return "^" + esc(text) + "$"


def fm_has(*conds):
    """Frontmatter holds a line (or lines) matching each condition, in any order."""
    return r"^---[ \t]*\n" + "".join(f"(?={FM_LINE}*?{c})" for c in conds)


def fm_field(key, value):
    return key + r":[ \t]*" + Q + value + Q + EOL


def nested(parent, key, value):
    """A key of a block mapping such as generated_by, or the same key in its flow form."""
    return (parent + r":(?:[ \t]*\n(?:[ \t]+[^\n]*\n)*?[ \t]+|[^\n]*[{,][ \t]*)" + key + r":[ \t]*" + Q + value
            + Q + r"[ \t]*[,}\n#]")


def link(doc, item=None, relation="constrains", version=None):
    """A link record to doc, in flow form ({id: …}) or block form (id: … on its own lines)."""
    keys = [(k, v) for k, v in (("item", item), ("relation", relation), ("version", version)) if v is not None]
    flow = (r"\{(?=[^}\n]*\bid:[ \t]*" + Q + doc + r"\b)"
            + "".join(r"(?=[^}\n]*\b" + k + r":[ \t]*" + Q + str(v) + r"\b)" for k, v in keys) + r"[^}\n]*\}")
    block = (r"id:[ \t]*" + Q + doc + Q + r"[ \t]*\n"
             + "".join(r"(?=(?:[ \t]+(?!- )[^\n]*\n){0,6}?[ \t]+" + k + r":[ \t]*" + Q + str(v) + r"\b)"
                       for k, v in keys))
    return r"[ \t]*-[ \t]*(?:" + flow + "|" + block + ")"


def item(prefix, *conds):
    """An item of the TEC, SRC or ENT collection whose own lines match every condition."""
    head = r"(?:^|\n)[ \t]*- id:[ \t]*" + Q + prefix + r"-\d{2}" + Q + r"[ \t]*\n"
    return head + "".join(f"(?={ITEM_LINE}*?{c})" for c in conds)


def name_is(name):
    return r"[ \t]*name:[ \t]*" + Q + ci(name) + r"(?: \d+(?:\.\d+)*)?" + Q + EOL


def field_is(key, value):
    return r"[ \t]*" + key + r":[ \t]*" + Q + value + Q + EOL


def section(title):
    """From a level-2 heading (numbered or not) to a match inside that section."""
    return r"\n##[ \t]+(?:\d+\.[ \t]+)?" + title + r"[^\n]*\n(?:(?!\n##[ \t])[\s\S])*?"


def statement(label):
    return r"\n[ \t]*-[ \t]+\*\*" + label + STMT_BODY


def proposed_in(title, table=False):
    stmt = r"\*\*Proposed:\*\*" + STMT_BODY + r"\[NEEDS CLARIFICATION: confirm\b"
    if table:
        stmt = r"(?:\n\|[^\n]*\bProposed\b[^\n]*\[NEEDS CLARIFICATION: confirm\b|" + stmt + ")"
    return section(title) + stmt


def block_line(label, rest):
    """A line of the reply's report block (BEH-19), bold or plain, in or out of a code block."""
    return r"(?:^|\n)[ \t>*-]*(?:\*\*)?" + label + r":(?:\*\*)?[ \t]*" + rest


PARA_START = r"(?:^|\n[ \t]*\n)[ \t]*(?:\*\*|__)?Next step\b"
PARA_REST = r"(?:(?!\n[ \t]*\n)[\s\S])*?"
NEXT_STEP_LAST = PARA_START + PARA_REST + r"\s*$"
NEXT_STEP_IN_CODE = r"Next step" + PARA_REST + r"\n[ \t]*```[ \t]*\s*$"


def next_step_names(command):
    return PARA_START + PARA_REST + command + PARA_REST + r"\s*$"


EPIC_CMD = r"/devforgeai:epic[` \t]+PRD-001\b"
ARCH_CMD = r"/devforgeai:architecture[` \t]+PRD-001\b"
SKILL_MATCH = r"""'"skill"\s*:\s*"(?:[\w-]+:)?context"'"""

# --------------------------------------------------------------------------------------------------------
# Cases and graders


@dataclass
class Grader:
    name: str
    type: str
    target: str = None      # "last_message" or a workspace path
    pattern: str = None
    match: str = "contains"
    flags: str = ""
    exists: bool = None
    min: int = None
    max: int = None
    witness: str = None     # text that, appended to the target, must make a not_contains grader fail


@dataclass
class Case:
    name: str
    vers: list
    description: str
    prompt: str
    files: dict
    graders: list
    limits: tuple = WRITING_LIMITS
    tags: list = None
    invalid: dict = field(default_factory=dict)  # path -> the frontmatter field expected to fail
    policy_exit: int = None                       # validate_policy.py's expected exit, when policy is seeded


def rx(name, target, pattern, match="contains", flags="", witness=None):
    target = target if target == "last_message" else (target if "/" in target else f"{CTX}/{target}.md")
    return Grader(name, "regex", target=target, pattern=pattern, match=match, flags=flags, witness=witness)


def present(name, path, exists=True):
    return Grader(name, "file_exists", target=path, exists=exists)


def skill_fired(name, fired):
    return Grader(name, "tool_used", min=1 if fired else 0, max=None if fired else 0)


def unchanged(name, path, text):
    return rx(name, path, whole(text))


def ids_and_titles(ver, docs):
    out = []
    for d in docs:
        out.append(rx(f"{ver}-{d}-id", d, fm_has(fm_field("id", IDS[d]), fm_field("document", d))))
    return out


def tech(name, vr, basis, *more):
    return item("TEC", name_is(name), field_is("version_range", vr), field_is("basis", basis), *more)


def lock_file_convention(ver):
    return rx(f"{ver}-tech-stack-lock-file-convention", "tech-stack",
              section("Upgrades") + r"\*\*Convention:\*\*" + STMT_BODY + r"[Ll]ock[ -]?file")


def resolution_row(line):
    return r"\|[^|\n]*" + esc(line) + r"[ \t]*\|"


def writes_the_set():
    g = []
    for d in SHARED_SET:
        g.append(present(f"ver01-{d}-written", f"{CTX}/{d}.md"))
    for d in ("back-end", "api", "datastore"):
        g.append(present(f"ver01-no-{d}", f"{CTX}/{d}.md", exists=False))
    g += ids_and_titles("ver01", SHARED_SET)
    g += [unchanged("ver01-arch-001-unchanged", "docs/specs/arch/ARCH-001.md", ARCH),
          unchanged("ver01-adr-001-unchanged", "docs/specs/adr/ADR-001.md", ADR_1),
          unchanged("ver01-adr-002-unchanged", "docs/specs/adr/ADR-002.md", ADR_2),
          unchanged("ver01-prd-001-unchanged", "docs/specs/prd/PRD-001.md", PRD)]
    # VER-02: index.md
    no_l2 = r"(?:(?!\n##[ \t])[\s\S])*"
    g.append(rx("ver02-index-sections", "index",
                r"^---[\s\S]*?\n---[ \t]*\n" + no_l2 + r"\n##[ \t]+Documents[ \t]*\n" + no_l2
                + r"\n##[ \t]+Loading[ \t]*\n" + no_l2 + r"\n##[ \t]+Change Log[ \t]*\n" + no_l2 + "$"))
    for d in SHARED_SET[1:]:
        g.append(rx(f"ver02-index-row-{d}", "index",
                    r"\n\|[^\n]*\b" + esc(d) + r"\.md\b[^\n]*\|[ \t]*" + IDS[d] + r"[ \t]*\|[ \t]*1[ \t]*\|"))
    g.append(rx("ver02-index-no-other-rows", "index",
                r"\n\|[^\n]*\b(?:index|back-end|api|datastore)\.md\b[^\n]*\|[ \t]*CTX-\d{3}[ \t]*\|",
                match="not_contains", witness="| [api.md](api.md) | CTX-014 | 1 | api | Interfaces |\n"))
    g.append(rx("ver02-index-loading-rule", "index",
                section("Loading") + r"\*\*DevForgeAI rule — context loading:\*\*" + STMT_BODY
                + r"read this index first"))
    g.append(rx("ver02-index-at-most-100-lines", "index", r"^(?:[^\n]*\n){100}[^\n]", match="not_contains",
                witness="x\n" * 101))
    # VER-03: decisions cited
    g += [rx("ver03-python-decision", "tech-stack", tech("Python", r"3\.12\.x", "decision", link("ADR-001"))),
          rx("ver03-sqlite-decision", "tech-stack", tech("SQLite", r"3\.x", "decision", link("ADR-002"))),
          rx("ver03-typer-convention", "tech-stack", tech("Typer", r"0\.12\.x", "convention")),
          rx("ver03-alembic-convention", "tech-stack", tech("Alembic", r"1\.13\.x", "convention")),
          rx("ver03-pytest-convention", "tech-stack", tech("pytest", r"8\.x", "convention")),
          rx("ver03-pipx-decision", "tech-stack",
             tech("pipx", "unpinned", "decision", r"[^\n]*ARCH-001#CMP-01\b", r"[^\n]*ARCH-001#CMP-02\b",
                  link("ARCH-001", item="CMP-01"), link("ARCH-001", item="CMP-02"))),
          rx("ver03-rdbms-decision-statement", "rdbms", statement(r"Decision\*\*[ \t]*\([ \t]*ADR-002[ \t]*\):")),
          rx("ver03-rdbms-adr-002-link", "rdbms", fm_has(link("ADR-002")))]
    for n in ("01", "02", "03"):
        g.append(rx(f"ver03-architecture-links-cmp-{n}", "architecture", fm_has(link("ARCH-001", item=f"CMP-{n}"))))
    for d in SHARED_SET:
        g.append(rx(f"ver03-{d}-no-needs-adr", d, r"\[NEEDS ADR", match="not_contains",
                    witness="\n- **Proposed:** x [NEEDS ADR: x; affects y]\n"))
    # VER-18: the reply
    g += [rx("ver18-opens-with-block", "last_message", r"^\s*(?:```[^\n]*\n\s*)?(?:\*\*)?Context documents:"),
          rx("ver18-inspection-none", "last_message", block_line("Inspection", r"none\b")),
          rx("ver18-next-step-is-last", "last_message", NEXT_STEP_LAST),
          rx("ver18-next-step-outside-code", "last_message", NEXT_STEP_IN_CODE, match="not_contains",
             witness="\n```"),
          rx("ver18-next-step-names-epic", "last_message", next_step_names(EPIC_CMD))]
    # VER-19: frontmatter and Change Log of each document
    for d in SHARED_SET:
        conds = [nested("generated_by", "tool", "claude-code"),
                 nested("generated_by", "model", r"[A-Za-z0-9][^\"'\n,}]*"),
                 nested("generated_by", "session", UUID),
                 r"reviewed_by:[ \t]*\[\]" + EOL, fm_field("status", "draft"),
                 r"approved_by:[ \t]*(?:\"\"|'')" + EOL, r"approved_on:[ \t]*null" + EOL]
        if d != "index":
            conds.append(r"freshness_days:[ \t]*90" + EOL)
        g.append(rx(f"ver19-{d}-title", d, fm_has(r"title:[ \t]*[\"']" + esc(f"shiftlog: {TITLES[d]}") + r"[\"']" + EOL)))
        g.append(rx(f"ver19-{d}-provenance", d, fm_has(*conds)))
        g.append(rx(f"ver19-{d}-hashes-null", d, r"\bhash:[ \t]*(?!null\b)[^\s,}]", match="not_contains",
                    witness='\n  - {id: ADR-001, relation: constrains, version: 1, hash: "0912ab3c"}\n'))
        g.append(rx(f"ver19-{d}-change-log-row", d,
                    r"session:[ \t]*" + Q + "(" + UUID + ")" + Q + r"[\s\S]*\n\|[^\n]*\|[ \t]*claude-code \(session \1\)"
                    r"[ \t]*" + resolution_row(RESOLUTION)))
        g.append(rx(f"ver19-{d}-one-claude-row", d, r"claude-code \(session[\s\S]*claude-code \(session",
                    match="not_contains",
                    witness="| 1 | 2026-10-01 | claude-code (session x) | Again | all |\n"))
    g.append(rx("ver19-index-no-freshness", "index", fm_has(r"freshness_days:"), match="not_contains",
                witness=None))
    return g


def nothing_confirmed():
    g = []
    for d in SHARED_SET:
        g.append(rx(f"ver04-{d}-draft", d, fm_has(fm_field("status", "draft"))))
        g.append(rx(f"ver04-{d}-no-convention", d, r"\*\*Convention:\*\*", match="not_contains",
                    witness="\n- **Convention:** x\n"))
    for d, sections in PROPOSED_SECTIONS.items():
        for s in sections:
            title, table = (s[0], True) if isinstance(s, tuple) else (s, False)
            slug = re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-")
            g.append(rx(f"ver04-{d}-{slug}-proposed", d, proposed_in(esc(title), table)))
    g.append(rx("ver04-tech-stack-no-convention-item", "tech-stack", r"\n[ \t]*basis:[ \t]*" + Q + "convention",
                match="not_contains", witness="\n    basis: convention\n"))
    for slug in ("shiftlog-cli", "shift-service", "local-database"):
        for top in ("src", "tests"):
            g.append(rx(f"ver04-proposed-root-{top}-{slug}", "source-tree",
                        item("SRC", field_is("path", esc(f"{top}/{slug}/")), field_is("basis", "proposed"))))
    return g


def no_observed(ver):
    return [rx(f"{ver}-{d}-no-observed", d, r"observed_in|\*\*Observed\*\*|\|[ \t]*Observed[ \t]*\(",
               match="not_contains", witness="\n    observed_in: \"x\"\n") for d in SHARED_SET]


def observed_and_confirmed():
    return [
        rx("ver05-typer-observed", "tech-stack",
           tech("Typer", r"[^\n]+", "observed", field_is("observed_in", r"pyproject\.toml"),
                field_is("observed_on", DATE))),
        rx("ver05-pytest-convention-keeps-observed-in", "tech-stack",
           item("TEC", name_is("pytest"), field_is("basis", "convention"), field_is("observed_in", r"pyproject\.toml"))),
        rx("ver05-root-src-shiftlog-cli-observed", "source-tree",
           item("SRC", field_is("path", r"src/shiftlog/cli/"), field_is("holds", "code"), field_is("basis", "observed"),
                field_is("observed_in", r"[^\"'\n]+"), field_is("observed_on", DATE))),
        rx("ver05-root-tests-service-observed", "source-tree",
           item("SRC", field_is("path", r"tests/service/"), field_is("holds", "tests"), field_is("basis", "observed"),
                field_is("observed_in", r"[^\"'\n]+"), field_is("observed_on", DATE))),
        rx("ver05-inspection-names-paths", "last_message",
           block_line("Inspection", r"(?=[^\n]*pyproject\.toml)(?=[^\n]*src/shiftlog)(?=[^\n]*\btests/)")),
    ]


def needs_adr():
    docs = SHARED_SET + ["back-end"]
    g = [rx("ver07-back-end-jobs-and-queues-marker", "back-end",
            section("Jobs and queues") + r"\[NEEDS ADR:[^\]\n]*[Bb]roker")]
    for d in docs:
        if d == "back-end":
            g.append(rx("ver07-back-end-one-marker", d, r"\[NEEDS ADR[\s\S]*\[NEEDS ADR", match="not_contains",
                        witness="\n- **Proposed:** x [NEEDS ADR: x; affects y]\n"))
        else:
            g.append(rx(f"ver07-{d}-no-marker", d, r"\[NEEDS ADR", match="not_contains",
                        witness="\n- **Proposed:** x [NEEDS ADR: x; affects y]\n"))
    g += [rx("ver07-handed-back-lists-broker", "last_message",
             block_line("Handed back to architecture", r"[^\n]*[Bb]roker")),
          rx("ver07-next-step-is-last", "last_message", NEXT_STEP_LAST),
          rx("ver07-next-step-names-architecture", "last_message", next_step_names(ARCH_CMD))]
    return g


def approve():
    g = [rx("ver08-tech-stack-approved", "tech-stack", fm_has(fm_field("status", "approved"))),
         rx("ver08-tech-stack-approved-by", "tech-stack", fm_has(fm_field("approved_by", "Example Owner"))),
         rx("ver08-tech-stack-approved-on", "tech-stack", fm_has(fm_field("approved_on", DATE))),
         rx("ver08-tech-stack-approved-row", "tech-stack",
            r"\n\|[ \t]*\d+[ \t]*\|[ \t]*" + DATE + r"[ \t]*\|[ \t]*Example Owner[ \t]*\|[ \t]*Approved\.?[ \t]*\|")]
    for d in SHARED_SET:
        if d != "tech-stack":
            g.append(rx(f"ver08-{d}-draft", d, fm_has(fm_field("status", "draft"))))
    return g


def revision():
    return [rx("ver09-tech-stack-version-3", "tech-stack", fm_has(r"version:[ \t]*3" + EOL)),
            rx("ver09-tech-stack-draft", "tech-stack", fm_has(fm_field("status", "draft"))),
            rx("ver09-tech-stack-approved-by-empty", "tech-stack", fm_has(r"approved_by:[ \t]*(?:\"\"|'')" + EOL)),
            lock_file_convention("ver09"),
            rx("ver09-tech-stack-new-change-log-row", "tech-stack",
               r"\n\|[ \t]*3[ \t]*\|[^\n]*\|[ \t]*claude-code \(session " + UUID + r"\)[ \t]*\|"),
            rx("ver09-reply-story-001-proposal", "last_message",
               r"STORY-001[^\n]*\b[Pp]roposals?\b|\b[Pp]roposals?\b[^\n]*STORY-001"),
            unchanged("ver09-story-001-unchanged", "docs/specs/story/STORY-001.md", STORY_1)]


def suspect_review():
    return [present("ver10-api-written", f"{CTX}/api.md"),
            rx("ver10-api-version-1-draft", "api", fm_has(r"version:[ \t]*1" + EOL, fm_field("status", "draft"))),
            rx("ver10-architecture-version-2", "architecture", fm_has(r"version:[ \t]*2" + EOL)),
            rx("ver10-architecture-row-cmp-04", "architecture", section("Components") + r"\n\|[^\n]*ARCH-001#CMP-04\b"),
            rx("ver10-rdbms-version-1-approved", "rdbms",
               fm_has(r"version:[ \t]*1" + EOL, fm_field("status", "approved"))),
            rx("ver10-rdbms-arch-link-version-2", "rdbms", fm_has(link("ARCH-001", version=2))),
            rx("ver10-rdbms-relink-row", "rdbms", r"\n\|[^\n]*Re-reviewed against ARCH-001 v2: no change")]


def amb_expected():
    text = replace(AMB_3, '    state: accepted\n    decided_by: "Example Owner"\n    decided_on: 2026-09-29\n'
                          '    resolution: ""\n',
                   '    state: accepted\n    decided_by: "Example Owner"\n    decided_on: 2026-09-29\n'
                   '    resolution: @@ALREADY@@\n')
    text = replace(text, '    decided_on: 2026-09-30\n    resolution: ""\n',
                   '    decided_on: 2026-09-30\n    resolution: @@NEW@@\n')
    return text


def quoted(value):
    return r"(?:\"" + esc(value) + r"\"|'" + esc(value) + r"')"


def fold():
    pattern = "^" + esc(amb_expected()).replace("@@ALREADY@@", quoted(FOLD_ALREADY)).replace("@@NEW@@", quoted(FOLD_NEW)) + "$"
    amb = "docs/specs/ambiguities/AMB-001.md"
    return [rx("ver11-tech-stack-version-3", "tech-stack", fm_has(r"version:[ \t]*3" + EOL)),
            lock_file_convention("ver11"),
            rx("ver11-ent-03-resolution", amb, item("ENT", r"[ \t]*question:[ \t]*" + Q + "Commit the lock file",
                                                    r"[ \t]*resolution:[ \t]*" + quoted(FOLD_NEW) + EOL)),
            rx("ver11-ent-01-resolution", amb, item("ENT", r"[ \t]*question:[ \t]*" + Q + "Typer 0\\.12\\.5",
                                                    r"[ \t]*resolution:[ \t]*" + quoted(FOLD_ALREADY) + EOL)),
            rx("ver11-ent-02-open-and-empty", amb,
               item("ENT", r"[ \t]*question:[ \t]*" + Q + "source-tree\\.md names no fixtures",
                    field_is("state", "open"), r"[ \t]*resolution:[ \t]*(?:\"\"|'')" + EOL)),
            rx("ver11-amb-001-otherwise-unchanged", amb, pattern)]


def designs():
    row = r"\n\|[ \t]*{story}[ \t]*\|[^|\n]*{screen}[^|\n]*\|[^|\n]*{path}[^|\n]*\|[ \t]*{date}[ \t]*\|[ \t]*none[ \t]*\|"
    return [rx("ver16-ui-mockups-version-2", "ui-mockups", fm_has(r"version:[ \t]*2" + EOL)),
            rx("ver16-row-story-001", "ui-mockups", row.format(story="STORY-001", screen="shiftlog list",
               path=esc("docs/specs/story/design/STORY-001/list-output.png"), date="2026-09-29")),
            rx("ver16-row-story-002", "ui-mockups", row.format(story="STORY-002", screen="shiftlog add",
               path=esc("docs/specs/story/design/STORY-002/add-prompt.png"), date="2026-09-30")),
            rx("ver16-row-story-003", "ui-mockups", row.format(story="STORY-003", screen=r"\(not recorded\)",
               path=esc("docs/specs/story/design/STORY-003/edit.png"), date="2026-09-30")),
            rx("ver16-no-story-004-row", "ui-mockups", r"\n\|[ \t]*STORY-004[ \t]*\|", match="not_contains",
               witness="| STORY-004 | x | docs/specs/story/design/STORY-004/edit.png | 2026-09-30 | none |\n"),
            rx("ver16-three-rows", "ui-mockups", r"(?:\n\|[ \t]*STORY-\d{3}[ \t]*\|[^\n]*){4}", match="not_contains",
               witness=None),
            rx("ver16-no-story-link", "ui-mockups", r"^---[ \t]*\n" + FM_LINE + r"*?[^\n]*\bSTORY-\d{3}",
               match="not_contains", witness=None),
            rx("ver16-reports-story-004", "last_message", r"STORY-004")]


def one_document():
    g = [rx("ver17-tech-stack-version-3", "tech-stack", fm_has(r"version:[ \t]*3" + EOL)),
         lock_file_convention("ver17"),
         rx("ver17-index-row-tech-stack-version-3", "index",
            r"\n\|[^\n]*\btech-stack\.md\b[^\n]*\|[ \t]*CTX-003[ \t]*\|[ \t]*3[ \t]*\|")]
    for d in EXAMPLE_DOCS:
        if d not in ("tech-stack", "index"):
            g.append(unchanged(f"ver17-{d}-unchanged", f"{CTX}/{d}.md", CONTEXT[d]))
    g.append(unchanged("ver17-rdbms-migrations-unchanged", f"{CTX}/rdbms/migrations.md", MIGRATIONS))
    return g


FRONT_END_INVALID = replace(CONTEXT["front-end"], "status: approved", "status: in-review")
NOTES = "Scratch notes from the planning call.\n"
SOURCE_TREE_STALE = replace(CONTEXT["source-tree"], "freshness_days: 90", "freshness_days: 30")
SOURCE_TREE_STALE = replace(SOURCE_TREE_STALE, """\
    basis: observed
    observed_in: "tests/service/"
    observed_on: 2026-09-29""", """\
    basis: observed
    observed_in: "tests/service/"
    observed_on: 2026-01-01""")


def findings():
    return [rx("ver24-reports-front-end-status", "last_message",
               r"front-end\.md[^\n]*(?:status|in-review)|(?:status|in-review)[^\n]*front-end\.md"),
            rx("ver24-reports-notes-by-path", "last_message", r"(?:docs/specs/context/)?notes\.md"),
            rx("ver24-reports-stale-observation", "last_message",
               r"tests/service/[^\n]*2026-01-01|2026-01-01[^\n]*tests/service/"),
            unchanged("ver24-front-end-unchanged", f"{CTX}/front-end.md", FRONT_END_INVALID),
            unchanged("ver24-notes-unchanged", f"{CTX}/notes.md", NOTES),
            unchanged("ver24-source-tree-unchanged", f"{CTX}/source-tree.md", SOURCE_TREE_STALE)]


def testing_policy():
    g = [rx("ver15-testing-threshold-from-pol-001", "testing",
            r"\n\|[ \t]*`?testing\.coverage_threshold`?[ \t]*\|[ \t]*`?90%?`?[ \t]*\|[ \t]*`?POL-001#SET-01`?[ \t]*\|"),
         rx("ver15-testing-method-tdd-default", "testing",
            r"\n\|[ \t]*`?testing\.method`?[ \t]*\|[ \t]*`?tdd`?[ \t]*\|[ \t]*`?\(default\)`?[ \t]*\|")]
    for key in ("coverage_metric", "coverage_scope", "coverage_exclusions", "exception_approvers"):
        g.append(rx(f"ver15-testing-{key.replace('_', '-')}-default", "testing",
                    r"\n\|[ \t]*`?testing\." + key + r"`?[ \t]*\|[^|\n]*\|[ \t]*`?\(default\)`?[ \t]*\|"))
    g += [rx("ver15-testing-constrains-pol-001-set-01", "testing", fm_has(link("POL-001", item="SET-01"))),
          rx("ver15-testing-pass-rule", "testing", section("The pass rule") + r"\*\*DevForgeAI rule — pass rule:\*\*"),
          rx("ver15-testing-investigating-rule", "testing",
             section("Investigating a failing test") + r"\*\*DevForgeAI rule — investigating a failing test:\*\*")]
    for d in SHARED_SET:
        g.append(rx(f"ver15-{d}-resolution-line", d,
                    r"\n\|[^\n]*\|[ \t]*claude-code \(session [^)\n]*\)[ \t]*" + resolution_row(RESOLUTION_POL)))
    return g


TRIGGERS = [
    (True, "Write the context documents for this project."),
    (True, "Set up our tech stack and source tree documents."),
    (True, "Document the coding conventions for this repository."),
    (True, "Update testing.md with how we run the tests."),
    (True, "The story step says the context documents are missing. Create them."),
    (True, "Refresh the project context after the architecture change."),
    (True, "Approve tech-stack.md."),
    (True, "Create docs/specs/context/ for this project."),
    (False, "Give me some background context on the Roman empire."),
    (False, "What's in my context window right now?"),
    (False, "Explain how React's Context API works."),
    (False, "Write an ADR that chooses PostgreSQL."),
]

CASES = [
    Case("writes-the-set", ["01", "02", "03", "18", "19"],
         "VER-01, VER-02, VER-03, VER-18, VER-19: the shared fixture and prompt write exactly the nine documents "
         "the ARCH's kinds need, each with its fixed ID, title, provenance and resolution line; decisions are cited "
         "with constrains links; the reply opens with the report block and ends with the epic next step.",
         SHARED_PROMPT, SHARED, writes_the_set()),
    Case("nothing-confirmed", ["04"],
         "VER-04: with no conventions confirmed and no questions, every undecided section is a Proposed statement "
         "with a marker, nothing is a convention, and source-tree.md proposes a code and a tests root per component.",
         "Write the project context documents. Don't inspect any code. Proceed without questions.", SHARED,
         nothing_confirmed()),
    Case("observed-and-confirmed", ["05"],
         "VER-05: inspection reads only the named paths; observed facts carry their path and date; pytest, "
         "confirmed in the request, becomes a convention that keeps observed_in.",
         "Write the project context documents. You may read pyproject.toml, src/shiftlog/ and tests/. Keep pytest "
         "as our convention. Proceed without questions.", dict(SHARED, **CODE), observed_and_confirmed()),
    Case("no-scope-no-inspection", ["06"],
         "VER-06: with no paths named and no questions, nothing is inspected: no Observed statement or observed_in "
         "anywhere, and the report says Inspection: none.",
         "Write the project context documents. Proceed without questions.", dict(SHARED, **CODE),
         no_observed("ver06") + [rx("ver06-inspection-none", "last_message", block_line("Inspection", r"none\b"))]),
    Case("needs-adr-handback", ["07"],
         "VER-07: an undecided message broker becomes the only [NEEDS ADR] marker, in back-end.md section 4; the "
         "reply hands it back to architecture and the next step is /devforgeai:architecture PRD-001.",
         SHARED_PROMPT, dict(SHARED, **{"docs/specs/arch/ARCH-001.md": ARCH_REMINDER}), needs_adr()),
    Case("approve-on-explicit-words", ["08"],
         "VER-08: an explicit approval of tech-stack.md by a named approver approves only that document.",
         SHARED_PROMPT + "\n\nI'm Example Owner, and I approve tech-stack.md.", SHARED, approve()),
    Case("revision-clears-approval", ["09"],
         "VER-09: a change to approved tech-stack.md raises it to version 3, returns it to draft and names "
         "STORY-001, which cites it, as a proposal; STORY-001 is unchanged.",
         "Update the context documents: in tech-stack.md, add the convention that the lock file is committed with "
         "every dependency change. Proceed without questions.", EXAMPLE_PROJECT, revision()),
    Case("suspect-review", ["10"],
         "VER-10: ARCH-001 v2 adds an api component: api.md is written, architecture.md gains its row, and "
         "rdbms.md, whose statements don't change, is relinked without a version or status change.",
         "ARCH-001 changed; update the context documents. Proceed without questions.",
         dict(EXAMPLE_PROJECT, **{"docs/specs/arch/ARCH-001.md": ARCH_V2}), suspect_review()),
    Case("fold-accepted-entries", ["11"],
         "VER-11: accepted ambiguity entries for CTX-003 are folded: a new convention for ENT-03, 'already stated' "
         "for ENT-01; only their resolution fields change, and the open ENT-02 is left alone.",
         "Update the context documents. Proceed without questions.",
         dict(EXAMPLE_PROJECT, **{"docs/specs/ambiguities/AMB-001.md": AMB_3}), fold()),
    Case("no-arch-hands-back", ["12"],
         "VER-12: with no ARCH, nothing is written and the reply hands back to /devforgeai:architecture PRD-001.",
         SHARED_PROMPT, NO_ARCH,
         [present("ver12-nothing-written", f"{CTX}/**", exists=False),
          rx("ver12-names-architecture-prd-001", "last_message", ARCH_CMD)]),
    Case("kinds-missing", ["13"],
         "VER-13: a component without kinds gets a [NEEDS CLARIFICATION] marker in architecture.md's Kinds column "
         "and no layer document.",
         SHARED_PROMPT, dict(SHARED, **{"docs/specs/arch/ARCH-001.md": ARCH_NO_KINDS}),
         [rx("ver13-architecture-cmp-02-kinds-marker", "architecture",
             r"\n\|[^\n]*ARCH-001#CMP-02\b[^\n]*\[NEEDS CLARIFICATION: kinds of ARCH-001#CMP-02\][^\n]*\|"),
          present("ver13-no-middle-tier", f"{CTX}/middle-tier.md", exists=False)]),
    Case("invalid-policy-stops", ["14"],
         "VER-14: an approved policy with an impossible date stops the run before anything is written, naming the "
         "file and the field.",
         SHARED_PROMPT, dict(SHARED, **{"docs/specs/policy/POL-001.md": POLICY_BAD_DATE}),
         [present("ver14-nothing-written", f"{CTX}/**", exists=False),
          rx("ver14-names-pol-001", "last_message", r"POL-001\.md"),
          rx("ver14-names-field-updated", "last_message",
             r"\bupdated\b[^\n]*(?:2026-13-45|\bdate\b)|2026-13-45[^\n]*\bupdated\b")],
         invalid={"docs/specs/policy/POL-001.md": "updated"}, policy_exit=1),
    Case("testing-policy-cited", ["15"],
         "VER-15: an organization setting for the coverage threshold appears in testing.md's policy table with its "
         "constrains link, the other testing keys as defaults, and on every document's resolution line.",
         SHARED_PROMPT, dict(SHARED, **{"docs/specs/policy/POL-001.md": POLICY}), testing_policy(), policy_exit=0),
    Case("designs-generated", ["16"],
         "VER-16: ui-mockups.md's approved-design table is rebuilt from the stories' records in both line forms; a "
         "record in neither form is reported and gets no row.",
         "Update the context documents. Proceed without questions.",
         dict(EXAMPLE_PROJECT, **{"docs/specs/story/STORY-002.md": STORY_2, "docs/specs/story/STORY-003.md": STORY_3,
                                  "docs/specs/story/STORY-004.md": STORY_4}), designs()),
    Case("one-document", ["17"],
         "VER-17: a request to update only tech-stack.md changes tech-stack.md and index.md, and nothing else.",
         "Update only tech-stack.md: add the convention that the lock file is committed with every dependency "
         "change. Proceed without questions.", EXAMPLE_PROJECT, one_document()),
    Case("ignores-unrelated-request", ["20"],
         "VER-20: a request for background context on a historical topic doesn't invoke the skill.",
         "Give me some context on the French revolution.", SHARED,
         # A tool_used grader doesn't count toward the score when the baseline arm runs, so the case also
         # checks that nothing is written, as every other suite's unrelated-request case does.
         [skill_fired("ver20-skill-not-fired", False), present("ver20-nothing-written", f"{CTX}/**", exists=False)],
         limits=SHORT_LIMITS),
    Case("unknown-document", ["23"],
         "VER-23: a document name outside the set writes nothing and lists the set's names with a question.",
         "Update only the context document named banana.", SHARED,
         [present("ver23-no-index", f"{CTX}/index.md", exists=False),
          rx("ver23-names-documents", "last_message",
             r"^(?=[\s\S]*\btech-stack\b)(?=[\s\S]*\btesting\b)(?=[\s\S]*\bsource-tree\b)"),
          rx("ver23-asks-which", "last_message", r"\b[Ww]hich\b[^?\n]*\?")]),
    Case("existing-set-findings", ["24"],
         "VER-24: an existing document that fails its check is reported and left unchanged, a stray file is "
         "reported by path, and a stale observation is reported; none of the three changes.",
         "Update the context documents. Proceed without questions.",
         dict(EXAMPLE_PROJECT, **{f"{CTX}/front-end.md": FRONT_END_INVALID, f"{CTX}/notes.md": NOTES,
                                  f"{CTX}/source-tree.md": SOURCE_TREE_STALE}), findings(),
         invalid={f"{CTX}/front-end.md": "status"}),
] + [
    Case(f"trigger-{i:02d}", ["26"],
         f"VER-26 ({'positive' if fired else 'negative'}): the skill {'fires' if fired else 'does not fire'}.",
         prompt, NO_ARCH, [skill_fired("ver26-skill-fired" if fired else "ver26-skill-not-fired", fired)],
         limits=SHORT_LIMITS, tags=["trigger", "ver-26"])
    for i, (fired, prompt) in enumerate(TRIGGERS, start=1)
]

# --------------------------------------------------------------------------------------------------------
# Validation of the fixtures


def registry():
    reg = Registry()
    for p in SCHEMAS.glob("*.json"):
        s = json.loads(p.read_text())
        reg = reg.with_resource(s["$id"], Resource.from_contents(s)).with_resource(p.name, Resource.from_contents(s))
    return reg


class _Loader(yaml.SafeLoader):
    pass


_Loader.yaml_implicit_resolvers = {k: [r for r in v if r[0] != "tag:yaml.org,2002:timestamp"]
                                   for k, v in yaml.SafeLoader.yaml_implicit_resolvers.items()}
SCHEMA_FOR = {"prd": "prd", "arch": "arch", "adr": "adr", "story": "story", "policy": "policy",
              "ambiguities": "ambiguities", "context": "context"}


def parse(text):
    m = re.match(r"---\n(.*?)\n---\n", text, re.S)
    doc = {"frontmatter": yaml.load(m.group(1), Loader=_Loader)}
    for block in re.findall(r"^```yaml items\n(.*?)^```", text, re.S | re.M):
        for key, value in yaml.load(block, Loader=_Loader).items():
            doc.setdefault(key, []).extend(value)
    return doc


def schema_for(path):
    parts = Path(path).parts
    if parts[:2] != ("docs", "specs") or len(parts) != 4:
        return None  # code files, and detail files one level below a context document
    if parts[2] == "context" and Path(path).stem not in IDS:
        return None
    return SCHEMA_FOR.get(parts[2])


def validate(case, path, text, reg):
    kind = schema_for(path)
    if kind is None:
        return
    v = Draft202012Validator(json.loads((SCHEMAS / f"{kind}.schema.json").read_text()), registry=reg,
                             format_checker=FormatChecker())
    errors = sorted(".".join(str(p) for p in e.absolute_path) for e in v.iter_errors(parse(text)))
    if path in case.invalid:
        expected = f"frontmatter.{case.invalid[path]}"
        assert errors == [expected], f"{case.name}: {path} should fail only at {expected}, got {errors}"
    else:
        assert not errors, f"{case.name}: {path} is invalid: {errors}"


def check_policy_script(case, ws):
    if case.policy_exit is None:
        return
    p = subprocess.run([sys.executable, "-B", str(Path.cwd() / POLICY_SCRIPT), "docs/specs/policy"], cwd=ws,
                       capture_output=True, text=True)
    assert p.returncode == case.policy_exit, f"{case.name}: validate_policy.py exit {p.returncode}:\n{p.stdout}"
    if case.policy_exit == 1:
        assert "frontmatter: updated:" in p.stdout, p.stdout


def check_context_script(case, ws):
    if not RUN_CONTEXT_CHECK or not (Path(ws) / CTX).exists():
        return
    p = subprocess.run([sys.executable, "-B", str(Path.cwd() / CONTEXT_CHECK), "check"], cwd=ws,
                       capture_output=True, text=True)
    bad = [k for k in case.invalid if k.startswith(CTX)]
    if bad:
        assert p.returncode == 1 and all(b in p.stdout for b in bad), f"{case.name}: {p.stdout}"
        assert all(line.startswith(tuple(bad)) for line in p.stdout.splitlines()[:-1]), p.stdout
    else:
        assert p.returncode == 0, f"{case.name}: context_check.py check:\n{p.stdout}"


# --------------------------------------------------------------------------------------------------------
# Writing the cases


def scaffold(case):
    lines = ["#!/usr/bin/env bash", f"# Seeds the fixtures for SPEC-011 {', '.join('VER-' + v for v in case.vers)} "
             f"({case.name}). Generated by src/tests/context/make_evals.py; edit the generator, not this file.",
             "set -euo pipefail"]
    for path, text in sorted(case.files.items()):
        assert text.endswith("\n") and "\nCTXFIXTURE\n" not in text, path
        parent = str(Path(path).parent)
        if parent != ".":
            lines.append(f"mkdir -p {parent}")
        lines.append(f"cat > {path} <<'CTXFIXTURE'\n{text}CTXFIXTURE")
    return "\n".join(lines) + "\n"


def grader_file(g):
    if g.type == "regex":
        target = "last_message" if g.target == "last_message" else f"{{source: file, path: {g.target}}}"
        head = [f"type: regex", f"target: {target}", f"match: {g.match}"] + ([f"flags: {g.flags}"] if g.flags else [])
        assert "\n" not in g.pattern
        return "---\n" + "\n".join(head) + "\n---\n" + g.pattern + "\n"
    if g.type == "file_exists":
        return f"---\ntype: file_exists\npath: {g.target}\nexists: {'true' if g.exists else 'false'}\n---\n"
    head = ["type: tool_used", "tool: Skill", f"input_match: {SKILL_MATCH}"]
    head += [f"min: {g.min}"] + ([f"max: {g.max}"] if g.max is not None else []) + ["arm: both"]
    return "---\n" + "\n".join(head) + "\n---\n"


def prompt_file(case):
    tags = case.tags or (["context"] + [f"ver-{v}" for v in case.vers])
    turns, seconds = case.limits
    return (f"---\ndescription: {json.dumps(case.description)}\ntags: [{', '.join(tags)}]\nmax_turns: {turns}\n"
            f"timeout_seconds: {seconds}\nallowed_tools: {TOOLS}\n---\n{case.prompt}\n")


def run_scaffold(case_dir, ws):
    subprocess.run(["bash", str(Path(case_dir).resolve() / "scaffold.sh")], cwd=ws, check=True)


def main():
    if not SCHEMAS.is_dir():
        sys.exit("Run from the repository root.")
    names = [c.name for c in CASES]
    assert len(names) == len(set(names)) == 30, names
    for c in CASES:
        gnames = [g.name for g in c.graders]
        assert len(gnames) == len(set(gnames)), c.name
        assert all(n.startswith(tuple(f"ver{v}-" for v in c.vers)) for n in gnames), c.name
    reg = registry()
    if ROOT.exists():
        shutil.rmtree(ROOT)
    for c in CASES:
        d = ROOT / c.name
        (d / "graders").mkdir(parents=True)
        (d / "prompt.md").write_text(prompt_file(c))
        (d / "case.yaml").write_text(f'schema_version: "1.1"\nname: {c.name}\ncontext:\n  scaffold_script: scaffold.sh\n')
        (d / "scaffold.sh").write_text(scaffold(c))
        (d / "scaffold.sh").chmod(0o755)
        for g in c.graders:
            (d / "graders" / f"{g.name}.md").write_text(grader_file(g))
        with tempfile.TemporaryDirectory() as ws:
            run_scaffold(d, ws)
            for path, text in c.files.items():
                written = (Path(ws) / path).read_text()
                assert written == text, f"{c.name}: the scaffold changed {path}"
                validate(c, path, written, reg)
            check_policy_script(c, ws)
            check_context_script(c, ws)
    print(f"wrote {len(CASES)} cases ({sum(len(c.graders) for c in CASES)} graders) to {ROOT}; fixtures valid"
          + ("; context_check.py passes" if RUN_CONTEXT_CHECK else "; context_check.py pass off (§11 step 6)"))


if __name__ == "__main__":
    main()
