# Sprint Planner - Reference Data

**Context Files (Read-Only):**
- `devforgeai/specs/context/tech-stack.md` (referenced in sprint goals)
- `devforgeai/specs/context/source-tree/` (for story context)

**Reference Documentation:**
- `.claude/skills/spec-driven-lifecycle/references/sprint-planning-guide.md` (sprint planning patterns)
- `.claude/skills/spec-driven-lifecycle/references/workflow-states.md` (11-state machine)
- `.claude/skills/spec-driven-lifecycle/references/state-transitions.md` (valid transitions)

**DevForgeAI Framework:**
- Spec-driven development: Epic to Sprint to Story to Implementation
- Story is atomic work unit (1-5 story points)
- Capacity planning: 20-40 points per 2-week sprint
- Quality gates: Enforce workflow state machine
- No shortcuts: Every story must pass quality gates

---

**Token Budget**: < 40K per invocation
**Priority**: High (Core sprint planning)
**Model**: Opus (Complex workflow coordination)
**Context Isolation**: Yes (operates in isolated Task context)
