---
id: STORY-263
title: Add gaps.json auto-detection to /dev Phase 01.0
type: feature
epic: EPIC-040
sprint: Backlog
status: QA Approved
points: 2
depends_on: []
priority: MEDIUM
created: 2026-01-15
format_version: "2.5"
---

# Story: Add gaps.json auto-detection to /dev Phase 01.0

## Description

Currently, the `/dev` workflow requires developers to explicitly pass the `--fix` flag to enable remediation mode when QA gaps exist. This story adds automatic detection of `gaps.json` files in Phase 01.0.3 (Pre-Flight Validation), automatically enabling remediation mode without requiring the flag. This streamlines the QA-to-Dev feedback loop.

**Business Value:**
- Reduce friction in remediation workflow (eliminate flag requirement)
- Ensure developers don't forget `--fix` flag when gaps exist
- Automate mode selection based on actual QA output
- Improve developer experience during defect remediation

---

## User Story

**As a** DevForgeAI developer,
**I want** the `/dev` workflow to automatically detect the presence of a `gaps.json` file for my story during Phase 01.0 (Pre-Flight Validation),
**so that** remediation mode is enabled seamlessly without requiring me to remember the `--fix` flag, streamlining the QA-to-Dev feedback loop.

---

## Acceptance Criteria

### AC#1: Automatic gaps.json detection in Phase 01.0.3
**Given** a story with ID `STORY-XXX` has a corresponding gaps file at `devforgeai/qa/reports/STORY-XXX-gaps.json`
**When** the `/dev STORY-XXX` command is invoked (without `--fix` flag)
**Then** Phase 01.0.3 (after STORY_ID parsing in Pre-Flight Validation) checks for the gaps file existence, finds it, and sets `REMEDIATION_MODE=true` automatically

### AC#2: Mode change notification displayed
**Given** `REMEDIATION_MODE` has been automatically set to `true` due to gaps.json detection
**When** Phase 01.0.3 completes the detection check
**Then** a notification banner is displayed to inform the user that remediation mode was auto-detected

### AC#3: No change when gaps.json absent
**Given** a story with ID `STORY-YYY` has no corresponding gaps file
**When** the `/dev STORY-YYY` command is invoked
**Then** Phase 01.0.3 checks for gaps file, finds none, and `REMEDIATION_MODE` remains `false` (normal development workflow proceeds)

### AC#4: Explicit --fix flag still works
**Given** a developer explicitly passes the `--fix` flag
**When** the `/dev STORY-XXX --fix` command is invoked
**Then** `REMEDIATION_MODE=true` is set regardless of gaps.json presence, maintaining backward compatibility

### AC#5: Detection occurs before Phase 01.9.5
**Given** the current gaps.json loading happens at Phase 01.9.5
**When** auto-detection is implemented in Phase 01.0.3
**Then** the detection check runs immediately after STORY_ID parsing (Phase 01.0.2) and before git status validation (Phase 01.1)

---

## AC Verification Checklist

- [x] Phase 01.0.3 includes gaps.json detection logic after STORY_ID parsing
- [x] Glob pattern matches `devforgeai/qa/reports/STORY-XXX-gaps.json` exactly
- [x] REMEDIATION_MODE variable set to `true` when gaps file detected
- [x] Notification banner displayed when auto-detection occurs
- [x] Normal mode proceeds when no gaps file exists
- [x] Explicit `--fix` flag overrides auto-detection logic
- [x] Detection timing verified (Phase 01.0.3, before Phase 01.9.5)
- [ ] Phase state JSON records detection result (`gaps_auto_detected` field) - DEFERRED: Requires runtime instrumentation
- [ ] Performance < 100ms for detection operation - DEFERRED: Requires runtime benchmark
- [ ] Works on Windows, Linux, and macOS - DEFERRED: Requires CI platform testing

---

## Technical Specification

```yaml
technical_specification:
  format_version: "2.0"

  components:
    - type: "Service"
      name: "Phase 01.0.3 gaps.json Auto-Detection Service"
      file_path: ".claude/commands/dev.md"
      responsibilities:
        - "Check for gaps.json file existence after STORY_ID parsing"
        - "Set REMEDIATION_MODE=true if gaps file detected"
        - "Display notification to user"
      requirements:
        - id: "COMP-001"
          description: "Parse STORY_ID from command argument"
          testable: true
          test_requirement: "Test: STORY_ID extracted correctly from input (e.g., 'STORY-086' from '/dev STORY-086')"
          priority: "Critical"
        - id: "COMP-002"
          description: "Construct canonical gaps.json path from STORY_ID"
          testable: true
          test_requirement: "Test: Path constructed as 'devforgeai/qa/reports/STORY-XXX-gaps.json' with exact STORY_ID"
          priority: "Critical"
        - id: "COMP-003"
          description: "Check gaps.json file existence using Glob"
          testable: true
          test_requirement: "Test: Glob returns match when file exists, empty when absent"
          priority: "Critical"
        - id: "COMP-004"
          description: "Set REMEDIATION_MODE environment variable"
          testable: true
          test_requirement: "Test: REMEDIATION_MODE=true passed to subsequent phases"
          priority: "High"
        - id: "COMP-005"
          description: "Display auto-detection notification banner"
          testable: true
          test_requirement: "Test: Notification shown to user when gaps detected"
          priority: "High"
        - id: "COMP-006"
          description: "Handle missing gaps.json gracefully"
          testable: true
          test_requirement: "Test: No error when gaps.json absent; normal mode proceeds"
          priority: "High"

    - type: "Configuration"
      name: "Remediation Mode Override"
      file_path: ".claude/commands/dev.md"
      config_items:
        - "EXPLICIT_FIX_FLAG: Boolean flag for explicit --fix argument"
        - "GAPS_AUTO_DETECTED: Boolean flag for detection result"
        - "REMEDIATION_MODE: Final remediation mode (explicit flag OR auto-detected)"
      requirements:
        - id: "COMP-007"
          description: "Priority: explicit --fix flag overrides auto-detection"
          testable: true
          test_requirement: "Test: REMEDIATION_MODE=true with both --fix and auto-detected gaps"
          priority: "High"

    - type: "Logging"
      name: "Phase 01.0 Detection Logging"
      file_path: ".claude/commands/dev.md"
      requirements:
        - id: "COMP-008"
          description: "Record detection result in phase-state.json"
          testable: true
          test_requirement: "Test: phase-state.json includes 'gaps_auto_detected' field with true/false value"
          priority: "Medium"

  business_rules:
    - id: "BR-001"
      rule: "Detection must use exact STORY_ID pattern matching (preserve leading zeros, case)"
      category: "Pattern Matching"
      test_requirement: "Test: STORY-007 matches STORY-007-gaps.json, not STORY-7-gaps.json"

    - id: "BR-002"
      rule: "Explicit --fix flag takes priority over auto-detection"
      category: "Flag Priority"
      test_requirement: "Test: /dev STORY-XXX --fix enables REMEDIATION_MODE even if gaps.json absent"

    - id: "BR-003"
      rule: "If gaps.json malformed but exists, detection succeeds; parsing validates in Phase 01.9.5"
      category: "Graceful Degradation"
      test_requirement: "Test: Empty or invalid JSON in gaps.json still triggers REMEDIATION_MODE in Phase 01.0.3"

    - id: "BR-004"
      rule: "Multiple gaps files (versioned) do not trigger detection; only canonical format matches"
      category: "File Naming"
      test_requirement: "Test: STORY-086-gaps-v2.json present but STORY-086-gaps.json absent does not trigger"

  non_functional_requirements:
    - id: "NFR-001"
      category: "Performance"
      requirement: "Detection must not introduce significant Phase 01.0 delay"
      metric: "Detection < 100ms; Phase 01.0.3 overhead < 50ms"
      test_requirement: "Test: Measure Phase 01.0.3 execution time with/without gaps file"
      priority: "High"

    - id: "NFR-002"
      category: "Reliability"
      requirement: "Detection must work across all supported platforms"
      metric: "Windows, Linux, macOS all support Glob pattern matching"
      test_requirement: "Test: Auto-detection works on CI/CD runners for all platforms"
      priority: "High"

    - id: "NFR-003"
      category: "Security"
      requirement: "STORY_ID must be validated before path construction"
      metric: "STORY_ID matches regex '^STORY-\\d{1,4}$'; no path traversal possible"
      test_requirement: "Test: Invalid STORY_ID (../../escape, STORY-9999999) rejected before detection"
      priority: "Critical"

    - id: "NFR-004"
      category: "Scalability"
      requirement: "Detection independent of number of gaps files in directory"
      metric: "Pattern-based matching, not directory enumeration"
      test_requirement: "Test: Performance same with 1 vs 1000 gaps files"
      priority: "Medium"
```

---

## Non-Functional Requirements

### Performance
- Detection completion: < 100ms
- Phase 01.0.3 overhead: < 50ms above baseline
- No additional file reads or parsing during Phase 01.0

### Security
- STORY_ID validated against strict regex before path construction
- No path traversal: STORY_ID cannot contain `/`, `\`, `..`, or null bytes
- All file operations within project root boundary

### Reliability
- Works across Windows, Linux, macOS (using native Claude Code tools)
- Graceful degradation if Glob fails (log warning, proceed with REMEDIATION_MODE=false)
- Idempotent: multiple invocations produce identical results

### Scalability
- Detection performance independent of total gaps.json count
- Pattern-based matching, not directory enumeration
- Handles 1 to 1000+ gaps files without degradation

---

## Definition of Done

### Implementation
- [x] Phase 01.0.3 in `/dev` command includes gaps.json detection logic - Completed: Lines 107-130 in dev.md
- [x] Detection uses Glob pattern: `devforgeai/qa/reports/STORY-XXX-gaps.json` - Completed: Line 116
- [x] REMEDIATION_MODE set to true when gaps file detected - Completed: Line 121
- [x] Notification banner displayed on auto-detection - Completed: Lines 122-124
- [x] Explicit `--fix` flag takes priority over auto-detection - Completed: Line 118 condition
- [x] Backward compatibility maintained (existing `--fix` flag still works) - Verified: test-ac4 passes
- [ ] Phase 01.0.3 timing remains < 100ms for detection - DEFERRED: Requires runtime benchmark

### Testing
- [x] Unit test: gaps.json detection returns true when file exists - Completed: test-ac1
- [x] Unit test: Detection returns false when file absent - Completed: test-ac3
- [x] Unit test: STORY_ID validation rejects invalid formats - Completed: test-nfr003
- [x] Integration test: `/dev STORY-XXX` auto-detects gaps and sets REMEDIATION_MODE - Completed: integration-tester
- [x] Integration test: `/dev STORY-XXX --fix` works with/without gaps file - Completed: test-ac4
- [ ] Platform test: Detection works on Windows, Linux, macOS - DEFERRED: Requires CI runners
- [ ] Performance test: Detection completes < 100ms - DEFERRED: Requires runtime benchmark

### Documentation
- [x] Phase 01.0.3 section in `.claude/commands/dev.md` updated - Completed: Lines 107-130
- [x] Auto-detection behavior documented in `/dev` command reference - Completed: Quick Reference lines 23-24
- [x] Notification banner format documented - Completed: Lines 122-124 show format
- [x] Troubleshooting guide added for detection failures - Completed: docs/guides/gaps-json-auto-detection-troubleshooting.md

### Quality Assurance
- [x] Code review completed (correctness, edge case handling) - Completed: code-reviewer subagent
- [x] No Critical/High anti-pattern violations - Completed: context-validator passed
- [x] All acceptance criteria verified in test environment - Completed: 9/9 tests pass

---

## Edge Cases & Error Handling

1. **Missing gaps.json:** Silent proceed to normal mode (no error/warning)
2. **Multiple gaps files (versioned):** Only canonical `STORY-XXX-gaps.json` triggers detection
3. **Malformed gaps.json:** Detection succeeds, parsing validation deferred to Phase 01.9.5
4. **Permission denied:** Display warning, fall back to REMEDIATION_MODE=false
5. **Symbolic link to gaps.json:** Follow symlink and check target existence
6. **Concurrent deletion:** If deleted between Phase 01.0.3 and Phase 01.9.5, handle gracefully
7. **STORY_ID with leading zeros:** Match exactly (STORY-007 != STORY-7)
8. **Relative/absolute path:** Use project-root-relative path after project root validation

---

## Dependencies

**Dependencies on:** Phase 01.0 preflight completion (STORY_ID parsing at Phase 01.0.2, project root validation at Phase 01.0.1)

**Enables:** Phase 01.9.5 gaps.json loading (already exists, auto-detection makes flag optional)

---

## Implementation Notes

- Step 0.3 added to `.claude/commands/dev.md` (lines 107-130) implementing gaps.json auto-detection
- Uses native Glob tool for file detection (compliant with tech-stack.md)
- Security: STORY_ID validated in Step 0.1 before path construction (NFR-003)
- Notification banner displays "🔧 Auto-detected gaps.json - Remediation mode enabled" with path
- Explicit `--fix` flag takes priority over auto-detection (backward compatible)
- Quick Reference documentation updated (lines 23-24) to describe auto-detection behavior
- 9 test scripts created in `tests/results/STORY-263/` covering all ACs and technical requirements

### Deferred Items (Technical Reasons)
| Item | Reason | Follow-up |
|------|--------|-----------|
| Performance test < 100ms | Requires runtime benchmark instrumentation | Add to CI pipeline with timing metrics |
| Platform test (Win/Linux/macOS) | Requires CI runners on multiple platforms | Include in cross-platform CI matrix |
| Phase state JSON gaps_auto_detected field | Requires runtime instrumentation | Add to devforgeai-development skill Phase 01 |

---

## Change Log

| Date | Author | Phase/Action | Change | Files Affected |
|------|--------|-------------|--------|-----------------|
| 2026-01-15 | claude/story-requirements-analyst | Story Creation (Phase 2) | Initial requirements, AC, edge cases, NFRs generated | devforgeai/specs/Stories/STORY-263*.story.md |
| 2026-01-15 | claude/story-creation-skill | Story Creation (Phase 5) | Story file assembled and written to disk | devforgeai/specs/Stories/STORY-263-gaps-json-auto-detection-phase-0.story.md |
| 2026-01-16 | claude | Constitutional Compliance | Renamed "Phase 0.1" to "Phase 01.0.3" per coding-standards.md (phases start at 01, sub-steps Phase 01 Only) | STORY-263-gaps-json-auto-detection-phase-0.story.md |
| 2026-01-17 | claude/test-automator | Red (Phase 02) | Generated 9 test scripts for AC#1-5, COMP-002, COMP-003, BR-001, NFR-003 | tests/results/STORY-263/*.sh |
| 2026-01-17 | claude/backend-architect | Green (Phase 03) | Implemented Step 0.3 gaps.json auto-detection in dev.md | .claude/commands/dev.md |
| 2026-01-17 | claude/refactoring-specialist | Refactor (Phase 04) | Code review - no refactoring needed (clean implementation) | N/A |
| 2026-01-17 | claude/integration-tester | Integration (Phase 05) | Verified 8 integration points between Step 0.1/0.3/Phase 1 | N/A |
| 2026-01-17 | claude/opus | DoD Update (Phase 07) | Updated DoD checkboxes, documented deferrals, status → Dev Complete | STORY-263-gaps-json-auto-detection-phase-0.story.md |
| 2026-01-17 | claude/opus | Documentation (Phase 08) | Created troubleshooting guide per user request | docs/guides/gaps-json-auto-detection-troubleshooting.md |
| 2026-01-17 | claude/qa-result-interpreter | QA Deep | PASSED: Tests 9/9, Validators 3/3, Deferrals VALID | - |

**Current Status:** QA Approved (ready for /release)
