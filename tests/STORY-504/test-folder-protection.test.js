/**
 * Test: STORY-504 - Test Folder Write Protection Rule
 * Phase: RED (TDD - all tests should FAIL initially)
 * Generated: 2026-02-27
 *
 * Tests verify the rule file at src/claude/rules/workflow/test-folder-protection.md
 * and the CLAUDE.md conditional rules table update.
 */

const fs = require('fs');
const path = require('path');

const PROJECT_ROOT = path.resolve(__dirname, '..', '..');
const RULE_FILE = path.join(PROJECT_ROOT, 'src', 'claude', 'rules', 'workflow', 'test-folder-protection.md');
const CLAUDE_MD = path.join(PROJECT_ROOT, 'CLAUDE.md');

/**
 * Helper: Read file content or return null if missing.
 */
function readFileOrNull(filePath) {
  try {
    return fs.readFileSync(filePath, 'utf-8');
  } catch {
    return null;
  }
}

// ---------------------------------------------------------------------------
// AC#1: Rule File Exists at Correct Path with Required Content
// ---------------------------------------------------------------------------
describe('AC#1: Rule File Exists at Correct Path with Required Content', () => {
  let content;

  beforeAll(() => {
    content = readFileOrNull(RULE_FILE);
  });

  test('test_should_exist_when_rule_file_path_checked', () => {
    expect(content).not.toBeNull();
  });

  test('test_should_contain_halt_trigger_section_when_rule_file_read', () => {
    expect(content).not.toBeNull();
    expect(content.toLowerCase()).toMatch(/halt\s+trigger/i);
  });

  test('test_should_declare_tests_folder_as_restricted_write_when_halt_trigger_read', () => {
    expect(content).not.toBeNull();
    expect(content).toMatch(/tests\//);
    expect(content.toLowerCase()).toMatch(/restricted/i);
  });

  test('test_should_name_test_automator_as_authorized_agent_when_rule_file_read', () => {
    expect(content).not.toBeNull();
    expect(content).toMatch(/test-automator/);
  });

  test('test_should_name_integration_tester_as_authorized_agent_when_rule_file_read', () => {
    expect(content).not.toBeNull();
    expect(content).toMatch(/integration-tester/);
  });

  test('test_should_specify_askuserquestion_protocol_when_rule_file_read', () => {
    expect(content).not.toBeNull();
    expect(content).toMatch(/AskUserQuestion/);
  });
});

// ---------------------------------------------------------------------------
// AC#2: Rule Is Auto-Loaded via .claude/rules/ Discovery
// ---------------------------------------------------------------------------
describe('AC#2: Rule Is Auto-Loaded via .claude/rules/ Discovery', () => {
  test('test_should_be_in_claude_rules_workflow_directory_when_path_checked', () => {
    const content = readFileOrNull(RULE_FILE);
    expect(content).not.toBeNull();
    // Verify directory structure matches .claude/rules/workflow/
    expect(RULE_FILE).toMatch(/rules[/\\]workflow[/\\]test-folder-protection\.md$/);
  });

  test('test_should_be_referenced_in_claude_md_when_conditional_rules_checked', () => {
    const claudeMd = readFileOrNull(CLAUDE_MD);
    expect(claudeMd).not.toBeNull();
    expect(claudeMd).toMatch(/test-folder-protection\.md/);
  });
});

// ---------------------------------------------------------------------------
// AC#3: HALT Fires for Unauthorized Test Modification
// ---------------------------------------------------------------------------
describe('AC#3: HALT Fires for Unauthorized Test Modification', () => {
  let content;

  beforeAll(() => {
    content = readFileOrNull(RULE_FILE);
  });

  test('test_should_contain_halt_instruction_for_unauthorized_agents_when_rule_read', () => {
    expect(content).not.toBeNull();
    expect(content).toMatch(/HALT/);
    // Must mention halting for agents that are NOT authorized
    expect(content.toLowerCase()).toMatch(/unauthorized|not authorized|non-authorized/i);
  });

  test('test_should_require_askuserquestion_before_proceeding_when_halt_triggered', () => {
    expect(content).not.toBeNull();
    // Rule must instruct agent to use AskUserQuestion and wait for approval
    expect(content).toMatch(/AskUserQuestion/);
    expect(content.toLowerCase()).toMatch(/approval|permission|consent/i);
  });

  test('test_should_cover_write_and_edit_operations_when_halt_conditions_listed', () => {
    expect(content).not.toBeNull();
    expect(content).toMatch(/Write\(\)/i);
    expect(content).toMatch(/Edit\(\)/i);
  });
});

// ---------------------------------------------------------------------------
// AC#4: test-automator Permitted During Phase 02
// ---------------------------------------------------------------------------
describe('AC#4: test-automator Permitted During Phase 02', () => {
  let content;

  beforeAll(() => {
    content = readFileOrNull(RULE_FILE);
  });

  test('test_should_explicitly_permit_test_automator_when_phase_02_active', () => {
    expect(content).not.toBeNull();
    // Must mention test-automator AND Phase 02 together as permitted
    expect(content).toMatch(/test-automator/);
    expect(content).toMatch(/Phase\s*0?2/i);
  });

  test('test_should_not_halt_for_test_automator_during_phase_02_when_rule_parsed', () => {
    expect(content).not.toBeNull();
    // The rule must declare test-automator as permitted/authorized during Phase 02
    const lines = content.split('\n');
    const hasPermission = lines.some(
      (line) => /test-automator/i.test(line) && /permit|allow|authorized|exempt/i.test(line)
    );
    expect(hasPermission).toBe(true);
  });
});

// ---------------------------------------------------------------------------
// AC#5: integration-tester Permitted During Phase 05
// ---------------------------------------------------------------------------
describe('AC#5: integration-tester Permitted During Phase 05', () => {
  let content;

  beforeAll(() => {
    content = readFileOrNull(RULE_FILE);
  });

  test('test_should_explicitly_permit_integration_tester_when_phase_05_active', () => {
    expect(content).not.toBeNull();
    expect(content).toMatch(/integration-tester/);
    expect(content).toMatch(/Phase\s*0?5/i);
  });

  test('test_should_not_halt_for_integration_tester_during_phase_05_when_rule_parsed', () => {
    expect(content).not.toBeNull();
    const lines = content.split('\n');
    const hasPermission = lines.some(
      (line) => /integration-tester/i.test(line) && /permit|allow|authorized|exempt/i.test(line)
    );
    expect(hasPermission).toBe(true);
  });
});

// ---------------------------------------------------------------------------
// AC#6: CLAUDE.md Conditional Rules Table Updated
// ---------------------------------------------------------------------------
describe('AC#6: CLAUDE.md Conditional Rules Table Updated', () => {
  let claudeMd;

  beforeAll(() => {
    claudeMd = readFileOrNull(CLAUDE_MD);
  });

  test('test_should_have_entry_for_test_folder_protection_when_conditional_rules_table_read', () => {
    expect(claudeMd).not.toBeNull();
    // Must appear in the conditional rules section/table
    expect(claudeMd).toMatch(/test-folder-protection\.md/);
  });

  test('test_should_include_test_path_patterns_in_entry_when_conditional_rules_parsed', () => {
    expect(claudeMd).not.toBeNull();
    // The conditional rules entry must reference test file patterns
    // Look for the entry line that contains both the rule name and test patterns
    const lines = claudeMd.split('\n');
    const entryLine = lines.find((line) => line.includes('test-folder-protection'));
    expect(entryLine).toBeDefined();
    // Must cover tests/** or *.test.* or *.spec.* patterns
    expect(entryLine).toMatch(/tests\/|\.test\.|\.spec\./);
  });
});

// ---------------------------------------------------------------------------
// Technical Spec: Required Keys Verification
// ---------------------------------------------------------------------------
describe('Technical Spec: Required Keys in Rule File', () => {
  let content;

  beforeAll(() => {
    content = readFileOrNull(RULE_FILE);
  });

  test('test_should_contain_halt_trigger_section_when_required_keys_checked', () => {
    expect(content).not.toBeNull();
    // Must have a section/heading about HALT triggers
    expect(content).toMatch(/#+\s*.*halt.*trigger/i);
  });

  test('test_should_contain_authorized_agents_section_when_required_keys_checked', () => {
    expect(content).not.toBeNull();
    expect(content).toMatch(/#+\s*.*authorized.*agent/i);
  });

  test('test_should_contain_test_path_patterns_when_required_keys_checked', () => {
    expect(content).not.toBeNull();
    // All required patterns from tech spec
    expect(content).toMatch(/tests\/\*\*/);
    expect(content).toMatch(/\*\.test\.\*/);
    expect(content).toMatch(/\*\.spec\.\*/);
    expect(content).toMatch(/test_\*\.py/);
    expect(content).toMatch(/\*_test\.py/);
  });

  test('test_should_contain_askuserquestion_protocol_section_when_required_keys_checked', () => {
    expect(content).not.toBeNull();
    expect(content).toMatch(/#+\s*.*AskUserQuestion/i);
  });
});

// ---------------------------------------------------------------------------
// NFR Tests: Non-Functional Requirements
// ---------------------------------------------------------------------------
describe('NFR: Non-Functional Requirements', () => {
  let content;

  beforeAll(() => {
    content = readFileOrNull(RULE_FILE);
  });

  test('test_should_be_between_50_and_300_lines_when_line_count_checked', () => {
    expect(content).not.toBeNull();
    const lineCount = content.split('\n').length;
    expect(lineCount).toBeGreaterThanOrEqual(50);
    expect(lineCount).toBeLessThanOrEqual(300);
  });

  test('test_should_not_mention_override_or_bypass_flag_when_content_scanned', () => {
    expect(content).not.toBeNull();
    // No override/bypass/force flag should exist
    expect(content.toLowerCase()).not.toMatch(/--override/);
    expect(content.toLowerCase()).not.toMatch(/--bypass/);
    expect(content.toLowerCase()).not.toMatch(/--force/);
    expect(content.toLowerCase()).not.toMatch(/--no-verify/);
  });
});
