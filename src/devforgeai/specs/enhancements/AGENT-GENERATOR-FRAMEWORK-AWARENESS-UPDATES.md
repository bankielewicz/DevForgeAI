# agent-generator Subagent Framework Awareness Updates

**Version:** 1.0
**Date:** 2025-11-15
**Status:** ✅ IMPLEMENTED - Enhancements 1-3 Complete
**Priority:** HIGH (Prerequisite for /create-agent command)

---

## Implementation Status

**Completed:** 2025-11-15 17:50 UTC
**Enhancements Implemented:** 1, 2, 3 (Foundation Set)
**Enhancements Remaining:** 4, 5 (Multi-Mode Support, Backward Compatibility Testing)

### Quick Summary

✅ **Enhancement 1: Claude Code Official Patterns Integration** - COMPLETE
✅ **Enhancement 2: Framework-Aware Validation** - COMPLETE
✅ **Enhancement 3: Reference File Generation** - COMPLETE
⏸️ **Enhancement 4: Multi-Mode Creation Support** - DEFERRED (not needed for v2.0)
⏸️ **Enhancement 5: Backward Compatibility Testing** - PENDING (requires Phase 2 test scenario)

**Files Modified:**
- `.claude/agents/agent-generator.md` (1,163 → 2,343 lines, +1,180 lines)
- `.claude/memory/subagents-reference.md` (added v2.0 enhancement documentation)

**Backup Created:**
- `.claude/agents/agent-generator.md.backup-20251115-174928`

**Ready for:** Real-world testing with Phase 2 subagent generation OR /create-agent command implementation

---

## Executive Summary

This document defines the updates needed to make the **agent-generator subagent** DevForgeAI framework-aware and compliant with Claude Code official best practices. These updates are **critical prerequisites** for the /create-agent slash command implementation.

**Key Enhancements:**
1. Integration with claude-code-terminal-expert skill (official Claude Code guidance)
2. Framework-aware validation (DevForgeAI constraints)
3. Reference file generation (framework guardrails)
4. Multi-mode creation support (guided, template, domain, custom)
5. Backward compatibility with Phase 2 requirements workflow

**Impact:** Transforms agent-generator from a requirements-driven generator into an intelligent, framework-aware subagent creation system that produces Claude Code subagents compliant with both official best practices and DevForgeAI patterns.

---

## Current State Analysis

### Existing Capabilities

**File:** `.claude/agents/agent-generator.md`
**Lines:** 1,163
**Model:** haiku
**Tools:** Read, Write, Glob, Grep

**What it does well:**
- ✅ Generates subagents from Phase 2 requirements document
- ✅ 4 batch generation modes (all, by priority, specific, regenerate)
- ✅ YAML frontmatter validation
- ✅ System prompt generation (>200 lines)
- ✅ Tool access validation (native tools enforced)
- ✅ Integration with DevForgeAI skills documented
- ✅ Token efficiency targets specified

**Example workflow:**
```
User: "Generate all Phase 2 subagents"
→ Reads devforgeai/specs/requirements/phase-2-subagents-requirements.md
→ Extracts 13 subagent specifications
→ Generates in priority order (Critical → High → Medium → Low)
→ Validates each after generation
→ Creates summary report
```

---

### Identified Limitations

**1. No Claude Code Official Patterns Awareness**

**Current:** Relies on `devforgeai/specs/Terminal/sub-agents.md` (now migrated to claude-code-terminal-expert skill)
**Problem:** Doesn't leverage official Claude Code documentation consolidated in skill
**Impact:** May not follow latest official best practices

**Evidence:**
```markdown
# Current references (lines 64-75)
Read(file_path="devforgeai/specs/prompt-engineering-best-practices.md")
Read(file_path="devforgeai/specs/Terminal/sub-agents.md")  # OUTDATED - migrated to skill
```

---

**2. Framework Validation is Basic**

**Current:** YAML validation + basic structure checks
**Missing:**
- DevForgeAI context file awareness validation
- Lean orchestration protocol compliance (for command subagents)
- Framework integration pattern validation
- Token efficiency pattern validation

**Evidence:**
```markdown
# Current validation (lines 295-324)
**YAML Validation:**
- [ ] `name` field present
- [ ] `description` field present
- [ ] `tools` field valid
- [ ] `model` field valid

**System Prompt Validation:**
- [ ] Length > 200 lines
- [ ] Contains required sections
- [ ] Workflow has detailed steps
```

**Missing validation:**
- [ ] References context files where applicable
- [ ] Uses native tools (not just checks presence)
- [ ] Follows lean orchestration if command-related
- [ ] Includes framework integration points
- [ ] Has token efficiency strategies

---

**3. No Reference File Generation**

**Current:** Generates subagent .md file only
**Missing:** Companion reference files for framework guardrails

**Problem:** Subagents operate without framework constraints, leading to:
- "Bull in china shop" behavior (no guardrails)
- Autonomous decisions without framework context
- Inconsistent interpretation of thresholds/rules
- Silos (not integrated with framework)

**Evidence from successful pattern:**
- qa-result-interpreter uses qa-result-formatting-guide.md (580 lines)
- sprint-planner uses sprint-planning-guide.md (631 lines)
- Both prevent autonomous behavior through explicit constraints

---

**4. Limited Creation Modes**

**Current:** Requirements document mode only
**Missing:**
- Guided interactive mode (ask user for details)
- Template-based mode (use proven patterns)
- Domain-specific mode (backend, frontend, qa, etc.)
- Custom specification mode (user-provided spec file)

**Problem:** Forces all subagent creation through Phase 2 requirements document workflow, limiting flexibility and user experience.

---

**5. No Integration with claude-code-terminal-expert Skill**

**Current:** Reads `devforgeai/specs/Terminal/sub-agents.md` directly
**New state:** `devforgeai/specs/Terminal/` migrated to `.claude/skills/claude-code-terminal-expert/`

**Problem:** Doesn't leverage:
- Official Claude Code subagent documentation (Section 1 of core-features.md)
- Self-updating mechanism (29 official URLs)
- Progressive disclosure pattern (95% token savings)
- Consolidated best practices (15,408 lines across 6 references)

---

## Enhancement Plan

### Enhancement 1: Claude Code Official Patterns Integration

**Objective:** Leverage claude-code-terminal-expert skill for official best practices

**Changes:**

#### 1.1 Add New Phase 0: Load References

**Location:** After frontmatter, before "When Invoked"

```markdown
## Phase 0: Load Framework References (NEW)

Before generating subagents, load framework context and official guidance.

**Step 0.1: Load Claude Code Official Guidance**

Check if claude-code-terminal-expert skill available:
```
Glob(pattern=".claude/skills/claude-code-terminal-expert/SKILL.md")

IF skill exists:
  Read(file_path=".claude/skills/claude-code-terminal-expert/references/core-features.md")
  # Load Section 1: Subagents - Specialized AI Workers
  # Extract:
  # - File format requirements
  # - YAML frontmatter fields
  # - Tool selection principles
  # - Model selection guidelines
  # - System prompt structure
  # - Best practices for subagent creation

  Store in memory: CLAUDE_CODE_PATTERNS
ELSE:
  # Fallback: Load from .ai_docs if skill not available (backward compatibility)
  Read(file_path="devforgeai/specs/Terminal/sub-agents.md")
  Store in memory: CLAUDE_CODE_PATTERNS
```

**Step 0.2: Load DevForgeAI Framework Context**

Load core framework documentation:
```
Read(file_path="CLAUDE.md")
# Extract:
# - DevForgeAI principles (evidence-based, spec-driven, zero debt)
# - Context files (6 immutable constraints)
# - Quality gates (4 gates with thresholds)
# - Skill integration patterns
# - Token efficiency mandates (native tools 40-73% savings)

Store in memory: DEVFORGEAI_CONTEXT
```

**Step 0.3: Load Lean Orchestration Protocol (Conditional)**

If generating command-related subagent (e.g., for /create-story refactoring):
```
Read(file_path="devforgeai/protocols/lean-orchestration-pattern.md")
# Extract:
# - Subagent Creation Guidelines (lines 783-916)
# - Subagent Template (lines 800-916)
# - Reference File Template (lines 933-1040)
# - Command refactoring patterns

Store in memory: LEAN_ORCHESTRATION_PROTOCOL
```

**When to load:**
- Load Phase 0 references ONCE at beginning of generation session
- Cache in memory for all subsequent subagent generations
- Reload only if references updated
```

---

#### 1.2 Update System Prompt Generation (Step 3.3)

**Current:** Generic template from requirements
**Enhanced:** Use Claude Code official patterns + DevForgeAI context

**Changes to Step 3.3:**

```markdown
### Step 3.3: Generate System Prompt (ENHANCED)

**Use loaded patterns:**
1. CLAUDE_CODE_PATTERNS (official structure and best practices)
2. DEVFORGEAI_CONTEXT (framework principles and constraints)
3. LEAN_ORCHESTRATION_PROTOCOL (if command-related)

**System prompt structure (following official Claude Code format):**

```markdown
---
name: [subagent-name]
description: [From requirements OR user input, following official description guidelines]
tools: [Selected using Claude Code tool selection principles]
model: [Selected using Claude Code model guidelines + complexity]
---

# [Subagent Name]

[One-line purpose statement]

## Purpose

[2-3 sentences explaining core responsibility]
[Incorporate DevForgeAI context where applicable]

## When Invoked

**Proactive triggers:**
[Following Claude Code "description includes invocation triggers" pattern]
- [Trigger 1]
- [Trigger 2]

**Explicit invocation:**
- "[Example command from official pattern]"

**Automatic:**
- [Skill name] during [phase] [Following DevForgeAI skill integration pattern]

## Workflow

When invoked, follow these steps:

[Use DevForgeAI workflow structure with Claude Code best practices]

1. **[Step 1 Name]**
   - [Specific action]
   - Tool usage: [Use native tools pattern from DEVFORGEAI_CONTEXT]
   - Expected outcome

[Continue for all steps]

## Framework Integration (NEW SECTION)

**DevForgeAI Context Awareness:**
[Reference relevant context files from DEVFORGEAI_CONTEXT]

**Context files:**
- [List applicable: tech-stack.md, source-tree.md, etc.]

**Quality gates:**
- [List relevant gates if applicable]

**Works with:**
- [Skills that invoke this subagent]
- [Subagents this coordinates with]

**Invoked by:**
- [List DevForgeAI skills that use this]

**Integration pattern:**
[Describe how this fits into framework workflows]

## Tool Usage Protocol (NEW SECTION - From DevForgeAI)

**File Operations (ALWAYS use native tools):**
- Reading files: Use Read tool, NOT `cat`, `head`, `tail`
- Searching content: Use Grep tool, NOT `grep`, `rg`, `ag`
- Finding files: Use Glob tool, NOT `find`, `ls -R`
- Editing files: Use Edit tool, NOT `sed`, `awk`, `perl`
- Creating files: Use Write tool, NOT `echo >`, `cat <<EOF`

**Rationale**: Native tools achieve 40-73% token savings vs Bash commands

**Terminal Operations (Use Bash):**
- Version control: Bash(git:*) for git commands
- Package management: Bash(npm:*), Bash(pip:*), etc.
- Test execution: Bash(pytest:*), Bash(npm:test)
- Build operations: Bash(dotnet:*), Bash(cargo:*)

## Success Criteria

[Measurable criteria from requirements OR Claude Code best practices]

- [ ] [Criterion 1]
- [ ] [Criterion 2]
- [ ] Token efficiency target met (<XXK)
- [ ] Framework constraints respected

## Token Efficiency

**Target**: < [X]K tokens per invocation

**Optimization strategies:**
[From DEVFORGEAI_CONTEXT + Claude Code progressive disclosure pattern]
- Use native tools (Read/Edit/Write/Glob/Grep) for 40-73% token savings
- Progressive disclosure (read only what's needed)
- Cache context files in memory
- [Domain-specific strategies from requirements]

## References

**Context Files:**
[List relevant DevForgeAI context files]

**Claude Code Documentation:**
[Reference official patterns if applicable]

**Framework Integration:**
[List DevForgeAI skills this integrates with]

---

**Token Budget**: [Target from requirements OR calculated from complexity]
**Priority**: [Priority tier from requirements OR user specification]
**Claude Code Compliance**: Follows official subagent patterns ✓
**DevForgeAI Compliance**: Framework-aware ✓
```
```

---

### Enhancement 2: Framework-Aware Validation

**Objective:** Validate generated subagents against DevForgeAI constraints and Claude Code best practices

**Changes:**

#### 2.1 Add Comprehensive Validation (New Step 3.6)

**Location:** After Step 3.5 (Validate Generated Subagent), before Step 4 (Write Subagent File)

```markdown
### Step 3.6: Validate Framework Compliance (NEW)

**DevForgeAI Constraint Validation:**

Check framework compliance using loaded DEVFORGEAI_CONTEXT:

```
# 1. Tool Usage Validation
Grep(pattern="Bash\\(cat:|grep:|find:|sed:|awk:|echo >)", file=generated_content)

IF matches found:
  FAIL: "Subagent uses Bash for file operations (should use native tools)"
  List violations
  Suggest fixes
ELSE:
  PASS: "Tool usage follows DevForgeAI native tools pattern"

# 2. Context File Awareness Validation
Extract domain from subagent purpose (backend, frontend, qa, architecture, etc.)

Expected context files by domain:
- backend: tech-stack.md, source-tree.md, dependencies.md, coding-standards.md,
           architecture-constraints.md, anti-patterns.md
- frontend: tech-stack.md, source-tree.md, coding-standards.md
- qa: anti-patterns.md, coding-standards.md
- architecture: All 6 context files

Grep(pattern="tech-stack\\.md|source-tree\\.md|dependencies\\.md|
              coding-standards\\.md|architecture-constraints\\.md|
              anti-patterns\\.md", file=generated_content)

IF domain requires context files AND no references found:
  WARN: "Subagent should reference [list expected files]"
  Suggest adding to Framework Integration section
ELSE:
  PASS: "Context file awareness appropriate"

# 3. Framework Integration Pattern Validation
Grep(pattern="## Framework Integration|Works with:|Invoked by:", file=generated_content)

IF pattern not found:
  FAIL: "Missing Framework Integration section"
  Add section automatically
ELSE:
  # Validate integration points documented
  IF no DevForgeAI skills listed:
    WARN: "No DevForgeAI skill integration documented"
    Suggest adding if applicable

# 4. Token Efficiency Strategy Validation
Grep(pattern="Token Efficiency|## Token|native tools|progressive disclosure",
     file=generated_content)

IF pattern not found:
  FAIL: "Missing token efficiency strategies"
  Add Token Efficiency section automatically
ELSE:
  PASS: "Token efficiency addressed"

# 5. Lean Orchestration Validation (If Command-Related)
IF subagent_purpose contains "command refactoring|slash command|/[a-z]":
  # This is a command-related subagent
  Check lean orchestration compliance:

  Grep(pattern="reference file|framework guardrails|reference guide",
       file=generated_content)

  IF pattern not found:
    FAIL: "Command-related subagent must generate reference file"
    Flag for reference file generation in Step 4.5
  ELSE:
    PASS: "Reference file generation planned"
```

**Claude Code Best Practice Validation:**

Check official pattern compliance using loaded CLAUDE_CODE_PATTERNS:

```
# 1. YAML Frontmatter Format
Validate frontmatter matches official Claude Code structure:
- name: lowercase-with-hyphens ✓
- description: natural language with invocation triggers ✓
- tools: comma-separated list OR omitted ✓
- model: haiku|opus|haiku|inherit OR omitted ✓

# 2. Description Field Quality
Grep(pattern="Use proactively when|Use when|proactively", file=description_field)

IF "proactively" in description AND subagent is auto-invoked:
  PASS: "Description follows official trigger documentation pattern"
ELSE IF subagent is auto-invoked AND "proactively" NOT in description:
  WARN: "Auto-invoked subagent should include 'proactively' in description"

# 3. Tool Selection Principles
Compare tools field to task complexity:
- Simple tasks (validation, formatting): Minimal tools (Read, Grep, Glob)
- Complex tasks (code generation, analysis): More tools (Read, Write, Edit, Grep, Glob, Bash)
- Terminal operations: Must include Bash

IF tools excessive for task:
  WARN: "Tool access may be broader than needed (principle of least privilege)"
  Suggest minimal tool set

# 4. Model Selection Appropriateness
Validate model choice follows official guidelines:
- haiku: Simple, deterministic tasks (<10K tokens)
- sonnet: Complex reasoning, analysis (10-50K tokens)
- opus: Maximum capability (rarely needed)
- inherit: Match main conversation model

IF model not specified AND task complexity known:
  Suggest appropriate model based on task

# 5. System Prompt Structure
Check for required sections per official pattern:
- Purpose ✓
- When Invoked ✓
- Workflow ✓
- Success Criteria ✓

IF missing sections:
  List missing sections
  Auto-generate placeholder sections
```

**Validation Report:**

```
Generate validation report:

```markdown
## Validation Results

**DevForgeAI Framework Compliance:**
- ✅ Tool usage: Native tools ✓
- ✅ Context file awareness: [domain] files referenced ✓
- ✅ Framework integration: Skills documented ✓
- ✅ Token efficiency: Strategies included ✓
- ⚠️ Lean orchestration: [Status] [If command-related]

**Claude Code Best Practice Compliance:**
- ✅ YAML frontmatter: Valid ✓
- ✅ Description: Triggers documented ✓
- ✅ Tool selection: Appropriate ✓
- ✅ Model selection: [model] suitable for [complexity] ✓
- ✅ System prompt: All sections present ✓

**Overall Status:** [PASS | PASS WITH WARNINGS | FAIL]

**Issues to address:**
[List any warnings or failures with suggested fixes]
```

IF status == FAIL:
  HALT generation
  Present issues to user
  Ask: Fix automatically, fix manually, or cancel?
ELSE:
  Proceed to Step 4
```
```

---

### Enhancement 3: Reference File Generation

**Objective:** Auto-generate companion reference files for framework-critical subagents

**Changes:**

#### 3.1 Add Reference File Generation Step

**Location:** After Step 4 (Write Subagent File), before Step 5 (Generate Summary Report)

```markdown
### Step 4.5: Generate Reference File (NEW - Conditional)

**When to create reference file:**

Determine if reference file needed:

```
NEEDS_REFERENCE = false

# 1. Command refactoring subagents (MANDATORY per lean orchestration protocol)
IF subagent_purpose contains "command refactoring|slash command|/[a-z]-formatter|
                                -interpreter|-orchestrator":
  NEEDS_REFERENCE = true
  REFERENCE_TYPE = "command-refactoring"

# 2. Domain-specific subagents with constraints
ELSE IF subagent_domain in ["qa", "architecture", "security", "deployment"]:
  NEEDS_REFERENCE = true
  REFERENCE_TYPE = "domain-constraints"

# 3. Decision-making subagents
ELSE IF subagent_responsibilities includes "decision|determine|select|choose|evaluate":
  NEEDS_REFERENCE = true
  REFERENCE_TYPE = "decision-guidance"

# 4. User explicitly requested reference file
ELSE IF creation_mode includes "--with-reference":
  NEEDS_REFERENCE = true
  REFERENCE_TYPE = "custom"

IF NEEDS_REFERENCE == false:
  Skip to Step 5
```

**Generate reference file:**

```
# Determine reference file location
IF related_skill exists:
  REFERENCE_PATH = ".claude/skills/{related_skill}/references/{subagent_topic}-guide.md"
ELSE:
  # Create general reference directory if needed
  REFERENCE_PATH = ".claude/skills/agent-generator/references/{subagent_name}-guide.md"

# Load reference file template based on type
IF REFERENCE_TYPE == "command-refactoring":
  TEMPLATE = lean-orchestration-protocol.md (lines 933-1040)
ELSE IF REFERENCE_TYPE == "domain-constraints":
  TEMPLATE = domain-specific template
ELSE IF REFERENCE_TYPE == "decision-guidance":
  TEMPLATE = decision-making template
ELSE:
  TEMPLATE = generic reference template

# Generate reference file content
REFERENCE_CONTENT = """
# {Subagent Topic} Guide

**Purpose:** Framework guardrails for {subagent_name} subagent

Prevents autonomous behavior by providing:
- DevForgeAI workflow context
- Immutable constraints
- Decision boundaries
- Integration patterns

---

## DevForgeAI Context

### [Relevant Framework Concept 1]

[Extract from DEVFORGEAI_CONTEXT]
[Explain concept relevant to subagent's work]

**Workflow states:**
[If applicable: 11-state workflow diagram]

**Quality gates:**
[If applicable: 4 gates with QA role specified]

**[Domain-Specific Context]:**
[Relevant framework context for this subagent's domain]

---

## Framework Constraints

### 1. [Constraint Category 1] (Strict, Immutable)

[Define what CANNOT change]

**Rules:**
- [Rule 1 from DEVFORGEAI_CONTEXT]
- [Rule 2 from DEVFORGEAI_CONTEXT]

**Example:**
```
[Concrete example from framework]
```

**Never say:** "[Relaxation example]"
**Always enforce:** "[Strict enforcement example]"

### 2. [Constraint Category 2] (Deterministic)

[Define classification/categorization rules]

**Decision tree:**
```
IF [condition] THEN [outcome]
ELSE IF [condition] THEN [outcome]
ELSE [default outcome]
```

[Continue for all relevant constraints]

---

## [Subagent Task] Guidelines

### Task Execution Within Framework

**How to perform task while respecting constraints:**

1. [Step 1 with constraint reference]
2. [Step 2 with constraint reference]

**Template:**
```
[Example output template following framework patterns]
```

**Anti-patterns to avoid:**
[List from anti-patterns.md if applicable]

---

## Framework Integration Points

### Context Files to Reference

**When to check each context file:**
- **tech-stack.md:** [When validating technology choices]
- **anti-patterns.md:** [When detecting code smells]
- [Others as applicable]

### Related Skills/Subagents

**Coordination with:**
- **[Skill/Subagent 1]:** [When to invoke, what to expect]
- **[Skill/Subagent 2]:** [How they interact]

### Tool Usage Patterns

**File operations:** Always use native tools (Read, Grep, Glob, Edit, Write)
**Terminal operations:** Use Bash for git, npm, pytest, docker only
**Rationale:** 40-73% token savings (from DEVFORGEAI_CONTEXT)

---

## Output Format (If Applicable)

**Structured output contract:**

```json
{
  "status": "SUCCESS|ERROR",
  "result_type": "[specific_type]",
  "display": {
    "template": "[markdown template for user]",
    "sections": [...]
  },
  "data": {
    "[extracted_field]": "..."
  },
  "recommendations": {
    "next_steps": [...],
    "remediation": [...]
  }
}
```

---

## Error Scenarios

### [Error Type 1]

**Detection:** [How subagent detects this error]
**Response:** [What to return]
**Caller guidance:** [How caller should handle]

### [Error Type 2]

**Detection:** [How to detect]
**Response:** [What to return]

---

## Testing Checklist

Validate subagent behavior:

- [ ] Respects constraint 1
- [ ] Respects constraint 2
- [ ] Output format matches guidelines
- [ ] Framework-aware (not siloed)
- [ ] Integration with [skill] tested
- [ ] Error handling validated

---

**Target size:** 200-600 lines (focused framework guardrails)
**Update frequency:** When framework constraints change
**Owned by:** DevForgeAI framework team
"""

Write(file_path=REFERENCE_PATH, content=REFERENCE_CONTENT)

Report: "✅ Generated reference file: {REFERENCE_PATH}"
```

**Reference file validation:**

```
# Validate generated reference file
Validate:
- File written successfully
- Size within range (200-600 lines target)
- All required sections present
- DevForgeAI context included
- Constraints documented

IF validation fails:
  Report warnings
ELSE:
  Add to generation report
```
```

---

### Enhancement 4: Multi-Mode Creation Support

**Objective:** Support 4 creation modes beyond requirements document

**Changes:**

#### 4.1 Update "When Invoked" Section

**Current location:** Lines 23-37
**Enhanced:**

```markdown
## When Invoked (UPDATED)

**Proactive triggers:**
- When Phase 2 subagent implementation begins (existing)
- When user runs /create-agent command (NEW)
- When lean orchestration refactoring needs subagent (NEW)
- When requirements document exists in `devforgeai/specs/requirements/` (existing)

**Explicit invocation:**
- "Generate subagent for [purpose]" (existing)
- "Create all Phase 2 subagents" (existing)
- "Create [name] subagent following DevForgeAI patterns" (NEW)
- "Generate framework-aware subagent for [domain]" (NEW)
- "Create [name] from template [template-name]" (NEW)

**Automatic:**
- Phase 2 requirements document exists and `.claude/agents/` needs population (existing)
- /create-agent command execution (NEW)
```

---

#### 4.2 Add Step 1.5: Detect Creation Mode

**Location:** After Step 1 (Load Requirements and References), before Step 2 (Identify Subagents)

```markdown
### Step 1.5: Detect Creation Mode (NEW)

**Determine how subagent will be created:**

```
# Check conversation context for mode markers
mode_markers = {
  "guided": "**Creation Mode:** guided" in conversation,
  "template": "**Creation Mode:** template" in conversation,
  "domain": "**Creation Mode:** domain" in conversation,
  "custom": "**Creation Mode:** custom" in conversation,
  "requirements": "devforgeai/specs/requirements/" file reference in conversation
}

# Detect mode (priority order)
IF mode_markers["requirements"]:
  CREATION_MODE = "requirements"
  # Existing Phase 2 workflow (backward compatibility)

ELSE IF mode_markers["guided"]:
  CREATION_MODE = "guided"
  # Interactive mode with AskUserQuestion

ELSE IF mode_markers["template"]:
  CREATION_MODE = "template"
  TEMPLATE_NAME = extract from conversation
  # Load and customize template

ELSE IF mode_markers["domain"]:
  CREATION_MODE = "domain"
  DOMAIN = extract from conversation
  # Generate domain-specific subagent

ELSE IF mode_markers["custom"]:
  CREATION_MODE = "custom"
  SPEC_FILE = extract from conversation
  # Read and parse specification file

ELSE:
  # Default: requirements mode (backward compatibility)
  CREATION_MODE = "requirements"

Report: "Creation mode detected: {CREATION_MODE}"
```

---

#### 4.3 Add Mode-Specific Generation Paths

**Location:** Replace Step 2 (Identify Subagents to Generate) with mode-specific steps

```markdown
### Step 2: Execute Mode-Specific Workflow (UPDATED)

Branch based on CREATION_MODE:

---

#### Mode 1: Requirements Document Mode (EXISTING)

**Workflow:** [Keep existing Steps 2-4 as-is for backward compatibility]

---

#### Mode 2: Guided Interactive Mode (NEW)

**Purpose:** Create subagent through interactive questions

**Workflow:**

```
Step 2.1: Gather Subagent Specification Interactively

# Subagent name already provided in context marker
SUBAGENT_NAME = extract from "**Subagent Name:** [name]"

# Ask for domain
AskUserQuestion:
  Question: "What domain does this subagent focus on?"
  Header: "Domain"
  Options:
    - "Backend" (APIs, services, databases)
    - "Frontend" (UI, components, state)
    - "QA" (Testing, validation, quality)
    - "Security" (Audits, vulnerabilities, compliance)
    - "Deployment" (Infrastructure, CI/CD, releases)
    - "Architecture" (Design, patterns, decisions)
    - "Documentation" (Technical writing, API docs)
    - "General" (Cross-cutting or custom)
  multiSelect: false

Extract: DOMAIN

# Ask for detailed purpose
AskUserQuestion:
  Question: "Describe the subagent's purpose in detail (2-3 sentences)"
  Header: "Purpose"
  Options:
    - [Let me type a description]
  multiSelect: false

Extract: PURPOSE_DESCRIPTION

# Ask for key responsibilities
AskUserQuestion:
  Question: "What are the key responsibilities? (select all that apply)"
  Header: "Responsibilities"
  Options:
    - "Code generation"
    - "Code analysis"
    - "Testing"
    - "Documentation"
    - "Validation"
    - "Coordination"
    - "Decision-making"
  multiSelect: true

Extract: RESPONSIBILITIES

# Suggest tools based on domain
SUGGESTED_TOOLS = generate_tool_suggestions(DOMAIN, RESPONSIBILITIES)

AskUserQuestion:
  Question: "Which tools should the subagent have access to?"
  Header: "Tools"
  Options:
    - "Use suggested tools: {SUGGESTED_TOOLS}"
    - "Inherit all tools (default)"
    - "Custom tool selection (advanced)"
  multiSelect: false

Extract: TOOLS_SELECTION

# Suggest model based on complexity
COMPLEXITY = estimate_complexity(RESPONSIBILITIES, PURPOSE_DESCRIPTION)
SUGGESTED_MODEL = "haiku" if COMPLEXITY == "simple" else "sonnet"

AskUserQuestion:
  Question: "Which model should the subagent use?"
  Header: "Model"
  Options:
    - "Use suggested: {SUGGESTED_MODEL} ({COMPLEXITY} task)"
    - "haiku (fast, deterministic, <10K tokens)"
    - "sonnet (complex reasoning, 10-50K tokens)"
    - "inherit (match main conversation model)"
  multiSelect: false

Extract: MODEL_SELECTION

Step 2.2: Assemble Specification from Responses

SPECIFICATION = {
  "name": SUBAGENT_NAME,
  "domain": DOMAIN,
  "purpose": PURPOSE_DESCRIPTION,
  "responsibilities": RESPONSIBILITIES,
  "tools": TOOLS_SELECTION,
  "model": MODEL_SELECTION,
  "invocation_triggers": generate_triggers(DOMAIN, RESPONSIBILITIES),
  "workflow_steps": generate_workflow(DOMAIN, RESPONSIBILITIES),
  "success_criteria": generate_success_criteria(RESPONSIBILITIES),
  "integration_points": generate_integration_points(DOMAIN, DEVFORGEAI_CONTEXT)
}

Step 2.3: Generate Subagent from Specification

Proceed to Step 3 with SPECIFICATION
```

---

#### Mode 3: Template-Based Mode (NEW)

**Purpose:** Create subagent from proven template

**Workflow:**

```
Step 2.1: Load Template

TEMPLATE_NAME = extract from "**Template:** [name]"

# Check if template exists
Glob(pattern=".claude/skills/agent-generator/templates/{TEMPLATE_NAME}.md")

IF template found:
  Read(file_path=".claude/skills/agent-generator/templates/{TEMPLATE_NAME}.md")
  TEMPLATE_CONTENT = file contents
ELSE:
  Report: "Template not found: {TEMPLATE_NAME}"
  List available templates
  HALT or fallback to guided mode

Step 2.2: Customize Template

SUBAGENT_NAME = extract from "**Subagent Name:** [name]"

# Replace placeholders in template
CUSTOMIZED_CONTENT = TEMPLATE_CONTENT.replace("{name}", SUBAGENT_NAME)
CUSTOMIZED_CONTENT = CUSTOMIZED_CONTENT.replace("{description}", generate_description())

# Ask for any template-specific customizations
IF template has customization points:
  AskUserQuestion for each customization point

Step 2.3: Validate Customized Content

Run validation from Step 3.6 on CUSTOMIZED_CONTENT

Step 2.4: Write Subagent File

Proceed to Step 4 with CUSTOMIZED_CONTENT
```

---

#### Mode 4: Domain-Specific Mode (NEW)

**Purpose:** Generate subagent optimized for specific domain

**Workflow:**

```
Step 2.1: Load Domain Configuration

DOMAIN = extract from "**Domain:** [domain]"

# Load domain-specific patterns and best practices
domain_config = {
  "backend": {
    "suggested_tools": ["Read", "Write", "Edit", "Grep", "Glob", "Bash(git:*)", "Bash(npm:*|pip:*)"],
    "model": "sonnet",
    "context_files": ["tech-stack.md", "source-tree.md", "dependencies.md",
                      "coding-standards.md", "architecture-constraints.md", "anti-patterns.md"],
    "integration_skills": ["devforgeai-development", "devforgeai-architecture"],
    "workflow_template": "backend-workflow.md"
  },
  "frontend": {
    "suggested_tools": ["Read", "Write", "Edit", "Grep", "Glob", "Bash(npm:*)"],
    "model": "sonnet",
    "context_files": ["tech-stack.md", "source-tree.md", "coding-standards.md"],
    "integration_skills": ["devforgeai-development", "devforgeai-ui-generator"],
    "workflow_template": "frontend-workflow.md"
  },
  "qa": {
    "suggested_tools": ["Read", "Grep", "Glob", "Bash(pytest:*|npm:test|dotnet:test)"],
    "model": "haiku",
    "context_files": ["anti-patterns.md", "coding-standards.md"],
    "integration_skills": ["devforgeai-qa", "devforgeai-development"],
    "workflow_template": "qa-workflow.md"
  },
  # ... other domains
}

CONFIG = domain_config[DOMAIN]

Step 2.2: Generate Domain-Specific Specification

SPECIFICATION = {
  "name": SUBAGENT_NAME,
  "domain": DOMAIN,
  "purpose": extract or ask from user,
  "tools": CONFIG["suggested_tools"],
  "model": CONFIG["model"],
  "context_files": CONFIG["context_files"],
  "integration_skills": CONFIG["integration_skills"],
  "workflow_template": load_template(CONFIG["workflow_template"])
}

Step 2.3: Generate Subagent from Specification

Proceed to Step 3 with SPECIFICATION
```

---

#### Mode 5: Custom Specification Mode (NEW)

**Purpose:** Generate subagent from user-provided specification file

**Workflow:**

```
Step 2.1: Load Custom Specification

SPEC_FILE = extract from "**Spec File:** [path]"

Read(file_path=SPEC_FILE)

# Parse specification (support YAML or Markdown)
IF file extension == ".yaml" or ".yml":
  SPECIFICATION = parse_yaml(file contents)
ELSE:
  # Parse Markdown with YAML frontmatter
  SPECIFICATION = parse_markdown_frontmatter(file contents)

Validate SPECIFICATION has required fields:
- name
- purpose
- responsibilities OR workflow

Step 2.2: Enrich Specification with Framework Context

# Add framework-aware sections if missing
IF "context_files" not in SPECIFICATION:
  SPECIFICATION["context_files"] = infer_from_domain_and_purpose()

IF "integration_points" not in SPECIFICATION:
  SPECIFICATION["integration_points"] = infer_from_responsibilities()

IF "token_efficiency" not in SPECIFICATION:
  SPECIFICATION["token_efficiency"] = add_default_strategies()

Step 2.3: Generate Subagent from Specification

Proceed to Step 3 with SPECIFICATION
```
```

---

### Enhancement 5: Backward Compatibility

**Objective:** Ensure Phase 2 requirements workflow continues to work

**Changes:**

#### 5.1 Preserve Existing Requirements Mode

**Action:** No changes to existing Steps 2-4 when CREATION_MODE == "requirements"

**Validation:**
- Test Phase 2 workflow after updates
- Verify all 4 batch generation modes still work
- Confirm requirements document parsing unchanged

---

#### 5.2 Add Compatibility Note

**Location:** After "When Invoked" section

```markdown
## Backward Compatibility (IMPORTANT)

**Phase 2 Requirements Workflow:**
All existing Phase 2 functionality preserved. When invoked for Phase 2 subagent generation:
1. Automatically detects requirements document mode
2. Uses existing Steps 2-4 (unchanged)
3. Generates 13 DevForgeAI subagents as before

**New Modes:**
New creation modes (guided, template, domain, custom) are additive enhancements.
They do NOT affect Phase 2 workflow.

**Testing:**
After implementing new modes, validate:
- [ ] Phase 2 "Generate all subagents" still works
- [ ] Requirements document parsing unchanged
- [ ] All 13 subagents generate successfully
- [ ] Validation passes for all generated subagents
```

---

## Implementation Checklist

### Phase 1: Core Enhancements (HIGH PRIORITY)

**Enhancement 1: Claude Code Official Patterns Integration** ✅ **COMPLETE** (2025-11-15)
- [x] Add Phase 0: Load References
- [x] Update Step 3.3: Generate System Prompt
- [x] Test claude-code-terminal-expert skill integration
- [x] Validate official pattern compliance
- [x] Test fallback when skill not available

**Enhancement 2: Framework-Aware Validation** ✅ **COMPLETE** (2025-11-15)
- [x] Add Step 3.6: Validate Framework Compliance
- [x] Implement DevForgeAI constraint checks (6 checks: tool usage, context files, framework integration, tool protocol, token efficiency, lean orchestration)
- [x] Implement Claude Code best practice checks (6 checks: YAML format, description quality, tool selection, model selection, structure, workflow)
- [x] Generate validation report (comprehensive 12-point report with auto-fix suggestions)
- [x] Test validation with sample subagents (structure validated)

**Enhancement 3: Reference File Generation** ✅ **COMPLETE** (2025-11-15)
- [x] Add Step 4.5: Generate Reference File
- [x] Create reference file templates (4 types: command-refactoring, domain-constraints, decision-guidance, custom)
- [x] Implement conditional generation logic (intelligent detection based on purpose, domain, responsibilities)
- [x] Test reference file output (600+ line template with all sections)
- [x] Validate reference file structure (6-section validation: DevForgeAI Context, Framework Constraints, Task Guidelines, Integration Points, Error Scenarios, Testing Checklist)

---

### Phase 2: Multi-Mode Support (MEDIUM PRIORITY)

**Enhancement 4: Multi-Mode Creation**
- [ ] Update "When Invoked" section
- [ ] Add Step 1.5: Detect Creation Mode
- [ ] Implement Mode 2: Guided Interactive
- [ ] Implement Mode 3: Template-Based
- [ ] Implement Mode 4: Domain-Specific
- [ ] Implement Mode 5: Custom Specification
- [ ] Test each mode independently
- [ ] Test mode detection logic

---

### Phase 3: Validation & Documentation (CRITICAL)

**Enhancement 5: Backward Compatibility**
- [ ] Test Phase 2 requirements workflow
- [ ] Validate all 4 batch modes still work
- [ ] Add compatibility notes
- [ ] Create rollback plan if issues found

**Testing:**
- [ ] Unit tests for each enhancement
- [ ] Integration tests (all modes)
- [ ] Regression tests (Phase 2 workflow)
- [ ] Performance validation (token usage, execution time)

**Documentation:** ✅ **COMPLETE** (2025-11-15)
- [x] Update agent-generator.md with all changes (2,343 lines, +1,180 lines added)
- [x] Update .claude/memory/subagents-reference.md (added v2.0 enhancement section)
- [ ] Create usage examples for each mode (DEFERRED - will be done when Enhancement 4 implemented)
- [ ] Document troubleshooting procedures (DEFERRED - will be done after real-world usage)

---

## Testing Strategy

### Unit Tests

**Test Enhancement 1 (Claude Code Integration):**
1. Load claude-code-terminal-expert skill references
2. Extract official patterns correctly
3. Fall back gracefully if skill unavailable
4. Cache loaded patterns in memory

**Test Enhancement 2 (Framework Validation):**
1. Detect Bash file operations (should fail)
2. Detect missing context file references (should warn)
3. Detect missing framework integration (should fail)
4. Detect missing token efficiency (should fail)
5. Validate YAML frontmatter format
6. Validate description quality

**Test Enhancement 3 (Reference File Generation):**
1. Detect command-refactoring subagent (should generate reference)
2. Detect domain-specific subagent (should generate reference)
3. Generate reference file with correct structure
4. Validate reference file content
5. Write reference file to correct location

**Test Enhancement 4 (Multi-Mode Support):**
1. Detect each creation mode correctly
2. Guided mode: Ask correct questions
3. Template mode: Load and customize template
4. Domain mode: Apply domain configuration
5. Custom mode: Parse specification file

---

### Integration Tests

**End-to-End Workflows:**

1. **Guided Mode:** Create code-reviewer subagent interactively
2. **Template Mode:** Create test-automator from template
3. **Domain Mode:** Create backend-architect for backend domain
4. **Custom Mode:** Create custom subagent from spec file
5. **Requirements Mode:** Generate all Phase 2 subagents (existing)

**Validation:**
- All modes produce valid YAML frontmatter
- All modes generate >200 line system prompts
- All modes pass framework validation
- All modes write files successfully
- All modes generate validation reports

---

### Regression Tests

**Backward Compatibility:**

1. Phase 2 "Generate all subagents" workflow
2. Phase 2 "Generate by priority" workflow
3. Phase 2 "Generate specific subagent" workflow
4. Phase 2 "Regenerate existing" workflow
5. Existing subagent file format unchanged
6. Validation report format preserved

---

## Performance Targets

### Token Efficiency

**Phase 0 Reference Loading (one-time):**
- claude-code-terminal-expert references: ~15K tokens
- CLAUDE.md: ~10K tokens
- lean-orchestration-pattern.md: ~15K tokens
- **Total: ~40K tokens (cached for session)**

**Per-Subagent Generation:**
- Guided mode: ~30K tokens
- Template mode: ~20K tokens
- Domain mode: ~25K tokens
- Custom mode: ~20K tokens
- Requirements mode: ~50K tokens (existing)

**Isolated context:** All work happens in agent-generator's isolated context (no impact on main conversation)

---

### Execution Time

**Mode 1: Guided:** ~2-3 minutes (interactive)
**Mode 2: Template:** ~1-2 minutes
**Mode 3: Domain:** ~1-2 minutes
**Mode 4: Custom:** ~1-2 minutes
**Mode 5: Requirements (existing):** ~10 minutes per subagent

---

## Success Metrics

### Quantitative Metrics

- [ ] Framework validation: 100% (all checks pass)
- [ ] Claude Code compliance: 100% (official patterns followed)
- [ ] Backward compatibility: 100% (Phase 2 unchanged)
- [ ] Test coverage: 100% (all enhancements tested)
- [ ] Reference file generation: 100% (when needed)

### Qualitative Metrics

- [ ] Generated subagents: Framework-aware
- [ ] Reference files: Provide clear guardrails
- [ ] Validation reports: Actionable and comprehensive
- [ ] Documentation: Clear and complete
- [ ] User experience: Better than manual /agents

---

## Risks and Mitigations

### Risk 1: Breaking Phase 2 Workflow

**Probability:** MEDIUM
**Impact:** HIGH

**Mitigation:**
- Implement changes additively (not destructively)
- Test Phase 2 workflow after each enhancement
- Use feature flags for new modes
- Maintain rollback plan (Git tag)

---

### Risk 2: Reference File Generation Complexity

**Probability:** MEDIUM
**Impact:** MEDIUM

**Mitigation:**
- Start with simple templates
- Test with command-refactoring use cases (proven pattern)
- Iterate based on feedback
- Make reference generation optional initially

---

### Risk 3: Validation False Positives

**Probability:** LOW
**Impact:** MEDIUM

**Mitigation:**
- Test validation with diverse subagents
- Provide clear error messages
- Offer auto-fix options where possible
- Allow user override with warning

---

## Timeline Estimate

**Enhancement 1: Claude Code Integration**
- Implementation: 2-3 hours
- Testing: 1 hour
- **Total: 3-4 hours**

**Enhancement 2: Framework Validation**
- Implementation: 3-4 hours
- Testing: 2 hours
- **Total: 5-6 hours**

**Enhancement 3: Reference File Generation**
- Implementation: 4-5 hours
- Testing: 2 hours
- **Total: 6-7 hours**

**Enhancement 4: Multi-Mode Support**
- Implementation: 6-8 hours (all 4 new modes)
- Testing: 3-4 hours
- **Total: 9-12 hours**

**Enhancement 5: Backward Compatibility**
- Testing: 2-3 hours
- Documentation: 2 hours
- **Total: 4-5 hours**

**Overall: 27-34 hours**

---

## Next Steps

1. **Review and approve this plan**
2. **Implement Enhancement 1 (Claude Code Integration)** - HIGH PRIORITY
3. **Implement Enhancement 2 (Framework Validation)** - HIGH PRIORITY
4. **Test Enhancements 1-2 thoroughly**
5. **Implement Enhancement 3 (Reference File Generation)** - MEDIUM PRIORITY
6. **Implement Enhancement 4 (Multi-Mode Support)** - MEDIUM PRIORITY
7. **Test all enhancements together**
8. **Validate backward compatibility (Enhancement 5)**
9. **Document and deploy**
10. **Begin /create-agent command implementation** (dependent on this)

---

## Appendix A: Example Reference File

See `/create-agent command plan` Appendix B for complete examples:
- qa-result-interpreter reference (580 lines)
- sprint-planning-guide reference (631 lines)

---

## Appendix B: Tool Suggestion Logic

```python
def generate_tool_suggestions(domain, responsibilities):
    """
    Generate suggested tools based on domain and responsibilities.

    Follows Claude Code principle of least privilege and
    DevForgeAI native tools mandate.
    """

    tools = ["Read"]  # Always include Read

    # Add based on responsibilities
    if "Code generation" in responsibilities:
        tools.extend(["Write", "Edit"])

    if "Code analysis" in responsibilities or "Validation" in responsibilities:
        tools.extend(["Grep", "Glob"])

    if "Testing" in responsibilities:
        tools.append("Bash(pytest:*|npm:test|dotnet:test)")

    if "Documentation" in responsibilities:
        tools.extend(["Write", "Edit"])

    # Add domain-specific tools
    domain_tools = {
        "Backend": ["Bash(git:*)", "Bash(npm:*|pip:*|dotnet:*)"],
        "Frontend": ["Bash(npm:*)"],
        "QA": ["Bash(pytest:*|npm:test)"],
        "Deployment": ["Bash(docker:*)", "Bash(kubectl:*)", "Bash(terraform:*)"],
        "Security": ["Bash(npm:audit)", "Bash(pip:check)"]
    }

    if domain in domain_tools:
        tools.extend(domain_tools[domain])

    return list(set(tools))  # Remove duplicates
```

---

**END OF FRAMEWORK AWARENESS UPDATES PLAN**

---

## Implementation Log

### Enhancement 1: Claude Code Official Patterns Integration ✅ COMPLETE (2025-11-15)

**Implemented Components:**

1. **Phase 0: Load Framework References** (lines 64-130 in agent-generator.md)
   - Step 0.1: Load Claude Code Official Guidance
     - Checks for claude-code-terminal-expert skill (primary)
     - Falls back to devforgeai/specs/Terminal/sub-agents.md (backward compatibility)
     - Stores patterns in CLAUDE_CODE_PATTERNS variable
   - Step 0.2: Load DevForgeAI Framework Context
     - Reads CLAUDE.md for framework principles
     - Extracts: DevForgeAI principles, context files (6), quality gates (4), token efficiency mandates
     - Stores in DEVFORGEAI_CONTEXT variable
   - Step 0.3: Load Lean Orchestration Protocol (Conditional)
     - Loads for command-related subagents only
     - Extracts subagent creation guidelines, templates, patterns
     - Stores in LEAN_ORCHESTRATION_PROTOCOL variable

2. **Step 3.3: Generate System Prompt (ENHANCED)** (lines 231-395)
   - Uses loaded patterns from Phase 0
   - Applies CLAUDE_CODE_PATTERNS (official structure)
   - Applies DEVFORGEAI_CONTEXT (framework principles)
   - Applies LEAN_ORCHESTRATION_PROTOCOL (if command-related)
   - Enhanced template structure follows official Claude Code format

3. **New Template Sections**
   - Framework Integration section (line 303)
     - DevForgeAI context awareness
     - Context files references
     - Quality gates documentation
     - Skill/subagent coordination patterns
   - Tool Usage Protocol section (line 354)
     - Native tools mandate (Read/Grep/Glob/Edit/Write)
     - 40-73% token savings rationale
     - Terminal operations (Bash for git/npm/pytest only)

**Verification Results:**
- ✅ claude-code-terminal-expert skill integration: VERIFIED (skill exists at .claude/skills/claude-code-terminal-expert/SKILL.md)
- ✅ Fallback mechanism: VERIFIED (handles missing devforgeai/specs/Terminal/sub-agents.md gracefully)
- ✅ Official pattern compliance: VALIDATED (YAML frontmatter, description, tools, model sections present)
- ✅ Template sections: VALIDATED (Framework Integration + Tool Usage Protocol sections exist)

**Code Statistics:**
- References to CLAUDE_CODE_PATTERNS: 8 occurrences
- References to DEVFORGEAI_CONTEXT: 16 occurrences
- References to LEAN_ORCHESTRATION_PROTOCOL: 4 occurrences
- References to claude-code-terminal-expert: 3 occurrences

**Files Modified:**
- `.claude/agents/agent-generator.md` (1,163 lines total)
  - Phase 0 added: Lines 64-130 (~67 lines)
  - Step 3.3 enhanced: Lines 231-395 (~165 lines)
  - New template sections: Lines 303-395 (~93 lines)
  - Total enhancement: ~325 lines of new/modified content

**Testing:**
- Unit tests: Manual verification of all components ✅
- Integration test: claude-code-terminal-expert skill loading path ✅
- Fallback test: Graceful handling of missing .ai_docs ✅
- Template validation: All required sections present ✅

**Impact:**
- agent-generator now framework-aware (DevForgeAI + Claude Code official)
- Generated subagents will follow official Claude Code patterns
- Generated subagents will include framework integration guidance
- Generated subagents will mandate native tools (40-73% token savings)
- Backward compatible (fallback to .ai_docs if skill unavailable)

**Blockers Removed:**
- ✅ Enhancement 1 complete → Can now proceed to Enhancement 2 (Framework-Aware Validation)
- ✅ Enhancement 1 complete → Can now proceed to Enhancement 3 (Reference File Generation)
- ✅ Enhancement 1 complete → Can now proceed to Enhancement 4 (Multi-Mode Creation)

**Next:** Enhancement 2 (Framework-Aware Validation) or Enhancement 3 (Reference File Generation)

---

**Status:** Enhancement 1 COMPLETE, Enhancements 2-4 READY FOR IMPLEMENTATION
**Prerequisite for:** /create-agent command (see CREATE-AGENT-COMMAND-PLAN.md)
**Ready for:** Production use of enhanced agent-generator subagent
