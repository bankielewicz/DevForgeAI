'use strict';

const fs = require('fs');
const fsp = fs.promises;
const path = require('path');

const TEXT_EXTENSIONS = new Set([
  '.md', '.js', '.ts', '.json', '.yaml', '.yml',
  '.sh', '.py', '.txt', '.css', '.html'
]);

function isTextFile(filePath) {
  const ext = path.extname(filePath).toLowerCase();
  return TEXT_EXTENSIONS.has(ext);
}

class Copier {
  constructor(sourceRoot, targetRoot) {
    if (!sourceRoot || !targetRoot) {
      throw new Error('Copier requires both sourceRoot and targetRoot');
    }
    this.sourceRoot = path.resolve(sourceRoot);
    this.targetRoot = path.resolve(targetRoot);
    this.installedFiles = [];
    this.createdDirs = [];
  }

  async copyDirectory(fromRelative, toRelative, options = {}) {
    const srcDir = path.join(this.sourceRoot, fromRelative);
    const destDir = path.join(this.targetRoot, toRelative);

    let entries;
    try {
      entries = await fsp.readdir(srcDir, { withFileTypes: true });
    } catch (err) {
      throw new Error(`Source directory not found: ${srcDir}`);
    }

    await fsp.mkdir(destDir, { recursive: true });

    for (const entry of entries) {
      const srcPath = path.join(fromRelative, entry.name);
      const destPath = path.join(toRelative, entry.name);

      if (entry.isDirectory()) {
        await this.copyDirectory(srcPath, destPath, options);
      } else {
        await this.copyFile(srcPath, destPath, options);
      }
    }
  }

  async copyFile(fromRelative, toRelative, options = {}) {
    const srcFile = path.join(this.sourceRoot, fromRelative);
    const destFile = path.join(this.targetRoot, toRelative);

    try {
      await fsp.access(srcFile);
    } catch (err) {
      throw new Error(`Source file not found: ${srcFile}`);
    }

    const destDir = path.dirname(destFile);
    await fsp.mkdir(destDir, { recursive: true });

    if (options.template && isTextFile(srcFile)) {
      let content = await fsp.readFile(srcFile, 'utf8');
      const variables = options.variables || {};
      for (const [key, value] of Object.entries(variables)) {
        const pattern = new RegExp(`\\{\\{${key}\\}\\}`, 'g');
        content = content.replace(pattern, value);
      }
      await fsp.writeFile(destFile, content, 'utf8');
    } else {
      await fsp.copyFile(srcFile, destFile);
    }

    // Preserve execute permissions from source (important for .sh scripts)
    try {
      const srcStat = await fsp.stat(srcFile);
      await fsp.chmod(destFile, srcStat.mode);
    } catch {
      // chmod may fail on Windows — non-fatal
    }

    this.installedFiles.push(toRelative);
  }

  async createDirectories(dirs) {
    for (const dir of dirs) {
      const fullPath = path.join(this.targetRoot, dir);
      await fsp.mkdir(fullPath, { recursive: true });
      this.createdDirs.push(dir);
    }
  }

  getInstalledFiles() {
    return [...this.installedFiles];
  }

  getCreatedDirs() {
    return [...this.createdDirs];
  }

  getStats() {
    return {
      filesCopied: this.installedFiles.length,
      directoriesCreated: this.createdDirs.length
    };
  }
}

module.exports = { Copier, isTextFile };
