/**
 * Python Detection Tests with Proper Mocking
 * Tests error paths by mocking child_process at module level
 */

const fs = require('fs');
const path = require('path');

// Mock child_process BEFORE requiring cli module
jest.mock('child_process');

describe('CLI Python Detection (Mocked)', () => {
  let cli;
  let childProcess;

  beforeEach(() => {
    // Clear module cache to get fresh imports
    jest.resetModules();

    // Get mocked child_process
    childProcess = require('child_process');

    // Set test environment
    process.env.NODE_ENV = 'test';
  });

  afterEach(() => {
    jest.restoreAllMocks();
  });

  describe('Python not found scenarios', () => {
    test('checkPython throws when Python command not found', () => {
      // Mock execSync to throw ENOENT (command not found)
      childProcess.execSync.mockImplementation(() => {
        const error = new Error('spawn python3 ENOENT');
        error.code = 'ENOENT';
        throw error;
      });

      // Require cli AFTER mocking
      cli = require('../../../lib/cli');

      expect(() => {
        cli.checkPython();
      }).toThrow(/Python 3\.10\+ required/);
    });

    test('error message includes resolution steps', () => {
      childProcess.execSync.mockImplementation(() => {
        const error = new Error('Command not found');
        throw error;
      });

      cli = require('../../../lib/cli');

      try {
        cli.checkPython();
      } catch (error) {
        expect(error.message).toContain('Install Python');
        expect(error.message).toContain('https://www.python.org');
      }
    });
  });

  describe('Python version too old scenarios', () => {
    test('checkPython throws when Python version < 3.10', () => {
      // Mock execSync to return old Python version
      // NOTE: lib/cli.js uses encoding:'utf8', so execSync returns string (not Buffer)
      childProcess.execSync.mockReturnValue('Python 3.9.0');

      cli = require('../../../lib/cli');

      expect(() => {
        cli.checkPython();
      }).toThrow(/Python version mismatch/);
    });

    test('error message shows found vs required version', () => {
      childProcess.execSync.mockReturnValue('Python 2.7.18');

      cli = require('../../../lib/cli');

      try {
        cli.checkPython();
      } catch (error) {
        expect(error.message).toContain('Found: Python 2.7');
        expect(error.message).toContain('Required: Python 3.10+');
      }
    });
  });

  describe('Python version validation logic', () => {
    test('accepts Python 3.10.x', () => {
      childProcess.execSync.mockReturnValue('Python 3.10.11');

      cli = require('../../../lib/cli');

      const result = cli.checkPython();
      expect(result).toBe(true);
    });

    test('accepts Python 3.11+', () => {
      childProcess.execSync.mockReturnValue('Python 3.11.5');

      cli = require('../../../lib/cli');

      const result = cli.checkPython();
      expect(result).toBe(true);
    });

    test('accepts Python 4.x (future)', () => {
      childProcess.execSync.mockReturnValue('Python 4.0.0');

      cli = require('../../../lib/cli');

      const result = cli.checkPython();
      expect(result).toBe(true);
    });
  });

  describe('subprocess invocation', () => {
    test('invokePythonInstaller spawns python3 with correct args', () => {
      // Mock spawn
      const mockProcess = {
        on: jest.fn(),
        kill: jest.fn()
      };
      childProcess.spawn.mockReturnValue(mockProcess);
      childProcess.execSync.mockReturnValue('Python 3.10.11\n');

      cli = require('../../../lib/cli');

      const result = cli.invokePythonInstaller(['install', '/tmp/test']);

      expect(childProcess.spawn).toHaveBeenCalledWith(
        'python3',
        expect.arrayContaining(['install', '/tmp/test']),
        expect.objectContaining({
          stdio: 'inherit'
        })
      );

      expect(result).toBe(mockProcess);
    });
  });
});
