---
id: STORY-248
title: GUI Installer Template
type: feature
epic: EPIC-039
sprint: Backlog
priority: Medium
points: 8
depends_on: ["STORY-247"]
status: Backlog
created: 2025-01-06
updated: 2025-01-06
format_version: "2.5"
adr: ADR-009
---

# STORY-248: GUI Installer Template

## User Story

**As a** non-technical DevForgeAI user,
**I want** a graphical installer with point-and-click interface,
**So that** I can install the framework without using the terminal.

## Acceptance Criteria

### AC#1: Electron Application Launch

**Given** the user double-clicks the installer executable
**When** the Electron app launches
**Then** a native window opens with:
- Framework logo and branding
- Window size 800x600 (resizable)
- Professional styling (CSS framework)
**And** the window is centered on screen
**And** DevTools are disabled in production builds

### AC#2: Welcome Page

**Given** the Electron app has launched
**When** the welcome page is rendered
**Then** the page displays:
- Welcome message
- Framework version
- Installation requirements checklist
- "Next" button to continue
**And** requirements are checked automatically (disk space, permissions)
**And** warning icons shown for unmet requirements

### AC#3: Component Selection Page

**Given** the user clicks "Next" from welcome page
**When** the component selection page loads
**Then** checkboxes are displayed for:
- Core Framework (checked, disabled)
- CLI Tools
- Templates
- Examples
**And** each component shows:
  - Name and description
  - Installation size
  - Icon/image
**And** total selected size updates dynamically
**And** "Back" and "Next" buttons are available

### AC#4: Installation Path Picker

**Given** the component selection is complete
**When** the installation path page loads
**Then** a directory picker is shown with:
- Default path pre-filled
- "Browse" button to open native file dialog
- Path validation indicator (✓ valid, ✗ invalid)
**And** native directory picker opens on "Browse" click
**And** selected path is validated for write permissions
**And** invalid paths show error message below picker

### AC#5: Installation Progress Page

**Given** the user confirms installation settings
**When** installation begins
**Then** the progress page displays:
- Animated progress bar
- Current operation text ("Installing CLI Tools...")
- Overall percentage
- Cancel button (with confirmation dialog)
**And** progress updates in real-time via IPC
**And** detailed log is available via "Show Details" toggle
**And** errors are displayed in red with retry option

### AC#6: Completion Page

**Given** installation has completed successfully
**When** the completion page loads
**Then** the page shows:
- Success icon (✓ checkmark animation)
- "Installation Complete!" message
- Summary of installed components
- "Launch DevForgeAI" checkbox
- "Finish" button
**And** clicking "Finish" with checkbox launches CLI tool
**And** clicking "Finish" without checkbox closes installer

### AC#7: Error Handling Page

**Given** a fatal error occurs during installation
**When** the error is encountered
**Then** the error page displays:
- Error icon and message
- Technical details (collapsible)
- "Save Log" button
- "Retry" and "Exit" buttons
**And** "Save Log" opens save dialog for install.log
**And** "Retry" returns to previous step
**And** "Exit" closes installer with cleanup

### AC#8: Cross-Platform Native Look

**Given** the installer runs on Windows, macOS, or Linux
**When** the GUI is rendered
**Then** the interface uses native:
- Window controls (minimize, maximize, close)
- File picker dialogs
- System fonts
- Color scheme (light/dark mode detection)
**And** the design follows platform UI guidelines

## AC Verification Checklist

### AC#1 Verification (Launch)
- [ ] Window opens at 800x600
- [ ] Window is centered
- [ ] Logo and branding visible
- [ ] DevTools disabled in production

### AC#2 Verification (Welcome)
- [ ] Requirements checked automatically
- [ ] Unmet requirements show warnings
- [ ] Next button enabled only when ready
- [ ] Version displayed correctly

### AC#3 Verification (Component Selection)
- [ ] All 4 components listed
- [ ] Core Framework locked as selected
- [ ] Size calculations correct
- [ ] Back/Next navigation works

### AC#4 Verification (Path Picker)
- [ ] Browse button opens native dialog
- [ ] Path validation works
- [ ] Invalid paths show error
- [ ] Default path is reasonable

### AC#5 Verification (Progress)
- [ ] Progress bar animates smoothly
- [ ] Current operation text updates
- [ ] Cancel button works with confirmation
- [ ] Details toggle shows/hides log

### AC#6 Verification (Completion)
- [ ] Success animation plays
- [ ] Component summary accurate
- [ ] Launch checkbox works
- [ ] Finish button closes installer

### AC#7 Verification (Error Handling)
- [ ] Error details collapsible
- [ ] Save Log dialog works
- [ ] Retry returns to previous step
- [ ] Exit performs cleanup

### AC#8 Verification (Cross-Platform)
- [ ] Windows: follows Windows 11 design
- [ ] macOS: follows macOS Big Sur+ design
- [ ] Linux: follows GTK/Qt conventions
- [ ] Dark mode detection works

## Technical Specification

### Architecture

**Technology Stack:**
- **Framework:** Electron 28+
- **Frontend:** HTML5 + CSS3 + Vanilla JavaScript
- **IPC:** electron-IPC for main/renderer communication
- **Packaging:** electron-builder

**File Structure:**
```
installer-gui/
├── package.json
├── main.js              # Electron main process
├── preload.js           # Preload script (context bridge)
├── renderer/
│   ├── index.html
│   ├── styles.css
│   ├── app.js          # Main app logic
│   └── pages/
│       ├── welcome.html
│       ├── components.html
│       ├── path.html
│       ├── progress.html
│       ├── complete.html
│       └── error.html
├── assets/
│   ├── logo.png
│   ├── icons/
│   └── animations/
└── build/              # Electron-builder config
    └── builder-config.json
```

### Electron Main Process

```javascript
// main.js
const { app, BrowserWindow, ipcMain, dialog } = require('electron');

class InstallerWindow {
    constructor() {
        this.window = null;
        this.installer = null;
    }

    create() {
        this.window = new BrowserWindow({
            width: 800,
            height: 600,
            webPreferences: {
                nodeIntegration: false,
                contextIsolation: true,
                preload: path.join(__dirname, 'preload.js')
            }
        });

        this.window.loadFile('renderer/index.html');
    }

    setupIPC() {
        ipcMain.handle('select-directory', this.handleSelectDirectory);
        ipcMain.handle('start-installation', this.handleStartInstallation);
        ipcMain.handle('cancel-installation', this.handleCancelInstallation);
    }

    async handleStartInstallation(event, config) {
        // Spawn Python installer process
        // Send progress updates via event.sender.send()
    }
}
```

### IPC Communication

**Main → Renderer (Progress Updates):**
```javascript
// main.js
win.webContents.send('installation-progress', {
    percent: 45,
    message: 'Installing CLI Tools...',
    details: 'Extracting devforgeai_cli.tar.gz'
});
```

**Renderer → Main (User Actions):**
```javascript
// renderer/app.js
const result = await window.electronAPI.startInstallation({
    path: '/usr/local/devforgeai',
    components: ['core', 'cli', 'templates']
});
```

### Packaging Configuration

**electron-builder config:**
```json
{
  "appId": "com.devforgeai.installer",
  "productName": "DevForgeAI Installer",
  "directories": {
    "output": "dist"
  },
  "files": [
    "main.js",
    "preload.js",
    "renderer/**/*",
    "assets/**/*"
  ],
  "win": {
    "target": "nsis",
    "icon": "assets/icon.ico"
  },
  "mac": {
    "target": "dmg",
    "icon": "assets/icon.icns"
  },
  "linux": {
    "target": ["AppImage", "deb"],
    "icon": "assets/icon.png"
  }
}
```

### Data Flow

```
User Interaction (Renderer)
    ↓ (IPC)
Electron Main Process
    ↓ (child_process.spawn)
Python Installer (installer/wizard.py)
    ↓ (stdout/progress events)
Electron Main Process
    ↓ (IPC)
Renderer Updates UI
```

## Implementation Notes

### Dependencies
- **STORY-247 (CLI Wizard):** GUI wraps the CLI wizard logic
- **Node.js 18+:** Required for Electron build
- **Python 3.10+:** Backend installer execution

### Technology Constraints
- **Template Only:** This story creates the Electron template, not full production
- **Optional Feature:** Users can skip GUI and use CLI wizard
- **Bundle Size:** Target <150MB for packaged installer

### Security Considerations
- **Context Isolation:** Enabled to prevent XSS
- **Node Integration:** Disabled in renderer
- **CSP:** Content Security Policy enforced
- **Code Signing:** Required for macOS/Windows (not in this story)

### Testing Strategy
- **Unit Tests:** IPC handlers, business logic
- **E2E Tests:** Spectron/Playwright for full GUI flow
- **Manual Tests:** Cross-platform installation testing

## Definition of Done

- [ ] All acceptance criteria verified and passing
- [ ] Electron app launches on Windows, macOS, Linux
- [ ] IPC communication working
- [ ] Progress updates in real-time
- [ ] Error handling graceful
- [ ] electron-builder config complete
- [ ] Template documented in README
- [ ] No security vulnerabilities (npm audit)

## Notes

- GUI is a **template** - full production packaging is out of scope
- Consider adding telemetry (opt-in) for installation success rates
- Future: Auto-update capability for the installer itself
- Bundle size optimization: Use electron-builder's compression

## Change Log

**Current Status:** Backlog

| Date | Author | Phase/Action | Change | Files Affected |
|------|--------|--------------|--------|----------------|
| 2025-01-06 | claude/batch-creation | Story Creation | Initial story created from EPIC-039 Feature 2 | STORY-248-gui-installer-template.story.md |
| 2025-01-06 | claude/normalization | Template Update | Normalized to format_version 2.5, added ADR-009 reference | STORY-248-gui-installer-template.story.md |

---

**Template Version:** 2.5
**Created:** 2025-01-06 by /create-missing-stories (batch mode)
**ADR:** ADR-009 (Electron GUI Installer Template)
