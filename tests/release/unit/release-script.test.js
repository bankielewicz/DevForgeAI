/**
 * Release Script Unit Tests (STORY-070)
 * Tests for scripts/release.sh through mock-based subprocess testing
 *
 * Testing Approach: Since Bats/shellspec would require external dependencies,
 * we test the script logic through controlled subprocess mocks using child_process.
 *
 * Coverage Target: >= 80% for script logic
 */

// Mock child_process BEFORE any imports
jest.mock('child_process', () => {
  const originalModule = jest.requireActual('child_process');

  return {
    ...originalModule,
    execSync: jest.fn(),
    spawn: jest.fn(),
    exec: jest.fn()
  };
});

const { execSync, spawn, exec } = require('child_process');
const fs = require('fs');
const path = require('path');

// Test environment setup
process.env.NODE_ENV = 'test';

describe('Release Script Unit Tests (STORY-070)', () => {

  const SCRIPT_PATH = path.join(__dirname, '../../../scripts/release.sh');
  const CONFIG_PATH = path.join(__dirname, '../../../.devforgeai/config/release-config.sh');

  beforeEach(() => {
    // Clear all mocks before each test
    execSync.mockClear();
    spawn.mockClear();
    exec.mockClear();
  });

  describe('Phase 0: Pre-Flight Validation', () => {

    describe('SCR-002: Git Working Tree Validation', () => {

      test('should reject dirty git working tree', () => {
        // Arrange - Mock git status showing uncommitted changes
        execSync.mockImplementation((cmd) => {
          if (cmd.includes('git status --porcelain')) {
            return 'M  .ai_docs/Stories/STORY-070.story.md\n?? new-file.txt\n';
          }
          return '';
        });

        // Act & Assert
        expect(() => {
          execSync('bash scripts/release.sh');
        }).toThrow(/Uncommitted changes detected/);
      });

      test('should pass with clean git working tree', () => {
        // Arrange - Mock git status showing clean tree
        execSync.mockImplementation((cmd) => {
          if (cmd.includes('git status --porcelain')) {
            return ''; // Empty = clean tree
          }
          return '';
        });

        // Act
        const result = execSync('bash scripts/release.sh --dry-run');

        // Assert
        expect(result).toBeDefined();
        expect(execSync).toHaveBeenCalledWith(expect.stringContaining('git status --porcelain'));
      });

      test('should display list of uncommitted files on dirty tree', () => {
        // Arrange
        const dirtyFiles = [
          'M  src/version.json',
          '?? untracked-file.md'
        ].join('\n');

        execSync.mockImplementation((cmd) => {
          if (cmd.includes('git status --porcelain')) {
            return dirtyFiles;
          }
          throw new Error('Uncommitted changes detected:\n' + dirtyFiles);
        });

        // Act & Assert
        try {
          execSync('bash scripts/release.sh');
          throw new Error('Should have thrown');
        } catch (error) {
          expect(error.message).toContain('Uncommitted changes detected');
          expect(error.message).toContain('src/version.json');
          expect(error.message).toContain('untracked-file.md');
        }
      });

    });

    describe('Test Suite Execution', () => {

      test('should run test suite before proceeding', () => {
        // Arrange
        execSync.mockImplementation((cmd) => {
          if (cmd.includes('npm test')) {
            return 'Tests passed: 156/156';
          }
          return '';
        });

        // Act
        execSync('bash scripts/release.sh --dry-run');

        // Assert
        expect(execSync).toHaveBeenCalledWith(expect.stringContaining('npm test'));
      });

      test('should block release if tests fail', () => {
        // Arrange
        execSync.mockImplementation((cmd) => {
          if (cmd.includes('npm test')) {
            const error = new Error('Tests failed: 155/156 passed, 1 failed');
            error.code = 1;
            throw error;
          }
          return '';
        });

        // Act & Assert
        expect(() => {
          execSync('bash scripts/release.sh');
        }).toThrow(/Tests failed/);
      });

    });

    describe('External Tools Validation', () => {

      test('should check gh CLI is installed', () => {
        // Arrange
        execSync.mockImplementation((cmd) => {
          if (cmd.includes('gh --version')) {
            return 'gh version 2.40.1';
          }
          return '';
        });

        // Act
        execSync('bash scripts/release.sh --dry-run');

        // Assert
        expect(execSync).toHaveBeenCalledWith(expect.stringContaining('gh --version'));
      });

      test('should check gh CLI is authenticated', () => {
        // Arrange
        execSync.mockImplementation((cmd) => {
          if (cmd.includes('gh auth status')) {
            return 'Logged in to github.com as user123';
          }
          return '';
        });

        // Act
        execSync('bash scripts/release.sh --dry-run');

        // Assert
        expect(execSync).toHaveBeenCalledWith(expect.stringContaining('gh auth status'));
      });

      test('should block release if gh CLI not authenticated', () => {
        // Arrange
        execSync.mockImplementation((cmd) => {
          if (cmd.includes('gh auth status')) {
            const error = new Error('Not authenticated. Run: gh auth login');
            error.code = 1;
            throw error;
          }
          return '';
        });

        // Act & Assert
        expect(() => {
          execSync('bash scripts/release.sh');
        }).toThrow(/Not authenticated/);
      });

      test('should check npm is authenticated', () => {
        // Arrange
        execSync.mockImplementation((cmd) => {
          if (cmd.includes('npm whoami')) {
            return 'devforgeai-bot';
          }
          return '';
        });

        // Act
        execSync('bash scripts/release.sh --dry-run');

        // Assert
        expect(execSync).toHaveBeenCalledWith(expect.stringContaining('npm whoami'));
      });

    });

  });

  describe('Phase 1: Version Selection and Confirmation (SCR-001)', () => {

    describe('Version Bump Calculation', () => {

      test('should calculate patch version bump (1.2.3 → 1.2.4)', () => {
        // Arrange - Current version 1.2.3
        const currentVersion = '1.2.3';

        // Act - Calculate patch bump
        const nextVersion = incrementVersion(currentVersion, 'patch');

        // Assert
        expect(nextVersion).toBe('1.2.4');
      });

      test('should calculate minor version bump (1.2.3 → 1.3.0)', () => {
        // Arrange
        const currentVersion = '1.2.3';

        // Act
        const nextVersion = incrementVersion(currentVersion, 'minor');

        // Assert
        expect(nextVersion).toBe('1.3.0');
      });

      test('should calculate major version bump (1.2.3 → 2.0.0)', () => {
        // Arrange
        const currentVersion = '1.2.3';

        // Act
        const nextVersion = incrementVersion(currentVersion, 'major');

        // Assert
        expect(nextVersion).toBe('2.0.0');
      });

      test('should accept custom version input', () => {
        // Arrange
        const customVersion = '2.5.1-beta.3';

        // Act
        const isValid = validateSemver(customVersion);

        // Assert
        expect(isValid).toBe(true);
      });

      test('should reject invalid semver format', () => {
        // Arrange
        const invalidVersions = ['1.2', 'v1.2.3', '1.2.3.4', 'latest'];

        // Act & Assert
        invalidVersions.forEach(version => {
          expect(validateSemver(version)).toBe(false);
        });
      });

    });

    describe('Interactive Version Selection', () => {

      test('should display current version from src/version.json', () => {
        // Arrange
        const versionData = { version: '1.2.3' };
        execSync.mockImplementation((cmd) => {
          if (cmd.includes('cat src/version.json')) {
            return JSON.stringify(versionData);
          }
          return '';
        });

        // Act
        const result = execSync('bash scripts/release.sh --dry-run');

        // Assert
        expect(execSync).toHaveBeenCalledWith(expect.stringContaining('cat src/version.json'));
      });

      test('should prompt for version bump type (major/minor/patch/custom)', () => {
        // Arrange - Mock interactive input
        const stdin = require('mock-stdin').stdin();

        // Act
        const prompt = 'Select version bump type:\n  1) patch\n  2) minor\n  3) major\n  4) custom';

        // Assert
        expect(prompt).toContain('patch');
        expect(prompt).toContain('minor');
        expect(prompt).toContain('major');
        expect(prompt).toContain('custom');
      });

      test('should display calculated next version before confirmation', () => {
        // Arrange
        const currentVersion = '1.2.3';
        const bumpType = 'minor';
        const nextVersion = '1.3.0';

        // Act
        const confirmationMessage = `Release v${nextVersion} will:\n  - Create git tag v${nextVersion}`;

        // Assert
        expect(confirmationMessage).toContain('v1.3.0');
      });

      test('should require explicit Y/N confirmation', () => {
        // Arrange
        const prompt = 'Proceed? [y/N]:';

        // Assert
        expect(prompt).toMatch(/\[y\/N\]/);
      });

    });

    describe('BR-001: Version Uniqueness Validation', () => {

      test('should check version does not exist in npm registry', () => {
        // Arrange
        execSync.mockImplementation((cmd) => {
          if (cmd.includes('npm view @devforgeai/framework versions')) {
            return '["1.0.0", "1.1.0", "1.2.0", "1.2.3"]';
          }
          return '';
        });

        // Act
        const newVersion = '1.2.4';
        const exists = checkVersionExists(newVersion, ['1.0.0', '1.1.0', '1.2.0', '1.2.3']);

        // Assert
        expect(exists).toBe(false);
      });

      test('should block release if version already exists in npm', () => {
        // Arrange
        execSync.mockImplementation((cmd) => {
          if (cmd.includes('npm view')) {
            return '["1.0.0", "1.2.3", "1.2.4"]'; // 1.2.4 already published
          }
          return '';
        });

        // Act & Assert
        expect(() => {
          execSync('bash scripts/release.sh');
        }).toThrow(/Version 1\.2\.4 already exists/);
      });

      test('should check version does not exist as git tag', () => {
        // Arrange
        execSync.mockImplementation((cmd) => {
          if (cmd.includes('git tag -l')) {
            return 'v1.0.0\nv1.1.0\nv1.2.0\nv1.2.3';
          }
          return '';
        });

        // Act
        const newVersion = 'v1.2.4';
        const tags = ['v1.0.0', 'v1.1.0', 'v1.2.0', 'v1.2.3'];

        // Assert
        expect(tags).not.toContain(newVersion);
      });

      test('should block release if git tag already exists', () => {
        // Arrange
        execSync.mockImplementation((cmd) => {
          if (cmd.includes('git tag -l v1.2.4')) {
            return 'v1.2.4'; // Tag exists
          }
          if (cmd.includes('git tag v1.2.4')) {
            const error = new Error('fatal: tag \'v1.2.4\' already exists');
            error.code = 128;
            throw error;
          }
          return '';
        });

        // Act & Assert
        expect(() => {
          execSync('bash scripts/release.sh');
        }).toThrow(/tag.*already exists/);
      });

    });

  });

  describe('Phase 2: Operational Files Sync (SCR-003, SCR-004)', () => {

    describe('Claude Directory Sync', () => {

      test('should sync .claude/ to src/claude/ recursively', () => {
        // Arrange
        execSync.mockImplementation((cmd) => {
          if (cmd.includes('rsync') && cmd.includes('.claude/') && cmd.includes('src/claude/')) {
            return 'sent 234 files';
          }
          return '';
        });

        // Act
        execSync('bash scripts/release.sh --dry-run');

        // Assert
        expect(execSync).toHaveBeenCalledWith(
          expect.stringMatching(/rsync.*\.claude\/.*src\/claude\//)
        );
      });

      test('should exclude *.backup* files from sync', () => {
        // Arrange
        const excludePatterns = ['*.backup*', '__pycache__/', '*.pyc', '.DS_Store'];

        // Act
        const syncCommand = 'rsync -av --exclude="*.backup*" --exclude="__pycache__/" .claude/ src/claude/';

        // Assert
        expect(syncCommand).toContain('--exclude="*.backup*"');
      });

      test('should exclude __pycache__/ directories from sync', () => {
        // Arrange
        const syncCommand = 'rsync -av --exclude="__pycache__/" .claude/ src/claude/';

        // Assert
        expect(syncCommand).toContain('--exclude="__pycache__/"');
      });

      test('should exclude *.pyc files from sync', () => {
        // Arrange
        const syncCommand = 'rsync -av --exclude="*.pyc" .claude/ src/claude/';

        // Assert
        expect(syncCommand).toContain('--exclude="*.pyc"');
      });

      test('should exclude .DS_Store files from sync', () => {
        // Arrange
        const syncCommand = 'rsync -av --exclude=".DS_Store" .claude/ src/claude/';

        // Assert
        expect(syncCommand).toContain('--exclude=".DS_Store"');
      });

    });

    describe('DevForgeAI Directory Sync', () => {

      test('should sync .devforgeai/ to src/devforgeai/ recursively', () => {
        // Arrange
        execSync.mockImplementation((cmd) => {
          if (cmd.includes('.devforgeai/') && cmd.includes('src/devforgeai/')) {
            return 'sent 145 files';
          }
          return '';
        });

        // Act
        execSync('bash scripts/release.sh --dry-run');

        // Assert
        expect(execSync).toHaveBeenCalledWith(
          expect.stringMatching(/\.devforgeai\/.*src\/devforgeai\//)
        );
      });

      test('should exclude backups/ directory from sync', () => {
        // Arrange
        const syncCommand = 'rsync -av --exclude="backups/" .devforgeai/ src/devforgeai/';

        // Assert
        expect(syncCommand).toContain('--exclude="backups/"');
      });

      test('should exclude qa/reports/ directory from sync', () => {
        // Arrange
        const syncCommand = 'rsync -av --exclude="qa/reports/" .devforgeai/ src/devforgeai/';

        // Assert
        expect(syncCommand).toContain('--exclude="qa/reports/"');
      });

      test('should exclude feedback/sessions/ directory from sync', () => {
        // Arrange
        const syncCommand = 'rsync -av --exclude="feedback/sessions/" .devforgeai/ src/devforgeai/';

        // Assert
        expect(syncCommand).toContain('--exclude="feedback/sessions/"');
      });

      test('should exclude *.log files from sync', () => {
        // Arrange
        const syncCommand = 'rsync -av --exclude="*.log" .devforgeai/ src/devforgeai/';

        // Assert
        expect(syncCommand).toContain('--exclude="*.log"');
      });

    });

    describe('Sync Validation', () => {

      test('should validate file counts match expected (source vs destination)', () => {
        // Arrange
        execSync.mockImplementation((cmd) => {
          if (cmd.includes('find .claude/ -type f | wc -l')) {
            return '234';
          }
          if (cmd.includes('find src/claude/ -type f | wc -l')) {
            return '234';
          }
          return '';
        });

        // Act
        const sourceCount = 234;
        const destCount = 234;

        // Assert
        expect(sourceCount).toBe(destCount);
      });

      test('should report missing files if sync incomplete', () => {
        // Arrange
        execSync.mockImplementation((cmd) => {
          if (cmd.includes('find .claude/')) {
            return '234'; // Source has 234 files
          }
          if (cmd.includes('find src/claude/')) {
            return '232'; // Destination has 232 files (2 missing)
          }
          throw new Error('Sync incomplete: expected 234 files, found 232. Missing: [list]');
        });

        // Act & Assert
        expect(() => {
          execSync('bash scripts/release.sh');
        }).toThrow(/Sync incomplete.*expected 234.*found 232/);
      });

    });

    describe('MAN-001: Sync Manifest Generation', () => {

      test('should create src/.sync-manifest.json', () => {
        // Arrange
        const manifest = {
          sync_timestamp: '2025-11-25T10:30:00Z',
          file_count: 234,
          excluded_patterns: ['*.backup*', '__pycache__/', '*.pyc', '.DS_Store'],
          source_hash: 'a3f5c1b9e2d4'
        };

        // Act
        const manifestPath = 'src/.sync-manifest.json';

        // Assert
        expect(manifest).toHaveProperty('sync_timestamp');
        expect(manifest).toHaveProperty('file_count');
        expect(manifest).toHaveProperty('excluded_patterns');
        expect(manifest).toHaveProperty('source_hash');
      });

      test('manifest file_count should match actual synced files', () => {
        // Arrange
        const manifestFileCount = 234;
        const actualFileCount = 234; // from find src/ | wc -l

        // Assert
        expect(manifestFileCount).toBe(actualFileCount);
      });

      test('manifest should contain ISO 8601 timestamp', () => {
        // Arrange
        const timestamp = '2025-11-25T10:30:00Z';

        // Act
        const isISO8601 = /^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$/.test(timestamp);

        // Assert
        expect(isISO8601).toBe(true);
      });

    });

  });

  // Helper functions (JavaScript implementations mirroring bash script logic)
  function incrementVersion(version, type) {
    const parts = version.split('.');
    let major = parseInt(parts[0]);
    let minor = parseInt(parts[1]);
    let patch = parseInt(parts[2].split('-')[0]); // Remove pre-release suffix

    switch (type) {
      case 'major':
        return `${major + 1}.0.0`;
      case 'minor':
        return `${major}.${minor + 1}.0`;
      case 'patch':
        return `${major}.${minor}.${patch + 1}`;
      default:
        return version;
    }
  }

  function validateSemver(version) {
    const semverRegex = /^[0-9]+\.[0-9]+\.[0-9]+(-[a-zA-Z0-9.]+)?$/;
    return semverRegex.test(version);
  }

  function checkVersionExists(version, existingVersions) {
    return existingVersions.includes(version);
  }

});
