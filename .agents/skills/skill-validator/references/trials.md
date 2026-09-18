# Trials and retained attempts

### SV-008/SV-014

Write the trial plan before execution: case ID, tested requirement, fixture inputs and digests, expected outputs/side effects, executor, command or task prompt, timeout, and permitted write root. Expected outcomes come from the selected contract or explicit user outcome, not from whatever the implementation produced. Include a positive and a relevant failure/boundary case for each changed or suspect script/interface; do not impose an arbitrary universal trial count.

Use synthetic, non-sensitive fixtures in `trials/<case-id>/`. Never run the selected skill against canonical project data simply to test it. Invoking scripts requires inspection of the script and relevant dependencies. No new dependency installation, credential use, live network service, external message, or production mutation is implied. Read-only documentation refresh is separately allowed. If available isolation cannot contain the planned effects, do not execute that case; continue static review and record the limitation.

Default short local utility commands to 120 seconds and whole native skill sessions to 600 seconds, overridable by an explicit recorded trial requirement. Use the sealed runner and progression rules in [reliable evaluation](reliable-evaluation.md). This is a development execution ceiling, not a confidence ritual. Record command, cwd, environment identity, start/end time, stdout/stderr or accurately labeled combined output, exit/timeout result, artifacts, and before/after side-effect observations. Record retries as new attempts; preserve failures.

Where the host offers an appropriate Codex task runner, exercise the workflow from minimal inputs without injecting intended fixes into its prompt. Otherwise mark native workflow execution unperformed and retain script trials or a manual walkthrough as separate evidence. Lack of a runner does not block package inspection or report generation. Execution that is required to substantiate a workflow claim cannot be replaced by an invented PASS.

On interruption, preserve completed stage artifacts and identify the next unfinished action. Resume only if original input identities and hashes still match; otherwise allocate a fresh run linked to the prior run. Do not silently restart failed trials or label a partially produced report complete.

## Trial records

Before each attempt, save `trials/<case-id>/plan.json` with schema_version, case_id, requirement_ids, fixture references, expected outputs and effects, executor, exact command or task prompt, timeout_seconds and permitted_write_root. Snapshot the evaluator's package/input bytes and copy its exact case definition before execution. Record expected observations independently from implementation output. Save `attempt-001.json`, stdout/stderr files, before/after manifests and readback. Increment attempt names without replacing failures. A timeout preserves partial output and names the unfinished action.

Use separate Codex agents for independent reviews where the selected build task requires them; ordinary validation can use one primary agent. A cold workflow task receives only the selected skill entrypoint, minimal raw inputs, user outcome and authorized scope. Keep evaluator expectations out of that prompt. An agent's assigned path boundary is not OS-enforced isolation; inspect before/after effects.

Routing uses predeclared positive and near-miss prompts. Have an independent agent classify from the description without the expected labels, then compare actual labels. Record native implicit invocation NOT_RUN unless the host actually selected the skill through discovery. Explicitly loading a file is not that observation.
