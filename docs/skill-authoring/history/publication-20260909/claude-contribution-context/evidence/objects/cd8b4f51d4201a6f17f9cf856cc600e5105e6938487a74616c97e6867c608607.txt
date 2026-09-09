# FIND-912 — open finding scoped to SESSION-912 (synthetic fixture)

- Against: the in-progress Claude candidate under SESSION-912@2
- State: OPEN
- Observation: the package's runtime resource list still includes an authoring-only directory,
  so a runtime export would carry files it should omit. Recorded outcome of the affected
  inventory check: FAIL.
- Owner to resolve: SESSION-912 (this worker), within its existing authoring delegation.
