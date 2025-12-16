---
title: Meta-Agentic System Requirements Specification
project: DevForgeAI Meta-Agentic Enhancement
version: 1.0
created: 2025-12-16
complexity-score: 44/60
architecture-tier: Tier 3 (Complex Platform)
---

# Meta-Agentic System Requirements Specification

## Executive Summary

The Meta-Agentic System is a brownfield enhancement to the DevForgeAI Spec-Driven Framework that enables agents to accumulate expertise, learn from execution, and self-improve without human intervention. This transformation moves agents from "execute-and-forget" to "execute-and-learn" paradigm, solving the critical pain point of agents repeatedly re-learning codebases and requiring manual maintenance.

**Project Type:** Brownfield enhancement
**Complexity:** 44/60 (Tier 3 - Complex Platform)
**Timeline:** No fixed deadline (quality over speed)
**Resources:** User + Claude collaboration, existing DevForgeAI infrastructure

## Business Goals

1. **Enable Expertise Accumulation** - Agents automatically build and maintain mental models (expertise files) as they work
2. **Project-Specific Specialization** - Each DevForgeAI project develops unique domain experts tailored to its codebase
3. **Knowledge Updates Beyond LLM Cutoff** - Agents use internet-sleuth to research and update expertise with post-training-date knowledge
4. **Reduce Manual Maintenance** - Self-improving templates reduce engineering overhead by 80%

**Success Metrics:**
- 70% reduction in agent file searching (validate mental models instead)
- 50% improvement in agent accuracy when using expertise files
- 80% reduction in time to create domain experts (15min vs. 2hr manual)
- 95% of expertise updates happen autonomously (not manual commands)

## User Personas

**Primary Persona: DevForgeAI Framework User**
- Role: Software engineer using DevForgeAI for spec-driven development
- Needs: Efficient agents that learn project patterns, reduce repetitive searching
- Frustrations: Agents forget context, manual agent/skill/prompt maintenance overhead
- Goals: Fast, accurate agents that accumulate project-specific knowledge automatically

**Secondary Persona: Project Team**
- Role: Teams deploying DevForgeAI for their projects
- Needs: Domain-specific agent experts (database, API, websocket, etc.)
- Frustrations: Generic agents don't understand project-specific patterns
- Goals: Specialized experts that understand their unique codebase

## Scope Boundaries

### In Scope (MVP)
✅ Meta-Skills (generate skills with self-improvement)
✅ Meta-Agents (generate agents with expertise accumulation)
✅ Meta-Prompts (generate prompts with learning patterns)
✅ Expertise Files (YAML-based mental models)
✅ Self-Improvement Workflow (automatic learning after N executions)
✅ Threshold-Based Triggers (execution counter in expertise files)
✅ Hook Integration (post-dev, post-qa, post-release)
✅ /create-meta-expert command (user-facing)
✅ /self-improve command (manual trigger)
✅ Subagent context injection (pre-launch mental models)
✅ Ideation integration (create meta-files after /ideate)
✅ internet-sleuth integration (knowledge updates)

### Out of Scope (Future Releases)
❌ Meta-Commands (comprehensive meta-layer for all commands) - Deferred to Epic 4+
❌ Meta-Context (evolving context files) - Deferred to Epic 4+
❌ Meta-Rules (self-modifying rules) - Deferred to Epic 4+
❌ Advanced ML-based pattern extraction - Use Claude's native analysis only
❌ External knowledge bases - File-based only, no databases
❌ Multi-project expertise sharing - Per-project isolation only

## Functional Requirements

### FR-001: Expertise File Management
**Priority:** P0 (EPIC-001, Feature 1)

The system shall provide CRUD operations for expertise files stored in `devforgeai/meta/expertise/{domain}-expert.yaml`.

**Requirements:**
- FR-001.1: Define YAML schema with fields: domain, knowledge, learnings, validation_rules, metrics
- FR-001.2: Create new expertise file with placeholder structure
- FR-001.3: Read existing expertise file and parse YAML
- FR-001.4: Update expertise file (add knowledge, learnings, update metrics)
- FR-001.5: List all expertise files in project
- FR-001.6: Validate expertise file against schema before writing

**Acceptance Criteria:**
- Expertise files follow consistent YAML structure
- File size <100KB (enforce pruning if exceeded)
- All file operations complete in <100ms
- Invalid YAML is rejected with clear error message

---

### FR-002: Mental Model Validation
**Priority:** P0 (EPIC-001, Feature 2)

The system shall validate expertise mental models against actual codebase to detect staleness and calculate accuracy scores.

**Requirements:**
- FR-002.1: Execute validation rules from expertise file (e.g., "Check if table X exists")
- FR-002.2: Compare mental model facts with codebase reality
- FR-002.3: Calculate accuracy score (% of facts that are correct)
- FR-002.4: Detect staleness (if accuracy <70%, mark as STALE)
- FR-002.5: Update metrics with last_validation timestamp and accuracy_score

**Acceptance Criteria:**
- Validation workflow completes in <30s
- Accuracy score is 0.0-1.0 (0-100%)
- Staleness flag is boolean (true if <70% accurate)
- Validation errors logged for debugging

---

### FR-003: Execution History Tracking
**Priority:** P0 (EPIC-001, Feature 3)

The system shall track agent execution history in separate per-expert files (`devforgeai/meta/history/{domain}-expert-history.json`) to enable threshold-based triggers.

**Requirements:**
- FR-003.1: Create execution history file when expert first used
- FR-003.2: Increment execution_count after each agent execution
- FR-003.3: Record last_executed timestamp
- FR-003.4: Log execution details (timestamp, operation, outcome, tokens_used)
- FR-003.5: Reset execution_count after self-improvement triggers

**Acceptance Criteria:**
- Execution count increments correctly (no duplicates)
- History file supports 100+ execution records
- File I/O completes in <100ms
- History file is separate from expertise file (no bloat)

---

### FR-004: Domain Mapping Configuration
**Priority:** P0 (EPIC-001, Feature 4)

The system shall maintain domain mappings configuration (`devforgeai/meta/domain-mappings.yaml`) that maps file path glob patterns to relevant domain experts.

**Requirements:**
- FR-004.1: Define YAML schema for domain mappings (glob_pattern → expert_id)
- FR-004.2: Load domain mappings at workflow start
- FR-004.3: Match changed files against glob patterns to find relevant experts
- FR-004.4: Support wildcard patterns (e.g., `src/db/**`, `**/*.sql`)
- FR-004.5: Allow manual override (user specifies expert explicitly)

**Acceptance Criteria:**
- Domain mappings YAML is valid and parseable
- Pattern matching works correctly (10/10 test cases pass)
- Supports at least 20 domain mappings per project
- Lookup completes in <1s

---

### FR-005: File Locking & Concurrency
**Priority:** P0 (EPIC-001, Feature 5)

The system shall implement file locking to prevent simultaneous writes to expertise files and provide merge strategies for concurrent updates.

**Requirements:**
- FR-005.1: Acquire file lock before writing expertise file
- FR-005.2: Wait for lock if unavailable (timeout after 5 minutes)
- FR-005.3: Release lock after write completes
- FR-005.4: Atomic writes (write to temp file, rename)
- FR-005.5: Merge changes if another agent updated expertise while waiting

**Acceptance Criteria:**
- No corrupted expertise files from concurrent writes (0 failures in 100 concurrent test runs)
- Lock acquisition completes in <1s (typical case)
- Timeout triggers after 5 minutes (edge case)
- Merge strategy preserves both agents' learnings (no data loss)

---

### FR-006: Ideation Integration
**Priority:** P0 (EPIC-001, Feature 6)

The system shall detect ambiguities and missing framework capabilities during `/ideate` workflow, auto-generating meta-file specifications in first epic for project-specific customization.

**Requirements:**
- FR-006.1: Detect when project requires capabilities not in DevForgeAI framework
- FR-006.2: Propose meta-file creation (agents, skills, prompts) for project needs
- FR-006.3: Create Epic 0 (if needed) for meta-file generation
- FR-006.4: Invoke internet-sleuth for knowledge updates (APIs, libraries post-LLM-cutoff)
- FR-006.5: User reviews and approves proposed meta-files

**Acceptance Criteria:**
- Ambiguity detection identifies 90% of missing capabilities
- Epic 0 proposal includes clear justification (why meta-files needed)
- internet-sleuth invocation provides relevant research
- User can accept/reject proposal via AskUserQuestion

---

### FR-007 through FR-025: Meta-Generation Layer (EPIC-002)
[Detailed requirements for Features 1-6 of EPIC-002: Meta-Prompt Generator, Meta-Skill Generator, Meta-Agent Generator, Subagent Context Injection, /create-meta-expert Command, Meta-Template Library]

---

### FR-026 through FR-045: Self-Improvement Automation (EPIC-003)
[Detailed requirements for Features 1-7 of EPIC-003: Self-Improvement Workflow, Threshold-Based Triggers, Hook Integration, Staleness Detection, /self-improve Command, internet-sleuth Integration, Feedback Complement]

---

## Non-Functional Requirements

### NFR-001: Performance
- **NFR-001.1:** Expertise file I/O: <100ms per read/write operation
- **NFR-001.2:** Mental model validation: <30s to validate against codebase
- **NFR-001.3:** Self-improvement workflow: <30s to analyze execution and update expertise
- **NFR-001.4:** Meta-generation: <60s to generate agent + skill + expertise file
- **NFR-001.5:** Context injection: <5s to extract context and create mental model YAML

### NFR-002: Quality
- **NFR-002.1:** Mental model accuracy: >80% facts correct when validated
- **NFR-002.2:** Learning accuracy: 85% of auto-learned facts remain valid after 30 days
- **NFR-002.3:** Generated expert validation: 90% pass validation on first attempt
- **NFR-002.4:** Hook reliability: 99% of post-execution hooks successfully trigger
- **NFR-002.5:** Staleness detection recall: 95% of stale expertise correctly detected

### NFR-003: Scalability
- **NFR-003.1:** Support 10-20 expertise files per project
- **NFR-003.2:** Support 100+ execution records per expert
- **NFR-003.3:** Handle 5 concurrent expertise file updates (with file locking)
- **NFR-003.4:** Expertise file size: <100KB per file (with pruning)

### NFR-004: Usability
- **NFR-004.1:** /create-meta-expert command: <10 questions to create domain expert
- **NFR-004.2:** Error messages: Clear guidance when generation/learning fails
- **NFR-004.3:** Staleness warnings: Users notified when expert is re-learning
- **NFR-004.4:** Learning transparency: Users see what changed in expertise files

### NFR-005: Reliability
- **NFR-005.1:** Atomic writes: No partial expertise file updates (rollback on failure)
- **NFR-005.2:** Backup before update: Preserve previous expertise version
- **NFR-005.3:** Hook failures logged: Alert on hook failures, retry 3x
- **NFR-005.4:** False positive rate: <10% of staleness detections are false alarms

### NFR-006: Backward Compatibility
- **NFR-006.1:** 100% of existing DevForgeAI workflows continue working (opt-in enhancement)
- **NFR-006.2:** No breaking changes to existing skills, agents, commands
- **NFR-006.3:** Feedback system continues working (complementary, not replaced)

### NFR-007: Constraints
- **NFR-007.1:** CRITICAL: All features must work within Claude Code Terminal confines (no aspirational features)
- **NFR-007.2:** No external dependencies (npm packages) for meta-system core
- **NFR-007.3:** File-based only (no databases, no external knowledge bases)
- **NFR-007.4:** WSL2 compatibility (file locking must work in /mnt/c/ paths)

## Data Model

### Entities

**1. Expertise File** (`devforgeai/meta/expertise/{domain}-expert.yaml`)
```yaml
domain: string  # e.g., "database", "api", "websocket"
knowledge:
  patterns: dict  # codebase patterns (e.g., table names, API endpoints)
  architecture: dict  # architectural insights (e.g., layer structure)
  entities: list  # key entities in domain
learnings:
  - pattern: string  # discovered pattern
    first_seen: datetime
    occurrence_count: integer
    confidence: float  # 0.0-1.0
validation_rules:
  - rule: string  # validation check (e.g., "Table 'users' exists")
    expected: any  # expected value
    last_validated: datetime
metrics:
  execution_count: integer
  last_executed: datetime
  last_updated: datetime
  accuracy_score: float  # 0.0-1.0
  staleness_flag: boolean
```

**2. Execution History** (`devforgeai/meta/history/{domain}-expert-history.json`)
```json
{
  "expert_id": "database-expert",
  "execution_log": [
    {
      "timestamp": "2025-12-16T10:30:00Z",
      "operation": "validate-schema",
      "outcome": "success",
      "tokens_used": 1500
    }
  ],
  "execution_count": 15,
  "last_executed": "2025-12-16T10:30:00Z",
  "last_updated": "2025-12-16T10:30:00Z"
}
```

**3. Domain Mapping** (`devforgeai/meta/domain-mappings.yaml`)
```yaml
mappings:
  "src/db/**": database-expert
  "src/api/**": api-expert
  "src/websockets/**": websocket-expert
  "**/*.sql": database-expert
```

**4. Meta-Template** (`devforgeai/meta/templates/{type}-{domain}-template.md`)
- type: "meta-prompt" | "meta-skill" | "meta-agent"
- domain: "database" | "api" | "websocket" | "generic"
- template_content: markdown with {{placeholders}}
- placeholders: list of variables to replace
- validation_rules: checks for generated output

### Relationships
- Expertise File ↔ Execution History: one-to-one
- Domain Mapping → Expertise File: one-to-many
- Meta-Template → Generated Expert: one-to-many

## Integration Points

### INT-001: DevForgeAI Hook System (STORY-018)
**Protocol:** Bash scripts in `.claude/hooks/`
**Trigger:** post-dev, post-qa, post-release
**Data Flow:** Hook → Check execution threshold → Trigger self-improvement → Update expertise
**Failure Handling:** Log failure, retry 3x, alert user if all retries fail

### INT-002: internet-sleuth Agent
**Protocol:** Task tool invocation
**Purpose:** Research latest API documentation, library updates beyond LLM cutoff
**Data Flow:** Expert detects need → Invoke internet-sleuth → Parse findings → Update expertise
**Caching:** Cache research results for 30 days

### INT-003: devforgeai-subagent-creation Skill
**Protocol:** Skill enhancement
**Purpose:** Add meta-generation logic to existing agent creation
**Data Flow:** User requests agent → Skill generates with expertise patterns → Expert created
**Backward Compatibility:** Existing agent creation continues working (opt-in meta-generation)

### INT-004: File System (YAML, JSON)
**Protocol:** Read, Write, Edit tools
**Purpose:** Persist expertise files, execution history, domain mappings
**Data Flow:** Agent → Read expertise → Validate mental model → Update expertise → Write file
**Concurrency:** File locking (flock) prevents simultaneous writes

## Risk Register

| Risk ID | Risk | Severity | Probability | Mitigation | Owner |
|---------|------|----------|-------------|------------|-------|
| RISK-001 | File locking fails in WSL2 environment | HIGH | MEDIUM | Test `flock` early (Epic 1, Feature 5), fallback to last-write-wins | TBD |
| RISK-002 | Expertise files grow unbounded | MEDIUM | HIGH | Implement size limits (<100KB), pruning/summarization | TBD |
| RISK-003 | Self-improvement corrupts expertise files | CRITICAL | LOW | Atomic writes (temp + rename), backup before update, rollback on failure | TBD |
| RISK-004 | Learning extracts wrong patterns (false positives) | HIGH | MEDIUM | Confidence scoring, require pattern seen 3+ times before adding | TBD |
| RISK-005 | Staleness detection misses real changes | MEDIUM | MEDIUM | Multiple validation strategies (file timestamps, content comparison, validation rules) | TBD |
| RISK-006 | Generated experts don't follow DevForgeAI conventions | HIGH | MEDIUM | Comprehensive validation in EPIC-002 Feature 6, template quality gates | TBD |
| RISK-007 | Hook failures silently skip self-improvement | MEDIUM | LOW | Hook logging, alert on failures, retry mechanism (3 attempts) | TBD |
| RISK-008 | internet-sleuth research is slow | LOW | MEDIUM | Cache research results for 30 days, trigger research asynchronously | TBD |

## Validation Criteria

### Phase 1 Validation (EPIC-001 Complete)
- ✅ Expertise files can be created, read, updated with <100ms I/O
- ✅ Mental model validation detects staleness correctly (95% recall)
- ✅ Execution history tracking increments correctly (0 duplicates)
- ✅ Domain mappings match file patterns accurately (10/10 test cases)
- ✅ File locking prevents corruption (0 failures in 100 concurrent writes)
- ✅ Ideation integration proposes meta-files when ambiguity detected

### Phase 2 Validation (EPIC-002 Complete)
- ✅ Meta-generation creates valid agents/skills/prompts (90% first-attempt pass rate)
- ✅ /create-meta-expert command creates functional domain expert in <10 questions
- ✅ Subagent context injection increases accuracy by 50%
- ✅ Generated experts use expertise files correctly (validate mental models)

### Phase 3 Validation (EPIC-003 Complete)
- ✅ Self-improvement workflow updates expertise autonomously (95% of updates automatic)
- ✅ Threshold triggers work correctly (fire after N executions)
- ✅ Hook integration triggers self-improvement reliably (99% success rate)
- ✅ Staleness detection identifies outdated expertise (95% recall, <10% false positives)
- ✅ internet-sleuth integration updates knowledge beyond LLM cutoff
- ✅ Feedback system continues working (complementary, not replaced)

### MVP Complete Validation
- ✅ All 3 epics complete with passing acceptance criteria
- ✅ End-to-end workflow: Create expert → Execute → Threshold triggers → Self-improve → Expertise grows
- ✅ Backward compatibility: Existing DevForgeAI workflows unaffected
- ✅ User acceptance: 70% of DevForgeAI projects use at least one meta-generated expert
- ✅ Success metrics met: 70% search reduction, 50% accuracy improvement, 80% creation time reduction, 95% autonomous learning

## Next Steps

### Immediate (After Ideation Complete)
1. **Run /create-context meta-agentic-system** - Create 6 context files (tech-stack, source-tree, dependencies, coding-standards, architecture-constraints, anti-patterns)
2. **Review Epic Documents** - Validate EPIC-001, EPIC-002, EPIC-003 align with requirements
3. **Prototype File Locking** - Test `flock` in WSL2 environment early (de-risk RISK-001)

### Sprint Planning
1. **Sprint 1 (EPIC-001):** Feature 1-2 (Expertise Files + Validation)
2. **Sprint 2 (EPIC-001):** Feature 3-4 (Execution History + Domain Mappings)
3. **Sprint 3 (EPIC-001):** Feature 5-6 (File Locking + Ideation Integration)
4. **Sprint 4 (EPIC-002):** Feature 1-3 (Meta-Prompts, Meta-Skills, Meta-Agents)
5. **Sprint 5 (EPIC-002):** Feature 4-6 (Context Injection, /create-meta-expert, Templates)
6. **Sprint 6 (EPIC-003):** Feature 1-3 (Self-Improvement Workflow, Thresholds, Hooks)
7. **Sprint 7 (EPIC-003):** Feature 4-7 (Staleness, /self-improve, internet-sleuth, Feedback)

### Long-Term (Post-MVP)
- Epic 4: Meta-Commands (generate slash commands with learning patterns)
- Epic 5: Meta-Context & Meta-Rules (self-evolving context files and rules)
- Epic 6: Multi-Project Expertise Sharing (optional expertise export/import)
- Epic 7: Advanced Pattern Extraction (ML-based learning algorithms)

---

**Document Version:** 1.0
**Last Updated:** 2025-12-16
**Status:** Complete - Ready for Architecture Phase
