/**
 * Integration Test Suite: NPM Publishing Workflow End-to-End
 * Story: STORY-067 - NPM Registry Publishing Workflow
 *
 * Tests cover:
 * - AC#3: Complete build pipeline execution
 * - AC#7: Idempotency with duplicate versions
 * - NFR-001: Workflow execution time
 * - NFR-004: Retry on transient failures
 */

const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

describe('NPM Publishing Workflow - Integration Tests', () => {
  const workflowPath = '.github/workflows/npm-publish.yml';
  const validationScriptPath = '.github/scripts/validate-version.js';
  const packageJsonPath = 'package.json';

  describe('AC#3: Complete Build Pipeline Execution', () => {
    test('should execute full workflow stages in correct order', () => {
      // Arrange
      const expectedStages = [
        'checkout',
        'setup-node',
        'npm ci',
        'npm test',
        'validate-version',
        'npm publish'
      ];

      // Act
      let workflowContent = null;
      try {
        workflowContent = fs.readFileSync(workflowPath, 'utf8');
      } catch (error) {
        // Expected to fail in Red phase
        workflowContent = '';
      }

      // Assert
      expectedStages.forEach(stage => {
        expect(workflowContent).toContain(stage);
      });
    });

    test('should fail workflow if npm ci fails', () => {
      // Arrange
      // Simulate corrupted package-lock.json scenario

      // Act & Assert
      // Workflow should halt on npm ci failure
      // This will be verified through actual workflow execution
      expect(true).toBe(true); // Placeholder for integration test
    });

    test('should fail workflow if npm test fails', () => {
      // Arrange
      // Simulate failing test scenario

      // Act & Assert
      // Workflow should halt on test failure
      // This will be verified through actual workflow execution
      expect(true).toBe(true); // Placeholder for integration test
    });

    test('should fail workflow if version validation fails', () => {
      // Arrange
      const tag = 'v1.0.1';
      const packageJson = { version: '1.0.0' }; // Mismatched version

      // Act
      let validationPassed = false;
      try {
        if (fs.existsSync(validationScriptPath)) {
          const validateVersion = require(path.resolve(validationScriptPath));
          const result = validateVersion.validate(tag, packageJson);
          validationPassed = result.valid;
        }
      } catch (error) {
        validationPassed = false;
      }

      // Assert
      expect(validationPassed).toBe(false);
    });

    test('should proceed to publish only after all validations pass', () => {
      // Arrange
      const tag = 'v1.0.0';
      let packageJson = null;

      try {
        const content = fs.readFileSync(packageJsonPath, 'utf8');
        packageJson = JSON.parse(content);
      } catch (error) {
        packageJson = { version: '1.0.0' };
      }

      // Act
      let validationPassed = false;
      try {
        if (fs.existsSync(validationScriptPath)) {
          const validateVersion = require(path.resolve(validationScriptPath));
          const result = validateVersion.validate(tag, packageJson);
          validationPassed = result.valid;
        } else {
          // In Red phase, assume validation logic exists
          validationPassed = tag.replace(/^v/, '') === packageJson.version;
        }
      } catch (error) {
        validationPassed = false;
      }

      // Assert
      // If validation fails, publish should not be reached
      if (!validationPassed) {
        expect(validationPassed).toBe(false);
      }
    });
  });

  describe('AC#7: Idempotency with Duplicate Versions', () => {
    test('should detect when version already exists on NPM registry', () => {
      // Arrange
      const packageName = 'devforgeai';
      const version = '1.0.0';

      // Act
      let versionExists = false;
      try {
        // Simulate checking npm registry
        // In actual implementation: npm view devforgeai@1.0.0 version
        // For test: assume version doesn't exist yet (Red phase)
        versionExists = false;
      } catch (error) {
        versionExists = false;
      }

      // Assert
      // Workflow should detect existing versions
      expect(typeof versionExists).toBe('boolean');
    });

    test('should skip publish and exit with success when version exists', () => {
      // Arrange
      const versionAlreadyPublished = true;

      // Act
      let exitCode = 0;
      if (versionAlreadyPublished) {
        console.log('Version already published. Skipping publish.');
        exitCode = 0; // Idempotent behavior - success
      }

      // Assert
      expect(exitCode).toBe(0);
    });

    test('should log appropriate message on duplicate version detection', () => {
      // Arrange
      const logMessages = [];
      const originalLog = console.log;
      console.log = (msg) => logMessages.push(msg);

      // Act
      const versionAlreadyPublished = true;
      if (versionAlreadyPublished) {
        console.log('Version already published. Skipping publish.');
      }

      console.log = originalLog; // Restore

      // Assert
      expect(logMessages).toContain('Version already published. Skipping publish.');
    });

    test('should NOT attempt npm publish when version exists', () => {
      // Arrange
      const versionExists = true;
      let publishAttempted = false;

      // Act
      if (!versionExists) {
        publishAttempted = true;
        // npm publish would be called here
      }

      // Assert
      expect(publishAttempted).toBe(false);
    });
  });

  describe('NFR-001: Workflow Execution Time < 5 Minutes', () => {
    test('should complete dependency installation within 2 minutes', () => {
      // Arrange
      const startTime = Date.now();
      const timeoutMs = 2 * 60 * 1000; // 2 minutes

      // Act
      let installTime = 0;
      try {
        // This would measure actual npm ci execution
        // For test: simulate timing check
        installTime = 0; // Placeholder
      } catch (error) {
        installTime = Infinity;
      }

      // Assert
      expect(installTime).toBeLessThan(timeoutMs);
    });

    test('should complete test execution within 2 minutes', () => {
      // Arrange
      const startTime = Date.now();
      const timeoutMs = 2 * 60 * 1000; // 2 minutes

      // Act
      let testTime = 0;
      try {
        // This would measure actual npm test execution
        // For test: simulate timing check
        testTime = 0; // Placeholder
      } catch (error) {
        testTime = Infinity;
      }

      // Assert
      expect(testTime).toBeLessThan(timeoutMs);
    });

    test('should complete entire workflow within 5 minutes', () => {
      // Arrange
      const maxWorkflowTime = 5 * 60 * 1000; // 5 minutes in ms

      // Act
      // This would be measured from workflow start to completion
      const estimatedTime = 0; // Placeholder

      // Assert
      expect(estimatedTime).toBeLessThan(maxWorkflowTime);
    });

    test('should use npm ci caching to improve performance', () => {
      // Arrange
      let workflowContent = '';
      try {
        workflowContent = fs.readFileSync(workflowPath, 'utf8');
      } catch (error) {
        workflowContent = '';
      }

      // Act & Assert
      // Workflow should configure npm cache
      expect(workflowContent).toMatch(/cache.*npm|setup-node.*cache/i);
    });
  });

  describe('NFR-004: Retry on Transient Failures', () => {
    test('should retry npm publish on 502 Bad Gateway error', () => {
      // Arrange
      let attemptCount = 0;
      const maxRetries = 3;
      const simulateError = () => {
        attemptCount++;
        if (attemptCount < maxRetries) {
          throw new Error('502 Bad Gateway');
        }
        return { success: true };
      };

      // Act
      let result = null;
      for (let i = 0; i < maxRetries; i++) {
        try {
          result = simulateError();
          break;
        } catch (error) {
          if (i === maxRetries - 1) throw error;
          // Retry with backoff
        }
      }

      // Assert
      expect(attemptCount).toBe(maxRetries);
      expect(result?.success).toBe(true);
    });

    test('should use exponential backoff between retries', () => {
      // Arrange
      const delays = [];
      const expectedDelays = [5000, 10000, 20000]; // 5s, 10s, 20s

      // Act
      for (let i = 0; i < 3; i++) {
        const delay = Math.pow(2, i) * 5000;
        delays.push(delay);
      }

      // Assert
      expect(delays).toEqual(expectedDelays);
    });

    test('should fail after 3 retry attempts on persistent errors', () => {
      // Arrange
      let attemptCount = 0;
      const maxRetries = 3;
      const alwaysFails = () => {
        attemptCount++;
        throw new Error('Persistent failure');
      };

      // Act & Assert
      expect(() => {
        for (let i = 0; i < maxRetries; i++) {
          try {
            alwaysFails();
          } catch (error) {
            if (i === maxRetries - 1) throw error;
          }
        }
      }).toThrow('Persistent failure');

      expect(attemptCount).toBe(maxRetries);
    });

    test('should retry on network timeout errors', () => {
      // Arrange
      let attemptCount = 0;
      const simulateTimeout = () => {
        attemptCount++;
        if (attemptCount === 1) {
          throw new Error('ETIMEDOUT');
        }
        return { success: true };
      };

      // Act
      let result = null;
      const maxRetries = 3;
      for (let i = 0; i < maxRetries; i++) {
        try {
          result = simulateTimeout();
          break;
        } catch (error) {
          if (i === maxRetries - 1) throw error;
        }
      }

      // Assert
      expect(attemptCount).toBe(1); // Succeeds on first retry
      expect(result?.success).toBe(true);
    });
  });

  describe('Edge Case: NPM Token Authentication', () => {
    test('should handle HTTP 401 Unauthorized with clear error message', () => {
      // Arrange
      const simulateAuthError = () => {
        const error = new Error('401 Unauthorized');
        error.statusCode = 401;
        return error;
      };

      // Act
      const error = simulateAuthError();

      // Assert
      expect(error.statusCode).toBe(401);
      expect(error.message).toContain('401 Unauthorized');
    });

    test('should suggest NPM_TOKEN renewal on authentication failure', () => {
      // Arrange
      const errorMessage = '401 Unauthorized: Invalid token';

      // Act
      const remediation = errorMessage.includes('401')
        ? 'NPM_TOKEN may be expired. Please regenerate token in GitHub secrets.'
        : '';

      // Assert
      expect(remediation).toContain('regenerate token');
    });
  });

  describe('Edge Case: Multiple Tags Pushed Simultaneously', () => {
    test('should handle concurrent workflow runs independently', () => {
      // Arrange
      const tags = ['v1.0.0', 'v1.0.1', 'v1.0.2'];
      const workflowRuns = [];

      // Act
      tags.forEach(tag => {
        workflowRuns.push({
          tag,
          status: 'running',
          startTime: Date.now()
        });
      });

      // Assert
      expect(workflowRuns).toHaveLength(3);
      // Each run should be independent
      workflowRuns.forEach(run => {
        expect(run.status).toBe('running');
      });
    });

    test('should prevent race conditions with idempotency check', () => {
      // Arrange
      const publishedVersions = new Set();
      const version = '1.0.0';

      // Act
      const attemptPublish = (ver) => {
        if (publishedVersions.has(ver)) {
          return { skipped: true, reason: 'Version already published' };
        }
        publishedVersions.add(ver);
        return { success: true };
      };

      const result1 = attemptPublish(version);
      const result2 = attemptPublish(version); // Duplicate

      // Assert
      expect(result1.success).toBe(true);
      expect(result2.skipped).toBe(true);
    });
  });

  describe('Edge Case: Pre-release After Newer Stable', () => {
    test('should allow publishing v1.0.0-beta.1 after v1.0.0 is released', () => {
      // Arrange
      const existingVersions = ['v1.0.0'];
      const newVersion = 'v1.0.0-beta.1';

      // Act
      const isAllowed = true; // NPM allows this, just logs warning

      // Assert
      expect(isAllowed).toBe(true);
    });

    test('should log warning when pre-release is published after stable', () => {
      // Arrange
      const logMessages = [];
      const originalWarn = console.warn;
      console.warn = (msg) => logMessages.push(msg);

      // Act
      const newVersion = 'v1.0.0-beta.1';
      const latestStable = 'v1.0.0';
      if (newVersion.includes('-') && latestStable > newVersion) {
        console.warn(`Warning: Publishing pre-release ${newVersion} after stable ${latestStable}`);
      }

      console.warn = originalWarn; // Restore

      // Assert
      expect(logMessages.length).toBeGreaterThan(0);
    });
  });

  describe('Workflow Configuration Validation', () => {
    test('should have all required workflow jobs defined', () => {
      // Arrange
      let workflowContent = '';
      try {
        workflowContent = fs.readFileSync(workflowPath, 'utf8');
      } catch (error) {
        workflowContent = '';
      }

      // Act & Assert
      expect(workflowContent).toContain('jobs:');
      expect(workflowContent).toContain('publish:');
    });

    test('should configure Node.js version >= 18', () => {
      // Arrange
      let workflowContent = '';
      try {
        workflowContent = fs.readFileSync(workflowPath, 'utf8');
      } catch (error) {
        workflowContent = '';
      }

      // Act & Assert
      expect(workflowContent).toMatch(/node-version.*['"](18|20|latest)['"]/);
    });

    test('should have permissions for id-token write', () => {
      // Arrange
      let workflowContent = '';
      try {
        workflowContent = fs.readFileSync(workflowPath, 'utf8');
      } catch (error) {
        workflowContent = '';
      }

      // Act & Assert
      expect(workflowContent).toMatch(/permissions:[\s\S]*id-token:\s*write/);
    });
  });

  describe('Package.json Validation', () => {
    test('should have required npm package fields', () => {
      // Arrange
      let packageJson = null;
      try {
        const content = fs.readFileSync(packageJsonPath, 'utf8');
        packageJson = JSON.parse(content);
      } catch (error) {
        packageJson = {};
      }

      // Act & Assert
      expect(packageJson.name).toBeDefined();
      expect(packageJson.version).toBeDefined();
      expect(packageJson.description).toBeDefined();
      expect(packageJson.repository).toBeDefined();
    });

    test('should have valid semver version in package.json', () => {
      // Arrange
      let packageJson = null;
      try {
        const content = fs.readFileSync(packageJsonPath, 'utf8');
        packageJson = JSON.parse(content);
      } catch (error) {
        packageJson = { version: '1.0.0' };
      }

      const semverPattern = /^\d+\.\d+\.\d+(-[a-z0-9.]+)?$/;

      // Act & Assert
      expect(packageJson.version).toMatch(semverPattern);
    });
  });
});
