# Conversion Rules

Use this reference when extracting the source contract and adapting host-specific behavior. Do not apply transformations to names, citations, or examples that legitimately describe Claude as domain content.

## Preserve meaning

Classify each instruction by its effect: domain knowledge, input/output contract, permission boundary, host mechanism, duplication, or unsupported assertion. Keep information that changes a decision, preserves a constraint, or improves an output. Keep concrete examples when they clarify a real ambiguity.

Before omitting or consolidating a file, trace its callers and links. Retain copyright/license notices and material provenance. A file that is not linked from SKILL.md can still be a required template or script input.

Preserve the output schema and version by default. Do not relax required fields to hide missing behavior. Do not claim downstream compatibility without inspecting the relevant consumer within scope. Record an out-of-scope consumer as unverified, not compatible.

## Map host features

| Claude feature | Codex treatment |
| --- | --- |
| `name`, `description` | Keep the capability identity; describe what it does and when it applies. Use lowercase letters/digits and single hyphens for a normalized name; no leading/trailing hyphens; keep it under 64 characters. Record normalization. |
| Other metadata | Preserve useful fields supported by the target and its required structural checker. Move unsupported top-level fields into the conversion record; retain compatibility requirements in the instructions when the checker does not accept a `compatibility` field. |
| `model`, `effort` | Remove Claude-specific overrides and inherit the configured session. An explicitly requested override needs target-host support; do not invent a model mapping. |
| `allowed-tools` | Record required capabilities and side effects. Copied metadata does not grant or enforce Codex permissions. Preserve actual scope limits in the task contract. |
| `Read`, `Glob`, `Grep` | Describe the needed file read or search using available tools. Prefer `rg` for scoped searches. |
| `Write`, `Edit`, `Bash` | Use the available editing/shell tools with explicit paths and shell-appropriate syntax. Preserve overwrite and side-effect boundaries. |
| `AskUserQuestion` | Use ordinary terminal conversation. Ask only for missing facts or decisions; do not require a tool available only in a particular collaboration mode. |
| Slash commands / `$ARGUMENTS` / positional arguments | Translate to Codex skill invocation and named information in the user request. Define required inputs and defaults; do not retain unsupported substitution syntax. |
| Implicit `@file` loading or Claude environment variables | Replace with an explicit scoped read/path resolution. Do not assume automatic expansion. |
| Hardcoded `.claude/skills/...` | Make bundled references relative to the loaded skill directory. Keep project outputs relative to the resolved project root. |
| `Task`, `agent`, `context: fork`, `background` | Preserve the task, independence, and isolation requirements in skill-local worker contracts. Delegate through available Codex tools. Sequential execution is allowed only when independence is nonessential and behavior is preserved; essential unsupported isolation blocks conversion. |
| Nested `Skill` calls | Verify an available target dependency or emit the required handoff artifact. A required unavailable downstream execution is a blocker. |
| Dynamic shell injection | Never run it during inspection. Replace a necessary operation with an explicit authorized terminal step; remove automatic injection semantics. |
| `disable-model-invocation: true` | Preserve explicit-only intent in `agents/openai.yaml` using supported Codex policy; record any additional Claude behavior that is not reproduced. |
| `user-invocable: false` | No assumed equivalent. If hiding explicit invocation is essential, obtain a contract decision rather than inventing support. |
| Skill hooks and legacy CLI calls | Record required properties and incompatibilities outside executable instructions. Do not read/port excluded implementations or leave dead calls in the target. |

For a source that explicitly disallows implicit activation, the supported Codex metadata shape is:

```yaml
policy:
  allow_implicit_invocation: false
```

Keep normal implicit discovery otherwise. Preserve unrelated existing target metadata on revision. Do not generate UI fields, icons, or dependency declarations without a concrete need. Implicit discovery never supplies missing input or authorization.

Use the shared contract and worker guidance in [spec-build.md](spec-build.md) to record requirement source locations, artifact ownership, dependencies, and executable worker behavior. A worker contract is not a native profile or enforced permission boundary. Import retains full source accounting; provenance does not replace per-file dispositions.

## Remove ceremony without deleting requirements

| Source pattern | Conversion |
| --- | --- |
| Ask at least N questions | Ask for required missing information; reuse answers already supplied. Retain a question count only as descriptive data if the output contract uses it. |
| Read every file again to prove compliance | Read the resources needed for the current work; independently inspect resulting artifacts where relevant. A read event proves neither comprehension nor correctness. |
| EXECUTE/VERIFY/RECORD repeated around every sentence | Express the useful action once and define the artifact or evidence it produces. |
| Estimate context usage above a fixed percentage | Save material working state and provide an explicit resume path without claiming an unavailable measurement. |
| Hidden rubric or confidence score proves success | Retain substantive quality criteria; remove self-scoring as acceptance authority. |
| CLI missing: proceed as though gates passed | Remove the unsupported claim. Produce an agreed draft without acceptance or report the essential dependency as blocked. |
| Future commands in an installation/README template | Remove fictitious execution guidance or defer the template with rationale. Do not initialize or install a project merely because the source contains scaffolding. |
| Old checkpoint wins over current correction | Preserve original exchanges and append the correction; current explicit user instructions determine the working interpretation. |

Example: replace “Ask three questions and mark the phase PASS” with “Capture the analysis scope and success criteria; ask for either if missing.” This preserves the data requirement without a ritual count or false acceptance claim.

Example: preserve a business-analysis HTML data-island identifier and schema while using its existing draft status when agreed. Do not label the file accepted or schema-validated unless those operations actually occurred.

## Runtime boundary and manual assessment

Framework authority remains separate compiled-Rust design. Builder performs authoring custody only. Structural checks, grader profiles, generated-script execution and independent trials belong to the later skill-validator invocation. Do not generate evaluator campaigns as part of authoring. Preserve required runtime capabilities; unavailable essential enforcement remains a concrete gap, never advisory prose presented as enforcement.

## Capability evidence

Use the current host's available tools and read-only CLI help/version evidence. Record missing capabilities. A version number is not proof that a hook, agent profile, or permission policy is installed or qualified. Do not change configuration or use bypass flags to make a compatibility claim.

When a specific mapping remains uncertain, inspect local guidance first and consult the relevant primary source if needed. Record the fetched URL/section and date; do not substitute a search snippet for evidence:

- [Codex skills](https://learn.chatgpt.com/docs/build-skills): discovery and invocation metadata.
- [Agent Skills specification](https://agentskills.io/specification): portable package contract.
- [Claude skills](https://code.claude.com/docs/en/skills): source-host semantics.
- [Codex hooks](https://learn.chatgpt.com/docs/hooks): event behavior and limitations, for design only.

These references support targeted decisions; they are not mandatory full-document reads for every import.
