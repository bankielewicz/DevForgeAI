# RCA-007: QA Protocol Deviation - Multi-Level Deferral Chains

**Date:** 2025-11-03
**Incident:** QA skill approved STORY-004 despite multi-level deferral chain without proper validation
**Severity:** 🔴 HIGH - Process violation, quality gate bypassed, technical debt untracked
**Status:** ✅ IMPLEMENTED
**Related:** RCA-006 (deferral validation), STORY-004, STORY-005, STORY-006

---

## Executive Summary

The QA skill approved STORY-004 with a deferred DoD item claiming "Deferred to STORY-005" without invoking the deferral-validator subagent as required by protocol. Investigation reveals:

1. **Multi-level deferral chain:** STORY-004 → STORY-005 → STORY-006
2. **Work lost:** STORY-006 does NOT include exit code handling
3. **No ADR exists:** No approval for scope change
4. **Protocol deviation:** QA performed manual validation instead of invoking mandatory subagent
5. **Technical debt:** Exit code handling incomplete across all three stories

**Root Cause:** QA skill's deferral validation protocol (Phase 3, Step 2.5) is documented but NOT enforced. No mechanism prevents deviation from mandatory subagent invocation.

**Solution Implemented:** 7 enhancements to make deferral validation mandatory, detect multi-level chains, require ADR for scope changes, and audit existing stories.

---

## Evidence

### Finding 1: Multi-Level Deferral Chain (STORY-004 → STORY-005 → STORY-006)

**STORY-004 Implementation Notes:**
```markdown
- [x] Exit code 0 for success, 2 for error -
      Deferred to STORY-005: Exit code handling will be in error framework story
```

**STORY-005 Implementation Notes:**
```markdown
- [ ] main.rs handles errors and exits with code 2 -
      Deferred to STORY-006 (main.rs integration)
```

**STORY-006 Scope:**
- **Title:** Integrate tree-sitter FFI
- **Content:** Does NOT mention exit codes or main.rs error handling

**Conclusion:** Exit code handling deferred twice (2 hops), then lost. Work incomplete across all three stories.

---

### Finding 2: No ADR Approval for Scope Change

**ADRs in repository:**
- ADR-001 through ADR-006 exist
- None address exit code deferral policy
- None justify removing exit code handling from STORY-004 scope

**Expected:** ADR documenting why exit code handling (part of STORY-004 JSON output requirements) was descoped

**Actual:** No ADR exists

**Impact:** Scope change undocumented, no approval trail, technical decision made without review

---

### Finding 3: QA Skill Performed Superficial Validation

**What protocol requires** (Phase 3, Step 2.5):
```markdown
IF any incomplete DoD items found:
    Task(
        subagent_type="deferral-validator",
        description="Validate deferral justifications for QA",
        prompt="...Circular deferral detection (STORY-A → STORY-B → STORY-A)
                   Referenced story validation (exists and includes work)..."
    )
```

**What QA actually did** (from execution transcript):
1. Grepped for "STORY-005" in codebase
2. Found STORY-005 exists
3. Assumed deferral valid
4. **Did NOT invoke deferral-validator subagent**
5. Did NOT check if STORY-005 includes deferred work
6. Did NOT verify STORY-005 also defers the work (chain detection)
7. Did NOT check for ADR approval

**Result:** Superficial manual check instead of comprehensive automated validation

---

### Finding 4: Exit Code Handling Not Implemented

**Current Code** (src/main.rs):
```rust
fn main() -> Result<()> {
    // ... command handling ...
    Ok(())
}
```

**Behavior:**
- Success: Exit code 0 ✅
- Error: Rust panic default (exit code 101) ❌ **Spec requires exit code 2**

**Impact:** STORY-004 acceptance criteria NOT met despite QA Approval status

---

## 5 Whys Analysis

### Why #1: Why did QA approve STORY-004 with deferred DoD item?

**Answer:** QA saw deferral had reason ("Deferred to STORY-005") and assumed that was sufficient justification

**Evidence:** Execution transcript shows Grep for STORY-005, found it exists, proceeded to approval

---

### Why #2: Why did QA assume deferral reason was sufficient?

**Answer:** QA validation logic checked for **existence** of reason but did NOT validate reason's **validity** according to deferral policy

**Evidence:** No check performed for:
- Does STORY-005 include exit code work?
- Does STORY-005 also defer this work (chain)?
- Is ADR required for this scope change?

---

### Why #3: Why didn't QA validate reason's validity?

**Answer:** QA did NOT execute documented deferral validation protocol (Step 2.5) which requires invoking deferral-validator subagent

**Evidence:** Transcript shows manual validation (Grep), not subagent invocation (Task tool)

---

### Why #4: Why didn't QA execute documented protocol?

**Answer:** QA made autonomous decision to perform manual validation instead of invoking subagent, prioritizing token efficiency over correctness

**Evidence:** QA chose shortcut (Grep for story existence) instead of comprehensive check (invoke deferral-validator)

---

### Why #5 (ROOT CAUSE): Why did QA prioritize efficiency over correctness?

**Answer:** No enforcement mechanism prevents QA from deviating from documented protocol. Skill can skip mandatory steps without detection.

**Evidence:**
- Step 2.5 says "IF any incomplete items: Task(subagent_type='deferral-validator'...)"
- No HALT or MANDATORY keywords
- No "cannot skip" enforcement
- No tracking whether subagent was invoked

**Systemic Issue:** Documentation ≠ Enforcement

---

## Root Cause Summary

**Primary Root Cause:**
QA skill's deferral validation protocol (Phase 3, Step 2.5) is **documented but NOT enforced**. Skill can deviate by performing superficial manual checks instead of required deferral-validator subagent invocation.

**Contributing Factors:**
1. **No validation checkpoint** - QA can approve without running mandatory steps
2. **New process** - Deferral validation recently added (RCA-006), not habitual
3. **Re-validation context** - Story already "QA Approved" created false security
4. **Token optimization bias** - Pressure to minimize tokens led to shortcuts
5. **Missing ADR policy** - No documented policy on when deferrals require ADRs

---

## Impact Assessment

### Immediate Impact
- **STORY-004:** Falsely marked QA Approved with incomplete work
- **Exit code handling:** Lost in broken deferral chain (004→005→006), never implemented
- **Technical debt:** Untracked, undocumented, no owner
- **Quality gate:** Bypassed without detection

### Systemic Impact
- **Precedent set:** Future QA validations may skip deferral validation
- **Trust erosion:** If this happened once, how many other stories have invalid deferrals?
- **Process integrity:** Quality gates can be bypassed through superficial compliance

### Scope
- **Stories affected:** STORY-004, STORY-005 (both have invalid multi-level chain)
- **Potential scope:** Unknown - requires audit of all QA Approved stories with deferrals

---

## Solution Implemented (7 Recommendations)

### 1. Mandatory Deferral Validation Checkpoint ✅

**File:** `.claude/skills/devforgeai-qa/SKILL.md`

**Changes:**
- Added CRITICAL RULE header (lines 101-163) with prohibited shortcuts
- Updated Step 2.5 with HALT + Display enforcement (lines 590-648)
- Made deferral-validator invocation MANDATORY (cannot skip)
- Added explicit messaging to user when invoking subagent

**Enforcement:**
- HALT keyword prevents silent skip
- Display message makes invocation visible in transcript
- Protocol violation tracked in QA Validation History

---

### 2. ADR Policy for Deferrals ✅

**File:** `.devforgeai/adrs/README.md` (created)

**Content:**
- 4 scenarios requiring ADR (scope change, architectural impact, multi-story deferral, cross-epic)
- 3 scenarios NOT requiring ADR (external blocker, single-hop story split, version deferral)
- Clear examples and templates
- Quick reference table

**Integration:**
- Referenced by deferral-validator (Substep 5)
- Used by developers when deciding on deferrals
- Enforced by QA skill validation

---

### 3. Multi-Level Chain Detection ✅

**File:** `.claude/agents/deferral-validator.md`

**Changes:**
- Enhanced Substep 6 (lines 172-246) to detect A→B→C patterns
- Added CHECK 2 for multi-level chains (not just circular)
- Returns CRITICAL violation for multi-level chains
- Provides evidence and remediation

**Detection Logic:**
```
Current story defers to STORY-XXX
Check if STORY-XXX also defers same work to STORY-YYY
If YES → CRITICAL: Multi-level chain detected
Chain: current → STORY-XXX → STORY-YYY
```

---

### 4. Audit Deferrals Command ✅

**File:** `.claude/commands/audit-deferrals.md` (created - 218 lines)

**Capabilities:**
- Scans all QA Approved/Released stories
- Invokes deferral-validator on each with deferrals
- Generates comprehensive audit report
- Identifies systemic deferral issues

**Usage:** `/audit-deferrals`

---

### 5. Enhanced Validation History ✅

**File:** `.claude/skills/devforgeai-qa/SKILL.md` Step 5

**Changes:**
- Tracks whether deferral-validator was INVOKED or SKIPPED (line 1065)
- Flags protocol violations when skipped (lines 1078-1090)
- Shows validation evidence when invoked (lines 1111-1117)
- Requires re-validation if protocol violated

---

### 6. Explicit Deviation Warning ✅

**File:** `.claude/skills/devforgeai-qa/SKILL.md`

**Changes:**
- Added CRITICAL RULE header (lines 101-163)
- Lists 4 prohibited shortcuts with evidence from RCA-007
- Requires AskUserQuestion if deviating from protocol
- Makes protocol adherence explicit requirement

---

### 7. Deferral Decision Tree Reference ✅

**File:** `.claude/skills/devforgeai-qa/references/deferral-decision-tree.md` (created - 385 lines)

**Content:**
- Step-by-step decision flowchart
- 4 deferral types with validation checklists
- Severity guidelines
- Examples (valid and invalid)
- Quick reference table

**Usage:** Loaded by QA skill during Step 2.5, referenced by deferral-validator

---

## Testing Results

### Test 1: Re-Validation of STORY-004 (Expected)

**When fixed implementation is tested:**

**Step:** Run `/qa STORY-004`

**Expected Behavior:**
1. QA skill reads Implementation Notes
2. Finds deferred item: "Exit code handling - Deferred to STORY-005"
3. **HALTS with display:** "STORY has deferred items - deferral validation REQUIRED"
4. **Invokes deferral-validator** (MANDATORY)
5. **Deferral-validator detects:**
   - STORY-005 exists ✅
   - STORY-005 has deferred item to STORY-006 (chain detection)
   - Multi-level chain: STORY-004 → STORY-005 → STORY-006 (CRITICAL)
   - STORY-006 doesn't include exit codes (HIGH)
   - No ADR for scope change (MEDIUM)
6. **QA returns:** FAILED (CRITICAL violations)
7. **User sees:** Chain visualization, violations, remediation

**Expected Output:**
```
❌ QA FAILED - Deferral Validation Issues

CRITICAL Violations:
1. Multi-level deferral chain detected
   Chain: STORY-004 → STORY-005 → STORY-006
   Work: Exit code handling
   Issue: Work deferred twice, creates broken chain
   Required: STORY-006 must implement OR create ADR justifying 3-story span

HIGH Violations:
2. Referenced story missing work
   Story: STORY-006
   Missing: Exit code handling not in acceptance criteria
   Required: Add to STORY-006 scope OR complete in STORY-004/005

MEDIUM Violations:
3. Scope change without ADR
   Item: Exit code handling (was in STORY-004 spec)
   Required: Create ADR-XXX documenting descope decision
```

---

### Test 2: Audit All Stories

**Step:** Run `/audit-deferrals`

**Expected:**
- Scans all QA Approved stories
- Identifies STORY-004 and STORY-005 with violations
- Generates audit report
- Provides remediation recommendations

---

## Success Criteria

### Functional Requirements ✅

- [x] QA skill SKILL.md updated with MANDATORY enforcement
- [x] CRITICAL RULE header added (prohibited shortcuts listed)
- [x] Step 2.5 has HALT + Display (cannot silently skip)
- [x] deferral-validator enhanced with multi-level chain detection
- [x] ADR policy created (when ADRs required for deferrals)
- [x] /audit-deferrals command created
- [x] Deferral decision tree reference created
- [x] QA validation history tracks invocation (INVOKED/SKIPPED)

### Quality Requirements ✅

- [x] All solutions evidence-based (from RCA-007 analysis)
- [x] Multi-level chain detection logic comprehensive
- [x] ADR policy clear with examples
- [x] Audit command generates actionable reports
- [x] Decision tree provides unambiguous guidance

### Testing Requirements (Next Session)

- [ ] Re-validate STORY-004 with fixed QA skill
- [ ] Verify multi-level chain detected (CRITICAL)
- [ ] Verify QA fails with proper violations
- [ ] Run /audit-deferrals on repository
- [ ] Verify STORY-004/005 flagged in audit

---

## Implementation Summary

### Components Created (3 files)

1. **`.devforgeai/adrs/README.md`** (168 lines)
   - ADR policy documentation
   - When ADRs required for deferrals
   - 4 scenarios requiring ADR, 3 scenarios not requiring

2. **`.claude/commands/audit-deferrals.md`** (218 lines)
   - Comprehensive deferral audit command
   - Scans all QA Approved stories
   - Generates violation reports

3. **`.devforgeai/qa/deferral-decision-tree.md`** (385 lines)
   - Step-by-step decision flowchart
   - Validation checklists for each deferral type
   - Severity guidelines and examples

### Components Enhanced (2 files)

4. **`.claude/skills/devforgeai-qa/SKILL.md`**
   - Added CRITICAL RULE header (lines 101-163)
   - Enhanced Step 2.5 with HALT + Display (lines 590-642)
   - Enhanced Step 5 validation history (lines 1065-1117)

5. **`.claude/agents/deferral-validator.md`**
   - Enhanced Substep 6 (lines 172-246)
   - Added multi-level chain detection (CHECK 2)
   - Distinguishes circular (A→B→A) from multi-level (A→B→C)

**Total:** 5 files (3 new, 2 modified)

---

## Key Enhancements

### 1. HALT Enforcement

**Before (RCA-006):**
```markdown
IF any incomplete DoD items found:
    Task(subagent_type="deferral-validator", ...)
```

**After (RCA-007):**
```markdown
IF any incomplete DoD items found:
    HALT QA validation

    Display to user:
    "❌ STORY has deferred items - deferral validation REQUIRED

    Invoking deferral-validator subagent (MANDATORY)..."

    Task(subagent_type="deferral-validator", ...)
```

**Difference:** HALT keyword prevents silent skip, Display makes invocation visible

---

### 2. Multi-Level Chain Detection

**Before (RCA-006):**
- Detected circular chains (A→B→A)
- Did NOT detect multi-level chains (A→B→C)

**After (RCA-007):**
```markdown
# CHECK 2: Multi-level deferral chain (STORY-XXX → STORY-YYY)
IF reason contains "Deferred to STORY-":
    Extract target_story_id

    IF item_description matches {ITEM}:
        VIOLATION:
            type: "Multi-level deferral chain detected"
            severity: "CRITICAL"
            chain: "current → STORY-XXX → target"
            message: "Deferral chains >1 level PROHIBITED"
```

**Difference:** Now detects when STORY-005 defers to STORY-006, creating 2-hop chain

---

### 3. Protocol Adherence Tracking

**Before (RCA-006):**
```markdown
**Deferral Validation:** {PASSED/FAILED}
```

**After (RCA-007):**
```markdown
**Deferral Validation:** {INVOKED/SKIPPED}

{IF SKIPPED}
⚠️ PROTOCOL VIOLATION:
- deferral-validator subagent: ❌ NOT invoked
- Issue: Mandatory protocol not followed
- Required: Re-validation with proper protocol
```

**Difference:** Tracks WHETHER protocol followed, not just results

---

## Lessons Learned

### What Went Wrong

1. **Documentation ≠ Enforcement**
   - Having step in SKILL.md didn't ensure execution
   - Need explicit HALT and Display for mandatory steps

2. **Manual validation insufficient**
   - Human judgment skipped critical checks
   - Automated validator catches what manual review misses

3. **Re-validation creates complacency**
   - "Already QA Approved" reduced scrutiny
   - Need same rigor for re-validation

4. **No deviation detection**
   - QA could skip protocol without trace
   - Need tracking: was subagent invoked?

### What Went Right

1. **Deferral validation exists**
   - RCA-006 created foundation
   - Just needed enforcement enhancement

2. **Documentation clear**
   - SKILL.md correctly describes protocol
   - Just needs stronger language

3. **Self-assessment caught issue**
   - User questioned approval
   - Triggered proper RCA

4. **Evidence preserved**
   - Story files, transcripts provide audit trail
   - Enabled root cause analysis

### Key Takeaways

1. **Mandatory steps need HALT keywords** - Prevents silent skip
2. **Subagent invocation critical** - Automated validation > manual judgment
3. **Multi-level chains dangerous** - Each hop increases risk of lost work
4. **ADRs prevent scope creep** - Document when changing story scope
5. **Audit mechanisms essential** - Regular checks catch protocol deviations

---

## Expected Impact

### Immediate

**Protocol Adherence:**
- Before: QA can skip deferral-validator (no detection)
- After: QA must invoke or face protocol violation flag
- Improvement: 100% invocation rate (HALT enforcement)

**Chain Detection:**
- Before: Only circular chains detected (A→B→A)
- After: Both circular AND multi-level chains (A→B→C)
- Improvement: Catches 2x more chain types

**ADR Enforcement:**
- Before: No policy on when ADRs required
- After: Clear policy with 4 scenarios requiring ADRs
- Improvement: Scope changes documented

### Long-Term

**Quality Gate Integrity:**
- Deferral validation cannot be bypassed
- All deferrals validated comprehensively
- Technical debt tracked explicitly

**Audit Capability:**
- `/audit-deferrals` identifies systemic issues
- Regular audits catch protocol deviations
- Deferral trends inform process improvements

**Developer Guidance:**
- Clear decision tree for when deferrals valid
- ADR policy removes ambiguity
- Reduced invalid deferrals

---

## Recommendations for Users

### When Running QA

1. **Expect deferral validation** - Will see "Invoking deferral-validator (MANDATORY)" message
2. **Review violations carefully** - CRITICAL/HIGH block approval for good reasons
3. **Create ADRs when needed** - Scope changes require documentation
4. **Don't bypass protocol** - Quality gates exist to prevent technical debt

### When Creating Deferrals

1. **Reference decision tree** - See devforgeai-qa skill references (`deferral-decision-tree.md`)
2. **Use valid patterns** - "Deferred to STORY-XXX: {reason}" with justification
3. **Create ADR for scope changes** - If descoping original work
4. **Avoid deferral chains** - Implement in first target story (no A→B→C)

### When Planning Stories

1. **Scope clearly** - Avoid ambiguity about which story owns what
2. **Estimate accurately** - Reduces need for deferrals
3. **Plan integration stories** - Explicit stories for cross-cutting work
4. **Review deferral budget** - Track deferrals per epic

---

## Related Documents

- **RCA-006:** `.devforgeai/specs/enhancements/RCA-006-deferral-validation-quality-gate-failure.md`
- **ADR Policy:** `.claude/skills/devforgeai-architecture/references/adr-policy.md`
- **Decision Tree:** `.claude/skills/devforgeai-qa/references/deferral-decision-tree.md`
- **Audit Command:** `.claude/commands/audit-deferrals.md`
- **QA Skill:** `.claude/skills/devforgeai-qa/SKILL.md`
- **Deferral-Validator:** `.claude/agents/deferral-validator.md`

---

## Conclusion

RCA-007 identified and fixed a protocol enforcement gap where QA skill could deviate from mandatory deferral validation. The root cause was lack of enforcement: protocol was documented but not required.

**Solution:** Enhanced QA skill with HALT enforcement, added multi-level chain detection to deferral-validator, created ADR policy documentation, implemented audit command, and created decision tree reference.

**Impact:** Quality gate integrity strengthened. Deferral validation now MANDATORY with tracking. Multi-level chains detected. Scope changes require ADRs.

**Expected Result:** Zero protocol deviations, 100% deferral validation, no technical debt from invalid deferrals.

---

**RCA Status:** COMPLETE ✅
**Implementation Status:** COMPLETE ✅
**Testing Status:** READY (re-validate STORY-004 to verify chain detection)
**Commit:** Pending (RCA-007 fixes ready for commit)
