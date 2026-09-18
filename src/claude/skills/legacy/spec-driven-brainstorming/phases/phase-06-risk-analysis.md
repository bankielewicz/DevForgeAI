# Phase 06: Risk Analysis

## Entry Gate

```bash
devforgeai-validate phase-check ${BRAINSTORM_ID} --workflow=brainstorming --from=05 --to=06 --project-root=. 2>&1
```

| Exit Code | Action |
|-----------|--------|
| 0 | Proceed to Phase 06 |
| 127 | CLI not installed — proceed without enforcement |
| Other | HALT — previous phase not complete |

---

## Contract

| Attribute | Value |
|-----------|-------|
| **PURPOSE** | Identify the risks to this initiative, assess each by likelihood and impact, plan mitigation and ownership, and run a pre-mortem to surface failure modes while they can still be addressed |
| **REFERENCE** | `.claude/skills/spec-driven-brainstorming/references/conversation-checkpoint-format.md` |
| **STEP COUNT** | 6 mandatory steps |
| **MINIMUM QUESTIONS** | 3 |
| **GOVERNING ADR** | ADR-065 |

NEW phase in the 11-phase Business Analysis workflow. Phase 05 established whether the
initiative is worth doing and can be done; this phase establishes **what could go wrong**.
It produces a structured risk register — each risk scored, mitigated, and owned — and
relocates the Pre-Mortem exercise (formerly Phase 05 Step 5.6.5, work item Z16) here,
where it belongs alongside the rest of the risk work.

## Phase Exit Criteria

Field names listed are the canonical RECORD targets — each maps to the `risk_analysis`
section of the data island (`references/brainstorm.schema.json` v2.0).

- [ ] At least 1 risk identified → `session.risk_analysis.risks` (length ≥ 1)
- [ ] Every risk scored for likelihood and impact → each `risks[]` entry has `likelihood` + `impact`
- [ ] Severity derived for every risk → each `risks[]` entry has `severity`
- [ ] Every risk has a mitigation and an owner → each `risks[]` entry has `mitigation` + `owner`
- [ ] Pre-Mortem completed → `session.risk_analysis.premortem` (length ≥ 1; warn-only if 0)
- [ ] Conversation checkpoint updated with Phase 06 exchanges
- [ ] Context window check completed → `session.phases["06"].context_check_completed`

**IF any criterion is unmet: HALT. Do NOT proceed to Phase 07.**

---

## Reference Loading

```
Read(file_path=".claude/skills/spec-driven-brainstorming/references/conversation-checkpoint-format.md")
Read(file_path=".claude/skills/spec-driven-brainstorming/references/user-interaction-patterns.md")
Read(file_path=".claude/skills/spec-driven-brainstorming/references/question-templates.md")
```

IF any Read fails: HALT -- "Phase 06 reference files not loaded. Cannot proceed without reference material."

---

## Mandatory Steps

### Step 6.1: Risk Identification

Seed candidate risks from earlier phases, then ask the user to add any the analysis
missed. Risk IDs follow the pattern `RISK-NNN` (`RISK-001`, `RISK-002`, …).

EXECUTE:
```
Initialize: session.risk_analysis.risks = []

Review earlier phases for risk signals and propose candidates:
  - From Phase 03 pain points → operational / problem-persistence risks
  - From Phase 04 opportunities and technology ideas → delivery / technical risks
  - From Phase 05 feasibility ratings → any "Low" or "Medium" rating is a candidate risk

Display the proposed candidate risks as a numbered list.

AskUserQuestion: template=QT-5 (intent: list)
  question_text: "Here are the risks I see from our discussion so far. What other risks
                  should we add? (Choose 'Done — no more to add' to finish.)"
  header: "Risks"

Loop:
  IF user selects "Done — no more to add": BREAK
  Capture the user's risk description.
  Continue prompting for the next risk.

Combine the user-confirmed candidates and user-added risks into a single list. Assign
each a sequential id RISK-001, RISK-002, … and append to session.risk_analysis.risks
with {id, description}.
```

VERIFY: `session.risk_analysis.risks` has length ≥ 1.
IF empty: HALT -- "Step 6.1: At least one risk must be identified. Re-prompt the user — every initiative carries risk."

RECORD: Append the exchange to the Phase 06 checkpoint block; persist
`session.risk_analysis.risks`.

```bash
devforgeai-validate phase-record ${BRAINSTORM_ID} --workflow=brainstorming --phase=06 --step=6.1 --project-root=. 2>&1
```

---

### Step 6.2: Likelihood & Impact Assessment

Score each risk on two axes, then derive severity from the matrix below.

EXECUTE:
```
FOR each risk in session.risk_analysis.risks:
  AskUserQuestion:
    questions:
      - question: "How likely is '{risk.description}' to occur?"
        header: "Likelihood"
        multiSelect: false
        options:
          - label: "Low"
            description: "Unlikely — would be a surprise"
          - label: "Medium"
            description: "Plausible — could reasonably happen"
          - label: "High"
            description: "Likely — expect it unless prevented"
      - question: "If '{risk.description}' occurred, how badly would it hurt the initiative?"
        header: "Impact"
        multiSelect: false
        options:
          - label: "Low"
            description: "Minor — absorbed without major change"
          - label: "Medium"
            description: "Significant — notable rework or delay"
          - label: "High"
            description: "Severe — threatens the initiative"

  risk.likelihood = likelihood answer
  risk.impact = impact answer
```

Derive severity (likelihood × impact):
```
Severity matrix:
  High   likelihood × High   impact → Critical
  High   × Medium  OR  Medium × High → High
  High   × Low     OR  Medium × Medium  OR  Low × High → Medium
  Medium × Low     OR  Low × Medium  OR  Low × Low → Low

FOR each risk: risk.severity = matrix(risk.likelihood, risk.impact)
```

VERIFY: every `risks[]` entry has non-empty `likelihood`, `impact`, and `severity`.
IF any is missing: HALT -- "Step 6.2: Risk scoring incomplete."

RECORD: Append the exchanges to the Phase 06 checkpoint block; persist the updated
`session.risk_analysis.risks` with likelihood, impact, and severity.

```bash
devforgeai-validate phase-record ${BRAINSTORM_ID} --workflow=brainstorming --phase=06 --step=6.2 --project-root=. 2>&1
```

---

### Step 6.3: Mitigation & Ownership

EXECUTE:
```
# Address the highest-severity risks first.
Sort session.risk_analysis.risks by severity (Critical → High → Medium → Low).

FOR each risk in the sorted list:
  AskUserQuestion: template=QT-5 (intent: describe)
    question_text: "How could '{risk.description}' (severity: {risk.severity}) be
                    mitigated, avoided, or reduced?"
    header: "Mitigation"
  risk.mitigation = response

  AskUserQuestion: template=QT-5 (intent: describe)
    question_text: "Who should own '{risk.description}' — the role or person
                    accountable for watching and managing it?"
    header: "Owner"
  risk.owner = response
```

VERIFY: every `risks[]` entry has non-empty `mitigation` and `owner`.
IF any is missing: HALT -- "Step 6.3: Every risk must have a mitigation and an owner."

RECORD: Append the exchanges to the Phase 06 checkpoint block; persist the updated
`session.risk_analysis.risks` with mitigation and owner.

```bash
devforgeai-validate phase-record ${BRAINSTORM_ID} --workflow=brainstorming --phase=06 --step=6.3 --project-root=. 2>&1
```

---

### Step 6.4: Pre-Mortem (Devil's Advocate)

**Methodology reference:** `references/brainstorming-techniques.md` § 5 (Pre-Mortem —
Devil's Advocate / Black Hat). Loads on first execution of this step. Relocated from the
former Phase 05 Step 5.6.5 (work item Z16).

EXECUTE:

Display:
"Pre-Mortem exercise. Imagine it's 6 months from now and our top opportunity failed
catastrophically. What was the cause? This isn't pessimism — it's surfacing risks while
we can still address them."

```
Initialize: session.risk_analysis.premortem = []

Display the compiled opportunities from Phase 04 (session.opportunity.opportunities) as
a numbered list.

AskUserQuestion:
  questions:
    - question: "Which 3 of these opportunities are the most significant to pressure-test?"
      header: "Top 3"
      multiSelect: true
      options:
        # Options generated dynamically from session.opportunity.opportunities[]
        - label: "{opportunity_1.description}"
          description: "Source: {opportunity_1.source}"
        - label: "{opportunity_2.description}"
          description: "Source: {opportunity_2.source}"
        ...

selected = the up-to-3 opportunities the user picked.

FOR each opp in selected:
  AskUserQuestion: template=QT-5 (intent: explain)
    question_text: "If '{opp.description}' failed catastrophically in 6 months, what was
                    the most likely cause?"
    header: "Pre-Mortem"
  failure_cause = response
  Append {opportunity_id: opp.id, opportunity_description: opp.description,
          failure_cause: failure_cause} to session.risk_analysis.premortem.

  AskUserQuestion: template=QT-1 (variant: 2-option, with Skip)
    question_text: "Should we add '{failure_cause}' to the risk register as a tracked risk?"
    header: "Add risk?"
  IF response == "Yes":
    Assign the next sequential id (RISK-NNN).
    Append to session.risk_analysis.risks with:
      id: "RISK-NNN"
      description: failure_cause
      source: "premortem"
      likelihood: "Medium"   # default — refine with the user if time allows
      impact: "High"         # pre-mortem causes are catastrophic by definition
      severity: "High"       # derived per the Step 6.2 matrix (Medium × High)
      mitigation: ""         # prompt the user for a mitigation before phase exit
      owner: ""              # prompt the user for an owner before phase exit
    IF mitigation or owner is empty:
      Re-run Step 6.3 questioning for this single new risk so the exit criteria hold.
```

VERIFY: `session.risk_analysis.premortem` is a list.
  IF `len(session.risk_analysis.premortem) == 0`:
    Display: "Pre-Mortem skipped. Recommend revisiting before committing to the top
    opportunity."
  (No HALT — this is a warn-only check; Phase 06 exit is not blocked on the pre-mortem.)

RECORD: Append the exchanges to the Phase 06 checkpoint block; persist
`session.risk_analysis.premortem`. Any risk promoted from a pre-mortem cause is persisted
in `session.risk_analysis.risks` with `source: "premortem"` and inherits the risk exit
criteria (likelihood, impact, severity, mitigation, owner).

```bash
devforgeai-validate phase-record ${BRAINSTORM_ID} --workflow=brainstorming --phase=06 --step=6.4 --project-root=. 2>&1
```

---

### Step 6.5: Risk Register Consolidation

EXECUTE:
```
Sort session.risk_analysis.risks by severity (Critical → High → Medium → Low).

Display the consolidated risk register as a table:
  | ID | Risk | Likelihood | Impact | Severity | Mitigation | Owner |

Display: "This register is rendered as a sortable table in the Phase 11 HTML document.
Critical and High risks should be reviewed before the funding decision."
```

VERIFY: every risk in the register has all seven fields populated (`id`, `description`,
`likelihood`, `impact`, `severity`, `mitigation`, `owner`).
IF any field is missing: HALT -- "Step 6.5: Risk register incomplete — {id} is missing {field}."

RECORD: Append the exchange to the Phase 06 checkpoint block; persist the final
`session.risk_analysis.risks`.

```bash
devforgeai-validate phase-record ${BRAINSTORM_ID} --workflow=brainstorming --phase=06 --step=6.5 --project-root=. 2>&1
```

---

### Step 6.6: Context Window Check

EXECUTE:
```
IF estimated_context_usage > 70%:
  AskUserQuestion: template=QT-1
    question_text: "Context window is approximately {PERCENT}% full. Continue or save?"
    header: "Session"
    overrides:
      "Yes (Recommended)": { label: "Continue", description: "Proceed to Phase 07 (Constraints & Solution Scope)" }
      "No":                { label: "Save and continue later", description: "Update checkpoint and exit" }
      remove: ["Skip / Defer"]

  IF response == "Save and continue later":
    Update the conversation checkpoint with all Phase 06 data
    Display: "Session saved. Resume with: /brainstorm --resume {BRAINSTORM_ID}"
    EXIT skill
ELSE:
  Display: "Context window healthy. Proceeding to Phase 07."
```

VERIFY: the context window check was performed.
IF skipped: HALT -- "Step 6.6: Context Window Check not performed."

RECORD: Persist `session.phases["06"].context_check_completed = true`.

```bash
devforgeai-validate phase-record ${BRAINSTORM_ID} --workflow=brainstorming --phase=06 --step=6.6 --project-root=. 2>&1
```

---

## Phase Exit Verification

Before transitioning to Phase 07, verify ALL exit criteria:

```
VERIFY_EXIT:
  CHECK: session.risk_analysis.risks.length >= 1
    IF FAIL: HALT -- "Exit blocked: No risks identified."
  CHECK: every risks[] entry has likelihood, impact, and severity
    IF FAIL: HALT -- "Exit blocked: One or more risks are not fully scored."
  CHECK: every risks[] entry has mitigation and owner
    IF FAIL: HALT -- "Exit blocked: One or more risks lack a mitigation or an owner."
  CHECK: session.risk_analysis.premortem is a list (may be empty — warn-only)
    IF FAIL: HALT -- "Exit blocked: Pre-mortem field not initialised."
  CHECK: session.phases["06"].context_check_completed == true
    IF FAIL: HALT -- "Exit blocked: Context window check not completed."
  CHECK: session.phases["06"].questions_answered >= 3
    IF FAIL: HALT -- "Exit blocked: Minimum 3 questions required, only {count} answered."
```

Update the conversation checkpoint on successful exit (per
`references/conversation-checkpoint-format.md`): set the Phase 06 block `completed: true`,
write its `phase_summary`, advance `current_phase` to `"07"`.

VERIFY: `tmp/{BRAINSTORM_ID}/checkpoint.json` shows the Phase 06 block `completed: true`.
IF write fails: HALT -- "Phase 06 exit checkpoint not saved."

---

## Exit Gate

```bash
devforgeai-validate phase-complete ${BRAINSTORM_ID} --workflow=brainstorming --phase=06 --checkpoint-passed --project-root=. 2>&1
```

| Exit Code | Action |
|-----------|--------|
| 0 | Phase 06 complete — proceed to next phase |
| 127 | CLI not installed — proceed without enforcement |
| Other | HALT — checkpoint/step validation failed |

---

## Phase Transition Display

Display: "Phase 06 Complete — Risk Analysis. Risks identified: {count} ({critical_count}
Critical, {high_count} High). Pre-mortem failure modes surfaced: {premortem_count}.
Proceeding to Phase 07 (Constraints & Solution Scope)."
