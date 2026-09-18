# Phase 03: Problem & Current-State Analysis

## Entry Gate

```bash
devforgeai-validate phase-check ${BRAINSTORM_ID} --workflow=brainstorming --from=02 --to=03 --project-root=. 2>&1
```

| Exit Code | Action |
|-----------|--------|
| 0 | Proceed to Phase 03 |
| 127 | CLI not installed — proceed without enforcement |
| Other | HALT — previous phase not complete |

---

## Contract

| Attribute | Value |
|-----------|-------|
| **PURPOSE** | Deep dive into WHAT the actual problem is, the current state, and the as-is process, using root cause analysis |
| **REFERENCE** | `.claude/skills/spec-driven-brainstorming/references/problem-exploration-workflow.md` |
| **STEP COUNT** | 10 mandatory steps (with substeps 3.1.1 and 3.1.2) |
| **MINIMUM QUESTIONS** | 6 |
| **GOVERNING ADR** | ADR-065 |

Renumbered from the former Phase 02 and expanded with an explicit **As-Is Process Model**
step — for workflow-centric initiatives (ticketing, change control, approvals) the
current process flow is itself a core analysis artifact, not just prose.

## Phase Exit Criteria

Field names listed are the canonical RECORD targets — each maps to the `problem_analysis`
section of the data island, except `problem_statement` which is a top-level field
(`references/brainstorm.schema.json` v2.0).

- [ ] Current state documented → `session.current_state.type`
- [ ] As-is process model captured → `session.problem_analysis.as_is_process_model`
- [ ] At least 3 levels of 5 Whys completed → `session.root_causes` (length ≥ 3) OR `session.root_cause_found == true`
- [ ] At least 1 pain point identified with severity → `session.pain_points` (length ≥ 1, each with severity)
- [ ] Problem statement generated and user-validated → `session.problem_statement` (non-empty) and `session.problem_statement_validated == true`
- [ ] HMW reframings explored (optional opt-in) → `session.hmw_reframings` (may be empty array)
- [ ] Cross-industry analogy explored (optional opt-in) → `session.cross_industry_analogies` (may be empty array)
- [ ] Conversation checkpoint updated with Phase 03 exchanges
- [ ] Context window check completed → `session.phases["03"].context_check_completed`

---

## Reference Loading

```
Read(file_path=".claude/skills/spec-driven-brainstorming/references/problem-exploration-workflow.md")
Read(file_path=".claude/skills/spec-driven-brainstorming/references/user-interaction-patterns.md")
Read(file_path=".claude/skills/spec-driven-brainstorming/references/question-templates.md")
Read(file_path=".claude/skills/spec-driven-brainstorming/references/conversation-checkpoint-format.md")
```

IF any Read fails: HALT -- "Phase 03 reference files not loaded. Cannot proceed without reference material."

---

## Mandatory Steps

### Step 3.1: Current State Assessment

EXECUTE:
```
AskUserQuestion:
  questions:
    - question: "How is this task or process currently being done?"
      header: "Current State"
      multiSelect: false
      options:
        - label: "Manual process"
          description: "Done by humans with little automation"
        - label: "Semi-automated"
          description: "Mix of manual and automated steps"
        - label: "Automated but broken"
          description: "System exists but has issues"
        - label: "No process exists"
          description: "Currently not being done at all"
```

Decision logic:
```
session.current_state.type = response

IF response IN ("Manual process", "Semi-automated"):    GOTO Step 3.1.1
ELSE IF response == "Automated but broken":              session.current_state.type = "automated_broken"; GOTO Step 3.1.2
ELSE IF response == "No process exists":                 session.current_state.type = "none"; SKIP to Step 3.2
```

VERIFY: `session.current_state.type` is set.

RECORD: Append the exchange to the Phase 03 checkpoint block; persist
`session.current_state.type`.

```bash
devforgeai-validate phase-record ${BRAINSTORM_ID} --workflow=brainstorming --phase=03 --step=3.1 --project-root=. 2>&1
```

---

### Step 3.1.1: Process Details (Manual / Semi-Automated)

**Condition:** Only execute if `session.current_state.type` IN ("Manual process", "Semi-automated").

EXECUTE (Duration):
```
AskUserQuestion: template=QT-3
  question_text: "How long does the current process take per instance?"
  header: "Duration"
  range_type: duration
```

EXECUTE (Volume):
```
AskUserQuestion: template=QT-3
  question_text: "How many times per day/week is this process executed?"
  header: "Volume"
  range_type: volume
```

EXECUTE (Error Rate):
```
AskUserQuestion: template=QT-3
  question_text: "How often does the current process fail or produce errors?"
  header: "Error Rate"
  range_type: error_rate
```

VERIFY: `session.current_state.duration`, `.volume`, `.error_rate` all populated.

RECORD: Append the exchange to the Phase 03 checkpoint block; persist
`session.current_state.{duration, volume, error_rate}`.

```bash
devforgeai-validate phase-record ${BRAINSTORM_ID} --workflow=brainstorming --phase=03 --step=3.1.1 --project-root=. 2>&1
```

---

### Step 3.1.2: System Issues (Automated but Broken)

**Condition:** Only execute if `session.current_state.type == "automated_broken"`.

EXECUTE:
```
AskUserQuestion:
  questions:
    - question: "What are the main issues with the current system?"
      header: "Issues"
      multiSelect: true
      options:
        - label: "Reliability problems"
          description: "System crashes or fails"
        - label: "Performance issues"
          description: "Too slow"
        - label: "Missing features"
          description: "Doesn't do what we need"
        - label: "Hard to use"
          description: "Poor user experience"
```

VERIFY: At least 1 issue selected.

RECORD: Append the exchange to the Phase 03 checkpoint block; persist
`session.current_state.system_issues[]`.

```bash
devforgeai-validate phase-record ${BRAINSTORM_ID} --workflow=brainstorming --phase=03 --step=3.1.2 --project-root=. 2>&1
```

---

### Step 3.2: As-Is Process Model

Capture the current process as an ordered sequence of steps with the actor for each.
A textual swimlane is sufficient — the goal is a shared, explicit picture of how work
flows today, against which the future-state (Phase 04) and requirements (Phase 08) are
defined. If `session.current_state.type == "none"` (no process exists), record that
explicitly and skip the step sequence.

EXECUTE:
```
IF session.current_state.type == "none":
  session.problem_analysis.as_is_process_model = "No current process exists (greenfield)."
  SKIP to Step 3.3

AskUserQuestion: template=QT-5 (intent: list)
  question_text: "Walk through the current process step by step. For each step name the
                  actor and what they do — e.g. '1. Requester emails IT; 2. IT logs a
                  ticket manually; 3. Manager approves by reply'."
  header: "As-Is Flow"

Capture the ordered steps.

AskUserQuestion: template=QT-5 (intent: list)
  question_text: "Where in that flow are the worst delays, hand-offs, or breakdowns?"
  header: "Bottlenecks"

Capture the bottlenecks.

session.problem_analysis.as_is_process_model =
  { steps: [ordered actor+action entries], bottlenecks: [captured bottlenecks] }
```

VERIFY: `session.problem_analysis.as_is_process_model` is populated (either the greenfield
note or a steps+bottlenecks object).

RECORD: Append the exchange to the Phase 03 checkpoint block; persist
`session.problem_analysis.as_is_process_model`.

```bash
devforgeai-validate phase-record ${BRAINSTORM_ID} --workflow=brainstorming --phase=03 --step=3.2 --project-root=. 2>&1
```

---

### Step 3.3: 5 Whys Root Cause Analysis

Introduction:
```
Display:
"Now let's explore WHY this problem exists using the 5 Whys technique.
 We'll ask 'why' repeatedly to find the root cause."
```

EXECUTE (Why Level 1):
```
current_problem = session.topic

AskUserQuestion: template=QT-5
  question_text: "Why does {current_problem} happen?"
  header: "Why 1"
  intent: explain

IF response == "Let me explain":
  Capture user's free-form explanation.
  session.root_causes[0] = explanation
  current_problem = explanation
ELSE IF response == "I'm not sure":
  session.root_causes[0] = "Unknown - needs investigation"
  Ask reframe: "What do people blame when this problem occurs?"
  IF user provides answer: update session.root_causes[0]; continue loop.
  ELSE: SKIP remaining whys.
ELSE IF response == "Skip":
  SKIP remaining whys.
```

EXECUTE (Why Levels 2-5 Loop):
```
FOR level in [2, 3, 4, 5]:
  IF current_problem == "Unknown" OR user_says_stop:
    BREAK

  AskUserQuestion:
    questions:
      - question: "Why does {current_problem} happen?"
        header: "Why {level}"
        multiSelect: false
        options:
          - label: "Let me explain"
            description: "I'll describe the cause"
          - label: "That's the root cause"
            description: "We've found the fundamental issue"
          - label: "I don't know"
            description: "Unsure of deeper cause"

  IF response == "Let me explain":
    Capture user's free-form explanation.
    session.root_causes[level-1] = explanation
    current_problem = explanation
  ELSE IF response == "That's the root cause":
    session.root_cause_found = true
    session.root_cause_level = level - 1
    BREAK
  ELSE IF response == "I don't know":
    session.root_causes[level-1] = "Unknown"
    session.root_cause_level = level - 1
    BREAK
```

VERIFY: `len(session.root_causes) >= 3` OR `session.root_cause_found == true`.
IF below 3 levels AND no root_cause_found: HALT -- "Step 3.3: Minimum 3 Why levels required. Only {count} completed."

RECORD: Append the exchange to the Phase 03 checkpoint block; persist
`session.root_causes`, `session.root_cause_level`, `session.root_cause_found`.

```bash
devforgeai-validate phase-record ${BRAINSTORM_ID} --workflow=brainstorming --phase=03 --step=3.3 --project-root=. 2>&1
```

---

### Step 3.4: Pain Point Inventory

EXECUTE (Initial Prompt):
```
AskUserQuestion: template=QT-5
  question_text: "What are the top 3-5 pain points caused by this problem?"
  header: "Pain Points"
  intent: list
```

EXECUTE (Pain Point Loop — iterations 1 through 5):
```
FOR i in [1..5]:
  Capture pain_point.description from user input.
  IF empty OR user says done: BREAK

  AskUserQuestion: template=QT-4
    question_text: "What type of business impact does '{pain_point.description}' cause?"
    header: "Impact Type"
    category: business_impact
  pain_point.impact_types = response

  AskUserQuestion: template=QT-2
    question_text: "How severe is '{pain_point.description}' for your business?"
    header: "Severity"
    scale_type: severity
  pain_point.severity = response

  Append pain_point to session.pain_points[].
```

VERIFY: `session.pain_points.length >= 1`; every pain point has `impact_types` AND `severity`.
IF empty OR any pain point missing fields: HALT -- "Step 3.4: Pain point '{description}' missing impact type or severity."

RECORD: Append the exchange to the Phase 03 checkpoint block; persist `session.pain_points`.

```bash
devforgeai-validate phase-record ${BRAINSTORM_ID} --workflow=brainstorming --phase=03 --step=3.4 --project-root=. 2>&1
```

---

### Step 3.5: Impact Quantification

**Condition:** Only execute for pain points with severity in ("Critical", "High").

```
critical_high_pains = [p for p in session.pain_points WHERE p.severity in ["Critical", "High"]]
IF len(critical_high_pains) == 0:
  Display: "No Critical/High pain points to quantify. Proceeding to Step 3.6."
  SKIP to Step 3.6
```

EXECUTE:
```
FOR each pain_point in critical_high_pains:
  AskUserQuestion:
    questions:
      - question: "Can you estimate the cost of '{pain_point.description}' per month?"
        header: "Cost"
        multiSelect: false
        options:
          - label: "< $1,000/month"
            description: "Minor cost"
          - label: "$1,000 - $10,000/month"
            description: "Moderate cost"
          - label: "$10,000 - $100,000/month"
            description: "Significant cost"
          - label: "> $100,000/month"
            description: "Major cost"
          - label: "Can't estimate"
            description: "Unknown or hard to quantify"
  pain_point.estimated_cost = response
```

VERIFY: Each Critical/High pain point has `estimated_cost` (including "Can't estimate" as a valid value).
IF any missing: HALT -- "Step 3.5: Impact quantification incomplete for '{pain_point.description}'."

RECORD: Append the exchange to the Phase 03 checkpoint block; persist updated
`session.pain_points` (with costs).

```bash
devforgeai-validate phase-record ${BRAINSTORM_ID} --workflow=brainstorming --phase=03 --step=3.5 --project-root=. 2>&1
```

---

### Step 3.6: Failed Solution History

EXECUTE:
```
AskUserQuestion:
  questions:
    - question: "Have you tried solving this problem before?"
      header: "History"
      multiSelect: false
      options:
        - label: "Yes - it failed"
          description: "We tried but it didn't work"
        - label: "Yes - partially worked"
          description: "Some success but not complete"
        - label: "No - first attempt"
          description: "Haven't tried before"
        - label: "Not sure"
          description: "Before my time or don't know"
```

Conditional follow-up:
```
IF response IN ("Yes - it failed", "Yes - partially worked"):
  AskUserQuestion: template=QT-5
    question_text: "What was tried before?"
    header: "Previous"
    intent: describe
  failed_solution.what = captured description

  AskUserQuestion:
    questions:
      - question: "Why didn't it work?"
        header: "Why Failed"
        multiSelect: true
        options:
          - label: "Too expensive"
            description: "Cost exceeded budget"
          - label: "Too complex"
            description: "Solution was too complicated"
          - label: "Poor adoption"
            description: "People didn't use it"
          - label: "Didn't solve the problem"
            description: "Wrong solution for the issue"
          - label: "Other factors"
            description: "External circumstances"
  failed_solution.why = response
  Append failed_solution to session.failed_solutions[].
ELSE IF response == "No - first attempt":
  session.failed_solutions = []
ELSE IF response == "Not sure":
  session.failed_solutions = "unknown"
```

VERIFY: `session.failed_solutions` is set (list, empty list, or string "unknown").

RECORD: Append the exchange to the Phase 03 checkpoint block; persist
`session.failed_solutions`.

```bash
devforgeai-validate phase-record ${BRAINSTORM_ID} --workflow=brainstorming --phase=03 --step=3.6 --project-root=. 2>&1
```

---

### Step 3.7: Generate Problem Statement

EXECUTE (Synthesis):
```
primary_stakeholder = session.stakeholders.primary[0].name
primary_pain = session.pain_points[0].description
root_cause = session.root_causes[-1]
impact = session.pain_points[0].impact_types[0]

problem_statement = "{primary_stakeholder} experiences {primary_pain} because {root_cause}, resulting in {impact}."
```

EXECUTE (User Validation):
```
Display:
"Based on our discussion, here's the problem statement:

  \"{problem_statement}\"
"

AskUserQuestion: template=QT-5
  question_text: "Does this accurately capture the problem?"
  header: "Validate"
  intent: rewrite
```

Decision logic:
```
IF response == "Yes, that's accurate":
  session.problem_statement = problem_statement
  session.problem_statement_validated = true
ELSE IF response == "Needs minor adjustment":
  Ask user for specific adjustments. Apply to problem_statement.
  session.problem_statement = adjusted_statement
  session.problem_statement_validated = true
ELSE IF response == "Let me rewrite it":
  Capture user's rewritten problem statement.
  session.problem_statement = user_rewrite
  session.problem_statement_validated = true
```

VERIFY: `session.problem_statement` is non-empty AND `session.problem_statement_validated == true`.
IF not validated: HALT -- "Step 3.7: Problem statement not validated by user."

RECORD: Append the exchange to the Phase 03 checkpoint block; persist
`session.problem_statement` and `session.problem_statement_validated`.

```bash
devforgeai-validate phase-record ${BRAINSTORM_ID} --workflow=brainstorming --phase=03 --step=3.7 --project-root=. 2>&1
```

---

### Step 3.8: How-Might-We Reframing (Optional)

**Methodology reference:** `references/brainstorming-techniques.md` § 3 (How Might We
Reframing). Loads on first execution of this step.

EXECUTE:

Display:
"The problem statement we agreed on is:
  '{session.problem_statement}'

Let's try reframing it as 'How might we...' questions. Different framings reveal different
solution paths. This step is optional — choose 'Skip this question' on any prompt to stop."

```
Initialize: session.hmw_reframings = []
Initialize: N = 1

Loop (target: 3-5 reframings):
  AskUserQuestion: template=QT-5 (intent: describe)
    question_text: "Reframe #{N} — 'How might we ___?' Fill in the blank."
    header: "HMW {N}"
  IF user selects "Skip this question": BREAK
  Append the user's description to session.hmw_reframings.
  N += 1
  IF len(session.hmw_reframings) >= 5: BREAK
```

VERIFY: `session.hmw_reframings` is a list (may be empty if the user skipped the step).

RECORD: Append the exchange to the Phase 03 checkpoint block; persist
`session.hmw_reframings`. These feed Phase 04 opportunity generation as alternate framings.

```bash
devforgeai-validate phase-record ${BRAINSTORM_ID} --workflow=brainstorming --phase=03 --step=3.8 --project-root=. 2>&1
```

---

### Step 3.9: Cross-Industry Analogy (Optional)

**Methodology reference:** `references/brainstorming-techniques.md` § 4 (Cross-Industry
Analogy). Loads on first execution of this step.

EXECUTE:

Display:
"Cross-industry analogy reveals novel approaches by studying how an unrelated industry
solves a structurally similar problem. This step is optional."

```
AskUserQuestion: template=QT-1 (variant: 2-option)
  question_text: "Would a cross-industry analogy help here?"
  header: "Try analogy?"

IF response == "No":
  Initialize: session.cross_industry_analogies = []
  SKIP to RECORD.

# Inline custom AskUserQuestion — industry list is domain-specific, no QT template applies
AskUserQuestion:
  questions:
    - question: "Which industry should we look at?"
      header: "Industry"
      multiSelect: false
      options:
        - label: "Healthcare / hospitals"
        - label: "Aviation / airlines"
        - label: "Retail / e-commerce"
        - label: "Manufacturing / supply chain"
        - label: "Entertainment / streaming"
        - label: "Education"

selected_industry = response

AskUserQuestion: template=QT-5 (intent: describe)
  question_text: "If a {selected_industry} organization faced this problem
                  ('{session.problem_statement}'), what's a step they would take that you
                  wouldn't normally consider?"
  header: "Analogy"

Append {industry: selected_industry, insight: response} to session.cross_industry_analogies.
```

VERIFY: `session.cross_industry_analogies` is a list (may be empty if the user opted out).

RECORD: Append the exchange to the Phase 03 checkpoint block; persist
`session.cross_industry_analogies`.

```bash
devforgeai-validate phase-record ${BRAINSTORM_ID} --workflow=brainstorming --phase=03 --step=3.9 --project-root=. 2>&1
```

---

### Step 3.10: Context Window Check

EXECUTE:
```
IF estimated_context_usage > 70%:
  AskUserQuestion: template=QT-1
    question_text: "Context window is approximately {PERCENT}% full. Continue or save?"
    header: "Session"
    overrides:
      "Yes (Recommended)": { label: "Continue", description: "Proceed to Phase 04 (Future-State & Opportunity Mapping)" }
      "No":                { label: "Save and continue later", description: "Update checkpoint and exit" }
      remove: ["Skip / Defer"]

  IF response == "Save and continue later":
    Update the conversation checkpoint with all Phase 03 data
    Display: "Session saved. Resume with: /brainstorm --resume {BRAINSTORM_ID}"
    EXIT skill
ELSE:
  Display: "Context window healthy. Proceeding to Phase 04."
```

VERIFY: the context window check was performed.
IF skipped: HALT -- "Step 3.10: Context Window Check not performed."

RECORD: Persist `session.phases["03"].context_check_completed = true`.

```bash
devforgeai-validate phase-record ${BRAINSTORM_ID} --workflow=brainstorming --phase=03 --step=3.10 --project-root=. 2>&1
```

---

## Phase Exit Verification

Before transitioning to Phase 04, verify ALL exit criteria:

```
VERIFY_EXIT:
  CHECK: session.current_state.type is not null
    IF FAIL: HALT -- "Exit blocked: Current state not documented."
  CHECK: session.problem_analysis.as_is_process_model is populated
    IF FAIL: HALT -- "Exit blocked: As-is process model not captured."
  CHECK: len(session.root_causes) >= 3 OR session.root_cause_found == true
    IF FAIL: HALT -- "Exit blocked: Less than 3 Why levels completed without root cause found."
  CHECK: session.pain_points.length >= 1
    IF FAIL: HALT -- "Exit blocked: No pain points identified."
  CHECK: ALL pain points have severity set
    IF FAIL: HALT -- "Exit blocked: Pain point '{description}' missing severity."
  CHECK: session.problem_statement is non-empty AND session.problem_statement_validated == true
    IF FAIL: HALT -- "Exit blocked: Problem statement not generated or not validated."
  CHECK: session.phases["03"].context_check_completed == true
    IF FAIL: HALT -- "Exit blocked: Context window check not completed."
  CHECK: session.phases["03"].questions_answered >= 6
    IF FAIL: HALT -- "Exit blocked: Minimum 6 questions required, only {count} answered."
```

Update the conversation checkpoint on successful exit (per
`references/conversation-checkpoint-format.md`): set the Phase 03 block `completed: true`,
write its `phase_summary`, advance `current_phase` to `"04"`.

VERIFY: `tmp/{BRAINSTORM_ID}/checkpoint.json` shows the Phase 03 block `completed: true`.
IF write fails: HALT -- "Phase 03 exit checkpoint not saved."

---

## Exit Gate

```bash
devforgeai-validate phase-complete ${BRAINSTORM_ID} --workflow=brainstorming --phase=03 --checkpoint-passed --project-root=. 2>&1
```

| Exit Code | Action |
|-----------|--------|
| 0 | Phase 03 complete — proceed to next phase |
| 127 | CLI not installed — proceed without enforcement |
| Other | HALT — checkpoint/step validation failed |

---

## Phase Transition Display

Display: "Phase 03 Complete — Problem & Current-State Analysis. Problem:
{problem_statement}. Root cause (level {root_cause_level}): {deepest_root_cause}.
Pain points: {count}. Proceeding to Phase 04 (Future-State & Opportunity Mapping)."
