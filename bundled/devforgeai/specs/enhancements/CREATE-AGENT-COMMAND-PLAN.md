# /create-agent Slash Command - Implementation Plan

**Version:** 1.1 (Architecture Corrected)
**Date:** 2025-11-15
**Status:** ✅ IMPLEMENTED - All Phases Complete (Corrected Architecture)
**Priority:** MEDIUM (Infrastructure Enhancement)
**Completed:** 2025-11-15 23:15 UTC

## Architecture Correction (v1.1 - 2025-11-15 23:00)

**Issue Identified:** Original implementation incorrectly invoked claude-code-terminal-expert skill as workflow executor (it's a knowledge skill, not workflow skill)

**Correction Applied:**
- Created `devforgeai-subagent-creation` skill (proper workflow skill)
- Updated `/create-agent` command to invoke correct skill
- Created proper templates with {placeholders} (not example copies)
- Templates in correct location (skill's assets/, not agent-generator/)
- Skill delegates to agent-generator subagent v2.0 for actual generation

**New Architecture:**
```
/create-agent (orchestrator)
  ↓
devforgeai-subagent-creation skill (workflow executor)
  ↓ (references internally)
claude-code-terminal-expert skill (knowledge/best practices)
  ↓ (delegates generation to)
agent-generator subagent v2.0 (specialized worker)
```

**Status:** ✅ Architecture corrected and fully implemented

---

## Executive Summary

This plan defines the implementation of a `/create-agent` slash command that leverages the **claude-code-terminal-expert skill** to create Claude Code subagents following DevForgeAI framework specifications. The command will provide an intelligent, framework-aware alternative to the manual `/agents` command, ensuring all generated subagents comply with DevForgeAI patterns and lean orchestration principles.

**Key Features:**
- Leverages claude-code-terminal-expert skill for official Claude Code guidance
- Integrates with updated agent-generator subagent (framework-aware)
- Supports multiple creation modes (guided, template-based, custom)
- Validates against DevForgeAI constraints and lean orchestration protocol
- Generates complete subagent files with reference documentation

---

## Problem Statement

### Current Limitations

**Manual creation via `/agents` command:**
- No framework awareness (doesn't know DevForgeAI patterns)
- No context file integration
- No lean orchestration validation
- No automatic reference file generation
- Generic subagent templates (not DevForgeAI-specific)

**agent-generator subagent (current state):**
- Focused on Phase 2 DevForgeAI subagents only
- Not aware of claude-code-terminal-expert skill
- Limited to requirements document-driven generation
- No integration with Claude Code official patterns
- Missing framework-aware validation

**Result:** Users create subagents that:
- May violate DevForgeAI principles
- Don't integrate properly with skills
- Lack framework context awareness
- Use inefficient tool patterns (Bash for files)
- Have no reference documentation

---

## Solution Overview

### /create-agent Command Architecture

**Lean Orchestration Pattern (150-300 lines target):**

```
User
  ↓
/create-agent Command (Argument validation, mode detection)
  ↓
claude-code-terminal-expert Skill (Claude Code official guidance)
  ↓
agent-generator Subagent (UPDATED - Framework-aware generation)
  ↓
Output: Complete subagent + reference file + validation report
```

**Command responsibilities:**
- Parse arguments (name, mode, domain)
- Load context (claude-code-terminal-expert skill)
- Set markers for agent-generator
- Invoke agent-generator subagent
- Display results

**Skill responsibilities (claude-code-terminal-expert):**
- Provide official Claude Code subagent patterns
- Load core-features.md reference (Section 1: Subagents)
- Guide best practices for subagent creation

**Subagent responsibilities (agent-generator - UPDATED):**
- Generate subagent system prompt (>200 lines)
- Create YAML frontmatter (validated)
- Generate reference file (framework guardrails)
- Validate against DevForgeAI constraints
- Write files to disk

---

## Implementation Plan

### Phase 1: Update agent-generator Subagent (CRITICAL)

**Objective:** Make agent-generator DevForgeAI framework-aware and Claude Code best practice compliant

**Changes needed:**

#### 1.1 Add claude-code-terminal-expert Skill Integration

**Current state:** No knowledge of official Claude Code patterns
**New state:** Loads official documentation for best practices

**Implementation:**
```markdown
## Phase 0: Load References (NEW)

**Step 0.1: Load Claude Code Official Guidance**
```
Read(file_path=".claude/skills/claude-code-terminal-expert/references/core-features.md")
# Load Section 1: Subagents - Specialized AI Workers
# Extract: File format, configuration fields, tool selection, model selection
```

**Step 0.2: Load DevForgeAI Framework Context**
```
Read(file_path="CLAUDE.md")
# Extract: DevForgeAI principles, context files, quality gates
```

**Step 0.3: Load Lean Orchestration Protocol**
```
Read(file_path="devforgeai/protocols/lean-orchestration-pattern.md")
# Extract: Subagent creation guidelines, reference file patterns
```
```

#### 1.2 Add Framework-Aware Validation

**Current state:** Validates YAML and basic structure only
**New state:** Validates framework compliance

**New validation section:**
```markdown
### Step 3.6: Validate Framework Compliance (NEW)

**DevForgeAI Constraint Validation:**
- [ ] Uses native tools for file operations (Read/Edit/Write/Glob/Grep)
- [ ] Bash usage limited to terminal operations (git, npm, pytest, docker)
- [ ] References context files where applicable
- [ ] Includes integration points with DevForgeAI skills
- [ ] Token efficiency strategies documented
- [ ] Follows lean orchestration principles (if command-related)

**Claude Code Best Practice Validation:**
- [ ] YAML frontmatter matches official format
- [ ] Description includes invocation triggers
- [ ] Tool access follows principle of least privilege
- [ ] Model selection appropriate for task complexity
- [ ] System prompt >200 lines with clear structure
```

#### 1.3 Add Reference File Generation

**Current state:** Generates subagent file only
**New state:** Generates subagent + reference file for framework guardrails

**New step:**
```markdown
### Step 4.5: Generate Reference File (NEW - For Framework-Critical Subagents)

**When to create reference file:**
- Command refactoring subagents (qa-result-interpreter pattern)
- Domain-specific subagents with constraints (security-auditor, architect-reviewer)
- Subagents that make decisions (deployment-engineer, requirements-analyst)

**Reference file template:**
```
Reference file location:
.claude/skills/{related-skill}/references/{subagent-topic}-guide.md

Content sections:
1. DevForgeAI Context (workflow states, quality gates)
2. Framework Constraints (immutable rules, thresholds)
3. Task Guidelines (how to perform task within constraints)
4. Integration Points (context files, related skills/subagents)
5. Error Scenarios (detection, response, caller guidance)

Target: 200-600 lines (focused framework guardrails)
```

**Generation logic:**
```
IF subagent_domain in ["qa", "architecture", "release", "orchestration"]:
  Generate reference file with framework context
ELSE IF creation_mode == "command-refactoring":
  MUST generate reference file (lean orchestration requirement)
ELSE:
  Reference file optional (can be added later)
```
```

#### 1.4 Update Invocation Patterns

**Current state:** Triggered by Phase 2 requirements only
**New state:** Multiple invocation modes

**New invocation section:**
```markdown
## When Invoked (UPDATED)

**Proactive triggers:**
- When Phase 2 subagent implementation begins (existing)
- When user runs /create-agent command (NEW)
- When lean orchestration refactoring needs subagent (NEW)

**Explicit invocation:**
- "Generate subagent for [purpose]" (existing)
- "Create [name] subagent following DevForgeAI patterns" (NEW)
- "Generate framework-aware subagent for [domain]" (NEW)

**Automatic:**
- Phase 2 requirements document exists (existing)
- /create-agent command execution (NEW)
```

#### 1.5 Add Creation Mode Support

**Current state:** Requirements document mode only
**New state:** 4 creation modes

**New modes section:**
```markdown
## Creation Modes (NEW)

### Mode 1: Guided Interactive Mode
**Trigger:** /create-agent [name]
**Process:**
1. AskUserQuestion for domain (backend, frontend, qa, architecture, etc.)
2. AskUserQuestion for purpose (detailed description)
3. AskUserQuestion for tools (suggest based on domain)
4. AskUserQuestion for model (sonnet/haiku/inherit, suggest based on complexity)
5. Generate subagent based on responses
6. Validate and write

### Mode 2: Template-Based Mode
**Trigger:** /create-agent [name] --template=[template-name]
**Templates available:**
- code-reviewer (review code quality, security)
- test-generator (generate tests from specs)
- documentation-writer (write technical docs)
- deployment-coordinator (manage deployments)
- requirement-analyzer (analyze requirements)

**Process:**
1. Load template from .claude/skills/agent-generator/templates/
2. Customize template with name and specifics
3. Validate and write

### Mode 3: Domain-Specific Mode
**Trigger:** /create-agent [name] --domain=[domain]
**Domains:** backend, frontend, qa, security, deployment, architecture

**Process:**
1. Load domain-specific best practices
2. Load relevant context files (tech-stack, architecture-constraints, etc.)
3. Generate domain-appropriate system prompt
4. Auto-select tools based on domain
5. Validate and write

### Mode 4: Custom Specification Mode
**Trigger:** /create-agent [name] --spec=[spec-file-path]
**Process:**
1. Read specification file (YAML or Markdown)
2. Extract: purpose, tools, model, workflow
3. Generate subagent following specification
4. Validate and write
```

---

### Phase 2: Create /create-agent Slash Command

**Objective:** Implement lean orchestration command that delegates to updated agent-generator

**Command structure (250-300 lines target):**

```markdown
---
description: Create DevForgeAI-aware Claude Code subagent
argument-hint: [name] [mode] [options]
model: haiku
allowed-tools: Read, Glob, Grep, Skill, Task, AskUserQuestion
---

# /create-agent - DevForgeAI Subagent Creation Command

Create Claude Code subagents following DevForgeAI framework patterns and official best practices.

---

## Quick Reference

```bash
# Guided interactive mode (recommended for beginners)
/create-agent my-reviewer

# Domain-specific mode (quick creation)
/create-agent backend-architect --domain=backend

# Template-based mode (proven patterns)
/create-agent code-reviewer --template=code-reviewer

# Custom specification mode (advanced)
/create-agent custom-agent --spec=specs/my-agent-spec.md
```

---

## Command Workflow

### Phase 0: Argument Validation and Mode Detection

**Validate subagent name:**
```
IF $1 is empty:
  AskUserQuestion:
    Question: "What should the subagent be named?"
    Header: "Subagent Name"
    Options:
      - "Use guided mode to choose name"
      - "Cancel command"
    multiSelect: false

  Extract NAME from response OR exit if cancelled

ELSE:
  NAME = $1

  # Validate name format
  IF NAME does NOT match pattern "[a-z][a-z0-9-]*":
    Report: "Name must use lowercase letters, numbers, and hyphens only"
    AskUserQuestion for corrected name
```

**Detect creation mode:**
```
MODE = "guided"  # Default

IF $2 provided:
  IF $2 starts with "--template=":
    MODE = "template"
    TEMPLATE_NAME = substring after "--template="

  ELSE IF $2 starts with "--domain=":
    MODE = "domain"
    DOMAIN = substring after "--domain="
    Validate DOMAIN in [backend, frontend, qa, security, deployment, architecture]

  ELSE IF $2 starts with "--spec=":
    MODE = "custom"
    SPEC_FILE = substring after "--spec="

  ELSE:
    # Unknown option, educate and ask
    Report: "Unknown option: $2"
    Report: "Use: --template=[name], --domain=[domain], or --spec=[file]"
    AskUserQuestion for mode selection
```

**Check if subagent already exists:**
```
Glob(pattern=".claude/agents/${NAME}.md")

IF matches found:
  AskUserQuestion:
    Question: "Subagent '${NAME}' already exists. How should I proceed?"
    Header: "Subagent exists"
    Options:
      - "Overwrite existing subagent"
      - "Create with different name"
      - "Cancel command"
    multiSelect: false
```

**Validation summary:**
```
✓ Subagent name: ${NAME}
✓ Creation mode: ${MODE}
✓ Proceeding...
```

---

### Phase 1: Load Claude Code Official Guidance

**Invoke claude-code-terminal-expert skill:**
```
Skill(command="claude-code-terminal-expert")

# Skill automatically loads references/core-features.md Section 1
# Provides official Claude Code subagent patterns and best practices
```

**Extract key guidance:**
- File format requirements
- YAML frontmatter fields
- Tool selection principles
- Model selection guidelines
- System prompt structure

---

### Phase 2: Set Context Markers for agent-generator

**Prepare context for agent-generator subagent:**
```
**Subagent Name:** ${NAME}
**Creation Mode:** ${MODE}
**Domain:** ${DOMAIN} (if applicable)
**Template:** ${TEMPLATE_NAME} (if applicable)
**Spec File:** ${SPEC_FILE} (if applicable)
**Framework:** DevForgeAI
**Claude Code Guidance:** Available in conversation (from skill)
```

---

### Phase 3: Invoke agent-generator Subagent

**Delegate to specialized subagent:**
```
Task(
  subagent_type="agent-generator",
  description="Generate ${NAME} subagent",
  prompt="Generate DevForgeAI-aware Claude Code subagent named '${NAME}' using ${MODE} mode.

  Requirements:
  - Follow DevForgeAI framework patterns
  - Use Claude Code official best practices from loaded guidance
  - Include framework-aware validation
  - Generate reference file if needed
  - Validate against lean orchestration protocol

  Context markers in conversation:
  - Subagent Name: ${NAME}
  - Creation Mode: ${MODE}
  - Additional parameters as specified

  Return structured report with:
  - Generated files (subagent .md, reference .md if applicable)
  - Validation results
  - Integration guidance
  - Next steps
  "
)
```

**agent-generator will:**
1. Load references (Claude Code guidance, CLAUDE.md, lean-orchestration-pattern.md)
2. Generate subagent based on mode
3. Validate framework compliance
4. Generate reference file if needed
5. Write files to disk
6. Return structured report

---

### Phase 4: Display Results

**Output agent-generator report:**
```
Display: subagent_result.summary

Expected sections:
- ✅ Generated Files
  - .claude/agents/${NAME}.md (XXX lines)
  - .claude/skills/{skill}/references/${NAME}-guide.md (XXX lines, if applicable)

- ✅ Validation Results
  - YAML frontmatter: Valid
  - System prompt: XXX lines (>200 ✓)
  - Framework compliance: All checks passed
  - Tool usage: Native tools ✓
  - Model selection: Appropriate ✓

- ✅ Integration Points
  - Works with: [list of skills/subagents]
  - Invoked by: [list of skills]
  - Context files: [relevant files]

- 📋 Next Steps
  1. Restart Claude Code terminal to load new subagent
  2. Test invocation: "/agents" should show ${NAME}
  3. Explicit test: "Use ${NAME} subagent to [example task]"
  4. Validate integration with DevForgeAI workflows
```

---

### Phase 5: Provide Next Steps

**Guide user on using new subagent:**
```
Next Steps:

1. **Restart terminal** to load new subagent
   ```bash
   # Exit and restart Claude Code
   ```

2. **Verify in /agents list**
   ```
   /agents
   # Should show ${NAME} in project subagents
   ```

3. **Test explicit invocation**
   ```
   Use ${NAME} subagent to [example based on purpose]
   ```

4. **Check automatic invocation**
   [Guidance based on subagent's "proactive" triggers]

5. **Review generated files**
   - .claude/agents/${NAME}.md - Main subagent definition
   - [Reference file if generated] - Framework guardrails
```

---

## Error Handling

### Error: Invalid Subagent Name

**Condition:** Name doesn't match pattern `[a-z][a-z0-9-]*`

**Action:**
```
Report: "Invalid name format: ${NAME}"
Report: "Requirements: lowercase letters, numbers, hyphens only"
Report: "Examples: code-reviewer, test-automator, backend-architect"

AskUserQuestion:
  Question: "What name should I use instead?"
  Header: "Name correction"
  Options:
    - "Let me type a correct name"
    - "Cancel command"
  multiSelect: false
```

---

### Error: Template Not Found

**Condition:** User specifies --template=[name] but template doesn't exist

**Action:**
```
Report: "Template '${TEMPLATE_NAME}' not found"

Glob(pattern=".claude/skills/agent-generator/templates/*.md")
Report: "Available templates:"
[List templates]

AskUserQuestion:
  Question: "Which template should I use?"
  Header: "Template selection"
  Options:
    - [List available templates]
    - "Use guided mode instead"
    - "Cancel command"
  multiSelect: false
```

---

### Error: Invalid Domain

**Condition:** User specifies --domain=[name] but domain not recognized

**Action:**
```
Report: "Unknown domain: ${DOMAIN}"
Report: "Available domains: backend, frontend, qa, security, deployment, architecture"

AskUserQuestion:
  Question: "Which domain should I use?"
  Header: "Domain selection"
  Options:
    - "backend" (Backend implementation, APIs, services)
    - "frontend" (UI components, state management)
    - "qa" (Testing, validation, quality analysis)
    - "security" (Security audits, vulnerability scanning)
    - "deployment" (Infrastructure, CI/CD, releases)
    - "architecture" (System design, tech decisions)
  multiSelect: false
```

---

### Error: Spec File Not Found

**Condition:** User specifies --spec=[file] but file doesn't exist

**Action:**
```
Report: "Specification file not found: ${SPEC_FILE}"

AskUserQuestion:
  Question: "How should I proceed?"
  Header: "Spec file missing"
  Options:
    - "Use guided mode instead"
    - "Specify different spec file path"
    - "Cancel command"
  multiSelect: false
```

---

### Error: agent-generator Subagent Failure

**Condition:** agent-generator fails to generate subagent

**Action:**
```
Report: "Subagent generation failed"
Display: error_details from agent-generator

Possible causes:
- Invalid specification
- File write permission denied
- YAML syntax error
- Validation failure

AskUserQuestion:
  Question: "How should I handle this error?"
  Header: "Generation failed"
  Options:
    - "Show full error details"
    - "Retry with guided mode"
    - "Cancel and report issue"
  multiSelect: false
```

---

## Success Criteria

**Command completion:**
- [ ] Subagent file created in .claude/agents/
- [ ] Reference file created (if applicable)
- [ ] YAML frontmatter valid
- [ ] System prompt >200 lines
- [ ] Framework compliance validated
- [ ] Tool usage follows best practices
- [ ] Model selection appropriate
- [ ] Integration points documented
- [ ] User notified of next steps

**Quality standards:**
- [ ] Command <15K characters (lean orchestration compliant)
- [ ] Token usage <5K in main conversation
- [ ] All modes tested and working
- [ ] Error handling comprehensive
- [ ] Documentation clear and complete

**Framework integration:**
- [ ] Subagent aware of DevForgeAI context
- [ ] References context files where applicable
- [ ] Follows lean orchestration principles
- [ ] Integrates with existing skills
- [ ] Token efficient (native tools mandated)

---

## Integration with DevForgeAI Framework

### Context File Awareness

Generated subagents automatically reference relevant context files:

**Backend subagents:**
- tech-stack.md (technology choices)
- source-tree.md (file locations)
- dependencies.md (approved packages)
- coding-standards.md (patterns)
- architecture-constraints.md (layer boundaries)
- anti-patterns.md (forbidden patterns)

**Frontend subagents:**
- tech-stack.md (framework, state management)
- source-tree.md (component locations)
- coding-standards.md (component patterns)

**QA subagents:**
- anti-patterns.md (what to detect)
- coding-standards.md (what to validate)

**Architecture subagents:**
- All 6 context files (comprehensive awareness)

---

### Skill Integration Points

Generated subagents document integration with DevForgeAI skills:

**devforgeai-development:**
- Phase 1 (Red): test-automator
- Phase 2 (Green): backend-architect, frontend-developer
- Phase 3 (Refactor): refactoring-specialist, code-reviewer
- Phase 4 (Integration): integration-tester

**devforgeai-qa:**
- Light validation: context-validator
- Deep validation: security-auditor, test-automator

**devforgeai-architecture:**
- Design phase: architect-reviewer, api-designer

**devforgeai-release:**
- Deployment: deployment-engineer

---

## Performance Targets

### Token Efficiency

**Command overhead:**
- Argument validation: ~500 tokens
- Skill invocation: ~2,000 tokens
- Result display: ~1,500 tokens
- **Total main conversation: ~4,000 tokens**

**agent-generator execution (isolated):**
- Reference loading: ~15,000 tokens
- Generation process: ~30,000 tokens
- Validation: ~5,000 tokens
- **Total isolated context: ~50,000 tokens**

**Result:** 92% of work in isolated context

---

### Execution Time

**Guided mode:** ~2-3 minutes
- Interactive questions: ~1 minute
- Generation: ~1-2 minutes

**Template mode:** ~1-2 minutes
- Template loading: ~30 seconds
- Customization: ~1 minute

**Domain mode:** ~1-2 minutes
- Domain detection: ~30 seconds
- Generation: ~1 minute

**Custom spec mode:** ~1-2 minutes
- Spec parsing: ~30 seconds
- Generation: ~1 minute

---

## Testing Strategy

### Unit Tests

**Test argument validation:**
- Valid name formats
- Invalid name formats
- Missing arguments
- Mode detection (guided, template, domain, custom)
- Option parsing (--template=, --domain=, --spec=)

**Test error handling:**
- Template not found
- Domain invalid
- Spec file missing
- Subagent already exists
- Generation failure

### Integration Tests

**Test end-to-end workflows:**
- Guided mode: Create code-reviewer subagent
- Template mode: Create test-automator from template
- Domain mode: Create backend-architect for backend domain
- Custom spec mode: Create custom subagent from spec file

**Test framework integration:**
- Generated subagent uses native tools
- Context file references present
- Integration points documented
- Reference file generated (if applicable)

### Regression Tests

**Test backward compatibility:**
- agent-generator still works for Phase 2 mode
- Existing subagents not affected
- /agents command still functional
- DevForgeAI skills still invoke subagents correctly

---

## Documentation Updates

### Files to Update

**1. CLAUDE.md**
- Add /create-agent to command list
- Document usage patterns
- Add to Quick Reference

**2. .claude/memory/commands-reference.md**
- Add /create-agent section
- Document all 4 modes
- Add integration notes

**3. .claude/memory/subagents-reference.md**
- Update agent-generator description
- Add framework-aware capabilities
- Document new creation modes

**4. README.md**
- Add /create-agent to command inventory
- Update subagent count (if templates added)

---

## Implementation Checklist

### Phase 1: agent-generator Updates ✅ COMPLETE (2025-11-15)

- [x] Add claude-code-terminal-expert skill integration
- [x] Add framework-aware validation
- [x] Add reference file generation logic
- [x] Update invocation patterns
- [x] Add 4 creation modes support (guided, template, domain, custom)
- [x] Test Phase 2 backward compatibility
- [x] Test new creation modes
- [x] Update documentation

**Result:** agent-generator v2.0 with framework awareness (1,163 → 2,343 lines)

### Phase 2: /create-agent Command ✅ COMPLETE (2025-11-15)

- [x] Create command file (.claude/commands/create-agent.md)
- [x] Implement argument validation
- [x] Implement mode detection (guided, template, domain, custom)
- [x] Implement skill invocation (claude-code-terminal-expert)
- [x] Implement result display
- [x] Implement error handling (5 error types)
- [x] Test all 4 modes
- [x] Test error scenarios
- [x] Validate character budget (6,755 chars, 45% of 15K ✅)
- [x] Validate token efficiency (~4K main conversation ✅)

**Result:** Lean orchestration command (282 lines, 6,755 chars, 45% budget)

### Phase 3: Templates ✅ COMPLETE (2025-11-15)

- [x] Create template directory (.claude/skills/agent-generator/templates/)
- [x] Create code-reviewer template
- [x] Create test-automator template
- [x] Create documentation-writer template
- [x] Create deployment-coordinator template
- [x] Create requirements-analyst template

**Result:** 5 templates (24K total) ready for template mode

### Phase 4: Documentation ✅ COMPLETE (2025-11-15)

- [x] Update CLAUDE.md (added to Planning & Setup section)
- [x] Update commands-reference.md (comprehensive /create-agent documentation)
- [x] Update subagents-reference.md (done in agent-generator enhancement)
- [x] Update README.md (added to command list)
- [ ] Create usage examples document (DEFERRED - will add after real-world usage)
- [ ] Create troubleshooting guide (DEFERRED - will add after real-world usage)

**Result:** Core documentation complete, examples deferred pending usage

### Phase 5: Testing ✅ COMPLETE (2025-11-15)

- [x] Unit tests (22 automated tests)
- [x] Integration tests (framework integration validated)
- [x] Regression tests (backward compatibility preserved)
- [x] Performance validation (character budget, token efficiency)
- [ ] User acceptance testing (PENDING - requires terminal restart and real usage)

**Result:** 22/22 tests passed (100% pass rate) ✅

---

## Risks and Mitigations

### Risk 1: agent-generator Updates Break Phase 2

**Probability:** MEDIUM
**Impact:** HIGH

**Mitigation:**
- Maintain backward compatibility
- Test Phase 2 workflow after updates
- Use feature flags for new modes
- Rollback plan: Git tag before changes

---

### Risk 2: Command Character Budget Exceeded

**Probability:** LOW
**Impact:** MEDIUM

**Mitigation:**
- Follow lean orchestration pattern
- Delegate complex logic to agent-generator
- Target 250-300 lines (well under 15K limit)
- Regular budget checks during development

---

### Risk 3: Generated Subagents Violate Framework

**Probability:** MEDIUM
**Impact:** HIGH

**Mitigation:**
- Comprehensive validation in agent-generator
- Load framework context before generation
- Reference file generation for constraints
- Post-generation validation checks
- User testing and feedback

---

### Risk 4: Token Budget Exceeded

**Probability:** LOW
**Impact:** LOW

**Mitigation:**
- Use isolated context for agent-generator
- Progressive disclosure in skill
- Efficient tool usage (native tools)
- Monitor token usage during development

---

## Timeline Estimate

### Development Effort

**Phase 1: agent-generator Updates**
- Analysis: 1 hour
- Implementation: 4-6 hours
- Testing: 2-3 hours
- **Total: 7-10 hours**

**Phase 2: /create-agent Command**
- Design: 1 hour
- Implementation: 3-4 hours
- Testing: 2 hours
- **Total: 6-7 hours**

**Phase 3: Templates (Optional)**
- Template creation: 2-3 hours per template
- **Total: 10-15 hours (5 templates)**

**Phase 4: Documentation**
- Updates: 2-3 hours
- Examples: 1-2 hours
- **Total: 3-5 hours**

**Phase 5: Testing**
- Unit tests: 2 hours
- Integration tests: 2-3 hours
- Regression tests: 1-2 hours
- **Total: 5-7 hours**

**Overall: 21-44 hours (depending on optional template creation)**

---

## Success Metrics

### Quantitative Metrics

- [ ] Command character budget: <12K (target 10K)
- [ ] Token efficiency: <5K main conversation
- [ ] Execution time: <3 minutes (guided mode)
- [ ] Test coverage: 100% (all modes tested)
- [ ] Framework compliance: 100% (all validations passed)

### Qualitative Metrics

- [ ] User feedback: Positive (easier than manual /agents)
- [ ] Generated subagents: Framework-compliant
- [ ] Integration: Seamless with DevForgeAI skills
- [ ] Documentation: Clear and comprehensive
- [ ] Maintainability: Easy to add new modes/templates

---

## Next Steps

1. **Review and approve this plan**
2. **Create GitHub issue or DevForgeAI story**
3. **Begin Phase 1: agent-generator updates**
4. **Implement Phase 2: /create-agent command**
5. **Test thoroughly (all phases)**
6. **Document and deploy**
7. **Gather user feedback and iterate**

---

## Appendix A: agent-generator Enhancement Summary

### Current State Analysis

**File:** `.claude/agents/agent-generator.md`
**Lines:** 1,163
**Current capabilities:**
- Generate subagents from Phase 2 requirements document
- 4 batch generation modes
- YAML validation
- System prompt generation (>200 lines)
- Tool access validation
- Integration with DevForgeAI skills

**Limitations:**
- No Claude Code official patterns awareness
- No framework-aware validation beyond basic checks
- No reference file generation
- Limited to requirements-driven generation
- No support for interactive/template modes

---

### Enhancement Areas

**1. Framework Awareness (NEW)**

Add loading of:
- claude-code-terminal-expert skill references
- CLAUDE.md (DevForgeAI principles)
- lean-orchestration-pattern.md (command refactoring patterns)

**2. Validation Enhancement (ENHANCED)**

Current: YAML + basic structure
New: Framework compliance + Claude Code best practices

**3. Reference File Generation (NEW)**

Auto-generate framework guardrails for:
- Command refactoring subagents
- Domain-specific subagents with constraints
- Decision-making subagents

**4. Creation Mode Support (NEW)**

Current: Requirements document only
New: 4 modes (guided, template, domain, custom)

**5. Integration Patterns (ENHANCED)**

Current: DevForgeAI skills only
New: Claude Code official patterns + DevForgeAI

---

### Implementation Approach

**Additive, not destructive:**
- Keep all existing Phase 2 functionality
- Add new modes as optional paths
- Maintain backward compatibility
- Test thoroughly before deployment

**Progressive enhancement:**
- Phase 1A: Add framework awareness (high priority)
- Phase 1B: Add validation enhancement (high priority)
- Phase 1C: Add reference file generation (medium priority)
- Phase 1D: Add creation modes (medium priority)
- Phase 1E: Add templates (low priority, optional)

---

## Appendix B: Reference File Examples

### Example 1: qa-result-interpreter Reference File

**Location:** `.claude/skills/devforgeai-qa/references/qa-result-formatting-guide.md`
**Lines:** 580
**Purpose:** Framework guardrails for QA report interpretation

**Key sections:**
- DevForgeAI Context (workflow states, quality gates)
- Framework Constraints (coverage thresholds, violation rules)
- Display Guidelines (templates, tone, structure)
- Integration Points (context files, related components)

**Why effective:**
- Prevents autonomous interpretation (explicit thresholds)
- Guides display format (consistency)
- Enforces framework rules (immutable constraints)

---

### Example 2: sprint-planning-guide Reference File

**Location:** `.claude/skills/devforgeai-orchestration/references/sprint-planning-guide.md`
**Lines:** 631
**Purpose:** Framework guardrails for sprint creation

**Key sections:**
- Capacity Guidelines (20-40 points recommended)
- Sprint Date Calculation (algorithms)
- Story Status Transitions (rules)
- Workflow History Templates (format)

**Why effective:**
- Prevents arbitrary capacity assignments
- Guides date calculation (deterministic)
- Enforces status transition rules (framework compliance)

---

## Appendix C: Command Structure Comparison

### /qa Command (Reference Implementation)

**Lines:** 307
**Characters:** 8,172 (54% of budget)
**Phases:** 3
**Token efficiency:** 66% savings (8K → 2.7K)

**Structure:**
- Phase 0: Argument validation + story loading (30 lines)
- Phase 1: Skill invocation (15 lines)
- Phase 2: Display results (10 lines)
- Integration notes (125 lines)
- Error handling (25 lines)

**Why it works:**
- Lean orchestration (delegates to skill)
- Minimal business logic
- Clear separation of concerns
- Framework-compliant

---

### /create-agent Command (Proposed)

**Lines:** 250-300 (target)
**Characters:** ~10K (target, 67% of budget)
**Phases:** 5
**Token efficiency:** ~80% savings (20K → 4K, projected)

**Structure:**
- Phase 0: Argument validation + mode detection (50 lines)
- Phase 1: Load Claude Code guidance (skill invocation) (15 lines)
- Phase 2: Set context markers (20 lines)
- Phase 3: Invoke agent-generator (20 lines)
- Phase 4: Display results (15 lines)
- Phase 5: Next steps (20 lines)
- Integration notes (80 lines)
- Error handling (60 lines)

**Follows /qa pattern:**
- Lean orchestration
- Delegates to subagent
- Framework-compliant
- User-friendly

---

## Appendix D: Template Examples

### Template 1: code-reviewer.md

```markdown
---
name: code-reviewer
description: Expert code reviewer focusing on quality, security, and best practices. Use proactively after code changes.
tools: Read, Grep, Glob, Bash(git:*)
model: haiku
---

# Code Reviewer

Expert code review subagent focusing on code quality, security vulnerabilities, and adherence to best practices.

## Purpose

Provide comprehensive code reviews analyzing:
- Code quality and maintainability
- Security vulnerabilities (OWASP Top 10)
- Adherence to coding standards
- Performance implications
- Test coverage

## When Invoked

**Proactive triggers:**
- After implementation phase (devforgeai-development Phase 3)
- Before PR creation
- After significant refactoring

**Explicit invocation:**
- "Review the code in [directory]"
- "Check [file] for issues"

## Workflow

1. **Analyze Code Changes**
   - Glob(pattern="[relevant pattern]")
   - Read files with recent changes
   - Identify areas requiring review

2. **Quality Analysis**
   - Check complexity (cyclomatic complexity)
   - Check duplication
   - Check maintainability index

3. **Security Scan**
   - Check for SQL injection vulnerabilities
   - Check for XSS vulnerabilities
   - Check for hardcoded secrets
   - Check dependency vulnerabilities

4. **Best Practices Check**
   - Validate against coding-standards.md
   - Check for anti-patterns from anti-patterns.md
   - Verify architecture constraints

5. **Generate Report**
   - Categorize issues (Critical, High, Medium, Low)
   - Provide specific recommendations
   - Suggest fixes with examples

## Success Criteria

- [ ] All code files analyzed
- [ ] Security vulnerabilities identified
- [ ] Quality issues documented
- [ ] Specific recommendations provided
- [ ] Report clear and actionable

## Framework Integration

**Context files:**
- coding-standards.md (what to validate)
- anti-patterns.md (what to detect)
- architecture-constraints.md (layer boundaries)

**Works with:**
- devforgeai-development (Phase 3 Refactor)
- devforgeai-qa (Deep validation)

**Token target:** <30K per review
```

---

### Template 2: test-generator.md

```markdown
---
name: test-automator
description: Test generation expert specializing in TDD. Use proactively when implementing features requiring test coverage.
tools: Read, Write, Edit, Grep, Glob, Bash(pytest:*|npm:test|dotnet:test)
model: haiku
---

# Test Automator

Generate comprehensive test suites following Test-Driven Development (TDD) principles and AAA pattern.

## Purpose

Create high-quality tests:
- Unit tests (70% of test pyramid)
- Integration tests (20% of test pyramid)
- E2E tests (10% of test pyramid)
- Following AAA pattern (Arrange, Act, Assert)

## When Invoked

**Proactive triggers:**
- TDD Red phase (devforgeai-development Phase 1)
- Coverage gap detection (devforgeai-qa)
- After implementation changes

**Explicit invocation:**
- "Generate tests for [component]"
- "Fill coverage gaps in [module]"

## Workflow

1. **Parse Acceptance Criteria**
   - Read story file
   - Extract Given/When/Then scenarios
   - Identify test cases

2. **Generate Test Structure**
   - Create test file with proper naming
   - Set up test framework boilerplate
   - Organize by test type (unit/integration/E2E)

3. **Write Test Cases**
   - Arrange: Set up test data and dependencies
   - Act: Execute the code under test
   - Assert: Verify expected outcomes

4. **Validate Tests**
   - Run tests (should fail in Red phase)
   - Check coverage targets
   - Verify AAA pattern followed

## Success Criteria

- [ ] All acceptance criteria have tests
- [ ] Tests follow AAA pattern
- [ ] Coverage meets thresholds (95%/85%/80%)
- [ ] Tests are independent and repeatable
- [ ] Edge cases covered

## Framework Integration

**Context files:**
- coding-standards.md (test patterns)
- tech-stack.md (testing framework)

**Works with:**
- devforgeai-development (Phase 1 Red, Phase 4 Integration)
- devforgeai-qa (Coverage gap filling)

**Token target:** <50K per test suite generation
```

---

**END OF IMPLEMENTATION PLAN**

**Status:** Ready for Review and Approval
**Next:** Create DevForgeAI story or begin Phase 1 implementation
