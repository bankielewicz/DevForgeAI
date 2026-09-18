# Records and report semantics

### SV-009: storage and machine records

Use UTF-8 Markdown/JSON/JSONL. JSON parsing rejects duplicate keys and non-finite values. Machine paths inside a run are normalized forward-slash relative paths; original resolved absolute paths are separately informational. SHA-256 values are lowercase raw-byte digests. Hash actual bytes, not model-written strings. Byte intervals are zero-based and end-exclusive; line locators are one-based and refer to the identified snapshot.

Work products, created when their inputs exist:

| Path within run | Contract |
| --- | --- |
| `source/`, `source-manifest.json`, `source-after-manifest.json` | Snapshot plus sorted permitted file rows `{path, bytes, sha256}` and explicit excluded boundaries. Capture original resolved root and actual capture time. |
| `origin-spec.md` | Reconstructed origin only when none exists. Existing specifications are captured under `inputs/` and referenced instead. |
| `origin-record.json` | Schema 1: run/target identity, original source root, manifest reference, specification reference or null, `origin_kind: existing_spec|reconstructed|unresolved`, `history_kind: observed|adopted|generated`, prior evidence reference or null, completeness, uncertainties, and source readback state. An adopted/generated history kind requires verified corresponding evidence. |
| `sources.json`, `rule-set.json` | Schema 1: observed source IDs, URLs/original paths, retrieval times, content hashes, snapshot paths, sections, freshness; selected rule records from section 7 and their source bindings. |
| `workflow-map.json` | Schema 1: run/target identity and step rows defined in section 5. |
| `checks.jsonl`, `findings.json` | Per-check coverage and finding records below; findings JSON has schema 1, run/target identity, and a `findings` array. |
| `trials/`, `command-log.md` | Planned and observed trial evidence, all real execution attempts, and relevant file/tool operations. |
| `validation-report.md` | Identity, outcome, freshness, source preservation, five assessment dimensions, findings, tests/limitations, proposed changes, and next action. |
| `revision-spec.md` | Complete proposed future behavior and builder instructions when fixes/enhancements are justified; never overwrite origin. |
| `enforcement-recommendations.md` | Register from section 7, or an explicit no-candidates finding. |
| `handoff.json` | Review and execution readiness, references, proposed changes, preservation boundaries, adoption requirements, and unresolved decisions. |

A reference object is `{path, sha256}`; all referenced files must already exist before recording their digest. Source locators additionally carry `source_id` and a section/line/byte locator. Do not create self-referential manifests or cite a future report as input evidence. Source manifest digests cover source files, not the run directory. Define `package_digest` as SHA-256 of the UTF-8 JSON array of permitted file rows sorted by path, with each row ordered `path`, `bytes`, `sha256`, compact separators and unescaped Unicode. Exclude timestamps and root locations from that digest; retain excluded boundaries separately. Package identity is not a completeness claim when exclusions exist.

Each check row has `schema_version: "1"`, `run_id`, `check_id`, `rule_id`, `subject_path`, `method`, `required`, `applicability: applicable|not_applicable|unknown`, `result: PASS|FAIL|NOT_RUN|ERROR|NOT_APPLICABLE`, `reason`, and evidence references. Required/advisory selection and trial applicability are recorded before results. Unknown applicability uses NOT_RUN, not NOT_APPLICABLE.

Each finding has `finding_id`, `rule_id`, `category`, `severity: blocker|major|minor|advisory`, subject path/locator, source and observation references, factual description, user impact, proposed correction, preserved requirements, verification cases, and `disposition: proposed|selected|deferred|rejected`. Categories distinguish standards defects, workflow bugs, instruction issues, resource/tool issues, enhancements, enforcement gaps, and input/evidence limitations. Severity reflects impact; it does not upgrade a recommendation into a format requirement.

Construct finding IDs as `F-` followed by the full SHA-256 of the compact UTF-8 JSON array `[rule_id, subject_path, anchor, occurrence]`. Use forward-slash paths; normalize anchor line endings to LF and trim surrounding whitespace; occurrence is the zero-based ordinal of that exact anchor within the file. For file-absence findings, use anchor `MISSING_FILE` and occurrence zero. Preserve the identity array in the finding record. Equal identities deduplicate; a hash collision with different identity material is an evidence error, not a silent merge. Across changed bytes, use an explicit predecessor ID where semantic matching establishes continuity. Do not claim identical semantic findings from repeated model runs; byte-level checks may be deterministic while interpretation can vary.

### Assessment reduction and readiness

For each of standards compliance, workflow correctness, instruction quality, and behavioral evaluation: FAIL when an applicable required check fails; otherwise INCOMPLETE when a required check is NOT_RUN/ERROR or applicability is unresolved; otherwise PASS. A genuinely inapplicable dimension is NOT_APPLICABLE with rationale. Keep incomplete checks visible even when FAIL takes precedence. Advisory findings do not automatically fail a dimension.

Overall assessment is FAIL if any required dimension fails; otherwise INCOMPLETE if any is incomplete or source readback changed; otherwise PASS. Report `assessment_completed` separately from outcome: a completed review can conclude FAIL or INCOMPLETE. Missing target is a completed intake with no package assessment, not a passed validation.

Builder readiness is separate: `NO_CHANGE`, `REVIEW_REQUIRED`, `READY`, or `BLOCKED`. Apply this order: a material unresolved contract, identity, evidence, capability, or authorization-scope issue is BLOCKED; otherwise no proposed change is NO_CHANGE; otherwise a proposal awaiting the selected human review is REVIEW_REQUIRED; otherwise a fully approved executable handoff is READY. Pending review alone is REVIEW_REQUIRED, not a separate authorization-scope error. READY requires recorded review authorization bound to the proposal digest and target, a complete contract, and verified existing baseline or implemented adoption capability plus its explicit managed-path authorization. Missing baseline/adoption support is BLOCKED for execution, even when the proposal is fully reviewable. Represent proposal review state separately as `not_needed|pending|approved|changes_requested` so one state cannot conceal the other. NO_CHANGE does not itself imply a passed assessment.

The exact compliance claim is: all applicable mandatory checks in rule-set digest X passed for package digest Y. Include evaluated/total required coverage, advisory issues, excluded scope, and source freshness. Never equate this with framework acceptance, guaranteed future execution, or complete current standards coverage when sources are incomplete.

## Concrete schema conventions for v1

Top-level JSON records use schema_version "1", run_id and target_name where applicable. `sources.json` contains `sources`; `rule-set.json` contains `rules`; `workflow-map.json` contains `steps`. Source records use source_id, url or original_path, retrieved_at_utc (null if unknown), sha256, snapshot_path, sections and freshness. Rules use rule_id, revision, title, source_refs, authority_class, applicability, method, expected_observation, required and limitation. A source reference includes path, sha256, source_id and locator; locator is a section string or an object containing line_start/line_end or start_byte/end_byte. Locators are claims requiring manual support review.

Check evidence uses `evidence` arrays of reference objects. An optional `dimension` is standards, workflow, instructions or behavior; document mappings for rule IDs when omitted. Findings use `identity` array, `subject_path`, `locator`, `source_refs`, `observation_refs`, `description`, `user_impact`, `proposed_correction`, `preserved_requirements`, `verification_cases` and the category/severity/disposition fields above. Use category values standards_defect, workflow_bug, instruction_issue, resource_tool_issue, enhancement, enforcement_gap or input_evidence_limitation.

`origin-record.json` fields: schema_version, run_id, target_name, original_source_root, manifest, specification (reference or null), origin_kind, history_kind, prior_evidence (reference or null), completeness (complete or partial), uncertainties (array), source_readback_state (UNCHANGED, SOURCE_CHANGED or NOT_RUN), historical_origin (unknown when no verified history). Describe origin separately from recovery completeness.

Reports must show required evaluated/total counts and unknown applicability; FAIL precedence does not erase NOT_RUN/ERROR rows. Record standards, workflow, instructions and behavior dimensions, plus the descriptive enforcement recommendation dimension. `assessment_completed` means the selected review was finished with honest observations, not that each capability executed. Do not call an empty rule set complete coverage.

Run `records --run-root <run>` only after references exist. It checks supported machine shapes, duplicate/non-finite input, file-reference digests, findings' identity material and declared statuses where represented. It cannot establish historical truth, authorization, source passage support, unrecorded check completeness, or future enforceability. Read the output's coverage/limitations and manually inspect unsupported schemas. Never recursively interpret inspected target JSON under source/ or trial fixtures as validator records.
