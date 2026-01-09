/**
 * STORY-248: GUI Installer Template - Electron Builder Config Tests
 * TDD Red Phase: These tests MUST FAIL initially (no config exists)
 *
 * Test Framework: Jest 30+
 * Coverage: electron-builder configuration validation
 */

const fs = require('fs');
const path = require('path');

describe('STORY-248: Electron Builder Configuration', () => {
  let builderConfig;
  const configPath = path.join(__dirname, '..', 'build', 'builder-config.json');

  beforeAll(() => {
    // This will fail until builder-config.json exists
    const configContent = fs.readFileSync(configPath, 'utf8');
    builderConfig = JSON.parse(configContent);
  });

  describe('Basic Configuration', () => {
    test('should_have_valid_appId', () => {
      expect(builderConfig.appId).toBe('com.devforgeai.installer');
    });

    test('should_have_correct_productName', () => {
      expect(builderConfig.productName).toBe('DevForgeAI Installer');
    });

    test('should_specify_output_directory', () => {
      expect(builderConfig.directories).toBeDefined();
      expect(builderConfig.directories.output).toBe('dist');
    });
  });

  describe('File Inclusion', () => {
    test('should_include_main_js', () => {
      expect(builderConfig.files).toContain('main.js');
    });

    test('should_include_preload_js', () => {
      expect(builderConfig.files).toContain('preload.js');
    });

    test('should_include_renderer_directory', () => {
      expect(builderConfig.files).toContain('renderer/**/*');
    });

    test('should_include_assets_directory', () => {
      expect(builderConfig.files).toContain('assets/**/*');
    });
  });

  describe('Windows Configuration (AC#8)', () => {
    test('should_configure_windows_nsis_target', () => {
      expect(builderConfig.win).toBeDefined();
      expect(builderConfig.win.target).toBe('nsis');
    });

    test('should_specify_windows_icon', () => {
      expect(builderConfig.win.icon).toMatch(/\.ico$/);
    });
  });

  describe('macOS Configuration (AC#8)', () => {
    test('should_configure_macos_dmg_target', () => {
      expect(builderConfig.mac).toBeDefined();
      expect(builderConfig.mac.target).toBe('dmg');
    });

    test('should_specify_macos_icon', () => {
      expect(builderConfig.mac.icon).toMatch(/\.icns$/);
    });
  });

  describe('Linux Configuration (AC#8)', () => {
    test('should_configure_linux_targets', () => {
      expect(builderConfig.linux).toBeDefined();
      expect(builderConfig.linux.target).toEqual(
        expect.arrayContaining(['AppImage', 'deb'])
      );
    });

    test('should_specify_linux_icon', () => {
      expect(builderConfig.linux.icon).toMatch(/\.png$/);
    });
  });

  describe('Security Configuration', () => {
    test('should_have_asar_packaging_enabled', () => {
      // ASAR packaging improves security and load time
      expect(builderConfig.asar).not.toBe(false);
    });
  });
});
