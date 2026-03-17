---
description: Run QA validation on story implementation
argument-hint: [STORY-ID] [mode]
model: opus
effort: Medium
allowed-tools: AskUserQuestion, Read, Glob, Agent
execution-mode: immediate
---

# /qa - Quality Assurance Validation

Execute QA validation on story implementation (light during dev, deep after completion).

Do not skip any phases nor skip the devforgeai-qa skill.

You MUST execute the devforgeai-qa skill, when called upon: Skill(command="devforgeai-qa")

```bash
/qa STORY-001 light    # Light validation (~1 min)
/qa STORY-001 deep     # Deep validation (~5 min)
/qa STORY-001          # Auto-infer mode from story status
```

## Lean Orchestration Enforcement

**DO NOT (before skill invocation):**
- DO NOT validate CWD (skill Phase 0 handles this)
- DO NOT read or parse context files (skill handles context validation)
- DO NOT infer mode from story status (skill parameter extraction handles this)
- DO NOT generate QA reports or update story files (skill Phases 3-4 handle this)
- DO NOT invoke feedback hooks (skill Phase 4 handles this)

**DO (command responsibilities only):**
- Validate story ID format via AskUserQuestion if invalid
- Validate story file exists via Glob
- Set context markers (Story ID, Validation Mode)
- Invoke skill immediately after validation

## Phase 0: Argument Validation

```
IF plan mode active: ExitPlanMode()
IF $1 empty OR NOT "STORY-[0-9]+":
  AskUserQuestion(question="Story ID invalid. What story?", header="Story ID",
    options=["List Dev Complete stories","List In Development stories","Show syntax"])
Glob: IF story not found: AskUserQuestion(question="Not found", options=["List","Cancel"])
IF $2 in ["deep","light"]: MODE=$2
ELIF $2 "--mode=X": extract; AskUserQuestion if invalid
ELIF $2 unknown: AskUserQuestion for valid mode
ELSE: MODE="auto" (Dev Complete->deep, In Development->light, other->AskUserQuestion)
**Story ID:** ${STORY_ID}  |  **Mode:** ${MODE}
```

## Phase 1: Invoke Skill

```
Agent(subagent_type="qa-executor", prompt="Execute QA validation for ${STORY_ID}. Mode: ${MODE}.")
```

qa-executor handles: CWD validation, tests, coverage, anti-patterns, reports, story updates, hooks.

Skill(command="devforgeai-qa")

## Phase 2: Display Results

Output `result.display.template` and `result.next_steps` as-is.

## Error Handling

| Error | Message | Recovery |
|-------|---------|----------|
| Story ID Invalid | `Usage: /qa STORY-001 [mode]` | Provide valid STORY-NNN |
| Story Not Found | `Path: devforgeai/specs/Stories/{ID}.story.md` | Check ID, list stories |
| Invalid Mode | `Valid: light, deep` | Use positional: `/qa STORY-001 deep` |
| Skill Failed | `QA validation failed` | Check context files, verify tests, retry |

## Success Criteria

Story validated, mode set, skill invoked, results displayed, story updated (deep pass only).

## Integration

**Invoked by:** Developer, implementing-stories (light), orchestration (deep)
**Invokes:** qa-executor subagent -> devforgeai-qa workflow -> specialist subagents
**Gates:** Gate 2 (Test Passing), Gate 3 (QA Approval)

## Related Commands

- `/dev STORY-ID` - Return to development after QA failure
- `/release STORY-ID` - Deploy QA-approved story
- `/orchestrate STORY-ID` - Full lifecycle (dev -> qa -> release)

## Performance Targets

| Mode | Time | Tokens |
|------|------|--------|
| Light | <2 min | <15K |
| Deep | <5 min | <70K |
