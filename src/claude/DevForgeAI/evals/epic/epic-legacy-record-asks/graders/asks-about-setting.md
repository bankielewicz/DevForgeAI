---
type: llm
---

The workspace held POL-001 at version 2 with SET-01 (the mandated mail relay for transactional email)
unchanged, and an ARCH-001 whose policy resolution line records POL-001#SET-01 only in an older form,
with no platform or capability. DEC-07 (which email service sends booking confirmations) is resolved by
POL-001#SET-01 and cites FR-012. The user asked for one epic covering everything eligible and did not
say to proceed without questions, so a user is present to answer, and the skill must ask before writing
anything: did POL-001#SET-01 mandate the "Regional network mail relay (SMTP)" for transactional email
when DEC-07 was resolved?

Judge only the final reply.
PASS if the reply asks the user that question, in any wording (whether the setting already mandated the
regional network mail relay, or that platform, when DEC-07 was resolved), and doesn't present an epic as
written.
FAIL if it presents an epic as written, decides the answer itself, or never asks about POL-001#SET-01's
platform.
