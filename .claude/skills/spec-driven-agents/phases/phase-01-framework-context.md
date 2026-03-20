# Phase 01: Framework Context Loading

## Contract

| Attribute | Value |
|-----------|-------|
| **PURPOSE** | Load DevForgeAI framework references that inform agent generation |
| **REFERENCE** | `src/claude/skills/spec-driven-agents/references/framework-integration-patterns.md` |
| **STEP COUNT** | 3 mandatory steps |

## Phase Exit Criteria

Before this phase can complete, ALL of the following MUST be true:

- [ ] Framework integration patterns loaded (checkpoint.framework_context.references_loaded includes "framework-integration-patterns.md")
- [ ] Validation checklist loaded (checkpoint.framework_context.references_loaded includes "validation-checklist.md")
- [ ] Context files required determined based on mode/domain (checkpoint.framework_context.context_files_required populated)
- [ ] Checkpoint updated with phase data

---

## Reference Loading [MANDATORY]

```
Read(file_path="src/claude/skills/spec-driven-agents/references/framework-integration-patterns.md")
```

IF Read fails: HALT -- "Phase 01 reference file not loaded. Cannot proceed without framework context."

---

## Mandatory Steps

### Step 1.1: Load Framework Integration Patterns

EXECUTE:
```
Read(file_path="src/claude/skills/spec-driven-agents/references/framework-integration-patterns.md")

Extract and store:
- 6 immutable context files and their purposes
- Domain-to-context-file mapping (which domains need which context files)
- 4 quality gates with participants, checks, and actions
- 11 workflow states
- Skill integration patterns (which skills invoke which subagents)
- Token efficiency mandates (native tools 40-73% savings)
- Model selection guidelines (haiku <10K, sonnet 10-50K, opus >50K)
- Subagent naming conventions (kebab-case, domain-function pattern)
```

VERIFY: Framework integration patterns loaded. At minimum: context file list extracted, domain mapping available, quality gates known.
IF content is empty or Read failed: HALT -- "Step 1.1: Framework integration patterns not loaded."

RECORD: Update checkpoint:
```
checkpoint.framework_context.references_loaded.push("framework-integration-patterns.md")
checkpoint.phases["01"].steps_completed.push("1.1")
```

---

### Step 1.2: Load Validation Checklist

EXECUTE:
```
Read(file_path="src/claude/skills/spec-driven-agents/references/validation-checklist.md")

Extract and store:
- 6 DevForgeAI compliance checks
- 6 Claude Code compliance checks
- Auto-fix logic (which checks can be auto-fixed)
- Validation outcomes (PASS, PASS WITH WARNINGS, FAIL)
```

VERIFY: Validation checklist loaded. At minimum: 12 check names extracted.
IF content is empty or Read failed: HALT -- "Step 1.2: Validation checklist not loaded."

RECORD: Update checkpoint:
```
checkpoint.framework_context.references_loaded.push("validation-checklist.md")
checkpoint.phases["01"].steps_completed.push("1.2")
```

---

### Step 1.3: Determine Required Context Files

Based on the creation mode and domain (from Phase 00 parameters), determine which of the 6 context files the generated agent will need to reference.

EXECUTE:
```
IF checkpoint.parameters.domain is known:
  Use domain-to-context-file mapping from Step 1.1:
    backend → all 6 context files
    frontend → tech-stack, source-tree, coding-standards
    qa → anti-patterns, coding-standards
    security → anti-patterns, architecture-constraints, coding-standards
    deployment → tech-stack, source-tree, dependencies
    architecture → all 6 context files
    documentation → source-tree, coding-standards
    general → tech-stack, coding-standards (minimum set)
ELSE:
  Set context_files_required = ["tech-stack.md", "coding-standards.md"] (minimum set)
  Note: Will be refined in Phase 02 after domain is determined
```

VERIFY: `checkpoint.framework_context.context_files_required` is a non-empty array.
IF empty: HALT -- "Step 1.3: Context files required not determined."

RECORD: Update checkpoint:
```
checkpoint.framework_context.context_files_required = determined_files
checkpoint.phases["01"].steps_completed.push("1.3")
checkpoint.phases["01"].status = "completed"
checkpoint.progress.current_phase = 2
checkpoint.progress.phases_completed.push("01")
checkpoint.progress.completion_percentage = 17
```
Write updated checkpoint to disk.

---

## Phase Exit Verification

```
VERIFY ALL:
  checkpoint.framework_context.references_loaded.length >= 2
  checkpoint.framework_context.context_files_required.length >= 1
  checkpoint.phases["01"].status == "completed"

IF ANY fails: HALT -- "Phase 01 exit criteria not met."
```

---

## Phase Transition Display

```
Display:
"Phase 01 Complete: Framework Context Loaded
  References: {references_loaded.length} loaded
  Context files required: {context_files_required.join(', ')}
  → Proceeding to Phase 02: Requirements Gathering"
```
