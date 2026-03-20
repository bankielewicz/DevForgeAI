# Context File Validation

## Purpose

Verify that the 6 constitutional context files exist. These files are required for /dev and /qa workflows to function correctly in headless mode.

## Required Context Files

| # | File | Path |
|---|------|------|
| 1 | Technology Stack | `devforgeai/specs/context/tech-stack.md` |
| 2 | Source Tree | `devforgeai/specs/context/source-tree.md` |
| 3 | Dependencies | `devforgeai/specs/context/dependencies.md` |
| 4 | Coding Standards | `devforgeai/specs/context/coding-standards.md` |
| 5 | Architecture Constraints | `devforgeai/specs/context/architecture-constraints.md` |
| 6 | Anti-Patterns | `devforgeai/specs/context/anti-patterns.md` |

## Validation Procedure

Check each file exists:

```
FOR each file in context_files:
    result = Glob(pattern=file.path)
    IF result is empty:
        missing_files.append(file.name)
```

## Result Classification

**All 6 present:** $CONTEXT_FILES_VALID = true
- Workflows will function correctly with full framework context.

**1-5 present:** $CONTEXT_FILES_VALID = "warn"
- Display warning listing missing files:
  ```
  Warning: {N} context file(s) missing:
    - {missing_file_1}
    - {missing_file_2}

  Headless /dev and /qa workflows may not function correctly.
  Run /create-context to generate missing context files.
  ```

**0 present:** $CONTEXT_FILES_VALID = "warn"
- Display warning:
  ```
  Warning: No context files found in devforgeai/specs/context/.
  Run /create-context before using the generated CI workflows.
  Workflows will be generated but will fail during execution.
  ```

## Important

Do NOT halt on missing context files. Context files are a prerequisite for /dev and /qa *execution*, not for *workflow generation*. The workflows themselves can be generated regardless -- they will simply fail when run if context files are absent.
