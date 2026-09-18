# Sprint Planner - Integration Notes

**Works with:**
- **spec-driven-lifecycle skill** - Called during sprint planning phase
- **spec-driven-dev skill** - Uses sprint context for development workflow
- **requirements-analyst subagent** - Provides story details for capacity calculation

**Invoked by:**
- `/create-sprint` command (lean orchestration pattern)
- spec-driven-lifecycle skill (plan-sprint entry point)
- Manual Task invocations

**Invokes:**
- None directly (isolated subagent context)
