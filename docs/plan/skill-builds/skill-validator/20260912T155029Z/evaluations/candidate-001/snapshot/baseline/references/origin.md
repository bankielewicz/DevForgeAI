# Origin and source preservation

### SV-001/SV-002: existing and reconstructed origin

Read an existing specification before judging conformance. Preserve it unchanged, record its digest, and identify differences between intended behavior and observed implementation. A missing explicit specification path is an input error, not permission to silently reconstruct another one. An ambiguous lookup is also not absence.

When no specification exists, generate `origin-spec.md` describing current observed behavior before proposing enhancements. Include identity, purpose, triggers/non-triggers, inputs/defaults, output formats, workflow steps, resources, dependencies, side effects, recovery, known defects, supported environments, representative cases, and reconstruction instructions. Cite actual source files for observations. Mark inferred intent and unresolved decisions explicitly. Do not launder an existing defect into an approved requirement merely by describing it.

The origin specification documents functional reconstruction. Exact restoration uses the separately captured `source/` bytes and manifest. Neither prose nor a digest alone is a backup. Declare snapshot completeness and excluded boundaries; do not claim full restoration when material files or dependencies were omitted.

Reuse verified provenance rather than building a competing history. With no history, start an `observed` record dated at this run, with `historical_origin: unknown`. A validator-generated origin is not an adopted baseline or a previous successful generated build. Any first repair relying on adoption follows the companion project adoption specification.

Recheck the original target's permitted file set, sizes, and raw-byte hashes after assessment. If it changed, preserve the assessed snapshot and label the report `SOURCE_CHANGED`; conclusions apply only to the recorded snapshot. Do not publish builder-ready status until a new run assesses the intended current bytes. Recheck origin and rule input digests too. Do not change a baseline to conceal drift.

## Operational capture

Use `python -B -X utf8 <loaded-validator>/scripts/observe.py --help` and each subcommand's `--help`. Snapshot example in PowerShell (substitute actual absolute paths):

```powershell
python -B -X utf8 "$validator/scripts/observe.py" snapshot --source "$target" --output "$newRun"
python -B -X utf8 "$validator/scripts/observe.py" structure --source "$newRun/source"
python -B -X utf8 "$validator/scripts/observe.py" readback --source "$target" --manifest "$newRun/source-manifest.json"
```

The host selects these variables from the authorized request; they are not environment requirements. The snapshot directory must not already exist. Record shell redirections as effects outside the target. Subsequent helper commands only emit JSON stdout/diagnostics stderr and do not write reports themselves. Helper exits: 0 completed observations without required deterministic mismatch; 1 mismatch; 2 usage/access/dependency/execution failure. Exit 0 does not establish semantic or behavioral PASS.

For resolution, read only permitted candidate Markdown frontmatter in the two lookup roots; exclude evidence snapshots that are historical captures rather than candidate project specifications and record that scope. Do not infer a specification from filename alone. Validate frontmatter identity and present competing plausible originals without precedence. Missing explicit input does not trigger reconstruction. Verify all relevant successful evidence references and current output hashes before calling history generated; preserve unknown history when verification is incomplete.

The companion adoption specification is a separately selected project input, normally `docs/plan/skill-builder-adoption-spec.md`. Locate and read it only when an adoption-dependent future revision is relevant; do not treat its existence as implemented capability or authorization. Operational builder copies remain read-only.
