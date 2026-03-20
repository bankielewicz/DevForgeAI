# DevForgeAI Slash Commands Reference

<quick_index> <!-- 46 commands -->
## Quick Reference Index

| Category | Commands | Count | Jump To |
|----------|----------|-------|---------|
| **Planning & Setup** | /brainstorm, /ideate, /create-context, /create-epic, /create-sprint, /assess-me | 6 | [↓](#planning-setup-5-commands) |
| **Story Development** | /create-story, /create-ui, /dev, /dev-status, /resume-dev | 5 | [↓](#story-development-5-commands) |
| **Validation & Release** | /qa, /release, /validate-stories, /fix-story | 4 | [↓](#validation-release-4-commands) |
| **Orchestration** | /orchestrate, /validate-epic-coverage, /create-missing-stories | 3 | [↓](#orchestration-lifecycle-3-commands) |
| **Framework Maintenance** | /audit-deferrals, /audit-alignment, /audit-budget, /audit-hooks, /audit-hybrid, /audit-orphans, /audit-w3, /rca, /create-stories-from-rca, /review-qa-reports, /prompt-version | 11 | [↓](#framework-maintenance-9-commands) |
| **Session & History** | /chat-search, /insights | 2 | [↓](#session-history-2-commands) |
| **Research & Analysis** | /research, /recommendations-triage | 2 | [↓](#research-analysis-2-commands) |
| **Feedback System** | /feedback, /feedback-config, /feedback-search, /feedback-reindex, /export-feedback, /import-feedback, /feedback-export-data | 7 | [↓](#feedback-system-6-commands) |
| **Collaboration** | /collaborate | 1 | [↓](#collaboration-1-command) |
| **Infrastructure** | /create-agent, /document, /setup-github-actions, /worktrees | 4 | [↓](#infrastructure-4-commands) |
| **Utility** | /read-constitution, /devforgeai-validate | 2 | [↓](#utility-2-commands) |

**Total Commands:** 46 | **Pattern Compliance:** See `command-pattern-compliance.md`
</quick_index>

---

<overview> <!-- 46 commands overview -->
Complete guide to the **46 slash commands** for DevForgeAI workflows.

**Last Updated:** 2026-02-24

**📊 Pattern Compliance Status:** See `command-pattern-compliance.md` for lean orchestration pattern compliance status of all commands (budget %, refactoring status, token efficiency).
</overview>

---

<command_overview> <!-- 46 commands -->
## Command Overview

DevForgeAI provides **46 slash commands** organized into **11 categories**:

**Planning & Setup (6 commands):**
- `/brainstorm` - Transform vague problems into structured brainstorm documents
- `/ideate` - Transform business idea to structured requirements
- `/create-context` - Generate 6 architectural context files
- `/create-epic` - Generate epic from requirements
- `/create-sprint` - Plan 2-week sprint with story selection
- `/assess-me` - Run guided self-assessment to generate adaptive coaching profile

**Story Development (5 commands):**
- `/create-story` - Generate story with acceptance criteria
- `/create-ui` - Generate UI component specs (web/GUI/terminal)
- `/dev` - Execute TDD development cycle (Red→Green→Refactor)
- `/dev-status` - Display development progress without invoking full workflow
- `/resume-dev` - Resume development from specific phase (NEW)

**Validation & Release (4 commands):**
- `/qa` - Run quality validation (light/deep modes)
- `/release` - Deploy to staging and production
- `/validate-stories` - Validate stories against constitutional context files
- `/fix-story` - Apply automated/guided fixes to story/epic files from audit findings (NEW)

**Orchestration & Lifecycle (3 commands):**
- `/orchestrate` - Full lifecycle: Dev → QA → Release
- `/validate-epic-coverage` - Validate epic coverage and report gaps (NEW)
- `/create-missing-stories` - Create stories for detected coverage gaps (NEW)

**Framework Maintenance (11 commands):**
- `/audit-deferrals` - Audit deferred work for circular chains and invalid references
- `/audit-alignment` - Validate configuration layer alignment across all project layers (NEW)
- `/audit-budget` - Audit command character budgets against lean orchestration
- `/audit-hooks` - Audit hook registry and invocation history (NEW)
- `/audit-hybrid` - Audit commands for hybrid command/skill violations (NEW)
- `/audit-orphans` - Scan for orphaned files, duplicate templates, and sync drift (NEW)
- `/audit-w3` - Audit codebase for W3 violations (auto-skill chaining) (NEW)
- `/rca` - Perform Root Cause Analysis with 5 Whys methodology
- `/create-stories-from-rca` - Create user stories from RCA recommendations
- `/review-qa-reports` - Process QA gap files and create remediation stories
- `/prompt-version` - Prompt versioning with before/after snapshots and SHA-256 verification (NEW)

**Session & History (2 commands):**
- `/chat-search` - Search chat history and resume previous conversations
- `/insights` - Session data mining for workflow patterns (NEW - EPIC-034)

**Research & Analysis (2 commands):**
- `/research` - Capture and persist research findings across sessions
- `/recommendations-triage` - Triage AI-generated improvement recommendations (NEW)

**Feedback System (7 commands):**
- `/feedback` - Manual feedback trigger with context (NEW)
- `/feedback-config` - View and edit feedback system configuration (NEW)
- `/feedback-search` - Search feedback history with filters (NEW)
- `/feedback-reindex` - Rebuild feedback session index (NEW)
- `/export-feedback` - Export feedback sessions to portable ZIP (NEW)
- `/import-feedback` - Import feedback sessions from ZIP package (NEW)
- `/feedback-export-data` - Export feedback data with selection criteria (NEW)

**Collaboration (1 command):**
- `/collaborate` - Generate cross-AI collaboration document for sharing issues with external LLMs (NEW)

**Infrastructure (4 commands):**
- `/create-agent` - Create DevForgeAI-aware Claude Code subagent
- `/document` - Generate and maintain project documentation
- `/setup-github-actions` - Create GitHub Actions CI/CD workflows (NEW)
- `/worktrees` - List and manage Git worktrees for parallel development (NEW)

**Utility (2 commands):**
- `/read-constitution` - Read constitutional context files
- `/devforgeai-validate` - Validate DevForgeAI installation (NEW)
</command_overview>

---

<command_details>
## Command Details

### /brainstorm [optional-topic] | --resume BRAINSTORM-ID

**Purpose:** Transform vague business problems into structured brainstorm documents

**Invokes:** `brainstorming` skill

**Workflow:**
1. Argument parsing (topic or resume mode)
2. Invoke brainstorming skill (7-phase BA discovery)
3. Generate brainstorm document in `devforgeai/specs/brainstorms/`
4. Display completion summary with next steps

**The skill handles 7 phases:**
- **Phase 1:** Stakeholder Discovery - Who is involved?
- **Phase 2:** Problem Exploration - 5 Whys analysis
- **Phase 3:** Opportunity Mapping - Blue-sky thinking
- **Phase 4:** Constraint Discovery - Budget, timeline, resources
- **Phase 5:** Hypothesis Formation - Testable assumptions
- **Phase 6:** Prioritization - MoSCoW + Impact-Effort matrix
- **Phase 7:** Handoff Synthesis - Generate AI-consumable document

**Examples:**
```bash
# Start new brainstorm (interactive topic discovery)
/brainstorm

# Start with a topic
/brainstorm "improve customer onboarding"

# Resume a previous session
/brainstorm --resume BRAINSTORM-001
```

**Session Continuity:**
- Context window monitoring at 70% threshold
- Checkpoints saved to `devforgeai/specs/brainstorms/BRAINSTORM-NNN.checkpoint.json`
- Resume with `--resume BRAINSTORM-ID`

**Output:**
- Brainstorm document: `devforgeai/specs/brainstorms/BRAINSTORM-NNN-title.brainstorm.md`
- Feeds into `/ideate` (auto-detected)

**Next Step:**
```
/ideate
```

---

### /ideate [business-idea]

**Purpose:** Transform business idea into structured requirements

**Invokes:** `spec-driven-ideation` skill

**Workflow:**
1. Argument validation (capture business idea)
2. Invoke spec-driven-ideation skill (6-phase discovery)
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

### User Input Guidance

**For effective ideation input:** Business ideas should describe the problem being solved, target market, and expected benefits. Avoid vague statements like "build an app" - instead, provide specific context.

**File:** `.claude/skills/spec-driven-ideation/references/user-input-guidance.md`

**Load command:**
```
Read(file_path=".claude/skills/spec-driven-ideation/references/user-input-guidance.md")
```

**Example effective input:**
```
/ideate Build an AI-powered task prioritization system for software teams that automatically categorizes tasks by urgency, dependency chains, and team member capacity to reduce planning time by 40% and improve sprint velocity by 25%
```

**Output:**
- Epic document(s) in `devforgeai/specs/Epics/`
- Requirements spec in `devforgeai/specs/requirements/`
- Complexity assessment (0-60 score, architecture tier)
- Technology recommendations by tier

**Architecture (Post-Refactoring 2025-11-05):**

**Command (410 lines - Lean Orchestration):**
- Argument parsing and validation
- Skill invocation with context markers
- Basic artifact verification
- Brief completion confirmation
- Next steps guidance (defers to skill)

**Skill (spec-driven-ideation - Comprehensive Discovery):**
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

**Invokes:** `spec-driven-architecture` skill

**Workflow:**
1. Interactive technology selection (via AskUserQuestion)
2. Generate all 6 context files
3. Create initial ADR
4. Validate context completeness

**Example:**
```
> /create-context my-saas-platform
```

### User Input Guidance

**For architecture setup:** Context creation is interactive and skill-driven. Provide the project name and be ready to answer questions about technology choices, architecture patterns, and project scope.

**File:** `.claude/skills/spec-driven-architecture/references/user-input-guidance.md`

**Load command:**
```
Read(file_path=".claude/skills/spec-driven-architecture/references/user-input-guidance.md")
```

**Example effective input:**
```
/create-context enterprise-reporting-platform
(Then answer skill questions about: greenfield/brownfield, tech stack preferences, team size, deployment targets, regulatory requirements)
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

### User Input Guidance

**For epic definition:** Epic names should be clear and business-focused. The skill will guide you through feature decomposition and technical assessment with interactive questions. Provide specific requirements about goals, timeline, and stakeholders.

**File:** `.claude/skills/devforgeai-orchestration/references/user-input-guidance.md`

**Load command:**
```
Read(file_path=".claude/skills/devforgeai-orchestration/references/user-input-guidance.md")
```

**Example effective input:**
```
/create-epic Multi-Factor Authentication Enhancement
(Then provide: business goal, timeline, success metrics, affected teams, and dependencies)
```

**Output:**
- Epic file in `devforgeai/specs/Epics/{EPIC-ID}.epic.md`
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
- **Character budget: 13,457 chars (89% of limit) - HIGH USAGE**

**Example:**
```
> /create-sprint "User Authentication Sprint"
> /create-sprint
```

### User Input Guidance

**For sprint planning:** Provide clear sprint names and select stories with realistic capacity (20-40 points recommended). The skill will validate capacity and guide story selection with interactive questions.

**File:** `.claude/skills/devforgeai-orchestration/references/user-input-guidance.md`

**Load command:**
```
Read(file_path=".claude/skills/devforgeai-orchestration/references/user-input-guidance.md")
```

**Example effective input:**
```
/create-sprint Sprint-5-Performance-Optimization
(Then select stories, provide start/end dates, confirm team capacity allocation)
```

**Output:**
- Sprint file in `devforgeai/specs/Sprints/Sprint-{N}.md`
- Stories updated to "Ready for Dev" status
- Sprint references added to story files
- Workflow history entries

---

### /assess-me

**Description:** Run a guided self-assessment questionnaire to generate an adaptive coaching profile
**Usage:** `/assess-me [--recalibrate]`
**Invokes:** `assessing-entrepreneur` skill
**Category:** Planning & Setup

**Workflow:**
1. Load assessment questionnaire (interactive)
2. Normalize self-reported responses into structured profile
3. Generate adaptive coaching recommendations
4. Persist profile for future sessions

**Examples:**
```bash
/assess-me              # Run initial assessment
/assess-me --recalibrate  # Recalibrate existing profile
```

**Output:**
- Structured entrepreneurship profile
- Adaptive coaching recommendations
- Persisted assessment data for future sessions

---

### /create-story [feature-description | epic-id]

**Purpose:** Generate user story with acceptance criteria, technical specifications, and UI specifications

**Invokes:** `spec-driven-stories` skill

**Modes:**
- **Single Story Mode:** `/create-story [feature-description]` - Create one story from description
- **Batch Mode:** `/create-story [epic-id]` - Create multiple stories from epic features (NEW 2025-11-07)

**Workflow (Single Story):**
1. Argument validation (capture feature description)
2. Invoke spec-driven-stories skill (8-phase workflow)
3. Verify story file created
4. Brief confirmation
5. Next steps guidance

**Workflow (Batch Mode - NEW):**
1. Detect epic pattern (epic-001, EPIC-001)
2. Extract features from epic (Grep)
3. Multi-select features (AskUserQuestion, multiSelect: true)
4. Collect batch metadata (sprint, priority - ask once for all)
5. Loop: Create stories sequentially with progress tracking (TodoWrite)
6. Display batch summary (created/failed counts)

**The skill handles all implementation:**
- **Phase 1-2:** Story Discovery & Requirements Analysis (epic/sprint, metadata, requirements-analyst subagent)
- **Phase 3-4:** Technical & UI Specification (api-designer subagent, data models, components, mockups)
- **Phase 5-6:** Story File Creation & Epic/Sprint Linking
- **Phase 7:** Self-Validation (quality checks, self-healing)
- **Phase 8:** Completion Report (summary, next actions)
- **Batch Mode:** Detects `**Batch Mode:** true` marker, extracts metadata, skips interactive questions

**Example:**
```
> /create-story User login with email and password
> /create-story Admin dashboard with analytics and charts
> /create-story epic-001  # NEW: Batch mode - creates multiple stories
```

### User Input Guidance

**For story creation:** Feature descriptions must be specific and include business context, success criteria, and any constraints. Avoid generic statements; instead describe the complete user workflow and business value.

**File:** `devforgeai/specs/Stories/` (stories reference context from parent epic and project tech-stack)

**Load command:**
```
Read(file_path=".claude/memory/effective-prompting-guide.md")
```

**Example effective input:**
```
/create-story User login with email/password authentication, password reset via email, session timeout after 30 minutes of inactivity, account lockout after 5 failed attempts, and TOTP multi-factor authentication support for enterprise users
```

**Output (Single):**
- Story file in `devforgeai/specs/Stories/{STORY-ID}-{slug}.story.md`
- YAML frontmatter with metadata
- User story (As a/I want/So that format)
- 3+ testable acceptance criteria (Given/When/Then)
- Technical specification (API contracts, data models, business rules, dependencies)
- UI specification (components, mockups, interfaces, accessibility - if applicable)
- Non-functional requirements (measurable performance, security, scalability)
- Edge cases and error handling
- Definition of Done with checkboxes

**Output (Batch - NEW):**
- Multiple `.story.md` files (one per selected feature)
- All stories linked to epic and sprint
- Gap-aware story IDs (fills gaps before incrementing)
- Batch summary with created/failed counts
- Progress tracking during creation (TodoWrite)

**Architecture (Post-Refactoring 2025-11-07):**

**Command (477 lines - Lean Orchestration + Batch Support):**
- Phase 0: Mode detection (epic pattern vs. feature description) - NEW
- Epic Batch Workflow (~40 lines) - NEW
- Phase 1: Single story argument validation
- Phase 2: Skill invocation with context markers
- Phase 3: Story file verification
- Phase 4: Brief completion confirmation
- Phase 5: Next steps guidance (simplified)

**Skill (spec-driven-stories - Complete Story Generation):**
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
- Command (single): ~2,500 tokens (down from ~5,752)
- Command (batch): ~6,000 tokens (for 5 stories)
- Skill: ~90,000 tokens/story (isolated context)
- References: ~56,000 tokens total (loaded progressively per phase, isolated context)
- **Savings: 56% reduction in main conversation tokens (single mode)**
- **Batch savings: 66% reduction (vs. 5 separate commands)**
- **Character budget: 14,895 chars (99% of 15K limit) - HIGH USAGE** (was 153% - **CRITICAL FIX**)

**Batch Mode Benefits (NEW):**
- Question reduction: 20 questions → 4 questions (for 5 stories)
- Command executions: 5 → 1 (80% reduction)
- Time: 10 min (5 separate) → 10-12 min (1 batch) - same time, better UX
- Gap-aware IDs: Automatically fills gaps in story numbering

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

### /create-agent [name] [options]

**Purpose:** Create DevForgeAI-aware Claude Code subagents following framework patterns and official best practices

**Invokes:** `spec-driven-cc-guide` skill → `agent-generator` subagent v2.0

**Modes:**
- **Guided Mode:** `/create-agent [name]` - Interactive creation with questions (recommended)
- **Domain Mode:** `/create-agent [name] --domain=[domain]` - Use domain presets
- **Template Mode:** `/create-agent [name] --template=[name]` - Use proven template
- **Custom Spec Mode:** `/create-agent [name] --spec=[file]` - From specification file

**Workflow:**
1. Argument validation (name format, mode detection)
2. Load Claude Code official guidance (spec-driven-cc-guide skill)
3. Set context markers for agent-generator
4. Invoke agent-generator subagent (framework-aware generation)
5. Display results (files, validation, integration)

**Example:**
```
> /create-agent my-backend-validator --domain=backend
```

### User Input Guidance

**For subagent specification:** Agent names should be descriptive and lowercase with hyphens (e.g., my-code-reviewer). Provide clear domain or template selections. Answer all interactive questions to ensure the subagent aligns with framework patterns and your project constraints.

**File:** `.claude/skills/spec-driven-cc-guide/references/` (official Claude Code patterns and DevForgeAI framework constraints)

**Load command:**
```
Read(file_path=".claude/memory/skills-reference.md")
```

**Example effective input:**
```
/create-agent security-validator --domain=security
(Then answer: special capabilities, tool requirements, integration points, naming patterns)
```

**Output:**
- Subagent file in `.claude/agents/[name].md`
- Reference file (if command-related, domain-specific, or decision-making)
- Validation report (12-point framework compliance)
- Integration guidance

**Features:**
- Framework-aware generation (references context files, quality gates, workflow states)
- Claude Code best practice compliance (official patterns)
- 12-point validation (6 DevForgeAI + 6 Claude Code checks)
- Automatic reference file generation for framework guardrails
- Template library (5 templates: code-reviewer, test-automator, documentation-writer, deployment-coordinator, requirements-analyst)
- Domain presets (7 domains: backend, frontend, qa, security, deployment, architecture, documentation)

**Architecture (2025-11-15):**

**Command (282 lines, 6,755 chars, 45% budget):**
- Argument validation and mode detection
- spec-driven-cc-guide skill invocation
- Context markers for agent-generator
- agent-generator subagent invocation
- Result display and next steps

**Skill (spec-driven-cc-guide):**
- Loads official Claude Code subagent patterns
- Section 1: Subagents - Specialized AI Workers
- Provides: file format, YAML fields, tool selection, model guidelines

**Subagent (agent-generator v2.0):**
- Phase 0: Load framework references (Claude Code, CLAUDE.md, lean-orchestration)
- Execute mode-specific workflow (guided/template/domain/custom)
- Generate framework-aware system prompt
- Step 3.6: Validate framework compliance (12 checks)
- Step 4.5: Generate reference file (conditional)
- Return structured report

**Token Efficiency:**
- Command: ~4K tokens
- Skill (isolated): ~2K tokens
- Subagent (isolated): ~30-50K tokens
- **Savings: 92% in isolated contexts**

**Execution Time:** 1-3 minutes (varies by mode)

**Integration:**
- Created subagents are framework-aware
- Reference DevForgeAI context files
- Integrate with DevForgeAI skills
- Follow Claude Code official patterns
- Use native tools (40-73% token savings)

**Status:** Production ready (2025-11-15)

---

### /create-ui [STORY-ID or component-description]

**Purpose:** Generate UI component specs (web/GUI/terminal)

**Invokes:** `spec-driven-ui` skill

**Workflow:**
1. Argument validation and mode detection (story vs standalone)
2. Invoke spec-driven-ui skill (7-phase workflow)
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

### User Input Guidance

**For UI specification:** Describe components with specific requirements (web/desktop/terminal), interactive elements, validation rules, accessibility needs, and responsive behavior. The skill will ask clarifying questions about design patterns and framework preferences.

**File:** `.claude/skills/spec-driven-ui/references/user-input-guidance.md`

**Load command:**
```
Read(file_path=".claude/skills/spec-driven-ui/references/user-input-guidance.md")
```

**Example effective input:**
```
/create-ui "Multi-step form wizard with email validation, password strength indicator, WCAG AA accessibility, responsive grid layout for mobile/tablet/desktop, error messages below fields"
```

**Output:**
- UI component code in `devforgeai/specs/ui/`
- UI-SPEC-SUMMARY.md
- Story updated with UI references (if story mode)

**Architecture (Post-Refactoring 2025-11-05 - PLANNED):**

**Command (614 lines - FUTURE: ~300 lines after refactoring):**
- Argument parsing and validation (25 lines)
- Story file loading via @file reference (if story mode)
- Context markers for skill
- Skill invocation (15 lines)
- Result display (10 lines) - outputs subagent-generated template

**Skill (spec-driven-ui - Enhanced with Phase 7):**
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

**Invokes:** `spec-driven-dev` skill

**Workflow:**
1. **Phase 0:** Argument validation (story ID format, file exists, status check)
2. **Phase 1:** Set context markers and invoke `spec-driven-dev` skill
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

### User Input Guidance

**For development cycle:** Provide the story ID. The skill will read the story file (acceptance criteria, technical specification) and follow TDD workflow. Ensure story is in "Ready for Dev" status and all acceptance criteria are clearly defined.

**File:** Story AC (acceptance criteria in story file) and project context files (tech-stack.md, coding-standards.md, architecture-constraints.md)

**Load command:**
```
Read(file_path="devforgeai/specs/Stories/STORY-042.story.md")
```

**Example effective input:**
```
/dev STORY-042
(Story file contains clear AC, tech spec, and business context for TDD implementation)
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

**Skill (spec-driven-dev - Comprehensive Implementation):**
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

### /document [STORY-ID | --type=TYPE | --mode=MODE]

**Purpose:** Generate and maintain project documentation automatically

**Invokes:** `spec-driven-documentation` skill

**Modes:**
- **Greenfield**: Generate docs from completed stories
- **Brownfield**: Analyze codebase and identify gaps

**Example:**
```
> /document STORY-040                # Generate docs for story
> /document --type=readme            # Generate README.md
> /document --mode=brownfield --analyze  # Analyze codebase
> /document --list-templates         # Show available templates
```

**Output:**
- Documentation files (README, API docs, guides)
- Mermaid diagrams (architecture, sequences)
- Coverage report (≥80% threshold)

**Key Features:**
- 8 templates (README, API, Architecture, Developer Guide, etc.)
- Greenfield (story-based) + Brownfield (code analysis) modes
- Mermaid diagram generation
- Quality gate (80% coverage enforcement)
- HTML/PDF export support

**For detailed documentation, see:** `@.claude/memory/documentation-command-guide.md`

**Created:** 2025-11-18 (STORY-040)

---

### /dev-status [STORY-ID]

**Purpose:** Display development progress for a story without invoking full workflow

**Syntax:** `/dev-status [STORY-ID]`

**Invokes:** None (read-only utility command - no skill)

**Workflow:**
1. **Phase 0:** Argument validation (story ID format, locate story file)
2. **Phase 1:** Extract current state (phase-state.json, DoD checkboxes)
3. **Phase 2:** Display status (progress, remaining items)
4. **Phase 3:** Suggest next action (based on story state)

**Example:**
```
> /dev-status STORY-057
```

**Output:**
```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  Development Status: STORY-057
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

**Story:** Additional Skill Integrations
**Status:** In Development

**Progress:**
- Current Phase: 06 (Deferral Challenge)
- DoD Completion: 26/30 (87%)
- TDD Iteration: 2

**Remaining DoD Items:**
- Implementation: 2 items
- Quality: 1 item
- Testing: 1 item

**Suggested Next Action:**
Run `/dev STORY-057` to continue development
```

**Architecture (2026-01-04):**

**Command (236 lines, ~6,000 chars - Read-Only Utility):**
- Argument parsing and validation
- Phase-state.json reading (if exists)
- Story file DoD counting
- Progress display with formatting
- Next action suggestion (state-based)

**Tools Used:**
- `Read` - Read story file and phase-state.json
- `Glob` - Locate story and phase-state files
- `Grep` - (optional) Count DoD checkboxes

**Key Features:**
- **Read-only:** No file modifications, no skill invocation
- **Lightweight:** Uses haiku model for fast execution
- **Progress visibility:** Shows "where am I?" without re-running /dev
- **Smart suggestions:** Different next actions based on story state

**Character Budget:** ~6,000 chars (40% of 15K budget) - COMPLIANT

**Data Sources:**
- Story file: `devforgeai/specs/Stories/STORY-XXX*.story.md`
- Phase state: `devforgeai/workflows/STORY-XXX-phase-state.json`

**Related:**
- `/dev` - Execute full TDD development workflow
- `/resume-dev` - Resume development from specific phase
- `/qa` - Run QA validation

**Created:** 2026-01-04 (STORY-171, RCA-013 REC-5)

---

### /qa [STORY-ID] [mode]

**Purpose:** Run quality validation (light or deep mode)

**Syntax:** `/qa [STORY-ID] [mode]`
- Mode: `deep` or `light` (no -- prefix)
- Default: Inferred from story status (deep if Dev Complete, light if In Development)

**Invokes:** `spec-driven-qa` skill

**Modes:**
- **Light (~10K tokens)**: Build/syntax checks, test execution, quick anti-pattern scan
- **Deep (~65K tokens)**: Coverage analysis, comprehensive anti-patterns, spec compliance, quality metrics

**Workflow:**
1. Argument validation and story loading
2. Invoke spec-driven-qa skill
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

**Skill (spec-driven-qa - Comprehensive Validation):**
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

### User Input Guidance

**For QA validation:** Provide story ID and optionally specify validation mode (light/deep). Story should be in "Dev Complete" status with all AC implemented. No input description needed - validation rules are determined by story file and project context files.

**File:** Story file (acceptance criteria) and project context files (tech-stack.md, coding-standards.md)

**Load command:**
```
Read(file_path="devforgeai/specs/Stories/STORY-042.story.md")
```

**Example effective input:**
```
/qa STORY-042 deep
(Story file AC and implementation are validated against tech-stack and coding-standards constraints)
```

**Output:**
- QA report in `devforgeai/qa/reports/{STORY-ID}-qa-report.md`
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
  - Post-skill orchestration (no bypass of spec-driven-qa skill)

---

### /release [STORY-ID] [environment]

**Purpose:** Deploy to staging and/or production

**Syntax:** `/release [STORY-ID] [environment]`
- Environment: `staging` or `production` (no -- prefix)
- Default: `staging` if not specified

**Invokes:** `spec-driven-release` skill

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

### User Input Guidance

**For release operations:** Provide story ID and environment (staging/production). Story must be "QA Approved" status. The skill will handle deployment validation, smoke tests, and rollback if needed. Environment selection determines deployment target and validation level.

**File:** Story file (deployment specs) and deployment configuration (`devforgeai/deployment/`)

**Load command:**
```
Read(file_path="devforgeai/specs/Stories/STORY-042.story.md")
```

**Example effective input:**
```
/release STORY-042 staging
(Verify staging deployment and smoke tests before running: /release STORY-042 production)
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
2. Development phase (invokes spec-driven-dev)
3. QA validation (invokes spec-driven-qa)
4. **Phase 3.5: QA Failure Handling** (NEW - RCA-006) - Retry loop with max 3 attempts
5. Staging release (invokes spec-driven-release --env=staging)
6. Production release (invokes spec-driven-release --env=production)
7. Workflow history finalization

**Checkpoint Recovery:**
- Resumes from last successful phase if failures occur
- Checkpoints: DEV_COMPLETE, QA_APPROVED, STAGING_COMPLETE

**Example:**
```
> /orchestrate STORY-042
```

### User Input Guidance

**For full lifecycle orchestration:** Provide story ID only. The skill will execute all phases: development, QA validation, staging release, and production deployment. Story must be in "Ready for Dev" status. This command is best for stories without external dependencies.

**File:** Story file and project context files (all 6 context files required)

**Load command:**
```
Read(file_path="devforgeai/specs/Stories/STORY-042.story.md")
```

**Example effective input:**
```
/orchestrate STORY-042
(Single command handles: /dev → /qa deep → /release staging → /release production)
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
@devforgeai/specs/Stories/$1.story.md  ✅ Correct
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
@devforgeai/specs/Stories/$ARGUMENTS.story.md  ❌ Wrong (includes all args/flags in filename)
```

**Skill invocations with arguments:**
```
Skill(command="spec-driven-qa --mode=deep")  ❌ Wrong (Skills don't accept parameters)
```

### Correct Parameter Passing to Skills

**Skills cannot accept command-line parameters.** Use conversation context instead:

```
# Step 1: Load context (via @file or explicit text)
@devforgeai/specs/Stories/STORY-001.story.md

# Step 2: State parameters explicitly
**Validation Mode:** deep
**Environment:** staging

# Step 3: Invoke skill WITHOUT arguments
Skill(command="spec-driven-qa")

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
- Audit report in `devforgeai/qa/deferral-audit-{timestamp}.md`
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

### /audit-alignment [options]

**Purpose:** Validate configuration layer alignment across CLAUDE.md, system prompt, context files, rules, and ADRs

**Category:** Framework Maintenance

**Invokes:** `alignment-auditor` subagent

**Workflow:**
1. Load all configuration layers (CLAUDE.md, system prompt, 6 context files, rules, ADRs)
2. Perform pairwise comparison across layers
3. Detect contradictions and gaps with structured JSON evidence
4. Generate resolution proposals respecting mutability constraints
5. Produce alignment report with findings

**Examples:**
```bash
/audit-alignment                    # Full alignment audit
/audit-alignment --layer rules    # Audit rules layer only
```

**Output:**
- Alignment report with contradiction/gap findings
- JSON evidence with line numbers
- Resolution proposals (immutable-aware)
- Summary statistics

**Related:**
- `/audit-deferrals` - Audit deferred work
- `/audit-budget` - Audit command budgets
- `/create-context` - Generate context files (triggers alignment check)

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

### /rca [issue-description] [severity]

**Purpose:** Perform Root Cause Analysis with 5 Whys methodology for framework breakdowns

**Syntax:** `/rca [issue-description] [severity]`
- Issue description: Brief description of framework breakdown (required)
- Severity: CRITICAL | HIGH | MEDIUM | LOW (optional, defaults to inferred)

**Invokes:** `spec-driven-rca` skill

**Workflow:**
1. Argument validation (issue description, optional severity)
2. Auto-read relevant files (skills, commands, subagents, context)
3. Perform 5 Whys analysis (progressive questioning to root cause)
4. Collect evidence with file excerpts
5. Generate recommendations (CRITICAL → LOW priority)
6. Create RCA document in devforgeai/RCA/
7. Display completion report

**Example:**
```bash
/rca "spec-driven-dev didn't validate context files" CRITICAL
/rca "QA skill accepted pre-existing deferrals without challenge" HIGH
/rca "orchestration skipped checkpoint detection"
/rca "/dev command contains business logic"
```

**Output:**
- RCA document in `devforgeai/RCA/RCA-XXX-{slug}.md`
- Comprehensive 5 Whys analysis with evidence
- Files examined (with excerpts and line numbers)
- Prioritized recommendations (CRITICAL/HIGH/MEDIUM/LOW)
- Exact implementation code/text (copy-paste ready)
- Testing procedures for each recommendation
- Implementation checklist
- Prevention strategy (short-term and long-term)
- Related RCAs linked

**Architecture (2025-11-16):**

**Command (350 lines, ~9,500 chars - Lean Orchestration):**
- Phase 0: Argument validation (issue description, severity)
- Phase 1: Context markers for skill
- Phase 2: Skill invocation
- Phase 3: Result display (completion report)

**Skill (spec-driven-rca - Comprehensive RCA Workflow):**
- Phase 0: Issue Clarification (extract details, generate RCA number)
- Phase 1: Auto-Read Files (skills, commands, subagents, context files)
- Phase 2: 5 Whys Analysis (progressive questioning with evidence)
- Phase 3: Evidence Collection (organize excerpts, validate context)
- Phase 4: Recommendation Generation (prioritized, exact implementation)
- Phase 5: RCA Document Creation (auto-generate in devforgeai/RCA/)
- Phase 6: Validation & Self-Check (verify completeness, self-heal)
- Phase 7: Completion Report (return summary to command)

**Token Efficiency:**
- Command: ~3K tokens
- Skill: ~50-80K tokens (isolated context)
- References: ~4,000 lines (loaded progressively)
- **Savings: 94% of work in isolated context**

**Features:**
- **Auto-reads relevant files** - Based on affected component type
- **Evidence-based analysis** - All answers backed by file examination
- **Comprehensive evidence** - File excerpts with line numbers
- **Exact implementation** - Copy-paste ready code/text in recommendations
- **Framework-aware** - Understands context files, quality gates, workflow states
- **Progressive disclosure** - 5 reference files loaded as needed

**Character Budget:** 9,500 chars (63% of 15K budget) - COMPLIANT

**Execution Time:** 3-10 minutes (depends on complexity)

**Related:**
- `/audit-deferrals` - Audit technical debt
- `/audit-budget` - Audit command budgets
- Framework breakdowns can be analyzed systematically

---

### /create-stories-from-rca RCA-NNN [--threshold HOURS]

**Purpose:** Create user stories from RCA document recommendations

**Syntax:** `/create-stories-from-rca RCA-NNN [--threshold HOURS]`
- RCA-NNN: RCA document ID (case-insensitive, e.g., RCA-022 or rca-022)
- --threshold: Optional. Filter recommendations with effort >= N hours

**Invokes:** `spec-driven-stories` skill (batch mode)

**Workflow:**
1. Parse RCA document and extract recommendations (STORY-155)
2. Filter by effort threshold and sort by priority (STORY-156)
3. Display summary table for interactive selection
4. Create stories for selected recommendations (STORY-157)
5. Update RCA document with story links (STORY-158)

**Example:**
```bash
/create-stories-from-rca RCA-022
/create-stories-from-rca RCA-022 --threshold 2
/create-stories-from-rca --help
```

**Output:**
- Stories created in `devforgeai/specs/Stories/`
- RCA document updated with story references
- Completion summary with success/failure counts

**Architecture (2025-12-31):**

**Command (198 lines, 5,350 chars - Lean Orchestration):**
- Argument parsing and validation
- Progressive disclosure to 4 reference files
- Skill invocation for batch story creation
- RCA-Story linking after creation

**Reference Files:**
- `references/create-stories-from-rca/parsing-workflow.md` - Phases 1-5
- `references/create-stories-from-rca/selection-workflow.md` - Phases 6-9
- `references/create-stories-from-rca/batch-creation-workflow.md` - Phase 10
- `references/create-stories-from-rca/linking-workflow.md` - Phase 11

**Token Efficiency:**
- Command: ~2K tokens
- Progressive disclosure: 4 reference files (~28K total, loaded on demand)
- **Character budget: 5,350 chars (36% of 15K limit) - COMPLIANT**

**Related:**
- `/rca` - Create new RCA document
- `/create-story` - Create individual story
- `/audit-deferrals` - Audit deferred work

---

### /review-qa-reports [--source local|imports|all] [--min-severity LEVEL] [--epic EPIC-XXX] [--dry-run]

**Purpose:** Process QA gap files and create remediation user stories

**Category:** Framework Maintenance

**Invokes:** `devforgeai-qa-remediation` skill

**Workflow:**
1. Parse arguments and load config (`devforgeai/config/qa-remediation.yaml`)
2. Discover and parse gap files from specified source
3. Aggregate, deduplicate, score, and filter gaps by severity
4. Display summary table for interactive selection
5. Create stories for selected gaps via batch mode
6. Update source gap files with `implemented_in` references
7. Add skipped gaps to technical debt register

**Arguments:**
- `--source`: Gap file source - `local` (default), `imports`, or `all`
- `--min-severity`: Filter threshold - `CRITICAL`, `HIGH`, `MEDIUM` (default), `LOW`
- `--epic`: Associate created stories with an epic
- `--dry-run`: Preview gaps without creating stories

**Examples:**
```bash
/review-qa-reports                          # Review local reports, MEDIUM+ severity
/review-qa-reports --source imports         # Review imported external reports
/review-qa-reports --min-severity HIGH      # Only CRITICAL and HIGH gaps
/review-qa-reports --dry-run                # Preview without creating stories
/review-qa-reports --epic EPIC-025          # Associate stories with epic
```

**Gap Sources:**
- Local: `devforgeai/qa/reports/*-gaps.json` (generated by /qa)
- Imports: `devforgeai/qa/imports/**/*-gaps.json` (external projects)

**Gap Types Processed:**
- `coverage_gaps` - Test coverage below thresholds
- `anti_pattern_violations` - Code anti-patterns detected
- `code_quality_violations` - Metrics threshold violations
- `deferral_issues` - Invalid deferral patterns

**Output:**
- Stories created in `devforgeai/specs/Stories/`
- Enhancement report in `devforgeai/qa/enhancement-reports/`
- Skipped gaps added to `devforgeai/technical-debt-register.md`

**Token Efficiency:**
- Command: ~2K tokens
- Skill: ~12K tokens
- 5 reference files (progressive disclosure): ~8K tokens

**Related:**
- `/qa` - Generate gap files via QA validation
- `/create-stories-from-rca` - Similar pattern for RCA recommendations
- `/audit-deferrals` - Audit deferred work

---

### /audit-hybrid

**Description:** Audit commands for hybrid command/skill violations (excessive code before Skill invocation)
**Usage:** `/audit-hybrid`
**Model:** haiku
**Category:** Framework Maintenance

**Purpose:** Detect commands that implement business logic directly instead of delegating to skills, violating the lean orchestration pattern.

**Example:**
```bash
/audit-hybrid
```

**Output:**
- Report of commands with hybrid violations
- Severity classification per violation
- Refactoring recommendations

---

### /audit-orphans

**Description:** Scan for orphaned files, duplicate templates, backup artifacts, and sync drift
**Usage:** `/audit-orphans [--category=all|backups|duplicates|orphans|drift|agents|context] [--output=console|file]`
**Category:** Framework Maintenance

**Examples:**
```bash
/audit-orphans                          # Full scan all categories
/audit-orphans --category=backups       # Scan backup artifacts only
/audit-orphans --category=orphans       # Scan orphaned files only
/audit-orphans --output=file            # Write report to file
```

**Output:**
- Categorized findings (backups, duplicates, orphans, drift, agents, context)
- File paths with sizes
- Recommended cleanup actions

---

### /prompt-version

**Description:** Prompt versioning system for template migration safety - captures before/after snapshots with SHA-256 integrity verification
**Usage:** `/prompt-version <capture|finalize|rollback|history> <component-path-or-id> [--reason "description"] [--version N|previous]`
**Category:** Framework Maintenance

**Subcommands:**
- `capture` - Capture before-snapshot of a component before changes
- `finalize` - Record after-snapshot and commit version entry
- `rollback` - Restore component to a previous version
- `history` - Show version history for a component

**Examples:**
```bash
/prompt-version capture .claude/skills/spec-driven-dev/SKILL.md --reason "Adding phase markers"
/prompt-version finalize .claude/skills/spec-driven-dev/SKILL.md
/prompt-version rollback .claude/skills/spec-driven-dev/SKILL.md --version previous
/prompt-version history .claude/skills/spec-driven-dev/SKILL.md
```

**Output:**
- Version snapshot with SHA-256 hash
- Version history log
- Rollback confirmation with integrity verification

---

### /chat-search [search-keywords]

**Purpose:** Search chat history and resume previous conversations

**Category:** Session Management

**Workflow:**
1. Gather search criteria (keywords, project, timeframe)
2. Search through ~/.claude/history.jsonl
3. Display matching sessions with details
4. Optionally provide resume instructions

**Arguments:**
- `$1` (optional): Search keywords or phrase

**Example:**
```
> /chat-search "EPIC-010"
> /chat-search "story-066 development"
> /chat-search
```

**Interactive Features:**

**Phase 0: Search Criteria:**
- If no keywords provided → AskUserQuestion for search type:
  - Keywords/Text (e.g., "EPIC-010", "story-066")
  - Recent Sessions (last 10-50 sessions)
  - By Project (filter by project path)
  - By Slash Command (e.g., /dev, /create-story)
- Ask for project filter (current, all, or specific)
- Ask for result limit (10/20/50/all)

**Phase 1: Search Execution:**
- Search ~/.claude/history.jsonl using grep/jq
- Extract session details: ID, project, timestamp, message preview
- Deduplicate by session ID (keep most recent)
- Sort by timestamp descending
- Limit results as specified

**Phase 2: Display Results:**
```
═══════════════════════════════════════════════
CHAT HISTORY SEARCH RESULTS
═══════════════════════════════════════════════

Found 3 sessions matching "EPIC-010":

Session 1:
  ID: 83bfea53-ae2b-4e85-b755-33acd22892a4
  Project: /mnt/c/Projects/DevForgeAI2
  Last Active: 2024-11-18 14:32:44
  Last Message: 'devforgeai/specs/Epics/EPIC-010-parallel...'

[... more sessions ...]

═══════════════════════════════════════════════
```

**Phase 3: Resume Session:**
- AskUserQuestion: "Would you like to resume?"
  - Yes → Ask which session
  - No → Exit with instructions
- Display resume command:
  ```bash
  claude -r <session-id>
  claude -r <session-id> --fork-session
  ```

**Search Strategies:**

**By Keywords:**
- Story IDs: `STORY-066`, `story-066`
- Epic IDs: `EPIC-010`, `epic-010`
- Commands: `/dev`, `/create-story`, `/qa`
- Feature names: `parallel story development`
- Error messages: Paste exact error text

**By Project:**
- Current: `/mnt/c/Projects/DevForgeAI2`
- Other: `/mnt/c/Projects/SQLServer`
- All: Show all projects

**By Time Range:**
- Recent: Last 10-20 sessions
- Comprehensive: Last 50-100 sessions
- All: Entire history (~7000+ sessions)

**Use Cases:**

1. **Find incomplete work:**
   ```bash
   /chat-search "/dev STORY-066"
   ```

2. **Locate epic planning:**
   ```bash
   /chat-search "EPIC-010"
   ```

3. **Review QA sessions:**
   ```bash
   /chat-search "/qa"
   ```

4. **Browse recent work:**
   ```bash
   /chat-search
   # Choose "Recent Sessions"
   ```

5. **Debug issues:**
   ```bash
   /chat-search "error: context files missing"
   ```

**Architecture:**

**Command (Direct Implementation - No Skill):**
- Phase 0: Interactive search criteria gathering (AskUserQuestion)
- Phase 1: Direct bash/grep search of history.jsonl
- Phase 2: Format and display results
- Phase 3: Optional resume instructions (AskUserQuestion)
- No skill invocation - simple utility command

**Tools Used:**
- `Bash` - Execute grep/jq searches on history.jsonl
- `Read` - Read search results from temp files
- `AskUserQuestion` - Interactive search criteria and resume selection
- `Grep` - (optional) Alternative to bash grep

**Output:**
- Session listing with IDs, projects, timestamps, message previews
- Resume commands (claude -r <session-id>)
- No file creation (read-only operation)

**Character Budget:** ~11,500 chars (77% of 15K budget) - COMPLIANT

**Execution Time:** 5-60 seconds (depends on result count and history size)

**Error Handling:**
- History file not found → Clear error message
- Invalid JSON → Skip malformed lines, continue
- Permission denied → Suggest chmod fix
- Too many results → Display top N, suggest filtering

**Related:**
- `claude -r` - Resume session by ID
- `claude -r [sessionId]` - Resume specific session
- `claude --fork-session -r [sessionId]` - Fork from session
- All DevForgeAI commands create searchable sessions

---

### /research [topic] | --resume ID | --search query | --list | --category TYPE

**Purpose:** Capture and persist research findings across sessions

**Category:** Research

**Invokes:** `spec-driven-research` skill

**Modes:**
- **New Research:** `/research "topic"` - Start new research session
- **Resume:** `/research --resume RESEARCH-001` - Continue existing research
- **Search:** `/research --search "query"` - Search research documents
- **List:** `/research --list` - Display all research
- **Filter:** `/research --list --category competitive` - Filter by category

**Workflow (New Research):**
1. **Phase 0:** Initialize (generate ID, load index, check duplicates)
2. **Phase 1:** Topic Definition (interactive: category, research questions)
3. **Phase 2:** Research Execution (web searches by category strategy)
4. **Phase 3:** Findings Synthesis (theme extraction, recommendations)
5. **Phase 4:** Documentation (write document, update index)
6. **Phase 5:** Cross-Reference (link to epics, stories, ADRs)

**Categories:**
| Category | Description | Search Strategy |
|----------|-------------|-----------------|
| `competitive` | Competitor analysis | Features, pricing, reviews, comparisons |
| `technology` | Library/tool evaluation | GitHub health, docs, benchmarks, adoption |
| `market` | Industry trends | Statistics, surveys, pain points, trends |
| `integration` | External APIs/services | Docs, SDKs, rate limits, examples |
| `architecture` | Design patterns | Best practices, trade-offs, examples |

**Examples:**
```bash
# Start new research
/research "AWS Kiro Competitive Analysis"

# Resume existing
/research --resume RESEARCH-001

# Search for specific topic
/research --search "token efficiency"

# List all research
/research --list

# Filter by category
/research --list --category technology
```

**Output:**
- Research document: `devforgeai/specs/research/RESEARCH-NNN-{slug}.research.md`
- Research index updated: `devforgeai/specs/research/research-index.md`
- Assets folder (optional): `devforgeai/specs/research/RESEARCH-NNN/`

**Document Structure:**
```markdown
---
id: RESEARCH-001
title: "Topic Title"
category: competitive
status: complete
created: 2026-01-18
review_by: 2026-07-18
sources_count: 15
related_epics: [EPIC-045]
tags: [tag1, tag2]
---

# RESEARCH-001: Topic Title

## Executive Summary
## Research Questions
## Key Findings (with evidence, confidence levels)
## Recommendations (prioritized, actionable)
## Sources (properly cited)
## Related Work
## Change Log
```

**Key Features:**
- **Persistent knowledge:** Survives session restarts
- **Queryable:** Search and list existing research
- **Cross-referenced:** Links to epics, stories, ADRs
- **Staleness tracking:** 6-month review reminders
- **Evidence-based:** All findings cite sources

**Architecture (2026-01-18):**

**Command (80 lines - Lean Orchestration):**
- Argument parsing and mode detection
- Skill invocation with context markers
- Result display

**Skill (spec-driven-research - Comprehensive Research with Anti-Skip Enforcement):**
- 7-phase workflow with Execute-Verify-Record enforcement
- Category-specific search strategies
- Interactive topic definition
- Citation standards enforcement
- Cross-reference management

**Reference Files (Progressive Loading):**
- research-workflow.md (~760 lines)
- citation-standards.md (~160 lines)
- search-strategies.md (~310 lines)
- assets/templates/research-template.md (~63 lines)

**Token Efficiency:**
- Command: ~1K tokens
- Skill: ~40K tokens (isolated context)
- References: ~10K tokens (loaded progressively)

**Character Budget:** ~2,500 chars (17% of 15K limit) - COMPLIANT

**Related:**
- `/ideate` - Transform research into requirements
- `/create-epic` - Create epic from research findings
- internet-sleuth subagent - Deep web research automation

**Created:** 2026-01-18

---

### /insights [query-type] [options]

**Purpose:** Session data mining for workflow patterns, errors, and decisions

**Invokes:** `devforgeai-insights` skill → `session-miner` subagent

**Query Types:**
| Type | Description | Example |
|------|-------------|---------|
| `dashboard` | High-level session metrics | `/insights` |
| `workflows` | TDD cycle analysis | `/insights workflows` |
| `errors` | Error categorization | `/insights errors` |
| `decisions` | Plan file indexing | `/insights decisions "auth"` |
| `story-specific` | Story workflow history | `/insights story STORY-XXX` |
| `command-patterns` | N-gram command sequences | `/insights command-patterns` |

**Example:**
```bash
/insights                        # Dashboard overview
/insights workflows --last 30    # Workflow analysis
/insights story STORY-057        # Story-specific insights
```

**Created:** 2026-01-18 (EPIC-034)

---

### /resume-dev STORY-ID [phase]

**Purpose:** Resume TDD workflow from specific phase when previous `/dev` was incomplete

**Invokes:** `spec-driven-dev` skill with phase override

**Example:**
```bash
/resume-dev STORY-057 2     # Resume from Phase 2 (Implementation)
/resume-dev STORY-057       # Auto-detect resumption point
```

**Valid Phases:**
- 0 = Pre-Flight Validation
- 1 = Red Phase (Test Generation)
- 2 = Green Phase (Implementation)
- 3 = Refactor Phase
- 4 = Integration Testing

**Created:** 2026-01-04 (RCA-013 REC-5)

---

### /worktrees [--help]

**Purpose:** List and manage Git worktrees for parallel story development

**Invokes:** `git-worktree-manager` subagent

**Example:**
```bash
/worktrees           # List all worktrees
/worktrees --help    # Show help
```

**Output:**
- Worktree list with story associations
- Disk usage per worktree
- Age and status indicators
- Cleanup recommendations

**Created:** 2026-01-18 (EPIC-010)

---

### /validate-epic-coverage [EPIC-ID]

**Purpose:** Validate epic-to-story coverage and report gaps

**Example:**
```bash
/validate-epic-coverage           # Validate all epics
/validate-epic-coverage EPIC-015  # Validate single epic
```

**Output:**
- Features with/without stories
- Coverage percentage
- Suggested `/create-story` commands for gaps

---

### /validate-stories [options]

**Purpose:** Validate existing stories against constitutional context files

**Example:**
```bash
/validate-stories                    # Validate all stories
/validate-stories --story STORY-XXX  # Validate single story
```

---

### /create-missing-stories EPIC-ID

**Purpose:** Create stories for all detected coverage gaps in an epic

**Invokes:** `spec-driven-stories` skill (batch mode)

**Example:**
```bash
/create-missing-stories EPIC-015
```

---

### /recommendations-triage [options]

**Purpose:** Triage AI-generated framework improvement recommendations into stories

**Example:**
```bash
/recommendations-triage                    # Triage all recommendations
/recommendations-triage --priority high    # Filter by priority
```

---

### /setup-github-actions [options]

**Purpose:** Create GitHub Actions CI/CD workflows for DevForgeAI projects

**Output:**
- 4 workflow files in `.github/workflows/`
- 2 config files

---

### /devforgeai-validate [options]

**Purpose:** Validate DevForgeAI installation and configuration

**Example:**
```bash
/devforgeai-validate           # Validate installation
/devforgeai-validate --fix     # Auto-fix issues
```

---

### Feedback System Commands

**7 commands for feedback capture, search, and portability:**

| Command | Purpose |
|---------|---------|
| `/feedback` | Manual feedback trigger with context |
| `/feedback-config` | View/edit feedback configuration |
| `/feedback-search` | Search feedback history with filters |
| `/feedback-reindex` | Rebuild feedback session index |
| `/export-feedback` | Export sessions to ZIP package |
| `/import-feedback` | Import sessions from ZIP package |
| `/feedback-export-data` | Export feedback data with selection criteria |

**Example:**
```bash
/feedback-search --type=ai-analysis --priority=high
/export-feedback --story STORY-057
/feedback-export-data --severity high --status open
```

---

### /feedback-export-data

**Description:** Export feedback data with selection criteria (STORY-020 implementation)
**Usage:** `/feedback-export-data [--format] [--date-range] [--story-ids] [--severity] [--status]`
**Category:** Feedback System

**Options:**
- `--format`: Output format (json, csv, markdown)
- `--date-range`: Filter by date range (e.g., `2026-01-01:2026-02-01`)
- `--story-ids`: Filter by story IDs (e.g., `STORY-020,STORY-021`)
- `--severity`: Filter by severity (critical, high, medium, low)
- `--status`: Filter by status (open, resolved, deferred)

**Note:** For ZIP package exports with sanitization, see `/export-feedback`

**Examples:**
```bash
/feedback-export-data --severity high --status open
/feedback-export-data --story-ids STORY-020 --format csv
/feedback-export-data --date-range 2026-01-01:2026-02-24
```

**Output:**
- Filtered feedback data in requested format
- Export summary with record counts

---

### /collaborate

**Description:** Generate cross-AI collaboration document for sharing issues with external LLMs (Gemini, ChatGPT, etc.)
**Usage:** `/collaborate [issue-description] [--target=AI]`
**Invokes:** `spec-driven-collaboration` skill
**Category:** Collaboration

**Workflow:**
1. Capture issue description and relevant context
2. Identify target AI platform (Gemini, ChatGPT, etc.)
3. Generate self-contained collaboration document
4. Write document to `tmp/` with structured slug

**Options:**
- `--target`: Target AI platform (gemini, chatgpt, copilot, etc.)

**Examples:**
```bash
/collaborate "Debugging STORY-057 implementation failure"
/collaborate "Architecture review for auth system" --target=gemini
```

**Output:**
- Self-contained collaboration document in `tmp/collaborate-{ai}-{slug}-{date}.md`
- Document includes: issue description, context, relevant code excerpts, questions

---

### Audit Commands

**7 specialized audit commands:**

| Command | Purpose | Invokes |
|---------|---------|---------|
| `/audit-deferrals` | Audit deferred work for violations | deferral-validator |
| `/audit-alignment` | Validate configuration layer alignment | alignment-auditor |
| `/audit-budget` | Audit command character budgets | pattern-compliance-auditor |
| `/audit-hooks` | Audit hook registry | None (utility) |
| `/audit-hybrid` | Detect hybrid command/skill violations | None (haiku utility) |
| `/audit-orphans` | Scan for orphaned files and sync drift | None (utility) |
| `/audit-w3` | Detect W3 violations (auto-skill chaining) | None (utility) |

### Framework Versioning

| Command | Purpose | Invokes |
|---------|---------|---------|
| `/prompt-version` | Prompt versioning with SHA-256 integrity verification | None (standalone) |
</command_details>

---

<integration_patterns>
## Integration Patterns

Commands integrate with skills using the Skill tool:

<example>
```
Skill(command="spec-driven-dev --story=STORY-001")
Skill(command="spec-driven-qa --mode=deep --story=STORY-001")
Skill(command="spec-driven-release --story=STORY-001")
```
</example>

This creates **context isolation** - each skill operates in a separate context window, keeping main conversation efficient.
</integration_patterns>
