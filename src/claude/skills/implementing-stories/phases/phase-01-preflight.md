# Phase 01: Pre-Flight Validation

**Entry Gate:**
```bash
devforgeai-validate phase-init ${STORY_ID} --project-root=.

Examples (--project-root applies to phase-* commands only, not check-hooks/invoke-hooks):
 - Correct: devforgeai-validate phase-init ${STORY_ID} --project-root=.
 - Incorrect: python -m devforgeai.cli.devforgeai_validate phase-init ${STORY_ID} --project-root=.
# Exit code 0: State file created, proceed
# Exit code 1: State file exists (resume scenario)
# Exit code 2: Invalid story ID - HALT
```

---

## Mandatory Steps

**Purpose:** 13-step validation before TDD begins

**Required Subagents:**
- git-validator (Git availability check)
- tech-stack-detector (Technology detection)

**Steps:**

1. **Validate Git status** (git-validator subagent)
   ```
   Task(
     subagent_type="git-validator",
     description="Validate Git repository status",
     prompt="Check Git availability and repository status for workflow strategy"
   )
   ```

1.5. **User consent for git operations** (if uncommitted changes >10)
   - Use AskUserQuestion if uncommitted changes detected
   - Option: Stash, Continue, Abort

1.6. **Stash warning and confirmation** (if user chooses to stash)

1.7. **Check for existing plan file**
   ```
   Glob(".claude/plans/*.md")
   Grep(pattern="${STORY_ID}", path="{plan_file}")
   ```
   - If match found, offer to resume via AskUserQuestion

1.8. **Memory File Session Recovery** (STORY-303)
   ```
   # Check for existing memory file
   memory_path = ".claude/memory/sessions/${STORY_ID}-dev-session.md"

   IF file_exists(memory_path):
     # Read and validate memory file
     state = read_session_state(STORY_ID, "dev")

     IF state is not null:
       # Previous session detected - prompt for recovery
       Display: "Previous session found at Phase {state.current_phase} ({state.phase_progress * 100}% complete)"

       AskUserQuestion:
         Question: "Resume from previous session?"
         Options: ["Yes, resume from Phase {state.current_phase}", "No, start fresh session"]

       IF resume selected:
         SET $RESUME_PHASE = state.current_phase
         SET $RESUME_PROGRESS = state.phase_progress
         Display: "Resuming from Phase {$RESUME_PHASE} ({$RESUME_PROGRESS * 100}% complete)"
         # Skip completed phases
     ELSE:
       # Memory file corrupted - handled by handle_corrupted_file()
       # Proceeds with fresh session
   ELSE:
     # No memory file - backward compatibility
     Display: "Starting fresh session (no previous state found)"
   ```

   **Reference:** `references/memory-file-operations.md`

2. **Git Worktree Auto-Management** (git-worktree-manager subagent)
   ```
   Task(
     subagent_type="git-worktree-manager",
     description="Manage Git worktree for ${STORY_ID}",
     prompt="Create/manage worktree for parallel development"
   )
   ```

3. **Adapt workflow** (Git vs file-based)

4. **File-based tracking setup** (if no Git)

5. **Validate 6 context files exist**
   ```
   Read(file_path="devforgeai/specs/context/tech-stack.md")
   Read(file_path="devforgeai/specs/context/source-tree.md")
   Read(file_path="devforgeai/specs/context/dependencies.md")
   Read(file_path="devforgeai/specs/context/coding-standards.md")
   Read(file_path="devforgeai/specs/context/architecture-constraints.md")
   Read(file_path="devforgeai/specs/context/anti-patterns.md")
   ```

6. **Load story specification**
   ```
   Read(file_path="${STORY_FILE}")
   ```

7. **Validate spec vs context conflicts**

8. **Detect tech stack** (tech-stack-detector subagent)
   ```
   Task(
     subagent_type="tech-stack-detector",
     description="Detect technology stack for ${STORY_ID}",
     prompt="Auto-detect project technologies, validate against tech-stack.md"
   )
   ```

9. **Detect QA failures** (recovery mode check)

9.5. **Load structured gap data** (if gaps.json exists)
   ```
   IF Glob("tests/results/${STORY_ID}/gaps.json"):
     Read(file_path="tests/results/${STORY_ID}/gaps.json")
     SET $REMEDIATION_MODE = true
   ```

10. **Technical Debt Threshold Evaluation** (STORY-289)

    **Purpose:** Enforce tiered alerts when technical debt accumulates to warn/block new development.

    ```
    # Step 10.1: Read technical-debt-register.md for thresholds and debt count
    Read(file_path="devforgeai/technical-debt-register.md")

    # Step 10.2: Parse YAML frontmatter thresholds (configurable per-project)
    # Extract from thresholds section:
    #   warning_count (default: 5)
    #   critical_count (default: 10)
    #   blocking_count (default: 15)
    # If thresholds section missing, use defaults

    warning_count = thresholds.warning_count OR 5
    critical_count = thresholds.critical_count OR 10
    blocking_count = thresholds.blocking_count OR 15

    # Step 10.3: Extract total_open from analytics section
    total_open = analytics.total_open

    # Step 10.4: Check for --ignore-debt-threshold flag
    IGNORE_DEBT_FLAG = "--ignore-debt-threshold" in $ARGUMENTS
    ```

    **Step 10.5: Tiered Threshold Evaluation**

    ```
    IF total_open >= blocking_count:
        # BLOCKING LEVEL (15+ items by default)

        IF IGNORE_DEBT_FLAG:
            # AC#4: Override flag present - prompt for consent
            AskUserQuestion(questions=[{
                question: "Technical debt threshold exceeded ({total_open} items). Override to proceed?",
                header: "Debt Override",
                options: [
                    {label: "Yes, I accept increased technical debt risk", description: "Proceed with workflow, override logged for audit"},
                    {label: "No, I'll reduce debt first", description: "HALT workflow and show remediation guidance"}
                ],
                multiSelect: false
            }])

            IF user selects "Yes, I accept increased technical debt risk":
                # AC#5: Log override and proceed with banner
                # Update phase-state.json with override entry:
                Edit(file_path="devforgeai/workflows/${STORY_ID}-phase-state.json") to add:
                {
                    "debt_override": {
                        "timestamp": "{current_timestamp}",
                        "debt_count": {total_open},
                        "acknowledgment": "User accepted technical debt risk"
                    }
                }

                Display: "⚠️ DEBT OVERRIDE ACTIVE: Proceeding with {total_open} open debt items"
                SET $DEBT_OVERRIDE_BANNER = true
                # Workflow proceeds with persistent warning banner

            ELSE:
                # AC#6: User declined - HALT on decline and show remediation guidance
                # User must reduce debt first. Workflow does not proceed.
                # Get 5 oldest open debt items sorted by date ascending (oldest first)
                oldest_items = parse_oldest_open_items(register, count=5)

                Display:
                "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
                "❌ HALT on decline - Technical Debt Remediation Required"
                "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
                ""
                "Oldest 5 open debt items to prioritize (sorted ascending):"
                FOR item in oldest_items:
                    Display: "  • {item.id}: {item.description}"
                    Display: "    Estimated effort: {item.effort} points | Linked follow-up story: STORY-XXX or {item.follow_up_story OR 'None'}"
                ""
                "Suggested action: Run '/dev STORY-XXX' on existing remediation stories"
                "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

                # Workflow does not proceed - must reduce debt first
                HALT workflow
        ELSE:
            # AC#3: No override flag - HALT with blocking message
            oldest_items = parse_oldest_open_items(register, count=5)

            Display:
            "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
            "❌ BLOCKED: Technical debt exceeds threshold ({total_open}/{blocking_count} items)"
            "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
            ""
            "Reduce debt before starting new work."
            ""
            "Oldest 5 open debt items (DEBT-NNN IDs):"
            FOR item in oldest_items:
                Display: "  • {item.id}: {item.description}"
            ""
            "To override: /dev {STORY_ID} --ignore-debt-threshold"
            "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

            # Workflow does not proceed - HALT workflow
            HALT workflow

    ELIF total_open >= critical_count:
        # AC#2: CRITICAL LEVEL (10-14 items by default)
        # Note: Escalation from warning to critical (10 > 5 threshold escalation)
        Display:
        "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
        "🔴 CRITICAL: Technical debt at {total_open} items (threshold: {critical_count})"
        "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
        "Strongly recommended to reduce debt before new development."
        "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

        # Workflow proceeds with prominent notice

    ELIF total_open >= warning_count:
        # AC#1: WARNING LEVEL (5-9 items by default)
        Display:
        "⚠️ Technical debt warning: {total_open} open items (threshold: {warning_count})"
        "Consider addressing debt before starting new work."

        # Workflow proceeds normally

    ELSE:
        # Below all thresholds - proceed silently
        # No display needed
    ```

    **Reference:** `references/preflight/01.10-debt-threshold.md` for complete threshold evaluation workflow

**Preflight reference files** (load on demand per step):

| Step | File | Trigger |
|------|------|---------|
| 01.0 | `references/preflight/01.0-project-root.md` | Always |
| 01.0.5 | `references/preflight/01.0.5-cli-check.md` | Always |
| 01.1 | `references/preflight/01.1-git-status.md` | Always |
| 01.1.5 | `references/preflight/01.1.5-user-consent.md` | uncommitted > 10 |
| 01.1.6 | `references/preflight/01.1.6-stash-warning.md` | user selects stash |
| 01.1.7 | `references/preflight/01.1.7-story-isolation.md` | uncommitted story files |
| 01.2 | `references/preflight/01.2-worktree.md` | Git available + enabled |
| 01.2.5 | `references/preflight/01.2.5-dependency-graph.md` | story has dependencies |
| 01.2.6 | `references/preflight/01.2.6-file-overlap.md` | parallel stories |
| 01.3 | `references/preflight/01.3-workflow-adapt.md` | Always |
| 01.4 | `references/preflight/01.4-file-tracking.md` | Git unavailable |
| 01.5 | `references/preflight/01.5-context-files.md` | Always |
| 01.6 | `references/preflight/01.6-load-story.md` | Always |
| 01.7 | `references/preflight/01.7-validate-spec.md` | Always |
| 01.8 | `references/preflight/01.8-tech-stack.md` | Always |
| 01.9 | `references/preflight/01.9-qa-failures.md` | Always |
| 01.10 | `references/preflight/01.10-complexity.md` | Always |
| Final | `references/preflight/completion-checkpoint.md` | Always |

11. **Session Memory Creation** (STORY-341)

    **Purpose:** Create per-story session memory file to persist observations throughout story lifecycle.

    ```
    # Create session memory file with YAML frontmatter
    session_path = ".claude/memory/sessions/${STORY_ID}-session.md"

    Write(
      file_path=session_path,
      content="""
      ---
      story_id: ${STORY_ID}
      created: ${CURRENT_TIMESTAMP}
      last_updated: ${CURRENT_TIMESTAMP}
      status: active
      ---
      # Session Memory: ${STORY_ID}
      ## Observations
      (Observations from phases 02-08 will be appended here)
      ## Reflections
      (Reflections from retry cycles will be appended here)
      ## Subagent Invocations
      | Timestamp | Subagent | Phase | Duration |
      |-----------|----------|-------|----------|
      ## Phase Progression
      | Phase | Started | Completed | Iterations |
      |-------|---------|-----------|------------|
      """
    )
    ```

    **Session Memory Schema:**
    - `story_id`: Story identifier (STORY-NNN format, required)
    - `created`: ISO8601 timestamp when session started (required)
    - `last_updated`: ISO8601 timestamp of last modification (required)
    - `status`: Session lifecycle status - `active` or `archived` (required)

    **Sections:**
    - **Observations**: Phase observations with category, note, severity
    - **Reflections**: TDD retry cycle learnings (what happened, why, how to improve)
    - **Subagent Invocations**: Track subagent calls for analysis
    - **Phase Progression**: Track phase timing and iterations

    **Reference:** EPIC-052 Session Memory Layer specification

12. **Stale Session Cleanup** (STORY-341)

    **Purpose:** Clean up stale session files to prevent directory bloat.

    ```
    # Check for stale sessions (>7 days old with status=active)
    stale_sessions = Glob(pattern=".claude/memory/sessions/*-session.md")

    FOR each session_file in stale_sessions:
        Read(file_path=session_file)

        # Parse frontmatter for created date and status
        IF status == "active" AND (CURRENT_DATE - created) > 7 days:
            # Archive stale session by updating status
            Edit(
              file_path=session_file,
              old_string="status: active",
              new_string="status: archived"
            )
            Display: "Archived stale session: {session_file}"
    ```

    **Stale Session Criteria:**
    - Session file exists in `.claude/memory/sessions/` directory
    - YAML frontmatter `status` field equals `active`
    - Session age exceeds 7 days (based on `created` timestamp)

    **Cleanup Action:** Update `status` field from `active` to `archived`

13. **Context Preservation Validation** (STORY-299)
   ```
   Task(
     subagent_type="context-preservation-validator",
     description="Validate context preservation for ${STORY_ID}",
     prompt="Validate story-to-epic-to-brainstorm chain for ${STORY_FILE}. Trace full provenance and report chain status (intact/partial/broken)."
   )
   ```
   - Non-blocking by default (warnings only)
   - Reports provenance chain status
   - Generates recommendations for missing context

---

## Validation Checkpoint

**Before proceeding to Phase 02, verify:**

- [ ] git-validator subagent invoked
- [ ] Context files validated (6 files)
- [ ] Story specification loaded
- [ ] tech-stack-detector subagent invoked

**IF any checkbox UNCHECKED:** HALT workflow

---

## Pre-Exit Checklist

**Before calling `phase-complete`, verify ALL items:**

- [ ] git-validator invoked
- [ ] 6 context files loaded and validated
- [ ] Story loaded and validated
- [ ] tech-stack-detector invoked
- [ ] Session memory created
- [ ] Stale cleanup executed
- [ ] context-preservation-validator invoked

**IF any item UNCHECKED and no N/A justification:** HALT — do not call exit gate.

---

## Optional Captures

### Observation Capture

**Before exiting this phase, reflect:**
1. Did I encounter any friction? (unclear docs, missing tools, workarounds)
2. Did anything work particularly well? (constraints that helped, patterns that fit)
3. Did I notice any repeated patterns?
4. Are there gaps in tooling/docs?
5. Did I discover any bugs?

**If YES to any:** Append to phase-state.json `observations` array:
```json
{
  "id": "obs-01-{seq}",
  "phase": "01",
  "category": "{friction|success|pattern|gap|idea|bug}",
  "note": "{1-2 sentence description}",
  "files": ["{relevant files}"],
  "severity": "{low|medium|high}"
}
```

**Reference:** `references/observation-capture.md`
    Read(file_path="references/observation-capture.md")

### Record Subagents

```bash
# Record after each subagent invocation:
# (Called automatically by orchestrator)
# devforgeai-validate phase-record ${STORY_ID} --phase=01 --subagent=git-validator
# devforgeai-validate phase-record ${STORY_ID} --phase=01 --subagent=tech-stack-detector
```

---

## Exit Gate

```bash
devforgeai-validate phase-complete ${STORY_ID} --phase=01 --checkpoint-passed
# Exit code 0: Phase complete, proceed to Phase 02
# Exit code 1: Cannot complete - validation failed
```

---

## Change Log

| Date | Story | Change |
|------|-------|--------|
| 2026-02-02 | STORY-341 | Added Session Memory Creation (Step 11) and Stale Session Cleanup (Step 12) |
| 2026-03-02 | STORY-523 | Restructured with Mandatory/Optional separation |
