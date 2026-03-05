# DevForgeAI Developer Guide

**Last Updated:** 2026-03-04
**Applies To:** DevForgeAI Framework v1.x

---

## Table of Contents

- [Development Setup](#development-setup)
- [Project Structure](#project-structure)
- [Workflow Overview](#workflow-overview)
- [Testing](#testing)
- [Adding New Components](#adding-new-components)

---

## Development Setup

```bash
# Clone the repository
git clone https://github.com/bankielewicz/DevForgeAI.git
cd DevForgeAI

# Install Node.js dependencies
npm install

# Install Python CLI in development mode
pip install -e .claude/scripts/

# Verify installation
devforgeai-validate --help
npm test
```

### Prerequisites

- Node.js >= 18.0.0
- Python >= 3.10
- Git
- Claude Code Terminal

---

## Project Structure

DevForgeAI uses a dual-path architecture:

| Path | Purpose | Editable |
|------|---------|----------|
| `src/` | Development source files | Yes — all implementation work goes here |
| `.claude/` | Operational runtime files | Synced from `src/` after changes |
| `devforgeai/specs/context/` | Constitutional constraint files | Requires ADR to modify |

Tests always run against the `src/` tree to avoid WSL path issues with operational folders.

---

## Workflow Overview

```
/brainstorm → /ideate → /create-context → /create-epic → /create-story → /dev → /qa → /release
```

Each slash command delegates to a skill in `.claude/skills/` which orchestrates subagents from `.claude/agents/`.

---

## Testing

```bash
# Node.js tests (Jest)
npm test
npm run test:unit
npm run test:coverage

# Python tests (pytest)
pytest .claude/scripts/devforgeai_cli/tests/
pytest .claude/scripts/devforgeai_cli/tests/ --cov=devforgeai_cli
```

---

## Adding New Components

| Component | Command | Location |
|-----------|---------|----------|
| Subagent | `/create-agent` | `.claude/agents/{name}.md` |
| Skill | Use `skill-creator` skill | `.claude/skills/{name}/SKILL.md` |
| Slash Command | Manual creation | `.claude/commands/{name}.md` |

All new components must be added to both `src/` and `.claude/` paths.

---

<!-- Module-specific developer guidance is appended below as sections -->

<!-- SECTION: assessing-entrepreneur START -->
## Assessing Entrepreneur

The `assessing-entrepreneur` skill collects self-reported work-style preferences across 6 dimensions and produces a structured profile at `devforgeai/specs/business/user-profile.yaml`. The profile drives plan calibration, task granularity, and coaching style across downstream business skills.

This skill never diagnoses mental health conditions. All questions capture self-reported preferences only.

### File Layout

| File | Purpose | Lines |
|------|---------|-------|
| `src/claude/skills/assessing-entrepreneur/SKILL.md` | 9-phase assessment workflow | ~196 |
| `src/claude/agents/entrepreneur-assessor.md` | Normalizes responses into profile | ~128 |
| `src/claude/skills/assessing-entrepreneur/references/work-style-questionnaire.md` | 12 questions across 6 dimensions | ~270 |
| `src/claude/skills/assessing-entrepreneur/references/plan-calibration-engine.md` | Maps profile to 7 adaptive dimensions | ~153 |
| `src/claude/skills/assessing-entrepreneur/references/adhd-adaptation-framework.md` | Focus and micro-chunking strategies | ~95 |
| `src/claude/skills/assessing-entrepreneur/references/confidence-assessment-workflow.md` | Progressive exposure techniques | ~121 |

### Assessment Dimensions

The questionnaire covers 6 dimensions, each asked via `AskUserQuestion` with bounded options (2-5 choices, some `multiSelect: true`):

1. **Work Style** -- daily structure, environment, collaboration (3 questions)
2. **Task Completion** -- project patterns, interruption recovery (2 questions)
3. **Motivation** -- primary drivers, drop-off points (2 questions, both multiSelect)
4. **Energy Management** -- peak focus hours, recovery methods (2 questions)
5. **Previous Attempts** -- experience level, lessons learned (2 questions)
6. **Self-Reported Challenges** -- primary challenges, support preferences (2 questions, both multiSelect)

### Profile Output

The entrepreneur-assessor subagent normalizes questionnaire responses into `devforgeai/specs/business/user-profile.yaml`. The profile contains two layers:

**Per-dimension data** (6 sections matching the questionnaire):

```yaml
dimensions:
  work_style:
    primary_pattern: "flexible-flow"
    secondary_pattern: "inspiration-driven"
    adaptations: ["flexible-scheduling", "environment-anchoring"]
  # ... 5 more dimension blocks
```

**7-dimension adaptive profile** (consumed by downstream skills):

```yaml
adaptive_profile:
  task_chunk_size: micro        # micro | standard | extended
  session_length: short         # short | medium | long
  check_in_frequency: frequent  # frequent | moderate | minimal
  progress_visualization: per_task  # per_task | daily | weekly
  celebration_intensity: high   # high | medium | low
  reminder_style: specific      # specific | balanced | gentle
  overwhelm_prevention: strict  # strict | moderate | open
```

### Architecture

```
SKILL.md (orchestrates phases 1-9)
  |
  |-- Phases 2-7: AskUserQuestion per dimension
  |       (questions loaded from references/work-style-questionnaire.md)
  |
  |-- Phase 8: Task(subagent_type="entrepreneur-assessor")
  |       Normalizes responses -> user-profile.yaml
  |
  |-- Phase 9: Results summary displayed to user
  |
  +-- Reference files loaded on demand:
        adhd-adaptation-framework.md    (Phase 8-9, focus challenges)
        confidence-assessment-workflow.md (Phase 8-9, confidence patterns)
        plan-calibration-engine.md       (Phase 8-9, plan adjustment)
```

The entrepreneur-assessor subagent handles normalization only (single responsibility). It does not generate plans or invoke other subagents. Its tools are restricted to `Read`, `Glob`, `Grep`, and `AskUserQuestion`.

### Extending the Module

**Adding a new dimension:**

1. Add questions to `references/work-style-questionnaire.md` under a new `## Dimension N:` section
2. Add a matching phase in `SKILL.md` between the last dimension phase and Phase 8
3. Update the `REQUIRED_DIMENSIONS` list in `tests/STORY-465/test_ac2_questionnaire_dimensions.py`
4. Add a dimension block to the `dimensions:` section of `user-profile.yaml`

**Adding a new adaptive profile field:**

1. Define the enum values and range in `references/plan-calibration-engine.md` under "Seven-Dimension Adaptive Calibration"
2. Add the field to the `adaptive_profile:` section in `SKILL.md` Profile Synthesis Output
3. Update `devforgeai/specs/business/user-profile.yaml` with the new field

**Adding a new reference file:**

1. Create the file in `src/claude/skills/assessing-entrepreneur/references/`
2. Add a row to the Reference Files table in `SKILL.md`
3. Add a test for the file in `tests/STORY-465/test_ac4_reference_files.py`

### Key Constraints

- All questions use `AskUserQuestion` with bounded options (not free-text). This keeps the assessment to ~10-15 minutes.
- Phase 1 requires explicit user consent before proceeding.
- The skill never uses diagnostic language. Use "self-reported", "preferences", "patterns" -- never "diagnosis", "condition", "disorder".
- Reference files use progressive disclosure: `SKILL.md` stays under 200 lines, deep content lives in `references/`.
- The subagent produces output framed as self-reported preferences, never clinical assessments.

### Tests

47 tests across 5 files in `tests/STORY-465/`:

| File | Tests | Validates |
|------|-------|-----------|
| `test_ac1_skill_structure.py` | 8 | SKILL.md path, frontmatter, size, name |
| `test_ac2_questionnaire_dimensions.py` | 14 | All 6 dimensions present, AskUserQuestion usage |
| `test_ac3_assessor_subagent.py` | 8 | Subagent path, frontmatter, tool restrictions |
| `test_ac4_reference_files.py` | 13 | 4 reference files exist with valid content |
| `test_ac5_safety_disclaimers.py` | 3 | Disclaimer present, no diagnostic language |

Run them with:

```bash
pytest tests/STORY-465/ -v
```
<!-- SECTION: assessing-entrepreneur END -->

<!-- SECTION: coaching-entrepreneur START -->
## Coaching Entrepreneur

The `coaching-entrepreneur` skill delivers adaptive business coaching by dynamically blending two personas — Coach (empathetic, encouraging) and Consultant (structured, deliverable-focused) — based on user emotional state and context. The skill reads the user profile from `/assess-me` to calibrate persona transitions, task granularity, and celebration intensity without modifying the profile. Emotional state tracking across sessions (STORY-468) extends the skill with a persistent session log that adapts the opening tone of each new session based on the user's self-reported state from the previous one.

### File Layout

| File | Purpose | Lines |
|------|---------|-------|
| `src/claude/skills/coaching-entrepreneur/SKILL.md` | Persona blend workflow and session orchestration | target ≤1000 |
| `src/claude/agents/business-coach.md` | Executes coaching logic with persona-aware prompting | target ≤500 |
| `src/claude/skills/coaching-entrepreneur/references/coach-persona-prompts.md` | Empathetic language patterns, win celebration, self-doubt addressing | ~140 |
| `src/claude/skills/coaching-entrepreneur/references/consultant-frameworks.md` | Structured frameworks, deliverable templates, professional language | ~150 |
| `src/claude/skills/coaching-entrepreneur/references/persona-blend-rules.md` | Decision logic for mode shifts (user-reported state, context signals) | ~110 |
| `src/claude/skills/coaching-entrepreneur/references/profile-adaptation-engine.md` | Maps user profile dimensions to persona blend ratio, task chunking, celebration | ~130 |
| `devforgeai/specs/business/coaching/session-log.yaml` | Persistent record of per-session emotional state and user overrides | grows per session |

### Persona Definitions

The skill defines two distinct, complementary personas:

**Coach Mode** (empathetic, emotional support):
- Triggers: User reports feeling overwhelmed, discouraged, stuck, or after completing difficult tasks
- Responsibilities: Normalize struggles, celebrate incremental progress, address self-doubt, build confidence

**Consultant Mode** (structured, deliverable-focused):
- Triggers: User reports focus, ready to work, clear on goals, or requests structured guidance
- Responsibilities: Define frameworks, break down projects, provide templates, track metrics

**Transition Rules:**
- Start in Coach mode by default (safer for new users when profile unavailable)
- If profile available, blend ratio depends on `adaptive_profile.celebration_intensity` and reported energy
- Shift within-session if user state changes
- Never switch abruptly; bridge transitions with acknowledgment

### Profile Integration

When a `user-profile.yaml` exists (from `/assess-me`), the coaching skill reads and applies it:

| Profile Field | Coach Mode Effect | Consultant Mode Effect |
|---|---|---|
| `celebration_intensity: high` | Frequent celebration, explicit wins | Milestone ceremonies |
| `task_chunk_size: micro` | Celebrate every small win | 5-15 min task modules |
| `reminder_style: specific` | "You've got this, next is X" | "Action required: X by date" |
| `overwhelm_prevention: strict` | Show 1-2 tasks only | Milestone view |

**Fallback:** If no profile exists, defaults to 60% Coach / 40% Consultant blend with standard task chunking.

### Architecture

```
SKILL.md (orchestrates coaching workflow)
  |
  |-- Phase 1: Initialization & Profile Loading
  |       Reads user-profile.yaml (if exists)
  |       Sets persona blend ratio and adaptation parameters
  |
  |-- Phase 2: Session Opening
  |       Coach mode: Greeting, check emotional state
  |       Consultant mode: Confirm session goals
  |
  |-- Phase 3: Task(subagent_type="business-coach")
  |       Executes conversation with persona-aware prompting
  |       Handles transitions mid-session
  |
  +-- Reference files loaded on demand:
        coach-persona-prompts.md        (empathy patterns)
        consultant-frameworks.md        (structures)
        persona-blend-rules.md          (decision logic)
        profile-adaptation-engine.md    (customization)
```

The business-coach subagent receives explicit persona blend instructions in its system prompt. Its tools are restricted to Read, Grep, Glob, and AskUserQuestion — no Write access.

### Extending the Module

**Adding a new persona:**

1. Create a new reference file: `references/{persona-name}-framework.md` with language patterns, triggers, and responsibilities
2. Add decision logic to `references/persona-blend-rules.md` for when to activate the new persona
3. Update `SKILL.md` initialization to include the new persona in blend calculations
4. Extend `references/profile-adaptation-engine.md` with mappings from profile fields to new-persona intensity
5. Add tests to `tests/STORY-467/test_ac2_persona_definitions.py` verifying the new persona is defined

**Adding a new profile-based adaptation:**

1. Identify the profile field(s) that drive the adaptation
2. Document the adaptation rule in `references/profile-adaptation-engine.md`
3. Update business-coach.md system prompt to include the new rule
4. Add test to `tests/STORY-467/test_ac4_profile_reading.py`

### Emotional State Tracking (STORY-468)

Emotional state tracking adds cross-session memory to the coaching skill. At the start of each session, the skill reads `session-log.yaml` to check how the user reported feeling in the previous session, then adapts its opening tone accordingly. At session end, the current emotional state and any user overrides are appended to the log.

#### Session Log Schema

Path: `devforgeai/specs/business/coaching/session-log.yaml`

```yaml
sessions:
  - date: "2026-03-04T14:30:00"
    emotional_state: "frustrated"
    override: null
  - date: "2026-03-05T09:15:00"
    emotional_state: "energized"
    override: null
```

**`emotional_state` enum** (7 values):

| Value | Typical Opening Tone Adaptation |
|-------|--------------------------------|
| `energized` | "You were on fire last time — ready to keep that momentum?" |
| `focused` | "Great focus last session. Let's build on that." |
| `neutral` | Standard session opening, no prior-state callout |
| `tired` | "Last session felt heavy. Let's start lighter today." |
| `frustrated` | "Last session seemed tough. No pressure — we go at your pace." |
| `anxious` | Opens in Coach mode regardless of profile blend ratio |
| `overwhelmed` | Opens in Coach mode, shows only 1-2 tasks in first exchange |

**First-session behaviour:** When no `session-log.yaml` exists, the skill skips the cross-session read and opens with the standard profile-based greeting. The log file is created on first session completion.

#### Adding a New Emotional State Enum Value

1. Add the value to the `emotional_state` enum in `SKILL.md` (the AskUserQuestion options list and schema documentation)
2. Add the corresponding opening tone example to the emotional state table in this developer guide section
3. Update `tests/STORY-468/test_ac1_session_log.py` — the expected enum values list
4. If the new state warrants a forced persona mode, document the rule in `references/persona-blend-rules.md`

#### Adding New Session Log Fields

1. Add the field to the session entry schema in `SKILL.md`
2. Update the schema table in this developer guide section
3. Extend the log-write phase in `SKILL.md` to populate the new field
4. Add a field-presence assertion to `tests/STORY-468/test_ac1_session_log.py`

### Key Constraints

- The skill never infers or diagnoses mental/emotional state. All persona shifts respond to user-reported state only. The AI must not inspect message sentiment or conversation history to estimate emotional state.
- Coaching skill is read-only for user-profile.yaml. Never attempt writes; respect the profile as immutable session context.
- Session log writes (`session-log.yaml`) are the only file Write the skill performs. All writes append to the `sessions` array — existing entries are never modified.
- Default to Coach mode when profile unavailable. Structure without encouragement is risky for new users.
- Default to `neutral` if the user skips the emotional check-in. Do not re-prompt.
- User overrides are respected immediately within the session and logged. The logged override is visible to the next session's tone adaptation logic.
- Persona blend instructions are fully templated in system prompts, not emergent.
- Reference files use progressive disclosure: `SKILL.md` stays under 1000 lines; deep persona content lives in `references/`.

### Tests

**STORY-467 tests** — persona blend engine (4 files in `tests/STORY-467/`):

| File | Validates |
|------|-----------|
| `test_ac1_coaching_skill_structure.py` | SKILL.md path, frontmatter, size < 1000 lines |
| `test_ac2_persona_definitions.py` | Coach and Consultant modes defined, triggers documented, transition rules present |
| `test_ac3_business_coach_subagent.py` | Subagent path, frontmatter, tools restricted, size < 500 lines |
| `test_ac4_profile_reading.py` | Profile read without writes, adaptation mappings present, fallback behavior defined |

**STORY-468 tests** — emotional state tracking (3 files in `tests/STORY-468/`):

| File | Validates |
|------|-----------|
| `test_ac1_session_log.py` | Session log path documented in SKILL.md, schema fields present, all 7 enum values defined |
| `test_ac2_tone_adaptation.py` | Previous-session read logic present, tone adaptation examples provided for each emotional state |
| `test_ac3_user_override.py` | Override handling documented, override logging specified in session close phase |

Coverage target for all STORY-468 tests: 95%.

Run the full coaching module test suite:

```bash
pytest tests/STORY-467/ tests/STORY-468/ -v
```
<!-- SECTION: coaching-entrepreneur END -->
