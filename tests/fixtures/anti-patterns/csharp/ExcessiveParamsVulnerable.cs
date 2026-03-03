/**
 * Test Fixture: Excessive Parameters Vulnerable Pattern (C#)
 *
 * This file contains methods with >5 parameters.
 * Expected detections: >=1 violation for AP-008
 * Rule ID: AP-008
 * Severity: MEDIUM (info)
 */

using System;

namespace TestFixtures.AntiPatterns
{
    public class ExcessiveParamsVulnerable
    {
        // VULNERABLE: 7 parameters
        public void CreateUser(
            int userId,
            string username,
            string email,
            string password,
            string firstName,
            string lastName,
            string phoneNumber)
        {
            // Implementation
        }

        // SAFE: 5 parameters is acceptable
        public int Calculate(int a, int b, int c, int d, int e)
        {
            return a + b + c + d + e;
        }
    }
}
