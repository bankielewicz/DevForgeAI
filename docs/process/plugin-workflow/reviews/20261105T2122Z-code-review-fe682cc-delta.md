commit: the records fixes after fe682cc, reviewed uncommitted (PR #152; last plugin commit 1a14f85)

# Review of the records delta after fe682cc (`/code-review medium`)

Bryan, 2026-11-05: "Review just the delta (Recommended)": the fixes for the close review at fe682cc
(`20261105T2102Z-code-review-fe682cc.md`) are reviewed on their own, and fe682cc's full review with this one stands
as the close review on the final commit. The delta: SPEC-017 §9's Build and Version 3 rows, CHANGELOG.md's ui entry
moved under the existing "### Changed", the invocation times in the two plugin-validator reports, and the fe682cc
report. Run 2026-11-05 21:20 UTC by a forked `code-review` agent; it read the stack's whole diff against `main`, so
it also commented on #149's and #150's files.

On the delta, both challenged:
1. `SPEC-017.md:830`: the test counts should name the tree they were measured on. Challenged: the row says "On
   1a14f85", and the commits after it change only records and one test docstring.
2. `CHANGELOG.md:57`: the ui entry sits under "### Changed" below "### Added", and the file has no 0.32.0 heading.
   Challenged: it is the one "### Changed" under Unreleased (the fix the fe682cc review asked for); the file keeps
   every change under Unreleased, with no version headings; the "### Fixed" above "### Added" is #150's.

Outside this commit (#149's and #150's changes in the stack), noted for Bryan, not changed here:
3. `src/tests/context/test_context_check.py:656`: `WithoutUserSite` now pins no jsonschema behaviour; the pinned
   classes cover it and skip when `tmp/test-envs` is missing (#149's design; EVAL.md G2 forbids that skip).
4. `src/tests/prd/test_validate_policy.py:660`: `_pinned_python` runs git at import and is duplicated in
   `test_context_check.py` and `make_jsonschema_envs.sh` (#149).
5. `src/tests/process/make_jsonschema_envs.sh:9`: a half-built venv counts as built (#149).
6. `src/tests/process/test_skill_placeholders.py:26`: `$` and a digit, such as `$5`, counts as a placeholder (#150).
7. `skills/ui/SKILL.md:40`: the Inputs bullet relies on Claude Code appending an `ARGUMENTS:` line (#150).
8. `src/tests/progress/test_adapter_structure.py:97`: the comment names 0.31.2 as #135's patch; the reviewer says no
   manifest carried it. Challenged: #150 sets 0.31.2, and #152 moves it to 0.32.0.
