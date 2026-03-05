---
description: Resume development from specific phase
argument-hint: [STORY-ID] [phase-number]
model: opus
allowed-tools: Read, Skill, Bash(git:*)
execution-mode: immediate
---

# /resume-dev - Resume Development from Specific Phase

Resume TDD workflow from specified phase when previous `/dev` execution was incomplete.

## Quick Reference

```bash
/resume-dev STORY-057 2    # Resume from Phase 2 (Implementation)
/resume-dev STORY-057      # Auto-detect resumption point from DoD
```

---

## Command Workflow

### Phase 0: Argument Validation

**Step 0.1: Parse arguments and load story**

```
STORY_ID = first argument matching "STORY-[0-9]+"
PHASE_NUM = second argument (optional, 0-7)

IF STORY_ID empty: Display usage and HALT
IF PHASE_NUM provided AND NOT in range 0-7: Display "Invalid phase. Valid: 0-7" and HALT
RESUME_MODE = IF PHASE_NUM provided THEN "manual" ELSE "auto"

@devforgeai/specs/Stories/$STORY_ID*.story.md
IF file not found: Display "Story not found: $STORY_ID" and HALT
```

---

### Phase 1: Set Resume Context Markers and Invoke Skill

**All pre-flight validation, checkpoint detection, and DoD analysis are handled by the implementing-stories skill via `references/resume-detection.md`.**

```
Display: ""
Display: "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
Display: "  DevForgeAI Development Workflow (RESUME MODE)"
Display: "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
Display: ""
Display: "**Story ID:** $STORY_ID"
Display: "**Resume from Phase:** $PHASE_NUM (or auto-detect)"
Display: "**Resume Mode:** $RESUME_MODE"
Display: ""
Display: "Resuming TDD workflow..."
Display: ""

Skill(command="implementing-stories")
```

---

### Phase 2: Display Results

Skill returns result to command. Display skill's formatted output directly.

---

## Lean Orchestration Enforcement

- DO NOT run tech-stack-detector in command (delegated to skill via resume-detection.md)
- DO NOT parse DoD sections in command (delegated to skill via resume-detection.md)
- DO NOT read checkpoint files in command (delegated to skill via resume-detection.md)
- DO NOT determine resume phase in command for auto mode (delegated to skill)

---

## Error Handling

Errors are handled at command level (argument validation) or skill level (business logic). For detailed error descriptions, see `references/resume-detection.md` (Error Handling section).

---

**Refactored:** 2026-02-20 (STORY-459) | 676 -> ~80 lines (88% reduction)
**Pattern:** EPIC-071 Pattern B (Pre-Flight Logic Extraction)
**Reference:** `.claude/skills/implementing-stories/references/resume-detection.md`
