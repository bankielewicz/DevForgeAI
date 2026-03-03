# RCA-012: AC Checkbox Usage Conventions
## Documented Standards for Story Tracking Mechanisms

**Version:** 1.0
**Created:** 2025-01-21
**Status:** Established (RCA-012 Remediation)
**Authority:** Framework Standard

---

## Purpose

This document establishes official conventions for checkbox usage in DevForgeAI stories, eliminating the 80% inconsistency discovered during RCA-012 investigation and providing clear guidance for all framework users.

---

## Three-Layer Tracking System (RCA-011)

DevForgeAI uses **three complementary tracking mechanisms** with distinct purposes:

### Layer 1: TodoWrite (AI Self-Monitoring)

**Purpose:** AI tracks which TDD phase is currently executing

**Format:** Todo list managed by Claude during TDD workflow

**Example:**
```
Todos:
1. [completed] Execute Phase 0: Pre-Flight Validation
2. [in_progress] Execute Phase 1: Test-First Design
3. [pending] Execute Phase 2: Implementation
...
```

**Updated:** Real-time as phases start/complete

**Visible to:** User sees visual progress bars in Claude Code Terminal

**Source of Truth:** Workflow position (which phase is executing now)

---

### Layer 2: AC Verification Checklist (Granular Sub-Item Tracking)

**Purpose:** User visibility into AC completion progress (granular, per-sub-item)

**Format:** Checklist in story file's "Acceptance Criteria Verification Checklist" section

**Example:**
```markdown
## Acceptance Criteria Verification Checklist

### AC#1: Document Completeness

- [ ] Introduction section (≥200 words) - **Phase:** 2 - **Evidence:** src/claude/memory/effective-prompting-guide.md lines 1-50
- [ ] /ideate command guidance - **Phase:** 2 - **Evidence:** grep "## /ideate"
- [ ] /create-story command guidance - **Phase:** 2 - **Evidence:** grep "## /create-story"
...
```

**Updated:** End of each TDD phase (batch update Phase 1-5 items)

**Visible to:** User in story file

**Source of Truth:** Granular progress (which sub-items are complete)

**Checkbox Convention:** Mark `[x]` when sub-item complete (verified with evidence)

---

### Layer 3: Definition of Done (Official Completion Record)

**Purpose:** Quality gate validation - official record for story completion

**Format:** Checklist in story file's "Definition of Done" section

**Example:**
```markdown
## Definition of Done

### Implementation
- [x] Feature implemented
- [x] Code reviewed
- [x] Integration tested

### Quality
- [x] All tests passing
- [x] Coverage ≥95%

### Testing
- [x] Unit tests complete
- [x] Integration tests complete

### Documentation
- [x] API docs updated
- [x] User guide updated
```

**Updated:** Phase 4.5-5 Bridge (after deferrals validated, before git commit)

**Visible to:** User in story file, QA validation enforces

**Source of Truth:** Official completion status (what's done vs. what's deferred)

**Checkbox Convention:** Mark `[x]` when item complete, leave `[ ]` if deferred (requires "Approved Deferrals" section)

---

## Acceptance Criteria Headers (The Confusion Source)

### Template v2.1+ (Current Standard - As of 2025-01-21)

**Format:**
```markdown
### AC#1: [Criterion Title]

**Given** [precondition],
**When** [action],
**Then** [expected result].
```

**Checkbox Convention:** **NO CHECKBOXES** (headers are definitions, not trackers)

**Rationale:**
- AC headers define **WHAT to test** (immutable specification)
- They are **not progress trackers** (that's DoD and AC Checklist's role)
- Removing checkboxes eliminates ambiguity

**Marking Behavior:** Never marked (static definitions)

---

### Template v2.0 and v1.0 (Legacy - Before 2025-01-21)

**Format:**
```markdown
### 1. [ ] [Criterion Title]

**Given** [precondition],
**When** [action],
**Then** [expected result].
```

**Checkbox Convention:** **INCONSISTENT** (no documented standard existed)

**Observed Patterns:**
- **20% of stories:** AC headers marked `[x]` when DoD 100% complete (e.g., STORY-007)
- **80% of stories:** AC headers left `[ ]` regardless of completion (e.g., STORY-014, STORY-023, STORY-030, STORY-038)

**Issue:** No convention documented, leading to user confusion

**Marking Behavior:** Ambiguous (some mark when complete, most don't)

**Guidance for Old Stories:** **Ignore AC header checkboxes** - they don't reliably indicate completion. Check DoD section instead.

---

## Official Conventions (Established 2025-01-21)

### Convention 1: AC Headers Are Definitions (Not Trackers)

**Rule:** AC headers define WHAT needs to be tested/implemented. They are **static specifications** that do not change throughout story lifecycle.

**Checkbox Usage:**
- **Template v2.1+:** NO checkboxes (format: `### AC#N: Title`)
- **Template v2.0/v1.0:** Checkboxes present but **never marked** (vestigial artifact)

**Analogy:** AC headers are like "requirements specification document" - you don't mark the requirements doc "complete," you mark the implementation tracker (DoD) complete.

---

### Convention 2: DoD Is the Single Source of Truth for Completion

**Rule:** Definition of Done section is the **official completion record**. When reviewing any story (old or new format), check DoD section to determine completion status.

**Checkbox Usage:**
- Mark `[x]` when item is complete
- Leave `[ ]` if item is incomplete/deferred

**Deferral Rule:**
- ANY unchecked `[ ]` item in DoD REQUIRES "Approved Deferrals" section
- Section must include: user approval timestamp, blocker justification, follow-up reference

**Quality Gate:**
- QA validation (Phase 0.9) enforces this rule
- QA HALTS if DoD has unchecked items without "Approved Deferrals"

---

### Convention 3: AC Checklist Tracks Granular Progress (Optional)

**Rule:** AC Verification Checklist provides detailed sub-item tracking during TDD implementation. This is optional (not all stories use it).

**Checkbox Usage:**
- Mark `[x]` as sub-items complete during TDD phases
- Updated by devforgeai-development skill at end of each phase

**When Used:**
- Code implementation stories (when TDD workflow executed)
- Stories with complex AC requiring granular tracking

**When NOT Used:**
- Documentation stories (no code implementation)
- Simple stories (AC maps 1:1 to DoD items)
- Design-phase stories (implementation deferred)

---

### Convention 4: Workflow Status Tracks Lifecycle Phase

**Rule:** Workflow Status section shows which lifecycle phases are complete (Architecture, Development, QA, Release).

**Checkbox Usage:**
- Mark `[x]` when phase complete
- Leave `[ ]` if phase not yet executed

**Example:**
```markdown
## Workflow Status

- [x] Architecture phase complete   ← Story has gone through architecture
- [x] Development phase complete    ← Story has gone through TDD (status: "Dev Complete")
- [ ] QA phase complete             ← Story has NOT yet been QA validated
- [ ] Released                      ← Story has NOT yet been released
```

**Relationship to Story Status:**
- Status "Dev Complete" → Development checkbox `[x]`, QA checkbox `[ ]`
- Status "QA Approved" → Development and QA checkboxes `[x]`, Released checkbox `[ ]`
- Status "Released" → All checkboxes `[x]`

---

## Decision Trees

### "Should I Mark This Checkbox?"

```
Is this an AC header (### AC#N: or ### N. [ ])?
├─ YES → NEVER mark it (definitions are static)
└─ NO → Continue...

Is this in AC Verification Checklist section?
├─ YES → Mark [x] when sub-item complete (during TDD phase)
└─ NO → Continue...

Is this in Definition of Done section?
├─ YES → Is item complete?
│        ├─ YES → Mark [x]
│        └─ NO → Leave [ ] and add "Approved Deferrals" section
└─ NO → Continue...

Is this in Workflow Status section?
├─ YES → Mark [x] when phase complete (Architecture, Dev, QA, Release)
└─ NO → Unknown checkbox type (check story template documentation)
```

---

### "Is This Story Complete?"

```
Want to know if story is complete?
↓
Check DoD section
├─ All items [x]? → Story 100% complete ✅
└─ Some items [ ]? → Continue...
    ↓
    Check for "Approved Deferrals" section
    ├─ Section exists with user approval? → Story complete with documented deferrals ✅
    └─ Section missing? → Story incomplete (should not be "QA Approved") ❌
```

---

## Examples by Story Type

### Example 1: Code Implementation Story (Full TDD Workflow)

**Tracking Used:**
- ✅ TodoWrite (AI monitors TDD phases)
- ✅ AC Verification Checklist (granular sub-item tracking)
- ✅ Definition of Done (official completion)
- ✅ Workflow Status (lifecycle phases)

**Checkbox Patterns:**
```markdown
### AC#1: Feature Functionality                ← NO checkbox (definition)

## Acceptance Criteria Verification Checklist
- [x] Feature method created                   ← Marked when complete
- [x] Business logic implemented               ← Marked when complete

## Definition of Done
- [x] Feature implemented                      ← Marked in Phase 4.5-5 Bridge
- [x] All tests passing                        ← Marked in Phase 4.5-5 Bridge

## Workflow Status
- [x] Development phase complete               ← Marked when TDD done
- [ ] QA phase complete                        ← Marked when /qa passes
```

---

### Example 2: Documentation Story (No Code)

**Tracking Used:**
- ✅ TodoWrite (AI monitors phases)
- ❌ AC Verification Checklist (not used - no code implementation)
- ✅ Definition of Done (official completion)
- ✅ Workflow Status (lifecycle phases)

**Checkbox Patterns:**
```markdown
### AC#1: Documentation Complete               ← NO checkbox (definition)

## Acceptance Criteria Verification Checklist
(Section may be empty or omitted for documentation stories)

## Definition of Done
- [x] Document created                         ← Marked when complete
- [x] All sections included                    ← Marked when complete

## Workflow Status
- [x] Development phase complete               ← Marked when document done
- [ ] QA phase complete                        ← Pending validation
```

---

### Example 3: Design-Phase Story (Implementation Deferred)

**Tracking Used:**
- ✅ TodoWrite (monitors design phases)
- ❌ AC Verification Checklist (implementation deferred)
- ✅ Definition of Done (partially complete with deferrals)
- ✅ Workflow Status (design complete, implementation pending)

**Checkbox Patterns:**
```markdown
### AC#1: Design Specification Complete        ← NO checkbox (definition)

## Definition of Done

### Implementation
- [x] Design document created                  ← Design items marked
- [x] Architecture diagram included
- [ ] Feature implemented                      ← Implementation deferred

### Testing
- [ ] Unit tests                               ← Deferred to STORY-XXX
- [ ] Integration tests                        ← Deferred to STORY-XXX

## Approved Deferrals

**User Approval:** 2025-XX-XX HH:MM UTC
**Deferred Items:** Implementation and Testing (defer to STORY-XXX)

## Workflow Status
- [x] Development phase complete               ← Design phase counts as "development"
- [ ] QA phase complete                        ← Pending after implementation
```

---

## FAQ

### Q1: Why do old stories have unchecked AC headers if the story is complete?

**A:** Old stories (v1.0/v2.0 template) have **vestigial checkbox syntax** in AC headers. These checkboxes were never reliably marked (80% of stories left them unchecked). As of v2.1, AC headers have no checkboxes. For completion status, check the **Definition of Done** section, not AC headers.

---

### Q2: Should I go back and mark old AC headers [x] for completed stories?

**A:** **No.** AC headers are definitions (what to test), not trackers (what's complete). Even in old format, the convention is now to **leave AC headers unmarked**. If you want consistency, use the migration script to convert to v2.1 format (removes checkboxes entirely).

---

### Q3: What if DoD has unchecked items but story is "QA Approved"?

**A:** Check for **"Approved Deferrals"** section in Implementation Notes. If present with user approval timestamp, the unchecked items are intentionally deferred. If missing, this is a quality gate bypass (report for investigation).

---

### Q4: Can I mark AC headers [x] in v2.0 stories to track my own progress?

**A:** You can, but it's **not recommended**. This creates inconsistency with framework conventions and may confuse others reviewing your story. Use the **AC Verification Checklist** for granular tracking instead.

---

### Q5: What's the difference between AC Checklist and DoD?

**A:**

**AC Verification Checklist:**
- Granular (20-50 sub-items per story)
- Updated during TDD phases (real-time)
- Maps to phases (Phase 1 items, Phase 2 items, etc.)
- Optional (not all stories use it)

**Definition of Done:**
- Categorized (Implementation, Quality, Testing, Documentation)
- Updated in Phase 4.5-5 Bridge (after deferrals validated)
- Maps to quality gates (what must be complete for "Dev Complete" or "QA Approved")
- Required (all stories have DoD)

**Use AC Checklist for:** "What am I working on right now?"
**Use DoD for:** "Is this story officially complete?"

---

## Migration Guidance

### For Template v1.0/v2.0 Stories

**If You Want Consistency:**
```bash
# Use migration script (optional)
bash .claude/skills/devforgeai-story-creation/scripts/migrate-ac-headers.sh <story-file>

# Result: ### 1. [ ] → ### AC#1:
```

**If You're Fine with Old Format:**
- No action needed
- Framework supports both formats
- Just remember: **Ignore AC header checkboxes, check DoD section for completion**

---

### For New Stories (Template v2.1+)

**Automatic:** All new stories created with `/create-story` use v2.1 format automatically.

**AC Headers:** No checkboxes (format: `### AC#1: Title`)

**No Decision Needed:** Convention is built into template.

---

## Enforcement

### Automated Enforcement (Phase 2 - QA Enhancement)

**QA Phase 0.9 enforces:**
- 100% AC-to-DoD traceability (every AC requirement has DoD coverage)
- Documented deferrals (any unchecked DoD item requires "Approved Deferrals" section)

**QA does NOT enforce:**
- AC header checkbox status (ignored in both v2.0 and v2.1)

**Rationale:** AC headers are definitions, not subject to completion validation.

---

### Manual Enforcement (Code Review)

**When reviewing stories, check:**
- [ ] DoD section: All items `[x]` OR unchecked items have "Approved Deferrals"
- [ ] Workflow Status: Matches story status field (Dev Complete → Dev checkbox marked)
- [ ] AC headers: Ignore checkbox status in v1.0/v2.0, verify no checkboxes in v2.1

**Do NOT check:**
- AC header checkbox status (not reliable indicator)

---

## Historical Context

### Timeline of Checkbox Usage

**2025-10-XX (Template v1.0):**
- AC headers introduced with `### 1. [ ]` format
- No documented convention for marking
- Some users marked headers when complete, most didn't

**2025-10-30 (Template v2.0):**
- Structured tech spec added
- AC header format unchanged (still `### 1. [ ]`)
- Convention still undocumented
- Inconsistency continued

**2025-11-XX (RCA-011 - Three-Layer Tracking):**
- TodoWrite and AC Verification Checklist added
- AC headers became redundant for tracking
- Still included in template (oversight)
- Inconsistency worsened (now 3 tracking mechanisms, unclear which is authoritative)

**2025-01-21 (Template v2.1 - RCA-012 Remediation):**
- AC header checkboxes removed
- Convention documented in CLAUDE.md
- Single source of truth established (DoD)
- Inconsistency eliminated for future stories

---

## Related Documents

- **CLAUDE.md** - "Story Progress Tracking" and "Acceptance Criteria vs. Tracking Mechanisms" sections
- **INDEX.md** - RCA-012 overview
- **ANALYSIS.md** - Root cause: vestigial checkboxes
- **SAMPLING-REPORT.md** - 80% inconsistency evidence
- **TEMPLATE-REFACTORING.md** - REC-1 implementation (removes checkboxes)
- **MIGRATION-SCRIPT.md** - REC-4 optional migration for old stories

---

**Conventions Status:** Established and Documented
**Effective Date:** 2025-01-21 (template v2.1 release)
**Authority:** DevForgeAI Framework Standard (RCA-012 Remediation)
