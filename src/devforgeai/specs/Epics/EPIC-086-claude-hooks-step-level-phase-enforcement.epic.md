---
id: EPIC-086
title: Claude Hooks for Step-Level Phase Enforcement
status: Planning
priority: Critical
business_value: High
timeline: 1-2 sprints
total_points: 24
completed_points: 0
created: 2026-03-02
updated: 2026-03-02
owner: Bryan
tech_lead: DevForgeAI AI Agent
team: DevForgeAI
source: BRAINSTORM-013
plan: ~/.claude/plans/smooth-tumbling-beacon.md
---

# Epic: Claude Hooks for Step-Level Phase Enforcement

## Business Goal

Claude consistently skips mandatory phases, steps, and subagent invocations during `/dev` workflow execution despite extensive prompt-level instructions. Evidence from STORY-522 shows `subagents_invoked: []` across ALL 12 phases even when phases are marked "completed" — a 0% compliance rate on subagent invocation tracking. Current enforcement is 100% self-policed: Claude is both executor and auditor of its own phase compliance.

This epic implements an **external enforcement mechanism** using Claude Code hooks (SubagentStop, TaskCompleted, Stop, SessionStart) that operate outside Claude's decision-making process and cannot be rationalized away. Combined with progressive task disclosure (one phase's tasks at a time instead of all 72), this addresses both root causes: lack of external verification and context window bloat causing late-phase skipping.

The fundamental insight: prompt-level enforcement is policy ("please don't push to main"), hooks are enforcement (branch protection rules). We've been relying on policy. Hooks give us enforcement.

## Success Metrics

- **Metric 1:** `subagents_invoked` populated in phase-state.json — from 0% (always empty) to 100% for all completed phases
- **Metric 2:** Phases with required subagents actually invoked — from unknown/untracked to 95%+
- **Metric 3:** Workflow completions with all 12 phases executed — from estimated ~40% to 90%+
- **Metric 4:** Phase skips caught before session end — from 0 (all self-reported) to 80%+ caught by hooks

**Measurement Plan:**
- Compare phase-state.json `subagents_invoked` arrays before/after hook deployment
- Track Stop hook re-trigger frequency (indicates mid-workflow stop attempts)
- Monitor TaskCompleted hook block rate (indicates skipped subagent invocations)
- Review frequency: After first full `/dev` run with hooks active

## Scope

### In Scope

1. **Feature 1: Phase Steps Registry + Step-Level Tracking** (5 pts)
   - Create 72-step registry JSON derived from Pre-Exit Checklists in all 12 phase files
   - Add `record_step()` and `validate_phase_steps()` to phase_state.py
   - Add `phase-record-step` CLI command
   - Business value: Foundation for all hook-based enforcement — provides the source of truth for what each phase requires

2. **Feature 2: SubagentStop Hook — Auto-Track Invocations** (3 pts)
   - Shell script triggered on SubagentStop event
   - Automatically records subagent type in phase-state.json `subagents_invoked`
   - Filters out built-in agents (Explore, Plan, Bash)
   - Business value: Creates externally-verified audit trail — `subagents_invoked` becomes trustworthy because it's populated by a hook, not by Claude's self-reporting

3. **Feature 3: TaskCompleted Hook — Step Validation Gate** (5 pts)
   - Shell script triggered on TaskCompleted event
   - Blocks task completion if step requires a subagent that wasn't invoked
   - Supports OR-logic (e.g., backend-architect OR frontend-developer)
   - Handles conditional steps (N/A logic)
   - Business value: Prevents Claude from marking steps "done" without actually doing the work

4. **Feature 4: Stop Hook — Phase Completion Gate** (5 pts)
   - Shell script triggered on Stop event
   - Blocks Claude from stopping if active workflow has incomplete phases
   - Infinite loop prevention via counter file (max 3 re-triggers)
   - Reports which phase/steps are incomplete in stderr
   - Business value: The nuclear option — Claude literally cannot stop until the workflow is done

5. **Feature 5: SessionStart Hook — Progressive Context Injection** (3 pts)
   - Shell script triggered on SessionStart (resume/compact events only)
   - Re-injects active workflow state into Claude's context
   - Includes current phase, completed steps, required subagents
   - Business value: Survives compaction — Claude gets workflow state re-injected every time context is lost

6. **Feature 6: Phase File TaskCreate Integration** (3 pts)
   - Add Progressive Task Disclosure section to all 12 phase files
   - Instructions to create TaskCreate tasks for ONLY the current phase's steps
   - References phase-steps-registry.json for step definitions
   - Business value: Reduces active task list from 72 to 4-8 items, reducing context bloat and token optimization bias

### Out of Scope

- ❌ PreToolUse hook for phase-state write protection — deferred to Tier 2 after Tier 1 proven
- ❌ LLM-based phase auditor (prompt hook) — experimental, deferred to Tier 3
- ❌ Agent-based deep phase verifier — experimental, deferred to Tier 3
- ❌ PreCompact checkpoint hook — lower priority, deferred
- ❌ Modifying existing pre-commit hook (DoD validation) — unchanged by this epic

## Target Sprints

### Sprint 1 (Single Sprint): Hook Foundation + All 6 Features

**Goal:** Implement complete hook-based enforcement stack
**Estimated Points:** 24
**Features:** All 6 features (sequential dependencies)

**Execution Order (Dependencies):**
1. Story 1: Registry + Step Tracking (foundation — all others depend on this)
2. Story 2: SubagentStop Hook (depends on Story 1 for `phase-record` CLI)
3. Story 3: TaskCompleted Hook (depends on Story 1 registry + Story 2 subagent tracking)
4. Story 4: Stop Hook (depends on Story 1 phase state tracking)
5. Story 5: SessionStart Hook (depends on Story 1 registry)
6. Story 6: Phase File Updates (depends on Story 1 registry)

**Key Deliverables:**
- phase-steps-registry.json with 72 steps
- 4 hook scripts in .claude/hooks/
- Updated settings.json with all hook configurations
- Enhanced phase_state.py with step-level tracking
- 12 updated phase files with Progressive Task Disclosure

## User Stories

| Story | Feature | Points | Status | Depends On |
|-------|---------|--------|--------|------------|
| [STORY-525](../Stories/STORY-525-phase-steps-registry-step-level-tracking.story.md) | Feature 1: Phase Steps Registry + Step-Level Tracking | 5 | Backlog | — |
| [STORY-526](../Stories/STORY-526-subagent-stop-hook-auto-track-invocations.story.md) | Feature 2: SubagentStop Hook — Auto-Track Invocations | 3 | Backlog | STORY-525 |
| [STORY-527](../Stories/STORY-527-task-completed-hook-step-validation-gate.story.md) | Feature 3: TaskCompleted Hook — Step Validation Gate | 5 | Backlog | STORY-525, STORY-526 |
| [STORY-528](../Stories/STORY-528-stop-hook-phase-completion-gate.story.md) | Feature 4: Stop Hook — Phase Completion Gate | 5 | Backlog | STORY-525 |
| [STORY-529](../Stories/STORY-529-session-start-hook-context-injection.story.md) | Feature 5: SessionStart Hook — Progressive Context Injection | 3 | Backlog | STORY-525 |
| [STORY-530](../Stories/STORY-530-phase-file-taskcreate-integration.story.md) | Feature 6: Phase File TaskCreate Integration | 3 | Backlog | STORY-525 |

**Execution Order:** STORY-525 → STORY-526 → STORY-527 (parallel: STORY-528, STORY-529, STORY-530)

## Technical Considerations

### Architecture Impact
- **New files:** 4 hook scripts in `.claude/hooks/`, 1 registry JSON (`.claude/hooks/phase-steps-registry.json`)
- **Modified source files (src/ tree — canonical for development):**
  - `src/claude/scripts/devforgeai_cli/phase_state.py` — add `record_step()`, `validate_phase_steps()`, `load_registry()` methods
  - `src/claude/scripts/devforgeai_cli/commands/phase_commands.py` — add `phase-record-step` CLI subcommand
  - `src/claude/skills/implementing-stories/phases/phase-{01..10}.md` + `phase-04.5-*.md` + `phase-05.5-*.md` — add Progressive Task Disclosure section
- **Modified operational files (sync targets after src/ changes):**
  - `.claude/scripts/devforgeai_cli/phase_state.py` — synced from src/
  - `.claude/scripts/devforgeai_cli/commands/phase_commands.py` — synced from src/
  - `.claude/skills/implementing-stories/phases/*.md` — synced from src/
  - `.claude/settings.json` — hook configuration added directly (operational, no src/ equivalent)
- **Dual-path rule:** All Python/phase-file edits go to `src/` first, then sync to `.claude/` operational folders. Hook scripts go directly to `.claude/hooks/` (operational, committable). `.claude/settings.json` is edited directly (operational config).
- **No new services/components** — hooks are standalone shell scripts
- **Integration:** Hooks supplement existing prompt-level enforcement (additive, not replacement)

### Existing Infrastructure to Extend (phase_state.py)

Key existing code in `src/claude/scripts/devforgeai_cli/phase_state.py`:

| Element | Line | Purpose | How We Extend It |
|---------|------|---------|-----------------|
| `DEV_PHASES` dict | ~158 | Generic phase step names | Registry JSON replaces with 72 specific steps |
| `PHASE_REQUIRED_SUBAGENTS` dict | ~202 | Maps phases → required subagents | Registry JSON supersedes as source of truth |
| `record_subagent()` method | ~717 | Records subagent invocation in phase-state | Pattern for new `record_step()` method |
| `_atomic_write()` method | ~452 | Thread-safe JSON file writes | Reused by `record_step()` |
| `SubagentEnforcementError` class | ~127 | Exception for missing subagents | Pattern for new `StepEnforcementError` |
| `complete_phase()` method | varies | Marks phase done | Modified to call `validate_phase_steps()` before allowing completion |

### Existing CLI Commands (phase_commands.py)

Key existing commands in `src/claude/scripts/devforgeai_cli/commands/phase_commands.py`:

| Command | Line | Purpose | Relevance |
|---------|------|---------|-----------|
| `phase-record` | ~444 | Records subagent invocation via CLI | Story 2's SubagentStop hook calls this existing command |
| `phase-init` | varies | Initializes phase-state.json | Unchanged |
| `phase-complete` | varies | Marks phase complete | Unchanged |
| `phase-status` | varies | Shows current state | Unchanged |

**Important:** Story 1 adds a NEW `phase-record-step` command (for step tracking). Story 2's hook uses the EXISTING `phase-record` command (for subagent tracking). These are different commands.

### Existing settings.json Hook Configuration

Current `.claude/settings.json` hooks section (must merge new hooks into this):

```json
{
  "hooks": {
    "PreToolUse": [
      {"matcher": "Bash", "hooks": [{"type": "command", "command": "\"$CLAUDE_PROJECT_DIR\"/.claude/hooks/pre-tool-use.sh"}]}
    ],
    "PostToolUse": [
      {"matcher": "Edit|Write", "hooks": [{"type": "command", "command": "\"$CLAUDE_PROJECT_DIR\"/.claude/hooks/post-edit-write-check.sh", "timeout": 10}]},
      {"matcher": "Bash", "hooks": [{"type": "command", "command": "\"$CLAUDE_PROJECT_DIR\"/.claude/hooks/post-bash-test-check.sh", "timeout": 10}]}
    ],
    "PermissionRequest": [
      {"matcher": "Bash(devforgeai:*)", "hooks": [{"type": "command", "command": "echo '{\"decision\": \"approve\"}'"}]}
    ]
  }
}
```

New hooks to ADD (do not replace existing):
- `SubagentStop` — new event (Story 2)
- `TaskCompleted` — new event (Story 3)
- `Stop` — new event (Story 4)
- `SessionStart` — new event with matcher `resume|compact` (Story 5)

### Technology Decisions
- **Bash + jq** for hook scripts (already in tech-stack.md, lightweight, fast)
- **JSON registry** for step definitions (parseable by both Python CLI and Bash hooks)
- **Counter file** for infinite loop prevention (project-local `tmp/`, not system `/tmp/`)
- **No new dependencies** — uses existing `jq`, `bash`, `devforgeai-validate` CLI

### Security & Compliance
- Hook scripts are project-scoped (`.claude/settings.json`), not user-level
- Scripts read stdin JSON and phase-state files — no network access, no secrets
- Exit code 2 is the only blocking mechanism — well-documented Claude Code behavior

### Performance Requirements
- Hook scripts must complete within timeout (10-15s per script)
- Expected actual execution: <1s for JSON parsing with jq
- No database queries, no network calls — pure filesystem operations

### QA Workflow Scope
- All hooks filter out QA workflow phase-state files (`*-qa-*` pattern in `find` commands)
- Hooks only enforce the `/dev` workflow (implementing-stories skill), not `/qa`
- If `/qa` is running concurrently, hooks are no-ops for QA state files

### Hook Execution Order
- Claude Code executes hooks in the order they appear in the settings.json array
- Multiple hooks on the same event run sequentially
- No existing Stop/SubagentStop/TaskCompleted/SessionStart hooks exist — no ordering conflicts
- Existing PreToolUse/PostToolUse/PermissionRequest hooks are on different events — no interaction

## Decision Context

### Design Rationale

The hook-based approach was chosen over alternatives because it provides **external enforcement** — code that runs outside Claude's decision-making process. This is fundamentally different from prompt-level instructions which are "advisory" and subject to token optimization bias, context window pressure, and self-assessment conflict.

The 4-hook stack (SubagentStop → TaskCompleted → Stop → SessionStart) creates a closed feedback loop:
1. Subagent called → SubagentStop hook records it → phase-state reflects reality
2. Claude tries to complete step → TaskCompleted hook checks phase-state → blocks if subagent missing
3. Claude tries to stop → Stop hook checks phase-state → blocks if workflow incomplete
4. Context compacted → SessionStart hook re-injects state → workflow survives amnesia

### Rejected Alternatives

1. **Prompt-only enforcement (current approach)** — Rejected because evidence shows 0% subagent invocation compliance despite extensive prompt instructions. Claude is both executor and auditor, creating a fundamental conflict.
2. **PreToolUse hook for phase-state write protection** — Deferred (not rejected). Would prevent Claude from self-reporting phase completion, but adds complexity. Better to prove Tier 1 hooks first.
3. **LLM-based audit (prompt hook on Stop)** — Deferred to Tier 3. Haiku may not be reliable enough for complex workflow auditing. Could add later as defense-in-depth.
4. **Agent hook for deep verification** — Deferred to Tier 3. More powerful but slower (60s timeout). Better suited as periodic audit than per-turn enforcement.

### Adversary/Threat Model

- **Infinite loop risk:** Stop hook could create infinite re-triggers if phase-state tracking is broken. Mitigated by `stop_hook_active` check + 3-attempt counter file.
- **False positives:** TaskCompleted hook could block legitimate task completion if registry is wrong. Mitigated by conservative approach (exit 0 on any error, only exit 2 on proven violations).
- **Stale state:** Hook reads phase-state.json which could be stale. Mitigated by SubagentStop hook keeping it up-to-date in real-time.
- **Hook script errors:** If scripts crash, they exit non-zero (not 2), which is non-blocking by Claude Code convention. Graceful degradation built in.

### Implementation Constraints

- Hook scripts must be Bash (Claude Code hooks only support shell commands)
- `jq` must be available (standard in most dev environments, already used in project)
- Phase-state.json format must remain backward-compatible
- Must not interfere with existing pre-commit hook (DoD validation)
- All temporary files must use project-local `tmp/` per operational-safety.md
- All Python/phase-file changes go to `src/` tree first, then sync to `.claude/` operational folders (dual-path architecture per project CLAUDE.md)
- Tests run against `src/` tree, never operational folders (per project CLAUDE.md)

### Key Insights from Discovery

- **BRAINSTORM-013 evidence:** STORY-522 phase-state.json showed `subagents_invoked: []` and `steps_completed: []` for ALL 12 phases despite "completed" status — proving self-reporting is unreliable
- **Token optimization bias** is the #1 root cause of phase skipping — Claude rationalizes skipping as "efficiency"
- **Context window pressure** causes late phases (06-10) to get less attention as context fills up
- **Progressive task disclosure** (4-8 active tasks vs 72) directly combats context bloat
- **`stop_hook_active` flag** is critical for infinite loop prevention — documented in Claude Code hooks spec

## Dependencies

### Internal Dependencies
- [x] **STORY-522:** Pre-Exit Checklists in all 12 phase files — **Status:** Complete — provides the source data for the 72-step registry
- [x] **STORY-524:** Phase state tracking infrastructure — **Status:** Complete — provides `PhaseState`, `record_subagent()`, `_atomic_write()` methods to extend
- [x] **EPIC-031:** Phase Execution Enforcement System — **Status:** Partial — this epic implements the hook-based enforcement component

### External Dependencies
- [x] **Claude Code hooks feature:** Available in Claude Code — **Status:** Released — SubagentStop, TaskCompleted, Stop, SessionStart all supported
- [x] **jq:** JSON processor — **Status:** Available — required for hook scripts

## Risks & Mitigation

### Risk 1: Stop Hook Infinite Loop
- **Probability:** Medium
- **Impact:** High (stuck session, requires manual intervention)
- **Mitigation:** `stop_hook_active` boolean check + project-local counter file with 3-attempt max
- **Contingency:** User can `Ctrl+C` to force-quit; counter file auto-resets on next fresh stop attempt

### Risk 2: False Positives Blocking Progress
- **Probability:** Medium
- **Impact:** Medium (developer frustration, perceived slowdown)
- **Mitigation:** Conservative validation (exit 0 on any error, only exit 2 on proven violations); conditional steps pass through unblocked
- **Contingency:** Hooks can be temporarily disabled by commenting out in settings.json

### Risk 3: Hook Scripts Not Updated with Phase Changes
- **Probability:** Medium
- **Impact:** Medium (registry drift from actual phase requirements)
- **Mitigation:** Registry derives from phase files, not hardcoded expectations; Story 6 aligns phase files with registry
- **Contingency:** Re-generate registry from phase files via script

### Risk 4: Performance Overhead
- **Probability:** Low
- **Impact:** Low (hook execution adds <1s per event)
- **Mitigation:** All hooks use simple jq JSON parsing — no network calls, no database queries
- **Contingency:** Increase timeout if needed; hooks are designed to fail gracefully

## Stakeholders

### Primary Stakeholders
- **Product Owner:** Bryan — Framework vision and enforcement priorities
- **Tech Lead:** DevForgeAI AI Agent — Implementation and testing
- **QA Lead:** DevForgeAI QA Skill — Validation of hook behavior

### Additional Stakeholders
- **Framework Users:** Any developer using `/dev` command — directly affected by enforcement hooks
- **Framework Maintainers:** Contributors to phase files — must maintain registry alignment

## Timeline

```
Epic Timeline:
════════════════════════════════════════════════════
Week 1:  Stories 1-3 (Foundation + SubagentStop + TaskCompleted)
Week 2:  Stories 4-6 (Stop + SessionStart + Phase Files)
════════════════════════════════════════════════════
Total Duration: 1 sprint (2 weeks)
Target Release: 2026-03-16
```

### Key Milestones
- [ ] **Milestone 1:** Story 1 complete — Registry + step tracking foundation working
- [ ] **Milestone 2:** Stories 2-3 complete — SubagentStop + TaskCompleted hooks active
- [ ] **Milestone 3:** Story 4 complete — Stop hook preventing mid-workflow exits
- [ ] **Final:** Stories 5-6 complete — Full hook stack + progressive task disclosure

## Progress Tracking

### Sprint Summary

| Sprint | Status | Points | Stories | Completed | In Progress | Blocked |
|--------|--------|--------|---------|-----------|-------------|---------|
| SPRINT-TBD | Not Started | 24 | 6 | 0 | 0 | 0 |
| **Total** | **0%** | **24** | **6** | **0** | **0** | **0** |

### Burndown
- **Total Points:** 24
- **Completed:** 0
- **Remaining:** 24
- **Velocity:** TBD

## Retrospective (Post-Epic)

*To be completed after epic completes*

---

**Epic Template Version:** 1.0
**Last Updated:** 2026-03-02
