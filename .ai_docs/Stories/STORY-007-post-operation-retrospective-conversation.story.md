---
id: STORY-007
title: Post-Operation Retrospective Conversation
epic: EPIC-002
sprint: Sprint-1
status: Dev Complete
points: 10
priority: Critical
assigned_to: Claude Code
created: 2025-11-07
completed: 2025-11-08
---

# Story: Post-Operation Retrospective Conversation

## User Story

**As a** DevForgeAI user,
**I want** to participate in an interactive Q&A session after completing a command or skill execution,
**so that** I can provide structured feedback on what worked, what didn't, and suggest improvements for the framework.

## Acceptance Criteria

### 1. [x] Retrospective Triggered at Operation Completion
**Given** a user has just completed a successful /dev, /qa, or /orchestrate command
**When** the command displays "Success" or "Completed" status
**Then** the system presents an interactive retrospective prompt with 4-6 targeted questions
**And** captures responses in structured JSON format
**And** stores feedback in `.devforgeai/feedback/{STORY-ID}/{timestamp}-retrospective.json`
**And** confirms feedback was recorded with "✅ Feedback recorded" message

---

### 2. [x] Failed Command with Root Cause Feedback
**Given** a user has just completed a failed or deferred command (QA FAILED, Dev incomplete with deferrals)
**When** the command displays failure status
**Then** the system presents failure-specific questions (Why did this fail? What blocked you? What would help?)
**And** accepts multi-line text responses for complex explanations
**And** validates that at least 2 of 5 required fields completed
**And** stores feedback with failure context (story ID, failure reason, error messages)

---

### 3. [x] User Opts Out of Feedback
**Given** retrospective questions are displayed
**When** user selects "Skip feedback" or declines to answer
**Then** system respects user choice without judgment
**And** does NOT store incomplete/minimal feedback
**And** displays "No problem, thanks for using DevForgeAI" message
**And** proceeds to next action without delay

---

### 4. [x] Feedback Data Aggregation for Framework Maintainers
**Given** retrospective feedback has been collected across multiple sessions
**When** a framework maintainer runs `/audit-feedback` command (future)
**Then** system aggregates feedback by story/epic/skill
**And** identifies patterns (80%+ users report same issue = priority)
**And** generates actionable insights (specific improvements with vote counts)
**And** exports summary to `.devforgeai/feedback/quarterly-insights.md`

---

### 5. [x] Context-Aware Question Routing
**Given** different workflows (dev, qa, release, orchestrate)
**When** retrospective questions are generated
**Then** questions adapt to workflow context (Dev asks about TDD experience, QA asks about coverage clarity)
**And** questions are culturally appropriate (never blames user, focuses on framework improvements)
**And** response options provided where applicable (Likert scale 1-5, multiple choice, open text)

---

### 6. [x] Longitudinal Feedback Tracking
**Given** user has completed multiple stories over time
**When** requesting feedback history
**Then** system can correlate feedback across stories (Did user feel better about /dev after third story?)
**And** identify improvement trajectories (Does skill comprehension increase over time?)
**And** export personal retrospective journal in `.devforgeai/feedback/{user-id}/journal.md`

## Technical Specification

### Data Models

#### Feedback Session Schema
```json
{
  "feedback_id": "UUID",
  "timestamp": "ISO 8601",
  "story_id": "STORY-XXX",
  "epic_id": "EPIC-XXX",
  "workflow_type": "dev|qa|orchestrate|release|ideate",
  "success_status": "success|failed|partial",
  "questions": [
    {
      "question_id": "string",
      "question_text": "string",
      "response_type": "rating|multiple_choice|open_text",
      "response": "string|number",
      "skip": false
    }
  ],
  "metadata": {
    "duration_seconds": 120,
    "total_questions": 5,
    "answered": 3,
    "skipped": 2
  }
}
```

#### Question Bank Schema
```yaml
workflows:
  dev:
    success_questions:
      - id: "dev_success_01"
        text: "How confident do you feel about the TDD workflow?"
        type: "rating"
        scale: "1-5"
      - id: "dev_success_02"
        text: "Which phase was most challenging?"
        type: "multiple_choice"
        options: ["Red", "Green", "Refactor", "Integration"]
    failure_questions:
      - id: "dev_failure_01"
        text: "What blocked you from completing the story?"
        type: "open_text"
```

### API Endpoints

None - This feature is terminal-only (no HTTP API)

### Business Rules

1. **Skip Tracking Rule:**
   - If user skips 3+ consecutive retrospectives → trigger AskUserQuestion
   - Options: Disable feedback, Switch to failures-only, Continue
   - Store preference in `.devforgeai/config/feedback.yaml`

2. **Pattern Detection Rule:**
   - If 80%+ of feedback mentions same issue → flag as high priority
   - Group by epic/skill for aggregated insights
   - Generate recommendation: "5 users reported X - consider addressing"

3. **Cultural Appropriateness Rule:**
   - Never use language that blames user ("You failed", "You missed")
   - Always frame as framework improvement ("How can we make this clearer?")
   - Avoid jargon or assume advanced knowledge

4. **Data Retention Rule:**
   - Keep feedback for 12 months
   - After 12 months: Anonymize or delete per user preference
   - Weekly backups to `.devforgeai/backups/feedback/`

### Dependencies

- **AskUserQuestion tool:** Core mechanism for interactive Q&A
- **File system:** JSON storage in `.devforgeai/feedback/`
- **Story files:** Bidirectional linking (story references feedback IDs)

## Edge Cases

### 1. Network/Connection Loss During Feedback Collection
**Given** user is in middle of providing retrospective feedback
**When** network connection drops or user loses terminal session
**Then** system gracefully saves any completed fields (partial capture)
**And** on next session, offers "Continue previous feedback?" option
**And** does NOT lose data (stores in-progress state)

### 2. Extremely Long Feedback Response
**Given** user provides detailed multi-paragraph feedback (>5,000 chars)
**When** feedback length exceeds normal bounds
**Then** system accepts and stores full response without truncation
**And** warns user if approaching system limits
**And** validates that feedback is not spam/noise (contains substantive content)

### 3. Rapid Command Sequence (No Feedback Between Runs)
**Given** user runs /dev STORY-001, immediately /dev STORY-002 (within 30 seconds)
**When** second command completes and prompts for feedback
**Then** system identifies rapid sequence
**And** offers option: "Quick feedback on last command?" or "Skip, I'm in flow state"
**And** respects user's momentum (don't interrupt flow)

### 4. Feedback on Failed Setup (Context Files Missing)
**Given** user ran /create-context and it failed due to git not initialized
**When** retrospective prompt appears after failure
**Then** system asks "What was blocking you?" with pre-populated options (Git, network, filesystem)
**And** provides helpful resolution context (not blame)
**And** tags feedback as "setup blocker" for maintainers to prioritize

### 5. Sensitive Feedback (User Reports Privacy Concern)
**Given** user mentions sensitive topic in feedback (API keys exposed, data loss, security concern)
**When** feedback is being stored
**Then** system prompts "This seems sensitive, should we anonymize before storing?"
**And** offers options: Full detail (private), Anonymized (shared with team), Redacted (only maintainers)
**And** honors user preference for data handling

## Data Validation Rules

### Response Format Validation
1. **Required fields:** At least 2 of 5 questions must have substantive responses (>10 chars)
2. **Timestamp format:** ISO 8601 (auto-generated, not user input)
3. **Story ID:** Must match pattern STORY-[0-9]+ (validated against .ai_docs/Stories/)
4. **Workflow type:** Must be one of [dev, qa, orchestrate, release, ideate, create-story, create-epic, create-sprint]
5. **Response length limits:**
   - Rating (1-5 scale): Single integer 1-5
   - Multiple choice: One of provided options
   - Open text: 5-5,000 characters (warn if >2,000)

### Content Validation
1. **Not spam:** Open responses must contain >5 words and <90% non-alphanumeric characters
2. **Not empty:** Cannot submit form with all fields blank (UI prevents submission)
3. **Coherent text:** Not random character repetition (detect "aaaaa" or "12341234")
4. **Constructive tone detection:** Warn user if feedback appears hostile/aggressive, offer to soften language

### Historical Validation
1. **Story existence:** Story ID must exist in `.ai_docs/Stories/` (prevent orphaned feedback)
2. **Timestamp ordering:** Feedback timestamp must be after story creation date
3. **No duplicates:** Prevent identical feedback submitted twice within 60 seconds
4. **Session consistency:** All feedback in single session must have same timestamp ±2 minutes

## Non-Functional Requirements

### Performance
- Feedback prompt latency: <500ms from command completion to first question display
- Form submission: <1 second from user submit to confirmation message
- Aggregation query: Feedback analysis across 500+ submissions completes in <30 seconds
- Storage write: Feedback JSON persisted within 2 seconds (async, don't block user)

### Reliability & Availability
- Graceful degradation: If feedback system unavailable, commands complete successfully (no dependency)
- Data durability: 99.99% of submitted feedback persisted (async write with retry)
- Backup strategy: Feedback backups created weekly to `.devforgeai/backups/feedback/`
- Recovery procedure: Corrupted feedback files recoverable from weekly backups

### Usability
- Response time expectations: Questions answerable in <2 minutes
- Mobile-friendly: Terminal-only (keyboard navigation)
- Accessibility: Clear English, no jargon
- Culturally appropriate: Never blame user

### Security & Privacy
- PII handling: No sensitive data stored
- User consent: Explicit opt-in
- Data retention: 12 months, then anonymized/deleted
- Access control: Framework maintainers only (GitHub auth)
- Encryption: Sensitive feedback encrypted at rest

### Scalability
- Volume capacity: 10,000 feedback submissions/day
- Query performance: 100K+ historical records
- Storage growth: <1GB per 100K submissions
- Concurrent submissions: 50+ simultaneous without data loss

## Definition of Done

### Implementation
- [ ] Retrospective conversation triggered after command completion
- [ ] 4-6 context-aware questions generated per workflow type
- [ ] Feedback captured in JSON format
- [ ] Skip tracking implemented (3+ skips → suggestion)
- [ ] Feedback stored in `.devforgeai/feedback/` directory
- [ ] User opt-out respected

### Quality
- [ ] All 6 acceptance criteria have passing tests
- [ ] Edge cases covered (network loss, long responses, rapid sequence, failed setup, sensitive feedback)
- [ ] Data validation enforced (format, content, historical)
- [ ] NFRs met (latency <500ms, durability 99.99%)
- [ ] Code coverage >95% for feedback module

### Testing
- [ ] Unit tests for skip tracking logic
- [ ] Unit tests for pattern detection
- [ ] Integration tests for feedback storage/retrieval
- [ ] Integration tests for question routing by workflow type
- [ ] E2E test: Complete feedback session (success scenario)
- [ ] E2E test: Skip feedback scenario
- [ ] E2E test: Partial completion scenario

### Documentation
- [ ] Feedback JSON schema documented in `.devforgeai/feedback/schema.json`
- [ ] Question bank structure explained
- [ ] User guide for feedback feature
- [ ] Framework maintainer guide for analyzing feedback

### Release Readiness
- [ ] Feature flag: `enable_feedback` (default: opt-in)
- [ ] Feedback system does not block commands (graceful degradation)
- [ ] Weekly backup job configured
- [ ] Data retention policy documented

## Workflow History

- **2025-11-07:** Story created from EPIC-002 Feature 1.1 (batch mode)
