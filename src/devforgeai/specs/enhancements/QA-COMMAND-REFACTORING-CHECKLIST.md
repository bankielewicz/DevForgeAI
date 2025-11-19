# QA Command Refactoring - Implementation Checklist

**Status:** Ready for Implementation
**Priority:** High (improves command budget compliance and token efficiency)
**Effort:** 4-6 hours (analysis, testing, documentation)
**Owner:** DevForgeAI Framework Team

---

## Pre-Implementation Verification

- [ ] Review analysis document: `.devforgeai/specs/enhancements/QA-COMMAND-REFACTORING-ANALYSIS.md`
- [ ] Review summary document: `.devforgeai/specs/enhancements/QA-COMMAND-REFACTORING-SUMMARY.md`
- [ ] Approve architectural decision (Option B: new subagent)
- [ ] Confirm token efficiency targets acceptable
- [ ] Approve risk mitigation strategies

---

## Phase 1: File Creation (2 hours)

### New Subagent: qa-result-interpreter

- [ ] File created: `.claude/agents/qa-result-interpreter.md`
- [ ] YAML frontmatter complete:
  - [ ] name: qa-result-interpreter
  - [ ] description: Result interpretation and display generation
  - [ ] model: haiku
  - [ ] tools: Read, Glob, Grep (view-only)
- [ ] Purpose section clear and concise
- [ ] Workflow steps detailed (Step 1-8)
- [ ] Integration section documented
- [ ] Success criteria defined (8 items)
- [ ] Error handling documented
- [ ] Token budget target: <8K
- [ ] File total: ~300 lines

### Contextual Reference File

- [ ] File created: `.claude/skills/devforgeai-qa/references/qa-result-formatting-guide.md`
- [ ] DevForgeAI Context section:
  - [ ] Story workflow states explained
  - [ ] Quality gates documented
  - [ ] Validation modes contextualized
- [ ] Framework Constraints (6 sections):
  - [ ] Coverage thresholds (immutable rules)
  - [ ] Violation severity classification (deterministic)
  - [ ] Deferral handling (valid/invalid patterns)
  - [ ] Story status transitions
  - [ ] Anti-pattern categories
  - [ ] Spec compliance dimensions
- [ ] Display template guidelines (5 sections):
  - [ ] Structure for all templates
  - [ ] Emoji usage standards
  - [ ] Tone guidance
  - [ ] Length guidelines
  - [ ] Example templates
- [ ] Framework integration points (3 sections):
  - [ ] Context files references
  - [ ] Related skills/subagents
  - [ ] Workflow history tracking
- [ ] Error scenarios documented (4 types)
- [ ] Performance and reliability requirements
- [ ] Testing checklist included (20+ test cases)
- [ ] File total: ~250 lines

### Refactored Command

- [ ] File modified: `.claude/commands/qa.md`
- [ ] Old content archived (backup)
- [ ] New structure implemented:
  - [ ] YAML frontmatter preserved
  - [ ] Quick reference section added
  - [ ] Command workflow (Phase 0-3):
    - [ ] Phase 0: Argument validation (20 lines)
    - [ ] Phase 1: Invoke skill (15 lines)
    - [ ] Phase 2: Display results (10 lines)
    - [ ] Phase 3: Next steps (5 lines)
  - [ ] Error handling (25 lines)
  - [ ] Integration documentation (125 lines)
- [ ] No Phase 2-5 (old) content remains
- [ ] File total: ~200 lines
- [ ] Character count: <8K (verified)
- [ ] Within 15K character budget ✅

---

## Phase 2: Integration Updates (1 hour)

### Update devforgeai-qa Skill

- [ ] File to modify: `.claude/skills/devforgeai-qa/SKILL.md`
- [ ] Find Phase 5 (Generate QA Report), Step 3
- [ ] Add subagent invocation:
  ```
  Task(
      subagent_type="qa-result-interpreter",
      description="Interpret QA results",
      prompt="QA report: .devforgeai/qa/reports/{STORY_ID}-qa-report.md
              Interpret and generate user-friendly display.
              Return structured result."
  )
  ```
- [ ] Add code to parse result JSON
- [ ] Update skill to return result_summary (not raw report)
- [ ] Test invocation syntax
- [ ] Verify skill unchanged otherwise

### Update Memory References

- [ ] File: `.claude/memory/subagents-reference.md`
  - [ ] Add qa-result-interpreter to agent list
  - [ ] Add row to agent comparison table:
    | qa-result-interpreter | Result interpretation | haiku | <8K |
  - [ ] Add invocation method (proactive in skill)
  - [ ] Add token efficiency note
  - [ ] Add related subagents (deferral-validator)

- [ ] File: `.claude/memory/commands-reference.md`
  - [ ] Update /qa section (new refactored workflow)
  - [ ] Note command refactoring (71% reduction)
  - [ ] Update token budget notes (2.7K main conversation)
  - [ ] Update workflow diagram
  - [ ] Add reference to analysis document

---

## Phase 3: Testing (2 hours)

### Unit Tests: qa-result-interpreter Parsing

- [ ] Test 1: Light mode PASS report
  - [ ] Input: Valid light mode pass report
  - [ ] Expected: status=PASSED, mode=light
  - [ ] Result: Template generated, next steps provided

- [ ] Test 2: Light mode FAIL report
  - [ ] Input: Valid light mode fail report
  - [ ] Expected: status=FAILED, violations detected
  - [ ] Result: Remediation guidance provided

- [ ] Test 3: Deep mode PASS report (full metrics)
  - [ ] Input: Valid deep mode pass report with all metrics
  - [ ] Expected: status=PASSED, coverage shown by layer
  - [ ] Result: Approval confirmation, release guidance

- [ ] Test 4: Deep mode FAIL - coverage violations
  - [ ] Input: Deep mode report with coverage <95% business logic
  - [ ] Expected: CRITICAL coverage violation detected
  - [ ] Result: Specific gap and test suggestions provided

- [ ] Test 5: Deep mode FAIL - anti-pattern violations
  - [ ] Input: Deep mode report with CRITICAL violations
  - [ ] Expected: Violations grouped by type
  - [ ] Result: Remediation by category

- [ ] Test 6: Deep mode FAIL - spec compliance violations
  - [ ] Input: Deep mode report with AC not validated
  - [ ] Expected: Spec compliance failures detected
  - [ ] Result: AC validation guidance

- [ ] Test 7: Deep mode FAIL - deferral violations
  - [ ] Input: Deep mode report with deferral-validator violations
  - [ ] Expected: Deferral issues highlighted with RCA-007 context
  - [ ] Result: Specific remediation (fix justification, create ADR, complete work)

- [ ] Test 8: Report with 0 violations
  - [ ] Input: Report with no violations
  - [ ] Expected: Clean PASSED status
  - [ ] Result: Celebration template, release guidance

- [ ] Test 9: Report with 50+ violations (aggregation)
  - [ ] Input: Report with many violations
  - [ ] Expected: Proper aggregation by severity/type
  - [ ] Result: Priority-ordered remediation guidance

- [ ] Test 10: Malformed report (error handling)
  - [ ] Input: JSON syntax error in report
  - [ ] Expected: Error status, graceful degradation
  - [ ] Result: Helpful error message, retry guidance

- [ ] Test 11: Missing report file (error handling)
  - [ ] Input: Report path doesn't exist
  - [ ] Expected: ERROR status
  - [ ] Result: Clear error with recovery steps

### Integration Tests: Full Workflow

- [ ] Test 1: Light QA during development
  - [ ] Story status: In Development
  - [ ] Mode inferred: light
  - [ ] Result: Pass → Continue development
  - [ ] Status unchanged ✓

- [ ] Test 2: Deep QA after completion
  - [ ] Story status: Dev Complete
  - [ ] Mode inferred: deep
  - [ ] Result: Pass → QA Approved
  - [ ] Status changed to "QA Approved ✅"

- [ ] Test 3: Coverage gap failure
  - [ ] Story status: Dev Complete
  - [ ] Mode: deep
  - [ ] Coverage <95% business logic
  - [ ] Result: Fail → QA Failed
  - [ ] Specific gap shown with test suggestions

- [ ] Test 4: Anti-pattern failure
  - [ ] Story status: Dev Complete
  - [ ] Mode: deep
  - [ ] CRITICAL violation detected
  - [ ] Result: Fail → QA Failed
  - [ ] Remediation by pattern type

- [ ] Test 5: Deferral failure
  - [ ] Story status: Dev Complete
  - [ ] Mode: deep
  - [ ] Deferred DoD items with violations
  - [ ] Result: Fail → QA Failed
  - [ ] Deferral validation results shown
  - [ ] Return to dev recommended

- [ ] Test 6: Retry after fix (attempt #2)
  - [ ] Previous attempt: Failed
  - [ ] Status: QA Failed → Back to In Development
  - [ ] After fix: Re-run /qa
  - [ ] Result: Pass → QA Approved
  - [ ] Attempt history tracked

- [ ] Test 7: Multiple retries (attempt #3)
  - [ ] Attempt 1: Failed
  - [ ] Attempt 2: Failed
  - [ ] Attempt 3: Failed again
  - [ ] Warning shown: Consider story split
  - [ ] Suggests smaller stories going forward

- [ ] Test 8: Status transition verification
  - [ ] Deep pass: Status → "QA Approved ✅"
  - [ ] Deep fail: Status → "QA Failed ❌"
  - [ ] Light pass: Status unchanged
  - [ ] Light fail: Status unchanged

- [ ] Test 9: Next steps accuracy
  - [ ] Light pass: "Continue dev", "Run deep when ready"
  - [ ] Deep pass: "Ready for release", "/release command"
  - [ ] Deep fail (coverage): "Add tests for gap"
  - [ ] Deep fail (deferral): "Return to dev"

### Regression Tests (Behavior Unchanged)

- [ ] Light QA still blocks on test failure ✓
- [ ] Light QA still blocks on critical violations ✓
- [ ] Light QA doesn't change story status ✓
- [ ] Deep QA still updates status on pass ✓
- [ ] Deep QA still updates status on fail ✓
- [ ] Deep QA blocks approval on CRITICAL violations ✓
- [ ] Deep QA blocks approval on HIGH violations ✓
- [ ] Coverage thresholds still enforced ✓
- [ ] Deferral validation still required ✓
- [ ] All framework gates intact ✓

### Performance Tests

- [ ] Subagent token usage <8K (haiku model)
- [ ] Command overhead <2.5K
- [ ] Main conversation savings 65%+
- [ ] Report parsing <1 second
- [ ] Template generation <1 second
- [ ] Total subagent execution <30 seconds

---

## Phase 4: Validation (30 minutes)

### Code Quality Checks

- [ ] Subagent is framework-aware (references constraints)
- [ ] Reference file prevents "bull in china shop" (explicit guardrails)
- [ ] Coverage thresholds immutable (in reference file)
- [ ] Deferral rules enforced (RCA-007 context)
- [ ] Display templates consistent (same structure per type)
- [ ] JSON output valid (syntax, schema)
- [ ] Error handling graceful (no exceptions, clear messages)
- [ ] No code duplication (moved to appropriate layer)

### Documentation Checks

- [ ] Subagent has clear purpose statement
- [ ] Workflow steps are detailed and numbered
- [ ] Integration points documented
- [ ] Success criteria defined
- [ ] Error scenarios handled
- [ ] Token budget specified
- [ ] Reference file comprehensive
- [ ] Command workflow clear

### Framework Alignment Checks

- [ ] Subagent respects tech-stack.md references
- [ ] Subagent respects source-tree.md structure
- [ ] Subagent references anti-patterns.md
- [ ] Subagent references architecture-constraints.md
- [ ] Subagent references coding-standards.md
- [ ] Quality gates intact (no shortcuts)
- [ ] RCA-007 principles followed (deferral handling)

---

## Phase 5: Documentation (1 hour)

### Create Release Notes

**File:** `.devforgeai/specs/enhancements/QA-COMMAND-REFACTORING-RELEASE-NOTES.md`

- [ ] Executive summary (1 paragraph)
- [ ] What changed (3-4 main points)
- [ ] Why it matters (token efficiency, maintainability)
- [ ] User impact (minimal - behavior unchanged)
- [ ] Rollout (date, restart terminal)
- [ ] Questions? (point to analysis documents)

### Update CLAUDE.md (If Needed)

- [ ] Check if command architecture section needs update
- [ ] Check if subagent architecture section needs update
- [ ] Verify token efficiency guidelines still accurate
- [ ] Add reference to qa-result-interpreter if new pattern

### Verify All Documentation Links

- [ ] Analysis doc links correct
- [ ] Summary doc links correct
- [ ] Checklist doc links correct
- [ ] Memory references point to docs
- [ ] Commands reference updated
- [ ] Subagents reference updated

---

## Phase 6: Final Verification (30 minutes)

### Pre-Merge Checklist

- [ ] All tests passed (11 unit + 9 integration)
- [ ] Regression tests confirm no behavioral change
- [ ] Code review completed and approved
- [ ] Documentation reviewed and approved
- [ ] Token budgets verified
- [ ] File changes complete:
  - [ ] qa-result-interpreter.md created
  - [ ] qa-result-formatting-guide.md created
  - [ ] qa.md refactored (71% reduction)
  - [ ] devforgeai-qa skill updated (subagent invocation)
  - [ ] subagents-reference.md updated
  - [ ] commands-reference.md updated

### Merge Preparation

- [ ] Commit message prepared:
  ```
  refactor(qa-command): Lean orchestration with result-interpreter subagent

  - Reduce command from 692 to 200 lines (71% reduction)
  - Improve token efficiency: 8K → 2.7K (66% reduction)
  - Create qa-result-interpreter subagent (isolated context)
  - Create qa-result-formatting-guide (framework guardrails)
  - Maintain 100% backward compatibility (behavior unchanged)

  Closes: QA-COMMAND-REFACTORING
  ```
- [ ] All changed files listed
- [ ] Related PRs/issues referenced

---

## Phase 7: Deployment (30 minutes)

### Merge to Main

- [ ] All checks passing (CI, linting, tests)
- [ ] Code reviewed and approved
- [ ] Merge PR to main branch
- [ ] Verify merge successful

### Terminal Restart

- [ ] User restarts Claude Code terminal
- [ ] `/help` command shows updated `/qa` command
- [ ] Subagent appears in agent list (if `/agents` command available)

### Smoke Tests (Live Validation)

- [ ] Test 1: Run `/qa STORY-X light` on in-development story
  - [ ] Command executes without error
  - [ ] Mode inferred correctly
  - [ ] Results displayed clearly
  - [ ] No status change

- [ ] Test 2: Run `/qa STORY-Y deep` on dev-complete story
  - [ ] Command executes without error
  - [ ] Deep validation runs
  - [ ] QA report generated
  - [ ] Status updated if passed

- [ ] Test 3: Test failure scenario
  - [ ] Deliberately create QA failure (modify test)
  - [ ] Run `/qa STORY-Z deep`
  - [ ] Failure clearly displayed
  - [ ] Remediation guidance provided
  - [ ] Next steps appropriate

---

## Success Criteria (Final Validation)

### Code Metrics
- [ ] Command lines: 200 ± 10 (target 200)
- [ ] Command characters: 8K ± 500 (target 8K)
- [ ] Subagent lines: 300 ± 20 (target 300)
- [ ] Reference lines: 250 ± 20 (target 250)
- [ ] Total new files: 2 (qa-result-interpreter + reference guide)
- [ ] Files modified: 3 (qa command, qa skill, memory references)

### Token Efficiency
- [ ] Command overhead: <2.5K tokens (was 7.8K)
- [ ] Main conversation: <2.7K (was ~8K)
- [ ] Savings: 66% minimum
- [ ] Budget compliance: <8K characters ✅

### Quality Assurance
- [ ] All 11 unit tests pass ✅
- [ ] All 9 integration tests pass ✅
- [ ] All 10 regression tests pass ✅
- [ ] Performance tests meet targets ✅
- [ ] Code review approved ✅
- [ ] Documentation approved ✅

### Framework Alignment
- [ ] Quality gates intact ✅
- [ ] Coverage thresholds enforced ✅
- [ ] Deferral validation respected (RCA-007) ✅
- [ ] Context files referenced appropriately ✅
- [ ] Subagent framework-aware ✅
- [ ] Reference file prevents autonomous decisions ✅

### User Experience
- [ ] No behavior changes from user perspective ✅
- [ ] Display quality maintained ✅
- [ ] Error messages improved ✅
- [ ] Next steps clear and actionable ✅
- [ ] Documentation helpful ✅

---

## Estimated Timeline

**Total Implementation Time: 4-6 hours**

- Phase 1 (File Creation): 2 hours
- Phase 2 (Integration): 1 hour
- Phase 3 (Testing): 2 hours
- Phase 4 (Validation): 30 minutes
- Phase 5 (Documentation): 1 hour
- Phase 6 (Final Verification): 30 minutes
- Phase 7 (Deployment): 30 minutes

**Parallelizable:** Phases 1 and 2 can run in parallel if multiple developers

---

## Rollback Plan

If issues discovered post-deployment:

1. **Identify Issue**
   - Monitor error rates, token usage, user feedback
   - Create GitHub issue documenting problem

2. **Rapid Rollback**
   - Revert commit to previous version
   - Restart terminal
   - Verify old behavior restored

3. **Root Cause Analysis**
   - Review error logs
   - Identify test gap that missed issue
   - Update test cases

4. **Re-implement**
   - Fix identified issue
   - Add tests that catch problem
   - Re-run all test phases
   - Deploy again

**Estimated Rollback Time:** <15 minutes

---

## Sign-Off

- [ ] Analysis reviewed and approved: _______________
- [ ] Design approved (Option B: new subagent): _______________
- [ ] Code review approved: _______________
- [ ] Testing completed: _______________
- [ ] Documentation approved: _______________
- [ ] Ready to merge: _______________
- [ ] Deployed to production: _______________

---

## Post-Deployment Monitoring (Week 1)

- [ ] Monitor `/qa` command usage in daily meetings
- [ ] Track token usage per workflow
- [ ] Collect user feedback on display quality
- [ ] Check error rate (should be 0% for behavioral changes)
- [ ] Verify memory references working (subagents-reference, commands-reference)
- [ ] Confirm performance targets met (<8K main conversation)

---

## Notes

- All files created/modified are documented in this checklist
- Analysis and summary documents provide detailed context
- Reference file serves as guardrails for subagent
- Comprehensive test suite prevents regressions
- Rollback plan provides safety net
- Documentation supports future maintenance

