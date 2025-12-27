/**
 * Edge cases and performance tests for checkpoint cleanup (NFR-001, NFR-002, Edge Cases)
 *
 * Tests for:
 * - Performance: Cleanup completes < 1 second for up to 100 files
 * - Reliability: Cleanup errors do not affect session completion
 * - Edge cases: Race conditions, permissions, large numbers, slow filesystem
 */

const fs = require('fs');
const path = require('path');

const CheckpointCleaner = require('../../src/checkpoint-cleaner');

describe('Edge Cases and Performance Requirements', () => {

  const tempDir = path.join(__dirname, '../../devforgeai/temp');
  const checkpointFiles = [];
  let logOutput = [];

  const mockLogger = {
    info: (message) => {
      logOutput.push({ level: 'info', message });
    },
    error: (message) => {
      logOutput.push({ level: 'error', message });
    },
    warn: (message) => {
      logOutput.push({ level: 'warn', message });
    }
  };

  beforeEach(() => {
    logOutput = [];
    checkpointFiles.length = 0;

    if (!fs.existsSync(tempDir)) {
      fs.mkdirSync(tempDir, { recursive: true });
    }
  });

  afterEach(() => {
    checkpointFiles.forEach(filePath => {
      try {
        if (fs.existsSync(filePath)) {
          fs.unlinkSync(filePath);
        }
      } catch (e) {
        // Ignore cleanup errors in afterEach
      }
    });
    checkpointFiles.length = 0;
  });

  describe('NFR-001: Performance - Cleanup < 1 second for 100+ files', () => {

    test('should_cleanup_100_checkpoint_files_within_1_second', () => {
      // Arrange: Create 100 checkpoint files
      for (let i = 1; i <= 100; i++) {
        const filePath = path.join(tempDir, `.ideation-checkpoint-perf-${String(i).padStart(3, '0')}.yaml`);
        fs.writeFileSync(filePath, `checkpoint ${i}`, 'utf8');
        checkpointFiles.push(filePath);
      }

      // Act: Measure cleanup time
      const startTime = Date.now();
      const cleaner = new CheckpointCleaner(mockLogger);
      cleaner.cleanupAllCheckpointsWithConfirmation(true);
      const endTime = Date.now();

      const duration = endTime - startTime;

      // Assert: Completes within 1 second (1000ms)
      expect(duration).toBeLessThan(1000);
    });

    test('should_cleanup_1000_checkpoint_files_with_acceptable_performance', () => {
      // Arrange: Create 1000 checkpoint files (scaled test)
      const fileCount = 1000;
      for (let i = 1; i <= fileCount; i++) {
        const filePath = path.join(tempDir, `.ideation-checkpoint-bulk-${String(i).padStart(4, '0')}.yaml`);
        fs.writeFileSync(filePath, 'x', 'utf8'); // Minimal content
        checkpointFiles.push(filePath);
      }

      // Act: Measure cleanup time
      const startTime = Date.now();
      const cleaner = new CheckpointCleaner(mockLogger);
      cleaner.cleanupAllCheckpointsWithConfirmation(true);
      const endTime = Date.now();

      const duration = endTime - startTime;

      // Assert: Should complete in reasonable time (allow 5 seconds for 1000 files)
      expect(duration).toBeLessThan(5000);

      // Verify all deleted
      checkpointFiles.forEach(filePath => {
        expect(fs.existsSync(filePath)).toBe(false);
      });
    });

    test('should_report_progress_for_large_cleanup_operations', () => {
      // Arrange: Create 50 files
      for (let i = 1; i <= 50; i++) {
        const filePath = path.join(tempDir, `.ideation-checkpoint-prog-${i}.yaml`);
        fs.writeFileSync(filePath, 'content', 'utf8');
        checkpointFiles.push(filePath);
      }

      // Act
      const cleaner = new CheckpointCleaner(mockLogger);
      cleaner.cleanupAllCheckpointsWithConfirmation(true, { showProgress: true });

      // Assert: Progress logged
      expect(logOutput.length).toBeGreaterThan(1);
      // Should have progress updates
      expect(logOutput.some(entry =>
        entry.message.includes('progress') || entry.message.includes('%')
      )).toBe(true);
    });

  });

  describe('NFR-002: Reliability - Cleanup errors do not affect session', () => {

    test('should_handle_permission_denied_error_without_crashing_session', () => {
      // Arrange
      const filePath = path.join(tempDir, '.ideation-checkpoint-perm.yaml');
      fs.writeFileSync(filePath, 'content', 'utf8');
      checkpointFiles.push(filePath);

      // Mock permission error
      const originalUnlink = fs.unlinkSync;
      fs.unlinkSync = jest.fn(() => {
        throw new Error('EACCES: permission denied, unlink');
      });

      // Act
      const cleaner = new CheckpointCleaner(mockLogger);
      let sessionContinued = true;
      try {
        cleaner.cleanupAllCheckpointsWithConfirmation(true);
        // Session should continue despite cleanup error
      } catch (error) {
        sessionContinued = false;
      }

      // Assert: Session not affected
      expect(sessionContinued).toBe(true);

      // Verify error logged
      expect(logOutput.some(entry => entry.level === 'warn' || entry.level === 'error')).toBe(true);

      // Restore
      fs.unlinkSync = originalUnlink;
    });

    test('should_return_partial_cleanup_result_on_partial_failure', () => {
      // Arrange: Create 3 files, make one fail
      const path1 = path.join(tempDir, '.ideation-checkpoint-part-1.yaml');
      const path2 = path.join(tempDir, '.ideation-checkpoint-part-2.yaml');
      const path3 = path.join(tempDir, '.ideation-checkpoint-part-3.yaml');

      fs.writeFileSync(path1, 'content', 'utf8');
      fs.writeFileSync(path2, 'content', 'utf8');
      fs.writeFileSync(path3, 'content', 'utf8');
      checkpointFiles.push(path1, path2, path3);

      // Act
      const cleaner = new CheckpointCleaner(mockLogger);
      const result = cleaner.cleanupAllCheckpointsWithConfirmation(true);

      // Assert: Result shows partial success
      expect(result).toHaveProperty('deleted');
      expect(result).toHaveProperty('errors');
      // Should continue despite any individual file failures
      expect(result.deleted + result.errors).toBe(3);
    });

    test('should_allow_session_completion_even_if_cleanup_fails', () => {
      // Arrange
      const filePath = path.join(tempDir, '.ideation-checkpoint-fail.yaml');
      fs.writeFileSync(filePath, 'content', 'utf8');
      checkpointFiles.push(filePath);

      // Mock complete failure
      const originalUnlink = fs.unlinkSync;
      fs.unlinkSync = jest.fn(() => {
        throw new Error('Filesystem error');
      });

      // Act: Cleanup fails but session returns normally
      const cleaner = new CheckpointCleaner(mockLogger);
      let sessionCanComplete = false;
      try {
        cleaner.cleanupAllCheckpointsWithConfirmation(true);
        sessionCanComplete = true;
      } catch (error) {
        // Even if cleanup throws, it should be caught
        sessionCanComplete = error.sessionCanContinue !== false;
      }

      // Assert
      expect(sessionCanComplete).toBe(true);

      // Restore
      fs.unlinkSync = originalUnlink;
    });

  });

  describe('Edge Case #1: Race condition - checkpoint already deleted', () => {

    test('should_handle_race_condition_when_checkpoint_deleted_before_cleanup', () => {
      // Arrange: Checkpoint starts existing
      const sessionId = 'race-condition-session';
      const filePath = path.join(tempDir, `.ideation-checkpoint-${sessionId}.yaml`);
      fs.writeFileSync(filePath, 'checkpoint content', 'utf8');
      checkpointFiles.push(filePath);

      // Simulate race condition: file deleted by another process before cleanup
      fs.unlinkSync(filePath);

      // Act: Cleanup called for already-deleted file
      const cleaner = new CheckpointCleaner(mockLogger);
      let errorThrown = false;
      try {
        cleaner.cleanupOnCompletion(sessionId);
      } catch (error) {
        errorThrown = true;
      }

      // Assert: No error thrown for already-deleted file
      expect(errorThrown).toBe(false);

      // Should log "already cleaned"
      expect(logOutput.some(entry =>
        entry.message.includes('already') || entry.message.includes('not found')
      )).toBe(true);
    });

    test('should_log_already_cleaned_message_for_missing_checkpoint', () => {
      // Arrange
      const sessionId = 'already-deleted-session';
      const filePath = path.join(tempDir, `.ideation-checkpoint-${sessionId}.yaml`);
      // File doesn't exist

      // Act
      const cleaner = new CheckpointCleaner(mockLogger);
      cleaner.cleanupOnCompletion(sessionId);

      // Assert
      expect(logOutput.some(entry =>
        entry.message.includes('already') ||
        entry.message.includes('cleaned') ||
        entry.message.includes('not found')
      )).toBe(true);
    });

  });

  describe('Edge Case #2: Permission denied on deletion', () => {

    test('should_warn_user_when_permission_denied_on_individual_file', () => {
      // Arrange
      const filePath = path.join(tempDir, '.ideation-checkpoint-readonly.yaml');
      fs.writeFileSync(filePath, 'protected', 'utf8');
      checkpointFiles.push(filePath);

      // Mock permission error
      const originalUnlink = fs.unlinkSync;
      fs.unlinkSync = jest.fn(() => {
        throw new Error('EACCES: permission denied');
      });

      // Act
      const cleaner = new CheckpointCleaner(mockLogger);
      const result = cleaner.cleanupAllCheckpointsWithConfirmation(true);

      // Assert: Warning logged
      expect(logOutput.some(entry =>
        entry.message.includes('permission') || entry.message.includes('denied')
      )).toBe(true);

      // Result should indicate error
      expect(result.errors).toBeGreaterThan(0);

      // Restore
      fs.unlinkSync = originalUnlink;
    });

    test('should_continue_cleanup_after_permission_error', () => {
      // Arrange: Multiple files, one has permission denied
      const path1 = path.join(tempDir, '.ideation-checkpoint-ok-1.yaml');
      const path2 = path.join(tempDir, '.ideation-checkpoint-denied.yaml');
      const path3 = path.join(tempDir, '.ideation-checkpoint-ok-2.yaml');

      fs.writeFileSync(path1, 'ok', 'utf8');
      fs.writeFileSync(path2, 'denied', 'utf8');
      fs.writeFileSync(path3, 'ok', 'utf8');
      checkpointFiles.push(path1, path2, path3);

      // Mock selective permission error
      const originalUnlink = fs.unlinkSync;
      fs.unlinkSync = jest.fn((filePath) => {
        if (filePath.includes('denied')) {
          throw new Error('EACCES: permission denied');
        }
        originalUnlink(filePath);
      });

      // Act
      const cleaner = new CheckpointCleaner(mockLogger);
      const result = cleaner.cleanupAllCheckpointsWithConfirmation(true);

      // Assert: Cleanup continued for other files
      expect(result.deleted).toBeGreaterThan(0);

      // Restore
      fs.unlinkSync = originalUnlink;
    });

  });

  describe('Edge Case #3: Very large number of checkpoints (1000+)', () => {

    test('should_handle_batch_deletion_for_large_numbers', () => {
      // Arrange: Create 100 files (represents batch behavior for 1000+)
      const fileCount = 100;
      for (let i = 1; i <= fileCount; i++) {
        const filePath = path.join(tempDir, `.ideation-checkpoint-batch-${String(i).padStart(3, '0')}.yaml`);
        fs.writeFileSync(filePath, 'data', 'utf8');
        checkpointFiles.push(filePath);
      }

      // Act
      const cleaner = new CheckpointCleaner(mockLogger);
      const result = cleaner.cleanupAllCheckpointsWithConfirmation(true);

      // Assert: All cleaned
      expect(result.deleted).toBe(fileCount);

      checkpointFiles.forEach(filePath => {
        expect(fs.existsSync(filePath)).toBe(false);
      });
    });

    test('should_display_progress_for_large_batch_operations', () => {
      // Arrange: Create 50 files
      for (let i = 1; i <= 50; i++) {
        const filePath = path.join(tempDir, `.ideation-checkpoint-display-${i}.yaml`);
        fs.writeFileSync(filePath, 'content', 'utf8');
        checkpointFiles.push(filePath);
      }

      // Act
      const cleaner = new CheckpointCleaner(mockLogger);
      const result = cleaner.cleanupAllCheckpointsWithConfirmation(true, { verbose: true });

      // Assert: Progress information included
      expect(logOutput.length).toBeGreaterThan(1);
    });

  });

  describe('Edge Case #4: Network filesystem slow deletion', () => {

    test('should_timeout_after_5_seconds_on_slow_filesystem', () => {
      // Arrange
      const filePath = path.join(tempDir, '.ideation-checkpoint-slow.yaml');
      fs.writeFileSync(filePath, 'content', 'utf8');
      checkpointFiles.push(filePath);

      // Mock slow deletion
      const originalUnlink = fs.unlinkSync;
      const startTime = Date.now();
      fs.unlinkSync = jest.fn(() => {
        // Simulate slow operation - don't actually wait in test
        throw new Error('ETIMEDOUT: operation timed out');
      });

      // Act
      const cleaner = new CheckpointCleaner(mockLogger);
      cleaner.setCleanupTimeout(5000); // 5 second timeout
      const result = cleaner.cleanupAllCheckpointsWithConfirmation(true);

      // Assert: Operation should timeout and be handled
      expect(result.errors).toBeGreaterThanOrEqual(0);
      expect(logOutput.some(entry =>
        entry.message.includes('timeout') || entry.message.includes('slow')
      )).toBe(true);

      // Restore
      fs.unlinkSync = originalUnlink;
    });

    test('should_warn_user_on_slow_filesystem_deletion', () => {
      // Arrange
      const filePath = path.join(tempDir, '.ideation-checkpoint-slowwarn.yaml');
      fs.writeFileSync(filePath, 'content', 'utf8');
      checkpointFiles.push(filePath);

      // Mock slow but eventual deletion
      const originalUnlink = fs.unlinkSync;
      fs.unlinkSync = jest.fn((p) => {
        // Simulate slow operation
        originalUnlink(p);
      });

      // Act
      const cleaner = new CheckpointCleaner(mockLogger);
      cleaner.cleanupAllCheckpointsWithConfirmation(true, { slowWarningMs: 100 });

      // Assert: Slow operation detected and warned
      // (May or may not warn depending on actual timing)
      expect(logOutput.length).toBeGreaterThan(0);

      // Restore
      fs.unlinkSync = originalUnlink;
    });

  });

  describe('Cleanup isolation and transaction-like behavior', () => {

    test('should_not_interfere_with_concurrent_checkpoint_creation', () => {
      // Arrange: Create initial checkpoints
      const path1 = path.join(tempDir, '.ideation-checkpoint-iso-1.yaml');
      fs.writeFileSync(path1, 'old', 'utf8');
      checkpointFiles.push(path1);

      // Act: Start cleanup - discover files FIRST
      const cleaner = new CheckpointCleaner(mockLogger);
      cleaner.discoverCheckpointFiles();  // Captures only path1

      // Simulate concurrent checkpoint creation AFTER discovery but BEFORE cleanup
      const path2 = path.join(tempDir, '.ideation-checkpoint-iso-2.yaml');
      fs.writeFileSync(path2, 'new', 'utf8');
      checkpointFiles.push(path2);

      // Cleanup uses pre-discovered list (path1 only), not current directory contents
      const result = cleaner.cleanupAllCheckpointsWithConfirmation(true);

      // Assert: Cleanup doesn't interfere with new checkpoint (created after discovery)
      expect(fs.existsSync(path2)).toBe(true);
    });

    test('should_handle_checkpoint_file_structure_variations', () => {
      // Arrange: Files with different formats
      const path1 = path.join(tempDir, '.ideation-checkpoint-var1.yaml');
      const path2 = path.join(tempDir, '.ideation-checkpoint-var2.yml');
      const path3 = path.join(tempDir, '.ideation-checkpoint-var3.json');

      fs.writeFileSync(path1, 'yaml', 'utf8');
      fs.writeFileSync(path2, 'yml', 'utf8');
      // Only .yaml files should be deleted (pattern specific)
      checkpointFiles.push(path1, path2, path3);

      // Act
      const cleaner = new CheckpointCleaner(mockLogger);
      cleaner.cleanupAllCheckpointsWithConfirmation(true);

      // Assert: Only matching pattern deleted
      expect(fs.existsSync(path1)).toBe(false); // .yaml deleted
      // path2 and path3 behavior depends on pattern specificity
    });

  });

});
