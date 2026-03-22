# Execution Prompt: Enhance /validate-stories and /fix-story with Plan-Story Coherence Validation

**Copy-paste this entire prompt into a fresh Claude Code session to execute the plan.**

---

## Prompt

Read the plan file at `.claude/plans/smooth-tumbling-beacon.md`. This plan enhances the `/validate-stories` command and `/fix-story` command with a new "Plan-Story Coherence Validation" phase that detects discrepancies between plan specifications and generated story files.

**Your mission:** Implement the plan by modifying 5 existing files in the `src/` tree. No new files to create. User will sync src/ to operational folders after.

### What This Plan Does

Adds 7 new validation functions (#11-17) to the `/validate-stories --chain` workflow that detect:
1. **Cross-story schema mismatches** — sibling stories define incompatible schemas for shared data structures
2. **External API contract errors** — stories reference wrong field names in Claude hooks or CLI APIs
3. **Plan-story specification drift** — story content diverges from plan file specifications
4. **Naming inconsistencies** — sibling stories use different naming conventions for related artifacts
5. **Format pattern inconsistencies** — stories use incompatible ID/regex formats
6. **Instruction contradictions** — stories give conflicting placement/ordering instructions
7. **Dependency assumption mismatches** — dependent stories assume wrong output from their dependencies

Also adds corresponding fix procedures and verification to `/fix-story`.

### Step 1: Read the Plan

```
Read(".claude/plans/smooth-tumbling-beacon.md")
```

The plan contains:
- Section 2: The 7 validation checks with complete pseudocode logic and real examples
- Section 3: Where it slots into existing architecture (Phase 3e, chain mode)
- Section 4: Exact files to modify (5 files, all in src/ tree)
- Section 5: Detailed implementation for all 5 files
- Section 6: Progress checkpoints
- Section 9: Severity decision matrix

### Step 2: Read Existing Files

Read all 5 files that need modification to understand current structure:

```
Read("src/claude/skills/devforgeai-story-creation/references/context-validation.md")
Read("src/claude/skills/devforgeai-story-creation/references/custody-chain-workflow.md")
Read("src/claude/commands/validate-stories.md")
Read("src/claude/skills/story-remediation/references/fix-actions-catalog.md")
Read("src/claude/skills/story-remediation/references/fix-verification-workflow.md")
```

### Step 3: Implement Changes (5 files, in order)

**File 1:** `src/claude/skills/devforgeai-story-creation/references/context-validation.md`
- Add functions #11-17 after existing function #10 (`validate_story_quality`)
- Plan Section 5.1 has the complete function definitions with pseudocode

**File 2:** `src/claude/skills/devforgeai-story-creation/references/custody-chain-workflow.md`
- Add Sub-Phase 3e section after Sub-Phase 3d
- Plan Section 5.2 has the complete sub-phase definition

**File 3:** `src/claude/commands/validate-stories.md`
- Add Phase 3e dispatch in Phase 3 section, after existing 3d dispatch
- Plan Section 5.3 has the dispatch code

**File 4:** `src/claude/skills/story-remediation/references/fix-actions-catalog.md`
- Add 7 new finding types to Classification Matrix table
- Add fix procedures for each type (2 automated, 5 interactive)
- Plan Section 5.4 has the complete catalog entries

**File 5:** `src/claude/skills/story-remediation/references/fix-verification-workflow.md`
- Add coherence finding verification procedures
- Plan Section 5.5 has the verification logic

### Step 4: Update Progress Checkpoints

After each file is modified, update the progress checkpoints in Section 6 of the plan file.

### Key Constraints

- **Modify src/ tree only** — user will sync to operational folders
- **Extend, don't replace** — add to existing files, don't rewrite them
- **Use Edit tool** — targeted edits, not full file rewrites
- **Finding type prefix** — all new findings use `coherence/` prefix
- **Chain mode only** — new validation only runs with `--chain` flag
- **2+ stories required** — coherence checks need sibling stories in same epic

### Recovery

If session is interrupted:
1. Read `.claude/plans/smooth-tumbling-beacon.md`
2. Check Section 6 progress checkpoints for completed items
3. Resume from next unchecked item
4. Read the target file before editing (required by Edit tool)
