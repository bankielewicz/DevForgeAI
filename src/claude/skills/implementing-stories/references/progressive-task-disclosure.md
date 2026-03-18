# Progressive Task Disclosure

**Purpose:** Create phase-specific tasks to reduce context bloat. Only 4-8 tasks for the current phase are shown instead of ~72 for all phases.

**Usage:** Each phase file references this shared template. Substitute `{PHASE_ID}` with the current phase identifier (e.g., "01", "02", "4.5", "5.5").

---

## Registry Read

```
registry_path = ".claude/hooks/phase-steps-registry.json"

result = Glob(pattern=registry_path)
IF result is empty:
    HALT: "Phase steps registry not found at {registry_path}. Ensure STORY-525 is complete."

Read(file_path=registry_path)

IF JSON parse fails:
    HALT: "Registry JSON is malformed. Validate .claude/hooks/phase-steps-registry.json"
```

## Phase Filtering

```
current_phase_id = "{PHASE_ID}"

phase_steps = registry[current_phase_id].steps

IF phase_steps is empty:
    Display: "No steps defined for phase {PHASE_ID} in registry"
```

## Task Creation

```
FOR each step in phase_steps:
    subject = "Step {PHASE_ID}.{step.id}: {step.check}"
    IF step.conditional == true:
        subject = subject + " (conditional)"

    TaskCreate(
        subject=subject,
        description=step.check,
        activeForm="Executing Step {PHASE_ID}.{step.id}"
    )
```

## Task Completion

```
// After completing each step:
TaskUpdate(taskId=${step_task_id}, status="completed")
```

## Error Handling

```
// Invalid step entries (missing id or check fields):
FOR each step in phase_steps:
    IF step.id is missing OR step.check is missing:
        Display: "Warning: Skipping invalid step entry: {step}"
        CONTINUE
```
