'use strict';

const COMPONENTS = [
  {
    id: 'core-framework',
    name: 'Core Framework',
    description: 'CLAUDE.md, rules, memory, and context files (required)',
    required: true,
    defaultSelected: true,
    sources: [
      { from: 'CLAUDE.md', to: 'CLAUDE.md', template: true },
      { from: 'src/claude/rules/', to: '.claude/rules/', template: false },
      { from: 'src/claude/memory/', to: '.claude/memory/', template: false },
    ],
  },
  {
    id: 'agents',
    name: 'Agents',
    description: 'AI agent definitions for task delegation',
    required: false,
    defaultSelected: true,
    sources: [
      { from: 'src/claude/agents/', to: '.claude/agents/', template: false },
    ],
  },
  {
    id: 'skills',
    name: 'Skills',
    description: 'Workflow skills for development lifecycle phases',
    required: false,
    defaultSelected: true,
    sources: [
      { from: 'src/claude/skills/', to: '.claude/skills/', template: false },
    ],
  },
  {
    id: 'commands',
    name: 'Commands',
    description: 'Slash commands for common operations',
    required: false,
    defaultSelected: true,
    sources: [
      { from: 'src/claude/commands/', to: '.claude/commands/', template: false },
    ],
  },
  {
    id: 'hooks',
    name: 'Hooks',
    description: 'Git and lifecycle hooks',
    required: false,
    defaultSelected: true,
    sources: [
      { from: 'src/claude/hooks/', to: '.claude/hooks/', template: false },
    ],
  },
  {
    id: 'python-cli',
    name: 'Python CLI',
    description: 'Python scripts for validation and utilities',
    required: false,
    defaultSelected: true,
    sources: [
      { from: 'src/claude/scripts/', to: '.claude/scripts/', template: false },
    ],
  },
  {
    id: 'project-structure',
    name: 'Project Structure',
    description: 'Standard directory layout for DevForgeAI projects',
    required: false,
    defaultSelected: true,
    directories: [
      'devforgeai/',
    ],
    sources: [
      { from: 'docs/api/', to: 'docs/api/', template: false },
      { from: 'docs/architecture/', to: 'docs/architecture/', template: false },
      { from: 'docs/guides/', to: 'docs/guides/', template: false },
    ],
  },
];

function getComponent(id) {
  return COMPONENTS.find((c) => c.id === id) || null;
}

function getRequiredComponents() {
  return COMPONENTS.filter((c) => c.required);
}

function getDefaultComponents() {
  return COMPONENTS.filter((c) => c.required || c.defaultSelected);
}

function getAllComponents() {
  return [...COMPONENTS];
}

function getComponentChoices() {
  return COMPONENTS.map((c) => ({
    name: `${c.name} - ${c.description}`,
    value: c.id,
    checked: c.defaultSelected || c.required,
    disabled: c.required ? 'Required' : false,
  }));
}

module.exports = {
  COMPONENTS,
  getComponent,
  getRequiredComponents,
  getDefaultComponents,
  getAllComponents,
  getComponentChoices,
};
