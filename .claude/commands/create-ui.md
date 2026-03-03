---
description: Generate UI component specifications and code
argument-hint: [STORY-ID or component-description]
model: opus
allowed-tools: Read, Glob, Skill, AskUserQuestion
---

# /create-ui - Generate UI Component Specifications

Generate UI specs and code with framework-specific patterns, styling, and documentation.

## Lean Orchestration Enforcement

**DO NOT (before skill invocation):**
- ❌ DO NOT validate or read context files (skill Phase 1 handles this)
- ❌ DO NOT extract frontend stack from tech-stack.md (skill handles extraction)
- ❌ DO NOT verify output files or component structure (skill Phase 7 validates)
- ❌ DO NOT invoke feedback hooks (skill handles hook integration)
- ❌ DO NOT check for placeholders in generated specs (skill Phase 7 validates)

**DO (command responsibilities only):**
- ✅ Validate argument (story ID or component description)
- ✅ Set context markers (Mode, Story ID or Component Description)
- ✅ Invoke skill immediately after validation

## Phase 0: Argument Validation

```
IF ARG matches "STORY-[0-9]+":
  MODE="story"; STORY_ID=ARG
  Glob(pattern="devforgeai/specs/Stories/${STORY_ID}*.story.md")
  IF not found:
    AskUserQuestion:
      Question: "Story ${STORY_ID} not found. What should I do?"
      Header: "Story not found"
      Options: ["List all available stories","Use standalone mode","Cancel command"]
      multiSelect: false
ELIF ARG empty:
  AskUserQuestion:
    Question: "No argument provided. What UI should I generate?"
    Header: "UI Generation"
    Options: ["List stories with UI requirements","Standalone component (I'll describe it)","Show /create-ui syntax"]
    multiSelect: false
  # AskUserQuestion for placeholder resolution handled by skill Phase 7
  # AskUserQuestion for constraint violation overrides handled by skill Phase 7
  # AskUserQuestion for component type selection handled by skill Phase 3
  # AskUserQuestion for styling preferences handled by skill Phase 3
  # AskUserQuestion for accessibility level handled by skill Phase 3
  # AskUserQuestion for responsive breakpoints handled by skill Phase 3
ELSE:
  MODE="standalone"; COMPONENT_DESCRIPTION=ARG

**Mode:** ${MODE} | **Target:** ${STORY_ID or COMPONENT_DESCRIPTION}
```

## Phase 1: Invoke Skill

```
Skill(command="devforgeai-ui-generator")
```

Skill handles: context validation, tech-stack extraction, discovery (5-15 questions), templates, code gen, docs, validation, hooks.

## Phase 2: Display Results

Output `result.display.template` and `result.next_steps` as-is.

## Error Handling

| Error | Display | Recovery |
|-------|---------|----------|
| Story Not Found | `❌ Story Not Found: ${ID}` | `/create-story` or standalone mode |
| Context Missing | `❌ Context Files Required` (lists 6 files) | `/create-context` |
| No Frontend Stack | `❌ Frontend Stack Not Defined` | Update tech-stack.md |
| Skill Failed | `❌ UI Generator Failed` + debug info | Check SKILL.md, tech-stack.md |
| Validation Failed | `⚠️ Spec Issues` + missing/placeholder/violations | Resolve via prompts |

## Success Criteria

UI spec generated, components created per source-tree.md, no placeholders, constraints validated.

## Integration

**Invokes:** devforgeai-ui-generator skill
**Prerequisites:** 6 context files, frontend stack in tech-stack.md
**Related:** `/create-story`, `/create-context`, `/dev`, `/qa`
**Budget:** ~24K tokens total
