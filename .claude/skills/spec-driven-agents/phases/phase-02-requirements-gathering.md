# Phase 02: Requirements Gathering

## Contract

| Attribute | Value |
|-----------|-------|
| **PURPOSE** | Gather complete agent specification from user through mode-specific interaction |
| **REFERENCE** | `src/claude/skills/spec-driven-agents/references/user-interaction-patterns.md` |
| **STEP COUNT** | 5-8 mandatory steps (varies by mode) |
| **MINIMUM QUESTIONS** | 2 (template mode) to 8 (guided mode) |

## Phase Exit Criteria

Before this phase can complete, ALL of the following MUST be true:

- [ ] Agent name validated (kebab-case, no conflicts with existing agents)
- [ ] Purpose captured (non-empty, 2+ sentences)
- [ ] Domain determined (one of: backend, frontend, qa, security, deployment, architecture, documentation, general)
- [ ] Tools selected (non-empty array)
- [ ] Model selected (one of: haiku, sonnet, opus, inherit)
- [ ] Checkpoint updated with all specification data
- [ ] Context files required refined for actual domain (if domain changed from Phase 01)

---

## Reference Loading [MANDATORY]

```
Read(file_path="src/claude/skills/spec-driven-agents/references/user-interaction-patterns.md")
```

IF Read fails: HALT -- "Phase 02 reference file not loaded. Cannot proceed without interaction patterns."

---

## Mandatory Steps

### Step 2.1: Validate Agent Name

**Condition:** Execute for ALL modes.

EXECUTE:
```
IF checkpoint.parameters.agent_name is NOT null:
  EXISTING_CHECK = Glob(pattern=".claude/agents/${checkpoint.parameters.agent_name}.md")
  IF found:
    AskUserQuestion:
      Question: "An agent named '${checkpoint.parameters.agent_name}' already exists. What would you like to do?"
      Header: "Name Conflict"
      Options:
        - label: "Overwrite existing"
          description: "Replace the current agent with the new one"
        - label: "Choose a different name"
          description: "Enter a new name for this agent"
        - label: "Cancel"
          description: "Stop agent creation"
    IF "Overwrite": proceed with current name
    IF "Choose different": ask for new name, re-validate
    IF "Cancel": EXIT skill
  ELSE:
    Display: "Agent name '${checkpoint.parameters.agent_name}' is available."

ELSE (name is null):
  AskUserQuestion:
    Question: "What should the subagent be named? Use lowercase-with-hyphens (e.g., 'coverage-validator', 'api-tester')."
    Header: "Agent Name"
    Options:
      - label: "Let me type a name"
        description: "I'll provide a custom name"
      - label: "Cancel"
        description: "Stop agent creation"
  Extract name from response.
  Validate format: must match [a-z][a-z0-9-]*
  IF invalid format: Ask again with format guidance.
```

VERIFY: `checkpoint.specification.name` is non-null, non-empty, matches `[a-z][a-z0-9-]*`.
IF null or invalid: HALT -- "Step 2.1: Agent name not validated."

RECORD: Update checkpoint:
```
checkpoint.specification.name = validated_name
checkpoint.phases["02"].steps_completed.push("2.1")
checkpoint.phases["02"].questions_answered += 1 (if question was asked)
```

---

### Step 2.2: Determine Creation Mode Requirements

**Condition:** Execute for ALL modes. This step routes to mode-specific sub-steps.

EXECUTE:
```
SWITCH checkpoint.parameters.creation_mode:

  CASE "guided":
    → Execute Steps 2.3g, 2.4g, 2.5g, 2.6g, 2.7g (guided-specific steps)

  CASE "template":
    → Execute Steps 2.3t, 2.4t (template-specific steps)

  CASE "domain":
    → Execute Steps 2.3d, 2.4d (domain-specific steps)

  CASE "custom":
    → Execute Steps 2.3c, 2.4c (custom-specific steps)
```

VERIFY: Mode is one of: guided, template, domain, custom.
IF unknown mode: HALT -- "Step 2.2: Unknown creation mode."

RECORD: Update checkpoint:
```
checkpoint.phases["02"].steps_completed.push("2.2")
```

---

### Step 2.3g: Guided Mode - Domain and Purpose

**Condition:** Only execute if mode == "guided"

EXECUTE:
```
AskUserQuestion:
  Question: "What domain does this agent specialize in?"
  Header: "Domain"
  Options:
    - label: "Backend"
      description: "Server-side logic, APIs, databases, clean architecture"
    - label: "Frontend"
      description: "UI components, state management, accessibility"
    - label: "QA"
      description: "Testing, coverage, quality validation"
    - label: "Security"
      description: "Vulnerability detection, auth, data protection"

Store response as domain.

AskUserQuestion:
  Question: "Describe the agent's purpose in 2-3 sentences. What problem does it solve?"
  Header: "Purpose"
  Options:
    - label: "Let me describe it"
      description: "I'll provide a custom description"

Store response as purpose.
```

VERIFY: `checkpoint.specification.domain` is non-null AND `checkpoint.specification.purpose` is non-null and length > 20 characters.
IF either null or purpose too short: HALT -- "Step 2.3g: Domain or purpose not captured."

RECORD: Update checkpoint:
```
checkpoint.specification.domain = domain
checkpoint.specification.purpose = purpose
checkpoint.phases["02"].steps_completed.push("2.3g")
checkpoint.phases["02"].questions_answered += 2
```

---

### Step 2.4g: Guided Mode - Responsibilities

**Condition:** Only execute if mode == "guided"

EXECUTE:
```
AskUserQuestion:
  Question: "What are this agent's primary responsibilities? Select all that apply."
  Header: "Responsibilities"
  multiSelect: true
  Options:
    - label: "Code generation"
      description: "Writing production code"
    - label: "Analysis"
      description: "Reviewing, auditing, analyzing code or data"
    - label: "Testing"
      description: "Writing or running tests"
    - label: "Documentation"
      description: "Writing docs, comments, guides"

Store selected responsibilities.
```

VERIFY: `checkpoint.specification.responsibilities` is non-empty array with at least 1 item.
IF empty: HALT -- "Step 2.4g: Responsibilities not captured."

RECORD: Update checkpoint:
```
checkpoint.specification.responsibilities = selected_responsibilities
checkpoint.phases["02"].steps_completed.push("2.4g")
checkpoint.phases["02"].questions_answered += 1
```

---

### Step 2.5g: Guided Mode - Tools Selection

**Condition:** Only execute if mode == "guided"

EXECUTE:
```
# Suggest tools based on domain + responsibilities
suggested_tools = derive_tools_from(domain, responsibilities)

AskUserQuestion:
  Question: "Which tools should this agent have access to? Suggested based on domain: ${suggested_tools.join(', ')}"
  Header: "Tools"
  Options:
    - label: "Use suggested tools"
      description: "${suggested_tools.join(', ')}"
    - label: "Inherit all tools"
      description: "Give agent access to all available tools"
    - label: "Custom selection"
      description: "I'll specify which tools to include"

IF "Use suggested": tools = suggested_tools
IF "Inherit all": tools = ["*"]
IF "Custom": Ask follow-up for specific tool list
```

VERIFY: `checkpoint.specification.tools` is non-empty array.
IF empty: HALT -- "Step 2.5g: Tools not selected."

RECORD: Update checkpoint:
```
checkpoint.specification.tools = selected_tools
checkpoint.phases["02"].steps_completed.push("2.5g")
checkpoint.phases["02"].questions_answered += 1
```

---

### Step 2.6g: Guided Mode - Model Selection

**Condition:** Only execute if mode == "guided"

EXECUTE:
```
# Suggest model based on complexity
estimated_complexity = assess_from(responsibilities, purpose)
suggested_model = IF estimated_complexity == "simple" THEN "haiku"
                  ELIF estimated_complexity == "medium" THEN "sonnet"
                  ELSE "opus"

AskUserQuestion:
  Question: "Which model should power this agent? Suggested: ${suggested_model} (${estimated_complexity} complexity)"
  Header: "Model"
  Options:
    - label: "${suggested_model} (Recommended)"
      description: "Best for ${estimated_complexity} complexity tasks"
    - label: "haiku"
      description: "Fast, efficient - best for simple tasks (<10K tokens)"
    - label: "sonnet"
      description: "Balanced - best for medium complexity (10-50K tokens)"
    - label: "opus"
      description: "Most capable - best for complex tasks (>50K tokens)"
```

VERIFY: `checkpoint.specification.model` is one of: haiku, sonnet, opus, inherit.
IF null or invalid: HALT -- "Step 2.6g: Model not selected."

RECORD: Update checkpoint:
```
checkpoint.specification.model = selected_model
checkpoint.phases["02"].steps_completed.push("2.6g")
checkpoint.phases["02"].questions_answered += 1
```

---

### Step 2.7g: Guided Mode - Integration Skills

**Condition:** Only execute if mode == "guided"

EXECUTE:
```
# Determine integration skills from domain mapping in Phase 01
integration_skills = get_integration_skills_for(domain)

Display: "Based on domain '${domain}', this agent will integrate with: ${integration_skills.join(', ')}"

AskUserQuestion:
  Question: "Does this agent need to integrate with any additional DevForgeAI skills?"
  Header: "Integration"
  Options:
    - label: "Default integration is fine"
      description: "${integration_skills.join(', ')}"
    - label: "Add more integrations"
      description: "I need to add specific skill integrations"
```

VERIFY: `checkpoint.specification.integration_skills` is non-empty array.
IF empty: HALT -- "Step 2.7g: Integration skills not determined."

RECORD: Update checkpoint:
```
checkpoint.specification.integration_skills = final_integration_skills
checkpoint.phases["02"].steps_completed.push("2.7g")
checkpoint.phases["02"].questions_answered += 1
```

---

### Step 2.3t: Template Mode - Load and Customize Template

**Condition:** Only execute if mode == "template"

EXECUTE:
```
TEMPLATE_PATH = "src/claude/skills/spec-driven-agents/assets/templates/${checkpoint.parameters.template_name}-template.md"

Glob(pattern=TEMPLATE_PATH)
IF not found:
  AskUserQuestion:
    Question: "Template '${checkpoint.parameters.template_name}' not found. Available: code-reviewer, test-automator, documentation-writer, deployment-coordinator, requirements-analyst. Which template?"
    Header: "Template"
    Options:
      - label: "code-reviewer"
        description: "Code quality, security, best practices"
      - label: "test-automator"
        description: "TDD test generation"
      - label: "Use guided mode instead"
        description: "Switch to interactive guided creation"

Read(file_path=TEMPLATE_PATH)
Extract {placeholders} from template.
For each placeholder that cannot be auto-filled, ask user.
```

VERIFY: Template loaded and all placeholders resolved.

RECORD: Update checkpoint with template data, domain, purpose, tools, model extracted from template.

---

### Step 2.4t: Template Mode - Confirm Specification

**Condition:** Only execute if mode == "template"

EXECUTE:
```
Display specification summary extracted from template.
AskUserQuestion:
  Question: "Does this specification look correct for your agent?"
  Header: "Confirm"
  Options:
    - label: "Looks good, proceed"
      description: "Generate agent with these settings"
    - label: "I need to change something"
      description: "Let me adjust the specification"
```

VERIFY: User confirmed specification.

RECORD: Update checkpoint with confirmed specification data.

---

### Step 2.3d: Domain Mode - Apply Presets and Get Purpose

**Condition:** Only execute if mode == "domain"

EXECUTE:
```
# Apply domain presets from framework-integration-patterns.md
domain = checkpoint.parameters.domain
presets = get_domain_presets(domain)

checkpoint.specification.tools = presets.tools
checkpoint.specification.model = presets.model
checkpoint.specification.context_files = presets.context_files
checkpoint.specification.integration_skills = presets.integration_skills

AskUserQuestion:
  Question: "What specific purpose should this ${domain} agent serve? Describe in 2-3 sentences."
  Header: "Purpose"
  Options:
    - label: "Let me describe it"
      description: "I'll provide a custom description"
```

VERIFY: Purpose captured and domain presets applied.

RECORD: Update checkpoint with domain presets + purpose.

---

### Step 2.4d: Domain Mode - Confirm Presets

**Condition:** Only execute if mode == "domain"

EXECUTE:
```
Display: "Domain presets for '${domain}':"
Display: "  Tools: ${presets.tools.join(', ')}"
Display: "  Model: ${presets.model}"
Display: "  Context files: ${presets.context_files.join(', ')}"

AskUserQuestion:
  Question: "Accept these domain presets or customize?"
  Header: "Presets"
  Options:
    - label: "Accept presets"
      description: "Use standard ${domain} configuration"
    - label: "Customize"
      description: "I want to modify the tools, model, or context files"
```

VERIFY: User confirmed or customized presets. All spec fields populated.

RECORD: Update checkpoint with final specification.

---

### Step 2.3c: Custom Spec Mode - Load and Parse Specification

**Condition:** Only execute if mode == "custom"

EXECUTE:
```
Read(file_path=checkpoint.parameters.spec_file)
IF Read fails:
  AskUserQuestion:
    Question: "Specification file '${checkpoint.parameters.spec_file}' not found. What would you like to do?"
    Header: "Spec File"
    Options:
      - label: "Provide correct path"
        description: "I'll give the right file path"
      - label: "Switch to guided mode"
        description: "Create the agent interactively instead"

Parse specification (YAML or Markdown with frontmatter).
Extract: name, purpose, domain, tools, model, responsibilities, workflow.
Validate required fields present.
```

VERIFY: All required fields extracted from spec file.

RECORD: Update checkpoint with parsed specification data.

---

### Step 2.4c: Custom Spec Mode - Enrich with Framework Context

**Condition:** Only execute if mode == "custom"

EXECUTE:
```
Enrich specification with framework context:
- Add context_files if missing (infer from domain)
- Add integration_points if missing (infer from responsibilities)
- Add token_efficiency if missing (add standard strategies)

Display enriched specification to user.
AskUserQuestion:
  Question: "I've enriched your specification with framework context. Proceed with generation?"
  Header: "Enriched Spec"
  Options:
    - label: "Proceed"
      description: "Generate agent with enriched specification"
    - label: "Review changes"
      description: "Show me what was added"
```

VERIFY: Enriched specification has all required fields populated.

RECORD: Update checkpoint with enriched specification.

---

### Step 2.8: Finalize and Refine Context Files (ALL modes)

**Condition:** Execute for ALL modes after mode-specific steps complete.

EXECUTE:
```
# If domain changed from Phase 01's initial determination, update context_files_required
IF checkpoint.specification.domain != initial_domain_from_phase_01:
  Recalculate context_files_required using domain-to-context-file mapping
  Update checkpoint.framework_context.context_files_required

Display specification summary:
  Name: ${checkpoint.specification.name}
  Purpose: ${checkpoint.specification.purpose}
  Domain: ${checkpoint.specification.domain}
  Tools: ${checkpoint.specification.tools.join(', ')}
  Model: ${checkpoint.specification.model}
  Context Files: ${checkpoint.framework_context.context_files_required.join(', ')}
```

VERIFY: ALL of the following are non-null and non-empty:
- `checkpoint.specification.name`
- `checkpoint.specification.purpose`
- `checkpoint.specification.domain`
- `checkpoint.specification.tools`
- `checkpoint.specification.model`

IF ANY is null or empty: HALT -- "Step 2.8: Specification incomplete."

RECORD: Update checkpoint:
```
checkpoint.phases["02"].status = "completed"
checkpoint.progress.current_phase = 3
checkpoint.progress.phases_completed.push("02")
checkpoint.progress.completion_percentage = 33
```
Write updated checkpoint to disk.

---

## Phase Exit Verification

```
VERIFY ALL:
  checkpoint.specification.name is non-null
  checkpoint.specification.purpose is non-null (length > 20)
  checkpoint.specification.domain is in valid_domains
  checkpoint.specification.tools is non-empty array
  checkpoint.specification.model is in [haiku, sonnet, opus, inherit]
  checkpoint.phases["02"].status == "completed"

IF ANY fails: HALT -- "Phase 02 exit criteria not met."
```

---

## Phase Transition Display

```
Display:
"Phase 02 Complete: Requirements Gathered
  Agent: ${checkpoint.specification.name}
  Domain: ${checkpoint.specification.domain}
  Mode: ${checkpoint.parameters.creation_mode}
  Questions answered: ${checkpoint.phases['02'].questions_answered}
  → Proceeding to Phase 03: Specification Assembly"
```
