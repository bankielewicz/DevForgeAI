# Conversion Rules

Use this reference when extracting the source contract and adapting host-specific behavior for a Claude Code target. The common source is a Codex CLI package, but the same classification applies to any portable Agent Skills package. Do not apply transformations to names, citations, or examples that legitimately describe another host as domain content.

## Preserve meaning

Classify each instruction by its effect: domain knowledge, input/output contract, permission boundary, host mechanism, duplication, or unsupported assertion. Keep information that changes a decision, preserves a constraint, or improves an output. Keep concrete examples when they clarify a real ambiguity.

Before omitting or consolidating a file, trace its callers and links. Retain copyright/license notices and material provenance. A file that is not linked from SKILL.md can still be a required template or script input.

Preserve the output schema and version by default. Do not relax required fields to hide missing behavior. Do not claim downstream compatibility without inspecting the relevant consumer within scope. Record an out-of-scope consumer as unverified, not compatible.

## Map host features

| Source feature | Claude Code treatment |
| --- | --- |
| `name`, `description` | Preserve valid existing identities, including the 64-character boundary. For a new name, prefer concise lowercase letters/digits and single hyphens with no leading/trailing hyphens. The description carries the entire trigger, so fold any separate "when to use" prose into it; record any authorized normalization. |
| `agents/openai.yaml` `interface.display_name` / `short_description` | No separate metadata file exists. Merge the substantive naming and blurb into `name` and `description`, then drop the file — a converted Claude Code package that still carries `agents/openai.yaml` is carrying dead configuration. |
| `interface.icon_small` / `icon_large` / `brand_color` / `default_prompt` | No equivalent. Record them as unreproduced source metadata in the contract. Do not invent frontmatter keys to hold them, and do not retain `$skill-name` prompt syntax, which Claude Code does not substitute. |
| `policy.allow_implicit_invocation: false` | `disable-model-invocation: true`. Preserve explicit-only intent; keep normal implicit discovery otherwise. |
| `dependencies.tools` (MCP) | Record the required server and transport as a capability and a side effect. Claude Code configures MCP at the project or user level, not inside a skill package, so the dependency becomes a documented prerequisite rather than a declaration the skill can make. |
| Declared capabilities and side effects in the source contract | Derive `allowed-tools` from them. This is a capability the source host did not offer: a constraint that was prose there can become an actual boundary here. Grant the minimum the workflow needs — see [claude-frontmatter.md](claude-frontmatter.md). |
| `model` / effort assumptions | Omit unless the task genuinely needs an override. An absent key inherits the configured session; a written key asserts a decision the requirements must support. |
| Terminal-conversation clarification | `AskUserQuestion` is available and is the better shape for a bounded decision with known options. Use it where the source had to ask in prose, and keep asking only for what materially changes behavior. |
| Explicit `$skill-name` invocation | Claude Code invokes a skill by `/skill-name` or through the `Skill` tool. Translate the syntax; do not retain unsupported substitution. |
| Bundled script paths | Keep bundled references relative to the loaded skill directory. Keep project outputs relative to the resolved project root. Never hardcode an installation root such as `.claude/skills/...` into a generated package — it may be loaded from a different location in the next project, and a baked-in path breaks it there. |
| Skill-local worker contracts | `Task` provides real subagent isolation, so an independence requirement the source could only describe can now be executed. Grant `Task` only when delegated work is genuinely part of the contract; a worker contract is still not an enforced permission boundary. |
| Handoff to a downstream skill | `Skill` can invoke another skill directly. When the design requires stopping at a handoff artifact instead, omit `Skill` from `allowed-tools` so the boundary is structural rather than asserted. |
| Dynamic shell injection | Never run it during inspection. Replace a necessary operation with an explicit authorized step; remove automatic injection semantics. |
| Host hooks and legacy CLI calls | Record required properties and incompatibilities outside executable instructions. Do not read/port excluded implementations or leave dead calls in the target. |

Preserve unrelated existing target metadata on revision. Do not generate frontmatter keys without a concrete need. Implicit discovery never supplies missing input or authorization.

Use the shared contract and worker guidance in [spec-build.md](spec-build.md) to record requirement source locations, artifact ownership, dependencies, and executable worker behavior. Import retains full source accounting; provenance does not replace per-file dispositions.

## Remove ceremony without deleting requirements

| Source pattern | Conversion |
| --- | --- |
| Ask at least N questions | Ask for required missing information; reuse answers already supplied. Retain a question count only as descriptive data if the output contract uses it. |
| Read every file again to prove compliance | Read the resources needed for the current work; independently inspect resulting artifacts where relevant. A read event proves neither comprehension nor correctness. |
| EXECUTE/VERIFY/RECORD repeated around every sentence | Express the useful action once and define the artifact or evidence it produces. |
| Entry Gate / Exit Gate wrapping every phase | Keep a boundary only where something real happens at it — an artifact becomes available, or a condition genuinely stops the work. Delete the rest. |
| Estimate context usage above a fixed percentage | Save material working state and provide an explicit resume path without claiming an unavailable measurement. |
| Hidden rubric or confidence score proves success | Retain substantive quality criteria; remove self-scoring as acceptance authority. |
| CLI missing: proceed as though gates passed | Remove the unsupported claim. Produce an agreed draft without acceptance or report the essential dependency as blocked. |
| Future commands in an installation/README template | Remove fictitious execution guidance or defer the template with rationale. Do not initialize or install a project merely because the source contains scaffolding. |
| Old checkpoint wins over current correction | Preserve original exchanges and append the correction; current explicit user instructions determine the working interpretation. |

Example: replace "Ask three questions and mark the phase PASS" with "Capture the analysis scope and success criteria; ask for either if missing." This preserves the data requirement without a ritual count or false acceptance claim.

Example: preserve a business-analysis HTML data-island identifier and schema while using its existing draft status when agreed. Do not label the file accepted or schema-validated unless those operations actually occurred.

## Runtime boundary and manual assessment

Framework authority remains separate compiled-Rust design. Builder performs authoring custody only. Structural checks, grader profiles, generated-script execution and independent trials belong to the later independent assessment. Do not generate evaluator campaigns as part of authoring. Preserve required runtime capabilities; unavailable essential enforcement remains a concrete gap, never advisory prose presented as enforcement.

## Capability evidence

Use the current host's available tools and read-only CLI help/version evidence. Record missing capabilities. A version number is not proof that a hook, subagent, or permission policy is installed or qualified. Do not change configuration or use bypass flags to make a compatibility claim.

When a specific mapping remains uncertain, inspect local guidance first and consult the relevant primary source if needed. Record the fetched URL/section and date; do not substitute a search snippet for evidence:

- [Claude skills](https://code.claude.com/docs/en/skills): target-host discovery, frontmatter and invocation semantics.
- [Agent Skills specification](https://agentskills.io/specification): portable package contract.
- [Codex skills](https://learn.chatgpt.com/docs/build-skills): source-host discovery and invocation metadata.

These references support targeted decisions; they are not mandatory full-document reads for every import.
