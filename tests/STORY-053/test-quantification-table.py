#!/usr/bin/env python3
###############################################################################
# Test Suite: STORY-053 - Quantification Table Validation
# Purpose: Validate AC3 - NFR Quantification Accuracy (≥15 vague terms)
# Tests: DOC-003, BR-003 - Table structure, measurable ranges, examples
###############################################################################

import re
import sys
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
print("STORY-053 Quantification Table Validation Tests")
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

header("AC3: NFR Quantification Accuracy")

# Test 1: Find quantification table
test_case("Quantification table exists")
table_exists = "quantification" in content.lower() or "vague term" in content.lower()
if table_exists:
    pass_test("Quantification/NFR table section found")
else:
    fail_test("Quantification table section not found")
    # Try to continue with limited functionality
    sys.exit(1)

# Test 2: Extract table section
test_case("Extract and parse quantification table")

# Look for table patterns - markdown tables or structured sections
# Strategy: find "Vague Term" or "Term" headings and extract following rows
table_section = None
table_start = None

# Look for quantification table heading
if "quantification" in content.lower():
    idx = content.lower().find("quantification")
    if idx != -1:
        # Get 5000 chars after the heading to find the table
        table_start = content[idx:idx+5000]
        table_section = table_start

# Count vague terms in table
vague_term_count = 0
measured_ranges = []
examples = []
template_links = []

if table_section:
    # Look for pipe-delimited markdown table format
    lines = table_section.split('\n')
    in_table = False
    row_count = 0

    for line in lines:
        # Check if this is a table row (contains pipes)
        if '|' in line and not line.startswith('|---'):
            if '|' in line:
                cells = [cell.strip() for cell in line.split('|')]
                if len(cells) >= 2:
                    row_count += 1
                    # First cell is the vague term
                    if cells[0] and not cells[0].startswith('-'):
                        if cells[0].lower() not in ['term', 'vague', 'category', '']:
                            vague_term_count += 1
                            # Look for numbers in other cells (measurable range)
                            for cell in cells[1:]:
                                if any(char.isdigit() for char in cell):
                                    measured_ranges.append(cell)

    # Alternative: count vague term references in content
    if vague_term_count < 5:
        # Look for patterns like "fast", "slow", "scalable", "secure", etc.
        vague_terms = [
            'fast', 'slow', 'responsive', 'quick', 'slow',
            'scalable', 'flexible', 'extensible',
            'secure', 'safe', 'reliable', 'robust',
            'efficient', 'optimal', 'performant',
            'user-friendly', 'intuitive', 'simple'
        ]
        for term in vague_terms:
            if term in content.lower():
                vague_term_count += 1

if vague_term_count >= 15:
    pass_test(f"Found {vague_term_count} vague terms (≥15 required)")
else:
    fail_test(f"Found {vague_term_count} vague terms (need ≥15)")

# Test 3: Check for measurable ranges
test_case("Vague terms have measurable target ranges")

# Look for measurable units in table
measurable_count = 0
numeric_patterns = re.findall(r'[<>=]+\s*\d+|≥\d+|≤\d+|>\d+|<\d+|\d+%|p95|p99|ms|seconds|minutes', content, re.IGNORECASE)

if len(numeric_patterns) >= 15:
    pass_test(f"Found {len(numeric_patterns)} measurable ranges")
    measurable_count = len(numeric_patterns)
else:
    fail_test(f"Found only {len(numeric_patterns)} measurable ranges (need ≥15)")

# Test 4: Check for performance metrics
test_case("Measurable ranges include numeric values or percentiles")

# Count numeric references
numeric_refs = re.findall(r'\b\d+\s*(ms|s|seconds|minutes|hours|%|percentile|p\d+)\b', content, re.IGNORECASE)
percentile_refs = re.findall(r'(p\d+|percentile|median|average)', content, re.IGNORECASE)

total_metrics = len(numeric_refs) + len(percentile_refs)

if total_metrics >= 15:
    pass_test(f"Found {total_metrics} numeric metrics or percentiles")
else:
    fail_test(f"Found only {total_metrics} numeric metrics (need ≥15)")

# Test 5: Check for DevForgeAI examples
test_case("Quantification entries include DevForgeAI context examples")

# Look for references to QA times, story creation, metrics
devforgeai_examples = re.findall(
    r'(QA|story|test|coverage|execution|workflow|phase|skill|subagent)',
    content,
    re.IGNORECASE
)

example_count = len(devforgeai_examples)

if example_count >= 10:
    pass_test(f"Found {example_count} DevForgeAI context references in examples")
else:
    fail_test(f"Found only {example_count} DevForgeAI examples (should have ≥10)")

# Test 6: Check for template links/references
test_case("Each quantification entry references a template")

# Look for references to templates or AskUserQuestion
template_refs = re.findall(r'Template:|Use template|Ask template|AskUserQuestion|See pattern', content, re.IGNORECASE)

if len(template_refs) >= 10:
    pass_test(f"Found {len(template_refs)} template references")
else:
    fail_test(f"Found only {len(template_refs)} template references (need ≥10)")

header("BR-003: Measurable Target Validation")

# Test 7: Check for specific performance targets
test_case("Table includes performance targets (latency, throughput, response time)")

performance_terms = ['response time', 'latency', 'throughput', 'requests', 'qps', 'tps', 'rps', 'milliseconds', 'seconds']
performance_count = sum(1 for term in performance_terms if term in content.lower())

if performance_count >= 3:
    pass_test(f"Found {performance_count} performance target types")
else:
    fail_test(f"Found only {performance_count} performance targets (need ≥3)")

# Test 8: Check for security targets
test_case("Table includes security/reliability targets")

security_terms = ['encryption', 'authentication', 'authorization', 'reliability', 'availability', 'uptime', 'sla', 'failure']
security_count = sum(1 for term in security_terms if term in content.lower())

if security_count >= 2:
    pass_test(f"Found {security_count} security/reliability target types")
else:
    fail_test(f"Found only {security_count} security targets (need ≥2)")

# Test 9: Check for scalability targets
test_case("Table includes scalability targets (users, data, load)")

scalability_terms = ['users', 'concurrent', 'load', 'scale', 'growth', 'capacity', 'storage', 'memory']
scalability_count = sum(1 for term in scalability_terms if term in content.lower())

if scalability_count >= 3:
    pass_test(f"Found {scalability_count} scalability target types")
else:
    fail_test(f"Found only {scalability_count} scalability targets (need ≥2)")

# Test 10: Check for usability targets
test_case("Table includes usability targets (learning curve, error rate, satisfaction)")

usability_terms = ['usability', 'learning', 'error rate', 'satisfaction', 'nps', 'csat', 'time to learn', 'completion rate']
usability_count = sum(1 for term in usability_terms if term in content.lower())

if usability_count >= 2:
    pass_test(f"Found {usability_count} usability target types")
else:
    fail_test(f"Found only {usability_count} usability targets (need ≥2)")

header("Table Format and Structure")

# Test 11: Check for table headers
test_case("Table has clear column headers")

headers = ['term', 'vague', 'range', 'measurable', 'target', 'example', 'metric', 'unit']
header_count = sum(1 for h in headers if h in content.lower())

if header_count >= 3:
    pass_test(f"Found {header_count} column header types in table")
else:
    fail_test(f"Table structure may be unclear")

# Test 12: Check for table row separator (markdown format)
test_case("Table uses proper markdown formatting (pipes and dashes)")

pipe_count = content.count('|')
dash_separator_count = content.count('|---|') + content.count('|-|')

if pipe_count >= 30 and dash_separator_count >= 1:
    pass_test(f"Table uses markdown format (pipes: {pipe_count}, separators: {dash_separator_count})")
else:
    fail_test(f"Table may not use standard markdown format")

# Test 13: Verify table completeness
test_case("Table has minimum required rows (≥15)")

# Count markdown table rows (pattern: | ... | ... | ... |)
table_rows = re.findall(r'\|\s*[^|]+\s*\|', content)
if len(table_rows) >= 15:
    pass_test(f"Table has {len(table_rows)} rows (≥15 required)")
else:
    fail_test(f"Table has only {len(table_rows)} rows (need ≥15)")

header("Unmapped Terms Handling")

# Test 14: Check for guidance on unmapped terms
test_case("Document includes guidance for unmapped vague terms")

unmapped_guidance = re.findall(r'unmapped|not found|missing|fallback|generic|custom|other', content, re.IGNORECASE)

if len(unmapped_guidance) >= 2:
    pass_test(f"Found {len(unmapped_guidance)} references to handling unmapped terms")
else:
    fail_test(f"Document should explain how to handle unmapped vague terms")

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
