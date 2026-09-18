# Phase 10: Change & Transition Strategy

## Entry Gate

```bash
devforgeai-validate phase-check ${BRAINSTORM_ID} --workflow=brainstorming --from=09 --to=10 --project-root=. 2>&1
```

| Exit Code | Action |
|-----------|--------|
| 0 | Proceed to Phase 10 |
| 127 | CLI not installed — proceed without enforcement |
| Other | HALT — previous phase not complete |

---

## Contract

| Attribute | Value |
|-----------|-------|
| **PURPOSE** | Plan how the solution will be adopted — the rollout approach, the transition from the current state, the change-management response to resistance, and the training people will need |
| **REFERENCE** | `.claude/skills/spec-driven-brainstorming/references/conversation-checkpoint-format.md` |
| **STEP COUNT** | 5 mandatory steps |
| **MINIMUM QUESTIONS** | 4 |
| **GOVERNING ADR** | ADR-065 |

NEW phase in the 11-phase Business Analysis workflow. A solution that is built but not
adopted delivers no value. This phase closes that gap: it takes the as-is process (Phase
03), the to-be process (Phase 04), the organizational constraints and resistance (Phase
07), and the stakeholder map (Phase 02), and turns them into an adoption and transition
plan. It is the last analysis phase before Phase 11 synthesis.

## Phase Exit Criteria

Field names listed are the canonical RECORD targets — each maps to the `change_strategy`
section of the data island (`references/brainstorm.schema.json` v2.0).

- [ ] Adoption approach chosen → `session.change_strategy.adoption_approach` (non-empty)
- [ ] Transition plan captured → `session.change_strategy.transition_plan` (non-empty)
- [ ] Change-management response captured → `session.change_strategy.change_management` (non-empty)
- [ ] Training needs identified → `session.change_strategy.training_needs` (may be empty — warn-only)
- [ ] Conversation checkpoint updated with Phase 10 exchanges
- [ ] Context window check completed → `session.phases["10"].context_check_completed`

**IF any blocking criterion is unmet: HALT. Do NOT proceed to Phase 11.**

---

## Reference Loading

```
Read(file_path=".claude/skills/spec-driven-brainstorming/references/conversation-checkpoint-format.md")
Read(file_path=".claude/skills/spec-driven-brainstorming/references/user-interaction-patterns.md")
Read(file_path=".claude/skills/spec-driven-brainstorming/references/question-templates.md")
```

IF any Read fails: HALT -- "Phase 10 reference files not loaded. Cannot proceed without reference material."

---

## Mandatory Steps

### Step 10.1: Adoption Approach

EXECUTE:
```
AskUserQuestion:
  questions:
    - question: "How should the solution be rolled out to its users?"
      header: "Rollout"
      multiSelect: false
      options:
        - label: "Pilot then expand"
          description: "Prove it with a small group, then widen — lowest risk"
        - label: "Phased by group or region"
          description: "Roll out in waves across teams or sites"
        - label: "Big-bang cutover"
          description: "Everyone switches at once on a set date"
        - label: "Parallel run"
          description: "New and old run side by side until confidence is high"
```

Follow-up (rationale — always):
```
AskUserQuestion: template=QT-5 (intent: explain)
  question_text: "Why is that the right rollout approach given the constraints and
                  resistance surfaced in Phase 07?"
  header: "Rollout Why"

session.change_strategy.adoption_approach = "{rollout choice}: {rationale}"
```

VERIFY: `session.change_strategy.adoption_approach` is a non-empty string.
IF empty: HALT -- "Step 10.1: Adoption approach not captured."

RECORD: Append the exchange to the Phase 10 checkpoint block; persist
`session.change_strategy.adoption_approach`.

```bash
devforgeai-validate phase-record ${BRAINSTORM_ID} --workflow=brainstorming --phase=10 --step=10.1 --project-root=. 2>&1
```

---

### Step 10.2: Transition Plan

Plan the move from the as-is process (Phase 03) to the to-be process (Phase 04).

EXECUTE:
```
Display the As-Is Process Model (Phase 03) and the To-Be Process Sketch (Phase 04) side
by side for reference.

AskUserQuestion: template=QT-5 (intent: describe)
  question_text: "Describe the transition from today's process to the future one — what
                  has to happen in what order? Cover data migration, the cutover moment,
                  and whether old and new run in parallel for a while."
  header: "Transition"

session.change_strategy.transition_plan = response
```

Follow-up (rollback — always):
```
AskUserQuestion:
  questions:
    - question: "If the transition runs into trouble, what is the fallback?"
      header: "Fallback"
      multiSelect: false
      options:
        - label: "Revert to the current process"
          description: "Old process stays available as a safety net"
        - label: "Fix forward"
          description: "No revert — issues are resolved in the new process"
        - label: "Partial rollback"
          description: "Roll back the affected part only"
        - label: "Not yet decided"
          description: "Needs more planning"

Append the fallback answer to session.change_strategy.transition_plan as a closing clause.
```

VERIFY: `session.change_strategy.transition_plan` is a non-empty string.
IF empty: HALT -- "Step 10.2: Transition plan not captured."

RECORD: Append the exchange to the Phase 10 checkpoint block; persist
`session.change_strategy.transition_plan`.

```bash
devforgeai-validate phase-record ${BRAINSTORM_ID} --workflow=brainstorming --phase=10 --step=10.2 --project-root=. 2>&1
```

---

### Step 10.3: Change Management

Address the resistance and stakeholder concerns surfaced earlier.

EXECUTE:
```
Display the organizational resistance captured in Phase 07
(session.constraints_scope.organizational.resistance_sources and resistance_causes) and
the stakeholder concerns from Phase 02, if any.

AskUserQuestion: template=QT-5 (intent: describe)
  question_text: "How will the change be managed — how will resistance be addressed, who
                  communicates what, and how are stakeholders kept engaged through the
                  rollout?"
  header: "Change Mgmt"

session.change_strategy.change_management = response
```

Follow-up (sponsorship — always):
```
AskUserQuestion:
  questions:
    - question: "Who is the executive sponsor or champion driving adoption?"
      header: "Sponsor"
      multiSelect: false
      options:
        - label: "Identified and committed"
          description: "A named sponsor is actively backing the change"
        - label: "Identified, not yet committed"
          description: "A likely sponsor exists but is not yet secured"
        - label: "Not yet identified"
          description: "Securing a sponsor is itself an action item"

Append the sponsorship answer to session.change_strategy.change_management as a
supporting clause.
```

VERIFY: `session.change_strategy.change_management` is a non-empty string.
IF empty: HALT -- "Step 10.3: Change-management response not captured."

RECORD: Append the exchange to the Phase 10 checkpoint block; persist
`session.change_strategy.change_management`.

```bash
devforgeai-validate phase-record ${BRAINSTORM_ID} --workflow=brainstorming --phase=10 --step=10.3 --project-root=. 2>&1
```

---

### Step 10.4: Training Needs

EXECUTE:
```
Initialize: session.change_strategy.training_needs = []

AskUserQuestion: template=QT-5 (intent: list)
  question_text: "What training or enablement will people need to use the new solution
                  well? Name each audience and what they need. (Choose 'Done — no more'
                  to finish.)"
  header: "Training"

Loop:
  IF user selects "Done — no more": BREAK
  Append the user's training-need entry to session.change_strategy.training_needs.
```

VERIFY: `session.change_strategy.training_needs` is a list (may be empty).
  IF `len(session.change_strategy.training_needs) == 0`:
    Display: "No training needs captured. Continuing — confirm this is intentional; most
    rollouts need some enablement."
  (No HALT — warn-only check.)

RECORD: Append the exchange to the Phase 10 checkpoint block; persist
`session.change_strategy.training_needs`.

```bash
devforgeai-validate phase-record ${BRAINSTORM_ID} --workflow=brainstorming --phase=10 --step=10.4 --project-root=. 2>&1
```

---

### Step 10.5: Context Window Check

EXECUTE:
```
IF estimated_context_usage > 70%:
  AskUserQuestion: template=QT-1
    question_text: "Context window is approximately {PERCENT}% full. Continue or save?"
    header: "Session"
    overrides:
      "Yes (Recommended)": { label: "Continue", description: "Proceed to Phase 11 (Synthesis & Handoff)" }
      "No":                { label: "Save and continue later", description: "Update checkpoint and exit" }
      remove: ["Skip / Defer"]

  IF response == "Save and continue later":
    Update the conversation checkpoint with all Phase 10 data
    Display: "Session saved. Resume with: /brainstorm --resume {BRAINSTORM_ID}"
    EXIT skill
ELSE:
  Display: "Context window healthy. Proceeding to Phase 11."
```

VERIFY: the context window check was performed.
IF skipped: HALT -- "Step 10.5: Context Window Check not performed."

RECORD: Persist `session.phases["10"].context_check_completed = true`.

```bash
devforgeai-validate phase-record ${BRAINSTORM_ID} --workflow=brainstorming --phase=10 --step=10.5 --project-root=. 2>&1
```

---

## Phase Exit Verification

Before transitioning to Phase 11, verify ALL exit criteria:

```
VERIFY_EXIT:
  CHECK: session.change_strategy.adoption_approach is non-empty
    IF FAIL: HALT -- "Exit blocked: Adoption approach not captured."
  CHECK: session.change_strategy.transition_plan is non-empty
    IF FAIL: HALT -- "Exit blocked: Transition plan not captured."
  CHECK: session.change_strategy.change_management is non-empty
    IF FAIL: HALT -- "Exit blocked: Change-management response not captured."
  CHECK: session.change_strategy.training_needs is a list (may be empty — warn-only)
    IF FAIL: HALT -- "Exit blocked: Training-needs field not initialised."
  CHECK: session.phases["10"].context_check_completed == true
    IF FAIL: HALT -- "Exit blocked: Context window check not completed."
  CHECK: session.phases["10"].questions_answered >= 4
    IF FAIL: HALT -- "Exit blocked: Minimum 4 questions required, only {count} answered."
```

Update the conversation checkpoint on successful exit (per
`references/conversation-checkpoint-format.md`): set the Phase 10 block `completed: true`,
write its `phase_summary`, advance `current_phase` to `"11"`.

VERIFY: `tmp/{BRAINSTORM_ID}/checkpoint.json` shows the Phase 10 block `completed: true`.
IF write fails: HALT -- "Phase 10 exit checkpoint not saved."

---

## Exit Gate

```bash
devforgeai-validate phase-complete ${BRAINSTORM_ID} --workflow=brainstorming --phase=10 --checkpoint-passed --project-root=. 2>&1
```

| Exit Code | Action |
|-----------|--------|
| 0 | Phase 10 complete — proceed to next phase |
| 127 | CLI not installed — proceed without enforcement |
| Other | HALT — checkpoint/step validation failed |

---

## Phase Transition Display

Display: "Phase 10 Complete — Change & Transition Strategy. Adoption: {adoption_approach
one-line}. Training needs identified: {count}. All analysis phases complete — proceeding
to Phase 11 (Synthesis & Handoff)."
