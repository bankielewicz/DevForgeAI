# Phase 07: Specification Validation

**Purpose:** Comprehensive validation of generated UI specification with user-driven issue resolution.

**Core Principle:** "Ask, Don't Assume" — Never auto-fix. All issues presented to user for resolution.

**Pre-Flight:** Verify Phase 06 completed.

---

## Reference Loading [MANDATORY]

```
Read(file_path=".claude/skills/spec-driven-design/references/specification-validation.md")
Read(file_path=".claude/skills/spec-driven-design/references/design-source-of-truth-schema.md")
Read(file_path="devforgeai/specs/context/tech-stack.md")
Read(file_path="devforgeai/specs/context/dependencies.md")
Read(file_path="devforgeai/specs/context/anti-patterns.md")
```

IF any Read fails: HALT -- "Phase 07 reference files not loaded."

---

## Step 7.1: Load Specification Validation Reference

**EXECUTE:**
```
Read(file_path=".claude/skills/spec-driven-design/references/specification-validation.md")
```

**VERIFY:**
- File content loaded into context
- Content contains validation checklist

**RECORD:**
```
Bash(command="devforgeai-validate phase-record ${IDENTIFIER} ${WORKFLOW_FLAG} --phase=07 --step=7.1 --project-root=. 2>&1")
```

---

## Step 7.2: Completeness Check

**EXECUTE:**
Read the generated spec and validate these 10 required sections exist:
1. Component hierarchy
2. Props/API documented
3. State management approach
4. Styling approach
5. Accessibility considerations
6. Responsive behavior
7. Test strategy
8. Usage examples
9. Integration instructions
10. Dependencies listed

Record which sections are present and which are missing.

**VERIFY:**
- All 10 sections checked
- Missing sections list compiled

**RECORD:**
```
Bash(command="devforgeai-validate phase-record ${IDENTIFIER} ${WORKFLOW_FLAG} --phase=07 --step=7.2 --project-root=. 2>&1")
```

---

## Step 7.3: Placeholder Detection

**EXECUTE:**
```
Grep(pattern="TODO|TBD|FILL IN|PLACEHOLDER|FIXME", path="${OUTPUT_PATH}", output_mode="content")
```

Record all placeholders with line numbers.

**VERIFY:**
- Grep completed (even if no matches)
- Placeholder list compiled (may be empty — that's valid)

**RECORD:**
```
Bash(command="devforgeai-validate phase-record ${IDENTIFIER} ${WORKFLOW_FLAG} --phase=07 --step=7.3 --project-root=. 2>&1")
```

---

## Step 7.4: Framework Constraint Validation

**EXECUTE:**
Read and validate against context files:
```
Read(file_path="devforgeai/specs/context/tech-stack.md")
Read(file_path="devforgeai/specs/context/source-tree/governance.json")
Read(file_path="devforgeai/specs/context/dependencies.md")
Read(file_path="devforgeai/specs/context/anti-patterns.md")
```

Check:
- Technology used matches tech-stack.md approved list
- File location matches source-tree/ patterns
- Dependencies are in dependencies.md approved list
- No forbidden anti-patterns present (God Objects, hardcoded values, etc.)

Compile validation summary with severity levels: HIGH / MEDIUM / LOW.

**VERIFY:**
- All 4 context files read
- Validation summary compiled with severity ratings

**RECORD:**
```
Bash(command="devforgeai-validate phase-record ${IDENTIFIER} ${WORKFLOW_FLAG} --phase=07 --step=7.4 --project-root=. 2>&1")
```

---

## Step 7.5: User Resolution of Issues

**EXECUTE:**
For each category of issues found, present to user via AskUserQuestion:

**Missing sections (if any):**
```
AskUserQuestion:
  Question: "The following spec sections are missing: [list]. How should I handle them?"
  Header: "Missing Sections"
  Options:
    - label: "Add with defaults"
      description: "I'll generate reasonable defaults for missing sections"
    - label: "Regenerate"
      description: "Regenerate the component with all sections"
  multiSelect: false
```

**Placeholders (if any):**
```
AskUserQuestion:
  Question: "Found ${COUNT} placeholders in the generated code. How should I handle them?"
  Header: "Placeholders"
  Options:
    - label: "Resolve now"
      description: "I'll help fill in each placeholder"
  multiSelect: false
```

**Framework violations (if any):**
```
AskUserQuestion:
  Question: "Found constraint violations: [summary]. How should I proceed?"
  Header: "Violations"
  Options:
    - label: "Fix now"
      description: "Apply fixes to resolve violations"
    - label: "Show detailed report"
      description: "Display full violation details"
  multiSelect: false
```

Apply user decisions.

**VERIFY:**
- All issue categories presented to user (or skipped if no issues)
- User decisions captured and applied

**RECORD:**
```
Bash(command="devforgeai-validate phase-record ${IDENTIFIER} ${WORKFLOW_FLAG} --phase=07 --step=7.5 --project-root=. 2>&1")
```

---

## Step 7.6: Design Source of Truth Validation

**EXECUTE:**

1. Bind the canonical document path:

```
DESIGN_MD = "devforgeai/specs/ui/design.md"
```

2. For generated `story` and `standalone` modes, require `DESIGN_MD` to be
a regular, non-empty file. Missing or empty generated output is a blocking
failure; do not record Step 7.6.

3. If `DESIGN_MD` exists, run the shipped mode-aware validator:

```
Bash(command="python3 ${CLAUDE_SKILL_DIR}/scripts/validate_design_md.py devforgeai/specs/ui/design.md --mode=${MODE} 2>&1")
```

IF exit code != 0: Read the validator output, fix the reported failures, and
re-run until exit code = 0.

4. For generated `story` and `standalone` modes, require the validator output
to include a passing `schema_1_1_contract` with `schema_version: "1.1"`.
Schema 1.0 is downstream read compatibility only and is not valid newly
generated output.

5. For `extract`, validate `DESIGN_MD` with `--mode=extract` when the file
is supplied. An absent extract document is inapplicable; schema-1.0 reads remain
compatible and are never rewritten.

**VERIFY:**
- Generated `story` / `standalone` `design.md` exists and is non-empty
- The shipped `validate_design_md.py` completed with `--mode=${MODE}`
- Generated output passed the schema-1.1 contract
- Schema-1.0 handling is limited to downstream read compatibility

**RECORD:**
```
Bash(command="devforgeai-validate phase-record ${IDENTIFIER} ${WORKFLOW_FLAG} --phase=07 --step=7.6 --project-root=. 2>&1")
```
---

## Step 7.7: Design Source of Truth User Resolution

**EXECUTE:**

IF design.md validation found CRITICAL or WARNING issues:

```
AskUserQuestion:
  Question: "Design Source of Truth (design.md) validation found issues: [summary]. How should I handle them?"
  Header: "design.md"
  Options:
    - label: "Fix now"
      description: "Resolve all issues in design.md"
    - label: "Regenerate design.md"
      description: "Re-run Phase 06 Step 6.2.5 to regenerate the document"
  multiSelect: false
```

Apply user's chosen resolution.

IF no issues: Skip this step.

**VERIFY:**
- User decision captured and applied (or no issues to resolve)

**RECORD:**
```
Bash(command="devforgeai-validate phase-record ${IDENTIFIER} ${WORKFLOW_FLAG} --phase=07 --step=7.7 --project-root=. 2>&1")
```

---

## Step 7.8: Determine Final Validation Status

**EXECUTE:**
Based on ALL validation results (spec completeness + placeholder + framework constraints + design.md) and user decisions:

```
IF no issues OR all issues resolved:
    STATUS = "SUCCESS"
ELIF user accepted warnings / partial completion:
    STATUS = "PARTIAL"
ELIF critical violations remain unresolved:
    STATUS = "FAILED"
    HALT — "Specification validation failed. Critical issues remain unresolved."
```

Display final status to user, including design.md status:
- design.md generated: YES/NO
- design.md validation: PASSED/WARNING/FAILED/N-A

**VERIFY:**
- STATUS is one of: SUCCESS, PARTIAL, FAILED
- If FAILED: Workflow halts with error message

**RECORD:**
```
Bash(command="devforgeai-validate phase-record ${IDENTIFIER} ${WORKFLOW_FLAG} --phase=07 --step=7.8 --project-root=. 2>&1")
```

---

## Step 7.9: Deterministic Web Artifact Lint

**EXECUTE:**

```
IF MODE == "extract":
    Read the CLI-owned design-extract state.
    IF web_artifact_path is absent:
        SKIP 7.9 as inapplicable. Do not inspect other discovered HTML files.
    ELSE:
        Run lint_design_artifact.py against exactly web_artifact_path with --format=json.
        Write stdout bytes to devforgeai/specs/ui/extract-lint.json.
        Fix/re-run only when the user explicitly authorizes changes to the supplied artifact;
        extract itself never rewrites the artifact.
        Require exit 0 and zero P0 findings.
        Bash(command="devforgeai-validate phase-record ${IDENTIFIER} ${WORKFLOW_FLAG} --phase=07 --step=7.9 --artifact=devforgeai/specs/ui/extract-lint.json --project-root=. 2>&1")
        SKIP 7.10-7.13. Extract never renders, never jury-scores, and never writes review data.
ELIF PLATFORM == "web":
    Bash(command="python3 ${CLAUDE_SKILL_DIR}/scripts/lint_design_artifact.py devforgeai/specs/ui/artifact.html --format=json > devforgeai/specs/ui/design-lint.json")
    Fix every P0 and re-run until exit 0 and P0 is empty.
    Bash(command="devforgeai-validate phase-record ${IDENTIFIER} ${WORKFLOW_FLAG} --phase=07 --step=7.9 --project-root=. 2>&1")
ELSE:
    SKIP 7.9-7.13 as inapplicable to GUI/TUI generation.
```

**VERIFY:** The lint report binds the exact artifact SHA-256 and contains zero P0 findings.

---

## Step 7.10: Capture Desktop and Mobile Renders

Web story/standalone only. Execute the local renderer; missing Playwright or Chromium blocks.

```
Bash(command="python3 ${CLAUDE_SKILL_DIR}/scripts/capture_design_artifact.py devforgeai/specs/ui/artifact.html --output-dir devforgeai/specs/ui/render --format=json")
Bash(command="devforgeai-validate phase-record ${IDENTIFIER} ${WORKFLOW_FLAG} --phase=07 --step=7.10 --project-root=. 2>&1")
```

Require `desktop.png`, `mobile.png`, and `render-manifest.json` with no console, page, or request errors.

---

## Step 7.11: Execute the Inline Design Jury

Web story/standalone only.

```
Read(file_path="${CLAUDE_SKILL_DIR}/references/design-jury.md")
Read(file_path="${CLAUDE_SKILL_DIR}/references/design-review-contract.md")
Read(file_path="devforgeai/specs/ui/render/desktop.png")
Read(file_path="devforgeai/specs/ui/render/mobile.png")
```

Use Claude's supported local image-reading surface to inspect both images before scoring. Execute at most three rounds exactly as the jury contract defines. Do not dispatch subagents or add attestations.

**RECORD:**
```
Bash(command="devforgeai-validate phase-record ${IDENTIFIER} ${WORKFLOW_FLAG} --phase=07 --step=7.11 --project-root=. 2>&1")
```

---

## Step 7.12: Persist Review Evidence and Summary

Write `devforgeai/specs/ui/design-review.json` using the review contract. Update only the schema-1.1 `design_review` group in `design.md` from the same evidence. Label an honest degraded result `below_threshold`; never call `ship_best` gate-passed.

**RECORD:**
```
Bash(command="devforgeai-validate phase-record ${IDENTIFIER} ${WORKFLOW_FLAG} --phase=07 --step=7.12 --project-root=. 2>&1")
```

---

## Step 7.13: Validate Jury Evidence

**EXECUTE:**
```
Bash(command="python3 ${CLAUDE_SKILL_DIR}/scripts/validate_design_review.py --mode=${MODE} --artifact=devforgeai/specs/ui/artifact.html --lint=devforgeai/specs/ui/design-lint.json --render=devforgeai/specs/ui/render/render-manifest.json --review=devforgeai/specs/ui/design-review.json")
```

Only after exit 0:
```
Bash(command="devforgeai-validate phase-record ${IDENTIFIER} ${WORKFLOW_FLAG} --phase=07 --step=7.13 --project-root=. 2>&1")
```

Any malformed, tampered, inflated, or inapplicable evidence blocks completion. `below_threshold` is structurally honest but must remain visibly labelled.

---

## Phase 07 Completion

**EXECUTE:**
```
Bash(command="devforgeai-validate validate-design-phase ${IDENTIFIER} ${WORKFLOW_FLAG} --mode=${MODE} --phase=07 --project-root=. 2>&1")
Bash(command="devforgeai-validate phase-complete ${IDENTIFIER} ${WORKFLOW_FLAG} --phase=07 --project-root=. 2>&1")
```

**VERIFY:**
- Exit code 0; any non-zero result blocks completion

**NEXT:** Proceed to Phase 08 (Feedback & Completion).
