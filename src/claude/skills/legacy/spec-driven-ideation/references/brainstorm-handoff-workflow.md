---
id: brainstorm-handoff-workflow
title: Brainstorm to Ideation Handoff Workflow
version: "2.0"
created: 2025-12-21
updated: 2026-05-17
status: Published
---

# Brainstorm Handoff Workflow

Detailed workflow for detecting and integrating brainstorm session data into ideation.

---

## Table of Contents

- [Overview](#overview)
- [Section 1: Brainstorm Detection](#section-1-brainstorm-detection)
  - [1.1 When to Check](#11-when-to-check)
  - [1.2 Display Available Brainstorms](#12-display-available-brainstorms)
  - [1.3 User Selection](#13-user-selection)
- [Section 2: Data Extraction](#section-2-data-extraction)
  - [2.1 Read Brainstorm Document](#21-read-brainstorm-document)
  - [2.2 Validate Extracted Data](#22-validate-extracted-data)
- [Section 3: Ideation Pre-Population](#section-3-ideation-pre-population)
  - [3.1 Set Session Context](#31-set-session-context)
  - [3.2 Display Pre-Population Summary](#32-display-pre-population-summary)
- [Section 4: Phase 1 Behavior Change](#section-4-phase-1-behavior-change)
  - [4.1 Skip or Shorten Discovery](#41-skip-or-shorten-discovery)
  - [4.2 Validate Brainstorm Data](#42-validate-brainstorm-data)
- [Section 5: Conflict Resolution](#section-5-conflict-resolution)
  - [5.1 Brainstorm vs User Input Conflicts](#51-brainstorm-vs-user-input-conflicts)
  - [5.2 Handle Outdated Brainstorms](#52-handle-outdated-brainstorms)
- [Section 6: Integration Points](#section-6-integration-points)
  - [6.1 Where Brainstorm Data Flows](#61-where-brainstorm-data-flows)
  - [6.2 Phase Modifications](#62-phase-modifications)
- [Common Issues and Recovery](#common-issues-and-recovery)
- [Success Criteria](#success-criteria)

---

## Overview

| Attribute | Value |
|-----------|-------|
| **Purpose** | Pre-populate the PM phase with brainstorm / Business-Analysis discoveries |
| **Trigger** | /ideate command Phase 0 |
| **Input** | `BRAINSTORM-{NNN}-{slug}.brainstorm.html` (v2.0, ADR-065 — JSON data island) OR legacy `BRAINSTORM-{NNN}.brainstorm.md` (v1.0 — YAML frontmatter) |
| **Effect** | Skip/shorten discovery; pre-populate constraints, risks, deferred ideas, roadmap |

---

## Section 1: Brainstorm Detection

### 1.1 When to Check

Check for brainstorms at the START of ideation, before any user questions.

```
FUNCTION check_for_brainstorms():
  # Search for brainstorm documents -- BOTH formats.
  # v2.0 (ADR-065): self-contained HTML with an embedded JSON data island.
  # v1.0 (legacy):  Markdown with YAML frontmatter (BRAINSTORM-001..006).
  html_brainstorms = Glob(pattern="devforgeai/specs/brainstorms/BRAINSTORM-*.brainstorm.html")
  md_brainstorms   = Glob(pattern="devforgeai/specs/brainstorms/BRAINSTORM-*.brainstorm.md")
  brainstorms = html_brainstorms + md_brainstorms

  IF len(brainstorms) == 0:
    RETURN null  # No brainstorms, proceed normally

  # Sort by creation date (newest first)
  brainstorms = sort_by_date_desc(brainstorms)

  RETURN brainstorms
```

### 1.2 Display Available Brainstorms

```
Display:
"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  Existing Brainstorm(s) Detected
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

FOR each brainstorm in brainstorms:
  # read_brainstorm_meta: YAML frontmatter for .md, the #brainstorm-data island for .html
  meta = read_brainstorm_meta(brainstorm)
  Display:
  "• {meta.id}: {meta.title}
    Created: {meta.created}
    Confidence: {meta.confidence_level}
    Problem: {meta.problem_statement[:50]}..."
```

### 1.3 User Selection

```
AskUserQuestion:
  questions:
    - question: "Would you like to use an existing brainstorm as input for ideation?"
      header: "Brainstorm"
      multiSelect: false
      options:
        - label: "Yes - use most recent (Recommended)"
          description: "Pre-populate ideation with {most_recent.id}"
        - label: "Yes - let me choose"
          description: "Select which brainstorm to use"
        - label: "No - start fresh"
          description: "Begin new ideation discovery"
```

**Handle "let me choose":**
```
IF response == "Yes - let me choose":
  options = []
  FOR each brainstorm in brainstorms:
    options.append({
      label: brainstorm.id,
      description: brainstorm.title
    })

  AskUserQuestion:
    questions:
      - question: "Which brainstorm would you like to use?"
        header: "Select"
        multiSelect: false
        options: options
```

---

## Section 2: Data Extraction

**Note:** This section handles file reading and field extraction that was previously performed
in the `/ideate` command's Phase 0.2. The command now passes only the file path; this skill
reads the file, **branches on file extension**, performs format-appropriate field extraction,
and constructs the context variable used throughout ideation.

### 2.1 Read Brainstorm Document

The extractor **branches on file extension before any parsing** so the wrong parser is
never run against the wrong format:

- `.brainstorm.html` -> **v2.0 path.** Extract the embedded JSON data island, parse it,
  and read schema-v2.0 fields. This is the current format (ADR-065).
- `.brainstorm.md` -> **v1.0 legacy path.** Parse YAML frontmatter as before. Retained so
  existing `BRAINSTORM-001..006` documents can still seed a `/ideate` session.

```
FUNCTION extract_brainstorm_data(brainstorm_path):
  content = Read(file_path=brainstorm_path)

  IF brainstorm_path ends with ".brainstorm.html":
    RETURN extract_from_html_v2(content)
  ELSE IF brainstorm_path ends with ".brainstorm.md":
    RETURN extract_from_md_v1(content)
  ELSE:
    HALT -- "Unrecognized brainstorm file extension: {brainstorm_path}"
```

#### 2.1a -- v2.0 HTML path (current format)

The v2.0 HTML document embeds its machine-readable data in a single JSON data island.
Ideation consumes that island; it never parses the HTML layout (per RESEARCH-007 --
structured machine state belongs in JSON, not HTML).

```
FUNCTION extract_from_html_v2(content):
  # Extract the JSON data island. The brainstorming skill emits exactly one:
  #   <script type="application/json" id="brainstorm-data">{ ... }</script>
  start_marker = '<script type="application/json" id="brainstorm-data">'
  end_marker   = '</script>'
  start = index_of(content, start_marker)
  IF start == -1:
    HALT -- "Brainstorm HTML has no #brainstorm-data island. File may be corrupt or pre-ADR-065."
  json_start = start + length(start_marker)
  json_end   = index_of(content, end_marker, from=json_start)
  data_json  = substring(content, json_start, json_end)
  data       = parse_json(data_json)
  IF parse fails:
    HALT -- "Brainstorm #brainstorm-data island is not valid JSON."

  # Schema check -- must be the v2.0 data-island contract.
  IF data.schema_version != "2.0":
    Display: "WARN: Brainstorm data-island schema is '{data.schema_version}', expected '2.0'. Proceeding best-effort."

  # Build the ideation context variable from schema-v2.0 fields.
  # Field provenance: brainstorm.schema.json v2.0
  # (.claude/skills/spec-driven-brainstorming/references/brainstorm.schema.json).
  brainstorm_context = {
    # Identity
    brainstorm_id:    data.id,
    title:            data.title,
    confidence_level: normalize_confidence(data.confidence_level),  # -> HIGH / MEDIUM / LOW
    source_format:    "html-v2.0",

    # Core outputs
    problem_statement:    data.problem_statement,
    target_outcome:       data.opportunity.target_outcome,
    recommended_approach: data.handoff.recommended_approach,

    # Stakeholders (Phase 02) -- registry carries influence / interest / RACI
    primary_stakeholder:  data.stakeholders.primary_stakeholder,
    stakeholder_registry: data.stakeholders.registry,           # [{id,name_or_role,category,influence,interest,raci,goals,concerns}]

    # Constraints & scope (Phase 07)
    budget_range:     data.constraints_scope.budget_range,
    timeline:         data.constraints_scope.timeline,
    hard_constraints: data.constraints_scope.hard_constraints,
    out_of_scope:     data.constraints_scope.out_of_scope,      # [{item,rationale}]

    # Requirements (Phase 08)
    functional_requirements: data.requirements.functional,      # [{id,statement,priority,source}]
    nfr_requirements:        data.requirements.nfrs,            # [{id,category,statement,metric}]
    glossary:                data.requirements.glossary,
    assumptions:             data.requirements.assumptions,     # Phase-08 assumptions register

    # Risk (Phase 06)
    risks: data.risk_analysis.risks,                            # [{id,description,likelihood,impact,severity,mitigation,owner}]

    # Prioritization & roadmap (Phase 09)
    must_have_capabilities: data.prioritization.must_have_capabilities,
    should_have:            data.prioritization.should_have,
    could_have:             data.prioritization.could_have,
    wont_have:              data.prioritization.wont_have,
    deferred_ideas:         data.prioritization.deferred_ideas, # DEF-NNN -- the Deferred Ideas Register (ADR-065)
    release_roadmap:        data.prioritization.release_roadmap,
    recommended_sequence:   data.prioritization.recommended_sequence,

    # Handoff (Phase 11)
    critical_assumptions: data.handoff.critical_assumptions,
    open_questions:       data.handoff.open_questions,

    # Visual design context
    design_artifacts: data.design_artifacts
  }
  RETURN brainstorm_context
```

#### 2.1b -- v1.0 Markdown path (legacy)

Unchanged behaviour for pre-ADR-065 `.brainstorm.md` documents -- parse YAML frontmatter.

```
FUNCTION extract_from_md_v1(content):
  frontmatter = parse_yaml_frontmatter(content)

  brainstorm_context = {
    # Identity
    brainstorm_id:    frontmatter.id,
    title:            frontmatter.title,
    confidence_level: frontmatter.confidence_level,
    source_format:    "md-v1.0",

    # Session metadata
    session_type:        frontmatter.session_type OR "standard",
    project_name:        frontmatter.project_name OR frontmatter.title,
    project_description: frontmatter.project_description OR frontmatter.problem_statement,

    # Core outputs
    problem_statement:    frontmatter.problem_statement,
    target_outcome:       frontmatter.target_outcome,
    recommended_approach: frontmatter.recommended_approach,

    # Stakeholders
    primary_stakeholder: frontmatter.primary_stakeholder,
    user_personas:       frontmatter.user_personas,

    # Constraints
    budget_range:     frontmatter.budget_range,
    timeline:         frontmatter.timeline,
    hard_constraints: frontmatter.hard_constraints,

    # Hypotheses
    critical_assumptions: frontmatter.critical_assumptions,

    # Priorities
    must_have_capabilities: frontmatter.must_have_capabilities,
    nice_to_have:           frontmatter.nice_to_have
  }
  # v1.0 documents predate the Deferred Ideas Register, risk register, and roadmap --
  # those context fields stay null and are elicited during ideation.
  RETURN brainstorm_context
```

### 2.2 Validate Extracted Data

```
FUNCTION validate_brainstorm_context(context):
  # Required fields differ slightly by source format.
  IF context.source_format == "html-v2.0":
    required_fields = ["problem_statement", "stakeholder_registry",
                       "hard_constraints", "must_have_capabilities"]
  ELSE:  # md-v1.0
    required_fields = ["problem_statement", "user_personas",
                       "hard_constraints", "must_have_capabilities"]

  missing = []
  FOR field in required_fields:
    IF context[field] is null OR context[field] is empty:
      missing.append(field)

  IF len(missing) > 0:
    Display:
    "⚠ Brainstorm missing some fields: {missing}
     These will be asked during ideation."

    context.incomplete_fields = missing

  RETURN context
```

---

## Section 3: Ideation Pre-Population

### 3.1 Set Session Context

```
FUNCTION apply_brainstorm_to_ideation(context):
  session = new IdeationSession()

  # Pre-populate from brainstorm
  session.brainstorm_input = context
  session.skip_discovery = context.confidence_level in ["HIGH", "MEDIUM"]

  # Map brainstorm fields to ideation session
  session.problem_statement = context.problem_statement
  session.business_goals = [context.target_outcome]
  session.constraints = context.hard_constraints
  session.must_have_requirements = context.must_have_capabilities
  session.assumptions = context.critical_assumptions

  # Personas: v1.0 carries user_personas; v2.0 carries the richer stakeholder_registry.
  IF context.source_format == "html-v2.0":
    session.stakeholder_registry = context.stakeholder_registry
    session.user_personas = derive_personas(context.stakeholder_registry)
  ELSE:
    session.user_personas = context.user_personas

  # v2.0-only PM-phase fields (null/absent for v1.0 -- elicited later).
  session.brainstorm_risks        = context.risks            # -> PM risk register
  session.brainstorm_deferred     = context.deferred_ideas   # -> idea backlog (DEF-NNN)
  session.brainstorm_roadmap      = context.release_roadmap  # -> milestone roadmap
  session.brainstorm_out_of_scope = context.out_of_scope
  session.brainstorm_assumptions  = context.assumptions      # Phase-08 assumptions register

  RETURN session
```

### 3.2 Display Pre-Population Summary

```
Display:
"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  Continuing from Brainstorm: {context.brainstorm_id}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Pre-populated from brainstorm:
  ✓ Problem: {context.problem_statement[:60]}...
  ✓ Users: {len(context.user_personas)} persona(s)
  ✓ Constraints: {len(context.hard_constraints)} identified
  ✓ Must-haves: {len(context.must_have_capabilities)} capabilities

Confidence: {context.confidence_level}

{IF confidence_level == 'HIGH':}
  → Skipping Phase 1 discovery (already complete)
  → Starting at Phase 2: Requirements Elicitation
{ELSE:}
  → Shortened Phase 1 discovery
  → Will ask for missing details only
"
```

---

## Section 4: Phase 1 Behavior Change

### 4.1 Skip or Shorten Discovery

**If brainstorm context present with HIGH confidence:**
```
FUNCTION handle_phase_1_with_brainstorm(session):
  IF session.brainstorm_input AND session.brainstorm_input.confidence_level == "HIGH":
    # Skip Phase 1 entirely
    Display: "Phase 1 (Discovery) - Skipped (from brainstorm)"
    GOTO Phase 2

  ELSE IF session.brainstorm_input:
    # Shortened Phase 1 - only ask for missing fields
    FOR field in session.brainstorm_input.incomplete_fields:
      ask_question_for(field)

    Display: "Phase 1 (Discovery) - Validated with additions"
    GOTO Phase 2

  ELSE:
    # No brainstorm - full discovery
    execute_full_phase_1()
```

### 4.2 Validate Brainstorm Data

```
FUNCTION validate_brainstorm_with_user(session):
  Display:
  "From your brainstorm, the problem is:
   \"{session.problem_statement}\"

   Is this still accurate?"

  AskUserQuestion:
    questions:
      - question: "Is the problem statement still accurate?"
        header: "Validate"
        multiSelect: false
        options:
          - label: "Yes, proceed"
            description: "Use brainstorm problem statement"
          - label: "Update it"
            description: "I want to refine the problem"

  IF response == "Update it":
    AskUserQuestion:
      questions:
        - question: "What's the updated problem statement?"
          header: "Problem"
          multiSelect: false
          options:
            - label: "Let me describe"
              description: "I'll provide an update"

    session.problem_statement = user_input
```

---

## Section 5: Conflict Resolution

### 5.1 Brainstorm vs User Input Conflicts

**If user provides different answer than brainstorm:**
```
FUNCTION resolve_conflict(field, brainstorm_value, user_value):
  IF brainstorm_value != user_value:
    AskUserQuestion:
      questions:
        - question: "Your brainstorm said '{brainstorm_value}' but you now said '{user_value}'. Which is correct?"
          header: "Clarify"
          multiSelect: false
          options:
            - label: "Use new answer"
              description: "I've updated my thinking"
            - label: "Use brainstorm"
              description: "Original brainstorm is correct"
            - label: "Both are valid"
              description: "Context changed"

    IF response == "Use new answer":
      RETURN user_value
    ELSE IF response == "Use brainstorm":
      RETURN brainstorm_value
    ELSE:
      # Note both, let user clarify
      RETURN {original: brainstorm_value, updated: user_value}
```

### 5.2 Handle Outdated Brainstorms

```
FUNCTION check_brainstorm_freshness(context):
  brainstorm_date = parse_date(context.created)
  days_old = (today - brainstorm_date).days

  IF days_old > 30:
    AskUserQuestion:
      questions:
        - question: "This brainstorm is {days_old} days old. Has anything changed?"
          header: "Freshness"
          multiSelect: false
          options:
            - label: "Still accurate"
              description: "Proceed with brainstorm data"
            - label: "Some things changed"
              description: "I'll note the updates"
            - label: "Start fresh"
              description: "Too much has changed"

    IF response == "Start fresh":
      session.brainstorm_input = null
      session.skip_discovery = false
```

---

## Section 6: Integration Points

### 6.1 Where Brainstorm Data Flows

| Brainstorm Field | Ideation Phase | Usage |
|------------------|----------------|-------|
| `problem_statement` | Phase 1 | Pre-populate, validate |
| `user_personas` / `stakeholder_registry` | Phase 1-2 | Pre-populate, skip persona questions; seed stakeholder register |
| `target_outcome` | Phase 1 | Business goals |
| `hard_constraints` | Phase 5 | Feasibility constraints |
| `must_have_capabilities` | Phase 2 | Seed requirements |
| `critical_assumptions` / `assumptions` | Phase 5 | Risk assessment; assumptions register |
| `budget_range` | Phase 5 | Feasibility |
| `timeline` | Phase 5 | Feasibility |
| `recommended_approach` | Phase 4 | Epic structure hint |
| `risks` (v2.0) | Phase 3-5 | Seed the PM risk register (RISK-NNN) |
| `deferred_ideas` (v2.0) | Phase 2-5 | Seed the idea backlog (DEF-NNN) -- see brainstorm-data-mapping.md Section 9 |
| `release_roadmap` (v2.0) | Phase 3-5 | Seed the milestone roadmap |
| `out_of_scope` (v2.0) | Phase 2 | Scope boundary -- out-of-scope items |

### 6.2 Phase Modifications

| Phase | Without Brainstorm | With Brainstorm |
|-------|-------------------|-----------------|
| Phase 1 | 5-10 questions | 0-3 questions |
| Phase 2 | 15-25 questions | 10-20 questions |
| Phase 3 | Standard | Standard |
| Phase 4 | Standard | Hint from approach |
| Phase 5 | Discover constraints | Validate constraints |
| Phase 6 | Standard | Standard |

---

## Common Issues and Recovery

| Issue | Symptom | Recovery |
|-------|---------|----------|
| Brainstorm `.md` corrupted | YAML parse error | Offer fresh ideation |
| Brainstorm `.html` corrupted | No `#brainstorm-data` island / invalid JSON | HALT -- file pre-ADR-065 or corrupt; offer fresh ideation |
| Missing critical fields | Null values | Ask during Phase 1 |
| Outdated brainstorm | Old date | Prompt for updates |
| Conflicting data | User contradicts | Resolution dialog |

---

## Success Criteria

- [ ] Brainstorms detected at ideation start
- [ ] User can choose which brainstorm to use
- [ ] Data extracted correctly (HTML `#brainstorm-data` island or YAML frontmatter)
- [ ] Phase 1 shortened when brainstorm present
- [ ] Conflicts resolved through user dialog
- [ ] Pre-population summary displayed

---

**Version:** 2.0 | **Status:** Published | **Created:** 2025-12-21 | **Updated:** 2026-05-17 (ADR-065 dual-format handoff)
