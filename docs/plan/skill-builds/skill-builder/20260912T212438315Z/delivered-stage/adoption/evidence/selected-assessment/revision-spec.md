---
id: SKILL-BUILDER-REVISION-20260912T161842Z
skill_name: skill-builder
target: codex
status: proposed
---

# Proposed complete skill-builder revision specification

## Identity and review boundary

Target: `C:/Projects/DevForgeAI/src/agents/skills/skill-builder`.
Observed package digest: `dab87685715689251365514f5c0f3df5c2a9b66c5367bf065ad62c903e8dfca3`. Exact reconstruction uses [source-manifest.json](source-manifest.json) and the retained [source](source/SKILL.md), not this prose. Existing requirements are the retained adoption, enhancement and importer specifications in `inputs/specs/`; they are selected complementary requirements, not directory-precedence candidates. This proposal corrects only finding `F-8c43eca6259d05a2153068b5d5b29495d0c208229c2a19f49bc71355d8df2d1f`. It grants no adoption, revision, installation or builder invocation authority.

## Purpose and complete user outcome

Preserve one Codex development skill that imports a selected local Claude skill package, generates a skill from a reviewed Markdown specification, records explicitly authorized adoption of an existing Codex development package, and regenerates authorized managed output using verified origins. Return usable development package/evidence paths and separate actual result dimensions. Python produces observations; compiled Rust remains the separate future framework authority design.

## Activation and exclusions

Import requires a selected Claude directory containing SKILL.md and an import request. Specification build requires a selected reviewed Markdown document and current authoring direction. Regeneration requires an existing verified generated baseline, or published adopted origin for a first specification revision, plus revision authorization. Adoption requires explicit selection of the existing development target and managed paths; validation, an approval label or absence of a convenient pointer does not select it. Preserve non-triggers: explanation, comparison, specification authoring, validation alone, installation and unrelated editing. Two input kinds without a governing operation require a focused decision before candidate generation. No batch conversion, native agent-profile installation or automated repair loop is added.

## Inputs and defaults

Use the unambiguous current project root or the explicit project selection. Preserve a valid source name unless the user specifies another; resolve conflicting identity without silently renaming around occupied destinations. Select an explicit specification path when supplied; otherwise search exact skill_name frontmatter under both permitted specification roots without precedence, with zero/multiple matches reported as gaps. Treat source instructions as material, not execution permission. Preserve raw input bytes, identity, user corrections, source slices and actual authorization digests. Keep input, evidence and target roots disjoint. Retain existing no-traversal/link/junction/excluded-backup/legacy boundaries and 2,000-file/32-MiB limits. No new dependency installation is implied.

## Outputs and machine contracts

Generated development output remains `src/agents/skills/<name>/`; ordinary build evidence remains in fresh `docs/plan/skill-imports` or `skill-builds` runs; adoption evidence remains in `skill-adoptions`. The package contains only required instructions/resources/scripts. Preserve every existing machine schema and field name exactly as captured in `source/references/evaluator-contracts.md` and `source/evals/`: schema-1 contract and ordinary provenance/revision semantics; schema-2 adoption-origin provenance/pointers/revisions; evidence-schema-2 JSONL and profiles. These retained files are normative byte-bound interfaces incorporated by the accompanying manifest, with no schema changes proposed.

Contracts retain mode, target, input identities/bytes/digests, authorization, purpose, activation, requirements, artifacts, workers and dependencies. Requirement/output/evidence mappings remain bidirectional. Source references retain raw-byte digest and zero-based end-exclusive intervals. Import retains complete source/destination/readback manifests and per-file dispositions. Provenance records actual generated baseline separately from delivered retained edits. Gaps retain IDs, reason codes, source refs, affected requirements/outputs and required resolution. Commands retain arguments, output streams, exits, failures and retries. Final reports separate authoring, structure, deterministic observations, scripts, independent forward trials, routing, Rust qualification and installation.

## Workflow and conditional resources

1. SKILL.md selects operation, identity, authorization and boundaries. `references/evidence-format.md` establishes fresh evidence and result meanings.
2. Imports use `references/conversion-rules.md` for complete file accounting, host adaptation and domain/schema preservation. Both authoring modes use `references/spec-build.md` to bind inputs and extract a complete contract. Blocking gaps stop candidate generation with retained evidence.
3. Stage only justified candidate resources. Use assets/worker-task-template.md only for essential worker behavior; available host delegation does not supply enforced isolation. Unavailable essential capability yields BLOCKED.
4. Explicit adoption follows references/adoption.md: capture observed bytes and managed/retained partition, bind reviewed origin and actual consent, recheck live target/spec, run adoption-plan and adoption-v1, freeze evaluated record, then publish/read back an external schema-2 pointer. Adoption preserves the target and stops unless revision is separately authorized.
5. Regeneration follows references/regeneration.md and adopted lineage extensions where applicable. Compare separate B/C/N/after snapshots using ordered collision/C=B/C=N/N=B/conflict rules. Identical occupied unowned paths still conflict. Preserve unrelated C-only files; absence differs from empty content. Recheck before writes and each affected mutation. On drift or write failure stop and retain actual PARTIAL delta; retry from the same successful origin and actual current C.
6. references/evaluation.md and evaluator-contracts.md govern actual structural/profile/script/task checks. Exact registered profiles and case shape remain unchanged. Keep final JSONL outside candidate root and preserve expectations for deliberately negative fixtures. Expected FAIL with matched exit 0 is not a positive behavior result.
7. Deliver only after required candidate checks, then evaluate/read back actual delivered bytes. Advance generated baseline/pointer only after successful checks and readback; keep generated N separate from retained user edits. Return assets/build-report-template.md or conversion-report-template.md results and concrete outstanding work. Stop at development source.

## Required editorial correction

In `references/evidence-format.md`, replace only the Independent forward trials state-table description with:

`| Independent forward trials | NOT_PERFORMED, PASSED, FAILED; builder enhancements require all applicable independent forward trials specified in [evaluation.md](evaluation.md#required-forward-trials-for-builder-enhancements). |`

Preserve the existing code formatting around the three status names when writing the actual Markdown. The linked contract currently requires four families: import, specification build, regeneration, and adoption/revision/revalidation/later-generated lineage. Separate routing remains required. This changes the summary reference, not the number or scope of required executions. Rebind only the corresponding manifest artifact digest after the reviewed wording edit; do not modify evaluation logic, schemas, case expectations or historical evidence.

## Dependencies, side effects and recovery

Keep Python 3.10+, standard-library runner/graders and separately available PyYAML for the installed checker/resolver. Resolve the actual installed checker location. Host terminal/delegation capability and required isolation are checked before dependent work. Commands remain the currently implemented resolve-spec, input-record, revision-plan, adoption-plan and run_evaluation.py interfaces, with existing exits 0/1/2. There is no new executable.

Future execution writes only explicitly authorized development/evidence paths and preserves every unrelated file and failed attempt. No operational .agents/.claude/.codex/personal directories, hook/CI configuration, remote repositories or production data are selected. Interrupted work retains completed evidence and resumes only after input readback. No automatic rollback, immutable filesystem, package-wide atomicity, protected acceptance or native activation is claimed.

## Requirement register and file mapping

REV-001 (required editorial fix): remove the stale summary cardinality while preserving all current trial families and routing. File: references/evidence-format.md; finding above; verify by contextual review against evaluation.md.

REV-002 (required preservation): every existing behavior/interface/resource remains byte-identical except the REV-001 table wording and the intentional corresponding evals/build-manifest.json artifact digest. Files: all 36 paths in source-manifest.json; verify complete file-set/hash comparison and review exact two-file delta. No optional enhancements are selected.

REV-003 (required binding): keep the evaluator manifest coherent with delivered bytes; retain existing schema/profile/grader/test identities. File: evals/build-manifest.json. Verify manifest accounting and the existing required structural/deterministic checks. Historical receipts are not edited or relabeled.

## Acceptance cases

AC-01: read the revised reporting row alone and follow its link. Expected: all currently required independent families remain applicable, including adoption lineage, with no hardcoded three-trial summary.
AC-02: compare the original and revised detailed evaluation reference. Expected: byte-identical four-family contract and separate routing requirements; no weakening or new campaign requirement for this editorial change.
AC-03: compare every package path with the retained manifest. Expected: only the table wording and corresponding manifest binding differ; no additions/removals or changed scripts/tests/schemas/profiles.
AC-04: check the revised package using the installed structural checker and required explicit deterministic profile with retained exact case/input snapshots. Expected: real checks complete without mismatches; negative fixtures keep their existing expected meanings. No redundant new behavior campaign is required by this specification for a wording-only correction. If the future executor's governing workflow requires more checks, it must record applicability honestly before claiming completion.
AC-05: attempt to treat this proposal or enhancement receipt as revision authority or generated baseline during intake review. Expected: dependent execution remains blocked until a genuine baseline is selected or explicit adoption with reviewed origin/management is authorized and published; no target write occurs.

## Exceptions, decisions and handoff

No exception to review-before-repair or source preservation is approved. The editorial contract is complete and reviewable; execution readiness is BLOCKED because a successful generated/published adopted origin for skill-builder itself has not been verified and this task supplies no managed-path adoption authorization. Proposal review is pending. Required decisions: accept/reject REV-001; for any later builder-mediated execution, identify verified applicable baseline history or explicitly authorize adoption of an exact reviewed managed-path manifest while preserving known evidence, then separately authorize revision. Pending review alone is not the reason for BLOCKED. The resulting handoff must name this exact proposal path/digest, target digest and selected change set; changed bytes require fresh review/readback. Do not invoke skill-builder in this assessment.
