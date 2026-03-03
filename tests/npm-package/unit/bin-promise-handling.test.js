/**
 * Tests for bin/devforgeai.js Promise handling (lines 29-34)
 * Uses mocking to ensure Promise code path is covered
 */

// Mock lib/cli before requiring bin
jest.mock('../../../lib/cli', () => {
  const originalModule = jest.requireActual('../../../lib/cli');
  return {
    ...originalModule,
    run: jest.fn()
  };
});

const binEntry = require('../../../bin/devforgeai');
const cli = require('../../../lib/cli');

process.env.NODE_ENV = 'test';

describe('bin/devforgeai.js - Promise Handling Coverage', () => {

  beforeEach(() => {
    cli.run.mockClear();
  });

  test('handles result that is a Promise (lines 29-31)', async () => {
    // Mock cli.run() to return a Promise
    const mockPromise = Promise.resolve(0);
    cli.run.mockReturnValue(mockPromise);

    const exitCode = await binEntry.main(['install', '/tmp/test']);

    expect(cli.run).toHaveBeenCalledWith(['install', '/tmp/test']);
    expect(exitCode).toBe(0);
  });

  test('awaits Promise and returns its resolved value', async () => {
    // Test that Promise is awaited correctly (lines 30-31)
    cli.run.mockReturnValue(Promise.resolve(5));

    const exitCode = await binEntry.main(['test']);

    expect(exitCode).toBe(5);
  });

  test('handles Promise that resolves to non-zero exit code', async () => {
    cli.run.mockReturnValue(Promise.resolve(1));

    const exitCode = await binEntry.main(['command']);

    expect(exitCode).toBe(1);
  });

  test('returns 0 when result is neither number nor Promise (line 34)', async () => {
    // Mock cli.run() to return something else (edge case)
    cli.run.mockReturnValue(undefined);

    const exitCode = await binEntry.main(['test']);

    expect(exitCode).toBe(0);
  });

  test('handles numeric return value directly (skips Promise check)', async () => {
    // When result is a number, lines 29-31 should be skipped
    cli.run.mockReturnValue(0);

    const exitCode = await binEntry.main(['--version']);

    expect(exitCode).toBe(0);
  });

});
