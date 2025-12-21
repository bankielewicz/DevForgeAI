/**
 * STORY-069: Offline Installation Support
 * Unit Tests: Offline Bundle Structure
 *
 * Tests AC#1: Complete Framework Bundle in NPM Package
 * Tests AC#8: Bundle Integrity Verification
 *
 * Technical Specification Coverage:
 * - DM-001: .claude/ and devforgeai/ directories bundled
 * - DM-002: Python wheel files bundled
 * - DM-003: Compressed package ≤ 60MB
 * - CONF-001: All bundled files have checksum entries
 *
 * Expected Result: ALL TESTS SHOULD FAIL (TDD Red Phase)
 * Implementation: Bundled files and checksums do not exist yet
 */

const fs = require('fs');
const path = require('path');
const crypto = require('crypto');

describe('AC#1: Complete Framework Bundle in NPM Package', () => {
  const rootPath = path.join(__dirname, '../../..');
  const bundledPath = path.join(rootPath, 'bundled');

  describe('DM-001: Framework directories bundled', () => {
    test('bundled/ directory exists', () => {
      expect(fs.existsSync(bundledPath)).toBe(true);
      expect(fs.statSync(bundledPath).isDirectory()).toBe(true);
    });

    test('bundled/claude/ directory exists', () => {
      const claudePath = path.join(bundledPath, 'claude');
      expect(fs.existsSync(claudePath)).toBe(true);
      expect(fs.statSync(claudePath).isDirectory()).toBe(true);
    });

    test('bundled/claude/agents/ directory exists with files', () => {
      const agentsPath = path.join(bundledPath, 'claude/agents');
      expect(fs.existsSync(agentsPath)).toBe(true);

      const files = fs.readdirSync(agentsPath);
      expect(files.length).toBeGreaterThan(0);
    });

    test('bundled/claude/commands/ directory exists with files', () => {
      const commandsPath = path.join(bundledPath, 'claude/commands');
      expect(fs.existsSync(commandsPath)).toBe(true);

      const files = fs.readdirSync(commandsPath);
      expect(files.length).toBeGreaterThan(0);
    });

    test('bundled/claude/memory/ directory exists with files', () => {
      const memoryPath = path.join(bundledPath, 'claude/memory');
      expect(fs.existsSync(memoryPath)).toBe(true);

      const files = fs.readdirSync(memoryPath);
      expect(files.length).toBeGreaterThan(0);
    });

    test('bundled/claude/scripts/ directory exists with files', () => {
      const scriptsPath = path.join(bundledPath, 'claude/scripts');
      expect(fs.existsSync(scriptsPath)).toBe(true);

      const files = fs.readdirSync(scriptsPath);
      expect(files.length).toBeGreaterThan(0);
    });

    test('bundled/claude/skills/ directory exists with files', () => {
      const skillsPath = path.join(bundledPath, 'claude/skills');
      expect(fs.existsSync(skillsPath)).toBe(true);

      const files = fs.readdirSync(skillsPath);
      expect(files.length).toBeGreaterThan(0);
    });

    test('bundled/devforgeai/ directory exists', () => {
      const devforgeaiPath = path.join(bundledPath, 'devforgeai');
      expect(fs.existsSync(devforgeaiPath)).toBe(true);
      expect(fs.statSync(devforgeaiPath).isDirectory()).toBe(true);
    });

    test('bundled/devforgeai/context/ directory exists with template files', () => {
      const contextPath = path.join(bundledPath, 'devforgeai/context');
      expect(fs.existsSync(contextPath)).toBe(true);

      const files = fs.readdirSync(contextPath);
      expect(files.length).toBeGreaterThan(0);

      // Should contain template files like tech-stack.md.template
      const hasTemplates = files.some(file => file.endsWith('.template') || file.endsWith('.md'));
      expect(hasTemplates).toBe(true);
    });

    test('bundled/devforgeai/protocols/ directory exists with files', () => {
      const protocolsPath = path.join(bundledPath, 'devforgeai/protocols');
      expect(fs.existsSync(protocolsPath)).toBe(true);

      const files = fs.readdirSync(protocolsPath);
      expect(files.length).toBeGreaterThan(0);
    });

    test('bundled/devforgeai/specs/ directory exists with files', () => {
      const specsPath = path.join(bundledPath, 'devforgeai/specs');
      expect(fs.existsSync(specsPath)).toBe(true);

      const files = fs.readdirSync(specsPath);
      expect(files.length).toBeGreaterThan(0);
    });
  });

  describe('DM-002: Python wheel files bundled', () => {
    test('bundled/python-cli/ directory exists', () => {
      const pythonCliPath = path.join(bundledPath, 'python-cli');
      expect(fs.existsSync(pythonCliPath)).toBe(true);
      expect(fs.statSync(pythonCliPath).isDirectory()).toBe(true);
    });

    test('bundled/python-cli/wheels/ directory exists', () => {
      const wheelsPath = path.join(bundledPath, 'python-cli/wheels');
      expect(fs.existsSync(wheelsPath)).toBe(true);
      expect(fs.statSync(wheelsPath).isDirectory()).toBe(true);
    });

    test('bundled/python-cli/wheels/ contains .whl files', () => {
      const wheelsPath = path.join(bundledPath, 'python-cli/wheels');

      if (fs.existsSync(wheelsPath)) {
        const files = fs.readdirSync(wheelsPath);
        const wheelFiles = files.filter(file => file.endsWith('.whl'));

        expect(wheelFiles.length).toBeGreaterThan(0);
      } else {
        throw new Error('wheels/ directory does not exist');
      }
    });

    test('bundled/python-cli/wheels/ contains devforgeai CLI wheel', () => {
      const wheelsPath = path.join(bundledPath, 'python-cli/wheels');

      if (fs.existsSync(wheelsPath)) {
        const files = fs.readdirSync(wheelsPath);
        const devforgeaiWheel = files.find(file =>
          file.startsWith('devforgeai') && file.endsWith('.whl')
        );

        expect(devforgeaiWheel).toBeDefined();
      }
    });
  });

  describe('AC#1: Bundle contains 200+ framework files', () => {
    test('bundled/ directory contains at least 200 files recursively', () => {
      function countFilesRecursive(dir) {
        let count = 0;
        const items = fs.readdirSync(dir);

        for (const item of items) {
          const fullPath = path.join(dir, item);
          const stat = fs.statSync(fullPath);

          if (stat.isDirectory()) {
            count += countFilesRecursive(fullPath);
          } else if (stat.isFile()) {
            count++;
          }
        }

        return count;
      }

      if (fs.existsSync(bundledPath)) {
        const fileCount = countFilesRecursive(bundledPath);
        expect(fileCount).toBeGreaterThanOrEqual(200);
      } else {
        throw new Error('bundled/ directory does not exist');
      }
    });
  });

  describe('DM-003: Package size within limits', () => {
    test('bundled/ directory size is <= 150MB uncompressed', () => {
      function calculateDirectorySize(dir) {
        let totalSize = 0;
        const items = fs.readdirSync(dir);

        for (const item of items) {
          const fullPath = path.join(dir, item);
          const stat = fs.statSync(fullPath);

          if (stat.isDirectory()) {
            totalSize += calculateDirectorySize(fullPath);
          } else if (stat.isFile()) {
            totalSize += stat.size;
          }
        }

        return totalSize;
      }

      if (fs.existsSync(bundledPath)) {
        const totalBytes = calculateDirectorySize(bundledPath);
        const totalMB = totalBytes / (1024 * 1024);

        expect(totalMB).toBeLessThanOrEqual(150);
      }
    });
  });

  describe('Documentation files bundled', () => {
    test('bundled/CLAUDE.md template exists', () => {
      const claudeMdPath = path.join(bundledPath, 'CLAUDE.md');
      expect(fs.existsSync(claudeMdPath)).toBe(true);
    });

    test('bundled/README.md exists', () => {
      const readmePath = path.join(bundledPath, 'README.md');
      expect(fs.existsSync(readmePath)).toBe(true);
    });
  });
});

describe('AC#8: Bundle Integrity Verification', () => {
  const rootPath = path.join(__dirname, '../../..');
  const bundledPath = path.join(rootPath, 'bundled');
  const checksumsPath = path.join(bundledPath, 'checksums.json');

  describe('CONF-001: All bundled files have checksums', () => {
    test('bundled/checksums.json file exists', () => {
      expect(fs.existsSync(checksumsPath)).toBe(true);
      expect(fs.statSync(checksumsPath).isFile()).toBe(true);
    });

    test('checksums.json is valid JSON', () => {
      if (fs.existsSync(checksumsPath)) {
        const content = fs.readFileSync(checksumsPath, 'utf8');
        expect(() => JSON.parse(content)).not.toThrow();
      }
    });

    test('checksums.json contains at least 200 entries', () => {
      if (fs.existsSync(checksumsPath)) {
        const checksums = JSON.parse(fs.readFileSync(checksumsPath, 'utf8'));
        const entryCount = Object.keys(checksums).length;

        expect(entryCount).toBeGreaterThanOrEqual(200);
      }
    });

    test('every bundled file has a checksum entry', () => {
      function getAllFiles(dir, baseDir = dir) {
        let files = [];
        const items = fs.readdirSync(dir);

        for (const item of items) {
          // Skip checksums.json itself
          if (item === 'checksums.json') continue;

          const fullPath = path.join(dir, item);
          const stat = fs.statSync(fullPath);

          if (stat.isDirectory()) {
            files = files.concat(getAllFiles(fullPath, baseDir));
          } else if (stat.isFile()) {
            const relativePath = path.relative(baseDir, fullPath).replace(/\\/g, '/');
            files.push(relativePath);
          }
        }

        return files;
      }

      if (fs.existsSync(bundledPath) && fs.existsSync(checksumsPath)) {
        const allFiles = getAllFiles(bundledPath);
        const checksums = JSON.parse(fs.readFileSync(checksumsPath, 'utf8'));

        const missingChecksums = allFiles.filter(file => !(file in checksums));

        if (missingChecksums.length > 0) {
          throw new Error(
            `${missingChecksums.length} files missing checksums:\n${missingChecksums.slice(0, 10).join('\n')}`
          );
        }

        expect(missingChecksums.length).toBe(0);
      }
    });

    test('all checksums are valid SHA256 hashes (64 hex characters)', () => {
      if (fs.existsSync(checksumsPath)) {
        const checksums = JSON.parse(fs.readFileSync(checksumsPath, 'utf8'));

        for (const [file, hash] of Object.entries(checksums)) {
          expect(hash).toMatch(/^[a-f0-9]{64}$/i);
        }
      }
    });
  });

  describe('Checksum verification algorithm', () => {
    test('SHA256 checksum calculation matches expected format', () => {
      const testContent = 'Test content for checksum validation';
      const expectedHash = crypto
        .createHash('sha256')
        .update(testContent)
        .digest('hex');

      // Verify hash is 64 hex characters
      expect(expectedHash).toMatch(/^[a-f0-9]{64}$/);
      expect(expectedHash.length).toBe(64);
    });

    test('checksums can be verified for existing bundled files', () => {
      if (fs.existsSync(bundledPath) && fs.existsSync(checksumsPath)) {
        const checksums = JSON.parse(fs.readFileSync(checksumsPath, 'utf8'));

        // Test first 10 files for performance
        const filesToTest = Object.keys(checksums).slice(0, 10);

        for (const relativeFilePath of filesToTest) {
          const fullPath = path.join(bundledPath, relativeFilePath);

          if (fs.existsSync(fullPath)) {
            const content = fs.readFileSync(fullPath);
            const actualHash = crypto.createHash('sha256').update(content).digest('hex');
            const expectedHash = checksums[relativeFilePath];

            expect(actualHash).toBe(expectedHash);
          }
        }
      }
    });

    test('checksum mismatch is detectable', () => {
      const originalContent = 'Original file content';
      const modifiedContent = 'Modified file content';

      const originalHash = crypto.createHash('sha256').update(originalContent).digest('hex');
      const modifiedHash = crypto.createHash('sha256').update(modifiedContent).digest('hex');

      expect(originalHash).not.toBe(modifiedHash);
    });
  });

  describe('Checksum file coverage validation', () => {
    test('checksums.json covers all critical directories', () => {
      if (fs.existsSync(checksumsPath)) {
        const checksums = JSON.parse(fs.readFileSync(checksumsPath, 'utf8'));
        const files = Object.keys(checksums);

        // Critical directories that must have checksum coverage
        const criticalDirs = [
          'claude/agents',
          'claude/commands',
          'claude/memory',
          'claude/skills',
          'devforgeai/context',
          'devforgeai/protocols'
        ];

        for (const dir of criticalDirs) {
          const hasCoverage = files.some(file => file.startsWith(dir + '/'));
          expect(hasCoverage).toBe(true);
        }
      }
    });

    test('checksums.json includes Python wheel files', () => {
      if (fs.existsSync(checksumsPath)) {
        const checksums = JSON.parse(fs.readFileSync(checksumsPath, 'utf8'));
        const files = Object.keys(checksums);

        const hasWheelChecksums = files.some(file =>
          file.startsWith('python-cli/wheels/') && file.endsWith('.whl')
        );

        expect(hasWheelChecksums).toBe(true);
      }
    });

    test('checksums.json includes CLAUDE.md template', () => {
      if (fs.existsSync(checksumsPath)) {
        const checksums = JSON.parse(fs.readFileSync(checksumsPath, 'utf8'));

        expect(checksums).toHaveProperty('CLAUDE.md');
      }
    });
  });
});

describe('Bundle structure compliance with NPM best practices', () => {
  const rootPath = path.join(__dirname, '../../..');
  const bundledPath = path.join(rootPath, 'bundled');

  test('bundled/ directory does not contain development files', () => {
    const forbiddenPatterns = [
      /\.git\//,
      /\.vscode\//,
      /\.idea\//,
      /node_modules\//,
      /tests?\//,
      /\.test\.js$/,
      /\.spec\.js$/
    ];

    function checkDirectory(dir) {
      const items = fs.readdirSync(dir);

      for (const item of items) {
        const fullPath = path.join(dir, item);
        const relativePath = path.relative(bundledPath, fullPath).replace(/\\/g, '/');

        // Check if path matches any forbidden pattern
        for (const pattern of forbiddenPatterns) {
          if (pattern.test(relativePath)) {
            throw new Error(`Forbidden file/directory found in bundle: ${relativePath}`);
          }
        }

        const stat = fs.statSync(fullPath);
        if (stat.isDirectory()) {
          checkDirectory(fullPath);
        }
      }
    }

    if (fs.existsSync(bundledPath)) {
      checkDirectory(bundledPath);
    }
  });

  test('bundled/ directory contains only necessary framework files', () => {
    // Bundle should NOT contain operational directories from active projects
    const forbiddenDirs = [
      'devforgeai/qa',
      'devforgeai/adrs',
      '.ai_docs'
    ];

    for (const dir of forbiddenDirs) {
      const fullPath = path.join(bundledPath, dir);
      expect(fs.existsSync(fullPath)).toBe(false);
    }
  });
});

describe('Bundle version metadata', () => {
  const rootPath = path.join(__dirname, '../../..');
  const bundledPath = path.join(rootPath, 'bundled');

  test('bundled/version.json exists with version information', () => {
    const versionPath = path.join(bundledPath, 'version.json');
    expect(fs.existsSync(versionPath)).toBe(true);

    if (fs.existsSync(versionPath)) {
      const content = fs.readFileSync(versionPath, 'utf8');
      const versionData = JSON.parse(content);

      expect(versionData).toHaveProperty('version');
      expect(versionData.version).toMatch(/^\d+\.\d+\.\d+/);
    }
  });

  test('bundled version matches package.json version', () => {
    const packagePath = path.join(rootPath, 'package.json');
    const versionPath = path.join(bundledPath, 'version.json');

    if (fs.existsSync(packagePath) && fs.existsSync(versionPath)) {
      const packageJson = JSON.parse(fs.readFileSync(packagePath, 'utf8'));
      const versionData = JSON.parse(fs.readFileSync(versionPath, 'utf8'));

      expect(versionData.version).toBe(packageJson.version);
    }
  });
});
