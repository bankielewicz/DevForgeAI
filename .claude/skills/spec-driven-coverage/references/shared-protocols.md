# Shared Protocols: Spec-Driven Coverage

## Execute-Verify-Gate Pattern

Every mandatory step in this skill follows the EVG triplet:

1. **EXECUTE:** The exact action to perform — a specific tool call (Read, Glob, Grep, Bash, Task, Skill) or data operation
2. **VERIFY:** How to confirm the action happened — check file exists via Glob, content matches via Grep, exit code is 0, data key is populated
3. **RECORD:** CLI command to persist completion — `devforgeai-validate phase-record ${IDENTIFIER} --phase=NN --step=N.M --project-root=. 2>&1`

No step may be skipped, abbreviated, or declared "not applicable" without explicit user authorization.

---

## Self-Check Violations

If ANY of the following is true during execution, it is a VIOLATION — stop and correct immediately:

- [ ] Stopping to ask about token budget
- [ ] Stopping to offer execution options ("should I proceed?")
- [ ] Waiting passively for results
- [ ] Asking "should I execute this?"
- [ ] Skipping a phase because "it seems simple"
- [ ] Summarizing instead of loading a reference file via Read()
- [ ] Skipping a RECORD step because "the CLI might not be installed"
- [ ] Consolidating multiple phase reference loads into one

---

## Phase File Loading Protocol

Each phase file MUST be loaded via Read() at the start of that phase. Do not:
- Load all phase files at once during initialization
- Rely on memory of a phase file loaded in a previous invocation
- Summarize a phase file instead of loading it

The correct pattern:
```
# At the start of Phase NN:
Read(file_path="src/claude/skills/spec-driven-coverage/phases/phase-NN-{name}.md")
# If fails, try operational path:
Read(file_path=".claude/skills/spec-driven-coverage/phases/phase-NN-{name}.md")
```

---

## Reference File Loading Protocol

Reference files are loaded per-phase based on the Reference Files Index in SKILL.md. Each phase loads only the references it needs — no consolidated pre-loading.

---

## CLI Gate Backward Compatibility

The `devforgeai-validate` CLI may not be installed in all environments. Handle gracefully:

| Exit Code | Meaning | Action |
|-----------|---------|--------|
| 0 | Success | Continue normally |
| 2 | Identifier format not recognized | Continue — backward compatible |
| 127 | CLI not found | Continue without CLI gates — execute ALL steps regardless |

When CLI is unavailable, the remaining 3 anti-skip layers (reference loading, checkpoint state, artifact verification) still enforce execution discipline.

---

## Mode-Conditional Phase Execution

This skill supports 3 modes that determine which phases execute. The mode router sits in SKILL.md. Within each active phase, ALL steps are mandatory — the mode only controls which phases are active.

```
validate: Phases 00, 01, 02, 03
detect:   Phases 00, 01
create:   Phases 00, 01, 04, 05
```

A phase that is not in the active set is skipped entirely (not entered). A phase that IS in the active set must execute every step.
