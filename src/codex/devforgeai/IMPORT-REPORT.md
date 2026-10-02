# Brainstorm Codex import and SPEC-001 comparison

The requested source port and native evaluation are complete at `src/codex/devforgeai`.
The 48-run matrix produced **21/24 passing plugin trials** and **3/24 passing baseline
trials**; seven of eight imported cases meet the three-run threshold. Eight manual
scenarios and three supplemental isolation controls also ran. **Full SPEC-001 acceptance
is not met**: model provenance fails, its fallback prevents confirmed convergence, and
the PRD-present branch is blocked by the absent Codex PRD skill.

The [native evaluation report](import-evidence/native-evaluation-20260928/REPORT.md)
contains the full **7 PASS / 2 FAIL / 1 BLOCKED** expanded ten-obligation result and raw
evidence links. The literal VER-09 core passes; its expanded confirmation scenario fails.
No marketplace entry, installation, deployment, or specification approval was performed.

## Bound inputs and result

- Specification: [SPEC-001](../../../docs/specs/spec/SPEC-001.md), approved **v10**;
  SHA-256 `6e3f685033e1f6c07829022aeb5567a339c50399f3df654a78bfe284f8f96267`.
- Source: `src/claude/DevForgeAI/skills/brainstorm`, **SKL-001 v5**, plus its eight
  cases from `src/claude/DevForgeAI/evals/brainstorm` and the source plugin identity.
- Destination: plugin **devforgeai 0.1.0**, containing **SKL-001 v7**, a Codex provider
  variant. Keeping SKL-001 preserves the original SPEC link; v7 includes the requested Codex question-tool mapping.
- Imported files: **56**, of which **35 are byte-identical** and **21 are adapted**.
  The BRN template, framework index, and diverge-converge framework are byte-identical.
- Candidate: **62 files**, excluding this report and retained import evidence;
  SHA-256 **`319fdfe17a22688e7a39ae4018d3914777cbd2c76616f4486aaeba2e3e46ce8e`**. The exact file list and digest rule are in
  [candidate-manifest.json](import-evidence/candidate-manifest.json).
- At the original import readback, all **71 pre-existing inputs** had their original bytes.
  Separate work added Claude PRD files during this task; they were preserved and not imported.
  The final readback finds the Claude PRD skill present and the Codex PRD skill absent.
- This workspace has no Git metadata, so a worktree, commit, and historical diff were unavailable.

## Intentional provider adaptations

These are explicit differences from a specification written for Claude Code, rather than
claims of literal conformance to its provider interface.

| SPEC-001 contract | Codex implementation | Assessment |
|---|---|---|
| §3: `.claude-plugin/plugin.json` | `.codex-plugin/plugin.json`, normalized `devforgeai` folder/name, `skills: "./skills/"`, real author and UI metadata | Supported plugin-creator compatibility package. |
| §5, BEH-01: slash command, `$ARGUMENTS`, `argument-hint`, Claude tools | Codex skill selection or `$brainstorm` in CLI; topic from the message; host file/shell tools and `request_user_input`; Claude-only frontmatter field removed | Natural-language triggering observed; the native catalog names this skill `devforgeai:brainstorm`. Unqualified CLI alias resolution was not separately tested. |
| §5 automatic invocation | `agents/openai.yaml` explicitly sets `allow_implicit_invocation: true`; source trigger description retained | Static configuration verified. |
| BEH-03/08/09: `${CLAUDE_SKILL_DIR}` paths | Resources resolve from the actual loaded SKILL.md directory; BRNs resolve from the consuming project | No invented Codex path environment variable. |
| BEH-07/11, VER-03: `claude-code`, Claude session and resume semantics | `codex`, actual host model/task identity, Codex Change Log rows; prior Claude history retained | Necessary provider change. No Claude transcript-retention or resume guarantee is carried over. |
| BEH-10: `/devforgeai:prd BRN-NNN` | Available DevForgeAI Codex PRD skill, if supplied; otherwise explicit unavailable-workflow handoff | ID-only input and final `Next step` paragraph preserved. No PRD is generated. |
| QR-03, VER-01/06/07: Claude `Skill` events and tool allowlists | Explicit host trace reviews replace `tool_used: Skill`; Claude allowlists removed from case metadata | Definitions exercised by the retained native app-server evaluator; installed-plugin qualification remains separate. |

The validator now checks `codex (session ID)` as well as historical Claude rows, enforces
the latest agent/session match, and leaves earlier Change Log rows untouched. This is a
provider adaptation with regression coverage, not a general validator rewrite.

The packaging and invocation choices follow
[OpenAI plugin packaging](https://developers.openai.com/plugins/build/plugins) and
[OpenAI skill guidance](https://learn.chatgpt.com/docs/build-skills), read for this import.

## Remaining discrepancies and limits

### D-01 — PRD-present verification does not fit the imported scope

SPEC-001 **VER-10** (line 324) says the plugin ships PRD and requires the runnable command.
This requested single-skill Codex import has no `skills/prd/SKILL.md`. Its handoff correctly
uses BEH-10's absent-PRD branch, and its imported `hands-off-to-prd` case tests that branch.
Thus it does **not** satisfy the PRD-present VER-10 obligation as written. The Claude PRD
skill appeared after the import snapshot, but that does not make a Codex PRD skill available.
Resolution: port PRD separately, or have the specification owner define a Brainstorm-only
provider acceptance profile. The denominator has not been reduced.

### D-02 — Native evaluation completed; installation qualification remains separate

The eight imported cases ran three times with the plugin and three times without it.
The candidate was loaded through process-scoped native skill roots, without installation
or forced skill injection. Seven cases pass at 3/3; `records-provenance` fails at 0/3.
VER-05, stop/save choices, three-attempt handling, extension preservation and native
`request_user_input` behavior were exercised. The confirmed-convergence discrepancy is
recorded under D-04.

The [frozen plan](evals/verification-plan.json) retains its initial NOT_RUN states as
historical input; [current results](import-evidence/native-evaluation-20260928/results.json)
report every obligation. No mandatory failed or blocked item was removed. This is a
source evaluation graded by the importing agent, not independent or installed-plugin
qualification. Three filename-exposure controls and setup failures are retained.

### D-03 — Inherited validator accepts three rule violations

BEH-09 and the output-rule checklist require structurally valid content and no unresolved
template placeholders. Retained probes demonstrate these false negatives in **both** the
source and imported validator:

| Invalid input | Contract violated | Source / Codex result |
|---|---|---|
| `authors: 123` | Authors must be a list of names | Accepted / accepted |
| Extra `generated_by.unexpected` field | Provenance map is limited to tool, model, session | Accepted / accepted |
| `<change>` in a Change Log cell | No leftover template placeholders | Accepted / accepted |

See [probe results and fixture paths](import-evidence/validator-gap-probes.json). The script
checks selected fields and optionally YAML syntax, not complete JSON Schema conformance;
table rows are skipped by its generic placeholder scan. The port documents this limit.
These inherited defects remain open. A script exit-zero cannot establish full BEH-09 or
§4 conformance, and neither script can determine whether a user confirmed a decision.

**2026-10-01 resolution:** D-03's three demonstrated false negatives are resolved in the
Codex validator source. The unchanged historical Claude-provenance fixtures are each
rejected with their own message; see the [new probe results](brainstorm-validator-update-evidence/validator-gap-probes.json)
and [scoped update report](brainstorm-validator-update-evidence/REPORT.md). The earlier
results above remain the record of the imported candidate. This resolution does not
establish full schema conformance or verification of user confirmation.

### D-04 — Missing host identity is reported, not fabricated

BEH-07/VER-03 require the actual model and session identity. Codex does not always expose
both to a skill. The port uses the explicit `unknown` sentinel when needed, keeps the BRN
draft, and discloses incomplete provenance. This fallback **does not satisfy VER-03**.
The actual authoring task ID was available; the exact model identifier was not, so the
port's sidecar honestly records `model: "unknown"`. No source model ID was copied as if
Codex had authored with it. Provenance graders reject an unknown model or session.

Native evaluation confirms this gap in all three provenance runs: the host records
`gpt-6-astra`, while the BRNs use `unknown`; their session IDs match the host.
The expanded confirmation scenario also preserves the user's exact dispositions/reasons
but keeps `status: draft` despite explicit convergence confirmation. That follows the
port's missing-identity fallback and diverges from BEH-06. See the
[confirmed-decisions evidence](import-evidence/native-evaluation-20260928/manual/confirmed-decisions/grade.json).

### D-05 — Specification examples and measurement wording are stale

§5's proposed frontmatter still says `devforgeai-version: "4"` (line 124); the imported
Claude source is v5 and the Codex port is v7. QR-01 (line 212) still measures size using
`devforgeai check`, while BEH-09 expressly forbids running that nonexistent CLI. The port
preserves the prohibition and checks size and schemas directly. These are specification
maintenance discrepancies; the approved source specification was not edited.

## Requirement-by-requirement static comparison

“Preserved” below describes authored instructions and files, not observed model behavior.
References are to [the imported SKILL.md](skills/brainstorm/SKILL.md) and its linked resources.

| Requirement | Imported evidence | Static assessment |
|---|---|---|
| BEH-01 | Intake: topic required, at most three unanswered clarifications, no-questions path | Preserved; argument transport adapted. |
| BEH-02 | Write step: highest BRN number + 1, ID-only path, directory creation | Preserved. |
| BEH-03 | Framework selection and unchanged catalog/default | Preserved; resource resolution adapted. |
| BEH-04 | Evaluation step and output rules restrict collections and fields | Preserved in instructions; validator limitations D-03. |
| BEH-05 | Divergence: user wording, 5–15 ideas, initially open | Preserved. |
| BEH-06 | User-owned dispositions and convergence; unconfirmed values remain open/draft | Preserved. |
| BEH-07 | Frontmatter and latest Change Log row | Provider adaptation; incomplete-identity limit D-04. |
| BEH-08 | Original template and heading/comment rules | Preserved; template bytes identical. |
| BEH-09 | Bundled script, readback of confirmation, three attempts, no devforgeai command | Preserved flow; inherited false negatives D-03. |
| BEH-10 | Report counts, ID/path, last `Next step` paragraph, no PRD drafting | Provider adaptation; PRD-present gap D-01. |
| BEH-11 | Extension keeps IDs/meaning/history, adds new IDs, updates latest author/session | Preserved with Codex authorship; historical-row regression passes. |
| ERR-01 | Existing-topic question before any write | Preserved. |
| ERR-02 | Stop asks draft-save choice; yes saves open/draft, no writes nothing | Preserved. |
| ERR-03 | Create and disclose missing output directory | Preserved. |
| ERR-04 | Missing/malformed framework falls back with disclosure | Preserved. |
| ERR-05 | Three-attempt limit, remaining errors, draft status | Preserved; native three-attempt scenario passes. |
| QR-01 | 247-line skill; framework/output detail in references | Static size/layout checked; measurement wording D-05. |
| QR-02 | Sidecar; two quoted metadata values; matching IDs/versions; supported Codex frontmatter | Repository schemas and Codex validators pass. |
| QR-03 | Eight tagged definitions, three runs and baseline in plan | Executed; provenance case fails and full acceptance remains unmet. |

**2026-10-01 update:** The historical BEH-04 and BEH-09 rows above refer to D-03's
then-open validator gaps. Those three gaps are now resolved by the source fix and
[probe rerun](brainstorm-validator-update-evidence/validator-gap-probes.json); see the
[update report](brainstorm-validator-update-evidence/REPORT.md) for the scoped checks
and separate native results. Other behavior and acceptance limitations remain as recorded.

## Complete native verification denominator

| Obligation | Case / required exercise | Status |
|---|---|---|
| VER-01 | writes-valid-brn | PASS, 3/3 |
| VER-02 | no-unconfirmed-dispositions | PASS, 3/3 |
| VER-03 | records-provenance | FAIL, 0/3: unknown model |
| VER-04 | uses-named-framework | PASS, 3/3 plus two separate controls |
| VER-05 | Add/select framework and missing-file fallback | PASS |
| VER-06 | ignores-unrelated-request | PASS, 3/3 |
| VER-07 | asks-for-topic | PASS, 3/3 |
| VER-08 | existing-brn and full-file preservation | PASS, 3/3; extension also passes |
| VER-09 | Expanded imported manual plan | FAIL: confirmed convergence stays draft; original SPEC stop/save, three failures and static limits pass |
| VER-10 | PRD-present handoff | BLOCKED / present branch NOT_RUN; imported absent branch passes 3/3 |

The expanded VER-09 status retains the extra confirmation/extension work required by
the imported eval README. It does not imply that the original stop/save or three-attempt
obligations failed. The full [evaluation report](import-evidence/native-evaluation-20260928/REPORT.md)
separates these checks and records the baseline scoring caveat.

## Checks performed and delivery status

| Check | Result / evidence |
|---|---|
| Plugin-creator manifest/package validation | PASS; [raw result](import-evidence/plugin-validation-r007.json) |
| Skill-creator quick validation | PASS; [raw result](import-evidence/skill-validation-r007.json) |
| Skill frontmatter and provenance against repository schemas | PASS; [static checks](import-evidence/schema-validation-r007.json) |
| Provider validator and imported-grader regressions | **10 tests passed on unchanged v6 validator/test files**, including standard-library-only execution; [raw result](import-evidence/validator-regressions-final.json) |
| Local skill/reference links | 6 checked, all resolve within the package |
| Imported regex definitions | 21 compile; this does not grade native traces |
| Source preservation | 71 input hashes unchanged at import readback; later source changes recorded below |
| Independent validation | NOT_PERFORMED; this report and checks were authored by the importing agent |
| Native behavior / framework acceptance | EXECUTED / NOT_QUALIFIED; [results](import-evidence/native-evaluation-20260928/results.json) |
| Marketplace / installation / deployment | NOT_PERFORMED |

**2026-10-01 test update:** The original 10 tests and their file are unchanged and pass.
The new regression module adds 32 cases in three environments (96 executions), giving
106 brainstorm tests and **287 passing package tests**, compared with the independently
recorded 191-test baseline. See [baseline](brainstorm-validator-update-evidence/baseline-tests.json),
[failing regression run](brainstorm-validator-update-evidence/tdd-red.json),
[passing brainstorm tests](brainstorm-validator-update-evidence/tdd-green.json), and
[full package run](brainstorm-validator-update-evidence/package-tests-root.json).

Reproduce the focused tests from the repository root:

```bash
python3 -B -m unittest discover -s src/codex/devforgeai/tests -p 'test_*.py' -v
```

[Final import manifest](import-evidence/final-import-manifest.json) and
[final source comparison](import-evidence/claude-to-codex-final.patch) record every imported
file. Initial import receipts and the first eight-test run are retained alongside the final
checks. Existing Claude source, deployment state, approved specifications, and user documents
were not edited by this import.

## Requested question-tool correction (2026-09-28)

The Codex skill now explicitly maps Claude's `AskUserQuestion` to
`request_user_input` for questions and confirmations. Plain-text fallback applies only
when the tool is unavailable or disallowed in the active mode. Pending questions and
timeouts never count as confirmation. SKL-001 is now v7.

Plugin and skill validation and both repository schema checks passed for this revision.
Validator and test files retain their v6 hashes, so the ten passing regression results
were retained without rerunning unchanged tests. Native evaluation was subsequently completed; current results are linked above.

The prior candidate and report are retained under
[revisions/skill-v006](import-evidence/revisions/skill-v006/).
The original source comparison remains bound to the import-time Claude source; apply
[question-tool-r007.patch](import-evidence/question-tool-r007.patch) after the v6 comparison
to account for this revision. Three Claude PRD-handoff evaluation files changed separately
since import. Their paths are recorded in the current candidate manifest. This correction
does not reimport those changes or edit the Claude source.


## Evaluation delivery (2026-09-28)

The native evaluator used Codex 0.158.0 on WSL with the host-selected gpt-6-astra model
and high reasoning effort. Direct traces confirm `request_user_input` in default and
Plan modes. Pending questions never counted as acceptance. The exact 62-file v7
candidate remains unchanged; source README/plan NOT_RUN wording is retained as the
import-time snapshot, while this report records current status.

The pre-evaluation report and manifest are preserved under
[pre-native-evaluation-v007](import-evidence/revisions/pre-native-evaluation-v007/).
The expanded denominator is still ten. Raw attempts, prompts, host identities,
artifacts, assertions, semantic reviews and additional isolation controls are retained
in [native-evaluation-20260928](import-evidence/native-evaluation-20260928/).
