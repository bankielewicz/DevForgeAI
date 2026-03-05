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

<!-- SECTION: assessing-entrepreneur START -->

### 16. Profile not generated after running /assess-me

**Symptoms:**
- The `/assess-me` command completes all 9 phases but no `user-profile.yaml` file appears at `devforgeai/specs/business/user-profile.yaml`
- Phase 9 (Results Summary) displays recommendations but the profile data is not persisted

**Cause:** The `entrepreneur-assessor` subagent (Phase 8) is responsible for writing the profile file. If the subagent was not invoked, or its Task() prompt did not include the collected responses from Phases 2-7, the profile is never written.

**Solution:**
1. Verify the subagent file exists at `src/claude/agents/entrepreneur-assessor.md`
2. Confirm Phase 8 invokes the subagent with a Task() call that includes all 6 dimension responses
3. Check that the subagent's output targets `devforgeai/specs/business/user-profile.yaml`
4. If the file was generated but is empty or malformed, verify the schema contains required fields:
   ```yaml
   schema_version: "1.0"
   adaptive_profile:
     task_chunk_size: micro | standard | extended
     session_length: short | medium | long
     check_in_frequency: frequent | moderate | minimal
   ```
5. Re-run `/assess-me` if the profile is missing entirely

---

### 17. Assessment reference files not found during Phase 8-9

**Symptoms:**
- Phase 8 (Profile Generation) or Phase 9 (Results Summary) fails with a file-not-found error
- Error references one of the adaptation or calibration reference files

**Cause:** The skill loads 4 reference files on demand from `src/claude/skills/assessing-entrepreneur/references/`. If any file is missing or the path has changed, the phase cannot proceed.

**Required files:**
```
src/claude/skills/assessing-entrepreneur/references/work-style-questionnaire.md
src/claude/skills/assessing-entrepreneur/references/plan-calibration-engine.md
src/claude/skills/assessing-entrepreneur/references/adhd-adaptation-framework.md
src/claude/skills/assessing-entrepreneur/references/confidence-assessment-workflow.md
```

**Solution:**
1. Verify all 4 files exist at the paths above
2. If a file is missing, restore it from source control:
   ```bash
   git checkout main -- src/claude/skills/assessing-entrepreneur/references/
   ```
3. Confirm the skill file references use relative paths matching the actual directory layout

---

### 18. Assessment dimension skipped or missing from profile

**Symptoms:**
- The generated `user-profile.yaml` is missing one or more of the 6 dimensions
- The `entrepreneur-assessor` subagent reports incomplete input

**Cause:** One of Phases 2-7 was skipped, or the user's response to a dimension question was not captured and passed to the subagent in the Phase 8 Task() prompt.

**Solution:**
1. The subagent uses AskUserQuestion to request any missing dimension -- check if this prompt appeared and was answered
2. If the prompt did not appear, verify the Phase 8 Task() prompt includes all 6 dimension responses collected during Phases 2-7
3. Re-run `/assess-me` to complete the missing dimension. The skill does not support partial re-assessment; a full run is required

---

### 19. /assess-me command not found or fails to start

**Symptoms:**
- Running `/assess-me` produces no response or a "command not found" error
- The command appears in listings but does not execute

**Cause:** Either the command file is missing or its YAML frontmatter is malformed.

**Solution:**
1. Verify the command file exists at `src/claude/commands/assess-me.md`
2. Verify the skill file exists at `.claude/skills/assessing-entrepreneur/SKILL.md` (operational) or `src/claude/skills/assessing-entrepreneur/SKILL.md` (source)
3. Open the command file and confirm valid YAML frontmatter with `name: assess-me`
4. If the file is missing, restore from source control or re-run the story that created it (STORY-465)

---

### 20. entrepreneur-assessor subagent not found

**Symptoms:**
- Phase 8 fails with a subagent resolution error
- Error message references `entrepreneur-assessor` not being found

**Cause:** The subagent definition file is missing from the agents directory.

**Solution:**
1. Verify the subagent file exists at `src/claude/agents/entrepreneur-assessor.md`
2. Confirm the operational copy also exists at `.claude/agents/entrepreneur-assessor.md`
3. If missing, restore from source control:
   ```bash
   git checkout main -- src/claude/agents/entrepreneur-assessor.md
   ```
4. Verify the file contains valid YAML frontmatter with `name: entrepreneur-assessor` and a `tools:` field

<!-- SECTION: assessing-entrepreneur END -->

---

<!-- SECTION: coaching-entrepreneur START -->

### 21. Session log not created after coaching session completes

**Symptoms:**
- The coaching session completes normally but no `session-log.yaml` file exists at `devforgeai/specs/business/coaching/session-log.yaml`
- Subsequent sessions open without any tone adaptation

**Cause:** The session log is written at session close. If the coaching skill did not execute its session-close phase — for example, because the session ended abruptly — the file is never created. If the target directory `devforgeai/specs/business/coaching/` does not exist, the write fails silently.

**Solution:**
1. Verify the target directory exists: `devforgeai/specs/business/coaching/`
2. If the directory is missing, create it and re-run the coaching session
3. After a successful session, the file should contain at minimum:
   ```yaml
   sessions:
     - date: "2026-03-04T00:00:00Z"
       emotional_state: neutral
   ```
4. If the file is still not created, restore the coaching skill from source control:
   ```bash
   git checkout main -- src/claude/skills/coaching-entrepreneur/
   ```

---

### 22. Tone adaptation not applied at session start despite existing session log

**Symptoms:**
- `session-log.yaml` exists and contains a prior entry with an emotional state value
- The coaching session opens with neutral, generic tone rather than adapted tone

**Cause:** The coaching skill reads `session-log.yaml` during session initialization. If the file is present but the initialization step does not read it, or the file is malformed (missing `emotional_state` key), adaptation is skipped.

**Solution:**
1. Open `session-log.yaml` and confirm each entry has a valid `emotional_state` value:
   ```yaml
   emotional_state: frustrated   # valid: energized|focused|neutral|tired|frustrated|anxious|overwhelmed
   ```
2. Verify the skill's session-initialization step reads the log and extracts the most recent entry's `emotional_state`
3. If the key is present but adaptation still does not apply, trace the flow from the Read() call through to the opening message

---

### 23. User override of emotional state not persisted in session log

**Symptoms:**
- During a session, the user states a different emotional state
- The coaching skill acknowledges and adapts tone for the remainder of the session
- At session close, `session-log.yaml` still shows the original state

**Cause:** The session-close write step may use the session-open value rather than the current (overridden) value.

**Solution:**
1. Verify the skill tracks the active emotional state in a mutable variable, updating it on override
2. Confirm the session-close write step reads the current (post-override) state
3. After a session with an override, `session-log.yaml` should reflect:
   ```yaml
   - date: "2026-03-04T12:00:00Z"
     emotional_state: tired
     override: "Actually feeling great, let's push hard"
   ```

---

### 24. Emotional state enum validation fails on session-log.yaml load

**Symptoms:**
- Session initialization fails with a validation error referencing `session-log.yaml`
- Error indicates an unrecognized value for `emotional_state`

**Cause:** The `emotional_state` field holds a value outside the defined enum. This occurs if the file was edited manually or a typo was introduced.

**Valid enum values:**
```
energized | focused | neutral | tired | frustrated | anxious | overwhelmed
```

**Solution:**
1. Open `session-log.yaml` and locate the invalid value
2. Replace with the closest valid enum member or the safe default:
   ```yaml
   emotional_state: neutral
   ```
3. If the user declined to provide a state, the log must record `neutral` — verify the decline path writes `neutral` rather than an empty string

<!-- SECTION: coaching-entrepreneur END -->

---

## Getting Help

If none of the above solutions resolve your issue:

1. **Check the RCA archive:** `devforgeai/RCA/` contains root cause analyses for previously encountered issues
2. **Review ADRs:** `devforgeai/specs/adrs/` documents architectural decisions that may affect behavior
3. **Run alignment audit:** The `/audit-alignment` command detects configuration drift between layers
4. **Invoke diagnosis:** Use the root-cause-diagnosis skill at `.claude/skills/root-cause-diagnosis/SKILL.md`
5. **Escalate:** Use AskUserQuestion to surface the issue for manual investigation
