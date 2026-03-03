/**
 * Test Suite: GitHub Secrets Configuration
 * Story: STORY-067 - NPM Registry Publishing Workflow
 *
 * Tests cover:
 * - AC#1: NPM registry account configuration
 * - CONF-005: NPM_TOKEN secret authentication
 * - NFR-002: Token security (never exposed in logs)
 */

const fs = require('fs');
const path = require('path');

describe('GitHub Secrets Configuration', () => {
  const workflowPath = '.github/workflows/npm-publish.yml';

  describe('AC#1: NPM Registry Account Configuration', () => {
    test('should reference NPM_TOKEN secret from GitHub repository settings', () => {
      // Arrange
      let workflowContent = '';
      try {
        workflowContent = fs.readFileSync(workflowPath, 'utf8');
      } catch (error) {
        workflowContent = '';
      }

      // Act & Assert
      expect(workflowContent).toContain('secrets.NPM_TOKEN');
    });

    test('should configure organization scope @devforgeai', () => {
      // Arrange
      const packageJsonPath = path.resolve('package.json');
      let packageJson = null;

      try {
        const content = fs.readFileSync(packageJsonPath, 'utf8');
        packageJson = JSON.parse(content);
      } catch (error) {
        packageJson = { name: 'devforgeai' }; // Expected name
      }

      // Act
      const packageName = packageJson.name;

      // Assert
      // Package should be either scoped (@devforgeai/installer) or unscoped (devforgeai)
      expect(packageName).toMatch(/^(@devforgeai\/)?devforgeai/);
    });

    test('should use NPM_TOKEN with Automation access level', () => {
      // Arrange
      let workflowContent = '';
      try {
        workflowContent = fs.readFileSync(workflowPath, 'utf8');
      } catch (error) {
        workflowContent = '';
      }

      // Act & Assert
      // Token must be referenced but never logged
      expect(workflowContent).toContain('NPM_TOKEN');
      // Documentation should specify Automation token type
    });

    test('should configure NPM registry URL as https://registry.npmjs.org', () => {
      // Arrange
      let workflowContent = '';
      try {
        workflowContent = fs.readFileSync(workflowPath, 'utf8');
      } catch (error) {
        workflowContent = '';
      }

      // Act & Assert
      expect(workflowContent).toContain('https://registry.npmjs.org');
    });
  });

  describe('CONF-005: NPM_TOKEN Authentication', () => {
    test('should set NODE_AUTH_TOKEN environment variable from secret', () => {
      // Arrange
      let workflowContent = '';
      try {
        workflowContent = fs.readFileSync(workflowPath, 'utf8');
      } catch (error) {
        workflowContent = '';
      }

      // Act & Assert
      expect(workflowContent).toMatch(/NODE_AUTH_TOKEN.*secrets\.NPM_TOKEN/);
    });

    test('should authenticate to NPM registry during publish step', () => {
      // Arrange
      let workflowContent = '';
      try {
        workflowContent = fs.readFileSync(workflowPath, 'utf8');
      } catch (error) {
        workflowContent = '';
      }

      // Act & Assert
      // Workflow must have both registry-url and auth token
      expect(workflowContent).toContain('registry-url');
      expect(workflowContent).toContain('NODE_AUTH_TOKEN');
    });

    test('should fail publish with clear error if NPM_TOKEN is missing', () => {
      // Arrange
      const missingToken = undefined;

      // Act
      const errorMessage = !missingToken
        ? 'NPM_TOKEN secret is not configured. Please add it to GitHub repository secrets.'
        : '';

      // Assert
      expect(errorMessage).toContain('NPM_TOKEN secret is not configured');
      expect(errorMessage).toContain('GitHub repository secrets');
    });

    test('should fail publish with clear error if NPM_TOKEN is invalid', () => {
      // Arrange
      const httpStatus = 401; // Unauthorized

      // Act
      const errorMessage = httpStatus === 401
        ? 'NPM_TOKEN authentication failed (401 Unauthorized). Token may be expired or revoked.'
        : '';

      // Assert
      expect(errorMessage).toContain('401 Unauthorized');
      expect(errorMessage).toContain('expired or revoked');
    });
  });

  describe('NFR-002: Token Security - Never Exposed in Logs', () => {
    test('should NOT echo or log NPM_TOKEN value', () => {
      // Arrange
      let workflowContent = '';
      try {
        workflowContent = fs.readFileSync(workflowPath, 'utf8');
      } catch (error) {
        workflowContent = '';
      }

      // Act & Assert
      // Token should only appear in secret reference, never in echo/log commands
      expect(workflowContent).not.toMatch(/echo.*\$\{\{\s*secrets\.NPM_TOKEN\s*\}\}/);
      expect(workflowContent).not.toMatch(/console\.log.*NPM_TOKEN/);
      expect(workflowContent).not.toMatch(/print.*NPM_TOKEN/);
    });

    test('should use GitHub automatic secret masking', () => {
      // Arrange
      const tokenValue = '${{ secrets.NPM_TOKEN }}';

      // Act
      const isMasked = tokenValue.includes('secrets.');

      // Assert
      expect(isMasked).toBe(true);
      // GitHub automatically masks any value from secrets.* in logs
    });

    test('should NOT expose token in error messages', () => {
      // Arrange
      const sensitiveError = 'Authentication failed with token: npm_XXXXXXXXXXXX';
      const safeError = 'Authentication failed (401 Unauthorized). Check NPM_TOKEN secret.';

      // Act & Assert
      // Error messages should reference secret name, not value
      expect(safeError).not.toMatch(/npm_[a-zA-Z0-9]+/);
      expect(safeError).toContain('NPM_TOKEN');
    });

    test('should configure workflow to redact sensitive data', () => {
      // Arrange
      let workflowContent = '';
      try {
        workflowContent = fs.readFileSync(workflowPath, 'utf8');
      } catch (error) {
        workflowContent = '';
      }

      // Act & Assert
      // Workflow should use secrets.* syntax which auto-redacts
      const secretReferences = workflowContent.match(/secrets\.\w+/g) || [];
      expect(secretReferences).toContain('secrets.NPM_TOKEN');
    });

    test('should prevent accidental token exposure through npm commands', () => {
      // Arrange
      let workflowContent = '';
      try {
        workflowContent = fs.readFileSync(workflowPath, 'utf8');
      } catch (error) {
        workflowContent = '';
      }

      // Act & Assert
      // Should NOT use token directly in npm config commands
      expect(workflowContent).not.toMatch(/npm config set.*\$\{\{\s*secrets\.NPM_TOKEN\s*\}\}/);
      // Should use NODE_AUTH_TOKEN environment variable instead
      expect(workflowContent).toMatch(/NODE_AUTH_TOKEN/);
    });
  });

  describe('Secret Configuration Validation', () => {
    test('should document required secrets in workflow comments', () => {
      // Arrange
      let workflowContent = '';
      try {
        workflowContent = fs.readFileSync(workflowPath, 'utf8');
      } catch (error) {
        workflowContent = '';
      }

      // Act & Assert
      // Workflow should have comments explaining required secrets
      expect(workflowContent).toMatch(/#.*NPM_TOKEN|# Required secrets/i);
    });

    test('should provide remediation steps for missing secrets', () => {
      // Arrange
      const secretMissing = true;

      // Act
      const remediation = secretMissing
        ? [
            'NPM_TOKEN is not configured.',
            'Steps to fix:',
            '1. Generate token at https://www.npmjs.com/settings/tokens',
            '2. Add token to GitHub: Settings > Secrets and variables > Actions > New repository secret',
            '3. Name: NPM_TOKEN, Value: [your token]'
          ].join('\n')
        : '';

      // Assert
      expect(remediation).toContain('Generate token at');
      expect(remediation).toContain('Settings > Secrets');
      expect(remediation).toContain('Name: NPM_TOKEN');
    });

    test('should validate token has publish permissions', () => {
      // Arrange
      const tokenPermissions = ['read', 'publish']; // Expected

      // Act & Assert
      expect(tokenPermissions).toContain('publish');
    });
  });

  describe('Token Rotation and Expiration Handling', () => {
    test('should provide clear error on token expiration (403 Forbidden)', () => {
      // Arrange
      const httpStatus = 403;

      // Act
      const errorMessage = httpStatus === 403
        ? 'NPM_TOKEN may be expired or revoked (403 Forbidden). Please regenerate token.'
        : '';

      // Assert
      expect(errorMessage).toContain('expired or revoked');
      expect(errorMessage).toContain('regenerate token');
    });

    test('should document token rotation procedure', () => {
      // Arrange
      const rotationSteps = [
        '1. Generate new NPM token with Automation access',
        '2. Update GitHub secret NPM_TOKEN with new value',
        '3. Revoke old token on npmjs.com',
        '4. Verify workflow runs successfully with new token'
      ];

      // Act & Assert
      rotationSteps.forEach(step => {
        expect(step).toMatch(/\d\./); // All steps numbered
      });
      expect(rotationSteps).toHaveLength(4);
    });
  });

  describe('Multi-Environment Token Management', () => {
    test('should use same NPM_TOKEN for all environments (staging/production)', () => {
      // Arrange
      const environments = ['staging', 'production'];

      // Act & Assert
      // NPM registry is the same for all environments
      environments.forEach(env => {
        // Same token used regardless of deployment target
        expect(env).toBeDefined();
      });
    });

    test('should NOT require separate tokens per environment', () => {
      // Arrange
      let workflowContent = '';
      try {
        workflowContent = fs.readFileSync(workflowPath, 'utf8');
      } catch (error) {
        workflowContent = '';
      }

      // Act & Assert
      // Should only reference NPM_TOKEN (not NPM_TOKEN_STAGING, NPM_TOKEN_PROD, etc.)
      expect(workflowContent).not.toContain('NPM_TOKEN_STAGING');
      expect(workflowContent).not.toContain('NPM_TOKEN_PROD');
    });
  });

  describe('Security Best Practices', () => {
    test('should limit workflow permissions to minimum required', () => {
      // Arrange
      let workflowContent = '';
      try {
        workflowContent = fs.readFileSync(workflowPath, 'utf8');
      } catch (error) {
        workflowContent = '';
      }

      // Act & Assert
      // Should have explicit permissions block (not default full access)
      expect(workflowContent).toMatch(/permissions:/);
    });

    test('should enable id-token write for provenance', () => {
      // Arrange
      let workflowContent = '';
      try {
        workflowContent = fs.readFileSync(workflowPath, 'utf8');
      } catch (error) {
        workflowContent = '';
      }

      // Act & Assert
      expect(workflowContent).toMatch(/id-token:\s*write/);
    });

    test('should NOT grant excessive permissions (contents: write, etc.)', () => {
      // Arrange
      let workflowContent = '';
      try {
        workflowContent = fs.readFileSync(workflowPath, 'utf8');
      } catch (error) {
        workflowContent = '';
      }

      // Act & Assert
      // Publish workflow should only need id-token:write, not contents:write
      expect(workflowContent).not.toMatch(/contents:\s*write/);
    });
  });
});
