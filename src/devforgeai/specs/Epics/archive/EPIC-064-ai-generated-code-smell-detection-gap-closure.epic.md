---
id: EPIC-064
title: AI-Generated Code Smell Detection Gap Closure
status: Planning
start_date: 2026-02-13
target_date: 2026-03-15
total_points: 34
completed_points: 0
created: 2026-02-13
owner: DevForgeAI Framework Team
tech_lead: claude/opus
team: DevForgeAI
source_brainstorm: (conversational — AI code smell taxonomy analysis session 2026-02-13)
source_plan: .claude/plans/generic-drifting-pond.md
related_epics: [EPIC-060, EPIC-061, EPIC-062, EPIC-063]
---

# Epic: AI-Generated Code Smell Detection Gap Closure

## Business Goal

Expand DevForgeAI's automated code smell detection from **3 types to 11 types** (+267%) by extending existing detection infrastructure. AI-generated code frequently contains specific smell patterns (data classes, placeholder code, dead code, orphaned imports, message chains) that escape current detection. This epic closes those gaps using the **proven EPIC-060/061/062 methodology** — canonical templates, evaluation rubrics, prompt versioning, and confidence-scored two-stage filtering.

**Why this matters:** The framework's quality gates catch security, architecture, and testing smells, but miss structural and data quality smells that accumulate as technical debt. Closing these gaps prevents AI-generated code from introducing silent quality degradation.

**Provenance:** This epic was produced from a comprehensive gap analysis session that:
1. Cataloged the full taxonomy of AI-generated code smells (13 categories, 50+ individual patterns)
2. Mapped each category against DevForgeAI's 4 detection agents and 6 constitutional files
3. Classified gaps into 3 tiers by detection feasibility (Treelint-based / Grep-heuristic / new infrastructure)
4. Applied EPIC-060/061/062's proven methodology (+1.48 composite improvement) to the detection problem

---

## Research Context (Full — Required for Story Creation)

### Current Detection Coverage

DevForgeAI has 4 agents that detect code smells, distributed across different workflow phases:

| Agent | Where Invoked | Current Detections | Severity |
|-------|---------------|-------------------|----------|
| `anti-pattern-scanner` (Phase 5) | QA Phase 2 | God Object (>20 methods OR >300 lines), Long Method (>50 lines), Magic Numbers | MEDIUM |
| `code-reviewer` (Section 8) | QA Phase 2, Post-dev | Anti-Gaming: skip decorators, empty tests, TODO placeholders, excessive mocking | CRITICAL |
| `code-quality-auditor` (Phase 1.5) | QA Phase 2 | Function length (Treelint), nesting depth (Treelint), cyclomatic complexity | WARNING/CRITICAL |
| `security-auditor` | QA Phase 2 | OWASP Top 10, hardcoded secrets, SQL injection, XSS, auth gaps | CRITICAL |

**Documented but NOT automated** (in `.claude/skills/devforgeai-development/references/refactoring-patterns.md`):
- Dead Code (line 444): "Unused methods, unreachable code" — listed as Low priority, no scanner integration
- Data Class (line 456): "Class with only properties, no behavior" — documented but no detection
- Feature Envy (line 461): "Method uses more from another class" — manual code-reviewer checklist only
- Primitive Obsession (line 466): "Using primitives instead of small objects" — manual checklist only
- Shotgun Surgery (line 473): "Single change requires many class modifications" — documented, not detectable
- Divergent Change (line 478): "Class changes for multiple unrelated reasons" — documented, not detectable

### Gap Analysis Results

**13 AI-specific code smell categories** were analyzed. Results:

| Category | Current Status | This Epic |
|----------|---------------|-----------|
| Security Vulnerabilities | **Strong** (3 agents overlap, OWASP Top 10) | No change |
| Testing & Validation Gaming | **Strong** (Anti-Gaming in code-reviewer) | No change |
| Architecture Violations | **Strong** (layer boundaries, circular deps) | No change |
| Structural Anti-Patterns | **Partial** (God Object, Long Method only) | +Data Class, +Middle Man |
| Error Handling | **Partial** (empty catch, generic exceptions) | No change (adequate) |
| Placeholder/Incomplete Code | **Partial** (TODO only) | +Placeholder detection (pass, return null, NotImplementedError) |
| Configuration/Environment | **Partial** (secrets, magic numbers) | No change (adequate) |
| Orphaned/Dead Code | **None** | +Dead Code Detector, +Orphaned Imports |
| Copy-Paste Artifacts | **Partial** (duplication >20%) | +Commented-Out Code |
| Over-Engineering | **None** (no detection) | +Middle Man, +Long Parameter List |
| Data Handling Issues | **None** | Out of scope (requires data flow analysis) |
| Performance Anti-Patterns | **Partial** (N+1 queries) | No change (adequate) |
| Dependency Issues | **Strong** (library substitution, version checks) | No change |

### Treelint AST Capabilities (Detection Infrastructure)

**Source:** `devforgeai/specs/context/tech-stack.md` v1.4, `devforgeai/specs/context/dependencies.md` v1.1

Treelint v0.12.0+ provides AST-aware code search for supported languages:

**Available queries (used by this epic):**
- `treelint search --type function --name "PATTERN" --format json` — Returns: name, file, lines.start/end, signature, body
- `treelint search --type class --name "PATTERN" --format json` — Returns: name, file, lines.start/end, members.methods[], members.properties[], bases[]
- `treelint map --ranked --format json --top N` — Returns: files ranked by complexity/references
- `treelint deps --calls --symbol "FUNCTION" --format json` — Returns: callers[], callees[] (dependency graph)

**Supported languages:** Python (.py), TypeScript (.ts, .tsx), JavaScript (.js, .jsx), Rust (.rs), Markdown (.md)
**Unsupported (Grep fallback):** C# (.cs), Java (.java), Go (.go), Ruby (.rb), PHP (.php)

**Fallback decision tree** (from `.claude/agents/references/treelint-search-patterns.md`):
1. Check file extension → Supported? Use Treelint. Unsupported? Use Grep.
2. Attempt Treelint → Exit 0? Return results. Exit 127/126? Binary not found → Grep fallback.
3. Malformed JSON? → Grep fallback. Empty results (count=0)? → Valid result, do NOT fallback.

### EPIC-060/061/062 Proven Methodology (Applied to This Epic)

**Source:** `devforgeai/specs/research/evaluation-results.md`, `devforgeai/specs/research/evaluation-rubric.md`, `devforgeai/specs/research/evaluation-pipeline.md`

**Pilot results (3 agents, Sprint 1):**

| Agent | Before | After | Delta |
|-------|--------|-------|-------|
| test-automator | 3.15 | 4.65 | +1.50 |
| ac-compliance-verifier | 3.20 | 4.65 | +1.45 |
| requirements-analyst | 3.00 | 4.50 | +1.50 |
| **Average** | **3.12** | **4.60** | **+1.48** |

**5-dimension evaluation rubric** (from `evaluation-rubric.md` v1.0):

| Dimension | Weight | Scoring |
|-----------|--------|---------|
| Task Completion Accuracy | 30% | 1-5: Does agent fully satisfy task requirements? |
| Output Structure Compliance | 20% | 1-5: Does output conform to expected format? |
| Edge Case Handling | 20% | 1-5: Does agent handle boundary conditions? |
| Instruction Adherence | 15% | 1-5: Does agent follow constraints? |
| Conciseness/Token Efficiency | 15% | 1-5: Is output appropriately sized? |

**Composite = SUM(dimension_score x weight)**

**Key prompt engineering patterns applied:**
- **PE-059 (Confidence Scoring):** Attach 0.0-1.0 confidence to each finding. Threshold 0.7 = report; <0.7 = suppress.
- **PE-060 (Two-Stage Filtering):** Stage 1 = regex/Grep for high recall. Stage 2 = LLM assessment for precision. Reduces false positives from 40-60% to <15%.
- **PE-005 (Chain-of-Thought):** Explicit thinking tags in two-stage LLM assessment.
- **PE-047 (Fresh Context Recovery):** Phase 01 orientation for crash recovery.

**Prompt versioning** (STORY-390):
- Before modification: `/prompt-version capture {agent-file}`
- After modification: `/prompt-version finalize {agent} --reason "EPIC-064: {change}"`
- On regression: `/prompt-version rollback {agent} --version previous` (SLA: <120 seconds)

### Constitutional Alignment

**Source:** `devforgeai/specs/context/anti-patterns.md` v1.1 (line 285)

> *"REMEMBER: Projects using DevForgeAI will have their own anti-patterns.md with project-specific forbidden patterns (SQL injection, N+1 queries, God objects, etc.)."*

**Implication:** Code smell detection rules are **project-level** patterns detected by the anti-pattern-scanner agent. They are NOT framework-level anti-patterns in the constitutional file. Therefore:
- **No modification** to `anti-patterns.md` (stays LOCKED at v1.1)
- Detection rules live in `anti-pattern-scanner` Phase 5 and reference files
- ADR-017 formalizes this architectural decision

**Source:** `devforgeai/specs/context/architecture-constraints.md` v1.0

New `dead-code-detector` subagent follows Layer 2 (Subagent layer):
- ✅ Subagents can use: Read, Grep, Glob, Bash(treelint:*)
- ❌ Subagents cannot invoke: Skills, Commands
- Read-only constraint: NO Write/Edit tools (ADR-016)

**Source:** `devforgeai/specs/context/dependencies.md` v1.1

Zero new external dependencies. All detection via:
- Treelint (already approved, v0.12.0+)
- Native Claude Code tools (Read, Grep, Glob)
- No new packages, no new binaries

**Source:** `devforgeai/specs/context/source-tree.md` v3.8

New files follow established patterns:
- `.claude/agents/dead-code-detector.md` (agent definition)
- `.claude/agents/dead-code-detector/references/` (progressive disclosure)
- `.claude/agents/anti-pattern-scanner/references/` (extended references)
- `devforgeai/specs/adrs/ADR-016-*.md`, `ADR-017-*.md` (architectural decisions)

---

## Success Metrics

- **Metric 1:** Automated smell types: 3 → 11 (count in code-smell-catalog.md)
- **Metric 2:** anti-pattern-scanner composite score delta >= +1.0 (evaluated via EPIC-062 rubric)
- **Metric 3:** False positive rate < 15% average on two-stage filtered items (Commented-Out Code, Placeholder, Message Chains, Orphaned Imports)
- **Metric 4:** Zero regressions on existing 3 smell detections (God Object, Long Method, Magic Numbers)
- **Metric 5:** dead-code-detector baseline composite score >= 4.0 (new agent, evaluated fresh)

**Measurement Plan:**
- Evaluate using `devforgeai/specs/research/evaluation-pipeline.md` (3 prompts per agent, 5-dimension rubric)
- Track in `devforgeai/specs/research/evaluation-results.md` (add EPIC-064 section)
- Review after each sprint (3 evaluation checkpoints)

---

## Scope

### In Scope

<!-- IMPORTANT FOR STORY CREATION:
Each feature below contains ALL context needed for story creation.
A fresh Claude session should:
1. Read this epic file
2. Find the feature section for the target story
3. Have COMPLETE context to create the story without ambiguity
No external references required beyond the constitutional context files.
-->

#### Feature 1: Anti-Pattern-Scanner Phase 5 — Tier 1 Quick Wins (13 pts)

**Integration point:** `.claude/agents/anti-pattern-scanner.md` Phase 5 (Code Smells)
**Current Phase 5 detections:** God Objects (>20 methods OR >300 lines), Long Methods (>50 lines), Magic Numbers
**Pattern to follow:** Existing Phase 5 detection format with severity, JSON output, Treelint + Grep fallback

**STORY-399: Add Data Class Detection to Anti-Pattern-Scanner** (3 pts)

*What is a Data Class?* A class that holds data (properties/fields) but has little or no behavior (methods). This is a Fowler code smell indicating behavior should be moved to where the data lives, or the class should be a proper value object.

*Detection approach:*
- Use `treelint search --type class --format json` to enumerate all classes
- For each class, check `members.methods.length` and `members.properties.length`
- Flag if: `methods.length < 3 AND properties.length > 2`
- Two-stage filter (PE-060): Stage 1 matches → Stage 2 LLM reads class body to distinguish:
  - TRUE data class (only getters/setters, no logic) → confidence >= 0.7 → REPORT
  - Valid DTO with validation logic → confidence < 0.7 → SUPPRESS
  - Dataclass/record (Python @dataclass, TypeScript interface) → confidence varies by context
- Grep fallback for unsupported languages: `class\s+\w+.*{` then count method/property patterns

*JSON output format:*
```json
{
  "smell_type": "data_class",
  "severity": "MEDIUM",
  "class_name": "UserDTO",
  "file": "src/models/user.py",
  "line": 15,
  "method_count": 1,
  "property_count": 8,
  "confidence": 0.85,
  "evidence": "Class has 8 properties and only 1 method (__init__)",
  "remediation": "Consider moving behavior to this class or converting to a value object"
}
```

*Test scenarios:*
- Python class with 0 methods, 5 properties → detected (confidence >= 0.8)
- Python @dataclass with custom __eq__ → suppressed (confidence < 0.7, valid pattern)
- TypeScript interface (no methods by design) → suppressed (interfaces are structural, not behavioral)
- Java POJO with only getters/setters → detected (confidence >= 0.75)
- Class with 2 methods + 6 properties → borderline, LLM decides

*Files to modify:* `.claude/agents/anti-pattern-scanner.md` (Phase 5 extension)

---

**STORY-400: Add Long Parameter List Detection to Anti-Pattern-Scanner** (2 pts)

*What is a Long Parameter List?* A function/method with more than 4 parameters, indicating the function may be doing too much or parameters should be grouped into an object.

*Detection approach:*
- Use `treelint search --type function --format json` to enumerate all functions
- Parse `signature` field to count parameters
- Exclude `self` and `cls` (Python) from count
- Flag if: `parameter_count > 4`
- No two-stage filter needed (low false positive rate — parameter count is unambiguous)
- Grep fallback: `def\s+\w+\([^)]*,[^)]*,[^)]*,[^)]*,[^)]*\)` (5+ commas in signature)

*JSON output format:*
```json
{
  "smell_type": "long_parameter_list",
  "severity": "MEDIUM",
  "function_name": "create_user",
  "file": "src/services/user_service.py",
  "line": 42,
  "parameter_count": 7,
  "parameters": ["name", "email", "password", "role", "department", "manager_id", "is_active"],
  "evidence": "Function has 7 parameters (threshold: 4)",
  "remediation": "Introduce Parameter Object: group related params into CreateUserRequest"
}
```

*Test scenarios:*
- Function with 5 params (excl. self) → detected
- Function with 3 params → not detected (below threshold)
- Function with `self, a, b, c, d, e` → detected (5 params, self excluded)
- Python `*args, **kwargs` → not counted as individual params

*Files to modify:* `.claude/agents/anti-pattern-scanner.md` (Phase 5 extension)
*Note:* This smell is already documented in `refactoring-specialist` (threshold >4) — this story promotes it to automated detection.

---

**STORY-401: Add Commented-Out Code Detection to Anti-Pattern-Scanner** (5 pts)

*What is Commented-Out Code?* Code blocks that have been commented out rather than deleted. This is a form of dead code that clutters the codebase. Version control (git) should be used instead of commenting out code.

*Detection approach — Two-Stage Filter (PE-060):*

**Stage 1 (Grep — high recall):**
Patterns indicating code in comments:
```
# Python: commented-out code patterns
Grep(pattern="^\\s*#\\s*(def |class |import |from |return |if |for |while |try:|except)", glob="**/*.py")

# TypeScript/JavaScript: commented-out code patterns
Grep(pattern="^\\s*//\\s*(function |class |import |export |return |const |let |var |if |for )", glob="**/*.{ts,tsx,js,jsx}")

# Multi-line comment blocks containing code
Grep(pattern="/\\*[\\s\\S]*?(function|class|import|return)[\\s\\S]*?\\*/", glob="**/*.{ts,tsx,js,jsx}", multiline=true)
```

**Stage 2 (LLM assessment — high precision):**
For each Stage 1 match:
- Read ±5 lines of surrounding context
- LLM classifies as:
  - `code` (actual commented-out code) → confidence >= 0.7 → REPORT
  - `documentation` (code example in docstring/JSDoc) → confidence < 0.7 → SUPPRESS
  - `todo` (intentional TODO with code sketch) → confidence varies
- Chain-of-thought (PE-005): LLM explains reasoning before classification

*JSON output format:*
```json
{
  "smell_type": "commented_out_code",
  "severity": "LOW",
  "file": "src/services/auth.py",
  "line_start": 45,
  "line_end": 52,
  "excerpt": "# def old_authenticate(user, password):\n#     return check_hash(password, user.hash)",
  "confidence": 0.92,
  "classification": "code",
  "evidence": "8-line block of commented-out function definition",
  "remediation": "Delete commented-out code; use git history to recover if needed"
}
```

*Test scenarios:*
- 8-line commented Python function → detected (confidence ~0.9)
- JSDoc example showing usage → suppressed (confidence ~0.3, documentation)
- Single `# import os` → detected but low confidence (~0.6, borderline)
- `// TODO: refactor this later` → suppressed (not code, just comment)
- Commented-out test case → detected (confidence ~0.8)

*Files to modify:* `.claude/agents/anti-pattern-scanner.md` (Phase 5 extension)
*Files to create:* `.claude/agents/anti-pattern-scanner/references/two-stage-filter-patterns.md` — contains Grep patterns, LLM prompt template, confidence calibration examples

---

**STORY-402: Add Orphaned Import Detection to Anti-Pattern-Scanner** (3 pts)

*What is an Orphaned Import?* An import/require/using statement that brings in a symbol that is never used in the file. This adds unnecessary dependencies and confuses readers.

*Detection approach:*
- Grep all import statements per source file:
  ```
  Python: Grep(pattern="^(import |from .+ import )", glob="**/*.py")
  TypeScript/JS: Grep(pattern="^import .+ from ", glob="**/*.{ts,tsx,js,jsx}")
  ```
- Extract imported symbol name(s)
- Search the SAME file for each symbol (excluding the import line itself)
- Flag if symbol has zero usages in the file

*Edge cases requiring careful handling:*
- `import *` (wildcard) → skip (cannot determine individual symbol usage)
- Re-exports (`export { X } from './y'`) → not orphaned (used as re-export)
- Type-only imports (`import type { X }`) → check type usage, not value usage
- Side-effect imports (`import './polyfill'`) → not orphaned (intentional side effect)
- `__all__` in Python → symbols listed in `__all__` are used (for public API)

*JSON output format:*
```json
{
  "smell_type": "orphaned_import",
  "severity": "LOW",
  "file": "src/services/payment.py",
  "line": 3,
  "import_statement": "from datetime import timezone",
  "imported_symbol": "timezone",
  "usage_count": 0,
  "evidence": "Symbol 'timezone' imported but never referenced in file",
  "remediation": "Remove unused import: 'from datetime import timezone'"
}
```

*Test scenarios:*
- `import os` with no `os.` usage → detected
- `from typing import List` used in type hints → not detected (used)
- `import './styles.css'` (side-effect) → not detected (excluded)
- `import * as utils from './utils'` → skipped (wildcard)
- `from . import models` with `models.User` usage → not detected (used)

*Files to modify:* `.claude/agents/anti-pattern-scanner.md` (Phase 5 extension)

---

#### Feature 2: Dead Code Detector Subagent (8 pts)

**New subagent:** `.claude/agents/dead-code-detector.md`
**Architecture:** Layer 2 (Subagent), read-only tools only (ADR-016)
**Template:** Canonical 10-element composite prompt (EPIC-061 pattern)
**Invocation:** From anti-pattern-scanner Phase 5 or directly via Task()

**STORY-403: Create Dead-Code-Detector Subagent** (8 pts)

*What is Dead Code?* Functions, methods, or classes that are defined but never called from anywhere in the codebase. These are maintenance burdens that confuse developers and increase cognitive load.

*Why a separate subagent?* Dead code detection requires call-graph analysis (`treelint deps --calls`) which is a fundamentally different detection mechanism from the pattern-matching used in anti-pattern-scanner Phase 5. It also requires entry-point exclusion logic that would bloat the scanner agent beyond its size limit.

*10-element canonical template structure:*
1. **Role:** Dead code detection specialist for identifying unreachable functions in target project codebases
2. **Task:** Enumerate all functions → build dependency graph → identify zero-caller functions → exclude entry points → report with confidence
3. **Context:** Treelint AST dependency analysis, constitutional constraints from tech-stack.md and source-tree.md
4. **Examples:** Include 2-3 worked examples showing: zero-caller helper (REPORT), main() entry point (EXCLUDE), @pytest.fixture (EXCLUDE)
5. **Input Data:** Target directory path, optional file filter pattern, optional exclusion patterns
6. **Thinking:** Explicit thinking phase: "For each zero-caller function, check entry point patterns before reporting"
7. **Output Format:** JSON array of findings with function_name, file, line, callers_count, is_entry_point, exclusion_reason, confidence
8. **Constraints:** Read-only (Read, Bash(treelint:*), Grep, Glob ONLY), no file modification, no deletion
9. **Uncertainty Handling:** Dynamic dispatch, reflection, monkey-patching → flag with confidence < 0.5, suggest manual review
10. **Prefill:** Start with systematic entry-point check before reporting any dead code

*4-phase workflow:*
1. **Phase 1: Context Loading** — Read tech-stack.md, source-tree.md to understand project structure and supported languages
2. **Phase 2: Function Discovery** — `treelint search --type function --format json` for all source files. Grep fallback for unsupported languages.
3. **Phase 3: Dependency Analysis** — For each function, `treelint deps --calls --symbol {function_name} --format json`. Count callers. Flag zero-caller functions.
4. **Phase 4: Entry Point Exclusion + Results** — Apply exclusion patterns (see below). Report remaining zero-caller functions.

*Entry point exclusion patterns* (to be stored in `.claude/agents/dead-code-detector/references/entry-point-patterns.md`):

| Pattern | Language | Example | Reason |
|---------|----------|---------|--------|
| `main()`, `__main__` | Python | `if __name__ == '__main__': main()` | CLI entry point |
| `@app.route`, `@router.` | Python (Flask/FastAPI) | `@app.route('/api/users')` | HTTP endpoint |
| `@pytest.fixture` | Python | `@pytest.fixture def db_session()` | Test fixture |
| `@click.command`, `@click.group` | Python (Click) | `@click.command() def cli()` | CLI handler |
| `module.exports`, `export default` | JS/TS | `export default function handler()` | Module export |
| `@Controller`, `@Get`, `@Post` | TS (NestJS) | `@Get('/users') findAll()` | HTTP endpoint |
| `test_*`, `*_test` | Python/JS | `def test_login():` | Test function |
| `setup()`, `teardown()` | Python | `def setup_module():` | Test lifecycle |
| `@app.on_event` | Python (FastAPI) | `@app.on_event("startup")` | Lifecycle hook |
| `__init__`, `__str__`, `__repr__` | Python | `def __init__(self):` | Dunder methods |

*JSON output format:*
```json
{
  "findings": [
    {
      "smell_type": "dead_code",
      "severity": "LOW",
      "function_name": "calculate_legacy_discount",
      "file": "src/services/pricing.py",
      "line": 145,
      "callers_count": 0,
      "is_entry_point": false,
      "exclusion_reason": null,
      "confidence": 0.88,
      "evidence": "Function has 0 callers and matches no entry point patterns",
      "remediation": "Review function for removal; check git blame for last usage"
    }
  ],
  "summary": {
    "total_functions": 234,
    "zero_caller_functions": 12,
    "excluded_entry_points": 45,
    "reported_dead_code": 8,
    "suppressed_low_confidence": 4
  }
}
```

*Test scenarios:*
- Helper function with 0 callers → detected (confidence ~0.9)
- `main()` function → excluded (entry point)
- `@pytest.fixture` → excluded (test infrastructure)
- `@app.route('/api/health')` → excluded (HTTP endpoint)
- Function called only via dynamic dispatch (`getattr(obj, 'method')()`) → detected but low confidence (~0.4)
- Overridden method in subclass → NOT dead code (check inheritance chain)
- `__init__` with 0 explicit callers → excluded (dunder method, called implicitly)

*Files to create:*
- `.claude/agents/dead-code-detector.md` (canonical 10-element template)
- `.claude/agents/dead-code-detector/references/entry-point-patterns.md` (exclusion patterns table)

*ADR required:* ADR-016 — Dead-Code-Detector Read-Only Constraint
- Decision: Detection-only, no deletion capability
- Tools: Read, Bash(treelint:*), Grep, Glob — NO Write/Edit
- Rationale: Zero risk of incorrect deletion; manual review before removal

*Registry update:* Add to CLAUDE.md subagent registry table

---

#### Feature 3: Code-Reviewer Placeholder Detection (5 pts)

**Integration point:** `.claude/agents/code-reviewer.md` Section 8 (Anti-Gaming Validation)
**Current Section 8:** Detects skip decorators, empty tests, TODO/FIXME placeholders, excessive mocking
**Extension:** Add Section 8.5 for placeholder/incomplete code in production source files

**STORY-404: Extend Anti-Gaming with Placeholder/Incomplete Code Detection** (5 pts)

*What is Placeholder Code?* Code that was written as a stub during development and never completed. Common in AI-generated code where the model produces a function signature but defers the implementation.

*Detection approach — Two-Stage Filter (PE-060):*

**Stage 1 (Grep patterns):**
```
# Python placeholders
Grep(pattern="^\\s*pass\\s*$", glob="**/*.py")                        # bare pass
Grep(pattern="raise NotImplementedError", glob="**/*.py")              # unimplemented
Grep(pattern="return None\\s*#\\s*(TODO|FIXME|HACK)", glob="**/*.py") # placeholder return

# TypeScript/JavaScript placeholders
Grep(pattern="throw new Error\\('Not implemented'\\)", glob="**/*.{ts,tsx,js,jsx}")
Grep(pattern="return null;\\s*//(\\s*TODO|\\s*FIXME)", glob="**/*.{ts,tsx,js,jsx}")
Grep(pattern="\\{\\s*\\}", glob="**/*.{ts,tsx,js,jsx}")              # empty blocks

# General
Grep(pattern="console\\.log\\(['\"]fix later['\"]\\)", glob="**/*.{ts,tsx,js,jsx}")
Grep(pattern="# FIXME|# HACK|# XXX", glob="**/*.py")
```

**Stage 2 (LLM assessment):**
Exclusion patterns (valid, NOT placeholder):
- `except SomeError: pass` → valid catch-and-ignore (intentional)
- `class MyInterface(ABC): pass` → valid abstract class body
- `def __init__(self): pass` → valid empty constructor
- `{}` in object literal → valid empty object, not empty block
- `raise NotImplementedError` in abstract base class → valid (enforces subclass override)

LLM reads ±3 lines context, classifies as:
- `placeholder` (incomplete implementation) → confidence >= 0.7 → REPORT
- `valid_pattern` (intentional minimal code) → confidence < 0.7 → SUPPRESS

*JSON output format:*
```json
{
  "smell_type": "placeholder_code",
  "severity": "HIGH",
  "file": "src/services/notification.py",
  "line": 23,
  "pattern_type": "bare_pass",
  "surrounding_context": "def send_email(to, subject, body):\n    pass",
  "confidence": 0.95,
  "evidence": "Function body is only 'pass' — implementation missing",
  "remediation": "Implement send_email function or remove if not needed"
}
```

*Test scenarios:*
- `def process(): pass` in src/ → detected (confidence ~0.95, bare pass in production)
- `except ValueError: pass` → suppressed (confidence ~0.3, valid catch pattern)
- `class ABCMixin(ABC): pass` → suppressed (confidence ~0.2, valid abstract)
- `raise NotImplementedError("TODO")` in concrete class → detected (confidence ~0.85)
- `raise NotImplementedError` in abstract base → suppressed (confidence ~0.2, valid pattern)
- `return null; // TODO: implement` → detected (confidence ~0.9)

*IMPORTANT: Exclude test directories* — test files legitimately contain stubs, mocks, and minimal implementations. Only scan production source directories (src/, lib/, app/).

*Files to modify:* `.claude/agents/code-reviewer.md` (Section 8 extension, add Section 8.5)

---

#### Feature 4: Anti-Pattern-Scanner Phase 5 — Tier 2 (5 pts)

**Integration point:** `.claude/agents/anti-pattern-scanner.md` Phase 5 (Code Smells)
**Depends on:** Feature 1 completion (Tier 1 detections proven successful)

**STORY-405: Add Middle Man Detection to Anti-Pattern-Scanner** (3 pts)

*What is a Middle Man?* A class where the majority of its methods simply delegate to another class. The class adds no value and should be removed, with clients calling the delegated class directly.

*Detection approach:*
- Use `treelint search --type class --format json` to enumerate all classes
- For each class, analyze `members.methods[]`
- For each method, calculate body size: `lines.end - lines.start`
- A "delegation method" has body size <= 2 lines (single statement + optional return)
- Calculate `delegation_ratio = delegation_methods / total_methods`
- Flag if: `delegation_ratio > 0.80 AND total_methods >= 3`
- The `total_methods >= 3` threshold prevents false positives on small utility classes

*JSON output format:*
```json
{
  "smell_type": "middle_man",
  "severity": "MEDIUM",
  "class_name": "UserServiceProxy",
  "file": "src/services/user_proxy.py",
  "line": 10,
  "total_methods": 8,
  "delegating_methods": 7,
  "delegation_ratio": 0.875,
  "evidence": "7 of 8 methods are single-line delegations to UserService",
  "remediation": "Remove proxy class; have clients call UserService directly"
}
```

*Test scenarios:*
- Class with 8 methods, 7 single-line delegations → detected (ratio 0.875)
- Class with 3 methods, all short → detected but borderline (ratio 1.0, check context)
- Facade class with complex orchestration → not detected (methods are multi-line)
- Adapter class (legitimate pattern) → may detect, LLM context helps distinguish
- Class with 2 methods → not detected (below minimum threshold)

*Files to modify:* `.claude/agents/anti-pattern-scanner.md` (Phase 5 extension)

---

**STORY-406: Add Message Chain Detection to Anti-Pattern-Scanner** (2 pts)

*What is a Message Chain?* A series of chained method calls like `a.getB().getC().getD()`. This violates the Law of Demeter — a client shouldn't need to navigate through multiple objects to get what it needs.

*Detection approach — Two-Stage Filter (PE-060):*

**Stage 1 (Grep — high recall):**
```
# Detect 3+ chained method calls
Grep(pattern="\\w+(\\.\\w+\\([^)]*\\)){3,}", glob="**/*.{py,ts,tsx,js,jsx}")
```

**Stage 2 (LLM assessment — high precision):**
Exclusion patterns (valid, NOT message chains):
- Builder pattern: `QueryBuilder().where(...).orderBy(...).limit(10)` → EXCLUDE
- Fluent API: `app.use(...).get(...).listen(3000)` → EXCLUDE
- Promise/async chains: `fetch(...).then(...).catch(...)` → EXCLUDE
- jQuery chains: `$('#el').addClass(...).show().animate(...)` → EXCLUDE
- String builders: `StringBuilder().append(...).append(...).toString()` → EXCLUDE

LLM reads the full chain and classifies:
- Navigation chain (accessing nested objects) → confidence >= 0.7 → REPORT
- Builder/fluent pattern → confidence < 0.7 → SUPPRESS

*JSON output format:*
```json
{
  "smell_type": "message_chain",
  "severity": "LOW",
  "file": "src/controllers/order.py",
  "line": 67,
  "chain_excerpt": "order.get_customer().get_address().get_city()",
  "chain_length": 3,
  "confidence": 0.82,
  "evidence": "3-level navigation chain through order→customer→address→city",
  "remediation": "Add order.get_customer_city() to encapsulate navigation"
}
```

*Test scenarios:*
- `order.customer.address.city` → detected (navigation chain, confidence ~0.85)
- `QueryBuilder().where(x).orderBy(y).limit(10)` → suppressed (builder pattern, confidence ~0.3)
- `fetch(url).then(r => r.json()).then(data => process(data))` → suppressed (promise chain, confidence ~0.2)
- `user.getProfile().getSettings().getTheme()` → detected (confidence ~0.8)

*Files to modify:* `.claude/agents/anti-pattern-scanner.md` (Phase 5 extension)

---

#### Feature 5: Documentation and ADR (3 pts)

**STORY-407: Document Code Smell Detection Catalog in Anti-Pattern-Scanner Reference** (3 pts)

*Purpose:* Create a comprehensive reference document cataloging all 11 automated code smell types, their thresholds, detection methods, severity levels, and remediation guidance. This serves as the canonical reference for anti-pattern-scanner Phase 5.

*What to create:*

1. **Code Smell Catalog** (`.claude/agents/anti-pattern-scanner/references/code-smell-catalog.md`):
   - Table of all 11 smell types: name, threshold, severity, detection method (Treelint/Grep), two-stage required?
   - For each smell: definition, threshold, JSON schema, test scenarios, false positive patterns
   - Cross-reference to Fowler's refactoring catalog where applicable

2. **ADR-017** (`devforgeai/specs/adrs/ADR-017-code-smell-catalog-location.md`):
   - Decision: Code smell detection rules live in anti-pattern-scanner reference files
   - NOT in constitutional `anti-patterns.md` (which governs framework behavior, not project code quality)
   - Rationale: `anti-patterns.md` v1.1 line 285 distinguishes framework vs project patterns
   - Impact: No constitutional file modification, no LOCKED status change process

3. **Source-tree update** (`devforgeai/specs/context/source-tree.md` v3.8 → v3.9):
   - Add dead-code-detector paths
   - Add new reference file paths
   - Version increment

4. **Phase 5 update** (`.claude/agents/anti-pattern-scanner.md`):
   - Add progressive disclosure reference: "Load code-smell-catalog.md for full detection procedures"
   - Ensure Phase 5 header lists all 11 smell types

*Files to create:*
- `.claude/agents/anti-pattern-scanner/references/code-smell-catalog.md`
- `devforgeai/specs/adrs/ADR-017-code-smell-catalog-location.md`

*Files to modify:*
- `.claude/agents/anti-pattern-scanner.md` (Phase 5 progressive disclosure reference)
- `devforgeai/specs/context/source-tree.md` (v3.8 → v3.9, add new paths)

---

### Out of Scope

Explicitly excluded — these require infrastructure that does not exist in the framework:

- ❌ **Shotgun Surgery** — Requires git history co-change analysis (analyzing which files change together across commits). Future EPIC for `change-impact-analyzer` subagent.
- ❌ **Divergent Change** — Requires git change-reason classification (analyzing WHY a file changes). Future EPIC, same subagent.
- ❌ **Feature Envy (automated)** — Requires cross-class method ownership analysis (which class's data does a method access most). Infeasible with Treelint/Grep. Remains as manual code-reviewer checklist item.
- ❌ **Mutable Shared State** — Requires data flow analysis (tracking variable mutations across scopes). Beyond Treelint/Grep capability.
- ❌ **Null Safety** — Requires control flow analysis (tracking null values through code paths). Recommend language-specific linters (mypy, TypeScript strict mode).
- ❌ **Speculative Generality** — Requires usage analysis of interfaces/abstractions. Partially addressed by Dead Code detector for unused functions.
- ❌ **Parallel Inheritance Hierarchies** — Requires subclass correlation analysis. Too rare to warrant automation.

---

## Target Sprints

### Sprint N (Pilot): Feature 1 — Tier 1 Quick Wins
**Goal:** Add 4 new smell detections to anti-pattern-scanner Phase 5. Validate two-stage filtering approach.
**Estimated Points:** 13
**Features:**
- STORY-399: Data Class Detection (3 pts)
- STORY-400: Long Parameter List Detection (2 pts)
- STORY-401: Commented-Out Code Detection (5 pts)
- STORY-402: Orphaned Import Detection (3 pts)

**Key Deliverables:**
- anti-pattern-scanner Phase 5 extended with 4 new smell types
- Two-stage filter reference file created
- Evaluation checkpoint: anti-pattern-scanner before/after scores

**Evaluation Prompts for anti-pattern-scanner:**
1. "Scan a clean codebase with no smells. Expected: zero findings."
2. "Scan a codebase with 1 data class, 2 long param lists, 1 commented block, 3 orphaned imports. Expected: all detected with correct severity and confidence."
3. "Scan a codebase with edge cases: @dataclass, valid DTOs, docstring examples, re-exports. Expected: all correctly suppressed."

### Sprint N+1: Features 2 + 3
**Goal:** Create dead-code-detector subagent. Extend code-reviewer placeholder detection.
**Estimated Points:** 13
**Features:**
- STORY-403: Dead Code Detector Subagent (8 pts)
- STORY-404: Placeholder Detection (5 pts)

**Key Deliverables:**
- New `dead-code-detector` subagent created and registered
- ADR-016 documented
- Code-reviewer Section 8.5 added
- Evaluation checkpoint: code-reviewer and dead-code-detector scores

### Sprint N+2: Features 4 + 5
**Goal:** Complete Tier 2 detections. Document catalog. Finalize ADRs.
**Estimated Points:** 8
**Features:**
- STORY-405: Middle Man Detection (3 pts)
- STORY-406: Message Chain Detection (2 pts)
- STORY-407: Code Smell Catalog + ADR (3 pts)

**Key Deliverables:**
- anti-pattern-scanner Phase 5 complete with all 11 smell types
- Code smell catalog reference file
- ADR-017 documented
- source-tree.md updated to v3.9
- Final evaluation: all 3 agents measured

---

## User Stories

1. **As a** framework user, **I want** the anti-pattern-scanner to detect data classes, long parameter lists, commented-out code, and orphaned imports, **so that** AI-generated code quality issues are caught during QA.
2. **As a** framework user, **I want** a dead-code-detector that finds unused functions, **so that** code cleanup is guided by objective evidence rather than guesswork.
3. **As a** framework user, **I want** the code-reviewer to detect placeholder code (pass, return null, NotImplementedError), **so that** incomplete AI-generated implementations don't pass quality gates.
4. **As a** framework user, **I want** message chain and middle man detection, **so that** structural anti-patterns in AI-generated code are flagged for refactoring.
5. **As a** framework maintainer, **I want** a comprehensive code smell catalog with thresholds and test scenarios, **so that** detection rules are documented and maintainable.

---

## Technical Considerations

### Architecture Impact
- **New subagent:** `dead-code-detector` (Layer 2, read-only)
- **Extended agents:** `anti-pattern-scanner` (Phase 5), `code-reviewer` (Section 8)
- **New reference files:** 3 new reference documents for progressive disclosure
- **No new skills or commands** — all integration through existing QA workflow

### Technology Decisions
- **Treelint** for AST-aware detection (already approved, no new technology)
- **Grep fallback** for unsupported languages (already established pattern)
- **Two-stage filtering** (PE-060) for high false-positive detections (new pattern, documented in reference file)
- **Confidence scoring** (PE-059) for all two-stage detections (new pattern)

### Security & Compliance
- Dead-code-detector is **read-only** (ADR-016) — zero risk of code modification
- No new external dependencies — no supply chain risk
- All detection tools (Treelint, Grep, Read) are already approved in tech-stack.md

### Performance Requirements
- Stage 1 (Grep): < 5 seconds for typical project
- Stage 2 (LLM): ~500 tokens per assessment, limited to Stage 1 matches only
- Dead code analysis: < 30 seconds for projects with < 500 functions
- Treelint queries: < 100ms latency per query (per ADR-013)

---

## Dependencies

### Internal Dependencies
- [x] **EPIC-060:** Prompt engineering patterns (PE-059, PE-060) — COMPLETE
- [x] **EPIC-061:** Canonical template structure (10-element) — COMPLETE
- [x] **EPIC-062:** Evaluation pipeline and rubric — COMPLETE
- [x] **STORY-390:** Prompt versioning system — COMPLETE
- [ ] **EPIC-062 Wave 1:** Validator/analyzer batch rollout — IN PROGRESS (non-blocking for this epic)

### External Dependencies
- None

---

## Risks & Mitigation

### Risk 1: Two-Stage Filtering Token Cost
- **Probability:** Medium
- **Impact:** Medium (increased token consumption per QA run)
- **Mitigation:** Stage 1 eliminates 80-90% of candidates before LLM; limit context to ±5 lines; cache repeated patterns
- **Contingency:** Fall back to regex-only with documented higher false positive rate

### Risk 2: Dead Code False Positives (Dynamic Dispatch)
- **Probability:** Medium
- **Impact:** Medium (unused functions reported that ARE used via reflection/getattr)
- **Mitigation:** Entry point exclusion patterns, confidence < 0.5 for uncertain cases, manual review guidance
- **Contingency:** Expand exclusion patterns based on pilot feedback

### Risk 3: Treelint Unavailable for Target Language
- **Probability:** High (C#, Java, Go projects)
- **Impact:** Low (Grep fallback always available)
- **Mitigation:** All detections have Grep fallback patterns tested
- **Contingency:** Warning-level messaging, not HALT

### Risk 4: Anti-Pattern-Scanner Size Exceeds Limit
- **Probability:** Medium (adding 8 smell types to Phase 5)
- **Impact:** Medium (violates Category 4: Size Violations)
- **Mitigation:** Progressive disclosure — Phase 5 references code-smell-catalog.md for detailed procedures
- **Contingency:** Extract Phase 5 into separate reference file if scanner exceeds 1000 lines

---

## Stakeholders

### Primary Stakeholders
- **Product Owner:** Bryan — Framework direction and prioritization
- **Tech Lead:** claude/opus — Architecture decisions and implementation coordination

---

## Timeline

```
Epic Timeline:
================================================================
Sprint N:    Feature 1 — Tier 1 Quick Wins (13 pts)
Sprint N+1:  Features 2+3 — Dead Code + Placeholder (13 pts)
Sprint N+2:  Features 4+5 — Tier 2 + Catalog (8 pts)
================================================================
Total Duration: 3 sprints
Total Points: 34
Stories: 9
```

### Key Milestones
- [ ] **Milestone 1:** Sprint N complete — anti-pattern-scanner has 7 smell types (from 3)
- [ ] **Milestone 2:** Sprint N+1 complete — dead-code-detector operational, code-reviewer extended
- [ ] **Milestone 3:** Sprint N+2 complete — all 11 smell types, catalog documented, ADRs filed

---

## Progress Tracking

### Sprint Summary

| Sprint | Status | Points | Stories | Completed | In Progress | Blocked |
|--------|--------|--------|---------|-----------|-------------|---------|
| Sprint N | Not Started | 13 | 4 | 0 | 0 | 0 |
| Sprint N+1 | Not Started | 13 | 2 | 0 | 0 | 0 |
| Sprint N+2 | Not Started | 8 | 3 | 0 | 0 | 0 |
| **Total** | **0%** | **34** | **9** | **0** | **0** | **0** |

### Burndown
- **Total Points:** 34
- **Completed:** 0
- **Remaining:** 34

---

## Story Verification Checklist

Before creating stories from this epic:

- [ ] All target files verified to exist (Read each file)
- [ ] All test paths match source-tree.md patterns
- [ ] No references to deleted files (check git status)
- [ ] All dependencies verified to exist
- [ ] Exact edits specified (not vague "update X")

**Status:** Not Verified

---

**Epic Template Version:** 1.0
**Last Updated:** 2026-02-13
