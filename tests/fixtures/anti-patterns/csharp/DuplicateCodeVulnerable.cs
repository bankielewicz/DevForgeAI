/**
 * Test Fixture: Duplicate Code Vulnerable Pattern (C#)
 *
 * This file contains duplicated code blocks.
 * Expected detections: >=1 violation for AP-009
 * Rule ID: AP-009
 * Severity: HIGH (warning)
 */

using System;

namespace TestFixtures.AntiPatterns
{
    public class DuplicateCodeVulnerable
    {
        // VULNERABLE: Duplicated validation pattern
        public void ProcessUserA(dynamic user)
        {
            if (user == null)
                throw new ArgumentNullException(nameof(user));
            var id = user.Id;
            var name = user.Name;
            var email = user.Email;
            // Process user A
        }

        // VULNERABLE: Same pattern duplicated
        public void ProcessUserB(dynamic user)
        {
            if (user == null)
                throw new ArgumentNullException(nameof(user));
            var id = user.Id;
            var name = user.Name;
            var email = user.Email;
            // Process user B
        }
    }
}
