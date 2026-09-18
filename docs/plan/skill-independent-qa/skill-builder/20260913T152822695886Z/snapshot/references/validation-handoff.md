# Manual validation handoff

After authoring readback, publish validation-request.json with schema_version validation-request-v1 and record_kind validation_request. Include authoring_run_id, project_root, actual target_root/name, target_manifest reference, package_digest, authoring_record reference, applicable specification_refs, changed_paths, known_issues, capabilities, expected_outputs and declared side_effects. All file references bind actual bytes with SHA-256. Also return validator-request.md with an explicit invocation, packet path and digest.

The packet proposes assessment. It cannot authorize network, credentials, installation or external writes. Stop after returning it, even when validator is available. If unavailable, authoring may still complete; validation/testing remain NOT_PERFORMED and the same packet can be used later.

A later user invocation selects skill-validator. Validator independently rereads the target, rejects stale package/request/authoring bindings and creates its own rules, cases, fixtures, expected outcomes, execution records and results. Builder never imports a result automatically or starts a repair loop. A later authorized edit can use a selected validator report as a digest-bound input. Preserve its old result as history; edits invalidate any claim that it tests the new bytes.
