# ADR-001: Retrospective Feedback System Architecture

**Status:** Proposed
**Date:** 2025-11-07
**Decision Makers:** DevForgeAI Framework Maintainers
**Related Epics:** EPIC-002, EPIC-003, EPIC-004, EPIC-005

---

## Context

DevForgeAI framework currently lacks a systematic mechanism for users to provide feedback on their experiences with commands, skills, and subagents. When operations succeed or fail, users have no structured way to:
- Reflect on what went well or poorly
- Communicate issues to framework maintainers
- Learn from their experiences through guided reflection
- Contribute to framework improvement

This results in:
- Lost improvement opportunities (issues not documented)
- Repeated frustrations (same issues affect multiple users)
- Slow framework evolution (maintainers lack insight into real-world usage)
- Missed learning opportunities (users don't reflect on workflows)

---

## Decision

Implement a **Retrospective Feedback System** as a comprehensive DevForgeAI framework enhancement, consisting of:

1. **Post-operation retrospective conversations** using AskUserQuestion (5-10 questions)
2. **Context-aware template system** (adapts to operation type and success/failure)
3. **YAML-based configuration** (`devforgeai/config/feedback.yaml`)
4. **File-based storage with searchable indexing** (`devforgeai/feedback/`)
5. **Event-driven hooks** (TodoWrite completion triggers)
6. **Cross-project export/import** (feedback portability for maintainer communication)

**Architecture Tier:** Tier 3 (Complex Platform with Clean Architecture)
**Complexity Score:** 44/60
**Estimated Effort:** 100-160 story points (10-16 sprints)

---

## Rationale

### Why Event-Driven Hooks (vs Manual Triggering)?

**Considered Alternatives:**
- **Alternative A:** Manual `/feedback` command (users trigger explicitly)
  - **Pros:** Simpler implementation (Tier 2), user control
  - **Cons:** Relies on user remembering, feedback often forgotten, incomplete data

- **Alternative B:** Automatic prompts after every operation
  - **Pros:** Maximum feedback collection
  - **Cons:** Intrusive, token waste, user fatigue

- **Alternative C:** Event-driven hooks with configurable triggers ✅ **CHOSEN**
  - **Pros:** Balances automation with user control, configurable (always/failures/never), non-invasive integration
  - **Cons:** More complex implementation (Tier 3)

**Decision:** Event-driven hooks with failures-only default mode
**Rationale:**
- Users get feedback prompts when most valuable (after failures)
- Configuration allows customization (disable, change triggers)
- Non-invasive (hooks don't modify existing code)
- Token-efficient (failures-only ~3% budget overhead vs always ~11%)

### Why File-Based Storage (vs Database)?

**Considered Alternatives:**
- **Alternative A:** SQLite database
  - **Pros:** Structured queries, relational data, ACID guarantees
  - **Cons:** Adds dependency, violates DevForgeAI simplicity, not Git-friendly

- **Alternative B:** In-memory only (no persistence)
  - **Pros:** Simplest, no file I/O
  - **Cons:** Feedback lost after session, no historical analysis

- **Alternative C:** File-based with JSON index ✅ **CHOSEN**
  - **Pros:** No dependencies, Git-compatible, simple, aligns with DevForgeAI patterns
  - **Cons:** Limited query performance (acceptable for <10K sessions)

**Decision:** Markdown files in `devforgeai/feedback/sessions/` + JSON index
**Rationale:**
- Aligns with DevForgeAI's Markdown-first design philosophy
- Git-compatible (can version control feedback if desired)
- No external dependencies required
- Searchable via JSON index (sufficient performance for expected volume)
- Human-readable (users can manually review feedback files)

### Why YAML Configuration (vs JSON or Code)?

**Considered Alternatives:**
- **Alternative A:** JSON configuration (`devforgeai/config/feedback.json`)
  - **Pros:** Widely supported, schema validation
  - **Cons:** Less human-readable (no comments), verbose syntax

- **Alternative B:** Code-based configuration (JavaScript/Python config file)
  - **Pros:** Programmatic, dynamic rules
  - **Cons:** Violates framework-agnostic principle, requires execution environment

- **Alternative C:** YAML configuration ✅ **CHOSEN**
  - **Pros:** Human-readable, supports comments, language-neutral, schema validation available
  - **Cons:** Requires YAML parser (acceptable)

**Decision:** `devforgeai/config/feedback.yaml`
**Rationale:**
- Human-readable (users can easily edit)
- Supports comments (inline documentation)
- Language-neutral (works across .NET, Node.js, Python, etc.)
- Consistent with DevForgeAI patterns (YAML frontmatter used extensively)

### Why Tier 3 Architecture (vs Tier 2 MVP)?

**Considered Alternatives:**
- **Alternative A:** Tier 2 (Modular Monolith)
  - **Pros:** Simpler, faster to implement
  - **Cons:** Event hooks inherently complex, would accumulate debt, hard to extend

- **Alternative B:** Tier 3 (Clean Architecture) ✅ **CHOSEN**
  - **Pros:** Proper separation of concerns, extensible, maintainable
  - **Cons:** More upfront effort (10-16 sprints vs 6-8)

**Decision:** Tier 3 with Clean Architecture from start
**Rationale:**
- Event-driven hooks are inherently Tier 3 complexity
- Framework enhancement deserves proper architecture (avoid technical debt)
- 4-6 month timeline accommodates Tier 3 effort
- User explicitly chose "build it right from start"

---

## Architecture Design

### Clean Architecture Layers

**Layer 1: Presentation (Slash Commands)**
```
.claude/commands/feedback/
├── feedback.md           # /feedback [operation-name]
├── feedback-config.md    # /feedback-config [action]
├── feedback-search.md    # /feedback-search [filters]
└── export-feedback.md    # /export-feedback [options]
```

**Layer 2: Application (Feedback Skill)**
```
.claude/skills/devforgeai-feedback/
├── SKILL.md              # Orchestration logic
├── references/
│   ├── conversation-patterns.md      # Question banks by operation type
│   ├── template-rendering-guide.md   # Template engine logic
│   ├── hook-integration-guide.md     # Event hook patterns
│   └── storage-indexing-guide.md     # Persistence patterns
└── templates/
    ├── command-success-template.md
    ├── command-failure-template.md
    ├── skill-success-template.md
    ├── skill-failure-template.md
    ├── subagent-success-template.md
    └── subagent-failure-template.md
```

**Layer 3: Domain (Feedback Rules & Logic)**
- Trigger evaluation (enabled? matches rules?)
- Skip pattern detection (3+ consecutive → suggest disable)
- Template selection (operation type + success/failure)
- Sanitization rules (export data cleaning)

**Layer 4: Infrastructure (File System & Hooks)**
```
devforgeai/feedback/
├── sessions/                     # Feedback session files
│   ├── 2025-11-07T10-30-00-command-dev-success.md
│   ├── 2025-11-07T11-15-30-skill-qa-failure.md
│   └── ...
├── index.json                    # Searchable metadata index
├── skip-tracking.json            # Skip pattern tracking
└── exported/                     # Export packages
    └── devforgeai-feedback-export-{timestamp}.zip
```

### Component Interactions

```
User runs: /dev STORY-042
  ↓
devforgeai-development skill executes TDD
  ↓
TodoWrite marks final todo "completed" ← **HOOK TRIGGER POINT**
  ↓
Event Hook (Infrastructure Layer):
  - Read config: feedback.enabled? trigger.mode matches?
  - Extract context: operation type/name/args, TodoWrite list, errors, performance
  ↓
devforgeai-feedback skill (Application Layer):
  - Select question bank (Domain: operation type + success/failure)
  - Conduct retrospective (Presentation: AskUserQuestion × 5-10)
  - Render template (Domain: field mapping)
  - Persist feedback (Infrastructure: write file, update index)
  ↓
Control returns to user
```

---

## Consequences

### Positive Consequences

**For Users:**
- ✅ **Structured learning:** Guided reflection improves understanding
- ✅ **Better debugging:** Failure retrospectives capture context for issue resolution
- ✅ **Contribution channel:** Users can easily provide feedback to maintainers
- ✅ **Full control:** Configurable (enable/disable, change triggers, customize templates)

**For Framework Maintainers:**
- ✅ **Data-driven improvements:** Structured feedback enables pattern detection
- ✅ **User insight:** Real-world usage data informs prioritization
- ✅ **Quality assurance:** Systematic feedback catches issues early
- ✅ **Cross-project learning:** Export/import enables feedback aggregation

**For Framework:**
- ✅ **Continuous improvement culture:** Feedback embedded in workflow
- ✅ **Zero duplication:** Centralized feedback logic (not 40 duplicate implementations)
- ✅ **Extensible:** Clean Architecture supports future enhancements
- ✅ **Framework-agnostic:** Works for any project technology stack

### Negative Consequences

**Token Budget Impact:**
- ⚠️ 2,000-5,000 tokens per feedback session
- ⚠️ 3% of 1M budget if failures-only mode (acceptable)
- ⚠️ 11% if enabled for all operations (high, but user-controllable)
- **Mitigation:** Failures-only default, skip tracking, user can disable

**Implementation Effort:**
- ⚠️ 100-160 story points (significant investment)
- ⚠️ 10-16 sprints (3-8 months effort)
- **Mitigation:** Phased epic implementation, incremental value delivery

**Complexity:**
- ⚠️ Event-driven hooks add architectural complexity
- ⚠️ 4-layer Clean Architecture vs simpler alternatives
- **Mitigation:** Proper architecture prevents technical debt long-term

**Adoption Uncertainty:**
- ⚠️ Users may find retrospectives intrusive
- ⚠️ Skip rate unknown (could waste tokens)
- **Mitigation:** Disabled by default (opt-in), skip pattern tracking

### Trade-offs Accepted

**Complexity vs Correctness:** Chosen Tier 3 architecture over Tier 2 MVP
- **Why:** Event hooks inherently complex, worth proper architecture
- **Impact:** 10-16 sprints instead of 6-8 sprints
- **Benefit:** Extensible, maintainable, zero technical debt

**Token Overhead vs User Value:** Accepted 3% token budget overhead
- **Why:** Continuous improvement feedback worth the cost
- **Impact:** ~30K-50K tokens per day (failures-only mode)
- **Benefit:** Data-driven framework improvements, user learning

**File-Based vs Database:** Chosen file-based storage
- **Why:** Aligns with DevForgeAI simplicity, no dependencies
- **Impact:** Limited query performance (acceptable for <10K sessions)
- **Benefit:** Git-compatible, human-readable, zero licensing costs

---

## Alternatives Considered

### Alternative 1: Simple Post-Operation Prompt (Tier 1)

**Description:** Single AskUserQuestion after each operation: "Any feedback?"

**Pros:**
- Simplest implementation (~20 story points)
- Minimal token overhead (~500 tokens/session)
- Fast to deliver (2-3 sprints)

**Cons:**
- Unstructured feedback (hard to analyze)
- Low engagement (generic question ignored)
- No configuration (always on or always off)
- No templates (raw text feedback)

**Why Rejected:** Insufficient structure for actionable insights, low user engagement expected

### Alternative 2: Periodic Survey System (Tier 2)

**Description:** Weekly/monthly survey prompts users for feedback batch

**Pros:**
- Less intrusive (1 conversation per week vs 10 per day)
- Lower token overhead (amortized)
- Batch context (reflect on week's work)

**Cons:**
- Delayed feedback (issues forgotten by survey time)
- Separated from operation context (user forgets specifics)
- Still requires configuration, templates, storage (Tier 2+ anyway)

**Why Rejected:** Context loss unacceptable (users forget details), defeats learning goal

### Alternative 3: Manual /feedback Command Only (Tier 2 Simplified)

**Description:** Users run `/feedback` explicitly when they want to provide feedback

**Pros:**
- User-initiated (no intrusion)
- Simpler than hooks (Tier 2 complexity)
- Token-efficient (users opt-in per session)

**Cons:**
- Relies on user memory (often forgotten)
- Low adoption expected (extra step after work)
- Missing failure cases (users don't reflect after failures)

**Why Rejected:** Low expected adoption, misses failures (most valuable feedback opportunity)

### Alternative 4: Chosen Solution - Event-Driven Hooks with Full Configuration (Tier 3)

**Description:** Automatic hooks with comprehensive configuration, templates, storage, export

**Pros:**
- ✅ Automatic (users don't forget)
- ✅ Context-aware (captures operation specifics)
- ✅ Configurable (users control behavior)
- ✅ Structured (templates enable analysis)
- ✅ Portable (export for maintainers)

**Cons:**
- ⚠️ Complex (Tier 3 architecture required)
- ⚠️ Token overhead (3% budget in failures-only mode)
- ⚠️ Implementation effort (100-160 story points)

**Why Chosen:** Best balance of automation, user control, and actionable insights

---

## Implementation Plan

### Epic Sequence

**Epic 1: Feedback Capture & Interaction (P0) - Sprints 1-5**
- Feature 1.1: Post-Operation Retrospective Conversation
- Feature 1.2: Adaptive Questioning Engine
- Feature 1.3: Skip Pattern Tracking

**Epic 2: Template & Configuration System (P0) - Sprints 4-7**
- Feature 2.1: Feedback Template Engine
- Feature 2.2: Configuration Management
- Feature 2.3: Template Customization

**Epic 3: Storage & Indexing (P0) - Sprints 6-9**
- Feature 3.1: Feedback File Persistence
- Feature 3.2: Searchable Metadata Index
- Feature 3.3: Cross-Project Export/Import

**Epic 4: Framework Integration (P0) - Sprints 10-16**
- Feature 4.1: Event-Driven Hook System
- Feature 4.2: Operation Lifecycle Integration
- Feature 4.3: Feedback CLI Commands

**Dependencies:**
- Epic 2 depends on Epic 1 (question bank structure)
- Epic 3 depends on Epic 2 (template format)
- Epic 4 depends on all (integration is final phase)

### Technology Decisions

**Feedback Skill Implementation:**
- Format: Markdown (`.claude/skills/devforgeai-feedback/SKILL.md`)
- Size Target: <1,000 lines (progressive disclosure via references/)
- model: haiku (requires AskUserQuestion, complex orchestration)

**Configuration:**
- Format: YAML (`devforgeai/config/feedback.yaml`)
- Schema Validation: JSON Schema for YAML validation
- Default: Disabled (opt-in feature)

**Templates:**
- Format: Markdown with YAML frontmatter
- Location: `.claude/skills/devforgeai-feedback/templates/`
- Count: 6 templates (command/skill/subagent × success/failure)

**Storage:**
- Format: Markdown files with YAML frontmatter
- Location: `devforgeai/feedback/sessions/`
- Naming: `{timestamp}-{operation-type}-{status}.md`
- Index: JSON (`devforgeai/feedback/index.json`)

**Event Hooks:**
- Trigger: TodoWrite completion events
- Implementation: Hook detection in feedback skill (reads TodoWrite final status)
- Fallback: Manual `/feedback` command if hooks disabled

### Compliance with Existing Constraints

**Architecture Constraints:** ✅ COMPLIANT
- Three-layer architecture: Commands → Feedback Skill → Subagents (if needed)
- Single responsibility: devforgeai-feedback skill handles feedback ONLY
- No circular dependencies
- Skills can invoke other skills (feedback skill invokable by dev/qa/release skills)

**Tech Stack Constraints:** ✅ COMPLIANT
- Markdown for all documentation (SKILL.md, templates, session files)
- YAML for configuration (frontmatter pattern used throughout framework)
- JSON for index (structured data exchange, not documentation)
- No language-specific code (framework-agnostic)

**Source Tree Constraints:** ✅ COMPLIANT
- Feedback skill: `.claude/skills/devforgeai-feedback/`
- Feedback commands: `.claude/commands/feedback/`
- Configuration: `devforgeai/config/feedback.yaml`
- Storage: `devforgeai/feedback/`
- Size limits: Commands <500 lines, skill <1,000 lines

**Token Budget Constraints:** ✅ ACCEPTABLE
- Command size: ~200-300 lines (within 500 line limit)
- Skill size: ~800-1,000 lines (at target limit)
- Token overhead: 3% of 1M budget (failures-only mode)
- Progressive disclosure: References loaded on-demand

---

## Enforcement Mechanisms

### Configuration Validation

**Enforced by:** devforgeai-feedback skill on startup

**Validation Rules:**
```yaml
schema:
  enabled: boolean (required)
  trigger:
    mode: enum [always, failures-only, specific-operations, never] (required)
    operations: array of strings (required if mode=specific-operations)
  conversation:
    max-questions: integer 5-15 (required)
    allow-skip: boolean (required)
  skip-tracking:
    enabled: boolean (required)
    threshold: integer 1-10 (required)
  templates:
    default: enum [context-aware, universal] (required)
    custom-fields: array (optional)
```

**Action on Invalid Config:**
- HALT with error message listing validation failures
- Provide corrected config example
- Allow user to fix and retry

### Hook Integration Validation

**Enforced by:** Epic 4 Feature 4.1 implementation

**Validation Rules:**
- Hooks must not modify operation outcomes
- Hook failures must log but not throw to caller
- Hooks must complete within 30s or timeout
- Hooks must check config before execution (no-op if disabled)

**Action on Hook Failure:**
- Log error to `devforgeai/feedback/hook-errors.log`
- Display warning to user (not error)
- Allow operation to complete successfully

### Architectural Compliance Validation

**Enforced by:** context-validator subagent during implementation

**Validation Rules:**
- Feedback skill respects three-layer architecture
- No circular dependencies (feedback skill → X → feedback skill)
- Command size <500 lines
- Skill size <1,000 lines

**Action on Violations:**
- HALT during development with constraint violation message
- Provide remediation steps
- Require fix before story marked "Dev Complete"

---

## Success Metrics

### Feature Adoption

- **Target:** 60%+ of users enable feedback within 30 days
- **Measurement:** Config file analysis across DevForgeAI projects
- **Threshold:** If <40% after 60 days → Re-evaluate value proposition

### Feedback Quality

- **Target:** 80%+ of feedback sessions contain actionable insights
- **Measurement:** Manual review, keyword extraction ("should", "could", "bug")
- **Threshold:** If <60% → Review question bank quality

### Framework Improvement

- **Target:** 5+ enhancements per quarter from user feedback
- **Measurement:** GitHub issues/PRs tagged "user-feedback"
- **Threshold:** If <3 per quarter → Review feedback-to-enhancement pipeline

### Token Efficiency

- **Target:** ≤3% of 1M token budget (failures-only mode)
- **Measurement:** Token usage tracking
- **Threshold:** If >5% → Review conversation length, question count

---

## Review and Update

**Review Schedule:** Quarterly after implementation
**Review Criteria:**
- Adoption metrics meeting targets?
- Token overhead within acceptable range?
- User feedback quality sufficient?
- Framework improvements attributable to feedback?

**Update Triggers:**
- Adoption <40% → Simplify configuration, improve value prop
- Token overhead >5% → Reduce question count, improve skip tracking
- Feedback quality <60% → Revise question bank
- Improvements <3/quarter → Review export process, maintainer workflow

---

## Related Documents

- **Epic Documents:**
  - [EPIC-002: Feedback Capture & Interaction](devforgeai/specs/Epics/EPIC-002-feedback-capture-interaction.epic.md)
  - [EPIC-003: Template & Configuration System](devforgeai/specs/Epics/EPIC-003-template-configuration-system.epic.md)
  - [EPIC-004: Storage & Indexing](devforgeai/specs/Epics/EPIC-004-storage-indexing.epic.md)
  - [EPIC-005: Framework Integration](devforgeai/specs/Epics/EPIC-005-framework-integration.epic.md)

- **Requirements:**
  - [Retrospective Feedback System Requirements](devforgeai/specs/requirements/retrospective-feedback-system-requirements.md)

- **Context Files:**
  - [Architecture Constraints](devforgeai/context/architecture-constraints.md)
  - [Tech Stack](devforgeai/context/tech-stack.md)
  - [Source Tree](devforgeai/context/source-tree.md)

---

**Status:** Proposed (awaiting approval before implementation)
**Next Steps:** Validate design, create stories for Epic 1, begin Sprint 1 planning
