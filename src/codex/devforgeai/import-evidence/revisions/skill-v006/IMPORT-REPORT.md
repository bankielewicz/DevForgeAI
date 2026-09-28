# Brainstorm Codex import and SPEC-001 comparison

The requested source port is complete at `src/codex/devforgeai`. It is structurally valid
and passes the focused regression checks below. It is **not yet behaviorally qualified
against SPEC-001**: the native verification denominator remains ten obligations, all
`NOT_RUN`. No marketplace entry, installation, deployment, or specification approval was performed.

## Bound inputs and result

- Specification: [SPEC-001](../../../docs/specs/spec/SPEC-001.md), approved **v10**;
  SHA-256 `6e3f685033e1f6c07829022aeb5567a339c50399f3df654a78bfe284f8f96267`.
- Source: `src/claude/DevForgeAI/skills/brainstorm`, **SKL-001 v5**, plus its eight
  cases from `src/claude/DevForgeAI/evals/brainstorm` and the source plugin identity.
- Destination: plugin **devforgeai 0.1.0**, containing **SKL-001 v6**, a Codex provider
  variant. Keeping SKL-001 preserves the original SPEC link; v6 records the port changes.
- Imported files: **56**, of which **35 are byte-identical** and **21 are adapted**.
  The BRN template, framework index, and diverge-converge framework are byte-identical.
- Candidate: **62 files**, excluding this report and retained import evidence;
  SHA-256 **`b740cd0d3a5227e9e9653a39e9cda418d02344d90fe452acbb6dc6d5c68ae9c3`**. The exact file list and digest rule are in
  [candidate-manifest.json](import-evidence/candidate-manifest.json).
- All **71 pre-existing inputs** captured before import still have their original bytes.
  Separate work added Claude PRD files during this task; they were preserved and not imported.
  The final readback finds the Claude PRD skill present and the Codex PRD skill absent.
- This workspace has no Git metadata, so a worktree, commit, and historical diff were unavailable.

## Intentional provider adaptations

These are explicit differences from a specification written for Claude Code, rather than
claims of literal conformance to its provider interface.

| SPEC-001 contract | Codex implementation | Assessment |
|---|---|---|
| §3: `.claude-plugin/plugin.json` | `.codex-plugin/plugin.json`, normalized `devforgeai` folder/name, `skills: "./skills/"`, real author and UI metadata | Supported plugin-creator compatibility package. |
| §5, BEH-01: slash command, `$ARGUMENTS`, `argument-hint`, Claude tools | Codex skill selection or `$brainstorm` in CLI; topic from the message; host file/shell/question tools; Claude-only frontmatter field removed | Intent preserved; trigger behavior not yet evaluated. |
| §5 automatic invocation | `agents/openai.yaml` explicitly sets `allow_implicit_invocation: true`; source trigger description retained | Static configuration verified. |
| BEH-03/08/09: `${CLAUDE_SKILL_DIR}` paths | Resources resolve from the actual loaded SKILL.md directory; BRNs resolve from the consuming project | No invented Codex path environment variable. |
| BEH-07/11, VER-03: `claude-code`, Claude session and resume semantics | `codex`, actual host model/task identity, Codex Change Log rows; prior Claude history retained | Necessary provider change. No Claude transcript-retention or resume guarantee is carried over. |
| BEH-10: `/devforgeai:prd BRN-NNN` | Available DevForgeAI Codex PRD skill, if supplied; otherwise explicit unavailable-workflow handoff | ID-only input and final `Next step` paragraph preserved. No PRD is generated. |
| QR-03, VER-01/06/07: Claude `Skill` events and tool allowlists | Explicit host trace reviews replace `tool_used: Skill`; Claude allowlists removed from case metadata | Definitions imported; no native Codex case runner supplied or executed. |

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

### D-02 — Native evaluation and runtime evidence are missing

The eight case prompts, VER tags, assertions, fixtures, and rubric intent are retained under
`evals/brainstorm/`. They are evaluation definitions, not a supported native Codex execution
format. Claude-specific load assertions became manual host-trace checks; the ordinary regex
and rubric definitions remain data. The 0.8-per-case, three-run, no-plugin-baseline criteria
are preserved in [the evaluation plan](evals/verification-plan.json), but **zero native
obligations are complete**. The ten passing Python tests below do not substitute for them.
VER-05 and the runtime parts of VER-09 also remain unrun.

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

### D-04 — Missing host identity is reported, not fabricated

BEH-07/VER-03 require the actual model and session identity. Codex does not always expose
both to a skill. The port uses the explicit `unknown` sentinel when needed, keeps the BRN
draft, and discloses incomplete provenance. This fallback **does not satisfy VER-03**.
The actual authoring task ID was available; the exact model identifier was not, so the
port's sidecar honestly records `model: "unknown"`. No source model ID was copied as if
Codex had authored with it. Provenance graders reject an unknown model or session.

### D-05 — Specification examples and measurement wording are stale

§5's proposed frontmatter still says `devforgeai-version: "4"` (line 124); the imported
Claude source is v5 and the Codex port is v6. QR-01 (line 212) still measures size using
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
| ERR-05 | Three-attempt limit, remaining errors, draft status | Preserved; runtime unrun. |
| QR-01 | 246-line skill; framework/output detail in references | Static size/layout checked; measurement wording D-05. |
| QR-02 | Sidecar; two quoted metadata values; matching IDs/versions; supported Codex frontmatter | Repository schemas and Codex validators pass. |
| QR-03 | Eight tagged definitions, three runs and baseline in plan | Definitions retained; execution/evidence gap D-02. |

## Complete native verification denominator

| Obligation | Case / required exercise | Status |
|---|---|---|
| VER-01 | writes-valid-brn | NOT_RUN |
| VER-02 | no-unconfirmed-dispositions | NOT_RUN |
| VER-03 | records-provenance | NOT_RUN |
| VER-04 | uses-named-framework | NOT_RUN |
| VER-05 | Add/select framework, remove it, verify fallback | NOT_RUN |
| VER-06 | ignores-unrelated-request | NOT_RUN |
| VER-07 | asks-for-topic | NOT_RUN |
| VER-08 | existing-brn, including unchanged-file bytes | NOT_RUN |
| VER-09 | Stop/save choices, three failures, static limits | NOT_RUN overall; static subset checked |
| VER-10 | hands-off-to-prd; present branch requires Codex PRD | NOT_RUN; scope discrepancy D-01 |

## Checks performed and delivery status

| Check | Result / evidence |
|---|---|
| Plugin-creator manifest/package validation | PASS; [raw result](import-evidence/plugin-validation-final.json) |
| Skill-creator quick validation | PASS; [raw result](import-evidence/skill-validation-final.json) |
| Skill frontmatter and provenance against repository schemas | PASS; [static checks](import-evidence/static-checks.json) |
| Provider validator and imported-grader regressions | **10 tests passed**, including standard-library-only execution; [raw result](import-evidence/validator-regressions-final.json) |
| Local skill/reference links | 6 checked, all resolve within the package |
| Imported regex definitions | 21 compile; this does not grade native traces |
| Source preservation | 71 captured input hashes unchanged; concurrent additions listed separately |
| Independent validation | NOT_PERFORMED; this report and checks were authored by the importing agent |
| Native behavior / framework acceptance | NOT_RUN / NOT_EVALUATED |
| Marketplace / installation / deployment | NOT_PERFORMED |

Reproduce the focused tests from the repository root:

```bash
python3 -B -m unittest discover -s src/codex/devforgeai/tests -p 'test_*.py' -v
```

[Final import manifest](import-evidence/final-import-manifest.json) and
[final source comparison](import-evidence/claude-to-codex-final.patch) record every imported
file. Initial import receipts and the first eight-test run are retained alongside the final
checks. Existing Claude source, deployment state, approved specifications, and user documents
were not edited by this import.
