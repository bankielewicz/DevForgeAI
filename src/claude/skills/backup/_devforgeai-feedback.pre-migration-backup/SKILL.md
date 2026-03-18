---
name: devforgeai-feedback
description: >
  DEPRECATED - Use spec-driven-feedback instead. This skill has been replaced by
  spec-driven-feedback which provides structural anti-skip enforcement (Execute-Verify-Gate
  pattern) to prevent token optimization bias. Reference files in this directory are still
  used by spec-driven-feedback via shared reads. Do NOT invoke this skill directly.
version: 2.0
model: claude-opus-4-6
---

# DevForgeAI Feedback Skill

Capture retrospective feedback from development workflows to improve processes, identify patterns, and enable continuous improvement.

---

## Feedback Types

| Type | When Used | What Happens | Reference |
|------|-----------|--------------|-----------|
| **conversation** | After /dev, /qa, /release | Present context-aware questions via AskUserQuestion, persist responses | `references/adaptive-questioning.md` |
| **summary** | After any operation | Auto-generate markdown summary of results | `references/feedback-persistence-guide.md` |
| **metrics** | After any operation | Collect quantitative data (time, tokens, coverage) | `references/feedback-export-formats.md` |
| **checklist** | Sprint retrospectives | Interactive checklist via AskUserQuestion | `references/feedback-question-templates.md` |
| **ai_analysis** | After /dev, /qa (via hooks) | AI-generated framework improvement recommendations | `references/context-extraction.md` |
| **triage** | Manual via /recommendations-triage | Process recommendation queue, create stories | `references/triage-workflow.md` |

---

## Workflow

### Phase 1: Detect Context

1. Check for context markers set by invoking command:
   - `**Feedback Mode:**` — conversation, summary, metrics, checklist, ai_analysis, triage
   - `**Feedback Context:**` — story ID, operation details
   - `**Feedback Source:**` — manual, hook, auto
   - `**Search Query:**`, `**Severity:**`, `**Status:**` — for search operations
   - `**Priority Filter:**`, `**Selected Items:**` — for triage operations
2. If no markers, extract context from conversation history (operation type, story ID, outcome)
3. Load operation context using the context-extraction pattern:
   - Read `references/context-extraction.md` for the OperationContext data model
   - Extract from TaskList state (task content, status, timing)
   - Determine operation status (success/failure/partial)
   - Apply sanitization per `references/context-sanitization.md`

### Phase 2: Execute Feedback Type

**conversation:**
1. Select questions using adaptive questioning (`references/adaptive-questioning.md`)
2. Present 3-7 questions via AskUserQuestion (context-aware, natural language)
3. Capture responses

**summary:**
1. Generate markdown summary from operation context
2. Include: duration, test results, deferrals, phases completed, next steps

**metrics:**
1. Collect metric values: execution_time, token_usage, test_pass_rate
2. Structure as JSON

**checklist:**
1. Present checklist items via AskUserQuestion
2. Capture checked items, calculate completion percentage

**ai_analysis:**
1. Read workflow context (story file, phases, errors, deferrals)
2. Load analysis prompts from `references/feedback-question-templates.md`
3. Generate structured analysis (what_worked_well, areas_for_improvement, recommendations)
4. Validate: no aspirational language, evidence required, effort estimates, feasibility check
5. Apply merit filter (duplicate check, already-implemented check)
6. For detailed Phase 09 integration, see: `.claude/skills/spec-driven-dev/phases/phase-09-feedback.md`

**triage:**
1. Read `devforgeai/feedback/ai-analysis/aggregated/recommendations-queue.json`
2. Display recommendations grouped by priority
3. Process user selections -> invoke devforgeai-story-creation per item
4. Update queue (move to implemented)
5. For complete workflow, see: `references/triage-workflow.md`

### Phase 3: Persist & Index

1. Generate unique feedback ID: `FB-YYYY-MM-DD-###`
2. Write feedback file to `devforgeai/feedback/`:
   - Conversations: `{operation_id}-feedback.md`
   - Summaries: `{operation_id}-summary.md`
   - Checklists: `{operation_id}-checklist.md`
   - Metrics: `devforgeai/metrics/{metric_type}.json`
   - AI Analysis: `devforgeai/feedback/ai-analysis/{story_id}/{timestamp}-ai-analysis.json`
3. Update feedback index:
   ```
   Read(file_path="devforgeai/feedback/index.json")
   # Append new entry with id, timestamp, operation, story, feedback_file, tags
   Write(file_path="devforgeai/feedback/index.json", content=updated_index)
   ```
4. Append entry to `devforgeai/feedback/feedback-register.md`
5. Return confirmation with feedback ID and next steps

---

## Command Integration

These commands delegate to this skill. When invoked via a command, context markers are already set.

| Command | Purpose | Markers Set |
|---------|---------|-------------|
| `/feedback` (`DF:feedback`) | Manual feedback capture | Feedback Context, Feedback Source: manual |
| `/feedback-config` | View/edit/reset config | Subcommand: view, edit, reset |
| `/feedback-search` | Search feedback history | Search Query, Severity, Status, Limit, Page |
| `/feedback-reindex` | Rebuild index from all sources | (invokes CLI: `devforgeai-validate feedback-reindex`) |
| `/feedback-export-data` | Export filtered data (JSON/CSV/MD) | Format, Date Range, Story IDs, Severity, Status |
| `/export-feedback` | Export ZIP package with sanitization | Date Range, Sanitize, Output path |
| `/import-feedback` | Import ZIP package | Archive path |
| `/recommendations-triage` | Process recommendation queue | Feedback Mode: triage, Priority Filter, Selected Items |

---

## Hook Integration

This skill is auto-invoked by the event-driven hook system (STORY-018):

| Hook ID | Trigger | Feedback Type |
|---------|---------|---------------|
| `post-dev-feedback` | After /dev completes | conversation |
| `post-qa-retrospective` | After /qa completes | conversation |
| `post-release-monitoring` | After /release completes | conversation |
| `sprint-retrospective` | After sprint planning | checklist |
| `post-dev-ai-analysis` | After /dev completes | ai_analysis |
| `post-qa-ai-analysis` | After /qa completes | ai_analysis |

**Hook configuration:** `devforgeai/config/hooks.yaml`
**Feedback configuration:** `devforgeai/config/feedback.yaml`
**Hook system reference:** `HOOK-SYSTEM.md`

---

## AI Analysis Output Schema

```json
{
  "story_id": "STORY-XXX",
  "timestamp": "ISO8601",
  "ai_analysis": {
    "what_worked_well": [{"observation": "...", "evidence": "...", "impact": "..."}],
    "areas_for_improvement": [{"issue": "...", "evidence": "...", "root_cause": "..."}],
    "recommendations": [{
      "title": "...",
      "description": "...",
      "affected_files": ["..."],
      "implementation_code": "...",
      "effort_estimate": "15 min|30 min|1 hour|2 hours|4 hours",
      "priority": "HIGH|MEDIUM|LOW",
      "feasible_in_claude_code": true
    }],
    "patterns_observed": ["..."],
    "anti_patterns_detected": ["..."],
    "constraint_analysis": "..."
  }
}
```

**Constraint:** All recommendations MUST be implementable within Claude Code Terminal. If a recommendation requires tools beyond Read, Write, Edit, Glob, Grep, Bash, TaskCreate, TaskUpdate, AskUserQuestion — flag it as `feasible_in_claude_code: false`.

---

## Reference Files

Load these as needed — do not load all at once.

| Reference | When to Load | Content |
|-----------|-------------|---------|
| `references/context-extraction.md` | Phase 1 (context detection) | OperationContext data model, TaskList extraction, timing |
| `references/context-sanitization.md` | Phase 1 (before questions) | Secret/PII removal patterns |
| `references/adaptive-questioning.md` | Phase 2 (conversation type) | Question selection by outcome, variable substitution |
| `references/feedback-question-templates.md` | Phase 2 (any interactive type) | Question library by operation type |
| `references/feedback-persistence-guide.md` | Phase 3 (storage) | File formats, indexing patterns |
| `references/feedback-analysis-patterns.md` | After multiple sessions | Trend analysis, pattern detection |
| `references/feedback-export-formats.md` | Export operations | JSON, CSV, Markdown formats |
| `references/triage-workflow.md` | Triage mode | 6-phase triage workflow |
| `references/feedback-search-help.md` | Search operations | Query syntax, filter options |
| `references/field-mapping-guide.md` | Template customization | Field mappings between templates and output |
| `references/template-format-specification.md` | Template creation | Template YAML structure |
| `references/template-examples.md` | Template examples | Sample templates |
| `references/user-customization-guide.md` | User config | Customization options |

---

## Templates

Templates in `templates/` define question structure by operation type and outcome:

| Template | When Used |
|----------|-----------|
| `command-passed.yaml` | Command completed successfully |
| `command-failed.yaml` | Command failed |
| `skill-passed.yaml` | Skill completed successfully |
| `skill-failed.yaml` | Skill failed |
| `subagent-passed.yaml` | Subagent completed successfully |
| `subagent-failed.yaml` | Subagent failed |
| `generic.yaml` | Fallback for unknown operation types |

---

## Success Criteria

- [ ] Feedback type detected from context markers or conversation
- [ ] Appropriate questions/actions executed for feedback type
- [ ] Feedback persisted to filesystem with unique ID
- [ ] Index updated with new entry
- [ ] Confirmation returned to caller with feedback ID
- [ ] Token usage < 30K (isolated context)

---

## Configuration

**File:** `devforgeai/feedback/config.yaml`

| Setting | Default | Description |
|---------|---------|-------------|
| `retention_days` | 90 | Days to keep feedback (1-3650) |
| `auto_trigger_enabled` | true | Auto-trigger on operation completion |
| `export_format` | json | Default export format (json/csv/markdown) |
| `include_metadata` | true | Include metadata in exports |
| `search_enabled` | true | Enable search functionality |

---

## Related Documentation

- **Hook System:** `HOOK-SYSTEM.md` (complete technical reference)
- **Hook Config:** `devforgeai/config/hooks.yaml`
- **Feedback Config:** `devforgeai/feedback/config.yaml`
- **Phase 09 Integration:** `.claude/skills/spec-driven-dev/phases/phase-09-feedback.md`
- **Framework Analyst:** `.claude/agents/framework-analyst.md`
- **Feedback CLI:** `.claude/scripts/devforgeai_cli/feedback/`
