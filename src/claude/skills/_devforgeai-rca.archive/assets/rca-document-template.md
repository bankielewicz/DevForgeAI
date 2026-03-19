# RCA-{NUMBER}: {TITLE}

**Date:** {DATE}
**Reported By:** {REPORTER}
**Affected Component:** {COMPONENT}
**Severity:** {SEVERITY}

---

## Issue Description

{ISSUE_DESCRIPTION}

> Must include: What happened, When, Where, Expected vs Actual, Impact.

---

## 5 Whys Analysis

**Issue:** {ISSUE_STATEMENT}

1. **Why did this happen?**
   - {ANSWER_1}
   - **Evidence:** {file_path}:{line_range} — {brief quote}

2. **Why did {cause 1} occur?**
   - {ANSWER_2}
   - **Evidence:** {file_path}:{line_range} — {brief quote}

3. **Why did {cause 2} occur?**
   - {ANSWER_3}
   - **Evidence:** {file_path}:{line_range} — {brief quote}

4. **Why did {cause 3} occur?**
   - {ANSWER_4}
   - **Evidence:** {file_path}:{line_range} — {brief quote}

5. **Why did {cause 4} occur?**
   - **ROOT CAUSE:** {ROOT_CAUSE}
   - **Evidence:** {file_path}:{line_range} — {brief quote}

---

## Evidence Collected

> Populate per evidence-section-template.md. Minimum 3 files, each with
> significance rating and Why # linkage.

{EVIDENCE_SECTION}

---

## Codebase Context Snapshot

> Captures relevant source code so a fresh session can understand the
> codebase without needing to Read files. Include ONLY code referenced
> by recommendations.

### Module Hierarchy (Relevant Subset)

```
{MODULE_HIERARCHY_SUBSET}
```

### Key Type Definitions

```{language}
{STRUCT_AND_ENUM_DEFINITIONS}
```

### Key Function Signatures

```{language}
{FUNCTION_SIGNATURES_WITH_DOC_COMMENTS}
```

---

## Applicable Architecture Constraints

> Cited from devforgeai/specs/context/ files. Every recommendation that
> modifies source code MUST reference the constraints it must satisfy.

{FOR_EACH_RELEVANT_CONSTRAINT}
- **{constraint_name}** — {description} (Source: {context_file}, lines {N}-{M})
{END_FOR_EACH}

---

## Recommendations (Evidence-Based)

> Each recommendation uses the structured format from recommendation-template.md.
> Header format MUST be: ### REC-N: PRIORITY - Title
> (This is parsed by /create-stories-from-rca)

{FOR_EACH_RECOMMENDATION}

### REC-{N}: {PRIORITY} - {TITLE}

**Addresses:** Why #{WHY_NUMBER} — "{quoted why answer}"
**Conditional:** {YES: "Only if {condition}" | NO: "Always implement"}

{All sections from recommendation-template.md inlined here}

{END_FOR_EACH}

---

## Implementation Checklist

- [ ] Review all recommendations
- [ ] Implement REC-N for each CRITICAL/HIGH item
- [ ] Create stories via `/create-stories-from-rca RCA-{NUMBER}`
- [ ] Add regression tests
- [ ] Update documentation (if pattern change)
- [ ] Mark RCA as RESOLVED after verification

---

## Prevention Strategy

**Short-term (Immediate):**
{SHORT_TERM_ACTIONS}

**Long-term (Framework Enhancement):**
{LONG_TERM_ACTIONS}

**Monitoring:**
- Watch for: {specific error pattern}
- Track: {metric or frequency}
- Threshold: {when to escalate — concrete number}
- Audit: {periodic check with frequency}

---

## Related RCAs

{RELATED_RCAS}
