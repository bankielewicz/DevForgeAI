/**
 * STORY-066: NPM Package Creation & Structure
 * Unit Tests: package.json Validation
 *
 * Tests AC#1: Valid package.json with complete metadata
 * Tests AC#3: All runtime dependencies declared
 *
 * Expected Result: ALL TESTS SHOULD FAIL (TDD Red Phase)
 * Implementation: bin/devforgeai.js and package.json do not exist yet
 */

const fs = require('fs');
const path = require('path');

describe('AC#1: Valid package.json with complete metadata', () => {
  let packageJson;
  const packageJsonPath = path.join(__dirname, '../../../package.json');

  beforeAll(() => {
    // Attempt to read package.json (will fail in Red phase)
    try {
      const content = fs.readFileSync(packageJsonPath, 'utf8');
      packageJson = JSON.parse(content);
    } catch (error) {
      packageJson = null;
    }
  });

  describe('CONF-001: Required NPM metadata fields', () => {
    test('package.json file exists', () => {
      expect(fs.existsSync(packageJsonPath)).toBe(true);
    });

    test('package.json is valid JSON', () => {
      expect(packageJson).not.toBeNull();
      expect(typeof packageJson).toBe('object');
    });

    test('name field is "devforgeai"', () => {
      expect(packageJson).toHaveProperty('name');
      expect(packageJson.name).toBe('devforgeai');
    });

    test('version follows semantic versioning', () => {
      expect(packageJson).toHaveProperty('version');
      // Regex: MAJOR.MINOR.PATCH or MAJOR.MINOR.PATCH-prerelease
      const semverRegex = /^\d+\.\d+\.\d+(-[a-z0-9.]+)?$/;
      expect(packageJson.version).toMatch(semverRegex);
    });

    test('description field exists and is at least 50 characters', () => {
      expect(packageJson).toHaveProperty('description');
      expect(typeof packageJson.description).toBe('string');
      expect(packageJson.description.length).toBeGreaterThanOrEqual(50);
    });

    test('keywords array includes required terms', () => {
      expect(packageJson).toHaveProperty('keywords');
      expect(Array.isArray(packageJson.keywords)).toBe(true);

      const requiredKeywords = ['ai', 'development', 'framework', 'spec-driven', 'claude'];
      requiredKeywords.forEach(keyword => {
        expect(packageJson.keywords).toContain(keyword);
      });
    });

    test('author field is present', () => {
      expect(packageJson).toHaveProperty('author');
      expect(typeof packageJson.author).toBe('string');
      expect(packageJson.author.length).toBeGreaterThan(0);
    });

    test('license is MIT', () => {
      expect(packageJson).toHaveProperty('license');
      expect(packageJson.license).toBe('MIT');
    });

    test('repository object with type and url', () => {
      expect(packageJson).toHaveProperty('repository');
      expect(typeof packageJson.repository).toBe('object');
      expect(packageJson.repository.type).toBe('git');
      expect(packageJson.repository.url).toMatch(/github\.com/);
    });

    test('bugs object with issue tracking URL', () => {
      expect(packageJson).toHaveProperty('bugs');
      expect(typeof packageJson.bugs).toBe('object');
      expect(packageJson.bugs.url).toMatch(/github\.com.*\/issues/);
    });

    test('homepage URL points to documentation', () => {
      expect(packageJson).toHaveProperty('homepage');
      expect(typeof packageJson.homepage).toBe('string');
      expect(packageJson.homepage).toMatch(/^https?:\/\//);
    });
  });

  describe('BR-001: Package name validation', () => {
    test('package name is lowercase, no spaces, NPM-valid', () => {
      expect(packageJson).toHaveProperty('name');
      // Pattern: starts with letter, contains only lowercase letters, numbers, hyphens
      const npmNameRegex = /^[a-z][a-z0-9-]*$/;
      expect(packageJson.name).toMatch(npmNameRegex);
    });
  });
});

describe('AC#2: Bin entry point registered for global CLI', () => {
  let packageJson;
  const packageJsonPath = path.join(__dirname, '../../../package.json');

  beforeAll(() => {
    try {
      const content = fs.readFileSync(packageJsonPath, 'utf8');
      packageJson = JSON.parse(content);
    } catch (error) {
      packageJson = null;
    }
  });

  describe('CONF-004: Bin entry point configuration', () => {
    test('bin field exists in package.json', () => {
      expect(packageJson).toHaveProperty('bin');
      expect(typeof packageJson.bin).toBe('object');
    });

    test('bindevforgeai maps to entry point file', () => {
      expect(packageJson.bin).toHaveProperty('devforgeai');
      expect(typeof packageJson.bindevforgeai).toBe('string');
    });

    test('bin entry point path uses forward slashes (cross-platform)', () => {
      const binPath = packageJson?.bin?devforgeai || '';
      expect(binPath).not.toContain('\\');
      expect(binPath).toMatch(/^bin\//);
    });

    test('bin entry point file exists', () => {
      const binPath = packageJson?.bin?devforgeai;
      if (binPath) {
        const fullPath = path.join(__dirname, '../../../', binPath);
        expect(fs.existsSync(fullPath)).toBe(true);
      } else {
        throw new Error('bindevforgeai not defined in package.json');
      }
    });

    test('bin entry point file is executable (has +x permissions on Unix)', () => {
      const binPath = packageJson?.bin?devforgeai;
      if (binPath) {
        const fullPath = path.join(__dirname, '../../../', binPath);
        if (fs.existsSync(fullPath)) {
          const stats = fs.statSync(fullPath);
          // Check if file has execute permissions (Unix-like systems)
          // On Windows, this test will pass as file system doesn't use +x
          if (process.platform !== 'win32') {
            const isExecutable = !!(stats.mode & fs.constants.S_IXUSR);
            expect(isExecutable).toBe(true);
          } else {
            // On Windows, just verify file exists
            expect(stats.isFile()).toBe(true);
          }
        }
      }
    });
  });

  describe('BR-003: Cross-platform path format', () => {
    test('bin path uses forward slashes (not backslashes)', () => {
      const binPath = packageJson?.bin?devforgeai || '';
      expect(binPath).not.toContain('\\');
      expect(binPath).toMatch(/\//); // Contains at least one forward slash
    });
  });
});

describe('AC#3: All runtime dependencies declared', () => {
  let packageJson;
  const packageJsonPath = path.join(__dirname, '../../../package.json');

  beforeAll(() => {
    try {
      const content = fs.readFileSync(packageJsonPath, 'utf8');
      packageJson = JSON.parse(content);
    } catch (error) {
      packageJson = null;
    }
  });

  describe('CONF-003: Engines field requirements', () => {
    test('engines field specifies Node.js >=18.0.0', () => {
      expect(packageJson).toHaveProperty('engines');
      expect(packageJson.engines).toHaveProperty('node');
      expect(packageJson.engines.node).toBe('>=18.0.0');
    });

    test('engines field specifies npm >=8.0.0', () => {
      expect(packageJson).toHaveProperty('engines');
      expect(packageJson.engines).toHaveProperty('npm');
      expect(packageJson.engines.npm).toBe('>=8.0.0');
    });
  });

  test('dependencies field is empty or missing (zero npm dependencies)', () => {
    if (packageJson.hasOwnProperty('dependencies')) {
      expect(Object.keys(packageJson.dependencies).length).toBe(0);
    } else {
      expect(packageJson.dependencies).toBeUndefined();
    }
  });

  test('devDependencies are separate from runtime dependencies', () => {
    // If devDependencies exist, they should not leak into dependencies
    if (packageJson.hasOwnProperty('devDependencies')) {
      expect(typeof packageJson.devDependencies).toBe('object');
    }

    // Ensure no runtime dependencies
    const runtimeDeps = packageJson?.dependencies || {};
    expect(Object.keys(runtimeDeps).length).toBe(0);
  });
});

describe('CONF-002: Version format validation', () => {
  let packageJson;
  const packageJsonPath = path.join(__dirname, '../../../package.json');

  beforeAll(() => {
    try {
      const content = fs.readFileSync(packageJsonPath, 'utf8');
      packageJson = JSON.parse(content);
    } catch (error) {
      packageJson = null;
    }
  });

  test('version matches semantic versioning regex', () => {
    expect(packageJson).toHaveProperty('version');
    // More strict regex matching MAJOR.MINOR.PATCH format
    const semverRegex = /^\d+\.\d+\.\d+(-[a-z0-9.]+)?$/;
    expect(packageJson.version).toMatch(semverRegex);
  });

  test('version parts are numeric (MAJOR.MINOR.PATCH)', () => {
    const version = packageJson?.version || '';
    const versionParts = version.split('-')[0].split('.'); // Remove prerelease suffix

    expect(versionParts.length).toBe(3);
    versionParts.forEach(part => {
      expect(parseInt(part, 10)).not.toBeNaN();
      expect(parseInt(part, 10)).toBeGreaterThanOrEqual(0);
    });
  });
});
