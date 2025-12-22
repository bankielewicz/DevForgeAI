# DevForgeAI Documentation Skill

**Automated documentation generation integrated into your software development lifecycle (SDLC).**

**Version:** 1.0.0
**Status:** Production Ready (QA Approved)
**Framework:** DevForgeAI Spec-Driven Development

---

## Table of Contents

1. [Overview](#overview)
2. [Features](#features)
3. [Installation and Setup](#installation-and-setup)
4. [Quick Start](#quick-start)
5. [Command Reference](#command-reference)
6. [Documentation Templates](#documentation-templates)
7. [Workflows](#workflows)
8. [Architecture](#architecture)
9. [Quality Gates](#quality-gates)
10. [Advanced Usage](#advanced-usage)
11. [Troubleshooting](#troubleshooting)
12. [Next Steps](#next-steps)

---

## Overview

The **DevForgeAI Documentation Skill** automates comprehensive documentation generation for your projects. It eliminates manual effort by generating README files, API documentation, architecture diagrams, troubleshooting guides, and more—directly from your completed stories or codebase analysis.

### Why This Skill?

Documentation is often the last thing developers write, and the first thing to drift out of sync. The DevForgeAI Documentation Skill solves this by:

- **Automating generation** from your spec-driven stories and codebase
- **Maintaining consistency** through enforced templates and coding standards
- **Ensuring quality** with 80% documentation coverage requirements
- **Integrating with SDLC** as a quality gate before release
- **Supporting multiple modes** for greenfield (new projects) and brownfield (existing codebases)

### What Gets Generated

The skill can generate 8 types of documentation:

1. **README.md** - Project overview, installation, quick start guide
2. **Developer Guide** - Architecture, development workflow, coding conventions
3. **API Documentation** - Endpoint reference, request/response schemas, examples
4. **Architecture Diagrams** - System design, component relationships, data flow (Mermaid)
5. **Troubleshooting Guide** - Common issues, solutions, debugging tips
6. **Contributing Guide** - Contribution workflow, PR process, standards
7. **Changelog** - Version history, release notes, breaking changes
8. **Roadmap** - Feature timeline, milestones, release targets

---

## Features

### Greenfield Documentation (Story-Based)

Generate documentation directly from your completed user stories and technical specifications:

- Extracts features from acceptance criteria
- Pulls API specifications from technical requirements
- Creates diagrams from architecture patterns
- Includes code examples from implementations
- Generates README in minutes, not hours

**Best for:** New projects, rapid prototyping, spec-driven development

### Brownfield Documentation (Codebase Analysis)

Analyze existing codebases to discover and consolidate documentation:

- Scans all source files for architecture patterns
- Identifies public APIs automatically
- Discovers existing documentation fragments
- Generates coverage reports (what exists vs what's missing)
- Highlights gaps and outdated sections

**Best for:** Legacy projects, comprehensive refactoring, knowledge consolidation

### Architecture Diagram Generation

Automatically create Mermaid diagrams from code analysis:

- **Flowcharts** - User request flows, data processing pipelines
- **Sequence Diagrams** - API call sequences, workflow steps
- **Architecture Diagrams** - Component relationships, layer structure
- **Auto-rendering** - Validates syntax, auto-fixes common errors

### Incremental Updates

Update documentation after each story completion:

- Detects existing documentation files
- Preserves user-authored sections (marked with special comments)
- Updates auto-generated sections only
- Maintains version numbers and changelogs
- Creates backups before modifications

### Template Library

8 professionally designed templates with:

- **Variable substitution** - Auto-populate project name, tech stack, API endpoints
- **Customization support** - Override with project-specific templates
- **Coding standards integration** - Respects your documentation style conventions
- **Conditional sections** - Include/exclude based on your project type

### Quality Gate Integration

Enforces documentation quality before release:

- Validates documentation coverage ≥80%
- Checks all public APIs have documentation
- Verifies README.md exists and is current
- Validates Mermaid diagrams render correctly
- **Blocks release** if thresholds not met

### Multi-Format Export

Generate documentation in multiple formats:

- **Markdown** - Default, stored in git
- **HTML** - Styled with navigation and table of contents
- **PDF** - Publication-ready documents with formatting

---

## Installation and Setup

### Prerequisites

1. **DevForgeAI Framework** (must be set up in your project)
2. **Context files** created (run `/create-context` if not done)
3. **Git repository** initialized with commits
4. **Completed stories** or existing codebase (depending on mode)

### No Installation Required

The documentation skill is **built into DevForgeAI**. No additional packages to install.

**Optional dependencies** (for advanced features):

```bash
# For PDF export (choose one)
sudo apt install pandoc texlive-xelatex    # Linux
brew install pandoc                         # macOS
choco install pandoc                        # Windows

# OR for HTML-to-PDF conversion
sudo apt install wkhtmltopdf                # Linux
brew install --cask wkhtmltopdf             # macOS
```

### Verify Setup

Check that context files exist:

```bash
ls -la devforgeai/context/
# Should show 6 files:
# - tech-stack.md
# - source-tree.md
# - coding-standards.md
# - architecture-constraints.md
# - dependencies.md
# - anti-patterns.md
```

---

## Quick Start

### Generate README for a Story (Greenfield)

```bash
/document STORY-040
```

This command:

1. Loads story specifications (user story, acceptance criteria, technical spec)
2. Analyzes implemented code and features
3. Generates a comprehensive README.md
4. Reports documentation coverage
5. Updates your story file with documentation references

**Result:** `README.md` in your project root, ready to customize

### Generate All Documentation Types

```bash
/document --type=all
```

Generates all 8 documentation types for completed stories:

- README.md
- docs/DEVELOPER.md (developer guide)
- docs/API.md (API documentation)
- docs/ARCHITECTURE.md (architecture guide)
- docs/TROUBLESHOOTING.md (troubleshooting guide)
- CONTRIBUTING.md (contribution guidelines)
- CHANGELOG.md (version history)
- docs/ROADMAP.md (project roadmap)

### Analyze Brownfield Project

```bash
/document --mode=brownfield --analyze
```

Deep analysis of existing codebase:

1. Scans all source files
2. Discovers existing documentation
3. Identifies gaps (missing README, API docs, guides)
4. Generates coverage report
5. Suggests improvements

**Result:** Analysis report showing what exists and what's missing

### List Available Templates

```bash
/document --list-templates
```

Display all 7 documentation template types available for use.

---

## Command Reference

### Basic Syntax

```bash
/document [options]
```

### Options

| Option | Example | Purpose |
|--------|---------|---------|
| **Story ID** | `/document STORY-040` | Generate docs for specific story (greenfield mode) |
| `--type` | `/document --type=readme` | Generate specific documentation type |
| `--mode` | `/document --mode=brownfield` | Switch to brownfield mode (codebase analysis) |
| `--analyze` | `/document --mode=brownfield --analyze` | Run brownfield analysis |
| `--export` | `/document --export=html` | Export to HTML or PDF format |
| `--list-templates` | `/document --list-templates` | Show available templates |

### Documentation Types

Use with `--type=`:

- `readme` - Project overview and quick start
- `developer-guide` - Development workflow and architecture
- `api` - API reference and endpoint documentation
- `architecture` - System design and diagrams
- `troubleshooting` - Common issues and solutions
- `contributing` - Contribution guidelines and PR process
- `changelog` - Version history and release notes
- `roadmap` - Feature timeline and milestones
- `all` - Generate all types (default for general projects)

### Export Formats

Use with `--export=`:

- `markdown` - Default (stored in git)
- `html` - Standalone HTML with styling
- `pdf` - Publication-ready PDF document

### Common Workflows

**For story-based development:**
```bash
# After story is marked "QA Approved"
/document STORY-040

# Review documentation, then release
/qa STORY-040
/release STORY-040
```

**For brownfield documentation:**
```bash
# Analyze existing project
/document --mode=brownfield --analyze

# Generate README for existing code
/document --type=readme --mode=brownfield

# Generate complete documentation suite
/document --type=all --mode=brownfield
```

**For specific documentation needs:**
```bash
# Just generate API docs
/document --type=api

# Update troubleshooting guide after support tickets
/document --type=troubleshooting STORY-041

# Export to HTML for sharing
/document --type=readme --export=html
```

---

## Documentation Templates

The skill includes 8 professionally designed templates:

### 1. README Template (`readme-template.md`)

**Sections:**
- Project overview (2-3 sentences)
- Key features (bulleted list)
- Quick installation
- Basic usage examples
- Technology stack
- Links to detailed docs

**Use when:** Starting a new project, releasing to public

**Example output:** 500-1000 words

### 2. Developer Guide Template (`developer-guide-template.md`)

**Sections:**
- Project structure (directory layout)
- Architecture overview (clean architecture, MVC, etc.)
- Development workflow (local setup, testing)
- Coding conventions (style, naming, patterns)
- Common development tasks
- Debugging tips
- Performance considerations

**Use when:** Building internal tools, onboarding developers

**Example output:** 2000-3000 words

### 3. API Documentation Template (`api-docs-template.md`)

**Sections:**
- Authentication (API keys, tokens, OAuth)
- Base URL and versioning
- Endpoint reference (method, path, parameters)
- Request/response schemas (JSON examples)
- Error codes and messages
- Rate limiting
- Code examples (curl, JavaScript, Python)
- Webhook specifications

**Use when:** Building APIs, building integrations

**Example output:** 1500-2500 words

### 4. Architecture Template (`architecture-template.md`)

**Sections:**
- System overview diagram
- Component architecture
- Data flow diagrams
- Technology choices (with reasoning)
- Layer definitions
- Key design decisions
- Scaling strategy
- Security model

**Use when:** Complex systems, documenting design decisions

**Example output:** 1500-2000 words + diagrams

### 5. Troubleshooting Template (`troubleshooting-template.md`)

**Sections:**
- Common setup issues
- Installation problems
- Configuration errors
- Runtime errors (with solutions)
- Performance issues
- Debugging guide
- Getting help (support channels)
- FAQ section

**Use when:** Mature projects, reducing support tickets

**Example output:** 1000-2000 words

### 6. Contributing Template (`contributing-template.md`)

**Sections:**
- How to contribute
- Development setup
- Code style guide
- Testing requirements
- Pull request process
- Commit message format
- Code review checklist
- License information

**Use when:** Open source projects, collaborative teams

**Example output:** 800-1200 words

### 7. Changelog Template (`changelog-template.md`)

**Sections:**
- Version header (version number, release date)
- Added features
- Changed behavior
- Deprecated features
- Removed features
- Bug fixes
- Security notes
- Migration guide (for breaking changes)

**Use when:** Publishing releases, tracking changes

**Example output:** 500-1000 words per release

### 8. Roadmap Template (`roadmap-template.md`)

**Sections:**
- Vision statement
- Completed features (checkmarks)
- In-progress features
- Planned features (quarters/sprints)
- Milestones
- Known limitations
- Community requests

**Use when:** Planning features, managing expectations

**Example output:** 800-1500 words

### Template Customization

Override default templates with project-specific versions:

```bash
# Create custom template directory
mkdir -p devforgeai/templates/documentation/

# Copy template to customize
cp .claude/skills/devforgeai-documentation/assets/templates/readme-template.md \
   devforgeai/templates/documentation/readme-template.md

# Edit custom template (will be used instead of default)
# The skill automatically uses custom versions if they exist
```

---

## Workflows

### Workflow 1: Story-Based Documentation (Greenfield)

For projects using DevForgeAI's spec-driven development:

```
1. Complete story implementation (/dev STORY-040)
   ↓
2. Pass QA validation (/qa STORY-040)
   ↓
3. Generate documentation (/document STORY-040)
   ↓
4. Review generated docs
   ↓
5. Release (/release STORY-040)
```

**What the skill does:**

1. **Extracts** user story, acceptance criteria, and technical specifications
2. **Analyzes** implemented code to identify new APIs, classes, and features
3. **Generates** documentation from these sources
4. **Validates** 80% coverage (all public APIs documented)
5. **Creates** or updates README, API docs, guides

**Time saved:** 2-4 hours per story's documentation

### Workflow 2: Brownfield Documentation (Codebase Analysis)

For existing projects without comprehensive documentation:

```
1. Analyze codebase (/document --mode=brownfield --analyze)
   ↓
2. Review gap analysis report
   ↓
3. Generate missing docs (/document --type=all --mode=brownfield)
   ↓
4. Customize with project-specific details
   ↓
5. Commit to repository
```

**What the skill does:**

1. **Scans** all source files (500+ files supported)
2. **Discovers** existing documentation fragments
3. **Identifies** public APIs and architecture patterns
4. **Reports** gaps (missing README, API docs, guides)
5. **Generates** documentation for undocumented code

**Time saved:** 8-20 hours of manual analysis and writing

### Workflow 3: Incremental Updates

After completing each story in an ongoing project:

```
/document STORY-041

# Skill:
# - Detects existing README.md
# - Updates auto-generated sections (API endpoints, features)
# - Preserves user-authored sections
# - Updates CHANGELOG.md with new entry
# - Reports updated coverage
```

**Smart merging:**

- User-written content marked with `<!-- USER CONTENT START/END -->` is preserved
- Auto-generated sections (marked with `<!-- AUTO-GENERATED -->`) are updated
- Backups created: `README.md.backup-2025-11-18-120000`
- Version numbers updated (if semantic versioning detected)

### Workflow 4: Complete Documentation Refresh

Generate entire documentation suite for a mature project:

```bash
# Generate all documentation types at once
/document --type=all

# Results in:
# - README.md (2000 words)
# - docs/DEVELOPER.md (3000 words)
# - docs/API.md (2500 words)
# - docs/ARCHITECTURE.md (2000 words)
# - docs/TROUBLESHOOTING.md (1500 words)
# - CONTRIBUTING.md (1000 words)
# - CHANGELOG.md (auto-generated from git)
# - docs/ROADMAP.md (1500 words)

# Total: ~16,000 words across 8 files, generated in <10 minutes
```

---

## Architecture

### System Design

```
User Command
    ↓
/document command (Phase 0-3)
    ↓
devforgeai-documentation skill (Phase 0-7)
    ├─ Phase 0: Mode detection & validation
    ├─ Phase 1: Discovery (stories OR codebase analysis)
    ├─ Phase 2: Content generation (subagents)
    ├─ Phase 3: Template application
    ├─ Phase 4: Integration & updates
    ├─ Phase 5: Validation & quality check
    ├─ Phase 6: Export & finalization
    └─ Phase 7: Completion summary
    ↓
Generated documentation files
    ├─ README.md
    ├─ docs/DEVELOPER.md
    ├─ docs/API.md
    ├─ docs/ARCHITECTURE.md
    ├─ docs/TROUBLESHOOTING.md
    ├─ CONTRIBUTING.md
    ├─ CHANGELOG.md
    └─ docs/ROADMAP.md
```

### Subagent Coordination

**documentation-writer subagent**

Generates prose documentation sections:

- Reads story specifications, code metadata, and context files
- Writes clear, professional documentation sections
- Follows coding-standards.md style conventions
- Produces Markdown content ready for templates

**code-analyzer subagent** (NEW)

Analyzes codebase for brownfield documentation:

- Scans source files for architecture patterns
- Identifies public APIs (classes, functions, endpoints)
- Discovers dependencies and layer relationships
- Detects existing documentation
- Returns structured JSON for doc generation

### File Structure

The documentation skill is located at:

```
.claude/skills/devforgeai-documentation/
├── SKILL.md                    # Skill workflow (this file when invoked)
├── assets/
│   └── templates/              # 8 documentation templates
│       ├── readme-template.md
│       ├── developer-guide-template.md
│       ├── api-docs-template.md
│       ├── architecture-template.md
│       ├── troubleshooting-template.md
│       ├── contributing-template.md
│       ├── changelog-template.md
│       └── roadmap-template.md
└── references/                 # Deep documentation guides
    ├── documentation-standards.md
    ├── greenfield-workflow.md
    ├── brownfield-analysis.md
    ├── diagram-generation-guide.md
    └── template-customization.md
```

### Execution Phases

The skill executes in 7 sequential phases:

| Phase | Purpose | Output |
|-------|---------|--------|
| **0** | Mode detection and validation | Mode confirmed, context validated |
| **1** | Discovery and analysis | Story specs OR codebase metadata extracted |
| **2** | Content generation | Documentation sections generated (subagents) |
| **3** | Template application | Templates populated with variables |
| **4** | Integration and updates | Files written/updated, merges handled |
| **5** | Validation and quality check | Coverage ≥80%, diagrams valid, standards met |
| **6** | Export and finalization | HTML/PDF exported (if requested), story updated |
| **7** | Completion summary | Results reported, next steps suggested |

---

## Quality Gates

The documentation skill enforces strict quality gates to ensure release-ready documentation.

### Quality Gate Requirements

Before releasing a story, documentation must meet:

1. **Coverage ≥80%** - At least 80% of public APIs documented
2. **README.md Exists** - Current (updated in last 90 days)
3. **All Public APIs Documented** - Every public class, function, endpoint has docs
4. **Diagrams Render** - All Mermaid diagrams have valid syntax
5. **Framework Constraints Respected** - Docs match architecture-constraints.md

### Coverage Calculation

```
Documentation Coverage = (Documented APIs / Total Public APIs) × 100

Examples:
- 15 endpoints documented / 18 total = 83% ✅ Passes gate
- 12 functions documented / 20 total = 60% ❌ Fails gate (below 80%)
```

### What Counts as Documented?

An API is documented when:

- ✅ Included in API documentation
- ✅ Has JSDoc/docstring in code
- ✅ Listed in README with usage examples
- ✅ Explained in developer guide

An API is **NOT** documented if:

- ❌ Only exists in code comments
- ❌ Mentioned but no examples provided
- ❌ Outdated docs (>30 days old)

### Quality Gate Integration

When you run `/release`:

```bash
/release STORY-040

# Release command checks:
# 1. Tests pass ✅
# 2. Coverage ≥95%/85%/80% ✅
# 3. Documentation coverage ≥80% ← NEW GATE

IF documentation_coverage < 80:
    BLOCK RELEASE
    Display: "Documentation coverage 65% < 80%"
    Show: Which APIs are undocumented
    Ask: Generate missing docs or skip?
ELSE:
    ALLOW RELEASE
```

### Bypassing Quality Gates

Not recommended, but if necessary:

```bash
/release STORY-040 --skip-docs

# Not recommended because:
# - Reduces project quality
# - Creates technical debt
# - Confuses users and developers
# - Blocks quality metric tracking
```

**Better alternative:**

```bash
# Use --generate-stubs to create placeholder docs
/document STORY-040 --generate-stubs

# Then customize:
# - Add usage examples
# - Clarify requirements
# - Complete documentation
# - Retry release

/release STORY-040  # Now passes gate
```

---

## Advanced Usage

### Custom Documentation Workflows

#### Add Project Logo to README

Create custom template:

```bash
mkdir -p devforgeai/templates/documentation/
```

Edit `devforgeai/templates/documentation/readme-template.md`:

```markdown
# {{project_name}}

![Project Logo](assets/logo.png)

{{project_description}}

...rest of template...
```

#### Generate API Docs with OpenAPI/Swagger

The skill can extract endpoint definitions and generate OpenAPI specs:

```bash
# For API-heavy projects:
/document --type=api --export=openapi

# Results in:
# - docs/api.md (human-readable)
# - docs/openapi.yaml (machine-readable Swagger spec)
```

#### Create Language-Specific Examples

Customize API documentation with code examples:

```bash
/document --type=api --language=python,javascript,curl

# Generates API docs with examples in:
# - Python (async/await)
# - JavaScript (fetch API)
# - cURL (command line)
```

### Brownfield Project Best Practices

#### Phase 1: Analyze and Report

```bash
/document --mode=brownfield --analyze

# Review gap analysis report:
# - What documentation exists
# - What's missing (README, API docs, guides)
# - What's outdated (>30 days old)
```

#### Phase 2: Generate High-Priority Docs

```bash
# Priority 1: README
/document --type=readme --mode=brownfield

# Priority 2: Developer Guide (architecture)
/document --type=developer-guide --mode=brownfield

# Priority 3: API Docs (if applicable)
/document --type=api --mode=brownfield
```

#### Phase 3: Incremental Completion

```bash
# Fill remaining gaps as time allows
/document --type=troubleshooting --mode=brownfield
/document --type=contributing --mode=brownfield
/document --type=roadmap --mode=brownfield
```

### Batch Documentation Generation

Generate docs for multiple stories:

```bash
# For all completed stories in sprint
for story in $(find .ai_docs/Stories -name "*.story.md" -type f); do
    story_id=$(grep "^id:" "$story" | cut -d' ' -f2)
    /document "$story_id"
done
```

### Documentation Versioning

Track documentation versions with code:

```bash
# Before generating docs
git checkout -b docs/update-v1.2.0

# Generate docs
/document --type=all

# Review changes
git diff README.md docs/API.md

# Commit with version tag
git add docs/
git commit -m "docs: Update documentation for v1.2.0

- Generated README.md from STORY-040 through STORY-045
- Added API documentation for new endpoints
- Updated architecture diagrams for microservices
- Added troubleshooting section"

git tag v1.2.0-docs
```

### Continuous Documentation Updates

Integrate documentation generation into your workflow:

```bash
# Add to CI/CD pipeline (after QA passes)
if [ "$STATUS" = "QA_APPROVED" ]; then
    /document STORY-$STORY_ID
fi

# Add pre-release checks
/document --validate

# Generates documentation before each release
/release STORY-$STORY_ID
```

---

## Troubleshooting

### Common Issues and Solutions

#### Issue 1: "Context files missing"

```
Error: "Context files required. Run /create-context first."
```

**Solution:**

```bash
/create-context MyProject

# This creates 6 required context files:
# - devforgeai/context/tech-stack.md
# - devforgeai/context/source-tree.md
# - devforgeai/context/coding-standards.md
# - devforgeai/context/architecture-constraints.md
# - devforgeai/context/dependencies.md
# - devforgeai/context/anti-patterns.md
```

#### Issue 2: "No completed stories found"

```
Error: "No completed stories found (greenfield mode)"
```

**Solution:**

Option A: Complete a story first
```bash
/dev STORY-040      # Complete implementation
/qa STORY-040       # Pass quality validation
/document STORY-040 # Now have story to document
```

Option B: Use brownfield mode
```bash
/document --mode=brownfield --analyze
```

#### Issue 3: "Documentation coverage below 80%"

```
Warning: "Documentation coverage 65% < 80% (quality gate)"
Undocumented: 7 API endpoints
```

**Solution:**

```bash
# Option 1: Generate stubs for missing docs
/document --generate-stubs

# Option 2: Document specific endpoints in README
# Add section to README.md:
## API Reference

### POST /api/tasks
Create a new task. [Complete documentation here...]

# Option 3: Re-run documentation generation
/document STORY-040
```

#### Issue 4: "Mermaid diagram syntax error"

```
Error: "Diagram syntax error in docs/architecture.mmd"
```

**Solution:**

Check diagram syntax (common errors):

```markdown
❌ Missing semicolon:
flowchart TD
    A[Start] --> B[End]    # Missing ;

✅ Correct:
flowchart TD
    A[Start] --> B[End];

❌ Unclosed quotes:
graph TD
    A["Task Service

✅ Correct:
graph TD
    A["Task Service"];
```

The skill auto-fixes common errors. If still failing, check reference:
```bash
Read(file_path=".claude/skills/devforgeai-documentation/references/diagram-generation-guide.md")
```

#### Issue 5: "PDF export fails"

```
Error: "PDF export requires pandoc or wkhtmltopdf"
```

**Solution:**

Install PDF conversion tools:

```bash
# Linux (Ubuntu/Debian)
sudo apt update
sudo apt install pandoc texlive-xelatex

# macOS
brew install pandoc

# Windows
choco install pandoc

# Then retry
/document --type=readme --export=pdf
```

Alternative: Use HTML export instead
```bash
/document --type=readme --export=html
# HTML can be printed to PDF from browser
```

#### Issue 6: "Story file not found"

```
Error: "Story not found: STORY-999"
```

**Solution:**

List available stories:
```bash
Glob(pattern="devforgeai/specs/Stories/*.story.md")
```

Use correct story ID from output, then:
```bash
/document STORY-040  # Use correct ID
```

#### Issue 7: "Existing documentation conflicts"

```
Warning: "Existing README.md found. User content will be preserved."
Info: "Backup created: README.md.backup-2025-11-18-120000"
```

**Solution:**

The skill preserves user-authored sections. To ensure your content is preserved:

1. Mark user content in README.md:
```markdown
<!-- USER CONTENT START: Custom Installation Section -->

## Custom Installation

Your custom setup steps here...

<!-- USER CONTENT END -->
```

2. Auto-generated sections are marked:
```markdown
<!-- AUTO-GENERATED: API Endpoints -->

### Endpoints

Generated endpoint list...

<!-- AUTO-GENERATED END -->
```

The skill updates only `AUTO-GENERATED` sections, preserving everything else.

### Performance Troubleshooting

#### Generation takes too long (>10 minutes)

**For greenfield mode:**
- Story is too complex (many AC)
- Solution: Break into smaller stories

**For brownfield mode:**
- Codebase is very large (>1000 files)
- Solution: Analyze specific directory: `/document --path=src/`

#### High token usage

- Brownfield analysis of large codebase
- HTML/PDF export being generated
- Solution: Generate one doc type at a time

### Debug Mode

Enable verbose logging:

```bash
# Set environment variable
export DEVFORGEAI_DEBUG=true

# Run command
/document STORY-040

# Shows:
# - Phase transitions
# - File operations
# - Subagent invocations
# - Token usage per phase
```

### Getting Help

When troubleshooting, gather:

1. Command executed: `/document [args]`
2. Error message: Full text
3. Story ID (if applicable): STORY-XXX
4. Project mode: greenfield or brownfield
5. Context: What were you trying to do?

Then check:

1. **Skill reference:** `.claude/skills/devforgeai-documentation/SKILL.md`
2. **Documentation standards:** `references/documentation-standards.md`
3. **Workflow guide:** `references/greenfield-workflow.md` or `brownfield-analysis.md`

---

## Next Steps

### After Documentation Generation

1. **Review Generated Content**
   ```bash
   # Open and read the generated files
   cat README.md
   # Check for:
   # - Correct project name
   # - Accurate tech stack
   # - Clear installation steps
   # - Complete API reference
   ```

2. **Customize for Your Project**
   ```bash
   # Add project-specific sections
   # Update examples for your use case
   # Include company branding/guidelines
   # Add custom troubleshooting tips
   ```

3. **Validate Quality**
   ```bash
   # Check coverage
   /document STORY-040 --validate

   # Should report:
   # - Documentation coverage: 85%
   # - All diagrams valid
   # - Framework compliance: OK
   ```

4. **Release Documentation**
   ```bash
   # Commit generated docs
   git add README.md docs/
   git commit -m "docs: Generated documentation for STORY-040"

   # Then release story
   /release STORY-040
   ```

### Continuous Improvement

- **Run after each story:** `/document STORY-XXX` when story is QA Approved
- **Monitor coverage:** Aim for 85%+ documentation coverage
- **Update templates:** Create `devforgeai/templates/documentation/` overrides
- **Collect feedback:** Ask users/developers what documentation helps most

### Related Features

- **Code coverage:** [Coverage validation in `/qa` command]
- **Story specifications:** [Story templates in `devforgeai-story-creation`]
- **Architecture decisions:** [ADRs in `devforgeai/adrs/`]
- **API design:** [API specifications in `devforgeai-ui-generator`]

### Learn More

**Reference Files** (load with Read tool):

- `.claude/skills/devforgeai-documentation/references/documentation-standards.md` - Detailed style guide
- `.claude/skills/devforgeai-documentation/references/greenfield-workflow.md` - Story-based documentation
- `.claude/skills/devforgeai-documentation/references/brownfield-analysis.md` - Codebase analysis
- `.claude/skills/devforgeai-documentation/references/diagram-generation-guide.md` - Mermaid diagrams
- `.claude/skills/devforgeai-documentation/references/template-customization.md` - Custom templates

**Framework Integration:**

- See `.claude/memory/commands-reference.md` for all slash commands
- See `.claude/memory/documentation-command-guide.md` for documentation workflows
- See `CLAUDE.md` for complete framework overview

---

## Support and Feedback

**Documentation Skill Status:** Production Ready (QA Approved)

**Tested with:**
- Node.js projects (React, Express, NestJS)
- Python projects (FastAPI, Django)
- .NET projects (C#, ASP.NET)
- Go projects (Gin, Echo)
- Mixed-language projects

**Known Limitations:**

- PDF export requires external tools (pandoc or wkhtmltopdf)
- Brownfield analysis supports projects up to 5,000 source files
- Mermaid diagrams limited to 50 components per diagram

**Future Enhancements** (roadmap):

- Multi-language documentation (i18n)
- Interactive code examples (live playgrounds)
- Documentation search and indexing
- Automated coverage trend analysis
- Video documentation generation

---

**Version:** 1.0.0
**Last Updated:** November 18, 2025
**Status:** Production Ready (QA Approved)
**Framework:** DevForgeAI Spec-Driven Development v1.0+
