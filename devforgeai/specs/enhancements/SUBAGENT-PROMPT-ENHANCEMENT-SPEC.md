# Subagent Prompt Enhancement Specification

**Date:** 2025-11-06
**Related:** RCA-007 Fix (Phase 1)
**Priority:** HIGH
**Effort:** 30 minutes per subagent
**Status:** Specification Complete

---

## Purpose

Define standard prompt enhancement pattern for all subagents to prevent autonomous file creation and ensure content-only output for parent skill assembly.

**Applies to:**
- requirements-analyst
- api-designer
- Any subagent invoked by skills expecting content return (not file artifacts)

---

## Problem Statement

General-purpose subagents (requirements-analyst, api-designer) optimize for **completeness** by creating comprehensive deliverables with supporting documentation files. This violates the DevForgeAI single-file design principle when subagents are invoked by skills expecting content return for assembly.

**Example violation:**
- Skill invokes requirements-analyst expecting markdown content
- Subagent creates 6 files (main + 5 supporting docs)
- Skill receives file paths instead of content
- Assembly logic bypassed
- Framework design violated

---

## Standard Prompt Enhancement Pattern

### Template Structure

All subagent prompts invoked by skills MUST include these 4 sections:

**1. Pre-Flight Briefing**
**2. Output Constraints**
**3. Prohibited Actions**
**4. Output Format Examples**

---

## Section 1: Pre-Flight Briefing

**Purpose:** Establish subagent's role in larger workflow.

**Template:**
```markdown
**PRE-FLIGHT BRIEFING:**
You are being invoked by the {parent_skill_name} skill.
This skill will assemble your output into a {target_artifact} using {template_file}.

**YOUR ROLE:**
- Generate {content_type} (user story, API contracts, test cases, etc.)
- Return content as {format} (markdown sections, JSON object, etc.)
- Do NOT create files
- Parent skill handles file creation (Phase {phase_number}: {phase_name})

**OUTPUT WILL BE USED IN:**
- Phase {phase_number}: {phase_name} (assembly into {template_file})
- Your output is CONTENT for assembly, not a complete deliverable

**WORKFLOW CONTEXT:**
- Current workflow: {workflow_name}
- Current phase: Phase {current_phase}
- Next phase: Phase {next_phase}
- Final artifact: {final_artifact_path}
```

**Example (requirements-analyst invoked by devforgeai-story-creation):**
```markdown
**PRE-FLIGHT BRIEFING:**
You are being invoked by the devforgeai-story-creation skill.
This skill will assemble your output into a single .story.md file using story-template.md.

**YOUR ROLE:**
- Generate requirements content (user story, acceptance criteria, edge cases, NFRs)
- Return content as markdown sections
- Do NOT create files
- Parent skill handles file creation (Phase 5: Story File Creation)

**OUTPUT WILL BE USED IN:**
- Phase 5: Story File Creation (assembly into story-template.md)
- Your output is CONTENT for assembly, not a complete deliverable

**WORKFLOW CONTEXT:**
- Current workflow: Story creation (8-phase process)
- Current phase: Phase 2 (Requirements Analysis)
- Next phase: Phase 3 (Technical Specification)
- Final artifact: devforgeai/specs/Stories/{STORY-ID}-{slug}.story.md
```

---

## Section 2: Output Constraints

**Purpose:** Explicit constraints on what subagent can/cannot do.

**Template:**
```markdown
**CRITICAL OUTPUT CONSTRAINTS:**

1. **Format:** Return ONLY {format} (no file creation)
2. **Content:** Output will be inserted into {template_file} by parent skill
3. **Files:** Do NOT create separate files ({list_prohibited_file_types})
4. **Structure:** Output as sections: {section_1}, {section_2}, {section_3}
5. **Assembly:** Parent skill ({parent_skill_name}) will assemble all sections into single {artifact_type}
6. **Size:** Maximum {max_chars} characters (fits in parent template)

**Contract Reference:** {contract_yaml_path} (if applicable)
```

**Example (requirements-analyst):**
```markdown
**CRITICAL OUTPUT CONSTRAINTS:**

1. **Format:** Return ONLY markdown text content (no file creation)
2. **Content:** Output will be inserted into story-template.md by parent skill
3. **Files:** Do NOT create separate files (SUMMARY.md, QUICK-START.md, VALIDATION-CHECKLIST.md, FILE-INDEX.md, DELIVERY-SUMMARY.md)
4. **Structure:** Output as sections: User Story, Acceptance Criteria, Edge Cases, Data Validation Rules, Non-Functional Requirements
5. **Assembly:** Parent skill (devforgeai-story-creation) will assemble all sections into single .story.md file
6. **Size:** Maximum 50,000 characters (fits in story-template.md capacity)

**Contract Reference:** .claude/skills/devforgeai-story-creation/contracts/requirements-analyst-contract.yaml
```

**Example (api-designer):**
```markdown
**CRITICAL OUTPUT CONSTRAINTS:**

1. **Format:** Return ONLY OpenAPI 3.0 YAML specification (no file creation)
2. **Content:** Output will be inserted into technical specification section of .story.md
3. **Files:** Do NOT create separate files (api-spec.yaml, endpoints.md, schemas.md)
4. **Structure:** Single OpenAPI YAML document with paths, components, security
5. **Assembly:** Parent skill (devforgeai-story-creation) will embed this in Technical Specification section
6. **Size:** Maximum 30,000 characters (fits in story technical spec section)

**Contract Reference:** .claude/skills/devforgeai-story-creation/contracts/api-designer-contract.yaml
```

---

## Section 3: Prohibited Actions

**Purpose:** Explicit list of forbidden operations.

**Template:**
```markdown
**PROHIBITED ACTIONS:**

You MUST NOT:
1. ❌ Create files using Write tool
2. ❌ Create files using Edit tool on non-existent files
3. ❌ Create files using Bash with output redirection (>, >>, cat <<EOF)
4. ❌ Return file paths as output (e.g., "Created: file.md")
5. ❌ Return file creation statements (e.g., "File created successfully")
6. ❌ Generate multi-file deliverables (SUMMARY, QUICK-START, INDEX, etc.)
7. ❌ Write to disk in any form
8. ❌ Create comprehensive project structures (you generate CONTENT, not PROJECTS)

**Why prohibited:**
- Parent skill handles all file creation (Phase {phase_number})
- Your output is assembled with other content
- Multi-file output violates DevForgeAI single-file design
- Creates framework specification violations (RCA-007)

**What to do instead:**
- ✅ Return markdown text as string
- ✅ Structure content with section headers (## User Story, ## AC, etc.)
- ✅ Include all required information in text output
- ✅ Let parent skill decide file structure and naming
```

---

## Section 4: Output Format Examples

**Purpose:** Show subagent exactly what output should look like.

**Template:**
```markdown
**EXPECTED OUTPUT FORMAT:**

Your output should look like this (MARKDOWN TEXT, not files):

```markdown
## {Section 1 Name}
{Section 1 content example}

## {Section 2 Name}
{Section 2 content example}

...
```

**Example output:**
{Full example of expected output}

**What your output will become:**
Parent skill will insert your output into {template_file} at {location}:

```markdown
{Show how output fits into template}
```

**Final result:** Single {artifact_type} file at {final_path}
```

**Example (requirements-analyst):**
```markdown
**EXPECTED OUTPUT FORMAT:**

Your output should look like this (MARKDOWN TEXT, not files):

```markdown
## User Story
**As a** database administrator,
**I want** to capture all index characteristics before rebuild operations,
**so that** performance tuning settings are preserved and data loss prevented.

## Acceptance Criteria

### AC1: Capture standard index properties
**Given** a clustered or non-clustered index exists in the database
**When** fn_GetIndexDefinition() is called with database, schema, table, and index names
**Then** the function returns JSON containing IndexType, FillFactor, IsPadded, IgnoreDupKey, AllowRowLocks, AllowPageLocks, DataCompression, KeyColumns (with ASC/DESC), IncludedColumns, and FileGroupOrPartitionScheme

### AC2: Preserve filtered index predicates
**Given** a filtered index with WHERE clause exists
**When** fn_GetIndexDefinition() is called
**Then** the JSON includes FilterDefinition field with complete WHERE clause text

...

## Edge Cases
1. **Partitioned indexes (Enterprise Edition only):** Capture partition scheme name...
2. **Filtered indexes with complex predicates:** Preserve complete WHERE clause...

## Non-Functional Requirements

### Performance
- Response time: < 100ms per call (p95 and p99)
- Batch performance: < 5 seconds for 100 indexes

### Security
- Authentication: Inherits caller's SQL authentication
- SQL injection prevention: QUOTENAME() + sp_executesql

...
```

**What your output will become:**
Parent skill will insert your output into story-template.md at line 45:

```markdown
---
id: STORY-009
title: Index Characteristic Preservation
epic: EPIC-002
...
---

## User Story
{YOUR OUTPUT: User Story section}

## Acceptance Criteria
{YOUR OUTPUT: Acceptance Criteria section}

## Technical Specification
{Generated by Phase 3}

...
```

**Final result:** Single .story.md file at devforgeai/specs/Stories/STORY-009-index-characteristic-preservation.story.md
```

---

## Self-Validation Checklist (Subagent Internal)

All subagents should self-validate output before returning:

```markdown
## Step N: Self-Validate Output (Before Returning)

**Objective:** Ensure output complies with constraints before sending to parent skill.

**Validation checklist:**
```python
# 1. Check format
assert isinstance(output, str), "Output must be string (markdown text)"
assert not output.startswith("File:"), "Output cannot be file path"
assert "Created file:" not in output, "Output cannot contain file creation statements"

# 2. Check for prohibited file types
prohibited_files = [
    "SUMMARY.md",
    "QUICK-START.md",
    "VALIDATION-CHECKLIST.md",
    "FILE-INDEX.md",
    "DELIVERY-SUMMARY.md"
]

for filename in prohibited_files:
    assert filename not in output, f"Output contains prohibited file reference: {filename}"

# 3. Check required sections (skill-specific)
required_sections = {skill_specific_sections}  # e.g., ["User Story", "Acceptance Criteria"]

for section in required_sections:
    assert f"## {section}" in output, f"Missing required section: {section}"

# 4. Check size
assert len(output) <= {max_chars}, f"Output too large: {len(output)} chars (max: {max_chars})"

# 5. Check for tool usage violations
prohibited_tool_indicators = [
    "Write(file_path=",
    "Edit(file_path=",
    "Bash(command=\"cat >",
    "Bash(command=\"echo >"
]

for indicator in prohibited_tool_indicators:
    assert indicator not in output, f"Output contains prohibited tool usage: {indicator}"

# 6. Log validation result
Display: """
✓ Subagent Self-Validation: PASS

Output format: Markdown text ✅
File creation: None ✅
Required sections: {len(required_sections)}/{len(required_sections)} ✅
Size: {len(output)} chars (< {max_chars}) ✅
Tool violations: None ✅

Returning output to parent skill...
"""
```
```

---

## Prompt Enhancement Procedure

### Step 1: Identify Parent Skill

For each subagent:
1. Grep for subagent name in skill files:
   ```bash
   grep -r "subagent_type=\"{subagent_name}\"" .claude/skills/
   ```

2. Identify parent skills and phases:
   - requirements-analyst → devforgeai-story-creation (Phase 2), devforgeai-orchestration (Phase 3)
   - api-designer → devforgeai-story-creation (Phase 3), devforgeai-architecture (Phase 4)

3. Determine expected output format:
   - Story creation: Markdown sections for assembly
   - Architecture: OpenAPI YAML, data models
   - Testing: Test code snippets

---

### Step 2: Analyze Template/Assembly Logic

**Read parent skill's assembly logic:**
```python
# Example: devforgeai-story-creation Phase 5
Read(".claude/skills/devforgeai-story-creation/references/story-file-creation.md")

# Find assembly logic
# Example: "Insert acceptance criteria from Phase 2 at line 45 in template"
```

**Understand how output is used:**
- Where does subagent output get inserted?
- What format is expected?
- Are there size limits?
- What happens if output is missing sections?

---

### Step 3: Create Enhanced Prompt

**Use the 4-section template:**

1. Pre-Flight Briefing (who invokes you, what they'll do with your output)
2. Output Constraints (format, size, structure, prohibited files)
3. Prohibited Actions (8 forbidden operations)
4. Output Format Examples (show exactly what expected)

**Insert in subagent invocation:**
```python
# In parent skill's reference file (e.g., requirements-analysis.md)

Task(
    subagent_type="requirements-analyst",
    description="Generate user story content",
    prompt=f"""
    {pre_flight_briefing}

    {output_constraints}

    {prohibited_actions}

    {output_format_examples}

    ---

    Now proceed with requirements analysis:

    **Feature Description:** {feature_description}
    **Story Metadata:**
    - Story ID: {story_id}
    - Epic: {epic_id}
    - Priority: {priority}
    - Points: {points}

    Generate the following sections as markdown text (NOT files):
    1. User Story (As a/I want/So that)
    2. Acceptance Criteria (Given/When/Then, minimum 3)
    3. Edge Cases (minimum 2)
    4. Data Validation Rules (if applicable)
    5. Non-Functional Requirements (Performance, Security, Reliability, Scalability - all measurable)

    Remember: Return MARKDOWN TEXT ONLY. No file creation.
    """
)
```

---

### Step 4: Add Validation After Invocation

**Immediately after subagent returns:**
```python
# Get subagent output
subagent_output = Task(...)

# Validate output format
validate_subagent_output(
    output=subagent_output,
    expected_format="markdown_text",
    prohibited_patterns=["File created:", ".md created", "SUMMARY.md"],
    required_sections=["User Story", "Acceptance Criteria"],
    max_length=50000
)

# If validation fails, re-invoke with stricter prompt
if validation_failed:
    subagent_output = Task(
        prompt=f"""
        **STRICT MODE - SECOND ATTEMPT**

        Previous invocation violated output constraints.
        This is your second attempt.

        {original_prompt with enhanced warnings}

        CRITICAL: Return markdown TEXT only. NO file creation whatsoever.
        """
    )

# If second attempt also fails, HALT
if second_validation_failed:
    HALT: "Subagent repeatedly violates output constraints. Manual intervention required."
```

---

## Implementation Guide (Per Subagent)

### For requirements-analyst

**Parent Skills:**
- devforgeai-story-creation (Phase 2)
- devforgeai-orchestration (Phase 3 - epic feature decomposition)

**Expected Output:** Markdown sections (User Story, AC, Edge Cases, NFRs)

**Enhancement:**
```python
# File: .claude/skills/devforgeai-story-creation/references/requirements-analysis.md
# Step 2.1: Invoke Requirements Analyst Subagent

Task(
    subagent_type="requirements-analyst",
    description="Generate user story content",
    prompt="""
    **PRE-FLIGHT BRIEFING:**
    You are being invoked by the devforgeai-story-creation skill.
    This skill will assemble your output into a single .story.md file using story-template.md.

    **YOUR ROLE:**
    - Generate requirements content (user story, acceptance criteria, edge cases, NFRs)
    - Return content as markdown sections
    - Do NOT create files
    - Parent skill handles file creation (Phase 5: Story File Creation)

    **OUTPUT WILL BE USED IN:**
    - Phase 5: Story File Creation (assembly into story-template.md)
    - Your output is CONTENT for assembly, not a complete deliverable

    **WORKFLOW CONTEXT:**
    - Current workflow: Story creation (8-phase process)
    - Current phase: Phase 2 (Requirements Analysis)
    - Next phase: Phase 3 (Technical Specification)
    - Final artifact: devforgeai/specs/Stories/{STORY-ID}-{slug}.story.md

    ---

    **CRITICAL OUTPUT CONSTRAINTS:**

    1. **Format:** Return ONLY markdown text content (no file creation)
    2. **Content:** Output will be inserted into story-template.md by parent skill
    3. **Files:** Do NOT create separate files (SUMMARY.md, QUICK-START.md, VALIDATION-CHECKLIST.md, FILE-INDEX.md, DELIVERY-SUMMARY.md)
    4. **Structure:** Output as sections: User Story, Acceptance Criteria, Edge Cases, Data Validation Rules, Non-Functional Requirements
    5. **Assembly:** Parent skill (devforgeai-story-creation) will assemble all sections into single .story.md file
    6. **Size:** Maximum 50,000 characters (fits in story-template.md capacity)

    **Contract Reference:** .claude/skills/devforgeai-story-creation/contracts/requirements-analyst-contract.yaml

    ---

    **PROHIBITED ACTIONS:**

    You MUST NOT:
    1. ❌ Create files using Write tool
    2. ❌ Create files using Edit tool on non-existent files
    3. ❌ Create files using Bash with output redirection (>, >>, cat <<EOF)
    4. ❌ Return file paths as output (e.g., "Created: STORY-009-summary.md")
    5. ❌ Return file creation statements (e.g., "File created successfully")
    6. ❌ Generate multi-file deliverables (SUMMARY, QUICK-START, INDEX, etc.)
    7. ❌ Write to disk in any form
    8. ❌ Create comprehensive project structures (you generate CONTENT, not PROJECTS)

    **Why prohibited:**
    - Parent skill handles all file creation (Phase 5: Story File Creation)
    - Your output is assembled with other content (tech spec, UI spec)
    - Multi-file output violates DevForgeAI single-file design
    - Creates framework specification violations (RCA-007)

    **What to do instead:**
    - ✅ Return markdown text as string
    - ✅ Structure content with section headers (## User Story, ## Acceptance Criteria, etc.)
    - ✅ Include all required information in text output
    - ✅ Let parent skill decide file structure and naming

    ---

    **EXPECTED OUTPUT FORMAT:**

    Your output should look like this (MARKDOWN TEXT, not files):

    ```markdown
    ## User Story
    **As a** [role - specific persona, not "user"],
    **I want** [action - what functionality],
    **so that** [benefit - business value].

    ## Acceptance Criteria

    ### AC1: [Clear, testable title]
    **Given** [context - initial state]
    **When** [action - what happens]
    **Then** [outcome - expected result]

    ### AC2: [Title]
    **Given** [context]
    **When** [action]
    **Then** [outcome]

    (Minimum 3 acceptance criteria)

    ## Edge Cases
    1. **[Edge case scenario]:** [Description and expected behavior]
    2. **[Edge case scenario]:** [Description]

    (Minimum 2 edge cases)

    ## Data Validation Rules
    1. **[Input parameter]:** [Validation rule]
    2. **[Data format]:** [Validation rule]

    (Optional section)

    ## Non-Functional Requirements

    ### Performance
    - Response time: [MEASURABLE - e.g., "< 100ms per request (p95)"]
    - Throughput: [MEASURABLE - e.g., "1000 requests/second"]

    ### Security
    - Authentication: [SPECIFIC - e.g., "JWT tokens with 15-min expiry"]
    - Authorization: [SPECIFIC - e.g., "RBAC with admin/user roles"]

    ### Reliability
    - Error handling: [SPECIFIC - e.g., "Return 400 with error details"]

    ### Scalability
    - Concurrency: [MEASURABLE - e.g., "10,000 concurrent users"]
    ```

    **What your output will become:**
    Parent skill will insert your output into story-template.md at line 45:

    ```markdown
    ---
    id: {story_id}
    title: {title}
    ...
    ---

    ## User Story
    {YOUR OUTPUT: User Story section}

    ## Acceptance Criteria
    {YOUR OUTPUT: Acceptance Criteria section}

    ## Technical Specification
    {Generated by Phase 3 - api-designer or manual}

    ## Non-Functional Requirements
    {YOUR OUTPUT: NFRs section}

    ## Edge Cases
    {YOUR OUTPUT: Edge Cases section}

    ...
    ```

    **Final result:** Single .story.md file at devforgeai/specs/Stories/{story_id}-{slug}.story.md

    ---

    **Now proceed with requirements analysis:**

    **Feature Description:** {feature_description}

    **Story Metadata:**
    - Story ID: {story_id}
    - Epic: {epic_id}
    - Priority: {priority}
    - Points: {points}

    Generate the sections as markdown text (NOT files):
    """
)
```

**Effort:** 30 minutes to enhance prompt

---

### For api-designer

**Parent Skills:**
- devforgeai-story-creation (Phase 3 - conditional)
- devforgeai-architecture (Phase 4 - API specifications)

**Expected Output:** OpenAPI 3.0 YAML specification (text, not file)

**Enhancement:**
```python
# File: .claude/skills/devforgeai-story-creation/references/technical-specification-creation.md
# Step 3.2: Invoke API Designer Subagent (if API detected)

Task(
    subagent_type="api-designer",
    description="Generate API contract",
    prompt="""
    **PRE-FLIGHT BRIEFING:**
    You are being invoked by the devforgeai-story-creation skill.
    This skill will embed your API specification into the Technical Specification section of .story.md.

    **YOUR ROLE:**
    - Generate OpenAPI 3.0 specification
    - Return specification as YAML text
    - Do NOT create files
    - Parent skill embeds this in story document (Phase 5)

    **OUTPUT WILL BE USED IN:**
    - Phase 5: Story File Creation (embedded in Technical Specification section)
    - Your output is CONTENT for embedding, not a standalone API spec file

    **WORKFLOW CONTEXT:**
    - Current workflow: Story creation (8-phase process)
    - Current phase: Phase 3 (Technical Specification)
    - Next phase: Phase 4 (UI Specification)
    - Final artifact: devforgeai/specs/Stories/{STORY-ID}-{slug}.story.md

    ---

    **CRITICAL OUTPUT CONSTRAINTS:**

    1. **Format:** Return ONLY OpenAPI 3.0 YAML text (no file creation)
    2. **Content:** Output will be embedded in Technical Specification section of .story.md
    3. **Files:** Do NOT create separate files (api-spec.yaml, endpoints.md, schemas.md, models.md)
    4. **Structure:** Single OpenAPI YAML document with paths, components, security, info
    5. **Assembly:** Parent skill will wrap this in ```yaml code fence and insert into story
    6. **Size:** Maximum 30,000 characters (fits in story technical spec section)

    **Contract Reference:** .claude/skills/devforgeai-story-creation/contracts/api-designer-contract.yaml

    ---

    **PROHIBITED ACTIONS:**

    You MUST NOT:
    1. ❌ Create api-spec.yaml file
    2. ❌ Create separate schema files (user-schema.yaml, etc.)
    3. ❌ Create endpoint documentation files (endpoints.md)
    4. ❌ Return file paths (e.g., "Created: api-spec.yaml")
    5. ❌ Use Write or Edit tools
    6. ❌ Use Bash for file creation
    7. ❌ Generate multi-file API documentation
    8. ❌ Create Postman collections or other artifacts

    **What to do instead:**
    - ✅ Return OpenAPI YAML as text string
    - ✅ Include all schemas inline (components.schemas section)
    - ✅ Document all endpoints in single YAML
    - ✅ Let parent skill embed this in story document

    ---

    **EXPECTED OUTPUT FORMAT:**

    Your output should look like this (YAML TEXT, not files):

    ```yaml
    openapi: 3.0.0
    info:
      title: {Feature Name} API
      version: 1.0.0

    paths:
      /api/endpoint:
        post:
          summary: {Description}
          requestBody:
            content:
              application/json:
                schema:
                  $ref: '#/components/schemas/RequestModel'
          responses:
            200:
              description: Success
              content:
                application/json:
                  schema:
                    $ref: '#/components/schemas/ResponseModel'

    components:
      schemas:
        RequestModel:
          type: object
          properties:
            field1: {type: string}
            field2: {type: integer}

        ResponseModel:
          type: object
          properties:
            result: {type: string}
    ```

    **What your output will become:**
    Parent skill will embed your YAML in Technical Specification section:

    ```markdown
    ## Technical Specification

    ### API Contract

    ```yaml
    {YOUR OUTPUT: OpenAPI YAML specification}
    ```

    ### Data Models
    (Extracted from your components.schemas)

    ### Business Rules
    (Generated by skill based on your API design)
    ```

    **Final result:** Single .story.md file with embedded API spec

    ---

    **Now proceed with API design:**

    **Feature Description:** {feature_description}
    **Acceptance Criteria:** {acceptance_criteria}
    **Data Models:** {data_models_from_phase_2}

    Generate OpenAPI 3.0 YAML specification as text (NOT file):
    """
)
```

**Effort:** 30 minutes

---

## Rollout Strategy

### Phase 1: requirements-analyst Only (Week 1)

**Scope:** Update requirements-analyst invocations in:
- `.claude/skills/devforgeai-story-creation/references/requirements-analysis.md`
- `.claude/skills/devforgeai-orchestration/references/epic-management.md` (Phase 3)

**Testing:** Create 5 stories, verify no extra files

**Success Metric:** 0 extra files created (100% compliance)

---

### Phase 2: api-designer (Week 2)

**Scope:** Update api-designer invocations in:
- `.claude/skills/devforgeai-story-creation/references/technical-specification-creation.md`
- `.claude/skills/devforgeai-architecture/references/technical-specification-workflow.md`

**Testing:** Create 3 API stories, verify embedded YAML (not separate files)

**Success Metric:** 0 api-spec.yaml files created, YAML embedded in .story.md

---

### Phase 3: All Subagents (Week 3-4)

**Scope:** Audit and update all subagents invoked by skills:
- test-automator (if invoked expecting content)
- backend-architect (if invoked expecting code snippets)
- frontend-developer (if invoked expecting component code)

**Testing:** Comprehensive regression testing

**Success Metric:** 100% of skill-invoked subagents return content (not files)

---

## Validation Script

**Create:** `.claude/scripts/validate-subagent-output.py`

```python
#!/usr/bin/env python3
"""
Validate subagent output compliance with RCA-007 constraints.

Usage:
    python .claude/scripts/validate-subagent-output.py <subagent_output_file>
"""

import re
import sys
import yaml

def validate_output(output_text, contract_path=None):
    """Validate subagent output against constraints."""
    violations = []

    # Check 1: File creation indicators
    file_creation_patterns = [
        r"File created:",
        r"\.md created",
        r"STORY-\d+-.*\.md",
        r"Writing to file",
        r"Saved to disk",
        r"Created file:",
        r"Successfully wrote",
        r"SUMMARY\.md",
        r"QUICK-START\.md",
        r"VALIDATION-CHECKLIST\.md",
        r"FILE-INDEX\.md",
        r"DELIVERY-SUMMARY\.md"
    ]

    for pattern in file_creation_patterns:
        if re.search(pattern, output_text, re.IGNORECASE):
            violations.append({
                "type": "FILE_CREATION",
                "pattern": pattern,
                "severity": "CRITICAL"
            })

    # Check 2: Tool usage violations
    prohibited_tools = [
        r"Write\(file_path=",
        r"Edit\(file_path=",
        r"Bash\(command=\"cat >",
        r"Bash\(command=\"echo >"
    ]

    for tool in prohibited_tools:
        if re.search(tool, output_text):
            violations.append({
                "type": "TOOL_USAGE",
                "tool": tool,
                "severity": "HIGH"
            })

    # Check 3: Contract compliance (if contract provided)
    if contract_path:
        with open(contract_path, 'r') as f:
            contract = yaml.safe_load(f)

        # Validate required sections
        if 'output_sections' in contract:
            for section_name, section_spec in contract['output_sections'].items():
                if section_spec.get('required', False):
                    section_header = section_name.replace('_', ' ').title()
                    if f"## {section_header}" not in output_text:
                        violations.append({
                            "type": "MISSING_SECTION",
                            "section": section_header,
                            "severity": "HIGH"
                        })

        # Validate size constraint
        max_length = contract.get('max_output_length', 50000)
        if len(output_text) > max_length:
            violations.append({
                "type": "SIZE_EXCEEDED",
                "actual": len(output_text),
                "max": max_length,
                "severity": "MEDIUM"
            })

    # Return validation result
    if violations:
        return {
            "status": "FAILED",
            "violations": violations,
            "violation_count": len(violations)
        }
    else:
        return {
            "status": "PASSED",
            "violations": [],
            "violation_count": 0
        }

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python validate-subagent-output.py <output_file> [contract_yaml]")
        sys.exit(1)

    output_file = sys.argv[1]
    contract_file = sys.argv[2] if len(sys.argv) > 2 else None

    with open(output_file, 'r') as f:
        output_text = f.read()

    result = validate_output(output_text, contract_file)

    if result['status'] == "PASSED":
        print("✓ Validation PASSED")
        print(f"  Output compliant with RCA-007 constraints")
        sys.exit(0)
    else:
        print(f"✗ Validation FAILED ({result['violation_count']} violations)")
        for v in result['violations']:
            print(f"  [{v['severity']}] {v['type']}: {v.get('pattern', v.get('section', v.get('tool', 'N/A')))}")
        sys.exit(1)
```

**Usage:**
```bash
# Validate subagent output file
python .claude/scripts/validate-subagent-output.py subagent-output.txt

# Validate with contract
python .claude/scripts/validate-subagent-output.py \
    subagent-output.txt \
    .claude/skills/devforgeai-story-creation/contracts/requirements-analyst-contract.yaml
```

---

## Monitoring & Logging

### Violation Log Format

**File:** `.devforgeai/logs/rca-007-violations.log`

```
[VIOLATION DETECTED]
Timestamp: 2025-11-06T15:30:45Z
Story ID: STORY-009
Subagent: requirements-analyst
Parent Skill: devforgeai-story-creation
Phase: Phase 2 (Requirements Analysis)
Violation Type: FILE_CREATION
Pattern Matched: "File created:"
Output Snippet: "File created: STORY-009-SUMMARY.md..."
Recovery Action: Re-invoke with STRICT MODE
Recovery Result: SUCCESS (second attempt compliant)
---

[VIOLATION DETECTED]
Timestamp: 2025-11-06T16:15:22Z
Story ID: STORY-010
Subagent: api-designer
Parent Skill: devforgeai-story-creation
Phase: Phase 3 (Technical Specification)
Violation Type: FILE_CREATION
Pattern Matched: "api-spec.yaml"
Output Snippet: "Created api-spec.yaml with 250 lines..."
Recovery Action: Re-invoke with STRICT MODE
Recovery Result: FAILED (manual intervention required)
---
```

**Log analysis:**
```bash
# Count violations
grep -c "VIOLATION DETECTED" .devforgeai/logs/rca-007-violations.log

# Count by subagent
grep "Subagent:" .devforgeai/logs/rca-007-violations.log | sort | uniq -c

# Count by violation type
grep "Violation Type:" .devforgeai/logs/rca-007-violations.log | sort | uniq -c

# Check recovery success rate
total=$(grep -c "Recovery Action" .devforgeai/logs/rca-007-violations.log)
success=$(grep -c "Recovery Result: SUCCESS" .devforgeai/logs/rca-007-violations.log)
rate=$((success * 100 / total))
echo "Recovery success rate: ${rate}%"
```

---

## Success Metrics

### Prompt Enhancement Success

**Per subagent:**
- [ ] Prompt includes all 4 sections (briefing, constraints, prohibited, examples)
- [ ] Pre-flight briefing explains workflow context
- [ ] Output constraints specify exact format expected
- [ ] Prohibited actions list 8 forbidden operations
- [ ] Output examples show exact structure
- [ ] Prompt tested with actual invocation → No files created

**Framework-wide:**
- [ ] All skill-invoked subagents updated (requirements-analyst, api-designer)
- [ ] Zero extra files created in testing (30 test cases)
- [ ] Violation detection catches 100% of file creation attempts
- [ ] Recovery re-invocation succeeds 90%+ of the time

---

## Documentation Updates

**After implementation:**

1. Update `.claude/agents/requirements-analyst.md`:
   - Add "Output Contract" section
   - Document expected behavior when invoked by skills
   - Link to contract YAML files

2. Update `.claude/agents/api-designer.md`:
   - Add "Output Contract" section
   - Document YAML-only return format
   - Specify no file creation allowed

3. Update `.claude/memory/subagents-reference.md`:
   - Add "Subagent Output Contracts" section
   - Document RCA-007 fix and prompt enhancements
   - Link to validation script

4. Update `CLAUDE.md`:
   - Add RCA-007 to resolved issues
   - Document prompt enhancement pattern

---

## Related Documents

- **RCA:** `.devforgeai/RCA/RCA-007-multi-file-story-creation.md`
- **Implementation Plan:** `.devforgeai/specs/enhancements/RCA-007-FIX-IMPLEMENTATION-PLAN.md`
- **Contract Spec:** `.devforgeai/specs/enhancements/YAML-CONTRACT-SPECIFICATION.md` (next document)
- **Lean Orchestration:** `.devforgeai/protocols/lean-orchestration-pattern.md`

---

**Implementation Status:** Specification Complete - Ready for Phase 1 (Week 1)
**Priority:** HIGH (critical for RCA-007 fix)
**Dependencies:** None (can start immediately)
