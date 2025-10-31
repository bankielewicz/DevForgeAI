# DevForgeAI Release Skill - Phase 5: Validation & Testing Plan

**Session Objective**: Validate the devforgeai-release skill implementation against requirements and ensure production readiness

**Context**: Phases 0-4 complete (97% done). This final phase validates quality, correctness, and integration.

---

## Quick Start Instructions

### 1. Load Context Files (Read these first)

```
Read the following files to understand what to validate:

1. Progress tracker:
   Read(file_path="/mnt/c/Projects/DevForgeAI2/PROMPT-implement-release-skill.md")

2. Completed skill file:
   Read(file_path="/mnt/c/Projects/DevForgeAI2/.claude/skills/devforgeai-release/SKILL.md")

3. Skill creator requirements:
   Read(file_path="/mnt/c/Projects/DevForgeAI2/.claude/skills/skill-creator/skill.md")

4. Design specification (for completeness check):
   Read(file_path="/mnt/c/Projects/DevForgeAI2/.devforgeai/specs/requirements/devforgeai-release-skill-design.md")
```

### 2. Current Status Summary

**Completed**:
- ✅ Phase 0: Preparation
- ✅ Phase 1: SKILL.md (18,000 tokens)
- ✅ Phase 2: Reference Files (5 files, 24,500 tokens)
- ✅ Phase 3: Asset Templates (3 files, 7,600 tokens)
- ✅ Phase 4: Automation Scripts (6 files, 22,550 tokens)

**Current Phase**: Phase 5 - Validation & Testing

**Total Progress**: 97% complete (72,650 / 75,000 tokens)

---

## Phase 5: Validation Checklist

Create a comprehensive validation plan covering 8 categories:

### Category 1: SKILL.md Completeness ✓

**Validation Items**:
- [ ] YAML frontmatter complete and valid
  - [ ] `name` field present and correct
  - [ ] `description` field clear and specific
  - [ ] `allowed-tools` includes all required tools:
    - [ ] Read, Write, Edit, Glob, Grep
    - [ ] AskUserQuestion
    - [ ] Bash(git:*), Bash(kubectl:*), Bash(docker:*)
    - [ ] Bash(terraform:*), Bash(ansible:*)
    - [ ] Bash(az:*), Bash(aws:*), Bash(gcloud:*), Bash(helm:*)
    - [ ] Bash(dotnet:*), Bash(npm:*), Bash(pytest:*)
    - [ ] Skill

- [ ] Purpose section clear and concise
- [ ] When to Use section comprehensive
  - [ ] Positive use cases (✅) documented
  - [ ] Negative use cases (❌) documented
  - [ ] Typical invocation examples provided

- [ ] 6-phase workflow implementation complete:
  - [ ] Phase 1: Pre-Release Validation
  - [ ] Phase 2: Staging Deployment
  - [ ] Phase 3: Production Deployment
  - [ ] Phase 4: Post-Deployment Validation
  - [ ] Phase 5: Release Documentation
  - [ ] Phase 6: Post-Release Monitoring

- [ ] Rollback procedures documented
  - [ ] Automatic rollback triggers
  - [ ] Platform-specific commands (Kubernetes, Azure, AWS, Docker)
  - [ ] Database rollback procedures
  - [ ] Post-rollback actions

- [ ] 8+ AskUserQuestion patterns documented
  - [ ] Pattern 1: Deployment strategy selection
  - [ ] Pattern 2: Degraded metrics decision
  - [ ] Pattern 3: Hotfix expedite decision
  - [ ] Pattern 4: Rollback confirmation
  - [ ] Pattern 5: Database backup decision
  - [ ] Pattern 6: Conflicting deployment resolution
  - [ ] Pattern 7: Manual testing decision
  - [ ] Pattern 8: Extended monitoring decision

- [ ] Tool usage protocol documented
  - [ ] Native tools for file operations
  - [ ] Bash for terminal operations
  - [ ] Examples provided

- [ ] Integration points clearly documented
  - [ ] From devforgeai-qa
  - [ ] To devforgeai-orchestration

- [ ] Success criteria section complete
- [ ] Reference materials section lists all files

**Validation Method**:
```
Read SKILL.md and verify each section exists with substantive content (not placeholders).
Cross-reference with design specification to ensure all requirements met.
```

---

### Category 2: Reference Files Quality ✓

**Validation Items**:
- [ ] All 5 reference files exist:
  - [ ] deployment-strategies.md
  - [ ] smoke-testing-guide.md
  - [ ] rollback-procedures.md
  - [ ] monitoring-metrics.md
  - [ ] release-checklist.md

- [ ] Each reference file has comprehensive content:
  - [ ] No TODO or placeholder sections
  - [ ] Code examples included where applicable
  - [ ] Platform-specific guidance provided
  - [ ] Best practices documented

- [ ] Reference files align with SKILL.md instructions
  - [ ] SKILL.md references these files appropriately
  - [ ] No conflicting information between SKILL.md and references

- [ ] Token efficiency achieved:
  - [ ] References not duplicated in SKILL.md
  - [ ] Progressive disclosure design followed

**Validation Method**:
```
Read each reference file and verify:
1. Content is comprehensive (not summary)
2. Code examples are executable
3. Cross-references to SKILL.md are valid
4. No information duplication across files
```

---

### Category 3: Asset Templates Validation ✓

**Validation Items**:
- [ ] All 3 templates exist:
  - [ ] release-notes-template.md
  - [ ] rollback-plan-template.md
  - [ ] deployment-config-template.yaml

- [ ] Templates have {{VARIABLE}} placeholders
  - [ ] All variables documented
  - [ ] Variable naming consistent

- [ ] Templates are production-ready:
  - [ ] Kubernetes YAML is valid
  - [ ] Markdown templates follow conventions
  - [ ] All sections present

- [ ] Templates align with scripts:
  - [ ] release_notes_generator.py uses template variables
  - [ ] Placeholder names match script expectations

**Validation Method**:
```
Read each template and verify:
1. All {{VARIABLES}} are documented
2. YAML syntax is valid (for deployment-config-template.yaml)
3. Templates are comprehensive, not minimal
```

---

### Category 4: Automation Scripts Validation ✓

**Validation Items**:
- [ ] All 6 files exist in scripts/ directory:
  - [ ] health_check.py
  - [ ] smoke_test_runner.py
  - [ ] metrics_collector.py
  - [ ] rollback_automation.sh
  - [ ] release_notes_generator.py
  - [ ] README.md

- [ ] Python scripts have required structure:
  - [ ] Shebang line (#!/usr/bin/env python3)
  - [ ] Module docstring with usage examples
  - [ ] argparse command-line interface
  - [ ] Logging configuration
  - [ ] main() function
  - [ ] Exit codes documented (0, 1, 2)
  - [ ] Error handling (try/except)

- [ ] Bash script has required structure:
  - [ ] Shebang line (#!/bin/bash)
  - [ ] Usage function
  - [ ] Argument parsing
  - [ ] Logging functions
  - [ ] Error handling (set -e)

- [ ] Scripts implement required functionality:
  - [ ] health_check.py: Retry logic with exponential backoff
  - [ ] smoke_test_runner.py: pytest orchestration
  - [ ] metrics_collector.py: Multi-backend support
  - [ ] rollback_automation.sh: 4 platform support
  - [ ] release_notes_generator.py: Template population

- [ ] README.md documents all scripts:
  - [ ] Installation instructions
  - [ ] Configuration requirements
  - [ ] Usage examples for each script
  - [ ] Troubleshooting section

**Validation Method**:
```
Read each script and verify:
1. Full implementation (no TODO comments or placeholders)
2. Command-line interface complete
3. Error handling comprehensive
4. Exit codes used correctly
5. README documents the script
```

---

### Category 5: Design Specification Compliance ✓

**Validation Items**:
- [ ] All design requirements implemented:
  - [ ] 6-phase release workflow
  - [ ] 4 deployment strategies (Blue-Green, Rolling, Canary, Recreate)
  - [ ] 6 platform support (Kubernetes, Azure, AWS ECS, AWS Lambda, Docker, VPS)
  - [ ] Release gates (QA approval, dependencies, environment readiness)
  - [ ] Smoke testing automation
  - [ ] Metrics monitoring and baseline comparison
  - [ ] Rollback capabilities
  - [ ] Release documentation generation

- [ ] Integration points match design:
  - [ ] Receives QA-approved stories from devforgeai-qa
  - [ ] Updates story status to "Released"
  - [ ] Generates release notes
  - [ ] Updates CHANGELOG.md
  - [ ] Configures post-release monitoring

- [ ] AskUserQuestion patterns align with design:
  - [ ] All decision points identified in design are implemented
  - [ ] Questions have clear options (2-4 choices)
  - [ ] Multi-select appropriately used

**Validation Method**:
```
Read design specification and create checklist of all requirements.
Cross-reference with SKILL.md implementation.
Verify each requirement has corresponding implementation.
```

---

### Category 6: Skill Creator Requirements ✓

**Validation Items**:
- [ ] Follows skill-creator guidelines:
  - [ ] YAML frontmatter format correct
  - [ ] Description is specific (not generic)
  - [ ] Description uses third-person ("This skill should be used when...")
  - [ ] Imperative/infinitive form used throughout (not second person)
  - [ ] No emojis (unless explicitly required)

- [ ] Progressive disclosure design:
  - [ ] Metadata (name + description): ~100 words ✓
  - [ ] SKILL.md body: ~18,000 tokens ✓
  - [ ] Bundled resources: Load as needed ✓

- [ ] Tool usage follows conventions:
  - [ ] Native tools (Read, Write, Edit, Glob, Grep) for file operations
  - [ ] Bash for terminal operations only
  - [ ] No communication via echo/printf

- [ ] References organized correctly:
  - [ ] references/ contains documentation to load into context
  - [ ] assets/ contains files for output (not to load)
  - [ ] scripts/ contains executable code

- [ ] Quality standards met:
  - [ ] Comprehensive implementation (no "concise versions")
  - [ ] Code examples included
  - [ ] Platform coverage complete
  - [ ] No shortcuts taken

**Validation Method**:
```
Read skill-creator requirements document.
Verify skill follows all guidelines (metadata, structure, writing style).
Check that progressive disclosure design is used correctly.
```

---

### Category 7: Integration Testing (Dry Run) ✓

**Validation Items**:
- [ ] SKILL.md references are valid:
  - [ ] All reference file paths exist
  - [ ] All asset template paths exist
  - [ ] All script paths exist
  - [ ] No broken links to non-existent files

- [ ] Scripts can be found by SKILL.md:
  - [ ] SKILL.md uses correct paths: `{SKILL_DIR}/scripts/script_name.py`
  - [ ] Scripts directory structure matches expectations

- [ ] Workflow integration points:
  - [ ] Story status checks reference correct values ("QA Approved")
  - [ ] File paths match DevForgeAI conventions (.ai_docs/Stories/, .devforgeai/)
  - [ ] Git workflow commands are valid

- [ ] AskUserQuestion invocations:
  - [ ] All questions have valid syntax
  - [ ] Options are mutually exclusive (unless multiSelect: true)
  - [ ] Each question has 2-4 options
  - [ ] Headers are concise (<12 chars)

- [ ] Bash command patterns:
  - [ ] All Bash commands use allowed-tools patterns
  - [ ] No disallowed commands (cat, grep, find for file operations)
  - [ ] Git commands follow conventions

**Validation Method**:
```
Simulate skill invocation:
1. Verify SKILL.md loads without errors
2. Check all file path references
3. Validate AskUserQuestion syntax
4. Verify Bash commands match allowed-tools
```

---

### Category 8: Token Efficiency Analysis ✓

**Validation Items**:
- [ ] Native tools used for file operations:
  - [ ] SKILL.md demonstrates Read/Write/Edit usage
  - [ ] No `cat`, `grep`, `find` for file operations
  - [ ] Bash reserved for git, kubectl, docker, etc.

- [ ] Progressive disclosure followed:
  - [ ] SKILL.md is focused (instructions only)
  - [ ] Detailed info moved to reference files
  - [ ] Scripts externalized (not inline in SKILL.md)

- [ ] Token budget met:
  - [ ] SKILL.md: ~18,000 tokens ✓
  - [ ] References: ~24,500 tokens ✓
  - [ ] Templates: ~7,600 tokens ✓
  - [ ] Scripts: ~22,550 tokens ✓
  - [ ] Total: ~72,650 tokens (97% of 75,000 budget) ✓

- [ ] No token waste:
  - [ ] No duplicate information across files
  - [ ] Instructions are procedural (not explanatory)
  - [ ] Code examples are concise but complete

**Validation Method**:
```
Review SKILL.md for efficiency:
1. Check for native tool usage examples
2. Verify no file operation Bash commands
3. Confirm token budget alignment
4. Identify any duplicate content across files
```

---

## Validation Execution Plan

### Step 1: Create Validation Todo List

```
Use TodoWrite to create validation checklist with 8 items:
1. Validate SKILL.md completeness
2. Validate reference files quality
3. Validate asset templates
4. Validate automation scripts
5. Validate design specification compliance
6. Validate skill creator requirements
7. Integration testing (dry run)
8. Token efficiency analysis
```

### Step 2: Execute Validation (Category by Category)

For each category:
1. Mark todo as "in_progress"
2. Read relevant files
3. Verify each checklist item
4. Document any issues found
5. Mark todo as "completed"

### Step 3: Generate Validation Report

Create validation report documenting:
- All validation checks performed
- Pass/fail status for each category
- Issues found (if any)
- Recommendations for fixes (if needed)
- Overall skill quality assessment

**Report Location**: `.devforgeai/qa/skill-validation-report.md`

### Step 4: Update Progress Tracker

After validation complete:
```
Edit(file_path="/mnt/c/Projects/DevForgeAI2/PROMPT-implement-release-skill.md",
     old_string="**Current Status**: Phase 4 Complete (Scripts) - Phase 5 Pending (Validation)",
     new_string="**Current Status**: Phase 5 Complete (Validation) - Skill Ready for Use")

Update checklist items to mark validation complete
Update token budget table with final counts
```

---

## Validation Success Criteria

Phase 5 is complete when:

- [x] All 8 validation categories reviewed
- [x] SKILL.md meets skill-creator requirements
- [x] All reference files comprehensive and correct
- [x] All templates production-ready
- [x] All scripts fully implemented
- [x] Design specification requirements met
- [x] Integration points validated
- [x] Token efficiency achieved
- [x] Validation report generated
- [x] No critical issues found
- [x] Progress tracker updated

---

## Issues Resolution Process

If validation finds issues:

### Critical Issues (Must Fix)
- Missing required sections in SKILL.md
- Broken file path references
- Invalid AskUserQuestion syntax
- Scripts with placeholder code
- Design requirements not implemented

**Action**: Fix immediately before declaring skill complete

### Minor Issues (Should Fix)
- Typos or formatting inconsistencies
- Non-optimal token usage
- Missing best practices
- Documentation gaps

**Action**: Document in validation report, fix if time permits

### Enhancement Opportunities (Nice to Have)
- Additional code examples
- More comprehensive error handling
- Extended platform support

**Action**: Document for future enhancement

---

## Expected Validation Duration

- **Category 1-3**: 15 minutes (file completeness checks)
- **Category 4**: 20 minutes (script validation - 6 files)
- **Category 5-6**: 15 minutes (requirements compliance)
- **Category 7**: 10 minutes (integration dry run)
- **Category 8**: 10 minutes (token efficiency)
- **Report Generation**: 10 minutes

**Total Estimated Time**: 80 minutes (~1.5 hours)

---

## Quality Thresholds

### Pass Criteria
- ✅ 100% of required sections present in SKILL.md
- ✅ All 5 reference files comprehensive
- ✅ All 3 templates production-ready
- ✅ All 6 scripts fully implemented
- ✅ Zero broken file path references
- ✅ All design requirements implemented
- ✅ Token budget within 10% of target (67.5k - 82.5k)

### Fail Criteria
- ❌ Missing required SKILL.md sections
- ❌ Placeholder content (TODO, TBD)
- ❌ Broken references to non-existent files
- ❌ Scripts with incomplete implementations
- ❌ Design requirements not met
- ❌ Token budget exceeded by >25% (>93.75k)

---

## Validation Report Template

```markdown
# DevForgeAI Release Skill - Validation Report

**Date**: YYYY-MM-DD
**Skill Version**: 1.0.0
**Validator**: DevForgeAI QA Agent

## Summary

- **Overall Status**: PASS / FAIL
- **Categories Validated**: 8/8
- **Critical Issues**: 0
- **Minor Issues**: N
- **Enhancements**: N

## Category Results

### 1. SKILL.md Completeness
- **Status**: PASS / FAIL
- **Details**: [Summary of findings]
- **Issues**: [List any issues]

### 2. Reference Files Quality
- **Status**: PASS / FAIL
- **Details**: [Summary of findings]
- **Issues**: [List any issues]

[... for each category ...]

## Token Budget Analysis

| Component | Estimated | Actual | Variance |
|-----------|-----------|--------|----------|
| SKILL.md | 18,000 | X,XXX | ±X% |
| References | 20,000 | 24,500 | +22.5% |
| Templates | 5,000 | 7,600 | +52% |
| Scripts | 16,000 | 22,550 | +41% |
| **TOTAL** | 75,000 | 72,650 | -3.1% |

**Assessment**: Within budget ✓

## Integration Validation

- [x] File path references valid
- [x] AskUserQuestion syntax correct
- [x] Bash commands within allowed-tools
- [x] Story status checks valid
- [x] Integration points documented

## Recommendations

1. [If any issues found, list recommendations]
2. [Enhancement opportunities]
3. [Future improvements]

## Sign-Off

**Skill Ready for Production Use**: YES / NO

**Validation Complete**: YYYY-MM-DD HH:MM:SS
```

---

## Post-Validation Actions

After validation passes:

1. **Create skill package** (if needed):
   ```bash
   # Use skill packaging script (if available)
   scripts/package_skill.py .claude/skills/devforgeai-release
   ```

2. **Document skill usage**:
   - Add skill to project README
   - Document integration with other skills
   - Provide example invocations

3. **Test with real story** (optional):
   - Create test story with "QA Approved" status
   - Invoke skill: `Skill(command="devforgeai-release --story=TEST-001")`
   - Verify workflow executes correctly

4. **Declare skill production-ready**:
   - Update progress tracker to 100% complete
   - Mark skill as available for use
   - Communicate completion to stakeholders

---

## Important Reminders

1. **Read Before Validating**: Load all context files to understand what was implemented
2. **No Shortcuts**: Validate every category thoroughly, don't skip items
3. **Document Issues**: If problems found, document clearly for resolution
4. **Use Native Tools**: Validation should use Read/Glob/Grep (not Bash file operations)
5. **Update Progress Tracker**: Mark validation complete when done
6. **Generate Report**: Validation report provides audit trail

---

## Start Command

```
Begin Phase 5 validation:

1. Read progress tracker to understand current state
2. Read SKILL.md to understand implementation
3. Read skill-creator requirements to understand standards
4. Create validation todo list (8 categories)
5. Execute validation category by category
6. Generate validation report
7. Update progress tracker when complete
```

**Good luck! This is the final phase - comprehensive validation ensures the skill is production-ready.**
