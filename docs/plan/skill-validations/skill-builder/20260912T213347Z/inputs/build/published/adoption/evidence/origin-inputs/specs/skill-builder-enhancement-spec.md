# Specification: Enhance `skill-builder`

**Document:** `C:\Projects\DevForgeAI\docs\plan\skill-builder-enhancement-spec.md`  
**Status:** Approved plan transcribed as an implementation specification; skill enhancement not implemented by this document-delivery task.  
**Recorded:** 2026-09-12.  
**Implementation consumer:** `$skill-creator`  
**Target:** Existing development skill `src/agents/skills/skill-builder`.  
**Evidence:** [Command and research log](skill-builder-enhancement-research-log.md).

## 1. Purpose and fixed decisions

Enhance the existing skill with selected functionality from `SKILL-SPEC-012-skill-generator.md`, preserving its existing Claude-to-Codex import capability.

The enhanced skill has two authoring modes:

1. **Import:** Convert one selected local Claude skill package into a Codex skill.
2. **Specification build:** Generate one Codex skill from an explicitly selected, user-approved Markdown specification.

Both modes support authorized revisions through the regeneration procedure below.

The following decisions are fixed:

- Accept existing Markdown specifications; do not require their conversion into a new document template.
- Produce Codex development output only.
- Generate worker task contracts inside the skill when required; do not generate or install native agent profiles.
- Keep Python evaluation mandatory.
- Keep every DevForgeAI phase, gate, validator, mutation broker, and acceptance decision in the compiled-Rust design.
- Do not convert an existing project skill while implementing this enhancement. Use synthetic fixtures.
- Do not install the enhanced builder or its outputs into operational folders.

These are implementation requirements. They do not claim that the proposed enhancements or Rust runtime already exist.

## 2. Source and baseline

The source specification is:

```text
\\wsl$\Ubuntu\home\bryan\Projects\DevForgeAI\docs\design\specs\SKILL-SPEC-012-skill-generator.md
```

Its observed raw-byte SHA-256 is:

```text
893feaa938c45f228c7b571afe5bf4aaf469fdc61bc6bc2c9b0c011e9d88a96f
```

The existing builder's observed build-manifest SHA-256 is:

```text
5b39ca1a7e2833fa147101aa42d6ba6b185932b419bb457f811117f9e2ec5519
```

The existing builder contains a Python JSONL runner, two deterministic graders, required fixtures, artifact bindings, and regression tests. Its current workflow supports import only. Its runner requires both `package_links` and `manifest_accounting`, which cannot honestly represent a specification-only build without interface changes.

Observed host: Windows PowerShell, Codex CLI `0.154.0`. CLI identification and help succeeded with temporary-directory access warnings. This identifies the host; it does not qualify isolation, hooks, or framework enforcement.

### Source-feature disposition

| Source functionality | Required treatment |
| --- | --- |
| Cold-session generation | Adopt: explicit inputs and recorded decisions must make a build understandable without prior conversation history. |
| Specification resolution | Adapt: explicit file selection or bounded, unambiguous lookup by `skill_name`. |
| Specification-gap reporting | Adopt with exact source locations, affected outputs, and required resolutions. |
| Neutral package and two provider adapters | Replace with one Codex development package. |
| Requirement and provenance recording | Adopt as external evidence with actual source and output digests. |
| Worker-contract generation | Adapt to skill-local task contracts and available Codex delegation. |
| Resource inventory and templates | Adopt only resources required by the selected contract. |
| Regeneration and repair reports | Adopt with recorded ownership and three-way comparison. |
| Trigger examples | Adopt as separately evaluated routing examples. |
| Fixed six-worker workflow and prescribed file counts | Exclude. They describe the source generator's implementation, not a requirement of this builder. |
| Sequencer, hooks, registry admission, promotion, and rewind | Exclude from the executable skill; retain authority requirements in the Rust design. |
| Evaluation `skip` mode | Exclude. Required Python evaluation cannot be skipped for a completed build. |
| Legacy hook-dependent fixtures | Replace with self-contained synthetic fixtures. |
| Blanket "no interview" or "no human review" rules | Replace with focused gap resolution while honoring existing authorization. |
| Verbatim worker-prompt copying | Replace with preservation of domain meaning and explicit host adaptation. |
| Fixed frontmatter field count | Replace with fields supported by Codex and the required installed structural checker. |

Resolve the source document's contradictions explicitly:

- Producer workers may write assigned candidate files; a rule declaring every worker read-only is not carried forward.
- Required frontmatter is `name` and `description`. Do not insert empty optional fields to reach a count.
- A Markdown check, Python observation, or hook mention does not establish DevForgeAI enforcement.
- Report actual next actions; do not emit unavailable `/skill-validate`, phase, or promotion commands.
- Each negative fixture must contain the defect its expected result describes.
- Recording a dependency hash is distinct from verifying that dependency.

## 3. Invocation, inputs, and scope

### ENH-01 - Select the requested operation

Support requests equivalent to:

```text
Use $skill-builder to import the Claude skill at <directory>
into this project's development skills.
```

```text
Use $skill-builder to build the Codex skill specified in
<specification.md> into this project's development skills.
```

```text
Use $skill-builder to regenerate <target-name> from
<specification.md>, using the previous build evidence and <review-report>.
```

These are natural-language requests, not a new command-line parser or registered slash commands.

Selection rules:

- A selected Claude package and an import request select import mode.
- A selected specification and a build request select specification-build mode.
- Supplying both without identifying the governing operation requires clarification before candidate generation.
- Explanation, comparison, specification authoring, installation, and unrelated editing requests do not select a build operation.
- Preserve the existing skill name, `skill-builder`; do not introduce a renamed copy.

### ENH-02 - Resolve inputs and authorization

Require an identified target project root. Use the current project when unambiguous.

For import mode, retain the existing source-package, inventory, exclusions, and file-disposition requirements.

For specification-build mode:

- Prefer an explicitly supplied specification path.
- If the user supplies only a skill name, inspect permitted Markdown files beneath `docs/plan` and `docs/design/specs` for a matching frontmatter `skill_name`.
- Search both locations. Exactly one match is required; do not resolve duplicate matches by directory precedence.
- Missing search directories contribute no matches.
- Exclude backup directories and links before recursion.
- Zero or multiple matches produce a gap report listing the missing identifier or concrete candidates.

A current user request to build from a selected specification supplies authoring authorization. Record the instruction, selected path, and input digest. A document's `status: approved`, filename, or title alone does not authorize mutation.

Current user instructions take precedence over stale document metadata. Record any resolved discrepancy. Substantive unresolved requirements still produce gaps; authorization does not supply missing domain decisions.

Use an explicitly requested target name or the specification's unambiguous declared skill name. Do not silently derive a competing identity from a filename.

### Write boundaries

Generated packages belong under:

```text
src/agents/skills/<target-name>/
```

Preserve existing import evidence under:

```text
docs/plan/skill-imports/<target-name>/<run-id>/
```

Use the corresponding location for specification builds:

```text
docs/plan/skill-builds/<target-name>/<run-id>/
```

Candidate staging, snapshots, reports, and evaluation outputs belong in the selected run's evidence directory.

Do not write operational `.agents`, `.claude`, `.codex`, personal skill directories, hook configuration, or remote repositories. Disposable evaluation projects are permitted only within the explicitly scoped test workspace.

Do not inspect backup content or excluded legacy CLI/hook implementations.

## 4. Normalize specifications and record gaps

### ENH-03 - Extract a traceable build contract

Before generating candidate files, create `build-contract.json` in the evidence directory.

Use UTF-8 JSON with `schema_version: "1"` and these top-level fields:

| Field | Required content |
| --- | --- |
| `mode` | `import` or `spec_build`. |
| `target_name` | Resolved Codex skill name. |
| `inputs` | Input IDs, resolved paths, roles, byte counts, and raw-byte SHA-256 values. |
| `authorization` | Relevant user instruction and the input IDs/digests it authorizes. |
| `purpose` | Capability being built. |
| `activation` | Positive requests and exclusions. |
| `requirements` | Requirement records defined below. |
| `artifacts` | Planned package files defined below. |
| `workers` | Required task contracts, or an empty array. |
| `dependencies` | Required external resources/capabilities and their observed availability. |

Each requirement contains:

- Unique `id`.
- `origin`: `source` or `derived`.
- Exact requirement meaning in `text`.
- `source_refs`.
- `rationale` for a derived implementation constraint.
- Package `artifact_paths` carrying the requirement.
- Concrete `verification` methods and expected observations.

Preserve source requirement IDs when unique. Otherwise assign `req-0001`, `req-0002`, and subsequent IDs in source order. These IDs belong to the digest-bound contract; do not claim they remain stable after arbitrary specification changes.

Each source reference contains:

```text
input_id
start_byte
end_byte
sha256
```

Byte ranges are zero-based, end-exclusive ranges into the original input bytes. The reference digest hashes exactly that byte slice, without newline normalization. Reports may also display derived line numbers.

Separate source requirements from implementation decisions. Do not present an inferred constraint as a quotation or requirement from the source.

Each planned package artifact contains:

```text
path
role
requirement_ids
purpose
```

Paths are package-relative, use forward slashes, and identify concrete files. Do not create empty resource directories or count-based scaffolding.

The normalized contract must cover purpose, activation, inputs, outputs, domain rules, side effects, recovery behavior, and required capabilities. A field may be explicitly not applicable with a reason. Silence is not a resolved decision.

### ENH-04 - Produce actionable gaps

When necessary information is missing or contradictory, write `spec-gaps.json` and render its contents under `SPEC GAPS` in the report.

Each gap contains:

```text
id
reason_code
source_refs
requirement_ids
affected_outputs
description
required_resolution
```

Supported reason codes:

- `MISSING_INPUT`
- `AMBIGUOUS_INPUT`
- `CONTRADICTORY_REQUIREMENT`
- `UNSUPPORTED_CAPABILITY`
- `SOURCE_CHANGED`
- `TARGET_COLLISION`
- `REVISION_CONFLICT`
- `INVALID_EVIDENCE`

A gap report may be written before generation. Candidate package files must not be generated while a blocking contract gap remains.

Record supplied answers as additional digest-bound decision evidence. Do not silently edit the original specification, repeat already answered questions, or impose an interview count.

### Dependency handling

Read only dependencies necessary to interpret or implement the selected contract and within the authorized boundary.

Record availability and digest verification separately. A supplied digest using an unspecified algorithm is not verified.

If an unavailable dependency is essential, report a gap. If it is unnecessary to the selected behavior, record why it was not used. Do not invent replacement behavior.

## 5. Generate the Codex package

### ENH-05 - Generate required resources

Keep the entrypoint concise and focused on:

- Capability and activation.
- Input resolution.
- Essential domain decisions.
- Resource routing.
- Actual execution and result contracts.

Put detailed schemas, task contracts, examples, and conditional procedures in supporting resources.

Create references, templates, assets, and scripts only when the selected contract requires them. Preserve existing useful resources and supported metadata during authorized revisions.

Required frontmatter is `name` and `description`. Preserve supported optional values when useful. Do not invent a license, version, tool restriction, or provider policy.

Use `agents/openai.yaml` only when required metadata or invocation policy warrants it. Preserve automatic invocation unless the user explicitly selects otherwise. Codex documents this metadata separately from the skill body. [Official skill documentation](https://learn.chatgpt.com/docs/build-skills)

Do not generate:

- A neutral `skill.yaml` solely to imitate the source architecture.
- Claude adapters.
- Native Codex TOML profiles.
- Installation maps.
- Framework phase dispatchers.
- Calls to unimplemented DevForgeAI commands.

### ENH-06 - Preserve worker behavior without claiming enforcement

When the specification requires workers, generate task contracts under:

```text
references/workers/<role>.md
```

Each contract states:

- Responsibility and associated requirement IDs.
- Inputs.
- Expected output and return format.
- Assigned candidate paths, if any.
- Required tools.
- Whether independent execution is essential.
- Any required isolation property.
- Concrete error and incomplete-result behavior.

The main skill loads and delegates these contracts through available Codex subagent tools. Do not prescribe a fixed worker count.

Sequential execution is allowed only when it preserves the declared behavior and independent execution is not essential.

A task-contract file is not an installed agent profile and does not enforce tool or filesystem restrictions. Codex documents custom profiles and inherited sandbox behavior separately. [Official subagent documentation](https://learn.chatgpt.com/docs/agent-configuration/subagents)

An essential identity, isolation, or permission property unavailable in the current terminal produces `UNSUPPORTED_CAPABILITY` before candidate generation. Do not replace it with stronger-sounding prose.

## 6. Provenance, ownership, and regeneration

### ENH-07 - Record actual provenance

Create `build-provenance.json` after generation and evaluation.

It contains:

- Schema version and run ID.
- Operation and target identity.
- Builder manifest digest.
- Input and normalized-contract digests.
- Dependency verification results.
- Requirement-to-output-to-evaluation mappings.
- Output paths and actual delivered digests.
- Generated-baseline paths and digests.
- Ownership classification.
- Prior successful build reference, when revising.
- Result and evidence references.

Keep provenance outside the generated package unless the selected skill's runtime contract requires it. Do not inject comments or metadata into arbitrary output formats merely to mark ownership.

An ownership row distinguishes:

- `generated`: the builder owns regeneration of that path.
- `retained_user`: an existing unrelated file preserved without claiming ownership.

For generated files, store the new generated candidate bytes separately from the actual delivered bytes. This distinction matters when unchanged generation retains a user's edit.

Keep source inputs unchanged and verify their bytes again before reporting completion.

### ENH-08 - Regenerate without destroying unrelated edits

Require revision authorization and the previous successful build evidence.

For each previously generated path, compare:

- **B:** Last successful generated baseline.
- **C:** Current destination bytes or absence.
- **N:** New proposed generated bytes or absence.

Apply rules in this order:

| Condition | Result |
| --- | --- |
| A proposed path is occupied but not previously owned | Conflict, including identical bytes. |
| `C = B` | Use `N`. |
| `C = N` | Keep `C`. |
| `N = B` | Keep `C`, preserving the user's change. |
| Otherwise | Conflict. |

Absence is a distinct value. If a result would omit a currently required artifact, treat it as a conflict.

Consequences:

- An unchanged, previously owned obsolete file may be removed.
- A modified obsolete file conflicts.
- An unrelated file remains unchanged.
- Conflicting changes to the same owned file require resolution.
- Missing or invalid baseline evidence blocks regeneration; do not silently adopt current files as a generated baseline.

Record comparisons and proposed actions in `revision-plan.json`, including path, ownership, B/C/N digests, action, and reason.

Generate and evaluate the candidate before changing destination files. If conflicts exist, retain candidate evidence and leave the destination unchanged.

Before the first destination edit, recheck existence, type, and bytes for every affected path. Changed observations cause a conflict without destination writes.

Recheck each path immediately before its sequential mutation. If a later change or write error occurs:

- Stop remaining writes.
- Record the actual applied delta.
- Retain the failed run's evidence.
- Do not promise automatic rollback or package-wide atomicity.
- Do not advance the successful baseline.

After successful application, required evaluation, and readback, update the active development baseline reference. This reference is editable development evidence, not an authoritative framework record.

A retry after partial application uses the last successful B, actual current C, and new N. It links the prior failed delta; it does not redefine B from partially applied output.

## 7. Mandatory Python evaluation interfaces

### ENH-09 - Extend the existing evaluator

Retain the existing case-record shape:

```json
{
  "case_id": "unique-id",
  "grader_id": "registered-grader",
  "params": {},
  "expected": "PASS"
}
```

Add an explicit `--profile` argument to `scripts/run_evaluation.py`.

| Profile | Exact required grader set |
| --- | --- |
| `legacy-import-v1` | `package_links`, `manifest_accounting` |
| `import-v2` | `package_links`, `manifest_accounting`, `build_traceability` |
| `spec-v1` | `package_links`, `build_traceability` |
| `revision-import-v2` | Import-v2 graders plus `revision_consistency` |
| `revision-spec-v1` | Spec-v1 graders plus `revision_consistency` |
| `builder-v2` | All five graders, including `routing_outcomes` |

Omitting `--profile` selects `legacy-import-v1`, preserving existing invocation syntax and case files. The enhanced skill must explicitly select its applicable new profile. Legacy-profile evidence does not satisfy the enhanced completion requirements.

New evaluator output uses evidence schema version `"2"` and records the selected profile and version. Historical version-1 evidence remains unchanged. This is an explicit output-schema change; do not label it byte-compatible with version 1.

Bind profile definitions, grader versions, schemas, scripts, fixtures, expected results, and tests in the builder's version-2 build manifest.

Missing, unknown, duplicate, or omitted required profile/grader information produces `ERROR`. Do not fabricate Claude manifests for specification builds.

Retain:

- Strict JSONL parsing.
- Rejection of duplicate keys and non-finite values.
- Artifact verification before grader execution.
- Execution of the verified grader bytes.
- Bounded paths and snapshot sizes.
- New-file-only evidence output.
- No arbitrary command selection from case input.
- Exit 0 for matched observations, 1 for mismatches, and 2 for execution/configuration errors.

### New grader responsibilities

| Grader | Required observations | Explicit limit |
| --- | --- | --- |
| `build_traceability` | Input and excerpt hashes match; referenced requirement IDs exist; required artifact mappings resolve; delivered output digests match; cited evaluation evidence belongs to the identified run/package. | Does not prove that extracted requirements or generated prose preserve meaning. |
| `revision_consistency` | B/C/N classification follows the specified rules; unrelated files remain unchanged; conflicted runs have no destination delta; successful baseline publication follows successful readback. | Does not broker mutations or grant acceptance. |
| `routing_outcomes` | Observed routing decisions match fixture expectations by case ID; missing or duplicate results are errors. | Classification results are not proof of native implicit skill discovery. |

The installed Skill Creator `quick_validate.py` check remains mandatory for the builder and each completed generated skill. Resolve its actual installed location; do not hardcode this workstation's Codex home into the distributed skill.

Retain Python 3.10 or newer for local evidence tooling. Keep runner/graders standard-library-only. Record the separate PyYAML dependency of the installed structural checker.

Every new or changed script must have executed, meaningful tests.

### Rust authority boundary

Python may parse evaluation inputs, inspect bytes, compute deterministic observations, and write assigned evidence.

Python must not:

- Advance a DevForgeAI phase.
- Enforce a framework gate.
- Act as a DevForgeAI validator.
- Broker framework mutations.
- Write authoritative state.
- Issue acceptance.

The compiled-Rust design must describe independent validation of profile identity, artifact completeness, provenance, observations, and required thresholds. No proposed Rust command becomes a dependency of the enhanced skill before that runtime exists.

## 8. Verification and completion requirements

### ENH-10 - Deterministic regression coverage

Retain existing regression behavior and add cases covering:

- Explicit specification selection, missing matches, and ambiguous lookup.
- Missing domain decisions and contradictory requirements.
- Input mutation after contract extraction.
- Invalid source byte ranges and excerpt digests.
- Missing, duplicate, and unknown requirement IDs.
- Missing outputs and stale output digests.
- Unsupported essential worker isolation.
- Each evaluation profile and omitted required graders.
- Historical case-file compatibility and version-2 output.
- Unowned-path collision, including identical bytes.
- Every B/C/N comparison branch.
- Modified obsolete files and missing required artifacts.
- Destination drift before application.
- Partial application without baseline advancement.
- Retry using the last successful baseline.
- Malformed provenance, revision, and routing evidence.

Use actual fixture bytes and observable results. Do not replace these tests with wording, heading-count, or keyword checks.

### Independent forward trials

Use independent Codex agents with the enhanced skill, realistic requests, and raw synthetic inputs. Do not supply the intended solution.

Require these trials:

1. **Import:** Convert a synthetic Claude package containing a JSON output contract and a decimal CSV aggregation script. Exercise the resulting script; verify decimal totals, schema behavior, file accounting, and source preservation.
2. **Specification build:** Build the equivalent capability from approved Markdown. Exercise the generated script and inspect requirement/output/evaluation traceability.
3. **Revision:** Modify an owned file and add an unrelated file. Observe a conflict and unchanged destination. Resolve the specific conflict, retry, and verify retention of the unrelated file.

Run trials in disposable projects. Temporary `.agents/skills` copies used exclusively for these trials do not install anything into the real project or user skill directories.

Use existing Codex authentication and normal sandbox controls. Do not bypass approvals, hook trust, or rules. Capture CLI version, exact arguments, stdout/stderr, final outputs, and errors. If a required trial cannot execute, report it unperformed or errored and leave enhancement verification incomplete.

Evaluate routing separately for:

- Import.
- Specification build.
- Authorized regeneration.
- Explanation.
- Specification authoring.
- Installation.
- Unrelated editing.

Record routing classification separately from observed native activation. Do not infer activation from a model merely mentioning the skill.

### Editorial verification

Read all changed instructions and supporting resources to establish that:

- Domain requirements remain traceable.
- Commands refer to implemented, available interfaces.
- Worker instructions describe actual delegation behavior.
- No ritual counts, invented context measurements, or self-certified compliance flags were introduced.
- No prose claims to enforce runtime authority.
- No generic assurance replaces a concrete result or failure condition.

This review is a recorded assessment, not a mathematical proof of future model behavior.

### Completion report

Report separately:

- Authoring status.
- Structural checks.
- Deterministic evaluation.
- Supporting-script execution.
- Independent forward trials.
- Routing evaluation.
- Rust implementation and qualification.
- Operational installation.

A completed enhancement requires successful structural checks, required deterministic profiles, meaningful script tests, and the specified forward trials. Missing execution or unresolved conflicts cannot be hidden by a completion label.

Rust implementation remains `NOT_IMPLEMENTED`, and operational installation remains `NOT_PERFORMED` for this enhancement task.

## 9. Document delivery and implementation handoff

The approved document-delivery task saves this specification and a companion command/research log in `docs/plan`. The log contains:

- Exact commands and working directories.
- Returned exit codes, warnings, and output.
- Explicit labels for truncated output or excerpts.
- Interpretation of each result.
- Source and baseline hashes.
- The UNC read/hash denial and successful approved retry.
- Official documentation URLs and retrieval results.
- The four user decisions captured during planning.

The specification-writing task changes documentation only. It does not modify the builder, rebuild its manifest, convert a project skill, execute forward trials, or install anything.

The later `$skill-creator` enhancement task updates the existing skill in place, implements the specified evidence interfaces, executes the required checks, regenerates the manifest after intentional edits, and records the resulting evidence.

Preserve historical research logs, authoring logs, and previous evaluation outputs. They remain evidence for their original artifact versions.
