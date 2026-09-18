---
template_version: 1.0
format_version: 1.0
story_id: STORY-661
generated_at: "2026-05-08T16:00:00Z"
generated_by: devforgeai-validate generate-qa-recommendations
---

<!-- SECTION_MANIFEST
# Recommendation entry YAML schema — used by Blocking and Advisory sections:
#   required:
#     - id (format: REC-{STORY}-{severity-initial}-{3-digit-seq})
#     - severity (enum: CRITICAL, HIGH, MEDIUM, LOW)
#     - provenance (enum: GROUNDED, DERIVED, INCONCLUSIVE)
#     - title (string, 10-120 chars, no aspirational language)
#     - file (relative path from project root)
#     - line (integer) OR line_range ([start, end] integers)
#     - category (enum: correctness, security, performance, test_quality, coverage, anti_pattern, documentation)
#     - blocking_release (boolean)
#     - remediation (exactly one of: before_code+after_code pair OR remediation_steps list)
#     - verification ({command: string, expected: string})
#     - estimated_effort_minutes (integer)
#     - dependencies (list of REC-IDs; may be empty)
#   optional:
#     - references (list of {source: string, line_range?: [int, int], url?: string})
#     - cycle_first_seen (integer; auto-populated by /qa)
#     - classification (enum: REGRESSION, PRE_EXISTING; allowed on ANY category per
#       iteration-2 broadening decision 2026-05-08 — the regression-vs-pre-existing
#       signal is meaningful triage information regardless of category)
END_SECTION_MANIFEST -->

# QA Recommendations — STORY-661

**Story:** Conviction Worklog Contract via CLI Subprocess Emission
**QA Result:** PASS_WITH_WARNINGS
**Cycle:** 3

## Summary

| Severity | Count |
|----------|-------|
| CRITICAL | 0     |
| HIGH     | 0     |
| MEDIUM   | 2     |
| LOW      | 2     |

## Blocking Recommendations

_None._

## Advisory Recommendations

```yaml
- id: "REC-STORY-661-M-001"
  severity: MEDIUM
  provenance: GROUNDED
  title: "Replace sys.exit(1) with return 1 for consistent CLI exit-code contract"
  file: "src/claude/scripts/devforgeai_cli/commands/emit_conviction_worklog.py"
  line: 631
  line_range: [627, 631]
  category: anti_pattern
  classification: REGRESSION
  blocking_release: false
  before_code: |
    _emit_error(
        [f"target_path resolves outside project_root: {target_path}"],
        code="PATH_TRAVERSAL",
    )
    sys.exit(1)
  after_code: |
    _emit_error(
        [f"target_path resolves outside project_root: {target_path}"],
        code="PATH_TRAVERSAL",
    )
    return 1
  remediation_steps: null
  verification:
    command: "grep -n 'sys.exit(1)' src/claude/scripts/devforgeai_cli/commands/emit_conviction_worklog.py"
    expected: "Only line 686 (the if __name__ == '__main__': sys.exit(main()) entry point) matches; no occurrences inside cmd_emit_conviction_worklog body."
  estimated_effort_minutes: 10
  dependencies: []
  references:
    - source: "RCA-067"
      url: "devforgeai/RCA/RCA-067-framework-recovery-semantics-breakdown.md"
      line_range: [302, 344]
  cycle_first_seen: 3
```

```yaml
- id: "REC-STORY-661-M-002"
  severity: MEDIUM
  provenance: GROUNDED
  title: "Guard Windows fcntl-fallback WARNING behind once-per-session flag to prevent stderr spam"
  file: "src/claude/scripts/devforgeai_cli/commands/emit_conviction_worklog.py"
  line: 213
  line_range: [209, 217]
  category: anti_pattern
  classification: PRE_EXISTING
  blocking_release: false
  before_code: |
    except (ImportError, OSError):
        # Windows or unsupported FS: degrade gracefully; concurrent
        # writes are already serialized by sequential subprocess calls
        # in the documented use pattern.
        print(
            'WARNING: file lock unavailable on this platform; '
            'concurrent emissions may race',
            file=sys.stderr,
        )
  after_code: |
    except (ImportError, OSError):
        # Windows or unsupported FS: degrade gracefully; concurrent
        # writes are already serialized by sequential subprocess calls
        # in the documented use pattern. Emit warning once per process.
        global _LOCK_WARNING_EMITTED
        if not _LOCK_WARNING_EMITTED:
            print(
                'WARNING: file lock unavailable on this platform; '
                'concurrent emissions may race',
                file=sys.stderr,
            )
            _LOCK_WARNING_EMITTED = True
  remediation_steps: null
  verification:
    command: "python3 -c 'import subprocess; out=subprocess.run([\"python\",\"-m\",\"devforgeai_cli.cli\",\"emit-conviction-worklog\",\"--help\"],capture_output=True); print(out.stderr.decode().count(\"WARNING: file lock unavailable\"))'"
    expected: "0 (no warning on --help) or 1 (single warning even after multiple invocations within the same process)"
  estimated_effort_minutes: 30
  dependencies: []
  references:
    - source: "STORY-661 cycle 1 commit c5eaf571"
      url: "src/claude/scripts/devforgeai_cli/commands/emit_conviction_worklog.py"
      line_range: [213, 217]
  cycle_first_seen: 3
```

```yaml
- id: "REC-STORY-661-L-001"
  severity: LOW
  provenance: GROUNDED
  title: "Use tempfile + os.replace for crash-safe atomic worklog writes"
  file: "src/claude/scripts/devforgeai_cli/commands/emit_conviction_worklog.py"
  line_range: [421, 431]
  category: correctness
  blocking_release: false
  before_code: |
    with open(worklog_path, "w") as f:
        f.write(json.dumps(record))
  after_code: |
    tmp = worklog_path.with_suffix(".tmp")
    with open(tmp, "w") as f:
        f.write(json.dumps(record))
    os.replace(tmp, worklog_path)
  remediation_steps: null
  verification:
    command: "pytest tests/STORY-661/test_atomic_worklog.py -v"
    expected: "1 passed"
  estimated_effort_minutes: 15
  dependencies: []
  references: []
  cycle_first_seen: 2
```

```yaml
- id: "REC-STORY-661-L-002"
  severity: LOW
  provenance: GROUNDED
  title: "Add target_path resolve+relative_to validation to prevent path escape"
  file: "src/claude/scripts/devforgeai_cli/commands/emit_conviction_worklog.py"
  line_range: [560, 561]
  category: security
  classification: PRE_EXISTING
  blocking_release: false
  before_code: |
    target_path = project_root / user_supplied_path
  after_code: |
    target_path = (project_root / user_supplied_path).resolve()
    target_path.relative_to(project_root.resolve())  # raises if escapes
  remediation_steps: null
  verification:
    command: "pytest tests/STORY-661/test_path_escape_guard.py -v"
    expected: "1 passed"
  estimated_effort_minutes: 10
  dependencies: []
  references:
    - source: "RCA-066"
      url: "https://github.com/bankielewicz/DevForgeAI/blob/main/devforgeai/RCA/RCA-066.md"
  cycle_first_seen: 2
```

## Deferred Recommendations

_None._

## Verification Plan

| REC ID                  | Command                                                                                       | Expected             |
|-------------------------|-----------------------------------------------------------------------------------------------|----------------------|
| REC-STORY-661-M-001     | grep -n 'sys.exit(1)' src/claude/scripts/devforgeai_cli/commands/emit_conviction_worklog.py   | only line 686        |
| REC-STORY-661-M-002     | python3 -c 'subprocess... count("WARNING: file lock unavailable")'                             | 0 or 1               |
| REC-STORY-661-L-001     | pytest tests/STORY-661/test_atomic_worklog.py -v                                              | 1 passed             |
| REC-STORY-661-L-002     | pytest tests/STORY-661/test_path_escape_guard.py -v                                            | 1 passed             |

## Cycle History

```yaml
- cycle: 3
  source: qa-validation
  trigger: "iteration-2 fidelity refresh per skill-creator review feedback"
  started: "2026-05-08T16:00:00Z"
  rec_ids_attempted: ["REC-STORY-661-M-001", "REC-STORY-661-M-002", "REC-STORY-661-L-001", "REC-STORY-661-L-002"]
  rec_ids_closed: []
  rec_ids_deferred: []
  rec_ids_new: ["REC-STORY-661-M-001", "REC-STORY-661-M-002"]
  notes: "Cycle 3: M-001 and M-002 refined with concrete file:line + before/after code blocks per user review of skill-creator iteration-1 outputs. M-002 reclassified PRE_EXISTING (existed since cycle 1 authorship)."
```

## Provenance Summary

| Provenance   | Count |
|--------------|-------|
| GROUNDED     | 4     |
| DERIVED      | 0     |
| INCONCLUSIVE | 0     |
