# Phase 06: RCA Document Creation (Strategic Mode Only)

**Purpose:** Generate the complete, self-contained RCA document from template.
**Applies to:** Strategic mode only.

---

## Step 06.1: Load Writing Guide [MANDATORY]

### EXECUTE

```
Read(file_path=".claude/skills/spec-driven-rca/references/rca-writing-guide.md")
```

Use: Document structure, formatting standards, quality checklist.

### VERIFY

- Reference file content is in context

### RECORD

```bash
devforgeai-validate phase-record ${SESSION_ID} --workflow=rca --phase=06 --step=06.1
```

---

## Step 06.2: Load Document Template [MANDATORY]

### EXECUTE

```
Read(file_path=".claude/skills/spec-driven-rca/assets/rca-document-template.md")
```

Template has placeholders: `{NUMBER}`, `{TITLE}`, `{DATE}`, etc.

### VERIFY

- Template structure visible with placeholder markers

### RECORD

```bash
devforgeai-validate phase-record ${SESSION_ID} --workflow=rca --phase=06 --step=06.2
```

---

## Step 06.3: Populate Header [MANDATORY]

### EXECUTE

Replace placeholders:
```
{NUMBER} -> RCA_NUMBER (from Phase 00)
{TITLE} -> RCA_TITLE (from Phase 00)
{DATE} -> current date (YYYY-MM-DD format)
{REPORTER} -> "User" or extracted from conversation
{COMPONENT} -> AFFECTED_COMPONENT (from Phase 00)
{SEVERITY} -> SEVERITY (from Phase 00)
```

### VERIFY

- All header placeholders replaced with actual values
- Date is in YYYY-MM-DD format
- Severity is one of CRITICAL/HIGH/MEDIUM/LOW

### RECORD

```bash
devforgeai-validate phase-record ${SESSION_ID} --workflow=rca --phase=06 --step=06.3
```

---

## Step 06.4: Populate Issue Description [MANDATORY]

### EXECUTE

Replace `{ISSUE_DESCRIPTION}` with complete description including:
- What happened
- When it happened
- Where it happened (component)
- Expected vs actual behavior
- Impact

### VERIFY

- Issue description covers all 5 elements

### RECORD

```bash
devforgeai-validate phase-record ${SESSION_ID} --workflow=rca --phase=06 --step=06.4
```

---

## Step 06.5: Populate 5 Whys Section [MANDATORY]

### EXECUTE

```
Replace: {ISSUE_STATEMENT} -> brief version of issue description

FOR i = 1 to 5:
    Replace: {QUESTION_i} -> why_answers[i].question
    Replace: {ANSWER_i} -> why_answers[i].answer
    Replace: {EVIDENCE_i} -> why_answers[i].evidence

    IF i == 5:
        Prefix answer with: **ROOT CAUSE:**
```

### VERIFY

- All 5 Whys populated with questions, answers, and evidence
- Why #5 has ROOT CAUSE prefix
- Evidence references cite specific files and line numbers

### RECORD

```bash
devforgeai-validate phase-record ${SESSION_ID} --workflow=rca --phase=06 --step=06.5
```

---

## Step 06.6: Populate Evidence Section [MANDATORY]

### EXECUTE

From Phase 04 organized evidence:

```
FOR each file in files_examined (CRITICAL/HIGH significance first):
    Format per evidence template:
        **{path}**
        - Lines: {range}
        - Finding: {discovery}
        - Excerpt: ```{text}```
        - Significance: {why it matters}
        - Supports: Why #{N}

Add context files validation table from Phase 04
Add workflow state analysis from Phase 04 (if applicable)
```

### VERIFY

- Evidence section populated with organized file entries
- At least 3 files with CRITICAL/HIGH significance included
- Context file validation table present

### RECORD

```bash
devforgeai-validate phase-record ${SESSION_ID} --workflow=rca --phase=06 --step=06.6
```

---

## Step 06.7: Capture Codebase Context Snapshot [CONDITIONAL]

### EXECUTE

**Condition:** Execute if ANY recommendation references code files.

```
FOR each unique file_path in all_recommendations.implementation.file:
    Read(file_path="{file_path}")

    Extract and store:
        - Module path (e.g., crate::state::phase_state)
        - Struct/enum definitions referenced by recommendations (full definitions)
        - Function signatures being modified (with doc comments)
        - Relevant import statements

Build MODULE_HIERARCHY_SUBSET:
    Show only modules involved in recommendations
    Show dependency direction (-> means "depends on")

Build TYPE_DEFINITIONS:
    Full definitions with fields, derive macros, doc comments

Build FUNCTION_SIGNATURES:
    Full signatures with doc comments (NOT function bodies)

IF recommendations modify .rs files:
    Read("devforgeai/specs/context/architecture-constraints.md")
    Read("devforgeai/specs/context/anti-patterns.md")
    Read("devforgeai/specs/context/coding-standards.md")

    Extract applicable constraints with line number citations

VALIDATION:
    IF any recommendation modifies .rs files AND has zero architecture constraints:
        HALT: "REC-{N} modifies Rust code but cites no architecture constraints"

    IF MODULE_HIERARCHY_SUBSET is empty AND recommendations reference code files:
        HALT: "Codebase Context Snapshot is empty but recommendations reference source code"
```

### VERIFY

- Codebase context snapshot populated (if code files referenced)
- Type definitions and function signatures captured
- Architecture constraints cited for Rust file changes

### RECORD

```bash
devforgeai-validate phase-record ${SESSION_ID} --workflow=rca --phase=06 --step=06.7
```

---

## Step 06.8: Populate Recommendations Section [MANDATORY]

### EXECUTE

```
FOR each recommendation (sorted by priority, then dependency order):

    Use structured header format for consumer parser:
    ### REC-{rec.id}: {rec.priority} - {rec.title}

    **Addresses:** Why #{rec.why_number}
    **Conditional:** {rec.conditional_type}: {rec.condition}

    Include ALL mandatory subsections from recommendation-template.md:
    #### Evidence Traceability
    #### Conditional vs Unconditional
    #### Problem Addressed
    #### Current Code Context   <- [MANDATORY for code changes]
    #### Proposed Change
    #### Architecture Constraints  <- [MANDATORY for .rs files]
    #### Rationale
    #### Test Specification     <- [MANDATORY - table format]
    #### Effort Estimate        <- MUST include **Time:** N hours
    #### Success Criteria       <- MUST include - [ ] checkboxes
    #### Impact
```

### VERIFY

- Each recommendation has all mandatory subsections
- Header format matches: `### REC-N: PRIORITY - Title`
- No subsections missing or empty

### RECORD

```bash
devforgeai-validate phase-record ${SESSION_ID} --workflow=rca --phase=06 --step=06.8
```

---

## Step 06.9: Generate Supporting Sections [MANDATORY]

### EXECUTE

**Implementation Checklist:**
```
From recommendations:
    - [ ] Implement REC-X for each CRITICAL recommendation
    - [ ] Update specific files
    - [ ] Add/update tests
    - [ ] Documentation updates
    - [ ] Review all recommendations
    - [ ] Mark RCA as RESOLVED after implementation
```

**Prevention Strategy:**
```
Short-term (from CRITICAL recommendations):
    - {Primary fix from REC-1}
    - {Secondary fix from REC-2}

Long-term (from HIGH/MEDIUM recommendations):
    - Pattern improvements
    - Process enhancements

Monitoring:
    - What to watch for
    - When to audit
    - Escalation criteria
```

**Related RCAs:**
```
IF related_rcas from Phase 01:
    FOR each related_rca:
        - **{number}:** {title} ({relationship})
ELSE:
    "None"
```

### VERIFY

- Implementation checklist has at least 3 items
- Prevention strategy has short-term and long-term sections
- Related RCAs section populated (even if "None")

### RECORD

```bash
devforgeai-validate phase-record ${SESSION_ID} --workflow=rca --phase=06 --step=06.9
```

---

## Step 06.10: Write RCA Document [MANDATORY]

### EXECUTE

```
Generate filename:
    slug = RCA_TITLE.lowercase().replace(" ", "-")
    filename = "RCA-{RCA_NUMBER}-{slug}.md"
    path = "devforgeai/RCA/{filename}"

Write document:
    Write(file_path="{path}", content=populated_template)

Verify write:
    Read(file_path="{path}")
    Check: All placeholders replaced (no {PLACEHOLDER} remaining)
```

### VERIFY

- File exists at expected path
- Glob confirms: `Glob(pattern="devforgeai/RCA/RCA-{RCA_NUMBER}-*.md")`
- No `{PLACEHOLDER}` patterns remain in document

### RECORD

```bash
devforgeai-validate phase-record ${SESSION_ID} --workflow=rca --phase=06 --step=06.10
```

---

## Step 06.11: Phase 06 Summary [MANDATORY]

### EXECUTE

```
PHASE 06 COMPLETE (DOCUMENT)
==============================
RCA Document Created:
  File: devforgeai/RCA/RCA-{RCA_NUMBER}-{slug}.md
  Sections: 8/8 complete
  Recommendations: {count}
  Evidence: {count} files examined
  Codebase Context: {present | N/A}

Proceeding to Phase 07: Validation & Self-Check...
```

### VERIFY

- Summary displayed with file path

### RECORD

```bash
devforgeai-validate phase-record ${SESSION_ID} --workflow=rca --phase=06 --step=06.11
```
