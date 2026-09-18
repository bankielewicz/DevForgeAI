---
description: Create user story with acceptance criteria and technical specification
argument-hint: "[feature-description | EPIC-NNN | SEED-NNN | path/to/DEVARCH.development-architecture.html | --from-recommendations=STORY-NNN [--rec-ids=REC-A,REC-B] [--include-blocking]]"
model: opus
allowed-tools: Bash, Skill, AskUserQuestion
---

# /create-story

Transform a feature into a story file. Modes: SINGLE_STORY, EPIC_BATCH, FROM_RECOMMENDATIONS, DEVARCH_SEED. The skill (`spec-driven-stories`) owns mode detection, parsing, selection, creation, validation, and linking.

DEVARCH-seed input (SEED-NNN id or `*.development-architecture.html` path) uses its own early-route below — it does NOT flow through `story-preflight`.

## FROM_RECOMMENDATIONS early-route

```
IF $ARGUMENTS contains "--from-recommendations=":
    SOURCE_STORY_ID  = extract regex (?<=--from-recommendations=)STORY-\d+
    REC_IDS_FLAG     = extract (?<=--rec-ids=)[^ ]+   (or null)
    INCLUDE_BLOCKING = "--include-blocking" in $ARGUMENTS

    IF SOURCE_STORY_ID empty OR not matching STORY-\d+:
        Display "Usage: /create-story --from-recommendations=STORY-NNN [--rec-ids=...] [--include-blocking]"
        HALT

    **Mode:** FROM_RECOMMENDATIONS
    **Source Story ID:** ${SOURCE_STORY_ID}
    **Rec IDs Flag:** ${REC_IDS_FLAG or "null"}
    **Include Blocking:** ${INCLUDE_BLOCKING}
    Skill(command="spec-driven-stories")
    HALT — do NOT fall through to story-preflight
```

## DEVARCH_SEED early-route

```
IF $ARGUMENTS matches ^SEED-[0-9]{3,}$ OR $ARGUMENTS ends with ".development-architecture.html":
    DEVARCH_SOURCE = $ARGUMENTS

    **Mode:** DEVARCH_SEED
    **DEVARCH Source:** ${DEVARCH_SOURCE}
    Skill(command="spec-driven-stories")
    HALT — do NOT fall through to story-preflight
```

## Other modes — story-preflight CLI

```
result = Bash("devforgeai-validate story-preflight ${ARGUMENTS} --project-root=. --format=json 2>&1")

Parse result on exit 0:
  IF result.mode == "EPIC_BATCH" AND result.resume_session is not null:
    AskUserQuestion: "Resume session ${result.resume_session.session_id} at phase ${result.resume_session.current_phase}?"
    IF resume: set context from session
  Emit markers: **Mode:** ${result.mode}, **Epic ID:** ${result.epic_id or "null"}, **Feature Description:** ${result.feature_description or "null"}, **Next Session ID:** ${result.next_session_id}, **Next Story ID:** ${result.next_story_id or "null"}

Exit 1 → "Epic not found: ${ARGUMENTS}" → HALT
Exit 2 → AskUserQuestion: SINGLE_STORY vs EPIC_BATCH
```

```
Skill(command="spec-driven-stories")
```

Skill handles ALL workflow — parsing, selection, creation, validation, linking.

## References

- Skill: `.claude/skills/spec-driven-stories/SKILL.md`
- FROM_RECOMMENDATIONS workflow: `.claude/skills/spec-driven-stories/references/story-discovery-from-recommendations.md`
