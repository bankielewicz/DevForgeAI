/**
 * Test Fixture: Excessive Parameters Vulnerable Pattern (TypeScript)
 *
 * This file contains functions with >5 parameters.
 * Expected detections: >=1 violation for AP-008
 * Rule ID: AP-008
 * Severity: MEDIUM (info)
 */

// VULNERABLE: 7 parameters
export function createUser(
  userId: number,
  username: string,
  email: string,
  password: string,
  firstName: string,
  lastName: string,
  phoneNumber: string
): void {
  // Implementation
}

// SAFE: 5 parameters is acceptable
export function calculate(a: number, b: number, c: number, d: number, e: number): number {
  return a + b + c + d + e;
}
