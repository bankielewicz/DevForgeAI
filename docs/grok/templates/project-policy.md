# Template: Project policy

**Producer:** `architect` with user selection; consumed by every product skill  
**Consumers:** `dev`, `qa`, `release`, expertise packages  
**Does not:** export DevForgeAI's Rust/95% rules into an unrelated product; grant protected authority; let an expert lower a floor.

## Envelope

| Field | Value |
| --- | --- |
| Policy ID / revision | POL-[project]-r[n] |
| Producer | architect + recorded user selection |
| Downstream consumer | dev, qa, release |
| Failure behavior | Missing required measure blocks dependent claims; independent investigation may continue |
| Non-claims | Not an acceptance receipt; not a binding UUID |

## Upstream inputs

| Role | Locator | SHA-256 | Notes |
| --- | --- | --- | --- |
| Repository instructions | | | if present |
| User-selected profile | | | or none |
| Architecture | | | |
| Test / build manifests | | | observed tools, not assumed |

## Effective policy

| Category | Effective value | Source | Inapplicable reason |
| --- | --- | --- | --- |
| Languages and versions | | | |
| Package / build tools | | | |
| Source layout conventions | | | |
| Required test types | | | |
| Coverage metric and floor | definition, denominator, exclusions | | |
| Required-case pass-rate floor | unit vs other categories separately | | |
| Allowed test doubles | | | |
| Required platforms | | | |
| Effect boundaries | install / deploy / data | | |
| Exception authority | who may amend this revision | | |

Defaults cannot conceal a missing required policy. A subsequent change is a **new revision** identifying affected work/evidence.

## Platform matrix

| Platform | Required for | Qualification owner | Unavailable handling |
| --- | --- | --- | --- |
| | | | NOT_RUN; no cross-platform substitution |

## Downstream handoff

**To dev:** derive commands and thresholds from this document, not from skill constants.

**To qa:** independent floors and integrity rules for the selected project. If this policy conflicts with the current `qa` skill contract, record the conflict; do not silently weaken either.

**Return path:** an expert suggesting a lower floor is a proposal only. It does not change this revision.
