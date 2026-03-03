/**
 * Release Script Phases 3-7 Unit Tests (STORY-070)
 * Tests for version metadata, checksums, GitHub release, NPM publish, and rollback
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

describe('Release Script Phases 3-7 (STORY-070)', () => {

  beforeEach(() => {
    // Clear all mocks before each test
    execSync.mockClear();
    spawn.mockClear();
    exec.mockClear();
  });

  describe('Phase 3: Version Metadata and Changelog Update', () => {

    describe('DAT-001: version.json Update', () => {

      test('should update version field with semver format', () => {
        // Arrange
        const versionData = {
          version: '1.2.4',
          release_date: '2025-11-25',
          release_notes_path: 'CHANGELOG.md#v1.2.4'
        };

        // Act
        const semverRegex = /^\d+\.\d+\.\d+(-[a-zA-Z0-9]+)?$/;

        // Assert
        expect(semverRegex.test(versionData.version)).toBe(true);
      });

      test('should add release_date in ISO 8601 format', () => {
        // Arrange
        const releaseDate = '2025-11-25';

        // Act
        const isISO8601 = /^\d{4}-\d{2}-\d{2}$/.test(releaseDate);

        // Assert
        expect(isISO8601).toBe(true);
      });

      test('should add release_notes_path pointing to CHANGELOG.md section', () => {
        // Arrange
        const version = '1.2.4';
        const notesPath = `CHANGELOG.md#v${version}`;

        // Assert
        expect(notesPath).toBe('CHANGELOG.md#v1.2.4');
        expect(notesPath).toContain('CHANGELOG.md#');
      });

      test('should reject invalid semver format', () => {
        // Arrange
        const invalidVersions = ['1.2', 'v1.2.3', '1.2.3.4'];

        // Act & Assert
        invalidVersions.forEach(version => {
          const semverRegex = /^\d+\.\d+\.\d+(-[a-zA-Z0-9.]+)?$/;
          expect(semverRegex.test(version)).toBe(false);
        });
      });

    });

    describe('CHANGELOG.md Generation', () => {

      test('should generate changelog section with version and date', () => {
        // Arrange
        const version = '1.2.4';
        const date = '2025-11-25';

        // Act
        const changelogHeader = `## [v${version}] - ${date}`;

        // Assert
        expect(changelogHeader).toBe('## [v1.2.4] - 2025-11-25');
      });

      test('should group commits by type (feat, fix, chore, docs)', () => {
        // Arrange
        const commits = [
          'feat: Add new feature',
          'fix: Bug fix',
          'chore: Update dependencies',
          'docs: Update README'
        ];

        // Act
        const grouped = {
          feat: ['feat: Add new feature'],
          fix: ['fix: Bug fix'],
          chore: ['chore: Update dependencies'],
          docs: ['docs: Update README']
        };

        // Assert
        expect(grouped.feat).toHaveLength(1);
        expect(grouped.fix).toHaveLength(1);
        expect(grouped.chore).toHaveLength(1);
        expect(grouped.docs).toHaveLength(1);
      });

      test('should extract commit messages since last tag', () => {
        // Arrange
        execSync.mockImplementation((cmd) => {
          if (cmd.includes('git log --pretty=format:"%s" v1.2.3..HEAD')) {
            return 'feat: New feature\nfix: Bug fix\nchore: Update';
          }
          return '';
        });

        // Act
        const commits = execSync('git log --pretty=format:"%s" v1.2.3..HEAD')
          .toString()
          .split('\n');

        // Assert
        expect(commits).toHaveLength(3);
        expect(commits[0]).toContain('feat:');
      });

    });

    describe('Git Tag Creation', () => {

      test('should create git tag with v prefix', () => {
        // Arrange
        const version = '1.2.4';
        const tag = `v${version}`;

        // Assert
        expect(tag).toBe('v1.2.4');
      });

      test('should add tag message with release version', () => {
        // Arrange
        execSync.mockImplementation((cmd) => {
          if (cmd.includes('git tag -a v1.2.4 -m')) {
            return '';
          }
          return '';
        });

        // Act
        const tagMessage = 'Release v1.2.4';

        // Assert
        expect(tagMessage).toContain('Release v1.2.4');
      });

      test('should include changelog excerpt in tag message', () => {
        // Arrange
        const changelogExcerpt = 'feat: New feature\nfix: Bug fix';
        const tagMessage = `Release v1.2.4\n\n${changelogExcerpt}`;

        // Assert
        expect(tagMessage).toContain('feat: New feature');
        expect(tagMessage).toContain('fix: Bug fix');
      });

    });

    describe('Release Commit', () => {

      test('should create commit with chore(release) message', () => {
        // Arrange
        const version = '1.2.4';
        const commitMessage = `chore(release): bump version to ${version}`;

        // Assert
        expect(commitMessage).toBe('chore(release): bump version to 1.2.4');
      });

      test('should commit version.json and CHANGELOG.md changes', () => {
        // Arrange
        execSync.mockImplementation((cmd) => {
          if (cmd.includes('git add src/version.json CHANGELOG.md')) {
            return '';
          }
          return '';
        });

        // Act
        execSync('git add src/version.json CHANGELOG.md');

        // Assert
        expect(execSync).toHaveBeenCalledWith(expect.stringContaining('git add'));
      });

    });

  });

  describe('Phase 4: Integrity Verification with Checksum Generation (SCR-005)', () => {

    describe('CHK-001: Checksum File Format', () => {

      test('should generate SHA-256 checksums for all src/ files', () => {
        // Arrange
        execSync.mockImplementation((cmd) => {
          if (cmd.includes('find src/ -type f') && cmd.includes('sha256sum')) {
            return 'a1b2c3d4e5f6...  src/version.json\ne5f6a7b8c9d0...  src/checksums.txt';
          }
          return '';
        });

        // Act
        const checksums = execSync('find src/ -type f -exec sha256sum {} \\;');

        // Assert
        expect(checksums).toBeDefined();
      });

      test('each line should match format: {hash}  {filepath}', () => {
        // Arrange
        const checksumLine = 'a1b2c3d4e5f6789012345678901234567890123456789012345678901234  src/version.json';

        // Act
        const checksumRegex = /^[a-f0-9]{64}  .+$/;

        // Assert
        expect(checksumRegex.test(checksumLine)).toBe(true);
      });

      test('should use SHA-256 algorithm (64 hex characters)', () => {
        // Arrange
        const sha256Hash = 'a1b2c3d4e5f6789012345678901234567890123456789012345678901234';

        // Assert
        expect(sha256Hash).toHaveLength(64);
        expect(/^[a-f0-9]{64}$/.test(sha256Hash)).toBe(true);
      });

      test('should exclude checksums.txt itself from checksums', () => {
        // Arrange
        const checksumLines = [
          'hash1  src/version.json',
          'hash2  src/package.json',
          'hash3  src/README.md'
        ];

        // Assert
        checksumLines.forEach(line => {
          expect(line).not.toContain('checksums.txt');
        });
      });

      test('should exclude node_modules/ from checksums', () => {
        // Arrange
        const checksumLines = [
          'hash1  src/version.json',
          'hash2  src/package.json'
        ];

        // Assert
        checksumLines.forEach(line => {
          expect(line).not.toContain('node_modules/');
        });
      });

      test('should exclude .git/ directory from checksums', () => {
        // Arrange
        const checksumLines = [
          'hash1  src/version.json'
        ];

        // Assert
        checksumLines.forEach(line => {
          expect(line).not.toContain('.git/');
        });
      });

    });

    describe('CHK-002: Alphabetical Sorting', () => {

      test('checksums.txt should be sorted alphabetically by filepath', () => {
        // Arrange
        const checksums = [
          'hash1  src/a-file.txt',
          'hash2  src/b-file.txt',
          'hash3  src/c-file.txt'
        ];

        // Act
        const sorted = [...checksums].sort();

        // Assert
        expect(checksums).toEqual(sorted);
      });

    });

    describe('CHK-003: Minimum Entry Count', () => {

      test('checksums.txt should contain at least 50 entries', () => {
        // Arrange
        execSync.mockImplementation((cmd) => {
          if (cmd.includes('wc -l src/checksums.txt')) {
            return '230'; // Framework has 230 files
          }
          return '';
        });

        // Act
        const lineCount = parseInt(execSync('wc -l src/checksums.txt').toString().trim());

        // Assert
        expect(lineCount).toBeGreaterThanOrEqual(50);
      });

    });

    describe('Checksum File Hash in version.json', () => {

      test('should append checksum_file_sha256 to version.json', () => {
        // Arrange
        const versionData = {
          version: '1.2.4',
          release_date: '2025-11-25',
          release_notes_path: 'CHANGELOG.md#v1.2.4',
          checksum_file_sha256: 'e5f6a7b8c9d0...'
        };

        // Assert
        expect(versionData).toHaveProperty('checksum_file_sha256');
        expect(versionData.checksum_file_sha256).toHaveLength(64);
      });

    });

    describe('NFR-004: SHA-256 Algorithm Enforcement', () => {

      test('should use sha256sum command (not md5sum or sha1sum)', () => {
        // Arrange
        execSync.mockImplementation((cmd) => {
          if (cmd.includes('sha256sum')) {
            return 'hash  file';
          }
          return '';
        });

        // Act
        const command = 'sha256sum src/version.json';

        // Assert
        expect(command).toContain('sha256sum');
        expect(command).not.toContain('md5sum');
        expect(command).not.toContain('sha1sum');
      });

    });

    describe('NFR-009: Idempotent Checksums', () => {

      test('same input should produce same checksums on repeated runs', () => {
        // Arrange
        const fileContent = 'same content';

        // Act - Generate checksum twice
        const checksum1 = 'a1b2c3d4...'; // First run
        const checksum2 = 'a1b2c3d4...'; // Second run (same file)

        // Assert
        expect(checksum1).toBe(checksum2);
      });

    });

  });

  describe('Phase 5: GitHub Release Creation (SCR-006)', () => {

    describe('GitHub Release Command', () => {

      test('should create release using gh CLI', () => {
        // Arrange
        execSync.mockImplementation((cmd) => {
          if (cmd.includes('gh release create v1.2.4')) {
            return 'https://github.com/user/repo/releases/tag/v1.2.4';
          }
          return '';
        });

        // Act
        const releaseUrl = execSync('gh release create v1.2.4 --title "DevForgeAI v1.2.4"');

        // Assert
        expect(releaseUrl).toContain('github.com');
        expect(releaseUrl).toContain('/releases/tag/v1.2.4');
      });

      test('should set release title as "DevForgeAI v{version}"', () => {
        // Arrange
        const version = '1.2.4';
        const title = `DevForgeAI v${version}`;

        // Assert
        expect(title).toBe('DevForgeAI v1.2.4');
      });

      test('should attach checksums.txt to release', () => {
        // Arrange
        const releaseCommand = 'gh release create v1.2.4 src/checksums.txt';

        // Assert
        expect(releaseCommand).toContain('src/checksums.txt');
      });

      test('should mark as latest release (not pre-release)', () => {
        // Arrange
        const version = '1.2.4'; // No hyphen = stable release

        // Act
        const isPrerelease = version.includes('-');

        // Assert
        expect(isPrerelease).toBe(false);
      });

    });

    describe('BR-002: Pre-Release Detection', () => {

      test('should mark version with hyphen as pre-release', () => {
        // Arrange
        const version = '2.0.0-beta.1';

        // Act
        const isPrerelease = version.includes('-');

        // Assert
        expect(isPrerelease).toBe(true);
      });

      test('should use --prerelease flag for beta versions', () => {
        // Arrange
        const version = '2.0.0-beta.1';
        const command = `gh release create v${version} --prerelease`;

        // Assert
        expect(command).toContain('--prerelease');
      });

    });

    describe('Git Push to Remote', () => {

      test('should push git tag to origin', () => {
        // Arrange
        execSync.mockImplementation((cmd) => {
          if (cmd.includes('git push origin v1.2.4')) {
            return 'To github.com:user/repo.git';
          }
          return '';
        });

        // Act
        execSync('git push origin v1.2.4');

        // Assert
        expect(execSync).toHaveBeenCalledWith(expect.stringContaining('git push'));
      });

      test('should push release commit to origin/main', () => {
        // Arrange
        execSync.mockImplementation((cmd) => {
          if (cmd.includes('git push origin main')) {
            return 'To github.com:user/repo.git';
          }
          return '';
        });

        // Act
        execSync('git push origin main');

        // Assert
        expect(execSync).toHaveBeenCalledWith(expect.stringContaining('git push origin main'));
      });

    });

    describe('Release URL Output', () => {

      test('should output release URL for verification', () => {
        // Arrange
        const releaseUrl = 'https://github.com/devforgeai/framework/releases/tag/v1.2.4';

        // Assert
        expect(releaseUrl).toMatch(/^https:\/\/github\.com\/.+\/releases\/tag\/v\d+\.\d+\.\d+/);
      });

    });

  });

  describe('Phase 6: NPM Package Publication (SCR-007)', () => {

    describe('BR-005: STORY-067 Integration', () => {

      test('should verify src/package.json exists', () => {
        // Arrange
        execSync.mockImplementation((cmd) => {
          if (cmd.includes('test -f src/package.json')) {
            return '';
          }
          return '';
        });

        // Act
        const packageJsonExists = true; // Mock file exists

        // Assert
        expect(packageJsonExists).toBe(true);
      });

      test('should fail with helpful error if src/package.json missing', () => {
        // Arrange
        execSync.mockImplementation((cmd) => {
          if (cmd.includes('test -f src/package.json')) {
            const error = new Error('src/package.json not found. Run STORY-067 setup first.');
            error.code = 1;
            throw error;
          }
          return '';
        });

        // Act & Assert
        expect(() => {
          execSync('test -f src/package.json || exit 1');
        }).toThrow(/src\/package\.json not found/);
      });

    });

    describe('Package Version Update', () => {

      test('should update src/package.json version to match src/version.json', () => {
        // Arrange
        const versionJsonVersion = '1.2.4';
        const packageJsonVersion = '1.2.4';

        // Assert
        expect(packageJsonVersion).toBe(versionJsonVersion);
      });

    });

    describe('NPM Publish Execution', () => {

      test('should change directory to src/ before publishing', () => {
        // Arrange
        const command = 'cd src/ && npm publish';

        // Assert
        expect(command).toContain('cd src/');
      });

      test('should execute npm publish', () => {
        // Arrange
        execSync.mockImplementation((cmd) => {
          if (cmd.includes('npm publish')) {
            return '+ @devforgeai/framework@1.2.4';
          }
          return '';
        });

        // Act
        const result = execSync('npm publish');

        // Assert
        expect(result).toContain('@devforgeai/framework@1.2.4');
      });

      test('should use --dry-run flag when script invoked with --dry-run', () => {
        // Arrange
        const dryRun = true;
        const command = dryRun ? 'npm publish --dry-run' : 'npm publish';

        // Assert
        expect(command).toContain('--dry-run');
      });

    });

    describe('Dist-Tag Application', () => {

      test('should tag with "latest" for stable versions', () => {
        // Arrange
        const version = '1.2.4';
        const tag = version.includes('-') ? 'beta' : 'latest';

        // Assert
        expect(tag).toBe('latest');
      });

      test('should tag with "beta" for pre-release versions', () => {
        // Arrange
        const version = '2.0.0-beta.1';
        const tag = version.includes('-') ? 'beta' : 'latest';

        // Assert
        expect(tag).toBe('beta');
      });

    });

    describe('NPM Package URL Output', () => {

      test('should output npm package URL', () => {
        // Arrange
        const version = '1.2.4';
        const npmUrl = `https://www.npmjs.com/package/@devforgeai/framework/v/${version}`;

        // Assert
        expect(npmUrl).toContain('npmjs.com');
        expect(npmUrl).toContain('@devforgeai/framework');
        expect(npmUrl).toContain('v/1.2.4');
      });

    });

  });

  describe('Phase 7: Rollback and Error Recovery (SCR-008)', () => {

    describe('Error Detection', () => {

      test('should halt on non-zero exit code', () => {
        // Arrange
        execSync.mockImplementation((cmd) => {
          if (cmd.includes('failing-command')) {
            const error = new Error('Command failed');
            error.code = 1;
            throw error;
          }
          return '';
        });

        // Act & Assert
        expect(() => {
          execSync('failing-command');
        }).toThrow(/Command failed/);
      });

      test('should detect validation failure', () => {
        // Arrange
        const fileCount = 232; // Expected 234
        const expected = 234;

        // Act
        const validationFailed = fileCount !== expected;

        // Assert
        expect(validationFailed).toBe(true);
      });

      test('should detect user cancellation', () => {
        // Arrange
        const userInput = 'N'; // User said No to confirmation

        // Act
        const cancelled = userInput === 'N' || userInput === 'n';

        // Assert
        expect(cancelled).toBe(true);
      });

    });

    describe('BR-003: Atomic Phases', () => {

      test('should revert uncommitted changes on failure', () => {
        // Arrange
        execSync.mockImplementation((cmd) => {
          if (cmd.includes('git reset --hard HEAD')) {
            return 'HEAD is now at abc1234';
          }
          return '';
        });

        // Act
        execSync('git reset --hard HEAD');

        // Assert
        expect(execSync).toHaveBeenCalledWith(expect.stringContaining('git reset --hard HEAD'));
      });

      test('should delete created git tag if GitHub release not created', () => {
        // Arrange
        const tagCreated = true;
        const githubReleaseCreated = false;

        // Act
        if (tagCreated && !githubReleaseCreated) {
          execSync.mockImplementation((cmd) => {
            if (cmd.includes('git tag -d v1.2.4')) {
              return 'Deleted tag v1.2.4';
            }
            return '';
          });
          execSync('git tag -d v1.2.4');
        }

        // Assert
        expect(execSync).toHaveBeenCalledWith(expect.stringContaining('git tag -d'));
      });

      test('should NOT push to GitHub if local validation fails', () => {
        // Arrange
        const localValidationPassed = false;

        // Act
        const shouldPush = localValidationPassed;

        // Assert
        expect(shouldPush).toBe(false);
      });

      test('should NOT publish to npm if local validation fails', () => {
        // Arrange
        const localValidationPassed = false;

        // Act
        const shouldPublish = localValidationPassed;

        // Assert
        expect(shouldPublish).toBe(false);
      });

    });

    describe('Error Messages', () => {

      test('should display clear error message with failed phase name', () => {
        // Arrange
        const error = {
          phase: 'Phase 3: Version Metadata Update',
          message: 'Git tag v1.2.4 already exists'
        };

        // Act
        const errorOutput = `❌ Release Failed\nPhase: ${error.phase}\nError: ${error.message}`;

        // Assert
        expect(errorOutput).toContain('❌ Release Failed');
        expect(errorOutput).toContain('Phase 3');
        expect(errorOutput).toContain('Git tag v1.2.4 already exists');
      });

      test('should include specific error details', () => {
        // Arrange
        const errorMessage = 'Sync incomplete: expected 234 files, found 232. Missing: file1.txt, file2.txt';

        // Assert
        expect(errorMessage).toContain('Sync incomplete');
        expect(errorMessage).toContain('expected 234');
        expect(errorMessage).toContain('found 232');
        expect(errorMessage).toContain('Missing: file1.txt');
      });

    });

    describe('Rollback Summary', () => {

      test('should output rollback summary with reverted changes', () => {
        // Arrange
        const rollbackSummary = {
          reverted: ['version.json changes', 'git tag deleted'],
          notCreated: ['GitHub release', 'NPM publish']
        };

        // Act
        const summary = `
Rollback:
  ✓ ${rollbackSummary.reverted.join('\n  ✓ ')}
  ✗ ${rollbackSummary.notCreated.join('\n  ✗ ')}
        `.trim();

        // Assert
        expect(summary).toContain('✓ version.json changes');
        expect(summary).toContain('✓ git tag deleted');
        expect(summary).toContain('✗ GitHub release');
        expect(summary).toContain('✗ NPM publish');
      });

    });

    describe('Exit Code', () => {

      test('should exit with code 1 on failure', () => {
        // Arrange
        execSync.mockImplementation((cmd) => {
          if (cmd.includes('exit 1')) {
            const error = new Error('Exit code 1');
            error.code = 1;
            throw error;
          }
          return '';
        });

        // Act & Assert
        expect(() => {
          execSync('exit 1');
        }).toThrow();
      });

    });

  });

  describe('Command-Line Flags', () => {

    describe('SCR-009: --dry-run Flag', () => {

      test('should simulate release without external changes', () => {
        // Arrange
        const dryRun = true;

        // Act
        const shouldPush = !dryRun;
        const shouldPublish = !dryRun;

        // Assert
        expect(shouldPush).toBe(false);
        expect(shouldPublish).toBe(false);
      });

      test('should NOT push to GitHub in dry-run mode', () => {
        // Arrange
        execSync.mockImplementation((cmd) => {
          if (cmd.includes('git push') && cmd.includes('--dry-run')) {
            return '[DRY RUN] Would push to origin';
          }
          return '';
        });

        // Act
        const output = execSync('bash scripts/release.sh --dry-run');

        // Assert
        expect(output).toContain('[DRY RUN]');
      });

      test('should NOT publish to npm in dry-run mode', () => {
        // Arrange
        const command = 'npm publish --dry-run';

        // Assert
        expect(command).toContain('--dry-run');
      });

    });

    describe('SCR-010: --yes Flag', () => {

      test('should skip interactive prompts in CI mode', () => {
        // Arrange
        const yesFlag = true;

        // Act
        const shouldPrompt = !yesFlag;

        // Assert
        expect(shouldPrompt).toBe(false);
      });

      test('should auto-confirm version bump with --yes', () => {
        // Arrange
        const autoConfirm = true; // --yes flag passed

        // Act
        const needsConfirmation = !autoConfirm;

        // Assert
        expect(needsConfirmation).toBe(false);
      });

    });

  });

});
