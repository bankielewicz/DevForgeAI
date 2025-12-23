# Conflict Resolution Strategies for DevForgeAI Feature Improvements

**Date**: 2025-12-22
**Purpose**: Provide specific resolution approaches for 8 identified stakeholder conflicts
**Target Audience**: Decision-makers, stakeholder group leads, conflict mediators

---

## Conflict #1: Innovation vs. Stability

### The Tension
- **Product Manager** pushes for rapid feature delivery (12 stories/sprint goal)
- **Release Lead** requires stability and thorough testing (multi-week release cycles)
- **End Users** want new features but fear breaking changes
- **Framework Maintainers** concerned about technical debt from rushed implementation

### Root Causes
1. Single release train for all types of changes (features, bug fixes, patches)
2. No distinction between breaking and non-breaking changes
3. Testing requirements same for feature vs. patch releases
4. Release timeline dictated by longest feature story, not independent cadence

### Recommended Solution: Dual Release Cycle

**Strategy**: Separate "Feature Releases" (v1.X) from "Patch Releases" (v1.Y.Z)

```
Feature Release (v1.1)          Patch Release (v1.0.1)
- New skills/subagents         - Bug fixes
- New commands                 - Minor improvements
- Breaking changes allowed     - NO breaking changes
- Extended testing (3-4 weeks) - Quick testing (1 week)
- Quarterly (every 3 months)   - As-needed (every 1-2 weeks)

User Choice:
- Conservative teams: Use patch releases only, major version upgrades quarterly
- Aggressive teams: Use feature releases for latest capabilities
```

**Implementation Steps**:

1. **Define Release Types** (Document in tech-stack.md)
   - **Major (X.0.0)**: Breaking changes, context file format changes → User migration required
   - **Minor (X.Y.0)**: New features, new skills, non-breaking changes → Fully backward compatible
   - **Patch (X.Y.Z)**: Bug fixes, documentation → Zero breaking changes

2. **Create Feature Branch Strategy**
   ```
   main (latest stable v1.Y.Z)
     ↑ cherry-pick bug fixes
   main-stable (LTS version for conservative users)
     ↑ patch releases only
   develop (next feature release v1.X)
     ↑ feature branches for new skills
   ```

3. **Release Checklist by Type**
   ```
   PATCH RELEASE (1 week)         FEATURE RELEASE (3-4 weeks)
   ✓ Bug verification             ✓ Feature stories complete
   ✓ Regression test run          ✓ Integration testing
   ✓ Documentation update         ✓ Breaking change documentation
   ✓ Upgrade path tested          ✓ Migration guide created
   ✓ Changelog generated          ✓ Backward compatibility verified
                                   ✓ Extended QA cycle
   ```

4. **Communication Plan**
   - **Patch Release** (1 day announcement): "v1.0.1 available, security fix + 3 bug fixes"
   - **Feature Release** (2 week notice): "v1.1 coming Dec 15: New AI-assisted documentation skill"
   - **Major Release** (1 month notice): "v2.0 planned Q2 2026: Complete installer redesign"

**Stakeholder Impact**:
- PM: Can ship features in feature releases, doesn't block patch cycle
- Release Lead: Simpler patch process, thorough testing for features
- End Users: Choose stability (patch) or innovation (feature)
- Maintainers: Technical debt addressed in feature releases, not rushed

**Success Metrics**:
- Feature releases on quarterly schedule (100% on-time delivery)
- Patch releases delivered within 1 week of bug report
- Zero regressions in patch releases
- User upgrade adoption: 70% on latest patch, 40% on latest feature

---

## Conflict #2: Framework Constraints vs. User Flexibility

### The Tension
- **Maintainers** require mandatory TDD, 95% coverage, immutable context files
- **End Users** sometimes need to ship under deadline (skip tests, defer Definition of Done)
- **HALT patterns** block progression on violations (frustrating when urgent)
- **Historical incidents**: RCA-006 through RCA-013 document bypass attempts

### Root Causes
1. One-size-fits-all constraints (no flexibility options)
2. HALT messages don't explain rationale or recovery path
3. No legitimate exemption process (users forced to work around)
4. Constraints feel arbitrary without business context

### Recommended Solution: Tiered Execution Modes

**Strategy**: Three DevForgeAI modes with different constraint levels

```
STANDARD MODE (Default)        EXPRESS MODE (Deadline)      STARTUP MODE (MVP)
- Mandatory TDD                - Unit tests only (no E2E)   - Acceptance tests only
- 95% coverage (business logic) - 80% coverage (business)   - 60% coverage (core flows)
- Full HALT enforcement        - Warnings only (proceed)    - No blocking (advisory)
- Immutable context files      - Can defer non-core items   - Can defer docs
- All quality gates             - Skip less-critical gates   - Core gates only
- Time: 1-2 weeks/story        - Time: 3-5 days/story       - Time: 1-2 days/MVP
- Output: Production-ready     - Output: Testable            - Output: Functional
```

**Implementation**:

1. **Add Mode Selection to /create-story**
   ```yaml
   story: STORY-042
   title: Add Payment Processing Integration

   # User selects mode
   executionMode: "standard" | "express" | "startup"
   # If express/startup, requires justification:
   modeJustification: "Bank holiday deadline; will refactor after holiday"
   ```

2. **Update /dev Command**
   ```bash
   /dev --mode=express --story=STORY-042

   Output:
   "Express mode selected. Executing with reduced coverage (80%).
    Note: Code will need Express→Standard migration before production release.
    Estimated refactoring cost: 2-3 days for full TDD + E2E coverage."
   ```

3. **Automated Debt Tracking**
   ```
   When using express/startup mode, auto-create "Tech Debt Story":
   - STORY-043: "Refactor STORY-042 to Standard mode (TDD, 95% coverage)"
   - Story includes breakdown of remaining test coverage, E2E test scripts needed
   - Estimated effort: 2-3 days
   - MUST be completed before major release
   ```

4. **Mode Constraints Document**
   ```markdown
   ## Standard Mode Constraints
   - TDD mandatory (Red → Green → Refactor)
   - 95% coverage business logic, 85% application, 80% infrastructure
   - All context files immutable (must use ADR for changes)
   - All quality gates HALT on violation

   ## Express Mode Constraints
   - Unit tests required (no E2E regression testing)
   - 80% coverage minimum (business logic layer only)
   - Can defer non-critical Definition of Done items
   - Quality gate warnings (advisory, can override with justification)
   - Auto-creates tech debt story for refactoring
   - CANNOT be shipped without Standard refactoring

   ## Startup Mode Constraints
   - Acceptance tests required (happy path only)
   - 60% coverage minimum (core user flows)
   - Can skip documentation, performance optimization
   - Quality gates informational (no blocking)
   - For MVP/prototype only, must refactor to Standard before production
   - Timeline: max 2 days, then refactor to Standard
   ```

5. **Governance Process**
   ```
   If using Express or Startup:
   1. Story includes mode selection + justification
   2. Product Manager approves (confirms deadline pressure legitimate)
   3. Maintainer reviews tech debt story scope (will it be completable?)
   4. QA agrees on reduced coverage targets
   5. Tech debt story scheduled in next 2-3 sprints (not deferred)

   If tech debt story slips:
   - Code cannot ship in patch release
   - Becomes blocking item for next major release
   - RCA required (why did refactoring slip?)
   ```

**Stakeholder Impact**:
- Maintainers: Architectural integrity maintained; tech debt explicitly tracked
- Users: Can ship under pressure with explicit debt acknowledgment
- PM: Can prioritize urgent vs. standard work
- QA: Clear coverage expectations per mode
- Support: Tech debt stories become visible, prevent surprise failures

**Success Metrics**:
- Tech debt stories completed within 2-3 sprints (not deferred beyond)
- Express mode stories: <10% of sprint capacity
- Startup mode stories: <5% of sprint capacity
- No production issues from Express/Startup code refactoring
- User satisfaction: Clear understanding of mode trade-offs

---

## Conflict #3: Generalist Framework vs. Specialized Stack Support

### The Tension
- **Framework philosophy**: Technology-agnostic (any backend, frontend, database)
- **User requests**: Python/FastAPI team wants async/await patterns; Rust team wants ownership-aware code
- **Maintainers worried**: Adding stack-specific skills breaks meta-framework design
- **Market risk**: Users may fork if specialized needs not met

### Root Causes
1. Core framework truly agnostic, but ecosystem dominated by Node.js/React/TypeScript focus
2. No formalized way to create stack-specific extensions
3. Users don't know if requesting feature is "in scope" for framework
4. Community confusion about what devforgeai-development skill can support

### Recommended Solution: Plugin Architecture with Community Extensions

**Strategy**: Keep core framework agnostic; enable "stack profile" plugins

```
Core Framework (Agnostic)
├── 15 Universal Skills
├── 26 Universal Subagents
└── 24 Universal Commands

↓ Extended by ↓

Stack Profile Plugins (Community)
├── python-fastapi-profile/
│   ├── async-test-subagent
│   ├── dependency-injection-skill
│   └── async-pattern-examples.md
├── rust-tokio-profile/
│   ├── ownership-analyzer-subagent
│   ├── lifetimes-test-generator
│   └── concurrency-examples.md
└── dotnet-csharp-profile/
    ├── async-await-subagent
    ├── dependency-injection-skill
    └── entity-framework-patterns.md
```

**Implementation**:

1. **Define "Stack Profile" Format**
   ```yaml
   # .claude/profiles/python-fastapi.profile.md
   name: "Python + FastAPI + pytest"
   description: "Specialized support for async Python development"
   target_languages: ["python"]
   frameworks: ["fastapi", "starlette"]
   minimum_version: "1.1.0"

   extends:
     - backend-architect  # Use base backend architect
     - test-automator     # Use base test generation

   custom_subagents:
     - async-pattern-generator
     - dependency-injection-analyzer

   references:
     - async-testing-patterns.md
     - fastapi-project-layout.md
   ```

2. **Profile Installation Process**
   ```bash
   # Users can add profiles to their projects
   devforgeai add-profile python-fastapi

   # Or include in context files
   # project-root/devforgeai/PROFILE.md
   profile: python-fastapi
   ```

3. **Community Profile Repository**
   ```
   devforgeai-profiles (GitHub organization)
   ├── python-fastapi-profile/
   │   ├── PROFILE.md (definition)
   │   ├── .claude/agents/async-pattern-generator.md
   │   ├── references/async-testing.md
   │   └── examples/sample-story/
   ├── rust-tokio-profile/
   ├── dotnet-csharp-profile/
   └── java-spring-profile/
   ```

4. **Profile Validation**
   ```bash
   # Before publishing profile
   devforgeai validate-profile ./python-fastapi-profile/

   # Checks:
   ✓ PROFILE.md valid YAML
   ✓ All referenced subagents/skills exist
   ✓ No conflicts with core framework constraints
   ✓ Documentation complete and up-to-date
   ✓ Example stories execute successfully
   ```

5. **Profile Discovery & Registry**
   ```yaml
   # devforgeai-profiles registry (JSON)
   {
     "profiles": [
       {
         "id": "python-fastapi",
         "name": "Python + FastAPI + pytest",
         "author": "DevForgeAI Community",
         "version": "1.0.0",
         "min_framework_version": "1.1.0",
         "downloads": 1240,
         "rating": 4.8,
         "repo_url": "https://github.com/devforgeai-profiles/python-fastapi"
       },
       ...
     ]
   }
   ```

6. **Governance**
   ```
   Official Profiles (Maintained by core team):
   - typescript-node-express (v1.0+)
   - python-django-pytest (v1.0+)
   - csharp-dotnet-xunit (v1.0+)

   Community Profiles (User-maintained, community support):
   - rust-tokio-tokio-test
   - go-gin-testify
   - java-spring-junit5
   - (Register in community registry)

   Incubating (Early stage, not yet stable):
   - clojure-lein-midje
   - elixir-phoenix-exunit
   ```

7. **Profile Maintenance Commitment**
   ```markdown
   When publishing profile, author commits to:
   - Update profile for each DevForgeAI minor release
   - Support requests in GitHub issues (48-hour response)
   - Test profile against latest framework version
   - Remove profile if not updated within 2 releases
   ```

**Stakeholder Impact**:
- Maintainers: Core framework stays agnostic; specialized work in community
- Users: Can extend framework for their stack without waiting for core team
- Community: Clear process for creating and distributing profiles
- Educators: Can create Python-focused vs. JavaScript-focused courses
- Compatibility: Core framework changes don't break all profiles

**Success Metrics**:
- 5+ community profiles available within 6 months
- 80%+ adoption of profiles by new projects using that stack
- Profile validation automated (zero manual reviews needed)
- Profile update lag <1 sprint after framework releases

---

## Conflict #4: Skill Complexity vs. Usability

### The Tension
- **24+ commands** causes new user paralysis ("which one do I use?")
- **15+ skills** with varying patterns (some use AskUserQuestion, some don't)
- **6 context files** to understand before first story
- **Support team** reports 40% of first-time issues are "which command do I run?"

### Root Causes
1. Framework evolved organically; no consistent design patterns
2. No "simplified" onboarding path for new users
3. SKILL.md documentation varies (some 500 lines, some 1500 lines)
4. No visual decision tree or wizard for command selection

### Recommended Solution: Progressive Disclosure + Interactive Wizard

**Strategy**: Simplified entry points for beginners; full power available for experts

```
BEGINNER PATH (5 Essential Commands)     EXPERT PATH (24 Full Commands)
/brainstorm                              /brainstorm
/ideate                                  /ideate
/create-context                          /create-context
/create-story                            /create-epic
/dev (auto-runs TDD + QA)                /create-sprint
                                         /create-story
                                         /create-ui
                                         /dev (granular phases)
                                         /qa (independent)
                                         /release
                                         (+ 14 more...)
```

**Implementation**:

1. **Create Command Tiers**
   ```markdown
   # TIER 1: Essential (Required)
   - /brainstorm - Team ideation
   - /ideate - Structured requirements
   - /create-context - Set up framework
   - /create-story - Define story
   - /dev - Implement (includes TDD + QA by default)

   # TIER 2: Standard (Recommended)
   - /dev + granular phases (Red, Green, Refactor phases separately)
   - /qa (run QA independently if needed)
   - /release (manual release control)
   - /orchestrate (full lifecycle automation)

   # TIER 3: Advanced (Expert-Only)
   - /resume-dev (resume interrupted development)
   - /audit-deferrals (find deferred items)
   - /rca (root cause analysis)
   - /setup-github-actions (CI/CD integration)
   - (+ 10 more...)
   ```

2. **Interactive Wizard: /hello (First-Time Setup)**
   ```bash
   $ /hello

   Welcome to DevForgeAI!

   1. What's your role?
      a) Team Lead (wants best practices)
      b) Individual Developer (wants speed)
      c) DevOps/Infrastructure (wants automation)

   2. How many developers on your team?
      a) 1-3 (Individual/small team)
      b) 4-10 (Medium team)
      c) 10+ (Large team)

   3. How strict should we be with quality gates?
      a) Strict (95% coverage required)
      b) Standard (85% coverage required)
      c) Flexible (60% coverage + express mode)

   ✓ Based on your answers, here's your personalized flow:

   Your Path: Standard Developer + Medium Team + Strict Quality

   FIRST STORY:
   1. /brainstorm "Feature idea" (15 min)
   2. /ideate (structure requirements) (15 min)
   3. /create-context (set up framework) (5 min)
   4. /create-story (first story) (10 min)
   5. /dev (implement with TDD) (varies)

   Advanced commands available:
   - /dev --phase=red (just write tests)
   - /qa (run QA independently)
   - /orchestrate (full automation)

   Ready to start? Type: /brainstorm
   ```

3. **Command Decision Tree (Built into /help)**
   ```
   COMMAND SELECTOR

   I want to...
   ├─ Plan a feature
   │  ├─ Brainstorm with team → /brainstorm
   │  ├─ Formalize requirements → /ideate
   │  └─ Set up project framework → /create-context
   │
   ├─ Create a story
   │  ├─ Simple story → /create-story
   │  ├─ Complex story with UI → /create-story + /create-ui
   │  └─ Multiple related stories → /create-epic + /create-sprint
   │
   ├─ Implement a story
   │  ├─ Complete TDD (default) → /dev
   │  ├─ Just red phase (write tests) → /dev --phase=red
   │  ├─ Just green phase (implementation) → /dev --phase=green
   │  ├─ Just refactor phase → /dev --phase=refactor
   │  └─ Auto-run all phases → /orchestrate
   │
   ├─ Validate/test
   │  ├─ Quick syntax check → /qa --mode=light
   │  ├─ Full test suite → /qa --mode=deep
   │  └─ Find quality gaps → /qa --report
   │
   ├─ Deploy to production
   │  ├─ Manual control → /release --env=staging
   │  ├─ Automated deployment → /release --env=production
   │  └─ Rollback version → /release --action=rollback
   │
   └─ Diagnose problems
      ├─ Story went wrong → /rca --story=STORY-042
      ├─ Need to restart → /resume-dev --story=STORY-042
      └─ Find deferred work → /audit-deferrals
   ```

4. **Standardize Skill Patterns**
   ```yaml
   # All SKILL.md files must follow this structure:
   ---
   name: devforgeai-example
   description: "[1 line] Purpose of skill"
   invocation: "Skill(command=\"devforgeai-example --option=value\")"
   context_window: "Standard"
   prerequisites: "[Required context files/skills]"
   ---

   # PHASE 1: [Name]
   [Description]

   # PHASE 2: [Name]
   [Description]

   # Ambiguity Resolution
   IF [condition] → Use AskUserQuestion with:
   ...

   # See References
   - references/deep-dive.md - Advanced patterns
   - references/troubleshooting.md - Common issues
   ```

5. **Improve Error Messages with Next Steps**
   ```
   BEFORE (Confusing):
   ✗ HALT: Quality gate failed. Coverage below 95%.

   AFTER (Helpful):
   ✗ HALT: Quality gate failed. Coverage below 95%.

   Current coverage: 92.3%
   Missing coverage:
     - src/api/payment.ts (82% → need 3 more tests)
     - src/utils/validation.ts (88% → need 2 more tests)

   RECOVERY OPTIONS:
   1. Add tests: npm test -- --coverage (view gaps)
                  npm test -- --verbose (see what's not covered)
   2. Use express mode: /dev --mode=express --story=STORY-042
   3. Get help: /help --topic=coverage

   Recommended next step: Add 5 tests for payment.ts edge cases
   ```

**Stakeholder Impact**:
- New users: Clear onboarding path; /hello wizard reduces confusion
- Expert users: Full command set available; no "training wheels" forcing simple mode
- Support team: 70% fewer "which command?" questions
- Documentation team: Consistent SKILL.md format, easier to maintain
- PM: New project adoption faster with simplified path

**Success Metrics**:
- 80% of new teams reach first story within 1 week (vs. 3 weeks currently)
- Support tickets for "which command?" drop by 70%
- SKILL.md consistency score >90% (all follow standard format)
- Beginner command usage >60% in first month

---

## Conflict #5: Token Budget Constraints vs. Feature Completeness

### The Tension
- **Size limits**: Skills capped at 1000 lines (~40K characters)
- **Feature requests**: "Please add full TypeScript support analysis to backend-architect"
- **Problem**: Adding features requires splitting skills (adding complexity)
- **Maintainers concerned**: Framework becomes too fragmented

### Root Causes
1. Claude Code context windows create hard limits
2. Complex features need 50+ lines of documentation each
3. No standardized component extraction patterns
4. No dependency graph showing skill relationships

### Recommended Solution: Component Extraction Patterns + Dependency Graph

**Strategy**: Keep skills focused and lean; use explicit dependency patterns

```
MONOLITHIC (WRONG)             MODULAR (RIGHT)
1000-line skill                 300-line core skill
├─ Task A                       ├─ Task A
├─ Task B                       ├─ Task B
├─ Task C                       ├─ calls subagent-for-C
├─ Task D                       └─ calls skill-for-D
└─ Task E

Complexity: Single context      Complexity: Multiple contexts
Issue: Too long, hard to debug  Benefit: Focused, testable
```

**Implementation**:

1. **Create Component Extraction Guide**
   ```markdown
   # When to Extract a Component

   IF skill > 800 lines OR
      skill has 3+ major phases OR
      skill does 2+ unrelated things
   THEN extract a component

   ## Extraction Pattern

   ### Main Skill (300-400 lines)
   - Phase 1: Initial validation
   - Phase 2: Call helper skills/subagents
   - Phase 3: Aggregate results

   ### Helper Skill 1 (200-300 lines)
   - Focused task: Analysis step

   ### Helper Skill 2 (200-300 lines)
   - Focused task: Implementation step

   ### Subagent (100-150 lines)
   - Specialized domain: Code generation
   ```

2. **Skill Dependency Graph Format**
   ```yaml
   # devforgeai/SKILL-DEPENDENCIES.md

   orchestration-skill:
     depends_on:
       - development-skill
       - qa-skill
       - release-skill
     invoked_by:
       - /orchestrate (command)
     complexity: HIGH

   development-skill:
     depends_on:
       - test-automator (subagent)
       - refactoring-specialist (subagent)
     invoked_by:
       - /dev (command)
       - orchestration-skill
     complexity: HIGH

   test-automator:
     type: subagent
     dependencies: none
     complexity: MEDIUM
   ```

3. **Size Enforcement & Reporting**
   ```bash
   # Tool to check skill sizes
   devforgeai check-sizes

   Output:
   ✓ devforgeai-development: 725 lines (target: 500-800)
   ⚠ devforgeai-orchestration: 945 lines (target: 500-800)
     → Consider extracting "result aggregation" phase to separate skill
   ✗ devforgeai-qa: 1150 lines (exceeds maximum of 1000)
     → MUST extract component (suggestions: split deep/light modes into separate skills)
   ```

4. **Extraction Pattern Examples**
   ```markdown
   ## Pattern 1: Extract by Phase

   Large Skill (TDD implementation)
   ├─ Red Phase (250 lines) → keep in main skill
   ├─ Green Phase (250 lines) → keep in main skill
   ├─ Refactor Phase (500 lines) → EXTRACT to devforgeai-refactoring skill
   └─ Result Aggregation (50 lines) → keep in main skill

   Result: Main skill (550 lines) + Helper skill (500 lines)

   ---

   ## Pattern 2: Extract by Responsibility

   Large Skill (QA validation)
   ├─ Code Quality Analysis (200 lines) → Extract
   ├─ Security Scanning (250 lines) → Extract
   ├─ Coverage Validation (150 lines) → Extract
   ├─ Reporting (150 lines) → Keep in main skill
   └─ Gate Enforcement (50 lines) → Keep in main skill

   Result: Main skill (350 lines) + 3 Helper skills (200/250/150 lines)

   ---

   ## Pattern 3: Extract to Subagent

   Large Skill (Strategy selection)
   ├─ Validate inputs (100 lines)
   ├─ Strategic Analysis (800 lines) → Extract to subagent
   ├─ Results compilation (100 lines)
   └─ Reporting (50 lines)

   Result: Main skill (250 lines) + Subagent (800 lines)
   Note: Subagents have separate context windows; can be larger
   ```

5. **Dependency Documentation Pattern**
   ```markdown
   # devforgeai-orchestration Skill

   ## Invocation Graph
   ```
   /orchestrate command
     ↓ invokes
   devforgeai-orchestration skill
     ├─ invokes devforgeai-development (TDD phases)
     ├─ invokes devforgeai-qa (quality validation)
     ├─ invokes devforgeai-release (deployment)
     └─ invokes git-validator subagent
   ```

   ## Parallel Execution
   - dev + qa can run in parallel (different code areas)
   - qa must complete before release (gates release)
   - Total time: ~2 hours (vs. 4 hours sequential)

   ---

   ## Size Budget
   - orchestration skill: 350 lines (coordination only)
   - development skill: 750 lines (TDD phases)
   - qa skill: 600 lines (validation logic)
   - release skill: 400 lines (deployment)
   - Total: 2100 lines across 4 skills + subagents
   ```

6. **Extract-on-Grow Policy**
   ```
   When a skill reaches 800 lines:
   1. Identify extractable components (phases, responsibilities)
   2. Create extraction plan (which lines → new skill)
   3. Update SKILL-DEPENDENCIES.md
   4. Extract component to new skill (or subagent)
   5. Add invocation call from main skill
   6. Verify main skill now <800 lines
   7. Test coordinated execution
   8. Document in release notes
   ```

**Stakeholder Impact**:
- Maintainers: Clear extraction patterns prevent ad-hoc decisions
- Developers: Skills stay focused, easier to understand and modify
- QA: Smaller units easier to test in isolation
- Documentation: Dependency graph shows system architecture
- Users: No visible change; same functionality, better organized

**Success Metrics**:
- All skills <800 lines (none exceed 1000 line max)
- Average skill size: 500-600 lines (currently: 650)
- Dependency graph shows <3 levels deep (avoid excessive nesting)
- Extract-on-grow followed for 100% of new features

---

## Conflict #6: Rapid Feature Iteration vs. Documentation Currency

### The Tension
- **Framework changes** weekly (new skills, context file updates)
- **Documentation team** can't keep pace (docs updated monthly)
- **User confusion**: Examples in docs don't match latest code
- **Support load**: Questions about version differences increase

### Root Causes
1. Documentation written manually for each release
2. No automated documentation generation from source
3. Version markers missing (docs for v1.0 vs. v1.1 vs. v1.2)
4. Tutorial examples become stale quickly

### Recommended Solution: Auto-Generated + Versioned Documentation

**Strategy**: Generate docs from code; version docs by framework version

```
Framework Source Code
  ↓ Extract metadata
├─ SKILL.md frontmatter → Skill reference
├─ Subagent.md frontmatter → Subagent registry
├─ Story acceptance criteria → Tutorial content
└─ CHANGELOG.md → Migration guides

Generated Docs (Auto)
├─ API Reference (always current)
├─ Example commands (from SKILL.md)
├─ Subagent registry (with tool permissions)
└─ Migration guides (v1.0 → v1.1 → v1.2)

Manual Docs (Human)
├─ Concepts & philosophy
├─ Getting started guide
├─ Troubleshooting FAQ
└─ Community best practices
```

**Implementation**:

1. **Extract Metadata from SKILL.md**
   ```yaml
   # All SKILL.md files must have this frontmatter
   ---
   name: devforgeai-development
   description: "Implement user stories using Test-Driven Development"
   version: "1.1.0"
   framework_version: "1.1.0"  # Minimum required
   input_parameters:
     - name: story
       type: string
       description: "Story file path (e.g., devforgeai/specs/Stories/STORY-042.md)"
       required: true
     - name: phase
       type: enum
       values: ["red", "green", "refactor", "all"]
       default: "all"
   prerequisites:
     - "Context files in devforgeai/specs/context/"
     - "Story file with acceptance criteria"
   invocation: "Skill(command=\"devforgeai-development --story=STORY-042 --phase=red\")"
   ---
   ```

2. **Auto-Generate Skill Reference**
   ```bash
   # Script: devforgeai/docs/generate-docs.sh

   # Extract all SKILL.md frontmatter
   for skill in .claude/skills/*/SKILL.md; do
     extract_frontmatter "$skill" >> docs/generated/skill-reference.md
   done

   # Extract all subagent descriptions
   for agent in .claude/agents/*.md; do
     extract_description "$agent" >> docs/generated/subagent-registry.md
   done

   # Output: docs/generated/skill-reference-v1.1.0.md (versioned)
   ```

3. **Version Documentation by Release**
   ```
   docs/
   ├─ v1.0/
   │  ├─ getting-started.md
   │  ├─ skill-reference.md (for v1.0)
   │  ├─ commands.md (24 commands in v1.0)
   │  └─ examples/ (working examples for v1.0)
   ├─ v1.1/
   │  ├─ getting-started.md (updated)
   │  ├─ skill-reference.md (includes new skills in v1.1)
   │  ├─ commands.md (25 commands in v1.1)
   │  ├─ MIGRATION-1.0-to-1.1.md (breaking changes, how to upgrade)
   │  └─ examples/ (updated examples)
   └─ v2.0/ (future)
      └─ ...

   Default documentation points to latest stable (v1.1)
   Users can select version if using older framework
   ```

4. **Embed Version in Examples**
   ```markdown
   # Example: Implementing Your First Story

   **Framework Version**: v1.1.0+ (last verified: 2025-12-22)

   This example works with:
   ✓ devforgeai v1.1.0
   ✓ devforgeai v1.1.1
   ✓ devforgeai v1.2.0 (forward compatible)
   ✗ devforgeai v1.0.x (use docs/v1.0/examples instead)

   ## Step 1: Create a Story

   ```bash
   /create-story --epic=EPIC-001 --title="Add user authentication"
   ```

   [Example output showing v1.1.0 output format]
   ```

5. **Tutorial & Example Management**
   ```markdown
   # docs/examples/EXAMPLE-001-hello-world/

   ## Metadata
   - Title: "Your First Story: Hello World App"
   - Framework Version: v1.1.0+
   - Estimated Time: 30 minutes
   - Level: Beginner
   - Tech Stack: Node.js + Express + Jest

   ## Example Contents
   1. story.md (STORY-001 definition)
   2. test.js (Red phase - failing tests)
   3. implementation.js (Green phase - minimal code)
   4. refactored.js (Refactor phase - clean code)
   5. README.md (explanation of each phase)

   ## Auto-Verification
   - Run `npm test` on implementation.js → Should fail (Red)
   - Run `npm test` on refactored.js → Should pass (Green + Refactor)
   - Verify against framework v1.1.0 using example test

   Last Verified: 2025-12-22 (v1.1.0)
   ```

6. **Breaking Change Alert System**
   ```markdown
   # Automatic Breaking Change Alerts

   When creating a breaking change:
   1. Document in CHANGELOG.md (required)
   2. Create migration guide (docs/MIGRATION-v1.0-to-v1.1.md)
   3. Add version check to relevant skills
   4. Embed alert in old docs (auto-generated)

   ## Old Docs Auto-Include
   # docs/v1.0/skill-reference.md

   > ⚠️ **NOTE**: This is documentation for v1.0.
   > DevForgeAI v1.1 has breaking changes.
   > [See migration guide](../MIGRATION-v1.0-to-v1.1.md)
   ```

7. **Update Verification Process**
   ```bash
   # Before shipping release
   devforgeai verify-docs

   Checks:
   ✓ All SKILL.md files have frontmatter
   ✓ All examples work with latest framework
   ✓ Breaking changes documented in MIGRATION
   ✓ Docs for new version generated
   ✓ Old docs marked with version numbers
   ✓ No outdated version references in latest docs

   If any check fails: Block release
   ```

**Stakeholder Impact**:
- Documentation team: Auto-generation saves time; focus on concepts
- Users: Docs always current; examples work; version clarity
- Support: Fewer version-related questions; migration guides clear
- Maintainers: Breaking changes visible in auto-generated docs
- Community: Clear path to contribute docs

**Success Metrics**:
- Zero outdated examples in current docs
- Documentation updated within 1 hour of release (auto-generation)
- User complaints about stale docs drop by 90%
- Example verification: 100% of examples pass execution tests
- Version clarity: 95% of users choose correct docs version

---

## Conflict #7: Tool Privilege Principle vs. Subagent Functionality

### The Tension
- **Security Officer** wants "least privilege" (minimize tool access)
- **Subagent Developers** need flexible tools to accomplish tasks
- **Audit complexity**: Tracking which tools each subagent uses
- **Risk**: Accidental access to powerful tools (Write/Bash) creates security surface

### Root Causes
1. Tool bundles not standardized (each subagent requests different combo)
2. No audit trail showing which tools are actually used
3. Trade-off between functionality and security not explicit
4. New subagent types discover "I need more tools" mid-implementation

### Recommended Solution: Tool Bundles + Audit Trail + Capability Declaration

**Strategy**: Predefined tool bundles; explicit capability declarations; audit logging

```
TOOL BUNDLES (Predefined)

[read-only]           [code-modify]         [infrastructure]
├─ Read              ├─ Read                ├─ Read
├─ Glob              ├─ Edit                ├─ Write
├─ Grep              ├─ Write               ├─ Bash (docker, terraform, kubectl)
└─ AskUserQuestion   ├─ Bash (npm test)     ├─ Bash (git)
                     └─ AskUserQuestion     └─ AskUserQuestion

[analysis]            [security]            [full-access]
├─ Read              ├─ Read                ├─ All tools (reserved for core skills only)
├─ Glob              ├─ Grep
├─ Grep              ├─ Bash (npm audit)
├─ WebSearch         └─ AskUserQuestion
└─ WebFetch
```

**Implementation**:

1. **Define Tool Bundles**
   ```yaml
   # .claude/rules/tool-bundles.md

   ## read-only
   Purpose: Code analysis, search, questions
   Tools:
     - Read
     - Glob
     - Grep
     - AskUserQuestion
   Examples: code-reviewer, code-analyzer, requirements-analyst

   ## code-modify
   Purpose: Code generation, testing, refactoring
   Tools:
     - Read
     - Edit
     - Write
     - Bash (npm test, pytest, etc. - test running only)
     - AskUserQuestion
   Examples: test-automator, refactoring-specialist, frontend-developer

   ## infrastructure
   Purpose: Deployment, DevOps, system configuration
   Tools:
     - Read
     - Write
     - Bash (docker, terraform, kubectl, ansible, helm, git)
     - AskUserQuestion
   Examples: deployment-engineer, git-worktree-manager

   ## analysis
   Purpose: Research, competitive intelligence, documentation
   Tools:
     - Read
     - Glob
     - Grep
     - WebSearch
     - WebFetch
     - AskUserQuestion
   Examples: internet-sleuth, api-designer

   ## security
   Purpose: Security auditing, vulnerability scanning
   Tools:
     - Read
     - Grep
     - Bash (npm audit, pip check, security scanners - read-only)
     - AskUserQuestion
   Examples: security-auditor

   ## full-access
   Purpose: Framework orchestration (core skills only)
   Tools: All available
   Access: Restricted to core framework maintainers
   Examples: devforgeai-orchestration, devforgeai-development
   ```

2. **Tool Declaration in Subagent Spec**
   ```yaml
   # .claude/agents/code-reviewer.md

   ---
   name: code-reviewer
   description: "Senior code review specialist ensuring quality, security, maintainability"
   tools_bundle: "read-only"  # Explicit declaration

   tool_justification: |
     - Read: Analyze source code files
     - Glob: Find files matching patterns (e.g., test files)
     - Grep: Search for patterns (e.g., error handling)
     - AskUserQuestion: Clarify architectural intent

     NOT NEEDED:
     - Edit/Write: Reviews are advisory; core team implements changes
     - Bash: No code execution; read-only analysis only

   tool_audit: "Last reviewed 2025-12-15 by security officer"
   ---
   ```

3. **Tool Audit Trail Format**
   ```bash
   # .claude/audit/tool-usage.log
   # Auto-generated log of actual tool usage

   2025-12-22T14:35:12Z subagent=code-reviewer tool=Read path="src/api.ts"
   2025-12-22T14:35:18Z subagent=code-reviewer tool=Glob pattern="**/*.test.ts"
   2025-12-22T14:35:24Z subagent=code-reviewer tool=Grep pattern="TODO" file="src/"
   2025-12-22T14:35:31Z subagent=code-reviewer tool=AskUserQuestion header="Architecture intent"

   # Verify at release time:
   # code-reviewer ONLY used: Read, Glob, Grep, AskUserQuestion
   # NEVER used: Edit, Write, Bash ✓ APPROVED
   ```

4. **Capability Declaration System**
   ```yaml
   # When a subagent needs tool access NOT in its bundle:

   name: custom-code-generator
   tools_bundle: "code-modify"

   # Standard tools from code-modify bundle:
   #   - Read, Edit, Write, Bash (test only), AskUserQuestion ✓

   # Additional tools requested (requires justification + approval):
   additional_tools:
     - name: "Bash (npm install)"
       justification: "Install dependencies for code generation templates"
       security_review: "APPROVED by security-officer on 2025-12-15"
       approval_ticket: "SECURITY-042"

     - name: "Bash (git)"
       justification: "Clone template repositories for code patterns"
       security_review: "APPROVED by security-officer on 2025-12-15"
       approval_ticket: "SECURITY-043"

   # Review process:
   # 1. Subagent dev requests additional tools in spec
   # 2. Security officer reviews (1-2 days)
   # 3. If approved: Add to spec + create SECURITY ticket for audit
   # 4. If denied: Suggest alternative approach
   ```

5. **Tool Audit Checklist (Pre-Release)**
   ```markdown
   # Security Review Checklist: Tool Privileges

   For each new/modified subagent:

   - [ ] Tool bundle declared in frontmatter
   - [ ] Tool justification includes business case
   - [ ] No unnecessary Write access (read-only if possible)
   - [ ] No unnecessary Bash access (scoped to specific commands)
   - [ ] Additional tools justified and approved
   - [ ] Audit trail shows only declared tools used
   - [ ] No attempted access to undeclared tools (in logs)
   - [ ] Documentation explains why each tool needed

   Sign-off: ________ (Security Officer)
   Date: ___________
   ```

6. **Runtime Tool Enforcement** (Optional, for high-security contexts)
   ```
   Claude Code can optionally enforce tool restrictions:

   When subagent attempts to use tool NOT in its bundle:
   - Log attempt (security audit trail)
   - Block operation with error message
   - Alert security officer if repeated attempts

   This prevents "privilege creep" where subagent gradually
   acquires more permissions than authorized.
   ```

**Stakeholder Impact**:
- Security Officer: Clear tool restrictions; audit trails; approval process
- Subagent Developers: Flexible within approved bundles; clear requesting process
- Maintainers: Systematic tool privilege management; audit ready
- Users: Transparency on what tools each subagent can access
- Compliance: Audit trail shows all tool usage per subagent

**Success Metrics**:
- 100% of subagents have explicit tool bundle declaration
- All tool requests approved before use (zero unauthorized access)
- Audit trail captures 100% of tool usage
- Security review time <2 days per subagent change
- Zero unauthorized tool access incidents

---

## Conflict #8: Backward Compatibility vs. Technical Debt Cleanup

### The Tension
- **Release Lead** wants backward compatibility (no breaking changes)
- **Maintainers** see technical debt (ast-grep removal, CLAUDE.md format issues)
- **Breaking changes** → Major version bump (v1.0 → v2.0) → User migrations
- **But not fixing debt** → Harder to change code later → Interest compounds

### Root Causes
1. Architectural decisions made early (ast-grep, CLAUDE.md format) now limiting
2. Breaking changes require major version bump with 1-month migration notice
3. Users hesitant to upgrade major versions (significant effort)
4. Framework success means many projects depending on current design

### Recommended Solution: Staged Deprecation + Upgrade Tools + Batch Breaking Changes

**Strategy**: Multi-release deprecation path; automated migration tools; batch changes into single major release

```
CURRENT STATE (v1.1.0)    DEPRECATION (v1.2.0)      NEW STATE (v2.0.0)
Old: ast-grep pattern     Warning: "ast-grep        New: tree-sitter AST
     matching             deprecated; use           traversal
                          tree-sitter instead"
                          ✓ Still works
Old: CLAUDE.md format     Warning: "Format          New: CLAUDE.md v2 format
     (unversioned)        deprecated; run            (with version tracking)
                          migration tool"
Old: 3-layer arch         Docs: "Consider           New: 4-layer arch
                          transitioning to          (with plugins)
                          plugin system"
```

**Implementation**:

1. **Establish Deprecation Policy (Document in CHANGELOG.md)**
   ```markdown
   # DevForgeAI Deprecation Policy

   ## Timeline
   - **Release 1** (v1.X.Y): Feature announced, new preferred approach introduced
   - **Release 2** (v1.Z.0): Old approach deprecated (warning messages, but functional)
   - **Release 3** (v2.0.0): Old approach removed completely

   Example: ast-grep deprecation
   - v1.0.0: ast-grep introduced for static analysis
   - v1.1.0: tree-sitter introduced as alternative (alongside ast-grep)
   - v1.2.0: ast-grep marked deprecated (still works, warning shown)
   - v2.0.0: ast-grep removed completely; tree-sitter mandatory

   ## Exception: Emergency Security Deprecations
   If security vulnerability discovered:
   - Immediate: Issue security advisory
   - Immediate: Release patch (v1.0.X) with deprecation
   - Acceleration: Remove vulnerable feature in next major release (might be <2 releases)
   ```

2. **Create Breaking Change Migration Tools**
   ```bash
   # Tool: devforgeai-migrator

   devforgeai migrate-project /path/to/old-project v1.1.0 v2.0.0

   Output:
   ✓ Detected breaking changes (3 found)

   1. CLAUDE.md format change (v1 → v2)
      Current: Unversioned
      New: With version tracking
      Migration tool: ./migrate-claude-md.sh
      Status: Auto-migrated

   2. ast-grep removal
      Current: Uses ast-grep for pattern matching
      Replacement: tree-sitter AST analysis
      Migration tool: ./migrate-ast-grep-to-tree-sitter.sh
      Status: Manual review required

   3. 3-layer arch → 4-layer arch with plugins
      Current: Skills → Subagents → Commands
      New: Skills → Plugins → Subagents → Commands
      Migration: Most projects unaffected (passive backward compat)
      Status: Auto-migrated

   Ready to migrate? [y/n]
   ```

3. **Batch Breaking Changes into Single Major Release**
   ```
   v1.x.x ROADMAP (No major breaking changes)
   ├─ v1.1.0: New skills (tree-sitter support), new commands
   ├─ v1.2.0: Deprecation warnings for v2.0
   ├─ v1.3.0: More features, prepare for v2.0
   └─ v1.4.0: Feature freeze; only bug fixes going forward

   v2.0.0 BREAKING CHANGES (All at once)
   ├─ CLAUDE.md v2 format (required)
   ├─ Remove ast-grep (use tree-sitter only)
   ├─ 4-layer architecture with plugins
   ├─ Installer using NPM instead of Python
   ├─ Context file format v2
   └─ (All breaking changes shipped together)

   Migration impact: Single migration effort (not piecemeal)
   ```

4. **Create Migration Guide Template**
   ```markdown
   # Migration Guide: DevForgeAI v1.4 → v2.0

   **Estimated Migration Time**: 4-8 hours per project
   **Difficulty**: Moderate (most changes automated)
   **Support Available**: Community forum + Discord + email

   ## Breaking Changes (3 total)

   ### 1. CLAUDE.md Format
   **What Changed**: Version tracking added
   **Impact Level**: MEDIUM (affects development workflow)

   **Automated Migration**:
   ```bash
   devforgeai migrate-project ./my-project
   ```

   **Manual Review**:
   After automated migration, review:
   - `.claude/version` file created
   - CLAUDE.md has `<!-- VERSION: 2.0.0 -->` marker
   - Custom sections preserved

   **Rollback**: Old CLAUDE.md backed up as CLAUDE.md.v1.backup

   ### 2. ast-grep → tree-sitter
   **What Changed**: Static analysis tool replaced
   **Impact Level**: HIGH (if you use ast-grep for custom analysis)

   **If using default skills**: Automatic (no action needed)
   **If using custom ast-grep rules**:
   1. Identify rules in your ADRs/docs
   2. Convert to tree-sitter patterns
   3. Migration guide: [Link to ast-grep→tree-sitter cookbook](cookbook.md)
   4. Test converted rules

   **Example Conversion**:
   ```
   ast-grep: pattern: "function($FUNC) { ... }"
   tree-sitter: traverse(AST) → find(function_declaration)
   ```

   ### 3. Architecture: 3-Layer → 4-Layer
   **What Changed**: Plugin layer inserted
   **Impact Level**: LOW (mostly backward compatible)

   **Migration Required If**:
   - You created custom skills (slight refactoring)
   - You extended skill invocation patterns

   **Not Required If**:
   - You use framework as-is (passive compatibility)
   - You only invoke commands (no skill customization)

   ## Step-by-Step Migration

   ### Phase 1: Backup & Test Environment
   ```bash
   1. git commit all changes (on v1.4)
   2. Create migration branch: git checkout -b upgrade/v2.0
   3. Backup CLAUDE.md: cp CLAUDE.md CLAUDE.md.v1.backup
   4. Create test project copy
   ```

   ### Phase 2: Run Automated Migration
   ```bash
   devforgeai migrate-project ./my-project
   # Reviews changes, creates migration report
   ```

   ### Phase 3: Manual Review
   ```
   Review migration report
   ├─ CLAUDE.md format ✓ (usually passes)
   ├─ Custom ast-grep rules ✓ (may need manual work)
   ├─ Custom skills ✓ (usually pass)
   └─ Plugins integration ✓ (verify)
   ```

   ### Phase 4: Test First Story
   ```bash
   /create-story --title="Migration test story"
   /dev --story=STORY-TEST
   # Should succeed with no errors
   ```

   ### Phase 5: Deploy to Production
   ```bash
   git push origin upgrade/v2.0
   Create PR, team review
   Merge and deploy
   ```

   ## Rollback Procedure (If something goes wrong)
   ```bash
   # Rollback to v1.4
   git revert <migration-commit>
   rm -rf devforgeai/v2
   cp CLAUDE.md.v1.backup CLAUDE.md
   npm install devforgeai@1.4  # or @latest-1.x

   # Test
   /dev --story=STORY-EXISTING
   ```

   ## FAQ

   **Q: Can I skip v2.0 and stay on v1.4?**
   A: Yes, v1.4 will receive patch updates (v1.4.1, v1.4.2) for 12 months (through 2026-Q4).

   **Q: What if automated migration fails?**
   A: See manual migration section; community support available.

   **Q: Do all my custom subagents need updates?**
   A: No, subagents are fully backward compatible if they use standard tools.

   **Q: How long until v1.4 goes out of support?**
   A: 12 months from v2.0 release (approximately 2026-Q4).
   ```

5. **Release Announcement Template**
   ```markdown
   # DevForgeAI v2.0.0 - Major Update Available

   We're excited to announce DevForgeAI v2.0.0 with significant improvements:

   ## What's New
   - 4-layer architecture with plugin system (enables community extensions)
   - tree-sitter integration for advanced static analysis
   - NPM-based installer (easier distribution to Node.js ecosystem)
   - CLAUDE.md v2 format (better version tracking)

   ## Breaking Changes (Requires Migration)
   **Estimated Migration Time**: 4-8 hours per project

   See full migration guide: [Link]

   ## Timeline
   - **Today**: v2.0.0 released
   - **30 days**: v1.4 enters maintenance mode (patch fixes only)
   - **12 months**: v1.4 goes out of support

   ## Migration Support
   - Migration tool: `devforgeai migrate-project`
   - Community help: [Discord/GitHub/Forum]
   - Official support: [Email support]
   - Video walkthrough: [YouTube]

   ## Rollback Option
   ```bash
   npm uninstall -g devforgeai
   npm install -g devforgeai@1.4
   ```

   v1.4 will continue receiving patch updates for 12 months.
   ```

6. **Version Compatibility Matrix (Visible to Users)**
   ```markdown
   # Supported Versions

   | Version | Status | Support Until | Notes |
   |---------|--------|---------------|-------|
   | v2.1.x | CURRENT | 2027-Q4 | Latest features |
   | v2.0.x | ACTIVE | 2027-Q2 | Stable branch |
   | v1.4.x | MAINTENANCE | 2026-Q4 | Patch fixes only |
   | v1.3.x | EOL | 2025-12-31 | Use v1.4 or v2.0 |
   | v1.0.x | EOL | 2025-09-30 | Unsupported |

   **Recommendation**:
   - New projects: Use v2.1.x
   - Existing projects: Migrate to v2.0 within 12 months
   - Urgent deadline: Stay on v1.4 (support until 2026-Q4)
   ```

**Stakeholder Impact**:
- Release Lead: Clear deprecation policy; automated migration tools reduce support burden
- Maintainers: Can address technical debt without guilt
- Users: Clear timeline for breaking changes; migration automation; support available
- Framework ecosystem: Healthy evolution without stalling on old patterns
- Community: Can contribute improvements without backward compatibility constraints

**Success Metrics**:
- Major version transitions: <1 month average migration time per project
- Deprecation warnings appear in v1.X before removal in v2.0
- Automated migration tools reduce manual work by 70%
- 90% of projects migrate to v2.0 within 6 months
- Zero regression issues reported post-migration

---

## Summary: Conflict Resolution Maturity Model

| Stage | Characteristics | DevForgeAI Current State |
|-------|---|---|
| **Unaware** | Conflicts ignored | ❌ Not here |
| **Reactive** | Conflicts surface in crises | ⚠️ Incidents (RCA-006, RCA-013) |
| **Proactive** | Conflicts anticipated + planned | ✓ Implementing strategies |
| **Integrated** | Conflicts resolved systematically | → Goal: Next 2 sprints |
| **Optimized** | Conflict feedback loop continuous | → Goal: Next quarter |

---

**Document Version**: 1.0
**Last Updated**: 2025-12-22
**Next Review**: 2026-01-22 (30 days) - After implementing first 2 resolutions
**Stakeholder Feedback Deadline**: 2025-12-29 (7 days)
