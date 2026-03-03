/**
 * Test Fixture: Empty Catch Block Vulnerable Patterns (C#)
 *
 * This file contains empty catch blocks that swallow exceptions.
 * Expected detections: >=2 violations for AP-010
 * Rule ID: AP-010
 * Severity: HIGH (warning)
 */

using System;
using System.IO;

namespace TestFixtures.AntiPatterns
{
    public class EmptyCatchVulnerable
    {
        // VULNERABLE: Empty catch block
        public void ReadFileUnsafe(string path)
        {
            try
            {
                var content = File.ReadAllText(path);
                Console.WriteLine(content);
            }
            catch (Exception)
            {
                // Empty catch - exceptions silently swallowed
            }
        }

        // VULNERABLE: Another empty catch block
        public void ProcessDataUnsafe()
        {
            try
            {
                var result = DangerousOperation();
            }
            catch
            {
                // Empty catch without exception variable
            }
        }

        // SAFE: Catch block with logging
        public void ReadFileSafe(string path)
        {
            try
            {
                var content = File.ReadAllText(path);
                Console.WriteLine(content);
            }
            catch (Exception ex)
            {
                Console.WriteLine($"Error reading file: {ex.Message}");
                throw;
            }
        }

        // SAFE: Catch block with handling
        public void ProcessDataSafe()
        {
            try
            {
                var result = DangerousOperation();
            }
            catch (InvalidOperationException ex)
            {
                HandleError(ex);
            }
        }

        private int DangerousOperation() => throw new InvalidOperationException("Test");
        private void HandleError(Exception ex) => Console.WriteLine(ex.Message);
    }
}
