# RCA-006: Deferral Validation Quality Gate Failure - AI Handoff Prompt

**Purpose:** Complete prompt for new Claude Code session to implement RCA-006 fixes
**Context:** Quality gate allows unjustified deferrals - dev defers without approval, QA passes anyway
**Priority:** 🔴 CRITICAL - Quality gate integrity compromised
**Estimated Effort:** 18 hours total
**Related:** RCA-005 (slash command parameters) - COMPLETED in commit 039bbdd

---

## COPY-PASTE PROMPT FOR NEW CLAUDE SESSION

```
I need you to implement RCA-006 fixes for the DevForgeAI framework. This RCA addresses a critical quality gate failure where dev agents defer Definition of Done items without justification, and QA approves stories anyway, allowing technical debt into "QA Approved" state.

## Context

**What Happened:**
During TreeLint Codelens project development:

1. **STORY-004:** Dev agent deferred "Exit code handling" to STORY-005 without technical justification, no ADR created, QA approved anyway
2. **STORY-005:** Dev agent deferred scenarios 8 & 9, QA approved despite circular deferral (STORY-004 → STORY-005 → STORY-004)
3. **Quality Gate Failed:** QA validated "reason exists" but NOT "reason is justified"
4. **No Feedback Loop:** QA failure doesn't trigger dev rework cycle
5. **Technical Debt:** Gaps remain unfilled, no follow-up stories created

**Root Cause Identified:**
1. Dev skill allows autonomous deferrals without AskUserQuestion
2. QA skill validates documentation, not justification
3. No deferral-validator subagent enforcement
4. No feedback loop: QA FAIL → Dev fix → QA retry
5. No mechanism to create follow-up stories for deferred work

**Evidence Files:**
- tmp/output.md - WSL /qa execution showing issues
- tmp/STORY-004-qa-report.md - QA passed with unjustified deferral
- tmp/STORY-005-qa-report.md - QA passed with circular deferrals
- tmp/RCA-exit-code-deferral-story-004.md - Complete dev RCA
- tmp/RCA-qa-process-failure-story-004.md - Complete QA RCA

**Previous Work:**
- RCA-005 completed in commit 039bbdd (slash command parameter fixes)
- All files backed up and committed
- Framework validated in WSL (working correctly)
- Ready for RCA-006 implementation

## Your Task

Implement the comprehensive fix plan documented in:
`devforgeai/specs/enhancements/RCA-006-deferral-validation-plan-DRAFT.md`

**Read these files for complete context:**
1. `devforgeai/specs/enhancements/RCA-006-deferral-validation-plan-DRAFT.md` - Complete implementation plan
2. `tmp/RCA-exit-code-deferral-story-004.md` - Dev agent RCA with 5 Whys
3. `tmp/RCA-qa-process-failure-story-004.md` - QA process RCA with 5 Whys
4. `.claude/skills/devforgeai-development/SKILL.md` - Current dev workflow
5. `.claude/skills/devforgeai-qa/SKILL.md` - Current QA workflow
6. `CLAUDE.md` - Framework overview and critical rules

## Critical Constraints

**MUST Follow:**
1. **AskUserQuestion for ALL deferrals** - No autonomous deferral decisions
2. **Create deferral-validator subagent** - Must be explicitly invoked (not a silo!)
3. **QA FAILS unjustified deferrals** - CRITICAL/HIGH violations block approval
4. **Feedback loop required** - QA FAIL → Dev fix → QA retry (max 3 attempts)
5. **ADR for scope changes** - Deferring DoD item = scope change = needs ADR
6. **Follow-up story tracking** - All deferred work tracked (no orphans)
7. **All solutions evidence-based** - Use patterns from RCAs, no aspirational content

## Implementation Approach

Execute all components from RCA-006 plan:

### Phase 1: Create Subagents (7 hours)
1. **deferral-validator.md** (4h) - Complete spec from RCA-qa-process lines 814-911
   - Model: haiku
   - Tools: Read, Glob, Grep
   - Validates: blockers, ADRs, story refs, circular deferrals, feasibility
   - Returns: JSON violation report
   - **CRITICAL:** Must be invoked by dev & QA skills (no silo!)

2. **technical-debt-analyzer.md** (2h) - Debt trend analysis
   - model: haiku
   - Invoked by orchestration skill Phase 5
   - Generates reports, tracks patterns

3. **code-reviewer.md enhancement** (1h) - Add deferral review
   - Add "Review 6: DoD Completeness" section
   - Already invoked by dev skill Phase 3

### Phase 2: Update Skills (8.5 hours)
4. **devforgeai-development** (3h):
   - Add 5-step decision tree (RCA-exit-code lines 398-518)
   - Add Phase 6 Step 1.5: Invoke deferral-validator
   - Add AskUserQuestion for ALL deferrals
   - Add QA failure handling workflow

5. **devforgeai-qa** (4h):
   - Add 7-substep validation (RCA-qa-process lines 580-804)
   - Add Phase 0 Step 3: Invoke deferral-validator
   - Add Phase 5b: QA iteration history
   - FAIL QA if violations found

6. **devforgeai-orchestration** (1.5h):
   - Add Phase 5: Deferred work tracking
   - Invoke technical-debt-analyzer

### Phase 3: Update Commands (3.5 hours)
7. **/dev** (1h) - Add Phase 0c: QA failure detection
8. **/qa** (1h) - Add Phase 2: Handle QA results
9. **/orchestrate** (1.5h) - Add Phase 3.5: Retry loop (max 3)

### Phase 4: Quality Gates & Templates (2 hours)
10. **quality-gates.md** (30min) - Add deferral blocking conditions
11. **ADR-EXAMPLE-004-scope-descope.md** (30min) - Scope change template
12. **technical-debt-register.md** (30min) - Debt tracking template
13. **Update documentation** (30min) - skills/subagents/commands reference

### Phase 5: Story & RCA (2 hours)
14. **Create STORY-0XX** (30min) - Main.rs error integration (closes gap)
15. **Create RCA-006 document** (1.5h) - Complete analysis with evidence

## Key Implementation Details

### Deferral-Validator Invocation Points (CRITICAL)

**In devforgeai-development skill, Phase 6, add Step 1.5:**
```markdown
After updating Implementation Notes with DoD status:

IF any DoD items marked [ ] (incomplete):
    Task(
        subagent_type="deferral-validator",
        description="Validate deferral justifications",
        prompt="Validate all deferred Definition of Done items.
                Story already loaded in conversation.
                Check for: valid reasons, technical blockers, ADRs,
                circular deferrals, story references.
                Return JSON validation report."
    )

    IF validation returns CRITICAL or HIGH violations:
        HALT development
        Display violations to user
        User must fix before git commit
```

**In devforgeai-qa skill, Phase 0, add Step 3:**
```markdown
After validating test results:

IF any incomplete DoD items found:
    Task(
        subagent_type="deferral-validator",
        description="Validate deferral justifications for QA",
        prompt="Validate all deferred DoD items for QA approval.
                Story loaded in conversation.
                Perform comprehensive validation.
                Return JSON validation report."
    )

    IF CRITICAL or HIGH violations:
        QA Status: FAILED
        Add violations to QA report
        HALT QA approval
```

### AskUserQuestion Decision Points

**Dev Skill - For Each Incomplete DoD Item:**
```markdown
AskUserQuestion:
    Question: "DoD item '{item}' not complete. How to proceed?"
    Options:
        - "Complete it now"
        - "Defer to follow-up story (create STORY-XXX)"
        - "Scope change (create ADR)"
        - "External blocker (document with ETA)"
```

**QA Command - On Deferral Failure:**
```markdown
AskUserQuestion:
    Question: "QA failed due to deferrals. Fix and retry?"
    Options:
        - "Yes - return to /dev, fix issues, retry QA"
        - "No - I'll fix manually"
```

**Orchestrate Command - On QA Failure:**
```markdown
AskUserQuestion:
    Question: "QA failed (attempt {N}/3). Continue?"
    Options:
        - "Yes - fix in dev, retry QA"
        - "No - stop orchestration"
```

## Success Criteria

After implementation:
- [ ] Deferral-validator subagent created and invoked (Dev + QA)
- [ ] Dev skill requires AskUserQuestion for all deferrals
- [ ] QA skill validates deferrals (7 substeps)
- [ ] QA FAILS stories with unjustified deferrals
- [ ] Feedback loop works: Dev → QA FAIL → Dev fix → QA retry
- [ ] Circular deferrals detected (CRITICAL violation)
- [ ] All 3 commands updated (dev, qa, orchestrate)
- [ ] Quality gates updated with deferral blocking conditions
- [ ] Templates created (ADR, tech debt register)
- [ ] Documentation updated (3 memory files)
- [ ] STORY-0XX created (closes circular deferral gap)
- [ ] RCA-006 document complete
- [ ] All tested with realistic scenarios

## Testing Requirements

**Must test:**
1. Invalid deferral (no reason) → QA should FAIL
2. Valid deferral (story split) → QA should PASS, story must exist
3. Circular deferral → QA should FAIL with CRITICAL
4. QA failure → Dev fix → QA retry loop
5. AskUserQuestion triggers for each deferral

## Important Notes

**Subagent Invocation:**
- Subagents only run if explicitly invoked via Task tool
- Don't create subagents without invoking them (becomes silo)
- deferral-validator MUST be called in dev Phase 6.1.5 AND QA Phase 0.3

**Framework Philosophy:**
- Evidence-based only (use RCA specs verbatim)
- Ask, Don't Assume (AskUserQuestion for all deferrals)
- Quality over speed (comprehensive solution, not quick fix)

**Token Budget:**
- Previous session used ~393K tokens (RCA-005)
- You start fresh with 1M tokens available
- This work estimated ~400-500K tokens
- Plenty of room for comprehensive implementation

## Files You'll Modify/Create

**Subagents (3):**
1. .claude/agents/deferral-validator.md (NEW)
2. .claude/agents/technical-debt-analyzer.md (NEW)
3. .claude/agents/code-reviewer.md (ENHANCE)

**Skills (3):**
4. .claude/skills/devforgeai-development/SKILL.md
5. .claude/skills/devforgeai-qa/SKILL.md
6. .claude/skills/devforgeai-orchestration/SKILL.md

**Commands (3):**
7. .claude/commands/dev.md
8. .claude/commands/qa.md
9. .claude/commands/orchestrate.md

**Quality Gates (1):**
10. .claude/skills/devforgeai-orchestration/references/quality-gates.md

**Templates (2):**
11. .claude/skills/devforgeai-architecture/assets/adr-examples/ADR-EXAMPLE-004-scope-descope.md
12. devforgeai/technical-debt-register.md

**Documentation (3):**
13. .claude/memory/skills-reference.md
14. .claude/memory/subagents-reference.md
15. .claude/memory/commands-reference.md

**Story (1):**
16. devforgeai/specs/Stories/STORY-0XX-integrate-error-handling-main.story.md

**RCA (1):**
17. devforgeai/specs/enhancements/RCA-006-deferral-validation-quality-gate-failure.md

**Total: 17 files**

## Execution Strategy

**Start with critical path:**
1. Read complete plan (RCA-006-deferral-validation-plan-DRAFT.md)
2. Read both RCA documents (exit-code-deferral + qa-process-failure)
3. Create deferral-validator subagent (815 lines from RCA)
4. Update dev skill with invocation (Phase 6.1.5)
5. Update QA skill with invocation (Phase 0.3)
6. Test with sample story to validate approach
7. If working: Complete remaining components
8. Document results
9. Create git commit

**Use TodoWrite to track progress** - 19 tasks total.

## Questions for You (Before Starting)

If you encounter ambiguity, HALT and use AskUserQuestion:
1. Should deferral-validator block dev commits or just warn?
2. Should QA retry be automatic or require user approval each time?
3. What should happen if user refuses to justify deferral (abort story or force completion)?

## Reference Materials

**In this repository:**
- Complete plan: `devforgeai/specs/enhancements/RCA-006-deferral-validation-plan-DRAFT.md`
- Dev RCA: `tmp/RCA-exit-code-deferral-story-004.md`
- QA RCA: `tmp/RCA-qa-process-failure-story-004.md`
- Evidence: `tmp/output.md`, `tmp/STORY-004-qa-report.md`, `tmp/STORY-005-qa-report.md`
- Previous RCA: `devforgeai/specs/enhancements/RCA-005-skill-parameter-passing.md`
- Framework docs: `CLAUDE.md`, `README.md`, `ROADMAP.md`

**Pattern to follow:**
- Same quality as RCA-001 through RCA-005 (all were excellent)
- Evidence-based solutions only (use RCA specs verbatim)
- Comprehensive testing before documenting
- Clear audit trail maintained

## Start Here

Begin by reading the complete plan and both RCA documents:

```
Read(devforgeai/specs/enhancements/RCA-006-deferral-validation-plan-DRAFT.md)
Read(tmp/RCA-exit-code-deferral-story-004.md)
Read(tmp/RCA-qa-process-failure-story-004.md)
```

Then create a TodoWrite list for all 19 tasks and execute systematically.

## Key Success Factors

**Critical:**
1. ✅ Deferral-validator subagent must be explicitly invoked (Dev Phase 6.1.5, QA Phase 0.3)
2. ✅ Dev skill must use AskUserQuestion for ALL deferrals (no autonomous decisions)
3. ✅ QA skill must FAIL stories with unjustified deferrals
4. ✅ Complete feedback loop: Dev → QA FAIL → Dev fix → QA retry

**Quality:**
- All specifications from RCAs incorporated verbatim (not paraphrased)
- All subagents explicitly invoked (no silos)
- All AskUserQuestion decision points implemented
- Complete audit trail (workflow history + QA iteration history)

**Testing:**
- Test invalid deferral → QA should FAIL
- Test valid deferral → QA should PASS
- Test circular deferral → QA should FAIL (CRITICAL)
- Test feedback loop → Dev fix → QA retry → PASS

Good luck! This is critical work that will close the quality gate gap and prevent technical debt from deferrals. 🚀
```

---

**End of handoff prompt. Copy everything between the triple backticks above for new Claude session.**

## Additional Context for Handoff

**Current Framework Status:**
- Phase 3 + RCA 1-5 complete
- Commit 039bbdd: RCA-005 fixes (slash command parameters)
- WSL validated: Framework working correctly
- Token budget for RCA-006: Fresh 1M tokens

**Why Fresh Session Recommended:**
- RCA-006 is complex (17 files, 18 hours)
- Current session: 393K tokens used (39.3%)
- Fresh session: Better token efficiency for large refactor
- Clean context for comprehensive implementation

**What's Ready:**
- Complete plan documented
- All RCA evidence captured
- All specifications from TreeLint project documented
- Test scenarios defined

**Next Session Will:**
- Start fresh with full token budget
- Read all context documents
- Execute plan systematically
- Test thoroughly
- Commit RCA-006 fixes
- Framework will be production-ready with quality gate integrity restored
