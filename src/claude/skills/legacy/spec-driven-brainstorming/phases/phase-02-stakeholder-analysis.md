# Phase 02: Stakeholder Analysis

## Entry Gate

```bash
devforgeai-validate phase-check ${BRAINSTORM_ID} --workflow=brainstorming --from=01 --to=02 --project-root=. 2>&1
```

| Exit Code | Action |
|-----------|--------|
| 0 | Proceed to Phase 02 |
| 127 | CLI not installed — proceed without enforcement |
| Other | HALT — previous phase not complete |

---

## Contract

| Attribute | Value |
|-----------|-------|
| **PURPOSE** | Identify WHO is involved in the problem space, WHAT they want, and their power/interest positioning |
| **REFERENCE** | `.claude/skills/spec-driven-brainstorming/references/stakeholder-discovery-workflow.md` |
| **STEP COUNT** | 10 mandatory steps |
| **MINIMUM QUESTIONS** | 7 |
| **GOVERNING ADR** | ADR-065 |

Renumbered from the former Phase 01 and expanded for the full Business Analysis workflow:
a power/interest classification, a RACI assignment, and a per-stakeholder engagement plan
are now first-class outputs alongside the original stakeholder map. The topic itself was
captured in Phase 01.

## Phase Exit Criteria

Field names listed are the canonical RECORD targets — each maps to the `stakeholders`
section of the data island (`references/brainstorm.schema.json` v2.0).

- [ ] At least 1 primary stakeholder identified → `session.stakeholders.primary` (length ≥ 1)
- [ ] At least 1 secondary stakeholder identified → `session.stakeholders.secondary` (length ≥ 1)
- [ ] Goals captured for each primary stakeholder → `session.stakeholders.primary[].goals` (≥ 1 each)
- [ ] Concerns captured for each primary stakeholder → `session.stakeholders.primary[].concerns` (≥ 1 each)
- [ ] Influence, interest, and RACI classified for every stakeholder → `session.stakeholders.registry[]`
- [ ] Engagement plan derived → `session.stakeholders.engagement_plan`
- [ ] Conflicts identified or explicitly marked "none detected" → `session.conflicts`
- [ ] Stakeholder voices captured → `session.stakeholder_voices` (length ≥ `len(session.stakeholders.primary)`)
- [ ] Conversation checkpoint updated with Phase 02 exchanges
- [ ] Context window check completed → `session.phases["02"].context_check_completed`

---

## Reference Loading

```
Read(file_path=".claude/skills/spec-driven-brainstorming/references/stakeholder-discovery-workflow.md")
Read(file_path=".claude/skills/spec-driven-brainstorming/references/user-interaction-patterns.md")
Read(file_path=".claude/skills/spec-driven-brainstorming/references/question-templates.md")
Read(file_path=".claude/skills/spec-driven-brainstorming/references/conversation-checkpoint-format.md")
```

IF any Read fails: HALT -- "Phase 02 reference files not loaded. Cannot proceed without reference material."

---

## Mandatory Steps

### Step 2.1: Identify Primary Decision Maker

EXECUTE:
```
AskUserQuestion:
  questions:
    - question: "Who has the authority to approve or reject solutions for this problem?"
      header: "Decision Maker"
      multiSelect: false
      options:
        - label: "I am the decision maker"
          description: "I have budget and approval authority"
        - label: "Someone else"
          description: "I'll need to get approval from others"
        - label: "Multiple people"
          description: "It's a committee or shared decision"
        - label: "Not sure"
          description: "Decision authority is unclear"
```

Follow-up logic:
```
IF response IN ("Someone else", "Multiple people"):
  AskUserQuestion: template=QT-5 (intent: list)
    question_text: "Who are the key decision makers? List each."
    header: "Who"
  Capture names/roles. Append each to session.stakeholders.primary[].
ELSE IF response == "I am the decision maker":
  Append "User (self)" to session.stakeholders.primary[].
ELSE IF response == "Not sure":
  Ask about budget/approval process to infer the decision maker.
  Append the inferred decision maker to session.stakeholders.primary[].
```

VERIFY: `session.stakeholders.primary.length >= 1`.
IF empty: HALT -- "Step 2.1: No primary stakeholder captured."

RECORD: Append the exchange to the Phase 02 checkpoint block; persist
`session.stakeholders.primary`.

```bash
devforgeai-validate phase-record ${BRAINSTORM_ID} --workflow=brainstorming --phase=02 --step=2.1 --project-root=. 2>&1
```

---

### Step 2.2: Identify End Users

EXECUTE:
```
AskUserQuestion:
  questions:
    - question: "Who will actually use the solution on a daily basis?"
      header: "End Users"
      multiSelect: true
      options:
        - label: "Internal employees"
          description: "Staff within the organization"
        - label: "External customers"
          description: "Paying customers or clients"
        - label: "Partners/vendors"
          description: "Third-party business relationships"
        - label: "The general public"
          description: "Anyone can access it"
```

Follow-up logic:
```
FOR each selected user_type:
  AskUserQuestion:
    questions:
      - question: "How many {user_type} would use this solution?"
        header: "Count"
        multiSelect: false
        options:
          - label: "1-10"
            description: "Small team"
          - label: "10-100"
            description: "Department level"
          - label: "100-1000"
            description: "Company-wide"
          - label: "1000+"
            description: "Large scale"
  Append {type: user_type, count: response} to session.stakeholders.secondary[].
```

VERIFY: At least 1 user type selected; `session.stakeholders.secondary.length >= 1`.

RECORD: Append the exchange to the Phase 02 checkpoint block; persist
`session.stakeholders.secondary`.

```bash
devforgeai-validate phase-record ${BRAINSTORM_ID} --workflow=brainstorming --phase=02 --step=2.2 --project-root=. 2>&1
```

---

### Step 2.3: Identify Affected Parties

EXECUTE:
```
AskUserQuestion:
  questions:
    - question: "Who else will be impacted by this change, even if they don't use the solution directly?"
      header: "Affected"
      multiSelect: true
      options:
        - label: "IT/Operations team"
          description: "Those who maintain systems"
        - label: "Finance/Accounting"
          description: "Those who handle budgets and reporting"
        - label: "Compliance/Legal"
          description: "Those who ensure regulatory compliance"
        - label: "Customer Support"
          description: "Those who help users with issues"
```

VERIFY: Response captured. May be an empty array (acceptable — "no affected parties beyond users").

RECORD: Append the exchange to the Phase 02 checkpoint block; persist
`session.stakeholders.tertiary`.

```bash
devforgeai-validate phase-record ${BRAINSTORM_ID} --workflow=brainstorming --phase=02 --step=2.3 --project-root=. 2>&1
```

---

### Step 2.4: Map Stakeholder Goals

EXECUTE:
```
FOR each stakeholder in session.stakeholders.primary:
  AskUserQuestion:
    questions:
      - question: "What does {stakeholder.name} want to achieve from this initiative?"
        header: "Goals"
        multiSelect: true
        options:
          - label: "Reduce costs"
            description: "Save money on operations"
          - label: "Increase revenue"
            description: "Generate more income"
          - label: "Improve efficiency"
            description: "Do more with less"
          - label: "Reduce risk"
            description: "Prevent problems or losses"
  Append response to stakeholder.goals[].
```

Optional Subagent Enhancement (non-blocking):
```
Task(
  subagent_type="stakeholder-analyst",
  prompt="Analyze stakeholders for: {session.topic}.
          Primary: {session.stakeholders.primary}
          Secondary: {session.stakeholders.secondary}
          Identify goals, concerns, and potential conflicts."
)
```

VERIFY: Every primary stakeholder has `goals.length >= 1`.
IF any stakeholder has empty goals: HALT -- "Step 2.4: Goals not captured for {stakeholder.name}."

RECORD: Append the exchange to the Phase 02 checkpoint block; persist
`session.stakeholders.primary[].goals`.

```bash
devforgeai-validate phase-record ${BRAINSTORM_ID} --workflow=brainstorming --phase=02 --step=2.4 --project-root=. 2>&1
```

---

### Step 2.5: Map Stakeholder Concerns

EXECUTE:
```
FOR each stakeholder in session.stakeholders.primary:
  AskUserQuestion:
    questions:
      - question: "What concerns or fears does {stakeholder.name} have about this initiative?"
        header: "Concerns"
        multiSelect: true
        options:
          - label: "Budget overruns"
            description: "It might cost too much"
          - label: "Timeline delays"
            description: "It might take too long"
          - label: "Disruption"
            description: "It might disrupt current operations"
          - label: "Adoption issues"
            description: "People might not use it"
  Append response to stakeholder.concerns[].
```

VERIFY: Every primary stakeholder has `concerns.length >= 1`.
IF any stakeholder has empty concerns: HALT -- "Step 2.5: Concerns not captured for {stakeholder.name}."

RECORD: Append the exchange to the Phase 02 checkpoint block; persist
`session.stakeholders.primary[].concerns`.

```bash
devforgeai-validate phase-record ${BRAINSTORM_ID} --workflow=brainstorming --phase=02 --step=2.5 --project-root=. 2>&1
```

---

### Step 2.6: Power/Interest Classification & RACI

Build the stakeholder registry — the analytical backbone of the analysis. For every
stakeholder (primary + secondary + tertiary) capture **influence** (their power over the
decision), **interest** (how much the outcome affects them), and a **RACI** role. The
power/interest grid tells later phases who must be satisfied and who merely informed.

EXECUTE:
```
Initialize: session.stakeholders.registry = []

FOR each stakeholder in (primary + secondary + tertiary):
  AskUserQuestion:
    questions:
      - question: "{stakeholder.name} — how much INFLUENCE do they hold over this decision?"
        header: "Influence"
        multiSelect: false
        options:
          - label: "High"
            description: "Can approve, block, or fund"
          - label: "Medium"
            description: "Shapes the decision but doesn't own it"
          - label: "Low"
            description: "Little say in the decision"
      - question: "{stakeholder.name} — how much INTEREST do they have in the outcome?"
        header: "Interest"
        multiSelect: false
        options:
          - label: "High"
            description: "The outcome strongly affects them"
          - label: "Medium"
            description: "Moderately affected"
          - label: "Low"
            description: "Barely affected"
      - question: "{stakeholder.name} — RACI role for the initiative?"
        header: "RACI"
        multiSelect: false
        options:
          - label: "Accountable"
            description: "Owns the outcome — exactly one per initiative"
          - label: "Responsible"
            description: "Does or drives the work"
          - label: "Consulted"
            description: "Two-way input is sought"
          - label: "Informed"
            description: "Kept up to date, one-way"

  Append to session.stakeholders.registry:
    { id, name_or_role: stakeholder.name, category: stakeholder.category,
      influence, interest, raci, goals: stakeholder.goals, concerns: stakeholder.concerns }
```

VERIFY: `session.stakeholders.registry.length` equals the total stakeholder count;
every entry has non-null `influence`, `interest`, and `raci`. Exactly one stakeholder
SHOULD be `Accountable` — if zero or more than one, Display a warning and offer to
re-prompt (warn-only, non-blocking).

RECORD: Append the exchange to the Phase 02 checkpoint block; persist
`session.stakeholders.registry`.

```bash
devforgeai-validate phase-record ${BRAINSTORM_ID} --workflow=brainstorming --phase=02 --step=2.6 --project-root=. 2>&1
```

---

### Step 2.7: Derive the Engagement Plan

EXECUTE:
```
Classify each registry entry by its power/interest quadrant and derive an engagement
posture:
  - High influence + High interest  → "Manage closely" (involve in every decision)
  - High influence + Low interest   → "Keep satisfied" (consult on decisions affecting them)
  - Low influence  + High interest  → "Keep informed" (regular updates, gather feedback)
  - Low influence  + Low interest   → "Monitor" (minimal effort)

Display the derived grid back to the user as a table.

AskUserQuestion: template=QT-1
  question_text: "Here is the engagement posture per stakeholder. Does it look right?"
  header: "Engagement"
  overrides:
    "Yes (Recommended)": { label: "Yes, accurate", description: "Adopt this engagement plan" }
    "No":                { label: "Needs adjustment", description: "I'll correct some postures" }
    remove: ["Skip / Defer"]

IF response == "Needs adjustment":
  Capture the corrections and update the postures.
```

VERIFY: every registry entry has an engagement posture; `session.stakeholders.engagement_plan`
is a non-empty summary of the grid.

RECORD: Append the exchange to the Phase 02 checkpoint block; persist
`session.stakeholders.engagement_plan` and the per-stakeholder postures.

```bash
devforgeai-validate phase-record ${BRAINSTORM_ID} --workflow=brainstorming --phase=02 --step=2.7 --project-root=. 2>&1
```

---

### Step 2.8: Identify Conflicts

EXECUTE (Analysis):
```
conflicts = []
FOR each pair (stakeholder_a, stakeholder_b) in session.stakeholders.primary:
  IF stakeholder_a.goals CONFLICTS_WITH stakeholder_b.goals:
    conflicts.append({
      stakeholders: [stakeholder_a.name, stakeholder_b.name],
      nature: describe_conflict(stakeholder_a.goals, stakeholder_b.goals),
      resolution: null  # addressed in Phase 09 prioritization
    })
```

Conflict detection rules:
- "Reduce costs" vs "Increase features" = resource conflict
- "ASAP timeline" vs "High quality" = speed vs quality
- "Minimal disruption" vs "Complete overhaul" = scope conflict

EXECUTE (User Confirmation):
```
IF len(conflicts) > 0:
  Display the identified conflicts.
  AskUserQuestion: template=QT-1
    question_text: "Are these conflicts accurate? Any others?"
    header: "Validate"
    overrides:
      "Yes (Recommended)": { label: "Yes, accurate", description: "These conflicts are real" }
      "No":                { label: "Some corrections needed", description: "I'll clarify" }
      "Skip / Defer":      { label: "No conflicts", description: "They're actually aligned" }
ELSE:
  Display: "No conflicts detected between stakeholder goals."
  session.conflicts = "none detected"
```

VERIFY: `session.conflicts` is either a list (possibly empty) or the string "none detected" — NOT null.
IF analysis was skipped: HALT -- "Step 2.8: Identify Conflicts was not executed."

RECORD: Append the exchange to the Phase 02 checkpoint block; persist `session.conflicts`.

```bash
devforgeai-validate phase-record ${BRAINSTORM_ID} --workflow=brainstorming --phase=02 --step=2.8 --project-root=. 2>&1
```

---

### Step 2.9: Stakeholder Voice Role-Play

**Methodology reference:** `references/brainstorming-techniques.md` § 7 (Stakeholder Voice
Role-Play). Loads on first execution of this step.

EXECUTE:

Display:
"Stakeholder Voice exercise. You've described the stakeholders objectively. Now speak AS
each one. Each role gets ONE insistence or ONE veto — what's the single non-negotiable
from that person's seat?"

```
Initialize: session.stakeholder_voices = []
stakeholders_to_voice = session.stakeholders.primary + session.stakeholders.secondary

FOR each stakeholder in stakeholders_to_voice:
  AskUserQuestion: template=QT-5 (intent: explain)
    question_text: "Speaking AS {stakeholder.role} ({stakeholder.name}): what's the ONE
                    thing you'd insist on, or absolutely veto, in any solution?"
    header: "{stakeholder.role}"
  IF response is non-empty:
    Append {stakeholder_id, role, voice: response} to session.stakeholder_voices.
    Also copy voice into the matching session.stakeholders.registry[] entry.
```

VERIFY: `session.stakeholder_voices.length >= len(session.stakeholders.primary)`.
  IF fewer (a primary stakeholder was skipped):
    AskUserQuestion: template=QT-1 (variant: 2-option)
      question_text: "You skipped voicing {N} primary stakeholder(s). Re-prompt for those?"
      header: "Re-prompt?"
    IF response == "Yes": loop over the skipped primary stakeholders with QT-5.

RECORD: Append the exchange to the Phase 02 checkpoint block; persist
`session.stakeholder_voices`. Voices feed Phase 09 (conflict-resolution) and the Phase 11
HTML document Stakeholder section.

```bash
devforgeai-validate phase-record ${BRAINSTORM_ID} --workflow=brainstorming --phase=02 --step=2.9 --project-root=. 2>&1
```

---

### Step 2.10: Context Window Check

EXECUTE:
```
IF estimated_context_usage > 70%:
  AskUserQuestion: template=QT-1
    question_text: "Context window is approximately {PERCENT}% full. Continue or save?"
    header: "Session"
    overrides:
      "Yes (Recommended)": { label: "Continue", description: "Proceed to Phase 03 (Problem & Current-State Analysis)" }
      "No":                { label: "Save and continue later", description: "Update checkpoint and exit" }
      remove: ["Skip / Defer"]
  IF response == "Save and continue later":
    Update the conversation checkpoint with all Phase 02 data
    Display: "Session saved. Resume with: /brainstorm --resume {BRAINSTORM_ID}"
    EXIT skill
ELSE:
  Display: "Context window healthy. Proceeding to Phase 03."
```

VERIFY: the context window check was performed.
IF skipped: HALT -- "Step 2.10: Context Window Check not performed."

RECORD: Persist `session.phases["02"].context_check_completed = true`.

```bash
devforgeai-validate phase-record ${BRAINSTORM_ID} --workflow=brainstorming --phase=02 --step=2.10 --project-root=. 2>&1
```

---

## Phase Exit Verification

Before transitioning to Phase 03, verify ALL exit criteria:

```
VERIFY_EXIT:
  CHECK: session.stakeholders.primary.length >= 1
    IF FAIL: HALT -- "Exit blocked: No primary stakeholder identified."
  CHECK: session.stakeholders.secondary.length >= 1
    IF FAIL: HALT -- "Exit blocked: No secondary stakeholder identified."
  CHECK: ALL primary stakeholders have goals (>= 1 each)
    IF FAIL: HALT -- "Exit blocked: Goals missing for primary stakeholder {name}."
  CHECK: ALL primary stakeholders have concerns (>= 1 each)
    IF FAIL: HALT -- "Exit blocked: Concerns missing for primary stakeholder {name}."
  CHECK: session.stakeholders.registry covers every stakeholder with influence + interest + raci
    IF FAIL: HALT -- "Exit blocked: Power/interest/RACI classification incomplete."
  CHECK: session.stakeholders.engagement_plan is a non-empty string
    IF FAIL: HALT -- "Exit blocked: Engagement plan not derived."
  CHECK: session.conflicts is not null (list OR "none detected")
    IF FAIL: HALT -- "Exit blocked: Conflict analysis not completed."
  CHECK: session.stakeholder_voices.length >= len(session.stakeholders.primary)
    IF FAIL: HALT -- "Exit blocked: Stakeholder voices incomplete."
  CHECK: session.phases["02"].context_check_completed == true
    IF FAIL: HALT -- "Exit blocked: Context window check not completed."
  CHECK: session.phases["02"].questions_answered >= 7
    IF FAIL: HALT -- "Exit blocked: Minimum 7 questions required, only {count} answered."
```

Update the conversation checkpoint on successful exit (per
`references/conversation-checkpoint-format.md`): set the Phase 02 block `completed: true`,
write its `phase_summary`, advance `current_phase` to `"03"`.

VERIFY: `tmp/{BRAINSTORM_ID}/checkpoint.json` shows the Phase 02 block `completed: true`.
IF write fails: HALT -- "Phase 02 exit checkpoint not saved."

---

## Exit Gate

```bash
devforgeai-validate phase-complete ${BRAINSTORM_ID} --workflow=brainstorming --phase=02 --checkpoint-passed --project-root=. 2>&1
```

| Exit Code | Action |
|-----------|--------|
| 0 | Phase 02 complete — proceed to next phase |
| 127 | CLI not installed — proceed without enforcement |
| Other | HALT — checkpoint/step validation failed |

---

## Phase Transition Display

Display: "Phase 02 Complete — Stakeholder Analysis. Primary={primary_count},
Secondary={secondary_count}, Tertiary={tertiary_count}, Conflicts={conflict_count}.
Proceeding to Phase 03 (Problem & Current-State Analysis)."

## Hook-backed OUT-Attestation

This phase has Phase-D dispatch entries in `subagent_out_attestation_registry.json`. When dispatching those named subagents, instruct them to return a `subagent-result-v1` result that includes `coverage_attestation` in the normal response. Phase completion is blocked by `subagent-out-attestation-gate.sh` when the hook-owned ledger line lacks `coverage_attestation_present:true`. This Phase-D path is OUT-attestation-only and does not require `tmp/<WORK_ID>/handoffs/`.
