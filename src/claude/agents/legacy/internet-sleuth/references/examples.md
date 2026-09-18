# Examples for Internet Sleuth

**Version**: 1.0 | **Status**: Reference | **Agent**: internet-sleuth

---

## Example 1: Competitive Analysis Research

```
Task(
  subagent_type="internet-sleuth",
  description="Research React vs Vue.js component architecture patterns",
  prompt="""
  Research Mode: competitive-analysis
  Epic: EPIC-042-Frontend-Architecture-Modernization

  Analyze top GitHub repositories for React and Vue.js component patterns:
  1. State management approaches (Redux vs Vuex vs Pinia)
  2. Composition patterns (hooks vs composition API)
  3. Testing strategies and coverage approaches
  4. Build system integration (Webpack vs Vite)
  5. Performance optimization patterns

  Validate all recommendations against tech-stack.md constraints.
  Compare 5 leading repositories per framework.
  Generate comparison matrix with scoring.
  """
)
```

**Expected Output:**
- Research report (RESEARCH-{NNN}-react-vs-vue-comparison.md)
- Comparison matrix: State management, composition, testing, build, performance
- Technology conflict resolution (if recommendations differ from tech-stack.md)
- Risk assessment (5+ risks with mitigation strategies)
- ADR readiness assessment

---

## Example 2: Repository Architecture Pattern Mining

```
Task(
  subagent_type="internet-sleuth",
  description="Mine implementation patterns from top TypeScript monorepo projects",
  prompt="""
  Research Mode: repository-archaeology
  Story: STORY-285-Implement-Monorepo-Structure

  Analyze GitHub repositories for TypeScript monorepo patterns:
  1. Package.json organization and workspaces structure
  2. Build system approach (Turbo, Nx, Lerna)
  3. Testing strategies across monorepo packages
  4. CI/CD pipeline configuration
  5. Development workflow (dependency management)

  Focus on: Next.js, Vercel, and established tech companies' repos.
  Extract code examples (file paths and snippets).
  Validate architecture against architecture-constraints.md.
  Identify anti-patterns from anti-patterns.md.
  """
)
```

**Expected Output:**
- Research report with code examples and architecture diagrams
- Build system comparison (Turbo vs Nx vs Lerna)
- Monorepo structure templates extracted from real projects
- Framework compliance section (validates against all 6 context files)
- Implementation guidance with proven patterns
