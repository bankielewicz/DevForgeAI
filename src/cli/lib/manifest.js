'use strict';

const fs = require('fs');
const path = require('path');

const MANIFEST_FILENAME = '.devforgeai-manifest.json';

class ManifestManager {
  constructor(targetRoot) {
    this.targetRoot = targetRoot;
  }

  getManifestPath() {
    return path.join(this.targetRoot, MANIFEST_FILENAME);
  }

  exists() {
    return fs.existsSync(this.getManifestPath());
  }

  read() {
    const manifestPath = this.getManifestPath();
    if (!fs.existsSync(manifestPath)) {
      return null;
    }
    const content = fs.readFileSync(manifestPath, 'utf8');
    return JSON.parse(content);
  }

  create(data) {
    const now = new Date().toISOString();
    const manifest = {
      ...data,
      installDate: now,
      lastUpdated: now,
    };
    fs.writeFileSync(this.getManifestPath(), JSON.stringify(manifest, null, 2), 'utf8');
    return manifest;
  }

  update(data) {
    const existing = this.read();
    if (!existing) {
      return this.create(data);
    }
    const merged = {
      ...existing,
      ...data,
      lastUpdated: new Date().toISOString(),
    };
    fs.writeFileSync(this.getManifestPath(), JSON.stringify(merged, null, 2), 'utf8');
    return merged;
  }
}

module.exports = { ManifestManager };
