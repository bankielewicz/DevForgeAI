# Anti-Pattern Scanner: Metrics & Performance Reference

**Purpose:** Token efficiency metrics, savings data, and performance targets for the anti-pattern-scanner subagent.

**Loaded by:** `Read(file_path=".claude/agents/anti-pattern-scanner/references/metrics-reference.md")`

---

## Token Efficiency

### Token Savings with Context Summaries

| Invocation Method | Token Usage | Savings |
|-------------------|-------------|---------|
| Full context files (6 reads) | ~8K tokens | Baseline |
| Subagent (reads own context) | ~3K tokens | -5K (62%) |
| **With context summary** | ~0.5K tokens | **-7.5K (94%)** |

**Per-subagent savings:** ~3K tokens when using context summaries vs re-reading files.

**Aggregate savings (3 parallel validators):** ~9K tokens per QA validation cycle.

**Target (STORY-180):** -3K tokens per subagent call - **ACHIEVED** with context summary pattern.

---

## Performance Targets

**Execution Time:**
- Small projects (<100 files): <5 seconds
- Medium projects (100-500 files): <15 seconds
- Large projects (>500 files): <30 seconds

**Token Usage:** ~3K tokens per invocation (vs ~8K inline pattern matching)
