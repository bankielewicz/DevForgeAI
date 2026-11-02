# Runbook: SKL-002 v6 manual checks (SPEC-002 v6 VER-46, VER-47, VER-48)

Covers what the eval suite can't show for the prd skill's version 6 interview (SPEC-002 v6, issue #142):
eval runs are `claude -p` sessions that nobody answers, so every behaviour that needs a live answer is
checked here. Each item stays **NOT_RUN** until someone runs it on the SKL-002 v6 build commit. Record each
result in section 4: **pass**, **fail** (with what happened), or **not run** (with why). A failure stays a
failure: if the spec turns out to be wrong, record it and raise it with the owner; don't adjust the check.

Paste each command on its own. None starts with `!`, and none uses a `\` continuation or a heredoc.

## 0. Setup (once per shell)

The plugin is a **copy** of the build commit's source, loaded with `--plugin-dir`; the real source under
`src/` is never edited. The workspace sits outside the repository, so the session doesn't load the
project's `CLAUDE.md`, `AGENTS.md` or the deployed plugin.

```bash
WT=~/Projects/DevForgeAI          # or the worktree that holds the build commit
T=/tmp/prd-v6-test
rm -rf "$T" && mkdir -p "$T" && cp -r "$WT/src/claude/DevForgeAI" "$T/plugin"
fresh() { rm -rf "$T/ws" && mkdir "$T/ws" && cd "$T/ws" && bash "$T/plugin/evals/prd/$1/scaffold.sh"; }
```

`fresh <case>` makes an empty project in `$T/ws` and seeds it with that eval case's fixtures. The cases
to seed: `states-the-count` (BRN-003, 14 promoted ideas; VER-40), `locked-budget-respected` (the same plus
POL-001; VER-41), `continue-asks-only-open` (a draft PRD-001 with open decisions; VER-45). Then start
Claude from `$T/ws` with the copied plugin:

```bash
claude --plugin-dir "$T/plugin"
```

Check that `/devforgeai:prd` appears in the completion list. To restart between items: `/exit`, run
`fresh …` again, then the same `claude` line. Record the Claude Code version (`claude --version`), the
build commit (`git -C "$WT" rev-parse --short HEAD`) and the plugin version from `$T/plugin/.claude-plugin/plugin.json`.

The other project's brainstorm (about 35 promoted ideas, the shape #142 reports) is the candidate fixture
for M1, with Bryan's consent; `fresh states-the-count` is the fallback. For every item, note each question
whose wording caused difficulty: those examples feed #142's deferred plain-language question.

## 1. M1. Triage and the table (VER-46; BEH-20, BEH-21, BEH-22, ERR-10)

`fresh states-the-count`, then `/devforgeai:prd BRN-003`. Give no priorities in the request.

| Step | Do | Pass when |
|---|---|---|
| (a) | Read the first question of the first call (and, after the run, the reply's text before it in the transcript) | The question's text holds the reuse line and the count line (`interview.max_calls=8 (default)`, 14 or more open requirements, an estimate above 8, `8 available`), and so does the reply before the call. The first question is the mode question, with triage by group, a review file, a pasted list and a raise, each with its cost in calls, none marked recommended or pre-selected (VER-46 (a), (f)) |
| (b) | Pick triage by group. In the first triage call, tick one requirement in one group, nothing in another, and 'None of these' alone in a third | Each question holds at most three requirements plus 'None of these'; four questions per call. After the write: the ticked one is `must`/`current`; every requirement of the second and third groups has `priority: null` and `release: null` unless the table later set it; the reply and the Change Log row hold `Not must now:` with the third group's IDs and nothing for the second group |
| (c) | In a later group, tick 'None of these' together with a requirement | The reply says the answer contradicts itself, decides nothing for the group, and asks it again in the next call. Answer the same way again: the group stays null and the reply names it |
| (d) | At the table question: first type "FR-002 should now" as the answer; then, when the revised table comes back, type "accept" | The first table lists every open requirement with `later (suggested)`; after the typed change the revised table comes back as plain text, not as another options menu, with FR-002's row changed; typing "accept" writes every row, and the reply lists each ID with its statement, priority and release. (Run once more with 'Decide none now': nothing is written for the table's rows) |
| (e) | Count the AskUserQuestion calls in the transcript | The number equals the count the final reply gives, and is at most 8 (or the raised budget), the mode question, the repeat from (c) and the correction round from (d) included |

## 2. M2. The raise (VER-47; BEH-20, BEH-21, BEH-23, ERR-11)

| Step | Do | Pass when |
|---|---|---|
| (a) | `fresh states-the-count`, `/devforgeai:prd BRN-003`, choose "raise the budget to N" at the mode question | The interview continues past 8 calls, up to N. In PRD-001's Change Log row the resolution line still reads `interview.max_calls=8 (default)` and the row holds `Interview budget raised in the session to N calls` |
| (b) | As (a), but type "raise it to 25" | Refused, with ADR-003's range (1 to 20) named; the resolved budget stays; the modes are offered again |
| (c) | `fresh locked-budget-respected` (POL-001#SET-01 sets `interview.max_calls` 3 with `overridable_by: []`), `/devforgeai:prd BRN-003`, and say "take as many calls as you need" | The count line reads `interview.max_calls=3 (POL-001#SET-01)` and says the budget is locked by that setting; the mode question has no raise option; the count line names what stays null under each mode; asking for more in words is refused with the setting named |
| (d) | `fresh states-the-count`, add `.claude/devforgeai.local.md` with `devforgeai_local: 1` and `interview.max_calls: 1`, then `/devforgeai:prd` with no argument, and ask for no raise | The BRN gate takes the only call (the local value is not a lock: a raise would be allowed, but none is asked for); the reply says the gates used the budget, proceeds as if without questions, leaves every other decision null, and says the PRD can be continued with a pasted list in the request. Then `/devforgeai:prd BRN-003` with "Continue PRD-001: FR-001 must now; the rest: decide later. Proceed without questions.": PRD-001 reaches version 2 with FR-001 `must`/`current`, nothing else changed, and no call was made |

## 3. M3. The review file, the continue, and the answers that decide nothing (VER-48; BEH-13, BEH-24, BEH-25, BEH-26, ERR-07, ERR-09)

| Step | Do | Pass when |
|---|---|---|
| (a) | `fresh states-the-count`, `/devforgeai:prd BRN-003`, choose the review file | The draft PRD-001 is written with every undecided field null and validated; `devforgeai/drafts/prd/PRD-001-review.md` exists in SPEC-002 §4's shape, with one row per open decision and no suggestion; `devforgeai/drafts/.gitignore` holds `*`; the reply's last paragraph starts with "Next step" and names the file and `/devforgeai:prd BRN-003`, not the architecture step |
| (b) | Fill three cells (one priority, one release, `operating_context`), write `soon` in one priority cell, leave the rest blank; `/devforgeai:prd BRN-003` | The skill offers to continue PRD-001 (or continues on "continue PRD-001"); PRD-001 reaches version 2 with the three cells applied, the `soon` row reported as unreadable and unchanged, blanks still null, every other line byte-identical; the review file still exists; the Change Log row holds `Continued:` with the three values. Run `/devforgeai:prd BRN-003` again with "continue PRD-001, proceed without questions": nothing changes |
| (c) | `fresh continue-asks-only-open`, "Continue PRD-001." Dismiss the first question (Esc); leave the second blank or pick nothing; answer a quality category "none" | After the run: the dismissed and the empty question's fields keep their earlier value (null, or the value PRD-001 already had); the "none" is recorded in section 7's prose as the user's answer |
| (d) | In the same run, when an option is marked "(suggested)", pick a different one or type text | The suggested value is not written anywhere |
| (e) | Answer a multiple-choice question with free text | The skill acts on the text or asks in plain text; it doesn't show another options menu for that question |
| (f) | `fresh states-the-count`, `/devforgeai:prd BRN-003`, answer two calls, then say "stop" | The skill asks whether to save a draft, with or without a review file; "yes, without" writes PRD-001 with every undecided field null, validated and reported, and the reply says it can be continued. Then "Continue PRD-001.": the reply's reuse line lists the values already set with the source `PRD-001 v1`, and the questions cover only the open decisions (no quality category is asked again) |

## 4. Results

Fill one row per step. Keep the build commit, the Claude Code version and the plugin version at the top.

| Build commit | Claude Code | Plugin | Run by | Date |
|---|---|---|---|---|
| | | | | |

| Item | Step | Result | Notes (what happened; the question wordings that caused difficulty) |
|---|---|---|---|
| VER-46 | M1 (a) | NOT_RUN | |
| VER-46 | M1 (b) | NOT_RUN | |
| VER-46 | M1 (c) | NOT_RUN | |
| VER-46 | M1 (d) | NOT_RUN | |
| VER-46 | M1 (e) | NOT_RUN | |
| VER-46 | M1 (f) | NOT_RUN | (checked with M1 (a)) |
| VER-47 | M2 (a) | NOT_RUN | |
| VER-47 | M2 (b) | NOT_RUN | |
| VER-47 | M2 (c) | NOT_RUN | |
| VER-47 | M2 (d) | NOT_RUN | |
| VER-48 | M3 (a) | NOT_RUN | |
| VER-48 | M3 (b) | NOT_RUN | |
| VER-48 | M3 (c) | NOT_RUN | |
| VER-48 | M3 (d) | NOT_RUN | |
| VER-48 | M3 (e) | NOT_RUN | |
| VER-48 | M3 (f) | NOT_RUN | |

When every row is filled, record the outcome in SPEC-002 §9 as a record-only row (no version bump), as
VER-11, VER-12 and VER-23 were recorded.
