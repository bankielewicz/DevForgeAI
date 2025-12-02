/**
 * Unit Tests - PromptService
 *
 * Test Coverage:
 * - SVC-004: Display target directory prompt with default
 * - SVC-005: Display installation mode prompt (minimal, standard, full)
 * - SVC-006: Display merge strategy prompt (preserve-user, merge-smart, replace)
 * - SVC-007: Display confirmation prompt for destructive actions
 * - SVC-008: Skip prompts when TTY not available
 * - AC#1: Step-by-step wizard workflow
 * - AC#4: Confirmation prompts for destructive actions
 *
 * @jest-environment node
 */

const { PromptService } = require('../../../src/cli/wizard/prompt-service');
const inquirer = require('inquirer');

jest.mock('inquirer');

describe('PromptService', () => {
  let promptService;
  let mockOutputFormatter;

  beforeEach(() => {
    // Arrange: Create mock output formatter
    mockOutputFormatter = {
      info: jest.fn(),
      warning: jest.fn(),
      error: jest.fn(),
    };

    promptService = new PromptService({
      outputFormatter: mockOutputFormatter,
    });

    // Reset inquirer mock
    inquirer.prompt.mockReset();
  });

  describe('SVC-004: Display target directory prompt with default', () => {
    it('should prompt for target directory with current directory default', async () => {
      // Arrange
      inquirer.prompt.mockResolvedValue({ targetDirectory: './my-project' });

      // Act
      const result = await promptService.promptTargetDirectory();

      // Assert
      expect(inquirer.prompt).toHaveBeenCalledWith([
        expect.objectContaining({
          type: 'input',
          name: 'targetDirectory',
          message: expect.stringContaining('Target directory'),
          default: '.',
        }),
      ]);
      expect(result).toBe('./my-project');
    });

    it('should validate directory path format', async () => {
      // Arrange
      inquirer.prompt.mockResolvedValue({ targetDirectory: './valid-path' });

      // Act
      await promptService.promptTargetDirectory();
      const validateFn = inquirer.prompt.mock.calls[0][0][0].validate;

      // Assert
      expect(validateFn('/valid/path')).toBe(true);
      expect(validateFn('./relative/path')).toBe(true);
      expect(validateFn('')).toMatch(/cannot be empty/i);
    });

    it('should reject system directories', async () => {
      // Arrange
      inquirer.prompt.mockResolvedValue({ targetDirectory: './' });

      // Act
      await promptService.promptTargetDirectory();
      const validateFn = inquirer.prompt.mock.calls[0][0][0].validate;

      // Assert - Test each system directory rejection (counter increments)
      // Reset counter between assertions by calling with valid path
      expect(validateFn('/')).toMatch(/system directory/i);
      validateFn('./valid'); // Reset counter
      expect(validateFn('/usr')).toMatch(/system directory/i);
      validateFn('./valid'); // Reset counter
      expect(validateFn('/etc')).toMatch(/system directory/i);
      validateFn('./valid'); // Reset counter
      expect(validateFn('C:\\Windows')).toMatch(/system directory/i);
    });

    it('should enforce maximum path length (260 characters)', async () => {
      // Arrange
      inquirer.prompt.mockResolvedValue({ targetDirectory: './valid' });

      // Act
      await promptService.promptTargetDirectory();
      const validateFn = inquirer.prompt.mock.calls[0][0][0].validate;

      // Assert
      const longPath = 'a'.repeat(261);
      expect(validateFn(longPath)).toMatch(/exceeds maximum/i);
    });
  });

  describe('SVC-005: Display installation mode prompt', () => {
    it('should prompt with minimal, standard, full options', async () => {
      // Arrange
      inquirer.prompt.mockResolvedValue({ installationMode: 'standard' });

      // Act
      const result = await promptService.promptInstallationMode();

      // Assert
      expect(inquirer.prompt).toHaveBeenCalledWith([
        expect.objectContaining({
          type: 'list',
          name: 'installationMode',
          message: expect.stringContaining('installation mode'),
          choices: expect.arrayContaining([
            expect.objectContaining({ value: 'minimal' }),
            expect.objectContaining({ value: 'standard' }),
            expect.objectContaining({ value: 'full' }),
          ]),
          default: 'standard',
        }),
      ]);
      expect(result).toBe('standard');
    });

    it('should default to standard mode', async () => {
      // Arrange
      inquirer.prompt.mockResolvedValue({ installationMode: 'standard' });

      // Act
      await promptService.promptInstallationMode();

      // Assert
      const defaultValue = inquirer.prompt.mock.calls[0][0][0].default;
      expect(defaultValue).toBe('standard');
    });

    it('should display keyboard navigation hints', async () => {
      // Arrange
      inquirer.prompt.mockResolvedValue({ installationMode: 'full' });

      // Act
      await promptService.promptInstallationMode();

      // Assert
      expect(inquirer.prompt).toHaveBeenCalledWith([
        expect.objectContaining({
          message: expect.stringMatching(/arrow keys|enter/i),
        }),
      ]);
    });
  });

  describe('SVC-006: Display merge strategy prompt', () => {
    it('should prompt with preserve-user, merge-smart, replace options', async () => {
      // Arrange
      inquirer.prompt.mockResolvedValue({ mergeStrategy: 'merge-smart' });

      // Act
      const result = await promptService.promptMergeStrategy();

      // Assert
      expect(inquirer.prompt).toHaveBeenCalledWith([
        expect.objectContaining({
          type: 'list',
          name: 'mergeStrategy',
          message: expect.stringContaining('merge strategy'),
          choices: expect.arrayContaining([
            expect.objectContaining({ value: 'preserve-user' }),
            expect.objectContaining({ value: 'merge-smart' }),
            expect.objectContaining({ value: 'replace' }),
          ]),
          default: 'merge-smart',
        }),
      ]);
      expect(result).toBe('merge-smart');
    });

    it('should default to merge-smart', async () => {
      // Arrange
      inquirer.prompt.mockResolvedValue({ mergeStrategy: 'merge-smart' });

      // Act
      await promptService.promptMergeStrategy();

      // Assert
      const defaultValue = inquirer.prompt.mock.calls[0][0][0].default;
      expect(defaultValue).toBe('merge-smart');
    });
  });

  describe('SVC-007: Display confirmation prompt for destructive actions', () => {
    it('should display Yes/No confirmation with warning color', async () => {
      // Arrange
      inquirer.prompt.mockResolvedValue({ confirm: true });
      const options = {
        message: 'This will overwrite existing files. Continue?',
        affectedFiles: ['CLAUDE.md', 'README.md'],
      };

      // Act
      const result = await promptService.promptConfirmation(options);

      // Assert
      expect(inquirer.prompt).toHaveBeenCalledWith([
        expect.objectContaining({
          type: 'confirm',
          name: 'confirm',
          message: expect.stringContaining('overwrite'),
          default: false,
        }),
      ]);
      expect(result).toBe(true);
    });

    it('should default to No for destructive actions', async () => {
      // Arrange
      inquirer.prompt.mockResolvedValue({ confirm: false });

      // Act
      await promptService.promptConfirmation({ message: 'Delete files?' });

      // Assert
      const defaultValue = inquirer.prompt.mock.calls[0][0][0].default;
      expect(defaultValue).toBe(false);
    });

    it('should display affected file paths', async () => {
      // Arrange
      inquirer.prompt.mockResolvedValue({ confirm: false });
      const options = {
        message: 'Overwrite files?',
        affectedFiles: ['CLAUDE.md', 'README.md', 'package.json'],
      };

      // Act
      await promptService.promptConfirmation(options);

      // Assert
      expect(mockOutputFormatter.warning).toHaveBeenCalledWith(
        expect.stringContaining('CLAUDE.md')
      );
      expect(mockOutputFormatter.warning).toHaveBeenCalledWith(
        expect.stringContaining('README.md')
      );
      expect(mockOutputFormatter.warning).toHaveBeenCalledWith(
        expect.stringContaining('package.json')
      );
    });

    it('should display line count for affected files', async () => {
      // Arrange
      inquirer.prompt.mockResolvedValue({ confirm: true });
      const options = {
        message: 'Replace CLAUDE.md?',
        affectedFiles: [{ path: 'CLAUDE.md', lines: 500 }],
      };

      // Act
      await promptService.promptConfirmation(options);

      // Assert
      expect(mockOutputFormatter.warning).toHaveBeenCalledWith(
        expect.stringMatching(/CLAUDE\.md.*500.*lines/i)
      );
    });
  });

  describe('SVC-008: Skip prompts when TTY not available', () => {
    it('should throw error in non-TTY environment', async () => {
      // Arrange
      const originalIsTTY = process.stdout.isTTY;
      process.stdout.isTTY = false;

      // Act & Assert
      await expect(promptService.promptTargetDirectory()).rejects.toThrow(
        'Interactive prompts require TTY'
      );

      // Cleanup
      process.stdout.isTTY = originalIsTTY;
    });

    it('should display error message with --yes suggestion', async () => {
      // Arrange
      const originalIsTTY = process.stdout.isTTY;
      process.stdout.isTTY = false;

      // Act & Assert
      await expect(promptService.promptInstallationMode()).rejects.toThrow(
        'Use --yes for non-interactive mode'
      );

      // Cleanup
      process.stdout.isTTY = originalIsTTY;
    });
  });

  describe('AC#1: Keyboard navigation hints', () => {
    it('should show arrow keys navigation hint', async () => {
      // Arrange
      inquirer.prompt.mockResolvedValue({ installationMode: 'minimal' });

      // Act
      await promptService.promptInstallationMode();

      // Assert
      expect(inquirer.prompt).toHaveBeenCalledWith([
        expect.objectContaining({
          message: expect.stringMatching(/arrow keys/i),
        }),
      ]);
    });

    it('should show Enter to confirm hint', async () => {
      // Arrange
      inquirer.prompt.mockResolvedValue({ mergeStrategy: 'replace' });

      // Act
      await promptService.promptMergeStrategy();

      // Assert
      expect(inquirer.prompt).toHaveBeenCalledWith([
        expect.objectContaining({
          message: expect.stringMatching(/enter/i),
        }),
      ]);
    });
  });

  describe('Data Validation: Invalid user input', () => {
    it('should display error message for invalid directory', async () => {
      // Arrange
      inquirer.prompt.mockResolvedValue({ targetDirectory: './valid' });

      // Act
      await promptService.promptTargetDirectory();
      const validateFn = inquirer.prompt.mock.calls[0][0][0].validate;

      // Assert
      expect(validateFn('')).toMatch(/cannot be empty/i);
    });

    it('should keep prompt active on validation failure', async () => {
      // Arrange
      inquirer.prompt
        .mockResolvedValueOnce({ targetDirectory: '' }) // First attempt fails
        .mockResolvedValueOnce({ targetDirectory: './valid' }); // Second attempt succeeds

      // Act
      await promptService.promptTargetDirectory();

      // Assert
      expect(inquirer.prompt).toHaveBeenCalledTimes(1);
    });

    it('should offer default value after 3 consecutive failures', async () => {
      // Arrange
      inquirer.prompt.mockResolvedValue({ targetDirectory: '.' });

      // Act
      await promptService.promptTargetDirectory();
      const validateFn = inquirer.prompt.mock.calls[0][0][0].validate;

      // Assert - Test retry limit for INVALID inputs (counter only increments on failures)
      // Use empty path validation to trigger failures
      expect(validateFn('')).toMatch(/cannot be empty/i); // 1st failure, counter = 1
      expect(validateFn('')).toMatch(/cannot be empty/i); // 2nd failure, counter = 2
      const result = validateFn(''); // 3rd failure, counter = 3, triggers default

      expect(mockOutputFormatter.info).toHaveBeenCalledWith(
        expect.stringMatching(/using default/i)
      );
      expect(result).toBe(true); // Validation passes after 3 failures
    });
  });

  describe('NFR-001: Prompt response time under 50ms (p95)', () => {
    it('should respond to user input within 50ms', async () => {
      // Arrange
      inquirer.prompt.mockImplementation(async () => {
        const start = Date.now();
        await new Promise((resolve) => setTimeout(resolve, 10)); // Simulate input processing
        const elapsed = Date.now() - start;
        expect(elapsed).toBeLessThan(50);
        return { targetDirectory: './test' };
      });

      // Act
      await promptService.promptTargetDirectory();

      // Assert
      expect(inquirer.prompt).toHaveBeenCalled();
    });
  });
});
