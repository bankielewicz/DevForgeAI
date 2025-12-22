/**
 * PromptService - Interactive prompts for wizard
 *
 * Displays prompts using Inquirer.js for user input.
 * Handles validation, error messages, and TTY requirements.
 *
 * @class PromptService
 */

const inquirer = require('inquirer');

class PromptService {
  constructor(options = {}) {
    this.outputFormatter = options.outputFormatter;
    this.validationFailureCount = {};
  }

  /**
   * Check if TTY is available (SVC-008)
   * @private
   * @throws {Error} If TTY not available
   */
  checkTTY() {
    if (!process.stdout.isTTY) {
      throw new Error(
        'Interactive prompts require TTY. Use --yes for non-interactive mode.'
      );
    }
  }

  /**
   * Track validation failure and handle 3-failure threshold
   * @private
   * @param {string} key - Validation field key
   * @param {string} errorMessage - Error message to return
   * @returns {string|boolean} Error message or true (accept default after 3 failures)
   */
  trackValidationFailure(key, errorMessage) {
    this.validationFailureCount[key] = (this.validationFailureCount[key] || 0) + 1;

    // After 3 failures, suggest using default
    if (this.validationFailureCount[key] >= 3) {
      this.outputFormatter.info(
        'Using default value after multiple validation failures'
      );
      delete this.validationFailureCount[key];
      return true; // Accept default
    }

    return errorMessage;
  }

  /**
   * Prompt for target directory (SVC-004)
   * @returns {Promise<string>} Selected directory path
   */
  async promptTargetDirectory() {
    this.checkTTY();

    const answer = await inquirer.prompt([
      {
        type: 'input',
        name: 'targetDirectory',
        message: 'Target directory (use arrow keys and Enter to confirm):',
        default: '.',
        validate: (input) => {
          // Empty path
          if (!input || input.trim() === '') {
            return this.trackValidationFailure('targetDirectory', 'Target directory cannot be empty');
          }

          // System directories
          const systemDirs = ['/', '/usr', '/etc', 'C:\\Windows'];
          if (systemDirs.includes(input)) {
            return this.trackValidationFailure('targetDirectory', 'Cannot install to system directory');
          }

          // Path length (Windows MAX_PATH)
          if (input.length > 260) {
            return this.trackValidationFailure('targetDirectory', 'Path exceeds maximum length (260 characters)');
          }

          // Validation passed - reset failure counter
          delete this.validationFailureCount['targetDirectory'];
          return true;
        },
      },
    ]);

    return answer.targetDirectory;
  }

  /**
   * Prompt for installation mode (SVC-005)
   * @returns {Promise<string>} Selected mode (minimal, standard, full)
   */
  async promptInstallationMode() {
    this.checkTTY();

    const answer = await inquirer.prompt([
      {
        type: 'list',
        name: 'installationMode',
        message: 'Select installation mode (use arrow keys, press Enter):',
        choices: [
          {
            name: 'Minimal - Essential framework files only',
            value: 'minimal',
          },
          {
            name: 'Standard - Recommended setup with common tools',
            value: 'standard',
          },
          {
            name: 'Full - Complete framework with all features',
            value: 'full',
          },
        ],
        default: 'standard',
      },
    ]);

    return answer.installationMode;
  }

  /**
   * Prompt for merge strategy (SVC-006)
   * @returns {Promise<string>} Selected strategy
   */
  async promptMergeStrategy() {
    this.checkTTY();

    const answer = await inquirer.prompt([
      {
        type: 'list',
        name: 'mergeStrategy',
        message:
          'Select CLAUDE.md merge strategy (use arrow keys, press Enter):',
        choices: [
          {
            name: 'Preserve User - Keep existing CLAUDE.md unchanged',
            value: 'preserve-user',
          },
          {
            name: 'Merge Smart - Intelligently merge user and framework content',
            value: 'merge-smart',
          },
          {
            name: 'Replace - Overwrite with DevForgeAI template',
            value: 'replace',
          },
        ],
        default: 'merge-smart',
      },
    ]);

    return answer.mergeStrategy;
  }

  /**
   * Prompt for confirmation (SVC-007)
   * @param {Object} options - Confirmation options
   * @param {string} options.message - Confirmation message
   * @param {Array<string|Object>} options.affectedFiles - Files that will be affected
   * @returns {Promise<boolean>} True if confirmed
   */
  async promptConfirmation(options) {
    this.checkTTY();

    const { message, affectedFiles } = options;

    // Display affected files with warning color
    if (affectedFiles && affectedFiles.length > 0) {
      affectedFiles.forEach((file) => {
        if (typeof file === 'string') {
          this.outputFormatter.warning(`  - ${file}`);
        } else if (file.path && file.lines) {
          this.outputFormatter.warning(
            `  - ${file.path} (${file.lines} lines)`
          );
        }
      });
    }

    const answer = await inquirer.prompt([
      {
        type: 'confirm',
        name: 'confirm',
        message,
        default: false, // Default to No for destructive actions
      },
    ]);

    return answer.confirm;
  }
}

module.exports = { PromptService };
