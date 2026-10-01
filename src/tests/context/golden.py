"""Simulated runs of the context eval cases, for check_graders.py.

good(case) gives what a correct run leaves: the files it writes or changes (path -> text) and its final
reply. bad(case) gives targeted wrong runs, each a list of edits to the good run and the exact set of
graders it must fail. The documents follow SPEC-011 §4 and the templates for the fixtures in make_evals.py;
they are hand-built here, independent of the skill.
"""
import make_evals as M

TODAY = "2026-10-01"
SESSION = "3f1c2b9a-7d4e-4c1a-9b2f-0a1b2c3d4e5f"
ROW = f"claude-code (session {SESSION})"
CTX = M.CTX
ARCH_LINK = "{id: ARCH-001, relation: constrains, version: 1, hash: null}"


def between(text, start, end):
    i = text.index(start)
    return text[i:text.index(end, i)]


PASS_RULE = between(M.CONTEXT["testing"], "- **DevForgeAI rule — pass rule:**", "\n## 2.")
INVESTIGATE_RULE = between(M.CONTEXT["testing"], "- **DevForgeAI rule — investigating", "\n## 3.")
NAMING_RULE = between(M.CONTEXT["testing"], "- **DevForgeAI rule — test naming:**", "- **Convention:**")
UPGRADE_RULE = between(M.CONTEXT["tech-stack"], "- **DevForgeAI rule — ambiguities log:**", "- **Convention:**")
LOADING_RULE = between(M.CONTEXT["index"], "- **DevForgeAI rule — context loading:**", "\n## Change Log")

CMPS = [("01", "shiftlog CLI", "user-interface",
         "Commands to start, stop and list shifts, and the weekly report; formats all output",
         "The shiftlog Python package, installed with pipx", "front-end.md, ui-mockups.md"),
        ("02", "Shift service", "service", "Shift rules: no overlapping shifts, rounding to the minute, weekly totals",
         "The shiftlog Python package, installed with pipx", "middle-tier.md"),
        ("03", "Local database", "relational-store", "Stores shifts in a SQLite file in the user's data folder",
         "SQLite file under the user's data folder", "rdbms.md")]
REMINDER = ("04", "Reminder worker", "platform",
            "Sends reminders for shifts left running, from jobs the Shift service queues for it, on the user's machine",
            "A background process; the message broker is undecided", "back-end.md")
PURPOSE = {"architecture": ("all", "Components and the conventions that cut across layers"),
           "tech-stack": ("all", "Technologies, their allowed versions, and where each was chosen"),
           "source-tree": ("all", "Where code, tests, configuration and documentation live"),
           "testing": ("all", "How testing is done, and the testing policy in force"),
           "front-end": ("user-interface", "Command structure, flags, output and exit codes of the CLI"),
           "middle-tier": ("service", "How the shift service is organized"),
           "back-end": ("platform", "How the reminder worker runs, and its jobs and queues"),
           "api": ("api", "Conventions for the export interface"),
           "rdbms": ("relational-store", "SQLite naming, migrations and transactions"),
           "ui-mockups": ("user-interface", "The design system, and the approved designs")}
ORDER = ["architecture", "tech-stack", "source-tree", "testing", "front-end", "middle-tier", "back-end", "api",
         "rdbms", "ui-mockups"]


def proposed(text, what):
    return f"- **Proposed:** {text} [NEEDS CLARIFICATION: confirm {what}]\n"


def frontmatter(name, upstream, *, status="draft", approved_by="", approved_on="null"):
    lines = [f"id: {M.IDS[name]}", "type: context", f'title: "shiftlog: {M.TITLES[name]}"', f"status: {status}",
             "version: 1", f"created: {TODAY}", f"updated: {TODAY}", 'owner: "Example Owner"',
             'authors: ["Example Owner", "claude-code"]', "generated_by:", '  tool: "claude-code"',
             '  model: "claude-opus-5-5"', f'  session: "{SESSION}"', "reviewed_by: []",
             f'approved_by: "{approved_by}"', f"approved_on: {approved_on}", "upstream:"]
    lines += [f"  - {u}" for u in upstream]
    lines += ["supersedes: []", "superseded_by: null", "blocked_by: []", "# --- context-specific ---",
              f"document: {name}"] + ([] if name == "index" else ["freshness_days: 90"])
    return "---\n" + "\n".join(lines) + "\n---\n"


def change_log(res, extra=""):
    return ("## Change Log\n\n| Version | Date | Author | Change | Items affected |\n|---|---|---|---|---|\n"
            f"| 1 | {TODAY} | {ROW} | Initial draft from ARCH-001 v1. {res} | all |\n" + extra)


def tec(n, name, vr, used, basis, upstream=(), observed=None, notes=""):
    lines = [f"  - id: TEC-{n:02d}", "    status: active", f'    name: "{name}"', f'    version_range: "{vr}"',
             "    used_by:"] + [f'      - "ARCH-001#CMP-{c}"' for c in used] + [f"    basis: {basis}"]
    if upstream:
        lines += ["    upstream:"] + [f"      - {u}" for u in upstream]
    if observed:
        lines += [f'    observed_in: "{observed}"', f"    observed_on: {TODAY}"]
    return "\n".join(lines + [f'    notes: "{notes}"']) + "\n"


def root(n, path, holds, cmp, basis, observed=None):
    lines = [f"  - id: SRC-{n:02d}", "    status: active", f'    path: "{path}"', f"    holds: {holds}",
             f'    component: "ARCH-001#CMP-{cmp}"', f"    basis: {basis}"]
    if observed:
        lines += [f'    observed_in: "{observed}"', f"    observed_on: {TODAY}"]
    notes = "[NEEDS CLARIFICATION: confirm this folder]" if basis == "proposed" else ""
    return "\n".join(lines + [f'    notes: "{notes}"']) + "\n"


def covered(cmps, kind):
    return "".join(f"- ARCH-001#CMP-{c[0]} {c[1]}\n" for c in cmps if c[2] == kind)


def shared_set(*, confirmed=True, policy=False, reminder=False, kinds_missing=False, observed=False,
               approve=False):
    """The documents a correct run writes for the shared fixture (§9), and the names in the set."""
    res = M.RESOLUTION_POL if policy else M.RESOLUTION
    cmps = CMPS + ([REMINDER] if reminder else [])
    names = list(M.SHARED_SET) + (["back-end"] if reminder else [])
    if kinds_missing:
        names.remove("middle-tier")
    cmp_ids = [c[0] for c in cmps]
    docs = {}

    rows = []
    for c in cmps:
        kinds, documents = c[2], c[5]
        if kinds_missing and c[0] == "02":
            kinds, documents = "[NEEDS CLARIFICATION: kinds of ARCH-001#CMP-02]", "none"
        rows.append(f"| {c[1]} | ARCH-001#CMP-{c[0]} | {kinds} | {c[3]} | {c[4]} | {documents} |")
    docs["architecture"] = (
        frontmatter("architecture", [f"{{id: ARCH-001, item: CMP-{n}, relation: constrains, version: 1, hash: null}}"
                                     for n in cmp_ids])
        + "\n# CTX-002 — Architecture overview\n\n## 1. Components\n\n"
        "| Component | Item | Kinds | Responsibility | Deployment | Documents |\n|---|---|---|---|---|---|\n"
        + "\n".join(rows) + "\n\nOpen architectural questions are the DEC items of ARCH-001; none is open.\n\n"
        "## 2. Error handling\n\n"
        + proposed("the service raises one exception type per rule it enforces, and the CLI turns each into one\n"
                   "  message and exit code.", "how errors cross from the service to the CLI")
        + "\n## 3. Logging\n\n" + proposed("nothing is logged to standard output; debug logs go to standard error.",
                                           "the logging rules")
        + "\n## 4. Configuration\n\n" + proposed("the database path comes from an environment variable.",
                                                 "where configuration lives")
        + "\n## 5. Security basics\n\n" + proposed("the database file is readable by its owner only.",
                                                   "the security basics")
        + "\n" + change_log(res))

    upgrades = ("- **Convention:** dependency updates go in their own pull request, never mixed with a story's changes.\n"
                if confirmed else proposed("dependency updates go in their own pull request.",
                                           "how dependency updates are made"))
    items = [tec(1, "Python", "3.12.x", cmp_ids, "decision", ["{id: ADR-001, relation: constrains, version: 1, hash: null}"]),
             tec(2, "SQLite", "3.x", ["03"], "decision", ["{id: ADR-002, relation: constrains, version: 1, hash: null}"]),
             tec(3, "pipx", "unpinned", ["01", "02"], "decision",
                 ["{id: ARCH-001, item: CMP-01, relation: constrains, version: 1, hash: null}",
                  "{id: ARCH-001, item: CMP-02, relation: constrains, version: 1, hash: null}"])]
    if confirmed:
        items += [tec(4, "Typer", "0.12.x", ["01"], "convention"), tec(5, "Alembic", "1.13.x", ["03"], "convention"),
                  tec(6, "pytest", "8.x", ["01", "02", "03"], "convention")]
    if observed:
        items += [tec(4, "Typer", "==0.12.3", ["01"], "observed", observed="pyproject.toml"),
                  tec(5, "pytest", ">=8,<9", ["01", "02", "03"], "convention", observed="pyproject.toml")]
    approval = dict(status="approved", approved_by="Example Owner", approved_on=TODAY) if approve else {}
    docs["tech-stack"] = (
        frontmatter("tech-stack", [ARCH_LINK], **approval)
        + "\n# CTX-003 — Tech stack\n\n## Contents\n\n- [1. Technologies](#1-technologies)\n"
        "- [2. Upgrades](#2-upgrades)\n\n## 1. Technologies\n\n```yaml items\ntechnologies:\n" + "".join(items)
        + "```\n\n## 2. Upgrades\n\n" + UPGRADE_RULE + upgrades + "\n"
        + change_log(res, f"| 1 | {TODAY} | Example Owner | Approved | — |\n" if approve else ""))

    roots, n = [], 0
    have = {}
    if observed:
        roots += [root(1, "src/shiftlog/cli/", "code", "01", "observed", "src/shiftlog/"),
                  root(2, "tests/service/", "tests", "02", "observed", "tests/")]
        have = {("01", "code"), ("02", "tests")}
        n = 2
    for c in cmps:
        slug = M.re.sub(r"[^a-z0-9]+", "-", c[1].lower()).strip("-")
        for top, holds in (("src", "code"), ("tests", "tests")):
            if (c[0], holds) not in have:
                n += 1
                roots.append(root(n, f"{top}/{slug}/", holds, c[0], "proposed"))
    docs["source-tree"] = (
        frontmatter("source-tree", [ARCH_LINK])
        + "\n# CTX-004 — Source tree\n\n## Contents\n\n- [1. Roots](#1-roots)\n"
        "- [2. Layout conventions](#2-layout-conventions)\n- [3. Generated files](#3-generated-files)\n\n"
        "## 1. Roots\n\n```yaml items\nroots:\n" + "".join(roots) + "```\n\n## 2. Layout conventions\n\n"
        + proposed("one package per component under `src/`, and one test folder per component under `tests/`.",
                   "the layout")
        + "\n## 3. Generated files\n\n" + proposed("generated folders are never edited by hand or committed.",
                                                   "which folders are generated")
        + "\n" + change_log(res))

    threshold = ("| testing.coverage_threshold | 90 | POL-001#SET-01 |" if policy else
                 '| testing.coverage_threshold | none: not enforced, reported as "no coverage threshold set" | (default) |')
    levels = "".join(f"| {c[2]} | unit | tests/{M.re.sub(r'[^a-z0-9]+', '-', c[1].lower())}/ | Proposed "
                     f"[NEEDS CLARIFICATION: confirm the levels for {c[2]}] |\n"
                     for c in cmps if not (kinds_missing and c[0] == "02"))
    commands = "".join(f"| ARCH-001#CMP-{c[0]} | `pytest tests/{M.re.sub(r'[^a-z0-9]+', '-', c[1].lower())}` | "
                       f"Proposed [NEEDS CLARIFICATION: confirm the command] |\n" for c in cmps)
    pol_link = ["{id: POL-001, item: SET-01, relation: constrains, version: 1, hash: null}"] if policy else []
    docs["testing"] = (
        frontmatter("testing", [ARCH_LINK] + pol_link)
        + "\n# CTX-005 — Testing\n\n## 1. The pass rule\n\n" + PASS_RULE + "\n## 2. Investigating a failing test\n\n"
        + INVESTIGATE_RULE + "\n## 3. Testing policy in force\n\n| Setting | Value | Source |\n|---|---|---|\n"
        "| testing.method | tdd | (default) |\n| testing.coverage_metric | line | (default) |\n" + threshold + "\n"
        "| testing.coverage_scope | every `holds: code` root in source-tree.md | (default) |\n"
        "| testing.coverage_exclusions | the `generated`, `tests` and `fixtures` roots | (default) |\n"
        "| testing.exception_approvers | the story's owner | (default) |\n\n## 4. Test levels\n\n"
        "| Kind | Levels | Tests root | Basis |\n|---|---|---|---|\n" + levels + "\n## 5. Naming\n\n" + NAMING_RULE
        + proposed("`test_STORY_NNN_AC_NN_<what>` for every test that verifies an acceptance criterion.",
                   "the naming pattern")
        + "\n## 6. Fixtures and test data\n\n" + proposed("each test creates its own data.", "how fixtures are made")
        + "\n## 7. Running the tests\n\n| Component | Command | Basis |\n|---|---|---|\n" + commands + "\n"
        + change_log(res))

    def layer(name, title, kind, sections):
        body = f"\n# {M.IDS[name]} — {title}\n\n## 1. Components covered\n\n" + covered(cmps, kind)
        for i, (heading, text) in enumerate(sections, start=2):
            body += f"\n## {i}. {heading}\n\n" + text
        return body + "\n" + change_log(res)

    docs["front-end"] = frontmatter("front-end", [ARCH_LINK]) + layer("front-end", "Front end", "user-interface", [
        ("Framework and structure", proposed("one Typer command per module.", "how commands are organized")),
        ("State", proposed("the CLI keeps no state between runs.", "where state lives")),
        ("Interaction and output", proposed("commands are verbs, and exit codes are 0, 1 and 2.", "the output rules")),
        ("Accessibility", proposed("no meaning is carried by colour alone.", "the accessibility rules")),
        ("Design system", proposed("terminal output follows one style guide.", "the design system"))])
    if "middle-tier" in names:
        docs["middle-tier"] = frontmatter("middle-tier", [ARCH_LINK]) + layer("middle-tier", "Middle tier", "service", [
            ("Domain structure", proposed("one class holds the shift rules.", "the domain structure")),
            ("Boundaries within a component", proposed("the CLI calls only the service.", "the boundaries")),
            ("Orchestration", proposed("each command is one call to the service.", "how work is coordinated")),
            ("Validation", proposed("the service validates input before storing it.", "where input is validated")),
            ("Transactions", proposed("one transaction per service call.", "the transaction boundaries"))])
    docs["rdbms"] = frontmatter("rdbms", [ARCH_LINK, "{id: ADR-002, relation: constrains, version: 1, hash: null}"]) + layer(
        "rdbms", "Relational database", "relational-store", [
            ("Engine and version", "- **Decision** (ADR-002): SQLite 3, in a local file (tech-stack.md, TEC-02).\n"),
            ("Naming", proposed("tables are plural `snake_case` nouns.", "the naming rules")),
            ("Migrations", proposed("every schema change is an Alembic revision.", "the migration rules")),
            ("Indexing", proposed("an index is added with the query that needs it.", "the indexing rules")),
            ("Transactions", proposed("no transaction stays open across user input.", "the transaction rules"))])
    docs["ui-mockups"] = frontmatter("ui-mockups", [ARCH_LINK]) + layer("ui-mockups", "UI mockups", "user-interface", [
        ("Design system", proposed("a terminal style guide in `docs/`.", "where the design system lives")),
        ("Approved designs", "GENERATED by the context step from the approved-design records in stories (section 3 of "
                             "each story).\nChange a story's record, not this table.\n\n| Story | Screen or flow | "
                             "Exports | Approved on | Handoff bundle |\n|---|---|---|---|---|\n")])
    if reminder:
        docs["back-end"] = frontmatter("back-end", [ARCH_LINK]) + layer("back-end", "Back end", "platform", [
            ("Runtime and hosting", proposed("the worker runs on the user's machine.", "how the worker is started")),
            ("Deployment", proposed("the worker ships in the shiftlog package.", "how the worker is deployed")),
            ("Jobs and queues", "- [NEEDS ADR: the message broker between the Shift service and the Reminder worker; "
                                "affects back-end.md]\n"),
            ("Integrations", proposed("none.", "the integrations")),
            ("Configuration and secrets", proposed("no secrets.", "how configuration is supplied"))])
    index_rows = "".join(f"| [{d}.md]({d}.md) | {M.IDS[d]} | 1 | {PURPOSE[d][0]} | {PURPOSE[d][1]} |\n"
                         for d in ORDER if d in names)
    docs["index"] = (frontmatter("index", [ARCH_LINK]) + "\n# CTX-001 — Project context index\n\n## Documents\n\n"
                     "| File | ID | Version | Kinds | Purpose |\n|---|---|---|---|---|\n" + index_rows
                     + "\n## Loading\n\n" + LOADING_RULE + "\n" + change_log(res))
    assert set(docs) == set(names), (sorted(docs), sorted(names))
    return {f"{CTX}/{n}.md": docs[n] for n in names}, names


def block(names, *, inspection="none (no paths named)", handed="none", folded="none", res=M.RESOLUTION,
          status=None, kind="new"):
    docs = ", ".join(f"{n}.md ({M.IDS[n]} v1, {(status or {}).get(n, 'draft')}; {kind})" for n in names)
    return (f"Context documents: {docs}\nInspection: {inspection}\nMarkers left: see the documents\n"
            f"Handed back to architecture: {handed}\nAmbiguity entries folded: {folded}\n{res}\n\n"
            "Check 1: context_check.py printed OK: 9 files checked.\n\n")


EPIC_NEXT = "Next step: run `/devforgeai:epic PRD-001` to group the ready requirements into epics."
ARCH_NEXT = ("Next step: run `/devforgeai:architecture PRD-001` to decide the message broker; then run "
             "`/devforgeai:epic PRD-001`.")


def tweak(text, old, new, count=1):
    assert text.count(old) == count, f"expected {count} of {old!r}"
    return text.replace(old, new)


def example_revision(name, *, old_version, change, extra_edits=()):
    """A revision (BEH-13) of an approved example document: version up, back to draft, a new Change Log row."""
    text = M.CONTEXT[name]
    text = tweak(text, f"status: approved\nversion: {old_version}\n", f"status: draft\nversion: {old_version + 1}\n")
    text = M.re.sub(r"updated: \S+\n", f"updated: {TODAY}\n", text, count=1)
    text = M.re.sub(r'approved_by: "Example Owner"\napproved_on: \S+\n', 'approved_by: ""\napproved_on: null\n', text)
    for old, new in extra_edits:
        text = tweak(text, old, new)
    return text + f"| {old_version + 1} | {TODAY} | {ROW} | {change} {M.RESOLUTION} | — |\n"


LOCK = "- **Convention:** the lock file is committed with every dependency change.\n"
END_OF_UPGRADES = "never mixed with a story's changes.\n"
TS_REVISED = example_revision("tech-stack", old_version=2, change="Added the lock-file convention.",
                              extra_edits=[(END_OF_UPGRADES, END_OF_UPGRADES + LOCK)])
INDEX_REVISED = example_revision("index", old_version=2, change="tech-stack.md is version 3.", extra_edits=[
    ("| CTX-003 | 2 | all |", "| CTX-003 | 3 | all |")])


def good(case):
    """Returns (files, reply) for a correct run of the case."""
    n = case.name
    if n in ("writes-the-set", "approve-on-explicit-words"):
        files, names = shared_set(approve=n == "approve-on-explicit-words")
        status = {"tech-stack": "approved"} if n == "approve-on-explicit-words" else None
        return files, block(names, status=status) + EPIC_NEXT
    if n in ("nothing-confirmed", "no-scope-no-inspection"):
        files, names = shared_set(confirmed=False)
        return files, block(names) + EPIC_NEXT
    if n == "observed-and-confirmed":
        files, names = shared_set(confirmed=False, observed=True)
        return files, block(names, inspection="pyproject.toml, src/shiftlog/, tests/") + EPIC_NEXT
    if n == "needs-adr-handback":
        files, names = shared_set(reminder=True)
        return files, block(names, handed="the message broker between the Shift service and the Reminder worker "
                                          "(back-end.md)") + ARCH_NEXT
    if n == "kinds-missing":
        files, names = shared_set(kinds_missing=True)
        return files, block(names) + "The kinds of ARCH-001#CMP-02 are unknown.\n\n" + EPIC_NEXT
    if n == "testing-policy-cited":
        files, names = shared_set(policy=True)
        return files, block(names, res=M.RESOLUTION_POL) + EPIC_NEXT
    if n == "revision-clears-approval":
        return ({f"{CTX}/tech-stack.md": TS_REVISED, f"{CTX}/index.md": INDEX_REVISED},
                "Context documents: tech-stack.md (CTX-003 v3, draft; revised), …\n\nSTORY-001 cites tech-stack.md, "
                "so its work is a proposal until tech-stack.md is approved again.\n\n" + EPIC_NEXT)
    if n == "suspect-review":
        arch = M.CONTEXT["architecture"]
        arch = tweak(arch, "status: approved\nversion: 1\n", "status: draft\nversion: 2\n")
        arch = tweak(arch, "version: 1, hash: null}", "version: 2, hash: null}", count=3)
        arch = tweak(arch, "  - {id: ARCH-001, item: CMP-03, relation: constrains, version: 2, hash: null}\n",
                     "  - {id: ARCH-001, item: CMP-03, relation: constrains, version: 2, hash: null}\n"
                     "  - {id: ARCH-001, item: CMP-04, relation: constrains, version: 2, hash: null}\n")
        arch = tweak(arch, "| rdbms.md |\n", "| rdbms.md |\n| Export API | ARCH-001#CMP-04 | api | Exports a "
                     "week's shifts as CSV for other tools | api.md |\n")
        arch += f"| 2 | {TODAY} | {ROW} | Added CMP-04 from ARCH-001 v2. {M.RESOLUTION} | — |\n"
        rdbms = tweak(M.CONTEXT["rdbms"], "{id: ARCH-001, relation: constrains, version: 1,",
                      "{id: ARCH-001, relation: constrains, version: 2,")
        rdbms += f"| 1 | {TODAY} | {ROW} | Re-reviewed against ARCH-001 v2: no change | — |\n"
        api = (frontmatter("api", ["{id: ARCH-001, relation: constrains, version: 2, hash: null}"])
               + "\n# CTX-014 — API\n\n## 1. Components covered\n\n- ARCH-001#CMP-04 Export API\n\n## 2. Style\n\n"
               + proposed("CSV over a Python function.", "the style") + "\n" + change_log(M.RESOLUTION))
        return ({f"{CTX}/architecture.md": arch, f"{CTX}/rdbms.md": rdbms, f"{CTX}/api.md": api},
                "Context documents: api.md (CTX-014 v1, draft; new), rdbms.md (CTX-015 v1, approved; relinked)\n\n"
                + EPIC_NEXT)
    if n == "fold-accepted-entries":
        amb = M.amb_expected().replace("@@ALREADY@@", f'"{M.FOLD_ALREADY}"').replace("@@NEW@@", f'"{M.FOLD_NEW}"')
        return ({f"{CTX}/tech-stack.md": TS_REVISED, f"{CTX}/index.md": INDEX_REVISED,
                 "docs/specs/ambiguities/AMB-001.md": amb},
                "Ambiguity entries folded: AMB-001#ENT-01 → CTX-003, AMB-001#ENT-03 → CTX-003\n\n" + EPIC_NEXT)
    if n == "designs-generated":
        rows = ("| STORY-002 | `shiftlog add` prompt | docs/specs/story/design/STORY-002/add-prompt.png | 2026-09-30 | none |\n"
                "| STORY-003 | (not recorded) | docs/specs/story/design/STORY-003/edit.png | 2026-09-30 | none |\n")
        last = "| 2026-09-29 | none |\n"
        ui = example_revision("ui-mockups", old_version=1, change="Indexed the designs of STORY-002 and STORY-003.",
                              extra_edits=[(last, last + rows)])
        return ({f"{CTX}/ui-mockups.md": ui},
                "STORY-004's section 3 names docs/specs/story/design/STORY-004/edit.png in neither record form, "
                "so it has no row.\n\n" + EPIC_NEXT)
    if n == "one-document":
        return ({f"{CTX}/tech-stack.md": TS_REVISED, f"{CTX}/index.md": INDEX_REVISED},
                "Context documents: tech-stack.md (CTX-003 v3, draft; revised), index.md (CTX-001 v3, draft; "
                "revised)\n\n" + EPIC_NEXT)
    if n == "existing-set-findings":
        return ({}, "Findings:\n- front-end.md fails its check: frontmatter: status: 'in-review' is not one of "
                    "the allowed values (ERR-10); left unchanged.\n- docs/specs/context/notes.md isn't a context "
                    "document (ERR-11).\n- source-tree.md, SRC-06 (tests/service/): observed on 2026-01-01, older "
                    "than 30 days.\n\n" + EPIC_NEXT)
    if n == "no-arch-hands-back":
        return {}, ("The context documents need an architecture description. Run `/devforgeai:architecture PRD-001` "
                    "first.")
    if n == "invalid-policy-stops":
        return {}, ("Policy error in docs/specs/policy/POL-001.md, frontmatter field updated: '2026-13-45' is not a "
                    "'date' (schema). Nothing was written.")
    if n == "ignores-unrelated-request":
        return {}, "The French Revolution (1789-1799) ended the absolute monarchy in France."
    if n == "unknown-document":
        return {}, ("banana isn't a context document of this project. The set is index, architecture, tech-stack, "
                    "source-tree, testing, front-end, ui-mockups, middle-tier and rdbms. Which one should I update, "
                    "or should I run for all?")
    raise KeyError(n)


def fm_swap(path, old, new, count=1):
    return ("file", path, old, new, count)


def reply_swap(old, new):
    return ("reply", None, old, new, 1)


TS, IDX, ARCHD, RDB, TESTING = (f"{CTX}/{n}.md" for n in ("tech-stack", "index", "architecture", "rdbms", "testing"))
PYTHON_ITEM = ('    name: "Python"\n    version_range: "3.12.x"\n    used_by:\n      - "ARCH-001#CMP-01"\n'
               '      - "ARCH-001#CMP-02"\n      - "ARCH-001#CMP-03"\n    basis: decision\n    upstream:\n'
               '      - {id: ADR-001, relation: constrains, version: 1, hash: null}\n')
PIPX_LINKS = ("      - {id: ARCH-001, item: CMP-01, relation: constrains, version: 1, hash: null}\n"
              "      - {id: ARCH-001, item: CMP-02, relation: constrains, version: 1, hash: null}\n")

BAD = {
    "writes-the-set": [
        ("python range as written in ADR-001's wording", [fm_swap(TS, '"3.12.x"', '">=3.12,<3.13"')],
         {"ver03-python-decision"}),
        ("python as a convention without its link", [fm_swap(TS, PYTHON_ITEM, PYTHON_ITEM.replace(
            "basis: decision\n    upstream:\n      - {id: ADR-001, relation: constrains, version: 1, hash: null}\n",
            "basis: convention\n"))], {"ver03-python-decision"}),
        ("python's ADR link in frontmatter instead of on the item", [
            fm_swap(TS, PYTHON_ITEM, PYTHON_ITEM.replace(
                "    upstream:\n      - {id: ADR-001, relation: constrains, version: 1, hash: null}\n", "")),
            fm_swap(TS, "upstream:\n  - {id: ARCH-001", "upstream:\n  - {id: ADR-001, relation: constrains, version: 1, "
                    "hash: null}\n  - {id: ARCH-001")], {"ver03-python-decision"}),
        ("python's link written informed_by", [fm_swap(TS, "{id: ADR-001, relation: constrains",
                                                      "{id: ADR-001, relation: informed_by")],
         {"ver03-python-decision"}),
        ("sqlite range '3'", [fm_swap(TS, '"3.x"', '"3"')], {"ver03-sqlite-decision"}),
        ("typer as a decision", [fm_swap(TS, 'name: "Typer"\n    version_range: "0.12.x"\n    used_by:\n'
                                             '      - "ARCH-001#CMP-01"\n    basis: convention',
                                             'name: "Typer"\n    version_range: "0.12.x"\n    used_by:\n'
                                             '      - "ARCH-001#CMP-01"\n    basis: decision')],
         {"ver03-typer-convention"}),
        ("pytest range 8.0.x", [fm_swap(TS, '"8.x"', '"8.0.x"')], {"ver03-pytest-convention"}),
        ("pipx without its CMP-02 link", [fm_swap(TS, PIPX_LINKS, PIPX_LINKS.split("\n")[0] + "\n")],
         {"ver03-pipx-decision"}),
        ("pipx used by CMP-01 only", [fm_swap(TS, 'version_range: "unpinned"\n    used_by:\n      - "ARCH-001#CMP-01"\n'
                                                  '      - "ARCH-001#CMP-02"\n',
                                              'version_range: "unpinned"\n    used_by:\n      - "ARCH-001#CMP-01"\n')],
         {"ver03-pipx-decision"}),
        ("rdbms decision cites ADR-001", [fm_swap(RDB, "**Decision** (ADR-002)", "**Decision** (ADR-001)")],
         {"ver03-rdbms-decision-statement"}),
        ("rdbms without its ADR-002 link", [fm_swap(RDB, "  - {id: ADR-002, relation: constrains, version: 1, hash: null}\n",
                                                    "")], {"ver03-rdbms-adr-002-link"}),
        ("architecture without its CMP-02 link", [fm_swap(
            ARCHD, "  - {id: ARCH-001, item: CMP-02, relation: constrains, version: 1, hash: null}\n", "")],
         {"ver03-architecture-links-cmp-02"}),
        ("index with a fourth section", [fm_swap(IDX, "\n## Loading\n", "\n## Notes\n\nNone.\n\n## Loading\n")],
         {"ver02-index-sections"}),
        ("index lists tech-stack.md at version 2", [fm_swap(IDX, "| CTX-003 | 1 |", "| CTX-003 | 2 |")],
         {"ver02-index-row-tech-stack"}),
        ("index without the loading rule", [fm_swap(IDX, LOADING_RULE, "- Read what you need.\n")],
         {"ver02-index-loading-rule"}),
        ("the checklist before the block", [reply_swap("Context documents:", "- [x] 1. Resolve policy\n\nContext documents:")],
         {"ver18-opens-with-block"}),
        ("a path on the Inspection line", [reply_swap("Inspection: none (no paths named)", "Inspection: pyproject.toml")],
         {"ver18-inspection-none"}),
        ("a paragraph after the next step", [reply_swap(EPIC_NEXT, EPIC_NEXT + "\n\nLet me know if anything changes.")],
         {"ver18-next-step-is-last", "ver18-next-step-names-epic"}),
        ("the next step passes a path", [reply_swap("`/devforgeai:epic PRD-001`",
                                                    "`/devforgeai:epic docs/specs/prd/PRD-001.md`")],
         {"ver18-next-step-names-epic"}),
        ("the next step inside a code block", [reply_swap(EPIC_NEXT, "```\n" + EPIC_NEXT + "\n```")],
         {"ver18-next-step-outside-code", "ver18-next-step-is-last", "ver18-next-step-names-epic"}),
        ("the next step closes an open code block", [reply_swap(EPIC_NEXT, EPIC_NEXT + "\n```")],
         {"ver18-next-step-outside-code"}),
        ("the session written literally", [fm_swap(TS, f'session: "{SESSION}"', 'session: "${CLAUDE_SESSION_ID}"')],
         {"ver19-tech-stack-provenance", "ver19-tech-stack-change-log-row"}),
        ("tech-stack.md approved", [fm_swap(TS, "status: draft", "status: approved")], {"ver19-tech-stack-provenance"}),
        ("testing.md freshness 30", [fm_swap(TESTING, "freshness_days: 90", "freshness_days: 30")],
         {"ver19-testing-provenance"}),
        ("a tool other than claude-code", [fm_swap(RDB, 'tool: "claude-code"', 'tool: "codex"')],
         {"ver19-rdbms-provenance"}),
        ("reviewed_by filled", [fm_swap(RDB, "reviewed_by: []", 'reviewed_by: ["Example Owner"]')],
         {"ver19-rdbms-provenance"}),
        ("a wrong title", [fm_swap(TS, 'title: "shiftlog: tech stack"', 'title: "shiftlog: technologies"')],
         {"ver19-tech-stack-title"}),
        ("a resolution line without the testing entries", [
            fm_swap(TS, "; testing.method=tdd (default)" + M.RESOLUTION.split("; testing.method=tdd (default)")[1],
                    "")], {"ver19-tech-stack-change-log-row"}),
        ("a Change Log row from another session", [fm_swap(TS, f"| 1 | {TODAY} | {ROW} |",
                                                          f"| 1 | {TODAY} | claude-code (session "
                                                          "11111111-2222-3333-4444-555555555555) |")],
         {"ver19-tech-stack-change-log-row"}),
        ("index with freshness_days", [fm_swap(IDX, "document: index\n", "document: index\nfreshness_days: 90\n")],
         {"ver19-index-no-freshness"}),
        ("testing.md with another ID", [fm_swap(TESTING, "id: CTX-005", "id: CTX-006")], {"ver01-testing-id"}),
    ],
    "nothing-confirmed": [
        ("a convention in architecture.md's logging section", [fm_swap(
            ARCHD, "- **Proposed:** nothing is logged to standard output; debug logs go to standard error. "
                   "[NEEDS CLARIFICATION: confirm the logging rules]",
            "- **Convention:** nothing is logged to standard output.")],
         {"ver04-architecture-no-convention", "ver04-architecture-logging-proposed"}),
        ("a marker that isn't 'confirm'", [fm_swap(f"{CTX}/middle-tier.md", "[NEEDS CLARIFICATION: confirm where input "
                                                   "is validated]", "[NEEDS CLARIFICATION: where?]")],
         {"ver04-middle-tier-validation-proposed"}),
        ("a test-levels row with Convention as its basis", [fm_swap(
            TESTING, "| service | unit | tests/shift-service/ | Proposed [NEEDS CLARIFICATION: confirm the levels for "
                     "service] |\n", "| service | unit | tests/shift-service/ | Convention |\n")], set()),
        ("no proposed test-levels row at all", [fm_swap(TESTING, "Proposed [NEEDS CLARIFICATION: confirm the levels for",
                                                        "Convention (x", count=3)],
         {"ver04-testing-test-levels-proposed"}),
        ("a proposed root missing", [fm_swap(f"{CTX}/source-tree.md", '"tests/local-database/"', '"tests/db/"')],
         {"ver04-proposed-root-tests-local-database"}),
        ("a proposed root written as a convention", [fm_swap(
            f"{CTX}/source-tree.md", 'path: "src/shift-service/"\n    holds: code\n    component: "ARCH-001#CMP-02"\n'
                                     '    basis: proposed', 'path: "src/shift-service/"\n    holds: code\n'
                                     '    component: "ARCH-001#CMP-02"\n    basis: convention')],
         {"ver04-proposed-root-src-shift-service"}),
        ("a confirmed technology", [fm_swap(TS, 'name: "pipx"\n    version_range: "unpinned"\n    used_by:\n'
                                                '      - "ARCH-001#CMP-01"\n      - "ARCH-001#CMP-02"\n    basis: decision',
                                            'name: "pipx"\n    version_range: "unpinned"\n    used_by:\n'
                                            '      - "ARCH-001#CMP-01"\n      - "ARCH-001#CMP-02"\n    basis: convention')],
         {"ver04-tech-stack-no-convention-item"}),
        ("front-end.md approved", [fm_swap(f"{CTX}/front-end.md", "status: draft", "status: approved")],
         {"ver04-front-end-draft"}),
    ],
    "observed-and-confirmed": [
        ("typer as a convention", [fm_swap(TS, 'version_range: "==0.12.3"\n    used_by:\n      - "ARCH-001#CMP-01"\n'
                                               '    basis: observed', 'version_range: "==0.12.3"\n    used_by:\n'
                                               '      - "ARCH-001#CMP-01"\n    basis: convention')],
         {"ver05-typer-observed"}),
        ("pytest loses observed_in", [fm_swap(TS, 'basis: convention\n    observed_in: "pyproject.toml"\n',
                                              "basis: convention\n")],
         {"ver05-pytest-convention-keeps-observed-in"}),
        ("the cli root holds tests", [fm_swap(f"{CTX}/source-tree.md", 'path: "src/shiftlog/cli/"\n    holds: code',
                                              'path: "src/shiftlog/cli/"\n    holds: tests')],
         {"ver05-root-src-shiftlog-cli-observed"}),
        ("the service tests root without its date", [fm_swap(
            f"{CTX}/source-tree.md", f'observed_in: "tests/"\n    observed_on: {TODAY}\n', 'observed_in: "tests/"\n')],
         {"ver05-root-tests-service-observed"}),
        ("the Inspection line without tests/", [reply_swap("Inspection: pyproject.toml, src/shiftlog/, tests/",
                                                           "Inspection: pyproject.toml, src/shiftlog/")],
         {"ver05-inspection-names-paths"}),
    ],
    "no-scope-no-inspection": [
        ("a path on the Inspection line", [reply_swap("Inspection: none (no paths named)", "Inspection: pyproject.toml")],
         {"ver06-inspection-none"}),
        ("an observed basis in a table", [fm_swap(TESTING, "| ARCH-001#CMP-02 | `pytest tests/shift-service` | Proposed "
                                                  "[NEEDS CLARIFICATION: confirm the command] |",
                                                  "| ARCH-001#CMP-02 | `pytest tests/service` | Observed (tests/, "
                                                  f"{TODAY}) |")],
         {"ver06-testing-no-observed"}),
    ],
    "needs-adr-handback": [
        ("the marker in section 5", [fm_swap(f"{CTX}/back-end.md", "## 4. Jobs and queues\n\n- [NEEDS ADR",
                                             "## 4. Jobs and queues\n\n- **Proposed:** x [NEEDS CLARIFICATION: confirm "
                                             "x]\n\n## 4b. Elsewhere\n\n- [NEEDS ADR")],
         {"ver07-back-end-jobs-and-queues-marker"}),
        ("the marker doesn't name the broker", [fm_swap(f"{CTX}/back-end.md", "the message broker between",
                                                        "the transport between")],
         {"ver07-back-end-jobs-and-queues-marker"}),
        ("nothing handed back", [reply_swap("Handed back to architecture: the message broker between the Shift service "
                                            "and the Reminder worker (back-end.md)", "Handed back to architecture: none")],
         {"ver07-handed-back-lists-broker"}),
        ("the next step goes to epic", [reply_swap(ARCH_NEXT, EPIC_NEXT)], {"ver07-next-step-names-architecture"}),
    ],
    "approve-on-explicit-words": [
        ("another approver", [fm_swap(TS, 'approved_by: "Example Owner"', 'approved_by: "Bryan"')],
         {"ver08-tech-stack-approved-by"}),
        ("no approval date", [fm_swap(TS, f"approved_on: {TODAY}", "approved_on: null")],
         {"ver08-tech-stack-approved-on"}),
        ("the Approved row authored by claude-code", [fm_swap(TS, f"| 1 | {TODAY} | Example Owner | Approved |",
                                                              f"| 1 | {TODAY} | {ROW} | Approved |")],
         {"ver08-tech-stack-approved-row"}),
        ("tech-stack.md left draft", [fm_swap(TS, "status: approved", "status: draft")], {"ver08-tech-stack-approved"}),
        ("front-end.md approved too", [fm_swap(f"{CTX}/front-end.md", "status: draft", "status: approved")],
         {"ver08-front-end-draft"}),
    ],
    "revision-clears-approval": [
        ("version left at 2", [fm_swap(TS, "version: 3\n", "version: 2\n")], {"ver09-tech-stack-version-3"}),
        ("left approved", [fm_swap(TS, "status: draft", "status: approved")], {"ver09-tech-stack-draft"}),
        ("approver kept", [fm_swap(TS, 'approved_by: ""', 'approved_by: "Example Owner"')],
         {"ver09-tech-stack-approved-by-empty"}),
        ("the convention in section 1 instead", [fm_swap(TS, LOCK, ""), fm_swap(
            TS, 'notes: "The installer the components\' deployments name"',
            'notes: "The installer the components\' deployments name; the lock file is committed"')],
         {"ver09-tech-stack-lock-file-convention"}),
        ("no new Change Log row", [fm_swap(TS, f"| 3 | {TODAY} | {ROW} |", f"| 2 | {TODAY} | {ROW} |")],
         {"ver09-tech-stack-new-change-log-row"}),
        ("STORY-001 not named", [reply_swap("STORY-001 cites", "A story cites")], {"ver09-reply-story-001-proposal"}),
    ],
    "suspect-review": [
        ("rdbms.md version raised", [fm_swap(RDB, "status: approved\nversion: 1\n", "status: approved\nversion: 2\n")],
         {"ver10-rdbms-version-1-approved"}),
        ("rdbms.md returned to draft", [fm_swap(RDB, "status: approved", "status: draft")],
         {"ver10-rdbms-version-1-approved"}),
        ("rdbms.md's link not moved", [fm_swap(RDB, "{id: ARCH-001, relation: constrains, version: 2,",
                                               "{id: ARCH-001, relation: constrains, version: 1,")],
         {"ver10-rdbms-arch-link-version-2"}),
        ("no relink row", [fm_swap(RDB, "Re-reviewed against ARCH-001 v2: no change", "Reviewed")],
         {"ver10-rdbms-relink-row"}),
        ("no CMP-04 row", [fm_swap(ARCHD, "| Export API | ARCH-001#CMP-04 |", "| Export API | CMP-04 |")],
         {"ver10-architecture-row-cmp-04"}),
        ("architecture.md not raised", [fm_swap(ARCHD, "status: draft\nversion: 2\n", "status: draft\nversion: 1\n")],
         {"ver10-architecture-version-2"}),
        ("api.md approved", [fm_swap(f"{CTX}/api.md", "status: draft", "status: approved")],
         {"ver10-api-version-1-draft"}),
    ],
    "fold-accepted-entries": [
        ("ENT-03 folded at the old version", [fm_swap("docs/specs/ambiguities/AMB-001.md", f'"{M.FOLD_NEW}"',
                                                      '"folded into CTX-003 v2"')],
         {"ver11-ent-03-resolution", "ver11-amb-001-otherwise-unchanged"}),
        ("ENT-01 left empty", [fm_swap("docs/specs/ambiguities/AMB-001.md", f'"{M.FOLD_ALREADY}"', '""')],
         {"ver11-ent-01-resolution", "ver11-amb-001-otherwise-unchanged"}),
        ("ENT-02 folded too", [fm_swap("docs/specs/ambiguities/AMB-001.md",
                                       '    decided_on: null\n    resolution: ""\n',
                                       '    decided_on: null\n    resolution: "folded into CTX-004 v2"\n')],
         {"ver11-ent-02-open-and-empty", "ver11-amb-001-otherwise-unchanged"}),
        ("another field of ENT-03 changed", [fm_swap("docs/specs/ambiguities/AMB-001.md", "PR review\"\n    relates_to:\n"
                                                     "      - \"CTX-003\"\n    state: accepted\n    decided_by: \"Example "
                                                     "Owner\"\n    decided_on: 2026-09-30",
                                                     "PR review\"\n    relates_to:\n      - \"CTX-003\"\n    state: "
                                                     "accepted\n    decided_by: \"Example Owner\"\n    decided_on: "
                                                     "2026-10-01")],
         {"ver11-amb-001-otherwise-unchanged"}),
        ("single-quoted resolutions", [fm_swap("docs/specs/ambiguities/AMB-001.md", f'"{M.FOLD_NEW}"', f"'{M.FOLD_NEW}'"),
                                       fm_swap("docs/specs/ambiguities/AMB-001.md", f'"{M.FOLD_ALREADY}"',
                                               f"'{M.FOLD_ALREADY}'")], set()),
        ("no lock-file convention", [fm_swap(TS, LOCK, "")], {"ver11-tech-stack-lock-file-convention"}),
    ],
    "designs-generated": [
        ("a screen name invented for STORY-003", [fm_swap(f"{CTX}/ui-mockups.md", "| STORY-003 | (not recorded) |",
                                                          "| STORY-003 | Edit screen |")],
         {"ver16-row-story-003"}),
        ("STORY-002's date wrong", [fm_swap(f"{CTX}/ui-mockups.md", "add-prompt.png | 2026-09-30", "add-prompt.png | "
                                            "2026-10-01")], {"ver16-row-story-002"}),
        ("STORY-001's row dropped", [fm_swap(f"{CTX}/ui-mockups.md", "| STORY-001 |", "| STORY-0001 |")],
         {"ver16-row-story-001"}),
        ("a duplicate row", [fm_swap(f"{CTX}/ui-mockups.md", "| STORY-003 | (not recorded) |",
                                     "| STORY-002 | dup | x | y | none |\n| STORY-003 | (not recorded) |")],
         {"ver16-three-rows"}),
        ("a story link in frontmatter", [fm_swap(f"{CTX}/ui-mockups.md", "upstream:\n", "upstream:\n  - {id: STORY-001, "
                                                 "relation: informed_by, version: 2, hash: null}\n")],
         {"ver16-no-story-link"}),
        ("version left at 1", [fm_swap(f"{CTX}/ui-mockups.md", "version: 2\n", "version: 1\n")],
         {"ver16-ui-mockups-version-2"}),
        ("STORY-004 not reported", [reply_swap("STORY-004's section 3 names docs/specs/story/design/STORY-004/edit.png",
                                               "One story's section 3 names a design")],
         {"ver16-reports-story-004"}),
    ],
    "one-document": [
        ("index row not raised", [fm_swap(IDX, "| CTX-003 | 3 | all |", "| CTX-003 | 2 | all |")],
         {"ver17-index-row-tech-stack-version-3"}),
        ("tech-stack.md not raised", [fm_swap(TS, "version: 3\n", "version: 2\n")], {"ver17-tech-stack-version-3"}),
    ],
    "existing-set-findings": [
        ("front-end.md not reported", [reply_swap("- front-end.md fails its check: frontmatter: status: 'in-review' is "
                                                  "not one of the allowed values (ERR-10); left unchanged.\n", "")],
         {"ver24-reports-front-end-status"}),
        ("notes.md not reported", [reply_swap("- docs/specs/context/notes.md isn't a context document (ERR-11).\n", "")],
         {"ver24-reports-notes-by-path"}),
        ("the stale date not reported", [reply_swap("observed on 2026-01-01", "observed long ago")],
         {"ver24-reports-stale-observation"}),
    ],
    "testing-policy-cited": [
        ("the threshold as a default", [fm_swap(TESTING, "| testing.coverage_threshold | 90 | POL-001#SET-01 |",
                                                "| testing.coverage_threshold | none | (default) |")],
         {"ver15-testing-threshold-from-pol-001"}),
        ("another method", [fm_swap(TESTING, "| testing.method | tdd | (default) |",
                                    "| testing.method | test-after | (default) |")],
         {"ver15-testing-method-tdd-default"}),
        ("the scope from a setting", [fm_swap(TESTING, "root in source-tree.md | (default) |",
                                              "root in source-tree.md | POL-001#SET-02 |")],
         {"ver15-testing-coverage-scope-default"}),
        ("the link informed_by", [fm_swap(TESTING, "{id: POL-001, item: SET-01, relation: constrains",
                                          "{id: POL-001, item: SET-01, relation: informed_by")],
         {"ver15-testing-constrains-pol-001-set-01"}),
        ("no pass rule", [fm_swap(TESTING, PASS_RULE, "- **Convention:** tests pass.\n")], {"ver15-testing-pass-rule"}),
        ("an old resolution line", [fm_swap(ARCHD, "testing.coverage_threshold=90 (POL-001#SET-01)",
                                            "testing.coverage_threshold=none (default)")],
         {"ver15-architecture-resolution-line"}),
    ],
    "kinds-missing": [
        ("no marker in CMP-02's row", [fm_swap(ARCHD, "[NEEDS CLARIFICATION: kinds of ARCH-001#CMP-02]", "service")],
         {"ver13-architecture-cmp-02-kinds-marker"}),
    ],
    "no-arch-hands-back": [
        ("no command named", [reply_swap("Run `/devforgeai:architecture PRD-001` first.", "Define the architecture first.")],
         {"ver12-names-architecture-prd-001"}),
    ],
    "invalid-policy-stops": [
        ("the file not named", [reply_swap("docs/specs/policy/POL-001.md", "the policy")], {"ver14-names-pol-001"}),
        ("the field not named", [reply_swap("frontmatter field updated: '2026-13-45' is not a 'date'",
                                            "a frontmatter field is wrong")], {"ver14-names-field-updated"}),
    ],
    "unknown-document": [
        ("testing not listed", [reply_swap("source-tree, testing, front-end", "source-tree, front-end")],
         {"ver23-names-documents"}),
        ("no question", [reply_swap("Which one should I update, or should I run for all?", "Run again with a name.")],
         {"ver23-asks-which"}),
    ],
}


def bad(case):
    return BAD.get(case.name, [])
