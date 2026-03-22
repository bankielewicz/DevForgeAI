# BRAINSTORM-013: Claude Hooks for Phase Execution Enforcement

**Session ID:** BRAINSTORM-013
**Created:** 2026-03-02
**Status:** Complete
**Confidence:** HIGH
**Feeds Into:** /ideate
**Related:** BRAINSTORM-002 (Phase Execution Enforcement System)

---

## Executive Summary

Claude consistently skips or ignores mandatory phases/steps in the `/dev` workflow and `implementing-stories` skill despite extensive prompt-level instructions. Current enforcement is entirely self-policed — Claude marks phases as "completed" without actually executing required steps or invoking required subagents (evidence: `subagents_invoked: []` across all phases in phase-state.json). **Claude Code hooks provide an external enforcement mechanism** that operates outside Claude's context window and cannot be rationalized away.

---

## 1. Problem Analysis

### What Claude Skips (Observed Patterns)

| Skip Pattern | Frequency | Impact |
|---|---|---|
| Subagent invocations (marks phase done without calling required subagent) | Very High | No code review, no AC verification, no test generation by specialist |
| Phase steps (e.g., skips Phase 04 Refactor, Phase 4.5 AC-Verify) | High | Quality regressions, untested code |
| Reference file loading at checkpoints | High | Decisions made without constraint awareness |
| Integration testing (Phase 05) | Medium | Cross-component bugs missed |
| Feedback capture (Phase 09) | Medium | Framework improvement data lost |

### Why Prompt-Level Enforcement Fails

1. **Token optimization bias** — Claude rationalizes skipping as "efficiency"
2. **Context window pressure** — Late phases get less attention as context fills
3. **Self-assessment conflict** — Claude is both executor and auditor
4. **No external verification** — Phase-state.json is written by the same agent that skips steps
5. **Compaction amnesia** — After auto-compact, phase instructions may be lost

### Evidence: STORY-522 Phase State

```json
"subagents_required": ["test-automator"],
"subagents_invoked": [],  // EMPTY despite "completed" status
"checkpoint_passed": true  // Self-reported as passed
```

This pattern repeats across ALL 12 phases.

---

## 2. Stakeholder Analysis

| Stakeholder | Goal | Pain Point |
|---|---|---|
| Developer (user) | Reliable TDD execution, quality assurance | Phases skipped silently, quality regressions |
| Framework maintainer | Consistent, verifiable workflows | Trust erosion, RCAs keep finding same root cause |
| QA process | Evidence that phases actually ran | Phase-state.json is unreliable self-reporting |

---

## 3. Hook Integration Opportunities

### 3.1 Stop Hook — Phase Completion Gate (HIGHEST IMPACT)

**Hook Type:** `Stop` (fires when Claude finishes responding)
**Mechanism:** Prevent Claude from stopping if active workflow has incomplete phases

```json
{
  "hooks": {
    "Stop": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "\"$CLAUDE_PROJECT_DIR\"/.claude/hooks/phase-completion-gate.sh",
            "timeout": 30
          }
        ]
      }
    ]
  }
}
```

**What the script does:**
1. Reads `devforgeai/workflows/STORY-*-phase-state.json` for active workflows
2. Checks if `current_phase` < final phase (10)
3. Checks if `subagents_invoked` is empty for completed phases
4. If incomplete: `exit 2` with stderr message "Workflow STORY-XXX has incomplete phases. Current: Phase 03. Next required: Phase 04. Required subagents not invoked: refactoring-specialist, code-reviewer"
5. If complete or no active workflow: `exit 0`

**Why this is highest impact:** Claude literally cannot stop until the workflow is done. This is the nuclear option — external enforcement that bypasses all prompt-level rationalization.

**Risk:** Could create infinite loops if phase-state tracking is broken. Mitigate with `stop_hook_active` check.

### 3.2 SubagentStop Hook — Subagent Invocation Tracker (HIGH IMPACT)

**Hook Type:** `SubagentStop` (fires when a subagent finishes)
**Mechanism:** Automatically record subagent invocations in phase-state.json

```json
{
  "hooks": {
    "SubagentStop": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "\"$CLAUDE_PROJECT_DIR\"/.claude/hooks/track-subagent-invocation.sh"
          }
        ]
      }
    ]
  }
}
```

**What the script does:**
1. Reads `agent_type` from stdin JSON
2. Finds active workflow phase-state file
3. Appends agent_type to current phase's `subagents_invoked` array
4. Logs timestamp and agent_id

**Why this matters:** Creates an externally-verified audit trail. The phase-state.json `subagents_invoked` field becomes trustworthy because it's populated by a hook, not by Claude's self-reporting.

### 3.3 TaskCompleted Hook — Phase Task Validation (HIGH IMPACT)

**Hook Type:** `TaskCompleted` (fires when TaskUpdate marks a task completed)
**Mechanism:** Block task completion if phase requirements not met

```json
{
  "hooks": {
    "TaskCompleted": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "\"$CLAUDE_PROJECT_DIR\"/.claude/hooks/validate-phase-task.sh"
          }
        ]
      }
    ]
  }
}
```

**What the script does:**
1. Parse `task_subject` for phase identifiers (e.g., "Phase 02", "Red phase")
2. If task is a phase task, check phase-state.json for:
   - Required subagents actually invoked
   - Required steps actually completed
3. If validation fails: `exit 2` with "Cannot complete Phase 02 task: test-automator subagent was never invoked"

### 3.4 PreToolUse Hook — Write Protection for Phase State (MEDIUM IMPACT)

**Hook Type:** `PreToolUse` matching `Edit|Write`
**Mechanism:** Prevent Claude from marking phases complete in phase-state.json without validation

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [
          {
            "type": "command",
            "command": "\"$CLAUDE_PROJECT_DIR\"/.claude/hooks/protect-phase-state.sh"
          }
        ]
      }
    ]
  }
}
```

**What the script does:**
1. Check if `file_path` targets a `*-phase-state.json` file
2. If attempting to change phase status to "completed":
   - Verify subagents_invoked is not empty (for phases that require subagents)
   - Verify checkpoint markers exist
3. If validation fails: deny the write

### 3.5 SessionStart Hook — Workflow Resume Context (MEDIUM IMPACT)

**Hook Type:** `SessionStart` matching `resume|compact`
**Mechanism:** Inject active workflow state into Claude's context on resume/compact

```json
{
  "hooks": {
    "SessionStart": [
      {
        "matcher": "resume|compact",
        "hooks": [
          {
            "type": "command",
            "command": "\"$CLAUDE_PROJECT_DIR\"/.claude/hooks/inject-workflow-context.sh"
          }
        ]
      }
    ]
  }
}
```

**What the script does:**
1. Scan for active `*-phase-state.json` files
2. Output `additionalContext` with: current story, current phase, next required steps, required subagents
3. This survives compaction — Claude gets workflow state re-injected every time

### 3.6 PreCompact Hook — Checkpoint Preservation (MEDIUM IMPACT)

**Hook Type:** `PreCompact`
**Mechanism:** Save critical workflow state before context compaction

**What the script does:**
1. Write current phase progress to a checkpoint file
2. Ensure phase-state.json is up to date before context is lost

### 3.7 Prompt Hook on Stop — LLM-Based Phase Audit (EXPERIMENTAL)

**Hook Type:** `Stop` with `type: "prompt"`
**Mechanism:** Use a second LLM to audit whether Claude actually completed work

```json
{
  "hooks": {
    "Stop": [
      {
        "hooks": [
          {
            "type": "prompt",
            "prompt": "Review the last assistant message. The agent is working on a DevForgeAI /dev workflow. Check if the agent: 1) Actually invoked required subagents (look for Agent tool calls), 2) Completed all numbered phases in order, 3) Did not skip any mandatory steps. If any phase was skipped, respond {\"ok\": false, \"reason\": \"Phase X was skipped. Required subagent Y was not invoked.\"}. Context: $ARGUMENTS",
            "timeout": 30
          }
        ]
      }
    ]
  }
}
```

**Advantage:** Can reason about the transcript content, not just file state.
**Risk:** Haiku may not be reliable enough for complex workflow auditing. Agent hook (`type: "agent"`) might be more appropriate but slower.

### 3.8 Agent Hook on Stop — Deep Phase Verification (EXPERIMENTAL)

**Hook Type:** `Stop` with `type: "agent"`
**Mechanism:** Spawn verifier subagent that can read files and check actual work products

```json
{
  "hooks": {
    "Stop": [
      {
        "hooks": [
          {
            "type": "agent",
            "prompt": "You are a DevForgeAI workflow auditor. Read the phase-state file at devforgeai/workflows/ to find the active workflow. For each phase marked 'completed', verify: 1) subagents_invoked is not empty when subagents_required is not empty, 2) test files exist for Red phase, 3) implementation files changed for Green phase. Report any discrepancies. $ARGUMENTS",
            "timeout": 60
          }
        ]
      }
    ]
  }
}
```

---

## 4. Recommended Hook Stack (Prioritized)

### Tier 1 — Implement Immediately (Highest ROI)

| # | Hook | Event | Type | Purpose |
|---|---|---|---|---|
| 1 | Phase Completion Gate | `Stop` | command | Block Claude from stopping with incomplete workflow |
| 2 | Subagent Invocation Tracker | `SubagentStop` | command | External audit trail of actual subagent calls |
| 3 | Workflow Resume Context | `SessionStart` | command | Re-inject workflow state after compact/resume |

### Tier 2 — Implement After Tier 1 Proven

| # | Hook | Event | Type | Purpose |
|---|---|---|---|---|
| 4 | Phase Task Validator | `TaskCompleted` | command | Block task completion without requirements met |
| 5 | Phase State Write Protection | `PreToolUse` | command | Prevent self-reported phase completion |

### Tier 3 — Experimental / Future

| # | Hook | Event | Type | Purpose |
|---|---|---|---|---|
| 6 | LLM Phase Auditor | `Stop` | prompt | Second-opinion LLM verification |
| 7 | Deep Phase Verifier | `Stop` | agent | Agent with file access verifies work products |
| 8 | Compact Checkpoint | `PreCompact` | command | Save state before context loss |

---

## 5. Architecture Considerations

### Hook Script Location
```
.claude/hooks/
  phase-completion-gate.sh      # Stop hook
  track-subagent-invocation.sh  # SubagentStop hook
  inject-workflow-context.sh    # SessionStart hook
  validate-phase-task.sh        # TaskCompleted hook
  protect-phase-state.sh        # PreToolUse hook
```

### Configuration Location
`.claude/settings.json` (project-scoped, committable to repo)

### Infinite Loop Prevention
The `Stop` hook receives `stop_hook_active: true` when Claude is already continuing due to a Stop hook. The script MUST check this flag:

```bash
#!/bin/bash
INPUT=$(cat)
STOP_HOOK_ACTIVE=$(echo "$INPUT" | jq -r '.stop_hook_active')

# Prevent infinite loops
if [ "$STOP_HOOK_ACTIVE" = "true" ]; then
  exit 0  # Allow stop on second attempt
fi
```

Better approach: Use a counter file to limit re-triggers (e.g., max 3 attempts before allowing stop).

### Phase State JSON as Source of Truth
The SubagentStop hook writes to phase-state.json externally. The Stop hook reads from it. This creates a closed loop:
- Subagent called → SubagentStop hook records it → phase-state reflects reality
- Claude tries to stop → Stop hook checks phase-state → blocks if incomplete

### Compatibility with Existing System
- Hooks supplement (not replace) existing prompt-level enforcement
- Phase-state.json format remains unchanged, just populated by hooks instead of self-reporting
- `devforgeai-validate` CLI can be invoked from hooks for validation
- Existing pre-commit hook for DoD validation continues unchanged

---

## 6. Risk Assessment

| Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|
| Stop hook infinite loop | Medium | High (stuck session) | `stop_hook_active` check + counter file |
| Hook scripts break workflow | Low | High | Conservative exit 0 on errors, only exit 2 on proven violations |
| Performance overhead | Low | Medium | Command hooks are fast (< 1s for JSON parsing) |
| False positives blocking progress | Medium | Medium | Graceful degradation: allow after N attempts |
| Hook scripts not updated with phase changes | Medium | Medium | Derive requirements from phase-state.json, not hardcoded |

---

## 7. Implementation Complexity

| Hook | Script Complexity | Dependencies | Estimated LOC |
|---|---|---|---|
| Phase Completion Gate (Stop) | Medium | jq, phase-state.json | ~50 lines bash |
| Subagent Tracker (SubagentStop) | Low | jq, phase-state.json | ~30 lines bash |
| Workflow Resume (SessionStart) | Low | jq, phase-state.json | ~40 lines bash |
| Phase Task Validator (TaskCompleted) | Medium | jq, phase-state.json | ~60 lines bash |
| Phase State Protection (PreToolUse) | Medium | jq | ~50 lines bash |

**Total estimated effort:** 2-3 stories across 1 sprint

---

## 8. Success Metrics

| Metric | Current State | Target |
|---|---|---|
| `subagents_invoked` populated in phase-state | 0% (always empty) | 100% for all completed phases |
| Phases with required subagents actually invoked | Unknown (no tracking) | 95%+ |
| Workflow completions with all 12 phases executed | Estimated ~40% | 90%+ |
| Phase skips caught before session end | 0 (all self-reported) | 80%+ caught by hooks |

---

## 9. Key Insight: External vs. Internal Enforcement

The fundamental insight is that **prompt-level enforcement is internal** — it relies on Claude following instructions. Hooks are **external** — they run outside Claude's decision-making process and can physically prevent actions (block tool calls, prevent stopping, deny task completion).

This is analogous to:
- Internal: "Please don't push to main" (policy)
- External: Branch protection rules (enforcement)

We've been relying on policy. Hooks give us enforcement.

---

## 10. Next Steps

1. **Feed into /ideate** to create epic with stories for hook implementation
2. **Start with Tier 1** (3 hooks) as a proof-of-concept sprint
3. **Measure** subagent invocation rates before and after
4. **Iterate** based on false positive/negative rates

---

## Appendix: Claude Hook Reference Summary

| Event | Can Block? | Key Capability |
|---|---|---|
| `Stop` | Yes | Prevent Claude from finishing (forces continuation) |
| `SubagentStop` | Yes | Track/validate subagent completion |
| `TaskCompleted` | Yes | Block task completion without requirements |
| `PreToolUse` | Yes | Block/modify tool calls before execution |
| `SessionStart` | No | Inject context (survives compact) |
| `PreCompact` | No | Save state before context loss |
| `SubagentStart` | No | Inject context into subagents |

Source: https://code.claude.com/docs/en/hooks
