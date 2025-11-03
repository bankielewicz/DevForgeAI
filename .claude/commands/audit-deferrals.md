---
description: Audit all QA Approved stories for invalid deferrals and deferral chains
model: sonnet
---

# Audit Deferrals Command

Audit all QA Approved and Released stories for invalid deferrals, multi-level deferral chains, and missing ADR documentation.

**Purpose:** Identify systemic deferral issues across all completed stories to catch protocol violations and technical debt.

**Created:** RCA-007 Recommendation 4

---

## Workflow

### Phase 1: Discover QA Approved Stories

**Find all story files:**

```
Glob(pattern=".ai_docs/Stories/*.story.md")
```

**Filter to QA Approved or Released status:**

```
audit_list = []

FOR each story file:
    Read YAML frontmatter only (first 20 lines)
    Extract: id, status

    IF status == "QA Approved" OR status == "Released":
        Add to audit_list: {id, path, status}

Display: "Found {count} QA Approved/Released stories to audit"
```

---

### Phase 2: Scan for Deferrals

**Check each story for incomplete DoD items:**

```
deferred_stories = []

FOR each story in audit_list:
    Read full story content
    Search for "## Implementation Notes"

    IF "Implementation Notes" found:
        Search for "### Definition of Done Status"

        IF DoD Status found:
            Parse items (lines starting with "- [ ]" or "- [x]")

            FOR each item:
                IF item starts with "- [ ]" (incomplete):
                    Extract: item_description, deferral_reason
                    Record deferral: {
                        story_id: {id},
                        item: {item_description},
                        reason: {deferral_reason}
                    }

                    Add story to deferred_stories (if not already added)

Display: "Found {count} stories with deferrals"
```

---

### Phase 3: Validate Each Deferral

**For each story WITH deferrals, invoke deferral-validator:**

```
validation_results = {}

FOR each story in deferred_stories:
    Display: "Validating deferrals for {story_id}..."

    # Load story content into conversation
    Read(file_path=story.path)

    # Invoke deferral-validator subagent
    Task(
        subagent_type="deferral-validator",
        description="Validate deferrals for audit",
        prompt="Validate all deferred DoD items for {story_id}.

                Story loaded in conversation.

                Perform comprehensive validation:
                - Multi-level deferral chain detection (A→B→C) ← RCA-007
                - Circular deferral detection (A→B→A)
                - Referenced story validation (exists and includes work)
                - ADR requirement for scope changes
                - Technical blocker verification (external dependencies)
                - Implementation feasibility check

                Return JSON validation report with all violations."
    )

    Parse validation results
    Store results: validation_results[story_id] = {violations, summary}

    # Aggregate violations by severity
    FOR each violation in results:
        Increment: violations_by_severity[violation.severity]
```

---

### Phase 4: Aggregate Results

**Categorize findings:**

```
critical_stories = stories with CRITICAL violations
high_stories = stories with HIGH violations
medium_stories = stories with MEDIUM violations

deferral_chains = []
missing_adrs = []
invalid_references = []

FOR each story_result in validation_results:
    FOR each violation in story_result.violations:
        IF violation.type == "Multi-level deferral chain detected":
            Add to deferral_chains: {chain, stories_involved}

        IF violation.type == "Circular deferral detected":
            Add to deferral_chains: {chain, stories_involved}

        IF violation.type == "ADR reference not found":
            Add to missing_adrs: {story_id, item, expected_adr}

        IF violation.type == "Referenced story doesn't include work":
            Add to invalid_references: {story_id, referenced_story, item}
```

---

### Phase 5: Generate Audit Report

**Create comprehensive report:**

```
report_path = ".devforgeai/qa/deferral-audit-{timestamp}.md"

Write(
    file_path=report_path,
    content={audit_report_content}
)
```

**Report Template:**

```markdown
# Deferral Audit Report - {timestamp}

**Command:** `/audit-deferrals`
**Audit Date:** {date and time}
**Auditor:** DevForgeAI QA System
**Scope:** All QA Approved and Released stories

---

## Executive Summary

- **Total QA Approved/Released Stories:** {N}
- **Stories with Deferrals:** {M} ({percentage}%)
- **Stories with Violations:** {X} ({percentage}%)

**Violations by Severity:**
- **CRITICAL:** {count} violations in {story_count} stories
- **HIGH:** {count} violations in {story_count} stories
- **MEDIUM:** {count} violations in {story_count} stories
- **LOW:** {count} violations in {story_count} stories

**Audit Result:** {PASS/FAIL} ({fail_criteria})

---

## Critical Issues (Require Immediate Action)

### Multi-Level Deferral Chains ⭐ RCA-007

| Chain | Stories | Work Description | Status | Action Required |
|-------|---------|------------------|--------|-----------------|
| STORY-004 → STORY-005 → STORY-006 | 3 stories | Exit code handling | Lost (not in STORY-006) | Create ADR-XXX OR implement in STORY-006 |

**Impact:** Work deferred multiple times creates broken chains where work can be lost

**Remediation:**
- Implement work in final story (STORY-006)
- OR create ADR justifying 3-story span
- OR create new story explicitly for this work

### Circular Deferrals

| Chain | Stories | Work Description | Status | Action Required |
|-------|---------|------------------|--------|-----------------|
{List circular chains if any}

**Impact:** Infinite loops where work is never completed

**Remediation:** One story must own the work - break the cycle

---

## High Severity Issues

### Referenced Stories Missing Deferred Work

| Deferring Story | Referenced Story | Missing Work | Validated? | Action Required |
|-----------------|------------------|--------------|------------|-----------------|
{List stories where STORY-A defers to STORY-B but STORY-B doesn't include work}

**Impact:** Deferred work not tracked, likely to be forgotten

**Remediation:** Add work to referenced story acceptance criteria OR complete in original story

### Invalid Story References

| Story | Referenced | Issue | Action Required |
|-------|------------|-------|-----------------|
{List stories referencing non-existent stories}

**Impact:** Broken references, work untracked

**Remediation:** Create referenced story OR update reference OR complete in original story

---

## Medium Severity Issues

### Scope Changes Without ADR

| Story | Deferred Item | Was in Original Scope? | ADR Missing | Action Required |
|-------|---------------|------------------------|-------------|-----------------|
{List scope changes that need ADR documentation}

**Impact:** Scope changes undocumented, no audit trail

**Remediation:** Create ADR-XXX documenting why original scope changed

### External Blockers Missing ETA

| Story | Blocker | Issue | Action Required |
|-------|---------|-------|-----------------|
{List external blockers without resolution dates}

**Impact:** Unclear when work can resume

**Remediation:** Add ETA or resolution condition to deferral reason

---

## Stories Requiring Re-Validation

### Priority 1: CRITICAL Violations

1. **STORY-004** (Multi-level chain)
   - **Issue:** Deferred to STORY-005 → STORY-006 (2-hop chain)
   - **Work:** Exit code handling
   - **Status:** Lost (not in STORY-006 scope)
   - **Action:** Re-run `/qa STORY-004` after creating ADR OR implementing work

2. {Other CRITICAL stories}

### Priority 2: HIGH Violations

{List HIGH violation stories}

### Priority 3: MEDIUM Violations

{List MEDIUM violation stories}

---

## Deferral Statistics

**Overall Metrics:**
- **Deferral rate:** {M/N} = {percentage}% of QA Approved stories have deferrals
- **Invalid deferral rate:** {X/M} = {percentage}% of deferrals have violations
- **Chain detection rate:** {chains_found} deferral chains detected

**Deferral Types:**
- External blockers: {count} ({percentage}%)
- Story splits: {count} ({percentage}%)
- Scope changes: {count} ({percentage}%)

**Deferral Resolution:**
- Completed in follow-up: {count}
- Still open: {count}
- Lost/unknown: {count}

**Most Common Issues:**
1. {violation_type}: {count} occurrences
2. {violation_type}: {count} occurrences

---

## Recommended Actions

### Immediate (This Sprint)

1. **Re-validate stories with CRITICAL violations**
   - Priority: {list story IDs}
   - Command: `/qa {STORY-ID}` for each

2. **Create missing ADRs**
   - {count} scope changes need ADR documentation
   - Template: `.claude/skills/devforgeai-architecture/assets/adr-examples/ADR-EXAMPLE-006-scope-descope.md`

3. **Fix deferral chains**
   - Break multi-level chains (implement in intermediate story OR create ADR)
   - Resolve circular chains (assign work to one story)

### Short-term (Next Sprint)

4. **Review deferral policy with team**
   - Ensure developers understand when ADRs required
   - Clarify multi-level chain prohibition
   - Document lessons from audit

5. **Update story DoD validation**
   - Add ADR requirement reminders to story template
   - Emphasize no deferral chains policy

### Long-term (Quarterly)

6. **Run regular deferral audits**
   - Quarterly audits of all QA Approved stories
   - Track deferral rate trends
   - Identify systemic issues (poor estimation, scope creep)

7. **Implement deferral budget per epic**
   - Max N deferrals per epic before architectural review
   - Prevents "death by a thousand deferrals"

---

## Audit Methodology

**Validation Approach:**
- Automated via deferral-validator subagent (consistent, thorough)
- Manual validation prohibited (RCA-007 evidence shows it's insufficient)
- All stories receive same level of scrutiny

**Coverage:**
- 100% of QA Approved stories checked
- 100% of Released stories checked
- Future: Add to sprint retrospective automation

**Quality Assurance:**
- deferral-validator performs 7 substep validation
- Detects issues manual review misses
- Provides structured violation reports

---

## Phase 6: Display Summary

**Display to user:**

```
┌────────────────────────────────────────────────────────┐
│           Deferral Audit Complete                      │
└────────────────────────────────────────────────────────┘

**Scope:** {N} QA Approved/Released stories

**Findings:**
- Stories with deferrals: {M} ({percentage}%)
- Stories with violations: {X}

**Violations Detected:**
- CRITICAL: {count} (multi-level chains, circular deferrals)
- HIGH: {count} (invalid references, missing work in target)
- MEDIUM: {count} (missing ADRs, blocker missing ETA)

**Detailed Report:**
📄 .devforgeai/qa/deferral-audit-{timestamp}.md

{IF violations found}
**Action Required:**
- Re-validate {critical_count} stories with CRITICAL issues
- Create {adr_count} missing ADRs for scope changes
- Fix {chain_count} deferral chains

**Next Steps:**
1. Review detailed report
2. Prioritize corrective actions
3. Re-run `/qa {STORY-ID}` for affected stories
4. Create ADRs for scope changes

{ELSE}
✅ **All deferrals validated successfully**

No violations detected. All deferred DoD items have:
- Valid technical justification
- Proper story references (exist and include work)
- ADR approval where required
- No deferral chains detected

Deferral quality: EXCELLENT
```

---

## Usage

**Manual Invocation:**
```
> /audit-deferrals
```

**Recommended Schedule:**
- After implementing RCA-007 fixes (audit baseline)
- End of each sprint (retrospective)
- Quarterly (comprehensive audit)
- After major quality gate changes

**Expected Duration:**
- Small projects (<10 stories): 2-3 minutes
- Medium projects (10-50 stories): 5-10 minutes
- Large projects (50+ stories): 15-20 minutes

---

## Integration

**Invokes:**
- deferral-validator subagent (for each story with deferrals)

**Generates:**
- Audit report in `.devforgeai/qa/deferral-audit-{timestamp}.md`
- Violation summary by severity
- Recommended corrective actions

**Updates:**
- None (read-only audit, doesn't modify stories)

---

**Note:** This command performs comprehensive audit of deferral quality across all completed stories. Run regularly to ensure deferral validation protocol is being followed consistently.
