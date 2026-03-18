# Phase 05: Spec Validation

## Contract

| Attribute | Value |
|-----------|-------|
| **PURPOSE** | Cross-validate all 6 context files against each other and against technical specs for internal consistency |
| **REFERENCES** | `.claude/skills/designing-systems/references/architecture-validation.md` |
| **STEP COUNT** | 5 mandatory steps |

## Phase Exit Criteria

Before this phase can complete, ALL of the following MUST be true:
- [ ] All 6 context files loaded and readable
- [ ] Technology cross-validation passed (tech-stack vs dependencies)
- [ ] Structure cross-validation passed (source-tree vs architecture-constraints)
- [ ] context-validator subagent returned structured results
- [ ] All HIGH conflicts resolved (zero unresolved HIGHs)
**IF any criterion is unmet: HALT. Do NOT proceed to Phase 06.**

---

## Reference Loading [MANDATORY]

```
Read(file_path=".claude/skills/designing-systems/references/architecture-validation.md")
```

Do NOT rely on memory of previous reads. Load fresh every time.

---

## Mandatory Steps

### Step 5.1: Load All 6 Context Files

**EXECUTE:**
```
Read(file_path="devforgeai/specs/context/tech-stack.md")
Read(file_path="devforgeai/specs/context/source-tree.md")
Read(file_path="devforgeai/specs/context/dependencies.md")
Read(file_path="devforgeai/specs/context/coding-standards.md")
Read(file_path="devforgeai/specs/context/architecture-constraints.md")
Read(file_path="devforgeai/specs/context/anti-patterns.md")
```
All 6 reads may be issued in parallel.

**VERIFY:**
- Each Read returned content (non-empty, no error)
- Exactly 6 files loaded — if any file is missing, HALT immediately

**RECORD:**
```json
checkpoint.phase_05.step_5_1 = {
  "files_loaded": ["tech-stack.md", "source-tree.md", "dependencies.md", "coding-standards.md", "architecture-constraints.md", "anti-patterns.md"],
  "file_sizes": { "<filename>": <line_count> },
  "all_present": true
}
```

---

### Step 5.2: Cross-Validate Technologies

**EXECUTE:**
- Extract all technology names from `tech-stack.md` (languages, frameworks, libraries)
- Extract all package names from `dependencies.md`
- Extract all pattern references from `architecture-constraints.md`
- Extract all standard references from `coding-standards.md`
- Compare: every technology in `tech-stack.md` MUST have a corresponding entry in `dependencies.md` (unless it is a language or platform, not a package)
- Compare: every architectural pattern in `architecture-constraints.md` MUST have corresponding coding standards in `coding-standards.md`

**VERIFY:**
- Technology-to-dependency mapping is complete (no orphaned technologies)
- Pattern-to-standard mapping is complete (no unguided patterns)
- Any mismatches recorded as conflicts with severity HIGH or MEDIUM

**RECORD:**
```json
checkpoint.phase_05.step_5_2 = {
  "tech_dependency_matches": <count>,
  "tech_dependency_mismatches": [{ "tech": "<name>", "issue": "<description>" }],
  "pattern_standard_matches": <count>,
  "pattern_standard_mismatches": [{ "pattern": "<name>", "issue": "<description>" }],
  "conflicts_found": <count>
}
```

---

### Step 5.3: Cross-Validate Structure

**EXECUTE:**
- Extract layer definitions from `source-tree.md` (directory structure, layer names)
- Extract dependency matrix from `architecture-constraints.md` (which layers may depend on which)
- Verify: every layer in `source-tree.md` appears in the dependency matrix
- Verify: every layer in the dependency matrix has a corresponding directory in `source-tree.md`
- Extract anti-pattern categories from `anti-patterns.md`
- Verify: forbidden patterns in `architecture-constraints.md` have corresponding entries in `anti-patterns.md`

**VERIFY:**
- Layer-to-matrix mapping is complete (no orphaned layers)
- Forbidden pattern coverage is complete (no undetectable forbidden patterns)
- Any mismatches recorded as conflicts

**RECORD:**
```json
checkpoint.phase_05.step_5_3 = {
  "layers_in_source_tree": <count>,
  "layers_in_dependency_matrix": <count>,
  "layer_mismatches": [{ "layer": "<name>", "issue": "<description>" }],
  "antipattern_coverage": { "covered": <count>, "uncovered": <count> },
  "conflicts_found": <count>
}
```

---

### Step 5.4: Invoke context-validator Subagent

**EXECUTE:**
```
Task(
  subagent_type="context-validator",
  prompt="Validate all 6 context files in devforgeai/specs/context/ for:
    1. Internal consistency — no file contradicts itself
    2. Cross-file consistency — no two files contradict each other
    3. Completeness — no required sections missing per schema
    4. Reference integrity — all cross-references resolve to existing content
    Return structured JSON with: file, finding, severity (HIGH/MEDIUM/LOW), evidence (line numbers)."
)
```
This is a BLOCKING task. Wait for result before proceeding.

**VERIFY:**
- Task returned a result (not error, not timeout)
- Result contains structured findings (parseable as findings list)
- Each finding has: file, finding description, severity, evidence

**RECORD:**
```json
checkpoint.phase_05.step_5_4 = {
  "subagent_invoked": true,
  "subagent_result_received": true,
  "findings_count": { "HIGH": <n>, "MEDIUM": <n>, "LOW": <n> },
  "raw_findings": [ ... ]
}
```

---

### Step 5.5: Resolve Conflicts

**EXECUTE:**
- Aggregate all conflicts from Steps 5.2, 5.3, and 5.4
- Sort by severity: HIGH first, then MEDIUM, then LOW
- For each HIGH conflict:
  ```
  AskUserQuestion(
    question="Conflict found: <description>\nFile A: <file> line <N>\nFile B: <file> line <N>\nHow should this be resolved?",
    options=[
      { "label": "Update File A", "description": "<specific change>" },
      { "label": "Update File B", "description": "<specific change>" },
      { "label": "Both are correct (explain why)" }
    ]
  )
  ```
- Apply each approved resolution via `Edit(file_path=..., old_string=..., new_string=...)`
- For MEDIUM conflicts: present as batch, allow user to defer to stories
- For LOW conflicts: log only, do not block

**VERIFY:**
- Zero HIGH conflicts remain unresolved
- All approved edits applied successfully (Edit returned without error)
- MEDIUM deferrals recorded with justification

**RECORD:**
```json
checkpoint.phase_05.step_5_5 = {
  "total_conflicts": <count>,
  "high_resolved": <count>,
  "high_remaining": 0,
  "medium_resolved": <count>,
  "medium_deferred": <count>,
  "low_logged": <count>,
  "edits_applied": [{ "file": "<path>", "change": "<summary>" }]
}
```

---

## Phase Transition Display

```
============================================================
  PHASE 05 COMPLETE: Spec Validation
============================================================
  Context files loaded:    6/6
  Technology validation:   [PASS/FAIL]
  Structure validation:    [PASS/FAIL]
  Subagent validation:     [PASS/FAIL]
  Conflicts resolved:      <N> HIGH, <M> MEDIUM
  Conflicts deferred:      <N> MEDIUM (to stories)
------------------------------------------------------------
  Proceeding to Phase 06: Prompt Alignment
============================================================
```
