# RCA-026: Phase CLI Module Path Incorrect

**Date:** 2026-01-22
**Reporter:** User
**Component:** devforgeai-development skill (Phase State Initialization)
**Severity:** HIGH
**Status:** RESOLVED (STORY-308)

---

## Issue Description

When executing `/dev STORY-295`, Claude used incorrect Python command `python -m devforgeai_cli.main phase-init` instead of the correct command `devforgeai-validate phase-init`. The CLI failed with:

```
/usr/bin/python3: No module named devforgeai_cli.main
Exit code: 1
```

**Expected Behavior:** CLI invoked via `devforgeai-validate phase-init STORY-XXX --project-root=.`
**Actual Behavior:** CLI invoked via `python3 -m devforgeai_cli.main phase-init` (incorrect)
**Impact:** Phase state initialization failed, blocking TDD workflow

---

## 5 Whys Analysis

**Issue Statement:** Claude used incorrect Python module invocation instead of installed CLI binary

### Why #1
**Q:** Why did Claude use `python -m devforgeai_cli.main` instead of `devforgeai-validate`?
**A:** Claude didn't read the phase file documentation before executing. The phase file clearly shows both correct AND incorrect invocation patterns (lines 8-9 of phase-01-preflight.md), but Claude invented its own command pattern.

### Why #2
**Q:** Why didn't Claude read the phase file documentation before executing?
**A:** The SKILL.md Phase State Initialization section shows the command but Claude skipped loading the phase file that contains the actual command syntax.

### Why #3
**Q:** Why did Claude assume Python module invocation (`python -m`) pattern?
**A:** Claude confused the CLI entry point registration (`devforgeai-validate=devforgeai_cli.cli:main` in setup.py) with how to invoke it. The CLI is registered as `devforgeai-validate` binary via pip install, not as a Python module to run directly.

### Why #4
**Q:** Why is there confusion about how to invoke the CLI?
**A:** The 01.0.5-cli-check.md reference file shows `devforgeai` (without `-validate`) as the command, but setup.py registers `devforgeai-validate`. There's inconsistency in documentation.

### Why #5 (ROOT CAUSE)
**Q:** Why is the CLI not installed and why is there command name confusion?
**A:** **ROOT CAUSE:** The skill documentation doesn't enforce reading the preflight reference file `01.0.5-cli-check.md` which would verify CLI availability BEFORE attempting to use it. Additionally, there's a naming inconsistency between documentation (`devforgeai`) and actual registration (`devforgeai-validate`). The CLI also isn't installed in the current environment.

---

## Evidence Collected

### File: `.claude/skills/devforgeai-development/phases/phase-01-preflight.md`
- **Lines Examined:** 5-13
- **Finding:** Contains correct vs incorrect invocation patterns that Claude ignored
- **Excerpt:**
```markdown
devforgeai-validate phase-init ${STORY_ID} --project-root=.

Examples (--project-root applies to phase-* commands only):
 - Correct: devforgeai-validate phase-init ${STORY_ID} --project-root=.
 - Incorrect: python -m devforgeai.cli.devforgeai_validate phase-init ${STORY_ID} --project-root=.
```
- **Significance:** CRITICAL - Documentation explicitly warns against the exact pattern Claude used

### File: `.claude/scripts/setup.py`
- **Lines Examined:** 36-42
- **Finding:** CLI registered as `devforgeai-validate` entry point
- **Excerpt:**
```python
entry_points={
    'console_scripts': [
        'devforgeai-validate=devforgeai_cli.cli:main',
    ],
},
```
- **Significance:** CRITICAL - Shows the correct binary name that should be used

### File: `.claude/skills/devforgeai-development/SKILL.md`
- **Lines Examined:** 436, 464-467
- **Finding:** Shows correct command but backward compatibility warning not processed first
- **Excerpt:**
```markdown
devforgeai-validate phase-init ${STORY_ID} --project-root=.
...
IF devforgeai-validate command not found (exit code 127):
    Display: "⚠️  Warning: Phase enforcement CLI not installed"
```
- **Significance:** HIGH - Skill shows right command but Claude invented its own invocation

### File: `.claude/skills/devforgeai-development/references/preflight/01.0.5-cli-check.md`
- **Lines Examined:** 12-21
- **Finding:** CLI check step uses `devforgeai` (not `devforgeai-validate`) - naming inconsistency
- **Excerpt:**
```bash
if ! command -v devforgeai &> /dev/null; then
    CLI_AVAILABLE=false
```
- **Significance:** HIGH - Documentation uses wrong binary name

### File: `.claude/scripts/devforgeai_cli/cli.py`
- **Lines Examined:** 30-31
- **Finding:** CLI program name is `devforgeai`, not `devforgeai-validate`
- **Excerpt:**
```python
parser = argparse.ArgumentParser(
    prog='devforgeai',
```
- **Significance:** MEDIUM - Internal prog name differs from entry point name

### Context Files Status
| File | Status |
|------|--------|
| tech-stack.md | EXISTS |
| source-tree.md | EXISTS |
| dependencies.md | EXISTS |
| coding-standards.md | EXISTS |
| architecture-constraints.md | EXISTS |
| anti-patterns.md | EXISTS |

---

## Recommendations

### REC-1: Fix CLI Check Reference File - Correct Binary Name (HIGH)

**Problem Addressed:** The 01.0.5-cli-check.md file checks for `devforgeai` but the actual binary is `devforgeai-validate`

**Proposed Solution:** Update the CLI check to use correct binary name

**Implementation Details:**
- **File:** `.claude/skills/devforgeai-development/references/preflight/01.0.5-cli-check.md`
- **Section:** Lines 12-21
- **Change Type:** Modify

**Old Text:**
```bash
if ! command -v devforgeai &> /dev/null; then
    CLI_AVAILABLE=false
    echo "WARN: devforgeai CLI not installed"
    echo "  - Hook checks will be skipped"
    echo "  - Manual validation required"
else
    CLI_AVAILABLE=true
    DEVFORGEAI_VERSION=$(devforgeai --version 2>/dev/null || echo "unknown")
    echo "✓ devforgeai CLI: $DEVFORGEAI_VERSION"
fi
```

**New Text:**
```bash
if ! command -v devforgeai-validate &> /dev/null; then
    CLI_AVAILABLE=false
    echo "WARN: devforgeai-validate CLI not installed"
    echo "  - Run: pip install -e .claude/scripts/"
    echo "  - Hook checks will be skipped"
    echo "  - Manual validation required"
else
    CLI_AVAILABLE=true
    DEVFORGEAI_VERSION=$(devforgeai-validate --version 2>/dev/null || echo "unknown")
    echo "✓ devforgeai-validate CLI: $DEVFORGEAI_VERSION"
fi
```

**Rationale:** The binary name registered in setup.py is `devforgeai-validate`, not `devforgeai`. This inconsistency causes the CLI check to always fail even when the CLI is installed.

**Testing:**
1. Install CLI: `pip install -e .claude/scripts/`
2. Verify: `command -v devforgeai-validate` returns path
3. Run: `devforgeai-validate --version` shows version

**Effort Estimate:** Low (15 min)
**Impact:** High - enables proper CLI detection

---

### REC-2: Add Mandatory Phase File Read Before CLI Invocation (HIGH)

**Problem Addressed:** Claude skipped reading the phase file that contains correct invocation syntax

**Proposed Solution:** Add explicit Read() instruction in SKILL.md Phase State Initialization

**Implementation Details:**
- **File:** `.claude/skills/devforgeai-development/SKILL.md`
- **Section:** Phase State Initialization, before line 436
- **Change Type:** Add

**Code to Add (before line 436):**
```markdown
**MANDATORY: Read Phase 01 file BEFORE executing CLI command:**
```
Read(file_path=".claude/skills/devforgeai-development/phases/phase-01-preflight.md")
```

**Then execute the Entry Gate command from that file (lines 5-13).**
```

**Rationale:** Forces Claude to load the phase file which contains the correct vs incorrect invocation examples, preventing improvisation.

**Testing:**
1. Invoke `/dev STORY-XXX`
2. Verify phase-01-preflight.md is Read() before any CLI command
3. Verify correct `devforgeai-validate` command is used

**Effort Estimate:** Low (15 min)
**Impact:** High - prevents incorrect command invention

---

### REC-3: Update cli.py prog Name to Match Entry Point (MEDIUM)

**Problem Addressed:** Internal argparse prog name (`devforgeai`) differs from entry point (`devforgeai-validate`)

**Proposed Solution:** Align prog name with entry point

**Implementation Details:**
- **File:** `.claude/scripts/devforgeai_cli/cli.py`
- **Section:** Lines 30-31
- **Change Type:** Modify

**Old Text:**
```python
parser = argparse.ArgumentParser(
    prog='devforgeai',
```

**New Text:**
```python
parser = argparse.ArgumentParser(
    prog='devforgeai-validate',
```

**Rationale:** Consistency between entry point and help output. When user runs `devforgeai-validate --help`, it should say `devforgeai-validate` not `devforgeai`.

**Testing:**
1. Run: `devforgeai-validate --help`
2. Verify: First line shows `usage: devforgeai-validate`

**Effort Estimate:** Low (10 min)
**Impact:** Medium - improves consistency

---

### REC-4: Install CLI as Part of DevForgeAI Setup (MEDIUM)

**Problem Addressed:** CLI not installed in current environment

**Proposed Solution:** Document CLI installation requirement

**Implementation Details:**
- **File:** `CLAUDE.md` or `README.md`
- **Section:** Setup/Installation
- **Change Type:** Add

**Text to Add:**
```markdown
## CLI Installation (Required for Phase Enforcement)

The DevForgeAI workflow requires the validation CLI to be installed:

```bash
pip install -e .claude/scripts/
```

Verify installation:
```bash
devforgeai-validate --version
```
```

**Rationale:** Without CLI installed, phase enforcement cannot work. This should be a documented prerequisite.

**Testing:**
1. Run: `pip install -e .claude/scripts/`
2. Verify: `devforgeai-validate --version` outputs version

**Effort Estimate:** Low (15 min)
**Impact:** Medium - ensures environment is properly configured

---

## Implementation Checklist

- [x] Implement REC-1: Fix CLI check reference file binary name - **STORY-308** (2026-01-26)
- [ ] Implement REC-2: Add mandatory phase file read instruction - deferred to future story
- [x] Implement REC-3: Update cli.py prog name - **STORY-308** (2026-01-26)
- [ ] Implement REC-4: Document CLI installation requirement - STORY-309
- [x] Install CLI: `pip install -e .claude/scripts/`
- [x] Verify all changes work: run `/dev STORY-XXX`
- [x] Mark RCA as RESOLVED after verification - (2026-01-26)

---

## Prevention Strategy

### Short-term
- Fix binary name inconsistency (REC-1, REC-3)
- Add explicit Read() requirement before CLI invocation (REC-2)

### Long-term
- Consider auto-installing CLI when DevForgeAI is set up
- Add CLI availability check to all skill entry points
- Create integration tests that verify CLI invocation works

### Monitoring
- Watch for "No module named" errors in `/dev` workflow
- Audit phase files for correct/incorrect invocation examples
- Verify CLI is installed in development environments

---

## Related RCAs

- **RCA-001:** Phase State Module Missing From CLI (similar CLI invocation issues - module import error)

---

**RCA Created:** 2026-01-22
**Last Updated:** 2026-01-26
**Resolved By:** STORY-308 (Fix Binary Name Mismatch in Python CLI)
