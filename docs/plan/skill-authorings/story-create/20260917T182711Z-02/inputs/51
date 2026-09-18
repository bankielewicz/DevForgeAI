# Phase 2: Requirements Analysis

Generate user story and acceptance criteria using requirements-analyst subagent.

## Overview

This phase transforms the feature description into structured user story format and testable acceptance criteria following DevForgeAI standards.

**RCA-007 Enforcement (hook/CLI-backed — no procedural pseudocode):**
- Step 2.0: Sidecar prevention — enforced by `stories-sidecar-write-blocker.sh` and tool whitelist (citation)
- Step 2.1: Subagent invocation with content-only constraints (enhanced prompt)
- Step 2.1.5: File creation validation — enforced by hook + tool whitelist (citation)
- Step 2.2: Quality validation (section headers, AC format, NFR measurability)
- Step 2.2.5: Contract validation — enforced by `validate-subagent-contract` CLI (citation)
- Step 2.2.7: Post-invocation diff — superseded by hook; `validate-subagent-contract` is the structural check (citation)
- Step 2.3: Refine if incomplete

---

## Step 2.0: Pre-Invocation File System Snapshot (RCA-007 Phase 2)

> Enforcement: `stories-sidecar-write-blocker.sh` (PreToolUse[Write|Edit]) and `story-requirements-analyst` tool whitelist (no Write/Edit tools) make sidecar creation structurally impossible — no pre-flight snapshot is required.

---

## Step 2.1: Invoke Requirements Analyst Subagent (ENHANCED - RCA-007 Fix)

**Objective:** Generate user story, acceptance criteria, edge cases, and NFRs

**IMPORTANT:** This prompt has been enhanced to prevent RCA-007 violations (multi-file creation). The subagent MUST return content only (no file creation).

**Prepare detailed prompt for subagent:**

```
Task(
  subagent_type="story-requirements-analyst",  # UPDATED: Skill-specific (RCA-007 Phase 3)
  description="Generate user story content",
  prompt="""Transform feature description into structured user story for DevForgeAI framework.

**═══════════════════════════════════════════════════════════════════════════**
**PRE-FLIGHT BRIEFING:**
**═══════════════════════════════════════════════════════════════════════════**

You are being invoked by the spec-driven-stories skill.
This skill will assemble your output into a single .story.md file using story-template.md.

**YOUR ROLE:**
- Generate requirements content (user story, acceptance criteria, edge cases, NFRs)
- Return content as markdown sections
- Do NOT create files
- Parent skill handles file creation (Phase 5: Story File Creation)

**OUTPUT WILL BE USED IN:**
- Phase 5: Story File Creation (assembly into story-template.md)
- Your output is CONTENT for assembly, not a complete deliverable

**WORKFLOW CONTEXT:**
- Current workflow: Story creation (8-phase process)
- Current phase: Phase 2 (Requirements Analysis)
- Next phase: Phase 3 (Technical Specification)
- Final artifact: devforgeai/specs/Stories/{story_id}-{slug}.story.md

**═══════════════════════════════════════════════════════════════════════════**
**CRITICAL OUTPUT CONSTRAINTS:**
**═══════════════════════════════════════════════════════════════════════════**

1. **Format:** Return ONLY markdown text content (no file creation)
2. **Content:** Output will be inserted into story-template.md by parent skill
3. **Files:** Do NOT create separate files (SUMMARY.md, QUICK-START.md, VALIDATION-CHECKLIST.md, FILE-INDEX.md, DELIVERY-SUMMARY.md)
4. **Structure:** Output as sections: User Story, Acceptance Criteria, Edge Cases, Data Validation Rules, Non-Functional Requirements
5. **Assembly:** Parent skill (spec-driven-stories) will assemble all sections into single .story.md file
6. **Size:** Maximum 50,000 characters (fits in story-template.md capacity)

**Contract Reference:** .claude/skills/spec-driven-stories/contracts/requirements-analyst-contract.yaml

**═══════════════════════════════════════════════════════════════════════════**
**PROHIBITED ACTIONS:**
**═══════════════════════════════════════════════════════════════════════════**

You MUST NOT:
1. ❌ Create files using Write tool
2. ❌ Create files using Edit tool on non-existent files
3. ❌ Create files using Bash with output redirection (>, >>, cat <<EOF)
4. ❌ Return file paths as output (e.g., "Created: STORY-009-summary.md")
5. ❌ Return file creation statements (e.g., "File created successfully")
6. ❌ Generate multi-file deliverables (SUMMARY, QUICK-START, INDEX, etc.)
7. ❌ Write to disk in any form
8. ❌ Create comprehensive project structures (you generate CONTENT, not PROJECTS)

**Why prohibited:**
- Parent skill handles all file creation (Phase 5: Story File Creation)
- Your output is assembled with other content (tech spec from Phase 3, UI spec from Phase 4)
- Multi-file output violates DevForgeAI single-file design
- Creates framework specification violations (RCA-007)

**What to do instead:**
- ✅ Return markdown text as string
- ✅ Structure content with section headers (## User Story, ## Acceptance Criteria, etc.)
- ✅ Include all required information in text output
- ✅ Let parent skill decide file structure and naming

**═══════════════════════════════════════════════════════════════════════════**
**EXPECTED OUTPUT FORMAT:**
**═══════════════════════════════════════════════════════════════════════════**

Your output should look like this (MARKDOWN TEXT, not files):

```markdown
## User Story
**As a** [role - specific persona, not "user"],
**I want** [action - what functionality],
**so that** [benefit - business value].

## Acceptance Criteria

### AC1: [Clear, testable title]
**Given** [context - initial state]
**When** [action - what happens]
**Then** [outcome - expected result]

### AC2: [Title]
**Given** [context]
**When** [action]
**Then** [outcome]

### AC3: [Title]
**Given** [context]
**When** [action]
**Then** [outcome]

(Minimum 3 acceptance criteria)

## Edge Cases
1. **[Edge case scenario]:** [Description and expected behavior]
2. **[Edge case scenario]:** [Description]

(Minimum 2 edge cases)

## Data Validation Rules
1. **[Input parameter]:** [Validation rule]
2. **[Data format]:** [Validation rule]

## Non-Functional Requirements

### Performance
- Response time: [MEASURABLE - e.g., "< 100ms per request (p95)"]
- Throughput: [MEASURABLE - e.g., "1000 requests/second"]

### Security
- Authentication: [SPECIFIC - e.g., "JWT tokens with 15-min expiry"]
- Authorization: [SPECIFIC - e.g., "RBAC with admin/user roles"]

### Reliability
- Error handling: [SPECIFIC - e.g., "Return 400 with error details"]

### Scalability
- Concurrency: [MEASURABLE - e.g., "10,000 concurrent users"]
```

**What your output will become:**
Parent skill will insert your output into story-template.md at line 45:

```markdown
---
id: {story_id}
title: {title}
...
---

## User Story
{YOUR OUTPUT: User Story section}

## Acceptance Criteria
{YOUR OUTPUT: Acceptance Criteria section}

## Technical Specification
{Generated by Phase 3}

## Non-Functional Requirements
{YOUR OUTPUT: NFRs section}

## Edge Cases
{YOUR OUTPUT: Edge Cases section}

...
```

**Final result:** Single .story.md file at devforgeai/specs/Stories/{story_id}-{slug}.story.md

**═══════════════════════════════════════════════════════════════════════════**
**NOW PROCEED WITH REQUIREMENTS ANALYSIS:**
**═══════════════════════════════════════════════════════════════════════════**

**Feature Description:** {feature_description}

**Story Context:**
- Story ID: {story_id}
- Epic: {epic_id or 'None'}
- Priority: {priority}
- Points: {points}

**Generate the following sections as markdown text (NOT files):**

1. **User Story** (As a/I want/So that format)
   - Role: Specific user type (not generic "user")
   - Action: What the user wants to do
   - Benefit: Why this matters (business value)

2. **Acceptance Criteria** (Given/When/Then format, minimum 3)
   - Happy path scenario
   - Error/edge case scenarios
   - Data validation scenarios
   - Each criterion must be testable (can verify pass/fail)

3. **Edge Cases** (minimum 2)
   - Boundary conditions
   - Error conditions
   - Concurrent access scenarios
   - Data corruption scenarios

4. **Data Validation Rules**
   - Input constraints
   - Format requirements
   - Business rule validations

5. **Non-Functional Requirements**
   - Performance: Response time targets (e.g., <500ms, <100ms)
   - Security: Authentication, authorization, encryption needs
   - Reliability: Error handling, retry logic
   - Scalability: Concurrent user targets

**DevForgeAI Standards:**
- No vague terms ("fast", "secure", "user-friendly" without metrics)
- All NFRs must be measurable
- All acceptance criteria must be testable
- Follow spec-driven development principles

**REMINDER:** Return MARKDOWN TEXT ONLY. No file creation. No file paths in output.
"""
)
```

**Expected subagent output:**
- Markdown text with clear section headers
- User story in proper format
- 3+ acceptance criteria (Given/When/Then)
- Edge cases list (minimum 2)
- Data validation rules
- Quantified NFRs (all measurable)
- **NO file creation statements**
- **NO file paths in output**

**Subagent Migration Note (RCA-007 Phase 3):**

**Previous:** General-purpose `requirements-analyst` (`.claude/agents/requirements-analyst.md`)
- Tools: Read, Write, Edit, Grep, Glob, AskUserQuestion
- Purpose: Requirements analysis for ANY context
- Output: May create comprehensive deliverables (6 files)
- Issue: Created STORY-009-SUMMARY.md, QUICK-START.md, VALIDATION-CHECKLIST.md, FILE-INDEX.md, DELIVERY-SUMMARY.md (RCA-007 violation)

**Current:** Skill-specific `story-requirements-analyst` (`.claude/agents/story-requirements-analyst.md`)
- Tools: Read, Grep, Glob, AskUserQuestion (NO Write/Edit)
- Purpose: Requirements ONLY for spec-driven-stories
- Output: ONLY markdown content (file creation impossible by design)
- Fix: Cannot create files (Write/Edit tools not available)

**Migration Date:** 2025-11-06

**Fallback:** If `story-requirements-analyst` not available (not deployed yet), falls back to `requirements-analyst` with Phase 1+2 constraints (enhanced prompt + validation checkpoints).

**Benefit:** 99.9% violation prevention vs. 95-99% with general-purpose + constraints

---

## Step 2.1.5: Validate No File Creation (RCA-007 Fix)

> Enforcement: `stories-sidecar-write-blocker.sh` (PreToolUse[Write|Edit]) blocks sidecar Write/Edit at the OS hook layer; `story-requirements-analyst` tool whitelist (no Write/Edit) makes file creation impossible by design; `validate-subagent-contract` (Step 2.3) validates the content-only return contract.

---

## Step 2.1.7: Refactor Story Content-Preservation Analysis [CONDITIONAL]

**Trigger:** Execute ONLY when `type: refactor` in story YAML frontmatter.

**Purpose:** Analyze source files being refactored to auto-generate content-preservation ACs that prevent logic loss. Without this step, refactor stories generate only size-reduction ACs (proxy metrics) without content-completeness ACs (substance).

**Reference:** EPIC-071 STORY-457 revert — ACs measured structure/size but not content. This step prevents that failure mode.

**Skip conditions:** Do NOT execute for `type: feature`, `type: bugfix`, `type: documentation`.

**Procedure:**

### 1. Extract target file paths from epic feature description

```
Read epic feature section referenced in story provenance
Extract file paths mentioned in "Files to modify" or inline references
Store as: target_files[]
```

### 2. Read and inventory each target file

```
FOR each file in target_files:
    Read(file_path=file)

    display_count = Grep(pattern="Display:", path=file) count
    askuser_count = Grep(pattern="AskUserQuestion", path=file) count
    error_blocks = Grep(pattern="^### Error", path=file) count
    governance_sections = Grep(pattern="Architecture|Hook Integration|Integration Pattern|
                                Feedback Hook|Quality Gates|Framework Integration", path=file)
    help_sections = Grep(pattern="^## |^### ", path=file) count
    for_loops = Grep(pattern="FOR ", path=file) count

    Store inventory: {file, display_count, askuser_count, error_blocks,
                      governance_sections, help_sections, for_loops}
```

### 3. Generate preservation ACs from inventory

```
ac_number = next_available_ac_number

IF sum(display_count) > 0:
    Generate AC using Template 1 (Content Preservation)
    Fill: display_count, error_count, governance section names

IF sum(askuser_count) > 0:
    Generate AC using Template 3 (AskUserQuestion Placement)
    Fill: askuser_count per file, lean orchestration reference

    Generate AC using Template 5 (Interactive Prompt Completeness)
    Fill: enumerate each prompt's purpose and options

IF sum(error_blocks) > 0:
    Include in Content Preservation AC: "{error_count} error types: {list_names}"

IF len(governance_sections) > 0:
    Include in Content Preservation AC: governance section names

ALWAYS for refactor stories:
    Generate AC using Template 2 (Backward-Compatible Output)
    Fill: all invocation modes from Quick Reference sections

    Generate DoD items using Template 6 (Golden Output Capture)
    Fill: mode_count, section_count, error_count
```

**Template Reference:** See `acceptance-criteria-refactor.md` for all 6 templates and placeholder definitions. (Previously in `acceptance-criteria-patterns.md` "Refactor Story Patterns" section, now split into its own file for conditional loading.)

### 4. Add STORY-457 Lessons Learned note

```
Append to story Notes section:

**STORY-457 Lessons Learned (Auto-Generated):**
- ACs must measure content completeness, not just size/structure
- Source file inventory: {summarize_counts}
- Content-preservation ACs auto-generated from source file analysis
- Reference: lean-orchestration-pattern.md line 104 (AskUserQuestion in commands)
```

---

## Step 2.2: Validate Subagent Output Quality (RENUMBERED from Step 2.2)

**Objective:** Ensure requirements meet DevForgeAI quality standards

**Load acceptance criteria patterns for validation:**
```
# Both files already loaded in Phase 02 Reference Loading — no re-read needed.
# If loading fresh:
Read(file_path=".claude/skills/spec-driven-stories/references/acceptance-criteria-core.md")
Read(file_path=".claude/skills/spec-driven-stories/references/acceptance-criteria-domains.md")
```

**Validation checks:**

```
Validate user story:
- [ ] Follows "As a [role], I want [action], so that [benefit]" format
- [ ] Role is specific (not "user", but "customer", "admin", "developer")
- [ ] Action is clear and unambiguous
- [ ] Benefit articulates business value

Validate acceptance criteria:
- [ ] Minimum 3 criteria
- [ ] Each follows Given/When/Then structure
- [ ] At least 1 happy path scenario
- [ ] At least 1 error/edge case scenario
- [ ] All criteria are testable (can write automated test)
- [ ] No ambiguous language ("should", "might", "could")

Validate NFRs:
- [ ] Performance targets quantified (e.g., "<500ms response time")
- [ ] Security requirements specific (e.g., "OAuth2 authentication, JWT tokens")
- [ ] No vague terms without metrics

If validation fails:
    # Re-invoke requirements-analyst with specific feedback
    # Or use AskUserQuestion to fill gaps
```

---

## Step 2.2.5: Contract-Based Validation (RCA-007 Phase 2)

> Enforcement: `devforgeai-validate validate-subagent-contract` (Step 2.3) enforces the requirements-analyst contract (no file creation, required sections, AC format, NFR measurability, output size). The Python validation loop is superseded by this CLI gate.

---

## Step 2.2.7: Post-Invocation File System Diff (RCA-007 Phase 2)

> Enforcement: Post-invocation diff is superseded — `stories-sidecar-write-blocker.sh` exit-2's before any Write completes, making unauthorized file creation impossible. `validate-subagent-contract` (Step 2.3) provides the structural check.

---

## Step 2.3: Refine if Incomplete (RENUMBERED from Step 2.3)

**Objective:** Fill gaps in subagent output via user questions

**If subagent output incomplete or vague:**

```
Use AskUserQuestion to clarify:

Example: If NFR says "fast"
Question: "What performance target is acceptable?"
Options:
  - "High performance (<100ms response, >10k concurrent users)"
  - "Standard performance (<500ms response, 1k-10k users)"
  - "Moderate performance (<2s response, <1k users)"

Example: If acceptance criteria vague
Question: "What specific behavior should be tested?"
Options:
  - Provide examples of good AC
  - Ask for edge cases
  - Request error scenarios
```

---

## Subagent Coordination

**Subagent used:** requirements-analyst

**Invoked by:** This phase (Step 2.1)

**Input provided:**
- Feature description
- Story metadata (ID, epic, priority, points)
- DevForgeAI standards

**Output expected:**
- User story
- 3+ acceptance criteria
- Edge cases
- Data validation rules
- Measurable NFRs

**Reference files used by subagent:**
- acceptance-criteria-core.md (~280 lines — core principles + universal patterns)
- acceptance-criteria-domains.md (~1,020 lines — 13 domain libraries)
- acceptance-criteria-refactor.md (~90 lines — conditional, only for `type: refactor`)

---

## Output

**Phase 2 produces:**
- ✅ User story in proper format
- ✅ 3+ testable acceptance criteria
- ✅ Edge cases documented
- ✅ Data validation rules defined
- ✅ Measurable NFRs

---

## Error Handling

**Error 1: Subagent output incomplete**
- **Detection:** Missing user story, <3 AC, or vague NFRs
- **Recovery:** Re-invoke with specific feedback, or use AskUserQuestion to fill gaps

**Error 2: Acceptance criteria not testable**
- **Detection:** AC uses ambiguous language ("should", "might", "could")
- **Recovery:** Refine with specific assertions ("must", "will", "shall")

**Error 3: NFRs not measurable**
- **Detection:** Terms like "fast", "secure", "scalable" without metrics
- **Recovery:** Use AskUserQuestion to quantify targets

See `error-handling.md` for comprehensive error recovery procedures.

---

## Next Phase

**After Phase 2 completes →** Phase 3: Technical Specification

Load `technical-specification-creation.md` for Phase 3 workflow.
