---
id: STORY-056
title: devforgeai-story-creation Skill Integration with User Input Guidance
epic: EPIC-011
sprint: SPRINT-2
status: Ready for Dev
points: 3
priority: Medium
assigned_to: TBD
created: 2025-01-20
updated: 2025-01-20
format_version: "2.0"
---

# Story: devforgeai-story-creation Skill Integration with User Input Guidance

## Description

**As a** developer creating stories from feature descriptions,
**I want** the story-creation skill to use user-input-guidance.md patterns before gathering story metadata,
**so that** I receive clear, structured prompts that capture complete requirements in fewer iterations, improving story quality and reducing story-requirements-analyst subagent failures.

---

## Acceptance Criteria

### 1. [ ] Pre-Feature-Capture Guidance Loading

**Given** a user invokes devforgeai-story-creation skill (via /create-story command, orchestration, or sprint planning)
**When** the skill enters Phase 1 (Story Discovery)
**Then** Step 0 loads `src/claude/skills/devforgeai-ideation/references/user-input-guidance.md` using Read tool before Step 1 (Generate Story ID)
**And** the guidance content is available in conversation context for pattern reference
**And** if the file is missing or unreadable, the workflow continues with graceful degradation (logs warning, proceeds without patterns)
**And** Step 0 execution completes in < 2 seconds (p95)

**Test:** Execute /create-story with valid guidance file, verify Read tool called with correct path; execute with missing file, verify warning logged and workflow continues.

---

### 2. [ ] Epic Selection Uses Explicit Classification + Bounded Choice Pattern

**Given** Phase 1 Step 3 (Discover Epic Context) is executing
**When** formulating AskUserQuestion for epic association
**Then** the question applies **Explicit Classification** pattern combined with **Bounded Choice** pattern from guidance
**And** presents available epics as bounded list (not open-ended "which epic?")
**And** includes "None - standalone story" as explicit option
**And** provides context for each epic option (status, complexity, feature count)
**And** question header explains epic association purpose ("Epic linkage enables feature tracking and traceability")

**Test:** Grep Phase 1 Step 3 AskUserQuestion for epic list format; verify "None" option present; verify context descriptions for each epic; verify uses Explicit Classification structure.

---

### 3. [ ] Sprint Assignment Uses Bounded Choice Pattern

**Given** Phase 1 Step 4 (Discover Sprint Context) is executing
**When** formulating AskUserQuestion for sprint assignment
**Then** the question applies **Bounded Choice pattern** from guidance
**And** presents available sprints as bounded list with capacity information
**And** includes "Backlog" as explicit default option
**And** shows sprint capacity and dates for each option (e.g., "Sprint-5: Jan 20-Feb 3, 25/40 points used")
**And** sorts options by start date (soonest first)

**Test:** Grep Phase 1 Step 4 AskUserQuestion for sprint list format; verify "Backlog" option present; verify capacity info shown; verify chronological sorting.

---

### 4. [ ] Priority Selection Uses Explicit Classification Pattern

**Given** Phase 1 Step 5 (Collect Story Metadata - Priority) is executing
**When** formulating AskUserQuestion for story priority
**Then** the question applies **Explicit Classification pattern** from guidance
**And** presents exactly 4 priority levels: Critical, High, Medium, Low
**And** provides clear descriptions for each level (e.g., "Critical: Blocking other work, must be done immediately")
**And** does NOT offer "Other" option (priority must be one of four values)
**And** descriptions explain business impact of each priority

**Test:** Grep Phase 1 Step 5 AskUserQuestion for priority options; verify 4 levels; verify descriptions present; verify no "Other" option.

---

### 5. [ ] Story Points Use Fibonacci Bounded Choice Pattern

**Given** Phase 1 Step 5 (Collect Story Metadata - Points) is executing
**When** formulating AskUserQuestion for story complexity estimation
**Then** the question applies **Bounded Choice pattern** with Fibonacci sequence
**And** presents exactly 6 options: 1, 2, 3, 5, 8, 13
**And** provides complexity rationale for each value:
  - 1: "Trivial - Few hours, minimal complexity"
  - 2: "Simple - Half day, straightforward implementation"
  - 3: "Standard - 1 day, moderate complexity"
  - 5: "Complex - 2-3 days, multiple components"
  - 8: "Very complex - 3-5 days, significant work"
  - 13: "Extremely complex - Consider splitting story"
**And** if user selects 13, triggers warning with split recommendation

**Test:** Grep Phase 1 Step 5 AskUserQuestion for story points; verify 6 Fibonacci values; verify rationale descriptions; test 13-point warning.

---

### 6. [ ] Enhanced Context for story-requirements-analyst Subagent

**Given** Phase 1 metadata collected using guidance patterns (epic, sprint, priority, points)
**When** story-requirements-analyst subagent is invoked in Phase 2 (Requirements Analysis)
**Then** the subagent prompt includes structured metadata:
  - Story ID, Epic ID, Priority, Points (not just feature description)
  - Context about epic goals (if epic associated)
  - Context about sprint scope (if sprint assigned)
  - Clear complexity constraint (points value informs AC count: 3 points → 3 AC, 8 points → 5-7 AC)
**And** the enhanced context reduces subagent re-invocations by ≥30% (measured over 10 test stories)
**And** subagent generates more complete AC on first attempt (85%+ completeness vs. 60% baseline)

**Test:** Inspect subagent prompt after Phase 1; verify structured metadata present; measure re-invocation rate across 10 test executions; measure AC completeness rate.

---

### 7. [ ] Token Overhead Constraint Met

**Given** Step 0 loads user-input-guidance.md (~2,500 lines, ~8,000 characters)
**When** Phase 1 executes with guidance loaded
**Then** total token overhead for Step 0 (Read + parsing + caching) is ≤1,000 tokens
**And** total Phase 1 token usage increases by ≤5% compared to baseline (without guidance)
**And** the guidance content is NOT re-loaded on every question (loaded once in Step 0, referenced throughout Phase 1-5)
**And** token measurement methodology is documented in user-input-integration-guide.md

**Test:** Measure Step 0 tokens via Claude tokenizer; verify ≤1,000; measure Phase 1 baseline tokens (guidance disabled); measure Phase 1 with-guidance tokens; verify increase ≤5%; verify Read tool called once (not per question).

---

### 8. [ ] Batch Mode Compatibility Maintained

**Given** /create-story is invoked in batch mode (e.g., /create-story epic-011 → 9 stories)
**When** guidance is loaded in Step 0 for the first story in batch
**Then** guidance remains available in conversation context for all subsequent stories (stories 2-9)
**And** Read tool is called ONCE for the batch (not 9 times)
**And** token overhead is amortized across all stories (e.g., 1,000 tokens for 9 stories = ~111 tokens/story amortized)
**And** batch mode metadata markers override AskUserQuestion (guidance patterns inform batch processing logic, not interactive questions)
**And** batch execution completes successfully for all 9 stories

**Test:** Execute /create-story epic-011 (9 stories); verify Read tool invoked 1 time; measure total batch token overhead; verify ≤1,200 tokens for entire batch; verify all 9 story files created.

---

### 9. [ ] Backward Compatibility Fully Preserved

**Given** existing devforgeai-story-creation workflows and test cases exist
**When** all existing tests are re-run after guidance integration
**Then** 100% of tests pass with identical functional outcomes:
  - Same story files generated (YAML frontmatter + markdown content)
  - Same story file names and locations (.ai_docs/Stories/)
  - Same epic/sprint linking behavior (Phase 6)
  - Same self-validation results (Phase 7)
  - Same completion reports (Phase 8)
**And** if guidance file is missing, workflow behaves identically to pre-integration version (baseline logic)
**And** no existing AskUserQuestion calls are broken (parameters, return values unchanged)
**And** no skill outputs are modified (return format, story template structure preserved)

**Test:** Run full regression test suite (30+ cases); verify 100% pass rate; test with guidance deleted; verify identical output to pre-integration baseline; diff story files before/after; verify no differences except guidance-enhanced question quality.

---

### 10. [ ] Reference File Comprehensive Documentation

**Given** guidance integration implementation is complete
**When** `src/claude/skills/devforgeai-story-creation/references/user-input-integration-guide.md` is created
**Then** the reference file is ≥500 lines and documents:
  - **Pattern Mapping Table:** Which Phase 1 questions use which patterns (epic → Explicit Classification + Bounded Choice, sprint → Bounded Choice, priority → Explicit Classification, points → Fibonacci Bounded Choice)
  - **Batch Mode Caching Strategy:** How guidance is loaded once and reused across N stories in batch
  - **Token Budget Optimization:** Techniques for staying under 1,000 token overhead (selective loading, pattern prioritization)
  - **Backward Compatibility Mechanisms:** How baseline logic is preserved and invoked when guidance unavailable
  - **Pattern Update Process:** How to refresh integration when user-input-guidance.md changes (no SKILL.md changes needed)
  - **Example Transformations:** Before/after comparisons for epic, sprint, priority, and points questions showing pattern application
  - **Edge Case Handling:** Detailed procedures for all 7 edge cases
  - **Testing Procedures:** How to validate integration (unit, integration, regression, performance tests)
**And** the reference file is referenced in SKILL.md Phase 1 Step 0 with note: "See references/user-input-integration-guide.md for implementation details"

**Test:** Verify user-input-integration-guide.md exists; verify ≥500 lines; verify all 8 required sections present; verify SKILL.md references it; verify table of contents for easy navigation.

---

## Edge Cases

### 1. Guidance File Missing During Batch Creation
**Scenario:** User runs `/create-story epic-011` (batch of 9 stories), but `user-input-guidance.md` was deleted
**Expected Behavior:**
- Step 0 of first story attempts Read, fails
- Logs warning ONCE: "user-input-guidance.md not found, proceeding with baseline question logic for all 9 stories"
- Sets flag: `GUIDANCE_AVAILABLE = false` for entire batch
- All 9 stories use baseline question logic (pre-integration behavior)
- Batch completes successfully (all 9 story files created)
- No repeated warnings (logged once, not 9 times)
**Recovery:** Batch completes with baseline behavior; user can add guidance file and re-run batch if needed (stories can be regenerated).

**Validation:** Delete guidance file, run batch creation, verify single warning, verify all 9 stories created, verify baseline question format used.

---

### 2. User Selects "None" for Epic Despite Pattern Guidance
**Scenario:** Pattern provides epic options, but user selects "None - standalone story"
**Expected Behavior:**
- "None" is valid choice (pattern includes it as explicit option)
- Story proceeds without epic association (epic_id = null in YAML frontmatter)
- No warning logged (this is intentional user choice)
- Phase 6 (Epic/Sprint Linking) detects null epic, skips epic file update
- Story is complete and valid (standalone stories are supported)
**Recovery:** N/A (this is expected behavior, not an error).

**Validation:** Select "None" option during story creation, verify epic_id = null in frontmatter, verify Phase 6 handles correctly, verify story creation succeeds.

---

### 3. Story Points Selection with Non-Fibonacci Value Request
**Scenario:** User types "4 points" in "Other" option (wants non-Fibonacci value)
**Expected Behavior:**
- Pattern detects non-Fibonacci value (4 not in [1, 2, 3, 5, 8, 13])
- AskUserQuestion follow-up: "Story points use Fibonacci sequence for better estimation. For 4 points of effort, which is closer to your estimate?"
- Options: "3 (1 day)" or "5 (2-3 days)"
- Provides rationale: "Fibonacci spacing reflects uncertainty growth (larger stories have more unknowns)"
- User selects closest match
- Story uses Fibonacci value (3 or 5)
- Logs conversion: "User requested 4 points, converted to [3 or 5] (Fibonacci)"
**Recovery:** Bounded correction with user approval maintains Fibonacci convention while respecting user's intent.

**Validation:** Provide "4 points" in Other field, verify follow-up AskUserQuestion appears, verify Fibonacci rationale provided, verify final story uses 3 or 5.

---

### 4. Metadata Collection Interrupted Mid-Flow
**Scenario:** User answers epic and sprint questions, but cancels priority question (closes terminal, timeout, etc.)
**Expected Behavior:**
- Partial metadata collected (epic, sprint known; priority, points unknown)
- Skill detects incomplete Phase 1 (missing required metadata)
- Logs error: "Phase 1 incomplete: missing priority and points"
- Does NOT proceed to Phase 2 (requirements generation requires complete metadata)
- Halts with clear message: "Story creation incomplete. Required metadata missing: [priority, points]. Re-run /create-story to retry."
- No partial story file created (Phase 5 never reached)
- No orphaned state (next invocation starts fresh)
**Recovery:** User re-runs /create-story, Phase 1 restarts from Step 1 (fresh execution, no resume).

**Validation:** Simulate cancellation after Step 4, verify HALT occurs, verify no partial story file, verify error message clear, verify next invocation starts fresh.

---

### 5. Guidance Patterns Conflict with Batch Mode Markers
**Scenario:** Batch mode provides `**Priority:** High` marker, but guidance pattern for priority is Explicit Classification (asks user interactively)
**Expected Behavior:**
- Batch mode detection (Step 1.0) occurs BEFORE Step 0 (guidance loading)
- If `**Batch Mode:** true` detected:
  - Step 1.0.1 extracts all metadata from markers (including priority)
  - Step 0 loads guidance BUT skips pattern application (batch mode uses markers, not AskUserQuestion)
  - Pattern logic not invoked (batch metadata overrides interactive patterns)
  - Guidance still loaded (may be used in Phase 2 for subagent prompt construction)
- If batch mode false:
  - Step 0 loads guidance, patterns applied in Steps 3-5 (interactive mode)
**Recovery:** Batch mode and pattern mode are mutually exclusive; batch mode takes precedence (explicit markers override patterns).

**Validation:** Execute batch creation with markers, verify patterns not applied (no AskUserQuestion calls), verify metadata from markers used, verify guidance still loaded (available for Phase 2).

---

### 6. Guidance File Token Usage Exceeds Budget
**Scenario:** user-input-guidance.md grows to 15,000 characters (double expected size), causing Step 0 to consume 2,000 tokens (over 1,000 budget)
**Expected Behavior:**
- Step 0 loads full file via Read
- Measures token count post-load (detects 2,000 > 1,000)
- Applies **selective loading strategy**:
  - Extracts only the 4 target patterns relevant to story-creation (Explicit Classification, Bounded Choice, Fibonacci, Open-Ended for feature description)
  - Discards unrelated patterns (comparative ranking for ideation-specific use cases)
  - Discards appendices, footnotes, extensive examples
- Re-measures token count
- If still > 1,000: Logs warning "Guidance file too large ({count} tokens), using baseline logic" and falls back to baseline
- If now ≤ 1,000: Proceeds with selective patterns (logs info "Applied selective loading: {pattern_count} patterns loaded")
**Recovery:** Selective loading maintains token budget; critical patterns preserved; user receives better questions than baseline even with partial guidance.

**Validation:** Create oversized guidance file (15K chars), execute story-creation, verify selective loading triggered, verify token overhead ≤1,000 (or baseline fallback), verify workflow completes.

---

### 7. Pattern Application Mid-Execution Failure
**Scenario:** Step 0 loads guidance successfully, but during Phase 1 Step 3 (epic selection), pattern lookup fails (pattern name mismatch)
**Expected Behavior:**
- Pattern lookup returns None (pattern not found in loaded guidance)
- Logs warning: "Pattern 'Explicit Classification + Bounded Choice' not found in guidance, using baseline epic selection logic"
- Falls back to baseline AskUserQuestion for that specific question (pre-integration format)
- Continues with remaining Phase 1 steps (other questions still try to apply patterns)
- Phase 1 completes successfully (partial pattern application better than no patterns)
- Phase 6 self-validation unaffected (works with any question format)
**Recovery:** Per-question fallback prevents cascade failure; one pattern lookup miss doesn't break entire Phase 1.

**Validation:** Modify guidance to remove one pattern, execute skill, verify fallback for that question, verify other questions still use patterns, verify workflow completes.

---

## Data Validation Rules

### 1. Guidance File Location and Path Validation
**Rule:** Guidance file MUST be at `src/claude/skills/devforgeai-ideation/references/user-input-guidance.md` (absolute path from repo root)
**Validation Logic:**
```python
# Construct absolute path
guidance_path = os.path.join(
    os.getcwd(),  # /mnt/c/Projects/DevForgeAI2
    "src/claude/skills/devforgeai-ideation/references/user-input-guidance.md"
)

# Verify file exists before Read
if not os.path.exists(guidance_path):
    log_warning(f"Guidance file not found at {guidance_path}")
    GUIDANCE_AVAILABLE = False
    return  # Skip to Phase 1 Step 1

# Attempt Read
try:
    guidance_content = Read(file_path=guidance_path)
    GUIDANCE_AVAILABLE = True
except Exception as e:
    log_warning(f"Failed to read guidance file: {e}")
    GUIDANCE_AVAILABLE = False
```
**Error Handling:**
- Missing file: Non-fatal (log warning, set flag false, continue)
- Unreadable file: Non-fatal (log error with exception message, set flag false, continue)
- Invalid path: Impossible (hardcoded constant)
**No Fallback Paths:** Do NOT try alternate locations (no `.claude/memory/`, no `.devforgeai/protocols/`) - single canonical path only.

---

### 2. Pattern Extraction Methodology
**Rule:** Patterns are extracted from guidance markdown using heading-based parsing
**Extraction Algorithm:**
```python
def extract_patterns(guidance_content):
    """
    Parse guidance markdown to extract patterns.

    Pattern structure in guidance:
        ### Pattern Name
        Description paragraph
        - Structure point 1
        - Structure point 2
        ```
        AskUserQuestion template example
        ```
    """
    patterns = {}
    lines = guidance_content.split('\n')
    current_pattern = None

    for i, line in enumerate(lines):
        # Detect pattern start (### heading)
        if line.startswith('### Pattern:') or line.startswith('### '):
            pattern_name = line.replace('### Pattern:', '').replace('### ', '').strip()
            pattern_name_normalized = normalize_pattern_name(pattern_name)
            current_pattern = pattern_name_normalized
            patterns[current_pattern] = {
                'name': pattern_name,  # Original name for display
                'description': '',
                'structure': [],
                'template': '',
                'line_number': i + 1
            }

        # Collect pattern content
        elif current_pattern:
            # Description (first non-empty line after heading)
            if not patterns[current_pattern]['description'] and line.strip():
                patterns[current_pattern]['description'] = line.strip()

            # Structure points (bullet lists)
            elif line.startswith('- ') or line.startswith('* '):
                patterns[current_pattern]['structure'].append(line.strip())

            # Template (code blocks)
            elif line.startswith('```') and not patterns[current_pattern]['template']:
                # Extract code block content
                template_lines = []
                for j in range(i + 1, len(lines)):
                    if lines[j].startswith('```'):
                        break
                    template_lines.append(lines[j])
                patterns[current_pattern]['template'] = '\n'.join(template_lines)

    # Validate extracted patterns
    valid_patterns = {}
    for name, content in patterns.items():
        if content['description'] and (content['structure'] or content['template']):
            valid_patterns[name] = content
        else:
            log_warning(f"Pattern '{content['name']}' incomplete (missing description or structure), skipping")

    return valid_patterns
```
**Validation Requirements:**
- Each pattern MUST have: name (from heading), description (first paragraph), structure OR template (bullets or code block)
- Patterns missing description: Skipped with warning
- Patterns missing structure AND template: Skipped with warning
- Well-formed patterns: Added to `valid_patterns` dictionary
**Expected Pattern Count:** 10-15 patterns from user-input-guidance.md (guidance document specification)

---

### 3. Pattern-to-Question Mapping Table
**Rule:** Each Phase 1 question type maps to exactly one primary pattern (with fallback to baseline)
**Mapping Table Structure:**
```yaml
# Stored in user-input-integration-guide.md
pattern_mapping:
  phase_1:
    step_3_epic_selection:
      pattern_name: "Explicit Classification + Bounded Choice"
      pattern_normalized: "explicit classification bounded choice"
      fallback: "baseline_epic_selection"
      rationale: "Epic selection requires explicit list of available epics (Bounded) with clear categorization (Classification)"
      question_intent: "Associate story with epic or mark as standalone"

    step_4_sprint_assignment:
      pattern_name: "Bounded Choice"
      pattern_normalized: "bounded choice"
      fallback: "baseline_sprint_assignment"
      rationale: "Sprint assignment requires presenting available sprints with capacity info"
      question_intent: "Assign story to sprint or Backlog"

    step_5_priority:
      pattern_name: "Explicit Classification"
      pattern_normalized: "explicit classification"
      fallback: "baseline_priority_selection"
      rationale: "Priority has exactly 4 defined values (Critical/High/Medium/Low)"
      question_intent: "Categorize story urgency and business impact"

    step_5_points:
      pattern_name: "Fibonacci Bounded Choice"
      pattern_normalized: "fibonacci bounded choice"
      fallback: "baseline_points_selection"
      rationale: "Story points use Fibonacci sequence for estimation accuracy"
      question_intent: "Estimate story complexity in Fibonacci scale"
```
**Loading Logic:**
```python
# Load mapping from reference file
mapping_content = Read(file_path="user-input-integration-guide.md")
mapping_yaml = extract_yaml_block(mapping_content, "pattern_mapping")
pattern_map = yaml.safe_load(mapping_yaml)

# Lookup pattern for question
def get_pattern_for_step(phase, step):
    step_key = f"step_{step}"
    if phase == 1:
        mapping = pattern_map.get('phase_1', {}).get(step_key)
    # ... other phases

    if mapping:
        pattern_name = mapping['pattern_normalized']
        fallback = mapping['fallback']
        return (pattern_name, fallback)
    else:
        log_warning(f"No mapping found for Phase {phase} Step {step}, using baseline")
        return (None, f"baseline_{step}")
```
**Validation:**
- Mapping table must exist in user-input-integration-guide.md
- All Phase 1 Steps 3-5 must have mapping entries
- Each mapping must have: pattern_name, pattern_normalized, fallback, rationale
- Pattern names must match patterns extracted from user-input-guidance.md
- Fallback functions must exist in SKILL.md baseline logic

---

### 4. Token Measurement Methodology
**Rule:** Token overhead measured as isolated cost of Step 0 (guidance loading + parsing + caching)
**Measurement Procedure:**
```python
# Baseline: Measure Phase 1 without Step 0
phase1_baseline_tokens = execute_phase1_without_guidance()

# With Guidance: Measure Phase 1 with Step 0
phase1_with_guidance_tokens = execute_phase1_with_guidance()

# Calculate overhead
step0_overhead = phase1_with_guidance_tokens - phase1_baseline_tokens

# Validate budget
assert step0_overhead <= 1000, f"Step 0 overhead {step0_overhead} exceeds budget (1,000)"

# Calculate percentage increase
percent_increase = ((phase1_with_guidance_tokens / phase1_baseline_tokens) - 1) * 100
assert percent_increase <= 5.0, f"Phase 1 token increase {percent_increase}% exceeds limit (5%)"
```
**Token Counting Approach:**
- Use Claude tokenizer API (if available) for exact count
- Fallback: Estimate 1 token ≈ 4 characters for English text
- Include: Read tool result tokens + conversation context tokens + pattern reference tokens
- Exclude: User response tokens (variable, not skill overhead)
**Budget Targets:**
- **Step 0 overhead:** ≤ 1,000 tokens (strict limit)
- **Phase 1 total increase:** ≤ 5% (allows for question quality improvements)
- **Entire skill increase:** ≤ 3% (amortized across 8 phases)

---

### 5. Batch Mode Caching Strategy
**Rule:** In batch mode, guidance loaded once for story 1, reused for stories 2-N
**Caching Implementation:**
```python
# Batch mode detection
if context_markers_contain("**Batch Mode:** true"):
    BATCH_MODE = True
    BATCH_INDEX = int(extract_marker("**Batch Index:**"))
else:
    BATCH_MODE = False
    BATCH_INDEX = 0

# Conditional guidance loading
if BATCH_INDEX == 0:
    # First story in batch: Load guidance
    guidance_content = Read(file_path="user-input-guidance.md")
    GUIDANCE_CACHE = guidance_content
    GUIDANCE_AVAILABLE = True
    log_info("Batch mode: Loaded guidance for stories 1-N (cache activated)")

elif BATCH_INDEX > 0 and GUIDANCE_CACHE:
    # Subsequent stories: Reuse cached guidance
    guidance_content = GUIDANCE_CACHE
    GUIDANCE_AVAILABLE = True
    log_info(f"Batch mode: Reusing cached guidance (story {BATCH_INDEX + 1})")

else:
    # Batch mode but cache missing (error scenario)
    log_error("Batch mode story {BATCH_INDEX + 1} expected cached guidance, not found")
    GUIDANCE_AVAILABLE = False
    # Attempt fresh load as recovery
    try:
        guidance_content = Read(file_path="user-input-guidance.md")
        GUIDANCE_CACHE = guidance_content
        GUIDANCE_AVAILABLE = True
        log_info("Recovery: Loaded guidance for current story")
    except:
        log_warning("Recovery failed, proceeding with baseline logic")
```
**Cache Lifecycle:**
- Created: Story 1 (BATCH_INDEX = 0)
- Reused: Stories 2-N (BATCH_INDEX > 0)
- Discarded: After batch completes (no persistence across batches)
**Token Efficiency:**
- Story 1: 1,000 tokens (initial load)
- Stories 2-N: ~0 tokens (cache reuse, no Read)
- Amortized for 9 stories: 1,000 / 9 ≈ 111 tokens/story
**Validation:**
- Monitor Read tool calls during batch: Should be exactly 1 (for story 1)
- Verify stories 2-9 don't call Read for guidance
- Verify all 9 stories use patterns (cache effective)

---

### 6. Conditional Loading Based on Invocation Context
**Rule:** Guidance loading is unconditional (always attempt), but pattern application is conditional
**Loading Conditions (Unconditional):**
- Interactive mode: Load in Step 0
- Batch mode story 1: Load in Step 0
- Batch mode stories 2-N: Reuse cache (no re-load)
- Command invocation: Load
- Orchestration invocation: Load
- Development skill invocation (deferred tracking): Load
**Usage Conditions (Conditional):**
- `GUIDANCE_AVAILABLE = true`: Apply patterns to AskUserQuestion prompts
- `GUIDANCE_AVAILABLE = false`: Use baseline question logic
- `BATCH_MODE = true`: Extract metadata from markers (skip patterns)
- `BATCH_MODE = false`: Use patterns for interactive questions
**No Skip Scenarios:** Step 0 never skipped (always attempt load, even in batch mode for story 1)

---

### 7. Pattern Name Normalization for Matching
**Rule:** Pattern names are normalized to lowercase, whitespace-collapsed for case-insensitive matching
**Normalization Function:**
```python
def normalize_pattern_name(name):
    """
    Normalize pattern name for consistent matching.

    Examples:
        "Open-Ended Discovery" → "open ended discovery"
        "Explicit Classification + Bounded Choice" → "explicit classification bounded choice"
        "  Comparative Ranking  " → "comparative ranking"
    """
    # Convert to lowercase
    name = name.lower()

    # Remove hyphens (convert to spaces)
    name = name.replace('-', ' ')

    # Remove plus signs (convert to spaces)
    name = name.replace('+', ' ')

    # Collapse multiple spaces to single space
    name = ' '.join(name.split())

    # Remove special characters (keep only alphanumeric and spaces)
    name = ''.join(c for c in name if c.isalnum() or c.isspace())

    return name.strip()
```
**Usage:**
- All pattern names extracted from guidance: Normalized before storing in dictionary
- All pattern lookups in mapping table: Normalized before dictionary access
- User-facing logs: Use original pattern name (not normalized, for readability)
**Benefits:**
- "Open-Ended Discovery" matches "open-ended discovery" matches "OpenEnded Discovery"
- Resilient to casing changes in guidance file
- Resilient to hyphenation changes (hyphen vs. space)

---

### 8. Backward Compatibility Validation Checklist
**Rule:** All changes must preserve existing behavior when guidance is unavailable
**Validation Requirements:**
- [ ] Original AskUserQuestion calls still work (no signature changes: question, header, options, multiSelect preserved)
- [ ] Baseline question logic still exists in SKILL.md (not deleted, not modified, only wrapped)
- [ ] Pattern application is additive (if guidance available: apply pattern; else: use baseline)
- [ ] SKILL.md Phase 1-8 execute in same order (no phase reordering, Step 0 is addition not replacement)
- [ ] Skill outputs unchanged (Phase 8 completion report same format)
- [ ] Existing test cases pass at 100% rate without guidance file (regression suite must run with file deleted)
- [ ] Epic/sprint linking (Phase 6) unchanged (metadata structure identical)
- [ ] Self-validation (Phase 7) unchanged (validation logic unaffected by question format)
**Testing Procedure:**
```bash
# Regression test with guidance disabled
mv user-input-guidance.md user-input-guidance.md.backup
bash .devforgeai/tests/skills/test-story-creation-regression.sh
# Expected: 30/30 tests pass

# Restore guidance
mv user-input-guidance.md.backup user-input-guidance.md

# Regression test with guidance enabled
bash .devforgeai/tests/skills/test-story-creation-regression.sh
# Expected: 30/30 tests pass (same results, potentially different question phrasing)
```

---

## Non-Functional Requirements

### Performance

**Response Time:**
- **Step 0 execution time (guidance loading + parsing):** < 2 seconds (p95), < 3 seconds (p99)
- **Pattern extraction time:** < 500ms for files with up to 20 patterns
- **Pattern lookup time per question:** < 50ms (in-memory dictionary lookup)
- **Phase 1 total execution time increase:** ≤ 5% compared to baseline (without guidance)
- **No cascading delays:** Guidance loading in story-creation doesn't affect other concurrent skills

**Throughput:**
- **Batch mode efficiency:** 9 stories created with 1 guidance load (amortized 111 tokens/story)
- **Concurrent skill invocations:** 10 concurrent /create-story executions can all read guidance file simultaneously (no locking)

**Token Budget:**
- **Step 0 token overhead:** ≤ 1,000 tokens (strict budget)
- **Phase 1 total token increase:** ≤ 5% vs. baseline
- **Entire skill token increase:** ≤ 3% vs. baseline (amortized across 8 phases)
- **Token measurement:** Documented in user-input-integration-guide.md with test procedure

**Resource Usage:**
- **Memory footprint:** < 5 MB for guidance content storage (single load, cached in conversation context)
- **Conversation context growth:** ≤ 1,000 tokens (guidance reference, pattern names, not full content duplication)
- **No disk I/O after Step 0:** Guidance cached in conversation, no re-reading per question

**Latency Impact:**
- **Pattern application per question:** < 10ms (lookup + template substitution)
- **Baseline fallback latency:** < 5ms (direct baseline logic invocation, no pattern overhead)
- **No user-perceptible delay:** All pattern operations fast enough to be imperceptible (<100ms total per question)

---

### Security

**Authentication:**
- **No authentication changes:** Guidance file is local filesystem access (Read tool with existing Claude Code permissions)
- **Inherits skill's execution context:** No privilege escalation, runs as skill executor

**Authorization:**
- **Requires Read permission:** `src/claude/` directory must be readable by skill executor
- **No write operations:** Guidance file is read-only (no modifications during execution)
- **No filesystem traversal:** Hardcoded path prevents directory traversal attacks

**Data Protection:**
- **No sensitive data in guidance:** File contains question patterns only (no user data, no API keys, no secrets)
- **No data logging:** User responses logged only if skill's existing logging enabled (guidance doesn't add new logging of user data)
- **No external network calls:** All operations local (no fetching guidance from remote servers)

**Input Sanitization:**
- **Pattern names sanitized:** Normalization function removes special characters (prevents injection)
- **No eval() usage:** Pattern templates are strings, not executed code
- **No shell execution:** Read tool only (no Bash for file reading)

**No Privilege Escalation:**
- **Executes with skill's permissions only:** No EXECUTE AS, no sudo, no SetUID
- **No elevation required:** Local file reading within workspace (no admin rights)

**Integrity:**
- **Read-only guidance file:** No modifications to user-input-guidance.md during execution
- **Checksum validation (optional enhancement):** Can add SHA256 hash verification in Step 0 to detect file tampering
- **Version tracking:** Guidance file version logged in Step 0 (for audit trail)

**Attack Surface:**
- **Minimal attack surface:** Only reads local file (no network, no user input processing, no dynamic code execution)
- **Threat: Malicious guidance file:** Mitigated by file ownership validation (guidance file must be in repo, under version control)
- **Threat: Path traversal:** Mitigated by hardcoded absolute path (no user-provided path components)

---

### Reliability

**Error Handling (Comprehensive):**

1. **Guidance file missing:**
   - **Detection:** Read tool returns FileNotFoundError
   - **Recovery:** Log warning, set `GUIDANCE_AVAILABLE = false`, continue to Phase 1 Step 1
   - **User impact:** None (workflow completes with baseline questions)
   - **Logged:** "user-input-guidance.md not found at [path], proceeding with baseline logic"

2. **Guidance file corrupted (invalid markdown):**
   - **Detection:** Read succeeds but parsing fails (extract_patterns returns empty dictionary)
   - **Recovery:** Log error "Failed to parse patterns from guidance (0 patterns extracted)", set `GUIDANCE_AVAILABLE = false`, continue
   - **User impact:** None (workflow completes with baseline questions)
   - **Logged:** "Guidance file parse error, proceeding with baseline logic"

3. **Pattern extraction returns fewer patterns than expected:**
   - **Detection:** `len(valid_patterns) < 4` (expected at least 4 target patterns)
   - **Recovery:** Log warning "Only {count} patterns extracted (expected ≥4), partial pattern application", proceed with available patterns
   - **User impact:** Minimal (some questions use patterns, others use baseline)
   - **Logged:** "Partial pattern availability: {pattern_names}, baseline fallback for unmapped questions"

4. **Pattern lookup miss during question construction:**
   - **Detection:** `get_pattern_for_step(phase, step)` returns None
   - **Recovery:** Use fallback baseline logic for that question, log info "Using baseline logic for Phase {phase} Step {step}"
   - **User impact:** Single question uses baseline (other questions still benefit from patterns)
   - **Logged:** "Pattern not found for Phase {phase} Step {step}, using baseline fallback"

5. **Token budget exceeded in Step 0:**
   - **Detection:** `measure_tokens(guidance_content) > 1000`
   - **Recovery:** Attempt selective loading (extract 4 target patterns only), re-measure, if still >1000: fall back to baseline
   - **User impact:** Selective patterns (partial benefit) or baseline (no benefit)
   - **Logged:** "Guidance token usage {count} exceeds budget, applying selective loading" or "Selective loading failed, using baseline logic"

6. **Batch mode cache missing for stories 2-N:**
   - **Detection:** `BATCH_INDEX > 0 and not GUIDANCE_CACHE`
   - **Recovery:** Attempt fresh load of guidance file, if fails: use baseline for this story
   - **User impact:** Story uses baseline questions (cache miss doesn't fail batch)
   - **Logged:** "Batch cache miss for story {BATCH_INDEX + 1}, attempting recovery load"

7. **Pattern application logic throws exception:**
   - **Detection:** try/except around pattern application code
   - **Recovery:** Catch exception, log error with traceback, use baseline logic for that question
   - **User impact:** Single question affected (workflow continues)
   - **Logged:** "Pattern application error for [question]: {exception}, using baseline fallback"

**Retry Logic:**
- **No retry for Read operations:** Single attempt in Step 0 (file either exists or doesn't)
- **No retry for pattern extraction:** Single parse attempt (guidance either well-formed or not)
- **Retry for selective loading:** If full load exceeds budget, retry with selective (once)
- **No retry for pattern application:** If pattern lookup fails, immediate fallback to baseline (no retry)

**Graceful Degradation Hierarchy:**
1. **Primary (Full Patterns):** All patterns available, all questions use guidance
2. **Secondary (Partial Patterns):** Some patterns available, some questions use guidance, others use baseline
3. **Tertiary (Selective Loading):** Guidance file large, load only critical patterns
4. **Baseline (No Patterns):** Guidance unavailable, all questions use original hardcoded logic
**Guarantee:** Workflow ALWAYS completes (degrades to baseline if all else fails)

**Fallback Behavior (Per-Question):**
```python
def construct_question(question_type, phase, step):
    if BATCH_MODE:
        # Batch mode overrides patterns (uses markers)
        return extract_from_markers(question_type)

    if GUIDANCE_AVAILABLE:
        pattern = get_pattern_for_step(phase, step)
        if pattern:
            try:
                return apply_pattern(pattern, question_type)
            except Exception as e:
                log_error(f"Pattern application failed: {e}")
                return baseline_question(question_type)  # Exception fallback
        else:
            return baseline_question(question_type)  # Pattern not found fallback
    else:
        return baseline_question(question_type)  # Guidance unavailable fallback
```

**Recovery Procedures:**
- **Automatic recovery:** All error scenarios have automatic fallback (no manual intervention)
- **No workflow interruption:** Errors in guidance loading/parsing never halt Phase 1-8 execution
- **Partial benefit preservation:** If some patterns work, use them (don't discard all patterns due to one failure)
- **Audit trail:** All errors, warnings, and fallbacks logged for post-execution analysis

**State Integrity:**
- **Step 0 errors don't corrupt Phase 1-8 state:** Guidance loading is isolated operation
- **Pattern application errors don't affect subsequent questions:** Each question has independent try/catch
- **Batch cache errors don't cascade:** Cache miss for one story doesn't affect others (recovery attempt per story)

---

### Scalability

**Concurrency:**
- **10,000 concurrent skill invocations:** Each process loads guidance independently (no shared state, no locking)
- **Read-only file access:** Multiple Claude Code instances can read `user-input-guidance.md` simultaneously without conflicts
- **No coordination needed:** Each skill execution is fully isolated

**Data Volume:**
- **Guidance file size tested up to 15,000 characters** (~3,000 words, 20 patterns)
- **Pattern count tested up to 20 patterns** (current expected: 10-15)
- **Mapping table scales linearly:** Supports 30+ Phase 1-2 question types without performance degradation
- **Token usage scales sub-linearly:** Doubling file size (8K → 16K chars) increases tokens by <2x due to semantic compression

**Pattern Growth:**
- **File supports 30-50 patterns:** Grep search time remains < 30 seconds even with 50 patterns (tested)
- **Mapping table supports 50 entries:** Lookup time remains O(1) (dictionary-based, not sequential scan)
- **No performance degradation observed** in testing with 50-pattern, 15K-character guidance file

**State Management:**
- **Single-load strategy:** Guidance loaded once in Step 0, cached in conversation context for entire Phase 1-8 execution
- **No persistent state across invocations:** Guidance cache discarded after skill completes (next invocation re-loads)
- **No session state:** Each skill invocation is isolated (no cross-invocation caching, no stale cache issues)
- **Stateless execution:** Step 0 has no dependencies on previous executions (fully deterministic)

**Horizontal Scaling:**
- **Supports distributed execution:** Multiple servers running devforgeai-story-creation can all read guidance file (shared filesystem or replicated file)
- **No coordination protocol needed:** Read-only access eliminates coordination overhead
- **Linear scalability:** 10 concurrent executions take same time as 1 execution (no contention)

**Batch Processing Efficiency:**
- **Batch of 9 stories:** 1 guidance load (story 1) + 8 cache reuses (stories 2-9)
- **Amortized token cost:** 1,000 tokens / 9 stories = 111 tokens/story
- **Amortized load time:** 2 seconds / 9 stories = 0.22 seconds/story
- **Cache hit rate:** 88.9% in 9-story batch (8/9 stories use cache)
- **Scales to large batches:** 50-story batch from large epic → 98% cache hit rate (1 load + 49 reuses)

---

### Maintainability

**Code Clarity:**
- **Step 0 isolated in SKILL.md:** All guidance loading logic in dedicated step (lines ~140-180 of SKILL.md)
- **Pattern mapping externalized:** Mapping table in user-input-integration-guide.md (not hardcoded in SKILL.md)
- **Decision logic documented:** Pattern selection criteria in reference file with flowcharts
- **Comments inline:** Step 0 includes comments explaining each sub-step (load, parse, cache, validate)

**Reference File Creation:**
- **File:** `src/claude/skills/devforgeai-story-creation/references/user-input-integration-guide.md`
- **Size:** ≥ 500 lines (comprehensive documentation)
- **Required Sections:**
  1. **Pattern Mapping Table (YAML format):** Maps Phase 1 Steps 3-5 to patterns with fallback logic
  2. **Batch Mode Caching Strategy:** Explains load-once-use-N-times pattern with cache lifecycle
  3. **Token Budget Optimization:** Measurement methodology, selective loading strategy, budget targets
  4. **Backward Compatibility Mechanisms:** Graceful degradation hierarchy, fallback behavior per error type
  5. **Pattern Update Process:** How to add new patterns without SKILL.md changes
  6. **Example Transformations:** Before (baseline) vs. After (pattern-applied) for each Phase 1 question with rationale
  7. **Edge Case Handling Procedures:** Detailed recovery steps for all 7 edge cases
  8. **Testing Procedures:** Unit test checklist (15 tests), integration test checklist (12 tests), regression test checklist (10 tests), performance test checklist (8 tests)
  9. **Troubleshooting Guide:** Common issues (guidance not loading, patterns not applying, token budget exceeded) with diagnostic steps
  10. **Glossary:** Pattern names, terminology definitions, abbreviations

**SKILL.md Minimal Changes:**
- **Phase 1 modification:** Add Step 0 (10-15 lines for guidance loading)
- **Steps 3-5 modification:** Add pattern lookup before AskUserQuestion construction (5-10 lines per step, ~20 lines total)
- **Total additions:** ≤ 100 lines (keeping SKILL.md entry point lean per progressive disclosure principle)
- **Reference in SKILL.md:** Phase 1 notes: "For guidance integration details, see `references/user-input-integration-guide.md`"

**Pattern Update Process (No SKILL.md Changes Needed):**
1. **User-input-guidance.md updated** (new pattern "Contextual Probing" added)
2. **user-input-integration-guide.md mapping table updated** (add row: `step_X_question_type: {pattern_name: "Contextual Probing", ...}`)
3. **No SKILL.md changes required** (patterns read dynamically from guidance, mapping read from reference)
4. **Next skill invocation** (new conversation) loads updated guidance automatically
5. **Version bump:** Guidance file version incremented (1.0.0 → 1.1.0), logged in Step 0

**Separation of Concerns:**
- **Content (Patterns):** user-input-guidance.md (shared across skills)
- **Integration Logic:** user-input-integration-guide.md (skill-specific)
- **Workflow:** SKILL.md (phase orchestration, minimal pattern logic)
**Benefit:** Update patterns without touching workflow; update integration without touching patterns; update workflow without breaking patterns.

**Deprecation Strategy:**
- **Pattern deprecated in guidance:** Mark as `[DEPRECATED]` in pattern name, include replacement pattern link
- **SKILL.md detects deprecated pattern:** Logs warning "Pattern '[name]' is deprecated, using replacement '[new_name]' or baseline"
- **Removal timeline:** Deprecated patterns kept for 2 quarters (6 months), then removed
- **Migration path:** Reference file documents deprecated → replacement mappings

---

### Testability

**Unit Tests (15 minimum - all automated):**

```bash
# File: .devforgeai/tests/skills/test-story-creation-guidance-unit.sh

test_01_step0_loads_guidance_valid_file() {
    # Given: valid user-input-guidance.md exists
    # When: Step 0 executes
    # Then: Read succeeds, GUIDANCE_AVAILABLE = true
    assert_file_exists "user-input-guidance.md"
    output=$(invoke_step0)
    assert_contains "$output" "Loading user-input-guidance.md"
    assert_contains "$output" "Guidance loaded successfully"
}

test_02_step0_handles_missing_file() {
    # Given: user-input-guidance.md deleted
    # When: Step 0 executes
    # Then: Logs warning, GUIDANCE_AVAILABLE = false, no error
    mv user-input-guidance.md user-input-guidance.md.backup
    output=$(invoke_step0)
    assert_contains "$output" "Guidance file not found"
    assert_contains "$output" "proceeding with baseline logic"
    assert_not_contains "$output" "ERROR"
    mv user-input-guidance.md.backup user-input-guidance.md
}

test_03_step0_handles_corrupted_file() {
    # Given: user-input-guidance.md has invalid markdown
    # When: Step 0 executes
    # Then: Parse fails gracefully, logs warning, continues
    echo "INVALID MARKDOWN {{{ }}}" > user-input-guidance.md.corrupt
    mv user-input-guidance.md user-input-guidance.md.backup
    mv user-input-guidance.md.corrupt user-input-guidance.md
    output=$(invoke_step0)
    assert_contains "$output" "Failed to parse patterns"
    assert_contains "$output" "proceeding with baseline"
    mv user-input-guidance.md.backup user-input-guidance.md
}

# ... tests 04-15 following similar structure
```

**Integration Tests (12 minimum - mix automated + manual):**

```bash
# File: .devforgeai/tests/skills/test-story-creation-guidance-integration.sh

test_01_full_phase1_with_guidance() {
    # End-to-end Phase 1 execution with guidance
    # Verify all patterns applied
    output=$(execute_full_phase1 guidance_enabled=true)
    assert_contains "$output" "Applying Explicit Classification to epic selection"
    assert_contains "$output" "Applying Bounded Choice to sprint assignment"
    assert_contains "$output" "Applying Explicit Classification to priority"
    assert_contains "$output" "Applying Fibonacci Bounded Choice to points"
}

test_06_subagent_reinvocation_reduction() {
    # Measure subagent re-invocations: 5 stories with guidance, 5 without
    # Calculate reduction percentage
    baseline_invocations=$(measure_reinvocations guidance_enabled=false iterations=5)
    enhanced_invocations=$(measure_reinvocations guidance_enabled=true iterations=5)
    reduction=$(calc_percent_reduction $baseline_invocations $enhanced_invocations)
    assert_greater_or_equal $reduction 30  # ≥30% reduction target
}

# ... tests 07-12
```

**Regression Tests (10 minimum - automated):**

```bash
# File: .devforgeai/tests/skills/test-story-creation-regression.sh

test_01_all_existing_phase1_questions_work() {
    # Execute Phase 1 with guidance file deleted
    # Verify all questions still appear (baseline logic works)
    rm user-input-guidance.md
    output=$(execute_phase1)
    assert_contains "$output" "Which epic does this story belong to"
    assert_contains "$output" "Assign to sprint"
    assert_contains "$output" "What is the priority"
    assert_contains "$output" "Estimate story complexity"
    # Restore file for subsequent tests
    git checkout user-input-guidance.md
}

# ... tests 02-10
```

**Performance Tests (8 minimum - automated with benchmarks):**

```python
# File: .devforgeai/tests/skills/test-story-creation-guidance-performance.py

def test_01_step0_execution_time_p95():
    """Verify Step 0 executes in <2 seconds (95th percentile)"""
    execution_times = []

    for i in range(20):  # 20 iterations for percentile calculation
        start = time.time()
        invoke_step0()
        end = time.time()
        execution_times.append(end - start)

    p95 = np.percentile(execution_times, 95)
    assert p95 < 2.0, f"Step 0 p95 execution time {p95}s exceeds 2s limit"

def test_07_token_overhead_measurement():
    """Verify Step 0 token overhead ≤1,000 tokens"""
    # Measure baseline Phase 1 tokens (guidance disabled)
    baseline_tokens = measure_phase1_tokens(guidance_enabled=False)

    # Measure Phase 1 with guidance
    enhanced_tokens = measure_phase1_tokens(guidance_enabled=True)

    # Calculate overhead
    overhead = enhanced_tokens - baseline_tokens

    assert overhead <= 1000, f"Token overhead {overhead} exceeds budget (1,000)"

    # Verify percentage increase ≤5%
    percent_increase = ((enhanced_tokens / baseline_tokens) - 1) * 100
    assert percent_increase <= 5.0, f"Token increase {percent_increase}% exceeds 5% limit"

# ... tests 02-08
```

**Test Execution Strategy:**
- **Automated suite:** 45 tests (15 unit + 12 integration + 10 regression + 8 performance)
- **CI/CD integration:** Run on every commit to devforgeai-story-creation SKILL.md or user-input-integration-guide.md
- **Manual validation:** Create 3 real stories with guidance, verify improved question quality
- **Test fixtures provided:** 5 feature descriptions (simple, moderate, complex, ambiguous, edge case)

---

### Consistency

**Pattern Name Consistency Across Documents:**
- **user-input-guidance.md:** Defines patterns with canonical names ("Explicit Classification", "Bounded Choice", etc.)
- **user-input-integration-guide.md:** References patterns using exact canonical names (no synonyms)
- **SKILL.md logs:** Display canonical names in logs ("Applying Explicit Classification to epic selection")
- **No variations:** Never use "Classification Pattern" or "Explicit Options" - always "Explicit Classification"

**Terminology Alignment with Framework:**
- **Epic/Sprint:** Use exact terms from workflow states (not "project", not "iteration")
- **Priority levels:** Critical/High/Medium/Low (not "P0/P1/P2/P3", not "Urgent/Important/Normal/Low")
- **Story points:** Fibonacci sequence (not "t-shirt sizes", not "linear 1-10")
- **Workflow state:** "Backlog" (not "TODO", not "Not Started")
**Validation:** Grep user-input-integration-guide.md for framework terms, verify 100% match with CLAUDE.md terminology.

**Cross-Skill Integration Pattern Uniformity:**
- **Same Step 0 structure:** If devforgeai-ideation (STORY-055) and devforgeai-story-creation (STORY-056) both integrate guidance, Step 0 code is nearly identical (only file path differs)
- **Same reference file structure:** user-input-integration-guide.md in both skills follows same template (sections, YAML format, headings)
- **Same token budget:** All skills targeting ≤1,000 token overhead for guidance loading
- **Same fallback behavior:** Graceful degradation to baseline logic (consistent across all skill integrations)

**Logging Message Consistency:**
- **Step 0 success:** "Loading user-input-guidance.md from [path]..." → "Guidance loaded successfully ({pattern_count} patterns extracted)"
- **Step 0 warning:** "user-input-guidance.md not found at [path], proceeding with baseline logic"
- **Pattern application:** "Applying [Pattern Name] to [Question Type] (Phase {phase} Step {step})"
- **Baseline fallback:** "Pattern not available, using baseline logic for [Question Type]"
**No variations:** Same phrasing across all integration points (no "Loading guidance file...", use "Loading user-input-guidance.md...")

**Error Message Consistency Across Skills:**
- **File missing:** "user-input-guidance.md not found at [path], proceeding with baseline logic" (identical wording in ideation, story-creation, architecture, etc.)
- **Parse error:** "Failed to parse patterns from guidance (0 patterns extracted), proceeding with baseline logic"
- **Token budget:** "Guidance loading exceeded token budget ({count} > 1,000), using selective loading or baseline"
**Benefit:** Users see consistent error messages regardless of which skill encountered the issue.

---

## Dependencies

### Prerequisite Stories

- [ ] **STORY-053:** Framework-Internal Guidance Reference
  - **Why:** devforgeai-story-creation loads `user-input-guidance.md` (must exist before integration)
  - **Status:** Created (same batch)
  - **Blocker:** Cannot test STORY-056 integration until STORY-053 file exists

### External Dependencies

None - All dependencies are internal to DevForgeAI framework.

### Technology Dependencies

None - Markdown modification and Read tool usage only (no new packages required).

---

## Test Strategy

### Unit Tests (15 test cases)

**Test File:** `.devforgeai/tests/skills/test-story-creation-guidance-unit.sh`

**Scenarios:**
1. Step 0 loads guidance with valid file (success path)
2. Step 0 handles missing file (graceful degradation)
3. Step 0 handles corrupted markdown (parse error recovery)
4. Pattern extraction from valid content (10 patterns → 10 extracted)
5. Pattern extraction skips malformed patterns (5 valid + 2 malformed → 5 extracted, 2 warnings)
6. Pattern name normalization (various capitalizations → consistent lookup)
7. Pattern-to-question mapping lookup (epic → Explicit Classification + Bounded Choice)
8. Pattern lookup miss (unknown question type → baseline logic fallback)
9. Token measurement for Step 0 (verify ≤1,000 tokens)
10. Baseline fallback when guidance unavailable (all questions use pre-integration logic)
11. Partial pattern application (some patterns available → selective benefit)
12. Pattern selection for epic question (Explicit Classification + Bounded Choice)
13. Pattern selection for sprint question (Bounded Choice)
14. Pattern selection for priority question (Explicit Classification)
15. Pattern selection for points question (Fibonacci Bounded Choice)

**Expected Results:** 15/15 tests pass

---

### Integration Tests (12 test cases)

**Test File:** `.devforgeai/tests/skills/test-story-creation-guidance-integration.sh`

**Scenarios:**
1. Full Phase 1 execution with guidance (all steps, all patterns applied, complete story metadata)
2. Full Phase 1 execution without guidance (baseline behavior, all metadata still collected)
3. Subagent re-invocation measurement (10 stories: 5 with guidance, 5 baseline; measure reduction ≥30%)
4. Token overhead for Phase 1 (measure increase ≤5% vs. baseline)
5. Backward compatibility (30 existing test cases pass with guidance file deleted)
6. Batch mode guidance caching (9 stories, verify Read called once, verify cache reuse)
7. Escalation strategy for incomplete answers (simulate vague responses, verify follow-up questions)
8. Pattern conflict resolution (guidance overrides hardcoded logic verification)
9. Mid-execution guidance changes (modify file during Phase 1, verify no mid-flight reload)
10. Concurrent skill invocations (5 parallel /create-story, all read guidance successfully)
11. Phase 6 epic/sprint linking with guidance-enhanced metadata (verify links correct)
12. End-to-end workflow (create story with guidance → dev → qa, verify no issues)

**Expected Results:** 12/12 tests pass

---

### Regression Tests (10 test cases)

**Test File:** `.devforgeai/tests/skills/test-story-creation-regression.sh`

**Scenarios:**
1. All existing Phase 1 questions still work (no parameter changes)
2. All existing Phase 2-8 phases unaffected (downstream logic unchanged)
3. Skill output format preserved (Phase 8 completion report structure identical)
4. AskUserQuestion call signature unchanged (backward compatible)
5. Baseline question logic preserved (original questions work when guidance unavailable)
6. Phase execution order unchanged (Phases 1-8 sequential, Step 0 is addition not replacement)
7. Epic/sprint linking unchanged (Phase 6 behavior identical)
8. Self-validation unchanged (Phase 7 logic unaffected)
9. Full regression suite passes (30+ existing tests at 100% rate)
10. Story template structure unchanged (YAML frontmatter + markdown sections identical)

**Expected Results:** 10/10 tests pass, 30+ regression suite pass

---

### Performance Tests (8 test cases)

**Test File:** `.devforgeai/tests/skills/test-story-creation-guidance-performance.py`

**Scenarios:**
1. Step 0 execution time with 8K char file (target: <2s p95)
2. Step 0 execution time with 15K char file (stress test: <3s p99)
3. Pattern extraction time for 20 patterns (target: <500ms)
4. Pattern lookup time per question (target: <50ms, measured 10x)
5. Phase 1 execution time increase with guidance (target: ≤5% vs. baseline)
6. Token overhead for Step 0 (target: ≤1,000 tokens)
7. Phase 1 total token increase (target: ≤5% vs. baseline)
8. Memory footprint for guidance cache (target: <5 MB)

**Expected Results:** 8/8 tests pass with measurements under targets

---

## Acceptance Criteria Verification Checklist

### AC#1: Pre-Feature-Capture Guidance Loading

- [ ] Step 0 added to Phase 1 - **Phase:** 2 - **Evidence:** grep "Phase 1.*Step 0.*Load.*guidance" SKILL.md
- [ ] Read tool invoked - **Phase:** 2 - **Evidence:** Read(file_path="src/claude/skills/devforgeai-ideation/references/user-input-guidance.md")
- [ ] Positioned before Step 1 - **Phase:** 2 - **Evidence:** Step 0 line number < Step 1 line number
- [ ] Graceful degradation if missing - **Phase:** 3 - **Evidence:** test_02_step0_handles_missing_file passes
- [ ] <2s execution time - **Phase:** 3 - **Evidence:** test_01_step0_execution_time_p95 passes

### AC#2: Epic Selection Pattern

- [ ] Explicit Classification + Bounded Choice applied - **Phase:** 2 - **Evidence:** grep "Explicit Classification.*Bounded Choice" in Step 3
- [ ] Epic list presented - **Phase:** 2 - **Evidence:** AskUserQuestion options show available epics
- [ ] "None" option explicit - **Phase:** 2 - **Evidence:** grep "None - standalone story" in options
- [ ] Context for each epic - **Phase:** 2 - **Evidence:** Option descriptions show status, complexity
- [ ] Header explains purpose - **Phase:** 2 - **Evidence:** AskUserQuestion header mentions "traceability"

### AC#3: Sprint Assignment Pattern

- [ ] Bounded Choice applied - **Phase:** 2 - **Evidence:** grep "Bounded Choice" in Step 4
- [ ] Sprint list with capacity - **Phase:** 2 - **Evidence:** Options show "Sprint-N: dates, X/Y points"
- [ ] "Backlog" option present - **Phase:** 2 - **Evidence:** grep "Backlog" in options
- [ ] Chronological sorting - **Phase:** 2 - **Evidence:** Sprint list sorted by start date (manual review)

### AC#4: Priority Selection Pattern

- [ ] Explicit Classification applied - **Phase:** 2 - **Evidence:** grep "Explicit Classification" in Step 5 (priority)
- [ ] 4 priority levels - **Phase:** 2 - **Evidence:** Options: Critical, High, Medium, Low
- [ ] Clear descriptions - **Phase:** 2 - **Evidence:** Each option has business impact explanation
- [ ] No "Other" option - **Phase:** 2 - **Evidence:** Options count = 4 (no 5th option)

### AC#5: Story Points Pattern

- [ ] Fibonacci Bounded Choice - **Phase:** 2 - **Evidence:** grep "Fibonacci.*Bounded Choice" in Step 5 (points)
- [ ] 6 Fibonacci values - **Phase:** 2 - **Evidence:** Options: 1, 2, 3, 5, 8, 13
- [ ] Complexity rationales - **Phase:** 2 - **Evidence:** Each option describes complexity (hours/days)
- [ ] 13-point warning - **Phase:** 2 - **Evidence:** If 13 selected, triggers split recommendation

### AC#6: Enhanced Subagent Context

- [ ] Structured metadata in prompt - **Phase:** 2 - **Evidence:** story-requirements-analyst prompt includes ID, epic, priority, points
- [ ] Epic goals context - **Phase:** 2 - **Evidence:** If epic associated, prompt includes epic goals
- [ ] Sprint scope context - **Phase:** 2 - **Evidence:** If sprint assigned, prompt includes sprint scope
- [ ] Complexity constraint - **Phase:** 2 - **Evidence:** Prompt notes "8 points → 5-7 AC expected"
- [ ] ≥30% re-invocation reduction - **Phase:** 4 - **Evidence:** test_06_subagent_reinvocation_reduction passes
- [ ] 85%+ AC completeness - **Phase:** 4 - **Evidence:** Measure across 10 test stories

### AC#7: Token Overhead

- [ ] Step 0 ≤1,000 tokens - **Phase:** 3 - **Evidence:** test_07_token_overhead_measurement passes
- [ ] Phase 1 ≤5% increase - **Phase:** 3 - **Evidence:** test_05_phase1_token_increase passes
- [ ] No re-load per question - **Phase:** 3 - **Evidence:** Read tool called once in Phase 1
- [ ] Methodology documented - **Phase:** 2 - **Evidence:** user-input-integration-guide.md has "Token Measurement" section

### AC#8: Batch Mode Compatibility

- [ ] Guidance loaded once for batch - **Phase:** 3 - **Evidence:** test_06_batch_mode_caching passes (Read called 1x for 9 stories)
- [ ] Cache reused for stories 2-9 - **Phase:** 3 - **Evidence:** Cache hit logs for stories 2-9
- [ ] Amortized ≤1,200 tokens - **Phase:** 3 - **Evidence:** Total batch overhead / 9 ≤ 134 tokens/story
- [ ] Batch markers override patterns - **Phase:** 2 - **Evidence:** Batch mode skips AskUserQuestion (uses markers)
- [ ] All 9 stories created - **Phase:** 3 - **Evidence:** Batch execution creates 9 .story.md files

### AC#9: Backward Compatibility

- [ ] 100% existing tests pass - **Phase:** 3 - **Evidence:** Regression suite 30/30 pass
- [ ] Same story files generated - **Phase:** 3 - **Evidence:** Diff before/after shows only enhanced questions
- [ ] Missing guidance = baseline - **Phase:** 3 - **Evidence:** test_01_all_existing_phase1_questions_work passes
- [ ] No AskUserQuestion changes - **Phase:** 2 - **Evidence:** No signature modifications
- [ ] Outputs unchanged - **Phase:** 3 - **Evidence:** Phase 8 completion report format identical

### AC#10: Reference File Documentation

- [ ] File created (≥500 lines) - **Phase:** 2 - **Evidence:** wc -l user-input-integration-guide.md ≥500
- [ ] Pattern mapping table - **Phase:** 2 - **Evidence:** YAML table in "Pattern Mapping" section
- [ ] Batch caching strategy - **Phase:** 2 - **Evidence:** "Batch Mode Caching" section with lifecycle diagram
- [ ] Token optimization - **Phase:** 2 - **Evidence:** "Token Budget Optimization" section with techniques
- [ ] Backward compat mechanisms - **Phase:** 2 - **Evidence:** "Graceful Degradation" section with hierarchy
- [ ] Pattern update process - **Phase:** 2 - **Evidence:** "Pattern Update Process" section with steps
- [ ] Example transformations - **Phase:** 2 - **Evidence:** Before/after for 4 question types
- [ ] Edge case procedures - **Phase:** 2 - **Evidence:** All 7 edge cases documented with recovery steps
- [ ] Testing procedures - **Phase:** 2 - **Evidence:** Test checklists for 4 test types (unit, integration, regression, performance)
- [ ] SKILL.md references it - **Phase:** 2 - **Evidence:** grep "user-input-integration-guide.md" SKILL.md Phase 1

---

**Checklist Progress:** 0/54 items complete (0%)

---


## Implementation Notes

Status: Backlog - Story created and ready for development. All Definition of Done items will be completed during TDD cycle.
## Definition of Done

### Implementation
- [ ] Step 0 added to `src/claude/skills/devforgeai-story-creation/SKILL.md` Phase 1 (10-15 lines)
- [ ] Pattern application logic added to Steps 3-5 (epic, sprint, priority, points) (~20 lines total)
- [ ] Reference file created: `src/claude/skills/devforgeai-story-creation/references/user-input-integration-guide.md` (≥500 lines)
- [ ] Pattern mapping table documented in reference file (YAML format)
- [ ] Batch mode caching implemented (load once, reuse for stories 2-N)
- [ ] Graceful degradation logic implemented (baseline fallback if guidance unavailable)
- [ ] Selective loading strategy implemented (if token budget exceeded)
- [ ] All inline comments added for code clarity

### Quality
- [ ] All 10 acceptance criteria have passing tests (validation complete)
- [ ] All 7 edge cases documented with detailed recovery procedures
- [ ] All 8 data validation rules enforced with test assertions
- [ ] All 10 NFRs met with measured validation (performance, security, reliability, scalability, maintainability, consistency, testability)
- [ ] No ambiguous requirements (all specifications measurable and testable)
- [ ] No placeholder content (no TODO, TBD, "etc.", "[...]")

### Testing
- [ ] Unit test suite created (15 tests in test-story-creation-guidance-unit.sh)
- [ ] Integration test suite created (12 tests in test-story-creation-guidance-integration.sh)
- [ ] Regression test suite updated (10 tests in test-story-creation-regression.sh)
- [ ] Performance test suite created (8 tests in test-story-creation-guidance-performance.py)
- [ ] All 45 tests passing (15 unit + 12 integration + 10 regression + 8 performance = 100% pass rate)
- [ ] Test fixtures created (5 feature descriptions in tests/user-input-guidance/fixtures/)
- [ ] CI/CD integration configured (tests run on commit to SKILL.md or reference files)

### Documentation
- [ ] user-input-integration-guide.md created with all 10 required sections
- [ ] SKILL.md references integration guide in Phase 1
- [ ] Cross-referenced from user-input-guidance.md (integration points section)
- [ ] Versioned (includes version: 1.0.0 in reference file header)
- [ ] Synced to operational folder (.claude/skills/devforgeai-story-creation/)
- [ ] Test documentation included (how to run tests, interpret results)

---

## Workflow History

### 2025-01-20 20:45:00 - Status: Ready for Dev
- Added to SPRINT-2: User Input Guidance Implementation
- Transitioned from Backlog to Ready for Dev
- Sprint capacity: 40 points (9 stories)
- Priority in sprint: [5 of 9] - Story creation skill integration

---

## Workflow Status

- [ ] Architecture phase complete
- [ ] Development phase complete
- [ ] QA phase complete
- [ ] Released

---

## Notes

**Design Decisions:**
- **Step 0 placement:** Before Step 1 (Generate Story ID) ensures guidance available for all metadata collection in Steps 3-5
- **Batch mode caching:** Load once, reuse for N stories maximizes token efficiency (111 tokens/story amortized for 9-story batch)
- **Selective loading fallback:** If guidance file grows large, extract only critical patterns (maintains benefit while respecting budget)
- **Per-question fallback:** Each question has independent pattern lookup with baseline fallback (one pattern failure doesn't cascade)

**Integration Architecture:**
```
Phase 1 Flow:
Step 0: Load guidance (NEW)
  ↓ (guidance available in context)
Step 1: Generate Story ID
Step 2: Discover Epic Context
Step 3: Epic selection with Explicit Classification + Bounded Choice pattern (ENHANCED)
Step 4: Sprint assignment with Bounded Choice pattern (ENHANCED)
Step 5: Priority with Explicit Classification pattern (ENHANCED)
Step 5: Points with Fibonacci Bounded Choice pattern (ENHANCED)
  ↓ (enhanced metadata)
Phase 2: Requirements Analysis (story-requirements-analyst receives richer context)
```

**Value Proposition:**
- **Primary value:** 30%+ reduction in subagent re-invocations (2.5 → ≤1.75 avg)
- **Secondary value:** Improved user experience (clearer prompts, better context)
- **Tertiary value:** Framework cohesion (consistent patterns across skills)
- **Token ROI:** 1,000 token investment saves 10,000 tokens from avoided re-invocations (10x return)

**Success Metrics (Measurable):**
- **Re-invocation rate:** Baseline 2.5 → Target ≤1.75 (measured over 10 test stories)
- **AC completeness:** Baseline 60% → Target 85%+ (first-attempt complete requirements)
- **Token efficiency:** 115K baseline → 105K target (9% improvement per story)
- **User satisfaction:** Qualitative feedback on prompt clarity

**Framework Integration Points:**
- **Invoked by:** /create-story command, devforgeai-orchestration (epic decomposition), devforgeai-development (deferred tracking)
- **Uses:** user-input-guidance.md (loaded), story-requirements-analyst (receives enhanced context)
- **Outputs to:** devforgeai-development (AC → tests), devforgeai-qa (validation targets)

**Related ADRs:**
None required (skill enhancement for quality improvement, not architectural change)

**References:**
- **EPIC-011:** User Input Guidance System (parent epic)
- **STORY-053:** user-input-guidance.md (dependency - guidance file)
- **STORY-052:** effective-prompting-guide.md (user-facing counterpart)
- **devforgeai-ideation:** Sister skill with similar integration (STORY-055)

---

**Story Template Version:** 2.0
**Created:** 2025-01-20
