class BaseIDE {
  constructor(options = {}) {
    this.name = options.name || 'unknown';
    this.displayName = options.displayName || 'Unknown IDE';
  }

  // Override in subclass: return array of additional setup steps
  async setup(targetRoot, copier) {
    throw new Error(`${this.name}: setup() not implemented`);
  }

  // Override: return description of what this IDE integration does
  describe() {
    return `${this.displayName} integration`;
  }
}

module.exports = { BaseIDE };
