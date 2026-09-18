# Documentation Audit Workflow Reference

## Overview

The documentation audit scores a project's documentation across 4 dimensions, each scored 1-10. The total score (out of 40) provides a DevEx quality benchmark.

## Scoring Rubric

### Dimension 1: Tone & Personality (0-10)

| Score Range | Criteria |
|-------------|----------|
| 0-2 | No README or purely technical with no human voice |
| 3-4 | README exists but opens with WHAT not WHY, no pronouns |
| 5-6 | Has value proposition, some human voice |
| 7-8 | Strong WHY opening, empathetic troubleshooting, welcoming contributor language |
| 9-10 | Consistent human voice throughout, audience-aware tone, exemplary contributor experience |

**Evidence checklist:**
- [ ] README opens with WHY (value proposition / elevator pitch)
- [ ] Uses human pronouns (we/you/your/our)
- [ ] CONTRIBUTING.md uses welcoming language
- [ ] Troubleshooting uses empathetic phrasing ("if you see", "this usually means")

### Dimension 2: Information Architecture (0-10)

| Score Range | Criteria |
|-------------|----------|
| 0-2 | No organization, all in one file, no cross-references |
| 3-4 | Basic file structure but no navigation index, no routing |
| 5-6 | Navigation index exists, some cross-references |
| 7-8 | Audience-based routing, comprehensive cross-references, no duplicates |
| 9-10 | Perfect navigation hierarchy, progressive disclosure, topic-based grouping |

**Evidence checklist:**
- [ ] No duplicate filenames across directories
- [ ] docs/README.md or docs/index.md navigation index exists
- [ ] Cross-references between related docs
- [ ] Audience-based routing (users/developers/contributors)
- [ ] No over-documented modules (>3 files for one topic)
- [ ] No scope confusion (mixed versions/products)

### Dimension 3: Visual Design & Formatting (0-10)

| Score Range | Criteria |
|-------------|----------|
| 0-2 | Plain text only, no formatting enhancements |
| 3-4 | Basic markdown formatting, no admonitions or badges |
| 5-6 | Some GFM admonitions, basic badges |
| 7-8 | Comprehensive admonitions, badges, Keep a Changelog, no oversized files |
| 9-10 | Excellent visual hierarchy, diagrams, tables with grouping, consistent formatting |

**Evidence checklist:**
- [ ] GFM admonitions used (> [!NOTE], > [!WARNING], etc.)
- [ ] README badges present (>= 2)
- [ ] CHANGELOG uses Keep a Changelog categories
- [ ] No oversized files (>50KB)
- [ ] Tables with >10 rows have visual grouping

### Dimension 4: Onboarding Friction (0-10)

| Score Range | Criteria |
|-------------|----------|
| 0-2 | No install instructions, no LICENSE |
| 3-4 | Install steps exist but not in first 50 lines, no quick start |
| 5-6 | Install steps within first 50 lines, LICENSE present |
| 7-8 | Quick start narrative, prerequisites consistent, version matches manifest |
| 9-10 | Zero friction: copy-paste install, quick start in <2 min, consistent versions everywhere |

**Evidence checklist:**
- [ ] Install steps in first 50 lines of README
- [ ] Quick Start or Getting Started section
- [ ] Prerequisites listed
- [ ] LICENSE file present
- [ ] MSRV/version consistent with manifest

## Orphan Detection Algorithm

An "orphaned" file is a documentation file that no other file links to.

```
1. Build reference graph:
   FOR each doc in filtered_docs:
       Extract all markdown links: [text](path) and [text][ref]
       Resolve relative paths to absolute
       Add edge: linked_file <- current_doc

2. Identify entry points (immune from orphan detection):
   - README.md
   - docs/README.md
   - docs/index.md
   - CHANGELOG.md

3. Find orphans:
   FOR each doc not in entry_points:
       IF no inbound edges in reference graph:
           Mark as orphan

4. Report orphans with their directory context
```

## Severity Classification

| Severity | Point Impact | Examples |
|----------|-------------|----------|
| CRITICAL | -3 | Missing LICENSE, no README, broken entry point |
| HIGH | -2 | Missing install steps, no Quick Start, broken cross-refs |
| MEDIUM | -1 | Aspirational language, missing badges, inconsistent versions |
| LOW | -0.5 | Orphaned files, missing admonitions, minor formatting |

## Finding Type Taxonomy

| Type Prefix | Category | Examples |
|-------------|----------|----------|
| `tone:` | Tone & Personality | `tone:no_why`, `tone:no_pronouns`, `tone:gatekeeping` |
| `architecture:` | Information Architecture | `architecture:orphan`, `architecture:duplicate`, `architecture:no_index` |
| `formatting:` | Visual Design | `formatting:missing_badges`, `formatting:oversized`, `formatting:no_admonitions` |
| `onboarding:` | Onboarding Friction | `onboarding:no_install`, `onboarding:no_quickstart`, `onboarding:config_mismatch` |
| `license:` | License/Legal | `license:missing`, `license:mismatch` |
| `community:` | Community Files | `community:contributing`, `community:security`, `community:coc` |
