/**
 * Jest configuration for DevForgeAI tests
 * Runs from project root for proper coverage collection
 */

module.exports = {
  testEnvironment: 'node',
  rootDir: '.',
  testMatch: [
    '**/tests/npm-package/**/*.test.js',
    '**/tests/release/**/*.test.js',
    '**/tests/STORY-*/**/*.js'
  ],
  setupFiles: ['<rootDir>/tests/npm-package/jest.setup.js'],
  coverageDirectory: 'tests/coverage',
  collectCoverageFrom: [
    'bin/**/*.js',
    'lib/**/*.js',
    'src/**/*.js',
    'scripts/**/*.sh',
    '!**/node_modules/**',
    '!**/tests/**'
  ],
  coverageThreshold: {
    global: {
      branches: 80,
      functions: 80,
      lines: 80,
      statements: 80
    }
  },
  verbose: true
};
