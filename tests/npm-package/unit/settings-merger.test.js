'use strict';

const fs = require('fs');
const fsp = fs.promises;
const path = require('path');
const os = require('os');

const { SettingsMerger } = require('../../../src/cli/lib/settings-merger');

describe('SettingsMerger', () => {
  let tmpDir;

  beforeEach(async () => {
    tmpDir = await fsp.mkdtemp(path.join(os.tmpdir(), 'settings-merger-'));
    await fsp.mkdir(path.join(tmpDir, '.claude'), { recursive: true });
  });

  afterEach(async () => {
    await fsp.rm(tmpDir, { recursive: true, force: true });
  });

  const TEMPLATE = {
    permissions: {
      defaultMode: 'default',
      allow: ['Bash(git status*)', 'Bash(npm test*)'],
      ask: ['Bash(git push --force*)'],
      deny: ['Bash(rm -rf /)'],
    },
    includeCoAuthoredBy: false,
    statusLine: {
      type: 'command',
      command: '"$CLAUDE_PROJECT_DIR"/.claude/scripts/statusline.sh',
    },
    hooks: {
      PreToolUse: [{
        matcher: 'Bash',
        hooks: [{ type: 'command', command: '"$CLAUDE_PROJECT_DIR"/.claude/hooks/pre-tool-use.sh', timeout: 10 }],
      }],
      PostToolUse: [{
        matcher: 'Edit|Write',
        hooks: [{ type: 'command', command: '"$CLAUDE_PROJECT_DIR"/.claude/hooks/post-edit-write-check.sh', timeout: 10 }],
      }],
    },
  };

  describe('constructor', () => {
    it('should throw without targetRoot', () => {
      expect(() => new SettingsMerger(null)).toThrow('requires targetRoot');
    });
  });

  describe('fresh install (no existing settings.json)', () => {
    it('should create settings.json from template', async () => {
      const merger = new SettingsMerger(tmpDir);
      const result = await merger.install(TEMPLATE);

      expect(result.action).toBe('created');
      expect(result.backupCreated).toBe(false);

      const written = JSON.parse(await fsp.readFile(path.join(tmpDir, '.claude', 'settings.json'), 'utf8'));
      expect(written.hooks.PreToolUse).toHaveLength(1);
      expect(written.permissions.allow).toContain('Bash(git status*)');
    });
  });

  describe('overwrite mode', () => {
    it('should replace existing settings entirely', async () => {
      const existing = { permissions: { allow: ['Bash(custom)'] }, hooks: {} };
      await fsp.writeFile(path.join(tmpDir, '.claude', 'settings.json'), JSON.stringify(existing));

      const merger = new SettingsMerger(tmpDir);
      const result = await merger.install(TEMPLATE, { mode: 'overwrite' });

      expect(result.action).toBe('overwritten');
      const written = JSON.parse(await fsp.readFile(path.join(tmpDir, '.claude', 'settings.json'), 'utf8'));
      expect(written.permissions.allow).not.toContain('Bash(custom)');
      expect(written.hooks.PreToolUse).toHaveLength(1);
    });
  });

  describe('merge mode — existing settings WITHOUT hooks', () => {
    it('should add hooks while preserving existing permissions', async () => {
      const existing = {
        permissions: { allow: ['Bash(custom-cmd)'], deny: ['Bash(dangerous)'] },
      };
      await fsp.writeFile(path.join(tmpDir, '.claude', 'settings.json'), JSON.stringify(existing));

      const merger = new SettingsMerger(tmpDir);
      const result = await merger.install(TEMPLATE);

      expect(result.action).toBe('merged');
      expect(result.backupCreated).toBe(true);

      const written = JSON.parse(await fsp.readFile(path.join(tmpDir, '.claude', 'settings.json'), 'utf8'));
      // Existing permissions preserved
      expect(written.permissions.allow).toContain('Bash(custom-cmd)');
      expect(written.permissions.deny).toContain('Bash(dangerous)');
      // Template permissions added
      expect(written.permissions.allow).toContain('Bash(git status*)');
      // Hooks added
      expect(written.hooks.PreToolUse).toHaveLength(1);
    });
  });

  describe('merge mode — existing settings WITH hooks', () => {
    it('should add new hook events without duplicating existing ones', async () => {
      const existing = {
        permissions: { allow: [] },
        hooks: {
          PreToolUse: [{
            matcher: 'Bash',
            hooks: [{ type: 'command', command: 'my-custom-hook.sh' }],
          }],
        },
      };
      await fsp.writeFile(path.join(tmpDir, '.claude', 'settings.json'), JSON.stringify(existing));

      const merger = new SettingsMerger(tmpDir);
      await merger.install(TEMPLATE);

      const written = JSON.parse(await fsp.readFile(path.join(tmpDir, '.claude', 'settings.json'), 'utf8'));
      // Custom hook preserved, template hook added
      expect(written.hooks.PreToolUse).toHaveLength(2);
      expect(written.hooks.PreToolUse[0].hooks[0].command).toBe('my-custom-hook.sh');
      // PostToolUse added (didn't exist before)
      expect(written.hooks.PostToolUse).toHaveLength(1);
    });

    it('should not duplicate hooks that already match', async () => {
      const existing = {
        hooks: {
          PreToolUse: [{
            matcher: 'Bash',
            hooks: [{ type: 'command', command: '"$CLAUDE_PROJECT_DIR"/.claude/hooks/pre-tool-use.sh', timeout: 10 }],
          }],
        },
      };
      await fsp.writeFile(path.join(tmpDir, '.claude', 'settings.json'), JSON.stringify(existing));

      const merger = new SettingsMerger(tmpDir);
      await merger.install(TEMPLATE);

      const written = JSON.parse(await fsp.readFile(path.join(tmpDir, '.claude', 'settings.json'), 'utf8'));
      // Should still be 1, not duplicated
      expect(written.hooks.PreToolUse).toHaveLength(1);
    });
  });

  describe('merge mode — idempotent', () => {
    it('should produce same result when run twice', async () => {
      const merger = new SettingsMerger(tmpDir);
      await merger.install(TEMPLATE);
      const first = await fsp.readFile(path.join(tmpDir, '.claude', 'settings.json'), 'utf8');

      await merger.install(TEMPLATE);
      const second = await fsp.readFile(path.join(tmpDir, '.claude', 'settings.json'), 'utf8');

      expect(JSON.parse(second)).toEqual(JSON.parse(first));
    });
  });

  describe('merge mode — preserves existing statusLine', () => {
    it('should not overwrite custom statusLine', async () => {
      const existing = {
        statusLine: { type: 'command', command: 'my-status.sh' },
      };
      await fsp.writeFile(path.join(tmpDir, '.claude', 'settings.json'), JSON.stringify(existing));

      const merger = new SettingsMerger(tmpDir);
      await merger.install(TEMPLATE);

      const written = JSON.parse(await fsp.readFile(path.join(tmpDir, '.claude', 'settings.json'), 'utf8'));
      expect(written.statusLine.command).toBe('my-status.sh');
    });
  });

  describe('merge mode — preserves existing includeCoAuthoredBy', () => {
    it('should not overwrite user preference', async () => {
      const existing = { includeCoAuthoredBy: true };
      await fsp.writeFile(path.join(tmpDir, '.claude', 'settings.json'), JSON.stringify(existing));

      const merger = new SettingsMerger(tmpDir);
      await merger.install(TEMPLATE);

      const written = JSON.parse(await fsp.readFile(path.join(tmpDir, '.claude', 'settings.json'), 'utf8'));
      expect(written.includeCoAuthoredBy).toBe(true);
    });
  });

  describe('backup', () => {
    it('should create .bak file before merging', async () => {
      const existing = { permissions: { allow: ['original'] } };
      await fsp.writeFile(path.join(tmpDir, '.claude', 'settings.json'), JSON.stringify(existing));

      const merger = new SettingsMerger(tmpDir);
      await merger.install(TEMPLATE);

      const backup = JSON.parse(await fsp.readFile(path.join(tmpDir, '.claude', 'settings.json.bak'), 'utf8'));
      expect(backup.permissions.allow).toEqual(['original']);
    });
  });

  describe('mergePermissions', () => {
    it('should union allow lists without duplicates', () => {
      const merger = new SettingsMerger(tmpDir);
      const result = merger.mergePermissions(
        { allow: ['Bash(a)', 'Bash(b)'] },
        { allow: ['Bash(b)', 'Bash(c)'] }
      );
      expect(result.allow).toEqual(['Bash(a)', 'Bash(b)', 'Bash(c)']);
    });

    it('should set defaultMode if missing', () => {
      const merger = new SettingsMerger(tmpDir);
      const result = merger.mergePermissions({}, { defaultMode: 'default' });
      expect(result.defaultMode).toBe('default');
    });

    it('should not overwrite existing defaultMode', () => {
      const merger = new SettingsMerger(tmpDir);
      const result = merger.mergePermissions(
        { defaultMode: 'bypassPermissions' },
        { defaultMode: 'default' }
      );
      expect(result.defaultMode).toBe('bypassPermissions');
    });
  });

  describe('_hookEntriesMatch', () => {
    it('should match identical entries', () => {
      const merger = new SettingsMerger(tmpDir);
      const entry = { matcher: 'Bash', hooks: [{ command: 'hook.sh' }] };
      expect(merger._hookEntriesMatch(entry, entry)).toBe(true);
    });

    it('should not match entries with different matchers', () => {
      const merger = new SettingsMerger(tmpDir);
      const a = { matcher: 'Bash', hooks: [{ command: 'hook.sh' }] };
      const b = { matcher: 'Edit', hooks: [{ command: 'hook.sh' }] };
      expect(merger._hookEntriesMatch(a, b)).toBe(false);
    });

    it('should not match entries with different commands', () => {
      const merger = new SettingsMerger(tmpDir);
      const a = { matcher: 'Bash', hooks: [{ command: 'hook-a.sh' }] };
      const b = { matcher: 'Bash', hooks: [{ command: 'hook-b.sh' }] };
      expect(merger._hookEntriesMatch(a, b)).toBe(false);
    });

    it('should match entries without matchers', () => {
      const merger = new SettingsMerger(tmpDir);
      const a = { hooks: [{ command: 'hook.sh' }] };
      const b = { hooks: [{ command: 'hook.sh' }] };
      expect(merger._hookEntriesMatch(a, b)).toBe(true);
    });
  });
});
