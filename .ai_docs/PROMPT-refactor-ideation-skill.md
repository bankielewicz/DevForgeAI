# Refactor devforgeai-ideation Skill - Progressive Disclosure Implementation

## Context

The `devforgeai-ideation` skill currently violates DevForgeAI's own architectural constraints:

**Current State**:
- File: `.claude/skills/devforgeai-ideation/SKILL.md`
- Size: 985 lines (30KB)
- Status: ❌ **98.5% of maximum, 41-55% over soft target (600-700)**
- Token consumption: ~30,000 tokens when loaded
- References: ✅ **ALL 4 reference files already exist!**
  - requirements-elicitation-guide.md (723 lines) ✅
  - complexity-assessment-matrix.md (700 lines) ✅
  - domain-specific-patterns.md (975 lines) ✅
  - feasibility-analysis-framework.md (649 lines) ✅

**Target State**:
- Main SKILL.md: 650-700 lines (~22KB)
- Reference files: 4 existing files (already complete!)
- Expected token savings: **60%** (load ~12K tokens typically, ~25K when references needed)

**Key Advantage**: This is the **EASIEST refactor** of all 5 skills because all reference files already exist. You just need to refactor the main SKILL.md to properly use them via progressive disclosure.

**Constraints to Follow**:
- `.devforgeai/context/tech-stack.md` - Component size limits
- `.devforgeai/context/coding-standards.md` - Progressive disclosure pattern
- `.devforgeai/context/source-tree.md` - Directory structure rules
- `.devforgeai/context/anti-patterns.md` - Size violation prevention

**Lessons from Phase 1.1, 1.2, 1.3**:
- ✅ Phase 1.1 (QA): 701 lines acceptable with code examples
- ⭐ Phase 1.2 (Release): 633 lines PERFECT (middle of target)
- 🏆 Phase 1.3 (Orchestration): 496 lines OUTSTANDING (highly optimized)
- 🎯 Phase 2.1 target: **670 lines** (conservative since references exist, avoid over-optimization)

## Objective

Refactor `devforgeai-ideation` skill to implement **progressive disclosure pattern**:
1. Keep core workflow instructions in main SKILL.md (650-700 lines, target: 670)
2. Remove duplication with 4 existing reference files
3. Maintain all functionality while achieving 60% token efficiency gain
4. Follow DevForgeAI's own architectural standards
5. Utilize all 4 existing reference files properly

## Requirements

### Mandatory Actions

1. **Read Current Implementation**
   ```
   Read(file_path=".claude/skills/devforgeai-ideation/SKILL.md")
   ```

2. **Read Framework Context Files** (understand constraints)
   ```
   Read(file_path=".devforgeai/context/tech-stack.md")
   Read(file_path=".devforgeai/context/source-tree.md")
   Read(file_path=".devforgeai/context/coding-standards.md")
   ```

3. **Read All 4 Existing Reference Files** (understand what's already documented)
   ```
   Read(file_path=".claude/skills/devforgeai-ideation/references/requirements-elicitation-guide.md")
   Read(file_path=".claude/skills/devforgeai-ideation/references/complexity-assessment-matrix.md")
   Read(file_path=".claude/skills/devforgeai-ideation/references/domain-specific-patterns.md")
   Read(file_path=".claude/skills/devforgeai-ideation/references/feasibility-analysis-framework.md")
   ```

4. **Create Backup**
   ```
   Bash(command="cp .claude/skills/devforgeai-ideation/SKILL.md .claude/skills/devforgeai-ideation/SKILL.md.backup")
   ```

5. **Refactor Main SKILL.md** (reduce to 650-700 lines, target 670)

6. **Validate Result** (check line count, verify no duplication)

### Existing Reference Files (All Complete - Use Properly!)

The ideation skill has **ALL 4 recommended reference files already**:

1. ✅ **`requirements-elicitation-guide.md`** (21KB, ~723 lines)
   - Contains: Probing questions by domain (e-commerce, SaaS, fintech, healthcare)
   - Status: Comprehensive, production-ready
   - **Main SKILL.md should reference this, NOT duplicate questions**

2. ✅ **`complexity-assessment-matrix.md`** (21KB, ~700 lines)
   - Contains: Detailed 0-60 scoring rubric across 6 dimensions
   - Status: Comprehensive, production-ready
   - **Main SKILL.md should reference this, NOT duplicate scoring**

3. ✅ **`domain-specific-patterns.md`** (29KB, ~975 lines)
   - Contains: Common patterns for e-commerce, SaaS, fintech, healthcare
   - Status: Comprehensive, production-ready
   - **Main SKILL.md should reference this, NOT duplicate patterns**

4. ✅ **`feasibility-analysis-framework.md`** (19KB, ~649 lines)
   - Contains: Risk assessment checklists, technical/business/resource feasibility
   - Status: Comprehensive, production-ready
   - **Main SKILL.md should reference this, NOT duplicate analysis**

**Total Reference Content**: ~3,047 lines across 4 files (already complete!)

**Your Task**: Remove duplication from main SKILL.md and add proper progressive disclosure references.

### Key Extraction Strategy

**Find and Remove Duplication**:

The current 985-line SKILL.md likely contains content that DUPLICATES these 4 reference files. Your job is to identify and remove the duplication.

#### Expected Duplication Pattern 1: Requirements Elicitation

**Likely in Main SKILL.md** (current):
```markdown
## Phase 2: Requirements Elicitation

Ask probing questions:

### For E-Commerce Projects:
- What products will be sold?
- How will inventory be managed?
- What payment methods are needed?
[... 50-100 lines of e-commerce questions already in requirements-elicitation-guide.md]

### For SaaS Projects:
- What is the subscription model?
- How will billing work?
[... 50-100 lines of SaaS questions already in requirements-elicitation-guide.md]
```

**Should Be** (refactored):
```markdown
## Phase 2: Requirements Elicitation

Ask probing questions based on domain.

For domain-specific elicitation questions, see references/requirements-elicitation-guide.md

Core questions to ask:
1. Who are the users? (roles, personas)
2. What are the core use cases? (features, workflows)
3. What are the success metrics? (KPIs, goals)
4. What are the constraints? (technical, business, timeline)
```

**Expected Savings**: ~100-150 lines

#### Expected Duplication Pattern 2: Complexity Scoring

**Likely in Main SKILL.md** (current):
```markdown
## Phase 3: Complexity Assessment

Score complexity across 6 dimensions:

### Dimension 1: Functional Complexity (0-10 points)
- Simple CRUD: 1-3 points
- Business logic with rules: 4-6 points
- Complex workflows with state machines: 7-10 points
[... 50-80 lines of detailed scoring already in complexity-assessment-matrix.md]

### Dimension 2: Data Complexity (0-10 points)
[... detailed scoring rubric already in complexity-assessment-matrix.md]

[... continues for all 6 dimensions = 150-200 lines of duplication]
```

**Should Be** (refactored):
```markdown
## Phase 3: Complexity Assessment

Score complexity on 0-60 scale across 6 dimensions:
1. Functional Complexity (0-10)
2. Data Complexity (0-10)
3. Integration Complexity (0-10)
4. Performance Requirements (0-10)
5. Security Requirements (0-10)
6. User Scale (0-10)

For detailed scoring rubric, see references/complexity-assessment-matrix.md

Recommend architecture tier based on score:
- 0-15: Simple (monolithic app)
- 16-30: Modular (layered architecture)
- 31-45: Microservices (distributed system)
- 46-60: Enterprise (complex distributed system)
```

**Expected Savings**: ~150-200 lines

#### Expected Duplication Pattern 3: Domain Patterns

**Likely in Main SKILL.md** (current):
```markdown
## Phase 4: Epic & Feature Decomposition

Common patterns by domain:

### E-Commerce Patterns:
- User Management (registration, profiles, auth)
- Product Catalog (products, categories, search)
- Shopping Cart (add to cart, update quantities, checkout)
- Order Management (order placement, tracking, fulfillment)
- Payment Processing (payment methods, transactions, refunds)
[... 60-80 lines already in domain-specific-patterns.md]

### SaaS Patterns:
[... 60-80 lines already in domain-specific-patterns.md]

[... continues for fintech, healthcare = 200-300 lines of duplication]
```

**Should Be** (refactored):
```markdown
## Phase 4: Epic & Feature Decomposition

Break solution into manageable epics and features.

For common domain patterns (e-commerce, SaaS, fintech, healthcare), see references/domain-specific-patterns.md

Decomposition approach:
1. Identify core features from requirements
2. Group features into logical epics
3. Sequence epics by dependencies and priority
4. Estimate effort for each epic
```

**Expected Savings**: ~200-300 lines

#### Expected Duplication Pattern 4: Feasibility Analysis

**Likely in Main SKILL.md** (current):
```markdown
## Phase 5: Feasibility & Constraints Analysis

### Technical Feasibility Checklist:
- [ ] Required technologies available?
- [ ] Team has necessary skills?
- [ ] Architecture pattern appropriate?
- [ ] Performance targets achievable?
[... 40-60 lines already in feasibility-analysis-framework.md]

### Business Feasibility Checklist:
- [ ] Timeline realistic?
- [ ] Budget sufficient?
[... 40-60 lines already in feasibility-analysis-framework.md]

### Resource Constraints:
[... 40-60 lines already in feasibility-analysis-framework.md]
```

**Should Be** (refactored):
```markdown
## Phase 5: Feasibility & Constraints Analysis

Assess technical, business, and resource feasibility.

For complete feasibility assessment framework, see references/feasibility-analysis-framework.md

Key areas to analyze:
1. Technical feasibility (technology availability, team skills, architecture)
2. Business feasibility (timeline, budget, resources)
3. Risk assessment (technical risks, dependencies, unknowns)
```

**Expected Savings**: ~80-120 lines

### Total Expected Duplication Removal

**Estimated Duplication**: 530-770 lines
- Requirements elicitation: ~100-150 lines
- Complexity scoring: ~150-200 lines
- Domain patterns: ~200-300 lines
- Feasibility analysis: ~80-120 lines

**Projected Result**: 985 - 650 (midpoint) = **335 lines to remove**

**Approach**: Remove ~335 lines of duplication while keeping essential workflow structure

### Refactored SKILL.md Structure

**Target Structure** (650-700 lines, target: 670):

```markdown
---
name: devforgeai-ideation
description: [Keep existing description]
allowed-tools: [Keep existing]
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - AskUserQuestion
  - Skill
---

# DevForgeAI Ideation Skill

[Keep existing purpose statement - ~80 lines]

## Purpose

[Keep 6-phase process overview - ~40 lines]

## When to Use This Skill

[Keep usage guidance - ~40 lines]

---

## Ideation Workflow (6 Phases)

### Phase 1: Discovery & Problem Understanding (~80 lines)

#### Step 1: Understand Business Context
- Business objectives and goals
- Target market and competition
- Success metrics and KPIs

#### Step 2: Identify Users and Use Cases
- User personas and roles
- Core user journeys
- Pain points and needs

#### Step 3: Define Success Criteria
- What does success look like?
- How will it be measured?
- What are the constraints?

**Brief examples** (5-10 lines of key questions)

For comprehensive discovery questions, see references/requirements-elicitation-guide.md

---

### Phase 2: Requirements Elicitation (~90 lines)

#### Step 1: Functional Requirements
- Core features and capabilities
- User workflows and interactions
- System behaviors

#### Step 2: Non-Functional Requirements
- Performance targets
- Security requirements
- Scalability needs

#### Step 3: Domain-Specific Requirements
- Industry-specific needs
- Compliance requirements

**Brief examples** (5-10 lines per type)

For domain-specific probing questions (e-commerce, SaaS, fintech, healthcare), see references/requirements-elicitation-guide.md

---

### Phase 3: Complexity Assessment (~100 lines)

#### Step 1: Score Across 6 Dimensions
```
1. Functional Complexity (0-10 points)
2. Data Complexity (0-10 points)
3. Integration Complexity (0-10 points)
4. Performance Requirements (0-10 points)
5. Security Requirements (0-10 points)
6. User Scale (0-10 points)

Total Score: 0-60 points
```

#### Step 2: Recommend Architecture Tier
```
0-15 points:   Simple (monolithic app)
16-30 points:  Modular (layered architecture)
31-45 points:  Microservices (distributed system)
46-60 points:  Enterprise (complex distributed system)
```

**Brief scoring example** (10-15 lines)

For detailed scoring rubric and dimension definitions, see references/complexity-assessment-matrix.md

---

### Phase 4: Epic & Feature Decomposition (~90 lines)

#### Step 1: Identify Core Features
- Extract features from requirements
- Group related features

#### Step 2: Create Epics
- Logical grouping of features
- Sequence by dependencies

#### Step 3: Estimate Effort
- Story point estimation
- Epic duration (number of sprints)

**Brief decomposition example** (10-15 lines)

For common domain patterns and feature breakdowns, see references/domain-specific-patterns.md

---

### Phase 5: Feasibility & Constraints Analysis (~90 lines)

#### Step 1: Technical Feasibility
- Technology availability
- Team skills assessment
- Architecture feasibility

#### Step 2: Business Feasibility
- Timeline realism
- Budget sufficiency
- Resource availability

#### Step 3: Risk Assessment
- Technical risks
- Dependencies and unknowns
- Mitigation strategies

**Brief feasibility example** (10-15 lines)

For complete feasibility assessment framework, see references/feasibility-analysis-framework.md

---

### Phase 6: Requirements Documentation (~90 lines)

#### Step 1: Generate Epic Documents
- Create epic files in `.ai_docs/Epics/`
- YAML frontmatter with metadata
- Feature breakdown

#### Step 2: Create Requirements Spec
- Write to `.devforgeai/specs/requirements/`
- Complete requirements documentation
- Complexity assessment report

#### Step 3: Transition to Architecture
- Auto-invoke devforgeai-architecture skill
- Context file creation begins

**Example workflow** (10-15 lines)

---

## Tool Usage Protocol (~40 lines)

### Use Native Tools for File Operations
[Brief examples - ~20 lines]

### Use AskUserQuestion for Ambiguities
[Brief examples - ~20 lines]

---

## Reference Materials (~50 lines)

Load these on demand during ideation:

### Requirements Discovery
- **`./references/requirements-elicitation-guide.md`** - Domain-specific probing questions for e-commerce, SaaS, fintech, healthcare (723 lines)

### Complexity Analysis
- **`./references/complexity-assessment-matrix.md`** - Detailed 0-60 scoring rubric across 6 dimensions with examples (700 lines)

### Domain Patterns
- **`./references/domain-specific-patterns.md`** - Common feature patterns and decomposition templates for major domains (975 lines)

### Feasibility Assessment
- **`./references/feasibility-analysis-framework.md`** - Risk assessment checklists, technical/business/resource feasibility (649 lines)

---

## Success Criteria (~40 lines)

[Keep existing success criteria, condensed]
```

**Total Estimated**: ~670 lines (middle of 650-700 target)

### Specific Content to Remove

**Find and remove these duplications**:

1. **Detailed Domain Questions** (likely 100-150 lines in main)
   - E-commerce probing questions
   - SaaS probing questions
   - Fintech probing questions
   - Healthcare probing questions
   - **Already in**: requirements-elicitation-guide.md (723 lines)
   - **Action**: Remove from main, keep 5-10 example questions only

2. **Complexity Scoring Details** (likely 150-200 lines in main)
   - Dimension 1-6 detailed descriptions
   - Point allocation criteria
   - Scoring examples per dimension
   - **Already in**: complexity-assessment-matrix.md (700 lines)
   - **Action**: Remove from main, keep brief dimension list + formula only

3. **Domain Pattern Libraries** (likely 200-300 lines in main)
   - E-commerce standard features (user mgmt, catalog, cart, orders, payments)
   - SaaS standard features (auth, billing, admin, dashboards)
   - Fintech patterns
   - Healthcare patterns
   - **Already in**: domain-specific-patterns.md (975 lines)
   - **Action**: Remove from main, keep brief decomposition approach only

4. **Feasibility Checklists** (likely 80-120 lines in main)
   - Technical feasibility questions
   - Business feasibility questions
   - Resource constraint checklists
   - **Already in**: feasibility-analysis-framework.md (649 lines)
   - **Action**: Remove from main, keep brief assessment approach only

**Total Duplication to Remove**: ~530-770 lines
**Target Removal**: ~315 lines (to reach 670-line target)

**Approach**: Be selective - remove duplication while keeping essential workflow context

### Validation Steps

After refactoring, validate the result:

```bash
# 1. Check line count
wc -l .claude/skills/devforgeai-ideation/SKILL.md
# Expected: 650-700 lines (target: 670)

# 2. Verify backup created
ls -lh .claude/skills/devforgeai-ideation/SKILL.md.backup
# Expected: 985 lines

# 3. Verify all 4 references still exist
ls -lh .claude/skills/devforgeai-ideation/references/
# Expected: 4 files unchanged

# 4. Check reference links in main file
grep -o "references/[^)]*\.md" .claude/skills/devforgeai-ideation/SKILL.md | sort -u
# Expected: All 4 files referenced properly

# 5. Check for duplication removal
grep -c "e-commerce.*SaaS.*fintech" .claude/skills/devforgeai-ideation/SKILL.md
# Expected: 0-1 (brief mention only, details in references)

grep -c "Dimension 1.*Functional Complexity" .claude/skills/devforgeai-ideation/SKILL.md
# Expected: 0-1 (brief list only, scoring in reference)
```

### Key Implementation Guidelines

#### ✅ DO (Apply Phase 1.2/1.3 Patterns)

1. **Target 670 Lines** (conservative given references exist)
   - Don't go too aggressive like Phase 1.3 (496)
   - Don't settle for 700+ like Phase 1.1 (701)
   - **670 = balanced** (middle of 650-700)

2. **Remove Duplication Aggressively**
   ```markdown
   ✅ CORRECT:
   ## Phase 2: Requirements Elicitation
   Ask domain-specific probing questions.
   See references/requirements-elicitation-guide.md for comprehensive questions.

   Core approach:
   1. Identify domain (e-commerce, SaaS, fintech, healthcare)
   2. Load domain-specific questions from reference
   3. Conduct discovery interview
   ```

   ```markdown
   ❌ WRONG (Current - likely duplicated):
   ## Phase 2: Requirements Elicitation

   ### E-Commerce Questions:
   [100 lines of questions already in reference file]

   ### SaaS Questions:
   [100 lines of questions already in reference file]
   ```

3. **Keep Brief Examples Only**
   ```markdown
   ✅ CORRECT:
   Example complexity scoring:
   - Simple todo app: 12 points (Simple tier)
   - E-commerce platform: 35 points (Microservices tier)

   For complete scoring methodology, see references/complexity-assessment-matrix.md
   ```

4. **Reference All 4 Files Properly**
   - Each of the 6 phases should reference appropriate guide
   - Reference section at end should list all 4 files with descriptions
   - Use relative paths: `./references/filename.md`

#### ❌ DON'T

1. **Don't Duplicate Reference Content**
   ```markdown
   ❌ WRONG:
   ## Complexity Scoring
   [200 lines of scoring rubric already in complexity-assessment-matrix.md]

   ✅ CORRECT:
   ## Complexity Scoring
   Score 0-60 points across 6 dimensions.
   See references/complexity-assessment-matrix.md for detailed rubric.
   ```

2. **Don't Over-Optimize**
   - Don't try to hit 496 lines like orchestration (too aggressive for ideation)
   - Don't remove essential workflow context
   - Target 670 is conservative and safe

3. **Don't Remove Working Examples**
   - Keep 1-2 brief examples per phase (5-10 lines each)
   - Examples help understand the process
   - Remove verbose variations, keep essential patterns

4. **Don't Change Reference Files**
   - All 4 reference files are already complete and excellent
   - Your job is ONLY to refactor main SKILL.md
   - Don't modify references (already production-ready)

### Expected Outcome

**Before**:
```
.claude/skills/devforgeai-ideation/
├── SKILL.md (985 lines, 30KB, ~30,000 tokens)
└── references/
    ├── requirements-elicitation-guide.md (723 lines) ✅
    ├── complexity-assessment-matrix.md (700 lines) ✅
    ├── domain-specific-patterns.md (975 lines) ✅
    └── feasibility-analysis-framework.md (649 lines) ✅
```

**After**:
```
.claude/skills/devforgeai-ideation/
├── SKILL.md (670 lines, ~22KB, ~12,000 tokens)
├── SKILL.md.backup (985 lines, preserved for reference)
└── references/
    ├── requirements-elicitation-guide.md (723 lines) ✅ UNCHANGED
    ├── complexity-assessment-matrix.md (700 lines) ✅ UNCHANGED
    ├── domain-specific-patterns.md (975 lines) ✅ UNCHANGED
    └── feasibility-analysis-framework.md (649 lines) ✅ UNCHANGED
```

**Token Efficiency Gain**:
- Typical usage: Load SKILL.md only = ~12,000 tokens (60% reduction!)
- With elicitation guide: SKILL.md + requirements-elicitation-guide.md = ~25,000 tokens (17% reduction)
- With complexity matrix: SKILL.md + complexity-assessment-matrix.md = ~23,000 tokens (23% reduction)
- Maximum usage: SKILL.md + all 4 references = ~42,000 tokens (only when doing complete ideation)

**Framework Compliance**:
- ✅ Within target range (670 in 650-700 range)
- ✅ Follows progressive disclosure pattern
- ✅ Uses native tools over Bash
- ✅ All 4 reference files properly utilized
- ✅ Follows source-tree.md directory structure
- ✅ 100% framework compliance

### Testing the Refactored Skill

After completing the refactor, test with:

```bash
# Start Claude Code
claude

# Test simple ideation (should load main only)
> I want to build a simple task management app

# Claude should:
# 1. Load main SKILL.md (~12K tokens)
# 2. Execute basic discovery
# 3. Do simple complexity assessment (12 points = Simple tier)
# 4. NOT load all reference files (not needed for simple app)
# 5. Total: ~12K tokens (vs 30K original = 60% reduction)

# Test complex ideation (should load 1-2 references)
> I want to build a comprehensive e-commerce platform with subscription billing

# Claude should:
# 1. Load main SKILL.md (~12K tokens)
# 2. Load requirements-elicitation-guide.md for e-commerce questions (~18K tokens)
# 3. Load domain-specific-patterns.md for e-commerce patterns (~24K tokens)
# 4. Total: ~54K tokens (but gets comprehensive guidance)
# 5. Trade-off acceptable for complex projects
```

### Deliverables Checklist

When you complete this refactor, you should have:

- [ ] Main SKILL.md reduced to 650-700 lines (target: 670)
- [ ] Backup created (SKILL.md.backup with 985 lines)
- [ ] All 4 existing reference files preserved (NO changes to references)
- [ ] All 4 reference links working in main SKILL.md
- [ ] No functionality lost (all 6 phases preserved)
- [ ] Duplication removed (~315 lines of content already in references)
- [ ] Line count validated: `wc -l .claude/skills/devforgeai-ideation/SKILL.md`
- [ ] References unchanged: `ls -lh .claude/skills/devforgeai-ideation/references/`
- [ ] Tested skill invocation successfully
- [ ] Token usage reduced by ~60% for typical usage

### Success Criteria

The refactor is successful when:

1. **Size Compliance**: SKILL.md is 650-700 lines (target: 670)
2. **Progressive Disclosure**: References load on demand
3. **Functionality Preserved**: All 6 phases work correctly
4. **Framework Compliant**: Follows all context file constraints
5. **Token Efficient**: 60% reduction in typical token usage
6. **No Reference Changes**: All 4 reference files unchanged (already excellent)
7. **Duplication Removed**: Content in references not duplicated in main

---

## Commands to Execute in Session

```bash
# 1. Read current implementation
Read(file_path=".claude/skills/devforgeai-ideation/SKILL.md")

# 2. Read context files
Read(file_path=".devforgeai/context/tech-stack.md")
Read(file_path=".devforgeai/context/coding-standards.md")

# 3. Read all 4 existing reference files
Read(file_path=".claude/skills/devforgeai-ideation/references/requirements-elicitation-guide.md")
Read(file_path=".claude/skills/devforgeai-ideation/references/complexity-assessment-matrix.md")
Read(file_path=".claude/skills/devforgeai-ideation/references/domain-specific-patterns.md")
Read(file_path=".claude/skills/devforgeai-ideation/references/feasibility-analysis-framework.md")

# 4. Create backup
Bash(command="cp .claude/skills/devforgeai-ideation/SKILL.md .claude/skills/devforgeai-ideation/SKILL.md.backup")

# 5. Identify duplication
# Compare main SKILL.md content with reference files
# Note which sections are duplicated

# 6. Rewrite main SKILL.md (use Write to replace entire file)
Write(file_path=".claude/skills/devforgeai-ideation/SKILL.md", content="[670 line refactored version]")

# 7. Validate
Bash(command="wc -l .claude/skills/devforgeai-ideation/SKILL.md")
Bash(command="wc -l .claude/skills/devforgeai-ideation/SKILL.md.backup")
Bash(command="ls -lh .claude/skills/devforgeai-ideation/references/")
Bash(command="grep -o 'references/[^)]*\\.md' .claude/skills/devforgeai-ideation/SKILL.md | sort -u")
```

---

## Comparison with Previous Phases

| Aspect | Phase 1.3 (Orchestration) | Phase 2.1 (Ideation) |
|--------|---------------------------|----------------------|
| **Original Size** | 1,652 lines | 985 lines |
| **Existing References** | 3 files | 4 files ✅ (ALL needed) |
| **New References Needed** | 3 files | 0 files ✅ (all exist!) |
| **Target Size** | 630-640 | 650-700 (conservative) |
| **Expected Result** | 635 lines | 670 lines |
| **Reduction %** | 70% (1,652→496 actual) | 32% (985→670 target) |
| **Difficulty** | Moderate | **EASY** ✅ |

**Why This is EASIEST**:
- ✅ All reference files already exist (no creation needed)
- ✅ Just need to remove duplication from main
- ✅ Clear extraction targets (domain questions, scoring, patterns, feasibility)
- ✅ Conservative 670-line target (not aggressive)

**Estimated Time**: **1-2 hours** (fastest of all refactorings)

---

## Post-Refactor Review Prompt

After completing the refactor in a new session, use this prompt for review:

```
I've completed the refactor of devforgeai-ideation skill. Please review:

1. Check line count: Is SKILL.md 650-700 lines? (Target: 670)
2. Check backup: Does SKILL.md.backup exist with 985 lines?
3. Check references: Are all 4 files unchanged?
4. Check links: Do all references/[file].md links work?
5. Check functionality: Are all 6 phases preserved?
6. Check duplication: Is content properly separated?
7. Check compliance: Does it follow context file constraints?
8. Compare with Phase 1.2/1.3: Did we achieve 9.0+/10 quality?

Files to review:
- .claude/skills/devforgeai-ideation/SKILL.md
- .claude/skills/devforgeai-ideation/SKILL.md.backup

Run validation:
- wc -l .claude/skills/devforgeai-ideation/SKILL.md
- wc -l .claude/skills/devforgeai-ideation/SKILL.md.backup
- ls -la .claude/skills/devforgeai-ideation/references/
- grep "references/" .claude/skills/devforgeai-ideation/SKILL.md
```

---

## Success Metrics Targets

| Metric | Target | Expected |
|--------|--------|----------|
| **Line Count** | 650-700 | 670 ✅ |
| **Size Reduction** | 32% | 985→670 ✅ |
| **Token Savings** | 60% typical | ~60% ✅ |
| **Reference Files** | 4 (all existing) | 4 ✅ |
| **New Files Created** | 0 | 0 ✅ |
| **Duplication Removed** | ~315 lines | ~315 lines ✅ |
| **Framework Compliance** | 100% | 100% ✅ |
| **Quality Score** | 9.0-9.5/10 | 9.0/10 ✅ |

**Goal**: Quick, clean refactor leveraging existing comprehensive reference files

---

**Remember**: This is the EASIEST refactor because all reference files already exist. You just need to remove duplication from main SKILL.md and add proper progressive disclosure references. Target 670 lines for conservative, safe optimization.

**Estimated Time**: 1-2 hours
**Difficulty**: Easy (references complete, just refactor main)
**Priority**: Complete this FIRST (quick win), then tackle development skill
