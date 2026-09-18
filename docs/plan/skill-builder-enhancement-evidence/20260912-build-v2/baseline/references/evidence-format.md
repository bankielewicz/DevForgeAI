# Import Evidence Format

Use this format for an authorized conversion. Evidence documents what was read, changed, checked, or left unresolved. It is not a protected acceptance record.

## Evidence directory

Use `docs/plan/skill-imports/<target-name>/<UTC-timestamp>/` beneath the identified project root. Use a filesystem-safe UTC timestamp such as `20260912T034239123Z`. If occupied, select a new timestamp before writing; never reuse another run's evidence directory silently.

Create these artifacts:

- `source-manifest.json`
- `source-after-manifest.json`
- `file-dispositions.json`
- `conversion-report.md`
- `command-log.md`
- `destination-manifest.json`
- `evaluation-cases.jsonl`
- `evaluation-results.jsonl`

For an authorized revision, also create `destination-before-manifest.json` before changing target files. Keep unrelated files and edits; record additions, modifications, and authorized removals in the report. Do not merge unrelated source/target identities without a user decision.

## Inventory boundary

Record absolute resolved source/project/destination roots and excluded boundaries before traversing the package. Enumerate permitted directories only. Detect links/junctions before recursion and do not follow them out of scope. Do not descend into backup or excluded legacy implementation directories merely to count their files.

Record excluded directories and links as boundary entries with reasons. A boundary entry is not a claim that every file below it was inspected. If exclusion prevents understanding an essential dependency, report that limitation.

## Manifests

Use UTF-8 JSON with `schema_version: "1"`. A manifest contains:

| Field | Content |
| --- | --- |
| `root` | Absolute resolved root represented by this manifest. |
| `captured_at_utc` | Actual ISO-8601 capture time. |
| `files` | Permitted regular-file entries sorted by relative path. |
| `excluded_boundaries` | Path, kind (`directory` or `link`), and reason; no invented content hashes. |

Each `files` entry has `path` (forward-slash relative path), `bytes`, and `sha256` (lowercase 64-character digest of raw bytes). Never hash an excluded file to satisfy completeness. Capture reparse-point metadata without reading its target when recording a link boundary.

For an ordinary allowed file, PowerShell's `Get-Item -LiteralPath` and `Get-FileHash -LiteralPath ... -Algorithm SHA256` supply size and digest. Construct JSON using PowerShell objects and `ConvertTo-Json` or equivalent available tooling; do not hand-invent hashes or concatenate unescaped source text into commands.

At readback, capture `source-after-manifest.json` and compare its source file set, sizes, and hashes to the original manifest. Record the comparison and any changes in the report. Do not rewrite the baseline to conceal changes. Capture the destination manifest after the authored package is stable; the evidence directory itself is outside that hash set.

## File dispositions

Use `schema_version: "1"` and a `files` array in `file-dispositions.json`. Each permitted source file has exactly one entry:

| Field | Content |
| --- | --- |
| `source_path`, `source_sha256` | Match the source manifest. |
| `role` | Entrypoint, reference, schema, template, asset, or supporting script. |
| `disposition` | `PRESERVE`, `REWRITE`, `CONSOLIDATE`, `OMIT`, or `DEFER`. |
| `target_paths` | Destination-relative files; empty only for omitted/deferred material. |
| `rationale` | Specific reason for this treatment. |
| `behavior_preserved_or_changed` | Domain/interface behavior affected. |
| `dependencies` | In-package references or external capabilities, with their disposition. |
| `planned_verification` | Intended observation/check; this field does not mean it was run. |
| `performed_review` | What was actually inspected, evidence references, and unresolved limits. |

`PRESERVE` requires equal source/destination bytes. `CONSOLIDATE` names every resulting target that carries the retained behavior. Trace callers before `OMIT`. `DEFER` records absent work; an essential unresolved dependency requires overall `BLOCKED`.

Record new target-only files and their purpose in the conversion report. Do not fabricate a source file for them. Do not use a schema/body field named PASS as evidence of runtime execution.

## Conversion report

Copy [the report template](../assets/conversion-report-template.md) into the evidence directory and replace its bracketed fields with observed information. Use `NOT_PERFORMED`, `NOT_APPLICABLE`, or `UNKNOWN` with a reason where appropriate; do not leave scaffold text or invented facts.

Include the contract before rewriting, source/target name mapping, capability decisions, file dispositions, ceremony removed, preserved output schemas, blockers, source readback, and target manifest. Link to evidence using paths relative to the report.

Use independent states:

| Dimension | Allowed states and meaning |
| --- | --- |
| Conversion | `NOT_STARTED`, `IN_PROGRESS`, `COMPLETE`, `BLOCKED`; `COMPLETE` requires the declared conversion scope and successful required structural, deterministic, and changed-script checks. |
| Structural checks | `NOT_PERFORMED`, `PASSED`, `FAILED`; name the actual check and its execution evidence. Manual authoring readback is listed separately. |
| Deterministic evaluation | `NOT_PERFORMED`, `PASSED`, `FAILED`; name the runner, artifact digests, cases, JSONL observations, and execution errors. Incomplete or errored required execution is not `PASSED`. |
| Behavioral evaluation | `NOT_PERFORMED`, `PASSED`, `FAILED`; requires executed task cases and results. |
| Framework enforcement | `NOT_IMPLEMENTED` for this design-only runtime boundary. No acceptance claim is issued. |
| Operational installation | `NOT_PERFORMED`; installation is outside this workflow. |

The Skill Creator Python structural check and bundled Python deterministic evaluation are required. A missing check, missing artifact, failed observation, or execution error prevents reporting a completed build. Record changed-script exercises with their concrete inputs, outputs, and side effects. Update the report's validation sentence and state table together from actual execution evidence. Structural and deterministic success does not imply that semantic task cases ran or that Rust enforcement exists.

Follow [evaluation.md](evaluation.md) for artifact binding and the supported case format. Keep case definitions, grader observations, and command output in the evidence directory. Record the runner and grader digests used in that execution. These workspace files provide reproducible development evidence, not protected provenance or framework acceptance.

## Command log

For each shell operation, record timestamp, cwd, exact command, purpose, exit code, stdout, stderr, and interpretation. A running command has no final exit code until it completes. Record retries separately. Do not run commands merely to populate a log.

If the tool returns one combined output stream, label it combined; do not invent stdout/stderr separation. Keep complete output when practical. For long output, save a separate artifact and link it; label excerpts and any tool truncation. Redact credentials/private values and label the redaction rather than silently altering evidence.

For tool-based edits, record the tool, affected paths, action, returned result, and readback. The tool transcript contains the exact patch; the final destination manifest identifies the resulting bytes. Do not describe a successful edit call as successful skill execution.

For web lookups, record the exact query/URL, fetched page and section, retrieval result/date, and interpretation. Use factual citations near the conversion decision they support. Do not browse when local evidence already resolves the mapping.

## Partial work

Preserve partial evidence and target files when blocked; list them explicitly. Do not delete another run's artifacts or write a completion record over an unresolved dependency. Report the precise missing decision/capability and which outputs are usable drafts. Never claim a schema-valid or accepted output if that operation was not performed.
