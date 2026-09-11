# Packaged skill authoring contract

Derived for this Claude evaluator from DevForgeAI `docs/mvp/skill-authoring-contract.md`, draft revision 3, selected at base commit c17e758417da64928a0f47fc2600304465ac3f3c. Exact digests are in `../derivation.json`. This operational summary retains the requirements that apply to evaluating a Claude package; the selected source bytes govern any conflict. It declares no draft framework capability implemented.

## Ownership and package

DevForgeAI owns methodology and provider skills. Claude framework skill sources are `providers/claude/plugins/devforgeai/skills/<name>`; Codex sources are separate and separately owned. A project-local `.claude/skills` copy or an exported plugin is a generated artifact, never an alternative canonical source, and a provider source directory alone is not a discovered installation.

A skill is `SKILL.md` with YAML `name` and `description`, plus `references/`, `assets/`, `scripts/` and `evals/` where each is genuinely useful. Keep entry instructions focused and link detailed resources at the phase that needs them. Resolve package resources from the loaded skill directory and the consuming project's artifact root separately. Do not depend on a developer's home path or on the framework's `docs/mvp` tree being present.

Authored cases and reproducible fixtures live under `evals/` in source and are excluded from ordinary installations and exports. Reusable evaluation templates and procedures live under `assets/` and `references/` and do ship. Keep run output, history and caches out of the package. Installed content preserves source bytes, but executable mode is not preserved: invoke a helper through its documented interpreter.

For every shared template or contract copied into a package, record the source path and exact revision, the source and destination digests, the transformation and the refresh conditions. One maintenance record - `references/derivation.json` - is sufficient. Missing derivation metadata is a package correction, not permission to redesign the shared template.

## Helpers

A helper declares its prerequisites, arguments, exit meanings and bounded output, provides `--help` where it has a command interface, and requires no interactive prompt. A stdlib-only helper needs no package manager. Report an execution failure as a failure or as unavailability, never as a successful check. A placeholder or hash helper proves only those facts - not schema correctness, provenance meaning or quality.

## Isolation and native runtime

Each candidate and baseline arm and each retry gets a distinct attempt identity, writable output area and isolated history store. Verify the effective client-state mapping before relying on clean-context evidence. Keep writable state inside the assigned area, preserve contaminated attempts rather than cleaning them, and record only owned processes for termination. These are required conditions, not a claim that the framework enforces them; a launcher or harness must supply observed evidence of its actual boundary.

## Three separately reported tiers

| Tier | Conditions | Evidence and limits |
| --- | --- | --- |
| A: discovery and activation | The actual installed package in a fresh session. Explicit invocation, direct domain requests, indirect requests and near-miss negatives kept separate. | Record the discovered identity and consultation traces. An implicit prompt must not supply the skill path or force invocation. |
| B: output quality and boundaries | Supplying the skill path is allowed. The same raw facts and task for the candidate and an appropriate baseline, in separate clean contexts. | Artifacts and requirement-based grades demonstrate behaviour after loading, never implicit activation. Baselines are `old_skill` or `without_skill`. |
| C: installed resources and outputs | An actual installed or exported package in a consuming project where source docs are unavailable. | Templates, references and helpers resolve inside the installed package; outputs land in the consuming project's map. A changed working directory does not prove source files were unreachable. |

Do not blend A, B and C into one percentage. A source-level check, a path-based subagent exercise or a version probe cannot establish tier A. An exported plugin and a project-local copy are different installation modes; identify which was tested, and avoid duplicate installations that could activate a different copy.

Separate a selection request, a successful load and a completed execution. A negative case needs a successful terminal result without target consultation before it records `PASS`. A timeout, error, truncated stream or premature EOF is `COULD_NOT_RUN`. Exercise any transcript detector against deterministic synthetic transcripts before relying on its classifications.

## Grading and closure

Grade the named behaviour, the required artifact delivery and the overall case separately; a correct idea can still fail an artifact requirement. Use `NOT_RUN` for an unexecuted arm and `NOT_APPLICABLE` only for a stated scope exclusion. Record auxiliary tool use and its observed success, denial or failure per arm - shared availability does not establish equal effective assistance.

Use realistic positive and near-miss negative trigger queries with a fixed train/validation split, and keep held-out expectations out of the author's and the worker's context. Report counts and limits for a small sample rather than inventing statistical claims. Capture token and time metrics only where they are actually observable.

Each run manifest records the tier, provider, client version and model, installation mode, path and file manifest, the source candidate and baseline manifests, the specification, case and fixture identities, context isolation, the assignment, observed sibling availability, output and transcript locators, and the actual outcomes.

An author's grades support scoped review; they are not external acceptance. Recheck integrated bytes before adoption or release. An authoring-only assignment supplies an unvalidated candidate and proposed cases - it does not authorise running validators, installing hooks, launching models or accepting a result.

## What is not applicable to this package

The accepted Routine/Full manual-mode validation policy, the Codex `--manual-experts-only --manual-evidence` installation mode and its adoption-evidence predicate, and the owner-approved local unqualified baseline all govern the two promoted Codex identities. They are `NOT_APPLICABLE` here and establish no Claude adoption path.
