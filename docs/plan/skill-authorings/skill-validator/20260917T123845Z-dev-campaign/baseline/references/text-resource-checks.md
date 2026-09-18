# Text, resources, context and effects

Use `scripts/adaptive_observe.py package --source <captured-package>` for deterministic observations. Name the original package directory when retaining a snapshot; if the snapshot is named source, assess directory identity against its bound original separately.

### 3.2 Unicode, placeholders, and resource parsing

Scan complete captured UTF-8 text files; decoding failures in declared text are findings, not silently skipped content. Binary resources are inventoried and their call sites reviewed; do not interpret arbitrary binaries as UTF-8. Determine text by known text extensions and successful UTF-8 decode with no NUL; a declared resource's type overrides guessing. Record the classification. Excluded/oversize text is NOT_RUN, never a truncated PASS.

Unicode candidate set:

- C0 controls U+0000-U+001F except TAB, LF, CR; DEL U+007F; C1 U+0080-U+009F.
- Directional controls U+202A-U+202E and U+2066-U+2069; marks U+200E/U+200F and U+061C.
- U+200B-U+200D, U+2060, U+FEFF, U+00AD, U+034F, U+00A0, U+202F; variation selectors U+FE00-U+FE0F and U+E0100-U+E01EF; tag characters U+E0000-U+E007F.
- NFKC-changing characters in executable command names, metadata names/keys, resource locators, and exact protocol identifiers. Report the original and normalized form as a candidate; do not normalize source bytes or claim exhaustive Unicode confusable detection.

Each candidate record gives relative file, zero-based start/end byte offsets, one-based line/column in Unicode code points, `U+` code point, Unicode name, escaped excerpt of at most 160 code points, context type, and disposition. Boundary excerpts must not reveal suspected secrets. Legitimate joiners, variation selectors, RTL text, literal security fixtures, and nonbreaking typography are not defects without demonstrated ambiguity or behavior change. Unexpected control characters in commands/identifiers, visual masking of a different command/path, or metadata parsing failure are defects. A leading BOM is reported as a parser-compatibility observation, not silently stripped.

Placeholder candidates include `[TODO: ...]`, standalone `TODO`/`TBD` markers, and scaffold replacement markers. Quoted examples/fixtures documenting those tokens are not unfinished production instructions. Required content that is still an unresolved placeholder is FAIL; harmless explanatory use is dismissed with reason.

Resource graph nodes are captured files; edges contain source location, target, kind (`link`, `image`, `instruction`, `script_call`, `template_use`), and resolution (`resolved`, `missing`, `outside_scope`, `dynamic`, `unsupported_anchor`). Parse ordinary inline and reference-style Markdown links/images outside fenced code, ATX headings, Setext headings, and explicit HTML `id` anchors. For heading slugs use lowercase text, remove inline formatting punctuation, turn spaces into hyphens, and suffix duplicate slugs `-1`, `-2`; renderer-specific disagreement is manual/unresolved, not an automatic universal format failure. Do not resolve remote links by network requests in core checks.

Inspect command/path mentions and template consumers manually; do not execute or import arbitrary scripts to discover references. Descriptor `resource_roles` seed role analysis, not reachability. Roots are SKILL.md and optional host metadata; runtime helper and adaptive descriptor are reachable only through actual instructions/configuration. A declared fixture/license can be intentionally unlinked at runtime. Files with no known consumer remain `unresolved_usage` until manual examination; emit an orphan finding only when removal would discard no required resource and its unused status is supported. Do not delete files during assessment.

### 3.3 Semantic anti-slop rubric

Preserve the existing ceremonial finding classes: `useful_instruction`, `redundant_wording`, `ambiguous_requirement`, `unbounded_ritual`, `unenforced_control_claim`. Add precise reason text, not another aggregate slop score. Retain exact bounded excerpts, intended effect, contextual evidence, user impact, proposed disposition, and the substantive requirement that must survive a revision.

Review questions are concrete:

1. Does the passage change a decision/action, identify necessary context, or supply a usable output criterion? If none, identify the redundant or hollow passage and why it can be removed without losing a requirement.
2. Can a reader determine the inputs and observable completion? "Ensure enterprise-grade excellence" alone is ambiguous; a stated error response and test oracle are observable.
3. Do repeated instructions add necessary timing/context or contradict another branch? Repetition is not automatically defective.
4. Is routing content available before selection/action? A trigger hidden only in a reference is insufficient for description-based routing; a conditional sub-step may properly live there.
5. Does a command or external mechanism actually enforce the claimed invariant? "Mark PASS to unlock the phase" has no authority absent an implemented mechanism. A user review boundary still governs the agent's authorized workflow.

No keyword blacklist, capitalized MUST count, mandatory verbosity score, persona ban, heading count, or claim that models universally ignore a style is permitted. A proposed rewrite must retain necessary safeguards. The same phrase may be useful in one context and hollow in another; acceptance fixtures must cover both.

### 3.4 Context and security observations

Count raw bytes, Unicode code points and physical lines per file. Lines are `len(text.splitlines())`, zero for empty text. For token counts use an already installed tokenizer with an explicitly named encoding; record package/version, encoding, and per-file counts. No automatic dependency installation or guessed chars-per-token conversion. If unavailable, token counts are null with NOT_RUN reason while byte/character coverage can pass.

Report entrypoint and discovery metadata separately. A static branch estimate is the sum of identified loaded file counts, labeled estimated; actual CLI-observed loads are separate. Repeated-load cost counts each observed occurrence; unique-content cost counts each file once. Do not call a full-file estimate actual token consumption when the host read only an excerpt. Tool-output tokens and truncation behavior may be unknown. User-supplied budgets must identify unit and scope; an unmeasurable required token budget is INCOMPLETE, not an invented pass.

Security review covers selected skill scripts/instructions and explicit dependencies necessary to understand their effects. Identify network operations, credential reads, shell interpolation, executable deserialization, dynamic execution, traversal, destructive writes, and instructions pretending to override host controls. Inspect source-to-effect context; a string such as `eval` in a fixture is not a vulnerability verdict. Known private-key headers and secret-shaped literals are candidates; retain redacted locations and synthetic counterexamples, never real secret values. Absence of a pattern does not prove absence of vulnerabilities. Do not run exploit fixtures against the real project, access real credentials, or initiate live external calls.


## Finalizing observations

Retain helper stdout unchanged with its helper-local check identity. Put semantic dispositions, reasons and evidence in a separate adaptive-observations-v1 record. Package parser nodes remain unresolved_usage until actual consumers are reviewed. Unicode excerpts intentionally show only the escaped candidate character, avoiding adjacent secrets; inspect the retained byte/line location under the authorized secret-safe boundary. Scan results are not security certification.

Inspect malformed tables, ambiguous destinations, script calls, instruction path mentions and template uses manually. Add located edges of the declared kinds to the finalized graph; dynamic/unsupported renderer behavior remains unresolved. Read schemas and examples as data, never import a target to discover its runtime behavior. Binary resources are inventoried with classification and reviewed at call sites; declared binary/text type overrides guessing during finalized review.

The optional metadata reader checks the supported Claude Code frontmatter shapes and value domains. Unknown extension fields remain applicability questions; do not strip them or require optional fields. Pin [Claude Code frontmatter guidance](../assets/claude-frontmatter-guidance.md) when field applicability is relevant, and record source freshness. Claude Code reads no separate configuration file, so there is no second metadata document to check.

For a selected required token budget, null tokens imply NOT_RUN and incomplete budget verification. No budget is inferred. Named tiktoken encoding data must already be local; no downloads, arbitrary module imports or character-to-token conversions. Retain exact excerpt evidence for observed excerpts; do not charge a full-file estimate as actual host consumption. The record checker verifies arithmetic but cannot reconstruct missing host load events.
