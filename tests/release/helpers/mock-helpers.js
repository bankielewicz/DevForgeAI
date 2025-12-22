/**
 * Mock Helper Functions for Release Script Tests (STORY-070)
 * Provides reusable mock implementations for subprocess commands
 */

/**
 * Mock successful git status (clean tree)
 */
function mockGitCleanTree(execSyncMock) {
  execSyncMock.mockImplementation((cmd) => {
    if (cmd.includes('git status --porcelain')) {
      return ''; // Empty = clean
    }
    return '';
  });
}

/**
 * Mock dirty git working tree
 */
function mockGitDirtyTree(execSyncMock, files = ['M  file1.txt', '?? file2.txt']) {
  execSyncMock.mockImplementation((cmd) => {
    if (cmd.includes('git status --porcelain')) {
      return files.join('\n');
    }
    throw new Error(`Uncommitted changes detected:\n${files.join('\n')}`);
  });
}

/**
 * Mock successful test suite execution
 */
function mockTestsPassing(execSyncMock, testCount = 156) {
  execSyncMock.mockImplementation((cmd) => {
    if (cmd.includes('npm test')) {
      return `Tests passed: ${testCount}/${testCount}`;
    }
    return '';
  });
}

/**
 * Mock failing test suite
 */
function mockTestsFailing(execSyncMock, passed = 155, total = 156) {
  execSyncMock.mockImplementation((cmd) => {
    if (cmd.includes('npm test')) {
      const error = new Error(`Tests failed: ${passed}/${total} passed, ${total - passed} failed`);
      error.code = 1;
      throw error;
    }
    return '';
  });
}

/**
 * Mock gh CLI authentication check
 */
function mockGhAuthenticated(execSyncMock, username = 'devforgeai-bot') {
  execSyncMock.mockImplementation((cmd) => {
    if (cmd.includes('gh auth status')) {
      return `Logged in to github.com as ${username}`;
    }
    return '';
  });
}

/**
 * Mock gh CLI not authenticated
 */
function mockGhNotAuthenticated(execSyncMock) {
  execSyncMock.mockImplementation((cmd) => {
    if (cmd.includes('gh auth status')) {
      const error = new Error('Not authenticated. Run: gh auth login');
      error.code = 1;
      throw error;
    }
    return '';
  });
}

/**
 * Mock npm authentication check
 */
function mockNpmAuthenticated(execSyncMock, username = 'devforgeai-bot') {
  execSyncMock.mockImplementation((cmd) => {
    if (cmd.includes('npm whoami')) {
      return username;
    }
    return '';
  });
}

/**
 * Mock version.json read
 */
function mockVersionJson(execSyncMock, version = '1.2.3') {
  execSyncMock.mockImplementation((cmd) => {
    if (cmd.includes('cat src/version.json')) {
      return JSON.stringify({
        version,
        release_date: '2025-11-20',
        release_notes_path: `CHANGELOG.md#v${version}`
      });
    }
    return '';
  });
}

/**
 * Mock successful sync operation
 */
function mockSyncSuccess(execSyncMock, fileCount = 234) {
  execSyncMock.mockImplementation((cmd) => {
    if (cmd.includes('rsync') && cmd.includes('.claude/')) {
      return `sent ${fileCount} files`;
    }
    if (cmd.includes('find .claude/ -type f | wc -l')) {
      return fileCount.toString();
    }
    if (cmd.includes('find src/claude/ -type f | wc -l')) {
      return fileCount.toString();
    }
    return '';
  });
}

/**
 * Mock sync failure
 */
function mockSyncFailure(execSyncMock, errorMessage = 'rsync failed: permission denied') {
  execSyncMock.mockImplementation((cmd) => {
    if (cmd.includes('rsync')) {
      const error = new Error(errorMessage);
      error.code = 1;
      throw error;
    }
    return '';
  });
}

/**
 * Mock checksum generation
 */
function mockChecksumGeneration(execSyncMock, fileCount = 230) {
  execSyncMock.mockImplementation((cmd) => {
    if (cmd.includes('sha256sum') || cmd.includes('shasum -a 256')) {
      const checksums = [];
      for (let i = 0; i < fileCount; i++) {
        const hash = `a${i}b${i}c${i}d${i}`.padEnd(64, '0');
        checksums.push(`${hash}  src/file${i}.txt`);
      }
      return checksums.join('\n');
    }
    if (cmd.includes('wc -l src/checksums.txt')) {
      return fileCount.toString();
    }
    return '';
  });
}

/**
 * Mock GitHub release creation success
 */
function mockGithubReleaseSuccess(execSyncMock, version = '1.2.4', org = 'devforgeai', repo = 'framework') {
  execSyncMock.mockImplementation((cmd) => {
    if (cmd.includes('gh release create')) {
      return `https://github.com/${org}/${repo}/releases/tag/v${version}`;
    }
    return '';
  });
}

/**
 * Mock GitHub release creation failure
 */
function mockGithubReleaseFailure(execSyncMock, errorMessage = 'gh: authentication expired') {
  execSyncMock.mockImplementation((cmd) => {
    if (cmd.includes('gh release create')) {
      const error = new Error(errorMessage);
      error.code = 1;
      throw error;
    }
    return '';
  });
}

/**
 * Mock NPM publish success
 */
function mockNpmPublishSuccess(execSyncMock, packageName = '@devforgeai/framework', version = '1.2.4') {
  execSyncMock.mockImplementation((cmd) => {
    if (cmd.includes('npm publish')) {
      return `+ ${packageName}@${version}`;
    }
    return '';
  });
}

/**
 * Mock NPM publish failure
 */
function mockNpmPublishFailure(execSyncMock, errorMessage = 'npm ERR! 403 Forbidden') {
  execSyncMock.mockImplementation((cmd) => {
    if (cmd.includes('npm publish')) {
      const error = new Error(errorMessage);
      error.code = 1;
      throw error;
    }
    return '';
  });
}

/**
 * Mock git tag creation
 */
function mockGitTagSuccess(execSyncMock, version = '1.2.4') {
  execSyncMock.mockImplementation((cmd) => {
    if (cmd.includes(`git tag -a v${version}`)) {
      return '';
    }
    if (cmd.includes('git tag -l')) {
      return `v1.0.0\nv1.1.0\nv1.2.0\nv1.2.3`;
    }
    return '';
  });
}

/**
 * Mock git tag already exists
 */
function mockGitTagExists(execSyncMock, version = '1.2.4') {
  execSyncMock.mockImplementation((cmd) => {
    if (cmd.includes(`git tag -a v${version}`) || cmd.includes(`git tag v${version}`)) {
      const error = new Error(`fatal: tag 'v${version}' already exists`);
      error.code = 128;
      throw error;
    }
    return '';
  });
}

/**
 * Mock rollback commands
 */
function mockRollbackCommands(execSyncMock) {
  execSyncMock.mockImplementation((cmd) => {
    if (cmd.includes('git reset --hard HEAD')) {
      return 'HEAD is now at abc1234';
    }
    if (cmd.includes('git tag -d')) {
      return 'Deleted tag v1.2.4';
    }
    return '';
  });
}

/**
 * Create a full successful release mock
 */
function mockFullReleaseSuccess(execSyncMock, version = '1.2.4') {
  execSyncMock.mockImplementation((cmd) => {
    if (cmd.includes('git status --porcelain')) return '';
    if (cmd.includes('npm test')) return 'Tests passed: 156/156';
    if (cmd.includes('gh auth status')) return 'Logged in to github.com as devforgeai-bot';
    if (cmd.includes('npm whoami')) return 'devforgeai-bot';
    if (cmd.includes('cat src/version.json')) return JSON.stringify({ version: '1.2.3' });
    if (cmd.includes('npm view @devforgeai/framework versions')) return '["1.0.0", "1.1.0", "1.2.0", "1.2.3"]';
    if (cmd.includes('git tag -l')) return 'v1.0.0\nv1.1.0\nv1.2.0\nv1.2.3';
    if (cmd.includes('rsync')) return 'sent 234 files';
    if (cmd.includes('find') && cmd.includes('wc -l')) return '234';
    if (cmd.includes('git tag -a')) return '';
    if (cmd.includes('git commit')) return `[main abc1234] chore(release): bump version to ${version}`;
    if (cmd.includes('sha256sum')) return 'a1b2c3d4...  src/version.json';
    if (cmd.includes('wc -l src/checksums.txt')) return '230';
    if (cmd.includes('gh release create')) return `https://github.com/devforgeai/framework/releases/tag/v${version}`;
    if (cmd.includes('git push')) return 'To github.com:devforgeai/framework.git';
    if (cmd.includes('npm publish')) return `+ @devforgeai/framework@${version}`;
    return '';
  });
}

module.exports = {
  mockGitCleanTree,
  mockGitDirtyTree,
  mockTestsPassing,
  mockTestsFailing,
  mockGhAuthenticated,
  mockGhNotAuthenticated,
  mockNpmAuthenticated,
  mockVersionJson,
  mockSyncSuccess,
  mockSyncFailure,
  mockChecksumGeneration,
  mockGithubReleaseSuccess,
  mockGithubReleaseFailure,
  mockNpmPublishSuccess,
  mockNpmPublishFailure,
  mockGitTagSuccess,
  mockGitTagExists,
  mockRollbackCommands,
  mockFullReleaseSuccess
};
