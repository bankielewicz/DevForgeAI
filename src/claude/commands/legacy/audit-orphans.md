---
description: Scan for orphaned files, duplicate templates, backup artifacts, and sync drift
argument-hint: "[--category=all|backups|duplicates|orphans|drift|agents|context] [--output=console|file] [--baseline=<path>]"
model: opus
allowed-tools: Glob, Grep, Read, Bash(devforgeai-validate:*), Write
---

# /audit-orphans - Orphaned File & Duplicate Detection Audit

Scan the project for orphaned files, duplicate templates, backup artifacts, structural anomalies, agent size violations, and context file version drift. Generates a comprehensive markdown report.

---

## Quick Reference

```bash
# Full audit (all categories, file output)
/audit-orphans

# Specific category only
/audit-orphans --category=backups
/audit-orphans --category=duplicates
/audit-orphans --category=orphans
/audit-orphans --category=drift
/audit-orphans --category=agents
/audit-orphans --category=context

# Console output only (no file written)
/audit-orphans --output=console
```

---

## Command Workflow

### Phase 0: Argument Parsing

```
PARSE arguments:
  --category = $CATEGORY (default: "all")
  --output   = $OUTPUT   (default: "file")
  --baseline = $BASELINE (default: None)   # prior audit-fs JSON output for run-over-run delta (ISSUE-440)

SET report_path = "devforgeai/qa/orphan-audit-{YYYY-MM-DD}.md"
SET findings = {}
SET deltas = {}
SET severity_counts = { CRITICAL: 0, HIGH: 0, MEDIUM: 0, LOW: 0 }
SET BASELINE_ARG = ("--baseline " + $BASELINE) IF $BASELINE ELSE ""
# --baseline pointing at a missing/unparseable file makes the engine exit 2 — HALT and report, do not continue.
```

---

### Phases 1-6: Delegated FS Scans (devforgeai-validate audit-fs engine)

Six sequential `Bash(devforgeai-validate audit-fs)` calls — one per category. Each call writes a params JSON file and invokes the deterministic CLI engine. Phase 7 below consumes the populated `findings[<key>]` dict.

**Phase 1 — Backup File Scan** (`findings["backups"]`):

```
IF category == "all" OR category == "backups":
  Write(file_path="tmp/_framework/audit-fs-phase1.json", content=json.dumps({
    "kind": "glob_scan",
    "patterns": ["**/*.bak","**/*.old","**/*.orig","**/*-backup*","**/*.rec*-backup","**/.backup-*/**",".claude/skills/backup/**"],
    "classifier": {"rules": [
      {"op": "contains_path", "value": "skills/",    "label": "skill_backup"},
      {"op": "contains_path", "value": "scripts/",   "label": "config_backup"},
      {"op": "contains_path", "value": "logs/",      "label": "log_backup"},
      {"op": "contains_path", "value": "deprecated", "label": "deprecated_skill"},
      {"op": "default",                               "label": "general_backup"}
    ]},
    "severity_rules": [{"op": "default", "label": "LOW"}]
  }))
  result = Bash(devforgeai-validate audit-fs --params tmp/_framework/audit-fs-phase1.json ${BASELINE_ARG})
  findings["backups"] = parse_json(result).findings
  deltas["backups"]   = parse_json(result).delta   # present only when --baseline was passed
```

**Phase 2 — Duplicate Template Detection** (`findings["duplicates"]`):

```
IF category == "all" OR category == "duplicates":
  Write(file_path="tmp/_framework/audit-fs-phase2.json", content=json.dumps({
    "kind": "file_metrics",
    "paths_globs": ["**/assets/templates/*.md","devforgeai/specs/**/templates/*.md","src/**/templates/*.md"],
    "metrics": ["chars"],
    "group_by": "basename",
    "severity_rules": [
      {"op": "ne_field", "field": "chars", "value": "group_max_chars", "label": "HIGH"},
      {"op": "default",                                                   "label": "MEDIUM"}
    ]
  }))
  result = Bash(devforgeai-validate audit-fs --params tmp/_framework/audit-fs-phase2.json ${BASELINE_ARG})
  findings["duplicates"] = parse_json(result).findings
  deltas["duplicates"]   = parse_json(result).delta   # present only when --baseline was passed
```

**Phase 3 — Dual-Path Sync Drift** (`findings["drift"]`):

```
IF category == "all" OR category == "drift":
  Write(file_path="tmp/_framework/audit-fs-phase3.json", content=json.dumps({
    "kind": "dual_path_diff",
    "path_a": ".claude/skills",
    "path_b": "src/claude/skills",
    "glob_in": "**/*.md",
    "severity_rules": [{"op": "default", "label": "HIGH"}]
  }))
  result = Bash(devforgeai-validate audit-fs --params tmp/_framework/audit-fs-phase3.json ${BASELINE_ARG})
  findings["drift"] = parse_json(result).findings
  deltas["drift"]   = parse_json(result).delta   # present only when --baseline was passed
```

**Phase 4 — Orphaned Skill Detection** (`findings["orphans"]`):

```
IF category == "all" OR category == "orphans":
  Write(file_path="tmp/_framework/audit-fs-phase4.json", content=json.dumps({
    "kind": "presence_diff",
    "set_a": {"bash_cmd": "ls -d .claude/skills/*/"},
    "set_b": {"glob": ".claude/skills/*/SKILL.md"},
    "classification_rules": [
      {"op": "empty_dir",                              "label": "empty_shell"},
      {"op": "dir_no_skillmd",                         "label": "orphaned_content"},
      {"op": "contains_path", "value": ".deprecated",  "label": "deprecated"}
    ],
    "severity_rules": [{"op": "default", "label": "MEDIUM"}]
  }))
  result = Bash(devforgeai-validate audit-fs --params tmp/_framework/audit-fs-phase4.json ${BASELINE_ARG})
  findings["orphans"] = parse_json(result).findings
  deltas["orphans"]   = parse_json(result).delta   # present only when --baseline was passed
```

**Phase 5 — Agent Size Compliance (ADR-012)** (`findings["agents"]`):

```
IF category == "all" OR category == "agents":
  Write(file_path="tmp/_framework/audit-fs-phase5.json", content=json.dumps({
    "kind": "file_metrics",
    "glob": ".claude/agents/*.md",
    "metrics": ["lines"],
    "derived_fields": {
      "over_by": "($lines - 500)",
      "has_references": "exists('.claude/agents/$basename_no_ext/references/**')"
    },
    "severity_rules": [{"op": "gt", "field": "lines", "value": 500, "label": "HIGH"}]
  }))
  result = Bash(devforgeai-validate audit-fs --params tmp/_framework/audit-fs-phase5.json ${BASELINE_ARG})
  deltas["agents"] = parse_json(result).delta   # present only when --baseline was passed
  # Filter to violations (severity == HIGH) and sort descending by lines
  raw = parse_json(result).findings
  findings["agents"] = sorted([f for f in raw if f.get("severity") == "HIGH"],
                              key=lambda f: f["lines"], reverse=True)
```

**Phase 6 — Context File Drift** (`findings["context"]`):

```
IF category == "all" OR category == "context":
  Write(file_path="tmp/_framework/audit-fs-phase6.json", content=json.dumps({
    "kind": "file_metrics",
    "paths_globs": ["**/source-tree/","**/tech-stack.md","**/dependencies.md","**/coding-standards.md","**/architecture-constraints.md","**/anti-patterns.md"],
    "metrics": ["chars"],
    "canonical_baseline": "devforgeai/specs/context/$basename",
    "derived_fields": {"delta": "($canonical_size - $chars)"},
    "severity_rules": [
      {"op": "ne_field", "field": "chars", "value": "canonical_size", "label": "HIGH"},
      {"op": "default",                                                  "label": "LOW"}
    ]
  }))
  result = Bash(devforgeai-validate audit-fs --params tmp/_framework/audit-fs-phase6.json ${BASELINE_ARG})
  deltas["context"] = parse_json(result).delta   # present only when --baseline was passed
  # Exclude the canonical file itself from copies list
  raw = parse_json(result).findings
  findings["context"] = [f for f in raw
                          if not f["file"].startswith("devforgeai/specs/context/")]
```

---

### Phase 7: Report Generation

```
Assemble findings into structured markdown report:

# DevForgeAI Orphaned File Audit Report
**Generated:** {YYYY-MM-DD}
**Scope:** {category}

## Executive Summary
| Category | Count | Severity | Status |
(one row per category with highest severity)

## Delta Summary
(Include this section ONLY when $BASELINE was provided. One row per scanned
category, counts taken from that category's envelope delta block —
len(deltas[cat].new), len(deltas[cat].resolved), len(deltas[cat].persistent).
Note any findings escalated this run: persistent_runs >= 3 carries
escalated_from with the original severity.)

| Category | New | Resolved | Persistent |
|----------|-----|----------|------------|
(one row per category from deltas[cat])

## Detailed Findings
(Per-category tables with file paths, sizes, recommendations)

## Recommended Next Steps
(Priority-ordered cleanup actions)
For ARCHIVE-verdict findings, follow the quarantine lifecycle defined in `.claude/rules/workflow/archive-lifecycle.md`.

IF output == "file":
  Write report to {report_path}
  Display: "Report written to {report_path}"

Display summary table to console regardless.
```

---

## Error Handling

### No files found for category
```
IF findings[category] is empty:
  Message: "✅ No issues found for category: {category}"
  Continue to next category
```

### File access errors
```
IF Read or wc fails on a specific file:
  Log warning: "⚠️ Could not access: {file}"
  Continue scanning (don't halt for individual file errors)
```

---

## Success Criteria

- [ ] All requested categories scanned
- [ ] File paths verified (absolute, readable)
- [ ] Severity ratings assigned per finding
- [ ] Executive summary generated with counts
- [ ] Report file written (if --output=file)
- [ ] Console summary displayed

---

## Integration

**Invoked by:** Developers, sprint retrospectives, quarterly cleanup audits
**Generates:** `devforgeai/qa/orphan-audit-{YYYY-MM-DD}.md`
**Updates:** None (read-only audit)
**Uses:** All files in `.claude/`, `.claude/`, `devforgeai/specs/context/`

**Related commands:**
- `/audit-budget` - Audits command character budgets
- `/audit-deferrals` - Audits deferred work in stories
- `/audit-hooks` - Audits hook registry

---

## Notes

This command follows the lean orchestration pattern:
- No skill delegation needed (direct utility)
- Read-only (no modifications to project files)
- Generates actionable report with severity ratings
- Can be run incrementally with --category filter
- Designed for quarterly execution or after major refactors

**Recommended cadence:**
- After completing story batches (5+ stories)
- After skill refactors or file migrations
- Quarterly as part of technical debt review
- Before major releases (cleanup gate)
