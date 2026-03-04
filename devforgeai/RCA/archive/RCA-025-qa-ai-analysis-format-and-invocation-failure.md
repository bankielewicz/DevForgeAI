# RCA-025: QA AI Analysis Format and Invocation Failure

**Date:** 2026-01-11
**Reported By:** User
**Affected Component:** devforgeai-qa skill (Phase 4), devforgeai-feedback skill, CLAUDE.md
**Severity:** HIGH
**Story Context:** STORY-200 (Add Telemetry for Hook Performance Metrics)

---

## Issue Description

During STORY-200 `/qa deep` workflow execution, Claude made two errors related to AI architectural analysis capture:

1. **Wrong Format:** Created markdown file (`qa-deep-analysis.md`) instead of the JSON format specified in devforgeai-feedback SKILL.md (lines 124-143)
2. **Skipped Skill Invocation:** Did not invoke devforgeai-feedback skill until user explicitly pointed out the oversight by pasting CLAUDE.md excerpt

**Expected Behavior:**
- Read devforgeai-feedback SKILL.md to understand output requirements
- Create JSON file per schema: `{STORY_ID}/{timestamp}-qa-analysis.json`
- Invoke feedback skill for proper capture and indexing
- Update index.json and recommendations-queue.json

**Actual Behavior:**
- Created markdown file (qa-deep-analysis.md)
- Added "AI Commentary" section to story file (partial compliance)
- Did not invoke feedback skill
- User had to explicitly prompt for correct behavior
- Only after user intervention was JSON file created

**Impact:**
- Initial feedback capture in wrong format (markdown not JSON)
- Feedback skill not invoked (indexing incomplete)
- User had to intervene to fix
- Pattern from RCA-024 (/dev workflow) repeated in /qa workflow

---

## 5 Whys Analysis

**Issue:** Claude created markdown AI analysis file and skipped feedback skill invocation during QA workflow

**Why #1:** Why did Claude create a markdown file instead of JSON?

**Answer:** Claude relied on prior "AI Commentary" patterns from story templates rather than reading the devforgeai-feedback skill's explicit JSON schema requirements (SKILL.md lines 124-143).

**Evidence:**
- Created: `qa-deep-analysis.md` (markdown)
- Required: `{timestamp}-qa-analysis.json` (JSON)
- devforgeai-feedback SKILL.md lines 124-143 shows JSON schema

---

**Why #2:** Why did Claude rely on patterns instead of reading skill requirements?

**Answer:** The devforgeai-qa skill's Phase 4 (Cleanup) references feedback hooks but doesn't explicitly instruct to read devforgeai-feedback SKILL.md for output format requirements.

**Evidence:**
- devforgeai-qa SKILL.md Phase 4.2: References feedback-hooks-workflow.md
- No instruction: "Read devforgeai-feedback SKILL.md for output format"
- Missing: Explicit step for AI analysis capture in QA workflow

---

**Why #3:** Why did Claude not invoke the feedback skill until user pointed it out?

**Answer:** Claude treated the "AI Commentary" story file addition as complete feedback capture, not recognizing that feedback skill invocation and JSON storage were separate, mandatory requirements.

**Evidence:**
- CLAUDE.md line 312: Shows manual trigger but as "if needed"
- Claude's action: Added commentary to story, displayed in response
- Missing: Skill(command="devforgeai-feedback") invocation
- User intervention required to trigger correct behavior

---

**Why #4:** Why didn't Claude recognize feedback skill invocation as mandatory?

**Answer:** CLAUDE.md uses conditional language ("Manual trigger if needed") which Claude interpreted as optional, and QA skill Phase 4 has no explicit "Invoke feedback skill" step.

**Evidence:**
- CLAUDE.md line 310: "**Manual trigger (if needed):**" - conditional
- devforgeai-qa SKILL.md Phase 4: No feedback skill invocation step
- Same pattern as RCA-024: mandatory action with non-mandatory enforcement

---

**Why #5 (ROOT CAUSE):** Why is feedback skill invocation conditional/optional when it should be mandatory?

**Answer:** **ROOT CAUSE:** The framework has inconsistent enforcement across two documentation sources:

1. **CLAUDE.md** uses conditional language ("if needed") suggesting optional behavior
2. **devforgeai-feedback SKILL.md** shows mandatory JSON format but isn't referenced by QA skill
3. **devforgeai-qa SKILL.md** Phase 4 lacks explicit feedback skill invocation step

This **documentation enforcement gap** allows Claude to take shortcuts (markdown vs JSON, skip invocation) because requirements exist but are scattered and use permissive language.

**Evidence:**
- CLAUDE.md: "if needed" (conditional)
- Feedback skill: JSON schema (mandatory format)
- QA skill: Missing invocation step
- RCA-024: Same root pattern identified 2 hours earlier

---

## Evidence Collected

### File 1: CLAUDE.md (lines 287-315)

**Finding:** AI analysis requirements documented but with conditional language

**Excerpt:**
```markdown
## AI Architectural Analysis (Automatic)

After `/dev` and `/qa` workflows complete, AI architectural analysis is **automatically captured** via hooks:

**Hooks:** `post-dev-ai-analysis`, `post-qa-ai-analysis`

**Storage:** `devforgeai/feedback/ai-analysis/{STORY_ID}/`

**Manual trigger (if needed):**
Skill(command="devforgeai-feedback", args="--type=ai_analysis")
```

**Significance:** CRITICAL - Says "automatically captured" but hooks may not be configured. "If needed" language makes manual trigger seem optional.

---

### File 2: devforgeai-feedback SKILL.md (lines 101-143)

**Finding:** Explicit JSON schema requirement that was ignored

**Excerpt:**
```markdown
### 5. AI Architectural Analysis (NEW)

**Output Structure:**
{
  "ai_analysis": {
    "what_worked_well": ["..."],
    "areas_for_improvement": ["..."],
    "recommendations": [
      {
        "description": "...",
        "affected_files": ["..."],
        "implementation_notes": "...",
        "priority": "medium",
        "feasible_in_claude_code": true
      }
    ],
    "patterns_observed": ["..."],
    "anti_patterns_detected": ["..."],
    "constraint_analysis": "..."
  }
}
```

**Significance:** CRITICAL - Clear JSON format requirement exists but Claude didn't read this before creating markdown file.

---

### File 3: devforgeai-qa SKILL.md (Phase 4)

**Finding:** Phase 4 (Cleanup) references feedback hooks but has no explicit feedback skill invocation step

**Excerpt:**
```markdown
### Step 4.2: Invoke Feedback Hooks

**Reference:** `references/feedback-hooks-workflow.md`

# Map QA result to hook status
IF overall_status == "PASSED": STATUS = "success"
...
Bash(command="devforgeai-validate invoke-hooks --operation=qa --story=$STORY_ID")
```

**Significance:** HIGH - Step 4.2 invokes hooks via Bash but doesn't invoke the feedback skill directly. No Step 4.3 for AI analysis capture.

---

### File 4: RCA-024 (Related)

**Finding:** Same pattern identified 2 hours earlier in /dev workflow

**Relationship:**
- RCA-024: /dev workflow Phase 9 feedback storage skipped
- RCA-025: /qa workflow Phase 4 feedback skill not invoked
- Same root cause: Mandatory action with non-mandatory enforcement

**Pattern Recurrence:** 2 hours between RCA-024 and RCA-025 - same issue in different contexts

---

## Recommendations

### CRITICAL Priority (Implement Immediately)

**REC-1: Add Explicit AI Analysis Step to QA Skill Phase 4**

**Problem:** QA skill Phase 4 lacks explicit step for AI analysis capture with format requirements.

**File:** `.claude/skills/devforgeai-qa/SKILL.md`
**Section:** Phase 4, after Step 4.2

**Implementation:**

Add new Step 4.3:
```markdown
### Step 4.3: Capture AI Architectural Analysis (MANDATORY - Deep Mode)

**Purpose:** Generate and persist AI analysis per framework requirements.

IF mode == "deep":
    # Step 4.3.1: Read feedback skill schema
    Read(file_path=".claude/skills/devforgeai-feedback/SKILL.md")
    # Focus: Lines 101-143 (JSON schema)

    # Step 4.3.2: Generate JSON (NOT markdown)
    ai_analysis = {
        "metadata": {
            "story_id": "${STORY_ID}",
            "workflow": "qa",
            "mode": "deep",
            "timestamp": "${ISO_8601}",
            "author": "claude/opus",
            "hook": "post-qa-ai-analysis"
        },
        "ai_analysis": {
            "what_worked_well": [...],
            "areas_for_improvement": [...],
            "recommendations": [
                {
                    "id": "R1",
                    "description": "...",
                    "affected_files": [...],
                    "implementation_notes": "...",
                    "priority": "high|medium|low",
                    "effort": "low|medium|high",
                    "feasible_in_claude_code": true|false
                }
            ],
            "patterns_observed": [...],
            "anti_patterns_detected": [...],
            "constraint_analysis": {...}
        },
        "rca_assessment": {
            "rca_required": true|false,
            "rationale": "..."
        },
        "follow_up_stories": [...]
    }

    # Step 4.3.3: Write JSON file
    Write(
        file_path="devforgeai/feedback/ai-analysis/{STORY_ID}/{timestamp}-qa-analysis.json",
        content=JSON.stringify(ai_analysis, indent=2)
    )

    # Step 4.3.4: Verify write succeeded (BLOCKING)
    Read(file_path="devforgeai/feedback/ai-analysis/{STORY_ID}/{timestamp}-qa-analysis.json")
    IF read fails:
        HALT: "AI analysis storage failed - verify permissions and retry"

    # Step 4.3.5: Update index.json
    Read(file_path="devforgeai/feedback/ai-analysis/index.json")
    # Append new session entry
    # Update aggregated counts
    Write(file_path="devforgeai/feedback/ai-analysis/index.json", content=updated_index)

    Display: "✓ AI Analysis: {STORY_ID}/{timestamp}-qa-analysis.json"

ELSE:
    Display: "ℹ️ Light mode - AI analysis skipped"
```

**Rationale:**
1. Makes AI analysis capture explicit in QA workflow
2. Forces reading feedback skill schema before writing
3. Specifies JSON format (not markdown)
4. Includes blocking verification
5. Updates index for discoverability

**Testing:**
1. Run `/qa STORY-XXX deep`
2. Verify Step 4.3 executes after Step 4.2
3. Verify JSON file created (not markdown)
4. Verify index.json updated
5. Verify content matches schema

**Effort:** 30 minutes

---

### HIGH Priority (Implement This Sprint)

**REC-2: Change CLAUDE.md Language from Conditional to Mandatory**

**Problem:** "Manual trigger (if needed)" language interpreted as optional.

**File:** `CLAUDE.md`
**Section:** Lines 310-315

**Current:**
```markdown
**Manual trigger (if needed):**
Skill(command="devforgeai-feedback", args="--type=ai_analysis")
```

**Change to:**
```markdown
**Post-Workflow Requirement (MANDATORY if hooks don't auto-trigger):**

After /dev or /qa deep workflows, ALWAYS verify AI analysis was captured:

1. Check: `devforgeai/feedback/ai-analysis/{STORY_ID}/` exists
2. Verify: Contains `*-qa-analysis.json` or `*-ai-analysis.json` file
3. If missing: Invoke `Skill(command="devforgeai-feedback", args="--type=ai_analysis")`

**CRITICAL:** Output MUST be JSON format per devforgeai-feedback SKILL.md schema (lines 124-143)
**NOT ALLOWED:** Markdown files (.md) in ai-analysis directory
```

**Rationale:**
- Removes conditional language ("if needed")
- Adds explicit verification requirement
- Specifies JSON-only format
- References skill schema

**Effort:** 15 minutes

---

### MEDIUM Priority (Next Sprint)

**REC-3: Add Format Validation Before AI Analysis Write**

**Problem:** No validation prevents writing wrong format (markdown vs JSON).

**File:** `.claude/skills/devforgeai-feedback/SKILL.md`
**Section:** After AI Analysis section

**Add:**
```markdown
### AI Analysis Format Validation (BLOCKING)

Before writing to `devforgeai/feedback/ai-analysis/`:

**Filename Validation:**
IF file_extension != ".json":
    HALT: "Invalid format: {filename}"
    Display: "AI analysis MUST be JSON (.json), not {extension}"
    Display: "See lines 124-143 for required schema"

**Content Validation:**
IF content missing "ai_analysis" key:
    HALT: "Invalid JSON structure"
    Display: "Required: { 'ai_analysis': { 'what_worked_well': [...], ... } }"

IF content missing "recommendations" array:
    HALT: "Missing recommendations array"

IF any recommendation missing "feasible_in_claude_code" flag:
    HALT: "Recommendation missing feasibility flag"
```

**Rationale:** Catches format errors before persistence. Provides actionable error messages.

**Effort:** 20 minutes

---

### LOW Priority (Backlog)

**REC-4: Add Cross-Skill Reference Pattern Documentation**

**Problem:** Skills don't consistently reference other skills they depend on.

**File:** `.claude/memory/skills-reference.md` (or new file)

**Add:**
```markdown
## Cross-Skill Dependencies

When a skill depends on another skill's output format:

1. **Explicit Read:** Include `Read(file_path="...SKILL.md")` instruction
2. **Schema Reference:** Cite exact lines for format requirements
3. **Format Validation:** Add validation before write operations

**Example Pattern:**
# In skill that needs feedback format
Read(file_path=".claude/skills/devforgeai-feedback/SKILL.md")
# See lines 124-143 for JSON schema
```

**Effort:** 15 minutes

---

## Implementation Checklist

- [ ] Implement REC-1 (CRITICAL)
  - [ ] Add Step 4.3 to devforgeai-qa SKILL.md
  - [ ] Include schema read instruction
  - [ ] Specify JSON format explicitly
  - [ ] Add blocking verification
  - [ ] Test with `/qa STORY-XXX deep`

- [ ] Implement REC-2 (HIGH)
  - [ ] Update CLAUDE.md lines 310-315
  - [ ] Change "if needed" to "MANDATORY"
  - [ ] Add format specification

- [ ] Consider REC-3 (MEDIUM)
  - [ ] Add format validation to feedback skill
  - [ ] Test with wrong format

- [ ] Add REC-4 (LOW) to documentation backlog

- [ ] Mark RCA-025 as RESOLVED after verification
- [ ] Commit with reference to RCA-025

---

## Prevention Strategy

**Short-term:**
1. Add Step 4.3 to QA skill (REC-1)
2. Update CLAUDE.md language (REC-2)

**Long-term:**
1. Audit all skills for similar "assumed format" gaps
2. Add format validation to all persistence operations
3. Create cross-skill dependency documentation

**Monitoring:**
- After each /qa deep: Check ai-analysis directory for JSON files
- Weekly: Audit for markdown files in ai-analysis (should be zero)

---

## Related RCAs

- **RCA-024:** Phase 9 Feedback Storage Skipped (2026-01-11, 2 hours earlier)
  - Same root pattern: mandatory action with non-mandatory enforcement
  - /dev workflow vs /qa workflow context
  - Both involve feedback/AI analysis capture

- **RCA-009:** Incomplete Skill Workflow Execution
  - Pattern: Claude skips documented steps
  - Same class of issue

---

## Lessons Learned

1. **"If needed" = "Optional"** - Claude interprets conditional language as permission to skip.

2. **Format Requirements Need Explicit Instructions** - Saying "use JSON" in one skill doesn't ensure Claude reads it when executing another skill.

3. **Pattern Recurrence is Fast** - RCA-024 (Phase 9) and RCA-025 (Phase 4) occurred 2 hours apart. Fixes must address all similar contexts, not just the one that triggered the RCA.

4. **Cross-Skill Dependencies Need Documentation** - QA skill depends on feedback skill's format, but nothing enforced reading the format requirements.

5. **Verification is Essential** - Adding a "verify file exists and is correct format" step catches errors before they become user-visible issues.

---

**RCA-025 Document Complete**
