# PRD hand-off contract

**Status:** proposal, written 2026-11-18 by claude-code on the model Fable 5.2 (session
fa59a935-ed2e-4502-b6c4-93bb6d847546) for Bryan's review. It changes nothing until it is built. Its brainstorm side (BEH-34, VER-39: step 8's report
block) is built in SKL-001 version 13, with the fourth commit, under SPEC-001 version 19. Its PRD side is
built separately, under SPEC-002 version 10 and SKL-002 version 7, before the PRD interview at scale (SPEC-002
versions 6 to 9) is built: Bryan's decision of 2026-11-19 (§7). Read
[README.md](README.md) first, then [mvp-and-prototype-path.md](mvp-and-prototype-path.md) for the two shapes this
document reads most.

Items for the PRD skill's spec are written `SPEC-002#BEH-27`. SPEC-002 version 9 ends at BEH-26, ERR-11 and
VER-49, so this document takes `SPEC-002#BEH-27` to `SPEC-002#BEH-29`, `SPEC-002#ERR-12` and `SPEC-002#VER-50` to
`SPEC-002#VER-54`. BEH-34 and VER-39, without a prefix, are brainstorm items (README §6).

## Workflow steps this changes

Brainstorm (`/devforgeai:brainstorm`), built in SKL-001 version 13:

| Step (SKILL.md's line, unchanged) | Today | Added by this document |
|---|---|---|
| 8. Report and hand off | Report block; `/devforgeai:prd BRN-NNN` | The block names the project kind and the first-release ideas with the cut's status |

PRD (`/devforgeai:prd`; its ten checklist lines don't change either), built later:

| Step | Today | Added by this document |
|---|---|---|
| 3. Read the BRN | Frontmatter, item blocks, section 8 | A new-shape BRN's fixed shapes are read too |
| 6. Draft from the BRN | `brn-mapping.md` | Users from C-03, assumptions in C-07's order, metrics from C-08, states from confirmed C-11 rows; C-02 and C-06 never become requirements |
| 7. Interview only the gaps | Rounds 1 to 5 | The project kind marks a suggested stage; the first release cut marks a suggested release; neither is ever written unasked |
| 10. Report and hand off | Block, markers, discussion, next step | The discussion says what the brainstorm suggested and that it was not written |

## 1. Scope

**In.** What brainstorm's final reply tells the user about a new-shape BRN (built in SKL-001 version 13, with
mvp-and-prototype-path.md's commit, so the brainstorm skill needs no further version for it). What the PRD skill
does with each fixed shape of a new-shape BRN (a later build). That an earlier-shape BRN is handled exactly as
today.

**Out.**

- Any new PRD field, collection or link relation. `src/schemas/prd.schema.json` and the PRD template don't
  change.
- Any change to who decides: `stage`, `operating_context`, `priority` and `release` stay written only when the
  user supplied or confirmed them (SPEC-002 BEH-06).
- The interview at scale (SPEC-002 versions 6 to 9: BEH-19 to BEH-26), which is approved and not built. §3.6
  says how these items read once it is.
- The Codex port of the PRD skill (Codex sessions keep it).

## 2. Changes by file

Each edit gives old and new text (R7). Old texts are quoted from the files of plugin 0.34.0: brainstorm's
SKILL.md at version 11, whose quoted passages version 12 (plugin 0.35.0) left as they were (the four brainstorm documents change none of the passages quoted here, which §5.5 records), and the PRD
skill at SKL-002 version 6, which implements SPEC-002 version 5. The PRD side is built before the
interview at scale (§7), so those are the files it meets and the edits of §2.2 to §2.5 apply as written. The
interview build comes afterwards: it takes its own old texts from the files as this build leaves them, and
carries §3.6 forward.

### 2.1 `src/claude/DevForgeAI/skills/brainstorm/SKILL.md`

Built in the fourth commit of SKL-001 version 13, after mvp-and-prototype-path.md's edits S2 to S13. Six lines
are added; SKILL.md then has 386 lines (R2's limit is 400). The eval case of VER-39 is added with that commit.
§2.2 to §2.6 are the later PRD build.

**H1.** Step 8, the block's first line.

Old:

```text
BRN-NNN written to docs/specs/brainstorm/BRN-NNN.md (framework: [name])
```

New:

```text
BRN-NNN written to docs/specs/brainstorm/BRN-NNN.md (framework: [name]; project kind: [kind])
```

**H2.** Step 8, the block's new fourth line.

Old:

```text
Promoted: IDEA-NN, … | none confirmed yet (proposals are in section 6)
```

New:

```text
Promoted: IDEA-NN, … | none confirmed yet (proposals are in section 6)
   First release: IDEA-NN, … (confirmed) | IDEA-NN, … (proposed, not confirmed) | none
```

**H3.** Step 8, after the list.

Old:

```text
For the next step, check whether `${CLAUDE_SKILL_DIR}/../prd/SKILL.md` exists:
```

New:

```text
`[kind]` is `greenfield`, `brownfield`, or `not settled` when section 1 holds the NEEDS CLARIFICATION
form. `First release:` lists the ideas whose row in the first release cut says `yes`, then the cut's
status in brackets; `none` when no row says `yes`. For an earlier-shape BRN (no `Project kind:` line),
leave out `; project kind: [kind]` and the `First release:` line.

For the next step, check whether `${CLAUDE_SKILL_DIR}/../prd/SKILL.md` exists:
```

### 2.2 `src/claude/DevForgeAI/skills/prd/SKILL.md`

Six lines are added (430 today; the limit is 500).

**P1.** *Decisions that belong to the user*.

Old:

```text
and
`release` is never inferred from the stage.
```

New:

```text
and
`release` is never inferred from the stage. A brainstorm's `Project kind:` line never sets `stage`, and
its first release cut never sets `release`: each only marks a suggestion in the interview.
```

**P2.** Step 3.

Old:

```text
Read its frontmatter `status`, `owner` and `version`, and its `problems`, `ideas` and
`assumptions` item blocks, plus the candidate success signals (section 8).
```

New:

```text
Read its frontmatter `status`, `owner` and `version`, and its `problems`, `ideas` and
`assumptions` item blocks, plus the candidate success signals (section 8). When a line of the BRN
starts with `Project kind:`, it is a new-shape BRN: read its fixed shapes too, as "A new-shape BRN" in
[brn-mapping.md](references/brn-mapping.md) says. Read any other BRN exactly as before.
```

**P3.** Step 10, item 3.

Old:

```text
3. Any other discussion, such as where a gate's answer came from,
```

New:

```text
3. Any other discussion, such as where a gate's answer came from, what a new-shape BRN's project kind
   and first release cut suggested (and that neither was written unless the user chose it),
```

**P4.** Step 8, *Extending a PRD*: the one exception to leaving existing items as they are (SPEC-002#BEH-28
item 4).

Old:

```text
Leave every existing item
  byte-identical, even one that looks invalid: write the extension, and step 9 reports the error.
```

New:

```text
Leave every existing item
  byte-identical, even one that looks invalid: write the extension, and step 9 reports the error.
  The one exception is the `state` of an existing assumption that a confirmed assumption update of a
  new-shape BRN names (brn-mapping.md, "A new-shape BRN").
```

### 2.3 `src/claude/DevForgeAI/skills/prd/references/brn-mapping.md`

**M1.** *Contents*.

Old:

```text
- Everything else
```

New:

```text
- Everything else
- A new-shape BRN
```

**M2.** A new section before the worked example.

Old:

```text
## Worked example
```

New:

```text
## A new-shape BRN

A BRN is *new-shape* when a line after its frontmatter, outside every fenced block, starts with
`Project kind:` (ignoring case and extra spaces). Everything above still applies to it, and this section
adds what its fixed shapes give. Nothing in this section applies to any other BRN: read it exactly as the
sections above say. A shape that is missing, or can't be read as described here, counts as absent: say
which one in the reply, use the sections above for that part, and never repair the BRN.

| Shape in the BRN | The PRD takes from it | Never |
|---|---|---|
| `Project kind:` line (section 1) | A suggestion in the stage question: `brownfield` marks `evolution` "(suggested)"; `greenfield` and the NEEDS CLARIFICATION form mark nothing | Never writes `stage`, never skips the stage question, never sets `operating_context` |
| `### Existing product` (section 1) | Words for section 2's prose about what exists today | Never a requirement, constraint or link |
| Target users table (section 3) | Section 3 of the PRD | — |
| `### First release cut` (section 6) | A suggestion in each requirement's question (interview.md, round 3) | Never writes `release` or `priority` |
| `### Already covered`, `### Previously decided` (section 6) | Non-goals in words, without IDs, from the rows of Previously decided | Never a requirement, metric, assumption or link |
| `### Assumption updates` (section 6) | The `state` of an assumption, from a row whose `Status` starts `confirmed on` | A row that says `proposed, not confirmed` changes nothing |
| `### Assumption risk ranking` (section 7) | The order of the carried assumptions | Rank, class and confidence are not copied: the PRD gains no field |
| Candidate success signals (section 8) | One metric for each bullet whose idea this PRD drafts | — |

**Users.** Write one paragraph in section 3 for each row of the target users table whose persona is the
`who` of a problem this PRD links: the persona, the job to be done, the current workaround and the pain.
Keep a cell that is a `[NEEDS CLARIFICATION: …]` marker as that marker. Leave out the other rows.

**Assumptions.** Carry the assumptions over as above, in this order: first those with a row in the
assumption risk ranking, by rank; then the others, by BRN ID. `ASM-01` in the PRD is the BRN's
top-ranked assumption.

**Assumption updates.** For each row whose `Status` starts `confirmed on`, find the PRD assumptions whose
`derives` link names the row's `Earlier assumption` (`BRN-001#ASM-02` is `id: BRN-001, item: ASM-02`, at
any version). Set `state: validated` when `Change` is `open to validated` and `state: invalidated` when it
is `open to invalidated`:
- on an assumption this write carries;
- in an extension, on an existing assumption of the PRD being extended. Change its `state` and nothing
  else: not its statement, validation or links, and no other existing item. This is the one exception to
  leaving existing items byte-identical. The extension's Change Log row names it, before the sentence on
  review: `PRD-001#ASM-02 state: open to validated (BRN-002, assumption updates)`. An approved PRD returns
  to review as in any extension: `status: in-review`, `approved_by: ""`, `approved_on: null`, and the row
  says `Status approved to in-review, approval cleared.`

An assumption in a PRD this run doesn't write is left alone and named in the reply.

**Success signals.** A bullet reads `- IDEA-NN: <outcome>; baseline <value>`. For each bullet whose idea
this PRD drafts, write one metric: `metric` from the outcome, stated as something measurable; `baseline`
the bullet's value as written, with its source in parentheses, or its NEEDS CLARIFICATION marker;
a `derives` link to that idea; `target` and `measured_by` from the user, otherwise markers. Drop a bullet
whose idea this PRD doesn't draft. `- None.` gives no metric.

**The first release cut.** Read the status line and each row's idea and `yes` or `no`. The cut is
*confirmed* when the status line starts `First release cut: confirmed on`. A requirement takes the row
of the idea it derives from; a requirement that derives from two ideas takes `yes` when either row
says `yes`. interview.md, round 3, says what the question shows. With no interview, the cut writes
nothing: every `release` stays `null`, and the reply says which ideas the cut holds and its status.

For example, BRN-001 is `Project kind: brownfield`; its cut is confirmed with IDEA-01 `yes` and IDEA-03
`no`; section 8 holds `- IDEA-01: more enquiries end in a booking; baseline 43 of 74 phone enquiries
ended in a booking (data: van job log, June to October 2026)`. With "proceed without questions" the PRD
has `stage: null`, every `release: null`, and a metric whose `baseline` is that text and whose link
derives IDEA-01. With an interview, the stage question marks `evolution (suggested)`, the question for
IDEA-03's requirement marks `later (suggested)`, and nothing is written until the user picks.

## Worked example
```

### 2.4 `src/claude/DevForgeAI/skills/prd/references/interview.md`

**I1.** Round 1, the stage row.

Old:

```text
| Stage? | prototype (exploratory, may be discarded); mvp (smallest scope real users get value from, built upon); evolution (changes an established product) | The request or BRN states it |
```

New:

```text
| Stage? | prototype (exploratory, may be discarded); mvp (smallest scope real users get value from, built upon); evolution (changes an established product) | The request or BRN states it. A new-shape BRN's `Project kind:` line doesn't state it: on `brownfield`, mark evolution "(suggested)" and still ask |
```

**I2.** Round 1, the primary-users row.

Old:

```text
| Primary users? | The personas the BRN names, plus "others" | The BRN's target users section names them |
```

New:

```text
| Primary users? | The personas the BRN names, plus "others" | The BRN's target users section names them (a new-shape BRN: its table has a row for a problem this PRD links) |
```

**I3.** Round 3, after its last paragraph.

Old:

```text
A requirement that should never be built is edited
or dropped, not marked `wont`.
```

New:

```text
A requirement that should never be built is edited
or dropped, not marked `wont`.

**A new-shape BRN's first release cut** adds one line to the question of each requirement whose idea
has a row in the cut (brn-mapping.md, "A new-shape BRN"), after the statement:

| Cut | Row | Line added | Option marked |
|---|---|---|---|
| confirmed | `yes` | `Suggested release: current (IDEA-NN is in BRN-NNN's confirmed first release cut). The priority is yours.` | none |
| confirmed | `no` | `Suggested release: later (IDEA-NN is left out of BRN-NNN's confirmed first release cut).` | `later (suggested)` |
| proposed, not confirmed | `yes` | `Proposal only: BRN-NNN proposes IDEA-NN for the first release; nobody has confirmed that cut.` | none |
| proposed, not confirmed | `no` | `Proposal only: BRN-NNN proposes leaving IDEA-NN out of the first release; nobody has confirmed that cut.` | none |

Never mark must now or should now from the cut: it says which release, not how important. As with every
suggestion, write a value only after the user picks it.
```

**I4.** Round 5.

Old:

```text
For each drafted metric: baseline today, and target (with a time frame).
```

New:

```text
For each drafted metric: baseline today, and target (with a time frame). Don't ask for a baseline that
a new-shape BRN's success signal gave.
```

### 2.5 `src/claude/DevForgeAI/skills/prd/references/output-rules.md`

**R1.** *Change Log*.

Old:

```text
Never edit earlier rows. An extension adds a row naming the new BRN and the items added,
```

New:

```text
Never edit earlier rows. An extension adds a row naming the new BRN and the items added (and each
existing assumption whose `state` a confirmed assumption update changed, written
`PRD-NNN#ASM-NN state: open to validated (BRN-NNN, assumption updates)`),
```

**R2.** *Self-check list*, item 5.

Old:

```text
For an extension, every
   existing item is unchanged.
```

New:

```text
For an extension, every
   existing item is unchanged, except the `state` of an assumption set from a confirmed assumption
   update of a new-shape BRN, which the Change Log row names.
```

### 2.6 `src/tests/prd/make_evals.py`

The PRD skill's cases are generated: these additions go into the generator, and the case files are written by
running it. Three additions.

**G1.** Fixtures, after the line `CLINIC_PROMPT = …`. They are built from the example that
mvp-and-prototype-path.md stages, with the generator's own `replace()`, which fails when an old text is not
there:

```python
# --- SPEC-002 version 10: new-shape BRN fixtures (prd-handoff-contract.md) ---------------------------
BRN_VAN = Path("src/staging/examples/brainstorm-greenfield-mvp/BRN-001.md").read_text()


def replace_all(text, *pairs):
    for old, new in pairs:
        text = replace(text, old, new)
    return text


BROWNFIELD = (
    ("Project kind: greenfield", "Project kind: brownfield"),
    ("No such service exists yet: today there is the phone, a paper diary and a job log kept in a\nspreadsheet.",
     "A one-page booking form has run since June 2026 beside the phone, a paper diary and a job log kept in\n"
     "a spreadsheet; this brainstorm is about what the service should do next.\n\n"
     "### Existing product\n\nNo document was found in the project."),
    ("\n## 7. Assumptions and open questions",
     "\n### Already covered\n\nNone.\n\n### Previously decided\n\nNone.\n\n### Assumption updates\n\nNone.\n"
     "\n## 7. Assumptions and open questions"),
)
# The same brainstorm for a product that exists, with ASM-04 backed only by the owner's word: it now ranks first.
BRN_VAN_EVOLVING = replace_all(
    BRN_VAN, *BROWNFIELD,
    ("| IDEA-02 | yes | Tests ASM-03, ranked 3. |", "| IDEA-02 | no | Tests ASM-04, ranked 1, which IDEA-01 already tests. |"),
    ("| IDEA-01 | yes | Tests ASM-01, ranked 1. |", "| IDEA-01 | yes | Tests ASM-04, ranked 1. |"),
    ("| IDEA-03 | no | Tests ASM-02, ranked 2, which IDEA-01 already tests. |",
     "| IDEA-03 | no | Tests ASM-04, ranked 1, which IDEA-01 already tests. |"),
    ("| IDEA-05 | no | Tests no assumption ranked 1 to 3. |",
     "| IDEA-05 | no | Tests ASM-04, ranked 1, which IDEA-01 already tests. |"),
    ("| 1 | ASM-01 | Serious: stops IDEA-01, IDEA-02 (2 of 4 in the cut table). | low | Prototype: Run a four-week pilot of "
     "a one-page booking form at two stops and count bookings against phone enquiries. |\n"
     "| 2 | ASM-02 | Serious: stops IDEA-01, IDEA-03 (2 of 4 in the cut table). | low | Data: Compare the home and work "
     "postcodes in the van job log with the planned stops. |\n"
     "| 3 | ASM-03 | Serious: stops IDEA-02 (1 of 4 in the cut table). | medium | Interview: Ask ten commuters at a stop "
     "to pick their fault from the list, then check the bike. |\n"
     "| 4 | ASM-04 | Fatal: stops IDEA-01, IDEA-02, IDEA-03, IDEA-05 (4 of 4 in the cut table). | high | Data: Count the "
     "paid jobs per week in the van job log. |\n",
     "| 1 | ASM-04 | Fatal: stops IDEA-01, IDEA-02, IDEA-03, IDEA-05 (4 of 4 in the cut table). | medium | Data: Count the "
     "paid jobs per week in the van job log. |\n"
     "| 2 | ASM-01 | Serious: stops IDEA-01, IDEA-02 (2 of 4 in the cut table). | low | Prototype: Run a four-week pilot of "
     "a one-page booking form at two stops and count bookings against phone enquiries. |\n"
     "| 3 | ASM-02 | Serious: stops IDEA-01, IDEA-03 (2 of 4 in the cut table). | low | Data: Compare the home and work "
     "postcodes in the van job log with the planned stops. |\n"
     "| 4 | ASM-03 | Serious: stops IDEA-02 (1 of 4 in the cut table). | medium | Interview: Ask ten commuters at a stop "
     "to pick their fault from the list, then check the bike. |\n"),
    ("- IDEA-02: fewer jobs turned away for a missing part; baseline [NEEDS CLARIFICATION: how many jobs were turned "
     "away for a missing part]\n", ""),
)
# Two promoted ideas, so the requirements round fits one call: IDEA-01 in the first release, IDEA-03 out.
BRN_VAN_TWO = replace_all(
    BRN_VAN, *BROWNFIELD,
    ('    disposition: promoted\n    reason: "Cheap to add to a booking and the only idea that addresses missing parts."',
     '    disposition: parked\n    reason: "Wait until bookings exist."'),
    ('    disposition: promoted\n    reason: "Maya\'s own idea, in her words; two employers have already asked."',
     '    disposition: parked\n    reason: "Wait until the weekday stops are full."'),
    ("Promoted:\nIDEA-01, IDEA-02, IDEA-03 and IDEA-05. Parked: IDEA-07, until published stops prove too coarse.",
     "Promoted:\nIDEA-01 and IDEA-03. Parked: IDEA-02, IDEA-05 and IDEA-07."),
    ("| IDEA-01 | yes | Tests ASM-01, ranked 1. |\n| IDEA-02 | yes | Tests ASM-03, ranked 3. |\n"
     "| IDEA-03 | no | Tests ASM-02, ranked 2, which IDEA-01 already tests. |\n"
     "| IDEA-05 | no | Tests no assumption ranked 1 to 3. |\n",
     "| IDEA-01 | yes | Tests ASM-02, ranked 1. |\n"
     "| IDEA-03 | no | Tests ASM-02, ranked 1, which IDEA-01 already tests. |\n"),
    ("| 1 | ASM-01 | Serious: stops IDEA-01, IDEA-02 (2 of 4 in the cut table). | low |",
     "| 2 | ASM-01 | Serious: stops IDEA-01 (1 of 2 in the cut table). | low |"),
    ("| 2 | ASM-02 | Serious: stops IDEA-01, IDEA-03 (2 of 4 in the cut table). | low |",
     "| 1 | ASM-02 | Fatal: stops IDEA-01, IDEA-03 (2 of 2 in the cut table). | low |"),
    ("| 3 | ASM-03 | Serious: stops IDEA-02 (1 of 4 in the cut table). | medium |",
     "| 4 | ASM-03 | Minor: stops no idea in the cut table (0 of 2). | medium |"),
    ("| 4 | ASM-04 | Fatal: stops IDEA-01, IDEA-02, IDEA-03, IDEA-05 (4 of 4 in the cut table). | high |",
     "| 3 | ASM-04 | Fatal: stops IDEA-01, IDEA-03 (2 of 2 in the cut table). | high |"),
    ("- IDEA-02: fewer jobs turned away for a missing part; baseline [NEEDS CLARIFICATION: how many jobs were turned "
     "away for a missing part]\n", ""),
)
_ROWS = sorted(re.findall(r"^\| \d \| ASM-0\d [^\n]*\n", BRN_VAN_TWO, re.M))
BRN_VAN_TWO = replace(BRN_VAN_TWO, "".join(re.findall(r"^\| \d \| ASM-0\d [^\n]*\n", BRN_VAN_TWO, re.M)), "".join(_ROWS))
# The same, with the cut never confirmed (the dispositions and the convergence were).
BRN_VAN_TWO_PROPOSED = replace(BRN_VAN_TWO, "First release cut: confirmed on 2026-11-18",
                               "First release cut: proposed, not confirmed")
```

**G2.** In `main()`, before the cases are written, each of the four fixtures is validated with brainstorm's
validator, so a fixture that the brainstorm skill could not have written stops the generator:

```python
    for label in ("BRN_VAN", "BRN_VAN_EVOLVING", "BRN_VAN_TWO", "BRN_VAN_TWO_PROPOSED"):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "docs/specs/brainstorm/BRN-001.md"
            path.parent.mkdir(parents=True)
            path.write_text(globals()[label])
            out = subprocess.run([sys.executable, "-B", "src/claude/DevForgeAI/skills/brainstorm/scripts/validate_brn.py",
                                  str(path)], capture_output=True, text=True)
            assert out.returncode == 0, f"{label} is not a valid BRN:\n{out.stdout}"
```

The generator already imports `subprocess`, `sys` and `tempfile`.

**G3.** Four entries in `CASES`, one for each of `SPEC-002#VER-50` to `SPEC-002#VER-52` and `SPEC-002#VER-54`, with the `ver`,
`files`, `prompt`, `description` and `graders` that §5 gives; each regex grader is written with the generator's
`regex()` helper, each `llm` grader with `llm()`, the missing-PRD grader with `NO_PRD`.

`src/tests/prd/check_graders.py` gains, for each of the four cases, one good simulated result and the bad
results §5.3 lists, each failing exactly the graders named there.

### 2.7 SPEC-002's and SPEC-001's next versions

| Item | Change |
|---|---|
| SPEC-002 BEH-02 | Extended by SPEC-002#BEH-27: a new-shape BRN's fixed shapes are read |
| SPEC-002 BEH-04, §4's mapping table | Extended by SPEC-002#BEH-28: users, the order of assumptions, metrics from C-08 bullets |
| SPEC-002 BEH-05 | Extended by SPEC-002#BEH-27 and SPEC-002#BEH-29: the two suggestions; the skipped baseline and users questions |
| SPEC-002 BEH-06 | Unchanged; SPEC-002#BEH-27 and SPEC-002#BEH-29 say that the kind and the cut are suggestions, never supplied values |
| SPEC-002 BEH-09 | One exception, SPEC-002#BEH-28 item 4: an extension sets the `state` of an existing assumption from a confirmed assumption update |
| SPEC-002 BEH-13 | Extended by SPEC-002#BEH-29 item 5: the discussion names the suggestions |
| SPEC-002 BEH-14 | Unchanged: the BRN is never modified |
| SPEC-002 new | SPEC-002#BEH-27 to BEH-29, SPEC-002#ERR-12, SPEC-002#VER-50 to VER-54 |
| SPEC-001 BEH-10 | Extended by BEH-34 |
| SPEC-001 new (its next version, with the four brainstorm documents) | BEH-34, VER-39 |

BEH-34 and VER-39 enter SPEC-001 version 19 with the four brainstorm documents' items and ship in SKL-001
version 13. The PRD build is SPEC-002 version 10: it adds the SPEC-002 items of this document, moves SPEC-002's `upstream`
link to that SPEC-001 version, gives SKL-002 version 7 (`provenance.yaml` and `devforgeai-version`) and moves
the plugin version; it changes no brainstorm file. The interview at scale is then SKL-002's version after 7.

## 3. Behaviour

```yaml items
behaviors:
  - id: BEH-34
    status: proposed
    rule: |-
      1. For a new-shape BRN, step 8's block names the project kind on its first line, after the framework: greenfield, brownfield, or 'not settled' when C-01 is the NEEDS CLARIFICATION form.
      2. The block gains a line after 'Promoted:': 'First release:' followed by the IDs of the ideas whose row in C-05's table says yes, in ID order, and the cut's status in brackets, '(confirmed)' or '(proposed, not confirmed)'; or 'First release: none' when no row says yes.
      3. For an earlier-shape BRN the block is as SPEC-001 BEH-10 gives it today.
      4. Nothing else of the hand-off changes: the next step is still /devforgeai:prd with the BRN's ID.
    changes: "extends SPEC-001 BEH-10"
    lands_in: "brainstorm SKILL.md step 8 (H1 to H3), in SKL-001 version 13, with mvp-and-prototype-path.md's commit"
  - id: "SPEC-002#BEH-27"
    status: proposed
    rule: |-
      1. A BRN is new-shape when a line after its frontmatter and outside every fenced block, lowercased and with its runs of spaces collapsed, starts with 'project kind:'. The skill reads the fixed shapes of a new-shape BRN (C-01, C-02, C-03, C-05, C-06, C-07, C-08, C-11) as SPEC-002#BEH-28 and SPEC-002#BEH-29 say. An earlier-shape BRN is read, drafted, asked about and reported exactly as SPEC-002 version 9 specifies.
      2. The project kind never writes stage and never counts as the BRN stating it. With an interview, the stage question is asked whenever the request states no stage; when the kind is brownfield its evolution option is marked '(suggested)'; greenfield and the NEEDS CLARIFICATION form mark no option. The value is written only when the user picks an option or types one.
      3. Without an interview (proceed without questions, or nobody to ask), stage stays null unless the request states it.
      4. The project kind never sets or suggests operating_context.
    changes: "extends SPEC-002 BEH-02 and BEH-05"
    lands_in: "prd SKILL.md 'Decisions that belong to the user' (P1) and step 3 (P2); references/brn-mapping.md, 'A new-shape BRN' (M2); references/interview.md round 1 (I1)"
  - id: "SPEC-002#BEH-28"
    status: proposed
    rule: |-
      1. Users: section 3 of the PRD holds one paragraph for each row of C-03's table whose persona is the who of a problem the PRD links, with the row's job, workaround and pain; a NEEDS CLARIFICATION cell stays a marker; the primary-users question is skipped when there is such a row.
      2. Assumptions: the carried assumptions are numbered in this order: those with a row in C-07's ranking, by rank, then the others by BRN ID. Statement, validation, state and the derives link are carried as before. Rank, class and confidence are not copied.
      3. Metrics: each C-08 bullet whose idea the PRD drafts becomes one success metric that derives that idea: metric from the bullet's outcome, baseline the bullet's value as written with its source, or its marker; target and measured_by from the user, otherwise markers. A bullet whose idea the PRD does not draft is dropped. The baseline of such a metric is not asked for when the bullet gave a value.
      4. Assumption updates: for each C-11 row whose Status starts 'confirmed on', every assumption of the PRD being written whose derives link names the row's earlier assumption gets state validated or invalidated as the row's Change says: an assumption this write carries, and, in an extension, an existing one, of which only the state changes (not its statement, validation or links, and no other existing item); the extension's Change Log row names each as 'PRD-NNN#ASM-NN state: open to validated (BRN-NNN, assumption updates)'; an approved PRD returns to review as SPEC-002 BEH-09 says for any extension (status in-review, approved_by and approved_on cleared, the row saying 'Status approved to in-review, approval cleared.'). A row that says 'proposed, not confirmed' changes nothing. An assumption of a PRD the run does not write is named in the reply and left alone.
      5. C-02's rows and C-06's rows never become a requirement, a constraint, a metric, an assumption or a link. C-02 may inform section 2's prose. C-06's Previously decided rows may be listed as non-goals in words, without IDs.
    changes: "extends SPEC-002 BEH-04; one exception to BEH-09 (item 4)"
    lands_in: "references/brn-mapping.md, 'A new-shape BRN' (M1, M2); references/interview.md rounds 1 and 5 (I2, I4); prd SKILL.md step 8 (P4); references/output-rules.md, Change Log and self-check item 5 (R1, R2)"
  - id: "SPEC-002#BEH-29"
    status: proposed
    rule: |-
      1. The first release cut never writes release or priority and never counts as the BRN stating either.
      2. A requirement takes the cut row of the idea it derives from; one that derives from two ideas takes yes when either row says yes.
      3. With an interview and a confirmed cut (the status line starts 'First release cut: confirmed on'): the question of a requirement whose row says yes carries the line 'Suggested release: current (IDEA-NN is in BRN-NNN's confirmed first release cut). The priority is yours.' and marks no option; the question of one whose row says no carries 'Suggested release: later (IDEA-NN is left out of BRN-NNN's confirmed first release cut).' and marks the option 'later (suggested)'.
      4. With an interview and a cut that says 'proposed, not confirmed': the question carries 'Proposal only: BRN-NNN proposes IDEA-NN for the first release; nobody has confirmed that cut.' or 'Proposal only: BRN-NNN proposes leaving IDEA-NN out of the first release; nobody has confirmed that cut.', and marks no option.
      5. must now and should now are never marked from the cut. Whatever was suggested, a value is written only when the user picks or types it; a dismissed or unanswered question writes nothing.
      6. Without an interview every release stays null; the reply's discussion names the cut's yes ideas and its status, and says that no release was written from it. With an interview, the discussion says which suggestions were shown.
    changes: "extends SPEC-002 BEH-05 and BEH-13"
    lands_in: "references/interview.md round 3 (I3); references/brn-mapping.md, 'A new-shape BRN' (M2); prd SKILL.md step 10 (P3)"
```

### 3.1 The new block (BEH-34)

```text
BRN-NNN written to docs/specs/brainstorm/BRN-NNN.md (framework: [name]; project kind: [kind])
Problems: N · Ideas: N · Assumptions: N
Promoted: IDEA-NN, … | none confirmed yet (proposals are in section 6)
First release: IDEA-NN, … (confirmed) | IDEA-NN, … (proposed, not confirmed) | none
Open questions: [each NEEDS CLARIFICATION marker and open assumption, briefly]
```

For the staged example `brainstorm-greenfield-mvp`:

```text
BRN-001 written to docs/specs/brainstorm/BRN-001.md (framework: diverge-converge; project kind: greenfield)
Problems: 3 · Ideas: 7 · Assumptions: 4
Promoted: IDEA-01, IDEA-02, IDEA-03, IDEA-05
First release: IDEA-01, IDEA-02 (confirmed)
Open questions: missed-part count; which weekday stops stay; ASM-01 to ASM-04 are open
```

`hands-off-to-prd`'s graders read only the BRN path, the command and the absence of a path argument, so the new
lines leave them passing.

### 3.2 Why the kind and the cut are suggestions

The PRD skill's SKILL.md counts a value "in the BRN" as supplied, and round 1 skips the stage question when "the
BRN states it". Neither shape is such a statement:

- `Project kind: brownfield` says the product exists. `stage: evolution` says this PRD changes an established
  product. A product can exist and the PRD can still be a prototype of something new beside it. The kind
  makes evolution likely, so it is marked, and the user decides.
- A confirmed cut is the user's decision about ideas. `release` is a field of each requirement, and one idea
  becomes one or more requirements (brn-mapping.md), which the user has not seen when confirming the cut.
  Round 3's options also pair a release with a priority, and the cut says nothing about priority. So a `yes`
  row marks no option (two options mean "current"), and a `no` row marks `later`, which sets no priority.

### 3.3 Each shape, with a new-shape BRN

| Shape | No interview ("proceed without questions") | With an interview |
|---|---|---|
| C-01 `brownfield` | `stage: null` unless the request states a stage | Stage question asked; `evolution (suggested)`; written only on a pick |
| C-01 `greenfield` or NEEDS CLARIFICATION | the same | Stage question asked, no option marked |
| C-02 | Words in section 2; no item, no link | the same |
| C-03 | Section 3 from the linked problems' rows | the same; the primary-users question is skipped |
| C-05 confirmed | Every `release: null`; the reply names the cut | A line on each question; `later (suggested)` on `no` rows |
| C-05 proposed | the same | A "Proposal only" line; no option marked |
| C-06 | No item, no link; Previously decided rows may be non-goals in words | the same |
| C-07 | Carried assumptions in rank order | the same |
| C-08 | A metric for each bullet of a drafted idea, baseline kept | the same; no baseline question for a given value; the target is asked |
| C-11 confirmed row | The matching assumption's `state` set | the same |
| C-11 proposed row | Nothing | Nothing |

### 3.4 An earlier-shape BRN

Nothing in this document applies to a BRN without the `Project kind:` line. The edits are written so: P2 and
M2 open with the gate, and I1 to I4 name "a new-shape BRN" in each added clause. The PRD suite's existing cases
all use earlier-shape fixtures; they are the regression check, and the build runs them unchanged (§5).

### 3.5 A shape that can't be read

`SPEC-002#ERR-12` (§4). The PRD skill doesn't run brainstorm's validator and never repairs a BRN (SPEC-002
BEH-14, ERR-05). A broken item block still stops the run (ERR-05); a broken fixed shape does not, because the
PRD can be drafted without it.

### 3.6 With the interview at scale (SPEC-002 versions 6 to 9)

That build comes after this one (§7). SPEC-002 version 10 keeps BEH-19 to BEH-26 as they are, approved and not
built; when they are built, they read these rules as follows, and the build keeps the passages §2.2 to §2.5 add:

- BEH-19 (reuse before asking): the project kind is not a source for `stage`, and the cut is not a source for
  `release` or `priority`; neither appears in the reuse line. A C-08 baseline is a source for a metric's
  baseline and appears there as `BRN-NNN vN §8`.
- BEH-20 (the count): the stage question and each requirement's question are counted as open whatever the
  kind and the cut suggest.
- BEH-22 (triage, then the table): the table suggests `later` for every unticked requirement. A requirement
  whose row in a confirmed cut says `yes` is listed there with SPEC-002#BEH-29's line and no suggested value,
  so accepting every row writes nothing for it; a `no` row keeps the table's `later (suggested)`.
- BEH-23 and BEH-24 (a pasted list, the review file): unchanged. The review file never holds a suggestion, so
  the cut does not appear in it.

## 4. Errors and edge cases

```yaml items
errors:
  - id: "SPEC-002#ERR-12"
    status: proposed
    condition: "A new-shape BRN lacks one of its fixed shapes, or one can't be read as README §4 gives it (a table with the wrong columns, a status line in neither form, a C-08 bullet without an idea ID)"
    handling: "Treat that shape as absent and use SPEC-002 version 9's behaviour for that part: no suggestion from it, section 3 from the prose, assumptions in BRN ID order, a success signal mapped as a prose bullet. Name the shape and the BRN path in the reply. Never repair the BRN, and never stop for it"
    user_result: "The PRD drafted without that shape, and the shape named"
    changes: new
    lands_in: "references/brn-mapping.md, 'A new-shape BRN', first paragraph (M2)"
```

| Case | Result | Item |
|---|---|---|
| The request states the stage ("this is our MVP") and the kind is brownfield | `stage: mvp`; the question is not asked; no suggestion | SPEC-002#BEH-27 item 2 |
| The cut is confirmed but the BRN is not converged | SPEC-002 ERR-02's gate first; the cut's suggestions as usual after a yes | SPEC-002#BEH-29 |
| A `yes` row's idea is already cited by a PRD | The idea is left out as today; its row suggests nothing | SPEC-002 BEH-04 |
| A cut row's idea is `open` (a proposed cut over unconfirmed dispositions) | The PRD drafts only promoted ideas, so the row is not used | SPEC-002 BEH-02 |
| The user picks must now on a `no` row's question | Written as picked: the user's later word wins over the suggestion | SPEC-002#BEH-29 item 5 |
| C-08 holds `- None.` | No metric from the BRN | SPEC-002#BEH-28 item 3 |
| A C-11 row names an assumption no PRD assumption links | Nothing changes | SPEC-002#BEH-28 item 4 |
| An extension of an approved PRD sets an assumption's `state` | As any extension: `in-review`, approval cleared (SPEC-002 BEH-09) | SPEC-002#BEH-28 item 4 |

## 5. Verification

### 5.1 Items

`{ITEM}` in a pattern below is the generator's `ITEM` (the rest of one item's lines, never the next item); the
patterns are shown with it expanded. `PRD` is `docs/specs/prd/PRD-001.md`.

```yaml items
verifications:
  - id: VER-39
    status: proposed
    covers:
      - BEH-34
    level: eval
    obligation: "With nobody to confirm, the final reply's block names the project kind after the framework and holds a 'First release:' line that lists idea IDs as '(proposed, not confirmed)' or says 'none', never '(confirmed)'; the next step is still /devforgeai:prd BRN-001."
    case: reports-kind-and-first-release
    prompt: |-
      Two of us want to start a weekend repair cafe in our town's library, where people bring broken
      household things and volunteers fix them. Nothing exists yet, not even a sign-up sheet. Brainstorm
      how we could get it going. Don't ask me any questions, just work through it and write it up.
    scaffold: none
    graders:
      - name: block-names-the-kind
        type: regex
        target: last_message
        match: contains
        pattern: |-
          \(framework: [^)\n]*; project kind: greenfield\)
      - name: block-has-first-release-line
        type: regex
        target: last_message
        match: contains
        flags: m
        pattern: |-
          ^[ \t]*First release: (?:IDEA-\d{2}(?:, IDEA-\d{2})* \(proposed, not confirmed\)|none)[ \t]*$
      - name: first-release-not-confirmed
        type: regex
        target: last_message
        match: not_contains
        flags: m
        pattern: |-
          ^[ \t]*First release: [^\n]*\(confirmed\)
      - name: names-prd-command
        type: regex
        target: last_message
        match: contains
        pattern: |-
          /devforgeai:prd`? `?BRN-001\b
  - id: "SPEC-002#VER-50"
    status: proposed
    covers:
      - "SPEC-002#BEH-27"
      - "SPEC-002#BEH-28"
      - "SPEC-002#BEH-29"
    level: eval
    obligation: "From a brownfield new-shape BRN with a confirmed cut and no interview, the PRD has stage null, no release and no priority written, the carried assumptions in the ranking's order, section 3 naming both personas of the linked problems, and one metric from the one success signal with its baseline kept and a derives link to its idea."
    case: new-shape-brn-drafted
    prompt: |-
      Write the PRD for BRN-001. Proceed without questions.
    scaffold: "docs/specs/brainstorm/BRN-001.md is BRN_VAN_EVOLVING (G1)"
    graders:
      - name: prd-exists
        type: file_exists
        path: docs/specs/prd/PRD-001.md
        exists: true
      - name: stage-not-written
        type: regex
        target: "{source: file, path: docs/specs/prd/PRD-001.md}"
        match: contains
        flags: m
        pattern: |-
          ^stage: null[ \t]*$
      - name: no-release-written
        type: regex
        target: "{source: file, path: docs/specs/prd/PRD-001.md}"
        match: not_contains
        flags: m
        pattern: |-
          ^[ \t]+release:[ \t]*"?(?:current|later)\b
      - name: no-priority-written
        type: regex
        target: "{source: file, path: docs/specs/prd/PRD-001.md}"
        match: not_contains
        flags: m
        pattern: |-
          ^[ \t]+priority:[ \t]*"?(?:must|should|could|wont)\b
      - name: riskiest-assumption-first
        type: regex
        target: "{source: file, path: docs/specs/prd/PRD-001.md}"
        match: contains
        pattern: |-
          - id: ASM-01\n(?=(?:(?![ \t]*- id:)[ \t]+[^\n]*\n)*?[ \t]+statement: "[^"\n]*\bpay\b)(?=(?:(?![ \t]*- id:)[ \t]+[^\n]*\n)*?[ \t]+- \{id: BRN-001, item: ASM-04, relation: derives)
      - name: metric-keeps-the-baseline
        type: regex
        target: "{source: file, path: docs/specs/prd/PRD-001.md}"
        match: contains
        pattern: |-
          - id: SM-\d{2}\n(?=(?:(?![ \t]*- id:)[ \t]+[^\n]*\n)*?[ \t]+baseline: "[^"\n]*43 of 74[^"\n]*van job log)(?=(?:(?![ \t]*- id:)[ \t]+[^\n]*\n)*?[ \t]+- \{id: BRN-001, item: IDEA-01, relation: derives)
      - name: users-from-the-table
        type: regex
        target: "{source: file, path: docs/specs/prd/PRD-001.md}"
        match: contains
        pattern: |-
          ## 3\. Users and personas\n(?=(?:(?!\n## )[\s\S])*?Bike commuter)(?=(?:(?!\n## )[\s\S])*?Van mechanic)
      - name: reply-says-nothing-was-written-from-the-cut
        type: llm
        question: |-
          Context: the brainstorm BRN-001 is marked "Project kind: brownfield" and holds a confirmed first
          release cut with IDEA-01 in and IDEA-02, IDEA-03 and IDEA-05 out. The user asked for the PRD and
          said to proceed without questions.
          PASS if the reply mentions the brainstorm's first release cut (or first release ideas) and makes
          clear that no release, priority or stage was decided from it or from the project kind.
          FAIL if the reply says or implies that a release, a priority or a stage was set from the
          brainstorm, or does not mention the cut at all.
  - id: "SPEC-002#VER-51"
    status: proposed
    covers:
      - "SPEC-002#BEH-27"
      - "SPEC-002#BEH-29"
    level: eval
    obligation: "Asked without a waiver, with a brownfield new-shape BRN whose cut is confirmed, the skill writes no PRD and asks: the stage question marks evolution as suggested; the question for IDEA-01's requirement carries the 'Suggested release: current' line and marks no option; must now and should now are never marked suggested; a question for IDEA-03's requirement, when the reply holds one, carries the 'Suggested release: later' line and marks later as suggested."
    case: cut-suggests-release
    prompt: |-
      Write the PRD for BRN-001. It serves real customers in production from day one, and the release
      is called "Booking v2". There are no non-goals beyond what the brainstorm parked or rejected, no
      ADRs or mandated platforms apply, and I have no design preferences.
    scaffold: "docs/specs/brainstorm/BRN-001.md is BRN_VAN_TWO (G1)"
    graders:
      - name: no-prd-written
        type: file_exists
        path: docs/specs/prd/PRD-001.md
        exists: false
      - name: evolution-is-suggested
        type: regex
        target: last_message
        match: contains
        pattern: |-
          [Ee]volution[^\n;|]*\(suggested\)
      - name: yes-row-suggests-current
        type: regex
        target: last_message
        match: contains
        pattern: |-
          Suggested release: current \(IDEA-01 is in BRN-001's confirmed first release cut\)\. The priority is yours\.
      - name: no-priority-suggested
        type: regex
        target: last_message
        match: not_contains
        pattern: |-
          (?:[Mm]ust|[Ss]hould) now[^\n;|]*\(suggested\)
      - name: suggestions-follow-the-cut
        type: llm
        question: |-
          Context: BRN-001 is marked "Project kind: brownfield". Its confirmed first release cut has
          IDEA-01 in and IDEA-03 out. The user asked for the PRD without waiving questions, and stated the
          operating context and the release name but not the stage.
          PASS if all of these hold: (1) the reply asks which stage applies and does not state a stage as
          decided; (2) every requirement question about IDEA-03's requirement, if the reply has one,
          carries "Suggested release: later (IDEA-03 is left out of BRN-001's confirmed first release
          cut)." and marks the later option as suggested; (3) no question asks about the operating
          context or the release name.
          FAIL otherwise, quoting the question that breaks a point.
  - id: "SPEC-002#VER-52"
    status: proposed
    covers:
      - "SPEC-002#BEH-29"
    level: eval
    obligation: "With the same BRN and request but the cut left 'proposed, not confirmed', the reply shows the cut as a proposal only: the 'Proposal only' line for IDEA-01, no 'Suggested release' line and no option marked suggested from the cut; no PRD is written."
    case: unconfirmed-cut-is-a-proposal
    prompt: |-
      Write the PRD for BRN-001. It serves real customers in production from day one, and the release
      is called "Booking v2". There are no non-goals beyond what the brainstorm parked or rejected, no
      ADRs or mandated platforms apply, and I have no design preferences.
    scaffold: "docs/specs/brainstorm/BRN-001.md is BRN_VAN_TWO_PROPOSED (G1)"
    graders:
      - name: no-prd-written
        type: file_exists
        path: docs/specs/prd/PRD-001.md
        exists: false
      - name: shown-as-a-proposal
        type: regex
        target: last_message
        match: contains
        pattern: |-
          Proposal only: BRN-001 proposes IDEA-01 for the first release; nobody has confirmed that cut\.
      - name: no-suggested-release
        type: regex
        target: last_message
        match: not_contains
        pattern: |-
          Suggested release:
      - name: later-not-suggested
        type: regex
        target: last_message
        match: not_contains
        pattern: |-
          [Ll]ater[^\n;|]*\(suggested\)
  - id: "SPEC-002#VER-54"
    status: proposed
    covers:
      - "SPEC-002#BEH-28"
    level: eval
    obligation: "Extending the approved PRD-001 from the brownfield BRN-002, whose Assumption updates holds the confirmed row 'BRN-001#ASM-01, open to validated': PRD-001's assumption that derives BRN-001#ASM-01 has state validated, the Change Log row names that change, the version is 2, the status is in-review and the approval is cleared."
    case: assumption-update-reaches-the-prd
    prompt: |-
      Extend PRD-001 from BRN-002. Proceed without questions.
    scaffold: "docs/specs/brainstorm/BRN-001.md, docs/specs/brainstorm/BRN-002.md and docs/specs/prd/PRD-001.md are the three files of src/staging/examples/brainstorm-brownfield/, read by the generator, which first asserts that BRN-002 holds the row '| BRN-001#ASM-01 | open to validated |' with a 'confirmed on' status and that PRD-001 holds 'state: open' above the link '{id: BRN-001, item: ASM-01, relation: derives'"
    graders:
      - name: state-set-from-the-update
        type: regex
        target: "{source: file, path: docs/specs/prd/PRD-001.md}"
        match: contains
        pattern: |-
          - id: ASM-\d{2}\n(?=(?:(?![ \t]*- id:)[ \t]+[^\n]*\n)*?[ \t]+state: validated\b)(?=(?:(?![ \t]*- id:)[ \t]+[^\n]*\n)*?[ \t]+- \{id: BRN-001, item: ASM-01, relation: derives)
      - name: change-log-names-the-change
        type: regex
        target: "{source: file, path: docs/specs/prd/PRD-001.md}"
        match: contains
        pattern: |-
          PRD-001#ASM-\d{2} state: open to validated \(BRN-002, assumption updates\)
      - name: version-raised
        type: regex
        target: "{source: file, path: docs/specs/prd/PRD-001.md}"
        match: contains
        flags: m
        pattern: |-
          ^version: 2[ \t]*$
      - name: back-in-review
        type: regex
        target: "{source: file, path: docs/specs/prd/PRD-001.md}"
        match: contains
        flags: m
        pattern: |-
          ^status: in-review[ \t]*$
      - name: approval-cleared
        type: regex
        target: "{source: file, path: docs/specs/prd/PRD-001.md}"
        match: contains
        flags: m
        pattern: |-
          ^approved_by: ""[ \t]*\n^approved_on: null[ \t]*$
  - id: "SPEC-002#VER-53"
    status: proposed
    covers:
      - "SPEC-002#BEH-27"
      - "SPEC-002#BEH-28"
      - "SPEC-002#BEH-29"
      - "SPEC-002#ERR-12"
    level: manual
    obligation: |-
      Live, with AskUserQuestion, on a copy of the plugin loaded with claude --plugin-dir, each result recorded in SPEC-002 §9:
      (a) a brownfield new-shape BRN: the stage question shows the evolution option marked '(suggested)'; picking it writes stage evolution; in a second run dismissing the question leaves stage null;
      (b) a confirmed cut: each requirement's question shows SPEC-002#BEH-29's line for its row; a no row's question marks 'later (suggested)' and no other option is marked; picking it writes release later and priority null; picking must now on a no row writes must and current;
      (c) the staged example brainstorm-greenfield-mvp with 'Proceed without questions': stage null, every release null, two metrics with the baselines of section 8, assumptions in the ranking's order, and a reply that names the cut and says nothing was written from it;
      (d) the staged example brainstorm-brownfield: no requirement, metric, assumption or link comes from a row of Existing product, Already covered or Previously decided;
      (e) SPEC-002#VER-54's fixture with BRN-002's row edited to 'proposed, not confirmed': the extension changes no existing assumption, and the reply says the update is not confirmed;
      (f) a new-shape BRN whose cut table has a column removed: the PRD is drafted with no suggestion from the cut and the reply names the shape (SPEC-002#ERR-12);
      (g) src/staging/examples/prd-production-mvp/BRN-001.md, an earlier-shape BRN: no suggestion line, no new discussion sentence, the stage question as before.
```

### 5.2 The existing suites

Every existing prd case uses an earlier-shape BRN, so each must score as before: the build runs
`claude plugin eval … --tag prd` unchanged and compares with SPEC-002 §9's last record. Brainstorm's
`hands-off-to-prd` and `writes-valid-brn` read the final reply; they are run again with VER-39.

### 5.3 `check_graders.py`: simulated results

For each new case, the good result passes every regex and file grader; each bad result fails exactly the
graders named.

| Case | Bad result | Fails |
|---|---|---|
| `new-shape-brn-drafted` | `stage: evolution` in the frontmatter | `stage-not-written` |
| | `release: current` on FR-001 | `no-release-written` |
| | `priority: must` on FR-001 | `no-priority-written` |
| | The assumptions in BRN ID order (ASM-01 is "book a repair online") | `riskiest-assumption-first` |
| | The metric's baseline a NEEDS CLARIFICATION marker | `metric-keeps-the-baseline` |
| | Section 3 without "Van mechanic" | `users-from-the-table` |
| `cut-suggests-release` | A reply that states `stage: evolution` and asks nothing | `evolution-is-suggested`, `yes-row-suggests-current` |
| | "must now (suggested)" on FR-001's question | `no-priority-suggested` |
| | A PRD written | `no-prd-written` |
| `assumption-update-reaches-the-prd` | PRD-001's assumption left `state: open` | `state-set-from-the-update` |
| | A Change Log row that doesn't name the change | `change-log-names-the-change` |
| | `status: approved` kept | `back-in-review` |
| | `approved_by: "Dana"` kept | `approval-cleared` |
| `unconfirmed-cut-is-a-proposal` | The confirmed-cut lines used | `shown-as-a-proposal`, `no-suggested-release` |
| | "later (suggested)" on IDEA-03's question | `later-not-suggested` |

### 5.4 Regex graders, tested

Each pattern was read back from this file with PyYAML and run in node (v24) against a good and a wrong sample
(`check_graders_b.mjs`):

```text
reports-kind-and-first-release/block-names-the-kind (contains): good sample passes, wrong sample fails
reports-kind-and-first-release/block-has-first-release-line (contains): good sample passes, wrong sample fails
reports-kind-and-first-release/first-release-not-confirmed (not_contains): good sample passes, wrong sample fails
reports-kind-and-first-release/names-prd-command (contains): good sample passes, wrong sample fails
new-shape-brn-drafted/stage-not-written (contains): good sample passes, wrong sample fails
new-shape-brn-drafted/no-release-written (not_contains): good sample passes, wrong sample fails
new-shape-brn-drafted/no-priority-written (not_contains): good sample passes, wrong sample fails
new-shape-brn-drafted/riskiest-assumption-first (contains): good sample passes, wrong sample fails
new-shape-brn-drafted/metric-keeps-the-baseline (contains): good sample passes, wrong sample fails
new-shape-brn-drafted/users-from-the-table (contains): good sample passes, wrong sample fails
cut-suggests-release/evolution-is-suggested (contains): good sample passes, wrong sample fails
cut-suggests-release/yes-row-suggests-current (contains): good sample passes, wrong sample fails
cut-suggests-release/no-priority-suggested (not_contains): good sample passes, wrong sample fails
unconfirmed-cut-is-a-proposal/shown-as-a-proposal (contains): good sample passes, wrong sample fails
unconfirmed-cut-is-a-proposal/no-suggested-release (not_contains): good sample passes, wrong sample fails
unconfirmed-cut-is-a-proposal/later-not-suggested (not_contains): good sample passes, wrong sample fails
assumption-update-reaches-the-prd/state-set-from-the-update (contains): good sample passes, wrong sample fails
assumption-update-reaches-the-prd/change-log-names-the-change (contains): good sample passes, wrong sample fails
assumption-update-reaches-the-prd/version-raised (contains): good sample passes, wrong sample fails
assumption-update-reaches-the-prd/back-in-review (contains): good sample passes, wrong sample fails
assumption-update-reaches-the-prd/approval-cleared (contains): good sample passes, wrong sample fails
21 regex graders behave as intended
```

### 5.5 What was run for this document

| Check | Result |
|---|---|
| Every old text of §2.1 to §2.5 against the files of plugin 0.34.0 (`check_edits.py`) | each found exactly once, ignoring line breaks |
| H1 to H3 against brainstorm's SKILL.md with the four brainstorm documents' edits applied in build order (`skill_lines.py`) | each applies; SKILL.md then has 377 lines (371 after the four documents; the limit is 400). Re-checked on 2026-11-20 against `main` at `ff78d44` (SKL-001 version 12): each applies; 386 lines (380 after the four documents) |
| G1's fixtures, built with a `replace()` that requires exactly one match, under the validator with mvp-and-prototype-path.md's V1 and V2 applied, `python3` and `python3 -S` | `OK` for all four, both ways |
| The ranking and cut tables of `BRN_VAN_EVOLVING` and `BRN_VAN_TWO` against the rule as a script | identical |
| Every `yaml items` block here | parses with PyYAML; every item has R4's keys |
| Re-check of 2026-11-20 after Bryan's decision of that day that a confirmation names no owner (§7): every edit of §2 with the reviewer's script; G1's four fixtures built from the changed example, under the validator as the fourth brainstorm commit leaves it, `python3` and `python3 -S` | each edit applies as before; `OK` for all four fixtures, both ways |

G1's fixtures were also run under the validator with the three brainstorm documents' checks applied (IV, BV and
MV; mvp-and-prototype-path.md §5.4): `OK` for all four, with `python3` and `python3 -S`. G2 repeats this at the
build; a fixture a check rejects is corrected in G1, never by weakening the check.

## 6. Staged files

None. The PRD skill's files change by the exact edits of §2; the eval cases are generated; the fixtures are
built from mvp-and-prototype-path.md's staged example.

## 7. Decisions and open questions

**Decisions made here, with reasons.**

1. *The kind and the cut are suggestions, never supplied values* (§3.2). SPEC-002's first rule is that the PRD
   records decisions and the AI doesn't make them; neither shape is the user's decision about a stage or about
   a requirement.
2. *A `yes` row marks no option.* Two of round 3's options mean "current", and choosing between them is a
   priority decision the cut doesn't hold. The suggestion is a line in the question instead.
3. *An unconfirmed cut is shown, not hidden.* It tells the user what the brainstorm proposed, in words that
   can't be read as a decision, and marks nothing.
4. *Fixed sentences for the four lines*, so two builds ask the same question and a regex grader can check it.
5. *C-08 gives the baseline, never the target.* The brainstorm records what is measured today; a target is a
   commitment, which is the PRD interview's to ask.
6. *The ranking sets only the order of the carried assumptions.* The PRD gains no field (the schema and
   ADR-003's document contract stay as they are), and the riskiest assumption is the first a reader meets.
7. *A confirmed assumption update changes the matching assumption's `state` only* (Bryan's decision below).
   Without it the update could never reach the PRD that carries the assumption, since the earlier BRN's link
   is in an existing item. Nothing else of that assumption or of the PRD's existing items changes, the Change
   Log row names it, and an approved PRD returns to review by the PRD skill's existing rule for an extension.
8. *A broken fixed shape never stops the run* (SPEC-002#ERR-12). The PRD can be drafted without it, and the
   brainstorm skill's validator, not the PRD skill, is where a BRN's shape is enforced.
9. *The report block ships in SKL-001 version 13, with the fourth commit.* It only reports what version 13
   writes, so the brainstorm skill needs no further version when the PRD side is built later.
10. *C-11's eval reads brownfield-iteration.md's staged example* (`brainstorm-brownfield`: BRN-001, PRD-001
    made from it, and BRN-002 with a confirmed update of BRN-001#ASM-01). The case depends on that example
    keeping those three facts; G2-style, the generator asserts them before writing the case.

**Decided by Bryan on 2026-11-19** (session fa59a935-ed2e-4502-b6c4-93bb6d847546), on the questions this section
left open. His words: "The brainstorm report block belongs in the fourth brainstorm commit. Schedule the PRD-side
work separately under SPEC-002 v10, before the PRD interview-at-scale build. A confirmed cut informs the release
question. Ask before writing release. On a PRD extension, a confirmed assumption update may change the matching
assumption's state only. Record it in the Change Log and return an approved PRD to review."

| Question | Decision | Where |
|---|---|---|
| Which SKL-001 version ships the report block? | "The brainstorm report block belongs in the fourth brainstorm commit" | §2.1, BEH-34 (as drafted) |
| Which is built first: this hand-off's PRD side, or the interview at scale? | The hand-off: "Schedule the PRD-side work separately under SPEC-002 v10, before the PRD interview-at-scale build" | Status line, §2, §2.7, §3.6. The edits of §2.2 to §2.5 are written against SKL-002 version 6's files, which are the files that build meets |
| Should a confirmed cut be written into `release` without asking? | No: "A confirmed cut informs the release question. Ask before writing release" | SPEC-002#BEH-29 (as drafted); SPEC-002#VER-50 checks that no release is written unasked, SPEC-002#VER-51 that it is asked |
| May an extension change the `state` of an existing assumption from a confirmed assumption update? | Yes, that field only: "a confirmed assumption update may change the matching assumption's state only. Record it in the Change Log and return an approved PRD to review" | SPEC-002#BEH-28 item 4, M2, P4, R1, R2; SPEC-002#VER-54 |

**Decided by Bryan on 2026-11-20** (session fa59a935-ed2e-4502-b6c4-93bb6d847546; his words are quoted).

| Question | Decision | Where |
|---|---|---|
| Do the two brainstorm lines this document reads name the owner? | No. Asked about the brainstorm skill's ask for the owner's name: "the owner isn't necessary". Of the four readings then offered: "No owner in the line at all" (the option's text: "The line is always "confirmed on <date>", never naming anyone.") | A confirmed C-11 row's `Status` starts `confirmed on`, and a confirmed cut's status line starts `First release cut: confirmed on`: M2, SPEC-002#BEH-28 item 4, SPEC-002#BEH-29 item 3, G1's `BRN_VAN_TWO_PROPOSED`, SPEC-002#VER-54's scaffold (changed). The PRD skill reads no name from either line, and never did |

**Open, for Bryan.** None.
