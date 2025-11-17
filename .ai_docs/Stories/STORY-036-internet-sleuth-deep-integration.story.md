---
id: STORY-036
title: Internet-Sleuth Deep Integration (Phase 2 Migration)
epic: EPIC-007
sprint: Backlog
status: Backlog
points: 13
priority: High
assigned_to: Unassigned
created: 2025-11-14
updated: 2025-11-14
format_version: "2.0"
---

# Story: Internet-Sleuth Deep Integration (Phase 2 Migration)

## Description

**As a** DevForgeAI framework maintainer,
**I want** the internet-sleuth agent to be deeply integrated with framework skills and workflows,
**so that** evidence-based research capabilities are available throughout the development lifecycle with full framework compliance and traceability.

## Acceptance Criteria

### 1. [ ] Research Methodology Reference Files (Progressive Disclosure)

**Given** the internet-sleuth agent has complex research methodologies
**When** the agent is invoked for research tasks
**Then** the agent loads methodology reference files progressively (discovery-mode-methodology.md, investigation-mode-methodology.md, repository-archaeology-guide.md, competitive-analysis-patterns.md) only when needed for specific research types
**And** total token usage stays <50K per research operation through progressive loading
**And** reference files follow DevForgeAI pattern (200-600 lines each, framework-aware, explicit constraints)

---

### 2. [ ] Integration with devforgeai-ideation Skill (Phase 5 Feasibility Analysis)

**Given** devforgeai-ideation skill reaches Phase 5 (Feasibility & Constraints Analysis)
**When** feasibility analysis requires market research or technology evaluation
**Then** the skill invokes internet-sleuth agent with Task tool
**And** internet-sleuth returns structured research report with feasibility findings (technical feasibility score 0-10, market viability evidence, competitive landscape, risk factors)
**And** ideation skill incorporates research findings into feasibility assessment
**And** research report is saved to `.devforgeai/research/feasibility/{EPIC-ID}-{timestamp}-research.md`
**And** research findings validate against context files (no unapproved technologies recommended)

---

### 3. [ ] Integration with devforgeai-architecture Skill (Phase 2 Technology Selection)

**Given** devforgeai-architecture skill reaches Phase 2 (Create Immutable Context Files - Technology Selection)
**When** technology decisions require evaluation of multiple options
**Then** the skill invokes internet-sleuth agent for comparative technology research
**And** internet-sleuth returns comparison matrix with framework-compliant recommendations (respects tech-stack.md constraints, provides ADR-ready evidence)
**And** architecture skill uses research to inform tech-stack.md creation or validation
**And** research report includes repository archaeology findings (real implementation patterns from GitHub)
**And** technology recommendations include version compatibility, community health metrics, and security audit status

---

### 4. [ ] Workflow State Awareness

**Given** internet-sleuth is invoked in context of a story, epic, or sprint
**When** research is conducted
**Then** the agent detects workflow state from conversation context (Backlog, Architecture, Ready for Dev, In Development, Dev Complete, QA In Progress, QA Approved, Releasing, Released)
**And** research output is tagged with workflow state metadata
**And** research recommendations adapt to workflow state (e.g., Architecture state = technology evaluation focus, In Development state = implementation pattern research)
**And** research reports include workflow state in YAML frontmatter
**And** stale research is flagged if workflow state changed since research completion

---

### 5. [ ] Quality Gate Integration

**Given** internet-sleuth generates research reports with technology recommendations
**When** research is completed
**Then** the agent validates recommendations against all 6 context files (tech-stack.md, source-tree.md, dependencies.md, coding-standards.md, architecture-constraints.md, anti-patterns.md)
**And** violations are flagged with severity (CRITICAL = contradicts locked tech, HIGH = violates architecture constraint, MEDIUM = conflicts with coding standard, LOW = informational)
**And** research report includes compliance section documenting validation results
**And** CRITICAL violations require AskUserQuestion before proceeding (update context files or adjust recommendation)
**And** quality gate validation uses context-validator subagent for consistency

---

### 6. [ ] Example Research Reports Demonstrating Integration

**Given** internet-sleuth is integrated with framework skills
**When** example research scenarios are documented
**Then** 3 example research reports exist in `.devforgeai/research/examples/`:
  - `technology-evaluation-example.md` (comparative analysis with ADR-ready evidence)
  - `competitive-analysis-example.md` (market research with feasibility implications)
  - `repository-archaeology-example.md` (implementation pattern mining with code examples)
**And** each example demonstrates workflow state tagging, quality gate validation, and skill integration patterns
**And** examples include both compliant scenarios (recommendations match context files) and violation scenarios (how conflicts are handled)

---

### 7. [ ] Skill Coordination Patterns Documentation

**Given** internet-sleuth integrates with multiple DevForgeAI skills
**When** developers need to invoke internet-sleuth from skills
**Then** skill coordination patterns are documented in `.claude/skills/internet-sleuth-integration/references/skill-coordination-patterns.md` (400-500 lines)
**And** patterns include Task tool invocation syntax, result parsing examples, error handling procedures
**And** patterns show both synchronous research (block until complete) and asynchronous research (research in background, check results later)
**And** coordination guide includes token budget management (research in isolated context doesn't bloat main conversation)

---

### 8. [ ] Progressive Disclosure for Research Methodologies

**Given** internet-sleuth has 5 research modes (discovery, investigation, competitive-analysis, repository-archaeology, market-intelligence)
**When** a specific research mode is invoked
**Then** only the methodology reference file for that mode is loaded (e.g., *repository-archaeology loads repository-archaeology-guide.md only)
**And** common research principles are in shared base file (research-principles.md, ~300 lines)
**And** mode-specific methodologies are in separate files (discovery-mode-methodology.md, investigation-mode-methodology.md, etc., ~400-600 lines each)
**And** agent loads base + specific methodology (total ~700-900 lines per research operation, not all 2500+ lines)

---

### 9. [ ] Research Report Templates with Framework Integration

**Given** internet-sleuth generates structured research reports
**When** research is completed for any mode
**Then** report follows standardized template in `.claude/skills/internet-sleuth-integration/assets/research-report-template.md`
**And** template includes sections: Executive Summary, Research Scope, Methodology Used, Findings (with evidence URLs), Framework Compliance Check, Workflow State, Recommendations (prioritized), Risk Assessment, ADR Readiness (if applicable)
**And** template YAML frontmatter includes: research_id, epic_id/story_id (if applicable), workflow_state, research_mode, timestamp, quality_gate_status
**And** all generated reports validate against template (completeness check)

---

## Technical Specification

```yaml
technical_specification:
  format_version: "2.0"

  components:
    - type: "Service"
      name: "ResearchMethodologyLoader"
      file_path: ".claude/agents/internet-sleuth.md"
      requirements:
        - id: "COMP-001"
          description: "Implement progressive disclosure pattern to load methodology reference files based on research mode (discovery, investigation, competitive-analysis, repository-archaeology, market-intelligence)"
          testable: true
          test_requirement: "Test: Invoke *repository-archaeology, verify only repository-archaeology-guide.md + research-principles.md loaded (~700 lines), not all 2500+ lines"
          priority: "High"

        - id: "COMP-002"
          description: "Load research-principles.md (300 lines, shared base) for all research operations"
          testable: true
          test_requirement: "Test: All research modes load research-principles.md on invocation, verified via Read tool call"
          priority: "High"

    - type: "Configuration"
      name: "IdeationSkillIntegration"
      file_path: ".claude/skills/devforgeai-ideation/SKILL.md"
      requirements:
        - id: "COMP-003"
          description: "Add internet-sleuth invocation to Phase 5 (Feasibility Analysis) workflow with Task tool syntax"
          testable: true
          test_requirement: "Test: Parse devforgeai-ideation SKILL.md Phase 5, assert contains 'Task(subagent_type=\"internet-sleuth\"' invocation pattern"
          priority: "Critical"

        - id: "COMP-004"
          description: "Document research result parsing (extract technical_feasibility_score, market_viability, competitive_landscape from JSON)"
          testable: true
          test_requirement: "Test: Phase 5 workflow includes code example showing JSON field extraction from research report"
          priority: "High"

    - type: "Configuration"
      name: "ArchitectureSkillIntegration"
      file_path: ".claude/skills/devforgeai-architecture/SKILL.md"
      requirements:
        - id: "COMP-005"
          description: "Add internet-sleuth invocation to Phase 2 (Technology Selection) for comparative technology analysis"
          testable: true
          test_requirement: "Test: Parse devforgeai-architecture SKILL.md Phase 2, assert contains internet-sleuth invocation for tech evaluation"
          priority: "Critical"

        - id: "COMP-006"
          description: "Document repository archaeology findings integration into ADR Alternatives Considered section"
          testable: true
          test_requirement: "Test: Phase 3 (ADR creation) includes example citing repository archaeology evidence with GitHub URLs"
          priority: "High"

    - type: "Service"
      name: "WorkflowStateAwarenessModule"
      file_path: ".claude/agents/internet-sleuth.md"
      requirements:
        - id: "COMP-007"
          description: "Detect workflow state from conversation context (Backlog, Architecture, Ready for Dev, In Development, Dev Complete, QA In Progress, QA Approved, Releasing, Released)"
          testable: true
          test_requirement: "Test: Provide conversation with '**Workflow State:** Architecture' marker, invoke agent, assert research report YAML includes workflow_state: Architecture"
          priority: "High"

        - id: "COMP-008"
          description: "Implement stale research detection (>30 days or 2+ workflow states behind current story/epic state)"
          testable: true
          test_requirement: "Test: Load report from Backlog state (31 days old), current state In Development, assert report flagged STALE with re-research recommendation"
          priority: "Medium"

    - type: "Service"
      name: "QualityGateValidation"
      file_path: ".claude/agents/internet-sleuth.md"
      requirements:
        - id: "COMP-009"
          description: "Invoke context-validator subagent to validate research recommendations against all 6 context files"
          testable: true
          test_requirement: "Test: Research recommends Vue.js when tech-stack.md specifies React, assert CRITICAL violation triggered with AskUserQuestion"
          priority: "Critical"

        - id: "COMP-010"
          description: "Categorize violations by severity (CRITICAL = contradicts locked tech, HIGH = violates architecture, MEDIUM = coding standard conflict, LOW = informational)"
          testable: true
          test_requirement: "Test: Research violates coding-standards.md (naming convention), assert categorized as MEDIUM with WARN quality_gate_status"
          priority: "High"

    - type: "Configuration"
      name: "ReferenceFileCreation"
      file_path: ".claude/skills/internet-sleuth-integration/references/"
      requirements:
        - id: "COMP-011"
          description: "Create research-principles.md (300 lines, shared base with Purpose, Core Principles, Framework Integration, Evidence Standards sections)"
          testable: true
          test_requirement: "Test: File exists, contains all 5 required sections, line count 280-320"
          priority: "High"

        - id: "COMP-012"
          description: "Create discovery-mode-methodology.md (400 lines, discovery workflow steps + ideation integration)"
          testable: true
          test_requirement: "Test: File exists, documents discovery mode, integration with ideation skill, line count 380-420"
          priority: "High"

        - id: "COMP-013"
          description: "Create repository-archaeology-guide.md (600 lines, GitHub mining strategies + pattern extraction + quality assessment)"
          testable: true
          test_requirement: "Test: File exists, includes GitHub search strategies, code pattern extraction examples, quality scoring rubric, line count 580-620"
          priority: "High"

        - id: "COMP-014"
          description: "Create skill-coordination-patterns.md (450 lines, Task tool syntax + result parsing + error handling + token management)"
          testable: true
          test_requirement: "Test: File exists, contains Task tool examples, result parsing code, error handling patterns, line count 430-470"
          priority: "Critical"

        - id: "COMP-015"
          description: "Create competitive-analysis-patterns.md (500 lines, competitive landscape research + SWOT + market positioning)"
          testable: true
          test_requirement: "Test: File exists, documents competitive analysis methodology, SWOT template, market matrix, line count 480-520"
          priority: "Medium"

    - type: "Configuration"
      name: "ResearchReportTemplate"
      file_path: ".claude/skills/internet-sleuth-integration/assets/research-report-template.md"
      requirements:
        - id: "COMP-016"
          description: "Define YAML frontmatter schema (research_id, epic_id/story_id, workflow_state, research_mode, timestamp, quality_gate_status, version)"
          testable: true
          test_requirement: "Test: Template file contains YAML block with all 7 required fields as examples"
          priority: "Critical"

        - id: "COMP-017"
          description: "Define 9 standard sections (Executive Summary, Research Scope, Methodology, Findings, Compliance, Workflow State, Recommendations, Risks, ADR Readiness)"
          testable: true
          test_requirement: "Test: Template contains ## headings for all 9 sections with placeholder content"
          priority: "High"

    - type: "Configuration"
      name: "ResearchDirectoryStructure"
      file_path: ".devforgeai/research/"
      requirements:
        - id: "COMP-018"
          description: "Create directory structure: research/{feasibility, examples, shared, cache, logs}/"
          testable: true
          test_requirement: "Test: mkdir -p .devforgeai/research/{feasibility,examples,shared,cache,logs} succeeds, .gitkeep files added to prevent empty directory issues"
          priority: "High"

        - id: "COMP-019"
          description: "Create README.md documenting directory purposes, file naming conventions, archival policy"
          testable: true
          test_requirement: "Test: README exists at .devforgeai/research/README.md, contains directory explanations, naming pattern (RESEARCH-001), archival guidance (6 months)"
          priority: "Low"

    - type: "Configuration"
      name: "ExampleResearchReports"
      file_path: ".devforgeai/research/examples/"
      requirements:
        - id: "COMP-020"
          description: "Create technology-evaluation-example.md demonstrating comparative analysis with ADR-ready evidence"
          testable: true
          test_requirement: "Test: File exists, follows research-report-template.md structure, includes comparison matrix, ADR-ready citations"
          priority: "Medium"

        - id: "COMP-021"
          description: "Create competitive-analysis-example.md demonstrating market research with feasibility implications"
          testable: true
          test_requirement: "Test: File exists, includes SWOT analysis, competitive matrix, feasibility scores (0-10 scale)"
          priority: "Medium"

        - id: "COMP-022"
          description: "Create repository-archaeology-example.md demonstrating implementation pattern mining with code examples"
          testable: true
          test_requirement: "Test: File exists, includes GitHub URLs, code snippets, pattern synthesis, quality assessment"
          priority: "Medium"

  business_rules:
    - id: "BR-001"
      rule: "All research recommendations must validate against 6 context files before returning. CRITICAL violations (contradicts tech-stack.md) require AskUserQuestion before proceeding."
      test_requirement: "Test: Research recommends GraphQL when tech-stack.md specifies REST, assert CRITICAL violation triggers AskUserQuestion with 2 options (update tech-stack + ADR, adjust scope)"

    - id: "BR-002"
      rule: "Progressive disclosure loads only research-principles.md (300 lines) + mode-specific methodology (400-600 lines) = max 900 lines per operation, not all 2500+ lines"
      test_requirement: "Test: Invoke *competitive-analysis, measure loaded content via Read tool calls, assert total <1000 lines loaded"

    - id: "BR-003"
      rule: "Stale research detection: Reports >30 days old or 2+ workflow states behind current epic/story state flagged as STALE with re-research recommendation"
      test_requirement: "Test: Report dated 2025-10-01 with workflow_state: Backlog, current date 2025-11-14 (44 days) and story state In Development (2 states ahead), assert flagged STALE"

    - id: "BR-004"
      rule: "Research ID assignment is gap-aware: Glob finds existing IDs, fills gaps before incrementing (RESEARCH-001, RESEARCH-003 exist → next is RESEARCH-002)"
      test_requirement: "Test: Mock existing RESEARCH-001, RESEARCH-003, invoke agent, assert next ID assigned is RESEARCH-002 (gap filled)"

    - id: "BR-005"
      rule: "Research reports linked to epic_id/story_id must validate file existence in .ai_docs/Epics/ or .ai_docs/Stories/. Broken references trigger validation error."
      test_requirement: "Test: Research YAML includes epic_id: EPIC-999 (doesn't exist), assert validation fails with 'Epic file not found: .ai_docs/Epics/EPIC-999.epic.md'"

  non_functional_requirements:
    - id: "NFR-001"
      category: "Performance"
      requirement: "Research operations complete within defined time limits by mode"
      metric: "Discovery: <5min (p95), Investigation: <15min (p95), Repository archaeology: <10min (p95)"
      test_requirement: "Test: Run 10 discovery mode operations, measure duration, assert p95 < 300 seconds"

    - id: "NFR-002"
      category: "Performance"
      requirement: "Progressive disclosure overhead minimal"
      metric: "< 500ms to load methodology reference file (cached after first load)"
      test_requirement: "Test: Measure time between research mode selection and methodology file load, assert <500ms; second invocation <100ms (cached)"

    - id: "NFR-003"
      category: "Performance"
      requirement: "Quality gate validation fast"
      metric: "< 2 seconds to validate against all 6 context files"
      test_requirement: "Test: Invoke context-validator with 6 context files, measure time, assert <2000ms"

    - id: "NFR-004"
      category: "Security"
      requirement: "API key from environment variable only"
      metric: "Zero hardcoded API keys"
      test_requirement: "Test: Grep internet-sleuth.md for 'PERPLEXITY_API_KEY = \"sk-', assert zero matches; verify uses os.environ['PERPLEXITY_API_KEY']"

    - id: "NFR-005"
      category: "Security"
      requirement: "Research output sanitization (HTTPS URLs only, no directory traversal)"
      metric: "100% URL validation, 100% path sanitization"
      test_requirement: "Test: Research includes http://example.com URL, assert converted to https:// or flagged; test path ../../../etc/passwd rejected"

    - id: "NFR-006"
      category: "Reliability"
      requirement: "Perplexity API failures retried with exponential backoff"
      metric: "Max 3 retries with 1s, 2s, 4s delays"
      test_requirement: "Test: Mock Perplexity API to return 503, measure retry delays, assert 3 retries at 1s, 2s, 4s intervals"

    - id: "NFR-007"
      category: "Reliability"
      requirement: "Partial result recovery (research resumable from cache)"
      metric: "100% partial result preservation on failure"
      test_requirement: "Test: Simulate research failure after completing 2 of 5 sections, verify cache file contains 2 sections, resume loads from cache"

    - id: "NFR-008"
      category: "Scalability"
      requirement: "Support concurrent research operations"
      metric: "5 simultaneous research tasks (isolated Task contexts)"
      test_requirement: "Test: Launch 5 parallel Task invocations (internet-sleuth), verify all complete without interference, results correctly tagged"

    - id: "NFR-009"
      category: "Maintainability"
      requirement: "All reference files follow consistent structure"
      metric: "100% reference files include Purpose, When to Use, Workflow Steps, Framework Constraints, Success Criteria sections"
      test_requirement: "Test: Parse all 5 methodology files, assert each contains all 5 required sections"
```

---

## Edge Cases

### 1. Research during brownfield architecture analysis
**Scenario:** devforgeai-architecture invoked in brownfield mode (existing project with established tech stack)

**Expected Behavior:** internet-sleuth must respect existing tech-stack.md and only recommend compatible technologies or provide migration path evidence. If existing tech stack is outdated/deprecated, research report must flag this as CRITICAL with ADR requirement.

**Test:** Mock tech-stack.md with Angular v1.x (deprecated), invoke research for modern framework, assert report flags Angular v1.x as DEPRECATED and recommends migration with migration path evidence

---

### 2. Conflicting research findings vs. context files
**Scenario:** internet-sleuth research recommends technology X but tech-stack.md specifies technology Y

**Expected Behavior:** Agent must invoke AskUserQuestion with options: (a) Update tech-stack.md with ADR, (b) Adjust research scope to evaluate Y instead, (c) Document as technical debt. Never autonomously override context files.

**Test:** Research recommends PostgreSQL when tech-stack.md specifies MySQL, assert AskUserQuestion triggered with 3 options and CRITICAL violation logged

---

### 3. Stale research reports
**Scenario:** Research completed during Backlog state may become irrelevant if story moves to In Development

**Expected Behavior:** Research completed during Backlog state may become irrelevant if story moves to In Development (implementation patterns more critical than feasibility). Agent must detect workflow state changes via YAML frontmatter comparison and flag reports >30 days old or 2+ workflow states behind as "STALE - Re-research Recommended."

**Test:** Report dated 2025-10-01 with workflow_state: Backlog, current story state In Development (2 states ahead), assert flagged STALE with re-research recommendation

---

### 4. Repository archaeology with no results
**Scenario:** internet-sleuth searches GitHub for implementation patterns but finds zero matching repositories (obscure tech stack, new framework)

**Expected Behavior:** Gracefully degrade to general documentation research and flag "LIMITED EVIDENCE - Recommendation based on official docs only, not real-world implementations."

**Test:** Search for nonexistent framework "QuantumWebJS", assert zero repositories found, research report includes LIMITED EVIDENCE flag and documentation-only sources

---

### 5. Rate limiting during deep research
**Scenario:** internet-sleuth hits Perplexity API rate limits mid-research

**Expected Behavior:** Cache partial results in `.devforgeai/research/cache/{research_id}-partial.json` and resume from checkpoint on retry, not restart from scratch.

**Test:** Mock Perplexity API to return 429 rate limit after 2 of 5 sections completed, verify cache file created with 2 sections, retry resumes from section 3

---

### 6. Multi-epic research scope
**Scenario:** Research is relevant to multiple epics (e.g., "evaluate GraphQL for all API development")

**Expected Behavior:** Research report must be stored in `.devforgeai/research/shared/` and linked from all relevant epic/story files via YAML frontmatter reference (research_references: [RESEARCH-001]).

**Test:** Research spans EPIC-001 and EPIC-002, assert stored in shared/, both epic files include research_references: [RESEARCH-001] in frontmatter

---

### 7. Conflicting recommendations across research modes
**Scenario:** *competitive-analysis recommends Feature A but *repository-archaeology finds Feature A has poor community implementation examples

**Expected Behavior:** Final research report must synthesize findings with priority ranking and trade-off analysis, not present contradictory conclusions.

**Test:** Competitive analysis scores Feature A 9/10 (market demand), repository archaeology scores 3/10 (implementation quality), assert synthesis section explains trade-off with recommendation priority

---

## Non-Functional Requirements (NFRs)

### Performance

**Research Operation Completion Times:**
- **Discovery mode:** < 5 minutes (p95)
- **Investigation mode:** < 15 minutes (p95)
- **Repository archaeology:** < 10 minutes (p95)
- **Competitive analysis:** < 8 minutes (p95)
- **Market intelligence:** < 12 minutes (p95)

**Progressive Disclosure Overhead:**
- **Methodology file load:** < 500ms (first load), < 100ms (cached)
- **Quality gate validation:** < 2 seconds (all 6 context files)
- **Research report generation:** < 30 seconds (template population + disk write)
- **Stale research detection:** < 1 second (YAML frontmatter comparison)

**Performance Test:**
- Load test: 10 concurrent research operations
- Verify: p95 completion times within limits
- Verify: No memory leaks over 2-hour run

---

### Security

**API Key Management:**
- **Perplexity API key:** Environment variable PERPLEXITY_API_KEY only (never hardcoded)
- **GitHub token:** Environment variable GITHUB_TOKEN or gh CLI credentials

**Research Output Sanitization:**
- **URL validation:** All URLs must be HTTPS (no HTTP) or flagged
- **Path sanitization:** Prevent directory traversal attacks (../../../etc/passwd rejected)
- **Context file access:** Read-only access to .devforgeai/context/*.md (no modifications without user approval)
- **Sensitive data handling:** No PII or credentials stored in research reports (flagged and redacted if detected in findings)

**Security Testing:**
- [ ] No hardcoded API keys or tokens
- [ ] Environment variable usage verified
- [ ] URL validation enforced (HTTPS only)
- [ ] Path sanitization tested (directory traversal attempts blocked)
- [ ] Sensitive data redaction verified

---

### Reliability

**Error Handling:**
- **Perplexity API failures:** Max 3 retries with exponential backoff (1s, 2s, 4s delays)
- **Partial result recovery:** Cache partial results in `.devforgeai/research/cache/`, resume from checkpoint on retry
- **Validation failures:** Quality gate validation failures do not crash agent, return structured error with remediation steps
- **Graceful degradation:** If repository archaeology finds no results, fall back to documentation research with DEGRADED flag

**Retry Logic:**
- **Max retries:** 3 attempts
- **Backoff strategy:** Exponential (1s, 2s, 4s)
- **Retry conditions:** Retry on: rate limits (429), network timeouts (504, 503); Do not retry on: 404 (not found), 403 (forbidden)

**Monitoring:**
- **Log all research operations:** .devforgeai/research/logs/{YYYY-MM-DD}-research.log (INFO level minimum)
- **Track completion rate:** % of research operations completing successfully
- **Track retry frequency:** Average retries per operation
- **Alert on:** Consistent Perplexity API failures (>50% retry rate), cache corruption (partial results unrecoverable)

---

### Scalability

**Concurrency:**
- **Concurrent research operations:** Support 5 simultaneous research tasks (isolated Task contexts prevent interference)

**Research Report Storage:**
- **No hard limit:** File-based storage scales with disk space
- **Archival policy:** Move reports >6 months old to .devforgeai/research/archive/ (maintain .devforgeai/research/ performance)

**Methodology Reference Files:**
- **Scale to 10 research modes:** Progressive disclosure prevents token bloat (lazy loading)

**Context File Validation:**
- **Scales with project complexity:** Tested with tech-stack.md containing 50+ technologies, dependencies.md with 100+ packages

---

### Maintainability

**Reference File Structure:**
- **All methodology files follow consistent structure:** Purpose, When to Use, Workflow Steps, Framework Constraints, Success Criteria sections (5 required sections)

**Template Versioning:**
- **Research report template includes version field:** v2.0 for backward compatibility tracking
- **Template changes:** Version bump triggers migration guide creation

**Logging:**
- **All research operations logged:** Timestamp, research_mode, epic_id/story_id, duration, outcome (success/failure/retry)
- **Log retention:** 30 days in active logs/, archive to logs/archive/ monthly

**Self-Documentation:**
- **All skill coordination patterns include inline examples:** Expected output formats, error handling examples
- **Reference files include usage examples:** Concrete scenarios demonstrating integration

---

## Dependencies

### Prerequisite Stories

- [x] **STORY-035:** Internet-Sleuth Framework Compliance (Phase 1)
  - **Why:** Phase 2 deep integration builds on Phase 1 framework compliance work
  - **Status:** Must complete before STORY-036 begins

---

### External Dependencies

- [ ] **Perplexity API Access:** Available
  - **Owner:** Perplexity AI
  - **Status:** Stable (requires API key)
  - **Impact if unavailable:** Research operations fail (no fallback)

- [ ] **GitHub API Access:** Available
  - **Owner:** GitHub
  - **Status:** Stable
  - **Impact if unavailable:** Repository archaeology degrades to documentation-only research

---

### Technology Dependencies

No new packages required. Builds on existing tools:
- Read tool (file analysis)
- Write tool (report generation)
- Bash tool (git clone for repository archaeology)
- Grep tool (pattern searching)
- Glob tool (file discovery)
- WebSearch tool (web research)
- WebFetch tool (URL fetching)
- Task tool (subagent invocation)

---

## Test Strategy

### Unit Tests

**Coverage Target:** 85%+ for integration logic

**Test Scenarios:**
1. **Progressive Disclosure:** Invoke each research mode, verify only relevant methodology files loaded
2. **Workflow State Detection:** Provide conversation with workflow state markers, verify detection accuracy
3. **Quality Gate Validation:** Mock context files with violations, verify severity categorization
4. **Stale Research Detection:** Mock reports with various ages/workflow states, verify staleness flagging
5. **Research ID Assignment:** Mock existing IDs with gaps, verify gap-filling logic

**Test Structure:**
```bash
# Test progressive disclosure
test_progressive_disclosure() {
  # Invoke *repository-archaeology
  # Verify Read calls: research-principles.md + repository-archaeology-guide.md only
  # Assert <1000 lines loaded
}

# Test quality gate validation
test_quality_gate_critical_violation() {
  # Mock tech-stack.md with React
  # Research recommends Vue.js
  # Assert CRITICAL violation triggered
  # Assert AskUserQuestion invoked with 2 options
}
```

---

### Integration Tests

**Coverage Target:** 80%+ for skill integration

**Test Scenarios:**
1. **devforgeai-ideation Integration:** Ideation skill invokes internet-sleuth for feasibility research, receives structured report, incorporates findings
2. **devforgeai-architecture Integration:** Architecture skill invokes for technology evaluation, receives comparison matrix, uses for tech-stack.md
3. **context-validator Coordination:** Quality gate validation delegates to context-validator, receives structured violation report
4. **Report Template Validation:** Generated reports validate against template schema, all required sections present

**Example Test:**
```bash
test_ideation_integration() {
  # Simulate devforgeai-ideation Phase 5
  # Invoke Task(subagent_type="internet-sleuth", prompt="Research React ecosystem feasibility")
  # Assert: research report generated in .devforgeai/research/feasibility/
  # Assert: report includes technical_feasibility_score (0-10)
  # Assert: report validates against context files
}
```

---

### E2E Tests (If Applicable)

**Coverage Target:** Critical integration paths only

**Test Scenarios:**
1. **Complete Ideation-to-Architecture Flow:** Ideation Phase 5 → internet-sleuth research → Architecture Phase 2 → tech-stack.md creation using research findings

---

## Definition of Done

### Implementation
- [ ] COMP-001: Progressive disclosure pattern implemented (mode-specific methodology loading)
- [ ] COMP-002: research-principles.md loaded for all research operations
- [ ] COMP-003: devforgeai-ideation Phase 5 updated with internet-sleuth invocation
- [ ] COMP-004: Research result parsing documented in ideation skill
- [ ] COMP-005: devforgeai-architecture Phase 2 updated with internet-sleuth invocation
- [ ] COMP-006: Repository archaeology findings integration in ADR creation documented
- [ ] COMP-007: Workflow state detection from conversation context
- [ ] COMP-008: Stale research detection (>30 days or 2+ states behind)
- [ ] COMP-009: Quality gate validation via context-validator subagent
- [ ] COMP-010: Violation severity categorization (CRITICAL/HIGH/MEDIUM/LOW)
- [ ] COMP-011: research-principles.md created (300 lines)
- [ ] COMP-012: discovery-mode-methodology.md created (400 lines)
- [ ] COMP-013: repository-archaeology-guide.md created (600 lines)
- [ ] COMP-014: skill-coordination-patterns.md created (450 lines)
- [ ] COMP-015: competitive-analysis-patterns.md created (500 lines)
- [ ] COMP-016: Research report template YAML frontmatter schema defined
- [ ] COMP-017: Research report template 9 standard sections defined
- [ ] COMP-018: .devforgeai/research/ directory structure created
- [ ] COMP-019: .devforgeai/research/README.md created
- [ ] COMP-020: technology-evaluation-example.md created
- [ ] COMP-021: competitive-analysis-example.md created
- [ ] COMP-022: repository-archaeology-example.md created

### Quality
- [ ] All 9 acceptance criteria have passing tests
- [ ] Edge cases covered (7 scenarios: brownfield, conflicts, stale reports, no results, rate limiting, multi-epic, conflicting recommendations)
- [ ] Business rules enforced (5 rules: quality gate validation, progressive disclosure, stale detection, ID assignment, broken references)
- [ ] NFRs met (Performance: <5min discovery, <500ms progressive loading; Security: no hardcoded API keys; Reliability: retry with backoff, partial recovery; Scalability: 5 concurrent operations)
- [ ] Code coverage >85% for integration logic

### Testing
- [ ] Unit tests for progressive disclosure
- [ ] Unit tests for workflow state detection
- [ ] Unit tests for quality gate validation
- [ ] Integration tests for ideation skill integration
- [ ] Integration tests for architecture skill integration
- [ ] E2E test: Complete ideation-to-architecture flow

### Documentation
- [ ] 5 methodology reference files created and documented
- [ ] Research report template documented
- [ ] Skill coordination patterns documented
- [ ] 3 example research reports created

---

## Workflow Status

- [ ] Architecture phase complete
- [ ] Development phase complete
- [ ] QA phase complete
- [ ] Released

## Notes

**Migration Context:**
This is Phase 2 of a hybrid migration approach for the internet-sleuth agent. It builds on Phase 1 (STORY-035) framework compliance work to add deep integration with DevForgeAI skills and workflows.

**Design Decisions:**
- **Progressive disclosure:** Prevents token bloat (700-900 lines vs 2500+ lines per operation)
- **Quality gate integration:** Validates all research recommendations against 6 context files before returning
- **Workflow state awareness:** Research recommendations adapt to current development phase
- **Skill coordination:** devforgeai-ideation and devforgeai-architecture invoke internet-sleuth via Task tool
- **Research report templates:** Standardized structure ensures consistency and framework compliance
- **Directory structure:** .devforgeai/research/ with subdirectories for organization (feasibility/, examples/, shared/, cache/, logs/)

**Related Stories:**
- STORY-035: Internet-Sleuth Framework Compliance (Phase 1) - Prerequisite

**Related ADRs:**
- Future ADR required if research methodology patterns change

**References:**
- Phase 1 agent: .claude/agents/internet-sleuth.md (after STORY-035 completion)
- devforgeai-ideation skill: .claude/skills/devforgeai-ideation/SKILL.md
- devforgeai-architecture skill: .claude/skills/devforgeai-architecture/SKILL.md
- Research report examples: .devforgeai/research/examples/

---

## Implementation Notes

**Status:** Ready for Development (Backlog)

This story is in Backlog status - not yet assigned for implementation.

## Workflow Status

- [ ] Architecture phase complete
- [ ] Development phase complete
- [ ] QA phase complete
- [ ] Released

**Story Created:** 2025-11-14
**Story Template Version:** 2.0
