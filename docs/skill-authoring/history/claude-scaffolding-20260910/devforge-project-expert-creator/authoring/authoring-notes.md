# Authoring notes: Claude devforge-project-expert-creator

Assignment: worker A1, Claude scaffolding 2026-09-10. Enhance the Claude `devforge-project-expert-creator` package by adapting the current Codex creator.

- Worktree: `/home/bryan/Projects/DevForge/worktrees/claude-scaffold-project-expert-creator-20260910`
- Branch: `author/claude-devforge-project-expert-creator-scaffold-20260910`
- Base commit, verified with `git rev-parse HEAD` before any write: `c17e758417da64928a0f47fc2600304465ac3f3c`
- Working tree at start: clean
- Write fence honoured: `providers/claude/plugins/devforgeai/skills/devforge-project-expert-creator/**` and this authoring directory. Nothing else in either repository was created, modified or deleted.

## Route used: operator-author bootstrap

There is no Claude builder skill to invoke, so this was authored under the bootstrap the skill-authoring contract permits: "A native creator or an operator can run this process before devforge-evaluate-expert itself is implemented. That bootstrap does not fabricate an evaluator invocation or add a thirteenth runtime skill."

Concretely, the Codex creator's `SKILL.md` and its five references were read by absolute path and followed as source-loaded instructions - Intake, Selection, Design, Authoring, PreparedTransfer - with the operator-author performing each phase.

What that means for the claims in this package:

- **No builder skill was invoked.** No `skill-builder`, no `skill-creator`, no delegated authoring agent.
- **No validator or evaluator was invoked.** No evaluation, no test, no installation, no binding, no export.
- **No thirteenth core skill was created.** The roster is unchanged.
- Reading the Codex source, computing digests and confirming that writes landed are authoring operations. They are not evidence about behaviour.

## Codex source revision

Port source: `providers/codex/plugins/devforgeai/skills/devforge-project-expert-creator` at base `c17e758417da64928a0f47fc2600304465ac3f3c`, read read-only and not modified. Its complete eighteen-file digest map is recorded in the package's `references/derivation.json` under `port_source.files_sha256`.

## Claude baseline preserved

The baseline was three files (`SKILL.md` `3dc906dd...`, `assets/evaluation-cases.md` `8cb830c9...`, `assets/expert-spec-template.md` `3c8e0b7f...`). Behaviours carried into the enhancement:

- Grounding through `devforge expert prepare`, the named upstream documents, the actual relevant code and the approved dependencies.
- Version-specific research recorded with source URL, retrieval date, applicable package version and actual verification; a newer version is a proposal, never permission to change the stack.
- Expert-specification-first authoring, with independently stated expected outcomes written before the candidate.
- Reuse of existing expertise when it covers the work.
- Skills grant no tool permissions; executable control logic stays in the external DevForge CLI, and a local reference may explain a gate but must not redefine it.
- Staleness handling: a policy, upstream or expert-file change means reviewing the semantic change, updating, repeating the affected evaluation and rebinding. Existing evidence is not carried forward silently.
- Closing with specification and skill paths, sources used, structural status, behavioural status, remaining gaps and the next human-owned decision - and never marking a skill a proven expert because structural validation passed.

**Ownership reassigned, not deleted.** The baseline had the creator itself run `devforge expert bind` and `devforge check`. SKILL-007 revision 3 and the Codex creator both put binding and installation outside the creator's boundary ("no target tests, binding or installation by creator"). Both commands are retained in the package's knowledge in `references/manual-operation.md` with their owners named as the operator and integration owner. Nothing was removed from what the package knows.

**One baseline file was removed.** `assets/expert-spec-template.md` (`3c8e0b7f...`) was superseded by the governing shared template copied to `assets/expert-spec.md`. Two competing expert-specification templates in one package conflict with the rule against maintaining a second independent design. Its eight contract rows - Responsibility, Activation, Knowledge, Inputs, Decisions, Output, Evaluation, Refresh - and its AI-proposal-versus-user-decision rule were carried into `references/interview-guide.md` as the expert-specification content checklist. The original bytes remain reachable at base commit `c17e758417da64928a0f47fc2600304465ac3f3c`, and the removal is recorded in `references/derivation.json`.

## Provider transformations: what was not copied, and why

| Codex material | Disposition | Reason |
| --- | --- | --- |
| `agents/openai.yaml` | Not carried | Per-skill Codex metadata, explicitly not a subagent, no Claude counterpart. |
| `$devforge-evaluate-expert` receiving syntax | Replaced | Claude uses `/skill-name`, or `/plugin-name:skill-name` for a plugin skill. Both recorded as illustrative, because installation mode is the operator's choice. |
| Codex hook events and the hook-proposal design block | Replaced | Hooks are integration-owner scope. Under the language policy's phases/hooks/skill-content clarification, the check itself must be compiled Rust in the DevForge CLI. The design template now records an *enforcement route*: requirement, protected action, observable evidence, freshness, intended allow/refuse behaviour, owner = integration owner, feasibility Unknown until confirmed, status "requirement recorded; no gate implemented by this skill." "Hook status: Design only" became "Enforcement status" everywhere. |
| `references/managed-authoring.md` | Not carried | Governs the managed v1 protocol whose workflow IDs are `skill-builder` and `skill-validator`. No Claude counterpart; the IDs and the `advance`/`resume`/`complete` chain are retained only under a "Historical identities" heading in `manual-operation.md`. |
| `references/results-contract.md` | Absorbed, not carried | Its identity and storage rules (`{path, sha256}` locators, relative resolution, freeze before hashing, no self-digest) went into `validator-handoff.md`. The definitive paired contract belongs to the Claude `devforge-evaluate-expert` port. |
| `references/contracts/` (three full contract copies) | Distilled instead | `SKILL.md` does not need the full contracts at runtime. The operative rules were distilled into `references/framework-context.md`, with every source path, digest and section recorded - the pattern the Claude brainstorm package uses for `recording-rules.md`. This is a deliberate departure from the Codex package shape; noted here for the coordinator. |
| `.agents/skills` inventory | Replaced | Claude locations: project `.claude/skills` with parent and child discovery, nested subdirectory skills, personal `~/.claude/skills`, a plugin's `skills/`, the managed settings directory, and an `--add-dir` directory. |
| OpenAI documentation sources | Not carried | `references/sources.md` records the two Claude Code pages actually fetched and states explicitly that the Codex sources are not repeated as though they governed Claude behaviour. |
| Codex `--manual-experts-only --manual-evidence` mode and the local-unqualified-baseline record catalogue | `NOT_APPLICABLE` | Scoped to two recognised Codex identities by the authoring contract. Recorded as not applicable rather than silently dropped. |
| Codex Routine/Full manual-mode policy trailer | `NOT_APPLICABLE` | Governs the promoted Codex packages. Recorded as not applicable to this Claude package until an owner selects an equivalent. |

No `scripts/` directory was created. No deterministic evaluation-only helper is required, and framework logic may not be added in Python or shell.

## Commands actually run

Read-only, all of them. No gate command was run against any project, and nothing was built, installed, exported or evaluated.

| Command | Purpose | Result |
| --- | --- | --- |
| `git -C <worktree> rev-parse HEAD`, `rev-parse --abbrev-ref HEAD`, `rev-parse --git-common-dir`, `status --porcelain` | Verify assignment before writing | HEAD `c17e758417da...`, expected branch, DevForgeAI repo, clean tree |
| `sha256sum` over the Codex package, the `docs/mvp` templates, the contracts, the specification and the Claude baseline | Bind source identities for `derivation.json` | Recorded in the package derivation record |
| `devforge --help`, `devforge expert --help`, `devforge check --help`, `devforge expert prepare\|bind\|status --help` | Confirm every command named in the package exists, and its flag placement | All confirmed; leaf subcommands accept `--project/--policy/--state/--expert` |
| `grep` scans over the finished package | Scrub for `.agents/skills`, `$devforge-`, `agents/openai.yaml`, OpenAI hosts, absolute home paths, `.poc/`, stray Codex client references | No hits except the two labelled `NOT_APPLICABLE`/historical passages and the two verbatim template sections noted below |
| `python3 -c json.load` on `evals.json`, `trigger-queries.json`, `derivation.json` | Validate JSON | All parse |
| `python3` digest check of every `destination_sha256` in `derivation.json` against the files on disk | Catch the stale-digest defect this codebase has recorded three times | No mismatches; no self-digest present |

The `devforge` binary used for `--help` was the companion repository's existing debug build. Nothing was rebuilt.

## Write order

Package files first, then `references/derivation.json` with the destination digests, then `file-manifest.json` over the whole package including the derivation record, then these notes and `spec-mapping.md`, and the evidence handoff last. Digests were verified against the files on disk after the last write to each.

### Digest defects caught and corrected before commit

Recorded here because a corrected record is only trustworthy if the correction is visible.

The two withdrawn values quoted below are deliberately incorrect and are retained only as history. They do not resolve to any bytes, and a checker should not expect them to.

1. **Fabricated digest tail.** The evidence handoff's `evidence` block initially recorded `references/derivation.json` with a digest whose tail had been reconstructed from a truncated terminal display rather than read from a real value. The withdrawn string began `497fe6ee9fe2ab55`; only its first twelve characters were ever real. It was corrected to the actual digest, and after the later corrections in this same pass changed `derivation.json` again, the handoff was refreshed once more. The authoritative current value for that file is the one in `file-manifest.json`; this note deliberately pins no digest of its own, so that it cannot go stale behind a later edit. Caught by a programmatic readback that resolves every 64-character digest in the evidence against real bytes.
2. **Wrong truncated prefix.** `spec-mapping.md` recorded the authoring contract with the withdrawn prefix `3714623857`; the actual digest begins `371462385b4e`. The first readback checked only full-length digests, so it did not catch this. A truncated-prefix check was added and the readback re-run.

Both were caught before commit and no downstream record carried either value. A wrong prefix is the same defect class as a wrong full digest: a reader who cannot resolve it cannot check the claim.

Three template-filler values were corrected in the same pass: `recorded_at_utc` and `created_at_utc` in `references/derivation.json`, `file-manifest.json` and the evidence handoff had been written as midnight rather than the actual write time, which the artifact contract requires. A stray `}}` in the shipped `assets/handoff.md` `execution_ref` placeholder was also fixed, and its digest cascaded into `references/derivation.json` and `file-manifest.json`.

## Unresolved questions and things the coordinator must decide

1. **Commit attribution conflict.** The task packet supplies `Co-Authored-By: Claude Fable 5.1`. This session's system prompt states the model is Opus 5 (1M context), model ID `claude-opus-5[1m]`, and the harness attribution reminder - which states it replaces earlier attribution guidance - supplies `Co-Authored-By: Claude Opus 5 (1M context)`. Committing "Fable 5.1" would contradict the required first line of the report. The accurate attribution was used. Flagged for the coordinator.
2. **`contracts/` omitted.** The Claude package distils the three shared contracts into `references/framework-context.md` instead of shipping copies, unlike the Codex package. Sources and sections are recorded. If the coordinator wants shape parity with Codex, this is the deviation to reverse.
3. **Two verbatim template sections are inapplicable.** `assets/expert-spec.md` and `assets/expert-package.md` are byte-identical copies of the governing `docs/mvp` templates and both carry a "Promoted Codex content mapping" section, and `expert-spec.md` carries a "Codex / Claude" terminal placeholder. Editing them would change a shared template's governing meaning, which is outside a skill author's fence, so they were left untouched. The disposition belongs to the integration owner.
4. **`results-contract.md` absorbed rather than ported.** If the Claude `devforge-evaluate-expert` port defines record shapes that differ from the minimum stated in `validator-handoff.md`, that reference needs a bounded refresh.
5. **Runner and grader dependency.** `evals/evals.json` and `evals/triggers/trigger-queries.json` record that executing them needs the Python JSONL runner and deterministic graders from the Claude `devforge-evaluate-expert` package, which does not exist at this revision. Every case and query outcome is `NOT_RUN`. Evals are source-only and ship with no runtime copy.
6. **No `when_to_use` field used.** The packet specified frontmatter `name` + `description` only, so the triggers and near-miss exclusions are inside `description` (869 characters, within the documented 1,536-character combined cap). If a later revision wants `when_to_use`, the split is available.
7. **Nothing here is evaluated.** Validation status: Not performed. Behavioural status: `NOT_EVALUATED`. Discovery, activation, installed-resource resolution and output quality are all unobserved. Tier A, B and C are all `NOT_RUN`.

## Package shape produced

`SKILL.md` (118 lines, frontmatter `name` + `description` only), six `references/` files plus `derivation.json`, seven `assets/` files, `evals/evals.json` with ten cases, `evals/triggers/trigger-queries.json` with twenty-two queries, and nine synthetic fixtures. Twenty-five files, inventoried by digest in `file-manifest.json`.
