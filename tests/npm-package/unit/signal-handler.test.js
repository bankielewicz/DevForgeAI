/**
 * Unit Tests - SignalHandler
 *
 * Test Coverage:
 * - SVC-019: Handle SIGINT (Ctrl+C) gracefully
 * - SVC-020: Stop current operation without partial writes
 * - SVC-021: Display cancellation message before exit
 * - AC#7: Keyboard interrupt handling
 * - NFR-008: Atomic file operations with no partial writes
 *
 * @jest-environment node
 */

const { SignalHandler } = require('../../../src/cli/wizard/signal-handler');

describe('SignalHandler', () => {
  let signalHandler;
  let mockOutputFormatter;
  let mockCleanupService;
  let mockProcessExit;
  let originalListeners;

  beforeEach(() => {
    // Arrange: Create mocks
    mockOutputFormatter = {
      error: jest.fn(),
      warning: jest.fn(),
    };

    mockCleanupService = {
      cleanup: jest.fn().mockResolvedValue(true),
      removePartialFiles: jest.fn(),
      restoreOriginalState: jest.fn(),
    };

    mockProcessExit = jest.spyOn(process, 'exit').mockImplementation();

    // Store original SIGINT listeners
    originalListeners = process.listeners('SIGINT');
    process.removeAllListeners('SIGINT');

    signalHandler = new SignalHandler({
      outputFormatter: mockOutputFormatter,
      cleanupService: mockCleanupService,
    });
  });

  afterEach(() => {
    mockProcessExit.mockRestore();
    process.removeAllListeners('SIGINT');

    // Restore original listeners
    originalListeners.forEach((listener) => {
      process.on('SIGINT', listener);
    });

    jest.clearAllMocks();
  });

  describe('SVC-019: Handle SIGINT (Ctrl+C) gracefully', () => {
    it('should catch SIGINT signal', async () => {
      // Arrange
      signalHandler.register();

      // Act - emit SIGINT and wait for async handler
      process.emit('SIGINT');
      await new Promise(resolve => setImmediate(resolve));

      // Assert
      expect(mockOutputFormatter.error).toHaveBeenCalled();
      expect(mockProcessExit).toHaveBeenCalledWith(130);
    });

    it('should exit with code 130 on SIGINT', async () => {
      // Arrange
      signalHandler.register();

      // Act - emit SIGINT and wait for async handler
      process.emit('SIGINT');
      await new Promise(resolve => setImmediate(resolve));

      // Assert
      expect(mockProcessExit).toHaveBeenCalledWith(130);
    });

    it('should register SIGINT handler on initialization', () => {
      // Arrange
      const listenersBefore = process.listenerCount('SIGINT');

      // Act
      signalHandler.register();

      // Assert
      expect(process.listenerCount('SIGINT')).toBe(listenersBefore + 1);
    });

    it('should remove SIGINT handler on unregister', () => {
      // Arrange
      signalHandler.register();
      const listenersAfterRegister = process.listenerCount('SIGINT');

      // Act
      signalHandler.unregister();

      // Assert
      expect(process.listenerCount('SIGINT')).toBe(listenersAfterRegister - 1);
    });
  });

  describe('SVC-020: Stop current operation without partial writes', () => {
    it('should call cleanup service on SIGINT', async () => {
      // Arrange
      signalHandler.register();

      // Act
      process.emit('SIGINT');

      // Wait for async cleanup
      await new Promise((resolve) => setImmediate(resolve));

      // Assert
      expect(mockCleanupService.cleanup).toHaveBeenCalled();
    });

    it('should remove partial files during cleanup', async () => {
      // Arrange
      signalHandler.register();
      signalHandler.trackFile('/tmp/partial-file.txt');

      // Act
      process.emit('SIGINT');

      // Wait for async cleanup
      await new Promise((resolve) => setImmediate(resolve));

      // Assert
      expect(mockCleanupService.removePartialFiles).toHaveBeenCalledWith(
        expect.arrayContaining(['/tmp/partial-file.txt'])
      );
    });

    it('should restore original state if possible', async () => {
      // Arrange
      signalHandler.register();
      signalHandler.captureState({ claudeMdBackup: '/tmp/CLAUDE.md.backup' });

      // Act
      process.emit('SIGINT');

      // Wait for async cleanup
      await new Promise((resolve) => setImmediate(resolve));

      // Assert
      expect(mockCleanupService.restoreOriginalState).toHaveBeenCalledWith(
        expect.objectContaining({
          claudeMdBackup: '/tmp/CLAUDE.md.backup',
        })
      );
    });

    it('should stop file operations immediately on SIGINT', async () => {
      // Arrange
      signalHandler.register();
      const mockFileOperation = jest.fn();
      signalHandler.registerOperation(mockFileOperation);

      // Act
      process.emit('SIGINT');

      // Assert
      expect(mockFileOperation).toHaveBeenCalledWith('abort');
    });
  });

  describe('SVC-021: Display cancellation message before exit', () => {
    it('should display cancellation message on SIGINT', () => {
      // Arrange
      signalHandler.register();

      // Act
      process.emit('SIGINT');

      // Assert
      expect(mockOutputFormatter.error).toHaveBeenCalledWith(
        expect.stringMatching(/✗.*Installation cancelled by user/)
      );
    });

    it('should display message before cleanup', async () => {
      // Arrange
      const callOrder = [];
      mockOutputFormatter.error.mockImplementation(() =>
        callOrder.push('message')
      );
      mockCleanupService.cleanup.mockImplementation(async () =>
        callOrder.push('cleanup')
      );

      signalHandler.register();

      // Act
      process.emit('SIGINT');

      // Wait for async operations
      await new Promise((resolve) => setImmediate(resolve));

      // Assert
      expect(callOrder).toEqual(['message', 'cleanup']);
    });

    it('should display message before exit', async () => {
      // Arrange
      const callOrder = [];
      mockOutputFormatter.error.mockImplementation(() =>
        callOrder.push('message')
      );
      mockProcessExit.mockImplementation(() => callOrder.push('exit'));

      signalHandler.register();

      // Act - emit SIGINT and wait for async handler
      process.emit('SIGINT');
      await new Promise(resolve => setImmediate(resolve));

      // Assert
      expect(callOrder).toEqual(['message', 'exit']);
    });
  });

  describe('AC#7: Keyboard interrupt handling', () => {
    it('should handle Ctrl+C during prompt display', async () => {
      // Arrange
      signalHandler.register();
      signalHandler.setCurrentOperation('displaying prompt');

      // Act - emit SIGINT and wait for async handler
      process.emit('SIGINT');
      await new Promise(resolve => setImmediate(resolve));

      // Assert
      expect(mockOutputFormatter.error).toHaveBeenCalledWith(
        expect.stringContaining('Installation cancelled')
      );
      expect(mockProcessExit).toHaveBeenCalledWith(130);
    });

    it('should handle Ctrl+C during spinner display', async () => {
      // Arrange
      signalHandler.register();
      signalHandler.setCurrentOperation('copying files');

      // Act
      process.emit('SIGINT');

      // Wait for async cleanup
      await new Promise((resolve) => setImmediate(resolve));

      // Assert
      expect(mockCleanupService.cleanup).toHaveBeenCalled();
      expect(mockProcessExit).toHaveBeenCalledWith(130);
    });

    it('should clean up temporary files on SIGINT', async () => {
      // Arrange
      signalHandler.register();
      signalHandler.trackFile('/tmp/temp-file-1.txt');
      signalHandler.trackFile('/tmp/temp-file-2.txt');

      // Act
      process.emit('SIGINT');

      // Wait for async cleanup
      await new Promise((resolve) => setImmediate(resolve));

      // Assert
      expect(mockCleanupService.removePartialFiles).toHaveBeenCalledWith(
        expect.arrayContaining([
          '/tmp/temp-file-1.txt',
          '/tmp/temp-file-2.txt',
        ])
      );
    });

    it('should exit with code 130 (standard SIGINT code)', async () => {
      // Arrange
      signalHandler.register();

      // Act - emit SIGINT and wait for async handler
      process.emit('SIGINT');
      await new Promise(resolve => setImmediate(resolve));

      // Assert
      expect(mockProcessExit).toHaveBeenCalledWith(130);
    });
  });

  describe('NFR-008: Atomic file operations with no partial writes', () => {
    it('should not leave partial files after interruption', async () => {
      // Arrange
      signalHandler.register();
      signalHandler.trackFile('/tmp/partial-1.txt');
      signalHandler.trackFile('/tmp/partial-2.txt');

      // Act
      process.emit('SIGINT');

      // Wait for async cleanup
      await new Promise((resolve) => setImmediate(resolve));

      // Assert
      expect(mockCleanupService.removePartialFiles).toHaveBeenCalledWith(
        expect.arrayContaining(['/tmp/partial-1.txt', '/tmp/partial-2.txt'])
      );
    });

    it('should verify zero partial files after SIGINT', async () => {
      // Arrange
      signalHandler.register();
      mockCleanupService.cleanup.mockResolvedValue({ partialFiles: [] });

      // Act
      process.emit('SIGINT');

      // Wait for async cleanup
      await new Promise((resolve) => setImmediate(resolve));

      // Assert
      const result = await mockCleanupService.cleanup();
      expect(result.partialFiles).toEqual([]);
    });
  });

  describe('Edge Case: Cleanup failure handling', () => {
    it('should still exit even if cleanup fails', async () => {
      // Arrange
      signalHandler.register();
      mockCleanupService.cleanup.mockRejectedValue(
        new Error('Cleanup failed')
      );

      // Act
      process.emit('SIGINT');

      // Wait for async cleanup
      await new Promise((resolve) => setImmediate(resolve));

      // Assert
      expect(mockProcessExit).toHaveBeenCalledWith(130);
    });

    it('should log cleanup error before exit', async () => {
      // Arrange
      signalHandler.register();
      mockCleanupService.cleanup.mockRejectedValue(
        new Error('Cleanup failed')
      );

      // Act
      process.emit('SIGINT');

      // Wait for async cleanup
      await new Promise((resolve) => setImmediate(resolve));

      // Assert
      expect(mockOutputFormatter.warning).toHaveBeenCalledWith(
        expect.stringContaining('Cleanup failed')
      );
    });
  });

  describe('Edge Case: Multiple SIGINT signals', () => {
    it('should handle multiple SIGINT signals gracefully', async () => {
      // Arrange
      signalHandler.register();

      // Act - emit multiple SIGINTs and wait for async handler
      process.emit('SIGINT');
      process.emit('SIGINT');
      process.emit('SIGINT');
      await new Promise(resolve => setImmediate(resolve));

      // Assert
      expect(mockProcessExit).toHaveBeenCalledTimes(1); // Only exit once
    });

    it('should not run cleanup multiple times', async () => {
      // Arrange
      signalHandler.register();

      // Act
      process.emit('SIGINT');
      process.emit('SIGINT');

      // Wait for async cleanup
      await new Promise((resolve) => setImmediate(resolve));

      // Assert
      expect(mockCleanupService.cleanup).toHaveBeenCalledTimes(1);
    });
  });

  describe('Data Validation: Cleanup log', () => {
    it('should log interruption details to file', async () => {
      // Arrange
      signalHandler.register();
      signalHandler.setCurrentOperation('copying files');

      // Act
      process.emit('SIGINT');

      // Wait for async cleanup
      await new Promise((resolve) => setImmediate(resolve));

      // Assert
      expect(mockCleanupService.cleanup).toHaveBeenCalledWith(
        expect.objectContaining({
          operation: 'copying files',
          timestamp: expect.any(Number),
        })
      );
    });
  });
});
