# DevForgeAI Subagents Reference

<overview>
Detailed guidance for working with the 44 specialized subagents.

**Last Updated:** 2026-02-24

Subagents are specialized AI workers with domain expertise that operate in isolated contexts. They are automatically invoked by DevForgeAI skills or can be explicitly called for specific tasks. **44 subagents** are available in `.claude/agents/`.
</overview>

---

<invocation_methods>
## Subagent Invocation Methods

### 1. Automatic Invocation (Proactive)

Subagents are automatically invoked by DevForgeAI skills at appropriate workflow phases:

**During spec-driven-dev:**
- **Phase 0 (Preflight)**: git-worktree-manager creates isolated worktree, dependency-graph-analyzer validates dependencies, file-overlap-detector checks for conflicts
- **Phase 1 (Red)**: test-automator generates failing tests from acceptance criteria
- **Phase 2 (Green)**: backend-architect or frontend-developer implements code to pass tests
- **Phase 2 (Validation)**: context-validator checks constraint compliance
- **Phase 3 (Refactor)**: refactoring-specialist improves code quality, code-reviewer provides feedback
- **Phase 4 (Integration)**: integration-tester creates cross-component tests
- **Phase 4.5 (AC Verify)**: ac-compliance-verifier validates acceptance criteria with fresh context (NEW - EPIC-046)
- **Phase 5.5 (AC Verify)**: ac-compliance-verifier validates post-integration acceptance criteria (NEW - EPIC-046)
- **Phase 9 (Feedback)**: observation-extractor captures workflow insights, framework-analyst synthesizes recommendations

**During spec-driven-qa:**
- **Phase 0 Step 2.5**: deferral-validator validates deferred DoD items (MANDATORY)
- **Light Validation**: context-validator checks constraints
- **Deep Validation**: security-auditor scans for vulnerabilities, test-automator fills coverage gaps
- **Phase 5 Step 6**: qa-result-interpreter interprets results and generates user-facing display (NEW - QA Refactoring)

**During spec-driven-ui:**
- **Phase 6 Step 3.5**: ui-spec-formatter formats and validates generated UI specifications (NEW - UI Refactoring)

**During spec-driven-architecture:**
- architect-reviewer validates architecture decisions
- api-designer defines API contract standards
- CLAP alignment auditor validates cross-layer configuration alignment (Phase 5.5 - NEW EPIC-081)

**During spec-driven-release:**
- deployment-engineer handles infrastructure and deployment
- security-auditor performs pre-release security scan

### 2. Explicit Invocation

Invoke subagents directly using the Task tool with `subagent_type` parameter:

<example type="basic">
```
Task(
  subagent_type="test-automator",
  description="Generate tests for calculator",
  prompt="Generate comprehensive unit tests for a calculator class with add, subtract, multiply, and divide methods. Follow TDD principles and AAA pattern."
)
```
</example>

**Examples:**

<examples>
<example type="code_review">
```
# Code review
Task(
  subagent_type="code-reviewer",
  description="Review authentication code",
  prompt="Review the authentication implementation in src/auth/ for security issues, code quality, and adherence to coding standards."
)
```
</example>

<example type="frontend">
```
# Frontend implementation
Task(
  subagent_type="frontend-developer",
  description="Implement login component",
  prompt="Implement a login form component in React following the design system in context files. Include email/password fields, validation, and API integration."
)
```
</example>

<example type="security">
```
# Security audit
Task(
  subagent_type="security-auditor",
  description="Audit payment processing",
  prompt="Perform comprehensive security audit of payment processing code in src/payments/ focusing on PCI compliance and OWASP Top 10."
)

# Context validation
Task(
  subagent_type="context-validator",
  description="Validate constraints",
  prompt="Check all code changes for violations of the 6 context files (tech-stack, source-tree, dependencies, coding-standards, architecture-constraints, anti-patterns)."
)
```
</example>
</examples>

### 3. Parallel Execution

Multiple subagents can run simultaneously for different tasks:

<example type="parallel">
```
# Send single message with multiple Task tool calls
Task(subagent_type="test-automator", description="Generate tests", prompt="...")
Task(subagent_type="documentation-writer", description="Write API docs", prompt="...")

# Both execute in parallel, return results independently
```
</example>
</invocation_methods>

---

<subagents_catalog>
## Available Subagents

| Subagent | Purpose | Model | Token Target | When to Use |
|----------|---------|-------|--------------|-------------|
| **test-automator** | TDD test generation (unit, integration, E2E) | sonnet | <50K | Implementing features, filling coverage gaps |
| **backend-architect** | Backend implementation (clean architecture, DDD) | sonnet | <50K | Implementing backend features, APIs, services |
| **frontend-developer** | Frontend implementation (React, Vue, Angular) | sonnet | <50K | Implementing UI components, state management |
| **context-validator** | Fast constraint enforcement (6 context files) | haiku | <5K | Before commits, after implementation |
| **code-reviewer** | Code quality and security review | inherit | <30K | After implementation, during refactoring |
| **security-auditor** | OWASP Top 10, auth/authz, vulnerability scanning | sonnet | <40K | After auth code, handling sensitive data |
| **deployment-engineer** | Infrastructure, IaC, CI/CD pipelines | sonnet | <40K | Release phase, deployment configuration |
| **requirements-analyst** | User story creation, acceptance criteria | sonnet | <30K | Epic decomposition, story planning |
| **story-requirements-analyst** | Story requirements (content-only, RCA-007 fix) | sonnet | <50K | spec-driven-stories Phase 2 (replaces general-purpose) |
| **documentation-writer** | Technical docs, API specs, user guides | sonnet | <30K | After API implementation, when coverage <80% |
| **architect-reviewer** | Architecture validation, design patterns | sonnet | <40K | After ADRs, major architectural changes |
| **refactoring-specialist** | Safe refactoring, code smell removal | inherit | <40K | When complexity >10, code duplication >5% |
| **integration-tester** | Cross-component testing, API contracts | sonnet | <40K | After unit tests pass, API endpoints ready |
| **api-designer** | REST/GraphQL/gRPC contract design | sonnet | <30K | Creating new APIs, ensuring consistency |
| **agent-generator** | Generate framework-aware Claude Code subagents (ENHANCED v2.0) | haiku | <50K | Creating subagents for DevForgeAI, command refactoring, custom domains |
| **alignment-auditor** | Configuration layer alignment auditing (CLAP). Tools: Read, Glob, Grep | haiku | <15K | After /create-context, after ADR acceptance, /audit-alignment command (NEW - EPIC-081) |
| **deferral-validator** | Deferral justification validation, circular detection | haiku | <5K | Before commits (dev), before QA approval (qa) |
| **dead-code-detector** | Dead code detection specialist using call-graph analysis (Treelint deps --calls). Finds unused functions with entry-point exclusion logic and confidence scoring for dynamic dispatch. Read-only tools only (ADR-016) — zero risk of incorrect code deletion. | inherit | <30K | After major refactoring, when dead code suspected, pre-release cleanup |
| **technical-debt-analyzer** | Debt trend analysis, pattern detection, reporting | sonnet | <30K | Sprint planning, retrospectives, debt reviews |
| **tech-stack-detector** | Technology detection and tech-stack.md validation | haiku | <10K | Development workflow init, architecture validation |
| **git-validator** | Git availability check, workflow strategy, and enhanced file analysis (RCA-008 Phase 2.5) | haiku | <5K | Before development workflows, release validation (enhanced with file categorization per RCA-008) |
| **qa-result-interpreter** | QA result interpretation and display generation | haiku | <8K | After QA report generation, before user display (NEW - QA Refactoring) |
| **sprint-planner** | Sprint creation and capacity validation | sonnet | <40K | Sprint planning, story selection, capacity validation (NEW - Sprint Refactoring) |
| **ui-spec-formatter** | UI spec validation and display generation | haiku | <10K | After UI spec generation, before user display (NEW - UI Refactoring 2025-11-05) |
| **code-analyzer** | Deep codebase analysis for documentation metadata | sonnet | <50K | Brownfield documentation, architecture discovery, gap analysis (NEW - STORY-040) |
| **internet-sleuth** | Research & competitive intelligence, web research automation | haiku | <50K | Market research, technology discovery, repository archaeology (AUTO-INVOKED by ideation) |
| **pattern-compliance-auditor** | Lean orchestration pattern compliance auditing | haiku | <15K | Command refactoring analysis, budget violation detection (/audit-budget command) |
| **dev-result-interpreter** | Development workflow result interpretation and display | haiku | <8K | After /dev completes, before result display (similar to qa-result-interpreter) |
| **diagnostic-analyst** | Read-only diagnostic analysis subagent for spec drift detection and root cause investigation across constitutional context files. Has NO write access — investigates and reports only. | opus | <30K | When spec-driven-rca skill is invoked, persistent failures after 3+ fix attempts |
| **ac-compliance-verifier** | Fresh-context AC verification without prior coding knowledge | opus | <40K | Phase 4.5/5.5 of /dev workflow for independent AC verification (NEW - EPIC-046) |
| **observation-extractor** | Extract structured observations from subagent outputs | haiku | <15K | At phase exit gates, after test-automator/code-reviewer/backend-architect (NEW - STORY-319) |
| **session-miner** | Parse history.jsonl for session mining and workflow insights | opus | <50K | EPIC-034 session mining, command pattern analysis, workflow metrics (NEW) |
| **framework-analyst** | Synthesize workflow observations into improvement recommendations | opus | <40K | Phase 09 of /dev workflow, after observation extraction (NEW) |
| **dependency-graph-analyzer** | Story dependency validation with transitive resolution | opus | <30K | /dev Phase 0 Step 0.2.5 for dependency enforcement (NEW - EPIC-010) |
| **entrepreneur-assessor** | Normalizes self-reported assessment questionnaire responses into a structured user profile. Single responsibility: transform raw dimension responses into calibrated profile data. | inherit | <15K | When assessing entrepreneur profiles, during onboarding assessment workflows |
| **epic-coverage-result-interpreter** | Formats epic coverage validation results for display. Generates four display templates: single-epic breakdown, all-epics summary table, actionable gap list, and batch creation summary. | haiku | <8K | After validating-epic-coverage skill completes, before coverage results display |
| **file-overlap-detector** | Detect file overlaps between parallel stories | opus | <30K | /dev Phase 0 Step 0.2.6 for file overlap prevention (NEW - EPIC-010) |
| **git-worktree-manager** | Git worktree lifecycle for parallel development | opus | <30K | /dev Phase 0 Step 0.2 for isolated worktree creation (NEW - EPIC-010) |
| **ideation-result-interpreter** | Format ideation results for user display | opus | <15K | After spec-driven-ideation completes, before result display (NEW) |
| **context-preservation-validator** | Validate brainstorm→epic→story context linkage | opus | <20K | At workflow transitions, detect context loss (NEW) |
| **anti-pattern-scanner** | Architecture violation detection across 6 categories | opus | <50K | QA Phase 2 for anti-pattern and security scanning (NEW) |
| **stakeholder-analyst** | Stakeholder discovery for brainstorming sessions | opus | <30K | brainstorming Phase 1 stakeholder analysis (NEW) |
| **coverage-analyzer** | Test coverage analysis by architectural layer | opus | <40K | QA deep validation, 95%/85%/80% threshold enforcement (NEW) |
| **code-quality-auditor** | Code quality metrics (complexity, duplication, MI) | opus | <40K | QA deep validation, quality threshold enforcement (NEW) |

---

### agent-generator v2.0 Enhancement (2025-11-15)

The **agent-generator** subagent has been significantly enhanced to be DevForgeAI framework-aware and Claude Code best practice compliant:

**New Capabilities:**
- **Phase 0: Framework Reference Loading** - Automatically loads spec-driven-cc-guide skill, CLAUDE.md, and lean-orchestration-pattern.md
- **Enhanced System Prompt Generation** - Uses Claude Code official patterns + DevForgeAI context for comprehensive subagent creation
- **Framework Compliance Validation** - 12-point validation (6 DevForgeAI + 6 Claude Code checks) with auto-fix logic
- **Reference File Generation** - Automatically creates framework guardrail files for command-related, domain-specific, and decision-making subagents

**Key Features:**
- **Claude Code Integration:** Leverages spec-driven-cc-guide skill for official subagent patterns
- **DevForgeAI Awareness:** References context files, quality gates, workflow states
- **Lean Orchestration Compliance:** Follows protocol for command refactoring subagents
- **Auto-Fix Logic:** Suggests and applies corrections for validation failures
- **Reference File Templates:** 4 types (command-refactoring, domain-constraints, decision-guidance, custom)

**Generated Subagents Now Include:**
- Framework Integration section (context files, quality gates, skill coordination)
- Tool Usage Protocol section (native tools mandate with 40-73% savings rationale)
- Enhanced token efficiency strategies
- Structured output contracts (for result-returning subagents)
- Framework constraint awareness

**Backward Compatibility:** ✅ Phase 2 requirements workflow unchanged

**File Size:** 2,343 lines (was 855 lines - 174% growth for comprehensive framework awareness)

**See:** `devforgeai/specs/enhancements/AGENT-GENERATOR-FRAMEWORK-AWARENESS-UPDATES.md` for complete enhancement details

---

## Subagent Integration with Skills

**spec-driven-dev** uses:
- **git-worktree-manager** (Phase 0 Step 0.2) - Creates isolated worktree for story development
- **dependency-graph-analyzer** (Phase 0 Step 0.2.5) - Validates story dependencies
- **file-overlap-detector** (Phase 0 Step 0.2.6) - Detects file conflicts with parallel stories
- **git-validator** (Phase 01 Step 1) - Enhanced with RCA-008 file categorization (story_files, code, cache) and user consent recommendations
- **tech-stack-detector** (Phase 0 Step 7)
- test-automator → backend-architect/frontend-developer → context-validator → refactoring-specialist + code-reviewer → integration-tester → **deferral-validator** (Phase 5 Step 1.5)
- **ac-compliance-verifier** (Phase 4.5 and 5.5) - Fresh-context AC verification (EPIC-046)
- **observation-extractor** (Phase 9) - Extract observations from subagent outputs
- **framework-analyst** (Phase 9) - Synthesize observations into recommendations
- **dev-result-interpreter** (Phase 10) - Format results for user display
- requirements-analyst (when creating follow-up stories for deferrals)
- architect-reviewer (when creating ADRs for scope changes)

**spec-driven-qa** uses:
- **deferral-validator** (Phase 0 Step 2.5 - validates deferred DoD items)
- context-validator → security-auditor → test-automator (coverage gaps)
- **anti-pattern-scanner** (Phase 2 - architecture violation detection)
- **coverage-analyzer** (Phase 2 - test coverage by architectural layer)
- **code-quality-auditor** (Phase 2 - complexity, duplication, maintainability)
- **qa-result-interpreter** (Phase 5 Step 6 - interprets results and generates display)

**spec-driven-ui** uses:
- **ui-spec-formatter** (NEW - Phase 6 Step 3.5 - formats and validates UI spec results)

**spec-driven-architecture** uses:
- architect-reviewer → api-designer

**spec-driven-release** uses:
- security-auditor → deployment-engineer

**devforgeai-orchestration** uses:
- requirements-analyst (epic feature decomposition, sprint planning)
- **technical-debt-analyzer** (NEW - Phase 4.5 during sprint planning/retrospectives)
- **sprint-planner** (NEW - Phase 3 sprint planning workflow)

**spec-driven-stories** uses:
- **story-requirements-analyst** (Phase 2 - Requirements Analysis, RCA-007)
  - Skill-specific subagent for content-only output
  - Replaces general-purpose requirements-analyst
  - Cannot create files (no Write/Edit tools)
  - Returns markdown sections for assembly into story-template.md
- api-designer (conditional - Phase 3 if API endpoints detected)
- **context-preservation-validator** (Phase 7 - validates provenance chain)

**brainstorming** uses:
- **stakeholder-analyst** (Phase 1 - stakeholder discovery and mapping)
- **internet-sleuth** (Phase 3 - market research and competitive analysis)

**spec-driven-ideation** uses:
- **internet-sleuth** (Phase 2 - technology discovery and repository archaeology)
- **ideation-result-interpreter** (Phase 6.5 - format results for display)

**devforgeai-insights** uses:
- **session-miner** (all query types - parse history.jsonl for workflow insights)

---

## Autonomous Subagent Usage

**When to autonomously invoke subagents:**

1. **Context Validation**: Always use `context-validator` before git commits or after implementation
2. **Test Generation**: Use `test-automator` when implementing features (TDD Red phase)
3. **Code Review**: Use `code-reviewer` after implementation or refactoring
4. **Security Audits**: Use `security-auditor` after auth/security code or handling sensitive data
5. **Documentation**: Use `documentation-writer` after API implementation or when coverage <80%
6. **Architecture Review**: Use `architect-reviewer` after creating ADRs or major design changes
7. **Deferral Validation** (RCA-006): Always use `deferral-validator` when stories have deferred DoD items (dev Phase 6.1.5, QA Phase 0 Step 2.5)
8. **Technical Debt Analysis** (RCA-006): Use `technical-debt-analyzer` during sprint planning or when technical-debt-register.md updates
9. **QA Result Interpretation**: Always use `qa-result-interpreter` after QA report generation to prepare user-facing display
10. **UI Spec Formatting**: Always use `ui-spec-formatter` after UI spec generation to validate and format results
11. **AC Compliance Verification** (EPIC-046): Use `ac-compliance-verifier` in Phase 4.5/5.5 for fresh-context AC verification
12. **Dependency Validation** (EPIC-010): Use `dependency-graph-analyzer` when validating story dependencies before development
13. **File Overlap Detection** (EPIC-010): Use `file-overlap-detector` when checking for conflicts with parallel stories
14. **Session Mining** (EPIC-034): Use `session-miner` when analyzing command history and workflow patterns
15. **Stakeholder Analysis**: Use `stakeholder-analyst` during brainstorming Phase 1 for stakeholder discovery

---

## Subagent Context Isolation

- Each subagent operates in a separate context window
- Main conversation context is preserved (token efficiency)
- Subagents return results that integrate into main workflow
- No context leakage between parallel subagents

---

## Token Efficiency with Subagents

- Subagent work happens in isolated contexts
- Main conversation only pays invocation cost (~5-10K) + summary
- Total workflow can exceed 200K tokens across subagents without affecting main context
- **Example:** Full dev cycle (test-automator 50K + backend-architect 50K + code-reviewer 30K + integration-tester 40K = 170K) appears as ~15K in main conversation

---

## Subagent Best Practices

1. **Use specific, detailed prompts**: Subagents work best with clear instructions
2. **Reference context files**: Subagents respect tech-stack, source-tree, dependencies, etc.
3. **Specify success criteria**: Define what "done" looks like in the prompt
4. **Leverage parallelism**: Run independent subagents simultaneously for speed
5. **Check validation results**: context-validator blocks on violations, fix before proceeding
6. **Trust specialized expertise**: Subagents are domain experts (security, testing, architecture)

---

## Subagent File Locations

All subagents are defined in `.claude/agents/`:
- `test-automator.md` (546 lines)
- `backend-architect.md` (728 lines)
- `frontend-developer.md` (629 lines)
- `integration-tester.md` (502 lines)
- `context-validator.md` (356 lines)
- `code-reviewer.md` (enhanced with deferral review - Section 7)
- `security-auditor.md` (550 lines)
- `refactoring-specialist.md` (471 lines)
- `requirements-analyst.md` (473 lines)
- `architect-reviewer.md` (528 lines)
- `api-designer.md` (754 lines)
- `deployment-engineer.md` (820 lines)
- `documentation-writer.md` (519 lines)
- `agent-generator.md` (2,343 lines - ENHANCED 2025-11-15: Framework-aware v2.0)
- **`deferral-validator.md`** (NEW - 181 lines - RCA-006)
- **`technical-debt-analyzer.md`** (NEW - 172 lines - RCA-006)
- **`story-requirements-analyst.md`** (NEW - ~500 lines - RCA-007 Phase 3)

- **`tech-stack-detector.md`** (NEW - ~300 lines - Command Refactoring)
- **`git-validator.md`** (NEW - ~250 lines - Command Refactoring)
- **`qa-result-interpreter.md`** (NEW - 300 lines - QA Command Refactoring 2025-11-05)
- **`ui-spec-formatter.md`** (NEW - 507 lines - UI Command Refactoring 2025-11-05)

- **`internet-sleuth.md`** (AUTO-INVOKED by ideation for research)
- **`pattern-compliance-auditor.md`** (Used by /audit-budget)
- **`dev-result-interpreter.md`** (Used by /dev command)

**NEW - EPIC-010 Parallel Development:**
- **`git-worktree-manager.md`** (Phase 0 Step 0.2 worktree lifecycle)
- **`dependency-graph-analyzer.md`** (Phase 0 Step 0.2.5 dependency validation)
- **`file-overlap-detector.md`** (Phase 0 Step 0.2.6 conflict detection)

**NEW - EPIC-046 AC Verification:**
- **`ac-compliance-verifier.md`** (Phase 4.5/5.5 fresh-context verification)

**NEW - EPIC-034 Session Mining:**
- **`session-miner.md`** (history.jsonl parsing and workflow insights)

**NEW - Framework Self-Improvement:**
- **`observation-extractor.md`** (STORY-319 - extract observations from subagent outputs)
- **`framework-analyst.md`** (Phase 09 - synthesize recommendations)

**NEW - Workflow Interpretation:**
- **`ideation-result-interpreter.md`** (format ideation results for display)
- **`context-preservation-validator.md`** (validate provenance chains)

**NEW - QA Deep Validation:**
- **`anti-pattern-scanner.md`** (architecture violation detection)
- **`coverage-analyzer.md`** (test coverage by architectural layer)
- **`code-quality-auditor.md`** (complexity, duplication, maintainability)

**NEW - Brainstorming:**
- **`stakeholder-analyst.md`** (Phase 1 stakeholder discovery)

**NEW - Dead Code & Diagnostics:**
- **`dead-code-detector.md`** (ADR-016 read-only call-graph analysis. Source: `.claude/agents/dead-code-detector.md`)
- **`diagnostic-analyst.md`** (spec-driven-rca skill investigation. Source: `.claude/agents/diagnostic-analyst.md`)

**NEW - Profile Assessment & Coverage Interpretation:**
- **`entrepreneur-assessor.md`** (assessing-entrepreneur skill. Source: `.claude/agents/entrepreneur-assessor.md`)
- **`epic-coverage-result-interpreter.md`** (validating-epic-coverage skill. Source: `.claude/agents/epic-coverage-result-interpreter.md`)

**Total:** 44 subagents

Each file contains complete system prompts with tool access, model selection, and execution patterns.

### Proactive Trigger Mapping

| Trigger Pattern | Recommended Agent |
|-----------------|-------------------|
| after /create-context Phase 5 completes | alignment-auditor |
| after ADR acceptance | alignment-auditor |
| when /audit-alignment command invoked | alignment-auditor |
| after code implementation | code-reviewer |
| during TDD Red phase | test-automator |
| when mining session data | session-miner |

</subagents_catalog>
