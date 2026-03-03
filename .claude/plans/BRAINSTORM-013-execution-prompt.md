# Execution Prompt: Claude Hooks Phase Enforcement

**Copy-paste this entire prompt into a fresh Claude Code session to execute the plan.**

---

## Prompt

Read the plan file at `.claude/plans/smooth-tumbling-beacon.md`. This plan implements Claude Code hooks for step-level phase enforcement with progressive task disclosure across the DevForgeAI `/dev` workflow.

**Your mission:** Execute this plan by creating an epic and 6 stories, then implementing them.

### Step 1: Read the Plan

```
Read(".claude/plans/smooth-tumbling-beacon.md")
```

The plan contains:
- Full problem statement (Section 1)
- Solution architecture (Section 2)
- Complete Claude Code hooks reference (Section 3)
- 72-step phase registry across 12 phases (Section 4)
- 6 implementation stories with complete hook script code (Section 5)
- Progress checkpoints (Section 6)
- File locations reference (Section 7)
- Verification plan (Section 8)

### Step 2: Create the Epic

Use `/create-epic` to create an epic for this work:

**Epic title:** "Claude Hooks for Step-Level Phase Enforcement"
**Epic description:** External enforcement mechanism using Claude Code hooks (SubagentStop, TaskCompleted, Stop, SessionStart) to prevent phase/step skipping in the /dev workflow. Includes progressive task disclosure to reduce context bloat. Derived from BRAINSTORM-013.
**Features (6):**
1. Phase Steps Registry + Step-Level Tracking in phase_state.py (5 pts)
2. SubagentStop Hook — Auto-Track Subagent Invocations (3 pts)
3. TaskCompleted Hook — Step Validation Gate (5 pts)
4. Stop Hook — Phase Completion Gate (5 pts)
5. SessionStart Hook — Progressive Context Injection (3 pts)
6. Phase File TaskCreate Integration (3 pts)

**Total:** 24 story points

### Step 3: Create Stories from Epic

Use `/create-story` for each of the 6 stories. The plan (Section 5) contains complete specifications for each story including:
- Exact files to create/modify
- Complete hook script implementations (copy-paste ready bash scripts)
- Acceptance criteria
- Existing infrastructure to reuse (with file paths and line numbers)

### Step 4: Implement Stories

Use `/dev` to implement each story in order (Story 1 → Story 6). Stories must be implemented sequentially because:
- Story 2 (SubagentStop hook) depends on Story 1 (registry + CLI command)
- Story 3 (TaskCompleted hook) depends on Story 1 (registry) and Story 2 (subagent tracking)
- Story 4 (Stop hook) depends on Story 1 (phase state tracking)
- Story 5 (SessionStart hook) depends on Story 1 (registry)
- Story 6 (phase file updates) depends on Story 1 (registry)

### Step 5: Update Progress Checkpoints

After each story completes, update the progress checkpoints in Section 6 of the plan file (`.claude/plans/smooth-tumbling-beacon.md`). This allows any future session to see exactly where implementation stands.

### Key Constraints

- **Source tree:** All Python code changes go in `src/` tree first, then sync to operational `.claude/` folders
- **Hook scripts:** Go directly in `.claude/hooks/` (operational, committable)
- **Settings:** Modify `.claude/settings.json` for hook configuration
- **Tests:** Run against `src/` tree, never operational folders
- **TDD:** All stories follow Red-Green-Refactor (mandatory per framework rules)

### Recovery

If this session is interrupted or context is cleared:
1. Read `.claude/plans/smooth-tumbling-beacon.md`
2. Check Section 6 (Progress Checkpoints) for completed items
3. Resume from the next unchecked item
4. Check `devforgeai/specs/Stories/` for any already-created story files
5. Check `devforgeai/specs/Epics/` for the epic file
