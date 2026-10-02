# Runbook: SKL-003 v6 — paid evaluation and manual checks

Covers what the build session can't run for the architecture skill SKL-003 v6 (approved by Bryan on 2026-10-01), which
implements SPEC-003 v5, on branch `feat/spec-003-v5-architecture` (worktree
`.claude/worktrees/spec-003-v5`):
- section 1: the paid `claude plugin eval` runs, cheapest first, on Opus only (Bryan, 2026-10-01);
- sections 2 and 3: the manual items Bryan chose (decision D6): VER-20, VER-12 (a), (j) and (k), and
  VER-19 again, since SPEC-003 v5 changed it.

Every item stays **NOT_RUN** until someone runs it. Record each result in section 4: **pass**,
**fail** (with what happened), or **not run** (with why). A failure stays a failure: if a grader
turns out to be wrong, show it with controls first, and keep the old result on record.

Paste each command on its own. None starts with `!`, and none uses a `\` continuation or a heredoc.

## 1. Paid evaluation (plain terminal, not inside Claude)

Run from the worktree root, on a committed, clean tree:

```bash
cd ~/Projects/DevForgeAI/.claude/worktrees/spec-003-v5
P=src/claude/DevForgeAI
A="--allow-tools Write Edit Bash --scaffold --judge-model sonnet --threshold 0.8"
C="reuse-needs-prd-link reuse-names-uncited no-prd-exists"
C="$C changed-platform-blocks-reuse changed-platform-reopens"
N="--runs 1 --ablation none"
```

Before **every** run, bind a new results folder with `record_revision.sh`, which refuses a dirty tree
or an existing folder.

**1a. The five new cases on v6, one run each, no baseline** (about $2–3). Compare with the same run
on v5 (section 4):

```bash
R=tmp/eval-results/arch-v6-newcases-$(date +%Y%m%dT%H%M%S)
bash src/tests/prd/record_revision.sh $R architecture
for c in $C; do claude plugin eval $P --case $c $N $A --output-dir $R/$c; done
```

**1b. VER-20 by hand** (section 3, B1) before the full suite: it exercises the main change.

**1c. The whole suite, one run with the baseline** (21 cases, about $15):

```bash
R=tmp/eval-results/arch-v6-1run-$(date +%Y%m%dT%H%M%S)
bash src/tests/prd/record_revision.sh $R architecture
claude plugin eval $P --tag architecture --runs 1 $A -j 4 --output-dir $R
```

**1d. Three runs with the baseline** (about $55, 30 minutes at `-j 4`): the same as 1c without
`--runs 1`, into a new `arch-v6-3run-…` folder. Afterwards, check `cases[].arms.with[].error` in
`$R/aggregate-result.json` and look for a `not granted` line before trusting any score.

## 2. Setup for the manual checks (once per shell)

```bash
WT=~/Projects/DevForgeAI/.claude/worktrees/spec-003-v5
T=/tmp/arch-v6-test; M="$WT/src/tests/architecture/manual"
rm -rf "$T" && mkdir -p "$T" && cp -r "$WT/src/claude/DevForgeAI" "$T/plugin"
ws() { rm -rf "$T/ws" && mkdir "$T/ws" && cd "$T/ws"; }
fresh() { ws && bash "$T/plugin/evals/$1/scaffold.sh"; }
manual() { ws && bash "$M/$1/scaffold.sh"; }
base() { git init -q && git add -A && git -c user.name=t -c user.email=t@t commit -qm x; }
```

`fresh architecture/<case>` seeds an empty project in `$T/ws` with an eval case's fixtures; `manual
<name>` seeds a manual-only fixture. Run `base` right after, so `git diff` shows what the run changed.
Then start Claude from `$T/ws` with the copied plugin:

```bash
claude --plugin-dir "$T/plugin"
```

Give your name if asked who decides. Your `~/.claude/CLAUDE.md` still loads; remove any papercut
entries the deliberate failures below cause.

## 3. Manual checks

### B1. Deciding an open question later (VER-20; BEH-04, BEH-07, BEH-08, BEH-09, BEH-11)

`manual decide-open-question`, then `base`: the approved ARCH-001 links PRD-001 v1, the current
version; DEC-01 (identity provider) is resolved by the accepted ADR-001 (Auth0); DEC-02 (session
revocation) is open. Say, naming no outcome:

> /devforgeai:architecture PRD-001

Pick an option for DEC-02, answer *Decide later* to any other question, and confirm amend if asked.

**Expect:**
- It recommends amending ARCH-001 because DEC-02 is open, not reuse.
- A new ADR (ADR-002) with `status: accepted` and `approved_by` you; DEC-02 has `state: resolved`
  and `resolved_by: [ADR-002]`.
- ARCH-001: `version: 2`, `status: in-review` with `approved_by: ""` and `approved_on: null`,
  `outcome: amend`. `git diff docs/specs/arch/ARCH-001.md` shows no change inside an existing item
  except DEC-02's `state` and `resolved_by`, and the new Change Log row logs that transition.
- The report lists FR-001 and NFR-001 as ready (DEC-01 and DEC-02 are both resolved), unless a DEC
  this run added cites them.

**Second copy:** `manual decide-deferred-question`, then `base`. DEC-02's deferral is recorded as the
proposed ADR-002. Do the same. **Expect** as above, but the new ADR is ADR-003 with
`supersedes: [ADR-002]`, and `git diff docs/specs/adr/ADR-002.md` shows only `status: superseded`,
`superseded_by: ADR-003` and one Status history row.

### B2. Decisions accepted one by one (VER-12 (a))

`fresh architecture/creates-arch`, then `base`. Say:

> /devforgeai:architecture PRD-001

Pick an option for the identity-provider question, answer *Decide later* for session revocation,
and confirm `create` when asked.

**Expect:** each question is presented with options and trade-offs, the recommended one first. One
accepted ADR, for the identity provider only; the revocation DEC stays open with `resolved_by: []`
and no ADR; `outcome: create`; FR-001 is reported blocked by the revocation DEC. Confirming `create`
resolved nothing else.

### B3. Amending keeps old links and adds new ones at the new version (VER-12 (j))

`manual amend-links`, then `base`: the draft ARCH-001's links all cite PRD-001 v2; PRD-001 v3 adds a
NEEDS ADR marker about the roster. Say:

> /devforgeai:architecture PRD-001 — amend ARCH-001; I confirm the amend outcome.

Answer *Decide later* to every question.

**Expect:** links on existing items still cite `version: 2`; the frontmatter PRD link and every link
this run adds (the new roster DEC citing FR-003) cite `version: 3`; validation passes with no ERR-05;
ARCH-001 is `version: 2` and stays `draft`.

### B4. A supersession that passes validation (VER-12 (k))

`manual decide-open-question`, then `base`. Say:

> /devforgeai:architecture PRD-001 — amend ARCH-001; I confirm the amend outcome. We're replacing
> Auth0 for sign-in.

Approve superseding ADR-001, pick a provider for DEC-01, and pick an option for DEC-02 too.

**Expect:** `git diff docs/specs/adr/ADR-001.md` shows only `status: superseded`,
`superseded_by: ADR-NNN` and one Status history row; the new ADR is accepted with
`supersedes: [ADR-001]`; DEC-01's `resolved_by` changes from `[ADR-001]` to the new ADR, logged in the
Change Log; ADR-001 is recorded as a new EVD with `classification: context`; validation passes; the
report lists FR-001 as ready.

### B5. Failed supersession rolls back, EVD deprecated (VER-19, changed in SPEC-003 v5)

`manual failed-supersession`, then `base`, and follow section A3 of
`docs/runbooks/prd-v2-architecture-v4-checks.md`. **Expect** everything A3 lists, plus: the EVD item
the run added for ADR-001 is still in ARCH-001 with `status: deprecated` and its other fields as
written, no EVD item was deleted, and the ERR-05 Change Log row says the EVD was deprecated.

## 4. Results

| Item | Result | Date | Notes |
|---|---|---|---|
| Eval: 5 new cases on v5 (`cd892e0`), 1 run, no baseline | 2 of 5 at 1.00: VER-21 1.00, VER-22 0.33, VER-23 1.00, VER-24 0.80, VER-25 0.57; $2.40 | 2026-10-01 | `tmp/eval-results/arch-v5-newcases-20261001T133751/`, written in the `arch-v5-check` worktree and kept in the main checkout's `tmp/eval-results/`. VER-21 and VER-23 already pass on v5 (regression guards). VER-22: v5 refused the confirmed reuse (FR-003 "adds questions"). VER-24: v5 refused reuse but reported DEC-01 still resolved and proposed a new identity CMP (judge FAIL 3 of 3). VER-25: DEC-01 not reopened |
| 1a Eval: 5 new cases on v6, 1 run, no baseline | pass: 5 of 5 at 1.00; $2.21 | 2026-10-01 | `tmp/eval-results/arch-v6-newcases-20261001T134913/`, `dcbb024`. VER-22 recorded the reuse and marked FR-003 "(no architectural question cites it)", saying DEC-01, DEC-02 and NFR-002 probably apply and to amend if they should be checked |
| 1c Eval: architecture, 1 run with baseline | pass: 21 of 21 at 1.00, mean Δ +0.61; $17.81, 668 s | 2026-10-01 | `tmp/eval-results/arch-v6-1run-20261001T142042/`, `f663361`, Claude Code 2.1.287; no errors, no `not granted`. Δ 0.00 only for `ignores-unrelated-request` and `reuse-review-idempotent`, where the baseline also does nothing |
| 1d Eval: architecture, 3 runs with baseline | pass: 21 of 21 at 1.00 in every run, mean Δ +0.63; $53.04 for the runs kept | 2026-10-01 | Two folders, both bound to `0c93f9a` and plugin digest `51f246e6…`: `tmp/eval-results/arch-v6-3run-20261001T143253/` (13 cases complete; the usage limit stopped the other 8, whose runs all errored and are discarded) and `tmp/eval-results/arch-v6-3run-rest-20261001T163700/` (those 8 rerun with `--tag architecture --case`). `policy-bad-date`'s baseline lost 2 of 3 runs to the limit, so its Δ +0.50 rests on one baseline run; its plugin arm is complete |
| B1 VER-20 deciding later (both copies) | pass, with a spec-wording note | 2026-10-01 | Copy 1, session `797948c0`: recommended amend; ADR-002 accepted by Bryan; only DEC-02's `state`/`resolved_by` changed; row `DEC-02 open → resolved: ADR-002 accepted (decided by Bryan)`; v2, in-review, approval cleared. Copy 2, session `1228a170`: ADR-003 `supersedes: [ADR-002]`; ADR-002's diff only status, superseded_by and one history row; EVD-03 records ADR-002 as context. Note: each run added and deferred a new shared question (DEC-04 hosting; DEC-03 roles) that also cites FR-001 or NFR-001, so not every requirement "only DEC-02 blocked" reports ready. VER-20 lacks VER-05's "unless the amendment adds a DEC that cites them" clause: backlog for SPEC-003's next version |
| B2 VER-12 (a) | pass (also covers VER-12 (l)) | 2026-10-01 | Bryan decided DEC-02 to DEC-05 and deferred DEC-01 and DEC-06: four accepted ADRs (ADR-001..004, `approved_by: "Priya Nair"`, the decider named), one per explicit pick; DEC-01 and DEC-06 open with `resolved_by: []` and no ADR; `outcome: create` confirmed after the decisions, accepting nothing else. The uncertain kinds of CMP-02 and CMP-03 were asked about and left open as `[NEEDS CLARIFICATION: kinds of CMP-NN]`; check 1 found a malformed marker, repair 1 fixed it |
| B3 VER-12 (j) | pass | 2026-10-01 | All three questions deferred. The 5 links on existing items still cite v2 and no existing item changed; the frontmatter PRD link and every added link (DEC-03 → FR-003; new CMP-04 → NFR-002, NFR-003) cite v3; new EVD-02 for PRD-001 v3; check 1 passed, no ERR-05; ARCH-001 v2, still draft, `outcome: amend` |
| B4 VER-12 (k) | pass | 2026-10-01 | Session `dff4dde7`. The request's "replacing Auth0" was not taken as approval; Bryan approved superseding ADR-001 in an answer. ADR-001's diff: only status, superseded_by and one history row; ADR-002 accepted with `supersedes: [ADR-001]`; row `DEC-01 resolved_by ADR-001 → ADR-002 (supersession approved by …)`; ADR-001 recorded as context EVD-03; DEC-02 decided too (ADR-003); check 1 passed; FR-001 reported ready |
| B5 VER-19 with the EVD deprecated | pass | 2026-10-01 | Session `ffaafe1f`. Before writing, the skill named CMP-01's invalid status, said it couldn't fix it in an amendment, and offered the owner a fix; Bryan chose to proceed. Check 1 failed on CMP-01 (unrepairable). ADR-001 byte-identical to the fixture; ADR-002 (replacement) and ADR-003 proposed with approval and `supersedes` cleared, "Intended to supersede ADR-001 … not in force" and "Restored to proposed" rows; DEC-01..03 open with `resolved_by: []`; ARCH-001 in-review, approval cleared, no existing item changed; EVD-04 kept with `status: deprecated`, other fields as written, no EVD deleted; audit row names the rollback and the deprecation; failure report with no readiness. Observation: the read-back used `sed -n` and `cat -A`, outside the allowed command list (self-reported; read-only) |
