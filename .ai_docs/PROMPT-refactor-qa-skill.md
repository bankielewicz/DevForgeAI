# Refactor devforgeai-qa Skill - Progressive Disclosure Implementation

## Context

The `devforgeai-qa` skill currently violates DevForgeAI's own architectural constraints:

**Current State**:
- File: `.claude/skills/devforgeai-qa/SKILL.md`
- Size: 2,197 lines (64KB)
- Status: ❌ **120% over maximum allowed (1,000 lines)**
- Token consumption: ~65,000 tokens when loaded

**Target State**:
- Main SKILL.md: 500-600 lines (~20KB)
- Reference files: 5-6 files in `references/` subdirectory
- Expected token savings: **70%** (load ~10K tokens typically, ~35K when references needed)

**Constraints to Follow**:
- `.devforgeai/context/tech-stack.md` - Component size limits
- `.devforgeai/context/coding-standards.md` - Progressive disclosure pattern
- `.devforgeai/context/source-tree.md` - Directory structure rules
- `.devforgeai/context/anti-patterns.md` - Size violation prevention

## Objective

Refactor `devforgeai-qa` skill to implement **progressive disclosure pattern**:
1. Keep core workflow instructions in main SKILL.md (500-600 lines)
2. Extract detailed procedures to reference files (loaded on demand)
3. Maintain all functionality while achieving 70% token efficiency gain
4. Follow DevForgeAI's own architectural standards

## Requirements

### Mandatory Actions

1. **Read Current Implementation**
   ```
   Read(file_path=".claude/skills/devforgeai-qa/SKILL.md")
   ```

2. **Read Framework Context Files** (understand constraints)
   ```
   Read(file_path=".devforgeai/context/tech-stack.md")
   Read(file_path=".devforgeai/context/source-tree.md")
   Read(file_path=".devforgeai/context/coding-standards.md")
   Read(file_path=".devforgeai/context/architecture-constraints.md")
   ```

3. **Create references/ Directory**
   ```
   Bash(command="mkdir -p .claude/skills/devforgeai-qa/references")
   ```

4. **Extract Content to Reference Files** (create 5-6 files)

5. **Refactor Main SKILL.md** (reduce to 500-600 lines)

6. **Validate Result** (check line count, test references)

### Reference Files to Create

Based on analysis of current SKILL.md content, extract these sections:

#### 1. `references/validation-procedures.md`
**Content to Extract**:
- Light validation detailed procedures (syntax checks, test execution, quick scans)
- Deep validation comprehensive procedures (coverage, anti-patterns, spec compliance, quality metrics)
- Validation mode selection logic
- Step-by-step validation workflows

**Estimated Size**: 400-500 lines

**What Stays in Main SKILL.md**:
```markdown
## Phase 2: Execute Validation (Light or Deep)

IF mode is "light":
  Run light validation (see references/validation-procedures.md for details)
ELSE:
  Run deep validation (see references/validation-procedures.md for details)
```

#### 2. `references/coverage-analysis-guide.md`
**Content to Extract**:
- Coverage threshold calculations (95%/85%/80% by layer)
- Layer classification logic (business logic, application, infrastructure)
- Coverage measurement techniques per language
- Coverage gap identification procedures
- Coverage report generation formats

**Estimated Size**: 300-400 lines

**What Stays in Main SKILL.md**:
```markdown
## Coverage Analysis
Analyze test coverage using strict thresholds.
For detailed calculation methodology, see references/coverage-analysis-guide.md

Thresholds:
- Business Logic: 95%
- Application: 85%
- Infrastructure: 80%
```

#### 3. `references/anti-patterns-catalog.md`
**Content to Extract**:
- All 10+ anti-pattern categories with examples
- Detection patterns for each category
- Language-specific anti-pattern variations
- Security anti-patterns (SQL injection, XSS, secrets, weak crypto)
- Performance anti-patterns (N+1 queries, inefficient algorithms)
- Maintainability anti-patterns (God objects, tight coupling)
- Code smell detection patterns

**Estimated Size**: 600-800 lines

**What Stays in Main SKILL.md**:
```markdown
## Anti-Pattern Detection
Scan for 10+ categories of anti-patterns.
For complete catalog with detection patterns, see references/anti-patterns-catalog.md

Categories: Security, Performance, Maintainability, Code Smells, etc.
```

#### 4. `references/quality-metrics-guide.md`
**Content to Extract**:
- Cyclomatic complexity measurement
- Maintainability index calculation
- Code duplication detection techniques
- Documentation coverage measurement
- Code quality scoring formulas
- Threshold definitions for each metric

**Estimated Size**: 300-400 lines

**What Stays in Main SKILL.md**:
```markdown
## Code Quality Metrics
Measure code quality across multiple dimensions.
For detailed metric calculations, see references/quality-metrics-guide.md

Metrics: Complexity (<10), Maintainability (≥70), Duplication (<5%), Documentation (≥80%)
```

#### 5. `references/spec-compliance-validation.md`
**Content to Extract**:
- Acceptance criteria validation procedures
- API contract validation techniques
- NFR (non-functional requirements) validation
- Data model validation against specs
- Business rule validation procedures
- Compliance report generation

**Estimated Size**: 300-400 lines

**What Stays in Main SKILL.md**:
```markdown
## Spec Compliance Validation
Validate implementation matches specifications.
For detailed validation procedures, see references/spec-compliance-validation.md

Validates: Acceptance criteria, API contracts, NFRs, Data models, Business rules
```

#### 6. `references/language-specific-tooling.md` (NEW - addresses framework-agnostic issue)
**Content to Extract**:
- Test framework commands per language (.NET, Python, Node.js, Java, Go, Rust)
- Coverage tool commands per language
- Security scanner selection per language
- Linting tool selection per language
- Code quality analyzer selection per language

**Estimated Size**: 200-300 lines

**What Stays in Main SKILL.md**:
```markdown
## Tool Selection
Determine language-specific tools based on tech-stack.md.
For tool command patterns, see references/language-specific-tooling.md

Use AskUserQuestion if language-specific tooling not in tech-stack.md
```

### Refactored SKILL.md Structure

**Target Structure** (500-600 lines total):

```markdown
---
name: devforgeai-qa
description: [Keep existing description]
allowed-tools: [Simplify - remove language-specific tools]
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - AskUserQuestion
  - Bash(test:*)
  - Bash(coverage:*)
  - Bash(lint:*)
  - Skill
---

# DevForgeAI QA Skill

[Keep existing purpose statement - ~50 lines]

## When to Use This Skill

[Keep existing usage guidance - ~30 lines]

## Core Principle: Progressive Validation

[Keep core principle - ~30 lines]

---

## QA Workflow

### Phase 1: Context and Mode Selection (~50 lines)
- Read context files
- Determine validation mode (light vs deep)
- Load story file
- Prepare validation environment

### Phase 2: Execute Validation (~80 lines)
- Light validation: See references/validation-procedures.md
- Deep validation: See references/validation-procedures.md
- Execute validation steps
- Collect results

### Phase 3: Coverage Analysis (~60 lines)
- Measure coverage by layer
- Enforce thresholds (95%/85%/80%)
- For detailed methodology: references/coverage-analysis-guide.md
- Generate coverage report

### Phase 4: Anti-Pattern Detection (~60 lines)
- Scan for 10+ categories
- For complete catalog: references/anti-patterns-catalog.md
- Report violations by severity
- Identify fix locations

### Phase 5: Spec Compliance Validation (~60 lines)
- Validate acceptance criteria
- Check API contracts
- Verify NFRs
- For detailed procedures: references/spec-compliance-validation.md

### Phase 6: Quality Metrics Analysis (~60 lines)
- Measure complexity, maintainability, duplication
- For calculation details: references/quality-metrics-guide.md
- Generate quality score
- Identify improvement areas

### Phase 7: Generate QA Report (~60 lines)
- Compile all validation results
- Create structured report
- Determine PASS/FAIL status
- Update story status

---

## Language-Specific Tool Selection (~50 lines)

Read tech-stack.md to determine language
For tool commands: references/language-specific-tooling.md

Use AskUserQuestion if tools not specified in tech-stack.md

---

## Success Criteria (~30 lines)

[Keep existing success criteria]

## Reference Files (~20 lines)

Load these as needed during validation:
- [Validation Procedures](./references/validation-procedures.md)
- [Coverage Analysis Guide](./references/coverage-analysis-guide.md)
- [Anti-Patterns Catalog](./references/anti-patterns-catalog.md)
- [Quality Metrics Guide](./references/quality-metrics-guide.md)
- [Spec Compliance Validation](./references/spec-compliance-validation.md)
- [Language-Specific Tooling](./references/language-specific-tooling.md)
```

**Total Estimated**: ~570 lines (within 500-600 target)

### Validation Steps

After refactoring, validate the result:

```bash
# 1. Check line count
wc -l .claude/skills/devforgeai-qa/SKILL.md
# Expected: 500-600 lines

# 2. Check reference files created
ls -lh .claude/skills/devforgeai-qa/references/
# Expected: 6 files

# 3. Check total size reduction
du -h .claude/skills/devforgeai-qa/
# Expected: Smaller total, but content preserved

# 4. Verify all references exist
grep -o "references/[^)]*\.md" .claude/skills/devforgeai-qa/SKILL.md | sort -u
# Ensure all referenced files exist
```

### Key Implementation Guidelines

#### ✅ DO

1. **Preserve All Functionality**
   - No content should be lost
   - All validation procedures still documented
   - All anti-patterns still detectable

2. **Use Direct Instructions in Main SKILL.md**
   ```markdown
   ✅ CORRECT:
   ## Phase 3: Coverage Analysis
   Run coverage analysis:
   - Bash(command="[coverage-command-from-tech-stack]")
   - Read coverage report
   - Calculate percentages by layer
   - For layer classification logic, see references/coverage-analysis-guide.md

   HALT if coverage < thresholds
   ```

3. **Use Progressive Disclosure Pattern**
   ```markdown
   ✅ CORRECT:
   Main SKILL.md: "Scan for anti-patterns (see references/anti-patterns-catalog.md)"
   references/anti-patterns-catalog.md: [600 lines of detailed patterns]
   ```

4. **Keep Frontmatter Concise**
   - Remove language-specific Bash tools (bandit, madge, radon, jscpd)
   - Keep generic patterns (test:*, coverage:*, lint:*)

5. **Follow Existing Format**
   - Maintain YAML frontmatter structure
   - Keep phase-based workflow organization
   - Preserve HALT patterns for quality gates

#### ❌ DON'T

1. **Don't Use Narrative Prose**
   ```markdown
   ❌ WRONG:
   The system should analyze coverage and then it might generate a report...

   ✅ CORRECT:
   Analyze coverage:
   - Run coverage tool
   - Calculate percentages
   - Generate report
   ```

2. **Don't Embed Everything Inline**
   ```markdown
   ❌ WRONG:
   ## Anti-Pattern Detection
   [500 lines of detailed anti-pattern catalog inline]

   ✅ CORRECT:
   ## Anti-Pattern Detection
   Scan for 10+ categories. See references/anti-patterns-catalog.md for catalog.
   ```

3. **Don't Break References**
   - Ensure every referenced file is created
   - Use correct relative paths (./references/filename.md)
   - Test that references load correctly

4. **Don't Change Core Logic**
   - Validation workflow must remain the same
   - Quality gates must work identically
   - Coverage thresholds must be preserved

### Expected Outcome

**Before**:
```
.claude/skills/devforgeai-qa/
└── SKILL.md (2,197 lines, 64KB, ~65,000 tokens)
```

**After**:
```
.claude/skills/devforgeai-qa/
├── SKILL.md (500-600 lines, ~20KB, ~10,000 tokens)
└── references/
    ├── validation-procedures.md (~450 lines)
    ├── coverage-analysis-guide.md (~350 lines)
    ├── anti-patterns-catalog.md (~700 lines)
    ├── quality-metrics-guide.md (~350 lines)
    ├── spec-compliance-validation.md (~350 lines)
    └── language-specific-tooling.md (~250 lines)
```

**Token Efficiency Gain**:
- Typical usage: Load SKILL.md only = ~10,000 tokens (70% reduction!)
- When coverage details needed: SKILL.md + coverage-analysis-guide.md = ~15,000 tokens (50% reduction)
- Maximum usage: SKILL.md + all references = ~35,000 tokens (46% reduction)

**Framework Compliance**:
- ✅ Within size limit (500-600 lines < 1,000 max)
- ✅ Follows progressive disclosure pattern (coding-standards.md)
- ✅ Uses native tools over Bash (tech-stack.md)
- ✅ Removes language-specific tools from frontmatter (framework-agnostic)
- ✅ Follows source-tree.md directory structure

### Testing the Refactored Skill

After completing the refactor, test with:

```bash
# Start Claude Code
claude

# Test skill invocation (should load only main SKILL.md)
> I need to run QA validation on STORY-001 in light mode

# Claude should:
# 1. Load main SKILL.md (~10K tokens)
# 2. Execute light validation
# 3. NOT load all references (unless needed)
# 4. Complete validation successfully

# Test deep validation (may load some references)
> Run deep QA validation on STORY-001

# Claude should:
# 1. Load main SKILL.md
# 2. Load references as needed (e.g., coverage-analysis-guide.md if calculating coverage)
# 3. Execute comprehensive validation
# 4. Generate full QA report
```

### Deliverables Checklist

When you complete this refactor, you should have:

- [ ] Main SKILL.md reduced to 500-600 lines
- [ ] 6 reference files created in `references/` subdirectory
- [ ] All reference links working (no broken ./references/ links)
- [ ] YAML frontmatter simplified (removed language-specific tools)
- [ ] No functionality lost (all validation procedures preserved)
- [ ] Line count validated: `wc -l .claude/skills/devforgeai-qa/SKILL.md`
- [ ] Directory structure validated: `ls -la .claude/skills/devforgeai-qa/references/`
- [ ] Tested skill invocation successfully
- [ ] Token usage reduced by ~70% for typical usage

### Success Criteria

The refactor is successful when:

1. **Size Compliance**: SKILL.md is 500-600 lines (not 2,197)
2. **Progressive Disclosure**: References load on demand, not all upfront
3. **Functionality Preserved**: All validation capabilities still work
4. **Framework Compliant**: Follows all context file constraints
5. **Token Efficient**: 70% reduction in typical token usage
6. **Language Agnostic**: No hardcoded Python/JavaScript tools in frontmatter

---

## Commands to Execute in Session

```bash
# 1. Read current implementation
Read(file_path=".claude/skills/devforgeai-qa/SKILL.md")

# 2. Read context files
Read(file_path=".devforgeai/context/tech-stack.md")
Read(file_path=".devforgeai/context/coding-standards.md")
Read(file_path=".devforgeai/context/source-tree.md")

# 3. Create references directory
Bash(command="mkdir -p .claude/skills/devforgeai-qa/references")

# 4. Create reference files (use Write tool for each)
Write(file_path=".claude/skills/devforgeai-qa/references/validation-procedures.md", content="...")
Write(file_path=".claude/skills/devforgeai-qa/references/coverage-analysis-guide.md", content="...")
Write(file_path=".claude/skills/devforgeai-qa/references/anti-patterns-catalog.md", content="...")
Write(file_path=".claude/skills/devforgeai-qa/references/quality-metrics-guide.md", content="...")
Write(file_path=".claude/skills/devforgeai-qa/references/spec-compliance-validation.md", content="...")
Write(file_path=".claude/skills/devforgeai-qa/references/language-specific-tooling.md", content="...")

# 5. Rewrite main SKILL.md (use Write to replace entire file)
Write(file_path=".claude/skills/devforgeai-qa/SKILL.md", content="[500-600 line refactored version]")

# 6. Validate
Bash(command="wc -l .claude/skills/devforgeai-qa/SKILL.md")
Bash(command="ls -lh .claude/skills/devforgeai-qa/references/")
```

---

## Post-Refactor Review Prompt

After completing the refactor in a new session, use this prompt for review:

```
I've completed the refactor of devforgeai-qa skill. Please review:

1. Check line count: Is SKILL.md 500-600 lines?
2. Check references: Are all 6 files created?
3. Check links: Do all references/[file].md links work?
4. Check frontmatter: Are language-specific tools removed?
5. Check functionality: Is all content preserved?
6. Check compliance: Does it follow context file constraints?

Files to review:
- .claude/skills/devforgeai-qa/SKILL.md
- .claude/skills/devforgeai-qa/references/*.md

Run validation:
- wc -l .claude/skills/devforgeai-qa/SKILL.md
- ls -la .claude/skills/devforgeai-qa/references/
- grep "references/" .claude/skills/devforgeai-qa/SKILL.md
```

---

**Remember**: This refactor implements DevForgeAI's own architectural principles of progressive disclosure, token efficiency, and framework-agnostic design. The skill will be more maintainable, more efficient, and compliant with the framework's own standards.
