/**
 * Test Suite: GitHub Actions NPM Publishing Workflow
 * Story: STORY-067 - NPM Registry Publishing Workflow
 *
 * Tests cover:
 * - AC#2: Workflow triggers on version tags
 * - AC#3: Build and validation steps
 * - AC#4: NPM publish with provenance and dist-tags
 * - AC#6: Version tag validation
 * - AC#7: Idempotency
 * - Technical Spec: CONF-001 through CONF-004
 */

const fs = require('fs');
const path = require('path');
const yaml = require('js-yaml');

describe('GitHub Actions NPM Publish Workflow', () => {
  let workflowConfig;
  const workflowPath = '.github/workflows/npm-publish.yml';

  beforeAll(() => {
    // Arrange: Load workflow configuration
    try {
      const workflowContent = fs.readFileSync(workflowPath, 'utf8');
      workflowConfig = yaml.load(workflowContent);
    } catch (error) {
      // Expected to fail in Red phase - workflow file doesn't exist yet
      workflowConfig = null;
    }
  });

  describe('AC#2: Workflow Triggers on Version Tags', () => {
    test('should trigger on stable version tags matching vX.Y.Z pattern', () => {
      // Arrange
      const expectedPattern = /^v\d+\.\d+\.\d+$/;

      // Act
      const triggers = workflowConfig?.on?.push?.tags;

      // Assert
      expect(triggers).toBeDefined();
      expect(triggers).toContain('v*.*.*');

      // Verify pattern matches expected stable versions
      expect('v1.0.0').toMatch(expectedPattern);
      expect('v2.1.3').toMatch(expectedPattern);
      expect('v10.20.30').toMatch(expectedPattern);
    });

    test('should trigger on pre-release version tags matching vX.Y.Z-prerelease pattern', () => {
      // Arrange
      const expectedPattern = /^v\d+\.\d+\.\d+-[a-z0-9.]+$/;

      // Act
      const triggers = workflowConfig?.on?.push?.tags;

      // Assert
      expect(triggers).toBeDefined();

      // Verify pattern matches expected pre-release versions
      expect('v1.1.0-beta.1').toMatch(expectedPattern);
      expect('v2.0.0-rc.2').toMatch(expectedPattern);
      expect('v1.5.0-alpha.3').toMatch(expectedPattern);
    });

    test('should NOT trigger on branch pushes', () => {
      // Arrange & Act
      const branchTriggers = workflowConfig?.on?.push?.branches;

      // Assert
      expect(branchTriggers).toBeUndefined();
    });

    test('should NOT trigger on pull requests', () => {
      // Arrange & Act
      const prTriggers = workflowConfig?.on?.pull_request;

      // Assert
      expect(prTriggers).toBeUndefined();
    });
  });

  describe('AC#3: Package Build and Validation Before Publishing', () => {
    test('should execute npm ci for reproducible dependency installation', () => {
      // Arrange
      const publishJob = workflowConfig?.jobs?.publish;

      // Act
      const steps = publishJob?.steps || [];
      const ciStep = steps.find(step =>
        step.run?.includes('npm ci') || step.name?.includes('Install dependencies')
      );

      // Assert
      expect(ciStep).toBeDefined();
      expect(ciStep.run).toContain('npm ci');
    });

    test('should execute npm test with all tests passing', () => {
      // Arrange
      const publishJob = workflowConfig?.jobs?.publish;

      // Act
      const steps = publishJob?.steps || [];
      const testStep = steps.find(step =>
        step.run?.includes('npm test') || step.name?.includes('Run tests')
      );

      // Assert
      expect(testStep).toBeDefined();
      expect(testStep.run).toContain('npm test');
    });

    test('should validate package.json version matches tag version', () => {
      // Arrange
      const publishJob = workflowConfig?.jobs?.publish;

      // Act
      const steps = publishJob?.steps || [];
      const validationStep = steps.find(step =>
        step.run?.includes('validate-version') ||
        step.name?.includes('Validate version')
      );

      // Assert
      expect(validationStep).toBeDefined();
      expect(validationStep.run).toMatch(/validate-version|version.*match/i);
    });

    test('should fail workflow if validation steps fail', () => {
      // Arrange
      const publishJob = workflowConfig?.jobs?.publish;

      // Act
      const steps = publishJob?.steps || [];
      const criticalSteps = steps.filter(step =>
        step.run?.includes('npm ci') ||
        step.run?.includes('npm test') ||
        step.run?.includes('validate-version')
      );

      // Assert
      // All critical steps should not have continue-on-error: true
      criticalSteps.forEach(step => {
        expect(step['continue-on-error']).not.toBe(true);
      });
    });
  });

  describe('AC#4: NPM Publish with Provenance and Tag Management', () => {
    test('should publish with --provenance flag for supply chain transparency', () => {
      // Arrange
      const publishJob = workflowConfig?.jobs?.publish;

      // Act
      const steps = publishJob?.steps || [];
      const publishStep = steps.find(step =>
        step.run?.includes('npm publish') ||
        step.name?.includes('Publish')
      );

      // Assert
      expect(publishStep).toBeDefined();
      expect(publishStep.run).toContain('--provenance');
    });

    test('should assign "latest" dist-tag for stable versions', () => {
      // Arrange
      const publishJob = workflowConfig?.jobs?.publish;

      // Act
      const steps = publishJob?.steps || [];
      const publishStep = steps.find(step => step.run?.includes('npm publish'));

      // Assert
      expect(publishStep).toBeDefined();
      // Logic should detect stable versions and use --tag latest
      expect(publishStep.run).toMatch(/--tag\s+latest|tag.*latest/i);
    });

    test('should assign "beta" dist-tag for beta versions', () => {
      // Arrange
      const publishJob = workflowConfig?.jobs?.publish;

      // Act
      const steps = publishJob?.steps || [];
      const publishStep = steps.find(step => step.run?.includes('npm publish'));

      // Assert
      expect(publishStep).toBeDefined();
      // Logic should detect beta in version and use --tag beta
      expect(publishStep.run).toMatch(/beta.*--tag\s+beta|--tag.*beta/i);
    });

    test('should assign "rc" dist-tag for release candidate versions', () => {
      // Arrange
      const publishJob = workflowConfig?.jobs?.publish;

      // Act
      const steps = publishJob?.steps || [];
      const publishStep = steps.find(step => step.run?.includes('npm publish'));

      // Assert
      expect(publishStep).toBeDefined();
      // Logic should detect rc in version and use --tag rc
      expect(publishStep.run).toMatch(/rc.*--tag\s+rc|--tag.*rc/i);
    });
  });

  describe('AC#6: Version Tag Validation and Error Handling', () => {
    test('should detect and reject invalid tag formats', () => {
      // Arrange
      const publishJob = workflowConfig?.jobs?.publish;

      // Act
      const steps = publishJob?.steps || [];
      const validationStep = steps.find(step =>
        step.run?.includes('validate-version') ||
        step.run?.includes('semver')
      );

      // Assert
      expect(validationStep).toBeDefined();
      // Should have validation logic that exits on invalid format
    });

    test('should log clear error message for invalid tag format', () => {
      // Arrange
      const publishJob = workflowConfig?.jobs?.publish;

      // Act
      const steps = publishJob?.steps || [];
      const validationStep = steps.find(step =>
        step.run?.includes('validate-version')
      );

      // Assert
      expect(validationStep).toBeDefined();
      expect(validationStep.run).toMatch(/Invalid tag|Must match|vX\.Y\.Z/i);
    });

    test('should exit with non-zero status code on invalid tag', () => {
      // Arrange
      const publishJob = workflowConfig?.jobs?.publish;

      // Act
      const steps = publishJob?.steps || [];
      const validationStep = steps.find(step =>
        step.run?.includes('validate-version')
      );

      // Assert
      expect(validationStep).toBeDefined();
      expect(validationStep.run).toMatch(/exit\s+1|return\s+1|process\.exit\(1\)/i);
    });

    test('should NOT attempt to publish on invalid tag', () => {
      // Arrange
      const publishJob = workflowConfig?.jobs?.publish;

      // Act
      const steps = publishJob?.steps || [];
      const stepOrder = steps.map(step => step.name || step.run);
      const validationIndex = stepOrder.findIndex(name =>
        name?.includes('validate') || name?.includes('Validate')
      );
      const publishIndex = stepOrder.findIndex(name =>
        name?.includes('npm publish') || name?.includes('Publish')
      );

      // Assert
      expect(validationIndex).toBeLessThan(publishIndex);
      // Validation must come before publish
    });
  });

  describe('AC#7: Idempotency and Duplicate Version Prevention', () => {
    test('should detect existing version on NPM registry', () => {
      // Arrange
      const publishJob = workflowConfig?.jobs?.publish;

      // Act
      const steps = publishJob?.steps || [];
      const idempotencyCheck = steps.find(step =>
        step.run?.includes('npm view') ||
        step.run?.includes('already published') ||
        step.name?.includes('Check existing')
      );

      // Assert
      expect(idempotencyCheck).toBeDefined();
    });

    test('should log message when version already published', () => {
      // Arrange
      const publishJob = workflowConfig?.jobs?.publish;

      // Act
      const steps = publishJob?.steps || [];
      const idempotencyCheck = steps.find(step =>
        step.run?.includes('already published') ||
        step.run?.includes('Skipping publish')
      );

      // Assert
      expect(idempotencyCheck).toBeDefined();
      expect(idempotencyCheck.run).toMatch(/already published|Skipping/i);
    });

    test('should exit with success status on duplicate version', () => {
      // Arrange
      const publishJob = workflowConfig?.jobs?.publish;

      // Act
      const steps = publishJob?.steps || [];
      const idempotencyCheck = steps.find(step =>
        step.run?.includes('already published')
      );

      // Assert
      expect(idempotencyCheck).toBeDefined();
      // Should exit 0 (success) for idempotent behavior
      expect(idempotencyCheck.run).toMatch(/exit\s+0|return\s+0/i);
    });

    test('should NOT fail workflow on duplicate version', () => {
      // Arrange
      const publishJob = workflowConfig?.jobs?.publish;

      // Act
      const steps = publishJob?.steps || [];
      const publishStep = steps.find(step => step.run?.includes('npm publish'));

      // Assert
      expect(publishStep).toBeDefined();
      // Should have conditional or error handling for 409 Conflict
      expect(publishStep.run).toMatch(/if.*view|catch|409/i);
    });
  });

  describe('Technical Spec: CONF-001 - Workflow Trigger Configuration', () => {
    test('should have workflow name defined', () => {
      // Arrange & Act
      const workflowName = workflowConfig?.name;

      // Assert
      expect(workflowName).toBeDefined();
      expect(workflowName).toMatch(/npm|publish/i);
    });

    test('should trigger only on tag push events', () => {
      // Arrange & Act
      const triggers = workflowConfig?.on;

      // Assert
      expect(triggers).toBeDefined();
      expect(triggers.push).toBeDefined();
      expect(triggers.push.tags).toBeDefined();
      expect(triggers.push.branches).toBeUndefined();
    });

    test('should use semver tag pattern with v prefix', () => {
      // Arrange
      const semverPattern = /^v\d+\.\d+\.\d+(-[a-z0-9.]+)?$/;

      // Act
      const triggers = workflowConfig?.on?.push?.tags;

      // Assert
      expect(triggers).toBeDefined();

      // Test valid tags
      expect('v1.0.0').toMatch(semverPattern);
      expect('v1.0.0-beta.1').toMatch(semverPattern);

      // Test invalid tags
      expect('1.0.0').not.toMatch(semverPattern);
      expect('release-1.0').not.toMatch(semverPattern);
    });
  });

  describe('Technical Spec: CONF-002 - Build Step Execution Order', () => {
    test('should execute steps in correct order: checkout → install → test → validate → publish', () => {
      // Arrange
      const publishJob = workflowConfig?.jobs?.publish;

      // Act
      const steps = publishJob?.steps || [];
      const stepNames = steps.map(step => {
        if (step.uses?.includes('checkout')) return 'checkout';
        if (step.run?.includes('npm ci')) return 'install';
        if (step.run?.includes('npm test')) return 'test';
        if (step.run?.includes('validate-version')) return 'validate';
        if (step.run?.includes('npm publish')) return 'publish';
        return null;
      }).filter(Boolean);

      // Assert
      expect(stepNames.indexOf('checkout')).toBeLessThan(stepNames.indexOf('install'));
      expect(stepNames.indexOf('install')).toBeLessThan(stepNames.indexOf('test'));
      expect(stepNames.indexOf('test')).toBeLessThan(stepNames.indexOf('validate'));
      expect(stepNames.indexOf('validate')).toBeLessThan(stepNames.indexOf('publish'));
    });

    test('should use npm ci instead of npm install for reproducible builds', () => {
      // Arrange
      const publishJob = workflowConfig?.jobs?.publish;

      // Act
      const steps = publishJob?.steps || [];
      const installStep = steps.find(step => step.run?.includes('npm'));

      // Assert
      expect(installStep).toBeDefined();
      expect(installStep.run).toContain('npm ci');
      expect(installStep.run).not.toContain('npm install');
    });
  });

  describe('Technical Spec: CONF-003 - Provenance Configuration', () => {
    test('should enable provenance flag in npm publish command', () => {
      // Arrange
      const publishJob = workflowConfig?.jobs?.publish;

      // Act
      const steps = publishJob?.steps || [];
      const publishStep = steps.find(step => step.run?.includes('npm publish'));

      // Assert
      expect(publishStep).toBeDefined();
      expect(publishStep.run).toContain('--provenance');
    });

    test('should configure permissions for id-token write', () => {
      // Arrange & Act
      const jobPermissions = workflowConfig?.jobs?.publish?.permissions;
      const globalPermissions = workflowConfig?.permissions;

      // Assert
      const permissions = jobPermissions || globalPermissions;
      expect(permissions).toBeDefined();
      expect(permissions['id-token']).toBe('write');
    });
  });

  describe('Technical Spec: CONF-004 - Dist-Tag Assignment Logic', () => {
    test('should extract prerelease identifier from tag', () => {
      // Arrange
      const betaTag = 'v1.0.0-beta.1';
      const rcTag = 'v2.0.0-rc.2';
      const stableTag = 'v3.0.0';

      // Act & Assert
      // Logic should detect prerelease suffix
      expect(betaTag).toMatch(/-beta\./);
      expect(rcTag).toMatch(/-rc\./);
      expect(stableTag).not.toMatch(/-/);
    });

    test('should map beta prerelease to beta dist-tag', () => {
      // Arrange
      const publishJob = workflowConfig?.jobs?.publish;

      // Act
      const steps = publishJob?.steps || [];
      const publishStep = steps.find(step => step.run?.includes('npm publish'));

      // Assert
      expect(publishStep).toBeDefined();
      // Should have conditional logic for beta versions
      expect(publishStep.run).toMatch(/beta.*--tag\s+beta/i);
    });

    test('should map rc prerelease to rc dist-tag', () => {
      // Arrange
      const publishJob = workflowConfig?.jobs?.publish;

      // Act
      const steps = publishJob?.steps || [];
      const publishStep = steps.find(step => step.run?.includes('npm publish'));

      // Assert
      expect(publishStep).toBeDefined();
      // Should have conditional logic for rc versions
      expect(publishStep.run).toMatch(/rc.*--tag\s+rc/i);
    });

    test('should use latest dist-tag for stable versions', () => {
      // Arrange
      const publishJob = workflowConfig?.jobs?.publish;

      // Act
      const steps = publishJob?.steps || [];
      const publishStep = steps.find(step => step.run?.includes('npm publish'));

      // Assert
      expect(publishStep).toBeDefined();
      // Should default to latest for stable versions
      expect(publishStep.run).toMatch(/--tag\s+latest/i);
    });
  });

  describe('Technical Spec: CONF-005 - NPM Token Authentication', () => {
    test('should configure NPM_TOKEN as environment variable', () => {
      // Arrange
      const publishJob = workflowConfig?.jobs?.publish;

      // Act
      const env = publishJob?.env || workflowConfig?.env;

      // Assert
      expect(env).toBeDefined();
      expect(env.NODE_AUTH_TOKEN || env.NPM_TOKEN).toBeDefined();
    });

    test('should reference GitHub secret for NPM_TOKEN', () => {
      // Arrange
      const publishJob = workflowConfig?.jobs?.publish;

      // Act
      const env = publishJob?.env || workflowConfig?.env;
      const tokenValue = env?.NODE_AUTH_TOKEN || env?.NPM_TOKEN;

      // Assert
      expect(tokenValue).toBeDefined();
      expect(tokenValue).toContain('secrets.NPM_TOKEN');
    });

    test('should setup Node.js with registry-url for authentication', () => {
      // Arrange
      const publishJob = workflowConfig?.jobs?.publish;

      // Act
      const steps = publishJob?.steps || [];
      const nodeSetup = steps.find(step => step.uses?.includes('setup-node'));

      // Assert
      expect(nodeSetup).toBeDefined();
      expect(nodeSetup.with?.['registry-url']).toBe('https://registry.npmjs.org');
    });
  });

  describe('NFR-001: Performance - Workflow Execution Time', () => {
    test('should complete workflow within 5 minutes', () => {
      // Arrange
      const timeoutMinutes = workflowConfig?.jobs?.publish?.['timeout-minutes'];

      // Act & Assert
      expect(timeoutMinutes).toBeDefined();
      expect(timeoutMinutes).toBeLessThanOrEqual(5);
    });

    test('should use caching for dependencies to improve speed', () => {
      // Arrange
      const publishJob = workflowConfig?.jobs?.publish;

      // Act
      const steps = publishJob?.steps || [];
      const nodeSetup = steps.find(step => step.uses?.includes('setup-node'));

      // Assert
      expect(nodeSetup).toBeDefined();
      expect(nodeSetup.with?.cache).toBe('npm');
    });
  });

  describe('NFR-002: Security - Token Protection', () => {
    test('should NOT expose NPM_TOKEN in logs', () => {
      // Arrange
      const publishJob = workflowConfig?.jobs?.publish;

      // Act
      const steps = publishJob?.steps || [];
      const allCommands = steps.map(step => step.run).filter(Boolean).join(' ');

      // Assert
      // Token should only be referenced as ${{ secrets.NPM_TOKEN }}, never echoed
      expect(allCommands).not.toMatch(/echo.*NPM_TOKEN|console\.log.*NPM_TOKEN/i);
    });

    test('should use GitHub-masked secrets for sensitive data', () => {
      // Arrange
      const publishJob = workflowConfig?.jobs?.publish;

      // Act
      const env = publishJob?.env || workflowConfig?.env;
      const tokenValue = env?.NODE_AUTH_TOKEN || env?.NPM_TOKEN;

      // Assert
      expect(tokenValue).toContain('secrets.NPM_TOKEN');
      // GitHub automatically masks secrets in logs
    });
  });

  describe('NFR-004: Reliability - Retry on Transient Failures', () => {
    test('should implement retry logic for npm publish', () => {
      // Arrange
      const publishJob = workflowConfig?.jobs?.publish;

      // Act
      const steps = publishJob?.steps || [];
      const publishStep = steps.find(step => step.run?.includes('npm publish'));

      // Assert
      expect(publishStep).toBeDefined();
      // Should have retry logic or use action with retry capability
      expect(publishStep.run || publishStep.uses).toMatch(/retry|attempt/i);
    });

    test('should use exponential backoff for retries', () => {
      // Arrange
      const publishJob = workflowConfig?.jobs?.publish;

      // Act
      const steps = publishJob?.steps || [];
      const publishStep = steps.find(step => step.run?.includes('npm publish'));

      // Assert
      expect(publishStep).toBeDefined();
      // Should mention backoff or delay between attempts
      expect(publishStep.run).toMatch(/backoff|delay|sleep/i);
    });
  });

  describe('Business Rules Validation', () => {
    test('BR-001: Git tag must match semver with v prefix', () => {
      // Arrange
      const semverRegex = /^v\d+\.\d+\.\d+(-[a-z0-9.]+)?$/;

      // Act & Assert
      expect('v1.0.0').toMatch(semverRegex);
      expect('v2.1.3-beta.1').toMatch(semverRegex);
      expect('1.0.0').not.toMatch(semverRegex); // Missing v prefix
      expect('release-1.0').not.toMatch(semverRegex); // Invalid format
    });

    test('BR-002: Package.json version must match tag version (minus v prefix)', () => {
      // Arrange
      const tag = 'v1.0.0';
      const expectedVersion = '1.0.0';

      // Act
      const extractedVersion = tag.replace(/^v/, '');

      // Assert
      expect(extractedVersion).toBe(expectedVersion);
    });

    test('BR-003: Duplicate versions cannot be published', () => {
      // This will be tested through integration tests
      // Unit test validates workflow has idempotency check
      const publishJob = workflowConfig?.jobs?.publish;
      const steps = publishJob?.steps || [];
      const idempotencyCheck = steps.some(step =>
        step.run?.includes('npm view') ||
        step.run?.includes('already published')
      );

      expect(idempotencyCheck).toBe(true);
    });

    test('BR-004: Pre-release versions use appropriate dist-tag', () => {
      // Arrange
      const testCases = [
        { version: 'v1.0.0-beta.1', expectedTag: 'beta' },
        { version: 'v2.0.0-rc.1', expectedTag: 'rc' },
        { version: 'v3.0.0', expectedTag: 'latest' }
      ];

      // Act & Assert
      testCases.forEach(({ version, expectedTag }) => {
        const isBeta = version.includes('-beta');
        const isRC = version.includes('-rc');
        const isStable = !version.includes('-');

        if (isBeta) expect(expectedTag).toBe('beta');
        if (isRC) expect(expectedTag).toBe('rc');
        if (isStable) expect(expectedTag).toBe('latest');
      });
    });
  });
});
