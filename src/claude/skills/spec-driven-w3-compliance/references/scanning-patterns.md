# W3 Scanning Patterns Reference

This file contains the exact Grep patterns, exclusion rules, and filter logic used during Phase 02 (Scanning). Load this file fresh at the start of Phase 02. Do NOT rely on memory of previous reads.

---

## Grep Patterns

### Pattern 1: Skill Invocation Detection

**Regex:** `Skill\s*\(\s*command\s*=`

**Matches:**
- `Skill(command="spec-driven-dev")`
- `Skill( command = "spec-driven-qa" )`
- `Skill(command="any-skill-name")`

**Does NOT match:**
- `# Skill(command=...)` (commented out — but Grep may still match, manual filtering needed)
- Plain text mentioning "Skill" without parentheses

### Pattern 2: Auto-Invoke Language Detection

**Regex:** `(auto.*invoke|then invoke|invoking.*skill|automatically)`

**Flags:** Case-insensitive (`-i=true`)

**Matches:**
- "auto-invoke", "auto invoke", "automatically invoke"
- "then invoke the skill"
- "invoking another skill"
- "automatically triggers"

---

## Scan Targets

| Scan | Path | Glob | Severity |
|------|------|------|----------|
| CRITICAL | `.claude/agents/` | `*.md` | Subagent Skill() invocation |
| HIGH | `.claude/skills/` | `*.md` | Non-orchestration auto-chaining |
| MEDIUM | `.claude/skills/` | `*.md` | Missing W3 documentation |
| INFO | `.claude/` | `*.md` | Auto-invoke language patterns |

---

## Exclusion Patterns

These patterns are excluded from violation counts. They represent legitimate usage or inactive files.

| Pattern | Applied To | Reason |
|---------|-----------|--------|
| `devforgeai-orchestration/*` | HIGH, MEDIUM scans | Legitimate skill coordinator -- orchestration is explicitly authorized to coordinate skills |
| `*.backup` | ALL scans | Historical backup files, not active code |
| `*.backup-*` | ALL scans | Historical backup files with timestamps |
| `*.original-*` | ALL scans | Original template files before modification |
| `*.md.bak` | ALL scans | Editor backup files |
| `*.archive*` | INFO scan | Archived files no longer in active use |
| `README*` | INFO scan | Documentation files (expected to describe invocation patterns) |
| `CHANGELOG*` | INFO scan | Changelog entries (expected to mention invocations) |

---

## Filter Logic

### HIGH Scan: User Approval Gate Detection

After finding Skill() calls in non-orchestration skill files, each violation must be checked for a user approval gate. A file is NOT a violation if:

1. **AskUserQuestion appears before the Skill() call** — The skill asks for user consent before invoking another skill. Look for `AskUserQuestion` appearing at a line number LOWER than the Skill() call line number in the same file.

2. **Display-only recommendation pattern** — The Skill() call is shown as an example or recommendation, not executed. Look for these markers near the Skill() call:
   - `display-only`
   - `Recommended Next Action`
   - `recommendation`
   - Inside a code block labeled as "example" or "pattern"

### MEDIUM Scan: W3 Documentation Check

A file with Skill() calls is NOT a violation if the file contains EITHER:
- The string `W3` (case-sensitive) — indicating W3 compliance is documented
- The string `display-only` — indicating the invocation pattern is documented as display-only

---

## Grep Command Templates

### CRITICAL Scan
```
Grep(
    pattern='Skill\s*\(\s*command\s*=',
    path='.claude/agents/',
    glob='*.md',
    output_mode='content',
    -n=true
)
```

### HIGH Scan
```
Grep(
    pattern='Skill\s*\(\s*command\s*=',
    path='.claude/skills/',
    glob='*.md',
    output_mode='content',
    -n=true
)
```

### MEDIUM Scan
```
Grep(
    pattern='Skill\s*\(\s*command\s*=',
    path='.claude/skills/',
    glob='*.md',
    output_mode='files_with_matches'
)
```

### INFO Scan
```
Grep(
    pattern='(auto.*invoke|then invoke|invoking.*skill|automatically)',
    path='.claude/',
    glob='*.md',
    -i=true,
    output_mode='content',
    -n=true
)
```
