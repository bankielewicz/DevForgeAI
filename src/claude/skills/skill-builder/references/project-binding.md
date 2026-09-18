# Portable runtime binding

Builder authors a generic prerequisite, never real setup. Copy [the standard-library template](../assets/adaptive-runtime/check_project_binding.py) to `scripts/check_project_binding.py` in each newly authored adaptive package. No concrete project identity or author-machine root enters generated source. Ordinary authoring and these two maintenance tools need no binding.

Generated SKILL.md must instruct the executing host to resolve the currently selected project and actually loaded skill root and run, before product-specific actions and on resume or detected binding/package changes:

```text
python -B -X utf8 <loaded-package>/scripts/check_project_binding.py --project-root <selected-project> --skill-root <loaded-package>
```

Use an argument vector or native shell quoting; paths with spaces, Unicode, apostrophes, dollar signs, ampersands, semicolons and parentheses stay data. Do not interpolate a shell command from project text. Discover the Python executable; absent Python means an unavailable prerequisite with no product effects, not an assumed match. No dependencies are installed, and the helper needs no network.

Proceed with the declared product contract only for exit 0 / MATCH / BOUND. For any other result, report the reason, request separately authorized setup/rebinding, and perform no product writes or downstream workflow calls. Read-only explanation remains allowed. The result is an observation, never a cached approval token; a previous match does not survive changed bytes. The agent still honors current user scope and host permissions.

## Operational record owned by separate setup

The schema is [project-binding-v1](../schemas/project-binding-v1.schema.json). Only `<project>/.claude/devforgeai/project-binding.json` carries actual framework identity. Separate setup explicitly selects project, creates canonical lowercase UUID for a new identity, inspects complete installed bytes, selects active roles, writes and reads back the record. Root is resolved local absolute path; revision starts at 1 and increments on changes, preserving identity for the same project. Relocation requires explicit root update/recheck; a different product needs a new identity. No first-use initialization, installation or real binding mutation belongs to builder. Validator can create synthetic records only inside disposable projects.

Each installed path is a project-relative directory whose final component is the member name; the project owner chooses the parent, so no fixed skills-directory layout is required. Paths and names are unique, with digest, matching role and selected boolean. At most one selected implementation per core responsibility: a core uses its own name; a variant uses parent_core.name. Two variants of the same parent also conflict. The parent need not be installed. Selected related core/variant descriptors must be valid; expertise overlap is semantic assessment, not inferred by the helper.

Root comparison uses absolute resolution and native case normalization with no Windows/WSL substitution. Matching UUID never overrides a different root/package. These editable records detect ordinary relocation/staleness, not malicious editing of all fields; no Rust gate or protected acceptance is claimed.

## Observations

The helper inventories exact loaded bytes and related descriptors without links/junctions/special files or excluded/generated files, using a shared 2,000-file / 32-MiB ceiling. It prints one [binding-observation-v1](../schemas/binding-observation-v1.schema.json) JSON object containing only status, reason, nullable binding/package digests and sanitized details. No UUID, binding content, exception path or secret is printed. It creates no files/cache/bytecode.

Before content reads, shared capture excludes private-key basenames `id_rsa`, `id_dsa`, `id_ecdsa`, `id_ed25519`, `id_ecdsa_sk`, `id_ed25519_sk` and suffixes `.pem`, `.key`, `.pfx`, `.p12`, `.ppk`, case-insensitively. Exact package capture rejects these paths with UNSAFE_PATH instead of omitting them from a complete digest. Public `.pub`, `.crt`, and `.cer` files are permitted unless another exclusion applies. Environment-file prefixes such as `.env`, `.ENV`, and `.Env.local` are also excluded case-insensitively before reads. This filename policy does not claim comprehensive secret detection.

| Exit / status | Reasons |
| --- | --- |
| 0 / MATCH | BOUND |
| 1 / MISMATCH | MISSING_BINDING, INVALID_BINDING, ROOT_MISMATCH, UNBOUND_SKILL, PACKAGE_CHANGED, ROLE_MISMATCH, NOT_SELECTED, AMBIGUOUS_ROLE, UNSAFE_PATH |
| 2 / UNAVAILABLE | CAPTURE_LIMIT, IO_ERROR |

Malformed/unknown descriptor or record is INVALID_BINDING; absent binding is MISSING_BINDING. CLI usage errors exit 2 with stderr, without a claimed JSON observation. Invalid/changed bytes never become a full binding via exclusions. Builder copies the template without running it during normal authoring. Synthetic helper execution belongs to validator or an explicitly authorized maintenance task.
