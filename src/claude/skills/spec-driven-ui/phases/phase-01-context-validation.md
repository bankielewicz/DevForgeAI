# Phase 01: Context Validation

**Purpose:** Verify all 6 DevForgeAI context files exist and load critical constraints for UI generation.

**Pre-Flight:** Verify Phase 00 completed.

---

## Step 1.1: Load Context Validation Reference

**EXECUTE:**
```
Read(file_path="src/claude/skills/spec-driven-ui/references/context-validation.md")
```
If Read fails, try fallback path:
```
Read(file_path=".claude/skills/spec-driven-ui/references/context-validation.md")
```

**VERIFY:**
- File content loaded into context
- Content contains validation procedures

**RECORD:**
```
Bash(command="devforgeai-validate phase-record ${IDENTIFIER} --workflow=ui --phase=01 --step=1.1 --project-root=. 2>&1")
```

---

## Step 1.2: Verify 6 Context Files Exist

**EXECUTE:**
```
Glob(pattern="devforgeai/specs/context/tech-stack.md")
Glob(pattern="devforgeai/specs/context/source-tree.md")
Glob(pattern="devforgeai/specs/context/dependencies.md")
Glob(pattern="devforgeai/specs/context/coding-standards.md")
Glob(pattern="devforgeai/specs/context/architecture-constraints.md")
Glob(pattern="devforgeai/specs/context/anti-patterns.md")
```

**VERIFY:**
- All 6 files found
- If ANY file missing: HALT — "Context files missing. Run `/create-context` to generate them."

**RECORD:**
```
Bash(command="devforgeai-validate phase-record ${IDENTIFIER} --workflow=ui --phase=01 --step=1.2 --project-root=. 2>&1")
```

---

## Step 1.3: Load Critical Context Files

**EXECUTE:**
```
Read(file_path="devforgeai/specs/context/tech-stack.md")
Read(file_path="devforgeai/specs/context/source-tree.md")
Read(file_path="devforgeai/specs/context/dependencies.md")
```

**VERIFY:**
- All 3 files loaded into context
- tech-stack.md contains technology definitions
- source-tree.md contains directory structure

**RECORD:**
```
Bash(command="devforgeai-validate phase-record ${IDENTIFIER} --workflow=ui --phase=01 --step=1.3 --project-root=. 2>&1")
```

---

## Step 1.4: Extract UI-Specific Constraints

**EXECUTE:**
Extract from loaded context files:
- Approved frontend frameworks (from tech-stack.md)
- UI component output directory (from source-tree.md, default: `devforgeai/specs/ui/`)
- Approved CSS/styling packages (from dependencies.md)
- Any UI-specific anti-patterns (from anti-patterns.md — load if needed)

Store extracted constraints as working data for downstream phases.

**VERIFY:**
- At least one data point extracted (framework, directory, or package)
- If tech-stack.md has no frontend section: Note for Phase 03 (user will need to choose)

**RECORD:**
```
Bash(command="devforgeai-validate phase-record ${IDENTIFIER} --workflow=ui --phase=01 --step=1.4 --project-root=. 2>&1")
```

---

## Phase 01 Completion

**EXECUTE:**
```
Bash(command="devforgeai-validate phase-complete ${IDENTIFIER} --workflow=ui --phase=01 --project-root=. 2>&1")
```

**VERIFY:**
- Exit code 0 or 2 (backward compatibility)

**NEXT:** Proceed to Phase 02 (Story Analysis).
