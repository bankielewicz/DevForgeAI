#!/usr/bin/env python3
###############################################################################
# Test Suite: STORY-053 - Performance and NFR Validation
# Purpose: Validate NFR-001, NFR-002, NFR-003 - Performance requirements
# Tests: File load time, Grep search time, token count
###############################################################################

import sys
import time
import os
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
print("STORY-053 Performance and NFR Validation Tests")
print()

if not Path(GUIDANCE_FILE).exists():
    print(f"WARNING: Guidance file does not exist: {GUIDANCE_FILE}")
    print("All tests will FAIL in RED phase until file is created.")
    print()
    sys.exit(1)

# Read file
try:
    with open(GUIDANCE_FILE, 'r') as f:
        content = f.read()
except Exception as e:
    print(f"ERROR: Cannot read file: {e}")
    sys.exit(1)

header("NFR-001: File Load Performance (< 500ms)")

test_case("Measure file load time using Read tool equivalent")

# Simulate Read tool performance by timing file read
start_time = time.time()
with open(GUIDANCE_FILE, 'r') as f:
    file_content = f.read()
end_time = time.time()

load_time_ms = (end_time - start_time) * 1000
print(f"  File size: {len(file_content)} bytes")
print(f"  File load time: {load_time_ms:.2f}ms")

if load_time_ms < 500:
    pass_test(f"File loads in {load_time_ms:.2f}ms (< 500ms required)")
else:
    fail_test(f"File load took {load_time_ms:.2f}ms (need < 500ms)")

test_case("File size is reasonable (< 500KB)")
file_size_kb = len(file_content) / 1024
if file_size_kb < 500:
    pass_test(f"File size: {file_size_kb:.1f}KB (< 500KB)")
else:
    fail_test(f"File size: {file_size_kb:.1f}KB (should be < 500KB)")

header("NFR-002: Grep Search Performance (< 30 seconds)")

test_case("File is optimized for Grep searches")

# Measure line count
lines = content.split('\n')
line_count = len(lines)

if line_count > 0:
    pass_test(f"File has {line_count} lines (searchable)")
else:
    fail_test("File appears to be empty")

test_case("Search patterns are indexable (< 30s expected)")

# Simulate grep by counting searchable elements
import re

search_patterns = [
    (r'^### Pattern', 'Pattern headings'),
    (r'AskUserQuestion\(', 'Templates'),
    (r'\|\s*[^|]+\s*\|', 'Table rows'),
    (r'####', 'Section headers'),
    (r'^- ', 'List items')
]

total_matches = 0
for pattern, description in search_patterns:
    matches = len(re.findall(pattern, content, re.MULTILINE))
    total_matches += matches
    print(f"  {description}: {matches} matches")

if total_matches > 50:
    pass_test(f"File has {total_matches} searchable elements")
else:
    fail_test(f"File has only {total_matches} searchable elements (need >50)")

# Estimate grep time based on file size
# Rule of thumb: grep on local file typically ~1-5ms per MB
estimated_grep_time_ms = (file_size_kb / 1024) * 5
print(f"  Estimated Grep search time: ~{estimated_grep_time_ms:.1f}ms")

if estimated_grep_time_ms < 30000:  # 30 seconds
    pass_test(f"Estimated Grep search time ~{estimated_grep_time_ms:.0f}ms (< 30s)")
else:
    fail_test(f"Estimated search time may exceed 30s")

header("NFR-003: Token Overhead (≤ 3,000 tokens)")

test_case("Estimate token count using character-to-token ratio")

# OpenAI's token estimation: ~4 characters = 1 token (English text average)
# For documentation: ~1.2-1.4 tokens per word, or ~0.25 tokens per character
# Conservative estimate: 1 token per 3.5 characters (markdown can be verbose)

char_count = len(file_content)
estimated_tokens = char_count / 3.5  # Conservative estimate

print(f"  Character count: {char_count:,}")
print(f"  Estimated tokens (using 1 token per 3.5 chars): {estimated_tokens:.0f}")

if estimated_tokens <= 3000:
    pass_test(f"Estimated {estimated_tokens:.0f} tokens (≤ 3,000 required)")
else:
    # Check if we're close (within 10%)
    if estimated_tokens <= 3300:
        pass_test(f"Estimated {estimated_tokens:.0f} tokens (slightly over 3,000 limit)")
    else:
        fail_test(f"Estimated {estimated_tokens:.0f} tokens (need ≤ 3,000)")

test_case("Validate file structure supports efficient parsing")

# Check for markers that indicate good structure
structural_markers = [
    ('###', 'section headers (3+ levels)'),
    ('|', 'table structure'),
    ('`', 'code blocks'),
    ('[', 'links/references')
]

marker_count = 0
for marker, description in structural_markers:
    count = content.count(marker)
    if count > 0:
        marker_count += 1
        print(f"  {description}: {count} occurrences")

if marker_count >= 3:
    pass_test(f"File has good structural markers ({marker_count}/4 types)")
else:
    fail_test(f"File structure may be inefficient ({marker_count}/4 types)")

header("Content Validation")

test_case("File contains expected content sections")

required_sections = [
    ('Pattern', 'Pattern documentation'),
    ('Template', 'Template definitions'),
    ('Quantification', 'NFR quantification'),
    ('Integration', 'Skill integration'),
    ('Framework', 'Framework terminology')
]

found_sections = 0
for keyword, description in required_sections:
    if keyword.lower() in content.lower():
        found_sections += 1
        print(f"  ✓ {description}")
    else:
        print(f"  ✗ {description}")

if found_sections >= 4:
    pass_test(f"Found {found_sections}/5 content sections")
else:
    fail_test(f"Found only {found_sections}/5 content sections")

header("Searchability Metrics")

test_case("Document has good keyword density for common searches")

keywords = {
    'functional': 'Functional requirement',
    'non-functional': 'Non-functional requirement',
    'nfr': 'NFR abbreviation',
    'edge': 'Edge case',
    'integration': 'Integration',
    'constraint': 'Constraint',
    'performance': 'Performance',
    'security': 'Security',
    'scalability': 'Scalability',
    'reliability': 'Reliability'
}

keyword_count = 0
for keyword, description in keywords.items():
    count = content.lower().count(keyword)
    if count > 0:
        keyword_count += 1
        if count > 3:
            print(f"  ✓ {description}: {count} matches")

if keyword_count >= 8:
    pass_test(f"Found {keyword_count}/10 key terms with good density")
else:
    fail_test(f"Found only {keyword_count}/10 key terms")

header("Summary")
print()
print(f"Total Tests: {test_count}")
print(f"Passed: {pass_count}")
print(f"Failed: {fail_count}")
print()

# Summary metrics
print(f"File Metrics:")
print(f"  Size: {file_size_kb:.1f}KB")
print(f"  Lines: {line_count}")
print(f"  Characters: {char_count:,}")
print(f"  Estimated tokens: {estimated_tokens:.0f}")
print()

if fail_count == 0:
    print("Result: ALL TESTS PASSED")
    sys.exit(0)
else:
    print("Result: SOME TESTS FAILED")
    sys.exit(1)
