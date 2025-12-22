# Retrospective Feedback System - Requirements Specification

**Project:** DevForgeAI Framework Enhancement
**Feature:** Post-Operation Retrospective Feedback System
**Created:** 2025-11-07
**Status:** Requirements Complete - Ready for Architecture
**Complexity:** Tier 3 (Complex Platform) - Score 44/60

---

## Executive Summary

This document specifies requirements for a comprehensive retrospective feedback system that enables DevForgeAI users to reflect on operations (commands, skills, subagents) through structured conversations, capturing insights that improve both individual user learning and overall framework quality.

**Business Value:**
- **For Users:** Enhanced learning through structured reflection, improved understanding of DevForgeAI workflows
- **For Framework Maintainers:** Systematic insight collection enabling data-driven enhancements, bug fixes, and UX improvements
- **For Projects:** Continuous improvement culture embedded in development workflow

**Scope:** 4 epics, 12 features, 100-160 story points (10-16 sprints estimated)

---

## Problem Statement

DevForgeAI currently lacks a systematic mechanism for users to provide feedback on their experiences with commands, skills, and subagents. When something goes wrong or could be improved, users either:
1. Forget the issue by the time they could report it
2. Lack a structured way to communicate the problem
3. Don't have a feedback channel to DevForgeAI maintainers

This results in:
- Lost improvement opportunities (issues not documented)
- Repeated frustrations (same issues affect multiple users)
- Slow framework evolution (maintainers lack insight into real-world usage)

---

## Solution Overview

**Retrospective Feedback System** - A comprehensive, user-configurable feedback collection system that:
1. **Captures insights** through post-operation conversations (5-10 questions via AskUserQuestion)
2. **Structures feedback** using context-aware templates (adapts to operation type and success/failure)
3. **Persists data** to disk with searchable indexing (`devforgeai/feedback/` directory)
4. **Integrates seamlessly** via event-driven hooks at operation completion
5. **Enables cross-project feedback** through export/import for maintainer communication

---

## User Personas

### Primary Persona: DevForgeAI Project User (Sarah, Full-Stack Developer)
- **Role:** Uses DevForgeAI for spec-driven development on her team's SaaS platform
- **Goals:**
  - Understand what went wrong when operations fail
  - Learn DevForgeAI workflows through reflection
  - Contribute feedback to improve framework
- **Pain Points:**
  - Forgets to report issues after resolving them
  - Unsure how to communicate problems to maintainers
  - No visibility into whether feedback is being acted upon

### Secondary Persona: DevForgeAI Framework Maintainer (Alex, OSS Contributor)
- **Role:** Maintains and enhances DevForgeAI framework
- **Goals:**
  - Collect structured feedback from users
  - Identify common pain points and enhancement opportunities
  - Prioritize framework improvements based on data
- **Pain Points:**
  - Ad-hoc feedback hard to aggregate and analyze
  - Unclear which issues affect most users
  - Time-consuming to triage unstructured feedback

---

## Functional Requirements

### Epic 1: Feedback Capture & Interaction

#### FR-1.1: Post-Operation Retrospective Conversation
**Priority:** P0 (Must-Have)

**Description:** After command/skill/subagent completion, trigger interactive retrospective conversation gathering insights on success/failure, UX, and improvement suggestions.

**Acceptance Criteria:**
- AC-1.1.1: Retrospective triggered at operation completion (if enabled in config)
- AC-1.1.2: Conversation consists of 5-10 AskUserQuestion prompts
- AC-1.1.3: Questions cover: success/failure, clarity, ease of use, confusion points, suggestions
- AC-1.1.4: User can skip entire conversation or individual questions
- AC-1.1.5: Feedback captures: operation context (name, args, status), user responses, timestamp, TodoWrite list, error logs

**User Story:**
```
As a DevForgeAI user,
I want to reflect on what just happened after an operation completes,
So that I can learn from the experience and provide feedback to improve the framework.
```

#### FR-1.2: Adaptive Questioning Engine
**Priority:** P0 (Must-Have)

**Description:** Questions adapt based on operation type (command/skill/subagent), success status (pass/fail/partial), and user context (first-time vs repeat).

**Acceptance Criteria:**
- AC-1.2.1: Question bank organized by operation type (11 commands, 8 skills, 21 subagents)
- AC-1.2.2: Success vs failure question variations (different prompts for pass vs fail)
- AC-1.2.3: Dynamic selection based on context (TodoWrite status, error logs, performance metrics)
- AC-1.2.4: Questions limited to 5-10 interactions (balance depth vs user patience)
- AC-1.2.5: Questions follow AskUserQuestion format (header, options, multiSelect)

**User Story:**
```
As a user,
I want questions relevant to what I just did,
So that I'm not answering generic questions that don't apply to my situation.
```

#### FR-1.3: Skip Pattern Tracking
**Priority:** P1 (Should-Have)

**Description:** Track user skip behavior, detect patterns (3+ consecutive skips), suggest disabling feature to reduce token waste.

**Acceptance Criteria:**
- AC-1.3.1: Skip counter tracked per operation type in `devforgeai/feedback/skip-tracking.json`
- AC-1.3.2: Pattern detection: 3+ consecutive skips triggers suggestion
- AC-1.3.3: AskUserQuestion offers: disable feedback, switch to failures-only mode, continue as-is
- AC-1.3.4: User preference stored in config file (`devforgeai/config/feedback.yaml`)
- AC-1.3.5: Skip tracking resets after successful feedback session

**User Story:**
```
As a user,
I don't want to be pestered with feedback prompts if I consistently skip them,
So that the system learns my preferences and reduces friction.
```

---

### Epic 2: Template & Configuration System

#### FR-2.1: Feedback Template Engine
**Priority:** P0 (Must-Have)

**Description:** Context-aware templates structure feedback based on operation type and success status, with automatic field mapping from conversation responses.

**Acceptance Criteria:**
- AC-2.1.1: Template definitions for each operation type (command-template.md, skill-template.md, subagent-template.md)
- AC-2.1.2: Success/failure template variations (different sections for pass vs fail)
- AC-2.1.3: Automatic field mapping (map conversation responses to template fields)
- AC-2.1.4: Template rendering with metadata (timestamp, operation type, status, story ID if applicable)
- AC-2.1.5: Output format: YAML frontmatter + Markdown content
- AC-2.1.6: Templates stored in `.claude/skills/devforgeai-feedback/templates/`

**Template Structure Example:**
```markdown
---
operation: /dev STORY-042
type: command
status: success
timestamp: 2025-11-07T10:30:00Z
story-id: STORY-042
---

# Retrospective: /dev STORY-042

## What Went Well
{User responses}

## What Went Poorly
{User responses}

## Suggestions for Improvement
{User responses}

## Context
- TodoWrite Status: {final status}
- Errors: {Y/N + summary}
- Performance: {execution time, token usage}

## User Sentiment
{1-5 scale}

## Actionable Insights
{Auto-extracted keywords}
```

**User Story:**
```
As a framework maintainer,
I want standardized feedback templates,
So that I can aggregate insights across users and identify patterns.
```

#### FR-2.2: Configuration Management
**Priority:** P0 (Must-Have)

**Description:** YAML-based configuration file controls feedback behavior (enable/disable, trigger rules, template selection).

**Acceptance Criteria:**
- AC-2.2.1: Config file location: `devforgeai/config/feedback.yaml`
- AC-2.2.2: Config structure includes:
  - `enabled: true/false` (master toggle)
  - `trigger.mode: always|failures-only|specific-operations|never`
  - `trigger.operations: [list]` (if mode=specific-operations)
  - `conversation.max-questions: 5-15`
  - `conversation.allow-skip: true/false`
  - `skip-tracking.enabled: true/false`
  - `skip-tracking.threshold: 3` (consecutive skips)
  - `templates.default: context-aware`
- AC-2.2.3: Config validation on read (schema validation)
- AC-2.2.4: Default config auto-generated if missing
- AC-2.2.5: Config accessible via Read tool

**User Story:**
```
As a user,
I want to control when feedback triggers (always, failures-only, never),
So that I can balance feedback value with workflow disruption.
```

#### FR-2.3: Template Customization
**Priority:** P2 (Could-Have)

**Description:** Allow users to define custom template fields and inject custom questions into conversations.

**Acceptance Criteria:**
- AC-2.3.1: Custom field definitions in config YAML
- AC-2.3.2: Custom questions injected at configurable position (after core questions, before suggestions)
- AC-2.3.3: Template inheritance: custom templates extend (not replace) base templates
- AC-2.3.4: Validation: Reject invalid custom field definitions

**User Story:**
```
As a power user,
I want to add custom fields to feedback templates,
So that I can capture project-specific context (e.g., "Project phase", "Team size").
```

---

### Epic 3: Storage & Indexing

#### FR-3.1: Feedback File Persistence
**Priority:** P0 (Must-Have)

**Description:** Save feedback sessions to `devforgeai/feedback/` with timestamp-based naming and atomic writes.

**Acceptance Criteria:**
- AC-3.1.1: Feedback directory: `devforgeai/feedback/sessions/`
- AC-3.1.2: File naming: `{timestamp}-{operation-type}-{status}.md`
- AC-3.1.3: File format: Markdown with YAML frontmatter
- AC-3.1.4: Atomic writes (write to temp, rename to prevent corruption)
- AC-3.1.5: Directory auto-creation if missing
- AC-3.1.6: File permissions: User-readable/writable only (0600)

**User Story:**
```
As a user,
I want my feedback automatically saved,
So that I can review it later and don't lose insights.
```

#### FR-3.2: Searchable Metadata Index
**Priority:** P0 (Must-Have)

**Description:** Maintain searchable index (`devforgeai/feedback/index.json`) with metadata from all feedback sessions.

**Acceptance Criteria:**
- AC-3.2.1: Index file: `devforgeai/feedback/index.json`
- AC-3.2.2: Index structure includes: session ID, timestamp, operation (type/name/args), status, tags, story ID, keywords, file path
- AC-3.2.3: Index update: Append new entry on feedback write (incremental)
- AC-3.2.4: Index rebuild command: `/feedback-reindex`
- AC-3.2.5: Search API: Filter by date range, operation type/name, status, keywords, tags
- AC-3.2.6: Search performance: <1s for 1000+ sessions

**User Story:**
```
As a user,
I want to search "all failed /qa runs in last month",
So that I can identify patterns and recurring issues.
```

#### FR-3.3: Cross-Project Export/Import
**Priority:** P1 (Should-Have)

**Description:** Export feedback into portable package for sharing with DevForgeAI maintainers, with sanitization and import capability.

**Acceptance Criteria:**
- AC-3.3.1: Export command: `/export-feedback [--date-range] [--sanitize]`
- AC-3.3.2: Export package format: `devforgeai-feedback-export-{timestamp}.zip`
- AC-3.3.3: Package contents: `feedback-sessions/` (sanitized if requested), `index.json`, `manifest.json`
- AC-3.3.4: Sanitization rules: Replace story IDs, remove custom field values, remove project-specific context
- AC-3.3.5: Import command: `/import-feedback [file.zip]`
- AC-3.3.6: Import destination: `devforgeai/feedback/imported/{timestamp}/`
- AC-3.3.7: Validation: Reject corrupted or incompatible exports

**User Story:**
```
As a project user,
I want to export my feedback and send it to DevForgeAI maintainers,
So that they can fix issues I encountered.
```

---

### Epic 4: Framework Integration

#### FR-4.1: Event-Driven Hook System
**Priority:** P0 (Must-Have)

**Description:** Centralized hook registration and invocation triggering feedback at operation completion without modifying existing code.

**Acceptance Criteria:**
- AC-4.1.1: Hook registration centralized in `devforgeai-feedback` skill
- AC-4.1.2: Hook trigger points: Commands (after TodoWrite completed), Skills (after return), Subagents (after Task completes)
- AC-4.1.3: Hook invocation checks: Config enabled? Trigger rule matches?
- AC-4.1.4: Hook context extraction: Operation type, status, TodoWrite list, error logs
- AC-4.1.5: Graceful degradation: Hook errors don't break operations
- AC-4.1.6: Hook coverage: 100% commands, 100% skills, 80% subagents (via wrappers)

**User Story:**
```
As a framework maintainer,
I want feedback to trigger automatically after operations,
So users don't have to remember to run /feedback manually.
```

#### FR-4.2: Operation Lifecycle Integration
**Priority:** P0 (Must-Have)

**Description:** Integrate hooks into TodoWrite-based operation tracking, extracting rich context for feedback conversations.

**Acceptance Criteria:**
- AC-4.2.1: Hook extracts TodoWrite context: All todos, final status, execution time
- AC-4.2.2: Hook extracts error context (if failed): Error logs, stack traces, failed todo specifics
- AC-4.2.3: Context passed to retrospective: Pre-populate template metadata, adapt questions
- AC-4.2.4: Operation history update: Append feedback link to story workflow history

**User Story:**
```
As a user,
I want feedback questions to reference what I just did (specific todos),
So that questions are relevant and actionable.
```

#### FR-4.3: Feedback CLI Commands
**Priority:** P0 (Must-Have)

**Description:** User-facing slash commands for interacting with feedback system.

**Acceptance Criteria:**
- AC-4.3.1: `/feedback [operation-name]` - Manual feedback trigger
- AC-4.3.2: `/feedback-config [action]` - View/edit configuration
- AC-4.3.3: `/feedback-search [filters]` - Search feedback history
- AC-4.3.4: `/export-feedback [options]` - Cross-project export
- AC-4.3.5: Each command ≤300 lines (lean orchestration pattern)
- AC-4.3.6: Commands delegate to `devforgeai-feedback` skill (not inline logic)

**User Story:**
```
As a user,
I want to manually trigger feedback if I want to reflect outside normal hooks,
So that I have full control over when feedback happens.
```

---

## Data Model

### Entities

#### 1. FeedbackSession
**Purpose:** Represents a single feedback conversation

**Attributes:**
- `id` (string): Unique identifier (timestamp-based)
- `timestamp` (ISO8601): When feedback was collected
- `operation` (object):
  - `type` (enum): command|skill|subagent
  - `name` (string): /dev, devforgeai-qa, test-automator, etc.
  - `args` (string): Arguments passed to operation
- `status` (enum): success|failure|partial
- `story_id` (string|null): Associated story ID if applicable
- `context` (object):
  - `todos` (array): TodoWrite list
  - `errors` (array): Error logs
  - `performance` (object): Execution time, token usage
- `responses` (object): User answers to questions
- `sentiment` (integer): User satisfaction (1-5 scale)
- `keywords` (array): Auto-extracted actionable terms
- `tags` (array): User-assigned or auto-assigned tags
- `file_path` (string): Path to Markdown file

**Relationships:**
- One feedback session → One operation (1:1)
- One feedback session → Zero or one story (1:0..1)
- One operation → Many feedback sessions (1:N) (over time, repeats)

#### 2. FeedbackTemplate
**Purpose:** Template definition for structuring feedback

**Attributes:**
- `id` (string): Template identifier (command-success, skill-failure, etc.)
- `operation_type` (enum): command|skill|subagent
- `status_variant` (enum): success|failure|partial
- `sections` (array): Template sections (What Went Well, What Went Poorly, Suggestions, Context, Sentiment, Actionable Insights)
- `fields` (array): Field definitions (name, type, prompt, required)

**Relationships:**
- One template → Many feedback sessions (1:N)

#### 3. FeedbackConfiguration
**Purpose:** User-specific feedback settings

**Attributes:**
- `enabled` (boolean): Master toggle
- `trigger_mode` (enum): always|failures-only|specific-operations|never
- `trigger_operations` (array): Specific operations if mode=specific-operations
- `conversation_max_questions` (integer): 5-15
- `conversation_allow_skip` (boolean)
- `skip_tracking_enabled` (boolean)
- `skip_tracking_threshold` (integer): Consecutive skips before suggestion
- `template_default` (enum): context-aware
- `custom_fields` (array): User-defined custom fields

**Relationships:**
- One configuration per project (singleton)

#### 4. FeedbackIndex
**Purpose:** Searchable metadata index

**Attributes:**
- `version` (string): Index schema version
- `last_updated` (ISO8601): Last index update
- `feedback_sessions` (array): Array of session metadata (subset of FeedbackSession for search)

**Relationships:**
- Index references many feedback sessions (1:N)

### Entity Relationships Diagram

```
FeedbackConfiguration (1)
     │
     ▼
FeedbackSession (N)
     │
     ├──► FeedbackTemplate (1)
     ├──► Story (0..1)
     └──► Operation (1)

FeedbackIndex (1) ──references──► FeedbackSession (N)
```

---

## Non-Functional Requirements

### Performance

**NFR-P1: Conversation Response Time**
- Target: <3s from operation completion to first feedback question
- Rationale: User expects immediate feedback prompt after operation
- Measurement: 95th percentile latency

**NFR-P2: Index Search Performance**
- Target: <1s to search across 1000+ feedback sessions
- Rationale: Users need fast access to historical feedback
- Measurement: Query response time for complex filters

**NFR-P3: Token Budget Impact**
- Target: ≤3% of 1M token budget (failures-only mode)
- Rationale: Feedback valuable but shouldn't dominate token usage
- Measurement: Average tokens per session * session frequency

### Scalability

**NFR-S1: Feedback Session Volume**
- Capacity: Support 10,000+ feedback sessions per project
- Rationale: Long-lived projects accumulate years of feedback
- Measurement: Index size, search performance degradation

**NFR-S2: Concurrent User Support**
- Capacity: <100 concurrent users (file-based storage limitation)
- Rationale: DevForgeAI is individual developer tool, not multi-user platform
- Measurement: File lock contention, write conflicts

### Availability

**NFR-A1: Hook Reliability**
- Target: 99.9%+ hook invocations succeed
- Rationale: Hooks cannot break underlying operations
- Measurement: Hook success rate, operation breakage incidents

**NFR-A2: Graceful Degradation**
- Target: 0% operation failures due to feedback system
- Rationale: Feedback is enhancement, not requirement
- Measurement: Incident reports, error logs

### Security

**NFR-SEC1: Data Sanitization**
- Requirement: 100% of exported feedback sanitizes sensitive data (if --sanitize flag used)
- Rationale: Users may share feedback with maintainers, must not leak secrets
- Measurement: Manual audit of sanitized exports

**NFR-SEC2: File Permissions**
- Requirement: Feedback files readable/writable by user only (0600 permissions)
- Rationale: Prevent unauthorized access to user feedback
- Measurement: File permission checks

### Maintainability

**NFR-M1: Code Duplication**
- Target: 0 instances of duplicated feedback logic across framework
- Rationale: Feedback logic centralized in devforgeai-feedback skill
- Measurement: Code analysis, grep for duplicated patterns

**NFR-M2: Command Size Compliance**
- Target: All feedback commands ≤300 lines (lean orchestration pattern)
- Rationale: Maintain DevForgeAI command size standards
- Measurement: Line count per command file

---

## Integration Requirements

### INT-1: DevForgeAI Architecture Compliance
**Requirement:** Feedback system must respect all 6 existing context files
**Validation:**
- Read `devforgeai/specs/context/architecture-constraints.md`
- Verify no violations of three-layer architecture
- Verify single responsibility principle
- Verify progressive disclosure pattern

### INT-2: Framework-Agnostic Design
**Requirement:** Feedback system must work for any technology stack (.NET, Node.js, Python, Go, Java, etc.)
**Validation:**
- No language-specific code in feedback logic
- No language-specific examples in templates
- Configuration in language-neutral format (YAML)

### INT-3: TodoWrite Integration
**Requirement:** Leverage existing TodoWrite pattern for operation tracking
**Validation:**
- Hooks trigger on TodoWrite completion events
- Extract TodoWrite list for context
- No new tracking mechanism required

---

## Constraints

### Technical Constraints

**TC-1: File-Based Storage**
- Limitation: No database allowed (per DevForgeAI simplicity philosophy)
- Implication: File-based storage and JSON index required
- Mitigation: Optimize file I/O, use atomic writes

**TC-2: Context Window Budget**
- Limitation: 1M token budget per conversation
- Implication: Feedback conversations must be token-efficient
- Mitigation: 5-10 question limit, skip tracking, failures-only default

**TC-3: Architecture Dependency Rules**
- Limitation: Subagents cannot invoke skills or commands
- Implication: Subagent feedback requires parent wrapper
- Mitigation: Document limitation, accept 80% subagent coverage

### Business Constraints

**BC-1: Timeline**
- Constraint: 4-6 months target (16-24 weeks)
- Estimated Effort: 10-16 sprints (100-160 story points)
- Assessment: FEASIBLE (within range with good velocity)

**BC-2: Team Capacity**
- Constraint: 1-3 developers (DevForgeAI maintainers)
- Estimated Capacity: 10 points/sprint
- Assessment: FEASIBLE (single developer sufficient)

**BC-3: Budget**
- Constraint: Zero licensing costs, minimal cloud costs
- Assessment: FEASIBLE (file-based storage, no external services)

---

## Risk Register

| ID | Risk | Likelihood | Impact | Mitigation | Level |
|----|------|------------|--------|------------|-------|
| R1 | Event hook complexity | Medium | High | TodoWrite hook approach, graceful degradation | Medium |
| R2 | Token budget overhead | High | Medium | Failures-only default, skip tracking | Low |
| R3 | Adoption resistance | Medium | Medium | Disabled by default, clear value prop | Low |
| R4 | Index corruption | Low | Medium | Atomic updates, /feedback-reindex command | Low |
| R5 | Export file size | Medium | Low | Date range filtering, compression | Low |
| R6 | Sanitization gaps | Medium | High | Conservative defaults, user review prompts | Medium |
| R7 | Circular hook invocation | Low | Critical | Invocation guard, 30s timeout | Low |
| R8 | Subagent hook limitation | High | Medium | Document limitation, accept 80% coverage | Low |

**Overall Risk Assessment:** FEASIBLE with MEDIUM risk level (well-mitigated)

---

## Complexity Assessment

**Total Score:** 44/60
**Architecture Tier:** Tier 3 (Complex Platform)

### Score Breakdown

**Functional Complexity:** 20/20
- User roles: 2 (users, maintainers) = 5 points
- Core entities: 4 (FeedbackSession, Template, Config, Index) = 5 points
- Integrations: 1 (event hooks) = 3 points
- Workflow: State machine (trigger eval, adaptive templates, skip tracking) = 8 points
- **Subtotal capped at 20 points**

**Technical Complexity:** 13/20
- Data volume: <10K feedback sessions = 5 points
- Concurrency: <100 concurrent = 5 points
- Real-time: None (async file writes) = 3 points

**Team/Organizational Complexity:** 8/10
- Team size: 1-3 developers = 3 points
- Distribution: Remote same timezone = 5 points

**Non-Functional Complexity:** 3/10
- Performance: Moderate (<2s acceptable) = 3 points
- Compliance: None = 0 points

### Tier 3 Recommendations

**Architecture Pattern:** Clean Architecture with event-driven hooks
**Layers:**
1. Presentation (slash commands, AskUserQuestion integration)
2. Application (feedback orchestration, template selection, hook coordination)
3. Domain (feedback rules, skip tracking logic, trigger evaluation)
4. Infrastructure (file storage, index management, event hooks)

**Database Strategy:** File-based with searchable JSON index
**Deployment:** Integrated into DevForgeAI framework (no separate deployment)

---

## Success Metrics

### User Engagement Metrics

**M1: Feature Adoption**
- Target: 60%+ of users enable feedback feature within 30 days
- Measurement: Config file analysis across DevForgeAI projects

**M2: Feedback Quality**
- Target: 80%+ of feedback sessions contain actionable insights
- Measurement: Manual review of feedback content, keyword extraction

**M3: User Learning**
- Target: 70%+ of users report improved DevForgeAI understanding through feedback
- Measurement: User survey (optional feature request)

### Framework Improvement Metrics

**M4: Enhancement Implementation**
- Target: 5+ enhancements implemented per quarter from user feedback
- Measurement: GitHub issues/PRs tagged with "user-feedback" source

**M5: Issue Resolution**
- Target: 30-day median time from feedback to issue resolution (for valid bugs)
- Measurement: Timestamp delta between feedback export and issue close

### Technical Performance Metrics

**M6: Hook Reliability**
- Target: 99.9%+ hook invocations succeed
- Measurement: Error logs, operation breakage incidents

**M7: Token Efficiency**
- Target: ≤3% of 1M token budget consumed by feedback (failures-only mode)
- Measurement: Token usage tracking

**M8: Search Performance**
- Target: <1s search response time for 1000+ sessions
- Measurement: Query performance benchmarks

---

## Next Steps

**After Requirements Approval:**

1. **Architecture Phase** (`/create-context retrospective-feedback`)
   - Create 6 context files specific to this enhancement
   - Define technology decisions (Markdown templates, YAML config, JSON index)
   - Document architecture constraints (event hook design, clean architecture layers)
   - Create initial ADR (architecture decision record)

2. **Story Creation** (`/create-story` for each feature)
   - Break down 12 features into 30-50 implementable stories
   - Each story: acceptance criteria, technical spec, DoD checklist
   - Organize by epic for sequential implementation

3. **Sprint Planning** (`/create-sprint Sprint-1`)
   - Select stories for first sprint (Epic 1 foundational features)
   - Estimated: Sprint 1-3 = Epic 1, Sprint 4-7 = Epic 2, Sprint 8-11 = Epic 3, Sprint 12-16 = Epic 4

4. **Development** (`/dev STORY-XXX`)
   - TDD implementation (Red → Green → Refactor → Integration)
   - Context file compliance validation
   - QA validation after each story

---

## Appendix A: Glossary

- **Retrospective:** Structured reflection conversation after operation completion
- **Operation:** Any DevForgeAI command, skill, or subagent invocation
- **Hook:** Event-driven trigger that invokes feedback system at operation completion
- **Template:** Structured format for organizing feedback content
- **Sanitization:** Process of removing sensitive data before export
- **Skip Pattern:** User behavior of consistently skipping feedback prompts
- **Adaptive Questioning:** Dynamic question selection based on operation context
- **TodoWrite:** DevForgeAI's task tracking tool used to monitor operation lifecycle

---

## Appendix B: Related Documents

- Epic Documents:
  - `devforgeai/specs/Epics/EPIC-002-feedback-capture-interaction.epic.md`
  - `devforgeai/specs/Epics/EPIC-003-template-configuration-system.epic.md`
  - `devforgeai/specs/Epics/EPIC-004-storage-indexing.epic.md`
  - `devforgeai/specs/Epics/EPIC-005-framework-integration.epic.md`

- DevForgeAI Context Files:
  - `devforgeai/specs/context/architecture-constraints.md` (compliance validation)
  - `devforgeai/specs/context/tech-stack.md` (framework implementation constraints)
  - `devforgeai/specs/context/anti-patterns.md` (patterns to avoid)

- Tier 3 Planning (Future Reference):
  - `devforgeai/specs/enhancements/retrospective-feedback-tier3-roadmap.md` (to be created)

---

**END OF REQUIREMENTS SPECIFICATION**

**Status:** ✅ COMPLETE - Ready for `/create-context` and architecture phase
**Next Command:** `/create-context retrospective-feedback-system`
