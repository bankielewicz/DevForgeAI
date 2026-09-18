# Attributions and modified-material notice

DES-B adapts narrow design guidance and deterministic checks; it does not copy
third-party source wholesale. All adapted prose and Python behavior have been
modified for DevForgeAI's provider-neutral contracts, local-only renderer, and
shared CLI workflow gates.

## Open Design

- Source: `https://github.com/nexu-io/open-design`
- Exact commit: `10adca2cbf47be61829c74e21158ecccddf4c1cd`
- License: Apache-2.0; complete text in `assets/licenses/Apache-2.0.txt`
- Adapted surfaces: `craft/anti-ai-slop.md` (SHA-256
  `a20e6592af4649db2ab1a4e27012ae1e17949d374432293b2fcb8af20ff270ce`),
  `craft/color.md` (`896a24f3e3d3c1548e89c0102b0f46c275b2c27ef26e28a65f9170468ef613bf`),
  `craft/laws-of-ux.md` (`9a4db0fe294a240920921111d43a6af5ea0c4df1bf979f6e780610a36a9c6d1c`),
  and `apps/daemon/src/lint-artifact.ts`.
- Modification: guidance was distilled and reconciled with pinned-brief
  authority; TypeScript lint behavior was reimplemented in stdlib Python with
  an upstream-finding coverage manifest and DevForgeAI advisories.

## Anthropic frontend-design

- Source: `https://github.com/anthropics/claude-plugins-official`
- Exact commit: `e14e8fe2c1fca5912d7389ba7e3a44149d36b5c8`
- Verified installed `SKILL.md` SHA-256:
  `1608ea77fbb6fc30d13a97d12cfa8ebf31358d40f0dd97beed24829d6b3f45dd`
- License: Apache-2.0; upstream `LICENSE.txt` SHA-256
  `0d542e0c8804e39aa7f37eb00da5a762149dc682d7829451287e11b938e94594`;
  complete license text in `assets/licenses/Apache-2.0.txt`.
- Adapted surface: subject grounding, hero thesis, two-pass token/type/layout
  plan, signature element, single bold move, and responsive/accessibility floor.
- Modification: provider-specific instructions were rewritten as a concise,
  provider-neutral Web craft contract.

## Refero skill

- Source: `https://github.com/referodesign/refero_skill`
- Exact commit: `f78b4eccf112d7a179b92afeafdd7e8684560ac2`
- License: MIT; authoritative `LICENSE` SHA-256
  `7b5d57a0e210289fa900a0e2ab0513442e439e9d20b96f0cf5cba0e1b31b665e`;
  complete text in `assets/licenses/MIT-refero-skill.txt`.
- Adapted surface: upstream material reached DES-B through Open Design's
  explicitly attributed color, typography, and anti-slop craft references.
- Modification: rules were narrowed to the Web contract and reconciled with
  user-pinned tokens and directions.
