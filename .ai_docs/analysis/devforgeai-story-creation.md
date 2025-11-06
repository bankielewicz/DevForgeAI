# DevForgeAI Story Creation Skill - Refactoring Plan

**Status:** NOT STARTED
**Assigned Session:** None
**Last Updated:** 2025-01-06 (Initial Creation)
**Estimated Effort:** 3-4 hours
**Priority:** P1 - CRITICAL (Second worst: 9.2x over limit)

---

## Executive Summary

The `devforgeai-story-creation` skill is the second-largest skill requiring refactoring. At **1,840 lines**, it is **9.2x over the optimal 200-line limit**.

**Key Issue:** The 8-phase workflow is fully documented inline in SKILL.md, despite having 6 excellent reference files (7,477 lines). The entry point contains detailed phase implementation that should be progressively loaded.

**Target:** Reduce SKILL.md from 1,840 lines to ~180 lines while maintaining comprehensive story generation through improved progressive disclosure.

**Expected Gains:**
- **Token efficiency:** 10x improvement on skill activation
- **Activation time:** 500ms+ → <100ms (estimated)
- **Context relevance:** 25% → 90%+ (phase-specific loading)

---

## Current State Analysis

### Metrics

| Metric | Current | Target | Gap |
|--------|---------|--------|-----|
| **SKILL.md lines** | 1,840 | ~180 | -1,660 (-90%) |
| **References files** | 6 files | 13-15 files | +7-9 |
| **References lines** | 7,477 | ~9,000 | +1,523 |
| **Total lines** | 9,317 | ~9,180 | -137 |
| **Entry point ratio** | 19.7% | ~2% | -17.7% |
| **Cold start load** | 1,840 lines | <200 lines | -1,640 |
| **Estimated tokens** | ~14,720 | ~1,440 | -13,280 (-90%) |

### Current Structure (Line Distribution)

```
SKILL.md (1,840 lines total):
├─ Lines 1-13:      YAML Frontmatter (13 lines)
├─ Lines 15-51:     Purpose & Philosophy (37 lines) ✅ KEEP (condense to 25)
├─ Lines 52-69:     When to Use (18 lines) ✅ KEEP
├─ Lines 71-304:    Phase 1: Story Discovery (234 lines) → EXTRACT
├─ Lines 306-439:   Phase 2: Requirements Analysis (134 lines) → EXTRACT
├─ Lines 441-668:   Phase 3: Technical Specification (228 lines) → EXTRACT
├─ Lines 670-914:   Phase 4: UI Specification (245 lines) → EXTRACT
├─ Lines 916-1182:  Phase 5: Story File Creation (267 lines) → EXTRACT (includes templates)
├─ Lines 1184-1275: Phase 6: Epic/Sprint Linking (92 lines) → EXTRACT
├─ Lines 1277-1434: Phase 7: Self-Validation (158 lines) → EXTRACT
├─ Lines 1436-1554: Phase 8: Completion Report (119 lines) → EXTRACT
├─ Lines 1556-1703: Error Handling (148 lines) → EXTRACT
├─ Lines 1705-1762: Integration Patterns (58 lines) ✅ KEEP (condense to 20)
├─ Lines 1764-1785: Success Criteria (22 lines) ✅ KEEP (condense to 15)
├─ Lines 1787-1809: Reference Files List (23 lines) ✅ KEEP (update with new files)
├─ Lines 1811-1840: Best Practices (30 lines) ✅ KEEP (condense to 10)
```

### Existing Reference Files (Excellent Quality)

| File | Lines | Status | Usage |
|------|-------|--------|-------|
| acceptance-criteria-patterns.md | 1,259 | ✅ Excellent | Phase 2 |
| story-examples.md | 1,905 | ✅ Excellent | Reference examples |
| story-structure-guide.md | 662 | ✅ Good | Phase 5 |
| technical-specification-guide.md | 1,269 | ✅ Excellent | Phase 3 |
| ui-specification-guide.md | 1,344 | ✅ Excellent | Phase 4 |
| validation-checklists.md | 1,038 | ✅ Excellent | Phase 7 |

**Observation:** Reference files are comprehensive and well-structured. Problem is SKILL.md duplicates phase logic instead of just pointing to them.

### Problems Identified

1. **8-Phase Workflow Fully Documented Inline (1,477 lines)**
   - Phases 1-8 account for 80% of SKILL.md
   - Each phase has complete implementation details
   - Should be: Phase summary + "Load [phase-name].md for details"
   - Extract to: 8 individual phase reference files

2. **Story File Template Embedded in Phase 5 (267 lines)**
   - Lines 916-1182 contain complete story template
   - Template is 15% of entire SKILL.md
   - Already exists as `assets/story-template.md` (609 lines)
   - Should be: "Load template from assets/"

3. **Error Handling Inline (148 lines)**
   - 6 error scenarios with detailed recovery steps
   - Should be: Separate error-handling.md reference

4. **Integration Patterns Too Verbose (58 lines)**
   - Could be condensed to 20 lines with references
   - Details should be in integration-guide.md

5. **No Assets Directory**
   - Story template should be in `assets/story-template.md`
   - Currently embedded in Phase 5

---

## Target State Design

### Entry Point (SKILL.md ~180 lines)

```markdown
SKILL.md (Target: 180 lines)
├─ YAML Frontmatter (13 lines)
├─ Purpose & Philosophy (25 lines)
│  └─ Core principles, reusability
├─ When to Use This Skill (18 lines)
│  ├─ ✅ Trigger scenarios
│  └─ ❌ When NOT to use
├─ Story Creation Workflow (8 Phases) (50 lines)
│  ├─ Phase 1: Discovery → story-discovery.md
│  ├─ Phase 2: Requirements → requirements-analysis.md
│  ├─ Phase 3: Technical Spec → technical-specification.md
│  ├─ Phase 4: UI Spec → ui-specification.md
│  ├─ Phase 5: File Creation → story-file-creation.md
│  ├─ Phase 6: Linking → epic-sprint-linking.md
│  ├─ Phase 7: Validation → story-validation.md
│  └─ Phase 8: Completion → completion-report.md
├─ Integration Points (20 lines)
│  ├─ From: ideation, orchestration, development
│  └─ To: ui-generator, development, qa
├─ Subagent Coordination (15 lines)
│  ├─ requirements-analyst (Phase 2)
│  └─ api-designer (Phase 3, conditional)
├─ Success Criteria (15 lines)
│  └─ 12 criteria summary
├─ Reference File Map (15 lines)
│  └─ List 15 reference files
└─ Best Practices (10 lines)
   └─ Top 5 practices

Total: ~180 lines
```

### New Reference Files to Create

| New File | Lines | Source (from SKILL.md) | Purpose |
|----------|-------|------------------------|---------|
| **story-discovery.md** | ~280 | Lines 71-304 (234 lines) | Phase 1: ID generation, context |
| **requirements-analysis.md** | ~180 | Lines 306-439 (134 lines) | Phase 2: AC generation |
| **technical-specification.md** | ~250 | Lines 441-668 (228 lines) | Phase 3: API contracts, models |
| **ui-specification.md** | ~280 | Lines 670-914 (245 lines) | Phase 4: Components, mockups |
| **story-file-creation.md** | ~320 | Lines 916-1182 (267 lines) | Phase 5: YAML + markdown |
| **epic-sprint-linking.md** | ~120 | Lines 1184-1275 (92 lines) | Phase 6: Update parent docs |
| **story-validation.md** | ~200 | Lines 1277-1434 (158 lines) | Phase 7: Quality checks |
| **completion-report.md** | ~150 | Lines 1436-1554 (119 lines) | Phase 8: Summary generation |
| **error-handling.md** | ~200 | Lines 1556-1703 (148 lines) | Recovery procedures |
| **integration-guide.md** | ~100 | Enhance existing | Skill integration details |

### Keep/Enhance Existing Reference Files

| File | Current | Action | Purpose |
|------|---------|--------|---------|
| acceptance-criteria-patterns.md | 1,259 | ✅ KEEP | Used by Phase 2 |
| story-examples.md | 1,905 | ✅ KEEP | Reference examples |
| story-structure-guide.md | 662 | ✅ KEEP | Used by Phase 5 |
| technical-specification-guide.md | 1,269 | ✅ KEEP | Used by Phase 3 |
| ui-specification-guide.md | 1,344 | ✅ KEEP | Used by Phase 4 |
| validation-checklists.md | 1,038 | ✅ KEEP | Used by Phase 7 |

### Create Assets Directory

| New File | Lines | Purpose |
|----------|-------|---------|
| **assets/story-template.md** | ~300 | Story YAML + markdown template |

### Token Efficiency Projection

**Before:**
- SKILL.md activation: 1,840 lines × 8 tokens/line = **14,720 tokens**
- References loaded: 0 (until explicitly read)
- **Total first load: ~14,720 tokens**

**After:**
- SKILL.md activation: 180 lines × 8 tokens/line = **1,440 tokens**
- Reference loaded per phase: ~200-300 lines = 1,600-2,400 tokens
- **Total first load: ~1,440 tokens**
- **Typical usage: ~3,040-3,840 tokens** (entry + 1 phase)

**Efficiency Gain:** 10.2x improvement (14,720 → 1,440 tokens on activation)

---

## Refactoring Steps

### Phase 1: Preparation and Backup

#### Step 1.1: Create Backup
```bash
cd .claude/skills/devforgeai-story-creation/
cp SKILL.md SKILL.md.backup-2025-01-06
cp SKILL.md SKILL.md.original-1840-lines
```

**Validation:**
- [ ] Backup file created: `SKILL.md.backup-2025-01-06`
- [ ] Backup file has 1,840 lines
- [ ] Original preserved: `SKILL.md.original-1840-lines`

#### Step 1.2: Analyze Current Structure
```bash
# Count lines per phase
awk '/^### Phase 1: Story Discovery/,/^### Phase 2:/' SKILL.md | wc -l
awk '/^### Phase 2: Requirements/,/^### Phase 3:/' SKILL.md | wc -l
# ... continue for all 8 phases
```

**Validation:**
- [ ] Phase 1: 234 lines confirmed
- [ ] Phase 2: 134 lines confirmed
- [ ] Phase 3: 228 lines confirmed
- [ ] Phase 4: 245 lines confirmed
- [ ] Phase 5: 267 lines confirmed
- [ ] Phase 6: 92 lines confirmed
- [ ] Phase 7: 158 lines confirmed
- [ ] Phase 8: 119 lines confirmed

#### Step 1.3: Create Assets Directory
```bash
mkdir -p assets/
```

**Validation:**
- [ ] Directory created: `assets/`

---

### Phase 2: Extract Content to New Reference Files

**Order of Extraction (sequential to preserve references):**

#### Step 2.1: Extract Phase 1 → `references/story-discovery.md`

**Source:** Lines 71-304 (234 lines)

**File structure:**
```markdown
# Phase 1: Story Discovery & Context

This phase generates story ID, discovers epic/sprint context, and collects metadata.

## Overview

Story creation begins with discovery: assigning a unique ID, determining relationships to epics/sprints, and gathering essential metadata.

## Step 1.1: Generate Story ID

[Extract complete logic from SKILL.md lines ~75-120]

### ID Format

STORY-NNN where NNN is zero-padded 3-digit number

### ID Generation Algorithm

1. Glob all existing stories: .ai_docs/Stories/STORY-*.story.md
2. Extract highest number
3. Increment by 1
4. Zero-pad to 3 digits

### Conflict Detection

[Logic from SKILL.md]

## Step 1.2: Discover Epic Context

[Extract logic from lines ~125-180]

## Step 1.3: Discover Sprint Context

[Extract logic from lines ~185-230]

## Step 1.4: Collect Metadata

[Extract from lines ~235-304]

### Metadata Fields

- Title: Derived from feature description
- Priority: Default "Medium" or from conversation
- Points: Default 5 or from conversation
- Tags: Auto-detected from description

## Subagent Invocation

None in this phase.

## Output

Story ID, epic ID (if found), sprint ID (if found), metadata collected.

## Error Handling

See error-handling.md for recovery procedures.
```

**Commands:**
```bash
cd references/

awk '/^### Phase 1: Story Discovery/,/^### Phase 2: Requirements Analysis/' ../SKILL.md > story-discovery-temp.md

cat > story-discovery.md <<'EOF'
# Phase 1: Story Discovery & Context

This phase generates story ID, discovers epic/sprint context, and collects metadata.

EOF

tail -n +2 story-discovery-temp.md >> story-discovery.md
rm story-discovery-temp.md
```

**Validation:**
- [ ] File created: `references/story-discovery.md`
- [ ] Line count: ~280 lines
- [ ] All 4 steps documented (ID generation, epic, sprint, metadata)

#### Step 2.2: Extract Phase 2 → `references/requirements-analysis.md`

**Source:** Lines 306-439 (134 lines)

**File structure:**
```markdown
# Phase 2: Requirements Analysis

Generate user story and acceptance criteria using requirements-analyst subagent.

## Overview

This phase transforms the feature description into structured user story format and testable acceptance criteria.

## Step 2.1: Invoke requirements-analyst Subagent

[Extract complete invocation logic from SKILL.md]

### Prompt Structure

Task(
  subagent_type="requirements-analyst",
  description="Generate user story and AC",
  prompt="..."
)

## Step 2.2: Extract User Story

[Logic for parsing subagent output]

## Step 2.3: Extract Acceptance Criteria

[Validation logic for AC format]

### AC Format Requirements

- Given/When/Then structure
- Minimum 3 criteria
- Testable assertions

## Step 2.4: Validate Requirements

[Validation checks]

## Reference Files Used

- acceptance-criteria-patterns.md (loaded by subagent)

## Error Handling

See error-handling.md for incomplete subagent output recovery.
```

**Commands:**
```bash
cd references/

awk '/^### Phase 2: Requirements Analysis/,/^### Phase 3: Technical Specification/' ../SKILL.md > requirements-analysis-temp.md

cat > requirements-analysis.md <<'EOF'
# Phase 2: Requirements Analysis

Generate user story and acceptance criteria using requirements-analyst subagent.

EOF

tail -n +2 requirements-analysis-temp.md >> requirements-analysis.md
rm requirements-analysis-temp.md
```

**Validation:**
- [ ] File created: `references/requirements-analysis.md`
- [ ] Line count: ~180 lines
- [ ] Subagent invocation documented

#### Step 2.3: Extract Phase 3 → `references/technical-specification-creation.md`

**Source:** Lines 441-668 (228 lines)

**Note:** Different from existing `technical-specification-guide.md` (which is a guide). This is the workflow.

**Commands:**
```bash
cd references/

awk '/^### Phase 3: Technical Specification/,/^### Phase 4: UI Specification/' ../SKILL.md > tech-spec-creation-temp.md

cat > technical-specification-creation.md <<'EOF'
# Phase 3: Technical Specification Creation

Generate technical specifications including API contracts, data models, and business rules.

## Overview

This phase creates the technical foundation for implementation, defining APIs, data structures, and business logic.

EOF

tail -n +2 tech-spec-creation-temp.md >> technical-specification-creation.md
rm tech-spec-creation-temp.md
```

**Validation:**
- [ ] File created: `references/technical-specification-creation.md`
- [ ] Line count: ~250 lines
- [ ] API designer subagent invocation documented

#### Step 2.4: Extract Phase 4 → `references/ui-specification-creation.md`

**Source:** Lines 670-914 (245 lines)

**Commands:**
```bash
cd references/

awk '/^### Phase 4: UI Specification/,/^### Phase 5: Story File Creation/' ../SKILL.md > ui-spec-creation-temp.md

cat > ui-specification-creation.md <<'EOF'
# Phase 4: UI Specification Creation

Generate UI specifications including components, mockups, and accessibility requirements.

EOF

tail -n +2 ui-spec-creation-temp.md >> ui-specification-creation.md
rm ui-spec-creation-temp.md
```

**Validation:**
- [ ] File created: `references/ui-specification-creation.md`
- [ ] Line count: ~280 lines

#### Step 2.5: Extract Phase 5 → `references/story-file-creation.md` + `assets/story-template.md`

**Source:** Lines 916-1182 (267 lines - includes embedded template)

**Split into two files:**

**File 1: Workflow (story-file-creation.md)**
```markdown
# Phase 5: Story File Creation

Construct complete story document from collected information.

## Step 5.1: Build YAML Frontmatter

[Logic for frontmatter construction]

## Step 5.2: Build Markdown Sections

[Logic for section assembly]

## Step 5.3: Load Template

Load base template from assets/story-template.md

## Step 5.4: Populate Template

[Template population logic]

## Step 5.5: Write to Disk

Write to: .ai_docs/Stories/{story_id}-{slug}.story.md

## Reference Files Used

- story-structure-guide.md (formatting rules)
- assets/story-template.md (base template)
```

**File 2: Template (assets/story-template.md)**
```markdown
---
id: {story_id}
title: {title}
epic: {epic_id}
sprint: {sprint_id}
status: Backlog
priority: {priority}
points: {points}
tags: [{tags}]
---

# {title}

## User Story

[Template structure...]

## Acceptance Criteria

### AC1: {Criterion title}

...
```

**Commands:**
```bash
# Create workflow file
cd references/
awk '/^### Phase 5: Story File Creation/,/^## User Story/' ../SKILL.md | head -n -15 > story-file-creation-temp.md

cat > story-file-creation.md <<'EOF'
# Phase 5: Story File Creation

Construct complete story document from collected information.

EOF

tail -n +2 story-file-creation-temp.md >> story-file-creation.md
rm story-file-creation-temp.md

# Create template file
cd ../assets/
awk '/^## User Story/,/^### Phase 6:/' ../../SKILL.md | head -n -3 > story-template-temp.md

cat > story-template.md <<'EOF'
---
id: {story_id}
title: {title}
epic: {epic_id}
sprint: {sprint_id}
status: Backlog
priority: {priority}
points: {points}
tags: [{tags}]
---

# {title}

EOF

tail -n +2 story-template-temp.md >> story-template.md
rm story-template-temp.md
```

**Validation:**
- [ ] File created: `references/story-file-creation.md` (~80 lines)
- [ ] File created: `assets/story-template.md` (~300 lines)
- [ ] Template has all required sections

#### Step 2.6: Extract Phase 6 → `references/epic-sprint-linking.md`

**Source:** Lines 1184-1275 (92 lines)

**Commands:**
```bash
cd references/

awk '/^### Phase 6: Epic\/Sprint Linking/,/^### Phase 7: Self-Validation/' ../SKILL.md > epic-sprint-linking-temp.md

cat > epic-sprint-linking.md <<'EOF'
# Phase 6: Epic/Sprint Linking

Update epic and sprint documents to include references to newly created story.

EOF

tail -n +2 epic-sprint-linking-temp.md >> epic-sprint-linking.md
rm epic-sprint-linking-temp.md
```

**Validation:**
- [ ] File created: `references/epic-sprint-linking.md`
- [ ] Line count: ~120 lines

#### Step 2.7: Extract Phase 7 → `references/story-validation-workflow.md`

**Source:** Lines 1277-1434 (158 lines)

**Note:** Different from existing `validation-checklists.md` (which has checklists). This is the workflow.

**Commands:**
```bash
cd references/

awk '/^### Phase 7: Self-Validation/,/^### Phase 8: Completion Report/' ../SKILL.md > story-validation-workflow-temp.md

cat > story-validation-workflow.md <<'EOF'
# Phase 7: Story Self-Validation Workflow

Execute quality validation checks and self-healing procedures.

## Overview

This phase validates the generated story against quality standards and automatically corrects issues when possible.

EOF

tail -n +2 story-validation-workflow-temp.md >> story-validation-workflow.md
rm story-validation-workflow-temp.md
```

**Validation:**
- [ ] File created: `references/story-validation-workflow.md`
- [ ] Line count: ~200 lines

#### Step 2.8: Extract Phase 8 → `references/completion-report.md`

**Source:** Lines 1436-1554 (119 lines)

**Commands:**
```bash
cd references/

awk '/^### Phase 8: Completion Report/,/^## Error Handling/' ../SKILL.md > completion-report-temp.md

cat > completion-report.md <<'EOF'
# Phase 8: Completion Report Generation

Generate structured completion summary and guide user to next actions.

EOF

tail -n +2 completion-report-temp.md >> completion-report.md
rm completion-report-temp.md
```

**Validation:**
- [ ] File created: `references/completion-report.md`
- [ ] Line count: ~150 lines

#### Step 2.9: Extract Error Handling → `references/error-handling.md`

**Source:** Lines 1556-1703 (148 lines)

**File structure:**
```markdown
# Error Handling & Recovery Procedures

Complete error handling for story creation workflow.

## Error 1: Story ID Conflicts

**Detection:** [from SKILL.md]
**Recovery:** [procedure]

## Error 2: Subagent Output Incomplete

**Detection:** [from SKILL.md]
**Recovery:** [procedure]

## Error 3: Epic/Sprint Not Found

**Detection:** [from SKILL.md]
**Recovery:** [procedure]

## Error 4: UI Specification Ambiguous

**Detection:** [from SKILL.md]
**Recovery:** [procedure]

## Error 5: File Write Failures

**Detection:** [from SKILL.md]
**Recovery:** [procedure]

## Error 6: Validation Failures (Phase 7)

**Detection:** [from SKILL.md]
**Recovery:** [procedure]

## General Recovery Strategy

[Overall error handling approach]
```

**Commands:**
```bash
cd references/

awk '/^## Error Handling & Recovery/,/^## Integration with Other Skills/' ../SKILL.md > error-handling-temp.md

cat > error-handling.md <<'EOF'
# Error Handling & Recovery Procedures

Complete error handling for story creation workflow.

EOF

tail -n +2 error-handling-temp.md >> error-handling.md
rm error-handling-temp.md
```

**Validation:**
- [ ] File created: `references/error-handling.md`
- [ ] Line count: ~200 lines
- [ ] All 6 error types documented

#### Step 2.10: Create Integration Guide

**New file** (synthesized from lines 1705-1762 + enhancements)

**Commands:**
```bash
cd references/

cat > integration-guide.md <<'EOF'
# Story Creation Skill Integration Guide

How this skill integrates with other DevForgeAI skills.

## Integration Points

### Invoked By

**devforgeai-orchestration**
- Epic decomposition → story creation
- Sprint planning → story generation

**devforgeai-development**
- Deferred DoD items → tracking story creation
- Scope changes → follow-up story creation

**/create-story command**
- User-initiated story creation
- Standalone feature description

### Invokes

**requirements-analyst subagent** (Phase 2)
- User story generation
- Acceptance criteria creation

**api-designer subagent** (Phase 3, conditional)
- API contract design
- Endpoint specification

### Provides Output To

**devforgeai-ui-generator**
- Story acceptance criteria → UI requirements
- Feature description → component spec

**devforgeai-development**
- Acceptance criteria → test generation (TDD Red phase)
- Technical spec → implementation guidance

**devforgeai-qa**
- Acceptance criteria → validation targets
- Technical spec → compliance checks

## Data Flow

Feature Description (input)
  ↓
Story Creation Workflow (8 phases)
  ↓
Complete Story Document (output)
  ↓
Development → QA → Release

## Context Requirements

**Required:**
- Feature description (from user or orchestration)

**Optional:**
- Epic context (epic ID, name)
- Sprint context (sprint ID, name)
- Priority/points (defaults provided)

**Not Required:**
- Context files (story can be created without them)
- Existing stories (first story generates STORY-001)

## Reusability

This skill is invoked by 4+ framework components:
1. /create-story command (user-initiated)
2. devforgeai-orchestration (epic/sprint decomposition)
3. devforgeai-development (deferred work tracking)
4. Manual invocation (Skill(command="devforgeai-story-creation"))

## Framework Awareness

Story creation respects all 6 context files when present:
- tech-stack.md → Technology references in technical spec
- coding-standards.md → Code pattern references
- architecture-constraints.md → Layer boundary awareness
- anti-patterns.md → Forbidden pattern avoidance
- dependencies.md → Package references
- source-tree.md → File location awareness

**Operates in two modes:**
- **Greenfield:** Context files optional (before architecture phase)
- **Brownfield:** Context files referenced and respected
EOF
```

**Validation:**
- [ ] File created: `references/integration-guide.md`
- [ ] Line count: ~100 lines

---

### Phase 3: Rewrite Entry Point SKILL.md

**Target:** ~180 lines

#### Step 3.1: Create New SKILL.md Structure

```bash
cd .claude/skills/devforgeai-story-creation/

cat > SKILL.md.new <<'EOF'
---
name: devforgeai-story-creation
description: Create user stories with acceptance criteria, technical specifications, and UI specifications. Use when transforming feature descriptions into structured stories, generating stories from epic features, or creating follow-up stories for deferred work. Supports CRUD, authentication, workflow, and reporting story types with complete technical and UI specifications.
allowed-tools:
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - AskUserQuestion
  - Task
---

# DevForgeAI Story Creation Skill

Generate complete user stories with acceptance criteria, technical specifications, and UI specifications through an 8-phase workflow.

## Purpose

This skill transforms feature descriptions into comprehensive, implementation-ready user stories. Each generated story includes:

- **User Story:** As a/I want/So that format
- **Acceptance Criteria:** 3+ testable Given/When/Then scenarios
- **Technical Specification:** API contracts, data models, business rules
- **UI Specification:** Components, mockups, accessibility (if applicable)
- **Non-Functional Requirements:** Performance, security, scalability targets
- **Definition of Done:** Implementation, quality, testing, documentation checklists

### Core Philosophy

- **Self-contained stories** - Each story is independently implementable
- **Testable criteria** - All AC can be converted to automated tests
- **Complete specifications** - No ambiguity, ready for TDD implementation
- **Framework-aware** - Respects context files when present
- **Reusable** - Invoked by commands, skills, and manual requests

## When to Use This Skill

### ✅ Trigger Scenarios

- User runs `/create-story [feature-description]` command
- devforgeai-orchestration decomposes epic features into stories
- devforgeai-development creates tracking stories for deferred DoD items
- Sprint planning requires story generation
- Manual invocation: `Skill(command="devforgeai-story-creation")`

### ❌ When NOT to Use

- Epic creation (use devforgeai-orchestration epic mode)
- Sprint planning (use devforgeai-orchestration sprint mode)
- Story already exists (use Edit tool to modify)

---

## Story Creation Workflow (8 Phases)

Each phase loads its reference file on-demand for detailed implementation.

### Phase 1: Story Discovery
**Purpose:** Generate story ID, discover epic/sprint context, collect metadata
**Reference:** `story-discovery.md`
**Output:** Story ID, epic/sprint links, metadata (priority, points, tags)

### Phase 2: Requirements Analysis
**Purpose:** Generate user story and acceptance criteria
**Reference:** `requirements-analysis.md`
**Subagent:** requirements-analyst
**Output:** User story, 3+ AC (Given/When/Then format)

### Phase 3: Technical Specification
**Purpose:** Define API contracts, data models, business rules
**Reference:** `technical-specification-creation.md`
**Subagent:** api-designer (conditional - if API endpoints detected)
**Output:** API contracts, data models, dependencies

### Phase 4: UI Specification
**Purpose:** Document UI components, mockups, accessibility
**Reference:** `ui-specification-creation.md`
**Output:** Component list, ASCII mockups, WCAG AA compliance

### Phase 5: Story File Creation
**Purpose:** Assemble complete story document
**Reference:** `story-file-creation.md`
**Template:** `assets/story-template.md`
**Output:** Complete .story.md file in .ai_docs/Stories/

### Phase 6: Epic/Sprint Linking
**Purpose:** Update parent documents with story references
**Reference:** `epic-sprint-linking.md`
**Output:** Epic/sprint files updated

### Phase 7: Self-Validation
**Purpose:** Quality checks and self-healing
**Reference:** `story-validation-workflow.md`
**Checklist:** `validation-checklists.md`
**Output:** Validated story, auto-corrected issues

### Phase 8: Completion Report
**Purpose:** Generate summary and guide next actions
**Reference:** `completion-report.md`
**Output:** Structured completion summary, next step recommendations

**See individual phase reference files for complete implementation details.**

---

## Subagent Coordination

This skill delegates specialized tasks to subagents:

- **requirements-analyst** (Phase 2) - User story and AC generation
- **api-designer** (Phase 3, conditional) - API contract design when endpoints detected

**See `references/requirements-analysis.md` and `references/technical-specification-creation.md` for subagent coordination details.**

---

## Integration Points

**Invoked by:**
- `/create-story` command (user-initiated)
- devforgeai-orchestration skill (epic/sprint decomposition)
- devforgeai-development skill (deferred work tracking)

**Provides output to:**
- devforgeai-ui-generator (AC → UI requirements)
- devforgeai-development (AC → test generation)
- devforgeai-qa (AC → validation targets)

**See `references/integration-guide.md` for complete integration patterns.**

---

## Success Criteria

Complete story generated with:
- [ ] Valid story ID (STORY-NNN format)
- [ ] User story (As a/I want/So that)
- [ ] 3+ acceptance criteria (Given/When/Then)
- [ ] Technical specification (complete)
- [ ] UI specification (if applicable)
- [ ] Non-functional requirements (measurable)
- [ ] Edge cases documented
- [ ] Definition of Done (checkboxes)
- [ ] File written to .ai_docs/Stories/
- [ ] Epic/sprint updated (if applicable)
- [ ] Self-validation passed
- [ ] Token usage <90K (isolated context)

---

## Reference Files

Load these on-demand during workflow execution:

### Phase Workflows (8 files)
- **story-discovery.md** - Phase 1: ID generation, context discovery
- **requirements-analysis.md** - Phase 2: User story and AC
- **technical-specification-creation.md** - Phase 3: APIs, models, rules
- **ui-specification-creation.md** - Phase 4: Components, mockups
- **story-file-creation.md** - Phase 5: Document assembly
- **epic-sprint-linking.md** - Phase 6: Parent doc updates
- **story-validation-workflow.md** - Phase 7: Quality checks
- **completion-report.md** - Phase 8: Summary generation

### Supporting Guides (6 files - existing)
- **acceptance-criteria-patterns.md** - Given/When/Then templates by domain
- **story-examples.md** - 4 complete story examples (CRUD, auth, workflow, reporting)
- **story-structure-guide.md** - YAML frontmatter, section formatting
- **technical-specification-guide.md** - API contract patterns, data modeling
- **ui-specification-guide.md** - Component design, ASCII mockups, accessibility
- **validation-checklists.md** - Quality validation procedures

### Supporting Files
- **integration-guide.md** - Skill integration patterns
- **error-handling.md** - Recovery procedures

### Assets
- **assets/story-template.md** - Base story template (YAML + markdown)

---

## Best Practices

**Top 5 practices for story creation:**

1. **Use feature description** - Provide clear, specific feature description in conversation
2. **Associate with epic** - Link stories to epics when possible for traceability
3. **Validate AC quality** - Ensure all AC are testable (Given/When/Then)
4. **Include UI specs** - Document UI components when applicable
5. **Self-validate** - Let Phase 7 auto-correct common issues

**See phase-specific reference files for detailed best practices.**

EOF
```

**Validation:**
- [ ] New file created: `SKILL.md.new`
- [ ] Line count ≤200 lines
- [ ] All 8 phases summarized
- [ ] References to all 15 files

#### Step 3.2: Validate Line Count

```bash
wc -l SKILL.md.new
# Must be ≤200 lines
```

**Expected:** ~180 lines

**If over 200:**
- Condense Purpose section (25 → 20 lines)
- Condense Success Criteria (15 → 10 lines)
- Reduce Best Practices (10 → 5 lines)

**Validation:**
- [ ] Line count ≤200 lines

#### Step 3.3: Replace Original SKILL.md

```bash
# After validation passes
mv SKILL.md.new SKILL.md
```

**Validation:**
- [ ] SKILL.md replaced
- [ ] Backup still exists

---

### Phase 4: Testing

#### Step 4.1: Cold Start Test

```bash
wc -l .claude/skills/devforgeai-story-creation/SKILL.md
# Must be ≤200 lines
```

**Validation:**
- [ ] SKILL.md ≤200 lines
- [ ] Activation time <100ms (manual observation)

#### Step 4.2: Phase Execution Test

**Test:** Each phase correctly loads its reference file

**Test Case: Phase 2 (Requirements Analysis)**
```
Invoke skill with feature description

Expected:
1. Phase 2 triggered
2. Reference loaded: requirements-analysis.md
3. Subagent invoked: requirements-analyst
4. AC generated in Given/When/Then format
```

**Validation:**
- [ ] Phase 2 executes correctly
- [ ] requirements-analysis.md loaded
- [ ] requirements-analyst invoked
- [ ] AC generated

#### Step 4.3: Integration Test

**Test:** Complete story creation from feature description

```
Input: "User login with email and password"

Expected output:
- Story file created: .ai_docs/Stories/STORY-NNN-user-login.story.md
- YAML frontmatter populated
- User story section complete
- 3+ acceptance criteria
- Technical specification (API endpoints, data models)
- UI specification (login form components)
- Definition of Done checklist
```

**Validation:**
- [ ] Story file created
- [ ] All sections populated
- [ ] File structure correct

#### Step 4.4: Regression Test

**Test:** Behavior unchanged from original

**Validation:**
- [ ] Same story quality generated
- [ ] Same sections included
- [ ] Subagents still invoked
- [ ] Validation still runs

#### Step 4.5: Token Measurement

```bash
# Measure activation token usage
# Original: ~14,720 tokens
# Target: ~1,440 tokens (10x improvement)
```

**Validation:**
- [ ] Token usage measured
- [ ] ≥8x improvement achieved

---

### Phase 5: Documentation and Completion

#### Step 5.1: Update This Document

**Mark completion:**
- [ ] Status: COMPLETE
- [ ] Final line count: [actual]
- [ ] Token reduction: [actual %]
- [ ] Completion date: [date]
- [ ] Fill "Results" section below

#### Step 5.2: Commit Changes

```bash
cd /mnt/c/Projects/DevForgeAI2

git add .claude/skills/devforgeai-story-creation/
git commit -m "refactor(story-creation): Progressive disclosure - 1840→180 lines

- Reduced SKILL.md from 1,840 to ~180 lines (90% reduction)
- Created 9 new reference files for 8-phase workflow
- Created assets/story-template.md (300 lines)
- Organized 15 reference files total
- Token efficiency: 10x improvement (14.7K→1.4K on activation)
- All functionality preserved, behavior unchanged

Addresses: Reddit article cold start optimization
Pattern: Progressive disclosure per Anthropic architecture
Testing: All phases validated, integration tests pass"
```

**Validation:**
- [ ] Changes committed
- [ ] Commit message complete

#### Step 5.3: Update Framework Memory (After Parallel Sessions Complete)

**⚠️ IMPORTANT:** Use AskUserQuestion before updating shared files.

**Files to update:**
- `.claude/memory/skills-reference.md` (update story-creation entry)
- `.claude/memory/commands-reference.md` (update /create-story integration)

**Validation:**
- [ ] User confirmed no conflicts
- [ ] Shared files updated

---

## Completion Criteria

**All must be TRUE before marking COMPLETE:**

- [ ] SKILL.md ≤200 lines
- [ ] All 9 new reference files created
- [ ] assets/story-template.md created
- [ ] 15 reference files total
- [ ] Cold start test passes (<200 lines loaded)
- [ ] Phase execution tests pass (all 8 phases)
- [ ] Integration test passes (complete story created)
- [ ] Regression test passes (behavior unchanged)
- [ ] Token efficiency ≥8x improvement
- [ ] Changes committed to git
- [ ] This document updated with results

---

## Session Handoff Notes

**For next Claude session picking up this work:**

### Quick Start

1. **Read this document completely** - All context and steps are here
2. **Check status** - Resume from unchecked items in Refactoring Steps
3. **Create backup first** - Always preserve SKILL.md.backup-2025-01-06
4. **Extract sequentially** - Phase 2.1 → 2.10 in order
5. **Test incrementally** - Validate after each extraction
6. **Update checkboxes** - Mark progress as you go
7. **Commit frequently** - After Phase 2, 3, 4, 5

### Critical Reminders

- **Template extraction** - Phase 5 has embedded template, split into workflow + assets/
- **Two specification files** - technical-specification-CREATION.md (workflow) vs technical-specification-GUIDE.md (patterns guide)
- **Subagent coordination** - requirements-analyst (Phase 2), api-designer (Phase 3 conditional)
- **Error handling comprehensive** - 6 error types, all must be preserved
- **Asset directory** - Must create assets/ directory first
- **Shared files** - Use AskUserQuestion before updating .claude/memory/*.md

### Common Pitfalls

1. **Don't confuse workflow vs guide files** - Creation workflow ≠ reference guide
2. **Don't skip template extraction** - Template must go to assets/, not references/
3. **Preserve conditional logic** - API designer is conditional, not always invoked
4. **Test story quality** - Generated stories must match original quality
5. **Validate all 8 phases** - Each must execute correctly

### If Stuck

1. **Review story-examples.md** - See complete story examples for quality reference
2. **Check existing references** - Pattern already established in 6 existing files
3. **Read acceptance-criteria-patterns.md** - Understand AC generation requirements
4. **Measure phase lines** - Each phase should be 80-320 lines in reference

### Success Indicators

- ✅ SKILL.md opens instantly (responsive)
- ✅ Only relevant phase reference loads (not all 15)
- ✅ Stories generated match original quality
- ✅ Token usage ~1,440 on activation (down from ~14,720)

---

## Results (Post-Completion)

**To be filled in after refactoring completes:**

### Metrics Achieved

- **Final SKILL.md lines:** [X] (Target: ≤200)
- **Reference files created:** [N] (Target: 9 new + 6 existing = 15 total)
- **Assets created:** [M] (Target: 1 template file)
- **Token reduction:** [Y]% (Target: ≥88%)
- **Activation time:** [Z]ms (Target: <100ms)
- **Efficiency gain:** [R]x (Target: ≥8x)

### Files Modified

- `.claude/skills/devforgeai-story-creation/SKILL.md` (1,840 → [X] lines)
- `.claude/skills/devforgeai-story-creation/references/` (6 → 15 files)
  - Created: [list 9 new files]
- `.claude/skills/devforgeai-story-creation/assets/` (NEW directory)
  - Created: story-template.md

### Lessons Learned

[Notes for future skill refactorings]

### Unexpected Issues

[Any problems encountered and solutions]

### Recommendations for Next Skills

[What worked well, what to improve]

---

## Appendix: Line Count Breakdown

**Original SKILL.md (1,840 lines):**

| Section | Lines | % | Extraction Target |
|---------|-------|---|-------------------|
| Frontmatter | 13 | 0.7% | Keep |
| Purpose/Philosophy | 37 | 2.0% | Keep (condense to 25) |
| When to Use | 18 | 1.0% | Keep |
| Phase 1: Discovery | 234 | 12.7% | → story-discovery.md |
| Phase 2: Requirements | 134 | 7.3% | → requirements-analysis.md |
| Phase 3: Tech Spec | 228 | 12.4% | → technical-specification-creation.md |
| Phase 4: UI Spec | 245 | 13.3% | → ui-specification-creation.md |
| Phase 5: File Creation | 267 | 14.5% | → story-file-creation.md + assets/template |
| Phase 6: Linking | 92 | 5.0% | → epic-sprint-linking.md |
| Phase 7: Validation | 158 | 8.6% | → story-validation-workflow.md |
| Phase 8: Completion | 119 | 6.5% | → completion-report.md |
| Error Handling | 148 | 8.0% | → error-handling.md |
| Integration | 58 | 3.2% | → integration-guide.md (condense, 20 in SKILL.md) |
| Success Criteria | 22 | 1.2% | Keep (condense to 15) |
| Reference List | 23 | 1.3% | Keep (update) |
| Best Practices | 30 | 1.6% | Keep (condense to 10) |
| **TOTAL** | **1,840** | **100%** | **15 references + 1 asset** |

**Target SKILL.md (~180 lines):**

| Section | Lines | % |
|---------|-------|---|
| Frontmatter | 13 | 7.2% |
| Purpose | 25 | 13.9% |
| When to Use | 18 | 10% |
| 8-Phase Summary | 50 | 27.8% |
| Subagents | 15 | 8.3% |
| Integration | 20 | 11.1% |
| Success Criteria | 15 | 8.3% |
| Reference Map | 15 | 8.3% |
| Best Practices | 10 | 5.6% |
| **TOTAL** | **~180** | **~100%** |

---

**Document Version:** 1.0
**Created:** 2025-01-06
**Last Updated:** 2025-01-06 (Initial creation)
**Next Review:** After refactoring completion
