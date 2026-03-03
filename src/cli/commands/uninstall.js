const path = require('path');
const fs = require('fs').promises;
const chalk = require('chalk');
const inquirer = require('inquirer');
const { Detector } = require('../lib/detector');
const { ManifestManager } = require('../lib/manifest');

const command = 'uninstall [directory]';
const description = 'Remove DevForgeAI framework from a project';
const options = [
  ['-y, --yes', 'Skip confirmation prompt'],
];

async function action(directory, opts) {
  const targetRoot = path.resolve(directory || '.');
  const detector = new Detector(targetRoot);
  const detection = await detector.detect();

  if (!detection.exists) {
    console.log(chalk.yellow('No DevForgeAI installation found in ' + targetRoot));
    return;
  }

  // Framework directories to remove (NOT user code like src/, tests/, docs/)
  const frameworkDirs = ['.claude', 'devforgeai'];
  const frameworkFiles = ['CLAUDE.md', '.devforgeai-manifest.json'];

  console.log(chalk.yellow.bold('\nThe following will be removed:\n'));
  for (const dir of frameworkDirs) {
    const fullPath = path.join(targetRoot, dir);
    try {
      await fs.access(fullPath);
      console.log(chalk.red(`  📁 ${dir}/`));
    } catch { /* doesn't exist */ }
  }
  for (const file of frameworkFiles) {
    const fullPath = path.join(targetRoot, file);
    try {
      await fs.access(fullPath);
      console.log(chalk.red(`  📄 ${file}`));
    } catch { /* doesn't exist */ }
  }
  console.log(chalk.gray('\n  User code (src/, tests/, docs/) will NOT be removed.\n'));

  if (!opts.yes) {
    const answer = await inquirer.prompt([{
      type: 'confirm',
      name: 'confirm',
      message: 'Are you sure you want to uninstall DevForgeAI?',
      default: false,
    }]);
    if (!answer.confirm) {
      console.log(chalk.gray('Uninstall cancelled.'));
      return;
    }
  }

  // Remove framework directories
  for (const dir of frameworkDirs) {
    const fullPath = path.join(targetRoot, dir);
    try {
      await fs.rm(fullPath, { recursive: true, force: true });
      console.log(chalk.green(`  ✓ Removed ${dir}/`));
    } catch (e) {
      console.log(chalk.yellow(`  ⚠ Could not remove ${dir}/: ${e.message}`));
    }
  }

  // Remove framework files
  for (const file of frameworkFiles) {
    const fullPath = path.join(targetRoot, file);
    try {
      await fs.unlink(fullPath);
      console.log(chalk.green(`  ✓ Removed ${file}`));
    } catch { /* doesn't exist, ok */ }
  }

  console.log(chalk.green.bold('\n✓ DevForgeAI uninstalled successfully.\n'));
}

module.exports = { command, description, options, action };
