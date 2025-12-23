# Phase 7: Story Self-Validation Workflow

Execute quality validation checks and self-healing procedures.

## Overview

This phase validates the generated story against quality standards and automatically corrects issues when possible.

---

## Prerequisites

**Load validation checklists:**
```
Read(file_path=".claude/skills/devforgeai-story-creation/references/validation-checklists.md")
```

This reference provides comprehensive validation logic for story quality assurance.

---

## Step 7.1: Validate YAML Frontmatter

**Objective:** Ensure frontmatter complete and valid

```
Read created story file (first 15 lines for frontmatter)

Required fields:
- [ ] id: Matches filename
- [ ] title: Present and descriptive (5-80 chars)
- [ ] epic: Present (EPIC-XXX or null)
- [ ] sprint: Present (SPRINT-XXX or "Backlog")
- [ ] status: Set to "Backlog"
- [ ] priority: One of Critical/High/Medium/Low
- [ ] points: Fibonacci number (1/2/3/5/8/13)
- [ ] created: Today's date (YYYY-MM-DD format)
- [ ] updated: Same as created
- [ ] assigned_to: null (unassigned initially)

If validation fails:
    # Self-healing: Regenerate frontmatter
    # Edit story file to fix
    # Retry validation
```

---

## Step 7.2: Validate User Story Format

**Objective:** Verify user story follows As a/I want/So that format

```
Read user story section

Validation:
- [ ] Starts with "As a"
- [ ] Contains "I want"
- [ ] Contains "So that"
- [ ] Role is specific (not generic "user")
- [ ] Action is clear and unambiguous
- [ ] Benefit articulates business value

If validation fails:
    # Extract role, action, benefit from subagent output
    # Regenerate user story section
    # Edit story file
    # Retry validation
```

---

## Step 7.3: Validate Acceptance Criteria

**Objective:** Ensure AC meet quality standards

```
Read acceptance criteria section

Validation:
- [ ] Minimum 3 acceptance criteria
- [ ] Each has unique title/number (AC1, AC2, AC3, ...)
- [ ] Each follows Given/When/Then structure
- [ ] At least 1 happy path scenario
- [ ] At least 1 error/edge case scenario
- [ ] All criteria are testable (can write automated test)
- [ ] No ambiguous language ("should", "might", "probably")
- [ ] No vague terms ("fast", "easy", "intuitive" without definition)

If validation fails:
    # Identify which criteria are invalid
    # Regenerate specific criteria
    # Use acceptance-criteria-patterns.md for templates
    # Edit story file
    # Retry validation
```

---

## Step 7.4: Validate Technical Specification

**Objective:** Verify technical spec completeness

```
Validation:

If API contracts present:
- [ ] HTTP method specified (GET/POST/PUT/DELETE/PATCH)
- [ ] Endpoint path follows RESTful conventions
- [ ] Request schema includes all required fields
- [ ] Success response (200/201) schema defined
- [ ] Error responses (400/401/403/404/500) documented
- [ ] Authentication requirements specified

Data models:
- [ ] At least 1 entity defined
- [ ] Each entity has attributes with types
- [ ] Constraints specified (Required, Unique, Length, Format)
- [ ] Relationships documented (if applicable)
- [ ] Primary key identified

Business rules:
- [ ] At least 1 rule documented (if business logic exists)
- [ ] Rules are specific (not generic)
- [ ] Validation logic clear

Dependencies:
- [ ] All external dependencies identified
- [ ] Integration methods specified
- [ ] Fallback behavior defined

If validation fails:
    # Identify gaps
    # Regenerate missing sections
    # Use technical-specification-guide.md for templates
    # Edit story file
    # Retry validation
```

---

## Step 7.5: Validate Non-Functional Requirements

**Objective:** Ensure NFRs are measurable

```
Validation:

- [ ] Performance targets quantified (e.g., "<500ms response time")
- [ ] Security requirements specific (e.g., "OAuth2 with JWT", not "secure")
- [ ] Usability requirements clear (e.g., "Max 3 clicks to checkout")
- [ ] Scalability targets measurable (e.g., "Support 10k concurrent users")
- [ ] No vague terms without metrics

If validation fails:
    # Identify vague NFRs
    # Use AskUserQuestion to quantify
    # Edit story file
    # Retry validation
```

---

## Step 7.6: Validation Success Criteria

**Objective:** Confirm all validations passed before proceeding

**Before proceeding to Phase 8:**

```
All validations must pass:
- ✅ YAML frontmatter complete and valid
- ✅ User story follows format
- ✅ 3+ testable acceptance criteria
- ✅ Technical specification complete (if applicable)
- ✅ UI specification complete (if applicable)
- ✅ NFRs measurable (not vague)
- ✅ Edge cases documented
- ✅ Definition of Done present
- ✅ File exists on disk

If any CRITICAL failures (missing sections, invalid frontmatter):
    # Self-healing: Regenerate and retry (max 2 attempts)
    # If still failing: Report to user with specific issues

If all validations pass:
    ✅ Proceed to Step 7.7 (Context File Compliance)
```

---

## Step 7.7: Context File Compliance Validation

**Objective:** Final validation that story adheres to all constitutional context files

**Reference:** `.claude/skills/devforgeai-story-creation/references/context-validation.md`

**Purpose:** This is the comprehensive final gate that validates the complete story against all 6 context files before story creation completes.

**Workflow:**

```
1. Load context files (if exist):
   context_dir = "devforgeai/specs/context/"
   context_files = Glob(pattern=f"{context_dir}*.md")

   IF len(context_files) == 0:
     Display: "ℹ️ Greenfield mode: context compliance validation skipped"
     SKIP to Phase 8
     RETURN { greenfield: true, compliant: true }
```

```
2. Load all available context files in PARALLEL:
   Read(file_path="devforgeai/specs/context/tech-stack.md")
   Read(file_path="devforgeai/specs/context/source-tree.md")
   Read(file_path="devforgeai/specs/context/dependencies.md")
   Read(file_path="devforgeai/specs/context/coding-standards.md")
   Read(file_path="devforgeai/specs/context/architecture-constraints.md")
   Read(file_path="devforgeai/specs/context/anti-patterns.md")
```

```
3. For each context file that exists, call validation functions:

   violations = []

   # From context-validation.md:
   IF tech_stack_exists:
     violations.extend(validate_technologies(tech_spec_content))

   IF source_tree_exists:
     violations.extend(validate_file_paths(tech_spec_content))

   IF dependencies_exists:
     violations.extend(validate_dependencies(dependencies_section))

   IF coding_standards_exists:
     violations.extend(validate_coverage_thresholds(dod_content, file_paths))

   IF architecture_exists:
     violations.extend(validate_architecture(tech_spec_content))

   IF anti_patterns_exists:
     violations.extend(validate_anti_patterns(tech_spec_content))
```

```
4. Generate compliance report:

   context_compliance = {
     "validated_at": datetime.now().isoformat(),
     "context_files_checked": count_files_checked,
     "violations": {
       "CRITICAL": [v for v in violations if v.severity == "CRITICAL"],
       "HIGH": [v for v in violations if v.severity == "HIGH"],
       "MEDIUM": [v for v in violations if v.severity == "MEDIUM"],
       "LOW": [v for v in violations if v.severity == "LOW"]
     },
     "total_violations": len(violations),
     "status": "COMPLIANT" if len(critical + high) == 0 else "FAILED"
   }
```

```
5. Handle violations by severity:

   IF CRITICAL or HIGH violations found:
     HALT workflow

     Display: f"""
     ❌ Context Compliance Validation FAILED

     CRITICAL Issues: {len(critical)}
     HIGH Issues: {len(high)}

     {format_violations(critical + high)}

     Story cannot be completed until violations are resolved.
     """

     FOR each violation in (critical + high):
       AskUserQuestion:
         Question: f"How to resolve: {violation.type} - {violation.description}?"
         Header: "Fix needed"
         Options:
           - "Fix in story"
             Description: "I'll provide the correct value"
           - "Update context file"
             Description: "Requires ADR - constraint should change"
           - "Defer to manual review"
             Description: "Flag for later, proceed with warning"

       Apply resolution based on user choice

     # Re-run validation after fixes
     GOTO Step 7.7 (max 2 retry attempts)
```

```
6. If only MEDIUM or LOW violations:
   Display: f"""
   ⚠️ Context Compliance Validation PASSED with warnings

   MEDIUM Issues: {len(medium)}
   LOW Issues: {len(low)}

   {format_violations(medium + low)}

   Proceeding to Phase 8 with warnings noted.
   """

   # Embed warning note in story file
   Edit story file to add:
   """
   <!-- Context Validation Warnings
   {format_violations(medium + low)}
   -->
   """
```

```
7. If no violations:
   Display: f"""
   ✅ Context Compliance Validation PASSED

   Context files checked: {count}/6
   Violations found: 0
   Status: COMPLIANT

   Story is fully compliant with all constitutional context files.
   """
```

**Validation Summary Table:**

| Context File | Validation Checks |
|--------------|-------------------|
| tech-stack.md | All technologies in tech spec are LOCKED or approved |
| source-tree.md | File paths in tech spec match allowed directories |
| dependencies.md | All packages in Dependencies section are approved |
| coding-standards.md | Coverage thresholds match layer (95%/85%/80%) |
| architecture-constraints.md | No cross-layer violations in design |
| anti-patterns.md | No forbidden patterns in technical spec |

**Exit Criteria:** All CRITICAL and HIGH violations resolved

**Output:**

```yaml
context_compliance:
  validated_at: "2025-12-23T14:30:00Z"
  context_files_checked: 6
  violations_found: 0
  status: "COMPLIANT"
```

---

## Reference Files Used

**Phase 7 references:**
- `validation-checklists.md` (1,038 lines) - Comprehensive quality checks
- `story-structure-guide.md` (662 lines) - Frontmatter and section requirements
- `acceptance-criteria-patterns.md` (1,259 lines) - AC format validation
- `technical-specification-guide.md` (1,269 lines) - Tech spec completeness

---

## Output

**Phase 7 produces:**
- ✅ Story validated against all quality standards
- ✅ Auto-corrected issues (if self-healing applied)
- ✅ Confirmed ready for implementation

---

## Error Handling

**Error 1: CRITICAL validation failure (max retries exceeded)**
- **Detection:** Self-healing attempted 2 times, still failing
- **Recovery:** Report to user with specific validation failures, request manual intervention

**Error 2: Missing required sections**
- **Detection:** Sections expected from previous phases not found in story file
- **Recovery:** Re-execute relevant phase (2, 3, or 4), regenerate section, retry validation

**Error 3: Vague NFRs cannot be quantified automatically**
- **Detection:** NFR contains "fast", "scalable" without metrics, cannot infer numbers
- **Recovery:** Use AskUserQuestion to get specific targets from user

See `error-handling.md` for comprehensive error recovery procedures.

---

## Next Phase

**After Phase 7 completes →** Phase 8: Completion Report

Load `completion-report.md` for Phase 8 workflow.
