/**
 * WizardConfig - Configuration for Installation Wizard
 *
 * Provides default values, validation methods, and environment flag processing
 * for the DevForgeAI installation wizard.
 *
 * @class WizardConfig
 */

class WizardConfig {
  constructor() {
    this.defaults = {
      targetDirectory: '.',
      installationMode: 'standard',
      mergeStrategy: 'merge-smart',
    };

    this.thresholds = {
      spinnerDelayMs: 200,
    };

    this.exitCodes = {
      success: 0,
      sigint: 130, // 128 + SIGINT (signal 2)
    };

    this.allowedInstallationModes = ['minimal', 'standard', 'full'];
    this.allowedMergeStrategies = ['preserve-user', 'merge-smart', 'replace'];
  }

  /**
   * Validate filesystem path
   * @param {string} path - Path to validate
   * @returns {boolean} True if valid
   */
  validatePath(path) {
    if (!path || typeof path !== 'string') {
      return false;
    }
    return true; // Basic validation - actual file system checks done elsewhere
  }

  /**
   * Validate installation mode
   * @param {string} mode - Installation mode
   * @returns {boolean} True if valid
   */
  validateInstallationMode(mode) {
    return this.allowedInstallationModes.includes(mode);
  }

  /**
   * Validate merge strategy
   * @param {string} strategy - Merge strategy
   * @returns {boolean} True if valid
   */
  validateMergeStrategy(strategy) {
    return this.allowedMergeStrategies.includes(strategy);
  }

  /**
   * Validate spinner delay threshold
   * @param {number} delay - Delay in milliseconds
   * @returns {boolean} True if valid
   */
  validateSpinnerDelay(delay) {
    return typeof delay === 'number' && delay > 0;
  }

  /**
   * Validate exit code
   * @param {string} type - Exit code type ('success' or 'sigint')
   * @param {number} code - Exit code value
   * @returns {boolean} True if valid
   */
  validateExitCode(type, code) {
    if (type === 'success') {
      return code === 0;
    } else if (type === 'sigint') {
      return code === 130;
    }
    return false;
  }

  /**
   * Validate flag combinations (BR-005)
   * @param {Object} flags - Command-line flags
   * @throws {Error} If conflicting flags detected
   */
  validateFlags(flags) {
    // Check for conflicting flag combinations
    if (flags.yes && flags.noConfirm) {
      throw new Error('Cannot use --yes and --no-confirm together');
    }

    if (flags.quiet && flags.verbose) {
      throw new Error('Cannot use --quiet and --verbose together');
    }

    // --yes and --quiet together is VALID
  }

  /**
   * Apply environment variable flags (BR-006)
   * @param {Object} flags - Existing flags
   * @returns {Object} Updated flags with environment variables applied
   */
  applyEnvironmentFlags(flags) {
    const result = { ...flags };

    // CI=true auto-enables --yes and --quiet
    if (process.env.CI === 'true' || process.env.CI === '1') {
      console.log('CI mode detected: Enabling --yes and --quiet flags');

      // Apply defaults unless explicitly overridden
      if (result.yes === undefined) {
        result.yes = true;
      }

      if (result.quiet === undefined) {
        result.quiet = true;
      }
    }

    return result;
  }
}

/**
 * InstallationConfig - Data model for installation configuration
 *
 * Represents user-selected installation options with validation.
 *
 * @class InstallationConfig
 */
class InstallationConfig {
  constructor() {
    this.targetDirectory = null;
    this.installationMode = null;
    this.mergeStrategy = null;
    this.nonInteractive = false;
    this.quiet = false;
  }

  /**
   * Validate installation configuration
   * @throws {Error} If validation fails
   */
  validate() {
    // Required fields
    if (!this.targetDirectory) {
      throw new Error('targetDirectory is required');
    }

    if (!this.installationMode) {
      throw new Error('installationMode is required');
    }

    if (!this.mergeStrategy) {
      throw new Error('mergeStrategy is required');
    }

    // Field validation
    const allowedModes = ['minimal', 'standard', 'full'];
    if (!allowedModes.includes(this.installationMode)) {
      throw new Error(
        `installationMode must be one of: ${allowedModes.join(', ')}`
      );
    }

    const allowedStrategies = ['preserve-user', 'merge-smart', 'replace'];
    if (!allowedStrategies.includes(this.mergeStrategy)) {
      throw new Error(
        `mergeStrategy must be one of: ${allowedStrategies.join(', ')}`
      );
    }

    // Boolean field validation
    if (typeof this.nonInteractive !== 'boolean') {
      throw new Error('nonInteractive must be a boolean');
    }

    if (typeof this.quiet !== 'boolean') {
      throw new Error('quiet must be a boolean');
    }
  }

  /**
   * Validate target directory (placeholder - actual FS checks elsewhere)
   * @returns {boolean} True if valid
   */
  validateTargetDirectory() {
    return this.targetDirectory !== null && this.targetDirectory !== '';
  }
}

module.exports = { WizardConfig, InstallationConfig };
