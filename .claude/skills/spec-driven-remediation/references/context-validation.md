# Context Validation Rules for Remediation

Rules for validating fixes against the 6 constitutional context files. Internalized from spec-driven-stories to eliminate cross-skill dependencies.

---

## Constitutional Context Files

The following 6 files are immutable without an ADR:

1. `devforgeai/specs/context/tech-stack.md`
2. `devforgeai/specs/context/source-tree.md`
3. `devforgeai/specs/context/dependencies.md`
4. `devforgeai/specs/context/coding-standards.md`
5. `devforgeai/specs/context/architecture-constraints.md`
6. `devforgeai/specs/context/anti-patterns.md`

---

## Remediation-Specific Validation

### Before Applying Any Fix

1. **Check target file type:**
   - If target is a context file → classification MUST be "interactive" (never "automated")
   - If target is a story/epic file → automated classification is permitted (if other safety conditions met)

2. **Verify file exists:**
   ```
   Read(file_path=target_file)
   IF fails: HALT — "Target file does not exist: {target_file}"
   ```

3. **Verify file is writable:**
   - Context files require ADR + user approval
   - Story files are freely editable
   - Epic files are freely editable

### After Applying Any Fix

1. **Re-validate against source-tree.md** if the fix introduces new file paths
2. **Re-validate against tech-stack.md** if the fix introduces technology references
3. **Re-validate against anti-patterns.md** if the fix modifies code patterns

---

## Path Resolution

Story and epic files follow these path patterns:

```
Stories: devforgeai/specs/Stories/STORY-NNN-*.story.md
Epics:   devforgeai/specs/Epics/EPIC-NNN-*.epic.md
ADRs:    devforgeai/specs/adrs/ADR-NNN-*.md
Plans:   .claude/plans/*.md
```

To resolve a story ID to a file path:
```
Glob(pattern="devforgeai/specs/Stories/{STORY_ID}-*.story.md")
```

To resolve an epic ID to a file path:
```
Glob(pattern="devforgeai/specs/Epics/{EPIC_ID}-*.epic.md")
```
