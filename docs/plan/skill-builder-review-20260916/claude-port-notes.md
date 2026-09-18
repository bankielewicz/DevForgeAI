---
id: DEVFORGEAI-SKILL-BUILDER-CLAUDE-PORT-20260916
target: claude-code
status: observation
recorded: "2026-09-16"
---

# skill-builder — Claude Code port build note

Records what was built at `src/claude/skills/skill-builder/` and `.claude/skills/skill-builder/` on 2026-09-16, and what was actually verified.

**This is not an `authoring-v1` record.** The package was written with ordinary file tools, not staged through `authoring.py` custody, so no contract, run directory, baseline or publication readback exists for it. Manufacturing a custody record after the fact would be exactly the fabricated-evidence pattern AGENTS.md prohibits. Treat this as a development note.

## Authorization

Maintainer instruction, 2026-09-16: "generate a Claude Code version of the skill-builder under src/claude/skills/ named skill-builder." CLAUDE.md requires confirming intent before adding to `src/claude/`, because that framework is legacy; this instruction is that confirmation. A follow-up instruction the same day established the deployment model and required removing hardcoded path wiring — see "Portability correction" below.

## Two CLAUDE.md statements are stale

Discovered while locating the target directory, and worth correcting alongside OQ-1 in [review-findings.md](review-findings.md):

1. **The mirror rule's premise no longer holds.** CLAUDE.md describes `.claude/` and `src/claude/` as "independent byte-identical copies — 896 files each, currently `diff -rq`-clean." At the time of the port, `src/claude/` held 896 files and **`.claude/` held zero** — only three empty directories.
2. **The legacy tree was reorganized.** All 896 files sit under `*/legacy/` subdirectories (`src/claude/skills/legacy/` and siblings). The paths CLAUDE.md names do not exist as described.

The new package sits at the non-legacy top level of each tree, which is where the instruction pointed and is consistent with the `legacy/` quarantine.

## Portability correction

The first draft of this port was wrong in a way that would have broken the framework in every consuming project, and the maintainer caught it. Recording the error and the fix, because the corrected contract differs from the Codex original's.

**The deployment model:** DevForgeAI is deployed into a consuming project's operational skills directory. Inside DevForgeAI itself, authored skills live in `src/claude/`. A consuming project's owner decides where their skills go — it is not DevForgeAI's call.

**What was wrong:**

- `SKILL.md` recommended `<project>/src/claude/skills/` as the destination parent. That is DevForgeAI's own layout baked in as a universal default.
- `authoring.py` carried `PROTECTED = {'.agents', '.claude', '.codex'}` and rejected any write whose path contained one of those components. Inherited byte-identical from the Codex original. In the Claude Code deployment model this is fatal: the skill could not author into `.claude/skills/`, which is precisely where a consuming project keeps its skills.
- `custody.py`'s `adoption_record` required `target_root == project + "/src/agents/skills/" + name`. Not dead code — `build_evidence.py adoption-plan` and two call sites in `authoring.py` reach it, so adoption would fail in any project not shaped like DevForgeAI-Codex.
- `check_project_binding.py` required each installed binding's `package_path` to equal `.claude/skills/<name>`, which is stricter than `adaptive-common.schema.json` itself, which asks only for a relative path.

**What changed:**

| Change | Effect |
| --- | --- |
| Deleted `PROTECTED` and its check in `authoring.py` | The destination is whatever the selected contract's `target_root` names. `EXCLUDED` (`.git`, `__pycache__`, backups, `devforgeai_cli`), traversal rejection and link/junction rejection all remain. |
| `safe(..., write=)` now marks caller intent only | Kept the signature rather than refactoring 10 call sites; documented in-line so the flag is not mistaken for a live policy gate. |
| `custody.py` adoption check made structural | Target must sit inside the project root with a final component equal to the name. Widening only — every target that passed before still passes. |
| `check_project_binding.py` binding check made structural | Final component must equal the member name; the parent is the project owner's choice. Now aligned with its own schema instead of stricter than it. |
| `SKILL.md` destination resolution rewritten | Discovery-ordered, with no baked-in default. |
| `SKILL.md` boundary paragraph rewritten | See below. |

**The boundary moved from a directory to an action.** The original said "Stop at development source. Operational `.claude`, `.agents`, `.codex` … are outside this workflow." That is now wrong for this host: writing the package into the project's live skills directory *is* the delivery. The replacement keeps what is still true — writing package files is authoring; hooks, settings registration, CI wiring, plugin assembly, MCP configuration and Rust implementation are installation and stay out of scope. Authoring a package into a skills directory does not authorize configuring the host around it. This is a deliberate contract change from the Codex original, not a path fix.

**Destination resolution is now discovery-ordered,** which is what keeps DevForgeAI's `src/claude/` convention and a consuming project's choice from colliding: (1) the current request, (2) the project's own instructions — `CLAUDE.md`/`AGENTS.md` — treated as policy input, (3) observed layout of existing skills, (4) ask via `AskUserQuestion`, offering the Claude Code convention alongside any discovered development tree and naming the evidence for each. DevForgeAI's own instructions answer at step 2; another project's owner answers at step 1 or 4. No default is carried between projects.

### The Codex original has the same two defects

Verified, and unfixed there — this is a finding about `src/agents/skills/skill-builder/`, not the port:

- Its `SKILL.md` recommends `<project>/src/agents/skills/`, DevForgeAI's own layout.
- Its `authoring.py` carries the same `PROTECTED` set, so it **cannot author into `.agents/skills/`** — its own deployment target. Confirmed by direct call: `safe('someproject/.agents/skills/newskill', write=True)` raises `operational destination rejected`.
- Its `custody.py` carries the same hardcoded `/src/agents/skills/` adoption check.

Deploy that package to another project and skill creation fails the same way. Not fixed here, because the Codex package was outside the scope of this instruction.

## What was built

45 artifacts plus `package-manifest.json`, identical in both copies. Accounting against the Codex original:

| Disposition | Count |
| --- | --- |
| Byte-identical | 33 |
| Adapted | 11 |
| New (`references/claude-frontmatter.md`) | 1 |
| Dropped (`openai_yaml.md`, `generate_openai_yaml.py`) | 2 |

Adapted: `SKILL.md`, `scripts/{authoring,adaptive,custody,init_skill}.py`, `assets/adaptive-runtime/check_project_binding.py`, `references/{conversion-rules,scaffolding,project-binding,adaptive-contracts,adaptation}.md`.

Eight of the thirteen references needed no change at all. That is the adaptive design working as intended.

### Why each adaptation was necessary

- **`SKILL.md`** — rewritten for the Claude Code host. Adds `allowed-tools`, a real capability boundary: omitting `Task` and `Skill` makes "do not spawn workers" and "do not invoke the assessor" structural rather than asserted. The Python allowance is wider than the contract, and SKILL.md says so plainly rather than implying the allowlist enforces the helper-only rule.
- **`init_skill.py`** — scaffolds Claude Code frontmatter (`allowed-tools`/`model`/`effort`, emitted only when supplied) instead of `agents/openai.yaml`. Dropped the `generate_openai_yaml` import. It has no default destination; the caller resolves it.
- **`authoring.py`** — the generated handoff said `$skill-validator` (Codex syntax), now `/skill-validator`; plus the `PROTECTED` removal above.
- **`adaptive.py`, `check_project_binding.py`, `project-binding.md`** — binding record path moved to the Claude Code host, and the installed-path check made structural.
- **`conversion-rules.md`** — the host-mapping table inverts: source is now Codex or any portable package, target is Claude Code. `openai.yaml` interface fields fold into frontmatter, `allow_implicit_invocation: false` becomes `disable-model-invocation: true`, declared capabilities become `allowed-tools`. The ceremony-removal table is direction-independent and kept verbatim, with one row added for Entry/Exit gates.
- **`adaptation.md`** — one sentence: "Stop at development source" became "Stop at the authored package; configuring the host around it is installation."

### `model` and `effort` are deliberately absent

17 of 19 legacy siblings pin `model: opus` and `effort: High`, and a first draft carried both. They were removed: this package's own `claude-frontmatter.md` says "Set only when the task genuinely needs it," and `conversion-rules.md` says "Omit unless the task genuinely needs an override." The Codex original declares no model at all, so adding one would be a new decision the source contract never made, taken by the one skill least able to afford contradicting its own references.

### Deliberate departure from the legacy siblings

The 19 skills under `src/claude/skills/legacy/` are built on phases, Entry/Exit gates and EXECUTE→VERIFY→RECORD. This package has none of that. `workflow-design.md` forbids imposing fixed phases and manufactured checkpoints, AGENTS.md bans ceremonial content, and the skill being ported is authoring-only with no gates to run.

## Verification actually performed

| Check | Result |
| --- | --- |
| Manifest integrity, both copies | 45 artifacts; 0 missing, 0 mismatch, 0 untracked |
| `diff -rq src/claude/… .claude/…` | empty |
| Byte-identity of copied files (CRLF safety) | 0 unintended divergence |
| Source Codex package still pristine | 46/47, clean |
| `SKILL.md` frontmatter parses as YAML | valid; `Task` absent, `Skill` absent |
| Internal link targets resolve | 0 missing |
| Adapted Python compiles | all OK |
| No hardcoded `src/` tree or install root anywhere in the package | none |
| `init_skill.py` end-to-end | correct Claude frontmatter, `Bash(python:*)` preserved intact, name normalized, occupied directory refused |
| **`begin` → `publish` targeting `<consumer>/.claude/skills/note-taker`** | **STAGED → AUTHORED, package delivered — the case that was broken before the fix** |
| `init_skill.py` into `<consumer>/.claude/skills` | succeeds |
| Adoption check widening | legacy `src/agents/skills/` shape still passes; `.claude/skills/`, `src/claude/skills/` and flat layouts now pass; outside-project, name-mismatch and project-root targets still rejected |

Smoke-test and scaffold artifacts were written to a session scratchpad and deleted; `__pycache__` from compile checks was removed before each manifest was generated.

## Not done

- **No skill-creator eval loop.** Its subagent test runs, grading and benchmark viewer were skipped. This is a port of a skill whose contract is fixed by three existing specs, so a 3-prompt behavioural benchmark would not have justified the cost. Available on request.
- **No Claude-side assessor exists.** The handoff names `/skill-validator`, a Codex package. The generated packet is still correct and reusable; `validation-handoff.md` specifies that an absent assessor does not block authoring.
- **Nothing installed.** No settings registration, no hooks. Both copies are package files only.
- **The Codex original's identical defects were not fixed.** Out of scope for this instruction; see above.

**Validation: NOT_PERFORMED. Testing: NOT_RUN.** The checks above are build-integrity and write-safeguard observations, not an assessment of the authored skill's behavior.
