# Phase 04: Agent Generation

## Contract

| Attribute | Value |
|-----------|-------|
| **PURPOSE** | Delegate agent file generation to agent-generator subagent in isolated context |
| **REFERENCE** | `src/claude/skills/spec-driven-agents/references/subagent-creation-workflow.md` |
| **STEP COUNT** | 2 mandatory steps |
| **REQUIRED SUBAGENT** | agent-generator [BLOCKING] |

## Phase Exit Criteria

Before this phase can complete, ALL of the following MUST be true:

- [ ] agent-generator subagent invoked via Task() (NOT generated inline)
- [ ] Generated agent file exists on disk at `.claude/agents/{name}.md`
- [ ] Reference file exists on disk (if checkpoint.generation.reference_file_needed == true)
- [ ] Generation report captured in checkpoint
- [ ] Checkpoint updated with phase completion

---

## Reference Loading [MANDATORY]

```
Read(file_path="src/claude/skills/spec-driven-agents/references/subagent-creation-workflow.md")
```

IF Read fails: HALT -- "Phase 04 reference file not loaded. Cannot proceed without workflow reference."

---

## Mandatory Steps

### Step 4.1: Invoke agent-generator Subagent

This step MUST delegate to the agent-generator subagent. Do NOT attempt to generate the agent file inline. The agent-generator runs in isolated context, which prevents accumulated bias from affecting generation quality.

EXECUTE:
```
Task(
  subagent_type="agent-generator",
  description="Generate ${checkpoint.specification.name} subagent",
  prompt="Generate a DevForgeAI-aware Claude Code subagent following this specification:

**Specification:**
- Name: ${checkpoint.specification.name}
- Mode: ${checkpoint.parameters.creation_mode}
- Framework: DevForgeAI
- Purpose: ${checkpoint.specification.purpose}
- Domain: ${checkpoint.specification.domain}
- Tools: ${checkpoint.specification.tools.join(', ')}
- Model: ${checkpoint.specification.model}
- Responsibilities: ${checkpoint.specification.responsibilities.join(', ')}
- Integration Skills: ${checkpoint.specification.integration_skills.join(', ')}
- Context Files: ${checkpoint.framework_context.context_files_required.join(', ')}
- Reference File Needed: ${checkpoint.generation.reference_file_needed}

${IF template mode: 'Template Content:\n' + template_content}
${IF custom mode: 'Custom Spec:\n' + spec_file_content}

**Instructions:**
1. Load Phase 0 framework references
2. Execute mode-specific generation workflow
3. Generate system prompt with all 10 required sections:
   - YAML frontmatter, Purpose, When Invoked, Workflow, Framework Integration,
   - Tool Usage Protocol, Success Criteria, Principles, Token Efficiency, References
4. Run 12-point validation (6 DevForgeAI + 6 Claude Code checks)
5. Generate reference file if needed: ${checkpoint.generation.reference_file_needed}
6. Write subagent file to .claude/agents/${checkpoint.specification.name}.md
7. Return structured report with generated_files, validation, integration, next_steps

**Expected Output Format:**
{
  'generated_files': {'subagent': path, 'reference': path_or_null},
  'validation': {'devforgeai_compliance': results, 'claude_code_compliance': results, 'overall_status': status},
  'integration': {'works_with': [], 'invoked_by': [], 'context_files': []},
  'next_steps': []
}"
)
```

VERIFY:
1. Task() was invoked (not skipped or replaced with inline generation)
2. Task returned a result (not null, not error)
3. Generated file exists: `Glob(pattern=".claude/agents/${checkpoint.specification.name}.md")`
IF Glob returns empty: HALT -- "Step 4.1: Agent file not generated. Check agent-generator output for errors."

RECORD: Update checkpoint:
```
checkpoint.generation.generated_files = {
  "subagent": ".claude/agents/${checkpoint.specification.name}.md",
  "reference": reference_path_or_null
}
checkpoint.phases["04"].steps_completed.push("4.1")
```

---

### Step 4.2: Capture Generation Report

EXECUTE:
```
# Extract structured data from agent-generator response
generation_report = parse_agent_generator_output(task_result)

# Verify generated file content has minimum quality
Read(file_path=".claude/agents/${checkpoint.specification.name}.md")
line_count = count_lines(content)

IF line_count < 50:
  Display: "WARNING: Generated agent file is only ${line_count} lines. Expected >200 for framework compliance."

# Check for reference file if needed
IF checkpoint.generation.reference_file_needed:
  reference_path = generation_report.generated_files.reference
  IF reference_path:
    Glob(pattern=reference_path)
    IF not found:
      Display: "WARNING: Reference file was expected but not generated at ${reference_path}."
```

VERIFY:
- generation_report is not null
- generation_report.validation exists
- generation_report.generated_files.subagent path verified via Glob
IF generation_report is null: HALT -- "Step 4.2: Generation report not captured."

RECORD: Update checkpoint:
```
checkpoint.generation.validation_results = generation_report.validation
checkpoint.phases["04"].steps_completed.push("4.2")
checkpoint.phases["04"].status = "completed"
checkpoint.progress.current_phase = 5
checkpoint.progress.phases_completed.push("04")
checkpoint.progress.completion_percentage = 67
```
Write updated checkpoint to disk.

---

## Phase Exit Verification

```
VERIFY ALL:
  Glob(".claude/agents/${checkpoint.specification.name}.md") returns file
  checkpoint.generation.generated_files.subagent is non-null
  checkpoint.generation.validation_results is non-null
  checkpoint.phases["04"].status == "completed"

  IF checkpoint.generation.reference_file_needed:
    checkpoint.generation.generated_files.reference is non-null

IF ANY fails: HALT -- "Phase 04 exit criteria not met."
```

---

## Phase Transition Display

```
Display:
"Phase 04 Complete: Agent Generated
  File: ${checkpoint.generation.generated_files.subagent}
  Reference: ${checkpoint.generation.generated_files.reference || 'None'}
  Preliminary validation: ${checkpoint.generation.validation_results.overall_status}
  → Proceeding to Phase 05: Validation (independent 12-point compliance check)"
```
