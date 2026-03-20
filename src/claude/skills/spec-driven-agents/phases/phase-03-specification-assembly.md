# Phase 03: Specification Assembly

## Contract

| Attribute | Value |
|-----------|-------|
| **PURPOSE** | Assemble a complete specification document for the agent-generator subagent |
| **REFERENCE** | `src/claude/skills/spec-driven-agents/references/subagent-creation-workflow.md` |
| **STEP COUNT** | 3 mandatory steps |

## Phase Exit Criteria

Before this phase can complete, ALL of the following MUST be true:

- [ ] Specification JSON assembled with all required fields
- [ ] Template content loaded (if template mode)
- [ ] Specification written to checkpoint as structured data
- [ ] Checkpoint updated with phase completion

---

## Reference Loading [MANDATORY]

```
Read(file_path="src/claude/skills/spec-driven-agents/references/subagent-creation-workflow.md")
```

IF Read fails: HALT -- "Phase 03 reference file not loaded. Cannot proceed without workflow reference."

---

## Mandatory Steps

### Step 3.1: Load Template Content (If Applicable)

EXECUTE:
```
IF checkpoint.parameters.creation_mode == "template":
  TEMPLATE_PATH = "src/claude/skills/spec-driven-agents/assets/templates/${checkpoint.parameters.template_name}-template.md"
  Read(file_path=TEMPLATE_PATH)
  Store template_content in session

ELIF checkpoint.parameters.creation_mode == "domain":
  # No template to load, but load domain presets from framework-integration-patterns
  # (already loaded in Phase 01, use from checkpoint)
  domain_presets = checkpoint.framework_context (already populated)

ELIF checkpoint.parameters.creation_mode == "custom":
  # Spec file already parsed in Phase 02
  # Use enriched specification from checkpoint
  custom_spec = checkpoint.specification

ELSE (guided mode):
  # All data gathered interactively in Phase 02
  # No additional loading needed
  guided_spec = checkpoint.specification
```

VERIFY: For template mode: template_content is non-empty. For all other modes: checkpoint.specification is populated.
IF template mode and template_content is empty: HALT -- "Step 3.1: Template content not loaded."

RECORD: Update checkpoint:
```
checkpoint.phases["03"].steps_completed.push("3.1")
```

---

### Step 3.2: Assemble Complete Specification

EXECUTE:
```
specification = {
  "name": checkpoint.specification.name,
  "mode": checkpoint.parameters.creation_mode,
  "framework": "DevForgeAI",
  "purpose": checkpoint.specification.purpose,
  "domain": checkpoint.specification.domain,
  "tools": checkpoint.specification.tools,
  "model": checkpoint.specification.model,
  "responsibilities": checkpoint.specification.responsibilities,
  "integration_skills": checkpoint.specification.integration_skills,
  "context_files": checkpoint.framework_context.context_files_required,
  "template_content": template_content (if template mode, else null),
  "spec_file_content": custom_spec (if custom mode, else null),
  "generation_instructions": {
    "sections_required": [
      "YAML frontmatter",
      "Purpose",
      "When Invoked (proactive triggers)",
      "Workflow (numbered steps)",
      "Framework Integration",
      "Tool Usage Protocol",
      "Success Criteria",
      "Principles",
      "Token Efficiency",
      "References"
    ],
    "validation_required": true,
    "reference_file_generation": "conditional (based on domain and responsibilities)"
  }
}
```

VERIFY: specification object has ALL required fields non-null:
- name, mode, framework, purpose, domain, tools, model
- generation_instructions.sections_required is array with 10 items
IF any required field is null: HALT -- "Step 3.2: Specification incomplete."

RECORD: Update checkpoint:
```
checkpoint.specification = merge(checkpoint.specification, specification)
checkpoint.phases["03"].steps_completed.push("3.2")
```

---

### Step 3.3: Determine Reference File Need

The agent-generator can optionally create a reference file alongside the agent. This step determines whether one is needed, so the generator knows upfront.

EXECUTE:
```
NEEDS_REFERENCE = false

IF checkpoint.specification.domain in ["qa", "architecture", "security", "deployment"]:
  NEEDS_REFERENCE = true
  REFERENCE_TYPE = "domain-constraints"

ELIF responsibilities include "decision-making" or "coordination":
  NEEDS_REFERENCE = true
  REFERENCE_TYPE = "decision-guidance"

ELIF checkpoint.parameters.creation_mode == "template" AND template includes reference markers:
  NEEDS_REFERENCE = true
  REFERENCE_TYPE = "template-defined"

ELSE:
  NEEDS_REFERENCE = false

checkpoint.generation.reference_file_needed = NEEDS_REFERENCE
```

VERIFY: `checkpoint.generation.reference_file_needed` is set to true or false (not null).
IF null: HALT -- "Step 3.3: Reference file need not determined."

RECORD: Update checkpoint:
```
checkpoint.generation.reference_file_needed = NEEDS_REFERENCE
checkpoint.phases["03"].steps_completed.push("3.3")
checkpoint.phases["03"].status = "completed"
checkpoint.progress.current_phase = 4
checkpoint.progress.phases_completed.push("03")
checkpoint.progress.completion_percentage = 50
```
Write updated checkpoint to disk.

---

## Phase Exit Verification

```
VERIFY ALL:
  checkpoint.specification.name is non-null
  checkpoint.specification.purpose is non-null
  checkpoint.specification.domain is non-null
  checkpoint.specification.tools is non-empty
  checkpoint.specification.model is non-null
  checkpoint.generation.reference_file_needed is boolean (not null)
  checkpoint.phases["03"].status == "completed"

IF ANY fails: HALT -- "Phase 03 exit criteria not met."
```

---

## Phase Transition Display

```
Display:
"Phase 03 Complete: Specification Assembled
  Agent: ${checkpoint.specification.name}
  Sections required: 10
  Reference file: ${checkpoint.generation.reference_file_needed ? 'Will be generated' : 'Not needed'}
  → Proceeding to Phase 04: Agent Generation (delegating to agent-generator subagent)"
```
