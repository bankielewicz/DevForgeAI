# MVP and prototype path

**Status:** proposal, written 2026-11-18 by claude-code on the model Fable 5.2 (session
fa59a935-ed2e-4502-b6c4-93bb6d847546) for Bryan's review. It changes nothing until SPEC-001's next version is
approved and built (README §8). Read [README.md](README.md) first: this document uses its rules (R1 to R10), its
shapes (C-01 to C-11) and its words without repeating them.

## Workflow steps this changes

| Step (SKILL.md's line, unchanged) | Today | Added by this document |
|---|---|---|
| 5. Propose dispositions and ask the user to confirm | Two questions: dispositions, convergence | After the proposals and before the save and the form: the assumption risk ranking (C-07), then the proposed first release cut (C-05). The form's third question (C-10), and what each answer writes |
| 6. Write the BRN | Template, frontmatter, Change Log | The ranking written into section 7 and the cut into section 6, as step 5 left them |
| 7. Validate the BRN | `validate_brn.py`, then the read-back | Checks MV-01 to MV-12; the read-back also covers the cut's status line (R3) |

## 1. Scope

**In.**

- The grammar of C-07, every cell: which assumptions are ranked, what `If wrong`, `Confidence` and `Cheapest test`
  hold, and the order of the rows.
- The grammar of C-05, every cell: which ideas have a row, the rule that proposes `yes` or `no`, and the eight
  fixed sentences of the `Why` cell.
- C-10's third question: its form, what each answer writes, the unconfirmed form, confirming later, extending.
- The validator's checks for both shapes' own form and consistency.
- The reference file `references/mvp-path.md` and the example `brainstorm-greenfield-mvp`.

**Out.**

- Section 8 and the content of `sources` (intake-and-evidence.md). Its check IV-06 compares section 8's bullets
  with the cut's `yes` rows; this document adds no check for that, and reads only the kind of each `sources`
  entry.
- What a framework writes into `value`, `effort`, `risk` and `score` (framework-catalog.md). The cut reads
  `score` and nothing else of the evaluation.
- Step 8's report and what the PRD skill does with the cut (prd-handoff-contract.md).
- A prototype's design, a build plan, estimates, dates. "First release" here means only: the promoted ideas the
  user wants in the first thing that ships.
- Any new field or collection (R1). Both shapes are prose tables. The links they record, which ideas an
  assumption stops and which idea needs another, live in table cells only.

## 2. Changes by file

Paths are under `src/claude/DevForgeAI/skills/brainstorm/` unless they start with `src/`. Each edit gives the old
text and the new text (R7). An old text is quoted from version 11 of the file (plugin 0.34.0). This document is
built fourth (README §8); the three documents built before it change the same files. Each old text below was
chosen so that it still stands exactly once after their edits: where one of them adds words after a quoted
sentence, this document's words go directly after that sentence, before theirs. S1 is no edit
(brownfield-iteration.md's B-S1 made it), and S7's and O3's old texts are that document's new texts. §5.4 lists
what was verified.

### 2.1 `SKILL.md`

Thirteen lines are added. With the three earlier documents' edits and these applied in build order, SKILL.md has
371 lines (316 today; R2's limit is 400); `skill_lines.py` in §5.4 counted them. The same commit then applies
prd-handoff-contract.md's H1 to H3 (step 8's report block, BEH-34), which brings it to 377.

**S1.** *Decisions that belong to the user*, its first line. No edit: brownfield-iteration.md's edit B-S1, built
before this document, already changed "Two decisions are the user's, never yours:" to "These decisions are the
user's, never yours:". The number S1 is kept so that the later numbers don't move.

**S2.** The same section: the third decision.

Old:

```text
- **Convergence**: whether the brainstorm is finished (`status: converged`).
```

New:

```text
- **Convergence**: whether the brainstorm is finished (`status: converged`).
- **The first release cut**: which promoted ideas are in the first release (section 6).
```

**S3.** The same section: the unconfirmed form.

Old:

```text
Propose both, then ask. Anything the user has not explicitly confirmed stays `disposition: open`,
`reason: null` and `status: draft`.
```

New:

```text
Propose them, then ask. Anything the user has not explicitly confirmed stays `disposition: open`,
`reason: null` and `status: draft`, and the cut stays `First release cut: proposed, not confirmed`.
```

"Propose both" spoke of two decisions; the list now holds four.

**S4.** *Workflow* (which framework-catalog.md renames *Working through the steps*), item 3.

Old:

```text
confirming dispositions and convergence belongs to step 5;
```

New:

```text
confirming dispositions, convergence and the first release cut belongs to step 5;
```

**S5.** Step 5, the first sentence.

Old:

```text
Propose a disposition and a one-line reason for each idea, and ask the user to confirm them and
whether the brainstorm has converged.
```

New:

```text
Propose a disposition and a one-line reason for each idea, and ask the user to confirm them and
whether the brainstorm has converged. Then, before saving and asking, rank the open assumptions and
propose the first release cut from those proposals, as [mvp-path.md](references/mvp-path.md) says.
```

**S6.** Step 5, the form's lead-in.

Old:

```text
both questions with `header: "Step 5"`:
```

New:

```text
every question with `header: "Step 5"`:
```

**S7.** Step 5, the third question (C-10). brownfield-iteration.md's edit B-S5, built before this one, adds its
question as item 3. S7 rewrites the list once: this document's question becomes 3 and that one 4, C-10's order.

Old (question 2's line and the item B-S5 adds):

```text
2. "Has the brainstorm converged?", options `Converged` and `Not yet`.
3. "Confirm these assumption updates?", only when a brownfield BRN's *Assumption updates* table has
   a row: options `Accept all as proposed` and `Leave them proposed`, each option's `preview` holding
   the table. Changes come typed under Other.
```

New:

```text
2. "Has the brainstorm converged?", options `Converged` and `Not yet`.
3. "Confirm the first release cut?", only when the cut table has a row: options `Accept as proposed`
   and `Leave it proposed`, each option's `preview` holding the cut's status line and table. Changes
   come typed under Other.
4. "Confirm these assumption updates?", only when a brownfield BRN's *Assumption updates* table has
   a row: options `Accept all as proposed` and `Leave them proposed`, each option's `preview` holding
   the table. Changes come typed under Other.
```

**S8.** Step 5, what the answers write.

Old:

```text
- Set `status: converged` only on *Converged*; otherwise `draft`.
```

New:

```text
- Set `status: converged` only on *Converged*; otherwise `draft`.
- Write the cut as `confirmed by <owner> on <today>` only on *Accept as proposed* or typed changes, and
  only when every idea in its table is then `promoted`; otherwise it stays `proposed, not confirmed`
  ([mvp-path.md](references/mvp-path.md#confirm-the-cut)).
```

**S9.** Step 6, item 2.

Old:

```text
Replace the example items with the real ones. Delete every HTML comment.
```

New:

```text
Replace the example items with the real ones. Delete every HTML comment. Write the assumption risk
   ranking into section 7 and the first release cut into section 6 exactly as step 5 left them.
```

**S10.** Step 7, item 2 (the read-back).

Old:

```text
Reset anything else to `disposition: open` with `reason: null`, or to
`status: draft`.
```

New:

```text
Reset anything else to `disposition: open` with `reason: null`, or to
   `status: draft`. The cut's status line says `confirmed` only when the user confirmed the cut in step 5;
   otherwise reset it to `First release cut: proposed, not confirmed`.
```

**S11.** *Output contract*.

Old:

```text
- **Decisions:** dispositions and `status: converged` appear only when the user confirmed them.
```

New:

```text
- **Decisions:** dispositions, `status: converged` and a `confirmed` first release cut appear only when
  the user confirmed them.
```

**S12.** *Examples*, "User says to proceed without questions".

Old:

```text
It writes every idea with `disposition: open` and `status: draft`, and puts
its proposals in section 6.
```

New:

```text
It writes every idea with `disposition: open` and `status: draft`, puts
its proposals in section 6, and leaves the first release cut `proposed, not confirmed`.
```

**S13.** *References*.

Old:

```text
- `scripts/validate_brn.py`: run at step 7; it applies the output rules mechanically.
```

New:

```text
- [references/mvp-path.md](references/mvp-path.md): read at step 5, before the work file is saved. It
  holds the assumption risk ranking, the first release cut and how the cut is confirmed.
- `scripts/validate_brn.py`: run at step 7; it applies the output rules mechanically.
```

### 2.2 `references/output-rules.md`

**O1.** *Contents*.

Old:

```text
- Unknowns
```

New:

```text
- First release cut and risk ranking
- Unknowns
```

**O2.** A new section before *Unknowns*.

Old:

```text
## Unknowns
```

New:

```text
## First release cut and risk ranking

Two prose tables carry the path to a first release. [mvp-path.md](mvp-path.md) defines every cell; the
validator checks them (MV-01 to MV-12) in a BRN that has the `Project kind:` line.

| Where | Heading | Holds |
|---|---|---|
| Section 7, after the `assumptions` block and before the bullets | `### Assumption risk ranking` | One row per active assumption whose `state` is `open`: `Rank`, `Assumption`, `If wrong`, `Confidence`, `Cheapest test`. `None.` when there is no such assumption |
| Section 6, after the convergence prose | `### First release cut` | The status line, then one row per active idea that is promoted or proposed for promotion: `Idea`, `In first release` (`yes` or `no`), `Why`. `No idea is promoted or proposed for promotion.` when there is no such idea |

The status line is `First release cut: proposed, not confirmed` until the user confirms the cut, then
`First release cut: confirmed by <owner> on YYYY-MM-DD`, with the frontmatter `owner`. A cell never holds a
`|`. Section 8 lists exactly the ideas whose row says `yes` (see *Collections and fields* for its bullets).

## Unknowns
```

**O3.** *Validation checklist*, item 14, after item 13.

Old (the last line of item 13, which brownfield-iteration.md's edit adds):

```text
    one the user confirmed. A greenfield BRN has none of the four headings.
```

New (that line, then item 14):

```text
    one the user confirmed. A greenfield BRN has none of the four headings.
14. In a BRN with the `Project kind:` line: section 7 holds `### Assumption risk ranking` and section 6
    holds `### First release cut`, each cell as [mvp-path.md](mvp-path.md) defines it; the cut's status
    line says `confirmed` only where the user confirmed the cut.
```

### 2.3 `references/work-file.md`

**W1.** *When to write it*, item 3.

Old:

```text
3. With step 5 in progress, once the proposals are made: before asking step 5's question,
```

New:

```text
3. With step 5 in progress, once the proposals are made, the assumptions ranked and the first release
   cut proposed ([mvp-path.md](mvp-path.md)): before asking step 5's question,
```

**W2.** *Its shape*, and what a continued run keeps. (*Continuing a run*, item 1, is changed by
framework-catalog.md and intake-and-evidence.md; this document leaves it alone.)

Old:

```text
- No HTML comments.
```

New:

```text
- From the save at step 5 on: the assumption risk ranking in section 7 and the first release cut in
  section 6, the cut's status line always `First release cut: proposed, not confirmed`. A confirmed cut
  is never written into the work file. Before that save, neither heading is written. A continued run
  keeps both tables as its work file holds them, and asks step 5 from them.
- No HTML comments.
```

### 2.4 `scripts/validate_brn.py`

The script stays standard-library only and gives the same verdict with and without PyYAML: the new code reads
only `lines` and the parsed items. V2 is self-contained (it applies the gate itself); intake-and-evidence.md's
helpers (`new_shape_kind`, `section_body`, `subsection`, `cells`) are not needed by it and are left as they are.

**V1.** The call, inside `check()`.

Old:

```text
    # --- optional YAML syntax check ----------------------------------------------------
```

New:

```text
    # --- the first release cut and the assumption risk ranking (new-shape BRNs) ----------
    sources = list_of("sources") if "sources" in fm else None
    check_mvp_path(lines, fm_end, fm, [x for _, x in sources or []], items, err)

    # --- optional YAML syntax check ----------------------------------------------------
```

**V2.** The checks. Old: the line `def main(argv):`. New: the block below, two empty lines, then
`def main(argv):`. The block applies the gate itself (its first test), so it needs nothing from the other
documents' validator edits; when intake-and-evidence.md's commit has added a gate helper, V2 keeps its own
test unchanged.

```python
MV_RANK_HEAD = ["Rank", "Assumption", "If wrong", "Confidence", "Cheapest test"]
MV_CUT_HEAD = ["Idea", "In first release", "Why"]
MV_NO_ROWS = "No idea is promoted or proposed for promotion."
MV_FLAG = "Needs review: no rule supports this value."
MV_PROTOTYPE = (
    "prototype", "prototypes", "mock-up", "mock-ups", "mockup", "mockups", "pilot", "pilots", "trial",
    "trials", "beta", "demo", "demos", "experiment", "experiments", "a/b", "landing page", "smoke test",
    "fake door", "build", "launch",
)
MV_INTERVIEW = (
    "ask", "asks", "interview", "interviews", "survey", "surveys", "poll", "polls", "observe", "shadow",
    "talk to", "speak to", "questionnaire", "focus group", "workshop",
)
MV_IMPACT = {"Fatal": 3, "Serious": 2, "Minor": 0}
MV_DOUBT = {"low": 3, "medium": 2, "high": 1}
MV_KINDS = {"high": ("data", "document", "ticket"), "medium": ("interview", "url", "note")}
MV_IF_WRONG = re.compile(
    r"(Fatal|Serious): stops (IDEA-\d{2}(?:, IDEA-\d{2})*) \((\d+) of (\d+) in the cut table\)\."
    r"|(Minor): stops no idea in the cut table \(0 of (\d+)\)\.")
MV_STATUS = re.compile(
    r"First release cut: (?:proposed, not confirmed|confirmed by (.+) on (\d{4}-\d{2}-\d{2}))")


def cheapest_test(asm_id, validation):
    """The 'Cheapest test' cell (C-07) for an assumption's quoted `validation` value."""
    text = validation[1:-1].replace('\\"', '"').replace("|", "/").strip() if quoted(validation) else ""
    if not text or text.startswith("[NEEDS CLARIFICATION:"):
        return f"[NEEDS CLARIFICATION: how to test {asm_id}]"
    m = re.search(r"[.?!](?= |$)", text)
    sentence = text[:m.end()] if m else text + "."
    low = sentence.lower()

    def has(words):
        return any(re.search(r"(?<![a-z0-9])" + re.escape(w) + r"(?![a-z0-9])", low) for w in words)

    kind = "Prototype" if has(MV_PROTOTYPE) else "Interview" if has(MV_INTERVIEW) else "Data"
    return f"{kind}: {sentence}"


def check_mvp_path(lines, fm_end, fm, sources, items, err):
    """MV-01 to MV-12: the assumption risk ranking (C-07) and the first release cut (C-05)."""
    plain, inside = [], False  # indexes of the lines after the frontmatter and outside every fence
    for i in range(fm_end + 1, len(lines)):
        if lines[i].startswith("```"):
            inside = not inside
        elif not inside:
            plain.append(i)
    if not any(" ".join(lines[i].lower().split()).startswith("project kind:") for i in plain):
        return  # an earlier-shape BRN: none of these checks applies

    def at(text):
        return [i for i in plain if lines[i].rstrip() == text]

    def block(i, stop):
        """Non-blank lines after heading line i, up to a heading, a line `stop` accepts, or the end."""
        out = []
        for j in plain:
            if j > i:
                if lines[j].startswith("#") or stop(lines[j]):
                    break
                if lines[j].strip():
                    out.append(j)
        return out

    def cells(i):
        s = lines[i].strip()
        return [c.strip() for c in s[1:-1].split("|")] if len(s) > 1 and s[0] == "|" == s[-1] else None

    def table(rows, head, what, mv):
        """The data rows [(index, cells)] of the table that starts at rows[0], or None once reported."""
        if not rows or cells(rows[0]) != head:
            err((rows[0] if rows else 0) + 1,
                f"{what}: the table must start with the header row '| {' | '.join(head)} |' ({mv})")
            return None
        if len(rows) < 3 or not re.fullmatch(r"\|(\s*:?-+:?\s*\|)+", lines[rows[1]].strip()):
            err(rows[0] + 1,
                f"{what}: a |---| row and at least one row must follow the header row ({mv})")
            return None
        out = []
        for i in rows[2:]:
            c = cells(i)
            if c is None or len(c) != len(head):
                err(i + 1, f"{what}: each row has exactly {len(head)} cells, with no '|' inside a cell, "
                    f"and nothing else follows the table ({mv})")
                return None
            out.append((i, c))
        return out

    def active(collection):
        return [it for it in items[collection] if it["fields"].get("status", (0, ""))[1] == "active"]

    def field(it, name):
        return it["fields"].get(name, (0, ""))[1]

    def score(iid):
        v = field(ideas[iid], "score")
        return float(v) if NUMBER.match(v) else float("-inf")

    sec = [(at(h) or [None])[0] for h in SECTIONS[5:]]
    if None in sec or sorted(sec) != sec:
        return  # a missing or misplaced section heading is already reported
    s6, s7, s8 = sec[:3]
    ideas = {it["id"]: it for it in active("ideas")}
    open_asm = {it["id"]: it for it in active("assumptions") if field(it, "state") == "open"}

    # --- the first release cut (section 6): MV-08, MV-09 ---------------------------------------
    cut, confirmed, status_at, cut_ok = {}, None, 0, False  # cut: idea ID -> (index, yes or no, why)
    heads = at("### First release cut")
    if len(heads) != 1 or not s6 < heads[0] < s7:
        err(s6 + 1, "section 6 must hold exactly one '### First release cut' heading, and no other "
            "section may hold one (MV-08)")
    else:
        rows = block(heads[0], lambda l: False)
        m = MV_STATUS.fullmatch(lines[rows[0]].rstrip()) if rows else None
        if not m:
            err(heads[0] + 1, "the first line under '### First release cut' must be 'First release cut: "
                "proposed, not confirmed' or 'First release cut: confirmed by <owner> on YYYY-MM-DD' (MV-08)")
        else:
            confirmed, status_at = (m.groups() if m.group(1) else None), rows[0] + 1
            if len(rows) == 2 and lines[rows[1]].rstrip() == MV_NO_ROWS:
                data = []
            else:
                data = table(rows[1:], MV_CUT_HEAD, "first release cut", "MV-09")
            cut_ok = data is not None
            for i, (iid, value, why) in data or []:
                if iid not in ideas or field(ideas[iid], "disposition") not in ("promoted", "open"):
                    err(i + 1, f"first release cut: {iid!r} is not an active idea whose disposition is "
                        "promoted or open (MV-09)")
                    cut_ok = False
                elif cut and iid <= max(cut):
                    err(i + 1, "first release cut: rows are in idea ID order, each idea once; "
                        f"{iid} is out of place (MV-09)")
                    cut_ok = False
                if value not in ("yes", "no"):
                    err(i + 1, f"first release cut: 'In first release' for {iid} must be yes or no (MV-09)")
                    cut_ok = False
                cut[iid] = (i, value, why)
            for iid in ideas:
                if cut_ok and field(ideas[iid], "disposition") == "promoted" and iid not in cut:
                    err(heads[0] + 1, f"first release cut: the promoted idea {iid} has no row (MV-09)")
                    cut_ok = False
    yes = [iid for iid in sorted(cut) if cut[iid][1] == "yes"]
    flagged = [iid for iid in sorted(cut) if cut[iid][2] == MV_FLAG]

    # --- the assumption risk ranking (section 7): MV-01 to MV-07 -----------------------------------
    rank, rank_ok = {}, False  # assumption ID -> (rank, the ideas it stops)
    heads = at("### Assumption risk ranking")
    fences = [i for i in range(s7, s8) if lines[i].startswith("```")]
    bullets = [i for i in plain if s7 < i < s8 and lines[i].startswith("- ")]
    if (len(heads) != 1 or not s7 < heads[0] < s8 or (fences and heads[0] < fences[-1])
            or (bullets and heads[0] > bullets[0])):
        err(s7 + 1, "section 7 must hold exactly one '### Assumption risk ranking' heading, after its item "
            "block and before its bullets, and no other section may hold one (MV-01)")
    else:
        rows = block(heads[0], lambda l: l.startswith("- "))
        if len(rows) == 1 and lines[rows[0]].rstrip() == "None.":
            data = []
        else:
            data = table(rows, MV_RANK_HEAD, "assumption risk ranking", "MV-02")
        rank_ok = data is not None
        if rank_ok and sorted(c[1] for _, c in data) != sorted(open_asm):
            want = ", ".join(sorted(open_asm)) or "none, so the line 'None.' replaces the table"
            err(heads[0] + 1, "assumption risk ranking: one row for each active assumption whose state is "
                f"open, and no other row ({want}) (MV-03)")
            rank_ok = False
        kinds = {q[1:].split(": ", 1)[0] for q in sources if ": " in q}
        keys = []
        for n, (i, (r, aid, wrong, conf, test)) in enumerate(data or [], 1):
            if r != str(n):
                err(i + 1, f"assumption risk ranking: Rank counts 1, 2, 3 and so on; row {n} says {r!r} "
                    "(MV-03)")
                rank_ok = False
            m = MV_IF_WRONG.fullmatch(wrong)
            stops = m.group(2).split(", ") if m and m.group(2) else []
            cls = (m.group(1) or m.group(5)) if m else None
            if not m:
                err(i + 1, f"{aid}: 'If wrong' must read 'Fatal: stops IDEA-NN, IDEA-NN (N of M in the cut "
                    "table).', 'Serious: stops IDEA-NN (N of M in the cut table).' or 'Minor: stops no idea "
                    "in the cut table (0 of M).' (MV-04)")
                rank_ok = False
            elif cut_ok:
                want = "Minor" if not stops else "Fatal" if len(stops) == len(cut) else "Serious"
                if (stops != sorted(set(stops)) or any(s not in cut for s in stops) or cls != want
                        or int(m.group(3) or 0) != len(stops) or int(m.group(4) or m.group(6)) != len(cut)):
                    err(i + 1, f"{aid}: 'If wrong' lists rows of the cut table in ID order and counts them "
                        f"against its {len(cut)} row(s): Fatal when it lists every row, Serious when it lists "
                        "some, Minor when it lists none (MV-04)")
                    rank_ok = False
            if conf not in MV_DOUBT:
                err(i + 1, f"{aid}: Confidence must be high, medium or low (MV-05)")
                rank_ok = False
            elif conf != "low" and not kinds & set(MV_KINDS[conf]):
                need = MV_KINDS[conf]
                err(i + 1, f"{aid}: Confidence {conf} needs a sources entry of kind {need[0]}, {need[1]} or "
                    f"{need[2]} (MV-05)")
            want = cheapest_test(aid, field(open_asm[aid], "validation")) if aid in open_asm else test
            if test != want:
                err(i + 1, f"{aid}: 'Cheapest test' must be {want!r} (MV-07)")
            if m and conf in MV_DOUBT:
                rank[aid] = (n, stops)
                keys.append((-MV_IMPACT[cls] * MV_DOUBT[conf], -MV_IMPACT[cls], -MV_DOUBT[conf],
                             -len(stops), aid))
        if rank_ok and keys != sorted(keys):
            order = ", ".join(k[-1] for k in sorted(keys))
            err(heads[0] + 1, f"assumption risk ranking: rows out of order; the order is {order} (MV-06)")
            rank_ok = False

    # --- each row's reason, the top three covered, a confirmed cut: MV-10 to MV-12 -----------------
    if cut_ok and rank_ok:
        top = {a: v for a, v in rank.items() if v[0] <= 3}
        tested, by_user = [], False
        for iid in sorted(cut):
            i, value, why = cut[iid]
            mine = sorted((v[0], a) for a, v in top.items() if iid in v[1])
            ok = False
            m = re.fullmatch(r"Tests (ASM-\d{2}), ranked ([1-3])\.", why)
            if m and value == "yes":
                ok = (int(m.group(2)), m.group(1)) in mine and m.group(1) not in tested
                tested.append(m.group(1))
            m = re.fullmatch(r"Tests (ASM-\d{2}), ranked ([1-3]), which (IDEA-\d{2}) already tests\.", why)
            if m and value == "no":
                ok = (bool(mine) and mine[0] == (int(m.group(2)), m.group(1)) and m.group(3) != iid
                      and m.group(3) in yes and m.group(3) in top[m.group(1)][1])
            m = re.fullmatch(r"Needed by (IDEA-\d{2}), which is in the first release\.", why)
            if m and value == "yes":
                ok = m.group(1) != iid and m.group(1) in yes
            if why == "Highest score; no assumption ranked 1 to 3 picks an idea." and value == "yes":
                ok = iid == max(sorted(cut), key=score) and not any(v[1] for v in top.values())
            if why == "Tests no assumption ranked 1 to 3." and value == "no":
                ok = not mine
            if (why, value) in (("Included by the user.", "yes"), ("Left out by the user.", "no")):
                ok = by_user = True
            if not ok and why != MV_FLAG:
                err(i + 1, f"first release cut: the Why cell of {iid} is not one of the fixed sentences for "
                    f"'{value}', or it does not match the ranking or the other rows (MV-10)")
        for a, v in sorted(top.items()):
            if not by_user and not flagged and v[1] and not set(v[1]) & set(yes):
                err(cut[v[1][0]][0] + 1, f"first release cut: no 'yes' row tests {a}, ranked {v[0]}; one of "
                    f"{', '.join(v[1])} must be in the first release (MV-11)")
        if cut and not yes and not by_user and not flagged:
            err(status_at, "first release cut: a cut that the user did not change has a 'yes' row (MV-11)")
    if confirmed and cut_ok:
        owner = fm.get("owner", (0, '""'))[1][1:-1]
        created, updated = (fm.get(k, (0, ""))[1] for k in ("created", "updated"))
        try:
            real = bool(datetime.date.fromisoformat(confirmed[1]))
        except ValueError:
            real = False
        if (confirmed[0] != owner or owner.startswith("[NEEDS CLARIFICATION") or not real
                or not created <= confirmed[1] <= updated):
            err(status_at, "first release cut: a confirmed cut names the frontmatter owner (never a NEEDS "
                "CLARIFICATION marker) and a real date from created to updated (MV-12)")
        if flagged:
            err(cut[flagged[0]][0] + 1, "first release cut: a confirmed cut holds no row that says "
                f"'{MV_FLAG}'; flagged: {', '.join(flagged)} (MV-12)")
        loose = [iid for iid in sorted(cut) if field(ideas[iid], "disposition") != "promoted"]
        if loose or not cut:
            err(status_at, "first release cut: confirmed only when the table has a row and every row's idea "
                f"is promoted; not promoted: {', '.join(loose) or 'there is no row'} (MV-12)")
```

**V3.** The module docstring's last sentence.

Old:

```text
It cannot check whether the user confirmed a disposition or convergence: that is the skill's job.
```

New:

```text
It cannot check whether the user confirmed a disposition, convergence or the first release cut: that is
the skill's job.
```

### 2.5 `src/tests/brainstorm/test_validate_brn.py`

Tests are written first (README §8) and run every case three ways, as the file's classes already do.

**T1.** The example's path.

Old:

```text
PROBES = ROOT / "src/codex/devforgeai/import-evidence/validator-probes"
```

New:

```text
PROBES = ROOT / "src/codex/devforgeai/import-evidence/validator-probes"
MVP_EXAMPLE = ROOT / "src/staging/examples/brainstorm-greenfield-mvp/BRN-001.md"
```

**T2.** The tests, as the last methods of class `Base`. Old: the line
`@unittest.skipUnless(_has_yaml([]), "PyYAML is not installed for this interpreter")`. New: the methods
below, two empty lines, then that line.

```python
    # --- The path to a first release: MV-01 to MV-12, new-shape BRNs only ------------------------

    def mvp(self, *edits):
        text = MVP_EXAMPLE.read_text(encoding="utf-8")
        for old, new in edits:
            text = edit(text, old, new)
        return text

    def mvp_unconfirmed(self):
        """The example as a run with nobody to confirm writes it: ideas open, draft, the cut proposed."""
        text = re.sub(r'disposition: (?:promoted|parked|rejected)\n    reason: "[^\n]*"',
                      "disposition: open\n    reason: null", self.mvp())
        text = edit(text, "status: converged", "status: draft")
        return edit(text, "First release cut: confirmed by Maya Okafor on 2026-11-18",
                    "First release cut: proposed, not confirmed")

    def test_mvp_example_passes(self):
        self.assert_valid(self.mvp())

    def test_mvp_unconfirmed_cut_passes(self):
        self.assert_valid(self.mvp_unconfirmed())

    def test_mvp_rows_set_by_the_user_pass(self):
        self.assert_valid(self.mvp(
            ("| IDEA-03 | no | Tests ASM-02, ranked 2, which IDEA-01 already tests. |",
             "| IDEA-03 | yes | Included by the user. |"),
            ("\n\n## Change Log", "\n- IDEA-03: shorter waits at the stop; baseline "
             "[NEEDS CLARIFICATION: how long commuters wait today]\n\n## Change Log")))

    def mvp_idea_01_left_out(self):
        """The unconfirmed example after the typed change 'IDEA-01 out': reasons refreshed, one row flagged."""
        text = self.mvp_unconfirmed()
        for old, new in (
                ("| IDEA-01 | yes | Tests ASM-01, ranked 1. |", "| IDEA-01 | no | Left out by the user. |"),
                ("| IDEA-02 | yes | Tests ASM-03, ranked 3. |", "| IDEA-02 | yes | Tests ASM-01, ranked 1. |"),
                ("| IDEA-03 | no | Tests ASM-02, ranked 2, which IDEA-01 already tests. |",
                 "| IDEA-03 | no | Needs review: no rule supports this value. |")):
            text = edit(text, old, new)
        return re.sub(r"- IDEA-01: [^\n]*\n", "", text)

    def test_mvp_a_flagged_row_passes_in_a_proposed_cut(self):
        self.assert_valid(self.mvp_idea_01_left_out())

    def test_mvp_a_stale_reason_is_rejected_after_a_user_change(self):
        text = edit(self.mvp_idea_01_left_out(), "| IDEA-03 | no | Needs review: no rule supports this value. |",
                    "| IDEA-03 | no | Tests ASM-02, ranked 2, which IDEA-01 already tests. |")
        self.assert_rejects(text, r"the Why cell of IDEA-03 .* \(MV-10\)$")

    def test_mvp_a_user_sentence_is_never_checked_against_the_rules(self):
        self.assert_valid(edit(self.mvp_idea_01_left_out(),
                               "| IDEA-03 | no | Needs review: no rule supports this value. |",
                               "| IDEA-03 | no | Left out by the user. |"))

    def test_mv12_a_confirmed_cut_holds_no_flagged_row(self):
        text = self.mvp(("| IDEA-05 | no | Tests no assumption ranked 1 to 3. |",
                         "| IDEA-05 | no | Needs review: no rule supports this value. |"))
        self.assert_rejects(text, r"a confirmed cut holds no row that says .*; flagged: IDEA-05 \(MV-12\)$")

    def test_mvp_no_open_assumption_takes_the_highest_score(self):
        text = self.mvp().replace("    state: open\n", "    state: validated\n")
        text = re.sub(r"\| Rank \|[^\n]*\n\|---[^\n]*\n(?:\| \d \| ASM[^\n]*\n)+", "None.\n", text)
        for old, new in (
                ("| IDEA-01 | yes | Tests ASM-01, ranked 1. |",
                 "| IDEA-01 | yes | Highest score; no assumption ranked 1 to 3 picks an idea. |"),
                ("| IDEA-02 | yes | Tests ASM-03, ranked 3. |",
                 "| IDEA-02 | no | Tests no assumption ranked 1 to 3. |"),
                ("| IDEA-03 | no | Tests ASM-02, ranked 2, which IDEA-01 already tests. |",
                 "| IDEA-03 | no | Tests no assumption ranked 1 to 3. |")):
            text = edit(text, old, new)
        text = re.sub(r"- IDEA-02: [^\n]*\n", "", text)
        self.assert_valid(text)

    def test_mvp_no_cut_row_passes(self):
        text = re.sub(r"\| Idea \|[^\n]*\n\|---[^\n]*\n(?:\| IDEA[^\n]*\n)+",
                      "No idea is promoted or proposed for promotion.\n", self.mvp_unconfirmed())
        text = re.sub(r"(?:Serious|Fatal): stops [^|]*\|", "Minor: stops no idea in the cut table (0 of 0). |", text)
        text = text.replace("| medium |", "| low |").replace("| high |", "| low |")
        text = re.sub(r"- IDEA-01: [^\n]*\n- IDEA-02: [^\n]*\n", "- None.\n", text)
        self.assert_valid(text)

    def test_mvp_checks_skip_an_earlier_shape_brn(self):
        self.assert_valid(self.mvp(("Project kind: greenfield\n\n", ""),
                                   ("| IDEA-01 | yes | Tests ASM-01, ranked 1. |", "| IDEA-01 | maybe | |")))

    def test_mv01_ranking_heading_is_required(self):
        self.assert_rejects(self.mvp(("### Assumption risk ranking\n\n", "")), r"\(MV-01\)$")

    def test_mv02_ranking_header_row_is_fixed(self):
        self.assert_rejects(self.mvp(("| Rank | Assumption | If wrong | Confidence | Cheapest test |",
                                      "| Rank | Assumption | If wrong |")), r"\(MV-02\)$")

    def test_mv03_ranking_rows_are_the_open_assumptions(self):
        self.assert_rejects(self.mvp(("    state: open\n```", "    state: validated\n```")),
                            r"ASM-01, ASM-02, ASM-03\) \(MV-03\)$")

    def test_mv04_if_wrong_counts_the_cut_rows(self):
        self.assert_rejects(self.mvp(("(1 of 4 in the cut table)", "(1 of 3 in the cut table)")),
                            r"ASM-03: 'If wrong' .* \(MV-04\)$")

    def test_mv05_confidence_needs_a_source_of_its_kind(self):
        self.assert_rejects(self.mvp(('  - "note: Maya Okafor, conversation of 2026-11-18"\n', "")),
                            r"ASM-03: Confidence medium needs .* \(MV-05\)$")

    def test_mv06_ranking_order_is_checked(self):
        first, second = (re.search(rf"^\| {n} \| ASM-0{n} [^\n]*$", self.mvp(), re.M).group(0) for n in (1, 2))
        text = self.mvp((first + "\n" + second, "| 1 |" + second[5:] + "\n| 2 |" + first[5:]))
        self.assert_rejects(text, r"the order is ASM-01, ASM-02, ASM-03, ASM-04 \(MV-06\)$")

    def test_mv07_cheapest_test_comes_from_the_validation(self):
        self.assert_rejects(self.mvp(("| Data: Count the paid jobs per week in the van job log. |",
                                      "| Interview: Count the paid jobs per week in the van job log. |")),
                            r"must be 'Data: Count the paid jobs per week in the van job log\.' \(MV-07\)$")

    def test_mv08_cut_status_line_is_fixed(self):
        self.assert_rejects(self.mvp(("First release cut: confirmed by Maya Okafor on 2026-11-18",
                                      "First release cut: confirmed")), r"\(MV-08\)$")

    def test_mv09_every_promoted_idea_has_a_cut_row(self):
        self.assert_rejects(self.mvp(("| IDEA-05 | no | Tests no assumption ranked 1 to 3. |\n", "")),
                            r"the promoted idea IDEA-05 has no row \(MV-09\)$")

    def test_mv09_a_parked_idea_has_no_cut_row(self):
        self.assert_rejects(self.mvp(("| IDEA-05 | no | Tests no assumption ranked 1 to 3. |\n",
                                      "| IDEA-05 | no | Tests no assumption ranked 1 to 3. |\n"
                                      "| IDEA-07 | no | Tests no assumption ranked 1 to 3. |\n")),
                            r"'IDEA-07' is not an active idea .* \(MV-09\)$")

    def test_mv10_why_is_a_fixed_sentence(self):
        self.assert_rejects(self.mvp(("| IDEA-05 | no | Tests no assumption ranked 1 to 3. |",
                                      "| IDEA-05 | no | Too big for a first release. |")),
                            r"the Why cell of IDEA-05 .* \(MV-10\)$")

    def test_mv10_why_must_match_the_ranking(self):
        self.assert_rejects(self.mvp(("| IDEA-01 | yes | Tests ASM-01, ranked 1. |",
                                      "| IDEA-01 | yes | Tests ASM-03, ranked 3. |")),
                            r"the Why cell of IDEA-01 .* \(MV-10\)$")

    def test_mv11_each_of_the_top_three_is_tested(self):
        self.assert_rejects(self.mvp(("| IDEA-02 | yes | Tests ASM-03, ranked 3. |",
                                      "| IDEA-02 | no | Tests ASM-01, ranked 1, which IDEA-01 already tests. |")),
                            r"no 'yes' row tests ASM-03, ranked 3; one of IDEA-02 .* \(MV-11\)$")

    def test_mv12_a_confirmed_cut_needs_promoted_ideas(self):
        text = edit(self.mvp_unconfirmed(), "First release cut: proposed, not confirmed",
                    "First release cut: confirmed by Maya Okafor on 2026-11-18")
        self.assert_rejects(text, r"not promoted: IDEA-01, IDEA-02, IDEA-03, IDEA-05 \(MV-12\)$")

    def test_mv12_a_confirmed_cut_names_the_owner_and_a_date_in_range(self):
        for new in ("confirmed by claude-code on 2026-11-18", "confirmed by Maya Okafor on 2026-11-19",
                    "confirmed by Maya Okafor on 2026-02-30"):
            with self.subTest(new=new):
                self.assert_rejects(self.mvp(("confirmed by Maya Okafor on 2026-11-18", new)),
                                    r"names the frontmatter owner .* \(MV-12\)$")
```

### 2.6 New files

| File | From |
|---|---|
| `references/mvp-path.md` | [staged/skills/brainstorm/references/mvp-path.md](staged/skills/brainstorm/references/mvp-path.md) |
| `src/staging/examples/brainstorm-greenfield-mvp/BRN-001.md` and `README.md` | [staged/examples/brainstorm-greenfield-mvp/](staged/examples/brainstorm-greenfield-mvp/) |
| `src/claude/DevForgeAI/evals/brainstorm/proposes-first-release-cut/` | VER-35 (§5.1): `prompt.md` and one file per grader in `graders/` |
| `src/claude/DevForgeAI/evals/brainstorm/ranks-assumptions-by-risk/` | VER-36 (§5.1) |

Each eval case's `prompt.md` has the frontmatter of `no-unconfirmed-dispositions/prompt.md` with its own
`description` and `tags: [brainstorm, ver-35]` or `[brainstorm, ver-36]`. Each grader file has the frontmatter
keys the item gives (`type`, `target`, `match`, `flags`; an `llm` grader with `focus`) and the pattern or the
question as its body.

### 2.7 The template

`assets/brainstorm.md` is staged once, by intake-and-evidence.md (README §7), and already holds both shapes:
`### First release cut` with the unconfirmed status line and a one-row table in section 6, and
`### Assumption risk ranking` with a one-row table in section 7. This document changes nothing in it. What it
relies on: each example cell that step 6 must replace is an angle-bracket placeholder starting with a lowercase
letter, so the validator's leftover check rejects a BRN that kept one.

### 2.8 SPEC-001's next version

| SPEC-001 item | Change |
|---|---|
| BEH-06 | Extended by BEH-32: the step-5 form gains the third question; what its answers write |
| BEH-08 | Extended by BEH-33: the two shapes are written at step 6 |
| BEH-09 | Extended by BEH-33: checks MV-01 to MV-12; the read-back covers the cut's status line |
| BEH-14, §4 (work file) | Extended by BEH-33: the work file holds both tables from the step-5 save on, the cut always proposed; a continued run keeps them |
| §5, downstream contract | Gains: "`First release cut: confirmed by …` appears only after the user confirmed the cut" |
| New | BEH-30, BEH-31, BEH-32, BEH-33, ERR-10, VER-35 to VER-38 |

## 3. Behaviour

The staged [mvp-path.md](staged/skills/brainstorm/references/mvp-path.md) is the wording the skill follows. This
section is the specification it implements; where the two differ, this section is right and the staged file is
corrected.

```yaml items
behaviors:
  - id: BEH-30
    status: proposed
    rule: |-
      1. At step 5, after a disposition is proposed for each idea and before the work file is saved, rank every active assumption whose state is open, as §3.1 to §3.4 define.
      2. The cut rows are the active ideas whose disposition is promoted, or is open with a step-5 proposal of promoted, in ID order; M is their number.
      3. For each ranked assumption, decide for each cut row whether the idea depends on it (§3.1's test), and write the If wrong cell from the rows that do: Fatal when all M rows depend and M is at least 1, Serious when at least one and fewer than M depend, Minor when none does, in §3.2's three fixed forms.
      4. Write Confidence as high, medium or low from the kinds of the sources entries that support the assumption (§3.3).
      5. Write Cheapest test as the kind that §3.4's decision list gives, a colon, a space and the first sentence of the assumption's validation; or the marker [NEEDS CLARIFICATION: how to test ASM-NN] when the validation is empty or itself a marker.
      6. Order the rows by risk points (impact times doubt), then impact, then doubt, then the number of rows stopped, then assumption ID, and number them from 1 (§3.5).
      7. With no active assumption whose state is open, write the line None. in place of the table.
    changes: new
    lands_in: "references/mvp-path.md, 'The cut rows' and 'Rank the assumptions'; SKILL.md step 5 (S5)"
  - id: BEH-31
    status: proposed
    rule: |-
      1. After the ranking and before the work file is saved, propose yes or no for every cut row from the ranking alone, by §3.6's four steps: one idea picked for each assumption ranked 1 to 3 that stops a row and has no yes row yet (highest score, a null score lowest, lowest ID on a tie); the highest-scoring row when nothing was picked; every cut row that a yes idea needs, repeated until nothing is added; no for every other row.
      2. Write each row's Why cell as one of the five fixed sentences of §3.7 that the step producing the row names.
      3. With at least one cut row, the proposal holds at least one yes. With none, write the line No idea is promoted or proposed for promotion. in place of the table.
      4. When a yes idea needs an active idea that is not a cut row, change nothing in the cut and add §3.6's NEEDS CLARIFICATION bullet to section 7.
      5. A proposal's status line is exactly First release cut: proposed, not confirmed.
    changes: new
    lands_in: "references/mvp-path.md, 'Propose the cut'; SKILL.md step 5 (S5)"
  - id: BEH-32
    status: proposed
    rule: |-
      1. When the cut table has a row, step 5's form (C-10) holds a third question after the convergence question: 'Confirm the first release cut?', header 'Step 5', the options 'Accept as proposed' (description 'The ideas marked yes are the first release.') and 'Leave it proposed' (description 'The table stays a proposal; you can confirm it later.'), in that order, none marked recommended, each option's preview holding the status line, an empty line and the cut table; when the table is too long for a preview, the preview lists each row's idea ID with yes or no and the question says the reasons are in the reply. When the table has no row, the question is left out.
      2. Without AskUserQuestion and with a user to ask, the status line and the table are shown in plain text with the dispositions and the same question is asked. When no question is asked (the waiver's Proceed without questions, or nobody to ask), the cut stays proposed.
      3. The answers are applied in this order: the dispositions the first question confirmed are written, and in a brownfield run the assumption updates the fourth question confirmed (brownfield-iteration.md, BEH-28 and BEH-29); the cut rows and the ranked assumptions (the active ones whose state is open) are listed again; when either list differs from the one the form showed (an idea entered or left the cut rows, or a confirmed update closed one of this BRN's own assumptions), the ranking and the cut are made again from the new lists, the status line stays proposed whatever the third answer was, and the reply names the ideas that entered or left the table and the assumptions that left the ranking.
      4. Otherwise: 'Accept as proposed', or typed text that accepts the table, keeps the rows; typed changes set each named row to the stated value and its Why cell to 'Included by the user.' (yes) or 'Left out by the user.' (no); every other row keeps its value and has its Why cell derived again by §3.10's refresh, which gives it a rule sentence that holds or, when no rule supports its value, the flag 'Needs review: no rule supports this value.'; 'Leave it proposed', a dismissal, no answer, or typed text that states neither an acceptance nor a change keeps the rows and the proposed status line.
      5. After an acceptance or typed changes, the status line becomes First release cut: confirmed by <owner> on <today> (the frontmatter owner without its quotes; today as YYYY-MM-DD) only when every row's idea then has disposition promoted, no row is flagged and the owner is not a NEEDS CLARIFICATION marker; otherwise it stays proposed with the rows as item 4 left them, and the reply names the ideas that are not promoted and the rows that are flagged.
      6. A cut is never written as confirmed in any other way: not from a recommended option, not by the skill's own choice, not in the work file.
      7. A confirmation that arrives after the BRN is written follows SKILL.md's 'Decisions that belong to the user': step 5 is marked again and its form asked, the third question showing the table as the BRN holds it; when that table holds a flagged row, the question's text names each flagged row with its value as item 10 gives it and its answer is read as item 10 says, which counts as the one further asking; only then is the BRN edited in place, validated again and reported.
      8. When a new-shape BRN is extended, the ranking is made again from the BRN as it then stands and the cut rows are listed. When their idea IDs are the same set as the rows of the BRN's cut table, each row whose Why cell is 'Included by the user.' or 'Left out by the user.' keeps its value and its sentence, and every other row is proposed again by §3.11's rule (§3.6 with the user's rows kept). When the IDs differ, every row is proposed again by §3.6 and none is kept, and the reply and the Change Log row name each row the user had set, with its value. In both cases the status line is kept only when the new table equals the BRN's in every cell; otherwise the new table is written as proposed, the third question asks about it, and the reply and the Change Log row name the rows that changed.
      9. 'Included by the user.' and 'Left out by the user.' are written only on a row whose value the user stated: a row a typed change names, or a flagged row the user accepted when the third question was asked again (item 10). No other event writes them.
      10. When the refresh flags a row, the status line is the proposed one whatever the answer was. When a question can be asked, the third question is asked once more, alone in a form tagged step 5, its text naming each flagged row with its value ('Confirm the first release cut? Needs review: IDEA-04 (no).'), with the same options and the refreshed table in each preview: an acceptance turns each flagged row into the user's (its Why cell becomes the user sentence for its value); typed changes are applied; either is followed by one more refresh and by item 5; 'Leave it proposed', a dismissal or no answer leaves the flags. The question is never asked a third time. A row still flagged, or flagged when no question can be asked, stays flagged under the proposed status line, and the reply names it.
    changes: "extends SPEC-001 BEH-06"
    lands_in: "SKILL.md 'Decisions that belong to the user' (S2, S3), Workflow item 3 (S4), step 5 (S6 to S8); references/mvp-path.md, 'Confirm the cut' and 'Later runs'"
  - id: BEH-33
    status: proposed
    rule: |-
      1. Step 6 writes '### Assumption risk ranking' into section 7, after the assumptions item block and before the bullets, and '### First release cut' into section 6, after the convergence prose, each exactly as step 5 left it, in a new BRN and in an extended new-shape BRN; an extended earlier-shape BRN gets neither.
      2. The work file holds both from the step-5 save on, the cut's status line always the proposed one; a continued run that finds them in its work file keeps them and asks step 5 from them.
      3. A draft BRN saved before step 5's proposals exist (SPEC-001 ERR-02) holds the cut's line for no row and a ranking made with M = 0.
      4. Step 7's validator applies MV-01 to MV-12 (§5.2) to a new-shape BRN and none of them to an earlier-shape BRN, with the same verdict with and without PyYAML.
      5. Step 7's read-back checks that the cut's status line says confirmed only when the user confirmed the cut at step 5 of this run, or the BRN being extended said so and the table is unchanged; anything else is reset to First release cut: proposed, not confirmed.
    changes: "extends SPEC-001 BEH-08, BEH-09 and BEH-14"
    lands_in: "SKILL.md steps 6 and 7 (S9, S10), Output contract (S11); references/output-rules.md (O1 to O3); references/work-file.md (W1, W2); scripts/validate_brn.py (V1 to V3)"
```

### 3.1 Which rows an assumption stops (a judgment)

No field of a BRN links an assumption to an idea, and R1 forbids adding one. The link is a judgment the model
makes at step 5 and records in the `If wrong` cell, so that everything after it is mechanical and the validator
can check it.

The test: *an idea depends on an assumption when, if the assumption's statement were false, the idea as worded
would no longer relieve any problem it `addresses`.*

| | Assumption | Idea | Verdict |
|---|---|---|---|
| Depends | "We believe that patients read texts from the clinic the same day." | "Text a reminder two days before the visit." | Unread texts remind nobody: the idea relieves nothing |
| Does not depend | the same | "Phone patients who booked more than four weeks ahead." | The call works whether or not texts are read |

This can't be made mechanical (it weighs what two sentences mean). It is verified by VER-35's and VER-36's
`llm` graders and by VER-38.

### 3.2 `If wrong`

N is the number of cut rows that depend on the assumption; M is the number of cut rows. The cell is exactly one
of:

| When | Cell |
|---|---|
| N = M and M ≥ 1 | `Fatal: stops <IDs> (N of M in the cut table).` |
| 1 ≤ N < M | `Serious: stops <IDs> (N of M in the cut table).` |
| N = 0 | `Minor: stops no idea in the cut table (0 of M).` |

`<IDs>` is the depending rows' idea IDs in ID order, joined by a comma and a space. With one cut row, any
assumption that stops it is Fatal. With no cut row, every assumption is `Minor: … (0 of 0).`

The class is defined over the cut rows, which exist before the cut is proposed, never over the rows that say
`yes`: the ranking decides the cut, so it can't read it. README §4's sample row (C-07) shows the second form.

### 3.3 `Confidence`

A source *supports* an assumption when it states a fact about the people or the system the assumption names,
and that fact makes the statement more likely to be true. Only entries of the frontmatter `sources` list count
(C-09), by their kind:

| Cell | When |
|---|---|
| `high` | an entry of kind `data`, `document` or `ticket` supports it |
| `medium` | no such entry supports it, and an entry of kind `interview`, `url` or `note` does |
| `low` | no entry supports it |

| | Source | Assumption | Verdict |
|---|---|---|---|
| Supports | `data: reminder pilot export, October 2026` (8 of 10 reminder texts opened within a day) | "patients read texts from the clinic the same day" | A fact about these patients: `high` |
| Does not support | `url: an article on average text open rates` | the same | Says nothing about this clinic's patients: no support |

Whether a source supports is a judgment (verified as §3.1's). Which kinds a value needs is mechanical, and MV-05
checks it: `high` needs a `data`, `document` or `ticket` entry in `sources`, `medium` an `interview`, `url` or
`note` entry. So a BRN with `sources: []` has only `low`.

### 3.4 `Cheapest test`

Inputs: the assumption's ID and its `validation` value.

1. Take the value without its quotes, write `"` for each `\"`, write `/` for each `|`, and trim it.
2. When it is empty or starts with `[NEEDS CLARIFICATION:`, the cell is `[NEEDS CLARIFICATION: how to test
   ASM-NN]` with the assumption's ID, and the steps end.
3. The sentence is the text up to and including the first `.`, `?` or `!` that a space or the end of the text
   follows. With none, it is the whole text plus a full stop.
4. The kind is the first of these that matches the sentence, lowercased, a word matching only where no letter
   or digit touches it on either side:
   1. `Prototype`: prototype, prototypes, mock-up, mock-ups, mockup, mockups, pilot, pilots, trial, trials,
      beta, demo, demos, experiment, experiments, a/b, landing page, smoke test, fake door, build, launch.
   2. `Interview`: ask, asks, interview, interviews, survey, surveys, poll, polls, observe, shadow, talk to,
      speak to, questionnaire, focus group, workshop.
   3. `Data`: otherwise.
5. The cell is the kind, a colon, a space and the sentence.

The list is ordered by what the test needs: something built and put before people, then people's time, then
records that already exist. "Cheapest" is the cheapest way the `validation` names, not a cheaper way the
skill invents: the user wrote or accepted that validation. When the kind the list gives is not the test the
validation describes ("Read last year's survey results" gives `Interview`), the skill rewords the validation
so that its first sentence names the test, and derives the cell again; it never edits the cell alone. MV-07
checks the cell against this derivation.

### 3.5 Order

Risk points are impact times doubt: impact is Fatal 3, Serious 2, Minor 0; doubt is `low` 3, `medium` 2,
`high` 1. The rows are sorted by these keys, in order:

1. risk points, highest first;
2. impact, highest first;
3. doubt, highest first;
4. N, highest first;
5. assumption ID, lowest first.

The points give 9, 6, 6, 4, 3, 2, 0 for Fatal-low, Fatal-medium, Serious-low, Serious-medium, Fatal-high,
Serious-high and every Minor. Key 2 puts Fatal-medium before Serious-low. A Minor assumption is always below
one that stops an idea. `Rank` numbers the sorted rows 1 to n. MV-06 checks the order from the cells alone.

### 3.6 The cut

Inputs: the cut rows with each idea's `score`; the ranking; and which cut row needs which (a judgment, below).
The *counted* assumptions are those ranked 1 to 3 with N ≥ 1.

1. **Pick.** For each counted assumption, from rank 1 down: when one of the rows it stops is already `yes`,
   pick nothing. Otherwise the row it stops with the highest `score` becomes `yes`; a `null` score is lower than
   any number; on a tie the lowest ID wins.
2. **Fallback.** When step 1 made no row `yes` and M ≥ 1, the row with the highest `score` (lowest ID on a tie)
   becomes `yes`.
3. **Needs.** In passes: find every row that is not `yes` and that some `yes` idea needs; each becomes `yes`,
   naming the lowest-ID `yes` idea that needs it. Repeat until a pass adds nothing.
4. **The rest** is `no`.

Step 1 adds at most three ideas, one for each counted assumption. Step 3 has no limit.

The test for step 3: *an idea needs another when, as worded, it cannot be built or used unless the other
exists.*

| | Idea | Other idea | Verdict |
|---|---|---|---|
| Needs | "Let patients move a booking from the reminder link." | "Text a reminder two days before the visit." | No link without the text |
| Does not need | "Keep a waiting list for freed slots." | the same | Staff can fill it by phone |

A need for an active idea that is not a cut row can't be met by the cut: only a promoted idea can be in the
first release. The cut is left as it is and section 7 gains the bullet
`- [NEEDS CLARIFICATION: IDEA-NN is in the proposed first release and needs IDEA-MM, which is not promoted or
proposed for promotion. Promote IDEA-MM, or leave IDEA-NN out?]`

### 3.7 The `Why` cell

| Value | Sentence | Written by | What MV-10 checks |
|---|---|---|---|
| `yes` | `Tests ASM-NN, ranked R.` | step 1, for the assumption that picked the row | ASM-NN is ranked R, R ≤ 3, and stops this row; no other `yes` row names ASM-NN |
| `yes` | `Highest score; no assumption ranked 1 to 3 picks an idea.` | step 2 | No assumption ranked 1 to 3 stops a row; this row has the highest score, lowest ID on a tie |
| `yes` | `Needed by IDEA-NN, which is in the first release.` | step 3 | IDEA-NN is another row that says `yes` |
| `no` | `Tests ASM-NN, ranked R, which IDEA-MM already tests.` | step 4, when the row depends on a counted assumption: ASM-NN is the highest-ranked such, IDEA-MM the lowest-ID `yes` row it stops | ASM-NN is the highest-ranked assumption of ranks 1 to 3 that stops this row; IDEA-MM is another row, says `yes`, and ASM-NN stops it |
| `no` | `Tests no assumption ranked 1 to 3.` | step 4, otherwise | No assumption ranked 1 to 3 stops this row |
| `yes` | `Included by the user.` | BEH-32 items 4, 9 and 10: a row a typed change names, or a flagged `yes` row the user accepted | nothing |
| `no` | `Left out by the user.` | the same, for `no` | nothing |
| `yes` or `no` | `Needs review: no rule supports this value.` | §3.10's refresh, when no rule supports the row's value | nothing about the row; MV-12 rejects it under a confirmed status line |

The first five sentences are a proposal's. The two user sentences are reserved for choices the user actually
made. The last is the review flag. The two `no` sentences of step 4 are README §4's sample sentences; the first sample (`Tests ASM-01, ranked 1.`)
is step 1's.

### 3.8 Worked example

Four cut rows (M = 4), scores in brackets: IDEA-01 "Text a reminder two days before the visit" (3), IDEA-02 "Let
patients move a booking from the reminder link" (4), IDEA-04 "Keep a waiting list for freed slots" (2), IDEA-05
"Send a thank-you card after a kept visit" (1). IDEA-07 "Phone patients who booked more than four weeks ahead"
is proposed for parking, so it is no cut row. `sources` holds
`"url: booking system vendor's page on text messages"`.

| Assumption | Cut rows that depend on it | Support | `validation` |
|---|---|---|---|
| ASM-01 "patients read texts from the clinic the same day" | IDEA-01, IDEA-02 | none | "Ask ten patients at the desk whether they read texts from the clinic the same day." |
| ASM-02 "a patient who can't come will move the visit rather than skip it" | IDEA-02, IDEA-04 | none | "Count how many of last quarter's no-shows had phoned to cancel late, in the appointment book." |
| ASM-03 "the booking system can send texts" | IDEA-01, IDEA-02 | the `url` entry | "Run a one-week trial that sends test reminders from the booking system to staff phones. Check delivery." |
| ASM-04 "the front desk has 20 minutes a day for calls" | none (IDEA-07 is no cut row) | none | "[NEEDS CLARIFICATION: how to measure front-desk time]" |

Points: ASM-01 2 × 3 = 6; ASM-02 2 × 3 = 6; ASM-03 2 × 2 = 4; ASM-04 0 × 3 = 0. ASM-01 and ASM-02 tie on keys 1
to 4, so key 5 puts ASM-01 first.

```markdown
### Assumption risk ranking

| Rank | Assumption | If wrong | Confidence | Cheapest test |
|---|---|---|---|---|
| 1 | ASM-01 | Serious: stops IDEA-01, IDEA-02 (2 of 4 in the cut table). | low | Interview: Ask ten patients at the desk whether they read texts from the clinic the same day. |
| 2 | ASM-02 | Serious: stops IDEA-02, IDEA-04 (2 of 4 in the cut table). | low | Data: Count how many of last quarter's no-shows had phoned to cancel late, in the appointment book. |
| 3 | ASM-03 | Serious: stops IDEA-01, IDEA-02 (2 of 4 in the cut table). | medium | Prototype: Run a one-week trial that sends test reminders from the booking system to staff phones. |
| 4 | ASM-04 | Minor: stops no idea in the cut table (0 of 4). | low | [NEEDS CLARIFICATION: how to test ASM-04] |
```

The cut. Step 1: ASM-01 stops IDEA-01 (3) and IDEA-02 (4), none `yes` yet, so IDEA-02 is picked. ASM-02 stops
IDEA-02, already `yes`: nothing. ASM-03 the same. Step 2 doesn't apply. Step 3: IDEA-02 needs IDEA-01. Step 4:
IDEA-04 depends on ASM-02 (rank 2), whose lowest-ID `yes` row is IDEA-02; IDEA-05 depends on no counted
assumption.

```markdown
### First release cut

First release cut: proposed, not confirmed

| Idea | In first release | Why |
|---|---|---|
| IDEA-01 | yes | Needed by IDEA-02, which is in the first release. |
| IDEA-02 | yes | Tests ASM-01, ranked 1. |
| IDEA-04 | no | Tests ASM-02, ranked 2, which IDEA-02 already tests. |
| IDEA-05 | no | Tests no assumption ranked 1 to 3. |
```

Both tables are the output of the rule as a script (`harness.py`, §5.4), not hand-written. The staged example
BRN holds a second worked case, with a Fatal assumption that high confidence ranks last.

### 3.9 The answers, case by case

The form holds the dispositions question (Q1), the convergence question and the cut question (Q3). "All
promoted" means every row's idea has `disposition: promoted` once Q1's answer is written.

| Q1 | Rows after Q1 | Q3 | Cut written |
|---|---|---|---|
| Accept all as proposed | the same rows, all promoted | Accept as proposed | rows as proposed; `confirmed by <owner> on <today>` |
| Accept all as proposed | the same, all promoted | typed "add IDEA-04" | IDEA-04 `yes`, `Included by the user.`; confirmed |
| Accept all as proposed | the same, all promoted | Leave it proposed, dismissed, or no answer | rows as proposed; proposed |
| Leave them open | the same rows, all still open | Accept as proposed | rows as proposed; proposed. The reply names the ideas that are not promoted |
| typed "park IDEA-02" (IDEA-02 was a row) | IDEA-02 left the table | any | ranking and cut made again without IDEA-02; proposed. The reply says IDEA-02 left the table |
| typed "promote IDEA-06" (it was proposed for parking) | IDEA-06 entered the table | any | made again with IDEA-06; proposed. The reply says IDEA-06 entered |
| typed "IDEA-01 promoted" only (other rows stay open) | the same rows, not all promoted | Accept as proposed | rows as proposed; proposed. The reply names the open ideas |
| any | the same, all promoted | typed "IDEA-09 in" (no such row) | nothing changes; proposed (ERR-10) |
| any, in a run that extends a brownfield BRN, with the fourth answer confirming an update of this BRN's own ASM-01 | the same | any | ASM-01 is no longer open: ranking and cut made again without it; proposed. The reply says ASM-01 left the ranking |

Typed text is read for two things (a judgment, R9; verified by VER-38):

| | Text | Reading |
|---|---|---|
| A change | "add IDEA-04"; "IDEA-02 out"; "only IDEA-01" | The named row takes the value and its user sentence; "only IDEA-01" makes IDEA-01 `yes` and every other row `no`, each named by the change. The other rows' reasons are refreshed (§3.10) |
| No change | "IDEA-04 looks risky"; "why is IDEA-05 out?" | Nothing is written; the cut stays proposed (ERR-10) |
| An acceptance | "yes"; "accept"; "fine as proposed" | As `Accept as proposed` |

### 3.10 Refreshing the reasons, and the review flag

After typed changes the values stand: the user answered about them. A changed row can leave another row's
sentence untrue, so every row that is not the user's has its `Why` derived again. Inputs: the ranking, the
rows with their values, which rows are the user's (their `Why` is a user sentence), each idea's `score`, and
§3.6's needs. In order:

1. **Tests.** For each counted assumption, from rank 1 down: when a row it stops is a user row that says
   `yes`, or got a `Tests` sentence earlier in this pass, nothing. Otherwise, among the rows it stops that say
   `yes` and are not the user's, the one with the highest `score` (a `null` score lowest, lowest ID on a tie)
   gets `Tests ASM-NN, ranked R.`
2. **Each `yes` row still without a reason.** When a `yes` idea needs it: `Needed by IDEA-NN, which is in the
   first release.`, naming the lowest-ID such idea. Otherwise, when no assumption is counted and the row has
   the highest `score` of all rows (lowest ID on a tie): `Highest score; no assumption ranked 1 to 3 picks an
   idea.` Otherwise it is flagged.
3. **Each `no` row still without a reason.** When a `yes` idea needs it, it is flagged. Otherwise, when it
   depends on a counted assumption, take the highest-ranked one: when a row that assumption stops says `yes`,
   `Tests ASM-NN, ranked R, which IDEA-MM already tests.`, naming the lowest-ID such row; when none does, it
   is flagged. Otherwise `Tests no assumption ranked 1 to 3.`

A flagged row keeps its value and its `Why` is exactly `Needs review: no rule supports this value.` The flag is
a cell of the existing table, so no field is added (R1). A refresh of a table nobody changed gives that table
back: every sentence §3.6 wrote is the one this derivation writes.

In §3.8's table, the typed change "IDEA-02 out" gives:

```markdown
First release cut: proposed, not confirmed

| Idea | In first release | Why |
|---|---|---|
| IDEA-01 | yes | Tests ASM-01, ranked 1. |
| IDEA-02 | no | Left out by the user. |
| IDEA-04 | no | Needs review: no rule supports this value. |
| IDEA-05 | no | Tests no assumption ranked 1 to 3. |
```

IDEA-01's reason was `Needed by IDEA-02, which is in the first release.`; ASM-01 stops IDEA-01 and no user row
that says `yes`, so step 1 gives it `Tests ASM-01, ranked 1.` IDEA-04 depends on ASM-02 (rank 2), and neither
row ASM-02 stops says `yes` now, so nothing supports its `no`. The third question is asked once more with
"Needs review: IDEA-04 (no)."; `Accept as proposed` makes that row `Left out by the user.`, the next refresh
flags nothing, and the cut is confirmed. The typed change "add IDEA-04" flags nothing: IDEA-01 keeps `Needed by
IDEA-02, …` and IDEA-02 keeps `Tests ASM-01, ranked 1.`, so the cut is confirmed at once (§3.9's second row).

### 3.11 Extending a BRN: the user's rows kept

*The same eligible ideas* means: the set of idea IDs of the cut rows, listed at the extension's step 5 (the
active ideas that are promoted, or open and proposed for promotion), equals the set of idea IDs in the rows of
the cut table the BRN holds. *An explicit choice* is a row of that table whose `Why` is `Included by the user.`
or `Left out by the user.`; nothing else in a BRN records one (R1).

With the same eligible ideas, the user's rows are kept, value and sentence, and every other row is proposed
again by §3.6 with these differences:

- a user row that says `yes` counts as already `yes`, so an assumption that stops it picks nothing;
- steps 1 and 2 pick only among rows that are not the user's; when every row an assumption stops is a user row
  that says `no`, it picks nothing;
- step 2 applies only when no assumption is counted;
- steps 3 and 4 never change a user row; a user row that says `no` while a `yes` idea needs it is named in the
  reply.

A *stale reason* is a `Why` cell of a row that is not the user's and that differs from what this gives: it is
replaced, and so is the row's value when the rule now proposes the other one. A row the BRN holds as flagged is
not the user's, so it is proposed again. No row is flagged by an extension.

With different eligible ideas, every row is proposed again by §3.6 and no row is kept: the user chose among
other ideas. The reply and the Change Log row name each row the user had set, with its value, so the choice can
be stated again.

Either way, the new table is compared with the BRN's, cell by cell. Equal: the status line is kept. Different in
any cell: `First release cut: proposed, not confirmed`, and the third question asks about the new table.

For example, §3.9's second row left a confirmed cut with IDEA-04 `yes`, `Included by the user.` The BRN is
extended after ASM-01 was validated; the cut rows are the same four ideas. The ranking is now ASM-02, ASM-03,
ASM-04. ASM-02 stops IDEA-04, the user's `yes`, so it picks nothing; ASM-03 picks IDEA-02 (score 4):

```markdown
First release cut: proposed, not confirmed

| Idea | In first release | Why |
|---|---|---|
| IDEA-01 | yes | Needed by IDEA-02, which is in the first release. |
| IDEA-02 | yes | Tests ASM-03, ranked 2. |
| IDEA-04 | yes | Included by the user. |
| IDEA-05 | no | Tests no assumption ranked 1 to 3. |
```

IDEA-04's row is kept; IDEA-02's reason changed, so the table returns to proposed and is asked about.

## 4. Errors and edge cases

```yaml items
errors:
  - id: ERR-10
    status: proposed
    condition: "The typed answer to 'Confirm the first release cut?' can't be applied in full: it names an idea that has no row in the cut table, or it states neither an acceptance nor a change"
    handling: "Write only the changes that name a row. When nothing readable names a row, change no row and keep 'First release cut: proposed, not confirmed'. Never show the options again for the same question. Say in the reply which part was not applied, and that only a promoted idea, or one proposed for promotion, can be in the first release"
    user_result: "The cut with the readable changes applied, or still proposed; the part of the answer that was not applied, named"
    changes: new
    lands_in: "references/mvp-path.md, 'Confirm the cut', Typed changes"
```

Edge cases the behaviour items already settle:

| Case | Result | Item |
|---|---|---|
| No open active assumption | The ranking is the line `None.`; the cut is step 2's fallback: the highest-scoring row `yes` | BEH-30 item 7, BEH-31 |
| No cut row | The cut is the line `No idea is promoted or proposed for promotion.`; no third question; section 8 is `- None.`; every ranked assumption is `Minor: … (0 of 0).` | BEH-31 item 3, BEH-32 item 1 |
| Fewer than three ranked assumptions | The counted assumptions are the ones there are; the `no` sentence still reads "ranked 1 to 3" | §3.6 |
| Every `score` is `null` | Ties on the lowest ID | §3.6 step 1 |
| A `validation` that is a NEEDS CLARIFICATION marker | `[NEEDS CLARIFICATION: how to test ASM-NN]`; the only cell of either table that may hold a marker | §3.4 |
| A pipe character in a `validation` | Written `/` in the cell | §3.4 |
| A deprecated idea or assumption | No row in either table | BEH-30 item 1 |
| The user sets every row to `no` | Written as typed and confirmed; section 8 is `- None.` | BEH-32 item 4 |
| `owner` is a NEEDS CLARIFICATION marker | The skill asks for the owner's name; without it the cut stays proposed | BEH-32 item 5 |
| The user stops before step 5's proposals (ERR-02's draft) | No cut row; ranking with M = 0 | BEH-33 item 3 |
| An earlier-shape BRN is extended | Neither table is written; no MV check applies | BEH-33 items 1 and 4 |
| An extension with the same eligible ideas | The user's rows are kept; the others are proposed again; a table that changed in any cell is proposed, and asked about | BEH-32 item 8, §3.11 |
| An extension with different eligible ideas | Every row is proposed again, none kept; proposed, and asked about; the reply names the rows the user had set | BEH-32 item 8, §3.11 |
| A typed change leaves another row's reason untrue | The reason is derived again; a row no rule supports is flagged, the cut stays proposed and the question is asked once more | BEH-32 items 4 and 10, §3.10 |
| A row is flagged and no question can be asked | The flag stays under the proposed status line; the reply names the row | BEH-32 item 10 |
| The user leaves out an idea that a `yes` idea needs | The user's row stands; the reply names it | §3.10 |
| A framework switch at step 5 redoes the evaluation (framework-catalog.md) | Both tables are made again from the new proposals before the form is asked again | BEH-30 item 1, BEH-31 item 1 |

## 5. Verification

### 5.1 Items

```yaml items
verifications:
  - id: VER-35
    status: proposed
    covers:
      - BEH-31
      - BEH-32
      - BEH-33
    level: eval
    obligation: "With nobody to confirm, the BRN holds '### First release cut' with the status line 'First release cut: proposed, not confirmed', never a confirmed one; every row's Why cell is one of the five proposal sentences; at least one row says yes; no disposition is decided; section 8 lists exactly the yes rows; and each yes row's reason is true of the ranking."
    case: proposes-first-release-cut
    prompt: |-
      I repair commuters' bikes from a van that parks at a different stop each weekday morning. People
      phone me to book while I'm working, and a lot of them give up before we agree a slot. I want to
      offer some kind of booking service; nothing like it exists yet. Brainstorm what it could be. Don't
      ask me any questions, just work through it and write it up.
    scaffold: none
    graders:
      - name: brn-exists
        type: file_exists
        path: docs/specs/brainstorm/BRN-001.md
        exists: true
      - name: cut-is-proposed
        type: regex
        target: "{source: file, path: docs/specs/brainstorm/BRN-001.md}"
        match: contains
        flags: m
        pattern: |-
          ^### First release cut[ \t]*\n\n?First release cut: proposed, not confirmed[ \t]*$
      - name: cut-not-confirmed
        type: regex
        target: "{source: file, path: docs/specs/brainstorm/BRN-001.md}"
        match: not_contains
        pattern: |-
          First release cut: confirmed
      - name: cut-has-a-yes-row
        type: regex
        target: "{source: file, path: docs/specs/brainstorm/BRN-001.md}"
        match: contains
        flags: m
        pattern: |-
          ^\| IDEA-\d{2} \| yes \| (?:Tests ASM-\d{2}, ranked [1-3]\.|Highest score; no assumption ranked 1 to 3 picks an idea\.|Needed by IDEA-\d{2}, which is in the first release\.) \|[ \t]*$
      - name: cut-rows-use-fixed-sentences
        type: regex
        target: "{source: file, path: docs/specs/brainstorm/BRN-001.md}"
        match: not_contains
        flags: m
        pattern: |-
          ^\| IDEA-\d{2} \| (?!yes \| (?:Tests ASM-\d{2}, ranked [1-3]\.|Highest score; no assumption ranked 1 to 3 picks an idea\.|Needed by IDEA-\d{2}, which is in the first release\.) \|[ \t]*$)(?!no \| (?:Tests no assumption ranked 1 to 3\.|Tests ASM-\d{2}, ranked [1-3], which IDEA-\d{2} already tests\.) \|[ \t]*$)
      - name: no-decided-disposition
        type: regex
        target: "{source: file, path: docs/specs/brainstorm/BRN-001.md}"
        match: not_contains
        pattern: |-
          disposition:[ \t]*\"?(?:promoted|parked|rejected)
      - name: signals-match-the-cut
        type: llm
        focus: "{source: file, path: docs/specs/brainstorm/BRN-001.md}"
        question: |-
          The file is a brainstorm document. Under the heading "### First release cut" is a table with the
          columns Idea, In first release, Why. Section 8, "Candidate success signals", is a bullet list.
          Judge only this claim: section 8 has exactly one bullet starting with the ID of each idea whose
          row says "yes", in the same order, and no bullet for any other idea.
          PASS if the claim holds. FAIL otherwise, and name the idea ID that is missing or extra.
      - name: cut-follows-the-ranking
        type: llm
        focus: "{source: file, path: docs/specs/brainstorm/BRN-001.md}"
        question: |-
          The file is a brainstorm document. Under "### Assumption risk ranking" each row names an
          assumption (ASM-NN), its rank and, in "If wrong", the ideas it stops. Under "### First release
          cut" each row names an idea, yes or no, and a reason. Judge only these two claims:
          1. Every row whose reason reads "Tests ASM-NN, ranked R." names an assumption that has rank R
             in the ranking table and lists that idea in its "If wrong" cell.
          2. For each such row, the idea would in fact stop working if that assumption (read its
             statement in the assumptions block) were false.
          PASS if both hold for every such row, or if no row has that reason. FAIL otherwise, quoting the
          row and saying which claim it breaks.
  - id: VER-36
    status: proposed
    covers:
      - BEH-30
    level: eval
    obligation: "The BRN holds '### Assumption risk ranking' in section 7, directly after the assumptions item block, with the fixed header row and a first row ranked 1; every row has the fixed If wrong, Confidence and Cheapest test forms; no Minor row stands above a row that stops an idea; and the ideas each row lists, and its confidence, are sound."
    case: ranks-assumptions-by-risk
    prompt: |-
      Our community garden has 40 plots and a waiting list of 65 households. The list is a paper sheet
      in the shed, and last year's sign-up sheet shows that 11 plots were never planted. We want some
      way to manage the plots and the waiting list; nothing exists yet. Brainstorm it. Go ahead without
      asking me anything and write up the brainstorm.
    scaffold: none
    graders:
      - name: brn-exists
        type: file_exists
        path: docs/specs/brainstorm/BRN-001.md
        exists: true
      - name: ranking-follows-the-assumptions-block
        type: regex
        target: "{source: file, path: docs/specs/brainstorm/BRN-001.md}"
        match: contains
        flags: m
        pattern: |-
          ^## 7\. Assumptions and open questions\n[\s\S]*?^```[ \t]*\n+### Assumption risk ranking[ \t]*\n+\| Rank \| Assumption \| If wrong \| Confidence \| Cheapest test \|[ \t]*\n\|(?:[ \t]*:?-+:?[ \t]*\|){5}[ \t]*\n\| 1 \| ASM-\d{2} \|
      - name: ranking-rows-well-formed
        type: regex
        target: "{source: file, path: docs/specs/brainstorm/BRN-001.md}"
        match: not_contains
        flags: m
        pattern: |-
          ^\| \d+ \| ASM-\d{2} \| (?!(?:(?:Fatal|Serious): stops IDEA-\d{2}(?:, IDEA-\d{2})* \(\d+ of \d+ in the cut table\)\.|Minor: stops no idea in the cut table \(0 of \d+\)\.) \| (?:high|medium|low) \| (?:(?:Data|Prototype|Interview): [^|\n]+|\[NEEDS CLARIFICATION: how to test ASM-\d{2}\]) \|[ \t]*$)
      - name: minor-never-above-a-stopper
        type: regex
        target: "{source: file, path: docs/specs/brainstorm/BRN-001.md}"
        match: not_contains
        flags: m
        pattern: |-
          ^\| \d+ \| ASM-\d{2} \| Minor: [^\n]*\n(?:\|[^\n]*\n)*?\| \d+ \| ASM-\d{2} \| (?:Fatal|Serious):
      - name: ranking-is-sound
        type: llm
        focus: "{source: file, path: docs/specs/brainstorm/BRN-001.md}"
        question: |-
          The file is a brainstorm document about managing a community garden's plots and waiting list.
          Under "### Assumption risk ranking" each row names an assumption (ASM-NN, defined in the
          assumptions block above it), the ideas it stops ("If wrong") and a confidence. Judge only these
          two claims:
          1. For each row that lists ideas, each listed idea (read it in the ideas block) would stop
             working if the assumption's statement were false.
          2. No row says confidence "high" unless the frontmatter "sources" list has an entry starting
             "data:", "document:" or "ticket:".
          PASS if both hold. FAIL otherwise, quoting the row and saying which claim it breaks.
  - id: VER-37
    status: proposed
    covers:
      - BEH-33
    level: unit
    obligation: "src/tests/brainstorm/test_validate_brn.py (T2): the staged example passes; its unconfirmed form passes; rows set by the user pass; after a typed change that leaves an idea out, a flagged row passes under the proposed status line, the stale rule sentence in its place is rejected (MV-10), and a confirmed cut that holds a flagged row is rejected (MV-12); the fallback and the no-row forms pass; an earlier-shape BRN with a broken cut table passes (the gate); and one wrong sample for each of MV-01 to MV-12 is rejected with a line ending in that check's number, each with PyYAML, with the system's packages only and with python3 -S."
  - id: VER-38
    status: proposed
    covers:
      - BEH-30
      - BEH-31
      - BEH-32
      - ERR-10
    level: manual
    obligation: |-
      Live, with a user answering, on a copy of the plugin loaded with claude --plugin-dir (docs/runbooks/brainstorm-manual-test.md), each run's BRN printing OK under the validator:
      (a) step 5's form shows 'Confirm the first release cut?' third, header 'Step 5', the options 'Accept as proposed' and 'Leave it proposed' with BEH-32's descriptions, neither marked recommended, each preview showing the status line and the cut table; Accept all as proposed, Converged and Accept as proposed give 'First release cut: confirmed by <the owner> on <today>' and section 8 lists the yes ideas;
      (b) Leave them open with Accept as proposed gives the proposed status line and a reply naming the ideas that are not promoted;
      (c) a typed disposition change that parks a row's idea, with Accept as proposed, gives a table made again without that idea, the proposed status line, and a reply saying the idea left the table;
      (d) Accept all as proposed with the typed cut answer 'add IDEA-NN' (a no row) gives that row yes with 'Included by the user.', no other user sentence anywhere, and a confirmed status line; the typed answer 'IDEA-NN in' for an idea with no row changes nothing, shows no second menu, and the reply says why (ERR-10);
      (e) a run whose request says to proceed without questions (Proceed chosen) writes the cut proposed; the message 'I confirm the first release cut' then gets step 5's form again, and only after Accept as proposed is the BRN edited in place, validated and reported;
      (f) extending (d)'s BRN with one more idea proposed for promotion (different eligible ideas) gives a table proposed again in every row, the proposed status line, the third question, and a reply and Change Log row that say the earlier cut was replaced and name the row the user had set; extending (d)'s BRN after one assumption's state was changed, with the same eligible ideas, keeps the 'Included by the user.' row, proposes the others again, and returns the table to proposed only when a cell changed;
      (g) in (a)'s BRN, a reader checks three ranking rows against §3.1 and §3.3 (the listed ideas depend on the assumption; the confidence has its source) and the cut against §3.6 by hand;
      (h) in a run that extends a brownfield new-shape BRN, Accept as proposed for the cut together with Accept all as proposed for an update of that BRN's own assumption gives a ranking without that assumption, a cut made again, the proposed status line, and a reply saying the assumption left the ranking;
      (i) with a cut in which one yes idea is 'Needed by' another, the typed cut answer that leaves the other out gives the needed row a rule sentence that holds, or 'Needs review: no rule supports this value.' with the proposed status line and the third question asked once more, naming the flagged row; Accept as proposed then gives that row the user sentence and a confirmed cut; Leave it proposed leaves the flag; no row other than the one named and the one accepted holds a user sentence.
      Recorded in SPEC-001 §9.
```

### 5.2 The validator's checks

Every check applies only to a new-shape BRN (README, "The gate"), reads only lines outside fenced blocks (and
the parsed item blocks), and reports `line N: <message> (MV-NN)`. V2 is the implementation; this table is what
it must do. A table is: the header row, a `|---|` row, then rows, each starting and ending with `|`; cells are
split on `|` and trimmed.

| Check | Rule |
|---|---|
| MV-01 | Exactly one line `### Assumption risk ranking` in the document, in section 7, after the section's last fence line and before its first line starting `- ` |
| MV-02 | Under it, up to the first bullet or heading: only the line `None.`, or a table whose header cells are `Rank`, `Assumption`, `If wrong`, `Confidence`, `Cheapest test`, with at least one row and five cells in each row |
| MV-03 | The `Assumption` cells are exactly the IDs of the active assumptions whose `state` is `open`, each once (none when the line is `None.`); `Rank` is 1, 2, 3 and so on down the rows |
| MV-04 | `If wrong` matches one of §3.2's forms; the listed IDs are rows of the cut table, in ID order, each once; N is their number; M is the cut table's row count; the class is the one N and M give |
| MV-05 | `Confidence` is `high`, `medium` or `low`; `high` needs a `sources` entry starting `data: `, `document: ` or `ticket: `; `medium` one starting `interview: `, `url: ` or `note: ` |
| MV-06 | The rows are in §3.5's order (checked when MV-02 to MV-05 found no fault in the cells it reads) |
| MV-07 | `Cheapest test` equals §3.4's derivation from that assumption's `validation` |
| MV-08 | Exactly one line `### First release cut` in the document, in section 6; the first non-empty line under it is one of the two status lines |
| MV-09 | After the status line, up to the next heading: only the line `No idea is promoted or proposed for promotion.`, or a table with the header cells `Idea`, `In first release`, `Why` and three cells in each row. Each row's idea is an active idea whose `disposition` is `promoted` or `open`; rows are in ID order, each idea once; the second cell is `yes` or `no`; every active idea with `disposition: promoted` has a row |
| MV-10 | Each `Why` cell is one of §3.7's eight sentences, with the value its sentence belongs to (the flag goes with either value), and what it says holds (§3.7's last column) |
| MV-11 | When no row's `Why` is a user sentence or the flag: every assumption ranked 1 to 3 that stops a row has a `yes` row among the rows it stops; and a table with a row has a `yes` row |
| MV-12 | A confirmed status line names the frontmatter `owner` (which is not a NEEDS CLARIFICATION marker) and a real calendar date from `created` to `updated`; the table has a row; every row's idea has `disposition: promoted`; no row holds the flag |

The messages, each after `line N: `. Words in angle brackets are filled in; `<what>` is `assumption risk ranking`
(then the check is MV-02) or `first release cut` (MV-09):

```text
section 7 must hold exactly one '### Assumption risk ranking' heading, after its item block and before its bullets, and no other section may hold one (MV-01)
<what>: the table must start with the header row '| <the header cells> |' (MV-02 or MV-09)
<what>: a |---| row and at least one row must follow the header row (MV-02 or MV-09)
<what>: each row has exactly <5 or 3> cells, with no '|' inside a cell, and nothing else follows the table (MV-02 or MV-09)
assumption risk ranking: one row for each active assumption whose state is open, and no other row (<IDs, or: none, so the line 'None.' replaces the table>) (MV-03)
assumption risk ranking: Rank counts 1, 2, 3 and so on; row <n> says '<cell>' (MV-03)
ASM-NN: 'If wrong' must read 'Fatal: stops IDEA-NN, IDEA-NN (N of M in the cut table).', 'Serious: stops IDEA-NN (N of M in the cut table).' or 'Minor: stops no idea in the cut table (0 of M).' (MV-04)
ASM-NN: 'If wrong' lists rows of the cut table in ID order and counts them against its <M> row(s): Fatal when it lists every row, Serious when it lists some, Minor when it lists none (MV-04)
ASM-NN: Confidence must be high, medium or low (MV-05)
ASM-NN: Confidence <high or medium> needs a sources entry of kind <data, document or ticket | interview, url or note> (MV-05)
assumption risk ranking: rows out of order; the order is <IDs> (MV-06)
ASM-NN: 'Cheapest test' must be '<the derived cell>' (MV-07)
section 6 must hold exactly one '### First release cut' heading, and no other section may hold one (MV-08)
the first line under '### First release cut' must be 'First release cut: proposed, not confirmed' or 'First release cut: confirmed by <owner> on YYYY-MM-DD' (MV-08)
first release cut: 'IDEA-NN' is not an active idea whose disposition is promoted or open (MV-09)
first release cut: rows are in idea ID order, each idea once; IDEA-NN is out of place (MV-09)
first release cut: 'In first release' for IDEA-NN must be yes or no (MV-09)
first release cut: the promoted idea IDEA-NN has no row (MV-09)
first release cut: the Why cell of IDEA-NN is not one of the fixed sentences for '<yes or no>', or it does not match the ranking or the other rows (MV-10)
first release cut: no 'yes' row tests ASM-NN, ranked <R>; one of <IDs> must be in the first release (MV-11)
first release cut: a cut that the user did not change has a 'yes' row (MV-11)
first release cut: a confirmed cut holds no row that says 'Needs review: no rule supports this value.'; flagged: <IDs> (MV-12)
first release cut: a confirmed cut names the frontmatter owner (never a NEEDS CLARIFICATION marker) and a real date from created to updated (MV-12)
first release cut: confirmed only when the table has a row and every row's idea is promoted; not promoted: <IDs, or: there is no row> (MV-12)
```

MV-10 and MV-11 run only when both tables parsed without fault, MV-12 only when the cut did, so one
broken table gives one message, not a cascade. The validator can't know what the user confirmed (MV-12 checks
only what a confirmed cut requires); step 7's read-back does that (BEH-33 item 5).

That section 8 lists exactly the cut's `yes` rows is intake-and-evidence.md's IV-06, not a check of this series.

### 5.3 Regex graders, tested

Each pattern above was read back from this file with PyYAML and run in node (v24) against a good sample (the
staged example in its unconfirmed form) and a wrong one. `check_graders.mjs` printed:

```text
proposes-first-release-cut/cut-is-proposed (contains): good sample passes, wrong sample fails
proposes-first-release-cut/cut-not-confirmed (not_contains): good sample passes, wrong sample fails
proposes-first-release-cut/cut-has-a-yes-row (contains): good sample passes, wrong sample fails
proposes-first-release-cut/cut-rows-use-fixed-sentences (not_contains): good sample passes, wrong sample fails
proposes-first-release-cut/no-decided-disposition (not_contains): good sample passes, wrong sample fails
ranks-assumptions-by-risk/ranking-follows-the-assumptions-block (contains): good sample passes, wrong sample fails
ranks-assumptions-by-risk/ranking-rows-well-formed (not_contains): good sample passes, wrong sample fails
ranks-assumptions-by-risk/minor-never-above-a-stopper (not_contains): good sample passes, wrong sample fails
8 regex graders behave as intended
```

### 5.4 What was run for this document

Scripts are in the session's scratch folder, `fable/fable-mvp-handoff/`; none is part of the build.

| Check | Result |
|---|---|
| The staged example under version 11's validator, `python3` and `python3 -S` | `OK` and `OK` |
| The staged example, its unconfirmed form and its no-row form under version 11's validator with V1 and V2 applied, `python3` and `python3 -S` | `OK` each |
| One wrong sample for each of MV-01 to MV-12 | exit 1 with a line ending in that check's number, the same lines with `-S` |
| The test file with T1 and T2 applied, on a scratch copy of the tree with V1 and V2 applied | `Ran 171 tests`, `OK` (57 cases, three ways) |
| The rule as a script (`harness.py`: `rank()`, `cut()`) on §3.8's inputs and the staged example's | its output is the tables printed in §3.8 and in the example |
| §3.10's refresh and §3.11's rule as a script (`rules2.py`) on §3.8's table: the typed changes "IDEA-02 out" and "add IDEA-04", the acceptance of the flagged row, and the extension after ASM-01 was validated; and on the staged example with "IDEA-01 out" | its output is the tables printed in §3.10 and §3.11 and the rows of T2's `mvp_idea_01_left_out`; a refresh of an unchanged table returns it unchanged |
| Every old text of §2.1 to §2.5 against version 11 (`check_edits.py`) | each found exactly once, ignoring line breaks (S7 and O3 are checked against brownfield-iteration.md's new texts instead) |
| The same old texts against the three files with the three earlier documents' edits applied (`after_siblings.py`) | S2 to S13, O1 to O3, W1 and W2 each found exactly once; S1 is no edit, because brownfield-iteration.md's B-S1 already made the change |
| The validator with intake-and-evidence.md's A-V1 and A-V2, brownfield-iteration.md's B-V1 and B-V2, then V1 and V2 applied (`combined.py`), on the staged greenfield example and on both BRNs of the staged brownfield example, `python3` and `python3 -S` | `OK` for all three, both ways: the three documents' checks agree on the three examples |
| The whole test file as the fourth commit leaves it (`full_tree.py`): the validator and the test file with A-V1, A-V2, A-T1 to A-T3, B-V1, B-V2, B-T1, B-T2, then V1, V2, T1, T2; the staged template and both staged examples | `Ran 354 tests`, `OK` (118 cases, three ways) |
| SKILL.md with all four documents' edits applied in build order (`skill_lines.py`) | 371 lines |
| Every `yaml items` block here | parses with PyYAML; every item has R4's keys |

## 6. Staged files

| Staged | Destination | Notes |
|---|---|---|
| `staged/skills/brainstorm/references/mvp-path.md` | `src/claude/DevForgeAI/skills/brainstorm/references/mvp-path.md` (new) | Imperative, for Claude; opens with a contents list; links to `intake.md` (intake-and-evidence.md) for the form of a section 8 bullet |
| `staged/examples/brainstorm-greenfield-mvp/BRN-001.md` | `src/staging/examples/brainstorm-greenfield-mvp/BRN-001.md` (new) | Greenfield, new shape, converged, the cut confirmed; 3 problems, 7 ideas, 4 assumptions; T1 reads it |
| `staged/examples/brainstorm-greenfield-mvp/README.md` | the same folder (new) | What the example shows, and how its tables follow from the rule |

## 7. Decisions and open questions

**Decisions made here, with reasons.**

1. *The ranking is made before the cut and never reads it.* README says the ranking decides the cut. So `If
   wrong` counts the cut rows (promoted or proposed for promotion), not the `yes` rows, in three fixed forms.
2. *The links are recorded in cells.* Which ideas an assumption stops is written in `If wrong`, which idea
   needs which in a `Why` sentence. They are the only judgments (§3.1, §3.3's support, §3.6's need); the order,
   the cut and every other cell follow mechanically and the validator checks them.
3. *Fatal means every cut row.* It is the only class a count can define without a second judgment about which
   idea matters most. With one cut row any dependency is Fatal, which is right: that idea is the product.
4. *Risk points, not class first.* An assumption that would stop everything but is backed by the project's own
   data is less urgent to test than one that stops two ideas on no evidence. Impact times doubt orders them
   that way; Minor has impact 0, so it never outranks an assumption that stops an idea.
5. *Confidence comes from `sources` kinds.* The project's own records (`data`, `document`, `ticket`) count
   above reports and outside pages (`interview`, `url`, `note`). It makes `high` and `medium` checkable
   (MV-05) and ties confidence to C-09.
6. *`Cheapest test` is derived, word lists and all.* Two builders, and the validator, get the same cell. The
   cost is a wrong kind for an oddly worded validation; the remedy is rewording the validation, which is the
   field a reader trusts anyway.
7. *Ranks 1 to 3 count, one idea each.* README's sample sentence fixes "1 to 3". One idea for each keeps the
   first release as small as the top risks allow; an assumption already covered by a `yes` row adds nothing.
8. *`score` breaks the choice among an assumption's rows*, because it is the one evaluation field every
   framework fills (R1). A `null` score is lowest; ties go to the lowest ID.
9. *Needs are followed without a limit, and only among cut rows.* A first release missing what its idea needs
   can't ship. A need for an idea that isn't promoted is the user's to settle, so it becomes an open question.
10. *A cut is confirmed only over promoted ideas* (Bryan's rule for dispositions, extended: R3). Accepting the
    cut while the dispositions stay open confirms nothing; the reply says why.
11. *A table that changed after the first answer is not the table the user answered about.* It is made again
    and stays proposed. This costs a second confirmation in the rare case and never records a decision nobody
    made.
12. *Typed changes are the user's rows.* They get their own two sentences, so a reader, the validator and the
    PRD skill can tell a rule's row from a decision.
13. *No option of the third question is recommended.* The table is already the recommendation; marking
    `Accept as proposed` would nudge a decision R3 keeps the user's (SPEC-002 BEH-21 does the same).
14. *An extension keeps the user's rows when the eligible ideas are the same* (§3.11; the owner's decision
    below). Rows the rule made are proposed again rather than kept, because nothing in them is a choice; the
    table returns to proposed whenever a cell changed, so nothing unseen stays confirmed.
15. *Check numbers end each message* (`(MV-07)`), so a test, a grader or a reader can name the rule that
    failed. The other documents' series (IV, BV) are free to do the same.
16. *The unit tests read the staged example* from `src/staging/examples/`, so the example can't drift from the
    validator.
17. *ADR-003 is not touched.* It makes `disposition` and MoSCoW `priority` the document contract and asks for
    a mapping before another prioritisation method. The cut adds no field and sets no priority: it is prose a
    PRD may read as a suggestion (prd-handoff-contract.md).
18. *After a typed change the other rows' reasons are derived again, and a row no rule supports is flagged*
    (§3.10; the owner's decision below). The value stays, because the user answered about it; the flag says
    that nobody has given a reason for it; the cut stays proposed until the user has. This replaces an earlier
    draft, which gave such a row a user sentence.
19. *A confirmed update of this BRN's own assumption remakes both tables.* The assumption is no longer open,
    so MV-03 rejects its row and a cut row that tests it has lost its reason. As with a changed list of cut
    rows, the user answered about another table, so the new one stays proposed.
20. *The flag is an eighth fixed sentence, valid with either value and only under the proposed status line.* It
    needs no field (R1), a regex grader and MV-12 can see it, and a confirmed cut can never carry a row nobody
    justified.
21. *A flagged row the user accepts becomes the user's.* The re-asked question names the row and its value, so
    accepting is a choice the user actually made about that row; before that, it is not.
22. *The question is asked again once.* A second flagged result stays proposed and is named in the reply, so a
    run can't loop on the form.
23. *A later confirmation of a BRN that holds a flagged row asks the naming question.* Otherwise an acceptance
    could never confirm that cut: a flagged row bars the confirmed status line, and only an answer to a question
    that names the row makes it the user's.

**Decided by Bryan on 2026-11-19** (session fa59a935-ed2e-4502-b6c4-93bb6d847546), on the questions this section
left open. His words: "Enforce the drafted Cheapest test rule and use the top three assumptions for the cut. Change two defaults. First, when extending a BRN with the same eligible ideas, preserve my explicit yes and no choices. Refresh stale reasons and return a changed table to proposed status for confirmation. Second, if I remove IDEA-02 and another row's reason was "Needed by IDEA-02," recompute that row's reason. If no rule justifies its current value, flag the row for review. Reserve "Included by the user" and "Left out by the user" for choices I actually made."

| Question | Decision | Where |
|---|---|---|
| Should the `Cheapest test` kind be enforced by the validator? | Yes: "Enforce the drafted Cheapest test rule" | §3.4, MV-07 (unchanged) |
| How many top-ranked assumptions count for the cut? | Three: "use the top three assumptions for the cut" | §3.6 (unchanged) |
| When a BRN with a cut the user changed is extended with the same eligible ideas, are the user's rows kept? | Yes: "preserve my explicit yes and no choices. Refresh stale reasons and return a changed table to proposed status for confirmation" | BEH-32 item 8, §3.11 (changed) |
| After a typed change, what happens to a row whose reason no longer holds? | "recompute that row's reason. If no rule justifies its current value, flag the row for review. Reserve "Included by the user" and "Left out by the user" for choices I actually made" | BEH-32 items 4, 9 and 10, §3.10, MV-10, MV-12 (changed) |

**Open, for Bryan.** None.
