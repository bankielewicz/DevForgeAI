/**
 * ProgressService - Progress indicators for wizard operations
 *
 * Displays spinners for indeterminate operations and progress bars for
 * determinate operations. Respects --quiet flag and terminal capabilities.
 *
 * @class ProgressService
 */

const ora = require('ora');
const cliProgress = require('cli-progress');

class ProgressService {
  constructor(options = {}) {
    this.quiet = options.quiet || false;
    this.spinner = null;
    this.progressBar = null;
    this.spinnerTimeout = null;
    this.spinnerDelayMs = 200; // SVC-009: Start spinner after 200ms
  }

  /**
   * Start spinner for indeterminate operations (SVC-009)
   * Only displays if operation exceeds 200ms threshold
   *
   * @param {string} text - Spinner text to display
   */
  startSpinner(text) {
    if (this.quiet) {
      return; // No spinner in quiet mode
    }

    // Configure spinner options
    const spinnerOptions = {
      text,
      interval: 16, // 60 FPS (NFR-002)
    };

    // Windows platform uses ASCII fallback
    if (process.platform === 'win32') {
      spinnerOptions.spinner = {
        frames: ['|', '/', '-', '\\'],
        interval: 100,
      };
    }

    // Create spinner but don't start yet
    this.spinner = ora(spinnerOptions);

    // Start spinner after 200ms delay
    this.spinnerTimeout = setTimeout(() => {
      if (this.spinner) {
        this.spinner.start();
      }
    }, this.spinnerDelayMs);
  }

  /**
   * Stop spinner (SVC-009)
   *
   * @param {Object} options - Options for stopping
   * @param {boolean} options.success - Whether operation succeeded
   * @param {string} options.message - Optional message to display
   */
  stopSpinner(options = {}) {
    // Clear timeout if spinner hasn't started yet
    if (this.spinnerTimeout) {
      clearTimeout(this.spinnerTimeout);
      this.spinnerTimeout = null;
    }

    if (!this.spinner || this.quiet) {
      return;
    }

    // Stop with success or failure
    if (options.success === true) {
      this.spinner.succeed(options.message);
    } else if (options.success === false) {
      this.spinner.fail(options.message || 'Failed');
    } else {
      this.spinner.stop();
    }

    this.spinner = null;
  }

  /**
   * Update spinner text (SVC-011)
   *
   * @param {string} text - New text to display
   */
  updateSpinnerText(text) {
    if (this.quiet || !this.spinner) {
      return;
    }

    this.spinner.text = text;
  }

  /**
   * Start progress bar for determinate operations (SVC-010)
   *
   * @param {Object} options - Progress bar options
   * @param {number} options.total - Total number of items
   * @param {string} options.format - Format string (optional)
   */
  startProgressBar(options) {
    if (this.quiet) {
      return; // No progress bar in quiet mode
    }

    const { total, format } = options;

    // Default format string
    let formatString =
      format || '{bar} | {percentage}% | {value}/{total} files';

    // For narrow terminals (<40 columns), use percentage only
    if (process.stdout.columns && process.stdout.columns < 40) {
      formatString = '{percentage}%';
    }

    // Create progress bar
    this.progressBar = new cliProgress.SingleBar(
      {
        format: formatString,
        hideCursor: true,
        clearOnComplete: false,
      },
      cliProgress.Presets.shades_classic
    );

    this.progressBar.start(total, 0);
  }

  /**
   * Update progress bar (SVC-010)
   *
   * @param {number} current - Current progress value
   */
  updateProgress(current) {
    if (this.quiet || !this.progressBar) {
      return;
    }

    this.progressBar.update(current);
  }

  /**
   * Stop progress bar (SVC-010)
   */
  stopProgressBar() {
    if (this.quiet || !this.progressBar) {
      return;
    }

    this.progressBar.stop();
    this.progressBar = null;
  }
}

module.exports = { ProgressService };
