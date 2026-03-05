# Post-Creation Validation & Report Workflow (Phase 10)

Detailed workflow for validating context file completeness and generating the success report.

## Why This Phase Exists

A context file with TODO markers or placeholder content will cause confusing failures in every downstream workflow — stories will fail validation, QA will flag phantom violations, and developers will waste time debugging framework errors that are actually incomplete architecture. This phase catches those issues at the source.

## Step 10.1: Verify File Completeness

Check that all 6 required context files exist and contain meaningful content:

```
Glob(pattern="devforgeai/specs/context/*.md")
```

For each required file, verify:
- File exists
- File content is non-empty (>100 characters — a file with just a title and no content is effectively empty)

**Required files:**
1. `tech-stack.md`
2. `source-tree.md`
3. `dependencies.md`
4. `coding-standards.md`
5. `architecture-constraints.md`
6. `anti-patterns.md`

**If files missing:**
- Report which files are missing
- Re-invoke the relevant Phase 2 generation step for each missing file
- If re-generation fails, HALT and ask user for input

## Step 10.2: Check for Placeholder Content

Scan all context files for unresolved placeholders:

```
Grep(
  pattern="TODO|TBD|\\[FILL IN\\]|\\[TO BE DETERMINED\\]|\\[INSERT\\]|\\[PLACEHOLDER\\]",
  path="devforgeai/specs/context/",
  output_mode="content"
)
```

**If placeholders found:**
1. Report each file and line number containing placeholders
2. Use AskUserQuestion to resolve each placeholder (provide context about what information is needed)
3. Update files with the user's answers
4. Re-scan to confirm all placeholders resolved

## Step 10.3: Verify ADR Creation

```
Glob(pattern="devforgeai/specs/adrs/ADR-*.md")
```

**Expected ADRs (minimum):**
- ADR-001: Primary language selection

**Additional ADRs expected for:**
- Framework selection (if applicable)
- Database selection (if applicable)
- Any significant architectural choice made during Phases 1-5

If no ADRs exist, this indicates Phase 3 was skipped or failed — report as a warning.

## Step 10.4: Display Success Report

Generate a summary that gives the user confidence the architecture phase is complete:

```
Architecture Complete

Generated Files:
  tech-stack.md          - [N] technologies defined
  source-tree.md         - [N] layers structured
  dependencies.md        - [N] packages approved
  coding-standards.md    - [N] standards defined
  architecture-constraints.md - [N] constraints enforced
  anti-patterns.md       - [N] anti-patterns forbidden
  [design-system.md      - Design tokens and guidelines]

ADRs Created:
  ADR-001: [Decision title]
  ADR-002: [Decision title]
  [...]

Architecture Review: [PASSED / PASSED WITH CHANGES / SKIPPED]
Validation: [All checks green / N placeholders resolved]

Next Steps:
  1. Review context files in devforgeai/specs/context/
  2. Customize if needed (add project-specific constraints)
  3. Run /create-epic to define your first epic
  4. Run /create-sprint to plan your first sprint
```

To compute counts (e.g., "[N] technologies defined"), read each file and count the relevant items — technologies listed, layers defined, packages approved, etc. Approximate counts are acceptable; precision is less important than giving the user a sense of scope.

## Failure Modes

| Failure | Severity | Recovery |
|---------|----------|----------|
| Missing context file | BLOCKING | Re-invoke Phase 2 for that file |
| Placeholder content | BLOCKING | AskUserQuestion to resolve |
| No ADRs created | WARNING | Report but don't block |
| Empty file (<100 chars) | BLOCKING | Re-invoke Phase 2 for that file |
