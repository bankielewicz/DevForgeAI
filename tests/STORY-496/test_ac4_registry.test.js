/**
 * STORY-496 AC#4: CLAUDE.md Subagent Registry Updated with Diagnostic-Analyst Entry
 */
const fs = require('fs');
const path = require('path');

const CLAUDE_MD_PATH = path.join(__dirname, '..', '..', 'src', 'CLAUDE.md');

describe('AC#4: CLAUDE.md Registry Updated', () => {
  let content;

  beforeAll(() => {
    content = fs.readFileSync(CLAUDE_MD_PATH, 'utf8');
  });

  test('registry_contains_diagnostic_analyst_row', () => {
    // AC#4: Registry table contains diagnostic-analyst row
    expect(content).toMatch(/\|\s*diagnostic-analyst\s*\|/);
  });

  test('registry_diagnostic_analyst_has_description', () => {
    // AC#4: Description field populated
    expect(content).toMatch(/diagnostic-analyst\s*\|.*investigation/i);
  });

  test('registry_diagnostic_analyst_has_tools', () => {
    // AC#4: Tools field includes Read, Grep, Glob
    expect(content).toMatch(/diagnostic-analyst\s*\|[^|]*\|[^|]*Read.*Grep.*Glob/);
  });

  test('registry_has_four_proactive_trigger_mappings', () => {
    // AC#4: At least 4 proactive trigger mappings for diagnostic-analyst
    const triggerMatches = content.match(/diagnostic-analyst/g) || [];
    // Need at minimum: registry row + 4 trigger mappings = 5 occurrences
    expect(triggerMatches.length).toBeGreaterThanOrEqual(5);
  });
});
