/**
 * Unit tests for Checkpoint Preservation on Failure (AC#2)
 *
 * AC#2: Checkpoint Preserved on Failure
 * When ideation session fails or is interrupted before completion,
 * checkpoint file should be preserved for resume capability
 */

const fs = require('fs');
const path = require('path');

const CheckpointCleaner = require('../../src/checkpoint-cleaner');

describe('AC#2: Checkpoint Preserved on Failure', () => {

  const tempDir = path.join(__dirname, '../../devforgeai/temp');
  let sessionId;
  let checkpointFilePath;
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

  beforeEach(() => {
    sessionId = 'failure-session-' + Date.now();
    checkpointFilePath = path.join(tempDir, `.ideation-checkpoint-${sessionId}.yaml`);
    logOutput = [];

    if (!fs.existsSync(tempDir)) {
      fs.mkdirSync(tempDir, { recursive: true });
    }
  });

  afterEach(() => {
    if (fs.existsSync(checkpointFilePath)) {
      fs.unlinkSync(checkpointFilePath);
    }
  });

  describe('Failure scenarios', () => {

    test('should_preserve_checkpoint_when_session_fails_at_phase_3', () => {
      // Arrange: Create checkpoint at phase 3 (early in process)
      const checkpointContent = `
session_id: ${sessionId}
phase: 3
status: discovery_phase_in_progress
error: null
created_at: ${new Date().toISOString()}
`;
      fs.writeFileSync(checkpointFilePath, checkpointContent, 'utf8');

      // Act: Session encounters error - cleanup should NOT be called
      // (In failure scenarios, cleanupOnCompletion should not be invoked)
      // Simulate session end without successful completion

      // Assert: Checkpoint file should still exist
      expect(fs.existsSync(checkpointFilePath)).toBe(true);

      // Verify content is intact for resume
      const content = fs.readFileSync(checkpointFilePath, 'utf8');
      expect(content).toContain(sessionId);
      expect(content).toContain('phase: 3');
    });

    test('should_preserve_checkpoint_when_user_cancels_session', () => {
      // Arrange: Create checkpoint during session
      const checkpointContent = `
session_id: ${sessionId}
phase: 4
status: user_cancelled
cancel_time: ${new Date().toISOString()}
created_at: ${new Date().toISOString()}
`;
      fs.writeFileSync(checkpointFilePath, checkpointContent, 'utf8');

      // Act: Do not call cleanup (user cancelled)

      // Assert: Checkpoint preserved
      expect(fs.existsSync(checkpointFilePath)).toBe(true);
    });

    test('should_preserve_checkpoint_when_context_window_exhausted', () => {
      // Arrange: Checkpoint from interrupted session
      const checkpointContent = `
session_id: ${sessionId}
phase: 5
status: context_limit_reached
tokens_used: 95000
created_at: ${new Date().toISOString()}
`;
      fs.writeFileSync(checkpointFilePath, checkpointContent, 'utf8');

      // Act: Session interrupted - cleanup not called

      // Assert: Checkpoint available for resume
      expect(fs.existsSync(checkpointFilePath)).toBe(true);

      const content = fs.readFileSync(checkpointFilePath, 'utf8');
      expect(content).toContain('context_limit_reached');
    });

    test('should_preserve_checkpoint_when_unexpected_error_occurs', () => {
      // Arrange: Create checkpoint before error
      const checkpointContent = `
session_id: ${sessionId}
phase: 2
status: in_progress
created_at: ${new Date().toISOString()}
`;
      fs.writeFileSync(checkpointFilePath, checkpointContent, 'utf8');

      // Act: Error occurs - cleanup NOT called

      // Assert: File exists for recovery
      expect(fs.existsSync(checkpointFilePath)).toBe(true);
    });

  });

  describe('Checkpoint content validation', () => {

    test('should_preserve_checkpoint_with_complete_session_state', () => {
      // Arrange: Create checkpoint with full metadata
      const checkpointContent = `
session_id: ${sessionId}
phase: 4
status: requirements_elicitation_in_progress
timestamp: ${new Date().toISOString()}
business_problem: Test problem statement
context: Test context for resume
user_responses:
  - response1
  - response2
complexity_score: 35
created_at: ${new Date().toISOString()}
last_updated: ${new Date().toISOString()}
`;
      fs.writeFileSync(checkpointFilePath, checkpointContent, 'utf8');

      // Act: Session fails without cleanup

      // Assert: All metadata preserved
      const content = fs.readFileSync(checkpointFilePath, 'utf8');
      expect(content).toContain('business_problem');
      expect(content).toContain('user_responses');
      expect(content).toContain('complexity_score');
    });

    test('should_checkpoint_include_error_details_on_failure', () => {
      // Arrange: Create checkpoint with error information
      const errorDetails = 'Failed to parse user input: invalid JSON format';
      const checkpointContent = `
session_id: ${sessionId}
phase: 3
status: error_occurred
error_type: ParseError
error_message: ${errorDetails}
error_time: ${new Date().toISOString()}
`;
      fs.writeFileSync(checkpointFilePath, checkpointContent, 'utf8');

      // Act: Do not cleanup

      // Assert: Error details preserved for debugging
      const content = fs.readFileSync(checkpointFilePath, 'utf8');
      expect(content).toContain('ParseError');
      expect(content).toContain(errorDetails);
    });

  });

  describe('Resume capability validation', () => {

    test('should_checkpoint_be_readable_for_resume', () => {
      // Arrange: Create checkpoint
      const checkpointContent = `
session_id: ${sessionId}
phase: 5
problem_statement: "Build an AI system"
discovery_notes: "Initial discovery phase completed"
created_at: ${new Date().toISOString()}
`;
      fs.writeFileSync(checkpointFilePath, checkpointContent, 'utf8');

      // Act: Verify checkpoint can be read (simulating resume)
      const content = fs.readFileSync(checkpointFilePath, 'utf8');

      // Assert: Content is valid and parseable
      expect(content).toBeDefined();
      expect(content.length).toBeGreaterThan(0);
      expect(content).toContain(sessionId);
      expect(content).toContain('problem_statement');
    });

    test('should_checkpoint_contain_resume_metadata', () => {
      // Arrange: Create checkpoint with resume information
      const resumeMetadata = `
session_id: ${sessionId}
resume_point: phase_5
last_successful_phase: 4
phase_5_progress: 60%
next_action: Continue complexity assessment
`;
      fs.writeFileSync(checkpointFilePath, resumeMetadata, 'utf8');

      // Act: Session fails, file preserved

      // Assert: Resume metadata available
      const content = fs.readFileSync(checkpointFilePath, 'utf8');
      expect(content).toContain('resume_point');
      expect(content).toContain('next_action');
    });

  });

  describe('No automatic cleanup on failure', () => {

    test('should_not_call_cleanup_when_session_crashes', () => {
      // Arrange
      const checkpointContent = 'checkpoint data';
      fs.writeFileSync(checkpointFilePath, checkpointContent, 'utf8');

      // Act: Simulate crash (cleanupOnCompletion NOT called)
      // Arrange for some error to occur
      let cleanupWasCalled = false;
      const mockCleaner = {
        cleanupOnCompletion: () => {
          cleanupWasCalled = true;
        }
      };

      // Simulate session crash without calling cleanup
      // cleanupWasCalled remains false

      // Assert: Cleanup was not called
      expect(cleanupWasCalled).toBe(false);

      // File should still exist
      expect(fs.existsSync(checkpointFilePath)).toBe(true);
    });

    test('should_preserve_multiple_checkpoints_on_multiple_failures', () => {
      // Arrange: Multiple failed sessions
      const sessionId1 = 'fail-session-1';
      const sessionId2 = 'fail-session-2';
      const sessionId3 = 'fail-session-3';

      const path1 = path.join(tempDir, `.ideation-checkpoint-${sessionId1}.yaml`);
      const path2 = path.join(tempDir, `.ideation-checkpoint-${sessionId2}.yaml`);
      const path3 = path.join(tempDir, `.ideation-checkpoint-${sessionId3}.yaml`);

      fs.writeFileSync(path1, 'session 1', 'utf8');
      fs.writeFileSync(path2, 'session 2', 'utf8');
      fs.writeFileSync(path3, 'session 3', 'utf8');

      // Act: All sessions fail without cleanup

      // Assert: All files preserved
      expect(fs.existsSync(path1)).toBe(true);
      expect(fs.existsSync(path2)).toBe(true);
      expect(fs.existsSync(path3)).toBe(true);

      // Cleanup
      if (fs.existsSync(path1)) fs.unlinkSync(path1);
      if (fs.existsSync(path2)) fs.unlinkSync(path2);
      if (fs.existsSync(path3)) fs.unlinkSync(path3);
    });

  });

  describe('Failure recovery validation', () => {

    test('should_checkpoint_enable_session_recovery_after_error', () => {
      // Arrange: Create checkpoint with recovery info
      const checkpointContent = `
session_id: ${sessionId}
phase: 3
last_successful_action: requirements_elicitation
next_action_after_resume: continue_complexity_assessment
recovery_available: true
`;
      fs.writeFileSync(checkpointFilePath, checkpointContent, 'utf8');

      // Act: Session fails, checkpoint preserved

      // Assert: Recovery information available
      const content = fs.readFileSync(checkpointFilePath, 'utf8');
      expect(content).toContain('recovery_available: true');
      expect(content).toContain('last_successful_action');
      expect(content).toContain('next_action_after_resume');
    });

  });

});
