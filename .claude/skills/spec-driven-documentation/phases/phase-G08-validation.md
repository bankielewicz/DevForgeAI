# Phase G08: Validation & Quality Check

## Entry Gate

```bash
devforgeai-validate phase-check ${SESSION_ID} --from=G07 --to=G08 --workflow=doc-gen
# Exit 0: proceed | Exit 1: Phase G07 incomplete
```

## Contract

PURPOSE: Verify documentation coverage >= 80%, validate Mermaid diagram syntax, check framework constraint compliance, verify required sections, perform anti-aspirational content check.
REQUIRED SUBAGENTS: (none)
REQUIRED ARTIFACTS: Validation report with coverage percentage, violation list
STEP COUNT: 5 mandatory steps

---

## Reference Loading [MANDATORY]

```
Read(file_path="references/documentation-standards.md")
Read(file_path="references/anti-aspirational-guidelines.md")
```

IF any Read fails: HALT -- "Phase G08 reference files not loaded. Cannot proceed."

---

## Mandatory Steps

### Step G08.1: Verify Documentation Coverage

EXECUTE: Calculate documentation coverage percentage.
```
total_public_apis = count public functions/classes/endpoints from documentation_context
documented_apis = count APIs with documentation in generated sections

coverage = (documented_apis / total_public_apis) * 100

Display: "Documentation coverage: {coverage}%"

IF coverage < 80:
    Display: "Warning: Coverage {coverage}% below threshold (80%)"
    Display: "Undocumented items:"
    FOR each undocumented_api:
        Display: "  - {api.name} ({api.location})"

    AskUserQuestion:
        Question: "Documentation coverage is {coverage}% (threshold: 80%). How to proceed?"
        Header: "Coverage"
        Options:
            - label: "Continue with current coverage"
              description: "Accept below-threshold coverage for now"
            - label: "Add missing documentation"
              description: "Generate docs for undocumented items before continuing"
        multiSelect: false

    IF user chooses "Add missing documentation":
        # Re-invoke documentation-writer for missing items
        # Loop back to G04 pattern for missing items only
        FOR each undocumented_api:
            Task(subagent_type="documentation-writer", ...)
        # Re-calculate coverage
ELSE:
    Display: "Coverage meets quality gate threshold (>= 80%)"
```
VERIFY: coverage calculated. If below 80%, user decision recorded.
RECORD: `devforgeai-validate phase-record ${SESSION_ID} --phase=G08 --step=G08.1 --workflow=doc-gen`

---

### Step G08.2: Validate Mermaid Diagrams

EXECUTE: If architecture diagrams were generated, validate Mermaid syntax.
```
IF "architecture" in generated_sections:
    # Extract all Mermaid code blocks from architecture section
    content = Read(file_path=OUTPUT_MAP["architecture"])
    mermaid_blocks = extract_mermaid_blocks(content)

    FOR each block in mermaid_blocks:
        # Check for common syntax errors per diagram-generation-guide.md:
        # - Missing semicolons in sequence diagrams
        # - Unclosed quotes
        # - Invalid node IDs (spaces, special chars)
        # - Missing direction declarations
        errors = check_mermaid_syntax(block)

        IF errors:
            Display: "Diagram syntax error: {errors}"
            # Attempt auto-fix
            fixed = auto_fix_mermaid(block, errors)
            IF fixed != block:
                Edit(file_path=OUTPUT_MAP["architecture"],
                     old_string=block, new_string=fixed)
                Display: "  Auto-fixed diagram syntax"
            ELSE:
                Display: "  Manual review needed"
        ELSE:
            Display: "  Diagram syntax valid"

ELSE:
    Display: "No architecture diagrams to validate"
```
VERIFY: All Mermaid blocks either pass syntax check or are auto-fixed. If unfixable, flagged for manual review.
RECORD: `devforgeai-validate phase-record ${SESSION_ID} --phase=G08 --step=G08.2 --workflow=doc-gen`

---

### Step G08.3: Check Framework Constraint Compliance

EXECUTE: Verify documentation does not contradict architecture constraints.
```
Read(file_path="devforgeai/specs/context/architecture-constraints.md")

IF "architecture" in generated_sections:
    # Validate diagrams match architecture constraints:
    # - Layer structure matches documented layers
    # - Data flow direction respects constraints
    # - No prohibited dependencies shown
    content = Read(file_path=OUTPUT_MAP["architecture"])
    violations = check_architecture_compliance(content, architecture_constraints)

    IF violations:
        Display: "Architecture constraint violations in documentation:"
        FOR each violation:
            Display: "  - {violation.description}"
        Display: "Fix these before proceeding."
    ELSE:
        Display: "Architecture documentation compliant with constraints"
ELSE:
    Display: "No architecture docs to check against constraints"
```
VERIFY: No blocking constraint violations. Warnings displayed if any.
RECORD: `devforgeai-validate phase-record ${SESSION_ID} --phase=G08 --step=G08.3 --workflow=doc-gen`

---

### Step G08.4: Verify Required Sections Present

EXECUTE: Check that generated documentation contains required sections per type.
```
required_sections = {
    "api": ["Overview", "Endpoints", "Examples"],
    "architecture": ["Overview", "Diagrams"],
    "developer-guide": ["Overview", "Setup", "Development"],
    "troubleshooting": ["Overview"],
    "roadmap": ["Overview"]
}

FOR each doc_type in updated_files:
    content = Read(file_path=updated_files[doc_type])
    missing = []

    FOR section in required_sections.get(doc_type, []):
        IF section not in content (case-insensitive heading search):
            missing.append(section)

    IF missing:
        Display: "  {doc_type}: Missing sections: {missing}"
    ELSE:
        Display: "  {doc_type}: All required sections present"

IF any missing sections:
    Display: "Warning: Some required sections missing. Review generated content."
```
VERIFY: Required sections check completed for all doc types. Missing sections flagged.
RECORD: `devforgeai-validate phase-record ${SESSION_ID} --phase=G08 --step=G08.4 --workflow=doc-gen`

---

### Step G08.5: Anti-Aspirational Content Check

EXECUTE: Scan all generated content for prohibited language patterns.
```
# Reference: references/anti-aspirational-guidelines.md

aspirational_patterns = [
    "will be", "will support", "planned", "in the future",
    "upcoming", "powerful", "robust", "seamless",
    "easy to use", "simple", "intuitive"
]

placeholder_patterns = [
    "your-", "example-", "<placeholder>", "..."
]

total_violations = 0

FOR each doc_type, path in updated_files:
    # Check aspirational language
    FOR pattern in aspirational_patterns:
        matches = Grep(pattern=pattern, path=path, output_mode="content")
        IF matches:
            Display: "  {doc_type}: '{pattern}' found at:"
            FOR match in matches:
                Display: "    Line {line}: {context}"
            total_violations += len(matches)

    # Check placeholder content
    FOR pattern in placeholder_patterns:
        matches = Grep(pattern=pattern, path=path, output_mode="content")
        IF matches:
            Display: "  {doc_type}: Placeholder '{pattern}' found"
            total_violations += len(matches)

    # Check empty sections (heading followed by heading)
    content = Read(file_path=path)
    empty_sections = find_empty_sections(content)
    IF empty_sections:
        Display: "  {doc_type}: Empty sections detected: {empty_sections}"
        total_violations += len(empty_sections)

IF total_violations > 0:
    Display: ""
    Display: "Total content violations: {total_violations}"
    Display: "Fix aspirational language and placeholders before release."
ELSE:
    Display: "Anti-aspirational check passed: No violations"
```
VERIFY: Content scan completed for all doc types. Violations counted and displayed.
RECORD: `devforgeai-validate phase-record ${SESSION_ID} --phase=G08 --step=G08.5 --workflow=doc-gen`

---

## Exit Gate

```bash
devforgeai-validate phase-complete ${SESSION_ID} --phase=G08 --checkpoint-passed --workflow=doc-gen
```

## Phase Transition Display

```
Display: "Phase G08 complete: Validation & Quality Check"
Display: "  Coverage: {coverage}%"
Display: "  Violations: {total_violations}"
Display: "  Proceeding to Phase G09: Export & Finalization"
```
