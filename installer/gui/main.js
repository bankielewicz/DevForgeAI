/**
 * STORY-248: GUI Installer Template - Electron Main Process
 *
 * Electron main process with InstallerWindow class for GUI installer.
 * Implements IPC handlers for directory selection, installation, and error handling.
 */

const { app, BrowserWindow, ipcMain, dialog } = require('electron');
const path = require('path');
const fs = require('fs');
const fsPromises = require('fs').promises;

/**
 * InstallerWindow class manages the main Electron window and IPC communication.
 */
class InstallerWindow {
  constructor() {
    this.window = null;
    this.installer = null;
    this.installationProcess = null;
  }

  /**
   * Creates the main BrowserWindow with security and display settings.
   * AC#1: Window 800x600, centered, context isolation enabled, DevTools disabled in production.
   */
  async create() {
    const isProduction = app.isPackaged;

    this.window = new BrowserWindow({
      width: 800,
      height: 600,
      webPreferences: {
        nodeIntegration: false,
        contextIsolation: true,
        preload: path.join(__dirname, 'preload.js'),
        devTools: !isProduction,
      },
      resizable: true,
      show: false,
    });

    // Center the window on screen
    this.window.center();

    // Load the main HTML file
    await this.window.loadFile(path.join(__dirname, 'renderer', 'index.html'));

    // Show window once ready
    this.window.once('ready-to-show', () => {
      this.window.show();
    });

    return this.window;
  }

  /**
   * Sets up IPC handlers for renderer-main communication.
   * AC#4, AC#5, AC#7: Path picker, installation progress, error handling.
   */
  setupIPC() {
    // AC#4: Directory selection handler
    ipcMain.handle('select-directory', this.handleSelectDirectory.bind(this));

    // AC#4: Path validation handler
    ipcMain.handle('validate-path', this.handleValidatePath.bind(this));

    // AC#5: Installation handlers
    ipcMain.handle('start-installation', this.handleStartInstallation.bind(this));
    ipcMain.handle('cancel-installation', this.handleCancelInstallation.bind(this));

    // AC#7: Error handling - save log
    ipcMain.handle('save-log', this.handleSaveLog.bind(this));

    // AC#2: Requirements check
    ipcMain.handle('check-requirements', this.handleCheckRequirements.bind(this));

    // AC#6: Launch application
    ipcMain.handle('launch-application', this.handleLaunchApplication.bind(this));
  }

  /**
   * Handles directory selection via native dialog.
   * AC#4: Opens native directory picker.
   */
  async handleSelectDirectory(event, options = {}) {
    // Get default path, with fallback for testing
    let defaultPathValue = options.defaultPath;
    if (!defaultPathValue) {
      try {
        if (app.getPath) {
          defaultPathValue = app.getPath('home');
        }
      } catch (e) {
        defaultPathValue = undefined;
      }
    }

    const result = await dialog.showOpenDialog({
      properties: ['openDirectory', 'createDirectory'],
      defaultPath: defaultPathValue,
      title: 'Select Installation Directory',
    });

    if (result.canceled || result.filePaths.length === 0) {
      return { path: null, canceled: true };
    }

    return { path: result.filePaths[0], canceled: false };
  }

  /**
   * Validates a path for write permissions.
   * AC#4: Path validation indicator.
   */
  async handleValidatePath(event, options = {}) {
    const targetPath = options.path;

    if (!targetPath) {
      return { valid: false, message: 'No path provided' };
    }

    // Canonicalize path to prevent path traversal attacks
    const normalizedPath = path.resolve(targetPath);

    try {
      // Check if path exists using async API
      try {
        await fsPromises.access(normalizedPath, fs.constants.F_OK);
        // Path exists, check write permissions
        await fsPromises.access(normalizedPath, fs.constants.W_OK);
        return { valid: true, message: 'Path is writable' };
      } catch (accessError) {
        if (accessError.code === 'ENOENT') {
          // Path doesn't exist, check if parent directory is writable
          const parentPath = path.dirname(normalizedPath);
          try {
            await fsPromises.access(parentPath, fs.constants.W_OK);
            return { valid: true, message: 'Path can be created' };
          } catch {
            return { valid: false, message: 'Parent directory does not exist or is not writable' };
          }
        }
        return { valid: false, message: 'Path is not writable' };
      }
    } catch (error) {
      return { valid: false, message: 'Path validation failed' };
    }
  }

  /**
   * Starts the installation process.
   * AC#5: Installation progress via IPC.
   */
  async handleStartInstallation(event, config) {
    // Validate config structure
    if (!config || typeof config !== 'object') {
      return { success: false, error: 'Invalid configuration' };
    }

    // Validate path
    if (!config.path || typeof config.path !== 'string') {
      return { success: false, error: 'Installation path is required' };
    }

    // Validate components
    if (!Array.isArray(config.components) || config.components.length === 0) {
      return { success: false, error: 'At least one component must be selected' };
    }

    // Validate all components are valid strings
    const validComponents = ['core', 'cli', 'templates', 'examples'];
    for (const comp of config.components) {
      if (typeof comp !== 'string' || !validComponents.includes(comp)) {
        return { success: false, error: 'Invalid component selection' };
      }
    }

    // Implementation would spawn Python installer process
    // For template, return success structure
    return { success: true, started: true };
  }

  /**
   * Cancels the installation process.
   * AC#5: Cancel button with confirmation.
   */
  async handleCancelInstallation(event) {
    if (this.installationProcess) {
      this.installationProcess.kill();
      this.installationProcess = null;
    }
    return { success: true, canceled: true };
  }

  /**
   * Opens save dialog for installation log.
   * AC#7: Save Log button.
   */
  async handleSaveLog(event, options = {}) {
    // Get default path, with fallback for testing
    let defaultPath = 'install.log';
    try {
      if (app.getPath) {
        defaultPath = path.join(app.getPath('documents'), 'install.log');
      }
    } catch (e) {
      // Fallback if getPath not available
      defaultPath = 'install.log';
    }

    const result = await dialog.showSaveDialog({
      defaultPath: defaultPath,
      filters: [
        { name: 'Log Files', extensions: ['log', 'txt'] },
        { name: 'All Files', extensions: ['*'] },
      ],
      title: 'Save Installation Log',
    });

    if (result.canceled || !result.filePath) {
      return { success: false, canceled: true };
    }

    try {
      await fsPromises.writeFile(result.filePath, options.logContent || '');
      return { success: true, path: result.filePath };
    } catch (error) {
      // Return generic message to avoid leaking sensitive paths
      return { success: false, error: 'Failed to save log file' };
    }
  }

  /**
   * Checks system requirements.
   * AC#2: Requirements checking.
   */
  async handleCheckRequirements(event) {
    // Template implementation - actual check would verify disk space, Python, etc.
    return {
      diskSpace: { met: true, required: '500MB', available: '10GB' },
      permissions: { met: true },
      python: { met: true, version: '3.10.0' },
    };
  }

  /**
   * Launches the installed application.
   * AC#6: Launch after install.
   */
  async handleLaunchApplication(event) {
    // Template implementation - would launch devforgeai CLI
    return { success: true };
  }

  /**
   * Sends progress update to renderer.
   * AC#5: Real-time progress updates.
   */
  sendProgressUpdate(data) {
    if (this.window && this.window.webContents) {
      this.window.webContents.send('installation-progress', {
        percent: data.percent,
        message: data.message,
        details: data.details,
      });
    }
  }

  /**
   * Sends installation complete event to renderer.
   * AC#6: Completion notification.
   */
  sendInstallationComplete(data) {
    if (this.window && this.window.webContents) {
      this.window.webContents.send('installation-complete', {
        success: data.success,
        installedComponents: data.installedComponents,
      });
    }
  }

  /**
   * Sends installation error event to renderer.
   * AC#7: Error handling.
   */
  sendInstallationError(data) {
    if (this.window && this.window.webContents) {
      this.window.webContents.send('installation-error', {
        message: data.message,
        details: data.details,
        code: data.code,
      });
    }
  }
}

// App lifecycle management
let installerWindow = null;

app.whenReady().then(async () => {
  installerWindow = new InstallerWindow();
  await installerWindow.create();
  installerWindow.setupIPC();
});

app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') {
    app.quit();
  }
});

app.on('activate', async () => {
  if (BrowserWindow.getAllWindows().length === 0) {
    installerWindow = new InstallerWindow();
    await installerWindow.create();
    installerWindow.setupIPC();
  }
});

// Export for testing
module.exports = { InstallerWindow };
