# STORY-554 Refactoring Plan: MVP Launch Checklist

**Story:** STORY-554
**Phase:** 04 (Refactoring)
**Target File:** `src/claude/skills/operating-business/references/mvp-launch-checklist.md`
**Test Baseline:** 44/44 tests passing (10+14+10+10 across 4 suites)
**Created:** 2026-03-21

---

## Context

The `mvp-launch-checklist.md` is a 98-line markdown reference file that passed all Phase 03 tests. This refactoring focuses on improving content organization, eliminating structural inconsistencies, and applying DRY principles to the markdown document without changing test-observable behavior.

---

## Code Smells Detected

### Smell 1: Inconsistent Heading Casing (Naming Inconsistency)
- **Location:** Lines 22, 31, 40, 49, 58 (domain section headers)
- **Issue:** Domain headers use lowercase `legal`, `financial`, `marketing`, `technical`, `operations` while the H1 title and H2/H3 subsection headers use title case
- **Pattern:** `## legal Domain` vs `## Progressive Disclosure and Micro-Task Chunking`
- **Risk:** Tests use case-insensitive grep (`-qi`), so casing changes are safe for test suite compatibility

### Smell 2: Business Model Description Inconsistency (DRY Violation)
- **Location:** Lines 13-16 (Business Model Adaptation section)
- **Issue:** Two bullet items use "model applicable" phrasing and two use "model specific" phrasing for the same concept. This inconsistency makes the adaptation rules harder to parse.
- **Pattern:** "SaaS model applicable" vs "Service model specific" for semantically identical categorization

### Smell 3: Redundant Paragraph in Progressive Disclosure (DRY)
- **Location:** Lines 71 and 97
- **Issue:** The introductory sentence (line 71) and the Rationale section (lines 95-97) both explain the same concept (preventing overwhelm, reducing cognitive load). The rationale section repeats the introduction nearly verbatim.
- **Pattern:** Duplicate explanation of WHY progressive disclosure exists

### Smell 4: Missing Structural Separator Before Progressive Disclosure
- **Location:** Between line 66 (end of operations domain) and line 69 (start of progressive disclosure)
- **Issue:** There is a `---` separator after line 67 but the section transition from domain checklists to behavioral guidance would benefit from a clearer delineation

### Smell 5: Progressive Disclosure Subsection Hierarchy
- **Location:** Lines 73-97
- **Issue:** Four subsections (Chunking Configuration, Chunking Logic, Fallback Behavior, Rationale) are at the same H3 level but serve different purposes. Configuration and Logic are operational; Fallback and Rationale are meta/contextual. No structural grouping distinguishes these.

---

## Refactoring Steps (Executed Sequentially)

### Step 1: Normalize Domain Section Header Casing
- **Change:** Capitalize domain names in H2 headers for consistency with document title casing
- **From:** `## legal Domain`, `## financial Domain`, etc.
- **To:** `## Legal Domain`, `## Financial Domain`, etc.
- **Test Safety:** All domain tests use `grep -qi` (case-insensitive), so this is safe

### Step 2: Normalize Business Model Bullet Phrasing
- **Change:** Standardize all four model descriptions to use consistent "model-specific" phrasing
- **From:** Mixed "model applicable" / "model specific"
- **To:** All four using parallel grammatical structure
- **Test Safety:** AC1 tests grep for `(saas|marketplace|service|product).*(specific|only|model|applicable)` - maintaining any of these keywords preserves test compatibility

### Step 3: Consolidate Redundant Cognitive Load Explanation
- **Change:** Remove the redundant opening paragraph and let the Rationale section serve as the single explanation
- **Alternative:** Keep the opening paragraph concise (one sentence) and remove the rationale section
- **Decision:** Keep opening paragraph brief, merge unique rationale content into it, remove Rationale subsection
- **Test Safety:** Tests check for keywords like "overwhelm", "cognitive load", "ADHD", "manageable", "digestible" - these keywords must be preserved somewhere in the document

### Step 4: Run Full Test Suite
- **Command:** `bash tests/STORY-554/run_all_tests.sh`
- **Gate:** 44/44 must pass. If any fail, revert all changes and diagnose.

---

## Test Constraint Analysis

Critical patterns that MUST be preserved for tests to pass:

| Test Suite | Pattern Searched | Must Remain |
|---|---|---|
| AC1 Test 9 | `(saas|marketplace|service|product).*(specific|only|model|applicable)` | >= 2 matches |
| AC1 Test 10 | `(product|marketplace|physical).*inventory|inventory.*(product|marketplace|physical)` | >= 1 match |
| AC2 Test 2-6 | `## .*legal`, `## .*financ`, `## .*marketing`, `## .*technical`, `## .*operat` | H2 headers |
| AC2 Test 7-11 | `- [` items between domain headers | >= 3 per domain |
| AC2 Test 13 | `^- \[.\] .+( - | -- | \| ).+` | All 30 items with separator |
| AC3 Test 3 | `^- \[ \]` | >= 15 checkboxes |
| AC3 Test 5 | `^- \[ \] .+( - | -- |: ).+` | >= 90% with descriptions |
| AC3 Test 9 | `^# .*launch.*checklist|^# .*mvp.*launch|^# .*checklist` | H1 title |
| AC4 Test 2 | `progressive.*disclosure|micro.*task|chunking|pacing` | keyword present |
| AC4 Test 3 | `5.*(to|-).*7|chunk.*size|5.*7.*items|items.*5.*7` | chunk size documented |
| AC4 Test 5 | `20.*items|more.*than.*20|exceed.*20|threshold.*20|20.*threshold` | 20-item threshold |
| AC4 Test 6 | `^- \[ \]` | > 20 checkboxes |
| AC4 Test 7 | `ready for|shall we|would you like|let.*continue|next section|move on` | pacing prompt examples |
| AC4 Test 8 | `present.*chunk|group.*items|display.*batch|show.*at.*time|section.*by.*section` | chunking instructions |
| AC4 Test 9 | `fall.*back|full.*list|all.*at.*once|display.*all|skip.*chunk` | fallback behavior |
| AC4 Test 10 | `overwhelm|cognitive.*load|adhd|attention|manageable|digestible` | rationale keywords |

---

## Checkpoints

- [x] Baseline tests: 44/44 PASS
- [x] Step 1 complete (header casing) + tests pass (44/44)
- [x] Step 2 complete (model phrasing) + tests pass (44/44)
- [x] Step 3 complete (consolidate redundancy) + tests pass (44/44)
- [x] Final validation: 44/44 PASS (file reduced from 98 to 93 lines)

---

## Verification Checklist

- [ ] All target files verified to exist
- [ ] No references to deleted files
- [ ] Test patterns analyzed for safety

**Status:** Verified
