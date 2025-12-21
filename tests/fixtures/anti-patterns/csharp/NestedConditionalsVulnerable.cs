/**
 * Test Fixture: Nested Conditionals Vulnerable Pattern (C#)
 *
 * This file contains deeply nested conditionals (4+ levels).
 * Expected detections: >=1 violation for AP-006
 * Rule ID: AP-006
 * Severity: MEDIUM (info)
 */

using System;

namespace TestFixtures.AntiPatterns
{
    public class NestedConditionalsVulnerable
    {
        public string DeeplyNestedLogic(object user, object order, object payment, object shipping)
        {
            // VULNERABLE: 4+ levels of nesting
            if (user != null)
            {
                if (order != null)
                {
                    if (payment != null)
                    {
                        if (shipping != null)
                        {
                            return "Order processed";
                        }
                    }
                }
            }
            return "Failed";
        }
    }
}
