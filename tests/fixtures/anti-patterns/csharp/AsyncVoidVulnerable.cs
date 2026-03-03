/**
 * Test Fixture: Async Void Vulnerable Patterns (C#)
 *
 * This file contains async void methods that are NOT event handlers.
 * Expected detections: >=2 violations for AP-002
 * Rule ID: AP-002
 * Severity: HIGH (warning)
 */

using System;
using System.Threading.Tasks;

namespace TestFixtures.AntiPatterns
{
    public class AsyncVoidVulnerable
    {
        // VULNERABLE: async void method (not an event handler)
        public async void ProcessDataAsync()
        {
            await Task.Delay(100);
            Console.WriteLine("Processing complete");
        }

        // VULNERABLE: another async void method
        public async void SendNotificationAsync(string message)
        {
            await Task.Delay(50);
            Console.WriteLine($"Notification sent: {message}");
        }

        // SAFE: async Task (correct pattern)
        public async Task ProcessDataSafeAsync()
        {
            await Task.Delay(100);
            Console.WriteLine("Processing complete safely");
        }

        // SAFE: sync void method (not async)
        public void SyncMethod()
        {
            Console.WriteLine("Sync operation");
        }
    }
}
