# Instruction and resource review

Scope: exact captured system skill, all 9 files; no repair. Primary assessor wrote this review independently of the cold task agents. Helper behavior and cold outcomes are reported separately.

## Format and scope
SKILL.md has a unique-key YAML mapping, name skill-creator matching the original directory, a nonempty scoped description, and preserved string metadata. The source/ snapshot directory is an evidence convention, not a naming failure. All captured declared text decodes as UTF-8. Binary PNG is an icon consumed by optional metadata.

The description identifies skill creation and updates. It does not offer installation or general skill auditing; those uses must not be inferred solely from the name. Native implicit discovery is not established by explicitly reading this skill.

## Concrete contradiction: UI description constraint
source/references/openai_yaml.md says interface.short_description is 25–64 characters. source/agents/openai.yaml contains "Create or update a skill" (24 characters, independently measured).
This is a contradiction with the package's own UI guidance and generator constraint. It is not a universal YAML-format failure and no UI rendering failure was observed. A focused change should align the bundled metadata with its own documented constraint, preserving icon paths and automatic invocation.

## Naming limit discrepancy
SKILL.md says "under 64 characters", while init_skill.py and quick_validate.py permit 64.
This is a minor boundary-wording inconsistency. The helper's 64-character limit is not evidence that 63 is the universal standard. A proposal should choose explicit inclusive wording consistent with the selected standard rather than silently tightening accepted names.

## Progressive disclosure and references
One real Markdown link routes interface work to references/openai_yaml.md before edits. Fenced examples of PDF/cloud/document skill trees describe examples, not dependencies; their files must not be demanded in this package.
The entrypoint directly identifies all three scripts. init_skill.py imports write_openai_yaml from its sibling generator. The scripts are reachable through commands even though the Markdown-only graph cannot establish those edges.
agents/openai.yaml references the supplied SVG and PNG. license.txt is intentional legal material, not an orphan. The SVG has no scripted or external-resource behavior in the inspected bytes. No production resource is unexplained.

SKILL.md is 15,540 bytes, 229 lines. Supporting UI guidance is 2,405 bytes, 49 lines. No arbitrary size failure is assigned. UI details are conditional; ordinary narrow edits do not need every helper or asset loaded. Token counts and actual model context consumption were not measured.

## Scope and approval instructions
"Preserve user intent and scope" names concrete boundaries: keep chosen product, avoid unrelated configuration, do not infer permission for external actions. Creation should preserve the explicit location and keep normal invocation unless changed by the user. Existing invocation policy is preserved on update.
"The generator replaces the entire file" is an accurate, important routing warning; its policy/dependencies branch directs in-place edits. Regenerating such a file would violate the workflow even though the bare generator is documented as a replacing writer.
The wording about authorization immediately before a mutation should be read with existing user authorization and host controls. It is not a requirement to ask again for a currently authorized edit. Cold creation/update trials test actual behavior under this context.

## Placeholder and ceremony adjudication
The TODO markers in init_skill.py are intentional scaffold templates and guidance to replace them, not unfinished installed skill instructions. Their safe handling must be tested against produced skills. The quick validator's own placeholder-detection code is literal implementation data.
Emphatic core principles are useful instructions because they alter routing, resource creation, optional invocation policy and scope decisions. No "repeat until perfect", model-issued acceptance gate, or unsupported claim of enforced isolation appears.
Repeated normal-invocation guidance appears at the UI section and at workflow selection; it preserves timing/context and is not a demonstrated defect.
The reference's full example includes default_prompt, but the entrypoint says optional interface fields are included only when requested; a full example is not a mandate to generate every field.

## Workflow and recovery
Creation: user outcome/location -> choose resources -> optional initialization -> replace scaffolds -> validate -> task-specific output review -> deliver usable skill.
Update: inspect current files -> select requested changes -> preserve other fields/files -> use in-place metadata edit when policy/dependencies exist -> validate changed result -> deliver paths and limitations.
Failure: inspect errors and retained partial output; do not reinitialize an existing skill. Helper trials separately test invalid arguments and existing targets.
Independent testing: isolated disposable task scope, minimal raw inputs, no intended answer, review output. Shared subagent filesystem is not OS-enforced isolation.
No framework, installation, publication, production messaging or runtime acceptance action is part of the package contract.

## Source-to-effect review
Python helpers use argparse/pathlib and local text/YAML operations; no shell command construction, network clients, credential reads, subprocess launch or live-service mutation is implemented by the helpers. yaml.safe_load avoids arbitrary Python-object construction. Inputs can still cause malformed output or parsing errors; tests determine those narrower behavior defects.
Initializer normalizes names and appends to the caller-selected parent. It refuses existing directories. Generator replaces only the caller-selected agents/openai.yaml. Direct untrusted calls with arbitrary filesystem paths are not sandboxed by these utilities; caller authorization and host permissions remain necessary. This assessment does not certify race resistance or hostile filesystem isolation.

## Documentation freshness
Official Build skills documentation was opened through its former developers.openai.com URL and redirected to https://learn.chatgpt.com/docs/build-skills. Its description-based routing, progressive disclosure, optional metadata and implicit invocation default agree with the corresponding inspected instructions.
Its current user-location table lists ~/.agents/skills while the installed package instructs CODEX_HOME/skills or ~/.codex/skills. This host demonstrably loads the selected system skill under ~/.codex/skills/.system. Default-location discovery for newly authored skills was not exercised; retain the discrepancy as a portability question, not a proven local failure.
