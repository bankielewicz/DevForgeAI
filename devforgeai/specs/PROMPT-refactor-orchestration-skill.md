# Refactor devforgeai-orchestration Skill - Progressive Disclosure Implementation

## Context

The `devforgeai-orchestration` skill currently violates DevForgeAI's own architectural constraints:

**Current State**:
- File: `.claude/skills/devforgeai-orchestration/SKILL.md`
- Size: 1,652 lines (51KB)
- Status: ❌ **65% over maximum allowed (1,000 lines)**
- Token consumption: ~51,000 tokens when loaded
- References: ✅ 3 reference files already exist

**Target State**:
- Main SKILL.md: 630-640 lines (~21KB) - **Apply Phase 1.2 perfect targeting**
- Reference files: 5-6 files in `references/` subdirectory
- Expected token savings: **62%** (load ~20K tokens typically, ~45K when references needed)

**Constraints to Follow**:
- `.devforgeai/context/tech-stack.md` - Component size limits
- `.devforgeai/context/coding-standards.md` - Progressive disclosure pattern
- `.devforgeai/context/source-tree.md` - Directory structure rules
- `.devforgeai/context/anti-patterns.md` - Size violation prevention

**Lessons from Phase 1.1 and 1.2**:
- ✅ Phase 1.1 (QA): 701 lines acceptable, but 17% over target
- ⭐ Phase 1.2 (Release): 633 lines PERFECT (middle of 600-650 target) - **GOLD STANDARD**
- 🎯 Phase 1.3 target: **630-640 lines** (match Phase 1.2 excellence)

## Objective

Refactor `devforgeai-orchestration` skill to implement **progressive disclosure pattern**:
1. Keep core workflow instructions in main SKILL.md (630-640 lines)
2. Extract detailed procedures to reference files (loaded on demand)
3. Maintain all functionality while achieving 62% token efficiency gain
4. Follow DevForgeAI's own architectural standards
5. Preserve existing 3 reference files and create 2-3 new files

## Requirements

### Mandatory Actions

1. **Read Current Implementation**
   ```
   Read(file_path=".claude/skills/devforgeai-orchestration/SKILL.md")
   ```

2. **Read Framework Context Files** (understand constraints)
   ```
   Read(file_path=".devforgeai/context/tech-stack.md")
   Read(file_path=".devforgeai/context/source-tree.md")
   Read(file_path=".devforgeai/context/coding-standards.md")
   Read(file_path=".devforgeai/context/architecture-constraints.md")
   ```

3. **Check Existing Reference Files**
   ```
   Bash(command="ls -lh .claude/skills/devforgeai-orchestration/references/")
   ```

4. **Read Existing References** to understand content
   ```
   Read(file_path=".claude/skills/devforgeai-orchestration/references/workflow-states.md")
   Read(file_path=".claude/skills/devforgeai-orchestration/references/state-transitions.md")
   Read(file_path=".claude/skills/devforgeai-orchestration/references/quality-gates.md")
   ```

5. **Create 2-3 New Reference Files**

6. **Refactor Main SKILL.md** (reduce to 630-640 lines)

7. **Validate Result** (check line count, test references)

### Existing Reference Files (Keep and Enhance)

The orchestration skill already has 3 reference files:

1. ✅ **`workflow-states.md`** (14.4KB, ~480 lines)
   - Contains: 11 workflow state definitions
   - Status: Keep as-is, ensure SKILL.md references properly

2. ✅ **`state-transitions.md`** (28.5KB, ~950 lines)
   - Contains: State transition rules and validations
   - Status: Keep as-is, main SKILL.md should reference not duplicate

3. ✅ **`quality-gates.md`** (25.3KB, ~845 lines)
   - Contains: Quality gate requirements and enforcement
   - Status: Keep as-is

**Total Existing Reference Content**: ~2,275 lines across 3 files

**Note**: The SKILL.md references 5 files (lines 1638-1642):
- workflow-states.md ✅ EXISTS
- state-transitions.md ✅ EXISTS
- quality-gates.md ✅ EXISTS
- epic-management.md ❌ REFERENCED BUT MISSING
- sprint-planning.md ❌ REFERENCED BUT MISSING

### New Reference Files to Create

#### 4. `references/epic-management.md` (NEW - REFERENCED BUT MISSING)
**Content to Extract**:
- Epic document structure and YAML frontmatter
- Epic creation procedures
- Epic → Feature decomposition logic
- Epic estimation techniques
- Epic status tracking
- Epic completion criteria

**Estimated Size**: 300-400 lines

**What Stays in Main SKILL.md**:
```markdown
## Epic Management
Create and manage epics (high-level business initiatives).
For detailed epic planning procedures, see references/epic-management.md

Example workflow:
1. Read requirements from ideation phase
2. Create epic document with YAML frontmatter
3. Decompose into features
4. Link to related stories
```

#### 5. `references/sprint-planning.md` (NEW - REFERENCED BUT MISSING)
**Content to Extract**:
- Sprint document structure and YAML frontmatter
- Sprint capacity calculation (story points, team velocity)
- Story selection from backlog (priority, dependencies)
- Sprint goal definition
- Sprint metrics and burndown tracking
- Sprint retrospective procedures

**Estimated Size**: 300-400 lines

**What Stays in Main SKILL.md**:
```markdown
## Sprint Planning
Plan 2-week iterations with story selection.
For detailed sprint planning procedures, see references/sprint-planning.md

Example workflow:
1. Calculate team capacity
2. Select stories from backlog
3. Validate dependencies
4. Create sprint document
```

#### 6. `references/story-management.md` (NEW - CONSOLIDATE STORY OPERATIONS)
**Content to Extract**:
- Story document structure with complete YAML frontmatter example
- Acceptance criteria format (Given/When/Then)
- Technical specification template
- Non-functional requirements template
- Story estimation techniques
- Story status update procedures
- Workflow history format and templates

**Estimated Size**: 400-500 lines

**What Stays in Main SKILL.md**:
```markdown
## Story Creation
Create story documents with acceptance criteria.
For story document structure, see references/story-management.md

Required sections:
- YAML frontmatter (id, title, epic, sprint, status, points, priority)
- User story ("As a [role], I want [feature], so that [benefit]")
- Acceptance criteria (Given/When/Then)
- Technical specification
```

**Why This Reference is Needed**:
Currently, the main SKILL.md likely has extensive inline examples of:
- Story document templates (50-100 lines)
- Workflow history entry formats (50-100 lines)
- Epic and sprint document structures (50-100 lines)

This content should be in reference files for on-demand loading.

### Key Extraction Strategy

**Analyze Current SKILL.md Content Distribution**:

Based on structure (1,652 lines total), likely breakdown:
- Lines 1-100: Frontmatter, purpose, when to use (~100 lines)
- Lines 101-300: Workflow states overview (~200 lines) → **Can reduce to ~50 lines + reference**
- Lines 301-700: Skill coordination logic (~400 lines) → **Core workflow, keep most**
- Lines 701-1000: Quality gate enforcement (~300 lines) → **Extract to references/quality-gates.md**
- Lines 1001-1400: Story/Epic/Sprint operations (~400 lines) → **Extract to new references**
- Lines 1401-1550: State update procedures (~150 lines) → **Extract to references/story-management.md**
- Lines 1551-1652: Success criteria, references (~100 lines) → **Keep, consolidate**

**Extraction Plan**:

1. **Workflow States Overview** (lines 101-300, ~200 lines)
   - **Remove**: Detailed 11-state definitions (already in workflow-states.md)
   - **Keep**: Brief state list (20 lines) + reference to workflow-states.md
   - **Savings**: ~180 lines

2. **Quality Gate Details** (embedded throughout, ~150 lines)
   - **Remove**: Detailed gate validation procedures (already in quality-gates.md)
   - **Keep**: Brief gate enforcement logic (30 lines) + references
   - **Savings**: ~120 lines

3. **State Transition Logic** (embedded throughout, ~200 lines)
   - **Remove**: Detailed transition rules (already in state-transitions.md)
   - **Keep**: Core orchestration flow (50 lines) + references
   - **Savings**: ~150 lines

4. **Epic Document Templates** (~100 lines)
   - **Extract to**: references/epic-management.md (NEW)
   - **Keep**: Brief creation workflow (20 lines)
   - **Savings**: ~80 lines

5. **Sprint Document Templates** (~100 lines)
   - **Extract to**: references/sprint-planning.md (NEW)
   - **Keep**: Brief planning workflow (20 lines)
   - **Savings**: ~80 lines

6. **Story Document Templates and Procedures** (~200 lines)
   - **Extract to**: references/story-management.md (NEW)
   - **Keep**: Brief story creation workflow (40 lines)
   - **Savings**: ~160 lines

7. **Verbose Decision Trees** (lines 880-950, ~70 lines)
   - **Condense**: Simplify decision tree representation
   - **Extract**: Detailed next action logic to reference
   - **Savings**: ~40 lines

8. **Workflow History Entry Formats** (~100 lines)
   - **Extract to**: references/story-management.md
   - **Keep**: Brief append logic (20 lines)
   - **Savings**: ~80 lines

**Total Estimated Savings**: ~890 lines
**Target Achievement**: 1,652 - 890 = ~762 lines

**Additional Optimization Needed**: 762 → 635 target = ~130 more lines

9. **Condense Phase Descriptions** (~60 lines)
   - Tighten language in Phase 1-5
   - Remove explanatory paragraphs
   - Keep direct instructions only

10. **Simplify Code Examples** (~40 lines)
    - Keep essential examples
    - Remove redundant variations

11. **Consolidate Validation Steps** (~30 lines)
    - Similar validation patterns across phases
    - Create validation template

**Final Target**: 1,652 - 1,020 = **632 lines** (perfect middle of 630-640 target!)

### Refactored SKILL.md Structure

**Target Structure** (630-640 lines total):

```markdown
---
name: devforgeai-orchestration
description: [Keep existing description]
allowed-tools: [Keep existing - simple and clean]
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - AskUserQuestion
  - Skill
---

# DevForgeAI Orchestration Skill

[Keep existing purpose statement - ~60 lines]

## Purpose

[Keep core responsibilities - ~40 lines]

## When to Use This Skill

[Keep usage guidance with entry point examples - ~30 lines]

---

## Workflow States

### 11 Story States (Brief Overview)

```
1. Backlog → 2. Architecture → 3. Ready for Dev → 4. In Development →
5. Dev Complete → 6. QA In Progress → 7. QA Failed/QA Approved →
8. Releasing → 9. Released
```

For detailed state definitions, see `references/workflow-states.md`
For transition rules, see `references/state-transitions.md`

---

## Orchestration Workflow

### Phase 1: Load and Validate Story (~60 lines)

#### Step 1: Load Story Document
- Read story file
- Parse YAML frontmatter
- Extract current status
- Identify epic and sprint

#### Step 2: Validate Current State
- Check status is valid workflow state
- Verify prerequisites for requested transition
- For validation rules, see references/state-transitions.md

#### Step 3: Validate Quality Gates
- Check gate requirements for current → next transition
- For gate requirements, see references/quality-gates.md
- HALT if gate requirements not met

---

### Phase 2: Orchestrate Skill Invocation (~120 lines)

#### Architecture Phase (Backlog → Ready for Dev)
- Check for context files
- If missing: Invoke devforgeai-architecture
- Wait for completion
- Validate all 6 context files created
- Update story status

For context validation gate, see references/quality-gates.md

#### Development Phase (Ready for Dev → Dev Complete)
- Invoke devforgeai-development --story={story_id}
- Wait for TDD workflow completion
- Validate tests pass
- Update story status

For test passing gate, see references/quality-gates.md

#### QA Phase (Dev Complete → QA Approved/Failed)
- Invoke devforgeai-qa --mode=deep --story={story_id}
- Wait for validation completion
- Parse QA report
- Update story status based on results

For QA approval gate, see references/quality-gates.md

#### Release Phase (QA Approved → Released)
- Invoke devforgeai-release --story={story_id}
- Wait for deployment completion
- Validate deployment success
- Update story status

For release readiness gate, see references/quality-gates.md

---

### Phase 3: Update Story Status (~80 lines)

#### Update Frontmatter
```
Edit(file_path="devforgeai/specs/Stories/{story_id}.story.md",
     old_string="status: {old_status}",
     new_string="status: {new_status}")
```

#### Update Workflow Checkboxes
- Mark phase as complete: `- [ ]` → `- [x]`
- Track progress through workflow

#### Append Workflow History
```
### {timestamp} - {new_status}
- **Previous Status:** {old_status}
- **Action:** {description}
- **Result:** {summary}
```

For workflow history format, see references/story-management.md

---

### Phase 4: Epic and Sprint Management (~80 lines)

#### Epic Creation
- Load requirements from ideation phase
- Create epic document with YAML frontmatter
- Decompose into features
- Estimate epic effort

For epic planning procedures, see references/epic-management.md

#### Sprint Planning
- Calculate team capacity
- Select stories from backlog
- Create sprint document
- Track sprint progress

For sprint planning procedures, see references/sprint-planning.md

---

### Phase 5: Determine Next Action (~60 lines)

Based on current state, determine next orchestration action:

```
IF status == "Backlog":
    Next: Architecture (invoke devforgeai-architecture)

IF status == "Ready for Dev":
    Next: In Development (await developer or invoke devforgeai-development)

IF status == "Dev Complete":
    Next: QA In Progress (invoke devforgeai-qa)

IF status == "QA Approved":
    Next: Releasing (invoke devforgeai-release)
```

For complete decision tree, see references/state-transitions.md

---

## Quality Gate Enforcement (~60 lines)

Brief overview of 4 gates:
1. Context Validation Gate (Architecture → Ready for Dev)
2. Test Passing Gate (Dev Complete → QA In Progress)
3. QA Approval Gate (QA Approved → Releasing)
4. Release Readiness Gate (Releasing → Released)

For detailed gate requirements, see references/quality-gates.md

---

## Tool Usage Protocol (~40 lines)

### Use Native Tools for File Operations
[Keep brief examples - ~20 lines]

### Use Skill Tool for Orchestration
[Keep brief examples - ~20 lines]

---

## Reference Materials (~40 lines)

Load these on demand during orchestration:

### State Management
- **`./references/workflow-states.md`** - Detailed 11-state definitions
- **`./references/state-transitions.md`** - Transition rules, validations, decision trees
- **`./references/quality-gates.md`** - Gate requirements and enforcement procedures

### Project Management
- **`./references/epic-management.md`** - Epic planning, decomposition, estimation
- **`./references/sprint-planning.md`** - Sprint capacity, story selection, tracking

### Story Operations
- **`./references/story-management.md`** - Story structure, status updates, workflow history

---

## Success Criteria (~40 lines)

[Keep existing success criteria, condensed]
```

**Total Estimated**: ~635 lines (within 630-640 perfect target!)

### Validation Steps

After refactoring, validate the result:

```bash
# 1. Check line count
wc -l .claude/skills/devforgeai-orchestration/SKILL.md
# Expected: 630-640 lines (match Phase 1.2 perfection!)

# 2. Check reference files exist
ls -lh .claude/skills/devforgeai-orchestration/references/
# Expected: 6 files (3 existing + 3 new)

# 3. Verify new reference files created
ls -lh .claude/skills/devforgeai-orchestration/references/epic-management.md
ls -lh .claude/skills/devforgeai-orchestration/references/sprint-planning.md
ls -lh .claude/skills/devforgeai-orchestration/references/story-management.md
# Expected: All exist

# 4. Verify all referenced files exist (no broken links)
grep -o "references/[^)]*\.md" .claude/skills/devforgeai-orchestration/SKILL.md | sort -u
# Compare with actual files in references/

# 5. Check for duplication reduction
grep -c "YAML frontmatter" .claude/skills/devforgeai-orchestration/SKILL.md
# Expected: 1-2 brief mentions (vs many in original)
```

### Key Implementation Guidelines

#### ✅ DO (Apply Phase 1.2 Gold Standard)

1. **Target 630-640 Lines Exactly**
   - Phase 1.2 achieved 633 lines = perfect
   - Don't settle for 700 (Phase 1.1)
   - Don't over-optimize to 550 (sacrifices clarity)
   - **Sweet spot: 635 lines** ⭐

2. **Leverage Existing Reference Files Aggressively**
   ```markdown
   ✅ CORRECT:
   ## Workflow States
   Stories progress through 11 states.
   For detailed state definitions, see references/workflow-states.md

   [List only the 11 state names, ~10 lines]
   ```

   ```markdown
   ❌ WRONG:
   ## Workflow States
   [200 lines of detailed state definitions already in workflow-states.md]
   ```

3. **Keep Brief Code Examples** (Phase 1.2 pattern)
   ```markdown
   ✅ CORRECT:
   Example orchestration:
   1. Check story status
   2. Invoke appropriate skill
   3. Wait for completion
   4. Update story status

   For complete orchestration procedures, see references/state-transitions.md
   ```

4. **Create Comprehensive New Reference Files**
   - epic-management.md should cover ALL epic operations (300-400 lines)
   - sprint-planning.md should cover ALL sprint operations (300-400 lines)
   - story-management.md should cover ALL story operations (400-500 lines)
   - Better than multiple small fragmented files

5. **Remove Duplication from Existing References**
   - If workflow-states.md has state definitions, don't repeat in main
   - If state-transitions.md has transition rules, don't repeat in main
   - If quality-gates.md has gate procedures, don't repeat in main

#### ❌ DON'T

1. **Don't Duplicate Existing Reference Content**
   ```markdown
   ❌ WRONG:
   ## Quality Gates
   [150 lines of gate validation already in quality-gates.md]

   ✅ CORRECT:
   ## Quality Gate Enforcement
   4 gates enforce workflow integrity:
   1. Context Validation (Architecture → Ready for Dev)
   2. Test Passing (Dev Complete → QA In Progress)
   3. QA Approval (QA Approved → Releasing)
   4. Release Readiness (Releasing → Released)

   For gate requirements, see references/quality-gates.md
   ```

2. **Don't Include Verbose Templates Inline**
   ```markdown
   ❌ WRONG:
   ## Story Template
   [100 lines of complete story document template]

   ✅ CORRECT:
   ## Story Creation
   Create story with required sections.
   For story template, see references/story-management.md
   ```

3. **Don't Settle for 700 Lines**
   - Phase 1.1 accepted 701 (acceptable but not ideal)
   - Phase 1.2 achieved 633 (gold standard)
   - Phase 1.3 should match Phase 1.2: **630-640 lines**

4. **Don't Break Referenced Files**
   - The SKILL.md already references epic-management.md and sprint-planning.md
   - These files MUST be created (currently missing)
   - All 6 reference links must be valid

### Expected Outcome

**Before**:
```
.claude/skills/devforgeai-orchestration/
├── SKILL.md (1,652 lines, 51KB, ~51,000 tokens)
└── references/
    ├── workflow-states.md (~480 lines) ✅ EXISTING
    ├── state-transitions.md (~950 lines) ✅ EXISTING
    └── quality-gates.md (~845 lines) ✅ EXISTING
```

**After**:
```
.claude/skills/devforgeai-orchestration/
├── SKILL.md (630-640 lines, ~21KB, ~20,000 tokens)
├── SKILL.md.backup (1,652 lines, preserved for reference)
└── references/
    ├── workflow-states.md (~480 lines) ✅ EXISTING
    ├── state-transitions.md (~950 lines) ✅ EXISTING
    ├── quality-gates.md (~845 lines) ✅ EXISTING
    ├── epic-management.md (~350 lines) ✅ NEW
    ├── sprint-planning.md (~350 lines) ✅ NEW
    └── story-management.md (~450 lines) ✅ NEW
```

**Token Efficiency Gain**:
- Typical usage: Load SKILL.md only = ~20,000 tokens (62% reduction!)
- With state transitions: SKILL.md + state-transitions.md = ~32,000 tokens (37% reduction)
- With story management: SKILL.md + story-management.md = ~28,000 tokens (45% reduction)
- Maximum usage: SKILL.md + all 6 references = ~52,000 tokens (only when managing epic+sprint+story simultaneously)

**Framework Compliance**:
- ✅ Within perfect target (630-640 lines)
- ✅ Follows progressive disclosure pattern
- ✅ Uses native tools over Bash
- ✅ All reference files exist (no broken links)
- ✅ Follows source-tree.md directory structure
- ✅ 100% framework compliance (match Phase 1.2)

### Testing the Refactored Skill

After completing the refactor, test with:

```bash
# Start Claude Code
claude

# Test story creation (should load main + story-management.md)
> Create a new story for user authentication feature

# Claude should:
# 1. Load main SKILL.md (~20K tokens)
# 2. Load story-management.md (~12K tokens)
# 3. Total: ~32K tokens (vs 51K original = 37% reduction)
# 4. Create story document successfully

# Test story progression (should load main + state-transitions.md)
> Move STORY-001 from Backlog to Architecture phase

# Claude should:
# 1. Load main SKILL.md
# 2. Load state-transitions.md for validation rules
# 3. Check quality gate
# 4. Update story status
# 5. Invoke devforgeai-architecture if needed

# Test sprint planning (should load main + sprint-planning.md)
> Create sprint plan for Sprint 1

# Claude should:
# 1. Load main SKILL.md
# 2. Load sprint-planning.md for capacity and selection logic
# 3. Create sprint document
# 4. Select stories from backlog
```

### Deliverables Checklist

When you complete this refactor, you should have:

- [ ] Main SKILL.md reduced to 630-640 lines (target: 635 lines ⭐)
- [ ] 3 new reference files created (epic-management, sprint-planning, story-management)
- [ ] 3 existing reference files preserved and properly referenced
- [ ] All 6 reference links working (no broken links)
- [ ] No functionality lost (all orchestration capabilities preserved)
- [ ] No content duplication between main and references
- [ ] Line count validated: `wc -l .claude/skills/devforgeai-orchestration/SKILL.md`
- [ ] Directory structure validated: `ls -la .claude/skills/devforgeai-orchestration/references/`
- [ ] Tested skill invocation successfully
- [ ] Token usage reduced by ~62% for typical usage

### Success Criteria

The refactor is successful when:

1. **Size Compliance**: SKILL.md is 630-640 lines (match Phase 1.2 perfection!)
2. **Progressive Disclosure**: References load on demand
3. **Functionality Preserved**: All orchestration capabilities work
4. **Framework Compliant**: Follows all context file constraints
5. **Token Efficient**: 62% reduction in typical token usage
6. **No Broken Links**: All 6 referenced files exist (3 existing + 3 new)
7. **Quality Score**: 9.0-9.5/10 (match or exceed Phase 1.2)

---

## Commands to Execute in Session

```bash
# 1. Read current implementation
Read(file_path=".claude/skills/devforgeai-orchestration/SKILL.md")

# 2. Read context files
Read(file_path=".devforgeai/context/tech-stack.md")
Read(file_path=".devforgeai/context/coding-standards.md")
Read(file_path=".devforgeai/context/source-tree.md")

# 3. Read existing reference files to understand content
Read(file_path=".claude/skills/devforgeai-orchestration/references/workflow-states.md")
Read(file_path=".claude/skills/devforgeai-orchestration/references/state-transitions.md")
Read(file_path=".claude/skills/devforgeai-orchestration/references/quality-gates.md")

# 4. Create backup of original
Bash(command="cp .claude/skills/devforgeai-orchestration/SKILL.md .claude/skills/devforgeai-orchestration/SKILL.md.backup")

# 5. Create new reference files (use Write tool for each)
Write(file_path=".claude/skills/devforgeai-orchestration/references/epic-management.md", content="...")
Write(file_path=".claude/skills/devforgeai-orchestration/references/sprint-planning.md", content="...")
Write(file_path=".claude/skills/devforgeai-orchestration/references/story-management.md", content="...")

# 6. Rewrite main SKILL.md (use Write to replace entire file)
Write(file_path=".claude/skills/devforgeai-orchestration/SKILL.md", content="[630-640 line refactored version]")

# 7. Validate
Bash(command="wc -l .claude/skills/devforgeai-orchestration/SKILL.md")
Bash(command="ls -lh .claude/skills/devforgeai-orchestration/references/")
Bash(command="grep -o 'references/[^)]*\\.md' .claude/skills/devforgeai-orchestration/SKILL.md | sort -u")
```

---

## Specific Content to Extract

### From Main SKILL.md to epic-management.md

**Extract**:
- Epic document YAML frontmatter example (complete template)
- Epic → Feature decomposition procedures
- Epic estimation techniques (story point aggregation)
- Epic status tracking logic
- Epic completion criteria
- Epic-to-story linking procedures

**Keep in Main**:
```markdown
## Epic Management
Create and track high-level business initiatives.

Workflow:
1. Load requirements from ideation
2. Create epic document (see references/epic-management.md for template)
3. Decompose into features
4. Link stories to epic
```

### From Main SKILL.md to sprint-planning.md

**Extract**:
- Sprint document YAML frontmatter example (complete template)
- Team capacity calculation formulas
- Velocity tracking methods
- Story selection algorithms (priority, dependencies, capacity)
- Sprint goal definition guidelines
- Burndown tracking procedures
- Sprint retrospective template

**Keep in Main**:
```markdown
## Sprint Planning
Plan 2-week iterations.

Workflow:
1. Calculate capacity (see references/sprint-planning.md for methodology)
2. Select stories from backlog
3. Create sprint document
4. Track progress
```

### From Main SKILL.md to story-management.md

**Extract**:
- Complete story document template with all sections
- YAML frontmatter field definitions (id, title, epic, sprint, status, points, priority, etc.)
- Acceptance criteria format (Given/When/Then examples)
- Technical specification template
- Non-functional requirements template
- Story status update procedures (Edit commands for frontmatter)
- Workflow history entry format and examples
- Workflow checkbox update logic

**Keep in Main**:
```markdown
## Story Creation
Create atomic work units with acceptance criteria.

Required sections:
- YAML frontmatter
- User story format
- Acceptance criteria
- Technical specification

For complete story template, see references/story-management.md
```

### Remove Duplication of Existing References

**Workflow States** (currently ~200 lines inline):
- **Remove**: Detailed 11-state definitions
- **Keep**: Brief list (11 state names, ~10 lines)
- **Reference**: workflow-states.md (already exists with 480 lines)

**State Transitions** (currently ~200 lines inline):
- **Remove**: Detailed transition validation logic
- **Keep**: Brief orchestration flow (50 lines)
- **Reference**: state-transitions.md (already exists with 950 lines)

**Quality Gates** (currently ~150 lines inline):
- **Remove**: Detailed gate validation procedures
- **Keep**: Brief gate list with HALT logic (40 lines)
- **Reference**: quality-gates.md (already exists with 845 lines)

---

## Post-Refactor Review Prompt

After completing the refactor in a new session, use this prompt for review:

```
I've completed the refactor of devforgeai-orchestration skill. Please review:

1. Check line count: Is SKILL.md 630-640 lines? (Target: 635 to match Phase 1.2 perfection)
2. Check references: Are all 6 files present (3 existing + 3 new)?
3. Check new files: Do epic-management.md, sprint-planning.md, story-management.md exist?
4. Check links: Do all references/[file].md links work?
5. Check functionality: Are all orchestration capabilities preserved?
6. Check compliance: Does it follow context file constraints?
7. Check duplication: Is content properly separated between main and references?
8. Compare with Phase 1.2: Did we achieve similar quality (9.0-9.5/10)?

Files to review:
- .claude/skills/devforgeai-orchestration/SKILL.md
- .claude/skills/devforgeai-orchestration/references/epic-management.md
- .claude/skills/devforgeai-orchestration/references/sprint-planning.md
- .claude/skills/devforgeai-orchestration/references/story-management.md

Run validation:
- wc -l .claude/skills/devforgeai-orchestration/SKILL.md
- ls -la .claude/skills/devforgeai-orchestration/references/
- grep "references/" .claude/skills/devforgeai-orchestration/SKILL.md | sort -u
```

---

## Success Metrics Targets (Match Phase 1.2)

| Metric | Phase 1.2 (Release) | Phase 1.3 Target (Orchestration) |
|--------|---------------------|----------------------------------|
| **Line Count** | 633 lines | 630-640 lines (target: 635) ✅ |
| **Size Reduction** | 63% (1,734→633) | 62% (1,652→635) ✅ |
| **Target Achievement** | Perfect middle (633) | Perfect middle (635) ✅ |
| **Token Savings** | 65% typical | 62% typical ✅ |
| **Reference Files** | 6 (5+1) | 6 (3+3) ✅ |
| **Framework Compliance** | 100% (10/10) | 100% (10/10) ✅ |
| **Quality Score** | 9.5/10 | 9.0-9.5/10 ✅ |

**Goal**: Match Phase 1.2 excellence with 630-640 line targeting

---

## Phase 1.3 Quality Targets

### Must Achieve (Critical)
- [ ] Line count: 630-640 (not 700+)
- [ ] All 6 reference files exist (3 existing + 3 new)
- [ ] Zero broken reference links
- [ ] All workflow capabilities preserved
- [ ] 62% token reduction for typical usage

### Should Achieve (High Priority)
- [ ] Create comprehensive new reference files (350-450 lines each)
- [ ] Remove all duplication with existing references
- [ ] Keep brief code examples for clarity
- [ ] 100% framework compliance
- [ ] Quality score 9.0+/10

### Nice to Have (Medium Priority)
- [ ] Quality score 9.5/10 (match Phase 1.2)
- [ ] Perfect 635 lines (mathematical middle of 630-640)
- [ ] Zero content duplication anywhere
- [ ] Superior workflow clarity vs original

---

## Key Differences from Phase 1.1 and 1.2

**Phase 1.3 Unique Characteristics**:

1. **3 Existing References vs 0/5**
   - Phase 1.1 (QA): Created 7 new files
   - Phase 1.2 (Release): 5 existing + 1 new
   - Phase 1.3 (Orchestration): 3 existing + 3 new

2. **2 Referenced But Missing Files**
   - epic-management.md and sprint-planning.md are referenced in current SKILL.md but don't exist
   - **Must create these** to fix broken links

3. **Project Management Focus**
   - Orchestration manages epics, sprints, stories (project management artifacts)
   - Less technical than QA/Release (no test coverage, no deployments)
   - More about coordination and state management

4. **State Machine Complexity**
   - 11 workflow states with complex transition rules
   - Already well-documented in state-transitions.md (950 lines)
   - Main challenge: Don't duplicate this in main SKILL.md

---

## Implementation Priority

**Day 1 Focus**: Create missing reference files first
1. epic-management.md (fix broken link)
2. sprint-planning.md (fix broken link)
3. story-management.md (consolidate story operations)

**Day 1-2 Focus**: Refactor main SKILL.md
1. Remove duplication with workflow-states.md (~180 lines)
2. Remove duplication with state-transitions.md (~150 lines)
3. Remove duplication with quality-gates.md (~120 lines)
4. Extract epic/sprint templates to new references (~200 lines)
5. Extract story operations to story-management.md (~160 lines)
6. Condense remaining content (~100 lines)

**Target**: 1,652 - 1,010 = **642 lines** (within 630-640 acceptable range)

**Refinement**: Trim 7 lines to hit perfect 635 target ⭐

---

**Remember**: Apply all lessons from Phase 1.2 (gold standard):
- Target 630-640 lines exactly (sweet spot: 635)
- Leverage existing reference files aggressively
- Create comprehensive new reference files (350-450 lines each)
- Keep brief code examples in main file for clarity
- Remove all duplication with existing references
- Fix broken links (epic-management.md, sprint-planning.md)
- Achieve 100% framework compliance
- Quality score target: 9.0-9.5/10

**Phase 1.3 Objective**: Match or exceed Phase 1.2 excellence (9.5/10) while fixing broken reference links.
