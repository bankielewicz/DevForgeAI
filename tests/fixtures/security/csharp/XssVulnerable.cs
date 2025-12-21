/*
 * Test Fixture: XSS Vulnerable Patterns (C#)
 *
 * This file contains XSS vulnerability patterns for C# that MUST be detected.
 *
 * Expected detections: ≥2 violations
 * Rule ID: SEC-002
 * Severity: CRITICAL
 *
 * NOTE: Stub implementation - full patterns added during Phase 03 (Green)
 */

using System;
using System.Web;

namespace Security.Fixtures
{
    public class XssVulnerable
    {
        // Pattern 1: Response.Write without encoding
        public void RenderUserInput_ResponseWrite(string userInput)
        {
            // VULNERABLE: SEC-002 should detect this
            HttpContext.Current.Response.Write("<div>" + userInput + "</div>");
        }

        // Pattern 2: Direct string concatenation in HTML
        public string BuildHtml_NoEncoding(string userName)
        {
            // VULNERABLE: SEC-002 should detect this
            return $"<h1>Welcome, {userName}!</h1>";
        }

        // Additional patterns to be added in Phase 03
    }
}
