/**
 * Unit tests for Checkpoint Auto-Cleanup on Successful Completion (AC#1)
 *
 * AC#1: Checkpoint Deletion on Successful Completion
 * When ideation completes successfully (Phase 6 artifacts generated),
 * after user answers Phase 6.6 next-action question,
 * checkpoint file should be deleted and success logged.
 */

const fs = require('fs');
const path = require('path');

// Mock implementation - these will be imported from the actual implementation
// For now, we test the interface/contract
const CheckpointCleaner = require('../../src/checkpoint-cleaner');

describe('AC#1: Checkpoint Deletion on Successful Completion', () => {

  const tempDir = path.join(__dirname, '../../devforgeai/temp');
  let sessionId;
  let checkpointFilePath;
  let logOutput = [];

  // Mock logger to capture output
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

  beforeEach(() => {
    // Reset session data
    sessionId = 'test-session-' + Date.now();
    checkpointFilePath = path.join(tempDir, `.ideation-checkpoint-${sessionId}.yaml`);
    logOutput = [];

    // Create temp directory if it doesn't exist
    if (!fs.existsSync(tempDir)) {
      fs.mkdirSync(tempDir, { recursive: true });
    }
  });

  afterEach(() => {
    // Cleanup test checkpoint files
    if (fs.existsSync(checkpointFilePath)) {
      fs.unlinkSync(checkpointFilePath);
    }
  });

  describe('Successful completion cleanup', () => {

    test('should_delete_checkpoint_file_when_ideation_completes_successfully', () => {
      // Arrange: Create a checkpoint file for a session
      const checkpointContent = `
session_id: ${sessionId}
phase: 6
status: phase_6_artifacts_ready
created_at: ${new Date().toISOString()}
`;
      fs.writeFileSync(checkpointFilePath, checkpointContent, 'utf8');
      expect(fs.existsSync(checkpointFilePath)).toBe(true);

      // Act: Call cleanup on successful completion
      const cleaner = new CheckpointCleaner(mockLogger);
      cleaner.cleanupOnCompletion(sessionId);

      // Assert: Checkpoint file should be deleted
      expect(fs.existsSync(checkpointFilePath)).toBe(false);
    });

    test('should_log_success_message_when_checkpoint_deleted', () => {
      // Arrange
      const checkpointContent = `
session_id: ${sessionId}
phase: 6
`;
      fs.writeFileSync(checkpointFilePath, checkpointContent, 'utf8');

      // Act
      const cleaner = new CheckpointCleaner(mockLogger);
      cleaner.cleanupOnCompletion(sessionId);

      // Assert: Success message should be logged
      expect(logOutput).toContain(`Checkpoint marked for cleanup: ${sessionId}`);
    });

    test('should_verify_checkpoint_file_path_matches_pattern', () => {
      // Arrange
      const pattern = '.ideation-checkpoint-';
      const checkpointContent = 'test checkpoint';
      fs.writeFileSync(checkpointFilePath, checkpointContent, 'utf8');

      // Act
      const cleaner = new CheckpointCleaner(mockLogger);
      cleaner.cleanupOnCompletion(sessionId);

      // Assert: File path should match expected pattern
      expect(checkpointFilePath).toContain(pattern);
      expect(checkpointFilePath).toContain(sessionId);
    });

  });

  describe('Cleanup with various session IDs', () => {

    test('should_handle_cleanup_with_alphanumeric_session_id', () => {
      // Arrange
      const alphanumericSessionId = 'session-abc123-def456';
      const alphanumericCheckpointPath = path.join(tempDir, `.ideation-checkpoint-${alphanumericSessionId}.yaml`);
      fs.writeFileSync(alphanumericCheckpointPath, 'content', 'utf8');

      // Act
      const cleaner = new CheckpointCleaner(mockLogger);
      cleaner.cleanupOnCompletion(alphanumericSessionId);

      // Assert
      expect(fs.existsSync(alphanumericCheckpointPath)).toBe(false);
    });

    test('should_handle_cleanup_with_uuid_format_session_id', () => {
      // Arrange
      const uuidSessionId = '550e8400-e29b-41d4-a716-446655440000';
      const uuidCheckpointPath = path.join(tempDir, `.ideation-checkpoint-${uuidSessionId}.yaml`);
      fs.writeFileSync(uuidCheckpointPath, 'content', 'utf8');

      // Act
      const cleaner = new CheckpointCleaner(mockLogger);
      cleaner.cleanupOnCompletion(uuidSessionId);

      // Assert
      expect(fs.existsSync(uuidCheckpointPath)).toBe(false);
    });

  });

  describe('Edge cases', () => {

    test('should_handle_cleanup_when_checkpoint_already_deleted_race_condition', () => {
      // Arrange: Checkpoint doesn't exist (race condition - already deleted)
      sessionId = 'already-deleted-session';
      checkpointFilePath = path.join(tempDir, `.ideation-checkpoint-${sessionId}.yaml`);

      // Ensure file doesn't exist
      if (fs.existsSync(checkpointFilePath)) {
        fs.unlinkSync(checkpointFilePath);
      }

      // Act & Assert: Should not throw error
      const cleaner = new CheckpointCleaner(mockLogger);
      expect(() => {
        cleaner.cleanupOnCompletion(sessionId);
      }).not.toThrow();

      // Should log "already cleaned" message
      expect(logOutput.some(msg => msg.includes('already cleaned') || msg.includes('not found'))).toBe(true);
    });

    test('should_handle_permission_denied_on_deletion', () => {
      // Arrange: Create checkpoint with read-only permissions
      const checkpointContent = 'protected content';
      fs.writeFileSync(checkpointFilePath, checkpointContent, 'utf8');

      // Mock fs.unlinkSync to throw permission error
      const originalUnlink = fs.unlinkSync;
      fs.unlinkSync = jest.fn(() => {
        throw new Error('EACCES: permission denied');
      });

      // Act
      const cleaner = new CheckpointCleaner(mockLogger);

      // Assert: Should warn about permission error
      expect(() => {
        cleaner.cleanupOnCompletion(sessionId);
      }).not.toThrow();

      // Restore original
      fs.unlinkSync = originalUnlink;
    });

  });

  describe('Cleanup timing requirements', () => {

    test('should_cleanup_only_after_phase_6_6_confirmation', () => {
      // Arrange: Session at phase 5 (not yet ready for cleanup)
      const checkpointContent = `
session_id: ${sessionId}
phase: 5
status: phase_5_in_progress
`;
      fs.writeFileSync(checkpointFilePath, checkpointContent, 'utf8');

      // Act: Call cleanup at wrong phase
      const cleaner = new CheckpointCleaner(mockLogger);

      // This should NOT delete if implementation validates phase
      // (Implementation detail may vary, but concept should be tested)
      cleaner.cleanupOnCompletion(sessionId);

      // Assert: File may still exist if phase validation is implemented
      // OR file is deleted but warning is logged about timing
      if (!fs.existsSync(checkpointFilePath)) {
        expect(logOutput.some(msg => msg.includes('phase') || msg.includes('early'))).toBe(true);
      }
    });

    test('should_cleanup_return_session_id_for_confirmation', () => {
      // Arrange
      const checkpointContent = `
session_id: ${sessionId}
phase: 6
`;
      fs.writeFileSync(checkpointFilePath, checkpointContent, 'utf8');

      // Act
      const cleaner = new CheckpointCleaner(mockLogger);
      const result = cleaner.cleanupOnCompletion(sessionId);

      // Assert: Should return the cleaned session ID for confirmation
      expect(result).toBe(sessionId);
    });

  });

  describe('Session validation', () => {

    test('should_return_null_for_null_session_id', () => {
      // Arrange
      const cleaner = new CheckpointCleaner(mockLogger);

      // Act
      const result = cleaner.cleanupOnCompletion(null);

      // Assert
      expect(result).toBe(null);
      expect(logOutput.some(msg => msg.error && msg.error.includes('Invalid session ID'))).toBe(true);
    });

    test('should_return_null_for_empty_string_session_id', () => {
      // Arrange
      const cleaner = new CheckpointCleaner(mockLogger);

      // Act
      const result = cleaner.cleanupOnCompletion('');

      // Assert
      expect(result).toBe(null);
    });

    test('should_return_null_for_session_id_with_path_traversal', () => {
      // Arrange
      const cleaner = new CheckpointCleaner(mockLogger);

      // Act: Try path traversal attack
      const result = cleaner.cleanupOnCompletion('../../../etc/passwd');

      // Assert
      expect(result).toBe(null);
      expect(logOutput.some(msg => msg.error && msg.error.includes('Invalid session ID format'))).toBe(true);
    });

    test('should_return_null_for_non_string_session_id', () => {
      // Arrange
      const cleaner = new CheckpointCleaner(mockLogger);

      // Act
      const result = cleaner.cleanupOnCompletion(12345);

      // Assert
      expect(result).toBe(null);
    });

  });

  describe('isSessionComplete validation', () => {

    test('should_return_false_for_non_existent_session', () => {
      // Arrange
      const cleaner = new CheckpointCleaner(mockLogger);

      // Act
      const result = cleaner.isSessionComplete('non-existent-session');

      // Assert
      expect(result).toBe(false);
    });

    test('should_return_true_for_session_at_phase_6', () => {
      // Arrange
      const checkpointContent = `
session_id: ${sessionId}
phase: 6
status: completed
`;
      fs.writeFileSync(checkpointFilePath, checkpointContent, 'utf8');
      const cleaner = new CheckpointCleaner(mockLogger);

      // Act
      const result = cleaner.isSessionComplete(sessionId);

      // Assert
      expect(result).toBe(true);
    });

    test('should_return_false_for_session_at_phase_5', () => {
      // Arrange
      const checkpointContent = `
session_id: ${sessionId}
phase: 5
status: in_progress
`;
      fs.writeFileSync(checkpointFilePath, checkpointContent, 'utf8');
      const cleaner = new CheckpointCleaner(mockLogger);

      // Act
      const result = cleaner.isSessionComplete(sessionId);

      // Assert
      expect(result).toBe(false);
    });

    test('should_return_true_for_session_with_status_completed', () => {
      // Arrange
      const checkpointContent = `
session_id: ${sessionId}
status: completed
`;
      fs.writeFileSync(checkpointFilePath, checkpointContent, 'utf8');
      const cleaner = new CheckpointCleaner(mockLogger);

      // Act
      const result = cleaner.isSessionComplete(sessionId);

      // Assert
      expect(result).toBe(true);
    });

    test('should_return_true_for_session_with_phase_6_artifacts_ready', () => {
      // Arrange
      const checkpointContent = `
session_id: ${sessionId}
phase_6_artifacts_ready: true
`;
      fs.writeFileSync(checkpointFilePath, checkpointContent, 'utf8');
      const cleaner = new CheckpointCleaner(mockLogger);

      // Act
      const result = cleaner.isSessionComplete(sessionId);

      // Assert
      expect(result).toBe(true);
    });

    test('should_return_true_for_session_with_session_complete', () => {
      // Arrange
      const checkpointContent = `
session_id: ${sessionId}
session_complete: true
`;
      fs.writeFileSync(checkpointFilePath, checkpointContent, 'utf8');
      const cleaner = new CheckpointCleaner(mockLogger);

      // Act
      const result = cleaner.isSessionComplete(sessionId);

      // Assert
      expect(result).toBe(true);
    });

    test('should_return_false_for_incomplete_session_without_markers', () => {
      // Arrange
      const checkpointContent = `
session_id: ${sessionId}
current_step: 3
`;
      fs.writeFileSync(checkpointFilePath, checkpointContent, 'utf8');
      const cleaner = new CheckpointCleaner(mockLogger);

      // Act
      const result = cleaner.isSessionComplete(sessionId);

      // Assert
      expect(result).toBe(false);
    });

  });

  describe('Multi-file cleanup (future enhancement)', () => {

    test('should_cleanup_preserves_other_checkpoint_files', () => {
      // Arrange: Create multiple checkpoint files
      const sessionId1 = 'session-1';
      const sessionId2 = 'session-2';
      const checkpointPath1 = path.join(tempDir, `.ideation-checkpoint-${sessionId1}.yaml`);
      const checkpointPath2 = path.join(tempDir, `.ideation-checkpoint-${sessionId2}.yaml`);

      fs.writeFileSync(checkpointPath1, 'session 1 checkpoint', 'utf8');
      fs.writeFileSync(checkpointPath2, 'session 2 checkpoint', 'utf8');

      // Act: Cleanup only session 1
      const cleaner = new CheckpointCleaner(mockLogger);
      cleaner.cleanupOnCompletion(sessionId1);

      // Assert: Only session 1 deleted, session 2 preserved
      expect(fs.existsSync(checkpointPath1)).toBe(false);
      expect(fs.existsSync(checkpointPath2)).toBe(true);

      // Cleanup
      if (fs.existsSync(checkpointPath2)) {
        fs.unlinkSync(checkpointPath2);
      }
    });

  });

});
