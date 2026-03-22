# STORY-538: /market-research Command & Skill Assembly

## Plan

### Current Test Status
- AC1 (command invocation): 0/6 PASS - command file doesn't exist yet
- AC2 (standalone phase): 1/6 PASS - skill missing standalone/routing docs
- AC3 (full workflow): 3/5 PASS - skill missing context passing docs
- AC4 (profile integration): 5/6 PASS - missing pacing/chunking terminology
- AC5 (command size): 0/6 PASS - command file doesn't exist yet
- AC6 (skill structure): 6/6 PASS - already passing

### Steps

1. **Create command file** `src/claude/commands/market-research.md`
   - YAML frontmatter with `argument-hint`
   - Argument validation for 4 phases
   - Delegation to researching-market skill
   - No business logic (no TAM/SAM/SOM/SWOT/Porter/fermi)
   - Under 500 lines

2. **Edit skill file** `src/claude/skills/researching-market/SKILL.md`
   - Add "Execution Mode" / "Phase Routing" section
   - Document standalone mode for each phase
   - Document "no prerequisite" for individual phases
   - Add "context passing" for full mode
   - Add "pacing" / "task chunking" / "adaptive" for profile integration
   - Keep under 1000 lines

3. **Run tests** to verify all pass

### Checkpoint
- [ ] Command file created
- [ ] Skill file updated
- [ ] All 6 test suites pass

## Status: IN PROGRESS
