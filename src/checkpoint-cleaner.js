/**
 * Checkpoint Cleaner for DevForgeAI Ideation Sessions
 *
 * STORY-138: Auto-Cleanup Completed Checkpoints
 *
 * Handles:
 * - AC#1: Auto-cleanup on successful completion
 * - AC#2: Preservation on failure (no cleanup called)
 * - AC#3: Manual cleanup command (--clean-checkpoints)
 * - AC#4: Cleanup confirmation with file list
 */

const fs = require('fs');
const path = require('path');

class CheckpointCleaner {
  /**
   * Create a CheckpointCleaner instance
   * @param {Object} logger - Logger instance with info, warn, error methods
   */
  constructor(logger) {
    this.logger = logger || console;
    this.cleanupTimeout = 5000; // Default 5 second timeout
    this.tempDir = path.join(process.cwd(), 'devforgeai', 'temp');
    this.checkpointPattern = /^\.ideation-checkpoint-.*\.yaml$/;
    this._requiresConfirmation = true;
    this._discoveredFiles = [];
  }

  /**
   * AC#1: Clean up checkpoint file on successful completion
   * @param {string} sessionId - The ideation session ID
   * @returns {string|null} - The session ID for confirmation, or null if invalid
   */
  cleanupOnCompletion(sessionId) {
    // Validate sessionId to prevent path traversal
    if (!sessionId || typeof sessionId !== 'string') {
      this.logger.error('Invalid session ID: must be a non-empty string');
      return null;
    }

    // Only allow alphanumeric, dash, underscore (prevents path traversal)
    if (!/^[a-zA-Z0-9_-]+$/.test(sessionId)) {
      this.logger.error(`Invalid session ID format: ${sessionId}`);
      return null;
    }

    const checkpointPath = path.join(
      this.tempDir,
      `.ideation-checkpoint-${sessionId}.yaml`
    );

    try {
      // Check if file exists
      if (!fs.existsSync(checkpointPath)) {
        this.logger.info(`Checkpoint already cleaned or not found: ${sessionId}`);
        return sessionId;
      }

      // Read file to check phase (optional phase validation)
      try {
        const content = fs.readFileSync(checkpointPath, 'utf8');
        if (content.includes('phase: 5') && !content.includes('phase: 6')) {
          this.logger.info(`Warning: Cleaning checkpoint at early phase for session: ${sessionId}`);
        }
      } catch (readErr) {
        // Continue with deletion even if read fails
      }

      // Delete the checkpoint file
      fs.unlinkSync(checkpointPath);
      this.logger.info(`Checkpoint marked for cleanup: ${sessionId}`);
      return sessionId;
    } catch (err) {
      if (err.code === 'ENOENT') {
        this.logger.info(`Checkpoint already cleaned or not found: ${sessionId}`);
        return sessionId;
      }
      if (err.message.includes('EACCES') || err.message.includes('permission')) {
        this.logger.warn(`Permission denied when cleaning checkpoint: ${sessionId}`);
        return sessionId;
      }
      this.logger.error(`Error cleaning checkpoint ${sessionId}: ${err.message}`);
      return sessionId;
    }
  }

  /**
   * AC#3: Discover checkpoint files matching pattern
   * @returns {Array<string>} - Array of checkpoint file paths
   */
  discoverCheckpointFiles() {
    try {
      // Ensure temp directory exists
      if (!fs.existsSync(this.tempDir)) {
        this.logger.info('No checkpoint files found (temp directory does not exist)');
        this._discoveredFiles = [];
        return [];
      }

      // Read directory and filter matching files
      const files = fs.readdirSync(this.tempDir);
      const checkpointFiles = files
        .filter(file => this.checkpointPattern.test(file))
        .map(file => path.join(this.tempDir, file));

      this._discoveredFiles = checkpointFiles;

      if (checkpointFiles.length === 0) {
        this.logger.info('No checkpoint files found matching pattern');
      }

      return checkpointFiles;
    } catch (err) {
      this.logger.error(`Error discovering checkpoints: ${err.message}`);
      this._discoveredFiles = [];
      return [];
    }
  }

  /**
   * Check if confirmation is required for cleanup
   * @returns {boolean}
   */
  requiresConfirmation() {
    return this._requiresConfirmation;
  }

  /**
   * Request confirmation for cleanup
   * @param {number} count - Number of files to clean
   * @returns {boolean} - Always returns false until user confirms
   */
  requestConfirmation(count) {
    this._requiresConfirmation = true;
    return false; // Confirmation pending
  }

  /**
   * Display confirmation prompt with file count
   */
  displayConfirmationPrompt() {
    const count = this._discoveredFiles.length;
    this.logger.info(`Found ${count} checkpoint file(s) to delete`);
  }

  /**
   * AC#3: Clean up all checkpoints with user confirmation
   * @param {boolean} confirmed - Whether user confirmed deletion
   * @param {Object} options - Optional settings (timeout, etc.)
   * @returns {Object} - Result with count, errors, and message
   */
  cleanupAllCheckpointsWithConfirmation(confirmed, options = {}) {
    // If not confirmed, return without deleting
    if (!confirmed) {
      return {
        deleted: 0,
        errors: 0,
        message: 'Cleanup cancelled by user'
      };
    }

    // IMPORTANT: Use the pre-discovered files list
    // This ensures isolation - files created after discovery are NOT deleted
    // If no files were pre-discovered, discover now
    if (this._discoveredFiles.length === 0) {
      this.discoverCheckpointFiles();
    }

    // Copy the list at time of cleanup (isolation from concurrent creation)
    const files = [...this._discoveredFiles];
    const total = files.length;
    let deleted = 0;
    let errors = 0;

    // Report progress for large operations (>10 files)
    const reportProgress = total > 10;
    const progressInterval = Math.max(10, Math.floor(total / 10)); // Report every 10% or every 10 files

    // Delete each file
    for (let i = 0; i < files.length; i++) {
      const filePath = files[i];
      try {
        fs.unlinkSync(filePath);
        deleted++;

        // Report progress for large batches
        if (reportProgress && (deleted % progressInterval === 0 || deleted === total)) {
          const percent = Math.round((deleted / total) * 100);
          this.logger.info(`Cleanup progress: ${deleted}/${total} files (${percent}%)`);
        }
      } catch (err) {
        errors++;
        this.logger.warn(`Failed to delete ${filePath}: ${err.message}`);
      }
    }

    const message = `Removed ${deleted} checkpoint file${deleted !== 1 ? 's' : ''}`;
    this.logger.info(message);

    // Clear discovered files after cleanup
    this._discoveredFiles = [];

    return {
      deleted,
      errors,
      message
    };
  }

  /**
   * AC#4: Display list of checkpoint files with metadata
   * @returns {Array<Object>} - Formatted file list for display
   */
  displayCheckpointList() {
    if (this._discoveredFiles.length === 0) {
      this.discoverCheckpointFiles();
    }

    const fileList = [];

    for (const filePath of this._discoveredFiles) {
      try {
        const stats = fs.statSync(filePath);
        const content = fs.readFileSync(filePath, 'utf8');

        // Extract problem statement preview from YAML content
        let problemPreview = '';
        // Try multiple patterns for problem statement
        const problemMatch = content.match(/problem_statement:\s*"?([^"\n]+)/) ||
                            content.match(/problem:\s*"?([^"\n]+)/);
        if (problemMatch) {
          problemPreview = problemMatch[1].substring(0, 50) + (problemMatch[1].length > 50 ? '...' : '');
        }

        // Extract session ID from filename
        const sessionIdMatch = path.basename(filePath).match(/\.ideation-checkpoint-(.+)\.yaml$/);
        const sessionId = sessionIdMatch ? sessionIdMatch[1] : 'unknown';

        // Extract created_at from content if available
        const createdAtMatch = content.match(/created_at:\s*"?([^"\n]+)/);
        const createdAt = createdAtMatch ? createdAtMatch[1] : stats.mtime.toISOString();

        const fileInfo = {
          path: filePath,
          sessionId,
          timestamp: stats.mtime.toISOString(),
          size: stats.size,
          problemPreview: problemPreview || 'No problem statement found',
          created: createdAt
        };

        fileList.push(fileInfo);

        // Log each file info for display
        this.logger.info(`Session: ${sessionId} | Timestamp: ${createdAt} | Problem: ${fileInfo.problemPreview}`);
      } catch (err) {
        // File might have been deleted or unreadable
        fileList.push({
          path: filePath,
          sessionId: 'unknown',
          timestamp: new Date().toISOString(),
          size: 0,
          problemPreview: 'Unable to read file',
          error: err.message
        });
      }
    }

    // Sort by timestamp (newest first)
    fileList.sort((a, b) => new Date(b.timestamp) - new Date(a.timestamp));

    return fileList;
  }

  /**
   * AC#4: Display list then ask confirmation (combined UX flow)
   * @param {Function} askUserQuestion - AskUserQuestion callback
   * @returns {Object} - Question configuration after displaying list
   */
  displayListThenAskConfirmation(askUserQuestion) {
    // First display the list (logs each file)
    this.displayCheckpointList();

    // Then ask confirmation
    return this.displayConfirmationQuestion(askUserQuestion);
  }

  /**
   * AC#4: Display confirmation question to user
   * @param {Function} askUserQuestion - AskUserQuestion callback
   * @returns {Object} - Question configuration for AskUserQuestion
   */
  displayConfirmationQuestion(askUserQuestion) {
    // Discover files if not already done
    if (this._discoveredFiles.length === 0) {
      this.discoverCheckpointFiles();
    }

    const count = this._discoveredFiles.length;

    const question = {
      question: `Are you sure you want to delete these checkpoint files?`,
      header: `Delete ${count} checkpoint file${count !== 1 ? 's' : ''}?`,
      options: [
        {
          label: 'Yes, delete all',
          description: `Delete all ${count} checkpoint files permanently`
        },
        {
          label: 'No, keep them',
          description: 'Cancel cleanup and preserve all checkpoint files'
        },
        {
          label: 'Select specific files',
          description: 'Choose individual files to delete'
        }
      ],
      multiSelect: false
    };

    if (typeof askUserQuestion === 'function') {
      return askUserQuestion(question);
    }

    return question;
  }

  /**
   * AC#4: Handle user response to cleanup confirmation
   * @param {string} response - User's selection
   * @param {Array<Object>} files - List of checkpoint files
   * @returns {Object} - Result of cleanup operation
   */
  handleUserResponse(response, files) {
    const normalizedResponse = response.toLowerCase();

    if (normalizedResponse.includes('yes') || normalizedResponse.includes('delete all')) {
      // Delete all files
      return this.cleanupAllCheckpointsWithConfirmation(true);
    }

    if (normalizedResponse.includes('no') || normalizedResponse.includes('keep')) {
      // Keep all files
      return {
        deleted: 0,
        errors: 0,
        message: 'Cleanup cancelled - all checkpoint files preserved'
      };
    }

    if (normalizedResponse.includes('select') || normalizedResponse.includes('specific')) {
      // If files provided, delete them; otherwise return for file selection
      if (files && Array.isArray(files) && files.length > 0 && typeof files[0] === 'string') {
        // Files are paths - delete them directly
        return this.deleteSelectedFiles(files);
      }
      // Return file list for selective deletion (user needs to choose)
      return {
        deleted: 0,
        errors: 0,
        message: 'Selective deletion mode - awaiting file selection',
        pendingSelection: true,
        files: files || this.displayCheckpointList()
      };
    }

    // Default: treat as decline
    return {
      deleted: 0,
      errors: 0,
      message: 'Unknown response - no files deleted'
    };
  }

  /**
   * AC#3: Parse --clean-checkpoints flag from command arguments
   * @param {Array<string>} args - Command line arguments
   * @returns {boolean} - True if flag present
   */
  parseCleanupFlag(args) {
    if (!Array.isArray(args)) {
      return false;
    }
    return args.includes('--clean-checkpoints');
  }

  /**
   * Edge case: Set cleanup operation timeout
   * @param {number} ms - Timeout in milliseconds
   */
  setCleanupTimeout(ms) {
    if (typeof ms === 'number' && ms > 0) {
      this.cleanupTimeout = ms;
    }
  }

  /**
   * AC#4: Generate summary of checkpoint files
   * @returns {string} - Summary string with count
   */
  generateCheckpointSummary() {
    if (this._discoveredFiles.length === 0) {
      this.discoverCheckpointFiles();
    }

    const count = this._discoveredFiles.length;
    return `${count} checkpoint file${count !== 1 ? 's' : ''} found`;
  }

  /**
   * AC#2: Check if session is complete (for preservation logic)
   * @param {string} sessionId - Session ID to check
   * @returns {boolean} - True if session completed successfully
   */
  isSessionComplete(sessionId) {
    const checkpointPath = path.join(
      this.tempDir,
      `.ideation-checkpoint-${sessionId}.yaml`
    );

    try {
      if (!fs.existsSync(checkpointPath)) {
        return false;
      }

      const content = fs.readFileSync(checkpointPath, 'utf8');

      // Check if phase is 6 or higher
      const phaseMatch = content.match(/phase:\s*(\d+)/);
      if (phaseMatch) {
        const phase = parseInt(phaseMatch[1], 10);
        return phase >= 6;
      }

      // Check for completion status markers
      if (content.includes('status: completed') ||
          content.includes('phase_6_artifacts_ready') ||
          content.includes('session_complete')) {
        return true;
      }

      return false;
    } catch (err) {
      return false;
    }
  }

  /**
   * AC#4: Select specific files for deletion
   * @param {Array<string>} selectedFiles - File paths to delete
   * @returns {Object} - Result with deleted files and errors
   */
  deleteSelectedFiles(selectedFiles) {
    if (!Array.isArray(selectedFiles) || selectedFiles.length === 0) {
      return {
        deleted: 0,
        errors: 0,
        deletedFiles: [],
        errorFiles: [],
        message: 'No files selected for deletion'
      };
    }

    let deleted = 0;
    let errors = 0;
    const deletedFiles = [];
    const errorFiles = [];

    // Get absolute path of temp directory for path traversal check
    const tempDirAbsolute = path.resolve(this.tempDir);

    for (const filePath of selectedFiles) {
      try {
        // 1. Resolve to absolute path and check for path traversal
        const absolutePath = path.resolve(filePath);
        if (!absolutePath.startsWith(tempDirAbsolute)) {
          errors++;
          errorFiles.push({ path: filePath, error: 'Path is outside checkpoint directory' });
          continue;
        }

        // 2. Validate file matches checkpoint pattern
        const fileName = path.basename(absolutePath);
        if (!this.checkpointPattern.test(fileName)) {
          errors++;
          errorFiles.push({ path: filePath, error: 'Not a valid checkpoint file' });
          continue;
        }

        // 3. Verify file exists
        if (!fs.existsSync(absolutePath)) {
          errors++;
          errorFiles.push({ path: filePath, error: 'File not found' });
          continue;
        }

        // 4. Delete the file
        fs.unlinkSync(absolutePath);
        deleted++;
        deletedFiles.push(absolutePath);
      } catch (err) {
        errors++;
        errorFiles.push({ path: filePath, error: err.message });
      }
    }

    const message = `Deleted ${deleted} of ${selectedFiles.length} selected file${selectedFiles.length !== 1 ? 's' : ''}`;
    this.logger.info(message);

    return {
      deleted,
      errors,
      deletedFiles,
      errorFiles,
      message
    };
  }
}

module.exports = CheckpointCleaner;
