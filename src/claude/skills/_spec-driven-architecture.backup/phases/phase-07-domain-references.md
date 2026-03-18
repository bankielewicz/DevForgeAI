# Phase 07: Domain References

## Contract

| Attribute | Value |
|-----------|-------|
| **PURPOSE** | Generate project-specific domain reference files derived from context files for subagent consumption |
| **REFERENCES** | `.claude/skills/designing-systems/references/domain-reference-generation.md` |
| **STEP COUNT** | 5 mandatory steps |

## Phase Exit Criteria

Before this phase can complete, ALL of the following MUST be true:
- [ ] All 4 detection heuristics executed against context files
- [ ] User presented with recommendations and responded
- [ ] Approved reference files written (or phase marked completed-no-references)
- [ ] Derivation purity verified for all generated files (100% traceable to context)
- [ ] Generated file paths recorded in checkpoint
**IF any criterion is unmet: HALT. Do NOT proceed to Phase 08.**

---

## Reference Loading [MANDATORY]

```
Read(file_path=".claude/skills/designing-systems/references/domain-reference-generation.md")
```

Do NOT rely on memory of previous reads. Load fresh every time.

---

## Mandatory Steps

### Step 7.1: Run Detection Heuristics

**EXECUTE:**
Load context files for heuristic analysis:
```
Read(file_path="devforgeai/specs/context/tech-stack.md")
Read(file_path="devforgeai/specs/context/dependencies.md")
Read(file_path="devforgeai/specs/context/architecture-constraints.md")
Read(file_path="devforgeai/specs/context/coding-standards.md")
```

Run 4 detection heuristics against loaded content:

- **DH-01: Backend Framework Detection** — Scan `tech-stack.md` for backend frameworks (Express, FastAPI, ASP.NET, Spring, etc.). Match against `dependencies.md` for confirming packages.
- **DH-02: Frontend Framework Detection** — Scan `tech-stack.md` for frontend frameworks (React, Vue, Angular, Svelte, etc.). Match against `dependencies.md` for confirming packages.
- **DH-03: Database Pattern Detection** — Scan `tech-stack.md` for database technologies (PostgreSQL, MongoDB, Redis, etc.). Cross-reference `architecture-constraints.md` for data access patterns (Repository, ORM, raw SQL).
- **DH-04: Testing Framework Detection** — Scan `tech-stack.md` and `coding-standards.md` for testing frameworks (Jest, pytest, xUnit, Mocha, etc.). Identify test structure conventions.

**VERIFY:**
- All 4 heuristics executed (each produced a match/no-match result)
- At least 1 heuristic produced a match (if zero matches, project may lack context — log warning)
- Each match includes: framework name, source file, source line numbers

**RECORD:**
```json
checkpoint.phase_07.step_7_1 = {
  "heuristics_run": 4,
  "matches": {
    "DH-01_backend": { "matched": <boolean>, "framework": "<name_or_null>", "source": "<file:line>" },
    "DH-02_frontend": { "matched": <boolean>, "framework": "<name_or_null>", "source": "<file:line>" },
    "DH-03_database": { "matched": <boolean>, "technology": "<name_or_null>", "source": "<file:line>" },
    "DH-04_testing": { "matched": <boolean>, "framework": "<name_or_null>", "source": "<file:line>" }
  },
  "total_matches": <count>
}
```

---

### Step 7.2: Present Recommendations

**EXECUTE:**
Build recommendation list from heuristic matches. Only include matched heuristics.
```
AskUserQuestion(
  question="Based on your project's context files, the following domain reference files are recommended:\n\n<for each match>\n  - [DH-NN] project-<domain>.md — <framework> patterns derived from <source_file>\n</for each>\n\nThese files help subagents understand your project's specific patterns. Select which to generate.",
  options=[
    { "label": "Generate all recommended", "description": "Create all <N> reference files" },
    { "label": "Select individually", "description": "Choose which references to generate" },
    { "label": "Skip all", "description": "No domain references needed" }
  ]
)
```
If user selects "Select individually," present each reference as a separate yes/no question.
If user selects "Skip all," mark phase as `completed-no-references` and skip to Step 7.5.

**VERIFY:**
- User response received and is non-empty
- Approved list of references determined (may be empty if user skipped all)

**RECORD:**
```json
checkpoint.phase_07.step_7_2 = {
  "recommendations_presented": <count>,
  "user_decision": "generate_all" | "select_individually" | "skip_all",
  "approved_references": ["project-backend.md", "project-frontend.md", ...],
  "skipped_references": [...]
}
```

---

### Step 7.3: Generate Reference Files

**EXECUTE:**
For each approved reference file:
1. Extract relevant content from context files (tech-stack.md, dependencies.md, architecture-constraints.md, coding-standards.md)
2. Synthesize into a structured reference document with sections: Overview, Patterns, Constraints, Testing Conventions
3. Write the file:
```
Write(
  file_path="devforgeai/specs/context/project-<domain>.md",
  content=<synthesized reference content>
)
```

Content MUST be 100% derived from existing context files. Do NOT inject patterns, conventions, or recommendations not found in the project's context files.

**VERIFY:**
- Each approved file written successfully
- `Glob(pattern="devforgeai/specs/context/project-*.md")` returns all expected files
- File content is non-empty

**RECORD:**
```json
checkpoint.phase_07.step_7_3 = {
  "files_generated": <count>,
  "file_paths": ["devforgeai/specs/context/project-backend.md", ...],
  "generation_status": { "<filename>": "written" | "failed" }
}
```

---

### Step 7.4: Verify Derivation Purity

**EXECUTE:**
For each generated reference file:
1. Read the generated file
2. For each substantive claim or pattern statement in the file:
   - `Grep(pattern="<key phrase>", path="devforgeai/specs/context/")` across the 6 original context files
   - Confirm the claim traces back to a source line
3. If any content is NOT traceable to context files:
   ```
   AskUserQuestion(
     question="The following content in <file> could not be traced to any context file:\n\n  '<untraceable_content>'\n\nThis may be hallucinated. Options:",
     options=[
       { "label": "Approve — content is correct", "description": "Keep the content as-is" },
       { "label": "Remove — delete untraceable content", "description": "Edit file to remove this section" },
       { "label": "Add source — update context file", "description": "Add this as new content to a context file first" }
     ]
   )
   ```

**VERIFY:**
- Every generated file has been purity-checked
- Untraceable content either approved by user, removed, or sourced
- No silently hallucinated patterns remain

**RECORD:**
```json
checkpoint.phase_07.step_7_4 = {
  "files_checked": <count>,
  "traceable_claims": <count>,
  "untraceable_claims": <count>,
  "untraceable_resolved": { "approved": <n>, "removed": <n>, "sourced": <n> },
  "purity_score": "<percentage>%"
}
```

---

### Step 7.5: Report Generated Files

**EXECUTE:**
Display summary of all generated reference files:
```
For each generated file:
  - Path: devforgeai/specs/context/project-<domain>.md
  - Source heuristic: DH-NN
  - Line count: <N>
  - Purity: <percentage>%
```

**VERIFY:**
- Summary displayed with correct file paths
- All paths are absolute or project-relative and valid
- Checkpoint fully populated for this phase

**RECORD:**
```json
checkpoint.phase_07.step_7_5 = {
  "phase_status": "completed" | "completed-no-references",
  "files_generated_total": <count>,
  "files_with_full_purity": <count>,
  "summary_displayed": true
}
```

---

## Phase Transition Display

```
============================================================
  PHASE 07 COMPLETE: Domain References
============================================================
  Heuristics matched:      <N>/4
  References recommended:  <N>
  References generated:    <N>
  Derivation purity:       <percentage>% average
  Phase status:            [COMPLETED/COMPLETED-NO-REFERENCES]
------------------------------------------------------------
  Proceeding to Phase 08: Architecture Review
============================================================
```
