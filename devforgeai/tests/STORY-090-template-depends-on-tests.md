# STORY-090: Test Suite - Story Template v2.2 depends_on Field

**Story ID:** STORY-090
**Test Suite Version:** 1.0
**Created:** 2025-12-14
**Status:** FAILING (Tests validate requirements NOT YET MET)

---

## Test Overview

**Total Tests:** 45 tests across 7 acceptance criteria
**Test Categories:**
- Unit Tests: 35 (file content validation, parsing, formatting)
- Integration Tests: 8 (end-to-end flows, sync verification)
- Edge Case Tests: 2 (error handling, boundary conditions)

**Coverage Targets:**
- AC#1: 6 tests
- AC#2: 4 tests
- AC#3: 6 tests
- AC#4: 12 tests (2 per story)
- AC#5: 8 tests
- AC#6: 3 tests
- AC#7: 6 tests

---

## AC#1 Tests: Story Template Updated with depends_on Field

### Test 1.1: Template contains depends_on field in frontmatter

**Objective:** Verify that story-template.md includes `depends_on:` field in YAML frontmatter

**Test Name:** `test_template_contains_depends_on_field_in_frontmatter`

**Setup:**
- Read template file: `src/claude/skills/devforgeai-story-creation/assets/templates/story-template.md`
- Extract YAML frontmatter (lines between first and second `---` markers)

**Test Steps:**
1. Parse YAML frontmatter
2. Search for key: `depends_on`
3. Verify field exists

**Expected Result:** PASS
- Field `depends_on:` found in frontmatter
- Value type is array (YAML list)
- Default value is empty array `[]`

**Current Status:** FAILING
- Template currently at format_version 2.1
- depends_on field not yet present in frontmatter

---

### Test 1.2: depends_on field positioned after points and before status

**Objective:** Verify field ordering in YAML frontmatter matches specification

**Test Name:** `test_depends_on_field_position_after_points_before_status`

**Setup:**
- Read template frontmatter
- Parse field names and their line positions

**Test Steps:**
1. Extract field order from frontmatter
2. Find position of: `points`, `depends_on`, `status`
3. Verify sequential ordering

**Expected Result:** PASS
- Field order: ... `points:` ... `depends_on:` ... `status:` ...
- No fields between points and depends_on (optional: priority field allowed)
- No fields between depends_on and status

**Current Status:** FAILING
- Field ordering will need to be adjusted when field is added

---

### Test 1.3: depends_on field has comment explaining usage

**Objective:** Verify field includes inline YAML comment explaining purpose

**Test Name:** `test_depends_on_field_has_usage_comment`

**Setup:**
- Read template frontmatter
- Extract comment text after depends_on field

**Test Steps:**
1. Find line containing `depends_on:`
2. Extract trailing comment (after `#` symbol)
3. Verify comment exists and is meaningful

**Expected Result:** PASS
- Comment contains reference to "STORY-ID" or "dependencies"
- Comment explains array format
- Example: `# Array of STORY-NNN IDs this story depends on`

**Current Status:** FAILING
- Field not yet present to have comment

---

### Test 1.4: Default empty array is valid YAML

**Objective:** Verify default value syntax is correct YAML array

**Test Name:** `test_depends_on_default_empty_array_is_valid_yaml`

**Setup:**
- Extract depends_on field with default value
- Parse as YAML

**Test Steps:**
1. Extract: `depends_on: []`
2. Parse as YAML array
3. Verify parsed value is empty list/array type

**Expected Result:** PASS
- YAML parser accepts syntax without error
- Parsed value: `[]` (empty array)
- Type: list/array (not string, not null)

**Current Status:** FAILING
- Field not present to test

---

### Test 1.5: Template contains proper example of depends_on with single dependency

**Objective:** Verify template includes usage example with one dependency

**Test Name:** `test_template_includes_example_single_dependency_format`

**Setup:**
- Read template content (beyond YAML frontmatter)
- Search for examples or explanatory text

**Test Steps:**
1. Search template for example showing single dependency
2. Find pattern: `depends_on: ["STORY-NNN"]`
3. Verify example is valid YAML

**Expected Result:** PASS
- Template includes example like: `depends_on: ["STORY-044"]`
- Example is valid YAML
- Example follows naming convention (STORY- prefix with 3-4 digits)

**Current Status:** FAILING
- Field not yet documented in template

---

### Test 1.6: Template contains proper example of depends_on with multiple dependencies

**Objective:** Verify template includes usage example with multiple dependencies

**Test Name:** `test_template_includes_example_multiple_dependencies_format`

**Setup:**
- Read template content
- Search for multi-dependency example

**Test Steps:**
1. Search for pattern: `depends_on: ["STORY-NNN", "STORY-MMM"]`
2. Verify all items follow naming convention
3. Verify valid YAML array syntax

**Expected Result:** PASS
- Template includes example like: `depends_on: ["STORY-044", "STORY-045", "STORY-046"]`
- All items are strings in STORY-NNN format
- Valid YAML array syntax with commas

**Current Status:** FAILING
- Field not yet documented in template

---

## AC#2 Tests: Format Version Incremented to 2.2

### Test 2.1: format_version field equals "2.2"

**Objective:** Verify version is updated to 2.2

**Test Name:** `test_template_format_version_equals_2_2`

**Setup:**
- Read template frontmatter
- Extract `format_version` value

**Test Steps:**
1. Find line: `format_version: "..."`
2. Extract string value
3. Compare to expected value

**Expected Result:** PASS
- `format_version: "2.2"` (exact match)
- Value is string (quoted)

**Current Status:** FAILING
- Current template has `format_version: "2.1"`

---

### Test 2.2: Version string follows semantic versioning format

**Objective:** Verify format matches MAJOR.MINOR pattern

**Test Name:** `test_format_version_matches_semantic_versioning`

**Setup:**
- Extract format_version value
- Validate against regex pattern

**Test Steps:**
1. Extract value: `"2.2"`
2. Test regex: `^\\d+\\.\\d+$`
3. Verify match (MAJOR.MINOR format)

**Expected Result:** PASS
- Regex matches: `2.2`
- No v prefix: `"v2.2"` would FAIL
- No patch version: `"2.2.0"` would FAIL
- Format: `"[0-9]+\\.[0-9]+"`

**Current Status:** FAILING
- Dependency on Test 2.1 passing

---

### Test 2.3: Version is NOT a pre-release or beta version

**Objective:** Verify production-ready version (no -alpha, -beta, -rc suffixes)

**Test Name:** `test_format_version_not_prerelease`

**Setup:**
- Extract format_version value
- Check for prerelease markers

**Test Steps:**
1. Extract: `"2.2"`
2. Search for: `-alpha`, `-beta`, `-rc`, `alpha`, `beta`
3. Verify NOT found

**Expected Result:** PASS
- `"2.2"` - no prerelease markers
- `"2.2-alpha"` would FAIL
- `"2.2-rc1"` would FAIL
- Production version confirmed

**Current Status:** FAILING
- Dependency on Test 2.1 passing

---

### Test 2.4: Changelog entry references v2.2 update

**Objective:** Verify changelog section at top of template mentions v2.2

**Test Name:** `test_changelog_section_contains_v2_2_entry`

**Setup:**
- Read template lines 1-60 (changelog section)
- Search for version entry

**Test Steps:**
1. Extract changelog section
2. Search for: `v2.2`
3. Verify section exists with proper formatting

**Expected Result:** PASS
- Line contains: `# v2.2` or `v2.2 (date)`
- Entry in changelog section (first ~60 lines)
- Changelog follows existing v2.1 and v2.0 format

**Current Status:** FAILING
- Changelog not yet updated

---

## AC#3 Tests: Template Changelog Documents v2.2 Changes

### Test 3.1: Changelog contains v2.2 entry header

**Objective:** Verify changelog section has v2.2 entry with proper header format

**Test Name:** `test_changelog_has_v2_2_entry_header`

**Setup:**
- Read changelog section (lines 1-60)
- Parse entry headers

**Test Steps:**
1. Search for: `v2.2`
2. Verify it's followed by date: `(YYYY-MM-DD)`
3. Verify format matches existing entries: `# v2.0 (YYYY-MM-DD)`

**Expected Result:** PASS
- Header format: `# v2.2 (2025-11-25)`
- Date format: YYYY-MM-DD
- Matches existing entry format

**Current Status:** FAILING
- Changelog not updated

---

### Test 3.2: Changelog v2.2 entry includes date 2025-11-25

**Objective:** Verify correct date for v2.2 entry

**Test Name:** `test_changelog_v2_2_entry_has_correct_date`

**Setup:**
- Extract v2.2 entry
- Parse date field

**Test Steps:**
1. Find v2.2 entry header
2. Extract date in parentheses
3. Compare to: `2025-11-25`

**Expected Result:** PASS
- Date: `2025-11-25`
- Format: YYYY-MM-DD
- Exact match (not earlier or later date)

**Current Status:** FAILING
- Changelog not yet updated

---

### Test 3.3: Changelog v2.2 entry includes description about depends_on

**Objective:** Verify change description mentions depends_on field

**Test Name:** `test_changelog_v2_2_includes_depends_on_description`

**Setup:**
- Extract v2.2 entry content
- Search description text

**Test Steps:**
1. Find v2.2 entry
2. Extract description section (below header)
3. Search for keywords: `depends_on`, `dependency`, `dependencies`, `EPIC-010`

**Expected Result:** PASS
- Description contains: "depends_on"
- Description explains purpose (enables EPIC-010, parallel development, etc.)
- Description is 10-200 characters long
- Format example: `"Added depends_on field for EPIC-010 parallel development support"`

**Current Status:** FAILING
- Changelog not yet updated

---

### Test 3.4: Changelog v2.2 entry includes backward compatibility note

**Objective:** Verify changelog mentions backward compatibility with v2.1

**Test Name:** `test_changelog_v2_2_includes_backward_compat_note`

**Setup:**
- Extract v2.2 entry
- Search for compatibility statement

**Test Steps:**
1. Find v2.2 changelog entry
2. Search for: `backward`, `compatible`, `compatible with`, `optional`
3. Verify mentions v2.1 stories remaining valid

**Expected Result:** PASS
- Contains text like: "Compatible with v2.1 stories"
- Notes that depends_on is optional for existing stories
- Example: `"Compatible with v2.1 stories (depends_on field optional for existing stories)"`
- Confirms no breaking changes

**Current Status:** FAILING
- Changelog not yet updated

---

### Test 3.5: Changelog entry format matches existing entries (v2.1 and v2.0)

**Objective:** Verify consistency with existing changelog style

**Test Name:** `test_changelog_v2_2_format_matches_existing_entries`

**Setup:**
- Extract v2.1 entry (lines ~11)
- Extract v2.2 entry (when added)
- Compare formats

**Test Steps:**
1. Verify v2.2 entry structure matches v2.1 structure
2. Check for sections: Changes, Impact, References
3. Verify indentation and formatting consistency

**Expected Result:** PASS
- v2.2 entry follows same sections as v2.1:
  - Header: `# v2.2 (2025-11-25)`
  - Indented content with consistent structure
  - Similar description and notes format

**Current Status:** FAILING
- Changelog not yet updated

---

### Test 3.6: Changelog mentions this is a non-breaking change

**Objective:** Verify changelog clarifies no breaking changes for existing users

**Test Name:** `test_changelog_clarifies_non_breaking_change`

**Setup:**
- Extract v2.2 entry
- Parse backward compatibility section

**Test Steps:**
1. Find compatibility note
2. Verify it states change is non-breaking
3. Confirm existing stories continue to work

**Expected Result:** PASS
- Explicitly states no breaking changes
- Notes that v2.1 stories (without depends_on) remain valid
- Example language: "Non-breaking", "Backward compatible", "Existing stories unaffected"

**Current Status:** FAILING
- Changelog not yet updated

---

## AC#4 Tests: Six Existing Stories Standardized to Array Format

### Test 4.1: STORY-044 has depends_on field in array format

**Objective:** Verify STORY-044 has properly formatted depends_on array

**Test Name:** `test_STORY_044_has_depends_on_array_format`

**Setup:**
- Read: `devforgeai/specs/Stories/STORY-044.story.md` (if exists)
- Extract YAML frontmatter

**Test Steps:**
1. Extract `depends_on:` line
2. Verify value is array format: `[]` or `["STORY-NNN"]`
3. Verify NOT string format: `"STORY-044"`
4. Verify NOT comma-separated: `STORY-044, STORY-045`

**Expected Result:** PASS
- Format: `depends_on: []` OR `depends_on: ["STORY-044"]`
- Valid YAML array
- No string quotes around array

**Current Status:** FAILING
- Story file may not exist, or field not in array format

---

### Test 4.2: STORY-045 has depends_on field in array format

**Objective:** Verify STORY-045 has properly formatted depends_on array

**Test Name:** `test_STORY_045_has_depends_on_array_format`

**Setup:**
- Read: `devforgeai/specs/Stories/STORY-045.story.md`
- Extract YAML frontmatter

**Test Steps:**
1. Extract `depends_on:` line
2. Verify array format
3. Parse YAML to confirm array type

**Expected Result:** PASS
- Format: `depends_on: []` or array with STORY-IDs
- YAML parser confirms array type
- No non-array formats

**Current Status:** FAILING
- Dependency on standardization process

---

### Test 4.3: STORY-046 has depends_on field in array format

**Objective:** Verify STORY-046 has properly formatted depends_on array

**Test Name:** `test_STORY_046_has_depends_on_array_format`

**Setup:**
- Read: `devforgeai/specs/Stories/STORY-046.story.md`
- Extract YAML frontmatter

**Test Steps:**
1. Extract `depends_on:` field
2. Verify array format
3. Validate YAML syntax

**Expected Result:** PASS
- Array format confirmed
- Empty array `[]` or array with STORY-ID strings

**Current Status:** FAILING
- Story standardization not completed

---

### Test 4.4: STORY-047 has depends_on field in array format

**Objective:** Verify STORY-047 has properly formatted depends_on array

**Test Name:** `test_STORY_047_has_depends_on_array_format`

**Setup:**
- Read: `devforgeai/specs/Stories/STORY-047.story.md`
- Extract YAML frontmatter

**Test Steps:**
1. Extract `depends_on:` field
2. Verify array format (YAML list)

**Expected Result:** PASS
- Array format: `[]` or `["STORY-NNN"]`
- Valid YAML

**Current Status:** FAILING
- Story standardization not completed

---

### Test 4.5: STORY-048 has depends_on field in array format

**Objective:** Verify STORY-048 has properly formatted depends_on array

**Test Name:** `test_STORY_048_has_depends_on_array_format`

**Setup:**
- Read: `devforgeai/specs/Stories/STORY-048.story.md`
- Extract YAML frontmatter

**Test Steps:**
1. Extract `depends_on:` field
2. Verify array format

**Expected Result:** PASS
- Array format confirmed
- Valid YAML

**Current Status:** FAILING
- Story standardization not completed

---

### Test 4.6: STORY-070 has depends_on field in array format

**Objective:** Verify STORY-070 has properly formatted depends_on array

**Test Name:** `test_STORY_070_has_depends_on_array_format`

**Setup:**
- Read: `devforgeai/specs/Stories/STORY-070.story.md`
- Extract YAML frontmatter

**Test Steps:**
1. Extract `depends_on:` field
2. Verify array format

**Expected Result:** PASS
- Array format: `[]` or `["STORY-NNN"]`
- Valid YAML

**Current Status:** FAILING
- Story standardization not completed

---

### Test 4.7: No story uses string format (STORY-044 through STORY-048, STORY-070)

**Objective:** Verify none of 6 stories have string format depends_on

**Test Name:** `test_no_story_uses_string_format_depends_on`

**Setup:**
- Read all 6 story files
- Extract depends_on lines

**Test Steps:**
1. For each story file (STORY-044 through STORY-048, STORY-070):
   a. Extract depends_on line
   b. Search for pattern: `depends_on: "STORY-`
   c. Verify pattern NOT found

**Expected Result:** PASS
- None of 6 stories use: `depends_on: "STORY-044"`
- All use array format: `depends_on: ["STORY-044"]`
- String format FAILS: `"STORY-NNN"` (without array brackets)

**Current Status:** FAILING
- Test requires all 6 stories to be processed

---

### Test 4.8: No story uses comma-separated format (STORY-044 through STORY-048, STORY-070)

**Objective:** Verify none of 6 stories use comma-separated format

**Test Name:** `test_no_story_uses_comma_separated_depends_on`

**Setup:**
- Read all 6 story files
- Extract depends_on lines

**Test Steps:**
1. For each story:
   a. Extract depends_on line
   b. Search for pattern: `STORY-044, STORY-045` (comma with space)
   c. Search for pattern: `STORY-044,STORY-045` (comma without space)
   d. Verify neither pattern found

**Expected Result:** PASS
- No story uses: `depends_on: STORY-044, STORY-045`
- No story uses: `depends_on: STORY-044,STORY-045`
- All use array brackets: `depends_on: ["STORY-044", "STORY-045"]`

**Current Status:** FAILING
- Standardization not completed

---

### Test 4.9: All 6 stories have valid STORY-ID format in depends_on arrays

**Objective:** Verify all dependency references match STORY-NNN format

**Test Name:** `test_all_story_depends_on_references_have_valid_format`

**Setup:**
- Read all 6 story files
- Extract all depends_on values

**Test Steps:**
1. For each story file:
   a. Extract depends_on array
   b. For each element in array:
      - Test regex: `^STORY-\\d{3,4}$`
      - Verify match (STORY- prefix with 3-4 digits)

**Expected Result:** PASS
- Valid: `["STORY-044"]`, `["STORY-045", "STORY-046"]`, `[]`
- Invalid: `["story-044"]` (lowercase), `["STORY-44"]` (2 digits), `["044"]` (no prefix)
- All references in all 6 stories match pattern

**Current Status:** FAILING
- Standardization not completed

---

### Test 4.10: STORY-044 body content unchanged after depends_on update

**Objective:** Verify only frontmatter changed, body content unchanged

**Test Name:** `test_STORY_044_body_content_unchanged`

**Setup:**
- Obtain STORY-044 before update (backup/reference)
- Obtain STORY-044 after update
- Extract body content (after frontmatter)

**Test Steps:**
1. Extract body content before update
2. Extract body content after update
3. Compare line-by-line
4. Verify no differences

**Expected Result:** PASS
- Body content identical before/after
- Only frontmatter `depends_on` line added/changed
- Story title, description, AC, DoD all unchanged

**Current Status:** FAILING
- Standardization not yet executed

---

### Test 4.11: Story frontmatter fields (except depends_on) unchanged after update

**Objective:** Verify other YAML fields not modified

**Test Name:** `test_STORY_044_other_frontmatter_unchanged`

**Setup:**
- Extract STORY-044 frontmatter before update
- Extract STORY-044 frontmatter after update
- Parse YAML

**Test Steps:**
1. Extract all frontmatter fields from before update
2. Extract all frontmatter fields from after update
3. Compare all fields except `depends_on`
4. Verify match: id, title, epic, sprint, status, points, priority, assigned_to, created, format_version

**Expected Result:** PASS
- All fields match except `depends_on` (which was added/changed)
- No other fields modified
- `format_version` remains at story's original version (v2.1)
- Story identity, status, points unchanged

**Current Status:** FAILING
- Standardization not yet executed

---

### Test 4.12: STORY-070 body content unchanged after depends_on update

**Objective:** Verify STORY-070 body content preserved during standardization

**Test Name:** `test_STORY_070_body_content_unchanged`

**Setup:**
- Obtain STORY-070 before and after update
- Compare body sections

**Test Steps:**
1. Extract body content (after frontmatter) before update
2. Extract body content (after frontmatter) after update
3. Compare for equality

**Expected Result:** PASS
- Body content identical
- No lines added, removed, or modified
- Only frontmatter changes made

**Current Status:** FAILING
- Standardization not yet executed

---

## AC#5 Tests: Story-Creation Skill Phase 1 Dependency Question

### Test 5.1: Phase 1 includes optional dependency question in AskUserQuestion

**Objective:** Verify /create-story skill asks about dependencies in Phase 1

**Test Name:** `test_create_story_phase_1_includes_dependency_question`

**Setup:**
- Read: `src/claude/skills/devforgeai-story-creation/references/story-discovery.md` or similar Phase 1 workflow file
- Search for dependency-related question

**Test Steps:**
1. Find Phase 1 (Information Gathering) section
2. Search for AskUserQuestion block
3. Verify question about dependencies exists
4. Verify question is marked as optional

**Expected Result:** PASS
- Question text includes: "depend" OR "dependency" OR "STORY-ID"
- Question is optional (user can skip)
- Example: `"Does this story depend on other stories? (Enter STORY-IDs or 'none')"`

**Current Status:** FAILING
- Skill enhancement not yet implemented

---

### Test 5.2: Dependency question accepts "none" input

**Objective:** Verify skill accepts "none" for no dependencies

**Test Name:** `test_create_story_normalizes_none_input_to_empty_array`

**Setup:**
- Simulate user input: "none"
- Extract normalization logic

**Test Steps:**
1. Input: `"none"`
2. Process through normalization logic
3. Verify output is empty array

**Expected Result:** PASS
- Input: `"none"` (case-insensitive: "NONE", "None" also acceptable)
- Output: `[]` (empty array)
- Generated story has: `depends_on: []`

**Current Status:** FAILING
- Input normalization not yet implemented

---

### Test 5.3: Dependency question accepts single STORY-ID input

**Objective:** Verify skill accepts single STORY-ID like "STORY-044"

**Test Name:** `test_create_story_normalizes_single_story_id`

**Setup:**
- Simulate user input: "STORY-044"
- Extract normalization logic

**Test Steps:**
1. Input: `"STORY-044"`
2. Process through normalization
3. Verify output is array with one element

**Expected Result:** PASS
- Input: `"STORY-044"` (any valid STORY-NNN format)
- Output: `["STORY-044"]` (array with one string)
- Generated story has: `depends_on: ["STORY-044"]`

**Current Status:** FAILING
- Input normalization not yet implemented

---

### Test 5.4: Dependency question accepts comma-separated STORY-IDs

**Objective:** Verify skill converts "STORY-044, STORY-045" to array

**Test Name:** `test_create_story_normalizes_comma_separated_story_ids`

**Setup:**
- Simulate user input: "STORY-044, STORY-045"
- Extract normalization logic

**Test Steps:**
1. Input: `"STORY-044, STORY-045"`
2. Process through normalization
3. Verify output is array with two elements
4. Verify whitespace trimmed

**Expected Result:** PASS
- Input: `"STORY-044, STORY-045"` (comma-separated with spaces)
- Input: `"STORY-044,STORY-045"` (comma without spaces, also works)
- Output: `["STORY-044", "STORY-045"]`
- Generated story has: `depends_on: ["STORY-044", "STORY-045"]`
- Whitespace trimmed from each element

**Current Status:** FAILING
- Input normalization not yet implemented

---

### Test 5.5: Dependency question validation rejects invalid STORY-ID format

**Objective:** Verify skill rejects malformed input like "story-044" (lowercase)

**Test Name:** `test_create_story_rejects_invalid_story_id_format`

**Setup:**
- Simulate user input: "story-044" (lowercase, invalid)
- Extract validation logic

**Test Steps:**
1. Input: `"story-044"` (lowercase)
2. Run validation
3. Verify validation fails
4. Verify error message returned

**Expected Result:** PASS
- Input: `"story-044"` → REJECTED (lowercase, regex fails)
- Input: `"STORY-44"` → REJECTED (2 digits instead of 3-4)
- Input: `"STORY-044"` → ACCEPTED (valid format)
- Error message returned for invalid input

**Current Status:** FAILING
- Validation logic not yet implemented

---

### Test 5.6: Dependency question is optional (user can skip)

**Objective:** Verify story creation doesn't fail if user skips dependency question

**Test Name:** `test_create_story_dependency_question_optional_skip`

**Setup:**
- Read Phase 1 workflow
- Check AskUserQuestion configuration

**Test Steps:**
1. Find dependency question definition
2. Verify question is marked optional (not required)
3. Simulate skipping (returning null/empty)
4. Verify story creation continues

**Expected Result:** PASS
- Question marked as optional in AskUserQuestion
- User can skip without blocking story creation
- If skipped, default: `depends_on: []`
- Story creation completes successfully

**Current Status:** FAILING
- Skill enhancement not yet implemented

---

### Test 5.7: Generated story frontmatter includes normalized depends_on field

**Objective:** Verify created story has correct depends_on in frontmatter

**Test Name:** `test_generated_story_has_depends_on_in_frontmatter`

**Setup:**
- Run /create-story command
- Answer dependency question with: "STORY-044, STORY-045"
- Obtain generated story file

**Test Steps:**
1. Read generated story file
2. Extract YAML frontmatter
3. Find `depends_on:` field
4. Verify value is normalized array

**Expected Result:** PASS
- Generated story has: `depends_on: ["STORY-044", "STORY-045"]`
- Field in correct position (after points, before status)
- Valid YAML array format

**Current Status:** FAILING
- Skill enhancement not yet implemented

---

### Test 5.8: Dependency question follows existing Phase 1 pattern

**Objective:** Verify question format matches existing Phase 1 AskUserQuestion calls

**Test Name:** `test_dependency_question_follows_phase_1_pattern`

**Setup:**
- Extract existing AskUserQuestion calls from Phase 1
- Extract new dependency question
- Compare formats

**Test Steps:**
1. Find existing Phase 1 questions (title, description, etc.)
2. Find dependency question
3. Verify format consistency:
   - Same question header format
   - Same input/output pattern
   - Same optional marker if applicable

**Expected Result:** PASS
- Question format matches existing Phase 1 style
- Consistent with other information gathering questions
- Proper YAML/Markdown structure for AskUserQuestion

**Current Status:** FAILING
- Question not yet implemented

---

## AC#6 Tests: Operational Directory Sync Complete

### Test 6.1: src/ template synced to .claude/ (files identical)

**Objective:** Verify source and operational templates have identical content

**Test Name:** `test_source_and_operational_templates_identical_content`

**Setup:**
- Read source template: `src/claude/skills/devforgeai-story-creation/assets/templates/story-template.md`
- Read operational template: `.claude/skills/devforgeai-story-creation/assets/templates/story-template.md`

**Test Steps:**
1. Read both files completely
2. Compare byte-for-byte (or line-by-line)
3. Verify no differences

**Expected Result:** PASS
- Both files have identical content
- Same lines, same order, same formatting
- File sizes match
- No differences in diff

**Current Status:** FAILING
- Sync not yet executed

---

### Test 6.2: Operational template includes depends_on field (matches source)

**Objective:** Verify operational .claude/ copy has v2.2 update

**Test Name:** `test_operational_template_has_depends_on_field`

**Setup:**
- Read: `.claude/skills/devforgeai-story-creation/assets/templates/story-template.md`
- Extract YAML frontmatter

**Test Steps:**
1. Extract `format_version`
2. Verify equals "2.2"
3. Extract `depends_on` field
4. Verify exists and is array

**Expected Result:** PASS
- `format_version: "2.2"`
- `depends_on: []` field exists
- Valid array format
- Changelog updated with v2.2 entry

**Current Status:** FAILING
- Sync not yet executed

---

### Test 6.3: diff shows no differences between src/ and .claude/ templates

**Objective:** Verify sync is complete with no outstanding differences

**Test Name:** `test_diff_src_and_operational_templates_returns_zero`

**Setup:**
- Run: `diff src/claude/skills/devforgeai-story-creation/assets/templates/story-template.md .claude/skills/devforgeai-story-creation/assets/templates/story-template.md`

**Test Steps:**
1. Execute diff command
2. Capture exit code
3. Verify exit code is 0 (no differences)
4. Capture output (should be empty)

**Expected Result:** PASS
- Exit code: 0 (no differences)
- Output: (empty)
- No modified lines reported
- Sync is complete

**Current Status:** FAILING
- Sync not yet executed

---

## AC#7 Tests: Existing Story Content Preservation

### Test 7.1: STORY-044 story body content unchanged

**Objective:** Verify story body (User Story, AC, DoD) unchanged after depends_on addition

**Test Name:** `test_STORY_044_story_body_content_preserved`

**Setup:**
- Read STORY-044 before update (reference version)
- Read STORY-044 after update
- Extract body content (everything after frontmatter)

**Test Steps:**
1. Find end of YAML frontmatter (line with `---`)
2. Extract all subsequent content
3. Compare before/after versions
4. Verify identical

**Expected Result:** PASS
- Story body section identical
- Description unchanged
- Acceptance Criteria unchanged
- Definition of Done unchanged
- All story content preserved except frontmatter

**Current Status:** FAILING
- Update process not yet executed

---

### Test 7.2: STORY-045 all frontmatter fields (except depends_on) unchanged

**Objective:** Verify other fields preserved when depends_on added

**Test Name:** `test_STORY_045_frontmatter_preserved_except_depends_on`

**Setup:**
- Read STORY-045 before update
- Read STORY-045 after update
- Extract YAML frontmatter from both

**Test Steps:**
1. Parse YAML frontmatter from before version
2. Parse YAML frontmatter from after version
3. Compare all fields except `depends_on`
4. Verify match for: id, title, epic, sprint, status, points, priority, created, format_version, assigned_to

**Expected Result:** PASS
- All fields match except `depends_on`
- id: unchanged
- title: unchanged
- epic: unchanged
- sprint: unchanged
- status: unchanged
- points: unchanged (no accidental updates)
- format_version: unchanged (story keeps its version)
- Only `depends_on` field added/changed

**Current Status:** FAILING
- Update process not yet executed

---

### Test 7.3: STORY-046 description section unchanged

**Objective:** Verify story description/user story unchanged

**Test Name:** `test_STORY_046_description_section_unchanged`

**Setup:**
- Read STORY-046 before update
- Read STORY-046 after update

**Test Steps:**
1. Extract "## Description" section from both versions
2. Extract all content from "## Description" to next "##" section
3. Compare line-by-line
4. Verify identical

**Expected Result:** PASS
- Description section identical
- User story ("As a... I want... So that...") unchanged
- Any description details unchanged
- No accidental modifications

**Current Status:** FAILING
- Update process not yet executed

---

### Test 7.4: STORY-047 acceptance criteria unchanged

**Objective:** Verify AC section unchanged after depends_on field update

**Test Name:** `test_STORY_047_acceptance_criteria_unchanged`

**Setup:**
- Read STORY-047 before update
- Read STORY-047 after update

**Test Steps:**
1. Extract "## Acceptance Criteria" section from both versions
2. Extract all AC#N subsections
3. Compare before/after
4. Verify identical

**Expected Result:** PASS
- All AC#1, AC#2, ... subsections unchanged
- AC titles unchanged
- AC Given/When/Then content unchanged
- No accidental edits to AC wording

**Current Status:** FAILING
- Update process not yet executed

---

### Test 7.5: STORY-048 definition of done checklist unchanged

**Objective:** Verify DoD section unchanged

**Test Name:** `test_STORY_048_definition_of_done_unchanged`

**Setup:**
- Read STORY-048 before update
- Read STORY-048 after update

**Test Steps:**
1. Extract "## Definition of Done" section
2. Extract all checklist items
3. Compare before/after versions
4. Verify identical

**Expected Result:** PASS
- DoD section identical
- All checklist items unchanged (no [ ] ↔ [x] changes)
- DoD content preserved
- No accidental completion status changes

**Current Status:** FAILING
- Update process not yet executed

---

### Test 7.6: STORY-070 entire content preserved except frontmatter depends_on field

**Objective:** Verify complete content preservation for STORY-070

**Test Name:** `test_STORY_070_complete_content_preserved`

**Setup:**
- Read STORY-070 before update
- Read STORY-070 after update
- Prepare diff report

**Test Steps:**
1. Compare entire files line-by-line
2. Identify only differences that are:
   a. Addition of `depends_on:` field in frontmatter, OR
   b. Modification of existing `depends_on:` field to array format
3. Verify no other differences

**Expected Result:** PASS
- Diff shows ONLY depends_on line changes
- All other content identical
- Story body completely preserved
- Frontmatter fields (except depends_on) unchanged

**Current Status:** FAILING
- Update process not yet executed

---

## Summary Statistics

**Total Tests:** 45
- AC#1 (Template Field): 6 tests
- AC#2 (Version): 4 tests
- AC#3 (Changelog): 6 tests
- AC#4 (Six Stories): 12 tests
- AC#5 (Skill Enhancement): 8 tests
- AC#6 (Directory Sync): 3 tests
- AC#7 (Content Preservation): 6 tests

**Test Status:** ALL FAILING (TDD Red Phase)
- Tests validate requirements not yet implemented
- Implementation will proceed in TDD Green phase
- Refactoring will occur in TDD Refactor phase

**Coverage Areas:**
- Template structure validation: 6 tests
- Version management: 4 tests
- Changelog documentation: 6 tests
- Story standardization: 12 tests (2 per story)
- Skill enhancement: 8 tests
- Sync verification: 3 tests
- Content preservation: 6 tests

**Test Dependencies:**
- AC#1 tests: Independent
- AC#2 tests: Depend on AC#1 (template must exist first)
- AC#3 tests: Depend on AC#2 (changelog needs to be added)
- AC#4 tests: Independent (can run in parallel)
- AC#5 tests: Depend on skill being enhanced
- AC#6 tests: Depend on all AC#1-AC#4 completion
- AC#7 tests: Depend on AC#4 (stories must be updated)

---

## Test Execution Instructions

**Phase:** TDD Red (Failing Tests)
**Framework:** Claude Code native tools (Read, Write, Edit, Grep, Bash)
**No external test frameworks needed** - validation uses native tools as specified in tech-stack.md

**To Run Tests:**
1. Read story file: `/mnt/c/Projects/DevForgeAI2/devforgeai/specs/Stories/STORY-090-story-template-v2.2-depends-on-field.story.md`
2. Execute each test using Read/Grep/Bash tools
3. Record results against this test suite
4. All tests should FAIL initially (no implementation yet)
5. Implementation will be guided by test failures
6. Tests will pass when implementation matches specifications

**Implementation Sequence:**
1. Update template frontmatter (AC#1, AC#2)
2. Add changelog entry (AC#3)
3. Standardize 6 stories (AC#4, AC#7)
4. Enhance story-creation skill (AC#5)
5. Sync directories (AC#6)
6. Verify all tests pass

---

**Test Suite Version:** 1.0
**Last Updated:** 2025-12-14
**Status:** READY FOR EXECUTION
