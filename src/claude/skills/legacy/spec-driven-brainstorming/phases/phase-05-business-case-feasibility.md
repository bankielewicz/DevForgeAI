# Phase 05: Business Case & Feasibility

## Entry Gate

```bash
devforgeai-validate phase-check ${BRAINSTORM_ID} --workflow=brainstorming --from=04 --to=05 --project-root=. 2>&1
```

| Exit Code | Action |
|-----------|--------|
| 0 | Proceed to Phase 05 |
| 127 | CLI not installed — proceed without enforcement |
| Other | HALT — previous phase not complete |

---

## Contract

| Attribute | Value |
|-----------|-------|
| **PURPOSE** | Build the business case — cost-benefit, expected value, funding justification — and assess whether the initiative is technically, operationally, and economically feasible |
| **REFERENCE** | `.claude/skills/spec-driven-brainstorming/references/conversation-checkpoint-format.md` |
| **STEP COUNT** | 6 mandatory steps |
| **MINIMUM QUESTIONS** | 4 |
| **GOVERNING ADR** | ADR-065 |

NEW phase in the 11-phase Business Analysis workflow. Phases 02–04 established WHO is
affected, WHAT the problem is, and WHAT COULD BE. This phase answers the question a
funding decision actually turns on: **is this worth doing, and can it be done?** Cost and
benefit here are rough order-of-magnitude estimates that justify (or reject) the
initiative — the *available* budget constraint is captured later in Phase 07.

## Phase Exit Criteria

Field names listed are the canonical RECORD targets — each maps to the `business_case`
section of the data island (`references/brainstorm.schema.json` v2.0).

- [ ] Cost estimate captured → `session.business_case.cost_estimate` (non-empty)
- [ ] Expected value / benefit captured → `session.business_case.expected_value` (non-empty)
- [ ] Cost-benefit synthesis written and user-validated → `session.business_case.cost_benefit` (non-empty)
- [ ] Funding justification captured → `session.business_case.funding_justification` (non-empty)
- [ ] Technical feasibility assessed → `session.business_case.feasibility.technical` (non-empty)
- [ ] Operational feasibility assessed → `session.business_case.feasibility.operational` (non-empty)
- [ ] Economic feasibility assessed → `session.business_case.feasibility.economic` (non-empty)
- [ ] Conversation checkpoint updated with Phase 05 exchanges
- [ ] Context window check completed → `session.phases["05"].context_check_completed`

**IF any criterion is unmet: HALT. Do NOT proceed to Phase 06.**

---

## Reference Loading

```
Read(file_path=".claude/skills/spec-driven-brainstorming/references/conversation-checkpoint-format.md")
Read(file_path=".claude/skills/spec-driven-brainstorming/references/user-interaction-patterns.md")
Read(file_path=".claude/skills/spec-driven-brainstorming/references/question-templates.md")
```

IF any Read fails: HALT -- "Phase 05 reference files not loaded. Cannot proceed without reference material."

---

## Mandatory Steps

### Step 5.1: Cost Estimation

Estimate what the initiative will cost to build and run. This is a rough
order-of-magnitude estimate — precision is not expected at the brainstorming stage.

EXECUTE:
```
AskUserQuestion: template=QT-3
  question_text: "Roughly what total cost would it take to build and launch the
                  recommended solution?"
  header: "Cost"
  range_type: budget

Store the rough magnitude in session.business_case.cost_estimate.range.
```

Follow-up (cost composition — always):
```
AskUserQuestion:
  questions:
    - question: "Where would most of that cost go?"
      header: "Cost Drivers"
      multiSelect: true
      options:
        - label: "Engineering / build effort"
          description: "Developer time to build the solution"
        - label: "Software / licensing / infrastructure"
          description: "Tools, cloud, third-party services"
        - label: "Integration with existing systems"
          description: "Connecting to current platforms"
        - label: "Ongoing operations / support"
          description: "Run-cost after launch"
        - label: "Training / change management"
          description: "Getting people to adopt it"

Capture selections in session.business_case.cost_estimate.drivers.
```

VERIFY: `session.business_case.cost_estimate.range` is set.

RECORD: Append the exchange to the Phase 05 checkpoint block; persist
`session.business_case.cost_estimate`.

```bash
devforgeai-validate phase-record ${BRAINSTORM_ID} --workflow=brainstorming --phase=05 --step=5.1 --project-root=. 2>&1
```

---

### Step 5.2: Benefit Identification & Expected Value

EXECUTE (Part A — Benefit categories):
```
AskUserQuestion: template=QT-4
  question_text: "What kinds of value would the recommended solution deliver?"
  header: "Benefits"
  category: benefit_type

Capture selections in session.business_case.benefit_categories.
```

EXECUTE (Part B — Expected value):
```
AskUserQuestion: template=QT-5 (intent: describe)
  question_text: "Quantify the expected value as concretely as you can — e.g. hours
                  saved per week, error rate reduced, revenue gained, cost avoided.
                  A rough number is better than none."
  header: "Expected Value"

Capture the description in session.business_case.expected_value.
```

VERIFY: `session.business_case.expected_value` is a non-empty string.
IF empty: HALT -- "Step 5.2: Expected value not captured."

RECORD: Append the exchange to the Phase 05 checkpoint block; persist
`session.business_case.benefit_categories` and `session.business_case.expected_value`.

```bash
devforgeai-validate phase-record ${BRAINSTORM_ID} --workflow=brainstorming --phase=05 --step=5.2 --project-root=. 2>&1
```

---

### Step 5.3: Cost-Benefit Synthesis

Synthesise the cost estimate (5.1) and expected value (5.2) into a single comparative
statement, then have the user validate it.

EXECUTE:
```
Compose a cost-benefit summary:
  "Estimated cost: {session.business_case.cost_estimate.range}, driven mainly by
   {top cost drivers}. Expected value: {session.business_case.expected_value}.
   On balance this initiative {appears worth / appears marginal / appears not worth}
   the investment."

Display the summary.

AskUserQuestion: template=QT-5 (intent: rewrite)
  question_text: "Does this cost-benefit summary read accurately? Adjust it if not."
  header: "Validate"

IF response == "Needs minor adjustment" OR response == "Let me rewrite it":
  Capture the user's refined wording.
  session.business_case.cost_benefit = refined wording
ELSE:
  session.business_case.cost_benefit = the displayed summary
```

VERIFY: `session.business_case.cost_benefit` is a non-empty string the user has confirmed.
IF empty: HALT -- "Step 5.3: Cost-benefit synthesis not captured."

RECORD: Append the exchange to the Phase 05 checkpoint block; persist
`session.business_case.cost_benefit`.

```bash
devforgeai-validate phase-record ${BRAINSTORM_ID} --workflow=brainstorming --phase=05 --step=5.3 --project-root=. 2>&1
```

---

### Step 5.4: Funding Justification

EXECUTE:
```
AskUserQuestion: template=QT-5 (intent: explain)
  question_text: "If you had to justify funding this initiative to a decision-maker in
                  two or three sentences, what would you say? Why this, why now?"
  header: "Funding Case"

Capture the description in session.business_case.funding_justification.
```

Follow-up (cost of inaction — always):
```
AskUserQuestion:
  questions:
    - question: "What happens if this initiative is NOT funded?"
      header: "Do Nothing"
      multiSelect: false
      options:
        - label: "Problem worsens over time"
          description: "Cost or pain grows if unaddressed"
        - label: "Status quo holds — no worse"
          description: "Tolerable but the opportunity is lost"
        - label: "Competitive / strategic disadvantage"
          description: "Falling behind alternatives or competitors"
        - label: "Not sure"
          description: "Hard to predict"

Append the cost-of-inaction answer to session.business_case.funding_justification
as a supporting clause.
```

VERIFY: `session.business_case.funding_justification` is a non-empty string.
IF empty: HALT -- "Step 5.4: Funding justification not captured."

RECORD: Append the exchange to the Phase 05 checkpoint block; persist
`session.business_case.funding_justification`.

```bash
devforgeai-validate phase-record ${BRAINSTORM_ID} --workflow=brainstorming --phase=05 --step=5.4 --project-root=. 2>&1
```

---

### Step 5.5: Feasibility Assessment

Assess three feasibility dimensions. Each maps to a sub-field of
`session.business_case.feasibility`.

EXECUTE (Technical feasibility):
```
AskUserQuestion: template=QT-2
  question_text: "How technically feasible is the recommended solution with the skills
                  and technology available?"
  header: "Technical"
  scale_type: confidence
  overrides:
    "High":   { label: "Clearly buildable", description: "Known technology, available skills" }
    "Medium": { label: "Buildable with effort", description: "Some unknowns or skill gaps" }
    "Low":    { label: "Significant technical risk", description: "Unproven approach or major gaps" }

Capture the rating; then:
AskUserQuestion: template=QT-5 (intent: explain)
  question_text: "What is the main technical factor behind that rating?"
  header: "Technical Why"

session.business_case.feasibility.technical = "{rating}: {explanation}"
```

EXECUTE (Operational feasibility):
```
AskUserQuestion: template=QT-2
  question_text: "How feasible is it for the organisation to operate, support, and
                  sustain this solution after launch?"
  header: "Operational"
  scale_type: confidence
  overrides:
    "High":   { label: "Easily absorbed", description: "Existing teams can run it" }
    "Medium": { label: "Manageable with change", description: "Needs new process or roles" }
    "Low":    { label: "Hard to sustain", description: "No clear operational owner" }

Capture the rating; then:
AskUserQuestion: template=QT-5 (intent: explain)
  question_text: "What is the main operational factor behind that rating?"
  header: "Operational Why"

session.business_case.feasibility.operational = "{rating}: {explanation}"
```

EXECUTE (Economic feasibility):
```
AskUserQuestion: template=QT-2
  question_text: "Given the cost-benefit summary, how economically feasible is this
                  initiative — does the value justify the spend?"
  header: "Economic"
  scale_type: confidence
  overrides:
    "High":   { label: "Value clearly exceeds cost", description: "Strong return" }
    "Medium": { label: "Roughly breaks even", description: "Value and cost are close" }
    "Low":    { label: "Cost likely exceeds value", description: "Hard to justify economically" }

Capture the rating; then:
AskUserQuestion: template=QT-5 (intent: explain)
  question_text: "What is the main economic factor behind that rating?"
  header: "Economic Why"

session.business_case.feasibility.economic = "{rating}: {explanation}"
```

VERIFY: `session.business_case.feasibility.technical`,
`session.business_case.feasibility.operational`, and
`session.business_case.feasibility.economic` are all non-empty strings.
IF any is empty: HALT -- "Step 5.5: Feasibility assessment incomplete."

RECORD: Append the three exchanges to the Phase 05 checkpoint block; persist
`session.business_case.feasibility`.

```bash
devforgeai-validate phase-record ${BRAINSTORM_ID} --workflow=brainstorming --phase=05 --step=5.5 --project-root=. 2>&1
```

---

### Step 5.6: Context Window Check

EXECUTE:
```
IF estimated_context_usage > 70%:
  AskUserQuestion: template=QT-1
    question_text: "Context window is approximately {PERCENT}% full. Continue or save?"
    header: "Session"
    overrides:
      "Yes (Recommended)": { label: "Continue", description: "Proceed to Phase 06 (Risk Analysis)" }
      "No":                { label: "Save and continue later", description: "Update checkpoint and exit" }
      remove: ["Skip / Defer"]

  IF response == "Save and continue later":
    Update the conversation checkpoint with all Phase 05 data
    Display: "Session saved. Resume with: /brainstorm --resume {BRAINSTORM_ID}"
    EXIT skill
ELSE:
  Display: "Context window healthy. Proceeding to Phase 06."
```

VERIFY: the context window check was performed.
IF skipped: HALT -- "Step 5.6: Context Window Check not performed."

RECORD: Persist `session.phases["05"].context_check_completed = true`.

```bash
devforgeai-validate phase-record ${BRAINSTORM_ID} --workflow=brainstorming --phase=05 --step=5.6 --project-root=. 2>&1
```

---

## Phase Exit Verification

Before transitioning to Phase 06, verify ALL exit criteria:

```
VERIFY_EXIT:
  CHECK: session.business_case.cost_estimate.range is set
    IF FAIL: HALT -- "Exit blocked: Cost estimate not captured."
  CHECK: session.business_case.expected_value is non-empty
    IF FAIL: HALT -- "Exit blocked: Expected value not captured."
  CHECK: session.business_case.cost_benefit is non-empty
    IF FAIL: HALT -- "Exit blocked: Cost-benefit synthesis not captured."
  CHECK: session.business_case.funding_justification is non-empty
    IF FAIL: HALT -- "Exit blocked: Funding justification not captured."
  CHECK: session.business_case.feasibility.technical is non-empty
    IF FAIL: HALT -- "Exit blocked: Technical feasibility not assessed."
  CHECK: session.business_case.feasibility.operational is non-empty
    IF FAIL: HALT -- "Exit blocked: Operational feasibility not assessed."
  CHECK: session.business_case.feasibility.economic is non-empty
    IF FAIL: HALT -- "Exit blocked: Economic feasibility not assessed."
  CHECK: session.phases["05"].context_check_completed == true
    IF FAIL: HALT -- "Exit blocked: Context window check not completed."
  CHECK: session.phases["05"].questions_answered >= 4
    IF FAIL: HALT -- "Exit blocked: Minimum 4 questions required, only {count} answered."
```

Update the conversation checkpoint on successful exit (per
`references/conversation-checkpoint-format.md`): set the Phase 05 block `completed: true`,
write its `phase_summary`, advance `current_phase` to `"06"`.

VERIFY: `tmp/{BRAINSTORM_ID}/checkpoint.json` shows the Phase 05 block `completed: true`.
IF write fails: HALT -- "Phase 05 exit checkpoint not saved."

---

## Exit Gate

```bash
devforgeai-validate phase-complete ${BRAINSTORM_ID} --workflow=brainstorming --phase=05 --checkpoint-passed --project-root=. 2>&1
```

| Exit Code | Action |
|-----------|--------|
| 0 | Phase 05 complete — proceed to next phase |
| 127 | CLI not installed — proceed without enforcement |
| Other | HALT — checkpoint/step validation failed |

---

## Phase Transition Display

Display: "Phase 05 Complete — Business Case & Feasibility. Cost-benefit:
{cost_benefit one-line}. Feasibility — technical: {technical rating}, operational:
{operational rating}, economic: {economic rating}. Proceeding to Phase 06 (Risk
Analysis)."
