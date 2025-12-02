/**
 * Integration Tests - Wizard Flow
 *
 * Test Coverage:
 * - AC#1: Step-by-step wizard workflow
 * - AC#2: Progress indicators during operations
 * - AC#3: Color-coded output for status
 * - AC#4: Confirmation prompts for destructive actions
 * - AC#5: Non-interactive mode with --yes flag
 * - AC#6: Quiet mode with --quiet flag
 * - Complete wizard flow from prompts to installation
 *
 * @jest-environment node
 */

const { InstallWizard } = require('../../../src/cli/wizard/install-wizard');
const { PromptService } = require('../../../src/cli/wizard/prompt-service');
const { ProgressService } = require('../../../src/cli/wizard/progress-service');
const { OutputFormatter } = require('../../../src/cli/wizard/output-formatter');
const { SignalHandler } = require('../../../src/cli/wizard/signal-handler');
const fs = require('fs').promises;
const path = require('path');

describe('Wizard Flow Integration', () => {
  let wizard;
  let testDir;

  beforeEach(async () => {
    // Arrange: Create test directory
    testDir = path.join(__dirname, 'test-temp');
    await fs.mkdir(testDir, { recursive: true });
  });

  afterEach(async () => {
    // Cleanup: Remove test directory
    await fs.rm(testDir, { recursive: true, force: true });
  });

  describe('AC#1: Step-by-step wizard workflow', () => {
    it('should complete wizard with all prompts in sequence', async () => {
      // Arrange
      const mockPromptService = {
        promptTargetDirectory: jest.fn().mockResolvedValue(testDir),
        promptInstallationMode: jest.fn().mockResolvedValue('standard'),
        promptMergeStrategy: jest.fn().mockResolvedValue('merge-smart'),
      };

      wizard = new InstallWizard({
        promptService: mockPromptService,
        progressService: new ProgressService({ quiet: false }),
        outputFormatter: new OutputFormatter({ quiet: false }),
      });

      // Act
      const config = await wizard.run({ yes: false, quiet: false });

      // Assert
      expect(mockPromptService.promptTargetDirectory).toHaveBeenCalledBefore(
        mockPromptService.promptInstallationMode
      );
      expect(mockPromptService.promptInstallationMode).toHaveBeenCalledBefore(
        mockPromptService.promptMergeStrategy
      );
      expect(config.targetDirectory).toBe(testDir);
      expect(config.installationMode).toBe('standard');
      expect(config.mergeStrategy).toBe('merge-smart');
    });

    it('should allow keyboard navigation with arrow keys', async () => {
      // This test validates that Inquirer.js is configured for arrow key navigation
      // Actual keyboard input testing requires E2E tests

      // Arrange
      const promptService = new PromptService({
        outputFormatter: new OutputFormatter({ quiet: false }),
      });

      // Act - Verify prompt configuration includes keyboard navigation
      const mockInquirer = jest.requireMock('inquirer');
      await promptService.promptInstallationMode();

      // Assert
      expect(mockInquirer.prompt).toHaveBeenCalledWith([
        expect.objectContaining({
          type: 'list', // List type supports arrow key navigation
        }),
      ]);
    });

    it('should show current value and available options in prompts', async () => {
      // Arrange
      const promptService = new PromptService({
        outputFormatter: new OutputFormatter({ quiet: false }),
      });

      // Act
      const mockInquirer = jest.requireMock('inquirer');
      await promptService.promptInstallationMode();

      // Assert
      const call = mockInquirer.prompt.mock.calls[0][0][0];
      expect(call.choices).toBeDefined();
      expect(call.default).toBe('standard');
      expect(call.message).toMatch(/installation mode/i);
    });
  });

  describe('AC#2 & AC#3: Progress indicators and color-coded output', () => {
    it('should display spinner during long operations', async () => {
      // Arrange
      const progressService = new ProgressService({ quiet: false });
      const mockOra = jest.requireMock('ora');

      // Act
      progressService.startSpinner('Copying files...');
      await new Promise((resolve) => setTimeout(resolve, 250)); // Exceed 200ms threshold
      progressService.stopSpinner({ success: true });

      // Assert
      expect(mockOra).toHaveBeenCalledWith(
        expect.objectContaining({
          text: 'Copying files...',
        })
      );
    });

    it('should display progress bar for file operations', async () => {
      // Arrange
      const progressService = new ProgressService({ quiet: false });
      const mockCliProgress = jest.requireMock('cli-progress');

      // Act
      progressService.startProgressBar({ total: 50, format: 'files' });
      progressService.updateProgress(10);
      progressService.updateProgress(25);
      progressService.updateProgress(50);
      progressService.stopProgressBar();

      // Assert
      expect(mockCliProgress.SingleBar).toHaveBeenCalled();
      expect(
        mockCliProgress.SingleBar.mock.results[0].value.update
      ).toHaveBeenCalledWith(10);
      expect(
        mockCliProgress.SingleBar.mock.results[0].value.update
      ).toHaveBeenCalledWith(25);
      expect(
        mockCliProgress.SingleBar.mock.results[0].value.update
      ).toHaveBeenCalledWith(50);
    });

    it('should display color-coded output for different statuses', async () => {
      // Arrange
      const outputFormatter = new OutputFormatter({ quiet: false });
      const mockChalk = jest.requireMock('chalk');

      // Act
      outputFormatter.success('Installation complete');
      outputFormatter.warning('Existing file found');
      outputFormatter.error('Permission denied');
      outputFormatter.info('Select option');

      // Assert
      expect(mockChalk.green).toHaveBeenCalledWith(
        expect.stringContaining('✓')
      );
      expect(mockChalk.yellow).toHaveBeenCalledWith(
        expect.stringContaining('⚠')
      );
      expect(mockChalk.red).toHaveBeenCalledWith(expect.stringContaining('✗'));
      expect(mockChalk.blue).toHaveBeenCalledWith(expect.stringContaining('?'));
    });
  });

  describe('AC#4: Confirmation prompts for destructive actions', () => {
    it('should prompt for confirmation before overwriting files', async () => {
      // Arrange
      const claudeMdPath = path.join(testDir, 'CLAUDE.md');
      await fs.writeFile(claudeMdPath, '# Existing Content');

      const mockPromptService = {
        promptTargetDirectory: jest.fn().mockResolvedValue(testDir),
        promptInstallationMode: jest.fn().mockResolvedValue('full'),
        promptMergeStrategy: jest.fn().mockResolvedValue('replace'),
        promptConfirmation: jest.fn().mockResolvedValue(true),
      };

      wizard = new InstallWizard({
        promptService: mockPromptService,
        progressService: new ProgressService({ quiet: false }),
        outputFormatter: new OutputFormatter({ quiet: false }),
      });

      // Act
      await wizard.run({ yes: false, quiet: false });

      // Assert
      expect(mockPromptService.promptConfirmation).toHaveBeenCalledWith(
        expect.objectContaining({
          message: expect.stringMatching(/overwrite|replace/i),
          default: false,
        })
      );
    });

    it('should cancel operation when confirmation denied', async () => {
      // Arrange
      const mockPromptService = {
        promptTargetDirectory: jest.fn().mockResolvedValue(testDir),
        promptInstallationMode: jest.fn().mockResolvedValue('full'),
        promptMergeStrategy: jest.fn().mockResolvedValue('replace'),
        promptConfirmation: jest.fn().mockResolvedValue(false), // User says No
      };

      const mockInstaller = jest.fn();

      wizard = new InstallWizard({
        promptService: mockPromptService,
        progressService: new ProgressService({ quiet: false }),
        outputFormatter: new OutputFormatter({ quiet: false }),
        installer: { install: mockInstaller },
      });

      // Act
      await wizard.run({ yes: false, quiet: false });

      // Assert
      expect(mockInstaller).not.toHaveBeenCalled();
    });

    it('should default to No for destructive confirmations', async () => {
      // Arrange
      const promptService = new PromptService({
        outputFormatter: new OutputFormatter({ quiet: false }),
      });

      // Act
      const mockInquirer = jest.requireMock('inquirer');
      await promptService.promptConfirmation({
        message: 'Overwrite files?',
        affectedFiles: ['CLAUDE.md'],
      });

      // Assert
      expect(mockInquirer.prompt).toHaveBeenCalledWith([
        expect.objectContaining({
          default: false,
        }),
      ]);
    });
  });

  describe('AC#5: Non-interactive mode with --yes flag', () => {
    it('should complete installation without prompts using --yes', async () => {
      // Arrange
      const mockPromptService = {
        promptTargetDirectory: jest.fn(),
        promptInstallationMode: jest.fn(),
        promptMergeStrategy: jest.fn(),
      };

      wizard = new InstallWizard({
        promptService: mockPromptService,
        progressService: new ProgressService({ quiet: false }),
        outputFormatter: new OutputFormatter({ quiet: false }),
      });

      // Act
      const config = await wizard.run({ yes: true, quiet: false });

      // Assert
      expect(mockPromptService.promptTargetDirectory).not.toHaveBeenCalled();
      expect(mockPromptService.promptInstallationMode).not.toHaveBeenCalled();
      expect(mockPromptService.promptMergeStrategy).not.toHaveBeenCalled();
      expect(config.targetDirectory).toBe('.');
      expect(config.installationMode).toBe('standard');
      expect(config.mergeStrategy).toBe('merge-smart');
    });

    it('should use default values with --yes flag', async () => {
      // Arrange
      wizard = new InstallWizard({
        promptService: new PromptService({
          outputFormatter: new OutputFormatter({ quiet: false }),
        }),
        progressService: new ProgressService({ quiet: false }),
        outputFormatter: new OutputFormatter({ quiet: false }),
      });

      // Act
      const config = await wizard.run({ yes: true, quiet: false });

      // Assert
      expect(config).toEqual(
        expect.objectContaining({
          targetDirectory: '.',
          installationMode: 'standard',
          mergeStrategy: 'merge-smart',
          nonInteractive: true,
        })
      );
    });

    it('should exit with code 0 on successful --yes installation', async () => {
      // Arrange
      const mockExit = jest.spyOn(process, 'exit').mockImplementation();
      wizard = new InstallWizard({
        promptService: new PromptService({
          outputFormatter: new OutputFormatter({ quiet: false }),
        }),
        progressService: new ProgressService({ quiet: false }),
        outputFormatter: new OutputFormatter({ quiet: false }),
      });

      // Act
      await wizard.run({ yes: true, quiet: false });

      // Assert
      expect(mockExit).toHaveBeenCalledWith(0);

      mockExit.mockRestore();
    });
  });

  describe('AC#6: Quiet mode with --quiet flag', () => {
    it('should suppress non-error output with --quiet', async () => {
      // Arrange
      const mockStdoutWrite = jest
        .spyOn(process.stdout, 'write')
        .mockImplementation();
      const mockStderrWrite = jest
        .spyOn(process.stderr, 'write')
        .mockImplementation();

      wizard = new InstallWizard({
        promptService: new PromptService({
          outputFormatter: new OutputFormatter({ quiet: true }),
        }),
        progressService: new ProgressService({ quiet: true }),
        outputFormatter: new OutputFormatter({ quiet: true }),
      });

      // Act
      await wizard.run({ yes: true, quiet: true });

      // Assert
      expect(mockStdoutWrite).not.toHaveBeenCalled(); // No stdout output
      expect(mockStderrWrite).not.toHaveBeenCalled(); // No errors occurred

      mockStdoutWrite.mockRestore();
      mockStderrWrite.mockRestore();
    });

    it('should display errors to stderr with --quiet', async () => {
      // Arrange
      const mockStderrWrite = jest
        .spyOn(process.stderr, 'write')
        .mockImplementation();
      const outputFormatter = new OutputFormatter({ quiet: true });

      // Act
      outputFormatter.error('Installation failed');

      // Assert
      expect(mockStderrWrite).toHaveBeenCalledWith(
        expect.stringContaining('Installation failed')
      );

      mockStderrWrite.mockRestore();
    });

    it('should suppress spinners and progress bars with --quiet', async () => {
      // Arrange
      const progressService = new ProgressService({ quiet: true });
      const mockOra = jest.requireMock('ora');
      const mockCliProgress = jest.requireMock('cli-progress');

      // Act
      progressService.startSpinner('Installing...');
      progressService.startProgressBar({ total: 100 });

      // Assert
      expect(mockOra).not.toHaveBeenCalled();
      expect(mockCliProgress.SingleBar).not.toHaveBeenCalled();
    });
  });

  describe('NFR-003: Wizard initialization under 200ms', () => {
    it('should initialize wizard within 200ms', () => {
      // Arrange
      const startTime = Date.now();

      // Act
      wizard = new InstallWizard({
        promptService: new PromptService({
          outputFormatter: new OutputFormatter({ quiet: false }),
        }),
        progressService: new ProgressService({ quiet: false }),
        outputFormatter: new OutputFormatter({ quiet: false }),
        signalHandler: new SignalHandler({
          outputFormatter: new OutputFormatter({ quiet: false }),
          cleanupService: { cleanup: jest.fn() },
        }),
      });

      const elapsed = Date.now() - startTime;

      // Assert
      expect(elapsed).toBeLessThan(200);
    });
  });

  describe('Edge Case: Error recovery', () => {
    it('should recover from validation errors and continue', async () => {
      // Arrange
      const mockPromptService = {
        promptTargetDirectory: jest
          .fn()
          .mockRejectedValueOnce(new Error('Invalid path'))
          .mockResolvedValue(testDir), // Retry succeeds
        promptInstallationMode: jest.fn().mockResolvedValue('standard'),
        promptMergeStrategy: jest.fn().mockResolvedValue('merge-smart'),
      };

      wizard = new InstallWizard({
        promptService: mockPromptService,
        progressService: new ProgressService({ quiet: false }),
        outputFormatter: new OutputFormatter({ quiet: false }),
      });

      // Act
      await wizard.run({ yes: false, quiet: false });

      // Assert
      expect(mockPromptService.promptTargetDirectory).toHaveBeenCalledTimes(2);
      expect(mockPromptService.promptInstallationMode).toHaveBeenCalledTimes(
        1
      );
    });
  });
});
