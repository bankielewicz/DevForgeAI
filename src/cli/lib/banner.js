const chalk = require('chalk');

function displayBanner(version) {
  const g = chalk.gray;

  // Plain text banner - no box, just clean ASCII art with color
  const lines = [
    '',
    chalk.white.bold('    ____             ______                         ___   ____'),
    chalk.white.bold('   / __ \\  ___ _  __/ ____/___  _________ ____    /   |  /  /'),
    chalk.white.bold('  / / / / / _ \\ | / / /_  / __ \\/ ___/ __ `/ _ \\ / /| | /  /  '),
    chalk.white.bold(' / /_/ / /  __/ V / __/ / /_/ / /  / /_/ /  __// ___  |/  /   '),
    chalk.white.bold('/_____/  \\___/\\_/ /_/    \\____/_/   \\__, /\\___/ //  |_/__/   '),
    chalk.white.bold('                                   /____/                     '),
    '',
    chalk.yellow.bold('  Spec-Driven Development Framework') + g(`  v${version}`),
    '',
    g('  Zero technical debt. AI-powered quality gates.'),
    '',
  ];

  console.log(lines.join('\n'));
}

module.exports = { displayBanner };
