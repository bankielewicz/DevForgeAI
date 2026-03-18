---
id: orchestration-user-input-integration
title: Orchestration Skill - User Input Guidance Integration
version: "1.0"
created: 2025-01-21
updated: 2025-01-21
status: Published
audience: DevForgeAI Development Team
parent_document: user-input-guidance.md
skill: devforgeai-orchestration
---

# Orchestration Skill - User Input Guidance Integration Reference

**Purpose:** Document how devforgeai-orchestration skill integrates user-input-guidance.md with conditional loading logic for sprint planning mode.

**Context:** This skill coordinates the complete spec-driven development lifecycle. Sprint Planning (Phase 3) benefits from guided user input patterns.

---

## Section 1: Mode Detection and Conditional Loading

### 1.1 Orchestration Modes

This skill operates in 4 modes (from SKILL.md), but guidance loading applies to 1:

**Sprint Planning (Phase 3) - LOAD GUIDANCE**
- **Detection:** Context marker `**Command:** create-sprint` present
- **Action:** Load guidance in Phase 3 Step 1 (Sprint Planning)
- **Questions:** Epic selection (bounded + explicit none), story selection (multi-select with capacity)
- **Token Cost:** ~1,000 tokens

**Other Modes - SKIP GUIDANCE (not applicable):**
- Story Management: No user interaction needed (automated workflow)
- Audit Deferrals: No interactive guidance needed (audit mode)
- Checkpoint Detection: No guidance needed

### 1.2 Mode-Based Guidance Loading Logic

**Sprint Planning Mode:**

```python
def phase_3_sprint_planning():
    """Phase 3 Step 1: Sprint Planning with guidance"""

    # Check if sprint planning mode
    if context_marker_exists("**Command:** create-sprint"):
        mode = "sprint_planning"
        skip_guidance = False
        log_info("Sprint planning mode detected. Loading user-input-guidance.md for Phase 3...")
        guidance_content = Read(file_path=".claude/skills/devforgeai-orchestration/references/user-input-guidance.md")

        # Step 0: Load guidance (sprint patterns)
        # Patterns available for sprint questions

        # Step 1: Ask epic selection (Bounded + Explicit None)
        # Step 2: Ask story selection (Multi-Select with Capacity Guidance)
        # etc.

    else:
        mode = "other"
        # Not sprint mode - skip guidance for this mode
```

---

## Section 2: Sprint Mode Pattern Mapping

### 2.1 Phase 3 Questions-to-Patterns (Sprint Mode)

| Phase | Step | Question | Pattern Name | Pattern # | Template | Options/Bounds | Rationale |
|-------|------|----------|--------------|-----------|----------|----------------|-----------|
| **3** | **1** | "Select epic?" | Bounded + Explicit None | (custom) | CONST-001 | N+1 options (epics + "None") | Optional epic linkage |
| **3** | **1** | "Select stories?" | Bounded Multi-Select + Capacity | (custom) | CONST-002 | N items (all Backlog stories) | Multiple with capacity guidance |

### 2.2 Sprint Mode Pattern Applications

**Pattern (Custom): Bounded Choice + Explicit None (Epic Selection)**
- **Use for:** Optional epic linkage in sprint
- **Application:** List all epics + explicit "None - Standalone Sprint" option
- **Reasoning:** Sprint may or may not belong to epic
- **User Input:** Select 0 or 1 epic (single-select)
- **Result:** Link sprint to epic (or mark standalone)

**Pattern (Custom): Bounded Multi-Select with Capacity Guidance (Story Selection)**
- **Use for:** Selecting stories for sprint with capacity awareness
- **Application:** Multi-select from all Backlog stories, display running total, show capacity warnings
- **Reasoning:** Capacity planning (20-40 points recommended), but flexible
- **User Input:** Select multiple stories (multi-select), running total displayed
- **Guidance:** Warn if <20 or >40 points (recommendations, not enforcement)
- **Result:** Sprint created with selected stories

### 2.3 Sprint Mode Examples

**Example: Epic Selection (Bounded + Explicit None)**

```
# First, list all existing epics + explicit None option:
epics = [
    "EPIC-001: User Authentication",
    "EPIC-002: Dashboard Features",
    "EPIC-003: Reporting System"
]

AskUserQuestion(
    question: "Which epic does this sprint belong to? (optional)",
    header: "Sprint Epic Linkage",
    description: "Sprints can belong to an epic or be standalone. Select the epic this sprint contributes to, or select 'None' for independent work.",
    options: [
        {label: "EPIC-001: User Authentication", description: "Estimated remaining: 2-3 sprints"},
        {label: "EPIC-002: Dashboard Features", description: "Estimated remaining: 4-5 sprints"},
        {label: "EPIC-003: Reporting System", description: "Estimated remaining: 1-2 sprints"},
        {label: "None - Standalone Sprint", description: "This sprint is not part of any epic (maintenance, bugfixes, etc.)"}
    ],
    multiSelect: false
)
```

**Example: Story Selection (Multi-Select with Capacity Guidance)**

```
# Display all Backlog stories with capacity feedback:

AskUserQuestion(
    question: "Which stories will you include in this sprint?",
    header: "Sprint Story Selection",
    description: "Select stories to add to the sprint. Recommended capacity: 20-40 story points. As you select, running total displays with capacity warnings.",
    options: [
        {label: "STORY-051: User login form", description: "5 points | Frontend feature | Ready"},
        {label: "STORY-052: Database schema", description: "8 points | Infrastructure | Ready"},
        {label: "STORY-053: Email notifications", description: "13 points | Backend feature | Blocked (needs STORY-052)"},
        {label: "STORY-054: Analytics dashboard", description: "21 points | Full-stack | Ready"},
        {label: "STORY-055: Mobile responsive", description: "13 points | Frontend | Ready"},
        # ... more stories
    ],
    multiSelect: true
)

# DURING selection, show:
# "Selected: STORY-051 (5 pts), STORY-052 (8 pts) | Total: 13 pts"
# "Selected: STORY-051 (5 pts), STORY-052 (8 pts), STORY-054 (21 pts) | Total: 34 pts ✓ Optimal"
# "Selected: STORY-051 (5 pts), STORY-052 (8 pts), STORY-054 (21 pts), STORY-055 (13 pts) | Total: 47 pts ⚠️ Over capacity"
```

**Capacity Guidance Messages:**
- **<20 points:** "⚠️ Low capacity: X pts (recommended: 20-40 pts). Consider adding more stories."
- **20-40 points:** "✓ Optimal capacity: X pts. Good sprint load for typical team."
- **>40 points:** "⚠️ Over capacity: X pts (recommended: 20-40 pts). Consider reducing stories."
- **Enforcement:** Guidance is advice, not blocking. User can proceed with any total.

---

## Section 3: Reference Deployment

### 3.1 File Locations

**Master File:** `src/.claude/skills/spec-driven-ideation/references/user-input-guidance.md`

**Orchestration Deployment:**
- Location: `src/.claude/skills/devforgeai-orchestration/references/user-input-guidance.md`
- Deployment: Copy from master using:
  ```bash
  cp src/.claude/skills/spec-driven-ideation/references/user-input-guidance.md \
     src/.claude/skills/devforgeai-orchestration/references/user-input-guidance.md
  ```

**Operational Folder:**
- Also copied to: `.claude/skills/devforgeai-orchestration/references/user-input-guidance.md`

### 3.2 Checksum Validation

**Verify deployment integrity:**
```bash
# All 3 orchestration deployments should have identical SHA256
sha256sum src/.claude/skills/devforgeai-orchestration/references/user-input-guidance.md \
          .claude/skills/devforgeai-orchestration/references/user-input-guidance.md

# If hashes match: ✅ Deployment successful
# If hashes differ: ❌ Files out of sync, redeploy
```

---

## Section 4: Testing Strategy

### 4.1 Sprint Mode Unit Tests

**Test 1: Sprint mode loads guidance**
```python
def test_sprint_mode_loads_guidance():
    """Verify guidance loads for sprint planning"""
    # Setup: Context marker "**Command:** create-sprint"
    # Execute: Phase 3 Step 1
    # Assert: Read called with guidance file path
    # Assert: Log contains "Sprint planning mode"
```

**Test 2: Epic selection (Bounded + None)**
```python
def test_epic_selection_bounded_plus_none():
    """Verify epic selection includes 'None' option"""
    # Setup: Sprint mode, guidance loaded
    # Execute: Epic selection question
    # Assert: All existing epics listed
    # Assert: Explicit "None - Standalone Sprint" option present
    # Assert: User can select one epic or None
```

**Test 3: Story selection (Multi-Select)**
```python
def test_story_selection_multi_select():
    """Verify story selection supports multi-select"""
    # Setup: Sprint mode, guidance loaded
    # Execute: Story selection question
    # Assert: Multi-select enabled (multiple stories)
    # Assert: Running total displayed
    # Assert: Capacity warnings shown
```

**Test 4: Capacity guidance (running total)**
```python
def test_capacity_guidance_running_total():
    """Verify running total and capacity warnings"""
    # Setup: User selecting stories
    # User selects STORY-051 (5 pts)
    # Assert: Display "Selected: STORY-051 (5 pts) | Total: 5 pts"
    # User selects STORY-054 (21 pts)
    # Assert: Display "Selected: ... | Total: 26 pts ✓ Optimal"
    # User selects STORY-055 (13 pts)
    # Assert: Display "Selected: ... | Total: 39 pts ⚠️ Over capacity"
```

**Test 5: Capacity enforcement (none, guidance only)**
```python
def test_capacity_enforcement_guidance_only():
    """Verify capacity is guidance, not enforcement"""
    # Setup: Sprint with 55 points (well over 40)
    # Execute: Sprint creation with capacity warning
    # Assert: Sprint created successfully (no blocking)
    # Assert: Warning displayed (guidance)
    # Assert: User can proceed (no enforcement)
```

### 4.2 Integration Tests

**Test 6: Sprint planning full flow**
```python
def test_orchestration_sprint_full_flow():
    """Full sprint workflow: detect mode → load guidance → apply patterns"""
    # Setup: User runs /create-sprint
    # Execute: Phase 3 complete
    # Assert: Mode detected as sprint
    # Assert: Guidance loaded
    # Assert: Epic selection asked (with None option)
    # Assert: Story selection asked (multi-select, capacity warnings)
    # Assert: Running total displayed as user selects
    # Assert: Sprint file created with capacity note
```

**Test 7: Backward compatibility - story management unchanged**
```python
def test_backward_compat_story_management():
    """Verify story management mode unchanged (no guidance)"""
    # Setup: Existing story in development
    # Execute: Orchestration for story management
    # Assert: No guidance loaded
    # Assert: Same behavior as pre-STORY-057
    # Assert: Workflow progresses automatically (no interactive questions)
```

### 4.3 Regression Tests

**10 existing orchestration tests:**
- Sprint planning tests (5)
- Story management tests (3)
- Workflow state transition tests (2)

All must pass with guidance integration.

---

## Section 5: Token Budget Analysis

### 5.1 Sprint Mode Token Cost

```
Step 0: Mode detection + guidance loading
  - Context marker check: ~30 tokens
  - Log messages: ~20 tokens
  - Read file (600 lines): ~500-700 tokens
  - Pattern lookups: ~50-100 tokens
  - Subtotal: ~600-850 tokens

Steps 1-2: Pattern application (sprint questions)
  - Epic selection options: ~75-100 tokens
  - Story multi-select: ~50-75 tokens
  - Capacity guidance: ~50-100 tokens
  - Subtotal: ~175-275 tokens

TOTAL sprint mode: 775-1,125 tokens (~1,000 avg)
```

### 5.2 Other Modes Token Cost

```
Story Management, Audit, etc.: 0 tokens (no guidance loaded)
```

---

## Section 6: Skill Integration Checklist

### 6.1 SKILL.md Modifications

- [ ] **Phase 3 Step 1 Head:** Add note "Step 0: Conditional guidance loading for sprint mode"
- [ ] **Phase 3 Step 1 (NEW):** Add ~10 lines of sprint mode detection + guidance loading
- [ ] **Pattern References:** Add guidance pattern references to questions (10 lines)
- [ ] **Total additions:** ~20 lines to SKILL.md

### 6.2 Reference File Deployment

- [ ] **Master:** user-input-guidance.md exists in ideation/references/
- [ ] **Orchestration Copy:** user-input-guidance.md copied to orchestration/references/
- [ ] **Operational:** user-input-guidance.md synced to .claude/skills/devforgeai-orchestration/
- [ ] **Checksums:** All 3 copies have identical SHA256 hashes

### 6.3 Testing

- [ ] **Sprint Mode Tests:** 5 tests (mode detection, epic selection, story selection, capacity, enforcement)
- [ ] **Integration Tests:** 1 test (sprint full flow)
- [ ] **Regression Tests:** 10 existing orchestration tests all passing
- [ ] **Total:** 16 orchestration-specific tests (5 + 1 + 10)

### 6.4 Documentation

- [ ] **This Reference File:** Created and reviewed (~200 lines for sprint mode)
- [ ] **Sprint Pattern Mapping Table:** Completed (Section 2.1)
- [ ] **Examples:** 3 sprint mode examples
- [ ] **Deployment Process:** Step-by-step instructions provided

---

## Section 7: Success Validation

**Sprint Mode Validation:**
✅ Context marker `**Command:** create-sprint` detected
✅ guidance_content = Read(...) executes
✅ Log: "Sprint planning mode detected"
✅ Phase 3 Step 1 questions use guidance patterns:
  - Epic selection: Bounded + Explicit None (all epics + None)
  - Story selection: Multi-Select (all stories, running total)
  - Capacity guidance: Warnings for <20 or >40 points
✅ Sprint file created with capacity note

**Backward Compatibility Validation:**
✅ All 10 existing orchestration tests pass
✅ Story management mode behavior unchanged (no guidance)
✅ No breaking changes to SKILL interface
✅ Other modes (audit, checkpoint) unaffected
✅ Guidance is non-blocking (if file missing, continues)

---

## Section 8: Consistency Across All 3 Skills

**Same Guidance File:**
- Architecture uses: `.claude/skills/spec-driven-architecture/references/user-input-guidance.md`
- UI-Generator uses: `.claude/skills/devforgeai-ui-generator/references/user-input-guidance.md`
- Orchestration uses: `.claude/skills/devforgeai-orchestration/references/user-input-guidance.md`
- All 3 are IDENTICAL copies (checksum validated)

**Pattern Name Consistency:**
- Open-Ended Discovery (all 3 use)
- Bounded Choice (all 3 use)
- Explicit Classification (all 3 use)
- Closed Confirmation (architecture only)
- Custom patterns for multi-select with capacity (orchestration only)

**Fallback Behavior:**
- If guidance file missing: Log warning, use baseline questions
- If guidance file corrupted: Log error, graceful degradation
- If pattern not found: Log info, use fallback logic
- NO workflow halting (all non-blocking)

---

**Version 1.0** | **Status: Published** | **Created: 2025-01-21**
