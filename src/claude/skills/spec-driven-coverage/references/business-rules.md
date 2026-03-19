# Business Rules: Spec-Driven Coverage

## BR-001: Epic ID Normalization

**Rule:** Epic IDs are case-insensitive and normalized to the canonical format EPIC-NNN (uppercase, zero-padded 3-digit number).

**Enforcement:** Phase 00 (Initialization), Step 0.5

**Examples:**
- `epic-015` → `EPIC-015`
- `Epic-15` → `EPIC-015`
- `EPIC-015` → `EPIC-015` (already normalized)
- `all` → `all` (special value, no normalization)

**Validation:** After normalization, the ID must match the regex `^EPIC-[0-9]{3}$` or equal the literal string "all". Invalid IDs trigger a HALT with an error message.

---

## BR-002: Coverage Counting Rules

**Rule:** Only stories with status >= "Dev Complete" count toward coverage percentage. Stories in earlier lifecycle stages show as "Planned" but do not contribute to the coverage numerator.

**Enforcement:** Phase 01 (Gap Detection), Step 1.6

**Status Classification:**

| Status | Counts as Covered? | Display Label |
|--------|--------------------| --------------|
| Released | Yes | Covered |
| Releasing | Yes | Covered |
| QA Approved | Yes | Covered |
| QA In Progress | Yes | Covered |
| Dev Complete | Yes | Covered |
| In Development | No | Planned |
| Ready for Dev | No | Planned |
| Architecture | No | Planned |
| Backlog | No | Planned |

**Formula:**
```
coverage_percentage = (stories_with_status_gte_dev_complete / total_features) * 100
```

**Rationale:** Prevents premature coverage claims. A feature is only "covered" when its story has progressed through the full TDD cycle and reached at least Dev Complete status.

---

## BR-003: Shell-Safe Escaping

**Rule:** Feature descriptions containing quotes, backticks, or `$` must be escaped in /create-story command suggestions. Use POSIX shell single-quote wrapping with interior escaping.

**Enforcement:** Phase 03 (Display Formatting), Step 3.4

**Escaping Rules:**
1. Wrap the entire description in single quotes: `'description text'`
2. If the description contains single quotes, replace each `'` with `'\''`
3. If the description contains backticks, they are safe within single quotes
4. If the description contains `$`, it is safe within single quotes (no expansion)

**Examples:**
```
# Safe (no special characters):
/create-story "User authentication module"

# Contains single quote:
/create-story 'User'\''s profile page'

# Contains $:
/create-story 'Calculate $revenue per customer'
```

**Rationale:** Generated /create-story commands may be copy-pasted into a terminal. Unescaped special characters would cause shell errors or unintended expansion.

---

## BR-004: Batch Failure Isolation

**Rule:** During batch story creation, failure on item N does NOT prevent item N+1 from being created. Each story creation is independently wrapped in TRY/CATCH error handling.

**Enforcement:** Phase 04 (Batch Story Creation), Step 4.6

**Implementation Pattern:**
```
FOR each gap in missing_features:
    TRY:
        Invoke spec-driven-stories skill
        Verify story file created
        Record success
    CATCH:
        Record failure with error message
        Display failure notice
        Continue to next gap (DO NOT halt the batch)
```

**Failure Tracking:**
- Each failure is recorded with: feature_title, error message
- Failed items are listed in the completion summary (Phase 05) with recovery commands
- Recovery commands are individual /create-story invocations for manual retry

**Rationale:** A single story creation failure (e.g., missing template, invalid feature description) should not block the remaining N-1 stories from being created. The user can manually retry failed items after the batch completes.
