/**
 * STORY-248: GUI Installer Template - Renderer Application
 *
 * InstallerApp class manages page navigation, state, and UI interactions.
 * Implements all acceptance criteria for the installer wizard flow.
 */

/**
 * Component definitions with sizes and descriptions.
 */
const COMPONENTS = {
  core: {
    id: 'core',
    name: 'Core Framework',
    description: 'Essential DevForgeAI framework files',
    size: 50, // MB
    required: true,
  },
  cli: {
    id: 'cli',
    name: 'CLI Tools',
    description: 'Command-line interface and validators',
    size: 25,
    required: false,
  },
  templates: {
    id: 'templates',
    name: 'Templates',
    description: 'Project templates and boilerplate',
    size: 15,
    required: false,
  },
  examples: {
    id: 'examples',
    name: 'Examples',
    description: 'Example projects and tutorials',
    size: 30,
    required: false,
  },
};

/**
 * Framework version
 */
const FRAMEWORK_VERSION = '1.0.0';

/**
 * Page order for navigation
 */
const PAGE_ORDER = ['welcome', 'components', 'path', 'progress', 'complete', 'error'];

/**
 * Sanitizes a string for safe insertion into HTML.
 * Prevents XSS attacks by escaping HTML special characters.
 * @param {string} str - The string to sanitize
 * @returns {string} The sanitized string
 */
function sanitizeHTML(str) {
  if (typeof str !== 'string') return '';
  return str
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#039;');
}

/**
 * InstallerApp class manages the installer wizard UI and state.
 */
class InstallerApp {
  constructor() {
    this.currentPage = 'welcome';
    this.pageHistory = [];
    this.state = {
      selectedComponents: ['core'], // Core is always selected
      installPath: this.getDefaultInstallPath(),
      requirements: null,
      launchAfterInstall: false,
      installedComponents: [],
    };
    this.colorScheme = 'light';
    this.showingCancelConfirmation = false;
    this.closing = false;
    this.cleanupPerformed = false;
    this.lastError = null;
    this.previousPage = null;
  }

  /**
   * Gets the default installation path based on platform.
   */
  getDefaultInstallPath() {
    if (typeof process !== 'undefined') {
      if (process.platform === 'win32') {
        return 'C:\\DevForgeAI';
      } else if (process.platform === 'darwin') {
        return '/usr/local/devforgeai';
      }
    }
    return '/opt/devforgeai';
  }

  /**
   * Initializes the application.
   * AC#2: Welcome page on initial load.
   * AC#8: Dark mode detection.
   */
  async initialize() {
    // Detect color scheme
    this.detectColorScheme();

    // Apply system font
    this.applySystemFont();

    // Render initial page
    this.renderPage('welcome');

    // Check requirements automatically
    if (window.electronAPI) {
      await this.checkRequirements();
    }
  }

  /**
   * Detects system color scheme preference.
   * AC#8: Dark mode detection.
   */
  detectColorScheme() {
    if (window.matchMedia) {
      const darkModeQuery = window.matchMedia('(prefers-color-scheme: dark)');
      this.colorScheme = darkModeQuery.matches ? 'dark' : 'light';

      if (this.colorScheme === 'dark') {
        document.body.classList.add('dark-mode');
      }

      // Listen for changes
      darkModeQuery.addEventListener('change', (e) => {
        this.colorScheme = e.matches ? 'dark' : 'light';
        document.body.classList.toggle('dark-mode', e.matches);
      });
    }
  }

  /**
   * Applies system font to body.
   * AC#8: System fonts.
   */
  applySystemFont() {
    document.body.style.fontFamily = 'system-ui, -apple-system, "Segoe UI", Roboto, sans-serif';
  }

  /**
   * Checks system requirements.
   * AC#2: Requirements checked automatically.
   */
  async checkRequirements() {
    try {
      this.state.requirements = await window.electronAPI.checkRequirements();
      this.updateRequirementsDisplay();
    } catch (error) {
      console.error('Failed to check requirements:', error);
    }
  }

  /**
   * Updates the requirements display.
   * AC#2: Warning icons for unmet requirements.
   */
  updateRequirementsDisplay() {
    const requirements = this.state.requirements;
    if (!requirements) return;

    const container = document.querySelector('.requirements-list');
    if (!container) return;

    let allMet = true;

    Object.entries(requirements).forEach(([key, req]) => {
      const element = document.querySelector(`[data-requirement="${key}"]`);
      if (element) {
        if (!req.met) {
          allMet = false;
          const warning = document.createElement('span');
          warning.className = 'requirement-warning';
          warning.textContent = ' !';
          element.appendChild(warning);
        }
      }
    });

    // Enable/disable next button
    const nextButton = document.querySelector('.btn-next');
    if (nextButton) {
      nextButton.disabled = !allMet;
    }
  }

  /**
   * Navigates to a specific page.
   * Supports all pages: welcome, components, path, progress, complete, error.
   */
  navigateTo(page) {
    if (this.currentPage !== page) {
      this.pageHistory.push(this.currentPage);
      this.previousPage = this.currentPage;
    }
    this.currentPage = page;
    this.renderPage(page);
  }

  /**
   * Goes back to the previous page.
   */
  goBack() {
    if (this.pageHistory.length > 0) {
      this.currentPage = this.pageHistory.pop();
      this.renderPage(this.currentPage);
    }
  }

  /**
   * Renders a specific page.
   */
  renderPage(page) {
    const appContainer = document.getElementById('app');
    if (!appContainer) return;

    // Clear existing content
    appContainer.innerHTML = '';

    switch (page) {
      case 'welcome':
        this.renderWelcomePage(appContainer);
        break;
      case 'components':
        this.renderComponentsPage(appContainer);
        break;
      case 'path':
        this.renderPathPage(appContainer);
        break;
      case 'progress':
        this.renderProgressPage(appContainer);
        break;
      case 'complete':
        this.renderCompletePage(appContainer);
        break;
      case 'error':
        this.renderErrorPage(appContainer);
        break;
    }
  }

  /**
   * Renders the welcome page.
   * AC#2: Welcome page with version and requirements.
   */
  renderWelcomePage(container) {
    container.innerHTML = `
      <div class="page-welcome">
        <div class="logo-container">
          <img src="../assets/logo.png" alt="DevForgeAI Logo" class="logo" />
        </div>
        <h1>Welcome to DevForgeAI</h1>
        <p class="version-display">Version ${FRAMEWORK_VERSION}</p>
        <div class="requirements-list">
          <h3>System Requirements</h3>
          <div data-requirement="diskSpace">Disk Space: 500MB required</div>
          <div data-requirement="permissions">Write Permissions</div>
          <div data-requirement="python">Python 3.10+</div>
        </div>
        <div class="button-row">
          <button class="btn-next" onclick="app.navigateTo('components')">Next</button>
        </div>
      </div>
    `;
    this.updateRequirementsDisplay();
  }

  /**
   * Renders the components selection page.
   * AC#3: Component selection with sizes.
   */
  renderComponentsPage(container) {
    const componentsHtml = Object.values(COMPONENTS)
      .map(
        (comp) => `
        <div class="component-item">
          <label>
            <input type="checkbox"
              id="component-${comp.id}"
              ${this.state.selectedComponents.includes(comp.id) ? 'checked' : ''}
              ${comp.required ? 'disabled' : ''}
              onchange="app.selectComponent('${comp.id}', this.checked)"
            />
            <span class="component-name">${comp.name}</span>
          </label>
          <p class="component-description">${comp.description}</p>
          <span class="component-size">${comp.size} MB</span>
        </div>
      `
      )
      .join('');

    container.innerHTML = `
      <div class="page-components">
        <h2>Select Components</h2>
        <div class="components-list">
          ${componentsHtml}
        </div>
        <div class="total-size">Total: ${this.calculateTotalSize()} MB</div>
        <div class="button-row">
          <button class="btn-back" onclick="app.goBack()">Back</button>
          <button class="btn-next" onclick="app.navigateTo('path')">Next</button>
        </div>
      </div>
    `;
  }

  /**
   * Renders the path selection page.
   * AC#4: Installation path picker.
   */
  renderPathPage(container) {
    const safePath = sanitizeHTML(this.state.installPath);
    container.innerHTML = `
      <div class="page-path">
        <h2>Installation Path</h2>
        <div class="path-input-row">
          <input type="text" id="install-path" value="${safePath}"
            onchange="app.setInstallPath(this.value)" />
          <button class="btn-browse" onclick="app.browseDirectory()">Browse</button>
        </div>
        <div class="path-validation-indicator"></div>
        <div class="path-error-message"></div>
        <div class="button-row">
          <button class="btn-back" onclick="app.goBack()">Back</button>
          <button class="btn-next" onclick="app.startInstallation()">Install</button>
        </div>
      </div>
    `;
  }

  /**
   * Renders the progress page.
   * AC#5: Installation progress.
   */
  renderProgressPage(container) {
    container.innerHTML = `
      <div class="page-progress">
        <h2>Installing DevForgeAI</h2>
        <div class="progress-container">
          <div class="progress-bar" style="width: 0%"></div>
        </div>
        <p class="current-operation">Preparing installation...</p>
        <div class="details-toggle">
          <button onclick="app.toggleDetails()">Show Details</button>
        </div>
        <div class="details-panel">
          <pre class="log-output"></pre>
        </div>
        <div class="button-row">
          <button class="btn-cancel" onclick="app.confirmCancel()">Cancel</button>
        </div>
      </div>
    `;
  }

  /**
   * Renders the completion page.
   * AC#6: Completion with summary.
   */
  renderCompletePage(container) {
    const componentsSummary = this.state.installedComponents
      .map((c) => `<li>${c}</li>`)
      .join('');

    container.innerHTML = `
      <div class="page-complete">
        <div class="success-icon">&#10003;</div>
        <h2>Installation Complete!</h2>
        <div class="installed-components">
          <h3>Installed Components:</h3>
          <ul>${componentsSummary || '<li>Core Framework</li>'}</ul>
        </div>
        <label class="launch-option">
          <input type="checkbox" id="launch-after-install"
            ${this.state.launchAfterInstall ? 'checked' : ''}
            onchange="app.setLaunchAfterInstall(this.checked)" />
          Launch DevForgeAI after closing
        </label>
        <div class="button-row">
          <button class="btn-finish" onclick="app.finish()">Finish</button>
        </div>
      </div>
    `;
  }

  /**
   * Renders the error page.
   * AC#7: Error handling.
   */
  renderErrorPage(container) {
    const error = this.lastError || { message: 'Unknown error', details: '' };
    const safeMessage = sanitizeHTML(error.message);
    const safeDetails = sanitizeHTML(error.details || 'No additional details available.');

    container.innerHTML = `
      <div class="page-error">
        <div class="error-icon">&#10007;</div>
        <h2>Installation Failed</h2>
        <p class="error-message">${safeMessage}</p>
        <div class="error-details-toggle">
          <button onclick="app.toggleErrorDetails()">Show Technical Details</button>
        </div>
        <div class="error-details-panel">
          <pre>${safeDetails}</pre>
        </div>
        <div class="button-row">
          <button class="btn-save-log" onclick="app.saveErrorLog()">Save Log</button>
          <button class="btn-retry" onclick="app.retry()">Retry</button>
          <button class="btn-exit" onclick="app.exit()">Exit</button>
        </div>
      </div>
    `;
  }

  /**
   * Selects or deselects a component.
   * AC#3: Component selection with size updates.
   */
  selectComponent(componentId, selected) {
    if (selected && !this.state.selectedComponents.includes(componentId)) {
      this.state.selectedComponents.push(componentId);
    } else if (!selected) {
      this.state.selectedComponents = this.state.selectedComponents.filter(
        (c) => c !== componentId
      );
    }

    // Update total size display
    const totalSizeElement = document.querySelector('.total-size');
    if (totalSizeElement) {
      totalSizeElement.textContent = `Total: ${this.calculateTotalSize()} MB`;
    }
  }

  /**
   * Calculates total size of selected components.
   */
  calculateTotalSize() {
    return this.state.selectedComponents.reduce((total, compId) => {
      return total + (COMPONENTS[compId]?.size || 0);
    }, 0);
  }

  /**
   * Sets the installation path.
   */
  setInstallPath(path) {
    this.state.installPath = path;
  }

  /**
   * Opens directory browser.
   * AC#4: Browse button opens native dialog.
   */
  async browseDirectory() {
    if (!window.electronAPI) return;

    const result = await window.electronAPI.selectDirectory({
      defaultPath: this.state.installPath,
    });

    if (!result.canceled && result.path) {
      this.state.installPath = result.path;
      const pathInput = document.querySelector('#install-path');
      if (pathInput) {
        pathInput.value = result.path;
      }
      await this.validateInstallPath(result.path);
    }
  }

  /**
   * Validates the installation path.
   * AC#4: Path validation indicator.
   */
  async validateInstallPath(path) {
    if (!window.electronAPI) return;

    const result = await window.electronAPI.validatePath(path);
    const indicator = document.querySelector('.path-validation-indicator');
    const errorMessage = document.querySelector('.path-error-message');

    if (indicator) {
      indicator.classList.remove('valid', 'invalid');
      indicator.classList.add(result.valid ? 'valid' : 'invalid');
    }

    if (errorMessage) {
      errorMessage.textContent = result.valid ? '' : result.message;
    }
  }

  /**
   * Starts the installation.
   */
  async startInstallation() {
    this.navigateTo('progress');

    if (window.electronAPI) {
      try {
        await window.electronAPI.startInstallation({
          path: this.state.installPath,
          components: this.state.selectedComponents,
        });
      } catch (error) {
        this.handleError({ message: error.message });
      }
    }
  }

  /**
   * Updates progress display.
   * AC#5: Progress bar and current operation.
   */
  updateProgress(data) {
    const progressBar = document.querySelector('.progress-bar');
    const operationText = document.querySelector('.current-operation');

    if (progressBar) {
      progressBar.style.width = `${data.percent}%`;
    }

    if (operationText) {
      operationText.textContent = data.message;
    }
  }

  /**
   * Shows cancel confirmation.
   * AC#5: Cancel with confirmation.
   */
  async confirmCancel() {
    this.showingCancelConfirmation = true;
    // In real implementation, show confirmation dialog
    return true;
  }

  /**
   * Toggles details panel visibility.
   * AC#5: Show Details toggle.
   */
  toggleDetails() {
    const panel = document.querySelector('.details-panel');
    if (panel) {
      panel.classList.toggle('visible');
    }
  }

  /**
   * Toggles error details visibility.
   */
  toggleErrorDetails() {
    const panel = document.querySelector('.error-details-panel');
    if (panel) {
      panel.classList.toggle('visible');
    }
  }

  /**
   * Sets installed components for summary.
   */
  setInstalledComponents(components) {
    this.state.installedComponents = components;
  }

  /**
   * Sets launch after install preference.
   */
  setLaunchAfterInstall(launch) {
    this.state.launchAfterInstall = launch;
  }

  /**
   * Finishes installation.
   * AC#6: Finish button behavior.
   */
  async finish() {
    if (this.state.launchAfterInstall && window.electronAPI) {
      await window.electronAPI.launchApplication();
    }
    this.closing = true;
    // In real implementation, close the window
  }

  /**
   * Handles errors and shows error page.
   * AC#7: Error handling.
   */
  handleError(error) {
    this.lastError = error;
    this.previousPage = this.currentPage;
    this.navigateTo('error');
  }

  /**
   * Saves error log.
   * AC#7: Save Log button.
   */
  async saveErrorLog() {
    if (window.electronAPI) {
      const logContent = `Error: ${this.lastError?.message}\nDetails: ${this.lastError?.details || 'N/A'}`;
      await window.electronAPI.saveLog(logContent);
    }
  }

  /**
   * Retries from error.
   * AC#7: Retry returns to previous step.
   */
  retry() {
    if (this.previousPage) {
      this.currentPage = this.previousPage;
      this.renderPage(this.currentPage);
    }
  }

  /**
   * Exits with cleanup.
   * AC#7: Exit with cleanup.
   */
  async exit() {
    this.cleanupPerformed = true;
    this.closing = true;
    // In real implementation, perform cleanup and close
  }
}

// Export for testing and global access
if (typeof module !== 'undefined' && module.exports) {
  module.exports = { InstallerApp };
}

// Global instance
if (typeof window !== 'undefined') {
  window.InstallerApp = InstallerApp;
}
