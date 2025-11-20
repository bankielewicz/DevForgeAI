# Refactor devforgeai-release Skill - Progressive Disclosure Implementation

## Context

The `devforgeai-release` skill currently violates DevForgeAI's own architectural constraints:

**Current State**:
- File: `.claude/skills/devforgeai-release/SKILL.md`
- Size: 1,734 lines (58KB)
- Status: ❌ **73% over maximum allowed (1,000 lines)**
- Token consumption: ~58,000 tokens when loaded
- References: ✅ 5 reference files already exist

**Target State**:
- Main SKILL.md: 600-650 lines (~21KB)
- Reference files: 5-6 files in `references/` subdirectory
- Expected token savings: **65%** (load ~20K tokens typically, ~50K when references needed)

**Constraints to Follow**:
- `.devforgeai/context/tech-stack.md` - Component size limits
- `.devforgeai/context/coding-standards.md` - Progressive disclosure pattern
- `.devforgeai/context/source-tree.md` - Directory structure rules
- `.devforgeai/context/anti-patterns.md` - Size violation prevention

**Lesson from Phase 1.1 (devforgeai-qa)**:
- Acceptable to be 600-650 lines if code examples add clarity
- Don't sacrifice workflow readability for strict 600-line target
- Code examples are worth ~50 extra lines

## Objective

Refactor `devforgeai-release` skill to implement **progressive disclosure pattern**:
1. Keep core workflow instructions in main SKILL.md (600-650 lines)
2. Extract detailed procedures to reference files (loaded on demand)
3. Maintain all functionality while achieving 65% token efficiency gain
4. Follow DevForgeAI's own architectural standards
5. Preserve existing 5 reference files and enhance with 1 new file

## Requirements

### Mandatory Actions

1. **Read Current Implementation**
   ```
   Read(file_path=".claude/skills/devforgeai-release/SKILL.md")
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
   Bash(command="ls -lh .claude/skills/devforgeai-release/references/")
   ```

4. **Enhance/Create Reference Files** (5 existing + 1 new = 6 total)

5. **Refactor Main SKILL.md** (reduce to 600-650 lines)

6. **Validate Result** (check line count, test references)

### Existing Reference Files (Keep and Enhance)

The release skill already has 5 reference files:

1. ✅ **`deployment-strategies.md`** (8.9KB, ~300 lines)
   - Contains: Blue-Green, Rolling, Canary, Recreate strategies
   - Status: Keep as-is, but ensure SKILL.md references it properly
   - Main SKILL.md should NOT duplicate strategy details

2. ✅ **`smoke-testing-guide.md`** (10.7KB, ~360 lines)
   - Contains: Standard smoke tests, critical path validation
   - Status: Keep as-is, but main SKILL.md should reference, not duplicate

3. ✅ **`rollback-procedures.md`** (4KB, ~135 lines)
   - Contains: Platform-specific rollback commands
   - Status: Keep as-is

4. ✅ **`monitoring-metrics.md`** (23.4KB, ~780 lines)
   - Contains: Metrics, baselines, alert thresholds
   - Status: Keep as-is

5. ✅ **`release-checklist.md`** (21.8KB, ~730 lines)
   - Contains: Pre/during/post deployment checklists
   - Status: Keep as-is

**Total Existing Reference Content**: ~2,305 lines across 5 files

### New Reference File to Create

#### 6. `references/platform-deployment-commands.md` (NEW)
**Content to Extract**:
- Kubernetes deployment commands (kubectl set image, helm upgrade, etc.)
- Azure App Service deployment commands (az webapp deployment)
- AWS ECS/Lambda deployment commands (aws ecs update-service, aws lambda update-function)
- Docker deployment commands
- Traditional VPS deployment commands (Ansible, Terraform)
- Platform-specific rollout status checks
- Platform-specific health check commands

**Estimated Size**: 400-500 lines

**What Stays in Main SKILL.md**:
```markdown
## Phase 3: Production Deployment

Select deployment strategy based on tech-stack.md.
For detailed deployment strategy procedures, see references/deployment-strategies.md

Execute deployment using platform-specific commands.
For platform command templates, see references/platform-deployment-commands.md

Example workflow:
1. Read deployment config from tech-stack.md
2. Load platform commands from reference
3. Execute deployment with selected strategy
4. Monitor rollout status
```

**Why This Reference is Needed**:
Currently, the main SKILL.md has extensive inline deployment command examples for:
- Lines 600-850: Detailed deployment strategy implementations with kubectl commands
- Lines 1680-1703: Tool usage examples with platform commands

This content should be in a reference file for on-demand loading.

### Refactored SKILL.md Structure

**Target Structure** (600-650 lines total):

```markdown
---
name: devforgeai-release
description: [Keep existing description]
allowed-tools: [Keep existing - deployment tools are essential]
  - Read, Write, Edit, Glob, Grep
  - AskUserQuestion
  - Bash(git:*), Bash(kubectl:*), Bash(docker:*), Bash(terraform:*), Bash(ansible:*)
  - Bash(az:*), Bash(aws:*), Bash(gcloud:*), Bash(helm:*)
  - Bash(dotnet:*), Bash(npm:*), Bash(pytest:*)
  - Skill
---

# DevForgeAI Release Skill

[Keep existing purpose statement - ~60 lines]

## Purpose

[Keep philosophy and core capabilities - ~40 lines]

## When to Use This Skill

[Keep usage guidance - ~40 lines]

---

## Release Workflow

### Phase 1: Pre-Release Validation (~80 lines)

#### Step 1: Verify QA Approval
- Load story file
- Check status == "QA Approved"
- Verify zero CRITICAL/HIGH violations
- For quality gate details, see references/release-checklist.md

#### Step 2: Dependency Check
- Verify prerequisite stories deployed
- Check deployment dependencies
- HALT if dependencies not met

#### Step 3: Environment Readiness
- Verify staging environment healthy
- Verify production environment available
- Check maintenance window
- For environment checklist, see references/release-checklist.md

---

### Phase 2: Staging Deployment (~80 lines)

#### Step 1: Deploy to Staging
- Read deployment config from tech-stack.md
- Select deployment strategy (blue-green, rolling, canary, recreate)
- For strategy details, see references/deployment-strategies.md
- For platform commands, see references/platform-deployment-commands.md

#### Step 2: Staging Smoke Tests
- Run smoke test suite against staging
- For smoke test procedures, see references/smoke-testing-guide.md
- HALT if tests fail

#### Step 3: Staging Validation
- Verify critical paths functional
- Check performance metrics acceptable
- For metrics baselines, see references/monitoring-metrics.md

---

### Phase 3: Production Deployment (~120 lines)

#### Step 1: Select Deployment Strategy
- Read from tech-stack.md or use AskUserQuestion
- Options: Blue-Green, Rolling Update, Canary, Recreate
- For detailed strategy procedures, see references/deployment-strategies.md

#### Step 2: Execute Production Deployment
- Load platform-specific commands
- For command templates, see references/platform-deployment-commands.md
- Execute deployment with selected strategy
- Monitor rollout status

**Example deployment workflow** (brief):
```
IF strategy == "Blue-Green":
  Deploy new version to green environment
  Run health checks on green
  Switch traffic from blue to green
  For detailed steps, see references/deployment-strategies.md
  For platform commands, see references/platform-deployment-commands.md
```

#### Step 3: Monitor Rollout
- Check rollout status per platform
- Watch for errors or degradation
- For monitoring setup, see references/monitoring-metrics.md

---

### Phase 4: Post-Deployment Validation (~80 lines)

#### Step 1: Production Smoke Tests
- Wait for stabilization (60 seconds)
- Run health check
- Execute smoke test suite
- For test procedures, see references/smoke-testing-guide.md
- If tests fail: Execute rollback (see references/rollback-procedures.md)

#### Step 2: Metrics Monitoring
- Collect production metrics
- Compare against baseline
- For metrics details, see references/monitoring-metrics.md
- If degradation detected: AskUserQuestion for rollback decision

#### Step 3: Declare Success or Rollback
- If all checks pass: Declare success
- If failures detected: Execute rollback (see references/rollback-procedures.md)

---

### Phase 5: Release Documentation (~60 lines)

#### Step 1: Generate Release Notes
- Extract changes from story document
- Generate release notes from template
- Update CHANGELOG.md

#### Step 2: Update Story Status
- Edit story file: status → "Released"
- Add workflow history entry
- Record deployment timestamp and version

#### Step 3: Git Tagging
- Create version tag
- Push tag to remote
- Document deployment in audit trail

---

### Phase 6: Post-Release Monitoring (~50 lines)

#### Step 1: Configure Alerts
- Set up monitoring alerts for key metrics
- For alert thresholds, see references/monitoring-metrics.md

#### Step 2: Schedule Review
- Plan post-release review (24 hours)
- Monitor for 24-48 hours for issues

#### Step 3: Report Success
- Generate deployment report
- Notify stakeholders
- Update release dashboard

---

## Tool Usage Protocol (~30 lines)

### Use Native Tools for File Operations
[Keep brief examples - 15 lines]

### Use Bash for Terminal Operations
[Keep brief examples - 15 lines]

---

## Reference Files (~40 lines)

Load these on demand during release execution:

### Deployment Procedures
- **`./references/deployment-strategies.md`** - Blue-green, canary, rolling, recreate strategies
- **`./references/platform-deployment-commands.md`** - Kubernetes, Azure, AWS, Docker, VPS commands

### Validation and Testing
- **`./references/smoke-testing-guide.md`** - Standard tests, critical path validation
- **`./references/rollback-procedures.md`** - Platform-specific rollback commands

### Monitoring and Checklists
- **`./references/monitoring-metrics.md`** - Metrics, baselines, alert thresholds
- **`./references/release-checklist.md`** - Pre/during/post deployment checklists

---

## Rollback Protocol (~40 lines)

### Automatic Rollback Triggers
- Health check fails
- Smoke tests fail
- Error rate >2x baseline
- Critical metric degradation

### Rollback Execution
See references/rollback-procedures.md for platform-specific commands

---

## Success Criteria (~30 lines)

[Keep existing success criteria]
```

**Total Estimated**: ~640 lines (within 600-650 target)

### Key Extraction Strategy

**Remove from Main SKILL.md**:

1. **Detailed Deployment Strategy Implementations** (lines 600-850, ~250 lines)
   - Blue-Green step-by-step with kubectl commands
   - Rolling Update with kubectl commands
   - Canary deployment 5→25→50→100% progression
   - Recreate deployment steps
   - **Move to**: `references/platform-deployment-commands.md` (platform commands) + reference `deployment-strategies.md` (strategies)
   - **Keep in Main**: Brief workflow outline + "see references/" pattern

2. **Platform-Specific Command Examples** (lines 1680-1703, ~25 lines)
   - Kubectl, helm, az, aws commands
   - **Move to**: `references/platform-deployment-commands.md`
   - **Keep in Main**: Tool usage principle only

3. **Verbose Smoke Test Procedures** (inline throughout)
   - Detailed test execution steps
   - **Already in**: `references/smoke-testing-guide.md`
   - **Action**: Remove duplication from main, reference only

4. **Metrics Collection Details** (inline in Phase 4)
   - Metric collection logic
   - Baseline comparison algorithms
   - **Already in**: `references/monitoring-metrics.md`
   - **Action**: Remove duplication from main, reference only

5. **Verbose AskUserQuestion Examples** (lines 1640-1656, ~15 lines per question)
   - Keep the usage, simplify the examples
   - **Reduction**: ~30 lines

**Estimated Savings**:
- Deployment strategies: ~250 lines
- Platform commands: ~25 lines
- Smoke test duplication: ~50 lines
- Metrics duplication: ~40 lines
- Simplified examples: ~30 lines
- **Total: ~395 lines** → **1,734 - 395 = 1,339 lines**

**Need Additional Reduction**: 1,339 → 640 target = ~700 more lines

**Additional Optimization**:
6. **Condense Phase Descriptions** (~150 lines saved)
   - Current phases are very verbose with detailed explanations
   - Can tighten language while keeping clarity

7. **Simplify Code Examples** (~100 lines saved)
   - Keep essential examples
   - Remove redundant variations

8. **Remove Narrative Prose** (~100 lines saved)
   - Replace explanatory paragraphs with direct instructions

9. **Consolidate Validation Steps** (~50 lines saved)
   - Similar validation patterns repeated across phases
   - Can create validation template referenced multiple times

**Total Additional**: ~400 lines → **1,339 - 400 = 939 lines**

**Final Push** (~300 line reduction needed):
10. **More Aggressive Reference Usage**
    - Move more procedure details to references
    - Keep only essential workflow structure
    - Can achieve 600-650 line target

### Validation Steps

After refactoring, validate the result:

```bash
# 1. Check line count
wc -l .claude/skills/devforgeai-release/SKILL.md
# Expected: 600-650 lines (acceptable up to 700 per Phase 1.1 lesson)

# 2. Check reference files exist
ls -lh .claude/skills/devforgeai-release/references/
# Expected: 6 files (5 existing + 1 new platform-deployment-commands.md)

# 3. Verify new reference file created
ls -lh .claude/skills/devforgeai-release/references/platform-deployment-commands.md
# Expected: Exists, ~400-500 lines

# 4. Verify all references exist
grep -o "references/[^)]*\.md" .claude/skills/devforgeai-release/SKILL.md | sort -u
# Ensure all referenced files exist

# 5. Check for content duplication
grep -c "kubectl set image" .claude/skills/devforgeai-release/SKILL.md
# Expected: 0-2 (brief examples only, details in reference)
```

### Key Implementation Guidelines

#### ✅ DO

1. **Preserve All Functionality**
   - All 6 phases must remain
   - All rollback capabilities preserved
   - All platform support maintained

2. **Use Direct Instructions**
   ```markdown
   ✅ CORRECT:
   ## Phase 3: Production Deployment
   Select deployment strategy from tech-stack.md
   For strategy details, see references/deployment-strategies.md
   For platform commands, see references/platform-deployment-commands.md

   Execute deployment:
   1. Load platform commands
   2. Execute with selected strategy
   3. Monitor rollout status
   4. Validate health checks
   ```

3. **Keep Brief Code Examples**
   ```markdown
   ✅ CORRECT:
   Example Blue-Green workflow:
   - Deploy to green environment
   - Test green environment
   - Switch traffic blue → green
   - For detailed commands, see references/platform-deployment-commands.md
   ```

4. **Reference Existing Files**
   - Don't recreate content that's already in references
   - Ensure main SKILL.md points to existing references correctly

#### ❌ DON'T

1. **Don't Duplicate Reference Content**
   ```markdown
   ❌ WRONG:
   ## Blue-Green Deployment
   [50 lines of detailed kubectl commands already in deployment-strategies.md]

   ✅ CORRECT:
   ## Blue-Green Deployment
   See references/deployment-strategies.md for detailed procedure
   See references/platform-deployment-commands.md for kubectl commands
   ```

2. **Don't Remove Essential Workflow**
   ```markdown
   ❌ WRONG:
   ## Phase 3: Production Deployment
   See references/deployment-strategies.md

   ✅ CORRECT:
   ## Phase 3: Production Deployment
   1. Select strategy
   2. Execute deployment
   3. Monitor rollout
   4. Validate success
   See references/deployment-strategies.md for detailed procedures
   ```

3. **Don't Over-Optimize**
   - Keep enough context for workflow understanding
   - 600-650 lines target (acceptable up to 700 if clarity demands it)
   - Don't sacrifice usability for strict line count

### Expected Outcome

**Before**:
```
.claude/skills/devforgeai-release/
├── SKILL.md (1,734 lines, 58KB, ~58,000 tokens)
└── references/ (5 files, ~2,305 lines)
```

**After**:
```
.claude/skills/devforgeai-release/
├── SKILL.md (600-650 lines, ~21KB, ~20,000 tokens)
└── references/
    ├── deployment-strategies.md (~300 lines) ✅ EXISTING
    ├── smoke-testing-guide.md (~360 lines) ✅ EXISTING
    ├── rollback-procedures.md (~135 lines) ✅ EXISTING
    ├── monitoring-metrics.md (~780 lines) ✅ EXISTING
    ├── release-checklist.md (~730 lines) ✅ EXISTING
    └── platform-deployment-commands.md (~450 lines) ✅ NEW
```

**Token Efficiency Gain**:
- Typical usage: Load SKILL.md only = ~20,000 tokens (65% reduction!)
- With deployment strategy: SKILL.md + deployment-strategies.md = ~28,000 tokens (52% reduction)
- With platform commands: SKILL.md + platform-deployment-commands.md = ~32,000 tokens (45% reduction)
- Maximum usage: SKILL.md + all references = ~60,000 tokens (but rare, only for complex multi-platform releases)

**Framework Compliance**:
- ✅ Within acceptable size (600-650 lines, or up to 700 with justification)
- ✅ Follows progressive disclosure pattern
- ✅ Uses native tools over Bash (preserved)
- ✅ References existing files correctly
- ✅ Follows source-tree.md directory structure

### Testing the Refactored Skill

After completing the refactor, test with:

```bash
# Start Claude Code
claude

# Test simple release (should load main + 1-2 references)
> Deploy STORY-001 to production using blue-green strategy

# Claude should:
# 1. Load main SKILL.md (~20K tokens)
# 2. Load deployment-strategies.md when needed (~8K tokens)
# 3. Load platform-deployment-commands.md when needed (~12K tokens)
# 4. Total: ~40K tokens (vs 58K original = 31% reduction)
# 5. Execute release workflow successfully

# Test rollback scenario
> Rollback STORY-001 deployment due to production issue

# Claude should:
# 1. Load main SKILL.md
# 2. Load rollback-procedures.md when needed
# 3. Execute rollback successfully
```

### Deliverables Checklist

When you complete this refactor, you should have:

- [ ] Main SKILL.md reduced to 600-650 lines (acceptable up to 700)
- [ ] 1 new reference file created (`platform-deployment-commands.md`)
- [ ] 5 existing reference files preserved and properly referenced
- [ ] All reference links working (no broken ./references/ links)
- [ ] No functionality lost (all 6 phases preserved)
- [ ] No content duplication between main and references
- [ ] Line count validated: `wc -l .claude/skills/devforgeai-release/SKILL.md`
- [ ] Directory structure validated: `ls -la .claude/skills/devforgeai-release/references/`
- [ ] Tested skill invocation successfully
- [ ] Token usage reduced by ~65% for typical usage

### Success Criteria

The refactor is successful when:

1. **Size Compliance**: SKILL.md is 600-700 lines (not 1,734)
2. **Progressive Disclosure**: References load on demand
3. **Functionality Preserved**: All release capabilities work
4. **Framework Compliant**: Follows all context file constraints
5. **Token Efficient**: 65% reduction in typical token usage
6. **Existing References**: All 5 existing reference files properly used
7. **New Reference**: Platform deployment commands extracted to new file

---

## Commands to Execute in Session

```bash
# 1. Read current implementation
Read(file_path=".claude/skills/devforgeai-release/SKILL.md")

# 2. Read context files
Read(file_path=".devforgeai/context/tech-stack.md")
Read(file_path=".devforgeai/context/coding-standards.md")
Read(file_path=".devforgeai/context/source-tree.md")

# 3. Check existing references
Bash(command="ls -lh .claude/skills/devforgeai-release/references/")

# 4. Read existing reference files to understand content
Read(file_path=".claude/skills/devforgeai-release/references/deployment-strategies.md")
Read(file_path=".claude/skills/devforgeai-release/references/smoke-testing-guide.md")

# 5. Create new reference file
Write(file_path=".claude/skills/devforgeai-release/references/platform-deployment-commands.md", content="...")

# 6. Rewrite main SKILL.md (use Write to replace entire file)
Write(file_path=".claude/skills/devforgeai-release/SKILL.md", content="[600-650 line refactored version]")

# 7. Validate
Bash(command="wc -l .claude/skills/devforgeai-release/SKILL.md")
Bash(command="ls -lh .claude/skills/devforgeai-release/references/")
```

---

## Post-Refactor Review Prompt

After completing the refactor in a new session, use this prompt for review:

```
I've completed the refactor of devforgeai-release skill. Please review:

1. Check line count: Is SKILL.md 600-700 lines?
2. Check references: Are all 6 files present (5 existing + 1 new)?
3. Check links: Do all references/[file].md links work?
4. Check new file: Does platform-deployment-commands.md exist with platform commands?
5. Check functionality: Are all 6 phases preserved?
6. Check compliance: Does it follow context file constraints?
7. Check duplication: Is content properly separated between main and references?

Files to review:
- .claude/skills/devforgeai-release/SKILL.md
- .claude/skills/devforgeai-release/references/platform-deployment-commands.md

Run validation:
- wc -l .claude/skills/devforgeai-release/SKILL.md
- ls -la .claude/skills/devforgeai-release/references/
- grep "references/" .claude/skills/devforgeai-release/SKILL.md
- grep -c "kubectl set image" .claude/skills/devforgeai-release/SKILL.md
```

---

**Remember**: Apply lessons from Phase 1.1 (devforgeai-qa):
- 600-650 lines is acceptable (up to 700 if code examples add clarity)
- Don't sacrifice workflow readability for strict line counts
- Keep brief code examples in main file for quick understanding
- Progressive disclosure is the goal, not minimalism
- All reference files should be properly utilized

**Phase 1.2 Objective**: Achieve similar success as Phase 1.1 with 65% token reduction while maintaining release workflow clarity and functionality.
