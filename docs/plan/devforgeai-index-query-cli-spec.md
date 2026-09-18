---
id: DEVFORGEAI-INDEX-QUERY-001
specification_version: "1.0"
status: proposed
recorded: "2026-09-13"
implementation_status: not_started
depends_on: DEVFORGEAI-INDEX-SERVICE-001
---

# DevForgeAI Index Query CLI Extension Specification

## 1. Purpose, dependency, and boundaries

Extend the `devforgeai` executable and Rust daemon defined by the [index service MVP specification](devforgeai-index-service-mvp-spec.md). Provide predictable structural and lexical retrieval so Codex and developers can discover existing code, inspect it with provenance, and decide whether to reuse, extend, compose, or create functionality.

This document is a proposed implementation contract, not a statement that the commands exist. Authoring it does not implement or install them. A subsequent implementation request must select it. MUST and MUST NOT are normative.

Use the existing service, database, IPC client, project registry, WSL bridge, error envelope, and lifecycle controls. Do not create a second indexer, copy index data into a CLI-owned cache, read SQLite from the CLI, or add MCP. Runtime queries do not execute project code or modify project source.

The service specification owns hosting, transport, identities, job semantics, generations, parser capabilities, and management operations. This specification owns query operations, result records, retrieval behavior, and Codex usage documentation. Both use protocol major version 1. A conflict must be resolved by revising the documents together, not by client-specific fallback behavior.

### 1.1 Required MVP outcome

A user can search a registered project by symbol name or by words appearing in documentation, comments, signatures, and source; obtain complete bounded symbol context; inspect outlines and candidate call syntax; and identify coverage/freshness gaps. A brownfield discovery workflow must work even when the requested feature name differs from the existing method name, provided there is useful lexical overlap in the indexed evidence.

No embeddings, inferred synonyms, model-generated summaries, semantic equivalence scores, resolved cross-file references, guaranteed duplication detection, source edits, or framework acceptance decisions are provided. Similar-purpose code with no shared searchable terms may be missed. An empty search is not proof that functionality is absent.

### 1.2 Mandatory engineering policy

Follow [repository guidance](../../AGENTS.md) and the companion's section 1.4: compiled Rust framework implementation, red -> green -> refactor -> QA, measured executed-line coverage >=95%, and required-case pass rate >=95%, independently per required platform. Retain denominators, exclusions, raw reports, and execution evidence; skipped/blocked/errored/unexecuted required cases are not passes. No failed mandatory acceptance scenario, unresolved regression, or authority/security invariant is waived by a numeric floor. Do not claim enforcement that has not been implemented and qualified.

All query behavior must be executable and verifiable through Codex CLI terminal. The extension does not create skills; if a separate selected skill build integrates it, that build must include its bound Python JSONL runner and deterministic graders. Python supplies evaluation evidence; compiled Rust retains all framework authority. Do not introduce ceremonial checks or speculative runtime claims into documentation or reports.

## 2. Commands and selection rules

**DQ-001 — Common arguments.** Query commands accept:

| Argument | Contract |
| --- | --- |
| `--environment <alias>` | Default `local`; Windows aliases may target registered WSL users. |
| `--project <id>` | Required; obtained from `project list`. No silent current-directory project selection. |
| `--json` | Exactly one versioned JSON envelope on stdout. Human-readable mode is default. |
| `--timeout-ms <n>` | Same bounds/default as the service specification. |
| `--require-current` | Request the freshness barrier in section 5; never silently accept an older index. |
| `--generation <id>` | Select a retained published generation; incompatible with `--require-current`. |

Ordinary queries select the current published generation once at admission. All fields and items in that response belong to it. A missing initial generation returns `INDEX_NOT_READY`. Queries do not start stopped daemons or wake stopped WSL distributions. Use `daemon start` explicitly first.

**DQ-002 — Search.**

```text
devforgeai code search --project <id> --query <text>
    [--field all|name|signature|docs|comments|code]
    [--path-prefix <relative-directory>] [--language <language>]
    [--limit <n>] [--cursor <opaque-token>] [--json]
```

Search combines declaration records and file text records according to section 4. `--field` defaults to `all`. `docs` searches attached documentation; `comments` searches internal and unattached comments. For text-only files, all content belongs to `code` (raw text), not an invented structural field. Empty or whitespace-only queries are invalid. Maximum query length is 4,096 UTF-8 bytes. Parameterize database queries; user input is not raw SQL or unrestricted FTS syntax.

**DQ-003 — Named symbols.**

```text
devforgeai code symbols --project <id> --name <name>
    [--match exact|prefix] [--kind <kind>] [--language <language>]
    [--path-prefix <relative-directory>] [--limit <n>] [--cursor <token>] [--json]
```

Default `--match exact` uses the identifier's original case. Prefix matching is also case-sensitive. Multiple declarations with the same name remain separate results. A name search finding nothing succeeds with an empty result; it is not `SYMBOL_NOT_FOUND`. This command does not resolve a reference to its declaration.

**DQ-004 — File outline.**

```text
devforgeai code outline --project <id> --path <relative-path>
    [--limit <n>] [--cursor <token>] [--json]
```

Return a flat source-ordered list with `parent_symbol_id`/`parent_node_id` for hierarchy. Include nested declarations and anonymous function outline nodes where adapters expose them. A text-only file returns an empty outline with `structural_support=false`; an excluded, unindexed, or nonexistent path reports its distinct known coverage reason rather than pretending it is an empty parsed file. A path not known to the generation returns `FILE_NOT_INDEXED` (exit 6).

**DQ-005 — Symbol inspection.**

```text
devforgeai code inspect --project <id> --symbol <symbol-id>
    [--part all|declaration|docs|comments]
    [--offset-bytes <n>] [--max-bytes <n>] [--json]
```

Default part is `all`: declaration source plus attached documentation, and internal comments as referenced ranges. Avoid duplicating internal comment text already contained in the declaration. Return source from captured index bytes, never from an unchecked live read. The result identifies containing declarations and relevant import syntax from the same file; import listings can be bounded separately and indicate truncation.

Symbol IDs encode or refer to their project and generation. An ID from the previous generation must be accompanied by matching `--generation`; otherwise return `STALE_SYMBOL`. An ID for an expired generation returns `SNAPSHOT_EXPIRED`. A nonexistent ID within the selected retained generation returns `SYMBOL_NOT_FOUND`. Renamed/moved symbols do not silently acquire the old identity.

**DQ-006 — Candidate calls.**

```text
devforgeai code calls --project <id> --name <callee-name>
    [--path-prefix <relative-directory>] [--language <language>]
    [--limit <n>] [--cursor <token>] [--json]
```

Match the extracted call spelling exactly and case-sensitively. With an unqualified name, match the final syntactic name segment; with a qualified name, match the full adapter-normalized spelling. Return the original spelling, enclosing symbol, and call-site range. Label every result `resolution=syntactic_candidate`; `service.validate()` does not prove a call to a particular `validate` declaration. Document per-language normalization and unsupported computed calls in adapter capability output. Do not label this operation “all callers.”

**DQ-007 — Coverage.**

```text
devforgeai code coverage --project <id>
    [--reason <reason-code>] [--limit <n>] [--cursor <token>] [--json]
```

Return generation-level coverage counters, supported adapter versions, effective exclusion summary, and paginated file-level gaps. This command can report project coverage before any generation exists, using null generation and unknown freshness. It never needs a scan unless `--require-current` is explicitly requested. Status/coverage remains useful while paused or degraded.

**DQ-008 — Filters and bounds.** Language values are `rust`, `python`, `javascript`, `typescript`, and `text`. Kind values come from a documented common set: `function`, `method`, `class`, `type`, `trait`, `interface`, `module`, and `constant`; adapters declare which kinds they actually extract. Constants are optional adapter capability in v1 and cannot be presented as universally supported.

List commands default to 20 items, accept 1 through 100, and return `next_cursor` when more items remain. Path filters use project-relative forward-slash form with exact normalized component matching; reject absolute paths and `..` traversal. Apply native filesystem case semantics, preserving original spelling in results. Do not interpret filters as arbitrary glob/regex expressions.

Inspection defaults to a 32 KiB source-text budget and accepts up to 256 KiB per response. Offsets are relative to the selected source part and must be on UTF-8 character boundaries. Return the next byte offset for continuation, explicit truncation, and the original full range; never imply an excerpt is a complete function. Search snippets default to at most 512 UTF-8 bytes per item, aligned to character boundaries. All query responses also obey the shared 8 MiB transport maximum.

## 3. Protocol operations and evidence records

**DQ-009 — Operations.** Add `code.search`, `code.symbols`, `code.outline`, `code.inspect`, `code.calls`, and `code.coverage` to the shared operation registry. The WSL bridge forwards the same requests and results. No client-only interpretation changes service behavior. Convert CLI flags into typed params, validated by both client and service. Supply JSON Schemas, examples, and unknown-field/error tests as implementation artifacts.

Successful query `data` contains:

| Field | Meaning |
| --- | --- |
| `project_id` | Daemon-owned index project identity. |
| `generation_id` | Immutable result generation, nullable only where explicitly allowed for coverage. |
| `observed_at` | RFC 3339 UTC observation time. |
| `freshness` | Observed-current, dirty, or unknown, with last reconciliation time and known pending changes. |
| `coverage` | Complete/partial/unknown plus eligibility, text, structural, exclusion, skip, and failure counters. |
| `items` or `symbol` | Operation-specific typed records. |
| `next_cursor` | Opaque continuation for paginated commands, otherwise null. |
| `truncated` | True if returned content was bounded; continuation information is mandatory when available. |
| `warnings` | Named nonfatal coverage/capability limitations. |

Use lowercase underscore enum values in serialized JSON, including `observed_current` and `syntactic_candidate`. Request/response identity, service version, environment identity, `ok`, and error fields remain in the service-owned outer envelope. Do not emit a top-level framework `accepted` or `passed` field.

**DQ-010 — Source references.** Each source-backed record includes relative path, language, original display name where relevant, file SHA-256, file byte length, generation ID, adapter/query version, and extraction status. Ranges use zero-based start-inclusive/end-exclusive UTF-8 byte offsets into the exact captured file, including any BOM. Human-readable locations are one-based lines and columns measured in Unicode scalar values; JSON retains byte offsets as the authoritative coordinates. Do not confuse Tree-sitter byte columns with display columns. For noncontiguous attached documentation, return an array of ranges.

Search items identify `record_kind` (`symbol` or `file`), optional symbol identity, containing symbol, matching fields, rank score, and matching snippets with source ranges. Return source excerpts as data, never as instructions to execute. Inspection exposes original comments separately from any service metadata. No LLM-generated explanations or inferred behavior enter the extracted-fact fields.

**DQ-011 — Errors.** Reuse every shared exit category. Add `FILE_NOT_INDEXED` to exit 6, with details distinguishing known excluded/skipped paths from paths absent from the generation. Unsupported filters and invalid cursor/query combinations use `INVALID_ARGUMENT`. Query timeout uses exit 7. Corrupt storage uses exit 8. A syntactically valid query with no matches is exit 0 even when coverage is partial, unless `--require-current` demands complete eligibility coverage. Such results must still include the partial-coverage warning.

## 4. Lexical retrieval and deterministic ranking

**DQ-012 — Search units.** Index a named symbol as a retrieval unit containing its name, signature, attached documentation, internal comments, and declaration source. For eligible structural-language files, also provide file-level text records for imports, file headers, top-level code, and other bytes not owned by a named symbol. A nested named symbol owns its body for retrieval to reduce repeated matches in parents; inspection still returns the complete parent declaration. Text-only files use file-level records. Long file records may be chunked internally, but results deduplicate the same matched source range and retain file identity.

Store search terms with links to exact source spans. A source match that lies in multiple structural views must not create several identical search hits. Do not discard a function because its comments are absent; its signature and implementation remain searchable.

**DQ-013 — Query semantics.** Normalize query terms with SQLite FTS5 `unicode61`, case-folding and diacritic removal. During indexing, add searchable aliases for snake_case and ASCII camelCase identifier segments, retaining original spelling for display and exact symbol lookup. Apply the same identifier splitting to queries. Do not claim stemming, automatic synonyms, or semantic similarity.

Treat a sequence of terms as an AND query; double-quoted text requests an ordered phrase in a field. Literal punctuation outside quotes acts as a separator. Reject unmatched quotes and user FTS operators rather than pass them through. All examples and help must state these semantics. A caller can broaden a query by issuing a second query with fewer terms; the service never silently relaxes a failed query.

**DQ-014 — Ranking.** Use the pinned SQLite FTS5 BM25 implementation with field weights: name 10, signature 5, attached docs 4, internal/unattached comments 2, and code/raw text 1. Prepend an exact case-insensitive full-name match tier for single-name queries. Within a tier, sort by BM25 relevance, then normalized relative path, starting byte offset, and record ID. Record the ranking implementation version. Scores are relative lexical relevance, not confidence or probability that code satisfies a requirement.

**DQ-015 — Pagination.** Cursors bind the selected generation, operation, normalized query and filters, ordering, and next position. Subsequent requests must repeat matching query/filter values and cannot change the limit. Reject altered or malformed cursor data. Use a daemon-owned persisted authentication key for cursor integrity; no credentials appear in output. A cursor is not an access-control token. Once its generation is no longer retained, return `SNAPSHOT_EXPIRED` rather than switch to newer data. Generation retirement during an admitted request must not invalidate that request's read transaction.

## 5. Freshness, concurrency, and failure behavior

**DQ-016 — Ordinary queries.** Query one committed generation and return its evidence/freshness qualifiers. Paused indexing still supports ordinary reads. If a newer generation is staging, do not wait for it. If files have changed since capture, cached source remains internally consistent and the response reports known dirty state. No freshness label proves absence of an unobserved concurrent edit.

**DQ-017 — Explicit freshness barrier.** `--require-current` requests a daemon reconciliation job or joins an already-running compatible reconciliation, waits within the end-to-end deadline, then reads the resulting generation in one admission step. This is the only query option that intentionally schedules indexing work. It does not start a daemon or wake WSL.

Require active indexing, an available root, successful eligible-file reconciliation, and no known unprocessed events at admission. Excluded files are accounted for and do not defeat complete coverage; eligible files skipped for encoding/size, unstable reads, parse errors, or permission failures make this strict request incomplete. Text-only files can satisfy complete text coverage while explicitly lacking structural support. Return `INDEX_PAUSED`, `INDEX_INCOMPLETE`, or `TIMEOUT` as applicable. Never relax the caller's freshness requirement.

A timed-out waiting query does not cancel a shared reconciliation job. Include its job ID in error details if available. If new changes prevent a clean barrier before the deadline, return timeout/incomplete details. `--require-current` is incompatible with a cursor or explicit generation; callers page the returned generation afterward using its cursor without repeating the freshness flag.

**DQ-018 — Deletion and retirement.** Deletions disappear from newly published generations but can remain inspectable through explicitly selected retained generations. Project removal makes its queries unavailable immediately after the removal transaction; in-flight read transactions may finish before cache reclamation. Never redirect a missing project or environment to another available one. A service restart preserves valid retained generations and cursor integrity; an explicit cache rebuild invalidates them with a named expiration/not-ready result.

**DQ-019 — Query bounds.** Enforce deadlines in database progress/cancellation hooks and while formatting output. Client disconnection cancels query work, without cancelling shared indexing. Parameterized SQL and size limits apply to all commands. An access-denied or protocol error cannot trigger an alternate endpoint or unrestricted filesystem fallback.

## 6. Codex and human workflow

**DQ-020 — Documentation.** Provide help and examples for PowerShell and POSIX shells. Document the following intended sequence, without installing or modifying skills, `AGENTS.md`, or Codex configuration:

1. Inspect daemon/project status and choose the explicit environment/project.
2. Search names, documentation, and code for existing functionality using several focused lexical queries where necessary.
3. Inspect candidates from their identified generation and note partial extraction or stale coverage.
4. Examine candidate call syntax, actual callers, tests, and source contracts through normal development tools; a syntactic call listing alone is not complete impact analysis.
5. Record whether to reuse, extend, compose, or create, with source references and reasons.
6. Before making changes based on captured evidence, compare relevant current source hashes using the framework's existing development tools or request a fresh query. The index does not authorize edits.

For example, a fixture contains `reconcile_entries()` documented as “Combine duplicate customer records, retaining the newest version.” A search for `duplicate customer` must find it even though its name lacks those terms. Inspection must reveal the exact implementation and limitations. Do not promise a match for unrelated wording with no lexical overlap.

**DQ-021 — Output clarity.** Human output leads with project/environment, generation, freshness, and any coverage limitation, then relevant matches. JSON stays machine-oriented with stable fields. Label syntactic candidate calls, text-only matches, parse errors, and truncated excerpts explicitly. An empty-result message states that there were no matches within the indexed scope; it does not assert that equivalent functionality is absent.

## 7. Acceptance matrix

Run meaningful tests against real temporary daemons and synthetic registered roots, in addition to unit tests for tokenization/formatting. Use exact source hashes and expected ranges. Native Windows, Linux, and WSL results remain separately labeled.

| Scenario | Requirements | Required result |
| --- | --- | --- |
| DQ-A01: explicit target and stopped daemon | DQ-001 | No implicit project choice, startup, WSL wake, or fallback environment. |
| DQ-A02: lexical brownfield discovery | DQ-002, DQ-012, DQ-013, DQ-020 | Comment/doc match discovers the differently named helper; inspection provides exact code. |
| DQ-A03: deterministic ranking | DQ-013, DQ-014 | Names/docs weighted as specified; stable ties, phrase behavior, identifier splitting, and repeated results. |
| DQ-A04: symbol lookup/outline | DQ-003, DQ-004, DQ-008 | Duplicates and nested symbols remain distinct; text-only outline and unknown paths are honest. |
| DQ-A05: inspection provenance | DQ-005, DQ-010 | Hashes/ranges match captured bytes, including BOM, Unicode and CRLF; live-file changes cannot mix bytes. |
| DQ-A06: candidate call semantics | DQ-006 | Same-spelled methods return candidates with no false resolved-target claim; computed-call gaps reported. |
| DQ-A07: coverage and no-match | DQ-007, DQ-011, DQ-021 | Empty results succeed with scope qualifiers; missing eligible coverage remains visible. |
| DQ-A08: pause and freshness | DQ-016, DQ-017 | Ordinary reads work paused; strict reads fail paused; active barrier reconciles or fails explicitly. |
| DQ-A09: generation pagination | DQ-015, DQ-018 | Stable generation pages; altered cursor rejected; retired generation returns expiration, never silent switching. |
| DQ-A10: stale/deleted symbol | DQ-005, DQ-018 | Explicit retained snapshot can show old source; stale/default/expired references return distinct errors. |
| DQ-A11: output and error contract | DQ-009, DQ-011 | Schema-valid one-envelope stdout and documented exit categories for all error paths. |
| DQ-A12: output/query limits | DQ-002, DQ-008, DQ-019 | Malformed/large queries rejected; SQL/FTS injection treated as invalid/literal input; snippets and continuations bounded. |
| DQ-A13: concurrent reindex and timeout | DQ-016, DQ-017, DQ-019 | Coherent reads during publication; query timeout does not cancel shared indexing. |
| DQ-A14: Windows/WSL/Linux shell use | DQ-001, DQ-009, DQ-020 | Paths with spaces and Unicode, quote characters, and stdin bridge round trips preserve values safely. |
| DQ-A15: source immutability | DQ-019, DQ-020 | Query operations never modify project bytes or execute repository scripts. |
| DQ-A16: structural languages | DQ-003 through DQ-006 | Real adapter-backed retrieval works for Rust, Python, JS/JSX, TS/TSX; comments and unsupported constructs accurately labeled. |
| DQ-A17: engineering policy | Section 1.2 | Retained red/green/refactor/QA evidence, both measured quality floors >=95%, and terminal-only operation; mandatory failures are never converted to acceptance by aggregate percentages. |

Measure cold/warm query latency, p50/p95 for 100 fixed queries, output size, and peak memory using the service specification's benchmark fixture. Retain the query set and generation identity. Performance measurements do not establish retrieval completeness or semantic equivalence.

## 8. Implementation delivery and integration

After the service's protocol/index/client foundation exists, implement query types and service handlers, deterministic retrieval, CLI formatting, the WSL forwarding integration, and then native conformance tests. Reuse the same Rust client in the tray if query views are added later; a graphical code-search UI is not required here.

Deliver locked source, versioned operation/result schemas, sample JSON, command reference, PowerShell/POSIX examples, fixtures with expected results, tests, and retained native evidence. Verify the two documents' common options, limits, error codes, identity rules, and lifecycle assumptions together before release. Do not modify either installed skill package to make the demonstration work.

Release notes must separate structural extraction support, lexical search support, platform qualification, installation, and framework acceptance. This extension provides none of the protected acceptance authority described in the existing Rust enforcement design.

## 9. References

- [Companion service specification](devforgeai-index-service-mvp-spec.md): normative transport, lifecycle, storage, coverage, error/exit, and platform contracts.
- [Existing Rust enforcement design](devforgeai-codex-rust-enforcement-design.md): separate authority boundary; no implementation inherited by this query CLI.
- [Tree-sitter code navigation](https://tree-sitter.github.io/tree-sitter/4-code-navigation.html): structural tagging and documentation association.
- [Tree-sitter query syntax](https://tree-sitter.github.io/tree-sitter/using-parsers/queries/1-syntax.html): syntax captures and error regions.
- [SQLite FTS5](https://www.sqlite.org/fts5.html): tokenizer and BM25 facilities used by the proposed lexical layer; pin and qualify the shipped implementation.

The retrieval rules, weights, command names, protocol fields, and behavioral requirements above are DevForgeAI design decisions, not guarantees supplied by Tree-sitter or SQLite.
