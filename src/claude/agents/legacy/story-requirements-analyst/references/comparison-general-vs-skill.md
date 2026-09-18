## Comparison: General-Purpose vs. Skill-Specific

| Aspect | requirements-analyst (General) | story-requirements-analyst (Skill-Specific) |
|--------|-------------------------------|-------------------------------------------|
| **Location** | `.claude/agents/requirements-analyst.md` | `.claude/agents/story-requirements-analyst.md` |
| **Purpose** | Requirements for ANY context | Requirements ONLY for story creation |
| **Tools** | Read, Write, Edit, Grep, Glob, AskUserQuestion | Read, Grep, Glob, AskUserQuestion (NO Write/Edit) |
| **Optimization** | Completeness (comprehensive deliverables) | Integration (content for assembly) |
| **Output** | May create 6 files (story + 5 supporting) | ONLY markdown text (no files) |
| **Used by** | Multiple skills (story, epic, architecture) | ONLY spec-driven-stories |
| **File creation** | Possible (has Write/Edit tools) | IMPOSSIBLE (no Write/Edit tools) |
| **Contract** | None (general-purpose) | requirements-analyst-contract.yaml |
| **Parent skill** | None specified | spec-driven-stories (documented) |
| **Model** | haiku | sonnet |

**Key architectural difference:** Skill-specific subagent CANNOT create files even if it wanted to (Write/Edit tools not available).

---

For RCA-007 compliance documentation, load: `references/rca-007-compliance.md`
---

For quality check procedures and success criteria, load: `references/quality-checks.md`
