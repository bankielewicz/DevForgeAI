/**
 * SignalHandler - Graceful interrupt handling
 *
 * Handles SIGINT (Ctrl+C) to ensure clean shutdown with no partial writes.
 * Performs cleanup and displays cancellation message before exit.
 *
 * @class SignalHandler
 */

class SignalHandler {
  constructor(options = {}) {
    this.outputFormatter = options.outputFormatter;
    this.cleanupService = options.cleanupService;
    this.currentOperation = null;
    this.trackedFiles = [];
    this.capturedState = {};
    this.operations = [];
    this.isHandling = false; // Prevent multiple SIGINT handling
    this.boundHandler = null;
  }

  /**
   * Register SIGINT handler (SVC-019)
   */
  register() {
    // Create bound handler for removal later
    this.boundHandler = this.handleSIGINT.bind(this);
    process.on('SIGINT', this.boundHandler);
  }

  /**
   * Unregister SIGINT handler
   */
  unregister() {
    if (this.boundHandler) {
      process.removeListener('SIGINT', this.boundHandler);
      this.boundHandler = null;
    }
  }

  /**
   * Handle SIGINT signal (SVC-019, SVC-020, SVC-021)
   * @private
   */
  async handleSIGINT() {
    // Prevent multiple SIGINT handling
    if (this.isHandling) {
      return;
    }
    this.isHandling = true;

    // Display cancellation message first (SVC-021)
    this.outputFormatter.error('✗ Installation cancelled by user');

    try {
      // Stop current operations immediately (SVC-020)
      this.abortOperations();

      // Perform cleanup (SVC-020)
      await this.cleanup();
    } catch (cleanupError) {
      // Log cleanup error but still exit
      this.outputFormatter.warning(
        `Cleanup failed: ${cleanupError.message}`
      );
    } finally {
      // Exit with code 130 (128 + SIGINT signal 2)
      process.exit(130);
    }
  }

  /**
   * Set current operation name
   * @param {string} operation - Operation description
   */
  setCurrentOperation(operation) {
    this.currentOperation = operation;
  }

  /**
   * Track file for cleanup on interrupt
   * @param {string} filePath - File path to track
   */
  trackFile(filePath) {
    if (!this.trackedFiles.includes(filePath)) {
      this.trackedFiles.push(filePath);
    }
  }

  /**
   * Capture state for restoration
   * @param {Object} state - State object to capture
   */
  captureState(state) {
    this.capturedState = { ...this.capturedState, ...state };
  }

  /**
   * Register abortable operation
   * @param {Function} operation - Operation to register
   */
  registerOperation(operation) {
    this.operations.push(operation);
  }

  /**
   * Abort all registered operations (SVC-020)
   * @private
   */
  abortOperations() {
    this.operations.forEach((operation) => {
      try {
        operation('abort');
      } catch (error) {
        // Ignore errors during abort
      }
    });
    this.operations = [];
  }

  /**
   * Perform cleanup (SVC-020)
   * @private
   * @returns {Promise<void>}
   */
  async cleanup() {
    if (!this.cleanupService) {
      return;
    }

    const cleanupData = {
      operation: this.currentOperation,
      timestamp: Date.now(),
    };

    // Call cleanup service
    await this.cleanupService.cleanup(cleanupData);

    // Remove partial files
    if (this.trackedFiles.length > 0) {
      await this.cleanupService.removePartialFiles(this.trackedFiles);
    }

    // Restore original state if captured
    if (Object.keys(this.capturedState).length > 0) {
      await this.cleanupService.restoreOriginalState(this.capturedState);
    }
  }
}

module.exports = { SignalHandler };
