# Sprint Planner Subagent Verification Guide

Verification steps to confirm sprint-planner subagent is correctly implemented and ready for use.

---

## Pre-Deployment Verification

### 1. File Existence Check

Verify all generated files exist:

```bash
# Subagent definition
ls -la .claude/agents/sprint-planner.md
# Expected: 467 lines, ~12KB

# Reference guide
ls -la .claude/skills/devforgeai-orchestration/references/sprint-planning-guide.md
# Expected: 391 lines, ~11KB

# This summary
ls -la devforgeai/SPRINT-PLANNER-GENERATION-SUMMARY.md
# Expected: ~380 lines
```

### 2. YAML Frontmatter Validation

Check subagent frontmatter:

```bash
head -20 .claude/agents/sprint-planner.md

# Expected output:
# ---
# name: sprint-planner
# description: Sprint planning and execution specialist...
# tools: Read, Write, Edit, Glob, Grep
# model: haiku
# ---
```

**Validate:**
- [ ] name = "sprint-planner"
- [ ] description includes "sprint planning"
- [ ] tools = "Read, Write, Edit, Glob, Grep" (no Bash, no AskUserQuestion)
- [ ] model = "sonnet"
- [ ] No extra fields
- [ ] YAML syntax valid (can be parsed)

### 3. System Prompt Structure Check

Verify complete system prompt sections:

```bash
grep -n "^## " .claude/agents/sprint-planner.md | head -20

# Expected sections:
# 1. Purpose
# 2. When Invoked
# 3. Workflow
# 4. Success Criteria
# 5. Principles
# 6. Best Practices
# 7. Token Efficiency
# 8. Error Handling
# 9. Integration
# 10. References
```

**Validate:**
- [ ] All 10 major sections present
- [ ] Workflow section has 6 numbered phases
- [ ] Each phase has clear instructions
- [ ] Code examples provided in markdown
- [ ] No placeholders (TODO, TBD, FIXME)
- [ ] Links to reference guide included

### 4. Token Count Estimation

Verify system prompt meets 200-line minimum:

```bash
# Count total lines
wc -l .claude/agents/sprint-planner.md
# Expected: 467 lines

# Count system prompt (after YAML frontmatter, before end)
tail -n +8 .claude/agents/sprint-planner.md | head -n -0 | wc -l
# Expected: ~450+ lines in system prompt
```

**Validate:**
- [ ] Total file > 200 lines (framework minimum)
- [ ] System prompt > 200 lines (actual guideline)

### 5. Tool Access Validation

Verify no forbidden tools are referenced:

```bash
# Check for Bash references (should be ZERO)
grep -i "bash" .claude/agents/sprint-planner.md | wc -l
# Expected: 0

# Check for AskUserQuestion (should be ZERO - stays in command/skill)
grep -i "AskUserQuestion" .claude/agents/sprint-planner.md | wc -l
# Expected: 0

# Check for Skill invocations (should be ZERO - subagent doesn't invoke skills)
grep -i "Skill(command" .claude/agents/sprint-planner.md | wc -l
# Expected: 0

# Verify allowed tools are referenced
grep -E "(Read|Write|Edit|Glob|Grep)" .claude/agents/sprint-planner.md | wc -l
# Expected: 20+ references across workflow phases
```

**Validate:**
- [ ] No Bash tool references
- [ ] No AskUserQuestion references
- [ ] No Skill invocations
- [ ] Read tool used for discovery (Glob, Read for story validation)
- [ ] Write tool used for sprint document creation
- [ ] Edit tool used for story status updates
- [ ] Grep tool available for pattern matching (if needed)

---

## Post-Deployment Verification

### 1. Terminal Registration

After restarting Claude Code terminal:

```
/agents

# Should display:
# Available agents (18 total):
# ...
# sprint-planner - Sprint planning and execution specialist...
# ...
```

**Validate:**
- [ ] sprint-planner appears in /agents list
- [ ] Description is correct
- [ ] Word count shown (~467 lines)

### 2. Direct Subagent Invocation Test

Test invoking sprint-planner directly:

```
# First, create test stories in backlog
> /create-story Test story 1
> /create-story Test story 2

# Then invoke sprint-planner directly
Task(
  subagent_type="sprint-planner",
  description="Test sprint creation",
  prompt="Create sprint with:
    - Sprint name: Test Sprint
    - Selected stories: STORY-001, STORY-002
    - Duration: 14 days
    - Epic: EPIC-001 (or standalone if no epics)
    - Start date: 2025-11-10

    Execute complete sprint planning workflow and return summary."
)
```

**Expected output:**
```json
{
  "success": true,
  "sprint_id": "SPRINT-1",
  "sprint_name": "Test Sprint",
  "file_path": "devforgeai/specs/Sprints/Sprint-1.md",
  "capacity": {
    "total_points": [sum of test stories],
    "total_stories": 2,
    "status": "optimal"
  },
  "stories_added": [...],
  "stories_updated_count": 2,
  "next_steps": [...]
}
```

**Validate:**
- [ ] Returns success = true
- [ ] sprint_id generated correctly
- [ ] file_path points to devforgeai/specs/Sprints/Sprint-1.md
- [ ] Capacity calculation correct (sum of story points)
- [ ] stories_updated_count = 2 (both test stories)
- [ ] JSON structure complete
- [ ] No errors in output

### 3. Sprint File Creation Verification

After subagent invocation, verify sprint file:

```bash
# Check file exists
ls -la devforgeai/specs/Sprints/Sprint-1.md

# Check YAML frontmatter
head -15 devforgeai/specs/Sprints/Sprint-1.md

# Expected:
# ---
# id: SPRINT-1
# name: Test Sprint
# epic: EPIC-001
# start_date: 2025-11-10
# end_date: 2025-11-23
# duration_days: 14
# status: Active
# total_points: [calculated]
# completed_points: 0
# stories:
#   - STORY-001
#   - STORY-002
# created: 2025-11-XX HH:MM:SS
# ---
```

**Validate:**
- [ ] File exists at correct path
- [ ] YAML frontmatter valid and complete
- [ ] All required fields present
- [ ] Stories list matches input
- [ ] Dates calculated correctly
- [ ] Created timestamp present

### 4. Story Status Updates Verification

Verify stories moved to "Ready for Dev":

```bash
# Check first story
grep -A 5 "^status:" devforgeai/specs/Stories/STORY-001.story.md | head -1
# Expected: status: Ready for Dev

# Check sprint reference
grep -A 5 "^sprint:" devforgeai/specs/Stories/STORY-001.story.md | head -1
# Expected: sprint: SPRINT-1

# Check workflow history updated
grep "Workflow History" devforgeai/specs/Stories/STORY-001.story.md
# Should have entry: "Added to SPRINT-1"
```

**Validate:**
- [ ] Story status changed from Backlog to Ready for Dev
- [ ] Sprint reference added/updated to SPRINT-1
- [ ] Workflow history entry present
- [ ] Timestamp in workflow history
- [ ] All test stories updated

### 5. Reference Guide Availability

Verify reference guide can be loaded:

```bash
# Check file exists
ls -la .claude/skills/devforgeai-orchestration/references/sprint-planning-guide.md

# Check size
wc -l .claude/skills/devforgeai-orchestration/references/sprint-planning-guide.md
# Expected: ~391 lines

# Check major sections
grep "^## " .claude/skills/devforgeai-orchestration/references/sprint-planning-guide.md

# Expected sections:
# ## Overview
# ## Sprint Capacity Guidelines
# ## Story Selection Workflow
# ## Story Status Transition
# ## Sprint File Structure
# ## Sprint Duration Options
# ## Velocity Tracking
# ## Common Sprint Planning Scenarios
# ## Integration with DevForgeAI Workflow
# ## Best Practices Checklist
# ## References
```

**Validate:**
- [ ] File exists and is readable
- [ ] Contains 391+ lines
- [ ] All major sections present
- [ ] Code examples included
- [ ] Best practices documented
- [ ] Framework integration explained

---

## Integration Testing

### Test 1: Command to Subagent Integration

Verify lean orchestration pattern works:

```
# Preconditions: 2+ backlog stories exist

> /create-sprint "Integration Test"
[Select stories: STORY-001, STORY-002]
[Choose duration: 14]
[Choose epic: EPIC-001]

# Expected flow:
# 1. Command displays story selection prompt
# 2. Command gathers metadata via AskUserQuestion
# 3. Command invokes sprint-planner subagent
# 4. Subagent generates sprint file and updates stories
# 5. Command displays results from subagent

# Expected outcome:
# Sprint-1.md created
# STORY-001 and STORY-002 moved to Ready for Dev
# Results displayed to user
```

**Validate:**
- [ ] Command parses arguments correctly
- [ ] Story selection works (AskUserQuestion)
- [ ] Metadata collection works (AskUserQuestion)
- [ ] Subagent invoked (no errors)
- [ ] Sprint file created with correct content
- [ ] Story status updates applied
- [ ] Results displayed to user
- [ ] No token overflow in main context

### Test 2: Capacity Validation

Test sprint planner capacity analysis:

**Test A: Optimal Capacity (20-40 points)**
```
Stories: 5 + 8 + 3 + 5 = 21 points
Expected: status = "optimal"
Validation: capacity.status == "optimal"
```

**Test B: Under Capacity (< 20 points)**
```
Stories: 3 + 5 = 8 points
Expected: status = "under", warning in summary
Validation: capacity.status == "under"
```

**Test C: Over Capacity (> 40 points)**
```
Stories: 8 + 8 + 8 + 8 + 8 = 40+ points
Expected: status = "over", warning in summary
Validation: capacity.status == "over"
```

**Validate:**
- [ ] Optimal capacity (20-40) identified correctly
- [ ] Under-capacity warning triggered
- [ ] Over-capacity warning triggered
- [ ] Capacity status included in response

### Test 3: Error Handling

Test subagent error handling:

**Test A: Non-existent Story**
```
Stories: STORY-999 (doesn't exist)
Expected: Error returned, no sprint created
Validation: success = false, error message includes "STORY-999 does not exist"
```

**Test B: Non-backlog Story**
```
Stories: STORY-001 (status = "In Development")
Expected: Error returned, validation message
Validation: success = false, error indicates status mismatch
```

**Test C: Missing Directory**
```
If .ai_docs/Sprints doesn't exist
Expected: Directory created automatically
Validation: Sprint file created in devforgeai/specs/Sprints/Sprint-N.md
```

**Validate:**
- [ ] Non-existent stories handled gracefully
- [ ] Status validation enforced
- [ ] Helpful error messages returned
- [ ] Directory creation/validation works

### Test 4: Multi-Sprint Numbering

Test sequential sprint numbering:

```
# Create first sprint
Task(...) → SPRINT-1.md created

# Create second sprint
Task(...) → SPRINT-2.md created

# Create third sprint
Task(...) → SPRINT-3.md created

# Verify numbering
ls -1 devforgeai/specs/Sprints/Sprint-*.md
# Expected:
# Sprint-1.md
# Sprint-2.md
# Sprint-3.md
```

**Validate:**
- [ ] First sprint numbered SPRINT-1
- [ ] Each subsequent sprint incremented
- [ ] No gaps in numbering
- [ ] Existing sprints not overwritten

---

## Performance Validation

### 1. Token Usage Check

Verify token efficiency target met:

```
# Expected: < 40K tokens per invocation

During test invocation:
- Subagent reads ~5 story files: ~5,000 tokens
- Subagent discovers sprints (Glob): ~1,000 tokens
- Subagent generates document: ~5,000 tokens
- Subagent updates 5 stories: ~20,000 tokens
- Subagent generates summary: ~2,000 tokens
- Total: ~33,000 tokens (within 40K budget)
```

**Validate:**
- [ ] Invocation completes within expected time
- [ ] No timeout or truncation warnings
- [ ] Response complete and properly formatted

### 2. File I/O Performance

Verify native tool efficiency:

```bash
# Time a sprint creation (informal)
time Task(subagent_type="sprint-planner", ...)

# Expected:
# - Invocation < 30 seconds
# - File I/O operations < 5 seconds
# - Response generation < 5 seconds
```

**Validate:**
- [ ] Subagent completes promptly
- [ ] No file I/O bottlenecks
- [ ] Response generated before timeout

---

## Documentation Verification

### 1. Subagent Reference Updated

Check that subagents reference document includes sprint-planner:

```bash
grep -A 5 "sprint-planner" .claude/memory/subagents-reference.md

# Expected: Entry in subagents table with:
# - Name: sprint-planner
# - Purpose: Sprint planning
# - model: haiku
# - Token target: <40K
```

**Validate:**
- [ ] Subagent listed in reference
- [ ] Description accurate
- [ ] Model and token target correct

### 2. Commands Reference Updated

Check that commands reference includes sprint-planner mention:

```bash
grep -i "sprint" .claude/memory/commands-reference.md

# Should mention:
# - /create-sprint command invokes sprint-planner
# - Sprint-planner handles document generation
```

**Validate:**
- [ ] /create-sprint documented as using sprint-planner
- [ ] Integration pattern explained

### 3. Framework Documentation Coherent

Verify all references to sprint planning are consistent:

```bash
# Count references to "sprint"
grep -r "sprint" .claude/memory/*.md .claude/agents/sprint-planner.md .claude/skills/devforgeai-orchestration/references/ | wc -l
# Expected: 100+ consistent references

# Check for contradictions
grep -i "sprint.*40.*points" .claude/memory/*.md .claude/agents/sprint-planner.md .claude/skills/devforgeai-orchestration/references/
# All should reference 20-40 point capacity consistently
```

**Validate:**
- [ ] No contradictory guidance
- [ ] Capacity guidelines consistent (20-40 points)
- [ ] Status transitions documented consistently
- [ ] References link correctly

---

## Final Checklist

Before considering deployment complete:

**Subagent Implementation:**
- [ ] YAML frontmatter valid
- [ ] System prompt > 200 lines (467 lines)
- [ ] All required sections present
- [ ] No forbidden tools referenced
- [ ] Workflow phases documented (6 phases)
- [ ] Error handling specified
- [ ] Integration documented

**Reference Guide:**
- [ ] Created and complete (391 lines)
- [ ] Capacity guidelines documented
- [ ] Status transitions explained
- [ ] File structure specified
- [ ] Best practices included
- [ ] Integration with workflow explained

**File Generation:**
- [ ] sprint-planner.md created ✅
- [ ] sprint-planning-guide.md created ✅
- [ ] Generation summary created ✅
- [ ] Refactoring guide created ✅
- [ ] This verification guide created ✅

**Functional Testing:**
- [ ] Direct subagent invocation works
- [ ] Sprint file created with valid content
- [ ] Story statuses updated correctly
- [ ] Workflow history entries added
- [ ] Capacity calculation accurate
- [ ] Error handling works
- [ ] Multi-sprint numbering correct

**Integration Testing:**
- [ ] Command can invoke subagent
- [ ] Subagent response parsed correctly
- [ ] Results displayed to user
- [ ] No token overflow

**Performance:**
- [ ] Token usage < 40K
- [ ] Execution time acceptable
- [ ] File I/O efficient

**Documentation:**
- [ ] Subagents reference updated
- [ ] Commands reference updated
- [ ] No contradictions in guidance
- [ ] All links correct

---

## Troubleshooting

### Issue: Subagent Not Found in `/agents`

**Symptom:** `/agents` doesn't show sprint-planner

**Causes:**
1. Terminal not restarted after file creation
2. File syntax error in sprint-planner.md

**Resolution:**
1. Restart Claude Code terminal
2. Run `/agents` again
3. If still missing, check YAML frontmatter syntax

### Issue: Sprint File Not Created

**Symptom:** Sprint planner returns success but file doesn't exist

**Causes:**
1. Directory .ai_docs/Sprints doesn't exist
2. File write permission issue
3. Subagent error not reported

**Resolution:**
1. Check if .ai_docs/Sprints exists: `ls .ai_docs/Sprints`
2. If missing, create: `mkdir -p .ai_docs/Sprints`
3. Check file permissions: `ls -la .ai_docs/`
4. Rerun subagent invocation

### Issue: Story Status Not Updated

**Symptom:** Sprint created but stories still in Backlog

**Causes:**
1. Edit operations failed silently
2. YAML frontmatter format issue in story file
3. File permissions on story files

**Resolution:**
1. Check story file format: `head -20 devforgeai/specs/Stories/STORY-001.story.md`
2. Verify YAML syntax is valid
3. Check permissions: `ls -la devforgeai/specs/Stories/`
4. Manually run Edit operations to verify they work

### Issue: Token Budget Exceeded

**Symptom:** Subagent times out or truncates response

**Causes:**
1. Too many stories selected (> 10)
2. Very large story files
3. Token budget was underestimated

**Resolution:**
1. Test with smaller selection (3-5 stories)
2. Check if story files have excessive content
3. If consistent timeout, may need to increase model or split work

### Issue: Circular Dependency Warning

**Symptom:** Stories selected with circular dependencies not detected

**Causes:**
1. Dependency validation not yet implemented
2. Subagent skipped dependency check

**Resolution:**
1. This is acceptable for MVP - dependency validation can be added in Phase 2
2. Document circular dependency issue in story notes
3. Manual resolution required for now

---

## Deployment Readiness Checklist

Before marking as production-ready:

**Code Quality:**
- [x] Subagent YAML valid
- [x] System prompt comprehensive
- [x] Framework-aware design
- [x] Error handling complete

**Testing:**
- [ ] Direct invocation tested
- [ ] File creation verified
- [ ] Story updates verified
- [ ] Capacity calculation validated
- [ ] Error scenarios tested
- [ ] Integration with command tested

**Documentation:**
- [x] Subagent well-documented
- [x] Reference guide complete
- [x] Integration points clear
- [x] Best practices included

**Performance:**
- [ ] Token usage verified < 40K
- [ ] Execution time acceptable
- [ ] No timeout issues

**Integration:**
- [ ] Subagents reference updated
- [ ] Commands reference updated
- [ ] No documentation conflicts

---

## Sign-Off

When all checks complete:

```
✅ SPRINT-PLANNER SUBAGENT VERIFIED AND READY FOR PRODUCTION

Generated: 2025-11-05
Framework: DevForgeAI 1.0.1
Status: Ready for /create-sprint Command Refactoring
Next: Refactor /create-sprint to lean orchestration pattern
```

---

**Document:** Sprint Planner Subagent Verification Guide
**Status:** Complete
**Last Updated:** 2025-11-05
