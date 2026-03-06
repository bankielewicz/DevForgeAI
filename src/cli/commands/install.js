const path = require('path');
const fs = require('fs');
const fsp = fs.promises;
const { OutputFormatter } = require('../wizard/output-formatter');
const { ProgressService } = require('../wizard/progress-service');
const { SignalHandler } = require('../wizard/signal-handler');
const { PromptService } = require('../wizard/prompt-service');
const { displayBanner } = require('../lib/banner');
const { Copier } = require('../lib/copier');
const { ManifestManager } = require('../lib/manifest');
const { Detector } = require('../lib/detector');
const { getAllComponents, getDefaultComponents, getComponentChoices, getComponent } = require('../lib/components');
const { ClaudeCodeIDE } = require('../lib/ide/claude-code');

// Resolve the framework source root (where the package files live)
function getSourceRoot() {
  // Go up from src/cli/commands/ to package root
  return path.resolve(__dirname, '..', '..', '..');
}

function getVersion() {
  const pkg = require(path.join(getSourceRoot(), 'package.json'));
  return pkg.version;
}

const command = 'install [directory]';
const description = 'Install DevForgeAI framework into a project';

const options = [
  ['-y, --yes', 'Skip all prompts, use defaults'],
  ['-q, --quiet', 'Suppress non-error output'],
  ['--skip-python', 'Skip Python CLI installation'],
];

async function action(directory, opts) {
  const targetRoot = path.resolve(directory || '.');
  const version = getVersion();
  const formatter = new OutputFormatter({ quiet: opts.quiet });
  const progress = new ProgressService({ quiet: opts.quiet });
  const signalHandler = new SignalHandler({ outputFormatter: formatter });
  const promptService = new PromptService({ outputFormatter: formatter });
  const detector = new Detector(targetRoot);
  const inquirer = require('inquirer');

  signalHandler.register();

  try {
    // Phase 1: Welcome
    if (!opts.quiet) {
      displayBanner(version);
    }

    // Phase 2: Directory (already resolved from argument, or prompt)
    let installDir = targetRoot;
    if (!opts.yes && !directory) {
      const answer = await inquirer.prompt([{
        type: 'input',
        name: 'directory',
        message: 'Where do you want to install DevForgeAI?',
        default: '.',
      }]);
      installDir = path.resolve(answer.directory);
    }

    // Phase 3: Detection
    const detection = await detector.detect();
    if (detection.exists) {
      if (!opts.quiet) {
        formatter.warning('Existing DevForgeAI installation detected.');
      }
      if (!opts.yes) {
        const answer = await inquirer.prompt([{
          type: 'list',
          name: 'action',
          message: 'What would you like to do?',
          choices: [
            { name: 'Update — re-copy framework files, preserve context files', value: 'update' },
            { name: 'Reinstall — overwrite everything', value: 'reinstall' },
            { name: 'Cancel', value: 'cancel' },
          ],
        }]);
        if (answer.action === 'cancel') {
          formatter.info('Installation cancelled.');
          return;
        }
        // For update mode, we'll skip context files later
        if (answer.action === 'update') {
          opts._updateMode = true;
        }
      }
    }

    // Phase 4: Component Selection
    let selectedComponents;
    if (opts.yes) {
      selectedComponents = getDefaultComponents().map(c => c.id);
    } else {
      const choices = getComponentChoices();
      const answer = await inquirer.prompt([{
        type: 'checkbox',
        name: 'components',
        message: 'Select components to install:',
        choices,
        validate: (input) => input.length > 0 ? true : 'Select at least one component.',
      }]);
      // Always include required components
      const required = getAllComponents().filter(c => c.required).map(c => c.id);
      selectedComponents = [...new Set([...required, ...answer.components])];
    }

    // Phase 5: Python check (conditional)
    if (selectedComponents.includes('python-cli')) {
      if (opts.skipPython) {
        selectedComponents = selectedComponents.filter(id => id !== 'python-cli');
        if (!opts.quiet) formatter.info('Skipping Python CLI (--skip-python).');
      } else {
        try {
          const { checkPython } = require('../../../lib/cli');
          checkPython();
        } catch (e) {
          selectedComponents = selectedComponents.filter(id => id !== 'python-cli');
          if (!opts.quiet) formatter.warning('Python 3.10+ not found. Skipping Python CLI.');
        }
      }
    }

    // Phase 6: Configuration
    let projectName = path.basename(installDir);
    if (!opts.yes) {
      const answer = await inquirer.prompt([{
        type: 'input',
        name: 'projectName',
        message: 'Project name:',
        default: projectName,
      }]);
      projectName = answer.projectName;
    }

    // Phase 7: Installation
    const sourceRoot = getSourceRoot();
    const copier = new Copier(sourceRoot, installDir);
    const variables = { PROJECT_NAME: projectName };

    if (!opts.quiet) {
      formatter.info(`Installing DevForgeAI to ${installDir}...`);
    }
    progress.startSpinner('Installing components...');

    let totalFiles = 0;
    for (const componentId of selectedComponents) {
      const component = getComponent(componentId);
      if (!component) continue;

      progress.updateSpinnerText(`Installing ${component.name}...`);

      if (component.directories) {
        await copier.createDirectories(component.directories);
      }

      if (component.sources) {
        for (const source of component.sources) {
          // In update mode, skip context files
          if (opts._updateMode && source.from === 'devforgeai/specs/context/') {
            continue;
          }
          const copyOpts = source.template ? { template: true, variables } : {};
          try {
            await copier.copyDirectory(source.from, source.to, copyOpts);
          } catch (e) {
            // If directory doesn't exist, try as file
            try {
              await copier.copyFile(source.from, source.to, copyOpts);
            } catch (e2) {
              formatter.warning(`Could not copy ${source.from}: ${e2.message}`);
            }
          }
        }
      }
    }

    // Python CLI pip install (uses venv to avoid PEP 668 externally-managed errors)
    if (selectedComponents.includes('python-cli')) {
      progress.updateSpinnerText('Installing Python CLI...');
      try {
        const { execSync } = require('child_process');
        const scriptsDir = path.join(installDir, '.claude', 'scripts');
        const venvDir = path.join(installDir, '.venv');

        // Create venv if it doesn't exist
        try {
          await fsp.access(path.join(venvDir, 'bin', 'pip'));
        } catch {
          execSync(`python3 -m venv "${venvDir}"`, { stdio: 'pipe', cwd: installDir });
        }

        // Install into venv
        const venvPip = path.join(venvDir, 'bin', 'pip');
        execSync(`"${venvPip}" install -e "${scriptsDir}"`, { stdio: 'pipe', cwd: installDir });

        if (!opts.quiet) {
          formatter.info('Python CLI installed in .venv/ — activate with: source .venv/bin/activate');
        }
      } catch (e) {
        formatter.warning(`Python CLI install failed: ${e.message}`);
      }
    }

    progress.stopSpinner({ success: true, message: 'Components installed.' });

    // Phase 8: Manifest
    const manifest = new ManifestManager(installDir);
    const stats = copier.getStats();
    const moduleData = selectedComponents.map(id => ({
      name: id,
      installed: true,
    }));
    await manifest.create({
      version,
      projectName,
      modules: moduleData,
      ide: ['claude-code'],
    });

    // IDE setup (merge settings on update, overwrite on reinstall)
    const claudeCode = new ClaudeCodeIDE();
    const ideResult = await claudeCode.setup(installDir, copier, {
      reinstall: !opts._updateMode,
    });
    if (!opts.quiet && ideResult.message) {
      formatter.info(ideResult.message);
    }

    // Phase 9: Summary
    if (!opts.quiet) {
      console.log('');
      formatter.success(`DevForgeAI v${version} installed successfully!`);
      console.log('');
      console.log(`  Project:    ${projectName}`);
      console.log(`  Directory:  ${installDir}`);
      console.log(`  Components: ${selectedComponents.length}`);
      console.log(`  Files:      ${stats.filesCopied}`);
      console.log(`  Dirs:       ${stats.directoriesCreated}`);
      console.log('');
      formatter.info('Next steps:');
      console.log('  1. Run /create-context to generate your project context files');
      console.log('  2. Run /brainstorm to start your first project');
      console.log('  3. See docs/ for guides and documentation');
      console.log('');
    }
  } catch (error) {
    progress.stopSpinner({ success: false });
    formatter.error(`Installation failed: ${error.message}`);
    throw error;
  } finally {
    signalHandler.unregister();
  }
}

module.exports = { command, description, options, action };
