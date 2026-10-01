# Codex brainstorm validator update — 2026-10-01

The script fix is authored. All three D-03 probes are rejected with specific messages,
and the package suite passes 287 tests. Native `writes-valid-brn` passes; `records-provenance`
fails the existing D-04 model-identity requirement. Both validate on their first invocation.
Plugin Creator's package validator is unavailable (NOT_RUN). Strict whole-run custody
FAILS because transient untracked primary paths appeared and the shared papercut log changed,
although every captured original primary file still matches. This source update does not
establish owner acceptance or skill qualification.

## Authority and candidate

- Worktree: `/tmp/devforgeai-brainstorm-validator-20261001`.
- Branch: `codex/brainstorm-validator-20261001`.
- Baseline: `7e2bfb66abb5998446aadee0f0b5b2692406fd49`, both primary HEAD and origin/main at intake.
- Implementation checkpoint: `6f01ecf`; the exact source/test file hashes accompany each test record.
- Authority: SPEC-001 v10, approved, BEH-09 at line 168; SHA-256
  `be35ffe8fa1ed28dab03f9adc5bec531a8595c66b42213937b1b4f1f2ec13702`.
- Provider contract: `skills/brainstorm/references/output-rules.md` in this Codex package.
- Reference: Claude commits `c921b0e` and `d7ac060`, merged as `7e2bfb6`,
  [PR #33](https://github.com/bankielewicz/DevForgeAI/pull/33). The reference is not the authority.
- Candidate runtime manifest/digest, exact executable/version, frozen cases and controller hashes:
  [native binding](native/binding.json). Candidate digest:
  `efb8dd298d909a2b76bd1627127c6e85d0486901dd08b84a8ce68e9f1227c2c4`.
- Plugin stays 0.6.0; brainstorm stays SKL-001 v7, draft. No conflicting version-bump convention
  was found in the applicable package guidance. Skill instructions and contracts are unchanged.

## Changes mapped to authority

Line references below use the frozen Codex output rules and Claude's validator at `7e2bfb6`.
All script changes come from `c921b0e`, except the two requested Codex diagnostic adaptations.
The third test environment comes from `d7ac060`.

| File / fix | Claude counterpart | Codex output-rule lines / authority | Evidence |
|---|---|---|---|
| `skills/brainstorm/scripts/validate_brn.py`: calendar dates, catch all optional YAML parsing exceptions, one-line diagnostics without duplicate date errors | 186–196, 431–446 | 46, 143; SPEC-001 BEH-09 | Invalid month/non-leap date and valid leap-day cases in all three environments |
| Same: reject blank owner and empty/non-list authors; accept quoted block/flow lists and clarification owner | 197–218, helpers 54–110 | 47–48, 118–122, 143 | Template/default, block-list and author cases |
| Same: blank last Change Log author; preserve Codex tool/session checks and historical Claude rows | 294–309; existing Codex adaptation retained | 126–136, 155–156; explicit port instruction for historical rows | All 10 original tests unchanged; historical/latest-row case in all three environments |
| Same: reject unknown provenance key; scan table placeholders while permitting inline HTML | 241–269 | 37, 49, 143–145, 153–154 | Three frozen D-03 probes, table placeholder and inline-HTML controls |
| Same: validate lifecycle fields, participants, sources and upstream flow records in a block list | 219–231 | 53–58, 62–69 | Frontmatter negative cases and valid list/link controls |
| Same: retain item boundaries and addresses with comments; reject text after a closing quote | 54–83, 348–354, 396 | 75–81, 102, 149–150 | Comment, quoted-tail and hidden-disposition regression cases |
| Same: identify unindented lists, independent empty-block errors, one fence per collection, token-specific fixes | 262–269, 324–362 | 73–81, 147, 153–154; indentation example 163 | Unindented/empty/two-collection/template cases |
| Same: report non-UTF-8 input without traceback | 126–131 | SPEC-001 BEH-09 and the explicit port error-handling requirement | Invalid-byte subprocess case in all three environments |
| `tests/test_validate_brn_regressions.py`: 32 cases × 3 environments | Claude test module at `7e2bfb6`, including `d7ac060` | BEH-09; package README Local checks | 96 executions; same verdicts with user PyYAML, system PyYAML and no PyYAML |
| `IMPORT-REPORT.md`: three dated additions only | No Claude counterpart; required Codex resolution record | Handoff deliverables D-03, BEH-04/09 and updated test count | Original text/tables preserved; links to new evidence |
| `brainstorm-validator-update-evidence/`: command, custody and native records | Historical native controller reused read-only | Handoff evaluation/delivery requirements | Per-attempt records and final acceptance matrix |

The author diagnostic uses `authors must be a non-empty list of quoted names, e.g. ["Bryan", "codex"]`.
The blank-author diagnostic names `codex (session ID)`, explicitly accepts historical
`claude-code (session ID)` rows, and permits the name of the person who made the change.
Tests assert this wording. The existing tool/session matching branch is retained unchanged.

`test_real_brn_001_passes` was replaced by `test_historical_claude_latest_row_passes` in the
new module: the suite depends only on this package, so it runs from the package README's
working directory. The new valid fixture has Codex provenance. The three historical
probe files under `import-evidence/validator-probes/*/claude/` remain byte-for-byte unchanged;
the new probe test requires all three fixtures rather than silently skipping missing files.
The existing `tests/test_validate_brn.py` is unchanged. No acceptance test was weakened.

## Verification

Commands are run from the worktree root unless a different working directory is specified.
Each JSON record retains command, cwd, revision, source/test hashes, stdout, stderr and exit code.

| Requirement / check | Status | Command / result and evidence |
|---|---|---|
| All seven intake pins | PASS | SHA-256 comparison; [primary baseline](primary-before.json), [worktree baseline](worktree-before.json) |
| Baseline before first source edit | PASS | `python3 -B -m unittest discover -s src/codex/devforgeai/tests -p 'test_*.py'`: exit 0, 191 tests, 17.239s; [record](baseline-tests.json) |
| Meaningful failing regression test | PASS | New module against the original script: exit 1, 96 executions, 75 failures; [RED](tdd-red.json). Expected failures are retained, including false acceptances and tracebacks. |
| Requested fixes and original Codex adaptation | PASS | `python3 -B -m unittest discover -s src/codex/devforgeai/tests -p 'test_validate_brn*.py'`: exit 0, 106 tests, no skips; [GREEN](tdd-green.json) |
| Full package regression suite | PASS | Baseline command on checkpoint `6f01ecf`: exit 0, 287 tests, 20.749s; [record](package-tests-root.json) |
| Full package suite from package directory | NOT_RUN | Final checkpoint run pending |
| D-03 frozen probes | PASS | New Codex script rejects all three, each with its specific message; [same-shape results](validator-gap-probes.json) |
| Valid Codex-provenance BRN | PASS | `OK` in all three subprocess environments; [fixture](valid-codex/docs/specs/brainstorm/BRN-001.md), [results](valid-codex-results.json) |
| PyYAML environment distinction | PASS | User site 6.0.3; throwaway HOME uses system 6.0.1; `python3 -S` cannot import PyYAML. All 96 cases executed without skips. |
| Obsolete catch/table exemption removed | PASS | Both searched strings absent; [search record](required-searches.json) |
| Skill validation | PASS | `python3 -B /home/bryan/.codex/skills/.system/skill-creator/scripts/quick_validate.py src/codex/devforgeai/skills/brainstorm`: exit 0; [record](skill-validation.json) |
| Manifest JSON syntax | PASS | `python3 -m json.tool src/codex/devforgeai/.codex-plugin/plugin.json`: exit 0; [record](manifest-json.json) |
| Plugin Creator package validator | NOT_RUN | Helper absent from installed skills/plugin bundles and no callable equivalent found; [discovery](plugin-validator-availability.json). Manifest/skill checks do not substitute for this gate. |
| Primary/source custody after native execution | FAIL overall | All 3,690 read-only worktree files and 3,694 captured primary files match. Primary status/path set and the external Codex papercut log changed; [full before/after hashes](custody-after-native.json), [drift details](primary-drift-details.json). Candidate, definitions, runtime executable, trial copies and user config still match. |
| Whole-patch whitespace | FAIL | `git diff --cached --check`: exit 2, whitespace in retained actor Markdown hard breaks and unified-diff context lines; [unmodified diagnostics](whitespace-attempt1.json). Raw evidence is retained as emitted. Source/tests/import-report whitespace is checked separately and does not waive this failure. |
| Write scope | PASS | No path outside the authorized script, new test module, import-report additions and new evidence folder changed in this worktree; [audit](custody-after-native.json). |

## Native evaluation

One plugin-arm repetition each of `writes-valid-brn` and `records-provenance`, using the
historical Brainstorm import's `Server` controller without modifying it. The wrapper
[native_trials.py](native_trials.py) pins the immutable Codex CLI 0.159.3 executable
and checks its SHA-256 before each launch. Candidate copies include the full current
package runtime and match the frozen manifest. Each project has a unique temporary parent.
The frozen prompt bodies are unchanged; model and session come from `thread/start` receipts.
The controller uses the process-scoped skill discovery and thread APIs described in the
[official app-server documentation](https://learn.chatgpt.com/docs/app-server#skills).

| Case | Native status | Score | Validator attempts / retries |
|---|---|---|---|
| writes-valid-brn | PASS | 1.00 | One successful invocation, zero repair retries |
| records-provenance | FAIL | 0.00 | One successful invocation, zero repair retries |

Both native turns completed, in 559.990s and 444.483s respectively. Binary scores use
the frozen historical all-applicable-graders rule, not the fraction of graders passed.
See the [final summary](native/summary-final.json),
[valid-BRN assessment](native/writes-valid-brn--plugin--1/grade-final.json), and
[provenance assessment](native/records-provenance--plugin--1/grade.json).
The first valid-BRN assessment is retained with handoff review pending; its separate final
assessment completes that manual rubric without changing automated results or rerunning the actor.

The provenance failures are `session-substituted` and `host-provenance-match`:
the document records model `unknown`, while the host receipt records `gpt-6-astra`.
Session `01a0f7ea-96ef-7680-b03d-56a1661283ea` matches exactly. The actor checked the available
model environment variables and disclosed the unavailable identifier. This reproduces
the historical D-04 host-exposure limitation; the sentinel is honest but does not meet VER-03.
The valid-BRN document also has incomplete model provenance, outside its narrower VER-01 rubric.
Neither trial needed a stricter-validator repair. There was no harness failure, platform
interruption or observed grader defect. No native trial was retried.

The raw traces show reads of each trial's own candidate/project and explicit ancestor
instruction checks, plus ordinary web lookups. No sibling trial or historical-evidence content
read was observed. Native nonzero discovery commands (empty `rg` results and `git status`
in a non-repository) are retained; they are not validator failures.

Raw attempts, failures and interruptions are retained. A completed response is not by itself
a behavior pass. Each applicable grader is evaluated, including actual validator execution
and exact host provenance; the document-quality rubric is reviewed against the saved BRN.
The inherited 0.8 threshold and three-run full qualification contract are unchanged. These
two one-run trials are the requested focused smoke measurement, not a new full qualification.
Claude's two 1.00 scores are reference evidence only and do not qualify this Codex candidate.

## Custody and delivery

All tracked files in the worktree and all tracked/untracked visible files in the primary
checkout were hashed before edits, including the pinned handoff prompt. This covers the
read-only Claude files, specifications, schemas, templates, contracts, eval definitions and
all historical evidence. [External inputs](external-inputs-before.json) bind the skill guidance,
quick validator and both papercut logs. The primary's two modified rule files and untracked
handoff were preserved byte-for-byte.

The first custody audit observed 21 new untracked Claude configuration paths in the primary
checkout. All had disappeared by the follow-up observation, without any cleanup by this task.
Their origin is unverified. The Codex papercut log gained an unrelated LLM Foundations S0 entry;
the other six external inputs match. Preserve the [failed initial audit](custody-after-native.json),
[failed follow-up observation](primary-drift-details-attempt1.json), and
[drift details](primary-drift-details.json). This prevents claiming the primary was wholly
unchanged throughout the run even if its closing state matches. Proposal: review ownership
of those transient configuration paths separately; do not restore, remove or adopt them here.

The Git staging/checkpoint operations required host escalation because the sandbox makes
shared `.git` metadata read-only. The native launchers also used approved host access;
their actor threads retain workspace-write sandboxing and never approval policy.
This task ran no operations to change permissions, marketplaces, saved user configuration,
deployment or installation. The frozen user config digest still matches.
No new papercut entry was needed: both the Git metadata restriction and missing Plugin
Creator validator are already documented in the Codex log.

| Dimension | Status |
|---|---|
| Source authored | PASS; script and new test module authored, original tests preserved |
| Static validation | Package/skill/manifest/probes PASS; whole-patch whitespace FAIL on raw evidence; Plugin Creator validator NOT_RUN |
| Native behavior | FAIL overall: valid-BRN PASS; provenance FAIL on existing D-04; zero validator retries |
| Whole-run preservation | FAIL for observed primary/external drift; scoped source and all captured original primary bytes preserved |
| Git delivery | NOT_RUN by instruction: local checkpoints only; no push, PR or merge |
| Owner acceptance | NOT_RUN; Bryan owns this decision |

No newly required contract change or Codex-host conflict was identified while porting the
specified fixes. This remains a partial structural validator, not a complete schema validator
or proof of confirmed user decisions. Existing skill-text, handoff, trigger and broader
qualification findings remain outside this update.
