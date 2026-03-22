# RCA-012: AC-to-DoD Traceability Matrix
## Visual Mapping Examples and Template Enhancement (REC-7)

**Recommendation ID:** REC-7
**Priority:** MEDIUM
**Effort:** 2 hours
**Purpose:** Enhanced transparency via visual mapping

---

## Objective

Provide visual mapping template showing how each Acceptance Criterion requirement is validated in Definition of Done, making traceability explicit and reducing cognitive load for users reviewing stories.

---

## Traceability Matrix Concept

### What It Is

A **table showing the relationship** between:
- Acceptance Criteria requirements (what needs to be tested/implemented)
- Definition of Done items (how requirements are validated)
- Validation type (explicit checkbox, test validation, metric validation)

### Why It's Valuable

**Before Matrix:**
- User must infer which DoD items validate which AC requirements
- Traceability is implicit (requires reading full story)
- Validation gaps are hard to spot
- QA Phase 0.9 does this algorithmically (but user can't see the mapping)

**After Matrix:**
- Explicit visual mapping (AC → DoD relationship clear)
- Traceability is explicit (one table shows everything)
- Validation gaps obvious (empty cells in matrix)
- Users can verify traceability before submitting for QA

---

## Matrix Template Format

### Basic Structure

```markdown
## AC-to-DoD Traceability Matrix

**Purpose:** Visual mapping showing how each AC requirement is validated in DoD

| AC | Requirement | DoD Item | Validation Type | Evidence |
|----|-------------|----------|-----------------|----------|
| AC#1 | {Requirement text} | Implementation: Item #{N} | Explicit Checkbox | {File/line/metric} |
| AC#1 | {Another requirement} | Testing: Item #{N} | Test Validation | {Test name/file} |
| AC#2 | {Requirement text} | Quality: Item #{N} | Explicit Checkbox | {File/line/metric} |
| AC#3 | {Requirement text} | Testing: Item #{N} | Test Validation | {Test name} |

**Validation Types:**
- **Explicit Checkbox:** DoD item directly states requirement with measurable criteria
- **Test Validation:** DoD item references test that validates requirement
- **Metric Validation:** DoD item provides quantitative proof (e.g., "Coverage >95%")

**Traceability Score:** {checked requirements} / {total requirements} × 100 = {percentage}%

**Quality Gate:** 100% required for QA approval
```

---

## Complete Example: STORY-052 Traceability Matrix

```markdown
## AC-to-DoD Traceability Matrix

**Story:** STORY-052 - User-Facing Prompting Guide Documentation
**Total ACs:** 6
**Total AC Requirements:** 30 (granular)
**Total DoD Items:** 26
**Traceability Score:** 100%

| AC | Requirement Description | DoD Item | Validation Type | Evidence |
|----|-------------------------|----------|-----------------|----------|
| **AC#1** | Introduction ≥200 words | Implementation #2: "Document includes introduction (648 words)" | Explicit Checkbox | src/claude/memory/effective-prompting-guide.md (648 words counted) |
| **AC#1** | 11 command sections | Implementation #3: "All 11 commands have dedicated guidance sections" | Explicit Checkbox | grep "^## /" returns 11 matches |
| **AC#1** | 20-30 examples | Implementation #4: "24 before/after examples included" | Explicit Checkbox | grep "❌ BEFORE" returns 24 matches |
| **AC#1** | Quick reference checklist | Implementation #5: "Quick reference checklist created (in first 500 lines)" | Explicit Checkbox | head -500 contains checklist |
| **AC#1** | ≥10 pitfalls | Implementation #7: "Common pitfalls section (10 pitfalls with mitigations)" | Explicit Checkbox | grep "^### Pitfall" returns 10 matches |
| **AC#1** | Progressive disclosure | Quality #6: "Document coverage 100%" | Implicit Coverage | Structure verified in testing |
| **AC#2** | Realistic examples | Testing #2: "Example validation test (AC2 - PASS)" | Test Validation | tests/STORY-052/test-example-quality.sh |
| **AC#2** | ≥50 words explanations | Testing #2: "Example validation test (AC2 - PASS)" | Test Validation | Word count validated by test |
| **AC#2** | Reference actual commands | Testing #2: "Example validation test (AC2 - PASS)" | Test Validation | Command references validated |
| **AC#2** | Demonstrate improvements | Testing #2: "Example validation test (AC2 - PASS)" | Test Validation | Before/after comparisons validated |
| **AC#2** | Measurable improvements | Testing #2: "Example validation test (AC2 - PASS)" | Test Validation | Metrics validated in examples |
| **AC#3** | Required inputs listed | Testing #4: "Quality validation test (AC3, AC5 - PASS)" | Test Validation | tests/STORY-052/test-command-guidance.sh |
| **AC#3** | 2-3 examples per command | Testing #4: "Quality validation test (AC3, AC5 - PASS)" | Test Validation | Example count per command validated |
| **AC#3** | "Complete" definition | Testing #4: "Quality validation test (AC3, AC5 - PASS)" | Test Validation | Completeness criteria validated |
| **AC#3** | Cross-references | Testing #3: "Cross-reference validation test (AC4, AC6 - PASS)" | Test Validation | tests/STORY-052/test-framework-reality.sh |
| **AC#3** | SKILL.md alignment | Testing #4: "Quality validation test (AC3, AC5 - PASS)" | Test Validation | Alignment validated by test |
| **AC#4** | Links to source docs | Testing #3: "Cross-reference validation test (AC4, AC6 - PASS)" | Test Validation | Link validation test |
| **AC#4** | Inline explanations ≤100 words | Testing #3: "Cross-reference validation test (AC4, AC6 - PASS)" | Test Validation | Word count validated |
| **AC#4** | Consistent terminology | Testing #4: "Quality validation test (AC3, AC5 - PASS)" | Test Validation | Terminology consistency checked |
| **AC#4** | ToC with anchor links | Implementation #6: "Table of contents with functional anchor links" | Explicit Checkbox | ToC structure validated |
| **AC#5** | ToC in first 100 lines | Testing #1: "Structure validation test (AC1, AC5 - PASS)" | Test Validation | tests/STORY-052/test-document-structure.sh |
| **AC#5** | ≤3 clicks to section | Testing #1: "Structure validation test (AC1, AC5 - PASS)" | Test Validation | Navigation tested |
| **AC#5** | Visual hierarchy | Testing #1: "Structure validation test (AC1, AC5 - PASS)" | Test Validation | Markdown structure validated |
| **AC#5** | Quick ref in first 500 lines | Implementation #5: "Quick reference checklist created (in first 500 lines)" | Explicit Checkbox | Position validated |
| **AC#5** | Consistent formatting | Testing #1: "Structure validation test (AC1, AC5 - PASS)" | Test Validation | Code blocks, tables validated |
| **AC#6** | Commands exist | Testing #5: "Command existence validation (AC6 - PASS)" | Test Validation | Glob .claude/commands/*.md |
| **AC#6** | Skills exist | Testing #6: "Framework reality validation (AC6 - PASS)" | Test Validation | Glob .claude/skills/*/SKILL.md |
| **AC#6** | Examples work (5 samples) | Testing #6: "Framework reality validation (AC6 - PASS)" | Test Validation | 5 examples tested with commands |
| **AC#6** | Syntax matches | Testing #6: "Framework reality validation (AC6 - PASS)" | Test Validation | Syntax comparison validated |
| **AC#6** | No deprecated features | Testing #6: "Framework reality validation (AC6 - PASS)" | Test Validation | Deprecation check passed |

**Traceability:** 30/30 requirements have DoD coverage (100%)
```

---

## Template Integration (REC-7 Implementation)

### Add Matrix Section to Story Template

**File:** `.claude/skills/devforgeai-story-creation/assets/templates/story-template.md`

**Location:** Add new section after "Acceptance Criteria Verification Checklist" (~line 500)

**Content to Add:**
```markdown
---

## AC-to-DoD Traceability Matrix

**Purpose:** Visual mapping showing how each Acceptance Criterion requirement is validated in Definition of Done. Populated during story creation to ensure 100% AC-DoD coverage.

**Usage:**
1. For each AC, list granular requirements (Given/When/Then clauses, bullet points, metrics)
2. Map each requirement to corresponding DoD item
3. Identify validation type (Explicit, Test, Metric)
4. Provide evidence (file, test, metric value)

**Quality Gate:** QA Phase 0.9 validates this matrix - all ACs must have DoD coverage (100% required)

| AC | Requirement Description | DoD Item | Validation Type | Evidence/Notes |
|----|------------------------|----------|-----------------|----------------|
| AC#1 | {Extract from AC#1 - first requirement} | Implementation: Item #{N} | Explicit Checkbox | {File, line, or metric} |
| AC#1 | {Extract from AC#1 - second requirement} | Testing: Item #{N} | Test Validation | {Test name or file} |
| AC#2 | {Extract from AC#2 - requirement} | Quality: Item #{N} | Metric Validation | {Metric name and value} |
| AC#3 | {Extract from AC#3 - requirement} | Implementation: Item #{N} | Explicit Checkbox | {Evidence} |

**Validation Types Defined:**

- **Explicit Checkbox:** DoD item directly mentions requirement with measurable criteria
  - Example: "- [ ] API response time <200ms (p95)" validates AC requirement for performance

- **Test Validation:** DoD item references test(s) that validate requirement
  - Example: "- [ ] Integration test: Auth workflow (AC#2 - validates login, logout, token refresh)" validates AC#2 requirements

- **Metric Validation:** DoD item provides quantitative proof without explicit checkbox
  - Example: "- [ ] Code coverage >95% (business logic)" validates AC requirement for test coverage

**Example Matrix (Reference):**

See STORY-007 (exemplar story) for complete traceability matrix showing 6 ACs mapped to 22 DoD items with 100% coverage.

**Traceability Score Calculation:**
```
covered_requirements = count(requirements with DoD item)
total_requirements = count(all granular requirements across all ACs)
traceability_score = (covered_requirements / total_requirements) × 100

Target: 100% (all requirements must have DoD coverage)
```

**Incomplete Matrix Handling:**

If matrix shows <100% traceability:
1. Add missing DoD items to cover unmapped requirements, OR
2. Update AC to clarify existing DoD items provide coverage, OR
3. Remove invalid/obsolete AC requirements

QA Phase 0.9 validates this matrix and HALTS if traceability <100%.

---
```

**Effort:** 2 hours
- Template section design: 1 hour
- Integration with story-creation skill: 45 minutes
- Testing with new story: 15 minutes

---

## Matrix Population Guidance

### How to Populate Matrix During Story Creation

**Step 1: Extract AC Requirements (Granular)**

For each AC, identify discrete testable requirements:
```markdown
AC#1: User Authentication Works

**Given** user provides valid credentials
**When** user submits login form
**Then** system authenticates user             ← Requirement 1
**And** system generates JWT token             ← Requirement 2
**And** system returns token in response       ← Requirement 3
**And** token is valid for 24 hours            ← Requirement 4
```

**Granular Requirements from AC#1:**
1. System authenticates user (auth logic)
2. System generates JWT token (token generation)
3. System returns token in response (API contract)
4. Token valid for 24 hours (expiration logic)

---

**Step 2: Create DoD Items Matching Requirements**

```markdown
## Definition of Done

### Implementation
- [ ] Authentication logic implemented (validates credentials) ← Covers Req 1
- [ ] JWT token generation implemented (RS256 algorithm) ← Covers Req 2
- [ ] API returns token in response payload ← Covers Req 3
- [ ] Token expiration set to 24 hours ← Covers Req 4
```

---

**Step 3: Fill Matrix Table**

| AC | Requirement | DoD Item | Validation Type | Evidence |
|----|-------------|----------|-----------------|----------|
| AC#1 | System authenticates user | Implementation #1: "Authentication logic implemented" | Explicit Checkbox | src/services/AuthService.cs:authenticateUser() |
| AC#1 | Generates JWT token | Implementation #2: "JWT token generation implemented (RS256)" | Explicit Checkbox | src/services/TokenService.cs:generateToken() |
| AC#1 | Returns token in response | Implementation #3: "API returns token in response payload" | Explicit Checkbox | API contract: POST /auth/login → {token} |
| AC#1 | Token valid 24 hours | Implementation #4: "Token expiration set to 24 hours" | Explicit Checkbox | Token.ExpiresAt = Now + 24h |

**Traceability Score:** 4/4 requirements covered = 100%

---

## Example Matrices by Story Type

### Example 1: API Development Story

**AC Requirements:**
```
AC#1: GET /api/users/{id} returns user data
  Req 1: Endpoint accepts user ID parameter
  Req 2: Returns 200 with user JSON {id, email, name}
  Req 3: Returns 404 if user not found
  Req 4: Requires authentication (Bearer token)
  Req 5: Response time <200ms (p95)
```

**Traceability Matrix:**

| AC | Requirement | DoD Item | Validation Type | Evidence |
|----|-------------|----------|-----------------|----------|
| AC#1 | Endpoint accepts user ID | Implementation: "GET /api/users/{id} endpoint created" | Explicit Checkbox | src/controllers/UserController.cs:GetUser() |
| AC#1 | Returns 200 with JSON | Implementation: "User DTO response mapping" | Explicit Checkbox | UserDTO {Id, Email, Name} |
| AC#1 | Returns 404 if not found | Testing: "Integration test: 404 handling" | Test Validation | tests/Integration/UserControllerTests.cs:GetUser_NotFound_Returns404() |
| AC#1 | Requires authentication | Implementation: "[Authorize] attribute added" | Explicit Checkbox | [Authorize] on GetUser method |
| AC#1 | Response time <200ms | Quality: "Performance validated (<200ms p95)" | Metric Validation | Load test results: 185ms p95 |

**Traceability:** 5/5 = 100%

---

### Example 2: Documentation Story (STORY-052)

**AC Requirements:**
```
AC#1: Document Completeness
  Req 1: Introduction ≥200 words
  Req 2: 11 command sections
  Req 3: 20-30 examples
  Req 4: Quick reference checklist
  Req 5: ≥10 pitfalls
  Req 6: Progressive disclosure
```

**Traceability Matrix:**

| AC | Requirement | DoD Item | Validation Type | Evidence |
|----|-------------|----------|-----------------|----------|
| AC#1 | Introduction ≥200 words | Implementation #2: "Document includes introduction (648 words)" | Explicit Checkbox | wc -w: 648 words |
| AC#1 | 11 command sections | Implementation #3: "All 11 commands have dedicated guidance sections" | Explicit Checkbox | grep "^## /" returns 11 |
| AC#1 | 20-30 examples | Implementation #4: "24 before/after examples included" | Explicit Checkbox | grep "❌ BEFORE" returns 24 |
| AC#1 | Quick reference checklist | Implementation #5: "Quick reference checklist created (in first 500 lines)" | Explicit Checkbox | head -500 contains checklist |
| AC#1 | ≥10 pitfalls | Implementation #7: "Common pitfalls section (10 pitfalls)" | Explicit Checkbox | grep "^### Pitfall" returns 10 |
| AC#1 | Progressive disclosure | Quality #6: "Document coverage 100%" | Implicit Coverage | Structure: overview → command-specific → deep dive |

**Traceability:** 6/6 = 100%

---

### Example 3: Story with Test-Based Validation

**AC Requirements:**
```
AC#2: Example Quality and Realism
  Req 1: Shows realistic user input
  Req 2: Demonstrates specific improvement
  Req 3: ≥50 words explanations per example
  Req 4: References actual commands
  Req 5: Measurable improvements
```

**Traceability Matrix:**

| AC | Requirement | DoD Item | Validation Type | Evidence |
|----|-------------|----------|-----------------|----------|
| AC#2 | Realistic user input | Testing #2: "Example validation test (AC2 - PASS)" | Test Validation | tests/STORY-052/test-example-quality.sh (validates realistic patterns) |
| AC#2 | Specific improvements | Testing #2: "Example validation test (AC2 - PASS)" | Test Validation | Test checks vague→specific, incomplete→complete patterns |
| AC#2 | ≥50 words explanations | Testing #2: "Example validation test (AC2 - PASS)" | Test Validation | Test counts words per example (wc -w validation) |
| AC#2 | References actual commands | Testing #2: "Example validation test (AC2 - PASS)" | Test Validation | Test greps for "/[a-z-]+" patterns |
| AC#2 | Measurable improvements | Testing #2: "Example validation test (AC2 - PASS)" | Test Validation | Test validates metrics like "5 questions → 0 questions" |

**Traceability:** 5/5 = 100%

**Note:** Single DoD item (one test) validates multiple AC requirements. This is efficient and acceptable (rollup validation).

---

## Matrix Patterns

### Pattern 1: One-to-One Mapping

```
AC Requirement: "API accepts user ID parameter"
  ↓
DoD Item: "- [x] Endpoint accepts userId parameter (validated via unit test)"
```

**Traceability:** Simple, direct mapping

---

### Pattern 2: One-to-Many Mapping (One AC → Multiple DoD Items)

```
AC#1: User authentication complete
  Req 1: Email validation
  Req 2: Password hashing
  Req 3: Token generation
  ↓
DoD Items:
  - [x] Email validation implemented
  - [x] Password hashing (bcrypt) implemented
  - [x] JWT token generation implemented
```

**Traceability:** Complex AC requires multiple DoD items

---

### Pattern 3: Many-to-One Mapping (Multiple ACs → One DoD Item)

```
AC#1: Feature works for valid input
AC#2: Feature handles errors
AC#3: Feature has proper logging
  ↓
DoD Item:
  - [x] All tests passing (validates AC#1, AC#2, AC#3)
```

**Traceability:** Rollup validation (one DoD item proves multiple ACs)

---

### Pattern 4: Test-Based Validation

```
AC#2: Examples are high quality
  (Multiple granular requirements: realistic, ≥50 words, measurable, etc.)
  ↓
DoD Item:
  - [x] Example validation test (AC#2 - PASS)
  ↓
Test validates all granular requirements algorithmically
```

**Traceability:** Test provides comprehensive validation

---

## How QA Phase 0.9 Uses Matrix

**IF matrix is populated:**
```
QA reads matrix table
Verifies each row has DoD item (no empty cells in "DoD Item" column)
Calculates traceability_score from matrix
Displays matrix in Phase 0.9 output
```

**IF matrix is NOT populated (empty or missing):**
```
QA generates matrix algorithmically:
  1. Extract AC requirements (parse story file)
  2. Extract DoD items (parse DoD section)
  3. Map requirements to items (keyword matching)
  4. Calculate traceability score
  5. Display generated matrix in output

User can see which requirements lack coverage
```

**Benefit:** Matrix serves as pre-validation (user catches gaps before submitting for QA)

---

## Template Enhancement Implementation

### Add Matrix Section to Template

**Location:** After "Acceptance Criteria Verification Checklist", before "Definition of Done"

**Rationale:** Logical flow:
1. Acceptance Criteria (define what to test)
2. AC Verification Checklist (granular tracking during TDD)
3. **AC-to-DoD Traceability Matrix** (map AC → DoD) ← NEW
4. Definition of Done (official completion record)

---

### Skill Integration: Auto-Populate Matrix

**Enhancement to devforgeai-story-creation skill:**

During story creation (Phase 2: Technical Specification):
```
Step 2.X: Generate AC-to-DoD Traceability Matrix

Extract AC requirements from Phase 1
Generate DoD items from technical specification (Phase 2)

FOR each ac_requirement:
  Find corresponding DoD item (keyword match)
  Determine validation type (explicit, test, metric)
  Provide evidence placeholder

Generate matrix table with all mappings

Include in story file output
```

**Benefit:** Pre-populated matrix saves user effort, ensures traceability from creation

---

## Validation of Populated Matrix

### Matrix Quality Checklist

**Valid matrix must have:**
- [ ] Row for each granular AC requirement (30 rows for STORY-052)
- [ ] DoD item identified for every requirement (no empty "DoD Item" cells)
- [ ] Validation type specified (Explicit / Test / Metric)
- [ ] Evidence provided (file, test name, metric value)
- [ ] Traceability score calculated (should be 100%)

**Invalid matrix examples:**

**Missing DoD Item:**
```
| AC#2 | Requirement X | ??? | ??? | ??? |
                        ↑ Empty - no DoD coverage identified
```
**Action:** Add DoD item or update AC

**Wrong Validation Type:**
```
| AC#1 | Performance <200ms | Implementation: Feature complete | Explicit Checkbox | ... |
                                                              ↑ Should be Metric Validation
```
**Action:** Correct validation type

---

## Benefits of Traceability Matrix

### For Story Authors

**Benefits:**
- Visual validation before submitting for QA
- Catch missing DoD items early
- Understand which DoD items validate which ACs
- Easier to write comprehensive DoD (matrix guides you)

**Example:**
"I see AC#3 has 5 requirements but only 2 DoD items. I need to add 3 more DoD items or clarify existing ones cover the requirements."

---

### For Code Reviewers

**Benefits:**
- Quick traceability verification (scan matrix table)
- Identify validation gaps at a glance
- Understand story structure faster
- Validate QA Phase 0.9 won't fail this story

**Example:**
"Matrix shows 100% traceability (30/30). DoD is comprehensive. Approve for development."

---

### For QA Validation

**Benefits:**
- Pre-populated matrix speeds up Phase 0.9 (no algorithmic generation needed)
- User has already validated traceability (self-service QA)
- Fewer QA failures due to incomplete DoD

**Metrics:**
- QA failure rate due to traceability: Expected to drop from ~15% to <5%
- Time saved: ~2 minutes per QA run (no matrix generation needed)

---

## Rollback Plan

**If matrix template causes issues:**

### Issue: Matrix confuses users (too complex)

**Resolution:**
- Make matrix optional (add "Optional:" prefix to section header)
- Provide simplified example
- Clarify: "Pre-populate if you want, or QA Phase 0.9 generates it"

---

### Issue: Auto-population generates wrong mappings

**Resolution:**
- Disable auto-population
- Provide empty matrix template
- User fills manually (or QA Phase 0.9 generates)

---

## Success Criteria

**REC-7 is successful when:**

- [ ] Matrix section added to story template v2.1
- [ ] Template includes clear usage instructions
- [ ] Example matrix provided (reference STORY-007 or STORY-052)
- [ ] Validation types documented
- [ ] Test story created includes empty matrix (ready for population)
- [ ] User understands how to populate matrix
- [ ] QA Phase 0.9 uses matrix if populated (or generates if empty)

**User Experience:**
- "Matrix helped me catch missing DoD items before QA"
- "I can see 100% traceability at a glance"
- "Understanding which DoD items validate which ACs is clearer"

---

## Related Documents

- **INDEX.md** - RCA-012 navigation
- **REMEDIATION-PLAN.md** - Phase 4 overview (REC-7)
- **SAMPLING-REPORT.md** - STORY-007 exemplar (perfect traceability)
- **QA-ENHANCEMENT.md** - How QA Phase 0.9 validates matrix
- **TESTING-PLAN.md** - Matrix validation tests

---

**REC-7 Status:** Ready for Implementation
**Effort:** 2 hours (template addition + skill integration + testing)
**Priority:** MEDIUM (enhancement for transparency)
**Impact:** Improved user experience, reduced QA failures
