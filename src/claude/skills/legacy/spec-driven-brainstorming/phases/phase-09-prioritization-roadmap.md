# Phase 09: Prioritization & Roadmap

## Entry Gate

```bash
devforgeai-validate phase-check ${BRAINSTORM_ID} --workflow=brainstorming --from=08 --to=09 --project-root=. 2>&1
```

| Exit Code | Action |
|-----------|--------|
| 0 | Proceed to Phase 09 |
| 127 | CLI not installed — proceed without enforcement |
| Other | HALT — previous phase not complete |

---

## Contract

| Attribute | Value |
|-----------|-------|
| **PURPOSE** | Rank the capabilities and opportunities with MoSCoW and impact-effort analysis, sequence them, capture deferred ideas in a durable register, and lay out a phased release roadmap |
| **REFERENCE** | `.claude/skills/spec-driven-brainstorming/references/prioritization-workflow.md` |
| **STEP COUNT** | 7 mandatory steps |
| **MINIMUM QUESTIONS** | 4 |
| **GOVERNING ADR** | ADR-065 |

Renumbered from the former Phase 06 (Prioritization) and expanded with a **Deferred Ideas
Register** (Step 9.5) and a **Phased Release Roadmap** (Step 9.6). MoSCoW here operates on
the capability / opportunity set — distinct from the per-requirement `priority` already
assigned in Phase 08; the two are complementary schema views, not duplicates. The Deferred
Ideas Register is the structural fix for the ADR-065 render-leak defect: ideas raised but
not built are recorded with stable `DEF-NNN` ids instead of being lost at synthesis.

## Phase Exit Criteria

Field names listed are the canonical RECORD targets — each maps to the `prioritization`
section of the data island (`references/brainstorm.schema.json` v2.0).

- [ ] All items MoSCoW-classified → `session.prioritization.{must_have_capabilities, should_have, could_have, wont_have}`
- [ ] At least 1 Must Have identified → `session.prioritization.must_have_capabilities` (length ≥ 1, or explicit user override)
- [ ] Impact-effort assessed for Must/Should items → `session.prioritization.impact_effort`
- [ ] Recommended sequence generated and user-validated → `session.prioritization.recommended_sequence` (length ≥ 1)
- [ ] Deferred Ideas Register populated → `session.prioritization.deferred_ideas` (may be empty — warn-only)
- [ ] Phased release roadmap generated → `session.prioritization.release_roadmap` (length ≥ 1)
- [ ] Conversation checkpoint updated with Phase 09 exchanges
- [ ] Context window check completed → `session.phases["09"].context_check_completed`

**IF any blocking criterion is unmet: HALT. Do NOT proceed to Phase 10.**

---

## Reference Loading

```
Read(file_path=".claude/skills/spec-driven-brainstorming/references/prioritization-workflow.md")
Read(file_path=".claude/skills/spec-driven-brainstorming/references/question-templates.md")
Read(file_path=".claude/skills/spec-driven-brainstorming/references/conversation-checkpoint-format.md")
```

IF any Read fails: HALT -- "Phase 09 reference files not loaded. Cannot proceed without reference material."

---

## Mandatory Steps

### Step 9.1: Compile Items for Prioritization

EXECUTE:
```
items_to_prioritize = []

# Opportunities from Phase 04
FOR each opportunity in session.opportunity.opportunities:
  items_to_prioritize.append({id: "OPP-{index}", description: opportunity.description,
                              source: opportunity.source, type: "opportunity"})

# Combined opportunities from Phase 04
FOR each combined in session.opportunity.combined_opportunities:
  items_to_prioritize.append({id: "COMB-{index}", description: combined.description,
                              source: "combined", type: "combined"})

# Adjacent opportunities from Phase 04
FOR each adjacent in session.opportunity.adjacent_opportunities:
  items_to_prioritize.append({id: "ADJ-{index}", description: adjacent.problem,
                              source: "adjacent", type: "adjacent"})

session.prioritization_items = items_to_prioritize

# Pre-populate Won't Have from the Phase 07 out-of-scope anti-features.
# wont_have[] is a string array per schema; attribution is kept in a parallel structure.
Initialize: session.prioritization.wont_have_provenance = []
FOR each oos in session.constraints_scope.out_of_scope:
  Append oos.item to a pending wont_have set.
  Append {item: oos.item, rationale: oos.rationale,
          source: "out_of_scope_pregeneration"} to session.prioritization.wont_have_provenance.

Display:
  "We have {len(items)} items to prioritize, plus {len(out_of_scope)} items already
  marked out-of-scope in Phase 07 (these pre-populate Won't Have). Let's classify each
  open item."
```

VERIFY: `session.prioritization_items` length ≥ 1; each item has id, description, source, type.
IF empty: HALT -- "Step 9.1: No items to prioritize — Phase 04 should have produced at least one opportunity."

RECORD: Append the exchange to the Phase 09 checkpoint block; persist
`session.prioritization_items` and `session.prioritization.wont_have_provenance`.

```bash
devforgeai-validate phase-record ${BRAINSTORM_ID} --workflow=brainstorming --phase=09 --step=9.1 --project-root=. 2>&1
```

---

### Step 9.2: MoSCoW Classification

EXECUTE:
```
FOR each item in session.prioritization_items:
  AskUserQuestion: template=QT-2
    question_text: "How would you classify '{item.description}'?"
    header: "Priority"
    scale_type: moscow
  item.moscow = response

# Build the schema string arrays (descriptions only — wont_have is string-typed).
session.prioritization.must_have_capabilities = [item.description WHERE moscow == "Must Have"]
session.prioritization.should_have           = [item.description WHERE moscow == "Should Have"]
session.prioritization.could_have            = [item.description WHERE moscow == "Could Have"]
session.prioritization.wont_have             = [item.description WHERE moscow == "Won't Have (this time)"]
                                               + the pending wont_have set from Step 9.1

# Validation: 0 Must Haves
IF len(must_have_capabilities) == 0:
  AskUserQuestion: template=QT-1
    question_text: "No Must Haves identified. Is there truly nothing absolutely required?"
    header: "Confirm"
    overrides:
      "Yes (Recommended)": { label: "Correct - all flexible", description: "Everything is negotiable" }
      "No":                { label: "Let me reconsider",      description: "I'll upgrade some items" }
      remove: ["Skip / Defer"]
  IF response == "Let me reconsider": Re-present items for reclassification.

# Validation: 5+ Must Haves
IF len(must_have_capabilities) > 5:
  AskUserQuestion: template=QT-1
    question_text: "Many Must Haves identified — this may exceed constraints. Reduce to the most critical?"
    header: "Reduce"
    overrides:
      "Yes (Recommended)": { label: "Yes, let me reconsider", description: "I'll downgrade some items" }
      "No":                { label: "All are truly critical", description: "Keep as is" }
      remove: ["Skip / Defer"]
  IF response == "Yes, let me reconsider": Re-present Must Have items for reclassification.
```

VERIFY: every item has a `moscow` classification; at least 1 Must Have (or explicit user override).

RECORD: Append the exchanges to the Phase 09 checkpoint block; persist
`session.prioritization.{must_have_capabilities, should_have, could_have, wont_have}`.

```bash
devforgeai-validate phase-record ${BRAINSTORM_ID} --workflow=brainstorming --phase=09 --step=9.2 --project-root=. 2>&1
```

---

### Step 9.3: Impact-Effort Matrix

EXECUTE:
```
Display: "Now let's assess impact and effort for each Must Have and Should Have item, to
find the Quick Wins (high impact + low effort)."

FOR each item in [Must Have + Should Have items]:
  AskUserQuestion:
    questions:
      - question: "What is the expected impact of '{item.description}'?"
        header: "Impact"
        multiSelect: false
        options:
          - label: "High impact"
            description: "Significant business value"
          - label: "Medium impact"
            description: "Moderate business value"
          - label: "Low impact"
            description: "Minor business value"
      - question: "How much effort would '{item.description}' require?"
        header: "Effort"
        multiSelect: false
        options:
          - label: "Low effort"
            description: "Days to a week"
          - label: "Medium effort"
            description: "Weeks to a month"
          - label: "High effort"
            description: "Months of work"
  item.impact = impact answer
  item.effort = effort answer

session.prioritization.impact_effort = {
  quick_wins:     [items WHERE impact in ["High","Medium"] AND effort == "Low"],
  major_projects: [items WHERE impact in ["High","Medium"] AND effort == "High"],
  fill_ins:       [items WHERE impact == "Low" AND effort == "Low"],
  avoid:          [items WHERE impact == "Low" AND effort == "High"]
}
```

VERIFY: every Must/Should Have item has `impact` AND `effort`, categorized into exactly one quadrant.

RECORD: Append the exchanges to the Phase 09 checkpoint block; persist
`session.prioritization.impact_effort`. The matrix is rendered as an inline SVG in the
Phase 11 HTML document.

```bash
devforgeai-validate phase-record ${BRAINSTORM_ID} --workflow=brainstorming --phase=09 --step=9.3 --project-root=. 2>&1
```

---

### Step 9.4: Recommended Sequence

EXECUTE (Generate):
```
sequence = []
order = 1

# 1. Quick Wins that are Must Have      → "Do first"
# 2. Quick Wins that are Should Have    → "Do early"
# 3. Major Projects that are Must Have  → "Plan carefully"
# 4. Major Projects that are Should Have→ "If time allows"
# 5. Fill-ins                           → "When bandwidth available"
FOR each tier in the order above:
  FOR each item in that tier:
    sequence.append({order, item_description: item.description, rationale: tier label})
    order += 1

session.prioritization.recommended_sequence = sequence
Display the sequence; list Avoid-quadrant items separately as "defer or drop".
```

EXECUTE (Validate):
```
AskUserQuestion:
  questions:
    - question: "Does this sequence look right? Any adjustments needed?"
      header: "Validate"
      multiSelect: false
      options:
        - label: "Yes, looks good"
          description: "Proceed with this sequence"
        - label: "Adjust order"
          description: "Change the priority order"
        - label: "Add dependencies"
          description: "Some items depend on others"

IF response == "Adjust order":
  Capture which items to move; apply; re-display.
IF response == "Add dependencies":
  Capture dependencies (item X depends on item Y); re-sort respecting dependency order;
  persist session.prioritization.dependencies.
```

VERIFY: `session.prioritization.recommended_sequence` length ≥ 1; contains all Must/Should
Have items; the user validated the final sequence.

RECORD: Append the exchanges to the Phase 09 checkpoint block; persist the final
`session.prioritization.recommended_sequence` (and `dependencies` if captured).

```bash
devforgeai-validate phase-record ${BRAINSTORM_ID} --workflow=brainstorming --phase=09 --step=9.4 --project-root=. 2>&1
```

---

### Step 9.5: Deferred Ideas Register

Capture ideas raised during the session but intentionally NOT in the MVP, so they survive
into the final document instead of being lost. Deferred-idea ids follow the pattern
`DEF-NNN`. A deferred idea is "retained for later evaluation" — distinct from a Won't
Have (rejected for this initiative); the two are different schema concepts.

EXECUTE:
```
Initialize: session.prioritization.deferred_ideas = []

Compile candidate deferred ideas (do NOT seed from Won't Have — that set is rejected,
not deferred):
  - From Phase 01 session.ba_planning.vision_beyond_scope (larger vision outside session scope)
  - From Phase 04 session.opportunity.divergent_ideas not selected into an opportunity
  - From Phase 04 session.opportunity.combined_opportunities not carried into the sequence
  - From session.prioritization.could_have (Could Have items are natural defer candidates)

Display the candidate list with each candidate's origin phase.

AskUserQuestion:
  questions:
    - question: "Which of these ideas should be recorded in the Deferred Ideas Register —
                 retained for evaluation in a later release?"
      header: "Defer"
      multiSelect: true
      options:
        # Options generated dynamically from the candidate list
        - label: "{candidate_1}"
          description: "From: {origin phase}"
        - label: "{candidate_2}"
          description: "From: {origin phase}"
        ...

FOR each selected candidate:
  Assign the next sequential id DEF-001, DEF-002, …
  AskUserQuestion: template=QT-5 (intent: describe)
    question_text: "For '{candidate}': in one or two sentences — why is it deferred, and
                    what trigger or milestone should prompt revisiting it?"
    header: "Defer Detail"
  Parse the answer into why_deferred and revisit_when.

  Append to session.prioritization.deferred_ideas with:
    id: "DEF-NNN"
    description: candidate text
    why_deferred: parsed why
    business_value: ""           # optional — left blank unless the user volunteered it
    mvp_dependency: ""           # optional
    revisit_when: parsed trigger
    source_phase: origin phase
    status: "open"
```

VERIFY: `session.prioritization.deferred_ideas` is a list; every entry has `id`,
`description`, and `status` (the schema-required fields).
  IF `len(session.prioritization.deferred_ideas) == 0`:
    Display: "No deferred ideas recorded. Continuing — the Deferred Ideas Register will
    be empty in the final document."
  (No HALT — warn-only check.)

RECORD: Append the exchanges to the Phase 09 checkpoint block; persist
`session.prioritization.deferred_ideas`. The register is rendered as a structured table
in the Phase 11 HTML document and mirrored into the JSON data island as `deferred_ideas[]`.

```bash
devforgeai-validate phase-record ${BRAINSTORM_ID} --workflow=brainstorming --phase=09 --step=9.5 --project-root=. 2>&1
```

---

### Step 9.6: Phased Release Roadmap

EXECUTE:
```
Propose a phased grouping of the recommended sequence:
  - Release 1 (MVP): the Must Have items, Quick Wins first
  - Release 2: Should Have items and Major Projects
  - Future / backlog: Could Have items and the Deferred Ideas Register

Display the proposed roadmap.

AskUserQuestion:
  questions:
    - question: "Does this phased release roadmap look right?"
      header: "Roadmap"
      multiSelect: false
      options:
        - label: "Yes, looks good"
          description: "Proceed with this roadmap"
        - label: "Adjust the phasing"
          description: "Move items between releases"

IF response == "Adjust the phasing":
  Capture which items move to which release; apply.

session.prioritization.release_roadmap = [
  {release: "Release 1 (MVP)", goal: "...", items: [descriptions]},
  {release: "Release 2",       goal: "...", items: [descriptions]},
  {release: "Future / backlog",goal: "...", items: [descriptions]}
]
```

VERIFY: `session.prioritization.release_roadmap` length ≥ 1; every release entry has a
`release` label and an `items` list.
IF empty: HALT -- "Step 9.6: Release roadmap not generated."

RECORD: Append the exchange to the Phase 09 checkpoint block; persist
`session.prioritization.release_roadmap`.

```bash
devforgeai-validate phase-record ${BRAINSTORM_ID} --workflow=brainstorming --phase=09 --step=9.6 --project-root=. 2>&1
```

---

### Step 9.7: Context Window Check

EXECUTE:
```
IF estimated_context_usage > 70%:
  AskUserQuestion: template=QT-1
    question_text: "Context window is approximately {PERCENT}% full. Continue or save?"
    header: "Session"
    overrides:
      "Yes (Recommended)": { label: "Continue", description: "Proceed to Phase 10 (Change & Transition Strategy)" }
      "No":                { label: "Save and continue later", description: "Update checkpoint and exit" }
      remove: ["Skip / Defer"]

  IF response == "Save and continue later":
    Update the conversation checkpoint with all Phase 09 data
    Display: "Session saved. Resume with: /brainstorm --resume {BRAINSTORM_ID}"
    EXIT skill
ELSE:
  Display: "Context window healthy. Proceeding to Phase 10."
```

VERIFY: the context window check was performed.
IF skipped: HALT -- "Step 9.7: Context Window Check not performed."

RECORD: Persist `session.phases["09"].context_check_completed = true`.

```bash
devforgeai-validate phase-record ${BRAINSTORM_ID} --workflow=brainstorming --phase=09 --step=9.7 --project-root=. 2>&1
```

---

## Phase Exit Verification

Before transitioning to Phase 10, verify ALL exit criteria:

```
VERIFY_EXIT:
  CHECK: every prioritization item has a MoSCoW classification
    IF FAIL: HALT -- "Exit blocked: One or more items not MoSCoW-classified."
  CHECK: session.prioritization.must_have_capabilities.length >= 1 OR explicit user override
    IF FAIL: HALT -- "Exit blocked: No Must Have identified and no user override."
  CHECK: session.prioritization.impact_effort is populated
    IF FAIL: HALT -- "Exit blocked: Impact-effort matrix not assessed."
  CHECK: session.prioritization.recommended_sequence.length >= 1
    IF FAIL: HALT -- "Exit blocked: No recommended sequence generated."
  CHECK: session.prioritization.deferred_ideas is a list (may be empty — warn-only)
    IF FAIL: HALT -- "Exit blocked: Deferred Ideas Register not initialised."
  CHECK: session.prioritization.release_roadmap.length >= 1
    IF FAIL: HALT -- "Exit blocked: No release roadmap generated."
  CHECK: session.phases["09"].context_check_completed == true
    IF FAIL: HALT -- "Exit blocked: Context window check not completed."
  CHECK: session.phases["09"].questions_answered >= 4
    IF FAIL: HALT -- "Exit blocked: Minimum 4 questions required, only {count} answered."
```

Update the conversation checkpoint on successful exit (per
`references/conversation-checkpoint-format.md`): set the Phase 09 block `completed: true`,
write its `phase_summary`, advance `current_phase` to `"10"`.

VERIFY: `tmp/{BRAINSTORM_ID}/checkpoint.json` shows the Phase 09 block `completed: true`.
IF write fails: HALT -- "Phase 09 exit checkpoint not saved."

---

## Exit Gate

```bash
devforgeai-validate phase-complete ${BRAINSTORM_ID} --workflow=brainstorming --phase=09 --checkpoint-passed --project-root=. 2>&1
```

| Exit Code | Action |
|-----------|--------|
| 0 | Phase 09 complete — proceed to next phase |
| 127 | CLI not installed — proceed without enforcement |
| Other | HALT — checkpoint/step validation failed |

---

## Phase Transition Display

Display: "Phase 09 Complete — Prioritization & Roadmap. Must Have: {count}, Should Have:
{count}, Could Have: {count}, Won't Have: {count}. Deferred ideas registered: {count}.
Releases planned: {count}. Proceeding to Phase 10 (Change & Transition Strategy)."
