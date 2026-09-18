# Display Templates

**Purpose:** Markdown display templates for the dev-result-interpreter subagent. Loaded via `Read()` from Step 6 of the core agent file.

---

## Template Selection

Each template includes:
1. Title with status emoji (&#x2705;/&#x26A0;&#xFE0F;/&#x274C;)
2. Story identification (ID, title, points)
3. Workflow summary (phases completed, tests passing)
4. DoD completion status (completed/total items)
5. Next steps (based on result)
6. Link to story file for details

---

## Success Template (&#x2705;)

```markdown
# Success Template (✅)
## ✅ Development Complete - {STORY_ID}: {TITLE}

**Story:** {STORY_ID} ({POINTS} points, {PRIORITY} priority)
**Workflow Status:** Completed ✓
**Final Status:** Dev Complete

### TDD Phases Completed

✓ Phase 0: Pre-Flight Validation
  - Git status verified
  - Context files validated
  - Tech stack detected

✓ Phase 1: Red Phase (Test Generation)
  - {N} acceptance criteria tests created
  - {N} unit tests generated
  - All tests failing (expected for TDD)

✓ Phase 2: Green Phase (Implementation)
  - Implementation code written
  - All {N}/{N} tests passing ✓
  - Code coverage: {COVERAGE}%

✓ Phase 3: Refactor Phase (Quality)
  - Code quality improved
  - Complexity reduced
  - Code review performed

✓ Phase 4: Integration Phase
  - Cross-component tests added
  - Integration verified
  - All scenarios passing

✓ Phase 5: Deferral Challenge
  - All DoD items reviewed
  - No deferrals found (or all justified and approved)

✓ Phase 6: Git Workflow
  - Changes committed: {HASH}
  - Branch: {BRANCH}
  - Files changed: {N}, Lines added: {N}, Deleted: {N}

### Quality Metrics

**Test Results:**
- Total tests: {N}
- Passing: {N} ✓
- Failing: 0
- Coverage: {COVERAGE}%

**Code Quality:**
- Complexity: {AVG} avg (max allowed: 10)
- Duplication: {DUP}% (threshold: <5%)
- Issues detected: 0

### Definition of Done

✓ All {N} DoD items completed:
{FOR each completed item:}
  ✓ {Item name}

### Recommendations

✅ **READY FOR QA**

Story has completed all development phases and met quality standards.

**Next Steps:**
1. Run: `/qa {STORY_ID}` for quality validation
2. If QA passes: `/release {STORY_ID}` to deploy
3. If QA has issues: `/dev {STORY_ID}` to fix and re-validate

---
```

---

## Incomplete - High Progress Template (&#x26A0;&#xFE0F;)

```markdown
# Incomplete - High Progress Template (⚠️)
## ⚠️ Development In Progress - {STORY_ID}: {TITLE}

**Story:** {STORY_ID} ({POINTS} points, {PRIORITY} priority)
**Workflow Status:** In Progress
**Completion:** {PERCENT}% ({COMPLETED}/{TOTAL} DoD items)

### Phases Completed

✓ Phase 0: Pre-Flight ✓
✓ Phase 1: Red (Tests) ✓
✓ Phase 2: Green (Implementation) ✓
⏳ Phase 3: Refactor (In Progress)
  - Current: Code quality improvements
  - Tests passing: {N}/{N}
  - Coverage: {COVERAGE}%

### DoD Completion Status

**Completed Items ({COMPLETED}/{TOTAL}):**
{List first 5 [✓] items}
...

**Remaining Items ({REMAINING}/{TOTAL}):**
{List [□] items:}
- [ ] {Item 1}
- [ ] {Item 2}
- [ ] {Item 3}

### Recommendations

**Continue Development:**
- Run: `/dev {STORY_ID}` to resume where workflow left off
- Workflow will auto-detect completed phases and continue from next phase
- Target: Complete remaining {REMAINING} DoD items

**Estimated Effort:**
- {N} hours remaining (based on item complexity)
- {DAYS} days to completion

---
```

---

## Incomplete - Deferrals Template (&#x26A0;&#xFE0F;)

```markdown
# Incomplete - Deferrals Template (⚠️)
## ⚠️ Development with Deferrals - {STORY_ID}: {TITLE}

**Story:** {STORY_ID}
**Status:** In Development
**Completed DoD:** {COMPLETED}/{TOTAL} ({PERCENT}%)
**Deferred Items:** {DEFERRED_COUNT}

### DoD Completion

✓ Completed Items ({COMPLETED}/{TOTAL}):
{List completed items}

→ Deferred Items ({DEFERRED_COUNT}):
{FOR each deferred item:}
- **{Item name}** - Reason: {Deferral reason}
  - Blocker: {Blocker type}
  - Workaround: {If applicable}
  - Follow-up story: {Reference story if created}

### Impact Assessment

**Completion:** {PERCENT}%

**Deferrals by Type:**
- Critical blockers: {COUNT}
- Valid dependencies: {COUNT}
- Complexity deferrals: {COUNT}

### Resolution Path

Choose one approach:

**Option 1: Continue Development** (Recommended)
- Run: `/dev {STORY_ID}` to resume
- Workflow will re-evaluate deferrals
- Use deferral-validator to justify/resolve

**Option 2: Accept Current Deferrals**
- Run: `/qa {STORY_ID}` for QA validation
- QA will review deferral justifications
- May block QA approval if invalid

**Option 3: Create Follow-up Stories**
- For each deferral, create tracking story
- Link in current story's Implementation Notes
- Can proceed to QA once deferrals documented

---
```

---

## Failure Template (&#x274C;)

```markdown
# Failure Template (❌)
## ❌ Development Workflow Failed - {STORY_ID}

**Story:** {STORY_ID}: {TITLE}
**Status:** Failed
**Last Completed Phase:** {Phase name}

### Error Details

**Error Type:** {Type: Execution failure, Deferral blocker, Validation failure}

**Error Message:**
{Error description from Implementation Notes}

**Where It Occurred:**
- Phase: {Phase name}
- Step: {Step description}
- Context: {Brief context}

### Diagnosis

**Completed Progress:**
- Phases: {List completed phases}
- DoD Items: {COMPLETED}/{TOTAL} ({PERCENT}%)
- Code Status: {Status description}

**What Failed:**
- {Specific issue}
- {Related issue}

### Recovery Steps

**Option 1: Retry Development** (Recommended)
- Run: `/dev {STORY_ID}`
- Workflow will detect previous progress
- Continue from next incomplete phase
- Fix encountered issue this time

**Option 2: Manual Investigation**
- Review error details above
- Check story file: devforgeai/specs/Stories/{STORY_ID}.story.md
- Look for Implementation Notes section (error context)
- Fix root cause manually
- Run: `/dev {STORY_ID}` to resume

**Option 3: Start Over**
- Review original acceptance criteria
- Manually reset Implementation Notes
- Run: `/dev {STORY_ID}` fresh
- Warns: Will overwrite previous work

**Recommended:** Option 1 (Retry) - preserves progress and fixes issue

---
```
