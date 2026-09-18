# Independent validator handoff

Use $skill-validator to independently validate the development skill-builder at
`C:\Projects\DevForgeAI\src\agents\skills\skill-builder` against the original selected specifications in
`C:\Projects\DevForgeAI\docs\plan\skill-builder-postmvp-maintenance\20260914T2108252255451Z\requirement-refs.json` (SHA-256 `85de94117e636b5c81174272ec17b55019bb3e7b8b193474158d083108d35158`).

Expected current package digest: `ecb01ece2c38443e58fe7a5b307e9d0de22a1fa9b9ec1f726b79cfa328cb9c9e`.
Bind and reread `C:\Projects\DevForgeAI\docs\plan\skill-builder-postmvp-maintenance\20260914T2108252255451Z\delivered-manifest.json`
(SHA-256 `3b1849497c6fd2e1bc451975a18e63876ebda474a854f963a4faad3d86bb18a3`) and reject stale source.
The digest includes package-manifest.json; that file's artifacts map excludes itself.

This standalone maintenance handoff does not fabricate a builder authoring-record
or change validation-request-v1. The enhanced builder's actual packet was exercised
through unchanged validator intake in maintenance fixtures.

Independently derive fixtures and oracles from original requirements. Builder design
artifacts and adverse-condition descriptions are authored expectations, not executed
results or waivers. Maintenance helper results do not qualify a cold workflow.

Assess all SBPV-01 through SBPV-18 from the post-MVP specification, retaining applicable
legacy/adaptive regressions. For SBPV-18 cold-invoke the enhanced builder, then separately
exercise two actual generated skills: a simple transformation and a branching workflow
with file delivery and a relevant failure path. Use different layouts and literal paths
with spaces/Unicode. Verify outputs, failed delivery, interruption/recovery, unchanged
source reporting, native obligations and independent oracle construction.

Prepare the mandatory external Python JSONL runner, deterministic graders, fixtures,
expected results, schema, runtime/dependencies and artifact byte bindings. The present
maintenance bundle is supporting evidence, not a replacement for your independent bundle.
Predeclare commands, permitted effects, output paths, case budgets and retry policy.
Preserve all attempts. No silent timeout increase or automatic repair cycle.

Unresolved implementation decisions: none identified. Unperformed qualification:
all cold builder/generator and generated-skill SBPV behavioral scenarios, Linux coverage,
full-package coverage outside the declared custody scope, and framework acceptance.
Maintenance: 154/154 Windows cases pass;
line coverage 596/615 = 96.910569%
for authoring.py and record_schema.py only, no excluded lines. Branch coverage is separate.

Validation: NOT_PERFORMED. Generated-skill Testing: NOT_PERFORMED.
An unchanged or AUTHORED skill is not an evaluated build. Preserve operational copies,
validator source, original specs, existing generated skills and historical evidence.
This file grants no evaluation, installation, network, external-effect or repair permission;
the later user invocation determines assessment authorization. Next owner: skill-validator;
next action: bind current source and propose the independent assessment under that invocation.
