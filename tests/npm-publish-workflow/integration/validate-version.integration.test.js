/**
 * Integration Test Suite: Version Validation Script - Main Function Execution
 * Story: STORY-067 - NPM Registry Publishing Workflow
 *
 * Tests cover:
 * - Lines 151-184: main() function error handling paths
 * - Line 199: main() execution guard (require.main === module)
 * - Real script execution with process.exit() and console output
 */

const fs = require('fs');
const path = require('path');
const { execSync, spawn } = require('child_process');

describe('Version Validation Script - Main Function Integration', () => {
  const scriptPath = path.resolve('.github/scripts/validate-version.js');
  const testDir = path.resolve('tests/npm-publish-workflow/fixtures');

  beforeAll(() => {
    // Ensure test fixtures directory exists
    if (!fs.existsSync(testDir)) {
      fs.mkdirSync(testDir, { recursive: true });
    }
  });

  afterAll(() => {
    // Clean up test fixtures
    if (fs.existsSync(testDir)) {
      fs.rmSync(testDir, { recursive: true, force: true });
    }
  });

  describe('Main Function - Command Line Argument Handling (Line 151)', () => {
    test('should exit with code 0 when tag matches package.json version', () => {
      // Arrange
      const testPackageJson = path.join(testDir, 'package.json');
      fs.writeFileSync(
        testPackageJson,
        JSON.stringify({ name: 'test', version: '1.0.0' }, null, 2)
      );

      // Act
      const result = execSync(
        `cd ${testDir} && node ${scriptPath} v1.0.0`,
        { encoding: 'utf8' }
      );

      // Assert
      expect(result).toContain('Version validation passed');
      expect(result).toContain('v1.0.0');
      expect(result).toContain('1.0.0');

      // Cleanup
      fs.unlinkSync(testPackageJson);
    });

    test('should exit with code 1 when no tag provided', (done) => {
      // Arrange
      const testPackageJson = path.join(testDir, 'package.json');
      fs.writeFileSync(
        testPackageJson,
        JSON.stringify({ name: 'test', version: '1.0.0' }, null, 2)
      );

      // Act
      const child = spawn('node', [scriptPath], {
        cwd: testDir,
        env: { ...process.env, GITHUB_REF: undefined }
      });

      let stderr = '';
      child.stderr.on('data', (data) => {
        stderr += data.toString();
      });

      child.on('close', (code) => {
        // Assert
        expect(code).toBe(1);
        expect(stderr).toContain('No tag provided');
        expect(stderr).toContain('Usage: node validate-version.js <tag>');

        // Cleanup
        fs.unlinkSync(testPackageJson);
        done();
      });
    });

    test('should use GITHUB_REF environment variable when argv not provided', () => {
      // Arrange
      const testPackageJson = path.join(testDir, 'package.json');
      fs.writeFileSync(
        testPackageJson,
        JSON.stringify({ name: 'test', version: '2.0.0' }, null, 2)
      );

      // Act
      const result = execSync(
        `node ${scriptPath}`,
        {
          cwd: testDir,
          env: { ...process.env, GITHUB_REF: 'refs/tags/v2.0.0' },
          encoding: 'utf8'
        }
      );

      // Assert
      expect(result).toContain('Version validation passed');
      expect(result).toContain('v2.0.0');

      // Cleanup
      fs.unlinkSync(testPackageJson);
    });

    test('should strip refs/tags/ prefix from GITHUB_REF', () => {
      // Arrange
      const testPackageJson = path.join(testDir, 'package.json');
      fs.writeFileSync(
        testPackageJson,
        JSON.stringify({ name: 'test', version: '1.5.0-beta.1' }, null, 2)
      );

      // Act
      const result = execSync(
        `node ${scriptPath}`,
        {
          cwd: testDir,
          env: { ...process.env, GITHUB_REF: 'refs/tags/v1.5.0-beta.1' },
          encoding: 'utf8'
        }
      );

      // Assert
      expect(result).toContain('Version validation passed');
      expect(result).toContain('v1.5.0-beta.1');

      // Cleanup
      fs.unlinkSync(testPackageJson);
    });
  });

  describe('Main Function - package.json Error Handling (Lines 162-174)', () => {
    test('should exit with code 1 when package.json not found', (done) => {
      // Arrange
      const emptyTestDir = path.join(testDir, 'no-package-json');
      fs.mkdirSync(emptyTestDir, { recursive: true });

      // Act
      const child = spawn('node', [scriptPath, 'v1.0.0'], {
        cwd: emptyTestDir
      });

      let stderr = '';
      child.stderr.on('data', (data) => {
        stderr += data.toString();
      });

      child.on('close', (code) => {
        // Assert
        expect(code).toBe(1);
        expect(stderr).toContain('package.json not found');

        // Cleanup
        fs.rmSync(emptyTestDir, { recursive: true, force: true });
        done();
      });
    });

    test('should exit with code 1 when package.json has invalid JSON', (done) => {
      // Arrange
      const testPackageJson = path.join(testDir, 'package.json');
      fs.writeFileSync(testPackageJson, '{ invalid json {{{');

      // Act
      const child = spawn('node', [scriptPath, 'v1.0.0'], {
        cwd: testDir
      });

      let stderr = '';
      child.stderr.on('data', (data) => {
        stderr += data.toString();
      });

      child.on('close', (code) => {
        // Assert
        expect(code).toBe(1);
        expect(stderr).toContain('Error reading package.json');

        // Cleanup
        fs.unlinkSync(testPackageJson);
        done();
      });
    });

    test('should exit with code 1 when package.json has malformed syntax', (done) => {
      // Arrange
      const testPackageJson = path.join(testDir, 'package.json');
      fs.writeFileSync(testPackageJson, '{ "version": "1.0.0", }'); // Trailing comma

      // Act
      const child = spawn('node', [scriptPath, 'v1.0.0'], {
        cwd: testDir
      });

      let stderr = '';
      child.stderr.on('data', (data) => {
        stderr += data.toString();
      });

      child.on('close', (code) => {
        // Assert
        expect(code).toBe(1);
        expect(stderr).toContain('Error reading package.json');

        // Cleanup
        fs.unlinkSync(testPackageJson);
        done();
      });
    });
  });

  describe('Main Function - Validation Error Handling (Lines 177-185)', () => {
    test('should exit with code 1 when tag format is invalid', (done) => {
      // Arrange
      const testPackageJson = path.join(testDir, 'package.json');
      fs.writeFileSync(
        testPackageJson,
        JSON.stringify({ name: 'test', version: '1.0.0' }, null, 2)
      );

      // Act
      const child = spawn('node', [scriptPath, 'invalid-tag'], {
        cwd: testDir
      });

      let stderr = '';
      child.stderr.on('data', (data) => {
        stderr += data.toString();
      });

      child.on('close', (code) => {
        // Assert
        expect(code).toBe(1);
        expect(stderr).toContain('Version validation failed');
        expect(stderr).toContain('Invalid tag format');

        // Cleanup
        fs.unlinkSync(testPackageJson);
        done();
      });
    });

    test('should exit with code 1 when tag version mismatches package.json', (done) => {
      // Arrange
      const testPackageJson = path.join(testDir, 'package.json');
      fs.writeFileSync(
        testPackageJson,
        JSON.stringify({ name: 'test', version: '1.0.0' }, null, 2)
      );

      // Act
      const child = spawn('node', [scriptPath, 'v2.0.0'], {
        cwd: testDir
      });

      let stderr = '';
      child.stderr.on('data', (data) => {
        stderr += data.toString();
      });

      child.on('close', (code) => {
        // Assert
        expect(code).toBe(1);
        expect(stderr).toContain('Version validation failed');
        expect(stderr).toContain('Version mismatch');
        expect(stderr).toContain('2.0.0');
        expect(stderr).toContain('1.0.0');

        // Cleanup
        fs.unlinkSync(testPackageJson);
        done();
      });
    });

    test('should exit with code 1 when package.json missing version field', (done) => {
      // Arrange
      const testPackageJson = path.join(testDir, 'package.json');
      fs.writeFileSync(
        testPackageJson,
        JSON.stringify({ name: 'test' }, null, 2) // No version
      );

      // Act
      const child = spawn('node', [scriptPath, 'v1.0.0'], {
        cwd: testDir
      });

      let stderr = '';
      child.stderr.on('data', (data) => {
        stderr += data.toString();
      });

      child.on('close', (code) => {
        // Assert
        expect(code).toBe(1);
        expect(stderr).toContain('Version validation failed');
        expect(stderr).toContain('Missing version field');

        // Cleanup
        fs.unlinkSync(testPackageJson);
        done();
      });
    });

    test('should display success message on successful validation', () => {
      // Arrange
      const testPackageJson = path.join(testDir, 'package.json');
      fs.writeFileSync(
        testPackageJson,
        JSON.stringify({ name: 'test', version: '3.2.1' }, null, 2)
      );

      // Act
      const result = execSync(
        `cd ${testDir} && node ${scriptPath} v3.2.1`,
        { encoding: 'utf8' }
      );

      // Assert
      expect(result).toContain('✓ Version validation passed');
      expect(result).toContain('v3.2.1 matches package.json 3.2.1');

      // Cleanup
      fs.unlinkSync(testPackageJson);
    });

    test('should display error message prefix on failed validation', (done) => {
      // Arrange
      const testPackageJson = path.join(testDir, 'package.json');
      fs.writeFileSync(
        testPackageJson,
        JSON.stringify({ name: 'test', version: '1.0.0' }, null, 2)
      );

      // Act
      const child = spawn('node', [scriptPath, 'v1.0.1'], {
        cwd: testDir
      });

      let stderr = '';
      child.stderr.on('data', (data) => {
        stderr += data.toString();
      });

      child.on('close', (code) => {
        // Assert
        expect(stderr).toContain('✗ Version validation failed');

        // Cleanup
        fs.unlinkSync(testPackageJson);
        done();
      });
    });
  });

  describe('Main Function - Prerelease Handling', () => {
    test('should validate prerelease versions correctly', () => {
      // Arrange
      const testPackageJson = path.join(testDir, 'package.json');
      fs.writeFileSync(
        testPackageJson,
        JSON.stringify({ name: 'test', version: '2.0.0-rc.1' }, null, 2)
      );

      // Act
      const result = execSync(
        `cd ${testDir} && node ${scriptPath} v2.0.0-rc.1`,
        { encoding: 'utf8' }
      );

      // Assert
      expect(result).toContain('Version validation passed');
      expect(result).toContain('v2.0.0-rc.1');

      // Cleanup
      fs.unlinkSync(testPackageJson);
    });

    test('should detect prerelease mismatch', (done) => {
      // Arrange
      const testPackageJson = path.join(testDir, 'package.json');
      fs.writeFileSync(
        testPackageJson,
        JSON.stringify({ name: 'test', version: '2.0.0-rc.1' }, null, 2)
      );

      // Act
      const child = spawn('node', [scriptPath, 'v2.0.0-rc.2'], {
        cwd: testDir
      });

      let stderr = '';
      child.stderr.on('data', (data) => {
        stderr += data.toString();
      });

      child.on('close', (code) => {
        // Assert
        expect(code).toBe(1);
        expect(stderr).toContain('Version mismatch');
        expect(stderr).toContain('rc.2');
        expect(stderr).toContain('rc.1');

        // Cleanup
        fs.unlinkSync(testPackageJson);
        done();
      });
    });
  });

  describe('require.main === module Guard (Line 199)', () => {
    test('should execute main() when run as script directly', () => {
      // Arrange
      const testPackageJson = path.join(testDir, 'package.json');
      fs.writeFileSync(
        testPackageJson,
        JSON.stringify({ name: 'test', version: '1.0.0' }, null, 2)
      );

      // Act - Execute script directly (not as module)
      const result = execSync(
        `cd ${testDir} && node ${scriptPath} v1.0.0`,
        { encoding: 'utf8' }
      );

      // Assert - Main function executes (output shows validation result)
      expect(result).toContain('Version validation passed');

      // Cleanup
      fs.unlinkSync(testPackageJson);
    });

    test('should NOT execute main() when required as module', () => {
      // Arrange & Act
      const validateVersion = require(scriptPath);

      // Assert - Module exports functions but doesn't execute main
      expect(validateVersion).toHaveProperty('stripVPrefix');
      expect(validateVersion).toHaveProperty('isValidSemverTag');
      expect(validateVersion).toHaveProperty('checkVersionMatch');
      expect(validateVersion).toHaveProperty('validate');
      expect(validateVersion).toHaveProperty('extractVersion');
    });
  });

  describe('Real-World Scenarios', () => {
    test('should validate against actual project package.json', () => {
      // Arrange
      const projectPackageJson = path.resolve('package.json');
      const projectPackage = JSON.parse(fs.readFileSync(projectPackageJson, 'utf8'));
      const expectedTag = `v${projectPackage.version}`;

      // Act
      const result = execSync(
        `node ${scriptPath} ${expectedTag}`,
        { encoding: 'utf8' }
      );

      // Assert
      expect(result).toContain('Version validation passed');
      expect(result).toContain(expectedTag);
    });

    test('should work with GitHub Actions GITHUB_REF format', () => {
      // Arrange
      const testPackageJson = path.join(testDir, 'package.json');
      fs.writeFileSync(
        testPackageJson,
        JSON.stringify({ name: 'test', version: '1.2.3' }, null, 2)
      );

      // Act - Simulate GitHub Actions environment
      const result = execSync(
        `node ${scriptPath}`,
        {
          cwd: testDir,
          env: { ...process.env, GITHUB_REF: 'refs/tags/v1.2.3' },
          encoding: 'utf8'
        }
      );

      // Assert
      expect(result).toContain('Version validation passed');

      // Cleanup
      fs.unlinkSync(testPackageJson);
    });
  });
});
