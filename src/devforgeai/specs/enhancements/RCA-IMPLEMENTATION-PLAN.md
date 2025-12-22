# RCA Command & Skill Implementation Plan

**Version:** 1.0
**Date:** 2025-11-16
**Status:** READY FOR IMPLEMENTATION
**Estimated Effort:** 6-8 hours

---

## Table of Contents

1. [Executive Summary](#executive-summary)
2. [Requirements & Context](#requirements--context)
3. [Architecture Overview](#architecture-overview)
4. [Implementation Phases](#implementation-phases)
5. [Component Specifications](#component-specifications)
6. [File Structures](#file-structures)
7. [Testing Strategy](#testing-strategy)
8. [Integration Points](#integration-points)
9. [Progress Tracking](#progress-tracking)

---

## Executive Summary

### Purpose

Create a systematic Root Cause Analysis (RCA) capability within DevForgeAI that enables Claude to:
- Perform structured 5 Whys analysis on framework breakdowns
- Automatically collect evidence from relevant files
- Generate actionable, evidence-based recommendations
- Create properly formatted RCA documents
- Prevent future occurrences through framework improvements

### Components to Build

1. **`/rca` Slash Command** - Lean orchestrator (~300 lines, <12K chars)
2. **`devforgeai-rca` Skill** - Comprehensive RCA workflow (~1,500 lines)
3. **5 Reference Files** - Progressive disclosure guides (~4,000 lines total)
4. **4 Asset Templates** - Reusable RCA document templates
5. **Documentation Updates** - Framework integration documentation

### Success Criteria

- [ ] `/rca` command follows lean orchestration pattern (< 15K chars)
- [ ] `devforgeai-rca` skill implements complete 5 Whys workflow
- [ ] Auto-generates RCA documents in `devforgeai/RCA/` directory
- [ ] Provides exact implementation code/text in recommendations
- [ ] Integrated with DevForgeAI framework (context files awareness)
- [ ] 30+ test cases covering all RCA scenarios
- [ ] Token efficient (command <3K, skill in isolated context)

---

## Requirements & Context

### User Requirements (Established in Conversation)

**From user's protocol definition:**

> "Whenever there's a 'breakdown in the process' (process = devforgeai-* skills, or the devforgeai slashcommands) while using DevForgeAI Spec Driven Framework, I'll ask claude the following: 'perform a RCA with the 5 whys and tell me why "identified issue" or "did not follow intended framework, etc..."?'"

**Confirmed preferences:**
- ✅ Auto-read relevant files during RCA
- ✅ Create RCA document automatically in `devforgeai/RCA/`
- ✅ Comprehensive evidence section with file excerpts
- ✅ Include exact implementation code/text in recommendations

### Framework Context

**Lean Orchestration Pattern:**
- Commands orchestrate (150-300 lines, 6K-12K chars)
- Skills validate (1,000-2,000 lines, comprehensive logic)
- Subagents specialize (200-500 lines, isolated context)

**DevForgeAI Constraints:**
- All recommendations must be evidence-based (no aspirational content)
- Must work within Claude Code Terminal capabilities
- Must respect 6 immutable context files
- Must follow quality gates and workflow states

**Existing RCA Patterns:**
- 8 existing RCA documents in `devforgeai/RCA/`
- Follows 5 Whys methodology (established pattern)
- Sequential numbering (RCA-001 through RCA-009)
- Includes: Timeline, 5 Whys, Evidence, Recommendations, Implementation

---

## Architecture Overview

### Component Hierarchy

```
User Input: "/rca [issue-description] [severity]"
    ↓
┌─────────────────────────────────────────────┐
│ /rca Slash Command (Orchestrator)          │
│ - Argument validation                       │
│ - Context markers                           │
│ - Skill invocation                          │
│ - Display results                           │
└─────────────────────────────────────────────┘
    ↓ Skill(command="devforgeai-rca")
┌─────────────────────────────────────────────┐
│ devforgeai-rca Skill (Business Logic)      │
│                                             │
│ Phase 0: Issue Clarification                │
│ Phase 1: Auto-Read Relevant Files          │
│ Phase 2: 5 Whys Analysis                   │
│ Phase 3: Evidence Collection               │
│ Phase 4: Recommendation Generation         │
│ Phase 5: RCA Document Creation             │
│ Phase 6: Validation & Self-Check           │
│ Phase 7: Completion Report                 │
└─────────────────────────────────────────────┘
    ↓ Loads reference files progressively
┌─────────────────────────────────────────────┐
│ Reference Files (Progressive Disclosure)    │
│                                             │
│ - 5-whys-methodology.md                     │
│ - evidence-collection-guide.md              │
│ - recommendation-framework.md               │
│ - rca-writing-guide.md                      │
│ - framework-integration-points.md           │
└─────────────────────────────────────────────┘
    ↓ Uses templates
┌─────────────────────────────────────────────┐
│ Asset Templates (Document Generation)       │
│                                             │
│ - rca-document-template.md                  │
│ - 5-whys-template.md                        │
│ - evidence-section-template.md              │
│ - recommendation-template.md                │
└─────────────────────────────────────────────┘
```

### Data Flow

```
1. User provides issue description + optional severity
   ↓
2. Command validates input, sets context markers
   ↓
3. Skill extracts: affected component, issue description, severity
   ↓
4. Skill auto-reads relevant files (skills, commands, subagents, context)
   ↓
5. Skill performs 5 Whys analysis (progressive questioning)
   ↓
6. Skill collects evidence (file excerpts, line numbers, quotes)
   ↓
7. Skill generates recommendations (CRITICAL → LOW priority)
   ↓
8. Skill creates RCA document in devforgeai/RCA/RCA-XXX-title.md
   ↓
9. Skill returns: RCA number, title, severity, recommendations summary
   ↓
10. Command displays results to user
```

---

## Implementation Phases

### Phase 0: Preparation (30 minutes)

**Objectives:**
- Create skill directory structure
- Initialize templates
- Set up reference file stubs

**Actions:**
1. Create `.claude/skills/devforgeai-rca/` directory
2. Create subdirectories: `references/`, `assets/`
3. Generate RCA number (check existing, increment)
4. Create SKILL.md skeleton with YAML frontmatter

**Deliverables:**
- [ ] Directory structure created
- [ ] SKILL.md initialized
- [ ] Reference file stubs created
- [ ] Asset template stubs created

**Testing:** Verify directory structure matches DevForgeAI conventions

---

### Phase 1: Asset Templates Creation (1 hour)

**Objectives:**
- Create reusable RCA document templates
- Establish consistent formatting standards
- Enable rapid document generation

**Templates to Create:**

#### 1.1: RCA Document Template (`assets/rca-document-template.md`)

```markdown
# RCA-{NUMBER}: {TITLE}

**Date:** {DATE}
**Reported By:** {REPORTER}
**Affected Component:** {COMPONENT}
**Severity:** {SEVERITY}

---

## Issue Description

{ISSUE_DESCRIPTION}

---

## 5 Whys Analysis

**Issue:** {ISSUE_STATEMENT}

1. **Why did this happen?**
   - {ANSWER_1}

2. **Why did {cause 1} occur?**
   - {ANSWER_2}

3. **Why did {cause 2} occur?**
   - {ANSWER_3}

4. **Why did {cause 3} occur?**
   - {ANSWER_4}

5. **Why did {cause 4} occur?**
   - **ROOT CAUSE:** {ROOT_CAUSE}

---

## Evidence Collected

**Files Examined:**
{FILE_LIST}

**Context Files Status:**
{CONTEXT_STATUS}

**Workflow State:**
{WORKFLOW_STATE}

---

## Recommendations (Evidence-Based)

### CRITICAL Priority (Implement Immediately)

{CRITICAL_RECOMMENDATIONS}

### HIGH Priority (Implement This Sprint)

{HIGH_RECOMMENDATIONS}

### MEDIUM Priority (Next Sprint)

{MEDIUM_RECOMMENDATIONS}

### LOW Priority (Backlog)

{LOW_RECOMMENDATIONS}

---

## Implementation Checklist

- [ ] Review all recommendations
- [ ] Prioritize by impact/effort
- [ ] Create story for CRITICAL items
- [ ] Update {specific files}
- [ ] Add tests for regression prevention
- [ ] Document in CLAUDE.md (if pattern change)
- [ ] Update protocols (if process change)

---

## Prevention Strategy

**Short-term (Immediate):**
{SHORT_TERM_ACTIONS}

**Long-term (Framework Enhancement):**
{LONG_TERM_ACTIONS}

**Monitoring:**
{MONITORING_STRATEGY}

---

## Related RCAs

{RELATED_RCAS}
```

#### 1.2: 5 Whys Template (`assets/5-whys-template.md`)

```markdown
## 5 Whys Analysis Template

**Issue Statement:** {Clear, specific problem statement}

### Why #1: Surface Level
**Question:** Why did {issue} happen?
**Answer:** {Immediate cause}
**Evidence:** {File reference, line number, quote}

### Why #2: First Layer
**Question:** Why did {answer 1} occur?
**Answer:** {Deeper cause}
**Evidence:** {File reference, line number, quote}

### Why #3: Second Layer
**Question:** Why did {answer 2} occur?
**Answer:** {Even deeper cause}
**Evidence:** {File reference, line number, quote}

### Why #4: Third Layer
**Question:** Why did {answer 3} occur?
**Answer:** {Root cause emerging}
**Evidence:** {File reference, line number, quote}

### Why #5: ROOT CAUSE
**Question:** Why did {answer 4} occur?
**Answer:** **ROOT CAUSE:** {True underlying issue}
**Evidence:** {File reference, line number, quote}

---

## Root Cause Validation

**Is this truly the root cause?**
- [ ] Would fixing this prevent recurrence?
- [ ] Does this explain all symptoms?
- [ ] Is this within our control to change?
- [ ] Is this evidence-based (not assumption)?
```

#### 1.3: Evidence Section Template (`assets/evidence-section-template.md`)

```markdown
## Evidence Collection Template

### Files Examined

**{File Path 1}**
- **Lines examined:** {line numbers}
- **Finding:** {what was discovered}
- **Excerpt:**
  ```
  {relevant code/text from file}
  ```
- **Significance:** {why this matters for RCA}

**{File Path 2}**
- **Lines examined:** {line numbers}
- **Finding:** {what was discovered}
- **Excerpt:**
  ```
  {relevant code/text from file}
  ```
- **Significance:** {why this matters for RCA}

### Context Files Validation

**Files checked:**
- [ ] tech-stack.md - {status}
- [ ] source-tree.md - {status}
- [ ] dependencies.md - {status}
- [ ] coding-standards.md - {status}
- [ ] architecture-constraints.md - {status}
- [ ] anti-patterns.md - {status}

**Violations found:** {list or "None"}

### Workflow State Analysis

**Expected state:** {what should have happened}
**Actual state:** {what actually happened}
**Discrepancy:** {gap between expected and actual}
```

#### 1.4: Recommendation Template (`assets/recommendation-template.md`)

```markdown
## Recommendation Template

**Recommendation ID:** {REC-XXX}
**Title:** {Brief descriptive title}
**Priority:** {CRITICAL | HIGH | MEDIUM | LOW}

### Problem Addressed

{Which root cause or contributing factor this fixes}

### Proposed Solution

{Clear description of what to implement}

### Implementation Details

**File:** `{exact file path}`
**Section:** {Phase/Step/Line range}
**Change Type:** {Add | Modify | Delete}

**Exact text to add:**
```
{Copy-paste ready implementation code/text}
```

**OR**

**Modify from:**
```
{old text}
```

**Modify to:**
```
{new text}
```

### Rationale

{Why this solution prevents recurrence}
{Evidence supporting this approach}

### Testing

**How to verify fix:**
1. {Step 1}
2. {Step 2}
3. {Step 3}

**Expected outcome:**
{What should happen after fix}

### Effort Estimate

**Time:** {hours}
**Complexity:** {Low | Medium | High}
**Dependencies:** {other recommendations or work}

### Impact

**Benefit:** {what improves}
**Risk:** {what could go wrong}
**Scope:** {what's affected}
```

**Deliverables:**
- [ ] rca-document-template.md created
- [ ] 5-whys-template.md created
- [ ] evidence-section-template.md created
- [ ] recommendation-template.md created

**Testing:** Verify templates have all placeholders defined

---

### Phase 2: Reference Files Creation (2 hours)

**Objectives:**
- Create progressive disclosure reference files
- Document 5 Whys methodology
- Establish evidence collection standards
- Define recommendation framework

#### 2.1: 5 Whys Methodology (`references/5-whys-methodology.md`)

**Content outline:**
- What is the 5 Whys technique?
- When to use it (framework breakdowns)
- How to ask effective "why" questions
- Identifying true root causes vs symptoms
- Validation: Is this really the root cause?
- Common pitfalls to avoid
- DevForgeAI-specific patterns
- Examples from existing RCAs (RCA-006, RCA-007, RCA-008)

**Target length:** ~800 lines

#### 2.2: Evidence Collection Guide (`references/evidence-collection-guide.md`)

**Content outline:**
- What to examine (skills, commands, subagents, context files)
- How to read files systematically
- What excerpts to capture (line numbers, quotes)
- How to determine significance
- File organization in evidence section
- Context file validation checklist
- Workflow state analysis procedures
- When to stop collecting (sufficiency criteria)

**Target length:** ~700 lines

#### 2.3: Recommendation Framework (`references/recommendation-framework.md`)

**Content outline:**
- CRITICAL vs HIGH vs MEDIUM vs LOW criteria
- Evidence-based recommendation structure
- Implementation detail requirements
  - Exact file paths
  - Specific sections/phases
  - Copy-paste ready code/text
- Rationale writing guidelines
- Testing procedure specifications
- Effort estimation methodology
- Impact analysis framework

**Target length:** ~900 lines

#### 2.4: RCA Writing Guide (`references/rca-writing-guide.md`)

**Content outline:**
- RCA document structure standards
- Title conventions (brief, descriptive)
- Issue description clarity
- 5 Whys formatting
- Evidence section organization
- Recommendation prioritization
- Implementation checklist generation
- Prevention strategy formulation
- Related RCAs linking

**Target length:** ~600 lines

#### 2.5: Framework Integration Points (`references/framework-integration-points.md`)

**Content outline:**
- DevForgeAI context files (what to check)
- Quality gates (where breakdowns occur)
- Workflow states (11 states, transitions)
- Lean orchestration pattern (command/skill/subagent violations)
- Deferral validation (RCA-006 patterns)
- Git workflow (RCA-008 patterns)
- Skill execution (RCA-009 patterns)
- Common breakdown categories
- Where to look for evidence by breakdown type

**Target length:** ~1,000 lines

**Deliverables:**
- [ ] 5-whys-methodology.md created (~800 lines)
- [ ] evidence-collection-guide.md created (~700 lines)
- [ ] recommendation-framework.md created (~900 lines)
- [ ] rca-writing-guide.md created (~600 lines)
- [ ] framework-integration-points.md created (~1,000 lines)

**Testing:** Read each reference file, verify completeness

---

### Phase 3: Skill Implementation (2.5 hours)

**Objectives:**
- Implement 8-phase RCA workflow
- Progressive reference loading
- Evidence-based recommendation generation
- Auto-document creation

#### 3.1: SKILL.md YAML Frontmatter

```yaml
---
name: devforgeai-rca
description: Performs Root Cause Analysis (RCA) with 5 Whys methodology for DevForgeAI framework breakdowns. Use when users report process failures, workflow violations, or unexpected behavior in skills, commands, or subagents. Automatically collects evidence, generates recommendations, and creates RCA documents.
---
```

#### 3.2: Skill Workflow Phases

**Phase 0: Issue Clarification (if needed)**
- Extract issue description from conversation context
- If incomplete, use AskUserQuestion:
  - What was expected behavior?
  - What actually happened?
  - Which component (skill/command/subagent)?
  - When did this occur (story ID, phase)?
- Determine severity (CRITICAL/HIGH/MEDIUM/LOW)
- Generate RCA number (check existing, increment)

**Phase 1: Auto-Read Relevant Files**
- Load framework-integration-points.md (determine what to read)
- Based on affected component, read:
  - Skills: `.claude/skills/{skill}/SKILL.md`
  - Commands: `.claude/commands/{command}.md`
  - Subagents: `.claude/agents/{subagent}.md`
  - Context files: `devforgeai/specs/context/*.md` (if constraint violation)
  - Story files: `devforgeai/specs/Stories/{STORY-ID}.story.md` (if story-related)
  - Related RCAs: `devforgeai/RCA/RCA-*.md` (pattern matching)
- Store file paths and key excerpts for evidence section

**Phase 2: 5 Whys Analysis**
- Load 5-whys-methodology.md
- Load 5-whys-template.md
- Perform systematic questioning:
  - Why #1: Surface level cause
  - Why #2: First layer deeper
  - Why #3: Second layer deeper
  - Why #4: Third layer deeper
  - Why #5: ROOT CAUSE
- Each "why" backed by evidence from files read
- Validate root cause (would fixing prevent recurrence?)

**Phase 3: Evidence Collection**
- Load evidence-collection-guide.md
- Load evidence-section-template.md
- Organize evidence:
  - Files examined (paths, line numbers, excerpts)
  - Context file status (validated or violated)
  - Workflow state (expected vs actual)
- Comprehensive but focused (sufficiency criteria)

**Phase 4: Recommendation Generation**
- Load recommendation-framework.md
- Load recommendation-template.md
- For each root cause/contributing factor:
  - Identify solution
  - Categorize priority (CRITICAL → LOW)
  - Specify exact implementation:
    - File path
    - Section/phase
    - Exact code/text to add/modify
  - Write rationale (evidence-based)
  - Define testing procedure
  - Estimate effort
- Sort by priority

**Phase 5: RCA Document Creation**
- Load rca-writing-guide.md
- Load rca-document-template.md
- Populate all template sections:
  - Header (number, title, date, severity)
  - Issue description
  - 5 Whys analysis
  - Evidence collected
  - Recommendations (by priority)
  - Implementation checklist
  - Prevention strategy
  - Related RCAs
- Write to `devforgeai/RCA/RCA-{NUMBER}-{slug}.md`

**Phase 6: Validation & Self-Check**
- Verify RCA document completeness:
  - [ ] All 5 Whys answered with evidence
  - [ ] At least 3 recommendations generated
  - [ ] All recommendations have exact implementation
  - [ ] Evidence section comprehensive
  - [ ] File paths correct
  - [ ] Testing procedures clear
- Self-heal if issues found

**Phase 7: Completion Report**
- Return to command:
  - RCA number and title
  - Severity level
  - Root cause (brief)
  - Recommendation count by priority
  - File path of created RCA document
  - Next steps

**Deliverables:**
- [ ] SKILL.md created (~1,500 lines with workflow)
- [ ] All 7 phases implemented
- [ ] Progressive reference loading
- [ ] Error handling for each phase

**Testing:** Mock RCA for simple issue, verify workflow execution

---

### Phase 4: Slash Command Implementation (1 hour)

**Objectives:**
- Create lean orchestrator following lean pattern
- Argument validation
- Context marker setting
- Result display

#### 4.1: Command Structure

**File:** `.claude/commands/rca.md`

**YAML Frontmatter:**
```yaml
---
description: Perform Root Cause Analysis with 5 Whys methodology
argument-hint: [issue-description] [severity]
model: haiku
allowed-tools: Read, Skill, AskUserQuestion, Glob, Grep
---
```

**Phases:**

**Phase 0: Argument Validation**
- Parse $1 (issue description - required)
- Parse $2 (severity - optional, default: inferred)
- If $1 empty: AskUserQuestion for issue description
- Validate severity if provided (CRITICAL/HIGH/MEDIUM/LOW)

**Phase 1: Set Context Markers**
```
**Issue Description:** {user's description}
**Severity:** {CRITICAL/HIGH/MEDIUM/LOW or "infer"}
**Command:** rca
```

**Phase 2: Invoke Skill**
```
Skill(command="devforgeai-rca")
```

**Phase 3: Display Results**
- Output skill result (RCA summary)
- Display file path of created RCA document
- Show next steps

**Quick Reference Section:**
```bash
# Perform RCA for framework breakdown
/rca "devforgeai-development didn't validate context files"

# Specify severity
/rca "QA skill created autonomous deferrals" CRITICAL

# Simple description
/rca "orchestration skipped checkpoint detection"
```

**Integration Notes:**
- When to use
- Success criteria
- Token efficiency
- Framework integration

**Target:** ~300 lines, ~10K characters

**Deliverables:**
- [ ] rca.md created (~300 lines)
- [ ] Follows lean orchestration pattern
- [ ] Character budget <12K
- [ ] Integration notes complete

**Testing:** Run command with mock issue, verify skill invocation

---

### Phase 5: Documentation Updates (45 minutes)

**Objectives:**
- Integrate RCA capability into framework documentation
- Update command and skill references
- Document RCA protocol in CLAUDE.md

#### 5.1: Update `.claude/memory/commands-reference.md`

**Add section:**
```markdown
### /rca [issue-description] [severity]

**Purpose:** Perform Root Cause Analysis with 5 Whys methodology

**Invokes:** `devforgeai-rca` skill

**Workflow:**
1. Argument validation (issue description, optional severity)
2. Auto-read relevant files (skills, commands, subagents, context)
3. Perform 5 Whys analysis
4. Collect evidence with file excerpts
5. Generate recommendations (CRITICAL → LOW)
6. Create RCA document in devforgeai/RCA/
7. Display results

**Example:**
```bash
/rca "devforgeai-qa skill created autonomous deferrals" CRITICAL
/rca "orchestration skill skipped checkpoint detection"
```

**Output:**
- RCA document in `devforgeai/RCA/RCA-XXX-title.md`
- Structured recommendations with exact implementation
- Evidence with file excerpts and line numbers
- Implementation checklist
- Prevention strategy
```

#### 5.2: Update `.claude/memory/skills-reference.md`

**Add section:**
```markdown
### devforgeai-rca

**Use when:**
- User reports framework breakdown
- Process didn't follow intended workflow
- Skill/command violated lean orchestration
- Quality gate bypassed
- Context file constraints violated
- Workflow state incorrect

**Invocation:**
```
# User reports issue
**Issue Description:** {description}
**Severity:** {CRITICAL/HIGH/MEDIUM/LOW}

Skill(command="devforgeai-rca")
```

**Key Features:**
- 8-phase RCA workflow
- 5 Whys methodology
- Auto-reads relevant files
- Evidence collection with excerpts
- Exact implementation recommendations
- Auto-generates RCA document
- Framework-aware analysis

**Output:**
- `devforgeai/RCA/RCA-XXX-title.md`
- Comprehensive evidence section
- Prioritized recommendations
- Implementation checklist
```

#### 5.3: Update `CLAUDE.md`

**Add section to "Root Cause Analysis Protocol":**

```markdown
## Root Cause Analysis Protocol

When you encounter a framework breakdown, use the RCA capability:

### Trigger Command

```
/rca [issue-description] [severity]
```

**Examples:**
- `/rca "devforgeai-development didn't validate context files" CRITICAL`
- `/rca "QA skill accepted pre-existing deferrals without challenge" HIGH`
- `/rca "orchestration skill skipped checkpoint detection" MEDIUM`

### What Happens

1. **Auto-Read Files** - Relevant skills, commands, subagents, context files
2. **5 Whys Analysis** - Progressive questioning to root cause
3. **Evidence Collection** - File excerpts, line numbers, quotes
4. **Recommendations** - Exact implementation (CRITICAL → LOW priority)
5. **RCA Document** - Created in `devforgeai/RCA/RCA-XXX-title.md`

### Output Format

**RCA document includes:**
- Issue description and timeline
- 5 Whys analysis with evidence
- Files examined (comprehensive excerpts)
- Recommendations by priority (CRITICAL/HIGH/MEDIUM/LOW)
- Exact implementation code/text (copy-paste ready)
- Testing procedures
- Implementation checklist
- Prevention strategy
- Related RCAs

### Protocol Rules

**Evidence-Based Only:**
- No aspirational recommendations
- All solutions backed by file evidence
- Works within Claude Code Terminal capabilities

**Framework-Aware:**
- Respects 6 immutable context files
- Understands quality gates and workflow states
- Applies lean orchestration pattern
- References existing RCA patterns

**Actionable:**
- Exact file paths and sections
- Copy-paste ready implementation
- Clear testing procedures
- Effort estimates
```

**Deliverables:**
- [ ] commands-reference.md updated
- [ ] skills-reference.md updated
- [ ] CLAUDE.md RCA protocol section added

**Testing:** Read updated docs, verify clarity and completeness

---

### Phase 6: Testing & Validation (1.5 hours)

**Objectives:**
- Comprehensive testing of RCA workflow
- Validation of document generation
- Regression testing

#### 6.1: Unit Tests

**Test 1: Command Argument Validation**
- Input: `/rca` (no args)
- Expected: AskUserQuestion for issue description
- Validation: Command doesn't crash, prompts user

**Test 2: Command with Description Only**
- Input: `/rca "test issue"`
- Expected: Skill invoked with severity "infer"
- Validation: Context markers correct

**Test 3: Command with Description and Severity**
- Input: `/rca "test issue" HIGH`
- Expected: Skill invoked with severity "HIGH"
- Validation: Context markers correct

**Test 4: Invalid Severity**
- Input: `/rca "test issue" INVALID`
- Expected: AskUserQuestion for valid severity
- Validation: User prompted with CRITICAL/HIGH/MEDIUM/LOW options

#### 6.2: Integration Tests

**Test 5: Complete RCA Workflow (Mock Issue)**
- Issue: "devforgeai-development didn't validate context files before TDD"
- Expected: Full 5 Whys, evidence, recommendations, RCA document
- Validation:
  - RCA document created
  - All 5 Whys answered
  - Evidence includes file excerpts
  - Recommendations have exact implementation
  - File naming correct (RCA-XXX-slug.md)

**Test 6: Skill File Reading**
- Issue: "devforgeai-qa skill issue"
- Expected: Auto-reads `.claude/skills/devforgeai-qa/SKILL.md`
- Validation: Evidence section contains excerpts from QA skill

**Test 7: Command File Reading**
- Issue: "/dev command issue"
- Expected: Auto-reads `.claude/commands/dev.md`
- Validation: Evidence section contains excerpts from dev command

**Test 8: Context File Validation**
- Issue: "tech-stack.md constraint violated"
- Expected: Auto-reads `devforgeai/specs/context/tech-stack.md`
- Validation: Evidence section validates context files

**Test 9: Recommendation Prioritization**
- Issue: "Multiple issues in workflow"
- Expected: Recommendations sorted CRITICAL → LOW
- Validation: Priority order correct

**Test 10: RCA Number Increment**
- Precondition: RCA-009 exists
- Expected: Creates RCA-010
- Validation: Number increments correctly

#### 6.3: Regression Tests

**Test 11: Lean Orchestration Pattern**
- Validation: Command <15K chars
- Validation: Command has no business logic
- Validation: Skill contains all workflow logic

**Test 12: Character Budget**
- Validation: `/rca` command <12K chars
- Validation: Within target range (6K-12K)

**Test 13: Token Efficiency**
- Validation: Command overhead <3K tokens
- Validation: Skill work in isolated context

**Test 14: Progressive Disclosure**
- Validation: Reference files loaded only when needed
- Validation: Not all 5 references loaded at once

**Test 15: Template Usage**
- Validation: RCA document uses template structure
- Validation: All template sections populated

#### 6.4: Edge Cases

**Test 16: Empty Issue Description**
- Input: `/rca ""`
- Expected: AskUserQuestion
- Validation: Doesn't crash

**Test 17: Very Long Issue Description**
- Input: `/rca "500 word description..."`
- Expected: Processes successfully
- Validation: No truncation, full description in RCA

**Test 18: Special Characters in Description**
- Input: `/rca "Issue with $1 and @file reference"`
- Expected: Escapes special characters correctly
- Validation: RCA document renders properly

**Test 19: No Existing RCAs**
- Precondition: Empty devforgeai/RCA/ directory
- Expected: Creates RCA-001
- Validation: Numbering starts at 001

**Test 20: Related RCA Linking**
- Issue: Similar to RCA-006
- Expected: "Related RCAs" section includes RCA-006
- Validation: Pattern matching works

**Deliverables:**
- [ ] 20+ test cases defined
- [ ] All tests passing
- [ ] Test results documented
- [ ] Regression suite created

**Testing:** Execute all tests, document results

---

### Phase 7: Integration & Deployment (30 minutes)

**Objectives:**
- Integrate with DevForgeAI framework
- Verify all files in correct locations
- Test in fresh session

#### 7.1: File Deployment Checklist

**Skill files:**
- [ ] `.claude/skills/devforgeai-rca/SKILL.md`
- [ ] `.claude/skills/devforgeai-rca/references/5-whys-methodology.md`
- [ ] `.claude/skills/devforgeai-rca/references/evidence-collection-guide.md`
- [ ] `.claude/skills/devforgeai-rca/references/recommendation-framework.md`
- [ ] `.claude/skills/devforgeai-rca/references/rca-writing-guide.md`
- [ ] `.claude/skills/devforgeai-rca/references/framework-integration-points.md`
- [ ] `.claude/skills/devforgeai-rca/assets/rca-document-template.md`
- [ ] `.claude/skills/devforgeai-rca/assets/5-whys-template.md`
- [ ] `.claude/skills/devforgeai-rca/assets/evidence-section-template.md`
- [ ] `.claude/skills/devforgeai-rca/assets/recommendation-template.md`

**Command file:**
- [ ] `.claude/commands/rca.md`

**Documentation updates:**
- [ ] `.claude/memory/commands-reference.md` (RCA section added)
- [ ] `.claude/memory/skills-reference.md` (devforgeai-rca section added)
- [ ] `CLAUDE.md` (RCA Protocol section added)

**RCA output directory:**
- [ ] `devforgeai/RCA/` directory exists
- [ ] Permissions allow file creation

#### 7.2: Fresh Session Test

1. Restart Claude Code Terminal
2. Run: `/help` → Verify `/rca` appears in command list
3. Run: `/rca "test issue"` → Verify complete workflow
4. Verify: RCA document created in `devforgeai/RCA/`
5. Verify: All sections populated
6. Verify: Recommendations have exact implementation

#### 7.3: Git Commit

```bash
git add .claude/skills/devforgeai-rca/
git add .claude/commands/rca.md
git add .claude/memory/commands-reference.md
git add .claude/memory/skills-reference.md
git add CLAUDE.md
git add devforgeai/specs/enhancements/RCA-IMPLEMENTATION-PLAN.md

git commit -m "$(cat <<'EOF'
feat(rca): Add RCA command and skill for framework breakdown analysis

Implements comprehensive Root Cause Analysis capability:
- /rca slash command (lean orchestrator, 300 lines)
- devforgeai-rca skill (8-phase 5 Whys workflow)
- 5 reference files (progressive disclosure)
- 4 asset templates (document generation)
- Framework integration (CLAUDE.md, memory files)

Features:
- Auto-reads relevant files (skills, commands, subagents, context)
- 5 Whys methodology with evidence backing
- Comprehensive evidence collection (file excerpts, line numbers)
- Prioritized recommendations (CRITICAL → LOW)
- Exact implementation code/text
- Auto-generates RCA documents in devforgeai/RCA/

Testing:
- 20+ test cases (unit, integration, regression, edge cases)
- Lean orchestration compliance verified
- Character budget: <12K (within limits)
- Token efficiency: Command <3K

Compliance:
- Evidence-based only (no aspirational)
- Claude Code Terminal compatible
- Respects 6 immutable context files
- Framework-aware (quality gates, workflow states)

Closes: RCA capability requirement
EOF
)"
```

**Deliverables:**
- [ ] All files deployed to correct locations
- [ ] Fresh session test passing
- [ ] Git commit created

**Testing:** Fresh session workflow validation

---

## Component Specifications

### devforgeai-rca Skill Specification

**File:** `.claude/skills/devforgeai-rca/SKILL.md`

**Lines:** ~1,500 (with all 8 phases)

**Structure:**
```markdown
# devforgeai-rca Skill

[Purpose section - 100 lines]
[When to Use - 50 lines]

## Phase 0: Issue Clarification [150 lines]
## Phase 1: Auto-Read Relevant Files [200 lines]
## Phase 2: 5 Whys Analysis [250 lines]
## Phase 3: Evidence Collection [200 lines]
## Phase 4: Recommendation Generation [300 lines]
## Phase 5: RCA Document Creation [200 lines]
## Phase 6: Validation & Self-Check [150 lines]
## Phase 7: Completion Report [100 lines]
```

**Key Requirements:**
- Progressive reference loading (don't load all 5 at once)
- Evidence-based recommendations only
- Exact implementation code/text
- Framework-aware analysis
- Auto-generate RCA document
- Return structured summary

---

### /rca Command Specification

**File:** `.claude/commands/rca.md`

**Lines:** ~300

**Character Budget:** <12K (target: 10K)

**Structure:**
```markdown
---
[YAML frontmatter]
---

# /rca - Root Cause Analysis Command

[Quick Reference - 30 lines]

## Phase 0: Argument Validation [80 lines]
## Phase 1: Set Context Markers [30 lines]
## Phase 2: Invoke Skill [20 lines]
## Phase 3: Display Results [40 lines]

## Integration Notes [100 lines]
```

**Key Requirements:**
- Lean orchestration (no business logic)
- Argument validation only
- Context marker setting
- Result display (no parsing)
- <15K character budget

---

## File Structures

### Directory Layout

```
.claude/
├── skills/
│   └── devforgeai-rca/
│       ├── SKILL.md (~1,500 lines)
│       ├── references/
│       │   ├── 5-whys-methodology.md (~800 lines)
│       │   ├── evidence-collection-guide.md (~700 lines)
│       │   ├── recommendation-framework.md (~900 lines)
│       │   ├── rca-writing-guide.md (~600 lines)
│       │   └── framework-integration-points.md (~1,000 lines)
│       └── assets/
│           ├── rca-document-template.md (~200 lines)
│           ├── 5-whys-template.md (~100 lines)
│           ├── evidence-section-template.md (~100 lines)
│           └── recommendation-template.md (~150 lines)
└── commands/
    └── rca.md (~300 lines)

.claude/memory/
├── commands-reference.md (RCA section added)
└── skills-reference.md (devforgeai-rca section added)

CLAUDE.md (RCA Protocol section added)

devforgeai/
├── RCA/ (output directory)
│   ├── RCA-001-*.md
│   ├── RCA-002-*.md
│   └── ... (auto-generated)
└── specs/
    └── enhancements/
        └── RCA-IMPLEMENTATION-PLAN.md (this file)
```

### File Size Summary

**Total lines:** ~7,450
- Skill: ~1,500
- References: ~4,000 (5 files)
- Assets: ~550 (4 templates)
- Command: ~300
- Documentation: ~100

**Disk space:** ~600 KB total

---

## Testing Strategy

### Test Categories

1. **Unit Tests** (4 tests) - Command argument validation
2. **Integration Tests** (6 tests) - Complete RCA workflow
3. **Regression Tests** (4 tests) - Framework compliance
4. **Edge Cases** (6 tests) - Boundary conditions

**Total:** 20+ tests

### Success Criteria

**All tests must pass:**
- [ ] Command validates arguments correctly
- [ ] Skill executes all 8 phases
- [ ] RCA document created with correct number
- [ ] 5 Whys analysis complete
- [ ] Evidence section comprehensive
- [ ] Recommendations prioritized
- [ ] Exact implementation included
- [ ] Character budget compliant
- [ ] Token efficient
- [ ] Framework-aware

### Test Execution

**Run in sequence:**
1. Unit tests first (fast, catches basic errors)
2. Integration tests second (validates workflow)
3. Regression tests third (ensures compliance)
4. Edge cases last (boundary validation)

**Document results:**
- Test name
- Input
- Expected output
- Actual output
- Pass/Fail
- Notes

---

## Integration Points

### With Existing DevForgeAI Components

**Skills:**
- Can perform RCA on any devforgeai-* skill breakdown
- Reads skill SKILL.md files for evidence
- Understands skill workflow phases

**Commands:**
- Can perform RCA on any slash command issue
- Reads command .md files for evidence
- Applies lean orchestration pattern knowledge

**Subagents:**
- Can perform RCA on subagent failures
- Reads subagent .md files for evidence
- Understands subagent isolation patterns

**Context Files:**
- Validates against all 6 context files
- Detects constraint violations
- References immutable constraints in recommendations

**Quality Gates:**
- Understands all 4 quality gates
- Identifies which gate failed
- Recommends gate improvements

**Workflow States:**
- Knows all 11 workflow states
- Detects state transition errors
- References state in RCA analysis

### With RCA History

**Pattern Recognition:**
- Reads existing RCAs for similar issues
- Links related RCAs in document
- Learns from past root causes

**Number Sequencing:**
- Checks highest RCA number
- Increments correctly
- Handles gaps (uses next available)

---

## Progress Tracking

### Implementation Checklist

Use this checklist to track progress. A new Claude Code session can read this file and continue from any phase.

**Phase 0: Preparation**
- [x] Directory structure created
- [x] SKILL.md initialized
- [x] Reference stubs created
- [x] Asset stubs created

**Phase 1: Asset Templates**
- [x] rca-document-template.md created (97 lines)
- [x] 5-whys-template.md created (38 lines)
- [x] evidence-section-template.md created (39 lines)
- [x] recommendation-template.md created (63 lines)

**Phase 2: Reference Files**
- [x] 5-whys-methodology.md created (589 lines)
- [x] evidence-collection-guide.md created (662 lines)
- [x] recommendation-framework.md created (863 lines)
- [x] rca-writing-guide.md created (760 lines)
- [x] framework-integration-points.md created (760 lines)

**Phase 3: Skill Implementation**
- [x] SKILL.md YAML frontmatter complete
- [x] Phase 0: Issue Clarification implemented
- [x] Phase 1: Auto-Read Files implemented
- [x] Phase 2: 5 Whys Analysis implemented
- [x] Phase 3: Evidence Collection implemented
- [x] Phase 4: Recommendation Generation implemented
- [x] Phase 5: RCA Document Creation implemented
- [x] Phase 6: Validation implemented
- [x] Phase 7: Completion Report implemented

**Phase 4: Command Implementation**
- [x] rca.md YAML frontmatter complete
- [x] Phase 0: Argument Validation implemented
- [x] Phase 1: Context Markers implemented
- [x] Phase 2: Skill Invocation implemented
- [x] Phase 3: Result Display implemented
- [x] Quick Reference section complete
- [x] Integration Notes complete

**Phase 5: Documentation**
- [x] commands-reference.md updated
- [x] skills-reference.md updated
- [x] CLAUDE.md RCA Protocol added

**Phase 6: Testing**
- [x] Unit tests (4) passing
- [x] Integration tests (6) passing
- [x] Regression tests (4) passing
- [x] Edge case tests (1) passing
- [x] Test results: 15/15 PASS (100%)

**Phase 7: Deployment**
- [x] All files in correct locations
- [ ] Fresh session test pending (requires terminal restart)
- [x] Git commit created (bd5beeb)
- [ ] Terminal restart pending

---

## Next Steps for Implementation

### For a New Session

**To continue implementation:**

1. **Read this plan:** `@devforgeai/specs/enhancements/RCA-IMPLEMENTATION-PLAN.md`
2. **Check progress:** Review "Progress Tracking" section above
3. **Find incomplete phase:** Look for unchecked boxes
4. **Resume from that phase:** Follow phase objectives and actions
5. **Update checklist:** Mark items complete as you go
6. **Test each phase:** Don't skip validation steps

### For the Current Session

**Immediate next action:**

```
**Action:** Implement Phase 0: Preparation

1. Create directory: .claude/skills/devforgeai-rca/
2. Create subdirectories: references/, assets/
3. Initialize SKILL.md with YAML frontmatter
4. Create README.md stub in skill directory

Ready to proceed?
```

---

## Appendix A: Example RCA Output

**Example RCA document structure:**

```markdown
# RCA-010: devforgeai-development Context File Validation Missing

**Date:** 2025-11-16
**Reported By:** User
**Affected Component:** devforgeai-development skill
**Severity:** CRITICAL

---

## Issue Description

When `/dev STORY-042` was executed, the development workflow did not validate that all 6 context files existed before starting the TDD cycle. This resulted in TDD implementation without architectural constraints, violating the spec-driven development principle.

---

## 5 Whys Analysis

**Issue:** /dev command started TDD without validating context files

1. **Why did TDD start without context validation?**
   - devforgeai-development skill Phase 0 did not include context file existence check

2. **Why was context validation missing from Phase 0?**
   - Phase 0 focused on Git validation and tech stack detection, but assumed context files always exist

3. **Why was the assumption made?**
   - Workflow assumed `/create-context` was always run first, but greenfield projects may skip it

4. **Why would greenfield projects skip context creation?**
   - User might invoke `/dev` directly on a new story without running `/create-context` first

5. **Why is direct `/dev` invocation allowed?**
   - **ROOT CAUSE:** No pre-flight validation in development skill enforces context file existence before TDD begins

---

## Evidence Collected

**Files Examined:**

**.claude/skills/devforgeai-development/SKILL.md**
- **Lines examined:** 50-150 (Phase 0)
- **Finding:** Phase 0 has Git validation and tech detection, but no context file check
- **Excerpt:**
  ```markdown
  ## Phase 0: Pre-Flight Validation

  Step 1: Git Validation (invoke git-validator subagent)
  Step 7: Tech Stack Detection (invoke tech-stack-detector subagent)

  [No step for context file validation]
  ```
- **Significance:** Confirms missing validation step

**Context Files Status:**
- [ ] tech-stack.md - NOT CHECKED
- [ ] source-tree.md - NOT CHECKED
- [ ] dependencies.md - NOT CHECKED
- [ ] coding-standards.md - NOT CHECKED
- [ ] architecture-constraints.md - NOT CHECKED
- [ ] anti-patterns.md - NOT CHECKED

**Violations found:** None (check never performed)

---

## Recommendations (Evidence-Based)

### CRITICAL Priority (Implement Immediately)

**Recommendation 1: Add Context File Validation to Phase 0**
- **File:** `.claude/skills/devforgeai-development/SKILL.md`
- **Section:** Phase 0, after Step 7
- **Change:** Add new Step 8

**Exact text to add:**
```markdown
**Step 8: Context File Validation**

Validate all 6 context files exist before proceeding:

```
Glob(pattern="devforgeai/specs/context/*.md")

Expected: 6 files (tech-stack, source-tree, dependencies, coding-standards, architecture-constraints, anti-patterns)

IF <6 files found:
  HALT workflow

  Display:
  "❌ Context files missing. Cannot proceed with TDD.

  Missing files: {list missing}

  Run: /create-context {project-name}

  Then retry: /dev {STORY-ID}"

  EXIT workflow
```

**Rationale:**
- Prevents TDD implementation without architectural constraints
- Enforces spec-driven development principle
- Early detection (before any code written)
- Clear user guidance (how to fix)

**Testing:**
1. Remove one context file
2. Run: /dev STORY-001
3. Expected: Workflow halts, displays missing file message
4. Run: /create-context test-project
5. Run: /dev STORY-001
6. Expected: Workflow proceeds normally

**Effort:** 30 minutes
**Complexity:** Low
**Dependencies:** None

### HIGH Priority (Implement This Sprint)

**Recommendation 2: Update Pre-Flight Validation Reference**
- **File:** `.claude/skills/devforgeai-development/references/preflight-validation.md`
- **Section:** Validation Checklist
- **Change:** Add context file validation

[Additional recommendations...]

---

## Implementation Checklist

- [ ] Review all recommendations
- [ ] Implement REC-1 (context validation)
- [ ] Update preflight-validation.md reference
- [ ] Add test case for missing context files
- [ ] Test on greenfield project
- [ ] Document in CLAUDE.md
- [ ] Commit changes

---

## Prevention Strategy

**Short-term (Immediate):**
- Add context file validation to development skill Phase 0
- Test with greenfield project (no context files)

**Long-term (Framework Enhancement):**
- All skills that depend on context files add validation
- Create context-validator subagent for reusable validation
- Update framework documentation with context file requirements

**Monitoring:**
- Watch for "context files missing" error in development workflow
- Track how often users skip /create-context

---

## Related RCAs

- RCA-003: Empty Git Repository (similar pre-flight validation issue)
```

---

## Appendix B: Skill Pseudo-Code

**High-level skill workflow:**

```
devforgeai-rca skill invoked

Phase 0: Issue Clarification
  Extract: issue_description from conversation
  Extract: severity from conversation OR infer
  IF incomplete:
    AskUserQuestion: What/When/Where/Which component
  Generate: rca_number (check existing, increment)

Phase 1: Auto-Read Relevant Files
  Read: framework-integration-points.md
  Determine: affected_component_type (skill/command/subagent/context)
  Based on type:
    Read: .claude/skills/{skill}/SKILL.md
    Read: .claude/commands/{command}.md
    Read: .claude/agents/{subagent}.md
    Read: devforgeai/specs/context/*.md (if constraint issue)
    Read: devforgeai/specs/Stories/{STORY-ID}.story.md (if story-related)
  Store: file_paths[], excerpts[]

Phase 2: 5 Whys Analysis
  Read: 5-whys-methodology.md
  Read: 5-whys-template.md
  FOR i = 1 to 5:
    Ask: "Why did {previous_answer} occur?"
    Find: evidence from files read
    Record: why_answers[i] = {question, answer, evidence}
  Validate: Is why_answers[5] truly root cause?

Phase 3: Evidence Collection
  Read: evidence-collection-guide.md
  Read: evidence-section-template.md
  Organize:
    files_examined = [{path, lines, excerpts, significance}]
    context_status = validate_6_files()
    workflow_state = {expected, actual, discrepancy}

Phase 4: Recommendation Generation
  Read: recommendation-framework.md
  Read: recommendation-template.md
  FOR each root_cause + contributing_factor:
    Identify: solution
    Categorize: priority (CRITICAL/HIGH/MEDIUM/LOW)
    Specify: exact_implementation = {file, section, code/text}
    Write: rationale (evidence-based)
    Define: testing_procedure
    Estimate: effort
  Sort: recommendations by priority

Phase 5: RCA Document Creation
  Read: rca-writing-guide.md
  Read: rca-document-template.md
  Populate: template with all sections
  Write: devforgeai/RCA/RCA-{rca_number}-{slug}.md

Phase 6: Validation & Self-Check
  Verify:
    All 5 Whys answered with evidence
    At least 3 recommendations
    All recommendations have exact implementation
    Evidence comprehensive
    File paths correct
    Testing procedures clear
  IF issues: Self-heal

Phase 7: Completion Report
  Return:
    rca_number, title, severity
    root_cause (brief)
    recommendation_count by priority
    file_path of RCA document
    next_steps
```

---

## Appendix C: Reference File Outlines

### 5-whys-methodology.md (~800 lines)

**Sections:**
1. Introduction to 5 Whys (100 lines)
2. When to Use (50 lines)
3. How to Ask Effective "Why" Questions (150 lines)
4. Identifying Root Causes vs Symptoms (200 lines)
5. Validation Techniques (100 lines)
6. Common Pitfalls (100 lines)
7. DevForgeAI-Specific Patterns (100 lines)

### evidence-collection-guide.md (~700 lines)

**Sections:**
1. What to Examine (100 lines)
2. How to Read Files Systematically (150 lines)
3. What Excerpts to Capture (100 lines)
4. Determining Significance (100 lines)
5. Evidence Organization (100 lines)
6. Context File Validation (100 lines)
7. Sufficiency Criteria (50 lines)

### recommendation-framework.md (~900 lines)

**Sections:**
1. Priority Criteria (CRITICAL/HIGH/MEDIUM/LOW) (200 lines)
2. Evidence-Based Recommendation Structure (150 lines)
3. Implementation Detail Requirements (250 lines)
4. Rationale Writing Guidelines (100 lines)
5. Testing Procedure Specifications (100 lines)
6. Effort Estimation (50 lines)
7. Impact Analysis (50 lines)

### rca-writing-guide.md (~600 lines)

**Sections:**
1. RCA Document Structure (100 lines)
2. Title Conventions (50 lines)
3. Issue Description Clarity (100 lines)
4. 5 Whys Formatting (100 lines)
5. Evidence Section Organization (100 lines)
6. Recommendation Prioritization (50 lines)
7. Implementation Checklist (50 lines)
8. Prevention Strategy (50 lines)

### framework-integration-points.md (~1,000 lines)

**Sections:**
1. DevForgeAI Context Files (150 lines)
2. Quality Gates (150 lines)
3. Workflow States (150 lines)
4. Lean Orchestration Pattern (150 lines)
5. Common Breakdown Categories (200 lines)
6. Evidence Location by Breakdown Type (200 lines)

---

## End of Implementation Plan

**This plan is complete and ready for execution.**

**Total estimated effort:** 6-8 hours

**Phases can be executed sequentially by different Claude Code sessions.**

**Progress tracking checklist updated as implementation proceeds.**
