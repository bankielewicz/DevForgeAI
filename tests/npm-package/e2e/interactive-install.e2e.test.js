/**
 * E2E Tests - Interactive Installation
 *
 * Test Coverage:
 * - AC#1: Complete interactive wizard flow with real terminal
 * - AC#2: Progress indicators during real file operations
 * - AC#3: Color-coded output in real terminal
 * - AC#7: Keyboard interrupt handling (Ctrl+C)
 * - NFR-005: Terminal compatibility
 * - NFR-007: Keyboard-only navigation
 * - NFR-008: Atomic file operations
 *
 * @jest-environment node
 */

const { spawn } = require('child_process');
const fs = require('fs').promises;
const path = require('path');

describe('E2E: Interactive Installation', () => {
  let testDir;

  beforeEach(async () => {
    // Arrange: Create test directory
    testDir = path.join(__dirname, 'e2e-test-temp');
    await fs.mkdir(testDir, { recursive: true });
  });

  afterEach(async () => {
    // Cleanup: Remove test directory
    await fs.rm(testDir, { recursive: true, force: true });
  });

  describe('AC#1: Complete interactive wizard flow', () => {
    it('should complete installation with user prompts', async () => {
      // This test requires manual interaction or automated input simulation
      // For TDD, this test will FAIL until implementation exists

      // Arrange
      const installProcess = spawn('devforgeai', ['install'], {
        cwd: testDir,
        env: { ...process.env, FORCE_TTY: 'true' },
      });

      const inputs = [
        testDir, // Target directory
        '\n', // Enter to confirm
        '\x1B[B', // Arrow down to "standard" (default, no movement needed)
        '\n', // Enter to confirm
        '\x1B[B', // Arrow down to "merge-smart" (default)
        '\n', // Enter to confirm
      ];

      // Act
      for (const input of inputs) {
        installProcess.stdin.write(input);
        await new Promise((resolve) => setTimeout(resolve, 100));
      }

      installProcess.stdin.end();

      // Assert
      await new Promise((resolve, reject) => {
        installProcess.on('exit', (code) => {
          expect(code).toBe(0);
          resolve();
        });

        installProcess.on('error', reject);

        setTimeout(() => reject(new Error('Test timeout')), 30000);
      });

      // Verify installation files created
      const claudeMdExists = await fs
        .access(path.join(testDir, 'CLAUDE.md'))
        .then(() => true)
        .catch(() => false);
      expect(claudeMdExists).toBe(true);
    }, 30000); // 30 second timeout for interactive test
  });

  describe('AC#2: Progress indicators during real operations', () => {
    it('should display spinner for file operations exceeding 200ms', async () => {
      // Arrange
      const installProcess = spawn('devforgeai', ['install', '--yes'], {
        cwd: testDir,
        env: { ...process.env, FORCE_TTY: 'true' },
      });

      let stdout = '';

      // Act
      installProcess.stdout.on('data', (data) => {
        stdout += data.toString();
      });

      await new Promise((resolve, reject) => {
        installProcess.on('exit', resolve);
        installProcess.on('error', reject);
        setTimeout(() => reject(new Error('Test timeout')), 30000);
      });

      // Assert
      // Look for spinner frames or progress indicators
      expect(stdout).toMatch(/[⠋⠙⠹⠸⠼⠴⠦⠧⠇⠏]|Installing|Copying/);
    }, 30000);

    it('should display progress bar for multiple file operations', async () => {
      // Arrange
      const installProcess = spawn(
        'devforgeai',
        ['install', '--yes', '--mode=full'],
        {
          cwd: testDir,
          env: { ...process.env, FORCE_TTY: 'true' },
        }
      );

      let stdout = '';

      // Act
      installProcess.stdout.on('data', (data) => {
        stdout += data.toString();
      });

      await new Promise((resolve, reject) => {
        installProcess.on('exit', resolve);
        installProcess.on('error', reject);
        setTimeout(() => reject(new Error('Test timeout')), 30000);
      });

      // Assert
      // Look for progress bar characters
      expect(stdout).toMatch(/[█▓▒░]|\d+%|[\d+\/\d+]/);
    }, 30000);
  });

  describe('AC#3: Color-coded output in real terminal', () => {
    it('should display ANSI color codes in terminal output', async () => {
      // Arrange
      const installProcess = spawn('devforgeai', ['install', '--yes'], {
        cwd: testDir,
        env: { ...process.env, FORCE_COLOR: '1' },
      });

      let stdout = '';

      // Act
      installProcess.stdout.on('data', (data) => {
        stdout += data.toString();
      });

      await new Promise((resolve, reject) => {
        installProcess.on('exit', resolve);
        installProcess.on('error', reject);
        setTimeout(() => reject(new Error('Test timeout')), 30000);
      });

      // Assert
      // Look for ANSI escape codes for colors
      expect(stdout).toMatch(/\x1b\[3[0-7]m/); // ANSI color codes
    }, 30000);

    it('should disable colors when NO_COLOR is set', async () => {
      // Arrange
      const installProcess = spawn('devforgeai', ['install', '--yes'], {
        cwd: testDir,
        env: { ...process.env, NO_COLOR: '1' },
      });

      let stdout = '';

      // Act
      installProcess.stdout.on('data', (data) => {
        stdout += data.toString();
      });

      await new Promise((resolve, reject) => {
        installProcess.on('exit', resolve);
        installProcess.on('error', reject);
        setTimeout(() => reject(new Error('Test timeout')), 30000);
      });

      // Assert
      // Should NOT contain ANSI color codes
      expect(stdout).not.toMatch(/\x1b\[3[0-7]m/);
      // Should still contain status symbols
      expect(stdout).toMatch(/\[OK\]|\[ERROR\]|\[WARN\]/);
    }, 30000);
  });

  describe('AC#7: Keyboard interrupt handling (Ctrl+C)', () => {
    it('should handle SIGINT gracefully during installation', async () => {
      // Arrange
      const installProcess = spawn('devforgeai', ['install', '--yes'], {
        cwd: testDir,
        env: { ...process.env, FORCE_TTY: 'true' },
      });

      let stderr = '';

      // Act
      installProcess.stderr.on('data', (data) => {
        stderr += data.toString();
      });

      // Wait 500ms then send SIGINT
      await new Promise((resolve) => setTimeout(resolve, 500));
      installProcess.kill('SIGINT');

      const exitCode = await new Promise((resolve) => {
        installProcess.on('exit', (code) => resolve(code));
      });

      // Assert
      expect(exitCode).toBe(130); // Standard SIGINT exit code
      expect(stderr).toMatch(/Installation cancelled by user/);
    }, 30000);

    it('should clean up partial files after SIGINT', async () => {
      // Arrange
      const installProcess = spawn('devforgeai', ['install', '--yes'], {
        cwd: testDir,
        env: { ...process.env, FORCE_TTY: 'true' },
      });

      // Act
      // Wait for file copying to start
      await new Promise((resolve) => setTimeout(resolve, 300));
      installProcess.kill('SIGINT');

      await new Promise((resolve) => {
        installProcess.on('exit', resolve);
      });

      // Assert
      // Check for partial files (should not exist)
      const files = await fs.readdir(testDir);
      const partialFiles = files.filter((file) => file.endsWith('.partial'));
      expect(partialFiles).toEqual([]);
    }, 30000);

    it('should display cancellation message before exit', async () => {
      // Arrange
      const installProcess = spawn('devforgeai', ['install', '--yes'], {
        cwd: testDir,
        env: { ...process.env, FORCE_TTY: 'true' },
      });

      let stderr = '';
      const messages = [];

      // Act
      installProcess.stderr.on('data', (data) => {
        stderr += data.toString();
        messages.push({ timestamp: Date.now(), message: data.toString() });
      });

      await new Promise((resolve) => setTimeout(resolve, 500));
      installProcess.kill('SIGINT');

      await new Promise((resolve) => {
        installProcess.on('exit', resolve);
      });

      // Assert
      expect(stderr).toMatch(/✗.*Installation cancelled by user/);
      // Verify message appears before exit
      const cancelMsg = messages.find((m) =>
        m.message.includes('cancelled by user')
      );
      expect(cancelMsg).toBeDefined();
    }, 30000);
  });

  describe('NFR-005: Terminal compatibility', () => {
    const terminals = [
      { name: 'iTerm2', env: { TERM_PROGRAM: 'iTerm.app' } },
      { name: 'GNOME Terminal', env: { TERM: 'xterm-256color' } },
      { name: 'Windows Terminal', env: { WT_SESSION: 'test' } },
    ];

    terminals.forEach(({ name, env }) => {
      it(`should work on ${name}`, async () => {
        // Arrange
        const installProcess = spawn('devforgeai', ['install', '--yes'], {
          cwd: testDir,
          env: { ...process.env, ...env },
        });

        // Act
        const exitCode = await new Promise((resolve, reject) => {
          installProcess.on('exit', resolve);
          installProcess.on('error', reject);
          setTimeout(() => reject(new Error('Test timeout')), 30000);
        });

        // Assert
        expect(exitCode).toBe(0);
      }, 30000);
    });
  });

  describe('NFR-007: Keyboard-only navigation', () => {
    it('should complete installation using only keyboard', async () => {
      // This test validates keyboard navigation is possible
      // Actual keyboard input testing requires automation tools

      // Arrange
      const installProcess = spawn('devforgeai', ['install'], {
        cwd: testDir,
        env: { ...process.env, FORCE_TTY: 'true' },
      });

      const keyboardInputs = [
        '\n', // Enter on target directory (use default)
        '\x1B[A', // Arrow up (navigate to minimal)
        '\x1B[B', // Arrow down (back to standard)
        '\n', // Enter to confirm
        '\n', // Enter on merge strategy (use default)
      ];

      // Act
      for (const input of keyboardInputs) {
        installProcess.stdin.write(input);
        await new Promise((resolve) => setTimeout(resolve, 100));
      }

      installProcess.stdin.end();

      const exitCode = await new Promise((resolve, reject) => {
        installProcess.on('exit', resolve);
        installProcess.on('error', reject);
        setTimeout(() => reject(new Error('Test timeout')), 30000);
      });

      // Assert
      expect(exitCode).toBe(0);
    }, 30000);
  });

  describe('NFR-008: Atomic file operations', () => {
    it('should use temp file + rename pattern for writes', async () => {
      // Arrange
      const installProcess = spawn('devforgeai', ['install', '--yes'], {
        cwd: testDir,
        env: { ...process.env, FORCE_TTY: 'true' },
      });

      // Act
      await new Promise((resolve, reject) => {
        installProcess.on('exit', resolve);
        installProcess.on('error', reject);
        setTimeout(() => reject(new Error('Test timeout')), 30000);
      });

      // Assert
      // Verify no .tmp files left behind
      const files = await fs.readdir(testDir);
      const tmpFiles = files.filter((file) => file.endsWith('.tmp'));
      expect(tmpFiles).toEqual([]);

      // Verify final files exist
      const claudeMdExists = await fs
        .access(path.join(testDir, 'CLAUDE.md'))
        .then(() => true)
        .catch(() => false);
      expect(claudeMdExists).toBe(true);
    }, 30000);

    it('should have zero partial files after interruption', async () => {
      // Arrange
      const installProcess = spawn('devforgeai', ['install', '--yes'], {
        cwd: testDir,
        env: { ...process.env, FORCE_TTY: 'true' },
      });

      // Act
      await new Promise((resolve) => setTimeout(resolve, 300));
      installProcess.kill('SIGINT');

      await new Promise((resolve) => {
        installProcess.on('exit', resolve);
      });

      // Assert
      const files = await fs.readdir(testDir);
      const partialFiles = files.filter(
        (file) => file.endsWith('.partial') || file.endsWith('.tmp')
      );
      expect(partialFiles).toEqual([]);
    }, 30000);
  });

  describe('CI/CD Mode: --yes --quiet', () => {
    it('should complete installation in CI mode without interaction', async () => {
      // Arrange
      const installProcess = spawn(
        'devforgeai',
        ['install', '--yes', '--quiet'],
        {
          cwd: testDir,
          env: { ...process.env, CI: 'true' },
        }
      );

      let stdout = '';
      let stderr = '';

      // Act
      installProcess.stdout.on('data', (data) => {
        stdout += data.toString();
      });

      installProcess.stderr.on('data', (data) => {
        stderr += data.toString();
      });

      const exitCode = await new Promise((resolve, reject) => {
        installProcess.on('exit', resolve);
        installProcess.on('error', reject);
        setTimeout(() => reject(new Error('Test timeout')), 30000);
      });

      // Assert
      expect(exitCode).toBe(0);
      expect(stdout).toBe(''); // No stdout in quiet mode
      expect(stderr).toBe(''); // No errors
    }, 30000);

    it('should detect CI environment and auto-enable flags', async () => {
      // Arrange
      const installProcess = spawn('devforgeai', ['install'], {
        cwd: testDir,
        env: { ...process.env, CI: 'true' },
      });

      let stdout = '';

      // Act
      installProcess.stdout.on('data', (data) => {
        stdout += data.toString();
      });

      const exitCode = await new Promise((resolve, reject) => {
        installProcess.on('exit', resolve);
        installProcess.on('error', reject);
        setTimeout(() => reject(new Error('Test timeout')), 30000);
      });

      // Assert
      expect(exitCode).toBe(0);
      expect(stdout).toMatch(/CI mode detected/i);
    }, 30000);
  });
});
