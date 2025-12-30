# AI Analysis Hook Guide

A comprehensive guide to the DevForgeAI framework self-improvement system that captures workflow observations and synthesizes them into actionable improvement recommendations.

---

## Table of Contents

1. [Overview](#overview)
2. [Architecture](#architecture)
3. [Observation Capture Protocol](#observation-capture-protocol)
4. [Framework Analyst Subagent](#framework-analyst-subagent)
5. [Validation & Merit Filter](#validation--merit-filter)
6. [Recommendations Triage](#recommendations-triage)
7. [Data Flow & Storage](#data-flow--storage)
8. [Configuration](#configuration)
9. [Troubleshooting](#troubleshooting)
10. [Design Commentary](#design-commentary)

---

## Overview

### What It Does

The AI Analysis Hook creates a **self-improvement loop** for DevForgeAI:

1. **Captures observations** during `/dev` workflow (phases 01-08)
2. **Synthesizes recommendations** via specialized subagent (phase 09)
3. **Stores meritorious items** in a priority queue
4. **Enables story creation** via `/recommendations-triage` command

### Why It Exists

Before this system, framework improvement insights were:
- Lost when context windows cleared
- Captured inconsistently (sometimes in docs, sometimes nowhere)
- Not actionable (vague or aspirational)
- Not validated (no feasibility checks)

This system ensures:
- **Real-time capture** — Observations logged as they happen
- **Structured output** — JSON with required fields
- **Quality enforcement** — Validation gates block aspirational content
- **Actionability** — Each recommendation has file paths, effort estimates, implementation code

### Quick Start

```bash
# 1. Run development workflow (observations captured automatically)
/dev STORY-001

# 2. View captured recommendations
/recommendations-triage

# 3. Select recommendations to convert to stories
# (Interactive multi-select)

# 4. Implement the selected framework improvements
/dev STORY-XXX  # (new story created from recommendation)
```

---

## Architecture

### System Components

```
┌─────────────────────────────────────────────────────────────────────┐
│                    /dev Workflow (10 Phases)                        │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  Phase 01  →  Phase 02  →  Phase 03  →  ... →  Phase 08             │
│     │            │            │                    │                │
│     ▼            ▼            ▼                    ▼                │
│  ┌──────────────────────────────────────────────────────────┐       │
│  │              Observation Capture                          │       │
│  │  (friction, success, pattern, gap, idea, bug)             │       │
│  │  Stored in: phase-state.json → observations[]             │       │
│  └─────────────────────────┬────────────────────────────────┘       │
│                            │                                        │
│                            ▼                                        │
│  ┌──────────────────────────────────────────────────────────┐       │
│  │              Phase 09: Feedback Hook                      │       │
│  │                                                           │       │
│  │  1. Read phase-state.json observations                    │       │
│  │  2. Task(subagent_type="framework-analyst")               │       │
│  │  3. Validate output (JSON, aspirational, evidence)        │       │
│  │  4. Apply merit filter (duplicates, already-implemented)  │       │
│  │  5. Store to devforgeai/feedback/ai-analysis/             │       │
│  └─────────────────────────┬────────────────────────────────┘       │
│                            │                                        │
│                            ▼                                        │
│                       Phase 10                                      │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────────┐
│                 /recommendations-triage                              │
├─────────────────────────────────────────────────────────────────────┤
│  1. Read recommendations-queue.json                                  │
│  2. Display by priority (HIGH → MEDIUM → LOW)                        │
│  3. User multi-select                                                │
│  4. Invoke /create-story for each selected                           │
│  5. Mark converted items in queue                                    │
└─────────────────────────────────────────────────────────────────────┘
```

### Files Involved

| File | Purpose |
|------|---------|
| `.claude/skills/devforgeai-development/references/observation-capture.md` | Observation protocol documentation |
| `.claude/skills/devforgeai-development/phases/phase-01-08.md` | Phases with observation capture prompts |
| `.claude/skills/devforgeai-development/phases/phase-09-feedback.md` | Subagent invocation and validation |
| `.claude/agents/framework-analyst.md` | Subagent definition |
| `.claude/commands/recommendations-triage.md` | Triage command |
| `devforgeai/workflows/{STORY_ID}-phase-state.json` | Observation storage |
| `devforgeai/feedback/ai-analysis/aggregated/recommendations-queue.json` | Priority queue |

---

## Observation Capture Protocol

### When to Capture

At the end of each phase (01-08), reflect on:

1. **Friction** — Did anything slow you down or require workarounds?
2. **Success** — Did anything work particularly well?
3. **Patterns** — Did you notice repeated behavior (good or bad)?
4. **Gaps** — Is there missing documentation, tooling, or guidance?
5. **Ideas** — Are there improvement opportunities?
6. **Bugs** — Did you discover any framework defects?

### Observation Schema

```json
{
  "id": "obs-02-001",
  "phase": "02",
  "category": "friction",
  "note": "Unclear how to name test files for shell scripts - checked 3 examples",
  "files": ["tests/STORY-XXX/", ".claude/agents/test-automator.md"],
  "severity": "medium"
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `id` | string | Yes | Format: `obs-{phase}-{sequence}` (e.g., `obs-02-001`) |
| `phase` | string | Yes | Phase number where observation occurred (01-08) |
| `category` | enum | Yes | One of: friction, success, pattern, gap, idea, bug |
| `note` | string | Yes | Brief description (1-2 sentences, max 200 chars) |
| `files` | array | No | Related file paths (helps subagent find context) |
| `severity` | enum | Yes | One of: low, medium, high |

### Severity Guidelines

| Severity | Criteria |
|----------|----------|
| `low` | Minor inconvenience, polish item |
| `medium` | Noticeable friction, should be addressed |
| `high` | Significant blocker, caused error, or prevented quality work |

### Storage Location

Observations are appended to the `observations` array in `phase-state.json`:

```json
{
  "story_id": "STORY-XXX",
  "phases": { ... },
  "observations": [
    { "id": "obs-02-001", "phase": "02", ... },
    { "id": "obs-03-001", "phase": "03", ... }
  ]
}
```

---

## Framework Analyst Subagent

### Purpose

The `framework-analyst` subagent is a **DevForgeAI expert** that transforms terse observation notes into structured, validated recommendations.

### Why a Subagent?

1. **Fresh context window** — Not fatigued from 8 phases of development
2. **Expert perspective** — Specialized in framework architecture
3. **Consistent output** — Same validation rules every time
4. **Read-only safety** — Can only Read, Grep, Glob (cannot modify files)

### Invocation

```
Task(
  subagent_type="framework-analyst",
  prompt="Analyze the ${STORY_ID} workflow execution and generate framework improvement recommendations.

INPUT:
- Story ID: ${STORY_ID}
- Workflow Type: dev
- Phase State Path: devforgeai/workflows/${STORY_ID}-phase-state.json

INSTRUCTIONS:
1. Read phase-state.json and extract observations array
2. Read each file mentioned in observations to gather context
3. Check recommendations-queue.json for duplicates
4. Expand terse observations into structured recommendations
5. Return ONLY valid JSON matching the required schema"
)
```

### Output Schema

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
      "impact": "Enforced TDD discipline"
    }
  ],
  "areas_for_improvement": [
    {
      "issue": "Test naming convention for shell scripts unclear",
      "evidence": "Checked test-automator.md - no shell guidance",
      "root_cause": "Framework designed for Python/JS, shell added later"
    }
  ],
  "recommendations": [
    {
      "title": "Document shell script test naming convention",
      "description": "Add explicit guidance for shell script test naming",
      "affected_files": [".claude/agents/test-automator.md"],
      "implementation_code": "Add ### Shell Script Testing section",
      "effort_estimate": "15 min",
      "priority": "MEDIUM",
      "feasible_in_claude_code": true
    }
  ],
  "patterns_observed": ["Phase state enforcement working well"],
  "anti_patterns_detected": [],
  "constraint_analysis": "Context files prevented 2 violations"
}
```

---

## Validation & Merit Filter

### Validation Gate (Blocking)

Recommendations are **rejected** if ANY of these checks fail:

| Check | What It Validates | Failure Action |
|-------|-------------------|----------------|
| JSON Schema | Valid JSON, required fields present | Reject entire output |
| Aspirational Language | No "could", "might", "consider", "should explore", "potentially", "possibly", "maybe", "perhaps" | Reject output |
| Evidence Requirement | Each item has non-empty evidence/affected_files | Reject output |
| Effort Estimate | Valid format ("15 min", "30 min", "1 hour", etc.) | Reject output |
| Feasibility | `feasible_in_claude_code: true` present | Reject output |

### Merit Filter (Post-Validation)

For recommendations that pass validation:

| Check | Criteria | Action |
|-------|----------|--------|
| Duplicate | >80% similarity to existing queue item | Filter out |
| Already Implemented | Affected file modified in last 7 days with related commit message | Filter out |

### Why So Strict?

The validation is intentionally strict because:

1. **Aspirational content is useless** — "We could consider improving X" provides no actionable guidance
2. **Missing file paths prevent implementation** — Without knowing what to modify, recommendations stall
3. **Effort estimates enable prioritization** — Teams can plan capacity
4. **Duplicates waste time** — Reviewing the same recommendation twice is inefficient

---

## Recommendations Triage

### Command Usage

```bash
# Show all pending recommendations
/recommendations-triage

# Filter by priority
/recommendations-triage --priority=HIGH

# Limit results
/recommendations-triage --limit=10
```

### Workflow

1. **Read Queue** — Load `recommendations-queue.json`
2. **Display** — Show recommendations grouped by priority (HIGH → MEDIUM → LOW)
3. **Select** — User multi-select via AskUserQuestion
4. **Create Stories** — For each selected, invoke `/create-story` with pre-filled context
5. **Update Queue** — Mark converted items, move to `implemented` array

### Story Creation

When a recommendation is converted to a story:

- Feature description pre-filled from recommendation
- `source: framework-enhancement` tag added
- Priority inherited from recommendation
- Affected files documented in technical specification

---

## Data Flow & Storage

### Directory Structure

```
devforgeai/feedback/ai-analysis/
├── index.json                           # Session index
├── aggregated/
│   ├── recommendations-queue.json       # Priority queue
│   └── patterns-detected.json           # Aggregated patterns
└── {STORY_ID}/
    └── {TIMESTAMP}-ai-analysis.json     # Individual analysis
```

### Recommendations Queue Schema

```json
{
  "version": "1.0",
  "last_updated": "2025-12-29T10:00:00Z",
  "recommendations": {
    "high": [
      {
        "id": "rec-001",
        "title": "...",
        "source_story": "STORY-001",
        "created_at": "...",
        ...
      }
    ],
    "medium": [],
    "low": []
  },
  "implemented": [
    {
      "original_recommendation": { ... },
      "converted_to_story": "STORY-050",
      "converted_at": "2025-12-29T11:00:00Z"
    }
  ],
  "deferred": []
}
```

---

## Configuration

### Enable/Disable AI Analysis

In `devforgeai/config/hooks.yaml`:

```yaml
hooks:
  - id: post-dev-ai-analysis
    name: "Post-Development AI Analysis"
    operation_type: command
    operation_pattern: "dev"
    trigger_status: [success, partial]
    feedback_type: ai_analysis
    enabled: true  # Set to false to disable
```

### Observation Capture Toggle

Observation capture is enabled by default in phases 01-08. To disable, remove the "Observation Capture" section from phase files.

### Merit Filter Thresholds

Currently hardcoded (future: configurable):
- Duplicate similarity threshold: 80%
- Already-implemented lookback: 7 days

---

## Troubleshooting

### No Observations Captured

**Symptoms:** Phase 09 reports "0 observations processed"

**Causes:**
- Observation capture section missing from phase files
- No friction/issues encountered (legitimate)
- phase-state.json not found

**Resolution:**
1. Verify phases 01-08 have "Observation Capture" section
2. Check `devforgeai/workflows/{STORY_ID}-phase-state.json` exists
3. If genuinely no issues, this is expected behavior

### Validation Failures

**Symptoms:** "AI Analysis validation failed: [reason]"

**Causes:**
- Subagent returned aspirational language
- Missing required fields
- Invalid JSON

**Resolution:**
- Non-blocking — workflow continues
- Check `framework-analyst.md` subagent constraints
- Review recent output for patterns

### Empty Recommendations Queue

**Symptoms:** `/recommendations-triage` shows "No pending recommendations"

**Causes:**
- No `/dev` workflows completed yet
- All recommendations filtered (duplicates, already-implemented)
- AI analysis disabled

**Resolution:**
1. Run `/dev` on a story
2. Check `recommendations-queue.json` for filtered items
3. Verify `post-dev-ai-analysis` hook is enabled

### Subagent Not Invoked

**Symptoms:** Phase 09 skips AI analysis

**Causes:**
- Phase 09 file missing subagent invocation
- `framework-analyst.md` agent file missing

**Resolution:**
1. Verify `.claude/agents/framework-analyst.md` exists
2. Verify Phase 09 has `Task(subagent_type="framework-analyst", ...)` call

---

## Design Commentary

### Why Inline Observation Capture?

**Alternative considered:** Invoke a separate subagent at the end of each phase to capture observations.

**Why rejected:** Too much overhead (8 extra subagent calls), increased latency, complex coordination.

**Chosen approach:** Primary Claude captures terse notes inline (low overhead), single expert subagent synthesizes at Phase 09 (quality expansion).

### Why a Separate Subagent for Synthesis?

**Alternative considered:** Have primary Claude generate recommendations after Phase 08.

**Why rejected:** By Phase 08, Claude has been working for 30+ minutes. Context fatigue leads to lower-quality recommendations (more aspirational, less specific).

**Chosen approach:** Fresh subagent with specialized prompt ensures consistent, high-quality output.

### Why Strict Validation?

**Alternative considered:** Accept all recommendations, let humans filter.

**Why rejected:** Creates noise, wastes review time, sets bad precedent for quality.

**Chosen approach:** Strict machine validation ensures only actionable items reach the queue. Better to reject 10 vague recommendations than pollute the queue.

### Why Explicit Story Creation (Not Auto-Create)?

**Alternative considered:** Automatically create stories from HIGH priority recommendations.

**Why rejected:** Violates user authority principle. Users should decide which improvements to pursue and when.

**Chosen approach:** `/recommendations-triage` requires explicit user selection. User remains in control of the backlog.

### Why Store in phase-state.json?

**Alternative considered:** Separate observations file per story.

**Why rejected:** Creates file proliferation, complicates cleanup, duplicates story ID tracking.

**Chosen approach:** Leverage existing phase-state.json infrastructure. Observations are part of the workflow state.

---

## Summary

The AI Analysis Hook creates a sustainable self-improvement loop:

1. **Capture** — Observations logged during phases 01-08
2. **Synthesize** — Expert subagent expands into recommendations
3. **Validate** — Strict gates ensure quality
4. **Queue** — Priority-based storage
5. **Triage** — User-controlled story creation

This ensures framework improvements are:
- **Captured** before context is lost
- **Specific** with file paths and effort estimates
- **Actionable** with implementation guidance
- **Validated** against Claude Code Terminal constraints
- **User-controlled** via explicit triage

---

[← Back to Feedback Overview](./feedback-overview.md) | [Feedback Troubleshooting →](./feedback-troubleshooting.md)
