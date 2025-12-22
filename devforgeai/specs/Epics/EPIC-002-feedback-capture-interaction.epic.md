---
id: EPIC-002
title: Feedback Capture & Interaction
business-value: Enable framework users to provide structured feedback on DevForgeAI operations, improving both user learning and framework quality through systematic retrospectives
status: Planning
priority: High
complexity-score: 44
architecture-tier: Tier 3 (Complex Platform)
created: 2025-11-07
estimated-points: 26-41
target-sprints: 3-5
---

# Feedback Capture & Interaction

## Business Goal

Enable DevForgeAI users to participate in post-operation retrospectives that capture what went well and what went poorly, creating a continuous improvement feedback loop that benefits both individual users (learning) and the framework maintainers (insights for enhancements).

**Success Metrics:**
- User engagement: 60%+ of users enable feedback feature within 30 days
- Feedback quality: 80%+ of feedback sessions contain actionable insights
- Framework improvement: 5+ enhancements implemented per quarter from user feedback
- User learning: 70%+ of users report improved understanding of DevForgeAI through feedback conversations

## Features

### Feature 1.1: Post-Operation Retrospective Conversation
**Description:** Interactive Q&A conversation triggered after command/skill/subagent completion, gathering insights on success/failure, user experience, confusion points, and improvement suggestions.

**User Stories (high-level):**
1. As a DevForgeAI user, I want to reflect on what just happened after an operation completes, so that I can learn from the experience
2. As a framework maintainer, I want to collect structured feedback from users, so that I can identify improvement opportunities
3. As a user, I want retrospectives to be optional and skippable, so that I'm not forced to participate when busy

**Acceptance Criteria:**
- Retrospective conversation triggered at operation completion (if enabled)
- 5-10 AskUserQuestion prompts adapt to operation type (command vs skill vs subagent)
- Questions cover: success/failure, clarity, ease of use, confusion points, suggestions
- User can skip entire conversation or individual questions
- Feedback captured includes: operation context, user responses, timestamp

**Estimated Effort:** Medium (8-13 story points)

### Feature 1.2: Adaptive Questioning Engine
**Description:** Intelligent question selection system that adapts questions based on operation type (command, skill, subagent), success status (passed, failed, partial), and user context (first-time vs repeat operation).

**User Stories (high-level):**
1. As a user, I want questions relevant to what I just did, not generic questions
2. As a user experiencing failure, I want questions focused on debugging and learning, not just satisfaction
3. As a framework maintainer, I want consistent question patterns across operation types, enabling aggregated analysis

**Acceptance Criteria:**
- Question bank organized by operation type (11 commands, 8 skills, 21 subagents)
- Success/failure variations (different questions for pass vs fail)
- Dynamic question selection based on context (TodoWrite status, error logs, performance metrics)
- Question templates follow AskUserQuestion format (header, options, multiSelect)
- Questions target 5-10 interactions (balance depth vs user patience)

**Estimated Effort:** Large (13-20 story points)

### Feature 1.3: Skip Pattern Tracking
**Description:** Monitor user skip behavior, detect patterns (e.g., 3+ consecutive skips), and proactively suggest disabling feedback feature to reduce token waste and improve UX.

**User Stories (high-level):**
1. As a user, I don't want to be pestered with feedback prompts if I consistently skip them
2. As a framework maintainer, I want to avoid wasting tokens on unanswered feedback prompts
3. As a user, I want the system to learn my preferences (e.g., only failures-only mode)

**Acceptance Criteria:**
- Skip counter per operation type tracked in `devforgeai/feedback/skip-tracking.json`
- Pattern detection: 3+ consecutive skips triggers suggestion
- AskUserQuestion offers: disable feedback, switch to failures-only, continue as-is
- User preference stored in config file (`devforgeai/config/feedback.yaml`)
- Skip tracking resets after successful feedback session

**Estimated Effort:** Small (5-8 story points)

## Dependencies

**Prerequisite:**
- None (foundational epic)

**Dependent Epics:**
- EPIC-003 (Template & Configuration) depends on Feature 1.2 (question bank structure)
- EPIC-004 (Storage & Indexing) depends on Feature 1.1 (feedback data format)

## Technical Considerations

**Architecture:**
- Clean architecture with domain layer (feedback rules, skip tracking logic)
- Application layer (retrospective orchestration, question selection)
- Presentation layer (AskUserQuestion integration)

**Technology Stack:**
- Implementation: Markdown-based skill (`.claude/skills/devforgeai-feedback/SKILL.md`)
- Configuration: YAML (`devforgeai/config/feedback.yaml`)
- Data persistence: JSON for skip tracking, Markdown for feedback sessions

**Token Budget Impact:**
- Per conversation: 2,000-4,000 tokens (5-10 AskUserQuestion interactions)
- Mitigation: Skip pattern tracking reduces waste

## Risks

**Risk 1: User Intrusion Perception**
- Likelihood: Medium
- Impact: Medium (feature unused if annoying)
- Mitigation: Disabled by default (opt-in), easy skip, skip pattern tracking

**Risk 2: Question Fatigue**
- Likelihood: High
- Impact: Low (users stop engaging)
- Mitigation: 5-10 question limit, adaptive questioning (skip irrelevant), failures-only default

## Acceptance Criteria (Epic Level)

- [ ] All 3 features implemented and tested
- [ ] Retrospective conversations functional for commands, skills, subagents
- [ ] Adaptive questioning based on operation type and success status
- [ ] Skip pattern tracking with auto-disable suggestion
- [ ] User feedback demonstrates value (80%+ actionable insights)
- [ ] Token overhead ≤3% of 1M budget (failures-only mode)
- [ ] Integration with Epic 3 (templates) and Epic 4 (storage) validated

## Notes

This epic establishes the foundation for the DevForgeAI retrospective feedback system. It focuses on the **human-in-the-middle conversation** that captures insights. Subsequent epics add structure (templates), persistence (storage), and automation (framework hooks).

**Target Complexity:** Tier 3 (Clean Architecture with event-driven patterns)
**Timeline:** 3-5 sprints (6-10 weeks at 10 points/sprint)
