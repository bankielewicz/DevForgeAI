# Custody Chain Audit: STORY-013 through STORY-033

**Audit Date:** 2026-02-14
**Auditor:** Claude (DevForgeAI session)
**Scope:** Full provenance review from brainstorms through requirements, epics, sprints, and into story files STORY-013 to STORY-033
**Purpose:** Detect context loss, ambiguity, and broken traceability; produce remediation guide for future sessions

---

## 1. Document Inventory

| Layer | Document | Path |
|-------|----------|------|
| Brainstorm | BRAINSTORM-001 | `devforgeai/specs/brainstorms/BRAINSTORM-001-treelint-ast-code-search.brainstorm.md` |
| Brainstorm | BRAINSTORM-002 | `devforgeai/specs/brainstorms/BRAINSTORM-002-indexing-efficiency-language-expansion.brainstorm.md` |
| Research | RESEARCH-001 | `devforgeai/specs/Research/RESEARCH-001-claude-code-search-token-efficiency.research.md` |
| Research | RESEARCH-002 | `devforgeai/specs/Research/RESEARCH-002-incremental-indexing-daemon-restart.md` |
| Requirements | Requirements v1 | `devforgeai/specs/requirements/treelint-requirements.md` |
| Requirements | Requirements v2 | `devforgeai/specs/requirements/treelint-post-mvp-requirements.md` |
| ADR | ADR-001 through ADR-006 | `devforgeai/specs/adrs/ADR-00{1-6}-*.md` |
| Epic | EPIC-003 | `devforgeai/specs/Epics/EPIC-003-incremental-indexing.epic.md` |
| Epic | EPIC-004 | `devforgeai/specs/Epics/EPIC-004-csharp-language-support.epic.md` |
| Epic | EPIC-005 | `devforgeai/specs/Epics/EPIC-005-sql-language-support.epic.md` |
| Epic | EPIC-006 | `devforgeai/specs/Epics/EPIC-006-dependency-graph-api.epic.md` |
| Sprint | SPRINT-002 | `devforgeai/specs/Sprints/SPRINT-002-incremental-indexing.sprint.md` |
| Sprint | SPRINT-003 | `devforgeai/specs/Sprints/SPRINT-003-dependency-graph-api.sprint.md` |
| Stories | STORY-013 to STORY-033 | `devforgeai/specs/Stories/STORY-0{13-33}-*.story.md` |

---

## 2. Provenance Chain Map

```
BRAINSTORM-001 ──→ treelint-requirements.md ──→ EPIC-001 ──→ STORY-001..006 (out of scope)
   (RESEARCH-001/005)                         ──→ EPIC-002 ──→ STORY-007..012 (out of scope)

BRAINSTORM-002 ──→ treelint-post-mvp-requirements.md ──→ EPIC-003 ──→ SPRINT-002 ──→ STORY-013..017
   (RESEARCH-002)                                     ──→ EPIC-004 ──────────────→ STORY-018..023
                                                      ──→ EPIC-005 ──────────────→ STORY-024..029
                                                      ──→ EPIC-006 ──→ SPRINT-003 ──→ STORY-030..033

ADR-003 (C# grammar)       ← required by EPIC-004 ← accepted
ADR-004 (SQL grammar)       ← required by EPIC-005 ← accepted
ADR-005 (binary size relax) ← required by EPIC-004, EPIC-005 ← accepted
ADR-006 (SymbolType extend) ← required by EPIC-004, EPIC-005 ← accepted
ADR-TBD (XML parser crate)  ← required by STORY-023 ← NOT CREATED (BLOCKER)
```

### Chain Integrity Verdict

| Transition | Status | Notes |
|-----------|--------|-------|
| BRAINSTORM-001 → Requirements v1 | **PASS with warning** | Research ID mismatch (see F-005) |
| BRAINSTORM-002 → Requirements v2 | **PASS with warning** | Path case sensitivity (see F-009) |
| Requirements v1 → EPIC-001/002 | **PASS** | All 6 opportunities mapped to features |
| Requirements v2 → EPIC-003/004/005/006 | **PASS** | All 4 recommended epics created; MoSCoW preserved |
| EPIC-003 → SPRINT-002 → STORY-013..017 | **PASS** | All 5 features mapped to stories |
| EPIC-004 → STORY-018..023 | **PASS with blocker** | Missing ADR for STORY-023 (see F-001) |
| EPIC-005 → STORY-024..029 | **PASS with risk** | Grammar node names unknown (see F-002) |
| EPIC-006 → SPRINT-003 → STORY-030..033 | **PASS with warning** | Undeclared cross-deps (see F-003) |

---

## 3. Dependency Chain Validation

### EPIC-003 (Incremental Indexing)

```
STORY-013 (no deps) ─── ROOT
    ├── STORY-014 ──→ STORY-017
    ├── STORY-015 (parallel with 014)
    └── STORY-016 (parallel with 014, 015)
```

**Verdict:** Valid acyclic graph. No circular dependencies. No missing links.

### EPIC-004 (C# Language Support)

```
STORY-018 (no deps) ─── ROOT
    └── STORY-019 ──→ STORY-020 ──→ STORY-021 ──→ STORY-022
                  └── STORY-023 (also blocked on ADR TBD)
```

**Verdict:** Valid chain. STORY-023 has a hard external blocker (missing ADR).

### EPIC-005 (SQL Language Support)

```
STORY-024 (no deps) ─── ROOT
    └── STORY-025 ──→ STORY-026 ──→ STORY-027 ──→ STORY-028 ──→ STORY-029
```

**Verdict:** Valid linear chain. STORY-025 dependency on STORY-026+ is architectural (not functional) — see F-003 note.

### EPIC-006 (Dependency Graph API)

```
STORY-011 (done) ──→ STORY-030 ─── ROOT
                         ├── STORY-031 ──┐
                         ├── STORY-032 ──┤
                         └───────────────┴── STORY-033
```

**Verdict:** Valid DAG. STORY-031 and STORY-032 have an undeclared mutual dependency (see F-003).

---

## 4. Findings

### CRITICAL Findings (Block Implementation)

---

#### F-001: STORY-023 Blocked — Missing ADR for XML Parser Crate

**Severity:** CRITICAL
**Affected Story:** STORY-023
**Affected Files:**
- `devforgeai/specs/Stories/STORY-023-csharp-csproj-project-parsing.story.md` (line 27, 40, 368-369)
- `devforgeai/specs/Epics/EPIC-004-csharp-language-support.epic.md` (line ~117, ~283)
- `devforgeai/specs/requirements/treelint-post-mvp-requirements.md` (Section 9.2)

**Evidence:**
> STORY-023 line 27: "This story requires an ADR for XML parser crate selection (currently TBD in the epic). The ADR must be approved before implementation begins."
> STORY-023 line 368-369: "XML parser crate selection requires a separate ADR (currently TBD in EPIC-004). Implementation cannot begin until the ADR is approved and the crate is added to dependencies.md."

**Impact:** STORY-023 cannot enter TDD Red phase. It should be in "Architecture" status, not "Backlog", since it has an unfulfilled architectural prerequisite.

**Remediation:**
1. Create `devforgeai/specs/adrs/ADR-007-xml-parser-crate-selection.md` evaluating `quick-xml` vs `roxmltree`
2. Update `devforgeai/specs/context/dependencies.md` with the selected crate after ADR acceptance
3. Update STORY-023 to reference ADR-007 instead of "ADR TBD"
4. Change STORY-023 status from `Backlog` to `Architecture` until ADR is accepted

**Verification:** `grep -r "ADR TBD" devforgeai/specs/Stories/STORY-023*` returns no matches after fix.

**Session Handoff Context:** The story itself recommends `quick-xml` v0.31+ (~100KB binary impact, byte-offset position tracking). XXE protection is a critical security requirement — the selected parser must NOT expand external entities. Use ADR-003 as a template for format.

---

#### F-002: STORY-026/027/028 — Tree-sitter-sql AST Node Names Unknown

**Severity:** CRITICAL
**Affected Stories:** STORY-026, STORY-027, STORY-028
**Affected Files:**
- `devforgeai/specs/Stories/STORY-026-sql-procedural-object-extraction.story.md` (TL-002)
- `devforgeai/specs/Stories/STORY-027-sql-schema-object-extraction.story.md` (TL-002)
- `devforgeai/specs/Stories/STORY-028-sql-trigger-constraint-extraction.story.md` (TL-002)

**Evidence:**
> STORY-026 TL-002: "Exact AST node names for CREATE PROCEDURE/FUNCTION depend on grammar's parser rules, which must be discovered during implementation."

All three stories share the identical risk: the tree-sitter query strings that form the core implementation cannot be written until the grammar is inspected.

**Impact:** TDD Red phase cannot specify exact node names in test expectations. The developer must perform grammar introspection before writing tests.

**Remediation:**
1. Before starting STORY-026, run a grammar discovery spike:
   ```rust
   // Spike: parse a sample SQL file and dump all node kinds
   let parser = tree_sitter::Parser::new();
   parser.set_language(tree_sitter_sql::language()).unwrap();
   let tree = parser.parse(sql_content, None).unwrap();
   // Walk tree and print all node.kind() values
   ```
2. Document discovered node names in a new file: `devforgeai/specs/Research/RESEARCH-003-tree-sitter-sql-node-mapping.md`
3. Update STORY-026, 027, 028 TL-002 sections with resolved node names
4. This discovery should cover ALL SQL object types (procedure, function, table, view, index, trigger, schema, alter table) in a single spike, preventing re-discovery per story

**Verification:** Each story's TL-002 section updated from "must be discovered" to "resolved: [node names]".

**Session Handoff Context:** The grammar is `tree-sitter-sql v0.0.2` (early maturity, PostgreSQL-focused). Some node types may not exist at all (e.g., CREATE SCHEMA, ALTER TABLE ADD CONSTRAINT). If a node type doesn't exist, the corresponding AC should be updated to document graceful degradation behavior.

---

### HIGH Findings (Context Loss / Ambiguity Causing Rework Risk)

---

#### F-003: STORY-031 and STORY-032 Have Undeclared Mutual Dependency

**Severity:** HIGH
**Affected Stories:** STORY-031, STORY-032
**Affected Files:**
- `devforgeai/specs/Stories/STORY-031-cli-dependency-query-flags.story.md` (line 9: `depends_on: ["STORY-030"]`)
- `devforgeai/specs/Stories/STORY-032-compact-json-dependency-output.story.md` (line 9: `depends_on: ["STORY-030"]`)

**Evidence:**
- STORY-031 AC#3 says output "matches EPIC-006 compact JSON spec" — this is the `DepsResult` struct defined in STORY-032
- STORY-032 AC#5 says "CLI deps command outputs DepsResult format in focused query mode" — this requires STORY-031's `--direction`/`--depth` flags

Both stories declare `depends_on: ["STORY-030"]` only, but each functionally requires the other's output.

**Impact:** If a developer implements STORY-031 first, they will need to either create the `DepsResult` struct (duplicating STORY-032 work) or implement STORY-032 first. The SPRINT-003 file correctly shows them as parallel, which creates a sequencing trap.

**Remediation:**
1. In STORY-032, change `depends_on: ["STORY-030"]` to `depends_on: ["STORY-030"]` (keep as-is — STORY-032 defines the struct)
2. In STORY-031, change `depends_on: ["STORY-030"]` to `depends_on: ["STORY-030", "STORY-032"]`
3. Update SPRINT-003 recommended execution order:
   ```
   1. STORY-030 (IPC foundation)
   2. STORY-032 (define DepsResult/DepEntry structs)
   3. STORY-031 (CLI flags, uses DepsResult)
   4. STORY-033 (transitive traversal)
   ```

**Verification:** `grep "depends_on" devforgeai/specs/Stories/STORY-031*` shows `["STORY-030", "STORY-032"]`.

**Session Handoff Context:** SPRINT-003 dependency graph (line 33-38) must also be updated to show STORY-031 depending on STORY-032. The sprint's "parallel tracks" recommendation (Week 2: STORY-031 + STORY-032 in parallel) must change to sequential: STORY-032 first, then STORY-031.

---

#### F-004: ADR-006 "Add ALL Variants First" Contradicts Incremental Story Approach

**Severity:** HIGH
**Affected Stories:** STORY-019, STORY-026, STORY-027, STORY-028
**Affected Files:**
- `devforgeai/specs/adrs/ADR-006-symboltype-enum-extension-strategy.md` (line 252)
- `devforgeai/specs/Stories/STORY-026-sql-procedural-object-extraction.story.md` (adds Procedure only)
- `devforgeai/specs/Stories/STORY-027-sql-schema-object-extraction.story.md` (adds Table, View)
- `devforgeai/specs/Stories/STORY-028-sql-trigger-constraint-extraction.story.md` (adds Trigger)

**Evidence:**
> ADR-006 line 252: "First story in EPIC-004 or EPIC-005 (whichever starts first) adds ALL new variants from this ADR"

But the EPIC-005 stories add variants incrementally: STORY-026 adds `Procedure`, STORY-027 adds `Table` and `View`, STORY-028 adds `Trigger`.

For EPIC-004, STORY-019 adds `Interface`, `Record`, `Property`, `Event` — this appears to follow ADR-006 more closely since it adds C#-relevant types in one shot. However, it doesn't add the SQL types (Table, View, Trigger, Procedure).

**Impact:** If EPIC-004 stories run first (STORY-019), ADR-006 says ALL variants should be added then — including SQL types. If EPIC-005 stories run first (STORY-026), only `Procedure` is added, violating ADR-006. Each incremental addition requires updating all match arms in `symbols.rs` and `args.rs`, creating merge conflict risk.

**Remediation (choose one):**
- **Option A (follow ADR-006 strictly):** Whichever epic starts first, its first extraction story adds ALL 8 new SymbolType variants (Interface, Record, Property, Event, Table, View, Trigger, Procedure) even if the extraction logic comes later. Update STORY-019 or STORY-026 (whichever runs first) to include all variant additions.
- **Option B (amend ADR-006):** Update ADR-006 to explicitly allow incremental variant addition per-epic, documenting the tradeoff. Add a note: "Variants may be added per-epic rather than all-at-once if epics are developed sequentially."

**Verification:** Check `src/parser/symbols.rs` SymbolType enum — after the first extraction story completes, all 8 new variants exist.

**Session Handoff Context:** STORY-019 currently adds Property and Event "even though extraction is in STORY-020" — this is the right instinct but should be extended to all 8 variants if Option A is chosen. The relevant code files are `src/parser/symbols.rs` (SymbolType enum, Display impl, as_str method) and `src/cli/args.rs` (CLI SymbolType enum).

---

#### F-005: BRAINSTORM-001 Research ID Mismatch (RESEARCH-005 vs RESEARCH-001)

**Severity:** HIGH
**Affected Files:**
- `devforgeai/specs/brainstorms/BRAINSTORM-001-treelint-ast-code-search.brainstorm.md` (lines 11, 47, 405)
- `devforgeai/specs/requirements/treelint-requirements.md` (line 8, 310, 320, 441)

**Evidence:**
> BRAINSTORM-001 line 11: `related_research: [RESEARCH-005]`
> BRAINSTORM-001 line 47: "validated by RESEARCH-005 market data"
> BRAINSTORM-001 line 405: "Research Used | RESEARCH-005"

> Requirements v1 line 8: "Source: BRAINSTORM-001, RESEARCH-001"
> Requirements v1 line 441: "RESEARCH-001 | devforgeai/specs/research/RESEARCH-001-claude-code-search-token-efficiency.research.md"

The brainstorm cites RESEARCH-005. The requirements doc cites RESEARCH-001. Only RESEARCH-001 exists on disk at `devforgeai/specs/Research/RESEARCH-001-claude-code-search-token-efficiency.research.md`. RESEARCH-005 does not exist.

**Impact:** Automated citation validation against BRAINSTORM-001 would fail. The custody chain has a broken back-reference at the brainstorm level.

**Remediation:**
1. In BRAINSTORM-001, change all 3 occurrences of `RESEARCH-005` to `RESEARCH-001`:
   - Line 11: `related_research: [RESEARCH-001]`
   - Line 47: "validated by RESEARCH-001 market data"
   - Line 405: "Research Used | RESEARCH-001"

**Verification:** `grep "RESEARCH-005" devforgeai/specs/brainstorms/BRAINSTORM-001*` returns no matches.

**Session Handoff Context:** This is a numbering error from the brainstorm creation phase. The actual research document is RESEARCH-001. No content is lost — only the ID reference is wrong.

---

#### F-006: STORY-029 Architectural Tension — Additive Extraction vs Pre-Processing

**Severity:** HIGH
**Affected Story:** STORY-029
**Affected File:** `devforgeai/specs/Stories/STORY-029-sql-multi-dialect-support.story.md`

**Evidence:**
> Line 384 (BR-004): "Dialect-specific extraction is additive — it enhances generic extraction, it does not replace it"
> Line 451-455 (TL-003): "DELIMITER is a MySQL client command — the tree-sitter-sql grammar may not recognize it as a syntactic element [...] pre-process MySQL files to detect DELIMITER blocks before tree-sitter parsing; strip DELIMITER lines"
> Lines 734-735 (Open Questions): Whether MySQL DELIMITER and T-SQL GO require pre-processing or post-processing is explicitly unresolved

**Impact:** The "additive" principle (BR-004) states dialect processing enhances but never replaces generic extraction. However, if MySQL DELIMITER lines confuse the tree-sitter parser, the generic parse produces incorrect/no symbols. Pre-processing (stripping DELIMITER lines before parse) means the generic parse runs on modified content — this is replacement, not augmentation. The architectural principle and the implementation approach are in tension.

**Remediation:**
1. Update STORY-029 BR-004 to clarify the boundary:
   ```
   "Dialect-specific extraction is additive where possible. For dialects requiring content
   pre-processing (MySQL DELIMITER, T-SQL GO), the pre-processed content is passed to the
   generic parser. The generic parser's output on pre-processed content IS the baseline;
   dialect strategies then augment that baseline. Pre-processing is permitted when the
   alternative is a failed generic parse."
   ```
2. Add a new AC or update AC#1/AC#3 to explicitly test that pre-processed files still produce valid generic extraction results

**Verification:** Read STORY-029 BR-004 — it explicitly addresses pre-processing as an acceptable deviation from pure additive.

**Session Handoff Context:** The open questions at lines 734-735 are correctly flagged for resolution at sprint start. The remediation here is to update the principle to match reality, not to change the implementation approach.

---

#### F-007: STORY-020 Internal Inconsistency — Variable vs Constant for const Fields

**Severity:** HIGH
**Affected Story:** STORY-020
**Affected File:** `devforgeai/specs/Stories/STORY-020-csharp-method-property-extraction.story.md`

**Evidence:**
> Line 138 (AC#5 then-clause): "symbol_type=Variable (per ADR-006: fields map to Variable)"
> Line 521 (Edge Case #8): "Const field: public const int MaxRetries = 3; — should extract as Variable (or Constant if const keyword detected)."
> Line 556 (Verification): "Const field -> Variable (or Constant)"
> Line 688 (Design Decision): "Const fields could map to Constant instead of Variable — decided to use Variable for consistency"

The AC says "Variable", the edge case says "Variable (or Constant)", and the design decision says "Variable". This is internally contradictory.

**Impact:** A developer writing TDD tests would write conflicting assertions depending on which section they read. If they read line 521 first, they might test for Constant. If they read line 688 first, they'd test for Variable.

**Remediation:**
1. In STORY-020, update line 521 to remove the ambiguity:
   ```
   8. **Const field:** `public const int MaxRetries = 3;` — should extract as Variable (per ADR-006 and design decision: Variable for consistency).
   ```
2. Update line 556:
   ```
   - Const field -> Variable
   ```

**Verification:** `grep -n "or Constant" devforgeai/specs/Stories/STORY-020*` returns no matches.

**Session Handoff Context:** ADR-006 maps C# fields to Variable (line 368 of STORY-020 confirms: "C# fields MUST map to SymbolType::Variable per ADR-006"). The design decision at line 688 aligns. Only the edge case notes and verification checklist contain the stale "(or Constant)" language.

---

#### F-008: STORY-016 Has Three Unresolved Architectural Gaps

**Severity:** HIGH
**Affected Story:** STORY-016
**Affected File:** `devforgeai/specs/Stories/STORY-016-index-health-api.story.md`

**Evidence and Gaps:**

**Gap A — `src/cli/commands/daemon.rs` may not exist:**
The story references `src/cli/commands/daemon.rs` (lines 154, 173, 212, 538, 539, 544, 553, 570) as the CLI handler location. However, the project's architecture in CLAUDE.md only shows `src/cli/commands/search.rs`. This file may need to be created. The story does not specify whether this is a new file or an extension of an existing file.

**Gap B — `reindex_queue_depth` requires cross-component access:**
Line 525: "reindex_queue_depth from watcher pending queues". The health handler in `server.rs` needs access to the `FileWatcher`'s internal pending set sizes. The story does not specify the data access mechanism (Arc<Mutex<>>, channel, shared struct, etc.).

**Gap C — Daemon start time storage:**
Line 410-411: stale_count uses "daemon start time" as the threshold. The story doesn't specify where or how the daemon records its start time. Is it a field on the DaemonServer struct? A global? Passed as a parameter?

**Impact:** A developer starting STORY-016 will need to make three architectural micro-decisions not covered by the story spec. These could lead to inconsistent implementations across sessions.

**Remediation:**
1. Add a "Pre-Implementation Notes" section to STORY-016 specifying:
   ```
   ### Pre-Implementation Decisions (resolve before TDD Red)

   A. **daemon.rs file:** Create new file `src/cli/commands/daemon.rs` and register in
      `src/cli/commands/mod.rs`. Pattern: follow `search.rs` structure.

   B. **reindex_queue_depth access:** Add `pub fn pending_count(&self) -> usize` method to
      FileWatcher. Pass Arc<FileWatcher> to health handler via DaemonServer struct field.

   C. **Daemon start time:** Add `start_time: std::time::Instant` field to DaemonServer,
      initialized in DaemonServer::new(). Convert to Unix timestamp for stale_count SQL query.
   ```
2. Update `devforgeai/specs/context/source-tree.md` to include `src/cli/commands/daemon.rs` if it's a new file

**Verification:** Read STORY-016 and confirm all three gaps have prescribed solutions.

**Session Handoff Context:** Check if `src/cli/commands/daemon.rs` exists. If STORY-012 (daemon-index integration, now complete) created it, Gap A is already resolved. Run `ls src/cli/commands/` to verify.

---

### MEDIUM Findings (Documentation Gaps / Stale Labels)

---

#### F-009: Path Case Sensitivity in Research Citations

**Severity:** MEDIUM
**Affected Files:**
- `devforgeai/specs/brainstorms/BRAINSTORM-001-treelint-ast-code-search.brainstorm.md` (line 21)
- `devforgeai/specs/brainstorms/BRAINSTORM-002-indexing-efficiency-language-expansion.brainstorm.md`
- `devforgeai/specs/requirements/treelint-requirements.md` (line 441)
- `devforgeai/specs/requirements/treelint-post-mvp-requirements.md`

**Evidence:**
Citations use lowercase path: `devforgeai/specs/research/RESEARCH-001-...`
Actual directory on disk: `devforgeai/specs/Research/` (capital R)

**Impact:** On case-sensitive filesystems (Linux, WSL), automated citation validators would fail to resolve these paths. On Windows/macOS, no functional impact.

**Remediation:**
Replace `devforgeai/specs/research/` with `devforgeai/specs/Research/` in all citation paths across all 4 affected files. Use case-sensitive search-and-replace.

**Verification:** `grep -r "specs/research/" devforgeai/specs/` returns no matches (all should be `specs/Research/`).

---

#### F-010: EPIC-002 Sprint Summary Table Shows "TBD"

**Severity:** MEDIUM
**Affected File:** `devforgeai/specs/Epics/EPIC-002-advanced-features.epic.md` (lines 488-495)

**Evidence:**
> Line 488: `| SPRINT-002 | Not Started | 29 | TBD | 0 | 0 | 0 |`
> Line 495: `- **Velocity:** TBD`

All 6 stories (STORY-007 through STORY-012) are created and listed in the epic's "Created Stories" section above this table.

**Remediation:**
Update the sprint summary table to reflect actual story count (6 stories, all created). Update velocity after sprint completion.

**Verification:** The TBD values in lines 488-489 are replaced with actual data.

---

#### F-011: Stale Dependency Status Labels in STORY-014 and STORY-015

**Severity:** MEDIUM
**Affected Files:**
- `devforgeai/specs/Stories/STORY-014-startup-reconciliation-scan.story.md` (dependency section)
- `devforgeai/specs/Stories/STORY-015-file-watcher-hash-skip-optimization.story.md` (dependency section)

**Evidence:** Both stories list STORY-013's status as "Backlog" in their dependency tables, but STORY-013 is "Ready for Dev".

**Remediation:**
In both story files, update the STORY-013 dependency status from "Backlog" to "Ready for Dev".

**Verification:** `grep -A2 "STORY-013" devforgeai/specs/Stories/STORY-014*` shows "Ready for Dev".

---

#### F-012: STORY-030 Accepts depth 1-5 but Only Implements depth=1

**Severity:** MEDIUM
**Affected Story:** STORY-030
**Affected File:** `devforgeai/specs/Stories/STORY-030-daemon-ipc-dependency-query.story.md`

**Evidence:** AC#4 validates depth 1-5 as valid input. But the story only implements depth=1 behavior. Depth > 1 is deferred to STORY-033. A caller sending `depth=3` would receive depth=1 results with no indication the depth was clamped.

**Impact:** API consumers could receive silently truncated results between STORY-030 delivery and STORY-033 delivery.

**Remediation (choose one):**
- **Option A:** Add a response field `"actual_depth": 1` to indicate clamping, and a note in the response when depth was reduced
- **Option B:** Reject depth > 1 with error E005 until STORY-033 is implemented, then relax the validation
- **Option C (least disruptive):** Document the limitation in STORY-030's API notes and add a TODO comment in the handler code referencing STORY-033

**Verification:** The chosen approach is documented in STORY-030.

---

#### F-013: STORY-020 Constructor Name Extraction Requires Undocumented Context Tracking

**Severity:** MEDIUM
**Affected Story:** STORY-020
**Affected File:** `devforgeai/specs/Stories/STORY-020-csharp-method-property-extraction.story.md` (AC#2, line 76-78)

**Evidence:**
> AC#2: "Each constructor is extracted as a Symbol with symbol_type=Method, name matching the class name"

In tree-sitter, `constructor_declaration` nodes do not contain the parent class name. The extractor must track the enclosing class name during the AST walk (e.g., maintain a stack of parent type names). This is a non-trivial implementation detail that the story does not address.

**Remediation:**
Add to STORY-020 technical specification:
```
### Constructor Name Resolution
The `walk_csharp_node()` function must maintain a `parent_type_name: Option<String>` context
parameter (or a stack for nested types). When entering a class/struct/record declaration,
push the type name. When processing constructor_declaration, use the current parent type name
as the constructor's Symbol.name. This requires modifying walk_csharp_node()'s signature to
accept context, which is a refactoring of the STORY-019 implementation.
```

**Verification:** STORY-020 technical spec explicitly addresses how constructor name is resolved.

---

### LOW Findings (Known Tradeoffs, Properly Documented)

---

#### F-014: ADR-006 Maps C# Fields to Variable (Loses Distinction)

**Severity:** LOW (documented tradeoff)
**Source:** `devforgeai/specs/adrs/ADR-006-symboltype-enum-extension-strategy.md`
**Note:** Users cannot filter `--type field` separately from `--type variable`. Escape hatch documented: future ADR can add `Field` variant if needed.

**Action Required:** None. Informational for implementors of STORY-020.

---

#### F-015: ADR-004 Grammar Maturity Risk (tree-sitter-sql v0.0.2)

**Severity:** LOW (documented with fallback)
**Source:** `devforgeai/specs/adrs/ADR-004-tree-sitter-sql-grammar.md`
**Note:** Grammar may not cover all SQL constructs. Fallback to `tree-sitter-sequel` documented. Grammar validation gate recommended for STORY-024.

**Action Required:** None. Risk is acknowledged and has a mitigation path.

---

#### F-016: STORY-033 Shared Visited Set Produces Non-Obvious Bidirectional Results

**Severity:** LOW (documented tradeoff)
**Source:** `devforgeai/specs/Stories/STORY-033-bidirectional-transitive-traversal.story.md` (BR-003)
**Note:** In bidirectional queries, a symbol reachable from both directions appears in only one array (whichever direction found it first). Diamond graph topologies may produce incomplete `called_by` results.

**Action Required:** None. BR-003 documents this explicitly. Test strategy includes diamond graph edge case.

---

## 5. Cross-Cutting Issues

### Issue A: No Sprint Assigned for EPIC-004 (C#) and EPIC-005 (SQL) Stories

Stories STORY-018 through STORY-029 are all in "Backlog" status with no sprint assignment. EPIC-003 has SPRINT-002 and EPIC-006 has SPRINT-003, but EPIC-004 and EPIC-005 have no sprint files. This means 12 stories (57% of the audit scope) have no sprint-level planning, capacity validation, or execution order.

**Recommendation:** Create SPRINT-004 (or similar) for EPIC-004 and SPRINT-005 for EPIC-005 before beginning implementation. Use `/create-sprint` command.

### Issue B: EPIC-004/005 Stories Assigned to "Bryan" but Sprint Stories Assigned to "Claude"

EPIC-003 stories (013-017) are assigned to "Claude" in the sprint. EPIC-004 stories (018-023) are assigned to "Bryan". EPIC-006 stories (030-033) are in SPRINT-003 with no explicit assignee per story. This inconsistency should be resolved during sprint planning.

### Issue C: STORY-014 References `get_all_tracked_files()` Without Listing in DoD

STORY-014 assumes `IndexStorage::get_all_tracked_files()` exists for deleted file detection. This method is not listed in the story's DoD or technical specification as something to create. If it doesn't exist, the developer must add it, which is undocumented scope.

**Recommendation:** Verify if `get_all_tracked_files()` exists in `src/index/storage.rs`. If not, add it to STORY-014's DoD.

---

## 6. Summary Statistics

| Metric | Count |
|--------|-------|
| Stories audited | 21 (STORY-013 through STORY-033) |
| Epics covered | 4 (EPIC-003, 004, 005, 006) |
| Sprints covered | 2 (SPRINT-002, SPRINT-003) |
| Brainstorms traced | 2 (BRAINSTORM-001, 002) |
| Requirements docs traced | 2 (v1, v2 post-MVP) |
| ADRs validated | 6 (ADR-001 through ADR-006) |
| **Total findings** | **16** |
| CRITICAL | 2 |
| HIGH | 6 |
| MEDIUM | 5 |
| LOW | 3 |
| Cross-cutting issues | 3 |

---

## 7. Remediation Priority Order

For a future Claude session picking up this work, address findings in this order:

1. **F-001** (CRITICAL) — Create the missing ADR for XML parser crate. Blocks STORY-023.
2. **F-002** (CRITICAL) — Run tree-sitter-sql grammar introspection spike. Blocks STORY-026/027/028.
3. **F-007** (HIGH, quick fix) — Remove "or Constant" ambiguity from STORY-020. Two line changes.
4. **F-005** (HIGH, quick fix) — Fix RESEARCH-005 → RESEARCH-001 in BRAINSTORM-001. Three line changes.
5. **F-009** (MEDIUM, quick fix) — Fix path case sensitivity in research citations. Search-and-replace.
6. **F-011** (MEDIUM, quick fix) — Update stale dependency status labels. Two file changes.
7. **F-010** (MEDIUM, quick fix) — Update EPIC-002 sprint summary table.
8. **F-003** (HIGH) — Add STORY-032 as dependency to STORY-031. Update SPRINT-003 execution order.
9. **F-004** (HIGH) — Resolve ADR-006 variant addition strategy. Requires decision (Option A or B).
10. **F-008** (HIGH) — Add pre-implementation decisions to STORY-016. Three architectural micro-decisions.
11. **F-013** (MEDIUM) — Add constructor name resolution strategy to STORY-020.
12. **F-006** (HIGH) — Clarify STORY-029 additive principle to accommodate pre-processing.
13. **F-012** (MEDIUM) — Document STORY-030 depth limitation behavior.

Items 14-16 (F-014, F-015, F-016) are LOW/informational and require no action.

---

## 8. Session Handoff Instructions

**For future Claude sessions reading this document:**

1. **Start here.** This document is self-contained. You do not need the original audit conversation.
2. **Check current state.** Before remediating any finding, verify it still exists — prior sessions may have already fixed some items.
3. **Use the verification step** in each finding to confirm the fix was applied correctly.
4. **File paths are absolute from project root** (`/mnt/c/Projects/Treelint/` prefix for local, or relative `devforgeai/specs/...` within the project).
5. **For CRITICAL findings (F-001, F-002):** These block story implementation. Prioritize them.
6. **For quick fixes (F-005, F-007, F-009, F-010, F-011):** These can all be done in a single session with no architectural decisions needed.
7. **For architectural decisions (F-004, F-008):** Use `AskUserQuestion` to confirm the chosen approach before making changes.

---

*End of audit report.*
