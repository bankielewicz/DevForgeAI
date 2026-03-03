# Framework Validation Workflow

**Purpose:** Complete validation procedures for generated subagents against DevForgeAI constraints.

---

## Pre-Generation Validation

**MANDATORY before any Write() operation:**

### Step 1: Load source-tree.md Constraints

```
Read(file_path="devforgeai/specs/context/source-tree.md")
```

### Step 2: Validate Output Location

**Allowed locations:**
- Subagent files: `.claude/agents/` or `src/.claude/agents/`
- Reference files: `.claude/agents/{subagent}/references/` or `src/.claude/agents/{subagent}/references/`

**Validation:**
```
IF target_path NOT in allowed_patterns:
  HALT: SOURCE-TREE CONSTRAINT VIOLATION
  - Expected: .claude/agents/ or src/.claude/agents/
  - Attempted: {target_path}
  - Action: Use AskUserQuestion for guidance
```

---

## DevForgeAI Framework Compliance Validation

### Check 1: Tool Usage Validation

Verify no Bash for file operations:

```
Grep(pattern="Bash\\(cat:|grep:|find:|sed:|awk:|echo >|head:|tail:",
     path="[generated_content]")

IF matches found:
  VIOLATION: "Subagent uses Bash for file operations"
  List violations with line numbers
  Auto-fix: Replace Bash commands with native tools
  Status: FAIL
ELSE:
  PASS: "✅ Tool usage follows native tools pattern"
```

### Check 2: Context File Awareness

Verify domain-appropriate context file references:

**Expected by domain:**
- backend: All 6 context files
- frontend: tech-stack.md, source-tree.md, coding-standards.md
- qa: anti-patterns.md, coding-standards.md
- architecture: All 6 context files
- security: anti-patterns.md, coding-standards.md, architecture-constraints.md
- deployment: tech-stack.md, dependencies.md, source-tree.md

```
Grep(pattern="tech-stack\\.md|source-tree\\.md|dependencies\\.md|
              coding-standards\\.md|architecture-constraints\\.md|
              anti-patterns\\.md",
     path="[generated_content]")

context_file_count = count of matches

IF domain requires context files AND context_file_count == 0:
  WARN: "Should reference context files: [list for domain]"
  Suggestion: "Add to Framework Integration section"
  Status: PASS WITH WARNINGS
ELSE:
  PASS: "✅ Context file awareness present"
```

### Check 3: Framework Integration Section

```
Grep(pattern="## Framework Integration|Works with:|Invoked by:",
     path="[generated_content]")

IF pattern not found:
  VIOLATION: "Missing Framework Integration section"
  Auto-fix: Add Framework Integration section
  Status: FAIL
ELSE:
  # Check for skill references
  Grep(pattern="devforgeai-[a-z]+", path="[generated_content]")

  IF skill_references == 0:
    WARN: "No DevForgeAI skill integration documented"
    Status: PASS WITH WARNINGS
  ELSE:
    PASS: "✅ Framework integration documented"
```

### Check 4: Tool Usage Protocol Section

```
Grep(pattern="## Tool Usage Protocol|File Operations.*native tools",
     path="[generated_content]")

IF pattern not found:
  VIOLATION: "Missing Tool Usage Protocol section"
  Auto-fix: Add complete Tool Usage Protocol section
  Status: FAIL
ELSE:
  PASS: "✅ Tool Usage Protocol section present"
```

### Check 5: Token Efficiency Section

```
Grep(pattern="## Token Efficiency|Token.*target|40-73% token savings",
     path="[generated_content]")

IF pattern not found:
  VIOLATION: "Missing Token Efficiency section"
  Auto-fix: Add Token Efficiency section
  Status: FAIL
ELSE:
  PASS: "✅ Token efficiency strategies documented"
```

### Check 6: Lean Orchestration (Command-Related Only)

```
IF subagent_purpose contains "command|formatter|interpreter|orchestrator":

  Grep(pattern="reference file|framework guardrails",
       path="[generated_content]")

  IF pattern not found:
    VIOLATION: "Command-related subagent MUST generate reference file"
    Flag: NEEDS_REFERENCE_FILE = true
    Status: FAIL
  ELSE:
    PASS: "✅ Reference file generation planned"
ELSE:
  PASS: "N/A - Not command-related"
```

---

## Claude Code Best Practice Validation

### Check 1: YAML Frontmatter Format

```
Validate:
- name: lowercase-with-hyphens ✓
- description: natural language with triggers ✓
- tools: comma-separated list ✓
- model: haiku|sonnet|opus|inherit ✓
- Proper YAML delimiters (---) ✓

IF parse_error:
  VIOLATION: "Invalid YAML syntax"
  Show error details
  Status: FAIL
ELSE:
  PASS: "✅ YAML frontmatter valid"
```

### Check 2: Description Field Quality

```
IF "proactively" in description AND subagent has auto-invoke triggers:
  PASS: "✅ Description follows trigger documentation pattern"
ELSE IF subagent has auto-invoke triggers AND "proactively" NOT in description:
  WARN: "Should include 'proactively' in description"
  Status: PASS WITH WARNINGS
ELSE:
  PASS: "Description appropriate"
```

### Check 3: Tool Selection Appropriateness

```
Expected tools by task type:
- Validation/Analysis: Read, Grep, Glob
- Code Generation: Read, Write, Edit, Grep, Glob
- Testing: Read, Write, Edit, Bash(pytest:*|npm:test)
- Deployment: Read, Write, Bash(docker:*|kubectl:*)

IF tools_count > expected:
  WARN: "Tool access broader than needed"
  Suggest: [minimal tool set]
  Status: PASS WITH WARNINGS
ELSE:
  PASS: "✅ Tool selection follows least privilege"
```

### Check 4: Model Selection

```
Validate model choice:
- haiku: <10K tokens (simple tasks)
- sonnet: 10-50K tokens (complex reasoning)
- opus: >50K tokens (extremely complex)
- inherit: Match main conversation

IF model == "haiku" AND estimated_tokens > 10000:
  WARN: "Haiku may be insufficient"
  Suggest: "Use sonnet for tasks >10K tokens"
ELSE IF model == "sonnet" AND estimated_tokens < 5000:
  INFO: "Sonnet may be overqualified"
  Suggest: "Consider haiku for faster execution"
ELSE:
  PASS: "✅ Model selection appropriate"
```

### Check 5: System Prompt Structure

**Required sections:**
- `## Purpose`
- `## When Invoked`
- `## Workflow`
- `## Success Criteria`

**DevForgeAI sections (if framework-aware):**
- `## Framework Integration`
- `## Tool Usage Protocol`
- `## Token Efficiency`

```
missing_sections = []
FOR section in required_sections:
  IF section not found:
    missing_sections.append(section)

IF missing_sections:
  VIOLATION: "Missing sections: [list]"
  Auto-fix: Generate placeholder sections
  Status: FAIL
ELSE:
  PASS: "✅ All required sections present"
```

### Check 6: Workflow Steps Quality

```
Count workflow steps

IF step_count < 3:
  WARN: "Workflow too simple (<3 steps)"
  Status: PASS WITH WARNINGS
ELSE IF step_count > 15:
  WARN: "Workflow too complex (>15 steps, consider decomposition)"
  Status: PASS WITH WARNINGS
ELSE:
  PASS: "✅ Workflow step count appropriate"
```

---

## Validation Report Template

```markdown
## Framework Compliance Validation Report

**Generated for:** [subagent-name]
**Validation Date:** [timestamp]

### DevForgeAI Framework Compliance

| Check | Status | Details |
|-------|--------|---------|
| Tool usage (native tools) | [✅/❌/⚠️] | [Details] |
| Context file awareness | [✅/❌/⚠️] | [Files referenced] |
| Framework integration | [✅/❌/⚠️] | [Skills documented] |
| Tool usage protocol | [✅/❌/⚠️] | [Section present] |
| Token efficiency | [✅/❌/⚠️] | [Strategies documented] |
| Lean orchestration | [✅/❌/⚠️/N/A] | [Reference file planned] |

### Claude Code Best Practice Compliance

| Check | Status | Details |
|-------|--------|---------|
| YAML frontmatter | [✅/❌] | [Valid or error] |
| Description quality | [✅/⚠️] | [Triggers documented] |
| Tool selection | [✅/⚠️] | [Appropriate or excessive] |
| Model selection | [✅/⚠️] | [Appropriate or suboptimal] |
| System prompt structure | [✅/❌] | [All sections or missing] |
| Workflow quality | [✅/⚠️] | [[count] steps] |

### Overall Status

**Result:** [PASS | PASS WITH WARNINGS | FAIL]

**Critical Issues (Must Fix):**
[List FAIL items with auto-fix suggestions]

**Warnings (Should Address):**
[List WARN items with suggestions]

**Summary:**
- Passes: [count]/12 checks
- Warnings: [count]/12 checks
- Failures: [count]/12 checks

### Recommended Actions

IF status == FAIL:
  1. Address critical issues
  2. Apply auto-fixes: [list]
  3. Manual fixes: [list]
  4. Re-validate

IF status == PASS WITH WARNINGS:
  1. Review warnings (optional)
  2. Decide: Apply or proceed as-is
  3. Warnings don't block file write
```

---

## Auto-Fix Logic

```
IF status == FAIL AND auto_fixes_available:

  AskUserQuestion:
    Question: "Framework validation found issues. How to proceed?"
    Options:
      - "Apply auto-fixes automatically"
      - "Show me the issues first"
      - "Cancel generation"

  IF user selects "Apply auto-fixes":
    Apply all auto-fix suggestions
    Re-run validation

    IF still failing:
      Report: "Auto-fixes applied but issues remain"
      Display remaining issues
      Require manual intervention
    ELSE:
      PASS: "✅ Auto-fixes applied successfully"
      Proceed to write

  ELSE IF user selects "Show me issues":
    Display full validation report
    AskUserQuestion for next action

  ELSE:
    HALT: "Generation cancelled"
    Return validation report

ELSE IF status == PASS WITH WARNINGS:
  Report: "⚠️ Passed with [count] warnings"
  Proceed to write

ELSE IF status == PASS:
  Report: "✅ All checks passed"
  Proceed to write
```
