# ADR-001: Use Markdown for All Framework Documentation

**Date**: 2025-10-30
**Status**: Accepted
**Deciders**: Framework Architect

## Context

DevForgeAI framework needs a documentation format for skills, subagents, slash commands, and context files. The framework must work across all programming languages and technology stacks, requiring a language-agnostic approach.

Three primary options exist:
1. **Markdown** - Natural language format with light structure
2. **JSON/YAML** - Structured data formats
3. **Mixed approach** - Different formats for different components

Claude Code Terminal can interpret multiple formats, but the optimal choice affects:
- Token efficiency (how much context budget is consumed)
- Claude's ability to understand and execute instructions
- Framework maintainability and readability
- Cross-language compatibility

## Decision

We will use **Markdown as the primary documentation format** for all framework components:
- Skills (SKILL.md files)
- Subagents (.md files)
- Slash commands (.md files)
- Context files (tech-stack.md, source-tree.md, etc.)
- ADRs (this file)
- Reference documentation

**YAML frontmatter** will be used exclusively for metadata (name, description, tools, model).

**JSON** will be used only for structured data exchange where necessary (not documentation).

## Rationale

### 1. Claude's Natural Language Processing

**Research Evidence**: Claude interprets natural language (Markdown) significantly better than structured formats.

From official Claude Code documentation:
> "Keep formats close to what the model has seen naturally occurring in text on the internet"

Markdown is ubiquitous in:
- GitHub repositories
- Stack Overflow answers
- Technical documentation
- API documentation
- README files

Claude has seen millions of Markdown documents during training, making interpretation more accurate.

### 2. Token Efficiency with Progressive Disclosure

**Research Evidence**: Community implementations show 60-80% token savings with Markdown + progressive disclosure.

Pattern:
```markdown
# Main Instructions (500 lines)
For detailed guidance, see references/deep-dive.md

# references/deep-dive.md (1,000 lines, loaded on demand)
```

This allows main files to remain concise while providing deep documentation when needed.

**Comparison**:
- JSON spec (all inline): ~40,000 tokens
- Markdown (main + references): ~10,000 tokens typical, ~35,000 tokens when references loaded

### 3. Readability and Maintainability

Markdown is human-readable without tooling:
- Developers can read .md files in any editor
- Git diffs are comprehensible
- No parsing required for manual review
- Supports inline code examples with syntax highlighting

JSON/YAML require:
- Careful escaping of special characters
- Harder to read multi-line content
- Difficult to include formatted examples
- Easy to introduce syntax errors

### 4. Framework Agnosticism

Markdown has no language-specific constructs:
- No imports or dependencies
- No language keywords
- Pure documentation
- Works equally well for C#, Python, JavaScript, Go, Java, Rust

This aligns with DevForgeAI's core principle of framework-agnostic design.

### 5. Community Best Practices

**Production implementations validate this choice**:

**Pimzino's claude-code-spec-workflow** (1,000+ downloads):
- All components in Markdown
- YAML frontmatter for metadata only
- Reference files for deep documentation

**julibuilds/claude-code-workflow** (58 commands):
- Pure Markdown commands
- No JSON/YAML for instructions
- Achieved 70% debugging time reduction

**OneRedOak's production AI startup**:
- Markdown for all agent prompts
- "Bullet points rather than narrative paragraphs"
- Successful elimination of years of technical debt

### 6. Examples vs Structured Data

**Markdown excels at examples**:

```markdown
✅ CORRECT:
Use Read(file_path="story.md")

❌ FORBIDDEN:
Use Bash(command="cat story.md")
```

**JSON would require**:
```json
{
  "examples": [
    {
      "correct": "Use Read(file_path=\"story.md\")",
      "forbidden": "Use Bash(command=\"cat story.md\")",
      "rationale": "40-73% token efficiency"
    }
  ]
}
```

The Markdown version is:
- More readable
- Easier to maintain
- Uses fewer tokens
- Requires no escaping

## Consequences

### Positive

1. **Superior Token Efficiency**: 60-80% reduction with progressive disclosure
2. **Better Claude Understanding**: Natural language interpretation
3. **Improved Maintainability**: Human-readable without tooling
4. **Framework Agnostic**: No language-specific constructs
5. **Community Alignment**: Matches proven production patterns
6. **Git-Friendly**: Clear diffs, easy code review
7. **Tooling Independence**: Works with any text editor
8. **Example-Rich**: Easy to show correct/incorrect patterns

### Negative

1. **Less Structured**: No schema validation for Markdown content
2. **Potential Inconsistency**: Writers could use different styles
3. **No Type Safety**: Can't enforce field types like JSON schema
4. **Parser Complexity**: If programmatic parsing needed later

### Mitigations for Negatives

1. **Structured sections**: Use consistent heading hierarchy
2. **Style guide**: Establish patterns in coding-standards.md
3. **YAML frontmatter**: Structured metadata where needed
4. **Templates**: Provide reference templates for consistency
5. **Code review**: Enforce patterns through review process

## Alternatives Considered

### Alternative 1: JSON for Configuration, Markdown for Documentation

**Rejected because**:
- Adds complexity (two formats to maintain)
- JSON not significantly better for metadata
- YAML frontmatter provides structure where needed
- Splitting formats reduces cohesion

### Alternative 2: Pure YAML

**Rejected because**:
- YAML's multiline strings are awkward for long content
- Indentation errors are common
- Less readable than Markdown
- Claude interprets natural language better
- Not optimal for examples and instructions

### Alternative 3: Mixed Format Per Component Type

**Rejected because**:
- Inconsistency complicates framework
- Developers would need to learn multiple formats
- No clear benefit to justify complexity
- Research shows Markdown works for all component types

## Implementation

### Phase 1: Core Components (Complete)
- ✅ Skills use Markdown with YAML frontmatter
- ✅ Subagents use Markdown with YAML frontmatter
- ✅ Commands use Markdown with YAML frontmatter
- ✅ Context files use pure Markdown

### Phase 2: Templates and Guides (In Progress)
- Create Markdown templates for each component type
- Document style guide in coding-standards.md
- Provide examples of correct patterns

### Phase 3: Migration Tools (Future)
- If needed, create validators for Markdown structure
- Develop linters for style consistency
- Build generators for common patterns

## Enforcement

**This decision is LOCKED in**:
- `.devforgeai/context/tech-stack.md` - Documents Markdown requirement
- `.devforgeai/context/coding-standards.md` - Markdown style guide
- `.devforgeai/context/anti-patterns.md` - Forbids JSON/YAML for documentation

**Quality gates check**:
- All skills have SKILL.md (not SKILL.json)
- All context files use .md extension
- No JSON/YAML files for instructions (metadata only)

## References

- [Claude Code Documentation - Slash Commands](https://docs.claude.com/en/docs/claude-code/slash-commands)
- [Native Tools vs Bash Efficiency Analysis](.ai_docs/Terminal/native-tools-vs-bash-efficiency-analysis.md)
- [Slash Commands Best Practices](.ai_docs/Terminal/slash-commands-best-practices.md)
- [Framework Workflows Research](.ai_docs/Workflows.md)
- Community implementations: Pimzino/claude-code-spec-workflow, julibuilds/claude-code-workflow

## Revision History

- **2025-10-30**: Initial decision - Markdown for all documentation
