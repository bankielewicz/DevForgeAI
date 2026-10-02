# Runbook: epic skill VER-13 — manual checks

Covers SPEC-004 v3 VER-13, the epic skill's manual verification item, for SKL-004 v3 as merged in PR #47
(`3cf7033`) and deployed in plugin 0.8.0. VER-13 has never been run, for any version. Its clause (d) is
automated since SPEC-004 v2 (VER-14 and VER-19), so it isn't repeated here.

Every item stays **NOT_RUN** until someone runs it. Record each result in section 4: **pass**, **fail** (with
what happened), or **not run** (with why). A failure stays a failure: if an expectation turns out to be wrong,
show why, and keep the result on record.

Paste each command on its own. None starts with `!`, and none uses a `\` continuation or a heredoc.

## 1. Setup (once per shell)

```bash
R=~/Projects/DevForgeAI
T=/tmp/epic-v3-test
rm -rf "$T" && mkdir -p "$T" && cp -r "$R/src/claude/DevForgeAI" "$T/plugin"
fresh() { rm -rf "$T/ws" && mkdir "$T/ws" && cd "$T/ws" && bash "$T/plugin/evals/epic/$1/scaffold.sh"; }
manual() { rm -rf "$T/ws" && mkdir "$T/ws" && cd "$T/ws" && bash "$R/src/tests/epic/manual/$1/scaffold.sh"; }
```

`fresh <case>` makes an empty project in `$T/ws` and seeds it with that epic eval case's fixtures;
`manual <name>` does the same with a manual-only fixture from `src/tests/epic/manual/`, which
`python3 src/tests/epic/make_manual.py` generates from the eval generator's shared fixture. The project
sits outside the repository, so the session doesn't load the repository's `CLAUDE.md` or the deployed
plugin. Start Claude from `$T/ws` with the copied plugin:

```bash
claude --plugin-dir "$T/plugin"
```

Check that `/devforgeai:epic` appears in the completion list. To restart between checks: `/exit`, run
`fresh …` or `manual …` again, then the same `claude` line. Your `~/.claude/CLAUDE.md` still loads.

**The shared fixture** (SPEC-004 §9): PRD-001 v2 ("Spring launch", approved), ARCH-001 citing it at v2,
ADR-001 to ADR-003 and POL-001. Its eligible requirements are FR-002, FR-003, FR-004, FR-012 and NFR-001.

## 2. Interactive checks

### C-a. A changed grouping is followed (VER-13 (a); BEH-07)

`fresh selects-ready-current` (the shared fixture). Say:

> /devforgeai:epic PRD-001

When it proposes a grouping and asks, change it: "Put FR-003 (the coordinator's roster) in its own epic;
everything else together."

**Expect:**
- Before your answer: a proposal showing each epic's working title, priority and requirements, and a question.
  Nothing is written under `docs/specs/epic/` until you answer.
- After: two epics. The one with FR-002, FR-004, FR-012 and NFR-001 is `priority: must` and is EPIC-001. The one
  with FR-003 is `priority: should` and is EPIC-002 (Must first). NFR-001 may also be attached to EPIC-002 with
  a `partial:` note.
- No epic carries the unconfirmed-grouping marker, since you confirmed the grouping.
- The reply opens with the report, gives each left-out row, and ends with the Next step naming EPIC-001 and
  EPIC-002.

### C-b. An unknown PRD ID (VER-13 (b); BEH-01, ERR-01)

`fresh selects-ready-current`. Say:

> /devforgeai:epic PRD-009

**Expect:** it lists the PRDs that exist (PRD-001, its title "Volunteer shift sign-up for the Riverside Food
Bank" and status approved) and writes nothing: `ls docs/specs/epic` fails.

### C-c. Two active ARCHs (VER-13 (c); ERR-04)

`manual two-archs` (ARCH-001 and ARCH-002 both approved, both citing PRD-001 v2). Say:

> /devforgeai:epic PRD-001

**Expect:** it lists ARCH-001 and ARCH-002, each with its `system` and the version of its PRD link (2), and
asks which to use. Nothing is written until you answer. Then answer "ARCH-002" and say "one epic for everything
eligible": EPIC-001's `informed_by` link is `{id: ARCH-002, relation: informed_by, version: 1, hash: null}`.

### C-e. Stopping before confirming (VER-13 (e); ERR-07)

`fresh selects-ready-current`. Say `/devforgeai:epic PRD-001`; when it proposes a grouping and asks, answer:
"Stop here, I'll come back to this."

**Expect:** nothing under `docs/specs/epic/`, and the reply says how to resume: run `/devforgeai:epic PRD-001`
again.

### C-g. This repository's own PRD-001, which has no ARCH (VER-13 (g); ERR-02)

Copy the repository's own specs into a fresh project (this repository has no `docs/specs/arch/`):

```bash
rm -rf "$T/ws" && mkdir -p "$T/ws/docs/specs" && cd "$T/ws"
cp -r "$R/docs/specs/prd" "$R/docs/specs/adr" docs/specs/
```

Start Claude as in section 1 and say `/devforgeai:epic PRD-001`.

**Expect:** nothing written; the reply says readiness comes from the architecture description, that no ARCH
cites PRD-001, and tells you to run `/devforgeai:architecture PRD-001` first.

### C-i. The review loop after a priority-only PRD change (VER-13 (i); BEH-03, ERR-03)

`manual prd-priority-change` (PRD-001 v3: only FR-004's priority changed, could to should; ARCH-001 still
cites PRD-001 v2). This ARCH-001 passes the architecture skill's own self-checks, unlike the eval cases' one:
DEC-03 (reminders) and DEC-05 (monthly hours) are open rather than resolved by the superseded ADR-002 or the
missing ADR-004, and open DEC-08 and DEC-09 answer the import and payment-provider markers. Otherwise the review
record in step 2 would fail validation and clear ARCH-001's approval. The eligible set is unchanged. Record the
starting state:

```bash
git init -q && git add -A && git -c user.name=t -c user.email=t@t commit -qm fixtures
```

1. Say `/devforgeai:epic PRD-001`. **Expect:** ERR-03. Nothing written; the reply names both versions
   (ARCH-001 reviewed against PRD-001 v2; the PRD is v3) and tells you to review the architecture with
   `/devforgeai:architecture PRD-001`.
2. Say `/devforgeai:architecture PRD-001` and, when it asks, confirm **reuse** of ARCH-001 (no architectural
   change). **Expect:** `git diff docs/specs/arch/ARCH-001.md` shows exactly: the frontmatter PRD link's version
   2 → 3, `outcome` from `create` to `reuse`, and one new Change Log row ("Reviewed against PRD-001 v3: reuse
   confirmed …", ending with a `Policy resolution:` line). ARCH-001's `version`, `status: approved`, approval
   fields and every item are unchanged.
3. Say `/devforgeai:epic PRD-001` and "one epic for everything eligible". **Expect:** EPIC-001 refines
   FR-002, FR-003, FR-004, FR-012 and NFR-001 at PRD-001 version 3, and links ARCH-001 at version 1.
4. Commit (`git add -A && git -c user.name=t -c user.email=t@t commit -qm epic`), then say
   `/devforgeai:architecture PRD-001` again and confirm reuse. **Expect:** `git status --short` shows no
   change to ARCH-001: a second review against the same PRD version writes nothing.

### C-j. A superseded ARCH and its replacement (VER-13 (j); BEH-03, ERR-02 to ERR-04)

`manual superseded-arch` (ARCH-001 `status: superseded`, `superseded_by: ARCH-002`; ARCH-002 approved,
`supersedes: [ARCH-001]`, citing PRD-001 v2). Say:

> /devforgeai:epic PRD-001 — one epic for everything eligible. Proceed without questions.

**Expect:** no question about which ARCH. EPIC-001 is written and links `{id: ARCH-002, relation: informed_by,
version: 1, hash: null}`; the report's first line names ARCH-002.

### C-k. A changed mandated platform (VER-13 (k); BEH-04, check 3)

Automated since SPEC-004 version 4 by VER-20 (eval case `epic-mandate-changed-blocked`): a changed platform
now makes FR-012 **blocked** by DEC-07, not unknown, so this check is not run by hand. The `manual
platform-changed` fixture stays for anyone who wants to see it interactively; expect the FR-012 row
`blocked by DEC-07 (POL-001#SET-01 now mandates "Network-hosted mail service (HTTPS API) for transactional
email"; ARCH-001 recorded "Regional network mail relay (SMTP) for transactional email")`, with the next action
`/devforgeai:architecture PRD-001`.

## 3. Reading checks (no Claude session)

From the repository root, on the merged source.

### C-f. SKILL.md within NFR-001's limits; versions mirror (VER-13 (f); QR-01, QR-02)

```bash
S=src/claude/DevForgeAI/skills/epic
awk 'NR==1,/^---$/{next} /^---$/{f=1;next} f' $S/SKILL.md | wc -l
grep -m1 '^description:' $S/SKILL.md | wc -c
grep 'devforgeai-version' $S/SKILL.md; grep '^version:' $S/provenance.yaml
```

**Expect:** the body is at most 500 lines (PRD-001 NFR-001); the description line is at most 1,036 characters
(1,024 plus the `description: ` prefix and the newline); `devforgeai-version` is `"3"` and provenance `version: 3`.

### C-h. The three-attempt limit and the ERR-06 report (VER-13 (h); BEH-10, ERR-06)

```bash
grep -n -i 'three attempts' $S/SKILL.md $S/references/output-rules.md
grep -n 'ERR-06' $S/SKILL.md $S/references/output-rules.md
```

**Expect:** SKILL.md step 8 says to fix and re-check "at most three attempts" and, if errors remain, to stop and
end with a validation-failure report naming each file and its unresolved errors (ERR-06); output-rules.md's
"When validation still fails (ERR-06)" section says the same. ERR-06 can't be forced without a checker, so this
is a reading check, not an exercise (SPEC-004 VER-13 (h)).

## 4. Results

| Item | Result | Date | Notes |
|---|---|---|---|
| C-a VER-13 (a) changed grouping followed | NOT_RUN | | |
| C-b VER-13 (b) unknown PRD ID | NOT_RUN | | |
| C-c VER-13 (c) two active ARCHs | NOT_RUN | | |
| VER-13 (d) nothing eligible / everything covered | automated | | VER-19 and VER-14; SPEC-004 §9 (v3-c) |
| C-e VER-13 (e) stop before confirming | NOT_RUN | | |
| C-f VER-13 (f) NFR-001 limits, version mirror | NOT_RUN | | |
| C-g VER-13 (g) this repository's PRD-001, no ARCH | NOT_RUN | | |
| C-h VER-13 (h) three attempts, ERR-06 (reading) | NOT_RUN | | |
| C-i VER-13 (i) review loop | NOT_RUN | | |
| C-j VER-13 (j) superseded ARCH | NOT_RUN | | |
| C-k VER-13 (k) changed mandated platform | AUTOMATED (VER-20, SPEC-004 v4) | | |
