/**
 * DevForgeAI CLI Logic Module
 *
 * Testable CLI logic extracted from bin/devforgeai.js for coverage collection.
 * All business logic and functions are here; bin/devforgeai.js is a thin wrapper.
 */

const fs = require('fs');
const path = require('path');
const { spawn } = require('child_process');
const { execSync } = require('child_process');

// Constants
const MINIMUM_PYTHON_MAJOR = 3;
const MINIMUM_PYTHON_MINOR = 10;
const PYTHON_DOWNLOAD_URL = 'https://www.python.org';
const GITHUB_REPO_URL = 'https://github.com/bankielewicz/DevForgeAI';
const HELP_FOOTER = '\nFor help, run: devforgeai --help';

/**
 * Get package version from package.json
 * @returns {string} Version string
 */
function getVersion() {
  const packageJsonPath = path.join(__dirname, '..', 'package.json');
  const packageJson = JSON.parse(fs.readFileSync(packageJsonPath, 'utf8'));
  return packageJson.version;
}

/**
 * Display help message
 */
function displayHelp() {
  console.log(`devforgeai - DevForgeAI Framework Installer

Usage: devforgeai <command> [options]

Commands:
  install <path>    Install DevForgeAI framework to target directory
  --version         Display version number
  --help            Display this help message

Examples:
  devforgeai install .           Install to current directory
  devforgeai install /project    Install to /project directory

Documentation: ${GITHUB_REPO_URL}`);
}

/**
 * Parse Python version from version string
 * @param {string} versionString - e.g., "Python 3.10.11"
 * @returns {{major: number, minor: number} | null}
 */
function parsePythonVersion(versionString) {
  const versionMatch = versionString.match(/Python (\d+)\.(\d+)/);
  if (!versionMatch) return null;

  return {
    major: parseInt(versionMatch[1], 10),
    minor: parseInt(versionMatch[2], 10)
  };
}

/**
 * Check if Python version meets minimum requirements
 * @param {{major: number, minor: number}} version
 * @returns {boolean}
 */
function isPythonVersionValid(version) {
  if (!version) return false;

  return (
    version.major > MINIMUM_PYTHON_MAJOR ||
    (version.major === MINIMUM_PYTHON_MAJOR && version.minor >= MINIMUM_PYTHON_MINOR)
  );
}

/**
 * Display error message and throw
 * @param {string} title - Error title
 * @param {string} message - Error message
 * @throws {Error} Always throws for testability
 */
function exitWithError(title, message) {
  const errorMessage = `Error: ${title}\n\n${message}${HELP_FOOTER}`;
  const error = new Error(errorMessage);
  error.exitCode = 1;
  error.title = title;

  // Always throw (caller decides whether to process.exit or propagate)
  throw error;
}

/**
 * Check for Python availability and version
 * @returns {object} Python command info { command: 'python3'|'python', version: {...} }
 * @throws {Error} Exits with error if Python not found or version invalid
 */
function checkPython() {
  let pythonVersionOutput;
  let pythonCommand;

  // Try python3 first (Unix/Linux/macOS standard), then python (Windows standard)
  const pythonCommands = ['python3', 'python'];
  let lastError;

  for (const cmd of pythonCommands) {
    try {
      pythonVersionOutput = execSync(`${cmd} --version`, {
        encoding: 'utf8',
        stdio: 'pipe'
      }).trim();

      if (process.env.DEBUG_CLI) console.log(`[DEBUG] ${cmd} found:`, pythonVersionOutput);

      pythonCommand = cmd;
      break; // Found working Python command
    } catch (error) {
      if (process.env.DEBUG_CLI) console.log(`[DEBUG] ${cmd} not found:`, error.message);
      lastError = error;
      // Continue to next command
    }
  }

  // If no Python command worked, show error
  if (!pythonVersionOutput) {
    exitWithError(
      'Python 3.10+ required',
      `DevForgeAI requires Python ${MINIMUM_PYTHON_MAJOR}.${MINIMUM_PYTHON_MINOR} or newer to run the installer.

Resolution steps:
1. Install Python ${MINIMUM_PYTHON_MAJOR}.${MINIMUM_PYTHON_MINOR}+ from ${PYTHON_DOWNLOAD_URL}
2. Ensure 'python3' or 'python' is in your PATH
3. Verify installation: python3 --version (or python --version on Windows)`
    );
  }

  // Parse and validate version (outside try-catch so errors aren't caught)
  const version = parsePythonVersion(pythonVersionOutput);

  if (process.env.DEBUG_CLI) console.log('[DEBUG] parsed version:', version);

  if (!isPythonVersionValid(version)) {
    if (process.env.DEBUG_CLI) console.log('[DEBUG] Version invalid, throwing mismatch');

    const versionString = version ? `${version.major}.${version.minor}` : 'unknown';
    exitWithError(
      'Python version mismatch',
      `Found: Python ${versionString}
Required: Python ${MINIMUM_PYTHON_MAJOR}.${MINIMUM_PYTHON_MINOR}+

Please install Python ${MINIMUM_PYTHON_MAJOR}.${MINIMUM_PYTHON_MINOR} or newer from ${PYTHON_DOWNLOAD_URL}`
    );
  }

  return { command: pythonCommand, version };
}

/**
 * Invoke Python installer subprocess
 * @param {string[]} args - Command-line arguments
 * @param {string} pythonCommand - Python command to use ('python3' or 'python')
 * @returns {ChildProcess} Spawned Python process
 */
function invokePythonInstaller(args, pythonCommand = 'python3') {
  // Use -m to run installer as a module (solves relative import issues)
  // The installer package is at ../installer relative to this file
  const installerDir = path.join(__dirname, '..');
  const pythonArgs = ['-m', 'installer', ...args];

  const pythonProcess = spawn(pythonCommand, pythonArgs, {
    stdio: 'inherit',
    cwd: installerDir  // Run from package root so 'installer' module is found
  });

  pythonProcess.on('error', (error) => {
    exitWithError(
      'Failed to invoke Python installer',
      error.message
    );
  });

  return pythonProcess;
}

/**
 * Main CLI entry point
 * @param {string[]} argv - Command-line arguments (process.argv.slice(2))
 * @param {object} options - Options for testability
 * @param {boolean} options.exitOnCompletion - Whether to call process.exit (default: true)
 * @returns {number|ChildProcess|Promise<number>} Exit code or Python process
 */
function run(argv, options = {}) {
  const { exitOnCompletion = true } = options;

  // Handle --version flag
  if (argv.includes('--version') || argv.includes('-v')) {
    console.log(`devforgeai v${getVersion()}`);
    return 0;
  }

  // Handle --help flag or no arguments
  if (argv.includes('--help') || argv.includes('-h') || argv.length === 0) {
    displayHelp();
    return 0;
  }

  // Handle unknown commands (throws error)
  if (argv.length > 0 && argv[0] !== 'install') {
    exitWithError(
      'Unknown command',
      `'${argv[0]}' is not a recognized command.`
    );
  }

  // Check Python before invoking installer (throws on error, returns detected command)
  const pythonInfo = checkPython();

  // Invoke Python installer subprocess with detected Python command
  const pythonProcess = invokePythonInstaller(argv, pythonInfo.command);

  // If not exiting on completion, return process for testing
  if (!exitOnCompletion) {
    return pythonProcess;
  }

  // In production mode, wait for subprocess and exit with its code
  return new Promise((resolve) => {
    pythonProcess.on('close', (code) => {
      resolve(code || 0);
    });
  });
}

// Export for testing
module.exports = {
  getVersion,
  displayHelp,
  parsePythonVersion,
  isPythonVersionValid,
  checkPython,
  invokePythonInstaller,
  run,
  // Export constants for testing
  MINIMUM_PYTHON_MAJOR,
  MINIMUM_PYTHON_MINOR,
  PYTHON_DOWNLOAD_URL,
  GITHUB_REPO_URL,
  HELP_FOOTER
};
