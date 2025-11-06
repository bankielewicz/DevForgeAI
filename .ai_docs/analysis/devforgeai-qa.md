# DevForgeAI QA Skill - Refactoring Plan

**Status:** NOT STARTED
**Assigned Session:** None
**Last Updated:** 2025-01-06 (Initial Creation)
**Estimated Effort:** 3-4 hours
**Priority:** P2 - HIGH (Sixth: 6.7x over limit)

---

## Executive Summary

The `devforgeai-qa` skill is **1,330 lines**, which is **6.7x over the optimal 200-line limit**.

**Key Issue:** Despite having 9 excellent reference files (4,796 lines), the SKILL.md contains complete Phase 0-5 implementation inline (875 lines of workflow logic).

**Target:** Reduce SKILL.md from 1,330 lines to ~190 lines while maintaining rigorous quality validation through improved progressive disclosure.

**Expected Gains:**
- **Token efficiency:** 7x improvement on skill activation
- **Activation time:** 400ms+ → <100ms (estimated)
- **Context relevance:** 22% → 90%+ (mode-specific loading)

---

## Current State Analysis

### Metrics

| Metric | Current | Target | Gap |
|--------|---------|--------|-----|
| **SKILL.md lines** | 1,330 | ~190 | -1,140 (-86%) |
| **References files** | 9 files | 13-15 files | +4-6 |
| **References lines** | 4,796 | ~7,000 | +2,204 |
| **Total lines** | 6,126 | ~7,190 | +1,064 |
| **Entry point ratio** | 21.7% | ~2.6% | -19.1% |
| **Cold start load** | 1,330 lines | <200 lines | -1,130 |
| **Estimated tokens** | ~10,640 | ~1,520 | -9,120 (-86%) |

### Current Structure (Line Distribution)

```
SKILL.md (1,330 lines total):
├─ Lines 1-12:      YAML Frontmatter (12 lines)
├─ Lines 14-99:     Parameter Extraction (86 lines) → EXTRACT
├─ Lines 101-164:   Protocol Adherence (64 lines) → EXTRACT to dod-protocol.md
├─ Lines 166-190:   Purpose & When to Use (25 lines) ✅ KEEP
├─ Lines 192-242:   Validation Modes (51 lines) ✅ KEEP (condense to 30)
├─ Lines 244-347:   Phase 1: Coverage (104 lines) → EXTRACT
├─ Lines 349-464:   Phase 2: Anti-Patterns (116 lines) → EXTRACT
├─ Lines 466-814:   Phase 3: Spec Compliance (349 lines) → EXTRACT (massive!)
│  ├─ Step 0: Story documentation (83 lines)
│  ├─ Step 2.5: Deferral validation (161 lines)
│  └─ Steps 1-5: Other validations (105 lines)
├─ Lines 816-906:   Phase 4: Code Quality (91 lines) → EXTRACT
├─ Lines 908-1138:  Phase 5: QA Report (231 lines) → EXTRACT
│  ├─ Steps 1-5: Report generation (152 lines)
│  └─ Step 6: qa-result-interpreter invocation (79 lines)
├─ Lines 1140-1264: Automation Scripts (125 lines) → EXTRACT
├─ Lines 1266-1286: Success Criteria (21 lines) ✅ KEEP (condense to 15)
├─ Lines 1288-1313: Reference Files List (26 lines) ✅ KEEP (update)
├─ Lines 1315-1330: Token Budget (16 lines) ✅ KEEP (condense to 10)
```

### Existing Reference Files (Excellent Quality)

| File | Lines | Status | Usage |
|------|-------|--------|-------|
| anti-pattern-detection.md | 411 | ✅ Excellent | Phase 2 |
| coverage-analysis.md | 876 | ✅ Excellent | Phase 1 |
| deferral-decision-tree.md | 823 | ✅ Excellent | Phase 3 Step 2.5 |
| language-specific-tooling.md | 1,036 | ✅ Excellent | Test execution |
| qa-result-formatting-guide.md | 580 | ✅ Excellent | qa-result-interpreter guardrails |
| quality-metrics.md | 76 | ✅ Good | Phase 4 |
| security-scanning.md | 121 | ✅ Good | Phase 2 Step 3 |
| spec-validation.md | 273 | ✅ Good | Phase 3 |
| validation-procedures.md | 600 | ✅ Excellent | General procedures |

**Observation:** Reference files are comprehensive. SKILL.md duplicates Phase 1-5 workflow logic instead of just pointing to them.

### Problems Identified

1. **Phase 3 Spec Compliance Massive (349 lines)**
   - 26% of entire SKILL.md
   - Contains Step 0 (story docs), Step 2.5 (deferral validation), Steps 1-5
   - Step 2.5 alone is 161 lines (deferral validation logic)
   - Should be: Brief summary + pointers to spec-compliance-workflow.md
   - Extract to: spec-compliance-workflow.md

2. **Phase 5 Report Generation (231 lines)**
   - 17% of SKILL.md
   - Includes qa-result-interpreter invocation (79 lines)
   - Should be: Summary + pointer to report-generation.md
   - Extract to: report-generation.md

3. **Protocol Adherence Section (64 lines)**
   - Important DoD protocol rules
   - Should be: Brief note + pointer to dod-protocol.md
   - Extract to: dod-protocol.md (new file, distinct from dod-validation-checkpoint.md in development skill)

4. **Automation Scripts Documentation (125 lines)**
   - Python script documentation inline
   - Should be: Brief note + pointer to automation-scripts.md
   - Extract to: automation-scripts.md

5. **Parameter Extraction (86 lines)**
   - Similar pattern to other skills
   - Extract to: parameter-extraction.md

---

## Target State Design

### Entry Point (SKILL.md ~190 lines)

```markdown
SKILL.md (Target: 190 lines)
├─ YAML Frontmatter (12 lines)
├─ Parameter Extraction (Brief) (15 lines)
│  └─ "Extract story ID and mode → See parameter-extraction.md"
├─ DoD Protocol Note (15 lines)
│  └─ "CRITICAL: Never skip Step 2.5 → See dod-protocol.md"
├─ Purpose & When to Use (25 lines)
├─ Validation Modes (30 lines)
│  ├─ Light: Build, tests, quick scans (~10K tokens)
│  └─ Deep: Coverage, anti-patterns, metrics (~65K tokens)
├─ QA Workflow (5 Phases) (45 lines)
│  ├─ Phase 1: Coverage → coverage-analysis-workflow.md
│  ├─ Phase 2: Anti-Patterns → anti-pattern-detection-workflow.md
│  ├─ Phase 3: Spec Compliance → spec-compliance-workflow.md
│  ├─ Phase 4: Code Quality → code-quality-workflow.md
│  └─ Phase 5: Report Generation → report-generation.md
├─ Automation Scripts Note (15 lines)
│  └─ "6 Python scripts → See automation-scripts.md"
├─ Integration (15 lines)
├─ Subagent Coordination (15 lines)
│  ├─ deferral-validator (Phase 3 Step 2.5)
│  └─ qa-result-interpreter (Phase 5 Step 6)
├─ Success Criteria (15 lines)
├─ Reference File Map (20 lines)
│  └─ 15 reference files listed
└─ Token Budget Note (10 lines)

Total: ~190 lines
```

### New Reference Files to Create

| New File | Lines | Source (from SKILL.md) | Purpose |
|----------|-------|------------------------|---------|
| **parameter-extraction.md** | ~120 | Lines 14-99 (86 lines) | Story ID and mode extraction |
| **dod-protocol.md** | ~100 | Lines 101-164 (64 lines) | DoD adherence requirements |
| **coverage-analysis-workflow.md** | ~140 | Lines 244-347 (104 lines) | Phase 1: 7 steps |
| **anti-pattern-detection-workflow.md** | ~150 | Lines 349-464 (116 lines) | Phase 2: 4 steps |
| **spec-compliance-workflow.md** | ~400 | Lines 466-814 (349 lines) | Phase 3: 6 steps including deferral |
| **code-quality-workflow.md** | ~120 | Lines 816-906 (91 lines) | Phase 4: 5 steps |
| **report-generation.md** | ~280 | Lines 908-1138 (231 lines) | Phase 5: Report + formatter |
| **automation-scripts.md** | ~180 | Lines 1140-1264 (125 lines) | Python scripts usage |

### Keep Existing Reference Files

| File | Current | Action | Purpose |
|------|---------|--------|---------|
| anti-pattern-detection.md | 411 | ✅ KEEP | Referenced by Phase 2 |
| coverage-analysis.md | 876 | ✅ KEEP | Referenced by Phase 1 |
| deferral-decision-tree.md | 823 | ✅ KEEP | Referenced by Phase 3 Step 2.5 |
| language-specific-tooling.md | 1,036 | ✅ KEEP | Test execution tools |
| qa-result-formatting-guide.md | 580 | ✅ KEEP | qa-result-interpreter guardrails |
| quality-metrics.md | 76 | ✅ KEEP | Referenced by Phase 4 |
| security-scanning.md | 121 | ✅ KEEP | Referenced by Phase 2 Step 3 |
| spec-validation.md | 273 | ✅ KEEP | Referenced by Phase 3 |
| validation-procedures.md | 600 | ✅ KEEP | General procedures |

**Pattern:** Workflow files reference guide files. For example:
- `coverage-analysis-workflow.md` (workflow) → `coverage-analysis.md` (guide with thresholds)
- `anti-pattern-detection-workflow.md` (workflow) → `anti-pattern-detection.md` (detection patterns)

### Token Efficiency Projection

**Before:**
- SKILL.md activation: 1,330 lines × 8 tokens/line = **10,640 tokens**
- References loaded: 0 (until explicitly read)
- **Total first load: ~10,640 tokens**

**After:**
- SKILL.md activation: 190 lines × 8 tokens/line = **1,520 tokens**
- Light mode: Entry + Phase 1,2 references = 1,520 + 2,320 = ~3,840 tokens
- Deep mode: Entry + Phase 1-5 references = 1,520 + 9,600 = ~11,120 tokens
- **Total first load: ~1,520 tokens**
- **Typical light usage: ~3,840 tokens** (7x more efficient than current)
- **Typical deep usage: ~11,120 tokens** (same as current, but progressive)

**Efficiency Gain:** 7x improvement on activation (10,640 → 1,520 tokens)

---

## Refactoring Steps

### Phase 1: Preparation and Backup

#### Step 1.1: Create Backup
```bash
cd .claude/skills/devforgeai-qa/
cp SKILL.md SKILL.md.backup-2025-01-06
cp SKILL.md SKILL.md.original-1330-lines
```

**Validation:**
- [ ] Backup file created
- [ ] Backup file has 1,330 lines
- [ ] Original preserved

---

### Phase 2: Extract Content to New Reference Files

**Order of Extraction:**

#### Step 2.1: Extract Parameter Extraction → `references/parameter-extraction.md`

**Source:** Lines 14-99 (86 lines)

**Commands:**
```bash
cd references/

awk '/^## CRITICAL: Extracting Parameters/,/^## CRITICAL RULE: Protocol Adherence/' ../SKILL.md > parameter-extraction-temp.md

cat > parameter-extraction.md <<'EOF'
# Parameter Extraction from Conversation Context

How QA skill extracts story ID and validation mode from conversation.

## Story ID Extraction

[Complete algorithm from SKILL.md]

## Validation Mode Extraction

[Complete logic for deep vs light]

EOF

tail -n +2 parameter-extraction-temp.md >> parameter-extraction.md
rm parameter-extraction-temp.md
```

**Validation:**
- [ ] File created: `references/parameter-extraction.md`
- [ ] Line count: ~120 lines

#### Step 2.2: Extract DoD Protocol → `references/dod-protocol.md`

**Source:** Lines 101-164 (64 lines)

**Commands:**
```bash
cd references/

awk '/^## CRITICAL RULE: Protocol Adherence/,/^## Purpose/' ../SKILL.md > dod-protocol-temp.md

cat > dod-protocol.md <<'EOF'
# Definition of Done Protocol

CRITICAL requirements for DoD validation that CANNOT be skipped.

## PROHIBITED Shortcuts

[From SKILL.md]

## Required Actions

[From SKILL.md]

## Enforcement

[From SKILL.md]

## Rationale

[From SKILL.md]

EOF

tail -n +2 dod-protocol-temp.md >> dod-protocol.md
rm dod-protocol-temp.md
```

**Validation:**
- [ ] File created: `references/dod-protocol.md`
- [ ] Line count: ~100 lines

#### Step 2.3: Extract Phase 1 → `references/coverage-analysis-workflow.md`

**Source:** Lines 244-347 (104 lines)

**Commands:**
```bash
cd references/

awk '/^## Phase 1: Test Coverage Analysis/,/^## Phase 2: Anti-Pattern Detection/' ../SKILL.md > coverage-analysis-workflow-temp.md

cat > coverage-analysis-workflow.md <<'EOF'
# Phase 1: Test Coverage Analysis Workflow

Execute 7-step coverage analysis and validation.

## Overview

Analyzes test coverage by layer (business, application, infrastructure) and validates against thresholds.

## References Used

This workflow references:
- coverage-analysis.md (thresholds, analysis procedures)

EOF

tail -n +2 coverage-analysis-workflow-temp.md >> coverage-analysis-workflow.md
rm coverage-analysis-workflow-temp.md
```

**Validation:**
- [ ] File created: `references/coverage-analysis-workflow.md`
- [ ] Line count: ~140 lines

#### Step 2.4: Extract Phase 2 → `references/anti-pattern-detection-workflow.md`

**Source:** Lines 349-464 (116 lines)

**Commands:**
```bash
cd references/

awk '/^## Phase 2: Anti-Pattern Detection/,/^## Phase 3: Spec Compliance/' ../SKILL.md > anti-pattern-detection-workflow-temp.md

cat > anti-pattern-detection-workflow.md <<'EOF'
# Phase 2: Anti-Pattern Detection Workflow

Execute 4-step anti-pattern scanning and security checks.

## References Used

This workflow references:
- anti-pattern-detection.md (detection patterns)
- security-scanning.md (OWASP Top 10 checks)

EOF

tail -n +2 anti-pattern-detection-workflow-temp.md >> anti-pattern-detection-workflow.md
rm anti-pattern-detection-workflow-temp.md
```

**Validation:**
- [ ] File created: `references/anti-pattern-detection-workflow.md`
- [ ] Line count: ~150 lines

#### Step 2.5: Extract Phase 3 → `references/spec-compliance-workflow.md` (MASSIVE)

**Source:** Lines 466-814 (349 lines - 26% of SKILL.md!)

**File structure:**
```markdown
# Phase 3: Spec Compliance Validation Workflow

Execute 6-step spec compliance validation including MANDATORY deferral validation.

## Overview

Phase 3 ensures implementation matches story specification and validates all deferred Definition of Done items.

## Step 0: Validate Story Documentation (CRITICAL)

[Complete logic from SKILL.md lines ~468-550]

### Documentation Requirements

[Requirements list...]

## Step 1: Load Story Specification

[Logic from lines ~551-562]

## Step 2: Validate Acceptance Criteria

[Logic from lines ~563-589]

## Step 2.5: Validate Deferred Definition of Done Items (MANDATORY - CANNOT SKIP)

**This step CANNOT be skipped or deferred. See dod-protocol.md for rationale.**

[Complete logic from lines 590-750 - 161 lines!]

### deferral-validator Subagent Invocation

Task(
  subagent_type="deferral-validator",
  description="Validate deferred DoD items",
  prompt="..."
)

### Violation Handling

**CRITICAL violations (circular deferrals):**
- QA status: FAILED
- Block progression

**HIGH violations (unjustified deferrals):**
- QA status: FAILED
- Require justification or implementation

### References Used

- deferral-decision-tree.md (decision logic)
- dod-protocol.md (adherence requirements)

## Step 3: Validate API Contracts

[Logic from lines ~751-775]

## Step 4: Validate Non-Functional Requirements

[Logic from lines ~776-796]

## Step 5: Generate Traceability Matrix

[Logic from lines ~797-814]

### References Used

This workflow references:
- spec-validation.md (validation procedures)
- deferral-decision-tree.md (Step 2.5 decision logic)

EOF
```

**Commands:**
```bash
cd references/

awk '/^## Phase 3: Spec Compliance Validation/,/^## Phase 4: Code Quality/' ../SKILL.md > spec-compliance-workflow-temp.md

cat > spec-compliance-workflow.md <<'EOF'
# Phase 3: Spec Compliance Validation Workflow

Execute 6-step spec compliance validation including MANDATORY deferral validation.

EOF

tail -n +2 spec-compliance-workflow-temp.md >> spec-compliance-workflow.md
rm spec-compliance-workflow-temp.md
```

**Validation:**
- [ ] File created: `references/spec-compliance-workflow.md`
- [ ] Line count: ~400 lines
- [ ] Step 2.5 deferral validation preserved (CRITICAL)

#### Step 2.6: Extract Phase 4 → `references/code-quality-workflow.md`

**Source:** Lines 816-906 (91 lines)

**Commands:**
```bash
cd references/

awk '/^## Phase 4: Code Quality Metrics/,/^## Phase 5: Generate QA Report/' ../SKILL.md > code-quality-workflow-temp.md

cat > code-quality-workflow.md <<'EOF'
# Phase 4: Code Quality Metrics Workflow

Execute 5-step code quality analysis.

## References Used

This workflow references:
- quality-metrics.md (metric thresholds)

EOF

tail -n +2 code-quality-workflow-temp.md >> code-quality-workflow.md
rm code-quality-workflow-temp.md
```

**Validation:**
- [ ] File created: `references/code-quality-workflow.md`
- [ ] Line count: ~120 lines

#### Step 2.7: Extract Phase 5 → `references/report-generation.md`

**Source:** Lines 908-1138 (231 lines)

**File structure:**
```markdown
# Phase 5: QA Report Generation Workflow

Generate comprehensive QA report and invoke qa-result-interpreter subagent.

## Step 1: Aggregate Results

[Logic from SKILL.md]

## Step 2: Determine Overall Status

[Logic...]

### Status Decision Logic

- PASSED: All checks pass
- FAILED: CRITICAL or HIGH violations, or coverage below threshold
- PARTIAL: Warnings only

## Step 3: Write QA Report

[Logic...]

### Report Template

[Template structure from SKILL.md lines ~982-1004]

## Step 4: Update Story Status

[Logic from lines ~1012-1033]

### Status Transitions

- PASSED → "QA Approved"
- FAILED → "QA Failed"

## Step 5: Track QA Iteration History

[Logic from lines ~1034-1138]

### History Entry Template

[Template from lines ~1054-1139]

## Step 6: Invoke qa-result-interpreter Subagent

**Purpose:** Parse report and generate user-facing display

Task(
  subagent_type="qa-result-interpreter",
  description="Interpret QA results",
  prompt="..."
)

### Subagent Output

Returns structured JSON:
- display.template (PASSED/FAILED/PARTIAL template)
- violations (categorized list)
- recommendations (next steps)

### References Used by Subagent

- qa-result-formatting-guide.md (display guidelines, framework constraints)

## Output

QA report file, story status updated, iteration history, formatted display for user.

EOF
```

**Commands:**
```bash
cd references/

awk '/^## Phase 5: Generate QA Report/,/^## Automation Scripts/' ../SKILL.md > report-generation-temp.md

cat > report-generation.md <<'EOF'
# Phase 5: QA Report Generation Workflow

Generate comprehensive QA report and invoke qa-result-interpreter subagent.

EOF

tail -n +2 report-generation-temp.md >> report-generation.md
rm report-generation-temp.md
```

**Validation:**
- [ ] File created: `references/report-generation.md`
- [ ] Line count: ~280 lines
- [ ] qa-result-interpreter invocation documented

#### Step 2.8: Extract Automation Scripts → `references/automation-scripts.md`

**Source:** Lines 1140-1264 (125 lines)

**Commands:**
```bash
cd references/

awk '/^## Automation Scripts/,/^## Success Criteria/' ../SKILL.md > automation-scripts-temp.md

cat > automation-scripts.md <<'EOF'
# Automation Scripts Documentation

6 Python scripts for automated quality analysis.

EOF

tail -n +2 automation-scripts-temp.md >> automation-scripts.md
rm automation-scripts-temp.md
```

**Validation:**
- [ ] File created: `references/automation-scripts.md`
- [ ] Line count: ~180 lines

---

### Phase 3: Rewrite Entry Point SKILL.md

**Target:** ~190 lines

#### Step 3.1: Create New SKILL.md Structure

```bash
cd .claude/skills/devforgeai-qa/

cat > SKILL.md.new <<'EOF'
---
name: devforgeai-qa
description: Validates code quality through hybrid progressive validation (light checks during development, deep analysis after completion). Enforces test coverage (95%/85%/80% strict thresholds), detects anti-patterns, validates spec compliance, and analyzes code quality metrics. Use when validating implementations, ensuring quality standards, or preparing for release.
allowed-tools:
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - Bash
  - Task
model: sonnet
---

# DevForgeAI QA Skill

Validate code quality through comprehensive testing, anti-pattern detection, and spec compliance verification.

## Parameter Extraction

This skill extracts story ID and validation mode (light/deep) from conversation context.

**See `references/parameter-extraction.md` for complete extraction algorithm.**

---

## CRITICAL: Definition of Done Protocol

**Step 2.5 (Deferral Validation) CANNOT be skipped.**

All deferred DoD items MUST:
- Have explicit user approval
- Reference follow-up story or ADR
- Have technical justification

**PROHIBITED:** Autonomous deferrals (AI deciding to defer without user approval)

**See `references/dod-protocol.md` for complete protocol requirements and enforcement.**

---

## Purpose

Enforce quality standards through automated validation at two levels:
- **Light validation** (~10K tokens) - During development for rapid feedback
- **Deep validation** (~65K tokens) - After completion for comprehensive analysis

---

## When to Use

### Automatic Invocation (Light Mode)
- After TDD Green phase (devforgeai-development Phase 2)
- After TDD Refactor phase (devforgeai-development Phase 3)

### Manual Invocation
- After story completion (deep mode)
- Pre-release validation (deep mode)
- Mid-development checks (light mode)

---

## Validation Modes

### Light Validation (~10,000 tokens)
**Duration:** 2-3 minutes
**Scope:**
- Build/syntax checks
- Test execution (all tests must pass)
- Quick anti-pattern scan (critical only)
- Deferral validation (MANDATORY - Step 2.5)

**When to use:** During development iterations

### Deep Validation (~65,000 tokens)
**Duration:** 8-12 minutes
**Scope:**
- Complete test coverage analysis (by layer)
- Comprehensive anti-pattern detection (all categories)
- Full spec compliance validation (AC, API, NFRs)
- Code quality metrics (complexity, maintainability, duplication)
- Security scanning (OWASP Top 10)
- Deferral validation (MANDATORY - Step 2.5)

**When to use:** After story completion, before release

---

## QA Workflow (5 Phases)

Each phase loads its reference file on-demand for detailed implementation.

### Phase 1: Test Coverage Analysis
**Purpose:** Validate coverage against thresholds (95%/85%/80%)
**Reference:** `coverage-analysis-workflow.md`
**Guide:** `coverage-analysis.md` (thresholds and procedures)
**Steps:** 7 (load thresholds, generate reports, classify files, calculate by layer, validate, identify gaps, analyze quality)
**Output:** Coverage report, gap identification

### Phase 2: Anti-Pattern Detection
**Purpose:** Detect forbidden patterns and security issues
**Reference:** `anti-pattern-detection-workflow.md`
**Guides:** `anti-pattern-detection.md`, `security-scanning.md`
**Steps:** 4 (load context, detect patterns, run security scan, categorize violations)
**Output:** Anti-pattern violations by severity

### Phase 3: Spec Compliance Validation
**Purpose:** Validate implementation matches story specification
**Reference:** `spec-compliance-workflow.md`
**Guides:** `spec-validation.md`, `deferral-decision-tree.md`, `dod-protocol.md`
**Steps:** 6 (validate docs, load spec, validate AC, **VALIDATE DEFERRALS (2.5)**, validate API, validate NFRs, traceability)
**Subagent:** deferral-validator (Step 2.5 - MANDATORY)
**Output:** Spec compliance status, deferral validation results

**CRITICAL:** Step 2.5 deferral validation CANNOT be skipped. See dod-protocol.md.

### Phase 4: Code Quality Metrics
**Purpose:** Analyze code quality (complexity, maintainability, duplication, documentation)
**Reference:** `code-quality-workflow.md`
**Guide:** `quality-metrics.md`
**Steps:** 5 (complexity, maintainability, duplication, documentation, coupling)
**Output:** Quality metrics, violation identification

### Phase 5: QA Report Generation
**Purpose:** Aggregate results, generate report, invoke formatter
**Reference:** `report-generation.md`
**Guide:** `qa-result-formatting-guide.md`
**Steps:** 6 (aggregate, determine status, write report, update story, track history, invoke qa-result-interpreter)
**Subagent:** qa-result-interpreter (formats results for display)
**Output:** QA report file, story status updated, formatted display

**See individual phase reference files for complete workflow details.**

---

## Automation Scripts

**6 Python scripts** for automated quality analysis:
1. generate_coverage_report.py
2. detect_duplicates.py
3. analyze_complexity.py
4. security_scan.py
5. validate_spec_compliance.py
6. generate_test_stubs.py

**See `references/automation-scripts.md` for installation, usage, and integration patterns.**

---

## Subagent Coordination

**deferral-validator** (Phase 3 Step 2.5 - MANDATORY)
- Validates deferred DoD items
- Detects circular deferrals (CRITICAL)
- Validates justifications (HIGH if missing)
- Checks story/ADR references exist

**qa-result-interpreter** (Phase 5 Step 6)
- Parses QA report
- Generates display template (PASSED/FAILED/PARTIAL)
- Provides remediation guidance
- Respects framework constraints (see qa-result-formatting-guide.md)

---

## Integration Points

**Invoked by:**
- devforgeai-development (automatic light validation)
- `/qa` command (manual deep validation)
- devforgeai-orchestration (automated progression)

**Invokes:**
- deferral-validator subagent (Phase 3 Step 2.5)
- qa-result-interpreter subagent (Phase 5 Step 6)

**Provides output to:**
- devforgeai-development (QA failures trigger rework)
- devforgeai-release (QA approval required)
- User (formatted display via qa-result-interpreter)

---

## Success Criteria

### Light Validation Success
- [ ] Build passes
- [ ] All tests pass (100%)
- [ ] No CRITICAL violations
- [ ] Deferral validation passes

### Deep Validation Success
- [ ] Coverage meets thresholds (95%/85%/80%)
- [ ] No CRITICAL or HIGH violations
- [ ] Spec compliance validated
- [ ] Code quality acceptable
- [ ] Deferral validation passes
- [ ] Story status = "QA Approved"

---

## Reference Files

Load these on-demand during workflow execution:

### Workflow Files (8 files - NEW)
- **parameter-extraction.md** - Story ID and mode extraction
- **dod-protocol.md** - DoD adherence requirements (CRITICAL)
- **coverage-analysis-workflow.md** - Phase 1: 7-step coverage analysis
- **anti-pattern-detection-workflow.md** - Phase 2: 4-step pattern detection
- **spec-compliance-workflow.md** - Phase 3: 6-step spec validation (includes Step 2.5)
- **code-quality-workflow.md** - Phase 4: 5-step quality metrics
- **report-generation.md** - Phase 5: Report and formatter invocation
- **automation-scripts.md** - 6 Python scripts documentation

### Guide Files (9 files - existing)
- **coverage-analysis.md** - Thresholds and procedures
- **anti-pattern-detection.md** - Detection patterns
- **deferral-decision-tree.md** - Deferral validation logic
- **language-specific-tooling.md** - Test execution tools
- **qa-result-formatting-guide.md** - qa-result-interpreter guardrails
- **quality-metrics.md** - Metric thresholds
- **security-scanning.md** - OWASP Top 10 checks
- **spec-validation.md** - Validation procedures
- **validation-procedures.md** - General procedures

---

## Token Budget Management

**Light mode:** ~10K tokens (entry + Phases 1-2)
**Deep mode:** ~65K tokens (entry + Phases 1-5)

**Progressive loading ensures only necessary validation executed.**

EOF
```

**Validation:**
- [ ] New file created: `SKILL.md.new`
- [ ] Line count ≤200 lines
- [ ] All 5 phases summarized
- [ ] DoD protocol highlighted
- [ ] References to all 17 files

#### Step 3.2: Validate Line Count

```bash
wc -l SKILL.md.new
# Must be ≤200 lines
```

**If over 200:**
- Condense Validation Modes section
- Reduce Automation Scripts note
- Minimize Integration Points

**Validation:**
- [ ] Line count ≤200 lines

#### Step 3.3: Replace Original SKILL.md

```bash
mv SKILL.md.new SKILL.md
```

**Validation:**
- [ ] SKILL.md replaced
- [ ] Backup preserved

---

### Phase 4: Testing

#### Step 4.1: Cold Start Test

```bash
wc -l .claude/skills/devforgeai-qa/SKILL.md
# Must be ≤200 lines
```

**Validation:**
- [ ] SKILL.md ≤200 lines
- [ ] Activation time <100ms

#### Step 4.2: Mode Tests

**Test Case 1: Light Validation**
```
Invoke skill in light mode

Expected:
1. Mode: Light detected
2. Phases 1-2 executed only
3. References loaded: coverage-analysis-workflow.md, anti-pattern-detection-workflow.md
4. Step 2.5 deferral validation STILL EXECUTES (mandatory)
5. Token usage ~10K
```

**Validation:**
- [ ] Light mode executes
- [ ] Only Phases 1-2 run
- [ ] Step 2.5 not skipped
- [ ] Token usage ~10K

**Test Case 2: Deep Validation**
```
Invoke skill in deep mode

Expected:
1. Mode: Deep detected
2. Phases 1-5 executed
3. All workflow references loaded progressively
4. deferral-validator subagent invoked (Phase 3)
5. qa-result-interpreter subagent invoked (Phase 5)
6. Token usage ~65K (isolated context)
```

**Validation:**
- [ ] Deep mode executes
- [ ] All 5 phases run
- [ ] Both subagents invoked
- [ ] Token usage ~65K

#### Step 4.3: Deferral Validation Test (CRITICAL)

**Test Case 3: Story with Deferred Items**
```
Story has deferred DoD items

Expected:
1. Phase 3 Step 2.5 executes
2. deferral-validator subagent invoked
3. Validation checks:
   - User approval markers present
   - Story/ADR references exist
   - Technical justification present
4. If violations: QA status = FAILED
```

**Validation:**
- [ ] Step 2.5 executes
- [ ] deferral-validator invoked
- [ ] Violations detected correctly
- [ ] QA fails on CRITICAL/HIGH

**Test Case 4: Story with No Deferrals**
```
Story has all DoD items complete

Expected:
1. Phase 3 Step 2.5 executes
2. deferral-validator invoked
3. Validation: No deferrals found
4. Step 2.5 passes quickly
```

**Validation:**
- [ ] Step 2.5 still executes (not skipped)
- [ ] Passes when no deferrals
- [ ] No false positives

#### Step 4.4: Integration Test

**Test:** Complete QA validation workflow

```
Input: Story with implementation complete

Expected:
1. Mode determined (light or deep)
2. All applicable phases execute
3. References load progressively
4. Subagents invoked as needed
5. Report generated
6. Story status updated
7. Formatted display returned

Output:
- QA report in .devforgeai/qa/reports/
- Story status: "QA Approved" or "QA Failed"
- Formatted display (from qa-result-interpreter)
```

**Validation:**
- [ ] Full workflow completes
- [ ] Both modes tested
- [ ] Reports generated
- [ ] Story updated

#### Step 4.5: Regression Test

**Test:** Behavior unchanged from original

**Validation:**
- [ ] Same validation rigor
- [ ] Same thresholds enforced
- [ ] Same deferral detection
- [ ] Same report quality

#### Step 4.6: Token Measurement

```bash
# Measure activation token usage
# Original: ~10,640 tokens
# Target: ~1,520 tokens (7x improvement)

# Measure mode-specific usage
# Light mode: ~3,840 tokens (entry + Phases 1-2)
# Deep mode: ~11,120 tokens (entry + Phases 1-5)
```

**Validation:**
- [ ] Activation: ≥6x improvement
- [ ] Light mode: ~3,840 tokens
- [ ] Deep mode: ~11,120 tokens (progressive, not all at once)

---

### Phase 5: Documentation and Completion

#### Step 5.1: Update This Document

**Mark completion:**
- [ ] Status: COMPLETE
- [ ] Final line count: [actual]
- [ ] Token reduction: [actual %]
- [ ] Completion date: [date]

#### Step 5.2: Commit Changes

```bash
cd /mnt/c/Projects/DevForgeAI2

git add .claude/skills/devforgeai-qa/

git commit -m "refactor(qa): Progressive disclosure - 1330→190 lines

- Reduced SKILL.md from 1,330 to ~190 lines (86% reduction)
- Created 8 new reference files for 5-phase workflow
- Separated DoD protocol into dedicated reference (CRITICAL)
- Organized 17 reference files total
- Token efficiency: 7x improvement (10.6K→1.5K on activation)
- Light mode: 3.8K tokens, Deep mode: 11.1K tokens (progressive)
- All functionality preserved, Step 2.5 deferral validation MANDATORY

Key extractions:
- Phase 3 spec compliance (349 lines → spec-compliance-workflow.md)
- Phase 5 report generation (231 lines → report-generation.md)
- DoD protocol (64 lines → dod-protocol.md) - CRITICAL rules

Addresses: Reddit article cold start optimization
Pattern: Progressive disclosure per Anthropic architecture
Testing: Both modes validated, deferral validation mandatory"
```

**Validation:**
- [ ] Changes committed
- [ ] DoD protocol emphasis in message

#### Step 5.3: Update Framework Memory (After Parallel Sessions Complete)

**⚠️ IMPORTANT:** Use AskUserQuestion before updating shared files.

**Files to update:**
- `.claude/memory/skills-reference.md`
- `.claude/memory/qa-automation.md`
- `.claude/memory/commands-reference.md` (update /qa)

**Validation:**
- [ ] User confirmed no conflicts
- [ ] Shared files updated

---

## Completion Criteria

**All must be TRUE before marking COMPLETE:**

- [ ] SKILL.md ≤200 lines
- [ ] All 8 new reference files created
- [ ] 17 reference files total (8 new + 9 existing)
- [ ] Cold start test passes (<200 lines loaded)
- [ ] Mode tests pass (light and deep)
- [ ] Deferral validation test passes (CRITICAL)
- [ ] Phase execution tests pass (all 5 phases)
- [ ] Integration test passes (complete workflow)
- [ ] Regression test passes (behavior unchanged)
- [ ] Token efficiency ≥6x improvement
- [ ] Light mode ~3.8K tokens
- [ ] Deep mode ~11K tokens (progressive)
- [ ] Changes committed to git
- [ ] This document updated with results

---

## Session Handoff Notes

**For next Claude session picking up this work:**

### Quick Start

1. **Read this document completely**
2. **Check status** - Resume from unchecked items
3. **Create backup first**
4. **Extract Phase 3 first** - Largest (349 lines, includes deferral validation)
5. **Preserve Step 2.5** - CANNOT be skipped or made optional
6. **Test both modes** - Light and deep have different phase coverage
7. **Update checkboxes** - Track progress

### Critical Reminders

- **Phase 3 is massive** - 349 lines (26% of skill), extract to spec-compliance-workflow.md
- **Step 2.5 is MANDATORY** - Deferral validation cannot be skipped (see dod-protocol.md)
- **Two validation modes** - Light (Phases 1-2) and Deep (Phases 1-5) load different references
- **Two subagents** - deferral-validator (Phase 3), qa-result-interpreter (Phase 5)
- **DoD protocol critical** - Extract to separate file, highlight in entry point
- **Shared files** - Use AskUserQuestion before updating .claude/memory/*.md

### Common Pitfalls

1. **Don't make Step 2.5 optional** - Deferral validation is MANDATORY in both modes
2. **Don't lose mode distinction** - Light vs deep affects which phases execute
3. **Don't skip automation scripts** - 6 Python scripts are part of deep validation
4. **Preserve qa-result-interpreter** - Phase 5 Step 6 invocation critical
5. **Test deferral detection** - Must catch autonomous deferrals (RCA-006)

### If Stuck

1. **Review spec-compliance-workflow.md extraction** - Largest, most complex
2. **Check deferral-decision-tree.md** - Already exists, workflow references it
3. **Review qa-result-formatting-guide.md** - Pattern for subagent integration
4. **Test with deferred story** - Validate Step 2.5 works correctly

### Success Indicators

- ✅ SKILL.md opens instantly
- ✅ Light mode loads Phases 1-2 only
- ✅ Deep mode loads all phases progressively
- ✅ Step 2.5 executes in both modes
- ✅ Token usage: Light ~3.8K, Deep ~11K

---

## Results (Post-Completion)

**To be filled in after refactoring completes:**

### Metrics Achieved

- **Final SKILL.md lines:** [X] (Target: ≤200)
- **Reference files created:** [N] (Target: 8 new + 9 existing = 17 total)
- **Token reduction:** [Y]% (Target: ≥85%)
- **Activation time:** [Z]ms (Target: <100ms)
- **Light mode tokens:** [L] (Target: ~3.8K)
- **Deep mode tokens:** [D] (Target: ~11K)
- **Efficiency gain:** [R]x (Target: ≥6x)

### Files Modified

- `.claude/skills/devforgeai-qa/SKILL.md` (1,330 → [X] lines)
- `.claude/skills/devforgeai-qa/references/` (9 → 17 files)
  - Created: [list 8 new files]

### Lessons Learned

[Notes for future skill refactorings]

---

## Appendix: Line Count Breakdown

**Original SKILL.md (1,330 lines):**

| Section | Lines | % | Extraction Target |
|---------|-------|---|-------------------|
| Frontmatter | 12 | 0.9% | Keep |
| Parameter Extraction | 86 | 6.5% | → parameter-extraction.md |
| DoD Protocol | 64 | 4.8% | → dod-protocol.md |
| Purpose/When | 25 | 1.9% | Keep |
| Modes | 51 | 3.8% | Keep (condense to 30) |
| Phase 1: Coverage | 104 | 7.8% | → coverage-analysis-workflow.md |
| Phase 2: Anti-Patterns | 116 | 8.7% | → anti-pattern-detection-workflow.md |
| Phase 3: Spec | 349 | 26.2% | → spec-compliance-workflow.md |
| Phase 4: Quality | 91 | 6.8% | → code-quality-workflow.md |
| Phase 5: Report | 231 | 17.4% | → report-generation.md |
| Automation Scripts | 125 | 9.4% | → automation-scripts.md |
| Success Criteria | 21 | 1.6% | Keep (condense to 15) |
| Reference List | 26 | 2.0% | Keep (update) |
| Token Budget | 16 | 1.2% | Keep (condense to 10) |
| **TOTAL** | **1,330** | **100%** | **17 references** |

**Target SKILL.md (~190 lines):**

| Section | Lines | % |
|---------|-------|---|
| Frontmatter | 12 | 6.3% |
| Parameter Note | 10 | 5.3% |
| DoD Protocol Note | 15 | 7.9% |
| Purpose/When | 25 | 13.2% |
| Modes | 30 | 15.8% |
| 5-Phase Summary | 45 | 23.7% |
| Automation Note | 10 | 5.3% |
| Subagents | 15 | 7.9% |
| Integration | 15 | 7.9% |
| Success Criteria | 15 | 7.9% |
| Reference Map | 20 | 10.5% |
| Token Note | 10 | 5.3% |
| **TOTAL** | **~190** | **~100%** |

---

**Document Version:** 1.0
**Created:** 2025-01-06
**Last Updated:** 2025-01-06 (Initial creation)
**Next Review:** After refactoring completion
