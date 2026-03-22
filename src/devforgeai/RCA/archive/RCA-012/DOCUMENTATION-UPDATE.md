# RCA-012: Documentation Updates (REC-2, REC-3)
## CLAUDE.md and Skill Documentation Enhancements

**Recommendation IDs:** REC-2 (CLAUDE.md), REC-3 (Skill versioning)
**Priority:** HIGH
**Combined Effort:** 1.25 hours
**Target:** User clarity and template evolution transparency

---

## REC-2: CLAUDE.md Tracking Mechanisms Clarification

### Objective

Add comprehensive documentation to CLAUDE.md explaining the distinction between AC headers (definitions) and tracking mechanisms (AC Checklist, DoD), eliminating user confusion when reviewing stories with unchecked AC headers.

---

### Implementation

**File:** `src/CLAUDE.md` (distribution source)

**Location:** After "Story Progress Tracking (NEW - RCA-011)" section

**Current Line:** ~line 470-500 (search for "RCA-011")

**Content to Add:** (Complete implementation in IMPLEMENTATION-GUIDE Step 1.4)

---

### Key Points in Documentation

1. **Table Comparing Three Tracking Mechanisms**
   - AC Headers: Definitions (never marked)
   - AC Checklist: Granular tracking (marked during TDD)
   - DoD: Official completion (marked in Phase 4.5-5 Bridge)

2. **Why AC Headers Have No Checkboxes**
   - Specifications vs. trackers distinction
   - Marking complete would imply no longer relevant (incorrect)

3. **Handling Old Stories (v1.0/v2.0)**
   - Checkbox syntax explanation (vestigial)
   - Inconsistent practice warning (some marked, most not)
   - Guidance: Ignore AC headers, check DoD section

4. **Single Source of Truth: DoD Section**
   - How to read DoD (all [x] = complete)
   - How to interpret incomplete items (check for Approved Deferrals)
   - Workflow Status as secondary indicator

5. **Quality Gate Rule**
   - 100% AC-to-DoD traceability required
   - Documented deferrals required for incomplete items
   - QA HALTS if either missing

---

### Validation

**Test 1: Section Exists**
```bash
grep -A 50 "Acceptance Criteria vs. Tracking Mechanisms" src/CLAUDE.md | head -60
# Expected: Full section visible with table and explanations
```

**Test 2: Table Formatted Correctly**
```bash
grep "| Element | Purpose | Checkbox Behavior |" src/CLAUDE.md
# Expected: 1 match (table header)
```

**Test 3: Quality Gate Rule Documented**
```bash
grep "100% AC-to-DoD traceability required" src/CLAUDE.md
# Expected: 1 match
```

**Test 4: User Review**
- User reads new section
- User reviews STORY-052 (old format with unchecked AC headers)
- User confirms: "Now I understand DoD is the source of truth"
- User approves documentation

---

### Sync to Operational Location

**After src/CLAUDE.md updated:**
```bash
cp src/CLAUDE.md CLAUDE.md
echo "✓ CLAUDE.md synced to root"
```

**Validation:**
```bash
diff src/CLAUDE.md CLAUDE.md
# Expected: No differences (files identical)
```

---

### Success Criteria

- [ ] New section added to CLAUDE.md
- [ ] Table clearly documents three mechanisms
- [ ] Old story format explained (v1.0/v2.0 caveat)
- [ ] Quality gate rule documented
- [ ] Synced to operational location
- [ ] User review approved
- [ ] No confusion in user feedback

**Effort:** 45 minutes
- Writing: 30 minutes
- Review: 10 minutes
- Sync: 5 minutes

---

## REC-3: Template Version History in Skill Documentation

### Objective

Document template evolution in devforgeai-story-creation skill so users and maintainers understand why different stories have different formats.

---

### Implementation

**File:** `.claude/skills/devforgeai-story-creation/SKILL.md`

**Location:** Add new section "Story Template Versions" after template description

**Search For:** "story template" or "template.md" to find insertion point

**Content to Add:** (Complete implementation in IMPLEMENTATION-GUIDE Step 1.3)

---

### Key Points in Documentation

1. **Current Version**: 2.1 (as of 2025-01-21)

2. **Version History Table**:
   - v2.1: AC header checkbox removal (RCA-012)
   - v2.0: Structured tech spec (RCA-006)
   - v1.0: Original format

3. **Migration Path**:
   - v1.0 → v2.0: Gradual
   - v2.0 → v2.1: Optional script
   - Backward compatibility: All versions supported

4. **Cross-Reference**:
   - "See template changelog in assets/templates/story-template.md"

---

### Validation

**Test 1: Section Exists**
```bash
grep -A 20 "Story Template Versions" .claude/skills/devforgeai-story-creation/SKILL.md
# Expected: Version history section visible
```

**Test 2: All Versions Documented**
```bash
grep "v2.1" .claude/skills/devforgeai-story-creation/SKILL.md
grep "v2.0" .claude/skills/devforgeai-story-creation/SKILL.md
grep "v1.0" .claude/skills/devforgeai-story-creation/SKILL.md
# Expected: All 3 versions mentioned
```

**Test 3: Migration Path Explained**
```bash
grep -i "migration" .claude/skills/devforgeai-story-creation/SKILL.md | grep -i "optional"
# Expected: "Optional migration script available"
```

---

### Success Criteria

- [ ] "Story Template Versions" section added
- [ ] All 3 versions documented (v1.0, v2.0, v2.1)
- [ ] Change rationale explained for each version
- [ ] Migration path documented
- [ ] Cross-reference to template changelog present
- [ ] Backward compatibility noted

**Effort:** 30 minutes
- Writing: 20 minutes
- Review: 5 minutes
- Validation: 5 minutes

---

## Combined Testing (REC-2 + REC-3)

### Integration Test: Documentation Cohesion

**Test:** User follows documentation journey
1. User creates story: `/create-story "Test"`
2. User sees format v2.1 in YAML frontmatter
3. User checks devforgeai-story-creation skill → finds "Story Template Versions" section
4. User reads version history → understands v2.1 changes
5. User checks CLAUDE.md → reads "Acceptance Criteria vs. Tracking Mechanisms"
6. User reviews old story (STORY-052) → understands AC headers won't be marked
7. User confirms: "I understand the three tracking mechanisms"

**Expected:** User can navigate from template version → skill docs → CLAUDE.md → understanding

**Validation:**
- [ ] User completes journey successfully
- [ ] User reports no confusion
- [ ] All documentation cross-references work
- [ ] User can explain tracking mechanisms

---

### Consistency Test: Terminology Alignment

**Test:** Verify both documents use consistent terminology

**Terms to Validate:**
- "AC Headers" (not "Acceptance Criteria Headers" or "AC Titles")
- "Definition of Done" (not "DoD Section" or "Completion Tracker")
- "AC Verification Checklist" (not "Granular Checklist" or "Sub-Item Tracker")
- "TodoWrite" (not "Phase Tracker" or "AI Monitoring")
- "Three-layer tracking" (consistent phrasing)

**Command:**
```bash
# Extract terminology from both files
grep -E "(AC Headers|Definition of Done|AC Verification Checklist|TodoWrite|three-layer)" src/CLAUDE.md > /tmp/claude-terms.txt
grep -E "(AC Headers|Definition of Done|AC Verification Checklist|TodoWrite|three-layer)" .claude/skills/devforgeai-story-creation/SKILL.md > /tmp/skill-terms.txt

# Compare usage
diff /tmp/claude-terms.txt /tmp/skill-terms.txt
# Expected: Similar usage patterns (no conflicting terminology)
```

**Validation:**
- [ ] Terminology consistent across documents
- [ ] No conflicting definitions
- [ ] Cross-references use same terms
- [ ] User won't encounter confusion from term variations

---

## Documentation Quality Standards

### Clarity Requirements

**CLAUDE.md Section Must:**
- [ ] Use table format for visual comparison (3 tracking mechanisms)
- [ ] Provide concrete examples (STORY-052 reference)
- [ ] Explain historical context (v1.0/v2.0 template caveat)
- [ ] State quality gate rule clearly (100% traceability required)
- [ ] Include navigation aids (cross-references to skills, guides)

**Skill Documentation Must:**
- [ ] List all 3 versions (v1.0, v2.0, v2.1)
- [ ] Explain rationale for each version change
- [ ] Document migration path (optional, not required)
- [ ] Cross-reference template changelog
- [ ] Note backward compatibility

### Completeness Requirements

**CLAUDE.md Coverage:**
- ✓ What AC headers are (definitions)
- ✓ What AC headers are NOT (trackers)
- ✓ Where to find completion status (DoD section)
- ✓ How to handle old stories (ignore AC checkboxes)
- ✓ Quality gate enforcement (100% traceability)

**Skill Documentation Coverage:**
- ✓ Version evolution timeline
- ✓ Changes in each version
- ✓ Impact of each change
- ✓ Migration guidance
- ✓ Backward compatibility assurance

---

## Rollback Procedures

### REC-2 Rollback (CLAUDE.md)

**If documentation causes confusion:**
```bash
# Revert using git
git checkout src/CLAUDE.md CLAUDE.md

echo "✓ CLAUDE.md reverted to pre-RCA-012 state"
```

**Alternative:** Edit section to improve clarity (don't remove, refine)

---

### REC-3 Rollback (Skill Documentation)

**If version history is incorrect:**
```
Edit .claude/skills/devforgeai-story-creation/SKILL.md
Remove or correct "Story Template Versions" section
Save changes
```

**Low Risk:** Documentation only, no code changes

---

## Completion Checklist

### REC-2: CLAUDE.md Update
- [ ] New section added after RCA-011 section
- [ ] Table formatted correctly (3 mechanisms)
- [ ] Old story format explained
- [ ] Quality gate rule documented
- [ ] Synced to root CLAUDE.md
- [ ] User review approved

### REC-3: Skill Versioning
- [ ] "Story Template Versions" section added
- [ ] v1.0, v2.0, v2.1 all documented
- [ ] Change rationale clear
- [ ] Migration path explained
- [ ] Cross-reference to changelog present

### Combined Validation
- [ ] Terminology consistent (CLAUDE.md ↔ Skill docs)
- [ ] Cross-references work (bidirectional)
- [ ] User can navigate documentation
- [ ] No confusion in user testing

---

**REC-2 + REC-3 Status:** Ready for Implementation
**Combined Effort:** 1.25 hours (45 min + 30 min + 10 min review)
**Priority:** HIGH (supports REC-1 template refactoring)
