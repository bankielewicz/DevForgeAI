/**
 * Jest Configuration for STORY-071: Wizard-Driven Interactive UI
 *
 * Test Pyramid:
 * - Unit tests: 70% (6 test files covering individual services)
 * - Integration tests: 20% (1 test file covering wizard flow)
 * - E2E tests: 10% (1 test file covering complete installation)
 *
 * Coverage Targets:
 * - Wizard services (unit): 95%+
 * - Wizard flow (integration): 85%+
 */

module.exports = {
  // Test Environment
  testEnvironment: 'node',

  // Root Directory (project root, not test directory)
  rootDir: '../..',

  // Test Match Patterns
  testMatch: [
    '<rootDir>/tests/npm-package/unit/**/*.test.js',
    '<rootDir>/tests/npm-package/integration/**/*.test.js',
    '<rootDir>/tests/npm-package/e2e/**/*.test.js',
  ],

  // Coverage Configuration
  collectCoverageFrom: [
    '<rootDir>/src/cli/wizard/**/*.js',
    '!<rootDir>/src/cli/wizard/**/*.test.js',
    '!**/node_modules/**',
  ],

  coverageThreshold: {
    global: {
      branches: 85,
      functions: 90,
      lines: 90,
      statements: 90,
    },
    '<rootDir>/src/cli/wizard/install-wizard.js': {
      branches: 95,
      functions: 95,
      lines: 95,
      statements: 95,
    },
    '<rootDir>/src/cli/wizard/prompt-service.js': {
      branches: 95,
      functions: 95,
      lines: 95,
      statements: 95,
    },
    '<rootDir>/src/cli/wizard/progress-service.js': {
      branches: 95,
      functions: 95,
      lines: 95,
      statements: 95,
    },
    '<rootDir>/src/cli/wizard/output-formatter.js': {
      branches: 95,
      functions: 95,
      lines: 95,
      statements: 95,
    },
    '<rootDir>/src/cli/wizard/signal-handler.js': {
      branches: 95,
      functions: 95,
      lines: 95,
      statements: 95,
    },
  },

  // Coverage Reporters
  coverageReporters: ['text', 'lcov', 'html', 'json'],

  // Coverage Directory
  coverageDirectory: '<rootDir>/tests/coverage/npm-package',

  // Setup Files
  setupFilesAfterEnv: ['<rootDir>/tests/npm-package/setup.js'],

  // Module Paths
  modulePaths: ['<rootDir>/src'],

  // Timeouts
  testTimeout: 30000, // 30 seconds for E2E tests

  // Verbose Output
  verbose: true,

  // Bail on Failure (TDD workflow)
  bail: false, // Run all tests to see complete failure report

  // Clear Mocks
  clearMocks: true,
  resetMocks: true,
  restoreMocks: false, // Disabled - conflicts with property mocks (TTY mocking)

  // Error on Deprecated
  errorOnDeprecated: true,
};
