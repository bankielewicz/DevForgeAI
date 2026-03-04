# DevForgeAI

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Node.js >= 18](https://img.shields.io/badge/Node.js-%3E%3D18-green.svg)](https://nodejs.org/)
[![Built with Claude Code](https://img.shields.io/badge/Built%20with-Claude%20Code-blueviolet.svg)](https://docs.anthropic.com/en/docs/claude-code)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](CONTRIBUTING.md)

> **Transform vague business ideas into production-ready code with zero technical debt.**

DevForgeAI is a development framework for [Claude Code](https://docs.anthropic.com/en/docs/claude-code) that enforces TDD, quality gates, and architectural constraints across the entire software lifecycle. It works with **any technology stack**.

**[Interactive Demo (Coming Soon)](https://www.devforgeai.com)** | **[Full Documentation](docs/)**

---

## Quick Start

```bash
# Install into your project
npx devforgeai install

# Open in Claude Code Terminal, then:

/create-context my-project        # Set up architectural constraints
/create-story user-authentication # Create a spec'd user story
/dev STORY-001                    # Build it with enforced TDD
/qa STORY-001 deep                # Validate quality
```

Or start from scratch with a vague idea:

```bash
/brainstorm "I want to build a marketplace for local artisans"
# The framework guides you from idea -> requirements -> architecture -> code -> release
```

---

## See It in Action

<p align="center">
  <a href="https://www.devforgeai.com">
    <img src="https://img.shields.io/badge/Interactive%20Demo-Coming%20Soon-blueviolet?style=for-the-badge&logo=data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIyNCIgaGVpZ2h0PSIyNCIgdmlld0JveD0iMCAwIDI0IDI0IiBmaWxsPSJub25lIiBzdHJva2U9IndoaXRlIiBzdHJva2Utd2lkdGg9IjIiPjxwb2x5Z29uIHBvaW50cz0iNSAzIDIxIDEyIDUgMjEgNSAzIi8+PC9zdmc+" alt="Interactive Demo">
  </a>
</p>

Explore the full development pipeline, TDD cycle, quality gates, and architecture — all interactive, right in your browser.

**[www.devforgeai.com](https://www.devforgeai.com)**

---

## Why DevForgeAI?

AI coding assistants are powerful but undisciplined. Without guardrails, they make autonomous technology decisions, skip tests, and accumulate technical debt faster than any human team.

DevForgeAI fixes this with three mechanisms:

**1. Constitutional Context Files** — 6 immutable documents define your approved technologies, directory structure, dependencies, coding standards, architecture constraints, and forbidden anti-patterns. The AI cannot deviate without an approved Architecture Decision Record.

**2. Mandatory TDD** — Every feature goes through a 10-phase cycle: write failing tests first, implement minimum code to pass, refactor, verify acceptance criteria, run integration tests. No shortcuts.

**3. Quality Gates** — 4 checkpoints block progression until standards are met. Coverage thresholds (95% business logic, 85% application, 80% infrastructure) are enforced as blockers, not warnings.

---

## Key Features

- **Technology Agnostic** — Works with any stack. Your context files define the rules, not the framework.
- **44 Specialized Subagents** — Single-responsibility AI agents: test-automator, backend-architect, security-auditor, code-reviewer, and 40 more.
- **46 Slash Commands** — From `/brainstorm` to `/release`, every workflow step has a dedicated command.
- **Root Cause Analysis** — Built-in `/rca` command with 5 Whys methodology when things go wrong.
- **Test Integrity Protection** — Only designated agents can write tests during designated phases, preventing implementation agents from weakening assertions.
- **Cross-AI Collaboration** — `/collaborate` generates portable documents for sharing issues with other LLMs.

---

## Installation

**Prerequisites:** Node.js >= 18, npm >= 8, Git, [Claude Code Terminal](https://docs.anthropic.com/en/docs/claude-code)

```bash
# Recommended
npx devforgeai install

# From source
git clone https://github.com/bankielewicz/DevForgeAI.git
cd DevForgeAI && npm install
node bin/devforgeai.js install /path/to/your-project

# Global
npm install -g devforgeai
devforgeai install
```

After installing, run `/create-context my-project` in Claude Code to generate your constitutional context files interactively.

---

## How the Workflow Fits Together

```
/brainstorm     Vague idea -> structured problem discovery
      |
/ideate         Problem -> requirements (functional + non-functional)
      |
/create-context Requirements -> 6 constitutional constraint files
      |
/create-epic    Constraints -> feature decomposition
      |
/create-story   Features -> implementable stories with acceptance criteria
      |
/dev            Story -> TDD implementation (10 phases, enforced)
      |
/qa             Code -> quality validation (coverage, security, patterns)
      |
/release        Validated code -> production deployment
```

---

## Documentation

| Topic | Location |
|-------|----------|
| All 46 commands | [Commands Reference](docs/guides/DEVELOPER-GUIDE.md) |
| Architecture & subagents | [Architecture Guide](docs/architecture/ARCHITECTURE.md) |
| API documentation | [API Reference](docs/api/API.md) |
| Troubleshooting | [Troubleshooting Guide](docs/guides/TROUBLESHOOTING.md) |
| Project roadmap | [Roadmap](docs/guides/ROADMAP.md) |
| Competitive analysis | [Research](devforgeai/specs/research/research-index.md) |

---

## Contributing

1. Fork the repository
2. Create a feature branch
3. Use the DevForgeAI workflow: `/create-story` -> `/dev` -> `/qa`
4. Push and open a Pull Request

See [CONTRIBUTING.md](CONTRIBUTING.md) for full guidelines.

---

## Support

If DevForgeAI has been useful, consider buying me a coffee!

<a href="https://buymeacoffee.com/devforgeai" target="_blank">
  <img src="https://cdn.buymeacoffee.com/buttons/v2/default-yellow.png" alt="Buy Me A Coffee" height="50">
</a>

---

## License

MIT License — see [LICENSE](LICENSE) for details.

---

<p align="center">
  <strong>Built with Claude Code</strong> — Spec-driven development with 44 subagents, 26 skills, and zero tolerance for technical debt.
</p>
