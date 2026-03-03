/**
 * STORY-496 AC#2: Phase 05 (Integration) Invokes Diagnostic-Analyst on Integration Test Failure
 */
const fs = require('fs');
const path = require('path');

const PHASE05_PATH = path.join(__dirname, '..', '..', 'src', 'claude', 'skills', 'implementing-stories', 'phases', 'phase-05-integration.md');

describe('AC#2: Phase 05 Diagnostic Hook', () => {
  let content;

  beforeAll(() => {
    content = fs.readFileSync(PHASE05_PATH, 'utf8');
  });

  test('phase05_hook_present_diagnostic_analyst_invoked', () => {
    // AC#2: Task(subagent_type="diagnostic-analyst") must be invoked
    expect(content).toMatch(/diagnostic-analyst/);
  });

  test('phase05_hook_uses_task_subagent_invocation', () => {
    // AC#2: Must use Task() with correct subagent_type
    expect(content).toMatch(/Task\([\s\S]*subagent_type.*diagnostic-analyst/);
  });

  test('phase05_hook_graceful_skip_when_unavailable', () => {
    // BR-003: Graceful skip when diagnostic-analyst not available
    // Must be near diagnostic-analyst reference
    expect(content).toMatch(/diagnostic-analyst[\s\S]{0,500}(graceful|unavailable|fallback|skip)/i);
  });

  test('phase05_hook_includes_integration_test_output', () => {
    // AC#5: Integration test failure output passed as context to diagnostic-analyst
    expect(content).toMatch(/diagnostic-analyst[\s\S]{0,500}(integration.*output|failure.*output|test.*result)/i);
  });
});
