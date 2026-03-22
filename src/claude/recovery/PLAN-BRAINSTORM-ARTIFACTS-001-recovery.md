# Recovery Prompt: PLAN-BRAINSTORM-ARTIFACTS-001

**Use this prompt to resume work if context window was cleared or session crashed.**

---

## Copy-Paste Prompt Below

```
You are resuming work on an approved DevForgeAI enhancement plan. A previous session may have been interrupted mid-implementation.

## Plan Location
Read the full plan first:
```
Read(file_path="/home/bryan/.claude/plans/immutable-tumbling-pizza.md")
```

If that path fails, try:
```
Read(file_path="/mnt/c/Projects/Treelint/.claude/recovery/PLAN-BRAINSTORM-ARTIFACTS-001-recovery.md")
```

## What This Plan Does

**Enhancement:** Add project artifact generation (README.md, CLAUDE.md, .gitignore) to devforgeai-brainstorming skill Phase 7

**Approach:** Extend Phase 7 with new Step 7.7, add templates, always ask user consent

**Files to Modify:**
1. `.claude/skills/devforgeai-brainstorming/SKILL.md` (+50-80 lines)
2. `.claude/skills/devforgeai-brainstorming/references/handoff-synthesis-workflow.md` (+150-200 lines)
3. `.claude/skills/devforgeai-brainstorming/references/output-templates.md` (+100-150 lines)

**Files to Create:**
1. `.claude/skills/devforgeai-brainstorming/assets/templates/readme-brainstorm-template.md` (~150 lines)
2. `.claude/skills/devforgeai-brainstorming/assets/templates/claude-md-template.md` (~120 lines)
3. `.claude/skills/devforgeai-brainstorming/assets/templates/gitignore-template.md` (~50 lines)

## Detecting Partial Work

Before continuing, check what was already done:

### Check 1: Templates Created?
```bash
ls -la .claude/skills/devforgeai-brainstorming/assets/templates/
```
Look for:
- [ ] `readme-brainstorm-template.md` - exists?
- [ ] `claude-md-template.md` - exists?
- [ ] `gitignore-template.md` - exists?

### Check 2: SKILL.md Modified?
```bash
grep -n "Step 7.7" .claude/skills/devforgeai-brainstorming/SKILL.md
```
If found → SKILL.md was modified

### Check 3: Handoff Workflow Modified?
```bash
grep -n "Generate Project Artifacts" .claude/skills/devforgeai-brainstorming/references/handoff-synthesis-workflow.md
```
If found → Workflow was modified

### Check 4: Output Templates Modified?
```bash
grep -n "artifact_generation" .claude/skills/devforgeai-brainstorming/references/output-templates.md
```
If found → Output templates were modified

## Resume Logic

Based on checks above, determine checkpoint status:

| Checkpoint | Condition | Action |
|------------|-----------|--------|
| 1 | No templates exist | Start from Checkpoint 1 |
| 2 | Templates exist, no SKILL.md changes | Start from Checkpoint 2 |
| 3 | SKILL.md modified, no workflow changes | Start from Checkpoint 3 |
| 4 | Workflow modified, no output template changes | Start from Checkpoint 4 |
| 5 | All modifications done | Run integration test |
| 6 | All tests pass | Update documentation |

## Checkpoint Definitions (from plan Section 10)

### Checkpoint 1: Templates Created
- [ ] Create `readme-brainstorm-template.md`
- [ ] Create `claude-md-template.md`
- [ ] Create `gitignore-template.md`

### Checkpoint 2: SKILL.md Updated
- [ ] Add Step 7.7 to Phase 7 section
- [ ] Renumber Steps 7.8-7.11
- [ ] Add reference file loading instruction

### Checkpoint 3: Reference Workflow Updated
- [ ] Add Step 7.7 detailed implementation to `handoff-synthesis-workflow.md`
- [ ] Add conflict handling documentation
- [ ] Add user consent AskUserQuestion pattern

### Checkpoint 4: Output Templates Updated
- [ ] Add artifact generation display templates to `output-templates.md`
- [ ] Add confirmation message templates

### Checkpoint 5: Integration Tested
- [ ] Verify templates load correctly
- [ ] Test with sample session data
- [ ] Verify conflict handling works

### Checkpoint 6: Documentation Updated
- [ ] Update skill README.md
- [ ] Note devforgeai-documentation conflict handling

## User Decisions (Already Confirmed)

| Decision | Choice |
|----------|--------|
| Phase structure | Extend Phase 7 (not new Phase 8) |
| User consent | Always ask before generating |
| Artifacts | README.md, CLAUDE.md, .gitignore |

## If Partial/Corrupted Files Found

If any file appears incomplete or corrupted:

1. **Check git status:**
   ```bash
   git status
   git diff .claude/skills/devforgeai-brainstorming/
   ```

2. **If changes are staged but broken:**
   ```bash
   # Ask user before running:
   git checkout -- <file>  # Revert specific file
   ```

3. **If unsure:** Ask user before reverting. Show them the diff.

## Ready to Resume

After running the checks above:

1. Report which checkpoint you're resuming from
2. Show what work was already completed
3. Ask user: "Ready to continue from Checkpoint N?"
4. On confirmation, proceed with implementation

## Reference Files (Read as Needed)

| Purpose | Path |
|---------|------|
| Full Plan | `/home/bryan/.claude/plans/immutable-tumbling-pizza.md` |
| Example README | `/mnt/c/Projects/Treelint/README.md` (278 lines) |
| Example CLAUDE.md | `/mnt/c/Projects/Treelint/CLAUDE.md` (241 lines) |
| Target SKILL.md | `.claude/skills/devforgeai-brainstorming/SKILL.md` |
| Handoff Workflow | `.claude/skills/devforgeai-brainstorming/references/handoff-synthesis-workflow.md` |
| Output Templates | `.claude/skills/devforgeai-brainstorming/references/output-templates.md` |
| Documentation Templates | `.claude/skills/devforgeai-documentation/assets/templates/` |

## Important Context

- **Project:** This is enhancing the DevForgeAI framework itself
- **Framework:** DevForgeAI is the spec-driven development framework
- **Treelint:** Was the brainstorming session that revealed this gap (BRAINSTORM-001)
- **Goal:** Auto-generate README.md, CLAUDE.md, .gitignore after brainstorming sessions

Now run the detection checks and report your findings.
```

---

## Quick Reference Card

**Plan ID:** PLAN-BRAINSTORM-ARTIFACTS-001
**Plan Path:** `/home/bryan/.claude/plans/immutable-tumbling-pizza.md`
**Recovery Path:** `/mnt/c/Projects/Treelint/.claude/recovery/PLAN-BRAINSTORM-ARTIFACTS-001-recovery.md`
**Date Created:** 2025-12-23
**Status:** Approved, ready for implementation

**6 Checkpoints:**
1. Templates Created
2. SKILL.md Updated
3. Reference Workflow Updated
4. Output Templates Updated
5. Integration Tested
6. Documentation Updated

**3 Files to Modify:**
- SKILL.md
- handoff-synthesis-workflow.md
- output-templates.md

**3 Files to Create:**
- readme-brainstorm-template.md
- claude-md-template.md
- gitignore-template.md
