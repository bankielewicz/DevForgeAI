/**
 * STORY-496 AC#5: Diagnostic Context Passes Relevant Failure Data
 */
const fs = require('fs');
const path = require('path');

const PHASE03_PATH = path.join(__dirname, '..', '..', 'src', 'claude', 'skills', 'implementing-stories', 'phases', 'phase-03-implementation.md');
const PHASE05_PATH = path.join(__dirname, '..', '..', 'src', 'claude', 'skills', 'implementing-stories', 'phases', 'phase-05-integration.md');
const QA_SKILL_PATH = path.join(__dirname, '..', '..', 'src', 'claude', 'skills', 'devforgeai-qa', 'SKILL.md');

describe('AC#5: Diagnostic Context Passes Relevant Failure Data', () => {
  let phase03, phase05, qaSkill;

  beforeAll(() => {
    phase03 = fs.readFileSync(PHASE03_PATH, 'utf8');
    phase05 = fs.readFileSync(PHASE05_PATH, 'utf8');
    qaSkill = fs.readFileSync(QA_SKILL_PATH, 'utf8');
  });

  test('phase03_passes_test_output_in_diagnostic_context', () => {
    // AC#5: Phase 03 hook includes specific test output, not generic invocation
    expect(phase03).toMatch(/root-cause-diagnosis[\s\S]*?(test_output|test_result|failure_output|TEST_OUTPUT)/i);
  });

  test('phase05_passes_integration_output_in_diagnostic_context', () => {
    // AC#5: Phase 05 hook includes integration test output
    expect(phase05).toMatch(/diagnostic-analyst[\s\S]*?(integration.*output|failure.*output|test.*result)/i);
  });

  test('qa_phase2_passes_coverage_antipattern_results_in_context', () => {
    // AC#5: QA Phase 2 hook includes coverage or anti-pattern scan results
    expect(qaSkill).toMatch(/diagnostic-analyst[\s\S]*?(coverage|anti.pattern|violation|scan.*result)/i);
  });
});
