---
id: EPIC-006
title: Feedback System Integration Completion
business-value: Complete Epic 4 (Framework Integration) by implementing hook invocation across all 11 DevForgeAI commands, enabling automatic retrospective feedback capture, and completing TodoWrite context extraction for rich, context-aware feedback conversations
status: Planning
priority: Critical
complexity-score: 47
architecture-tier: Tier 3 (Complex Platform Integration)
created: 2025-11-12
estimated-points: 88-120
target-sprints: 9-12
dependencies:
  - EPIC-002 (Feedback Capture & Interaction - COMPLETE)
  - EPIC-003 (Template & Configuration System - COMPLETE)
  - EPIC-004 (Storage & Indexing - COMPLETE)
  - EPIC-005 Feature 4.3 (CLI Commands - COMPLETE)
  - STORY-019 (Operation Lifecycle Integration - 95% complete, needs full integration)
---

# Feedback System Integration Completion

## Executive Summary

The retrospective feedback system (STORY-007 through STORY-020) has **79% overall completion** with all infrastructure built (Epics 1-3: 100% complete) and CLI commands implemented (Epic 4: 33% complete). However, a **critical gap exists**: the event-driven hook system is defined but **not invoked by any DevForgeAI operations**, creating a "dormant feature set" rather than an active integration.

This epic completes the feedback system by:
1. **Wiring hooks into all 11 commands** (100% command coverage)
2. **Implementing hook invocation infrastructure** (check-hooks, invoke-hooks CLI)
3. **Completing TodoWrite context extraction** (STORY-019 specification → full implementation)
4. **Enabling automatic retrospective feedback** (seamless user experience)

**Critical Business Impact:**
- Users currently must manually remember to run `/feedback` after operations
- Rich operation context (todos, errors, timing) exists but isn't passed to feedback conversations
- Feedback system cannot achieve its core value proposition: "automatic retrospective without user remembering"
- Hook reliability NFR-A1 (99.9% success) cannot be measured (hooks never invoked)

## Business Goal

Transform the feedback system from **"infrastructure exists but unused"** to **"fully operational and automatically engaged"** by completing framework integration, enabling DevForgeAI users to receive context-aware retrospective feedback prompts at operation completion without manual triggering.

**Success Metrics:**
- **Hook Coverage:** 100% of commands (11 commands with hook invocation)
- **Hook Reliability:** 99.9%+ invocations succeed without breaking operations
- **Context Awareness:** 100% of feedback conversations pre-populated with operation context
- **User Adoption:** 60%+ of users enable feedback feature within 30 days (vs. <10% with manual triggering)
- **Feedback Quality:** 80%+ of sessions contain actionable insights (vs. ~50% with generic questions)
- **Token Efficiency:** ≤3% of 1M token budget (failures-only mode with skip tracking)

## Current State Assessment

### What's Complete (79%)

**Epic 1: Feedback Capture & Interaction (83%)**
- ✅ Adaptive Questioning Engine (STORY-008)
- ✅ Skip Pattern Tracking (STORY-009)
- ⚠️ Post-Operation Retrospective (STORY-007) - Infrastructure exists, hooks not invoked

**Epic 2: Template & Configuration System (100%)**
- ✅ Feedback Template Engine (STORY-010)
- ✅ Configuration Management (STORY-011)
- ✅ Template Customization (STORY-012)

**Epic 3: Storage & Indexing (100%)**
- ✅ File Persistence (STORY-013)
- ✅ Searchable Index (STORY-016)
- ✅ Cross-Project Export (STORY-017)

**Epic 4: Framework Integration (33%)**
- ✅ Feedback CLI Commands (STORY-020)
- ❌ Event-Driven Hook System (STORY-018) - Config exists, invocation missing
- ❌ Operation Lifecycle Integration (STORY-019) - Specification complete, implementation incomplete

### Critical Gaps

**Gap 1: Hook Invocation Missing (CRITICAL - P0)**
- **Current Reality:** Zero commands invoke `devforgeai check-hooks` or `devforgeai invoke-hooks`
- **Evidence:** `grep -r "devforgeai.*hook" .claude/commands/*.md` returns zero results
- **Impact:** Users must manually run `/feedback`, defeating automatic retrospective purpose
- **Original Requirement Violated:** FR-4.1 AC-4.1.2 (Hook trigger points at command completion)

**Gap 2: TodoWrite Context Extraction Missing (HIGH - P0)**
- **Current Reality:** STORY-019 has complete specification but implementation incomplete
- **Evidence:** Skill documentation shows "TodoWrite integration (EPIC-004) ⏸️ Pending"
- **Impact:** Feedback conversations lack contextual awareness (generic questions, not specific to todos/errors)
- **Original Requirement Violated:** FR-4.2 AC-4.2.1-4.2.3 (Context extraction and template pre-population)

**Gap 3: Test Cleanup Issue (LOW - P2)**
- **Current Reality:** 116 test artifact zip files created in project root (hygiene issue)
- **Impact:** Test pollution, risk of accidental git commits
- **Priority:** Should-Have (not blocking, but needs fixing)

## Features

### Feature 6.1: Hook Invocation Infrastructure

**Description:** Implement CLI commands for checking hook eligibility and invoking hooks, enabling DevForgeAI commands to trigger feedback conversations automatically.

**User Stories:**
1. As a command implementer, I want a simple `devforgeai check-hooks --operation=dev --status=success` call to determine if feedback should trigger, so I don't duplicate hook evaluation logic
2. As a framework maintainer, I want hook invocation centralized in CLI, not duplicated across 11 commands, ensuring consistent behavior
3. As a user, I want hooks to work reliably (99.9%+ success) without breaking my operations, so feedback never disrupts my workflow

**Acceptance Criteria:**
- `devforgeai check-hooks` command implemented
  - Arguments: `--operation=<name>` `--status=<completed|failed|partial>`
  - Returns: Exit code 0 (should trigger) or 1 (should not trigger)
  - Checks: Config enabled? Trigger rule matches? User approval required?
  - Performance: <100ms response time (fast check)
- `devforgeai invoke-hooks` command implemented
  - Arguments: `--operation=<name>` `--story=<STORY-ID>` (optional)
  - Behavior: Extract context → Invoke feedback skill → Persist feedback
  - Graceful degradation: Errors logged, don't throw to caller
  - Timeout: 30s max execution, abort if exceeded
- Invocation guard implemented
  - Tracks active hook (prevent circular invocation)
  - Logs circular attempts for debugging
  - Returns early if hook already active
- Hook success metrics tracked
  - Log all invocations (operation, status, duration, success/failure)
  - Calculate success rate (target: 99.9%+)
  - Alert if success rate <95%

**Technical Specification:**
- Location: `.claude/scripts/devforgeai_cli/hooks.py`
- Functions: `check_hooks()`, `invoke_hooks()`, `get_hook_registry()`
- Configuration: Read from `devforgeai/config/hooks.yaml`
- Integration: Import from `devforgeai_cli.hooks` in commands

**Estimated Effort:** 13 story points (Large)

**Stories:**
- STORY-021: Implement devforgeai check-hooks CLI command (5 points)
- STORY-022: Implement devforgeai invoke-hooks CLI command (8 points)

---

### Feature 6.2: Command Integration Rollout (Pilot + Full Rollout)

**Description:** Wire hooks into all 11 DevForgeAI commands, starting with pilot (/dev) and rolling out to remaining commands after validation.

**User Stories:**
1. As a user running /dev, I want automatic feedback prompt after TDD cycle completes, so I can reflect on what I learned without having to remember to run /feedback
2. As a user running /qa, I want feedback prompt only on failures (default config), so I'm not pestered when everything passes
3. As a user, I want consistent feedback experience across all commands (same questions, same flow), regardless of which command I ran

**Acceptance Criteria:**
- Phase N added to all 11 commands (after main workflow, before completion)
  ```markdown
  ### Phase N: Invoke Feedback Hook (if enabled)

  **Check if feedback should trigger:**
  ```bash
  devforgeai check-hooks --operation=$OPERATION_NAME --status=$STATUS
  if [ $? -eq 0 ]; then
    devforgeai invoke-hooks --operation=$OPERATION_NAME --story=$STORY_ID
  fi
  ```

  **What happens:**
  - If config enabled and trigger matches → Retrospective conversation
  - If user skips → Skip counter incremented
  - If hook fails → Warning logged, operation succeeds
  ```
- Commands updated (in order):
  1. **Pilot:** /dev (workflow command, high usage, good test case)
  2. **Workflow commands:** /qa, /release, /orchestrate
  3. **Planning commands:** /create-story, /create-epic, /create-sprint
  4. **Utility commands:** /create-context, /ideate, /create-ui, /audit-deferrals
- All hooks follow same pattern (consistency)
- No code duplication (hooks use CLI, not inline logic)
- Graceful degradation verified (hook failures don't break commands)
- User testing with real stories (validate UX)

**Technical Specification:**
- Location: `.claude/commands/*.md` (11 files updated)
- Pattern: Add Phase N at end of workflow (before final success message)
- Integration: Call devforgeai CLI commands (check-hooks, invoke-hooks)
- Error Handling: Log warnings, don't throw exceptions

**Estimated Effort:** 55 story points (8 points/command average, some simpler)

**Stories:**
- STORY-023: Wire hooks into /dev command (pilot) (8 points)
- STORY-024: Wire hooks into /qa command (5 points)
- STORY-025: Wire hooks into /release command (5 points)
- STORY-026: Wire hooks into /orchestrate command (5 points)
- STORY-027: Wire hooks into /create-story command (5 points)
- STORY-028: Wire hooks into /create-epic command (5 points)
- STORY-029: Wire hooks into /create-sprint command (5 points)
- STORY-030: Wire hooks into /create-context command (3 points)
- STORY-031: Wire hooks into /ideate command (5 points)
- STORY-032: Wire hooks into /create-ui command (5 points)
- STORY-033: Wire hooks into /audit-deferrals command (4 points)

---

### Feature 6.3: TodoWrite Context Extraction (Complete STORY-019)

**Description:** Complete TodoWrite context extraction implementation, enabling rich operation context to be passed to feedback conversations for adaptive, context-aware questioning.

**User Stories:**
1. As a user who just completed /dev with 8 todos, I want feedback questions to reference specific todos (e.g., "The refactor phase took 20 minutes - was that expected?"), not generic "how did it go?"
2. As a user whose /qa run failed, I want feedback questions to ask about the specific error (e.g., "Coverage failed at 82% - what prevented higher coverage?"), so my feedback is actionable
3. As a framework maintainer, I want all feedback sessions to include operation context (todos, errors, timing), so I can correlate user feedback with technical events

**Acceptance Criteria:**
- `extractOperationContext()` implemented and integrated
  - Extract todos, status, execution time from TodoWrite
  - Extract error context (message, stack trace, failed todo)
  - Sanitize context (remove secrets, credentials, PII)
  - Performance: <200ms extraction time
- Context passed to feedback conversation
  - Pre-populate template metadata (operation type, duration, status, todo count)
  - Make context available to AskUserQuestion prompts
  - Adapt questions based on context (e.g., ask about failed todos specifically)
- Operation history updated
  - Link feedback session to operation
  - Queryable: feedback-linked operations vs standalone
- Graceful degradation for incomplete context
  - Log warning if TodoWrite data missing
  - Extract partial context if available
  - Continue without blocking
- Context size limits enforced
  - Max 50KB per context
  - Summarize if >100 todos
  - Truncate stack traces if >5KB

**Technical Specification:**
- Location: `.claude/skills/devforgeai-feedback/context_extraction.py`
- Functions: `extract_operation_context()`, `sanitize_context()`, `pass_to_feedback()`
- Data Model: `OperationContext` (operation_id, type, story_id, start_time, end_time, duration, status, todos, error, phases)
- Integration: Called by `invoke-hooks` before feedback conversation starts

**Estimated Effort:** 21 story points (Large - significant implementation work)

**Stories:**
- STORY-103: Implement extractOperationContext() function (13 points)
- STORY-104: Implement adaptive questioning based on context (8 points)

---

### Feature 6.4: Testing, Refinement & Documentation

**Description:** Comprehensive testing, performance optimization, test cleanup, and documentation updates to ensure production readiness.

**User Stories:**
1. As a framework maintainer, I want comprehensive test coverage (>90% for hook system), so I'm confident hooks work reliably
2. As a user, I want hook invocation to be fast (<3s to first feedback question), so feedback doesn't feel like a workflow interruption
3. As a developer, I want test artifacts cleaned up properly (no zip files in project root), so my project stays clean

**Acceptance Criteria:**
- Test cleanup issue fixed
  - Update `tests/test_feedback_export_import.py` to use `tempfile.TemporaryDirectory()`
  - No test artifacts in project root
  - Tests clean up after themselves
- Performance optimization
  - Hook check: <100ms
  - Context extraction: <200ms
  - Feedback conversation start: <3s from operation completion
  - Token budget: ≤3% of 1M tokens (failures-only mode)
- NFR validation
  - NFR-A1: 99.9%+ hook reliability (measured over 100+ invocations)
  - NFR-P1: <3s response time (measured in production)
  - NFR-P3: ≤3% token budget (measured over sprint)
- Documentation updates
  - User guide: How to enable/disable hooks, configure triggers
  - Framework docs: Hook system architecture, integration patterns
  - Troubleshooting: Common issues, solutions, FAQ
  - Migration guide: Enabling feedback on existing projects

**Technical Specification:**
- Test coverage target: >90% for hook system, >80% overall
- Performance benchmarks: Record in `devforgeai/qa/performance/`
- Documentation locations:
  - User guide: `docs/guides/feedback-system-user-guide.md`
  - Architecture: `docs/architecture/hook-system-design.md`
  - Troubleshooting: `docs/guides/feedback-troubleshooting.md`

**Estimated Effort:** 16 story points (Medium)

**Stories:**
- STORY-105: Fix test cleanup issue (3 points)
- STORY-106: Performance optimization and NFR validation (8 points)
- STORY-107: Documentation and user guide updates (5 points)

---

## Dependencies

### Prerequisites (All Complete)

- ✅ EPIC-002 (Feedback Capture & Interaction) - Conversation system works
- ✅ EPIC-003 (Template & Configuration System) - Templates and config exist
- ✅ EPIC-004 (Storage & Indexing) - Storage and search work
- ✅ EPIC-005 Feature 4.3 (CLI Commands) - User-facing commands implemented

### Internal Dependencies (Sequential)

**Critical Path:**
1. Feature 6.1 (Hook Infrastructure) → Feature 6.2 (Command Integration)
2. Feature 6.3 (Context Extraction) can be parallel with Feature 6.1
3. Feature 6.2 (Pilot /dev) → Feature 6.2 (Full Rollout)
4. Feature 6.4 (Testing) after all features implemented

**Dependency Graph:**
```
Feature 6.1 (Hook Infrastructure)
  ↓
Feature 6.2 (Pilot /dev)
  ↓
Feature 6.2 (Full Rollout - 10 remaining commands)
  ↓
Feature 6.4 (Testing & Refinement)

Feature 6.3 (Context Extraction) [Parallel with 6.1]
  ↓ (Integrates into)
Feature 6.1 (Hook invocation uses context)
```

## Technical Considerations

### Architecture Compliance

**Three-Layer Architecture:**
- ✅ Presentation Layer: Commands invoke hooks (no business logic)
- ✅ Application Layer: devforgeai-feedback skill orchestrates (conversation → template → storage)
- ✅ Infrastructure Layer: CLI commands (check-hooks, invoke-hooks) interface with skill

**No Violations:** All integration respects architecture constraints

### Hook Invocation Pattern (Recommended)

**TodoWrite Hook Approach (Already Defined in EPIC-005):**
- Hook triggers on TodoWrite completion event
- Non-invasive (no changes to command logic, just add Phase N)
- Framework-wide coverage (all commands use TodoWrite)
- Graceful degradation (hook failures isolated)

**Implementation:**
```markdown
### Phase N: Invoke Feedback Hook

devforgeai check-hooks --operation=$OPERATION --status=$STATUS
if [ $? -eq 0 ]; then
  devforgeai invoke-hooks --operation=$OPERATION --story=$STORY_ID
fi
```

### Technology Stack

- **Hook Infrastructure:** Python CLI commands (`.claude/scripts/devforgeai_cli/hooks.py`)
- **Command Integration:** Markdown slash commands (`.claude/commands/*.md`)
- **Context Extraction:** Python module (`.claude/skills/devforgeai-feedback/context_extraction.py`)
- **Configuration:** YAML (`devforgeai/config/hooks.yaml`)
- **Storage:** File-based (`devforgeai/feedback/sessions/`)

### Performance Targets

- **Hook Check:** <100ms (fast decision, no blocking)
- **Hook Invocation:** <3s total (check → extract → prompt → persist)
- **Context Extraction:** <200ms (parse TodoWrite, sanitize)
- **Token Budget:** ≤3% of 1M tokens (skip tracking, failures-only default)

## Risks

### Risk 1: Command Integration Complexity

**Likelihood:** Medium
**Impact:** High (if done wrong, could break 11 commands)
**Mitigation:**
- Start with pilot (/dev) to validate pattern
- Test pilot extensively (30+ scenarios) before rollout
- Rollback plan: Comment out Phase N if issues detected
- Graceful degradation: Hook failures don't break commands
- Automated testing: Integration tests for all 11 commands

**Level:** Medium → Low (with pilot and testing)

---

### Risk 2: Performance Degradation

**Likelihood:** Low
**Impact:** Medium (users notice slower command completion)
**Mitigation:**
- Performance benchmarks before/after integration
- Optimize context extraction (<200ms target)
- Cache hook eligibility checks (don't re-evaluate)
- Monitor token usage (stay under 3% budget)
- Disable hooks if performance issues detected

**Level:** Low

---

### Risk 3: User Adoption Resistance

**Likelihood:** Medium
**Impact:** Medium (feedback feature unused despite effort)
**Mitigation:**
- Default config: failures-only mode (less intrusive)
- Skip tracking: Suggest disabling if user skips 3+ times
- Clear value proposition: "Learn from failures without manual effort"
- User education: Guide, examples, success stories
- Easy disable: Single config change to turn off

**Level:** Medium → Low (with defaults and skip tracking)

---

### Risk 4: Circular Hook Invocation

**Likelihood:** Low
**Impact:** Critical (infinite loop, system hang)
**Mitigation:**
- Invocation guard: Track active hook, prevent re-entry
- Timeout: 30s max execution, abort if exceeded
- Logging: Log circular attempts for debugging
- Testing: Explicit tests for circular scenarios

**Level:** Low

---

## Roadmap

### Sprint 1-2: Hook Infrastructure & Pilot (Feature 6.1 + partial 6.2)

**Goals:**
- Implement hook infrastructure (check-hooks, invoke-hooks)
- Wire hooks into /dev (pilot)
- Validate pattern with real usage
- Measure performance and reliability

**Deliverables:**
- STORY-021: devforgeai check-hooks implemented
- STORY-022: devforgeai invoke-hooks implemented
- STORY-023: /dev command with hooks (pilot)
- Performance benchmarks (hook check <100ms, invocation <3s)

**Success Criteria:**
- /dev command triggers feedback automatically
- Hook reliability >99% in pilot
- No operation breakage (100% /dev commands succeed)

---

### Sprint 3-5: Context Extraction (Feature 6.3)

**Goals:**
- Implement TodoWrite context extraction
- Pass context to feedback conversations
- Enable adaptive questioning

**Deliverables:**
- STORY-034: extractOperationContext() implemented
- STORY-035: Adaptive questioning based on context
- Context size <50KB
- Extraction time <200ms

**Success Criteria:**
- Feedback questions reference specific todos/errors
- Context sanitization 100% (no secrets leaked)
- Graceful degradation for incomplete context

---

### Sprint 6-8: Full Command Rollout (Feature 6.2 remainder)

**Goals:**
- Wire hooks into remaining 10 commands
- Validate consistency across all commands
- Enable hooks in production

**Deliverables:**
- STORY-024 to STORY-033: All commands with hooks
- Integration tests for all 11 commands
- Hook success rate >99.9%

**Success Criteria:**
- 100% command coverage
- Consistent UX across all commands
- No operation breakage

---

### Sprint 9: Testing, Refinement & Documentation (Feature 6.4)

**Goals:**
- Fix test cleanup issue
- Performance optimization
- NFR validation
- Documentation complete

**Deliverables:**
- STORY-036: Test cleanup fixed
- STORY-037: Performance validated
- STORY-038: Documentation complete
- User guide, architecture docs, troubleshooting guide

**Success Criteria:**
- Test artifacts cleaned up
- NFR-A1, NFR-P1, NFR-P3 validated
- Documentation comprehensive

---

### Sprint 10 (Optional): Refinement & Monitoring

**Goals:**
- Production monitoring
- User feedback collection
- Bug fixes and enhancements

**Deliverables:**
- Production metrics dashboard
- User adoption tracking
- Enhancement backlog

---

## Acceptance Criteria (Epic Level)

- [ ] All 4 features implemented and tested
- [ ] Hook invocation infrastructure complete (check-hooks, invoke-hooks CLI)
- [ ] 100% command coverage (11 commands with hooks)
- [ ] TodoWrite context extraction complete (STORY-019 fully implemented)
- [ ] Hook reliability: 99.9%+ success rate (NFR-A1)
- [ ] Performance: <3s to first feedback question (NFR-P1)
- [ ] Token budget: ≤3% of 1M tokens (NFR-P3)
- [ ] Context-aware feedback: 100% of sessions pre-populated with operation context
- [ ] Test artifacts cleaned up (no project root pollution)
- [ ] Documentation complete (user guide, architecture, troubleshooting)
- [ ] Zero violations of architecture constraints
- [ ] Rollback capability (disable hooks via config)
- [ ] User testing complete (10+ real-world scenarios)

## Success Metrics

### User Engagement Metrics

**M1: Feature Adoption**
- **Baseline:** <10% (with manual triggering)
- **Target:** 60%+ of users enable feedback within 30 days
- **Measurement:** Config file analysis across projects

**M2: Feedback Quality**
- **Baseline:** ~50% with generic questions
- **Target:** 80%+ of sessions contain actionable insights
- **Measurement:** Manual review + keyword extraction

**M3: User Satisfaction**
- **Baseline:** Unknown (feature unused)
- **Target:** 70%+ report improved DevForgeAI understanding
- **Measurement:** Optional user survey

### Framework Improvement Metrics

**M4: Issue Identification Rate**
- **Baseline:** 0 (no feedback collected)
- **Target:** 5+ bugs/enhancements identified per month
- **Measurement:** GitHub issues tagged "user-feedback"

**M5: Time to Resolution**
- **Baseline:** N/A
- **Target:** 30-day median from feedback to issue resolution
- **Measurement:** Timestamp delta (feedback → issue close)

### Technical Performance Metrics

**M6: Hook Reliability (NFR-A1)**
- **Target:** 99.9%+ hook invocations succeed
- **Measurement:** Hook success rate over 1000+ invocations

**M7: Token Efficiency (NFR-P3)**
- **Target:** ≤3% of 1M token budget
- **Measurement:** Token usage tracking (failures-only mode)

**M8: Performance (NFR-P1)**
- **Target:** <3s to first feedback question
- **Measurement:** Latency from operation completion to first AskUserQuestion

## Timeline Estimate

**Total Effort:** 88-120 story points

**Sprint Velocity:** 10 points/sprint (average)

**Duration:** 9-12 sprints (18-24 weeks)

**Breakdown by Feature:**
- Feature 6.1 (Hook Infrastructure): 13 points (2 sprints)
- Feature 6.2 (Command Integration): 55 points (6 sprints)
- Feature 6.3 (Context Extraction): 21 points (2-3 sprints)
- Feature 6.4 (Testing & Refinement): 16 points (2 sprints)

**Parallel Work Opportunities:**
- Feature 6.3 can be parallel with Feature 6.1 (saves 2-3 sprints)
- Actual Duration: 9-10 sprints (18-20 weeks) with parallelization

## Notes

### Key Design Decisions

**1. TodoWrite Hook vs Explicit Calls**
- **Chosen:** TodoWrite Hook (non-invasive)
- **Rationale:** Centralized logic, no code duplication, framework-wide coverage
- **Already Defined:** EPIC-005 recommended this approach

**2. Pilot Rollout Strategy**
- **Chosen:** Start with /dev, validate, then roll out to 10 remaining commands
- **Rationale:** De-risks integration, catches issues early, validates pattern
- **Timeline:** 1 sprint pilot, then 3-5 sprints full rollout

**3. Context Extraction Completion**
- **Chosen:** Complete STORY-019 implementation (was 95% spec, 5% code)
- **Rationale:** Context-aware questioning is core value proposition
- **Timeline:** 2-3 sprints parallel with hook infrastructure

### Integration with Existing Stories

**STORY-007 (Post-Operation Retrospective):**
- Currently: Infrastructure exists but hooks not invoked
- After: Hooks trigger retrospective automatically
- Impact: Feature becomes operational

**STORY-019 (Operation Lifecycle Integration):**
- Currently: Specification complete, implementation incomplete
- After: Full implementation, context extraction working
- Impact: Feedback conversations become context-aware

**STORY-020 (Feedback CLI Commands):**
- Currently: Complete
- After: Enhanced with hook infrastructure (check-hooks, invoke-hooks)
- Impact: Commands gain automatic triggering capability

### User Experience Flow (Target)

```
User runs: /dev STORY-042
  ↓
devforgeai-development executes TDD (Red → Green → Refactor)
  ↓
TodoWrite marks final todo "completed"
  ↓
Phase N: Check hooks
  ↓ (if enabled)
devforgeai invoke-hooks --operation=dev --story=STORY-042
  ↓
Extract context (todos, errors, timing)
  ↓
Invoke devforgeai-feedback skill
  ↓
Retrospective conversation (5-10 questions, context-aware)
  ↓
User provides feedback
  ↓
Template rendered and persisted
  ↓
Control returns to user
  ↓
"Story STORY-042 complete. Feedback collected."
```

### Rollback Plan

**If issues arise:**
1. **Immediate:** Disable hooks via config (`enabled: false`)
2. **Short-term:** Comment out Phase N in affected commands
3. **Long-term:** Fix issue, re-enable hooks

**No breaking changes:** All changes are additive (Phase N at end of workflow)

## Related Documents

- **Audit Report:** `devforgeai/silo/feedback-system-integration-audit-2025-11-12.md`
- **Requirements:** `devforgeai/specs/requirements/retrospective-feedback-system-requirements.md`
- **Epic 5:** `devforgeai/specs/Epics/EPIC-005-framework-integration.epic.md` (original integration epic)
- **Story 18:** `devforgeai/specs/Stories/STORY-018-event-driven-hook-system.story.md` (hook config exists)
- **Story 19:** `devforgeai/specs/Stories/STORY-019-operation-lifecycle-integration.story.md` (context extraction spec)
- **Story 20:** `devforgeai/specs/Stories/STORY-020-feedback-cli-commands.story.md` (CLI commands complete)

---

## Stories

### Feature 6.1: Hook Invocation Infrastructure (13 points)
- STORY-021: Implement devforgeai check-hooks CLI command (5 points) - QA Approved
- STORY-022: Implement devforgeai invoke-hooks CLI command (8 points) - QA Approved
- STORY-256: Implement invoke_feedback_skill() Method in Hooks Service (3 points) - Backlog

### Feature 6.2: Command Integration Rollout (55 points)
- STORY-023: Wire hooks into /dev command (pilot) (8 points) - QA Approved
- STORY-024: Wire hooks into /qa command (5 points) - QA Approved
- STORY-025: Wire hooks into /release command (5 points) - Dev Complete
- STORY-026: Wire hooks into /orchestrate command (5 points) - QA Approved
- STORY-027: Wire hooks into /create-story command (5 points) - QA Approved
- STORY-028: Wire hooks into /create-epic command (5 points) - QA Approved
- STORY-029: Wire hooks into /create-sprint command (5 points) - QA Approved
- STORY-030: Wire hooks into /create-context command (3 points) - QA Approved
- STORY-031: Wire hooks into /ideate command (5 points) - QA Approved
- STORY-032: Wire hooks into /create-ui command (5 points) - QA Approved
- STORY-033: Wire hooks into /audit-deferrals command (4 points) - Dev Complete

### Feature 6.3: TodoWrite Context Extraction (21 points)
- STORY-103: Implement extractOperationContext() function (13 points) - Backlog
- STORY-104: Implement adaptive questioning based on context (8 points) - Backlog

### Feature 6.4: Testing, Refinement & Documentation (16 points)
- STORY-105: Fix test cleanup issue (3 points) - Backlog
- STORY-106: Performance optimization and NFR validation (8 points) - Backlog
- STORY-107: Documentation and user guide updates (5 points) - Backlog

---

**END OF EPIC DOCUMENT**

**Status:** ✅ COMPLETE - Ready for sprint planning and story creation

**Next Steps:**
1. Review and approve epic document
2. Create 18 stories (STORY-021 through STORY-038)
3. Plan Sprint 1 (Feature 6.1 + pilot)
4. Begin implementation with /dev pilot integration
