/**
 * Test Fixture: Duplicate Code Vulnerable Pattern (TypeScript)
 *
 * This file contains duplicated code blocks.
 * Expected detections: >=1 violation for AP-009
 * Rule ID: AP-009
 * Severity: HIGH (warning)
 */

interface User {
  id: number;
  name: string;
  email: string;
}

// VULNERABLE: Duplicated validation pattern
export function processUserA(user: User | null): void {
  if (!user) {
    throw new Error("User is required");
  }
  const id = user.id;
  const name = user.name;
  const email = user.email;
  // Process user A
}

// VULNERABLE: Same pattern duplicated
export function processUserB(user: User | null): void {
  if (!user) {
    throw new Error("User is required");
  }
  const id = user.id;
  const name = user.name;
  const email = user.email;
  // Process user B
}
