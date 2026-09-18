# Phase 08: Requirements Definition

## Entry Gate

```bash
devforgeai-validate phase-check ${BRAINSTORM_ID} --workflow=brainstorming --from=07 --to=08 --project-root=. 2>&1
```

| Exit Code | Action |
|-----------|--------|
| 0 | Proceed to Phase 08 |
| 127 | CLI not installed — proceed without enforcement |
| Other | HALT — previous phase not complete |

---

## Contract

| Attribute | Value |
|-----------|-------|
| **PURPOSE** | Translate the analysed problem, opportunities, and constraints into formal requirements — functional requirements, non-functional requirements, a domain glossary, and an assumptions register |
| **REFERENCE** | `.claude/skills/spec-driven-brainstorming/references/conversation-checkpoint-format.md` |
| **STEP COUNT** | 5 mandatory steps |
| **MINIMUM QUESTIONS** | 4 |
| **GOVERNING ADR** | ADR-065 |

NEW phase in the 11-phase Business Analysis workflow. It replaces the former Phase 05
(Hypothesis Formation) — the hypothesis and critical-assumption work folds into the
**Assumptions Register** (Step 8.4) here. This phase turns the discovery of Phases 02–07
into requirements a downstream build can act on: each functional requirement carries an
`FR-NNN` id, each non-functional requirement an `NFR-NNN` id.

## Phase Exit Criteria

Field names listed are the canonical RECORD targets — each maps to the `requirements`
section of the data island (`references/brainstorm.schema.json` v2.0).

- [ ] At least 1 functional requirement captured → `session.requirements.functional` (length ≥ 1)
- [ ] Every functional requirement has a priority → each `functional[]` entry has `priority` (Must/Should/Could/Won't)
- [ ] At least 1 non-functional requirement captured → `session.requirements.nfrs` (length ≥ 1)
- [ ] Domain glossary captured → `session.requirements.glossary` (may be empty — warn-only)
- [ ] Assumptions register populated → `session.requirements.assumptions` (length ≥ 1)
- [ ] Conversation checkpoint updated with Phase 08 exchanges
- [ ] Context window check completed → `session.phases["08"].context_check_completed`

**IF any blocking criterion is unmet: HALT. Do NOT proceed to Phase 09.**

---

## Reference Loading

```
Read(file_path=".claude/skills/spec-driven-brainstorming/references/conversation-checkpoint-format.md")
Read(file_path=".claude/skills/spec-driven-brainstorming/references/user-interaction-patterns.md")
Read(file_path=".claude/skills/spec-driven-brainstorming/references/question-templates.md")
```

IF any Read fails: HALT -- "Phase 08 reference files not loaded. Cannot proceed without reference material."

---

## Mandatory Steps

### Step 8.1: Functional Requirements

Compile candidate functional requirements from earlier phases, let the user refine and
extend the set, then assign each a stable id. Functional-requirement ids follow the
pattern `FR-NNN` (`FR-001`, `FR-002`, …).

EXECUTE:
```
Compile candidate functional requirements:
  - From Phase 04 session.opportunity.opportunities → one candidate FR per opportunity
  - From Phase 04 session.opportunity.to_be_process_sketch → one candidate FR per
    actor+action step (the system must enable that step)
  - From Phase 04 session.opportunity.combined_opportunities → one candidate FR each

Display the candidate functional requirements as a numbered list.

AskUserQuestion: template=QT-5 (intent: list)
  question_text: "Here are the functional requirements I derived from our discussion.
                  What should be added, merged, or removed? (Choose 'Done — the set is
                  complete' to finish.)"
  header: "Functional Reqs"

Loop:
  IF user selects "Done — the set is complete": BREAK
  Capture the user's add / merge / remove instruction and apply it.

Finalise the set. Assign each a sequential id FR-001, FR-002, … and append to
session.requirements.functional with {id, statement, source}.
  - source = "opportunity:{OPP-id}" | "to_be_process" | "combined_opportunity" | "user_added"
```

Per-requirement priority (always):
```
FOR each fr in session.requirements.functional:
  AskUserQuestion: template=QT-2
    question_text: "How would you prioritise '{fr.statement}'?"
    header: "Priority"
    scale_type: moscow
  fr.priority = response   # one of Must / Should / Could / Won't
```

Acceptance notes (optional, single pass):
```
AskUserQuestion:
  questions:
    - question: "Would you like to add a one-line acceptance note to any requirement
                 (a quick test of 'done')?"
      header: "Accept Notes"
      multiSelect: false
      options:
        - label: "Yes — let me add notes"
          description: "Add acceptance notes to selected requirements"
        - label: "No — skip"
          description: "Leave acceptance notes empty"

IF response == "Yes — let me add notes":
  FOR each fr the user selects:
    Capture a one-line acceptance note into fr.acceptance_note.
```

VERIFY: `session.requirements.functional` has length ≥ 1; every entry has a non-empty
`statement` and a `priority` in {Must, Should, Could, Won't}.
IF empty: HALT -- "Step 8.1: At least one functional requirement must be captured."
IF any entry lacks a priority: HALT -- "Step 8.1: Every functional requirement needs a priority."

RECORD: Append the exchanges to the Phase 08 checkpoint block; persist
`session.requirements.functional`.

```bash
devforgeai-validate phase-record ${BRAINSTORM_ID} --workflow=brainstorming --phase=08 --step=8.1 --project-root=. 2>&1
```

---

### Step 8.2: Non-Functional Requirements

Non-functional-requirement ids follow the pattern `NFR-NNN`. Each NFR has a `category`
from the schema enum (performance, scalability, availability, security, usability,
maintainability, compliance, other).

EXECUTE:
```
AskUserQuestion:
  questions:
    - question: "Which quality attributes (non-functional requirements) matter for this
                 solution?"
      header: "NFR Categories"
      multiSelect: true
      options:
        - label: "Performance"
          description: "Speed, response time, throughput"
        - label: "Scalability"
          description: "Handling growth in load or data"
        - label: "Availability"
          description: "Uptime, reliability, recovery"
        - label: "Security"
          description: "Access control, data protection, auditing"
        - label: "Usability"
          description: "Ease of use, accessibility"
        - label: "Maintainability"
          description: "Ease of change, supportability"
        - label: "Compliance"
          description: "Regulatory or contractual standards"

selected_categories = response  (at least one expected)
```

For each selected category:
```
FOR each category in selected_categories:
  AskUserQuestion: template=QT-5 (intent: describe)
    question_text: "State the {category} requirement — and if you can, a measurable
                    target (e.g. 'page loads under 2s', '99.9% uptime')."
    header: "{category}"

  Parse the response into statement and (if present) a measurable metric.
  Assign the next sequential id NFR-001, NFR-002, … and append to
  session.requirements.nfrs with {id, category (lowercased), statement, metric,
  source: "phase-08"}.
```

VERIFY: `session.requirements.nfrs` has length ≥ 1; every entry has a `category` from the
schema enum and a non-empty `statement`.
IF empty: HALT -- "Step 8.2: At least one non-functional requirement must be captured — every software initiative carries quality constraints."

RECORD: Append the exchanges to the Phase 08 checkpoint block; persist
`session.requirements.nfrs`.

```bash
devforgeai-validate phase-record ${BRAINSTORM_ID} --workflow=brainstorming --phase=08 --step=8.2 --project-root=. 2>&1
```

---

### Step 8.3: Domain Glossary

Capture the project-specific terms that a reader of the final document would need
defined. This is the standard glossary the skill previously left optional.

EXECUTE:
```
Initialize: session.requirements.glossary = []

Propose candidate terms — scan the problem statement, opportunities, and requirements for
domain-specific nouns or acronyms — and display them as a list.

AskUserQuestion: template=QT-5 (intent: list)
  question_text: "Which domain terms or acronyms should the glossary define? (Choose
                  'Done — no more terms' to finish.)"
  header: "Glossary Terms"

Loop:
  IF user selects "Done — no more terms": BREAK
  term = the user's term

  AskUserQuestion: template=QT-5 (intent: describe)
    question_text: "Define '{term}' in one sentence."
    header: "Definition"
  definition = response

  Append {term: term, definition: definition} to session.requirements.glossary.
```

VERIFY: `session.requirements.glossary` is a list (may be empty).
  IF `len(session.requirements.glossary) == 0`:
    Display: "No glossary terms captured. Continuing — the glossary section will be
    omitted from the final document."
  (No HALT — warn-only check.)

RECORD: Append the exchange to the Phase 08 checkpoint block; persist
`session.requirements.glossary`.

```bash
devforgeai-validate phase-record ${BRAINSTORM_ID} --workflow=brainstorming --phase=08 --step=8.3 --project-root=. 2>&1
```

---

### Step 8.4: Assumptions Register

Surface the implicit assumptions the analysis has been resting on, so they can be
recorded and challenged later. Do NOT auto-classify — present candidates and let the
user decide what is recorded.

EXECUTE:
```
Scan earlier phases for candidate assumptions and present them as a plain bulleted list
(no inference labels, no auto-priority):
  - claims in session.problem_statement made without cited evidence
  - root causes in session.problem_analysis.root_causes stated as fact
  - the belief that the top opportunities will actually solve the problem
  - any constraint the user described as flexible / negotiable

Display the candidate list.

AskUserQuestion:
  questions:
    - question: "Which of these should be recorded as assumptions in the analysis?"
      header: "Assumptions"
      multiSelect: true
      options:
        # Options generated dynamically from the candidate list
        - label: "{candidate_1}"
          description: "Surfaced from: {origin phase}"
        - label: "{candidate_2}"
          description: "Surfaced from: {origin phase}"
        ...

Capture the selected candidates into session.requirements.assumptions (as strings).

AskUserQuestion: template=QT-5 (intent: list)
  question_text: "Any other assumptions to add that I didn't surface? (Choose 'Done — no
                  more' to finish.)"
  header: "More Assumptions"

Loop:
  IF user selects "Done — no more": BREAK
  Append the user's assumption text to session.requirements.assumptions.
```

VERIFY: `session.requirements.assumptions` has length ≥ 1.
IF empty: HALT -- "Step 8.4: At least one assumption must be recorded — re-prompt; every analysis rests on assumptions."

RECORD: Append the exchanges to the Phase 08 checkpoint block; persist
`session.requirements.assumptions`. Phase 11 surfaces the critical subset into the
`handoff.critical_assumptions` field.

```bash
devforgeai-validate phase-record ${BRAINSTORM_ID} --workflow=brainstorming --phase=08 --step=8.4 --project-root=. 2>&1
```

---

### Step 8.5: Context Window Check

EXECUTE:
```
IF estimated_context_usage > 70%:
  AskUserQuestion: template=QT-1
    question_text: "Context window is approximately {PERCENT}% full. Continue or save?"
    header: "Session"
    overrides:
      "Yes (Recommended)": { label: "Continue", description: "Proceed to Phase 09 (Prioritization & Roadmap)" }
      "No":                { label: "Save and continue later", description: "Update checkpoint and exit" }
      remove: ["Skip / Defer"]

  IF response == "Save and continue later":
    Update the conversation checkpoint with all Phase 08 data
    Display: "Session saved. Resume with: /brainstorm --resume {BRAINSTORM_ID}"
    EXIT skill
ELSE:
  Display: "Context window healthy. Proceeding to Phase 09."
```

VERIFY: the context window check was performed.
IF skipped: HALT -- "Step 8.5: Context Window Check not performed."

RECORD: Persist `session.phases["08"].context_check_completed = true`.

```bash
devforgeai-validate phase-record ${BRAINSTORM_ID} --workflow=brainstorming --phase=08 --step=8.5 --project-root=. 2>&1
```

---

## Phase Exit Verification

Before transitioning to Phase 09, verify ALL exit criteria:

```
VERIFY_EXIT:
  CHECK: session.requirements.functional.length >= 1
    IF FAIL: HALT -- "Exit blocked: No functional requirements captured."
  CHECK: every functional[] entry has a priority in {Must, Should, Could, Won't}
    IF FAIL: HALT -- "Exit blocked: One or more functional requirements lack a priority."
  CHECK: session.requirements.nfrs.length >= 1
    IF FAIL: HALT -- "Exit blocked: No non-functional requirements captured."
  CHECK: session.requirements.glossary is a list (may be empty — warn-only)
    IF FAIL: HALT -- "Exit blocked: Glossary field not initialised."
  CHECK: session.requirements.assumptions.length >= 1
    IF FAIL: HALT -- "Exit blocked: Assumptions register is empty."
  CHECK: session.phases["08"].context_check_completed == true
    IF FAIL: HALT -- "Exit blocked: Context window check not completed."
  CHECK: session.phases["08"].questions_answered >= 4
    IF FAIL: HALT -- "Exit blocked: Minimum 4 questions required, only {count} answered."
```

Update the conversation checkpoint on successful exit (per
`references/conversation-checkpoint-format.md`): set the Phase 08 block `completed: true`,
write its `phase_summary`, advance `current_phase` to `"09"`.

VERIFY: `tmp/{BRAINSTORM_ID}/checkpoint.json` shows the Phase 08 block `completed: true`.
IF write fails: HALT -- "Phase 08 exit checkpoint not saved."

---

## Exit Gate

```bash
devforgeai-validate phase-complete ${BRAINSTORM_ID} --workflow=brainstorming --phase=08 --checkpoint-passed --project-root=. 2>&1
```

| Exit Code | Action |
|-----------|--------|
| 0 | Phase 08 complete — proceed to next phase |
| 127 | CLI not installed — proceed without enforcement |
| Other | HALT — checkpoint/step validation failed |

---

## Phase Transition Display

Display: "Phase 08 Complete — Requirements Definition. Functional requirements: {count}.
Non-functional requirements: {count}. Glossary terms: {count}. Assumptions recorded:
{count}. Proceeding to Phase 09 (Prioritization & Roadmap)."
