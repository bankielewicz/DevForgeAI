# Structural inspection contract

Use [inspect_skill.py](../scripts/inspect_skill.py) during the deterministic phase to inspect the exact selected candidate. This helper produces structural evidence only. It does not load a skill into Codex, execute candidate code, evaluate prompts, establish provenance meaning, prove package installation, or produce a final validation verdict.

## Prerequisites and invocation

Use a trusted Python 3.11 or newer environment. Python's standard library supplies hashing, JSON, TOML, and Python syntax parsing. Genuine YAML parsing requires PyYAML, available in the approved evaluator environment. The helper does not install it. If PyYAML is absent, S004 and its dependent field checks return COULD_NOT_RUN while independent checks continue.

Resolve the script from the actually loaded validator package. Pass absolute paths; neither the current working directory nor the framework source checkout is an implied resource root.

~~~text
python3 /absolute/validator/scripts/inspect_skill.py \
  --skill-root /absolute/candidate/skill-name \
  --specification /absolute/accepted/skill-design-spec.md \
  --mode source \
  --output /absolute/run/structure-source.json
~~~

The command interface supports --help. --skill-root, --specification, and --output are required. --mode accepts source or installed and defaults to source. The output parent directory must already exist. Each invocation requires a fresh output filename outside the candidate tree and distinct from the specification. Existing files are never overwritten. A report is created exclusively only after inspection finishes; an I/O failure returns exit 2 and stderr. If an output write fails after creation, preserve the partial file as incomplete evidence and use a new filename.

The helper reads candidate files and the selected specification. It writes only the specified report, does not invoke subprocesses, does not use the network, and does not import or execute candidate Python. PyYAML is an evaluator dependency, not a candidate dependency to discover or install.

## Stable checks

Each report has exactly one aggregate result for each S001–S013 rule. A rule may contain multiple file findings; all distinct affected file locators are retained. PASS with no applicable optional files means the structural rule found no applicable defect; it does not prove those resources should be absent.

| ID | Deterministic assertion | FAIL means | COULD_NOT_RUN means |
| --- | --- | --- | --- |
| S001 | The supplied root is a directory available to the inspector. | Not used; an invalid target is an invocation/input problem. | Missing, invalid, or inaccessible target. |
| S002 | Enumerate the bounded package tree, read regular files, and hash the complete bytes of every read file. | Not used; concrete format defects have their own rules. | Unreadable or unstable files, incomplete enumeration, exceeded bounds, special files, directory symlinks, or resources that were intentionally not read. |
| S003 | A file named exactly SKILL.md is present and decodes as UTF-8; an optional UTF-8 BOM is accepted. | Missing SKILL.md, SKILL.md is a directory, or invalid UTF-8. | The file or required inventory cannot be read. |
| S004 | The first line and closing delimiter are exactly ---, and the enclosed YAML is a mapping parsed by PyYAML's SafeLoader with duplicate-key rejection. | Missing delimiters, invalid YAML, duplicate mapping keys, or a non-mapping root. | Missing PyYAML, unavailable SKILL.md, exceeded frontmatter bound, or parser resource failure. |
| S005 | Parsed name and description values are nonempty strings. Other frontmatter fields are permitted. | A required field is absent, empty/whitespace, or has another type. | Parsed frontmatter is unavailable. |
| S006 | The name has 1–64 characters, consists of lowercase ASCII letters/digits separated by single internal hyphens, and exactly equals the resolved skill folder name. | Invalid length/characters/hyphens or folder mismatch. | A parsed string name is unavailable. |
| S007 | Supported local Markdown destinations in SKILL.md and all inventoried references/**/*.md resolve to files or directories inside the candidate package. | An observed local target is missing, escapes the package, uses a file: URL, uses nonportable backslashes/NUL, or has another observed invalid destination. | Incomplete Markdown inventory, unreadable resolution, exceeded bounds, or a recognized representation outside the parser's supported subset. |
| S008 | Enumerated symlinks resolve and stay inside the package. | A broken/cyclic symlink or a resolved link that escapes the root. | An inaccessible symlink or incomplete inventory. |
| S009 | Top-level evals is excluded in installed mode. Source mode permits evals, including its absence. | A top-level evals entry is present in installed mode. | Inventory is incomplete. |
| S010 | All inventoried .json files parse with duplicate object keys and NaN/Infinity rejected. | Invalid UTF-8/JSON or a duplicate key/non-JSON number. | Incomplete inventory or a parser resource failure. |
| S011 | All inventoried .toml files parse with Python tomllib. | Invalid UTF-8 or invalid TOML. | Incomplete inventory or a parser resource failure. |
| S012 | All inventoried .py files parse with ast.parse, preserving declared Python source encoding and never executing code. | Invalid source encoding or Python syntax for the evaluator's Python version. | Incomplete inventory or a parser resource failure. |
| S013 | The exact selected specification bytes are readable and SHA-256 hashed. | Not used; specification meaning is reviewed separately. | Missing/unreadable specification, a non-file input, changed bytes during reading, or an exceeded bound. |

S006 follows the inclusive 64-character Agent Skills limit. A recommendation to keep names shorter is an authoring preference, not a reason to fail a conforming 64-character name. S005 is a field-presence/type check, not every provider-specific frontmatter rule. Optional metadata is preserved and is not rejected because its keys are unfamiliar.

The duplicate-key YAML policy also rejects collisions introduced by YAML merge mappings. Safe parsing does not establish the business meaning of a field, API compatibility, or trustworthiness of its content.

The source/installed switch does not certify all distribution exclusions. Python caches, output history, provenance sidecars, executable permission behavior, and the exact installer inclusion/exclusion rules remain separate contract and installed-resource observations. The helper cannot confirm that a source with no evals satisfies DevForgeAI's requirement for authored release-evaluation cases.

## Markdown scope

The parser examines SKILL.md after its frontmatter and Markdown files anywhere under references. It supports conventional fenced-code exclusion; inline links and images with ordinary or angle-bracket destinations; balanced destination parentheses up to depth 32; optional quoted/parenthesized titles; reference definitions and full, collapsed, or shortcut reference links. Backslash escapes are interpreted and URL percent escapes are decoded before resolving local paths. Reference documents resolve links relative to their containing directory; SKILL.md resolves links relative to the skill root.

External URL destinations are counted but are not fetched or checked. Empty and anchor-only destinations are counted separately and ignored. A local file destination containing a fragment is checked for file existence only; anchor correctness is not checked. Undefined bracket references remain plain text under this parser rather than fabricated missing files.

This helper is not a complete CommonMark/HTML renderer. Indented link syntax whose interpretation can depend on nested-list context, HTML resource attributes, entity-encoded destinations, unsupported link endings, and multiline/otherwise unparsed reference destinations cause COULD_NOT_RUN for S007. Those representations need an independent renderer or documented manual inspection in the validation record; do not edit this report into PASS. Other Markdown dialect features such as MDX, wiki links, embedded JavaScript, and raw textual paths are outside this check. Review those separately when the candidate uses them.

Markdown under assets and evals is not treated as executable instructions by this rule. Template placeholders are intentional content, so there is no blanket placeholder regex, word-count score, or marker-based prompt-quality assertion.

## Resource bounds and manifests

The implemented limits are:

- 4,096 filesystem entries, including directories and symlinks.
- Directory depth 32 below the candidate root.
- 16 MiB per file, including the selected specification.
- 128 MiB of total candidate file reads.
- 128 KiB of SKILL.md frontmatter.
- 2 MiB per Markdown document and 4,096 link-start markers per parsed document.
- 64 KiB streamed file-read chunks.

Exceeding a limit produces COULD_NOT_RUN, never a guessed PASS or a partial-file digest. Other independently observable defects may still be reported. A total-read limit can stop reading later files while recording each encountered uninspected file; an entry/depth limit prevents further enumeration and records that explicit coverage gap. The manifest contains only fully read regular-file bytes under slash-separated, package-relative keys.

Contained file symlinks are read under their package-relative names and hashed by target bytes. Escaping symlinks are reported without reading their targets. Contained directory symlinks are not recursively traversed, to avoid aliased and cyclic inventories; S002 records incomplete coverage. Special files are never intentionally consumed as regular resources. The report does not hash directory topology, symlink text, executable bits, or permissions.

Before/after file identity, size, and modification time are compared during reading. These checks can detect some concurrent changes; they are not an operating-system snapshot or a proof against adversarial races. The enclosing validation workflow must supply an immutable or otherwise isolated candidate and bind these file hashes to that preserved input. Input byte bounds are not a hard CPU/memory sandbox for third-party YAML or standard-library parsers; apply the evaluator's established process/resource boundary separately.

## Report and exit contract

The JSON object uses these fields:

~~~json
{
  "schema_version": "devforge.skill-structure/v1",
  "created_at_utc": "<actual UTC timestamp>",
  "skill_root": "<absolute resolved candidate path>",
  "mode": "source",
  "specification": {
    "path": "<absolute resolved specification path>",
    "sha256": "<exact-byte SHA-256, or null when unavailable>"
  },
  "files_sha256": {
    "SKILL.md": "<exact-byte SHA-256>"
  },
  "checks": [
    {
      "id": "S001",
      "outcome": "PASS",
      "reason": "<observations and limits>",
      "evidence": [
        {"path": "<absolute observed path>", "line": 1}
      ]
    }
  ],
  "overall": "PASS",
  "behavior": "NOT_EVALUATED"
}
~~~

The illustrated checks array is abbreviated; actual reports contain S001–S013. Evidence line is omitted when no reliable line is available. The timestamp comes from the actual system clock when the report is assembled. Null is used for an unavailable specification digest. Unread file digests are absent and the corresponding incomplete-coverage checks explain why.

Per-rule and overall precedence is FAIL, then COULD_NOT_RUN, then PASS. Thus an observed failure and an unrelated incomplete check can coexist; consumers must inspect every rule, not assume overall FAIL means every check completed.

| Exit | Meaning |
| --- | --- |
| 0 | All structural checks completed with PASS, including vacuous optional-file checks. |
| 1 | At least one observed structural conformance defect. Other checks may still be incomplete. |
| 2 | No observed FAIL but a required structural observation could not be obtained; or invalid invocation, unsupported runtime, unexpected inspection error, or report I/O failure. |

Argument parsing and unexpected failures may produce stderr without a complete report. A missing, truncated, or invalid report is COULD_NOT_RUN to the enclosing workflow. Never substitute process exit success, a filename, or an empty report for the required fields and complete rule set.

Structural PASS does not establish behavior, AI review quality, acceptance authority, native activation, isolation, or successful fixes. The devforge-evaluate-expert combines these scoped observations with its other enforced phases and issues a separate evidence-based verdict. The devforge-project-expert-creator alone owns candidate repairs.

## Authoring status

This helper and its interface are authored source. During the builder's authoring-only creation of devforge-evaluate-expert, the helper was not executed, compiled, tested, or used to validate this skill. Its future validation must preserve that distinction until actual execution evidence exists.
