/**
 * Test Fixture: God Object Vulnerable Pattern (C#)
 *
 * This class has too many public methods (10+), indicating a god object.
 * Expected detections: >=1 violation for AP-001
 * Rule ID: AP-001
 * Severity: HIGH (warning)
 */

using System;

namespace TestFixtures.AntiPatterns
{
    public class GodObjectVulnerable
    {
        private string _data;

        public void Method01_ProcessInput() { }
        public void Method02_ValidateData() { }
        public void Method03_TransformData() { }
        public void Method04_SaveToDatabase() { }
        public void Method05_LoadFromDatabase() { }
        public void Method06_SendNotification() { }
        public void Method07_GenerateReport() { }
        public void Method08_ExportToCsv() { }
        public void Method09_ExportToJson() { }
        public void Method10_CalculateMetrics() { }
        public void Method11_AggregateResults() { }
        public void Method12_FilterItems() { }
    }
}
