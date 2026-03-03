## Recommendation Template

> Every recommendation MUST include ALL sections below. Sections marked
> [MANDATORY] cause a HALT in Phase 6 validation if missing.

**Recommendation ID:** {REC-N}
**Title:** {Brief descriptive title}
**Priority:** {CRITICAL | HIGH | MEDIUM | LOW}

### Evidence Traceability [MANDATORY]

**Addresses:** Why #{N} — "{exact quoted text from 5 Whys answer}"
**Evidence Files:** {comma-separated list of evidence file paths supporting this recommendation}

### Conditional vs Unconditional [MANDATORY]

**Type:** {Unconditional | Conditional}
**Condition:** {if conditional: exact trigger condition | if unconditional: "Always implement — no trigger condition"}

### Problem Addressed

{Which root cause or contributing factor this fixes. Reference the Why # explicitly.}

### Current Code Context [MANDATORY for code changes]

> Quote enough current code that a fresh session understands the modification
> target WITHOUT reading the source file. Minimum 5 lines, maximum 30 lines.
> Write "N/A — documentation-only change" if no code is modified.

**File:** `{exact file path}`
**Lines:** {start}-{end}
**Language:** {rust | markdown | yaml | etc.}
```{language}
{5-30 lines of CURRENT code being modified — verbatim from source}
```

### Proposed Change

**Change Type:** {Add | Modify | Delete}

{For Add — show exact text to add with insertion point:}
**Insert after:** {description of insertion point, e.g., "line 190, after `state.save(project_root)?;`"}
```{language}
{Copy-paste ready new code/text}
```

{For Modify — show before and after:}
**Current (lines {N}-{M}):**
```{language}
{old text}
```
**Replace with:**
```{language}
{new text}
```

{For Delete — show what to remove:}
**Remove lines {N}-{M}:**
```{language}
{text to delete}
```

### Architecture Constraints [MANDATORY for .rs file changes]

> Cite each constraint from devforgeai/specs/context/ that this change must satisfy.
> Write "N/A — no Rust code changes" if only documentation is modified.

- {constraint description} (Source: {context_file}, lines {N}-{M})
- {constraint description} (Source: {context_file}, lines {N}-{M})

### Rationale

1. **Why this solution?** {mechanism}
2. **How does it prevent recurrence?** {prevention logic}
3. **Evidence supporting this:** {reference Evidence #{N} from Phase 3}
4. **Trade-offs:** {if any, or "None identified"}

### Test Specification [MANDATORY]

> Concrete test names with inputs and expected outputs.
> Forbidden: "Verify the fix works" or "Run tests and check they pass."

**Test File:** `{exact test file path}`
**Test Type:** {Unit | Integration | Manual verification}

| Test Name | Input / Setup | Expected Output / Assertion |
|-----------|--------------|---------------------------|
| `{test_function_name_1}` | {concrete input or state} | {concrete expected result} |
| `{test_function_name_2}` | {concrete input or state} | {concrete expected result} |

### Effort Estimate

**Time:** {N} hours
**Complexity:** {Low | Medium | High}
**Story Points:** {N} (1 point ≈ 4 hours)
**Dependencies:** {other REC-IDs that must be implemented first, or "None"}

### Success Criteria

- [ ] {concrete, verifiable criterion 1}
- [ ] {concrete, verifiable criterion 2}
- [ ] {concrete, verifiable criterion 3}

### Impact

**Benefit:** {what improves}
**Risk:** {what could go wrong, how to mitigate}
**Scope:** {files affected count, workflows affected}
