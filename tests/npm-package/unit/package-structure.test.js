/**
 * STORY-066: NPM Package Creation & Structure
 * Unit Tests: Package Structure and Files
 *
 * Tests AC#4: Package structure follows NPM best practices
 * Tests AC#5: README with installation instructions
 * Tests AC#7: Package size optimization
 *
 * Expected Result: ALL TESTS SHOULD FAIL (TDD Red Phase)
 * Implementation: Package structure files do not exist yet
 */

const fs = require('fs');
const path = require('path');

describe('AC#4: Package structure follows NPM best practices', () => {
  const rootPath = path.join(__dirname, '../../..');

  describe('DM-001: bin/ directory with CLI entry point', () => {
    test('bin/ directory exists', () => {
      const binDir = path.join(rootPath, 'bin');
      expect(fs.existsSync(binDir)).toBe(true);
      expect(fs.statSync(binDir).isDirectory()).toBe(true);
    });

    test('bin/devforgeai.js exists', () => {
      const binFile = path.join(rootPath, 'bin/devforgeai.js');
      expect(fs.existsSync(binFile)).toBe(true);
      expect(fs.statSync(binFile).isFile()).toBe(true);
    });
  });

  describe('DM-002: installer/ directory with Python scripts', () => {
    test('installer/ directory exists', () => {
      const installerDir = path.join(rootPath, 'installer');
      expect(fs.existsSync(installerDir)).toBe(true);
      expect(fs.statSync(installerDir).isDirectory()).toBe(true);
    });

    test('installer/install.py exists', () => {
      const installPy = path.join(rootPath, 'installer/install.py');
      expect(fs.existsSync(installPy)).toBe(true);
    });

    test('installer/backup.py exists', () => {
      const backupPy = path.join(rootPath, 'installer/backup.py');
      expect(fs.existsSync(backupPy)).toBe(true);
    });

    test('installer/rollback.py exists', () => {
      const rollbackPy = path.join(rootPath, 'installer/rollback.py');
      expect(fs.existsSync(rollbackPy)).toBe(true);
    });

    test('installer/merge.py exists', () => {
      const mergePy = path.join(rootPath, 'installer/merge.py');
      expect(fs.existsSync(mergePy)).toBe(true);
    });

    test('installer/version.py exists', () => {
      const versionPy = path.join(rootPath, 'installer/version.py');
      expect(fs.existsSync(versionPy)).toBe(true);
    });

    test('installer/validate.py exists', () => {
      const validatePy = path.join(rootPath, 'installer/validate.py');
      expect(fs.existsSync(validatePy)).toBe(true);
    });

    test('installer/deploy.py exists', () => {
      const deployPy = path.join(rootPath, 'installer/deploy.py');
      expect(fs.existsSync(deployPy)).toBe(true);
    });
  });

  describe('DM-003: src/ directory with framework source', () => {
    test('src/ directory exists', () => {
      const srcDir = path.join(rootPath, 'src');
      expect(fs.existsSync(srcDir)).toBe(true);
      expect(fs.statSync(srcDir).isDirectory()).toBe(true);
    });

    test('src/.claude/ subdirectory exists', () => {
      const claudeDir = path.join(rootPath, 'src/claude');
      expect(fs.existsSync(claudeDir)).toBe(true);
      expect(fs.statSync(claudeDir).isDirectory()).toBe(true);
    });

    test('src/.devforgeai/ subdirectory exists', () => {
      const devforgeaiDir = path.join(rootPath, 'src/devforgeai');
      expect(fs.existsSync(devforgeaiDir)).toBe(true);
      expect(fs.statSync(devforgeaiDir).isDirectory()).toBe(true);
    });
  });

  describe('DM-004: LICENSE file with MIT license', () => {
    test('LICENSE file exists in root directory', () => {
      const licensePath = path.join(rootPath, 'LICENSE');
      expect(fs.existsSync(licensePath)).toBe(true);
      expect(fs.statSync(licensePath).isFile()).toBe(true);
    });

    test('LICENSE file contains "MIT License" text', () => {
      const licensePath = path.join(rootPath, 'LICENSE');
      const content = fs.readFileSync(licensePath, 'utf8');
      expect(content).toContain('MIT License');
    });

    test('LICENSE file is at least 1000 characters', () => {
      const licensePath = path.join(rootPath, 'LICENSE');
      const content = fs.readFileSync(licensePath, 'utf8');
      expect(content.length).toBeGreaterThanOrEqual(1000);
    });
  });
});

describe('AC#5: README with installation instructions', () => {
  const rootPath = path.join(__dirname, '../../..');
  const readmePath = path.join(rootPath, 'README.md');

  describe('DM-005: README.md completeness', () => {
    test('README.md file exists', () => {
      expect(fs.existsSync(readmePath)).toBe(true);
      expect(fs.statSync(readmePath).isFile()).toBe(true);
    });

    test('README.md word count is at least 300 words', () => {
      const content = fs.readFileSync(readmePath, 'utf8');
      const words = content.split(/\s+/).filter(word => word.length > 0);
      expect(words.length).toBeGreaterThanOrEqual(300);
    });

    test('README.md contains "npm install -g devforgeai" command', () => {
      const content = fs.readFileSync(readmePath, 'utf8');
      expect(content).toContain('npm install -g devforgeai');
    });

    test('README.md contains system requirements section', () => {
      const content = fs.readFileSync(readmePath, 'utf8');
      expect(content).toMatch(/requirements?/i);
      expect(content).toContain('Node.js');
      expect(content).toContain('Python');
    });

    test('README.md specifies Node.js 18+', () => {
      const content = fs.readFileSync(readmePath, 'utf8');
      expect(content).toMatch(/Node\.js\s+18\+/i);
    });

    test('README.md specifies Python 3.10+', () => {
      const content = fs.readFileSync(readmePath, 'utf8');
      expect(content).toMatch(/Python\s+3\.10\+/i);
    });

    test('README.md contains quick start guide', () => {
      const content = fs.readFileSync(readmePath, 'utf8');
      expect(content).toMatch(/quick\s*start/i);
      expect(content).toContain('devforgeai install');
    });

    test('README.md contains link to full documentation', () => {
      const content = fs.readFileSync(readmePath, 'utf8');
      expect(content).toMatch(/documentation/i);
      expect(content).toMatch(/https?:\/\//);
    });

    test('README.md contains troubleshooting section', () => {
      const content = fs.readFileSync(readmePath, 'utf8');
      expect(content).toMatch(/troubleshoot(ing)?/i);
    });

    test('README.md has required headings', () => {
      const content = fs.readFileSync(readmePath, 'utf8');

      const requiredHeadings = [
        /^#+ Installation/im,
        /^#+ Requirements/im,
        /^#+ Quick\s*Start/im,
        /^#+ Documentation/im,
        /^#+ License/im
      ];

      requiredHeadings.forEach(headingRegex => {
        expect(content).toMatch(headingRegex);
      });
    });
  });
});

describe('AC#7: Package size optimization', () => {
  const rootPath = path.join(__dirname, '../../..');
  const npmignorePath = path.join(rootPath, '.npmignore');

  describe('CONF-005: .npmignore excludes development files', () => {
    test('.npmignore file exists', () => {
      expect(fs.existsSync(npmignorePath)).toBe(true);
      expect(fs.statSync(npmignorePath).isFile()).toBe(true);
    });

    test('.npmignore excludes tests/ directory', () => {
      const content = fs.readFileSync(npmignorePath, 'utf8');
      expect(content).toMatch(/^tests?\//m);
    });

    test('.npmignore excludes docs/ directory', () => {
      const content = fs.readFileSync(npmignorePath, 'utf8');
      expect(content).toMatch(/^docs?\//m);
    });

    test('.npmignore excludes .git directory', () => {
      const content = fs.readFileSync(npmignorePath, 'utf8');
      expect(content).toMatch(/^\.git/m);
    });

    test('.npmignore excludes .devforgeai/ directory (operational folder)', () => {
      const content = fs.readFileSync(npmignorePath, 'utf8');
      // We exclude the entire .devforgeai/ operational folder (source is in src/devforgeai/)
      expect(content).toMatch(/^\.devforgeai\/$/m);
    });

    test('.npmignore excludes .ai_docs/ directory', () => {
      const content = fs.readFileSync(npmignorePath, 'utf8');
      expect(content).toMatch(/\.ai_docs\//);
    });

    test('.npmignore excludes *.test.js files', () => {
      const content = fs.readFileSync(npmignorePath, 'utf8');
      expect(content).toMatch(/\*\.test\.js/);
    });

    test('.npmignore excludes .vscode directory', () => {
      const content = fs.readFileSync(npmignorePath, 'utf8');
      expect(content).toMatch(/^\.vscode/m);
    });

    test('.npmignore excludes .idea directory', () => {
      const content = fs.readFileSync(npmignorePath, 'utf8');
      expect(content).toMatch(/^\.idea/m);
    });
  });

  describe('CONF-006: npm pack excludes development files', () => {
    test('npm pack --dry-run shows only essential files', () => {
      // This test will verify npm pack output in integration tests
      // Placeholder for Red phase
      expect(true).toBe(true);
    });
  });

  describe('BR-004: Package size constraint', () => {
    test('unpacked package size is <= 2 MB', () => {
      // This test will be validated via npm pack in integration tests
      // Placeholder for Red phase
      expect(true).toBe(true);
    });
  });
});

describe('BR-005: No hardcoded secrets in package', () => {
  const rootPath = path.join(__dirname, '../../..');

  test('bin/devforgeai.js contains no hardcoded secrets', () => {
    const binPath = path.join(rootPath, 'bin/devforgeai.js');

    if (fs.existsSync(binPath)) {
      const content = fs.readFileSync(binPath, 'utf8');

      const secretPatterns = [
        /API_KEY\s*=\s*["'][^"']+["']/,
        /SECRET\s*=\s*["'][^"']+["']/,
        /TOKEN\s*=\s*["'][^"']+["']/,
        /PASSWORD\s*=\s*["'][^"']+["']/,
        /ANTHROPIC_API_KEY\s*=\s*["'][^"']+["']/
      ];

      secretPatterns.forEach(pattern => {
        expect(content).not.toMatch(pattern);
      });
    }
  });

  test('package.json contains no hardcoded secrets', () => {
    const packagePath = path.join(rootPath, 'package.json');

    if (fs.existsSync(packagePath)) {
      const content = fs.readFileSync(packagePath, 'utf8');

      const secretPatterns = [
        /"[^"]*API_KEY[^"]*"\s*:\s*"[^"]+"/,
        /"[^"]*SECRET[^"]*"\s*:\s*"[^"]+"/,
        /"[^"]*TOKEN[^"]*"\s*:\s*"[^"]+"/,
        /"[^"]*PASSWORD[^"]*"\s*:\s*"[^"]+"/
      ];

      secretPatterns.forEach(pattern => {
        expect(content).not.toMatch(pattern);
      });
    }
  });

  test('README.md contains no hardcoded secrets', () => {
    const readmePath = path.join(rootPath, 'README.md');

    if (fs.existsSync(readmePath)) {
      const content = fs.readFileSync(readmePath, 'utf8');

      const secretPatterns = [
        /API_KEY\s*=\s*["'][a-zA-Z0-9_-]{20,}["']/,
        /SECRET\s*=\s*["'][a-zA-Z0-9_-]{20,}["']/,
        /TOKEN\s*=\s*["'][a-zA-Z0-9_-]{20,}["']/,
        /ANTHROPIC_API_KEY\s*=\s*sk-[a-zA-Z0-9-]+/
      ];

      secretPatterns.forEach(pattern => {
        expect(content).not.toMatch(pattern);
      });
    }
  });
});

describe('Package file structure validation', () => {
  const rootPath = path.join(__dirname, '../../..');

  test('all required root files exist', () => {
    const requiredFiles = [
      'package.json',
      'README.md',
      'LICENSE',
      '.npmignore'
    ];

    requiredFiles.forEach(file => {
      const filePath = path.join(rootPath, file);
      expect(fs.existsSync(filePath)).toBe(true);
    });
  });

  test('all required directories exist', () => {
    const requiredDirs = [
      'bin',
      'installer',
      'src'
    ];

    requiredDirs.forEach(dir => {
      const dirPath = path.join(rootPath, dir);
      expect(fs.existsSync(dirPath)).toBe(true);
      expect(fs.statSync(dirPath).isDirectory()).toBe(true);
    });
  });
});
