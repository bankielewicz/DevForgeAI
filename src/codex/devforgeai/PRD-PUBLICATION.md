# PRD port publication scope

Date: 2026-09-29. The owner authorized a draft PR containing the port, review reports
and selected supporting evidence, with raw execution output retained locally. This
follows the repository convention established in [PR #7](https://github.com/bankielewicz/DevForgeAI/pull/7).

## Included in the PR

- The Codex PRD skill, shared plugin metadata and package documentation.
- Evaluation case definitions, graders, fixtures, the mechanical generator and provider mapping.
- The SPEC-002 comparison report and separate, unapproved clarification proposals.
- The frozen 49-file runtime candidate and its manifest, source comparison evidence,
  complete evaluation plan, concise validation results and retained failure summaries.
- Repository ignore rules and the current publication checks and file manifest.

## Retained locally

The raw catalog/protocol files, logs, temporary authoring helpers, diagnostic control
files, generated Claude-to-Codex diff and superseded publication receipt remain in the
task worktree. The new ignore rules exclude these locations while retaining the catalog
result summary, candidate snapshots and failure summaries. They do not ignore all reports
or all evidence.

The complete original bundle is also preserved in local commit
`6d684411a8c81de0bea415ab2defdf55e3b62bb2`, referenced by
`codex/prd-port-local-evidence-20260929`. That backup ref is local only. The publication
branch's single unpublished commit was revised before pushing, so excluded files are
absent from its outgoing history as well as its final tree. No published history was rewritten.

## Evidence scope

The existing `delivery-manifest*.json`, `delivery-checks*.json` and preservation records
are historical import snapshots. They include files now retained only locally and the
original import-report bytes. They are not manifests of the filtered PR checkout.
The original report remains recoverable from the local backup; its publication revision
clarifies local-only evidence references and the later Git-delivery authorization.

Use [publication-manifest.json](prd-import-evidence/publication-manifest.json) for the
current PR file hashes and [publication-checks.json](prd-import-evidence/publication-checks.json)
for the filtering, ignore-rule and preservation checks. The publication manifest excludes
itself to avoid a self-referential hash. The checks cover the staged publication tree before
the check receipt and manifest are added; those two files receive a final whitespace and
manifest readback before commit.

The runtime candidate remains
`c46638c6881a99b3b29ac30e523bbe5e88f176ccb227292b19e2f40fd1947aef`.
No runtime instructions or evaluation case bytes changed during publication filtering.
The earlier 44/44 package regressions, structural validations and catalog-discovery result
remain scoped to that candidate. Native PRD behavior remains **NOT_RUN**: all 120 automated
trials, manual and supplemental obligations remain unqualified. This PR is a draft source
port; publication does not establish installation, deployment or owner acceptance.
