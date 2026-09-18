---
template_version: 1.0
format_version: 1.0
story_id: STORY-660
generated_at: "2026-05-08T10:00:00Z"
generated_by: devforgeai-validate generate-qa-recommendations
---

<!-- SECTION_MANIFEST
# FIXTURE NOTE: This is a synthetic test story. File paths under `src/lib/` and
# `tests/STORY-660/` are illustrative — they do not exist in the live tree.
# Verification commands will fail if executed against the real repo.
# Eval scope grades skill behavior (drafting, idempotency, labels) — not
# whether the rec applies to real source.
#
# (manifest abbreviated for fixture — see STORY-661 fixture for full schema)
END_SECTION_MANIFEST -->

# QA Recommendations — STORY-660 (Idempotency-Detection Fixture)

**Note:** This fixture is for skill-creator eval-2 testing. REC-STORY-660-L-001 already
has a `**Posted as:** Issue-42` marker (simulating a prior `/create-incident-from-recommendations`
run). REC-STORY-660-M-001 is new and unposted. The skill must detect the L-001 marker
in idempotency check (Phase 1.5) and prompt the user.

**Synthetic paths warning:** `src/lib/db_query.py`, `src/lib/helpers.py`, and
`tests/STORY-660/test_sql_injection.py` are FABRICATED paths used only to give
the eval a coherent shape. Do NOT execute the verification commands against the
live repo — they will fail with file-not-found. The eval grades the skill's
drafting/idempotency logic, not the underlying code.

## Summary

| Severity | Count |
|----------|-------|
| MEDIUM   | 1     |
| LOW      | 1     |

## Advisory Recommendations

### REC-STORY-660-L-001 (PREVIOUSLY POSTED)

**Posted as:** Issue-42 — https://github.com/bankielewicz/DevForgeAI/issues/42

```yaml
- id: "REC-STORY-660-L-001"
  severity: LOW
  provenance: GROUNDED
  title: "Add docstring to obscure_helper_function for maintainability"
  file: "src/lib/helpers.py"
  line: 88
  category: documentation
  blocking_release: false
  before_code: null
  after_code: null
  remediation_steps:
    - "Add a one-paragraph docstring explaining the function's purpose"
    - "Document the parameters and return value"
    - "Add a doctest example showing typical usage"
  verification:
    command: "python -c \"import src.lib.helpers; help(src.lib.helpers.obscure_helper_function)\""
    expected: "docstring printed (not 'No documentation available')"
  estimated_effort_minutes: 8
  dependencies: []
  references: []
  cycle_first_seen: 1
```

### REC-STORY-660-M-001 (NEW THIS CYCLE — unposted)

```yaml
- id: "REC-STORY-660-M-001"
  severity: MEDIUM
  provenance: GROUNDED
  title: "Replace string concatenation with parameterized SQL query"
  file: "src/lib/db_query.py"
  line: 42
  category: security
  classification: REGRESSION
  blocking_release: false
  before_code: |
    cursor.execute("SELECT * FROM users WHERE id = " + user_id)
  after_code: |
    cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
  remediation_steps: null
  verification:
    command: "pytest tests/STORY-660/test_sql_injection.py -v"
    expected: "1 passed"
  estimated_effort_minutes: 5
  dependencies: []
  references: []
  cycle_first_seen: 2
```

## Verification Plan

| REC ID                  | Command                                          | Expected          |
|-------------------------|--------------------------------------------------|-------------------|
| REC-STORY-660-L-001     | python -c "import src.lib.helpers; help(...)"    | docstring printed |
| REC-STORY-660-M-001     | pytest tests/STORY-660/test_sql_injection.py -v  | 1 passed          |

## Provenance Summary

| Provenance   | Count |
|--------------|-------|
| GROUNDED     | 2     |
| DERIVED      | 0     |
| INCONCLUSIVE | 0     |
