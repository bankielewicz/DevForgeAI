/**
 * Custom Jest Test Sequencer for STORY-071
 *
 * Purpose:
 * - Run tests in test pyramid order: Unit → Integration → E2E
 * - Ensures fast feedback (unit tests fail first)
 * - Optimizes CI/CD pipeline execution
 */

const Sequencer = require('@jest/test-sequencer').default;

class CustomSequencer extends Sequencer {
  sort(tests) {
    // Create a copy of the tests array
    const copyTests = Array.from(tests);

    // Define test priority order
    const testOrder = {
      unit: 1,
      integration: 2,
      e2e: 3,
    };

    // Sort tests by type (unit → integration → e2e)
    return copyTests.sort((testA, testB) => {
      const typeA = this.getTestType(testA.path);
      const typeB = this.getTestType(testB.path);

      const priorityA = testOrder[typeA] || 999;
      const priorityB = testOrder[typeB] || 999;

      // Sort by priority
      if (priorityA !== priorityB) {
        return priorityA - priorityB;
      }

      // If same type, sort alphabetically by filename
      return testA.path.localeCompare(testB.path);
    });
  }

  getTestType(testPath) {
    if (testPath.includes('/unit/')) {
      return 'unit';
    } else if (testPath.includes('/integration/')) {
      return 'integration';
    } else if (testPath.includes('/e2e/')) {
      return 'e2e';
    }
    return 'unknown';
  }
}

module.exports = CustomSequencer;
