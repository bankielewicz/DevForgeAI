# DevForgeAI

This repository contains development skills, a Rust index application, isolated Rust worker experiments, framework specifications, and retained evaluation records.

The components have different implementation and assessment scopes. The [framework specification collection](docs/specs/framework/index.md) remains a planning baseline; it does not describe a completed, installed workflow engine. A skill assessment or an experimental worker's offline test result is not framework-wide acceptance.

## Repository contents

| Location | Contents |
| --- | --- |
| [src/agents/skills/](src/agents/skills/) | Development packages for Codex skills, with their instructions and supporting resources. |
| [.agents/skills/](.agents/skills/) | Operational skill copies. Editing development source does not update these copies. |
| [src/claude/](src/claude/) | Claude skill and agent source, including historical workflows. |
| [.claude/](.claude/) | Local Claude agent, command, and skill copies. The local legacy skill directory is excluded from Git. |
| [devforgeai/](devforgeai/README.md) | Rust index application: CLI, daemon, and Windows tray source. |
| [devforgeai/experiments/](devforgeai/experiments/) | Separate Rust worker-probe packages, including the logging candidate and its QA fixes. |
| [docs/specs/framework/](docs/specs/framework/index.md) | Framework capability contracts, open decisions, and the first discovery-workflow specification. |
| [docs/plan/](docs/plan/) | Companion specifications, implementation records, and retained assessment evidence. |
| [docs/grok/](docs/grok/README.md) | Design visualizations; these do not replace the governing specifications. |

Repository instructions, execution boundaries, and quality requirements are in [AGENTS.md](AGENTS.md).

## Existing skill packages

| Package | Responsibility |
| --- | --- |
| [brainstorm](src/agents/skills/brainstorm/SKILL.md) | Explore selected product uncertainty and produce discovery discussion or a requested brief. |
| [dev](src/agents/skills/dev/SKILL.md) | Implement explicitly selected specifications through tests, refactoring, integration, and developer QA. |
| [qa](src/agents/skills/qa/SKILL.md) | Independently assess selected product work and return demonstrated defects for repair. |
| [story-create](src/agents/skills/story-create/SKILL.md) | Author selected stories from governing requirements and project context. |
| [skill-builder](src/agents/skills/skill-builder/SKILL.md) | Author skills and selected project adaptations. |
| [skill-validator](src/agents/skills/skill-validator/SKILL.md) | Assess identified skill packages and their behavioral evidence. |
| [advisor](src/agents/skills/advisor/SKILL.md) | Obtain a bounded Claude second opinion through its documented external-CLI contract. |

Read the selected package's instructions before use. Standalone `dev` does not require a project binding; the current `story-create` package does. Copying a package or naming a workflow does not satisfy its installation, binding, or runtime prerequisites.

The current `dev` and `qa` contracts have different quality-policy and stop rules. [MIG-01 and MIG-02](docs/specs/framework/roadmap-and-decisions.md#compatibility-and-migration-register) record those differences. This README does not change either contract.

## Rust implementation

The [index application](devforgeai/README.md) has source for project registration, index lifecycle operations, a daemon, and a Windows tray. Its CLI currently defines `daemon`, `project`, `index`, `job`, `environment`, and `tray` command groups. The [query CLI specification](docs/plan/devforgeai-index-query-cli-spec.md) is a separate contract; those query commands are not supplied by the current main CLI.

The worker probes are isolated experiments with their own Cargo manifests. The [2026-09-17 logging retest](docs/plan/framework-worker-logging/20260917T105456Z-qa-retest/qa-report.md) reports 178/178 required offline cases for its identified candidate and verifies QA-LOG-01 and QA-LOG-02. That report explicitly records native Codex as `NOT_RUN` and framework acceptance as `NOT_EVALUATED`. It is retained evidence for those bytes and that scope, not a current qualification of every component.

There is no repository-root Cargo manifest. For the main index package, the following commands run from the repository root and require its documented Rust/C toolchain and dependencies:

```powershell
cargo build --manifest-path .\devforgeai\Cargo.toml --locked
cargo test --manifest-path .\devforgeai\Cargo.toml --locked --all-targets
cargo fmt --manifest-path .\devforgeai\Cargo.toml --all -- --check
cargo clippy --manifest-path .\devforgeai\Cargo.toml --locked --all-targets -- -D warnings
```

These commands do not install the application, configure startup, or run the isolated experiments. Read the selected package's README and evidence before running its lifecycle operations. Documented commands are not a claim that this checkout has passed a fresh build or QA campaign.

## Framework contracts and work selection

The [core-workflow contract](docs/specs/framework/core-workflows.md) defines six capabilities: discovery/business analysis, architecture/design, work planning, development, independent QA, and delivery/follow-up. They are not a compulsory sequence. An adequate specification or a specified defect can enter development without a new brainstorm, PRD, or story.

The optional discovery route uses the selected names below:

| Workflow | Defined output | Implementation status |
| --- | --- | --- |
| [brainstorm](docs/specs/framework/workflows/phase-1-brainstorm-spec.md) | A discovery brief, named missing inputs, or a handoff that reuses an adequate existing artifact. | Development and operational packages exist. Their presence does not establish behavioral qualification. |
| `prd-create` | Product or feature requirements for review. | Named responsibility; full workflow specification and package not authored. |
| `prd-review` | Review of the identified PRD, architecture gaps, contradictions, and testability. | Named responsibility; full workflow specification and package not authored. |

Work planning and selected story creation follow when needed. Setup/activation is a [separate responsibility](docs/specs/framework/installation-and-integrations.md), not a mandatory phase 0. Its bootstrap and concurrent-worktree binding contracts remain open decisions.

Project facts and governing rules belong to [project context and policy](docs/specs/framework/project-context-and-policy.md). Stories reference canonical requirements and design decisions. [Core, variant, and expertise roles](docs/specs/framework/skills-and-project-expertise.md) have different responsibilities; none grants authority to rewrite policy or install itself.

The repository's framework implementation requires compiled Rust and the quality thresholds in AGENTS.md. Supporting Python tools and model-written records provide evidence; they do not issue protected acceptance. QA PASS does not itself authorize a merge or release. [Quality and delivery](docs/specs/framework/quality-and-delivery.md) defines these distinctions.

## Reading and continuing work

Start with the [framework index](docs/specs/framework/index.md), then select the document and component relevant to the requested outcome. The [roadmap](docs/specs/framework/roadmap-and-decisions.md) records unresolved decisions and separates discovery-workflow authoring from the runtime experiments. Its historical handoffs must be checked against the current candidate before reuse.

Reports under `docs/plan/` identify their own candidates, platforms, executed checks, and limitations. Preserve those distinctions when citing them. A specification describes required behavior; package source shows implementation; executed evidence supports only its declared assessment scope.

Git includes source, specifications and review records. Generated build trees, disposable trial workspaces/fixtures and bulky raw artifacts remain local under the ignore rules. Reports may reference those local artifacts or machine-specific paths; a Git checkout is not a complete copy of every historical evaluation run. The repository's attributes preserve exact bytes rather than normalizing line endings, because retained manifests contain file hashes.
