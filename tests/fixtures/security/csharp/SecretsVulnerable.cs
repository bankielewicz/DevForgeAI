/*
 * Test Fixture: Hardcoded Secrets Vulnerable Patterns (C#)
 *
 * This file contains hardcoded secret patterns for C# that MUST be detected.
 *
 * Expected detections: ≥3 violations
 * Rule ID: SEC-003
 * Severity: CRITICAL
 *
 * NOTE: Stub implementation - full patterns added during Phase 03 (Green)
 */

using System;
using System.Data.SqlClient;

namespace Security.Fixtures
{
    public class SecretsVulnerable
    {
        // Pattern 1: Hardcoded API key
        private const string ApiKey = "sk-1234567890abcdef1234567890abcdef";

        // Pattern 2: Hardcoded connection string with password
        private const string ConnectionString = "Server=localhost;Database=MyDb;User Id=admin;Password=P@ssw0rd123;";

        // Pattern 3: Hardcoded AWS credentials
        private const string AwsAccessKey = "AKIAIOSFODNN7EXAMPLE";
        private const string AwsSecretKey = "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY";

        public void ConnectToDatabase()
        {
            // VULNERABLE: SEC-003 should detect hardcoded connection string
            using (var connection = new SqlConnection(ConnectionString))
            {
                connection.Open();
            }
        }

        // Additional patterns to be added in Phase 03
    }
}
