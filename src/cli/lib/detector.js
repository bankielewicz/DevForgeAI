'use strict';

const fs = require('fs');
const path = require('path');
const { ManifestManager } = require('./manifest');

class Detector {
  constructor(targetRoot) {
    this.targetRoot = targetRoot;
    this.manifestManager = new ManifestManager(targetRoot);
  }

  detect() {
    const manifest = this.manifestManager.read();
    return {
      exists: manifest !== null,
      manifest: manifest,
      hasClaudeDir: fs.existsSync(path.join(this.targetRoot, '.claude')),
      hasDevforgeaiDir: fs.existsSync(path.join(this.targetRoot, 'devforgeai')),
      hasClaudeMd: fs.existsSync(path.join(this.targetRoot, 'CLAUDE.md')),
    };
  }

  isDevForgeAIProject() {
    if (this.manifestManager.exists()) {
      return true;
    }
    const hasClaudeDir = fs.existsSync(path.join(this.targetRoot, '.claude'));
    const hasDevforgeaiDir = fs.existsSync(path.join(this.targetRoot, 'devforgeai'));
    return hasClaudeDir && hasDevforgeaiDir;
  }
}

module.exports = { Detector };
