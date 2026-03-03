/**
 * Test Fixture: Long Method Vulnerable Pattern (C#)
 *
 * This file contains a method with many statements.
 * Expected detections: >=1 violation for AP-005
 * Rule ID: AP-005
 * Severity: MEDIUM (info)
 */

using System;
using System.Collections.Generic;

namespace TestFixtures.AntiPatterns
{
    public class LongMethodVulnerable
    {
        // VULNERABLE: Method with 15+ statements
        public Dictionary<string, object> VeryLongProcessingMethod(Dictionary<string, object> data)
        {
            var result = new Dictionary<string, object>();
            var errors = new List<string>();
            var warnings = new List<string>();

            if (data == null)
            {
                errors.Add("Data is empty");
                result["status"] = "error";
                result["errors"] = errors;
                return result;
            }

            var userId = data.GetValueOrDefault("userId");
            var username = data.GetValueOrDefault("username");
            var email = data.GetValueOrDefault("email");
            var password = data.GetValueOrDefault("password");
            var firstName = data.GetValueOrDefault("firstName");
            var lastName = data.GetValueOrDefault("lastName");

            if (userId == null)
            {
                errors.Add("Missing userId");
            }

            if (username == null)
            {
                errors.Add("Missing username");
            }

            if (email == null)
            {
                errors.Add("Missing email");
            }

            if (password == null)
            {
                errors.Add("Missing password");
            }

            result["userId"] = userId;
            result["username"] = username?.ToString()?.ToLower();
            result["email"] = email?.ToString()?.ToLower();
            result["firstName"] = firstName;
            result["lastName"] = lastName;
            result["status"] = "success";
            result["warnings"] = warnings;

            return result;
        }
    }
}
