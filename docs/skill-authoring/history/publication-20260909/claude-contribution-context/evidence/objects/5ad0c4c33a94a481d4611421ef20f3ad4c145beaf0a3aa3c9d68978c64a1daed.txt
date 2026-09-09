# Shared authoring rules (synthetic fixture excerpt, revision 2)

- Canonical sources are provider-specific. Work only in the provider and skill named by your
  assignment. A sibling provider's source is protected.
- Authored eval inputs live under the skill's evals directory; run outputs live in the assigned
  provider evaluation workspace.
- Check outcomes use exactly PASS, FAIL, NOT_RUN, COULD_NOT_RUN, NOT_APPLICABLE.
- No package or file-hash check certifies native activation or behavioral quality.
- The companion repository owns the CLI, policy, tests and workflows. Do not change a gate to
  make a candidate pass; report the defect to its owner.
