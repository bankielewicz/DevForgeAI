---
description: Run QA validation on story implementation
argument-hint: [STORY-ID] [mode]
model: opus
effort: Medium
allowed-tools: AskUserQuestion, Read, Glob, Bash, Skill
execution-mode: immediate
---

# /qa — Quality Assurance Validation

Execute QA validation on story implementation. All workflow logic lives in the `spec-driven-qa` skill — this command is a thin orchestrator that validates story ID + mode, then invokes the skill immediately.

```bash
/qa STORY-001 light    # Light validation (~1 min)
/qa STORY-001 deep     # Deep validation (~5 min)
/qa STORY-001          # Auto-infer mode from story status
```

Invoke `spec-driven-qa`: `Skill(command="spec-driven-qa")`.

## Lean Orchestration Boundary

| Command | Skill |
|---------|-------|
| Validate story ID format | CWD validation, context files, mode inference |
| Validate story file exists (CLI / Glob fallback) | QA reports, story-file updates, feedback hooks |
| Set `$STORY_ID` + `$MODE` markers | All 6 phases |
| Invoke skill | — |

## Phase 0: Argument Validation

```
IF plan mode active: ExitPlanMode()
IF $1 empty OR NOT "STORY-[0-9]+":
  AskUserQuestion("Story ID invalid. What story?", header="Story ID",
    options=["List Dev Complete stories","List In Development stories","Show syntax"])

IF $2 in ["deep","light"]:                    MODE=$2
ELIF $2 matches "--mode=X":                   extract; AskUserQuestion if invalid
ELIF $2 unknown:                              AskUserQuestion for valid mode
ELSE:                                         MODE="auto"  (Dev Complete→deep, In Development→light, other→AskUserQuestion)

result = Bash("devforgeai-validate qa-setup ${STORY_ID} --workflow=qa --project-root=. --format=json 2>&1")
Parse JSON:
  IF "story_file" key present:                story found
  IF errors contains "Story file not found":  AskUserQuestion("Story not found", options=["List stories","Cancel"])
  IF exit 127 (CLI not installed):            fallback Glob("devforgeai/specs/Stories/${STORY_ID}*.story.md")
```

## Phase 1: Invoke Skill

```
Skill(command="spec-driven-qa")
```

## Phase 2: Display Results

Output `result.display.template` and `result.next_steps` as-is.

---

## Error Handling

| Error            | Message                                                 | Recovery                              |
|------------------|---------------------------------------------------------|---------------------------------------|
| Story ID Invalid | `Usage: /qa STORY-001 [mode]`                           | Provide valid STORY-NNN               |
| Story Not Found  | `Path: devforgeai/specs/Stories/{ID}.story.md`          | Check ID, list stories                |
| Invalid Mode     | `Valid: light, deep`                                    | Use positional: `/qa STORY-001 deep`  |
| Skill Failed     | `QA validation failed`                                  | Check context files, verify tests, retry |

## Success Criteria

Story validated, mode set, skill invoked, results displayed, story updated (deep pass only).

## Integration

**Invoked by:** Developer, spec-driven-dev (light), orchestration (deep)
**Invokes:** spec-driven-qa skill → specialist subagents
**Gates:** Gate 2 (Test Passing), Gate 3 (QA Approval)

## Related Commands

- `/dev STORY-ID` — Return to development after QA failure
- `/release STORY-ID` — Deploy QA-approved story
- `/orchestrate STORY-ID` — Full lifecycle (dev → qa → release)

## Performance Targets

| Mode  | Time   | Tokens |
|-------|--------|--------|
| Light | <2 min | <15K   |
| Deep  | <5 min | <70K   |
