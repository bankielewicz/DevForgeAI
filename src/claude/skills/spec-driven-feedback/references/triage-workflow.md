---
name: triage-workflow
description: Extracted recommendation triage business logic from recommendations-triage.md command
---

# Triage Workflow Reference

Business logic for the /recommendations-triage command, extracted per lean orchestration pattern (STORY-458).

---

## Phase 1: Read Queue

Parse queue JSON from: `devforgeai/feedback/ai-analysis/aggregated/recommendations-queue.json`

```
Read(file_path="devforgeai/feedback/ai-analysis/aggregated/recommendations-queue.json")
```

Extract recommendations by priority bucket (high, medium, low arrays).

Apply filters:
- If PRIORITY_FILTER set: Only include that priority bucket
- Apply LIMIT to total results (across all priorities)

---

## Phase 2: Display Recommendations

Present grouped by priority (HIGH first):

### HIGH Priority ({high_count} items)

| # | Title | Effort | Affected Files |
|---|-------|--------|----------------|

Details per item: Description, Files, Implementation, Source

### MEDIUM Priority ({medium_count} items)

(Same table format)

### LOW Priority ({low_count} items)

(Same table format)

---

## Phase 3: Selection Processing

After the command collects user selection via context markers:

1. Parse selected recommendation IDs from context markers
2. Validate each selected recommendation exists in queue
3. Return structured list for story creation

---

## Phase 4: Story Creation

For each selected recommendation:

1. Prepare story context markers:
   - Feature Description: Framework Enhancement: {title}
   - Implementation Approach: {implementation_code}
   - Affected Files: {files}
   - Source: framework-enhancement
   - Priority: {priority}

2. Invoke: `Skill(command="devforgeai-story-creation")`

3. Track: Record recommendation_id, story_id, timestamp, converted_by

---

## Phase 5: Queue Update

1. Read current queue JSON
2. For each converted recommendation:
   - Remove from priority bucket
   - Add to implemented array with conversion metadata and timestamp
3. Write updated queue JSON

---

## Phase 6: Completion Summary

Display:
- Stories Created count
- Recommendations Remaining count
- Created Stories table (Story ID, Title, Priority, Effort)
- Queue Status (remaining per priority)
- Next Steps: `/dev STORY-XXX`, `/recommendations-triage`, `/feedback-search`

---

## Error Handling

### Queue File Not Found

Error: recommendations-queue.json not found
Expected: devforgeai/feedback/ai-analysis/aggregated/recommendations-queue.json
Resolution: Run /dev on a story to generate recommendations, or create empty queue

### Story Creation Failed

Warning: Failed to create story for recommendation "{title}"
The recommendation remains in queue and can be retried.
Continuing with remaining selections...

### Queue Write Failed

Error: Cannot update recommendations-queue.json
Stories were created but queue not updated.
Manual fix: Edit queue JSON to move items to implemented array

---

## Data Flow Pipeline

1. /dev workflow Phase 09 invokes framework-analyst subagent
2. Subagent generates recommendations stored in queue
3. /recommendations-triage reads queue and user selects
4. Selected items sent to devforgeai-story-creation skill
5. Stories created with source: framework-enhancement tag
6. Queue updated (items moved from pending to implemented with timestamp)

---

## References

- `.claude/agents/framework-analyst.md` - Subagent that generates recommendations
- `.claude/skills/spec-driven-dev/phases/phase-09-feedback.md` - Where recommendations are captured
- `.claude/skills/spec-driven-dev/references/observation-capture.md` - Observation capture protocol
- `devforgeai/feedback/ai-analysis/aggregated/recommendations-queue.json` - Queue file
- `devforgeai/feedback/schema.json` - AI analysis schema
