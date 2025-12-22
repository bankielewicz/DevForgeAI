/**
 * OutputFormatter - Terminal output formatting service
 *
 * Formats messages with colors and symbols for consistent wizard output.
 * Respects NO_COLOR environment variable and terminal capabilities.
 *
 * @class OutputFormatter
 */

const chalk = require('chalk');

class OutputFormatter {
  constructor(options = {}) {
    this.quiet = options.quiet || false;
    this.useColors = this.shouldUseColors();
    this.useUnicode = this.shouldUseUnicode();
  }

  /**
   * Determine if colors should be used
   * @private
   * @returns {boolean} True if colors should be enabled
   */
  shouldUseColors() {
    // NO_COLOR environment variable disables colors
    if (process.env.NO_COLOR) {
      return false;
    }

    // Check chalk's color support
    if (!chalk.supportsColor) {
      return false;
    }

    return true;
  }

  /**
   * Determine if Unicode symbols should be used
   * @private
   * @returns {boolean} True if Unicode supported
   */
  shouldUseUnicode() {
    // TERM=dumb indicates no Unicode support
    if (process.env.TERM === 'dumb') {
      return false;
    }

    return true;
  }

  /**
   * Get symbol for message type
   * @private
   * @param {string} type - Message type (success, warning, error, info)
   * @returns {string} Symbol character
   */
  getSymbol(type) {
    if (this.useUnicode) {
      const symbols = {
        success: '✓',
        warning: '⚠',
        error: '✗',
        info: '?',
      };
      return symbols[type] || '';
    } else {
      // ASCII fallbacks
      const symbols = {
        success: '[OK]',
        warning: '[WARN]',
        error: '[ERROR]',
        info: '[?]',
      };
      return symbols[type] || '';
    }
  }

  /**
   * Format and output success message (SVC-013)
   * @param {string} message - Message to display
   */
  success(message) {
    if (this.quiet) {
      return; // Suppress in quiet mode
    }

    const symbol = this.getSymbol('success');
    const formattedMessage = `${symbol} ${message}\n`;

    if (this.useColors) {
      process.stdout.write(chalk.green(formattedMessage));
    } else {
      process.stdout.write(formattedMessage);
    }
  }

  /**
   * Format and output warning message (SVC-014)
   * @param {string} message - Message to display
   */
  warning(message) {
    if (this.quiet) {
      return; // Suppress in quiet mode
    }

    const symbol = this.getSymbol('warning');
    const formattedMessage = `${symbol} ${message}\n`;

    if (this.useColors) {
      process.stdout.write(chalk.yellow(formattedMessage));
    } else {
      process.stdout.write(formattedMessage);
    }
  }

  /**
   * Format and output error message (SVC-015)
   * @param {string} message - Message to display
   */
  error(message) {
    // Errors ALWAYS display (even in quiet mode)
    const symbol = this.getSymbol('error');
    const formattedMessage = `${symbol} ${message}\n`;

    if (this.useColors) {
      process.stderr.write(chalk.red(formattedMessage));
    } else {
      process.stderr.write(formattedMessage);
    }
  }

  /**
   * Format and output info message (SVC-016)
   * @param {string} message - Message to display
   */
  info(message) {
    if (this.quiet) {
      return; // Suppress in quiet mode
    }

    const symbol = this.getSymbol('info');
    const formattedMessage = `${symbol} ${message}\n`;

    if (this.useColors) {
      process.stdout.write(chalk.blue(formattedMessage));
    } else {
      process.stdout.write(formattedMessage);
    }
  }
}

module.exports = { OutputFormatter };
