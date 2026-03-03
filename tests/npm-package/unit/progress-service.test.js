/**
 * Unit Tests - ProgressService
 *
 * Test Coverage:
 * - SVC-009: Display spinner for indeterminate operations (>200ms)
 * - SVC-010: Display progress bar for determinate operations
 * - SVC-011: Update spinner text with sub-operation status
 * - SVC-012: Disable spinners/progress when --quiet flag set
 * - AC#2: Progress indicators during operations
 * - AC#6: Quiet mode with --quiet flag
 *
 * @jest-environment node
 */

const { ProgressService } = require('../../../src/cli/wizard/progress-service');
const ora = require('ora');
const cliProgress = require('cli-progress');

jest.mock('ora');
jest.mock('cli-progress');

describe('ProgressService', () => {
  let progressService;
  let mockSpinner;
  let mockProgressBar;

  beforeEach(() => {
    // Arrange: Create mocks
    mockSpinner = {
      start: jest.fn().mockReturnThis(),
      stop: jest.fn().mockReturnThis(),
      succeed: jest.fn().mockReturnThis(),
      fail: jest.fn().mockReturnThis(),
      text: '',
    };

    mockProgressBar = {
      start: jest.fn(),
      update: jest.fn(),
      stop: jest.fn(),
    };

    ora.mockReturnValue(mockSpinner);
    cliProgress.SingleBar.mockImplementation(() => mockProgressBar);

    progressService = new ProgressService({ quiet: false });
  });

  afterEach(() => {
    jest.clearAllMocks();
  });

  describe('SVC-009: Display spinner for indeterminate operations (>200ms)', () => {
    it('should start spinner after 200ms threshold', async () => {
      // Arrange
      jest.useFakeTimers();

      // Act
      progressService.startSpinner('Installing files...');
      jest.advanceTimersByTime(199);

      // Assert - Spinner should NOT start yet
      expect(mockSpinner.start).not.toHaveBeenCalled();

      // Act - Advance past threshold
      jest.advanceTimersByTime(2);

      // Assert - Spinner should NOW start
      expect(mockSpinner.start).toHaveBeenCalled();

      jest.useRealTimers();
    });

    it('should not start spinner if operation completes within 200ms', async () => {
      // Arrange
      jest.useFakeTimers();

      // Act
      progressService.startSpinner('Quick operation...');
      jest.advanceTimersByTime(100);
      progressService.stopSpinner();

      // Assert
      expect(mockSpinner.start).not.toHaveBeenCalled();

      jest.useRealTimers();
    });

    it('should display operation description in spinner', () => {
      // Arrange
      const description = 'Copying configuration files...';

      // Act
      progressService.startSpinner(description);

      // Assert
      expect(ora).toHaveBeenCalledWith(
        expect.objectContaining({
          text: description,
        })
      );
    });

    it('should stop spinner successfully on completion', () => {
      // Arrange
      progressService.startSpinner('Processing...');

      // Act
      progressService.stopSpinner({ success: true });

      // Assert
      expect(mockSpinner.succeed).toHaveBeenCalled();
    });

    it('should stop spinner with failure on error', () => {
      // Arrange
      progressService.startSpinner('Processing...');

      // Act
      progressService.stopSpinner({ success: false, message: 'Failed' });

      // Assert
      expect(mockSpinner.fail).toHaveBeenCalledWith('Failed');
    });
  });

  describe('SVC-010: Display progress bar for determinate operations', () => {
    it('should display progress bar for file count operations', () => {
      // Arrange
      const total = 50;

      // Act
      progressService.startProgressBar({ total, format: 'files' });

      // Assert
      expect(cliProgress.SingleBar).toHaveBeenCalled();
      expect(mockProgressBar.start).toHaveBeenCalledWith(total, 0);
    });

    it('should update progress bar with percentage', () => {
      // Arrange
      progressService.startProgressBar({ total: 100 });

      // Act
      progressService.updateProgress(23);

      // Assert
      expect(mockProgressBar.update).toHaveBeenCalledWith(23);
    });

    it('should stop progress bar on completion', () => {
      // Arrange
      progressService.startProgressBar({ total: 100 });
      progressService.updateProgress(100);

      // Act
      progressService.stopProgressBar();

      // Assert
      expect(mockProgressBar.stop).toHaveBeenCalled();
    });

    it('should show percentage complete in progress bar', () => {
      // Arrange
      const formatString = '{bar} | {percentage}% | {value}/{total} files';

      // Act
      progressService.startProgressBar({
        total: 50,
        format: formatString,
      });

      // Assert
      expect(cliProgress.SingleBar).toHaveBeenCalledWith(
        expect.objectContaining({
          format: expect.stringMatching(/{percentage}/),
        }),
        expect.any(Object)
      );
    });
  });

  describe('SVC-011: Update spinner text with sub-operation status', () => {
    it('should update spinner text with file count status', () => {
      // Arrange
      progressService.startSpinner('Copying files...');

      // Act
      progressService.updateSpinnerText('Copying src/ [23/50 files]');

      // Assert
      expect(mockSpinner.text).toBe('Copying src/ [23/50 files]');
    });

    it('should update spinner text during multi-step operation', () => {
      // Arrange
      progressService.startSpinner('Installing...');

      // Act
      progressService.updateSpinnerText('Step 1/3: Copying files');
      progressService.updateSpinnerText('Step 2/3: Updating configs');
      progressService.updateSpinnerText('Step 3/3: Finalizing');

      // Assert
      expect(mockSpinner.text).toBe('Step 3/3: Finalizing');
    });
  });

  describe('SVC-012: Disable spinners/progress when --quiet flag set', () => {
    it('should not display spinner with --quiet flag', () => {
      // Arrange
      progressService = new ProgressService({ quiet: true });

      // Act
      progressService.startSpinner('Installing...');

      // Assert
      expect(ora).not.toHaveBeenCalled();
      expect(mockSpinner.start).not.toHaveBeenCalled();
    });

    it('should not display progress bar with --quiet flag', () => {
      // Arrange
      progressService = new ProgressService({ quiet: true });

      // Act
      progressService.startProgressBar({ total: 100 });

      // Assert
      expect(cliProgress.SingleBar).not.toHaveBeenCalled();
      expect(mockProgressBar.start).not.toHaveBeenCalled();
    });

    it('should not update spinner text with --quiet flag', () => {
      // Arrange
      progressService = new ProgressService({ quiet: true });

      // Act
      progressService.startSpinner('Installing...');
      progressService.updateSpinnerText('Updated text');

      // Assert
      expect(mockSpinner.text).toBe('');
    });
  });

  describe('AC#2: Progress indicators during operations', () => {
    it('should display animated spinner for >200ms operations', async () => {
      // Arrange
      jest.useFakeTimers();

      // Act
      progressService.startSpinner('Long operation...');
      jest.advanceTimersByTime(201);

      // Assert
      expect(mockSpinner.start).toHaveBeenCalled();
      expect(ora).toHaveBeenCalledWith(
        expect.objectContaining({
          text: 'Long operation...',
        })
      );

      jest.useRealTimers();
    });

    it('should display progress bar showing percentage for file operations', () => {
      // Arrange
      const total = 50;

      // Act
      progressService.startProgressBar({ total });
      progressService.updateProgress(10); // 20%
      progressService.updateProgress(25); // 50%
      progressService.updateProgress(50); // 100%

      // Assert
      expect(mockProgressBar.update).toHaveBeenCalledWith(10);
      expect(mockProgressBar.update).toHaveBeenCalledWith(25);
      expect(mockProgressBar.update).toHaveBeenCalledWith(50);
    });

    it('should update spinner text with sub-operation status', () => {
      // Arrange
      progressService.startSpinner('Copying files...');

      // Act
      progressService.updateSpinnerText('Copying src/ [23/50 files]');

      // Assert
      expect(mockSpinner.text).toBe('Copying src/ [23/50 files]');
    });
  });

  describe('NFR-002: Spinner animation at 60 FPS', () => {
    it('should configure Ora for 60 FPS (16ms per frame)', () => {
      // Arrange & Act
      progressService.startSpinner('Testing FPS...');

      // Assert
      expect(ora).toHaveBeenCalledWith(
        expect.objectContaining({
          interval: expect.any(Number),
        })
      );

      const interval = ora.mock.calls[0][0].interval;
      expect(interval).toBeLessThanOrEqual(16); // 60 FPS = 16.67ms per frame
    });
  });

  describe('Edge Case: Terminal resize during progress bar', () => {
    it('should handle terminal resize gracefully', () => {
      // Arrange
      progressService.startProgressBar({ total: 100 });

      // Act - Simulate terminal resize
      process.stdout.columns = 40; // Narrow terminal
      progressService.updateProgress(50);

      // Assert - Progress bar should still function
      expect(mockProgressBar.update).toHaveBeenCalledWith(50);
    });

    it('should switch to percentage-only display if terminal too narrow', () => {
      // Arrange
      process.stdout.columns = 35; // Below 40 column threshold

      // Act
      progressService.startProgressBar({ total: 100 });

      // Assert
      expect(cliProgress.SingleBar).toHaveBeenCalledWith(
        expect.objectContaining({
          format: expect.stringMatching(/{percentage}/),
        }),
        expect.any(Object)
      );
    });
  });

  describe('Windows terminal Unicode support', () => {
    it('should use ASCII fallback on Windows with limited Unicode', () => {
      // Arrange
      const originalPlatform = process.platform;
      Object.defineProperty(process, 'platform', { value: 'win32' });

      // Act
      progressService = new ProgressService({ quiet: false });
      progressService.startSpinner('Installing...');

      // Assert
      expect(ora).toHaveBeenCalledWith(
        expect.objectContaining({
          spinner: expect.objectContaining({
            frames: expect.arrayContaining(['|', '/', '-', '\\']),
          }),
        })
      );

      // Cleanup
      Object.defineProperty(process, 'platform', { value: originalPlatform });
    });
  });
});
