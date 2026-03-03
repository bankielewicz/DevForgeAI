/*
 * Test Fixture: Insecure Deserialization Vulnerable Patterns (C#)
 *
 * This file contains insecure deserialization patterns for C# that MUST be detected.
 *
 * Expected detections: ≥2 violations
 * Rule ID: SEC-005
 * Severity: CRITICAL
 *
 * NOTE: Stub implementation - full patterns added during Phase 03 (Green)
 */

using System;
using System.IO;
using System.Runtime.Serialization.Formatters.Binary;

namespace Security.Fixtures
{
    public class DeserializationVulnerable
    {
        // Pattern 1: BinaryFormatter.Deserialize()
        public object DeserializeWithBinaryFormatter(byte[] data)
        {
            // VULNERABLE: SEC-005 should detect this
            var formatter = new BinaryFormatter();

            using (var stream = new MemoryStream(data))
            {
                return formatter.Deserialize(stream);
            }
        }

        // Additional patterns to be added in Phase 03
    }
}
