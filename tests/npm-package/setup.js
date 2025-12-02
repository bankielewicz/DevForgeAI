/**
 * Jest Setup File for STORY-071 Tests
 *
 * Purpose:
 * - Configure global test utilities
 * - Mock external dependencies
 * - Setup custom matchers
 * - Configure test environment
 */

// Extend Jest matchers
expect.extend({
  toHaveBeenCalledBefore(received, expected) {
    const receivedCalls = received.mock.invocationCallOrder;
    const expectedCalls = expected.mock.invocationCallOrder;

    const pass =
      receivedCalls.length > 0 &&
      expectedCalls.length > 0 &&
      receivedCalls[0] < expectedCalls[0];

    if (pass) {
      return {
        message: () =>
          `expected ${received.getMockName()} not to be called before ${expected.getMockName()}`,
        pass: true,
      };
    } else {
      return {
        message: () =>
          `expected ${received.getMockName()} to be called before ${expected.getMockName()}`,
        pass: false,
      };
    }
  },
});

// Mock console methods to reduce noise during tests
global.console = {
  ...console,
  log: jest.fn(),
  debug: jest.fn(),
  info: jest.fn(),
  warn: jest.fn(),
  // Keep error for test failure debugging
  error: console.error,
};

// Mock process.exit to prevent tests from exiting
// Use jest.spyOn to avoid initialization issues
jest.spyOn(process, 'exit').mockImplementation((code) => {
  // Don't throw during Jest setup - only during actual test execution
  // This prevents hanging if Jest internally calls process.exit during init
  return undefined;
});

// Restore process.exit after all tests
afterAll(() => {
  jest.restoreAllMocks();
});

// Set default timeout for all tests
jest.setTimeout(10000); // 10 seconds

// Mock environment variables for consistent testing
process.env.NODE_ENV = 'test';
process.env.FORCE_COLOR = '0'; // Disable colors in tests by default

// Mock TTY for interactive prompt tests (STORY-071 requirement)
// Jest runs without TTY, but PromptService checks process.stdout.isTTY
// Apply before each test to persist through jest.restoreAllMocks()
const applyTTYMock = () => {
  Object.defineProperty(process.stdout, 'isTTY', {
    value: true,
    writable: true,
    configurable: true,
  });
  Object.defineProperty(process.stdin, 'isTTY', {
    value: true,
    writable: true,
    configurable: true,
  });
};

// Apply TTY mock at startup
applyTTYMock();

// Re-apply TTY mock before each test (restoreMocks undoes it)
beforeEach(() => {
  applyTTYMock();
});

// Clean up after each test
afterEach(() => {
  jest.clearAllMocks();
  // jest.restoreAllMocks() removed - conflicts with config restoreMocks: false and property mocks
});
