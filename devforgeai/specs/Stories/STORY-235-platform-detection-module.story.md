---
id: STORY-235
title: Platform Detection Module
type: feature
epic: EPIC-035
sprint: Backlog
status: Backlog
points: 3
depends_on: []
priority: Critical
assigned_to: Unassigned
created: 2025-01-05
format_version: "2.5"
---

# Story: Platform Detection Module

## Description

**As a** DevForgeAI installer user,
**I want** the installer to automatically detect my operating system, WSL version, and filesystem type,
**so that** the installer can provide platform-specific handling, warnings, and error messages tailored to my environment.

**Background:**
This story implements EPIC-035 Feature 2, which enables the installer to detect:
- Operating system (Windows, macOS, Linux)
- WSL presence and version (WSL 1 vs WSL 2)
- Filesystem type (NTFS, ext4, APFS, etc.)
- Cross-filesystem scenarios (e.g., WSL accessing /mnt/c which is NTFS)
- chmod support capability (NTFS doesn't support Unix permissions)

## Acceptance Criteria

### AC#1: Operating System Detection

**Given** the installer is running on any supported platform,
**When** the platform detector is invoked,
**Then** it correctly identifies the operating system as "Windows", "Darwin" (macOS), or "Linux".

---

### AC#2: WSL Version Detection

**Given** the installer is running on a Linux system,
**When** the platform detector checks for WSL,
**Then** it correctly identifies:
- Whether WSL is present (True/False)
- WSL version (1 or 2) if present
- None if not running in WSL

---

### AC#3: Filesystem Type Detection

**Given** the installer is running with a target installation path,
**When** the platform detector analyzes the path,
**Then** it correctly identifies the filesystem type:
- "ext4", "btrfs", "xfs" for native Linux
- "ntfs", "fat32" for Windows
- "apfs", "hfs+" for macOS
- "ntfs-wsl" for NTFS accessed via WSL

---

### AC#4: Cross-Filesystem Detection

**Given** the installer is running in WSL with a target path starting with "/mnt/",
**When** the platform detector analyzes the path,
**Then** it correctly sets `is_cross_filesystem: true` and determines that chmod operations will not work.

---

### AC#5: PlatformInfo Data Structure

**Given** platform detection completes successfully,
**When** the detection results are returned,
**Then** a `PlatformInfo` dataclass is returned with all fields populated:
- `os_type`: str
- `is_wsl`: bool
- `wsl_version`: Optional[int]
- `filesystem`: str
- `is_cross_filesystem`: bool
- `supports_chmod`: bool

---

## Technical Specification

```yaml
technical_specification:
  format_version: "2.0"

  components:
    - type: "DataModel"
      name: "PlatformInfo"
      table: "N/A (in-memory dataclass)"
      purpose: "Holds platform detection results for use throughout installer"
      fields:
        - name: "os_type"
          type: "String"
          constraints: "Required"
          description: "Operating system: 'Linux', 'Darwin', 'Windows'"
          test_requirement: "Test: Verify os_type matches platform.system() output"
        - name: "is_wsl"
          type: "Bool"
          constraints: "Required"
          description: "True if running inside Windows Subsystem for Linux"
          test_requirement: "Test: Verify WSL detection via /proc/version"
        - name: "wsl_version"
          type: "Optional[Int]"
          constraints: "None"
          description: "1 or 2 if WSL detected, None otherwise"
          test_requirement: "Test: Verify WSL 1 vs 2 detection"
        - name: "filesystem"
          type: "String"
          constraints: "Required"
          description: "Filesystem type: 'ext4', 'ntfs', 'apfs', 'ntfs-wsl', etc."
          test_requirement: "Test: Verify filesystem detection for each platform"
        - name: "is_cross_filesystem"
          type: "Bool"
          constraints: "Required"
          description: "True if path crosses filesystem boundaries (e.g., WSL -> /mnt/c)"
          test_requirement: "Test: Verify cross-filesystem detection for /mnt/ paths"
        - name: "supports_chmod"
          type: "Bool"
          constraints: "Required"
          description: "False for NTFS/FAT32, True for Unix filesystems"
          test_requirement: "Test: Verify chmod support based on filesystem type"

    - type: "Service"
      name: "PlatformDetector"
      file_path: "installer/platform_detector.py"
      interface: "Static methods"
      lifecycle: "Static"
      dependencies: []
      requirements:
        - id: "SVC-001"
          description: "Detect operating system using platform.system()"
          testable: true
          test_requirement: "Test: Mock platform.system() and verify os_type"
          priority: "Critical"
        - id: "SVC-002"
          description: "Detect WSL by parsing /proc/version for 'microsoft'"
          testable: true
          test_requirement: "Test: Mock /proc/version content and verify WSL detection"
          priority: "Critical"
        - id: "SVC-003"
          description: "Detect WSL version (1 vs 2) from version string"
          testable: true
          test_requirement: "Test: Verify 'WSL2' in version string returns version=2"
          priority: "High"
        - id: "SVC-004"
          description: "Detect cross-filesystem when path starts with /mnt/ in WSL"
          testable: true
          test_requirement: "Test: Verify /mnt/c paths return is_cross_filesystem=True"
          priority: "Critical"
        - id: "SVC-005"
          description: "Determine chmod support based on filesystem type"
          testable: true
          test_requirement: "Test: Verify supports_chmod=False for NTFS/FAT32"
          priority: "High"

  business_rules:
    - id: "BR-001"
      rule: "WSL detection must gracefully handle missing /proc/version"
      trigger: "When /proc/version does not exist (Windows/macOS)"
      validation: "Catch FileNotFoundError and return is_wsl=False"
      error_handling: "Return default non-WSL values"
      test_requirement: "Test: Verify no exception when /proc/version missing"
      priority: "Critical"
    - id: "BR-002"
      rule: "Cross-filesystem detection only applies in WSL"
      trigger: "When checking path for cross-filesystem access"
      validation: "Only check /mnt/ prefix if is_wsl=True"
      error_handling: "Return is_cross_filesystem=False if not WSL"
      test_requirement: "Test: Verify non-WSL Linux with /mnt/ returns False"
      priority: "High"

  non_functional_requirements:
    - id: "NFR-001"
      category: "Performance"
      requirement: "Platform detection must complete quickly"
      metric: "< 100ms execution time"
      test_requirement: "Test: Verify detection completes under 100ms"
      priority: "High"
    - id: "NFR-002"
      category: "Reliability"
      requirement: "Must work on all supported platforms"
      metric: "100% success rate on Windows, macOS, Linux, WSL 1/2"
      test_requirement: "Test: Platform-specific test cases for each OS"
      priority: "Critical"
```

---

## Technical Limitations

```yaml
technical_limitations: []
```

---

## Non-Functional Requirements (NFRs)

### Performance

**Response Time:**
- **Platform detection:** < 100ms

**Throughput:**
- Single call per installation session

---

### Security

**Authentication:**
- None required (local system detection)

**Authorization:**
- None required

**Data Protection:**
- No sensitive data collected
- No PII handling

---

### Reliability

**Error Handling:**
- Gracefully handle missing /proc/version
- Gracefully handle permission errors reading filesystem info
- Return safe defaults on detection failure

**Retry Logic:**
- No retries (single attempt)

---

## Dependencies

### Prerequisite Stories

None - this is a foundational component.

### External Dependencies

None - uses Python stdlib only.

### Technology Dependencies

- **Python 3.10+:** Standard library modules only
  - `platform` module for OS detection
  - `pathlib` for path handling
  - `dataclasses` for PlatformInfo structure

---

## Test Strategy

### Unit Tests

**Coverage Target:** 95%+

**Test Scenarios:**
1. **Happy Path:** Detect Linux on Linux, Windows on Windows, macOS on macOS
2. **Edge Cases:**
   - WSL 1 vs WSL 2 differentiation
   - /mnt/c path in WSL (cross-filesystem)
   - Native Linux with /mnt/ directory (not cross-filesystem)
3. **Error Cases:**
   - Missing /proc/version file
   - Unreadable filesystem info

**Test File:** `tests/STORY-235/test_platform_detector.py`

---

### Integration Tests

**Coverage Target:** 85%

**Test Scenarios:**
1. **End-to-End Detection:** Run detector on current platform, verify all fields populated
2. **Cross-Platform:** CI tests on Windows, macOS, Linux runners

---

## Acceptance Criteria Verification Checklist

### AC#1: Operating System Detection

- [x] Test: platform.system() mocked to "Linux" returns os_type="Linux" - **Phase:** 2 - **Evidence:** test_platform_detector.py
- [x] Test: platform.system() mocked to "Darwin" returns os_type="Darwin" - **Phase:** 2 - **Evidence:** test_platform_detector.py
- [x] Test: platform.system() mocked to "Windows" returns os_type="Windows" - **Phase:** 2 - **Evidence:** test_platform_detector.py

### AC#2: WSL Version Detection

- [x] Test: /proc/version with "microsoft" returns is_wsl=True - **Phase:** 2 - **Evidence:** test_platform_detector.py
- [x] Test: /proc/version with "WSL2" returns wsl_version=2 - **Phase:** 2 - **Evidence:** test_platform_detector.py
- [x] Test: /proc/version without "microsoft" returns is_wsl=False - **Phase:** 2 - **Evidence:** test_platform_detector.py
- [x] Test: Missing /proc/version returns is_wsl=False - **Phase:** 2 - **Evidence:** test_platform_detector.py

### AC#3: Filesystem Type Detection

- [x] Test: Native Linux path returns filesystem="ext4" or similar - **Phase:** 2 - **Evidence:** test_platform_detector.py
- [x] Test: WSL /mnt/c path returns filesystem="ntfs-wsl" - **Phase:** 2 - **Evidence:** test_platform_detector.py

### AC#4: Cross-Filesystem Detection

- [x] Test: WSL + /mnt/c path returns is_cross_filesystem=True - **Phase:** 2 - **Evidence:** test_platform_detector.py
- [x] Test: Native Linux + /mnt/data returns is_cross_filesystem=False - **Phase:** 2 - **Evidence:** test_platform_detector.py

### AC#5: PlatformInfo Data Structure

- [x] Implement PlatformInfo dataclass with all fields - **Phase:** 3 - **Evidence:** platform_detector.py
- [x] Test: All fields populated in returned PlatformInfo - **Phase:** 3 - **Evidence:** test_platform_detector.py

---

**Checklist Progress:** 13/13 items complete (100%)

---

## Definition of Done

### Implementation
- [x] PlatformInfo dataclass created in installer/platform_detector.py
- [x] PlatformDetector.detect() method implemented
- [x] WSL detection via /proc/version parsing
- [x] Cross-filesystem detection for /mnt/ paths
- [x] chmod support determination based on filesystem

### Quality
- [x] All 5 acceptance criteria have passing tests
- [x] Edge cases covered (WSL 1 vs 2, missing files, native Linux /mnt/)
- [x] Error handling for missing /proc/version
- [x] NFRs met (< 100ms execution)
- [x] Code coverage >95% for platform_detector.py

### Testing
- [x] Unit tests for OS detection
- [x] Unit tests for WSL detection
- [x] Unit tests for filesystem detection
- [x] Unit tests for cross-filesystem detection
- [x] Integration test on current platform

### Documentation
- [x] Docstrings for PlatformInfo and PlatformDetector
- [x] Usage examples in module docstring

---

## Change Log

**Current Status:** Dev Complete

| Date | Author | Phase/Action | Change | Files Affected |
|------|--------|--------------|--------|----------------|
| 2025-01-05 17:30 | claude/story-requirements-analyst | Created | Story created for EPIC-035 Feature 2 | STORY-235-platform-detection-module.story.md |
| 2026-01-06 | claude/test-automator | Red (Phase 02) | 43 tests generated for all ACs | installer/tests/STORY-235/test_platform_detector.py |
| 2026-01-06 | claude/backend-architect | Green (Phase 03) | PlatformInfo and PlatformDetector implemented | installer/platform_detector.py |
| 2026-01-06 | claude/refactoring-specialist | Refactor (Phase 04) | No refactoring needed - code clean | installer/platform_detector.py |
| 2026-01-06 | claude/opus | DoD (Phase 07) | All DoD items completed | STORY-235-platform-detection-module.story.md |

## Implementation Notes

- [x] PlatformInfo dataclass created in installer/platform_detector.py - Completed: 6 fields (os_type, is_wsl, wsl_version, filesystem, is_cross_filesystem, supports_chmod)
- [x] PlatformDetector.detect() method implemented - Completed: static method with optional path parameter, caching
- [x] WSL detection via /proc/version parsing - Completed: case-insensitive "microsoft" check with graceful error handling
- [x] Cross-filesystem detection for /mnt/ paths - Completed: only in WSL context when path starts with /mnt/ + drive letter
- [x] chmod support determination based on filesystem - Completed: False for NTFS/FAT32, True for ext4/btrfs/xfs/apfs/hfs+
- [x] All 5 acceptance criteria have passing tests - Completed: 43 tests, 96% coverage
- [x] Edge cases covered (WSL 1 vs 2, missing files, native Linux /mnt/) - Completed: comprehensive test suite
- [x] Error handling for missing /proc/version - Completed: returns is_wsl=False gracefully
- [x] NFRs met (< 100ms execution) - Completed: sub-100ms per test NFR-001
- [x] Code coverage >95% for platform_detector.py - Completed: 96% coverage
- [x] Unit tests for OS detection - Completed: TestOperatingSystemDetection class
- [x] Unit tests for WSL detection - Completed: TestWSLVersionDetection class
- [x] Unit tests for filesystem detection - Completed: TestFilesystemTypeDetection class
- [x] Unit tests for cross-filesystem detection - Completed: TestCrossFilesystemDetection class
- [x] Integration test on current platform - Completed: end-to-end detection test
- [x] Docstrings for PlatformInfo and PlatformDetector - Completed: comprehensive docstrings with usage examples
- [x] Usage examples in module docstring - Completed: module-level usage example

## Notes

**Design Decisions:**
- Use dataclass for PlatformInfo (Python stdlib, no dependencies)
- Static methods on PlatformDetector class for simplicity
- Cache detection results (platform doesn't change during session)

**Implementation Notes:**
- WSL detection relies on /proc/version containing "microsoft" (case-insensitive)
- WSL 2 is identified by "WSL2" or "wsl2" in version string
- Cross-filesystem detection only meaningful in WSL context

**References:**
- EPIC-035: Installer Pre-Flight Validation & Platform Detection
- installer/deploy.py: Will consume PlatformInfo for permission handling
