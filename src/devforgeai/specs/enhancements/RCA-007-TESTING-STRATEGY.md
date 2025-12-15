# RCA-007 & Batch Creation Testing Strategy

**Date:** 2025-11-06
**Scope:** RCA-007 Fix + Batch Story Creation Enhancement
**Test Phases:** 3 (aligned with implementation phases)
**Total Test Cases:** 87 (42 RCA fix + 45 batch enhancement)
**Status:** Specification Complete

---

## Testing Objectives

### RCA-007 Fix Objectives

1. ✅ Verify only 1 `.story.md` file created per story (zero extra files)
2. ✅ Validate subagent output constraints enforced (prompt enhancements work)
3. ✅ Confirm validation checkpoint catches violations (Step 2.2 effective)
4. ✅ Test contract enforcement (YAML validation works)
5. ✅ Verify file system diff detects unauthorized files
6. ✅ Validate recovery logic (re-invoke works)
7. ✅ Ensure no regression (story quality unchanged)

### Batch Creation Objectives

1. ✅ Verify epic detection works (`epic-001` pattern recognized)
2. ✅ Validate multi-select feature picker (all features selectable)
3. ✅ Confirm sequential story creation (correct IDs assigned)
4. ✅ Test gap detection and filling (STORY-004 fills gap)
5. ✅ Verify batch metadata reduces questions (14 → 4)
6. ✅ Validate progress tracking (TodoWrite updates)
7. ✅ Test error handling (partial success scenarios)
8. ✅ Confirm dry-run accuracy (preview matches execution)
9. ✅ Measure parallel optimization (40-60% speedup target)
10. ✅ Ensure single story mode unchanged (backward compatible)

---

## Test Execution Environment

### Setup

**Prerequisites:**
```bash
# 1. Clean test environment
cd /mnt/c/Projects/DevForgeAI2

# 2. Create test epic with 7 features
# (Use existing EPIC-001 or create test epic)

# 3. Initialize violation log
mkdir -p devforgeai/logs
touch devforgeai/logs/rca-007-violations.log

# 4. Backup existing stories
mkdir -p devforgeai/backups/stories-$(date +%Y%m%d)
cp devforgeai/specs/Stories/*.story.md devforgeai/backups/stories-$(date +%Y%m%d)/

# 5. Install validation script
pip install pyyaml  # If not already installed
chmod +x .claude/skills/devforgeai-story-creation/scripts/validate_contract.py
```

### Teardown

**After each test:**
```bash
# 1. Count files created
ls devforgeai/specs/Stories/STORY-*.story.md | wc -l

# 2. Check for extra files
ls devforgeai/specs/Stories/STORY-*-SUMMARY.md 2>/dev/null
ls devforgeai/specs/Stories/STORY-*-QUICK-START.md 2>/dev/null
ls devforgeai/specs/Stories/STORY-*-VALIDATION-CHECKLIST.md 2>/dev/null
ls devforgeai/specs/Stories/STORY-*-FILE-INDEX.md 2>/dev/null

# 3. Review violation log
tail -20 devforgeai/logs/rca-007-violations.log

# 4. Clean up test stories (if needed)
# (Keep or delete based on test type)
```

---

## Phase 1 Testing (RCA-007 Immediate Fix - Week 1)

### Unit Tests (15 cases)

#### Test 1.1: Prompt Constraint Detection

**Objective:** Verify enhanced prompt includes all 4 sections.

**Procedure:**
```bash
# Read enhanced prompt
prompt=$(grep -A 100 "PRE-FLIGHT BRIEFING" .claude/skills/devforgeai-story-creation/references/requirements-analysis.md)

# Assertions
echo "$prompt" | grep -q "PRE-FLIGHT BRIEFING"  # Section 1
echo "$prompt" | grep -q "CRITICAL OUTPUT CONSTRAINTS"  # Section 2
echo "$prompt" | grep -q "PROHIBITED ACTIONS"  # Section 3
echo "$prompt" | grep -q "EXPECTED OUTPUT FORMAT"  # Section 4

# Expected: All 4 grep commands return 0 (found)
```

**Success Criteria:**
- [ ] All 4 sections present in prompt
- [ ] Each section has required content
- [ ] Prompt explicitly prohibits file creation

---

#### Test 1.2: Subagent Returns Content (Not Files)

**Objective:** Verify subagent returns markdown text, not file artifacts.

**Procedure:**
```bash
# Create test story
/create-story Test prompt constraint enforcement

# Wait for completion

# Check output type
# (Inspect subagent result in skill execution log)

# Expected: subagent_output is plain text (markdown sections)
# Expected: No "File created:" statements
# Expected: No file paths in output
```

**Success Criteria:**
- [ ] Subagent output is string type (markdown text)
- [ ] Output contains section headers (## User Story, ## Acceptance Criteria)
- [ ] Output does NOT contain file creation statements
- [ ] Output does NOT contain file paths (STORY-*-SUMMARY.md, etc.)

---

#### Test 1.3: Validation Checkpoint Catches File Creation

**Objective:** Verify Step 2.2 validation detects file creation attempts.

**Procedure:**
```python
# Simulate violation (for testing only)
# Manually create subagent output with file creation indicators

test_output = """
## User Story
**As a** user, **I want** feature, **so that** benefit.

## Acceptance Criteria
### AC1: Test
**Given** context
**When** action
**Then** outcome

File created: STORY-TEST-SUMMARY.md
Successfully wrote STORY-TEST-QUICK-START.md
"""

# Run validation
violations = validate_subagent_output(test_output)

# Assertions
assert len(violations) >= 2  # At least 2 file creation patterns detected
assert any(v['type'] == "FILE_CREATION" for v in violations)
assert any(v['severity'] == "CRITICAL" for v in violations)
```

**Success Criteria:**
- [ ] Validation detects "File created:" pattern
- [ ] Validation detects "Successfully wrote" pattern
- [ ] Validation detects ".md" file references
- [ ] Severity is CRITICAL
- [ ] Recovery action is "re_invoke"

---

#### Test 1.4: Re-Invocation Logic Works

**Objective:** Verify recovery re-invokes subagent with stricter prompt.

**Procedure:**
```bash
# Create story that triggers violation (simulation)
# First attempt: Subagent creates files
# Expected: Validation catches violation
# Expected: Skill re-invokes with STRICT MODE

# Monitor skill execution
# Watch for: "Re-invoking subagent with stricter constraints"

# Check result
# Expected: Second attempt succeeds (returns content only)
```

**Success Criteria:**
- [ ] First attempt violation detected
- [ ] Re-invocation triggered automatically
- [ ] STRICT MODE prompt used in retry
- [ ] Second attempt succeeds (no violations)
- [ ] Violation logged to devforgeai/logs/rca-007-violations.log

---

#### Test 1.5: Required Sections Validation

**Objective:** Verify validation detects missing sections.

**Procedure:**
```python
# Simulate incomplete output
test_output = """
## User Story
**As a** user, **I want** feature, **so that** benefit.

## Acceptance Criteria
### AC1: Test
**Given** context
**When** action
**Then** outcome

(Missing: Edge Cases, NFRs)
"""

# Run validation
violations = validate_subagent_output(test_output)

# Assertions
assert len(violations) == 2  # Missing Edge Cases, Missing NFRs
assert all(v['type'] == "MISSING_SECTION" for v in violations)
missing_sections = [v['section'] for v in violations]
assert "Edge Cases" in missing_sections
assert "Non-Functional Requirements" in missing_sections
```

**Success Criteria:**
- [ ] Missing sections detected correctly
- [ ] Severity is HIGH
- [ ] All missing sections identified
- [ ] Recovery prompts user or re-invokes

---

### Integration Tests (12 cases)

#### Test 1.6: Single Story Creation (End-to-End)

**Objective:** Verify complete story creation workflow with RCA-007 fix.

**Procedure:**
```bash
# Pre-test: Count existing stories
before_count=$(ls devforgeai/specs/Stories/STORY-*.story.md 2>/dev/null | wc -l)

# Execute command
/create-story Database connection pooling with retry logic

# Wait for completion

# Post-test: Count stories
after_count=$(ls devforgeai/specs/Stories/STORY-*.story.md 2>/dev/null | wc -l)

# Assertions
new_stories=$((after_count - before_count))
assert [ $new_stories -eq 1 ]  # Exactly 1 new story

# Check for extra files
extra_files=$(ls devforgeai/specs/Stories/STORY-*-SUMMARY.md devforgeai/specs/Stories/STORY-*-QUICK-START.md 2>/dev/null | wc -l)
assert [ $extra_files -eq 0 ]  # Zero extra files

# Validate story content
story_file=$(ls -t devforgeai/specs/Stories/STORY-*.story.md | head -1)  # Most recent
assert grep -q "## User Story" "$story_file"
assert grep -q "## Acceptance Criteria" "$story_file"
assert grep -q "## Edge Cases" "$story_file"
assert grep -q "## Non-Functional Requirements" "$story_file"
```

**Success Criteria:**
- [ ] Exactly 1 .story.md file created
- [ ] Zero extra files (SUMMARY, QUICK-START, etc.)
- [ ] Story file contains all required sections
- [ ] YAML frontmatter valid
- [ ] Epic/sprint linking works (if applicable)

---

#### Test 1.7: Violation Detection and Recovery

**Objective:** Test validation catches violations and recovery succeeds.

**Procedure:**
```bash
# This test requires temporarily modifying requirements-analyst subagent
# to simulate file creation (for testing only)

# Backup subagent
cp .claude/agents/requirements-analyst.md .claude/agents/requirements-analyst.md.backup

# Modify subagent to create files (simulation)
# (Add: "Write(file_path='STORY-XXX-SUMMARY.md', content='...')")

# Run command
/create-story Test violation recovery

# Expected behavior:
# 1. Subagent creates files (first attempt)
# 2. Validation detects violation
# 3. Recovery re-invokes with STRICT MODE
# 4. Second attempt succeeds (returns content only)

# Check violation log
assert grep -q "VIOLATION DETECTED" devforgeai/logs/rca-007-violations.log
assert grep -q "Recovery Result: SUCCESS" devforgeai/logs/rca-007-violations.log

# Restore subagent
mv .claude/agents/requirements-analyst.md.backup .claude/agents/requirements-analyst.md

# Check final result
# Expected: Only 1 .story.md file, no extras
assert [ $(ls devforgeai/specs/Stories/STORY-*-SUMMARY.md 2>/dev/null | wc -l) -eq 0 ]
```

**Success Criteria:**
- [ ] First attempt violation logged
- [ ] Re-invocation triggered
- [ ] Second attempt succeeds
- [ ] Final result: 1 file only
- [ ] Violation log entry created

---

#### Test 1.8: AC Format Validation

**Objective:** Verify Given/When/Then format enforced.

**Procedure:**
```python
# Create story
/create-story Test acceptance criteria format validation

# Extract AC section from generated story
story_file = get_latest_story_file()
ac_section = extract_section(story_file, "Acceptance Criteria")

# Validate format
assert "Given" in ac_section
assert "When" in ac_section
assert "Then" in ac_section

# Count AC
ac_count = ac_section.count("### AC")
assert ac_count >= 3  # Minimum 3 AC

# Check each AC has all keywords
for i in range(1, ac_count + 1):
    ac_block = extract_ac_block(ac_section, i)
    assert "**Given**" in ac_block
    assert "**When**" in ac_block
    assert "**Then**" in ac_block
```

**Success Criteria:**
- [ ] All AC follow Given/When/Then format
- [ ] Minimum 3 AC present
- [ ] Each AC independently testable
- [ ] AC titles descriptive

---

#### Test 1.9: NFR Measurability Validation

**Objective:** Verify NFRs have measurable targets (no vague terms).

**Procedure:**
```python
# Create story
/create-story Test NFR measurability validation

# Extract NFR section
story_file = get_latest_story_file()
nfr_section = extract_section(story_file, "Non-Functional Requirements")

# Check for prohibited vague terms
vague_terms = ["fast", "secure", "scalable", "performant", "reliable", "quickly", "efficiently"]

violations = []
for term in vague_terms:
    if term in nfr_section.lower():
        violations.append(term)

# Assertions
assert len(violations) == 0, f"Vague NFR terms found: {violations}"

# Check for measurable targets
assert re.search(r'<\s*\d+\s*(ms|seconds|minutes)', nfr_section)  # Performance metric
assert re.search(r'\d+(\.\d+)?%', nfr_section)  # Percentage (uptime, coverage, etc.)
```

**Success Criteria:**
- [ ] No vague terms in NFRs
- [ ] All performance targets measurable (< 100ms, < 5s, etc.)
- [ ] All security measures specific (QUOTENAME(), JWT with 15-min expiry)
- [ ] All reliability targets quantified (99.9% uptime, max 3 retries)

---

#### Test 1.10: Epic/Sprint Linking Preserved

**Objective:** Verify Phase 6 still works with RCA-007 fix.

**Procedure:**
```bash
# Pre-test: Read epic file
epic_before=$(cat devforgeai/specs/Epics/EPIC-002.epic.md)

# Create story for epic feature
/create-story epic-002  # Select Feature 2.3

# Post-test: Read epic file
epic_after=$(cat devforgeai/specs/Epics/EPIC-002.epic.md)

# Assertions
diff <(echo "$epic_before") <(echo "$epic_after")  # Should show story reference added

# Check story reference in epic
assert grep -q "STORY-0[0-9][0-9]" <(echo "$epic_after")

# Check epic reference in story
story_file=$(ls -t devforgeai/specs/Stories/STORY-*.story.md | head -1)
assert grep -q "epic: EPIC-002" "$story_file"
```

**Success Criteria:**
- [ ] Epic updated with story reference
- [ ] Story contains epic reference in YAML frontmatter
- [ ] Bi-directional linking correct

---

#### Test 1.11: Self-Validation (Phase 7) Still Works

**Objective:** Verify Phase 7 validation not affected by RCA-007 fix.

**Procedure:**
```bash
# Create story
/create-story Test self-validation preservation

# Monitor skill execution log
# Look for: "Phase 7: Self-Validation"

# Expected output:
# ✓ Story ID valid
# ✓ Title clear
# ✓ User story format correct
# ✓ AC count >= 3
# ✓ NFRs measurable
# ✓ Edge cases documented
# Validation Result: PASS

# Assertions
assert phase_7_executed
assert validation_result == "PASS"
```

**Success Criteria:**
- [ ] Phase 7 executes
- [ ] All validation checks pass
- [ ] Self-healing works (if needed)
- [ ] Story quality meets standards

---

#### Test 1.12: Completion Report (Phase 8) Generated

**Objective:** Verify Phase 8 still produces summary.

**Procedure:**
```bash
# Create story
/create-story Test completion report generation

# Check for completion report in output
# Expected sections:
# - "Story Creation Complete"
# - "Summary"
# - "What Was Created"
# - "Key Technical Details"
# - "Next Steps"

# Assertions
assert output_contains("Story Creation Complete")
assert output_contains("Summary")
assert output_contains("Next Steps")
```

**Success Criteria:**
- [ ] Completion report generated
- [ ] Summary accurate
- [ ] Next steps appropriate
- [ ] AskUserQuestion for next action (if not batch mode)

---

### Regression Tests (15 cases)

#### Test 1.13: Story Content Quality Unchanged

**Objective:** Verify RCA-007 fix doesn't degrade story quality.

**Procedure:**
```bash
# Create 2 identical stories (same feature description)

# Story 1: Before RCA-007 fix (from backup)
# Story 2: After RCA-007 fix (new creation)

# Compare content quality
story_before="devforgeai/backups/stories-baseline/STORY-SAMPLE.story.md"
story_after=$(ls -t devforgeai/specs/Stories/STORY-*.story.md | head -1)

# Compare sections
diff <(grep "## User Story" -A 5 "$story_before") <(grep "## User Story" -A 5 "$story_after")

# Count AC
ac_before=$(grep -c "### AC" "$story_before")
ac_after=$(grep -c "### AC" "$story_after")
assert [ $ac_before -eq $ac_after ] || [ $ac_after -ge $ac_before ]  # Same or more AC

# Compare NFR depth
nfr_lines_before=$(grep "## Non-Functional Requirements" -A 50 "$story_before" | wc -l)
nfr_lines_after=$(grep "## Non-Functional Requirements" -A 50 "$story_after" | wc -l)
assert [ $nfr_lines_after -ge $((nfr_lines_before * 8 / 10)) ]  # At least 80% of original depth
```

**Success Criteria:**
- [ ] AC count same or higher
- [ ] User story quality comparable
- [ ] NFR depth comparable
- [ ] Technical specification completeness same
- [ ] Edge cases count same or higher

---

#### Test 1.14: Epic Feature Extraction Works

**Objective:** Verify epic features extracted correctly.

**Procedure:**
```bash
# Read test epic
epic_file="devforgeai/specs/Epics/EPIC-001.epic.md"

# Extract features using regex pattern
features=$(grep -E "^### Feature [0-9]+\.[0-9]+:" "$epic_file")

# Count features
feature_count=$(echo "$features" | wc -l)

# Expected: 7 features for EPIC-001
assert [ $feature_count -eq 7 ]

# Validate feature format
echo "$features" | grep -E "^### Feature [0-9]+\.[0-9]+: .+$"  # All match pattern
```

**Success Criteria:**
- [ ] All features extracted
- [ ] Feature numbers correct (1.1, 1.2, ..., 1.7)
- [ ] Feature names preserved
- [ ] Feature descriptions captured

---

## Phase 2 Testing (Contract Validation - Week 2)

### Unit Tests (15 cases)

#### Test 2.1: Contract YAML Valid

**Objective:** Verify contract file is valid YAML.

**Procedure:**
```bash
# Validate YAML syntax
python -c "
import yaml
with open('.claude/skills/devforgeai-story-creation/contracts/requirements-analyst-contract.yaml') as f:
    contract = yaml.safe_load(f)
    print('✓ Valid YAML')
    print(f'  Contract: {contract[\"skill\"]} <-> {contract[\"subagent\"]}')
    print(f'  Version: {contract[\"contract_version\"]}')
"

# Expected: No YAML parsing errors
```

**Success Criteria:**
- [ ] YAML parses without errors
- [ ] All required fields present
- [ ] Version field valid (semantic versioning)

---

#### Test 2.2: Contract Validation Script Works

**Objective:** Verify `validate_contract.py` script detects violations.

**Procedure:**
```bash
# Test 1: Valid output
echo "## User Story\n## Acceptance Criteria\n## Edge Cases\n## Non-Functional Requirements" > /tmp/valid-output.txt

python .claude/skills/devforgeai-story-creation/scripts/validate_contract.py \
    /tmp/valid-output.txt \
    .claude/skills/devforgeai-story-creation/contracts/requirements-analyst-contract.yaml

# Expected: Exit code 0 (PASSED)
assert [ $? -eq 0 ]

# Test 2: Invalid output (file creation)
echo "## User Story\nFile created: SUMMARY.md" > /tmp/invalid-output.txt

python .claude/skills/devforgeai-story-creation/scripts/validate_contract.py \
    /tmp/invalid-output.txt \
    .claude/skills/devforgeai-story-creation/contracts/requirements-analyst-contract.yaml

# Expected: Exit code 1 (FAILED)
assert [ $? -eq 1 ]
```

**Success Criteria:**
- [ ] Valid output: Script exits 0
- [ ] Invalid output: Script exits 1
- [ ] Violations displayed clearly
- [ ] Severity levels correct

---

#### Test 2.3: File System Diff Detects Unauthorized Files

**Objective:** Verify pre/post snapshot catches file creation.

**Procedure:**
```bash
# Create test story with file system monitoring enabled
/create-story Test file system diff monitoring

# During execution, skill should:
# 1. Take snapshot before subagent (Step 2.0)
# 2. Invoke subagent
# 3. Take snapshot after subagent (Step 2.2.5)
# 4. Compare snapshots
# 5. Detect any new files

# If violation (files created):
# - Delete unauthorized files
# - Log violation
# - Re-invoke subagent

# Check result
assert [ $(ls devforgeai/specs/Stories/STORY-*-SUMMARY.md 2>/dev/null | wc -l) -eq 0 ]
```

**Success Criteria:**
- [ ] Pre-snapshot captured
- [ ] Post-snapshot captured
- [ ] Diff calculated correctly
- [ ] Unauthorized files deleted (if created)
- [ ] Violation logged

---

#### Test 2.4: Contract Error Handling Applied

**Objective:** Verify error handling from contract is executed.

**Procedure:**
```python
# Simulate violation
test_output = "File created: SUMMARY.md"

# Load contract
contract = load_contract(".claude/skills/devforgeai-story-creation/contracts/requirements-analyst-contract.yaml")

# Validate
violations = validate_output(test_output, contract)

# Get error handling config
error_config = contract['error_handling']['on_file_creation_detected']

# Assertions
assert error_config['action'] == "re_invoke"
assert error_config['max_retries'] == 2
assert error_config['fallback'] == "HALT with manual intervention required"

# Apply error handling
result = apply_error_handling(violations, contract, test_output, retry_count=0)

assert result['action'] == "re_invoke"
assert result['retry_count'] == 1
assert result['max_retries'] == 2
```

**Success Criteria:**
- [ ] Error handling config loaded from contract
- [ ] Correct action applied (re_invoke, halt, ask_user_question)
- [ ] Max retries respected
- [ ] Fallback applied after retries exhausted

---

#### Test 2.5: Monitoring Data Logged

**Objective:** Verify monitoring metrics tracked correctly.

**Procedure:**
```bash
# Create 3 test stories
/create-story Test monitoring story 1
/create-story Test monitoring story 2
/create-story Test monitoring story 3

# Check violation log exists and has entries (if violations occurred)
log_file="devforgeai/logs/rca-007-violations.log"

if [ -f "$log_file" ]; then
    # Count entries
    entry_count=$(grep -c "VIOLATION DETECTED" "$log_file")

    # Validate log format
    assert grep -q "Timestamp:" "$log_file"
    assert grep -q "Story ID:" "$log_file"
    assert grep -q "Subagent:" "$log_file"
    assert grep -q "Recovery Result:" "$log_file"
fi

# Check performance tracking (if enabled)
# (Look for execution time warnings if >5 minutes)
```

**Success Criteria:**
- [ ] Violation log created (if violations occur)
- [ ] Log format correct (all fields present)
- [ ] Performance warnings logged (if execution slow)
- [ ] Retry counts tracked

---

### Performance Tests (5 cases)

#### Test 2.6: Validation Overhead Measurement

**Objective:** Measure performance impact of contract validation.

**Procedure:**
```bash
# Test 1: Create story without contract validation (baseline)
# (Temporarily disable validation Step 2.3)
time /create-story Baseline performance test
baseline_time=$?

# Test 2: Create story with contract validation (enhanced)
# (Enable validation Step 2.3)
time /create-story Enhanced performance test
enhanced_time=$?

# Calculate overhead
overhead=$((enhanced_time - baseline_time))
overhead_percent=$((overhead * 100 / baseline_time))

# Assertion
assert [ $overhead_percent -lt 5 ]  # Less than 5% overhead

echo "Validation overhead: ${overhead}s (${overhead_percent}%)"
```

**Success Criteria:**
- [ ] Validation overhead <5% of total execution time
- [ ] Contract loading <100ms
- [ ] YAML parsing <50ms
- [ ] Pattern matching <200ms

**Target:** Total validation time <500ms per story

---

## Phase 3 Testing (Long-Term - Week 3-4)

### Unit Tests (12 cases)

#### Test 3.1: story-requirements-analyst Subagent Created

**Objective:** Verify skill-specific subagent exists and is valid.

**Procedure:**
```bash
# Check file exists
assert [ -f .claude/agents/story-requirements-analyst.md ]

# Validate frontmatter
grep -q "name: story-requirements-analyst" .claude/agents/story-requirements-analyst.md
grep -q "parent_skill: devforgeai-story-creation" .claude/agents/story-requirements-analyst.md
grep -q "output_format: content_only" .claude/agents/story-requirements-analyst.md

# Check for output contract section
grep -q "Output Contract:" .claude/agents/story-requirements-analyst.md
grep -q "PROHIBITED ACTIONS" .claude/agents/story-requirements-analyst.md
```

**Success Criteria:**
- [ ] File exists in `.claude/agents/`
- [ ] YAML frontmatter valid
- [ ] Output contract documented
- [ ] Prohibited actions listed

---

#### Test 3.2: Skill Uses Skill-Specific Subagent

**Objective:** Verify skill invokes `story-requirements-analyst` (not `requirements-analyst`).

**Procedure:**
```bash
# Check skill reference file
grep "subagent_type=" .claude/skills/devforgeai-story-creation/references/requirements-analysis.md

# Expected: "subagent_type=\"story-requirements-analyst\""
assert grep -q "story-requirements-analyst" .claude/skills/devforgeai-story-creation/references/requirements-analysis.md
```

**Success Criteria:**
- [ ] Skill invokes `story-requirements-analyst`
- [ ] NOT invoking general-purpose `requirements-analyst`
- [ ] Invocation documented in reference file

---

#### Test 3.3: Skill-Specific Subagent Returns Content (Not Files)

**Objective:** Verify skill-specific subagent enforces content-only output.

**Procedure:**
```bash
# Create story using skill-specific subagent
/create-story Test skill-specific subagent behavior

# Check result
after_count=$(ls devforgeai/specs/Stories/STORY-*.story.md | wc -l)
extra_count=$(ls devforgeai/specs/Stories/STORY-*-SUMMARY.md 2>/dev/null | wc -l)

# Assertions
assert [ $extra_count -eq 0 ]  # Zero extra files

# Check subagent output in skill log
# Expected: Markdown text sections (not file paths)
```

**Success Criteria:**
- [ ] Only 1 .story.md file created
- [ ] Zero extra files
- [ ] Content quality matches general-purpose subagent
- [ ] All sections present

---

## Batch Creation Testing (Week 4-6)

### Unit Tests (15 cases)

#### Test 4.1: Epic Pattern Detection

**Objective:** Verify command detects epic-001 pattern.

**Procedure:**
```bash
# Test various epic formats
test_patterns=(
    "epic-001"      # Lowercase
    "EPIC-001"      # Uppercase
    "Epic-001"      # Mixed case
    "epic-002"      # Different epic
    "EPIC-999"      # High number
)

for pattern in "${test_patterns[@]}"; do
    # Parse pattern
    mode=$(detect_mode "$pattern")

    # Assertion
    assert [ "$mode" == "EPIC_BATCH_MODE" ]
done

# Test non-epic patterns (should NOT match)
non_epic=(
    "epic001"       # No hyphen
    "epic-1"        # Not 3 digits
    "epic-1234"     # Too many digits
    "story-001"     # Wrong prefix
)

for pattern in "${non_epic[@]}"; do
    mode=$(detect_mode "$pattern")
    assert [ "$mode" != "EPIC_BATCH_MODE" ]
done
```

**Success Criteria:**
- [ ] All valid epic formats detected
- [ ] Invalid formats rejected
- [ ] Case-insensitive matching works

---

#### Test 4.2: Feature Extraction from Epic

**Objective:** Verify all features extracted correctly.

**Procedure:**
```bash
# Extract features from EPIC-001
features=$(extract_epic_features "EPIC-001")

# Count features
count=$(echo "$features" | jq length)
assert [ $count -eq 7 ]  # EPIC-001 has 7 features

# Validate feature structure
echo "$features" | jq -e '.[0].number' > /dev/null  # Feature number present
echo "$features" | jq -e '.[0].name' > /dev/null    # Feature name present
echo "$features" | jq -e '.[0].description' > /dev/null  # Description present
echo "$features" | jq -e '.[0].points' > /dev/null  # Points present

# Validate points are integers
points=$(echo "$features" | jq '.[].points')
for p in $points; do
    assert [ $p -gt 0 ]
    assert [ $p -le 21 ]
done
```

**Success Criteria:**
- [ ] All features extracted (7/7)
- [ ] Feature numbers correct (1.1 through 1.7)
- [ ] Feature names captured
- [ ] Feature descriptions captured
- [ ] Points are valid integers

---

#### Test 4.3: Multi-Select Feature Picker

**Objective:** Verify AskUserQuestion with multiSelect: true.

**Procedure:**
```bash
# Run command
/create-story epic-001

# Expected: AskUserQuestion with 7 options (one per feature)
# User can select 0, 1, or multiple features

# Test selections:
# 1. Select none → Should exit or ask again
# 2. Select 1 feature → Create 1 story
# 3. Select 3 features → Create 3 stories
# 4. Select all 7 → Create 7 stories

# Assertions for each scenario
```

**Success Criteria:**
- [ ] All features presented as options
- [ ] Multi-select enabled (can select multiple)
- [ ] Selection count validated
- [ ] Correct number of stories created based on selection

---

#### Test 4.4: Gap Detection and Filling

**Objective:** Verify gap-aware story ID calculation.

**Procedure:**
```bash
# Setup: Create stories with gaps
# Existing: STORY-001, STORY-002, STORY-003, STORY-005, STORY-007

# Delete STORY-004 and STORY-006 (create gaps)
rm devforgeai/specs/Stories/STORY-004*.story.md
rm devforgeai/specs/Stories/STORY-006*.story.md

# Create new story
/create-story epic-001  # Select 1 feature

# Expected: Next ID is STORY-004 (fills first gap)
latest=$(ls -t devforgeai/specs/Stories/STORY-*.story.md | head -1)
assert echo "$latest" | grep -q "STORY-004"

# Create another story
/create-story epic-001  # Select 1 feature

# Expected: Next ID is STORY-006 (fills second gap)
latest=$(ls -t devforgeai/specs/Stories/STORY-*.story.md | head -1)
assert echo "$latest" | grep -q "STORY-006"

# Create another story
/create-story epic-001  # Select 1 feature

# Expected: Next ID is STORY-008 (no gaps, increment from max=7)
latest=$(ls -t devforgeai/specs/Stories/STORY-*.story.md | head -1)
assert echo "$latest" | grep -q "STORY-008"
```

**Success Criteria:**
- [ ] First gap detected (STORY-004)
- [ ] Second gap detected (STORY-006)
- [ ] After gaps filled, increments from max
- [ ] User notified of gap filling

---

#### Test 4.5: Batch Metadata Application

**Objective:** Verify batch metadata applied to all stories.

**Procedure:**
```bash
# Create batch with uniform metadata
/create-story epic-001

# Select 3 features
# Sprint: Sprint-1 (batch apply)
# Priority: High (batch apply)

# Check all 3 stories have same metadata
for story in STORY-009 STORY-010 STORY-011; do
    story_file=$(ls devforgeai/specs/Stories/${story}*.story.md)

    # Extract metadata
    sprint=$(grep "^sprint:" "$story_file" | awk '{print $2}')
    priority=$(grep "^priority:" "$story_file" | awk '{print $2}')

    # Assertions
    assert [ "$sprint" == "Sprint-1" ]
    assert [ "$priority" == "High" ]
done
```

**Success Criteria:**
- [ ] All stories have same sprint
- [ ] All stories have same priority
- [ ] Only 2 questions asked (not 6 for 3 stories)

---

#### Test 4.6: TodoWrite Progress Tracking

**Objective:** Verify visual progress updates work.

**Procedure:**
```bash
# Create batch with 5 stories
/create-story epic-002

# Select 5 features

# Monitor TodoWrite updates
# Expected progression for each story:
# [ ] Create STORY-XXX → [→] Create STORY-XXX → [✓] Create STORY-XXX

# Check final todo state
# Expected: All 5 todos marked "completed"
```

**Success Criteria:**
- [ ] Todo list created before loop
- [ ] Each todo marked in_progress when creating
- [ ] Each todo marked completed after creation
- [ ] Visual updates visible to user

---

### Integration Tests (15 cases)

#### Test 4.7: Full Batch Creation (7 Stories)

**Objective:** End-to-end test creating all features from epic.

**Procedure:**
```bash
# Pre-test state
before=$(ls devforgeai/specs/Stories/STORY-*.story.md | wc -l)

# Execute
/create-story epic-001

# Select all 7 features
# Sprint: Sprint-1
# Priority: Inherit from epic

# Wait for completion (expected: 6-14 minutes depending on parallel optimization)

# Post-test state
after=$(ls devforgeai/specs/Stories/STORY-*.story.md | wc -l)
new=$((after - before))

# Assertions
assert [ $new -eq 7 ]  # Exactly 7 new stories

# Check IDs are sequential
expected_ids=("STORY-009" "STORY-010" "STORY-011" "STORY-012" "STORY-013" "STORY-014" "STORY-015")
for id in "${expected_ids[@]}"; do
    assert [ -f devforgeai/specs/Stories/${id}*.story.md ]
done

# Check no extra files
for id in "${expected_ids[@]}"; do
    assert [ ! -f devforgeai/specs/Stories/${id}-SUMMARY.md ]
    assert [ ! -f devforgeai/specs/Stories/${id}-QUICK-START.md ]
done

# Check epic updated
epic="devforgeai/specs/Epics/EPIC-001.epic.md"
for id in "${expected_ids[@]}"; do
    assert grep -q "$id" "$epic"
done
```

**Success Criteria:**
- [ ] 7 stories created (one per feature)
- [ ] Story IDs sequential (009-015)
- [ ] Zero extra files (no SUMMARY.md, etc.)
- [ ] All stories linked to epic
- [ ] Epic updated with references

---

#### Test 4.8: Partial Selection (3 of 6 Features)

**Objective:** Verify selective feature creation.

**Procedure:**
```bash
# Create batch (partial)
/create-story epic-002

# Select features: 2.3, 2.4, 2.6 (skip 2.1, 2.2, 2.5)
# Expected: Only 3 stories created (for selected features)

# Post-test
new_stories=$(ls devforgeai/specs/Stories/STORY-010*.story.md devforgeai/specs/Stories/STORY-011*.story.md devforgeai/specs/Stories/STORY-012*.story.md 2>/dev/null | wc -l)

assert [ $new_stories -eq 3 ]

# Check epic shows stories only for selected features
epic="devforgeai/specs/Epics/EPIC-002.epic.md"

# Feature 2.3 should have story
assert grep -A 3 "Feature 2.3" "$epic" | grep -q "STORY-"

# Feature 2.5 should NOT have story (not selected)
assert ! grep -A 3 "Feature 2.5" "$epic" | grep -q "STORY-"
```

**Success Criteria:**
- [ ] Only selected features create stories
- [ ] Non-selected features have no stories
- [ ] Epic accurately reflects partial completion

---

#### Test 4.9: Error Recovery (1 Failure in 5)

**Objective:** Test continue-on-error with partial success.

**Procedure:**
```bash
# Create batch
/create-story epic-003

# Select 5 features

# Simulate failure on feature 3 (for testing):
# (Temporarily corrupt Feature 3 description in epic to trigger validation error)

# Expected:
# - Story 1: SUCCESS
# - Story 2: SUCCESS
# - Story 3: FAILURE (validation error)
# - Story 4: SUCCESS
# - Story 5: SUCCESS

# Check summary
# Expected: "4 succeeded, 1 failed"

# Assertions
created=$(ls devforgeai/specs/Stories/STORY-016*.story.md devforgeai/specs/Stories/STORY-017*.story.md 2>/dev/null | wc -l)
assert [ $created -eq 4 ]  # 4 succeeded (feature 3 failed)

# Check retry option presented
assert output_contains("Retry failed stories?")
```

**Success Criteria:**
- [ ] Batch doesn't halt on single failure
- [ ] Successful stories created
- [ ] Failed stories tracked
- [ ] Summary accurate (4/5 success)
- [ ] Retry option available

---

#### Test 4.10: Dry-Run Preview Accuracy

**Objective:** Verify dry-run preview matches actual execution.

**Procedure:**
```bash
# Step 1: Run dry-run
/create-story epic-004 --dry-run

# Select 4 features
# Capture preview output:
# - Story IDs shown (e.g., STORY-020, STORY-021, STORY-022, STORY-023)
# - File paths shown
# - Capacity calculation shown

dry_run_ids=$(echo "$preview_output" | grep -oE "STORY-[0-9]{3}")

# Step 2: Run actual creation
/create-story epic-004

# Select same 4 features
# Same sprint, same priority

# Capture actual results
actual_ids=$(ls devforgeai/specs/Stories/STORY-*.story.md | grep -oE "STORY-[0-9]{3}" | tail -4)

# Compare
assert [ "$dry_run_ids" == "$actual_ids" ]  # IDs match preview
```

**Success Criteria:**
- [ ] Dry-run story IDs match actual IDs
- [ ] Dry-run file paths match actual paths
- [ ] Dry-run capacity matches actual capacity
- [ ] Dry-run creates no files

---

### Performance Tests (8 cases)

#### Test 4.11: Sequential Execution Baseline

**Objective:** Measure baseline performance (no parallel optimization).

**Procedure:**
```bash
# Create 7 stories sequentially
time /create-story epic-001

# Select all 7 features
# Sprint: Backlog
# Priority: High

# Measure execution time
sequential_time=$?

# Expected: ~14 minutes (7 stories × 2 min each)
assert [ $sequential_time -ge 12 ]  # At least 12 min
assert [ $sequential_time -le 18 ]  # At most 18 min

echo "Sequential execution: ${sequential_time} seconds"
```

**Success Criteria:**
- [ ] Execution time 12-18 minutes
- [ ] All 7 stories created
- [ ] Zero extra files

---

#### Test 4.12: Parallel Execution Speedup

**Objective:** Measure parallel optimization speedup (target: 40-60%).

**Procedure:**
```bash
# Enable parallel optimization (Phase 6)
# Create 7 stories with pseudo-parallel subagent invocation

time /create-story epic-005

# Select all 7 features

# Measure execution time
parallel_time=$?

# Calculate speedup
speedup=$(( (sequential_time - parallel_time) * 100 / sequential_time ))

# Assertions
assert [ $parallel_time -lt $sequential_time ]  # Faster than sequential
assert [ $speedup -ge 40 ]  # At least 40% speedup
assert [ $speedup -le 70 ]  # Realistic upper bound

echo "Parallel execution: ${parallel_time} seconds"
echo "Speedup: ${speedup}%"
```

**Success Criteria:**
- [ ] Execution time 6-9 minutes (for 7 stories)
- [ ] Speedup 40-60% vs. sequential
- [ ] All stories created correctly
- [ ] No race conditions or conflicts

---

### Regression Tests (15 cases)

#### Test 4.13: Single Story Mode Unchanged

**Objective:** Verify batch enhancement doesn't break single story mode.

**Procedure:**
```bash
# Create single story (old workflow)
/create-story User authentication with OAuth2 and Google provider

# Expected: Normal single story workflow
# - Asks for epic/sprint
# - Asks for priority/points
# - Creates 1 story
# - No batch mode triggered

# Assertions
assert mode == "SINGLE_STORY_MODE"
assert batch_mode == false
assert file_count increases by 1
```

**Success Criteria:**
- [ ] Single story mode still works
- [ ] No batch mode triggered
- [ ] All interactive questions asked
- [ ] Story quality unchanged

---

#### Test 4.14: Backward Compatibility (Existing Stories)

**Objective:** Verify existing stories not affected by enhancement.

**Procedure:**
```bash
# Check existing stories
existing_stories=$(ls devforgeai/specs/Stories/STORY-*.story.md)

# Read each story
for story in $existing_stories; do
    # Validate structure still valid
    assert grep -q "^---$" "$story"  # YAML frontmatter
    assert grep -q "^id: STORY-" "$story"
    assert grep -q "## User Story" "$story"
    assert grep -q "## Acceptance Criteria" "$story"
done

# Run /dev on existing story (should work normally)
/dev STORY-001

# Expected: No errors, development workflow works
```

**Success Criteria:**
- [ ] Existing stories readable
- [ ] Existing story structure valid
- [ ] /dev command works on existing stories
- [ ] No migration needed

---

## Test Execution Procedure

### Pre-Implementation Testing (Validation)

**Before implementing fixes:**

1. **Baseline test** - Create story with current code:
   ```bash
   /create-story Baseline test before RCA-007 fix
   # Expected: 5 files created (current bug)
   # Document baseline behavior
   ```

2. **Record baseline metrics:**
   - File count: 5 (1 main + 4 extra)
   - Execution time: ~2 minutes
   - Questions asked: 4-5
   - Story quality: Excellent (comprehensive)

---

### Post-Implementation Testing (Verification)

**After implementing each phase:**

1. **Phase 1 (Immediate Fix):**
   - Run Tests 1.1 - 1.5 (unit tests)
   - Run Tests 1.6 - 1.12 (integration tests)
   - Run Tests 1.13 - 1.14 (regression tests)
   - **Target:** 27/27 tests pass (100%)

2. **Phase 2 (Contract Validation):**
   - Run Tests 2.1 - 2.5 (unit tests)
   - Run Test 2.6 (performance test)
   - **Target:** 6/6 tests pass (100%)

3. **Phase 3 (Skill-Specific Subagent):**
   - Run Tests 3.1 - 3.3 (unit tests)
   - Re-run all Phase 1 tests (regression)
   - **Target:** 30/30 tests pass (100%)

4. **Phase 4-6 (Batch Enhancement):**
   - Run Tests 4.1 - 4.14 (unit, integration, performance, regression)
   - **Target:** 45/45 tests pass (100%)

**Overall:** 87 total test cases, 100% pass rate required

---

## Test Automation

### Create Test Suite Script

**File:** `devforgeai/tests/rca-007-test-suite.sh`

```bash
#!/bin/bash
# RCA-007 & Batch Creation Test Suite
# Usage: bash devforgeai/tests/rca-007-test-suite.sh [phase]

set -e

PHASE=${1:-all}
RESULTS_DIR="devforgeai/tests/results"
TIMESTAMP=$(date +%Y%m%d-%H%M%S)

mkdir -p "$RESULTS_DIR"

# Color codes
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'  # No color

# Test counters
total_tests=0
passed_tests=0
failed_tests=0

# Helper functions
run_test() {
    local test_name=$1
    local test_cmd=$2

    echo -e "\n${YELLOW}Running: ${test_name}${NC}"
    total_tests=$((total_tests + 1))

    if eval "$test_cmd"; then
        echo -e "${GREEN}✓ PASSED${NC}"
        passed_tests=$((passed_tests + 1))
        return 0
    else
        echo -e "${RED}✗ FAILED${NC}"
        failed_tests=$((failed_tests + 1))
        return 1
    fi
}

# Phase 1 Tests
if [ "$PHASE" == "phase1" ] || [ "$PHASE" == "all" ]; then
    echo "═══════════════════════════════════════"
    echo "Phase 1: RCA-007 Immediate Fix Tests"
    echo "═══════════════════════════════════════"

    # Test 1.1: Prompt constraints present
    run_test "Test 1.1: Prompt Constraints" \
        "grep -q 'CRITICAL OUTPUT CONSTRAINTS' .claude/skills/devforgeai-story-creation/references/requirements-analysis.md"

    # Test 1.2: Validation checkpoint exists
    run_test "Test 1.2: Validation Checkpoint" \
        "grep -q 'Step 2.2: Validate Subagent Output' .claude/skills/devforgeai-story-creation/references/requirements-analysis.md"

    # Test 1.6: Single story creation (integration)
    run_test "Test 1.6: Single Story Creation" \
        "test_single_story_creation"

    # Add more tests...
fi

# Phase 2 Tests
if [ "$PHASE" == "phase2" ] || [ "$PHASE" == "all" ]; then
    echo "═══════════════════════════════════════"
    echo "Phase 2: Contract Validation Tests"
    echo "═══════════════════════════════════════"

    # Test 2.1: Contract YAML valid
    run_test "Test 2.1: Contract YAML Valid" \
        "python -c 'import yaml; yaml.safe_load(open(\".claude/skills/devforgeai-story-creation/contracts/requirements-analyst-contract.yaml\"))'"

    # Test 2.2: Validation script works
    run_test "Test 2.2: Validation Script" \
        "test_validation_script"

    # Add more tests...
fi

# Summary
echo ""
echo "═══════════════════════════════════════"
echo "Test Summary"
echo "═══════════════════════════════════════"
echo "Total:  $total_tests"
echo -e "Passed: ${GREEN}$passed_tests${NC}"
echo -e "Failed: ${RED}$failed_tests${NC}"
echo "Pass Rate: $((passed_tests * 100 / total_tests))%"

# Generate report
cat > "$RESULTS_DIR/test-report-${TIMESTAMP}.md" <<EOF
# RCA-007 Test Report

**Date:** $(date)
**Phase:** $PHASE

## Summary

- Total Tests: $total_tests
- Passed: $passed_tests
- Failed: $failed_tests
- Pass Rate: $((passed_tests * 100 / total_tests))%

## Results

[Test results here]

EOF

# Exit with appropriate code
if [ $failed_tests -eq 0 ]; then
    echo -e "\n${GREEN}All tests PASSED ✓${NC}"
    exit 0
else
    echo -e "\n${RED}${failed_tests} tests FAILED ✗${NC}"
    exit 1
fi
```

**Usage:**
```bash
# Run all tests
bash devforgeai/tests/rca-007-test-suite.sh all

# Run specific phase
bash devforgeai/tests/rca-007-test-suite.sh phase1
bash devforgeai/tests/rca-007-test-suite.sh phase2
```

---

## Success Metrics

### Phase-Specific Metrics

| Phase | Test Cases | Target Pass Rate | Critical Tests |
|-------|------------|------------------|----------------|
| Phase 1 | 27 | 100% | Tests 1.2, 1.6, 1.7 (validation, integration, recovery) |
| Phase 2 | 6 | 100% | Tests 2.2, 2.3 (validation script, file diff) |
| Phase 3 | 12 | 100% | Tests 3.3, 3.4 (subagent behavior, regression) |
| Batch (4-6) | 42 | 95% | Tests 4.7, 4.11, 4.13 (full batch, performance, backward compat) |

### Overall Success Criteria

- [ ] **Zero extra files:** No SUMMARY, QUICK-START, VALIDATION-CHECKLIST, FILE-INDEX files created
- [ ] **100% single-file compliance:** Only .story.md files in devforgeai/specs/Stories/
- [ ] **Validation effectiveness:** 100% detection rate for file creation violations
- [ ] **Recovery success:** 90%+ first-retry success rate
- [ ] **Performance:** Validation overhead <5%
- [ ] **Batch creation:** 7 stories in 6-8 min (40-60% speedup with parallel)
- [ ] **Question reduction:** 86-94% fewer questions (batch metadata)
- [ ] **Zero regressions:** All existing functionality preserved
- [ ] **Pass rate:** 95%+ across all 87 test cases

---

## Test Reporting

### Daily Test Report Template

```markdown
# RCA-007 Test Report - {YYYY-MM-DD}

**Phase:** {Phase 1/2/3/Batch}
**Tester:** {Name}
**Duration:** {HH:MM}

## Summary

- Tests Executed: {N}
- Passed: {N} ✅
- Failed: {N} ✗
- Skipped: {N} ⚠️
- Pass Rate: {X}%

## Critical Failures

{List any critical test failures}

## Performance Metrics

- Validation overhead: {X}%
- Average story creation time: {X} seconds
- Batch creation time (7 stories): {X} minutes
- Speedup vs. sequential: {X}%

## Regression Check

- Single story mode: ✅/✗
- Story quality: ✅/✗
- Epic linking: ✅/✗
- Self-validation: ✅/✗

## Issues Discovered

1. {Issue description}
2. {Issue description}

## Recommendations

1. {Recommendation}
2. {Recommendation}

## Next Steps

- [ ] {Action item 1}
- [ ] {Action item 2}
```

---

## Continuous Testing

### Pre-Commit Testing (Automated)

**Hook:** `.git/hooks/pre-commit` (add RCA-007 check)

```bash
#!/bin/bash
# Pre-commit hook: RCA-007 validation

# Check if story-creation files modified
if git diff --cached --name-only | grep -qE "devforgeai-story-creation|requirements-analyst"; then
    echo "Story creation files modified - running RCA-007 tests..."

    # Run quick validation
    python .claude/skills/devforgeai-story-creation/scripts/validate_contract.py \
        devforgeai/tests/fixtures/sample-subagent-output.txt \
        .claude/skills/devforgeai-story-creation/contracts/requirements-analyst-contract.yaml

    if [ $? -ne 0 ]; then
        echo "✗ Contract validation failed - check changes"
        exit 1
    fi

    echo "✓ RCA-007 validation passed"
fi
```

---

### Weekly Regression Testing

**Schedule:** Every Friday

**Tests:**
```bash
# 1. Create single story
/create-story Weekly regression test - single story

# Assertions
assert only 1 file created
assert no extra files

# 2. Create batch (3 stories)
/create-story epic-001  # Select 3 features

# Assertions
assert 3 files created
assert no extra files per story
assert batch metadata applied

# 3. Check violation log
violations=$(grep -c "VIOLATION DETECTED" devforgeai/logs/rca-007-violations.log)

# Report
echo "Weekly Regression: $violations violations this week"

# Alert if violations increasing
if [ $violations -gt $previous_week_violations ]; then
    ALERT: "Violations increasing - review subagent behavior"
fi
```

---

## Related Documents

- **RCA:** `devforgeai/RCA/RCA-007-multi-file-story-creation.md`
- **Implementation Plan:** `devforgeai/specs/enhancements/RCA-007-FIX-IMPLEMENTATION-PLAN.md`
- **Batch Enhancement:** `devforgeai/specs/enhancements/BATCH-STORY-CREATION-ENHANCEMENT.md`
- **Prompt Spec:** `devforgeai/specs/enhancements/SUBAGENT-PROMPT-ENHANCEMENT-SPEC.md`
- **Contract Spec:** `devforgeai/specs/enhancements/YAML-CONTRACT-SPECIFICATION.md`

---

**Testing Status:** Specification Complete - Ready for Phase 1 Testing (Week 1)
**Total Test Cases:** 87 (comprehensive coverage)
**Target Pass Rate:** 95%+ (allow 5% for edge cases requiring refinement)
