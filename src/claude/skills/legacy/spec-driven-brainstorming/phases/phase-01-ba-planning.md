# Phase 01: BA Planning & Approach

## Entry Gate

```bash
devforgeai-validate phase-check ${BRAINSTORM_ID} --workflow=brainstorming --from=00 --to=01 --project-root=. 2>&1
```

| Exit Code | Action |
|-----------|--------|
| 0 | Proceed to Phase 01 |
| 127 | CLI not installed — proceed without enforcement |
| Other | HALT — previous phase not complete |

---

## Contract

| Attribute | Value |
|-----------|-------|
| **PURPOSE** | Establish the scope, approach, and success definition for this Business Analysis session before discovery begins |
| **REFERENCE** | `.claude/skills/spec-driven-brainstorming/references/conversation-checkpoint-format.md` |
| **STEP COUNT** | 5 mandatory steps |
| **MINIMUM QUESTIONS** | 3 |
| **GOVERNING ADR** | ADR-065 |

This is the first dedicated phase of the 11-phase Business Analysis workflow. It frames
the engagement: what problem is being analysed, how wide the analysis goes this session,
how rigorous it will be, and what a successful session must produce. Getting this wrong
makes every later phase drift — a session scoped to an MVP must not be analysed as if it
were the full platform.

## Phase Exit Criteria

Field names listed are the canonical RECORD targets — each maps to the `ba_planning`
section of the data island (`references/brainstorm.schema.json` v2.0).

- [ ] Topic captured → `session.topic` and `session.topic_type`
- [ ] Analysis scope defined → `session.ba_planning.analysis_scope`
- [ ] BA approach defined → `session.ba_planning.approach`
- [ ] Session success defined → `session.ba_planning.session_success_definition`
- [ ] Conversation checkpoint updated with Phase 01 exchanges
- [ ] Context window check completed → `session.phases["01"].context_check_completed`

---

## Reference Loading

```
Read(file_path=".claude/skills/spec-driven-brainstorming/references/conversation-checkpoint-format.md")
Read(file_path=".claude/skills/spec-driven-brainstorming/references/user-interaction-patterns.md")
Read(file_path=".claude/skills/spec-driven-brainstorming/references/question-templates.md")
```

IF any Read fails: HALT -- "Phase 01 reference files not loaded. Cannot proceed without reference material."

---

## Mandatory Steps

### Step 1.1: Capture the Topic

**Condition:** Only execute the AskUserQuestion if `session.topic` is null (topic not
provided in command arguments).

EXECUTE:
```
IF session.topic is NOT null:
  Display: "Topic already set: {session.topic}"
  SKIP to Step 1.2

AskUserQuestion:
  questions:
    - question: "What business problem or opportunity should this analysis address?"
      header: "Topic"
      multiSelect: false
      options:
        - label: "A specific problem"
          description: "Something isn't working well"
        - label: "An opportunity"
          description: "Something could be better"
        - label: "Not sure yet"
          description: "Help me discover it"
```

Decision logic:
```
IF response == "A specific problem":   session.topic_type = "problem"
ELSE IF response == "An opportunity":  session.topic_type = "opportunity"
ELSE:                                  session.topic_type = "discovery"

IF session.topic_type IN ("problem", "opportunity"):
  Capture the follow-up free-text description into session.topic.
```

VERIFY: `session.topic` and `session.topic_type` are populated.

RECORD: Append the exchange to the Phase 01 checkpoint block; persist `session.topic`
and `session.topic_type`.

```bash
devforgeai-validate phase-record ${BRAINSTORM_ID} --workflow=brainstorming --phase=01 --step=1.1 --project-root=. 2>&1
```

---

### Step 1.2: Define Analysis Scope

This step separates the **full vision** from what **this session** will analyse. A user
may describe an enterprise platform but want this session scoped to an MVP slice — that
distinction must be explicit, because every later phase analyses the scoped slice while
out-of-scope vision feeds the Phase 09 Deferred Ideas Register.

EXECUTE:
```
AskUserQuestion:
  questions:
    - question: "How wide is the scope of THIS analysis session?"
      header: "Scope"
      multiSelect: false
      options:
        - label: "MVP / first slice"
          description: "Analyse a minimal first release; larger vision noted for later"
        - label: "Full initiative"
          description: "Analyse the complete intended solution"
        - label: "A single capability"
          description: "Deep-dive one feature or workflow within a larger system"
```

Follow-up (always):
```
AskUserQuestion: template=QT-5 (intent: describe)
  question_text: "Describe the scope boundary in one or two sentences — what this session
                  WILL analyse, and what larger vision (if any) sits outside it."
  header: "Boundary"
```

Decision logic:
```
session.ba_planning.analysis_scope = "{scope_choice}: {boundary_description}"

IF the user named larger vision outside the session scope:
  Note it as session.ba_planning.vision_beyond_scope — Phase 09 seeds the Deferred Ideas
  Register from it so no out-of-scope idea is lost.
```

VERIFY: `session.ba_planning.analysis_scope` is a non-empty string.
IF empty: HALT -- "Step 1.2: Analysis scope not captured."

RECORD: Append the exchange to the Phase 01 checkpoint block; persist
`session.ba_planning.analysis_scope` (and `vision_beyond_scope` if captured).

```bash
devforgeai-validate phase-record ${BRAINSTORM_ID} --workflow=brainstorming --phase=01 --step=1.2 --project-root=. 2>&1
```

---

### Step 1.3: Choose the BA Approach

EXECUTE:
```
AskUserQuestion:
  questions:
    - question: "How rigorous should this analysis be?"
      header: "Approach"
      multiSelect: false
      options:
        - label: "Thorough"
          description: "Full 11-phase analysis — recommended for new platforms"
        - label: "Focused"
          description: "All phases, but lighter questioning per phase"
    - question: "Should the session include external market/competitor research?"
      header: "Research"
      multiSelect: false
      options:
        - label: "Yes"
          description: "Phase 04 will run market research via the internet-sleuth subagent"
        - label: "No"
          description: "Rely on the user's own knowledge"
```

Decision logic:
```
session.ba_planning.approach = "{rigour_choice}"
session.research_enabled = (research answer == "Yes")
```

VERIFY: `session.ba_planning.approach` is populated; `session.research_enabled` is a boolean.

RECORD: Append the exchange to the Phase 01 checkpoint block; persist
`session.ba_planning.approach` and `session.research_enabled`.

```bash
devforgeai-validate phase-record ${BRAINSTORM_ID} --workflow=brainstorming --phase=01 --step=1.3 --project-root=. 2>&1
```

---

### Step 1.4: Define Session Success

EXECUTE:
```
AskUserQuestion:
  questions:
    - question: "What decision or outcome must this Business Analysis document support?"
      header: "Success"
      multiSelect: false
      options:
        - label: "Go / no-go funding decision"
          description: "A stakeholder must decide whether to fund the build"
        - label: "Scope a build"
          description: "Hand off to requirements and development"
        - label: "Align stakeholders"
          description: "Build shared understanding before committing"
        - label: "Explore feasibility"
          description: "Determine whether the idea is viable at all"
```

VERIFY: a success definition was selected.

RECORD: Append the exchange to the Phase 01 checkpoint block; persist
`session.ba_planning.session_success_definition`.

```bash
devforgeai-validate phase-record ${BRAINSTORM_ID} --workflow=brainstorming --phase=01 --step=1.4 --project-root=. 2>&1
```

---

### Step 1.5: Context Window Check

EXECUTE:
```
IF estimated_context_usage > 70%:
  AskUserQuestion: template=QT-1
    question_text: "Context window is approximately {PERCENT}% full. Continue or save?"
    header: "Session"
    overrides:
      "Yes (Recommended)": { label: "Continue", description: "Proceed to Phase 02 (Stakeholder Analysis)" }
      "No":                { label: "Save and continue later", description: "Update checkpoint and exit" }
      remove: ["Skip / Defer"]

  IF response == "Save and continue later":
    Update the conversation checkpoint with all Phase 01 data
    Display: "Session saved. Resume with: /brainstorm --resume {BRAINSTORM_ID}"
    EXIT skill
ELSE:
  Display: "Context window healthy. Proceeding to Phase 02."
```

VERIFY: the context window check was performed.
IF skipped: HALT -- "Step 1.5: Context Window Check not performed."

RECORD: Persist `session.phases["01"].context_check_completed = true`.

```bash
devforgeai-validate phase-record ${BRAINSTORM_ID} --workflow=brainstorming --phase=01 --step=1.5 --project-root=. 2>&1
```

---

## Phase Exit Verification

Before transitioning to Phase 02, verify ALL exit criteria:

```
VERIFY_EXIT:
  CHECK: session.topic is not null
    IF FAIL: HALT -- "Exit blocked: Topic not captured."
  CHECK: session.ba_planning.analysis_scope is a non-empty string
    IF FAIL: HALT -- "Exit blocked: Analysis scope not defined."
  CHECK: session.ba_planning.approach is populated
    IF FAIL: HALT -- "Exit blocked: BA approach not defined."
  CHECK: session.ba_planning.session_success_definition is populated
    IF FAIL: HALT -- "Exit blocked: Session success not defined."
  CHECK: session.phases["01"].context_check_completed == true
    IF FAIL: HALT -- "Exit blocked: Context window check not completed."
  CHECK: session.phases["01"].questions_answered >= 3
    IF FAIL: HALT -- "Exit blocked: Minimum 3 questions required, only {count} answered."
```

Update the conversation checkpoint on successful exit (per
`references/conversation-checkpoint-format.md`): set the Phase 01 block `completed: true`,
write its `phase_summary`, advance `current_phase` to `"02"`.

VERIFY: `tmp/{BRAINSTORM_ID}/checkpoint.json` shows the Phase 01 block `completed: true`.
IF write fails: HALT -- "Phase 01 exit checkpoint not saved."

---

## Exit Gate

```bash
devforgeai-validate phase-complete ${BRAINSTORM_ID} --workflow=brainstorming --phase=01 --checkpoint-passed --project-root=. 2>&1
```

| Exit Code | Action |
|-----------|--------|
| 0 | Phase 01 complete — proceed to next phase |
| 127 | CLI not installed — proceed without enforcement |
| Other | HALT — checkpoint/step validation failed |

---

## Phase Transition Display

Display: "Phase 01 Complete — BA Planning. Scope: {analysis_scope}. Approach:
{approach}. Proceeding to Phase 02 (Stakeholder Analysis)."
