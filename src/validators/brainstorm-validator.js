/**
 * STORY-140: Brainstorm YAML Validator
 *
 * Validates brainstorm file YAML syntax and schema for the spec-driven-ideation skill.
 *
 * Features:
 * - AC#1: YAML validation on brainstorm load
 * - AC#2: Clear error messages with file path and line numbers
 * - AC#3: Graceful fallback support (never throws, returns error object)
 * - AC#4: Detection of 5 common YAML error types
 * - AC#5: Schema validation for required and optional fields
 */

const fs = require('fs');
const path = require('path');

/**
 * Error types for YAML validation failures
 */
const ErrorTypes = {
  UNCLOSED_FRONTMATTER: 'UNCLOSED_FRONTMATTER',
  INVALID_INDENTATION: 'INVALID_INDENTATION',
  DUPLICATE_KEY: 'DUPLICATE_KEY',
  INVALID_DATE_FORMAT: 'INVALID_DATE_FORMAT',
  MISSING_REQUIRED_FIELD: 'MISSING_REQUIRED_FIELD',
  INVALID_STATUS_ENUM: 'INVALID_STATUS_ENUM',
  INVALID_ID_PATTERN: 'INVALID_ID_PATTERN',
  YAML_PARSE_ERROR: 'YAML_PARSE_ERROR',
  EMPTY_FILE: 'EMPTY_FILE',
  BINARY_FILE: 'BINARY_FILE',
  FILE_NOT_FOUND: 'FILE_NOT_FOUND'
};

/**
 * Valid status enum values for brainstorm files
 */
const VALID_STATUSES = ['Active', 'Complete', 'Abandoned'];

/**
 * Required fields in brainstorm YAML frontmatter
 */
const REQUIRED_FIELDS = ['id', 'title', 'status', 'created'];

/**
 * Maps YAML parser errors to user-friendly messages
 */
class YAMLErrorMapper {
  /**
   * Maps a YAML error to a user-friendly error object
   * @param {Object} yamlError - The YAML parsing error
   * @returns {Object} Mapped error with type, message, and lineNumber
   */
  static mapError(yamlError) {
    if (!yamlError) {
      return {
        type: ErrorTypes.YAML_PARSE_ERROR,
        message: 'Unknown YAML error',
        lineNumber: null
      };
    }

    const errorMessage = yamlError.message || String(yamlError);

    // Detect specific error types from error message
    if (errorMessage.includes('duplicate key') || errorMessage.includes('Duplicate key')) {
      const lineMatch = errorMessage.match(/line (\d+)/i);
      const keyMatch = errorMessage.match(/'([^']+)'/);
      return {
        type: ErrorTypes.DUPLICATE_KEY,
        message: `Duplicate key '${keyMatch ? keyMatch[1] : 'unknown'}' detected`,
        lineNumber: lineMatch ? parseInt(lineMatch[1], 10) : null
      };
    }

    if (errorMessage.includes('indentation') || errorMessage.includes('tab')) {
      const lineMatch = errorMessage.match(/line (\d+)/i);
      return {
        type: ErrorTypes.INVALID_INDENTATION,
        message: 'Invalid indentation - use spaces only (no tabs)',
        lineNumber: lineMatch ? parseInt(lineMatch[1], 10) : null
      };
    }

    // Default YAML parse error
    const lineMatch = errorMessage.match(/line (\d+)/i);
    return {
      type: ErrorTypes.YAML_PARSE_ERROR,
      message: errorMessage,
      lineNumber: lineMatch ? parseInt(lineMatch[1], 10) : null
    };
  }
}

/**
 * Validates brainstorm file YAML syntax and schema
 */
class BrainstormValidator {
  /**
   * Finds the first occurrence of a YAML delimiter (---) starting from a given line
   * @private
   * @param {string[]} lines - Array of file lines
   * @param {number} startIndex - Starting index for search
   * @returns {number} Line index of delimiter, or -1 if not found
   */
  static _findDelimiter(lines, startIndex = 0) {
    for (let i = startIndex; i < lines.length; i++) {
      if (lines[i].trim() === '---') {
        return i;
      }
    }
    return -1;
  }

  /**
   * Calculates absolute line number in file from offset relative to opening delimiter
   * @private
   * @param {number} openingDelimiterLine - Line number of opening delimiter (0-indexed)
   * @param {number} offset - Offset from opening delimiter (0-indexed)
   * @returns {number} Absolute line number (1-indexed for display)
   */
  static _getAbsoluteLineNumber(openingDelimiterLine, offset) {
    return openingDelimiterLine + 2 + offset;
  }

  /**
   * Removes surrounding quotes from a value if present
   * @private
   * @param {string} value - Value potentially surrounded by quotes
   * @returns {string} Value with quotes removed if applicable
   */
  static _stripQuotes(value) {
    if ((value.startsWith('"') && value.endsWith('"')) ||
        (value.startsWith("'") && value.endsWith("'"))) {
      return value.slice(1, -1);
    }
    return value;
  }

  /**
   * Main validation entry point
   * @param {string} filePath - Path to the brainstorm file
   * @returns {Object} Validation result with valid, metadata, or error
   */
  static validate(filePath) {
    try {
      // Check if file exists
      if (!fs.existsSync(filePath)) {
        return this._createErrorResult(
          ErrorTypes.FILE_NOT_FOUND,
          `File not found: ${filePath}`,
          filePath,
          null
        );
      }

      // Read file content
      let content;
      try {
        content = fs.readFileSync(filePath, 'utf8');
      } catch (readError) {
        // Check for binary/encoding issues
        return this._createErrorResult(
          ErrorTypes.BINARY_FILE,
          'File appears to be binary or has encoding issues - cannot read as text',
          filePath,
          null
        );
      }

      // Check for empty file
      if (!content || content.trim().length === 0) {
        return this._createErrorResult(
          ErrorTypes.EMPTY_FILE,
          'File is empty - brainstorm files require YAML frontmatter',
          filePath,
          null
        );
      }

      // Check for binary content (null bytes)
      if (content.includes('\x00')) {
        return this._createErrorResult(
          ErrorTypes.BINARY_FILE,
          'File contains binary content - cannot parse as text',
          filePath,
          null
        );
      }

      // Validate YAML syntax
      const yamlResult = this.validateYAML(content, filePath);
      if (!yamlResult.valid) {
        return yamlResult;
      }

      // Validate schema
      const schemaResult = this.validateSchema(yamlResult.frontmatter);
      if (!schemaResult.valid) {
        return this._createErrorResult(
          schemaResult.errorType,
          schemaResult.message,
          filePath,
          schemaResult.lineNumber
        );
      }

      // Success - return valid result with metadata
      return {
        valid: true,
        metadata: yamlResult.frontmatter
      };

    } catch (error) {
      // Catch-all for unexpected errors (graceful fallback - AC#3)
      return this._createErrorResult(
        ErrorTypes.YAML_PARSE_ERROR,
        `Unexpected error: ${error.message}`,
        filePath,
        null
      );
    }
  }

  /**
   * Validates YAML syntax of the file content
   * @param {string} content - File content
   * @param {string} filePath - Path to the file (for error messages)
   * @returns {Object} Result with valid, frontmatter, or error
   */
  static validateYAML(content, filePath) {
    const lines = content.split('\n');

    // Find opening delimiter
    const openingDelimiterLine = this._findDelimiter(lines);
    if (openingDelimiterLine === -1) {
      return this._createErrorResult(
        ErrorTypes.UNCLOSED_FRONTMATTER,
        'Missing YAML frontmatter - file must start with ---',
        filePath,
        1
      );
    }

    // Find closing delimiter
    const closingDelimiterLine = this._findDelimiter(lines, openingDelimiterLine + 1);
    if (closingDelimiterLine === -1) {
      return this._createErrorResult(
        ErrorTypes.UNCLOSED_FRONTMATTER,
        'Unclosed YAML frontmatter - missing closing --- delimiter',
        filePath,
        openingDelimiterLine + 1
      );
    }

    // Extract frontmatter content
    const frontmatterLines = lines.slice(openingDelimiterLine + 1, closingDelimiterLine);

    // Check for tabs (invalid indentation)
    for (let i = 0; i < frontmatterLines.length; i++) {
      if (frontmatterLines[i].includes('\t')) {
        const lineNumber = this._getAbsoluteLineNumber(openingDelimiterLine, i);
        return this._createErrorResult(
          ErrorTypes.INVALID_INDENTATION,
          `Invalid indentation at line ${lineNumber} - use spaces only (no tabs)`,
          filePath,
          lineNumber
        );
      }
    }

    // Parse YAML (simple key-value parser for frontmatter)
    const frontmatter = {};
    const seenKeys = new Set();

    for (let i = 0; i < frontmatterLines.length; i++) {
      const line = frontmatterLines[i];
      const lineNumber = this._getAbsoluteLineNumber(openingDelimiterLine, i);

      // Skip empty lines and comments
      if (line.trim() === '' || line.trim().startsWith('#')) {
        continue;
      }

      // Handle array items (e.g., user_personas:, followed by - items)
      if (line.trim().startsWith('-')) {
        continue; // Array items handled with parent key
      }

      // Parse key: value
      const colonIndex = line.indexOf(':');
      if (colonIndex === -1) {
        continue; // Not a key-value line
      }

      const key = line.substring(0, colonIndex).trim();
      let value = line.substring(colonIndex + 1).trim();

      // Check for duplicate keys
      if (seenKeys.has(key)) {
        return this._createErrorResult(
          ErrorTypes.DUPLICATE_KEY,
          `Duplicate key '${key}' at line ${lineNumber}`,
          filePath,
          lineNumber
        );
      }
      seenKeys.add(key);

      // Remove quotes from value
      value = this._stripQuotes(value);

      // Handle array values (collect subsequent - items)
      if (value === '' || value === '|' || value === '>') {
        // Check for array items following this key
        const arrayItems = [];
        for (let j = i + 1; j < frontmatterLines.length; j++) {
          const arrayLine = frontmatterLines[j].trim();
          if (arrayLine.startsWith('-')) {
            arrayItems.push(arrayLine.substring(1).trim().replace(/^["']|["']$/g, ''));
          } else if (arrayLine !== '' && !arrayLine.startsWith('#')) {
            break;
          }
        }
        if (arrayItems.length > 0) {
          frontmatter[key] = arrayItems;
        } else {
          frontmatter[key] = value;
        }
      } else {
        frontmatter[key] = value;
      }
    }

    return {
      valid: true,
      frontmatter
    };
  }

  /**
   * Validates required fields exist and are non-empty
   * @private
   * @param {Object} frontmatter - Parsed YAML frontmatter
   * @returns {Object|null} Error object if validation fails, null if valid
   */
  static _validateRequiredFields(frontmatter) {
    for (const field of REQUIRED_FIELDS) {
      if (!frontmatter[field] || frontmatter[field] === '') {
        return {
          valid: false,
          errorType: ErrorTypes.MISSING_REQUIRED_FIELD,
          message: `Missing required field: ${field}`,
          lineNumber: null
        };
      }
    }
    return null;
  }

  /**
   * Validates id field pattern
   * @private
   * @param {string} id - ID value to validate
   * @returns {Object|null} Error object if validation fails, null if valid
   */
  static _validateIdFormat(id) {
    const idPattern = /^BRAINSTORM-\d+$/;
    if (!idPattern.test(id)) {
      return {
        valid: false,
        errorType: ErrorTypes.INVALID_ID_PATTERN,
        message: `Invalid id format: expected BRAINSTORM-NNN, got '${id}'`,
        lineNumber: null
      };
    }
    return null;
  }

  /**
   * Validates status field is a valid enum value
   * @private
   * @param {string} status - Status value to validate
   * @returns {Object|null} Error object if validation fails, null if valid
   */
  static _validateStatusEnum(status) {
    if (!VALID_STATUSES.includes(status)) {
      return {
        valid: false,
        errorType: ErrorTypes.INVALID_STATUS_ENUM,
        message: `Invalid status: must be one of [${VALID_STATUSES.join(', ')}], got '${status}'`,
        lineNumber: null
      };
    }
    return null;
  }

  /**
   * Validates created field is a valid YYYY-MM-DD date
   * @private
   * @param {string} created - Date string to validate
   * @returns {Object|null} Error object if validation fails, null if valid
   */
  static _validateDateFormat(created) {
    const datePattern = /^\d{4}-\d{2}-\d{2}$/;
    if (!datePattern.test(created)) {
      return {
        valid: false,
        errorType: ErrorTypes.INVALID_DATE_FORMAT,
        message: `Invalid date format for 'created' field: expected YYYY-MM-DD, got '${created}'`,
        lineNumber: null
      };
    }
    return null;
  }

  /**
   * Validates optional fields if present
   * @private
   * @param {Object} frontmatter - Parsed YAML frontmatter
   * @returns {Object|null} Error object if validation fails, null if valid
   */
  static _validateOptionalFields(frontmatter) {
    if (frontmatter.problem_statement !== undefined && typeof frontmatter.problem_statement !== 'string') {
      return {
        valid: false,
        errorType: ErrorTypes.YAML_PARSE_ERROR,
        message: `Invalid type for 'problem_statement': expected string`,
        lineNumber: null
      };
    }

    if (frontmatter.key_challenges !== undefined && !Array.isArray(frontmatter.key_challenges)) {
      return {
        valid: false,
        errorType: ErrorTypes.YAML_PARSE_ERROR,
        message: `Invalid type for 'key_challenges': expected array`,
        lineNumber: null
      };
    }

    if (frontmatter.personas !== undefined && !Array.isArray(frontmatter.personas)) {
      return {
        valid: false,
        errorType: ErrorTypes.YAML_PARSE_ERROR,
        message: `Invalid type for 'personas': expected array`,
        lineNumber: null
      };
    }

    return null;
  }

  /**
   * Validates the schema of parsed frontmatter
   * @param {Object} frontmatter - Parsed YAML frontmatter
   * @returns {Object} Result with valid or error details
   */
  static validateSchema(frontmatter) {
    // Validate required fields (fail-fast on first error - AC#5)
    let error = this._validateRequiredFields(frontmatter);
    if (error) return error;

    // Validate required field formats
    error = this._validateIdFormat(frontmatter.id);
    if (error) return error;

    error = this._validateStatusEnum(frontmatter.status);
    if (error) return error;

    error = this._validateDateFormat(frontmatter.created);
    if (error) return error;

    // Validate optional fields if present
    error = this._validateOptionalFields(frontmatter);
    if (error) return error;

    return { valid: true };
  }

  /**
   * Formats an error message for display to the user (AC#2)
   * @param {Object} error - Error object with type, message, lineNumber
   * @param {string} filePath - Path to the file
   * @param {number|null} lineNumber - Line number where error occurred
   * @returns {string} Formatted user-friendly error message
   */
  static formatErrorMessage(error, filePath, lineNumber) {
    let message = `⚠️ Brainstorm file has invalid YAML\n\n`;
    message += `File: ${filePath}\n`;
    message += `Error: ${error.message || error}\n`;

    if (lineNumber !== null && lineNumber !== undefined) {
      message += `Line: ${lineNumber}\n`;
    }

    message += `\nThe file cannot be loaded in its current state.`;

    return message;
  }

  /**
   * Creates a standardized error result object
   * @private
   */
  static _createErrorResult(type, message, filePath, lineNumber) {
    return {
      valid: false,
      error: {
        type,
        message,
        userMessage: this.formatErrorMessage({ message }, filePath, lineNumber),
        lineNumber,
        canContinueWithoutBrainstorm: true
      }
    };
  }
}

module.exports = {
  BrainstormValidator,
  YAMLErrorMapper,
  ErrorTypes,
  VALID_STATUSES,
  REQUIRED_FIELDS
};
