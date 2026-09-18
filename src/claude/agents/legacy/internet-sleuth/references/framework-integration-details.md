# Framework Integration Details for Internet Sleuth

**Version**: 1.0 | **Status**: Reference | **Agent**: internet-sleuth

---

## Context Files Awareness

The internet-sleuth agent must validate all research recommendations against these 6 context files:

1. **`devforgeai/specs/context/tech-stack.md`** (Locked Technologies)
   - **Purpose:** Defines approved frameworks, libraries, and platforms
   - **When to check:** Before recommending any technology
   - **Action if conflict:** Flag "REQUIRES ADR" and present AskUserQuestion

2. **`devforgeai/specs/context/source-tree/`** (Project Structure)
   - **Purpose:** Defines directory organization and file naming conventions
   - **When to check:** When recommending project structure patterns
   - **Action if conflict:** Align recommendations with existing structure

3. **`devforgeai/specs/context/dependencies.md`** (Approved Packages)
   - **Purpose:** Lists approved dependencies with versions
   - **When to check:** Before recommending new packages
   - **Action if conflict:** Flag package and recommend ADR if beneficial

4. **`devforgeai/specs/context/coding-standards.md`** (Code Patterns)
   - **Purpose:** Defines naming conventions, code style, patterns
   - **When to check:** When analyzing repository code patterns
   - **Action if aligned:** Highlight as matching existing standards

5. **`devforgeai/specs/context/architecture-constraints.md`** (Layer Boundaries)
   - **Purpose:** Defines dependency rules, layer isolation, integration boundaries
   - **When to check:** When recommending architectural patterns
   - **Action if conflict:** Note violation and recommend alternatives

6. **`devforgeai/specs/context/anti-patterns.md`** (Forbidden Patterns)
   - **Purpose:** Lists prohibited patterns (God Objects, SQL injection, hardcoded secrets, etc.)
   - **When to check:** During repository pattern extraction
   - **Action if found:** Explicitly mark as anti-pattern and recommend alternatives

## ADR Integration

- Check `devforgeai/specs/adrs/` directory before recommending technology changes
- If ADR exists: Reference it in recommendations
- If no ADR and technology conflicts: Recommend creating ADR with proper naming format
- **Technology Conflict Workflow:** When ADR conflict requires user decision, use AskUserQuestion pattern to present conflict resolution options (Update tech-stack.md + create ADR, Adjust research scope, or defer as follow-up). See Technology Conflict Resolution section below for full implementation pattern and code examples

## Technology Conflict Resolution (ADR Conflict Workflow with AskUserQuestion Options)

When research discovers technology that conflicts with tech-stack.md, use AskUserQuestion to present ADR conflict resolution options with three choices: (1) Update tech-stack.md and create ADR for technology change, (2) Adjust research scope to existing tech stack, or (3) Defer as follow-up investigation. This AskUserQuestion pattern is the standard DevForgeAI approach for ADR decisions.

**Example:**

```
AskUserQuestion(
    questions=[{
        question: "Technology conflict detected: Research recommends {new-tech} but tech-stack.md specifies {existing-tech}. How should we proceed?",
        header: "Tech Conflict",
        multiSelect: false,
        options: [
            {
                label: "Update tech-stack.md and create ADR",
                description: "Accept new technology and document decision in ADR-{NNN}-{tech-decision}.md"
            },
            {
                label: "Adjust research scope to existing stack",
                description: "Continue research using {existing-tech} patterns only"
            },
            {
                label: "Mark as follow-up investigation",
                description: "Document conflict and defer decision to later sprint"
            }
        ]
    }]
)
```

## Framework-Aware Behavior

- Agent operates within DevForgeAI constraints (not autonomously)
- All technology recommendations validated against context files
- Conflicts trigger user interaction (AskUserQuestion) rather than autonomous decisions
- Research outputs reference framework compliance explicitly

## Invoked By

- spec-driven-ideation skill (Phase 5: Feasibility Analysis)
- spec-driven-system-architecture skill (Phase 2: Create Context Files)

## Works With

- requirements-analyst (coordinates on epic feature technology requirements)
- architect-reviewer (validates technical feasibility of research findings)

## Invokes

- context-validator (quality gate validation against 6 context files) - NEW Phase 2
- requirements-analyst (optional: requirement synthesis)
- architect-reviewer (optional: architecture pattern evaluation)
