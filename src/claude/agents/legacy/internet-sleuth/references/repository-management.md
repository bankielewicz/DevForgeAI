# Repository Management for Internet Sleuth

**Version**: 1.0 | **Status**: Reference | **Agent**: internet-sleuth

---

## Repository Organization

```bash
tmp/repos/
├── competitive-analysis/
│   ├── competitor-repo-1/
│   └── competitor-repo-2/
├── technology-trends/
│   ├── framework-repo-1/
│   └── library-repo-2/
├── implementation-patterns/
│   ├── pattern-repo-1/
│   └── pattern-repo-2/
└── validation-frameworks/
    ├── test-framework-repo/
    └── quality-tool-repo/
```

## Research Output Directory

```bash
devforgeai/specs/research/
├── tech-eval-react-patterns-2025-11-17.md
├── pattern-analysis-next-js-2025-11-17.md
├── competitive-vue-vs-react-2025-11-17.md
└── market-intelligence-saas-platforms-2025-11-17.md
```

## Cleanup Strategy

- Maintain organized repository structure by research category
- Clean repositories older than 7 days to manage disk space
- Create summary reports before cleanup to preserve insights
- Archive critical findings in permanent research documentation (`devforgeai/specs/research/`)
- Copy key code examples to research reports before repository removal

## Filename Conventions

- Technology evaluations: `tech-eval-{topic}-{YYYY-MM-DD}.md`
- Pattern analyses: `pattern-analysis-{repo-name}-{YYYY-MM-DD}.md`
- Competitive research: `competitive-{topic}-{YYYY-MM-DD}.md`
- Market intelligence: `market-intelligence-{segment}-{YYYY-MM-DD}.md`
- Use ISO date format: YYYY-MM-DD
- Lowercase kebab-case for topic/repo names

## Output Locations Reference

- **Feasibility research (epic/story-specific):** `devforgeai/specs/research/feasibility/{EPIC-ID}-{timestamp}-research.md`
- **General research (multi-epic):** `devforgeai/specs/research/shared/RESEARCH-{NNN}-{slug}.md`
- **Example reports (documentation):** `devforgeai/specs/research/examples/{example-name}.md`

## Naming Conventions Reference

- Research ID: `RESEARCH-{NNN}` (gap-aware, 3-digit zero-padded)
- Timestamp slug: `YYYY-MM-DD-HHMMSS` (e.g., 2025-11-17-153022)
- Topic slug: `kebab-case` (e.g., oauth2-evaluation, react-patterns)
