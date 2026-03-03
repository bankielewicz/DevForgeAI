---
status: Proposed
date: 2025-12-21
adr-number: ADR-006
title: Integrate jscpd for Duplicate Code Detection
context: STORY-119, STORY-120, EPIC-018
author: Research (internet-sleuth agent)
---

# ADR-006: Integrate jscpd for Duplicate Code Detection

## Status
**Proposed** (pending team review and story implementation)

## Context

DevForgeAI requires duplicate code detection capabilities to enhance code quality validation. Currently, duplicate code detection is limited to pattern-based rules (AP-009 in ast-grep), which can only flag specific predefined patterns.

### Problem Statement
1. **Gap in Coverage**: Cannot detect arbitrary copy-pasted functions or code variants
2. **Multi-Language Need**: DevForgeAI supports 40+ project types; solution must be language-agnostic
3. **Tool Evaluation Question**: Should we use ast-grep, or choose an alternative?

### Research Findings
Comprehensive research (RESEARCH-006) evaluated multiple approaches:

1. **ast-grep**: Explicitly NOT designed for duplication detection
   - Designed for pattern search, lint, and rewrite
   - Can only flag exact patterns, not code variants
   - Existing rule AP-009 acknowledges this limitation
   - **Verdict**: Not suitable as duplication engine

2. **jscpd**: Rabin-Karp rolling hash algorithm
   - 150+ language support (vs PMD CPD 31 languages)
   - Mature, actively maintained, 3K+ GitHub stars
   - Fast O(n) average complexity
   - Can detect Type 1-2 clones with 85-95% accuracy
   - **Evidence**: [jscpd GitHub](https://github.com/kucherenko/jscpd)

3. **PMD CPD**: Java-based alternative
   - Better enterprise features
   - Only 31 languages (jscpd advantage)
   - Java dependency (heavier)
   - **Verdict**: Alternative if Java environment available

4. **Custom AST Implementation**: Research-backed approach
   - DECKARD and ASPDup algorithms documented
   - Requires 2-3 sprints (high effort)
   - Better AST awareness but slower
   - **Verdict**: Phase 2 enhancement if MVP proves insufficient

**Source**: RESEARCH-006 in `devforgeai/specs/research/`

## Decision

We will **integrate jscpd v1.15.0+ as the primary duplicate code detection tool** using a subprocess wrapper pattern with graceful Node.js fallback.

### Rationale

1. **Multi-Language Support**: 150+ languages covers all DevForgeAI project types
   - Python, TypeScript, C#, Java, Go, Rust, etc.
   - vs PMD CPD: only 31 languages

2. **Proven Algorithm**: Rabin-Karp rolling hash is industry standard
   - Used in plagiarism detection systems
   - Average time complexity O(n) with rolling hash
   - Double hashing prevents hash collisions
   - Type 1 clones: 95%+ accuracy
   - Type 2 clones: 85-90% accuracy

3. **Integration Patterns**: Follows established STORY-115 precedent
   - ast-grep validator uses subprocess wrapper pattern
   - Error handling and graceful fallback already proven
   - Low-risk integration approach

4. **Licensing & Community**: MIT license, active maintenance
   - 3K+ GitHub stars, community adoption
   - Regular updates and issue resolution
   - Open-source with clear development roadmap

5. **Performance**: Acceptable for DevForgeAI scale
   - <10 seconds for 1,000 files (rolling hash optimization)
   - Acceptable vs current grep approach

## Alternatives Considered

### Alternative 1: PMD CPD
- **Pros**: Industry standard, better enterprise features, exit codes for CI
- **Cons**: Java dependency (heavier), only 31 languages
- **Decision**: REJECTED for MVP, available as Phase 2 option

### Alternative 2: Custom AST Implementation
- **Pros**: Full control, DECKARD/ASPDup algorithms proven, language-agnostic
- **Cons**: 2-3 sprint development effort, maintenance burden, higher complexity
- **Decision**: DEFERRED to Phase 2-3 after MVP validation

### Alternative 3: Semgrep
- **Pros**: Already integrated in ast-grep validator
- **Cons**: Not designed for clone detection, inefficient for this use case
- **Decision**: REJECTED, security tool not suitable for duplication

### Alternative 4: No Integration (Status Quo)
- **Cons**: Cannot detect copy-pasted functions, limited quality validation
- **Decision**: REJECTED, functionality gap too significant

## Implementation Plan

### Phase 1: MVP (STORY-119/120) - 2 Weeks
1. Create `DuplicationValidator` class wrapping jscpd CLI
2. Implement JSON output parsing to DevForgeAI violation format
3. Node.js installation check with interactive prompts
4. Graceful fallback: heuristics or skip if missing
5. Severity mapping: CRITICAL/HIGH/MEDIUM/LOW based on clone type
6. YAML + JSON report generation
7. Integration tests with sample code

**Deliverables**:
- `src/claude/scripts/devforgeai_cli/validators/duplication_validator.py`
- `/validate-duplication` CLI command integration
- Test fixtures for various clone types

### Phase 2: Enhancement (STORY-120+) - 2-3 Weeks
1. Add PMD CPD as alternative tool option
2. Simple heuristic detection (regex patterns)
3. Result caching for repeated scans
4. Performance optimization and benchmarking

### Phase 3: Advanced (Future) - Optional
1. Custom AST-based implementation (if MVP insufficient)
2. Rust/C extension for performance-critical use cases
3. Incremental scanning support

## Configuration & Thresholds

### Default Settings
```yaml
tool: "jscpd"
version: ">=1.15.0,<2.0.0"

detection:
  minimum_tokens: 10              # Skip trivial duplicates
  minimum_similarity: 70%         # Below 70% likely false positive
  file_duplication_threshold: 5%  # Flag file if >5% duplicated
  timeout_seconds: 300            # 5 minute limit

severity_mapping:
  type_1_exact:
    similarity_percent: 100
    min_lines: 20
    severity: CRITICAL

  type_2_renamed:
    similarity_percent: 85-95
    min_lines: 10
    severity: HIGH

  type_3_modified:
    similarity_percent: 70-84
    min_lines: 5
    severity: MEDIUM

  type_4_semantic:
    similarity_percent: 50-69
    severity: LOW
```

### Exemptions
Support DUP-OFF/DUP-ON comments (similar to PMD CPD) for explicit code exclusion:
```python
# DUP-OFF
def generate_boilerplate():
    """Generated code, exempted from duplication checks"""
    # ... code ...
# DUP-ON
```

## Output Format

### DevForgeAI Violation Format
```yaml
violations:
  - rule_id: "DUP-001"
    severity: "HIGH"
    file: "src/models/user.py"
    start_line: 15
    end_line: 35
    message: "Duplicate code: 21-line block matches src/models/account.py:42-62 (92% similarity)"

    metadata:
      clone_type: "Type 2"
      token_count: 187
      similarity_percentage: 92
      match_count: 3

    clone_matches:
      - file: "src/models/account.py"
        line_start: 42
        line_end: 62
        similarity: 92
      - file: "src/models/profile.py"
        line_start: 18
        line_end: 38
        similarity: 91

    remediation: |
      Extract to shared function:
      1. Create extract_user_fields() in src/models/base.py
      2. Update user.py, account.py, profile.py to call shared function

summary:
  total_violations: 12
  critical: 1
  high: 5
  medium: 4
  low: 2
  duplication_percentage: 5.9%

tool:
  name: "jscpd"
  version: "1.15.0"
  algorithm: "Rabin-Karp rolling hash"
```

### Supported Output Formats
- YAML (primary for DevForgeAI integration)
- JSON (programmatic parsing)
- Text (human-readable summary)
- HTML (reporting dashboards)

## Risk Assessment

| Risk | Severity | Probability | Mitigation |
|------|----------|-------------|-----------|
| Node.js dependency | MEDIUM | MEDIUM | Interactive install prompt + heuristic fallback |
| False positives | MEDIUM | HIGH | Configurable thresholds + exemption comments |
| Performance degradation | LOW | LOW | Benchmark before optimization |
| Language-specific gaps | MEDIUM | MEDIUM | Focus on primary languages + document limitations |
| Tool maintenance | LOW | MEDIUM | Version pinning + quarterly updates |

### Mitigation Strategies

1. **Node.js Missing**:
   - Check for Node.js at validation start
   - Offer interactive install: `npm install -g jscpd`
   - Provide heuristic fallback detection (Phase 2)
   - Allow user to skip this check

2. **False Positives**:
   - Default minimum 10 tokens (skip trivial duplicates)
   - Require 70% similarity minimum
   - Provide DUP-OFF/DUP-ON comments
   - Extensive testing with real codebases
   - Community feedback loop

3. **Performance**:
   - Benchmark against current grep approach
   - Profile on large codebases (10K+ files)
   - Add optional caching (Phase 2)
   - Document timeout configuration

4. **Language Gaps**:
   - Test with primary DevForgeAI languages
   - Document known limitations per language
   - Allow per-language threshold configuration
   - Plan language-specific refinements

## Success Criteria

### Phase 1 (MVP) Acceptance
- [ ] Type 1 clones detection: ≥95% accuracy
- [ ] Type 2 clones detection: ≥80% accuracy
- [ ] False positive rate: <10% on test suite
- [ ] Performance: <10 seconds for 1,000 files
- [ ] Clear error messages for missing Node.js
- [ ] Graceful fallback works without jscpd
- [ ] Comprehensive test coverage
- [ ] Documentation complete

### Quality Metrics
- Type 1 clone accuracy: 95%+ (exact duplicates)
- Type 2 clone accuracy: 80%+ (renamed variables)
- False positive rate: <10%
- Performance: <10s per 1,000 files
- Tool available: Node.js (required) or graceful fallback

## Deployment Considerations

### Installation Requirements
1. Python 3.10+ (DevForgeAI requirement)
2. Node.js 14+ (for jscpd)
   - Check at validation start time
   - Offer install prompt if missing
   - Support system-level and npm-based installation

### Documentation
1. Setup guide with npm install instructions
2. Configuration guide for thresholds
3. Known limitations per language
4. Remediation guidance for duplicates
5. Performance characteristics by project size

### Backward Compatibility
- Optional feature (not required)
- Graceful degradation if unavailable
- No breaking changes to existing validations

## Future Enhancements

### Phase 2 (Planned)
- PMD CPD integration as alternative
- Heuristic duplication detection (regex patterns)
- Result caching for performance
- Per-language threshold configuration

### Phase 3 (Research)
- Custom AST-based implementation (DECKARD/ASPDup)
- Rust/C performance optimization
- Incremental scanning support
- Machine learning-based clone detection

## Feedback & Review

### Questions for Team
1. Is jscpd acceptable for MVP, or prefer PMD CPD despite Java dependency?
2. Should heuristic fallback be Phase 1 or Phase 2?
3. Are severity mappings (CRITICAL/HIGH/MEDIUM/LOW) appropriate?
4. Acceptable false positive rate <10% or should be lower?

### References

**Research**: `devforgeai/specs/research/RESEARCH-006-duplicate-code-detection-tools.md`
**Quick Ref**: `devforgeai/specs/research/RESEARCH-006-QUICK-REFERENCE.md`
**Tool Docs**: [jscpd GitHub](https://github.com/kucherenko/jscpd)
**Algorithm**: [DECKARD Paper](https://www.cs.ucdavis.edu/~su/publications/icse07.pdf)
**Existing Rule**: `devforgeai/ast-grep/rules/python/anti-patterns/duplicate-code.yml`

## Sign-Off

- [ ] Architecture Team Review
- [ ] Product Owner Approval
- [ ] Security Review (if required)
- [ ] Implementation Team Commitment

---

**ADR Created**: 2025-12-21
**Status**: PROPOSED (awaiting team review)
**Next Action**: Present to architecture team for feedback and approval

