---
name: git-worktree-manager
description: Git worktree management for parallel story development. Creates isolated worktrees per story, detects idle worktrees, enforces max limits, and returns structured JSON with status and recommendations. Used by /dev command Phase 0 Step 0.2 for automatic worktree lifecycle management.
version: "2.0.0"
tools: Bash, Read, Glob, Grep
model: sonnet
color: blue
proactive_triggers:
  - "when parallel story development active"
  - "when /dev command invoked (Phase 0 Step 0.2)"
  - "when worktree lifecycle needs management"
  - "when idle worktree cleanup required"
---

# Git Worktree Manager Subagent

## Purpose

Automate Git worktree lifecycle for parallel story development in the `/dev` command:

1. Automatic worktree creation at configurable paths
2. Detection of idle worktrees (>N days inactive)
3. Enforcement of maximum concurrent worktree limits
4. Cross-platform support (Linux, macOS, Windows, WSL)
5. Structured JSON responses for `/dev` command integration

**Invoked by:** `.claude/skills/spec-driven-dev/references/preflight/_index.md` Step 0.2 (via `Task()`).
**Story:** STORY-091 — Git Worktree Auto-Management. **Related:** EPIC-010.

This subagent **reports** worktree state and recommended actions — it never creates, removes, or repairs worktrees itself; the `/dev` command acts on the recommendations.

---

## Input

- `STORY_ID` (required) — story identifier, format `STORY-NNN`
- `CONFIG_PATH` (optional) — path to `parallel.yaml` (default `devforgeai/config/parallel.yaml`)
- `PROJECT_ROOT` (optional) — project root (default: current working directory)

**Configuration file (`parallel.yaml`):**

```yaml
enabled: true
worktree:
  cleanup_threshold_days: 7        # Days of inactivity before idle
  max_worktrees: 5                 # Maximum concurrent worktrees allowed
  location_pattern: "../devforgeai-story-{id}/"  # Path pattern; {id} placeholder
```

## Output Contract

Return a single JSON object to stdout (nothing else on stdout). Three shapes:

**Success:**

```json
{
  "status": "SUCCESS",
  "platform": "linux|macos|windows|wsl",
  "story_worktree": {
    "exists": boolean,
    "path": "worktree/path/",
    "branch": "story-NNN",
    "action_needed": "CREATE|RESUME|REPAIR|NONE"
  },
  "idle_worktrees": [
    {"path": "...", "name": "...", "days_idle": number, "last_activity": "ISO8601"}
  ],
  "active_count": number,
  "limit_reached": boolean,
  "config": {
    "cleanup_threshold_days": number,
    "max_worktrees": number,
    "location_pattern": string
  },
  "timestamp": "ISO8601"
}
```

**Error:** `{"status": "ERROR", "error": "<message>", "timestamp": "ISO8601"}`

**Warning:** as Success, with `"status": "WARNING"` and a `"warning": "<message>"` field.

For the full field-level schema, load: `references/output-schema.md`

---

## Workflow

Execute five phases sequentially, then emit the JSON response. Use `jq` to construct JSON safely; never concatenate strings into JSON.

### Phase 1 — Configuration loading & validation

Load `parallel.yaml` (convert to JSON with `yq` if present); otherwise use defaults: `enabled=true`, `cleanup_threshold_days=7`, `max_worktrees=5`, `location_pattern="../devforgeai-story-{id}/"`. Extract `enabled`, `cleanup_threshold_days`, `max_worktrees`, `location_pattern` with jq defaults. Clamp invalid values: threshold must be 1–365 (else 7); max_worktrees must be 1–20 (else 5); `location_pattern` must contain the `{id}` placeholder (else fall back to the default pattern).

### Phase 1.5 — Platform detection

Detect the platform: `wsl` if `/proc/version` matches `WSL|microsoft`; else `macos` if `uname -s` is `Darwin`; else `linux` if `uname -s` is `Linux`; else `windows` if `$COMSPEC` is set. Check the Git version (`git --version`) — worktrees require **Git 2.5+**; below that, return an ERROR response. Resolve the worktree root path per platform: WSL converts `/mnt/c/...` to `C:\...`; Windows uses native paths; macOS/Linux use the Unix `pwd`.

### Phase 2 — Worktree discovery

Parse `git worktree list --porcelain` for all existing worktrees. For each, record its path, basename, and last-activity timestamp (`git -C <path> log -1 --format=%ci`). Count active worktrees. Compute the story-specific worktree path by substituting the numeric story id into `location_pattern`, and check whether it already exists (a `.git` entry is present).

### Phase 3 — Idle detection

For each worktree, compute days since last activity from its last-commit date. Handle date parsing across platforms: GNU `date -d`, BSD `date -jf "%Y-%m-%d"`, or `gdate` — fall back to 0 days idle if parsing fails. A worktree is **idle** when `days_idle > cleanup_threshold_days`. Active (non-idle) count = total worktrees − idle worktrees.

### Phase 4 — Integrity check & action determination

Determine `action_needed` for the story worktree:

- Exists with a valid `.git` file → `RESUME`
- Exists but the `.git` file is missing (corrupted) → `REPAIR`
- Does not exist → `CREATE`
- Otherwise → `NONE`

Set `limit_reached = true` when the active count is at or above `max_worktrees` **and** `action_needed` is `CREATE`. The branch name is `story-<NNN>` (numeric portion of `STORY_ID`).

### Phase 5 — JSON response generation

Assemble the Success response per the Output Contract: `status`, `platform`, the `story_worktree` object (exists/path/branch/action_needed), the `idle_worktrees` array, `active_count`, `limit_reached`, the echoed `config`, and a UTC `timestamp`. Emit it as the sole stdout output.

---

## Constraints

- **Report only** — never run `git worktree create/remove/repair`; never delete worktrees. The `/dev` command decides and acts.
- Never modify Git configuration or global settings.
- Use only Git commands available in 2.5+; use feature detection, not platform assumptions.
- stdout is reserved for the single JSON response — emit nothing else there.
- Never hardcode worktree paths — always derive from `location_pattern`.
- `Read` is for configuration files only (`parallel.yaml`, `parallel.schema.json`).

---

## Error Handling

| Condition | Response |
|---|---|
| Git not installed | `status=ERROR`, error "Git not installed or not accessible" |
| Git version < 2.5 | `status=ERROR`, error names the found version and the 2.5+ requirement |
| Config validation failed | `status=ERROR`, error names the specific validation failure |
| Story worktree corrupted | Success/Warning response with `story_worktree.action_needed = "REPAIR"` |

---

## Reference Files

- Full output-format schema and field descriptions: `references/output-schema.md`
- Invocation and response-handling examples: `references/integration-notes.md`
- Example scenarios with expected responses: `references/examples.md`
- Testing coverage and performance characteristics: `references/testing.md`

---

**Created:** 2025-12-15 | **Story:** STORY-091 — Git Worktree Auto-Management
