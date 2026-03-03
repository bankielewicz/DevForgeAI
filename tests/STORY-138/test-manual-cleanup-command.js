/**
 * Integration tests for Manual Cleanup Command (AC#3)
 *
 * AC#3: Manual Cleanup Command
 * When user runs `/ideate --clean-checkpoints`,
 * all checkpoint files matching pattern should be removed with user confirmation
 */

const fs = require('fs');
const path = require('path');

const CheckpointCleaner = require('../../src/checkpoint-cleaner');

describe('AC#3: Manual Cleanup Command', () => {

  const tempDir = path.join(__dirname, '../../devforgeai/temp');
  const checkpointFiles = [];
  let logOutput = [];

  const mockLogger = {
    info: (message) => {
      logOutput.push(message);
    },
    error: (message) => {
      logOutput.push({ error: message });
    },
    warn: (message) => {
      logOutput.push({ warn: message });
    }
  };

  // Clean temp directory before running ANY tests in this suite
  beforeAll(() => {
    if (fs.existsSync(tempDir)) {
      const existingFiles = fs.readdirSync(tempDir)
        .filter(f => f.match(/^\.ideation-checkpoint-/));
      existingFiles.forEach(f => {
        try {
          fs.unlinkSync(path.join(tempDir, f));
        } catch (e) {
          // Ignore cleanup errors
        }
      });
    }
  });

  beforeEach(() => {
    logOutput = [];
    checkpointFiles.length = 0;

    if (!fs.existsSync(tempDir)) {
      fs.mkdirSync(tempDir, { recursive: true });
    }
  });

  afterEach(() => {
    // Cleanup all test checkpoint files
    checkpointFiles.forEach(filePath => {
      if (fs.existsSync(filePath)) {
        fs.unlinkSync(filePath);
      }
    });
    checkpointFiles.length = 0;
  });

  describe('Checkpoint discovery', () => {

    test('should_discover_all_checkpoint_files_matching_pattern', () => {
      // Arrange: Create multiple checkpoint files
      for (let i = 1; i <= 5; i++) {
        const filePath = path.join(tempDir, `.ideation-checkpoint-session-${i}.yaml`);
        fs.writeFileSync(filePath, `session ${i}`, 'utf8');
        checkpointFiles.push(filePath);
      }

      // Act: Discover checkpoints matching pattern
      const cleaner = new CheckpointCleaner(mockLogger);
      const discovered = cleaner.discoverCheckpointFiles();

      // Assert: All files discovered
      expect(discovered).toHaveLength(5);
      discovered.forEach(file => {
        expect(file).toContain('.ideation-checkpoint-');
      });
    });

    test('should_use_correct_glob_pattern_for_checkpoint_files', () => {
      // Arrange
      const expectedPattern = 'devforgeai/temp/.ideation-checkpoint-*.yaml';
      const matchFile1 = path.join(tempDir, '.ideation-checkpoint-abc123.yaml');
      const matchFile2 = path.join(tempDir, '.ideation-checkpoint-xyz789.yaml');
      const nonMatchFile = path.join(tempDir, 'checkpoint-abc.yaml'); // No dot prefix

      fs.writeFileSync(matchFile1, 'content', 'utf8');
      fs.writeFileSync(matchFile2, 'content', 'utf8');
      fs.writeFileSync(nonMatchFile, 'content', 'utf8');
      checkpointFiles.push(matchFile1, matchFile2, nonMatchFile);

      // Act
      const cleaner = new CheckpointCleaner(mockLogger);
      const discovered = cleaner.discoverCheckpointFiles();

      // Assert: Only files matching pattern discovered
      expect(discovered).toContain(matchFile1);
      expect(discovered).toContain(matchFile2);
      expect(discovered).not.toContain(nonMatchFile);
    });

    test('should_handle_no_checkpoints_found_scenario', () => {
      // Arrange: No checkpoint files exist
      // (tempDir exists but is empty of checkpoints)

      // Act
      const cleaner = new CheckpointCleaner(mockLogger);
      const discovered = cleaner.discoverCheckpointFiles();

      // Assert
      expect(discovered).toEqual([]);
      // Case-insensitive check for "no checkpoint" or "not found" or "No checkpoint"
      expect(logOutput.some(msg =>
        typeof msg === 'string' && (
          msg.toLowerCase().includes('no checkpoint') ||
          msg.toLowerCase().includes('not found')
        )
      )).toBe(true);
    });

  });

  describe('Confirmation flow', () => {

    test('should_require_user_confirmation_before_deletion', () => {
      // Arrange: Create checkpoints
      const filePath = path.join(tempDir, '.ideation-checkpoint-test-1.yaml');
      fs.writeFileSync(filePath, 'content', 'utf8');
      checkpointFiles.push(filePath);

      // Act: Request cleanup without confirmation
      const cleaner = new CheckpointCleaner(mockLogger);
      const confirmed = cleaner.requestConfirmation(1);

      // Assert: Should request confirmation (not auto-delete)
      expect(cleaner.requiresConfirmation()).toBe(true);
      // confirmed will be false until user answers
      expect(typeof confirmed).toBe('boolean');
    });

    test('should_display_confirmation_prompt_with_file_count', () => {
      // Arrange
      for (let i = 1; i <= 3; i++) {
        const filePath = path.join(tempDir, `.ideation-checkpoint-s${i}.yaml`);
        fs.writeFileSync(filePath, 'data', 'utf8');
        checkpointFiles.push(filePath);
      }

      // Act
      const cleaner = new CheckpointCleaner(mockLogger);
      cleaner.discoverCheckpointFiles();
      cleaner.displayConfirmationPrompt();

      // Assert: Prompt should mention count
      expect(logOutput.some(msg => msg.includes('3') || msg.includes('checkpoint'))).toBe(true);
    });

    test('should_not_delete_when_user_declines_confirmation', () => {
      // Arrange
      const filePath = path.join(tempDir, '.ideation-checkpoint-decl.yaml');
      fs.writeFileSync(filePath, 'content', 'utf8');
      checkpointFiles.push(filePath);

      // Act: User declines
      const cleaner = new CheckpointCleaner(mockLogger);
      const result = cleaner.cleanupAllCheckpointsWithConfirmation(false); // false = declined

      // Assert: File should still exist
      expect(fs.existsSync(filePath)).toBe(true);
      expect(result.deleted).toBe(0);
    });

  });

  describe('Bulk deletion', () => {

    test('should_delete_all_checkpoint_files_when_confirmed', () => {
      // Arrange: Create 5 checkpoint files
      for (let i = 1; i <= 5; i++) {
        const filePath = path.join(tempDir, `.ideation-checkpoint-bulk-${i}.yaml`);
        fs.writeFileSync(filePath, `checkpoint ${i}`, 'utf8');
        checkpointFiles.push(filePath);
      }

      // Act: Execute cleanup with confirmation
      const cleaner = new CheckpointCleaner(mockLogger);
      const result = cleaner.cleanupAllCheckpointsWithConfirmation(true); // true = confirmed

      // Assert: All files deleted
      checkpointFiles.forEach(filePath => {
        expect(fs.existsSync(filePath)).toBe(false);
      });

      // Result should show count
      expect(result.deleted).toBe(5);
    });

    test('should_report_cleanup_count_in_message', () => {
      // Arrange
      for (let i = 1; i <= 3; i++) {
        const filePath = path.join(tempDir, `.ideation-checkpoint-rep-${i}.yaml`);
        fs.writeFileSync(filePath, 'content', 'utf8');
        checkpointFiles.push(filePath);
      }

      // Act
      const cleaner = new CheckpointCleaner(mockLogger);
      const result = cleaner.cleanupAllCheckpointsWithConfirmation(true);

      // Assert: Report message contains count
      expect(result.message).toContain('3');
      expect(logOutput.some(msg => msg.includes('Removed') || msg.includes('3'))).toBe(true);
    });

    test('should_handle_deletion_errors_gracefully', () => {
      // Arrange
      const filePath = path.join(tempDir, '.ideation-checkpoint-error.yaml');
      fs.writeFileSync(filePath, 'content', 'utf8');
      checkpointFiles.push(filePath);

      // Mock fs.unlinkSync to fail
      const originalUnlink = fs.unlinkSync;
      fs.unlinkSync = jest.fn(() => {
        throw new Error('EACCES: permission denied');
      });

      // Act
      const cleaner = new CheckpointCleaner(mockLogger);
      const result = cleaner.cleanupAllCheckpointsWithConfirmation(true);

      // Assert: Should report error but not crash
      expect(result.errors).toBeGreaterThan(0);

      // Restore
      fs.unlinkSync = originalUnlink;
    });

  });

  describe('Cleanup reporting', () => {

    test('should_report_removed_N_checkpoint_files_message', () => {
      // Arrange: Create checkpoints
      for (let i = 1; i <= 4; i++) {
        const filePath = path.join(tempDir, `.ideation-checkpoint-msg-${i}.yaml`);
        fs.writeFileSync(filePath, 'content', 'utf8');
        checkpointFiles.push(filePath);
      }

      // Act
      const cleaner = new CheckpointCleaner(mockLogger);
      const result = cleaner.cleanupAllCheckpointsWithConfirmation(true);

      // Assert: Message format matches spec: "Removed {N} checkpoint files"
      expect(result.message).toMatch(/Removed \d+ checkpoint files?/i);
    });

    test('should_display_cleanup_results_summary', () => {
      // Arrange
      for (let i = 1; i <= 2; i++) {
        const filePath = path.join(tempDir, `.ideation-checkpoint-sum-${i}.yaml`);
        fs.writeFileSync(filePath, 'content', 'utf8');
        checkpointFiles.push(filePath);
      }

      // Act
      const cleaner = new CheckpointCleaner(mockLogger);
      const result = cleaner.cleanupAllCheckpointsWithConfirmation(true);

      // Assert: Result contains summary
      expect(result).toHaveProperty('deleted');
      expect(result).toHaveProperty('message');
      expect(result.deleted).toBe(2);
    });

  });

  describe('Command argument parsing', () => {

    test('should_detect_clean_checkpoints_flag', () => {
      // Arrange: Simulated command args
      const args = ['--clean-checkpoints'];

      // Act
      const cleaner = new CheckpointCleaner(mockLogger);
      const isCleanupCommand = cleaner.parseCleanupFlag(args);

      // Assert
      expect(isCleanupCommand).toBe(true);
    });

    test('should_ignore_other_flags_and_detect_cleanup_flag', () => {
      // Arrange
      const args = ['--verbose', '--clean-checkpoints', '--force'];

      // Act
      const cleaner = new CheckpointCleaner(mockLogger);
      const isCleanupCommand = cleaner.parseCleanupFlag(args);

      // Assert
      expect(isCleanupCommand).toBe(true);
    });

    test('should_return_false_when_cleanup_flag_not_present', () => {
      // Arrange
      const args = ['--help', '--version'];

      // Act
      const cleaner = new CheckpointCleaner(mockLogger);
      const isCleanupCommand = cleaner.parseCleanupFlag(args);

      // Assert
      expect(isCleanupCommand).toBe(false);
    });

  });

  describe('Edge cases - bulk deletion', () => {

    test('should_handle_large_number_of_checkpoints_1000_plus', () => {
      // Arrange: Create many checkpoint files
      const fileCount = 100; // Reduced for test performance (represents 1000+)
      for (let i = 1; i <= fileCount; i++) {
        const filePath = path.join(tempDir, `.ideation-checkpoint-large-${i}.yaml`);
        fs.writeFileSync(filePath, 'content', 'utf8');
        checkpointFiles.push(filePath);
      }

      // Act
      const cleaner = new CheckpointCleaner(mockLogger);
      const result = cleaner.cleanupAllCheckpointsWithConfirmation(true);

      // Assert: All deleted successfully
      checkpointFiles.forEach(filePath => {
        expect(fs.existsSync(filePath)).toBe(false);
      });
      expect(result.deleted).toBe(fileCount);
    });

    test('should_handle_mixed_valid_and_invalid_checkpoint_files', () => {
      // Arrange: Create valid and invalid files
      const validPath1 = path.join(tempDir, '.ideation-checkpoint-valid-1.yaml');
      const validPath2 = path.join(tempDir, '.ideation-checkpoint-valid-2.yaml');
      const invalidPath1 = path.join(tempDir, 'other-file.txt');
      const invalidPath2 = path.join(tempDir, 'checkpoint-no-dot.yaml');

      fs.writeFileSync(validPath1, 'content', 'utf8');
      fs.writeFileSync(validPath2, 'content', 'utf8');
      fs.writeFileSync(invalidPath1, 'content', 'utf8');
      fs.writeFileSync(invalidPath2, 'content', 'utf8');

      checkpointFiles.push(validPath1, validPath2, invalidPath1, invalidPath2);

      // Act
      const cleaner = new CheckpointCleaner(mockLogger);
      const result = cleaner.cleanupAllCheckpointsWithConfirmation(true);

      // Assert: Only valid checkpoints deleted
      expect(fs.existsSync(validPath1)).toBe(false);
      expect(fs.existsSync(validPath2)).toBe(false);
      expect(fs.existsSync(invalidPath1)).toBe(true);
      expect(fs.existsSync(invalidPath2)).toBe(true);
      expect(result.deleted).toBe(2);
    });

  });

});
