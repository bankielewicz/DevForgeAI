# Phase 08: Git Workflow & Commit

**Entry Gate:**
```bash
devforgeai-validate phase-check ${STORY_ID} --from=07 --to=08

Examples (--project-root applies to phase-* commands only, not check-hooks/invoke-hooks):
 - Correct: devforgeai-validate phase-init ${STORY_ID} --project-root=.
 - Incorrect: python -m devforgeai.cli.devforgeai_validate phase-init ${STORY_ID} --project-root=.
# Exit code 0: Transition allowed
# Exit code 1: Phase 07 not complete - HALT (DoD not validated)
# Exit code 2: DoD validation failed - HALT
```

---

## Progressive Task Disclosure

Read and follow `references/progressive-task-disclosure.md` (substitute PHASE_ID = "08").

---

## Mandatory Steps

**Purpose:** Budget enforcement, handle incomplete items, git commit

**Required Subagents:** None (git operations)

**Pre-Requisite:** DoD format validated in Phase 07

**Steps:**

1.6. **Budget enforcement**
   - Check deferral budget per story
   - HALT if budget exceeded

1.7. **Handle new incomplete items**
   - Any items discovered during Phase 08 need deferral challenge
   - Return to Phase 06 if new deferrals detected

1.8. **Lock acquisition** (parallel story support)
   ```
   # Acquire story lock for commit
   # See references/lock-file-coordination.md
       Read(file_path="references/lock-file-coordination.md")

   ```

2.0. **Stage files for commit**
   ```bash
   git add ${STORY_FILE}
   git add ${IMPL_FILES}
   git add ${TEST_FILES}
   ```

2.1. **Create git commit**
   ```bash
   git commit -m "$(cat <<'EOF'
   feat(${STORY_ID}): ${STORY_TITLE}

   - Implemented ${FEATURE_DESCRIPTION}
   - Tests passing (X/Y)
   - Coverage: ${COVERAGE}%

   Refs: ${STORY_ID}
   EOF
   )"
   ```

2.2. **Verify commit success**
   ```bash
   git log -1 --format="%H %s"
   # Should show new commit
   ```

2.3. **Release lock**
   ```
   # Release story lock after commit
   ```

2.4. **Update story status**
   - Story file status should already be "Dev Complete" from Phase 07

2.5. **Update AC Checklist (deployment items)**
   ```
   Edit(
     file_path="${STORY_FILE}",
     old_string="- [ ] Git commit",
     new_string="- [x] Git commit"
   )
   ```

**Reference:** `references/git-workflow-conventions.md` for complete workflow
    Read(file_path="references/git-workflow-conventions.md")

### Git Commit Message Format

```
feat(STORY-XXX): Brief description

- Key implementation detail 1
- Key implementation detail 2
- Test results summary

Refs: STORY-XXX
```

**Commit Types:**
- `feat` - New feature
- `fix` - Bug fix
- `refactor` - Code refactoring
- `test` - Test changes
- `docs` - Documentation

---

## Validation Checkpoint

**Before proceeding to Phase 09, verify:**

- [ ] Git commit succeeded (commit hash exists)
- [ ] Story file included in commit
- [ ] AC Checklist (deployment items) updated ([ ] → [x])

**IF any checkbox UNCHECKED:** HALT workflow

### AC Checklist Update Verification (RCA-003)

After Step 2.5 completes, verify AC Checklist was actually updated:
```
Grep(pattern="- \\[x\\].*[Gg]it", path="${STORY_FILE}")
# Should find checked git/deployment-related items
# If no matches found: AC Checklist update was skipped - HALT
```

---

## Pre-Exit Checklist

**Before calling `phase-complete`, verify ALL items:**

- [ ] Budget enforcement checked (deferral budget per story)
- [ ] Files staged for commit (story file, impl files, test files)
- [ ] Git commit succeeded (commit hash exists)
- [ ] Story file included in commit
- [ ] AC checklist updated (deployment items)
- [ ] Observation capture executed

**IF any item UNCHECKED and no N/A justification:** HALT — do not call exit gate.

---

## Optional Captures

### Observation Capture (EPIC-051)

Before exiting this phase, capture observations from git operations:

1. **Collect Explicit Observations:**
   IF git-validator was invoked and returned `observations[]` in output:
   - Extract each observation object
   - Set source: "explicit"

   Capture git operation results as observations:
   - IF commit succeeded (exit code 0):
     - Set category: "success"
     - Set note: "Git commit completed successfully"
     - Set severity: "low"
   - IF commit failed or encountered issues:
     - Set category: "friction"
     - Set note: "Git operation encountered issues: {error_details}"
     - Set severity: "medium"
   - Set source: "self-captured"

2. **Invoke Observation Extractor (if git-validator was used):**
   ```
   Task(subagent_type="observation-extractor",
        description="Extract observations from Phase 08 git operations",
        prompt="Extract implicit observations from git-validator output including repository issues, commit patterns, and workflow friction.")
   ```
   - Set source: "extracted" for returned observations

3. **Append to Phase State:**
   FOR each observation (explicit OR self-captured OR extracted):
   - Generate ID: "OBS-08-{timestamp}" (ISO8601 milliseconds)
   - Set fields: id, phase ("08"), category, note, severity, files[], source, timestamp
   - Append to phase-state.json observations[] array
   - Ensure no duplicate observations (skip if same finding in explicit and extracted)

**Error Handling:** If observation capture fails, log warning and continue phase completion (non-blocking per BR-001).

### Session Memory Update (STORY-341)

Before exiting this phase, append observations to the session memory file:

```
# Append Phase 08 observations to session memory
session_path = ".claude/memory/sessions/${STORY_ID}-session.md"

Edit(
  file_path=session_path,
  old_string="## Observations",
  new_string="## Observations\n\n### Phase 08 (Git Workflow)\n${OBSERVATIONS_LIST}"
)

# Update last_updated timestamp
Edit(
  file_path=session_path,
  old_string="last_updated: ${OLD_TIMESTAMP}",
  new_string="last_updated: ${CURRENT_TIMESTAMP}"
)
```

**Reference:** EPIC-052 Session Memory Layer specification

---

## Exit Gate
```bash
devforgeai-validate phase-complete ${STORY_ID} --phase=08 --checkpoint-passed
# Exit code 0: Phase complete, proceed to Phase 09
# Exit code 1: Cannot complete - commit failed
```
