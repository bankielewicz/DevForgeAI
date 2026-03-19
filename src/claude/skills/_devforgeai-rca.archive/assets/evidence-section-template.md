## Evidence Collection Template

> **Minimums:** 3+ files examined. Each excerpt 5-30 lines with line numbers.
> **Rating:** Each finding rated CRITICAL / HIGH / MEDIUM significance.
> **Traceability:** Each finding linked to the Why # it supports.

### Files Examined

**Evidence {N}: `{absolute_file_path}`**
- **Lines examined:** {start}-{end}
- **Significance:** {CRITICAL | HIGH | MEDIUM}
- **Finding:** {what was discovered — 1-2 sentences}
- **Supports:** Why #{N} — "{brief quote from the Why answer this evidence backs}"
- **Excerpt** ({line_count} lines):
  ```{language}
  // Lines {start}-{end} of {filename}
  {5-30 lines of verbatim code/text}
  ```

> Repeat for each file. Minimum 3 evidence entries.

### Evidence Summary Table

| # | File | Lines | Significance | Supports Why # |
|---|------|-------|-------------|----------------|
| 1 | `{path}` | {range} | {CRITICAL/HIGH/MEDIUM} | #{N} |
| 2 | `{path}` | {range} | {CRITICAL/HIGH/MEDIUM} | #{N} |
| 3 | `{path}` | {range} | {CRITICAL/HIGH/MEDIUM} | #{N} |

### Context Files Validation

**Files checked:**
- [ ] tech-stack.md - {PASS | FAIL: violation description | N/A}
- [ ] source-tree.md - {PASS | FAIL: violation description | N/A}
- [ ] dependencies.md - {PASS | FAIL: violation description | N/A}
- [ ] coding-standards.md - {PASS | FAIL: violation description | N/A}
- [ ] architecture-constraints.md - {PASS | FAIL: violation description | N/A}
- [ ] anti-patterns.md - {PASS | FAIL: violation description | N/A}

**Violations found:** {list or "None"}

### Workflow State Analysis

**Expected state:** {what should have happened}
**Actual state:** {what actually happened}
**Discrepancy:** {gap between expected and actual}
