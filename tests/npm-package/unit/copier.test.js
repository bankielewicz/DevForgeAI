'use strict';

const fs = require('fs');
const fsp = fs.promises;
const path = require('path');
const os = require('os');

const { Copier, isTextFile } = require('../../../src/cli/lib/copier');

describe('Copier', () => {
  let tmpDir;
  let sourceDir;
  let targetDir;

  beforeEach(async () => {
    tmpDir = await fsp.mkdtemp(path.join(os.tmpdir(), 'copier-test-'));
    sourceDir = path.join(tmpDir, 'source');
    targetDir = path.join(tmpDir, 'target');
    await fsp.mkdir(sourceDir, { recursive: true });
    await fsp.mkdir(targetDir, { recursive: true });
  });

  afterEach(async () => {
    await fsp.rm(tmpDir, { recursive: true, force: true });
  });

  describe('isTextFile', () => {
    it('should identify .md files as text', () => {
      expect(isTextFile('README.md')).toBe(true);
    });

    it('should identify .sh files as text', () => {
      expect(isTextFile('script.sh')).toBe(true);
    });

    it('should identify .py files as text', () => {
      expect(isTextFile('validate.py')).toBe(true);
    });

    it('should not identify .png as text', () => {
      expect(isTextFile('image.png')).toBe(false);
    });
  });

  describe('copyFile', () => {
    it('should copy a file from source to target', async () => {
      const copier = new Copier(sourceDir, targetDir);
      await fsp.writeFile(path.join(sourceDir, 'test.txt'), 'hello');

      await copier.copyFile('test.txt', 'test.txt');

      const content = await fsp.readFile(path.join(targetDir, 'test.txt'), 'utf8');
      expect(content).toBe('hello');
    });

    it('should create intermediate directories', async () => {
      const copier = new Copier(sourceDir, targetDir);
      await fsp.writeFile(path.join(sourceDir, 'test.txt'), 'hello');

      await copier.copyFile('test.txt', 'nested/dir/test.txt');

      const content = await fsp.readFile(path.join(targetDir, 'nested/dir/test.txt'), 'utf8');
      expect(content).toBe('hello');
    });

    it('should track copied files in stats', async () => {
      const copier = new Copier(sourceDir, targetDir);
      await fsp.writeFile(path.join(sourceDir, 'a.txt'), 'a');
      await fsp.writeFile(path.join(sourceDir, 'b.txt'), 'b');

      await copier.copyFile('a.txt', 'a.txt');
      await copier.copyFile('b.txt', 'b.txt');

      expect(copier.getStats().filesCopied).toBe(2);
      expect(copier.getInstalledFiles()).toEqual(['a.txt', 'b.txt']);
    });

    it('should throw if source file does not exist', async () => {
      const copier = new Copier(sourceDir, targetDir);
      await expect(copier.copyFile('missing.txt', 'missing.txt'))
        .rejects.toThrow('Source file not found');
    });
  });

  // Skip permission tests on Windows (chmod is a no-op on NTFS)
  const describeUnix = process.platform === 'win32' ? describe.skip : describe;

  describeUnix('executable permissions (Unix only)', () => {
    it('should set +x on .sh files even when source lacks execute bit', async () => {
      const copier = new Copier(sourceDir, targetDir);
      const srcFile = path.join(sourceDir, 'hook.sh');
      await fsp.writeFile(srcFile, '#!/bin/bash\necho hello');
      // Simulate NTFS-packed file: no execute bit
      await fsp.chmod(srcFile, 0o644);

      await copier.copyFile('hook.sh', 'hook.sh');

      const destStat = await fsp.stat(path.join(targetDir, 'hook.sh'));
      // Check that execute bits are set (owner, group, other)
      expect(destStat.mode & 0o111).not.toBe(0);
      // Specifically expect 0o755
      expect(destStat.mode & 0o777).toBe(0o755);
    });

    it('should set +x on .py files even when source lacks execute bit', async () => {
      const copier = new Copier(sourceDir, targetDir);
      const srcFile = path.join(sourceDir, 'validate.py');
      await fsp.writeFile(srcFile, '#!/usr/bin/env python3\nprint("hello")');
      await fsp.chmod(srcFile, 0o644);

      await copier.copyFile('validate.py', 'validate.py');

      const destStat = await fsp.stat(path.join(targetDir, 'validate.py'));
      expect(destStat.mode & 0o777).toBe(0o755);
    });

    it('should set +x on devforgeai-validate wrapper', async () => {
      const copier = new Copier(sourceDir, targetDir);
      const srcFile = path.join(sourceDir, 'devforgeai-validate');
      await fsp.writeFile(srcFile, '#!/bin/bash\npython3 -m devforgeai_cli.cli "$@"');
      await fsp.chmod(srcFile, 0o644);

      await copier.copyFile('devforgeai-validate', 'devforgeai-validate');

      const destStat = await fsp.stat(path.join(targetDir, 'devforgeai-validate'));
      expect(destStat.mode & 0o777).toBe(0o755);
    });

    it('should preserve original permissions on non-script files', async () => {
      const copier = new Copier(sourceDir, targetDir);
      const srcFile = path.join(sourceDir, 'readme.md');
      await fsp.writeFile(srcFile, '# Hello');
      await fsp.chmod(srcFile, 0o644);

      await copier.copyFile('readme.md', 'readme.md');

      const destStat = await fsp.stat(path.join(targetDir, 'readme.md'));
      expect(destStat.mode & 0o777).toBe(0o644);
    });

    it('should not downgrade permissions if source already has +x', async () => {
      const copier = new Copier(sourceDir, targetDir);
      const srcFile = path.join(sourceDir, 'already-exec.sh');
      await fsp.writeFile(srcFile, '#!/bin/bash');
      await fsp.chmod(srcFile, 0o755);

      await copier.copyFile('already-exec.sh', 'already-exec.sh');

      const destStat = await fsp.stat(path.join(targetDir, 'already-exec.sh'));
      expect(destStat.mode & 0o777).toBe(0o755);
    });
  });

  describe('copyDirectory', () => {
    it('should recursively copy a directory', async () => {
      const copier = new Copier(sourceDir, targetDir);
      await fsp.mkdir(path.join(sourceDir, 'subdir'), { recursive: true });
      await fsp.writeFile(path.join(sourceDir, 'subdir', 'file.txt'), 'content');

      await copier.copyDirectory('subdir', 'subdir');

      const content = await fsp.readFile(path.join(targetDir, 'subdir', 'file.txt'), 'utf8');
      expect(content).toBe('content');
    });

    it('should throw if source directory does not exist', async () => {
      const copier = new Copier(sourceDir, targetDir);
      await expect(copier.copyDirectory('missing', 'missing'))
        .rejects.toThrow('Source directory not found');
    });
  });

  describe('template processing', () => {
    it('should replace template variables in text files', async () => {
      const copier = new Copier(sourceDir, targetDir);
      await fsp.writeFile(path.join(sourceDir, 'config.md'), 'Project: {{PROJECT_NAME}}');

      await copier.copyFile('config.md', 'config.md', {
        template: true,
        variables: { PROJECT_NAME: 'MyApp' },
      });

      const content = await fsp.readFile(path.join(targetDir, 'config.md'), 'utf8');
      expect(content).toBe('Project: MyApp');
    });
  });

  describe('createDirectories', () => {
    it('should create directories and track them', async () => {
      const copier = new Copier(sourceDir, targetDir);
      await copier.createDirectories(['dir1/', 'dir2/sub/']);

      expect(copier.getCreatedDirs()).toEqual(['dir1/', 'dir2/sub/']);
      expect(copier.getStats().directoriesCreated).toBe(2);
    });
  });

  describe('constructor', () => {
    it('should throw without sourceRoot', () => {
      expect(() => new Copier(null, '/target')).toThrow('requires both');
    });

    it('should throw without targetRoot', () => {
      expect(() => new Copier('/source', '')).toThrow('requires both');
    });
  });
});
