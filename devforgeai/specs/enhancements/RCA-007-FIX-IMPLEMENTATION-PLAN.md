# RCA-007 Fix Implementation Plan

**Date:** 2025-11-06
**Issue:** Multi-File Story Creation Violation
**Priority:** HIGH
**Total Effort:** 25-35 hours (3 phases)
**Status:** Ready for Implementation

---

## Executive Summary

This document provides detailed implementation instructions for fixing the multi-file story creation issue identified in RCA-007. The fix prevents the `requirements-analyst` subagent from creating 5 extra files and ensures only a single `.story.md` file is generated per story.

---

## Phase 1: Immediate Fixes (Week 1 - 2-4 hours)

### Goal
Stop multi-file creation immediately with minimal changes.

### Tasks

#### Task 1.1: Update Subagent Prompt with Output Constraints (30 minutes)

**File:** `.claude/skills/devforgeai-story-creation/references/requirements-analysis.md`

**Current Implementation (Lines ~50-80):**
```markdown
## Step 2.1: Invoke Requirements Analyst Subagent

Task(
  subagent_type="requirements-analyst",
  prompt="""Transform feature description into structured user story for DevForgeAI framework.

  **Feature Description:** {feature_description}

  **Story Metadata:**
  - Story ID: {story_id}
  - Epic: {epic_id}
  - Priority: {priority}
  - Points: {points}

  Generate:
  1. **User Story** (As a/I want/So that format)
  2. **Acceptance Criteria** (Given/When/Then format, minimum 3)
  3. **Edge Cases** (minimum 2)
  4. **Data Validation Rules**
  5. **Non-Functional Requirements**

  Output Format: Markdown with clear sections
  """
)
```

**NEW Implementation:**
```markdown
## Step 2.1: Invoke Requirements Analyst Subagent

Task(
  subagent_type="requirements-analyst",
  description="Generate user story content",
  prompt="""Transform feature description into structured user story for DevForgeAI framework.

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

  **PROHIBITED ACTIONS:**
  - Creating files (SUMMARY.md, QUICK-START.md, VALIDATION-CHECKLIST.md, FILE-INDEX.md, DELIVERY-SUMMARY.md, etc.)
  - Writing to disk (Write, Edit, Bash with output redirection)
  - Generating file paths or file references

  ---

  **CRITICAL OUTPUT CONSTRAINTS:**
  - Return ONLY markdown text content (no file creation)
  - Output will be inserted into story-template.md by parent skill
  - Do NOT create separate files
  - Structure output as sections: User Story, Acceptance Criteria, Edge Cases, Data Validation Rules, NFRs
  - Parent skill (devforgeai-story-creation) will assemble all sections into single .story.md file

  ---

  **Feature Description:** {feature_description}

  **Story Metadata:**
  - Story ID: {story_id}
  - Epic: {epic_id}
  - Priority: {priority}
  - Points: {points}

  Generate the following sections as markdown text (NOT files):

  1. **User Story** (As a/I want/So that format)
  2. **Acceptance Criteria** (Given/When/Then format, minimum 3)
  3. **Edge Cases** (minimum 2)
  4. **Data Validation Rules**
  5. **Non-Functional Requirements** (Performance, Security, Reliability, Scalability - all measurable)

  **Output Format:** Markdown sections with clear headers (NOT file paths, NOT file creation statements)

  **Example Output Structure:**
  ```markdown
  ## User Story
  **As a** [role],
  **I want** [action],
  **so that** [benefit].

  ## Acceptance Criteria

  ### AC1: [Title]
  **Given** [context]
  **When** [action]
  **Then** [outcome]

  ...

  ## Edge Cases
  1. [Edge case 1]
  2. [Edge case 2]

  ## Non-Functional Requirements

  ### Performance
  - Target: [measurable metric]

  ### Security
  - Target: [measurable metric]

  ...
  ```

  Now generate the requirements content (markdown sections only, no files):
  """
)
```

**Validation:** Test with actual subagent invocation, verify no files created.

---

#### Task 1.2: Add Output Validation Checkpoint (1-2 hours)

**File:** `.claude/skills/devforgeai-story-creation/references/requirements-analysis.md`

**Add NEW Step 2.2 after subagent invocation:**

```markdown
## Step 2.2: Validate Subagent Output Format (NEW - RCA-007 Fix)

**Objective:** Ensure subagent returned markdown content, not file artifacts.

**Validation Procedure:**

### Check 1: File Creation Detection

**Search for file creation indicators:**
```python
file_creation_patterns = [
    r"File created:",
    r"\.md created",
    r"STORY-\d+-.*\.md",
    r"Writing to file",
    r"Saved to disk",
    r"Created file:",
    r"Successfully wrote",
    r"Document generated:",
    r"SUMMARY\.md",
    r"QUICK-START\.md",
    r"VALIDATION-CHECKLIST\.md",
    r"FILE-INDEX\.md",
    r"DELIVERY-SUMMARY\.md"
]

subagent_output_text = subagent_result

for pattern in file_creation_patterns:
    if re.search(pattern, subagent_output_text, re.IGNORECASE):
        # VIOLATION DETECTED
        ERROR: Subagent created files instead of returning content
        Pattern matched: {pattern}

        # Log violation
        Write(
            file_path=".devforgeai/logs/rca-007-violations.log",
            content=f"""
            [VIOLATION DETECTED]
            Timestamp: {datetime.now()}
            Story ID: {story_id}
            Subagent: requirements-analyst
            Pattern matched: {pattern}
            Output snippet: {subagent_output_text[:500]}
            ---
            """
        )

        # Recovery: Re-invoke with stricter prompt
        Display: """
        ⚠️ Subagent Output Violation Detected

        The requirements-analyst subagent attempted to create files instead of returning content.
        This violates the devforgeai-story-creation workflow specification.

        Recovery: Re-invoking subagent with stricter output constraints...
        """

        # Re-invoke with enhanced prompt (add "STRICT MODE" marker)
        Task(
            subagent_type="requirements-analyst",
            prompt="""
            **STRICT MODE - NO FILE CREATION**

            Previous invocation violated output constraints by creating files.
            This invocation is STRICTLY content-only.

            {original_prompt with enhanced constraints}

            REMINDER: Return markdown TEXT only. NO file creation allowed.
            """
        )

        # If second attempt also fails, HALT
        if second_attempt_also_creates_files:
            HALT: "Subagent repeatedly violates output constraints. Manual intervention required."
            Exit Phase 2
```

### Check 2: Required Sections Validation

**Verify all required sections present:**
```python
required_sections = [
    "User Story",
    "Acceptance Criteria",
    "Edge Cases",
    "Non-Functional Requirements"
]

missing_sections = []

for section in required_sections:
    if section not in subagent_output_text:
        missing_sections.append(section)

if missing_sections:
    ERROR: Subagent output incomplete
    Missing sections: {missing_sections}

    # Recovery: AskUserQuestion to fill gaps or re-invoke
    AskUserQuestion:
        question: f"Subagent output is missing sections: {missing_sections}. How should I proceed?"
        options:
            - "Re-invoke subagent" → Task(subagent_type="requirements-analyst", ...)
            - "Manually provide content" → AskUserQuestion for each missing section
            - "Skip missing sections" → Continue with warning (not recommended)
```

### Check 3: Acceptance Criteria Format

**Validate Given/When/Then format:**
```python
# Extract acceptance criteria section
ac_section = extract_section(subagent_output_text, "Acceptance Criteria")

# Check for Given/When/Then keywords
required_keywords = ["Given", "When", "Then"]

ac_count = ac_section.count("### AC")  # Count criteria

if ac_count < 3:
    WARNING: Less than 3 acceptance criteria (DevForgeAI minimum)
    Actual: {ac_count}

for keyword in required_keywords:
    if keyword not in ac_section:
        WARNING: Acceptance criteria missing "{keyword}" keywords
        Suggest: Ensure all AC follow Given/When/Then format
```

### Validation Summary

**Display validation results:**
```
✓ Phase 2 Validation Complete

Results:
- File creation check: PASS (no files created)
- Required sections: PASS (all 4 sections present)
- Acceptance criteria: PASS (5 criteria, all Given/When/Then format)

Proceeding to Phase 3: Technical Specification
```

**If validation fails:**
```
✗ Phase 2 Validation FAILED

Issues:
- File creation check: FAIL (detected SUMMARY.md creation)
- Required sections: PASS
- Acceptance criteria: WARNING (only 2 criteria, need minimum 3)

Recovery actions taken:
- Re-invoked subagent with stricter constraints
- Second attempt validation: PASS

Proceeding to Phase 3
```
```

**Effort:** 1-2 hours (including testing)

---

#### Task 1.3: Testing Phase 1 Fixes (30 minutes)

**Test Case 1: Single Story Creation**
```bash
# Test command
/create-story User authentication with JWT tokens

# Expected behavior:
# 1. Subagent receives constrained prompt
# 2. Subagent returns markdown content only
# 3. Validation passes (no file creation detected)
# 4. Only 1 file created: STORY-XXX-user-authentication-jwt-tokens.story.md

# Assertions:
ls devforgeai/specs/Stories/STORY-*.md | wc -l  # Should increase by 1
ls devforgeai/specs/Stories/STORY-*-SUMMARY.md  # Should NOT exist
ls devforgeai/specs/Stories/STORY-*-QUICK-START.md  # Should NOT exist
```

**Test Case 2: Validation Catches Violation (Simulated)**

Manually trigger violation by modifying subagent prompt to create files:
```bash
# Simulate violation
# (Temporarily modify requirements-analyst.md to create files)

/create-story Test validation checkpoint

# Expected behavior:
# 1. Subagent creates files (violation)
# 2. Validation detects file creation patterns
# 3. Recovery re-invokes subagent
# 4. Second attempt succeeds
# 5. Only 1 .story.md file remains

# Assertions:
ls .devforgeai/logs/rca-007-violations.log  # Violation logged
cat .devforgeai/logs/rca-007-violations.log | grep "Pattern matched"  # Has violation entry
```

**Success Criteria:**
- [ ] Test Case 1: Only 1 .story.md file created
- [ ] Test Case 2: Validation detects and recovers from violations
- [ ] No SUMMARY, QUICK-START, VALIDATION-CHECKLIST, FILE-INDEX files created
- [ ] Violation log created and populated (when violation occurs)

---

## Phase 2: Short-Term Improvements (Week 2 - 5-7 hours)

### Goal
Add contract-based validation and file system monitoring.

### Tasks

#### Task 2.1: Create Subagent-Skill Contract (3-4 hours)

**Create NEW File:** `.claude/skills/devforgeai-story-creation/contracts/requirements-analyst-contract.yaml`

```yaml
# Contract: devforgeai-story-creation <-> requirements-analyst
# Version: 1.0
# Date: 2025-11-06
# Purpose: Define expected input/output format between skill and subagent

skill: devforgeai-story-creation
subagent: requirements-analyst
phase: "Phase 2: Requirements Analysis"
rca_reference: RCA-007

# Input specification
input:
  feature_description:
    type: string
    min_length: 10
    description: "Feature description from user or epic"

  story_metadata:
    story_id:
      type: string
      pattern: "^STORY-\\d{3}$"
      example: "STORY-042"

    epic_id:
      type: string
      pattern: "^EPIC-\\d{3}$|null"
      example: "EPIC-002"
      optional: true

    priority:
      type: enum
      values: ["Critical", "High", "Medium", "Low"]

    points:
      type: integer
      values: [1, 2, 3, 5, 8, 13]

# Output specification
output_format: markdown_content  # NOT file paths, NOT file artifacts
output_type: text/markdown
max_output_length: 50000  # Characters (fits in Phase 5 assembly)

output_sections:
  user_story:
    format: "As a [role], I want [action], so that [benefit]"
    required: true

  acceptance_criteria:
    format: "array of Given/When/Then scenarios"
    min_count: 3
    structure:
      - title: string
      - given: string
      - when: string
      - then: string
    required: true

  edge_cases:
    format: "array of edge case descriptions"
    min_count: 2
    required: true

  data_validation_rules:
    format: "array of validation rules"
    required: false

  nfrs:
    format: "object with performance, security, reliability, scalability"
    required: true
    structure:
      performance:
        target: string (measurable)
        example: "< 100ms response time"
      security:
        target: string (measurable)
        example: "SQL injection prevention via parameterized queries"
      reliability:
        target: string (measurable)
        example: "99.9% uptime"
      scalability:
        target: string (measurable)
        example: "Support 10,000 concurrent users"

# Constraints (CRITICAL - RCA-007 Fix)
constraints:
  no_file_creation:
    enabled: true
    description: "Subagent MUST NOT create files"
    prohibited_tools: ["Write", "Edit", "Bash(with output redirection)"]

  content_only:
    enabled: true
    description: "Return text content, not file references"

  single_output:
    enabled: true
    description: "Return single markdown text block, not multiple files"

  max_output_length:
    value: 50000
    description: "Output must fit in Phase 5 assembly (story-template.md capacity)"

# Validation rules
validation:
  check_sections_present:
    enabled: true
    required_sections: ["User Story", "Acceptance Criteria", "Edge Cases", "Non-Functional Requirements"]

  check_no_file_paths:
    enabled: true
    prohibited_patterns:
      - "File created:"
      - "\\.md created"
      - "STORY-\\d+-.*\\.md"
      - "Writing to file"
      - "Saved to disk"
      - "SUMMARY\\.md"
      - "QUICK-START\\.md"
      - "VALIDATION-CHECKLIST\\.md"
      - "FILE-INDEX\\.md"
      - "DELIVERY-SUMMARY\\.md"

  check_ac_format:
    enabled: true
    required_keywords: ["Given", "When", "Then"]
    min_count: 3

  check_nfr_measurability:
    enabled: true
    prohibited_vague_terms: ["fast", "secure", "scalable", "performant", "reliable"]
    description: "All NFRs must have measurable targets"

# Error handling
error_handling:
  on_file_creation_detected:
    action: "re_invoke"
    max_retries: 2
    fallback: "HALT with manual intervention required"

  on_missing_sections:
    action: "ask_user_question"
    options: ["Re-invoke subagent", "Manually provide content", "Skip with warning"]

  on_invalid_format:
    action: "re_invoke"
    max_retries: 1
    fallback: "ask_user_question"

# Monitoring
monitoring:
  log_violations:
    enabled: true
    log_path: ".devforgeai/logs/rca-007-violations.log"

  track_retries:
    enabled: true
    max_retries_before_alert: 2

  performance_tracking:
    enabled: true
    warn_if_execution_exceeds: "5 minutes"

# Version history
changelog:
  - version: "1.0"
    date: "2025-11-06"
    changes: "Initial contract definition for RCA-007 fix"
    author: "DevForgeAI Framework"
```

**Effort:** 3-4 hours (including validation logic implementation)

---

#### Task 2.2: Implement Contract Validation in Skill (1 hour)

**File:** `.claude/skills/devforgeai-story-creation/references/requirements-analysis.md`

**Add NEW Step 2.3 (after Step 2.2 output validation):**

```markdown
## Step 2.3: Validate Against Contract (NEW - RCA-007 Contract Enforcement)

**Objective:** Enforce subagent-skill contract specifications.

**Load contract:**
```python
contract_path = ".claude/skills/devforgeai-story-creation/contracts/requirements-analyst-contract.yaml"
contract = Read(file_path=contract_path)

# Parse YAML
import yaml
contract_spec = yaml.safe_load(contract)
```

**Validate constraints:**
```python
# Constraint 1: No file creation
if contract_spec['constraints']['no_file_creation']['enabled']:
    prohibited_patterns = contract_spec['validation']['check_no_file_paths']['prohibited_patterns']

    for pattern in prohibited_patterns:
        if re.search(pattern, subagent_output, re.IGNORECASE):
            ERROR: Contract violation - File creation detected
            Pattern: {pattern}
            Contract: {contract_spec['constraints']['no_file_creation']}

            # Apply error handling from contract
            error_action = contract_spec['error_handling']['on_file_creation_detected']['action']

            if error_action == "re_invoke":
                max_retries = contract_spec['error_handling']['on_file_creation_detected']['max_retries']
                # Re-invoke logic (up to max_retries)

# Constraint 2: Required sections
if contract_spec['validation']['check_sections_present']['enabled']:
    required_sections = contract_spec['validation']['check_sections_present']['required_sections']

    missing = [s for s in required_sections if s not in subagent_output]

    if missing:
        ERROR: Contract violation - Missing required sections: {missing}

        # Apply error handling
        error_action = contract_spec['error_handling']['on_missing_sections']['action']

        if error_action == "ask_user_question":
            # AskUserQuestion logic

# Constraint 3: AC format
if contract_spec['validation']['check_ac_format']['enabled']:
    min_count = contract_spec['validation']['check_ac_format']['min_count']
    required_keywords = contract_spec['validation']['check_ac_format']['required_keywords']

    # Validate AC count and format

# Constraint 4: NFR measurability
if contract_spec['validation']['check_nfr_measurability']['enabled']:
    prohibited_terms = contract_spec['validation']['check_nfr_measurability']['prohibited_vague_terms']

    nfr_section = extract_section(subagent_output, "Non-Functional Requirements")

    for term in prohibited_terms:
        if term in nfr_section.lower():
            WARNING: Vague NFR term detected: "{term}"
            Guidance: All NFRs must have measurable targets
            Example: "Response time < 100ms" (not "fast response")
```

**Log monitoring data:**
```python
if contract_spec['monitoring']['log_violations']['enabled']:
    log_path = contract_spec['monitoring']['log_violations']['log_path']

    if violations_detected:
        Write(
            file_path=log_path,
            content=f"""
            [CONTRACT VALIDATION]
            Timestamp: {datetime.now()}
            Story ID: {story_id}
            Contract: requirements-analyst-contract.yaml
            Violations: {violations_count}
            Details: {violation_details}
            ---
            """
        )
```

**Display contract validation results:**
```
✓ Contract Validation Complete

Contract: requirements-analyst-contract.yaml v1.0
Story ID: {story_id}

Constraints Validated:
- no_file_creation: PASS ✅
- content_only: PASS ✅
- required_sections: PASS ✅ (4/4 sections present)
- ac_format: PASS ✅ (5 criteria, Given/When/Then)
- nfr_measurability: PASS ✅ (all measurable)

Proceeding to Phase 3
```
```

**Effort:** 1 hour

---

#### Task 2.3: File System Diff Check (2-3 hours)

**File:** `.claude/skills/devforgeai-story-creation/references/requirements-analysis.md`

**Add file system monitoring BEFORE subagent invocation:**

```markdown
## Step 2.0: Pre-Invocation File System Snapshot (NEW - RCA-007 Monitoring)

**Objective:** Capture file system state before subagent execution to detect unauthorized file creation.

**Take snapshot:**
```python
# Capture current .story.md files
files_before_subagent = Glob(pattern="devforgeai/specs/Stories/STORY-*.md")

# Capture current supporting files (should be none for this story)
supporting_patterns = [
    f"devforgeai/specs/Stories/{story_id}-SUMMARY.md",
    f"devforgeai/specs/Stories/{story_id}-QUICK-START.md",
    f"devforgeai/specs/Stories/{story_id}-VALIDATION-CHECKLIST.md",
    f"devforgeai/specs/Stories/{story_id}-FILE-INDEX.md",
    f"devforgeai/specs/Stories/{story_id}-DELIVERY-SUMMARY.md"
]

supporting_files_before = []
for pattern in supporting_patterns:
    if file_exists(pattern):
        supporting_files_before.append(pattern)

# Store snapshot
snapshot = {
    "timestamp": datetime.now(),
    "story_files": files_before_subagent,
    "supporting_files": supporting_files_before,
    "total_count": len(files_before_subagent)
}
```

**After subagent invocation, add Step 2.2.5:**

```markdown
## Step 2.2.5: Post-Invocation File System Diff (NEW - RCA-007 Monitoring)

**Objective:** Detect unauthorized files created during subagent execution.

**Compare snapshots:**
```python
# Capture current state
files_after_subagent = Glob(pattern="devforgeai/specs/Stories/STORY-*.md")

supporting_files_after = []
for pattern in supporting_patterns:
    if file_exists(pattern):
        supporting_files_after.append(pattern)

# Calculate diff
new_story_files = set(files_after_subagent) - set(files_before_subagent)
new_supporting_files = set(supporting_files_after) - set(supporting_files_before)

# Check for violations
if len(new_story_files) > 0:
    WARNING: Unauthorized .story.md files created during Phase 2
    Files: {new_story_files}
    Expected: No files created (Phase 2 is content generation only)

if len(new_supporting_files) > 0:
    ERROR: Unauthorized supporting files created during Phase 2
    Files: {new_supporting_files}
    This is a CRITICAL violation of single-file design

    # Rollback: Delete unauthorized files
    for file in new_supporting_files:
        Bash(command=f"rm {file}")
        Log: Deleted unauthorized file: {file}

    # Log violation
    Write(
        file_path=".devforgeai/logs/rca-007-violations.log",
        content=f"""
        [FILE CREATION VIOLATION]
        Timestamp: {datetime.now()}
        Story ID: {story_id}
        Phase: Phase 2 (Requirements Analysis)
        Subagent: requirements-analyst
        Unauthorized files created: {new_supporting_files}
        Action taken: Files deleted (rollback)
        ---
        """
    )

    # Re-invoke with stricter constraints
    Display: """
    ⚠️ File Creation Violation Detected

    The subagent created unauthorized files during execution.
    Files created: {new_supporting_files}

    Action taken:
    - Unauthorized files deleted
    - Re-invoking subagent with STRICT MODE constraints

    Recovery in progress...
    """

    # Re-invoke (Step 2.1 with STRICT MODE)
```

**Diff summary:**
```
File System Diff Check: PASS ✅

Before subagent: {len(files_before_subagent)} .story.md files
After subagent: {len(files_after_subagent)} .story.md files
New files: 0 (as expected)

Supporting files before: 0
Supporting files after: 0
Unauthorized files: 0

Phase 2 file creation compliance: PASS ✅
```
```

**Effort:** 2-3 hours (including rollback logic)

---

## Phase 3: Long-Term Architectural Changes (Week 3-4 - 10-14 hours)

### Goal
Create skill-specific subagent for tight coupling.

### Tasks

#### Task 3.1: Create story-requirements-analyst Subagent (4-6 hours)

**Create NEW File:** `.claude/agents/story-requirements-analyst.md`

```yaml
---
name: story-requirements-analyst
description: Requirements analysis subagent specifically for devforgeai-story-creation skill. Returns CONTENT ONLY (no file creation). Enforces single-file story design principle.
parent_skill: devforgeai-story-creation
output_format: content_only
tools: [Read, Grep, Glob, AskUserQuestion]
model: haiku
contract: .claude/skills/devforgeai-story-creation/contracts/requirements-analyst-contract.yaml
---

# Story Requirements Analyst Subagent

**Purpose:** Generate user story, acceptance criteria, edge cases, and NFRs as **markdown content** (not files) for assembly into story-template.md by parent skill.

**CRITICAL:** This subagent is a CONTENT GENERATOR, not a DOCUMENT CREATOR. Your output will be assembled by the devforgeai-story-creation skill into a single .story.md file. Do NOT create files yourself.

---

## Output Contract

**Single Responsibility:** Return structured markdown sections for assembly (NOT create complete files).

**Format:** Markdown text with clear section headers
**File Creation:** STRICTLY PROHIBITED
**Target Consumer:** devforgeai-story-creation skill Phase 5 (Story File Creation)

**Contract Reference:** `.claude/skills/devforgeai-story-creation/contracts/requirements-analyst-contract.yaml`

---

## Invocation Pattern

**Parent skill provides:**
- Feature description (string, min 10 words)
- Story metadata (story_id, epic_id, priority, points)

**Subagent returns:**
- Structured markdown sections (text content, NOT file paths)
- Sections: User Story, Acceptance Criteria, Edge Cases, Data Validation Rules, NFRs

**Parent skill uses output:**
- Inserts content into story-template.md
- Assembles single .story.md file
- No post-processing required (content is final)

---

## Workflow

### Step 1: Receive Context from Parent Skill

**Extract from conversation:**
```python
# Parent skill sets these context markers before invoking subagent
feature_description = extract_from_conversation("Feature Description:")
story_id = extract_from_conversation("Story ID:")
epic_id = extract_from_conversation("Epic:")
priority = extract_from_conversation("Priority:")
points = extract_from_conversation("Points:")
```

**Validate inputs:**
```python
assert len(feature_description.split()) >= 10, "Feature description too short"
assert re.match(r"^STORY-\d{3}$", story_id), "Invalid story ID format"
assert priority in ["Critical", "High", "Medium", "Low"], "Invalid priority"
assert points in [1, 2, 3, 5, 8, 13], "Invalid story points"
```

---

### Step 2: Generate User Story

**Format:** As a/I want/So that

**Pattern:**
```markdown
## User Story

**As a** [role - who benefits],
**I want** [action - what functionality],
**so that** [benefit - why it matters].
```

**Example:**
```markdown
## User Story

**As a** database administrator,
**I want** to capture all index characteristics before rebuild operations,
**so that** performance tuning settings are preserved and data loss prevented.
```

**Validation:**
- Role is specific (not "user" - identify actual persona)
- Action is clear and measurable
- Benefit explains business value

---

### Step 3: Generate Acceptance Criteria

**Format:** Given/When/Then (minimum 3)

**Pattern:**
```markdown
## Acceptance Criteria

### AC1: [Clear, specific title]
**Given** [context - initial state]
**When** [action - what happens]
**Then** [outcome - expected result]

### AC2: [Title]
**Given** [context]
**When** [action]
**Then** [outcome]

...
```

**Requirements:**
- Minimum 3 AC (DevForgeAI standard)
- All AC testable (can verify pass/fail)
- Cover happy path + edge cases
- Each AC independent (can test in isolation)

**Example:**
```markdown
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
```

---

### Step 4: Generate Edge Cases

**Format:** Numbered list (minimum 2)

**Pattern:**
```markdown
## Edge Cases

1. **[Edge case scenario]:** [Description of edge case and expected behavior]
2. **[Edge case scenario]:** [Description]
...
```

**Requirements:**
- Minimum 2 edge cases
- Cover unusual inputs, boundary conditions, error states
- Each edge case has clear handling strategy

**Example:**
```markdown
## Edge Cases

1. **Partitioned indexes (Enterprise Edition only):** Capture partition scheme name and partition function details. Consumer must check edition before rebuild.
2. **Filtered indexes with complex predicates:** Preserve complete WHERE clause including nested conditions (e.g., "WHERE (Active = 1 AND (Type = 'A' OR Type = 'B'))").
3. **Columnstore indexes:** No key columns (return NULL for KeyColumns/IncludedColumns), DataCompression as COLUMNSTORE or COLUMNSTORE_ARCHIVE.
...
```

---

### Step 5: Generate Non-Functional Requirements

**Format:** Performance, Security, Reliability, Scalability (all MEASURABLE)

**Pattern:**
```markdown
## Non-Functional Requirements

### Performance
- Response time: [specific metric, e.g., "< 100ms per call (p95 and p99)"]
- Throughput: [specific metric, e.g., "< 5 seconds for 100 indexes"]
- No blocking: [specific constraint, e.g., "Read-only queries, no locking"]

### Security
- Authentication: [specific mechanism]
- Authorization: [specific permissions required]
- Data protection: [specific measures, e.g., "SQL injection prevention via QUOTENAME()"]
- No privilege escalation: [specific constraint]

### Reliability
- Error handling: [specific strategy, e.g., "Return NULL on errors (no exceptions)"]
- Retry logic: [specific policy or "none needed"]
- Graceful degradation: [specific behavior]

### Scalability
- Concurrency: [specific limit, e.g., "Support 10,000 concurrent callers"]
- Data volume: [specific limit, e.g., "Scales with 10,000+ indexes"]
- State management: [specific approach, e.g., "Stateless function"]
```

**CRITICAL:** All targets must be MEASURABLE. Prohibited vague terms:
- ❌ "fast", "secure", "reliable", "scalable", "performant"
- ✅ "< 100ms", "99.9% uptime", "QUOTENAME() + parameterized queries", "10,000 concurrent users"

**Example:**
```markdown
## Non-Functional Requirements

### Performance
- Response time: < 100ms per call (p95 and p99)
- Batch performance: < 5 seconds for 100 indexes
- No locking or blocking (read-only queries)

### Security
- Authentication: Inherits caller's SQL authentication
- Authorization: Requires VIEW DEFINITION on target database
- SQL injection prevention: QUOTENAME() + sp_executesql
- No privilege elevation (caller's permissions only)

### Reliability
- Error handling: Return NULL on errors (no exceptions)
- No retry logic needed (read-only, safe to retry)
- Graceful degradation on permission failures

### Scalability
- Stateless function (no session state)
- Supports concurrent callers (read-only)
- Scales with sys.indexes row count (10,000+ indexes)
```

---

### Step 6: Generate Data Validation Rules (Optional)

**Format:** Numbered list of validation rules

**Pattern:**
```markdown
## Data Validation Rules

1. **[Input parameter]:** [Validation rule]
2. **[Data format]:** [Validation rule]
...
```

**Example:**
```markdown
## Data Validation Rules

1. **Database name:** Use QUOTENAME() to prevent SQL injection
2. **FILLFACTOR value:** 0 or 1-100 (0 = use default, not invalid)
3. **Index name:** Must exist in sys.indexes for target table
4. **JSON format:** Use FOR JSON PATH (SQL 2016+) or manual construction (SQL 2012-2014)
```

---

### Step 7: Return Structured Output

**CRITICAL:** Return MARKDOWN TEXT ONLY. Do NOT create files.

**Output structure:**
```markdown
## User Story
[Content from Step 2]

## Acceptance Criteria
[Content from Step 3]

## Edge Cases
[Content from Step 4]

## Data Validation Rules
[Content from Step 6 - optional]

## Non-Functional Requirements
[Content from Step 5]
```

**Validation before returning:**
```python
# Self-check
assert "## User Story" in output
assert "## Acceptance Criteria" in output
assert "## Edge Cases" in output
assert "## Non-Functional Requirements" in output

# Count AC
ac_count = output.count("### AC")
assert ac_count >= 3, f"Only {ac_count} AC (need minimum 3)"

# Check for file creation indicators (should be none)
prohibited = ["File created", ".md created", "Writing to file", "Saved to disk"]
for term in prohibited:
    assert term not in output, f"Output contains file creation indicator: {term}"

# Check for vague NFR terms
vague_terms = ["fast", "secure", "scalable", "performant", "reliable"]
nfr_section = extract_section(output, "Non-Functional Requirements")
for term in vague_terms:
    if term in nfr_section.lower():
        WARNING: Vague NFR term detected: "{term}" - Consider making measurable
```

**Return output:**
```python
return output  # Markdown text (NOT file path, NOT file creation statement)
```

---

## Prohibited Actions

### ❌ NEVER Do These:

1. **Create files:**
   ```python
   # ❌ WRONG
   Write(file_path=f"{story_id}-SUMMARY.md", content="...")
   Write(file_path=f"{story_id}-QUICK-START.md", content="...")
   ```

2. **Write to disk:**
   ```bash
   # ❌ WRONG
   Bash(command="cat > STORY-009-SUMMARY.md <<EOF...")
   ```

3. **Return file paths:**
   ```python
   # ❌ WRONG
   return "Created files:\n1. STORY-009-user-story.md\n2. STORY-009-acceptance-criteria.md"
   ```

4. **Create comprehensive deliverables:**
   ```python
   # ❌ WRONG - This is what general-purpose requirements-analyst does
   create_summary_document()
   create_quick_start_guide()
   create_validation_checklist()
   create_file_index()
   create_delivery_summary()
   ```

### ✅ ALWAYS Do These:

1. **Return markdown text:**
   ```python
   # ✅ CORRECT
   return """
   ## User Story
   **As a** DBA...

   ## Acceptance Criteria
   ### AC1: ...
   """
   ```

2. **Follow contract:**
   ```python
   # ✅ CORRECT
   contract = Read(".claude/skills/devforgeai-story-creation/contracts/requirements-analyst-contract.yaml")
   # Validate output against contract before returning
   ```

3. **Self-validate output:**
   ```python
   # ✅ CORRECT
   assert all required sections present
   assert no file creation indicators
   assert NFRs are measurable
   ```

---

## Error Handling

**If insufficient information:**
```python
if len(feature_description.split()) < 10:
    ERROR: Feature description too short to generate meaningful requirements
    Action: Request more detail from parent skill

    return """
    ERROR: Insufficient Information

    Feature description is too short (< 10 words).
    Please provide more detail about:
    - Who is the user/persona?
    - What functionality is needed?
    - Why is this valuable (business benefit)?

    Minimum: 10 words describing who/what/why
    """
```

**If ambiguous requirements:**
```python
if ambiguity_detected:
    # Do NOT make assumptions - ask parent skill

    return """
    CLARIFICATION NEEDED

    Feature description is ambiguous:
    - [Ambiguity 1]
    - [Ambiguity 2]

    Please clarify before proceeding with requirements analysis.
    """
```

**If contract violation risk:**
```python
# HALT before violating contract

if about_to_create_file:
    HALT: "Contract violation prevented"
    Log: "story-requirements-analyst attempted file creation - blocked by self-check"

    # Return error to parent skill
    return "ERROR: Internal constraint violation prevented. Please re-invoke subagent."
```

---

## Success Criteria

**Subagent output is successful when:**
- [ ] Returned markdown text (NOT files)
- [ ] All required sections present (User Story, AC, Edge Cases, NFRs)
- [ ] Minimum 3 acceptance criteria (Given/When/Then format)
- [ ] Minimum 2 edge cases
- [ ] All NFRs measurable (no vague terms)
- [ ] No file creation indicators in output
- [ ] Contract validation passes
- [ ] Parent skill can assemble output into story-template.md without modification

---

## Testing

**Unit Test 1: Content Return (Not Files)**
```python
# Invoke subagent
output = Task(
    subagent_type="story-requirements-analyst",
    prompt="Feature: User login with email/password..."
)

# Assertions
assert isinstance(output, str), "Output should be string (markdown text)"
assert "## User Story" in output
assert "## Acceptance Criteria" in output
assert ".md" not in output or "markdown" in output.lower(), "No file references"
assert "File created" not in output
```

**Unit Test 2: Required Sections**
```python
output = invoke_subagent()

required = ["User Story", "Acceptance Criteria", "Edge Cases", "Non-Functional Requirements"]
for section in required:
    assert f"## {section}" in output, f"Missing section: {section}"
```

**Unit Test 3: Measurable NFRs**
```python
output = invoke_subagent()
nfr_section = extract_section(output, "Non-Functional Requirements")

vague_terms = ["fast", "secure", "scalable"]
for term in vague_terms:
    assert term not in nfr_section.lower(), f"Vague NFR term: {term}"
```

---

**Integration Test: Full Story Creation**
```python
# Create story using story-requirements-analyst
/create-story Database backup automation with retention policy

# Assertions:
# 1. Only 1 .story.md file created
# 2. No supporting files (SUMMARY, QUICK-START, etc.)
# 3. Story file contains all sections
# 4. Content quality matches general-purpose requirements-analyst
```

---

**This subagent enforces the single-file design principle and prevents RCA-007 recurrence.**
```

**Effort:** 4-6 hours (creation + testing)

---

#### Task 3.2: Update Skill to Use story-requirements-analyst (1 hour)

**File:** `.claude/skills/devforgeai-story-creation/references/requirements-analysis.md`

**Change subagent invocation:**

**Before:**
```python
Task(
  subagent_type="requirements-analyst",  # General-purpose
  ...
)
```

**After:**
```python
Task(
  subagent_type="story-requirements-analyst",  # Skill-specific
  ...
)
```

**Document change:**
```markdown
## Step 2.1: Invoke Story Requirements Analyst Subagent (UPDATED - RCA-007 Fix)

**Subagent:** `story-requirements-analyst` (skill-specific)
**Contract:** `.claude/skills/devforgeai-story-creation/contracts/requirements-analyst-contract.yaml`

**Change History:**
- **2025-11-06:** Switched from general-purpose `requirements-analyst` to skill-specific `story-requirements-analyst`
- **Reason:** RCA-007 - general-purpose subagent created multiple files instead of returning content
- **Benefit:** Skill-specific subagent understands story-template.md assembly pattern and returns content only

**Migration Note:** If `story-requirements-analyst` not available, fallback to `requirements-analyst` with enhanced prompt constraints (Fix 1).
```

**Effort:** 1 hour

---

#### Task 3.3: Regression Testing (2-3 hours)

**Test Suite: Verify No Behavior Changes**

**Test 1: Content Quality Unchanged**
```python
# Create story with original subagent
story_1 = create_story_with_requirements_analyst()

# Create story with new subagent
story_2 = create_story_with_story_requirements_analyst()

# Compare quality
assert len(story_1['acceptance_criteria']) == len(story_2['acceptance_criteria'])
assert story_1['user_story_format'] == story_2['user_story_format']
assert story_1['nfr_measurability'] == story_2['nfr_measurability']
```

**Test 2: Self-Validation Still Works**
```python
# Phase 7 should still pass
/create-story Test self-validation preservation

# Check Phase 7 output
assert "Phase 7: Self-Validation" in workflow_log
assert "Validation Result: PASS" in workflow_log
```

**Test 3: Epic/Sprint Linking Still Works**
```python
# Phase 6 should still update epic/sprint
/create-story epic-003

# Check epic file
epic_content = Read("devforgeai/specs/Epics/EPIC-003.epic.md")
assert "STORY-XXX" in epic_content  # New story referenced
```

**Test 4: Completion Report Generated**
```python
# Phase 8 should still produce summary
/create-story Test completion report

# Check for summary output
assert "Story Creation Complete" in output
assert "Next Steps" in output
```

**Effort:** 2-3 hours

---

## Total Implementation Timeline

### Week 1 (Phase 1 - Immediate)
- **Monday:** Task 1.1 (30 min) + Task 1.2 (2 hrs) = 2.5 hours
- **Tuesday:** Task 1.3 testing (30 min) + Phase 1 validation = 1 hour
- **Total:** 3.5 hours

### Week 2 (Phase 2 - Short-Term)
- **Monday:** Task 2.1 contract creation (4 hrs)
- **Tuesday:** Task 2.2 validation (1 hr) + Task 2.3 file diff (3 hrs) = 4 hours
- **Wednesday:** Phase 2 testing = 2 hours
- **Total:** 10 hours

### Week 3-4 (Phase 3 - Long-Term)
- **Week 3 Mon-Tue:** Task 3.1 create subagent (6 hrs)
- **Week 3 Wed:** Task 3.2 update skill (1 hr) + Task 3.3 regression testing (3 hrs) = 4 hours
- **Week 3 Thu:** Phase 3 validation + documentation = 2 hours
- **Total:** 12 hours

**Grand Total:** 25.5 hours (within 25-35 hour estimate)

---

## Success Metrics

### Phase 1 Success
- [ ] Zero extra files created (SUMMARY, QUICK-START, etc.)
- [ ] Only 1 .story.md file per story
- [ ] Validation catches file creation attempts (tested)
- [ ] Re-invocation logic works (tested)

### Phase 2 Success
- [ ] Contract YAML file created and validated
- [ ] Contract validation integrated into workflow
- [ ] File system diff detects violations
- [ ] Rollback logic works correctly

### Phase 3 Success
- [ ] story-requirements-analyst subagent created
- [ ] Skill uses new subagent
- [ ] Content quality unchanged (regression tests pass)
- [ ] Zero file creation violations (production testing)

---

## Rollback Plan

**If fixes cause issues:**

1. **Immediate rollback (Phase 1):**
   - Remove output validation step (Step 2.2)
   - Revert to original prompt (remove constraints)
   - File: `.claude/skills/devforgeai-story-creation/references/requirements-analysis.md.backup`

2. **Contract rollback (Phase 2):**
   - Disable contract validation (comment out Step 2.3)
   - Keep contract file for reference
   - Revert to Phase 1 state

3. **Subagent rollback (Phase 3):**
   - Switch back to `requirements-analyst` (general-purpose)
   - Keep `story-requirements-analyst` as optional
   - Revert skill reference file

**Rollback criteria:**
- 3+ consecutive failures with new constraints
- User reports quality degradation
- Performance degradation >50% (execution time doubled)

---

## Related Documents

- **RCA:** `.devforgeai/RCA/RCA-007-multi-file-story-creation.md`
- **Enhancement:** `.devforgeai/specs/enhancements/BATCH-STORY-CREATION-PLAN.md` (next document)
- **Skill:** `.claude/skills/devforgeai-story-creation/SKILL.md`
- **Subagent:** `.claude/agents/requirements-analyst.md`
- **Contract:** `.claude/skills/devforgeai-story-creation/contracts/requirements-analyst-contract.yaml` (to be created)

---

**Implementation Status:** Ready to Begin
**Estimated Completion:** 3-4 weeks (3 phases)
**Priority:** HIGH (RCA-007 fix is critical for framework integrity)
