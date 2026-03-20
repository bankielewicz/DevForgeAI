# Phase 06: Result Processing & Handoff

## Contract

| Attribute | Value |
|-----------|-------|
| **PURPOSE** | Format results for display, clean up checkpoint, and provide next steps |
| **REFERENCE** | `src/claude/skills/spec-driven-agents/references/create-agent-help.md` |
| **STEP COUNT** | 3 mandatory steps |

## Phase Exit Criteria

Before this phase can complete, ALL of the following MUST be true:

- [ ] Generation report displayed to user
- [ ] Next steps provided
- [ ] Checkpoint deleted (session complete)

---

## Reference Loading [MANDATORY]

```
Read(file_path="src/claude/skills/spec-driven-agents/references/create-agent-help.md")
```

IF Read fails: Display warning but continue -- help reference is supplementary, not blocking.

---

## Mandatory Steps

### Step 6.1: Format and Display Generation Report

EXECUTE:
```
# Read the generated agent file for line count
agent_path = checkpoint.generation.generated_files.subagent
Read(file_path=agent_path)
agent_line_count = count_lines(content)

# Read reference file for line count (if generated)
reference_line_count = 0
IF checkpoint.generation.generated_files.reference:
  reference_path = checkpoint.generation.generated_files.reference
  Read(file_path=reference_path)
  reference_line_count = count_lines(content)

# Format the report
Display:
"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  Agent Generation Report
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Session: ${checkpoint.session_id}
Agent: ${checkpoint.specification.name}
Domain: ${checkpoint.specification.domain}
Mode: ${checkpoint.parameters.creation_mode}

Generated Files:
  ✅ Subagent: ${agent_path} (${agent_line_count} lines)
  ${IF reference: '✅ Reference: ' + reference_path + ' (' + reference_line_count + ' lines)'}
  ${IF no reference: '⊘ Reference: Not needed'}

Validation:
  DevForgeAI: ${devforgeai_pass_count}/6 checks passed
  Claude Code: ${claude_code_pass_count}/6 checks passed
  Overall: ${checkpoint.generation.validation_results.overall_status}
  ${IF warnings: '⚠️ Warnings: ' + warn_count}

Integration:
  Works with: ${checkpoint.specification.integration_skills.join(', ')}
  Context files: ${checkpoint.framework_context.context_files_required.join(', ')}
  Model: ${checkpoint.specification.model}
  Tools: ${checkpoint.specification.tools.join(', ')}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
```

VERIFY: Report displayed (all sections rendered, no null values shown).

RECORD: Update checkpoint:
```
checkpoint.phases["06"].steps_completed.push("6.1")
```

---

### Step 6.2: Provide Next Steps

EXECUTE:
```
Display:
"Next Steps:
  1. Restart your terminal to load the new subagent
  2. Verify it appears: check available agents list
  3. Test it: 'Use ${checkpoint.specification.name} to [describe a task]'
  ${IF reference: '4. Review reference file: ' + reference_path}

Resume Command (if session interrupted):
  /create-agent --resume ${checkpoint.session_id}

Integration Notes:
  - This agent can be invoked via Task(subagent_type='${checkpoint.specification.name}')
  - It integrates with: ${checkpoint.specification.integration_skills.join(', ')}
  - It references: ${checkpoint.framework_context.context_files_required.join(', ')}"
```

VERIFY: Next steps displayed with at least 3 items.

RECORD: Update checkpoint:
```
checkpoint.phases["06"].steps_completed.push("6.2")
```

---

### Step 6.3: Clean Up Checkpoint

EXECUTE:
```
# Mark session as completed
checkpoint.status = "completed"
checkpoint.progress.current_phase = 6
checkpoint.progress.phases_completed = ["01", "02", "03", "04", "05", "06"]
checkpoint.progress.completion_percentage = 100
checkpoint.completed_outputs = {
  "subagent": checkpoint.generation.generated_files.subagent,
  "reference": checkpoint.generation.generated_files.reference,
  "validation_status": checkpoint.generation.validation_results.overall_status
}

# Write final checkpoint state (for audit trail)
Write(file_path="devforgeai/workflows/agent-creation/${checkpoint.session_id}.checkpoint.json", content=checkpoint)

# Then delete checkpoint (session complete)
# Note: In practice, we keep the final checkpoint as a completion record.
# The "delete" is conceptual - the status="completed" field marks it as done.
```

VERIFY:
```
Read(file_path="devforgeai/workflows/agent-creation/${checkpoint.session_id}.checkpoint.json")
Confirm: checkpoint.status == "completed"
Confirm: checkpoint.progress.completion_percentage == 100
Confirm: checkpoint.progress.phases_completed.length == 6
```

RECORD: Update checkpoint:
```
checkpoint.phases["06"].steps_completed.push("6.3")
checkpoint.phases["06"].status = "completed"
```

---

## Phase Exit Verification

```
VERIFY ALL:
  checkpoint.status == "completed"
  checkpoint.progress.completion_percentage == 100
  checkpoint.progress.phases_completed.length == 6
  Generated agent file exists on disk
  checkpoint.phases["06"].status == "completed"

IF ANY fails: HALT -- "Phase 06 exit criteria not met."
```

---

## Phase Transition Display

```
Display:
"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  Agent Creation Complete
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

✅ ${checkpoint.specification.name} created successfully
📁 ${checkpoint.generation.generated_files.subagent}
🔍 Validation: ${checkpoint.generation.validation_results.overall_status}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
```
