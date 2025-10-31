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
Skill(command="devforgeai-orchestration --create-epic --title='User Management'")
Skill(command="devforgeai-orchestration --plan-sprint --epic=EPIC-001")
Skill(command="devforgeai-orchestration --create-story --sprint=SPRINT-001")
Skill(command="devforgeai-orchestration --story=STORY-001")
Skill(command="devforgeai-orchestration --status=STORY-001")
```

---

## Workflow States

### 11 Story States (Brief Overview)

```
1. Backlog → 2. Architecture → 3. Ready for Dev → 4. In Development →
5. Dev Complete → 6. QA In Progress → 7. QA Failed/QA Approved →
8. Releasing → 9. Released
(11. Blocked - can occur from any state)
```

**For detailed state definitions:** See `references/workflow-states.md`
**For transition rules and validation:** See `references/state-transitions.md`

---

## Orchestration Workflow

### Phase 1: Load and Validate Story

#### Step 1: Load Story Document
```
Read(file_path=".ai_docs/Stories/{story_id}.story.md")

Extract YAML frontmatter:
  - id, title, epic, sprint
  - status (current state)
  - points, priority
  - assigned_to, created

Extract content sections:
  - Acceptance criteria
  - Technical specification
  - NFRs
  - Dependencies
  - Workflow status
```

#### Step 2: Validate Current State
```
Check status is valid workflow state
Verify prerequisites for requested transition

For validation rules: See references/state-transitions.md
```

#### Step 3: Validate Quality Gates
```
Check gate requirements for current → next transition

Gate 1: Context Validation (Architecture → Ready for Dev)
Gate 2: Test Passing (Dev Complete → QA In Progress)
Gate 3: QA Approval (QA Approved → Releasing)
Gate 4: Release Readiness (Releasing → Released)

For gate requirements: See references/quality-gates.md

HALT if gate requirements not met
```

---

### Phase 2: Orchestrate Skill Invocation

#### Architecture Phase (Backlog → Ready for Dev)
```
Check for context files (.devforgeai/context/*.md)

IF missing:
    Invoke: Skill(command="devforgeai-architecture")
    Wait for completion
    Validate all 6 context files created
    Update story status: Architecture → Ready for Dev

For context validation gate details: See references/quality-gates.md
```

#### Development Phase (Ready for Dev → Dev Complete)
```
Invoke: Skill(command="devforgeai-development --story={story_id}")

Development skill executes TDD workflow:
  - Phase 1: Context Validation
  - Phase 2: Test-First (Red)
  - Phase 3: Implementation (Green) + light QA
  - Phase 4: Refactor + light QA
  - Phase 5: Integration + light QA
  - Phase 6: Git workflow

Update story status: In Development → Dev Complete
Check workflow box: "Development phase complete"

For test passing gate details: See references/quality-gates.md
```

#### QA Phase (Dev Complete → QA Approved/Failed)
```
Invoke: Skill(command="devforgeai-qa --mode=deep --story={story_id}")

QA skill executes 5 phases:
  - Phase 1: Test Coverage Analysis
  - Phase 2: Anti-Pattern Detection
  - Phase 3: Spec Compliance Validation
  - Phase 4: Code Quality Metrics
  - Phase 5: Generate QA Report

Parse QA report:
Read(file_path=".devforgeai/qa/reports/{story_id}-qa-report.md")

IF qa_status == "PASS":
    Update status: QA In Progress → QA Approved
    Check workflow box: "QA phase complete"
    Append QA report section to story
ELSE:
    Update status: QA In Progress → QA Failed
    Extract action items
    Return to In Development

For QA approval gate details: See references/quality-gates.md
```

#### Release Phase (QA Approved → Released)
```
Invoke: Skill(command="devforgeai-release --story={story_id}")

Release skill executes deployment

IF successful:
    Update status: Releasing → Released
    Check workflow box: "Released"
    Append release info
    Update sprint progress
    Update epic progress

For release readiness gate details: See references/quality-gates.md
```

---

### Phase 3: Update Story Status

#### Update Frontmatter
```
Edit(file_path=".ai_docs/Stories/{story_id}.story.md",
     old_string="status: {old_status}",
     new_string="status: {new_status}")
```

#### Update Workflow Checkboxes
```
Mark phase as complete: - [ ] → - [x]

Checkboxes:
- Architecture phase complete
- Development phase complete
- QA phase complete
- Released
```

#### Append Workflow History
```
Add entry (format):
### {timestamp} - {new_status}
- **Previous Status:** {old_status}
- **Action Taken:** {description}
- **Result:** {summary}
- **Next Steps:** {next_steps}

For workflow history format and examples: See references/story-management.md
```

---

### Phase 4: Epic and Sprint Management

#### Epic Creation
```
Load requirements from ideation phase
Create epic document with YAML frontmatter
Decompose into features
Estimate epic effort

For epic planning procedures: See references/epic-management.md

Template: assets/templates/epic-template.md
```

#### Sprint Planning
```
Calculate team capacity
Select stories from backlog
Create sprint document
Track sprint progress

For sprint planning procedures: See references/sprint-planning.md

Template: assets/templates/sprint-template.md
```

#### Story Creation
```
Create story document with:
- YAML frontmatter (id, title, epic, sprint, status, points, priority)
- User story format: "As a [role], I want [feature], so that [benefit]"
- Acceptance criteria (Given/When/Then)
- Technical specification
- Non-functional requirements

For story document structure and procedures: See references/story-management.md

Template: assets/templates/story-template.md
```

---

### Phase 5: Determine Next Action

Based on current state, determine next orchestration action:

```
Backlog → Architecture: Invoke devforgeai-architecture
Architecture → Ready for Dev: Context files created, ready for developer
Ready for Dev → In Development: Developer starts work
In Development → Dev Complete: TDD workflow complete
Dev Complete → QA In Progress: Invoke devforgeai-qa
QA Approved → Releasing: Invoke devforgeai-release when ready
Releasing → Released: Deployment complete
QA Failed → In Development: Developer fixes violations
Blocked → Previous State: When blocker resolved
```

**For complete decision tree:** See `references/state-transitions.md`

---

## Quality Gate Enforcement

### Four Gates Block Workflow Progression

1. **Context Validation Gate** (Architecture → Ready for Dev)
   - All 6 context files exist and valid
   - No placeholder content
   - Tech stack locked

2. **Test Passing Gate** (Dev Complete → QA In Progress)
   - Build succeeds
   - All tests pass (100% pass rate)
   - Light validation clean

3. **QA Approval Gate** (QA Approved → Releasing)
   - Deep validation PASSED
   - Coverage meets thresholds (95%/85%/80%)
   - Zero CRITICAL violations
   - Zero HIGH violations (or approved exceptions)

4. **Release Readiness Gate** (Releasing → Released)
   - Deployment successful
   - Health checks pass
   - All workflow checkboxes complete

**For detailed gate requirements and enforcement:** See `references/quality-gates.md`

---

## AskUserQuestion Patterns

### Pattern 1: Story Priority Conflict
```
Sprint capacity: 20 points
Stories ready: 3 (totaling 25 points)

AskUserQuestion:
  Question: "Sprint has 3 stories (25 points) but capacity for 20 points. Which stories to include?"
  Header: "Sprint capacity"
  Options:
    - STORY-001: User registration (5 points, High priority)
    - STORY-002: Order history (8 points, Medium priority)
    - STORY-003: Admin dashboard (12 points, Low priority)
  multiSelect: true
```

### Pattern 2: Blocked Story Resolution
```
Story blocked on external dependency (email service API not ready)

AskUserQuestion:
  Question: "STORY-001 blocked waiting for email API (ETA: 7 days, beyond sprint). How to proceed?"
  Header: "Story blocker"
  Options:
    - "Wait for dependency (keep blocked)"
    - "Create mock/stub to unblock"
    - "De-prioritize, start different story"
    - "Escalate to tech lead"
  multiSelect: false
```

### Pattern 3: QA Threshold Exception Request
```
Infrastructure coverage: 68% (threshold: 80%)
Uncovered code: Logging utilities (non-critical)
Business logic: 97% (exceeds 95%)

AskUserQuestion:
  Question: "Infrastructure coverage 68% < 80%. Uncovered: non-critical utilities. Business logic: 97%. Accept exception?"
  Header: "Coverage exception"
  Options:
    - "Fail QA - Require tests for all infrastructure"
    - "Pass with waiver - Document reason"
    - "Require public API tests only - Skip internals"
  multiSelect: false
```

---

## Integration with Other Skills

### devforgeai-architecture
**When:** Architecture → Ready for Dev transition
**Invocation:** `Skill(command="devforgeai-architecture")`
**Process:** Creates/validates all 6 context files, creates ADRs
**Result:** Update story status, check workflow box

### devforgeai-development
**When:** In Development workflow execution
**Invocation:** `Skill(command="devforgeai-development --story={story_id}")`
**Process:** Executes TDD workflow (6 phases), light QA automatic
**Result:** Update story status when Phase 6 complete

### devforgeai-qa
**When 1 (Light):** During development (Phases 3, 4, 5) - automatic
**When 2 (Deep):** After Dev Complete
**Invocation:** `Skill(command="devforgeai-qa --mode=deep --story={story_id}")`
**Process:** 5 comprehensive validation phases, generates QA report
**Result:** Update status to QA Approved or QA Failed

### devforgeai-release
**When:** QA Approved → Releasing transition
**Invocation:** `Skill(command="devforgeai-release --story={story_id}")`
**Process:** Deployment to production, health checks
**Result:** Update status to Released, update progress

---

## Tool Usage Protocol

### Use Native Tools for File Operations

✅ **CORRECT:**
```
Read(file_path="story.md")
Edit(file_path="story.md", old_string="old", new_string="new")
Glob(pattern="**/*.story.md")
Grep(pattern="epic: EPIC-001", glob="**/*.md")
```

❌ **FORBIDDEN:**
```
Bash(command="cat story.md")
Bash(command="sed -i 's/old/new/' story.md")
Bash(command="find . -name '*.story.md'")
Bash(command="grep 'epic: EPIC-001' **/*.md")
```

**Use Bash ONLY for:**
- Git operations: `git status`, `git commit`, `git push`
- Test execution: `pytest`, `npm test`, `dotnet test`
- Build commands: `npm run build`, `dotnet build`

---

## Reference Materials

Load these on demand during orchestration:

### State Management
- **`./references/workflow-states.md`** - Detailed 11-state definitions (585 lines)
- **`./references/state-transitions.md`** - Transition rules, validations, decision trees (1,105 lines)
- **`./references/quality-gates.md`** - Gate requirements and enforcement procedures (987 lines)

### Project Management
- **`./references/epic-management.md`** - Epic planning, decomposition, estimation (496 lines)
- **`./references/sprint-planning.md`** - Sprint capacity, story selection, tracking (620 lines)

### Story Operations
- **`./references/story-management.md`** - Story structure, status updates, workflow history (691 lines)

### Templates (Assets)
- **`./assets/templates/epic-template.md`** - Epic document structure (265 lines)
- **`./assets/templates/sprint-template.md`** - Sprint planning template (366 lines)
- **`./assets/templates/story-template.md`** - Story specification format (610 lines)

---

## Success Criteria

### Orchestration Success

**Story Lifecycle:**
- [x] Story progresses through all required workflow stages
- [x] No stages skipped (strict enforcement)
- [x] Quality gates enforced at each transition
- [x] Story status always accurate and up-to-date

**Skill Coordination:**
- [x] Skills invoked in correct sequence
- [x] Architecture skill creates context before development
- [x] Development skill executes TDD workflow
- [x] QA skill validates before release approval
- [x] Skills communicate state back to orchestration

**State Management:**
- [x] Story state transitions follow defined rules
- [x] Invalid transitions blocked
- [x] Workflow history maintained for audit trail
- [x] All checkboxes completed before release

**Quality Enforcement:**
- [x] Context validation gate enforced
- [x] Test passing gate enforced
- [x] QA approval gate enforced
- [x] Release readiness gate enforced

**Documentation:**
- [x] Story documents always current
- [x] Workflow history appended at each transition
- [x] QA reports linked from stories
- [x] Action items documented when QA fails

**Overall Success:**
- [x] Stories progress from Backlog to Released without manual intervention (when no blockers)
- [x] Quality standards maintained throughout workflow
- [x] Developer experience smooth (minimal friction)
- [x] Transparency into workflow status
- [x] Audit trail for compliance/review

---

**The orchestration skill ensures every story follows the same high-quality workflow: Architecture → Development → QA → Release, with no shortcuts and complete transparency.**
