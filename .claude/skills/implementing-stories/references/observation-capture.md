# Observation Capture Protocol

Capture framework improvement observations during /dev workflow execution for later synthesis into actionable recommendations.

---

## Purpose

Enable DevForgeAI self-improvement by capturing "friction notes" as Claude works through each phase. These observations become input for the `framework-analyst` subagent at Phase 09.

---

## Categories

| Category | When to Log | Examples |
|----------|-------------|----------|
| `friction` | Something slowed you down or required workaround | "Had to read 4 files to find naming convention", "Unclear which subagent to use" |
| `success` | Something worked well, saved time, or prevented error | "anti-patterns.md caught God Object before commit", "Phase state resume worked perfectly" |
| `pattern` | Noticed repeated behavior (good or bad) | "3rd time manually updating DoD - should automate", "Same validation logic in 3 phases" |
| `gap` | Missing documentation, tooling, or guidance | "No example for handling edge case X", "Missing error message for Y scenario" |
| `idea` | Improvement opportunity or enhancement | "Phase could run in parallel with previous", "Subagent could cache this result" |
| `bug` | Framework defect discovered during workflow | "CLI exits 0 even on validation failure", "Lock file not cleaned up on error" |

---

## Schema

Observations are stored in the `observations` array of `phase-state.json`:

```json
{
  "story_id": "STORY-XXX",
  "phases": { ... },
  "observations": [
    {
      "id": "obs-02-001",
      "phase": "02",
      "source": "test-automator",
      "category": "friction",
      "note": "Unclear how to name test files for shell scripts - had to check 3 examples",
      "files": ["tests/STORY-XXX/", ".claude/agents/test-automator.md"],
      "severity": "medium",
      "timestamp": "2026-02-16T10:15:00Z"
    },
    {
      "id": "obs-03-001",
      "phase": "03",
      "source": "backend-architect",
      "category": "success",
      "note": "anti-patterns.md constraint prevented class from exceeding 500 lines",
      "files": ["devforgeai/specs/context/anti-patterns.md"],
      "severity": "high",
      "timestamp": "2026-02-16T11:30:00Z"
    }
  ]
}
```

### Field Definitions

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `id` | string | Yes | Format: `obs-{phase}-{sequence}` (e.g., `obs-02-001`) |
| `phase` | string | Yes | Phase number where observation occurred (01-08) |
| `source` | string | Yes | Subagent name that produced the observation (e.g., "test-automator", "backend-architect") |
| `category` | enum | Yes | One of: friction, success, pattern, gap, idea, bug |
| `note` | string | Yes | Brief description (1-2 sentences, max 200 chars) |
| `files` | array | No | Related file paths (if applicable) |
| `severity` | enum | Yes | One of: low, medium, high |
| `timestamp` | string | Yes | ISO 8601 format (e.g., "2026-02-08T10:00:00Z") |

### Severity Guidelines

| Severity | Criteria |
|----------|----------|
| `low` | Minor inconvenience, polish item |
| `medium` | Noticeable friction, should be addressed |
| `high` | Significant blocker, caused error, or prevented quality work |

### Phase-to-Subagent Mapping

| Phase | Subagent | Capture Observations |
|-------|----------|---------------------|
| Phase 02 (Red) | test-automator | Yes |
| Phase 03 (Green) | backend-architect OR frontend-developer | Yes |
| Phase 04 (Refactor) | refactoring-specialist | Yes |
| Phase 04.5 (AC Verify) | ac-compliance-verifier | Yes |
| Phase 05 (Integration) | integration-tester | Yes |
| Phase 05.5 (AC Verify) | ac-compliance-verifier | Yes |
| Phase 06 (Deferral) | deferral-validator | Yes (if deferrals exist) |
| Phase 07 (DoD Update) | None | No (skip) |
| Phase 08 (Git) | None | No (skip) |

---

## Capture Prompt

Add this prompt to the exit of each phase (01-08):

```markdown
### Observation Capture (Before Exit)

**Before marking this phase complete, reflect:**
1. Did I encounter any friction? (unclear docs, missing tools, workarounds needed)
2. Did anything work particularly well? (constraints that helped, patterns that fit)
3. Did I notice any repeated patterns across phases?
4. Are there gaps in tooling/docs that would help future stories?
5. Did I discover any bugs or unexpected behavior?

**If YES to any:** Append observation to phase-state.json `observations` array:
```json
{
  "id": "obs-{phase}-{seq}",
  "phase": "{current_phase}",
  "source": "{subagent_name}",
  "category": "{friction|success|pattern|gap|idea|bug}",
  "note": "{1-2 sentence description}",
  "files": ["{relevant files if any}"],
  "severity": "{low|medium|high}",
  "timestamp": "{ISO_8601_timestamp}"
}
```

**If NO observations:** Continue to exit gate (no action needed).
```

---

## Examples

### Example 1: Friction Observation

**Scenario:** During Phase 02 (Test-First), Claude couldn't find the test naming convention.

```json
{
  "id": "obs-02-001",
  "phase": "02",
  "source": "test-automator",
  "category": "friction",
  "note": "Test naming convention unclear - checked test-automator.md, tdd-patterns.md, and 2 example test files before finding pattern",
  "files": [".claude/agents/test-automator.md", "references/tdd-patterns.md"],
  "severity": "medium",
  "timestamp": "2026-02-16T10:15:00Z"
}
```

### Example 2: Success Observation

**Scenario:** During Phase 03 (Implementation), a context file constraint prevented a mistake.

```json
{
  "id": "obs-03-001",
  "phase": "03",
  "source": "backend-architect",
  "category": "success",
  "note": "architecture-constraints.md Single Responsibility Principle reminded me to split service class before it grew too large",
  "files": ["devforgeai/specs/context/architecture-constraints.md"],
  "severity": "high",
  "timestamp": "2026-02-16T11:30:00Z"
}
```

### Example 3: Pattern Observation

**Scenario:** During Phase 07 (DoD Update), Claude notices repeated manual work.

```json
{
  "id": "obs-07-001",
  "phase": "07",
  "source": "implementing-stories",
  "category": "pattern",
  "note": "This is the 3rd story where I manually updated Implementation Notes section - could be automated from phase-state.json",
  "files": ["references/dod-update-workflow.md"],
  "severity": "medium",
  "timestamp": "2026-02-16T14:45:00Z"
}
```

---

## Integration with Phase 09

At Phase 09, the `framework-analyst` subagent:

1. Reads `phase-state.json` including `observations` array
2. Expands terse notes into full recommendations
3. Validates each recommendation (file paths, effort, feasibility)
4. Applies merit filter (no duplicates, not already implemented)
5. Stores meritorious items to `devforgeai/feedback/ai-analysis/`

**Data Flow:**
```
Phases 01-08: Capture observations → phase-state.json
Phase 09: framework-analyst reads observations → synthesizes → stores recommendations
Later: /recommendations-triage → user selects → stories created
```

---

## Non-Blocking Capture Behavior

**CRITICAL:** Observation capture failures MUST NOT halt the TDD workflow.

```
TRY:
    execute_observation_capture()
CATCH any error:
    Display: "⚠️ Observation capture failed: {error_message}"
    Display: "   Continuing workflow (observation loss acceptable)"
    # Log warning and proceed - do NOT halt
```

---

## Backward Compatibility

When observation capture encounters a phase-state.json without an `observations` field:

1. Initialize `observations` as empty array: `[]`
2. Append new observations normally
3. No errors, no halting

---

## Constraints

1. **Keep notes brief** - 1-2 sentences, max 200 characters
2. **Include files when relevant** - Helps subagent find context
3. **Don't force observations** - Only log when something notable occurred
4. **Severity matters** - High severity items get priority in synthesis
5. **Phase must be accurate** - Enables correlation with phase-specific issues
6. **Source must be accurate** - Enables traceability to which subagent produced the observation
7. **Timestamp required** - Enables temporal ordering and correlation

---

## Sibling Story Pattern Reuse

When processing 3+ sibling stories from the same epic in a single session, reuse patterns established by the first story rather than rediscovering them each time.

### When to Reuse

| Condition | Action |
|-----------|--------|
| Batch workflow, 3+ stories from same epic, same session | Apply pattern reuse |
| Single story or stories from different epics | Standard capture (no reuse) |
| First story in batch | Establish patterns — note them in observations |
| Subsequent stories in batch | Reference first story as pattern source |

### What to Reuse

- **Test structure** — File layout, naming convention, runner script pattern established by story 1
- **Fixtures** — Shared setup/teardown patterns, mock data formats
- **Assertion patterns** — How AC conditions map to test assertions in this epic
- **Phase-state shape** — Any epic-specific fields added by story 1

### How to Reference

When reusing a pattern from the first story, log an observation citing it as the source:

```json
{
  "id": "obs-02-001",
  "phase": "02",
  "source": "test-automator",
  "category": "pattern",
  "note": "Reused test structure from STORY-NNN (sibling, same session) — no rediscovery needed",
  "files": ["tests/STORY-NNN/"],
  "severity": "low",
  "timestamp": "2026-02-16T10:15:00Z"
}
```

- Cite the first sibling story ID in `note` and `files`
- Use category `pattern` (not `success`) — this is structural reuse, not a one-off win
- Severity `low` unless the reuse prevented a significant error

### Cross-Reference: Batch Session Template

For full guidance on managing state across a sibling story batch session, including session-level pattern tracking and handoff between stories, apply:

**`.claude/memory/batch-sibling-story-session-template.md`**

| Usage Context | When to Apply |
|---------------|---------------|
| Starting a batch of 3+ sibling stories | Load template before story 1 to establish session tracking |
| Mid-batch context window pressure | Use template's checkpoint format to preserve pattern state |
| Handing off batch to new session | Use template's resume section to transfer established patterns |
