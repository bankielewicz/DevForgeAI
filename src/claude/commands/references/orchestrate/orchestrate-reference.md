# /orchestrate - Extended Reference Documentation

Supplementary documentation for the `/orchestrate` command. The command file contains core workflow logic; this file contains detailed documentation, examples, and recovery procedures.

---

## Checkpoint Resume Capability

The skill automatically detects and resumes from checkpoints:

| Checkpoint | Starting Phase | Skips |
|------------|----------------|-------|
| **None** | Phase 2 (Development) | None (full cycle) |
| **DEV_COMPLETE** | Phase 3 (QA) | Phase 2 |
| **QA_APPROVED** | Phase 4 (Staging) | Phases 2-3 |
| **STAGING_COMPLETE** | Phase 5 (Production) | Phases 2-4 |
| **PRODUCTION_COMPLETE** | Skip (already done) | All (exit with message) |

**Checkpoint precedence:** Checkpoint status overrides story status field

---

## QA Retry Handling (Phase 3.5)

The skill now handles QA failures intelligently:

**Retry Loop:**
1. QA fails → Skill categorizes failure type
2. Skill counts retry attempts (from workflow history)
3. If < 3 attempts: User chooses recovery strategy
4. If "retry": Skill re-invokes dev → QA automatically
5. If QA passes: Continue to staging
6. If QA fails again: Loop repeats (up to 3 total attempts)
7. If 3 attempts reached: Halt with story split recommendation

**Recovery Options:**
- **Retry:** Automatic dev fix → QA retry cycle
- **Follow-ups:** Create tracking stories for deferred items
- **Manual:** User fixes via /dev, then re-run /orchestrate
- **Exception:** Create ADR for coverage/anti-pattern exceptions

**This was 134 lines in command, now coordinated by skill.**

---

## Error Recovery

### Manual Phase Execution (If Orchestration Halted)

```bash
# Development only
/dev STORY-042

# QA only
/qa STORY-042

# Staging only
/release STORY-042 staging

# Production only
/release STORY-042 production

# Resume orchestration
/orchestrate STORY-042    # Auto-resumes from checkpoint
```

### Common Error Scenarios

**Scenario 1: QA Fails Due to Deferrals**
- Skill presents 3 options (retry, follow-ups, manual)
- User chooses path
- Skill coordinates recovery
- Command displays result

**Scenario 2: Staging Deployment Fails**
- Skill creates STAGING_FAILED checkpoint
- Orchestration halts
- User fixes deployment config
- Run: `/orchestrate STORY-042` (resumes from staging)

**Scenario 3: Manual Process Running**
- Story status: "In Development"
- Skill blocks orchestration (manual process detected)
- User completes manual process or cancels
- Re-run: `/orchestrate STORY-042`

---

## Architecture (Lean Orchestration Pattern)

**This command exemplifies lean orchestration:**

**Command responsibilities (ONLY):**
1. Parse arguments (story ID validation)
2. Load context (story file via @file)
3. Set markers (explicit context for skill)
4. Invoke skill (single delegation point)
5. Display results (output what skill returns)

**Command does NOT:**
- Parse checkpoints (skill Phase 0 does this)
- Coordinate retries (skill Phase 3.5 does this)
- Update story status (skill Phase 6 does this)
- Determine starting phase (skill Phase 0 does this)
- Count retry attempts (skill Phase 3.5 does this)

**Benefits:**
- Command loads quickly (~2.5K tokens vs ~4K before)
- Skill contains all orchestration logic (proper layer)
- Easy to maintain (single source of truth)
- Budget compliant (60% usage vs 100% before)

---

## What the Skill Handles

The devforgeai-orchestration skill executes complete workflow coordination:

**Phases:**
- Phase 0: Checkpoint detection (NEW - was in command)
- Phase 1: Story validation
- Phase 2: Development (invokes spec-driven-dev)
- Phase 3: QA (invokes devforgeai-qa)
- Phase 3.5: QA retry with loop prevention (NEW - was in command, max 3 attempts)
- Phase 4: Staging release (invokes devforgeai-release)
- Phase 5: Production release (invokes devforgeai-release)
- Phase 6: Finalization (NEW - was in command)

**Key Features:**
- Automatic checkpoint resume (Phase 0)
- QA retry coordination (Phase 3.5)
- Loop prevention (max 3 QA attempts)
- Follow-up story creation for deferrals
- Complete workflow history tracking
- Structured summary generation

---

## Usage Examples

**Full orchestration:**
```
/orchestrate STORY-042
→ Executes: Dev → QA → Staging → Production
→ Result: Story released to production
```

**Resume from checkpoint:**
```
/orchestrate STORY-042  # Auto-detects previous progress
→ Skill resumes from last checkpoint
→ Skips completed phases
```

**After QA failure:**
```
/orchestrate STORY-042
→ Skill offers retry options
→ Coordinates dev fix → QA retry
→ Continues to release if QA passes
```

---

## Performance

**Token Budget:**
- Command overhead: ~2.5K tokens (argument validation + skill invocation + display)
- Skill execution (isolated context): ~155K-175K tokens total
  - Development: ~85K
  - QA (deep): ~65K
  - QA retry (if needed): ~20K additional
  - Release (staging + production): ~40K
- **Main conversation impact:** ~2.5K (83% reduction from 15K original)

**Execution Time:**
- Typical (no retries): 60-90 minutes
  - Development: 30-45 min
  - QA: 10-15 min
  - Staging: 5-10 min
  - Production: 10-15 min
- With retries: Add 40-60 min per QA retry cycle
- Complex stories: Up to 2 hours

**Character Budget:**
- Target: ~9,000 characters (60% of 15K limit)
- Down from: 15,012 characters (100% of limit, over by 12)
- Savings: ~6,000 characters (40% reduction)

---

## Related Commands

**Workflow commands:**
- `/dev [STORY-ID]` - Development only (no QA or release)
- `/qa [STORY-ID]` - QA validation only
- `/release [STORY-ID] [env]` - Release only (staging or production)
- `/orchestrate [STORY-ID]` - Complete lifecycle (dev → QA → release)

**Planning commands:**
- `/create-story [description]` - Create story before orchestration
- `/create-sprint [name]` - Plan sprint before development

**Framework maintenance:**
- `/audit-budget` - Check command character budgets
- `/audit-deferrals` - Check story deferral violations

---

## Notes

**Lean Orchestration Applied:**
- Checkpoint detection: Skill Phase 0 (was in command)
- QA retry coordination: Skill Phase 3.5 (was in command)
- Finalization: Skill Phase 6 (was in command)
- Command delegates, skill coordinates, clean separation

**Refactored:** 2025-11-06 (599 → 527 lines, 15,012 → 14,422 chars)
**Reduction:** 12% lines, 4% characters
**Budget:** 96% (was 100% over limit)
**Pattern:** Lean orchestration (234 lines business logic extracted to skill)

---

**Version:** 3.0 - Lean Orchestration Reference | **Source:** Extracted from orchestrate.md v2.0
