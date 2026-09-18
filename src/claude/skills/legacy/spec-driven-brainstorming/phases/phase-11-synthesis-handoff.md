# Phase 11: Synthesis & Handoff

## Entry Gate

```bash
devforgeai-validate phase-check ${BRAINSTORM_ID} --workflow=brainstorming --from=10 --to=11 --project-root=. 2>&1
```

| Exit Code | Action |
|-----------|--------|
| 0 | Proceed to Phase 11 |
| 127 | CLI not installed — proceed without enforcement |
| Other | HALT — previous phase not complete |

---

## Contract

| Attribute | Value |
|-----------|-------|
| **PURPOSE** | Compile the full Business Analysis into the self-contained HTML deliverable — render all 11 phases, embed the schema-validated JSON data island, render the Session Transcript appendix from the conversation checkpoint, and RECORD the handoff section the downstream skill consumes |
| **REFERENCE** | `.claude/skills/spec-driven-brainstorming/references/conversation-checkpoint-format.md` |
| **STEP COUNT** | 10 mandatory steps |
| **MINIMUM QUESTIONS** | 3 |
| **GOVERNING ADR** | ADR-065 |

This is the **terminal** phase of the 11-phase Business Analysis workflow — the expansion
of the old synthesis phase. It does not advance to a Phase 12; its "transition" is skill
completion. It compiles the working `session.*` data captured across Phases 01–10 into the
v2.0 data-island structure, generates the self-contained HTML Business Analysis document
(`devforgeai/specs/brainstorms/BRAINSTORM-NNN-{slug}.brainstorm.html`), embeds the
machine-readable JSON conduit, and renders the accumulated conversation checkpoint as the
HTML "Session Transcript" appendix. Markdown output is retired (ADR-065 §Decision 3).

## Phase Exit Criteria

Field names listed are the canonical RECORD targets. The `handoff` section maps to the
`handoff` object of the data island (`references/brainstorm.schema.json` v2.0); the
compiled data maps to all 11 schema sections.

- [ ] All session data compiled into the 11 schema sections → `session.compiled_data`
- [ ] Confidence level computed → `session.confidence_level` (HIGH/MEDIUM/LOW)
- [ ] Short name (slug) generated → `session.short_name`
- [ ] Handoff section captured → `session.handoff.recommended_approach` (non-empty),
  `session.handoff.critical_assumptions`, `session.handoff.open_questions`
- [ ] JSON data island built and schema-validated → `session.data_island`
- [ ] HTML document written → `session.output_file` (file exists on disk via Glob)
- [ ] Session Transcript appendix rendered from the conversation checkpoint
- [ ] User validated the output → `session.user_validated`
- [ ] Conversation checkpoint retired → `session.checkpoint_retired`

**IF any blocking criterion is unmet: HALT. The skill is not complete.**

---

## Reference Loading

```
Read(file_path=".claude/skills/spec-driven-brainstorming/references/conversation-checkpoint-format.md")
Read(file_path=".claude/skills/spec-driven-brainstorming/references/brainstorm.schema.json")
Read(file_path=".claude/skills/spec-driven-brainstorming/references/user-interaction-patterns.md")
Read(file_path=".claude/skills/spec-driven-brainstorming/references/question-templates.md")
```

IF any Read fails: HALT -- "Phase 11 reference files not loaded. Cannot proceed without reference material."

The HTML output template is loaded in Step 11.6 (not here) — it is an asset, not a reference.

---

## Mandatory Steps

### Step 11.1: Compile Session Data

Map the working `session.*` fields captured across Phases 01–10 into the v2.0 data-island
section structure. The schema (`references/brainstorm.schema.json`) is the authoritative
target shape.

EXECUTE:
```
compiled_data = {
  # Top-level (schema required: schema_version, id, title, status, created,
  # problem_statement, confidence_level, handoff)
  schema_version: "2.0",
  id: BRAINSTORM_ID,
  title: session.topic,
  status: "Complete",
  created: {today's date, YYYY-MM-DD},
  facilitator: "DevForgeAI",
  question_count: {total questions answered across all phases},
  problem_statement: session.problem_statement,
  # confidence_level set in Step 11.2; handoff set in Step 11.4

  # Phase 01 → ba_planning
  ba_planning: {
    analysis_scope: session.ba_planning.analysis_scope,
    approach: session.ba_planning.approach,
    session_success_definition: session.ba_planning.session_success_definition
  },

  # Phase 02 → stakeholders. Phase 02 records voices top-level (session.stakeholder_voices)
  # and conflicts top-level (session.conflicts); Phase 11 is the translation layer.
  stakeholders: {
    primary_stakeholder: {name_or_role of the first Primary-category entry in session.stakeholders.registry},
    registry: session.stakeholders.registry,   # each entry conforms to $defs/stakeholder
    conflicts: session.conflicts,
    engagement_plan: session.stakeholders.engagement_plan,
    voices: session.stakeholder_voices         # schema stakeholders is additionalProperties:true
  },

  # Phase 03 → problem_analysis (Z15 HMW + cross-industry render here)
  problem_analysis: {
    root_causes: session.root_causes,            # Phase 03 records root_causes top-level
    current_state: session.current_state,
    as_is_process_model: session.problem_analysis.as_is_process_model,
    pain_points: session.pain_points,
    failed_solutions: session.failed_solutions,
    hmw_reframings: session.hmw_reframings,
    cross_industry_analogies: session.cross_industry_analogies
  },

  # Phase 04 → opportunity (Z13 divergent + Z14 combination render here)
  opportunity: {
    target_outcome: session.opportunity.target_outcome,
    ideal_state: session.opportunity.ideal_state,
    opportunities: session.opportunity.opportunities,
    divergent_ideas: session.opportunity.divergent_ideas,
    combined_opportunities: session.opportunity.combined_opportunities,
    adjacent_opportunities: session.opportunity.adjacent_opportunities,
    to_be_process_sketch: session.opportunity.to_be_process_sketch,
    success_metrics: session.success_vision.metrics   # Phase 04 records success metrics under session.success_vision
  },

  # Phase 05 → business_case
  business_case: {
    cost_benefit: session.business_case.cost_benefit,
    expected_value: session.business_case.expected_value,
    funding_justification: session.business_case.funding_justification,
    feasibility: session.business_case.feasibility   # {technical, operational, economic}
  },

  # Phase 06 → risk_analysis (Z16 pre-mortem rendered here)
  risk_analysis: {
    risks: session.risk_analysis.risks,         # each entry conforms to $defs/risk
    premortem: session.risk_analysis.premortem
  },

  # Phase 07 → constraints_scope (Z17 out-of-scope rendered here)
  constraints_scope: {
    budget_range: session.constraints_scope.budget_range,
    timeline: session.constraints_scope.timeline,
    hard_constraints: session.constraints_scope.hard_constraints,
    out_of_scope: session.constraints_scope.out_of_scope,
    context_boundary: session.constraints_scope.context_boundary
  },

  # Phase 08 → requirements
  requirements: {
    functional: session.requirements.functional,   # each entry conforms to $defs/functional_requirement
    nfrs: session.requirements.nfrs,                # each entry conforms to $defs/nfr
    glossary: session.requirements.glossary,
    assumptions: session.requirements.assumptions
  },

  # Phase 09 → prioritization (Deferred Ideas Register renders here)
  prioritization: {
    must_have_capabilities: session.prioritization.must_have_capabilities,
    should_have: session.prioritization.should_have,
    could_have: session.prioritization.could_have,
    wont_have: session.prioritization.wont_have,
    recommended_sequence: session.prioritization.recommended_sequence,
    deferred_ideas: session.prioritization.deferred_ideas,   # each entry conforms to $defs/deferred_idea
    release_roadmap: session.prioritization.release_roadmap
  },

  # Phase 10 → change_strategy
  change_strategy: {
    adoption_approach: session.change_strategy.adoption_approach,
    transition_plan: session.change_strategy.transition_plan,
    change_management: session.change_strategy.change_management,
    training_needs: session.change_strategy.training_needs
  },

  # Optional — populated only if UI was discussed
  design_artifacts: session.design_artifacts or null
}

For any section whose source field is null or empty, retain the key with an empty
value ([] for arrays, "" for strings) and add a note to session.handoff.open_questions
in Step 11.4 — never silently drop a section.
```

VERIFY: `compiled_data` contains all 11 section keys plus the schema-required top-level
fields. `problem_statement`, `ba_planning`, `stakeholders`, and `prioritization` MUST be
populated (a Business Analysis with none of these is not a valid handoff).
IF a required-populated section is empty: HALT -- "Step 11.1: {section} is empty — cannot synthesise an incomplete Business Analysis."

RECORD: Persist `session.compiled_data`.

```bash
devforgeai-validate phase-record ${BRAINSTORM_ID} --workflow=brainstorming --phase=11 --step=11.1 --project-root=. 2>&1
```

---

### Step 11.2: Compute Confidence Level

EXECUTE:
```
confidence_factors = []

# Factor 1: Stakeholder completeness
IF len(session.stakeholders.registry) >= 2 AND session.stakeholders.engagement_plan not empty:
  confidence_factors.append("stakeholders_complete")

# Factor 2: Root cause depth
IF len(session.problem_analysis.root_causes) >= 1 AND session.root_cause_found == true:
  confidence_factors.append("root_cause_explored")

# Factor 3: Constraint clarity
IF session.constraints_scope.budget_range not empty AND session.constraints_scope.timeline not empty:
  confidence_factors.append("constraints_clear")

# Factor 4: Requirements defined
IF len(session.requirements.functional) >= 1:
  confidence_factors.append("requirements_defined")

# Factor 5: Prioritization focused
IF len(session.prioritization.must_have_capabilities) >= 1 AND len(session.prioritization.must_have_capabilities) <= 7:
  confidence_factors.append("priorities_focused")

# Factor 6: Business case present
IF session.business_case.cost_benefit not empty:
  confidence_factors.append("business_case_present")

# Calculate
IF len(confidence_factors) >= 4:      confidence_level = "HIGH"
ELSE IF len(confidence_factors) >= 2: confidence_level = "MEDIUM"
ELSE:                                  confidence_level = "LOW"
```

VERIFY: `confidence_level` is one of HIGH/MEDIUM/LOW.

RECORD: Persist `session.confidence_level` and `session.confidence_factors`;
set `compiled_data.confidence_level = confidence_level`.

```bash
devforgeai-validate phase-record ${BRAINSTORM_ID} --workflow=brainstorming --phase=11 --step=11.2 --project-root=. 2>&1
```

---

### Step 11.3: Generate Short Name

EXECUTE:
```
topic_words = session.topic.lower().split()
stop_words = ["the", "a", "an", "and", "or", "for", "to", "of", "in", "on"]
key_words = [w for w in topic_words if w not in stop_words]
short_name = "-".join(key_words[:3])
short_name = sanitize_filename(short_name)   # lowercase, alphanumeric + hyphens only
```

VERIFY: `short_name` is non-empty, 3–50 chars, lowercase alphanumerics and hyphens.
IF empty after sanitization: use `"business-analysis"` as the fallback.

RECORD: Persist `session.short_name`.

```bash
devforgeai-validate phase-record ${BRAINSTORM_ID} --workflow=brainstorming --phase=11 --step=11.3 --project-root=. 2>&1
```

---

### Step 11.4: Capture the Handoff Section

The `handoff` object is the schema-required AI-consumable conduit core. It is the one
section the downstream skill reads first — confirm it with the user rather than deriving
it silently.

EXECUTE:
```
# Derive a candidate from the prioritised must-haves
candidate_approach = synthesise_one_sentence(session.prioritization.must_have_capabilities,
                                             session.opportunity.target_outcome)

AskUserQuestion: template=QT-5 (intent: rewrite)
  question_text: "Here is the recommended approach this analysis points to:
                  '{candidate_approach}'
                  Confirm it, or rewrite it in your own words."
  header: "Approach"
session.handoff.recommended_approach = {confirmed or rewritten text}

AskUserQuestion: template=QT-5 (intent: list)
  question_text: "What critical assumptions must hold for this approach to succeed?
                  Name each one. (Choose 'Done — no more' to finish.)"
  header: "Assumptions"
Loop: append each entry to session.handoff.critical_assumptions; BREAK on "Done — no more".
Seed the list with any session.requirements.assumptions already captured in Phase 08.

AskUserQuestion: template=QT-5 (intent: list)
  question_text: "What questions remain open — things the downstream work must still
                  resolve? (Choose 'Done — no more' to finish.)"
  header: "Open Qs"
Loop: append each entry to session.handoff.open_questions; BREAK on "Done — no more".
Add any empty-section notes flagged in Step 11.1 to this list.
```

VERIFY: `session.handoff.recommended_approach` is a non-empty string;
`critical_assumptions` and `open_questions` are lists (may be empty).
IF `recommended_approach` empty: HALT -- "Step 11.4: Handoff recommended_approach not captured."

RECORD: Append the exchanges to the Phase 11 checkpoint block; persist `session.handoff`;
set `compiled_data.handoff = session.handoff`.

```bash
devforgeai-validate phase-record ${BRAINSTORM_ID} --workflow=brainstorming --phase=11 --step=11.4 --project-root=. 2>&1
```

---

### Step 11.5: Build and Validate the JSON Data Island

EXECUTE:
```
data_island = serialise_json(compiled_data)
```

**Serialisation note (string-array flattening — from PR 4).** These schema fields are
typed `array of strings` and MUST emit a flat array of strings, NOT array-of-objects —
if the working `session.*` capture holds richer objects, flatten each to a single string:

- `requirements.assumptions`
- `prioritization.must_have_capabilities`, `prioritization.should_have`,
  `prioritization.could_have`, `prioritization.wont_have`
- `change_strategy.training_needs`

By contrast these stay as arrays of objects (do NOT flatten):
`prioritization.recommended_sequence`, `prioritization.release_roadmap`,
`prioritization.deferred_ideas`, `risk_analysis.risks`, `risk_analysis.premortem`,
`requirements.functional`, `requirements.nfrs`, `stakeholders.registry`.

VERIFY: validate `data_island` against `references/brainstorm.schema.json` (v2.0):
- `schema_version` is the string `"2.0"`
- all 8 required top-level fields present and non-empty: `schema_version`, `id`, `title`,
  `status`, `created`, `problem_statement`, `confidence_level`, `handoff`
- `id` matches `^BRAINSTORM-[0-9]{3,}$`
- `handoff.recommended_approach` is a non-empty string
- every `prioritization.deferred_ideas[].id` matches `^DEF-[0-9]{3,}$`
- every `risk_analysis.risks[].id` matches `^RISK-[0-9]{3,}$`
- every `requirements.functional[].id` matches `^FR-[0-9]{3,}$`
- every `requirements.nfrs[].id` matches `^NFR-[0-9]{3,}$`
- the string-array fields listed above are flat string arrays
IF validation fails: HALT -- "Step 11.5: Data island does not validate against brainstorm.schema.json v2.0 — {specific failure}."

RECORD: Persist `session.data_island` (the validated JSON text).

```bash
devforgeai-validate phase-record ${BRAINSTORM_ID} --workflow=brainstorming --phase=11 --step=11.5 --project-root=. 2>&1
```

---

### Step 11.6: Render Phase Sections and Transcript

EXECUTE:
```
Read(file_path=".claude/skills/spec-driven-brainstorming/assets/templates/brainstorm-template.html")
```

Render the HTML body for each of the 11 `{{PHASE_NN_CONTENT}}` placeholders from
`compiled_data`, using the template's existing CSS classes (no new CSS, no external
assets — the document stays self-contained):

- Registries render as `<table>` (stakeholders, risks, functional requirements, NFRs,
  the Deferred Ideas Register, the release roadmap).
- Risk severities use the `.sev-Low` / `.sev-Medium` / `.sev-High` / `.sev-Critical`
  classes already defined in the template.
- The Phase 09 impact-effort matrix renders as inline `<svg>` (ADR-065 §Decision 3).
- Lists (pain points, divergent ideas, HMW reframings, out-of-scope items, training
  needs, assumptions) render as `<ul>`.
- Stream C outputs render inside their host phase: divergent ideas + combinations in
  Phase 04, HMW + cross-industry in Phase 03, pre-mortem in Phase 06, out-of-scope in
  Phase 07, stakeholder voices in the Phase 02 stakeholder table `voice` column.
- An empty section renders a single `<p class="muted">Not captured in this session.</p>`.

Render the `{{TRANSCRIPT}}` placeholder from the conversation checkpoint
(`tmp/{BRAINSTORM_ID}/checkpoint.json`): for each object in `phases[]`, emit a
`<details>` block titled with the phase name; inside, render each `exchanges[]` entry as
the question (`q`) followed by the answer (`a`), and the `phase_summary` as a closing
line. Per `references/conversation-checkpoint-format.md` § "Relationship to the Output
Document".

VERIFY: every `{{PHASE_NN_CONTENT}}` (01–11) and `{{TRANSCRIPT}}` placeholder has
rendered content; no unsubstituted `{{...}}` token remains except inside the
`brainstorm-data` data-island script element (substituted in Step 11.7).
IF any phase placeholder is still literal: HALT -- "Step 11.6: Phase {NN} content not rendered."

RECORD: Persist `session.rendered_html` (the body with phase + transcript content filled in).

```bash
devforgeai-validate phase-record ${BRAINSTORM_ID} --workflow=brainstorming --phase=11 --step=11.6 --project-root=. 2>&1
```

---

### Step 11.7: Write the HTML Document

EXECUTE:
```
# Substitute the remaining header + data-island placeholders
html = session.rendered_html
html = substitute(html, {
  "{{TITLE}}":             compiled_data.title,
  "{{BRAINSTORM_ID}}":     compiled_data.id,
  "{{CREATED}}":           compiled_data.created,
  "{{CONFIDENCE}}":        compiled_data.confidence_level,
  "{{PROBLEM_STATEMENT}}": compiled_data.problem_statement,
  "{{DATA_ISLAND_JSON}}":  session.data_island
})

output_path = "devforgeai/specs/brainstorms/{BRAINSTORM_ID}-{short_name}.brainstorm.html"

TRY:
  Write(file_path=output_path, content=html)
  session.output_file = output_path
EXCEPT PermissionError:
  alt_path = "./brainstorms/{BRAINSTORM_ID}-{short_name}.brainstorm.html"
  Write(file_path=alt_path, content=html)
  session.output_file = alt_path
EXCEPT:
  Display: "Could not write the HTML document. Please copy the following:"
  Display: html
  HALT -- "Step 11.7: File write failed. Content displayed for manual save."
```

VERIFY: the output file exists on disk.
`Glob(pattern="devforgeai/specs/brainstorms/${BRAINSTORM_ID}*.brainstorm.html")`
Confirm no literal `{{` token remains anywhere in the written file.
IF not found: HALT -- "Step 11.7: Output HTML document was NOT created on disk."

RECORD: Persist `session.output_file` (the verified path).

```bash
devforgeai-validate phase-record ${BRAINSTORM_ID} --workflow=brainstorming --phase=11 --step=11.7 --project-root=. 2>&1
```

---

### Step 11.8: Generate Project Artifacts (OPTIONAL)

EXECUTE:
```
AskUserQuestion:
  questions:
    - question: "Would you like to generate initial project files from this analysis?"
      header: "Artifacts"
      multiSelect: false
      options:
        - label: "Yes — all (README.md, CLAUDE.md, .gitignore)"
          description: "Complete project initialization from the Business Analysis"
        - label: "README.md and CLAUDE.md only"
          description: "Documentation files, no .gitignore"
        - label: "README.md only"
          description: "Human-readable project overview"
        - label: "Skip"
          description: "I'll create these manually later"

IF response != "Skip":
  Read the requested templates from
  `.claude/skills/spec-driven-brainstorming/assets/templates/`
  (`readme-brainstorm-template.md`, `claude-md-template.md`, `gitignore-template.md`).
  Populate from compiled_data (problem_statement, must_have_capabilities, constraints,
  output_file basename). For each artifact already present at the project root, ask
  Overwrite / alternative-name / Skip before writing.
ELSE:
  Display: "Skipping project artifact generation."
```

VERIFY: the user responded; if generating, each requested file was written (or its
conflict resolved); if skipping, no files were written.

RECORD: Persist `session.artifacts_generated`.

```bash
devforgeai-validate phase-record ${BRAINSTORM_ID} --workflow=brainstorming --phase=11 --step=11.8 --project-root=. 2>&1
```

---

### Step 11.9: Validate with User

EXECUTE:
```
Display:
  "Business Analysis complete.
   Problem:       {problem_statement}
   Stakeholders:  {count}
   Requirements:  {functional count} FR / {nfr count} NFR
   Must-Haves:    {count}
   Risks:         {count}
   Deferred:      {deferred_ideas count}
   Confidence:    {confidence_level}
   Document:      {output_file}"

AskUserQuestion:
  questions:
    - question: "Does the generated Business Analysis document accurately capture this session?"
      header: "Validation"
      multiSelect: false
      options:
        - label: "Yes — accurate"
          description: "Proceed to completion"
        - label: "Needs minor corrections"
          description: "I'll make small edits to the HTML later"
        - label: "Missing something important"
          description: "Key information was missed — re-render needed"

IF response == "Missing something important":
  Capture what is missing, update compiled_data, and re-run Steps 11.5–11.7.
```

VERIFY: the user explicitly responded; if corrections were needed, the document was
re-rendered and re-verified on disk via Glob.

RECORD: Persist `session.user_validated = true` and `session.validation_response`.

```bash
devforgeai-validate phase-record ${BRAINSTORM_ID} --workflow=brainstorming --phase=11 --step=11.9 --project-root=. 2>&1
```

---

### Step 11.10: Complete the Session and Retire the Checkpoint

The conversation transcript is now durably embedded in the HTML document, so the working
checkpoint is no longer the only copy and may be retired
(`references/conversation-checkpoint-format.md` § "Relationship to the Output Document").

EXECUTE:
```
# Mark the checkpoint complete before retiring it (audit trail)
Update tmp/{BRAINSTORM_ID}/checkpoint.json: set the Phase 11 block completed: true,
write its phase_summary, set current_phase: "11".

# Retire the checkpoint — its content is now durable inside the HTML transcript appendix
IF tmp/{BRAINSTORM_ID}/checkpoint.json exists:
  Delete it.
  Display: "Conversation checkpoint retired (content preserved in the HTML transcript)."

Display the completion summary and next steps:
  "Business Analysis document: {output_file}
   Open it in any browser — all 11 phases, the risk register, the impact-effort matrix,
   the Deferred Ideas Register, and the full session transcript are self-contained.
   The embedded JSON data island (id 'brainstorm-data') is the machine-readable handoff
   conduit for downstream tooling."
```

VERIFY: `Glob(pattern="tmp/${BRAINSTORM_ID}/checkpoint.json")` returns empty (retired);
the completion summary was displayed.

RECORD: Persist `session.checkpoint_retired = true` and `session.phase_11_complete = true`.

```bash
devforgeai-validate phase-record ${BRAINSTORM_ID} --workflow=brainstorming --phase=11 --step=11.10 --project-root=. 2>&1
```

---

## Phase Exit Verification

This is the terminal phase — exit verification confirms the deliverable, not a handoff to
a successor phase.

```
VERIFY_EXIT:
  CHECK: session.compiled_data contains all 11 schema sections
    IF FAIL: HALT -- "Exit blocked: session data not fully compiled."
  CHECK: session.confidence_level is one of HIGH/MEDIUM/LOW
    IF FAIL: HALT -- "Exit blocked: confidence level not computed."
  CHECK: session.handoff.recommended_approach is a non-empty string
    IF FAIL: HALT -- "Exit blocked: handoff section not captured."
  CHECK: session.data_island validated against brainstorm.schema.json v2.0
    IF FAIL: HALT -- "Exit blocked: data island not schema-valid."
  CHECK: session.output_file exists on disk (Glob)
    IF FAIL: HALT -- "Exit blocked: HTML document not on disk."
  CHECK: session.user_validated == true
    IF FAIL: HALT -- "Exit blocked: user did not validate the output."
  CHECK: session.checkpoint_retired == true
    IF FAIL: HALT -- "Exit blocked: conversation checkpoint not retired."
  CHECK: session.phases["11"].questions_answered >= 3
    IF FAIL: HALT -- "Exit blocked: Minimum 3 questions required, only {count} answered."
```

---

## Exit Gate

```bash
devforgeai-validate phase-complete ${BRAINSTORM_ID} --workflow=brainstorming --phase=11 --checkpoint-passed --project-root=. 2>&1
```

| Exit Code | Action |
|-----------|--------|
| 0 | Phase 11 complete — proceed to next phase |
| 127 | CLI not installed — proceed without enforcement |
| Other | HALT — checkpoint/step validation failed |

---

## Phase Transition Display

Display: "Phase 11 Complete — Synthesis & Handoff. The Business Analysis is finished.
Document: {output_file}. Confidence: {confidence_level}. All 11 phases are complete —
the spec-driven-brainstorming workflow has finished."
