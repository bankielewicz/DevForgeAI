# Document Command - Help & Reference

**Source:** Extracted from `/document` command for lean orchestration compliance (STORY-461)

---

## Quick Reference

```bash
# Generate docs for specific story
/document STORY-040

# Generate specific documentation type
/document --type=readme
/document --type=api
/document --type=architecture
/document --type=roadmap

# Brownfield analysis
/document --mode=brownfield --analyze

# Export formats
/document --export=html
/document --export=pdf

# Generate all documentation
/document --type=all

# List available templates
/document --list-templates
```

### Documentation Audit

```bash
# Audit documentation quality (generates findings file)
/document --audit=dryrun

# Fix all findings from audit
/document --audit-fix --type=all

# Fix by category
/document --audit-fix --type=license        # License files only
/document --audit-fix --type=community      # CONTRIBUTING, SECURITY, CODE_OF_CONDUCT, templates
/document --audit-fix --type=tone           # README opening, FAQ warmth, human voice
/document --audit-fix --type=architecture   # Duplicates, navigation, orphans, scope banners
/document --audit-fix --type=formatting     # Admonitions, badges, CHANGELOG, oversized files
/document --audit-fix --type=onboarding     # Quick Start, MSRV, prerequisites

# Fix a single finding
/document --audit-fix --finding=F-003
```

**Workflow:** Run `--audit=dryrun` first to generate `devforgeai/qa/audit/doc-audit.json`, then `--audit-fix` to apply fixes from that file.

---

## Audit Finding Types

| Type Key | What It Detects |
|----------|----------------|
| `license` | Missing LICENSE files, Cargo.toml license field |
| `community` | Missing CONTRIBUTING, SECURITY, CODE_OF_CONDUCT, issue/PR templates |
| `tone` | Dry openings, gatekeeping language, missing human voice, clinical troubleshooting |
| `architecture` | Duplicate files, scope confusion, missing navigation, orphaned files |
| `formatting` | Missing admonitions/badges, flat CHANGELOG, oversized files, table walls |
| `onboarding` | Missing Quick Start, prerequisite mismatches, MSRV inconsistencies |
| `all` | Everything above |

---

## Available Templates

| Template | Description |
|----------|-------------|
| readme | Project overview, installation, quick start |
| developer-guide | Architecture, development workflow |
| api | API reference, endpoints, schemas |
| troubleshooting | Common issues, solutions |
| contributing | Contribution guidelines, PR process |
| changelog | Version history, release notes |
| architecture | System design, diagrams, ADRs |

---

## Display Results Format

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  Documentation Generated Successfully
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Files Created/Updated:
  ✓ {file.path}
    Type: {file.type}
    Words: {file.word_count}
    Coverage: {file.coverage}%

Diagrams Generated:
  ✓ {diagram.path}
    Type: {diagram.type}
    Components: {diagram.component_count}

Overall Documentation Coverage: {result.overall_coverage}%
  ✅ Meets release quality gate (≥80%)
  OR
  ⚠️ Below release threshold (≥80%)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## Next Steps

- Review generated documentation
- Run `/qa {STORY_ID}` if story-based
- Customize with project-specific details
- Add documentation for undocumented items if coverage < 80%

---

## Error Handling Details

**Invalid Story ID:** Story not found - list available stories, display usage
**Context Files Missing:** Run `/create-context` first
**No Completed Stories (greenfield):** Suggest brownfield mode or wait for completion
**Export Dependencies Missing:** PDF requires pandoc/wkhtmltopdf, fallback to Markdown
**Coverage Below Threshold:** List undocumented APIs, suggest fixes

---

## Success Criteria

- Documentation files created/updated
- Coverage ≥80% (if quality gate mode)
- All diagrams render correctly
- Story file updated (if story-based)
- Export formats created (if requested)

---

## Integration

**Invoked by:** Users, `/release` command (quality gate), `/orchestrate` (after QA)
**Invokes:** `devforgeai-documentation` skill
**Updates:** Documentation files, story files, CHANGELOG.md

---

## Performance

| Component | Tokens |
|-----------|--------|
| Command overhead | ~3K |
| Skill execution (isolated) | ~50K |
| Total main conversation | ~3K |

**Execution Time:** Greenfield <2 min, Brownfield <10 min, Architecture diagrams <30s, Incremental <1 min
