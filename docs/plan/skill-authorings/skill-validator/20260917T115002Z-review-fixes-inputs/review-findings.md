# Reviewer findings on authoring run 20260917T112416Z-claude-conversion

An independent reviewer read the published conversion. Four items were raised; two
were verified as real defects in the delivered bytes, two were checked and did not hold.

## F1 (confirmed, blocking) — the portability divergence reduces every sibling to INCOMPLETE

`scripts/text_resources.py` emitted the YAML-list `allowed-tools` divergence as
`check('AV-F04','SKILL.md','NOT_RUN', ..., 'unknown')`. That factory defaults
`required=True`, and `observe.reduce_checks` puts any required row with
`applicability == 'unknown'` or `result == 'NOT_RUN'` into `incomplete`, which reduces
to INCOMPLETE. `scripts/adaptive_observe.py` `reduction()` calls exactly that function
over the AV rows and additionally counts `unknown_applicability`.

Effect: `advisor`, `dev`, `skill-builder` and the converted `skill-validator` itself all
declare `allowed-tools` as a YAML list, so all four would reduce to INCOMPLETE. This is
the same defect the conversion set out to remove, moved from "required FAIL" to
"required NOT_RUN -> INCOMPLETE". A validator that can never report PASS on this
repository's own skills is still wrong.

The shipped test asserted the row's `result` only and never the reduction, so it passed
while the reduction was broken.

Fix: keep one required AV-F04 row carrying the actual outcome, and emit each divergence
as a separate non-required row with a distinct discriminator so multiple divergences do
not collide on `check_id`. Keep `applicability` at `applicable`: `adaptive_observe.py`
requires `(applicability == 'not_applicable') == (result == 'NOT_APPLICABLE')`, so a
`not_applicable` row must carry `NOT_APPLICABLE`, not `NOT_RUN`. Keep the
unknown-*extension* row required, because an unrecognized field genuinely needs
adjudication.

## F2 (confirmed) — one malformed optional field produces two required FAIL rows

AV-F01 calls `frontmatter()` and FAILs on exception. The new AV-F04 block called it a
second time and FAILed on the same exception, so a single bad field yielded two required
FAIL rows against the same bytes. `references/adaptive-validation.md` requires each check
to be counted once.

Fix: parse the entrypoint once. When the entrypoint metadata does not resolve, AV-F04 is
`not_applicable` / `NOT_APPLICABLE` with a reason naming AV-F01 as the carrier of the
failure, rather than a second FAIL.

## F3 (checked, does not hold) — `init_skill.py` scaffolding

The reviewer asked whether `skill-builder/scripts/init_skill.py` still scaffolds
`agents/openai.yaml`, which would falsify the rewritten assertion in
`tests/test_authoring.py`. It does not: the script contains no `agents/` scaffolding at
all. The assertion stands and is a useful regression guard.

## F4 (checked, does not hold) — references to deleted check identifiers

The conversion deleted the `configuration_yaml`, `configuration_policy` and
`invocation_policy_type` check identifiers from `scripts/observe.py`. A grep of `evals/`
and `tests/` finds no reference to any of them. `evals/runtime.json` pins Python version
and capture limits only, no package digest, so it is not stale.
