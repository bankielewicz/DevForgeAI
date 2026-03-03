/*
 * Test Fixture: SQL Injection Vulnerable Patterns (C#)
 *
 * This file contains SQL injection vulnerability patterns for C# that MUST be detected.
 *
 * Expected detections: ≥3 violations
 * Rule ID: SEC-001
 * Severity: CRITICAL
 *
 * NOTE: Stub implementation - full patterns added during Phase 03 (Green)
 */

using System;
using System.Data.SqlClient;

namespace Security.Fixtures
{
    public class SqlInjectionVulnerable
    {
        // Pattern 1: String interpolation in SQL
        public void GetUserById_StringInterpolation(int userId)
        {
            // VULNERABLE: SEC-001 should detect this
            string query = $"SELECT * FROM Users WHERE Id = {userId}";

            using (var connection = new SqlConnection("..."))
            {
                var command = new SqlCommand(query, connection);
                connection.Open();
                command.ExecuteReader();
            }
        }

        // Pattern 2: String concatenation in SQL
        public void GetUserByUsername_Concatenation(string username)
        {
            // VULNERABLE: SEC-001 should detect this
            string query = "SELECT * FROM Users WHERE Username = '" + username + "'";

            using (var connection = new SqlConnection("..."))
            {
                var command = new SqlCommand(query, connection);
                connection.Open();
                command.ExecuteReader();
            }
        }

        // Additional patterns to be added in Phase 03
    }
}
