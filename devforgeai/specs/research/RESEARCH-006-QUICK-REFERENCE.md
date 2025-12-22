# RESEARCH-006: Duplicate Code Detection - Quick Reference

**Status**: Complete | **Quality Gate**: PASS | **Date**: 2025-12-21

---

## TL;DR (Executive Summary)

**Question**: How should DevForgeAI detect duplicate code for STORY-119?

**Answer**: Integrate **jscpd via subprocess wrapper** with graceful Node.js fallback.

**Why not ast-grep?** Explicitly not designed for duplication. Rule AP-009 documentation states this.

**Why jscpd?** 150+ languages, proven Rabin-Karp algorithm, light (no Java), easy integration.

---

## Tool Comparison Matrix

| Feature | jscpd | PMD CPD | ast-grep | Custom AST |
|---------|-------|---------|----------|-----------|
| **Languages** | 150+ | 31 | 40+ (not for duplication) | 40+ (if implemented) |
| **Algorithm** | Rabin-Karp | Token-based | N/A (not suitable) | Suffix tree/DECKARD |
| **Installation** | npm (Node.js) | Java+Maven | N/A | N/A |
| **Type 1 Detection** | 95%+ | 90%+ | Pattern-based only | 95%+ |
| **Type 2 Detection** | 85-90% | 85%+ | Pattern-based only | 85-90% |
| **Integration Effort** | **MEDIUM** | HIGH | N/A | **3 SPRINTS** |
| **Licensing** | MIT | Apache 2.0 | N/A | MIT |
| **Recommendation** | **PRIMARY** | Alternative | Not suitable | Phase 2 |

---

## Recommended Architecture

### Phase 1 (MVP - STORY-119/120)

```
User: devforgeai validate --duplication /path

Check Node.js? → YES → Run jscpd → Parse JSON → Generate Report
                → NO  → Interactive Prompt:
                        1) Install npm + jscpd
                        2) Use simple heuristics
                        3) Skip this check
```

### Implementation Pattern

```python
# src/claude/scripts/devforgeai_cli/validators/duplication_validator.py

class DuplicationValidator:
    def __init__(self, tool="jscpd"):
        self.tool = tool
        self._check_installation()

    def scan(self, path, language=None):
        cmd = self._build_command(path, language)
        result = subprocess.run(cmd, capture_output=True)
        return self._parse_output(result.stdout)
```

### Future Phases

**Phase 2**: Add PMD CPD alternative + heuristics + caching
**Phase 3**: Custom AST-based implementation (if needed)

---

## Algorithm Comparison

### Rabin-Karp Rolling Hash (jscpd)
- **Time**: O(n) average (n = total tokens)
- **Space**: O(n)
- **Pros**: Fast, simple, handles all languages
- **Cons**: Token-based, misses semantic clones
- **Best For**: Type 1-2 clones (exact + renamed variables)

### AST Suffix Tree (DECKARD)
- **Time**: O(n log n) with binary search
- **Space**: O(n)
- **Pros**: AST-aware, better accuracy, semantic understanding
- **Cons**: Slow, complex, high resource usage
- **Best For**: Type 1-2 clones with structural complexity
- **Research**: [DECKARD Paper](https://www.cs.ucdavis.edu/~su/publications/icse07.pdf)

---

## Severity Mapping

```
Type 1 (100% exact):         CRITICAL
  └─ "Identical function copied 3 times"

Type 2 (85-95% similar):     HIGH
  └─ "Same logic, different variable names"

Type 3 (50-80% similar):     MEDIUM
  └─ "Similar with control flow changes"

Type 4 (<50% semantic):      LOW
  └─ "Probably not a real clone"
```

**Configurable Thresholds**:
- Min tokens: 10 (skip trivial duplicates)
- Min similarity: 70%
- File threshold: 5% duplication flags file

---

## Key Findings

### Finding 1: ast-grep NOT Designed for Duplication
- Explicitly for pattern search, lint, rewrite
- Existing rule AP-009 acknowledges limitation
- Can flag specific patterns, not general duplicates
- **Verdict**: Use for pattern-based rules, not duplication engine

**Source**: `devforgeai/ast-grep/rules/python/anti-patterns/duplicate-code.yml, lines 30-35`

### Finding 2: jscpd Superior Multi-Language Support
- jscpd: 150+ languages
- PMD CPD: 31 languages
- Critical for DevForgeAI multi-project goal

**Sources**:
- [jscpd Supported Languages](https://github.com/kucherenko/jscpd)
- [PMD CPD Supported Languages](https://pmd.github.io/pmd/pmd_userdocs_cpd.html)

### Finding 3: Rabin-Karp Algorithm Proven
- Used by jscpd, plagiarism detection, DNA matching
- Average O(n) complexity with rolling hash
- Double hashing prevents collisions
- Industry standard

**Source**: [Rabin-Karp Algorithm Explained](https://www.bomberbot.com/algorithms/the-rabin-karp-algorithm-explained-a-deep-dive-for-developers/)

### Finding 4: Subprocess Pattern Proven in STORY-115
- ast-grep validator uses subprocess wrapper
- Established error handling
- Graceful fallback pattern
- Low risk integration

**File**: `src/claude/scripts/devforgeai_cli/validators/ast_grep_validator.py`

### Finding 5: Custom AST Approach Requires 2-3 Sprints
- Need AST generation for all files (slow)
- Requires suffix tree or characteristic vector approach
- Type 1-2 clones 90%+ accuracy, Type 3-4 limited
- Better as Phase 2 after MVP stability

**Sources**: DECKARD paper, ASPDup paper (see full research report)

---

## Risk Summary

| Risk | Severity | Mitigation |
|------|----------|-----------|
| Node.js dependency | MEDIUM | Interactive install + heuristic fallback |
| False positives | MEDIUM | Configurable thresholds + exemption comments |
| Performance | LOW | Benchmark before optimization |
| Language gaps | MEDIUM | Focus on primary languages (Python, TypeScript, C#) |
| Tool maintenance | LOW | Version pinning + quarterly reviews |

---

## Implementation Checklist (STORY-119/120)

**Phase 1 (MVP)**:
- [ ] Create DuplicationValidator class
- [ ] Implement jscpd subprocess wrapper
- [ ] Parse JSON output to violation format
- [ ] Implement Node.js installation check
- [ ] Graceful fallback (prompt or heuristics)
- [ ] Severity mapping logic
- [ ] Generate YAML violation report
- [ ] Integration test with sample code

**Phase 2 (Enhancement)**:
- [ ] Add PMD CPD as alternative
- [ ] Simple heuristic detection (regex patterns)
- [ ] Result caching
- [ ] Performance optimization

**Phase 3 (Optional)**:
- [ ] Custom AST-based implementation
- [ ] Rust/C extension for speed
- [ ] Incremental scanning support

---

## Output Format Example

```yaml
rule_id: DUP-001
severity: HIGH
file: src/models/user.py
start_line: 15
end_line: 35

message: |
  Duplicate code: 21-line block matches src/models/account.py:42-62 (92% similarity)
  Extract to shared function in src/models/base.py

clone_matches:
  - file: src/models/account.py
    line_start: 42
    line_end: 62
    similarity: 92%
  - file: src/models/profile.py
    line_start: 18
    line_end: 38
    similarity: 91%

metadata:
  clone_type: Type 2
  token_count: 187
  match_count: 3

summary:
  total_violations: 12
  critical: 1
  high: 5
  medium: 4
  low: 2
  duplication_percentage: 5.9%
```

---

## Decision Summary

**Primary Choice**: jscpd
- 150+ languages ✓
- Proven algorithm ✓
- Light integration ✓
- Pattern precedent (STORY-115) ✓

**Alternative**: PMD CPD (if Java available)
- Better enterprise features
- Heavier integration (Java dependency)

**Not Suitable**:
- ast-grep (not designed for duplication)
- Semgrep (security tool, not for clones)

**Future Option**:
- Custom AST (Phase 2-3, research effort)

---

## Resources & Links

### Research Report
- Full report: `devforgeai/specs/research/RESEARCH-006-duplicate-code-detection-tools.md`
- Planning file: `.claude/plans/calm-humming-hennessy-agent-aceaaa8.md`

### Documentation
- [jscpd GitHub](https://github.com/kucherenko/jscpd)
- [PMD CPD Docs](https://pmd.github.io/pmd/pmd_userdocs_cpd.html)
- [DECKARD Paper](https://www.cs.ucdavis.edu/~su/publications/icse07.pdf)

### Existing DevForgeAI
- Duplicate rule: `devforgeai/ast-grep/rules/python/anti-patterns/duplicate-code.yml`
- ast-grep validator: `src/claude/scripts/devforgeai_cli/validators/ast_grep_validator.py`
- EPIC-018: `devforgeai/specs/Epics/EPIC-018-astgrep-foundation-core-rules.epic.md`

---

## FAQ

**Q: Why not just use ast-grep for duplication?**
A: ast-grep explicitly not designed for clone detection. See rule AP-009 documentation in codebase.

**Q: Does jscpd require Node.js?**
A: Yes, but can offer fallback options (heuristics or skip). Node.js likely available (npm used for npm package distribution).

**Q: What about Java projects?**
A: jscpd supports Java. If Java-focused, PMD CPD alternative available.

**Q: How accurate is jscpd?**
A: Type 1 (exact): 95%+, Type 2 (renamed vars): 85-90%, Type 3+: decreases. Threshold tuning needed.

**Q: Can we exempt code from detection?**
A: Yes, planned for Phase 1 (DUP-OFF/DUP-ON comments like PMD).

**Q: How fast is jscpd?**
A: Rabin-Karp algorithm O(n), handles 1000+ files in <10 seconds.

---

**Next Step**: Review recommendations with team → Approve architecture → Begin STORY-119/120 implementation

