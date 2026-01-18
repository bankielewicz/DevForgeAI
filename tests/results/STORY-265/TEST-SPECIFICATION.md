# Test Specification: STORY-265 QA Reference Consolidation

**Story Type:** Refactor (Documentation/Markdown)
**Output Type:** Test Specification Document (non-executable)
**Generated:** 2026-01-17

---

## Baseline Measurement Tests

### BL-001: Reference File Count Baseline
- **Verify:** Count files in `.claude/skills/devforgeai-qa/references/`
- **Expected:** 26 files (current baseline)
- **Method:** `Glob(pattern="*.md", path=".claude/skills/devforgeai-qa/references/")`

### BL-002: Token Estimate Baseline
- **Verify:** Estimate tokens per file using word count * 1.3 factor
- **Expected:** Total ~15K-20K tokens across all reference files
- **Method:** `wc -w` on each file, multiply by 1.3, sum totals
- **Accuracy:** ±10% (per COMP-003)

### BL-003: deep-validation-workflow.md Pattern Baseline
- **Verify:** Existing consolidated file structure documented
- **Expected:** 886 lines, ~3.5K token savings documented in file header
- **Method:** Read file, verify "Token savings" header present

---

## Consolidation Candidate Tests

### CC-001: Minimum Candidates Identified (AC#1)
- **Verify:** ≥3 consolidation candidate pairs identified
- **Expected:** Pairs like coverage-analysis + coverage-analysis-workflow, anti-pattern-detection + anti-pattern-detection-workflow
- **Method:** Check for files with matching base names (X.md + X-workflow.md pattern)

### CC-002: Redundancy Detection
- **Verify:** Related files share overlapping content sections
- **Expected:** Workflow files contain procedural steps for their paired concept files
- **Method:** Grep for shared section headers between candidate pairs

### CC-003: Phase Usage Mapping (COMP-001)
- **Verify:** Reference files mapped to QA phases that load them
- **Expected:** Each reference file shows which phase(s) invoke Read() for it
- **Method:** Grep SKILL.md and phase files for Read() calls to reference files

---

## Pattern Extraction Tests

### PE-001: Consolidation Pattern Documented (AC#2)
- **Verify:** deep-validation-workflow.md pattern is extracted and reusable
- **Expected:** Pattern includes: Overview section, Token savings header, Phase grouping, Step numbering
- **Method:** Verify consolidated files follow same structural template

### PE-002: Progressive Disclosure Structure (BR-001)
- **Verify:** Overview appears before detailed steps
- **Expected:** `## Overview` section within first 30 lines, detailed phases follow
- **Method:** Check line position of Overview vs Phase sections

---

## Token Savings Tests

### TS-001: Target Savings Achieved (BR-003, NFR-001)
- **Verify:** ≥5K token reduction after consolidation
- **Expected:** Baseline - Post-consolidation ≥ 5000 tokens
- **Method:** Compare pre/post word counts * 1.3 factor

### TS-002: File Count Reduction
- **Verify:** 3-5 fewer reference files after consolidation
- **Expected:** Post-consolidation count: 21-23 files (from 26)
- **Method:** Count files before/after

---

## Structure Validation Tests

### SV-001: Anchor References Replace Cross-File Links (BR-002)
- **Verify:** No external file references within consolidated content
- **Expected:** Links use `#section-anchor` format, not `other-file.md`
- **Method:** Grep for `.md)` patterns in consolidated files; should be zero

### SV-002: TOC Accuracy (NFR-002)
- **Verify:** Table of Contents maps to actual sections
- **Expected:** Every TOC entry has matching `##` or `###` header
- **Method:** Extract TOC links, verify each anchor exists

### SV-003: File Size Limit (NFR-002)
- **Verify:** No consolidated file exceeds 5000 lines
- **Expected:** Max lines per file < 5000
- **Method:** `wc -l` on consolidated files

---

## SKILL.md Reference Tests

### SR-001: References Updated (AC#5)
- **Verify:** SKILL.md Read() calls point to consolidated locations
- **Expected:** No Read() calls to deleted/merged files
- **Method:** Grep SKILL.md for Read() patterns, verify targets exist

### SR-002: No Broken References
- **Verify:** All referenced files exist after consolidation
- **Expected:** Zero 404s when following SKILL.md references
- **Method:** Extract all file paths from Read() calls, verify each exists

---

## Functionality Preservation Tests

### FP-001: QA Skill Execution Unchanged (NFR-003)
- **Verify:** QA skill phases complete successfully post-consolidation
- **Expected:** Same validation output, same phase sequence
- **Method:** Run `/qa STORY-XXX` on test story, compare output structure

### FP-002: Phase Content Complete
- **Verify:** All original reference content accessible in consolidated files
- **Expected:** No workflow steps lost during merge
- **Method:** Diff original files against consolidated sections

---

## Validation Checklist Summary

| Test ID | Requirement | Priority |
|---------|-------------|----------|
| BL-001 | Baseline file count | High |
| CC-001 | ≥3 candidates (AC#1) | High |
| PE-001 | Pattern documented (AC#2) | High |
| TS-001 | ≥5K savings (BR-003) | High |
| SV-001 | Anchors replace links (BR-002) | High |
| SR-001 | SKILL.md updated (AC#5) | High |
| FP-001 | Behavior unchanged (NFR-003) | Critical |
