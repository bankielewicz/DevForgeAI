---
description: Implement user story using TDD workflow
argument-hint: [STORY-ID] [--force] [--fix] [--ignore-debt-threshold]
model: Sonnet
effort: High
allowed-tools: AskUserQuestion, Read, Skill, Bash(git:*)
execution-mode: immediate
---

# /dev - TDD Development Workflow

Execute full Test-Driven Development cycle for a user story.

You MUST execute the spec-driven-dev skill, when called upon: Skill(command="spec-driven-dev")
---

## Phase 0: Parse Arguments and Set Context Markers

```
STORY_ID = null
FORCE_FLAG = false
REMEDIATION_MODE = false
IGNORE_DEBT_FLAG = false

FOR arg in arguments:
    IF arg == "--force": FORCE_FLAG = true
    ELIF arg == "--fix": REMEDIATION_MODE = true
    ELIF arg == "--ignore-debt-threshold": IGNORE_DEBT_FLAG = true
    ELIF arg matches "STORY-[0-9]+": STORY_ID = arg

IF STORY_ID empty:
    Display: "Usage: /dev STORY-NNN [--force] [--fix] [--ignore-debt-threshold]"
    HALT
```

Run preflight (finds story, detects gaps.json/qa-recommendations, creates/resumes phase state, and emits next-action guidance in one call):
```
result = Bash(command="devforgeai-validate dev-preflight ${STORY_ID} --project-root=. --format=json")
Parse JSON result:
  IF exit 1: Display "Story not found: $STORY_ID" and HALT
  IF exit 3 AND result.next_action == "halt-corrupt-state":
    Display "❌ ${result.guidance}" and HALT
  IF exit 3: Display "Invalid story ID format" and HALT
  IF exit 0 or 2:
    # Legacy markers (Sprint 4)
    Extract result.story_file → $STORY_FILE
    Extract result.remediation_mode → $REMEDIATION_MODE_FROM_PREFLIGHT
    Extract result.current_phase → $CURRENT_PHASE
    Extract result.qa_recommendations → $QA_RECOMMENDATIONS_STATUS
    Extract result.remediation_source → $REMEDIATION_SOURCE
    Extract result.open_rec_ids → $OPEN_REC_IDS
    # STORY-658 next-action markers
    Extract result.next_action → $NEXT_ACTION
    Extract result.next_command → $NEXT_COMMAND
    Extract result.next_phase_to_enter → $NEXT_PHASE_TO_ENTER
    Extract result.guidance → $GUIDANCE
    Extract result.cycle_status → $CYCLE_STATUS
    # Combine flag-based REMEDIATION_MODE (from --fix) with auto-detected one
    IF $REMEDIATION_MODE_FROM_PREFLIGHT == true: REMEDIATION_MODE = true
```

---

## Phase 0.5: Display Mode Banner (STORY-658)

```
IF $NEXT_ACTION == "phase-cycle-start":
    # Remediation re-entry on completed (phase 10) story
    open_count = $QA_RECOMMENDATIONS_STATUS.open_count IF $QA_RECOMMENDATIONS_STATUS ELSE 0
    blocking_count = $QA_RECOMMENDATIONS_STATUS.blocking_count IF $QA_RECOMMENDATIONS_STATUS ELSE 0
    by_severity = $QA_RECOMMENDATIONS_STATUS.by_severity IF $QA_RECOMMENDATIONS_STATUS ELSE {}
    Display: ""
    Display: "╔═══════════════════════════════════════════════════════════════════╗"
    Display: "║  REMEDIATION MODE — Story at phase ${CURRENT_PHASE}              ║"
    Display: "╠═══════════════════════════════════════════════════════════════════╣"
    Display: "║  Open recommendations: ${open_count} (${blocking_count} blocking) ║"
    Display: "║  Severity: C=${by_severity.CRITICAL} H=${by_severity.HIGH}        ║"
    Display: "║            M=${by_severity.MEDIUM} L=${by_severity.LOW}           ║"
    Display: "║                                                                   ║"
    Display: "║  Next action: ${NEXT_ACTION}                                      ║"
    Display: "║  Will reset to phase: ${NEXT_PHASE_TO_ENTER}                      ║"
    Display: "║                                                                   ║"
    Display: "║  ${GUIDANCE}                                                      ║"
    Display: "╚═══════════════════════════════════════════════════════════════════╝"
ELIF $NEXT_ACTION == "already-complete":
    Display: ""
    Display: "ℹ️  ${GUIDANCE}"
    Display: ""
    HALT  # Skill dispatcher will also halt; halting here saves a Skill load.
ELIF $NEXT_ACTION == "halt-ambiguous":
    Display: ""
    Display: "⚠️  ${GUIDANCE}"
    Display: "    The skill will ask for your decision via AskUserQuestion."
ELIF result.phase_state == "exists":
    # Generic resume display for any non-special action
    Display: "Resuming ${STORY_ID} from phase ${CURRENT_PHASE} (next action: ${NEXT_ACTION})"
    Display: "Guidance: ${GUIDANCE}"
ELSE:
    # Fresh workflow (begin-phase-01)
    Display: "▶ Beginning fresh workflow for ${STORY_ID} (phase 01)"
```

---

## Phase 1: Invoke Skill

```
Display: ""
Display: "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
Display: "  DevForgeAI Development Workflow"
Display: "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
Display: "**Story ID:** ${STORY_ID}"
Display: "Executing TDD workflow (Red > Green > Refactor > Integration)..."

**Story ID:** ${STORY_ID}
**Force Flag:** ${FORCE_FLAG}
**Remediation Mode:** ${REMEDIATION_MODE}
**Next Action:** ${NEXT_ACTION}
**Next Phase To Enter:** ${NEXT_PHASE_TO_ENTER}
**Cycle Status:** ${CYCLE_STATUS}
**Ignore Debt Threshold:** ${IGNORE_DEBT_FLAG}

Skill(command="spec-driven-dev")
```

---

## Phase 2: Display Results

Display skill's formatted result directly. No processing, parsing, or template generation in command. All business logic delegated to skill, all display templates generated by dev-result-interpreter subagent.

---

## Error Handling

| Error | Resolution |
|-------|------------|
| Invalid Story ID | Usage: /dev STORY-NNN |
| Story Not Found | Glob(pattern="devforgeai/specs/Stories/*.story.md") |
| Skill Failed | Check: context files (/create-system-architecture), git init, tech-stack.md |
