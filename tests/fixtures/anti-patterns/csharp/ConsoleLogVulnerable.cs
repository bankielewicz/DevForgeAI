/**
 * Test Fixture: Console Log Vulnerable Pattern (C#)
 *
 * This file contains Console.WriteLine statements in production code.
 * Expected detections: >=2 violations for AP-003
 * Rule ID: AP-003
 * Severity: MEDIUM (info)
 */

using System;

namespace TestFixtures.AntiPatterns
{
    public class ConsoleLogVulnerable
    {
        public void ProcessData(object data)
        {
            Console.WriteLine("Processing data: " + data);  // VULNERABLE

            if (data == null)
            {
                Console.Error.WriteLine("Data is null");  // VULNERABLE
            }

            Console.Write("Done");  // VULNERABLE
        }
    }
}
