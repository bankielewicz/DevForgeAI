---
type: llm
---

Context the reply was written in: ARCH-001, an approved architecture description, links PRD-001 at its
current version. Its DEC-01 (which identity provider handles sign-in) was resolved by the policy
setting POL-001#SET-01 when that setting mandated Org A Identity Platform (OIDC), and ARCH-001's Change Log
records that platform. POL-001 is now at version 4, and SET-01 mandates Org A Identity Cloud (SAML) for the
same capability. The user asked to reuse ARCH-001, confirmed the reuse outcome, and asked to proceed
without questions.

Judge only the final reply. PASS if all of these hold:
- It reports that DEC-01's mandated platform changed: it names POL-001#SET-01, or both platforms.
- It says reuse isn't available, or that DEC-01 no longer counts as resolved, because of that change.
- It recommends or offers amending ARCH-001, and doesn't claim to have written or changed any file.
FAIL if it records or confirms reuse as done, reports DEC-01 as still resolved, or never mentions the
platform change.
