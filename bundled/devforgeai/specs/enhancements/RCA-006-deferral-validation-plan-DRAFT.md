# RCA-006: Quality Gate Failure - Deferral Without Justification

**Issue:** Dev agent defers DoD items without justification, QA approves anyway, creating technical debt
**Date:** 2025-11-03
**Priority:** 🔴 CRITICAL - Quality gate integrity compromised
**Status:** ✅ PLAN COMPLETE - Ready for implementation in fresh Claude session
**Related:** RCA-005 (slash command parameter passing)

---

## Executive Summary

**Problem Discovered:**
During TreeLint Codelens project development:
1. Dev agent deferred DoD items from STORY-004 and STORY-005 without user approval
2. QA skill approved both stories despite unjustified deferrals
3. No feedback loop exists for QA failures back to dev
4. Circular deferrals created (STORY-004 → STORY-005 → STORY-004)
5. Technical debt accumulated in "QA Approved" state

**Evidence:**
- STORY-004: Exit code handling deferred without justification, QA passed
- STORY-005: Scenarios 8, 9 deferred, QA passed
- QA reports show deferrals noted but not validated
- No ADRs created for scope changes
- No follow-up stories created for deferred work

**Impact:**
- Quality gate credibility compromised ("QA Approved" includes incomplete work)
- Technical debt in production
- Circular deferrals leave gaps unfilled
- Framework allows under-delivery without justification

**Root Cause:**
1. Dev skill allows autonomous deferrals (no AskUserQuestion requirement)
2. QA skill validates "reason exists" not "reason is justified"
3. No feedback loop: QA FAIL → Dev fix → QA re-evaluate
4. No mechanism to create follow-up stories for deferred work
5. Subagents not invoked (existing subagents are silos)

---

## Solution Overview

### Core Principle: "Complete or Justify - No Free Deferrals"

**Three-Tier Enforcement:**

1. **Prevention (Dev Skill):**
   - AskUserQuestion for ALL deferrals (user must approve)
   - Create follow-up story or ADR when deferring
   - Early warning from code-reviewer subagent

2. **Detection (QA Skill):**
   - Validate all deferrals have justification
   - Detect circular deferrals
   - Validate story/ADR references
   - FAIL QA if deferrals unjustified

3. **Resolution (Orchestration + Commands):**
   - Feedback loop: Dev → QA FAIL → Dev fix → QA re-evaluate
   - Track technical debt from deferrals
   - Analyze deferral patterns

---

## Detailed Implementation Plan

### Component 1: QA Skill Enhancement (3 hours)

**File:** `.claude/skills/devforgeai-qa/SKILL.md`

**Change 1.1: Add Step 0b - Validate Deferral Justifications**

**Location:** After line 484 (after Step 0: Story Documentation Validation)

**Implementation:**

```markdown
### Step 0b: Validate Deferral Justifications (CRITICAL)

**Purpose:** Ensure all incomplete Definition of Done items have valid technical justifications

**Extract incomplete DoD items:**
```
Read Implementation Notes > Definition of Done Status section
Parse all items marked [ ] (incomplete)
FOR each incomplete item:
    Extract: Item description, Deferral reason
```

**Deferral Validation Categories:**

**Category 1: Valid Deferrals (Pass Validation)**

1. **External Blocker (External dependency not ready)**
   - Pattern: "Blocked by {external_system}: {specific_reason}"
   - Validation: Check blocker is external (not internal code/decision)
   - Requires: ETA or condition for blocker resolution
   - Example: "Blocked by Payment API v2 (available 2025-12-01)"
   - Action: Log to technical debt register

2. **Scope Change with ADR (Requirements changed)**
   - Pattern: "Out of scope: ADR-XXX"
   - Validation: Verify ADR-XXX exists in .devforgeai/adrs/
   - Validation: ADR created within last 30 days (recent decision)
   - Example: "Out of scope: ADR-042 descoped performance benchmarks"
   - Action: Verify ADR documents this specific scope change

3. **Story Split (Work moved to follow-up story)**
   - Pattern: "Deferred to STORY-XXX: {justification}"
   - Validation: Verify STORY-XXX exists via Glob
   - Validation: Verify STORY-XXX acceptance criteria includes deferred work
   - Validation: Check STORY-XXX status is Backlog or Ready for Dev
   - Example: "Deferred to STORY-125 (performance optimization epic)"
   - Action: Verify no circular deferral

**Category 2: Invalid Deferrals (FAIL QA)**

1. **No Justification**
   - Pattern: "Not completed" OR "Deferred" with no reason
   - Violation: "Missing deferral justification"
   - Severity: HIGH

2. **Vague Reason**
   - Pattern: "Will add later", "Not enough time", "Too complex"
   - Violation: "Invalid deferral reason (not technical)"
   - Severity: HIGH

3. **Circular Deferral**
   - Pattern: Story A → Story B, Story B → Story A
   - Violation: "Circular deferral detected"
   - Severity: CRITICAL

4. **Invalid Story Reference**
   - Pattern: "Deferred to STORY-XXX" but STORY-XXX doesn't exist
   - Violation: "Referenced story not found"
   - Severity: HIGH

5. **Scope Change Without ADR**
   - Pattern: "Out of scope" but no ADR-XXX reference
   - Violation: "Scope change requires ADR documentation"
   - Severity: MEDIUM

**Validation Procedure:**

```
FOR each incomplete DoD item:
    reason = extract_deferral_reason(item)

    # Check reason type
    IF reason matches "Blocked by {external}":
        Validate external blocker is real
        IF blocker is internal code/decision:
            VIOLATION: "Internal blocker - should be resolved in story"
            Severity: HIGH

    ELSE IF reason matches "Out of scope: ADR-XXX":
        Glob(pattern=".devforgeai/adrs/ADR-{XXX}*.md")
        IF not found:
            VIOLATION: "ADR-{XXX} not found"
            Severity: MEDIUM
        ELSE:
            Read ADR to verify it documents this scope change
            IF ADR doesn't mention this item:
                VIOLATION: "ADR doesn't document this scope change"
                Severity: MEDIUM

    ELSE IF reason matches "Deferred to STORY-{XXX}":
        # Check story exists
        Glob(pattern=".ai_docs/Stories/STORY-{XXX}*.md")
        IF not found:
            VIOLATION: "Referenced STORY-{XXX} not found"
            Severity: HIGH
        ELSE:
            # Invoke subagent for deep validation
            Task(
                subagent_type="story-dependency-validator",
                prompt="Validate STORY-{XXX} includes work: '{item}'"
            )

            # Check for circular deferral
            Read STORY-{XXX} Implementation Notes
            IF STORY-{XXX} also defers this work:
                VIOLATION: "Circular deferral detected"
                Severity: CRITICAL
                Details: "Current story → STORY-{XXX} → (back to current or another)"

    ELSE IF reason is empty OR vague ("later", "not enough time", "too complex"):
        VIOLATION: "Invalid deferral reason"
        Severity: HIGH

    ELSE:
        VIOLATION: "Unrecognized deferral pattern"
        Severity: MEDIUM

# Generate deferral validation section in QA report
IF any CRITICAL or HIGH deferral violations:
    QA Status: FAILED
    Add section to QA report:

    ## Deferral Validation FAILED

    Unjustified Deferrals: {count}

    {list each violation with severity, item, reason, required action}

    Required Actions Before QA Approval:
    1. Complete deferred items OR
    2. Create proper justifications:
       - Create follow-up story (STORY-XXX)
       - Create ADR for scope change (ADR-XXX)
       - Document external blocker with ETA
```

**Update Phase 3 Success Criteria (line ~520):**

Add:
- All incomplete DoD items have valid justification
- No circular deferrals detected
- All story references validated (exist + include work)
- All ADR references validated (exist + document change)

---

**Change 1.2: Add Phase 5b - Track QA Iteration History**

**Location:** After line 807 (after Phase 5: Generate QA Report)

**Implementation:**

```markdown
### Phase 5b: Track QA Iteration History

**Purpose:** Maintain audit trail of QA attempts and deferral resolutions

**Check if this is a re-validation:**

```
Grep(pattern="## QA Validation History", path=".ai_docs/Stories/{story-id}.story.md")

IF found:
    # This is a re-validation
    Count previous QA attempts
    Read previous QA results
```

**Append to story file:**

```
Edit story file to add QA iteration entry:

## QA Validation History

### QA Attempt {N} - {timestamp} - {PASSED/FAILED}

**Mode:** {deep/light}
**Duration:** {duration}

**Results:**
- Test Coverage: {coverage}%
- Violations: CRITICAL: {n}, HIGH: {n}, MEDIUM: {n}, LOW: {n}
- Deferral Validation: {PASSED/FAILED}

{IF FAILED}
**Deferral Issues:**
1. {item}: {violation_type} - {reason}
2. {item}: {violation_type} - {reason}

**Resolution Required:**
- {specific_actions}

{IF PASSED}
**Deferrals Validated:**
- All {count} deferrals have valid justification
- {count} follow-up stories created
- {count} ADRs documented

**Report:** .devforgeai/qa/reports/{story-id}-qa-report-attempt-{N}.md
```

**Track metrics:**

```
Calculate and log:
- Total QA attempts for this story
- Deferral resolution time (first attempt → final pass)
- Number of deferrals resolved vs. justified
```

---

### Component 2: Dev Skill Enhancement (2.5 hours)

**File:** `.claude/skills/devforgeai-development/SKILL.md`

**Change 2.1: Update Phase 6 Step 1 - Require User Approval for Deferrals**

**Location:** Lines 569-582 (Definition of Done Status section)

**Replace current text with:**

```markdown
### Step 1: Update Definition of Done Status (WITH DEFERRAL VALIDATION)

**Copy each Definition of Done item from story, marking completion status:**

```
FOR each DoD item in story acceptance criteria:
    IF item is complete:
        Mark: [x] {item} - Completed: {brief_completion_note}

    ELSE:
        # Item not complete - MUST get user approval to defer

        AskUserQuestion:
            Question: "DoD item not complete: '{item}'. How should we proceed?"
            Header: "Incomplete DoD item"
            Options:
                - "Complete it now (continue development to finish item)"
                - "Defer to follow-up story (create STORY-XXX for tracking)"
                - "Scope change (requirements changed - requires ADR)"
                - "External blocker (document dependency with ETA)"
            multiSelect: false

        BASED ON USER SELECTION:

        **Option 1: "Complete it now"**
        ```
        Return to Phase 2-4 (TDD cycle)
        Implement the DoD item
        Run tests
        Mark: [x] {item} - Completed: {note}
        ```

        **Option 2: "Defer to follow-up story"**
        ```
        AskUserQuestion:
            Question: "Create follow-up story for '{item}' now or later?"
            Options:
                - "Create now (I'll approve story details)"
                - "I'll create manually later (provide story ID)"

        IF "Create now":
            Task(
                subagent_type="requirements-analyst",
                prompt="Create follow-up story for deferred work:

                        Original Story: {current_story_id}
                        Deferred DoD Item: '{item}'

                        Extract acceptance criteria from original item.
                        Set dependency: prerequisite_stories: [{current_story_id}]
                        Set epic: {current_epic}
                        Set status: Backlog

                        Return new story ID."
            )

            new_story_id = {result from subagent}

            Mark: [ ] {item} - Deferred to {new_story_id}: Work split for focused implementation

        ELSE:
            AskUserQuestion:
                Question: "What is the follow-up story ID?"
                (User must provide STORY-XXX ID)

            Verify story exists:
            Glob(pattern=".ai_docs/Stories/{user_provided_id}*.md")
            IF not found:
                WARN: "Story doesn't exist yet. You must create it."

            Mark: [ ] {item} - Deferred to {user_provided_id}: {get reason from user}
        ```

        **Option 3: "Scope change (requires ADR)"**
        ```
        AskUserQuestion:
            Question: "Create ADR documenting scope change now or later?"
            Options:
                - "Create now (I'll provide justification)"
                - "I'll create manually later (provide ADR number)"

        IF "Create now":
            Task(
                subagent_type="architect-reviewer",
                prompt="Create ADR for scope change:

                        Story: {current_story_id}
                        Descoped Item: '{item}'

                        Document:
                        - Why requirement changed
                        - Business justification
                        - Impact on system
                        - Alternatives considered

                        Return ADR number."
            )

            adr_number = {result from subagent}

            Mark: [ ] {item} - Out of scope: ADR-{adr_number} documents scope change

        ELSE:
            AskUserQuestion:
                Question: "What is the ADR number?"
                (User must provide ADR-XXX number)

            Mark: [ ] {item} - Out of scope: ADR-{user_provided_adr}
        ```

        **Option 4: "External blocker"**
        ```
        AskUserQuestion:
            Question: "Describe the external blocker for '{item}'"
            Free-form: "Example: Payment API v2 not available until 2025-12-01"

        blocker_description = {user input}

        Validate blocker is external:
        IF blocker_description contains internal terms (our code, our API, our module):
            WARN: "This seems like an internal blocker, not external. Are you sure?"
            AskUserQuestion:
                Question: "Is this truly an external blocker (outside our control)?"
                Options: ["Yes - external dependency", "No - I can resolve it now"]

            IF "No":
                Return to "Complete it now" path

        Mark: [ ] {item} - Blocked by: {blocker_description}

        # Log to technical debt register
        Add to .devforgeai/technical-debt-register.md:
            "- {item} (from {story_id}): Blocked by {blocker_description}"
        ```
```

**Add validation after all DoD items processed:**

```
# Ensure all incomplete items have user-approved justifications
incomplete_items = count_items_marked_incomplete()

IF incomplete_items > 0:
    Display summary:
    "Definition of Done Status:
     - Complete: {complete_count}/{total_count}
     - Deferred: {deferred_count}
       - Story splits: {story_split_count} (follow-up stories created)
       - Scope changes: {scope_change_count} (ADRs created)
       - External blockers: {blocker_count} (tracked in tech debt register)

    All deferrals have user approval and proper justification ✓"
```

---

**Change 2.2: Add Section - Handling QA Deferral Failures**

**Location:** After line 654 (after Implementation Notes template)

**Implementation:**

```markdown
## Handling QA Deferral Failures

**When invoked after QA failure due to deferrals:**

**Step 1: Detect QA failure context**

```
Check for QA report:
Glob(pattern=".devforgeai/qa/reports/{story-id}-qa-report*.md")

IF multiple reports found (multiple QA attempts):
    Read most recent report

IF report status is "FAILED":
    Parse failure reasons

    IF failure includes "Deferral Validation FAILED":
        # This is a deferral-specific failure
        Extract deferral violations from report

        Display to user:
        "Previous QA attempt failed due to deferral issues:

         Unjustified Deferrals:
         1. '{item}': {violation_type}
            Current reason: '{reason}'
            Required: {required_action}

         2. '{item}': {violation_type}
            Current reason: '{reason}'
            Required: {required_action}"
```

**Step 2: Resolve each deferral issue**

```
FOR each deferral violation from QA report:
    AskUserQuestion:
        Question: "QA flagged deferral for '{item}'. How to resolve?"
        Header: "Deferral issue"
        Options:
            - "Complete the work now (implement {item})"
            - "Create follow-up story (proper tracking)"
            - "Create ADR (document scope change)"
            - "Document external blocker (with ETA)"

    Based on user selection:
        Execute appropriate resolution (same as Phase 6 Step 1)
        Update Implementation Notes with proper justification
```

**Step 3: Run light QA to verify fixes**

```
After resolving all deferral issues:
    Display: "Deferral issues resolved. Running light QA validation..."

    # Don't need full deep QA, just validate deferrals fixed
    Read updated Implementation Notes
    Verify all incomplete items now have valid justifications

    IF validation passes:
        Display: "Deferral issues resolved ✓ Ready for QA re-evaluation"
        Update story status remains "Dev Complete"

    ELSE:
        Display: "Some deferral issues remain. Please review."
        List remaining issues
```
```

---

### Component 3: Code-Reviewer Subagent Enhancement (1 hour)

**File:** `.claude/agents/code-reviewer.md`

**Change 3.1: Add Deferral Review to Code Review Scope**

**Location:** After line ~300 (in review checklist section)

**Implementation:**

```markdown
## Review 6: Definition of Done Completeness

**Purpose:** Early detection of deferral issues before QA

**When:** During Phase 3 (Refactor) of dev workflow

**Check Implementation Notes:**

```
Read story file > Implementation Notes > Definition of Done Status

FOR each DoD item:
    IF marked incomplete [ ]:
        Extract deferral reason

        Apply quick validation:

        ✅ Valid patterns:
        - "Deferred to STORY-{number}"
        - "Blocked by {external_system}"
        - "Out of scope: ADR-{number}"

        ❌ Invalid patterns:
        - "Will add later"
        - "Not enough time"
        - "Too complex"
        - "Optional"
        - Empty reason

        IF invalid pattern detected:
            Flag in code review report:
            "⚠️ Deferral Issue Detected: '{item}'
             Reason: '{reason}'
             Issue: Invalid deferral justification
             Will fail QA validation

             Recommended action:
             - Complete the item in refactor phase OR
             - Get user approval to defer properly (create story/ADR)"
```

**Add to code review report:**

```
## Deferral Review

**Incomplete DoD Items:** {count}

{IF issues found}
**Deferral Issues (Will Fail QA):**
1. {item}: Invalid reason '{reason}'
   Recommended: Complete now or create proper justification

{IF no issues}
**Deferral Validation:** ✓ All deferrals appear properly justified
Note: QA will perform full validation
```

**Integration in Dev Skill Phase 3:**

```
# In .claude/skills/devforgeai-development/SKILL.md, Phase 3 (Refactor)

After refactoring complete:
    Task(
        subagent_type="code-reviewer",
        prompt="Review code quality, complexity, AND deferral justifications.

                Check Implementation Notes for incomplete DoD items.
                Flag any invalid deferral reasons.

                Provide feedback before story completion."
    )

    IF code review flags deferral issues:
        Display warnings to user
        Opportunity to fix before proceeding to git workflow
```

---

### Component 4: Story-Dependency-Validator Subagent (NEW - 2 hours)

**File:** `.claude/agents/story-dependency-validator.md` (NEW)

**Purpose:** Validate story references in deferrals are real and include deferred work

**Model:** haiku (fast validation)

**System Prompt:**

```markdown
---
name: story-dependency-validator
description: Validates story references in deferrals exist and include the deferred work. Detects circular deferrals. Use during QA validation when stories have deferred DoD items.
model: haiku
allowed-tools:
  - Read
  - Glob
  - Grep
---

# Story Dependency Validator Subagent

## Purpose

Validate that deferred DoD items reference valid stories that actually include the deferred work.

## When Invoked

- By devforgeai-qa skill during Step 0b (Deferral Validation)
- When story has DoD items marked "Deferred to STORY-XXX"
- Before approving stories with deferrals

## Validation Workflow

### Input (from conversation context)

Extract from QA skill prompt:
- Referenced story ID (STORY-XXX)
- Deferred work description
- Current story ID (for circular check)

### Validation Steps

**Step 1: Verify Story Exists**

```
Glob(pattern=".ai_docs/Stories/{referenced_story_id}*.md")

IF no matches:
    Return VIOLATION:
        type: "Invalid story reference"
        severity: "HIGH"
        message: "Referenced {referenced_story_id} does not exist"
        recommendation: "Create story OR update reference to existing story"

IF multiple matches:
    Return WARNING:
        type: "Ambiguous story reference"
        message: "Multiple files match {referenced_story_id}"
        files: {list matched files}
        recommendation: "Use full story filename for clarity"
```

**Step 2: Verify Story Includes Deferred Work**

```
Read referenced story file

Search for deferred work in:
1. Acceptance Criteria: Grep for keywords from deferred item
2. Technical Specification: Grep for related terms
3. Definition of Done: Check if item appears in DoD

IF found in any section:
    Return PASS:
        message: "{referenced_story_id} includes work: '{deferred_item}'"
        location: "{section where found}"

ELSE:
    Return VIOLATION:
        type: "Referenced story doesn't include work"
        severity: "HIGH"
        message: "{referenced_story_id} has no mention of '{deferred_item}'"
        recommendation: "Update {referenced_story_id} scope OR complete work in current story"
```

**Step 3: Check for Circular Deferrals**

```
Read referenced story > Implementation Notes

IF referenced story status is "Dev Complete" or "QA Approved":
    # Story is already implemented, check what it did

    Search DoD Status for incomplete items

    FOR each incomplete item in referenced story:
        Extract deferral reason

        IF reason contains "Deferred to {current_story_id}":
            Return VIOLATION:
                type: "Circular deferral detected"
                severity: "CRITICAL"
                message: "{current_story_id} → {referenced_story_id} → {current_story_id}"
                details: "Circular deferral chain detected"
                recommendation: "One story must own this work - break the cycle"

        IF reason contains "Deferred to STORY-{other}":
            # Check indirect circular
            Read STORY-{other}
            IF STORY-{other} defers to {current_story_id}:
                Return VIOLATION:
                    type: "Indirect circular deferral"
                    severity: "CRITICAL"
                    chain: "{current_story_id} → {referenced_story_id} → STORY-{other} → {current_story_id}"
```

**Step 4: Generate Validation Report**

```
Return structured report:

{
    "referenced_story": "{story_id}",
    "validation_result": "PASS/FAIL",
    "violations": [
        {
            "type": "{violation_type}",
            "severity": "{CRITICAL/HIGH/MEDIUM}",
            "message": "{detailed_message}",
            "recommendation": "{action_to_fix}"
        }
    ],
    "story_includes_work": true/false,
    "circular_deferral_detected": true/false
}
```

## Integration Points

**Invoked by:**
- devforgeai-qa skill (Step 0b, during deferral validation)

**Returns:**
- Validation report (JSON structure)
- QA skill incorporates violations into QA report
- QA fails if CRITICAL/HIGH violations found
```

---

### Component 5: Technical-Debt-Analyzer Subagent (NEW - 2 hours)

**File:** `.claude/agents/technical-debt-analyzer.md` (NEW)

**Purpose:** Analyze accumulated technical debt from deferrals, generate reports

**Model:** sonnet (complex analysis)

**System Prompt:**

```markdown
---
name: technical-debt-analyzer
description: Analyzes accumulated technical debt from deferred DoD items. Generates debt trends, identifies oldest items, recommends debt reduction sprints. Use during sprint planning or retrospectives.
model: haiku
allowed-tools:
  - Read
  - Glob
  - Grep
  - Write
---

# Technical Debt Analyzer Subagent

## Purpose

Analyze technical debt accumulated from deferred Definition of Done items across all stories.

## When Invoked

- During sprint planning (identify debt to address)
- During sprint retrospectives (analyze deferral patterns)
- Quarterly debt reviews
- When technical-debt-register.md updates

## Analysis Workflow

### Input

Read from conversation context or default sources:
- Technical debt register: .devforgeai/technical-debt-register.md
- All story files: .ai_docs/Stories/*.story.md
- Sprint data: .ai_docs/Sprints/*.md
- Epic data: .ai_docs/Epics/*.md

### Analysis Phases

**Phase 1: Inventory Technical Debt**

```
Read technical-debt-register.md

Parse all open debt items:
FOR each debt entry:
    Extract:
        - Source story ID
        - Deferred item description
        - Deferral reason (blocker, scope change, story split)
        - Date deferred
        - Follow-up reference (STORY-XXX or ADR-XXX)
        - Priority (High/Medium/Low)
        - Status (Open/In Progress/Resolved)

    Calculate age: days_since_deferred = today - date_deferred

    Categorize by type:
        - External blockers: {count}
        - Story splits: {count}
        - Scope changes: {count}
```

**Phase 2: Analyze Debt Trends**

```
Generate statistics:

Total Debt:
- Open items: {count}
- In progress: {count}
- Resolved: {count}

By Age:
- <30 days: {count}
- 30-90 days: {count}
- >90 days: {count} ⚠️ (stale debt)

By Type:
- External blockers: {count} ({percentage}%)
- Story splits: {count} ({percentage}%)
- Scope changes: {count} ({percentage}%)

By Epic:
- EPIC-001: {count} items
- EPIC-002: {count} items

Top 5 Oldest Debt Items:
1. {item} - {age} days old - from {story_id}
2. ...
```

**Phase 3: Detect Patterns**

```
Analyze deferral patterns:

Most Common Reasons:
1. "{reason}": {count} occurrences
2. "{reason}": {count} occurrences

Stories with Most Deferrals:
1. {story_id}: {count} deferrals
2. {story_id}: {count} deferrals

Blockers by Type:
- External APIs: {count}
- Third-party services: {count}
- Infrastructure: {count}

Circular Deferrals Detected: {count}
- {story_a} ↔ {story_b}
```

**Phase 4: Generate Recommendations**

```
IF open debt >10 items:
    RECOMMEND: "Schedule debt reduction sprint"
    Suggested scope: Top 5 oldest items

IF any debt >90 days:
    WARN: "{count} stale debt items (>90 days old)"
    RECOMMEND: "Review and close or escalate"

IF circular deferrals exist:
    CRITICAL: "Circular deferrals must be resolved"
    List circular chains
    RECOMMEND: "Create integration story to break cycle"

IF pattern detected (e.g., 50% deferrals are "not enough time"):
    WARN: "Pattern detected: Story estimation issues"
    RECOMMEND: "Improve estimation process or reduce story scope"
```

**Phase 5: Generate Report**

```
Write(
    file_path=".devforgeai/technical-debt-analysis-{date}.md",
    content={comprehensive analysis report}
)

Update technical-debt-register.md with:
- Last analyzed: {date}
- Total open items: {count}
- Recommendations: {summary}
```

## Output Format

Return to orchestration skill:
- Debt count and trends
- Critical issues (stale debt, circular deferrals)
- Recommendations for sprint planning
- Report file location

## Integration Points

**Invoked by:**
- devforgeai-orchestration skill (sprint planning)
- /create-sprint command (before sprint planning)
- Manual invocation for debt reviews
```

---

### Component 6: Update `/qa` Command (1 hour)

**File:** `.claude/commands/qa.md`

**Change 6.1: Add Phase 2 - Handle QA Results**

**Location:** After Phase 1 (Invoke QA Skill) - around line 145

**Implementation:**

```markdown
### Phase 2: Handle QA Results

**Read QA report:**

```
Wait for QA skill to complete
Read QA report: .devforgeai/qa/reports/{STORY_ID}-qa-report.md
Parse report status: PASSED or FAILED
```

**IF QA PASSED:**

```
Display success summary (existing logic)
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
    {list each deferral violation}

    Required Actions:
    1. Fix deferral justifications OR
    2. Complete deferred work

    Then re-run QA validation"

    AskUserQuestion:
        Question: "How to proceed with deferral failures?"
        Header: "QA deferral failure"
        Options:
            - "Return to development (/dev will fix deferrals)"
            - "I'll fix manually, then re-run /qa"
            - "Review detailed QA report first"

    IF "Return to development":
        Display: "Run: /dev {STORY_ID}"
        Display: "Dev will read QA report and help resolve deferral issues"
        Exit command

    IF "Review detailed QA report":
        Display: "QA Report: .devforgeai/qa/reports/{STORY_ID}-qa-report.md"
        Display: "After review, run /dev {STORY_ID} to fix issues"
        Exit command

ELSE IF other QA failures (coverage, anti-patterns, etc.):
    Display standard QA failure handling (existing logic)
```

---

### Component 7: Update `/dev` Command (1 hour)

**File:** `.claude/commands/dev.md`

**Change 7.1: Add Phase 0c - Detect QA Failure Context**

**Location:** After Phase 0b (Technology Detection) - around line 147

**Implementation:**

```markdown
### Phase 0c: QA Failure Context Detection

**Check for previous QA failures:**

```
Glob(pattern=".devforgeai/qa/reports/{STORY_ID}-qa-report*.md")

IF QA report(s) found:
    Read most recent report
    Parse status: PASSED or FAILED

    IF status is FAILED:
        Parse failure type:

        IF "Deferral Validation FAILED" found in report:
            Extract deferral violations

            Display to user:
            "📋 QA Failure Context Detected

            Previous QA attempt failed due to deferral issues:

            {list deferral violations from report}

            Development will focus on resolving these issues.

            Options:
            1. Complete deferred work (implement in this story)
            2. Create proper justifications (follow-up stories, ADRs)

            The skill will guide you through resolution."

            Set mode flag:
            MODE = "deferral_resolution"
            QA_ISSUES = {list of violations}

        ELSE:
            # Other QA failures (coverage, anti-patterns)
            Display: "Previous QA failed due to: {other_issues}"
            MODE = "normal_development"

ELSE:
    # No previous QA failures
    MODE = "normal_development"
    QA_ISSUES = none
```

**Update Phase 2 (Skill Invocation) to pass context:**

```
**Context for skill:**
- Story content loaded via @file reference above
- Story ID: ${STORY_ID}
- Development Mode: ${MODE}
{IF deferral resolution mode}
- QA Failure Issues: ${QA_ISSUES}

Skill(command="devforgeai-development")
```

**The dev skill will:**
- Detect deferral_resolution mode
- Focus on fixing deferral issues (using "Handling QA Deferral Failures" section added in Component 2)
- Re-validate before completing

---

### Component 8: Update `/orchestrate` Command (1.5 hours)

**File:** `.claude/commands/orchestrate.md`

**Change 8.1: Add Phase 3.5 - QA Failure Handling with Retry**

**Location:** After Phase 3 (QA Validation) - around line 160

**Implementation:**

```markdown
### Phase 3.5: Handle QA Failure (NEW)

**IF QA validation FAILED:**

```
Read QA report to determine failure type

Grep(pattern="Deferral Validation FAILED", path=QA report)

IF deferral failures found:
    # Specific handling for deferral failures

    Extract deferral issues
    Count QA attempts from story workflow history

    IF qa_attempts >= 3:
        # Loop prevention
        Display:
        "❌ QA failed 3 times due to deferral issues

        This indicates:
        - Story scope may be too large
        - DoD items were not properly estimated
        - Systemic issues with story planning

        Halting orchestration.

        Recommended actions:
        - Split story into smaller stories
        - Review and correct DoD items
        - Escalate blockers to leadership
        - Run /dev {STORY_ID} manually to resolve"

        Exit orchestration with failure status

    ELSE:
        # Retry with dev fix

        AskUserQuestion:
            Question: "QA failed due to deferrals (attempt {qa_attempts}/3). Fix and retry?"
            Header: "QA deferral failure"
            Options:
                - "Yes - return to dev, fix deferrals, retry QA"
                - "No - stop orchestration, I'll fix manually"
                - "Create follow-up stories, skip retry"

        IF user selects "Yes":
            Display: "Returning to Phase 2 (Development) to fix deferral issues..."

            # Set context for dev skill
            Context: QA failure mode, deferral issues from report

            # Re-invoke Phase 2 (Development)
            GOTO Phase 2

            # After dev completes, automatically retry QA
            # Loop continues until QA passes or 3 attempts reached

        IF user selects "No":
            Display: "Orchestration halted. Story status: QA Failed"
            Exit with instructions to run /dev manually

        IF user selects "Create follow-up stories":
            # Use orchestration to create tracking stories

            FOR each deferred item:
                AskUserQuestion:
                    Question: "Create follow-up story for '{item}'?"
                    Options: ["Yes", "Skip this one"]

                IF "Yes":
                    Task(
                        subagent_type="requirements-analyst",
                        prompt="Create story for: '{item}'"
                    )

            Display: "Follow-up stories created. Mark original story as complete with deferrals?"
            # User decides whether to accept story as-is with justified deferrals

ELSE:
    # Other QA failures (coverage, anti-patterns)
    Display standard failure handling (existing logic)
```

**Add retry loop tracking:**

```
Track in story workflow history:
- QA attempt count
- Failure reasons per attempt
- Resolution actions taken
- Final outcome
```

---

### Component 9: Quality Gate Definition Update (30 min)

**File:** `.claude/skills/devforgeai-orchestration/references/quality-gates.md`

**Change 9.1: Update Gate 3 - QA Approval Gate**

**Location:** Line ~528 (Gate 3 definition)

**Add to Gate 3 passing criteria:**

```markdown
### Gate 3: QA Approval

**Blocking Conditions (UPDATED):**

**CRITICAL Violations (Must Fix):**
- Coverage below thresholds
- Layer violations
- Library substitution
- Circular deferrals ← NEW
- Security vulnerabilities (OWASP Top 10)

**HIGH Violations (Must Fix or Document Exception):**
- Anti-pattern violations
- Missing acceptance criteria tests
- Architecture constraint violations
- Unjustified deferrals (no valid reason) ← NEW
- Invalid story references in deferrals ← NEW
- Implementation feasible but deferred unnecessarily ← NEW

**MEDIUM Violations (Document Exception or Fix):**
- Code complexity >10
- Documentation coverage <80%
- Scope change without ADR ← NEW

**Completeness Criteria (NEW):**

✅ **All DoD items complete OR**
✅ **All incomplete DoD items have VALID justification:**
- Technical blocker documented with ETA
- Scope change with ADR reference (ADR-XXX exists)
- Story split with follow-up story (STORY-XXX exists and includes work)
- External dependency with tracking

**Deferral Validation Requirements (NEW):**
- [ ] All story references exist (Glob validation)
- [ ] Referenced stories include deferred work (content validation)
- [ ] No circular deferrals detected (chain analysis)
- [ ] All scope changes have ADR documentation
- [ ] All external blockers have ETA or condition
- [ ] Technical debt register updated for all deferrals
```

---

### Component 10: Orchestration Skill Enhancement (2 hours)

**File:** `.claude/skills/devforgeai-orchestration/SKILL.md`

**Change 10.1: Add Phase 5 - Deferred Work Tracking**

**Location:** Add new phase after existing workflow phases

**Implementation:**

```markdown
## Phase 5: Deferred Work Tracking (NEW)

**Purpose:** Ensure deferred DoD items are tracked and not lost

**Triggered when:**
- Story reaches "Dev Complete" status
- Implementation Notes contain deferred items
- Before QA validation begins

**Workflow:**

**Step 1: Scan for Deferrals**

```
Read story > Implementation Notes > Definition of Done Status

Extract all items marked [ ] (incomplete)
Count deferrals by type:
- Story splits: {count}
- Scope changes: {count}
- External blockers: {count}
```

**Step 2: Validate Deferral Tracking**

```
FOR each deferral:
    reason_type = parse_deferral_type(reason)

    IF reason_type == "story_split":
        referenced_story = extract_story_id(reason)

        Glob(pattern=".ai_docs/Stories/{referenced_story}*.md")

        IF not found:
            WARN: "Referenced {referenced_story} not found"

            AskUserQuestion:
                Question: "Deferral references {referenced_story} but story doesn't exist. Create it?"
                Options:
                    - "Yes - create tracking story now"
                    - "No - I'll create it manually"
                    - "Fix reference (I meant different story)"

            IF "Yes":
                Task(
                    subagent_type="requirements-analyst",
                    prompt="Create story {referenced_story} for deferred work: '{item}'"
                )

    ELSE IF reason_type == "scope_change":
        adr_reference = extract_adr_id(reason)

        Glob(pattern=".devforgeai/adrs/{adr_reference}*.md")

        IF not found:
            WARN: "Referenced {adr_reference} not found"

            AskUserQuestion:
                Question: "Deferral references {adr_reference} but ADR doesn't exist. Create it?"
                Options:
                    - "Yes - document scope change in ADR"
                    - "No - I'll create it manually"
                    - "Change justification (not scope change)"

            IF "Yes":
                Task(
                    subagent_type="architect-reviewer",
                    prompt="Create {adr_reference} documenting scope change for: '{item}'"
                )

    ELSE IF reason_type == "external_blocker":
        # Log to technical debt register
        Ensure entry exists in .devforgeai/technical-debt-register.md
```

**Step 3: Update Technical Debt Register**

```
Read or create: .devforgeai/technical-debt-register.md

FOR each deferral:
    Check if already logged

    IF not logged:
        Append entry:

        ---
        ## {STORY_ID}: {deferred_item_description}

        **Date Deferred:** {date}
        **Type:** {story_split/scope_change/external_blocker}
        **Justification:** {deferral_reason}
        **Follow-up:** {STORY-XXX or ADR-XXX or Blocker condition}
        **Priority:** {High/Medium/Low based on item criticality}
        **Status:** Open
        **Resolution Target:** {Sprint X or date if known}
        ---
```

**Step 4: Analyze Debt Trends (Periodic)**

```
IF invoked during sprint planning OR retrospective:
    Task(
        subagent_type="technical-debt-analyzer",
        prompt="Analyze current technical debt from deferrals.

                Generate trends, identify oldest items, recommend actions.

                Focus on:
                - Items >90 days old
                - Circular deferrals
                - Pattern detection

                Provide recommendations for upcoming sprint."
    )

    Display debt analysis summary to user
    Recommend debt reduction if debt count >10
```

---

### Component 11: Update `/dev` Command (1 hour)

**Location:** `.claude/commands/dev.md`

**Changes documented in Component 7 above**

Plus ensure skill invocation passes QA failure context:

```markdown
**Context for skill:**
- Story content loaded via @file reference above
- Story ID: ${STORY_ID}
- Development Mode: ${MODE} (normal OR deferral_resolution)
{IF QA failure context exists}
- QA Deferral Issues: ${QA_ISSUES}
```

---

### Component 12: Update `/orchestrate` Command (1.5 hours)

**Location:** `.claude/commands/orchestrate.md`

**Changes documented in Component 8 above**

Add complete feedback loop: Dev → QA FAIL → Dev fix → QA retry (max 3 attempts)

---

### Component 13: New Subagent - Deferral-Validator (4 hours)

**File:** `.claude/agents/deferral-validator.md` (NEW)

**Purpose:** Automated validation of all deferral justifications before QA approval

**Model:** haiku (fast, cost-effective for validation)

**Complete Specification (from RCA-qa-process-failure lines 814-911):**

```markdown
---
name: deferral-validator
description: Validates that deferred Definition of Done items have justified technical reasons and proper documentation. Detects circular deferrals, validates story/ADR references, checks implementation feasibility. Use during QA validation when stories have deferred DoD items.
model: haiku
allowed-tools:
  - Read
  - Glob
  - Grep
---

# Deferral Validator Subagent

## Purpose

Validate all deferred Definition of Done items in a story to ensure:
1. Technical blockers are documented and verified
2. No unnecessary deferrals (work could be done now)
3. Scope changes have ADR documentation
4. No circular deferral chains
5. Referenced stories exist and include deferred work

## When to Invoke

**Invoked by:**
- devforgeai-development skill (Phase 6, Step 1.5 - before git commit)
- devforgeai-qa skill (Phase 0, Step 3 - during deferral validation)

**Trigger Condition:**
- Story has ANY DoD items marked [ ] (incomplete)

## Input (from conversation context)

Extract from loaded story file:
- Story ID (from YAML frontmatter)
- Definition of Done section
- Technical Specification section
- Implementation Notes (for context)

## Validation Workflow

### Substep 1: Extract Deferral Information

Parse DoD Status section:
```
FOR each item marked [ ]:
    Extract:
        - ITEM = Item description
        - REASON = Deferral reason/justification
        - STORY_REF = Referenced story ID (if "Deferred to STORY-XXX")
        - ADR_REF = Referenced ADR (if "Out of scope: ADR-XXX")
```

### Substep 2: Validate Deferral Type

Check reason matches valid patterns:

Valid formats:
- "Blocked by {external_system}: {specific_reason}"
- "Deferred to STORY-XXX: {justification}"
- "Out of scope: ADR-XXX"
- "User approved via AskUserQuestion: {context}"

Invalid formats:
- "Will add later" ❌
- "Not enough time" ❌
- "Too complex" ❌
- "Deferred" (no details) ❌
- Empty reason ❌

IF invalid format:
```
VIOLATION:
    type: "Invalid deferral reason format"
    severity: "MEDIUM"
    item: {ITEM}
    reason: {REASON}
    message: "Reason must specify: blocker, target story, or ADR"
    remediation: "Use format: 'Deferred to STORY-XXX: {reason}'"
```

### Substep 3: Validate Technical Blocker (If Claimed)

IF reason contains "Blocked by":
```
Extract blocker: {BLOCKER_NAME}

Validate blocker is external:
    Internal indicators: "our code", "our API", "our module", "internal"
    External indicators: "API v2", "third-party", "platform", "service"

IF blocker appears internal:
    VIOLATION:
        type: "Internal blocker (not valid)"
        severity: "HIGH"
        message: "Blocker '{BLOCKER_NAME}' appears to be internal code/decision"
        remediation: "Internal blockers should be resolved in story. Only external dependencies are valid blockers."

Validate blocker has resolution condition:
    Look for: "available {date}", "when {condition}", "ETA: {date}"

IF no resolution condition:
    VIOLATION:
        type: "Blocker missing resolution condition"
        severity: "MEDIUM"
        message: "External blocker must include ETA or condition for resolution"
```

### Substep 4: Check Implementation Feasibility

Read Technical Specification section:
```
Search spec for code patterns related to {ITEM}

Feasibility indicators:
1. Code pattern provided? (search for code blocks, examples)
2. Estimated size mentioned? (look for "15 lines", "simple", etc.)
3. Dependencies available? (check tech-stack.md, dependencies.md)

IF ALL true (feasible now):
    AND no technical blocker documented:
    VIOLATION:
        type: "Unnecessary deferral - implementation feasible"
        severity: "HIGH"
        item: {ITEM}
        evidence:
            - "Code pattern found in spec at lines {X-Y}"
            - "Estimated: ~{N} lines"
            - "Dependencies: All available"
        message: "This item could be implemented NOW"
        remediation: "Complete in current story OR create proper justification (ADR for scope change)"
```

### Substep 5: Check for ADR Requirement

IF deferral doesn't reference ADR:
```
AND item appears in original DoD (in scope):
AND no technical blocker documented:

THEN:
    VIOLATION:
        type: "Scope change without ADR"
        severity: "MEDIUM"
        item: {ITEM}
        message: "Deferring in-scope DoD item requires ADR documentation"
        justification: "Item was in Definition of Done (in scope), removing it is a scope change"
        remediation: "Create ADR-XXX documenting why work moved to future story"
```

IF deferral references ADR:
```
Glob(pattern=".devforgeai/adrs/{ADR_REF}*.md")

IF not found:
    VIOLATION:
        type: "ADR reference not found"
        severity: "HIGH"
        message: "Referenced {ADR_REF} does not exist"
        remediation: "Create ADR OR update deferral reference"

ELSE:
    Read ADR file
    Search for {ITEM} keywords

    IF ADR doesn't mention this item:
        VIOLATION:
            type: "ADR doesn't document this deferral"
            severity: "MEDIUM"
            message: "{ADR_REF} doesn't describe deferral of '{ITEM}'"
```

### Substep 6: Detect Circular Deferrals

IF reason contains "Deferred to STORY-{XXX}":
```
1. Check story exists:
   Glob(pattern=".ai_docs/Stories/STORY-{XXX}*.md")

   IF not found:
       VIOLATION:
           type: "Invalid story reference"
           severity: "HIGH"
           message: "Referenced STORY-{XXX} does not exist"

2. Read referenced story:
   Check story status

   IF status is "Dev Complete" or "QA Approved":
       # Story already implemented, check what happened
       Read Implementation Notes > DoD Status

       Search for incomplete items

       FOR each incomplete item in referenced story:
           IF reason contains "Deferred to {current_story_id}":
               VIOLATION:
                   type: "Circular deferral detected"
                   severity: "CRITICAL"
                   chain: "{current_story_id} → STORY-{XXX} → {current_story_id}"
                   message: "Circular deferral chain detected"
                   remediation: "One story must own this work - break the cycle by implementing in one story"

3. Check if referenced story includes work:
   Search acceptance criteria for {ITEM} keywords
   Search technical spec for {ITEM} keywords

   IF not found anywhere:
       VIOLATION:
           type: "Referenced story doesn't include work"
           severity: "HIGH"
           message: "STORY-{XXX} has no mention of '{ITEM}' in scope"
           remediation: "Update STORY-{XXX} OR complete work in current story"
```

### Substep 7: Generate Validation Report

Return structured JSON:
```json
{
    "story_id": "STORY-XXX",
    "total_deferred": 2,
    "validation_results": [
        {
            "item": "Exit code 0 for success, 2 for error",
            "reason": "Deferred to STORY-005: Exit code handling will be in error framework story",
            "violations": [
                {
                    "type": "Unnecessary deferral",
                    "severity": "HIGH",
                    "message": "Implementation feasible NOW (15 lines, no blockers)",
                    "evidence": {
                        "code_pattern": "lines 270-300 in spec",
                        "estimated_lines": 15,
                        "dependencies_met": true,
                        "blocker_documented": false
                    },
                    "remediation": "Complete in current story OR create ADR for scope change"
                },
                {
                    "type": "Scope change without ADR",
                    "severity": "MEDIUM",
                    "message": "DoD item deferred but no ADR documenting scope change"
                },
                {
                    "type": "Circular deferral risk",
                    "severity": "CRITICAL",
                    "message": "STORY-005 also defers this work",
                    "chain": "STORY-004 → STORY-005 → STORY-004"
                }
            ]
        }
    ],
    "summary": {
        "critical_violations": 1,
        "high_violations": 2,
        "medium_violations": 1,
        "low_violations": 0,
        "recommendation": "FAIL - Fix violations before approval"
    }
}
```

## Integration

**In devforgeai-development skill (Phase 6, Step 1.5 - NEW):**
```markdown
After updating Implementation Notes with DoD status:

IF any DoD items marked [ ] (incomplete):
    Task(
        subagent_type="deferral-validator",
        description="Validate deferral justifications",
        prompt="Validate all deferred Definition of Done items.

                Story already loaded in conversation.

                Check for:
                - Valid deferral reasons
                - Technical blockers documented
                - ADR for scope changes
                - Circular deferrals
                - Referenced stories exist and include work

                Return JSON validation report."
    )

    IF validation returns CRITICAL or HIGH violations:
        HALT development
        Display violations to user
        User must fix before proceeding to git commit
```

**In devforgeai-qa skill (Phase 0, Step 3 - NEW):**
```markdown
After validating test results:

Read Implementation Notes > Definition of Done Status

IF any incomplete items found:
    Task(
        subagent_type="deferral-validator",
        description="Validate deferral justifications for QA",
        prompt="Validate all deferred DoD items for QA approval.

                Story loaded in conversation.

                Perform comprehensive validation:
                - Technical blocker verification
                - Implementation feasibility check
                - ADR requirement for scope changes
                - Circular deferral detection
                - Referenced story validation

                Return JSON validation report."
    )

    Parse validation results

    IF CRITICAL or HIGH violations:
        Add to QA report violations section
        QA Status: FAILED
        Story status: QA Failed
        HALT QA approval
```
```

**CRITICAL: This subagent MUST be created and invoked - it's the enforcement mechanism!**

---

### Component 14: Story-Dependency-Validator → RENAMED to Deferral-Validator

**Note:** The Plan agent identified that story-dependency-validator should actually be the more comprehensive deferral-validator subagent documented above in Component 13.

**Action:** Remove Component 14 as separate entity, consolidate into Component 13 (deferral-validator).

---

### Component 14: New Subagent - Technical-Debt-Analyzer (2 hours)

**File:** `.claude/agents/technical-debt-analyzer.md` (NEW)

**Details:** Documented in Component 5 above

**CRITICAL: Must be invoked explicitly in orchestration skill Phase 5**

---

### Component 15: Templates & Documentation (1.5 hours)

**15.1: ADR Template for Scope Descoping**

**File:** `.claude/skills/devforgeai-architecture/assets/adr-examples/ADR-EXAMPLE-004-scope-descope.md` (NEW)

**Content:**
- Template for documenting scope changes
- Sections: Context, Decision, Rationale, Consequences, Alternatives
- Example from STORY-004 exit code deferral

**15.2: Technical Debt Register Template**

**File:** `.devforgeai/technical-debt-register.md` (NEW)

**Content:**
- Header explaining purpose
- Template for debt entries
- Status tracking (Open/In Progress/Resolved)
- Analysis section (last analyzed date, trends)

**15.3: Update Reference Documentation**

**Files:**
- `.claude/memory/skills-reference.md` - Add deferral validation notes
- `.claude/memory/subagents-reference.md` - Add 2 new subagents
- `.claude/memory/commands-reference.md` - Document QA failure handling

---

### Component 16: Create RCA-006 Document (1.5 hours)

**File:** `.devforgeai/specs/enhancements/RCA-006-deferral-validation-quality-gate-failure.md` (NEW)

**Content:**
- Problem statement (from STORY-004/005 evidence)
- 5 Whys analysis for both dev and QA failures
- Evidence from tmp/output.md, QA reports, Claude's RCAs
- Complete solution documentation
- Testing requirements
- Prevention strategies

---

## Summary: What Gets Updated and Why

### Skills (3 files)
1. **devforgeai-development** - AskUserQuestion for deferrals, QA failure handling
2. **devforgeai-qa** - Deferral validation logic, QA iteration tracking
3. **devforgeai-orchestration** - Deferred work tracking, debt analysis invocation

### Commands (3 files)
4. **dev.md** - QA failure context detection, pass issues to skill
5. **qa.md** - Handle QA failures, guide user to resolution
6. **orchestrate.md** - Retry loop for QA failures (max 3 attempts)

### Subagents Enhanced (1 file)
7. **code-reviewer.md** - Add deferral review during refactor phase

### Subagents Created (2 files)
8. **story-dependency-validator.md** - Validate story references in deferrals
9. **technical-debt-analyzer.md** - Analyze debt trends, generate reports

### Reference Files (1 file)
10. **quality-gates.md** - Add deferral validation to Gate 3

### Templates (2 files)
11. **ADR-EXAMPLE-004-scope-descope.md** - Scope change ADR template
12. **technical-debt-register.md** - Debt tracking template

### Documentation (3 files)
13. **skills-reference.md** - Document deferral validation
14. **subagents-reference.md** - Add 2 new subagents
15. **commands-reference.md** - Document QA failure handling

### RCA (1 file)
16. **RCA-006-deferral-validation-quality-gate-failure.md** - Complete RCA

---

## Critical: Subagent Invocation Points (No Silos!)

**User's Key Insight:** Subagents only run if explicitly invoked via Task tool

**Invocation Map:**

1. **story-dependency-validator** ← Invoked by QA skill Step 0b
2. **technical-debt-analyzer** ← Invoked by orchestration skill Phase 5
3. **code-reviewer** ← Already invoked by dev skill Phase 3 (ENHANCE to include deferrals)
4. **requirements-analyst** ← Invoked by dev skill when creating deferral tracking stories
5. **architect-reviewer** ← Invoked by dev skill when creating scope change ADRs

**All subagents explicitly called - no orphaned components!**

---

## Testing Requirements

1. Test invalid deferral (QA should fail)
2. Test valid deferral with story split (QA should pass, story should exist)
3. Test circular deferral (QA should fail with CRITICAL)
4. Test QA failure → dev fix → QA retry loop
5. Test 3-attempt limit in orchestration
6. Test technical debt analyzer generates correct reports

---

## Review Findings (From Plan Agent Analysis)

**Gaps Found and Addressed:**

1. ✅ **Deferral-validator subagent specification** - Added complete 815-line spec from RCA
2. ✅ **5-step decision tree for dev skill** - Referenced from RCA-exit-code-deferral
3. ✅ **7-substep validation for QA skill** - Referenced from RCA-qa-process-failure
4. ✅ **Explicit invocation points** - Dev Phase 6 Step 1.5, QA Phase 0 Step 3
5. ✅ **Quality gate blocking conditions** - Updated with deferral violations
6. ✅ **User's critical insight** - All subagents explicitly invoked (no silos)

**Evidence Incorporated:**
- STORY-004/005 QA reports analyzed
- Circular deferral patterns from tmp/output.md
- Complete RCA specifications included
- User's ADR requirement addressed

---

## Estimated Effort: ~18 hours total (REVISED)

**Breakdown:**
- Skills: 8.5 hours (dev: 3h, qa: 4h, orchestration: 1.5h)
- Commands: 3.5 hours (dev: 1h, qa: 1h, orchestrate: 1.5h)
- Subagents: 7 hours (deferral-validator: 4h, tech-debt-analyzer: 2h, code-reviewer: 1h)
- Templates + Docs: 3 hours
- RCA Document: 1.5 hours
- STORY-0XX Creation: 0.5 hours

**Total: 17 files modified/created**

---

## Final Component Checklist

**Skills (3):**
- [ ] devforgeai-development - AskUserQuestion for all deferrals, 5-step decision tree, QA failure handling
- [ ] devforgeai-qa - 7-substep deferral validation, QA iteration tracking, invoke deferral-validator
- [ ] devforgeai-orchestration - Phase 5 deferred work tracking, invoke tech-debt-analyzer

**Commands (3):**
- [ ] /dev - Phase 0c QA failure detection, pass context to skill
- [ ] /qa - Phase 2 handle QA results, guide to resolution
- [ ] /orchestrate - Phase 3.5 QA failure retry loop (max 3 attempts)

**Subagents (3):**
- [ ] deferral-validator (NEW) - Complete validation logic with JSON output
- [ ] technical-debt-analyzer (NEW) - Debt trend analysis and reporting
- [ ] code-reviewer (ENHANCE) - Add deferral review in refactor phase

**Quality Gates (1):**
- [ ] quality-gates.md - Add deferral blocking conditions to Gate 3

**Templates (2):**
- [ ] ADR-EXAMPLE-004-scope-descope.md - Template for scope change ADRs
- [ ] technical-debt-register.md - Debt tracking template

**Documentation (3):**
- [ ] skills-reference.md - Document deferral validation
- [ ] subagents-reference.md - Add 2 new subagents
- [ ] commands-reference.md - Document QA failure handling

**Stories (1):**
- [ ] STORY-0XX-integrate-error-handling-main.md - Closes circular deferral gap

**RCA (1):**
- [ ] RCA-006-deferral-validation-quality-gate-failure.md - Complete analysis

---

## Success Criteria (FINAL)

**Functional:**
- [ ] QA fails stories with unjustified deferrals
- [ ] Dev uses AskUserQuestion for all deferrals
- [ ] Feedback loop works: Dev → QA FAIL → Dev fix → QA retry
- [ ] Circular deferrals detected and blocked (CRITICAL)
- [ ] All deferrals have follow-up tracking (story or ADR)
- [ ] Technical debt register updated automatically

**Quality:**
- [ ] Deferral rate <10% (from ~20%)
- [ ] Invalid deferrals: 0 (blocked at dev or QA)
- [ ] QA escape rate <1% (from ~20%)
- [ ] All scope changes have ADRs

**User Experience:**
- [ ] Clear guidance on when/how to defer
- [ ] Helpful error messages for invalid deferrals
- [ ] Automated story creation for valid deferrals
- [ ] Complete audit trail maintained

---

## PLAN STATUS: READY FOR USER REVIEW

All evidence files reviewed, gaps identified and addressed, complete specifications included.