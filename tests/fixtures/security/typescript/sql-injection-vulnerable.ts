/*
 * Test Fixture: SQL Injection Vulnerable Patterns (TypeScript)
 *
 * This file contains SQL injection vulnerability patterns for TypeScript that MUST be detected.
 *
 * Expected detections: ≥3 violations
 * Rule ID: SEC-001
 * Severity: CRITICAL
 *
 * NOTE: Stub implementation - full patterns added during Phase 03 (Green)
 */

import { Client } from 'pg';

// Pattern 1: Template literal in SQL
async function getUserById_TemplateLiteral(userId: number) {
    const client = new Client();
    await client.connect();

    // VULNERABLE: SEC-001 should detect this
    const query = `SELECT * FROM users WHERE id = ${userId}`;
    const result = await client.query(query);

    await client.end();
    return result.rows;
}

// Pattern 2: String concatenation in SQL
async function getUserByUsername_Concatenation(username: string) {
    const client = new Client();
    await client.connect();

    // VULNERABLE: SEC-001 should detect this
    const query = "SELECT * FROM users WHERE username = '" + username + "'";
    const result = await client.query(query);

    await client.end();
    return result.rows;
}

// Additional patterns to be added in Phase 03
