# Brainstorm evaluation definitions

These eight cases and their graders were imported from the Claude plugin. Prompt bodies,
VER tags, file assertions, and rubric intent are retained. Claude tool allowlists are
removed, provenance assertions use Codex, and Skill-tool graders become explicit trace
reviews. Regex, file-existence, and LLM frontmatter describe checks; this package does not
provide a native Codex runner for that format. Do not run `claude plugin eval` to qualify
the Codex port or equate these files with completed evaluations.

The complete denominator is SPEC-001 VER-01 through VER-10: eight automated-in-source
cases plus two manual obligations. `verification-plan.json` freezes that denominator and
initial NOT_RUN states. No native behavior or trigger rate has been measured for this port.

For a future native evaluation, use a fresh disposable project with the candidate enabled
and no parent project instructions. Repeat each of the eight case prompts three times and
compare with a no-plugin baseline. Retain the full prompt, loaded candidate identity, raw
trace, files, grader decisions, and failures. The inherited bar is 0.8 per case over three
runs; a score does not waive an unrun obligation or missing confirmation evidence.

For `existing-brn`, run its inspected `scaffold.sh` only in the disposable project before
the prompt. It intentionally seeds a historical Claude-authored document. Hash it before
and after the unanswered extend/new question; do not infer preservation from the marker
regex alone. Human-rubric and skill-load checks need explicit evidence, not invented results.

For VER-03, compare model and session values to the host's recorded identity and the last
Change Log row. `unknown` is incomplete provenance, even if a shape-only regex matches it.
For VER-10, the supplied case covers the actually available, PRD-absent branch of BEH-10.
The specification's PRD-present expectation remains a discrepancy, not a passed case.

Manual VER-05: in a copy of the plugin, add a framework with all six required sections and
an index row, confirm selection with SKILL.md unchanged, then remove the added file and
confirm fallback plus disclosure. Never mutate the source candidate for this exercise.

Manual VER-09: check the <500-line skill and frontmatter separately from runtime behavior.
Exercise stopping with save=yes and save=no, and an intentionally unfixable validator in
the disposable copy: after three attempts the BRN must be draft with remaining errors
reported. Also exercise user-confirmed dispositions/convergence and extension preserving
old IDs, meanings, authors, and Change Log rows. Static checks do not complete this obligation.
