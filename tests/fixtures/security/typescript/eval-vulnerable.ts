/*
 * Test Fixture: Eval/Exec Vulnerable Patterns (TypeScript)
 *
 * This file contains dynamic code execution patterns for TypeScript that MUST be detected.
 *
 * Expected detections: ≥2 violations
 * Rule ID: SEC-004
 * Severity: CRITICAL
 *
 * NOTE: Stub implementation - full patterns added during Phase 03 (Green)
 */

// Pattern 1: eval() with user input
function calculateExpression_Eval(expression: string): number {
    // VULNERABLE: SEC-004 should detect this
    return eval(expression);
}

// Pattern 2: new Function() with string
function createDynamicFunction_NewFunction(functionBody: string) {
    // VULNERABLE: SEC-004 should detect this
    const dynamicFunc = new Function('x', functionBody);
    return dynamicFunc;
}

// Additional patterns to be added in Phase 03
