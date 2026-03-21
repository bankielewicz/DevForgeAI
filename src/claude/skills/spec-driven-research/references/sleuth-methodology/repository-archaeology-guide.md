# Repository Archaeology Guide - Internet-Sleuth

**Purpose:** Mine GitHub repositories for real-world implementation patterns, code examples, and architectural decisions.

**When to Use:** spec-driven-architecture Phase 2 (Technology Selection), implementation research during "Ready for Dev" / "In Development" states, pattern validation

**Loaded:** Conditionally (when research_mode = "repository-archaeology")

**Location:** Absorbed from internet-sleuth-integration per ADR-045

---

## Repository Archaeology Overview

**Scope:** Deep code analysis and pattern extraction (depth over breadth)
**Duration:** 8-10 minutes (p95)
**Output:** Implementation patterns with code examples, quality-scored repositories, architectural insights

**Research Questions Answered:**
- "How do production systems implement [pattern]?"
- "What are common pitfalls in [technology] implementations?"
- "What architectural patterns work well at scale?"
- "What are real-world code examples for [feature]?"

---

## Archaeology Workflow (8 Steps)

### Step 1: Define Search Strategy
- Formulate precise GitHub search queries
- Syntax: `[keyword] language:[lang] stars:>[stars] pushed:>[date] archived:false`
- Advanced filters: `in:readme`, `in:file`, `path:/`, `filename:`

### Step 2: Repository Quality Scoring (0-10 Scale)
- Community Health (0-3): Stars count
- Maintenance Activity (0-2): Recent commits
- Documentation Quality (0-2): README + docs/
- Test Coverage (0-2): Tests + CI
- Production Indicators (0-1): Docker/K8s configs + CI/CD

### Step 3: Code Pattern Extraction
- Architectural Patterns (layered, repository, DI, event-driven)
- Design Patterns (factory, strategy, observer, decorator)
- Integration Patterns (API clients, DB, cache, message queues)
- Security Patterns (auth flows, RBAC, input validation, secrets)

### Step 4: Architectural Insights
- Technology stack choices with rationale
- Project structure analysis
- Design decisions and trade-offs
- Scalability patterns
- Testing strategies

### Step 5: Common Pitfalls & Anti-Patterns
- GitHub Issues (bug reports, feature requests)
- PR Discussions (code review insights)
- Commit Messages (bug fix patterns)
- Documentation FAQs and gotchas

### Step 6: Framework Compliance Validation
- Validate patterns against 6 DevForgeAI context files
- Invoke context-validator subagent
- Categorize compliance issues (CRITICAL/HIGH/MEDIUM/LOW)

### Step 7: Pattern Synthesis
- Rank patterns by quality + compliance
- Filter by applicability (project type, scale, team size, maturity)
- Generate top 3 recommendations with code examples
- Link to ADR preparation if needed

### Step 8: Report Generation
- 9 required sections with YAML frontmatter
- Code snippets embedded with file paths
- Repository quality scores table
- Save to devforgeai/specs/research/

---

## Success Criteria

Repository archaeology succeeds when:
- [ ] Search strategy defined (3-5 precise GitHub queries)
- [ ] Repository quality scored (5-10 repos, score >=5 selected)
- [ ] Code patterns extracted (3-5 patterns per repo, annotated)
- [ ] Architectural insights documented (5+ high-level decisions)
- [ ] Pitfalls identified (5-10 common mistakes with fixes)
- [ ] Framework compliance validated (patterns checked against 6 context files)
- [ ] Pattern synthesis complete (top 3 ranked recommendations)
- [ ] Report generated (9 sections, YAML frontmatter, code examples)
- [ ] Duration <10 minutes (p95 threshold)
- [ ] Token usage <50K (within budget)

---

**Created:** 2025-11-17
**Absorbed into spec-driven-research:** 2026-03-20 (ADR-045)
**Version:** 1.1
**Purpose:** GitHub code mining and implementation pattern extraction
