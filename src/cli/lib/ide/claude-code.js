const { BaseIDE } = require('./base');

class ClaudeCodeIDE extends BaseIDE {
  constructor() {
    super({ name: 'claude-code', displayName: 'Claude Code' });
  }

  async setup(targetRoot, copier) {
    // Claude Code uses .claude/ directory which is already handled
    // by the core-framework, agents, skills, commands, hooks components.
    // This integration ensures the directory structure is correct
    // and any Claude Code-specific config is in place.

    // No additional steps needed - all .claude/ content
    // is handled by component copier
    return { success: true, message: 'Claude Code integration ready' };
  }

  describe() {
    return 'Claude Code — .claude/ directory with agents, skills, commands, rules, hooks';
  }
}

module.exports = { ClaudeCodeIDE };
