/**
 * Test Fixture: Async Void Event Handler (C#)
 *
 * This file contains async void methods that ARE event handlers.
 * Expected detections: 0 violations (event handlers are allowed)
 * Rule ID: AP-002
 * Severity: N/A (should not trigger for event handlers)
 */

using System;
using System.Threading.Tasks;
using System.Windows.Forms;

namespace TestFixtures.AntiPatterns
{
    public class AsyncVoidEventHandler
    {
        // SAFE: Event handler pattern - async void is acceptable
        private async void OnButtonClick(object sender, EventArgs e)
        {
            await Task.Delay(100);
            Console.WriteLine("Button clicked");
        }

        // SAFE: Another event handler pattern
        private async void HandleFormLoad(object sender, EventArgs e)
        {
            await Task.Delay(100);
            Console.WriteLine("Form loaded");
        }

        // SAFE: Event handler with different naming
        private async void DataGrid_SelectionChanged(object sender, EventArgs e)
        {
            await Task.Delay(50);
            Console.WriteLine("Selection changed");
        }

        // SAFE: Custom event handler
        public async void OnCustomEvent(object sender, CustomEventArgs e)
        {
            await Task.Delay(50);
            Console.WriteLine("Custom event handled");
        }
    }

    public class CustomEventArgs : EventArgs
    {
        public string Message { get; set; }
    }
}
