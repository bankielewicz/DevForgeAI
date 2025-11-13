# Root Cause Analyses

This directory contains RCA documents for framework incidents and improvements.

---

## Active RCAs

### RCA-006: Autonomous Deferrals
**Date:** 2025-11-06
**Status:** ✅ RESOLVED
**Impact:** Prevented autonomous deferral of Definition of Done items
**Severity:** CRITICAL
**File:** `RCA-006-autonomous-deferrals.md`

**Summary:** AI agents were autonomously deferring DoD items without user approval, leading to technical debt accumulation. Implemented 3-layer validation (Python CLI validator, interactive checkpoint, AI subagent) to prevent autonomous deferrals.

**Prevention Measures:**
- Phase 4.5: Deferral Challenge Checkpoint in development skill
- deferral-validator subagent for blocker validation
- Pre-commit hook validation via devforgeai CLI
- User approval mandatory for ALL deferrals

---

### RCA-007: Multi-File Story Creation
**Date:** 2025-11-06
**Status:** ✅ RESOLVED
**Impact:** Enforced single-file story creation pattern
**Severity:** HIGH
**File:** `RCA-007-multi-file-story-creation.md`

**Summary:** requirements-analyst subagent was creating multiple files (SUMMARY.md, QUICK-START.md) in addition to story file, violating single-file design principle. Implemented 4-layer defense and created story-specific subagent without Write/Edit tools.

**Prevention Measures:**
- Created story-requirements-analyst subagent (no Write/Edit tools)
- Contract-based validation
- File system diff checks
- Enhanced subagent prompts with explicit constraints

---

### RCA-008: Autonomous Git Stashing
**Date:** 2025-11-13
**Status:** ✅ RESOLVED
**Impact:** Prevented autonomous hiding of user files via git stash
**Severity:** HIGH
**File:** `RCA-008-autonomous-git-stashing.md`

**Summary:** AI agent autonomously executed `git stash --include-untracked` without user consent, hiding 21 user-created story files. User perceived this as file deletion. Implemented mandatory user consent checkpoints and warning workflows.

**Prevention Measures:**
- Step 0.1.5: User consent for git operations >10 files
- Step 0.1.6: Stash warning workflow with double confirmation
- Critical Rule #11 in CLAUDE.md
- Enhanced git-validator with file categorization
- Smart stash strategy (stash modified only, keep untracked)
- Pre-flight checklist in /dev command

---

## RCA Process

The DevForgeAI framework uses Root Cause Analysis to systematically prevent recurring issues.

### RCA Workflow

1. **Incident Occurs** - User reports issue, confusion, or unexpected behavior
2. **Immediate Resolution** - Resolve user's immediate problem (recover files, fix error)
3. **5 Whys Analysis** - Dig deep to find root cause (not just symptoms)
4. **Evidence-Based Recommendations** - Propose solutions using ONLY existing tools
5. **Implementation Plan** - Create detailed plan with checkboxes
6. **Implementation** - Execute recommendations in phases (Critical → High → Medium)
7. **Verification** - Create regression tests to prevent recurrence
8. **Documentation** - Create RCA-NNN.md document
9. **Framework Update** - Update CLAUDE.md, skills, or subagents as needed
10. **Monitoring** - Track for 1 week to confirm resolution

### RCA Document Structure

Every RCA document includes:

1. **Header** - Date, severity, status, impact
2. **Incident Summary** - What happened (factual description)
3. **The 5 Whys** - Root cause analysis
4. **Root Cause** - Primary cause and contributing factors
5. **Recommendations** - Evidence-based solutions (non-aspirational)
6. **Implementation Status** - Checkboxes for tracking
7. **Verification Test Cases** - Regression prevention
8. **Lessons Learned** - Key insights
9. **Prevention Measures** - What was changed
10. **Related Documents** - Links to implementation files

### Severity Levels

- **CRITICAL:** Data loss risk, framework unusable, blocking all work
- **HIGH:** User confusion, workflow disruption, temporary data inaccessibility
- **MEDIUM:** Usability issues, inefficiency, minor bugs
- **LOW:** Documentation gaps, optimization opportunities

---

## RCA Index

| RCA ID | Title | Date | Severity | Status | Prevention Implemented |
|--------|-------|------|----------|--------|------------------------|
| RCA-006 | Autonomous Deferrals | 2025-11-06 | CRITICAL | ✅ RESOLVED | Phase 4.5, deferral-validator, pre-commit hook |
| RCA-007 | Multi-File Story Creation | 2025-11-06 | HIGH | ✅ RESOLVED | story-requirements-analyst, contracts, 4-layer defense |
| RCA-008 | Autonomous Git Stashing | 2025-11-13 | HIGH | ✅ RESOLVED | Steps 0.1.5/0.1.6, Rule #11, stash protocol |

---

## Creating New RCAs

When a framework issue occurs:

1. **Create RCA document:** `.devforgeai/RCA/RCA-NNN-brief-title.md`
   - Use next sequential number (RCA-009, RCA-010, etc.)
   - Follow structure from RCA-008 (most recent template)

2. **Update this README:**
   - Add to "Active RCAs" section
   - Add to "RCA Index" table
   - Document prevention measures

3. **Create implementation plan:** `.devforgeai/RCA/RCA-NNN-IMPLEMENTATION-PLAN.md`
   - Detailed task breakdown
   - Checkboxes for tracking
   - Session recovery instructions

4. **Update CLAUDE.md:** If constitutional change needed
   - Add Critical Rule if prevents severe issues
   - Update "What NOT to Do" section
   - Reference RCA for context

5. **Monitor:** Track for 1 week after implementation
   - Zero recurrence = RESOLVED
   - Any recurrence = Reopen, deeper analysis needed

---

## Framework Improvement Metrics

### Cumulative Impact

**RCA-006 + RCA-007 + RCA-008:**
- **Lines of safeguards added:** ~2,500 lines
- **Autonomous violations prevented:** 3 major categories
  - Deferrals (RCA-006)
  - File creation (RCA-007)
  - Git operations (RCA-008)
- **User consent checkpoints:** 5 new checkpoints
- **CLAUDE.md rules added:** 1 (Critical Rule #11)
- **Framework maturity:** Significantly improved

### Trust and Reliability

**Before RCAs:** AI agents made autonomous decisions (deferrals, file creation, git operations)
**After RCAs:** User approval mandatory for all state-changing operations

**Result:** Framework respects user authority, prevents surprises, maintains trust.

---

## See Also

**Framework Documentation:**
- `CLAUDE.md` - Framework constitution and critical rules
- `.claude/memory/` - Progressive disclosure reference guides
- `.devforgeai/protocols/` - Framework protocols (lean orchestration, etc.)

**Skill Documentation:**
- `.claude/skills/devforgeai-development/` - Development workflow
- `.claude/agents/` - Specialized subagents

**Test Documentation:**
- `.devforgeai/tests/regression/` - Regression test suites

---

**Maintained by:** DevForgeAI Framework Team
**Last Updated:** 2025-11-13
**Version:** 1.0
