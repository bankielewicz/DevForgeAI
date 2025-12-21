/**
 * Test Fixture: Long Method Vulnerable Pattern (TypeScript)
 *
 * This file contains a function with many statements.
 * Expected detections: >=1 violation for AP-005
 * Rule ID: AP-005
 * Severity: MEDIUM (info)
 */

interface UserData {
  userId?: number;
  username?: string;
  email?: string;
  password?: string;
  firstName?: string;
  lastName?: string;
}

// VULNERABLE: Function with 15+ statements
export function veryLongProcessingFunction(data: UserData): Record<string, any> {
  const result: Record<string, any> = {};
  const errors: string[] = [];
  const warnings: string[] = [];

  if (!data) {
    errors.push("Data is empty");
    return { status: "error", errors };
  }

  const userId = data.userId;
  const username = data.username;
  const email = data.email;
  const password = data.password;
  const firstName = data.firstName;
  const lastName = data.lastName;

  if (!userId) {
    errors.push("Missing userId");
  }

  if (!username) {
    errors.push("Missing username");
  }

  if (!email) {
    errors.push("Missing email");
  }

  if (!password) {
    errors.push("Missing password");
  }

  result.userId = userId;
  result.username = username?.toLowerCase();
  result.email = email?.toLowerCase();
  result.firstName = firstName;
  result.lastName = lastName;
  result.status = "success";
  result.warnings = warnings;

  return result;
}
