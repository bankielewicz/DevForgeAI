# Phase 07: Constraints & Solution Scope

## Entry Gate

```bash
devforgeai-validate phase-check ${BRAINSTORM_ID} --workflow=brainstorming --from=06 --to=07 --project-root=. 2>&1
```

| Exit Code | Action |
|-----------|--------|
| 0 | Proceed to Phase 07 |
| 127 | CLI not installed — proceed without enforcement |
| Other | HALT — previous phase not complete |

---

## Contract

| Attribute | Value |
|-----------|-------|
| **PURPOSE** | Understand WHAT LIMITS the solution space — budget, timeline, resource, technical, and organizational constraints — name the explicit non-goals, and draw the solution context boundary |
| **REFERENCE** | `.claude/skills/spec-driven-brainstorming/references/constraint-discovery-workflow.md` |
| **STEP COUNT** | 8 mandatory steps |
| **MINIMUM QUESTIONS** | 4 |
| **GOVERNING ADR** | ADR-065 |

Renumbered from the former Phase 04 (Constraint Discovery) and expanded. The five
constraint steps are carried forward; the Out-of-Scope Generation step (work item Z17) is
kept; and a new **Solution Context Boundary** step is added — drawing what sits inside
the solution, what sits outside it, and which external systems it must interface with.

## Phase Exit Criteria

Field names listed are the canonical RECORD targets — each maps to the `constraints_scope`
section of the data island (`references/brainstorm.schema.json` v2.0). The working
session captures keep richer sub-fields under `session.constraints_scope.*`; the flat
`hard_constraints[]` list is derived in Step 7.5.

- [ ] Budget range identified (even if "TBD") → `session.constraints_scope.budget_range`
- [ ] Timeline identified → `session.constraints_scope.timeline`
- [ ] Resource availability assessed → `session.constraints_scope.resources.availability`
- [ ] Technical constraints documented → `session.constraints_scope.technical.requirements`
- [ ] Organizational constraints documented → `session.constraints_scope.organizational.requirements`
- [ ] Hard-constraints list derived → `session.constraints_scope.hard_constraints` (length ≥ 1)
- [ ] Out-of-scope items captured → `session.constraints_scope.out_of_scope` (length ≥ 1; target 3-5; warn-only if < 3)
- [ ] Solution context boundary captured → `session.constraints_scope.context_boundary` (inside + outside populated)
- [ ] Conversation checkpoint updated with Phase 07 exchanges
- [ ] Context window check completed → `session.phases["07"].context_check_completed`

**IF any criterion is unmet: HALT. Do NOT proceed to Phase 08.**

---

## Reference Loading

```
Read(file_path=".claude/skills/spec-driven-brainstorming/references/constraint-discovery-workflow.md")
Read(file_path=".claude/skills/spec-driven-brainstorming/references/question-templates.md")
Read(file_path=".claude/skills/spec-driven-brainstorming/references/conversation-checkpoint-format.md")
```

IF any Read fails: HALT -- "Phase 07 reference files not loaded. Cannot proceed without reference material."

---

## Mandatory Steps

### Step 7.1: Budget Constraints

EXECUTE:
```
AskUserQuestion: template=QT-3
  question_text: "What budget range is available for this initiative?"
  header: "Budget"
  range_type: budget

Store in session.constraints_scope.budget_range.
```

Follow-Up (only if budget defined — not "Not defined yet"):
```
IF response != "Not defined yet":
  AskUserQuestion:
    questions:
      - question: "Is this budget flexible or fixed?"
        header: "Flexibility"
        multiSelect: false
        options:
          - label: "Fixed - cannot exceed"
            description: "Hard budget limit"
          - label: "Somewhat flexible"
            description: "Can adjust with justification"
          - label: "Very flexible"
            description: "Budget can grow if value proven"
  session.constraints_scope.budget_flexibility = response

  AskUserQuestion:
    questions:
      - question: "Is there budget for ongoing operational costs?"
        header: "Ongoing"
        multiSelect: false
        options:
          - label: "Yes - included in budget"
            description: "Operating costs considered"
          - label: "Separate budget"
            description: "OpEx is different from CapEx"
          - label: "Not considered yet"
            description: "Need to discuss"
  session.constraints_scope.budget_ongoing_costs = response

ELSE:
  session.constraints_scope.budget_flexibility = "TBD"
  session.constraints_scope.budget_ongoing_costs = "TBD"
```

VERIFY: `session.constraints_scope.budget_range` is set.

RECORD: Append the exchange to the Phase 07 checkpoint block; persist the budget fields.

```bash
devforgeai-validate phase-record ${BRAINSTORM_ID} --workflow=brainstorming --phase=07 --step=7.1 --project-root=. 2>&1
```

---

### Step 7.2: Timeline Constraints

EXECUTE:
```
AskUserQuestion: template=QT-3
  question_text: "When does this need to be done?"
  header: "Timeline"
  range_type: timeline

Store in session.constraints_scope.timeline.
```

Follow-Up (only if urgent):
```
IF response IN ("ASAP (< 1 month)", "This quarter"):
  AskUserQuestion:
    questions:
      - question: "Is this deadline negotiable?"
        header: "Fixed?"
        multiSelect: false
        options:
          - label: "Fixed - regulatory/contractual"
            description: "Cannot miss this date"
          - label: "Fixed - business event"
            description: "Tied to launch/event"
          - label: "Preferred but flexible"
            description: "Can adjust if needed"
  session.constraints_scope.timeline_flexibility = response

  AskUserQuestion:
    questions:
      - question: "What happens if the deadline is missed?"
        header: "Consequence"
        multiSelect: false
        options:
          - label: "Significant penalties"
            description: "Financial or legal impact"
          - label: "Missed opportunity"
            description: "Business impact but no penalty"
          - label: "Minor inconvenience"
            description: "Not critical"
  session.constraints_scope.timeline_consequence = response

ELSE:
  session.constraints_scope.timeline_flexibility = "Flexible"
  session.constraints_scope.timeline_consequence = "N/A"
```

VERIFY: `session.constraints_scope.timeline` is set.

RECORD: Append the exchange to the Phase 07 checkpoint block; persist the timeline fields.

```bash
devforgeai-validate phase-record ${BRAINSTORM_ID} --workflow=brainstorming --phase=07 --step=7.2 --project-root=. 2>&1
```

---

### Step 7.3: Resource Constraints

EXECUTE:
```
AskUserQuestion:
  questions:
    - question: "What team or resources are available for this initiative?"
      header: "Resources"
      multiSelect: false
      options:
        - label: "Dedicated team available"
          description: "Have people assigned"
        - label: "Shared resources"
          description: "People split across projects"
        - label: "Need to hire/contract"
          description: "No current resources"
        - label: "Not sure"
          description: "Resource plan unclear"

Store in session.constraints_scope.resources.availability.
```

Follow-Up (team size — only if resources exist):
```
IF response IN ("Dedicated team available", "Shared resources"):
  AskUserQuestion: template=QT-3
    question_text: "Approximately how many people?"
    header: "Team Size"
    range_type: team_size
  session.constraints_scope.resources.team_size = response
ELSE:
  session.constraints_scope.resources.team_size = "TBD"
```

Follow-Up (skill gaps — unconditional):
```
AskUserQuestion: template=QT-4
  question_text: "Are there any skill gaps that would need to be filled?"
  header: "Skill Gaps"
  category: skill_gap

Store in session.constraints_scope.resources.skill_gaps.
```

VERIFY: `session.constraints_scope.resources.{availability, team_size, skill_gaps}` all set.

RECORD: Append the exchange to the Phase 07 checkpoint block; persist
`session.constraints_scope.resources`.

```bash
devforgeai-validate phase-record ${BRAINSTORM_ID} --workflow=brainstorming --phase=07 --step=7.3 --project-root=. 2>&1
```

---

### Step 7.4: Technical Constraints

EXECUTE:
```
AskUserQuestion: template=QT-4
  question_text: "Are there technical constraints we need to work within?"
  header: "Tech Limits"
  category: technical_constraint

Store in session.constraints_scope.technical.requirements.
```

Follow-Up (integration systems):
```
IF "Must integrate with existing systems" selected:
  AskUserQuestion: template=QT-5
    question_text: "Which systems must be integrated? List each."
    header: "Systems"
    intent: list
  Capture system names; store in session.constraints_scope.technical.systems[].
```

Follow-Up (security standards):
```
IF "Must meet security standards" selected:
  AskUserQuestion: template=QT-4
    question_text: "Which security or compliance standards apply?"
    header: "Standards"
    category: security_standard
  Store in session.constraints_scope.technical.security_standards[].
```

VERIFY: `session.constraints_scope.technical.requirements` is set; conditional sub-fields populated if applicable.

RECORD: Append the exchange to the Phase 07 checkpoint block; persist
`session.constraints_scope.technical`.

```bash
devforgeai-validate phase-record ${BRAINSTORM_ID} --workflow=brainstorming --phase=07 --step=7.4 --project-root=. 2>&1
```

---

### Step 7.5: Organizational Constraints

EXECUTE:
```
AskUserQuestion: template=QT-4
  question_text: "Are there organizational or political constraints?"
  header: "Org Limits"
  category: org_constraint

Store in session.constraints_scope.organizational.requirements.
```

Follow-Up (change resistance):
```
IF "Change resistance expected" selected:
  AskUserQuestion:
    questions:
      - question: "Where is the resistance likely to come from?"
        header: "Source"
        multiSelect: true
        options:
          - label: "End users"
            description: "People who use current system"
          - label: "IT department"
            description: "Technical teams"
          - label: "Management"
            description: "Middle management"
          - label: "Executive leadership"
            description: "Senior leaders"
  session.constraints_scope.organizational.resistance_sources = response

  AskUserQuestion:
    questions:
      - question: "What's driving the resistance?"
        header: "Cause"
        multiSelect: true
        options:
          - label: "Fear of job loss"
            description: "Automation concerns"
          - label: "Comfort with current system"
            description: "Change fatigue"
          - label: "Previous bad experiences"
            description: "Past failures"
          - label: "Unclear benefits"
            description: "Don't see the value"
  session.constraints_scope.organizational.resistance_causes = response

ELSE:
  session.constraints_scope.organizational.resistance_sources = []
  session.constraints_scope.organizational.resistance_causes = []
```

Derive the flat hard-constraints list:
```
session.constraints_scope.hard_constraints = []

# Pull the non-negotiable items from the rich captures into one flat one-line list.
IF session.constraints_scope.budget_flexibility starts with "Fixed":
  Append "Budget: {budget_range} (fixed)" to hard_constraints.
IF session.constraints_scope.timeline_flexibility starts with "Fixed":
  Append "Timeline: {timeline} (fixed)" to hard_constraints.
FOR each item in session.constraints_scope.technical.requirements:
  Append "Technical: {item}" to hard_constraints.
FOR each item in session.constraints_scope.organizational.requirements:
  Append "Organizational: {item}" to hard_constraints.

IF hard_constraints is empty:
  Append "No hard constraints identified — solution space is open." to hard_constraints.
```

VERIFY: `session.constraints_scope.organizational.requirements` is set; resistance
sub-fields populated if applicable; `session.constraints_scope.hard_constraints` has
length ≥ 1.

RECORD: Append the exchange to the Phase 07 checkpoint block; persist
`session.constraints_scope.organizational` and `session.constraints_scope.hard_constraints`.

```bash
devforgeai-validate phase-record ${BRAINSTORM_ID} --workflow=brainstorming --phase=07 --step=7.5 --project-root=. 2>&1
```

---

### Step 7.6: Out-of-Scope Generation (Explicit Non-Goals)

**Methodology reference:** `references/brainstorming-techniques.md` § 6 (Out-of-Scope
Generation — Explicit Non-Goals). Loads on first execution of this step. Kept from the
former Phase 04 Step 4.6 (work item Z17).

EXECUTE:

Display:
"Now let's name what we are explicitly NOT building. This isn't the same as MoSCoW
'Won't Have' (which classifies things we considered). This is generative: name 3-5
things that someone might naturally expect or request, but you will deliberately
exclude — to keep scope focused."

```
Initialize: session.constraints_scope.out_of_scope = []
Initialize: N = 1

Loop (target: 3-5 items):
  AskUserQuestion: template=QT-5 (intent: describe)
    question_text: "Out of scope #{N}: name something this initiative will deliberately
                    NOT do. (Choose 'Skip this question' to stop.)"
    header: "Anti-feature {N}"

  IF user selects "Skip this question": BREAK

  anti_feature = response

  AskUserQuestion: template=QT-5 (intent: explain)
    question_text: "Why is '{anti_feature}' out of scope?"
    header: "Rationale"

  rationale = response

  Append {item: anti_feature, rationale: rationale} to session.constraints_scope.out_of_scope.
  N += 1
```

VERIFY: `session.constraints_scope.out_of_scope` is a list with length ≥ 1.
  IF `len(session.constraints_scope.out_of_scope) == 0`:
    HALT -- "Step 7.6: At least one out-of-scope item must be captured. Re-prompt user."
  ELSE IF `len(session.constraints_scope.out_of_scope) < 3`:
    Display: "Note: {count} item(s) captured. Methodology recommends 3-5. Continuing —
    these can be augmented in Phase 09 (MoSCoW)."
  (Length 1-2 is a warn-only state; length 0 HALTs.)

RECORD: Append the exchanges to the Phase 07 checkpoint block; persist
`session.constraints_scope.out_of_scope`. The items feed Phase 09 MoSCoW classification
as pre-populated Won't Have entries with attribution `source: "out_of_scope_pregeneration"`.

```bash
devforgeai-validate phase-record ${BRAINSTORM_ID} --workflow=brainstorming --phase=07 --step=7.6 --project-root=. 2>&1
```

---

### Step 7.7: Solution Context Boundary

Draw the boundary of the solution: what the solution itself covers (inside), what is
deliberately external (outside), and which external systems or actors it must interface
with across that boundary. This complements the Out-of-Scope list — out-of-scope names
*features not built*; the context boundary names *the system's edges*.

EXECUTE (Inside the boundary):
```
AskUserQuestion: template=QT-5 (intent: list)
  question_text: "List what sits INSIDE the solution — the capabilities, data, or
                  processes this solution itself will own and control."
  header: "Inside"

session.constraints_scope.context_boundary.inside = [captured items]
```

EXECUTE (Outside the boundary):
```
AskUserQuestion: template=QT-5 (intent: list)
  question_text: "List what sits OUTSIDE the solution — things in the surrounding
                  environment the solution depends on or affects but does NOT own."
  header: "Outside"

session.constraints_scope.context_boundary.outside = [captured items]
```

EXECUTE (External interfaces):
```
AskUserQuestion: template=QT-5 (intent: list)
  question_text: "List the external systems, services, or actors the solution must
                  INTERFACE with across that boundary — APIs, data feeds, user roles,
                  upstream/downstream systems. (May be empty.)"
  header: "Interfaces"

session.constraints_scope.context_boundary.external_interfaces = [captured items]
```

VERIFY: `session.constraints_scope.context_boundary.inside` and
`session.constraints_scope.context_boundary.outside` are both populated
(length ≥ 1); `external_interfaces` is set (may be empty).
IF inside or outside is empty: HALT -- "Step 7.7: Solution context boundary incomplete — inside and outside must both be populated."

RECORD: Append the exchanges to the Phase 07 checkpoint block; persist
`session.constraints_scope.context_boundary`.

```bash
devforgeai-validate phase-record ${BRAINSTORM_ID} --workflow=brainstorming --phase=07 --step=7.7 --project-root=. 2>&1
```

---

### Step 7.8: Context Window Check

EXECUTE:
```
IF estimated_context_usage > 70%:
  AskUserQuestion: template=QT-1
    question_text: "Context window is approximately {PERCENT}% full. Continue or save?"
    header: "Session"
    overrides:
      "Yes (Recommended)": { label: "Continue", description: "Proceed to Phase 08 (Requirements Definition)" }
      "No":                { label: "Save and continue later", description: "Update checkpoint and exit" }
      remove: ["Skip / Defer"]

  IF response == "Save and continue later":
    Update the conversation checkpoint with all Phase 07 data
    Display: "Session saved. Resume with: /brainstorm --resume {BRAINSTORM_ID}"
    EXIT skill
ELSE:
  Display: "Context window healthy. Proceeding to Phase 08."
```

VERIFY: the context window check was performed.
IF skipped: HALT -- "Step 7.8: Context Window Check not performed."

RECORD: Persist `session.phases["07"].context_check_completed = true`.

```bash
devforgeai-validate phase-record ${BRAINSTORM_ID} --workflow=brainstorming --phase=07 --step=7.8 --project-root=. 2>&1
```

---

## Phase Exit Verification

Before transitioning to Phase 08, verify ALL exit criteria:

```
VERIFY_EXIT:
  CHECK: session.constraints_scope.budget_range is set
    IF FAIL: HALT -- "Exit blocked: Budget range not captured."
  CHECK: session.constraints_scope.timeline is set
    IF FAIL: HALT -- "Exit blocked: Timeline not captured."
  CHECK: session.constraints_scope.resources.availability is set
    IF FAIL: HALT -- "Exit blocked: Resource availability not assessed."
  CHECK: session.constraints_scope.technical.requirements is set
    IF FAIL: HALT -- "Exit blocked: Technical constraints not documented."
  CHECK: session.constraints_scope.organizational.requirements is set
    IF FAIL: HALT -- "Exit blocked: Organizational constraints not documented."
  CHECK: session.constraints_scope.hard_constraints.length >= 1
    IF FAIL: HALT -- "Exit blocked: Hard-constraints list not derived."
  CHECK: session.constraints_scope.out_of_scope.length >= 1
    IF FAIL: HALT -- "Exit blocked: No out-of-scope items captured."
  CHECK: session.constraints_scope.context_boundary.inside.length >= 1 AND
         session.constraints_scope.context_boundary.outside.length >= 1
    IF FAIL: HALT -- "Exit blocked: Solution context boundary incomplete."
  CHECK: session.phases["07"].context_check_completed == true
    IF FAIL: HALT -- "Exit blocked: Context window check not completed."
  CHECK: session.phases["07"].questions_answered >= 4
    IF FAIL: HALT -- "Exit blocked: Minimum 4 questions required, only {count} answered."
```

Update the conversation checkpoint on successful exit (per
`references/conversation-checkpoint-format.md`): set the Phase 07 block `completed: true`,
write its `phase_summary`, advance `current_phase` to `"08"`.

VERIFY: `tmp/{BRAINSTORM_ID}/checkpoint.json` shows the Phase 07 block `completed: true`.
IF write fails: HALT -- "Phase 07 exit checkpoint not saved."

---

## Exit Gate

```bash
devforgeai-validate phase-complete ${BRAINSTORM_ID} --workflow=brainstorming --phase=07 --checkpoint-passed --project-root=. 2>&1
```

| Exit Code | Action |
|-----------|--------|
| 0 | Phase 07 complete — proceed to next phase |
| 127 | CLI not installed — proceed without enforcement |
| Other | HALT — checkpoint/step validation failed |

---

## Phase Transition Display

Display: "Phase 07 Complete — Constraints & Solution Scope. Budget: {budget_range}.
Timeline: {timeline}. Hard constraints: {count}. Out-of-scope items: {count}. Context
boundary drawn ({inside_count} inside / {outside_count} outside). Proceeding to Phase 08
(Requirements Definition)."
