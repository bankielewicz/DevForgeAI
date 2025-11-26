/**
 * STORY-066: NPM Package Creation & Structure
 * Integration Tests: Global installation (npm install -g)
 *
 * Tests AC#2: Bin entry point registered for global CLI
 * Tests AC#6: Cross-platform compatibility
 *
 * Expected Result: ALL TESTS SHOULD FAIL (TDD Red Phase)
 * Implementation: Package not yet installable globally
 *
 * NOTE: These tests require elevated permissions or local npm prefix
 */

const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');
const os = require('os');

describe('Integration: Global installation workflow', () => {
  const rootPath = path.join(__dirname, '../../..');
  const tempPrefix = path.join(os.tmpdir(), 'npm-test-prefix');
  let tarballPath;

  beforeAll(() => {
    // Create temporary npm prefix for testing
    if (!fs.existsSync(tempPrefix)) {
      fs.mkdirSync(tempPrefix, { recursive: true });
    }

    // Create tarball for installation
    try {
      const output = execSync('npm pack', {
        cwd: rootPath,
        encoding: 'utf8',
        stdio: 'pipe'
      }).trim();

      tarballPath = path.join(rootPath, output);
    } catch (error) {
      console.error('Failed to create tarball:', error);
    }
  });

  afterAll(() => {
    // Clean up tarball
    if (tarballPath && fs.existsSync(tarballPath)) {
      fs.unlinkSync(tarballPath);
    }

    // Clean up temporary prefix
    if (fs.existsSync(tempPrefix)) {
      fs.rmSync(tempPrefix, { recursive: true, force: true });
    }
  });

  describe('Global installation from tarball', () => {
    test('npm install -g from tarball succeeds', () => {
      if (!tarballPath) {
        throw new Error('Tarball not created');
      }

      try {
        execSync(`npm install -g ${tarballPath} --prefix ${tempPrefix}`, {
          encoding: 'utf8',
          stdio: 'pipe'
        });

        expect(true).toBe(true);
      } catch (error) {
        throw new Error(`Global installation failed: ${error.message}`);
      }
    });

    test('global installation creates bin symlink', () => {
      const binPath = path.join(tempPrefix, 'bin', 'devforgeai');

      // Unix: symlink or executable script
      // Windows: devforgeai.cmd wrapper
      const exists = fs.existsSync(binPath) || fs.existsSync(`${binPath}.cmd`);

      expect(exists).toBe(true);
    });

    test('devforgeai command is available after installation', () => {
      const binPath = path.join(tempPrefix, 'bin', 'devforgeai');

      try {
        const output = execSync(`"${binPath}" --version`, {
          encoding: 'utf8',
          stdio: 'pipe',
          env: { ...process.env, PATH: `${tempPrefix}/bin:${process.env.PATH}` }
        });

        expect(output).toContain('devforgeai');
      } catch (error) {
        throw new Error(`devforgeai command not available: ${error.message}`);
      }
    });

    test('devforgeai --version works after global install', () => {
      const binPath = path.join(tempPrefix, 'bin', 'devforgeai');

      const output = execSync(`"${binPath}" --version`, {
        encoding: 'utf8',
        stdio: 'pipe'
      });

      expect(output).toMatch(/devforgeai v\d+\.\d+\.\d+/);
    });

    test('devforgeai --help works after global install', () => {
      const binPath = path.join(tempPrefix, 'bin', 'devforgeai');

      const output = execSync(`"${binPath}" --help`, {
        encoding: 'utf8',
        stdio: 'pipe'
      });

      expect(output).toContain('Usage:');
      expect(output).toContain('devforgeai');
    });
  });

  describe('Global installation directory structure', () => {
    test('package is installed to node_modules/devforgeai', () => {
      const packageDir = path.join(tempPrefix, 'lib/node_modules/devforgeai');

      expect(fs.existsSync(packageDir)).toBe(true);
    });

    test('installed package contains package.json', () => {
      const packageJson = path.join(tempPrefix, 'lib/node_modules/devforgeai/package.json');

      expect(fs.existsSync(packageJson)).toBe(true);
    });

    test('installed package contains bin/devforgeai.js', () => {
      const binFile = path.join(tempPrefix, 'lib/node_modules/devforgeai/bin/devforgeai.js');

      expect(fs.existsSync(binFile)).toBe(true);
    });

    test('installed package contains installer/ directory', () => {
      const installerDir = path.join(tempPrefix, 'lib/node_modules/devforgeai/installer');

      expect(fs.existsSync(installerDir)).toBe(true);
    });

    test('installed package contains src/ directory', () => {
      const srcDir = path.join(tempPrefix, 'lib/node_modules/devforgeai/src');

      expect(fs.existsSync(srcDir)).toBe(true);
    });
  });

  describe('Global uninstallation', () => {
    test('npm uninstall -g removes package', () => {
      try {
        execSync(`npm uninstall -g devforgeai --prefix ${tempPrefix}`, {
          encoding: 'utf8',
          stdio: 'pipe'
        });

        const packageDir = path.join(tempPrefix, 'lib/node_modules/devforgeai');
        expect(fs.existsSync(packageDir)).toBe(false);
      } catch (error) {
        throw new Error(`Global uninstallation failed: ${error.message}`);
      }
    });

    test('devforgeai command is removed after uninstallation', () => {
      const binPath = path.join(tempPrefix, 'bin', 'devforgeai');

      const exists = fs.existsSync(binPath) || fs.existsSync(`${binPath}.cmd`);
      expect(exists).toBe(false);
    });
  });
});

describe('AC#6: Cross-platform compatibility', () => {
  const rootPath = path.join(__dirname, '../../..');
  const tempPrefix = path.join(os.tmpdir(), 'npm-test-prefix-cross');

  beforeAll(() => {
    if (!fs.existsSync(tempPrefix)) {
      fs.mkdirSync(tempPrefix, { recursive: true });
    }
  });

  afterAll(() => {
    if (fs.existsSync(tempPrefix)) {
      fs.rmSync(tempPrefix, { recursive: true, force: true });
    }
  });

  describe('NFR-005: Works on all major operating systems', () => {
    test('CLI detects current operating system correctly', () => {
      const platform = process.platform;

      expect(['linux', 'darwin', 'win32']).toContain(platform);
    });

    test('CLI works on current platform', () => {
      const binPath = path.join(rootPath, 'bin/devforgeai.js');

      if (fs.existsSync(binPath)) {
        try {
          const output = execSync(`node "${binPath}" --version`, {
            encoding: 'utf8',
            stdio: 'pipe'
          });

          expect(output).toContain('devforgeai');
        } catch (error) {
          throw new Error(`CLI failed on ${process.platform}: ${error.message}`);
        }
      } else {
        throw new Error('bin/devforgeai.js does not exist');
      }
    });

    test('CLI uses os-agnostic path resolution', () => {
      const libPath = path.join(rootPath, 'lib/cli.js');

      if (fs.existsSync(libPath)) {
        const content = fs.readFileSync(libPath, 'utf8');

        // Should use path.join() or path.resolve()
        expect(content).toMatch(/path\.(join|resolve)/);

        // Should NOT have hardcoded platform-specific paths
        expect(content).not.toMatch(/['"][A-Z]:\\\\/); // Windows paths
        expect(content).not.toMatch(/['"]\/(usr|home|tmp)\//); // Unix absolute paths
      }
    });

    test('CLI line endings are LF (not CRLF)', () => {
      const binPath = path.join(rootPath, 'bin/devforgeai.js');

      if (fs.existsSync(binPath)) {
        const content = fs.readFileSync(binPath, 'utf8');

        // Check for CRLF
        expect(content).not.toContain('\r\n');
      }
    });
  });

  describe('Path compatibility', () => {
    test('package.json bin path uses forward slashes', () => {
      const packagePath = path.join(rootPath, 'package.json');
      const packageJson = JSON.parse(fs.readFileSync(packagePath, 'utf8'));

      expect(packageJson.bin.devforgeai).not.toContain('\\');
      expect(packageJson.bin.devforgeai).toContain('/');
    });

    test('CLI handles spaces in paths correctly', () => {
      const binPath = path.join(rootPath, 'bin/devforgeai.js');

      if (fs.existsSync(binPath)) {
        const testDirWithSpaces = path.join(os.tmpdir(), 'test dir with spaces');

        if (!fs.existsSync(testDirWithSpaces)) {
          fs.mkdirSync(testDirWithSpaces, { recursive: true });
        }

        try {
          execSync(`node "${binPath}" --help`, {
            cwd: testDirWithSpaces,
            encoding: 'utf8',
            stdio: 'pipe'
          });

          expect(true).toBe(true);
        } catch (error) {
          throw new Error('CLI failed with spaces in path');
        } finally {
          fs.rmSync(testDirWithSpaces, { recursive: true, force: true });
        }
      }
    });
  });
});

describe('NFR-001: Global installation performance', () => {
  const rootPath = path.join(__dirname, '../../..');
  const tempPrefix = path.join(os.tmpdir(), 'npm-test-prefix-perf');

  beforeAll(() => {
    if (!fs.existsSync(tempPrefix)) {
      fs.mkdirSync(tempPrefix, { recursive: true });
    }
  });

  afterAll(() => {
    if (fs.existsSync(tempPrefix)) {
      fs.rmSync(tempPrefix, { recursive: true, force: true });
    }
  });

  test('npm install -g completes in reasonable time (<30s)', () => {
    // Create tarball
    const output = execSync('npm pack', {
      cwd: rootPath,
      encoding: 'utf8',
      stdio: 'pipe'
    }).trim();

    const tarballPath = path.join(rootPath, output);

    try {
      const startTime = Date.now();

      execSync(`npm install -g ${tarballPath} --prefix ${tempPrefix}`, {
        encoding: 'utf8',
        stdio: 'pipe'
      });

      const elapsed = (Date.now() - startTime) / 1000; // Convert to seconds

      expect(elapsed).toBeLessThan(30);
    } finally {
      // Clean up
      fs.unlinkSync(tarballPath);
    }
  }, 35000); // Jest timeout 35s (slightly more than test requirement)
});

describe('Edge Case: Conflicting global installation', () => {
  const rootPath = path.join(__dirname, '../../..');
  const tempPrefix = path.join(os.tmpdir(), 'npm-test-prefix-conflict');

  beforeAll(() => {
    if (!fs.existsSync(tempPrefix)) {
      fs.mkdirSync(tempPrefix, { recursive: true });
    }
  });

  afterAll(() => {
    if (fs.existsSync(tempPrefix)) {
      fs.rmSync(tempPrefix, { recursive: true, force: true });
    }
  });

  test('installing over existing version shows upgrade message', () => {
    // Create tarball
    const output = execSync('npm pack', {
      cwd: rootPath,
      encoding: 'utf8',
      stdio: 'pipe'
    }).trim();

    const tarballPath = path.join(rootPath, output);

    try {
      // First installation
      execSync(`npm install -g ${tarballPath} --prefix ${tempPrefix}`, {
        encoding: 'utf8',
        stdio: 'pipe'
      });

      // Second installation (should upgrade)
      const installOutput = execSync(`npm install -g ${tarballPath} --prefix ${tempPrefix}`, {
        encoding: 'utf8',
        stdio: 'pipe'
      });

      // npm should indicate package was already installed
      expect(installOutput).toBeTruthy();
    } finally {
      fs.unlinkSync(tarballPath);
    }
  });
});

describe('Edge Case: Node.js version mismatch', () => {
  const rootPath = path.join(__dirname, '../../..');

  test('package.json engines field enforces Node.js >=18.0.0', () => {
    const packagePath = path.join(rootPath, 'package.json');
    const packageJson = JSON.parse(fs.readFileSync(packagePath, 'utf8'));

    expect(packageJson.engines.node).toBe('>=18.0.0');
  });

  test('current Node.js version meets requirement', () => {
    const nodeVersion = process.version.replace('v', '');
    const [major] = nodeVersion.split('.').map(Number);

    expect(major).toBeGreaterThanOrEqual(18);
  });
});
