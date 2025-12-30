# Feedback System Overview

The DevForgeAI Feedback System is an automated retrospective feedback collection mechanism that captures developer insights after completing operations. It enables continuous improvement by gathering data about challenges, successes, and workflows while context is fresh.

---

## Table of Contents

1. [What is the Feedback Phase?](#what-is-the-feedback-phase)
2. [When It Runs](#when-it-runs)
3. [Feedback Types](#feedback-types)
4. [Commands Reference](#commands-reference)
5. [Data Storage & Privacy](#data-storage--privacy)
6. [Quick Start](#quick-start)
7. [Architecture Overview](#architecture-overview)
8. [Related Documentation](#related-documentation)

---

## What is the Feedback Phase?

The feedback phase is an **event-driven, non-blocking** system that automatically triggers after DevForgeAI operations complete. It uses hooks to collect structured insights without modifying existing workflows.

### Key Features

| Feature | Description |
|---------|-------------|
| **Non-Blocking** | Hook failures never affect operation success |
| **Event-Driven** | Automatically triggers via hook system |
| **Adaptive** | Questions adapt to operation context |
| **Privacy-First** | Local storage only, never auto-transmitted |
| **Configurable** | Enable/disable per operation, customize questions |
| **Searchable** | Index-based retrieval with filtering |

### Benefits

- **Continuous Improvement** — Learn from successes and failures
- **Context Preservation** — Capture insights while fresh
- **Pattern Detection** — Identify recurring challenges
- **Knowledge Building** — Organizational learning over time

---

## When It Runs

The feedback phase integrates into DevForgeAI workflows at specific points:

### Position in `/dev` Workflow

```
Phase 08: Git Commit
    ↓
Phase 09: Feedback Hook Integration  ← FEEDBACK TRIGGERED
    ↓
Phase 10: Result & Completion
```

**Entry Gate:** `devforgeai-validate phase-check ${STORY_ID} --from=08 --to=09`
**Behavior:** Non-blocking — hook failures are logged but don't halt workflow

### Position in `/qa` Workflow

```
Phase 05: QA Report Generation
    ↓
Phase 06: Feedback Hooks Workflow  ← FEEDBACK TRIGGERED
    ↓
Phase 07: Story Updates
```

**Behavior:** Non-blocking — QA result is immutable regardless of hook outcome

### Other Trigger Points

| Command | When Feedback Triggers |
|---------|------------------------|
| `/orchestrate` | After each phase (dev, qa, release) |
| `/release` | After deployment completes |
| `/create-story` | After story creation completes |
| `/create-epic` | After epic creation completes |
| `/create-sprint` | After sprint planning completes |

### Manual Invocation

Trigger feedback manually at any time:
```bash
/feedback
```

Or invoke the skill directly:
```
Skill(command="devforgeai-feedback")
```

---

## Feedback Types

The system supports five types of feedback collection:

### 1. Conversation (Default)

Interactive Q&A with 3-5 context-aware questions.

```yaml
feedback_type: conversation
feedback_config:
  mode: focused
  questions:
    - "What challenges did you encounter during TDD?"
    - "Were acceptance criteria clear and testable?"
    - "Did you defer any DoD items? Why?"
```

**Best for:** Detailed qualitative feedback after development or QA

### 2. Summary

Auto-generated operation summary without user interaction.

```yaml
feedback_type: summary
summary_sections:
  - duration
  - test_results
  - deferrals
  - next_steps
```

**Best for:** Quick documentation of operation outcomes

### 3. Metrics

Quantitative data collection for analysis.

```yaml
feedback_type: metrics
metrics:
  - execution_time
  - token_usage
  - test_pass_rate
  - coverage_percentage
```

**Best for:** Performance tracking and trend analysis

### 4. Checklist

Interactive retrospective checklist.

```yaml
feedback_type: checklist
checklist_items:
  - "Sprint capacity realistic?"
  - "Dependencies identified early?"
  - "Tests written before implementation?"
  - "Code review completed?"
```

**Best for:** Sprint retrospectives and process compliance

### 5. AI Architectural Analysis (Enhanced)

AI-generated framework improvement recommendations with **real-time observation capture**. This captures Claude's architectural insights during and after workflows - NOT user-facing feedback.

#### How It Works: Two-Part System

**Part 1: Observation Capture (Phases 01-08)**

As Claude works through each development phase, it captures "friction notes" - things that worked well, caused friction, or could be improved.

```
Phase 01 completes → Capture observations → phase-state.json
Phase 02 completes → Capture observations → phase-state.json
... (phases 03-08) ...
Phase 09 starts → framework-analyst subagent reads observations
```

**Observation Categories:**
| Category | When to Log | Examples |
|----------|-------------|----------|
| `friction` | Something slowed you down | "Had to read 4 files to find naming convention" |
| `success` | Something worked well | "anti-patterns.md caught God Object before commit" |
| `pattern` | Noticed repeated behavior | "3rd time manually updating DoD - should automate" |
| `gap` | Missing documentation/tooling | "No example for handling edge case X" |
| `idea` | Improvement opportunity | "Phase could run in parallel with previous" |
| `bug` | Framework defect discovered | "CLI exits 0 even on validation failure" |

**Part 2: Subagent Synthesis (Phase 09)**

The `framework-analyst` subagent (DevForgeAI expert) reads the captured observations and:
1. Expands terse notes into structured recommendations
2. Validates each recommendation (file paths, effort, feasibility)
3. Applies merit filter (no duplicates, not already implemented)
4. Stores meritorious items to queue

```yaml
feedback_type: ai_analysis
feedback_config:
  mode: architectural
  observation_capture: true  # NEW - enables inline capture
  analysis_prompts:
    - what_worked_well
    - areas_for_improvement
    - recommendations
    - patterns_observed
    - constraint_analysis
  constraint_check: claude-code-terminal
```

**What it captures:**
- What aspects of the framework worked well
- Areas for improvement (non-aspirational, implementable)
- Specific, actionable recommendations with priority
- Patterns observed during workflow
- Anti-patterns detected
- Constraint effectiveness analysis

**Key constraint:** All recommendations MUST be implementable within Claude Code Terminal.

**Storage:** `devforgeai/feedback/ai-analysis/{STORY_ID}/`

**Best for:** Continuous framework improvement, systematizing post-workflow architectural advice

**Validation Gate (Strict):**

Recommendations are rejected if they contain:
- Aspirational language: "could", "might", "consider", "should explore", "potentially"
- Missing file paths (each recommendation MUST cite specific files)
- Missing effort estimates (valid: "15 min", "30 min", "1 hour", "2 hours", "4 hours")
- `feasible_in_claude_code: false` or missing

**Example output (expanded schema):**
```json
{
  "story_id": "STORY-XXX",
  "workflow_type": "dev",
  "analysis_date": "2025-12-29T10:00:00Z",
  "observations_processed": 3,
  "what_worked_well": [
    {
      "observation": "Phase state validation prevented skipping Phase 03",
      "evidence": ".claude/scripts/devforgeai_cli/commands/phase_commands.py:45",
      "impact": "Enforced TDD discipline, caught implementation without tests"
    }
  ],
  "areas_for_improvement": [
    {
      "issue": "Test naming convention for shell scripts unclear",
      "evidence": "Checked test-automator.md, tdd-patterns.md - no shell guidance",
      "root_cause": "Framework originally designed for Python/JS, shell testing added later"
    }
  ],
  "recommendations": [
    {
      "title": "Document shell script test naming convention",
      "description": "Add explicit guidance for shell script test naming",
      "affected_files": [".claude/agents/test-automator.md"],
      "implementation_code": "Add ### Shell Script Testing section with Bats/shell patterns",
      "effort_estimate": "15 min",
      "priority": "MEDIUM",
      "feasible_in_claude_code": true
    }
  ],
  "patterns_observed": ["Phase state enforcement working well across all 10 phases"],
  "anti_patterns_detected": [],
  "constraint_analysis": "Context files effectively prevented 2 anti-pattern violations"
}
```

#### Converting Recommendations to Stories

Use `/recommendations-triage` to convert accumulated recommendations to user stories:

```bash
# View all pending recommendations
/recommendations-triage

# Filter by priority
/recommendations-triage --priority=HIGH

# Convert selected recommendations to stories
# (Interactive multi-select, then invokes /create-story)
```

See [AI Analysis Hook Guide](./ai-analysis-hook-guide.md) for detailed documentation.

---

## Commands Reference

### Core Feedback Commands

| Command | Purpose | Example |
|---------|---------|---------|
| `/feedback` | Manual feedback collection | `/feedback` |
| `/feedback-config` | View/edit configuration | `/feedback-config` |
| `/feedback-search` | Search feedback history | `/feedback-search STORY-001` |
| `/feedback-search --type=ai-analysis` | Search AI recommendations | `/feedback-search --type=ai-analysis --priority=high` |
| `/export-feedback` | Export feedback data | `/export-feedback --format=json` |
| `/feedback-reindex` | Rebuild feedback index | `/feedback-reindex` |
| `/audit-hooks` | Audit hook registry | `/audit-hooks` |
| `/recommendations-triage` | Convert AI recommendations to stories | `/recommendations-triage --priority=HIGH` |

### Feedback Search Examples

```bash
# Search by story
/feedback-search STORY-001

# Search by date range
/feedback-search 2025-11-01..2025-11-07

# Search by operation type
/feedback-search dev

# Search with filters
/feedback-search STORY-001 --severity=high --limit=20

# Complex query
/feedback-search 2025-11-01..2025-11-07 --status=open --limit=50

# AI Analysis searches (NEW)
/feedback-search --type=ai-analysis --priority=high

# Find patterns across stories
/feedback-search --type=patterns --story-range=STORY-001..STORY-050

# Export AI recommendations for review
/export-feedback --type=ai-analysis --format=markdown
```

### Export Options

```bash
# Export all feedback as JSON
/export-feedback --format=json --output=feedback-export.json

# Export specific story feedback
/export-feedback --story=STORY-001 --format=json

# Export with date filter
/export-feedback --from=2025-11-01 --to=2025-11-30
```

---

## Data Storage & Privacy

### Storage Location

```
devforgeai/feedback/
├── config.yaml              # System configuration
├── feedback-index.json      # Searchable session index
├── questions.yaml           # Question bank
├── STORY-001/
│   └── 20250109_143022-retrospective.json
├── STORY-002/
│   └── 20250109_150145-retrospective.json
├── anonymized/              # Post-retention anonymized data
└── sensitive/               # Encrypted sensitive feedback
```

### What IS Stored

| Data | Stored | Notes |
|------|--------|-------|
| Workflow type | Yes | dev, qa, orchestrate, etc. |
| Story/Epic ID | Yes | For correlation |
| Operation outcome | Yes | success, failed, partial |
| Your responses | Yes | Answers to questions |
| Timestamp | Yes | When submitted |
| Duration | Yes | How long operation took |
| Questions asked | Yes | For context |

### What IS NOT Stored

| Data | Stored | Reason |
|------|--------|--------|
| Personal info | No | Privacy by design |
| API keys | No | Security |
| Code snippets | No | Security |
| File paths | No | Privacy |
| System info | No | Privacy |
| Conversation history | No | Scope limitation |

### Retention Policy

**Default Timeline:**

| Period | Action |
|--------|--------|
| Months 1-12 | Active storage, full access |
| Month 12 | 30-day notice before action |
| After Month 12 | User chooses: Delete, Anonymize (default), Archive, Extend |

**Retention Actions:**

| Action | Description |
|--------|-------------|
| **Delete** | Permanent removal, cannot be recovered |
| **Anonymize** (default) | Remove story ID, keep aggregated insights |
| **Archive** | Keep with archived flag, exclude from analysis |
| **Extend** | Add another 12 months retention |

**Sensitive Feedback:** 18-month retention (encrypted at rest)

### User Control

You have full control over your feedback data:

- **Export** — Download all your data anytime (JSON format)
- **Delete** — Remove specific sessions or all data
- **Anonymize** — Remove identifying info, keep insights
- **Opt Out** — Disable feedback collection entirely
- **Modify** — Edit or annotate past feedback

### Compliance

| Standard | Support |
|----------|---------|
| **GDPR** | Right to be forgotten, data portability, access |
| **CCPA** | Right to know, delete, opt-out, non-discrimination |
| **SOC 2** | Security, availability, confidentiality, privacy |

---

## Quick Start

### Enable Feedback

Edit `devforgeai/config/feedback.yaml`:

```yaml
enabled: true
trigger_mode: failures-only  # Start conservatively
```

### Disable Feedback

```yaml
enabled: false  # Master switch - disables all feedback
```

### Customize Questions

Add custom questions in `devforgeai/config/hooks.yaml`:

```yaml
hooks:
  - id: my-custom-feedback
    name: "Custom Development Feedback"
    operation_type: command
    operation_pattern: "dev"
    trigger_status: [success, partial]
    feedback_type: conversation
    feedback_config:
      mode: focused
      questions:
        - "Was the TDD workflow helpful?"
        - "What would make development faster?"
        - "Any suggestions for improvement?"
    max_duration_ms: 5000
    enabled: true
```

### Skip Feedback Temporarily

Users can always skip feedback:
- **Individual Skip** — Skip current question, continue to next
- **Session Skip** — Exit feedback session entirely
- **Auto-Pause** — After 3 consecutive skips, system suggests disabling

---

## Architecture Overview

The feedback system uses an **event-driven hook architecture**:

```
┌─────────────────────┐
│  Operation Complete │
│  (dev, qa, release) │
└──────────┬──────────┘
           ↓
┌─────────────────────┐
│   Hook System       │
│   - Pattern match   │
│   - Condition check │
│   - Circular detect │
└──────────┬──────────┘
           ↓
┌─────────────────────┐
│  Feedback Skill     │
│  - Question select  │
│  - User interaction │
│  - Response capture │
└──────────┬──────────┘
           ↓
┌─────────────────────┐
│   Storage Layer     │
│   - Session save    │
│   - Index update    │
│   - Retention apply │
└─────────────────────┘
```

### Key Modules

| Module | Responsibility |
|--------|----------------|
| `hook_system.py` | Main coordinator and public API |
| `hook_registry.py` | YAML configuration loading |
| `hook_patterns.py` | Pattern matching (exact/glob/regex) |
| `hook_conditions.py` | Trigger condition evaluation |
| `hook_invocation.py` | Hook execution orchestration |
| `hook_circular.py` | Circular dependency detection |

### Non-Blocking Guarantee

**Critical Design Principle:** Hook failures NEVER affect primary operations.

```
Operation completes → SUCCESS
    ↓
Hook triggered
    ↓
Hook fails (timeout, error, etc.)
    ↓
Error logged, user notified (optional)
    ↓
Operation result unchanged → SUCCESS
```

### Pattern Matching

Hooks support three pattern types:

| Type | Example | Matches |
|------|---------|---------|
| Exact | `"dev"` | Only "dev" |
| Glob | `"create-*"` | "create-story", "create-epic", etc. |
| Regex | `"^(dev\|qa)$"` | "dev" or "qa" only |

---

## Related Documentation

| Document | Description |
|----------|-------------|
| [User Guide](./feedback-system-user-guide.md) | Detailed configuration and use cases |
| [AI Analysis Hook Guide](./ai-analysis-hook-guide.md) | Observation capture and framework improvement workflow |
| [Troubleshooting](./feedback-troubleshooting.md) | Common issues and solutions |
| [Migration Guide](./feedback-migration-guide.md) | Enable on existing projects |
| [Hook System Design](../architecture/hook-system-design.md) | Technical architecture |

---

## Summary

The DevForgeAI Feedback System is a sophisticated, non-blocking retrospective mechanism that:

1. **Triggers automatically** via event-driven hooks
2. **Captures structured insights** through adaptive questions
3. **Respects privacy** with local-only storage and user control
4. **Integrates seamlessly** with development workflows
5. **Enables continuous improvement** through aggregated analysis

It's designed to be **helpful, not intrusive** — questions are adaptive (3-5 max), collection is configurable, and you maintain complete control over your data.

---

[← Back to Documentation Index](../README.md)
