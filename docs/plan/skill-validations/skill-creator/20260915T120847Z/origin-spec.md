---
id: OBSERVED-SKILL-CREATOR-20260915T120847Z
skill_name: skill-creator
target: codex
status: observed
---
# Observed origin
Current package observed on 2026-09-15; historical origin unknown. Exact restoration uses source/ and source-manifest.json, complete with no exclusions. This is not a generated or adopted baseline.

## Purpose and triggers
Create/update Codex skills when the user asks for reusable skill authoring. Ordinary task execution, installation and independent audits are separate capabilities. Metadata in source/SKILL.md lines 1-6 governs discovery.

## Inputs and defaults
User task, intended name/location, existing package for updates, optional resources and interface fields. Entry instructions choose CODEX_HOME/skills or ~/.codex/skills absent a destination; preserve explicit destinations and current invocation policy. Hosts and current discovery paths may differ and require verification.

## Outputs and schemas
A folder containing UTF-8 SKILL.md with YAML name/description and Markdown instructions; only needed resources. Optional agents/openai.yaml contains interface strings, dependency records and boolean invocation policy. UI guidance is source/references/openai_yaml.md. Python helpers initialize files, generate UI metadata, and perform limited validation.

## Workflow and recovery
Understand the selected outcome and material unknowns; select resources; initialize only a new directory when helpful; author concise instructions; preserve unrelated existing bytes; validate and review observable results; deliver paths and limits. Existing directory initialization is rejected. Generator replaces openai.yaml, so policy/dependency-bearing updates must be edited in place. Retry and partial-work preservation are reviewed against actual helper behavior. Independent forward tests are conditional on complexity, authorization and availability.

## Resources, dependencies and environments
Three Python helpers (init_skill.py imports generate_openai_yaml.py; both and quick_validate.py use standard library and PyYAML). SKILL.md routes metadata changes to references/openai_yaml.md. agents/openai.yaml consumes two icons; license is intentional nonruntime material. Windows Python 3.10.11/PyYAML 6.0.2 available. Other platforms not qualified.

## Effects and boundaries
Write only user-selected skill destinations and disposable trial locations. No installation or external service mutation implied. The assessment retains original system package unchanged.

## Known uncertainty
Observed helper limitations are not approved future requirements. Current source is the baseline; no separate matching project specification was found in the bounded lookup. Native implicit selection and default user-location discovery require distinct runtime evidence.

## Cases and reconstruction
Cover new minimal skill, resource initialization, invalid inputs, existing destination, metadata generation/update, malformed frontmatter/placeholders, and independent create/update tasks. Reconstruct functionally using these inputs and cited source resources; restore exact bytes only from captured source/ and manifest.
