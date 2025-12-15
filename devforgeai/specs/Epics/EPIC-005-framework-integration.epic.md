---
id: EPIC-005
title: Framework Integration
business-value: Seamlessly integrate feedback system into DevForgeAI's 3-layer architecture (commands → skills → subagents) through event-driven hooks, enabling automatic feedback triggering without code duplication across 11 commands, 8 skills, 21 subagents
status: Planning
priority: High
complexity-score: 44
architecture-tier: Tier 3 (Complex Platform)
created: 2025-11-07
estimated-points: 29-46
target-sprints: 3-5
dependencies:
  - EPIC-002 (all features - conversation system must exist)
  - EPIC-003 Feature 2.2 (config management - hooks need config to determine when to trigger)
  - EPIC-004 Feature 3.1 (storage - hooks persist feedback)
---

# Framework Integration

## Business Goal

Make retrospective feedback a **native part of DevForgeAI's operation lifecycle** by integrating event-driven hooks at operation completion points, eliminating manual feedback triggering and ensuring consistent feedback opportunities across all framework components.

**Success Metrics:**
- Hook coverage: 100% of DevForgeAI operations (11 commands, 8 skills, 21 subagents) support feedback hooks
- Hook reliability: 99.9%+ hook invocations succeed without breaking underlying operations
- Zero code duplication: Feedback logic centralized in devforgeai-feedback skill, not duplicated across 40 components
- User adoption: 80%+ of enabled users receive feedback prompts at appropriate times (failures-only mode)

## Features

### Feature 4.1: Event-Driven Hook System
**Description:** Centralized hook registration and invocation system that triggers feedback conversations at operation completion without modifying existing command/skill/subagent code.

**Story:** STORY-018

**User Stories (high-level):**
1. As a framework maintainer, I want feedback to trigger automatically after operations, so users don't have to remember to run `/feedback` manually
2. As a maintainer, I want hook failures to be graceful (no broken workflows), so feedback system can't break DevForgeAI
3. As a user, I want feedback to appear seamlessly, without noticing "hook injection" complexity

**Acceptance Criteria:**
- Hook registration centralized in `devforgeai-feedback` skill
- Hook trigger points:
  - Commands: After final TodoWrite status = "completed" (or "failed")
  - Skills: After skill returns control to caller
  - Subagents: After Task tool completes
- Hook invocation mechanism:
  - Check config: Is feedback enabled? Does trigger rule match?
  - Extract context: Operation type, status, TodoWrite list, error logs
  - Invoke retrospective conversation (Epic 2)
  - Persist feedback (Epic 4)
- Graceful degradation:
  - Hook errors logged but don't throw to caller
  - Operation completes successfully even if hook fails
  - User notified of hook failure via warning (not error)
- Hook registry:
  ```json
  {
    "hooks": [
      {
        "operation-pattern": "/dev *",
        "trigger": "on-completion",
        "enabled": true
      },
      {
        "operation-pattern": "devforgeai-qa",
        "trigger": "on-failure",
        "enabled": true
      }
    ]
  }
  ```

**Technical Implementation Options:**
1. **TodoWrite Hook** (Recommended): Intercept TodoWrite completion events
   - **Pros:** Non-invasive, leverages existing pattern, framework-wide coverage
   - **Cons:** Requires TodoWrite in all operations (already standard)
2. **Explicit Hook Calls:** Add `invoke_feedback_hook()` to each command/skill
   - **Pros:** Explicit, easy to debug
   - **Cons:** Code duplication, maintenance burden (40 files to update)
3. **Decorator Pattern:** Wrap Skill/Task invocations
   - **Pros:** Centralized, automatic
   - **Cons:** Complex implementation, may interfere with context isolation

**Recommended:** TodoWrite Hook approach

**Estimated Effort:** Large (13-20 story points)

### Feature 4.2: Operation Lifecycle Integration
**Description:** Integrate feedback hooks into DevForgeAI's TodoWrite-based operation tracking, extracting rich context (todos, status, errors) for feedback conversations.

**Story:** STORY-019

**User Stories (high-level):**
1. As a user, I want feedback questions to reference what I just did (specific todos), not generic "how did it go?"
2. As a framework maintainer, I want feedback to capture operation context automatically (no manual extraction)
3. As a user, I want my operation history to link to feedback sessions, so I can correlate work with reflections

**Acceptance Criteria:**
- Hook extracts TodoWrite context:
  - All todos (content, status, activeForm)
  - Final status (all completed? any failed?)
  - Execution time (start to end)
- Hook extracts error context (if status = failed):
  - Error logs from last operation
  - Stack traces (sanitized for user display)
  - Failed todo specifics
- Context passed to retrospective conversation:
  - Pre-populate template metadata
  - Adapt questions based on context (e.g., ask about specific failed todo)
- Operation history update:
  - Append feedback link to story workflow history (if story-based operation)
  - Example: `STORY-042.story.md` → "Workflow History" section → "[Feedback: 2025-11-07T10:30](.devforgeai/feedback/sessions/...)"

**Estimated Effort:** Medium (8-13 story points)

### Feature 4.3: Feedback CLI Commands
**Description:** User-facing slash commands for interacting with feedback system (manual trigger, config management, search, export).

**Story:** STORY-020

**User Stories (high-level):**
1. As a user, I want to manually trigger feedback if I want to reflect outside normal hooks
2. As a user, I want to view/edit my feedback config without editing YAML manually
3. As a user, I want to search my feedback history and export for sharing

**Acceptance Criteria:**
- `/feedback` - Manual feedback trigger
  - Usage: `/feedback [operation-name]` (optional - defaults to last operation)
  - Invokes Epic 2 retrospective conversation
  - Persists via Epic 4 storage
- `/feedback-config` - View/edit configuration
  - Usage: `/feedback-config` (displays current config)
  - Usage: `/feedback-config enable` (sets enabled: true)
  - Usage: `/feedback-config mode failures-only` (sets trigger mode)
  - Validates config changes before writing
- `/feedback-search` - Search feedback history
  - Usage: `/feedback-search --date=last-30-days`
  - Usage: `/feedback-search --operation=/qa --status=failure`
  - Usage: `/feedback-search --keyword="confusing error"`
  - Uses Epic 4 searchable index
  - Displays results in table format (timestamp, operation, status, keywords)
- `/export-feedback` - Cross-project export
  - Usage: `/export-feedback --sanitize` (sanitize sensitive data)
  - Usage: `/export-feedback --date=2025-11` (November 2025 only)
  - Creates ZIP package via Epic 4

**Command Architecture:**
- Each command ≤300 lines (lean orchestration pattern)
- Delegate to `devforgeai-feedback` skill (not inline logic)
- Commands in `.claude/commands/feedback/` directory

**Estimated Effort:** Medium (8-13 story points)

## Dependencies

**Prerequisites:**
- EPIC-002 (all features) - conversation system must work before integration
- EPIC-003 Feature 2.2 (config) - hooks check config to determine when to trigger
- EPIC-004 Feature 3.1 (storage) - hooks persist feedback after conversation

**Critical Path:**
- This epic depends on ALL prior epics (integration is last phase)

## Technical Considerations

**Architecture:**
- Hook system in application layer (orchestrates conversation → template → storage)
- TodoWrite interception in infrastructure layer (hook trigger point)
- CLI commands in presentation layer (user interaction)

**Technology Stack:**
- Hook implementation: Markdown-based skill with event detection
- CLI commands: Slash commands (`.claude/commands/feedback/`)
- Integration: Leverage existing TodoWrite tool, no new dependencies

**Framework Constraints (CRITICAL):**
- **Three-Layer Architecture:** Hooks must not violate dependency rules
  - ✅ Commands can invoke feedback skill
  - ✅ Skills can invoke feedback skill
  - ❌ Subagents cannot invoke feedback skill (limitation: subagent feedback requires command/skill wrapper)
- **Single Responsibility:** Feedback skill does ONE thing (feedback collection)
- **Progressive Disclosure:** Hook logic in skill, not commands (avoid duplication)

**Compliance Validation:**
- Read `devforgeai/context/architecture-constraints.md`
- Validate hook design against locked patterns
- HALT if any violations detected

## Risks

**Risk 1: Hook Implementation Complexity**
- Likelihood: Medium
- Impact: High (if done wrong, breaks framework)
- Mitigation:
  - TodoWrite hook approach (non-invasive)
  - Graceful degradation (hook failures isolated)
  - Extensive testing (100+ hook invocation scenarios)
  - Rollback plan (disable hooks via config)

**Risk 2: Circular Hook Invocation**
- Likelihood: Low
- Impact: Critical (infinite loop, system hang)
- Mitigation:
  - Hook invocation guard (track active hook, prevent re-entry)
  - Timeout: Hooks must complete within 30s or abort
  - Log circular invocation attempts for debugging

**Risk 3: Subagent Hook Limitation**
- Likelihood: High (architectural constraint)
- Impact: Medium (subagent feedback requires workaround)
- Mitigation:
  - Document limitation in architecture docs
  - Subagent feedback flows through parent skill/command
  - Accept limitation (subagents are low-level, less user-facing)

## Acceptance Criteria (Epic Level)

- [ ] All 3 features implemented and tested
- [ ] Event-driven hooks trigger feedback at operation completion
- [ ] Hook coverage: 100% of commands, 100% of skills, ~80% of subagents (via parent wrappers)
- [ ] Hook reliability: 99.9%+ success rate, 0% operation breakage
- [ ] Operation lifecycle integration extracts rich context (todos, errors, performance)
- [ ] CLI commands provide complete feedback management (trigger, config, search, export)
- [ ] Zero violations of architecture constraints (validated against context files)
- [ ] Rollback capability (disable hooks via config without code changes)

## Notes

This epic is the **culmination** of the retrospective feedback system. It makes feedback **automatic** (no manual triggers), **context-aware** (rich operation data), and **user-friendly** (CLI commands for management).

**Key Design Decision:** TodoWrite Hook vs Explicit Calls
- **Chosen:** TodoWrite Hook (non-invasive, framework-wide coverage)
- **Rejected:** Explicit calls (code duplication across 40 files)
- **Rationale:** Centralized logic, easier maintenance, consistent behavior

**Integration Pattern:**
```
User runs: /dev STORY-042
  ↓
devforgeai-development skill executes TDD
  ↓
TodoWrite marks final todo "completed"
  ↓
**HOOK TRIGGERS** (if config.enabled && config.trigger matches)
  ↓
devforgeai-feedback skill invokes retrospective conversation
  ↓
User provides feedback (Epic 2)
  ↓
Feedback rendered via template (Epic 3)
  ↓
Feedback persisted to disk (Epic 4)
  ↓
Control returns to user
```

**Target Complexity:** Tier 3 (Event-driven architecture with clean separation of concerns)
**Timeline:** 3-5 sprints (6-10 weeks at 10 points/sprint)
