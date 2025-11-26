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

// Run CLI with command-line arguments
(async () => {
  try {
    const result = await cli.run(process.argv.slice(2));

    // If result is a number (exit code), exit with that code
    if (typeof result === 'number') {
      process.exit(result);
    }

    // If result is a Promise (resolves to exit code), wait and exit
    if (result && typeof result.then === 'function') {
      const exitCode = await result;
      process.exit(exitCode);
    }
  } catch (error) {
    // Error thrown by lib/cli.js (from exitWithError)
    console.error(error.message);
    process.exit(error.exitCode || 1);
  }
})();
