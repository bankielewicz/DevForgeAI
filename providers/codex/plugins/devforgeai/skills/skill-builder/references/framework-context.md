# DevForgeAI intrinsic context

Selected source snapshot: 2026-09-07. Exact source and package identities are recorded in derivation.json. This describes observed POC capabilities and governing draft contracts; it does not promote them to accepted production guarantees.

## Identity and authority

DevForgeAI is an adaptive, spec-driven software engineering framework. Adaptation selects relevant workflows/context, creates or refreshes concrete expertise gaps, and reevaluates affected work under accepted specifications and recorded authority. Current status remains local Linux/WSL2 proof of concept.

DevForgeAI owns conversational workflows, skills, examples and expertise. The companion DevForge owns Rust CLI policy, deterministic external gates, installation tooling, tests and CI. Neither builder nor validator may change an external gate or governing specification merely to obtain PASS.

A specification, artifact status, byte identity, runtime observation, AI judgment and human acceptance are separate records. A hash proves bytes only. Proposed recommendations require their actual adoption source before becoming accepted constraints.

## Canonical source and installed copies

For a Codex framework custom skill, the canonical source is:
providers/codex/plugins/devforgeai/skills/<skill-name>/
inside the operator-selected DevForgeAI root.

The Claude provider tree is a separate assignment. Normal Codex project-local copies live in the consuming project's .agents/skills; they are generated installations, not alternative canonical sources. Provider source existence does not establish runtime installation or activation.

For project-specific custom expertise, record the actual source-to-install mapping in the design. Do not assume portable example fixtures define every project's mapping. Resolve the user's selected roots rather than hard-coding a developer home directory.

skill-builder and skill-validator are paired authoring infrastructure introduced by the current user assignment. They do not silently replace the existing 12-stage application roster or the separately proposed XSPEC/XPKG project-expert evaluator, devforge-evaluate-expert. Existing devforge-project-expert-creator is an older specialized draft whose evaluation instructions are not changed by this assignment.

## The builder/validator contract

skill-builder gathers requirements, searches related skills, writes skill-design-spec.md-based design documents, authors/enhances the canonical skill, and proposes hooks. It does not execute skill validation, behavioral tests, candidate helper scripts, or hooks.

skill-validator inspects a frozen candidate, runs allowed deterministic checks and actual native tests, performs independent AI review, and writes evidence plus a repair/enhancement specification for skill-builder. It does not modify the target candidate or declare external acceptance.

For these utilities, authored means files have been written. Evaluated means actual scoped results exist. Enforced requirements do not imply hooks or an external acceptance system are installed.

## Runtime packaging and evidence

The selected authoring contract uses separate C (installed resources), B (output quality), and A (native activation) results, exercised in that order. A path-supplied worker cannot establish implicit activation.

Runtime resources belong in scripts, references and assets. Tests of the skill itself belong in evals and are excluded from runtime exports. Package-local copied contracts/templates carry source and destination digests in references/derivation.json. Installed skills resolve their resources internally; source documentation need not be reachable.

The companion installer observed on 2026-09-07 excludes evals, history, Python cache artifacts, and files named provenance.json. Runtime-required derivation metadata therefore uses derivation.json.

## Observed tooling boundaries

- The companion validate_framework.py checks the entire framework structurally, not one target skill's semantics or native behavior.
- validate_mvp.py assumes the existing 12 indexed specs; it is not the new generic skill checker.
- The companion delivery supervisor refuses native (synthetic=False) launches because its native launcher/authentication and effective hook-source verification are unavailable. Synthetic runs are not native skill evidence.
- The older DevForge isolate command leaves other source paths readable and reports no network isolation. It alone cannot establish source-inaccessible tier C or a clean baseline.
- The authoring contract permits a manual operator-established, isolated subscribed native terminal. Observe its effective boundary and identity before relying on it; unavailable conditions remain COULD_NOT_RUN.

These are dated observations, not eternal limitations. A future adopted tooling revision must be inspected and its actual behavior observed before replacing the recorded arrangement. Do not invent a devforge skill-validation subcommand or expose a proposed hook as active.

## Governing references

Load the relevant selected contract when needed:
- [Authoring, ownership, packaging and evaluation](contracts/skill-authoring-contract.md)
- [Artifact identities, evidence and acceptance](contracts/artifact-contract.md)
- [Execution assignments, isolation and hook limits](contracts/execution-contract.md)

derivation.json preserves the source paths and hashes of these packaged derivations. If a user supplies a different accepted revision, record that selection and its exact bytes; do not silently substitute the newest checkout.

## Controlled modernization selection

The user-selected SENH revision 3 explicitly refreshes this builder to the preserved revision-3 authoring/execution sources in derivation.json. Historical evaluation inputs and outcomes stay unchanged. The shared handoff governing path is the same one used by skill-validator; the builder copy selects its current preserved bytes, and the bounded validator alignment now selects that same preserved revision under the recorded release.

The selected shared contracts describe the brainstorm adapter and four provider callback declarations. Separately selected DevForge utility sources provide protected builder/validator mechanics; derivation.json pins that reviewed component. Native readiness, effective callback behavior, activation and rendered delivery remain unobserved. See [managed authoring](managed-authoring.md) when admitted context or handoff delivery applies. Substantive authoring belongs to the skill; protected runtime owns transitions, evidence checks, waiting, corrections and final receipts. Missing adapters never justify ceremonial self-certification.
