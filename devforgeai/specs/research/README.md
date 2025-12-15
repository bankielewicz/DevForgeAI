# DevForgeAI Research Directory

**Purpose:** Centralized storage for internet-sleuth agent research reports, supporting evidence-based decision-making throughout the development lifecycle.

---

## Directory Structure

```
.devforgeai/research/
├── feasibility/        # Feasibility analysis reports (ideation Phase 5)
├── examples/           # Example research reports (documentation/templates)
├── shared/             # Multi-epic/multi-story research (reusable across epics)
├── cache/              # Partial research results (resumable operations)
└── logs/               # Research operation logs (30-day retention)
```

---

## Directory Purposes

### `/feasibility/`
**Purpose:** Store feasibility analysis research reports generated during devforgeai-ideation Phase 5.

**File Naming Convention:** `{EPIC-ID}-{timestamp}-research.md`
- Example: `EPIC-007-2025-11-17-143022-research.md`

**Content:** Technical feasibility scores (0-10), market viability evidence, competitive landscape, risk factors.

**Retention:** Keep all reports (linked from epic files via YAML frontmatter).

---

### `/examples/`
**Purpose:** Example research reports demonstrating integration patterns, quality standards, and report structures.

**Files (Required):**
- `technology-evaluation-example.md` - Comparative technology analysis with ADR-ready evidence
- `competitive-analysis-example.md` - Market research with feasibility implications
- `repository-archaeology-example.md` - Implementation pattern mining with code examples

**Usage:** Reference templates for new research reports, onboarding documentation.

**Retention:** Permanent (framework documentation).

---

### `/shared/`
**Purpose:** Research reports relevant to multiple epics or stories (cross-cutting concerns).

**File Naming Convention:** `RESEARCH-{NNN}-{slug}.md`
- Example: `RESEARCH-001-graphql-evaluation.md`

**Linking:** Epic/story files reference via YAML frontmatter:
```yaml
research_references:
  - RESEARCH-001
  - RESEARCH-003
```

**Retention:** Keep all reports (may be referenced by future epics/stories).

---

### `/cache/`
**Purpose:** Partial research results for resumable operations (failure recovery).

**File Naming Convention:** `{research_id}-partial.json`
- Example: `RESEARCH-001-partial.json`

**Content:** JSON format with completed sections, checkpoint markers, Perplexity API state.

**Retention:** 7 days (auto-delete after research completes or expires).

**Cleanup:**
```bash
# Delete cache files older than 7 days
find .devforgeai/research/cache/ -name "*.json" -mtime +7 -delete
```

---

### `/logs/`
**Purpose:** Research operation logs for monitoring, debugging, and performance analysis.

**File Naming Convention:** `{YYYY-MM-DD}-research.log`
- Example: `2025-11-17-research.log`

**Log Format:**
```
[2025-11-17 14:30:22] INFO: Research operation started (RESEARCH-001, mode: repository-archaeology)
[2025-11-17 14:32:15] INFO: Perplexity API call completed (status: 200, duration: 1.8s)
[2025-11-17 14:35:40] INFO: Research operation completed (RESEARCH-001, duration: 5m18s)
```

**Retention:** 30 days active, monthly archival to `/logs/archive/`.

**Cleanup:**
```bash
# Archive logs older than 30 days
mkdir -p .devforgeai/research/logs/archive/
find .devforgeai/research/logs/ -maxdepth 1 -name "*.log" -mtime +30 -exec mv {} .devforgeai/research/logs/archive/ \;
```

---

## Research ID Assignment

**Pattern:** Gap-aware ID assignment (fills gaps before incrementing).

**Algorithm:**
1. Glob existing research IDs: `RESEARCH-001, RESEARCH-003, RESEARCH-005`
2. Identify gaps: `RESEARCH-002, RESEARCH-004`
3. Assign next ID: `RESEARCH-002` (lowest gap)
4. If no gaps: Increment highest ID → `RESEARCH-006`

**Example:**
```python
import glob
import re

def get_next_research_id():
    existing = glob.glob('.devforgeai/research/shared/RESEARCH-*.md')
    ids = sorted([int(re.search(r'RESEARCH-(\d+)', f).group(1)) for f in existing])

    # Find gaps
    for i in range(1, max(ids) + 1):
        if i not in ids:
            return f"RESEARCH-{i:03d}"

    # No gaps, increment
    return f"RESEARCH-{max(ids) + 1:03d}" if ids else "RESEARCH-001"
```

---

## Archival Policy

**Trigger:** Reports >6 months old with no recent epic/story references.

**Process:**
1. Move to `.devforgeai/research/archive/{YYYY}/`
2. Update epic/story YAML frontmatter (mark as archived)
3. Keep archive/ out of main search paths

**Retention:** Archive indefinitely (disk space permitting).

**Restoration:** Copy archived reports back to shared/ if needed.

---

## Quality Standards

All research reports must:
- ✅ Follow `research-report-template.md` structure
- ✅ Include YAML frontmatter with required fields
- ✅ Validate against all 6 context files (quality gate)
- ✅ Include workflow state metadata
- ✅ Provide evidence URLs (HTTPS only)
- ✅ Pass completeness validation (all 9 sections present)

---

## Integration Points

**Invoked by:**
- devforgeai-ideation (Phase 5: Feasibility Analysis)
- devforgeai-architecture (Phase 2: Technology Selection)
- internet-sleuth agent (all research modes)

**Outputs to:**
- `.devforgeai/research/feasibility/` (ideation research)
- `.devforgeai/research/shared/` (multi-epic research)
- Epic/story files (YAML frontmatter references)

---

## Monitoring

**Track:**
- Research completion rate (% of operations completing successfully)
- Average operation duration by mode (discovery, investigation, repository-archaeology, etc.)
- Perplexity API retry frequency (target: <10% of calls)
- Cache hit rate (partial result recovery)

**Alert on:**
- Consistent Perplexity API failures (>50% retry rate)
- Research operations exceeding p95 duration thresholds
- Cache corruption (partial results unrecoverable)

---

## Related Documentation

- `research-report-template.md` - Standard report structure
- `research-principles.md` - Core research methodology
- `.claude/agents/internet-sleuth.md` - Agent implementation
- `.claude/skills/devforgeai-ideation/SKILL.md` - Ideation integration
- `.claude/skills/devforgeai-architecture/SKILL.md` - Architecture integration

---

**Created:** 2025-11-17
**Version:** 1.0
**Maintainer:** DevForgeAI Framework
