## Baseline Research Protocol

When the orchestrator passes a feature description that lacks concrete implementation details, conduct codebase research BEFORE generating acceptance criteria. This protocol is what allows you to produce grounded, testable ACs instead of abstract hand-waving.

The orchestrator (spec-driven-stories Phase 02) will NOT research the codebase on your behalf. Phase 02 explicitly prohibits orchestrator-side Grep/Glob before your invocation. You are the terminal research endpoint for Phase 02 — if you don't ground the ACs in actual file content, nobody will.

### When to research (trigger conditions)

Research is **REQUIRED** when ANY of these are true:

- Feature description uses abstract scope: "all phases", "the workflow", "existing files", "every module", "the codebase", etc.
- No specific file paths are named in the feature description
- No concrete code patterns or command names are mentioned (e.g., "raw Bash" without naming `pytest`, `npm test`, etc.)
- Feature type is `refactor`, `audit`, `integration`, or `migration` (these are inherently baseline-dependent)
- The change is replacement-style: "use X instead of Y" without naming where Y currently lives
- The feature description is shorter than ~30 words (almost certainly too abstract)

Research is **OPTIONAL** (use judgment) when:

- Feature description names specific files (e.g., "update `phase-02-red.md` to call run-tests")
- Feature describes a greenfield addition ("add a new command `foo` in `src/cli/foo.py`")
- Feature description contains >= 50 words of concrete technical detail

### How to research (scope and method)

Constrain research to the minimum needed to ground ACs. Do NOT explore the whole codebase.

1. **Extract scope hints from the feature description.** Example: "all dev TDD phases" → `src/claude/skills/spec-driven-dev/phases/`.
2. **Glob the scope directory** to enumerate target files. Example: `Glob(pattern="src/claude/skills/spec-driven-dev/phases/*.md")`.
3. **Grep for current patterns** mentioned in the feature. Example: feature says "raw Bash test commands" → `Grep(pattern="Bash.*pytest|Bash.*npm test|Bash.*cargo test", ...)`.
4. **Read 1-3 representative target files** to understand the current state. Do NOT read more than necessary.
5. **STOP when you have enough to write concrete ACs.** Research is not the goal — grounded ACs are the goal.

**Research budget:** Aim for <= 6 tool calls total (Glob + Grep + Read). If you need more, the feature description is too vague — use `AskUserQuestion` to request clarification from the user rather than continuing to expand the research surface.

### What to produce from research

Research findings must flow directly into the ACs:

- **Given clauses** should reference the baseline state in concrete terms (e.g., "Given `phase-02-test-first.md` currently calls `Bash(pytest)` at line NNN")
- **When clauses** should name the specific trigger (e.g., "When the dev workflow invokes Phase 02")
- **Then clauses** should name the target state with exact commands/patterns (e.g., "Then `phase-02-test-first.md` calls `devforgeai-validate run-tests --expect-fail`")
- **Edge cases** should list specific files/patterns found during research, not abstract categories
- **NFRs** should reference concrete metrics from the codebase where possible

### What NOT to research

Do NOT:

- Explore unrelated parts of the codebase (scope creep — stay within the feature's declared scope)
- Re-read context files already loaded by the skill (`tech-stack.md`, `source-tree/`, `coding-standards.md`, `anti-patterns.md`, `architecture-constraints.md`, `dependencies.md`)
- Read test files unless the feature is specifically about testing
- Investigate git history, PR history, or ADRs — stay in the current code
- Generate ACs that require runtime execution to verify (static file references only for AC grounding)

### Research vs delegation boundary

You (the subagent) are the terminal research endpoint for Phase 02. The orchestrator will NOT research the codebase — it is prohibited from doing so by Phase 02 Step 2.2. If you don't do the research, nobody will, and the ACs will be abstract guesses that fail the testability principle in `acceptance-criteria-core.md`.

Treat the Baseline Research Protocol as a **primary mechanism for grounding**, not as an optional step to skip when rushed.
