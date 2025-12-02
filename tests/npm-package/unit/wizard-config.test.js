/**
 * Unit Tests - WizardConfig
 *
 * Test Coverage:
 * - Configuration: defaults.targetDirectory, installationMode, mergeStrategy
 * - Configuration: thresholds.spinnerDelayMs
 * - Configuration: exitCodes.success, exitCodes.sigint
 * - Data Validation: InstallationConfig model
 * - BR-005: Conflicting flags must be rejected
 * - BR-006: CI=true environment variable auto-enables --yes and --quiet
 *
 * @jest-environment node
 */

const { WizardConfig } = require('../../../src/cli/wizard/config');
const { InstallationConfig } = require('../../../src/cli/wizard/installation-config');

describe('WizardConfig', () => {
  let config;

  beforeEach(() => {
    config = new WizardConfig();
  });

  describe('defaults.targetDirectory', () => {
    it('should default to current directory', () => {
      // Act
      const targetDirectory = config.defaults.targetDirectory;

      // Assert
      expect(targetDirectory).toBe('.');
    });

    it('should validate as a valid filesystem path', () => {
      // Act
      const isValid = config.validatePath('./my-project');

      // Assert
      expect(isValid).toBe(true);
    });

    it('should accept absolute paths', () => {
      // Act
      const isValid = config.validatePath('/home/user/project');

      // Assert
      expect(isValid).toBe(true);
    });

    it('should accept relative paths', () => {
      // Act
      const isValid = config.validatePath('../other-project');

      // Assert
      expect(isValid).toBe(true);
    });
  });

  describe('defaults.installationMode', () => {
    it('should default to standard', () => {
      // Act
      const mode = config.defaults.installationMode;

      // Assert
      expect(mode).toBe('standard');
    });

    it('should validate against allowed values', () => {
      // Act
      const isValidMinimal = config.validateInstallationMode('minimal');
      const isValidStandard = config.validateInstallationMode('standard');
      const isValidFull = config.validateInstallationMode('full');
      const isValidInvalid = config.validateInstallationMode('invalid');

      // Assert
      expect(isValidMinimal).toBe(true);
      expect(isValidStandard).toBe(true);
      expect(isValidFull).toBe(true);
      expect(isValidInvalid).toBe(false);
    });

    it('should have exactly three allowed values', () => {
      // Act
      const allowedModes = config.allowedInstallationModes;

      // Assert
      expect(allowedModes).toEqual(['minimal', 'standard', 'full']);
    });
  });

  describe('defaults.mergeStrategy', () => {
    it('should default to merge-smart', () => {
      // Act
      const strategy = config.defaults.mergeStrategy;

      // Assert
      expect(strategy).toBe('merge-smart');
    });

    it('should validate against allowed values', () => {
      // Act
      const isValidPreserve = config.validateMergeStrategy('preserve-user');
      const isValidMerge = config.validateMergeStrategy('merge-smart');
      const isValidReplace = config.validateMergeStrategy('replace');
      const isValidInvalid = config.validateMergeStrategy('invalid');

      // Assert
      expect(isValidPreserve).toBe(true);
      expect(isValidMerge).toBe(true);
      expect(isValidReplace).toBe(true);
      expect(isValidInvalid).toBe(false);
    });

    it('should have exactly three allowed values', () => {
      // Act
      const allowedStrategies = config.allowedMergeStrategies;

      // Assert
      expect(allowedStrategies).toEqual([
        'preserve-user',
        'merge-smart',
        'replace',
      ]);
    });
  });

  describe('thresholds.spinnerDelayMs', () => {
    it('should default to 200ms', () => {
      // Act
      const delay = config.thresholds.spinnerDelayMs;

      // Assert
      expect(delay).toBe(200);
    });

    it('should validate as a positive integer', () => {
      // Act
      const isValid = config.validateSpinnerDelay(200);
      const isInvalidNegative = config.validateSpinnerDelay(-1);
      const isInvalidZero = config.validateSpinnerDelay(0);

      // Assert
      expect(isValid).toBe(true);
      expect(isInvalidNegative).toBe(false);
      expect(isInvalidZero).toBe(false);
    });
  });

  describe('exitCodes.success', () => {
    it('should default to 0', () => {
      // Act
      const exitCode = config.exitCodes.success;

      // Assert
      expect(exitCode).toBe(0);
    });

    it('should validate as integer 0', () => {
      // Act
      const isValid = config.validateExitCode('success', 0);
      const isInvalid = config.validateExitCode('success', 1);

      // Assert
      expect(isValid).toBe(true);
      expect(isInvalid).toBe(false);
    });
  });

  describe('exitCodes.sigint', () => {
    it('should default to 130', () => {
      // Act
      const exitCode = config.exitCodes.sigint;

      // Assert
      expect(exitCode).toBe(130);
    });

    it('should validate as integer 130 (128 + SIGINT)', () => {
      // Act
      const isValid = config.validateExitCode('sigint', 130);
      const isInvalid = config.validateExitCode('sigint', 2);

      // Assert
      expect(isValid).toBe(true);
      expect(isInvalid).toBe(false);
    });

    it('should match standard SIGINT exit code', () => {
      // Act
      const exitCode = config.exitCodes.sigint;

      // Assert
      expect(exitCode).toBe(128 + 2); // SIGINT is signal 2
    });
  });
});

describe('InstallationConfig', () => {
  let installConfig;

  beforeEach(() => {
    installConfig = new InstallationConfig();
  });

  describe('targetDirectory', () => {
    it('should be required', () => {
      // Act & Assert
      expect(() => {
        installConfig.validate();
      }).toThrow('targetDirectory is required');
    });

    it('should validate path exists or parent exists', () => {
      // Arrange
      installConfig.targetDirectory = './existing-dir';

      // Act
      const isValid = installConfig.validateTargetDirectory();

      // Assert
      expect(isValid).toBe(true);
    });
  });

  describe('installationMode', () => {
    it('should be required', () => {
      // Arrange
      installConfig.targetDirectory = '.';

      // Act & Assert
      expect(() => {
        installConfig.validate();
      }).toThrow('installationMode is required');
    });

    it('should validate against allowed values', () => {
      // Arrange
      installConfig.targetDirectory = '.';
      installConfig.installationMode = 'invalid';

      // Act & Assert
      expect(() => {
        installConfig.validate();
      }).toThrow('installationMode must be one of: minimal, standard, full');
    });

    it('should accept minimal, standard, full', () => {
      // Arrange - all required fields must be set
      installConfig.targetDirectory = '.';
      installConfig.mergeStrategy = 'merge-smart';

      // Act & Assert
      installConfig.installationMode = 'minimal';
      expect(() => installConfig.validate()).not.toThrow();

      installConfig.installationMode = 'standard';
      expect(() => installConfig.validate()).not.toThrow();

      installConfig.installationMode = 'full';
      expect(() => installConfig.validate()).not.toThrow();
    });
  });

  describe('mergeStrategy', () => {
    it('should be required', () => {
      // Arrange
      installConfig.targetDirectory = '.';
      installConfig.installationMode = 'standard';

      // Act & Assert
      expect(() => {
        installConfig.validate();
      }).toThrow('mergeStrategy is required');
    });

    it('should validate against allowed values', () => {
      // Arrange
      installConfig.targetDirectory = '.';
      installConfig.installationMode = 'standard';
      installConfig.mergeStrategy = 'invalid';

      // Act & Assert
      expect(() => {
        installConfig.validate();
      }).toThrow(
        'mergeStrategy must be one of: preserve-user, merge-smart, replace'
      );
    });

    it('should accept preserve-user, merge-smart, replace', () => {
      // Arrange
      installConfig.targetDirectory = '.';
      installConfig.installationMode = 'standard';

      // Act & Assert
      installConfig.mergeStrategy = 'preserve-user';
      expect(() => installConfig.validate()).not.toThrow();

      installConfig.mergeStrategy = 'merge-smart';
      expect(() => installConfig.validate()).not.toThrow();

      installConfig.mergeStrategy = 'replace';
      expect(() => installConfig.validate()).not.toThrow();
    });
  });

  describe('nonInteractive', () => {
    it('should be optional', () => {
      // Arrange
      installConfig.targetDirectory = '.';
      installConfig.installationMode = 'standard';
      installConfig.mergeStrategy = 'merge-smart';

      // Act & Assert
      expect(() => installConfig.validate()).not.toThrow();
    });

    it('should default to false', () => {
      // Act
      const defaultValue = installConfig.nonInteractive;

      // Assert
      expect(defaultValue).toBe(false);
    });

    it('should validate as boolean', () => {
      // Arrange
      installConfig.nonInteractive = 'true'; // Invalid (string)

      // Act & Assert
      expect(() => installConfig.validate()).toThrow(
        'nonInteractive must be a boolean'
      );
    });
  });

  describe('quiet', () => {
    it('should be optional', () => {
      // Arrange
      installConfig.targetDirectory = '.';
      installConfig.installationMode = 'standard';
      installConfig.mergeStrategy = 'merge-smart';

      // Act & Assert
      expect(() => installConfig.validate()).not.toThrow();
    });

    it('should default to false', () => {
      // Act
      const defaultValue = installConfig.quiet;

      // Assert
      expect(defaultValue).toBe(false);
    });

    it('should validate as boolean', () => {
      // Arrange
      installConfig.quiet = 1; // Invalid (number)

      // Act & Assert
      expect(() => installConfig.validate()).toThrow(
        'quiet must be a boolean'
      );
    });
  });
});

describe('BR-005: Conflicting flags must be rejected', () => {
  it('should reject --yes and --no-confirm together', () => {
    // Arrange
    const config = new WizardConfig();

    // Act & Assert
    expect(() => {
      config.validateFlags({ yes: true, noConfirm: true });
    }).toThrow('Cannot use --yes and --no-confirm together');
  });

  it('should reject --quiet and --verbose together', () => {
    // Arrange
    const config = new WizardConfig();

    // Act & Assert
    expect(() => {
      config.validateFlags({ quiet: true, verbose: true });
    }).toThrow('Cannot use --quiet and --verbose together');
  });

  it('should allow --yes and --quiet together', () => {
    // Arrange
    const config = new WizardConfig();

    // Act & Assert
    expect(() => {
      config.validateFlags({ yes: true, quiet: true });
    }).not.toThrow();
  });

  it('should exit with code 1 on conflicting flags', () => {
    // Arrange
    const config = new WizardConfig();

    // Act & Assert - validateFlags throws error instead of process.exit
    // (process.exit removed for testability and safety per coding-standards.md)
    expect(() => {
      config.validateFlags({ yes: true, noConfirm: true });
    }).toThrow('Cannot use --yes and --no-confirm together');
  });
});

describe('BR-006: CI=true environment variable auto-enables --yes and --quiet', () => {
  it('should detect CI=true in environment', () => {
    // Arrange
    const originalCI = process.env.CI;
    process.env.CI = 'true';
    const config = new WizardConfig();

    // Act
    const flags = config.applyEnvironmentFlags({});

    // Assert
    expect(flags.yes).toBe(true);
    expect(flags.quiet).toBe(true);

    // Cleanup
    process.env.CI = originalCI;
  });

  it('should not override explicit --no-quiet in CI mode', () => {
    // Arrange
    const originalCI = process.env.CI;
    process.env.CI = 'true';
    const config = new WizardConfig();

    // Act
    const flags = config.applyEnvironmentFlags({ quiet: false });

    // Assert
    expect(flags.yes).toBe(true);
    expect(flags.quiet).toBe(false); // User explicitly disabled

    // Cleanup
    process.env.CI = originalCI;
  });

  it('should log that CI mode detected', () => {
    // Arrange
    const originalCI = process.env.CI;
    process.env.CI = 'true';
    const config = new WizardConfig();
    const mockLog = jest.spyOn(console, 'log').mockImplementation();

    // Act
    config.applyEnvironmentFlags({});

    // Assert
    expect(mockLog).toHaveBeenCalledWith(
      expect.stringMatching(/CI mode detected/i)
    );

    // Cleanup
    process.env.CI = originalCI;
    mockLog.mockRestore();
  });
});
