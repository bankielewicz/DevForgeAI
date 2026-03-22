# ADR-008: Exclude Test Fixtures from Pre-Commit Story Validation

## Status
Accepted

## Date
2025-12-16

## Context

The DevForgeAI pre-commit hook validates all `*.story.md` files to ensure:
- No autonomous deferrals (DoD items marked complete without implementation)
- Implementation Notes section exists
- Valid deferral justifications

STORY-093 (Dependency Graph Enforcement) introduced test fixtures in `tests/dependency-graph/fixtures/` that use `.story.md` extension for realistic testing. These are minimal YAML frontmatter files designed to test the dependency graph analyzer, not full story documents.

### Problem
When committing test fixtures, the pre-commit hook rejects them because they lack:
- Implementation Notes section
- Full Definition of Done structure
- Complete story format

This blocks legitimate test file commits and creates friction in the TDD workflow.

## Decision

Modify the pre-commit hook to exclude files in the `tests/` directory from story validation.

### Implementation
Change line 18 in `.git/hooks/pre-commit` from:
```bash
STORY_FILES=$(git diff --cached --name-only --diff-filter=d | grep '\.story\.md$' || true)
```
To:
```bash
STORY_FILES=$(git diff --cached --name-only --diff-filter=d | grep '\.story\.md$' | grep -v '^tests/' || true)
```

## Rationale

1. **Test fixtures are not real stories** - They are minimal files containing only the YAML fields needed for unit tests (id, status, depends_on)

2. **Reproducibility** - Test fixtures must be in version control so tests run consistently across environments and in CI/CD

3. **Separation of concerns** - Real stories in `devforgeai/specs/Stories/` should be validated; test data in `tests/` should not

4. **Minimal change** - Adding `| grep -v '^tests/'` is a one-line change with clear intent

## Alternatives Considered

### 1. Rename fixtures to `.fixture.md`
- **Rejected**: Would require updating test code and conftest.py to use different extension
- Less realistic testing (real stories use `.story.md`)

### 2. Add to .gitignore
- **Rejected**: Would prevent fixtures from being committed, breaking test reproducibility

### 3. Use --no-verify for test commits
- **Rejected**: Poor practice, bypasses all validation, not sustainable

### 4. Add Implementation Notes to fixtures
- **Rejected**: Bloats test fixtures with irrelevant boilerplate, reduces clarity

## Consequences

### Positive
- Test fixtures can be committed without validation friction
- TDD workflow unblocked for STORY-093 and future stories
- Clear separation between test data and production stories

### Negative
- Malformed story files in `tests/` won't be caught (acceptable - they're test data)
- Pattern must be documented so future developers understand the exclusion

### Neutral
- Pre-commit hook file is in `.git/hooks/` (not tracked), so this change must be documented or hook installation script updated

## References
- STORY-093: Dependency Graph Enforcement with Transitive Resolution
- `.git/hooks/pre-commit`: Pre-commit validation hook
- `tests/dependency-graph/fixtures/`: Test fixture location
