# Phase 03: Feedback Execution

## Entry Gate

```bash
devforgeai-validate phase-check ${SESSION_ID} --workflow=feedback --from=02 --to=03 --project-root=.
```

| Exit Code | Action |
|-----------|--------|
| 0 | Prerequisites met. Proceed. |
| 1 | Phase 02 incomplete. HALT. |
| 2 | Validation error. HALT. |
| 127 | CLI not installed. Proceed without enforcement. |

---

## Contract

- **PURPOSE:** Execute the feedback type workflow resolved in Phase 01 and prepared in Phase 02
- **REQUIRED SUBAGENTS:** framework-analyst (ai_analysis type ONLY)
- **REQUIRED ARTIFACTS:** Feedback data captured — questions answered, summary generated, metrics collected, analysis produced, triage processed, or operation result
- **STEP COUNT:** 3-6 (varies by feedback type)
- **REFERENCE FILES:** Already loaded in Phase 02 (type-specific references). No additional loading needed.

---

## Reference Loading

References for this phase were loaded in Phase 02 (Step 2.2). Do NOT reload them.

However, if context window is approaching limits, reload the type-specific reference:

```
IF estimated context > 80%:
  Reload the primary reference for $FEEDBACK_TYPE from the Phase 02 table
```

---

## Dispatch

Execute ONE of the following sub-workflows based on `$FEEDBACK_TYPE`:

```
SWITCH $FEEDBACK_TYPE:
  CASE "conversation":  GOTO Sub-Workflow: Conversation
  CASE "summary":       GOTO Sub-Workflow: Summary
  CASE "metrics":       GOTO Sub-Workflow: Metrics
  CASE "checklist":     GOTO Sub-Workflow: Checklist
  CASE "ai_analysis":   GOTO Sub-Workflow: AI Analysis
  CASE "triage":        GOTO Sub-Workflow: Triage
  CASE "config":        GOTO Sub-Workflow: Config
  CASE "search":        GOTO Sub-Workflow: Search
  CASE "export":        GOTO Sub-Workflow: Export
  CASE "import":        GOTO Sub-Workflow: Import
```

---

## Sub-Workflow: Conversation (5 Steps)

### Step 3.1C: Select Questions

**EXECUTE:**
```
Use adaptive questioning algorithm (from adaptive-questioning.md):

1. Determine question category based on operation status and duration:
   | Status  | Duration  | Category                    |
   |---------|-----------|----------------------------|
   | success | < 10 min  | success_standard (3-4 Qs)  |
   | success | >= 10 min | success_long_running (3-4)  |
   | failure | any       | failure_focused (5-6 Qs)    |
   | partial | any       | partial_mixed (3-4 Qs)      |
   | unknown | any       | generic_fallback (4 Qs)     |

2. Select questions from feedback-question-templates.md for the matching category
3. Apply variable substitution:
   - {operation_type} -> dev, qa, release
   - {duration} -> formatted ("45 minutes", "about an hour")
   - {story_id} -> STORY-042
   - {error_message} -> from context
   - {failed_todo} -> which task failed
   - {longest_phase} -> phase with max duration

4. Result: 3-7 context-aware questions
```

**VERIFY:** `selected_questions.length >= 3 AND selected_questions.length <= 7`
```
IF selected_questions.length < 3: Use generic_fallback questions (minimum 3)
IF selected_questions.length > 7: Trim to 7 (keep highest priority)
```

**RECORD:**
```bash
devforgeai-validate phase-record ${SESSION_ID} --workflow=feedback --phase=03 --step=3.1C --project-root=.
```
Update checkpoint: `phases["03"].steps_completed.append("3.1C")`
Update checkpoint: `phases["03"].questions_selected = selected_questions.length`

---

### Step 3.2C: Present Questions

**EXECUTE:**
```
AskUserQuestion:
  questions: [
    For each selected question, create an AskUserQuestion entry:
    {
      question: "{substituted question text}",
      header: "Feedback",
      options: [
        // Options vary by question type:
        // For rating questions: label: "1-5 scale options"
        // For open questions: user provides free text via "Other"
        // For multiple-choice: predefined options from template
      ],
      multiSelect: false  // unless checklist-style
    }
  ]
```

Note: AskUserQuestion supports 1-4 questions per call. If more than 4 selected, split into multiple calls.

**VERIFY:** User responded to at least 1 question (response is non-null and non-empty).
```
IF all responses are null or empty: HALT -- "No feedback responses received"
```

**RECORD:**
```bash
devforgeai-validate phase-record ${SESSION_ID} --workflow=feedback --phase=03 --step=3.2C --project-root=.
```
Update checkpoint: `phases["03"].steps_completed.append("3.2C")`
Update checkpoint: `phases["03"].questions_asked = total_questions_presented`

---

### Step 3.3C: Capture Responses

**EXECUTE:**
```
For each question-response pair:
  Store response text
  Map to template field using field-mapping-guide.md:
    response -> template_section (e.g., "what-went-well", "suggestions")
  Track: questions_answered vs questions_skipped
```

**VERIFY:** At least 1 non-empty response captured.
```
IF questions_answered == 0: HALT -- "All questions were skipped"
```

**RECORD:**
```bash
devforgeai-validate phase-record ${SESSION_ID} --workflow=feedback --phase=03 --step=3.3C --project-root=.
```
Update checkpoint:
```
phases["03"].questions_answered = questions_answered
phases["03"].questions_skipped = questions_skipped
phases["03"].steps_completed.append("3.3C")
```

---

### Step 3.4C: Validate Response Mappings

**EXECUTE:**
```
For each response, verify it maps to a template section:
  response.field_name -> template.field-mappings[field_name]
  IF no mapping exists: assign to "additional-feedback" section
```

**VERIFY:** All responses have valid template section mappings.

**RECORD:**
```bash
devforgeai-validate phase-record ${SESSION_ID} --workflow=feedback --phase=03 --step=3.4C --project-root=.
```
Update checkpoint: `phases["03"].steps_completed.append("3.4C")`

---

### Step 3.5C: Structure Feedback Document

**EXECUTE:**
```
Build feedback document with YAML frontmatter:

---
session-id: ${SESSION_ID}
operation: ${OPERATION_CONTEXT.operation_type}
operation-type: command|skill|subagent
status: ${OPERATION_CONTEXT.status}
story-id: ${OPERATION_CONTEXT.story_id}
timestamp: ${current ISO 8601}
duration-ms: ${OPERATION_CONTEXT.duration_seconds * 1000}
template-used: ${template_file}
version: 1.0
---

## {Template Section 1}
{Response for section 1}

## {Template Section 2}
{Response for section 2}

...

## Performance Metrics
- Questions asked: ${questions_asked}
- Questions answered: ${questions_answered}
- Questions skipped: ${questions_skipped}

## Additional Feedback
{Any unmapped responses}
```

**VERIFY:** Document contains YAML frontmatter with `session-id` field AND at least 1 content section.
```
IF document does NOT contain "session-id:": HALT -- "Feedback document structure invalid"
```

**RECORD:**
```bash
devforgeai-validate phase-record ${SESSION_ID} --workflow=feedback --phase=03 --step=3.5C --project-root=.
```
Update checkpoint:
```
phases["03"].feedback_data_captured = true
phases["03"].sub_workflow = "conversation"
phases["03"].steps_completed.append("3.5C")
```

---

## Sub-Workflow: Summary (3 Steps)

### Step 3.1S: Generate Summary

**EXECUTE:**
```
Generate markdown summary from $OPERATION_CONTEXT:

# Feedback Summary: ${OPERATION_CONTEXT.operation_type} - ${OPERATION_CONTEXT.story_id}

## Operation Details
- **Type:** ${operation_type}
- **Story:** ${story_id}
- **Status:** ${status}
- **Duration:** ${formatted_duration}
- **Timestamp:** ${current ISO 8601}

## Results
- **Tests Passed:** ${test_results or "N/A"}
- **Coverage:** ${coverage or "N/A"}
- **Phases Completed:** ${phases_completed.join(", ") or "N/A"}

## Deferrals
${list deferrals or "None"}

## Next Steps
${derived next steps based on operation outcome}
```

**VERIFY:** Summary contains all required sections: Operation Details, Results, Deferrals, Next Steps.

**RECORD:**
```bash
devforgeai-validate phase-record ${SESSION_ID} --workflow=feedback --phase=03 --step=3.1S --project-root=.
```
Update checkpoint: `phases["03"].steps_completed.append("3.1S")`

---

### Step 3.2S: Validate Summary Sections

**EXECUTE:**
```
Check that each required section has content (not just headers):
  - "## Operation Details" has at least Type and Status filled
  - "## Results" has at least one data point
  - "## Next Steps" has at least one action item
```

**VERIFY:** All required sections have non-empty content.

**RECORD:**
```bash
devforgeai-validate phase-record ${SESSION_ID} --workflow=feedback --phase=03 --step=3.2S --project-root=.
```
Update checkpoint: `phases["03"].steps_completed.append("3.2S")`

---

### Step 3.3S: Format Per Template

**EXECUTE:**
```
Apply template formatting from template-format-specification.md.
Add YAML frontmatter with session metadata.
```

**VERIFY:** Document has valid YAML frontmatter.

**RECORD:**
```bash
devforgeai-validate phase-record ${SESSION_ID} --workflow=feedback --phase=03 --step=3.3S --project-root=.
```
Update checkpoint:
```
phases["03"].feedback_data_captured = true
phases["03"].sub_workflow = "summary"
phases["03"].steps_completed.append("3.3S")
```

---

## Sub-Workflow: Metrics (3 Steps)

### Step 3.1M: Collect Metric Values

**EXECUTE:**
```
Collect from $OPERATION_CONTEXT:
  execution_time_ms: duration in milliseconds
  token_usage: estimated token count
  test_pass_rate: percentage (0-100)
  coverage_percentage: if available
  phases_completed: count
  subagents_invoked: count
  errors_encountered: count
```

**VERIFY:** At least `execution_time_ms` has a numeric value.

**RECORD:**
```bash
devforgeai-validate phase-record ${SESSION_ID} --workflow=feedback --phase=03 --step=3.1M --project-root=.
```
Update checkpoint: `phases["03"].steps_completed.append("3.1M")`

---

### Step 3.2M: Structure as JSON

**EXECUTE:**
```
metrics_json = {
  "session_id": SESSION_ID,
  "timestamp": current ISO 8601,
  "operation_type": $OPERATION_CONTEXT.operation_type,
  "story_id": $OPERATION_CONTEXT.story_id,
  "metrics": {
    "execution_time_ms": value,
    "token_usage": value,
    "test_pass_rate": value,
    "coverage_percentage": value,
    "phases_completed": value,
    "subagents_invoked": value,
    "errors_encountered": value
  }
}
```

**VERIFY:** JSON is valid and `metrics` object has at least 1 non-null field.

**RECORD:**
```bash
devforgeai-validate phase-record ${SESSION_ID} --workflow=feedback --phase=03 --step=3.2M --project-root=.
```
Update checkpoint: `phases["03"].steps_completed.append("3.2M")`

---

### Step 3.3M: Validate Schema

**EXECUTE:**
```
Validate metrics_json against expected schema:
  - session_id: string (FB-YYYY-MM-DD-NNN)
  - timestamp: valid ISO 8601
  - metrics.*: numeric or null
```

**VERIFY:** Schema validation passes.

**RECORD:**
```bash
devforgeai-validate phase-record ${SESSION_ID} --workflow=feedback --phase=03 --step=3.3M --project-root=.
```
Update checkpoint:
```
phases["03"].feedback_data_captured = true
phases["03"].sub_workflow = "metrics"
phases["03"].steps_completed.append("3.3M")
```

---

## Sub-Workflow: Checklist (4 Steps)

### Step 3.1K: Present Checklist

**EXECUTE:**
```
Build checklist from feedback-question-templates.md (sprint retrospective section):

AskUserQuestion:
  questions: [{
    question: "Select items that apply to this sprint:",
    header: "Retrospective",
    options: [
      { label: "Stories completed on time", description: "All planned stories delivered within sprint" },
      { label: "Test coverage maintained", description: "Coverage thresholds met for all stories" },
      { label: "No critical bugs escaped", description: "No production incidents from sprint work" },
      { label: "Clear acceptance criteria", description: "ACs were unambiguous and testable" }
    ],
    multiSelect: true
  }]
```

**VERIFY:** User responded (even if no items selected — that is valid data).

**RECORD:**
```bash
devforgeai-validate phase-record ${SESSION_ID} --workflow=feedback --phase=03 --step=3.1K --project-root=.
```
Update checkpoint: `phases["03"].steps_completed.append("3.1K")`

---

### Step 3.2K: Capture Checked Items

**EXECUTE:**
```
Parse AskUserQuestion response:
  checked_items = list of selected labels
  unchecked_items = list of unselected labels
```

**VERIFY:** Response parsed successfully (checked_items is a list, even if empty).

**RECORD:**
```bash
devforgeai-validate phase-record ${SESSION_ID} --workflow=feedback --phase=03 --step=3.2K --project-root=.
```
Update checkpoint: `phases["03"].steps_completed.append("3.2K")`

---

### Step 3.3K: Calculate Completion Percentage

**EXECUTE:**
```
completion_percentage = (checked_items.length / total_items.length) * 100
```

**VERIFY:** `completion_percentage` is between 0 and 100.

**RECORD:**
```bash
devforgeai-validate phase-record ${SESSION_ID} --workflow=feedback --phase=03 --step=3.3K --project-root=.
```
Update checkpoint: `phases["03"].steps_completed.append("3.3K")`

---

### Step 3.4K: Structure Results

**EXECUTE:**
```
Build checklist feedback document:

---
session-id: ${SESSION_ID}
operation: sprint-retrospective
status: completed
timestamp: ${current ISO 8601}
template-used: checklist
completion-percentage: ${completion_percentage}
version: 1.0
---

## Sprint Retrospective Checklist

### Completed
${for each checked item: "- [x] {item}"}

### Not Completed
${for each unchecked item: "- [ ] {item}"}

### Completion Rate
${completion_percentage}% (${checked_items.length}/${total_items.length})

### Notes
${any additional text from user}
```

**VERIFY:** Document has YAML frontmatter and at least 1 checklist section.

**RECORD:**
```bash
devforgeai-validate phase-record ${SESSION_ID} --workflow=feedback --phase=03 --step=3.4K --project-root=.
```
Update checkpoint:
```
phases["03"].feedback_data_captured = true
phases["03"].sub_workflow = "checklist"
phases["03"].steps_completed.append("3.4K")
```

---

## Sub-Workflow: AI Analysis (6 Steps)

### Step 3.1A: Read Workflow Context

**EXECUTE:**
```
# Read the story file for the completed operation
IF $OPERATION_CONTEXT.story_id is not null:
  story_path_results = Glob(pattern="devforgeai/specs/Stories/${OPERATION_CONTEXT.story_id}*.story.md")
  IF found:
    Read(file_path=story_path_results[0])
    Extract: acceptance criteria, implementation notes, deferrals, errors

# Read phase state for the completed operation
IF $OPERATION_CONTEXT.story_id is not null:
  phase_state_results = Glob(pattern="devforgeai/workflows/${OPERATION_CONTEXT.story_id}-phase-state.json")
  IF found:
    Read(file_path=phase_state_results[0])
    Extract: phase durations, subagent invocations, error counts
```

**VERIFY:** At least one source of workflow context loaded (story file or phase state).

**RECORD:**
```bash
devforgeai-validate phase-record ${SESSION_ID} --workflow=feedback --phase=03 --step=3.1A --project-root=.
```
Update checkpoint: `phases["03"].steps_completed.append("3.1A")`

---

### Step 3.2A: Invoke Framework Analyst Subagent

**EXECUTE:**
```
Task(
  subagent_type="framework-analyst",
  prompt="Analyze the following DevForgeAI workflow execution and generate improvement recommendations.

    Story: ${OPERATION_CONTEXT.story_id}
    Operation: ${OPERATION_CONTEXT.operation_type}
    Status: ${OPERATION_CONTEXT.status}
    Duration: ${OPERATION_CONTEXT.duration_seconds} seconds

    Story Context:
    ${story_content_excerpt}

    Phase Execution:
    ${phase_state_excerpt}

    Generate structured analysis following this schema:
    - what_worked_well: observations with evidence and impact
    - areas_for_improvement: issues with evidence and root cause
    - recommendations: title, description, affected_files, effort_estimate, priority, feasible_in_claude_code
    - patterns_observed: recurring patterns
    - anti_patterns_detected: violations found

    Requirements:
    - No aspirational language (reject 'could', 'might', 'consider')
    - Evidence required for ALL observations
    - Effort estimates for ALL recommendations
    - Feasibility check: MUST be implementable in Claude Code Terminal
    - Return valid JSON matching the AI Analysis Output Schema"
)
```

**VERIFY:** Subagent returned non-empty result containing "recommendations" key.
```
IF result is empty: HALT -- "Framework analyst subagent returned no result"
IF result does NOT contain "recommendations": HALT -- "Analysis output missing recommendations"
```

**RECORD:**
```bash
devforgeai-validate phase-record ${SESSION_ID} --workflow=feedback --phase=03 --step=3.2A --project-root=.
```
Update checkpoint:
```
phases["03"].subagent_invoked = true
phases["03"].steps_completed.append("3.2A")
```

---

### Step 3.3A: Validate Output

**EXECUTE:**
```
Validate the analysis JSON:
  1. Schema check: all required fields present (what_worked_well, areas_for_improvement, recommendations)
  2. Aspirational language check: scan for "could", "might", "consider", "perhaps", "possibly"
     IF found: remove offending recommendations or rewrite to imperative
  3. Evidence check: every observation has non-empty "evidence" field
     IF missing: flag as incomplete
  4. Effort estimate check: every recommendation has valid effort_estimate
     IF missing: default to "1 hour"
  5. Feasibility check: every recommendation has feasible_in_claude_code boolean
     IF missing: default to true
```

**VERIFY:** Validation passes — no aspirational language, all evidence present, all estimates provided.

**RECORD:**
```bash
devforgeai-validate phase-record ${SESSION_ID} --workflow=feedback --phase=03 --step=3.3A --project-root=.
```
Update checkpoint: `phases["03"].steps_completed.append("3.3A")`

---

### Step 3.4A: Apply Merit Filter

**EXECUTE:**
```
For each recommendation:
  1. Duplicate check: search existing recommendations in devforgeai/feedback/ai-analysis/
     Glob(pattern="devforgeai/feedback/ai-analysis/**/*-ai-analysis.json")
     For each existing analysis, check if recommendation.title is similar
     IF duplicate found: mark recommendation.status = "duplicate", skip

  2. Already-implemented check: search codebase for recommendation.affected_files
     For each affected file, check if the suggested change already exists
     IF already implemented: mark recommendation.status = "already_implemented", skip

  3. Keep only recommendations with status != "duplicate" and status != "already_implemented"
```

**VERIFY:** Merit filter applied — at least 0 recommendations remain (it is valid to have 0 after filtering).

**RECORD:**
```bash
devforgeai-validate phase-record ${SESSION_ID} --workflow=feedback --phase=03 --step=3.4A --project-root=.
```
Update checkpoint: `phases["03"].steps_completed.append("3.4A")`

---

### Step 3.5A: Update Recommendations Queue (if HIGH priority)

**EXECUTE:**
```
high_priority_recs = [r for r in recommendations if r.priority == "HIGH"]

IF high_priority_recs.length > 0:
  queue_path = "devforgeai/feedback/ai-analysis/aggregated/recommendations-queue.json"
  queue_exists = Glob(pattern=queue_path)

  IF queue_exists:
    Read(file_path=queue_path)
    Append high_priority_recs to queue.HIGH array
    Write(file_path=queue_path, content=updated_queue)
  ELSE:
    Create new queue with HIGH array containing high_priority_recs
    Write(file_path=queue_path, content=new_queue)
```

**VERIFY:**
```
IF high_priority_recs.length > 0:
  Grep(pattern=high_priority_recs[0].title, path=queue_path)
  IF not found: HALT -- "Recommendations queue not updated"
ELSE:
  # No HIGH priority recs — nothing to update, verification passes
```

**RECORD:**
```bash
devforgeai-validate phase-record ${SESSION_ID} --workflow=feedback --phase=03 --step=3.5A --project-root=.
```
Update checkpoint: `phases["03"].steps_completed.append("3.5A")`

---

### Step 3.6A: Structure Validated Analysis

**EXECUTE:**
```
Build final analysis JSON:
{
  "story_id": $OPERATION_CONTEXT.story_id,
  "timestamp": current ISO 8601,
  "session_id": SESSION_ID,
  "ai_analysis": {
    "what_worked_well": validated_observations,
    "areas_for_improvement": validated_issues,
    "recommendations": filtered_recommendations,
    "patterns_observed": patterns,
    "anti_patterns_detected": anti_patterns,
    "constraint_analysis": constraint_notes
  },
  "meta": {
    "total_recommendations": original_count,
    "filtered_recommendations": filtered_count,
    "duplicates_removed": duplicates_count,
    "already_implemented_removed": already_implemented_count,
    "high_priority_queued": high_priority_recs.length
  }
}
```

**VERIFY:** Final JSON has valid structure with "ai_analysis" key.

**RECORD:**
```bash
devforgeai-validate phase-record ${SESSION_ID} --workflow=feedback --phase=03 --step=3.6A --project-root=.
```
Update checkpoint:
```
phases["03"].feedback_data_captured = true
phases["03"].sub_workflow = "ai_analysis"
phases["03"].steps_completed.append("3.6A")
```

---

## Sub-Workflow: Triage (5 Steps)

### Step 3.1T: Read Recommendations Queue

**EXECUTE:**
```
queue_path = "devforgeai/feedback/ai-analysis/aggregated/recommendations-queue.json"
queue_exists = Glob(pattern=queue_path)

IF queue_exists:
  Read(file_path=queue_path)
  Parse queue JSON
ELSE:
  Display: "No recommendations queue found. Nothing to triage."
  Mark phase as complete with 0 items processed.
  GOTO Phase 04.
```

**VERIFY:** Queue loaded and parsed (or confirmed empty).

**RECORD:**
```bash
devforgeai-validate phase-record ${SESSION_ID} --workflow=feedback --phase=03 --step=3.1T --project-root=.
```
Update checkpoint: `phases["03"].steps_completed.append("3.1T")`

---

### Step 3.2T: Display Grouped by Priority

**EXECUTE:**
```
Display recommendations grouped by priority:

## HIGH Priority
| # | Title | Effort | Affected Files |
|---|-------|--------|----------------|
${for each HIGH rec: "| {i} | {title} | {effort} | {files} |"}

## MEDIUM Priority
${same format}

## LOW Priority
${same format}

Apply $PRIORITY_FILTER if set (only show matching priority level).
```

**VERIFY:** At least 1 recommendation displayed (or empty queue message shown).

**RECORD:**
```bash
devforgeai-validate phase-record ${SESSION_ID} --workflow=feedback --phase=03 --step=3.2T --project-root=.
```
Update checkpoint: `phases["03"].steps_completed.append("3.2T")`

---

### Step 3.3T: Process User Selections

**EXECUTE:**
```
IF $SELECTED_ITEMS is set (from command marker):
  Parse selected item IDs
ELSE:
  AskUserQuestion:
    question: "Which recommendations should be converted to stories?"
    header: "Triage"
    options: [top 4 recommendations by priority]
    multiSelect: true

selected_recommendations = match selections to queue items
```

**VERIFY:** Selections parsed (even if empty — user may choose none).

**RECORD:**
```bash
devforgeai-validate phase-record ${SESSION_ID} --workflow=feedback --phase=03 --step=3.3T --project-root=.
```
Update checkpoint: `phases["03"].steps_completed.append("3.3T")`

---

### Step 3.4T: Create Stories from Selections

**EXECUTE:**
```
FOR each selected_recommendation:
  Skill(command="devforgeai-story-creation", args={
    title: recommendation.title,
    description: recommendation.description,
    affected_files: recommendation.affected_files,
    source: "ai-recommendation",
    source_session: SESSION_ID
  })

  Track: story_id created for each recommendation
```

**VERIFY:** Stories created for all selected items (track count).
```
IF selected_recommendations.length > 0 AND stories_created.length == 0:
  HALT -- "Story creation failed for all selected recommendations"
```

**RECORD:**
```bash
devforgeai-validate phase-record ${SESSION_ID} --workflow=feedback --phase=03 --step=3.4T --project-root=.
```
Update checkpoint:
```
phases["03"].stories_created = stories_created.length
output.stories_created = story_ids
phases["03"].steps_completed.append("3.4T")
```

---

### Step 3.5T: Update Queue

**EXECUTE:**
```
For each successfully triaged recommendation:
  Move from priority bucket (HIGH/MEDIUM/LOW) to "implemented" array
  Add: implementation_date, story_id, session_id

Write(file_path=queue_path, content=updated_queue)
```

**VERIFY:**
```
Read(file_path=queue_path)
Grep for each triaged recommendation title in "implemented" array
IF not found: HALT -- "Queue update failed"
```

**RECORD:**
```bash
devforgeai-validate phase-record ${SESSION_ID} --workflow=feedback --phase=03 --step=3.5T --project-root=.
```
Update checkpoint:
```
phases["03"].feedback_data_captured = true
phases["03"].sub_workflow = "triage"
phases["03"].steps_completed.append("3.5T")
output.recommendations_triaged = triaged_count
```

---

## Sub-Workflow: Config (3 Steps)

### Step 3.1CFG: Execute Config Subcommand

**EXECUTE:**
```
config_path = "devforgeai/feedback/config.yaml"

SWITCH $SUBCOMMAND:
  CASE "view":
    config_exists = Glob(pattern=config_path)
    IF config_exists:
      Read(file_path=config_path)
      Display config contents in formatted table
    ELSE:
      Display: "No config file found. Using defaults."
      Display default values table

  CASE "edit":
    Read(file_path=config_path)
    AskUserQuestion for which setting to change
    Update config
    Write(file_path=config_path, content=updated_config)

  CASE "reset":
    Write default config to config_path
```

**VERIFY:** Config operation completed (view displayed, edit written, reset written).

**RECORD:**
```bash
devforgeai-validate phase-record ${SESSION_ID} --workflow=feedback --phase=03 --step=3.1CFG --project-root=.
```
Update checkpoint: `phases["03"].steps_completed.append("3.1CFG")`

---

### Step 3.2CFG-3.3CFG: Validate and Confirm

**EXECUTE:** Verify config file is valid YAML after edit/reset. Display confirmation.

**VERIFY:** Config file exists and is parseable.

**RECORD:** Update checkpoint:
```
phases["03"].feedback_data_captured = true
phases["03"].sub_workflow = "config"
```

---

## Sub-Workflow: Search (3 Steps)

### Step 3.1SRCH: Execute Search

**EXECUTE:**
```
Read(file_path="devforgeai/feedback/index.json")
Parse index JSON

Apply filters:
  IF $SEARCH_QUERY: text match against keywords, story-id, operation fields
  IF $SEVERITY: filter by severity field
  IF $STATUS: filter by status field

Sort results:
  Date range queries: descending by date
  Text queries: by relevance
  Story ID queries: descending by date

Apply pagination: skip ($PAGE - 1) * $LIMIT, take $LIMIT
```

**VERIFY:** Search executed (results may be empty — that is valid).

**RECORD:**
```bash
devforgeai-validate phase-record ${SESSION_ID} --workflow=feedback --phase=03 --step=3.1SRCH --project-root=.
```
Update checkpoint: `phases["03"].steps_completed.append("3.1SRCH")`

---

### Step 3.2SRCH-3.3SRCH: Format and Display Results

**EXECUTE:** Format results as table with pagination info. Display to user.

**VERIFY:** Results displayed (or "No results found" message shown).

**RECORD:** Update checkpoint:
```
phases["03"].feedback_data_captured = true
phases["03"].sub_workflow = "search"
```

---

## Sub-Workflow: Export (3 Steps)

### Step 3.1EXP: Prepare Export

**EXECUTE:**
```
Read(file_path="devforgeai/feedback/index.json")
Apply date range and story ID filters
Collect matching feedback files via Glob

SWITCH $FORMAT:
  CASE "json": Structure as JSON array
  CASE "csv": Convert to CSV rows
  CASE "markdown": Generate markdown report

IF $SANITIZE == true:
  Apply sanitization patterns from context-sanitization.md
```

**VERIFY:** Export data prepared with at least 1 entry (or empty with message).

**RECORD:**
```bash
devforgeai-validate phase-record ${SESSION_ID} --workflow=feedback --phase=03 --step=3.1EXP --project-root=.
```
Update checkpoint: `phases["03"].steps_completed.append("3.1EXP")`

---

### Step 3.2EXP-3.3EXP: Write Export File and Confirm

**EXECUTE:** Write export file to output path. Display confirmation with file location.

**VERIFY:** Export file exists on disk (Glob).

**RECORD:** Update checkpoint:
```
phases["03"].feedback_data_captured = true
phases["03"].sub_workflow = "export"
```

---

## Sub-Workflow: Import (3 Steps)

### Step 3.1IMP: Validate and Import Archive

**EXECUTE:**
```
Validate $ARCHIVE_PATH exists (Glob)
Read manifest from archive
Check framework version compatibility
For each feedback entry:
  Check for duplicates (compare session IDs)
  IF duplicate: auto-generate unique ID (append "-imported-N")
  Import entry to devforgeai/feedback/
Update index.json with imported entries
```

**VERIFY:** Import completed. At least 1 entry imported (or 0 with conflict report).

**RECORD:**
```bash
devforgeai-validate phase-record ${SESSION_ID} --workflow=feedback --phase=03 --step=3.1IMP --project-root=.
```

---

### Step 3.2IMP-3.3IMP: Update Index and Confirm

**EXECUTE:** Update feedback index. Display import summary.

**VERIFY:** Index updated with imported entries.

**RECORD:** Update checkpoint:
```
phases["03"].feedback_data_captured = true
phases["03"].sub_workflow = "import"
```

---

## Phase Completion (All Sub-Workflows)

After any sub-workflow completes, update checkpoint:
```
checkpoint.phases["03"].status = "completed"
checkpoint.progress.current_phase = 4
checkpoint.progress.phases_completed.append("03")
```
Write updated checkpoint to disk.

---

## Exit Gate

```bash
devforgeai-validate phase-complete ${SESSION_ID} --workflow=feedback --phase=03 --checkpoint-passed --project-root=.
```

---

## Exit Verification Checklist

Before proceeding to Phase 04, verify ALL:

- [ ] One sub-workflow executed completely
- [ ] `feedback_data_captured` == true in checkpoint
- [ ] Sub-workflow type recorded in checkpoint
- [ ] All sub-workflow steps completed (steps_completed array)
- [ ] Checkpoint updated with phase 03 completion
- [ ] Checkpoint written to disk (verified via Glob)

**IF any criterion is unmet: HALT. Do NOT proceed to Phase 04.**

---

## Phase Transition Display

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  Phase 03: Feedback Execution ✓
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  Sub-Workflow: ${sub_workflow}
  Data Captured: Yes
  Questions: ${questions_answered || 'N/A'}
  Stories Created: ${stories_created || 'N/A'}
  Steps: ${steps_completed.length}/${expected_steps}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```
