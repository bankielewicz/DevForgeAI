# Phase 3: Artifact Generation (Steps 3.1-3.2)

Generate YAML-structured requirements.md from discovered requirements per F4 schema. Epic creation is delegated to the /create-epic workflow.

---

## Table of Contents

- [Overview](#overview)
- [Step 3.1: Generate Requirements Document (Mandatory)](#step-31-generate-requirements-document-mandatory)
  - [Requirements Document Structure (F4 Schema)](#requirements-document-structure-f4-schema)
- [Step 3.2: Populate Requirements from Phase 2 Data](#step-32-populate-requirements-from-phase-2-data)
  - [Map Phase 2 Elicitation Output to F4 Schema](#map-phase-2-elicitation-output-to-f4-schema)
  - [User Personas Section (Optional)](#user-personas-section-optional)
  - [Write Requirements File](#write-requirements-file)
- [Step 3.2: Transition to Epic Creation](#step-32-transition-to-epic-creation)
  - [Report to user:](#report-to-user)
- [Common Issues and Recovery](#common-issues-and-recovery)
  - [Issue: Requirements Too Large (>800 lines)](#issue-requirements-too-large-800-lines)
- [Output from Steps 3.1-3.2](#output-from-steps-31-32)
- [Success Criteria for Steps 3.1-3.2](#success-criteria-for-steps-31-32)
- [References Used in Steps 3.1-3.2](#references-used-in-steps-31-32)

---

## Overview

Phase 3 transforms all discovered requirements into a YAML-structured requirements.md document that feeds downstream DevForgeAI skills. This phase creates the primary output from ideation: a structured requirements specification for consumption by the architecture skill and /create-epic command.

**Duration:** 5-15 minutes
**Output:** YAML-structured requirements.md (per F4 schema), transition to /create-epic workflow

---

## Step 3.1: Generate Requirements Document (Mandatory)

### Requirements Document Structure (F4 Schema)

Create YAML-structured file at `devforgeai/specs/requirements/{project-name}-requirements.md`:

```yaml
---
# F4 Schema: Structured Requirements for Cross-Session AI Consumption
version: "1.0"
project_name: "{project-name}"
created: "{YYYY-MM-DD}"
status: "draft"
author: "DevForgeAI Ideation"
---

functional_requirements:
  - id: "FR-001"
    category: "{category}"
    description: "{requirement description}"
    priority: "{High|Medium|Low}"
    user_story: "As a {role}, I want {capability} so that {benefit}"
    acceptance_criteria:
      - "{criterion 1}"
      - "{criterion 2}"

  - id: "FR-002"
    # ... additional functional requirements

non_functional_requirements:
  performance:
    - id: "NFR-P001"
      description: "{quantified performance requirement}"
      metric: "{measurable metric}"
      target: "{specific target value}"

  security:
    - id: "NFR-S001"
      description: "{security requirement}"
      compliance: "{standard if applicable}"

  scalability:
    - id: "NFR-SC001"
      description: "{scalability requirement}"
      target: "{specific target}"

constraints:
  technical:
    - id: "CON-T001"
      description: "{technical constraint}"
      rationale: "{why this constraint exists}"

  business:
    - id: "CON-B001"
      description: "{business constraint}"
      rationale: "{why this constraint exists}"

dependencies:
  external_systems:
    - name: "{system name}"
      integration_type: "{API|SDK|Database|etc.}"
      criticality: "{High|Medium|Low}"

  third_party_services:
    - name: "{service name}"
      purpose: "{why needed}"

design_decisions:
  - id: "DD-001"
    decision: "{what was decided}"
    rationale: "{why this approach was chosen}"
    alternatives_rejected:
      - name: "{alternative name}"
        reason: "{why rejected}"
    user_observations: "{relevant user insights from ideation}"
    constraints: "{constraints that influenced this decision}"

threat_model:
  adversary: "{who/what could attack or misuse the system}"
  in_scope:
    - "{threat vector 1}"
    - "{threat vector 2}"
  out_of_scope:
    - "{explicitly excluded threat 1}"
```

**F4 Schema Required Fields:**
- `functional_requirements` - Array of categorized requirements
- `non_functional_requirements` - Quantified performance/security/scalability
- `constraints` - Technical and business constraints
- `dependencies` - External systems and third-party services
- `design_decisions` - Design rationale, rejected alternatives, and user observations
- `threat_model` - Adversary definition, in-scope and out-of-scope threats

---

## Step 3.2: Populate Requirements from Phase 2 Data

### Map Phase 2 Elicitation Output to F4 Schema

```
# Transform Phase 2 user stories to functional_requirements
FOR each user_story in phase_2_output.user_stories:
    functional_requirement = {
        id: generate_id("FR"),
        category: categorize(user_story),
        description: user_story.summary,
        priority: user_story.priority,
        user_story: user_story.formatted,
        acceptance_criteria: user_story.criteria
    }
    requirements.functional_requirements.append(functional_requirement)

# Transform Phase 2 NFRs to non_functional_requirements
FOR each nfr in phase_2_output.non_functional:
    nfr_entry = {
        id: generate_id("NFR"),
        description: nfr.description,
        metric: nfr.metric,
        target: nfr.quantified_target
    }
    requirements.non_functional_requirements.{nfr.category}.append(nfr_entry)

# Populate constraints from Phase 2 discovery
FOR each constraint in phase_2_output.constraints:
    constraint_entry = {
        id: generate_id("CON"),
        description: constraint.description,
        rationale: constraint.rationale
    }
    requirements.constraints.{constraint.type}.append(constraint_entry)

# Populate dependencies from Phase 2 integrations
FOR each integration in phase_2_output.integrations:
    dependency_entry = {
        name: integration.name,
        integration_type: integration.type,
        criticality: integration.criticality
    }
    requirements.dependencies.external_systems.append(dependency_entry)
```

### User Personas Section (Optional)

```yaml
user_personas:
  - name: "{Persona Name}"
    role: "{role}"
    goals:
      - "{goal 1}"
      - "{goal 2}"
    pain_points:
      - "{pain point 1}"
      - "{pain point 2}"
```

---

### Write Requirements File

```
Write(
    file_path="devforgeai/specs/requirements/{project-name}-requirements.md",
    content=generated_yaml_requirements
)

Display: "✓ requirements.md created at devforgeai/specs/requirements/{project-name}-requirements.md"
```

**File Size:** Typically 200-800 lines depending on project scope

---

## Step 3.2: Transition to Epic Creation

### Report to user:

```
✅ Requirements documentation complete

Generated Artifacts:
- requirements.md (YAML per F4 schema) in devforgeai/specs/requirements/

Next Steps:
1. Run `/create-epic {project-name}` to create epic documents from requirements
2. Run `/create-context {project-name}` to create context files (greenfield)
3. Run `/create-sprint 1` to begin sprint planning
```

**Recommended Next Action (display-only, no auto-invocation):**

Run `/create-epic {project-name}`

The architecture skill will:
1. Load requirements.md (YAML per F4 schema)
2. Perform complexity assessment and feasibility analysis
3. Generate epic documents with feature decomposition
4. Create ADRs for technology decisions

**NOTE:** Per W3 compliance (STORY-135), the ideation skill does NOT auto-invoke
the architecture skill. The user manually runs `/create-epic` when ready.

---

## Common Issues and Recovery

### Issue: Requirements Too Large (>800 lines)

**Symptom:** Generated requirements.md is too verbose

**Recovery:**

```
# Focus on structured YAML, reduce narrative prose
# Each requirement should be 2-5 lines of YAML
# Use references instead of inline detail
```

---

## Output from Steps 3.1-3.2

**Files Created:**

1. **Requirements Document** (1 file, mandatory)
   - Location: `devforgeai/specs/requirements/{project}-requirements.md`
   - Size: 200-800 lines
   - Format: YAML-structured per F4 schema

**Verification:**

```
req_files = Glob(pattern="devforgeai/specs/requirements/*.md")
assert len(req_files) >= 1

✓ Artifact generation complete
→ Proceed to Phase 3.3 (Self-Validation)
```

---

## Success Criteria for Steps 3.1-3.2

Artifact generation complete when:
- [ ] requirements.md created (YAML per F4 schema)
- [ ] All F4 required fields present (functional_requirements, non_functional_requirements, constraints, dependencies)
- [ ] No write errors occurred
- [ ] Ready for validation (Phase 3.3)

**Token Budget:** ~3,000-5,000 tokens (requirements generation)

---

## References Used in Steps 3.1-3.2

**Phase Data Sources:**
- Phase 1: Problem statement, users, goals
- Phase 2: Complete requirements list

**On Error:**
- **error-type-2-artifact-failures.md** - Artifact generation failure recovery

---

**Next Step:** Phase 3.3 (Self-Validation) - Load self-validation-workflow.md
