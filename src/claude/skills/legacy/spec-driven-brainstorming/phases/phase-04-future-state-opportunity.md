# Phase 04: Future-State & Opportunity Mapping

## Entry Gate

```bash
devforgeai-validate phase-check ${BRAINSTORM_ID} --workflow=brainstorming --from=03 --to=04 --project-root=. 2>&1
```

| Exit Code | Action |
|-----------|--------|
| 0 | Proceed to Phase 04 |
| 127 | CLI not installed — proceed without enforcement |
| Other | HALT — previous phase not complete |

---

## Contract

| Attribute | Value |
|-----------|-------|
| **PURPOSE** | Explore WHAT COULD BE — the future state — through blue-sky thinking, market research, and solution ideation |
| **REFERENCE** | `.claude/skills/spec-driven-brainstorming/references/opportunity-mapping-workflow.md` |
| **STEP COUNT** | 10 mandatory steps |
| **MINIMUM QUESTIONS** | 4 |
| **GOVERNING ADR** | ADR-065 |

Renumbered from the former Phase 03. The market-research opt-in decision was made in
Phase 01 (`session.research_enabled`) and is not re-asked here. A **To-Be Process Sketch**
step is added to complement the As-Is Process Model captured in Phase 03.

## Phase Exit Criteria

Field names listed are the canonical RECORD targets — each maps to the `opportunity`
section of the data island (`references/brainstorm.schema.json` v2.0).

- [ ] Ideal state described → `session.opportunity.ideal_state` (non-empty)
- [ ] Future-state target outcome described → `session.opportunity.target_outcome` (non-empty)
- [ ] Success metrics identified → `session.success_vision.metrics` (length ≥ 1)
- [ ] To-be process sketch captured → `session.opportunity.to_be_process_sketch`
- [ ] Rapid Ideation captured → `session.opportunity.divergent_ideas` (≥ 5 recommended)
- [ ] At least 1 opportunity compiled → `session.opportunity.opportunities` (length ≥ 1)
- [ ] Adjacent opportunities explored → `session.opportunity.adjacent_opportunities` (may be empty)
- [ ] Idea combinations explored → `session.opportunity.combined_opportunities` (may be empty)
- [ ] Conversation checkpoint updated with Phase 04 exchanges
- [ ] Context window check completed → `session.phases["04"].context_check_completed`

**IF any criterion is unmet: HALT. Do NOT proceed to Phase 05.**

---

## Reference Loading

```
Read(file_path=".claude/skills/spec-driven-brainstorming/references/opportunity-mapping-workflow.md")
Read(file_path=".claude/skills/spec-driven-brainstorming/references/question-templates.md")
Read(file_path=".claude/skills/spec-driven-brainstorming/references/conversation-checkpoint-format.md")
```

IF any Read fails: HALT -- "Phase 04 reference files not loaded."

---

## Mandatory Steps

### Step 4.1: Conduct Market Research [CONDITIONAL]

**Condition:** Only execute if `session.research_enabled == true` (set in Phase 01).
IF `session.research_enabled == false`: Display "Market research skipped per Phase 01."
and SKIP to Step 4.2.

EXECUTE:
```
Display: "Researching market solutions and competitor approaches..."
```

Build the registry-protected Phase 04 handoff for `internet-sleuth`. This
dispatch returns market-research findings and does not mutate repo files, so the
handoff is floor-only.

```bash
mkdir -p tmp/${BRAINSTORM_ID}
: > tmp/${BRAINSTORM_ID}/brainstorm-phase04-internet-sleuth-handoff-changed-files.txt

HANDOFF_OUTPUT_INTERNET_SLEUTH=$(devforgeai-validate build-subagent-handoff ${BRAINSTORM_ID} \
  --workflow=spec-driven-brainstorming \
  --phase=04 \
  --subagent=internet-sleuth \
  --changed-files-file=tmp/${BRAINSTORM_ID}/brainstorm-phase04-internet-sleuth-handoff-changed-files.txt \
  --project-root=. 2>&1)
HANDOFF_PATH_INTERNET_SLEUTH=$(echo "$HANDOFF_OUTPUT_INTERNET_SLEUTH" | jq -r '.handoff_md_path')
```

VERIFY before dispatch:
- `HANDOFF_PATH_INTERNET_SLEUTH` exists and is non-empty.
- `tmp/${BRAINSTORM_ID}/handoffs/phase-04-internet-sleuth-handoff.manifest.json` exists.
- The manifest has `context_pack.coverage_matrix == {}` and `unresolved == []`.

```
Task(
  subagent_type="internet-sleuth",
  prompt="Handoff: ${HANDOFF_PATH_INTERNET_SLEUTH}
          Read the handoff first. Use its context_pack.coverage_matrix and role-domain rules as the context source. If a required domain or artifact is absent, return H-CONTEXT-MISS and stop.

          Research market trends and competitor approaches for:
          Problem: {session.problem_statement}
          Find: competitors, available solutions, market trends, case studies.
          Return structured findings.
          Include a subagent-result-v1 coverage_attestation with context_pack_path='${HANDOFF_PATH_INTERNET_SLEUTH}', context_pack_consumed=true, and context_miss=[]."
)
```

Graceful degradation:
```
IF task_result is null (timeout/failure):
  Display: "Research unavailable. Continuing with internal knowledge."
  session.market_research = null
ELSE:
  session.market_research = task_result
```

VERIFY: Either `session.market_research` is populated OR the failure was logged and
`session.market_research` set to null.

RECORD: Append the exchange to the Phase 04 checkpoint block; persist
`session.market_research`; record the subagent invocation.

```bash
devforgeai-validate phase-record ${BRAINSTORM_ID} --workflow=brainstorming --phase=04 --step=4.1 --project-root=. 2>&1
```

---

### Step 4.2: Blue-Sky Visioning

EXECUTE:
```
AskUserQuestion: template=QT-5
  question_text: "If you had unlimited resources, what would the ideal solution look like?"
  header: "Ideal State"
  intent: describe
```

Follow-up path (if user selected "Help me brainstorm"):
```
IF response == "Help me brainstorm":
  AskUserQuestion:
    questions:
      - question: "In an ideal world, how fast would this process be?"
        header: "Ideal Speed"
        multiSelect: false
        options:
          - label: "Instant"
            description: "Happens immediately"
          - label: "Minutes"
            description: "Done in a few minutes"
          - label: "Same day"
            description: "Completed within hours"
  AskUserQuestion:
    questions:
      - question: "In an ideal world, who would do this work?"
        header: "Ideal Actor"
        multiSelect: false
        options:
          - label: "Fully automated"
            description: "No human intervention"
          - label: "Minimal human oversight"
            description: "Humans review exceptions"
          - label: "Assisted by technology"
            description: "Humans do it faster with help"
  Synthesize user's speed + actor answers into session.opportunity.ideal_state.
ELSE IF response == "Let me describe":
  Capture free-form description.
  session.opportunity.ideal_state = description
```

VERIFY: `session.opportunity.ideal_state` is non-empty.

RECORD: Append the exchange to the Phase 04 checkpoint block; persist
`session.opportunity.ideal_state`.

```bash
devforgeai-validate phase-record ${BRAINSTORM_ID} --workflow=brainstorming --phase=04 --step=4.2 --project-root=. 2>&1
```

---

### Step 4.3: Rapid Ideation (Divergent Mode)

**Methodology reference:** `references/brainstorming-techniques.md` § 1 (Divergent /
Convergent Separation). Loads on first execution of this step.

EXECUTE:

Display:
"Rapid Ideation mode. Quantity over quality. Feasibility doesn't matter yet — list ideas
freely. We'll narrow later. Aim for 5 or more."

```
Initialize: session.opportunity.divergent_ideas = []
Initialize: N = 1

Loop:
  AskUserQuestion: template=QT-5 (intent: list)
    question_text: "Idea {N}: what's another way to address the problem? (Choose
                    'Done — no more to add' to finish.)"
    header: "Idea {N}"
  IF user selects "Done — no more to add": BREAK
  Append the user's description to session.opportunity.divergent_ideas.
  N += 1
```

VERIFY: `session.opportunity.divergent_ideas` is a list.
  IF `len(session.opportunity.divergent_ideas) < 5`:
    Display: "Note: {count} idea(s) captured. Methodology recommends 5+ for a true
    divergent set. Continuing — you can revisit during compilation."
  (No HALT — warn-only check.)

RECORD: Append the exchange to the Phase 04 checkpoint block; persist
`session.opportunity.divergent_ideas`.

```bash
devforgeai-validate phase-record ${BRAINSTORM_ID} --workflow=brainstorming --phase=04 --step=4.3 --project-root=. 2>&1
```

---

### Step 4.4: Success Vision

EXECUTE (Part A — Vision):
```
AskUserQuestion: template=QT-5
  question_text: "What would change in your organization if this problem was completely solved?"
  header: "Vision"
  intent: describe
```
Capture description in `session.success_vision.description` and copy it into
`session.opportunity.target_outcome` (the desired future state).

EXECUTE (Part B — Metrics):
```
AskUserQuestion: template=QT-4
  question_text: "How would you measure success for this initiative?"
  header: "Success Metrics"
  category: success_metrics
```
Capture selections in `session.success_vision.metrics`.

VERIFY: `session.opportunity.target_outcome` is non-empty AND
`session.success_vision.metrics.length >= 1`.

RECORD: Append the exchange to the Phase 04 checkpoint block; persist
`session.success_vision` and `session.opportunity.target_outcome`.

```bash
devforgeai-validate phase-record ${BRAINSTORM_ID} --workflow=brainstorming --phase=04 --step=4.4 --project-root=. 2>&1
```

---

### Step 4.5: To-Be Process Sketch

Sketch how the process SHOULD flow in the future state — the to-be counterpart of the
Phase 03 As-Is Process Model. A textual step sequence is sufficient; the contrast
between as-is and to-be is what later phases (Requirements, Change Strategy) build on.

EXECUTE:
```
Display the As-Is Process Model from Phase 03 for reference.

AskUserQuestion: template=QT-5 (intent: list)
  question_text: "Sketch the future process step by step — for each step name the actor
                  and what they do, the way it SHOULD work once the problem is solved."
  header: "To-Be Flow"

session.opportunity.to_be_process_sketch = { steps: [ordered actor+action entries] }
```

VERIFY: `session.opportunity.to_be_process_sketch` is populated.

RECORD: Append the exchange to the Phase 04 checkpoint block; persist
`session.opportunity.to_be_process_sketch`.

```bash
devforgeai-validate phase-record ${BRAINSTORM_ID} --workflow=brainstorming --phase=04 --step=4.5 --project-root=. 2>&1
```

---

### Step 4.6: Technology Opportunities

EXECUTE:
```
AskUserQuestion:
  questions:
    - question: "Are there any technologies you've heard about that might help?"
      header: "Tech Ideas"
      multiSelect: true
      options:
        - label: "AI/ML automation"
          description: "Artificial intelligence solutions"
        - label: "Process automation (RPA)"
          description: "Robotic process automation"
        - label: "Cloud migration"
          description: "Moving to cloud infrastructure"
        - label: "Integration/APIs"
          description: "Connecting existing systems"
        - label: "Mobile/Web apps"
          description: "New user interfaces"
        - label: "Data analytics"
          description: "Better insights and reporting"
```

Capture selections in `session.technology_ideas` (may be empty array).

Follow-up (per selected technology):
```
IF len(selected_technologies) > 0:
  FOR each technology in selected_technologies:
    AskUserQuestion: template=QT-5
      question_text: "Why do you think {technology} might help?"
      header: "Rationale"
      intent: explain
    Capture rationale in session.technology_ideas[].rationale
```

VERIFY: Response captured (empty array is valid).

RECORD: Append the exchange to the Phase 04 checkpoint block; persist
`session.technology_ideas`.

```bash
devforgeai-validate phase-record ${BRAINSTORM_ID} --workflow=brainstorming --phase=04 --step=4.6 --project-root=. 2>&1
```

---

### Step 4.7: Adjacent Opportunities

EXECUTE:
```
AskUserQuestion:
  questions:
    - question: "Are there related problems that could be solved at the same time?"
      header: "Related"
      multiSelect: false
      options:
        - label: "Yes, several"
          description: "Multiple related issues"
        - label: "Maybe one or two"
          description: "A few possibilities"
        - label: "No, this is isolated"
          description: "Problem is independent"
        - label: "Not sure"
          description: "Haven't thought about it"
```

Follow-up:
```
IF response IN ("Yes, several", "Maybe one or two"):
  FOR i in [1..3]:
    Capture related_problem from user input.
    IF empty: BREAK
    AskUserQuestion:
      questions:
        - question: "How is '{related_problem}' connected to the main problem?"
          header: "Connection"
          multiSelect: false
          options:
            - label: "Same root cause"
              description: "Both stem from same issue"
            - label: "Same stakeholders"
              description: "Affects same people"
            - label: "Same system"
              description: "Same technology involved"
            - label: "Same process"
              description: "Part of same workflow"
    Append {problem: related_problem, connection: response} to session.opportunity.adjacent_opportunities[].
```

VERIFY: `session.opportunity.adjacent_opportunities` is set (may be empty).

RECORD: Append the exchange to the Phase 04 checkpoint block; persist
`session.opportunity.adjacent_opportunities`.

```bash
devforgeai-validate phase-record ${BRAINSTORM_ID} --workflow=brainstorming --phase=04 --step=4.7 --project-root=. 2>&1
```

---

### Step 4.8: Compile Opportunities

EXECUTE:
```
opportunities = []

# From user vision
opportunities.append({source: "user_vision", description: session.opportunity.ideal_state, type: "solution"})

# From divergent ideas (Step 4.3)
FOR idea in session.opportunity.divergent_ideas:
  opportunities.append({source: "divergent", description: idea})

# From technology ideas
FOR tech in session.technology_ideas:
  opportunities.append({source: "technology", description: "Implement {tech.name}", rationale: tech.rationale})

# From market research (if available)
IF session.market_research:
  FOR competitor in session.market_research.competitors:
    opportunities.append({source: "competitor", description: "Adopt {competitor.approach}", pros: competitor.pros, cons: competitor.cons})

# From adjacent problems
FOR adjacent in session.opportunity.adjacent_opportunities:
  opportunities.append({source: "adjacent", description: "Also solve: {adjacent.problem}", synergy: adjacent.connection})

session.opportunity.opportunities = opportunities
```

Display the compiled list and note: "These will be prioritized in Phase 09."

VERIFY: `session.opportunity.opportunities.length >= 1`.
IF empty: HALT -- "Step 4.8: No opportunities compiled. At least the user vision should yield 1."

RECORD: Append the exchange to the Phase 04 checkpoint block; persist
`session.opportunity.opportunities`.

```bash
devforgeai-validate phase-record ${BRAINSTORM_ID} --workflow=brainstorming --phase=04 --step=4.8 --project-root=. 2>&1
```

---

### Step 4.9: Idea Combination (Combinatorial Creativity)

**Methodology reference:** `references/brainstorming-techniques.md` § 2 (Idea Combination
— Combinatorial Creativity). Loads on first execution of this step.

EXECUTE:

Display:
"Some of the strongest opportunities come from combining ideas across sources. Below are
pairings of high-impact opportunities from different categories. Tell me if any
combinations would be stronger than the individuals."

```
Initialize: session.opportunity.combined_opportunities = []

# Compute pairings — prefer pairs whose .source values differ (cross-source diversity)
top_pairs = pick_top_3_to_5_pairings_by_source_diversity(session.opportunity.opportunities)

FOR each pair (A, B) in top_pairs:
  AskUserQuestion: template=QT-1 (variant: 2-option)
    question_text: "Can '{A.description}' (source: {A.source}) and '{B.description}'
                    (source: {B.source}) combine into something stronger?"
    header: "Combine?"
  IF response == "Yes":
    AskUserQuestion: template=QT-5 (intent: describe)
      question_text: "Describe the combined opportunity in one or two sentences."
      header: "Combined"
    Append {pair_id: [A.id, B.id], description: response, sources: [A.source, B.source]}
      to session.opportunity.combined_opportunities.
```

VERIFY: `session.opportunity.combined_opportunities` is a list (may be empty).

RECORD: Append the exchange to the Phase 04 checkpoint block; persist
`session.opportunity.combined_opportunities`. Feeds Phase 09 prioritization alongside
`session.opportunity.opportunities`.

```bash
devforgeai-validate phase-record ${BRAINSTORM_ID} --workflow=brainstorming --phase=04 --step=4.9 --project-root=. 2>&1
```

---

### Step 4.10: Context Window Check

EXECUTE:
```
IF estimated_context_usage > 70%:
  AskUserQuestion: template=QT-1
    question_text: "Context window is approximately {PERCENT}% full. Continue or save?"
    header: "Session"
    overrides:
      "Yes (Recommended)": { label: "Continue", description: "Proceed to Phase 05 (Business Case & Feasibility)" }
      "No":                { label: "Save and continue later", description: "Update checkpoint and exit" }
      remove: ["Skip / Defer"]
  IF response == "Save and continue later":
    Update the conversation checkpoint with all Phase 04 data
    Display: "Session saved. Resume with: /brainstorm --resume {BRAINSTORM_ID}"
    EXIT skill
ELSE:
  Display: "Context window healthy. Proceeding to Phase 05."
```

VERIFY: the context window check was performed.
IF skipped: HALT -- "Step 4.10: Context Window Check not performed."

RECORD: Persist `session.phases["04"].context_check_completed = true`.

```bash
devforgeai-validate phase-record ${BRAINSTORM_ID} --workflow=brainstorming --phase=04 --step=4.10 --project-root=. 2>&1
```

---

## Phase Exit Verification

Before transitioning to Phase 05, verify ALL exit criteria:

```
VERIFY_EXIT:
  CHECK: session.opportunity.ideal_state is non-empty
    IF FAIL: HALT -- "Exit blocked: Ideal state not described."
  CHECK: session.opportunity.target_outcome is non-empty
    IF FAIL: HALT -- "Exit blocked: Future-state target outcome not described."
  CHECK: session.success_vision.metrics.length >= 1
    IF FAIL: HALT -- "Exit blocked: No success metrics selected."
  CHECK: session.opportunity.to_be_process_sketch is populated
    IF FAIL: HALT -- "Exit blocked: To-be process sketch not captured."
  CHECK: session.opportunity.opportunities.length >= 1
    IF FAIL: HALT -- "Exit blocked: No opportunities compiled."
  CHECK: session.phases["04"].context_check_completed == true
    IF FAIL: HALT -- "Exit blocked: Context window check not completed."
  CHECK: session.phases["04"].questions_answered >= 4
    IF FAIL: HALT -- "Exit blocked: Minimum 4 questions required, only {count} answered."
```

Update the conversation checkpoint on successful exit (per
`references/conversation-checkpoint-format.md`): set the Phase 04 block `completed: true`,
write its `phase_summary`, advance `current_phase` to `"05"`.

VERIFY: `tmp/{BRAINSTORM_ID}/checkpoint.json` shows the Phase 04 block `completed: true`.
IF write fails: HALT -- "Phase 04 exit checkpoint not saved."

---

## Exit Gate

```bash
devforgeai-validate phase-complete ${BRAINSTORM_ID} --workflow=brainstorming --phase=04 --checkpoint-passed --project-root=. 2>&1
```

| Exit Code | Action |
|-----------|--------|
| 0 | Phase 04 complete — proceed to next phase |
| 127 | CLI not installed — proceed without enforcement |
| Other | HALT — checkpoint/step validation failed |

---

## Phase Transition Display

Display: "Phase 04 Complete — Future-State & Opportunity Mapping. Opportunities compiled:
{count}. Divergent ideas: {count}. Combined: {count}. Proceeding to Phase 05 (Business
Case & Feasibility)."
