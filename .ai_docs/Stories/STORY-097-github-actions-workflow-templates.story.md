---
id: STORY-097
title: GitHub Actions Workflow Templates with Headless Claude Code
epic: EPIC-010
sprint: Sprint-6
status: Backlog
points: 13
priority: Medium
assigned_to: TBD
created: 2025-11-25
format_version: "2.1"
depends_on: ["STORY-091", "STORY-092", "STORY-093", "STORY-094", "STORY-095", "STORY-096"]
deferred_to_phase: 2
---

# Story: GitHub Actions Workflow Templates with Headless Claude Code

## Description

**As a** DevForgeAI framework user,
**I want** GitHub Actions workflows that execute /dev and /qa in headless mode,
**so that** I can automate parallel story development on pull requests and enable CI/CD integration.

**Context:** This is Feature 7 of EPIC-010 (Parallel Story Development). **DEFERRED TO PHASE 2** - Proceed only after Phase 1 MVP (Features 1-6) complete and validated.

## Acceptance Criteria

### AC#1: Automated /dev Execution Workflow

**Given** GitHub Actions workflow `dev-story.yml` exists
**When** triggered via workflow_dispatch with story_id input
**Then** runs `claude -p "/dev ${{inputs.story_id}}"` in headless mode
**And** uploads test results, coverage, story file as artifacts

---

### AC#2: PR Quality Gate Workflow

**Given** GitHub Actions workflow `qa-validation.yml` exists
**When** pull request opened to main
**Then** extracts story ID from PR title
**And** runs `/qa deep` for that story
**And** blocks merge if QA fails

---

### AC#3: Matrix Parallel Execution

**Given** GitHub Actions workflow `parallel-stories.yml` exists
**When** triggered with array of story_ids
**Then** uses matrix strategy to run /dev for each story simultaneously
**And** supports up to 5 concurrent jobs (configurable)

---

### AC#4: Cost Optimization

**Given** CI/CD workflows are executing
**When** Claude Code is invoked
**Then** uses prompt caching (90% API cost savings)
**And** prefers Haiku model for routine operations
**And** tracks cost per story (< $0.15/story target)

---

### AC#5: Configuration Setup Command

**Given** user runs `/setup-github-actions`
**When** command completes
**Then** creates:
- `.github/workflows/dev-story.yml`
- `.github/workflows/qa-validation.yml`
- `.github/workflows/parallel-stories.yml`
- `.github/workflows/installer-testing.yml`
- `.devforgeai/config/github-actions.yaml`
- `.devforgeai/config/ci-answers.yaml`

---

## Technical Specification

```yaml
technical_specification:
  format_version: "2.0"

  components:
    - type: "Service"
      name: "devforgeai-github"
      file_path: "src/claude/skills/devforgeai-github/SKILL.md"
      interface: "Skill"
      lifecycle: "On-demand"
      requirements:
        - id: "SKL-001"
          description: "Generate GitHub Actions workflow files"
          testable: true
          test_requirement: "Test: /setup-github-actions creates 4 workflows"
          priority: "Critical"
        - id: "SKL-002"
          description: "Configure headless mode with ci-answers.yaml"
          testable: true
          test_requirement: "Test: AskUserQuestion prompts answered from config"
          priority: "Critical"
        - id: "SKL-003"
          description: "Implement cost tracking and optimization"
          testable: true
          test_requirement: "Test: Cost per story logged to artifacts"
          priority: "High"

    - type: "Configuration"
      name: "github-actions.yaml"
      file_path: "src/devforgeai/config/github-actions.yaml.example"
      required_keys:
        - key: "max_parallel_jobs"
          type: "integer"
          default: "5"
        - key: "cost_optimization.enable_prompt_caching"
          type: "boolean"
          default: "true"
        - key: "cost_optimization.prefer_haiku"
          type: "boolean"
          default: "true"
        - key: "cost_optimization.max_cost_per_story"
          type: "number"
          default: "0.15"

    - type: "Configuration"
      name: "ci-answers.yaml"
      file_path: "src/devforgeai/config/ci-answers.yaml.example"
      purpose: "Pre-defined answers for headless AskUserQuestion prompts"
      required_keys:
        - key: "test_failure_action"
          type: "string"
          default: "fix-implementation"
        - key: "deferral_strategy"
          type: "string"
          default: "never"
        - key: "priority_default"
          type: "string"
          default: "high"

  business_rules:
    - id: "BR-001"
      rule: "Headless mode requires pre-configured answers"
      trigger: "CI/CD execution"
      validation: "ci-answers.yaml must exist and cover all prompts"
      test_requirement: "Test: Missing answer triggers fail-fast"
      priority: "Critical"

  non_functional_requirements:
    - id: "NFR-001"
      category: "Performance"
      requirement: "Workflow execution time"
      metric: "< 30 minutes per story including setup"
      test_requirement: "Test: Full /dev completes in <30 min"
      priority: "High"
    - id: "NFR-002"
      category: "Cost"
      requirement: "API cost per story"
      metric: "< $0.15 per story with caching"
      test_requirement: "Test: Track actual costs, verify <$0.15"
      priority: "High"
```

---

## Non-Functional Requirements

### Performance
- Workflow execution: < 30 minutes per story
- Parallel matrix: up to 5 concurrent jobs
- Startup overhead: < 2 minutes

### Cost
- API cost: < $0.15 per story (with caching)
- Runner cost: $0.04/story (GitHub hosted)
- Free tier: 2,000 min/month sufficient for solo dev

### Reliability
- Retry failed jobs: max 2 retries
- Artifact retention: 7 days
- Fail-fast on missing config

---

## Edge Cases

1. **ANTHROPIC_API_KEY missing:** Fail with setup instructions
2. **Concurrent story limit exceeded:** Queue additional jobs
3. **Network timeout:** Retry with backoff
4. **Prompt not in ci-answers.yaml:** Fail-fast with prompt text

---

## Dependencies

### Prerequisite Stories
- [ ] All Phase 1 MVP stories (STORY-091 through STORY-096)

### External Dependencies
- GitHub Actions runner
- ANTHROPIC_API_KEY secret
- Claude Code GitHub Action (`anthropics/claude-code-action`)

---

## Definition of Done

### Implementation
- [ ] devforgeai-github skill created (11th skill)
- [ ] /setup-github-actions command created
- [ ] 4 workflow templates generated
- [ ] github-actions.yaml configuration
- [ ] ci-answers.yaml configuration
- [ ] Cost tracking implementation

### Quality
- [ ] All 5 acceptance criteria pass
- [ ] Cost target validated (< $0.15/story)
- [ ] Workflow tested on real PR

### Testing
- [ ] Unit tests for workflow generation
- [ ] Integration tests with GitHub Actions
- [ ] Cost validation tests

### Documentation
- [ ] .github/README.md created
- [ ] GITHUB-ACTIONS-GUIDE.md
- [ ] COST-OPTIMIZATION.md
- [ ] TROUBLESHOOTING-CICD.md

---

## Workflow Status

- [ ] Architecture phase complete
- [ ] Development phase complete
- [ ] QA phase complete
- [ ] Released

---

## Notes

**Deferral Justification:** Per EPIC-010 discovery, CI/CD is "medium priority - nice to have later." Focus Phase 1 on local parallel development (higher immediate value).

**Go/No-Go Checkpoint:** After Week 6 (Phase 1 MVP complete), decision on Phase 2 based on:
- 2 concurrent stories work without collisions
- Quality gates 100% preserved
- Dependency enforcement validated

---

**Story Template Version:** 2.1
**Created:** 2025-11-25

## Implementation Notes

No implementation yet - story in planning/backlog phase.
