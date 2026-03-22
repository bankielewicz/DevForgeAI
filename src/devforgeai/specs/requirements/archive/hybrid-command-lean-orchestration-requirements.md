---
# =============================================================================
# REQUIREMENTS SPECIFICATION
# =============================================================================
# Schema Version: 1.0 (STORY-435)
# Purpose: Structured requirements for cross-session AI consumption
#
# IMPORTANT: This YAML frontmatter contains ALL structured data.
# The markdown body below is for human readability only - do not duplicate data.
#
# PROVENANCE: Derived from /audit-hybrid results + Anthropic documentation analysis
# PLAN FILE: .claude/plans/piped-baking-crystal.md (full refactoring roadmap)

schema_version: "1.0"
document_id: "REQ-071"
title: "Hybrid Command Lean Orchestration Refactoring"
created: "2026-02-20"
last_updated: "2026-02-20"
status: "Draft"

# =============================================================================
# DECISIONS (locked choices with excluded options)
# =============================================================================
# Each decision corresponds to a refactoring pattern from the roadmap.
# Anthropic documentation citations are embedded in rationale fields.
decisions:
  - id: "DR-1"
    domain: "command-architecture"
    decision: "All 20 audited commands adopt the lean orchestration pattern: Validate args, Set context markers, Invoke skill. Zero business logic in commands."
    rejected:
      - option: "Keep business logic inline in commands for commands under 300 lines"
        reason: "Even short commands with inline logic violate separation of concerns, waste context window tokens, and create maintenance burden when logic changes"
      - option: "Create standalone scripts instead of skills for extracted logic"
        reason: "Scripts bypass the progressive disclosure model (Three-Tier Loading) and cannot leverage subagent delegation pattern"
    rationale: "DevForgeAI Lean Orchestration Protocol (devforgeai/protocols/lean-orchestration-pattern.md) mandates: 'Commands orchestrate. Skills validate. Subagents specialize.' Anthropic best-practices.md: 'Concise is key -- the context window is a public good... every token competes with conversation history.'"
    locked: true

  - id: "DR-2"
    domain: "refactoring-pattern-a"
    decision: "Pattern A (Full Workflow Extraction): Commands with embedded validation + display + interaction logic create/extend a dedicated skill to absorb all Phases 1-2+ logic. Optionally create a result-interpreter subagent for display formatting exceeding 50 lines."
    rejected:
      - option: "Move only display logic to skills, keep validation in command"
        reason: "Partial extraction leaves business logic in commands, still violating lean orchestration. Validation algorithms (gap detection, coverage calculation) are business logic, not argument parsing."
      - option: "Combine all extracted logic into one monolithic skill"
        reason: "Violates Single Responsibility Principle per architecture-constraints.md and Anthropic's progressive disclosure model. Each skill handles ONE phase of development lifecycle."
    rationale: "Anthropic chain-complex-prompts.md: 'Breaking down complex tasks into smaller, manageable subtasks... each subtask gets Claude's full attention, reducing errors.' Anthropic best-practices.md: 'Use workflows for complex tasks -- break complex operations into clear, sequential steps.'"
    locked: true

  - id: "DR-3"
    domain: "refactoring-pattern-b"
    decision: "Pattern B (Pre-Flight Logic Extraction): Commands with inline pre-flight validation and DoD parsing move those checks into the target skill's Phase 0 and resumption logic."
    rejected:
      - option: "Keep pre-flight checks in command as a shared validation library"
        reason: "Commands cannot import shared libraries. Pre-flight checks are contextual to the skill's workflow and need access to skill state (phase markers, story context)."
    rationale: "Anthropic agent-skills-spec.md Three-Tier Loading Model: 'Progressive disclosure -- load detailed materials only when needed.' Pre-flight logic loaded at Execution tier, not Discovery tier."
    locked: true

  - id: "DR-4"
    domain: "refactoring-pattern-c"
    decision: "Pattern C (Multi-Phase Slimming): Commands that correctly invoke a skill but have excessive pre/post-skill logic move mode detection and context probing into skill Phase 0, and result interpretation into skill post-execution phases. All slimmed commands add a 'DO NOT' guardrail section."
    rejected:
      - option: "Accept pre-skill probing as necessary command overhead"
        reason: "Mode detection via Glob/Read in commands consumes main conversation tokens unnecessarily. Skills can perform the same detection in isolated context at zero main-conversation cost."
    rationale: "Anthropic best-practices.md: 'Concise is key -- the context window is a public good.' The gold standard create-story.md (73 lines, 1 block) proves that even complex workflows need only argument validation in the command."
    locked: true

  - id: "DR-5"
    domain: "refactoring-pattern-d"
    decision: "Pattern D (Standalone Audit to Skill): Audit commands that embed scan+report logic without skill delegation create a lightweight skill to contain that logic."
    rejected:
      - option: "Keep audit commands as pure inline scripts since they are read-only"
        reason: "Read-only does not exempt from token efficiency requirements. A 240-line command with 6 code blocks still wastes main conversation tokens. Skill delegation isolates the scan context."
    rationale: "Anthropic best-practices.md: 'Keep SKILL.md under 500 lines -- split content into separate files when approaching this limit.' Even diagnostic commands benefit from skill delegation for token efficiency."
    locked: true

  - id: "DR-6"
    domain: "refactoring-pattern-e"
    decision: "Pattern E (Documentation Trimming): Commands bloated by help text, examples, or verbose error handling move that content to references/ files loaded on --help. Error handling condensed to 3-5 rows maximum."
    rejected:
      - option: "Inline all documentation for discoverability"
        reason: "Inline documentation is loaded every time the command is invoked, even when help is not requested. Progressive disclosure loads it only when needed, saving tokens on every non-help invocation."
    rationale: "Anthropic best-practices.md: 'Progressive disclosure -- SKILL.md serves as overview that points to detailed materials as needed.' Same principle applies to command files."
    locked: true

  - id: "DR-7"
    domain: "gold-standard-template"
    decision: "All refactored commands follow the create-story.md gold standard structure: YAML frontmatter, one-line description, 'Lean Orchestration Enforcement' section with DO NOT guardrails, Phase 0 argument validation (1-2 code blocks), Phase 1 skill invocation, error handling table (3-5 rows), references."
    rejected:
      - option: "Allow per-command customization of section structure"
        reason: "Inconsistent structure prevents automated auditing and increases cognitive load when maintaining commands. Uniform structure enables the audit-hybrid script to detect violations reliably."
    rationale: "Gold standard proven by create-story.md (73 lines, 1 block, zero violations). Template documented at devforgeai/protocols/lean-orchestration-pattern.md lines 50-89."
    locked: true

  - id: "DR-8"
    domain: "false-positive-handling"
    decision: "Three commands identified as false positives require NO changes: fix-story.md (all 6 blocks are argument validation), setup-github-actions.md (132 lines, all blocks are arg validation), dev.backup.md (DELETE as duplicate of dev.md)."
    rejected:
      - option: "Refactor all 20 flagged commands uniformly"
        reason: "fix-story.md and setup-github-actions.md have code blocks that are ALL legitimate argument parsing -- no business logic. Refactoring them would remove necessary validation. dev.backup.md is a file management issue, not an architecture violation."
    rationale: "The audit-hybrid script counts code blocks mechanically. Manual review confirms blocks in fix-story.md and setup-github-actions.md contain only regex validation, Glob checks, and AskUserQuestion fallbacks -- all legitimate command responsibilities per lean orchestration protocol."
    locked: true

  - id: "DR-9"
    domain: "batch-sequencing"
    decision: "Batches 1-3 execute sequentially (skill dependencies). Batches 4-7 execute in parallel (independent commands and skills)."
    rejected:
      - option: "Execute all batches sequentially"
        reason: "Unnecessary delay. Batches 4-7 modify different skills with no cross-dependencies."
      - option: "Execute all batches in parallel"
        reason: "Batches 1-3 create or extend skills that later batches might reference. Specifically: Batch 1 creates devforgeai-epic-validation skill; Batch 2 extends devforgeai-orchestration; Batch 3 extends implementing-stories."
    rationale: "Dependency analysis: Batch 1 artifacts (devforgeai-epic-validation skill) are not consumed by Batches 2-7. Batch 2 artifacts (devforgeai-orchestration extension) are not consumed by Batch 3. Batch 3 artifacts (implementing-stories extension) affect /dev command but that command is already refactored. Batches 4-7 touch distinct, independent skills."
    locked: true

# =============================================================================
# SCOPE
# =============================================================================
scope:
  in:
    - "Refactor validate-epic-coverage.md (14 blocks -> <=2 blocks, Pattern A, create devforgeai-epic-validation skill)"
    - "Refactor create-missing-stories.md (10 blocks -> <=2 blocks, Pattern A, extend devforgeai-epic-validation skill)"
    - "Refactor create-sprint.md (11 blocks -> <=3 blocks, Pattern A+C, extend devforgeai-orchestration skill)"
    - "Refactor recommendations-triage.md (10 blocks -> <=2 blocks, Pattern A, extend devforgeai-feedback skill)"
    - "Refactor resume-dev.md (11 blocks -> <=3 blocks, Pattern B, extend implementing-stories skill)"
    - "Refactor qa.md (8 blocks -> <=3 blocks, Pattern C, extend devforgeai-qa skill)"
    - "Refactor create-ui.md (8 blocks -> <=3 blocks, Pattern C, extend devforgeai-ui-generator skill)"
    - "Refactor ideate.md (7 blocks -> <=3 blocks, Pattern C, extend discovering-requirements skill)"
    - "Refactor audit-w3.md (6 blocks -> <=3 blocks, Pattern D, create devforgeai-w3-audit skill)"
    - "Refactor create-epic.md (6 blocks -> <=3 blocks, Pattern C+E, extend designing-systems skill)"
    - "Refactor create-stories-from-rca.md (6 blocks -> <=3 blocks, Pattern E, move help to reference file)"
    - "Refactor document.md (6 blocks -> <=3 blocks, Pattern C+E, move templates to reference file)"
    - "Refactor orchestrate.md (6 blocks -> <=3 blocks, Pattern E, move 200 lines docs to reference file)"
    - "Refactor rca.md (5 blocks -> <=3 blocks, Pattern C+E, move 150 lines examples to reference file)"
    - "Refactor insights.md (5 blocks -> <=3 blocks, Pattern C+E, move inline help to reference file)"
    - "Refactor create-agent.md (5 blocks -> <=3 blocks, Pattern C+E, move mode detection to skill)"
    - "Refactor feedback-search.md (4 blocks -> <=3 blocks, Pattern E, move 250 lines help to reference file)"
    - "Delete dev.backup.md (confirmed duplicate of dev.md, safe to delete)"
    - "Create epic-coverage-result-interpreter subagent for display formatting"
    - "Add 'Lean Orchestration Enforcement' DO NOT guardrail section to all refactored commands"
  out:
    - item: "fix-story.md (6 blocks) - false positive, all blocks are legitimate argument validation"
      deferral_target: "Never"
    - item: "setup-github-actions.md (4 blocks, 132 lines) - false positive, compliant at 132 lines"
      deferral_target: "Never"
    - item: "Warning commands with no Skill() invocation (14 commands: audit-budget, audit-hooks, audit-hybrid, audit-orphans, chat-search, dev-status, devforgeai-validate, export-feedback, feedback-config, feedback-export-data, feedback-reindex, import-feedback, prompt-version, read-constitution, validate-stories, worktrees)"
      deferral_target: "Phase 2 - Separate epic for standalone command refactoring"
    - item: "Updating the audit-hybrid script threshold from 4 to a lower number"
      deferral_target: "Post-MVP - After all commands refactored and baseline established"

# =============================================================================
# SUCCESS CRITERIA (quantified, measurable)
# =============================================================================
success_criteria:
  - id: "SC-1"
    metric: "Code blocks before Skill() invocation per command"
    target: "<= 4 blocks (hard limit), <= 2 blocks (target)"
    measurement: "Run bash .claude/scripts/audit-command-skill-overlap.sh -- 0 violations (exit code 0)"

  - id: "SC-2"
    metric: "Command character count"
    target: "<= 12,000 characters (target), <= 15,000 characters (hard limit)"
    measurement: "Run /audit-budget -- all refactored commands under limit"

  - id: "SC-3"
    metric: "Business logic in commands"
    target: "0 instances of Bash(command=, Task(, or loop logic (FOR...in) in command files"
    measurement: "Grep for forbidden patterns: Bash(command=, Task(, FOR .* in .*: -- 0 matches per command"

  - id: "SC-4"
    metric: "Lean Orchestration Enforcement section presence"
    target: "100% of refactored commands contain ## Lean Orchestration Enforcement with DO NOT guardrails"
    measurement: "Grep for 'Lean Orchestration Enforcement' in each refactored command file -- 1 match per file"

  - id: "SC-5"
    metric: "Token reduction in main conversation"
    target: ">= 40% average token reduction per command invocation"
    measurement: "Before/after token usage comparison during smoke testing"

  - id: "SC-6"
    metric: "Line count reduction"
    target: ">= 50% average line reduction across all refactored commands"
    measurement: "wc -l before vs after for each command file"

  - id: "SC-7"
    metric: "Backward compatibility"
    target: "100% of command invocation syntaxes unchanged"
    measurement: "Smoke test each refactored command 3x with same arguments as before refactoring"

  - id: "SC-8"
    metric: "Skill line count compliance"
    target: "<= 500 lines per SKILL.md body for any new or extended skill"
    measurement: "wc -l for each affected SKILL.md after extension"

# =============================================================================
# CONSTRAINTS
# =============================================================================
constraints:
  - type: "technical"
    constraint: "Commands must use only tools listed in their allowed-tools frontmatter field"
    source: "devforgeai/protocols/lean-orchestration-pattern.md"

  - type: "technical"
    constraint: "Skills must follow Agent Skills Specification v1.0 YAML frontmatter schema (name 1-64 chars lowercase+hyphens, description 1-1024 chars with 'Use when' trigger)"
    source: ".claude/skills/claude-code-terminal-expert/references/skills/agent-skills-spec.md"

  - type: "technical"
    constraint: "SKILL.md body must stay under 500 lines. Overflow content goes to references/ directory for progressive disclosure."
    source: ".claude/skills/claude-code-terminal-expert/references/skills/best-practices.md, lines 233-235"

  - type: "technical"
    constraint: "Reference files must be one level deep from SKILL.md (no nested references that reference other references)"
    source: ".claude/skills/claude-code-terminal-expert/references/skills/best-practices.md, lines 345-371"

  - type: "technical"
    constraint: "All file paths must use forward slashes (Unix-style), never backslashes"
    source: ".claude/skills/claude-code-terminal-expert/references/skills/best-practices.md, lines 806-813"

  - type: "technical"
    constraint: "Command character budget hard limit is 15,000 characters per command file"
    source: "devforgeai/protocols/lean-orchestration-pattern.md, line 89"

  - type: "technical"
    constraint: "Extracted logic moving to skills must maintain identical user-facing behavior (same outputs, same prompts, same error messages)"
    source: "Backward compatibility requirement -- no breaking changes to user experience"

  - type: "business"
    constraint: "Batches 1-3 must be implemented sequentially due to skill creation dependencies. Batches 4-7 may be parallelized."
    source: "Dependency analysis in plan file (.claude/plans/piped-baking-crystal.md)"

  - type: "technical"
    constraint: "Gold standard template for refactored commands: YAML frontmatter, one-line description, Lean Orchestration Enforcement section (DO NOT + DO), Phase 0 arg validation, Phase 1 skill invocation, error handling table, references."
    source: ".claude/commands/create-story.md (73 lines, 1 block -- reference implementation)"

# =============================================================================
# NON-FUNCTIONAL REQUIREMENTS
# =============================================================================
nfrs:
  - category: "performance"
    requirement: "Each refactored command must reduce main conversation token consumption by >= 40% compared to pre-refactoring baseline"
    priority: "High"

  - category: "maintainability"
    requirement: "All refactored commands must pass /audit-hybrid with 0 violations (exit code 0)"
    priority: "Critical"

  - category: "maintainability"
    requirement: "Each refactored command must contain a Lean Orchestration Enforcement section with explicit DO NOT guardrails to prevent future workflow creep"
    priority: "High"

  - category: "usability"
    requirement: "No changes to command invocation syntax -- all existing /command [args] patterns remain identical"
    priority: "Critical"

  - category: "maintainability"
    requirement: "New or extended skills must follow progressive disclosure: SKILL.md overview (<500 lines) with references/ for detailed workflows"
    priority: "High"

  - category: "reliability"
    requirement: "Each refactored command must be smoke-tested 3x with valid input before acceptance"
    priority: "High"

# =============================================================================
# STAKEHOLDERS
# =============================================================================
stakeholders:
  - role: "Framework Owner"
    goals:
      - "Eliminate all hybrid violations detected by /audit-hybrid"
      - "Align all commands with Anthropic Agent Skills best practices"
      - "Reduce token waste across command invocations"
    decision_authority:
      - "Refactoring pattern selection per command"
      - "Batch sequencing and priority"
      - "False positive classification"

  - role: "DevForgeAI AI Agent"
    goals:
      - "Execute /dev and /qa workflows against generated stories"
      - "Maintain backward compatibility during refactoring"
      - "Extend skills without exceeding 500-line SKILL.md limit"
    decision_authority:
      - "Technical implementation details within approved patterns"
      - "Subagent delegation within skill phases"

# =============================================================================
# AUDIT EVIDENCE (context from /audit-hybrid results)
# =============================================================================
# This section preserves the exact audit data that triggered this effort.
# A new Claude session can verify current state by re-running the audit.

audit_evidence:
  audit_command: "bash .claude/scripts/audit-command-skill-overlap.sh"
  audit_date: "2026-02-20"
  total_commands_scanned: 41
  violations_detected: 20
  clean_commands: 7
  warnings_no_skill: 14
  violation_threshold: "> 4 code blocks before Skill() invocation"

  violations_by_severity:
    critical:
      - command: "validate-epic-coverage.md"
        blocks: 14
        fence_lines: 29
        current_lines: 463
        pattern: "A"
        target_lines: 120
        skill_target: "NEW: devforgeai-epic-validation"
      - command: "create-sprint.md"
        blocks: 11
        fence_lines: 23
        current_lines: 527
        pattern: "A+C"
        target_lines: 100
        skill_target: "EXTEND: devforgeai-orchestration"
      - command: "resume-dev.md"
        blocks: 11
        fence_lines: 23
        current_lines: 676
        pattern: "B"
        target_lines: 120
        skill_target: "EXTEND: implementing-stories"
      - command: "create-missing-stories.md"
        blocks: 10
        fence_lines: 21
        current_lines: 483
        pattern: "A"
        target_lines: 100
        skill_target: "EXTEND: devforgeai-epic-validation"
      - command: "recommendations-triage.md"
        blocks: 10
        fence_lines: 21
        current_lines: 382
        pattern: "A"
        target_lines: 80
        skill_target: "EXTEND: devforgeai-feedback"

    high:
      - command: "qa.md"
        blocks: 8
        fence_lines: 17
        current_lines: 344
        pattern: "C"
        target_lines: 100
        skill_target: "EXTEND: devforgeai-qa"
      - command: "create-ui.md"
        blocks: 8
        fence_lines: 17
        current_lines: 675
        pattern: "C"
        target_lines: 100
        skill_target: "EXTEND: devforgeai-ui-generator"
      - command: "ideate.md"
        blocks: 7
        fence_lines: 15
        current_lines: 374
        pattern: "C"
        target_lines: 90
        skill_target: "EXTEND: discovering-requirements"
      - command: "audit-w3.md"
        blocks: 6
        fence_lines: 12
        current_lines: 240
        pattern: "D"
        target_lines: 120
        skill_target: "NEW: devforgeai-w3-audit"
      - command: "dev.backup.md"
        blocks: 6
        fence_lines: 13
        current_lines: 258
        pattern: "DELETE"
        target_lines: 0
        skill_target: "N/A - duplicate of dev.md"
      - command: "create-epic.md"
        blocks: 6
        fence_lines: 13
        current_lines: 444
        pattern: "C+E"
        target_lines: 150
        skill_target: "EXTEND: designing-systems"
      - command: "create-stories-from-rca.md"
        blocks: 6
        fence_lines: 13
        current_lines: 264
        pattern: "E"
        target_lines: 180
        skill_target: "Move help to reference file"
      - command: "document.md"
        blocks: 6
        fence_lines: 13
        current_lines: 284
        pattern: "C+E"
        target_lines: 100
        skill_target: "Move templates to reference file"
      - command: "fix-story.md"
        blocks: 6
        fence_lines: 13
        current_lines: 205
        pattern: "FALSE_POSITIVE"
        target_lines: 205
        skill_target: "N/A - all blocks are arg validation"
      - command: "orchestrate.md"
        blocks: 6
        fence_lines: 13
        current_lines: 536
        pattern: "E"
        target_lines: 300
        skill_target: "Move 200 lines docs to reference file"
      - command: "rca.md"
        blocks: 5
        fence_lines: 11
        current_lines: 448
        pattern: "C+E"
        target_lines: 120
        skill_target: "Move 150 lines examples to reference file"
      - command: "insights.md"
        blocks: 5
        fence_lines: 11
        current_lines: 276
        pattern: "C+E"
        target_lines: 100
        skill_target: "Move inline help to reference file"
      - command: "create-agent.md"
        blocks: 5
        fence_lines: 11
        current_lines: 256
        pattern: "C+E"
        target_lines: 100
        skill_target: "Move mode detection to skill"

    medium:
      - command: "feedback-search.md"
        blocks: 4
        fence_lines: 9
        current_lines: 398
        pattern: "E"
        target_lines: 120
        skill_target: "Move 250 lines help to reference file"
      - command: "setup-github-actions.md"
        blocks: 4
        fence_lines: 9
        current_lines: 132
        pattern: "FALSE_POSITIVE"
        target_lines: 132
        skill_target: "N/A - all blocks are arg validation"

  false_positives:
    - command: "fix-story.md"
      reason: "All 6 code blocks are legitimate argument validation (regex, Glob, AskUserQuestion). Zero business logic."
    - command: "setup-github-actions.md"
      reason: "132 lines total, 4 blocks are force flag parse, existing file check, context markers, skill invocation. All legitimate."
    - command: "dev.backup.md"
      reason: "Duplicate of dev.md. Not a pattern violation -- file management issue. Action: DELETE."

  clean_commands_reference:
    - command: "create-story.md"
      blocks: 1
      lines: 73
      note: "GOLD STANDARD - reference implementation for all refactored commands"
    - command: "review-qa-reports.md"
      blocks: 1
      lines: 187
      note: "Clean delegation with extensive but appropriate documentation"
    - command: "research.md"
      blocks: 2
      lines: 112
      note: "Mode detection + skill invocation only"
    - command: "create-context.md"
      blocks: 2
      lines: 69
      note: "Pre-flight check + skill invocation"
    - command: "brainstorm.md"
      blocks: 3
      lines: 73
      note: "Mode detection + skill invocation"
    - command: "release.md"
      blocks: 3
      lines: 114
      note: "Validation + compliance check + skill invocation"

# =============================================================================
# REFACTORING PATTERNS (detailed specifications for story creation)
# =============================================================================
# Each pattern is fully specified so /create-story can generate unambiguous ACs.

refactoring_patterns:
  - id: "PATTERN-A"
    name: "Full Workflow Extraction"
    description: "Extract embedded validation + display + interaction logic from command into a new or extended skill. Optionally create result-interpreter subagent for display formatting."
    commands: ["validate-epic-coverage", "create-missing-stories", "create-sprint", "recommendations-triage"]
    extraction_steps:
      - "Identify all Glob/Read/Bash calls that perform data processing (gap detection, report generation, filtering)"
      - "Identify all display formatting logic (table rendering, coverage indicators, progress bars)"
      - "Identify all interactive workflows (AskUserQuestion sequences for multi-step selection)"
      - "Create skill phase(s) to contain extracted logic"
      - "If display logic exceeds 50 lines, create result-interpreter subagent"
      - "Replace extracted logic in command with context markers + Skill() invocation"
      - "Add Lean Orchestration Enforcement section with DO NOT guardrails"
    anthropic_citations:
      - "chain-complex-prompts.md: 'Breaking down complex tasks into smaller, manageable subtasks... each subtask gets Claude's full attention'"
      - "best-practices.md: 'Use workflows for complex tasks -- break complex operations into clear, sequential steps'"

  - id: "PATTERN-B"
    name: "Pre-Flight Logic Extraction"
    description: "Move inline pre-flight validation and DoD parsing from command into target skill's Phase 0 and resumption logic."
    commands: ["resume-dev", "dev.backup"]
    extraction_steps:
      - "Identify pre-flight Task() calls (tech-stack-detector, context-preservation-validator)"
      - "Identify DoD/checkpoint parsing logic"
      - "Move pre-flight checks to skill's existing Phase 0 (or create Phase 0.5: Resume Detection)"
      - "Move DoD analysis to skill's phase state loader"
      - "Command retains only: arg parsing, story file loading, Skill() invocation"
    anthropic_citations:
      - "agent-skills-spec.md: Three-Tier Loading Model -- load detailed materials only at Execution tier, not Discovery tier"

  - id: "PATTERN-C"
    name: "Multi-Phase Slimming"
    description: "Move mode detection and context probing from command into skill Phase 0. Move result interpretation into skill post-execution phases."
    commands: ["ideate", "create-epic", "create-ui", "document", "create-agent", "rca", "insights", "qa"]
    extraction_steps:
      - "Identify mode detection logic (Glob checks, config reads, brainstorm auto-detection)"
      - "Identify context probing (reading context files to determine workflow path)"
      - "Identify result interpretation (Task() calls to interpreter subagents)"
      - "Move mode detection to skill Phase 0 (skill can Glob/Read context files itself)"
      - "Move result interpretation to skill final phase"
      - "Add DO NOT guardrail section following create-story.md gold standard"
    anthropic_citations:
      - "best-practices.md: 'Concise is key -- the context window is a public good'"

  - id: "PATTERN-D"
    name: "Standalone Audit to Skill"
    description: "Create a lightweight skill to contain scan + report logic from audit commands."
    commands: ["audit-w3"]
    extraction_steps:
      - "Create new skill directory: .claude/skills/devforgeai-w3-audit/"
      - "Create SKILL.md with scan logic (Phase 1: Scan, Phase 2: Report)"
      - "Move Grep-based scanning patterns to skill Phase 1"
      - "Move report formatting to skill Phase 2"
      - "Command retains: arg parsing + Skill() invocation"
    anthropic_citations:
      - "best-practices.md: 'Keep SKILL.md under 500 lines -- split content into separate files'"

  - id: "PATTERN-E"
    name: "Documentation Trimming"
    description: "Move help text, examples, and verbose error handling to references/ files loaded on --help."
    commands: ["feedback-search", "orchestrate", "create-stories-from-rca", "rca", "insights", "create-epic", "document", "create-agent"]
    extraction_steps:
      - "Identify help text sections (typically 50-250 lines of usage examples and troubleshooting)"
      - "Create references/{command}-help.md file with extracted documentation"
      - "Replace inline help with: 'For detailed help, load references/{command}-help.md'"
      - "Condense error handling table to 3-5 core scenarios"
      - "Remove verbose examples, keep only Quick Reference section in command"
    anthropic_citations:
      - "best-practices.md: 'Progressive disclosure... SKILL.md serves as overview that points to detailed materials'"

# =============================================================================
# BATCH PLAN (for epic feature decomposition)
# =============================================================================
# Each batch maps to one epic feature. Features listed in implementation order.

batch_plan:
  - batch: 1
    name: "Epic Coverage Pipeline Refactoring"
    commands: ["validate-epic-coverage.md", "create-missing-stories.md"]
    pattern: "A"
    points: 16
    new_artifacts:
      - "NEW skill: devforgeai-epic-validation (or extend devforgeai-orchestration)"
      - "NEW subagent: epic-coverage-result-interpreter"
    dependency: "None (first batch)"

  - batch: 2
    name: "Sprint & Triage Workflow Refactoring"
    commands: ["create-sprint.md", "recommendations-triage.md"]
    pattern: "A+C"
    points: 16
    new_artifacts:
      - "EXTEND skill: devforgeai-orchestration Phase 3"
      - "EXTEND skill: devforgeai-feedback with triage mode"
    dependency: "After Batch 1 (sequential)"

  - batch: 3
    name: "Resume Dev Pre-Flight Extraction"
    commands: ["resume-dev.md"]
    pattern: "B"
    points: 8
    new_artifacts:
      - "EXTEND skill: implementing-stories with resume detection"
    dependency: "After Batch 2 (sequential -- touches critical skill)"

  - batch: 4
    name: "Skill-Invoking Command Slimming"
    commands: ["qa.md", "create-ui.md", "ideate.md"]
    pattern: "C"
    points: 15
    new_artifacts:
      - "EXTEND skills: devforgeai-qa, devforgeai-ui-generator, discovering-requirements"
    dependency: "After Batch 3 (parallel-safe with Batches 5-7)"

  - batch: 5
    name: "Documentation-Heavy Command Trimming"
    commands: ["create-epic.md", "document.md", "create-agent.md", "rca.md", "insights.md"]
    pattern: "C+E"
    points: 9
    new_artifacts:
      - "Reference help files for trimmed documentation"
    dependency: "After Batch 3 (parallel-safe with Batches 4, 6-7)"

  - batch: 6
    name: "Special Cases & Cleanup"
    commands: ["audit-w3.md", "dev.backup.md", "orchestrate.md", "create-stories-from-rca.md"]
    pattern: "D+E+DELETE"
    points: 10
    new_artifacts:
      - "NEW skill: devforgeai-w3-audit (optional)"
      - "DELETE: dev.backup.md"
      - "Reference help files"
    dependency: "After Batch 3 (parallel-safe with Batches 4-5, 7)"

  - batch: 7
    name: "Borderline Command Trimming"
    commands: ["feedback-search.md"]
    pattern: "E"
    points: 3
    new_artifacts:
      - "Reference help file for feedback-search"
    dependency: "After Batch 3 (parallel-safe with Batches 4-6)"

# =============================================================================
# PROVENANCE
# =============================================================================
source_brainstorm: "N/A"
source_plan: ".claude/plans/piped-baking-crystal.md"
source_audit: "bash .claude/scripts/audit-command-skill-overlap.sh (2026-02-20)"
source_anthropic_docs:
  - ".claude/skills/claude-code-terminal-expert/references/skills/best-practices.md"
  - ".claude/skills/claude-code-terminal-expert/references/skills/agent-skills-spec.md"
  - ".claude/skills/claude-code-terminal-expert/references/prompt-engineering/chain-complex-prompts.md"
  - ".claude/skills/claude-code-terminal-expert/references/prompt-engineering/be-clear-and-direct.md"
source_framework_docs:
  - "devforgeai/protocols/lean-orchestration-pattern.md"
  - ".claude/commands/create-story.md (gold standard reference)"
  - ".claude/commands/dev.md (successfully refactored reference)"

---

# Requirements: Hybrid Command Lean Orchestration Refactoring

## Overview

This document captures the structured requirements for refactoring 20 DevForgeAI command files to comply with the lean orchestration pattern. All data is stored in the YAML frontmatter above for cross-session AI consumption.

The effort was triggered by `/audit-hybrid` results showing 20 commands with >4 code blocks before `Skill()` invocation. Analysis against Anthropic's Agent Skills best practices and the DevForgeAI lean orchestration protocol produced 5 refactoring patterns, 7 implementation batches, and 14 planned stories totaling 77 points.

## Reading This Document

- **Decisions (DR-1 through DR-9):** Locked architectural choices with rejected alternatives and Anthropic citations
- **Scope:** 18 commands to refactor + 1 to delete + 1 subagent to create. 3 false positives excluded.
- **Success Criteria (SC-1 through SC-8):** Quantified targets with measurement methods
- **Constraints:** Technical and business boundaries
- **NFRs:** Performance (token reduction), maintainability (audit compliance), usability (backward compatibility)
- **Audit Evidence:** Complete /audit-hybrid results with per-command violation data
- **Refactoring Patterns (PATTERN-A through PATTERN-E):** Detailed extraction steps and Anthropic citations per pattern
- **Batch Plan:** 7 batches with commands, patterns, points, artifacts, and dependencies

## Key References

| Document | Purpose |
|----------|---------|
| `.claude/plans/piped-baking-crystal.md` | Original refactoring roadmap plan |
| `devforgeai/protocols/lean-orchestration-pattern.md` | Lean orchestration constitutional protocol |
| `.claude/commands/create-story.md` | Gold standard command (73 lines, 1 block) |
| `.claude/commands/dev.md` | Successfully refactored command reference |
| `.claude/scripts/audit-command-skill-overlap.sh` | Audit script for verification |

## Next Steps

1. Review locked decisions in frontmatter
2. Validate scope boundaries and false positive classifications
3. Proceed to `/create-epic` with this requirements document

---

*Generated manually from /audit-hybrid analysis and Anthropic documentation review | Schema v1.0*
