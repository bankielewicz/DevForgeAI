#!/usr/bin/env node
/**
 * Version Validation Script
 * Story: STORY-067 - NPM Registry Publishing Workflow
 *
 * Validates that a Git tag matches the version in package.json
 * Enforces semver format: v{major}.{minor}.{patch}[-prerelease]
 *
 * Usage: node validate-version.js <tag>
 * Exit Codes:
 *   0 - Validation successful
 *   1 - Validation failed
 */

const fs = require('fs');
const path = require('path');

// Constants
const SEMVER_PATTERN = /^v\d+\.\d+\.\d+(-[a-z0-9.]+)?$/;

/**
 * Strip 'v' prefix from version tag
 * @param {string} tag - Version tag (e.g., 'v1.0.0')
 * @returns {string} Version without 'v' prefix (e.g., '1.0.0')
 */
function stripVPrefix(tag) {
  return tag.replace(/^v/, '');
}

/**
 * Validate if tag matches semver pattern
 * @param {string} tag - Version tag to validate
 * @returns {boolean} True if tag matches semver pattern
 */
function isValidSemverTag(tag) {
  return SEMVER_PATTERN.test(tag);
}

/**
 * Check if version tag matches package.json version
 * @param {string} tag - Git tag (e.g., 'v1.0.0')
 * @param {string} packageVersion - Version from package.json (e.g., '1.0.0')
 * @returns {boolean} True if versions match
 */
function checkVersionMatch(tag, packageVersion) {
  const tagVersion = stripVPrefix(tag);
  return tagVersion === packageVersion;
}

/**
 * Validate tag is not empty
 * @param {string} tag - Git tag to validate
 * @returns {object|null} Error object or null if valid
 */
function validateTagNotEmpty(tag) {
  if (!tag || tag.trim() === '') {
    return { valid: false, error: 'Tag is required and cannot be empty' };
  }
  return null;
}

/**
 * Validate package.json exists
 * @param {object} packageJson - Parsed package.json content
 * @returns {object|null} Error object or null if valid
 */
function validatePackageJsonExists(packageJson) {
  if (!packageJson) {
    return { valid: false, error: 'package.json not found or invalid' };
  }
  return null;
}

/**
 * Validate tag format matches semver
 * @param {string} tag - Git tag to validate
 * @returns {object|null} Error object or null if valid
 */
function validateTagFormat(tag) {
  if (!SEMVER_PATTERN.test(tag)) {
    return {
      valid: false,
      error: `Invalid tag format: "${tag}". Must match vX.Y.Z or vX.Y.Z-prerelease (e.g., v1.0.0, v2.1.0-beta.1)`
    };
  }
  return null;
}

/**
 * Validate package.json has version field
 * @param {object} packageJson - Parsed package.json content
 * @returns {object|null} Error object or null if valid
 */
function validatePackageVersion(packageJson) {
  if (!packageJson.version) {
    return { valid: false, error: 'Missing version field in package.json' };
  }
  return null;
}

/**
 * Validate tag version matches package.json version
 * @param {string} tag - Git tag (e.g., 'v1.0.0')
 * @param {string} packageVersion - Version from package.json (e.g., '1.0.0')
 * @returns {object|null} Error object or null if valid
 */
function validateVersionMatch(tag, packageVersion) {
  if (!checkVersionMatch(tag, packageVersion)) {
    const tagVersion = stripVPrefix(tag);
    return {
      valid: false,
      error: `Version mismatch: tag is "${tagVersion}" but package.json is "${packageVersion}"`
    };
  }
  return null;
}

/**
 * Validate version tag format and matching
 * @param {string} tag - Git tag to validate
 * @param {object} packageJson - Parsed package.json content
 * @returns {object} Validation result { valid: boolean, error?: string }
 */
function validate(tag, packageJson) {
  // Run validations in sequence - return first error encountered
  let error;

  error = validateTagNotEmpty(tag);
  if (error) return error;

  error = validatePackageJsonExists(packageJson);
  if (error) return error;

  error = validateTagFormat(tag);
  if (error) return error;

  error = validatePackageVersion(packageJson);
  if (error) return error;

  error = validateVersionMatch(tag, packageJson.version);
  if (error) return error;

  return { valid: true };
}

/**
 * Main execution function
 */
function main() {
  // Get tag from command-line arguments or environment variable
  const tag = process.argv[2] || process.env.GITHUB_REF?.replace('refs/tags/', '');

  if (!tag) {
    console.error('Error: No tag provided');
    console.error('Usage: node validate-version.js <tag>');
    process.exit(1);
  }

  // Read package.json
  const packageJsonPath = path.resolve(process.cwd(), 'package.json');

  if (!fs.existsSync(packageJsonPath)) {
    console.error('Error: package.json not found in current directory');
    process.exit(1);
  }

  let packageJson;
  try {
    const packageJsonContent = fs.readFileSync(packageJsonPath, 'utf8');
    packageJson = JSON.parse(packageJsonContent);
  } catch (error) {
    console.error(`Error reading package.json: ${error.message}`);
    process.exit(1);
  }

  // Validate tag
  const result = validate(tag, packageJson);

  if (result.valid) {
    console.log(`✓ Version validation passed: ${tag} matches package.json ${packageJson.version}`);
    process.exit(0);
  } else {
    console.error(`✗ Version validation failed: ${result.error}`);
    process.exit(1);
  }
}

// Export functions for testing
module.exports = {
  stripVPrefix,
  extractVersion: stripVPrefix, // Alias for backward compatibility
  isValidSemverTag,
  checkVersionMatch,
  validate,
  main // Export main for testing
};

// Run main if executed directly
if (require.main === module) {
  main();
}
