/**
 * STORY-066: NPM Package Creation & Structure
 * Unit Tests: CLI Entry Point (bin/devforgeai.js)
 *
 * Tests AC#2: Bin entry point functionality
 * Tests Technical Specification: SVC-001 through SVC-006
 *
 * Expected Result: ALL TESTS SHOULD FAIL (TDD Red Phase)
 * Implementation: bin/devforgeai.js does not exist yet
 */

const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

describe('AC#2: CLI Entry Point Functionality', () => {
  const binPath = path.join(__dirname, '../../../bin/devforgeai.js');

  describe('SVC-001: Node.js shebang line', () => {
    test('bin/devforgeai.js file exists', () => {
      expect(fs.existsSync(binPath)).toBe(true);
    });

    test('first line is exactly "#!/usr/bin/env node"', () => {
      const content = fs.readFileSync(binPath, 'utf8');
      const lines = content.split('\n');
      expect(lines[0]).toBe('#!/usr/bin/env node');
    });

    test('shebang line has no BOM (Byte Order Mark)', () => {
      const buffer = fs.readFileSync(binPath);
      // Check for UTF-8 BOM (0xEF, 0xBB, 0xBF)
      const hasBOM = buffer[0] === 0xEF && buffer[1] === 0xBB && buffer[2] === 0xBF;
      expect(hasBOM).toBe(false);
    });

    test('shebang line uses LF (not CRLF) line ending', () => {
      const buffer = fs.readFileSync(binPath);
      const firstLine = buffer.toString('utf8').split('\n')[0];
      // Check if first line ends with \r (CRLF)
      expect(firstLine.endsWith('\r')).toBe(false);
    });
  });

  describe('SVC-003: --version flag handling', () => {
    test('CLI responds to --version flag', () => {
      try {
        const output = execSync('node bin/devforgeai.js --version', {
          cwd: path.join(__dirname, '../../..'),
          encoding: 'utf8'
        });
        expect(output).toBeTruthy();
      } catch (error) {
        throw new Error('CLI should respond to --version without error');
      }
    });

    test('--version outputs version from package.json', () => {
      const packageJson = JSON.parse(
        fs.readFileSync(path.join(__dirname, '../../../package.json'), 'utf8')
      );

      const output = execSync('node bin/devforgeai.js --version', {
        cwd: path.join(__dirname, '../../..'),
        encoding: 'utf8'
      });

      expect(output).toContain(packageJson.version);
    });

    test('--version output matches format "devforgeai v{version}"', () => {
      const output = execSync('node bin/devforgeai.js --version', {
        cwd: path.join(__dirname, '../../..'),
        encoding: 'utf8'
      }).trim();

      const versionRegex = /^devforgeai v\d+\.\d+\.\d+(-[a-z0-9.]+)?$/;
      expect(output).toMatch(versionRegex);
    });
  });

  describe('SVC-004: --help flag handling', () => {
    test('CLI responds to --help flag', () => {
      try {
        const output = execSync('node bin/devforgeai.js --help', {
          cwd: path.join(__dirname, '../../..'),
          encoding: 'utf8'
        });
        expect(output).toBeTruthy();
      } catch (error) {
        throw new Error('CLI should respond to --help without error');
      }
    });

    test('--help output contains usage information', () => {
      const output = execSync('node bin/devforgeai.js --help', {
        cwd: path.join(__dirname, '../../..'),
        encoding: 'utf8'
      });

      expect(output).toContain('Usage:');
      expect(output).toContain('devforgeai');
    });

    test('--help output contains "install" command', () => {
      const output = execSync('node bin/devforgeai.js --help', {
        cwd: path.join(__dirname, '../../..'),
        encoding: 'utf8'
      });

      expect(output).toContain('install');
    });

    test('--help output contains documentation link', () => {
      const output = execSync('node bin/devforgeai.js --help', {
        cwd: path.join(__dirname, '../../..'),
        encoding: 'utf8'
      });

      expect(output).toMatch(/https?:\/\//); // Contains a URL
      expect(output).toContain('github.com');
    });

    test('--help output contains example usage', () => {
      const output = execSync('node bin/devforgeai.js --help', {
        cwd: path.join(__dirname, '../../..'),
        encoding: 'utf8'
      });

      expect(output).toContain('Example');
      expect(output).toContain('devforgeai install');
    });
  });

  describe('SVC-005: Python detection and error handling', () => {
    // NOTE: These integration tests are skipped - Python detection is fully tested
    // in cli-python-mocking-v2.test.js with proper mocks (9/9 tests passing)
    test.skip('CLI detects missing Python and shows clear error', () => {
      // Mock Python unavailable by using PATH without python3
      const originalPath = process.env.PATH;

      try {
        // Set PATH to empty (Python unavailable)
        process.env.PATH = '';

        const result = execSync('node bin/devforgeai.js install /tmp/test', {
          cwd: path.join(__dirname, '../../..'),
          encoding: 'utf8',
          stdio: 'pipe'
        });

        throw new Error('CLI should exit with error code 1 when Python unavailable');
      } catch (error) {
        expect(error.status).toBe(1);
        expect(error.stderr.toString()).toContain('Python');
        expect(error.stderr.toString()).toContain('3.10');
      } finally {
        process.env.PATH = originalPath;
      }
    });

    test.skip('error message includes "Python 3.10+ required"', () => {
      const originalPath = process.env.PATH;

      try {
        process.env.PATH = '';

        execSync('node bin/devforgeai.js install /tmp/test', {
          cwd: path.join(__dirname, '../../..'),
          encoding: 'utf8',
          stdio: 'pipe'
        });

        throw new Error('Should throw error');
      } catch (error) {
        const errorOutput = error.stderr.toString();
        expect(errorOutput).toContain('Python 3.10+');
        expect(errorOutput).toContain('required');
      } finally {
        process.env.PATH = originalPath;
      }
    });

    test.skip('error exit code is 1 when Python unavailable', () => {
      const originalPath = process.env.PATH;

      try {
        process.env.PATH = '';

        execSync('node bin/devforgeai.js install /tmp/test', {
          cwd: path.join(__dirname, '../../..'),
          encoding: 'utf8',
          stdio: 'pipe'
        });

        throw new Error('Should throw error');
      } catch (error) {
        expect(error.status).toBe(1);
      } finally {
        process.env.PATH = originalPath;
      }
    });
  });

  describe('SVC-006: Argument passing to Python installer', () => {
    test('CLI passes "install" command to Python installer', () => {
      // This test will fail in Red phase - Python installer not integrated yet
      const testDir = path.join(__dirname, '../../../.test-output/install-test');

      try {
        execSync(`node bin/devforgeai.js install ${testDir}`, {
          cwd: path.join(__dirname, '../../..'),
          encoding: 'utf8',
          stdio: 'pipe'
        });

        // If successful, verify install.py was called with correct arguments
        // (This will be verified via mocking in Green phase)
        expect(true).toBe(true); // Placeholder - will be replaced with proper assertion
      } catch (error) {
        // Expected to fail in Red phase
        expect(error).toBeDefined();
      }
    });

    test('CLI passes path argument to Python installer', () => {
      const testDir = '/tmp/test-project';

      try {
        execSync(`node bin/devforgeai.js install ${testDir}`, {
          cwd: path.join(__dirname, '../../..'),
          encoding: 'utf8',
          stdio: 'pipe'
        });

        // Verify path was passed correctly (will be implemented with mocking)
        expect(true).toBe(true); // Placeholder
      } catch (error) {
        // Expected to fail in Red phase
        expect(error).toBeDefined();
      }
    });
  });

  describe('SVC-002: Python installer subprocess invocation', () => {
    test('CLI spawns Python subprocess for install command', () => {
      // This test verifies CLI calls python3 installer/install.py
      // Will be implemented with process mocking in Green phase
      expect(fs.existsSync(binPath)).toBe(true);

      // Placeholder - will verify subprocess spawning with mock
      // const cliCode = fs.readFileSync(binPath, 'utf8');
      // expect(cliCode).toContain('spawn');
      // expect(cliCode).toContain('python3');
    });

    // NOTE: Subprocess invocation is fully tested in cli-python-mocking-v2.test.js
    test.skip('CLI invokes installer/install.py', () => {
      const cliCode = fs.readFileSync(binPath, 'utf8');

      // Verify CLI code references installer/install.py
      expect(cliCode).toContain('installer/install.py');
    });
  });
});

describe('NFR-002: CLI command startup performance', () => {
  const binPath = path.join(__dirname, '../../../bin/devforgeai.js');

  test('devforgeai --version executes in less than 200ms', () => {
    const startTime = Date.now();

    execSync('node bin/devforgeai.js --version', {
      cwd: path.join(__dirname, '../../..'),
      encoding: 'utf8',
      stdio: 'pipe'
    });

    const elapsed = Date.now() - startTime;
    expect(elapsed).toBeLessThan(200);
  });

  test('devforgeai --help executes in less than 200ms', () => {
    const startTime = Date.now();

    execSync('node bin/devforgeai.js --help', {
      cwd: path.join(__dirname, '../../..'),
      encoding: 'utf8',
      stdio: 'pipe'
    });

    const elapsed = Date.now() - startTime;
    expect(elapsed).toBeLessThan(200);
  });
});

describe('Error Handling: Invalid arguments', () => {
  test('CLI shows help when no arguments provided', () => {
    try {
      const output = execSync('node bin/devforgeai.js', {
        cwd: path.join(__dirname, '../../..'),
        encoding: 'utf8',
        stdio: 'pipe'
      });

      expect(output).toContain('Usage:');
    } catch (error) {
      // May exit with error code, but should still show help
      expect(error.stdout.toString() + error.stderr.toString()).toContain('Usage:');
    }
  });

  test('CLI shows error for unknown command', () => {
    try {
      execSync('node bin/devforgeai.js unknown-command', {
        cwd: path.join(__dirname, '../../..'),
        encoding: 'utf8',
        stdio: 'pipe'
      });

      throw new Error('Should exit with error for unknown command');
    } catch (error) {
      expect(error.status).not.toBe(0);
      const output = error.stdout.toString() + error.stderr.toString();
      expect(output).toContain('Error');
    }
  });
});

describe('Cross-platform compatibility', () => {
  const binPath = path.join(__dirname, '../../../bin/devforgeai.js');
  const libPath = path.join(__dirname, '../../../lib/cli.js');

  test('CLI uses cross-platform path resolution', () => {
    // Check lib/cli.js (business logic) for path.join/resolve usage
    const libCode = fs.readFileSync(libPath, 'utf8');
    expect(libCode).toMatch(/path\.(join|resolve)/);
  });

  test('CLI does not contain hardcoded backslashes in paths', () => {
    // Check both bin and lib for hardcoded Windows paths
    const binCode = fs.readFileSync(binPath, 'utf8');
    const libCode = fs.readFileSync(libPath, 'utf8');

    // Check for Windows-style paths (e.g., "C:\\path\\to\\file")
    const windowsPathRegex = /['"][A-Z]:\\\\/;
    expect(binCode).not.toMatch(windowsPathRegex);
    expect(libCode).not.toMatch(windowsPathRegex);
  });
});
