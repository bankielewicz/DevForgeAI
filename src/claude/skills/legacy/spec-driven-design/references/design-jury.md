# Inline Design Jury

Run this jury only for generated Web `story` and `standalone` modes after lint
and local desktop/mobile capture. It remains inline in the active provider
session. Do not dispatch subagents or create attestation rows. Jury output is
untrusted until `validate_design_review.py` exits 0.

## Roster and weights

| Role | Weight | Responsibility |
|---|---:|---|
| Designer | 0.0 | Draft, revise, and explain the chosen response |
| Critic | 0.4 | Hierarchy, type, contrast, rhythm, and space |
| Brand | 0.2 | Palette, typography, and spacing versus the brief/tokens |
| A11y | 0.2 | Contrast, focus, headings, alt text, and target sizes |
| Copy | 0.2 | Specificity, voice, action naming, and length |

The provider must inspect both captured images through its native local-image
surface before scoring. Every dimension score cites at least one concrete
artifact/source line or screenshot region (`desktop:x,y,w,h` or
`mobile:x,y,w,h`). General impressions are not evidence.

## Round protocol

1. Score every dimension from 0–10. The claimed panel score is the arithmetic
   mean of that panel's dimensions. Composite is Critic×0.4 + Brand×0.2 +
   A11y×0.2 + Copy×0.2; Designer never raises it.
2. A round passes only at composite ≥ 8.0 with zero open MUST_FIX items.
3. Every non-final round has at least one open MUST_FIX from every scoring
   panelist. Critic plus at least one of Brand/A11y/Copy must target different
   subsystems.
4. Revise the artifact, re-lint, and re-capture before rescoring changed bytes.
5. Run at most three rounds. Round n+1 critique-transcript bytes must be
   strictly less than round n, forcing convergence rather than repeated prose.

If no round passes, select the highest independently recomputed composite as
`ship_best`, set status `below_threshold`, and disclose every remaining open
MUST_FIX item. Never label `ship_best` as `gate_passed`. Ties select the earliest
highest round deterministically.
