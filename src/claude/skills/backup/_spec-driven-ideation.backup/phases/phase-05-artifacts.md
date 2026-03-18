# Phase 05: Artifact Generation

## Contract

| Attribute | Value |
|-----------|-------|
| **PURPOSE** | Generate the requirements.md output file in YAML per F4 schema format. This file is the primary deliverable of the entire ideation workflow and feeds into /create-epic and /create-context commands. |
| **REFERENCE** | `.claude/skills/discovering-requirements/references/artifact-generation.md` (299 lines), `.claude/skills/discovering-requirements/references/examples.md` |
| **STEP COUNT** | 6 mandatory steps (5.1 through 5.6) |
| **MINIMUM QUESTIONS** | 0-2 |

## Phase Exit Criteria

Before this phase can complete, ALL of the following MUST be true:

- [ ] project_name determined (non-empty, valid for filename)
- [ ] compiled_data assembled from all completed_outputs (Phases 02-04)
- [ ] F4 schema YAML generated with all required sections
- [ ] Requirements file written to `devforgeai/specs/requirements/{project_name}-requirements.md`
- [ ] File existence verified on disk (Glob confirmed)
- [ ] All 4 F4 required sections present in file (Grep confirmed: functional_requirements, non_functional_requirements, constraints, dependencies)
- [ ] User reviewed or acknowledged the generated artifact
- [ ] Checkpoint updated with phase data
- [ ] Context window check completed

**IF any criterion is unmet: HALT. Do NOT proceed to Phase 06.**

---

## Reference Loading [MANDATORY]

```
Read(file_path=".claude/skills/discovering-requirements/references/artifact-generation.md")
Read(file_path=".claude/skills/discovering-requirements/references/examples.md")
Read(file_path=".claude/skills/discovering-requirements/assets/templates/requirements-schema.yaml")
Read(file_path=".claude/skills/discovering-requirements/assets/templates/requirements-template.md")
```

IF any Read fails: HALT -- "Phase 05 cannot proceed without reference files and templates."

Do NOT rely on memory of previous reads. Load ALL FOUR references fresh every time this phase executes.

---

## Mandatory Steps

### Step 5.1: Determine Project Name

**Condition:** Uses `session.completed_outputs.problem_statement`, `session.brainstorm_input` (if present), and user input to derive a filename-safe project name.

**EXECUTE:**
```
# Priority 1: Check if brainstorm input provided a project name
IF session.brainstorm_input is not null AND session.brainstorm_input.project_name is not null:
  candidate_name = session.brainstorm_input.project_name
  Display: "Project name detected from brainstorm input: '{candidate_name}'"

# Priority 2: Check if business_idea or topic contains a project name
ELSE IF session.completed_outputs.business_idea is not null:
  candidate_name = derive_slug(session.completed_outputs.business_idea)
  Display: "Project name derived from business idea: '{candidate_name}'"

# Priority 3: Derive from problem statement keywords
ELSE IF session.completed_outputs.problem_statement is not null:
  # Extract 2-3 key words from problem statement
  topic_words = session.completed_outputs.problem_statement.lower().split()
  stop_words = ["the", "a", "an", "and", "or", "for", "to", "of", "in", "on", "is", "are", "we", "our", "this", "that"]
  key_words = [w for w in topic_words if w not in stop_words]
  candidate_name = "-".join(key_words[:3])
  Display: "Project name derived from problem statement: '{candidate_name}'"

# Priority 4: Ask the user
ELSE:
  candidate_name = null

# Sanitize candidate name for filename safety
IF candidate_name is not null:
  # Lowercase, replace spaces with hyphens, remove special chars
  sanitized_name = sanitize_for_filename(candidate_name)
  # Strip to max 50 chars
  sanitized_name = sanitized_name[:50]

  AskUserQuestion:
    questions:
      - question: "The project name will be '{sanitized_name}'. This determines the output filename. Is this correct?"
        header: "Project Name"
        multiSelect: false
        options:
          - label: "Yes, use this name"
            description: "Proceed with '{sanitized_name}'"
          - label: "I want a different name"
            description: "I'll provide my own project name"

  IF response == "I want a different name":
    AskUserQuestion:
      questions:
        - question: "What should the project be called? (lowercase, hyphens allowed, no special characters)"
          header: "Custom Name"
          multiSelect: false
          options:
            - label: "Let me type it"
              description: "I'll provide the name"

    Capture user_provided_name
    sanitized_name = sanitize_for_filename(user_provided_name)
    Increment question counter by 1

  session.project_name = sanitized_name
  Increment question counter by 1

ELSE:
  # No candidate at all -- must ask user
  AskUserQuestion:
    questions:
      - question: "What should we call this project? (This determines the output filename.)"
        header: "Project Name"
        multiSelect: false
        options:
          - label: "Let me type it"
            description: "I'll provide the project name"

  Capture user_provided_name
  session.project_name = sanitize_for_filename(user_provided_name)
  Increment question counter by 1
```

**VERIFY:**
```
IF session.project_name is null OR session.project_name == "":
  HALT -- "Step 5.1: Project name is empty. Cannot generate requirements file without a name."

IF len(session.project_name) < 2:
  HALT -- "Step 5.1: Project name too short ('{session.project_name}'). Minimum 2 characters."

IF session.project_name contains characters NOT in [a-z, 0-9, -]:
  HALT -- "Step 5.1: Project name contains invalid characters. Only lowercase letters, numbers, and hyphens allowed."

# Check for filename collision
existing = Glob(pattern="devforgeai/specs/requirements/{session.project_name}*requirements.md")
IF len(existing) > 0:
  Display: "WARNING: A requirements file already exists for this project name."
  Display: "  Existing: {existing[0]}"
  AskUserQuestion:
    questions:
      - question: "A requirements file already exists for '{session.project_name}'. What should we do?"
        header: "File Conflict"
        multiSelect: false
        options:
          - label: "Overwrite existing file"
            description: "Replace the existing requirements file"
          - label: "Use a different name"
            description: "I'll provide an alternative project name"
          - label: "Cancel artifact generation"
            description: "Stop -- I need to review the existing file first"

  IF response == "Use a different name":
    # Re-run Step 5.1 name capture
    Capture new name, re-validate
  ELSE IF response == "Cancel artifact generation":
    HALT -- "Step 5.1: User cancelled artifact generation due to file conflict."
  # ELSE overwrite proceeds normally
```

**RECORD:**
```
session.project_name = sanitized_name
session.phases["05"].output_path = "devforgeai/specs/requirements/{session.project_name}-requirements.md"
Update checkpoint: { phase: 5, step: "5.1", status: "complete" }
session.phases["05"].step_5_1_completed = true
```

---

### Step 5.2: Compile Requirements Data

**Condition:** Gathers all data from `session.completed_outputs` across Phases 02, 03, and 04.

**EXECUTE:**
```
compiled_data = {
  # ===== From Phase 02: Discovery & Problem Understanding =====
  problem_statement: session.completed_outputs.problem_statement,
  personas: session.completed_outputs.personas,
  business_goals: session.completed_outputs.business_goals,
  success_metrics: session.completed_outputs.success_metrics,
  scope_boundaries: session.completed_outputs.scope_boundaries,
  complexity_assessment: session.completed_outputs.complexity_assessment,

  # ===== From Phase 03: Requirements Elicitation =====
  functional_requirements: session.completed_outputs.functional_requirements,
  nfr_requirements: session.completed_outputs.nfr_requirements,
  data_entities: session.completed_outputs.data_entities,
  integrations: session.completed_outputs.integrations,
  domain: session.completed_outputs.domain,

  # ===== From Phase 04: Analysis & Validation (if exists) =====
  adr_prerequisites: session.completed_outputs.adr_prerequisites or [],
  compliance_requirements: session.completed_outputs.compliance_requirements or [],

  # ===== Derived fields =====
  design_decisions: [],
  threat_model: null,
  constraints: []
}

# Merge constraints from multiple sources
# Source 1: scope_boundaries.out_of_scope (items with deferral targets)
IF compiled_data.scope_boundaries is not null:
  FOR each out_item in compiled_data.scope_boundaries.out_of_scope:
    compiled_data.constraints.append({
      type: "business",
      constraint: "Out of scope: {out_item}",
      source: "Phase 02 scope boundaries"
    })

# Source 2: ADR prerequisites from Phase 04
IF compiled_data.adr_prerequisites is not null:
  FOR each adr in compiled_data.adr_prerequisites:
    compiled_data.constraints.append({
      type: "technical",
      constraint: adr.description,
      source: "Phase 04 ADR prerequisite"
    })

# Derive design decisions from complexity assessment and domain selection
IF compiled_data.complexity_assessment is not null:
  compiled_data.design_decisions.append({
    id: "DD-001",
    decision: "Complexity tier {compiled_data.complexity_assessment.tier} ({compiled_data.complexity_assessment.tier_label}) architecture approach",
    rationale: "Based on complexity score {compiled_data.complexity_assessment.total}/20",
    alternatives_rejected: [],
    user_observations: "Validated by user during Phase 02 complexity assessment"
  })

IF compiled_data.domain is not null:
  compiled_data.design_decisions.append({
    id: "DD-002",
    decision: "Apply {compiled_data.domain} domain patterns",
    rationale: "Domain selected and confirmed by user during Phase 03 elicitation",
    alternatives_rejected: [],
    user_observations: "Domain-specific requirements patterns applied"
  })

# Derive threat model from compliance requirements and integrations
threat_in_scope = []
threat_out_of_scope = []

IF compiled_data.compliance_requirements is not null AND len(compiled_data.compliance_requirements) > 0:
  FOR each compliance in compiled_data.compliance_requirements:
    threat_in_scope.append("Compliance: {compliance}")

IF compiled_data.integrations is not null AND len(compiled_data.integrations) > 0:
  FOR each integration in compiled_data.integrations:
    threat_in_scope.append("Integration security: {integration.name}")

IF len(threat_in_scope) > 0:
  compiled_data.threat_model = {
    adversary: "External attackers, unauthorized users, data leakage vectors",
    in_scope: threat_in_scope,
    out_of_scope: ["Nation-state attacks", "Physical security", "Social engineering"]
  }
ELSE:
  compiled_data.threat_model = {
    adversary: "Standard web application threat model",
    in_scope: ["Unauthorized access", "Data validation bypass", "Injection attacks"],
    out_of_scope: ["Nation-state attacks", "Physical security", "Social engineering"]
  }

Display:
"Compilation Summary:
  Functional Requirements: {len(compiled_data.functional_requirements)}
  Non-Functional Requirements: {len(compiled_data.nfr_requirements)}
  Data Entities: {len(compiled_data.data_entities)}
  Integrations: {len(compiled_data.integrations)}
  Constraints: {len(compiled_data.constraints)}
  Design Decisions: {len(compiled_data.design_decisions)}
  Personas: {len(compiled_data.personas)}
  Business Goals: {len(compiled_data.business_goals)}
  Threat Model: {'Present' if compiled_data.threat_model else 'None'}"
```

**VERIFY:**
```
# F4 required fields check
IF compiled_data.functional_requirements is null OR len(compiled_data.functional_requirements) < 1:
  HALT -- "Step 5.2: functional_requirements is empty. Cannot generate F4 schema without at least 1 functional requirement."

IF compiled_data.nfr_requirements is null OR len(compiled_data.nfr_requirements) < 1:
  HALT -- "Step 5.2: nfr_requirements is empty. Cannot generate F4 schema without at least 1 non-functional requirement."

IF compiled_data.constraints is null OR len(compiled_data.constraints) < 1:
  Display: "WARNING: No constraints compiled. Adding placeholder constraint."
  compiled_data.constraints.append({
    type: "business",
    constraint: "No explicit constraints identified during ideation",
    source: "Phase 05 artifact generation"
  })

IF compiled_data.integrations is null:
  compiled_data.integrations = []
  Display: "NOTE: No integrations identified. Dependencies section will list 'None identified'."

# Verify problem statement exists (critical for document header)
IF compiled_data.problem_statement is null OR compiled_data.problem_statement == "":
  HALT -- "Step 5.2: problem_statement is missing. Cannot generate requirements without a problem statement."
```

**RECORD:**
```
session.compiled_data = compiled_data
Update checkpoint: { phase: 5, step: "5.2", status: "complete" }
session.phases["05"].step_5_2_completed = true
session.phases["05"].compilation_counts = {
  functional: len(compiled_data.functional_requirements),
  nfr: len(compiled_data.nfr_requirements),
  constraints: len(compiled_data.constraints),
  integrations: len(compiled_data.integrations),
  design_decisions: len(compiled_data.design_decisions)
}
```

---

### Step 5.3: Generate F4 Schema YAML

**Condition:** Uses `session.compiled_data` from Step 5.2 and templates loaded during Reference Loading.

**EXECUTE:**
```
# Generate sequential IDs for each requirement type
fr_counter = 1
nfr_p_counter = 1
nfr_s_counter = 1
nfr_sc_counter = 1
nfr_r_counter = 1
nfr_u_counter = 1
nfr_m_counter = 1
con_t_counter = 1
con_b_counter = 1
dep_counter = 1

# ============================
# YAML Frontmatter Generation
# ============================

yaml_frontmatter = """---
# =============================================================================
# REQUIREMENTS SPECIFICATION
# =============================================================================
# Schema Version: 1.0
# Purpose: Structured requirements for cross-session AI consumption
# Generated by: spec-driven-ideation skill, Phase 05

schema_version: "1.0"
document_id: "REQ-{session.ideation_id}"
title: "{session.project_name}"
created: "{current_date_YYYY_MM_DD}"
last_updated: "{current_date_YYYY_MM_DD}"
status: "Draft"

# DECISIONS (locked choices with excluded options)
decisions:
"""

FOR each dd in session.compiled_data.design_decisions:
  yaml_frontmatter += """  - id: "{dd.id}"
    domain: "{derive_domain(dd)}"
    decision: "{dd.decision}"
    rejected:
"""
  IF len(dd.alternatives_rejected) > 0:
    FOR each alt in dd.alternatives_rejected:
      yaml_frontmatter += """      - option: "{alt.name}"
        reason: "{alt.reason}"
"""
  ELSE:
    yaml_frontmatter += """      - option: "No alternatives evaluated"
        reason: "Single approach identified during ideation"
"""
  yaml_frontmatter += """    rationale: "{dd.rationale}"
    locked: true
"""

# SCOPE (explicit boundaries with deferral targets)
yaml_frontmatter += """
# SCOPE (explicit boundaries with deferral targets)
scope:
  in:
"""
FOR each item in session.compiled_data.scope_boundaries.in_scope:
  yaml_frontmatter += """    - "{item}"
"""

yaml_frontmatter += """  out:
"""
IF session.compiled_data.scope_boundaries.out_of_scope is not null:
  FOR each item in session.compiled_data.scope_boundaries.out_of_scope:
    yaml_frontmatter += """    - item: "{item}"
      deferral_target: "Post-MVP"
"""
IF session.compiled_data.scope_boundaries.future is not null:
  FOR each item in session.compiled_data.scope_boundaries.future:
    yaml_frontmatter += """    - item: "{item}"
      deferral_target: "Phase 2"
"""

# SUCCESS CRITERIA (quantified, measurable)
yaml_frontmatter += """
# SUCCESS CRITERIA (quantified, measurable)
success_criteria:
"""
sc_counter = 1
FOR each metric in session.compiled_data.success_metrics:
  yaml_frontmatter += """  - id: "SC-{sc_counter}"
    metric: "{metric.kpi}"
    target: "{metric.target_value}"
    measurement: "{metric.source or 'To be determined during implementation'}"
"""
  sc_counter += 1

# FUNCTIONAL REQUIREMENTS
yaml_frontmatter += """
# FUNCTIONAL REQUIREMENTS
functional_requirements:
"""
FOR each fr in session.compiled_data.functional_requirements:
  fr_id = "FR-{str(fr_counter).zfill(3)}"
  yaml_frontmatter += """  - id: "{fr_id}"
    category: "{fr.category or 'General'}"
    description: "{fr.description or fr.summary}"
    priority: "{fr.priority or fr.moscow_priority}"
    user_story: "{fr.user_story or fr.formatted}"
    acceptance_criteria:
"""
  IF fr.acceptance_criteria is not null:
    FOR each criterion in fr.acceptance_criteria:
      yaml_frontmatter += """      - "{criterion}"
"""
  ELSE:
    yaml_frontmatter += """      - "To be defined during architecture phase"
"""
  fr_counter += 1

# NON-FUNCTIONAL REQUIREMENTS
yaml_frontmatter += """
# NON-FUNCTIONAL REQUIREMENTS
non_functional_requirements:
  performance:
"""
FOR each nfr in session.compiled_data.nfr_requirements:
  IF nfr.category == "performance":
    yaml_frontmatter += """    - id: "NFR-P{str(nfr_p_counter).zfill(3)}"
      description: "{nfr.description}"
      metric: "{nfr.metric}"
      target: "{nfr.quantified_target or nfr.target}"
"""
    nfr_p_counter += 1

yaml_frontmatter += """  security:
"""
FOR each nfr in session.compiled_data.nfr_requirements:
  IF nfr.category == "security":
    yaml_frontmatter += """    - id: "NFR-S{str(nfr_s_counter).zfill(3)}"
      description: "{nfr.description}"
      compliance: "{nfr.compliance or 'N/A'}"
"""
    nfr_s_counter += 1

yaml_frontmatter += """  scalability:
"""
FOR each nfr in session.compiled_data.nfr_requirements:
  IF nfr.category == "scalability":
    yaml_frontmatter += """    - id: "NFR-SC{str(nfr_sc_counter).zfill(3)}"
      description: "{nfr.description}"
      target: "{nfr.quantified_target or nfr.target}"
"""
    nfr_sc_counter += 1

# CONSTRAINTS
yaml_frontmatter += """
# CONSTRAINTS
constraints:
  technical:
"""
FOR each con in session.compiled_data.constraints:
  IF con.type == "technical":
    yaml_frontmatter += """    - id: "CON-T{str(con_t_counter).zfill(3)}"
      description: "{con.constraint}"
      rationale: "{con.source or con.rationale or 'Identified during ideation'}"
"""
    con_t_counter += 1

yaml_frontmatter += """  business:
"""
FOR each con in session.compiled_data.constraints:
  IF con.type == "business":
    yaml_frontmatter += """    - id: "CON-B{str(con_b_counter).zfill(3)}"
      description: "{con.constraint}"
      rationale: "{con.source or con.rationale or 'Identified during ideation'}"
"""
    con_b_counter += 1

# DEPENDENCIES
yaml_frontmatter += """
# DEPENDENCIES
dependencies:
  external_systems:
"""
IF len(session.compiled_data.integrations) > 0:
  FOR each integration in session.compiled_data.integrations:
    yaml_frontmatter += """    - name: "{integration.name}"
      integration_type: "{integration.type or 'API'}"
      criticality: "{integration.criticality or 'Medium'}"
"""
ELSE:
  yaml_frontmatter += """    - name: "None identified"
      integration_type: "N/A"
      criticality: "N/A"
"""

yaml_frontmatter += """  third_party_services: []

# DESIGN DECISIONS
design_decisions:
"""
FOR each dd in session.compiled_data.design_decisions:
  yaml_frontmatter += """  - id: "{dd.id}"
    decision: "{dd.decision}"
    rationale: "{dd.rationale}"
    alternatives_rejected:
"""
  IF len(dd.alternatives_rejected) > 0:
    FOR each alt in dd.alternatives_rejected:
      yaml_frontmatter += """      - name: "{alt.name}"
        reason: "{alt.reason}"
"""
  ELSE:
    yaml_frontmatter += """      - name: "No alternatives evaluated"
        reason: "Single approach identified during ideation"
"""
  yaml_frontmatter += """    user_observations: "{dd.user_observations or ''}"
    constraints: "{dd.constraints or 'None'}"
"""

# THREAT MODEL
yaml_frontmatter += """
# THREAT MODEL
threat_model:
  adversary: "{session.compiled_data.threat_model.adversary}"
  in_scope:
"""
FOR each threat in session.compiled_data.threat_model.in_scope:
  yaml_frontmatter += """    - "{threat}"
"""
yaml_frontmatter += """  out_of_scope:
"""
FOR each threat in session.compiled_data.threat_model.out_of_scope:
  yaml_frontmatter += """    - "{threat}"
"""

# USER PERSONAS (optional but recommended)
yaml_frontmatter += """
# USER PERSONAS
user_personas:
"""
IF session.compiled_data.personas is not null:
  FOR each persona in session.compiled_data.personas:
    yaml_frontmatter += """  - name: "{persona.name}"
    role: "{persona.role}"
    goals:
"""
    FOR each goal in persona.goals:
      yaml_frontmatter += """      - "{goal}"
"""
    yaml_frontmatter += """    pain_points:
"""
    FOR each pp in persona.pain_points:
      yaml_frontmatter += """      - "{pp}"
"""

# STAKEHOLDERS
yaml_frontmatter += """
# STAKEHOLDERS
stakeholders:
"""
IF session.compiled_data.business_goals is not null:
  yaml_frontmatter += """  - role: "Product Owner"
    goals:
"""
  FOR each goal in session.compiled_data.business_goals:
    yaml_frontmatter += """      - "{goal.goal}"
"""
  yaml_frontmatter += """    decision_authority:
      - "Feature priority"
      - "Release timing"
"""

# PROVENANCE
yaml_frontmatter += """
# PROVENANCE
source_brainstorm: "{session.brainstorm_input.brainstorm_id or 'N/A'}"
"""

yaml_frontmatter += """---"""

# ============================
# Markdown Body Generation
# ============================

markdown_body = """

# Requirements: {session.project_name}

## Overview

This document captures the structured requirements produced by the spec-driven-ideation skill.
All data is stored in the YAML frontmatter above for cross-session AI consumption.

**Problem Statement:** {session.compiled_data.problem_statement}

**Complexity:** Tier {session.compiled_data.complexity_assessment.tier} ({session.compiled_data.complexity_assessment.tier_label})

## Reading This Document

- **Decisions:** See `decisions` in frontmatter -- locked choices with explicit excluded options
- **Scope:** See `scope.in` (included) and `scope.out` (excluded with deferral targets)
- **Success Criteria:** See `success_criteria` -- quantified metrics with targets
- **Functional Requirements:** See `functional_requirements` -- categorized with acceptance criteria
- **NFRs:** See `non_functional_requirements` -- performance, security, scalability
- **Constraints:** See `constraints` -- technical and business limitations
- **Dependencies:** See `dependencies` -- external systems and third-party services

## Summary

| Category | Count |
|----------|-------|
| Functional Requirements | {fr_counter - 1} |
| Non-Functional Requirements | {total_nfr_count} |
| Constraints | {con_t_counter + con_b_counter - 2} |
| Dependencies | {len(session.compiled_data.integrations)} |
| Design Decisions | {len(session.compiled_data.design_decisions)} |
| User Personas | {len(session.compiled_data.personas)} |
| Success Criteria | {sc_counter - 1} |

## Next Steps

1. Review locked decisions in frontmatter
2. Validate scope boundaries
3. Proceed to `/create-epic` with this requirements document
4. Run `/create-context` if greenfield project

---

*Generated by spec-driven-ideation skill | Schema v1.0 | {current_date}*
"""

requirements_content = yaml_frontmatter + markdown_body
```

**VERIFY:**
```
# YAML structural validation
IF requirements_content does not start with "---":
  HALT -- "Step 5.3: Generated content does not start with YAML frontmatter delimiter."

IF requirements_content does not contain a closing "---" after frontmatter:
  HALT -- "Step 5.3: Generated content missing closing YAML frontmatter delimiter."

# Required F4 sections present in generated content
required_sections = [
  "functional_requirements:",
  "non_functional_requirements:",
  "constraints:",
  "dependencies:",
  "design_decisions:",
  "threat_model:"
]

FOR each section in required_sections:
  IF section NOT in requirements_content:
    HALT -- "Step 5.3: F4 required section '{section}' missing from generated YAML."

# Verify at least 1 FR has an ID
IF "FR-001" NOT in requirements_content:
  HALT -- "Step 5.3: No functional requirement IDs found. Generation may have failed."

# Verify no placeholder text leaked through
placeholder_patterns = ["[Project/Feature Title]", "[domain]", "YYYY-MM-DD", "REQ-XXX"]
FOR each pattern in placeholder_patterns:
  IF pattern in requirements_content:
    HALT -- "Step 5.3: Unresolved placeholder '{pattern}' found in generated content."
```

**RECORD:**
```
session.requirements_content = requirements_content
session.requirements_yaml = yaml_frontmatter
Update checkpoint: { phase: 5, step: "5.3", status: "complete" }
session.phases["05"].step_5_3_completed = true
session.phases["05"].generated_line_count = count_lines(requirements_content)
```

---

### Step 5.4: Write Requirements File

**EXECUTE:**
```
output_path = "devforgeai/specs/requirements/{session.project_name}-requirements.md"

TRY:
  Write(
    file_path=output_path,
    content=session.requirements_content
  )
  Display: "Requirements file written to: {output_path}"

EXCEPT PermissionError:
  # Try alternative path under project root
  alt_path = "devforgeai/specs/requirements/ideation-output-{session.project_name}.md"
  Display: "Permission denied on primary path. Trying alternative: {alt_path}"
  Write(file_path=alt_path, content=session.requirements_content)
  output_path = alt_path

EXCEPT:
  Display: "ERROR: Could not write requirements file."
  Display: "Content will be displayed for manual save."
  Display: session.requirements_content
  HALT -- "Step 5.4: File write failed. Content displayed for manual copy."
```

**VERIFY:**
```
# Verify file exists on disk
glob_result = Glob(pattern="devforgeai/specs/requirements/{session.project_name}*requirements.md")
IF len(glob_result) == 0:
  HALT -- "Step 5.4: Requirements file NOT created on disk. Glob returned 0 matches."

verified_path = glob_result[0]
Display: "File existence verified: {verified_path}"

# Verify F4 required sections are present in the written file
section_checks = [
  "functional_requirements:",
  "non_functional_requirements:",
  "constraints:",
  "dependencies:"
]

FOR each section in section_checks:
  grep_result = Grep(pattern=section, path=verified_path)
  IF grep_result returns 0 matches:
    HALT -- "Step 5.4: F4 schema field '{section}' missing from generated file at {verified_path}."

Display: "All 4 F4 required sections verified in file."

# Verify file is not empty or trivially small
file_content = Read(file_path=verified_path)
line_count = count_lines(file_content)
IF line_count < 20:
  HALT -- "Step 5.4: Generated file suspiciously small ({line_count} lines). Expected 50+ lines."
Display: "File size: {line_count} lines"
```

**RECORD:**
```
session.completed_outputs.requirements_file_path = verified_path
session.phases["05"].output_path = verified_path
session.phases["05"].output_line_count = line_count
Update checkpoint: { phase: 5, step: "5.4", status: "complete" }
session.phases["05"].step_5_4_completed = true
```

---

### Step 5.5: User Review of Generated Artifact

**EXECUTE:**
```
# Count requirements by type for summary
fr_count = len(session.compiled_data.functional_requirements)
nfr_count = len(session.compiled_data.nfr_requirements)
con_count = len(session.compiled_data.constraints)
dep_count = len(session.compiled_data.integrations)

# Count MoSCoW priorities
must_count = len([r for r in session.compiled_data.functional_requirements if r.priority in ["Must", "High", "Critical"]])
should_count = len([r for r in session.compiled_data.functional_requirements if r.priority in ["Should", "Medium"]])
could_count = len([r for r in session.compiled_data.functional_requirements if r.priority in ["Could", "Low"]])
wont_count = len([r for r in session.compiled_data.functional_requirements if r.priority in ["Won't", "Deferred"]])

Display:
"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  Requirements Artifact Generated
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

File: {session.phases['05'].output_path}
Lines: {session.phases['05'].output_line_count}

Requirement Counts:
  Functional Requirements:     {fr_count}
  Non-Functional Requirements: {nfr_count}
  Constraints:                 {con_count}
  Dependencies:                {dep_count}
  Design Decisions:            {len(session.compiled_data.design_decisions)}

Priority Breakdown:
  Must Have / Critical:  {must_count}
  Should Have / Medium:  {should_count}
  Could Have / Low:      {could_count}
  Won't Have / Deferred: {wont_count}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

AskUserQuestion:
  questions:
    - question: "Would you like to review the generated requirements file?"
      header: "Review Artifact"
      multiSelect: false
      options:
        - label: "Yes, show me the file"
          description: "Display the full requirements document"
        - label: "No, proceed to validation"
          description: "I trust the generation -- move to Phase 6"
        - label: "I need to make changes"
          description: "I want to edit specific sections"

IF response == "Yes, show me the file":
  Read(file_path=session.phases["05"].output_path)
  Display: "[Full file content displayed above]"
  session.phases["05"].user_reviewed = true

  AskUserQuestion:
    questions:
      - question: "Does the generated document look correct?"
        header: "Confirm"
        multiSelect: false
        options:
          - label: "Looks good"
            description: "Proceed to validation"
          - label: "Needs changes"
            description: "I'll describe what needs fixing"

  IF response == "Needs changes":
    AskUserQuestion:
      questions:
        - question: "What needs to be changed?"
          header: "Changes"
          multiSelect: false
          options:
            - label: "Let me describe the changes"
              description: "I'll explain what to fix"

    Capture user_changes
    # Apply changes to requirements_content
    # Re-write file with updated content
    Write(file_path=session.phases["05"].output_path, content=updated_content)

    # Re-verify after changes
    glob_verify = Glob(pattern="devforgeai/specs/requirements/{session.project_name}*requirements.md")
    IF len(glob_verify) == 0:
      HALT -- "Step 5.5: Re-written file not found on disk after changes."
    Display: "Changes applied and file re-written."
    session.phases["05"].user_reviewed = true
    session.phases["05"].changes_applied = true

ELSE IF response == "No, proceed to validation":
  session.phases["05"].user_reviewed = false
  session.phases["05"].user_acknowledged = true
  Display: "Acknowledged. Proceeding to context window check."

ELSE IF response == "I need to make changes":
  AskUserQuestion:
    questions:
      - question: "Describe the changes you'd like to make:"
        header: "Edit Request"
        multiSelect: false
        options:
          - label: "Let me describe"
            description: "I'll explain the edits needed"

  Capture user_edits
  # Apply edits to requirements_content
  # Re-write file
  Write(file_path=session.phases["05"].output_path, content=updated_content)

  # Re-verify
  glob_verify = Glob(pattern="devforgeai/specs/requirements/{session.project_name}*requirements.md")
  IF len(glob_verify) == 0:
    HALT -- "Step 5.5: Re-written file not found on disk after edits."
  Display: "Edits applied and file re-written."
  session.phases["05"].user_reviewed = true
  session.phases["05"].changes_applied = true
```

**VERIFY:**
```
IF session.phases["05"].user_reviewed != true AND session.phases["05"].user_acknowledged != true:
  HALT -- "Step 5.5: User has neither reviewed nor acknowledged the generated artifact."

# If changes were applied, re-verify F4 sections
IF session.phases["05"].changes_applied == true:
  FOR each section in ["functional_requirements:", "non_functional_requirements:", "constraints:", "dependencies:"]:
    grep_result = Grep(pattern=section, path=session.phases["05"].output_path)
    IF grep_result returns 0 matches:
      HALT -- "Step 5.5: F4 section '{section}' lost after user edits. File integrity compromised."
```

**RECORD:**
```
session.phases["05"].user_reviewed = true or false
session.phases["05"].user_acknowledged = true or false
session.phases["05"].changes_applied = true or false
Update checkpoint: { phase: 5, step: "5.5", status: "complete" }
session.phases["05"].step_5_5_completed = true
IF questions asked: session.phases["05"].questions_answered += count
```

---

### Step 5.6: Context Window Check

**EXECUTE:**
```
IF estimated_context_usage > 70%:
  AskUserQuestion:
    questions:
      - question: "Context window is approximately {PERCENT}% full. Would you like to:"
        header: "Session Management"
        multiSelect: false
        options:
          - label: "Continue in this session"
            description: "Proceed to Phase 6 (Validation)"
          - label: "Save and continue later"
            description: "Create checkpoint and exit -- resume with /ideate --resume {IDEATION_ID}"

  IF response == "Save and continue later":
    # Update checkpoint with all Phase 05 data before exit
    checkpoint.progress.current_phase = 6
    checkpoint.progress.phases_completed.append("05")
    checkpoint.progress.completion_percentage = round(5/7 * 100)
    checkpoint.updated_at = "current ISO 8601 timestamp"

    Write(file_path="devforgeai/specs/ideation/${IDEATION_ID}.checkpoint.json", content=checkpoint)

    # Verify checkpoint write
    verify_result = Glob(pattern="devforgeai/specs/ideation/${IDEATION_ID}.checkpoint.json")
    IF not found: HALT -- "Step 5.6: Checkpoint save failed during session exit."

    Display: "Session saved. Resume with: /ideate --resume ${IDEATION_ID}"
    Display: "Requirements file already written to: {session.phases['05'].output_path}"
    EXIT skill

  ELSE:
    Display: "Continuing in current session."
    session.phases["05"].context_check_completed = true

ELSE:
  Display: "Context window healthy ({PERCENT}%). Proceeding to Phase 6."
  session.phases["05"].context_check_completed = true
```

**VERIFY:**
```
IF session.phases["05"].context_check_completed is null or false:
  HALT -- "Step 5.6: Context Window Check not performed."
```

**RECORD:**
```
Update checkpoint: session.phases["05"].context_check_completed = true
Update checkpoint: session.phases["05"].step_5_6_completed = true
```

---

## Phase Exit Verification

Before transitioning to Phase 06, verify ALL exit criteria:

```
VERIFY_EXIT:
  CHECK: session.project_name is not null AND session.project_name != ""
    IF FAIL: HALT -- "Exit blocked: project_name not determined."

  CHECK: session.compiled_data is not null
    IF FAIL: HALT -- "Exit blocked: compiled_data not assembled."

  CHECK: session.completed_outputs.requirements_file_path is not null
    IF FAIL: HALT -- "Exit blocked: requirements_file_path is null. File was not written."

  CHECK: Glob(pattern="devforgeai/specs/requirements/{session.project_name}*requirements.md") returns at least 1 result
    IF FAIL: HALT -- "Exit blocked: Requirements file not found on disk."

  CHECK: Grep(pattern="functional_requirements:", path=session.completed_outputs.requirements_file_path) returns matches
    IF FAIL: HALT -- "Exit blocked: functional_requirements section missing from file."

  CHECK: Grep(pattern="non_functional_requirements:", path=session.completed_outputs.requirements_file_path) returns matches
    IF FAIL: HALT -- "Exit blocked: non_functional_requirements section missing from file."

  CHECK: Grep(pattern="constraints:", path=session.completed_outputs.requirements_file_path) returns matches
    IF FAIL: HALT -- "Exit blocked: constraints section missing from file."

  CHECK: Grep(pattern="dependencies:", path=session.completed_outputs.requirements_file_path) returns matches
    IF FAIL: HALT -- "Exit blocked: dependencies section missing from file."

  CHECK: session.phases["05"].user_reviewed == true OR session.phases["05"].user_acknowledged == true
    IF FAIL: HALT -- "Exit blocked: User has not reviewed or acknowledged the artifact."

  CHECK: session.phases["05"].context_check_completed == true
    IF FAIL: HALT -- "Exit blocked: Context window check not completed."
```

Update checkpoint on successful exit:
```
checkpoint.progress.current_phase = 6
checkpoint.progress.phases_completed.append("05")
checkpoint.progress.completion_percentage = round(5/7 * 100)
checkpoint.updated_at = "current ISO 8601 timestamp"

checkpoint.phases["05"] = {
  "project_name": session.project_name,
  "output_path": session.completed_outputs.requirements_file_path,
  "output_line_count": session.phases["05"].output_line_count,
  "compilation_counts": session.phases["05"].compilation_counts,
  "user_reviewed": session.phases["05"].user_reviewed,
  "user_acknowledged": session.phases["05"].user_acknowledged,
  "changes_applied": session.phases["05"].changes_applied or false,
  "context_check_completed": session.phases["05"].context_check_completed,
  "questions_answered": session.phases["05"].questions_answered or 0,
  "steps_completed": ["step_5_1", "step_5_2", "step_5_3", "step_5_4", "step_5_5", "step_5_6"]
}

Write(file_path="devforgeai/specs/ideation/${IDEATION_ID}.checkpoint.json", content=checkpoint)
```

**VERIFY checkpoint write:** `Glob(pattern="devforgeai/specs/ideation/${IDEATION_ID}.checkpoint.json")`
IF not found: HALT -- "Phase 05 exit checkpoint was NOT saved."

---

## Phase Transition Display

```
Display:
"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  Phase 5 Complete: Artifact Generation
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Requirements File: {session.completed_outputs.requirements_file_path}
File Size: {session.phases['05'].output_line_count} lines

Requirement Counts:
  Functional Requirements:     {session.phases['05'].compilation_counts.functional}
  Non-Functional Requirements: {session.phases['05'].compilation_counts.nfr}
  Constraints:                 {session.phases['05'].compilation_counts.constraints}
  Dependencies:                {session.phases['05'].compilation_counts.integrations}
  Design Decisions:            {session.phases['05'].compilation_counts.design_decisions}

User Review: {session.phases['05'].user_reviewed ? 'Reviewed' : 'Acknowledged'}
Changes Applied: {session.phases['05'].changes_applied ? 'Yes' : 'No'}

Proceeding to Phase 6: Validation...
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
```

---

## Common Issues and Recovery

| Issue | Symptom | Recovery |
|-------|---------|----------|
| File write fails | Permission denied or disk error | Try alternative path, display content for manual save |
| Missing Phase 02/03 data | compiled_data has null fields | Mark as "TBD" in output, note in document body |
| F4 section missing after write | Grep returns 0 for a required section | Re-generate YAML, check for syntax errors in template |
| Requirements too large (>800 lines) | File exceeds expected size | Focus on structured YAML, reduce narrative prose |
| Project name collision | Existing file found during Step 5.1 | Offer overwrite, rename, or cancel options |
| Placeholder text leaked | Unresolved template variables in output | Re-run Step 5.3 with explicit variable substitution |
| User edits break F4 compliance | Grep fails after re-write | Re-verify all sections, offer to restore from pre-edit version |
