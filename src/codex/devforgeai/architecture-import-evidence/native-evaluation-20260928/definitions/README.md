# Architecture evaluations

These 14 generated cases cover SPEC-003 VER-01 through VER-11 and VER-14 through
VER-16. Regenerate them from the repository root with:

```bash
python3 -B src/codex/devforgeai/tests/make_architecture_evals.py
```

Edit the Codex generator and regenerate the suite; do not edit generated case files
directly. The inline fixtures are validated against the repository schemas before
generation. Their historical `claude-code` authorship is intentionally preserved
byte for byte. Only records authored during a Codex trial are expected to identify
`codex` as the tool.

## Native evaluation contract

Each automated case requires three plugin runs and three no-plugin baseline runs,
for 84 native trials. Every case must score at least 0.8 in each plugin run. Missing,
failed, or incomplete trials remain in the denominator. VER-12 is manual and VER-13
is an operator custody check; neither may be inferred from the automated matrix.

Claude's `tool_used: Skill` checks are represented by `skill_loaded` graders bound
to `skills/architecture/SKILL.md`. VER-07 additionally requires a native
`request_user_input` event before choosing whether to reuse or amend ARCH-001.
The negative trigger checks that the Architecture skill is not loaded in either arm.

The Codex 0.158 host exposes `request_user_input` to this workflow in Plan mode, so
the native VER-07 gate runs both arms in Plan mode and records that mode with the
trace. The gate ends at the question and must not write files. The preserved
semantic rubric still accepts a clear plain-text choice request when the rubric is
used outside this native-tool gate; that fallback does not satisfy the Codex-native
`request_user_input` grader.

Two semantic rubrics remain explicit review obligations:

- `existing-arch-not-duplicated/recommends-and-asks.md` checks the recommendation
  and choice request.
- `superseded-adr/readiness-mapping.md` checks the complete, non-contradictory
  requirement-to-decision mapping.

Regex or file-presence checks cannot replace those reviews. The suite has no grader
that claims a runtime Architecture validator ran: generation validates fixture
documents only, while artifact conformance must be established from the saved files.
`strict_pass` therefore means the defined source checks and supplemental guards all
passed; it is not a claim that a complete ARCH or ADR schema validator ran.

## Provider adaptations

Prompt metadata exposes `exec_command`, `apply_patch`, and `request_user_input`.
Activation uses observed Codex skill loads. Newly written provenance expects `codex`;
pre-existing fixture provenance and review history continue to expect `claude-code`.
The VER-10 handoff uses Codex's namespaced `$devforgeai:epic PRD-001` command.
Prompts, scaffolds, fixtures, regexes, and semantic rubric text otherwise preserve
the Claude suite's behavior and grading intent.
