# Template: Research finding

**Producer:** planned `research` (legacy `/research`)  
**Consumers:** `discover`, `specify`, `architect`, `story-create` as selected context  
**Does not:** select a product objective, change policy, or authorize implementation.

## Envelope

| Field | Value |
| --- | --- |
| Finding ID | RF-[topic]-[utc] |
| Producer | research |
| Downstream consumer | [discover / specify / architect / story-create] |
| Failure behavior | Optional absence: consumer reports unused research, does not block |
| Non-claims | Not a requirement; not a vendor endorsement unless user selected it |

## Upstream inputs

| Role | Locator | SHA-256 / URL+date | Notes |
| --- | --- | --- | --- |
| Selected question | | | |
| Sources inspected | | | include retrieval date |

## Question

[Exact question the finding answers.]

## Observations

| Claim | Source locator | Date | Confidence | Counter-evidence |
| --- | --- | --- | --- | --- |
| | | | observed / second-hand / unknown | |

Separate fact, vendor claim, and inference. Missing sources are gaps, not empty tables presented as exhaustive market proof.

## Implications for this project

- Relevant constraints: [compatibility, license, ops, skill]
- Options considered: [with rejected reasons]
- Recommended next document: [which template should consume this]
- What this finding must not be used for: [e.g. lowering a quality floor]

## Downstream handoff

Consumer may cite this finding as **context**. Promoting a recommendation into a requirement requires an explicit specify/user selection.
