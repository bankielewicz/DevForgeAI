# Canonical Agent Template

**Version**: 1.0
**Status**: LOCKED
**Last Updated**: 2026-02-11

This reference document defines the canonical structure for all DevForgeAI subagent `.md` files. It specifies 10 required sections, a frontmatter schema with 9 fields, 4 agent categories with optional sections, size guidance, and a migration mapping table for field naming consistency.

---

## How to Use This Template

1. Determine agent category using the Category Decision Table below
2. Create a new `.md` file in `.claude/agents/` following the naming convention
3. Add all 10 required sections (Sections 1-10)
4. Add category-specific optional sections as needed
5. Validate frontmatter against the schema (Section 1)
6. Ensure the final agent file is within the 100-500 line range

---

## Section 1: YAML Frontmatter

**Purpose:** Define machine-readable metadata for Claude Code Terminal agent discovery, tool access control, and model selection. The frontmatter enables the framework to discover, configure, and invoke agents without parsing the full document.

**Format:** YAML block delimited by `---` markers at the top of the file. All fields use underscore_separated naming for multi-word identifiers.

**Minimum Content:** All required fields must be present with valid values. Example:

```yaml
---
name: example-agent              # string, required
description: >                   # string, required
  Brief summary of what this agent does and when to use it.
  First sentence is a standalone summary usable in registry tables.
tools:                           # array, required
  - Read
  - Grep
  - Glob
model: opus                      # enum, required
color: green                     # string, optional
permissionMode: default          # enum, optional
skills: spec-driven-qa            # string, optional
proactive_triggers:              # array, optional
  - "after code implementation"
  - "when coverage gaps detected"
version: "1.0.0"                 # string (semver), optional
---
```

### Frontmatter Schema

The following table defines all 9 frontmatter fields with type, requirement status, validation rules, and defaults.

| Field | Type | Required | Validation Rules | Default |
|-------|------|----------|------------------|---------|
| name | string | Required | Lowercase kebab-case; must match filename without `.md` extension; pattern `^[a-z][a-z0-9-]+$` | None |
| description | string | Required | 20-200 words; first sentence is standalone summary (~80 chars max for CLAUDE.md registry); no markdown formatting | None |
| tools | array | Required | Array of strings from allowed tool set: Read, Write, Edit, Grep, Glob, Bash, Bash(scope:*), WebFetch, WebSearch, AskUserQuestion; use empty array `[]` for tool-less agents | None |
| model | enum | Required | One of: `opus`, `sonnet`, `haiku`, `inherit`; `opus` for complex reasoning, `sonnet` for balanced, `haiku` for fast/simple, `inherit` to match parent conversation | `opus` |
| color | string | Optional | Any valid CSS color identifier; used for terminal display differentiation | `green` |
| permissionMode | enum | Optional | One of: `default`, `acceptEdits`; `default` requires user approval for writes, `acceptEdits` auto-approves | `default` |
| skills | string | Optional | Parent skill identifier or comma-separated list; identifies which skill(s) invoke this agent | None |
| proactive_triggers | array | Optional | Array of strings describing when the agent should be automatically invoked; each trigger is a natural language phrase | None |
| version | string (semver) | Optional | Semantic version for change tracking; format `MAJOR.MINOR.PATCH`; increment on prompt changes | None |

---

## Section 2: Title

**Purpose:** Provide a human-readable H1 heading that identifies the agent. The title serves as the primary identifier in documentation, logs, and agent registry displays.

**Format:** Single H1 (`#`) heading. Must be title-case version of the `name` field with hyphens converted to spaces.

**Minimum Content:** One H1 heading matching the agent identifier.

```markdown
# Example Agent
```

**Rules:**
- Exactly one H1 heading per agent file
- Title must correspond to the `name` frontmatter field (e.g., `name: code-reviewer` produces `# Code Reviewer`)
- No additional text on the title line

---

## Section 3: Purpose

**Purpose:** Explain what the agent does, its specialization, and the value it provides. This section enables other developers and AI orchestrators to understand the agent's role within the framework.

**Format:** 2-5 sentences of direct, instructive prose. Use numbered list for multi-faceted agents (3-5 bullet points). Address the agent in second person ("You are...") for system prompt clarity.

**Minimum Content:** At least 2 sentences describing the agent's domain expertise and primary function.

```markdown
## Purpose

You are a [domain] expert specializing in:

1. **[Primary capability]** - [brief description]
2. **[Secondary capability]** - [brief description]
3. **[Tertiary capability]** - [brief description]
```

---

## Section 4: When Invoked

**Purpose:** Define the conditions under which the agent activates. This enables proactive triggering by the framework, explicit invocation by users, and automatic invocation by skills.

**Format:** Three subsections with bullet lists:
- **Proactive triggers**: Conditions where the agent should be automatically suggested
- **Explicit invocation**: User commands or phrases that invoke the agent
- **Automatic**: Skill phases or workflow stages that invoke the agent

**Minimum Content:** At least one entry in each of the three subsections.

```markdown
## When Invoked

**Proactive triggers:**
- After [event or condition]
- When [state or threshold detected]

**Explicit invocation:**
- "[User command or phrase]"
- "[Alternative command or phrase]"

**Automatic:**
- When `[skill-id]` skill enters [Phase N]
- When `[other-skill]` detects [condition]
```

---

## Section 5: Input/Output Specification

**Purpose:** Define what data the agent receives as input and what it produces as output. This creates a contract between the invoking skill/command and the agent, enabling predictable integration.

**Format:** Two subsections (Input and Output) with structured descriptions of data shape, required fields, and format.

**Minimum Content:** At least one input source and one output artifact specified.

```markdown
## Input/Output Specification

### Input
- **Story file**: `devforgeai/specs/Stories/[STORY-ID].story.md` - acceptance criteria source
- **Context files**: 6 context files from `devforgeai/specs/context/` - constraint enforcement
- **Prompt parameters**: Task-specific instructions from invoking skill

### Output
- **Primary deliverable**: [Description of main output artifact]
- **Format**: [Markdown/JSON/structured text]
- **Location**: [Where output is written or returned]
```

---

## Section 6: Constraints and Boundaries

**Purpose:** Define what the agent must NOT do, its tool access limitations, read-only policies, and scope boundaries. This prevents scope creep, enforces least-privilege access, and maintains single responsibility.

**Format:** Bullet list organized by constraint type: tool restrictions, scope limitations, forbidden actions, and delegation rules.

**Minimum Content:** At least 3 constraint statements covering tool access, scope boundaries, and forbidden actions.

```markdown
## Constraints and Boundaries

**Tool Restrictions:**
- Read-only access to context files (no Write/Edit on `devforgeai/specs/context/`)
- Bash restricted to [specific scope] (e.g., `Bash(git:*)`)

**Scope Boundaries:**
- Does NOT [out-of-scope action]
- Delegates [related concern] to [other-agent] subagent

**Forbidden Actions:**
- NEVER modify context files directly
- NEVER approve its own output without user review
- NEVER invoke skills or commands (terminal subagent)
```

---

## Section 7: Workflow

**Purpose:** Define the step-by-step execution process the agent follows. The workflow ensures consistent, reproducible behavior across invocations and provides a clear mental model for developers.

**Format:** Numbered steps organized into phases. Each step includes the action, the tool call pattern, and decision logic. Use code blocks for tool invocations.

**Minimum Content:** At least 3 numbered workflow steps covering setup, core execution, and output generation.

```markdown
## Workflow

1. **Read Context and Requirements**
   - Read story file for acceptance criteria
   - Read relevant context files for constraints
   ```
   Read(file_path="devforgeai/specs/Stories/[STORY-ID].story.md")
   Read(file_path="devforgeai/specs/context/tech-stack.md")
   ```

2. **Execute Core Analysis/Generation**
   - [Domain-specific steps]
   - [Decision logic and branching]

3. **Generate Output**
   - [Format results per Output Format section]
   - [Write deliverables to specified location]
```

---

## Section 8: Success Criteria

**Purpose:** Provide a measurable checklist of conditions that indicate successful agent execution. These criteria enable both human review and automated validation of agent output quality.

**Format:** Markdown checklist (`- [ ]`) with specific, measurable items. Each criterion should be independently verifiable.

**Minimum Content:** At least 4 checklist items covering completeness, accuracy, standards compliance, and token efficiency.

```markdown
## Success Criteria

- [ ] [Primary deliverable produced and complete]
- [ ] [Accuracy/quality threshold met]
- [ ] [Context file constraints respected]
- [ ] [Standards compliance verified]
- [ ] Token usage < [budget]K per invocation
```

---

## Section 9: Output Format

**Purpose:** Define the structured format of the agent's deliverable. This enables consuming skills and users to parse, display, and act on agent output predictably.

**Format:** A complete example of the output structure with placeholders. Include format type (Markdown, JSON, YAML), required sections, and field descriptions.

**Minimum Content:** One complete output example with all required fields shown.

```markdown
## Output Format

```markdown
# [Report/Analysis/Result Title]

**Status**: [PASS | FAIL | NEEDS REVIEW]

## [Section 1]
[Content structure with field placeholders]

## [Section 2]
[Content structure with field placeholders]

## Summary
[Key findings and recommendations]
```
```

---

## Section 10: Examples

**Purpose:** Provide concrete invocation examples showing how the agent is called via `Task()` pattern. Examples serve as integration documentation and enable quick adoption by skill developers.

**Format:** At least one complete `Task()` invocation example with realistic parameters. Include context about when this invocation would occur.

**Minimum Content:** At least 1 Task() pattern example with prompt, expected behavior, and context.

```markdown
## Examples

### Example 1: Standard Invocation

**Context:** During Phase 2 of spec-driven-dev skill.

```
Task(
  subagent_type="[agent-id]",
  prompt="[Specific task description with context]. Story: STORY-XXX. Files: [relevant paths]."
)
```

**Expected behavior:**
- Agent reads specified files
- Agent applies domain expertise
- Agent returns structured output per Output Format section
```

---

## Agent Categories and Optional Sections

Agents are classified into 4 categories based on their primary function. Each category has 3 optional sections that extend the required sections for domain-specific needs. An agent may belong to multiple categories.

### Category 1: Validator

**Description:** Agents that check compliance, enforce rules, and verify constraints. Examples: context-validator, ac-compliance-verifier, deferral-validator.

**Optional Sections:**

#### Validation Rules

**Purpose:** Define the specific rules the validator checks, organized by category or severity.

**Format:** Numbered or categorized rule list with pass/fail conditions.

#### Severity Classification

**Purpose:** Define how validation findings are categorized by severity (Critical, High, Medium, Low) with specific examples for each level.

**Format:** Table or tiered list mapping violation types to severity levels.

#### Pass/Fail Criteria

**Purpose:** Define the aggregate conditions that determine overall validation pass or fail status.

**Format:** Threshold definitions and blocking rules (e.g., "FAIL if any Critical violations found").

---

### Category 2: Implementor

**Description:** Agents that generate code, tests, or implementation artifacts. Examples: backend-architect, test-automator, frontend-developer.

**Optional Sections:**

#### Implementation Patterns

**Purpose:** Define the design patterns, architectural approaches, and coding standards the implementor follows when generating code.

**Format:** Pattern descriptions with code examples showing correct and incorrect usage.

#### Code Generation Rules

**Purpose:** Specify rules governing generated code quality: naming conventions, file structure, dependency injection, error handling.

**Format:** Rule list with code examples demonstrating each rule.

#### Test Requirements

**Purpose:** Define testing expectations for generated code: coverage thresholds, test patterns, and verification steps.

**Format:** Checklist or table specifying test type, coverage target, and required assertions.

---

### Category 3: Analyzer

**Description:** Agents that examine code, metrics, or artifacts to produce assessments and scores. Examples: code-analyzer, coverage-analyzer, code-quality-auditor.

**Optional Sections:**

#### Analysis Metrics

**Purpose:** Define the specific metrics the analyzer computes, with formulas and data sources.

**Format:** Table of metric label, formula, data source, and interpretation guidance.

#### Scoring Rubrics

**Purpose:** Define how raw metrics translate to qualitative scores or grades.

**Format:** Scoring scale with thresholds (e.g., A: 95-100, B: 85-94, C: 75-84).

#### Threshold Definitions

**Purpose:** Define pass/warn/fail thresholds for each metric, with configurable values.

**Format:** Table of metric, pass threshold, warn threshold, and fail threshold.

---

### Category 4: Formatter

**Description:** Agents that transform data into human-readable displays, reports, or structured outputs. Examples: dev-result-interpreter, qa-result-interpreter, ui-spec-formatter.

**Optional Sections:**

#### Output Templates

**Purpose:** Define the display templates used to format output for different contexts (terminal, markdown, summary).

**Format:** Complete template examples with placeholder syntax.

#### Data Transformation Rules

**Purpose:** Define how raw input data maps to display fields, including filtering, aggregation, and enrichment logic.

**Format:** Transformation rules as input-to-output mapping descriptions.

#### Display Modes

**Purpose:** Define different display modes (compact, detailed, summary) and when each is appropriate.

**Format:** Mode definitions with trigger conditions and example output for each.

---

### Category Decision Table

Use this decision table to determine which category (or categories) an agent belongs to, and which optional sections to include.

| Primary Function | Category | Optional Sections to Include | Example Agents |
|-----------------|----------|------------------------------|----------------|
| Checks rules, validates constraints, enforces compliance | Validator | Validation Rules, Severity Classification, Pass/Fail Criteria | context-validator, ac-compliance-verifier, deferral-validator |
| Generates code, tests, or artifacts | Implementor | Implementation Patterns, Code Generation Rules, Test Requirements | backend-architect, test-automator, frontend-developer, deployment-engineer |
| Examines code or metrics, produces scores/assessments | Analyzer | Analysis Metrics, Scoring Rubrics, Threshold Definitions | code-analyzer, coverage-analyzer, code-quality-auditor, anti-pattern-scanner |
| Transforms data into displays or reports | Formatter | Output Templates, Data Transformation Rules, Display Modes | dev-result-interpreter, qa-result-interpreter, ui-spec-formatter |
| Reviews code for quality and issues | Analyzer + Validator | Analysis Metrics, Severity Classification, Pass/Fail Criteria | code-reviewer, security-auditor |
| Generates tests and analyzes coverage | Implementor + Analyzer | Implementation Patterns, Test Requirements, Analysis Metrics, Threshold Definitions | test-automator |

**Multi-category agents:** When an agent spans multiple categories, include optional sections from all relevant categories. Monitor total line count -- if the agent exceeds 300 lines, consider extracting detailed content to a `references/` subdirectory.

---

## Size Guidance

### Line Count Constraints

Agents created from this template must respect the following line count limits (Source: tech-stack.md, lines 385-388; source-tree.md, lines 593-608):

| Metric | Line Range | Action |
|--------|-----------|--------|
| Minimum populated agent | 100 lines | Below 100 lines indicates missing required sections |
| Target range | 100-300 lines | Ideal size for token efficiency |
| Warning threshold | 300-400 lines | Consider extracting to references/ subdirectory |
| Hard limit for agent files | 500 lines | BLOCK: Extract detailed content to references/ |
| This reference document | < 800 lines | Reference documents are exempt from 500-line agent limit |

**Progressive Disclosure Pattern:**

When an agent exceeds 300 lines, extract reference documentation:

```
.claude/agents/
  my-agent.md                # Core agent (<=300 lines)
  my-agent/
    references/
      detailed-workflow.md    # Extracted details
      domain-patterns.md      # Domain-specific content
```

**Extractable sections** (move to references/):
- Detailed code examples, pattern libraries, extended checklists, domain-specific guides

**Non-extractable sections** (must remain in core file):
- Frontmatter, Title, Purpose, When Invoked, Constraints, Success Criteria

---

## Field Naming Convention

### Underscore Convention

All multi-word frontmatter fields use **underscore_separated** naming:

- `proactive_triggers` (not `proactive-triggers`)
- `permissionMode` (single camelCase word, no underscore needed)

**Rationale:** The underscore convention matches the existing majority pattern across DevForgeAI agents. YAML parsers handle underscores consistently across all platforms.

### Migration Mapping Table

When migrating existing agents to the canonical template, use this mapping table to normalize fields and types.

| Old Field | Canonical Field | Change Type | Notes |
|---------------|---------------------|-------------|-------|
| allowed-tools | tools | Rename field | Hyphenated variant used in early agents |
| proactive-triggers | proactive_triggers | Rename field | Hyphen to underscore for consistency |
| tools (string) | tools (array) | Type change | Convert comma-separated string `"Read, Write"` to array `[Read, Write]` |
| allowed_tools | tools | Rename field | Underscore variant also normalizes to `tools` |
| model (missing) | model | Add field | Default to `opus` if not specified |
| color (missing) | color | Add field | Default to `green` if not specified |
| trigger_patterns | proactive_triggers | Rename field | Alternate label used in prototype agents |
| tool-access | tools | Rename field | Early variant |
| description (>200 words) | description (20-200 words) | Trim content | Truncate to 200 words; move details to Purpose section |

### Migration Checklist

To migrate an existing agent to canonical template compliance:

1. **Frontmatter normalization** (~2 min): Remap fields per migration mapping table
2. **Type corrections** (~2 min): Convert string fields to arrays where specified
3. **Add missing required fields** (~2 min): Add `model`, `tools` if absent
4. **Section reorganization** (~5 min): Map existing content to 10 required sections
5. **Optional sections** (~3 min): Identify category, add category-specific sections if needed
6. **Size validation** (~1 min): Check line count is 100-500; extract to references/ if over 300
7. **Final validation** (~2 min): Run agent-generator validation checks

**Estimated total migration time per agent: 10-20 minutes**

---

## Appendix A: Gap Analysis

This appendix validates the canonical template against 3 structurally diverse existing agents: test-automator.md (Implementor), code-reviewer.md (Analyzer + Validator), and security-auditor.md (Analyzer + Validator). For each agent, the table maps existing content to template sections and identifies gaps.

### Gap Analysis: test-automator.md

**Category:** Implementor + Analyzer

| Required Section | Present | Gap Severity | Notes |
|-----------------|---------|--------------|-------|
| 1. YAML Frontmatter | Yes | None | All 9 fields present including proactive_triggers |
| 2. Title | Yes | None | "# Test Automator" matches identifier |
| 3. Purpose | Yes | None | 5-point numbered list describing specialization |
| 4. When Invoked | Yes | None | All 3 subsections (proactive, explicit, automatic) |
| 5. Input/Output Specification | Partial | Medium | Input sources documented inline; no explicit I/O section heading |
| 6. Constraints and Boundaries | No | High | No dedicated constraints section; tool restrictions implied but not stated |
| 7. Workflow | Yes | None | "Core Workflow" with numbered phases |
| 8. Success Criteria | Yes | None | 9-item checklist present |
| 9. Output Format | No | Medium | No structured output format section; output implied by test file generation |
| 10. Examples | No | Medium | No Task() invocation example provided |

**Frontmatter Compliance:** Full compliance -- all 9 fields present with correct types.

### Gap Analysis: code-reviewer.md

**Category:** Analyzer + Validator

| Required Section | Present | Gap Severity | Notes |
|-----------------|---------|--------------|-------|
| 1. YAML Frontmatter | Yes | None | 8 of 9 fields present (missing version) |
| 2. Title | Yes | None | "# Code Reviewer" matches identifier |
| 3. Purpose | Yes | None | 2-sentence purpose description |
| 4. When Invoked | Yes | None | All 3 subsections present |
| 5. Input/Output Specification | Partial | Medium | Input via git diff/status documented; no explicit I/O heading |
| 6. Constraints and Boundaries | No | High | No dedicated constraints section |
| 7. Workflow | Yes | None | 4-step numbered workflow |
| 8. Success Criteria | Yes | None | 8-item checklist present |
| 9. Output Format | Yes | None | "Feedback Format" section with complete markdown template |
| 10. Examples | No | Medium | No Task() invocation example |

**Frontmatter Compliance:** 8/9 fields -- missing `version` (optional, acceptable).

### Gap Analysis: security-auditor.md

**Category:** Analyzer + Validator

| Required Section | Present | Gap Severity | Notes |
|-----------------|---------|--------------|-------|
| 1. YAML Frontmatter | Yes | None | 7 of 9 fields present (missing proactive_triggers, version) |
| 2. Title | Yes | None | "# Security Auditor" matches identifier |
| 3. Purpose | Yes | None | 2-sentence purpose description |
| 4. When Invoked | Yes | None | All 3 subsections present |
| 5. Input/Output Specification | No | High | No input/output specification; sources implied by workflow |
| 6. Constraints and Boundaries | No | High | No dedicated constraints section |
| 7. Workflow | Yes | None | 6-step numbered workflow |
| 8. Success Criteria | Yes | None | 6-item checklist present |
| 9. Output Format | Yes | None | "Security Report Format" with 7-section structure |
| 10. Examples | No | Medium | No Task() invocation example |

**Frontmatter Compliance:** 7/9 fields -- missing `proactive_triggers` and `version` (both optional, acceptable).

### Gap Analysis Summary

| Gap Pattern | Frequency | Severity | Remediation |
|-------------|-----------|----------|-------------|
| Missing Input/Output Specification | 3/3 agents | Medium-High | Add explicit I/O section; extract from workflow descriptions |
| Missing Constraints and Boundaries | 3/3 agents | High | Add dedicated section; extract implied restrictions |
| Missing Examples (Task() pattern) | 3/3 agents | Medium | Add at least 1 invocation example |
| Missing Output Format | 1/3 agents | Medium | Formalize implicit output structure |
| Missing version field | 2/3 agents | Low | Optional field; add during migration |

**Key Finding:** No information loss occurs when mapping existing agent content to template sections. All existing content fits within the 10 required sections. The primary gaps are missing sections (Constraints, I/O Spec, Examples) that would improve agent clarity and integration documentation.

---

## Appendix B: Extension Sections

Agents may include additional domain-specific sections beyond the required 10 and category-specific optional sections. Extension sections are permitted under these rules:

1. Extension sections use H2 (`##`) headings
2. Section titles are action-oriented (e.g., "Error Handling", "Integration", "Token Efficiency")
3. Extension sections must NOT duplicate required section content
4. Extension sections appear after the 10 required sections
5. Common extensions: Error Handling, Integration, Token Efficiency, References, Observation Capture

---

## References

- **Source**: tech-stack.md, lines 385-399 (component size limits, progressive disclosure)
- **Source**: source-tree.md, lines 593-608 (agent file constraints, progressive disclosure)
- **Source**: coding-standards.md, lines 56-68 (YAML frontmatter standards)
- **Source**: architecture-constraints.md, lines 46-63 (subagent design constraints)
- **Related**: `.claude/agents/agent-generator/references/frontmatter-specification.md`
- **Related**: `.claude/agents/agent-generator/references/template-patterns.md`
