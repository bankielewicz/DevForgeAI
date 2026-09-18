---
id: SKILL-VALIDATOR-REVISION-20260915T1342575302099Z
skill_name: skill-validator
target: codex
status: proposed
---
# Proposed validator test and measurement repair contract

## Identity, purpose and scope

Target: C:\Projects\DevForgeAI\src\agents\skills\skill-validator. Package digest: 8852ab64ea1b757af6cb17ebde9d411e4ed0ce21962290b8c241c31f0320fb3b. Origin is inputs/raw/skill-validator-spec.md; current complete implementation is the 89-file source snapshot. Finding F-63308bc35a6c4f35c8bd5f3b71e1800f553b8b2b6537d95146360021c71330ef motivates this proposal. This is a future scoped repair contract; no changes are authorized by this document.

Retain the current skill's purpose: assess explicitly selected Codex skill packages, preserve source and origin, use grounded rules, inspect instructions/resources/workflow, execute bounded disposable tests, deliver findings and a revision proposal, then stop at review. Existing adaptive-set, authoring-intake and legacy assessment interfaces remain unchanged. The snapshot plus preserved origin and linked current references define all unchanged behavior.

## Triggers and inputs

Keep the current description and invocation policy. Validation/revalidation requests activate the skill; creation, repair, installation, product-code audits and framework implementation remain separate. Inputs remain explicit package/project, optional selected specification/prior evidence, current user requirements and available tools. No new metadata or mandatory dependency for ordinary validation is introduced.

The maintenance test task additionally selects a byte-bound development builder dependency and existing Python/PyYAML/coverage tools. AUTHORING_BUILDER_ROOT continues to select that dependency for integration tests only. Do not silently bind an arbitrary installed copy or copy credentials.

## Outputs and operational workflow

Preserve existing schema-1 records, supplemental adaptive records, Python JSONL runner/cases/graders/schemas/manifests and their meanings. Ordinary assessment continues through snapshot, origin, rule pinning, static/semantic review, bounded behavior, readback, report, findings, optional full revision specification and handoff. Missing dependencies produce explicit unperformed checks while independent work proceeds. Reports distinguish observations from compiled-Rust authority.

Maintenance should declare all unique required cases before execution, run them against captured packages with temporary files under the evidence root, and retain every attempt. Load errors must identify missing dependency setup without counting synthetic loader placeholders as additional test cases. Never erase failed attempts or count successful retries twice.

## Mandatory repair requirements

VR-01: Update the noncanonical-stage test to handle the actual selected authoring failure-record contract. Verify BLOCKED, zero applied paths, a concrete recovery reason in the contract-defined error representation, absent successful baseline and unchanged source/contract bytes. Do not reduce this to accepting any exception or nonzero exit.

VR-02: Construct a valid competing-writer fixture at the actual callback boundary. Ensure the synthetic target directory exists when the independent writer writes. Prove the competing write occurred, preserved bytes equal that writer's content, validator/builder applied no replacement, and publication did not create successful custody evidence. Do not merely change PARTIAL to BLOCKED to make the old test pass.

VR-03: Make the interrupted readback fixture reach files(target). Establish the target's existence before injecting read failure. Prove the attempted read and real exception, explicit readback gap, no accepted baseline and retained failed-attempt evidence. Do not assert an error phrase for a branch never exercised.

VR-04: Retain validator-only coverage denominator: every executable line in its 14 captured scripts, with no first-party exclusion. Instrument subprocess/copy execution using verified source identity; only merge a copied file's executed lines when its bytes match the bound source. Report unmapped or changed copies separately. Preserve initial limited measurements. Once measurement is correct, add meaningful negative/integration cases only for genuinely uncovered behavior. Require >=95% line coverage and >=95% unique-case pass rate independently; failed mandatory cases still prevent qualification.

VR-05: Update maintenance invocation guidance if needed to show explicit dependency selection and coverage setup. Ordinary skill execution must remain builder-independent. Retain exact runtime versions, source/dependency manifests, cases, stdout/stderr, duration, source readback and all errors.

## Files and preservation

Primary allowed future test edits: tests/test_authoring.py and tests/test_authoring_safeguards.py (VR-01 through VR-03). Maintenance guidance/evaluation support may implement VR-04/VR-05 after selecting the coverage approach. Preserve SKILL.md, runtime scripts, schemas and legacy record meanings unless an additional demonstrated requirement justifies an explicitly selected change. No edits to src/agents/skills/skill-builder, .agents, prior evidence, source specifications, hooks or startup configuration.

## Dependencies, failure paths and recovery

Use existing Python 3.10+ and PyYAML. Coverage is an evaluation dependency, not a framework authority. Windows fault-injection tests remain Windows-qualified; other platforms need separately reported runs. Preserve setup errors, test failures, timeouts and incomplete source mapping. Re-execution uses fresh attempt directories and unchanged or freshly captured inputs.

## Acceptance and handoff

A1: Execute the three focused original failure scenarios before repair and retain real failures; then verify VR-01/02/03 with independent assertions of reached effects and preservation.
A2: Execute all 402 currently declared unique regression cases (plus justified new cases), with no skipped required cases promoted to pass.
A3: Verify correct byte-bound subprocess/copy coverage and report line/branch numerators and denominators; meet VR-04 without narrowing source.
A4: Repeat relevant cold assessment only if instructions/workflow changed; preserve target/source and distinguish implicit discovery.
A5: Run creator/structure/record checks and target/dependency readback, then deliver evidence for independent validation. These are development checks, not framework acceptance.

The observed source snapshot can support a later authorized scoped edit; no generated/adopted history was verified here. Proposal review is pending. Exact builder failure-contract version and the byte-bound copied-path coverage mechanism need selection before calling this implementation-ready. No repair or installation occurs in this assessment.
