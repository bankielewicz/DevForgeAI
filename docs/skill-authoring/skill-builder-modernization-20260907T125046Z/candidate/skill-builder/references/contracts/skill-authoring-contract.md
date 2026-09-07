# Packaged skill authoring contract

Derived for these Codex authoring utilities from DevForgeAI docs/mvp/skill-authoring-contract.md, draft revision 3, 2026-09-07. Exact source and destination hashes are in ../derivation.json. This operational summary retains applicable requirements; the assignment's selected source bytes govern any conflict. It does not declare draft framework capabilities implemented.

## Ownership and package

DevForgeAI owns methodology and provider skills. Codex framework skill sources are providers/codex/plugins/devforgeai/skills/<name>. Claude sources are separate. .agents/skills is the generated Codex project installation; a source directory alone is not discovered. Per-skill agents/openai.yaml is optional discovery metadata, not a standalone subagent. Shared templates and sibling policy have distinct owners.

A skill contains SKILL.md with YAML name and description. scripts, references, assets and metadata exist only when useful. Keep entry instructions focused and reference detailed resources at the phase that needs them. Resolve resources from the actual loaded installed skill directory; resolve the consuming project's artifact directory independently. Do not depend on developer home paths or source docs being present.

Authored cases and reproducible fixtures live under evals in source. Exclude evals from ordinary installations/exports. Reusable evaluator templates and procedures live under assets/references and ship at runtime. Keep run output/history/caches out of the package. Installed content preserves source bytes, but executable mode preservation is not assured: call helpers through their documented interpreter.

Package-local derivations record source path, selected preserved revision/location and exact SHA-256, destination path/hash, transformation and refresh condition. Pin sources before updating; source changes do not silently replace an assignment's governing version. Refresh only within the named skill/provider and preserve prior evidence. Runtime maintenance metadata uses references/derivation.json, not an excluded provenance sidecar.

Helpers declare runtime/dependencies, arguments, --help, noninteractive behavior, bounded output and exit meanings. Missing prerequisites are unavailable observations. A hash/placeholder check does not prove schema meaning, provenance fidelity or behavioral quality. Optional dependencies must be explicit; do not silently install them.

## Authoring and evidence

Recover actual task authorization, source/specification, ownership and template revisions. Preserve the previous candidate before enhancement. Resolve consequential ambiguity with the owner; do not reinterpret an accepted rule. This builder delegates validation to the separate validator by user decision; do not run validation while authoring.

Define realistic requirement-derived cases and reproducible raw fixtures before measured execution. Preserve train/validation split and hide held-out expectations from authors/task workers. Version expectations before measurement. Diagnostics may inform a later iteration; they cannot change the grading rule of a failed measured run.

Keep candidate and baseline source manifests separate from actual installed manifests. Record source and installed identities, case/spec/rubric/fixture/contract identities, provider/client/model, installation mode, actual assignment, output paths and evidence. Changes to any relevant input invalidate affected observations. Retain old bytes and failures. External acceptance is separate from an author's or validator's scoped recommendation.

## Isolation and native runtime

Each candidate arm, baseline arm and retry has a unique identity, writable output area and separate history/memory state. A new chat or worktree is insufficient proof. Observe effective client state, visible instructions/skills/plugins/tools/settings and actual tool success/denial. Shared availability does not imply equal effective assistance.

Use assigned disposable consuming projects. Keep global history, memory, configuration and credentials outside the writable run area. Subscription authentication needs an explicit operator arrangement; never copy secrets into evidence. Record launched process identities and terminate only verified owned processes. Probe the filesystem, source visibility and process boundaries harmlessly before model execution. Missing required isolation means COULD_NOT_RUN, with no unconfined fallback.

Manual isolated subscribed terminal evaluation is a supported method. No model API or API-backed CI is required. A tool's name does not prove native discovery or permitted authentication. Inspect its actual documented invocation, revision, source selection and observation method before adopting it.

## Three independent native tiers

Perform C, then B, then A, and report each separately.

- C, installed resources: use the actual installation in a consuming project with source docs demonstrably unavailable. Exercise package-local templates/references/helpers and output paths. A changed working directory does not establish source inaccessibility.
- B, quality and boundaries: explicit skill-path input is permitted. Give candidate and old_skill/without_skill baseline the same raw facts with isolated contexts/output. Grade required named behavior, artifacts, constraints and provenance. Baseline FAIL may be useful comparison evidence; unrun baseline is NOT_RUN.
- A, native discovery/activation: actual installed identity in a fresh target terminal. Separate explicit invocation, direct ordinary request, indirect request and near-miss negative. Implicit queries cannot give the skill path or force its name. Record selection request, actual loading/consultation and successful terminal completion independently.

Negative activation PASS requires a completed successful terminal with no target consultation. Timeout, premature EOF, truncated output or missing completion is COULD_NOT_RUN. Detect exact identity/consultation, not unrelated substrings. Test any detector's termination and identity handling with synthetic traces before relying on model observations; synthetic traces themselves are not native evidence.

## Grading and closure

Grade behavior, artifact delivery and overall result independently against accepted requirements. Resolve referenced revisions against retained bytes; provenance binding does not prove semantics. Record producer identity, active assignment, actual feedback and adoption separately. A historical author is not proof of a current exclusive writer.

Use PASS and FAIL only for supported observed conditions. NOT_RUN means unattempted; COULD_NOT_RUN means required observation unavailable with cause; NOT_APPLICABLE means predefined scoped exclusion with reason. Required phases cannot be silently excluded. A small pilot reports its counts and limits, not unsupported statistical claims.

Retain native outputs in their own formats. The report binds them with exact references rather than rewriting history. Promote only the provider, installation mode and use cases supported by evidence. A refreshed installation or integration candidate requires affected rechecks.

## Revision-3 controlled refresh

This assignment explicitly selects the revision-3 sources preserved in derivation.json. Historical evaluations retain their original revision-2 authoring contract and exact inputs. No previous result becomes revision-3 conformance evidence.

Managed operation keeps useful phase work in the skill and mechanical transitions, evidence predicates, waiting, correction bounds and receipt publication in the protected runtime. The current managed adapter is brainstorm-specific; builder/validator integration remains a separately owned gap. Native admission is NOT_VALIDATED and native activation/rendered delivery NOT_OBSERVED.

Keep conditional managed guidance package-local. Final identities and receipts come from runtime observations; no model-issued completion check or helper fallback. Delivery-aware installation/export belongs to integration and must bind the explicit runtime executable, six-field requirement and single effective synchronous callback per event from the execution contract. Package/source compatibility does not certify native behavior. Frozen case expectations, task deadlines, old failures and separate C/B/A results remain intact; runtime-aware measurement requires newly allocated independent evidence.
