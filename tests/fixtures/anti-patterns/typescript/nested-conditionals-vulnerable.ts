/**
 * Test Fixture: Nested Conditionals Vulnerable Pattern (TypeScript)
 *
 * This file contains deeply nested conditionals (4+ levels).
 * Expected detections: >=1 violation for AP-006
 * Rule ID: AP-006
 * Severity: MEDIUM (info)
 */

interface Entity {
  isValid?: boolean;
}

export function deeplyNestedLogic(
  user: Entity | null,
  order: Entity | null,
  payment: Entity | null,
  shipping: Entity | null
): string {
  // VULNERABLE: 4+ levels of nesting
  if (user) {
    if (order) {
      if (payment) {
        if (shipping) {
          return "Order processed";
        }
      }
    }
  }
  return "Failed";
}
