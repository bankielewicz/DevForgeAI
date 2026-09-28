# Documents Updater Codex import report

Ported Claude SKL-005 v1 into the existing Codex `devforgeai` plugin as SKL-005 v2.
The plugin manifest is 0.2.0. Authority: approved SPEC-006 v1, at base commit
`27b7c917f5083e798e322e556f3b1d68df09b84f`.
The source and specification are unchanged. Work was authored in the isolated
`codex/documents-updater-port` worktree.

## Candidate and source correspondence

[Source baseline](import-evidence/documents-updater-20260928/source-baseline.json) records
SHA-256 values for the Claude skill, its tests and evals, SPEC-006, and Brainstorm runtime.
The 21-file [frozen matrix plan](import-evidence/documents-updater-20260928/matrix-plan.json) binds
the evaluated Documents Updater runtime plus plugin manifest to:

`6db9f222372adc2618f9e3050c9d329160de90449b6a617a153907fdb6c7a9f3`

The digest hashes sorted `path + NUL + file SHA-256 + newline` rows. It is the
Documents Updater evaluation candidate identity, not a digest of all plugin development
evidence or the Brainstorm runtime. The checker, twelve templates and three unaffected
references are copied byte-for-byte. SKILL.md, scope-and-evidence.md and provenance
contain the provider adaptations; agents/openai.yaml is new.

## Discrepancies against SPEC-006

| ID | Specification | Codex result and disposition |
|---|---|---|
| DU-01 | §3, §5: Claude provider layout, slash command, Read/Glob/Grep/Bash/Write/Edit | Uses src/codex/devforgeai, native skill discovery, invocation text, exec_command/rg and apply_patch. Intentional provider adaptation; workflow unchanged. |
| DU-02 | §5, BEH-17: AskUserQuestion | Uses native request_user_input when available and permitted; plain-text fallback preserves unresolved questions. Required clarification may use plain text under Default mode restrictions. |
| DU-03 | §5, QR-02: argument-hint and $ARGUMENTS | Claude-specific argument-hint removed; optional revision/range/propose text retained. Codex UI invocation metadata lives in agents/openai.yaml. Both repository schemas and Codex validators accept the port. |
| DU-04 | BEH-03 and source scope reference: captured session-start state | Corrected the Claude-specific claim of an automatic start snapshot. Codex uses only a snapshot actually recorded before the work. It never substitutes the documentation request's snapshot for the base. |
| DU-05 | QR-03, §9: claude plugin eval and tool_used: Skill | Native Codex app-server trials replace Claude execution; actual SKILL.md loads replace the Skill-tool grader. Source prompts, fixture contents and content graders are preserved. Semantic grading is separately recorded. |
| DU-06 | §4: new files in docs/topic.md except README/CHANGELOG | Source also allows root CONTRIBUTING.md and numbered docs/adr files. Retained for import fidelity; SPEC-006's fallback-path description omits those exceptions. This discrepancy is inherited. |
| DU-07 | §11: deploy, then perform VER-10–12 | Source import only. No installation/deployment or owner acceptance was performed. All three manual obligations remain NOT_RUN; supplemental fixture runs do not satisfy them. |
| DU-08 | §9: recorded Claude scores and deployment status | Historical Claude results are not Codex qualification. The native results below apply only to this candidate and runtime. |

## Requirement coverage

Static correspondence means the instruction is present; it does not establish every
possible runtime behavior.

| Requirements | Port location and verification |
|---|---|
| BEH-01–04; ERR-01–03 | Workflow step 1 and scope-and-evidence.md; native baseline/no-commits cases, proposal guards and supplemental invalid-revision check |
| BEH-05–07 | Workflow steps 2–3; evidence grouping and unsupported-claim cases |
| BEH-08–10; ERR-04–05 | document-selection.md, twelve assets; README creation and out-of-diff configuration updates |
| BEH-11–13 | output-rules.md and writing-standards.md; release-history and content graders |
| BEH-14; ERR-07 | Governed-document protections retained; owner VER-12 remains NOT_RUN |
| BEH-15; ERR-06 | Unchanged check_docs.py, 23 unit tests, native validation traces and supplemental repeat check; three-repair failure path is not separately exercised |
| BEH-16–18 | Scope/write limits, question adapter and completion response; exact file/index/HEAD/ref guards plus positive/negative activation |
| QR-01–02 | Entrypoint remains under 300 lines; four linked references; matching SKL-005 version 2; frontmatter and provenance schemas pass |
| QR-03; VER-01–09 | Eight native cases with no-plugin baseline, three repeats; checker unit suite |
| VER-10–12 | NOT_RUN: real-session/deployed-skill owner checks remain outstanding |

## Evaluation

Native runtime: **Codex CLI 0.158.0**, model **gpt-6-astra**, using ephemeral source-loaded
skill threads. All **48/48** frozen trials completed: eight cases × three repeats × two
arms, with **zero run errors**. Every plugin case met the 0.8 threshold in every run.

- Plugin content mean: **1.000**; no-plugin mean: **0.690**; mean difference: **+0.310**.
- All source graders plus activation/preservation guards: **24/24 plugin**, **5/24 baseline**.
- All **23 Documents Updater checker tests** and **33 combined Codex tests** pass.
- Package, skill, frontmatter, provenance and report Markdown checks pass. Authored-source
  whitespace checks pass; a full diff check flags intentional hard breaks and blank lines
  in retained native replies/fixtures. Those evidence bytes were preserved.
- Positive skill loading: **21/21**; unrelated-request nonactivation: **3/3**.
- Every changed plugin Markdown file was checked by the bundled validator. Trace audit
  found no foreign trial paths or evaluation-artifact reads, and all 24 trial candidates
  retained their bound runtime bytes. This audit does not establish OS-level isolation.

| Obligation | Case | Plugin scores (three runs) | No-plugin scores |
|---|---|---|---|
| VER-01 | updates-readme-and-changelog | 1.00 / 1.00 / 1.00 | 0.857 / 0.857 / 0.857 |
| VER-02 | proposal-mode-no-edits | 1.00 / 1.00 / 1.00 | 0.750 / 0.750 / 0.750 |
| VER-03 | no-change-when-accurate | 1.00 / 1.00 / 1.00 | 0.000 / 0.000 / 0.000 |
| VER-04 | no-unsupported-claims | 1.00 / 1.00 / 1.00 | 1.000 / 1.000 / 1.000 |
| VER-05 | preserves-release-history | 1.00 / 1.00 / 1.00 | 0.917 / 0.917 / 0.917 |
| VER-06 | asks-for-unknown-baseline | 1.00 / 1.00 / 1.00 | 0.000 / 0.000 / 0.000 |
| VER-07 | creates-readme-from-profile | 1.00 / 1.00 / 1.00 | 1.000 / 1.000 / 1.000 |
| VER-08 | ignores-unrelated-request | 1.00 / 1.00 / 1.00 | 1.000 / 1.000 / 1.000 |

The score includes the specified completion-response contract; it is not a general
measure of writing quality. The baseline's unknown-scope runs guessed a comparison
point, its no-change runs documented internal refactors, and its release-history runs
omitted the required breaking marker. Some baseline runs also left Python cache files.
A 0.8 score does not waive any of those failed obligations.

[Full grades](import-evidence/documents-updater-20260928/matrix-grades.json),
[summary and all twelve obligation statuses](import-evidence/documents-updater-20260928/evaluation-summary.json),
and [trace audit](import-evidence/documents-updater-20260928/trace-audit.json) are retained.
The semantic unknown-baseline grader was assessed from actual replies and files by the
authoring Codex session, separately from each native trial. This is not an independent
owner acceptance review.

Three [supplemental native checks](import-evidence/documents-updater-20260928/supplemental-assessment.json)
pass: native request_user_input in Plan mode; proposal → apply → repeat without churn;
and blocking an invalid revision without writes. Two smoke trials also pass. These
controlled fixtures do not satisfy manual VER-10–12.

Initial smoke grades incorrectly treated the final Git command's expected exit 1 as
a validator failure; the checker itself printed success. The grader was corrected
before the matrix and the initial record retained. The initial schema call supplied
unwrapped provenance; validation passed with the schema's required frontmatter wrapper.
Neither correction changed the evaluated skill.

## Delivery limits

The runtime uses Python 3 for the checker and requires no packages or network for that
check. Evaluation tooling additionally uses PyYAML and an authenticated Codex runtime.
Provenance remains draft; exact authoring model/session identifiers were not exposed
and are recorded as unknown. Runtime trial model IDs are recorded separately.

No approved spec, deployed Claude copy, installed Codex plugin, marketplace, or
Brainstorm skill was modified. The existing historical Brainstorm report and evidence
remain tied to their earlier candidate.
