---
id: STORY-500
title: Add C++ Coverage Support to QA Workflow via OpenCppCoverage
type: feature
epic: EPIC-002
sprint: Sprint-3
status: QA Approved
points: 3
depends_on: []
priority: Medium
advisory: false
source_gap: null
source_story: null
assigned_to: Solo Developer
created: 2026-02-25
format_version: "2.9"
---

# Story: Add C++ Coverage Support to QA Workflow via OpenCppCoverage

## Description

**As a** developer working on C++ native components,
**I want** the QA coverage analysis pipeline to support C++ via OpenCppCoverage,
**so that** C++ stories receive instrumented line-level coverage data instead of silent no-data fallthrough.

## Acceptance Criteria

### XML Acceptance Criteria Format

### AC#1: Add C++ Branch to Coverage Step 2 in All 3 Workflow Files

```xml
<acceptance_criteria id="AC1" implements="CFG-001,CFG-002,CFG-003">
  <given>The QA coverage Step 2 supports 6 languages (.NET, Python, Node.js, Go, Rust, Java) but not C++</given>
  <when>A C++ project is detected (CMakeLists.txt present) during QA deep validation</when>
  <then>An `IF language == "C++":` branch executes OpenCppCoverage with --sources, --modules, --export_type cobertura flags, builds Debug config, and outputs Cobertura XML to the story-scoped coverage directory. The branch is added consistently across all 3 copies of the coverage workflow (coverage-analysis-workflow.md, deep-validation-workflow.md, coverage-analysis.md).</then>
  <verification>
    <source_files>
      <file hint="Primary coverage workflow">.claude/skills/devforgeai-qa/references/coverage-analysis-workflow.md</file>
      <file hint="Deep validation consolidated">.claude/skills/devforgeai-qa/references/deep-validation-workflow.md</file>
      <file hint="Coverage analysis guide">.claude/skills/devforgeai-qa/references/coverage-analysis.md</file>
    </source_files>
    <test_file>native/tests/test_address_cache.cpp</test_file>
    <coverage_threshold>95</coverage_threshold>
  </verification>
</acceptance_criteria>
```

---

### AC#2: Add C++ Section to Language-Specific Tooling Reference

```xml
<acceptance_criteria id="AC2" implements="CFG-004">
  <given>language-specific-tooling.md documents testing, coverage, linting, and parsing for 6 languages but not C++</given>
  <when>The upgrade is applied</when>
  <then>A complete C++ section is added (after Rust, before Quick Reference Matrix) covering: OpenCppCoverage invocation syntax with --sources/--modules/--export_type flags, Debug build requirement, Cobertura XML output format (identical to .NET — reuses existing parsing logic), story-scoped command variant, and the Quick Reference Matrix table includes a C++ row</then>
  <verification>
    <source_files>
      <file hint="Language tooling reference">.claude/skills/devforgeai-qa/references/language-specific-tooling.md</file>
    </source_files>
    <test_file>native/tests/test_address_cache.cpp</test_file>
  </verification>
</acceptance_criteria>
```

---

### AC#3: Add C++ Entry to Language Smoke Tests Configuration

```xml
<acceptance_criteria id="AC3" implements="CFG-005">
  <given>language-smoke-tests.yaml defines runtime smoke test configurations for 6 languages but not C++</given>
  <when>The upgrade is applied</when>
  <then>A `cpp:` entry is added following the extensibility pattern documented in deep-validation-workflow.md, with detection_pattern "C++17", entry_point_source "CMakeLists.txt", appropriate smoke_test_command for native test executables, timeout_seconds, and remediation_guidance</then>
  <verification>
    <source_files>
      <file hint="Smoke test config">.claude/skills/devforgeai-qa/assets/language-smoke-tests.yaml</file>
    </source_files>
    <test_file>native/tests/test_address_cache.cpp</test_file>
  </verification>
</acceptance_criteria>
```

---

### AC#4: Backward Compatibility — Existing 6 Language Branches Unchanged

```xml
<acceptance_criteria id="AC4" implements="BR-001">
  <given>The QA coverage pipeline currently works for .NET, Python, Node.js, Go, Rust, and Java projects</given>
  <when>The C++ branch is added</when>
  <then>All existing language branches remain byte-identical (no modifications to existing IF blocks). The C++ branch is added as an additional ELIF/IF after the Java branch. A non-C++ project (e.g., Rust-only) produces identical QA behavior before and after this change.</then>
  <verification>
    <source_files>
      <file hint="Coverage workflow">.claude/skills/devforgeai-qa/references/coverage-analysis-workflow.md</file>
      <file hint="Deep validation">.claude/skills/devforgeai-qa/references/deep-validation-workflow.md</file>
      <file hint="Coverage analysis">.claude/skills/devforgeai-qa/references/coverage-analysis.md</file>
    </source_files>
    <test_file>native/tests/test_address_cache.cpp</test_file>
  </verification>
</acceptance_criteria>
```

---

### Source Files Guidance

- `.claude/skills/devforgeai-qa/references/coverage-analysis-workflow.md` — Step 2 IF-chain (add C++ after Java, line 72)
- `.claude/skills/devforgeai-qa/references/deep-validation-workflow.md` — Step 2 table (add C++ row, line 48) and detection pattern (add C++ to grep, line 169)
- `.claude/skills/devforgeai-qa/references/coverage-analysis.md` — Step 2 IF-chain (add C++ after Java, line 59)
- `.claude/skills/devforgeai-qa/references/language-specific-tooling.md` — New C++ section (after Rust section ending at line 1020) + Quick Reference Matrix row (line 1032)
- `.claude/skills/devforgeai-qa/assets/language-smoke-tests.yaml` — New `cpp:` entry following extensibility pattern

## Technical Specification

```yaml
technical_specification:
  format_version: "2.0"

  components:
    - type: "Configuration"
      name: "CoverageWorkflowCppBranch"
      file_path: ".claude/skills/devforgeai-qa/references/coverage-analysis-workflow.md"
      requirements:
        - id: "CFG-001"
          description: "Add IF language == C++ branch to Step 2 with OpenCppCoverage command using --sources, --modules, --export_type cobertura flags and Debug build config"
          testable: true
          test_requirement: "Test: Grep for 'C++' in coverage-analysis-workflow.md returns the new branch with OpenCppCoverage command"
          priority: "High"

    - type: "Configuration"
      name: "DeepValidationCppBranch"
      file_path: ".claude/skills/devforgeai-qa/references/deep-validation-workflow.md"
      requirements:
        - id: "CFG-002"
          description: "Add C++ row to Step 2 coverage command table and extend language detection grep pattern from 6 to 7 languages"
          testable: true
          test_requirement: "Test: Grep for 'C++' in deep-validation-workflow.md returns both Step 2 table row and detection pattern"
          priority: "High"

    - type: "Configuration"
      name: "CoverageAnalysisCppBranch"
      file_path: ".claude/skills/devforgeai-qa/references/coverage-analysis.md"
      requirements:
        - id: "CFG-003"
          description: "Add IF language == C++ branch to Step 2 matching the branch in coverage-analysis-workflow.md"
          testable: true
          test_requirement: "Test: Grep for 'C++' in coverage-analysis.md returns the new branch matching CFG-001"
          priority: "High"

    - type: "Configuration"
      name: "LanguageToolingCppSection"
      file_path: ".claude/skills/devforgeai-qa/references/language-specific-tooling.md"
      requirements:
        - id: "CFG-004"
          description: "Add complete C++ section covering: OpenCppCoverage CLI syntax, Debug build requirement, --sources/--modules/--export_type flags, Cobertura XML format (reuses .NET parsing), story-scoped command table row, Quick Reference Matrix row"
          testable: true
          test_requirement: "Test: Grep for 'OpenCppCoverage' in language-specific-tooling.md returns section with all required subsections"
          priority: "High"

    - type: "Configuration"
      name: "SmokeTestCppEntry"
      file_path: ".claude/skills/devforgeai-qa/assets/language-smoke-tests.yaml"
      requirements:
        - id: "CFG-005"
          description: "Add cpp: entry with detection_pattern, entry_point_source (CMakeLists.txt), smoke_test_command for native test executables, timeout_seconds, and remediation_guidance"
          testable: true
          test_requirement: "Test: Grep for 'cpp:' in language-smoke-tests.yaml returns entry with all required fields"
          priority: "Medium"

  business_rules:
    - id: "BR-001"
      rule: "Existing 6 language branches must remain byte-identical after C++ addition"
      trigger: "Any modification to coverage-analysis-workflow.md, deep-validation-workflow.md, or coverage-analysis.md"
      validation: "Diff existing IF blocks before/after — zero changes to .NET, Python, Node.js, Go, Rust, Java branches"
      error_handling: "If existing branch modified, revert and use additive-only approach"
      test_requirement: "Test: Git diff shows only additions (new C++ branch), no modifications to existing branches"
      priority: "Critical"
    - id: "BR-002"
      rule: "OpenCppCoverage requires Debug build configuration (MSVC PDB symbols). Coverage command must explicitly build or reference Debug config, never Release."
      trigger: "C++ coverage command execution"
      validation: "Command includes --config Debug or targets Debug build output directory"
      error_handling: "If Release build attempted, OpenCppCoverage produces empty Cobertura XML (0 lines covered)"
      test_requirement: "Test: Coverage command string contains 'Debug' config reference"
      priority: "High"

  non_functional_requirements:
    - id: "NFR-001"
      category: "Performance"
      requirement: "C++ coverage command completes within 60 seconds for projects with up to 50 source files"
      metric: "< 60 seconds wall clock time"
      test_requirement: "Test: OpenCppCoverage on GPUXtend native/hook sources completes within 60s"
      priority: "Medium"
```

## Technical Limitations

```yaml
technical_limitations:
  - id: TL-001
    component: "OpenCppCoverage"
    limitation: "Requires Windows (MSVC Debug API). Not available on Linux/macOS."
    decision: "workaround:acceptable — C++ coverage only runs on Windows hosts where OpenCppCoverage is installed. Non-Windows CI skips C++ coverage gracefully."
    discovered_phase: "Architecture"
    impact: "C++ coverage analysis unavailable in Linux-only CI environments"
  - id: TL-002
    component: "OpenCppCoverage"
    limitation: "Requires Debug build. Release builds strip PDB symbols needed for line mapping."
    decision: "workaround:acceptable — coverage command explicitly builds Debug config. Production artifacts still use Release."
    discovered_phase: "Development"
    impact: "Coverage run builds Debug config separately from Release artifacts"
  - id: TL-003
    component: "OpenCppCoverage"
    limitation: "--modules flag is mandatory. Without it, no modules are selected and report is empty."
    decision: "workaround:documented — coverage command always includes --modules pointing to Debug output directory"
    discovered_phase: "Development"
    impact: "None if --modules is always specified in the command template"
```

## Non-Functional Requirements (NFRs)

### Performance

**Response Time:**
- OpenCppCoverage with 5 source files: < 15 seconds
- OpenCppCoverage with 50 source files: < 60 seconds

**Performance Test:**
- Run OpenCppCoverage on native/hook sources and measure wall clock time

---

### Security

- No change to security posture (coverage tool reads source, does not modify it)

---

### Scalability

- Supports projects with 100+ C++ source files (OpenCppCoverage handles large codebases)

---

### Reliability

- If OpenCppCoverage is not installed, the coverage step should fall through gracefully (same behavior as today — no coverage data, structural analysis fallback)

---

### Observability

- Display "C++ detected — using OpenCppCoverage" message during QA Phase 1 Step 2

---

## Dependencies

### Prerequisite Stories

- None (C++ coverage is independent of other stories)

### External Dependencies

- **OpenCppCoverage:** Must be installed on the developer's machine. Available via Chocolatey: `choco install opencppcoverage`. Not bundled with the framework.

### Technology Dependencies

- **OpenCppCoverage 0.9.9+** — Windows-only MSVC coverage tool. Installed via Chocolatey. Outputs Cobertura XML.

---

## Test Strategy

### Unit Tests

**Coverage Target:** 95%+

**Test Scenarios:**
1. **Happy Path:** Grep each of the 3 workflow files for `C++` and verify the OpenCppCoverage command is present with correct flags (--sources, --modules, --export_type cobertura, Debug config)
2. **Consistency:** Verify the C++ command in all 3 workflow files uses identical flag patterns
3. **Edge Cases:**
   - language-specific-tooling.md Quick Reference Matrix has exactly 7 rows (6 existing + 1 C++)
   - language-smoke-tests.yaml has a `cpp:` entry with all required fields
4. **Error Cases:**
   - Existing .NET/Python/Node.js/Go/Rust/Java branches are byte-identical before and after (git diff shows additions only)

---

### Integration Tests

**Coverage Target:** 85%+

**Test Scenarios:**
1. **End-to-end:** Run OpenCppCoverage with the documented command on native/build/tests/Debug/test_address_cache.exe and verify Cobertura XML output contains non-zero lines-covered
2. **Cobertura parsing:** Parse the generated coverage.xml using the same strategy documented for .NET and verify line-rate is extractable

---

## Acceptance Criteria Verification Checklist

### AC#1: Add C++ Branch to Coverage Step 2 in All 3 Workflow Files

- [ ] coverage-analysis-workflow.md has C++ IF branch after Java - **Phase:** 3 - **Evidence:** grep output
- [ ] deep-validation-workflow.md has C++ row in Step 2 table - **Phase:** 3 - **Evidence:** grep output
- [ ] coverage-analysis.md has C++ IF branch after Java - **Phase:** 3 - **Evidence:** grep output
- [ ] All 3 branches use identical OpenCppCoverage command pattern - **Phase:** 3 - **Evidence:** diff comparison

### AC#2: Add C++ Section to Language-Specific Tooling Reference

- [ ] C++ section exists in language-specific-tooling.md after Rust - **Phase:** 3 - **Evidence:** grep output
- [ ] Section covers: OpenCppCoverage CLI, Debug requirement, flags, Cobertura format, story-scoped commands - **Phase:** 3 - **Evidence:** section content
- [ ] Quick Reference Matrix has 7 rows - **Phase:** 3 - **Evidence:** table row count
- [ ] Story-Scoped Coverage Commands table has 7 rows - **Phase:** 3 - **Evidence:** table row count

### AC#3: Add C++ Entry to Language Smoke Tests Configuration

- [ ] language-smoke-tests.yaml has cpp: entry - **Phase:** 3 - **Evidence:** grep output
- [ ] Entry has detection_pattern, entry_point_source, smoke_test_command, timeout_seconds, remediation_guidance - **Phase:** 3 - **Evidence:** yaml content

### AC#4: Backward Compatibility

- [ ] Git diff shows zero modifications to existing 6 language branches - **Phase:** 3 - **Evidence:** git diff --stat

---

**Checklist Progress:** 0/12 items complete (0%)

---

<!-- IMPORTANT: Definition of Done items MUST be directly under ## Definition of Done as flat checkboxes. Do NOT nest under ### subsections or pre-commit validation will fail. -->

## Definition of Done

- [x] C++ IF branch added to coverage-analysis-workflow.md Step 2
- [x] C++ row added to deep-validation-workflow.md Step 2 table
- [x] C++ detection pattern added to deep-validation-workflow.md language grep (line 169)
- [x] C++ IF branch added to coverage-analysis.md Step 2
- [x] C++ section added to language-specific-tooling.md (after Rust)
- [x] Quick Reference Matrix updated with C++ row in language-specific-tooling.md
- [x] Story-Scoped Coverage Commands table updated with C++ row
- [x] cpp: entry added to language-smoke-tests.yaml
- [x] All 4 acceptance criteria have passing verification
- [x] Zero modifications to existing 6 language branches (backward compatible)
- [x] OpenCppCoverage command includes --sources, --modules, --export_type cobertura, and Debug config
- [x] OpenCppCoverage command validated end-to-end on native/hook sources (produces non-empty Cobertura XML)
- [x] Cobertura XML parseable using existing .NET parsing strategy (xmllint xpath)
- [x] All 3 workflow file C++ branches are consistent (identical flag patterns)
- [x] C++ coverage workflow documented in language-specific-tooling.md
- [x] Debug build requirement documented with rationale
- [x] --modules flag requirement documented (empty report without it)

### TDD Workflow Summary

| Phase | Status | Details |
|-------|--------|---------|
| Red (02) | ✅ Complete | 44 tests written (24 failing, 20 passing baseline) |
| Green (03) | ✅ Complete | All 44 tests passing |
| Refactor (04) | ✅ Complete | No refactoring needed (config-only) |

### Files Created/Modified

| File | Action | Lines |
|------|--------|-------|
| src/claude/skills/devforgeai-qa/references/coverage-analysis-workflow.md | Modified | +5 |
| src/claude/skills/devforgeai-qa/references/deep-validation-workflow.md | Modified | +2 |
| src/claude/skills/devforgeai-qa/references/coverage-analysis.md | Modified | +5 |
| src/claude/skills/devforgeai-qa/references/language-specific-tooling.md | Modified | +75 |
| src/claude/skills/devforgeai-qa/assets/language-smoke-tests.yaml | Modified | +12 |
| tests/test_story_500_cpp_coverage.py | Created | 343 |

---

## Implementation Notes

**Developer:** DevForgeAI AI Agent
**Implemented:** 2026-02-26

- [x] C++ IF branch added to coverage-analysis-workflow.md Step 2 - Completed: Added C++ branch after Java with OpenCppCoverage command using --sources, --modules, --export_type cobertura flags and Debug config
- [x] C++ row added to deep-validation-workflow.md Step 2 table - Completed: Added C++ coverage command row and updated detection grep pattern to include C++
- [x] C++ IF branch added to coverage-analysis.md Step 2 - Completed: Added identical C++ branch matching coverage-analysis-workflow.md
- [x] C++ section added to language-specific-tooling.md (after Rust) - Completed: Full section with GoogleTest, OpenCppCoverage, parsing strategy, WSL usage, and Cobertura XML documentation
- [x] Quick Reference Matrix updated with C++ row - Completed: 7 language rows in matrix
- [x] Story-Scoped Coverage Commands table updated with C++ row - Completed: 7 language rows in story-scoped table
- [x] cpp: entry added to language-smoke-tests.yaml - Completed: C++17 detection, CMakeLists.txt entry point, 15s timeout, remediation guidance
- [x] All 4 acceptance criteria have passing verification - Completed: AC compliance verifier confirmed all 4 ACs pass
- [x] Zero modifications to existing 6 language branches - Completed: Additive-only changes, backward compatible
- [x] OpenCppCoverage command includes all required flags and Debug config - Completed: Consistent across all 3 workflow files
- [x] All 3 workflow file C++ branches are consistent - Completed: Identical flag patterns verified by test
- [x] C++ coverage workflow documented in language-specific-tooling.md - Completed: Complete section with Debug requirement and --modules flag rationale
- [x] Debug build requirement documented with rationale - Completed: Release strips PDB symbols
- [x] --modules flag requirement documented - Completed: Empty report without it
- [x] OpenCppCoverage command validated end-to-end - Completed: Validated in STORY-012 session (45/45 lines covered)
- [x] Cobertura XML parseable using .NET strategy - Completed: Identical schema documented
- [x] All unit tests pass (44/44) - Completed: pytest tests/test_story_500_cpp_coverage.py
- [x] C++ detection pattern added to deep-validation-workflow.md language grep (line 169) - Completed: Updated grep pattern to include C++ alongside existing 6 languages
- [x] OpenCppCoverage command includes --sources, --modules, --export_type cobertura, and Debug config - Completed: All flags present in C++ branch across all 3 workflow files
- [x] Cobertura XML parseable using existing .NET parsing strategy (xmllint xpath) - Completed: Identical Cobertura XML schema documented in language-specific-tooling.md

**Validated OpenCppCoverage Command (from STORY-012 session):**

```bash
# Working command (validated 2026-02-25 on Windows 11 + RTX 5070):
"/mnt/c/Program Files/OpenCppCoverage/OpenCppCoverage.exe" \
  --sources "C:\Projects\GPUXtend\native\hook" \
  --modules "C:\Projects\GPUXtend\native\build\tests\Debug" \
  --export_type "cobertura:C:\Projects\GPUXtend\coverage.xml" \
  -- "C:\Projects\GPUXtend\native\build\tests\Debug\test_address_cache.exe"

# Result: 45/45 lines covered (100%), Cobertura XML generated successfully
# Key: Must use Debug build (Release strips PDB symbols)
# Key: --modules flag is REQUIRED (without it, report is empty)
# Key: Runs from WSL directly via /mnt/c/ path (no cmd.exe wrapper needed)
```

**Generic Command Template (for story-scoped workflow):**

```
IF language == "C++":
    # Build Debug config for coverage instrumentation
    Bash(command="cmake --build {native_build_dir} --config Debug")
    # Run OpenCppCoverage with Cobertura XML output
    Bash(command="OpenCppCoverage --sources {source_dir} --modules {debug_build_dir} --export_type cobertura:{coverage_dir}/coverage.cobertura.xml -- {test_executable}")
    coverage_file = "{coverage_dir}/coverage.cobertura.xml"
```

**Cobertura XML Output (validated):**

```xml
<coverage line-rate="1" lines-covered="45" lines-valid="45">
  <packages>
    <package name="test_address_cache.exe" line-rate="1">
      <classes>
        <class name="address_cache.h" filename="native\hook\include\address_cache.h" line-rate="1">
          <lines><line number="68" hits="1"/>...</lines>
        </class>
        <class name="address_cache.cpp" filename="native\hook\src\address_cache.cpp" line-rate="1">
          <lines><line number="5" hits="1"/>...</lines>
        </class>
      </classes>
    </package>
  </packages>
</coverage>
```

**Parsing:** Identical to .NET Cobertura path — `line-rate` attribute on `<coverage>`, per-`<class>` `filename` and `line-rate`, per-`<line>` `number` and `hits`. Zero new parsing logic needed.

## Change Log

**Current Status:** QA Approved

| Date | Author | Phase/Action | Change | Files Affected |
|------|--------|--------------|--------|----------------|
| 2026-02-25 | .claude/story-requirements-analyst | Created | Story created from STORY-012 feedback recommendation rec-012-001 | STORY-500.story.md |
| 2026-02-26 | .claude/qa-result-interpreter | QA Deep | PASSED: 44/44 tests, 0 violations, 3/3 validators passed | - |

## Notes

**Design Decisions:**
- OpenCppCoverage chosen over gcov/lcov because it works natively with MSVC Debug builds (the project uses Visual Studio 2022 / CMake generator)
- Cobertura XML output format enables zero-change reuse of existing .NET parsing strategy
- C++ branch is additive-only (ELIF after Java) — existing language IF-chains are untouched
- Detection via CMakeLists.txt presence (consistent with how other languages detect: Cargo.toml → Rust, package.json → Node.js, etc.)

**Open Questions:**
- None — all technical unknowns resolved during STORY-012 session validation

**References:**
- OpenCppCoverage GitHub: https://github.com/OpenCppCoverage/OpenCppCoverage
- OpenCppCoverage Wiki FAQ: https://github.com/OpenCppCoverage/OpenCppCoverage/wiki/FAQ
- STORY-012 feedback analysis: devforgeai/feedback/ai-analysis/STORY-012/2026-02-25-post-release-analysis.json

Story Template Version: 2.9
Last Updated: 2026-02-25
