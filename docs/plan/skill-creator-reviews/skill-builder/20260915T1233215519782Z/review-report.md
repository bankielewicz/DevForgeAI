# Skill-builder: focused skill-creator review

## Result

**Focused validation: FAIL. Broader skill qualification: INCOMPLETE.**

Reviewed development package `C:\Projects\DevForgeAI\src\agents\skills\skill-builder` through the user-selected skill-creator guidance. This is a bounded review, not a full skill-validator campaign. No repair, installation, operational update, or framework acceptance was performed.

Source package digest: `ecb01ece2c38443e58fe7a5b307e9d0de22a1fa9b9ec1f726b79cfa328cb9c9e`.

## Confirmed finding: design checks can be bypassed by switching staged mode

The normal design checks reject changed original design, changed captured design, and missing capture records. However, `scripts/authoring.py:282-288` trusts the editable `design_capture_requested` flag in origin.json: false with no capture binding/file returns before checking the captured design.

Independent reproduction:

1. Begin a fresh design-enabled authoring run and stage a valid candidate.
2. Change origin.json's `design_capture_requested` to false and remove `design_capture_ref`.
3. Move design-capture.json aside, retaining its bytes, and change the captured design at inputs/1.
4. Publish once.

Expected: reject publication before target delivery, with no successful baseline. This is required by SBP-011/SBPV-11 in `docs/specs/skill-builder-postmvp-spec.md` and the package's evidence-format.md.

Observed: `AUTHORED`, `applied_paths: ["SKILL.md"]`, no issues; target written, authoring baseline emitted, publication-readback.json marked `PUBLISHED`. The original design and supplied contract were not rewritten. This is an ordinary custody-integrity failure, not a claim that these editable records provide a protected security boundary.

Evidence: [independent test](test_publication.py), [executed failure](publication-tests.stderr.txt), and [retained publication](fixtures/test_legacy_mode_downgrade_cannot_hide_changed_design_snapshot/docs/plan/one/publication-readback.json). Original literal paths are retained in [fixture-paths.jsonl](fixture-paths.jsonl). Archived fixtures preserve original absolute references; they are evidence copies, not relocated runnable stages.

Recommended repair direction: independently bind the staged design selection and origin before publication dispatch; validate that binding before selecting legacy behavior or writing targets/baselines. Preserve genuine no-design compatibility and retain incompatible old stages. This is a proposal only; no repair was applied or retested.

## Executed checks

| Check | Result |
| --- | --- |
| Skill-creator quick_validate.py | PASS, exit 0 |
| Exact package manifest | PASS; no missing, extra, or mismatched artifact |
| Local Markdown file links and Python parsing | PASS |
| Independent publication cases | 7/8 PASS (87.5%); 1 failed assertion, 0 errors/skips |
| Independent authoring trial | Completed: begin/publish exit 0, AUTHORED/PUBLISHED |
| Full-package Python line coverage from focused tests | 390/2264 = 17.226148409893995%; below 95% |
| Source/operational preservation | See final-preservation.json; both unchanged |

The eight independent cases cover normal design publication, no-design compatibility, original-design drift, captured-design drift, missing capture, combined mode downgrade, requirement-source drift, and focused editing that preserves unmanaged bytes. Assertions check actual returned state, delivered bytes, quality state, and publication artifacts. No mocked product behavior or weakened assertions were used. The failed case was retained without retry.

Coverage denominator includes all eight Python files shipped in the package, including the runtime asset and locally adapted scaffolding helpers; no excluded lines. Coverage's initial directory report found only imported modules. [Full-source accounting](full-source-coverage.json) adds unimported files at zero coverage using the same execution data, without rerunning tests. Full-package branch coverage is NOT_RUN; coverage.json contains branch data for the two measured modules. These focused cases do not represent the full required skill suite or prove that uncovered behavior is defective.

## Independent forward trial and instruction review

An independent agent received a realistic meeting-notes skill authoring request, the selected builder, and an isolated temporary project. It received no suspected bug or intended answer. It delivered one SKILL.md, a completed external design, authoring records, baseline, and manual validation handoff. Parent review read the entire resulting skill and verified publication references and candidate/delivered equality; see [trial report](forward-trial.md) and forward-readback.json.

The generated instructions preserve the requested Action/Owner/Due date columns, absent-value literals, uncertainty, chat default, and explicit file destination. They introduce no external services or unnecessary helpers. The builder entrypoint routes branch-specific references and clearly distinguishes authoring from evaluation. These are instruction/artifact observations; the generated skill was not executed.

The trial is an explicitly directed subagent invocation, not proof of native implicit discovery or a cold Codex CLI campaign. One report-composition tool call failed before shell execution and is disclosed in the trial report; authoring publication was not retried.

## Environment, evidence, and limits

Windows native filesystem at C:\Projects\DevForgeAI, PowerShell, `C:\Program Files\Python310\python.exe` 3.10.11, coverage.py 7.9.0. No Git metadata. Test command ceiling 120 seconds; test execution completed in about four seconds. Exact argv, cwd, exit codes and elapsed times are in [command-receipts.json](command-receipts.json). Additional accounting command: `python -B -X utf8 docs/plan/skill-creator-reviews/skill-builder/20260915T1233215519782Z/complete_coverage.py`, exit 0.

Full legacy/adaptive/import/adoption regressions, Linux behavior, native implicit activation, generated-skill execution, full end-to-end qualification, and Rust framework acceptance were not evaluated. The failing mandatory custody scenario and unmet measured floors prevent a pass. No red/green repair cycle is claimed because this task did not change production code.

All current findings above were verified in this run. Prior memory only guided investigation of the custody area; historical outcomes were not counted as fresh evidence. Existing source, operational skills, and historical evaluation evidence were preserved. New receipts, original-byte fixture archives and an evidence manifest are retained in this run directory.
