/**
 * STORY-496 AC#3: QA Phase 2 Invokes Diagnostic-Analyst on Coverage or Anti-Pattern Failures
 */
const fs = require('fs');
const path = require('path');

const QA_SKILL_PATH = path.join(__dirname, '..', '..', 'src', 'claude', 'skills', 'devforgeai-qa', 'SKILL.md');

describe('AC#3: QA Phase 2 Diagnostic Hook', () => {
  let content;

  beforeAll(() => {
    content = fs.readFileSync(QA_SKILL_PATH, 'utf8');
  });

  test('qa_phase2_hook_present_diagnostic_analyst_invoked', () => {
    // AC#3: diagnostic-analyst must be invoked in Phase 2
    expect(content).toMatch(/Phase 2[\s\S]*diagnostic-analyst/);
  });

  test('qa_phase2_hook_attaches_diagnosis_to_gaps_json', () => {
    // AC#3: Diagnosis output attached to gaps.json
    expect(content).toMatch(/gaps\.json[\s\S]*diagnos|diagnos[\s\S]*gaps\.json/i);
  });

  test('qa_phase2_hook_covers_coverage_and_antipattern_failures', () => {
    // AC#3: Aggregates both coverage and anti-pattern failures in diagnostic context
    expect(content).toMatch(/diagnostic-analyst[\s\S]{0,500}(coverage.*anti.pattern|anti.pattern.*coverage)/i);
  });
});
