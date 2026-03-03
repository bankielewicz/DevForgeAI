/*
 * Test Fixture: Hardcoded Secrets Vulnerable Patterns (TypeScript)
 *
 * This file contains hardcoded secret patterns for TypeScript that MUST be detected.
 *
 * Expected detections: ≥3 violations
 * Rule ID: SEC-003
 * Severity: CRITICAL
 *
 * NOTE: Stub implementation - full patterns added during Phase 03 (Green)
 */

// Pattern 1: Hardcoded API key
const API_KEY = "sk-1234567890abcdef1234567890abcdef";

// Pattern 2: Hardcoded database password
const DB_CONFIG = {
    host: "localhost",
    user: "admin",
    password: "SuperSecret123!"  // VULNERABLE: SEC-003 should detect this
};

// Pattern 3: Hardcoded JWT secret
const JWT_SECRET = "my-super-secret-jwt-key-do-not-share";

async function fetchData() {
    // VULNERABLE: SEC-003 should detect hardcoded API key
    const response = await fetch("https://api.example.com/data", {
        headers: {
            "Authorization": `Bearer ${API_KEY}`
        }
    });

    return response.json();
}

// Additional patterns to be added in Phase 03
