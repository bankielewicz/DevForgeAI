/**
 * Test Fixture: Magic Numbers Vulnerable Pattern (C#)
 *
 * This file contains hardcoded numeric literals.
 * Expected detections: >=2 violations for AP-004
 * Rule ID: AP-004
 * Severity: MEDIUM (info)
 */

using System;

namespace TestFixtures.AntiPatterns
{
    public class MagicNumbersVulnerable
    {
        public decimal CalculateDiscount(int quantity)
        {
            if (quantity > 50)  // VULNERABLE: Magic number
            {
                return 0.15m;  // VULNERABLE: Magic number
            }
            return 0m;
        }

        public void SetTimeout()
        {
            var timeout = 30000;  // VULNERABLE: Magic number
            var maxRetries = 5;   // VULNERABLE: Magic number
        }
    }
}
