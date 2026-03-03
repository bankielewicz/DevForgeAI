# Security Policy

## Supported Versions

| Version | Supported |
|---------|-----------|
| 1.0.x   | Yes       |

## Reporting a Vulnerability

**Please do not report security vulnerabilities through public GitHub issues.**

Instead, please report them via email to the maintainers. You can find contact information on the [repository owner's GitHub profile](https://github.com/bankielewicz).

### What to Include

- Description of the vulnerability
- Steps to reproduce
- Potential impact
- Suggested fix (if any)

### Response Timeline

- **Acknowledgment:** Within 48 hours
- **Initial assessment:** Within 1 week
- **Resolution target:** Within 30 days for critical issues

### What to Expect

1. You will receive an acknowledgment of your report
2. We will investigate and determine the impact
3. We will develop and test a fix
4. We will release a patch and credit you (unless you prefer anonymity)

## Scope

### In Scope

- Vulnerabilities in the DevForgeAI CLI tools (`devforgeai`, `devforgeai-validate`)
- Security issues in pre-commit hooks or validation scripts
- Sensitive data exposure in generated files or logs
- Issues in the NPM package distribution

### Out of Scope

- Vulnerabilities in Claude Code Terminal itself (report to Anthropic)
- Issues in third-party dependencies (report to the dependency maintainer, but let us know too)
- Security of projects built using DevForgeAI (those are governed by the project's own context files)

## Security Practices

DevForgeAI enforces several security practices by design:

- **No hardcoded secrets** -- Anti-patterns file forbids API keys, passwords, and private keys in source code
- **Input validation rules** -- Built-in rules in `.claude/rules/security/` enforce parameterized queries and XSS prevention
- **Immutable constraints** -- Constitutional context files prevent unauthorized technology or dependency changes
- **Pre-commit validation** -- Git hooks block commits that violate security rules
