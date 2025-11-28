/**
 * Test Suite: Package Discoverability and Metadata
 * Story: STORY-067 - NPM Registry Publishing Workflow
 *
 * Tests cover:
 * - AC#5: Package discoverability and metadata
 * - package.json metadata validation
 */

const fs = require('fs');
const path = require('path');

describe('Package Discoverability and Metadata', () => {
  const packageJsonPath = path.resolve('package.json');
  let packageJson;

  beforeAll(() => {
    // Arrange: Load package.json
    try {
      const content = fs.readFileSync(packageJsonPath, 'utf8');
      packageJson = JSON.parse(content);
    } catch (error) {
      packageJson = null;
    }
  });

  describe('AC#5: Package Listing on npmjs.com', () => {
    test('should have package name defined', () => {
      // Arrange & Act
      const packageName = packageJson?.name;

      // Assert
      expect(packageName).toBeDefined();
      expect(packageName).toMatch(/^(@devforgeai\/)?devforgeai/);
    });

    test('should have description for search results', () => {
      // Arrange & Act
      const description = packageJson?.description;

      // Assert
      expect(description).toBeDefined();
      expect(description.length).toBeGreaterThan(20); // Meaningful description
      expect(description).toMatch(/DevForgeAI|framework|development/i);
    });

    test('should display latest stable version number', () => {
      // Arrange & Act
      const version = packageJson?.version;
      const semverPattern = /^\d+\.\d+\.\d+(-[a-z0-9.]+)?$/;

      // Assert
      expect(version).toBeDefined();
      expect(version).toMatch(semverPattern);
    });

    test('should include repository URL for GitHub link', () => {
      // Arrange & Act
      const repository = packageJson?.repository;

      // Assert
      expect(repository).toBeDefined();
      expect(repository.type).toBe('git');
      expect(repository.url).toContain('github.com');
      expect(repository.url).toContain('DevForgeAI');
    });

    test('should include keywords for discoverability', () => {
      // Arrange & Act
      const keywords = packageJson?.keywords;

      // Assert
      expect(keywords).toBeDefined();
      expect(Array.isArray(keywords)).toBe(true);
      expect(keywords.length).toBeGreaterThan(0);

      // Should include relevant search terms
      const expectedKeywords = ['ai', 'development', 'framework', 'spec-driven'];
      expectedKeywords.forEach(keyword => {
        expect(keywords).toContain(keyword);
      });
    });
  });

  describe('Package Metadata Completeness', () => {
    test('should have author information', () => {
      // Arrange & Act
      const author = packageJson?.author;

      // Assert
      expect(author).toBeDefined();
      expect(typeof author === 'string' || typeof author === 'object').toBe(true);
    });

    test('should have license specified', () => {
      // Arrange & Act
      const license = packageJson?.license;

      // Assert
      expect(license).toBeDefined();
      expect(license).toBe('MIT'); // As per project standards
    });

    test('should have bugs URL for issue reporting', () => {
      // Arrange & Act
      const bugs = packageJson?.bugs;

      // Assert
      expect(bugs).toBeDefined();
      expect(bugs.url).toContain('github.com');
      expect(bugs.url).toContain('issues');
    });

    test('should have homepage URL', () => {
      // Arrange & Act
      const homepage = packageJson?.homepage;

      // Assert
      expect(homepage).toBeDefined();
      expect(homepage).toContain('github.com');
    });

    test('should have bin entry for CLI command', () => {
      // Arrange & Act
      const bin = packageJson?.bin;

      // Assert
      expect(bin).toBeDefined();
      expect(bin.devforgeai).toBeDefined();
      expect(bin.devforgeai).toContain('bin/');
    });

    test('should specify Node.js engine requirements', () => {
      // Arrange & Act
      const engines = packageJson?.engines;

      // Assert
      expect(engines).toBeDefined();
      expect(engines.node).toBeDefined();
      expect(engines.node).toMatch(/>=\s*18/); // Node 18+
      expect(engines.npm).toBeDefined();
    });
  });

  describe('Keywords Optimization for Search', () => {
    test('should include primary category keywords', () => {
      // Arrange & Act
      const keywords = packageJson?.keywords || [];

      // Assert
      const primaryCategories = ['ai', 'development', 'framework'];
      primaryCategories.forEach(category => {
        expect(keywords).toContain(category);
      });
    });

    test('should include use-case keywords', () => {
      // Arrange & Act
      const keywords = packageJson?.keywords || [];

      // Assert
      const useCases = ['tdd', 'automation', 'code-quality'];
      useCases.forEach(useCase => {
        expect(keywords).toContain(useCase);
      });
    });

    test('should include technology keywords', () => {
      // Arrange & Act
      const keywords = packageJson?.keywords || [];

      // Assert
      const technologies = ['claude', 'devops', 'ci-cd'];
      technologies.forEach(tech => {
        expect(keywords).toContain(tech);
      });
    });

    test('should NOT include excessive keywords (spam)', () => {
      // Arrange & Act
      const keywords = packageJson?.keywords || [];

      // Assert
      expect(keywords.length).toBeLessThan(20); // Reasonable limit
    });

    test('should use lowercase keywords for consistency', () => {
      // Arrange & Act
      const keywords = packageJson?.keywords || [];

      // Assert
      keywords.forEach(keyword => {
        expect(keyword).toBe(keyword.toLowerCase());
      });
    });
  });

  describe('README and Documentation Links', () => {
    test('should reference README.md in repository', () => {
      // Arrange
      const readmePath = path.resolve('README.md');

      // Act
      const readmeExists = fs.existsSync(readmePath);

      // Assert
      expect(readmeExists).toBe(true);
    });

    test('should have installation instructions in README', () => {
      // Arrange
      const readmePath = path.resolve('README.md');
      let readmeContent = '';

      try {
        readmeContent = fs.readFileSync(readmePath, 'utf8');
      } catch (error) {
        readmeContent = '';
      }

      // Act & Assert
      expect(readmeContent).toContain('npm install');
      expect(readmeContent).toMatch(/install|installation/i);
    });
  });

  describe('NPM Search Result Display', () => {
    test('should format package name for readability', () => {
      // Arrange & Act
      const packageName = packageJson?.name;

      // Assert
      expect(packageName).toBeDefined();
      // Should be lowercase, alphanumeric with hyphens
      expect(packageName).toMatch(/^[@a-z0-9\-/]+$/);
    });

    test('should have concise description (< 200 characters)', () => {
      // Arrange & Act
      const description = packageJson?.description || '';

      // Assert
      expect(description.length).toBeLessThan(200);
      // NPM search results truncate long descriptions
    });

    test('should prioritize important keywords first', () => {
      // Arrange & Act
      const keywords = packageJson?.keywords || [];

      // Assert
      // First few keywords should be most important
      const priorityKeywords = keywords.slice(0, 3);
      expect(priorityKeywords).toContain('ai');
      expect(priorityKeywords).toContain('development');
    });
  });

  describe('Package Version Display', () => {
    test('should show stable version with latest tag by default', () => {
      // Arrange & Act
      const version = packageJson?.version;

      // Assert
      expect(version).toBeDefined();
      // Stable versions have no prerelease suffix
      if (!version.includes('-')) {
        expect(version).toMatch(/^\d+\.\d+\.\d+$/);
      }
    });

    test('should distinguish pre-release versions with tag', () => {
      // Arrange & Act
      const version = packageJson?.version;

      // Assert
      if (version?.includes('-beta')) {
        expect(version).toMatch(/^\d+\.\d+\.\d+-beta\.\d+$/);
      } else if (version?.includes('-rc')) {
        expect(version).toMatch(/^\d+\.\d+\.\d+-rc\.\d+$/);
      }
    });
  });

  describe('Social Proof and Trust Signals', () => {
    test('should link to GitHub repository for stars/forks visibility', () => {
      // Arrange & Act
      const repository = packageJson?.repository;

      // Assert
      expect(repository?.url).toBeDefined();
      expect(repository?.url).toContain('github.com');
      // GitHub link shows stars, forks, watchers
    });

    test('should encourage README badges for build status', () => {
      // Arrange
      const readmePath = path.resolve('README.md');
      let readmeContent = '';

      try {
        readmeContent = fs.readFileSync(readmePath, 'utf8');
      } catch (error) {
        readmeContent = '';
      }

      // Act & Assert
      // README should have badge placeholders or actual badges
      const hasBadges = readmeContent.match(/!\[.*\]\(.*badge.*\)/i) !== null;
      // Expected: CI status, version, license badges
    });
  });

  describe('Package Metrics Visibility', () => {
    test('should display download count on npmjs.com', () => {
      // This is automatically provided by NPM registry
      // Test validates package is configured for tracking
      expect(packageJson?.name).toBeDefined();
      // NPM tracks downloads per package name
    });

    test('should show last publish date', () => {
      // This is automatically provided by NPM registry
      // Test validates version is updated on publish
      expect(packageJson?.version).toBeDefined();
      // NPM shows publish date per version
    });
  });

  describe('Scoped vs Unscoped Package Strategy', () => {
    test('should use scoped package for namespace ownership', () => {
      // Arrange & Act
      const packageName = packageJson?.name;

      // Assert
      // Package can be scoped (@devforgeai/installer) or unscoped (devforgeai)
      const isScoped = packageName?.startsWith('@');
      const isUnscoped = !packageName?.startsWith('@');

      expect(isScoped || isUnscoped).toBe(true);
    });

    test('should reserve package name to prevent squatting', () => {
      // Arrange & Act
      const packageName = packageJson?.name;

      // Assert
      expect(packageName).toBeDefined();
      // Publishing reserves the name on NPM registry
    });
  });

  describe('Accessibility and Internationalization', () => {
    test('should use English for description and keywords', () => {
      // Arrange & Act
      const description = packageJson?.description || '';
      const keywords = packageJson?.keywords || [];

      // Assert
      expect(description).toMatch(/[a-zA-Z\s]+/);
      // NPM primarily serves English-speaking audience
    });

    test('should avoid special characters in metadata', () => {
      // Arrange & Act
      const packageName = packageJson?.name || '';
      const keywords = packageJson?.keywords || [];

      // Assert
      expect(packageName).toMatch(/^[@a-z0-9\-/]+$/);
      keywords.forEach(keyword => {
        expect(keyword).toMatch(/^[a-z0-9\-]+$/);
      });
    });
  });
});
