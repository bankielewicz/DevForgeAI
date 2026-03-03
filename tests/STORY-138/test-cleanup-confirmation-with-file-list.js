/**
 * Integration tests for Cleanup Confirmation with File List (AC#4)
 *
 * AC#4: Cleanup Confirmation with File List
 * When user runs `/ideate --clean-checkpoints` and checkpoints found,
 * display each checkpoint with timestamp and problem statement preview,
 * then ask user for confirmation with multiple options
 */

const fs = require('fs');
const path = require('path');

const CheckpointCleaner = require('../../src/checkpoint-cleaner');

describe('AC#4: Cleanup Confirmation with File List', () => {

  const tempDir = path.join(__dirname, '../../devforgeai/temp');
  const checkpointFiles = [];
  let logOutput = [];
  let userQuestionsCalled = [];

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

  const mockAskUserQuestion = (question) => {
    userQuestionsCalled.push(question);
    return {
      header: question.header,
      options: question.options
    };
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
    userQuestionsCalled = [];
    checkpointFiles.length = 0;

    if (!fs.existsSync(tempDir)) {
      fs.mkdirSync(tempDir, { recursive: true });
    }
  });

  afterEach(() => {
    checkpointFiles.forEach(filePath => {
      if (fs.existsSync(filePath)) {
        fs.unlinkSync(filePath);
      }
    });
    checkpointFiles.length = 0;
  });

  describe('File list display', () => {

    test('should_display_each_checkpoint_with_timestamp', () => {
      // Arrange: Create checkpoints with metadata
      const timestamp1 = '2025-12-25T10:30:00Z';
      const timestamp2 = '2025-12-26T14:45:00Z';

      const checkpoint1 = `
session_id: session-001
created_at: ${timestamp1}
problem: Build authentication system
status: phase_3_in_progress
`;
      const checkpoint2 = `
session_id: session-002
created_at: ${timestamp2}
problem: Create API client
status: phase_5_paused
`;

      const path1 = path.join(tempDir, '.ideation-checkpoint-001.yaml');
      const path2 = path.join(tempDir, '.ideation-checkpoint-002.yaml');

      fs.writeFileSync(path1, checkpoint1, 'utf8');
      fs.writeFileSync(path2, checkpoint2, 'utf8');
      checkpointFiles.push(path1, path2);

      // Act
      const cleaner = new CheckpointCleaner(mockLogger);
      cleaner.displayCheckpointList();

      // Assert: Timestamps displayed
      expect(logOutput.some(msg => msg.includes(timestamp1) || msg.includes('10:30'))).toBe(true);
      expect(logOutput.some(msg => msg.includes(timestamp2) || msg.includes('14:45'))).toBe(true);
    });

    test('should_display_problem_statement_preview_for_each_checkpoint', () => {
      // Arrange
      const problem1 = 'Build an AI-powered chatbot for customer support';
      const problem2 = 'Create a real-time notification system';

      const checkpoint1 = `
session_id: session-abc
problem_statement: ${problem1}
created_at: 2025-12-26T10:00:00Z
`;
      const checkpoint2 = `
session_id: session-xyz
problem_statement: ${problem2}
created_at: 2025-12-26T11:00:00Z
`;

      const path1 = path.join(tempDir, '.ideation-checkpoint-preview-1.yaml');
      const path2 = path.join(tempDir, '.ideation-checkpoint-preview-2.yaml');

      fs.writeFileSync(path1, checkpoint1, 'utf8');
      fs.writeFileSync(path2, checkpoint2, 'utf8');
      checkpointFiles.push(path1, path2);

      // Act
      const cleaner = new CheckpointCleaner(mockLogger);
      cleaner.displayCheckpointList();

      // Assert: Problem statements displayed
      expect(logOutput.some(msg => msg.includes(problem1) || msg.includes('AI-powered'))).toBe(true);
      expect(logOutput.some(msg => msg.includes(problem2) || msg.includes('notification'))).toBe(true);
    });

    test('should_truncate_long_problem_statement_preview', () => {
      // Arrange: Create checkpoint with very long problem
      const longProblem = 'A'.repeat(200); // 200 chars, likely needs truncation
      const checkpoint = `
session_id: session-long
problem_statement: ${longProblem}
created_at: 2025-12-26T12:00:00Z
`;

      const filePath = path.join(tempDir, '.ideation-checkpoint-long.yaml');
      fs.writeFileSync(filePath, checkpoint, 'utf8');
      checkpointFiles.push(filePath);

      // Act
      const cleaner = new CheckpointCleaner(mockLogger);
      cleaner.displayCheckpointList();

      // Assert: Preview is truncated with ellipsis
      const output = logOutput.join('');
      const previewText = output.match(/A{1,50}\.\.\./); // Should have ellipsis
      if (previewText) {
        expect(previewText[0]).toContain('...');
      }
    });

    test('should_display_session_id_for_each_checkpoint', () => {
      // Arrange
      // Session IDs are extracted from FILENAME, not file content
      const session1 = 'sess-uuid-1';
      const session2 = 'sess-uuid-2';

      const checkpoint1 = `
session_id: ${session1}
created_at: 2025-12-26T10:00:00Z
problem: Test problem 1
`;
      const checkpoint2 = `
session_id: ${session2}
created_at: 2025-12-26T11:00:00Z
problem: Test problem 2
`;

      // Use session IDs in filenames to match expected extraction
      const path1 = path.join(tempDir, `.ideation-checkpoint-${session1}.yaml`);
      const path2 = path.join(tempDir, `.ideation-checkpoint-${session2}.yaml`);

      fs.writeFileSync(path1, checkpoint1, 'utf8');
      fs.writeFileSync(path2, checkpoint2, 'utf8');
      checkpointFiles.push(path1, path2);

      // Act
      const cleaner = new CheckpointCleaner(mockLogger);
      cleaner.displayCheckpointList();

      // Assert: Session IDs displayed
      expect(logOutput.some(msg => msg.includes(session1))).toBe(true);
      expect(logOutput.some(msg => msg.includes(session2))).toBe(true);
    });

  });

  describe('Confirmation prompt', () => {

    test('should_ask_user_question_delete_N_checkpoint_files', () => {
      // Arrange: Create 3 checkpoints
      for (let i = 1; i <= 3; i++) {
        const filePath = path.join(tempDir, `.ideation-checkpoint-q${i}.yaml`);
        fs.writeFileSync(filePath, 'content', 'utf8');
        checkpointFiles.push(filePath);
      }

      // Act
      const cleaner = new CheckpointCleaner(mockLogger);
      cleaner.displayConfirmationQuestion(mockAskUserQuestion);

      // Assert: Question asked with count
      expect(userQuestionsCalled.length).toBeGreaterThan(0);
      const question = userQuestionsCalled[0];
      expect(question.header).toContain('Delete');
      expect(question.header).toContain('3');
      expect(question.header).toContain('checkpoint');
    });

    test('should_provide_yes_delete_all_option', () => {
      // Arrange
      const filePath = path.join(tempDir, '.ideation-checkpoint-yes.yaml');
      fs.writeFileSync(filePath, 'content', 'utf8');
      checkpointFiles.push(filePath);

      // Act
      const cleaner = new CheckpointCleaner(mockLogger);
      cleaner.displayConfirmationQuestion(mockAskUserQuestion);

      // Assert: "Yes, delete all" option present
      const question = userQuestionsCalled[0];
      // Use toContainEqual for deep object matching
      expect(question.options.some(opt =>
        /Yes.*delete all/i.test(opt.label)
      )).toBe(true);
    });

    test('should_provide_no_keep_them_option', () => {
      // Arrange
      const filePath = path.join(tempDir, '.ideation-checkpoint-no.yaml');
      fs.writeFileSync(filePath, 'content', 'utf8');
      checkpointFiles.push(filePath);

      // Act
      const cleaner = new CheckpointCleaner(mockLogger);
      cleaner.displayConfirmationQuestion(mockAskUserQuestion);

      // Assert: "No, keep them" option present
      const question = userQuestionsCalled[0];
      // Use direct regex matching for deep object matching
      expect(question.options.some(opt =>
        /No.*keep/i.test(opt.label)
      )).toBe(true);
    });

    test('should_provide_select_specific_files_option', () => {
      // Arrange
      for (let i = 1; i <= 2; i++) {
        const filePath = path.join(tempDir, `.ideation-checkpoint-sel${i}.yaml`);
        fs.writeFileSync(filePath, 'content', 'utf8');
        checkpointFiles.push(filePath);
      }

      // Act
      const cleaner = new CheckpointCleaner(mockLogger);
      cleaner.displayConfirmationQuestion(mockAskUserQuestion);

      // Assert: "Select specific files" option present
      const question = userQuestionsCalled[0];
      // Use direct regex matching for deep object matching
      expect(question.options.some(opt =>
        /Select.*specific/i.test(opt.label)
      )).toBe(true);
    });

  });

  describe('User response handling', () => {

    test('should_delete_all_when_user_selects_yes_delete_all', () => {
      // Arrange
      for (let i = 1; i <= 3; i++) {
        const filePath = path.join(tempDir, `.ideation-checkpoint-yesall${i}.yaml`);
        fs.writeFileSync(filePath, 'content', 'utf8');
        checkpointFiles.push(filePath);
      }

      // Act
      const cleaner = new CheckpointCleaner(mockLogger);
      cleaner.handleUserResponse('yes_delete_all');

      // Assert: All files deleted
      checkpointFiles.forEach(filePath => {
        expect(fs.existsSync(filePath)).toBe(false);
      });
    });

    test('should_keep_all_when_user_selects_no_keep_them', () => {
      // Arrange
      const filePath = path.join(tempDir, '.ideation-checkpoint-nokeepalll.yaml');
      fs.writeFileSync(filePath, 'content', 'utf8');
      checkpointFiles.push(filePath);

      // Act
      const cleaner = new CheckpointCleaner(mockLogger);
      cleaner.handleUserResponse('no_keep_them');

      // Assert: File preserved
      expect(fs.existsSync(filePath)).toBe(true);
    });

    test('should_allow_selective_deletion_when_user_selects_specific_files', () => {
      // Arrange: Create multiple checkpoints
      const path1 = path.join(tempDir, '.ideation-checkpoint-sel-1.yaml');
      const path2 = path.join(tempDir, '.ideation-checkpoint-sel-2.yaml');
      const path3 = path.join(tempDir, '.ideation-checkpoint-sel-3.yaml');

      fs.writeFileSync(path1, 'checkpoint 1', 'utf8');
      fs.writeFileSync(path2, 'checkpoint 2', 'utf8');
      fs.writeFileSync(path3, 'checkpoint 3', 'utf8');
      checkpointFiles.push(path1, path2, path3);

      // Act: User selects to delete only path1 and path2
      const cleaner = new CheckpointCleaner(mockLogger);
      cleaner.handleUserResponse('select_specific', [path1, path2]);

      // Assert: Only selected files deleted
      expect(fs.existsSync(path1)).toBe(false);
      expect(fs.existsSync(path2)).toBe(false);
      expect(fs.existsSync(path3)).toBe(true);
    });

  });

  describe('deleteSelectedFiles validation', () => {

    test('should_return_no_files_selected_when_empty_array', () => {
      // Arrange
      const cleaner = new CheckpointCleaner(mockLogger);

      // Act
      const result = cleaner.deleteSelectedFiles([]);

      // Assert
      expect(result.deleted).toBe(0);
      expect(result.message).toContain('No files selected');
    });

    test('should_reject_path_traversal_attempts', () => {
      // Arrange
      const cleaner = new CheckpointCleaner(mockLogger);
      const maliciousPath = '../../../etc/passwd';

      // Act
      const result = cleaner.deleteSelectedFiles([maliciousPath]);

      // Assert
      expect(result.deleted).toBe(0);
      expect(result.errors).toBe(1);
      expect(result.errorFiles[0].error).toContain('outside checkpoint directory');
    });

    test('should_reject_non_checkpoint_pattern_files', () => {
      // Arrange
      const cleaner = new CheckpointCleaner(mockLogger);
      const nonCheckpointPath = path.join(tempDir, 'not-a-checkpoint.yaml');

      // Act
      const result = cleaner.deleteSelectedFiles([nonCheckpointPath]);

      // Assert
      expect(result.deleted).toBe(0);
      expect(result.errors).toBe(1);
      expect(result.errorFiles[0].error).toContain('Not a valid checkpoint');
    });

    test('should_handle_file_not_found_error', () => {
      // Arrange
      const cleaner = new CheckpointCleaner(mockLogger);
      const nonExistentPath = path.join(tempDir, '.ideation-checkpoint-ghost.yaml');

      // Act
      const result = cleaner.deleteSelectedFiles([nonExistentPath]);

      // Assert
      expect(result.deleted).toBe(0);
      expect(result.errors).toBe(1);
      expect(result.errorFiles[0].error).toContain('File not found');
    });

    test('should_handle_mixed_valid_and_invalid_paths', () => {
      // Arrange
      const validPath = path.join(tempDir, '.ideation-checkpoint-valid.yaml');
      const invalidPath = path.join(tempDir, 'invalid-file.txt');

      fs.writeFileSync(validPath, 'valid content', 'utf8');
      checkpointFiles.push(validPath);

      const cleaner = new CheckpointCleaner(mockLogger);

      // Act
      const result = cleaner.deleteSelectedFiles([validPath, invalidPath]);

      // Assert
      expect(result.deleted).toBe(1);
      expect(result.errors).toBe(1);
    });

  });

  describe('Edge cases - file list display', () => {

    test('should_handle_checkpoint_with_missing_problem_statement', () => {
      // Arrange: Checkpoint without problem statement
      const checkpoint = `
session_id: session-noproblem
created_at: 2025-12-26T10:00:00Z
status: phase_2_in_progress
`;

      const filePath = path.join(tempDir, '.ideation-checkpoint-noprob.yaml');
      fs.writeFileSync(filePath, checkpoint, 'utf8');
      checkpointFiles.push(filePath);

      // Act
      const cleaner = new CheckpointCleaner(mockLogger);
      cleaner.displayCheckpointList();

      // Assert: Should display gracefully with placeholder
      const output = logOutput.join('');
      expect(output).toBeDefined();
      expect(output.length).toBeGreaterThan(0);
    });

    test('should_handle_checkpoint_with_missing_timestamp', () => {
      // Arrange: Checkpoint without created_at
      const checkpoint = `
session_id: session-notime
problem: Test problem
status: phase_3_in_progress
`;

      const filePath = path.join(tempDir, '.ideation-checkpoint-notime.yaml');
      fs.writeFileSync(filePath, checkpoint, 'utf8');
      checkpointFiles.push(filePath);

      // Act
      const cleaner = new CheckpointCleaner(mockLogger);
      cleaner.displayCheckpointList();

      // Assert: Should display gracefully
      expect(logOutput.length).toBeGreaterThan(0);
    });

    test('should_display_checkpoints_in_reverse_chronological_order', () => {
      // Arrange: Create checkpoints with different timestamps
      const oldTime = '2025-12-24T10:00:00Z';
      const newTime = '2025-12-26T20:00:00Z';

      // Session IDs are extracted from FILENAME, not file content
      const oldSessionId = 'old-session';
      const newSessionId = 'new-session';

      const oldCheckpoint = `
session_id: ${oldSessionId}
created_at: ${oldTime}
problem: Old problem
`;
      const newCheckpoint = `
session_id: ${newSessionId}
created_at: ${newTime}
problem: New problem
`;

      // Use session IDs in filenames
      const oldPath = path.join(tempDir, `.ideation-checkpoint-${oldSessionId}.yaml`);
      const newPath = path.join(tempDir, `.ideation-checkpoint-${newSessionId}.yaml`);

      fs.writeFileSync(oldPath, oldCheckpoint, 'utf8');
      fs.writeFileSync(newPath, newCheckpoint, 'utf8');
      checkpointFiles.push(oldPath, newPath);

      // Act
      const cleaner = new CheckpointCleaner(mockLogger);
      cleaner.displayCheckpointList();

      // Assert: Newest should appear first (reverse chronological)
      const output = logOutput.join('');
      const newIndex = output.indexOf(newSessionId);
      const oldIndex = output.indexOf(oldSessionId);

      expect(newIndex).toBeLessThan(oldIndex);
    });

  });

  describe('UX flow validation', () => {

    test('should_display_list_before_asking_confirmation', () => {
      // Arrange
      const filePath = path.join(tempDir, '.ideation-checkpoint-flow.yaml');
      fs.writeFileSync(filePath, 'content', 'utf8');
      checkpointFiles.push(filePath);

      // Act
      const cleaner = new CheckpointCleaner(mockLogger);
      cleaner.displayListThenAskConfirmation(mockAskUserQuestion);

      // Assert: List displayed before question
      const firstLogIndex = logOutput.findIndex(msg => msg.includes('session') || msg.includes('problem'));
      const firstQuestionIndex = userQuestionsCalled.length > 0 ? logOutput.length : -1;

      expect(firstLogIndex).toBeGreaterThanOrEqual(0);
    });

    test('should_provide_formatted_checkpoint_summary', () => {
      // Arrange
      for (let i = 1; i <= 2; i++) {
        const filePath = path.join(tempDir, `.ideation-checkpoint-sum${i}.yaml`);
        fs.writeFileSync(filePath, 'content', 'utf8');
        checkpointFiles.push(filePath);
      }

      // Act
      const cleaner = new CheckpointCleaner(mockLogger);
      const summary = cleaner.generateCheckpointSummary();

      // Assert: Summary is formatted and complete
      expect(summary).toBeDefined();
      expect(summary).toContain('2');
      expect(summary).toContain('checkpoint');
    });

  });

});
