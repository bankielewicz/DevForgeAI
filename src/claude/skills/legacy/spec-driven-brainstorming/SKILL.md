---
name: spec-driven-brainstorming
description: >
  Interactive question-driven discovery skill that transforms vague business problems
  into a complete, self-contained HTML Business Analysis. Applies structural anti-skip
  enforcement (Execute-Verify-Gate pattern) to every step of the 11-phase Business
  Analysis workflow (Phase 00 is inline initialization).
  Prevents token optimization bias through lean orchestration, per-phase reference
  loading, and artifact verification. Use when user says "brainstorm", wants to
  explore a vague business problem, needs stakeholder analysis, or runs /brainstorm.
  Do NOT use when user has structured requirements (use spec-driven-ideation) or
  wants a business plan directly (use planning-business).
allowed-tools:
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - AskUserQuestion
  - Task
  - Skill
model: opus
effort: High
version: "2.0.0"
last-updated: "2026-05-17"
topics: brainstorm, discovery, business analysis, ideation, stakeholder, problem exploration, anti-skip
---

# Discovering Problems

Transform a vague business problem into a complete, self-contained HTML Business Analysis
through guided interactive questioning. Governed by **ADR-065**.

**Output:** `devforgeai/specs/brainstorms/BRAINSTORM-{NNN}-{short-name}.brainstorm.html`
**Embedded conduit:** a schema-validated JSON data island
(`<script type="application/json" id="brainstorm-data">`) inside the HTML — the
forward-compatible machine-readable handoff for downstream tooling.

---

## Anti-Skip Enforcement Contract

Enforced structurally outside LLM control, not by this prose — by the framework's deterministic gates wired for this workflow (gh#284): `phase-init`/`phase-check`/`phase-record`/`phase-complete` (`devforgeai-validate`), and the boundary hook `pre-phase-complete-boundary-check.sh` (PreToolUse, `exit 2` when a phase file was never `Read()` before its `phase-complete` — ADR-132). `phase-entry-validator.sh` is PostToolUse telemetry (ADR-129). **Reference reads stay advisory** — brainstorming reads only skill-internal references, not constitutional files, so there is no `[MANDATORY]` manifest and no `pre-phase-record-reference-check.sh` gate.

---

## Parameter Extraction

Extract from conversation context:

| Parameter | Source | Default |
|-----------|--------|---------|
| `$TOPIC` | Text after `/brainstorm` command | null (will ask in Phase 01) |
| `$RESUME_ID` | `--resume BRAINSTORM-NNN` argument | null (new session) |
| `$MODE` | Derived from above | "new" or "resume" |

---

## Phase 00: Initialization [INLINE - Bootstraps State]

This phase runs inline because it creates the state that all other phases depend on.

### Step 0.1: Parse Arguments

```
IF conversation contains "--resume BRAINSTORM-":
  Extract BRAINSTORM_ID from argument
  MODE = "resume"
ELSE IF conversation contains topic text after /brainstorm:
  TOPIC = extracted text
  MODE = "new"
ELSE:
  MODE = "new"
  TOPIC = null
```

### Step 0.2: Handle Resume Mode

The checkpoint is the per-phase accumulating conversation checkpoint
(`references/conversation-checkpoint-format.md`).

```
IF MODE == "resume":
  checkpoint_path = "tmp/${BRAINSTORM_ID}/checkpoint.json"
  Glob(pattern=checkpoint_path)

  IF found:
    Read(file_path=checkpoint_path)
    Restore session state from the checkpoint per the Resumption Protocol in
    references/conversation-checkpoint-format.md — phases[] with completed: true are
    settled GROUNDED facts; do not re-ask their questions.
    CURRENT_PHASE = int(checkpoint.current_phase)   # checkpoint stores it as a string ("01".."11")
    Display: "Resuming ${BRAINSTORM_ID} from Phase ${CURRENT_PHASE}"
    GOTO Phase Orchestration Loop at CURRENT_PHASE
  ELSE:
    Display: "No checkpoint found for ${BRAINSTORM_ID}."
    AskUserQuestion:
      Question: "No checkpoint found. What would you like to do?"
      Header: "Resume"
      Options:
        - label: "Start a new brainstorm"
          description: "Begin fresh session"
        - label: "Check for completed document"
          description: "Look for existing brainstorm output"
    IF "Start new": MODE = "new", continue below
    IF "Check completed": Glob for existing .brainstorm.html files, display results
```

### Step 0.3: Generate Brainstorm ID (New Session)

```
IF MODE == "new":
  # Scan for highest existing ID
  Glob(pattern="devforgeai/specs/brainstorms/BRAINSTORM-*.brainstorm.html")
  Glob(pattern="tmp/BRAINSTORM-*/checkpoint.json")

  # Extract highest NNN, increment
  BRAINSTORM_ID = "BRAINSTORM-{NNN+1}" (zero-padded to 3 digits minimum)

  # Ensure output directory exists
  Glob(pattern="devforgeai/specs/brainstorms/.gitkeep")
  IF not found: Create directory structure
```

### Step 0.4: Create Initial Conversation Checkpoint

```
checkpoint = {
  "schema": "conversation-checkpoint-v1",
  "brainstorm_id": BRAINSTORM_ID,
  "topic": TOPIC,
  "created": "{current ISO-8601 UTC timestamp}",
  "last_updated": "{current ISO-8601 UTC timestamp}",
  "current_phase": "00",
  "phases": []
}

Write(file_path="tmp/${BRAINSTORM_ID}/checkpoint.json", content=checkpoint)
```

VERIFY: `Glob(pattern="tmp/${BRAINSTORM_ID}/checkpoint.json")`
IF not found: HALT -- "Initial conversation checkpoint was NOT created."

### Step 0.4b: Initialize CLI Phase-State (gh#284)

```bash
devforgeai-validate phase-init ${BRAINSTORM_ID} --workflow=brainstorming --project-root=. 2>&1
```

| Exit Code | Action |
|-----------|--------|
| 0 | Phase-state initialized — proceed |
| 127 | CLI not installed — proceed without enforcement |
| Other | HALT — phase-state could not be initialized |

This writes `devforgeai/workflows/${BRAINSTORM_ID}-brainstorming-phase-state.json`,
which **coexists** with the skill's own `tmp/${BRAINSTORM_ID}/checkpoint.json` (Step
0.4) — the CLI file backs the boundary hook (`pre-phase-complete-boundary-check.sh`);
the checkpoint backs resume. Do NOT unify or migrate them.

### Step 0.5: Display Session Banner

```
Display:
"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  DevForgeAI Business Analysis Session
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Session: ${BRAINSTORM_ID}
Mode: New Business Analysis
Topic: ${TOPIC || 'To be discovered in Phase 01'}

Phases: 11 (BA Planning > Stakeholders > Problem > Future-State > Business Case >
            Risk > Constraints > Requirements > Prioritization > Change Strategy >
            Synthesis)
Estimated Duration: 45-90 minutes
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
```

Set CURRENT_PHASE = 1.

---

## Phase Orchestration Loop

```
FOR phase_num in range(CURRENT_PHASE, 12):  # Phases 01-11

    1. LOAD: Read(file_path=".claude/skills/spec-driven-brainstorming/phases/{phase_files[phase_num]}")
       Load the phase file FRESH. Do NOT rely on memory of previous reads.

    2. REFERENCE: Read the phase's reference file as specified in the phase Contract section.
       Each phase references a file in .claude/skills/spec-driven-brainstorming/references/.

    3. EXECUTE: Follow EVERY step in the phase file using EXECUTE-VERIFY-RECORD triplets.
       - Each step's EXECUTE tells you exactly what AskUserQuestion to call
       - Each step's VERIFY tells you how to confirm the data was captured
       - Each step's RECORD tells you how to update the conversation checkpoint

    4. EXIT CRITERIA: Verify ALL phase exit criteria are met before proceeding.
       IF any required data key is null or empty: HALT.

    5. CHECKPOINT: Update the conversation checkpoint — append the phase's exchanges,
       set the phase block completed: true, write phase_summary, advance current_phase.

    6. CONTEXT CHECK: If estimated context > 70%, offer save-and-resume via AskUserQuestion.
       IF user chooses "Save and resume later":
         Write final checkpoint, display resume command, EXIT skill.
```

---

## Phase Table

| Phase | Name | File | Min Questions | Required Data |
|-------|------|------|---------------|---------------|
| 00 | Initialization | (inline above) | 0 | brainstorm_id, checkpoint on disk |
| 01 | BA Planning & Approach | `phases/phase-01-ba-planning.md` | 3 | ba_planning.{analysis_scope, approach, session_success_definition} |
| 02 | Stakeholder Analysis | `phases/phase-02-stakeholder-analysis.md` | 7 | stakeholders.registry[>=1], engagement_plan, stakeholder_voices |
| 03 | Problem & Current-State Analysis | `phases/phase-03-problem-current-state.md` | 6 | problem_statement, root_causes[>=1], pain_points[>=1] |
| 04 | Future-State & Opportunity Mapping | `phases/phase-04-future-state-opportunity.md` | 4 | opportunity.opportunities[>=1], ideal_state, divergent_ideas |
| 05 | Business Case & Feasibility | `phases/phase-05-business-case-feasibility.md` | 4 | business_case.cost_benefit, feasibility |
| 06 | Risk Analysis | `phases/phase-06-risk-analysis.md` | 3 | risk_analysis.risks[>=1], premortem |
| 07 | Constraints & Solution Scope | `phases/phase-07-constraints-solution-scope.md` | 4 | constraints_scope.{budget_range, timeline}, out_of_scope[>=1] |
| 08 | Requirements Definition | `phases/phase-08-requirements-definition.md` | 4 | requirements.functional[>=1], nfrs |
| 09 | Prioritization & Roadmap | `phases/phase-09-prioritization-roadmap.md` | 4 | prioritization.must_have_capabilities[>=1], deferred_ideas |
| 10 | Change & Transition Strategy | `phases/phase-10-change-transition-strategy.md` | 4 | change_strategy.{adoption_approach, transition_plan, change_management} |
| 11 | Synthesis & Handoff | `phases/phase-11-synthesis-handoff.md` | 3 | output_file (HTML on disk), handoff.recommended_approach |

---

## Required Subagents

| Phase | Subagent | Enforcement |
|-------|----------|-------------|
| 02 | stakeholder-analyst | OPTIONAL (enhances analysis, not blocking) |
| 04 | internet-sleuth | CONDITIONAL (user opts in to market research in Phase 01) |

---

## State Persistence

- **Checkpoint:** `tmp/${BRAINSTORM_ID}/checkpoint.json` (per-phase accumulating conversation checkpoint)
- **Output:** `devforgeai/specs/brainstorms/${BRAINSTORM_ID}-${short_name}.brainstorm.html`
- **Templates:** `.claude/skills/spec-driven-brainstorming/assets/templates/` (loaded via Read, not duplicated)

---

## Workflow Completion Validation

```
IF phases_completed < 11: HALT "WORKFLOW INCOMPLETE - {completed_count}/11 phases"
IF output_file not on disk (Glob returns empty): HALT "Output HTML document not generated"
IF checkpoint still exists: it is retired in Phase 11 Step 11.10 (session complete)
```

---

## Error Handling

Load error recovery patterns from: `.claude/skills/spec-driven-brainstorming/references/error-handling.md`

**Graceful Degradation Priority:**
1. User answers (highest - never lose)
2. Problem statement
3. Stakeholder map
4. Constraints
5. Priorities
6. Market research (lowest - can skip)

---

## Success Criteria

- All 11 phases executed (no skipping)
- Output HTML document exists on disk with all 11 phase sections and the JSON data island
- User validated output accuracy
- Conversation checkpoint retired after successful completion
- Next steps displayed to user
