---
description: Run QA validation on story implementation
argument-hint: [STORY-ID] [mode]
# Mode: 'deep' or 'light' (no -- prefix)
model: sonnet
allowed-tools: Read, Write, Edit, Glob, Grep, Skill, Bash
---

# /qa - Quality Assurance Validation Command

Execute QA validation on story implementation using light or deep mode.

## Context Loading

**Story File:**
```
@.ai_docs/Stories/$1.story.md
```

## Command Workflow

### Phase 0: Argument Validation

**Extract arguments:**
```
STORY_ID = $1
MODE_ARG = $2 (optional)
```

**Validate story ID format:**
```
IF $1 is empty OR does NOT match pattern "STORY-[0-9]+":
  AskUserQuestion:
  Question: "Story ID '$1' doesn't match format STORY-NNN. What story should I validate?"
  Header: "Story ID"
  Options:
    - "List stories in Dev Complete status"
    - "List stories in In Development status"
    - "Show correct /qa command syntax"
  multiSelect: false

  Extract STORY_ID from user response
```

**Validate story file exists:**
```
Glob(pattern=".ai_docs/Stories/${STORY_ID}*.story.md")

IF no matches found:
  AskUserQuestion:
  Question: "Story ${STORY_ID} not found. What should I do?"
  Header: "Story not found"
  Options:
    - "List all available stories"
    - "Cancel command"
  multiSelect: false
```

**Parse mode argument:**
```
IF $2 provided:
  IF $2 in ["deep", "light"]:
    MODE = $2

  ELSE IF $2 starts with "--mode=":
    # User used flag syntax (educate them)
    EXTRACTED_MODE = substring after "--mode="

    IF EXTRACTED_MODE in ["deep", "light"]:
      MODE = EXTRACTED_MODE

      Note to user: "Flag syntax (--mode=) not needed. Use: /qa STORY-001 deep"

    ELSE:
      AskUserQuestion:
      Question: "Unknown mode in flag: $2. Which validation mode?"
      Header: "QA Mode"
      Options:
        - "deep (comprehensive validation ~2 min)"
        - "light (quick checks ~30 sec)"
      multiSelect: false

  ELSE IF $2 starts with "--":
    # Unknown flag
    AskUserQuestion:
    Question: "Unknown flag: $2. Which validation mode?"
    Header: "QA Mode"
    Options:
      - "deep (comprehensive validation)"
      - "light (quick checks)"
    multiSelect: false

  ELSE:
    # Unknown value (not deep/light, not a flag)
    AskUserQuestion:
    Question: "Unknown mode: $2. Which validation mode?"
    Header: "QA Mode"
    Options:
      - "deep (comprehensive validation)"
      - "light (quick checks)"
    multiSelect: false

ELSE:
  # No mode provided - use intelligent default based on story status
  # Story content already loaded, check status from YAML frontmatter

  IF story status == "Dev Complete":
    MODE = "deep"  # Full validation before QA approval
  ELSE IF story status == "In Development":
    MODE = "light"  # Quick validation during development
  ELSE:
    # Unclear - ask user
    AskUserQuestion:
    Question: "No mode specified. Which validation?"
    Header: "QA Mode"
    Options:
      - "deep (comprehensive - for Dev Complete stories)"
      - "light (quick - for In Development stories)"
    multiSelect: false
```

**Validation summary:**
```
✓ Story ID: ${STORY_ID}
✓ Story file: ${STORY_FILE}
✓ Validation mode: ${MODE}
✓ Proceeding with QA validation...
```

---

### Phase 1: Invoke QA Skill

**Context for skill:**
- Story content loaded via @file reference above
- Story ID: ${STORY_ID}
- Validation mode: ${MODE}

**Skill Invocation:**
```
Skill(command="devforgeai-qa")
```

**Note:** Skill will extract story ID from conversation context (YAML frontmatter) and mode from the explicit statement above

**Mode Selection Logic:**
- **Light Mode (~10K tokens):**
  - Build/syntax checks
  - Test execution (pass/fail)
  - Quick anti-pattern scan (security-critical only)
  - Used during development phases (Red → Green → Refactor → Integration)

- **Deep Mode (~65K tokens):**
  - Full test coverage analysis (95%/85%/80% thresholds)
  - Comprehensive anti-pattern detection (10+ categories)
  - Spec compliance validation (acceptance criteria, API contracts, NFRs)
  - Code quality metrics (complexity, maintainability, duplication, docs)
  - Used after story completion (Dev Complete → QA In Progress)

**Skill Execution:**
The devforgeai-qa skill performs:
1. Context validation (6 context files exist)
2. Build verification
3. Test suite execution
4. Mode-specific analysis (light vs deep)
5. Deferral validation (NEW - RCA-006)
6. QA report generation
7. Story status update

---

### Phase 2: Handle QA Results (NEW - RCA-006)

**Wait for QA skill to complete, then read QA report:**

```
Read QA report: .devforgeai/qa/reports/{STORY_ID}-qa-report.md
Parse report status: PASSED or FAILED
```

**IF QA PASSED:**

```
Display success summary (existing logic in Phase 4)
Proceed to next steps (release or continue development)
```

**IF QA FAILED:**

```
Parse failure reasons from report

Check if failure includes deferral validation issues:
Grep(pattern="Deferral Validation FAILED|Unjustified Deferrals", path=QA report)

IF deferral failures found:
    # Special handling for deferral failures

    Extract deferral violations from report

    Display to user:
    "❌ QA Failed: Deferral Validation Issues

    Story: {STORY_ID}

    Unjustified Deferrals Detected:
    {list each deferral violation with severity, item, current reason, required action}

    Required Actions:
    1. Fix deferral justifications OR
    2. Complete deferred work

    Then re-run QA validation with /qa {STORY_ID} {MODE}"

    AskUserQuestion:
        Question: "How to proceed with deferral failures?"
        Header: "QA deferral failure"
        Options:
            - "Return to development (/dev will fix deferrals)"
            - "I'll fix manually, then re-run /qa"
            - "Review detailed QA report first"
        multiSelect: false

    IF "Return to development":
        Display: "Run: /dev {STORY_ID}
                 Dev skill will read QA report and help resolve deferral issues."
        Exit command

    IF "Review detailed QA report":
        Display: "QA Report: .devforgeai/qa/reports/{STORY_ID}-qa-report.md
                 After review, run /dev {STORY_ID} to fix issues."
        Exit command

    IF "I'll fix manually":
        Display: "After fixing, re-run: /qa {STORY_ID} {MODE}"
        Exit command

ELSE IF other QA failures (coverage, anti-patterns, etc.):
    # Display standard QA failure handling (existing logic)
    Display failure summary
    List violations by severity
    Provide remediation guidance
```

---

### Phase 3: Result Verification

**Check QA Report Generated:**
```
Expected path: .devforgeai/qa/reports/{STORY-ID}-qa-report.md
```

**Read QA Report:**
1. Use Read tool to load report contents
2. Parse report sections:
   - Validation Summary (PASSED/FAILED)
   - Violation Counts (CRITICAL/HIGH/MEDIUM/LOW)
   - Coverage Results (if deep mode)
   - Spec Compliance Results
   - Quality Metrics
   - Recommendation (APPROVE/FAIL)

**Verify Story Status Updated:**
```
Read story file frontmatter
Expected status changes:
  - Light mode: Status unchanged (blocks on failure)
  - Deep mode PASSED: "QA Approved"
  - Deep mode FAILED: "QA Failed"
```

**Error Handling:**
- **Report not found:** Skill execution failed, display error and skill output
- **Report unparseable:** Malformed report, display raw contents
- **Status not updated:** Skill failed to update story, manual intervention required

### Phase 4: Display Results

**Success Display (Light Mode):**
```markdown
## ✅ Light QA Validation PASSED - {STORY-ID}

**Story:** {STORY-TITLE}
**Mode:** Light
**Status:** {CURRENT-STATUS} (unchanged)

### Quick Checks
✓ Build successful
✓ All tests passing ({PASS-COUNT}/{TOTAL-COUNT})
✓ No critical anti-patterns detected

**Note:** Light validation passed. Continue development or run deep validation when story is Dev Complete.

**Next Steps:**
- Continue implementation if in development
- Run `/qa {STORY-ID} --mode=deep` when Dev Complete
```

**Success Display (Deep Mode):**
```markdown
## ✅ Deep QA Validation PASSED - {STORY-ID}

**Story:** {STORY-TITLE}
**Mode:** Deep
**Status:** Dev Complete → QA Approved ✓

### Validation Results

**Test Coverage:**
- Business Logic: {BUSINESS-LOGIC-PCT}% (threshold: ≥95%)
- Application Layer: {APPLICATION-PCT}% (threshold: ≥85%)
- Infrastructure: {INFRASTRUCTURE-PCT}% (threshold: ≥80%)
- Overall: {OVERALL-PCT}%

**Code Quality:**
- Cyclomatic Complexity: {AVG-COMPLEXITY} avg (threshold: <10)
- Maintainability Index: {MAINTAINABILITY} (threshold: ≥70)
- Code Duplication: {DUPLICATION-PCT}% (threshold: <5%)
- Documentation Coverage: {DOCS-PCT}% (threshold: ≥80%)

**Violations:**
- CRITICAL: 0
- HIGH: 0
- MEDIUM: {MEDIUM-COUNT}
- LOW: {LOW-COUNT}

**Spec Compliance:**
✓ All acceptance criteria validated
✓ API contracts match specification
✓ Non-functional requirements met

### Recommendation
✅ **APPROVE** - Story meets all quality gates and is ready for release.

**Next Steps:**
1. Review QA report: .devforgeai/qa/reports/{STORY-ID}-qa-report.md
2. Ready for release: `/release {STORY-ID}`
3. Or return to sprint board: `/board`
```

**Failure Display:**
```markdown
## ❌ QA Validation FAILED - {STORY-ID}

**Story:** {STORY-TITLE}
**Mode:** {MODE}
**Status:** {CURRENT-STATUS} → QA Failed

### Violation Summary

**CRITICAL Violations ({COUNT}):**
{List critical violations with file:line references}

**HIGH Violations ({COUNT}):**
{List high violations with file:line references}

**MEDIUM Violations ({COUNT}):**
{Summary or count only}

**LOW Violations ({COUNT}):**
{Summary or count only}

### Coverage Gaps (if deep mode)
{List uncovered files/methods below thresholds}

### Failed Acceptance Criteria
{List AC not validated by tests}

### Recommendation
❌ **FAIL** - Story has blocking violations and must be fixed.

**Required Actions:**
1. Fix all CRITICAL violations (blocks release)
2. Fix all HIGH violations (or request approved exception)
3. Add tests to meet coverage thresholds
4. Ensure all acceptance criteria have test coverage
5. Re-run QA validation: `/qa {STORY-ID} --mode={MODE}`

**Detailed Report:**
See .devforgeai/qa/reports/{STORY-ID}-qa-report.md for full analysis.
```

**Coverage Failure Display (Deep Mode):**
```markdown
## ⚠️ Coverage Thresholds Not Met - {STORY-ID}

**Story:** {STORY-TITLE}
**Status:** QA Failed (Coverage)

### Coverage Results
- Business Logic: {PCT}% ❌ (required: ≥95%)
- Application Layer: {PCT}% ❌ (required: ≥85%)
- Infrastructure: {PCT}% ✓ (required: ≥80%)

### Uncovered Code
{List files/methods with insufficient coverage}

### Required Actions
1. Add unit tests for uncovered business logic
2. Add integration tests for uncovered application code
3. Target coverage increases:
   - Business Logic: +{DELTA}% needed
   - Application Layer: +{DELTA}% needed
4. Re-run QA: `/qa {STORY-ID} --mode=deep`

**Use test stub generator:**
```bash
python .claude/skills/devforgeai-qa/scripts/generate_test_stubs.py \
  --coverage-report=.devforgeai/qa/coverage/coverage-report.json \
  --output-dir=tests/generated/ \
  --framework={FRAMEWORK}
```
```

**Spec Compliance Failure Display:**
```markdown
## ⚠️ Spec Compliance Issues - {STORY-ID}

**Story:** {STORY-TITLE}
**Status:** QA Failed (Spec Compliance)

### Failed Acceptance Criteria
{List AC without test validation}

### API Contract Mismatches
{List endpoint/method mismatches from spec}

### Missing Non-Functional Requirements
{List NFRs not validated}

### Required Actions
1. Add tests for missing acceptance criteria
2. Update API implementation to match contracts
3. Implement or validate NFRs (performance, security, etc.)
4. Update story spec if requirements changed (create ADR)
5. Re-run QA: `/qa {STORY-ID} --mode=deep`
```

### Phase 5: Summary and Next Actions

**Display Next Steps Based on Result:**

**On Light Mode Pass:**
```markdown
## Next Actions
- Continue development workflow
- Run deep validation when story Dev Complete
- Use `/dev {STORY-ID}` to continue implementation
```

**On Deep Mode Pass (QA Approved):**
```markdown
## Next Actions
✓ Story approved and ready for release
- Review full QA report for insights
- Deploy to production: `/release {STORY-ID}`
- Or view sprint progress: `/board`
```

**On Any Failure:**
```markdown
## Next Actions
❌ Fix violations before proceeding
1. Review detailed report: .devforgeai/qa/reports/{STORY-ID}-qa-report.md
2. Address CRITICAL violations (required)
3. Address HIGH violations (or document exceptions)
4. Re-run validation: `/qa {STORY-ID} --mode={MODE}`
5. If light mode failed, do NOT proceed to deep mode

**Development Loop:**
`/dev {STORY-ID}` → Fix issues → `/qa {STORY-ID}` → Repeat until pass
```

## Error Handling Matrix

### Story Not Found
```
Error: Story file not found: .ai_docs/Stories/{STORY-ID}.story.md

Available stories:
{List stories from Glob(".ai_docs/Stories/*.story.md")}

Usage: /qa [STORY-ID] [--mode=light|deep]
Example: /qa STORY-001 --mode=deep
```

### Invalid Story Status (Deep Mode)
```
Error: Story status must be "Dev Complete" for deep QA validation

Current status: {CURRENT-STATUS}
Story: {STORY-ID} - {STORY-TITLE}

Actions:
- For light validation during development: /qa {STORY-ID} --mode=light
- Complete implementation first: /dev {STORY-ID}
- Update status to "Dev Complete" before deep validation
```

### QA Skill Execution Failed
```
Error: QA skill execution failed

Story: {STORY-ID}
Mode: {MODE}

Skill output:
{Display skill error output}

Troubleshooting:
1. Verify context files exist: ls .devforgeai/context/
2. Verify tests can run: {test-command for stack}
3. Check build succeeds: {build-command for stack}
4. Review skill logs above for specific error

If issue persists, run development skill to fix build/test issues:
/dev {STORY-ID}
```

### Missing Context Files
```
Error: QA validation requires context files

Missing files:
{List missing context files from .devforgeai/context/}

Required files:
- tech-stack.md
- source-tree.md
- dependencies.md
- coding-standards.md
- architecture-constraints.md
- anti-patterns.md

Run architecture skill to generate context:
/arch
```

### Report Generation Failed
```
Error: QA report not generated

Expected path: .devforgeai/qa/reports/{STORY-ID}-qa-report.md
Skill executed but report missing.

Possible causes:
1. Skill interrupted before completion
2. File system permission issues
3. Report directory doesn't exist

Actions:
1. Create report directory: mkdir -p .devforgeai/qa/reports
2. Re-run QA validation: /qa {STORY-ID} --mode={MODE}
3. Check skill output above for errors
```

### Invalid Mode Argument
```
Error: Invalid mode specified: {PROVIDED-MODE}

Valid modes:
- light: Quick validation during development (~10K tokens)
- deep: Comprehensive validation after Dev Complete (~65K tokens)

Usage: /qa [STORY-ID] [--mode=light|deep]
Examples:
  /qa STORY-001              # Deep mode (default)
  /qa STORY-001 --mode=light # Light mode
  /qa STORY-001 --mode=deep  # Explicit deep mode
```

## Command Options Reference

### Mode: Light (~10K tokens)
**When to use:**
- During development (any status before Dev Complete)
- Quick feedback loop (Red → Green → Refactor)
- Pre-commit validation
- Blocking validation (halts on any failure)

**What it checks:**
- Build succeeds
- Tests pass (100% pass rate)
- Critical security anti-patterns only
- No coverage analysis
- No spec compliance validation

**Status impact:**
- Does NOT change story status
- Blocks development on failure

### Mode: Deep (~65K tokens)
**When to use:**
- After story implementation complete (status: Dev Complete)
- Before release (quality gate)
- Final validation before QA approval
- Comprehensive quality assessment

**What it checks:**
- Full test coverage (95%/85%/80% thresholds)
- 10+ anti-pattern categories
- Spec compliance (AC, API contracts, NFRs)
- Code quality metrics
- Documentation coverage
- Security scanning

**Status impact:**
- Updates story status on success: "QA Approved"
- Updates story status on failure: "QA Failed"

## Success Criteria

- [ ] Story identified and validated
- [ ] QA skill invoked with correct mode
- [ ] QA report generated successfully
- [ ] Story status updated (if deep mode)
- [ ] Results displayed with clear summary
- [ ] Next actions provided based on outcome
- [ ] Token usage within budget (light <15K, deep <70K)

## Integration with Framework

**Invoked by:**
- Manual: Developer runs `/qa {STORY-ID}`
- devforgeai-development skill (light mode after phases 3, 4, 5)
- devforgeai-orchestration skill (deep mode for quality gates)

**Invokes:**
- devforgeai-qa skill (performs actual validation)

**Updates:**
- Story status (deep mode only)
- QA report in .devforgeai/qa/reports/
- Workflow history in story document (via skill)

**Quality Gates:**
- Light mode: Blocks development on failure
- Deep mode: Blocks release on CRITICAL/HIGH violations
- Deep mode: Blocks release on coverage below thresholds

## Performance Targets

**Light Mode:**
- Token usage: <15K
- Execution time: <2 minutes
- Report size: <50 lines

**Deep Mode:**
- Token usage: <70K
- Execution time: <5 minutes
- Report size: 200-400 lines

## Related Commands

- `/dev {STORY-ID}` - Implement story with TDD
- `/release {STORY-ID}` - Deploy QA-approved story
- `/board` - View sprint progress
- `/stories` - List all stories

## Example Usage

```bash
# Quick validation during development
/qa STORY-001 --mode=light

# Full validation after implementation
/qa STORY-001 --mode=deep

# Default mode is deep
/qa STORY-001
```

## Implementation Notes

**Token Optimization:**
- Thin wrapper pattern (skill does analysis)
- Command handles validation and display only
- Parallel tool invocations where possible
- Cache context files in memory

**Error Recovery:**
- All errors provide actionable next steps
- Clear error messages with examples
- Graceful degradation (partial results shown)

**User Experience:**
- Color-coded results (✅ ❌ ⚠️)
- Summary-first display (details on demand)
- Clear next actions based on outcome
- Link to detailed report for deep dives
