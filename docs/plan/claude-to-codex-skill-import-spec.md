# Claude-to-Codex Skill Importer Specification

Status: development skill specification, amended to require Python structural checks and deterministic evaluation build artifacts. Importing an existing project skill and operational installation remain outside this build task.
Recorded: 2026-09-11 America/New_York.
Target host observed during research: Windows PowerShell, Codex CLI 0.154.0.

## 1. Purpose and authorized deliverable

Specify a Codex skill that imports a selected Claude skill package and converts it into a usable Codex CLI skill. Import means semantic conversion of the complete package, not copying or renaming SKILL.md.

The authorized deliverable is the development skill `skill-builder` and its required evaluation artifacts. The user subsequently authorized building it and explicitly required Python evaluation. That correction supersedes the earlier author-only restrictions. Running the importer against an existing project skill is a separately requested task; building and testing the importer with disposable fixtures does not select such a skill for conversion.

Companions:

- [Compiled-Rust enforcement design](devforgeai-codex-rust-enforcement-design.md).
- [Research and command log](claude-to-codex-skill-import-research-log.md).
- [Mandatory evaluation implementation and command log](skill-builder-mandatory-evaluation-log.md).

Importer source: `src/agents/skills/skill-builder/`, using the user's selected name. Operational skills belong in `.agents/skills/`. Source edits do not update operational copies. Do not use symlinks or automatic synchronization to erase this separation.

### Scope and exclusions

- One selected local skill directory per import invocation; no batch migration in the first version.
- Account for every package file, including references, templates, schemas, assets, and ordinary supporting scripts.
- Preserve source files and record their hashes.
- Write converted packages only under `src/agents/skills/` in the explicitly identified target project.
- No operational installation, hook registration, runtime activation, plugin publication, or Git publication.
- No new semantic importer CLI: the importer is a Codex skill guiding semantic conversion through terminal capabilities. Its required Python runner only executes deterministic evidence checks.
- No read, execution, copying, wrapping, or porting of excluded legacy CLI/hooks. The explicitly excluded CLI is `\\wsl$\Ubuntu\home\bryan\Projects\DevForgeAI2\.claude\scripts\devforgeai_cli`.
- Do not read or review the backup folder. Restrict discovery to selected permitted roots; do not perform an unrestricted repository crawl.
- A dependency mention in an allowed skill file may be recorded without following it into excluded code.
- Design the new DevForgeAI enforcement runtime in compiled Rust; do not implement it in this task.

## 2. Research basis and limits

The following primary sources were retrieved during planning. Their conclusions inform this specification; they do not establish that a target installation has passed qualification.

1. [Agent Skills specification](https://agentskills.io/specification): common entrypoint/frontmatter and resource conventions; optional `allowed-tools` support varies by host. Shared formatting is not a guarantee of shared execution semantics.
2. [Codex skills](https://learn.chatgpt.com/docs/build-skills): repository discovery in `.agents/skills`, progressive disclosure, and optional `agents/openai.yaml` metadata/invocation policy.
3. [Claude skills](https://code.claude.com/docs/en/skills): Claude-specific invocation flags, argument substitution, model configuration, forked agents, and hooks need explicit host mapping.
4. [Codex hooks](https://learn.chatgpt.com/docs/hooks): hooks have event-specific behavior, trust requirements, concurrency, and coverage limits. They are not a complete enforcement boundary.
5. [Evaluation best practices](https://developers.openai.com/api/docs/guides/evaluation-best-practices): evaluate outcomes with representative, edge, and adversarial cases; calibrate subjective judgments with human examples.
6. [Graders](https://developers.openai.com/api/docs/guides/graders): executable Python graders are an evidence/scoring mechanism. This design does not require hosted grading, fine-tuning, or an OpenAI API integration.

Also considered: the supplied local `docs/codex/prompt-engineering.md`, `model-guidance.md`, and `citation-formatting.md`; installed OpenAI Docs and Skill Creator instructions; targeted reads of source skills. Planning did not review every file in any source package. Complete package inspection is a requirement of a later authorized import.

Before relying on a host-specific capability, check installed guidance or CLI help and consult current official documentation when local evidence does not resolve its behavior. Record the exact target CLI version. Changes to host behavior must be reflected in the capability map rather than assumed compatible.

## 3. Importer contract

### Inputs

Required: an explicit source skill directory and an identified target project root. The current project root may be used when it is unambiguous from the session.

Optional: a requested target name and an explicit instruction to revise an existing converted package. Without revision authorization, an occupied destination stops the import before edits. Do not silently rename to evade a collision.

The source must contain a readable SKILL.md. Resolve the source and target roots before reading package contents. Do not follow directory junctions/symlinks into excluded or unrelated locations; record such dependencies and seek a specific scope decision if essential.

Use the source's valid skill name by default. Normalize an invalid name to lowercase words separated by hyphens only when the intended identity is unambiguous, and record the mapping. Ask a focused question if competing interpretations or destination conflicts affect identity.

Example invocation, not executed by this build task:

```text
Use $skill-builder to convert the skill at <source-directory>
into this project's src/agents/skills. Do not install it.
```

### Outputs

The package contains only resources needed by the converted skill:

```text
src/agents/skills/<target-name>/
  SKILL.md
  agents/openai.yaml       # only when invocation/UI/dependency metadata is needed
  references/             # retained or consolidated domain guidance
  assets/                 # retained output templates/resources
  scripts/                # only authorized, available, verified helpers
```

Optional directories are not scaffolded when empty. Existing useful structures such as `phases/` may be retained as domain organization; directory names do not establish authoritative phase control.

Import evidence is separate:

```text
docs/plan/skill-imports/<target-name>/<UTC-timestamp>/
  source-manifest.json
  source-after-manifest.json
  file-dispositions.json
  conversion-report.md
  command-log.md
  destination-manifest.json
  evaluation-cases.jsonl
  evaluation-results.jsonl
```

Use a timestamp precise enough to avoid collisions; if occupied, stop and select a fresh timestamp before writing. These files record conversion evidence, not protected framework acceptance.

### Reported states

Report independent facts rather than one overloaded PASS:

- Conversion: `NOT_STARTED`, `IN_PROGRESS`, `COMPLETE`, or `BLOCKED`.
- Structural checks: `NOT_PERFORMED`, `PASSED`, or `FAILED`, with commands/evidence.
- Deterministic evaluation: `NOT_PERFORMED`, `PASSED`, or `FAILED`, with bound artifacts, JSONL observations, and execution errors.
- Behavioral evaluation: `NOT_PERFORMED`, `PASSED`, or `FAILED`, with case outcomes.
- Framework enforcement: `NOT_IMPLEMENTED` until an actual runtime is implemented and qualified.
- Operational installation: `NOT_PERFORMED` for this importer workflow.

`COMPLETE` requires the declared conversion scope, successful Skill Creator structural validation, successful required deterministic cases, and meaningful execution checks for new or changed scripts. Missing artifacts, missing checks, failed required observations, or execution errors prevent reporting build completion. Behavioral task evaluation is reported separately: passing deterministic fixtures does not prove semantic conversion behavior. Neither result establishes installation or DevForgeAI acceptance.

## 4. Importer procedure

### A. Establish scope and inventory

1. Confirm source, target root, exclusions, revision authorization, and current host capabilities.
2. Record the CLI version, OS/shell, source path, destination path, and available tool capabilities. Do not change runtime configuration to manufacture compatibility.
3. Inventory every allowed file, recording relative path, size, and SHA-256. The source manifest is the baseline for readback.
4. Create the evidence directory after the import request authorizes conversion. Source inspection alone is not permission to execute source commands.

Outcome: an explicit package boundary and unchanged source baseline.

### B. Understand the complete package

Read the selected entrypoint and all supporting textual files. Inspect binary assets by appropriate metadata or rendering when their content affects conversion. Do not discard files solely because the entrypoint fails to link them.

Trace callers and dependencies for each resource. Identify tools, named agents, nested skills, shell assumptions, argument substitution, permissions, output schemas, persistent state, and side effects.

Assign each source file a disposition:

- `PRESERVE`: copied unchanged with destination hash evidence.
- `REWRITE`: adapted while preserving its useful role.
- `CONSOLIDATE`: merged into named target resources.
- `OMIT`: unnecessary or ceremonial content removed with a reason.
- `DEFER`: excluded implementation or essential incompatibility recorded outside the executable skill.

Each entry includes source hash, target path(s), rationale, affected behavior, and verification method. Account for references inside omitted files so omission does not break another consumer.

Outcome: every file and material dependency has a disposition; nothing is silently lost.

### C. Extract the behavioral contract

Write the purpose, activation boundary, inputs, outputs, non-obvious domain rules, required user decisions, side effects, and recovery behavior in the conversion report before rewriting.

Classify source instructions as domain knowledge, interface contract, host-specific mechanism, real permission boundary, duplicated ceremony, or unsupported assertion. Preserve meaningful requirements; do not preserve broken enforcement claims merely for textual fidelity.

Preserve compatible output schemas by default. If an essential behavior cannot be represented without a breaking contract change, stop and present the specific incompatibility. Do not invent fields, quietly relax required properties, or assert that downstream consumers remain compatible without checking them within scope.

Outcome: a traceable specification of what the converted skill must actually do.

### D. Map Claude behavior to Codex CLI

| Source feature | Required treatment |
| --- | --- |
| `name`, `description` | Preserve identity and rewrite discovery text around the real capability and activation boundary. |
| `model`, `effort` | Remove Claude-specific overrides; use the configured Codex session unless the user explicitly requests a supported override. |
| `allowed-tools` | Record required capabilities; never present copied metadata as enforced Codex permissions. |
| `AskUserQuestion` | Use ordinary terminal conversation for required input; do not depend on a mode-specific question tool. |
| `Read`, `Glob`, `Grep` | Express concrete reading/search operations through available host tools; prefer `rg` for search. |
| `Write`, `Edit` | Use supported Codex editing or shell operations with explicit paths. |
| Slash commands and `$ARGUMENTS` | Convert to Codex skill invocation plus explicit user-supplied input; do not assume Claude's substitution engine exists. |
| `.claude/skills/...` | Resolve package resources relative to the loaded skill; keep project artifacts relative to the identified project root. |
| `Task`, `context: fork`, named agents | Preserve the underlying task. Use the main session unless the user authorizes delegation and the target supports it. Essential isolation without an available equivalent is a blocking incompatibility. |
| Nested `Skill` calls | Use a verified available dependency, or preserve the handoff as an artifact. Do not pretend unavailable skills can run. |
| Dynamic shell injection | Replace with an explicit, authorized operation if required; never execute it while inspecting source. |
| `disable-model-invocation: true` | Preserve explicit-only intent through supported Codex invocation metadata; document semantic differences. |
| `user-invocable: false` | Do not invent a Codex equivalent. Record the mismatch and obtain a decision if the restriction is essential. |
| Claude hooks / legacy CLI | Record desired properties for the Rust design; do not port implementation or leave dead calls in converted instructions. |

Use PowerShell-compatible examples for the observed Windows target. Do not paste Bash syntax into a PowerShell command. Avoid globally replacing the word Claude: names, citations, or domain content can legitimately retain it.

Outcome: an explicit capability mapping with no hidden host dependency.

### E. Remove ceremony and restructure

Remove ritual question counts, unsupported context-percent thresholds, redundant banners, repeated MUST/HALT wrappers, hidden rubrics presented as proof, and model-authored completion markers presented as authority.

Retain concise instructions that affect decisions or output quality. A useful instruction describes an action, a real constraint, or a meaningful branch; it does not merely demand that the model declare compliance.

Keep the entrypoint focused on purpose, inputs, outputs, essential choices, and resource routing. Move substantial conditional domain content into references. Do not add fixed headings or length targets solely to satisfy a checker.

Inspect templates as carefully as instructions. Remove fictitious commands, assumed installations, obsolete scaffold actions, and unsupported promises from generated output. Do not initialize projects simply because a legacy template includes that behavior.

Outcome: the complete converted package, not only SKILL.md, contains useful and executable guidance.

### F. Produce a usable draft workflow

The selected skill must work within the available Codex CLI terminal capabilities. It may produce domain drafts without framework acceptance when that fulfills the agreed scope. It must not invoke proposed Rust commands or claim future gates are active.

Preserve real user answers. Reuse supplied facts rather than asking ritual questions. Record corrections without treating an older checkpoint as superior to a current explicit user correction. Save recoverable work at material updates; do not fabricate conversation history.

Report missing information and partial outputs honestly. If the original artifact schema has a suitable draft state, use it. Otherwise document a draft outside the acceptance contract rather than silently redefining status semantics.

If an essential dependency cannot be replaced using available capabilities, report `BLOCKED`. A dead instruction plus a warning is not a working conversion.

Outcome: a coherent development package with accurately limited behavior.

### G. Evaluate and hand off

Read back generated files. Check all local references, disposition coverage, capability mappings, changed schemas, unsupported tokens in executable contexts, and remaining ceremony. Rehash the source and destination. Treat byte changes to source as an error requiring investigation, not an expected side effect.

Python structural validation and deterministic evaluation are mandatory parts of the development workflow. Locate the installed Skill Creator `scripts/quick_validate.py` and execute it against the completed candidate. Execute the bundled JSONL runner using the documented case format and required manifest-bound artifacts. The structural checker verifies skill packaging; neither it nor the Python graders implement a DevForgeAI validator or acceptance decision.

Exercise new or changed scripts using disposable inputs with bounded local side effects. Inspect source commands before execution. A conversion request does not authorize operational installation, external service use, or mutations outside the declared development/evidence paths. If a required check needs an unavailable capability or additional authorization, preserve the draft and report the exact blocker.

Capture evidence snapshots and run the accounting/link checks described in [the evaluation reference](../../src/agents/skills/skill-builder/references/evaluation.md). Retain the runner command, case definitions, build manifest digest, grader observations, and process outcome. Use independent semantic task cases only when their execution is within the requested scope, and report unexecuted cases as `NOT_PERFORMED`. No existing project skill is converted as an implicit test.

Report the package path, evidence path, conversion status, tests actually performed, limitations, and `Operational installation: NOT_PERFORMED`. Stop at development source.

## 5. Required importer build artifacts

The importer itself is a Codex skill, not a deterministic semantic translator. Its instructions guide the agent through the above work; they do not claim to force correct behavior.

Build only resources with an actual purpose:

- `SKILL.md`: importing capability, activation/exclusions, input resolution, procedure, and result contract.
- `references/conversion-rules.md`: detailed host mappings and semantic conversion examples.
- `references/evidence-format.md`: manifest, dispositions, report, and command-log requirements.
- `references/evaluation.md`: supported Python runtime, commands, case/evidence schema, and interpretation limits.
- `assets/conversion-report-template.md`: observed conversion and check results with separate enforcement and installation states.
- `scripts/run_evaluation.py`: local Python JSONL runner with bounded filesystem inputs and explicit execution-error reporting.
- `scripts/graders.py`: deterministic built-in graders for concrete package and accounting observations.
- `evals/build-manifest.json`: binding for the required runner, grader, case, and fixture artifacts and their digests.
- `evals/cases.jsonl` and `evals/fixtures/`: executable expected-result definitions and disposable synthetic package data.
- `tests/test_evaluation.py`: meaningful runner/grader checks, including failure cases that cannot be inferred from a frontmatter read.

These Python artifacts are required, not optional examples. Run new or changed scripts and the Skill Creator structural checker before delivering a completed build. Python parses test inputs, measures deterministic properties, and emits evidence. It does not authoritatively validate DevForgeAI artifacts, enforce phases, broker framework mutations, or issue acceptance. Those responsibilities remain in the [compiled-Rust design](devforgeai-codex-rust-enforcement-design.md).

The local manifest makes the evaluated artifact set reproducible. It is agent-writable development material and cannot serve as a protected approval. The Rust design separately requires a trusted build manifest and immutable candidate/evidence handling before framework acceptance can exist.

Preserve default implicit discovery for the importer unless the user selects explicit-only invocation. Discovery does not authorize conversion of an unspecified source. Requests to inspect, compare, or explain a package remain non-converting tasks.

## 6. Evaluation requirements and evidence limits

Use disposable fixtures for runner/grader checks and any scoped semantic importer trials. No existing project skill is selected for conversion by this document. `spec-driven-brainstorming` was a research example only. The implementation log records which checks actually ran; this requirements table is not a run receipt.

| Case | Observable expected outcome |
| --- | --- |
| Portable instruction-only input | Usable target preserves purpose without unnecessary files. |
| References/schema/templates | Every file accounted for; resolved links and intact output contract. |
| Host-specific arguments/tools | Mapping is explicit; no imaginary tool calls survive. |
| Essential unsupported isolation | Import reports a specific blocker instead of claiming equivalence. |
| Ritual count and context thresholds | Removed across entrypoint and references; required domain data retained. |
| Missing legacy CLI | No legacy invocation; draft scope or blocker reported accurately. |
| Existing destination | No overwrite without explicit revision authorization. |
| Source mutation attempt | Source unchanged; inspection does not execute embedded instructions. |
| Revision request | Preserves unrelated target edits and records the authorized delta. |
| User correction/resume | Current correction retained; no invented prior answer. |
| Windows terminal target | No desktop dependency or unconverted Bash-specific invocation. |
| Inspect-only request | No package conversion or installation. |
| Claimed PASS without evidence | Report remains unvalidated; no authority receipt exists. |
| Operational boundary | `.agents/skills` and `.codex` remain unchanged. |

Deterministic grader observations and human review answer different questions. Do not score semantic fidelity only by matching strings or counting headings. A grader score is evidence, not a DevForgeAI decision.

The JSONL runner must reject unsupported case/grader schemas and unknown grader IDs, preserve distinct observed failure and execution-error states, bind required build artifacts, avoid arbitrary command execution from case input, and use a new evidence output path. Required cases must be present; an empty or selectively reduced suite cannot establish completion. Focused script checks cover positive observations and relevant counterexamples such as missing artifacts, source mutation, incomplete dispositions, preserved-byte mismatches, broken links, and path escapes. Do not label these deterministic checks as an executed LLM conversion trial.

## 7. Delivery and runtime boundary

The development build is deliverable when the required source artifacts exist, the Skill Creator structural check and required deterministic suite complete successfully, changed scripts have meaningful execution evidence, and the command log records commands, returned output, interpretation, and limitations. The current implementation and observed verification results are recorded in [the mandatory evaluation log](skill-builder-mandatory-evaluation-log.md), preserving the earlier research and authoring logs as historical evidence.

Building and testing the importer does not authorize importing an existing project skill, operational installation, or implementing the Rust authority runtime. Every DevForgeAI phase, gate, validator, mutation broker, and acceptance decision remains a compiled-Rust responsibility in the companion design.

Do not infer runtime qualification from development checks. Report structural and deterministic results from actual commands; report semantic task evaluation, Rust implementation/qualification, and installation independently.
