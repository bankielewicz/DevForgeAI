# Phase 07: Handoff Synthesis

## Contract

| Attribute | Value |
|-----------|-------|
| **PURPOSE** | Generate the structured AI-consumable brainstorm document for handoff to /ideate |
| **REFERENCE** | `.claude/skills/spec-driven-brainstorming/references/handoff-synthesis-workflow.md` |
| **STEP COUNT** | 11 mandatory steps |
| **MINIMUM QUESTIONS** | 0 (validation only) |

## Phase Exit Criteria

- [ ] All session data compiled
- [ ] Confidence level calculated
- [ ] Short name generated
- [ ] YAML frontmatter generated
- [ ] Document body generated with all 7 sections
- [ ] File written to devforgeai/specs/brainstorms/
- [ ] File existence verified on disk via Glob
- [ ] Checkpoint deleted (session complete)
- [ ] User validated output
- [ ] Next steps displayed

## Reference Loading [MANDATORY]

```
Read(file_path=".claude/skills/spec-driven-brainstorming/references/handoff-synthesis-workflow.md")
Read(file_path=".claude/skills/spec-driven-brainstorming/references/output-templates.md")
```

IF either Read fails: HALT -- "Phase 07 cannot proceed without reference files."

---

## Mandatory Steps

### Step 7.1: Compile Session Data

```
EXECUTE:
  Gather all outputs from Phases 1-6:

  compiled_data = {
    # Phase 1: Stakeholders
    stakeholder_map: session.stakeholder_map,

    # Phase 2: Problem
    problem_statement: session.problem_statement,
    root_causes: session.root_causes,
    current_state: session.current_state,
    pain_points: session.pain_points,
    failed_solutions: session.failed_solutions,

    # Phase 3: Opportunities
    research_conducted: session.research_enabled,
    market_research: session.market_research,
    ideal_state: session.ideal_state,
    success_vision: session.success_vision,
    technology_ideas: session.technology_ideas,
    opportunities: session.opportunities,
    adjacent_opportunities: session.adjacent_opportunities,

    # Phase 4: Constraints
    constraints: session.constraints,

    # Phase 5: Hypotheses
    hypotheses: session.hypotheses,

    # Phase 6: Prioritization
    moscow: session.moscow,
    impact_effort: session.impact_effort,
    recommended_sequence: session.recommended_sequence
  }

VERIFY:
  - compiled_data has non-null values for all Phase 1-6 sections
  - IF any section is empty: Mark as "TBD" in output, note in open questions
  - At minimum: problem_statement, stakeholder_map, and moscow must be populated

RECORD:
  session.compiled_data = compiled_data
  Update checkpoint: { phase: 7, step: "7.1", status: "complete" }
```

---

### Step 7.2: Generate Confidence Level

```
EXECUTE:
  confidence_factors = []

  # Factor 1: Stakeholder completeness
  IF len(stakeholder_map.primary) >= 1 AND len(stakeholder_map.secondary) >= 1:
    confidence_factors.append("stakeholders_complete")

  # Factor 2: Root cause depth
  IF root_cause_level >= 3:
    confidence_factors.append("root_cause_explored")

  # Factor 3: Constraint clarity
  IF constraints.budget.range != "Not defined yet" AND constraints.timeline.target != null:
    confidence_factors.append("constraints_clear")

  # Factor 4: Hypothesis validation plan
  IF len([h for h in hypotheses if h.validation_method]) >= 1:
    confidence_factors.append("hypotheses_testable")

  # Factor 5: Priority alignment
  IF len(moscow.must_have) >= 1 AND len(moscow.must_have) <= 5:
    confidence_factors.append("priorities_focused")

  # Calculate confidence level
  IF len(confidence_factors) >= 4:
    confidence_level = "HIGH"
  ELSE IF len(confidence_factors) >= 2:
    confidence_level = "MEDIUM"
  ELSE:
    confidence_level = "LOW"

VERIFY:
  - confidence_level is one of: HIGH, MEDIUM, LOW
  - Each factor evaluated against actual session data
  - Factor list stored for display in completion summary

RECORD:
  session.confidence_level = confidence_level
  session.confidence_factors = confidence_factors
  Update checkpoint: { phase: 7, step: "7.2", status: "complete" }
```

---

### Step 7.3: Generate Short Name

```
EXECUTE:
  # Extract key words from topic
  topic_words = session.topic.lower().split()

  # Remove common words
  stop_words = ["the", "a", "an", "and", "or", "for", "to", "of", "in", "on"]
  key_words = [w for w in topic_words if w not in stop_words]

  # Take first 3 key words
  short_name = "-".join(key_words[:3])

  # Sanitize for filename (lowercase, alphanumeric + hyphens only)
  short_name = sanitize_filename(short_name)

VERIFY:
  - short_name is non-empty
  - short_name contains only lowercase letters, numbers, and hyphens
  - short_name is 3-50 characters long
  IF empty after sanitization: Use "brainstorm-session" as fallback

RECORD:
  session.short_name = short_name
  Update checkpoint: { phase: 7, step: "7.3", status: "complete" }
```

---

### Step 7.4: Generate YAML Frontmatter

```
EXECUTE:
  Generate YAML frontmatter block with AI-consumable metadata:

  ---
  # DevForgeAI Brainstorm Session
  id: {brainstorm_id}
  title: "{topic}"
  status: Complete
  created: {date}
  facilitator: DevForgeAI
  session_duration: "{duration} minutes"
  question_count: {total_questions}

  # Core Outputs (AI-Consumable for /ideate)
  problem_statement: "{problem_statement}"
  target_outcome: "{ideal_state}"
  recommended_approach: "{first_must_have_description}"
  confidence_level: "{confidence_level}"

  # Stakeholder Summary
  primary_stakeholder: "{primary_stakeholder_name}"
  user_personas:
    - "{persona_1}: {role} - {goal}"
    - "{persona_2}: {role} - {goal}"

  # Constraint Summary
  budget_range: "{budget_range}"
  timeline: "{timeline_target}"
  hard_constraints:
    - "{constraint_1}"
    - "{constraint_2}"

  # Hypothesis Summary
  critical_assumptions:
    - "{hypothesis_1}"
    - "{hypothesis_2}"

  # Prioritization Summary
  must_have_capabilities:
    - "{must_have_1}"
    - "{must_have_2}"
  nice_to_have:
    - "{should_have_1}"
  ---

VERIFY:
  - All required YAML fields populated (id, title, status, created, problem_statement, confidence_level)
  - YAML is valid (no unclosed quotes, proper indentation)
  - Values pulled from actual session data, not placeholder text

RECORD:
  session.frontmatter = generated_frontmatter
  Update checkpoint: { phase: 7, step: "7.4", status: "complete" }
```

---

### Step 7.5: Generate Document Body

```
EXECUTE:
  Generate human-readable markdown with all 7 sections plus appendices:

  # {Title}

  ## Executive Summary
  {2-3 paragraph summary of session outcomes}

  ---

  ## 1. Stakeholder Analysis
  ### 1.1 Stakeholder Map
  {table: Category | Stakeholder | Role | Influence}
  ### 1.2 Goals & Concerns
  {details per stakeholder}
  ### 1.3 Conflicts
  {if any identified}

  ---

  ## 2. Problem Analysis
  ### 2.1 Problem Statement
  {blockquote}
  ### 2.2 Root Cause Analysis
  {5 whys table}
  ### 2.3 Current State
  {metrics table}
  ### 2.4 Pain Points
  {table with severity}
  ### 2.5 Failed Solutions
  {if any}

  ---

  ## 3. Opportunity Canvas
  ### 3.1 Blue-Sky Vision
  {ideal state}
  ### 3.2 Market Research
  {if conducted, otherwise note skipped}
  ### 3.3 Opportunities
  {table: ID | Opportunity | Description | Potential Impact}
  ### 3.4 Adjacent Opportunities
  {if any}

  ---

  ## 4. Constraint Matrix
  ### 4.1 Budget
  ### 4.2 Timeline
  ### 4.3 Resources
  ### 4.4 Technical
  ### 4.5 Organizational

  ---

  ## 5. Hypothesis Register
  {table: ID | Hypothesis | Success Criteria | Validation | Risk}

  ---

  ## 6. Prioritized Opportunities
  ### 6.1 MoSCoW Classification
  ### 6.2 Impact-Effort Matrix
  ### 6.3 Recommended Sequence

  ---

  ## 7. Handoff to Ideation
  ### 7.1 Summary for /ideate
  ### 7.2 Recommended Next Steps
  ### 7.3 Open Questions

  ---

  ## Appendix A: Session Metadata
  ## Appendix B: Raw Session Data

VERIFY:
  - All 7 numbered sections present in document body
  - Executive Summary is 2-3 paragraphs (not placeholder)
  - Tables populated with actual session data
  - Appendix A contains session metadata (id, date, duration, question count)

RECORD:
  session.document_body = generated_body
  Update checkpoint: { phase: 7, step: "7.5", status: "complete" }
```

---

### Step 7.6: Write Output File

```
EXECUTE:
  output_path = "devforgeai/specs/brainstorms/{brainstorm_id}-{short_name}.brainstorm.md"

  TRY:
    Write(
      file_path=output_path,
      content=session.frontmatter + session.document_body
    )
    session.output_file = output_path
  EXCEPT PermissionError:
    alt_path = "./brainstorms/{brainstorm_id}-{short_name}.brainstorm.md"
    Write(file_path=alt_path, content=content)
    session.output_file = alt_path
  EXCEPT:
    Display: "Could not write file. Please copy the following:"
    Display: content
    HALT -- "Step 7.6: File write failed. Content displayed for manual save."

VERIFY: Output file exists on disk.
  Glob(pattern="devforgeai/specs/brainstorms/${BRAINSTORM_ID}*.brainstorm.md")
  IF not found: HALT -- "Step 7.6: Output document was NOT created on disk."
  Store path in session.output_file

RECORD:
  session.output_file = verified_path
  Update checkpoint: { phase: 7, step: "7.6", status: "complete" }
```

---

### Step 7.7: Generate Project Artifacts (OPTIONAL)

```
EXECUTE:
  AskUserQuestion:
    questions:
      - question: "Would you like to generate initial project files?"
        header: "Artifacts"
        multiSelect: false
        options:
          - label: "Yes - Generate all (README.md, CLAUDE.md, .gitignore)"
            description: "Complete project initialization from brainstorm"
          - label: "README.md and CLAUDE.md only"
            description: "Documentation files, no .gitignore"
          - label: "README.md only"
            description: "Human-readable project overview"
          - label: "Skip"
            description: "I'll create these manually later"

  IF response != "Skip":
    # Load templates
    Read(file_path=".claude/skills/spec-driven-brainstorming/assets/templates/readme-brainstorm-template.md")
    Read(file_path=".claude/skills/spec-driven-brainstorming/assets/templates/claude-md-template.md")
    Read(file_path=".claude/skills/spec-driven-brainstorming/assets/templates/gitignore-template.md")

    # Map session data to template variables
    template_vars = {
      project_name: sanitize_title(session.topic),
      project_slug: slugify(session.topic),
      tagline: session.topic,
      problem_statement: session.problem_statement,
      pain_points: session.pain_points,
      mvp_features: session.moscow.must_have,
      post_mvp: session.moscow.should_have + session.moscow.could_have,
      tech_stack: session.technology_ideas,
      constraints: session.constraints,
      design_decisions: session.hypotheses,
      brainstorm_file: session.output_file.basename,
      key_insights: extract_key_insights(session),
      research_artifacts: session.market_research.files if session.research_enabled else null
    }

    # Conflict handling for each artifact
    FOR each artifact in [README.md, CLAUDE.md, .gitignore]:
      IF artifact exists at project root:
        AskUserQuestion:
          questions:
            - question: "{artifact} already exists. What should I do?"
              header: "Conflict"
              multiSelect: false
              options:
                - label: "Overwrite"
                  description: "Replace existing {artifact}"
                - label: "Create {artifact.stem}-brainstorm{artifact.suffix}"
                  description: "Create with alternative name"
                - label: "Skip {artifact}"
                  description: "Keep existing file"

    # Write selected artifacts
    Populate templates with template_vars and Write each file

  IF response == "Skip":
    Display: "Skipping project artifact generation."
    Display: "You can manually create README.md and CLAUDE.md later."

VERIFY:
  - User responded to artifact question
  - IF generating: Each requested file written (or conflict resolved)
  - IF skipping: No files written, skip acknowledged

RECORD:
  session.artifacts_generated = [list of created files]
  Update checkpoint: { phase: 7, step: "7.7", status: "complete" }
```

---

### Step 7.8: Delete Checkpoint

```
EXECUTE:
  IF session.checkpoint_file exists:
    Delete checkpoint file (session is now complete)
    Display: "Checkpoint removed (session complete)"

  IF session.checkpoint_file does not exist:
    # No checkpoint to clean up
    Display: "No checkpoint to clean up."

VERIFY:
  - IF checkpoint existed: Confirm file is deleted
  - Session data is preserved in the output brainstorm document (not lost with checkpoint)

RECORD:
  session.checkpoint_deleted = true
  # No checkpoint update needed -- checkpoint is deleted
```

---

### Step 7.9: Validate with User

```
EXECUTE:
  Display:
    "Here's a summary of the brainstorm:

    Problem: {problem_statement}
    Stakeholders: {count}
    Opportunities: {count}
    Must-Haves: {count}
    Confidence: {confidence_level}

    Document saved to: {output_path}"

  AskUserQuestion:
    questions:
      - question: "Does this summary accurately capture what we discussed?"
        header: "Validation"
        multiSelect: false
        options:
          - label: "Yes, looks accurate"
            description: "Proceed with handoff"
          - label: "Needs minor corrections"
            description: "I'll make small edits later"
          - label: "Missing something important"
            description: "Key information was missed"
          - label: "Needs context for other sessions"
            description: "Another Claude session wouldn't understand all terms"

  IF response == "Missing something important":
    AskUserQuestion:
      questions:
        - question: "What's missing?"
          header: "Missing"
          multiSelect: false
          options:
            - label: "Let me describe"
              description: "I'll explain what's missing"
    # Add to document appendix or update relevant section
    # May need to re-generate and re-write document

  IF response == "Needs context for other sessions":
    Run portability validation:
      - Scan for undefined framework terms
      - Scan for incomplete file paths
      - Generate Glossary section if terms found
      - Generate Key Files section if paths found
      - Regenerate document with context sections
    Display: "Added context sections for cross-session portability"

VERIFY:
  - User explicitly responded to validation question
  - IF corrections needed: Changes applied and document re-written
  - IF context sections added: Document re-verified on disk via Glob

RECORD:
  session.user_validated = true
  session.validation_response = response
```

---

### Step 7.10: Display Completion Summary

```
EXECUTE:
  Display:
    "
    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
      Brainstorm Session Complete
    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

    Document: {output_path}

    Summary:
      - Stakeholders: {stakeholder_count} identified ({primary_count} primary)
      - Problem: {problem_statement_short}
      - Opportunities: {opportunity_count} candidates
      - Constraints: {constraint_summary}
      - Hypotheses: {hypothesis_count} to validate

    Confidence: {confidence_level}
      {confidence_factor_1} [met]
      {confidence_factor_2} [met]
      ...

    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
      Next Steps
    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

    1. Review brainstorm document for accuracy
    2. Run /ideate to transform into formal requirements
       - The brainstorm will be automatically detected
       - Key inputs will be pre-populated
    3. After ideation: /create-context for architecture

    Recommended command:
      /ideate
    "

VERIFY:
  - Summary displays actual counts from session data
  - Confidence factors listed match those calculated in Step 7.2
  - Output path matches the verified path from Step 7.6

RECORD:
  session.completion_displayed = true
```

---

### Step 7.11: Next Steps Prompt

```
EXECUTE:
  AskUserQuestion:
    questions:
      - question: "What would you like to do next?"
        header: "Next Step"
        multiSelect: false
        options:
          - label: "Proceed to /ideate"
            description: "Transform into formal requirements"
          - label: "Review document first"
            description: "I want to review before continuing"
          - label: "Share with stakeholders"
            description: "I need to get input from others"
          - label: "Done for now"
            description: "I'll continue later"

  IF response == "Proceed to /ideate":
    Display: "Run: /ideate"
    Display: "The brainstorm will be auto-detected and pre-populate key fields."

  IF response == "Review document first":
    Display: "Document location: {output_path}"
    Display: "After review, run: /ideate"

  IF response == "Share with stakeholders":
    Display: "Document to share: {output_path}"
    Display: "After stakeholder review, run: /ideate"

  IF response == "Done for now":
    Display: "Your brainstorm is saved."
    Display: "Location: {output_path}"
    Display: "When ready: /ideate"

VERIFY:
  - User responded with a next step choice
  - Appropriate guidance displayed for the chosen option

RECORD:
  session.next_step = response
  session.phase_7_complete = true
  # SESSION COMPLETE -- no further checkpoint updates
```

---

## Common Issues and Recovery

| Issue | Symptom | Recovery |
|-------|---------|----------|
| File write fails | Permission denied | Try alternative path, display content for manual save |
| Missing data | Section is empty | Mark as TBD, note in open questions |
| Low confidence | Few factors met | Highlight gaps for follow-up |
| User says incorrect | Missing info | Add to appendix, offer re-run of specific phase |
