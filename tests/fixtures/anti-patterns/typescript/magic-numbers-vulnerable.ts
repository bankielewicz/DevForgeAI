/**
 * Test Fixture: Magic Numbers Vulnerable Pattern (TypeScript)
 *
 * This file contains hardcoded numeric literals.
 * Expected detections: >=2 violations for AP-004
 * Rule ID: AP-004
 * Severity: MEDIUM (info)
 */

export function calculateDiscount(quantity: number): number {
  if (quantity > 50) {  // VULNERABLE: Magic number
    return 0.15;  // VULNERABLE: Magic number
  }
  return 0;
}

export function setTimeout(): void {
  const timeout = 30000;  // VULNERABLE: Magic number
  const maxRetries = 5;   // VULNERABLE: Magic number
}
