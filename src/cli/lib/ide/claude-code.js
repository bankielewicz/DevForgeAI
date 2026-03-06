const path = require('path');
const fs = require('fs');
const fsp = fs.promises;
const { BaseIDE } = require('./base');
const { SettingsMerger } = require('../settings-merger');

class ClaudeCodeIDE extends BaseIDE {
  constructor() {
    super({ name: 'claude-code', displayName: 'Claude Code' });
  }

  async setup(targetRoot, copier, options = {}) {
    const merger = new SettingsMerger(targetRoot);

    // Load template settings from the package source
    const templatePath = path.join(copier.sourceRoot, 'src', 'claude', 'settings.json');
    let templateSettings;
    try {
      const raw = await fsp.readFile(templatePath, 'utf8');
      templateSettings = JSON.parse(raw);
    } catch (err) {
      return { success: false, message: `Could not read template settings: ${err.message}` };
    }

    const mode = options.reinstall ? 'overwrite' : 'merge';
    const result = await merger.install(templateSettings, { mode });

    return {
      success: true,
      message: `Claude Code settings ${result.action}${result.backupCreated ? ' (backup created)' : ''}`,
    };
  }

  describe() {
    return 'Claude Code — .claude/ directory with agents, skills, commands, rules, hooks, settings';
  }
}

module.exports = { ClaudeCodeIDE };
