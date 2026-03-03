const path = require('path');
const chalk = require('chalk');
const { Detector } = require('../lib/detector');
const { ManifestManager } = require('../lib/manifest');

const command = 'status [directory]';
const description = 'Show DevForgeAI installation status';
const options = [];

async function action(directory) {
  const targetRoot = path.resolve(directory || '.');
  const detector = new Detector(targetRoot);
  const detection = await detector.detect();

  if (!detection.exists) {
    console.log(chalk.yellow('No DevForgeAI installation found in ' + targetRoot));
    return;
  }

  const manifest = new ManifestManager(targetRoot);
  const data = await manifest.read();

  if (!data) {
    console.log(chalk.yellow('DevForgeAI files detected but no manifest found.'));
    console.log('  .claude/ directory: ' + (detection.hasClaudeDir ? chalk.green('Yes') : chalk.red('No')));
    console.log('  devforgeai/ directory: ' + (detection.hasDevforgeaiDir ? chalk.green('Yes') : chalk.red('No')));
    console.log('  CLAUDE.md: ' + (detection.hasClaudeMd ? chalk.green('Yes') : chalk.red('No')));
    return;
  }

  console.log(chalk.cyan.bold('\nDevForgeAI Installation Status\n'));
  console.log(`  Version:      ${chalk.white(data.version)}`);
  console.log(`  Project:      ${chalk.white(data.projectName)}`);
  console.log(`  Installed:    ${chalk.gray(data.installDate)}`);
  console.log(`  Last Updated: ${chalk.gray(data.lastUpdated)}`);
  console.log(`  IDE:          ${chalk.white((data.ide || []).join(', '))}`);
  console.log('');
  console.log(chalk.cyan('  Modules:'));
  (data.modules || []).forEach(mod => {
    const status = mod.installed ? chalk.green('✓') : chalk.red('✗');
    console.log(`    ${status} ${mod.name}`);
  });
  console.log('');
}

module.exports = { command, description, options, action };
