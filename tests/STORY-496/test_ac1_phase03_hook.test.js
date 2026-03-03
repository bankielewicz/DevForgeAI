/**
 * STORY-496 AC#1: Phase 03 (Green) Invokes Root-Cause-Diagnosis on Test Failure
 * Tests validate that implementing-stories Phase 03 has diagnostic hook.
 */
const fs = require('fs');
const path = require('path');

const PHASE03_PATH = path.join(__dirname, '..', '..', 'src', 'claude', 'skills', 'implementing-stories', 'phases', 'phase-03-implementation.md');

describe('AC#1: Phase 03 Diagnostic Hook', () => {
  let content;

  beforeAll(() => {
    content = fs.readFileSync(PHASE03_PATH, 'utf8');
  });

  test('phase03_hook_present_root_cause_diagnosis_skill_invoked', () => {
    // AC#1: Skill("root-cause-diagnosis") must be invoked in Phase 03
    expect(content).toMatch(/root-cause-diagnosis/);
  });

  test('phase03_hook_wrapped_in_failure_conditional', () => {
    // BR-001: Hook only fires on failure (zero overhead on success)
    // Must find root-cause-diagnosis near a failure conditional
    expect(content).toMatch(/IF.*fail[\s\S]{0,500}root-cause-diagnosis|root-cause-diagnosis[\s\S]{0,500}IF.*fail/i);
  });

  test('phase03_hook_includes_failure_context', () => {
    // AC#5: Invocation includes test output, story_id, file paths
    expect(content).toMatch(/test.*(output|result|failure)/i);
  });

  test('phase03_hook_single_invocation_guard', () => {
    // BR-002: Maximum one diagnostic invocation per phase cycle
    expect(content).toMatch(/diagnosis_invoked|diagnostic_count|single.invocation|once.per.cycle|already.*diagnosed/i);
  });
});
