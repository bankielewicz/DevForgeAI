# Specification builds and shared build contracts

Read this reference for specification selection and for the contract/provenance used by both authoring modes. Machine field shapes are maintained in [evaluator-contracts.md](evaluator-contracts.md); use those shapes rather than inventing parallel metadata.

For an existing package without successful generated provenance, explicit adoption is a separate operation described in [adoption.md](adoption.md). A validator's origin or revision specification is an input, not a generated baseline or user authorization. An adoption-origin revision retains this schema-1 build contract and uses schema-2 provenance plus `revision-spec-v2` evaluation. Require its published origin and separately authorized revision before generation/application.

## Resolve a specification

Accept an existing Markdown document. Do not demand a replacement template. An explicitly selected path takes precedence over lookup; read the actual file within the authorized scope. If only a skill name is supplied, inspect permitted Markdown frontmatter for an exact `skill_name` match under both `docs/plan` and `docs/design/specs`. Missing directories contribute no matches. Exclude backup directories and links before recursion. Exactly one match is required; report zero or multiple matches without directory precedence.

The evidence-only helper implements this lookup:

```text
python -B -X utf8 "<builder>/scripts/build_evidence.py" resolve-spec --project-root "<project>" --spec "<selected-file>"
python -B -X utf8 "<builder>/scripts/build_evidence.py" resolve-spec --project-root "<project>" --name "<skill-name>"
```

Choose one form. Replace placeholders with resolved paths and the requested name. The helper writes JSON to stdout: exit 0 identifies one selected file, exit 1 reports missing/ambiguous selection, and exit 2 reports invalid input, unavailable dependency, or access error. Frontmatter lookup requires PyYAML; do not install it without existing authorization. Preserve the output in the command log. A resolver result does not establish specification approval or completeness.

Use the requested target name or the specification's unambiguous declared skill name. Record a mismatch with stale metadata and the current user instruction resolving it. Neither a filename nor `status: approved` grants mutation authority. Clarify an unresolved substantive mismatch before generating candidate files.

## Extract the contract before generation

Write `build-contract.json` in the run's evidence directory. Capture original inputs as raw bytes and bounded evaluation copies. The contract records both original resolved paths and snapshot-relative paths. It covers purpose, activation, inputs/defaults, outputs/schemas, domain rules, side effects, recovery, required capabilities, worker contracts, dependencies, and the planned package files. Express these properties in the applicable requirements; use a reasoned not-applicable statement where a property does not apply.

The input helper computes real metadata and optional source-reference slices:

```text
python -B -X utf8 "<builder>/scripts/build_evidence.py" input-record --file "<original-file>" --id "<input-id>" --snapshot-path "inputs/<filename>" --role spec --start-byte 0 --end-byte <actual-byte-length>
```

Use `--role source` for an imported source file; omit the byte-range arguments when only an input record is needed. The helper returns `input` and, when requested, `source_ref` records. It observes the original file and does not copy it; create the separately bounded snapshot with ordinary authorized file operations and verify its bytes match. Byte offsets are zero-based and end-exclusive. SHA-256 covers exactly the original bytes or selected slice, without decoding/newline normalization. Use an excerpt's actual interval for a specific requirement. Do not calculate byte offsets from character counts.

Preserve unique source requirement IDs. Otherwise assign `req-0001` and subsequent IDs in source order. Their identity is bound to this input digest; arbitrary edits do not guarantee stable IDs. Mark requirements `source` or `derived`; derived requirements carry a rationale. A source requirement must have a real source reference, not an invented quotation. Record user clarifications as additional digest-bound input documents without editing the original specification.

Each requirement maps to concrete package artifacts and a verification method with an expected observation. The artifact inventory maps back to the same requirements and records each file's role and purpose. Requirements without outputs and outputs without a justified requirement are unresolved design gaps, not reasons to create filler files.

Before generation, inspect needed dependencies within scope. Record capability availability separately from digest verification. A digest without an identified algorithm or unread bytes is not verified. An essential unavailable dependency is a gap; an unused dependency records why it is irrelevant to this selected behavior.

## Gaps

Write `spec-gaps.json` as UTF-8 JSON with `schema_version: "1"` and a `gaps` array. Each record has `id`, `reason_code`, `source_refs`, `requirement_ids`, `affected_outputs`, `description`, and `required_resolution`. Use empty reference/requirement arrays only when the relevant input or requirement cannot yet be identified. Render the same facts under `SPEC GAPS` in the report.

Use these reason codes:

| Code | Meaning |
| --- | --- |
| `MISSING_INPUT` | Required input or substantive decision absent. |
| `AMBIGUOUS_INPUT` | Competing selected inputs, names, or lookup matches. |
| `CONTRADICTORY_REQUIREMENT` | Requirements cannot be satisfied together. |
| `UNSUPPORTED_CAPABILITY` | An essential terminal, dependency, identity, permission, or isolation property is unavailable. |
| `SOURCE_CHANGED` | Observed input bytes differ from the bound contract. |
| `TARGET_COLLISION` | An occupied destination lacks applicable ownership/revision authorization. |
| `REVISION_CONFLICT` | B/C/N comparison or destination drift requires resolution. |
| `INVALID_EVIDENCE` | Required baseline, contract, or execution evidence is absent or invalid. |

Do not generate candidate package files while a blocking contract gap remains. Gap records and source inventories may be retained before generation. Record the concrete answer that resolves a gap and preserve its history; do not repeat answered questions or impose an interview count.

## Workers and resource generation

Generate worker contracts only for required worker behavior, at `references/workers/<role>.md`. Adapt [worker-task-template.md](../assets/worker-task-template.md). State the responsibility, requirement IDs, inputs, outputs/return format, assigned candidate paths, required tools, essential independence, required isolation, and failure behavior.

Producer workers may write only their assigned candidate paths under existing authorization. Read-only reviewers receive no candidate write assignment. Use available Codex subagent tools; do not prescribe a fixed count or imply that a task contract installs an agent profile. Sequential execution is allowed only when independence is not essential and it preserves the selected behavior. An unavailable essential identity, isolation, or permission property blocks generation.

Keep conditional details in linked references, reusable output material in assets, and implemented ordinary automation in scripts. Do not create both provider adapters, neutral manifests, native agent profiles, or empty resources merely because the source generator specification listed them. Preserve domain meanings while adapting host-specific execution.

## Provenance and output ownership

After candidate generation and the preceding structural/script observations, create `build-provenance.json` using the machine contract. Record actual input, contract, builder-manifest, output, generated-baseline, dependency, and cited-evidence digests. Cite preceding observation files with this run ID, target name, and matching output digests. Store final evaluator JSONL outside its candidate root and link it from the report; input provenance must not cite a future result or its own digest.

Keep generated baseline bytes separate from the delivered package. A regeneration can retain a user edit when generation has not changed; the delivered and generated hashes then differ. Claim ownership only for `generated` paths; unrelated existing files are `retained_user`, never silently adopted.

Keep provenance, command logs, and baseline pointers outside the generated skill unless its runtime contract requires them. They are editable development evidence. Required evaluation and readback determine whether this build report can say complete; they do not implement a DevForgeAI validator, mutation broker, gate, or acceptance decision.
