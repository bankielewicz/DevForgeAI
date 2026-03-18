# Phase 03: ADR Creation

## Contract

| Attribute | Value |
|-----------|-------|
| **PURPOSE** | Create Architecture Decision Records for all major technology and design decisions. ADRs provide traceability and prevent revisiting settled decisions. |
| **REFERENCES** | `designing-systems/references/adr-creation-workflow.md`, `designing-systems/references/adr-policy.md`, `designing-systems/references/adr-template.md`, `designing-systems/assets/adr-examples/ADR-EXAMPLE-001-database-selection.md` |
| **STEP COUNT** | 4 mandatory steps |

## Phase Exit Criteria

Before this phase can complete, ALL of the following MUST be true:
- [ ] User confirmed which decisions warrant ADRs
- [ ] Each confirmed ADR file exists at `devforgeai/specs/adrs/`
- [ ] Each ADR contains all 6 required sections
- [ ] Checkpoint updated with ADR creation records

**IF any criterion is unmet: HALT. Do NOT proceed to Phase 04.**

---

## Reference Loading [MANDATORY]

```
Read(file_path=".claude/skills/designing-systems/references/adr-creation-workflow.md")
Read(file_path=".claude/skills/designing-systems/references/adr-policy.md")
Read(file_path=".claude/skills/designing-systems/references/adr-template.md")
Read(file_path=".claude/skills/designing-systems/assets/adr-examples/ADR-EXAMPLE-001-database-selection.md")
```

Do NOT rely on memory of previous reads. Load fresh every time this phase executes.

---

## Mandatory Steps

### Step 3.1: Identify ADR-Worthy Decisions

**EXECUTE:**
Read the tech-stack.md created in Phase 02 to extract all major decisions:
```
Read(file_path="devforgeai/specs/context/tech-stack.md")
```
Extract decision candidates: primary language, database engine, ORM, framework, architecture pattern, testing framework, deployment strategy, CI/CD tooling.

Present candidates to user for confirmation:
```
AskUserQuestion:
  Question: "The following decisions were extracted from your tech stack. Which ones should have formal ADRs? (ADRs document the WHY behind each decision and prevent revisiting them later.)"
  Header: "ADR Candidate Selection"
  Options:
    - label: "<Decision 1: e.g., Language Selection>"
      description: "<extracted choice>"
    - label: "<Decision 2: e.g., Database Selection>"
      description: "<extracted choice>"
    - label: "<Decision N: ...>"
      description: "<extracted choice>"
    - label: "All of the above"
      description: "Create ADRs for every identified decision"
  multiSelect: true
```

**VERIFY:**
- tech-stack.md was successfully read (content length > 0)
- At least 1 decision candidate was extracted
- User response is non-empty and contains at least 1 selection

**RECORD:**
```json
{
  "step": "3.1",
  "candidates_extracted": "<count>",
  "candidates_confirmed": ["<list of confirmed decisions>"],
  "user_selected_all": "<true|false>"
}
```

---

### Step 3.2: Load ADR Template and Examples

**EXECUTE:**
```
Read(file_path=".claude/skills/designing-systems/references/adr-template.md")
Read(file_path=".claude/skills/designing-systems/assets/adr-examples/ADR-EXAMPLE-001-database-selection.md")
```
Extract the 6 required ADR sections from the template:
1. Title
2. Context
3. Decision
4. Rationale
5. Consequences
6. Alternatives Considered

Note the format, heading levels, and content expectations from the example.

**VERIFY:**
- Template file was read successfully (content length > 0)
- Example file was read successfully (content length > 0)
- All 6 required section headers identified in template

**RECORD:**
```json
{
  "step": "3.2",
  "template_loaded": true,
  "example_loaded": true,
  "required_sections": ["Title", "Context", "Decision", "Rationale", "Consequences", "Alternatives Considered"],
  "template_length": "<char_count>"
}
```

---

### Step 3.3: Generate ADRs

**EXECUTE:**
For each confirmed decision from Step 3.1:

1. Determine the next available ADR number:
```
Glob(pattern="devforgeai/specs/adrs/ADR-*.md")
```
Parse existing ADR numbers, increment to next available.

2. Generate ADR content using template structure. Populate all 6 sections with decision-specific content drawn from tech-stack.md and user input from Phase 01.

3. Write each ADR file:
```
Write(file_path="devforgeai/specs/adrs/ADR-<NNN>-<kebab-case-title>.md", content=<adr_content>)
```

4. After all ADRs are written, verify each exists:
```
Glob(pattern="devforgeai/specs/adrs/ADR-*.md")
```

**VERIFY:**
- Number of ADR files created matches number of confirmed decisions
- Each ADR file exists (Glob confirms)
- Each ADR file has content length > 200 characters

**RECORD:**
```json
{
  "step": "3.3",
  "adrs_created": [
    {
      "number": "<NNN>",
      "title": "<decision title>",
      "file": "ADR-<NNN>-<kebab-case-title>.md",
      "content_length": "<char_count>"
    }
  ],
  "total_created": "<count>"
}
```

---

### Step 3.4: Validate ADR Format

**EXECUTE:**
For each created ADR file, verify all 6 required sections are present:
```
Grep(pattern="^## (Title|Context|Decision|Rationale|Consequences|Alternatives Considered)", path="devforgeai/specs/adrs/ADR-<NNN>-<title>.md", output_mode="content")
```

Count section headers found. If any ADR is missing sections, report the specific gaps.

**VERIFY:**
- Each ADR contains exactly 6 required section headers (or equivalent heading structure from template)
- No ADR has fewer than 6 sections
- If any section is missing: log the gap but do NOT auto-fix (report to user)

**RECORD:**
```json
{
  "step": "3.4",
  "validation_results": [
    {
      "adr": "ADR-<NNN>",
      "sections_found": "<count>",
      "missing_sections": ["<list or empty>"],
      "valid": "<true|false>"
    }
  ],
  "all_valid": "<true|false>"
}
```

---

## Phase Transition Display

```
Display:
  "Phase 03 Complete: ADR Creation"
  "{N} Architecture Decision Records created and validated."
  "All decisions are now documented with rationale and alternatives."
  "Proceeding to Phase 04: Technical Specifications"
```
