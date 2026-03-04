---
id: STORY-559
title: Anti-Rationalization Protections for Test Integrity
type: feature
epic: EPIC-087
sprint: Sprint-30
status: Backlog
points: 2
depends_on: []
priority: High
advisory: false
source_gap: null
source_story: null
assigned_to: null
created: 2026-03-03
format_version: "2.9"
---

# Story: Anti-Rationalization Protections for Test Integrity

## Description

**As a** DevForgeAI framework maintainer,
**I want** explicit anti-rationalization instructions in QA Phase 1.5 and a CLAUDE.md halt trigger for integrity mismatches,
**so that** the orchestrator cannot rationalize away CRITICAL test integrity findings by constructing plausible environmental explanations.

**Source:** RCA-046 (REC-3 + REC-4) — QA Test Integrity Bypass Via Rationalization

## Acceptance Criteria

### AC#1: Anti-Rationalization Warning in diff-regression-detection.md

```xml
<acceptance_criteria id="AC1" implements="REC-3">
  <given>The file src/claude/skills/devforgeai-qa/references/diff-regression-detection.md exists</given>
  <when>A developer reads Section 8 (Test Integrity Verification)</when>
  <then>An "ANTI-RATIONALIZATION WARNING" block appears immediately after the "no override mechanism" statement (line 206), explicitly naming forbidden rationalization patterns: WSL line endings, git analysis, encoding differences, platform artifacts. The warning states that snapshot checksums are ground truth and any mismatch sets overall_verdict = FAIL with no exceptions.</then>
  <verification>
    <source_files>
      <file hint="Target file">src/claude/skills/devforgeai-qa/references/diff-regression-detection.md</file>
    </source_files>
    <test_file>tests/STORY-559/test_ac1_anti_rationalization_warning.sh</test_file>
    <coverage_threshold>95</coverage_threshold>
  </verification>
</acceptance_criteria>
```

---

### AC#2: CLAUDE.md Halt Trigger for Integrity Mismatches

```xml
<acceptance_criteria id="AC2" implements="REC-4">
  <given>The CLAUDE.md file contains a halt_triggers section</given>
  <when>A developer reads the halt triggers</when>
  <then>A new halt trigger (number 10) exists for "Checksum/hash mismatch findings" that explicitly prohibits environmental rationalizations (WSL, line endings, encoding) as overrides for integrity failures, and instructs to report mismatches as-is without attempting to explain them away.</then>
  <verification>
    <source_files>
      <file hint="Target file">src/CLAUDE.md</file>
    </source_files>
    <test_file>tests/STORY-559/test_ac2_halt_trigger.sh</test_file>
    <coverage_threshold>95</coverage_threshold>
  </verification>
</acceptance_criteria>
```

---

### AC#3: System Prompt Halt Trigger Alignment

```xml
<acceptance_criteria id="AC3" implements="REC-4">
  <given>The system prompt contains halt_triggers section (in the DevForgeAI Core Directives)</given>
  <when>The orchestrator loads the system prompt at session start</when>
  <then>The system prompt halt_triggers section also contains the checksum integrity halt trigger, aligned with CLAUDE.md halt trigger #10</then>
  <verification>
    <source_files>
      <file hint="System prompt reference">src/CLAUDE.md</file>
    </source_files>
    <test_file>tests/STORY-559/test_ac3_system_prompt_alignment.sh</test_file>
    <coverage_threshold>95</coverage_threshold>
  </verification>
</acceptance_criteria>
```

## Technical Specification

```yaml
technical_specification:
  format_version: "2.0"

  components:
    - type: "Configuration"
      name: "diff-regression-detection-update"
      file_path: "src/claude/skills/devforgeai-qa/references/diff-regression-detection.md"
      required_keys:
        - key: "anti_rationalization_warning"
          type: "string"
          example: "ANTI-RATIONALIZATION WARNING block after line 206"
          required: true
          validation: "Must contain: 'ANTI-RATIONALIZATION', 'WSL', 'line ending', 'no exceptions', 'ground truth'"
          test_requirement: "Test: Verify warning block present with all required keywords"

    - type: "Configuration"
      name: "claude-md-halt-trigger"
      file_path: "src/CLAUDE.md"
      required_keys:
        - key: "halt_trigger_10"
          type: "string"
          example: "10. Checksum/hash mismatch findings"
          required: true
          validation: "Must appear in halt_triggers section, numbered 10"
          test_requirement: "Test: Verify halt trigger #10 exists with integrity mismatch content"

  business_rules:
    - id: "BR-001"
      rule: "Anti-rationalization warning must name specific forbidden patterns: WSL, line endings, git analysis, encoding, platform differences"
      trigger: "Any checksum mismatch during QA Phase 1.5"
      validation: "Warning text contains all 5 forbidden rationalization patterns"
      error_handling: "If any pattern missing, story fails AC#1"
      test_requirement: "Test: grep for each of the 5 forbidden patterns in warning block"
      priority: "Critical"
    - id: "BR-002"
      rule: "Halt trigger must be in both CLAUDE.md and system prompt for alignment"
      trigger: "Session start"
      validation: "Both files contain matching halt trigger content"
      error_handling: "If misaligned, run /audit-alignment"
      test_requirement: "Test: Verify both files contain 'Checksum/hash mismatch' halt trigger"
      priority: "High"

  non_functional_requirements:
    - id: "NFR-001"
      category: "Reliability"
      requirement: "Warning text must be unambiguous — no room for interpretation that allows rationalization"
      metric: "Warning contains explicit 'No exceptions. No analysis. No rationalization.' statement"
      test_requirement: "Test: Verify exact phrase exists in warning"
      priority: "Critical"
```

## Technical Limitations

```yaml
technical_limitations:
  - id: TL-001
    component: "Documentation-level enforcement"
    limitation: "Anti-rationalization warnings are still documentation-level, not programmatic. A sufficiently motivated rationalization could still bypass them."
    decision: "workaround:This is the short-term fix. STORY-560 (CLI command) provides the long-term programmatic enforcement."
    discovered_phase: "Architecture"
    impact: "Reduced but not eliminated rationalization risk until STORY-560 is implemented"
```

## Non-Functional Requirements (NFRs)

### Performance
- No performance impact (documentation changes only)

### Security
- No security implications

### Scalability
- N/A

### Reliability
- Warning effectiveness depends on LLM instruction following
- Long-term enforcement via STORY-560 CLI command

### Observability
- Future QA runs that encounter checksum mismatches will be observable evidence of whether the warning is effective

## Dependencies

### Prerequisite Stories
- None

### External Dependencies
- None

### Technology Dependencies
- None (markdown documentation changes only)

## Test Strategy

### Unit Tests

**Coverage Target:** 95%+

**Test Scenarios:**
1. Anti-rationalization warning present in diff-regression-detection.md
2. Warning contains all 5 forbidden rationalization patterns
3. CLAUDE.md halt trigger #10 exists
4. Halt trigger mentions integrity/checksum mismatches

### Integration Tests

**Coverage Target:** 85%+

**Test Scenarios:**
1. System prompt halt triggers aligned with CLAUDE.md
2. Warning positioned correctly (after "no override" statement)

## Acceptance Criteria Verification Checklist

### AC#1: Anti-Rationalization Warning
- [ ] Warning block present after line 206 - **Phase:** 2 - **Evidence:** diff-regression-detection.md
- [ ] Contains "ANTI-RATIONALIZATION" heading - **Phase:** 2
- [ ] Names WSL as forbidden rationalization - **Phase:** 2
- [ ] Names line endings as forbidden rationalization - **Phase:** 2
- [ ] Names git analysis as forbidden rationalization - **Phase:** 2
- [ ] States "No exceptions. No analysis. No rationalization." - **Phase:** 2

### AC#2: CLAUDE.md Halt Trigger
- [ ] Halt trigger #10 exists in CLAUDE.md - **Phase:** 2
- [ ] Mentions checksum/hash mismatch - **Phase:** 2
- [ ] Prohibits environmental rationalizations - **Phase:** 2

### AC#3: System Prompt Alignment
- [ ] System prompt halt triggers contain matching content - **Phase:** 2

---

**Checklist Progress:** 0/10 items complete (0%)

## Implementation Notes

*(To be filled during /dev workflow)*

## Definition of Done

### Implementation
- [ ] Anti-rationalization warning added to diff-regression-detection.md after line 206
- [ ] CLAUDE.md halt trigger #10 added for integrity mismatches
- [ ] System prompt halt trigger aligned with CLAUDE.md

### Quality
- [ ] No placeholder text (no TBD, TODO)
- [ ] Warning is unambiguous and names specific forbidden patterns

### Testing
- [ ] All AC tests pass
- [ ] Integration test confirms alignment between CLAUDE.md and system prompt

### Documentation
- [ ] RCA-046 referenced in warning text
- [ ] Change log updated

### TDD Workflow Summary

*(To be filled during /dev workflow)*

### Files Created/Modified

*(To be filled during /dev workflow)*

## Change Log

| Date | Author | Phase/Action | Change | Files Affected |
|------|--------|--------------|--------|----------------|
| 2026-03-03 | RCA-046 | Created | Story created from RCA-046 REC-3 + REC-4 | STORY-559 |

## Notes

**Design Decisions:**
- Combined REC-3 and REC-4 into single story since both are small documentation edits (~0.75 hours total)
- Warning text explicitly names the exact rationalization pattern observed in RCA-046 (WSL artifact)
- Short-term fix only — long-term enforcement is STORY-560 (CLI command)

**References:**
- RCA-046: QA Test Integrity Bypass Via Rationalization
- STORY-502: Red-Phase Test Integrity Checksums
- RCA-043: Test Integrity Snapshot Skipped

---

## Exact Implementation Specification

### AC#1 — Exact Text to Insert

**Target file:** `src/claude/skills/devforgeai-qa/references/diff-regression-detection.md`

**Insert AFTER this exact text** (the "No Override Rule" paragraph):
```
TEST TAMPERING, UNAUTHORIZED FILE ADDED, and FILE DELETED findings **cannot be deferred or bypassed**. There is **no override** mechanism for test integrity violations. Any such finding sets `overall_verdict = FAIL` unconditionally.
```

**Insert this block:**
```markdown
**ANTI-RATIONALIZATION WARNING (RCA-046):** Do NOT attempt to explain away
checksum mismatches using environmental factors. The following rationalizations
are EXPLICITLY FORBIDDEN:

1. **WSL line endings** — "Checksums differ due to CRLF/LF conversion"
2. **Git analysis** — "git log/git show proves the file wasn't modified"
3. **Encoding differences** — "File encoding changed but content is the same"
4. **Platform artifacts** — "Different OS computed checksums differently"
5. **Tool differences** — "sha256sum vs hashlib produce different results"

The red-phase snapshot checksums ARE the ground truth. They were computed
in the same environment during Phase 02. If checksums mismatch, the file
was modified after RED phase — period. The reason for the modification is
irrelevant. Any modification invalidates test integrity.

**Action on mismatch:** Set `overall_verdict = FAIL`. No exceptions.
No analysis. No rationalization. Do not perform additional git investigation.
Do not construct alternative explanations. Report the mismatch and HALT.
```

### AC#2 — Exact Text to Insert

**Target file:** `src/CLAUDE.md`

**Insert AFTER** halt trigger #9 (`3+ consecutive fix attempts fail`) in the `<halt_triggers>` section:
```markdown
10. **Checksum/hash mismatch findings** — When a security or integrity verification
    produces a mismatch (SHA-256, MD5, file hash), report it as-is and HALT.
    Do NOT construct environmental explanations (WSL, line endings, encoding,
    platform differences). Integrity mismatches are findings, not puzzles to solve.
```

### AC#3 — System Prompt Clarification

The "system prompt" in this project is the content embedded at the top of each conversation by Anthropic's system. It is NOT a separate file that developers edit directly. **The system prompt `<halt_triggers>` section is derived from CLAUDE.md** and loaded automatically.

**Action:** After updating CLAUDE.md (AC#2), verify the system prompt `<halt_triggers>` section shown at conversation start also includes trigger #10. If the system prompt is managed separately (e.g., in a `.claude/system-prompt-core.md` file), update that file too. If no separate file exists, AC#3 is satisfied by AC#2 since CLAUDE.md IS the source for system prompt halt triggers.

**Verification:** In a new session, check that the halt_triggers section visible in the system-reminder contains the checksum integrity trigger.

---

Story Template Version: 2.9
Last Updated: 2026-03-03
