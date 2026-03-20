# User Interaction Patterns

**Purpose:** AskUserQuestion patterns for guided, template, domain, and custom creation modes

---

## Interaction Principles

1. **Minimize question count** - Each question should gather maximum information
2. **Provide sensible defaults** - Based on domain, suggest tools and model
3. **Use options, not free text** - Reduce ambiguity with structured choices
4. **Confirm before generation** - Always show summary before Phase 04

---

## Guided Mode Questions (8 total)

### Question 1: Domain Selection
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
  # Additional domains available via "Other": deployment, architecture, documentation, general
```

### Question 2: Purpose Description
```
AskUserQuestion:
  Question: "Describe the agent's purpose in 2-3 sentences. What problem does it solve?"
  Header: "Purpose"
  Options:
    - label: "Let me describe it"
      description: "I'll provide a custom purpose description"
```
**Validation:** Response must be >20 characters. If shorter, ask for elaboration.

### Question 3: Responsibilities
```
AskUserQuestion:
  Question: "What are this agent's primary responsibilities?"
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
  # Additional via "Other": Validation, Coordination, Decision-making
```

### Question 4: Tool Selection
```
AskUserQuestion:
  Question: "Which tools should this agent have access to?"
  Header: "Tools"
  Options:
    - label: "Use suggested tools (Recommended)"
      description: "{suggested_tools_based_on_domain}"
    - label: "Inherit all tools"
      description: "Give agent access to everything"
    - label: "Custom selection"
      description: "I'll specify which tools"
```

### Question 5: Model Selection
```
AskUserQuestion:
  Question: "Which model should power this agent?"
  Header: "Model"
  Options:
    - label: "{suggested_model} (Recommended)"
      description: "Best for {complexity_level} tasks"
    - label: "haiku"
      description: "Fast and efficient (<10K tokens)"
    - label: "sonnet"
      description: "Balanced (10-50K tokens)"
    - label: "opus"
      description: "Most capable (>50K tokens)"
```

### Question 6: Integration Skills
```
AskUserQuestion:
  Question: "Does this agent need additional DevForgeAI skill integrations?"
  Header: "Integration"
  Options:
    - label: "Default integration is fine"
      description: "{default_integrations_for_domain}"
    - label: "Add more integrations"
      description: "I need additional skill connections"
```

---

## Template Mode Questions (2-4 total)

### Question 1: Template Confirmation (if template found)
```
AskUserQuestion:
  Question: "Using template: {template_name}. Customize placeholders?"
  Header: "Template"
  Options:
    - label: "Use defaults"
      description: "Auto-fill with sensible values"
    - label: "Customize"
      description: "I want to modify specific placeholders"
```

### Question 2: Specification Confirmation
```
AskUserQuestion:
  Question: "Does this specification look correct?"
  Header: "Confirm"
  Options:
    - label: "Looks good, proceed"
      description: "Generate with these settings"
    - label: "I need changes"
      description: "Let me adjust something"
```

---

## Domain Mode Questions (2-3 total)

### Question 1: Purpose within Domain
```
AskUserQuestion:
  Question: "What specific purpose should this {domain} agent serve?"
  Header: "Purpose"
  Options:
    - label: "Let me describe it"
      description: "I'll provide the specific purpose"
```

### Question 2: Preset Confirmation
```
AskUserQuestion:
  Question: "Accept standard {domain} configuration?"
  Header: "Presets"
  Options:
    - label: "Accept presets"
      description: "Tools: {tools}, Model: {model}"
    - label: "Customize"
      description: "Modify tools, model, or context files"
```

---

## Custom Spec Mode Questions (1-2 total)

### Question 1: Enrichment Confirmation
```
AskUserQuestion:
  Question: "I've enriched your spec with framework context. Proceed?"
  Header: "Enriched"
  Options:
    - label: "Proceed"
      description: "Generate with enriched specification"
    - label: "Review changes"
      description: "Show me what was added"
```

---

## Common Patterns

### Name Conflict Resolution
```
AskUserQuestion:
  Question: "Agent '{name}' already exists. What to do?"
  Header: "Conflict"
  Options:
    - label: "Overwrite"
      description: "Replace existing agent"
    - label: "Rename"
      description: "Choose a different name"
    - label: "Cancel"
      description: "Stop creation"
```

### Validation Failure Decision
```
AskUserQuestion:
  Question: "{N} validation checks failed after auto-fix. What to do?"
  Header: "Validation"
  Options:
    - label: "Proceed with warnings"
      description: "Accept agent with known issues"
    - label: "Regenerate"
      description: "Try generating again"
    - label: "Cancel"
      description: "Abort creation"
```

### Context Window Warning
```
AskUserQuestion:
  Question: "Context window approaching limit. Save progress?"
  Header: "Context"
  Options:
    - label: "Save and resume later"
      description: "Checkpoint saved, use --resume to continue"
    - label: "Continue"
      description: "Proceed (risk of truncation)"
```
