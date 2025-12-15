# Implementation Prompt: DevForgeAI Ideation Skill

Copy and paste this prompt to Claude Code to begin implementing the devforgeai-ideation skill:

---

## Prompt for Claude

I need you to implement the **devforgeai-ideation** skill for the DevForgeAI spec-driven development framework. This is the entry point skill that transforms business ideas into structured requirements.

**Context:**
- The complete design specification is in: `devforgeai/specs/requirements/devforgeai-ideation-skill-design.md`
- Use the skill-creator template as your guide: `.claude/skills/skill-creator/skill.md`
- Follow the implementation roadmap in: `devforgeai/specs/requirements/devforgeai-skills-implementation-roadmap.md`
- Reference existing skills for patterns: `.claude/skills/devforgeai-architecture/SKILL.md`, `.claude/skills/devforgeai-orchestration/SKILL.md`

**Implementation Requirements:**

1. **Read the design specification first:**
   - Read `devforgeai/specs/requirements/devforgeai-ideation-skill-design.md` (complete specification)

2. **Create the skill structure:**
   ```
   .claude/skills/devforgeai-ideation/
   ├── SKILL.md (main skill file)
   ├── references/
   │   ├── requirements-elicitation-guide.md
   │   ├── complexity-assessment-matrix.md
   │   ├── domain-specific-patterns.md
   │   └── feasibility-analysis-framework.md
   ├── assets/
   │   └── templates/
   │       ├── epic-template.md
   │       ├── requirements-spec-template.md
   │       ├── user-persona-template.md
   │       └── feature-prioritization-matrix.md
   └── scripts/
       ├── complexity_scorer.py
       ├── requirements_validator.py
       └── README.md
   ```

3. **Implementation Order:**
   - Phase 1: Create SKILL.md with YAML frontmatter and all 6 workflow phases
   - Phase 2: Create 4 reference files
   - Phase 3: Create 4 asset templates
   - Phase 4: Create 2 Python scripts
   - Phase 5: Test and validate

4. **Key Requirements:**
   - Use IMPERATIVE/INFINITIVE form (not second person) throughout
   - Include 15+ AskUserQuestion patterns from the design spec
   - Follow the 6-phase workflow exactly as specified
   - Use native tools (Read, Write, Edit, Glob, Grep) NOT Bash for file operations
   - Token budget: ~80,000 tokens total
   - Ensure complexity scoring algorithm is included (0-60 points, 4 tiers)

5. **Critical Design Principles:**
   - **"Ask, Don't Assume"** - Use AskUserQuestion for ALL ambiguities
   - **"Start with Why, Then What, Then How"** - Business value before technical details
   - **"Right-size the Solution"** - Progressive complexity assessment (simple → enterprise)
   - Support both greenfield and brownfield projects
   - Progressive disclosure (keep SKILL.md lean, details in references/)

6. **Integration Points:**
   - Output: Epic documents (`devforgeai/specs/Epics/`) and Requirements specs (`devforgeai/specs/requirements/`)
   - Handoff to: devforgeai-architecture (create context files) and devforgeai-orchestration (create sprints/stories)
   - Auto-invoke architecture skill if context files missing

7. **Quality Checklist:**
   - [ ] YAML frontmatter is valid and complete
   - [ ] All 6 workflow phases implemented in SKILL.md
   - [ ] 15+ AskUserQuestion patterns documented
   - [ ] 4 reference files created with comprehensive content
   - [ ] 4 asset templates created
   - [ ] 2 Python scripts implemented and tested
   - [ ] Integration points clearly documented
   - [ ] Success criteria section included
   - [ ] Examples provided (e-commerce walkthrough)

**Start by reading the design specification, then create the skill structure, and implement each component in order. Ask me questions if anything in the design is unclear.**

Let's begin with Phase 1: Creating SKILL.md.
