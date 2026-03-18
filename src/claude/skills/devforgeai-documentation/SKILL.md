---
name: devforgeai-documentation
description: Automated documentation generation integrated into SDLC workflow. Generates README, developer guides, API docs, architecture diagrams, and roadmaps from stories and codebase analysis. Supports greenfield (story-based) and brownfield (codebase analysis) modes. Use when generating project documentation, updating docs after story completion, or analyzing documentation coverage.
tools: Read, Write, Edit, Glob, Grep, Bash, Task, AskUserQuestion
model: claude-sonnet-4-6
---

# DevForgeAI Documentation Skill

Automated documentation generation integrated into the SDLC workflow, supporting greenfield and brownfield projects.

---

## ⚠️ EXECUTION MODEL: This Skill Expands Inline

**After invocation, YOU (Claude) execute these instructions phase by phase.**

**When you invoke this skill:**
1. This SKILL.md content is now in your conversation
2. You execute each phase sequentially
3. You display results as you work through phases
4. You complete with success/failure report

**Do NOT:**
- ❌ Wait passively for skill to "return results"
- ❌ Assume skill is executing elsewhere
- ❌ Stop workflow after invocation

**Proceed to "Parameter Extraction" section below and begin execution.**

---

## Parameter Extraction

This skill extracts parameters from conversation context:
- **Story ID**: From loaded story file YAML frontmatter or explicit `**Story ID:** STORY-XXX`
- **Documentation Type**: From `--type=` argument or explicit `**Type:** readme|api|architecture|roadmap|all`
- **Mode**: From `--mode=` argument or explicit `**Mode:** greenfield|brownfield`
- **Export Format**: From `--export=` argument or explicit `**Export:** html|pdf`
- **Audit Mode**: From `--audit=` argument → `**Audit Mode:** dryrun`
- **Audit Fix**: From `--audit-fix` flag → `**Audit Fix:** true`
- **Finding Filter**: From `--finding=` argument → `**Finding Filter:** F-NNN` or `all`

**Defaults:**
- Type: `readme` (if story ID provided) or `all` (if no story or audit-fix)
- Mode: `greenfield` (if story provided) or `brownfield` (if no story)
- Export: `markdown` (no export)
- Audit Mode: `null` (not an audit)
- Audit Fix: `false`
- Finding Filter: `all`

---

## Mode Router

**⚠️ ROUTING DECISION — evaluate BEFORE executing any workflow phase.**

```
IF Audit Mode is set (dryrun):
    → Execute Phase A: Documentation Audit (A.0 through A.4)
    → SKIP Phases 0-7 (generation workflow)
    → EXIT after Phase A.4

ELIF Audit Fix is true:
    → Execute Phase B: Documentation Fix (B.0 through B.5)
    → SKIP Phases 0-7 (generation workflow)
    → EXIT after Phase B.5

ELSE:
    → Execute Phases 0-7 (existing generation workflow, unchanged)
```

---

## Purpose

Generate and maintain comprehensive project documentation automatically:
- **Greenfield**: Generate docs from completed stories and technical specifications
- **Brownfield**: Analyze existing codebase and consolidate/generate missing documentation
- **Incremental**: Update docs after each story completion
- **Quality Gate**: Enforce 80% documentation coverage before release

---

## When to Use This Skill

**Invoked by:**
- `/document [STORY-ID]` command (greenfield mode)
- `/document --mode=brownfield --analyze` command (brownfield analysis)
- `/document --type=readme` command (specific doc type)
- `/release` command (documentation quality gate validation)
- Manual: `Skill(command="devforgeai-documentation")`

**Prerequisites:**
- Context files exist (`devforgeai/specs/context/*.md`) - 6 files required
- For greenfield: Story files exist and status ≥ "Dev Complete"
- For brownfield: Codebase exists with source files

---

## Documentation Workflow (7 Phases)

**⚠️ EXECUTION STARTS HERE - You are now executing the skill's workflow.**

### Phase 0: Mode Detection and Validation

**Steps:**

1. **Extract parameters** from conversation context (story ID, type, mode, export)

2. **Detect mode**:
   ```
   IF story ID provided:
       MODE = "greenfield"
   ELIF --mode=brownfield:
       MODE = "brownfield"
   ELSE:
       AskUserQuestion: "Generate docs from stories or analyze codebase?"
   ```

3. **Validate context files**:
   ```
   Glob(pattern="devforgeai/specs/context/*.md")

   IF count < 6:
       Display: "❌ Context files missing. Run /create-context first."
       HALT
   ```

4. **Determine documentation type**:
   ```
   TYPE = extracted type OR default

   IF TYPE == "all" OR TYPE == "module":
       TYPES = ["api", "architecture", "developer-guide", "troubleshooting", "roadmap"]
       # Note: "readme" is handled via README.md module blurb (Phase 4.5), not as a separate file
   ELSE:
       TYPES = [TYPE]
   ```

5. **Resolve output strategy** (section-level consolidation):
   ```
   # All story-based documentation merges into framework-level files as sections.
   # No per-module files are created. See references/post-generation-workflow.md Section 2.
   #
   # Target files (fixed, never grows):
   #   docs/api/API.md              ← all API docs
   #   docs/architecture/ARCHITECTURE.md  ← all architecture docs
   #   docs/guides/DEVELOPER-GUIDE.md     ← all dev guidance
   #   docs/guides/TROUBLESHOOTING.md     ← all troubleshooting (problem-first headings)
   #   docs/guides/ROADMAP.md             ← single project roadmap by priority tier
   ```

**Output**: Mode, types, output strategy, export format confirmed

---

### Phase 1: Discovery and Analysis

**Reference:** `references/greenfield-workflow.md` or `references/brownfield-analysis.md`

**For Greenfield Mode:**

1. **Load story files** for documentation:
   ```
   IF story ID provided:
       stories = [story ID]
   ELSE:
       Glob(pattern="devforgeai/specs/Stories/*.story.md")
       Filter: status IN ["Dev Complete", "QA Approved", "Released"]
   ```

2. **Extract technical specifications**:
   ```
   FOR each story:
       Read story file
       Extract: User story, AC, technical spec, API endpoints, NFRs
       Store in documentation context
   ```

3. **Load context files** for reference:
   ```
   Read: tech-stack.md (technologies)
   Read: source-tree.md (file structure)
   Read: coding-standards.md (conventions)
   ```

**For Brownfield Mode:**

1. **Invoke code-analyzer subagent** for deep analysis:
   ```
   Task(
       subagent_type="code-analyzer",
       description="Analyze codebase for documentation",
       prompt="Analyze the codebase to extract:
       - Architecture pattern (MVC, Clean, DDD, Layered)
       - Layer structure (presentation, application, domain, infrastructure)
       - Public APIs (classes, functions, endpoints)
       - Entry points (main files, startup)
       - Dependencies (external, internal)

       Return structured JSON with code metadata."
   )
   ```

2. **Discover existing documentation**:
   ```
   Glob(pattern="**/*.md")
   Filter: Documentation files (README, CONTRIBUTING, API, etc.)
   Read each file
   Categorize: readme, api-docs, developer-guide, etc.
   ```

3. **Identify gaps**:
   ```
   Compare: What exists vs what's needed
   Generate gap report: Missing, outdated, incomplete sections
   ```

**Output**: Documentation context loaded (stories OR codebase analysis)

---

### Phase 2: Content Generation

**Reference:** `references/documentation-standards.md`

**For each documentation type in TYPES:**

1. **Load framework doc and invoke documentation-writer subagent**:

   ```
   # Reference: references/post-generation-workflow.md (Section 2 — Section Insertion Map)
   # Reference: references/anti-aspirational-guidelines.md

   target_file = resolve_target(doc_type)   # e.g., docs/api/API.md
   existing_content = Read(target_file)
   module_name = derived from Phase 0 / post-generation-workflow.md Section 1
   ```

   ```
   Task(
       subagent_type="documentation-writer",
       description="Generate {type} section for {module_name}",
       prompt="Generate a SECTION (not a full document) for insertion into an existing
       framework document.

       Module: {module_name}
       Doc type: {type}
       Story context:
       {documentation_context}

       Existing framework document (your section must match this voice and style):
       {existing_content}

       Section markers — wrap your output in these exact markers:
       <!-- SECTION: {module_name} START -->
       ## {Module Display Name}
       (your content here)
       <!-- SECTION: {module_name} END -->

       Content rules (from anti-aspirational-guidelines.md):
       - No future tense for unimplemented features
       - No filler — if nothing to say for this doc type, return SKIP
       - Problem-first headings for troubleshooting (symptom as heading, not module name)
       - Concrete examples with real values, no placeholders
       - Match the tone and depth of surrounding sections in the existing document
       - No duplicate introductions — one sentence on what the module does, then specifics

       Return: Markdown section content wrapped in markers, OR the word SKIP"
   )
   ```

2. **Generate Mermaid diagrams** (if type == "architecture"):
   ```
   # Extract architecture from code analysis or story specs

   # Generate flowchart
   flowchart = """
   flowchart TD
       A[User Request] --> B[Controller]
       B --> C[Use Case]
       C --> D[Repository]
       D --> E[Database]
   """

   # Generate sequence diagram
   sequence = """
   sequenceDiagram
       User->>API: POST /tasks
       API->>Controller: createTask()
       Controller->>UseCase: execute()
       UseCase->>Repository: save()
       Repository->>DB: INSERT
   """

   # Validate Mermaid syntax
   Check for common errors: missing semicolons, unclosed quotes
   Auto-fix if possible
   ```

3. **Apply template**:
   ```
   Read template: assets/templates/{type}-template.md

   Substitute variables:
   - {{project_name}}
   - {{tech_stack}}
   - {{installation_steps}}
   - {{api_endpoints}}
   - {{architecture_diagram}}

   Output: Final markdown content
   ```

**Output**: Generated documentation content for each type

---

### Phase 3: Template Application and Customization

**Reference:** `references/template-customization.md`

1. **Load base template**:
   ```
   template_path = "assets/templates/{type}-template.md"

   # Check for custom template
   custom_path = "devforgeai/templates/documentation/{type}-template.md"

   IF custom_path exists:
       template = Read(custom_path)
   ELSE:
       template = Read(template_path)
   ```

2. **Apply customizations from coding-standards.md**:
   ```
   Read: devforgeai/specs/context/coding-standards.md
   Extract: Documentation style preferences

   Apply to template:
   - Heading styles
   - Code block formatting
   - Example structure
   - Tone and voice
   ```

3. **Populate template sections**:
   ```
   FOR each variable in template:
       Replace {{variable}} with generated content

   FOR each conditional section:
       IF condition met:
           Include section
       ELSE:
           Remove section
   ```

**Output**: Fully customized documentation ready to write

---

### Phase 4: Section-Level Integration

**Reference:** `references/post-generation-workflow.md` (Section 2 — Section Insertion Map)

All documentation is inserted as sections into fixed framework files. No per-module files are created.

**Section Insertion Map:**

| Doc Type | Target File |
|----------|-------------|
| api | `docs/api/API.md` |
| architecture | `docs/architecture/ARCHITECTURE.md` |
| developer-guide | `docs/guides/DEVELOPER-GUIDE.md` |
| troubleshooting | `docs/guides/TROUBLESHOOTING.md` |
| roadmap | `docs/guides/ROADMAP.md` |

**For each generated section:**

1. **Skip if documentation-writer returned SKIP** (no content for this doc type)

2. **Read target framework file**:
   ```
   target_path = section_insertion_map[doc_type]
   content = Read(target_path)
   ```

3. **Insert or update section using HTML comment markers**:
   ```
   MARKER_START = "<!-- SECTION: {module_name} START -->"
   MARKER_END = "<!-- SECTION: {module_name} END -->"

   IF MARKER_START found in content:
       # Update existing section (idempotent)
       Extract old_block from MARKER_START to MARKER_END (inclusive)
       Edit(file_path=target_path, old_string=old_block, new_string=generated_section)
       Display: "Updated {module_name} section in {target_path}"

   ELSE:
       # Insert new section before the last --- separator or at end of file
       # Preserve user-authored content (<!-- USER CONTENT START/END -->)
       Append generated_section to end of document (before final ---)
       Display: "Added {module_name} section to {target_path}"
   ```

4. **Track updated files** for Phase 7 summary:
   ```
   updated_files[doc_type] = target_path
   ```

**Output**: Framework files updated with module sections

---

### Phase 4.5: Post-Generation Integration

**Reference:** `references/post-generation-workflow.md`

**Trigger:** Executes ONLY when mode=greenfield AND story_id provided.
**Skip:** If trigger conditions not met, proceed directly to Phase 5.

**Steps:**

1. Derive module name — see reference (Section 1: Module Name Derivation)
2. Update root README.md module blurb — see reference (Section 4: Action 2)
   - Uses HTML comment markers for idempotency: `<!-- MODULE-DOC: {module} START/END -->`
   - Module blurb links to anchors within framework docs (not to per-module files)
3. Update CHANGELOG.md with documentation entry — see reference (Section 5: Action 3)
   - Per-story idempotency
4. Update story file Change Log with documentation row — see reference (Section 6: Action 4)

All actions are idempotent — safe to re-run without duplicating entries.

**Output**: README.md, CHANGELOG.md, and story file updated

---

### Phase 5: Validation and Quality Check

**Reference:** `references/documentation-standards.md`

1. **Verify documentation coverage**:
   ```
   total_public_apis = count public functions/classes/endpoints
   documented_apis = count APIs with documentation

   coverage = (documented_apis / total_public_apis) * 100

   IF coverage < 80:
       Display: "⚠️ Documentation coverage: {coverage}% (threshold: 80%)"
       List undocumented APIs

       AskUserQuestion: "Coverage below threshold. Continue or add docs?"
   ```

2. **Validate Mermaid diagrams** (if generated):
   ```
   FOR each diagram file:
       content = Read(diagram_file)

       # Check syntax
       errors = check_mermaid_syntax(content)

       IF errors:
           Display: "Diagram syntax error in {file}: {errors}"
           Attempt auto-fix

           IF auto-fix successful:
               Write corrected diagram
           ELSE:
               Display: "Manual review needed for {file}"
   ```

3. **Check framework constraint compliance**:
   ```
   Read: devforgeai/specs/context/architecture-constraints.md

   IF documentation describes architecture:
       Validate diagrams match constraints
       Check for layer violations in described flows
   ```

4. **Verify all required sections present**:
   ```
   required_sections = ["Overview", "Installation", "Usage"]

   FOR each doc file:
       content = Read(doc_file)

       FOR section in required_sections:
           IF section not in content:
               Display: "Missing section: {section} in {doc_file}"
   ```

5. **Anti-aspirational content check**:
   ```
   # Reference: references/anti-aspirational-guidelines.md

   FOR each generated section:
       # Check for prohibited language
       Grep for: "will be", "will support", "planned", "in the future",
                  "upcoming", "powerful", "robust", "seamless",
                  "easy to use", "simple", "intuitive"

       IF violations found:
           Display: "⚠️ Aspirational language detected in {module_name} {doc_type} section"
           List violations with line context
           Return content to documentation-writer with fix instructions

       # Check for empty/filler sections
       IF section contains heading followed immediately by another heading:
           Display: "⚠️ Empty section detected — remove or populate"

       # Check for placeholder examples
       Grep for: "your-", "example-", "<placeholder>", "..."
       IF found:
           Display: "⚠️ Placeholder detected — replace with real values"
   ```

**Output**: Validation report, any issues flagged

---

### Phase 6: Export and Finalization

**For HTML Export** (`--export=html`):

1. **Convert Markdown to HTML**:
   ```
   Bash(command="pandoc {markdown_file} -o {html_file} --standalone --toc")

   OR use Python markdown library if available:

   import markdown
   html = markdown.markdown(content, extensions=['toc', 'tables', 'fenced_code'])
   ```

2. **Apply styling**:
   ```
   Read: assets/templates/html-style.css (if exists)
   Wrap HTML in styled template
   Include: Navigation, header, footer
   ```

**For PDF Export** (`--export=pdf`):

1. **Convert Markdown to PDF**:
   ```
   # Via pandoc
   Bash(command="pandoc {markdown_file} -o {pdf_file} --pdf-engine=xelatex --toc")

   # Via wkhtmltopdf (HTML intermediate)
   Bash(command="pandoc {markdown_file} -o temp.html --standalone")
   Bash(command="wkhtmltopdf temp.html {pdf_file}")
   ```

2. **Check for dependencies**:
   ```
   IF export fails:
       Display: "PDF export requires: pandoc and xelatex OR wkhtmltopdf"
       Display: "Install: sudo apt install pandoc texlive-xelatex"
       Fallback to Markdown only
   ```

**Update story file** (if story-based):

1. **Story Change Log** — If Phase 4.5 executed (module docs mode),
   the story Change Log row was already added in that phase. Skip duplicate entry here.

2. **Add documentation references**:
   ```
   Edit story file to add section:

   ## Generated Documentation

   - README.md: {path}
   - Developer Guide: {path}
   - API Documentation: {path}
   - Last Generated: {timestamp}
   - Coverage: {coverage}%
   ```

**Output**: Exported formats (if requested), story updated

---

### Phase 7: Completion Summary

**Generate summary report**:

```
Display: ""
Display: "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
Display: "  Documentation Generation Complete"
Display: "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
Display: ""
Display: "Updated Sections ({module_name}):"
FOR each doc_type in updated_files:
    Display: "  ✓ {doc_type}: {updated_files[doc_type]} ({word_count} words)"
FOR each skipped_type in skipped_types:
    Display: "  ○ {skipped_type}: skipped (no content for this module)"

Display: ""
Display: "Documentation Coverage: {coverage}%"

IF coverage >= 80:
    Display: "  ✅ Meets quality gate threshold (≥80%)"
ELSE:
    Display: "  ⚠️ Below threshold (≥80% required for release)"

IF story_id provided:
    Display: ""
    Display: "Also updated:"
    Display: "  → README.md (module blurb)"
    Display: "  → CHANGELOG.md ([Unreleased] > Added)"
    Display: "  → {story_file} (Change Log table)"

Display: ""
Display: "Next Steps:"
Display: "  • Review generated documentation"
Display: "  • Run /qa {story_id} deep to validate story"
Display: "  • Update documentation with project-specific details"
Display: ""
```

**Return**: Summary object to command

---

## Integration Points

**From:**
- devforgeai-story-creation (story specifications)
- spec-driven-architecture (context files)
- spec-driven-dev (completed implementations)

**To:**
- devforgeai-release (documentation quality gate)
- Documentation files (README, guides, API docs)

**Auto-invokes:**
- documentation-writer subagent (prose generation)
- code-analyzer subagent (codebase analysis)

---

## Subagent Coordination

### documentation-writer Subagent

**Purpose**: Generate prose content for documentation sections

**Invocation**:
```
Task(
    subagent_type="documentation-writer",
    description="Generate {type} documentation",
    prompt="Generate {type} documentation.

    Context:
    {technical_specifications}
    {acceptance_criteria}
    {api_endpoints}

    Style: Follow coding-standards.md conventions
    Format: Markdown with code examples
    Sections: {required_sections}

    Return: Complete Markdown document"
)
```

**Returns**: Markdown content ready for template insertion

---

### code-analyzer Subagent

**Purpose**: Deep codebase analysis for brownfield projects

**Invocation**:
```
Task(
    subagent_type="code-analyzer",
    description="Analyze codebase for documentation",
    prompt="Analyze the codebase in {project_path}.

    Extract:
    - Architecture pattern (MVC, Clean, DDD, Layered)
    - Layer structure (directories and responsibilities)
    - Public APIs (all classes/functions with public visibility)
    - Entry points (main files, startup code)
    - Dependencies (external packages, internal modules)
    - Key workflows (user flows, data flows)

    Return JSON:
    {
        'architecture_pattern': '...',
        'layers': {...},
        'public_apis': [...],
        'entry_points': [...],
        'dependencies': {...}
    }"
)
```

**Returns**: Structured JSON with code metadata

---

## Reference Files

Load these on-demand during workflow execution:

### Core Workflow
- **documentation-standards.md** (~450 lines) - Style guide, formatting, Mermaid diagrams
- **greenfield-workflow.md** (~380 lines) - Story extraction, content generation
- **brownfield-analysis.md** (~520 lines) - Codebase scanning, gap identification
- **diagram-generation-guide.md** (~410 lines) - Mermaid syntax, flowcharts, sequences
- **template-customization.md** (~290 lines) - Variable substitution, custom templates
- **post-generation-workflow.md** (~300 lines) - Module name derivation, section insertion map, README/CHANGELOG/story updates, idempotency
- **anti-aspirational-guidelines.md** (~100 lines) - Prohibited language, structural rules, content quality enforcement

**Total reference content:** ~2,450 lines (loaded progressively as needed)

---

## Template Library

### Available Templates

**Location:** `assets/templates/`

1. **readme-template.md** - Project overview, installation, quick start
2. **developer-guide-template.md** - Architecture, development workflow, conventions
3. **api-docs-template.md** - API reference, endpoints, schemas, examples
4. **troubleshooting-template.md** - Common issues, solutions, debugging
5. **contributing-template.md** - Contribution guidelines, PR process, standards
6. **changelog-template.md** - Version history, release notes, breaking changes
7. **architecture-template.md** - System design, diagrams, ADRs

### Template Variables

Common variables across all templates:
- `{{project_name}}` - From context or story
- `{{project_description}}` - From story or codebase
- `{{tech_stack}}` - From tech-stack.md
- `{{installation_steps}}` - Generated from dependencies.md
- `{{usage_examples}}` - From acceptance criteria
- `{{api_endpoints}}` - From technical specifications
- `{{architecture_diagram}}` - Generated Mermaid diagram
- `{{version}}` - From git tags or package.json

---

## Success Criteria

This skill succeeds when:

- [ ] Documentation files generated/updated
- [ ] All required sections present
- [ ] Documentation coverage ≥80% (if quality gate)
- [ ] Mermaid diagrams render correctly
- [ ] Framework constraints respected
- [ ] Story file updated (if story-based)
- [ ] Export formats created (if requested)
- [ ] Token usage <50K (isolated context)

**The goal: Comprehensive, maintainable documentation that stays current with codebase.**

---

## Quality Gate Integration

**For `/release` command integration:**

When invoked by release command:
- Validate documentation coverage ≥80%
- Check README.md exists and is current (updated in last 90 days)
- Verify all public APIs have documentation
- **BLOCK release** if threshold not met

**Quality gate procedure:**

```
# Phase: Documentation Quality Gate (in release command)

Skill(command="devforgeai-documentation")
# Skill operates in validation-only mode

result = skill_result

IF result.coverage < 80:
    Display: "❌ Release blocked: Documentation coverage {result.coverage}% < 80%"
    Display: "Missing documentation for:"
    FOR api in result.undocumented_apis:
        Display: "  - {api.name} ({api.location})"

    AskUserQuestion: "How to proceed?"
    Options:
    - Generate missing documentation now
    - Skip documentation gate (not recommended)
    - Abort release

ELSE:
    Display: "✅ Documentation quality gate passed ({result.coverage}%)"
    Proceed with release
```

---

## Token Efficiency

**Estimated token usage:**

- **Phase 0-1** (Detection, Discovery): ~8,000 tokens
- **Phase 2** (Content Generation with subagents): ~35,000 tokens (isolated)
- **Phase 3** (Template Application): ~3,000 tokens
- **Phase 4** (Integration): ~2,000 tokens
- **Phase 5** (Validation): ~2,000 tokens
- **Total**: ~50,000 tokens (with subagent work isolated)

**Efficiency techniques:**
- Use native tools (Read, Write, Glob, Grep) - 40-73% savings vs Bash
- Progressive reference loading (only load needed guides)
- Subagent isolation (heavy analysis in separate context)
- Minimal file operations (targeted reads, single writes)

---

## Error Handling

### Error 1: Context Files Missing
```
Error: "Context files required. Run /create-context first."
Action: HALT, direct user to architecture setup
```

### Error 2: No Stories Found (Greenfield Mode)
```
Error: "No completed stories found. Nothing to document."
Action: Suggest running /qa on stories first OR switch to brownfield mode
```

### Error 3: Diagram Syntax Error
```
Error: "Mermaid diagram syntax invalid"
Action: Attempt auto-fix, fallback to text-only documentation
```

### Error 4: Export Failed (Missing Dependencies)
```
Error: "PDF export requires wkhtmltopdf or pandoc"
Action: Display install command, fallback to Markdown
```

### Error 5: Documentation Coverage Below Threshold
```
Error: "Coverage 65% < 80% (quality gate)"
Action: List undocumented APIs, ask user for next steps
```

---

## Framework Integration Notes

**This skill complements the existing SDLC:**

```
Dev Complete → /qa → Documentation → /release
```

**Quality gates enforced:**
- Documentation coverage ≥80%
- README.md exists and current
- Public APIs documented
- Diagrams render correctly

**Files updated:**
- Story files (add documentation references)
- CHANGELOG.md (version notes)
- Context files (if customizations added)

---

## Phase A: Documentation Audit (--audit=dryrun)

**⚠️ This phase executes ONLY when Mode Router selects audit path.**

**Reference:** Load `references/audit-workflow.md` before executing.

### Phase A.0: Discovery

1. **Inventory docs files:**
   ```
   docs_files = Glob("docs/**/*.md")
   root_md = Glob("*.md")
   ```

2. **Read entry points** (README.md, docs/README.md, docs/index.md if they exist)

3. **Inventory community files** — check existence of:
   - LICENSE / LICENSE-MIT / LICENSE-APACHE
   - CONTRIBUTING.md, CODE_OF_CONDUCT.md, SECURITY.md
   - .github/ISSUE_TEMPLATE/ (bug_report.md, feature_request.md)
   - .github/PULL_REQUEST_TEMPLATE.md

4. **Check configuration alignment:**
   - Read project manifest (Cargo.toml / package.json / pyproject.toml)
   - Extract: license field, MSRV/engine version, project version
   - Compare against README prerequisites and docs references
   - Record all discrepancies

### Phase A.1: Analysis

Score 4 dimensions (1-10 each) with evidence. Reference `audit-workflow.md` for full rubric.

**Dimension 1: Tone & Personality**
- Check README opening for WHY vs WHAT
- Check for value proposition / elevator pitch
- Check contributor language (welcoming vs gatekeeping)
- Check for human voice (we/you pronouns)
- Check troubleshooting for empathetic language

**Dimension 2: Information Architecture**
- Detect duplicate filenames across directories
- Check for scope confusion (mixed versions/products)
- Check for navigation index (docs/README.md or docs/index.md)
- Check for cross-references between related docs
- Check for audience-based routing
- Check for over-documented modules (>3 files for one module)

**Dimension 3: Visual Design & Formatting**
- Check for GFM admonitions (`> [!NOTE]`, `> [!WARNING]`, etc.)
- Check for README badges
- Check CHANGELOG for Keep a Changelog categories
- Check for oversized files (>50KB)
- Check for tables with >10 rows and no visual grouping

**Dimension 4: Onboarding Friction**
- Check install steps in first 50 lines of README
- Check for Quick Start narrative
- Check prerequisites consistency across docs
- Check LICENSE presence
- Check MSRV/version consistency with manifest

**Orphan Detection:** Run the orphan detection algorithm from `audit-workflow.md` to identify files with zero inbound references.

### Phase A.2: Prioritization

Classify each finding:
- **Severity:** CRITICAL (-3 points), HIGH (-2), MEDIUM (-1), LOW (-0.5)
- **Type:** `category:specific` key from `audit-fix-catalog.md`
- **Fix mode:** `automated` or `interactive` per fix catalog
- **Fix action:** action key from fix catalog

Assign sequential IDs (F-001, F-002, ...) ordered by severity.

### Phase A.3: Output

Ensure directory exists:
```
Bash("mkdir -p devforgeai/qa/audit")
```

Write structured JSON to `devforgeai/qa/audit/doc-audit.json` with schema:
- `version`, `generated`, `project_root`
- `scorecard` (4 dimensions with score, max, key_blocker)
- `findings` array (id, severity, type, affected, summary, evidence, remediation, fix_mode, fix_action)
- `inventory` (docs_files, community_files, orphaned_files, duplicate_groups)
- `fix_sessions` (empty array for first run)

### Phase A.4: Display

Display summary report:

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  Documentation Audit Complete
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Scorecard:
  Tone & Personality:      {score}/10 — {key_blocker}
  Information Architecture: {score}/10 — {key_blocker}
  Visual Design:           {score}/10 — {key_blocker}
  Onboarding Friction:     {score}/10 — {key_blocker}

Findings: {critical} CRITICAL, {high} HIGH, {medium} MEDIUM, {low} LOW

Top findings:
  F-001 [CRITICAL] {summary}
  F-002 [CRITICAL] {summary}
  F-003 [HIGH]     {summary}
  ...

Next Steps:
  • /document --audit-fix --type=all     Apply all fixes
  • /document --audit-fix --type=license Fix license only
  • /document --audit-fix --finding=F-001 Fix single finding

Audit saved: devforgeai/qa/audit/doc-audit.json
```

**EXIT after display. Do not proceed to Phases 0-7.**

---

## Phase B: Documentation Fix (--audit-fix)

**⚠️ This phase executes ONLY when Mode Router selects audit-fix path.**

**References:** Load `references/audit-fix-catalog.md` and `references/audit-workflow.md` before executing.

### Phase B.0: Load Findings

1. Read `devforgeai/qa/audit/doc-audit.json`
   - If not found: HALT with "No audit file found. Run `/document --audit=dryrun` first."

2. Parse findings array

3. **Filter by --type** (if provided):
   ```
   IF type_filter != "all":
       findings = findings.filter(f => f.type.startsWith(type_filter))
   ```

4. **Filter by --finding** (if provided):
   ```
   IF finding_filter != "all":
       findings = findings.filter(f => f.id == finding_filter)
   ```

5. **Skip previously applied findings:**
   ```
   FOR each session in fix_sessions:
       FOR each detail in session.details:
           IF detail.status == "applied":
               findings = findings.filter(f => f.id != detail.id)
   ```

6. Display: "Loaded {count} findings to process ({skipped} previously applied)"

### Phase B.1: Classify

Group filtered findings by fix_mode:
- `automated_findings` — deterministic, safe to apply
- `interactive_findings` — require user approval per action

Display:
```
Fix plan:
  {n} automated fixes (will apply without prompting)
  {m} interactive fixes (will ask for approval)
```

### Phase B.2: Preview

Display all planned changes in a summary table:

```
| ID | Type | Action | Target File | Mode |
|----|------|--------|-------------|------|
| F-001 | license:missing | create_dual_license | LICENSE-MIT, LICENSE-APACHE | interactive |
| F-003 | community:contributing | create_contributing | CONTRIBUTING.md | automated |
| F-007 | formatting:missing_badges | insert_badges | README.md | automated |
| ... | ... | ... | ... | ... |
```

AskUserQuestion: "Proceed with {n} automated + {m} interactive fixes?"
- Options: "Proceed" / "Auto-only (skip interactive)" / "Cancel"

IF "Cancel": EXIT
IF "Auto-only": Remove interactive_findings from execution list

### Phase B.3: Execute

**For each automated finding (in order):**

1. Load fix action from catalog
2. Read target file(s)
3. Apply transformation (create file from template, insert text, replace text)
4. Write result
5. Log: `"✓ F-{id}: {action} → {file}"`

**For each interactive finding (in order):**

1. Load fix action from catalog
2. Generate proposed change
3. Display before/after diff or new file preview
4. AskUserQuestion:
   - "Apply" — execute the fix
   - "Edit first" — user provides modified text, then apply
   - "Skip" — mark as deferred
5. Log result

**Template variable resolution** (for file creation actions):
- Read project manifest for: {{project_name}}, {{version}}, {{license}}
- Detect from codebase: {{test_command}}, {{lint_command}}, {{format_command}}, {{msrv}}
- Use git remote for: {{repo_url}}
- AskUserQuestion for: {{contact_email}}, any unresolvable variable
- Fallback: {{project_name}} = directory name

### Phase B.4: Verify

After all fixes applied:

1. **Re-run orphan detection** — ensure no new orphans created
2. **Check link integrity** — all entry points still reference expected files
3. **Check fact consistency** — MSRV, version numbers still match
4. **Check community files** — re-inventory, report remaining gaps

Display verification results:
```
Verification:
  ✓ No orphaned files
  ✓ All links valid
  ✓ Facts consistent
  ⚠ 2 community files still missing (CODE_OF_CONDUCT.md, .github/FUNDING.yml)
```

### Phase B.5: Report

1. **Append fix session to doc-audit.json:**
   ```json
   {
     "timestamp": "...",
     "type_filter": "all|license|tone|...",
     "findings_processed": N,
     "automated_applied": N,
     "interactive_applied": N,
     "skipped": N,
     "details": [
       { "id": "F-001", "action": "...", "status": "applied|skipped", "reason": "..." }
     ]
   }
   ```

2. **Display summary:**
   ```
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
     Documentation Fix Complete
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

   Applied: {applied} fixes
   Skipped: {skipped} fixes (user deferred)
   Remaining: {remaining} findings not yet addressed

   Files created:  {list}
   Files modified:  {list}

   Next Steps:
     • Review changes before committing
     • Run /document --audit=dryrun to re-score
     • Commit with: git add ... && git commit
   ```

**EXIT after report. Do not proceed to Phases 0-7.**

---

**Created:** 2025-11-18
**Updated:** 2026-03-12 (added Phase A: Audit, Phase B: Fix)
**Status:** Production Ready
**Version:** 1.1.0
