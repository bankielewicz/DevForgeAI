---
name: create-stories-from-rca
description: Create user stories from RCA recommendations
argument-hint: "RCA-NNN [--help]"
model: opus
allowed-tools: Read, Write, Edit, Glob, Grep, AskUserQuestion, Skill, TodoWrite
---

# /create-stories-from-rca - Create Stories from RCA Recommendations

Parse RCA documents, select recommendations interactively, and create stories in batch mode using devforgeai-story-creation Claude skill.

**Component Orchestration:** Parse (STORY-155) → Select (STORY-156) → Create (STORY-157) → Link (STORY-158)

**Reference:** `references/create-stories-from-rca/rca-stories-reference.md` for detailed docs.

---

## Usage

```bash
/create-stories-from-rca RCA-NNN [--threshold HOURS]
/create-stories-from-rca --help
```

---

## Argument Parsing

```
ARG = first argument from $ARGUMENTS

IF ARG == "--help" OR ARG == "help":
    Display abbreviated help:
    "Usage: /create-stories-from-rca RCA-NNN [--threshold HOURS]
     See: references/create-stories-from-rca/rca-stories-reference.md for full help"
    HALT

RCA_ID = extract from arguments matching "RCA-[0-9]+" (case-insensitive)

IF RCA_ID empty:
    Display: "❌ RCA ID required"
    Display: "Usage: /create-stories-from-rca RCA-NNN"
    Display: "Available RCAs:"
    FOR rca in Glob("devforgeai/RCA/*.md"):
        Display: "  • ${rca_id}"
    HALT

RCA_ID = uppercase(RCA_ID)  # rca-022 → RCA-022

IF Glob("devforgeai/RCA/${RCA_ID}*.md") not found:
    Display: "❌ RCA not found: ${RCA_ID}"
    Display: "Available RCAs:"
    FOR rca in Glob("devforgeai/RCA/*.md"):
        Display: "  • ${rca_id}"
    HALT
```

---

## Phase 1-5: RCA Parsing

IF RCA_ID ISNOT empty:
    Skill(command="devforgeai-story-creation", args="--RCA")

**See:** `references/create-stories-from-rca/parsing-workflow.md`

1. **Locate RCA File**: `Glob(pattern="devforgeai/RCA/${RCA_ID}*.md")`
2. **Parse Frontmatter**: Extract id, title, severity, status
3. **Extract Recommendations**: Parse `### REC-N:` sections
4. **Filter/Sort**: Apply effort threshold and priority sorting
5. **Display Results**: Show recommendations with effort estimates

---

## Phase 6-9: Interactive Selection

**See:** `references/create-stories-from-rca/selection-workflow.md`

```
AskUserQuestion(
    question: "Which recommendations to convert?",
    multiSelect: true,
    options: ["All recommendations", "REC-1: Title", "None - cancel"]
)
```

---

## Phase 10: Batch Story Creation

**See:** `references/create-stories-from-rca/batch-creation-workflow.md`

```
FOR recommendation in selected:
    batch_context = {
        story_id: get_next_story_id(),
        feature_name: recommendation.title,
        priority: map_priority(recommendation.priority),
        batch_mode: true,
        source_rca: RCA_ID,
        source_recommendation: recommendation.id
    }
    Skill(command="devforgeai-story-creation", args="--batch")
```

---

## Phase 11: RCA-Story Linking

**See:** `references/create-stories-from-rca/linking-workflow.md`

1. Update implementation checklist: `- [ ] REC-1` → `- [ ] REC-1: See STORY-NNN`
2. Add inline references: `**Implemented in:** STORY-NNN`
3. Update RCA status if all recommendations linked

---

## Error Handling

Validation errors, skill errors, and ID conflicts are handled with failure isolation (continue processing remaining items). See reference file for detailed error templates.

---

## Success Criteria

- [ ] RCA document parsed correctly
- [ ] Recommendations extracted and displayed
- [ ] User selection honored
- [ ] Stories created via devforgeai-story-creation skill
- [ ] RCA document updated with story links
- [ ] Failure isolation: individual failures don't block batch

---

## Integration

**Invoked by:** User via `/create-stories-from-rca RCA-NNN`
**Invokes:** `devforgeai-story-creation` skill (batch mode)
**Updates:** RCA document (story links), Story files (created)

**Reference Files:** `references/create-stories-from-rca/` directory contains:
- `parsing-workflow.md` - Phase 1-5 detailed workflow
- `selection-workflow.md` - Phase 6-9 detailed workflow
- `batch-creation-workflow.md` - Phase 10 detailed workflow
- `linking-workflow.md` - Phase 11 detailed workflow
- `rca-stories-reference.md` - Extended documentation

---

**Version:** 2.0 - Lean Orchestration | **Pattern:** Command delegates to skill
