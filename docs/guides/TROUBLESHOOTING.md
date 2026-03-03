# DevForgeAI Troubleshooting Guide

**Last Updated:** 2026-03-03
**Applies To:** DevForgeAI Framework v4.x

---

## Table of Contents

- [Quick Fixes](#quick-fixes)
- [Development Issues](#development-issues)
- [QA Issues](#qa-issues)
- [Git Issues](#git-issues)
- [WSL Issues](#wsl-issues)
- [Hook Issues](#hook-issues)

---

## Quick Fixes

| Symptom | Cause | Fix |
|---------|-------|-----|
| `COMMIT BLOCKED` | DoD items under `###` subsection | Move items directly under `## Implementation Notes` |
| `ModuleNotFoundError` | PYTHONPATH not set | `export PYTHONPATH=".:$PYTHONPATH"` |
| `Permission denied: script.sh` | WSL file permissions | `chmod +x script.sh` or `bash script.sh` |
| `$'\r': command not found` | CRLF line endings | `dos2unix script.sh` |
| `Context files missing` | Setup not run | Run `/create-context` before `/dev` or `/qa` |
| `Phase skipping error` | Attempted to skip a phase | Execute all phases in order; no exceptions |
| `Technology not in tech-stack.md` | HALT trigger fired | Create an ADR before introducing the technology |
| `Coverage below threshold` | Tests insufficient | Coverage gaps are CRITICAL blockers (ADR-010) |
| `3+ fix attempts failed` | Shotgun debugging | Invoke root-cause-diagnosis skill before attempt 4 |

---

## Development Issues

### 1. Context Files Missing

**Symptoms:**
- Skill invocation fails with references to missing context files
- `/dev` or `/qa` commands fail at Phase 01 pre-flight

**Cause:** The six immutable context files in `devforgeai/specs/context/` have not been generated for the project.

**Required files:**
1. `tech-stack.md`
2. `source-tree.md`
3. `dependencies.md`
4. `coding-standards.md`
5. `architecture-constraints.md`
6. `anti-patterns.md`

**Solution:**
Run the `/create-context` command before starting any development or QA workflow. This generates all six context files from the project's architecture specification.

---

### 2. Phase Skipping Errors

**Symptoms:**
- Phase validation fails because a previous phase was not completed
- Pre-flight checks at the start of a phase report missing artifacts from prior phases

**Cause:** All phases in the implementing-stories workflow are mandatory. The framework enforces sequential execution of every phase.

**Solution:**
Execute every phase in documented order. The following rationalizations are explicitly forbidden:
- "This phase is simple enough to skip"
- "I already know the answer, no need to verify"
- "Skipping this saves tokens/time"

Only the user can authorize phase skipping via explicit instruction.

(Source: `.claude/rules/workflow/tdd-workflow.md` and CLAUDE.md `no_token_optimization_of_phases` section)

---

### 3. Technology Not in tech-stack.md

**Symptoms:**
- HALT trigger fires when a technology, library, or tool is referenced that does not appear in `devforgeai/specs/context/tech-stack.md`

**Cause:** Context files are immutable. Any technology not listed in `tech-stack.md` cannot be used without an Architecture Decision Record.

**Solution:**
1. HALT immediately
2. Use AskUserQuestion to get user approval for the new technology
3. Create an ADR in `devforgeai/specs/adrs/` documenting the decision
4. Update `tech-stack.md` through the `/create-context` workflow (not direct edit)
5. Resume development

(Source: `.claude/rules/core/critical-rules.md`, Rule 1 and Rule 7)

---

### 4. Module Not Found (Python CLI)

**Symptoms:**
```
ModuleNotFoundError: No module named 'devforgeai_cli'
```

**Cause:** The Python CLI package is not installed or `PYTHONPATH` does not include the project root.

**Solution:**

Option A -- Install the CLI in development mode:
```bash
pip install -e .claude/scripts/
devforgeai-validate --help
```

Option B -- Set PYTHONPATH:
```bash
export PYTHONPATH=".:$PYTHONPATH"
```

---

### 5. 3+ Consecutive Fix Attempts Failing

**Symptoms:**
- The same test or error persists after three or more fix attempts
- Different code changes keep producing the same failure

**Cause:** Iterative fixes without root cause analysis (shotgun debugging).

**Solution:**
After the third failed attempt, you MUST invoke the root-cause-diagnosis skill before making any further changes:

```
Skill: .claude/skills/root-cause-diagnosis/SKILL.md
```

The skill enforces a 4-phase methodology:
1. **CAPTURE** -- Collect failure artifacts (error messages, stack traces, test output)
2. **INVESTIGATE** -- Cross-reference against context files using the diagnostic-analyst subagent
3. **HYPOTHESIZE** -- Generate ranked hypotheses with confidence scores
4. **PRESCRIBE** -- Recommend targeted fixes with specific file paths

If the prescribed fix also fails, try the next hypothesis. After 5 total attempts, escalate to the user via AskUserQuestion.

(Source: `.claude/rules/workflow/diagnosis-before-fix.md`)

---

## QA Issues

### 6. Coverage Below Thresholds

**Symptoms:**
- QA validation returns FAILED
- Coverage report shows percentages below required minimums

**Cause:** Test coverage does not meet the mandatory thresholds defined in ADR-010.

**Thresholds (CRITICAL blockers, not warnings):**

| Layer | Minimum Coverage |
|-------|-----------------|
| Business Logic | 95% |
| Application | 85% |
| Infrastructure | 80% |

**Solution:**
Coverage gaps cannot be deferred. If coverage is below threshold, the QA result MUST be FAILED. You must:

1. Identify uncovered code paths using coverage reports
2. Write additional tests to cover the gaps
3. Re-run the test suite to verify thresholds are met
4. Only then proceed through the QA gate

There is no "PASS WITH WARNINGS" path for coverage gaps.

(Source: `.claude/rules/workflow/qa-validation.md`, Coverage Threshold Enforcement section)

---

## Git Issues

### 7. Commit Blocked by Pre-Commit Hook (DoD Validation)

**Symptoms:**
```
VALIDATION FAILED
DoD item marked [x] but missing from Implementation Notes
COMMIT BLOCKED
```

**Cause:** The `devforgeai-validate validate-dod` pre-commit hook checks that all Definition of Done items marked `[x]` also appear in the `## Implementation Notes` section. The most common failure is placing DoD items under a `###` subsection header instead of directly under `## Implementation Notes`.

The validator's `extract_section()` function stops at the first `###` header. Any items below a `###` header are invisible to the validator.

**Wrong format (validator FAILS):**
```markdown
## Implementation Notes

**Developer:** DevForgeAI AI Agent

### Definition of Done Status
- [x] Item 1 - Completed: description
- [x] Item 2 - Completed: description
```

The parser stops at `### Definition of Done Status` and never sees the items below it.

**Correct format (validator PASSES):**
```markdown
## Implementation Notes

**Developer:** DevForgeAI AI Agent
**Implemented:** 2026-03-03

- [x] Item 1 - Completed: description
- [x] Item 2 - Completed: description

### TDD Workflow Summary
...
```

Items must be a flat list directly under `## Implementation Notes`, after developer metadata and before any `###` subsections.

**Recovery steps:**
1. Read the fix guide: `.claude/skills/implementing-stories/references/dod-update-workflow.md`
2. Read the failing story file (path shown in validator output)
3. Move DoD items above any `###` headers
4. Ensure item text matches exactly between the DoD section and Implementation Notes (including backticks and special characters)
5. Validate before retrying:
   ```bash
   devforgeai-validate validate-dod <STORY_FILE>
   ```
6. Only commit after exit code 0

**Never use `git commit --no-verify` to bypass validation.**

(Source: `.claude/rules/workflow/commit-failure-recovery.md` and `.claude/skills/implementing-stories/references/dod-update-workflow.md`)

---

### 8. Autonomous Deferral Detected

**Symptoms:**
```
AUTONOMOUS DEFERRAL DETECTED
COMMIT BLOCKED
```

**Cause:** A DoD item was marked `[x]` in the Definition of Done section but shows `[ ]` in Implementation Notes without user approval. The framework prohibits autonomous deferrals.

**Solution:**
1. Identify the mismatched item
2. Either complete the implementation or get explicit user approval to defer
3. If deferring with approval, document the justification in the story file
4. Re-validate with `devforgeai-validate validate-dod`

---

## WSL Issues

### 9. Permission Denied on Shell Scripts

**Symptoms:**
```
bash: ./script.sh: Permission denied
```

**Cause:** WSL file permission handling differs from native Linux. Scripts cloned from Git on Windows may lack execute permission.

**Solution:**

Option A -- Add execute permission:
```bash
chmod +x script.sh
```

Option B -- Run with explicit bash invocation:
```bash
bash script.sh
```

---

### 10. Line Ending Errors (`$'\r'`)

**Symptoms:**
```
/bin/bash^M: bad interpreter: No such file or directory
```
or
```
$'\r': command not found
```

**Cause:** Shell scripts have Windows-style CRLF line endings (`\r\n`) instead of Unix-style LF (`\n`). This happens when files are created or edited on Windows and run in WSL.

**Solution:**

Convert the file:
```bash
dos2unix script.sh
```

If `dos2unix` is not installed:
```bash
sudo apt install dos2unix
```

Alternatively, use sed:
```bash
sed -i 's/\r$//' script.sh
```

**Prevention:** Configure Git to handle line endings:
```bash
git config --global core.autocrlf input
```

This converts CRLF to LF on commit while leaving the working directory as-is.

---

### 11. Tests Failing Against Operational Folders

**Symptoms:**
- Corrupt or missing file errors when running tests
- Intermittent test failures that cannot be reproduced

**Cause:** WSL has historically generated corrupt or missing file errors when tests run against operational folders (`.claude/`, `devforgeai/`).

**Solution:**
Always run tests against the `src/` tree, not operational folders:

```bash
# Correct
pytest src/tests/

# Wrong -- may produce WSL file errors
pytest .claude/scripts/tests/
```

(Source: CLAUDE.md, "test against src/ tree not operational folders")

---

### 12. Temporary Files in /tmp/ Not Found

**Symptoms:**
- Files written to `/tmp/` are not accessible from other tools or sessions
- Cross-platform path resolution failures

**Cause:** The `/tmp/` directory is not reliably shared between WSL, Windows, and Linux environments.

**Solution:**
Use project-scoped temporary files instead:

```bash
# Wrong
/tmp/STORY-505/output.txt

# Correct
{project-root}/tmp/STORY-505/output.txt
```

(Source: `.claude/rules/workflow/operational-safety.md`, Rule 2)

---

## Hook Issues

### 13. SubagentStop Hook Failures

**Symptoms:**
- Hook validation fails silently
- Phase transitions blocked without clear error message

**Cause:** Hook scripts may return non-zero exit codes or write errors to stderr that are not surfaced clearly.

**Diagnostic steps:**
1. Check the hook script's exit code:
   ```bash
   devforgeai-validate check-hooks
   echo $?
   ```
2. Review stderr output -- hook errors are logged there, not stdout
3. Verify the hook script exists and is executable
4. Check that required environment variables are set

---

### 14. TaskCompleted Hook Validation Gate

**Symptoms:**
- Task completion is not recognized by the framework
- Phase state does not advance after task completion

**Cause:** The TaskCompleted hook performs step validation. If the validation gate fails, the phase state is not updated.

**Diagnostic steps:**
1. Check phase state:
   ```bash
   python -m devforgeai_cli.commands.phase_commands phase-status STORY-XXX --project-root=.
   ```
2. Review the phase state JSON file:
   ```
   devforgeai/workflows/STORY-XXX-qa-phase-state.json
   ```
3. Look for validation errors in the hook output
4. Verify all acceptance criteria for the current phase are met before the hook fires

---

### 15. Pre-Commit Hook Modification Attempts

**Symptoms:**
- HALT trigger fires when attempting to modify `.git/hooks/`

**Cause:** Modifying Git hooks is a forbidden operation in DevForgeAI. This is a safety measure to preserve commit validation integrity.

**Solution:**
Never modify `.git/hooks/` directly. If the pre-commit hook has a bug or incorrect behavior:
1. Report the issue
2. Fix the validation logic in the source (not the hook)
3. Rebuild the hook through the proper workflow

(Source: CLAUDE.md, HALT Triggers section)

---

## Getting Help

If none of the above solutions resolve your issue:

1. **Check the RCA archive:** `devforgeai/RCA/` contains root cause analyses for previously encountered issues
2. **Review ADRs:** `devforgeai/specs/adrs/` documents architectural decisions that may affect behavior
3. **Run alignment audit:** The `/audit-alignment` command detects configuration drift between layers
4. **Invoke diagnosis:** Use the root-cause-diagnosis skill at `.claude/skills/root-cause-diagnosis/SKILL.md`
5. **Escalate:** Use AskUserQuestion to surface the issue for manual investigation
