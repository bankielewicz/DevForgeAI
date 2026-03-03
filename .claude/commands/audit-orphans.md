---
description: Scan for orphaned files, duplicate templates, backup artifacts, and sync drift
argument-hint: "[--category=all|backups|duplicates|orphans|drift|agents|context] [--output=console|file]"
model: opus
allowed-tools: Glob, Grep, Read, Bash(wc:*), Bash(ls:*), Bash(du:*), Write
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

SET report_path = "devforgeai/qa/orphan-audit-{YYYY-MM-DD}.md"
SET findings = {}
SET severity_counts = { CRITICAL: 0, HIGH: 0, MEDIUM: 0, LOW: 0 }
```

---

### Phase 1: Backup File Scan

**Detect explicit backup/legacy files with telltale suffixes.**

```
IF category == "all" OR category == "backups":

  backup_patterns = [
    "**/*.bak",
    "**/*.old",
    "**/*.orig",
    "**/*-backup*",
    "**/*.rec*-backup",
    "**/.backup-*/**"
  ]

  FOR pattern IN backup_patterns:
    results = Glob(pattern)
    FOR file IN results:
      Classify file:
        IF path contains "skills/" → type = "skill_backup"
        IF path contains "scripts/" → type = "config_backup"
        IF path contains "logs/" → type = "log_backup"
        IF path contains "deprecated" → type = "deprecated_skill"
        ELSE → type = "general_backup"

  Also scan for deprecated skill directories:
    Glob(".claude/skills/backup/**")

  Severity: LOW (backups are safe to delete)
  Add to findings["backups"]
```

---

### Phase 2: Duplicate Template Detection

**Find templates that exist in multiple skill directories (version drift risk).**

```
IF category == "all" OR category == "duplicates":

  template_files = Glob("**/assets/templates/*.md")
  template_files += Glob("**/templates/*.md", path="devforgeai/specs/")
  template_files += Glob("**/templates/*.md", path="src/")

  Group by basename(file):
    FOR each group with count > 1:
      Compare file sizes using Bash("wc -c {file}")
      IF sizes differ → severity = HIGH (version drift!)
      IF sizes match → severity = MEDIUM (redundant copy)

  Template names to specifically check:
    - story-template.md (canonical: .claude/skills/devforgeai-story-creation/assets/templates/)
    - epic-template.md (canonical: .claude/skills/designing-systems/assets/templates/)
    - sprint-template.md (canonical: .claude/skills/devforgeai-orchestration/assets/templates/)
    - rca-document-template.md
    - brainstorm-template.md
    - requirements-template.md

  Severity: HIGH if size mismatch, MEDIUM if exact duplicate
  Add to findings["duplicates"]
```

---

### Phase 3: Dual-Path Sync Drift

**Detect files that exist in `.claude/` but not `.claude/` (or vice versa), and size mismatches.**

```
IF category == "all" OR category == "drift":

  claude_files = Glob(".claude/skills/**/*.md")
  src_files = Glob(".claude/skills/**/*.md")

  Normalize paths:
    claude_set = { path.removeprefix(".claude/") for path in claude_files }
    src_set = { path.removeprefix(".claude/") for path in src_files }

  only_in_claude = claude_set - src_set
  only_in_src = src_set - claude_set
  in_both = claude_set & src_set

  FOR file IN in_both:
    claude_size = Bash("wc -c .claude/{file}")
    src_size = Bash("wc -c .claude/{file}")
    IF sizes differ:
      Add to drift_mismatches with delta

  Report:
    - Count of files only in .claude/
    - Count of files only in src/
    - Files with size mismatch (detail each)

  Severity: HIGH (sync gap can cause stale enforcement)
  Add to findings["drift"]
```

---

### Phase 4: Orphaned Skill Detection

**Find skill directories without SKILL.md (invisible to Claude Code Terminal).**

```
IF category == "all" OR category == "orphans":

  all_skill_dirs = Bash("ls -d .claude/skills/*/")
  skill_md_files = Glob(".claude/skills/*/SKILL.md")

  Extract directory names from each:
    dirs_with_skillmd = { dirname(f) for f in skill_md_files }
    all_dirs = { d.rstrip("/") for d in all_skill_dirs }

  orphaned = all_dirs - dirs_with_skillmd

  FOR dir IN orphaned:
    List files in dir to determine:
      IF empty → "empty_shell"
      IF has files but no SKILL.md → "orphaned_content"
      IF named *.deprecated → "deprecated"

  Also check for nested directory anomalies:
    Glob("**/assets/assets/**")
    Glob("**/templates/templates/**")
    Glob("**/references/references/**")

  Severity: MEDIUM (dead weight, causes confusion)
  Add to findings["orphans"]
```

---

### Phase 5: Agent Size Compliance (ADR-012)

**Flag agents exceeding the 500-line limit.**

```
IF category == "all" OR category == "agents":

  agent_files = Glob(".claude/agents/*.md")

  FOR file IN agent_files:
    line_count = Bash("wc -l {file}")
    IF line_count > 500:
      over_by = line_count - 500
      has_refs = exists(Glob(".claude/agents/references/{basename_no_ext}/**"))
      Add to violations: { file, lines, over_by, has_references }

  Sort by line_count descending

  Severity: HIGH (violates ADR-012 progressive disclosure)
  Add to findings["agents"]
```

---

### Phase 6: Context File Drift

**Detect constitutional files that have been copied and drifted out of sync.**

```
IF category == "all" OR category == "context":

  context_files = [
    "source-tree.md",
    "tech-stack.md",
    "dependencies.md",
    "coding-standards.md",
    "architecture-constraints.md",
    "anti-patterns.md"
  ]

  FOR filename IN context_files:
    canonical = "devforgeai/specs/context/{filename}"
    canonical_size = Bash("wc -c {canonical}")

    copies = Glob("**/{filename}")
    Remove canonical from copies list

    FOR copy IN copies:
      copy_size = Bash("wc -c {copy}")
      IF copy_size != canonical_size:
        delta = canonical_size - copy_size
        severity = HIGH
      ELSE:
        severity = LOW (synced copy, just redundant)

  Add to findings["context"]
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

## Detailed Findings
(Per-category tables with file paths, sizes, recommendations)

## Recommended Next Steps
(Priority-ordered cleanup actions)

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

### Glob returns too many results
```
IF any Glob returns > 1000 files:
  Truncate to first 100 with note: "Showing 100 of {N} results. Use --category filter."
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
