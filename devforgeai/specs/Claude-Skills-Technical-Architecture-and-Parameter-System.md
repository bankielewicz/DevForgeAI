# Claude Skills: Technical Architecture and Parameter System

**Skills do NOT accept command parameters or custom runtime parameters.** Skills are **model-invoked** (Claude autonomously decides when to use them) rather than **user-invoked** (like CLI commands). Configuration is entirely static, defined in YAML frontmatter, with user intent conveyed through natural language conversation context.

Claude Skills represent a filesystem-based approach to extending Claude's capabilities through modular, organized folders containing instructions, scripts, and resources. According to Anthropic's engineering team, Skills are "organized folders of instructions, scripts, and resources that agents can discover and load dynamically to perform better at specific tasks." The architecture emphasizes simplicity, composability, and progressive disclosure—revealing information only when needed to minimize token consumption while enabling unlimited complexity through file resources.

## Progressive disclosure powers the architecture

The fundamental design principle that makes Skills scalable is **progressive disclosure**, revealing information in three distinct levels that balance token efficiency with comprehensive functionality.

**Level 1 metadata** (always loaded) consumes just 30-100 tokens per skill. The YAML frontmatter containing `name` and `description` loads at startup into the system prompt, providing just enough information for Claude to determine relevance without overwhelming context. This allows dozens of skills to be available simultaneously.

**Level 2 instructions** (loaded when triggered) typically consume under 5,000 tokens. The main Markdown body of SKILL.md loads only when a skill matches the user's task, providing detailed procedural knowledge and workflow guidance without affecting other conversations.

**Level 3 resources and code** (loaded as needed) have effectively unlimited size since files can be executed without loading into context. Bundled Python scripts, templates, datasets, and documentation are accessed only when specific resources are referenced, with only outputs consuming tokens.

This three-tier system enables skills to include comprehensive documentation and pre-written deterministic code while maintaining token efficiency. A skill can bundle megabytes of reference material that never impacts context unless explicitly needed.

## File structure and SKILL.md format

Every skill is a directory containing at minimum a **SKILL.md** file at the root level. The optional supporting structure includes **scripts/** for executable Python and bash code, **references/** for documentation loaded into context when referenced, and **assets/** for templates, fonts, images, and data files.

The SKILL.md file has a strict two-part structure. Part one is **YAML frontmatter** delimited by `---` markers containing configuration metadata. Part two is **Markdown content** with instructions, examples, and guidelines that Claude follows when the skill is active.

**Required YAML frontmatter parameters:**
- `name`: Maximum 64 characters, lowercase letters/numbers/hyphens only, cannot contain "anthropic" or "claude"
- `description`: Maximum 1024 characters, must describe both what the skill does AND when Claude should use it

**Optional YAML frontmatter parameters:**
- `license`: MIT, Apache, or filename reference
- `allowed-tools`: Array restricting which tools Claude can use (Claude Code only, not supported in API or Claude.ai)
- `metadata`: Custom key-value pairs for versioning, categorization, or other organizational needs

**Critical constraint**: Official Claude.ai validation rejects any frontmatter properties beyond these five fields. Properties like standalone `version` or `dependencies` fields are not officially supported according to GitHub issue #37 in the anthropics/skills repository.

Example minimal skill structure:
```yaml
---
name: safe-file-reader
description: Read files without making changes. Use when you need read-only file access.
allowed-tools: [Read, Grep, Glob]
---

# Safe File Reader
This skill provides read-only file access.

## Instructions
1. Use Read tool to access file contents
2. Use Grep for searching within files
3. Never modify files
```

## Skills as meta-tools, not parameterized functions

The most crucial architectural insight for your DevForgeAI framework: **Skills use a fundamentally different paradigm than traditional tools.** Skills register as a single meta-tool called "Skill" (capital S) that accepts exactly one parameter: `command` (the skill name).

When Claude determines a skill is relevant, it invokes the Skill tool like this:
```json
{
  "type": "tool_use",
  "id": "toolu_01JRBZGD3vy9gDsifuT89L8B",
  "name": "Skill",
  "input": {
    "command": "pdf"
  }
}
```

The system responds by loading SKILL.md content into context. The skill doesn't execute and return—it **injects instructions** that Claude then follows using the conversation context as implicit parameters.

**This means:**
- ❌ Skills CANNOT accept command-line style parameters like `my-skill --param=value`
- ❌ Skills CANNOT receive user-provided custom input at invocation time
- ❌ No runtime configuration or parameterization exists
- ✅ All "parameters" are conveyed through natural language in the conversation
- ✅ Configuration is entirely static, defined in YAML frontmatter
- ✅ Claude interprets user intent from conversation context and applies skill instructions

Traditional tools execute and return results. Skills load instructions and continue. Traditional tools accept runtime arguments. Skills use static config plus conversation context. This prompt-based context injection paradigm maximizes flexibility while keeping architecture simple and LLM-friendly.

## Discovery and invocation mechanism

Skills become available through an elegant discovery process. At startup, all installed skill metadata (name + description) embeds in the Skill tool's description as an `<available_skills>` list. Claude reads this list and when a user request matches a skill's description, it invokes the Skill tool with the appropriate skill name.

The description field is **critical for discovery**—it must clearly articulate both what the skill does and when Claude should use it. Vague descriptions cause false negatives (skill not invoked when needed) or false positives (skill invoked inappropriately). Best practice: be specific about capabilities and use cases.

Skills can automatically compose together for complex tasks. Claude can identify and coordinate multiple relevant skills without manual intervention, though the maximum is 8 skills per API request.

## API integration and configuration

Skills integrate through the Messages API using the `container` parameter:

```python
import anthropic

client = anthropic.Anthropic()
response = client.beta.messages.create(
    model="claude-sonnet-4-5-20250929",
    max_tokens=4096,
    betas=["code-execution-2025-08-25", "skills-2025-10-02"],
    container={
        "skills": [
            {
                "type": "anthropic",        # Pre-built skills
                "skill_id": "pptx",         # Short name
                "version": "latest"         # Or date like "20251002"
            },
            {
                "type": "custom",           # User-created skills
                "skill_id": "skill_01AbCdEfGhIjKlMnOpQrStUv",
                "version": "1759178010641129"  # Epoch timestamp
            }
        ]
    },
    messages=[{
        "role": "user",
        "content": "Create a presentation about renewable energy"
    }],
    tools=[{
        "type": "code_execution_20250825"
    }]
)
```

**API requirements:**
- Code Execution Tool must be enabled
- Three beta headers required: `code-execution-2025-08-25`, `skills-2025-10-02`, `files-api-2025-04-14`
- Maximum 8 skills per request
- Maximum 8MB total upload size for all skill files combined

**Skill management endpoints:**
- `POST /v1/skills` - Create a skill
- `GET /v1/skills` - List all skills
- `GET /v1/skills/{skill_id}` - Get specific skill details
- `DELETE /v1/skills/{skill_id}` - Delete a skill
- `POST /v1/skills/{skill_id}/versions` - Create new version
- `GET /v1/skills/{skill_id}/versions` - List all versions
- `DELETE /v1/skills/{skill_id}/versions/{version}` - Delete specific version

Skills uploaded via API are **workspace-wide**, available to all workspace members. This differs from Claude.ai where custom skills are individual per user.

## Claude Code terminal integration

For your DevForgeAI framework targeting Claude Code terminal, skills automatically load from three locations:

**Personal skills**: `~/.claude/skills/` directory contains skills available across all projects for the individual user.

**Project skills**: `.claude/skills/` directory at project root contains skills shared with the team via version control (git). This is the recommended approach for team collaboration.

**Plugin skills**: Automatically available when plugins are installed from the marketplace.

Installation via plugin marketplace:
```bash
# Add the official skills marketplace
/plugin marketplace add anthropics/skills

# Install skill collections
/plugin install document-skills@anthropic-agent-skills
/plugin install example-skills@anthropic-agent-skills
```

Skills in Claude Code are **model-invoked** (Claude decides when to use them automatically) as opposed to **slash commands** which are user-invoked (you type `/command`). Skills activate based on conversation context—you don't manually trigger them, though you can reference them directly: "Use the PDF skill to extract form fields from file.pdf."

The execution environment is a code execution container (virtual machine) where Claude has filesystem access to `/skills/{directory}/`, can execute bash commands and Python scripts, but has **no network access** and **no data persistence** between sessions. Each request gets a fresh isolated container.

## Pre-built Anthropic skills

Four official pre-built skills ship with Claude on all paying plans:

**pptx (PowerPoint)**: Creates presentations, edits slides, analyzes content with support for charts, images, and formatting.

**xlsx (Excel)**: Creates spreadsheets, analyzes data, generates reports with charts and pivot tables.

**docx (Word)**: Creates documents, edits content, applies formatting and styles.

**pdf**: Generates formatted PDF documents and reports, extracts text and form fields.

These skills use short names (`pptx`, `xlsx`, `docx`, `pdf`) and date-based versions (`20251002` or `latest`). They're maintained by Anthropic and available automatically—no setup required.

## The allowed-tools parameter for security

The `allowed-tools` parameter in YAML frontmatter restricts which tools Claude can use when a skill is active, providing permission scoping for security-sensitive workflows:

```yaml
---
name: safe-file-reader
description: Read files without making changes
allowed-tools: [Read, Grep, Glob]
---
```

**Important limitations:**
- Supported in **Claude Code only** (not Claude.ai or API)
- Parsed from frontmatter but enforcement happens at agent/harness level
- Values must match exact tool names available in the environment

This enables read-only skills that prevent file modifications, or analysis skills that prevent code execution. For DevForgeAI, you could create skills with carefully scoped permissions based on workflow requirements.

## Runtime environment constraints

The code execution container has specific constraints affecting skill design:

**No network access**: Skills cannot make external API calls or fetch remote resources. Use MCP (Model Context Protocol) connections instead for external service access.

**No runtime package installation (API only)**: API environment has pre-installed packages only. Claude.ai and Claude Code can install packages on-demand during execution.

**Isolated container per request**: No data persists between sessions. Each API call or conversation turn gets a fresh environment.

**Maximum upload size**: 8MB combined for all skill files. Large datasets should be referenced externally or loaded on-demand.

## Security considerations for DevForgeAI

Anthropic recommends treating skills like software installation—only use skills from trusted sources (self-created or from Anthropic). **Potential risks include:**

**Prompt injection**: Malicious skill content could inject instructions causing unintended actions.

**Code execution access**: Skills can execute arbitrary code with filesystem access in the container.

**Third-party packages**: Skills in Claude.ai/Code can install packages, introducing supply chain risks.

**Mitigations for your framework:**
- Audit all skill content thoroughly before deployment
- Review code dependencies and any network operations
- Never hardcode secrets or credentials in skills
- Use version pinning for production (`"version": "1759178010641129"` not `"latest"`)
- Test skills in isolated environments first

## How parameters flow through conversation context

Since skills don't accept traditional parameters, understanding implicit parameter flow is crucial for DevForgeAI design:

1. **User message becomes implicit input**: "Extract text from report.pdf" → filename and intent are in conversation
2. **Skill description matches intent**: PDF skill's description mentions "extracting text from PDFs"
3. **Claude invokes skill**: Loads SKILL.md instructions into context
4. **Instructions reference conversation**: "Use the filename the user provided in their message..."
5. **Claude executes workflow**: Applies instructions to conversation context with user's implicit parameters

This means your DevForgeAI skills should write instructions that guide Claude to extract needed information from the conversation. Rather than defining parameters like `function(filename, format)`, write instructions like: "Read the filename from the user's request. Determine their desired output format from context clues. Then execute the appropriate conversion script."

## Comparison: Skills vs. MCP vs. Custom Instructions

**Skills** provide procedural knowledge for completing specific tasks. They're reusable, automatically loaded when relevant, and survive across sessions. Token cost is minimal until used (30-100 tokens for metadata).

**MCP (Model Context Protocol)** connects Claude to external services and data sources. It provides real-time data access and tool integration. Skills and MCP complement each other: use MCP for tool access, skills for workflow instructions.

**Custom Instructions** apply broadly to all conversations but lack task-specific targeting. Skills are superior for specialized workflows since they load only when relevant and can include executable code and resources.

For DevForgeAI, the optimal pattern is likely: **MCP connections for external tools + Skills for framework-specific workflows + Project skills in `.claude/skills/` for team sharing.**

## Metadata field for organizational needs

The `metadata` field accepts custom key-value pairs for organizational purposes:

```yaml
---
name: brand-guidelines
description: Apply Acme Corp brand guidelines to presentations and documents
metadata:
  version: "2.1.0"
  author: "marketing-team"
  category: "design"
  framework: "DevForgeAI"
---
```

**Key characteristics:**
- ✅ Readable by clients and tools via API
- ✅ Useful for versioning, categorization, filtering
- ✅ Any reasonable key names (avoid conflicts)
- ❌ NOT accessible to Claude during skill execution
- ❌ NOT runtime-configurable
- ❌ Values must be strings

For DevForgeAI, you could use metadata to track skill compatibility versions, categorize skills by development phase, or mark skills as belonging to your framework ecosystem.

## Practical implications for DevForgeAI development

Based on this technical research, recommendations for your DevForgeAI framework:

**Design skills as instruction sets, not functions**: Write SKILL.md files that guide Claude through workflows rather than expecting parameterized function calls. Use conversation context as the "parameter passing" mechanism.

**Leverage project skills for team sharing**: Place your DevForgeAI skills in `.claude/skills/` at project root and commit to version control. This makes skills available to all team members automatically.

**Use metadata for framework tracking**: Tag skills with `metadata.framework: "DevForgeAI"` to identify framework-specific skills programmatically.

**Create focused, single-purpose skills**: Each skill should have one clear objective. Use skill composition for complex workflows rather than building monolithic skills.

**Write excellent descriptions**: The description field determines when Claude uses your skill. Be specific about capabilities and use cases. Test that descriptions trigger appropriately.

**Bundle executable scripts**: For deterministic operations (parsing config files, running build steps, etc.), include Python scripts in `scripts/` directory. These execute without consuming context tokens.

**Consider allowed-tools for safety**: For production workflows, restrict tool access using `allowed-tools` to prevent unintended modifications.

**Version skills carefully**: Use semantic versioning in metadata and pin specific versions for production API usage. Development can use `"latest"`.

## Conclusion

Claude Skills represent a paradigm shift from traditional parameterized tools to prompt-based context injection. The architecture prioritizes simplicity, token efficiency, and composability through progressive disclosure—revealing information only when needed across three distinct levels. For DevForgeAI, this means designing skills as instruction sets that guide Claude through workflows rather than as functions accepting parameters. User intent flows through natural language conversation context, with skills providing the procedural knowledge to accomplish tasks. The filesystem-based structure, version control integration through `.claude/skills/`, and automatic composition capabilities make Skills particularly powerful for team-based development frameworks like yours. Understanding that skills are model-invoked rather than user-invoked, and that all configuration is static, is crucial for effective framework design.