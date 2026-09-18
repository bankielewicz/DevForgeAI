# Reliable independent evaluation

Load this reference when planning script-interface checks, native workflow trials, incomplete campaign recovery, or comparisons. The [standards catalog](../assets/standards-catalog.json) distinguishes format requirements, selected host behavior, semantic guidance and advisory measurements. Source digests identify the supplied dated material; retrieve and bind current applicable sources before changing a campaign's rules. Never mix newly fetched rules into already-scored cases.

## Standards and resource checks

Run the existing `observe.py structure` and `adaptive_observe.py package` interfaces against captured bytes; they share `scripts/skill_format.py` for core metadata rules. Keep each helper's scope and raw output. The Agent Skills specification defines `allowed-tools` as a space-separated string while Claude Code also accepts a YAML list; the required rows accept both and `skill_format.advisory_checks` reports the list form as a portability divergence, never a defect. The ASCII name check is the selected Claude Code-compatible profile; Unicode ambiguity in a source requires an explicit applicable profile, not silent normalization. Unknown fields stay unresolved until selected host documentation supports them. The installed creator checker remains a named compatibility observation, including its known rejection of Agent Skills `compatibility`.

Use `python scripts/standards_observe.py --source <captured-package>` for supplemental advisory size/depth/cycle measurements. Cycles and long entrypoints are review locations, not automatic defects. This command does not execute target scripts, follow remote links, or assign semantic quality. Relative locators inside Markdown resolve from the containing file. Keep legitimate assets, quoted placeholders and Unicode controls under contextual review.

For inspected declared script interfaces, predeclare valid input, missing/invalid arguments, closed stdin, expected stdout/stderr, exit behavior and permitted side effects. Run `--help` only where the interface promises it. Do not execute every discovered script or require CLI flags from import-only modules. No installations or external effects are implied.

## Recorded trials

The supplemental [trial schema](../schemas/trial-plan-v1.schema.json) describes `scripts/trial_runner.py`. Its commands are terminal accessible:

```text
python scripts/trial_runner.py seal --plan <absolute-plan.json> --attempt <fresh-absolute-attempt-directory>
python scripts/trial_runner.py run --attempt <same-attempt-directory>
python scripts/trial_runner.py check --attempt <same-attempt-directory>
python scripts/trial_runner.py summary --cases <absolute-case-inventory.json>
```

Resolve scripts from the loaded validator package. Plans and attempt evidence must stay outside the disposable write root. Protected fixture inputs may be inside it: digest-bind the candidate, specifications and supplied tests, and require them unchanged. Keep evaluator assertions outside the actor's root/context. `inputs` must include every immutable file needed to identify the scenario, not just a convenient entrypoint. Native argv must use actual discovered host options and existing model/authentication; do not add sandbox bypasses. Every native scenario needs observable output or independently graded semantic obligations. Utility completion is only utility evidence.

`seal` captures the exact plan and binds original inputs. `run` rejects missing/changed plans or reused attempts, launches a gated Windows worker inside an owned Job Object, streams logs to disk, and records start/final receipts and before/after manifests. Windows Jobs contain process lifetime, not file access: host sandboxing and authorized scope still govern effects. Unexpected changes are assessed against the selected effect contract; the runner records them without issuing mutation authority. If capture excludes material paths, report incomplete side-effect coverage.

Utilities default to 120 seconds. Whole native skill tasks default to **600 seconds**. A positive finite `timeout_seconds` records an explicit selected limit. Preserve current user ceilings and authorization; do not silently extend/retry. The timeout starts when the owned worker receives its payload; elapsed receipt time also includes setup/cleanup. A timeout alone is NOT_RUN, not a target bug. Nonzero exit needs diagnosis before assigning a source finding. Missing required output after otherwise successful completion is a failed mechanical obligation.

For `expected_outputs`, declare relative path, requirement ID, and `exists`, `text`, `json`, or `manual`. Text/JSON assertions include the independently selected `value`. `manual` remains NOT_RUN until a separate evidence-backed semantic assessment; never edit the raw receipt to promote it. File existence alone cannot establish content quality. `check` rechecks original inputs, captured plan, stream/artifact bindings, timestamps, output grading and directory state. These editable receipts are not protected provenance.

Dependencies use case IDs and `dependency_attempts` mapping each ID to its qualified attempt. The summary inventory is a nonempty array of `{case_id, attempt, dependencies}`; `attempt` is null for unperformed cases. Derive the complete inventory from selected requirements before scoring. Duplicate cases/executions, missing prerequisites and dependency omissions are rejected. The checker can validate supplied inventory consistency, but cannot infer requirements the evaluator omitted from it. Keep controls, unit tests and native scenarios in separate inventories.

## Recovery and campaign progression

After timeout or interruption preserve logs, owned process state and partial artifacts. A start without a final receipt is unresolved; never rerun that directory. `check` may expose changed inputs without erasing the retained attempt. Select a new attempt only under applicable authorization, rechecking identity and owned-state cleanup. A successful Job cleanup must be observed; failed/uncertain cleanup blocks dependent work. Other platforms are NOT_RUN for this Windows-first adapter.

Proceed with independently ready cases after localized environment/harness gaps. Do not end a whole campaign merely because one pilot timed out. Name the shared safety/identity/authorization blocker or selected exhausted campaign limit when no more work can continue. Ask only for the unresolved additional budget/effect where required and continue permitted independent inspection/fixture work. Record the next unfinished action.

## Forward-testing, routing and comparisons

Fresh actors get the selected skill, realistic user request, raw artifacts and permitted effects; never the answer, proposed correction or evaluator conclusions. Derive assertions independently and freeze them before launch. Exploratory trials can inform the next iteration but cannot be retroactively scored using newly fitted expectations. A separate subagent/session is a held-out context, not proof of model or OS isolation. Disclose inherited host configuration and observed selection.

Grade concrete delivered artifacts, meaningful invariants, scope preservation and failure/recovery behavior. Add representative positive and adverse requests for changed branches. Description-only classification is separate from native implicit discovery; predeclare realistic positive/near-miss prompts before the reviewer starts. Do not inject outcome labels into the reviewer prompt.

Optional comparisons use a user-selected previous version or no-skill baseline, matched raw inputs, host/model, budgets and independent workspaces. Verify the no-skill branch cannot discover the target locally; disclose inherited/global discovery uncertainty. Blind artifact labels for qualitative comparisons when practical. Report duration and actually available usage data, not estimated tokens. Retain individual observations; do not replace mandatory conformance with an aggregate preference score or automatically run more paid trials. Neither comparison nor validation repairs source.

## Delivery and accounting

Lead with the requested outcome's status, then distinguish structural checks, grader tests, actual behavior, routing and unperformed obligations. Reports and fix/proposal paths must exist and be read back, or be named explicitly as undelivered. A completed report may describe an incomplete campaign, but cannot describe unfinished native work as assessed. The independent evaluator must still bind a Python JSONL bundle, fixtures, expected results, schemas and runtime information to exact source/specification bytes. All results remain evidence; compiled Rust retains protected framework authority.
