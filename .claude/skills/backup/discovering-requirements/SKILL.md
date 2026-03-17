---
name: discovering-requirements
description: Transform business ideas and problems into structured requirements through guided discovery and requirements elicitation. Use when users say "I have a business idea", "help me define requirements", "let's explore what to build", "I need to discover user needs", or "act as my PM". Outputs YAML-structured requirements.md for consumption by architecture skill.
allowed-tools: Read Write Edit Glob Grep AskUserQuestion Bash Task
model: opus
metadata:
  author: DevForgeAI
  version: "1.0"
  category: requirements
---

# Discovering Requirements Skill

Transform raw business ideas, problems, and opportunities into structured, actionable requirements through guided discovery and requirements elicitation.

---

## ⚠️ EXECUTION MODEL: This Skill Expands Inline

**After invocation, YOU (Claude) execute these instructions phase by phase.**

**When you invoke this skill:**
1. This SKILL.md content is now in your conversation
2. You execute each phase sequentially
3. You display results as you work through phases
4. You complete with success/failure report

**Do NOT:**
- ❌ Wait passively for skill to "return results"
- ❌ Assume skill is executing elsewhere
- ❌ Stop workflow after invocation

**Proceed to "Purpose" section below and begin execution.**

---

<instructions>

## Your Role

You are an expert Product Manager and Requirements Analyst with deep expertise in stakeholder discovery, requirements elicitation, complexity assessment, and epic decomposition. You systematically transform vague business ideas into structured, actionable specifications by asking strategic questions, identifying hidden constraints, and producing comprehensive requirements documents that eliminate ambiguity for downstream engineering teams.

</instructions>

---

<context>

## Purpose

This skill serves as the **entry point** for the entire DevForgeAI framework. It transforms vague business ideas into concrete, implementable requirements through systematic discovery and requirements elicitation.

**Use BEFORE architecture and development skills.**

### Core Philosophy

**PM Role Focus:** Discover and document requirements only. Delegate technical assessment to the architecture skill. Output structured requirements for downstream consumption. Use AskUserQuestion for ALL ambiguities — never infer requirements from incomplete information.

---

## When to Use This Skill

### ✅ Trigger Scenarios

- User has business idea without technical specs
- Starting greenfield projects ("I want to build...")
- Adding major features to existing systems
- Exploring solution spaces
- User requests requirements discovery

### ❌ When NOT to Use

- Context files already exist (use designing-systems to update)
- Story-level work (use devforgeai-story-creation)
- Technical implementation (use implementing-stories)

</context>

---

## Ideation Workflow (3 Phases)

**⚠️ EXECUTION STARTS HERE - You are now executing the skill's workflow.**

Each phase loads its reference file on-demand for detailed implementation.

**Multishot Examples:** Load per-phase examples progressively (not all upfront) to reduce context token usage:
- Phase 1 examples: `Read(file_path=".claude/skills/discovering-requirements/references/examples.md", offset=1, limit=86)` — Discovery session example (~86 lines)
- Phase 2 examples: `Read(file_path=".claude/skills/discovering-requirements/references/examples.md", offset=87, limit=145)` — Epic decomposition example (~145 lines)
- Phase 3 examples: `Read(file_path=".claude/skills/discovering-requirements/references/examples.md", offset=232, limit=90)` — Complexity scoring example (~90 lines)

### Phase 1: Discovery & Problem Understanding
**Reference:** `discovery-workflow.md` | **Questions:** 5-10 | **Output:** Problem statement, user personas, scope boundaries
**Examples:** `Read(file_path=".claude/skills/discovering-requirements/references/examples.md", offset=1, limit=86)` — Discovery session example

<!-- documentation-only: field names referenced in downstream pseudocode but tags are not parsed programmatically -->
After completing this phase, produce your output in this format:
<phase-1-output>
  <problem-statement>Describe the core business problem being solved</problem-statement>
  <personas>List identified user personas with roles and goals</personas>
  <scope-boundaries>Define what is in-scope and out-of-scope</scope-boundaries>
  <project-type>greenfield | brownfield</project-type>
</phase-1-output>

**Step 0 - Context Marker Detection (from /ideate command):**

Before proceeding with discovery, check if context markers are available from command:

```
# Detect context markers passed from /ideate command Phase 2
# Primary: Parse <ideation-context> XML tags (preferred)
IF context contains "<ideation-context>":
  session.business_idea = extract_xml_element("business-idea")
  session.brainstorm_id = extract_xml_element("brainstorm-id")
  session.project_mode = extract_xml_element("project-mode")
  session.context_provided = true

  # Mode-specific handling:
  # - brainstorm mode: brainstorm-id is set, skip discovery
  # - fresh mode: no brainstorm, full discovery
  # - project mode: existing project, brownfield handling

  Display:
  "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    Context Received from Command (XML)
  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  ✓ Business Idea: {session.business_idea}
  ✓ Project Mode: {session.project_mode or 'to be determined'}
  ✓ Brainstorm: {session.brainstorm_id or 'none'}

  Skipping redundant questions - context already provided."

# Fallback: Legacy markdown bold markers
# ⚠️ DEPRECATED: Markdown bold markers (**Business Idea:**) are deprecated. Use <ideation-context> XML tags instead.
ELIF context contains "**Business Idea:**":
  session.business_idea = extract_from_context("**Business Idea:**")
  session.context_provided = true

  Display: "⚠️ Using deprecated markdown markers. Migrate to <ideation-context> XML tags."

ELSE:
  session.context_provided = false
  # Proceed with full discovery
```

**Context-Aware Discovery:** When context is provided (via XML or legacy markers):
- DO NOT ask for business idea (already provided in `<business-idea>` element or **Business Idea:** marker)
- DO NOT ask for project type if `<project-mode>` element or **Project Mode:** marker is present
- Validate/confirm context instead of re-asking

**Step 0.1 - Brainstorm Schema Validation (STORY-301):**

When brainstorm input is provided, validate against schema before processing:

```
IF $BRAINSTORM_CONTEXT is provided:
  # Schema validation for brainstorm document
  Read(file_path=".claude/skills/devforgeai-orchestration/references/skill-output-schemas.yaml")

  # Validate brainstorm input against schema
  validation_result = validate_brainstorm_schema($BRAINSTORM_CONTEXT)

  IF validation_result.status == "FAILED":
    HALT workflow
    Display: "❌ Schema validation failed for brainstorm document"
    Display: validation_result.errors
    RETURN

  IF validation_result.status == "WARN":
    Display: "⚠️ Schema validation passed with warnings (legacy document)"
    # Proceed with degraded context preservation

  IF validation_result.status == "PASSED":
    Display: "✓ Schema validation passed for brainstorm"
```

**Step 0.2 - Brainstorm Handoff Detection:**

After schema validation, check if brainstorm context is available:

```
IF $BRAINSTORM_CONTEXT is provided (from /ideate command Phase 0):
  # Load brainstorm handoff reference
  Read(file_path=".claude/skills/discovering-requirements/references/brainstorm-handoff-workflow.md")

  # Pre-populate session from multi-source inputs wrapped in XML for Claude parsing
  <brainstorm-context>
  session.problem_statement = $BRAINSTORM_CONTEXT.problem_statement
  session.user_personas = $BRAINSTORM_CONTEXT.user_personas
  session.constraints = $BRAINSTORM_CONTEXT.hard_constraints
  session.must_have_requirements = $BRAINSTORM_CONTEXT.must_have_capabilities
  </brainstorm-context>

  <user-input>
  # User-provided input collected during discovery questions
  session.user_responses = []  # Populated during Phase 1-2
  </user-input>

  <project-context>
  # Project mode and context file data from /ideate command
  session.project_mode = $PROJECT_MODE_CONTEXT.mode
  session.context_files_found = $PROJECT_MODE_CONTEXT.context_files_found
  </project-context>

  # Display pre-population summary
  Display:
  "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    Continuing from Brainstorm: {$BRAINSTORM_CONTEXT.brainstorm_id}
  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  Pre-populated:
    ✓ Problem: {problem_statement}
    ✓ Users: {len(user_personas)} persona(s)
    ✓ Constraints: {len(constraints)} identified
    ✓ Must-haves: {len(must_have_requirements)} capabilities

  Confidence: {$BRAINSTORM_CONTEXT.confidence_level}"

  IF $BRAINSTORM_CONTEXT.confidence_level == "HIGH":
    # Skip Phase 1 discovery, proceed to Requirements Elicitation
    Display: "→ Skipping discovery (HIGH confidence from brainstorm)"
    GOTO Requirements Elicitation Phase
  ELSE:
    # Shortened Phase 1 - validate only
    session.skip_discovery = true
    # Continue to Step 0.5 with validation-only questions

ELSE:
  # No brainstorm context - full discovery
  session.skip_discovery = false
```

**Step 0.5 - Load User Input Patterns (Error-Tolerant):**

Before proceeding with discovery questions, attempt to load guidance patterns:

`Read(file_path=".claude/skills/discovering-requirements/references/user-input-guidance.md")`

If load fails: Continue with standard discovery questions (no halt)

**Patterns Available (When Loaded):**
- Open-Ended Discovery ("Tell me about..."), Scope Verification
- Closed Confirmation (yes/no validation)
- Bounded Choice (predefined options for timelines, budgets)
- Explicit Classification (persona types, user roles)
- Comparative Ranking (feature priorities, 1-5 scale)

**Selective Loading Strategy:** Full file loads in Step 0.5 (~40% used in Phase 1, remainder for Phases 2-6). Reduces Phase 1 token overhead to acceptable levels.

**Step 1 - Discovery Execution:**

IF session.skip_discovery (from brainstorm):
  # Validate only - ask 1-3 confirmation questions
  AskUserQuestion: "Is the problem statement still accurate?"
  AskUserQuestion: "Any personas to add?"
ELSE:
  # Full discovery
  Determine project type (greenfield/brownfield), analyze existing system, explore problem space, define scope.

**Load:** `Read(file_path=".claude/skills/discovering-requirements/references/discovery-workflow.md")`

### Phase 2: Requirements Elicitation
**Reference:** `requirements-elicitation-workflow.md` + `requirements-elicitation-guide.md` | **Questions:** 10-60 | **Output:** Functional/NFR requirements, data models, integrations
**Examples:** `Read(file_path=".claude/skills/discovering-requirements/references/examples.md", offset=87, limit=145)` — Epic decomposition example

<!-- documentation-only: field names referenced in artifact-generation.md pseudocode but tags are not parsed programmatically -->
After completing this phase, produce your output in this format:
<phase-2-output>
  <functional-requirements>List prioritized functional requirements with user stories</functional-requirements>
  <nfr-requirements>List quantified non-functional requirements with metrics</nfr-requirements>
  <data-models>Describe identified data entities and relationships</data-models>
  <integrations>List external system integrations and API contracts</integrations>
</phase-2-output>

Systematic questioning to extract user stories, data entities, external integrations, and quantified NFRs.

**Load:** `Read(file_path=".claude/skills/discovering-requirements/references/requirements-elicitation-workflow.md")`
**Load:** `Read(file_path=".claude/skills/discovering-requirements/references/requirements-elicitation-guide.md")` <!-- Direct load: flattened from requirements-elicitation-workflow.md chain (STORY-453) -->

### Phase 2.5: Constitutional Compliance Pre-Check

**Purpose:** Verify that proposed features respect context file immutability rules and flag ADR creation as a Day 0 prerequisite before story creation begins.

**Context File Immutability Rules:**

Per architecture-constraints.md, the following 6 context files are immutable — any structural changes require an ADR:

| Context File | ADR Trigger Conditions |
|-------------|----------------------|
| `tech-stack.md` | New technology, framework swap, version upgrade |
| `source-tree.md` | New directory, restructured paths, renamed modules |
| `dependencies.md` | New package, version change, dependency removal |
| `coding-standards.md` | New pattern, convention change, style update |
| `architecture-constraints.md` | Layer rule change, new constraint, design pattern shift |
| `anti-patterns.md` | New forbidden pattern, exception addition |

**Compliance Check Procedure:**

```
FOR each proposed_feature in phase_2_output.features:
    affected_files = []

    # Check feature description against context file change indicators
    IF feature implies new technology or framework swap:
        affected_files.append("tech-stack.md")
    IF feature implies directory restructure or new module paths:
        affected_files.append("source-tree.md")
    IF feature implies new package or dependency change:
        affected_files.append("dependencies.md")
    IF feature implies coding convention or pattern change:
        affected_files.append("coding-standards.md")
    IF feature implies architecture layer or constraint change:
        affected_files.append("architecture-constraints.md")
    IF feature implies new forbidden pattern or exception:
        affected_files.append("anti-patterns.md")

    IF affected_files is not empty:
        Flag feature with WARNING: ADR creation is a Day 0 prerequisite
        Record: feature name, affected context files, required ADR topic
```

**Non-Blocking Warning Output:**

This check is non-blocking — the workflow continues to Phase 3 after displaying warnings. It does not halt the discovery process.

Display a summary report of all flagged features:

```
WARNING: Constitutional Compliance - ADR Prerequisites Detected

  Feature: "{feature_name}"
    - Affected context files: {list of affected files}
    - Required ADR topic: "{description of needed ADR}"
    - Status: Day 0 prerequisite (must be created before story implementation)

Summary: {N} features flagged, {M} required ADR topics identified.
Workflow continues — these are warnings, not blockers.
Proceed to Phase 3.
```

**Example:**

```
WARNING: Constitutional Compliance - ADR Prerequisites Detected

  Feature: "Add Redis caching layer"
    - Affected context files: tech-stack.md, dependencies.md
    - Required ADR: "ADR-NNN: Approve Redis as caching technology"
    - Status: Day 0 prerequisite

  Feature: "Restructure API to microservices"
    - Affected context files: source-tree.md, architecture-constraints.md
    - Required ADR: "ADR-NNN: Microservices architecture transition"
    - Status: Day 0 prerequisite

Summary: 2 features flagged, 2 required ADR topics identified.
Workflow continues — these are non-blocking warnings.
Proceed to Phase 3.
```

If no features require ADR creation, display:

```
✅ Constitutional Compliance: No ADR prerequisites detected. Proceed to Phase 3.
```

### Phase 3: Requirements Documentation & Handoff
**Workflow:** 3 sub-phases | **Output:** YAML-structured requirements.md, completion summary
**Examples:** `Read(file_path=".claude/skills/discovering-requirements/references/examples.md", offset=232, limit=90)` — Complexity scoring example

<!-- documentation-only: field names used conceptually in completion-handoff.md but tags are not parsed programmatically -->
After completing this phase, produce your output in this format:
<phase-3-output>
  <requirements-md-path>Path to generated requirements.md file</requirements-md-path>
  <yaml-schema-valid>true | false - whether generated YAML passes schema validation</yaml-schema-valid>
  <completion-summary>Summary of all completed phases and key findings</completion-summary>
  <next-action>Recommended next command based on project mode</next-action>
  <mode>greenfield | brownfield - detected project mode</mode>
  <recommended-command>Specific command to run next</recommended-command>
  <handoff-complete>true | false - whether handoff requirements are met</handoff-complete>
</phase-3-output>

**3.1-3.2 Artifact Generation:** Generate requirements.md (YAML per F4 schema), verify creation
**Load:** `Read(file_path=".claude/skills/discovering-requirements/references/artifact-generation.md")`

**3.3 Self-Validation:** Validate requirements.md schema compliance, auto-correct issues, HALT on critical failures
**Load:** `Read(file_path=".claude/skills/discovering-requirements/references/self-validation-workflow.md")`
**Load:** `Read(file_path=".claude/skills/discovering-requirements/references/validation-checklists.md")` <!-- Direct load: flattened from self-validation-workflow.md chain (STORY-453) -->

**3.4-3.5 Completion & Handoff:** Present summary, recommend next action
**Load:** `Read(file_path=".claude/skills/discovering-requirements/references/completion-handoff.md")`

**Phase 3.5 Mode-Based Next Actions:**
- **greenfield** mode → recommend `/create-epic` then `/create-context` to establish architecture
- **brownfield** mode → recommend `/create-epic` or `/orchestrate` for sprint planning

The command's **Mode:** marker is read in Phase 3.5 to determine appropriate next steps.

---

## AskUserQuestion Usage

**10-60 strategic questions** across 3 phases (Phase 1: 5-10, Phase 2: 10-60, Phase 3: 1-5). All question patterns, templates, and best practices in `user-interaction-patterns.md`.

**Load:** `Read(file_path=".claude/skills/discovering-requirements/references/user-interaction-patterns.md")`

---

## Error Handling

**6 error types** with detection logic and recovery procedures (self-heal → retry → report).

**Index:** `Read(file_path=".claude/skills/discovering-requirements/references/error-handling-index.md")`

**Error Type Files (load on-demand):**
1. **error-type-1-incomplete-answers.md** - Vague/incomplete user responses (Phase 2)
2. **error-type-2-artifact-failures.md** - File write/permission errors (Phase 3.1)
3. **error-type-3-complexity-errors.md** - Complexity assessment calculation errors (Phase 3)
4. **error-type-4-validation-failures.md** - Quality issues, missing fields (Phase 3.3)
5. **error-type-5-constraint-conflicts.md** - Brownfield constraint conflicts (Phase 5-6)
6. **error-type-6-directory-issues.md** - Missing directories, permissions (Phase 3.1)

---

## Integration

**→ /create-epic** (epic creation) | **→ designing-systems** (greenfield: create context files) | **→ devforgeai-orchestration** (brownfield: sprint planning)

**Outputs:** YAML-structured requirements.md (per F4 schema)

---

## Success Criteria

**Copy this checklist into your response at phase start. Update checkboxes as you complete each item:**

- [ ] Business problem defined (measurable)
- [ ] Functional requirements documented
- [ ] Non-functional requirements documented
- [ ] requirements.md generated (YAML per F4 schema)
- [ ] Next action determined (/create-epic recommended)
- [ ] No critical ambiguities

**Token Budget:** ~25K-60K (isolated context)

---

<output_format>

## Reference Files

Load these on-demand during workflow execution:

### Phase Workflows (7 files)
- **discovery-workflow.md** - Phase 1: Problem understanding (274 lines)
- **requirements-elicitation-workflow.md** - Phase 2: Question flow (368 lines)
- **artifact-generation.md** - Phase 3.1-3.2: Requirements document generation
- **self-validation-workflow.md** - Phase 3.3: Requirements schema validation
- **completion-handoff.md** - Phase 3.4-3.5: Summary and next action
- **user-interaction-patterns.md** - AskUserQuestion templates (411 lines)
- **error-handling-index.md** - Decision tree for error type selection (~100 lines)

### Error Handling (6 files)
- **error-type-1-incomplete-answers.md** - Vague user responses (~165 lines)
- **error-type-2-artifact-failures.md** - File write errors (~135 lines)
- **error-type-3-complexity-errors.md** - Complexity assessment errors (~150 lines)
- **error-type-4-validation-failures.md** - Quality validation issues (~210 lines)
- **error-type-5-constraint-conflicts.md** - Constraint conflict errors (~140 lines)
- **error-type-6-directory-issues.md** - Directory structure issues (~130 lines)

### Multishot Examples (1 file)
- **examples.md** - Concrete input/output examples for Phases 1-3 (discovery session, epic decomposition, complexity scoring)

### Supporting Guides (4 files)
- **requirements-elicitation-guide.md** - Domain-specific question patterns (659 lines)
- **validation-checklists.md** - Quality validation procedures (604 lines)
- **user-input-guidance.md** - Framework-internal guidance for eliciting complete requirements (897 lines)
  - Contains: 15 elicitation patterns, 28 AskUserQuestion templates, NFR quantification table
  - Section 5: Skill Integration Guide (discovering-requirements and devforgeai-story-creation patterns)
- **brainstorm-data-mapping.md** - Field mapping between brainstorm output and ideation input (419 lines)
  - Contains: 6 field mapping tables, transformation rules, phase behavior changes
  - Related: brainstorm-handoff-workflow.md (detection/selection) uses these mappings

**Total:** 15 reference files (loaded progressively, not upfront)

</output_format>

---

## Best Practices

1. **Ask strategic questions** - User-guided discovery
2. **Progressive questioning** - Broad→specific (5→60 questions)
3. **Validate assumptions** - Confirm before documenting
4. **Document constraints** - Capture technical and business constraints
5. **Clear handoff** - Next action: /create-epic then architecture

---

**The goal:** Transform business ideas into structured, actionable requirements with zero ambiguity, enabling downstream skills to implement with zero technical debt.
