# FIND-901 — open finding (synthetic fixture)

- Raised by: SESSION-902@3 during its own authoring checks
- Against candidate: XPKG-902@1 (Claude provider)
- State: OPEN, unresolved. No owner has been assigned to resolve it.
- Observation: the candidate's checkpoint resource references a template path that resolves in
  the author's checkout but was not copied into the package, so an installed copy would not
  resolve it. Recorded outcome of the affected structural check: FAIL.
- Note from its author: "I could not verify installed behavior; installation is not allocated to
  this session." Affected observation: COULD_NOT_RUN.
