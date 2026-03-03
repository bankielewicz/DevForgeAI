/**
 * InstallationConfig - Data model for installation configuration
 *
 * Represents user-selected installation options with validation.
 * This model ensures configuration data meets all business rules before installation.
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
    // Boolean field validation (check these first since they have default values)
    if (typeof this.nonInteractive !== 'boolean') {
      throw new Error('nonInteractive must be a boolean');
    }

    if (typeof this.quiet !== 'boolean') {
      throw new Error('quiet must be a boolean');
    }

    // Required fields
    if (!this.targetDirectory) {
      throw new Error('targetDirectory is required');
    }

    if (!this.installationMode) {
      throw new Error('installationMode is required');
    }

    // Field validation - installationMode
    const allowedModes = ['minimal', 'standard', 'full'];
    if (this.installationMode && !allowedModes.includes(this.installationMode)) {
      throw new Error(
        `installationMode must be one of: ${allowedModes.join(', ')}`
      );
    }

    if (!this.mergeStrategy) {
      throw new Error('mergeStrategy is required');
    }

    // Field validation - mergeStrategy
    const allowedStrategies = ['preserve-user', 'merge-smart', 'replace'];
    if (this.mergeStrategy && !allowedStrategies.includes(this.mergeStrategy)) {
      throw new Error(
        `mergeStrategy must be one of: ${allowedStrategies.join(', ')}`
      );
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

module.exports = { InstallationConfig };
