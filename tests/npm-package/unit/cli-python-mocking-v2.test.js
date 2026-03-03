/**
 * Python Detection Tests with Module-Level Mocking (v2)
 * Based on Jest best practices from research
 */

// Step 1: Mock child_process BEFORE any imports
jest.mock('child_process', () => {
  const originalModule = jest.requireActual('child_process');

  return {
    ...originalModule,
    execSync: jest.fn(),
    spawn: jest.fn()
  };
});

// Step 2: NOW import the modules AFTER mock is established
const { execSync, spawn } = require('child_process');
const cli = require('../../../lib/cli');

// Step 3: Set test environment
process.env.NODE_ENV = 'test';

describe('CLI Python Detection (v2 - Proper Mocking)', () => {

  beforeEach(() => {
    // Clear all mocks before each test
    execSync.mockClear();
    spawn.mockClear();
  });

  describe('Python version < 3.10 (Too Old)', () => {
    test('throws error when Python 3.9 detected', () => {
      // Use mockImplementation (persistent) not mockImplementationOnce
      execSync.mockImplementation(() => {
        console.log('[MOCK] Returning Python 3.9.0');
        return 'Python 3.9.0';
      });

      try {
        cli.checkPython();
        throw new Error('Test failed: checkPython should have thrown');
      } catch (error) {
        console.log('[TEST] Caught error:', error.message.substring(0, 80));
        expect(error.message).toMatch(/Python version mismatch/);
      }
    });

    test('error message shows found version 3.9', () => {
      execSync.mockImplementation(() => 'Python 3.9.7');

      try {
        cli.checkPython();
        throw new Error('Should have thrown');
      } catch (error) {
        expect(error.message).toContain('Found: Python 3.9');
        expect(error.message).toContain('Required: Python 3.10+');
      }
    });

    test('throws error when Python 2.7 detected', () => {
      execSync.mockImplementation(() => 'Python 2.7.18');

      try {
        cli.checkPython();
        throw new Error('Should have thrown');
      } catch (error) {
        expect(error.message).toMatch(/Python version mismatch/);
      }
    });
  });

  describe('Python Not Found', () => {
    test('throws error when python3 command not found', () => {
      execSync.mockImplementation(() => {
        const error = new Error('spawn python3 ENOENT');
        error.code = 'ENOENT';
        throw error;
      });

      expect(() => {
        cli.checkPython();
      }).toThrow(/Python 3\.10\+ required/);
    });

    test('error includes installation instructions', () => {
      execSync.mockImplementation(() => {
        throw new Error('Command not found');
      });

      try {
        cli.checkPython();
        throw new Error('Should have thrown');
      } catch (error) {
        expect(error.message).toContain('Install Python 3.10+');
        expect(error.message).toContain('https://www.python.org');
        expect(error.message).toContain('python3 --version');
      }
    });
  });

  describe('Python Valid Version', () => {
    test('accepts Python 3.10', () => {
      execSync.mockImplementation(() => 'Python 3.10.0');

      const result = cli.checkPython();
      expect(result).toBeDefined();
      expect(result.command).toMatch(/^(python3|python)$/);
      expect(result.version.major).toBe(3);
      expect(result.version.minor).toBe(10);
    });

    test('accepts Python 3.11', () => {
      execSync.mockImplementation(() => 'Python 3.11.5');

      const result = cli.checkPython();
      expect(result).toBeDefined();
      expect(result.version.major).toBe(3);
      expect(result.version.minor).toBe(11);
    });

    test('accepts Python 3.12+', () => {
      execSync.mockImplementation(() => 'Python 3.12.1');

      const result = cli.checkPython();
      expect(result).toBeDefined();
      expect(result.version.major).toBe(3);
      expect(result.version.minor).toBe(12);
    });
  });

  describe('Subprocess Invocation', () => {
    test('spawn is called with correct arguments', () => {
      // Mock Python check to succeed
      execSync.mockImplementation(() => 'Python 3.10.11');

      // Mock spawn to return mock process
      const mockProcess = {
        on: jest.fn(),
        kill: jest.fn()
      };
      spawn.mockReturnValue(mockProcess);

      const result = cli.invokePythonInstaller(['install', '/tmp/test']);

      expect(spawn).toHaveBeenCalledWith(
        'python3',
        expect.arrayContaining([expect.stringContaining('install.py'), 'install', '/tmp/test']),
        expect.objectContaining({
          stdio: 'inherit'
        })
      );

      expect(result).toBe(mockProcess);
    });

    test('subprocess error handler triggered on spawn error', (done) => {
      // Mock spawn to trigger error event (line 160-162 in lib/cli.js)
      const mockProcess = {
        on: jest.fn((event, handler) => {
          if (event === 'error') {
            // Immediately trigger error to cover error handler
            setImmediate(() => {
              const error = new Error('spawn ENOENT');
              error.code = 'ENOENT';
              try {
                handler(error);
              } catch (e) {
                // exitWithError throws, which we expect
                expect(e.message).toContain('Failed to invoke Python installer');
                done();
              }
            });
          }
          return mockProcess;
        }),
        kill: jest.fn()
      };

      spawn.mockReturnValue(mockProcess);

      const result = cli.invokePythonInstaller(['install', '/tmp/test']);

      expect(result).toBe(mockProcess);
    });
  });

});
