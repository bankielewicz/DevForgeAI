/**
 * DevForgeAI CLI Logic Module
 *
 * Commander-based CLI with install, status, uninstall commands.
 * Replaces the previous Python subprocess delegation.
 */

const path = require('path');
const fs = require('fs');
const { Command } = require('commander');

// Constants (preserved from original for backward compatibility)
const MINIMUM_PYTHON_MAJOR = 3;
const MINIMUM_PYTHON_MINOR = 10;
const PYTHON_DOWNLOAD_URL = 'https://www.python.org';
const GITHUB_REPO_URL = 'https://github.com/bankielewicz/DevForgeAI';
const HELP_FOOTER = '\nFor help, run: devforgeai --help';

/**
 * Get package version from package.json
 */
function getVersion() {
  const packageJsonPath = path.join(__dirname, '..', 'package.json');
  const packageJson = JSON.parse(fs.readFileSync(packageJsonPath, 'utf8'));
  return packageJson.version;
}

/**
 * Parse Python version from version string
 */
function parsePythonVersion(versionString) {
  const versionMatch = versionString.match(/Python (\d+)\.(\d+)/);
  if (!versionMatch) return null;
  return {
    major: parseInt(versionMatch[1], 10),
    minor: parseInt(versionMatch[2], 10),
  };
}

/**
 * Check if Python version meets minimum requirements
 */
function isPythonVersionValid(version) {
  if (!version) return false;
  return (
    version.major > MINIMUM_PYTHON_MAJOR ||
    (version.major === MINIMUM_PYTHON_MAJOR && version.minor >= MINIMUM_PYTHON_MINOR)
  );
}

/**
 * Check for Python availability and version
 * @returns {object} Python command info
 * @throws {Error} If Python not found or version invalid
 */
function checkPython() {
  const { execSync } = require('child_process');
  let pythonVersionOutput;
  let pythonCommand;

  const pythonCommands = ['python3', 'python'];
  for (const cmd of pythonCommands) {
    try {
      pythonVersionOutput = execSync(`${cmd} --version`, {
        encoding: 'utf8',
        stdio: 'pipe',
      }).trim();
      pythonCommand = cmd;
      break;
    } catch (error) {
      // Continue to next
    }
  }

  if (!pythonVersionOutput) {
    const error = new Error(
      `Python ${MINIMUM_PYTHON_MAJOR}.${MINIMUM_PYTHON_MINOR}+ required but not found.`
    );
    error.exitCode = 1;
    throw error;
  }

  const version = parsePythonVersion(pythonVersionOutput);
  if (!isPythonVersionValid(version)) {
    const versionString = version ? `${version.major}.${version.minor}` : 'unknown';
    const error = new Error(
      `Python version mismatch. Found: ${versionString}, required: ${MINIMUM_PYTHON_MAJOR}.${MINIMUM_PYTHON_MINOR}+`
    );
    error.exitCode = 1;
    throw error;
  }

  return { command: pythonCommand, version };
}

/**
 * Create and configure the Commander program
 */
function createProgram() {
  const program = new Command();

  program
    .name('devforgeai')
    .description('DevForgeAI — Spec-Driven Development Framework')
    .version(getVersion(), '-v, --version');

  // Load commands from src/cli/commands/
  const commandsDir = path.join(__dirname, '..', 'src', 'cli', 'commands');

  if (fs.existsSync(commandsDir)) {
    const commandFiles = fs.readdirSync(commandsDir).filter(f => f.endsWith('.js'));

    for (const file of commandFiles) {
      const cmd = require(path.join(commandsDir, file));
      const sub = program.command(cmd.command).description(cmd.description);

      if (cmd.options) {
        for (const opt of cmd.options) {
          sub.option(...opt);
        }
      }

      sub.action(cmd.action);
    }
  }

  return program;
}

/**
 * Main CLI entry point
 * @param {string[]} argv - Command-line arguments (process.argv.slice(2))
 * @param {object} options - Options for testability
 * @returns {Promise<number>} Exit code
 */
async function run(argv, options = {}) {
  const program = createProgram();

  try {
    await program.parseAsync(['node', 'devforgeai', ...argv]);
    return 0;
  } catch (error) {
    if (error.exitCode !== undefined) {
      return error.exitCode;
    }
    return 1;
  }
}

module.exports = {
  getVersion,
  parsePythonVersion,
  isPythonVersionValid,
  checkPython,
  createProgram,
  run,
  MINIMUM_PYTHON_MAJOR,
  MINIMUM_PYTHON_MINOR,
  PYTHON_DOWNLOAD_URL,
  GITHUB_REPO_URL,
  HELP_FOOTER,
};
