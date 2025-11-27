#!/usr/bin/env node

/**
 * DevForgeAI CLI Entry Point
 *
 * This is a minimal Node.js wrapper that invokes the Python installer subprocess.
 * Zero external npm dependencies for minimal installation footprint.
 *
 * Business logic extracted to ../lib/cli.js for testability and coverage collection.
 */

const cli = require('../lib/cli');

/**
 * Main entry point function (exported for testing)
 * @param {string[]} argv - Command-line arguments
 * @returns {Promise<number>} Exit code
 */
async function main(argv) {
  try {
    const result = await cli.run(argv);

    // cli.run() returns Promise<number> or number
    // await resolves Promise to number before this check
    // result is always a number here (never a Promise object)
    if (typeof result === 'number') {
      return result;
    }

    // Defensive fallback (should never reach here)
    return 0;
  } catch (error) {
    // Error thrown by lib/cli.js (from exitWithError)
    if (process.env.NODE_ENV !== 'test') {
      console.error(error.message);
    }
    return error.exitCode || 1;
  }
}

// Export for testing
module.exports = { main };

// Run if executed directly (not imported)
if (require.main === module) {
  main(process.argv.slice(2)).then(exitCode => {
    process.exit(exitCode);
  });
}
