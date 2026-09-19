# Enforcement register — `dev`

Run `20260919T021255Z`. Target `C:\Projects\DevForgeAI\src\claude\skills\dev`.
Package digest `8321da52e578ce1d72ce40b281882c756c03b260c75953820b4f209f90eb2d81`.

These are **candidates for later design**, not claims that a hook event, check or CLI command
exists today. Nothing here is an implemented acceptance gate. This register is the fifth
descriptive dimension of the assessment and does not contribute to PASS/FAIL.

Four candidates are carried from run `20260918T202845Z` with their evidence updated against
this run's bytes. ENF-005 is new.

---

## ENF-001 — Detect frontmatter-as-enforcement claims in skill packages

| Field | Value |
| --- | --- |
| Proposed destination | `ci_workflow`, with `claude_hook` as a lighter-weight variant |
| Trigger | Any change to a `SKILL.md` under `.claude/skills/`, `src/claude/skills/` |
| Invariant | A package must not claim that absence of a tool from `allowed-tools` prevents that tool from being used. |
| Inputs | The changed `SKILL.md` bytes; the `allowed-tools` and `disallowed-tools` frontmatter values |
| Intended observation | Flag prose matching the semantic pattern "X is absent from `allowed-tools`, so this workflow cannot Y", and the phrase "structural rather than asserted" when applied to an allowlist |
| Current evidence | **Updated.** The `dev` occurrence that generated the prior run's `F-c3d23eda` is corrected and verified resolved in this run (check `C-INS-001`, trial `T1-boundary`). The pattern remains uncorrected in sibling packages this run did not assess; the builder's own `validation-request.json` records the list: `qa/SKILL.md:55`, `skill-validator/SKILL.md:32`, `skill-builder/SKILL.md:27`, each in both mirror paths. |
| Failure behavior | Advisory comment on the change; not a merge block, because the classification is semantic and a correctly-worded discussion of the allowlist must pass. |
| Bypass and coverage limits | Keyword matching cannot establish the finding on its own — `rules.md` SV-007 requires semantic classification with context. A reworded claim carrying the same false meaning escapes a regex. Treat a hit as a review prompt, never as an automatic defect. |
| Dependencies | An agreed canonical statement of what `allowed-tools` does, sourced from the live Claude Code reference rather than restated locally. **This run re-verified that source live;** the retained extract is `inputs/rule-sources/claude-code-skills-allowed-tools.md`. |
| Future verification scenario | Seed a fixture package asserting "`Task` is absent from `allowed-tools`, so this workflow cannot spawn a subagent" and confirm the check flags it; seed a second fixture carrying this target's corrected wording and confirm the check stays silent. The corrected wording is now available as a real positive control at `source/SKILL.md` line 33. |
| Root cause not reached | `.claude/skills/skill-builder/references/claude-frontmatter.md` lines 13 and 28 state that `allowed-tools` restricts. The builder recorded this as unedited. A check on delivered packages catches occurrences; correcting that reference is what stops new ones being authored. |

---

## ENF-002 — Enforce the real boundary with `disallowed-tools`

| Field | Value |
| --- | --- |
| Proposed destination | `guidance_only` today; `ci_workflow` once a policy decision exists |
| Trigger | A package states a tool-use boundary as part of its contract |
| Invariant | A boundary the package presents as structural is backed by `disallowed-tools`, or is stated as an obligation rather than a structural fact. |
| Inputs | Frontmatter `disallowed-tools`; the prose boundary claims |
| Intended observation | Where a package says it cannot use tool X, either `disallowed-tools` lists X, or the prose is phrased as a discipline. |
| Current evidence | **Updated.** The prior run's `OQ-1` asked whether to state the boundary as an obligation or make it real with `disallowed-tools: [Skill, Task]`. The delivered build chose the obligation; the target carries no `disallowed-tools` field. The live reference re-read in this run confirms `disallowed-tools` is the field that actually removes tools from the pool, and that it accepts a YAML list. No package in either skill tree uses it. |
| Failure behavior | Review prompt naming the specific tool and the two available remedies. |
| Bypass and coverage limits | `disallowed-tools` clears when the user sends the next message, so it bounds the invoking turn rather than the whole session. It is a real but **turn-scoped** control, and this register must not oversell it as a session-long guarantee. It also cannot remove `EndConversation` while other tools remain. A `dev` run spanning many turns would hold the restriction only on invoking turns — the untested interaction the prior run cited when recommending the obligation. |
| Dependencies | A maintainer decision on whether these skills want the restriction or only the obligation. Answered for `dev` (obligation). Open for the family. |
| Future verification scenario | Add `disallowed-tools: [Skill, Task]` to a fixture skill, invoke it, and observe whether a `Task` call is refused within the invoking turn and available again on the next message. |

---

## ENF-003 — Keep the two mirrored Claude Code trees identical

| Field | Value |
| --- | --- |
| Proposed destination | `git_hook` (pre-commit) with a `ci_workflow` backstop |
| Trigger | A commit touching `.claude/skills/**` or `src/claude/skills/**` |
| Invariant | `diff -rq .claude/skills/<name> src/claude/skills/<name>` is empty for every skill present in both trees. |
| Inputs | Both trees |
| Intended observation | An empty diff. |
| Current evidence | **Updated.** Re-verified for `dev` in this run: `diff -rq` is empty across all 11 files after the builder's edit, retained at `trials/T2-line-endings/observed.md` section 5. The builder applied the edit to `.claude/skills/dev` under custody and wrote the identical string to `src/claude/skills/dev` outside that custody harness — exactly the situation this candidate exists to cover. The mirror held, but nothing mechanical required it to. |
| Failure behavior | Block the commit locally and name the differing paths; CI re-checks, because a local hook is bypassable with `--no-verify`. |
| Bypass and coverage limits | A local Git hook is advisory — not installed by cloning, and skippable. A GitHub-hosted check is the enforcing half; the two are different mechanisms and this register keeps them distinct. This run verified `dev` only, not the tree-wide invariant. |
| Dependencies | None beyond Git. |
| Future verification scenario | Edit one path only, attempt a commit, confirm the hook names the mismatch; confirm CI independently fails the same change pushed with `--no-verify`. |

---

## ENF-004 — Bind a specification to each host variant of a ported skill

| Field | Value |
| --- | --- |
| Proposed destination | `guidance_only` |
| Trigger | A skill package is ported between hosts |
| Invariant | Every shipped host variant resolves to a governing specification, or records explicitly that it is a derived port with no separate contract. |
| Inputs | The package; the specification tree |
| Intended observation | A resolvable specification reference per variant. |
| Current evidence | **Persistent.** `docs/specs/dev-skill-spec.md` is byte-unchanged from the prior run (`b9783ca0…`), still specifies a Codex skill, and still names `src/agents/skills/dev` as its build target. The assessed Claude Code package still has no governing specification. The builder declined this item explicitly, and correctly: a specification or process change is outside a skill edit's charter. |
| Failure behavior | Review prompt at port time. |
| Bypass and coverage limits | This is an authoring-process recommendation. No mechanical check can distinguish a deliberate derived port from an unspecified one without a declared convention. |
| Dependencies | A convention for recording derived-port provenance. **Partially advanced since the prior run:** a builder authoring run now exists for this package at `docs/plan/skill-authorings/dev/20260919T011204Z/`, retaining a contract, before/candidate/delivered manifests and a validation request. That establishes custody for the *edit*, not for the *port*; the original Codex-to-Claude conversion still has no retained record, so `ORG-U4` stands. |
| Future verification scenario | Port a fixture skill without a variant specification and confirm the review prompt fires; add a derived-port provenance record and confirm it clears. |

---

## ENF-005 — Verify the delivered byte change matches the declared change scope

| Field | Value |
| --- | --- |
| Proposed destination | `ci_workflow`, with `git_hook` (pre-commit) as the local half |
| Trigger | A commit touching `.claude/skills/**` or `src/claude/skills/**`, or a builder run declaring `changed_paths` |
| Invariant | A scoped content edit changes only the bytes its contract describes. In particular it does not convert a file's line endings, because `.gitattributes` declares `* -text` on the stated ground that "Retained manifests bind exact bytes." |
| Inputs | The declared change scope (a builder `contract.json` / `validation-request.json`, or the commit diff); the before and after bytes; `git diff --stat` and `git diff --ignore-cr-at-eol --stat` |
| Intended observation | The two `--stat` figures agree. Where they disagree, the difference is line-ending conversion rather than content, and the check names it. |
| Current evidence | **New in this run.** Finding `F-cb3c4b14…` in `findings.json`. The conversion is confined to the working tree — `ls-files --eol` reports `i/lf w/crlf`, so the index still holds LF and this instance has not yet reached history, while `qa/SKILL.md` reads `i/crlf` with a CRLF HEAD blob and therefore has. The builder's `validation-request.json` declared `changed_paths: ["SKILL.md"]` with expected output "Corrected scope paragraph in .claude/skills/dev/SKILL.md". The delivered content is correct — and the same write also converted all 50 lines from LF to CRLF, growing the file from 5,479 to 5,809 bytes. Measured cost, retained at `trials/T2-line-endings/observed.md` section 6: `git diff --stat` reports 50 insertions and 50 deletions; `git diff --ignore-cr-at-eol --stat` reports 1 and 1. `SKILL.md` is now the only one of the package's 11 files using CRLF, and one of only 2 CRLF files among the 26 legacy `SKILL.md` files — the other being `qa/SKILL.md`, already committed that way, which indicates a recurring rather than one-off effect. |
| Failure behavior | Advisory comment naming the file and the two `--stat` figures. Not a merge block: a deliberate whole-file reformat is legitimate when declared, and the check cannot read intent. |
| Bypass and coverage limits | This run settled which layer is responsible, which narrows what the check must guard: `git check-attr` reports `text: unset` and `git ls-files --eol` reports `attr/-text`, so `* -text` is genuinely in force and `core.autocrlf true` is overridden for these paths. Git normalisation is ruled out, so the check is guarding a **writing tool**, not a git configuration. It still cannot name the tool. A conversion committed with no accompanying content change yields a diff that is *entirely* line endings and is trivially detectable; the mixed case here is what needs the two-`--stat` comparison. The check cannot say which ending is correct for a package, only that a conversion accompanied a content edit. |
| Dependencies | A recorded convention for which line ending these packages use. None is written down; the convention is currently observable only statistically (24 of 26 LF). Writing it into the repository instructions or `.gitattributes` is the prerequisite that would let this check assert a direction rather than merely flag a change — recorded as `OQ-103`. Identifying the writing tool is a second, independent prerequisite if the intent is to fix the cause rather than detect the symptom; this run ruled out git but did not identify the writer. |
| Future verification scenario | Take a fixture LF package, apply a one-line content edit that also rewrites the file as CRLF, and confirm the check reports the 2-versus-100 discrepancy; apply the same content edit preserving LF and confirm the check stays silent. |

---

## Not proposed

No enforcement candidate is recorded for the workflow's evidence, traceability, checkpoint or
QA-metric instructions. They are already expressed as observable obligations with concrete
artifacts, and this run found no gap between what they instruct and what they can deliver.
Proposing a gate there would add ceremony without a demonstrated failure to prevent.

No candidate is proposed for the behavioural checks this run could not perform (`C-BEH-002`,
`C-BEH-003`). Those are limits on what a validator session can observe about its own host, not
invariants a hook could assert.
