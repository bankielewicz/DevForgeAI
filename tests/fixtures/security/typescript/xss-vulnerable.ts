/*
 * Test Fixture: XSS Vulnerable Patterns (TypeScript)
 *
 * This file contains XSS vulnerability patterns for TypeScript that MUST be detected.
 *
 * Expected detections: ≥2 violations
 * Rule ID: SEC-002
 * Severity: CRITICAL
 *
 * NOTE: Stub implementation - full patterns added during Phase 03 (Green)
 */

// Pattern 1: innerHTML with user data
function renderUserComment_InnerHTML(comment: string) {
    const container = document.getElementById('comment-container');

    if (container) {
        // VULNERABLE: SEC-002 should detect this
        container.innerHTML = comment;
    }
}

// Pattern 2: Template literal with user data in HTML
function greetUser_TemplateLiteral(userName: string) {
    const greeting = document.createElement('div');

    // VULNERABLE: SEC-002 should detect this
    greeting.innerHTML = `<h1>Welcome, ${userName}!</h1>`;

    document.body.appendChild(greeting);
}

// Additional patterns to be added in Phase 03
