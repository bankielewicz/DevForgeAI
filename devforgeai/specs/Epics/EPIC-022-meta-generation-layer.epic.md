---
id: EPIC-002
title: Meta-Generation Layer
business-value: Enable automated creation of agents, skills, and prompts with self-improvement patterns, reducing manual agent creation time by 80%
status: Backlog
priority: P1
complexity-score: 44
architecture-tier: Tier 3
created: 2025-12-16
estimated-points: 35
target-sprints: 5
dependencies: [EPIC-021]
research_references: []
---

# Meta-Generation Layer

## Business Goal

Build meta-generation capabilities that create agents, skills, and prompts with built-in expertise accumulation and self-improvement patterns, enabling engineers to rapidly create domain-specific experts without manual template coding.

**Success Metrics:**
- **Agent creation speed:** 80% reduction in time to create domain expert (from 2 hours manual coding to 15 minutes with /create-meta-expert)
- **Expert quality:** 90% of auto-generated experts pass validation on first attempt
- **Adoption:** 70% of DevForgeAI projects use at least one meta-generated expert within first month

## Features

### Feature 1: Meta-Prompt Generator
**Description:** Generate prompt templates that create other prompts with self-improvement patterns, enabling prompt-that-writes-prompts workflows.

**User Stories (high-level):**
1. As a meta-system, I want to define meta-prompt template structure, so that generated prompts include self-improvement hooks
2. As an engineer, I want to create meta-prompt via /create-meta-prompt [purpose], so that I get prompt generator for specific domain
3. As a meta-prompt, I want to generate child prompts with expertise integration, so that child prompts read/update expertise files
4. As a meta-prompt, I want to include validation logic in generated prompts, so that child prompts verify mental models

**Estimated Effort:** Medium (6 story points)

### Feature 2: Meta-Skill Generator
**Description:** Create skills that generate other skills with expertise accumulation, enabling skill-that-writes-skills workflows (e.g., meta-expert skill → database-expert skill, api-expert skill).

**User Stories (high-level):**
1. As a meta-system, I want to define meta-skill template structure, so that generated skills follow DevForgeAI skill conventions
2. As an engineer, I want to create meta-skill via /create-meta-skill [domain], so that I get skill generator for specific capability
3. As a meta-skill, I want to generate child skills with SKILL.md structure, so that child skills are properly formatted
4. As a meta-skill, I want to embed expertise file references in generated skills, so that child skills read domain knowledge
5. As a meta-skill, I want to include self-improvement phases in generated skills, so that child skills update expertise after execution

**Estimated Effort:** Large (10 story points)

### Feature 3: Meta-Agent Generator
**Description:** Generate agents that create other agents with domain-specific mental models, enhancing existing devforgeai-subagent-creation skill.

**User Stories (high-level):**
1. As a meta-system, I want to enhance agent-generator.md with meta-generation logic, so that agents include expertise patterns
2. As an engineer, I want to create meta-agent via /create-meta-agent [domain], so that I get agent generator for specific specialty
3. As a meta-agent, I want to generate child agents with system prompts referencing expertise files, so that agents use mental models
4. As a meta-agent, I want to include validation instructions in generated agents, so that agents verify mental models before using
5. As a meta-agent, I want to configure agent tools (Read, Grep, Glob, Bash), so that generated agents have appropriate tool access

**Estimated Effort:** Large (9 story points)

### Feature 4: Subagent Context Injection
**Description:** Before launching subagent via Task tool, create YAML mental model from current conversation context and pass to subagent for increased accuracy.

**User Stories (high-level):**
1. As an orchestrator agent, I want to analyze current context before launching subagent, so that I can create relevant mental model
2. As an orchestrator agent, I want to extract key facts (file paths, entities, patterns) from context, so that subagent has working memory
3. As an orchestrator agent, I want to write context mental model to temp YAML file, so that subagent can read it
4. As a subagent, I want to read pre-launch mental model, so that I validate assumptions instead of searching from scratch
5. As a subagent, I want to update mental model with learnings, so that orchestrator can incorporate feedback

**Estimated Effort:** Medium (6 story points)

### Feature 5: /create-meta-expert Command
**Description:** User-facing slash command to interactively create domain experts (agent + expertise file + self-improvement workflow) via guided questions.

**User Stories (high-level):**
1. As an engineer, I want to run /create-meta-expert [domain], so that system guides me through expert creation
2. As a command, I want to ask domain-specific questions (what patterns to detect, validation rules), so that expertise file is tailored
3. As a command, I want to generate agent with system prompt including expertise file path, so that agent uses mental model
4. As a command, I want to create initial expertise file with placeholder knowledge, so that agent has structure to fill
5. As a command, I want to register domain mappings (file patterns → expert), so that expert is invoked automatically
6. As a command, I want to configure self-improvement hook, so that expert learns after threshold reached

**Estimated Effort:** Medium (7 story points)

### Feature 6: Meta-Template Library
**Description:** Reusable template library for meta-generation (prompt templates, skill templates, agent templates) with domain-specific variants.

**User Stories (high-level):**
1. As a meta-system, I want to store meta-templates in devforgeai/meta/templates/, so that generators have consistent starting points
2. As an engineer, I want to browse available meta-templates, so that I can see what domains have templates
3. As a meta-generator, I want to load domain-specific template (e.g., database-expert-template.md), so that generated experts follow best practices
4. As an engineer, I want to customize templates, so that project-specific patterns are reusable
5. As a meta-system, I want to validate templates against DevForgeAI conventions, so that invalid templates are rejected

**Estimated Effort:** Small (3 story points)

## Requirements Summary

### Functional Requirements
- Meta-prompt generation (prompt-that-writes-prompts)
- Meta-skill generation (skill-that-writes-skills)
- Meta-agent generation (agent-that-writes-agents)
- Subagent context injection (pre-launch mental model)
- /create-meta-expert command (interactive domain expert creation)
- Meta-template library (reusable generation templates)

### Data Model

**Entities:**
- **Meta-Template** (`devforgeai/meta/templates/{type}-{domain}-template.md`)
  - type: string ("meta-prompt", "meta-skill", "meta-agent")
  - domain: string ("database", "api", "websocket", "generic")
  - template_content: markdown (template structure with placeholders)
  - placeholders: list (variables to replace during generation)
  - validation_rules: list (checks to run on generated output)

- **Generated Expert** (output of meta-generation)
  - agent_file: path (e.g., `.claude/agents/database-expert.md`)
  - skill_file: path (e.g., `.claude/skills/database-expert/SKILL.md`)
  - expertise_file: path (e.g., `devforgeai/meta/expertise/database-expert.yaml`)
  - domain_mapping: entry in `devforgeai/meta/domain-mappings.yaml`

- **Context Mental Model** (temporary for subagent injection)
  - temp_file: path (e.g., `/tmp/subagent-context-{uuid}.yaml`)
  - extracted_facts: dict (file_paths, entities, patterns, assumptions)
  - confidence_scores: dict (fact → confidence 0.0-1.0)
  - expiration: timestamp (delete temp file after subagent completes)

**Relationships:**
- Meta-Template → Generated Expert: one-to-many (one template generates multiple experts)
- Generated Expert → Expertise File: one-to-one (each expert has one expertise file from EPIC-001)
- Context Mental Model → Subagent: one-to-one (created per subagent invocation)

### Integration Points
1. **EPIC-001 Expertise System** - Read/write expertise files using schema from EPIC-001
2. **devforgeai-subagent-creation skill** - Enhance with meta-generation logic
3. **Task tool** - Intercept subagent launches for context injection
4. **File system** - Read templates, write generated agents/skills/prompts
5. **AskUserQuestion** - Interactive domain expert creation via /create-meta-expert

### Non-Functional Requirements

**Performance:**
- Meta-generation: <60s to generate agent + skill + expertise file
- Context injection: <5s to extract context and create mental model YAML
- Template loading: <1s to read and parse template

**Quality:**
- Generated expert validation: 90% pass validation on first attempt
- Context extraction accuracy: >80% of extracted facts are relevant and correct
- Template coverage: 100% of generated outputs follow DevForgeAI conventions

**Usability:**
- /create-meta-expert command: <10 questions to create domain expert
- Template library: <5 minutes to browse and select template
- Error messages: Clear guidance when generation fails (missing placeholders, invalid syntax)

## Architecture Considerations

**Complexity Tier:** Tier 3 (Complex Platform, 44/60)

**Recommended Architecture:**
- Pattern: Clean Architecture with Template Method pattern
- Layers:
  - **Domain Layer:** Meta-generation logic, template parsing, placeholder replacement
  - **Application Layer:** Command orchestration, validation, file generation
  - **Infrastructure Layer:** Template storage, file I/O, subagent invocation
  - **Presentation Layer:** /create-meta-expert, /create-meta-skill, /create-meta-agent commands
- Database: File-based templates, generated outputs written to file system
- Deployment: Integrated into DevForgeAI framework

**Technology Recommendations:**
- Template Engine: Markdown with {{placeholder}} syntax (simple find-replace)
- Validation: JSON Schema for YAML outputs, Markdown linting for .md outputs
- Context Extraction: Claude's native context analysis (no external NLP)
- File Generation: Write tool for creating agents/skills/prompts

## Risks & Mitigations

| Risk | Severity | Mitigation |
|------|----------|------------|
| Generated experts don't follow DevForgeAI conventions | HIGH | Comprehensive validation in Feature 6, template quality gates |
| Context injection extracts irrelevant facts | MEDIUM | Confidence scoring, filter facts with confidence <0.7 |
| Meta-templates become outdated as framework evolves | MEDIUM | Version meta-templates, validate against current framework version |
| /create-meta-expert asks too many questions (UX) | LOW | Adaptive questioning (skip defaults), provide sensible defaults |
| Generated files overwrite existing files | HIGH | Pre-check if files exist, ask user for confirmation before overwriting |

## Dependencies

**Prerequisites:**
- **EPIC-001 (Expertise System Foundation)** - Required for expertise file schema and file operations

**Dependents:**
- **EPIC-003 (Self-Improvement Automation)** - Uses meta-generated experts for learning workflows

## Next Steps

1. **Story Creation:** Break features into stories via `/create-story [feature-description]`
   - Story 1: Define meta-prompt template structure
   - Story 2: Implement meta-prompt generation logic
   - Story 3: Create meta-skill generator with SKILL.md format
   - Story 4: Build /create-meta-expert interactive command
   - Story 5: Implement subagent context injection

2. **Sprint Planning:** Add Feature 1-3 to Sprint 2, Feature 4-6 to Sprint 3

3. **Testing Strategy:**
   - Generate sample experts for database, API, websocket domains
   - Validate generated outputs against DevForgeAI conventions
   - Test context injection with actual subagent invocations
   - Verify /create-meta-expert command with user acceptance testing
