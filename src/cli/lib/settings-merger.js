'use strict';

const fs = require('fs');
const fsp = fs.promises;
const path = require('path');

class SettingsMerger {
  constructor(targetRoot) {
    if (!targetRoot) {
      throw new Error('SettingsMerger requires targetRoot');
    }
    this.targetRoot = path.resolve(targetRoot);
    this.settingsPath = path.join(this.targetRoot, '.claude', 'settings.json');
    this.backupPath = path.join(this.targetRoot, '.claude', 'settings.json.bak');
  }

  /**
   * Install settings.json into target project.
   * @param {object} templateSettings - The DevForgeAI template settings object
   * @param {object} options - { mode: 'merge' | 'overwrite' }
   * @returns {object} { action: string, backupCreated: boolean }
   */
  async install(templateSettings, options = {}) {
    const mode = options.mode || 'merge';

    await fsp.mkdir(path.dirname(this.settingsPath), { recursive: true });

    let existing = null;
    try {
      const raw = await fsp.readFile(this.settingsPath, 'utf8');
      existing = JSON.parse(raw);
    } catch {
      // No existing file or invalid JSON — treat as fresh install
    }

    if (!existing || mode === 'overwrite') {
      await fsp.writeFile(this.settingsPath, JSON.stringify(templateSettings, null, 2) + '\n', 'utf8');
      return { action: existing ? 'overwritten' : 'created', backupCreated: false };
    }

    // Merge mode: backup first, then deep merge
    await this.backup(existing);
    const merged = this.merge(existing, templateSettings);
    await fsp.writeFile(this.settingsPath, JSON.stringify(merged, null, 2) + '\n', 'utf8');
    return { action: 'merged', backupCreated: true };
  }

  /**
   * Deep merge template into existing settings.
   * Existing values are preserved; template fills gaps.
   */
  merge(existing, template) {
    const result = JSON.parse(JSON.stringify(existing));

    // Merge permissions
    if (template.permissions) {
      result.permissions = this.mergePermissions(
        result.permissions || {},
        template.permissions
      );
    }

    // Merge hooks
    if (template.hooks) {
      result.hooks = this.mergeHooks(
        result.hooks || {},
        template.hooks
      );
    }

    // Set statusLine if missing
    if (template.statusLine && !result.statusLine) {
      result.statusLine = template.statusLine;
    }

    // Set includeCoAuthoredBy if missing
    if ('includeCoAuthoredBy' in template && !('includeCoAuthoredBy' in result)) {
      result.includeCoAuthoredBy = template.includeCoAuthoredBy;
    }

    return result;
  }

  /**
   * Merge permission arrays: union of allow/ask/deny with deduplication.
   */
  mergePermissions(existing, incoming) {
    const result = JSON.parse(JSON.stringify(existing));

    if (incoming.defaultMode && !result.defaultMode) {
      result.defaultMode = incoming.defaultMode;
    }

    for (const key of ['allow', 'ask', 'deny']) {
      if (incoming[key]) {
        const existingSet = new Set(result[key] || []);
        for (const item of incoming[key]) {
          existingSet.add(item);
        }
        result[key] = [...existingSet];
      }
    }

    return result;
  }

  /**
   * Merge hooks by event name. Within each event, deduplicate by command path.
   */
  mergeHooks(existing, incoming) {
    const result = JSON.parse(JSON.stringify(existing));

    for (const [eventName, incomingEntries] of Object.entries(incoming)) {
      if (!result[eventName]) {
        // Event doesn't exist — add all entries
        result[eventName] = incomingEntries;
        continue;
      }

      // Event exists — deduplicate by command path
      for (const incomingEntry of incomingEntries) {
        const isDuplicate = result[eventName].some(existingEntry =>
          this._hookEntriesMatch(existingEntry, incomingEntry)
        );
        if (!isDuplicate) {
          result[eventName].push(incomingEntry);
        }
      }
    }

    return result;
  }

  /**
   * Check if two hook entries match (same matcher + same command paths).
   */
  _hookEntriesMatch(a, b) {
    // Different matchers = different entries
    const matcherA = a.matcher || '';
    const matcherB = b.matcher || '';
    if (matcherA !== matcherB) return false;

    // Compare hook commands
    const cmdsA = (a.hooks || []).map(h => h.command).sort();
    const cmdsB = (b.hooks || []).map(h => h.command).sort();

    if (cmdsA.length !== cmdsB.length) return false;
    return cmdsA.every((cmd, i) => cmd === cmdsB[i]);
  }

  /**
   * Backup existing settings.json.
   */
  async backup(existingObj) {
    const content = JSON.stringify(existingObj, null, 2) + '\n';
    await fsp.writeFile(this.backupPath, content, 'utf8');
  }
}

module.exports = { SettingsMerger };
