/**
 * STORY-248: GUI Installer Template - Preload Script
 *
 * Context bridge for secure IPC communication between main and renderer processes.
 * Exposes electronAPI to renderer with all required methods and event listeners.
 */

const { contextBridge, ipcRenderer } = require('electron');

/**
 * Exposed API for renderer process.
 * All IPC communication goes through this secure bridge.
 */
const electronAPI = {
  /**
   * Opens native directory picker dialog.
   * AC#4: Browse button opens native file dialog.
   * @param {Object} options - Options with defaultPath
   * @returns {Promise<{path: string|null, canceled: boolean}>}
   */
  selectDirectory: (options = {}) => {
    return ipcRenderer.invoke('select-directory', options);
  },

  /**
   * Validates installation path for write permissions.
   * AC#4: Path validation indicator.
   * @param {string} path - Path to validate
   * @returns {Promise<{valid: boolean, message: string}>}
   */
  validatePath: (path) => {
    return ipcRenderer.invoke('validate-path', { path });
  },

  /**
   * Starts the installation process.
   * AC#5: Installation begins.
   * @param {Object} config - Installation configuration
   * @returns {Promise<{success: boolean}>}
   */
  startInstallation: (config) => {
    return ipcRenderer.invoke('start-installation', config);
  },

  /**
   * Cancels the installation process.
   * AC#5: Cancel button.
   * @returns {Promise<{success: boolean, canceled: boolean}>}
   */
  cancelInstallation: () => {
    return ipcRenderer.invoke('cancel-installation');
  },

  /**
   * Opens save dialog for installation log.
   * AC#7: Save Log button.
   * @param {string} logContent - Log content to save
   * @returns {Promise<{success: boolean, path?: string}>}
   */
  saveLog: (logContent) => {
    return ipcRenderer.invoke('save-log', { logContent });
  },

  /**
   * Checks system requirements.
   * AC#2: Requirements checked automatically.
   * @returns {Promise<Object>} Requirements check results
   */
  checkRequirements: () => {
    return ipcRenderer.invoke('check-requirements');
  },

  /**
   * Launches the installed application.
   * AC#6: Launch DevForgeAI checkbox.
   * @returns {Promise<{success: boolean}>}
   */
  launchApplication: () => {
    return ipcRenderer.invoke('launch-application');
  },

  /**
   * Registers progress event listener.
   * AC#5: Progress updates in real-time.
   * @param {Function} callback - Callback for progress events
   */
  onProgress: (callback) => {
    const handler = (event, data) => callback(data);
    ipcRenderer.on('installation-progress', handler);
    return handler;
  },

  /**
   * Registers completion event listener.
   * AC#6: Completion page.
   * @param {Function} callback - Callback for completion event
   */
  onComplete: (callback) => {
    const handler = (event, data) => callback(data);
    ipcRenderer.on('installation-complete', handler);
    return handler;
  },

  /**
   * Registers error event listener.
   * AC#7: Error handling page.
   * @param {Function} callback - Callback for error events
   */
  onError: (callback) => {
    const handler = (event, data) => callback(data);
    ipcRenderer.on('installation-error', handler);
    return handler;
  },

  /**
   * Removes progress event listener.
   * Cleanup for component unmount.
   * @param {Function} handler - Handler to remove
   */
  removeProgressListener: (handler) => {
    ipcRenderer.removeListener('installation-progress', handler);
  },

  /**
   * Removes completion event listener.
   * Cleanup for component unmount.
   * @param {Function} handler - Handler to remove
   */
  removeCompleteListener: (handler) => {
    ipcRenderer.removeListener('installation-complete', handler);
  },

  /**
   * Removes error event listener.
   * Cleanup for component unmount.
   * @param {Function} handler - Handler to remove
   */
  removeErrorListener: (handler) => {
    ipcRenderer.removeListener('installation-error', handler);
  },
};

// Expose the API to renderer process
contextBridge.exposeInMainWorld('electronAPI', electronAPI);
