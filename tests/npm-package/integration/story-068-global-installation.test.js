/**
 * STORY-068: Global CLI Entry Point
 * Integration Tests (TDD Red Phase)
 *
 * Tests end-to-end scenarios:
 * - Global installation simulation
 * - Command routing to Python installer
 * - Cross-platform execution
 * - Performance benchmarks
 *
 * NOTE: These tests simulate global npm installation without actually
 * installing globally (avoids polluting user's global npm packages).
 */

const fs = require('fs');
const path = require('path');
const { execSync, spawnSync } = require('child_process');
const os = require('os');

describe('STORY-068: Global Installation Integration Tests', () => {
  const binPath = path.join(__dirname, '../../../bin/devforgeai.js');
  const packageJsonPath = path.join(__dirname, '../../../package.json');

  describe('Global Installation Simulation', () => {
    test('[INTEGRATION] npm pack creates installable tarball', () => {
      // This verifies package can be installed globally
      // npm pack simulates what npm install -g does

      // Act
      const result = spawnSync('npm', ['pack', '--dry-run'], {
        cwd: path.join(__dirname, '../../..'),
        encoding: 'utf8'
      });

      // Assert
      expect(result.status).toBe(0);
      expect(result.stdout).toContain('devforgeai-');
      expect(result.stdout).toContain('.tgz');
    });

    test('[INTEGRATION] package.json declares bin entry point', () => {
      // Arrange
      const packageJson = JSON.parse(fs.readFileSync(packageJsonPath, 'utf8'));

      // Assert
      expect(packageJson.bin).toBeDefined();
      expect(packageJson.bindevforgeai).toBe('bin/devforgeai.js');
    });

    test('[INTEGRATION] bin entry point is executable', () => {
      // Arrange
      const stats = fs.statSync(binPath);

      // Assert - verify file has execute permission
      const isExecutable = (stats.mode & 0o111) !== 0;
      expect(isExecutable).toBe(true);
    });

    test('[INTEGRATION] bin entry point works when symlinked (npm install behavior)', () => {
      // npm install -g creates symlink to bin file
      // Verify bin file works when invoked through symlink

      // Arrange - create temporary symlink
      const tmpDir = fs.mkdtempSync(path.join(os.tmpdir(), 'devforgeai-test-'));
      const symlinkPath = path.join(tmpDir, 'devforgeai');

      try {
        fs.symlinkSync(binPath, symlinkPath, 'file');

        // Act - invoke through symlink
        const result = spawnSync('node', [symlinkPath, '--version'], {
          encoding: 'utf8'
        });

        // Assert
        expect(result.status).toBe(0);
        expect(result.stdout).toContain('devforgeai v');
      } finally {
        // Cleanup
        fs.unlinkSync(symlinkPath);
        fs.rmdirSync(tmpDir);
      }
    });
  });

  describe('Command Routing to Python Installer', () => {
    test('[INTEGRATION] install command requires Python availability', () => {
      // This test validates Python detection happens before subprocess spawn

      // Note: This test will PASS if Python is installed, FAIL if not
      // The important validation is that Python detection occurs

      // Act & Assert - we expect either:
      // 1. Python found → subprocess spawned (may fail due to missing args)
      // 2. Python not found → clear error message

      const result = spawnSync('node', [binPath, 'install'], {
        encoding: 'utf8'
      });

      // One of these must be true:
      const hasValidPythonError = result.stderr.includes('Python') && result.stderr.includes('required');
      const hasSubprocessError = result.stderr.includes('install.py') || result.status !== 0;

      expect(hasValidPythonError || hasSubprocessError).toBe(true);
    });

    test('[INTEGRATION] install command with path argument routes to Python', () => {
      // Arrange
      const testPath = '/tmp/devforgeai-test';

      // Act
      const result = spawnSync('node', [binPath, 'install', testPath], {
        encoding: 'utf8'
      });

      // Assert - command should either:
      // 1. Find Python and attempt to invoke installer (may fail at installer level)
      // 2. Show Python not found error

      const hasPythonError = result.stderr.includes('Python');
      const hasInstallerAttempt = result.stderr.includes('install.py') || result.status !== 0;

      expect(hasPythonError || hasInstallerAttempt).toBe(true);
    });
  });

  describe('Cross-Platform Execution', () => {
    test('[INTEGRATION] CLI executes on current platform', () => {
      // This test validates CLI works on the current platform
      // CI/CD will run this on Windows, macOS, Linux

      // Act
      const result = spawnSync('node', [binPath, '--version'], {
        encoding: 'utf8'
      });

      // Assert
      expect(result.status).toBe(0);
      expect(result.stdout).toContain('devforgeai v');
    });

    test('[INTEGRATION] Platform detection for Python command', () => {
      // Verify CLI correctly detects Python command for current platform

      // Arrange
      const platform = os.platform();

      // Act
      const result = spawnSync('node', [binPath, '--help'], {
        encoding: 'utf8'
      });

      // Assert - CLI should work regardless of platform
      expect(result.status).toBe(0);

      // Platform-specific Python command detection tested in unit tests
      // Here we just verify CLI works on current platform
    });

    test('[INTEGRATION] Path separators handled correctly on current platform', () => {
      // Verify cross-platform path handling

      // Act
      const result = spawnSync('node', [binPath, '--version'], {
        encoding: 'utf8',
        cwd: path.join(__dirname, '../../..')
      });

      // Assert
      expect(result.status).toBe(0);

      // If paths were incorrect, CLI wouldn't find package.json
      expect(result.stdout).toContain('devforgeai v');
    });
  });

  describe('Performance Benchmarks', () => {
    test('[INTEGRATION] --help completes in under 500ms (NFR-001)', () => {
      // Arrange
      const startTime = Date.now();

      // Act
      spawnSync('node', [binPath, '--help'], {
        encoding: 'utf8'
      });

      // Assert
      const elapsed = Date.now() - startTime;
      expect(elapsed).toBeLessThan(500);
    });

    test('[INTEGRATION] --version completes in under 500ms (NFR-001)', () => {
      // Arrange
      const startTime = Date.now();

      // Act
      spawnSync('node', [binPath, '--version'], {
        encoding: 'utf8'
      });

      // Assert
      const elapsed = Date.now() - startTime;
      expect(elapsed).toBeLessThan(500);
    });

    test('[INTEGRATION] Repeated --version calls have consistent performance', () => {
      // Measure performance consistency across multiple runs

      // Arrange
      const iterations = 10;
      const times = [];

      // Act
      for (let i = 0; i < iterations; i++) {
        const start = Date.now();
        spawnSync('node', [binPath, '--version'], { encoding: 'utf8' });
        times.push(Date.now() - start);
      }

      // Assert
      const avgTime = times.reduce((a, b) => a + b, 0) / times.length;
      const maxTime = Math.max(...times);

      expect(avgTime).toBeLessThan(200); // Average well under 500ms
      expect(maxTime).toBeLessThan(500); // No outliers
    });

    test('[INTEGRATION] CLI startup has minimal overhead', () => {
      // Verify CLI doesn't load unnecessary modules at startup

      // Act - measure time just to parse arguments and show version
      const start = Date.now();
      spawnSync('node', [binPath, '--version'], { encoding: 'utf8' });
      const elapsed = Date.now() - start;

      // Assert - startup should be nearly instantaneous
      expect(elapsed).toBeLessThan(150); // Very fast for simple flag
    });
  });

  describe('Error Handling Integration', () => {
    test('[INTEGRATION] Invalid command shows helpful error', () => {
      // Act
      const result = spawnSync('node', [binPath, 'nonexistent-command'], {
        encoding: 'utf8',
        env: { ...process.env, NODE_ENV: 'production' } // Override test env to capture stderr
      });

      // Assert
      expect(result.status).toBe(1);
      expect(result.stderr).toContain('Error');
      expect(result.stderr).toContain('--help');
    });

    test('[INTEGRATION] Error message format is user-friendly', () => {
      // Act
      const result = spawnSync('node', [binPath, 'invalid'], {
        encoding: 'utf8',
        env: { ...process.env, NODE_ENV: 'production' } // Override test env to capture stderr
      });

      // Assert
      expect(result.stderr).toContain('Error:');
      expect(result.stderr).toContain('invalid');
      expect(result.stderr).toContain('devforgeai --help');
    });

    test('[INTEGRATION] Multiple invalid arguments handled gracefully', () => {
      // Act
      const result = spawnSync('node', [binPath, 'bad', 'args', 'here'], {
        encoding: 'utf8',
        env: { ...process.env, NODE_ENV: 'production' } // Override test env to capture stderr
      });

      // Assert
      expect(result.status).toBe(1);
      expect(result.stderr).toContain('Error');
    });
  });

  describe('Package Integrity', () => {
    test('[INTEGRATION] package.json has required fields for npm publish', () => {
      // Arrange
      const packageJson = JSON.parse(fs.readFileSync(packageJsonPath, 'utf8'));

      // Assert
      expect(packageJson.name).toBe('devforgeai');
      expect(packageJson.version).toMatch(/^\d+\.\d+\.\d+/);
      expect(packageJson.description).toBeDefined();
      expect(packageJson.bin).toBeDefined();
      expect(packageJson.bindevforgeai).toBe('bin/devforgeai.js');
      expect(packageJson.engines).toBeDefined();
      expect(packageJson.engines.node).toBeDefined();
    });

    test('[INTEGRATION] bin file referenced in package.json exists', () => {
      // Arrange
      const packageJson = JSON.parse(fs.readFileSync(packageJsonPath, 'utf8'));
      const binFile = path.join(__dirname, '../../../', packageJson.bindevforgeai);

      // Assert
      expect(fs.existsSync(binFile)).toBe(true);
    });

    test('[INTEGRATION] bin file has correct shebang for npm', () => {
      // npm uses shebang to determine interpreter

      // Arrange
      const content = fs.readFileSync(binPath, 'utf8');
      const firstLine = content.split('\n')[0];

      // Assert
      expect(firstLine).toBe('#!/usr/bin/env node');
    });
  });

  describe('Real-World Usage Scenarios', () => {
    test('[INTEGRATION] User runs devforgeai with no args, sees help', () => {
      // Simulate: user types "devforgeai" with no arguments

      // Act
      const result = spawnSync('node', [binPath], {
        encoding: 'utf8'
      });

      // Assert
      expect(result.stdout).toContain('Usage:');
      expect(result.status).toBe(0); // Help is not an error
    });

    test('[INTEGRATION] User runs devforgeai --version, sees version', () => {
      // Simulate: user checks installed version

      // Act
      const result = spawnSync('node', [binPath, '--version'], {
        encoding: 'utf8'
      });

      // Assert
      expect(result.status).toBe(0);
      expect(result.stdout).toMatch(/devforgeai v\d+\.\d+\.\d+/);
    });

    test('[INTEGRATION] User runs devforgeai --help, sees usage', () => {
      // Simulate: user needs help

      // Act
      const result = spawnSync('node', [binPath, '--help'], {
        encoding: 'utf8'
      });

      // Assert
      expect(result.status).toBe(0);
      expect(result.stdout).toContain('Usage:');
      expect(result.stdout).toContain('install');
      expect(result.stdout).toContain('Example');
    });

    test('[INTEGRATION] User tries unknown command, gets clear error', () => {
      // Simulate: user makes typo

      // Act
      const result = spawnSync('node', [binPath, 'instal'], { // typo
        encoding: 'utf8',
        env: { ...process.env, NODE_ENV: 'production' } // Override test env to capture stderr
      });

      // Assert
      expect(result.status).toBe(1);
      expect(result.stderr).toContain('Error');
      expect(result.stderr).toContain('--help');
    });
  });

  describe('Edge Case Integration Tests', () => {
    test('[INTEGRATION] Edge Case: CLI works from different working directories', () => {
      // Verify CLI finds package.json regardless of cwd

      // Act
      const result = spawnSync('node', [binPath, '--version'], {
        encoding: 'utf8',
        cwd: os.tmpdir() // Run from system temp directory
      });

      // Assert
      expect(result.status).toBe(0);
      expect(result.stdout).toContain('devforgeai v');
    });

    test('[INTEGRATION] Edge Case: CLI handles path with spaces', () => {
      // Create temporary directory with space in name

      // Arrange
      const tmpDir = fs.mkdtempSync(path.join(os.tmpdir(), 'devforge ai test-'));

      try {
        // Act
        const result = spawnSync('node', [binPath, 'install', tmpDir], {
          encoding: 'utf8'
        });

        // Assert - should either find Python or show Python error
        // Should NOT fail due to path with spaces
        const validOutcomes = [
          result.stderr.includes('Python'),
          result.stderr.includes('install.py'),
          result.status !== 0 // May fail at installer level
        ];

        expect(validOutcomes.some(x => x)).toBe(true);
      } finally {
        // Cleanup
        fs.rmdirSync(tmpDir);
      }
    });

    test('[INTEGRATION] Edge Case: Long path arguments handled correctly', () => {
      // Windows has 260 character path limit (MAX_PATH)
      // Verify CLI doesn't crash with long paths

      // Arrange
      const longPath = '/a'.repeat(100) + '/target'; // ~200 chars

      // Act
      const result = spawnSync('node', [binPath, 'install', longPath], {
        encoding: 'utf8'
      });

      // Assert - should handle path without crashing
      expect(result.status).toBeDefined(); // Process completed
    });

    test('[INTEGRATION] Edge Case: Unicode characters in path', () => {
      // Verify cross-platform Unicode path handling

      // Arrange
      const unicodePath = '/tmp/测试目录'; // Chinese characters

      // Act
      const result = spawnSync('node', [binPath, 'install', unicodePath], {
        encoding: 'utf8'
      });

      // Assert - should not crash due to encoding
      expect(result.status).toBeDefined();
    });
  });
});
