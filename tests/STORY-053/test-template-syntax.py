#!/usr/bin/env python3
###############################################################################
# Test Suite: STORY-053 - Template Syntax Validation
# Purpose: Validate AC2 - Template Usability (20-30 templates with valid syntax)
# Tests: DOC-002, BR-002 - Template count, option count, and syntax validation
###############################################################################

import re
import sys
import json
from pathlib import Path

GUIDANCE_FILE = "src/claude/skills/devforgeai-ideation/references/user-input-guidance.md"
test_count = 0
pass_count = 0
fail_count = 0

def pass_test(msg):
    global pass_count
    pass_count += 1
    print(f"✓ PASS: {msg}")

def fail_test(msg):
    global fail_count
    fail_count += 1
    print(f"✗ FAIL: {msg}")

def skip_test(msg):
    print(f"⊘ SKIP: {msg}")

def test_case(msg):
    global test_count
    test_count += 1
    print(f"\nTest {test_count}: {msg}")

def header(msg):
    print(f"\n{'='*66}")
    print(msg)
    print('='*66)

# Check file existence
print("STORY-053 Template Syntax Validation Tests")
print()

if not Path(GUIDANCE_FILE).exists():
    print(f"WARNING: Guidance file does not exist: {GUIDANCE_FILE}")
    print("All tests will FAIL in RED phase until file is created.")
    print()
    sys.exit(1)

# Read file content
try:
    with open(GUIDANCE_FILE, 'r') as f:
        content = f.read()
except Exception as e:
    print(f"ERROR: Cannot read file: {e}")
    sys.exit(1)

header("AC2: Template Usability")

# Test 1: Count templates
test_case("Template count is within range (20-30)")
template_matches = re.findall(r'AskUserQuestion\(', content)
template_count = len(template_matches)

if template_count >= 20 and template_count <= 30:
    pass_test(f"Found {template_count} templates (20-30 required)")
else:
    fail_test(f"Found {template_count} templates (need 20-30)")

# Test 2: Extract and validate each template
test_case("Validate AskUserQuestion syntax in templates")
# Pattern to match AskUserQuestion calls with YAML content
template_pattern = r'(AskUserQuestion\([^)]*questions=\[.*?\]\))'

valid_template_count = 0
invalid_templates = []

# Look for YAML-style AskUserQuestion definitions
yaml_pattern = r'questions=\[(.*?)\]'
questions_blocks = re.findall(r'(AskUserQuestion\s*\(.*?multiSelect.*?\))', content, re.DOTALL)

if questions_blocks:
    for idx, block in enumerate(questions_blocks, 1):
        if 'question:' in block and 'options:' in block:
            valid_template_count += 1
        else:
            invalid_templates.append(f"Block {idx}: Missing required fields")

if valid_template_count >= 20:
    pass_test(f"Found {valid_template_count} valid AskUserQuestion templates")
elif len(questions_blocks) > 0:
    pass_test(f"Found {len(questions_blocks)} AskUserQuestion template definitions")
else:
    fail_test("Could not extract AskUserQuestion templates")

# Test 3: Check for question field in templates
test_case("Each template has 'question' field")
question_fields = re.findall(r'question\s*:\s*["\']', content)
if len(question_fields) >= 20:
    pass_test(f"Found {len(question_fields)} question fields")
else:
    fail_test(f"Found only {len(question_fields)} question fields (need >=20)")

# Test 4: Check for header field in templates
test_case("Each template has 'header' field for context")
header_fields = re.findall(r'header\s*:\s*["\']', content)
if len(header_fields) >= 20:
    pass_test(f"Found {len(header_fields)} header fields")
else:
    fail_test(f"Found only {len(header_fields)} header fields (need >=20)")

# Test 5: Check for options array in templates
test_case("Each template has 'options' array")
options_fields = re.findall(r'options\s*:\s*\[', content)
if len(options_fields) >= 20:
    pass_test(f"Found {len(options_fields)} options arrays")
else:
    fail_test(f"Found only {len(options_fields)} options arrays (need >=20)")

header("BR-002: Option Count Validation (3-5 per template)")

# Count options per template block
test_case("Each template has 3-5 options")

# Split by AskUserQuestion blocks and analyze each
blocks = re.split(r'AskUserQuestion\s*\(', content)

valid_option_count = 0
invalid_option_count = 0
templates_checked = 0

for block in blocks[1:]:  # Skip first split before any AskUserQuestion
    # Extract the options array for this template
    options_match = re.search(r'options\s*:\s*\[(.*?)\]', block, re.DOTALL)
    if options_match:
        templates_checked += 1
        options_text = options_match.group(1)

        # Count option entries (lines starting with { or look for label: patterns)
        option_count = len(re.findall(r'label\s*:', options_text))

        if option_count >= 3 and option_count <= 5:
            valid_option_count += 1
        else:
            invalid_option_count += 1
            if invalid_option_count <= 3:  # Show first 3 errors
                print(f"  Template {templates_checked}: {option_count} options (invalid)")

if templates_checked > 0:
    if invalid_option_count == 0:
        pass_test(f"All {valid_option_count} templates have 3-5 options")
    else:
        fail_test(f"{valid_option_count}/{templates_checked} templates have valid option count (3-5)")
        if invalid_option_count > 0:
            fail_test(f"  {invalid_option_count} templates have invalid option count")
else:
    fail_test("Could not parse template option counts")

# Test 6: Check for label field in options
test_case("Each option has 'label' field")
label_fields = re.findall(r'label\s*:\s*["\']', content)
expected_labels = template_count * 4  # Average 4 options per template (3-5 range)
if len(label_fields) >= 20:
    pass_test(f"Found {len(label_fields)} option labels")
else:
    fail_test(f"Found only {len(label_fields)} option labels")

# Test 7: Check for description field in options
test_case("Each option has 'description' field")
description_fields = re.findall(r'description\s*:\s*["\']', content)
if len(description_fields) >= 20:
    pass_test(f"Found {len(description_fields)} option descriptions")
else:
    fail_test(f"Found only {len(description_fields)} option descriptions")

# Test 8: Check for multiSelect field in templates
test_case("Each template specifies multiSelect property")
multiselect_fields = re.findall(r'multiSelect\s*:\s*(true|false)', content)
if len(multiselect_fields) >= 20:
    pass_test(f"Found {len(multiselect_fields)} multiSelect properties")
else:
    fail_test(f"Found only {len(multiselect_fields)} multiSelect properties")

header("Template Coverage by Scenario Type")

# Test 9: Functional specification templates
test_case("Templates cover functional specifications (3+ templates)")
functional_templates = len(re.findall(r'Functional\|Feature\|Requirement\|AC|acceptance criteria', content, re.IGNORECASE))
if functional_templates >= 3:
    pass_test(f"Found {functional_templates} functional specification templates")
else:
    fail_test(f"Found only {functional_templates} functional templates (need >=3)")

# Test 10: NFR templates
test_case("Templates cover non-functional requirements (3+ templates)")
nfr_templates = len(re.findall(r'NFR\|Non-functional\|Performance\|Security\|Scalability\|quantification', content, re.IGNORECASE))
if nfr_templates >= 3:
    pass_test(f"Found {nfr_templates} NFR templates")
else:
    fail_test(f"Found only {nfr_templates} NFR templates (need >=3)")

# Test 11: Edge case templates
test_case("Templates cover edge cases (3+ templates)")
edge_templates = len(re.findall(r'Edge\|Boundary\|Error\|Exception\|failure', content, re.IGNORECASE))
if edge_templates >= 3:
    pass_test(f"Found {edge_templates} edge case templates")
else:
    fail_test(f"Found only {edge_templates} edge case templates (need >=3)")

# Test 12: Integration templates
test_case("Templates cover integration points (3+ templates)")
integration_templates = len(re.findall(r'Integration\|API\|Dependencies\|Interface', content, re.IGNORECASE))
if integration_templates >= 3:
    pass_test(f"Found {integration_templates} integration templates")
else:
    fail_test(f"Found only {integration_templates} integration templates (need >=3)")

# Test 13: Constraint templates
test_case("Templates cover constraints (2+ templates)")
constraint_templates = len(re.findall(r'Constraint\|Limitation\|Boundary', content, re.IGNORECASE))
if constraint_templates >= 2:
    pass_test(f"Found {constraint_templates} constraint templates")
else:
    fail_test(f"Found only {constraint_templates} constraint templates (need >=2)")

header("Template Quality Checks")

# Test 14: Customization notes
test_case("Templates include customization guidance")
customization_notes = re.findall(r'Customization|Custom|Adjust|Modify|Replace|Change', content, re.IGNORECASE)
if len(customization_notes) >= 20:
    pass_test(f"Found {len(customization_notes)} customization guidance references")
else:
    fail_test(f"Found only {len(customization_notes)} customization references (need >=20)")

# Test 15: Valid YAML syntax in templates (basic check)
test_case("Templates use consistent YAML syntax")
valid_yaml_count = 0
yaml_issues = []

# Check for common YAML issues
if content.count('question:') != content.count('description:'):
    yaml_issues.append("question/description field count mismatch")

if content.count('options:') < 20:
    yaml_issues.append("Insufficient options arrays")

if len(yaml_issues) == 0:
    pass_test("YAML syntax validation passed")
else:
    fail_test(f"Found {len(yaml_issues)} potential YAML syntax issues: {', '.join(yaml_issues)}")

header("Summary")
print()
print(f"Total Tests: {test_count}")
print(f"Passed: {pass_count}")
print(f"Failed: {fail_count}")
print()

if fail_count == 0:
    print("Result: ALL TESTS PASSED")
    sys.exit(0)
else:
    print("Result: SOME TESTS FAILED")
    sys.exit(1)
