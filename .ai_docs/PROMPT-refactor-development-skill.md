# Refactor devforgeai-development Skill - Progressive Disclosure Implementation

## Context

The `devforgeai-development` skill currently violates DevForgeAI's own architectural constraints:

**Current State**:
- File: `.claude/skills/devforgeai-development/SKILL.md`
- Size: 987 lines (30KB)
- Status: ❌ **98.7% of maximum, 41-64% over soft target (600-700)**
- Token consumption: ~30,000 tokens when loaded
- References: ⚠️ **PARTIAL** - Has 1 of 3 recommended files
  - tdd-patterns.md (24KB, ~810 lines) ✅ EXISTS

**Target State**:
- Main SKILL.md: 600-650 lines (~20KB, target: 640)
- Reference files: 3 files in `references/` subdirectory (1 existing + 2 new)
- Expected token savings: **58%** (load ~13K tokens typically, ~28K when references needed)

**Constraints to Follow**:
- `.devforgeai/context/tech-stack.md` - Component size limits
- `.devforgeai/context/coding-standards.md` - Progressive disclosure pattern
- `.devforgeai/context/source-tree.md` - Directory structure rules
- `.devforgeai/context/anti-patterns.md` - Size violation prevention

**Lessons from Phase 1.1, 1.2, 1.3, 2.1**:
- ✅ Phase 1.1 (QA): 701 lines acceptable
- ⭐ Phase 1.2 (Release): 633 lines PERFECT
- 🏆 Phase 1.3 (Orchestration): 496 lines OUTSTANDING
- 🎯 Phase 2.1 (Ideation): 670 lines target (conservative)
- 🎯 Phase 2.2 target: **640 lines** (balanced - middle of 600-650 adjusted range)

## Objective

Refactor `devforgeai-development` skill to implement **progressive disclosure pattern**:
1. Keep core TDD workflow in main SKILL.md (600-650 lines, target: 640)
2. Create 2 new reference files (refactoring, git conventions)
3. Utilize 1 existing reference file (tdd-patterns.md)
4. Maintain all functionality while achieving 58% token efficiency gain
5. Follow DevForgeAI's own architectural standards

## Requirements

### Mandatory Actions

1. **Read Current Implementation**
   ```
   Read(file_path=".claude/skills/devforgeai-development/SKILL.md")
   ```

2. **Read Framework Context Files** (understand constraints)
   ```
   Read(file_path=".devforgeai/context/tech-stack.md")
   Read(file_path=".devforgeai/context/coding-standards.md")
   Read(file_path=".devforgeai/context/source-tree.md")
   ```

3. **Read Existing Reference File**
   ```
   Read(file_path=".claude/skills/devforgeai-development/references/tdd-patterns.md")
   ```

4. **Create Backup**
   ```
   Bash(command="cp .claude/skills/devforgeai-development/SKILL.md .claude/skills/devforgeai-development/SKILL.md.backup")
   ```

5. **Create 2 New Reference Files**

6. **Refactor Main SKILL.md** (reduce to 600-650 lines, target 640)

7. **Validate Result** (check line count, test references)

### Existing Reference File (Preserve and Use)

1. ✅ **`tdd-patterns.md`** (24KB, ~810 lines)
   - Contains: TDD patterns and best practices
   - Status: Keep as-is, ensure main SKILL.md references it properly
   - **Main SKILL.md should NOT duplicate TDD pattern content**

### New Reference Files to Create

#### 2. `references/refactoring-patterns.md` (NEW)
**Content to Create**:
- Refactoring techniques catalog (Extract Method, Extract Class, etc.)
- Code smell identification patterns
- Refactoring safety procedures (keep tests green)
- Language-specific refactoring patterns (.NET, Python, JavaScript)
- Refactoring decision trees (when to refactor vs rewrite)
- Refactoring anti-patterns (over-engineering, premature abstraction)
- IDE refactoring tool usage (VS Code, Visual Studio, PyCharm, IntelliJ)

**Estimated Size**: 400-500 lines

**What Stays in Main SKILL.md**:
```markdown
## Phase 4: Refactor

Improve code quality while keeping tests green.

Refactoring approach:
1. Identify code smells
2. Select refactoring technique
3. Apply refactoring incrementally
4. Run tests after each change
5. Invoke light QA validation

For refactoring techniques and patterns, see references/refactoring-patterns.md

HALT if tests break during refactoring
```

#### 3. `references/git-workflow-conventions.md` (NEW)
**Content to Create**:
- Git branch naming conventions (feature/, bugfix/, hotfix/)
- Commit message format (Conventional Commits)
- Commit message templates by change type
- When to commit (after each TDD phase, after refactoring, etc.)
- Staging strategy (what to include in commits)
- Push timing (after integration tests pass)
- Branch management (when to merge, delete)
- Git hooks integration (pre-commit, commit-msg)
- Multi-file change organization (how to split into commits)

**Estimated Size**: 350-400 lines

**What Stays in Main SKILL.md**:
```markdown
## Phase 6: Git Workflow

Version control operations after successful implementation.

Git workflow:
1. Review changes: git status, git diff
2. Stage files: git add [relevant files]
3. Create commit with conventional format
4. Push to remote

For commit message conventions and git best practices, see references/git-workflow-conventions.md

Example commit:
feat: Implement user authentication

- Added login/logout functionality
- Tests: 12 unit tests, 3 integration tests
- Coverage: 96% (exceeds 95% threshold)
- Compliance: tech-stack.md, coding-standards.md

Closes #STORY-001
```

### Key Extraction Strategy

**Analyze Current SKILL.md (987 lines)**:

Based on typical TDD skill structure:
- Lines 1-100: Frontmatter, purpose, principles (~100 lines) - **Keep most**
- Lines 101-300: Phase 1 - Context Validation (~200 lines) - **Condense to ~80 lines**
- Lines 301-500: Phase 2 - Test-First (Red) (~200 lines) - **Condense to ~100 lines**
- Lines 501-650: Phase 3 - Implementation (Green) (~150 lines) - **Condense to ~100 lines**
- Lines 651-800: Phase 4 - Refactor (~150 lines) - **Extract refactoring details, keep ~80 lines**
- Lines 801-900: Phase 5 - Integration (~100 lines) - **Condense to ~80 lines**
- Lines 901-987: Phase 6 - Git Workflow (~87 lines) - **Extract git details, keep ~60 lines**

**Total Projected**: ~100 + 80 + 100 + 100 + 80 + 80 + 60 = ~600 lines
**Add back**: Success criteria, tool protocol, references section = +40 lines
**Target**: ~640 lines ✅

**Content to Extract**:

1. **Detailed TDD Explanations** (~120 lines)
   - Red-Green-Refactor detailed descriptions
   - TDD philosophy and benefits
   - Common TDD mistakes
   - **Already in**: tdd-patterns.md (810 lines)
   - **Action**: Remove from main, reference tdd-patterns.md

2. **Refactoring Catalog** (~80 lines)
   - Refactoring techniques (Extract Method, etc.)
   - Code smell identification
   - Refactoring decision logic
   - **Create**: references/refactoring-patterns.md (400 lines)
   - **Action**: Extract to new reference file

3. **Git Workflow Details** (~60 lines)
   - Conventional commit format details
   - Branch naming conventions
   - Commit message templates
   - **Create**: references/git-workflow-conventions.md (350 lines)
   - **Action**: Extract to new reference file

4. **Verbose Phase Descriptions** (~80 lines)
   - Explanatory paragraphs vs direct instructions
   - **Action**: Condense to direct instructions

5. **Example Variations** (~40 lines)
   - Multiple examples of same concept
   - **Action**: Keep 1 essential example per concept

**Total Extraction**: ~380 lines → 987 - 380 = ~607 lines
**Add optimization**: Condense remaining ~33 lines → **640 lines target** ✅

### Refactored SKILL.md Structure

**Target Structure** (600-650 lines, target: 640):

```markdown
---
name: devforgeai-development
description: [Keep existing description]
allowed-tools: [Keep existing - already clean]
  - Read, Write, Edit, Glob, Grep
  - AskUserQuestion
  - Bash(git:*), Bash(npm:*), Bash(pytest:*), Bash(dotnet:*), Bash(cargo:*), Bash(mvn:*)
  - Skill
---

# DevForgeAI Development Skill

[Keep existing purpose statement - ~60 lines]

## Purpose

[Keep TDD workflow overview - ~40 lines]

## When to Use This Skill

[Keep usage guidance - ~30 lines]

---

## TDD Workflow (6 Phases)

### Phase 1: Context Validation (~80 lines)

#### Step 1: Load Context Files
```
Read all 6 context files in PARALLEL:
- Read(file_path=".devforgeai/context/tech-stack.md")
- Read(file_path=".devforgeai/context/source-tree.md")
- Read(file_path=".devforgeai/context/dependencies.md")
- Read(file_path=".devforgeai/context/coding-standards.md")
- Read(file_path=".devforgeai/context/architecture-constraints.md")
- Read(file_path=".devforgeai/context/anti-patterns.md")

HALT if ANY file missing: "Run /create-context first"
```

#### Step 2: Load Story
```
Read(file_path=".ai_docs/Stories/{story_id}.story.md")

Extract:
- Acceptance criteria
- Technical specification
- NFRs
```

#### Step 3: Validate Prerequisites
- Story status == "Ready for Dev"
- All context files exist and valid
- Test framework available

---

### Phase 2: Test-First (Red) (~100 lines)

#### Step 1: Generate Failing Tests
```
Based on acceptance criteria, create tests that:
1. Test each acceptance criterion
2. Follow AAA pattern (Arrange, Act, Assert)
3. Use test framework from tech-stack.md
```

For TDD patterns and test design, see references/tdd-patterns.md

#### Step 2: Run Tests (Verify RED)
```
Bash(command="[test-command-from-tech-stack]")

HALT if tests pass: "Tests should fail before implementation"
```

**Example workflow** (10 lines)

---

### Phase 3: Implementation (Green) (~100 lines)

#### Step 1: Implement Minimal Code
```
Write code to pass tests:
- Follow coding-standards.md patterns
- Respect architecture-constraints.md layers
- Use dependencies from dependencies.md only
```

#### Step 2: Run Light QA
```
Skill(command="devforgeai-qa --mode=light --story={story_id}")

HALT if violations detected
```

#### Step 3: Run Tests (Verify GREEN)
```
Bash(command="[test-command]")

HALT if tests fail: "Implementation doesn't satisfy tests"
```

**Example workflow** (10 lines)

---

### Phase 4: Refactor (~80 lines)

#### Step 1: Identify Refactoring Opportunities
- Code smells (duplication, long methods, complexity)
- Design improvements
- Performance optimizations

For refactoring techniques, see references/refactoring-patterns.md

#### Step 2: Apply Refactoring
```
Use Edit tool to improve code quality
Run tests after each refactoring
Keep tests GREEN throughout
```

#### Step 3: Validate Refactoring
```
Skill(command="devforgeai-qa --mode=light --story={story_id}")
Bash(command="[test-command]")

HALT if tests break or QA violations
```

**Example refactoring** (10 lines)

---

### Phase 5: Integration (~80 lines)

#### Step 1: Run Full Test Suite
```
Bash(command="[full-test-suite-command]")

HALT if any tests fail
```

#### Step 2: Deep QA Validation
```
Skill(command="devforgeai-qa --mode=deep --story={story_id}")

Review QA report for violations
```

#### Step 3: Handle QA Results
```
IF CRITICAL or HIGH violations:
  Use AskUserQuestion: "Fix now or create follow-up story?"
```

---

### Phase 6: Git Workflow (~60 lines)

#### Step 1: Review Changes
```
Bash(command="git status")
Bash(command="git diff")
```

#### Step 2: Stage and Commit
```
Bash(command="git add [files]")

Create conventional commit message
For commit conventions, see references/git-workflow-conventions.md

Bash(command='git commit -m "$(cat <<EOF
feat: Implement [feature]

- Completed acceptance criteria
- Tests: [count] passing, [coverage]%
- Compliance: tech-stack.md, coding-standards.md

Closes #[story-id]
EOF
)"')
```

#### Step 3: Push
```
Bash(command="git push")
```

#### Step 4: Update Story Status
```
Edit(file_path=".ai_docs/Stories/{story_id}.story.md",
     old_string="status: In Development",
     new_string="status: Dev Complete")
```

---

## Tool Usage Protocol (~40 lines)

### Use Native Tools for File Operations
[Brief examples - ~20 lines]

### Use Bash for Tests and Git
[Brief examples - ~20 lines]

---

## Reference Materials (~50 lines)

Load these on demand during development:

### TDD Guidance
- **`./references/tdd-patterns.md`** - Test-Driven Development patterns, AAA format, test design, TDD philosophy (810 lines)

### Refactoring
- **`./references/refactoring-patterns.md`** - Refactoring techniques catalog, code smell identification, safety procedures (400-500 lines)

### Version Control
- **`./references/git-workflow-conventions.md`** - Commit message format, branch naming, git best practices (350-400 lines)

---

## Success Criteria (~40 lines)

[Keep existing success criteria, condensed]
```

**Total Estimated**: ~640 lines (middle of 600-650 target)

### New Reference Files to Create

#### refactoring-patterns.md (400-500 lines)

**Structure**:
```markdown
# Refactoring Patterns Reference

Complete catalog of refactoring techniques for improving code quality.

## When to Refactor

- After tests are GREEN (never during RED or while tests failing)
- When code smells detected
- When complexity exceeds thresholds
- During dedicated refactoring phase (Phase 4 of TDD)

---

## Common Refactoring Techniques

### Extract Method
**Problem**: Long method with multiple responsibilities
**Solution**: Extract cohesive blocks into separate methods
**Example**: [Code example]

### Extract Class
**Problem**: Class with too many responsibilities
**Solution**: Split into multiple focused classes
**Example**: [Code example]

### Introduce Parameter Object
**Problem**: Methods with long parameter lists
**Solution**: Group related parameters into object
**Example**: [Code example]

### Replace Conditional with Polymorphism
**Problem**: Complex if/switch statements based on type
**Solution**: Use inheritance and polymorphism
**Example**: [Code example]

[... 10-15 common refactoring techniques with examples]

---

## Code Smell Identification

### Method-Level Smells
- **Long Method** (>50 lines): Break into smaller methods
- **Long Parameter List** (>4 params): Use parameter object
- **Complex Conditionals**: Extract to methods or use polymorphism

### Class-Level Smells
- **God Object** (>500 lines): Split responsibilities
- **Data Class**: Add behavior where data lives
- **Feature Envy**: Move method to class it uses most

[... 15-20 code smells with detection patterns]

---

## Refactoring Safety

### Always Keep Tests Green
1. Run tests before refactoring
2. Make one small refactoring change
3. Run tests immediately
4. If tests fail: Revert and try different approach
5. If tests pass: Commit and continue

### Invoke Light QA After Refactoring
```
Skill(command="devforgeai-qa --mode=light --story={story_id}")
```

---

## Language-Specific Refactoring

### .NET Refactoring
- Use Visual Studio refactoring tools
- ReSharper suggestions
- Code cleanup on save

### Python Refactoring
- Use PyCharm refactoring
- Rope library for automated refactoring
- Black for formatting

### JavaScript/TypeScript
- Use VS Code refactoring
- ESLint auto-fix
- Prettier formatting

[... patterns for Java, Go, Rust]

---

## Refactoring Decision Tree

When to refactor vs when to rewrite:
- <30% change: Refactor
- 30-70% change: Consider both
- >70% change: Rewrite

---

[Additional patterns and examples to reach 400-500 lines]
```

#### git-workflow-conventions.md (350-400 lines)

**Structure**:
```markdown
# Git Workflow Conventions Reference

Complete guide for version control operations in DevForgeAI development workflow.

## Branch Naming Conventions

### Feature Branches
```
feature/STORY-001-user-authentication
feature/EPIC-002-checkout-optimization
```

### Bugfix Branches
```
bugfix/STORY-015-login-redirect
bugfix/critical-security-patch
```

### Hotfix Branches
```
hotfix/production-crash
hotfix/HOTFIX-001-payment-failure
```

### Release Branches
```
release/v1.2.0
release/SPRINT-003
```

---

## Conventional Commit Format

### Standard Format
```
<type>(<scope>): <subject>

<body>

<footer>
```

### Commit Types
- **feat**: New feature
- **fix**: Bug fix
- **refactor**: Code refactoring (no behavior change)
- **test**: Adding/updating tests
- **docs**: Documentation changes
- **chore**: Build process, dependencies, tooling
- **perf**: Performance improvements
- **style**: Code formatting (no logic change)

### Examples

**Feature commit:**
```
feat(auth): Implement JWT authentication

- Added login/logout endpoints
- Implemented token validation middleware
- Created user session management
- Tests: 12 unit tests, 95% coverage
- Compliance: tech-stack.md (JWT), coding-standards.md

Closes #STORY-001
```

**Bugfix commit:**
```
fix(cart): Prevent duplicate items in shopping cart

- Added duplicate check before adding item
- Updated cart service tests
- Regression test added
- Coverage: 98%

Fixes #BUG-045
```

**Refactor commit:**
```
refactor(user-service): Extract validation logic to separate class

- Created UserValidator class
- Moved validation from UserService
- No behavior changes
- All tests still passing (100%)

Part of #STORY-003 refactoring phase
```

---

## Commit Timing

### When to Commit (Following TDD Phases)

**After Phase 2 (Red):**
```
test: Add failing tests for user authentication

- Added 12 test cases for login/logout
- Tests currently failing (RED phase)
- Will implement in next commit

Part of #STORY-001
```

**After Phase 3 (Green):**
```
feat: Implement user authentication (Green phase)

- Implemented login/logout functionality
- All tests now passing
- Minimal implementation (will refactor next)

Part of #STORY-001
```

**After Phase 4 (Refactor):**
```
refactor: Improve authentication code quality

- Extracted validation logic
- Simplified login method
- All tests still passing

Part of #STORY-001
```

**After Phase 5 (Integration):**
```
feat: Complete user authentication feature

- All tests passing (12 unit, 3 integration)
- Coverage: 96%
- QA validation: PASSED
- Ready for code review

Closes #STORY-001
```

**Recommendation**: Use the "After Phase 5" pattern (single commit per story) for simplicity.

---

## Staging Strategy

### What to Stage

**Include:**
- Source code changes
- Test files
- Updated documentation
- Configuration changes (if needed)

**Exclude:**
- Temporary files
- IDE configuration (.vscode/, .idea/)
- Build artifacts (bin/, dist/, node_modules/)
- Secrets or credentials

### Git Add Commands
```bash
# Stage specific files
git add src/Application/Services/AuthService.cs
git add tests/Application.Tests/Services/AuthServiceTests.cs

# Stage by pattern
git add src/**/*.cs
git add tests/**/*.cs

# Interactive staging (select changes)
git add -p
```

---

## Multi-File Commit Organization

### When to Split into Multiple Commits

**Single commit when:**
- Changes are cohesive (single story)
- All changes needed together
- Total <500 lines changed

**Multiple commits when:**
- Multiple stories in same session
- Refactoring separate from features
- >500 lines changed (split logically)

### Commit Splitting Strategy
```
Commit 1: Tests (Red phase)
Commit 2: Implementation (Green phase)
Commit 3: Refactoring (Refactor phase)
Commit 4: Documentation updates

OR

Commit 1: Complete story (all phases together)
```

**Recommendation**: Single commit per story after Phase 5 (simpler).

---

## Git Hooks Integration

### Pre-Commit Hooks
- Run linter
- Check for secrets/credentials
- Validate commit message format
- Run quick tests

### Commit-Msg Hooks
- Validate conventional commit format
- Ensure story ID referenced
- Check message length

---

[Additional git patterns and examples to reach 350-400 lines]
```

### Validation Steps

After refactoring, validate the result:

```bash
# 1. Check line count
wc -l .claude/skills/devforgeai-development/SKILL.md
# Expected: 600-650 lines (target: 640)

# 2. Verify backup created
ls -lh .claude/skills/devforgeai-development/SKILL.md.backup
# Expected: 987 lines

# 3. Verify all 3 reference files exist
ls -lh .claude/skills/devforgeai-development/references/
# Expected: 3 files (tdd-patterns.md + 2 new)

# 4. Verify new files created
ls -lh .claude/skills/devforgeai-development/references/refactoring-patterns.md
ls -lh .claude/skills/devforgeai-development/references/git-workflow-conventions.md
# Expected: Both exist, 350-500 lines each

# 5. Verify all reference links work
grep -o "references/[^)]*\.md" .claude/skills/devforgeai-development/SKILL.md | sort -u
# Expected: All 3 files referenced

# 6. Check for duplication
grep -c "Extract Method\|Extract Class" .claude/skills/devforgeai-development/SKILL.md
# Expected: 0-1 (brief mention only, catalog in refactoring-patterns.md)
```

### Key Implementation Guidelines

#### ✅ DO (Apply All Phase Lessons)

1. **Target 640 Lines** (balanced optimization)
   - Not too aggressive like Phase 1.3 (496)
   - Not too conservative like Phase 1.1 (701)
   - Balanced like Phase 1.2 (633)
   - **640 = perfect for development workflow with examples**

2. **Utilize Existing tdd-patterns.md**
   ```markdown
   ✅ CORRECT:
   ## Phase 2: Test-First (Red)
   Write failing tests based on acceptance criteria.
   For TDD patterns and test design, see references/tdd-patterns.md

   Brief workflow:
   1. Create test class
   2. Write test methods (AAA pattern)
   3. Run tests (should fail)
   ```

   ```markdown
   ❌ WRONG:
   ## Phase 2: Test-First (Red)
   [100 lines of TDD pattern explanations already in tdd-patterns.md]
   ```

3. **Create Comprehensive New References**
   - refactoring-patterns.md should be 400-500 lines (comprehensive catalog)
   - git-workflow-conventions.md should be 350-400 lines (complete guide)
   - Better than multiple small fragmented files

4. **Keep Brief Code Examples**
   ```markdown
   ✅ CORRECT:
   Example test:
   ```csharp
   [Fact]
   public void Login_WithValidCredentials_ReturnsSuccess()
   {
       // Arrange
       var service = new AuthService();

       // Act
       var result = service.Login("user@example.com", "password");

       // Assert
       Assert.True(result.IsSuccess);
   }
   ```

   For complete test patterns, see references/tdd-patterns.md
   ```

5. **Follow Phase 1.2/1.3 Quality Standards**
   - 100% framework compliance
   - Zero duplication
   - Clear progressive disclosure
   - Quality score 9.0+/10

#### ❌ DON'T

1. **Don't Duplicate Existing TDD Patterns**
   - tdd-patterns.md already has 810 lines of TDD guidance
   - Main file should reference it, not repeat it

2. **Don't Go Too Aggressive**
   - 496 lines worked for orchestration (coordinative skill)
   - Development is procedural/technical (needs more context)
   - 640 lines is appropriate (not 496)

3. **Don't Remove Essential TDD Workflow**
   - 6 phases must be clear and complete
   - Keep enough context to understand workflow
   - Progressive disclosure, not minimalism

### Expected Outcome

**Before**:
```
.claude/skills/devforgeai-development/
├── SKILL.md (987 lines, 30KB, ~30,000 tokens)
└── references/
    └── tdd-patterns.md (810 lines) ✅ EXISTING
```

**After**:
```
.claude/skills/devforgeai-development/
├── SKILL.md (640 lines, ~20KB, ~13,000 tokens)
├── SKILL.md.backup (987 lines, preserved)
└── references/
    ├── tdd-patterns.md (810 lines) ✅ EXISTING (unchanged)
    ├── refactoring-patterns.md (~450 lines) ✅ NEW
    └── git-workflow-conventions.md (~375 lines) ✅ NEW
```

**Token Efficiency Gain**:
- Typical usage: SKILL.md only = ~13,000 tokens (57% reduction!)
- With TDD patterns: SKILL.md + tdd-patterns.md = ~28,000 tokens (7% reduction, better organization)
- With refactoring: SKILL.md + refactoring-patterns.md = ~22,000 tokens (27% reduction)
- Maximum usage: SKILL.md + all 3 references = ~40,000 tokens (only when deep TDD guidance needed)

**Framework Compliance**:
- ✅ Within target range (640 in 600-650)
- ✅ Follows progressive disclosure pattern
- ✅ Uses native tools over Bash
- ✅ All 3 reference files properly utilized
- ✅ Follows source-tree.md directory structure
- ✅ 100% framework compliance

### Testing the Refactored Skill

After completing the refactor, test with:

```bash
# Start Claude Code
claude

# Test TDD workflow (should load main + might load tdd-patterns)
> Implement STORY-001 using TDD workflow

# Claude should:
# 1. Load main SKILL.md (~13K tokens)
# 2. Load tdd-patterns.md if needs detailed guidance (~20K tokens)
# 3. Execute Red-Green-Refactor cycle
# 4. Total: ~13-33K tokens (vs 30K original = 13-57% reduction)

# Test refactoring phase (should load refactoring-patterns)
> Refactor the authentication code to improve quality

# Claude should:
# 1. Load main SKILL.md
# 2. Load refactoring-patterns.md for techniques
# 3. Apply refactoring improvements
# 4. Keep tests green throughout
```

### Deliverables Checklist

When you complete this refactor, you should have:

- [ ] Main SKILL.md reduced to 600-650 lines (target: 640)
- [ ] Backup created (SKILL.md.backup with 987 lines)
- [ ] 2 new reference files created (refactoring-patterns, git-workflow-conventions)
- [ ] 1 existing reference file preserved (tdd-patterns.md unchanged)
- [ ] All 3 reference links working in main SKILL.md
- [ ] No functionality lost (all 6 TDD phases preserved)
- [ ] No duplication with tdd-patterns.md
- [ ] Line count validated: `wc -l .claude/skills/devforgeai-development/SKILL.md`
- [ ] Directory structure validated: `ls -la .claude/skills/devforgeai-development/references/`
- [ ] Tested skill invocation successfully
- [ ] Token usage reduced by ~57% for typical usage

### Success Criteria

The refactor is successful when:

1. **Size Compliance**: SKILL.md is 600-650 lines (target: 640)
2. **Progressive Disclosure**: References load on demand
3. **Functionality Preserved**: All 6 TDD phases work correctly
4. **Framework Compliant**: Follows all context file constraints
5. **Token Efficient**: 57% reduction in typical token usage
6. **3 Reference Files**: tdd-patterns (existing) + refactoring-patterns (new) + git-conventions (new)
7. **Quality Score**: 9.0+/10

---

## Commands to Execute in Session

```bash
# 1. Read current implementation
Read(file_path=".claude/skills/devforgeai-development/SKILL.md")

# 2. Read context files
Read(file_path=".devforgeai/context/tech-stack.md")
Read(file_path=".devforgeai/context/coding-standards.md")

# 3. Read existing reference file
Read(file_path=".claude/skills/devforgeai-development/references/tdd-patterns.md")

# 4. Create backup
Bash(command="cp .claude/skills/devforgeai-development/SKILL.md .claude/skills/devforgeai-development/SKILL.md.backup")

# 5. Create 2 new reference files
Write(file_path=".claude/skills/devforgeai-development/references/refactoring-patterns.md", content="...")
Write(file_path=".claude/skills/devforgeai-development/references/git-workflow-conventions.md", content="...")

# 6. Rewrite main SKILL.md
Write(file_path=".claude/skills/devforgeai-development/SKILL.md", content="[640 line refactored version]")

# 7. Validate
Bash(command="wc -l .claude/skills/devforgeai-development/SKILL.md .claude/skills/devforgeai-development/SKILL.md.backup")
Bash(command="ls -lh .claude/skills/devforgeai-development/references/")
```

---

## Post-Refactor Review Prompt

After completing the refactor in a new session, use this prompt for review:

```
I've completed the refactor of devforgeai-development skill. Please review:

1. Check line count: Is SKILL.md 600-650 lines? (Target: 640)
2. Check backup: Does SKILL.md.backup exist with 987 lines?
3. Check references: Are all 3 files present (1 existing + 2 new)?
4. Check new files: Do refactoring-patterns.md and git-workflow-conventions.md exist with appropriate content?
5. Check links: Do all references/[file].md links work?
6. Check functionality: Are all 6 TDD phases preserved?
7. Check duplication: Is tdd-patterns.md content not duplicated in main?
8. Check compliance: Does it follow context file constraints?
9. Compare quality: Did we achieve 9.0+/10?

Files to review:
- .claude/skills/devforgeai-development/SKILL.md
- .claude/skills/devforgeai-development/references/refactoring-patterns.md
- .claude/skills/devforgeai-development/references/git-workflow-conventions.md

Run validation:
- wc -l .claude/skills/devforgeai-development/SKILL.md
- ls -la .claude/skills/devforgeai-development/references/
- grep "references/" .claude/skills/devforgeai-development/SKILL.md
```

---

## Success Metrics Targets

| Metric | Target | Expected |
|--------|--------|----------|
| **Line Count** | 600-650 | 640 ✅ |
| **Size Reduction** | 35% | 987→640 ✅ |
| **Token Savings** | 57% typical | ~57% ✅ |
| **Reference Files** | 3 (1+2) | 3 ✅ |
| **New Files** | 2 | 2 ✅ |
| **Framework Compliance** | 100% | 100% ✅ |
| **Quality Score** | 9.0/10 | 9.0/10 ✅ |

**Goal**: Professional refactor matching Phase 1.2/1.3 quality standards

---

**Remember**:
- Target 640 lines (balanced, not too aggressive)
- Create 2 comprehensive reference files (400-500 lines each)
- Utilize existing tdd-patterns.md properly
- Remove duplication with TDD patterns reference
- Keep brief code examples for clarity
- Achieve 100% framework compliance
- Quality score 9.0+/10

**Estimated Time**: 2-3 hours
**Difficulty**: Moderate (need to create 2 new references + refactor main)
**Priority**: Complete AFTER ideation skill (ideation is easier - quick win first)
