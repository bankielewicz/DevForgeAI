# DevForgeAI Slash Commands Reference

Complete guide to the 11 slash commands for DevForgeAI workflows.

---

## Command Overview

DevForgeAI provides 11 slash commands organized into 5 categories:

**Planning & Setup (4 commands):**
- `/ideate` - Transform business idea to structured requirements
- `/create-context` - Generate 6 architectural context files
- `/create-epic` - Generate epic from requirements
- `/create-sprint` - Plan 2-week sprint with story selection

**Story Development (3 commands):**
- `/create-story` - Generate story with acceptance criteria
- `/create-ui` - Generate UI component specs (web/GUI/terminal)
- `/dev` - Execute TDD development cycle (Red→Green→Refactor)

**Validation & Release (2 commands):**
- `/qa` - Run quality validation (light/deep modes)
- `/release` - Deploy to staging and production

**Orchestration (1 command):**
- `/orchestrate` - Full lifecycle: Dev → QA → Release

**Framework Maintenance (2 commands):**
- `/audit-deferrals` - Audit deferred work in stories for circular chains and invalid references
- `/audit-budget` - Audit command character budgets against lean orchestration protocol

---

## Command Details

### /ideate [business-idea]

**Purpose:** Transform business idea into structured requirements

**Invokes:** `devforgeai-ideation` skill

**Workflow:**
1. Argument validation (capture business idea)
2. Invoke devforgeai-ideation skill (6-phase discovery)
3. Verify artifacts created
4. Brief completion confirmation
5. Next steps guidance

**The skill handles all implementation:**
- **Phase 1-2:** Discovery & Requirements Elicitation (10-60 questions)
- **Phase 3-5:** Complexity Assessment, Epic Decomposition, Feasibility Analysis
- **Phase 6:** Documentation, Self-Validation, Summary, Next Action

**Example:**
```
> /ideate Build a task management system with AI prioritization
```

**Output:**
- Epic document(s) in `.ai_docs/Epics/`
- Requirements spec in `.devforgeai/specs/requirements/`
- Complexity assessment (0-60 score, architecture tier)
- Technology recommendations by tier

**Architecture (Post-Refactoring 2025-11-05):**

**Command (410 lines - Lean Orchestration):**
- Argument parsing and validation
- Skill invocation with context markers
- Basic artifact verification
- Brief completion confirmation
- Next steps guidance (defers to skill)

**Skill (devforgeai-ideation - Comprehensive Discovery):**
- Phase 1-5: Complete 6-phase discovery workflow
- Phase 6.1-6.3: Artifact generation and architecture transition
- Phase 6.4: Self-Validation (NEW - validates all artifacts)
- Phase 6.5: Present Completion Summary (NEW - uses output-templates.md)
- Phase 6.6: Determine Next Action (NEW - greenfield/brownfield awareness)
- Error Handling & Recovery (NEW - comprehensive error recovery)

**Reference Files (NEW):**
- validation-checklists.md (569 lines) - Phase 6.4 validation logic
- output-templates.md (619 lines) - Summary templates, tech recommendations by tier

**Token Efficiency:**
- Command: ~2,929 tokens (down from ~3,837)
- Skill: ~100,000 tokens (isolated context)
- References: Loaded progressively (Phase 6.4, 6.5 only)
- **Savings: 24% reduction in main conversation tokens**
- **Character budget: 11,717 chars (78% of 15K limit) - WITHIN BUDGET**

---

### /create-context [project-name]

**Purpose:** Generate 6 architectural context files

**Invokes:** `devforgeai-architecture` skill

**Workflow:**
1. Interactive technology selection (via AskUserQuestion)
2. Generate all 6 context files
3. Create initial ADR
4. Validate context completeness

**Example:**
```
> /create-context my-saas-platform
```

**Output:**
- `tech-stack.md` - Technology choices
- `source-tree.md` - Project structure
- `dependencies.md` - Approved packages
- `coding-standards.md` - Code patterns
- `architecture-constraints.md` - Layer boundaries
- `anti-patterns.md` - Forbidden patterns

---

### /create-epic [epic-name]

**Purpose:** Create epic with feature breakdown

**Invokes:** `devforgeai-orchestration` skill (epic creation mode)

**Workflow:**
1. Argument validation (epic name format)
2. Set context markers (epic name, command mode)
3. Invoke orchestration skill
4. Display results from skill

**The skill handles all implementation:**
- **Phase 1-2:** Epic Discovery & Context Gathering (ID generation, goal, timeline, stakeholders, success criteria)
- **Phase 3-4:** Feature Decomposition & Technical Assessment (requirements-analyst, architect-reviewer subagents)
- **Phase 5-6:** Epic File Creation & Optional Requirements Spec
- **Phase 7-8:** Validation (self-healing) & Completion Summary

**Example:**
```
> /create-epic User Authentication System
```

**Output:**
- Epic file in `.ai_docs/Epics/{EPIC-ID}.epic.md`
- Feature list with descriptions (3-8 features)
- Technical assessment (complexity, risks, prerequisites)
- Optional requirements specification

**Architecture (Post-Refactoring 2025-11-06):**

**Command (392 lines - Lean Orchestration):**
- Argument parsing and validation
- Context markers for skill
- Skill invocation
- Results display

**Skill (devforgeai-orchestration - Epic Creation Mode):**
- Phase 1-8: Complete epic creation workflow
- Progressive reference loading (5 files, 3,311 lines)
- Subagent delegation (requirements-analyst, architect-reviewer)
- Framework validation (context files if exist)
- Self-validation and self-healing

**Token Efficiency:**
- Command: ~2,000 tokens (down from ~10,000)
- Skill: ~125,000 tokens (isolated context)
- **Savings: 80% reduction in main conversation tokens**
- **Character budget: 11,270 chars (75% of limit - down from 95%)**

---

### /create-sprint [sprint-name]

**Purpose:** Plan 2-week sprint with interactive story selection and capacity validation

**Invokes:** `devforgeai-orchestration` skill (Phase 3: Sprint Planning Workflow)

**Workflow:**
1. Epic selection (AskUserQuestion)
2. Story selection from Backlog (AskUserQuestion)
3. Sprint metadata collection (dates, duration)
4. Capacity validation (20-40 points recommended)
5. Invoke orchestration skill → sprint-planner subagent
6. Display results

**Architecture (Post-Refactoring 2025-11-05):**

**Command (250 lines - Lean Orchestration):**
- Phase 0: User interaction (epic, stories, metadata via AskUserQuestion)
- Phase 3: Skill invocation with context markers
- Phase 4: Result display

**Skill (devforgeai-orchestration - Phase 3):**
- Step 1: Extract sprint parameters from conversation
- Step 2: Invoke sprint-planner subagent
- Step 3: Process subagent result
- Step 4: Return formatted summary

**Subagent (sprint-planner - NEW):**
- Phase 1: Sprint discovery (calculate next sprint number)
- Phase 2: Story validation (verify Backlog status)
- Phase 3: Metrics calculation (capacity, dates)
- Phase 4: Document generation (YAML + markdown)
- Phase 5: Story updates (status, references, history)
- Phase 6: Summary report (structured JSON)

**Token Efficiency:**
- Command: ~5K tokens
- Skill: ~40K tokens (isolated)
- Subagent: ~35K tokens (isolated)
- **Savings: 58% reduction in main conversation tokens**
- **Character budget: 8K (53% of limit) - COMPLIANT**

**Example:**
```
> /create-sprint "User Authentication Sprint"
> /create-sprint
```

**Output:**
- Sprint file in `.ai_docs/Sprints/Sprint-{N}.md`
- Stories updated to "Ready for Dev" status
- Sprint references added to story files
- Workflow history entries

---

### /create-story [story-description]

**Purpose:** Generate user story with acceptance criteria, technical specifications, and UI specifications

**Invokes:** `devforgeai-story-creation` skill

**Workflow:**
1. Argument validation (capture feature description)
2. Invoke devforgeai-story-creation skill (8-phase workflow)
3. Verify story file created
4. Brief confirmation
5. Next steps guidance

**The skill handles all implementation:**
- **Phase 1-2:** Story Discovery & Requirements Analysis (epic/sprint, metadata, requirements-analyst subagent)
- **Phase 3-4:** Technical & UI Specification (api-designer subagent, data models, components, mockups)
- **Phase 5-6:** Story File Creation & Epic/Sprint Linking
- **Phase 7:** Self-Validation (quality checks, self-healing)
- **Phase 8:** Completion Report (summary, next actions)

**Example:**
```
> /create-story User login with email and password
> /create-story Admin dashboard with analytics and charts
> /create-story Shopping cart checkout with payment processing
```

**Output:**
- Story file in `.ai_docs/Stories/{STORY-ID}-{slug}.story.md`
- YAML frontmatter with metadata
- User story (As a/I want/So that format)
- 3+ testable acceptance criteria (Given/When/Then)
- Technical specification (API contracts, data models, business rules, dependencies)
- UI specification (components, mockups, interfaces, accessibility - if applicable)
- Non-functional requirements (measurable performance, security, scalability)
- Edge cases and error handling
- Definition of Done with checkboxes

**Architecture (Post-Refactoring 2025-11-05):**

**Command (500 lines - Lean Orchestration):**
- Argument parsing and validation (feature description)
- Skill invocation with context markers
- Basic story file verification
- Brief completion confirmation
- Next steps guidance with prerequisites

**Skill (devforgeai-story-creation - Complete Story Generation):**
- Phase 1: Story Discovery (ID generation, epic/sprint context, metadata via AskUserQuestion)
- Phase 2: Requirements Analysis (requirements-analyst subagent, AC generation, validation)
- Phase 3: Technical Specification (api-designer subagent, data models, business rules, dependencies)
- Phase 4: UI Specification (component detection, mockups, interfaces, accessibility - WCAG AA)
- Phase 5: Story File Creation (YAML frontmatter, all markdown sections, template-based)
- Phase 6: Epic/Sprint Linking (update parent documents)
- Phase 7: Self-Validation (comprehensive quality checks, self-healing, validation-checklists.md)
- Phase 8: Completion Report (summary, next action AskUserQuestion)
- Error Handling: ID conflicts, subagent failures, validation failures, file write issues

**Reference Files (NEW - 6 files, 7,477 lines):**
- story-structure-guide.md (662 lines) - YAML frontmatter, sections, formatting
- acceptance-criteria-patterns.md (1,259 lines) - Given/When/Then patterns by domain
- technical-specification-guide.md (1,269 lines) - API contracts, data models, business rules
- ui-specification-guide.md (1,344 lines) - ASCII mockups, components, accessibility (WCAG AA)
- validation-checklists.md (1,038 lines) - Quality validation, self-healing procedures
- story-examples.md (1,905 lines) - 4 complete story examples (CRUD, auth, workflow, reporting)

**Asset Files:**
- story-template.md (609 lines) - Base template for story construction

**Token Efficiency:**
- Command: ~3,548 tokens (down from ~5,752)
- Skill: ~90,000 tokens (isolated context)
- References: ~56,000 tokens total (loaded progressively per phase, isolated context)
- **Savings: 38% reduction in main conversation tokens**
- **Character budget: 14,193 chars (95% of 15K limit) - WITHIN BUDGET** (was 153% - **CRITICAL FIX**)

**Subagents Used:**
- requirements-analyst (Phase 2) - User story and acceptance criteria generation
- api-designer (Phase 3, conditional) - API contract design if endpoints detected

**Framework Integration:**
- Invoked by: `/create-story` command, orchestration skill, development skill (deferrals)
- Invokes: requirements-analyst, api-designer subagents
- References: Context files (tech-stack, coding-standards, architecture-constraints)
- Outputs to: Development skill (/dev uses story AC for TDD), QA skill (validates against story)

**Reusability:** Used by 4+ framework components (command, orchestration, development, sprint planning)

---

### /create-ui [STORY-ID or component-description]

**Purpose:** Generate UI component specs (web/GUI/terminal)

**Invokes:** `devforgeai-ui-generator` skill

**Workflow:**
1. Argument validation and mode detection (story vs standalone)
2. Invoke devforgeai-ui-generator skill (7-phase workflow)
3. Display results (from ui-spec-formatter subagent)
4. Verify critical outputs

**The skill handles all implementation:**
- **Phase 1-5:** Context validation, story analysis, interactive discovery, template loading, code generation
- **Phase 6:** Documentation, story update, **invoke ui-spec-formatter subagent**
- **Phase 7** (NEW): Specification validation (completeness, placeholders, framework compliance) - **user resolves all issues**

**Example:**
```
> /create-ui STORY-042                          # Story mode
> /create-ui "Login form with validation"       # Standalone mode
```

**Output:**
- UI component code in `.devforgeai/specs/ui/`
- UI-SPEC-SUMMARY.md
- Story updated with UI references (if story mode)

**Architecture (Post-Refactoring 2025-11-05 - PLANNED):**

**Command (614 lines - FUTURE: ~300 lines after refactoring):**
- Argument parsing and validation (25 lines)
- Story file loading via @file reference (if story mode)
- Context markers for skill
- Skill invocation (15 lines)
- Result display (10 lines) - outputs subagent-generated template

**Skill (devforgeai-ui-generator - Enhanced with Phase 7):**
- Phase 1-6: All generation phases (unchanged)
- Phase 6 Step 3.5: Invoke ui-spec-formatter subagent (NEW - 2025-11-05)
  - ui-spec-formatter validates and formats results
  - Returns structured JSON with display template
  - Skill returns result to command
- Phase 7: Specification Validation (NEW - 2025-11-05)
  - Step 7.1: Completeness check (10 required sections)
  - Step 7.2: Placeholder detection (Grep for TODO/TBD)
  - Step 7.3: Framework validation (all 6 context files)
  - Step 7.4: **User resolution of ALL issues** (no self-healing)
  - Step 7.5: Prepare validation context for formatter

**Subagent:**
- ui-spec-formatter (NEW - 2025-11-05, 507 lines)
  - Reads UI spec, validates framework compliance
  - Generates display template (SUCCESS/PARTIAL/FAILED)
  - Returns structured JSON

**Reference Files:**
- ui-result-formatting-guide.md (NEW - 2025-11-05, 394 lines) - Framework guardrails for formatter

**Token Efficiency (PROJECTED after command refactoring):**
- Command: ~3,000 tokens (down from ~8,000)
- Skill: ~42,000 tokens (up from ~35K, includes Phase 7 validation)
- Subagent (ui-spec-formatter): ~8,000 tokens (isolated context)
- **Savings: 62% reduction in main conversation tokens**

**Key Features:**
- **No self-healing:** All ambiguities resolved via AskUserQuestion
- **User authority:** User makes all decisions (fix/accept/defaults/regenerate)
- **Framework-aware:** Validates against all 6 context files
- **Quality gates:** FAILED halts, PARTIAL warns, SUCCESS proceeds

---

### /dev [STORY-ID]

**Purpose:** Execute TDD development cycle (Red→Green→Refactor)

**Invokes:** `devforgeai-development` skill

**Workflow:**
1. **Phase 0:** Argument validation (story ID format, file exists, status check)
2. **Phase 1:** Set context markers and invoke `devforgeai-development` skill
3. **Phase 2:** Verify completion (skill updated story status)
4. **Phase 3:** Report results (success/incomplete/failure)

**The skill handles all implementation logic:**
- **Phase 0 (Pre-Flight):** Git validation (git-validator subagent), tech detection (tech-stack-detector subagent), context files, QA failure detection
- **Phase 1-4 (TDD Cycle):** Red → Green → Refactor → Integration
- **Phase 4.5 (Deferral Challenge):** Challenge ALL deferrals (pre-existing + new) with deferral-validator subagent, require user approval (RCA-006)
- **Phase 5 (Git/Tracking):** Handle new incomplete items + commits/file-based tracking

**Example:**
```
> /dev STORY-042
```

**Output:**
- Implementation code in source tree
- Test files with 100% pass rate
- Git commits (or file-based change tracking)
- Story status updated to "Dev Complete"

**Architecture (Post-Refactoring 2025-11-05):**

**Command (513 lines - Lean Orchestration):**
- Argument parsing and validation
- Story file loading via @file reference
- Context markers for skill
- Skill invocation
- Results reporting

**Skill (devforgeai-development - Comprehensive Implementation):**
- Phase 0: Pre-Flight Validation
  - git-validator subagent
  - tech-stack-detector subagent
  - Context files validation
  - QA failure detection
- Phase 1-4: TDD Cycle (Red → Green → Refactor → Integration)
- Phase 4.5: Deferral Challenge Checkpoint (RCA-006)
  - Challenge ALL deferrals (pre-existing from template + new from TDD)
  - Invoke deferral-validator subagent (blocker validation)
  - Require user approval for EVERY deferred item
  - Timestamp all approvals
- Phase 5: Handle New Incomplete Items
  - Layer 1: Python validator (format check)
  - Layer 2: Interactive checkpoint (AskUserQuestion for new items)
  - Layer 3: Git commit or file-based tracking

**Token Efficiency:**
- Command: ~3,000-5,000 tokens (down from 15,000)
- Skill: ~85,000 tokens (isolated context)
- **Savings: 67% reduction in main conversation tokens**

---

### /qa [STORY-ID] [mode]

**Purpose:** Run quality validation (light or deep mode)

**Syntax:** `/qa [STORY-ID] [mode]`
- Mode: `deep` or `light` (no -- prefix)
- Default: Inferred from story status (deep if Dev Complete, light if In Development)

**Invokes:** `devforgeai-qa` skill

**Modes:**
- **Light (~10K tokens)**: Build/syntax checks, test execution, quick anti-pattern scan
- **Deep (~65K tokens)**: Coverage analysis, comprehensive anti-patterns, spec compliance, quality metrics

**Workflow:**
1. Argument validation and story loading
2. Invoke devforgeai-qa skill
3. Display results (from qa-result-interpreter subagent)
4. Update story file (deep mode pass only - Phase 4)
5. Provide next steps

**Architecture (Refactored 2025-11-05, Enhanced 2025-11-06):**

**Command (426 lines - Lean Orchestration with Phase 4):**
- Argument parsing and validation (20 lines)
- Story file loading via @file reference
- Context markers for skill
- Skill invocation (15 lines)
- Result display (10 lines) - outputs subagent-generated template
- **Phase 4: Story file updates (116 lines - NEW 2025-11-06)**
  - Updates story status to "QA Approved" (deep mode pass only)
  - Appends QA Validation History section
  - Updates YAML frontmatter timestamp
  - Error handling for file write failures

**Skill (devforgeai-qa - Comprehensive Validation):**
- Phase 0-4: All validation phases (unchanged)
- Phase 5: Generate QA report + invoke qa-result-interpreter subagent
  - qa-result-interpreter parses report and generates display template
  - Returns structured JSON with display, violations, next steps
  - Skill returns result to command

**Token Efficiency:**
- Command: ~3.5K tokens (down from 8,000)
- Skill: ~65,000 tokens (isolated context)
- Subagent (qa-result-interpreter): ~8,000 tokens (isolated context)
- **Savings: 56% reduction in main conversation tokens**

**Example:**
```
> /qa STORY-042           # Defaults to deep mode
> /qa STORY-042 deep      # Explicit deep mode
> /qa STORY-042 light     # Explicit light mode
```

**Output:**
- QA report in `.devforgeai/qa/reports/{STORY-ID}-qa-report.md`
- Coverage report
- **Story status updated to "QA Approved" (deep mode pass only - NEW 2025-11-06)**
- **QA Validation History section added to story file (deep mode pass only - NEW 2025-11-06)**
- **YAML frontmatter timestamp updated (deep mode pass only - NEW 2025-11-06)**

**Enhanced Features:**
- **RCA-006**: Invokes deferral-validator subagent (validates all deferred DoD items)
- **RCA-006**: FAILS QA on CRITICAL (circular deferrals) or HIGH (unjustified deferrals) violations
- **RCA-006**: Tracks QA iteration history in story file (attempt number, violations, resolutions)
- **QA Refactoring 2025-11-05**: Invokes qa-result-interpreter subagent for display generation
- **QA Refactoring 2025-11-05**: 57% code reduction (692 → 295 lines), 74% character reduction (31K → 8K)
- **Phase 4 Enhancement 2025-11-06**: Automatic story file updates on deep mode pass
  - Closes workflow gap identified in RCA (story status not updated after QA)
  - Maintains lean orchestration pattern (73% of 15K budget)
  - Post-skill orchestration (no bypass of devforgeai-qa skill)

---

### /release [STORY-ID] [environment]

**Purpose:** Deploy to staging and/or production

**Syntax:** `/release [STORY-ID] [environment]`
- Environment: `staging` or `production` (no -- prefix)
- Default: `staging` if not specified

**Invokes:** `devforgeai-release` skill

**Workflow:**
1. Pre-release validation (QA approved)
2. Staging deployment + smoke tests
3. Production deployment (if staging succeeds)
4. Post-deployment validation
5. Release documentation
6. Story status update to "Released"

**Example:**
```
> /release STORY-042              # Defaults to staging
> /release STORY-042 staging      # Explicit staging
> /release STORY-042 production   # Production deployment
```

**Output:**
- Code deployed to environments
- Smoke tests executed
- Release notes generated
- Story status = "Released"

---

### /orchestrate [STORY-ID]

**Purpose:** Execute complete story lifecycle end-to-end

**Invokes:** Multiple skills sequentially

**Workflow:**
1. Story validation & checkpoint detection
2. Development phase (invokes devforgeai-development)
3. QA validation (invokes devforgeai-qa)
4. **Phase 3.5: QA Failure Handling** (NEW - RCA-006) - Retry loop with max 3 attempts
5. Staging release (invokes devforgeai-release --env=staging)
6. Production release (invokes devforgeai-release --env=production)
7. Workflow history finalization

**Checkpoint Recovery:**
- Resumes from last successful phase if failures occur
- Checkpoints: DEV_COMPLETE, QA_APPROVED, STAGING_COMPLETE

**Example:**
```
> /orchestrate STORY-042
```

**Output:**
- Complete story lifecycle executed
- All quality gates passed
- Story deployed to production
- Workflow history documented

**Architecture (Post-Refactoring 2025-11-06):**

**Command (527 lines - Lean Orchestration):**
- Argument validation and story loading
- Skill invocation with context markers
- Result display from skill
- Minimal error handling

**Skill (devforgeai-orchestration - Enhanced):**
- Phase 0: Checkpoint detection (NEW - was in command)
- Phase 1-2: Story validation, development invocation
- Phase 3: QA invocation
- Phase 3.5: QA retry logic with loop prevention (NEW - was in command)
- Phase 4-5: Staging and production release
- Phase 6: Finalization (NEW - was in command)

**Token Efficiency:**
- Command: ~2.5K tokens (down from ~4K)
- Skill: ~155K-175K tokens (isolated context)
- **Savings: 37% reduction in main conversation tokens**

**Enhanced Features:**
- **Checkpoint Resume** (Phase 0) - Skill detects and resumes from DEV_COMPLETE, QA_APPROVED, STAGING_COMPLETE
- **QA Retry Loop** (Phase 3.5) - Max 3 attempts with deferral-specific handling, follow-up story creation, loop prevention
- **Complete Integration** (100% skill coverage) - All 7 devforgeai-* skills documented in orchestration skill

**Refactoring 2025-11-06:**
- 12% line reduction (599 → 527 lines)
- 4% character reduction (15,012 → 14,422 chars)
- Budget compliance achieved (100% → 96%)
- 234 lines business logic extracted to skill

---

---

## Slash Command Syntax & Limitations

### What Works

**Positional arguments:**
```
/qa STORY-001 deep           ✅ Correct
/release STORY-001 production ✅ Correct
```

**Multiple arguments:**
```
$1 = First argument (e.g., STORY-001)
$2 = Second argument (e.g., deep, production)
$3 = Third argument (if needed)
```

**@file references with $1:**
```
@.ai_docs/Stories/$1.story.md  ✅ Correct
```

### What Doesn't Work

**Flag syntax:**
```
/qa --mode=deep STORY-001      ❌ Wrong (will ask for clarification)
/qa STORY-001 --mode=deep      ⚠️ Works but educates user
/release STORY-001 --env=prod  ⚠️ Works but educates user
```

**@file with $ARGUMENTS:**
```
@.ai_docs/Stories/$ARGUMENTS.story.md  ❌ Wrong (includes all args/flags in filename)
```

**Skill invocations with arguments:**
```
Skill(command="devforgeai-qa --mode=deep")  ❌ Wrong (Skills don't accept parameters)
```

### Correct Parameter Passing to Skills

**Skills cannot accept command-line parameters.** Use conversation context instead:

```
# Step 1: Load context (via @file or explicit text)
@.ai_docs/Stories/STORY-001.story.md

# Step 2: State parameters explicitly
**Validation Mode:** deep
**Environment:** staging

# Step 3: Invoke skill WITHOUT arguments
Skill(command="devforgeai-qa")

# Skill extracts parameters from conversation context
```

---

## Command Discovery

All commands appear in `/help` after terminal restart.

**To see available commands:**
```
> /help
```

---

## Command Files Location

All command files are in `.claude/commands/`:
- `ideate.md` (410 lines - refactored 2025-11-05, down from 463)
- `create-context.md` (496 lines)
- `create-epic.md` (250 lines)
- `create-sprint.md` (250 lines - refactored 2025-11-05, down from 497)
- `create-story.md` (500 lines - refactored 2025-11-05, down from 857)
- `create-ui.md` (622 lines)
- `dev.md` (513 lines - refactored 2025-11-05, down from 860)
- `qa.md` (295 lines - refactored 2025-11-05, down from 692)
- `release.md` (~400 lines)
- `orchestrate.md` (527 lines - refactored 2025-11-06, down from 599)
- `audit-deferrals.md` (452 lines)
- `audit-budget.md` (371 lines - NEW 2025-11-05)

---

### /audit-deferrals

**Purpose:** Audit all stories for deferral violations, circular chains, and resolvable deferrals

**Invokes:** deferral-validator subagent (for each story with deferrals)

**Workflow:**
1. **Phase 1:** Discover QA Approved/Released stories
2. **Phase 2:** Scan for deferrals in each story
3. **Phase 2.5:** Blocker validation (RCA-006 Phase 2 - NEW)
   - Check dependency stories (git log, story status)
   - Check toolchains (rustup, npm, dotnet)
   - Check artifacts (file system validation)
   - Check ADRs (file existence)
   - Categorize: Resolvable vs Valid vs Invalid
4. **Phase 3:** Validate deferrals (deferral-validator subagent)
5. **Phase 4:** Aggregate results by severity
6. **Phase 5:** Generate audit report with actionable insights

**Example:**
```
> /audit-deferrals
```

**Output:**
- Audit report in `.devforgeai/qa/deferral-audit-{timestamp}.md`
- Resolvable deferrals (can be attempted now)
- Valid deferrals (blockers still present)
- Invalid deferrals (missing targets, circular chains)
- Technical debt metrics (age, trends)
- Actionable recommendations

**Enhanced Features (RCA-006 Phase 2):**
- **Blocker validation:** Automatically checks if blockers resolved
- **Actionable insights:** Specific commands to resolve deferrals
- **Debt metrics:** Total age, average age, oldest deferral
- **Trend analysis:** Flags aging deferrals (>30 days)
- **Recommendations:** Debt reduction sprint creation if ≥3 resolvable

**Integration:**
- **Auto-invoked:** Sprint retrospective (Phase 7 of orchestration skill)
- **Recommended schedule:** End of each sprint, quarterly, after major changes

**Architecture:**
- Command: 610 lines (comprehensive audit logic)
- Invokes: deferral-validator subagent
- Output: Markdown report, console summary

---

### /audit-budget

**Purpose:** Automated command budget compliance audit

**Invokes:** None (simple utility, no skill needed)

**Workflow:**
1. Load lean-orchestration-pattern.md (extract budget limits)
2. Scan all commands in `.claude/commands/`
3. Calculate character and line counts
4. Compare to budget thresholds (15K hard, 12K warning, 10K target)
5. Categorize commands (over, high, compliant)
6. Generate compliance report with priority queue

**Example:**
```
> /audit-budget
```

**Output:**
- Compliance summary (statistics table)
- Over-budget commands (priority 1)
- High-usage commands (priority 2)
- Compliant commands (reference implementations)
- Refactoring priority queue
- Protocol reference for methodology

**Architecture:**

This command exemplifies lean orchestration for simple tasks:
- No skill needed (task is straightforward)
- Minimal logic (scan, calculate, categorize)
- Actively leverages protocol (reads lean-orchestration-pattern.md)
- Read-only (no modifications)
- Fast execution (<30 seconds)
- Character budget: 9,978 (66% of limit) - demonstrates compliance

**Token Efficiency:**
- Command overhead: ~2K tokens
- Execution: ~1K tokens (wc operations)
- Total: ~3K tokens

**Current Audit Results (2025-11-05):**
- Over-budget: 4 commands (create-story 153%, create-ui 126%, release 121%, orchestrate 100%)
- High-usage: 5 commands (create-epic 95%, audit-deferrals 87%, create-context 84%, create-sprint 84%, dev 84%)
- Compliant: 5 commands (qa 48%, audit-budget 66%, test commands)

**Related:**
- `/audit-deferrals` - Audits deferred work in stories
- This complements with command architecture audit

---

## Integration Patterns

Commands integrate with skills using the Skill tool:
```
Skill(command="devforgeai-development --story=STORY-001")
Skill(command="devforgeai-qa --mode=deep --story=STORY-001")
Skill(command="devforgeai-release --story=STORY-001")
```

This creates **context isolation** - each skill operates in a separate context window, keeping main conversation efficient.
