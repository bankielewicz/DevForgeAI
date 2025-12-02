/**
 * InstallWizard - Main wizard orchestration service
 *
 * Orchestrates the installation wizard flow: prompts → validation → installation.
 * Handles --yes (non-interactive) and --quiet flags.
 *
 * @class InstallWizard
 */

const { WizardConfig } = require('./config');

class InstallWizard {
  constructor(options = {}) {
    this.promptService = options.promptService;
    this.progressService = options.progressService;
    this.outputFormatter = options.outputFormatter;
    this.installer = options.installer;
    this.signalHandler = options.signalHandler;
    this.config = new WizardConfig();
  }

  /**
   * Run the installation wizard (SVC-001, SVC-002, SVC-003)
   *
   * @param {Object} options - Command-line options
   * @param {boolean} options.yes - Skip prompts and use defaults
   * @param {boolean} options.quiet - Suppress non-error output
   * @returns {Promise<Object>} Installation configuration
   */
  async run(options = {}) {
    const { yes, quiet } = options;

    try {
      // BR-001: Non-TTY requires --yes flag
      if (!process.stdout.isTTY && !yes) {
        const error = new Error(
          'Interactive prompts require TTY. Use --yes for non-interactive mode.'
        );
        this.outputFormatter.error(error.message);
        throw error;
      }

      let installConfig;

      if (yes) {
        // SVC-002: Skip prompts with --yes flag
        installConfig = this.getDefaultConfig(yes, quiet);
      } else {
        // SVC-001: Display prompts in sequence
        installConfig = await this.collectUserInput(yes, quiet);
      }

      // Check if confirmation needed for destructive actions
      if (!yes && this.requiresConfirmation(installConfig)) {
        const confirmed = await this.promptService.promptConfirmation({
          message:
            'This will overwrite existing files. Continue? (use arrow keys, press Enter)',
          default: false,
          affectedFiles: ['CLAUDE.md'],
        });

        if (!confirmed) {
          // User declined confirmation
          if (!quiet) {
            this.outputFormatter.warning('Installation cancelled by user');
          }
          return installConfig;
        }
      }

      // Perform installation
      if (this.installer) {
        await this.installer.install({
          targetDirectory: installConfig.targetDirectory,
          installationMode: installConfig.installationMode,
          mergeStrategy: installConfig.mergeStrategy,
        });
      }

      // SVC-003: Suppress success message with --quiet flag
      if (!quiet) {
        this.outputFormatter.success('✓ Installation complete');
      }

      return installConfig;
    } catch (error) {
      // Display error (always shown, even in quiet mode)
      this.outputFormatter.error(error.message);

      throw error;
    }
  }

  /**
   * Get default configuration for --yes mode
   * @private
   * @param {boolean} yes - Non-interactive flag
   * @param {boolean} quiet - Quiet flag
   * @returns {Object} Default configuration
   */
  getDefaultConfig(yes, quiet) {
    return {
      targetDirectory: this.config.defaults.targetDirectory,
      installationMode: this.config.defaults.installationMode,
      mergeStrategy: this.config.defaults.mergeStrategy,
      nonInteractive: yes,
      quiet: quiet,
    };
  }

  /**
   * Collect user input through prompts
   * @private
   * @param {boolean} yes - Non-interactive flag
   * @param {boolean} quiet - Quiet flag
   * @returns {Promise<Object>} User-selected configuration
   */
  async collectUserInput(yes, quiet) {
    // Prompt in sequence
    const targetDirectory = await this.promptService.promptTargetDirectory();
    const installationMode = await this.promptService.promptInstallationMode();
    const mergeStrategy = await this.promptService.promptMergeStrategy();

    return {
      targetDirectory,
      installationMode,
      mergeStrategy,
      nonInteractive: yes,
      quiet: quiet,
    };
  }

  /**
   * Check if configuration requires confirmation
   * @private
   * @param {Object} config - Installation configuration
   * @returns {boolean} True if confirmation needed
   */
  requiresConfirmation(config) {
    // Destructive actions require confirmation
    return (
      config.mergeStrategy === 'replace' || config.installationMode === 'full'
    );
  }
}

module.exports = { InstallWizard };
