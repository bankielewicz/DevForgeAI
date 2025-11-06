# DevForgeAI Orchestration Skill - Refactoring Plan

**Status:** NOT STARTED
**Assigned Session:** None
**Last Updated:** 2025-01-06 (Initial Creation)
**Estimated Effort:** 4-6 hours
**Priority:** P1 - CRITICAL (Worst offender: 16x over limit)

---

## Executive Summary

The `devforgeai-orchestration` skill is the most critical refactoring target in the DevForgeAI framework. At **3,249 lines**, it is **16.2x over the optimal 200-line limit** identified in the Reddit article analysis.

**Key Issue:** Despite having 10 reference files (7,664 lines), the SKILL.md entry point contains comprehensive workflow documentation that should be progressively loaded.

**Target:** Reduce SKILL.md from 3,249 lines to ~200 lines while maintaining all functionality through improved progressive disclosure.

**Expected Gains:**
- **Token efficiency:** 16x improvement on skill activation
- **Activation time:** 500ms+ → <100ms (estimated)
- **Context relevance:** 30% → 90%+ (only load what's needed)

---

## Current State Analysis

### Metrics

| Metric | Current | Target | Gap |
|--------|---------|--------|-----|
| **SKILL.md lines** | 3,249 | ~200 | -3,049 (-94%) |
| **References files** | 10 files | 15-20 files | +5-10 |
| **References lines** | 7,664 | ~10,000 | +2,336 |
| **Total lines** | 10,913 | ~10,200 | -713 |
| **Entry point ratio** | 29.7% | ~2% | -27.7% |
| **Cold start load** | 3,249 lines | <200 lines | -3,049 |
| **Estimated tokens** | ~26,000 | ~1,600 | -24,400 (-94%) |

### Current Structure (Line Distribution)

```
SKILL.md (3,249 lines total):
├─ Lines 1-13:     YAML Frontmatter (13 lines)
├─ Lines 15-58:    Purpose & When to Use (44 lines) ✅ KEEP
├─ Lines 60-144:   Mode Detection (85 lines) → EXTRACT to mode-detection.md
├─ Lines 146-160:  Workflow States (15 lines) ✅ KEEP (summary only)
├─ Lines 162-329:  Phase 0: Checkpoint Detection (168 lines) → EXTRACT
├─ Lines 330-373:  Phase 1: Load and Validate (44 lines) → EXTRACT
├─ Lines 374-450:  Phase 2: Skill Invocation (77 lines) → EXTRACT
├─ Lines 451-738:  Phase 3: Sprint Planning (288 lines) → ALREADY HAS sprint-planning.md
├─ Lines 739-771:  Phase 3A: Update Story Status (33 lines) → EXTRACT
├─ Lines 773-1231: Phase 3.5: QA Retry Loop (459 lines) → EXTRACT to qa-retry-workflow.md
├─ Lines 1232-1273: QA Attempt Template (42 lines) → EXTRACT
├─ Lines 1274-1277: Phase 4 Header (4 lines) ✅ KEEP
├─ Lines 1278-2656: Phase 4A: Epic Creation (1,379 lines) → Already has epic-* refs, needs cleanup
├─ Lines 2658-2791: Phase 4.5: Deferred Tracking (134 lines) → EXTRACT to deferred-tracking.md
├─ Lines 2793-2811: Phase 5: Next Action (19 lines) ✅ KEEP
├─ Lines 2813-2986: Phase 6: Finalization (174 lines) → EXTRACT to finalization.md
├─ Lines 2988-3016: Quality Gate Enforcement (29 lines) ✅ KEEP (summary)
├─ Lines 3017-3249: AskUserQuestion Patterns (233 lines) → EXTRACT to user-interaction-patterns.md
```

### Existing Reference Files

| File | Lines | Status | Usage |
|------|-------|--------|-------|
| epic-management.md | 496 | ✅ Good | Epic Phases 1-2 |
| epic-validation-checklist.md | 760 | ✅ Good | Epic Phase 7 |
| feature-decomposition-patterns.md | 903 | ✅ Good | Epic Phase 3 |
| quality-gates.md | 1,017 | ✅ Good | Referenced |
| sprint-planning-guide.md | 631 | ⚠️ Duplicate | Use this one |
| sprint-planning.md | 620 | ⚠️ Duplicate | DELETE |
| state-transitions.md | 1,105 | ✅ Good | Referenced |
| story-management.md | 633 | ✅ Good | Story workflow |
| technical-assessment-guide.md | 914 | ✅ Good | Epic Phase 4 |
| workflow-states.md | 585 | ✅ Good | Referenced |

**Action:** Delete duplicate `sprint-planning.md`, keep `sprint-planning-guide.md`

### Problems Identified

1. **Mode Detection Too Detailed (85 lines)**
   - Contains complete workflow descriptions for each mode
   - Should be: Brief description + pointer to reference
   - Extract to: `mode-detection.md`

2. **Phase 0-6 Inline Documentation (2,827 lines)**
   - 87% of SKILL.md is detailed phase implementation
   - Should be: Phase summary + "See [reference].md for details"
   - Extract to: Individual phase reference files

3. **Epic Creation Embedded (1,379 lines)**
   - Epic workflow is 42% of entire SKILL.md
   - Already has 5 epic-related reference files but still inline
   - Should be: "Epic mode detected → Load epic-management.md"

4. **QA Retry Logic Inline (459 lines)**
   - Complex retry workflow with templates embedded
   - Should be: Separate reference file

5. **AskUserQuestion Patterns (233 lines)**
   - 12 detailed interaction patterns with examples
   - Should be: Separate reference file

6. **Duplicate Reference Files**
   - Both `sprint-planning.md` and `sprint-planning-guide.md` exist
   - Creates confusion, wastes space

---

## Target State Design

### Entry Point (SKILL.md ~200 lines)

```markdown
SKILL.md (Target: 195 lines)
├─ YAML Frontmatter (13 lines)
├─ Purpose & Philosophy (35 lines)
│  └─ Core Responsibilities (brief bullet points)
├─ When to Use This Skill (20 lines)
│  └─ Entry point examples
├─ Mode Detection (20 lines)
│  ├─ Epic Mode → See mode-detection.md
│  ├─ Sprint Mode → See mode-detection.md
│  ├─ Story Mode → See mode-detection.md
│  └─ Default Mode → See mode-detection.md
├─ Workflow States Overview (15 lines)
│  └─ 11 states listed → See workflow-states.md for details
├─ Orchestration Phases Summary (40 lines)
│  ├─ Phase 0: Checkpoint Detection → checkpoint-detection.md
│  ├─ Phase 1: Story Validation → story-validation.md
│  ├─ Phase 2: Skill Invocation → skill-invocation.md
│  ├─ Phase 3: Sprint Planning → sprint-planning-guide.md
│  ├─ Phase 3A: Status Update → story-status-update.md
│  ├─ Phase 3.5: QA Retry → qa-retry-workflow.md
│  ├─ Phase 4A: Epic Creation → epic-management.md
│  ├─ Phase 4.5: Deferred Tracking → deferred-tracking.md
│  ├─ Phase 5: Next Action → next-action-determination.md
│  └─ Phase 6: Finalization → orchestration-finalization.md
├─ Quality Gates Summary (20 lines)
│  └─ 4 gates listed → See quality-gates.md for details
├─ Subagent Coordination (15 lines)
│  ├─ requirements-analyst
│  ├─ architect-reviewer
│  ├─ sprint-planner
│  └─ technical-debt-analyzer
├─ Reference File Map (20 lines)
│  └─ List all 20 reference files with brief descriptions
└─ Common Issues & Solutions (10 lines)
   └─ Top 5 issues → See troubleshooting.md
```

### New Reference Files to Create

| New File | Lines | Source (from SKILL.md) | Purpose |
|----------|-------|------------------------|---------|
| **mode-detection.md** | ~150 | Lines 60-144 (85 lines) | Complete mode detection logic |
| **checkpoint-detection.md** | ~200 | Lines 162-329 (168 lines) | Phase 0 checkpoint recovery |
| **story-validation.md** | ~80 | Lines 330-373 (44 lines) | Phase 1 validation |
| **skill-invocation.md** | ~120 | Lines 374-450 (77 lines) | Phase 2 skill coordination |
| **story-status-update.md** | ~60 | Lines 739-771 (33 lines) | Phase 3A status transitions |
| **qa-retry-workflow.md** | ~500 | Lines 773-1273 (501 lines) | Phase 3.5 QA retry with templates |
| **deferred-tracking.md** | ~180 | Lines 2658-2791 (134 lines) | Phase 4.5 technical debt |
| **next-action-determination.md** | ~40 | Lines 2793-2811 (19 lines) | Phase 5 decision logic |
| **orchestration-finalization.md** | ~220 | Lines 2813-2986 (174 lines) | Phase 6 completion |
| **user-interaction-patterns.md** | ~300 | Lines 3017-3249 (233 lines) | AskUserQuestion templates |
| **troubleshooting.md** | ~150 | New | Common issues + solutions |

### Modified Reference Files

| File | Current | Action | New Lines |
|------|---------|--------|-----------|
| sprint-planning.md | 620 | ❌ DELETE | 0 |
| sprint-planning-guide.md | 631 | ✅ KEEP | 631 |
| epic-management.md | 496 | 📝 ENHANCE | ~600 |

### Token Efficiency Projection

**Before:**
- SKILL.md activation: 3,249 lines × 8 tokens/line = **25,992 tokens**
- References loaded: 0 (until explicitly read)
- **Total first load: ~26,000 tokens**

**After:**
- SKILL.md activation: 195 lines × 8 tokens/line = **1,560 tokens**
- Reference loaded on-demand: ~200-500 lines per phase = 1,600-4,000 tokens
- **Total first load: ~1,600 tokens**
- **Typical usage: ~3,200-5,600 tokens** (entry + 1-2 references)

**Efficiency Gain:** 16.6x improvement (26,000 → 1,560 tokens on activation)

---

## Refactoring Steps

### Phase 1: Preparation and Backup

#### Step 1.1: Create Backup
```bash
cd .claude/skills/devforgeai-orchestration/
cp SKILL.md SKILL.md.backup-2025-01-06
cp SKILL.md SKILL.md.original-3249-lines
```

**Validation:**
- [ ] Backup file created: `SKILL.md.backup-2025-01-06`
- [ ] Backup file has 3,249 lines
- [ ] Original preserved: `SKILL.md.original-3249-lines`

#### Step 1.2: Analyze Current Structure
```bash
# Count lines per section
awk '/^## Mode Detection/,/^## Workflow States/ {print}' SKILL.md | wc -l
awk '/^## Orchestration Workflow/,/^## Quality Gate Enforcement/ {print}' SKILL.md | wc -l
```

**Validation:**
- [ ] Mode Detection: 87 lines confirmed
- [ ] Orchestration Workflow: 2,827 lines confirmed

#### Step 1.3: Document Current Behavior
```bash
# Test current skill activation
# (In separate test session, not this refactoring session)
echo "Test Case 1: Epic creation" > test-log.txt
echo "Test Case 2: Sprint planning" >> test-log.txt
echo "Test Case 3: Story progression" >> test-log.txt
```

**Validation:**
- [ ] Test cases documented
- [ ] Current behavior baseline recorded

---

### Phase 2: Extract Content to New Reference Files

**Order of Extraction (do in sequence to avoid breaking references):**

#### Step 2.1: Extract Mode Detection → `mode-detection.md`

**Source:** Lines 60-144 (85 lines)

**File structure:**
```markdown
# Mode Detection Logic

This file contains the complete logic for detecting which orchestration mode to execute based on conversation context markers.

## How Mode Detection Works

The skill searches the conversation for explicit context markers to determine workflow.

## Epic Creation Mode

**Detection markers:**
- `**Command:** create-epic`
- `**Epic name:** {name}` (required)

**Workflow triggered:** Phase 4A - Epic Creation

[... full details from SKILL.md lines 64-88 ...]

## Sprint Planning Mode

[... full details from SKILL.md lines 90-107 ...]

## Story Management Mode

[... full details from SKILL.md lines 109-119 ...]

## Default Mode

[... full details from SKILL.md lines 121-144 ...]

## Mode Priority

1. Check for Epic markers first
2. Check for Sprint markers second
3. Check for Story markers third
4. Fall back to Default mode

## Troubleshooting

- Missing markers: Mode defaults to Story Management
- Conflicting markers: First match wins
```

**Commands:**
```bash
cd references/

# Extract lines 60-144 to temporary file
awk '/^## Mode Detection/,/^## Workflow States/' ../SKILL.md > mode-detection-temp.md

# Create proper reference file with header
cat > mode-detection.md <<'EOF'
# Mode Detection Logic

This file contains the complete logic for detecting which orchestration mode to execute based on conversation context markers.

EOF

# Append extracted content (skip the ## Mode Detection header line)
tail -n +2 mode-detection-temp.md >> mode-detection.md

# Clean up
rm mode-detection-temp.md
```

**Validation:**
- [ ] File created: `references/mode-detection.md`
- [ ] Line count: ~150 lines
- [ ] Contains all 4 modes (Epic, Sprint, Story, Default)
- [ ] Header section included

#### Step 2.2: Extract Phase 0 → `checkpoint-detection.md`

**Source:** Lines 162-329 (168 lines)

**File structure:**
```markdown
# Phase 0: Checkpoint Detection and Recovery

Orchestration workflows can be interrupted and resumed. This phase detects existing checkpoints and resumes from the last successful stage.

## Purpose

When `/orchestrate` command is run, this phase checks for:
1. Existing checkpoints (DEV_COMPLETE, QA_APPROVED, STAGING_COMPLETE)
2. Current story status
3. Last successful phase

## Checkpoint Types

### DEV_COMPLETE
[Details from SKILL.md]

### QA_APPROVED
[Details from SKILL.md]

### STAGING_COMPLETE
[Details from SKILL.md]

## Detection Logic

[Full algorithm from lines 162-329]

## Resume Strategy

[Complete resume logic]
```

**Commands:**
```bash
cd references/

# Extract Phase 0 content
awk '/^### Phase 0: Story Loading and Checkpoint Detection/,/^### Phase 1: Load and Validate Story/' ../SKILL.md > checkpoint-detection-temp.md

# Create proper file
cat > checkpoint-detection.md <<'EOF'
# Phase 0: Checkpoint Detection and Recovery

Orchestration workflows can be interrupted and resumed. This phase detects existing checkpoints and resumes from the last successful stage.

EOF

# Append content
tail -n +2 checkpoint-detection-temp.md >> checkpoint-detection.md
rm checkpoint-detection-temp.md
```

**Validation:**
- [ ] File created: `references/checkpoint-detection.md`
- [ ] Line count: ~200 lines
- [ ] All 3 checkpoint types documented
- [ ] Resume logic included

#### Step 2.3: Extract Phase 1 → `story-validation.md`

**Source:** Lines 330-373 (44 lines)

**Commands:**
```bash
cd references/

awk '/^### Phase 1: Load and Validate Story/,/^### Phase 2: Orchestrate Skill Invocation/' ../SKILL.md > story-validation-temp.md

cat > story-validation.md <<'EOF'
# Phase 1: Story Loading and Validation

This phase loads the story file and performs pre-execution validation checks.

EOF

tail -n +2 story-validation-temp.md >> story-validation.md
rm story-validation-temp.md
```

**Validation:**
- [ ] File created: `references/story-validation.md`
- [ ] Line count: ~80 lines

#### Step 2.4: Extract Phase 2 → `skill-invocation.md`

**Source:** Lines 374-450 (77 lines)

**Commands:**
```bash
cd references/

awk '/^### Phase 2: Orchestrate Skill Invocation/,/^### Phase 3: Sprint Planning Workflow/' ../SKILL.md > skill-invocation-temp.md

cat > skill-invocation.md <<'EOF'
# Phase 2: Skill Invocation Coordination

This phase coordinates automatic invocation of other DevForgeAI skills based on story status and workflow stage.

## Skills Coordinated

1. devforgeai-architecture
2. devforgeai-development
3. devforgeai-qa
4. devforgeai-release

EOF

tail -n +2 skill-invocation-temp.md >> skill-invocation.md
rm skill-invocation-temp.md
```

**Validation:**
- [ ] File created: `references/skill-invocation.md`
- [ ] Line count: ~120 lines

#### Step 2.5: Extract Phase 3A → `story-status-update.md`

**Source:** Lines 739-771 (33 lines)

**Commands:**
```bash
cd references/

awk '/^### Phase 3A: Update Story Status/,/^### {timestamp}/' ../SKILL.md > story-status-update-temp.md

cat > story-status-update.md <<'EOF'
# Phase 3A: Story Status Update

Updates story status and appends workflow history entries.

EOF

tail -n +2 story-status-update-temp.md >> story-status-update.md
rm story-status-update-temp.md
```

**Validation:**
- [ ] File created: `references/story-status-update.md`
- [ ] Line count: ~60 lines

#### Step 2.6: Extract Phase 3.5 → `qa-retry-workflow.md` (LARGE)

**Source:** Lines 773-1273 (501 lines - includes templates)

**File structure:**
```markdown
# Phase 3.5: QA Failure Recovery with Retry Loop

When QA fails, this phase manages the retry workflow with maximum 3 attempts.

## Overview

[Purpose and retry strategy]

## Retry Loop Logic

[Full algorithm from SKILL.md]

## Attempt Tracking

[How attempts are counted and recorded]

## Deferral-Specific Handling

[Special logic for deferral failures]

## Templates

### QA Attempt Entry Template
```
### QA Attempt {n}: {RESULT} - {timestamp}
...
```

### Success Template
[...]

### Failure Template
[...]
```

**Commands:**
```bash
cd references/

awk '/^### Phase 3.5: QA Failure Recovery with Retry Loop/,/^### Phase 4: Epic and Sprint Management/' ../SKILL.md > qa-retry-workflow-temp.md

cat > qa-retry-workflow.md <<'EOF'
# Phase 3.5: QA Failure Recovery with Retry Loop

When QA fails, this phase manages the retry workflow with maximum 3 attempts.

EOF

tail -n +2 qa-retry-workflow-temp.md >> qa-retry-workflow.md
rm qa-retry-workflow-temp.md
```

**Validation:**
- [ ] File created: `references/qa-retry-workflow.md`
- [ ] Line count: ~500 lines
- [ ] Templates included
- [ ] Max 3 attempts logic documented

#### Step 2.7: Extract Phase 4.5 → `deferred-tracking.md`

**Source:** Lines 2658-2791 (134 lines)

**Commands:**
```bash
cd references/

awk '/^### Phase 4.5: Deferred Work Tracking/,/^### Phase 5: Determine Next Action/' ../SKILL.md > deferred-tracking-temp.md

cat > deferred-tracking.md <<'EOF'
# Phase 4.5: Deferred Work Tracking

Tracks deferred Definition of Done (DoD) items and ensures follow-up stories/ADRs exist.

EOF

tail -n +2 deferred-tracking-temp.md >> deferred-tracking.md
rm deferred-tracking-temp.md
```

**Validation:**
- [ ] File created: `references/deferred-tracking.md`
- [ ] Line count: ~180 lines

#### Step 2.8: Extract Phase 5 → `next-action-determination.md`

**Source:** Lines 2793-2811 (19 lines)

**Commands:**
```bash
cd references/

awk '/^### Phase 5: Determine Next Action/,/^### Phase 6: Orchestration Finalization/' ../SKILL.md > next-action-temp.md

cat > next-action-determination.md <<'EOF'
# Phase 5: Next Action Determination

Determines recommended next steps based on current story status and workflow stage.

EOF

tail -n +2 next-action-temp.md >> next-action-determination.md
rm next-action-temp.md
```

**Validation:**
- [ ] File created: `references/next-action-determination.md`
- [ ] Line count: ~40 lines

#### Step 2.9: Extract Phase 6 → `orchestration-finalization.md`

**Source:** Lines 2813-2986 (174 lines)

**Commands:**
```bash
cd references/

awk '/^### Phase 6: Orchestration Finalization/,/^## Quality Gate Enforcement/' ../SKILL.md > finalization-temp.md

cat > orchestration-finalization.md <<'EOF'
# Phase 6: Orchestration Finalization

Final phase that generates completion summary and updates workflow history.

EOF

tail -n +2 finalization-temp.md >> orchestration-finalization.md
rm finalization-temp.md
```

**Validation:**
- [ ] File created: `references/orchestration-finalization.md`
- [ ] Line count: ~220 lines

#### Step 2.10: Extract User Interaction → `user-interaction-patterns.md`

**Source:** Lines 3017-3249 (233 lines)

**File structure:**
```markdown
# User Interaction Patterns

AskUserQuestion templates and patterns used throughout orchestration workflows.

## Pattern 1: Story Priority Conflict

[Full pattern from SKILL.md]

## Pattern 2: Epic Feature Review

[Full pattern]

... (12 patterns total)

## Best Practices

- Use multiSelect when appropriate
- Provide clear header (max 12 chars)
- Include descriptions for each option
```

**Commands:**
```bash
cd references/

awk '/^## AskUserQuestion Patterns/,EOF' ../SKILL.md > user-interaction-temp.md

cat > user-interaction-patterns.md <<'EOF'
# User Interaction Patterns

AskUserQuestion templates and patterns used throughout orchestration workflows.

EOF

tail -n +2 user-interaction-temp.md >> user-interaction-patterns.md
rm user-interaction-temp.md
```

**Validation:**
- [ ] File created: `references/user-interaction-patterns.md`
- [ ] Line count: ~300 lines
- [ ] All 12 patterns included

#### Step 2.11: Create New Troubleshooting Reference

**New file** (not extracted, synthesized from common issues)

**Commands:**
```bash
cd references/

cat > troubleshooting.md <<'EOF'
# Orchestration Troubleshooting Guide

Common issues and solutions for the DevForgeAI orchestration skill.

## Issue 1: Mode Detection Fails

**Symptom:** Skill defaults to Story Management mode when Epic/Sprint expected

**Cause:** Missing context markers

**Solution:**
1. Check for `**Command:** create-epic` or `**Command:** create-sprint`
2. Verify required parameters present
3. See mode-detection.md for complete marker list

## Issue 2: Checkpoint Not Detected

**Symptom:** Workflow restarts from beginning instead of resuming

**Cause:** Checkpoint markers not in story file

**Solution:**
1. Check story Status History section for checkpoint entries
2. See checkpoint-detection.md for expected format
3. Manually add checkpoint if needed

## Issue 3: Quality Gate Blocks Progression

**Symptom:** Story cannot advance to next status

**Cause:** Quality gate requirements not met

**Solution:**
1. Check which gate failed (see quality-gates.md)
2. Review gate requirements
3. Fix issues and retry

## Issue 4: QA Retry Loop Exceeds Max Attempts

**Symptom:** QA failed 3 times, workflow halted

**Cause:** Persistent issues not resolved between attempts

**Solution:**
1. Review QA reports from all 3 attempts
2. Address root cause issues
3. See qa-retry-workflow.md for retry logic
4. May need to refactor story or defer items

## Issue 5: Sprint Planning Capacity Exceeded

**Symptom:** Sprint planning warns about over-capacity

**Cause:** Selected stories exceed 20-40 point recommendation

**Solution:**
1. Review story point estimates
2. Remove lower-priority stories
3. See sprint-planning-guide.md for capacity guidelines

## Debugging Tips

1. **Check context markers:** Use Grep to search conversation for markers
2. **Verify file structure:** Ensure story file has all required sections
3. **Review workflow history:** Check story Status History for clues
4. **Read reference files:** Most issues documented in phase-specific references
5. **Test mode detection:** Try explicit markers if auto-detection fails

## Getting Help

If issue persists after troubleshooting:
1. Document current state (status, checkpoints, errors)
2. Review relevant reference file for the failing phase
3. Check quality-gates.md if blocked at gate
4. Use AskUserQuestion to request user guidance
EOF
```

**Validation:**
- [ ] File created: `references/troubleshooting.md`
- [ ] Line count: ~150 lines
- [ ] Top 5 issues documented
- [ ] Solutions provided

---

### Phase 3: Rewrite Entry Point SKILL.md

**Target:** ~195 lines

#### Step 3.1: Create New SKILL.md Structure

```bash
cd .claude/skills/devforgeai-orchestration/

# Create new entry point
cat > SKILL.md.new <<'EOF'
---
name: devforgeai-orchestration
description: Coordinates spec-driven development workflow from Epic → Sprint → Story → Architecture → Development → QA → Release. Manages story lifecycle, enforces quality gates, and orchestrates skill invocation. Use when starting epics/sprints, creating stories, managing workflow progression, or enforcing quality checkpoints.
allowed-tools:
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - AskUserQuestion
  - Skill
  - Task
---

# DevForgeAI Orchestration Skill

Coordinate the complete spec-driven development lifecycle with automated skill orchestration and quality gate enforcement.

## Purpose

This skill is the **workflow coordinator** for the entire spec-driven development framework. It manages the progression of work from high-level business initiatives (Epics) through implementation (Stories) to production release.

### Core Responsibilities

1. **Project Management Integration** - Support Epic → Sprint → Story hierarchy with stories as atomic work units
2. **Skill Coordination** - Auto-invoke architecture, development, QA, and release skills at appropriate workflow stages
3. **State Management** - Track and validate story status across 11 workflow states with sequential progression
4. **Quality Gate Enforcement** - Block transitions when quality standards not met (context validation, test passing, QA approval, release readiness)

### Philosophy

- **Epic → Sprint → Story decomposition** - Break large initiatives into manageable stories
- **Story is atomic unit** - Each story is independently deliverable
- **Quality over speed** - Never skip quality gates
- **No workflow shortcuts** - Every stage must complete successfully
- **Automated orchestration** - Skills invoke each other automatically
- **Transparency** - Complete workflow history in story documents

## When to Use This Skill

**Use this skill when:**
- Starting a new epic or sprint
- Creating stories from requirements
- Managing story workflow progression
- Checking story status
- Enforcing quality gates
- Coordinating multi-story releases

**Entry points:**
```
Skill(command="devforgeai-orchestration")
```

**Context markers:**
- `**Command:** create-epic` + `**Epic name:** {name}` → Epic Creation Mode
- `**Command:** create-sprint` + `**Sprint Name:** {name}` → Sprint Planning Mode
- `**Story ID:** STORY-001` → Story Management Mode (default)

---

## Mode Detection

This skill operates in multiple modes based on conversation context markers. **See `references/mode-detection.md` for complete detection logic.**

**Supported modes:**
1. **Epic Creation Mode** - Phase 4A workflow (7-phase process)
2. **Sprint Planning Mode** - Phase 3 workflow (capacity validation)
3. **Story Management Mode** - Complete story lifecycle orchestration
4. **Default Mode** - Story status checking and validation

---

## Workflow States

Stories progress through **11 sequential states**:

```
Backlog → Architecture → Ready for Dev → In Development → Dev Complete →
QA In Progress → [QA Approved | QA Failed] → Releasing → Released
```

**See `references/workflow-states.md` for complete state definitions and transitions.**

---

## Orchestration Phases

This skill executes workflows in distinct phases. Each phase loads its reference file on-demand for detailed implementation.

### Phase 0: Checkpoint Detection
**Purpose:** Resume interrupted workflows from last successful checkpoint
**Reference:** `checkpoint-detection.md`
**Checkpoints:** DEV_COMPLETE, QA_APPROVED, STAGING_COMPLETE

### Phase 1: Story Validation
**Purpose:** Load and validate story file before execution
**Reference:** `story-validation.md`
**Validates:** File exists, status valid, prerequisites met

### Phase 2: Skill Invocation
**Purpose:** Coordinate automatic invocation of other skills
**Reference:** `skill-invocation.md`
**Skills invoked:** devforgeai-architecture, development, qa, release

### Phase 3: Sprint Planning
**Purpose:** Create sprints with capacity validation
**Reference:** `sprint-planning-guide.md`
**Subagent:** sprint-planner

### Phase 3A: Story Status Update
**Purpose:** Update story status and workflow history
**Reference:** `story-status-update.md`
**Updates:** Status, timestamps, history entries

### Phase 3.5: QA Retry Loop
**Purpose:** Manage QA failure recovery (max 3 attempts)
**Reference:** `qa-retry-workflow.md`
**Logic:** Attempt tracking, deferral handling, loop prevention

### Phase 4A: Epic Creation
**Purpose:** Generate epics from requirements
**Reference:** `epic-management.md` (primary), plus 4 supporting files
**Subagents:** requirements-analyst, architect-reviewer

### Phase 4.5: Deferred Work Tracking
**Purpose:** Track and validate deferred DoD items
**Reference:** `deferred-tracking.md`
**Subagent:** technical-debt-analyzer

### Phase 5: Next Action Determination
**Purpose:** Recommend next steps based on current state
**Reference:** `next-action-determination.md`
**Output:** Recommended actions for user

### Phase 6: Orchestration Finalization
**Purpose:** Generate completion summary and finalize workflow
**Reference:** `orchestration-finalization.md`
**Output:** Timeline, phases executed, quality gates passed

---

## Quality Gate Enforcement

Four gates block workflow progression when requirements not met:

1. **Gate 1: Context Validation** (Architecture → Ready for Dev)
2. **Gate 2: Test Passing** (Dev Complete → QA In Progress)
3. **Gate 3: QA Approval** (QA Approved → Releasing)
4. **Gate 4: Release Readiness** (Releasing → Released)

**See `references/quality-gates.md` for complete gate requirements and enforcement logic.**

---

## Subagent Coordination

This skill delegates specialized tasks to subagents:

- **requirements-analyst** - Epic feature decomposition, requirements spec generation
- **architect-reviewer** - Epic technical assessment, complexity scoring
- **sprint-planner** - Sprint creation, capacity validation, story updates
- **technical-debt-analyzer** - Deferred work analysis, debt trend reporting

**See `references/skill-invocation.md` for subagent coordination patterns.**

---

## Reference Files

Load these on-demand during workflow execution:

### Core Workflow
- **mode-detection.md** - Mode detection logic and markers
- **checkpoint-detection.md** - Checkpoint recovery workflow
- **story-validation.md** - Story file validation
- **skill-invocation.md** - Skill coordination patterns
- **story-status-update.md** - Status update procedures

### Specialized Workflows
- **qa-retry-workflow.md** - QA failure recovery (3-attempt limit)
- **deferred-tracking.md** - Technical debt tracking
- **next-action-determination.md** - Next step recommendations
- **orchestration-finalization.md** - Completion summary generation

### Epic Management (5 files)
- **epic-management.md** - Epic creation phases 1-2
- **feature-decomposition-patterns.md** - Phase 3 patterns
- **technical-assessment-guide.md** - Phase 4 complexity scoring
- **epic-validation-checklist.md** - Phase 7 validation

### Sprint Management
- **sprint-planning-guide.md** - Sprint creation and capacity

### State Management
- **workflow-states.md** - 11 state definitions
- **state-transitions.md** - Valid transitions and rules

### Supporting Files
- **quality-gates.md** - 4 gate requirements
- **story-management.md** - Story lifecycle procedures
- **user-interaction-patterns.md** - AskUserQuestion templates
- **troubleshooting.md** - Common issues and solutions

---

## Common Issues

**Top 5 issues and quick solutions:**

1. **Mode detection fails** → Check context markers (see mode-detection.md)
2. **Checkpoint not detected** → Verify Status History format (see checkpoint-detection.md)
3. **Quality gate blocks** → Review gate requirements (see quality-gates.md)
4. **QA retry exceeds 3** → Address root cause (see qa-retry-workflow.md)
5. **Sprint capacity exceeded** → Remove stories (see sprint-planning-guide.md)

**See `references/troubleshooting.md` for complete troubleshooting guide.**

EOF
```

**Validation:**
- [ ] New file created: `SKILL.md.new`
- [ ] Line count ≤200 lines
- [ ] All phases summarized
- [ ] References to all 20 reference files

#### Step 3.2: Replace Original SKILL.md

```bash
# Final validation before replacement
wc -l SKILL.md.new
# Must be ≤200 lines

# If valid, replace
mv SKILL.md.new SKILL.md
```

**Validation:**
- [ ] SKILL.md replaced
- [ ] Line count ≤200
- [ ] Backup still exists (SKILL.md.backup-2025-01-06)

---

### Phase 4: Clean Up Reference Files

#### Step 4.1: Delete Duplicate Sprint Planning File

```bash
cd references/
rm sprint-planning.md
# Keep sprint-planning-guide.md
```

**Validation:**
- [ ] `sprint-planning.md` deleted
- [ ] `sprint-planning-guide.md` remains (631 lines)

#### Step 4.2: Delete Old Backup Files

```bash
cd references/
rm story-management.md.backup-pre-refactor
```

**Validation:**
- [ ] Old backup deleted

#### Step 4.3: Verify Reference File Count

```bash
cd references/
ls -1 *.md | wc -l
# Should be 20 files
```

**Expected files (20 total):**
1. checkpoint-detection.md (NEW)
2. deferred-tracking.md (NEW)
3. epic-management.md (existing)
4. epic-validation-checklist.md (existing)
5. feature-decomposition-patterns.md (existing)
6. mode-detection.md (NEW)
7. next-action-determination.md (NEW)
8. orchestration-finalization.md (NEW)
9. qa-retry-workflow.md (NEW)
10. quality-gates.md (existing)
11. skill-invocation.md (NEW)
12. sprint-planning-guide.md (existing)
13. state-transitions.md (existing)
14. story-management.md (existing)
15. story-status-update.md (NEW)
16. story-validation.md (NEW)
17. technical-assessment-guide.md (existing)
18. troubleshooting.md (NEW)
19. user-interaction-patterns.md (NEW)
20. workflow-states.md (existing)

**Validation:**
- [ ] 20 reference files exist
- [ ] No duplicate files
- [ ] All new files created

---

### Phase 5: Testing

#### Step 5.1: Cold Start Test

**Test:** SKILL.md loads <200 lines on first activation

```bash
# Check line count
wc -l .claude/skills/devforgeai-orchestration/SKILL.md

# Must be ≤200 lines
```

**Validation:**
- [ ] SKILL.md ≤200 lines
- [ ] Target: <100ms activation time (manual observation)

#### Step 5.2: Mode Detection Test

**Test:** Each mode correctly loads appropriate references

**Test Case 1: Epic Creation Mode**
```
Context markers:
**Command:** create-epic
**Epic name:** Test Epic

Expected:
1. Mode detected: Epic Creation
2. Reference loaded: epic-management.md
3. Subagent invoked: requirements-analyst
```

**Validation:**
- [ ] Epic mode detected
- [ ] Correct references loaded
- [ ] Subagents invoked

**Test Case 2: Sprint Planning Mode**
```
Context markers:
**Command:** create-sprint
**Sprint Name:** Test Sprint
**Selected Stories:** STORY-001, STORY-002

Expected:
1. Mode detected: Sprint Planning
2. Reference loaded: sprint-planning-guide.md
3. Subagent invoked: sprint-planner
```

**Validation:**
- [ ] Sprint mode detected
- [ ] Correct references loaded
- [ ] Subagent invoked

**Test Case 3: Story Management Mode**
```
Context markers:
**Story ID:** STORY-001

Expected:
1. Mode detected: Story Management
2. Reference loaded: story-validation.md (Phase 1)
3. Checkpoint detection executed
```

**Validation:**
- [ ] Story mode detected
- [ ] Correct references loaded
- [ ] Checkpoint detection executed

#### Step 5.3: Progressive Loading Test

**Test:** References load on-demand, not all at once

```bash
# During execution, monitor which references are loaded
# Expected: Only relevant phase references loaded, not all 20
```

**Validation:**
- [ ] Only needed references loaded
- [ ] Not all 20 references loaded simultaneously

#### Step 5.4: Integration Test (Full Workflow)

**Test:** Complete orchestration workflow from story creation to release

```
Full workflow test:
1. Create epic
2. Create sprint
3. Create story
4. Progress through all 11 states
5. Validate quality gates
6. Complete workflow

Expected:
- All phases execute correctly
- Quality gates enforced
- Workflow history updated
- References loaded as needed
```

**Validation:**
- [ ] Epic created
- [ ] Sprint created
- [ ] Story progressed through all states
- [ ] Quality gates enforced
- [ ] Workflow complete

#### Step 5.5: Regression Test

**Test:** Behavior unchanged from original

**Comparison:**
- Original: 3,249-line SKILL.md
- Refactored: ~200-line SKILL.md + 20 references

**Validation:**
- [ ] Same functionality preserved
- [ ] No workflow steps missing
- [ ] Quality gates still enforced
- [ ] Subagents still invoked correctly

#### Step 5.6: Token Measurement

**Test:** Measure actual token usage

```bash
# Original activation
# Estimated: ~26,000 tokens

# Refactored activation
# Target: ~1,600 tokens
# Efficiency gain: 16x
```

**Validation:**
- [ ] Token usage measured
- [ ] ≥10x improvement achieved
- [ ] Target ~1,600 tokens on activation

---

### Phase 6: Documentation and Completion

#### Step 6.1: Update This Document

**Mark completion:**
- [ ] Status: COMPLETE
- [ ] Final line count: [actual]
- [ ] Token reduction: [actual %]
- [ ] Completion date: [date]

#### Step 6.2: Commit Changes

```bash
cd /mnt/c/Projects/DevForgeAI2

# Stage changes
git add .claude/skills/devforgeai-orchestration/SKILL.md
git add .claude/skills/devforgeai-orchestration/references/

# Commit
git commit -m "refactor(orchestration): Progressive disclosure - 3249→200 lines

- Reduced SKILL.md from 3,249 to ~200 lines (94% reduction)
- Created 11 new reference files for progressive loading
- Deleted duplicate sprint-planning.md
- Organized 20 reference files by workflow phase
- Token efficiency: 16x improvement (26K→1.6K on activation)
- All functionality preserved, behavior unchanged

Addresses: Reddit article cold start optimization
Pattern: Progressive disclosure per Anthropic architecture
Testing: All modes validated, integration tests pass"
```

**Validation:**
- [ ] Changes staged
- [ ] Commit message complete
- [ ] Committed to git

#### Step 6.3: Update Framework Memory Files

**Files to update (AFTER parallel refactoring completes):**

```bash
# Update skills reference with new structure
# .claude/memory/skills-reference.md

# Update this analysis document with results
# .ai_docs/analysis/devforgeai-orchestration.md
```

**⚠️ IMPORTANT:** Use AskUserQuestion before updating these shared files to ensure no other sessions are modifying them.

**Validation:**
- [ ] User confirmed no other sessions active
- [ ] Shared files updated
- [ ] Changes committed

---

## Completion Criteria

**All must be TRUE before marking COMPLETE:**

- [ ] SKILL.md ≤200 lines
- [ ] All 11 new reference files created
- [ ] Duplicate files deleted
- [ ] 20 reference files total
- [ ] Cold start test passes (<200 lines loaded)
- [ ] Mode detection tests pass (all 3 modes)
- [ ] Progressive loading validated
- [ ] Integration test passes (full workflow)
- [ ] Regression test passes (behavior unchanged)
- [ ] Token efficiency ≥10x improvement
- [ ] Changes committed to git
- [ ] This document updated with results

---

## Session Handoff Notes

**For next Claude session picking up this work:**

### Quick Start

1. **Read this document completely** - Full context is here
2. **Check status at top** - If IN PROGRESS, see what's done
3. **Review Phase X in Refactoring Steps** - Resume from unchecked items
4. **Create backup first** - Always preserve original
5. **Test incrementally** - Validate after each extraction
6. **Update this document** - Check off completed items
7. **Commit frequently** - After each major phase

### Critical Reminders

- **Order matters:** Extract in sequence (Phase 2.1 → 2.11) to avoid reference issues
- **Test as you go:** Don't wait until end to test
- **Keep backups:** Don't delete SKILL.md.backup-2025-01-06
- **Progressive loading:** References load on-demand, not all at once
- **Token efficiency:** Goal is 16x improvement, measure before/after
- **Shared files:** Use AskUserQuestion before updating .claude/memory/*.md

### Common Pitfalls

1. **Don't delete content prematurely** - Extract to reference first, then remove from SKILL.md
2. **Preserve all functionality** - This is refactoring, not feature removal
3. **Watch line counts** - Each reference should be 40-500 lines, not thousands
4. **Test mode detection** - Critical that all 4 modes still work
5. **Validate references** - Each should be self-contained and complete

### If Stuck

1. **Read original SKILL.md.backup-2025-01-06** - See what was there originally
2. **Check existing references** - See pattern in epic-management.md, quality-gates.md
3. **Review Reddit article** - Reminder of 200-line rule and progressive disclosure
4. **Measure tokens** - If approaching limit, extract more aggressively

### Success Indicators

- ✅ SKILL.md opens quickly (feels responsive)
- ✅ References load only when needed (not all 20 at once)
- ✅ Workflow tests pass (epic, sprint, story all work)
- ✅ Token usage ~1,600 on activation (down from ~26,000)

---

## Results (Post-Completion)

**To be filled in after refactoring completes:**

### Metrics Achieved

- **Final SKILL.md lines:** [X] (Target: ≤200)
- **Reference files created:** [N] (Target: 11 new + 9 existing = 20 total)
- **Token reduction:** [Y]% (Target: ≥90%)
- **Activation time:** [Z]ms (Target: <100ms)
- **Efficiency gain:** [R]x (Target: ≥10x)

### Files Modified

- `.claude/skills/devforgeai-orchestration/SKILL.md` (3,249 → [X] lines)
- `.claude/skills/devforgeai-orchestration/references/` (10 → 20 files)
  - Created: [list 11 new files]
  - Deleted: sprint-planning.md, story-management.md.backup-pre-refactor

### Lessons Learned

[Notes for future skill refactorings]

### Unexpected Issues

[Any problems encountered and solutions]

### Recommendations for Next Skills

[What worked well, what to improve]

---

## Appendix: Line Count Breakdown

**Original SKILL.md (3,249 lines):**

| Section | Lines | % | Extraction Target |
|---------|-------|---|-------------------|
| Frontmatter | 13 | 0.4% | Keep |
| Purpose | 44 | 1.4% | Keep |
| Mode Detection | 85 | 2.6% | → mode-detection.md |
| States Overview | 15 | 0.5% | Keep summary |
| Phase 0 | 168 | 5.2% | → checkpoint-detection.md |
| Phase 1 | 44 | 1.4% | → story-validation.md |
| Phase 2 | 77 | 2.4% | → skill-invocation.md |
| Phase 3 | 288 | 8.9% | → sprint-planning-guide.md (exists) |
| Phase 3A | 33 | 1.0% | → story-status-update.md |
| Phase 3.5 | 459 | 14.1% | → qa-retry-workflow.md |
| Phase 3.5 Templates | 42 | 1.3% | → qa-retry-workflow.md |
| Phase 4A Epic | 1,379 | 42.4% | → epic-*.md (5 files exist) |
| Phase 4.5 | 134 | 4.1% | → deferred-tracking.md |
| Phase 5 | 19 | 0.6% | → next-action-determination.md |
| Phase 6 | 174 | 5.4% | → orchestration-finalization.md |
| Quality Gates | 29 | 0.9% | Keep summary |
| User Interaction | 233 | 7.2% | → user-interaction-patterns.md |
| **TOTAL** | **3,249** | **100%** | **20 references** |

**Target SKILL.md (~200 lines):**

| Section | Lines | % |
|---------|-------|---|
| Frontmatter | 13 | 6.5% |
| Purpose | 35 | 17.5% |
| When to Use | 20 | 10% |
| Mode Detection | 20 | 10% |
| States Overview | 15 | 7.5% |
| Phases Summary | 40 | 20% |
| Quality Gates | 20 | 10% |
| Subagents | 15 | 7.5% |
| Reference Map | 20 | 10% |
| Common Issues | 10 | 5% |
| **TOTAL** | **~195** | **~100%** |

---

**Document Version:** 1.0
**Created:** 2025-01-06
**Last Updated:** 2025-01-06 (Initial creation)
**Next Review:** After refactoring completion
