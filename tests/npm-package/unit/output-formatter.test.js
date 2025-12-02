/**
 * Unit Tests - OutputFormatter
 *
 * Test Coverage:
 * - SVC-013: Format success messages with green color and ✓ symbol
 * - SVC-014: Format warning messages with yellow color and ⚠ symbol
 * - SVC-015: Format error messages with red color and ✗ symbol
 * - SVC-016: Format info prompts with blue color and ? symbol
 * - SVC-017: Detect NO_COLOR env var and disable colors
 * - SVC-018: Fallback to ASCII symbols when Unicode not supported
 * - AC#3: Color-coded output for status
 * - AC#6: Quiet mode with --quiet flag
 *
 * @jest-environment node
 */

const { OutputFormatter } = require('../../../src/cli/wizard/output-formatter');
const chalk = require('chalk');

jest.mock('chalk', () => ({
  green: jest.fn((text) => `[GREEN]${text}[/GREEN]`),
  yellow: jest.fn((text) => `[YELLOW]${text}[/YELLOW]`),
  red: jest.fn((text) => `[RED]${text}[/RED]`),
  blue: jest.fn((text) => `[BLUE]${text}[/BLUE]`),
  supportsColor: { level: 2 },
}));

describe('OutputFormatter', () => {
  let formatter;
  let mockStdoutWrite;
  let mockStderrWrite;

  beforeEach(() => {
    formatter = new OutputFormatter({ quiet: false });
    mockStdoutWrite = jest.spyOn(process.stdout, 'write').mockImplementation();
    mockStderrWrite = jest.spyOn(process.stderr, 'write').mockImplementation();
  });

  afterEach(() => {
    mockStdoutWrite.mockRestore();
    mockStderrWrite.mockRestore();
    jest.clearAllMocks();
  });

  describe('SVC-013: Format success messages with green color and ✓ symbol', () => {
    it('should format success message with green color', () => {
      // Arrange
      const message = 'Installation complete';

      // Act
      formatter.success(message);

      // Assert
      expect(chalk.green).toHaveBeenCalledWith(expect.stringContaining('✓'));
      expect(mockStdoutWrite).toHaveBeenCalledWith(
        expect.stringContaining('[GREEN]')
      );
    });

    it('should include ✓ symbol in success message', () => {
      // Arrange
      const message = 'Files copied successfully';

      // Act
      formatter.success(message);

      // Assert
      expect(mockStdoutWrite).toHaveBeenCalledWith(
        expect.stringMatching(/✓.*Files copied successfully/)
      );
    });

    it('should write success message to stdout', () => {
      // Arrange
      const message = 'Configuration updated';

      // Act
      formatter.success(message);

      // Assert
      expect(mockStdoutWrite).toHaveBeenCalled();
      expect(mockStderrWrite).not.toHaveBeenCalled();
    });
  });

  describe('SVC-014: Format warning messages with yellow color and ⚠ symbol', () => {
    it('should format warning message with yellow color', () => {
      // Arrange
      const message = 'Existing CLAUDE.md found';

      // Act
      formatter.warning(message);

      // Assert
      expect(chalk.yellow).toHaveBeenCalledWith(expect.stringContaining('⚠'));
      expect(mockStdoutWrite).toHaveBeenCalledWith(
        expect.stringContaining('[YELLOW]')
      );
    });

    it('should include ⚠ symbol in warning message', () => {
      // Arrange
      const message = 'Directory not empty';

      // Act
      formatter.warning(message);

      // Assert
      expect(mockStdoutWrite).toHaveBeenCalledWith(
        expect.stringMatching(/⚠.*Directory not empty/)
      );
    });
  });

  describe('SVC-015: Format error messages with red color and ✗ symbol', () => {
    it('should format error message with red color', () => {
      // Arrange
      const message = 'Target directory not writable';

      // Act
      formatter.error(message);

      // Assert
      expect(chalk.red).toHaveBeenCalledWith(expect.stringContaining('✗'));
      expect(mockStderrWrite).toHaveBeenCalledWith(
        expect.stringContaining('[RED]')
      );
    });

    it('should include ✗ symbol in error message', () => {
      // Arrange
      const message = 'Installation failed';

      // Act
      formatter.error(message);

      // Assert
      expect(mockStderrWrite).toHaveBeenCalledWith(
        expect.stringMatching(/✗.*Installation failed/)
      );
    });

    it('should write error message to stderr', () => {
      // Arrange
      const message = 'Permission denied';

      // Act
      formatter.error(message);

      // Assert
      expect(mockStderrWrite).toHaveBeenCalled();
      expect(mockStdoutWrite).not.toHaveBeenCalled();
    });
  });

  describe('SVC-016: Format info prompts with blue color and ? symbol', () => {
    it('should format info message with blue color', () => {
      // Arrange
      const message = 'Select installation mode:';

      // Act
      formatter.info(message);

      // Assert
      expect(chalk.blue).toHaveBeenCalledWith(expect.stringContaining('?'));
      expect(mockStdoutWrite).toHaveBeenCalledWith(
        expect.stringContaining('[BLUE]')
      );
    });

    it('should include ? symbol in info message', () => {
      // Arrange
      const message = 'Enter target directory';

      // Act
      formatter.info(message);

      // Assert
      expect(mockStdoutWrite).toHaveBeenCalledWith(
        expect.stringMatching(/\?.*Enter target directory/)
      );
    });
  });

  describe('SVC-017: Detect NO_COLOR env var and disable colors', () => {
    it('should disable colors when NO_COLOR env var is set', () => {
      // Arrange
      const originalNoColor = process.env.NO_COLOR;
      process.env.NO_COLOR = '1';
      formatter = new OutputFormatter({ quiet: false });

      // Act
      formatter.success('Test message');

      // Assert
      expect(mockStdoutWrite).toHaveBeenCalledWith(
        expect.not.stringMatching(/\[GREEN\]|\[YELLOW\]|\[RED\]|\[BLUE\]/)
      );

      // Cleanup
      process.env.NO_COLOR = originalNoColor;
    });

    it('should still display symbols when NO_COLOR is set', () => {
      // Arrange
      const originalNoColor = process.env.NO_COLOR;
      process.env.NO_COLOR = '1';
      formatter = new OutputFormatter({ quiet: false });

      // Act
      formatter.success('Test message');

      // Assert
      expect(mockStdoutWrite).toHaveBeenCalledWith(
        expect.stringMatching(/✓.*Test message/)
      );

      // Cleanup
      process.env.NO_COLOR = originalNoColor;
    });

    it('should detect NO_COLOR with any non-empty value', () => {
      // Arrange
      const originalNoColor = process.env.NO_COLOR;
      process.env.NO_COLOR = 'true';
      formatter = new OutputFormatter({ quiet: false });

      // Act
      formatter.warning('Test warning');

      // Assert
      expect(mockStdoutWrite).toHaveBeenCalledWith(
        expect.not.stringMatching(/\[YELLOW\]/)
      );

      // Cleanup
      process.env.NO_COLOR = originalNoColor;
    });
  });

  describe('SVC-018: Fallback to ASCII symbols when Unicode not supported', () => {
    it('should use ASCII fallback when TERM=dumb', () => {
      // Arrange
      const originalTerm = process.env.TERM;
      process.env.TERM = 'dumb';
      formatter = new OutputFormatter({ quiet: false });

      // Act
      formatter.success('Test success');
      formatter.error('Test error');
      formatter.warning('Test warning');

      // Assert
      expect(mockStdoutWrite).toHaveBeenCalledWith(
        expect.stringMatching(/\[OK\].*Test success/)
      );
      expect(mockStderrWrite).toHaveBeenCalledWith(
        expect.stringMatching(/\[ERROR\].*Test error/)
      );
      expect(mockStdoutWrite).toHaveBeenCalledWith(
        expect.stringMatching(/\[WARN\].*Test warning/)
      );

      // Cleanup
      process.env.TERM = originalTerm;
    });

    it('should map Unicode symbols to ASCII equivalents', () => {
      // Arrange
      const originalTerm = process.env.TERM;
      process.env.TERM = 'dumb';
      formatter = new OutputFormatter({ quiet: false });

      // Act & Assert
      formatter.success('Test');
      expect(mockStdoutWrite).toHaveBeenCalledWith(
        expect.not.stringMatching(/✓/)
      );
      expect(mockStdoutWrite).toHaveBeenCalledWith(
        expect.stringMatching(/\[OK\]/)
      );

      // Cleanup
      process.env.TERM = originalTerm;
    });
  });

  describe('AC#3: Color-coded output for status', () => {
    it('should use consistent colors across all wizard screens', () => {
      // Arrange
      const messages = {
        success: 'Operation completed',
        warning: 'Existing file found',
        error: 'Permission denied',
        info: 'Select option',
      };

      // Act
      formatter.success(messages.success);
      formatter.warning(messages.warning);
      formatter.error(messages.error);
      formatter.info(messages.info);

      // Assert
      expect(chalk.green).toHaveBeenCalled();
      expect(chalk.yellow).toHaveBeenCalled();
      expect(chalk.red).toHaveBeenCalled();
      expect(chalk.blue).toHaveBeenCalled();
    });
  });

  describe('AC#6: Quiet mode with --quiet flag', () => {
    it('should suppress success messages with --quiet flag', () => {
      // Arrange
      formatter = new OutputFormatter({ quiet: true });

      // Act
      formatter.success('Installation complete');
      formatter.info('Informational message');

      // Assert
      expect(mockStdoutWrite).not.toHaveBeenCalled();
    });

    it('should suppress warning messages with --quiet flag', () => {
      // Arrange
      formatter = new OutputFormatter({ quiet: true });

      // Act
      formatter.warning('Existing file found');

      // Assert
      expect(mockStdoutWrite).not.toHaveBeenCalled();
    });

    it('should display errors to stderr with --quiet flag', () => {
      // Arrange
      formatter = new OutputFormatter({ quiet: true });

      // Act
      formatter.error('Installation failed');

      // Assert
      expect(mockStderrWrite).toHaveBeenCalledWith(
        expect.stringMatching(/✗.*Installation failed/)
      );
    });

    it('should only output errors in quiet mode', () => {
      // Arrange
      formatter = new OutputFormatter({ quiet: true });

      // Act
      formatter.success('Success');
      formatter.warning('Warning');
      formatter.info('Info');
      formatter.error('Error');

      // Assert
      expect(mockStdoutWrite).not.toHaveBeenCalled();
      expect(mockStderrWrite).toHaveBeenCalledTimes(1);
    });
  });

  describe('Edge Case: Color support detection', () => {
    it('should detect terminal color support level', () => {
      // Arrange & Act
      formatter = new OutputFormatter({ quiet: false });

      // Assert
      expect(chalk.supportsColor).toBeDefined();
    });

    it('should disable colors if chalk.supportsColor is false', () => {
      // Arrange
      const mockChalk = { ...chalk, supportsColor: false };
      jest.mock('chalk', () => mockChalk);

      // Act
      formatter = new OutputFormatter({ quiet: false });
      formatter.success('Test');

      // Assert - Should use plain text
      expect(mockStdoutWrite).toHaveBeenCalledWith(
        expect.not.stringMatching(/\[GREEN\]/)
      );
    });
  });

  describe('Edge Case: Message formatting', () => {
    it('should preserve multiline messages', () => {
      // Arrange
      const message = 'Line 1\nLine 2\nLine 3';

      // Act
      formatter.success(message);

      // Assert
      expect(mockStdoutWrite).toHaveBeenCalledWith(
        expect.stringMatching(/Line 1\nLine 2\nLine 3/)
      );
    });

    it('should escape special characters in messages', () => {
      // Arrange
      const message = 'Path: C:\\Users\\test\\file.txt';

      // Act
      formatter.info(message);

      // Assert
      expect(mockStdoutWrite).toHaveBeenCalledWith(
        expect.stringContaining('C:\\Users\\test\\file.txt')
      );
    });
  });
});
