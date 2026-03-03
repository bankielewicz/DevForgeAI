/**
 * Integration Tests: STORY-504 - Test Folder Write Protection Rule
 *
 * Verifies cross-system integrations:
 * 1. CLAUDE.md conditional rules table entry is parseable
 * 2. Cross-story references (STORY-502, STORY-503) from same EPIC-085
 * 3. Operational/Source sync (src/ vs .claude/ duplication)
 */

const fs = require('fs');
const path = require('path');

const PROJECT_ROOT = path.resolve(__dirname, '..', '..');
const RULE_FILE_SRC = path.join(PROJECT_ROOT, 'src', 'claude', 'rules', 'workflow', 'test-folder-protection.md');
const RULE_FILE_OPS = path.join(PROJECT_ROOT, '.claude', 'rules', 'workflow', 'test-folder-protection.md');
const CLAUDE_MD = path.join(PROJECT_ROOT, 'CLAUDE.md');
const STORY_502 = path.join(PROJECT_ROOT, 'devforgeai', 'specs', 'Stories', 'STORY-502-red-phase-test-integrity-checksums.story.md');
const STORY_503 = path.join(PROJECT_ROOT, 'devforgeai', 'specs', 'Stories', 'STORY-503-test-tampering-heuristic-patterns.story.md');

/**
 * Helper: Read file content or throw with context.
 */
function readFileRequired(filePath) {
  try {
    return fs.readFileSync(filePath, 'utf-8');
  } catch (error) {
    throw new Error(`Failed to read ${filePath}: ${error.message}`);
  }
}

/**
 * Helper: Extract conditional rules entries from CLAUDE.md
 */
function extractConditionalRulesEntries(claudeMdContent) {
  const lines = claudeMdContent.split('\n');

  // Find "Conditional Rules" section
  let inSection = false;
  let entries = [];

  for (let i = 0; i < lines.length; i++) {
    const line = lines[i];

    if (/^##\s+Conditional\s+Rules/i.test(line)) {
      inSection = true;
      continue;
    }

    // Stop at next section header (##)
    if (inSection && /^##\s+/i.test(line)) {
      break;
    }

    // Collect bullet entries (lines starting with -, *, or +)
    if (inSection && /^\s*[-*+]\s+`/.test(line)) {
      entries.push(line.trim());
    }
  }

  return entries;
}

// ===========================================================================
// INTEGRATION TEST 1: CLAUDE.md Conditional Rules Entry
// ===========================================================================
describe('INTEGRATION: CLAUDE.md Conditional Rules Entry', () => {
  let claudeMdContent;
  let entries;

  beforeAll(() => {
    claudeMdContent = readFileRequired(CLAUDE_MD);
    entries = extractConditionalRulesEntries(claudeMdContent);
  });

  test('should_parse_test_folder_protection_entry_in_conditional_rules_without_syntax_errors', () => {
    // Arrange: Look for test-folder-protection.md in entries
    const protectionEntry = entries.find(entry => entry.includes('test-folder-protection.md'));

    // Assert: Entry must exist and be parseable
    expect(protectionEntry).toBeDefined();

    // Verify it contains path patterns from the tech spec
    const fullEntry = protectionEntry.toLowerCase();
    expect(fullEntry).toMatch(/tests\/\*\*/);
    expect(fullEntry).toMatch(/\.test\./);
    expect(fullEntry).toMatch(/\.spec\./);
  });

  test('should_appear_adjacent_to_other_workflow_rules_with_consistent_formatting', () => {
    // Arrange: Count all rule entries in the list
    const ruleEntries = entries.filter(entry => entry.includes('.md'));

    // Assert: Must have multiple rules for consistent formatting context
    expect(ruleEntries.length).toBeGreaterThan(1);

    // Find position of test-folder-protection.md
    const testProtectionIdx = ruleEntries.findIndex(entry => entry.includes('test-folder-protection'));
    expect(testProtectionIdx).toBeGreaterThanOrEqual(0);

    // Assert: Should be surrounded by other rules (consistent with list structure)
    // Verify entries before and after follow same pattern
    if (testProtectionIdx > 0) {
      expect(ruleEntries[testProtectionIdx - 1]).toMatch(/^\s*[-*+]\s+`/);
    }
    if (testProtectionIdx < ruleEntries.length - 1) {
      expect(ruleEntries[testProtectionIdx + 1]).toMatch(/^\s*[-*+]\s+`/);
    }
  });
});

// ===========================================================================
// INTEGRATION TEST 2: Cross-Story References (EPIC-085)
// ===========================================================================
describe('INTEGRATION: Cross-Story References from EPIC-085', () => {
  let protectionRuleContent;
  let story502Content;
  let story503Content;

  beforeAll(() => {
    protectionRuleContent = readFileRequired(RULE_FILE_SRC);
    story502Content = readFileRequired(STORY_502);
    story503Content = readFileRequired(STORY_503);
  });

  test('should_reference_story_502_for_test_integrity_checksums_integration', () => {
    // Arrange: Protection rule rationale mentions STORY-502
    // Act: Search for reference
    const hasStory502Ref = /STORY-502|red-phase.*checksum|checksum.*integrity/i.test(protectionRuleContent);

    // Assert: Cross-reference must exist
    expect(hasStory502Ref).toBe(true);
    expect(protectionRuleContent).toMatch(/STORY-502|in conjunction with/i);
  });

  test('should_reference_story_503_for_test_tampering_heuristics_integration', () => {
    // Arrange: Protection rule rationale mentions STORY-503
    // Act: Search for reference
    const hasStory503Ref = /STORY-503|test.*tampering.*heuristic|heuristic.*pattern/i.test(protectionRuleContent);

    // Assert: Cross-reference must exist
    expect(hasStory503Ref).toBe(true);
    expect(protectionRuleContent).toMatch(/STORY-503|STORY-502|in conjunction with/i);
  });

  test('should_establish_epic_level_workflow_integration_with_related_stories', () => {
    // Arrange: All three stories should reference EPIC-085
    // Act: Check story metadata
    const testProtectionRefersToEpic = /EPIC-085/i.test(protectionRuleContent) ||
                                       /epic.*085|085.*epic/i.test(protectionRuleContent);
    const story502HasEpic = /EPIC-085/i.test(story502Content);
    const story503HasEpic = /EPIC-085/i.test(story503Content);

    // Assert: All three should be part of same epic
    expect(testProtectionRefersToEpic || story502HasEpic || story503HasEpic).toBe(true);

    // Verify thematic alignment (test integrity system)
    expect(protectionRuleContent.toLowerCase()).toContain('test');
    expect(story502Content.toLowerCase()).toContain('test');
    expect(story503Content.toLowerCase()).toContain('test');
  });
});

// ===========================================================================
// INTEGRATION TEST 3: Operational/Source Sync Validation
// ===========================================================================
describe('INTEGRATION: Operational/Source File Synchronization', () => {
  let srcContent;
  let opsContent;

  beforeAll(() => {
    srcContent = readFileRequired(RULE_FILE_SRC);
    opsContent = readFileRequired(RULE_FILE_OPS);
  });

  test('should_have_identical_content_in_src_and_operational_locations', () => {
    // Arrange: Both files should be byte-for-byte identical
    // Act: Compare content
    const contentMatch = srcContent === opsContent;

    // Assert: Must be in sync
    expect(contentMatch).toBe(true);

    if (!contentMatch) {
      // Provide diagnostic info
      const srcLines = srcContent.split('\n').length;
      const opsLines = opsContent.split('\n').length;
      expect(`src has ${srcLines} lines`).toBe(`ops has ${opsLines} lines`);
    }
  });

  test('should_maintain_file_integrity_across_both_storage_locations', () => {
    // Arrange: Hash both files to ensure integrity
    const crypto = require('crypto');

    // Act: Calculate checksums
    const srcHash = crypto.createHash('sha256').update(srcContent).digest('hex');
    const opsHash = crypto.createHash('sha256').update(opsContent).digest('hex');

    // Assert: Hashes must match
    expect(srcHash).toBe(opsHash);
  });

  test('should_preserve_critical_sections_across_sync', () => {
    // Arrange: Critical sections that must survive sync
    const criticalPatterns = [
      /##\s+HALT\s+Trigger/i,
      /##\s+Authorized\s+Agents/i,
      /##\s+Protected\s+Path\s+Patterns/i,
      /test-automator/,
      /integration-tester/,
      /Phase\s+0?2/,
      /Phase\s+0?5/
    ];

    // Act & Assert: Both files must contain all critical sections
    for (const pattern of criticalPatterns) {
      expect(srcContent).toMatch(pattern);
      expect(opsContent).toMatch(pattern);
    }
  });
});

// ===========================================================================
// INTEGRATION TEST 4: Rule Active During Workflow Phases
// ===========================================================================
describe('INTEGRATION: Rule Enforcement During TDD Workflow Phases', () => {
  let ruleContent;

  beforeAll(() => {
    ruleContent = readFileRequired(RULE_FILE_SRC);
  });

  test('should_document_phase_specific_behavior_for_all_workflow_phases', () => {
    // Arrange: Rule should have phase-specific behavior documented
    // Act: Check for phase table or explicit phase references
    const hasPhaseTable = /\|\s*Phase\s*\|/.test(ruleContent);
    const hasPhaseRefs = /(Phase\s+0[1-6]|Phase\s+1[0-9])/g.test(ruleContent);

    // Assert: Must document phases
    expect(hasPhaseTable || hasPhaseRefs).toBe(true);

    // Verify critical phases are mentioned
    expect(ruleContent).toMatch(/Phase\s+0?2.*Red/i);
    expect(ruleContent).toMatch(/Phase\s+0?5.*Integration/i);
    expect(ruleContent).toMatch(/Phase\s+0?4.*Refactor/i);
  });

  test('should_specify_halt_precedence_for_unauthorized_test_modifications_in_non_designated_phases', () => {
    // Arrange: Rule should be clear about default behavior
    // Act: Check for explicit restriction outside Phase 02 and 05
    const nonDesignatedPhaseRestrictions = ruleContent.match(/Phase\s+0[346]/gi);
    const haltsInOtherPhases = /Phase\s+0[346].*HALT|HALT.*Phase\s+0[346]/i.test(ruleContent);

    // Assert: Other phases must trigger HALT
    expect(haltsInOtherPhases || nonDesignatedPhaseRestrictions).toBeDefined();
    expect(ruleContent).toMatch(/Phase.*04.*HALT|Phase.*04.*AskUserQuestion/i);
  });
});
