/**
 * Test Fixture: Console Log Vulnerable Patterns (TypeScript)
 *
 * This file contains console.log statements in production code.
 * Expected detections: >=3 violations for AP-003
 * Rule ID: AP-003
 * Severity: MEDIUM (info)
 */

interface User {
  id: number;
  name: string;
  email: string;
}

function processUserData(user: User): User {
  console.log("Processing user:", user); // VULNERABLE: Debug log

  if (!user.email) {
    console.warn("User has no email"); // VULNERABLE: Should use proper logging
  }

  const result = transformUser(user);
  console.log(`Transformed result: ${JSON.stringify(result)}`); // VULNERABLE: Debug log

  return result;
}

function transformUser(user: User): User {
  console.debug("Transforming user"); // VULNERABLE: Debug log
  return { ...user, name: user.name.toUpperCase() };
}

function handleError(error: Error): void {
  console.error("An error occurred:", error); // VULNERABLE: Should use logging service
}

export { processUserData, transformUser, handleError };
