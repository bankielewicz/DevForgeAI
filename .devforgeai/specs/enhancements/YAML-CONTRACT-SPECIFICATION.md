# YAML Contract Specification for Skill-Subagent Integration

**Date:** 2025-11-06
**Related:** RCA-007 Fix (Phase 2)
**Priority:** MEDIUM
**Effort:** 3-4 hours per contract
**Status:** Specification Complete

---

## Purpose

Define formal contracts between skills and subagents using YAML files to specify expected input/output formats, constraints, and validation rules. This prevents autonomous behavior and ensures subagent outputs integrate correctly with parent skill workflows.

---

## Contract Architecture

### Contract Location

**Standard location:**
```
.claude/skills/{skill-name}/contracts/{subagent-name}-contract.yaml
```

**Examples:**
- `.claude/skills/devforgeai-story-creation/contracts/requirements-analyst-contract.yaml`
- `.claude/skills/devforgeai-story-creation/contracts/api-designer-contract.yaml`
- `.claude/skills/devforgeai-architecture/contracts/architect-reviewer-contract.yaml`

### Contract Versioning

**Version format:** Semantic versioning (MAJOR.MINOR.PATCH)

**Version changes:**
- **MAJOR:** Breaking changes (output format changed, new required fields)
- **MINOR:** New optional fields, additional validation rules
- **PATCH:** Documentation updates, clarifications

**Example:**
```yaml
contract_version: "1.0.0"

changelog:
  - version: "1.0.0"
    date: "2025-11-06"
    changes: "Initial contract for RCA-007 fix"
  - version: "1.1.0"
    date: "2025-11-15"
    changes: "Added NFR measurability validation"
  - version: "1.1.1"
    date: "2025-11-20"
    changes: "Clarified edge case format requirements"
```

---

## Contract Schema

### Complete Contract Template

```yaml
# Contract: {skill-name} <-> {subagent-name}
# Version: {MAJOR.MINOR.PATCH}
# Date: {YYYY-MM-DD}
# Purpose: {One-sentence description}

contract_version: "1.0.0"
skill: {skill-name}
subagent: {subagent-name}
phase: "{Phase name in skill workflow}"
rca_reference: "{RCA-XXX if applicable}"

# Input specification
input:
  {param_1}:
    type: {string|integer|boolean|enum|object|array}
    description: "{Description}"
    required: {true|false}
    default: {default_value if not required}
    min_length: {integer - for strings}
    max_length: {integer - for strings}
    pattern: "{regex pattern - for validation}"
    example: "{example value}"

  {param_2}:
    type: object
    description: "{Description}"
    required: true
    properties:
      {nested_field_1}:
        type: {type}
        required: {true|false}
      {nested_field_2}:
        type: {type}

# Output specification
output_format: {markdown_content|json|yaml|text}
output_type: {text/markdown|application/json|text/yaml}
max_output_length: {integer - characters}

output_sections:
  {section_1}:
    format: "{description of format}"
    required: {true|false}
    structure:
      - {field_1}: {type}
      - {field_2}: {type}

  {section_2}:
    format: "{description}"
    min_count: {integer - for arrays}
    required: {true|false}

# Constraints (CRITICAL - RCA-007 Fix)
constraints:
  no_file_creation:
    enabled: {true|false}
    description: "{Why this constraint exists}"
    prohibited_tools: [{list of tools}]

  content_only:
    enabled: {true|false}
    description: "{Requirement for content return}"

  single_output:
    enabled: {true|false}
    description: "{Single vs. multiple outputs}"

  max_output_length:
    value: {integer}
    description: "{Size limit rationale}"

  specific_format:
    enabled: {true|false}
    format_spec: "{Format specification}"

# Validation rules
validation:
  {validation_1}:
    enabled: {true|false}
    rule: "{Description of validation rule}"
    enforcement: {strict|warning|info}

  {validation_2}:
    enabled: true
    prohibited_patterns: [{list of regex patterns}]

# Error handling
error_handling:
  on_{error_scenario_1}:
    action: "{re_invoke|ask_user_question|halt|log_and_continue}"
    max_retries: {integer}
    fallback: "{Fallback action if retries exhausted}"

  on_{error_scenario_2}:
    action: "{action}"
    prompt_user_options: [{list of recovery options}]

# Monitoring
monitoring:
  log_violations:
    enabled: {true|false}
    log_path: "{path to violation log}"

  track_retries:
    enabled: {true|false}
    max_retries_before_alert: {integer}

  performance_tracking:
    enabled: {true|false}
    warn_if_execution_exceeds: "{duration}"

# Version history
changelog:
  - version: "{MAJOR.MINOR.PATCH}"
    date: "{YYYY-MM-DD}"
    changes: "{Description of changes}"
    author: "{Author or system}"
```

---

## Contract Examples

### Example 1: requirements-analyst Contract (Complete)

**File:** `.claude/skills/devforgeai-story-creation/contracts/requirements-analyst-contract.yaml`

```yaml
# Contract: devforgeai-story-creation <-> requirements-analyst
# Version: 1.0.0
# Date: 2025-11-06
# Purpose: Define expected input/output format for story requirements generation

contract_version: "1.0.0"
skill: devforgeai-story-creation
subagent: requirements-analyst
phase: "Phase 2: Requirements Analysis"
rca_reference: "RCA-007"

# Input specification
input:
  feature_description:
    type: string
    description: "Feature description from user or epic"
    required: true
    min_length: 10
    max_length: 5000
    example: "User authentication with email and password, including password reset flow"

  story_metadata:
    type: object
    description: "Story metadata from Phase 1 (Story Discovery)"
    required: true
    properties:
      story_id:
        type: string
        required: true
        pattern: "^STORY-\\d{3}$"
        example: "STORY-042"
        description: "Unique story identifier"

      epic_id:
        type: string
        required: false
        pattern: "^EPIC-\\d{3}$|null"
        example: "EPIC-002"
        description: "Parent epic identifier (null if standalone)"

      priority:
        type: enum
        required: true
        values: ["Critical", "High", "Medium", "Low"]
        example: "High"
        description: "Story priority level"

      points:
        type: integer
        required: true
        values: [1, 2, 3, 5, 8, 13]
        example: 8
        description: "Story complexity (Fibonacci sequence)"

# Output specification
output_format: markdown_content
output_type: text/markdown
max_output_length: 50000

output_sections:
  user_story:
    format: "As a [role], I want [action], so that [benefit]"
    required: true
    validation:
      - Must identify specific persona (not generic "user")
      - Action must be clear and measurable
      - Benefit must explain business value

  acceptance_criteria:
    format: "Array of Given/When/Then scenarios"
    required: true
    min_count: 3
    structure:
      - title: string (clear, testable)
      - given: string (context/initial state)
      - when: string (action/trigger)
      - then: string (expected outcome)
    validation:
      - All criteria must be testable (can verify pass/fail)
      - Cover happy path + edge cases
      - Each criterion independent (test in isolation)

  edge_cases:
    format: "Numbered list of edge case scenarios"
    required: true
    min_count: 2
    structure:
      - scenario: string (edge case description)
      - handling: string (expected behavior)
    validation:
      - Cover unusual inputs, boundary conditions, error states
      - Each has clear handling strategy

  data_validation_rules:
    format: "Numbered list of validation rules"
    required: false
    min_count: 0
    structure:
      - parameter: string (input/data field)
      - rule: string (validation rule)

  nfrs:
    format: "Object with performance, security, reliability, scalability"
    required: true
    structure:
      performance:
        target: string (measurable metric)
        example: "< 100ms response time (p95)"
      security:
        target: string (measurable metric)
        example: "SQL injection prevention via parameterized queries"
      reliability:
        target: string (measurable metric)
        example: "99.9% uptime"
      scalability:
        target: string (measurable metric)
        example: "Support 10,000 concurrent users"
    validation:
      - All targets MUST be measurable
      - Prohibited vague terms: ["fast", "secure", "reliable", "scalable", "performant"]

# Constraints (CRITICAL - RCA-007 Fix)
constraints:
  no_file_creation:
    enabled: true
    description: "Subagent MUST NOT create files - parent skill handles file creation"
    prohibited_tools:
      - Write
      - Edit (on non-existent files)
      - Bash (with output redirection >, >>)
    rationale: "Phase 5 of parent skill assembles content into story-template.md"

  content_only:
    enabled: true
    description: "Return text content, not file references or file paths"
    rationale: "Output is assembled with other sections (tech spec, UI spec) into single .story.md"

  single_output:
    enabled: true
    description: "Return single markdown text block, not multiple file artifacts"
    rationale: "DevForgeAI enforces single-file design principle per story"

  max_output_length:
    value: 50000
    description: "Output must fit in Phase 5 assembly (story-template.md has ~60K capacity)"
    enforcement: strict

# Validation rules
validation:
  check_sections_present:
    enabled: true
    required_sections:
      - "User Story"
      - "Acceptance Criteria"
      - "Edge Cases"
      - "Non-Functional Requirements"
    enforcement: strict
    error_message: "Subagent output missing required sections"

  check_no_file_paths:
    enabled: true
    prohibited_patterns:
      - "File created:"
      - "\\.md created"
      - "STORY-\\d+-.*\\.md"
      - "Writing to file"
      - "Saved to disk"
      - "Created file:"
      - "Successfully wrote"
      - "Document generated:"
      - "SUMMARY\\.md"
      - "QUICK-START\\.md"
      - "VALIDATION-CHECKLIST\\.md"
      - "FILE-INDEX\\.md"
      - "DELIVERY-SUMMARY\\.md"
    enforcement: critical
    error_message: "Subagent created files instead of returning content (RCA-007 violation)"

  check_ac_format:
    enabled: true
    required_keywords: ["Given", "When", "Then"]
    min_count: 3
    enforcement: strict
    error_message: "Acceptance criteria must follow Given/When/Then format (minimum 3)"

  check_nfr_measurability:
    enabled: true
    prohibited_vague_terms:
      - "fast"
      - "secure"
      - "scalable"
      - "performant"
      - "reliable"
      - "quickly"
      - "efficiently"
    enforcement: warning
    error_message: "NFRs contain vague terms - must be measurable (e.g., '< 100ms' not 'fast')"

# Error handling
error_handling:
  on_file_creation_detected:
    action: re_invoke
    max_retries: 2
    strict_mode_prompt: true
    fallback: "HALT with manual intervention required"
    log: true

  on_missing_sections:
    action: ask_user_question
    prompt_user_options:
      - "Re-invoke subagent"
      - "Manually provide content for missing sections"
      - "Skip missing sections (not recommended)"
    fallback: "re_invoke"

  on_invalid_ac_format:
    action: re_invoke
    max_retries: 1
    enhanced_examples: true
    fallback: "ask_user_question"

  on_vague_nfrs:
    action: log_and_continue
    warning_message: "NFRs contain vague terms - recommend making measurable"
    suggest_improvements: true

# Monitoring
monitoring:
  log_violations:
    enabled: true
    log_path: ".devforgeai/logs/rca-007-violations.log"
    log_format: |
      [VIOLATION DETECTED]
      Timestamp: {timestamp}
      Story ID: {story_id}
      Subagent: {subagent_name}
      Parent Skill: {skill_name}
      Phase: {phase}
      Violation Type: {type}
      Pattern Matched: {pattern}
      Output Snippet: {snippet}
      Recovery Action: {action}
      Recovery Result: {result}
      ---

  track_retries:
    enabled: true
    max_retries_before_alert: 2
    alert_message: "Subagent {subagent_name} failed {retry_count} times - review prompt constraints"

  performance_tracking:
    enabled: true
    warn_if_execution_exceeds: "5 minutes"
    log_execution_time: true

  success_rate:
    enabled: true
    track_metric: "first_attempt_success_rate"
    target: 90
    alert_if_below: 80

# Usage instructions
usage:
  parent_skill_reads:
    - "Load contract in Phase {phase}: Read(file_path='{contract_path}')"
    - "Parse YAML: import yaml; contract = yaml.safe_load(contract_content)"
    - "Validate subagent output against contract.validation rules"
    - "Apply contract.error_handling on violations"

  subagent_awareness:
    - "Subagent prompt should reference contract: 'Contract Reference: {contract_path}'"
    - "Subagent does NOT read contract directly (prompt includes all constraints)"
    - "Parent skill enforces contract, not subagent"

# Version history
changelog:
  - version: "1.0.0"
    date: "2025-11-06"
    changes: "Initial contract definition for RCA-007 fix (requirements-analyst)"
    author: "DevForgeAI Framework"
    breaking_changes: false
```

**File size:** ~350-500 lines (comprehensive)

---

## Contract Usage Pattern

### In Parent Skill (Validation Logic)

**File:** `.claude/skills/devforgeai-story-creation/references/requirements-analysis.md`

**Step 2.3: Validate Against Contract (added after subagent invocation):**

```markdown
## Step 2.3: Validate Subagent Output Against Contract

**Load contract:**
```python
contract_path = ".claude/skills/devforgeai-story-creation/contracts/requirements-analyst-contract.yaml"

# Check if contract exists
if not file_exists(contract_path):
    WARNING: "Contract file not found - using fallback validation"
    # Use basic validation (no contract enforcement)
else:
    # Load and parse contract
    contract_content = Read(file_path=contract_path)

    import yaml
    contract = yaml.safe_load(contract_content)

    # Display contract info
    Display: f"""
    Validating against contract:
    - Contract: {contract['skill']} <-> {contract['subagent']}
    - Version: {contract['contract_version']}
    - Phase: {contract['phase']}
    """
```

**Validate constraints:**
```python
violations = []

# Constraint 1: No file creation
if contract['constraints']['no_file_creation']['enabled']:
    prohibited_patterns = contract['validation']['check_no_file_paths']['prohibited_patterns']

    for pattern in prohibited_patterns:
        if re.search(pattern, subagent_output, re.IGNORECASE):
            violations.append({
                "type": "FILE_CREATION",
                "constraint": "no_file_creation",
                "pattern": pattern,
                "severity": "CRITICAL"
            })

# Constraint 2: Required sections
if contract['validation']['check_sections_present']['enabled']:
    required_sections = contract['validation']['check_sections_present']['required_sections']

    for section in required_sections:
        if f"## {section}" not in subagent_output:
            violations.append({
                "type": "MISSING_SECTION",
                "constraint": "check_sections_present",
                "section": section,
                "severity": "HIGH"
            })

# Constraint 3: AC format
if contract['validation']['check_ac_format']['enabled']:
    min_count = contract['validation']['check_ac_format']['min_count']
    required_keywords = contract['validation']['check_ac_format']['required_keywords']

    ac_section = extract_section(subagent_output, "Acceptance Criteria")
    ac_count = ac_section.count("### AC")

    if ac_count < min_count:
        violations.append({
            "type": "INSUFFICIENT_AC",
            "constraint": "check_ac_format",
            "actual": ac_count,
            "required": min_count,
            "severity": "HIGH"
        })

    for keyword in required_keywords:
        if keyword not in ac_section:
            violations.append({
                "type": "INVALID_AC_FORMAT",
                "constraint": "check_ac_format",
                "missing_keyword": keyword,
                "severity": "MEDIUM"
            })

# Constraint 4: NFR measurability
if contract['validation']['check_nfr_measurability']['enabled']:
    prohibited_terms = contract['validation']['check_nfr_measurability']['prohibited_vague_terms']

    nfr_section = extract_section(subagent_output, "Non-Functional Requirements")

    for term in prohibited_terms:
        if term in nfr_section.lower():
            violations.append({
                "type": "VAGUE_NFR",
                "constraint": "check_nfr_measurability",
                "term": term,
                "severity": "MEDIUM"
            })

# Constraint 5: Output size
max_length = contract['constraints']['max_output_length']['value']
actual_length = len(subagent_output)

if actual_length > max_length:
    violations.append({
        "type": "SIZE_EXCEEDED",
        "constraint": "max_output_length",
        "actual": actual_length,
        "max": max_length,
        "severity": "MEDIUM"
    })
```

**Handle violations:**
```python
if violations:
    # Categorize by severity
    critical = [v for v in violations if v['severity'] == "CRITICAL"]
    high = [v for v in violations if v['severity'] == "HIGH"]
    medium = [v for v in violations if v['severity'] == "MEDIUM"]

    # Display violations
    Display: f"""
    ⚠️ Contract Validation FAILED

    Contract: {contract['skill']} <-> {contract['subagent']}
    Violations: {len(violations)} total

    Critical: {len(critical)}
    {format_violations(critical)}

    High: {len(high)}
    {format_violations(high)}

    Medium: {len(medium)}
    {format_violations(medium)}
    """

    # Apply error handling from contract
    if critical:
        # Critical violations always trigger recovery
        error_type = critical[0]['type'].lower()
        error_config = contract['error_handling'].get(f'on_{error_type}', {})

        action = error_config.get('action', 're_invoke')

        if action == 're_invoke':
            max_retries = error_config.get('max_retries', 1)

            Display: f"Recovery: Re-invoking subagent (max {max_retries} retries)"

            # Re-invoke with enhanced prompt
            retry_count = 0
            while retry_count < max_retries:
                retry_count += 1

                subagent_output = Task(
                    subagent_type="requirements-analyst",
                    prompt=f"""
                    **STRICT MODE - RETRY #{retry_count}**

                    Previous attempt violated contract constraints:
                    {format_violations(critical)}

                    This is retry attempt {retry_count} of {max_retries}.

                    {original_prompt with ENHANCED constraints}

                    CRITICAL: Adhere strictly to output constraints. NO file creation.
                    """
                )

                # Re-validate
                violations = validate_against_contract(subagent_output, contract)

                if not violations:
                    Display: f"✓ Retry #{retry_count} successful - contract validation PASSED"
                    break

            # If all retries exhausted
            if violations:
                fallback = error_config.get('fallback', 'HALT')

                if fallback == 'HALT':
                    HALT: f"Subagent violated contract {retry_count} times. Manual intervention required."
                    Exit Phase 2

    # Log all violations
    if contract['monitoring']['log_violations']['enabled']:
        log_path = contract['monitoring']['log_violations']['log_path']
        log_format = contract['monitoring']['log_violations']['log_format']

        log_entry = log_format.format(
            timestamp=datetime.now(),
            story_id=story_id,
            subagent_name=contract['subagent'],
            skill_name=contract['skill'],
            phase=contract['phase'],
            type=violation['type'],
            pattern=violation.get('pattern', 'N/A'),
            snippet=subagent_output[:200],
            action=action,
            result="SUCCESS" if not violations else "FAILED"
        )

        # Append to log
        with open(log_path, 'a') as f:
            f.write(log_entry)

else:
    # No violations - validation passed
    Display: f"""
    ✓ Contract Validation PASSED

    Contract: {contract['skill']} <-> {contract['subagent']}
    Version: {contract['contract_version']}
    All constraints satisfied ✅

    Output compliant with:
    - no_file_creation ✅
    - content_only ✅
    - required_sections (4/4) ✅
    - ac_format (5 criteria, Given/When/Then) ✅
    - nfr_measurability ✅
    - size limit ({actual_length}/{max_length} chars) ✅

    Proceeding to Phase 3
    """
```

---

## Example 2: api-designer Contract

**File:** `.claude/skills/devforgeai-story-creation/contracts/api-designer-contract.yaml`

```yaml
contract_version: "1.0.0"
skill: devforgeai-story-creation
subagent: api-designer
phase: "Phase 3: Technical Specification (conditional)"
rca_reference: "RCA-007"

# Input
input:
  feature_description:
    type: string
    required: true
    min_length: 10

  acceptance_criteria:
    type: array
    required: true
    description: "Acceptance criteria from Phase 2 (requirements-analyst output)"
    min_count: 3

  detected_endpoints:
    type: array
    required: true
    description: "Endpoints detected in AC (GET /api/users, POST /api/login, etc.)"
    min_count: 1

# Output
output_format: yaml
output_type: text/yaml
max_output_length: 30000

output_sections:
  openapi_spec:
    format: "OpenAPI 3.0 YAML specification"
    required: true
    structure:
      - openapi: "3.0.0"
      - info: {title, version}
      - paths: {endpoints with methods, params, responses}
      - components: {schemas, securitySchemes}
    validation:
      - Must be valid OpenAPI 3.0 YAML
      - All endpoints from detected_endpoints must be documented
      - All request/response schemas defined in components.schemas

# Constraints
constraints:
  no_file_creation:
    enabled: true
    description: "Return YAML text, not api-spec.yaml file"
    prohibited_tools: [Write, Edit, Bash]

  yaml_text_only:
    enabled: true
    description: "Return YAML as text string, parent skill embeds in .story.md"

  inline_schemas:
    enabled: true
    description: "All schemas in single YAML (no separate schema files)"

# Validation
validation:
  check_openapi_version:
    enabled: true
    required_version: "3.0.0"
    enforcement: strict

  check_all_endpoints_documented:
    enabled: true
    enforcement: strict

  check_no_file_references:
    enabled: true
    prohibited_patterns:
      - "api-spec\\.yaml"
      - "schema.*\\.yaml"
      - "endpoints\\.md"
    enforcement: critical

# Error handling
error_handling:
  on_invalid_yaml:
    action: re_invoke
    max_retries: 1
    provide_yaml_example: true

  on_file_creation_detected:
    action: re_invoke
    max_retries: 2
    fallback: "HALT"

# Monitoring
monitoring:
  log_violations:
    enabled: true
    log_path: ".devforgeai/logs/rca-007-violations.log"

# Changelog
changelog:
  - version: "1.0.0"
    date: "2025-11-06"
    changes: "Initial contract for api-designer (RCA-007 fix)"
```

---

## Contract Validation Helper Functions

**Create:** `.claude/skills/devforgeai-story-creation/scripts/validate_contract.py`

```python
#!/usr/bin/env python3
"""
Validate subagent output against YAML contract.

Usage:
    python validate_contract.py <output_file> <contract_yaml>
"""

import re
import sys
import yaml
from datetime import datetime

def load_contract(contract_path):
    """Load and parse YAML contract."""
    with open(contract_path, 'r') as f:
        return yaml.safe_load(f)

def validate_output(output_text, contract):
    """Validate output against contract specifications."""
    violations = []

    # Validation 1: No file creation
    if contract['constraints']['no_file_creation']['enabled']:
        patterns = contract['validation']['check_no_file_paths']['prohibited_patterns']

        for pattern in patterns:
            if re.search(pattern, output_text, re.IGNORECASE):
                violations.append({
                    "type": "FILE_CREATION",
                    "pattern": pattern,
                    "severity": "CRITICAL",
                    "constraint": "no_file_creation"
                })

    # Validation 2: Required sections
    if contract['validation']['check_sections_present']['enabled']:
        required = contract['validation']['check_sections_present']['required_sections']

        for section in required:
            if f"## {section}" not in output_text:
                violations.append({
                    "type": "MISSING_SECTION",
                    "section": section,
                    "severity": "HIGH",
                    "constraint": "check_sections_present"
                })

    # Validation 3: AC format (if applicable)
    if 'check_ac_format' in contract['validation']:
        config = contract['validation']['check_ac_format']

        if config['enabled']:
            min_count = config['min_count']
            keywords = config['required_keywords']

            ac_section = extract_section(output_text, "Acceptance Criteria")
            ac_count = ac_section.count("### AC") if ac_section else 0

            if ac_count < min_count:
                violations.append({
                    "type": "INSUFFICIENT_AC",
                    "actual": ac_count,
                    "required": min_count,
                    "severity": "HIGH",
                    "constraint": "check_ac_format"
                })

            for keyword in keywords:
                if keyword not in ac_section:
                    violations.append({
                        "type": "MISSING_AC_KEYWORD",
                        "keyword": keyword,
                        "severity": "MEDIUM",
                        "constraint": "check_ac_format"
                    })

    # Validation 4: NFR measurability (if applicable)
    if 'check_nfr_measurability' in contract['validation']:
        config = contract['validation']['check_nfr_measurability']

        if config['enabled']:
            prohibited = config['prohibited_vague_terms']
            nfr_section = extract_section(output_text, "Non-Functional Requirements")

            for term in prohibited:
                if term in nfr_section.lower():
                    violations.append({
                        "type": "VAGUE_NFR",
                        "term": term,
                        "severity": "MEDIUM",
                        "constraint": "check_nfr_measurability"
                    })

    # Validation 5: Size limit
    max_length = contract['constraints']['max_output_length']['value']
    actual_length = len(output_text)

    if actual_length > max_length:
        violations.append({
            "type": "SIZE_EXCEEDED",
            "actual": actual_length,
            "max": max_length,
            "severity": "MEDIUM",
            "constraint": "max_output_length"
        })

    return violations

def extract_section(text, section_name):
    """Extract content between section header and next header."""
    pattern = f"## {section_name}(.*?)(?=##|$)"
    match = re.search(pattern, text, re.DOTALL)
    return match.group(1).strip() if match else ""

def format_violations(violations):
    """Format violations for display."""
    output = []
    for v in violations:
        output.append(f"  [{v['severity']}] {v['type']}: {v.get('pattern', v.get('section', v.get('term', 'N/A')))}")
    return "\n".join(output)

def apply_error_handling(violations, contract, subagent_output, retry_count=0):
    """Apply contract error handling rules."""
    if not violations:
        return {"action": "continue", "output": subagent_output}

    # Get highest severity violation
    critical = [v for v in violations if v['severity'] == "CRITICAL"]
    high = [v for v in violations if v['severity'] == "HIGH"]

    if critical:
        primary_violation = critical[0]
    elif high:
        primary_violation = high[0]
    else:
        # Medium violations - log and continue
        return {"action": "log_and_continue", "output": subagent_output}

    # Get error handling config for this violation type
    error_type = primary_violation['type'].lower()
    error_config = contract['error_handling'].get(f'on_{error_type}', {})

    action = error_config.get('action', 're_invoke')
    max_retries = error_config.get('max_retries', 1)

    if retry_count >= max_retries:
        # Retries exhausted - apply fallback
        fallback = error_config.get('fallback', 'HALT')
        return {"action": fallback, "output": subagent_output, "violations": violations}

    # Return recovery action
    return {
        "action": action,
        "retry_count": retry_count + 1,
        "max_retries": max_retries,
        "violations": violations
    }

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python validate_contract.py <output_file> <contract_yaml>")
        sys.exit(1)

    output_file = sys.argv[1]
    contract_file = sys.argv[2]

    # Load files
    with open(output_file, 'r') as f:
        output_text = f.read()

    contract = load_contract(contract_file)

    # Validate
    violations = validate_output(output_text, contract)

    # Display results
    if violations:
        print(f"✗ Contract Validation FAILED ({len(violations)} violations)")
        print(format_violations(violations))
        sys.exit(1)
    else:
        print("✓ Contract Validation PASSED")
        print(f"  Output compliant with {contract['skill']} <-> {contract['subagent']} contract")
        sys.exit(0)
```

**Usage in skill:**
```bash
# After subagent invocation
python .claude/skills/devforgeai-story-creation/scripts/validate_contract.py \
    /tmp/subagent-output.txt \
    .claude/skills/devforgeai-story-creation/contracts/requirements-analyst-contract.yaml
```

---

## Contract Creation Checklist

**For each new skill-subagent integration:**

- [ ] **Step 1:** Identify parent skill and phase
- [ ] **Step 2:** Define input parameters (feature_description, story_metadata, etc.)
- [ ] **Step 3:** Define output format (markdown_content, json, yaml)
- [ ] **Step 4:** List required output sections
- [ ] **Step 5:** Specify constraints (no_file_creation, content_only, etc.)
- [ ] **Step 6:** Define validation rules (sections, format, size)
- [ ] **Step 7:** Configure error handling (re_invoke, ask_user_question, halt)
- [ ] **Step 8:** Enable monitoring (log violations, track retries)
- [ ] **Step 9:** Create contract YAML file
- [ ] **Step 10:** Update parent skill to validate against contract
- [ ] **Step 11:** Test contract enforcement (violation scenarios)
- [ ] **Step 12:** Document contract in skill's SKILL.md

---

## Testing Contracts

### Test Case 1: Contract File Valid YAML

```bash
# Validate YAML syntax
python -c "import yaml; yaml.safe_load(open('.claude/skills/devforgeai-story-creation/contracts/requirements-analyst-contract.yaml'))"

# Expected: No errors (valid YAML)
```

### Test Case 2: Contract Enforces No File Creation

```python
# Simulate subagent output with file creation
subagent_output = """
## User Story
...

## Acceptance Criteria
...

File created: STORY-009-SUMMARY.md
"""

# Validate
violations = validate_output(subagent_output, contract)

# Expected: 1 CRITICAL violation (FILE_CREATION)
assert len(violations) == 1
assert violations[0]['severity'] == "CRITICAL"
assert violations[0]['type'] == "FILE_CREATION"
```

### Test Case 3: Contract Catches Missing Sections

```python
# Simulate incomplete output
subagent_output = """
## User Story
...

## Acceptance Criteria
...

(Missing: Edge Cases, NFRs)
"""

# Validate
violations = validate_output(subagent_output, contract)

# Expected: 2 HIGH violations (MISSING_SECTION for Edge Cases, NFRs)
assert len(violations) == 2
assert all(v['type'] == "MISSING_SECTION" for v in violations)
```

### Test Case 4: Contract Allows Valid Output

```python
# Simulate compliant output
subagent_output = """
## User Story
**As a** DBA, **I want** to capture index characteristics, **so that** rebuilds preserve settings.

## Acceptance Criteria

### AC1: Capture standard properties
**Given** index exists
**When** fn_GetIndexDefinition() called
**Then** returns JSON with all properties

### AC2: Handle filtered indexes
**Given** filtered index exists
**When** function called
**Then** includes FilterDefinition

### AC3: Performance requirement
**Given** database with 1000+ indexes
**When** function called for any index
**Then** completes in < 100ms

## Edge Cases
1. **Partitioned indexes:** Capture partition scheme
2. **Columnstore indexes:** No key columns (NULL)

## Non-Functional Requirements

### Performance
- Response time: < 100ms per call (p95 and p99)

### Security
- SQL injection prevention: QUOTENAME() + sp_executesql

### Reliability
- Error handling: Return NULL on errors

### Scalability
- Supports 10,000+ indexes
"""

# Validate
violations = validate_output(subagent_output, contract)

# Expected: 0 violations
assert len(violations) == 0
```

---

## Integration with Existing Workflows

### devforgeai-story-creation Skill

**Phases affected:**
- **Phase 2:** Requirements Analysis (requirements-analyst contract)
- **Phase 3:** Technical Specification (api-designer contract)

**Changes required:**
1. Create 2 contract YAML files
2. Add validation step after each subagent invocation (Step 2.3, Step 3.3)
3. Add error handling logic (re-invoke, halt)
4. Add monitoring/logging

**Files modified:**
- `references/requirements-analysis.md` (add Step 2.3)
- `references/technical-specification-creation.md` (add Step 3.3)

**Files created:**
- `contracts/requirements-analyst-contract.yaml`
- `contracts/api-designer-contract.yaml`
- `scripts/validate_contract.py`

---

### devforgeai-orchestration Skill

**Phases affected:**
- **Phase 3:** Feature Decomposition (requirements-analyst contract)
- **Phase 4:** Technical Assessment (architect-reviewer contract - to be created)

**Changes required:**
1. Create 1 contract YAML file (requirements-analyst in epic context)
2. Add validation step in epic-management.md (Step 3.3)

**Note:** Same subagent (requirements-analyst) but different context:
- Story creation context: Generate user story + AC
- Epic context: Decompose epic into features (different output structure)

**Contract reuse:**
- Create separate contract: `epic-requirements-analyst-contract.yaml`
- Different output_sections (features array vs. user story)
- Same constraints (no_file_creation, content_only)

---

## Maintenance

### When to Update Contracts

**Update contract when:**
1. Subagent behavior changes (new output format)
2. New validation rules needed (discovered through testing)
3. Error handling improvements (better recovery logic)
4. Monitoring enhancements (new metrics to track)

**Version bump rules:**
- **MAJOR (1.0.0 → 2.0.0):** Breaking changes (output format change, new required sections)
- **MINOR (1.0.0 → 1.1.0):** New optional fields, additional validation rules
- **PATCH (1.0.0 → 1.0.1):** Documentation updates, clarifications

### Contract Review Schedule

**Monthly review:**
- Check violation logs (`.devforgeai/logs/rca-007-violations.log`)
- Analyze common violations
- Update prohibited_patterns if new violation types discovered
- Adjust max_output_length if needed

**Quarterly review:**
- Review all contracts for consistency
- Update validation rules based on production data
- Sync contract versions across skills (if using same subagent)

---

## Benefits of Contract-Based Validation

### Before Contracts (Current State)

**Problem:**
- Subagents operate autonomously
- No formal specification of expected output
- Validation is ad-hoc (different per skill)
- Violations detected late (after file creation)

**Result:**
- RCA-007 violations (5 extra files created)
- Workflow short-circuits (Phases 3-5 skipped)
- Inconsistent subagent behavior

---

### After Contracts (Enhanced State)

**Benefits:**
- ✅ Formal specification (YAML contract is source of truth)
- ✅ Consistent validation (all skills use same contract for same subagent)
- ✅ Early detection (violations caught before assembly)
- ✅ Automated recovery (re-invoke logic in contract)
- ✅ Monitoring (violation logs, success rates)
- ✅ Documentation (contract serves as subagent-skill API spec)

**Result:**
- Zero extra files (contract enforces no_file_creation)
- Workflow completes (validation ensures output format)
- Predictable subagent behavior (contract constraints)

---

## Non-Aspirational Validation

**All contract features are implementable in Claude Code Terminal:**

| Feature | Implementable? | Evidence |
|---------|----------------|----------|
| YAML parsing | ✅ YES | Python `yaml.safe_load()` (built-in) |
| Regex pattern matching | ✅ YES | Python `re` module (built-in) |
| File system checks (Glob) | ✅ YES | Glob tool available |
| Validation scripts | ✅ YES | Python scripts in `.claude/scripts/` |
| Log file writing | ✅ YES | Write tool, Bash append |
| Contract versioning | ✅ YES | YAML field (semantic versioning) |
| Error handling logic | ✅ YES | Conditional logic, retry loops |
| Monitoring metrics | ✅ YES | Log parsing, statistics calculation |

**No aspirational features:**
- ❌ Real-time contract enforcement (post-hoc validation only)
- ❌ Automatic contract generation (manual creation required)
- ❌ Contract migration tools (manual versioning)

---

## Success Criteria

### Contract Creation Success

**Per contract:**
- [ ] YAML file created in correct location
- [ ] All required fields present (skill, subagent, phase, input, output, constraints, validation, error_handling)
- [ ] Input schema complete (all parameters documented)
- [ ] Output schema complete (all sections specified)
- [ ] Constraints enforce RCA-007 fix (no_file_creation: true)
- [ ] Validation rules cover critical paths
- [ ] Error handling defines recovery logic
- [ ] Monitoring configured (logs, retries, performance)
- [ ] Changelog initialized

### Contract Enforcement Success

**Per skill:**
- [ ] Skill reads contract in validation step
- [ ] Skill validates subagent output against contract
- [ ] Violations detected correctly (100% detection rate)
- [ ] Error handling applied per contract (re_invoke, halt, etc.)
- [ ] Monitoring data logged
- [ ] Violations logged to .devforgeai/logs/

### Framework-Wide Success

- [ ] All skill-subagent integrations have contracts
- [ ] Zero contract violations in production (after Phase 1-3 rollout)
- [ ] Recovery success rate >90% (first retry succeeds)
- [ ] Validation overhead <5% of total execution time

---

## Related Documents

- **RCA:** `.devforgeai/RCA/RCA-007-multi-file-story-creation.md`
- **Implementation Plan:** `.devforgeai/specs/enhancements/RCA-007-FIX-IMPLEMENTATION-PLAN.md`
- **Prompt Enhancement:** `.devforgeai/specs/enhancements/SUBAGENT-PROMPT-ENHANCEMENT-SPEC.md`
- **Batch Creation:** `.devforgeai/specs/enhancements/BATCH-STORY-CREATION-ENHANCEMENT.md`

---

**Implementation Status:** Specification Complete - Ready for Phase 2 (Week 2)
**Priority:** MEDIUM (Phase 1 must complete first)
**Dependencies:** Phase 1 fixes (prompt constraints) should be deployed before contracts
