/**
 * Unit Tests - InstallWizard Service
 *
 * Test Coverage:
 * - SVC-001: Orchestrate wizard flow (prompts → validation → installation)
 * - SVC-002: Handle --yes flag to skip interactive prompts
 * - SVC-003: Handle --quiet flag to suppress non-error output
 * - BR-001: Non-TTY environments require --yes flag
 * - BR-003: --yes flag overrides all prompts with default values
 *
 * @jest-environment node
 */

const { InstallWizard } = require('../../../src/cli/wizard/install-wizard');

describe('InstallWizard', () => {
  let wizard;
  let mockPromptService;
  let mockProgressService;
  let mockOutputFormatter;
  let mockInstaller;

  beforeEach(() => {
    // Arrange: Create mocks for dependencies
    mockPromptService = {
      promptTargetDirectory: jest.fn().mockResolvedValue('./test-dir'),
      promptInstallationMode: jest.fn().mockResolvedValue('standard'),
      promptMergeStrategy: jest.fn().mockResolvedValue('merge-smart'),
      promptConfirmation: jest.fn().mockResolvedValue(true),
    };

    mockProgressService = {
      startSpinner: jest.fn(),
      stopSpinner: jest.fn(),
      startProgressBar: jest.fn(),
      updateProgress: jest.fn(),
      stopProgressBar: jest.fn(),
    };

    mockOutputFormatter = {
      success: jest.fn(),
      warning: jest.fn(),
      error: jest.fn(),
      info: jest.fn(),
    };

    mockInstaller = {
      install: jest.fn().mockResolvedValue({ success: true }),
    };

    wizard = new InstallWizard({
      promptService: mockPromptService,
      progressService: mockProgressService,
      outputFormatter: mockOutputFormatter,
      installer: mockInstaller,
    });
  });

  describe('SVC-001: Orchestrate wizard flow', () => {
    it('should display prompts in sequence', async () => {
      // Arrange
      const options = { yes: false, quiet: false };

      // Act
      await wizard.run(options);

      // Assert
      expect(mockPromptService.promptTargetDirectory).toHaveBeenCalled();
      expect(mockPromptService.promptInstallationMode).toHaveBeenCalled();
      expect(mockPromptService.promptMergeStrategy).toHaveBeenCalled();
    });

    it('should pass collected config to installer', async () => {
      // Arrange
      const options = { yes: false, quiet: false };

      // Act
      await wizard.run(options);

      // Assert
      expect(mockInstaller.install).toHaveBeenCalledWith({
        targetDirectory: './test-dir',
        installationMode: 'standard',
        mergeStrategy: 'merge-smart',
      });
    });

    it('should display success message after installation', async () => {
      // Arrange
      const options = { yes: false, quiet: false };

      // Act
      await wizard.run(options);

      // Assert
      expect(mockOutputFormatter.success).toHaveBeenCalledWith(
        expect.stringContaining('Installation complete')
      );
    });
  });

  describe('SVC-002: Handle --yes flag to skip interactive prompts', () => {
    it('should skip prompts with --yes flag', async () => {
      // Arrange
      const options = { yes: true, quiet: false };

      // Act
      await wizard.run(options);

      // Assert
      expect(mockPromptService.promptTargetDirectory).not.toHaveBeenCalled();
      expect(mockPromptService.promptInstallationMode).not.toHaveBeenCalled();
      expect(mockPromptService.promptMergeStrategy).not.toHaveBeenCalled();
    });

    it('should use default values with --yes flag', async () => {
      // Arrange
      const options = { yes: true, quiet: false };

      // Act
      await wizard.run(options);

      // Assert
      expect(mockInstaller.install).toHaveBeenCalledWith({
        targetDirectory: '.',
        installationMode: 'standard',
        mergeStrategy: 'merge-smart',
      });
    });

    it('should exit with code 0 on success with --yes flag', async () => {
      // Arrange
      const options = { yes: true, quiet: false };
      const mockExit = jest.spyOn(process, 'exit').mockImplementation();

      // Act
      await wizard.run(options);

      // Assert
      expect(mockExit).toHaveBeenCalledWith(0);
      mockExit.mockRestore();
    });
  });

  describe('SVC-003: Handle --quiet flag to suppress non-error output', () => {
    it('should suppress success messages with --quiet flag', async () => {
      // Arrange
      const options = { yes: true, quiet: true };

      // Act
      await wizard.run(options);

      // Assert
      expect(mockOutputFormatter.success).not.toHaveBeenCalled();
      expect(mockOutputFormatter.info).not.toHaveBeenCalled();
    });

    it('should display errors to stderr with --quiet flag', async () => {
      // Arrange
      const options = { yes: true, quiet: true };
      mockInstaller.install.mockRejectedValue(new Error('Installation failed'));
      const mockStderrWrite = jest.spyOn(process.stderr, 'write').mockImplementation();

      // Act
      await wizard.run(options);

      // Assert
      expect(mockStderrWrite).toHaveBeenCalledWith(
        expect.stringContaining('Installation failed')
      );
      mockStderrWrite.mockRestore();
    });
  });

  describe('BR-001: Non-TTY environments require --yes flag', () => {
    it('should throw error in non-TTY without --yes flag', async () => {
      // Arrange
      const originalIsTTY = process.stdout.isTTY;
      process.stdout.isTTY = false;
      const options = { yes: false, quiet: false };

      // Act & Assert
      await expect(wizard.run(options)).rejects.toThrow(
        'Interactive prompts require TTY. Use --yes for non-interactive mode.'
      );

      // Cleanup
      process.stdout.isTTY = originalIsTTY;
    });

    it('should succeed in non-TTY with --yes flag', async () => {
      // Arrange
      const originalIsTTY = process.stdout.isTTY;
      process.stdout.isTTY = false;
      const options = { yes: true, quiet: false };

      // Act
      await wizard.run(options);

      // Assert
      expect(mockInstaller.install).toHaveBeenCalled();

      // Cleanup
      process.stdout.isTTY = originalIsTTY;
    });

    it('should exit with code 1 in non-TTY without --yes', async () => {
      // Arrange
      const originalIsTTY = process.stdout.isTTY;
      process.stdout.isTTY = false;
      const options = { yes: false, quiet: false };
      const mockExit = jest.spyOn(process, 'exit').mockImplementation();

      // Act
      await wizard.run(options).catch(() => {});

      // Assert
      expect(mockExit).toHaveBeenCalledWith(1);

      // Cleanup
      process.stdout.isTTY = originalIsTTY;
      mockExit.mockRestore();
    });
  });

  describe('BR-003: --yes flag overrides all prompts with default values', () => {
    it('should use all default values with --yes', async () => {
      // Arrange
      const options = { yes: true, quiet: false };

      // Act
      const config = await wizard.run(options);

      // Assert
      expect(config).toEqual({
        targetDirectory: '.',
        installationMode: 'standard',
        mergeStrategy: 'merge-smart',
        nonInteractive: true,
        quiet: false,
      });
    });

    it('should skip confirmation prompts with --yes', async () => {
      // Arrange
      const options = { yes: true, quiet: false };

      // Act
      await wizard.run(options);

      // Assert
      expect(mockPromptService.promptConfirmation).not.toHaveBeenCalled();
    });
  });

  describe('AC#4: Confirmation prompts for destructive actions', () => {
    it('should display confirmation prompt for overwrite', async () => {
      // Arrange
      const options = { yes: false, quiet: false };
      mockInstaller.install.mockResolvedValue({ requiresOverwrite: true });

      // Act
      await wizard.run(options);

      // Assert
      expect(mockPromptService.promptConfirmation).toHaveBeenCalledWith(
        expect.objectContaining({
          message: expect.stringContaining('overwrite'),
          default: false,
        })
      );
    });

    it('should cancel operation when confirmation is denied', async () => {
      // Arrange
      const options = { yes: false, quiet: false };
      mockPromptService.promptConfirmation.mockResolvedValue(false);

      // Act
      await wizard.run(options);

      // Assert
      expect(mockInstaller.install).not.toHaveBeenCalled();
      expect(mockOutputFormatter.warning).toHaveBeenCalledWith(
        expect.stringContaining('cancelled')
      );
    });

    it('should default to No for destructive actions', async () => {
      // Arrange
      const options = { yes: false, quiet: false };

      // Act
      await wizard.run(options);

      // Assert
      expect(mockPromptService.promptConfirmation).toHaveBeenCalledWith(
        expect.objectContaining({
          default: false,
        })
      );
    });
  });

  describe('Error handling', () => {
    it('should display error message on installation failure', async () => {
      // Arrange
      const options = { yes: true, quiet: false };
      mockInstaller.install.mockRejectedValue(new Error('Permission denied'));

      // Act
      await wizard.run(options).catch(() => {});

      // Assert
      expect(mockOutputFormatter.error).toHaveBeenCalledWith(
        expect.stringContaining('Permission denied')
      );
    });

    it('should exit with non-zero code on failure', async () => {
      // Arrange
      const options = { yes: true, quiet: false };
      mockInstaller.install.mockRejectedValue(new Error('Installation failed'));
      const mockExit = jest.spyOn(process, 'exit').mockImplementation();

      // Act
      await wizard.run(options).catch(() => {});

      // Assert
      expect(mockExit).toHaveBeenCalledWith(1);
      mockExit.mockRestore();
    });
  });

  describe('NFR-003: Wizard initialization under 200ms', () => {
    it('should initialize wizard within 200ms', async () => {
      // Arrange
      const startTime = Date.now();

      // Act
      wizard = new InstallWizard({
        promptService: mockPromptService,
        progressService: mockProgressService,
        outputFormatter: mockOutputFormatter,
        installer: mockInstaller,
      });
      const elapsed = Date.now() - startTime;

      // Assert
      expect(elapsed).toBeLessThan(200);
    });
  });
});
