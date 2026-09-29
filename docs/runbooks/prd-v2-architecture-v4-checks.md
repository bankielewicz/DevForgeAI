# Runbook: SKL-002 v2 and SKL-003 v4 — paid evaluation and manual checks

Covers what the build session couldn't run for the prd skill (SKL-002 v2, SPEC-002 v2) and the
architecture skill (SKL-003 v4, SPEC-003 v4), both built on branch `feat/prd-spec-002-v2`:
- section 1: the paid `claude plugin eval` runs;
- section 2: prd VER-11, VER-12 and VER-23, and the Claude-only session check (verification plan §4);
- section 3: architecture VER-12 (f) and (i), and VER-19 (the failed-supersession regression case).

SKL-003 v3 (commit `9bdb87a`) is superseded by v4. A result bound to `9bdb87a` stays on record, but it
doesn't qualify v4.

Every item stays **NOT_RUN** until someone runs it. Record each result in section 4: **pass**,
**fail** (with what happened), or **not run** (with why). A failure stays a failure: if a grader
turns out to be wrong, show it with controls first, and keep the old result on record.

Paste each command on its own. None starts with `!`, and none uses a `\` continuation or a heredoc.

## 1. Paid evaluation (plain terminal, not inside Claude)

Run from the worktree root, on a committed, clean tree:

```bash
cd ~/Projects/DevForgeAI/.claude/worktrees/prd-spec-002-v2
P=src/claude/DevForgeAI
A="--allow-tools Write Edit Bash --scaffold --judge-model sonnet --threshold 0.8 -j 4"
```

Before **every** run, bind a new results folder to the commit, the plugin digest and the case files.
`record_revision.sh` refuses a dirty tree or an existing folder, so a rerun never replaces an earlier
result:

```bash
R=tmp/eval-results/prd-v2-3run-$(date +%Y%m%dT%H%M%S)
bash src/tests/prd/record_revision.sh $R prd
claude plugin eval $P --tag prd $A --output-dir $R
```

For the architecture suite, use `R=tmp/eval-results/arch-v4-3run-…`, `record_revision.sh $R
architecture` and `--tag architecture`. Afterwards, check `cases[].arms.with[].error` in
`$R/aggregate-result.json` and look for a `not granted` line before trusting any score.

| Run | Cases | Command change | Estimate |
|---|---|---|---|
| Pilot (optional) | `stated-choice-honored`, `failed-extension-stays-in-review`, `policy-bad-authors` (prd) and `failed-amendment-stays-in-review` (architecture) | `--case <name> --runs 1 --ablation none`, one case per run | about $3 |
| 1 run with baseline (optional) | prd 29, architecture 16 | add `--runs 1` | about $12 and $13 |
| **3 runs with baseline (required)** | **prd 29 × 3 runs × 2 arms; architecture 16 × 3 × 2** | as above | **about $60 and $40** |

The required total is about $100; with the pilot and the 1-run passes, about $128. The prd estimate
scales the last 20-case run ($41.51); the architecture one, the last 14-case run ($35.09).

- **Both skills have a case named `policy-bad-date`**, as SPEC-002 VER-28 and SPEC-003 VER-17 name
  them. `--tag` keeps the suites apart; `--case policy-bad-date` may select both.
- The threshold is 0.8 per case over 3 runs, against the no-plugin baseline.
- Grader checks already run offline (no cost): `src/tests/prd/check_graders.py` and
  `src/tests/architecture/check_graders.py`, with scripted good and bad results.

## 2. prd manual checks (SPEC-002 VER-11, VER-12, VER-23)

### 2.0 Setup (once per shell)

```bash
WT=~/Projects/DevForgeAI/.claude/worktrees/prd-spec-002-v2
T=/tmp/prd-v2-test
rm -rf "$T" && mkdir -p "$T" && cp -r "$WT/src/claude/DevForgeAI" "$T/plugin"
X="$WT/src/staging/examples/policy-two-orgs"
fresh() { rm -rf "$T/ws" && mkdir "$T/ws" && cd "$T/ws" && bash "$T/plugin/evals/$1/scaffold.sh"; }
manual() { rm -rf "$T/ws" && mkdir "$T/ws" && cd "$T/ws" && bash "$WT/src/tests/architecture/manual/$1/scaffold.sh"; }
```

`fresh <skill>/<case>` makes an empty project in `$T/ws` and seeds it with that eval case's fixtures;
`manual <name>` does the same with a manual-only fixture from `src/tests/architecture/manual/`.
It sits outside the repository, so the session doesn't load the project's `CLAUDE.md`, `AGENTS.md` or
the deployed plugin. Then start Claude from `$T/ws` with the copied plugin:

```bash
claude --plugin-dir "$T/plugin"
```

Check that `/devforgeai:prd` appears in the completion list. To restart between tests: `/exit`,
run `fresh …` again, then the same `claude` line. Your `~/.claude/CLAUDE.md` still loads; remove any
papercut entries the deliberate failures below cause.

### M1. Interactive interview with a partial answer (VER-11; BEH-03, BEH-05)

`fresh prd/writes-prd-from-brn` (a converged food bank BRN-001 whose section 3 names the users). Say:

> /devforgeai:prd BRN-001 — It's our MVP, piloted with our own coordinator and volunteers on real
> volunteer data, so the operating context is internal.

Answer: FR for sign-up *must now*, FR for reminders *should now*; constraint *none*; security
"volunteers sign in with a one-time code"; privacy, partly: "phone numbers are visible only to the
coordinator; I don't know yet how long we keep data"; anything else *no*; metrics as you like.

**Expect:**
- No question asks the stage, the operating context or who the users are.
- Every question call has at most 4 questions with 2–4 options; count the calls, gates included:
  at most 8.
- The quality questions cover constraint, security and privacy (the internal floor) plus one
  "anything else" question, and no other required category.
- The partial privacy answer becomes an NFR for phone numbers, plus
  `[NEEDS CLARIFICATION: privacy requirements for internal]` in section 12 for the rest.
- Constraint *none* is one sentence in section 7's prose, with no constraint NFR and no constraint marker.
- The reply's block has `Validation: passed at check N of at most 4`, and the resolution line has
  `interview.max_calls=8 (default)`.

### M2. Stopping mid-interview (VER-11; ERR-07)

`fresh prd/writes-prd-from-brn`, same request. After the first question call, say "Stop here, I have
to go." **Expect:** it asks whether to save a draft PRD. Yes: `PRD-001.md` with `status: draft`,
every undecided field `null`. Repeat, answering no: no file.

### M3. Extending an approved PRD (VER-12; BEH-09, BEH-10, BEH-14)

`fresh prd/extension-keeps-review-history` (an approved, reviewed PRD-001, its BRN-001, and BRN-002
for the same initiative), then record the starting state:

```bash
git init -q && git add -A && git -c user.name=t -c user.email=t@t commit -qm fixtures
```

Say `/devforgeai:prd BRN-002`. It should recommend extending PRD-001; choose that, and answer the new
requirement's question (*should now*).

**Expect:**
- `git diff docs/specs/prd/PRD-001.md`: `version: 2`, a new `updated`, `status: in-review`,
  `approved_by: ""`, `approved_on: null`, this session in `generated_by`, and additions only
  (a BRN-002 link, FR-003 and so on, one Change Log row). Every existing item is unchanged, and so
  are `authors`, `reviewed_by: ["Marcus Lee"]` and the three earlier Change Log rows.
- The new Change Log row says `This revision has not been reviewed.`
- The reply warns that epics citing PRD-001 are suspect, and says the revision hasn't been reviewed.
- `git diff --stat docs/specs/brainstorm` prints nothing.

Then, in the same workspace, say `/devforgeai:prd` with no ID. **Expect (ERR-04):** every promoted
idea is already cited, and nothing is written.

### M4. A shared constraint is cited, not copied (VER-12; BEH-15)

`fresh prd/extension-keeps-review-history`. Say:

> /devforgeai:prd BRN-002 — write a new PRD for it. It runs on the same hosted services as PRD-001.

**Expect:** it writes `PRD-002.md` without asking new-versus-extend (the choice was stated, and the
reply says so). Its frontmatter has
`{id: PRD-001, item: NFR-001, relation: constrains, version: 1, hash: null}`, the PRD says what the
constraint applies to, and it has no constraint NFR copying NFR-001's statement.

### M5. Unknown and malformed BRNs, a failed extension, SKILL.md size (VER-12; ERR-01, ERR-05, ERR-06, QR-01)

- `fresh prd/extension-keeps-review-history`, then `/devforgeai:prd BRN-009`. **Expect:** it lists
  BRN-001 and BRN-002 and writes nothing.
- Break BRN-002's ideas block, then `/devforgeai:prd BRN-002`:

  ```bash
  sed -i 's/^    disposition: promoted/  disposition promoted/' docs/specs/brainstorm/BRN-002.md
  ```

  **Expect:** it names the failing block (`ideas`) and the BRN path, stops, writes nothing, and
  doesn't repair the BRN.
- `fresh prd/failed-extension-stays-in-review`, then `/devforgeai:prd BRN-002` and choose to extend
  PRD-001. **Expect (ERR-06):** at most four checks, then PRD-001 is `in-review` with the approval
  cleared, FR-001 is unchanged, and the reply is a validation-failure report that doesn't send you to
  `/devforgeai:architecture`.
- `wc -l "$T/plugin/skills/prd/SKILL.md"` prints at most 500.

### M6. Local preferences (VER-23; BEH-18)

`fresh prd/writes-prd-from-brn`, then:

```bash
L=.claude/devforgeai.local.md && mkdir -p .claude
printf -- '---\ndevforgeai_local: 1\ninterview.max_calls: 5\n---\n' > $L
```

Run M1's request and answer normally. **Expect:** at most 5 question calls, and the resolution line
has `interview.max_calls=5 (local)`.

Then replace the file with an organizational-policy key and an out-of-range value, and repeat:

```bash
printf -- '---\ndevforgeai_local: 1\ninterview.max_calls: 50\n' > $L
printf -- 'architecture.mandated_platforms: x\n---\n' >> $L
```

**Expect:** both entries are ignored and reported
(`ignored .claude/devforgeai.local.md <key> (<reason>)`), the budget stays 8, and the run continues.

### M7. Policy rules (VER-23; ERR-08, SV-01, SV-02, SV-06)

Each starts with `fresh prd/writes-prd-from-brn && mkdir -p docs/specs/policy`, then says
`/devforgeai:prd BRN-001. Proceed without questions.` You can also run the script yourself first:
`python3 "$T/plugin/skills/prd/scripts/validate_policy.py" docs/specs/policy`.

| Check | Seed | Expect |
|---|---|---|
| SV-01 | `sed 's/id: SET-02/id: SET-01/' "$X/org-a/POL-001.md" > docs/specs/policy/POL-001.md` | Stops before any question, naming `POL-001.md`, `SET-01` and `SV-01`; no PRD |
| SV-02 | `cp "$X/org-a/POL-001.md" docs/specs/policy/` then `sed 's/POL-001/POL-002/' "$X/org-b/POL-001.md" > docs/specs/policy/POL-002.md` | Stops, naming both files and `SV-02`; no PRD |
| SV-06 | `sed 's/status: approved/status: draft/' "$X/org-b/POL-001.md" > docs/specs/policy/POL-001.md` | Writes the PRD with the defaults; the resolution line has `ignored docs/specs/policy/POL-001.md (status draft)` |
| Calendar check | `sed 's/updated: 2026-09-01/updated: 2026-13-45/' "$X/org-a/POL-001.md" > docs/specs/policy/POL-001.md` | Stops, naming `POL-001.md`, the field `updated` and the rule `calendar check` (not `schema`); no PRD |
| Can't run | SV-06's seed but keep `status: approved` (`cp "$X/org-b/POL-001.md" docs/specs/policy/`), and start Claude with jsonschema hidden (below) | Stops: policy validation couldn't run, quoting `jsonschema is not installed`; no PRD |

To hide jsonschema for the last row:

```bash
mkdir -p "$T/shim" && echo 'raise ImportError("hidden", name="jsonschema")' > "$T/shim/jsonschema.py"
PYTHONPATH="$T/shim" claude --plugin-dir "$T/plugin"
```

### M8. Session ID (Claude only; BEH-10)

After M1, compare `generated_by.session` in `PRD-001.md` with the session's transcript name:

```bash
grep '^  session:' docs/specs/prd/PRD-001.md
ls -t ~/.claude/projects/-tmp-prd-v2-test-ws/*.jsonl | head -1
```

**Expect:** the same UUID, and the same ID in the Change Log row's author.

## 3. Architecture manual checks (SPEC-003 VER-12 (f) and (i))

### A1. Byte-identity of the shared policy files (VER-12 (f))

From the worktree root: `python3 -B src/tests/prd/test_shared_files.py`. **Expect:** OK (5 tests).
After deploying, also:

```bash
D=.claude/skills/devforgeai/skills
cmp $D/prd/scripts/validate_policy.py $D/architecture/scripts/validate_policy.py && echo same
```

The build session ran `test_shared_files.py` on the source (OK, 5 tests). That is evidence for the
source tree, not a recorded run of this item.

### A2. ERR-05 with a decision accepted before validation (VER-12 (i))

`fresh architecture/failed-amendment-stays-in-review` (PRD-001 v2 adds a NEEDS ADR marker about the
roster; the approved ARCH-001 has an existing CMP-01 whose `status: current` the self-check rejects).
Start Claude as in 2.0 and say:

> /devforgeai:architecture PRD-001 — amend ARCH-001; I confirm the amend outcome.

When it asks about the roster question, pick one option explicitly, and give your name if asked who
decides. Answer *Decide later* to any other question.

**Expect:**
- It writes an accepted ADR for your pick, then validation finds CMP-01's status, which it can't
  repair (an amendment leaves CMP-01 unchanged). It stops after at most four checks.
- The ADR is kept as `status: proposed` with `approved_by: ""` and `approved_on: null`, and has a
  Status history row `Restored to proposed: validation failed`.
- The roster DEC is back to `state: open` with `resolved_by: []`.
- ARCH-001 is `in-review` with `approved_by: ""` and `approved_on: null`, CMP-01 is unchanged, and a
  Change Log row records the failure.
- The reply is a validation-failure report: the files and the statuses left, the checks and repairs,
  and the unresolved CMP-01 error. It presents no readiness as validated and doesn't send you to
  `/devforgeai:epic`.

### A3. Failed supersession rolls back (VER-19)

`manual failed-supersession`: PRD-001 v2 adds a NEEDS ADR marker; the approved ARCH-001's DEC-01
(identity provider) is resolved by the accepted ADR-001 (Auth0), and its existing CMP-01 has
`status: current`, which the self-check rejects. Record the starting state, then start Claude as in 2.0:

```bash
git init -q && git add -A && git -c user.name=t -c user.email=t@t commit -qm fixtures
```

> /devforgeai:architecture PRD-001 — amend ARCH-001; I confirm the amend outcome. We're dropping
> Auth0 for sign-in.

The request can't approve a supersession by itself (the skill takes only four kinds of decision from
a request), so give the approval as an answer:
- when it asks about DEC-01 or about replacing ADR-001, choose a different provider and approve
  superseding ADR-001;
- if it doesn't bring DEC-01 up, answer: "Reopen DEC-01: replace ADR-001 with a new decision. I
  approve superseding ADR-001." Then pick a provider from the options it gives.

Give your name if asked who decides, and answer *Decide later* to anything else. If the skill never
records a supersession, the case didn't reach the rollback: record it as not run, with what happened.

**Expect:**
- It records the supersession (a new accepted ADR with `supersedes: [ADR-001]`, and ADR-001 marked
  superseded), then validation finds CMP-01's status, which it can't repair. It stops after at most
  four checks.
- `git diff --exit-code docs/specs/adr/ADR-001.md` prints nothing: ADR-001 is byte-identical to the
  fixture (`status: accepted`, `superseded_by: null`, the same Status history).
- The replacement ADR is kept with `status: proposed`, `approved_by: ""`, `approved_on: null` and
  `supersedes: []`. Its "Decision outcome" says it was intended to supersede ADR-001 as you decided,
  and is not in force; its Status history ends with a `Restored to proposed` row naming the rollback.
- DEC-01 is `state: open` with `resolved_by: []`, not `[ADR-001]`.
- ARCH-001 is `in-review` with `approved_by: ""` and `approved_on: null`, CMP-01 is unchanged, and
  the Change Log row records the failure and the rolled-back supersession.
- The reply is a validation-failure report naming the rollback. It presents no readiness as
  validated and doesn't send you to `/devforgeai:epic`.

## 4. Results

| Item | Result | Date | Notes |
|---|---|---|---|
| Eval: prd, 3 runs with baseline | NOT_RUN | | |
| Eval: architecture, 3 runs with baseline | NOT_RUN | | |
| M1 VER-11 interview and partial answer | NOT_RUN | | |
| M2 VER-11 stop mid-interview | NOT_RUN | | |
| M3 VER-12 approved extension, ERR-04 | NOT_RUN | | |
| M4 VER-12 shared constraint | NOT_RUN | | |
| M5 VER-12 unknown and malformed BRN, ERR-06, QR-01 | NOT_RUN | | |
| M6 VER-23 local preferences | NOT_RUN | | |
| M7 VER-23 SV rules, calendar check and can't run | NOT_RUN | | |
| M8 session ID | NOT_RUN | | |
| A1 SPEC-003 VER-12 (f) | NOT_RUN | | |
| A2 SPEC-003 VER-12 (i) | NOT_RUN | | |
| A3 SPEC-003 VER-19 failed supersession | NOT_RUN | | |
