/**
 * Jest configuration for DevForgeAI NPM package tests
 * Runs from project root for proper coverage collection
 */

module.exports = {
  testEnvironment: 'node',
  rootDir: '.',
  testMatch: ['**/tests/npm-package/**/*.test.js'],
  setupFiles: ['<rootDir>/tests/npm-package/jest.setup.js'],
  coverageDirectory: 'tests/npm-package/coverage',
  collectCoverageFrom: [
    'bin/**/*.js',
    'lib/**/*.js',
    '!**/node_modules/**',
    '!**/tests/**'
  ],
  coverageThreshold: {
    global: {
      branches: 95,
      functions: 95,
      lines: 95,
      statements: 95
    }
  },
  verbose: true
};
