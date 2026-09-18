# Exact command log

Arguments are serialized arrays; no shell reconstruction is needed. Each commands/<id>/ directory retains the original command/oracle, stdin when present, stdout, stderr and result. Tool-based bootstrap source reads and approvals remain in the conversation; they were not all independently transcribed before execution, as disclosed in E-01.

## author-adopt-begin

```json
{
  "case": "author-adopt-begin",
  "argv": [
    "C:\\Program Files\\Python310\\python.exe",
    "-B",
    "-X",
    "utf8",
    "C:\\Projects\\DevForgeAI\\src\\agents\\skills\\skill-builder\\scripts\\authoring.py",
    "begin",
    "--contract",
    "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z\\fixtures\\independent-01\\author-adopt\\input-contract.json",
    "--run-root",
    "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z\\fixtures\\independent-01\\author-adopt\\docs\\plan\\run"
  ],
  "cwd": "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z",
  "timeout_seconds": 120,
  "permitted_write_root": "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z",
  "expected": {
    "exit": 0,
    "field": "state",
    "value": "STAGED",
    "read_only_root": null,
    "before_manifest": null
  },
  "start_utc": "2026-09-13T15:51:11.576314+00:00",
  "stdin_sha256": null
}
```

Exit: 0; timeout: False. Raw output: `commands/author-adopt-begin/stdout.txt`, `stderr.txt`.

## author-adopt-publish

```json
{
  "case": "author-adopt-publish",
  "argv": [
    "C:\\Program Files\\Python310\\python.exe",
    "-B",
    "-X",
    "utf8",
    "C:\\Projects\\DevForgeAI\\src\\agents\\skills\\skill-builder\\scripts\\authoring.py",
    "publish",
    "--run-root",
    "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z\\fixtures\\independent-01\\author-adopt\\docs\\plan\\run"
  ],
  "cwd": "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z",
  "timeout_seconds": 120,
  "permitted_write_root": "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z",
  "expected": {
    "exit": 0,
    "field": "state",
    "value": "AUTHORED",
    "read_only_root": null,
    "before_manifest": null
  },
  "start_utc": "2026-09-13T15:51:11.735935+00:00",
  "stdin_sha256": null
}
```

Exit: 0; timeout: False. Raw output: `commands/author-adopt-publish/stdout.txt`, `stderr.txt`.

## author-corrupt-history

```json
{
  "case": "author-corrupt-history",
  "argv": [
    "C:\\Program Files\\Python310\\python.exe",
    "-B",
    "-X",
    "utf8",
    "C:\\Projects\\DevForgeAI\\src\\agents\\skills\\skill-builder\\scripts\\authoring.py",
    "begin",
    "--contract",
    "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z\\fixtures\\independent-01\\author-corrupt\\input-contract.json",
    "--run-root",
    "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z\\fixtures\\independent-01\\author-corrupt\\docs\\plan\\run"
  ],
  "cwd": "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z",
  "timeout_seconds": 120,
  "permitted_write_root": "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z",
  "expected": {
    "exit": 2,
    "field": null,
    "value": null,
    "read_only_root": null,
    "before_manifest": null
  },
  "start_utc": "2026-09-13T15:51:12.143495+00:00",
  "stdin_sha256": null
}
```

Exit: 2; timeout: False. Raw output: `commands/author-corrupt-history/stdout.txt`, `stderr.txt`.

## author-create-begin

```json
{
  "case": "author-create-begin",
  "argv": [
    "C:\\Program Files\\Python310\\python.exe",
    "-B",
    "-X",
    "utf8",
    "C:\\Projects\\DevForgeAI\\src\\agents\\skills\\skill-builder\\scripts\\authoring.py",
    "begin",
    "--contract",
    "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z\\fixtures\\independent-01\\authoring\\input-contract.json",
    "--run-root",
    "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z\\fixtures\\independent-01\\authoring\\docs\\plan\\run"
  ],
  "cwd": "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z",
  "timeout_seconds": 120,
  "permitted_write_root": "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z",
  "expected": {
    "exit": 0,
    "field": "state",
    "value": "STAGED",
    "read_only_root": null,
    "before_manifest": null
  },
  "start_utc": "2026-09-13T15:51:09.599676+00:00",
  "stdin_sha256": null
}
```

Exit: 0; timeout: False. Raw output: `commands/author-create-begin/stdout.txt`, `stderr.txt`.

## author-create-publish

```json
{
  "case": "author-create-publish",
  "argv": [
    "C:\\Program Files\\Python310\\python.exe",
    "-B",
    "-X",
    "utf8",
    "C:\\Projects\\DevForgeAI\\src\\agents\\skills\\skill-builder\\scripts\\authoring.py",
    "publish",
    "--run-root",
    "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z\\fixtures\\independent-01\\authoring\\docs\\plan\\run"
  ],
  "cwd": "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z",
  "timeout_seconds": 120,
  "permitted_write_root": "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z",
  "expected": {
    "exit": 0,
    "field": "state",
    "value": "AUTHORED",
    "read_only_root": null,
    "before_manifest": null
  },
  "start_utc": "2026-09-13T15:51:09.708685+00:00",
  "stdin_sha256": null
}
```

Exit: 0; timeout: False. Raw output: `commands/author-create-publish/stdout.txt`, `stderr.txt`.

## author-drift-begin

```json
{
  "case": "author-drift-begin",
  "argv": [
    "C:\\Program Files\\Python310\\python.exe",
    "-B",
    "-X",
    "utf8",
    "C:\\Projects\\DevForgeAI\\src\\agents\\skills\\skill-builder\\scripts\\authoring.py",
    "begin",
    "--contract",
    "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z\\fixtures\\independent-01\\author-drift\\input-contract.json",
    "--run-root",
    "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z\\fixtures\\independent-01\\author-drift\\docs\\plan\\run"
  ],
  "cwd": "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z",
  "timeout_seconds": 120,
  "permitted_write_root": "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z",
  "expected": {
    "exit": 0,
    "field": "state",
    "value": "STAGED",
    "read_only_root": null,
    "before_manifest": null
  },
  "start_utc": "2026-09-13T15:51:12.232499+00:00",
  "stdin_sha256": null
}
```

Exit: 0; timeout: False. Raw output: `commands/author-drift-begin/stdout.txt`, `stderr.txt`.

## author-drift-publish

```json
{
  "case": "author-drift-publish",
  "argv": [
    "C:\\Program Files\\Python310\\python.exe",
    "-B",
    "-X",
    "utf8",
    "C:\\Projects\\DevForgeAI\\src\\agents\\skills\\skill-builder\\scripts\\authoring.py",
    "publish",
    "--run-root",
    "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z\\fixtures\\independent-01\\author-drift\\docs\\plan\\run"
  ],
  "cwd": "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z",
  "timeout_seconds": 120,
  "permitted_write_root": "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z",
  "expected": {
    "exit": 1,
    "field": "state",
    "value": "BLOCKED",
    "read_only_root": null,
    "before_manifest": null
  },
  "start_utc": "2026-09-13T15:51:12.413689+00:00",
  "stdin_sha256": null
}
```

Exit: 1; timeout: False. Raw output: `commands/author-drift-publish/stdout.txt`, `stderr.txt`.

## author-edit-begin

```json
{
  "case": "author-edit-begin",
  "argv": [
    "C:\\Program Files\\Python310\\python.exe",
    "-B",
    "-X",
    "utf8",
    "C:\\Projects\\DevForgeAI\\src\\agents\\skills\\skill-builder\\scripts\\authoring.py",
    "begin",
    "--contract",
    "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z\\fixtures\\independent-01\\authoring\\edit\\input-contract.json",
    "--run-root",
    "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z\\fixtures\\independent-01\\authoring\\edit\\docs\\plan\\run"
  ],
  "cwd": "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z",
  "timeout_seconds": 120,
  "permitted_write_root": "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z",
  "expected": {
    "exit": 0,
    "field": "state",
    "value": "STAGED",
    "read_only_root": null,
    "before_manifest": null
  },
  "start_utc": "2026-09-13T15:51:10.044940+00:00",
  "stdin_sha256": null
}
```

Exit: 2; timeout: False. Raw output: `commands/author-edit-begin/stdout.txt`, `stderr.txt`.

## author-edit-publish

```json
{
  "case": "author-edit-publish",
  "argv": [
    "C:\\Program Files\\Python310\\python.exe",
    "-B",
    "-X",
    "utf8",
    "C:\\Projects\\DevForgeAI\\src\\agents\\skills\\skill-builder\\scripts\\authoring.py",
    "publish",
    "--run-root",
    "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z\\fixtures\\independent-01\\authoring\\edit\\docs\\plan\\run"
  ],
  "cwd": "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z",
  "timeout_seconds": 120,
  "permitted_write_root": "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z",
  "expected": {
    "exit": 0,
    "field": "state",
    "value": "AUTHORED",
    "read_only_root": null,
    "before_manifest": null
  },
  "start_utc": "2026-09-13T15:51:10.137443+00:00",
  "stdin_sha256": null
}
```

Exit: 2; timeout: False. Raw output: `commands/author-edit-publish/stdout.txt`, `stderr.txt`.

## author-extra-contract-field

```json
{
  "case": "author-extra-contract-field",
  "argv": [
    "C:\\Program Files\\Python310\\python.exe",
    "-B",
    "-X",
    "utf8",
    "C:\\Projects\\DevForgeAI\\src\\agents\\skills\\skill-builder\\scripts\\authoring.py",
    "begin",
    "--contract",
    "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z\\fixtures\\independent-01\\author-extra-field\\input-contract.json",
    "--run-root",
    "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z\\fixtures\\independent-01\\author-extra-field\\docs\\plan\\run"
  ],
  "cwd": "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z",
  "timeout_seconds": 120,
  "permitted_write_root": "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z",
  "expected": {
    "exit": 2,
    "field": null,
    "value": null,
    "read_only_root": null,
    "before_manifest": null
  },
  "start_utc": "2026-09-13T15:51:13.021288+00:00",
  "stdin_sha256": null
}
```

Exit: 0; timeout: False. Raw output: `commands/author-extra-contract-field/stdout.txt`, `stderr.txt`.

## author-import-begin

```json
{
  "case": "author-import-begin",
  "argv": [
    "C:\\Program Files\\Python310\\python.exe",
    "-B",
    "-X",
    "utf8",
    "C:\\Projects\\DevForgeAI\\src\\agents\\skills\\skill-builder\\scripts\\authoring.py",
    "begin",
    "--contract",
    "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z\\fixtures\\independent-01\\author-import\\input-contract.json",
    "--run-root",
    "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z\\fixtures\\independent-01\\author-import\\docs\\plan\\run"
  ],
  "cwd": "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z",
  "timeout_seconds": 120,
  "permitted_write_root": "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z",
  "expected": {
    "exit": 0,
    "field": "state",
    "value": "STAGED",
    "read_only_root": null,
    "before_manifest": null
  },
  "start_utc": "2026-09-13T15:51:10.800038+00:00",
  "stdin_sha256": null
}
```

Exit: 0; timeout: False. Raw output: `commands/author-import-begin/stdout.txt`, `stderr.txt`.

## author-import-publish

```json
{
  "case": "author-import-publish",
  "argv": [
    "C:\\Program Files\\Python310\\python.exe",
    "-B",
    "-X",
    "utf8",
    "C:\\Projects\\DevForgeAI\\src\\agents\\skills\\skill-builder\\scripts\\authoring.py",
    "publish",
    "--run-root",
    "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z\\fixtures\\independent-01\\author-import\\docs\\plan\\run"
  ],
  "cwd": "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z",
  "timeout_seconds": 120,
  "permitted_write_root": "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z",
  "expected": {
    "exit": 0,
    "field": "state",
    "value": "AUTHORED",
    "read_only_root": null,
    "before_manifest": null
  },
  "start_utc": "2026-09-13T15:51:10.903097+00:00",
  "stdin_sha256": null
}
```

Exit: 0; timeout: False. Raw output: `commands/author-import-publish/stdout.txt`, `stderr.txt`.

## author-observed-begin

```json
{
  "case": "author-observed-begin",
  "argv": [
    "C:\\Program Files\\Python310\\python.exe",
    "-B",
    "-X",
    "utf8",
    "C:\\Projects\\DevForgeAI\\src\\agents\\skills\\skill-builder\\scripts\\authoring.py",
    "begin",
    "--contract",
    "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z\\fixtures\\independent-01\\author-observed\\input-contract.json",
    "--run-root",
    "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z\\fixtures\\independent-01\\author-observed\\docs\\plan\\run"
  ],
  "cwd": "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z",
  "timeout_seconds": 120,
  "permitted_write_root": "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z",
  "expected": {
    "exit": 0,
    "field": "state",
    "value": "STAGED",
    "read_only_root": null,
    "before_manifest": null
  },
  "start_utc": "2026-09-13T15:51:10.218681+00:00",
  "stdin_sha256": null
}
```

Exit: 0; timeout: False. Raw output: `commands/author-observed-begin/stdout.txt`, `stderr.txt`.

## author-observed-publish

```json
{
  "case": "author-observed-publish",
  "argv": [
    "C:\\Program Files\\Python310\\python.exe",
    "-B",
    "-X",
    "utf8",
    "C:\\Projects\\DevForgeAI\\src\\agents\\skills\\skill-builder\\scripts\\authoring.py",
    "publish",
    "--run-root",
    "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z\\fixtures\\independent-01\\author-observed\\docs\\plan\\run"
  ],
  "cwd": "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z",
  "timeout_seconds": 120,
  "permitted_write_root": "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z",
  "expected": {
    "exit": 0,
    "field": "state",
    "value": "AUTHORED",
    "read_only_root": null,
    "before_manifest": null
  },
  "start_utc": "2026-09-13T15:51:10.399682+00:00",
  "stdin_sha256": null
}
```

Exit: 0; timeout: False. Raw output: `commands/author-observed-publish/stdout.txt`, `stderr.txt`.

## author-outside-scope-begin

```json
{
  "case": "author-outside-scope-begin",
  "argv": [
    "C:\\Program Files\\Python310\\python.exe",
    "-B",
    "-X",
    "utf8",
    "C:\\Projects\\DevForgeAI\\src\\agents\\skills\\skill-builder\\scripts\\authoring.py",
    "begin",
    "--contract",
    "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z\\fixtures\\independent-01\\author-outside-scope\\input-contract.json",
    "--run-root",
    "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z\\fixtures\\independent-01\\author-outside-scope\\docs\\plan\\run"
  ],
  "cwd": "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z",
  "timeout_seconds": 120,
  "permitted_write_root": "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z",
  "expected": {
    "exit": 0,
    "field": "state",
    "value": "STAGED",
    "read_only_root": null,
    "before_manifest": null
  },
  "start_utc": "2026-09-13T15:51:12.633148+00:00",
  "stdin_sha256": null
}
```

Exit: 0; timeout: False. Raw output: `commands/author-outside-scope-begin/stdout.txt`, `stderr.txt`.

## author-outside-scope-publish

```json
{
  "case": "author-outside-scope-publish",
  "argv": [
    "C:\\Program Files\\Python310\\python.exe",
    "-B",
    "-X",
    "utf8",
    "C:\\Projects\\DevForgeAI\\src\\agents\\skills\\skill-builder\\scripts\\authoring.py",
    "publish",
    "--run-root",
    "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z\\fixtures\\independent-01\\author-outside-scope\\docs\\plan\\run"
  ],
  "cwd": "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z",
  "timeout_seconds": 120,
  "permitted_write_root": "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z",
  "expected": {
    "exit": 1,
    "field": "state",
    "value": "BLOCKED",
    "read_only_root": null,
    "before_manifest": null
  },
  "start_utc": "2026-09-13T15:51:12.807578+00:00",
  "stdin_sha256": null
}
```

Exit: 1; timeout: False. Raw output: `commands/author-outside-scope-publish/stdout.txt`, `stderr.txt`.

## author-spec_build-begin

```json
{
  "case": "author-spec_build-begin",
  "argv": [
    "C:\\Program Files\\Python310\\python.exe",
    "-B",
    "-X",
    "utf8",
    "C:\\Projects\\DevForgeAI\\src\\agents\\skills\\skill-builder\\scripts\\authoring.py",
    "begin",
    "--contract",
    "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z\\fixtures\\independent-01\\author-spec_build\\input-contract.json",
    "--run-root",
    "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z\\fixtures\\independent-01\\author-spec_build\\docs\\plan\\run"
  ],
  "cwd": "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z",
  "timeout_seconds": 120,
  "permitted_write_root": "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z",
  "expected": {
    "exit": 0,
    "field": "state",
    "value": "STAGED",
    "read_only_root": null,
    "before_manifest": null
  },
  "start_utc": "2026-09-13T15:51:11.199103+00:00",
  "stdin_sha256": null
}
```

Exit: 0; timeout: False. Raw output: `commands/author-spec_build-begin/stdout.txt`, `stderr.txt`.

## author-spec_build-publish

```json
{
  "case": "author-spec_build-publish",
  "argv": [
    "C:\\Program Files\\Python310\\python.exe",
    "-B",
    "-X",
    "utf8",
    "C:\\Projects\\DevForgeAI\\src\\agents\\skills\\skill-builder\\scripts\\authoring.py",
    "publish",
    "--run-root",
    "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z\\fixtures\\independent-01\\author-spec_build\\docs\\plan\\run"
  ],
  "cwd": "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z",
  "timeout_seconds": 120,
  "permitted_write_root": "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z",
  "expected": {
    "exit": 0,
    "field": "state",
    "value": "AUTHORED",
    "read_only_root": null,
    "before_manifest": null
  },
  "start_utc": "2026-09-13T15:51:11.303107+00:00",
  "stdin_sha256": null
}
```

Exit: 0; timeout: False. Raw output: `commands/author-spec_build-publish/stdout.txt`, `stderr.txt`.

## bcn-divergent-begin

```json
{
  "case": "bcn-divergent-begin",
  "argv": [
    "C:\\Program Files\\Python310\\python.exe",
    "-B",
    "-X",
    "utf8",
    "C:\\Projects\\DevForgeAI\\src\\agents\\skills\\skill-builder\\scripts\\authoring.py",
    "begin",
    "--contract",
    "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z\\fixtures\\independent-01\\bcn-divergent\\second\\input-contract.json",
    "--run-root",
    "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z\\fixtures\\independent-01\\bcn-divergent\\second\\docs\\plan\\run"
  ],
  "cwd": "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z",
  "timeout_seconds": 120,
  "permitted_write_root": "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z",
  "expected": {
    "exit": 0,
    "field": "state",
    "value": "STAGED",
    "read_only_root": null,
    "before_manifest": null
  },
  "start_utc": "2026-09-13T15:51:15.297303+00:00",
  "stdin_sha256": null
}
```

Exit: 2; timeout: False. Raw output: `commands/bcn-divergent-begin/stdout.txt`, `stderr.txt`.

## bcn-divergent-publish

```json
{
  "case": "bcn-divergent-publish",
  "argv": [
    "C:\\Program Files\\Python310\\python.exe",
    "-B",
    "-X",
    "utf8",
    "C:\\Projects\\DevForgeAI\\src\\agents\\skills\\skill-builder\\scripts\\authoring.py",
    "publish",
    "--run-root",
    "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z\\fixtures\\independent-01\\bcn-divergent\\second\\docs\\plan\\run"
  ],
  "cwd": "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z",
  "timeout_seconds": 120,
  "permitted_write_root": "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z",
  "expected": {
    "exit": 1,
    "field": "state",
    "value": "BLOCKED",
    "read_only_root": null,
    "before_manifest": null
  },
  "start_utc": "2026-09-13T15:51:15.388303+00:00",
  "stdin_sha256": null
}
```

Exit: 2; timeout: False. Raw output: `commands/bcn-divergent-publish/stdout.txt`, `stderr.txt`.

## bcn-divergent-seed-begin

```json
{
  "case": "bcn-divergent-seed-begin",
  "argv": [
    "C:\\Program Files\\Python310\\python.exe",
    "-B",
    "-X",
    "utf8",
    "C:\\Projects\\DevForgeAI\\src\\agents\\skills\\skill-builder\\scripts\\authoring.py",
    "begin",
    "--contract",
    "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z\\fixtures\\independent-01\\bcn-divergent\\input-contract.json",
    "--run-root",
    "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z\\fixtures\\independent-01\\bcn-divergent\\docs\\plan\\run"
  ],
  "cwd": "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z",
  "timeout_seconds": 120,
  "permitted_write_root": "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z",
  "expected": {
    "exit": 0,
    "field": "state",
    "value": "STAGED",
    "read_only_root": null,
    "before_manifest": null
  },
  "start_utc": "2026-09-13T15:51:14.885204+00:00",
  "stdin_sha256": null
}
```

Exit: 0; timeout: False. Raw output: `commands/bcn-divergent-seed-begin/stdout.txt`, `stderr.txt`.

## bcn-divergent-seed-publish

```json
{
  "case": "bcn-divergent-seed-publish",
  "argv": [
    "C:\\Program Files\\Python310\\python.exe",
    "-B",
    "-X",
    "utf8",
    "C:\\Projects\\DevForgeAI\\src\\agents\\skills\\skill-builder\\scripts\\authoring.py",
    "publish",
    "--run-root",
    "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z\\fixtures\\independent-01\\bcn-divergent\\docs\\plan\\run"
  ],
  "cwd": "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z",
  "timeout_seconds": 120,
  "permitted_write_root": "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z",
  "expected": {
    "exit": 0,
    "field": "state",
    "value": "AUTHORED",
    "read_only_root": null,
    "before_manifest": null
  },
  "start_utc": "2026-09-13T15:51:14.991203+00:00",
  "stdin_sha256": null
}
```

Exit: 0; timeout: False. Raw output: `commands/bcn-divergent-seed-publish/stdout.txt`, `stderr.txt`.

## bcn-equal-base-begin

```json
{
  "case": "bcn-equal-base-begin",
  "argv": [
    "C:\\Program Files\\Python310\\python.exe",
    "-B",
    "-X",
    "utf8",
    "C:\\Projects\\DevForgeAI\\src\\agents\\skills\\skill-builder\\scripts\\authoring.py",
    "begin",
    "--contract",
    "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z\\fixtures\\independent-01\\bcn-equal-base\\second\\input-contract.json",
    "--run-root",
    "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z\\fixtures\\independent-01\\bcn-equal-base\\second\\docs\\plan\\run"
  ],
  "cwd": "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z",
  "timeout_seconds": 120,
  "permitted_write_root": "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z",
  "expected": {
    "exit": 0,
    "field": "state",
    "value": "STAGED",
    "read_only_root": null,
    "before_manifest": null
  },
  "start_utc": "2026-09-13T15:51:13.557438+00:00",
  "stdin_sha256": null
}
```

Exit: 2; timeout: False. Raw output: `commands/bcn-equal-base-begin/stdout.txt`, `stderr.txt`.

## bcn-equal-base-publish

```json
{
  "case": "bcn-equal-base-publish",
  "argv": [
    "C:\\Program Files\\Python310\\python.exe",
    "-B",
    "-X",
    "utf8",
    "C:\\Projects\\DevForgeAI\\src\\agents\\skills\\skill-builder\\scripts\\authoring.py",
    "publish",
    "--run-root",
    "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z\\fixtures\\independent-01\\bcn-equal-base\\second\\docs\\plan\\run"
  ],
  "cwd": "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z",
  "timeout_seconds": 120,
  "permitted_write_root": "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z",
  "expected": {
    "exit": 0,
    "field": "state",
    "value": "AUTHORED",
    "read_only_root": null,
    "before_manifest": null
  },
  "start_utc": "2026-09-13T15:51:13.655528+00:00",
  "stdin_sha256": null
}
```

Exit: 2; timeout: False. Raw output: `commands/bcn-equal-base-publish/stdout.txt`, `stderr.txt`.

## bcn-equal-base-seed-begin

```json
{
  "case": "bcn-equal-base-seed-begin",
  "argv": [
    "C:\\Program Files\\Python310\\python.exe",
    "-B",
    "-X",
    "utf8",
    "C:\\Projects\\DevForgeAI\\src\\agents\\skills\\skill-builder\\scripts\\authoring.py",
    "begin",
    "--contract",
    "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z\\fixtures\\independent-01\\bcn-equal-base\\input-contract.json",
    "--run-root",
    "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z\\fixtures\\independent-01\\bcn-equal-base\\docs\\plan\\run"
  ],
  "cwd": "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z",
  "timeout_seconds": 120,
  "permitted_write_root": "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z",
  "expected": {
    "exit": 0,
    "field": "state",
    "value": "STAGED",
    "read_only_root": null,
    "before_manifest": null
  },
  "start_utc": "2026-09-13T15:51:13.121797+00:00",
  "stdin_sha256": null
}
```

Exit: 0; timeout: False. Raw output: `commands/bcn-equal-base-seed-begin/stdout.txt`, `stderr.txt`.

## bcn-equal-base-seed-publish

```json
{
  "case": "bcn-equal-base-seed-publish",
  "argv": [
    "C:\\Program Files\\Python310\\python.exe",
    "-B",
    "-X",
    "utf8",
    "C:\\Projects\\DevForgeAI\\src\\agents\\skills\\skill-builder\\scripts\\authoring.py",
    "publish",
    "--run-root",
    "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z\\fixtures\\independent-01\\bcn-equal-base\\docs\\plan\\run"
  ],
  "cwd": "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z",
  "timeout_seconds": 120,
  "permitted_write_root": "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z",
  "expected": {
    "exit": 0,
    "field": "state",
    "value": "AUTHORED",
    "read_only_root": null,
    "before_manifest": null
  },
  "start_utc": "2026-09-13T15:51:13.223424+00:00",
  "stdin_sha256": null
}
```

Exit: 0; timeout: False. Raw output: `commands/bcn-equal-base-seed-publish/stdout.txt`, `stderr.txt`.

## bcn-equal-new-begin

```json
{
  "case": "bcn-equal-new-begin",
  "argv": [
    "C:\\Program Files\\Python310\\python.exe",
    "-B",
    "-X",
    "utf8",
    "C:\\Projects\\DevForgeAI\\src\\agents\\skills\\skill-builder\\scripts\\authoring.py",
    "begin",
    "--contract",
    "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z\\fixtures\\independent-01\\bcn-equal-new\\second\\input-contract.json",
    "--run-root",
    "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z\\fixtures\\independent-01\\bcn-equal-new\\second\\docs\\plan\\run"
  ],
  "cwd": "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z",
  "timeout_seconds": 120,
  "permitted_write_root": "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z",
  "expected": {
    "exit": 0,
    "field": "state",
    "value": "STAGED",
    "read_only_root": null,
    "before_manifest": null
  },
  "start_utc": "2026-09-13T15:51:14.137715+00:00",
  "stdin_sha256": null
}
```

Exit: 2; timeout: False. Raw output: `commands/bcn-equal-new-begin/stdout.txt`, `stderr.txt`.

## bcn-equal-new-publish

```json
{
  "case": "bcn-equal-new-publish",
  "argv": [
    "C:\\Program Files\\Python310\\python.exe",
    "-B",
    "-X",
    "utf8",
    "C:\\Projects\\DevForgeAI\\src\\agents\\skills\\skill-builder\\scripts\\authoring.py",
    "publish",
    "--run-root",
    "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z\\fixtures\\independent-01\\bcn-equal-new\\second\\docs\\plan\\run"
  ],
  "cwd": "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z",
  "timeout_seconds": 120,
  "permitted_write_root": "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z",
  "expected": {
    "exit": 0,
    "field": "state",
    "value": "AUTHORED",
    "read_only_root": null,
    "before_manifest": null
  },
  "start_utc": "2026-09-13T15:51:14.223538+00:00",
  "stdin_sha256": null
}
```

Exit: 2; timeout: False. Raw output: `commands/bcn-equal-new-publish/stdout.txt`, `stderr.txt`.

## bcn-equal-new-seed-begin

```json
{
  "case": "bcn-equal-new-seed-begin",
  "argv": [
    "C:\\Program Files\\Python310\\python.exe",
    "-B",
    "-X",
    "utf8",
    "C:\\Projects\\DevForgeAI\\src\\agents\\skills\\skill-builder\\scripts\\authoring.py",
    "begin",
    "--contract",
    "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z\\fixtures\\independent-01\\bcn-equal-new\\input-contract.json",
    "--run-root",
    "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z\\fixtures\\independent-01\\bcn-equal-new\\docs\\plan\\run"
  ],
  "cwd": "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z",
  "timeout_seconds": 120,
  "permitted_write_root": "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z",
  "expected": {
    "exit": 0,
    "field": "state",
    "value": "STAGED",
    "read_only_root": null,
    "before_manifest": null
  },
  "start_utc": "2026-09-13T15:51:13.741115+00:00",
  "stdin_sha256": null
}
```

Exit: 0; timeout: False. Raw output: `commands/bcn-equal-new-seed-begin/stdout.txt`, `stderr.txt`.

## bcn-equal-new-seed-publish

```json
{
  "case": "bcn-equal-new-seed-publish",
  "argv": [
    "C:\\Program Files\\Python310\\python.exe",
    "-B",
    "-X",
    "utf8",
    "C:\\Projects\\DevForgeAI\\src\\agents\\skills\\skill-builder\\scripts\\authoring.py",
    "publish",
    "--run-root",
    "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z\\fixtures\\independent-01\\bcn-equal-new\\docs\\plan\\run"
  ],
  "cwd": "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z",
  "timeout_seconds": 120,
  "permitted_write_root": "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z",
  "expected": {
    "exit": 0,
    "field": "state",
    "value": "AUTHORED",
    "read_only_root": null,
    "before_manifest": null
  },
  "start_utc": "2026-09-13T15:51:13.842128+00:00",
  "stdin_sha256": null
}
```

Exit: 0; timeout: False. Raw output: `commands/bcn-equal-new-seed-publish/stdout.txt`, `stderr.txt`.

## bcn-new-equal-base-begin

```json
{
  "case": "bcn-new-equal-base-begin",
  "argv": [
    "C:\\Program Files\\Python310\\python.exe",
    "-B",
    "-X",
    "utf8",
    "C:\\Projects\\DevForgeAI\\src\\agents\\skills\\skill-builder\\scripts\\authoring.py",
    "begin",
    "--contract",
    "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z\\fixtures\\independent-01\\bcn-new-equal-base\\second\\input-contract.json",
    "--run-root",
    "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z\\fixtures\\independent-01\\bcn-new-equal-base\\second\\docs\\plan\\run"
  ],
  "cwd": "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z",
  "timeout_seconds": 120,
  "permitted_write_root": "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z",
  "expected": {
    "exit": 0,
    "field": "state",
    "value": "STAGED",
    "read_only_root": null,
    "before_manifest": null
  },
  "start_utc": "2026-09-13T15:51:14.713695+00:00",
  "stdin_sha256": null
}
```

Exit: 2; timeout: False. Raw output: `commands/bcn-new-equal-base-begin/stdout.txt`, `stderr.txt`.

## bcn-new-equal-base-publish

```json
{
  "case": "bcn-new-equal-base-publish",
  "argv": [
    "C:\\Program Files\\Python310\\python.exe",
    "-B",
    "-X",
    "utf8",
    "C:\\Projects\\DevForgeAI\\src\\agents\\skills\\skill-builder\\scripts\\authoring.py",
    "publish",
    "--run-root",
    "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z\\fixtures\\independent-01\\bcn-new-equal-base\\second\\docs\\plan\\run"
  ],
  "cwd": "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z",
  "timeout_seconds": 120,
  "permitted_write_root": "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z",
  "expected": {
    "exit": 0,
    "field": "state",
    "value": "AUTHORED",
    "read_only_root": null,
    "before_manifest": null
  },
  "start_utc": "2026-09-13T15:51:14.804697+00:00",
  "stdin_sha256": null
}
```

Exit: 2; timeout: False. Raw output: `commands/bcn-new-equal-base-publish/stdout.txt`, `stderr.txt`.

## bcn-new-equal-base-seed-begin

```json
{
  "case": "bcn-new-equal-base-seed-begin",
  "argv": [
    "C:\\Program Files\\Python310\\python.exe",
    "-B",
    "-X",
    "utf8",
    "C:\\Projects\\DevForgeAI\\src\\agents\\skills\\skill-builder\\scripts\\authoring.py",
    "begin",
    "--contract",
    "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z\\fixtures\\independent-01\\bcn-new-equal-base\\input-contract.json",
    "--run-root",
    "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z\\fixtures\\independent-01\\bcn-new-equal-base\\docs\\plan\\run"
  ],
  "cwd": "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z",
  "timeout_seconds": 120,
  "permitted_write_root": "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z",
  "expected": {
    "exit": 0,
    "field": "state",
    "value": "STAGED",
    "read_only_root": null,
    "before_manifest": null
  },
  "start_utc": "2026-09-13T15:51:14.302541+00:00",
  "stdin_sha256": null
}
```

Exit: 0; timeout: False. Raw output: `commands/bcn-new-equal-base-seed-begin/stdout.txt`, `stderr.txt`.

## bcn-new-equal-base-seed-publish

```json
{
  "case": "bcn-new-equal-base-seed-publish",
  "argv": [
    "C:\\Program Files\\Python310\\python.exe",
    "-B",
    "-X",
    "utf8",
    "C:\\Projects\\DevForgeAI\\src\\agents\\skills\\skill-builder\\scripts\\authoring.py",
    "publish",
    "--run-root",
    "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z\\fixtures\\independent-01\\bcn-new-equal-base\\docs\\plan\\run"
  ],
  "cwd": "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z",
  "timeout_seconds": 120,
  "permitted_write_root": "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z",
  "expected": {
    "exit": 0,
    "field": "state",
    "value": "AUTHORED",
    "read_only_root": null,
    "before_manifest": null
  },
  "start_utc": "2026-09-13T15:51:14.411252+00:00",
  "stdin_sha256": null
}
```

Exit: 0; timeout: False. Raw output: `commands/bcn-new-equal-base-seed-publish/stdout.txt`, `stderr.txt`.

## bcn-obsolete-user-edit-begin

```json
{
  "case": "bcn-obsolete-user-edit-begin",
  "argv": [
    "C:\\Program Files\\Python310\\python.exe",
    "-B",
    "-X",
    "utf8",
    "C:\\Projects\\DevForgeAI\\src\\agents\\skills\\skill-builder\\scripts\\authoring.py",
    "begin",
    "--contract",
    "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z\\fixtures\\independent-01\\bcn-obsolete-user-edit\\second\\input-contract.json",
    "--run-root",
    "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z\\fixtures\\independent-01\\bcn-obsolete-user-edit\\second\\docs\\plan\\run"
  ],
  "cwd": "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z",
  "timeout_seconds": 120,
  "permitted_write_root": "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z",
  "expected": {
    "exit": 0,
    "field": "state",
    "value": "STAGED",
    "read_only_root": null,
    "before_manifest": null
  },
  "start_utc": "2026-09-13T15:51:15.882424+00:00",
  "stdin_sha256": null
}
```

Exit: 2; timeout: False. Raw output: `commands/bcn-obsolete-user-edit-begin/stdout.txt`, `stderr.txt`.

## bcn-obsolete-user-edit-seed-begin

```json
{
  "case": "bcn-obsolete-user-edit-seed-begin",
  "argv": [
    "C:\\Program Files\\Python310\\python.exe",
    "-B",
    "-X",
    "utf8",
    "C:\\Projects\\DevForgeAI\\src\\agents\\skills\\skill-builder\\scripts\\authoring.py",
    "begin",
    "--contract",
    "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z\\fixtures\\independent-01\\bcn-obsolete-user-edit\\input-contract.json",
    "--run-root",
    "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z\\fixtures\\independent-01\\bcn-obsolete-user-edit\\docs\\plan\\run"
  ],
  "cwd": "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z",
  "timeout_seconds": 120,
  "permitted_write_root": "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z",
  "expected": {
    "exit": 0,
    "field": "state",
    "value": "STAGED",
    "read_only_root": null,
    "before_manifest": null
  },
  "start_utc": "2026-09-13T15:51:15.467304+00:00",
  "stdin_sha256": null
}
```

Exit: 0; timeout: False. Raw output: `commands/bcn-obsolete-user-edit-seed-begin/stdout.txt`, `stderr.txt`.

## bcn-obsolete-user-edit-seed-publish

```json
{
  "case": "bcn-obsolete-user-edit-seed-publish",
  "argv": [
    "C:\\Program Files\\Python310\\python.exe",
    "-B",
    "-X",
    "utf8",
    "C:\\Projects\\DevForgeAI\\src\\agents\\skills\\skill-builder\\scripts\\authoring.py",
    "publish",
    "--run-root",
    "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z\\fixtures\\independent-01\\bcn-obsolete-user-edit\\docs\\plan\\run"
  ],
  "cwd": "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z",
  "timeout_seconds": 120,
  "permitted_write_root": "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z",
  "expected": {
    "exit": 0,
    "field": "state",
    "value": "AUTHORED",
    "read_only_root": null,
    "before_manifest": null
  },
  "start_utc": "2026-09-13T15:51:15.581303+00:00",
  "stdin_sha256": null
}
```

Exit: 0; timeout: False. Raw output: `commands/bcn-obsolete-user-edit-seed-publish/stdout.txt`, `stderr.txt`.

## binding-absent

```json
{
  "case": "binding-absent",
  "argv": [
    "C:\\Program Files\\Python310\\python.exe",
    "-B",
    "-X",
    "utf8",
    "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z\\fixtures\\independent-01\\binding-absent\\project\\.agents\\skills\\summary-skill\\scripts\\check_project_binding.py",
    "--project-root",
    "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z\\fixtures\\independent-01\\binding-absent\\project",
    "--skill-root",
    "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z\\fixtures\\independent-01\\binding-absent\\project\\.agents\\skills\\summary-skill"
  ],
  "cwd": "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z",
  "timeout_seconds": 120,
  "permitted_write_root": "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z",
  "expected": {
    "exit": 1,
    "field": "reason_code",
    "value": "MISSING_BINDING",
    "read_only_root": "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z\\fixtures\\independent-01\\binding-absent\\project\\.agents\\skills\\summary-skill",
    "before_manifest": [
      {
        "path": "SKILL.md",
        "bytes": 330,
        "sha256": "ec46e875e5688b56f14e01f4e67a5fe15b55f29f71da3dd9d6b7a60817324b67"
      },
      {
        "path": "assets/devforgeai-skill.json",
        "bytes": 431,
        "sha256": "1dea9c740cf1d7a68219895ba9ad2a09b97b0c67ab7f807ad8fa92ebc178d6f4"
      },
      {
        "path": "references/adaptive-contract.md",
        "bytes": 297,
        "sha256": "ee1b190a764954b0dda1b9addc95f9112deda708fa558d7a90b64374ad7dbb58"
      },
      {
        "path": "scripts/check_project_binding.py",
        "bytes": 12232,
        "sha256": "688b1b7404133639a6f0f69c8fdb88670db230110ac7e8e24b64ccf32a24e241"
      }
    ]
  },
  "start_utc": "2026-09-13T15:50:43.024020+00:00",
  "stdin_sha256": null
}
```

Exit: 1; timeout: False. Raw output: `commands/binding-absent/stdout.txt`, `stderr.txt`.

## binding-bad-date

```json
{
  "case": "binding-bad-date",
  "argv": [
    "C:\\Program Files\\Python310\\python.exe",
    "-B",
    "-X",
    "utf8",
    "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z\\fixtures\\independent-01\\binding-bad-date\\project\\.agents\\skills\\summary-skill\\scripts\\check_project_binding.py",
    "--project-root",
    "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z\\fixtures\\independent-01\\binding-bad-date\\project",
    "--skill-root",
    "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z\\fixtures\\independent-01\\binding-bad-date\\project\\.agents\\skills\\summary-skill"
  ],
  "cwd": "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z",
  "timeout_seconds": 120,
  "permitted_write_root": "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z",
  "expected": {
    "exit": 1,
    "field": "reason_code",
    "value": "INVALID_BINDING",
    "read_only_root": "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z\\fixtures\\independent-01\\binding-bad-date\\project\\.agents\\skills\\summary-skill",
    "before_manifest": [
      {
        "path": "SKILL.md",
        "bytes": 330,
        "sha256": "ec46e875e5688b56f14e01f4e67a5fe15b55f29f71da3dd9d6b7a60817324b67"
      },
      {
        "path": "assets/devforgeai-skill.json",
        "bytes": 431,
        "sha256": "1dea9c740cf1d7a68219895ba9ad2a09b97b0c67ab7f807ad8fa92ebc178d6f4"
      },
      {
        "path": "references/adaptive-contract.md",
        "bytes": 297,
        "sha256": "ee1b190a764954b0dda1b9addc95f9112deda708fa558d7a90b64374ad7dbb58"
      },
      {
        "path": "scripts/check_project_binding.py",
        "bytes": 12232,
        "sha256": "688b1b7404133639a6f0f69c8fdb88670db230110ac7e8e24b64ccf32a24e241"
      }
    ]
  },
  "start_utc": "2026-09-13T15:50:44.175385+00:00",
  "stdin_sha256": null
}
```

Exit: 1; timeout: False. Raw output: `commands/binding-bad-date/stdout.txt`, `stderr.txt`.

## binding-boolean-revision

```json
{
  "case": "binding-boolean-revision",
  "argv": [
    "C:\\Program Files\\Python310\\python.exe",
    "-B",
    "-X",
    "utf8",
    "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z\\fixtures\\independent-01\\binding-boolean-revision\\project\\.agents\\skills\\summary-skill\\scripts\\check_project_binding.py",
    "--project-root",
    "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z\\fixtures\\independent-01\\binding-boolean-revision\\project",
    "--skill-root",
    "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z\\fixtures\\independent-01\\binding-boolean-revision\\project\\.agents\\skills\\summary-skill"
  ],
  "cwd": "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z",
  "timeout_seconds": 120,
  "permitted_write_root": "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z",
  "expected": {
    "exit": 1,
    "field": "reason_code",
    "value": "INVALID_BINDING",
    "read_only_root": "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z\\fixtures\\independent-01\\binding-boolean-revision\\project\\.agents\\skills\\summary-skill",
    "before_manifest": [
      {
        "path": "SKILL.md",
        "bytes": 330,
        "sha256": "ec46e875e5688b56f14e01f4e67a5fe15b55f29f71da3dd9d6b7a60817324b67"
      },
      {
        "path": "assets/devforgeai-skill.json",
        "bytes": 431,
        "sha256": "1dea9c740cf1d7a68219895ba9ad2a09b97b0c67ab7f807ad8fa92ebc178d6f4"
      },
      {
        "path": "references/adaptive-contract.md",
        "bytes": 297,
        "sha256": "ee1b190a764954b0dda1b9addc95f9112deda708fa558d7a90b64374ad7dbb58"
      },
      {
        "path": "scripts/check_project_binding.py",
        "bytes": 12232,
        "sha256": "688b1b7404133639a6f0f69c8fdb88670db230110ac7e8e24b64ccf32a24e241"
      }
    ]
  },
  "start_utc": "2026-09-13T15:50:44.061381+00:00",
  "stdin_sha256": null
}
```

Exit: 1; timeout: False. Raw output: `commands/binding-boolean-revision/stdout.txt`, `stderr.txt`.

## binding-byte-limit

```json
{
  "case": "binding-byte-limit",
  "argv": [
    "C:\\Program Files\\Python310\\python.exe",
    "-B",
    "-X",
    "utf8",
    "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z\\fixtures\\independent-01\\binding-byte-limit\\project\\.agents\\skills\\summary-skill\\scripts\\check_project_binding.py",
    "--project-root",
    "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z\\fixtures\\independent-01\\binding-byte-limit\\project",
    "--skill-root",
    "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z\\fixtures\\independent-01\\binding-byte-limit\\project\\.agents\\skills\\summary-skill"
  ],
  "cwd": "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z",
  "timeout_seconds": 120,
  "permitted_write_root": "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z",
  "expected": {
    "exit": 2,
    "field": "reason_code",
    "value": "CAPTURE_LIMIT",
    "read_only_root": null,
    "before_manifest": null
  },
  "start_utc": "2026-09-13T15:51:03.576648+00:00",
  "stdin_sha256": null
}
```

Exit: 2; timeout: False. Raw output: `commands/binding-byte-limit/stdout.txt`, `stderr.txt`.

## binding-case-root

```json
{
  "case": "binding-case-root",
  "argv": [
    "C:\\Program Files\\Python310\\python.exe",
    "-B",
    "-X",
    "utf8",
    "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z\\fixtures\\independent-01\\binding-case-root\\project\\.agents\\skills\\summary-skill\\scripts\\check_project_binding.py",
    "--project-root",
    "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z\\fixtures\\independent-01\\binding-case-root\\project",
    "--skill-root",
    "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z\\fixtures\\independent-01\\binding-case-root\\project\\.agents\\skills\\summary-skill"
  ],
  "cwd": "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z",
  "timeout_seconds": 120,
  "permitted_write_root": "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z",
  "expected": {
    "exit": 0,
    "field": "reason_code",
    "value": "BOUND",
    "read_only_root": "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z\\fixtures\\independent-01\\binding-case-root\\project\\.agents\\skills\\summary-skill",
    "before_manifest": [
      {
        "path": "SKILL.md",
        "bytes": 330,
        "sha256": "ec46e875e5688b56f14e01f4e67a5fe15b55f29f71da3dd9d6b7a60817324b67"
      },
      {
        "path": "assets/devforgeai-skill.json",
        "bytes": 431,
        "sha256": "1dea9c740cf1d7a68219895ba9ad2a09b97b0c67ab7f807ad8fa92ebc178d6f4"
      },
      {
        "path": "references/adaptive-contract.md",
        "bytes": 297,
        "sha256": "ee1b190a764954b0dda1b9addc95f9112deda708fa558d7a90b64374ad7dbb58"
      },
      {
        "path": "scripts/check_project_binding.py",
        "bytes": 12232,
        "sha256": "688b1b7404133639a6f0f69c8fdb88670db230110ac7e8e24b64ccf32a24e241"
      }
    ]
  },
  "start_utc": "2026-09-13T15:50:45.528401+00:00",
  "stdin_sha256": null
}
```

Exit: 0; timeout: False. Raw output: `commands/binding-case-root/stdout.txt`, `stderr.txt`.

## binding-changed

```json
{
  "case": "binding-changed",
  "argv": [
    "C:\\Program Files\\Python310\\python.exe",
    "-B",
    "-X",
    "utf8",
    "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z\\fixtures\\independent-01\\binding-changed\\project\\.agents\\skills\\summary-skill\\scripts\\check_project_binding.py",
    "--project-root",
    "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z\\fixtures\\independent-01\\binding-changed\\project",
    "--skill-root",
    "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z\\fixtures\\independent-01\\binding-changed\\project\\.agents\\skills\\summary-skill"
  ],
  "cwd": "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z",
  "timeout_seconds": 120,
  "permitted_write_root": "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z",
  "expected": {
    "exit": 1,
    "field": "reason_code",
    "value": "PACKAGE_CHANGED",
    "read_only_root": "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z\\fixtures\\independent-01\\binding-changed\\project\\.agents\\skills\\summary-skill",
    "before_manifest": [
      {
        "path": "SKILL.md",
        "bytes": 330,
        "sha256": "ec46e875e5688b56f14e01f4e67a5fe15b55f29f71da3dd9d6b7a60817324b67"
      },
      {
        "path": "assets/devforgeai-skill.json",
        "bytes": 431,
        "sha256": "1dea9c740cf1d7a68219895ba9ad2a09b97b0c67ab7f807ad8fa92ebc178d6f4"
      },
      {
        "path": "new.txt",
        "bytes": 7,
        "sha256": "d67e2e944994496c8d8ec76eed0cf9f09679448d584b532bebf941852a37f5ed"
      },
      {
        "path": "references/adaptive-contract.md",
        "bytes": 297,
        "sha256": "ee1b190a764954b0dda1b9addc95f9112deda708fa558d7a90b64374ad7dbb58"
      },
      {
        "path": "scripts/check_project_binding.py",
        "bytes": 12232,
        "sha256": "688b1b7404133639a6f0f69c8fdb88670db230110ac7e8e24b64ccf32a24e241"
      }
    ]
  },
  "start_utc": "2026-09-13T15:50:43.341801+00:00",
  "stdin_sha256": null
}
```

Exit: 1; timeout: False. Raw output: `commands/binding-changed/stdout.txt`, `stderr.txt`.

## binding-core-variant

```json
{
  "case": "binding-core-variant",
  "argv": [
    "C:\\Program Files\\Python310\\python.exe",
    "-B",
    "-X",
    "utf8",
    "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z\\fixtures\\independent-01\\binding-core-variant\\project\\.agents\\skills\\summary-skill\\scripts\\check_project_binding.py",
    "--project-root",
    "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z\\fixtures\\independent-01\\binding-core-variant\\project",
    "--skill-root",
    "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z\\fixtures\\independent-01\\binding-core-variant\\project\\.agents\\skills\\summary-skill"
  ],
  "cwd": "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z",
  "timeout_seconds": 120,
  "permitted_write_root": "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z",
  "expected": {
    "exit": 1,
    "field": "reason_code",
    "value": "AMBIGUOUS_ROLE",
    "read_only_root": "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z\\fixtures\\independent-01\\binding-core-variant\\project\\.agents\\skills\\summary-skill",
    "before_manifest": [
      {
        "path": "SKILL.md",
        "bytes": 330,
        "sha256": "ec46e875e5688b56f14e01f4e67a5fe15b55f29f71da3dd9d6b7a60817324b67"
      },
      {
        "path": "assets/devforgeai-skill.json",
        "bytes": 426,
        "sha256": "bfb2faa90c47d6104067af8135ae8a453b84a03c19840aea79f9b673eed3d3f0"
      },
      {
        "path": "references/adaptive-contract.md",
        "bytes": 297,
        "sha256": "ee1b190a764954b0dda1b9addc95f9112deda708fa558d7a90b64374ad7dbb58"
      },
      {
        "path": "scripts/check_project_binding.py",
        "bytes": 12232,
        "sha256": "688b1b7404133639a6f0f69c8fdb88670db230110ac7e8e24b64ccf32a24e241"
      }
    ]
  },
  "start_utc": "2026-09-13T15:50:44.534322+00:00",
  "stdin_sha256": null
}
```

Exit: 1; timeout: False. Raw output: `commands/binding-core-variant/stdout.txt`, `stderr.txt`.

## binding-correct

```json
{
  "case": "binding-correct",
  "argv": [
    "C:\\Program Files\\Python310\\python.exe",
    "-B",
    "-X",
    "utf8",
    "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z\\fixtures\\independent-01\\binding-correct\\project\\.agents\\skills\\summary-skill\\scripts\\check_project_binding.py",
    "--project-root",
    "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z\\fixtures\\independent-01\\binding-correct\\project",
    "--skill-root",
    "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z\\fixtures\\independent-01\\binding-correct\\project\\.agents\\skills\\summary-skill"
  ],
  "cwd": "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z",
  "timeout_seconds": 120,
  "permitted_write_root": "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z",
  "expected": {
    "exit": 0,
    "field": "reason_code",
    "value": "BOUND",
    "read_only_root": "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z\\fixtures\\independent-01\\binding-correct\\project\\.agents\\skills\\summary-skill",
    "before_manifest": [
      {
        "path": "SKILL.md",
        "bytes": 330,
        "sha256": "ec46e875e5688b56f14e01f4e67a5fe15b55f29f71da3dd9d6b7a60817324b67"
      },
      {
        "path": "assets/devforgeai-skill.json",
        "bytes": 431,
        "sha256": "1dea9c740cf1d7a68219895ba9ad2a09b97b0c67ab7f807ad8fa92ebc178d6f4"
      },
      {
        "path": "references/adaptive-contract.md",
        "bytes": 297,
        "sha256": "ee1b190a764954b0dda1b9addc95f9112deda708fa558d7a90b64374ad7dbb58"
      },
      {
        "path": "scripts/check_project_binding.py",
        "bytes": 12232,
        "sha256": "688b1b7404133639a6f0f69c8fdb88670db230110ac7e8e24b64ccf32a24e241"
      }
    ]
  },
  "start_utc": "2026-09-13T15:50:42.820038+00:00",
  "stdin_sha256": null
}
```

Exit: 0; timeout: False. Raw output: `commands/binding-correct/stdout.txt`, `stderr.txt`.

## binding-duplicate-name

```json
{
  "case": "binding-duplicate-name",
  "argv": [
    "C:\\Program Files\\Python310\\python.exe",
    "-B",
    "-X",
    "utf8",
    "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z\\fixtures\\independent-01\\binding-duplicate-name\\project\\.agents\\skills\\summary-skill\\scripts\\check_project_binding.py",
    "--project-root",
    "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z\\fixtures\\independent-01\\binding-duplicate-name\\project",
    "--skill-root",
    "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z\\fixtures\\independent-01\\binding-duplicate-name\\project\\.agents\\skills\\summary-skill"
  ],
  "cwd": "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z",
  "timeout_seconds": 120,
  "permitted_write_root": "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z",
  "expected": {
    "exit": 1,
    "field": "reason_code",
    "value": "INVALID_BINDING",
    "read_only_root": "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z\\fixtures\\independent-01\\binding-duplicate-name\\project\\.agents\\skills\\summary-skill",
    "before_manifest": [
      {
        "path": "SKILL.md",
        "bytes": 330,
        "sha256": "ec46e875e5688b56f14e01f4e67a5fe15b55f29f71da3dd9d6b7a60817324b67"
      },
      {
        "path": "assets/devforgeai-skill.json",
        "bytes": 431,
        "sha256": "1dea9c740cf1d7a68219895ba9ad2a09b97b0c67ab7f807ad8fa92ebc178d6f4"
      },
      {
        "path": "references/adaptive-contract.md",
        "bytes": 297,
        "sha256": "ee1b190a764954b0dda1b9addc95f9112deda708fa558d7a90b64374ad7dbb58"
      },
      {
        "path": "scripts/check_project_binding.py",
        "bytes": 12232,
        "sha256": "688b1b7404133639a6f0f69c8fdb88670db230110ac7e8e24b64ccf32a24e241"
      }
    ]
  },
  "start_utc": "2026-09-13T15:50:43.523830+00:00",
  "stdin_sha256": null
}
```

Exit: 1; timeout: False. Raw output: `commands/binding-duplicate-name/stdout.txt`, `stderr.txt`.

## binding-excluded-generated

```json
{
  "case": "binding-excluded-generated",
  "argv": [
    "C:\\Program Files\\Python310\\python.exe",
    "-B",
    "-X",
    "utf8",
    "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z\\fixtures\\independent-01\\binding-excluded-generated\\project\\.agents\\skills\\summary-skill\\scripts\\check_project_binding.py",
    "--project-root",
    "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z\\fixtures\\independent-01\\binding-excluded-generated\\project",
    "--skill-root",
    "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z\\fixtures\\independent-01\\binding-excluded-generated\\project\\.agents\\skills\\summary-skill"
  ],
  "cwd": "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z",
  "timeout_seconds": 120,
  "permitted_write_root": "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z",
  "expected": {
    "exit": 1,
    "field": "reason_code",
    "value": "UNSAFE_PATH",
    "read_only_root": null,
    "before_manifest": null
  },
  "start_utc": "2026-09-13T15:50:45.176426+00:00",
  "stdin_sha256": null
}
```

Exit: 1; timeout: False. Raw output: `commands/binding-excluded-generated/stdout.txt`, `stderr.txt`.

## binding-extra-field

```json
{
  "case": "binding-extra-field",
  "argv": [
    "C:\\Program Files\\Python310\\python.exe",
    "-B",
    "-X",
    "utf8",
    "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z\\fixtures\\independent-01\\binding-extra-field\\project\\.agents\\skills\\summary-skill\\scripts\\check_project_binding.py",
    "--project-root",
    "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z\\fixtures\\independent-01\\binding-extra-field\\project",
    "--skill-root",
    "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z\\fixtures\\independent-01\\binding-extra-field\\project\\.agents\\skills\\summary-skill"
  ],
  "cwd": "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z",
  "timeout_seconds": 120,
  "permitted_write_root": "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z",
  "expected": {
    "exit": 1,
    "field": "reason_code",
    "value": "INVALID_BINDING",
    "read_only_root": "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z\\fixtures\\independent-01\\binding-extra-field\\project\\.agents\\skills\\summary-skill",
    "before_manifest": [
      {
        "path": "SKILL.md",
        "bytes": 330,
        "sha256": "ec46e875e5688b56f14e01f4e67a5fe15b55f29f71da3dd9d6b7a60817324b67"
      },
      {
        "path": "assets/devforgeai-skill.json",
        "bytes": 431,
        "sha256": "1dea9c740cf1d7a68219895ba9ad2a09b97b0c67ab7f807ad8fa92ebc178d6f4"
      },
      {
        "path": "references/adaptive-contract.md",
        "bytes": 297,
        "sha256": "ee1b190a764954b0dda1b9addc95f9112deda708fa558d7a90b64374ad7dbb58"
      },
      {
        "path": "scripts/check_project_binding.py",
        "bytes": 12232,
        "sha256": "688b1b7404133639a6f0f69c8fdb88670db230110ac7e8e24b64ccf32a24e241"
      }
    ]
  },
  "start_utc": "2026-09-13T15:50:43.969381+00:00",
  "stdin_sha256": null
}
```

Exit: 1; timeout: False. Raw output: `commands/binding-extra-field/stdout.txt`, `stderr.txt`.

## binding-file-limit

```json
{
  "case": "binding-file-limit",
  "argv": [
    "C:\\Program Files\\Python310\\python.exe",
    "-B",
    "-X",
    "utf8",
    "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z\\fixtures\\independent-01\\binding-file-limit\\project\\.agents\\skills\\summary-skill\\scripts\\check_project_binding.py",
    "--project-root",
    "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z\\fixtures\\independent-01\\binding-file-limit\\project",
    "--skill-root",
    "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z\\fixtures\\independent-01\\binding-file-limit\\project\\.agents\\skills\\summary-skill"
  ],
  "cwd": "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z",
  "timeout_seconds": 120,
  "permitted_write_root": "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z",
  "expected": {
    "exit": 2,
    "field": "reason_code",
    "value": "CAPTURE_LIMIT",
    "read_only_root": null,
    "before_manifest": null
  },
  "start_utc": "2026-09-13T15:50:46.445276+00:00",
  "stdin_sha256": null
}
```

Exit: 2; timeout: False. Raw output: `commands/binding-file-limit/stdout.txt`, `stderr.txt`.

## binding-hostile-path

```json
{
  "case": "binding-hostile-path",
  "argv": [
    "C:\\Program Files\\Python310\\python.exe",
    "-B",
    "-X",
    "utf8",
    "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z\\fixtures\\independent-01\\binding-hostile-path\\space café & $ ; ' (project)\\.agents\\skills\\summary-skill\\scripts\\check_project_binding.py",
    "--project-root",
    "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z\\fixtures\\independent-01\\binding-hostile-path\\space café & $ ; ' (project)",
    "--skill-root",
    "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z\\fixtures\\independent-01\\binding-hostile-path\\space café & $ ; ' (project)\\.agents\\skills\\summary-skill"
  ],
  "cwd": "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z",
  "timeout_seconds": 120,
  "permitted_write_root": "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z",
  "expected": {
    "exit": 0,
    "field": "reason_code",
    "value": "BOUND",
    "read_only_root": "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z\\fixtures\\independent-01\\binding-hostile-path\\space café & $ ; ' (project)\\.agents\\skills\\summary-skill",
    "before_manifest": [
      {
        "path": "SKILL.md",
        "bytes": 330,
        "sha256": "ec46e875e5688b56f14e01f4e67a5fe15b55f29f71da3dd9d6b7a60817324b67"
      },
      {
        "path": "assets/devforgeai-skill.json",
        "bytes": 431,
        "sha256": "1dea9c740cf1d7a68219895ba9ad2a09b97b0c67ab7f807ad8fa92ebc178d6f4"
      },
      {
        "path": "references/adaptive-contract.md",
        "bytes": 297,
        "sha256": "ee1b190a764954b0dda1b9addc95f9112deda708fa558d7a90b64374ad7dbb58"
      },
      {
        "path": "scripts/check_project_binding.py",
        "bytes": 12232,
        "sha256": "688b1b7404133639a6f0f69c8fdb88670db230110ac7e8e24b64ccf32a24e241"
      }
    ]
  },
  "start_utc": "2026-09-13T15:50:45.308427+00:00",
  "stdin_sha256": null
}
```

Exit: 0; timeout: False. Raw output: `commands/binding-hostile-path/stdout.txt`, `stderr.txt`.

## binding-inactive

```json
{
  "case": "binding-inactive",
  "argv": [
    "C:\\Program Files\\Python310\\python.exe",
    "-B",
    "-X",
    "utf8",
    "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z\\fixtures\\independent-01\\binding-inactive\\project\\.agents\\skills\\summary-skill\\scripts\\check_project_binding.py",
    "--project-root",
    "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z\\fixtures\\independent-01\\binding-inactive\\project",
    "--skill-root",
    "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z\\fixtures\\independent-01\\binding-inactive\\project\\.agents\\skills\\summary-skill"
  ],
  "cwd": "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z",
  "timeout_seconds": 120,
  "permitted_write_root": "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z",
  "expected": {
    "exit": 1,
    "field": "reason_code",
    "value": "NOT_SELECTED",
    "read_only_root": "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z\\fixtures\\independent-01\\binding-inactive\\project\\.agents\\skills\\summary-skill",
    "before_manifest": [
      {
        "path": "SKILL.md",
        "bytes": 330,
        "sha256": "ec46e875e5688b56f14e01f4e67a5fe15b55f29f71da3dd9d6b7a60817324b67"
      },
      {
        "path": "assets/devforgeai-skill.json",
        "bytes": 431,
        "sha256": "1dea9c740cf1d7a68219895ba9ad2a09b97b0c67ab7f807ad8fa92ebc178d6f4"
      },
      {
        "path": "references/adaptive-contract.md",
        "bytes": 297,
        "sha256": "ee1b190a764954b0dda1b9addc95f9112deda708fa558d7a90b64374ad7dbb58"
      },
      {
        "path": "scripts/check_project_binding.py",
        "bytes": 12232,
        "sha256": "688b1b7404133639a6f0f69c8fdb88670db230110ac7e8e24b64ccf32a24e241"
      }
    ]
  },
  "start_utc": "2026-09-13T15:50:43.225731+00:00",
  "stdin_sha256": null
}
```

Exit: 1; timeout: False. Raw output: `commands/binding-inactive/stdout.txt`, `stderr.txt`.

## binding-invalid-descriptor

```json
{
  "case": "binding-invalid-descriptor",
  "argv": [
    "C:\\Program Files\\Python310\\python.exe",
    "-B",
    "-X",
    "utf8",
    "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z\\fixtures\\independent-01\\binding-invalid-descriptor\\project\\.agents\\skills\\summary-skill\\scripts\\check_project_binding.py",
    "--project-root",
    "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z\\fixtures\\independent-01\\binding-invalid-descriptor\\project",
    "--skill-root",
    "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z\\fixtures\\independent-01\\binding-invalid-descriptor\\project\\.agents\\skills\\summary-skill"
  ],
  "cwd": "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z",
  "timeout_seconds": 120,
  "permitted_write_root": "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z",
  "expected": {
    "exit": 1,
    "field": "reason_code",
    "value": "INVALID_BINDING",
    "read_only_root": "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z\\fixtures\\independent-01\\binding-invalid-descriptor\\project\\.agents\\skills\\summary-skill",
    "before_manifest": [
      {
        "path": "SKILL.md",
        "bytes": 330,
        "sha256": "ec46e875e5688b56f14e01f4e67a5fe15b55f29f71da3dd9d6b7a60817324b67"
      },
      {
        "path": "assets/devforgeai-skill.json",
        "bytes": 3,
        "sha256": "ca3d163bab055381827226140568f3bef7eaac187cebd76878e0b63e9e442356"
      },
      {
        "path": "references/adaptive-contract.md",
        "bytes": 297,
        "sha256": "ee1b190a764954b0dda1b9addc95f9112deda708fa558d7a90b64374ad7dbb58"
      },
      {
        "path": "scripts/check_project_binding.py",
        "bytes": 12232,
        "sha256": "688b1b7404133639a6f0f69c8fdb88670db230110ac7e8e24b64ccf32a24e241"
      }
    ]
  },
  "start_utc": "2026-09-13T15:50:44.273213+00:00",
  "stdin_sha256": null
}
```

Exit: 1; timeout: False. Raw output: `commands/binding-invalid-descriptor/stdout.txt`, `stderr.txt`.

## binding-invalid-related

```json
{
  "case": "binding-invalid-related",
  "argv": [
    "C:\\Program Files\\Python310\\python.exe",
    "-B",
    "-X",
    "utf8",
    "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z\\fixtures\\independent-01\\binding-invalid-related\\project\\.agents\\skills\\summary-skill\\scripts\\check_project_binding.py",
    "--project-root",
    "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z\\fixtures\\independent-01\\binding-invalid-related\\project",
    "--skill-root",
    "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z\\fixtures\\independent-01\\binding-invalid-related\\project\\.agents\\skills\\summary-skill"
  ],
  "cwd": "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z",
  "timeout_seconds": 120,
  "permitted_write_root": "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z",
  "expected": {
    "exit": 1,
    "field": "reason_code",
    "value": "INVALID_BINDING",
    "read_only_root": "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z\\fixtures\\independent-01\\binding-invalid-related\\project\\.agents\\skills\\summary-skill",
    "before_manifest": [
      {
        "path": "SKILL.md",
        "bytes": 330,
        "sha256": "ec46e875e5688b56f14e01f4e67a5fe15b55f29f71da3dd9d6b7a60817324b67"
      },
      {
        "path": "assets/devforgeai-skill.json",
        "bytes": 431,
        "sha256": "1dea9c740cf1d7a68219895ba9ad2a09b97b0c67ab7f807ad8fa92ebc178d6f4"
      },
      {
        "path": "references/adaptive-contract.md",
        "bytes": 297,
        "sha256": "ee1b190a764954b0dda1b9addc95f9112deda708fa558d7a90b64374ad7dbb58"
      },
      {
        "path": "scripts/check_project_binding.py",
        "bytes": 12232,
        "sha256": "688b1b7404133639a6f0f69c8fdb88670db230110ac7e8e24b64ccf32a24e241"
      }
    ]
  },
  "start_utc": "2026-09-13T15:50:44.965425+00:00",
  "stdin_sha256": null
}
```

Exit: 1; timeout: False. Raw output: `commands/binding-invalid-related/stdout.txt`, `stderr.txt`.

## binding-missing-resource

```json
{
  "case": "binding-missing-resource",
  "argv": [
    "C:\\Program Files\\Python310\\python.exe",
    "-B",
    "-X",
    "utf8",
    "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z\\fixtures\\independent-01\\binding-missing-resource\\project\\.agents\\skills\\summary-skill\\scripts\\check_project_binding.py",
    "--project-root",
    "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z\\fixtures\\independent-01\\binding-missing-resource\\project",
    "--skill-root",
    "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z\\fixtures\\independent-01\\binding-missing-resource\\project\\.agents\\skills\\summary-skill"
  ],
  "cwd": "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z",
  "timeout_seconds": 120,
  "permitted_write_root": "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z",
  "expected": {
    "exit": 1,
    "field": "reason_code",
    "value": "INVALID_BINDING",
    "read_only_root": "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z\\fixtures\\independent-01\\binding-missing-resource\\project\\.agents\\skills\\summary-skill",
    "before_manifest": [
      {
        "path": "SKILL.md",
        "bytes": 330,
        "sha256": "ec46e875e5688b56f14e01f4e67a5fe15b55f29f71da3dd9d6b7a60817324b67"
      },
      {
        "path": "assets/devforgeai-skill.json",
        "bytes": 409,
        "sha256": "430da4d3572f503e1bc8cc62a1834cff2fdb2367831fa65642beef75f0e8e6f4"
      },
      {
        "path": "references/adaptive-contract.md",
        "bytes": 297,
        "sha256": "ee1b190a764954b0dda1b9addc95f9112deda708fa558d7a90b64374ad7dbb58"
      },
      {
        "path": "scripts/check_project_binding.py",
        "bytes": 12232,
        "sha256": "688b1b7404133639a6f0f69c8fdb88670db230110ac7e8e24b64ccf32a24e241"
      }
    ]
  },
  "start_utc": "2026-09-13T15:50:44.392942+00:00",
  "stdin_sha256": null
}
```

Exit: 1; timeout: False. Raw output: `commands/binding-missing-resource/stdout.txt`, `stderr.txt`.

## binding-role

```json
{
  "case": "binding-role",
  "argv": [
    "C:\\Program Files\\Python310\\python.exe",
    "-B",
    "-X",
    "utf8",
    "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z\\fixtures\\independent-01\\binding-role\\project\\.agents\\skills\\summary-skill\\scripts\\check_project_binding.py",
    "--project-root",
    "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z\\fixtures\\independent-01\\binding-role\\project",
    "--skill-root",
    "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z\\fixtures\\independent-01\\binding-role\\project\\.agents\\skills\\summary-skill"
  ],
  "cwd": "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z",
  "timeout_seconds": 120,
  "permitted_write_root": "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z",
  "expected": {
    "exit": 1,
    "field": "reason_code",
    "value": "ROLE_MISMATCH",
    "read_only_root": "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z\\fixtures\\independent-01\\binding-role\\project\\.agents\\skills\\summary-skill",
    "before_manifest": [
      {
        "path": "SKILL.md",
        "bytes": 330,
        "sha256": "ec46e875e5688b56f14e01f4e67a5fe15b55f29f71da3dd9d6b7a60817324b67"
      },
      {
        "path": "assets/devforgeai-skill.json",
        "bytes": 431,
        "sha256": "1dea9c740cf1d7a68219895ba9ad2a09b97b0c67ab7f807ad8fa92ebc178d6f4"
      },
      {
        "path": "references/adaptive-contract.md",
        "bytes": 297,
        "sha256": "ee1b190a764954b0dda1b9addc95f9112deda708fa558d7a90b64374ad7dbb58"
      },
      {
        "path": "scripts/check_project_binding.py",
        "bytes": 12232,
        "sha256": "688b1b7404133639a6f0f69c8fdb88670db230110ac7e8e24b64ccf32a24e241"
      }
    ]
  },
  "start_utc": "2026-09-13T15:50:43.614830+00:00",
  "stdin_sha256": null
}
```

Exit: 1; timeout: False. Raw output: `commands/binding-role/stdout.txt`, `stderr.txt`.

## binding-two-variants

```json
{
  "case": "binding-two-variants",
  "argv": [
    "C:\\Program Files\\Python310\\python.exe",
    "-B",
    "-X",
    "utf8",
    "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z\\fixtures\\independent-01\\binding-two-variants\\project\\.agents\\skills\\summary-skill\\scripts\\check_project_binding.py",
    "--project-root",
    "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z\\fixtures\\independent-01\\binding-two-variants\\project",
    "--skill-root",
    "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z\\fixtures\\independent-01\\binding-two-variants\\project\\.agents\\skills\\summary-skill"
  ],
  "cwd": "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z",
  "timeout_seconds": 120,
  "permitted_write_root": "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z",
  "expected": {
    "exit": 1,
    "field": "reason_code",
    "value": "AMBIGUOUS_ROLE",
    "read_only_root": "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z\\fixtures\\independent-01\\binding-two-variants\\project\\.agents\\skills\\summary-skill",
    "before_manifest": [
      {
        "path": "SKILL.md",
        "bytes": 330,
        "sha256": "ec46e875e5688b56f14e01f4e67a5fe15b55f29f71da3dd9d6b7a60817324b67"
      },
      {
        "path": "assets/devforgeai-skill.json",
        "bytes": 431,
        "sha256": "1dea9c740cf1d7a68219895ba9ad2a09b97b0c67ab7f807ad8fa92ebc178d6f4"
      },
      {
        "path": "references/adaptive-contract.md",
        "bytes": 297,
        "sha256": "ee1b190a764954b0dda1b9addc95f9112deda708fa558d7a90b64374ad7dbb58"
      },
      {
        "path": "scripts/check_project_binding.py",
        "bytes": 12232,
        "sha256": "688b1b7404133639a6f0f69c8fdb88670db230110ac7e8e24b64ccf32a24e241"
      }
    ]
  },
  "start_utc": "2026-09-13T15:50:44.746915+00:00",
  "stdin_sha256": null
}
```

Exit: 1; timeout: False. Raw output: `commands/binding-two-variants/stdout.txt`, `stderr.txt`.

## binding-unbound

```json
{
  "case": "binding-unbound",
  "argv": [
    "C:\\Program Files\\Python310\\python.exe",
    "-B",
    "-X",
    "utf8",
    "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z\\fixtures\\independent-01\\binding-unbound\\project\\.agents\\skills\\summary-skill\\scripts\\check_project_binding.py",
    "--project-root",
    "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z\\fixtures\\independent-01\\binding-unbound\\project",
    "--skill-root",
    "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z\\fixtures\\independent-01\\binding-unbound\\project\\.agents\\skills\\summary-skill"
  ],
  "cwd": "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z",
  "timeout_seconds": 120,
  "permitted_write_root": "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z",
  "expected": {
    "exit": 1,
    "field": "reason_code",
    "value": "UNBOUND_SKILL",
    "read_only_root": "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z\\fixtures\\independent-01\\binding-unbound\\project\\.agents\\skills\\summary-skill",
    "before_manifest": [
      {
        "path": "SKILL.md",
        "bytes": 330,
        "sha256": "ec46e875e5688b56f14e01f4e67a5fe15b55f29f71da3dd9d6b7a60817324b67"
      },
      {
        "path": "assets/devforgeai-skill.json",
        "bytes": 431,
        "sha256": "1dea9c740cf1d7a68219895ba9ad2a09b97b0c67ab7f807ad8fa92ebc178d6f4"
      },
      {
        "path": "references/adaptive-contract.md",
        "bytes": 297,
        "sha256": "ee1b190a764954b0dda1b9addc95f9112deda708fa558d7a90b64374ad7dbb58"
      },
      {
        "path": "scripts/check_project_binding.py",
        "bytes": 12232,
        "sha256": "688b1b7404133639a6f0f69c8fdb88670db230110ac7e8e24b64ccf32a24e241"
      }
    ]
  },
  "start_utc": "2026-09-13T15:50:43.745830+00:00",
  "stdin_sha256": null
}
```

Exit: 1; timeout: False. Raw output: `commands/binding-unbound/stdout.txt`, `stderr.txt`.

## binding-unknown-version

```json
{
  "case": "binding-unknown-version",
  "argv": [
    "C:\\Program Files\\Python310\\python.exe",
    "-B",
    "-X",
    "utf8",
    "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z\\fixtures\\independent-01\\binding-unknown-version\\project\\.agents\\skills\\summary-skill\\scripts\\check_project_binding.py",
    "--project-root",
    "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z\\fixtures\\independent-01\\binding-unknown-version\\project",
    "--skill-root",
    "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z\\fixtures\\independent-01\\binding-unknown-version\\project\\.agents\\skills\\summary-skill"
  ],
  "cwd": "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z",
  "timeout_seconds": 120,
  "permitted_write_root": "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z",
  "expected": {
    "exit": 1,
    "field": "reason_code",
    "value": "INVALID_BINDING",
    "read_only_root": "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z\\fixtures\\independent-01\\binding-unknown-version\\project\\.agents\\skills\\summary-skill",
    "before_manifest": [
      {
        "path": "SKILL.md",
        "bytes": 330,
        "sha256": "ec46e875e5688b56f14e01f4e67a5fe15b55f29f71da3dd9d6b7a60817324b67"
      },
      {
        "path": "assets/devforgeai-skill.json",
        "bytes": 431,
        "sha256": "1dea9c740cf1d7a68219895ba9ad2a09b97b0c67ab7f807ad8fa92ebc178d6f4"
      },
      {
        "path": "references/adaptive-contract.md",
        "bytes": 297,
        "sha256": "ee1b190a764954b0dda1b9addc95f9112deda708fa558d7a90b64374ad7dbb58"
      },
      {
        "path": "scripts/check_project_binding.py",
        "bytes": 12232,
        "sha256": "688b1b7404133639a6f0f69c8fdb88670db230110ac7e8e24b64ccf32a24e241"
      }
    ]
  },
  "start_utc": "2026-09-13T15:50:43.865381+00:00",
  "stdin_sha256": null
}
```

Exit: 1; timeout: False. Raw output: `commands/binding-unknown-version/stdout.txt`, `stderr.txt`.

## binding-wrong-root

```json
{
  "case": "binding-wrong-root",
  "argv": [
    "C:\\Program Files\\Python310\\python.exe",
    "-B",
    "-X",
    "utf8",
    "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z\\fixtures\\independent-01\\binding-wrong-root\\project\\.agents\\skills\\summary-skill\\scripts\\check_project_binding.py",
    "--project-root",
    "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z\\fixtures\\independent-01\\binding-wrong-root\\project",
    "--skill-root",
    "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z\\fixtures\\independent-01\\binding-wrong-root\\project\\.agents\\skills\\summary-skill"
  ],
  "cwd": "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z",
  "timeout_seconds": 120,
  "permitted_write_root": "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z",
  "expected": {
    "exit": 1,
    "field": "reason_code",
    "value": "ROOT_MISMATCH",
    "read_only_root": "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z\\fixtures\\independent-01\\binding-wrong-root\\project\\.agents\\skills\\summary-skill",
    "before_manifest": [
      {
        "path": "SKILL.md",
        "bytes": 330,
        "sha256": "ec46e875e5688b56f14e01f4e67a5fe15b55f29f71da3dd9d6b7a60817324b67"
      },
      {
        "path": "assets/devforgeai-skill.json",
        "bytes": 431,
        "sha256": "1dea9c740cf1d7a68219895ba9ad2a09b97b0c67ab7f807ad8fa92ebc178d6f4"
      },
      {
        "path": "references/adaptive-contract.md",
        "bytes": 297,
        "sha256": "ee1b190a764954b0dda1b9addc95f9112deda708fa558d7a90b64374ad7dbb58"
      },
      {
        "path": "scripts/check_project_binding.py",
        "bytes": 12232,
        "sha256": "688b1b7404133639a6f0f69c8fdb88670db230110ac7e8e24b64ccf32a24e241"
      }
    ]
  },
  "start_utc": "2026-09-13T15:50:43.114020+00:00",
  "stdin_sha256": null
}
```

Exit: 1; timeout: False. Raw output: `commands/binding-wrong-root/stdout.txt`, `stderr.txt`.

## codex-exec-help

```json
{
  "case": "codex-exec-help",
  "argv": [
    "codex",
    "exec",
    "--help"
  ],
  "cwd": "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z",
  "timeout_seconds": 120,
  "permitted_write_root": "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z",
  "expected": "Tool identification only; no acceptance claim",
  "start_utc": "2026-09-13T15:31:10.002749+00:00",
  "stdin_sha256": null
}
```

Exit: 0; timeout: False. Raw output: `commands/codex-exec-help/stdout.txt`, `stderr.txt`.

## codex-version

```json
{
  "case": "codex-version",
  "argv": [
    "codex",
    "--version"
  ],
  "cwd": "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z",
  "timeout_seconds": 120,
  "permitted_write_root": "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z",
  "expected": "Tool identification only; no acceptance claim",
  "start_utc": "2026-09-13T15:31:09.873814+00:00",
  "stdin_sha256": null
}
```

Exit: 0; timeout: False. Raw output: `commands/codex-version/stdout.txt`, `stderr.txt`.

## cold-create-01

```json
{
  "case": "cold-create-01",
  "argv": [
    "codex",
    "exec",
    "--cd",
    "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z\\native\\cold-create-01",
    "--sandbox",
    "workspace-write",
    "--skip-git-repo-check",
    "--ephemeral",
    "--json",
    "--output-last-message",
    "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z\\native\\cold-create-01\\.trial-output\\final.txt",
    "-"
  ],
  "cwd": "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z\\native\\cold-create-01",
  "timeout_seconds": 120,
  "permitted_write_root": "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z",
  "expected": "Package and digest-bound manual request, quality NOT_PERFORMED; no checker/test/validator process; no outside product effects",
  "start_utc": "2026-09-13T15:32:24.034860+00:00",
  "stdin_sha256": "a9bb491ee2afa187681e2b20272aab8d55c679b630ee08dccaf708ffb3454ce9"
}
```

Exit: 1; timeout: False. Raw output: `commands/cold-create-01/stdout.txt`, `stderr.txt`.

## cold-create-02

```json
{
  "case": "cold-create-02",
  "argv": [
    "codex",
    "exec",
    "--cd",
    "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z\\native\\cold-create-02",
    "--sandbox",
    "workspace-write",
    "--skip-git-repo-check",
    "--ephemeral",
    "--json",
    "--output-last-message",
    "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z\\native\\cold-create-02\\.trial-output\\final.txt",
    "-"
  ],
  "cwd": "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z\\native\\cold-create-02",
  "timeout_seconds": 120,
  "permitted_write_root": "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z",
  "expected": "Package and digest-bound manual request, quality NOT_PERFORMED; no checker/test/validator process; no outside product effects",
  "start_utc": "2026-09-13T15:46:00.990791+00:00",
  "stdin_sha256": "de68fb716834baea3ecf4d7b6125b3ae8d17f993152ef1af6d21b582cb4bca3d"
}
```

Exit: 1; timeout: True. Raw output: `commands/cold-create-02/stdout.txt`, `stderr.txt`.

## cold-propose-docs

```json
{
  "case": "cold-propose-docs",
  "argv": [
    "codex",
    "exec",
    "--cd",
    "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z\\native\\cold-propose-docs",
    "--sandbox",
    "workspace-write",
    "--skip-git-repo-check",
    "--ephemeral",
    "--json",
    "--output-last-message",
    "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z\\native\\cold-propose-docs\\.trial-output\\final.txt",
    "-"
  ],
  "cwd": "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z\\native\\cold-propose-docs",
  "timeout_seconds": 120,
  "permitted_write_root": "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z",
  "expected": "Cited fixture conventions and requirements; no invented tools or project execution; complete proposal/evidence or precise unresolved gaps; no skill packages",
  "start_utc": "2026-09-13T16:32:43.236855+00:00",
  "stdin_sha256": "274b3af4c0d834fdd9e9dea40d0e73130b8f0120723415f6bf1a2f57b7f8c097"
}
```

Exit: 1; timeout: True. Raw output: `commands/cold-propose-docs/stdout.txt`, `stderr.txt`.

## cold-propose-python

```json
{
  "case": "cold-propose-python",
  "argv": [
    "codex",
    "exec",
    "--cd",
    "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z\\native\\cold-propose-python",
    "--sandbox",
    "workspace-write",
    "--skip-git-repo-check",
    "--ephemeral",
    "--json",
    "--output-last-message",
    "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z\\native\\cold-propose-python\\.trial-output\\final.txt",
    "-"
  ],
  "cwd": "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z\\native\\cold-propose-python",
  "timeout_seconds": 120,
  "permitted_write_root": "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z",
  "expected": "Cited fixture conventions and requirements; no invented tools or project execution; complete proposal/evidence or precise unresolved gaps; no skill packages",
  "start_utc": "2026-09-13T16:20:01.522615+00:00",
  "stdin_sha256": "42b69e144bcd97b595eb1039b1ed41eb4434d46bec0be03d9d9c99bd076ba116"
}
```

Exit: 1; timeout: True. Raw output: `commands/cold-propose-python/stdout.txt`, `stderr.txt`.

## cold-propose-rust

```json
{
  "case": "cold-propose-rust",
  "argv": [
    "codex",
    "exec",
    "--cd",
    "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z\\native\\cold-propose-rust",
    "--sandbox",
    "workspace-write",
    "--skip-git-repo-check",
    "--ephemeral",
    "--json",
    "--output-last-message",
    "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z\\native\\cold-propose-rust\\.trial-output\\final.txt",
    "-"
  ],
  "cwd": "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z\\native\\cold-propose-rust",
  "timeout_seconds": 120,
  "permitted_write_root": "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z",
  "expected": "Cited fixture conventions and requirements; no invented tools or project execution; complete proposal/evidence or precise unresolved gaps; no skill packages",
  "start_utc": "2026-09-13T16:28:47.630101+00:00",
  "stdin_sha256": "b6d193cfdfbcdebf6dc6307c4f34bca27eab90721758b49e99e444e34d685229"
}
```

Exit: 1; timeout: True. Raw output: `commands/cold-propose-rust/stdout.txt`, `stderr.txt`.

## cold-propose-typescript

```json
{
  "case": "cold-propose-typescript",
  "argv": [
    "codex",
    "exec",
    "--cd",
    "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z\\native\\cold-propose-typescript",
    "--sandbox",
    "workspace-write",
    "--skip-git-repo-check",
    "--ephemeral",
    "--json",
    "--output-last-message",
    "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z\\native\\cold-propose-typescript\\.trial-output\\final.txt",
    "-"
  ],
  "cwd": "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z\\native\\cold-propose-typescript",
  "timeout_seconds": 120,
  "permitted_write_root": "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z",
  "expected": "Cited fixture conventions and requirements; no invented tools or project execution; complete proposal/evidence or precise unresolved gaps; no skill packages",
  "start_utc": "2026-09-13T16:29:33.480682+00:00",
  "stdin_sha256": "f107748893e0da9e440281b0eaf3b2ad925634f6ce884f97a302a84a15f7c036"
}
```

Exit: 1; timeout: True. Raw output: `commands/cold-propose-typescript/stdout.txt`, `stderr.txt`.

## coverage-json

```json
{
  "case": "coverage-json",
  "argv": [
    "python",
    "-B",
    "-X",
    "utf8",
    "-m",
    "coverage",
    "json",
    "--data-file=C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z\\coverage-data-02",
    "-o",
    "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z\\coverage.json"
  ],
  "cwd": "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z",
  "timeout_seconds": 120,
  "permitted_write_root": "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z",
  "expected": "Tool identification only; no acceptance claim",
  "start_utc": "2026-09-13T16:33:05.614834+00:00",
  "stdin_sha256": null
}
```

Exit: 0; timeout: False. Raw output: `commands/coverage-json/stdout.txt`, `stderr.txt`.

## coverage-version

```json
{
  "case": "coverage-version",
  "argv": [
    "python",
    "-B",
    "-X",
    "utf8",
    "-m",
    "coverage",
    "--version"
  ],
  "cwd": "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z",
  "timeout_seconds": 120,
  "permitted_write_root": "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z",
  "expected": "Tool identification only; no acceptance claim",
  "start_utc": "2026-09-13T16:25:15.729826+00:00",
  "stdin_sha256": null
}
```

Exit: 0; timeout: False. Raw output: `commands/coverage-version/stdout.txt`, `stderr.txt`.

## descriptor-valid

```json
{
  "case": "descriptor-valid",
  "argv": [
    "C:\\Program Files\\Python310\\python.exe",
    "-B",
    "-X",
    "utf8",
    "C:\\Projects\\DevForgeAI\\src\\agents\\skills\\skill-builder\\scripts\\adaptive.py",
    "inspect",
    "--record",
    "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z\\fixtures\\independent-01\\records\\source\\adaptive-one\\assets\\devforgeai-skill.json"
  ],
  "cwd": "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z",
  "timeout_seconds": 120,
  "permitted_write_root": "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z",
  "expected": {
    "exit": 0,
    "field": "status",
    "value": "VALID",
    "read_only_root": null,
    "before_manifest": null
  },
  "start_utc": "2026-09-13T15:51:07.408484+00:00",
  "stdin_sha256": null
}
```

Exit: 0; timeout: False. Raw output: `commands/descriptor-valid/stdout.txt`, `stderr.txt`.

## ext-initializer-new

```json
{
  "case": "ext-initializer-new",
  "argv": [
    "C:\\Program Files\\Python310\\python.exe",
    "-B",
    "-X",
    "utf8",
    "-m",
    "coverage",
    "run",
    "--append",
    "--branch",
    "--data-file=C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z\\coverage-data",
    "--source=C:\\Projects\\DevForgeAI\\src\\agents\\skills\\skill-builder",
    "C:\\Projects\\DevForgeAI\\src\\agents\\skills\\skill-builder\\scripts\\init_skill.py",
    "new-sample",
    "--path",
    "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z\\fixtures\\extended-03\\metadata"
  ],
  "cwd": "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z",
  "timeout_seconds": 120,
  "permitted_write_root": "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z",
  "expected": {
    "exit": 0,
    "field": null,
    "value": null,
    "read_only_root": null,
    "before_manifest": null
  },
  "start_utc": "2026-09-13T16:31:35.109833+00:00",
  "stdin_sha256": null
}
```

Exit: 1; timeout: False. Raw output: `commands/ext-initializer-new/stdout.txt`, `stderr.txt`.

## ext-initializer-occupied

```json
{
  "case": "ext-initializer-occupied",
  "argv": [
    "C:\\Program Files\\Python310\\python.exe",
    "-B",
    "-X",
    "utf8",
    "-m",
    "coverage",
    "run",
    "--append",
    "--branch",
    "--data-file=C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z\\coverage-data",
    "--source=C:\\Projects\\DevForgeAI\\src\\agents\\skills\\skill-builder",
    "C:\\Projects\\DevForgeAI\\src\\agents\\skills\\skill-builder\\scripts\\init_skill.py",
    "sample",
    "--path",
    "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z\\fixtures\\extended-03\\metadata"
  ],
  "cwd": "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z",
  "timeout_seconds": 120,
  "permitted_write_root": "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z",
  "expected": {
    "exit": 1,
    "field": null,
    "value": null,
    "read_only_root": null,
    "before_manifest": null
  },
  "start_utc": "2026-09-13T16:31:34.923465+00:00",
  "stdin_sha256": null
}
```

Exit: 1; timeout: False. Raw output: `commands/ext-initializer-occupied/stdout.txt`, `stderr.txt`.

## ext-legacy-adopted

```json
{
  "case": "ext-legacy-adopted",
  "argv": [
    "C:\\Program Files\\Python310\\python.exe",
    "-B",
    "-X",
    "utf8",
    "-m",
    "coverage",
    "run",
    "--append",
    "--branch",
    "--data-file=C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z\\coverage-data",
    "--source=C:\\Projects\\DevForgeAI\\src\\agents\\skills\\skill-builder",
    "C:\\Projects\\DevForgeAI\\src\\agents\\skills\\skill-builder\\scripts\\authoring.py",
    "begin",
    "--contract",
    "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z\\fixtures\\extended-03\\legacy-adopted\\contract.json",
    "--run-root",
    "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z\\fixtures\\extended-03\\legacy-adopted\\docs\\plan\\edit"
  ],
  "cwd": "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z",
  "timeout_seconds": 120,
  "permitted_write_root": "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z",
  "expected": {
    "exit": 0,
    "field": null,
    "value": null,
    "read_only_root": null,
    "before_manifest": null
  },
  "start_utc": "2026-09-13T16:31:33.300473+00:00",
  "stdin_sha256": null
}
```

Exit: 1; timeout: False. Raw output: `commands/ext-legacy-adopted/stdout.txt`, `stderr.txt`.

## ext-legacy-corrupt-generated

```json
{
  "case": "ext-legacy-corrupt-generated",
  "argv": [
    "C:\\Program Files\\Python310\\python.exe",
    "-B",
    "-X",
    "utf8",
    "-m",
    "coverage",
    "run",
    "--append",
    "--branch",
    "--data-file=C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z\\coverage-data",
    "--source=C:\\Projects\\DevForgeAI\\src\\agents\\skills\\skill-builder",
    "C:\\Projects\\DevForgeAI\\src\\agents\\skills\\skill-builder\\scripts\\authoring.py",
    "begin",
    "--contract",
    "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z\\fixtures\\extended-03\\legacy-corrupt-generated\\contract.json",
    "--run-root",
    "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z\\fixtures\\extended-03\\legacy-corrupt-generated\\docs\\plan\\edit"
  ],
  "cwd": "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z",
  "timeout_seconds": 120,
  "permitted_write_root": "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z",
  "expected": {
    "exit": 2,
    "field": null,
    "value": null,
    "read_only_root": null,
    "before_manifest": null
  },
  "start_utc": "2026-09-13T16:31:33.745892+00:00",
  "stdin_sha256": null
}
```

Exit: 1; timeout: False. Raw output: `commands/ext-legacy-corrupt-generated/stdout.txt`, `stderr.txt`.

## ext-legacy-generated

```json
{
  "case": "ext-legacy-generated",
  "argv": [
    "C:\\Program Files\\Python310\\python.exe",
    "-B",
    "-X",
    "utf8",
    "-m",
    "coverage",
    "run",
    "--append",
    "--branch",
    "--data-file=C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z\\coverage-data",
    "--source=C:\\Projects\\DevForgeAI\\src\\agents\\skills\\skill-builder",
    "C:\\Projects\\DevForgeAI\\src\\agents\\skills\\skill-builder\\scripts\\authoring.py",
    "begin",
    "--contract",
    "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z\\fixtures\\extended-03\\legacy-generated\\contract.json",
    "--run-root",
    "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z\\fixtures\\extended-03\\legacy-generated\\docs\\plan\\edit"
  ],
  "cwd": "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z",
  "timeout_seconds": 120,
  "permitted_write_root": "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z",
  "expected": {
    "exit": 0,
    "field": null,
    "value": null,
    "read_only_root": null,
    "before_manifest": null
  },
  "start_utc": "2026-09-13T16:31:33.082228+00:00",
  "stdin_sha256": null
}
```

Exit: 1; timeout: False. Raw output: `commands/ext-legacy-generated/stdout.txt`, `stderr.txt`.

## ext-legacy-wrong-pointer

```json
{
  "case": "ext-legacy-wrong-pointer",
  "argv": [
    "C:\\Program Files\\Python310\\python.exe",
    "-B",
    "-X",
    "utf8",
    "-m",
    "coverage",
    "run",
    "--append",
    "--branch",
    "--data-file=C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z\\coverage-data",
    "--source=C:\\Projects\\DevForgeAI\\src\\agents\\skills\\skill-builder",
    "C:\\Projects\\DevForgeAI\\src\\agents\\skills\\skill-builder\\scripts\\authoring.py",
    "begin",
    "--contract",
    "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z\\fixtures\\extended-03\\legacy-wrong-pointer\\contract.json",
    "--run-root",
    "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z\\fixtures\\extended-03\\legacy-wrong-pointer\\docs\\plan\\edit"
  ],
  "cwd": "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z",
  "timeout_seconds": 120,
  "permitted_write_root": "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z",
  "expected": {
    "exit": 2,
    "field": null,
    "value": null,
    "read_only_root": null,
    "before_manifest": null
  },
  "start_utc": "2026-09-13T16:31:33.521892+00:00",
  "stdin_sha256": null
}
```

Exit: 1; timeout: False. Raw output: `commands/ext-legacy-wrong-pointer/stdout.txt`, `stderr.txt`.

## ext-linked-kind

```json
{
  "case": "ext-linked-kind",
  "argv": [
    "C:\\Program Files\\Python310\\python.exe",
    "-B",
    "-X",
    "utf8",
    "-m",
    "coverage",
    "run",
    "--append",
    "--branch",
    "--data-file=C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z\\coverage-data",
    "--source=C:\\Projects\\DevForgeAI\\src\\agents\\skills\\skill-builder",
    "C:\\Projects\\DevForgeAI\\src\\agents\\skills\\skill-builder\\scripts\\adaptive.py",
    "inspect",
    "--record",
    "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z\\fixtures\\extended-03\\kind\\set.json"
  ],
  "cwd": "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z",
  "timeout_seconds": 120,
  "permitted_write_root": "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z",
  "expected": {
    "exit": 1,
    "field": "status",
    "value": "INVALID",
    "read_only_root": null,
    "before_manifest": null
  },
  "start_utc": "2026-09-13T16:31:32.307087+00:00",
  "stdin_sha256": null
}
```

Exit: 1; timeout: False. Raw output: `commands/ext-linked-kind/stdout.txt`, `stderr.txt`.

## ext-linked-quality

```json
{
  "case": "ext-linked-quality",
  "argv": [
    "C:\\Program Files\\Python310\\python.exe",
    "-B",
    "-X",
    "utf8",
    "-m",
    "coverage",
    "run",
    "--append",
    "--branch",
    "--data-file=C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z\\coverage-data",
    "--source=C:\\Projects\\DevForgeAI\\src\\agents\\skills\\skill-builder",
    "C:\\Projects\\DevForgeAI\\src\\agents\\skills\\skill-builder\\scripts\\adaptive.py",
    "inspect",
    "--record",
    "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z\\fixtures\\extended-03\\quality\\set.json"
  ],
  "cwd": "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z",
  "timeout_seconds": 120,
  "permitted_write_root": "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z",
  "expected": {
    "exit": 1,
    "field": "status",
    "value": "INVALID",
    "read_only_root": null,
    "before_manifest": null
  },
  "start_utc": "2026-09-13T16:31:32.120819+00:00",
  "stdin_sha256": null
}
```

Exit: 1; timeout: False. Raw output: `commands/ext-linked-quality/stdout.txt`, `stderr.txt`.

## ext-linked-request-identity

```json
{
  "case": "ext-linked-request-identity",
  "argv": [
    "C:\\Program Files\\Python310\\python.exe",
    "-B",
    "-X",
    "utf8",
    "-m",
    "coverage",
    "run",
    "--append",
    "--branch",
    "--data-file=C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z\\coverage-data",
    "--source=C:\\Projects\\DevForgeAI\\src\\agents\\skills\\skill-builder",
    "C:\\Projects\\DevForgeAI\\src\\agents\\skills\\skill-builder\\scripts\\adaptive.py",
    "inspect",
    "--record",
    "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z\\fixtures\\extended-03\\request-identity\\set.json"
  ],
  "cwd": "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z",
  "timeout_seconds": 120,
  "permitted_write_root": "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z",
  "expected": {
    "exit": 1,
    "field": "status",
    "value": "INVALID",
    "read_only_root": null,
    "before_manifest": null
  },
  "start_utc": "2026-09-13T16:31:32.490276+00:00",
  "stdin_sha256": null
}
```

Exit: 1; timeout: False. Raw output: `commands/ext-linked-request-identity/stdout.txt`, `stderr.txt`.

## ext-linked-request-manifest

```json
{
  "case": "ext-linked-request-manifest",
  "argv": [
    "C:\\Program Files\\Python310\\python.exe",
    "-B",
    "-X",
    "utf8",
    "-m",
    "coverage",
    "run",
    "--append",
    "--branch",
    "--data-file=C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z\\coverage-data",
    "--source=C:\\Projects\\DevForgeAI\\src\\agents\\skills\\skill-builder",
    "C:\\Projects\\DevForgeAI\\src\\agents\\skills\\skill-builder\\scripts\\adaptive.py",
    "inspect",
    "--record",
    "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z\\fixtures\\extended-03\\request-manifest\\set.json"
  ],
  "cwd": "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z",
  "timeout_seconds": 120,
  "permitted_write_root": "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z",
  "expected": {
    "exit": 1,
    "field": "status",
    "value": "INVALID",
    "read_only_root": null,
    "before_manifest": null
  },
  "start_utc": "2026-09-13T16:31:32.888939+00:00",
  "stdin_sha256": null
}
```

Exit: 1; timeout: False. Raw output: `commands/ext-linked-request-manifest/stdout.txt`, `stderr.txt`.

## ext-linked-request-type

```json
{
  "case": "ext-linked-request-type",
  "argv": [
    "C:\\Program Files\\Python310\\python.exe",
    "-B",
    "-X",
    "utf8",
    "-m",
    "coverage",
    "run",
    "--append",
    "--branch",
    "--data-file=C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z\\coverage-data",
    "--source=C:\\Projects\\DevForgeAI\\src\\agents\\skills\\skill-builder",
    "C:\\Projects\\DevForgeAI\\src\\agents\\skills\\skill-builder\\scripts\\adaptive.py",
    "inspect",
    "--record",
    "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z\\fixtures\\extended-03\\request-type\\set.json"
  ],
  "cwd": "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z",
  "timeout_seconds": 120,
  "permitted_write_root": "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z",
  "expected": {
    "exit": 1,
    "field": "status",
    "value": "INVALID",
    "read_only_root": null,
    "before_manifest": null
  },
  "start_utc": "2026-09-13T16:31:32.690153+00:00",
  "stdin_sha256": null
}
```

Exit: 1; timeout: False. Raw output: `commands/ext-linked-request-type/stdout.txt`, `stderr.txt`.

## ext-linked-valid

```json
{
  "case": "ext-linked-valid",
  "argv": [
    "C:\\Program Files\\Python310\\python.exe",
    "-B",
    "-X",
    "utf8",
    "-m",
    "coverage",
    "run",
    "--append",
    "--branch",
    "--data-file=C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z\\coverage-data",
    "--source=C:\\Projects\\DevForgeAI\\src\\agents\\skills\\skill-builder",
    "C:\\Projects\\DevForgeAI\\src\\agents\\skills\\skill-builder\\scripts\\adaptive.py",
    "inspect",
    "--record",
    "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z\\fixtures\\extended-03\\valid\\set.json"
  ],
  "cwd": "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z",
  "timeout_seconds": 120,
  "permitted_write_root": "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z",
  "expected": {
    "exit": 0,
    "field": "status",
    "value": "VALID",
    "read_only_root": null,
    "before_manifest": null
  },
  "start_utc": "2026-09-13T16:31:31.912754+00:00",
  "stdin_sha256": null
}
```

Exit: 1; timeout: False. Raw output: `commands/ext-linked-valid/stdout.txt`, `stderr.txt`.

## ext-metadata-preserve

```json
{
  "case": "ext-metadata-preserve",
  "argv": [
    "C:\\Program Files\\Python310\\python.exe",
    "-B",
    "-X",
    "utf8",
    "-m",
    "coverage",
    "run",
    "--append",
    "--branch",
    "--data-file=C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z\\coverage-data",
    "--source=C:\\Projects\\DevForgeAI\\src\\agents\\skills\\skill-builder",
    "C:\\Projects\\DevForgeAI\\src\\agents\\skills\\skill-builder\\scripts\\generate_openai_yaml.py",
    "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z\\fixtures\\extended-03\\metadata\\sample",
    "--interface",
    "display_name=Changed"
  ],
  "cwd": "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z",
  "timeout_seconds": 120,
  "permitted_write_root": "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z",
  "expected": {
    "exit": 0,
    "field": null,
    "value": null,
    "read_only_root": null,
    "before_manifest": null
  },
  "start_utc": "2026-09-13T16:31:34.723460+00:00",
  "stdin_sha256": null
}
```

Exit: 1; timeout: False. Raw output: `commands/ext-metadata-preserve/stdout.txt`, `stderr.txt`.

## ext-spec-ambiguous

```json
{
  "case": "ext-spec-ambiguous",
  "argv": [
    "C:\\Program Files\\Python310\\python.exe",
    "-B",
    "-X",
    "utf8",
    "-m",
    "coverage",
    "run",
    "--append",
    "--branch",
    "--data-file=C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z\\coverage-data",
    "--source=C:\\Projects\\DevForgeAI\\src\\agents\\skills\\skill-builder",
    "C:\\Projects\\DevForgeAI\\src\\agents\\skills\\skill-builder\\scripts\\build_evidence.py",
    "resolve-spec",
    "--project-root",
    "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z\\fixtures\\extended-03\\resolver",
    "--name",
    "requested"
  ],
  "cwd": "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z",
  "timeout_seconds": 120,
  "permitted_write_root": "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z",
  "expected": {
    "exit": 1,
    "field": "reason_code",
    "value": "AMBIGUOUS_INPUT",
    "read_only_root": null,
    "before_manifest": null
  },
  "start_utc": "2026-09-13T16:31:35.296203+00:00",
  "stdin_sha256": null
}
```

Exit: 1; timeout: False. Raw output: `commands/ext-spec-ambiguous/stdout.txt`, `stderr.txt`.

## ext-spec-explicit

```json
{
  "case": "ext-spec-explicit",
  "argv": [
    "C:\\Program Files\\Python310\\python.exe",
    "-B",
    "-X",
    "utf8",
    "-m",
    "coverage",
    "run",
    "--append",
    "--branch",
    "--data-file=C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z\\coverage-data",
    "--source=C:\\Projects\\DevForgeAI\\src\\agents\\skills\\skill-builder",
    "C:\\Projects\\DevForgeAI\\src\\agents\\skills\\skill-builder\\scripts\\build_evidence.py",
    "resolve-spec",
    "--project-root",
    "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z\\fixtures\\extended-03\\resolver",
    "--spec",
    "docs/plan/one.md"
  ],
  "cwd": "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z",
  "timeout_seconds": 120,
  "permitted_write_root": "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z",
  "expected": {
    "exit": 0,
    "field": "status",
    "value": "RESOLVED",
    "read_only_root": null,
    "before_manifest": null
  },
  "start_utc": "2026-09-13T16:31:35.525744+00:00",
  "stdin_sha256": null
}
```

Exit: 0; timeout: False. Raw output: `commands/ext-spec-explicit/stdout.txt`, `stderr.txt`.

## ext-update-equivalent-bytes

```json
{
  "case": "ext-update-equivalent-bytes",
  "argv": [
    "C:\\Program Files\\Python310\\python.exe",
    "-B",
    "-X",
    "utf8",
    "-m",
    "coverage",
    "run",
    "--append",
    "--branch",
    "--data-file=C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z\\coverage-data",
    "--source=C:\\Projects\\DevForgeAI\\src\\agents\\skills\\skill-builder",
    "C:\\Projects\\DevForgeAI\\src\\agents\\skills\\skill-builder\\scripts\\adaptive.py",
    "inspect",
    "--record",
    "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z\\fixtures\\extended-03\\updates\\equivalent.json"
  ],
  "cwd": "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z",
  "timeout_seconds": 120,
  "permitted_write_root": "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z",
  "expected": {
    "exit": 0,
    "field": "status",
    "value": "VALID",
    "read_only_root": null,
    "before_manifest": null
  },
  "start_utc": "2026-09-13T16:31:34.167931+00:00",
  "stdin_sha256": null
}
```

Exit: 1; timeout: False. Raw output: `commands/ext-update-equivalent-bytes/stdout.txt`, `stderr.txt`.

## ext-update-false-no-change

```json
{
  "case": "ext-update-false-no-change",
  "argv": [
    "C:\\Program Files\\Python310\\python.exe",
    "-B",
    "-X",
    "utf8",
    "-m",
    "coverage",
    "run",
    "--append",
    "--branch",
    "--data-file=C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z\\coverage-data",
    "--source=C:\\Projects\\DevForgeAI\\src\\agents\\skills\\skill-builder",
    "C:\\Projects\\DevForgeAI\\src\\agents\\skills\\skill-builder\\scripts\\adaptive.py",
    "inspect",
    "--record",
    "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z\\fixtures\\extended-03\\updates\\false-unchanged.json"
  ],
  "cwd": "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z",
  "timeout_seconds": 120,
  "permitted_write_root": "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z",
  "expected": {
    "exit": 1,
    "field": "status",
    "value": "INVALID",
    "read_only_root": null,
    "before_manifest": null
  },
  "start_utc": "2026-09-13T16:31:34.353931+00:00",
  "stdin_sha256": null
}
```

Exit: 1; timeout: False. Raw output: `commands/ext-update-false-no-change/stdout.txt`, `stderr.txt`.

## ext-update-missing-history

```json
{
  "case": "ext-update-missing-history",
  "argv": [
    "C:\\Program Files\\Python310\\python.exe",
    "-B",
    "-X",
    "utf8",
    "-m",
    "coverage",
    "run",
    "--append",
    "--branch",
    "--data-file=C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z\\coverage-data",
    "--source=C:\\Projects\\DevForgeAI\\src\\agents\\skills\\skill-builder",
    "C:\\Projects\\DevForgeAI\\src\\agents\\skills\\skill-builder\\scripts\\adaptive.py",
    "inspect",
    "--record",
    "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z\\fixtures\\extended-03\\updates\\missing.json"
  ],
  "cwd": "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z",
  "timeout_seconds": 120,
  "permitted_write_root": "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z",
  "expected": {
    "exit": 1,
    "field": "status",
    "value": "INVALID",
    "read_only_root": null,
    "before_manifest": null
  },
  "start_utc": "2026-09-13T16:31:34.538443+00:00",
  "stdin_sha256": null
}
```

Exit: 1; timeout: False. Raw output: `commands/ext-update-missing-history/stdout.txt`, `stderr.txt`.

## ext-update-unchanged

```json
{
  "case": "ext-update-unchanged",
  "argv": [
    "C:\\Program Files\\Python310\\python.exe",
    "-B",
    "-X",
    "utf8",
    "-m",
    "coverage",
    "run",
    "--append",
    "--branch",
    "--data-file=C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z\\coverage-data",
    "--source=C:\\Projects\\DevForgeAI\\src\\agents\\skills\\skill-builder",
    "C:\\Projects\\DevForgeAI\\src\\agents\\skills\\skill-builder\\scripts\\adaptive.py",
    "inspect",
    "--record",
    "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z\\fixtures\\extended-03\\updates\\unchanged.json"
  ],
  "cwd": "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z",
  "timeout_seconds": 120,
  "permitted_write_root": "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z",
  "expected": {
    "exit": 0,
    "field": "status",
    "value": "VALID",
    "read_only_root": null,
    "before_manifest": null
  },
  "start_utc": "2026-09-13T16:31:33.978415+00:00",
  "stdin_sha256": null
}
```

Exit: 1; timeout: False. Raw output: `commands/ext-update-unchanged/stdout.txt`, `stderr.txt`.

## ext2-initializer-new

```json
{
  "case": "ext2-initializer-new",
  "argv": [
    "C:\\Program Files\\Python310\\python.exe",
    "-B",
    "-X",
    "utf8",
    "-m",
    "coverage",
    "run",
    "--append",
    "--branch",
    "--data-file=C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z\\coverage-data-02",
    "--source=C:\\Projects\\DevForgeAI\\src\\agents\\skills\\skill-builder",
    "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z\\coverage_driver.py",
    "C:\\Projects\\DevForgeAI\\src\\agents\\skills\\skill-builder\\scripts\\init_skill.py",
    "new-sample",
    "--path",
    "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z\\fixtures\\extended-04\\metadata"
  ],
  "cwd": "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z",
  "timeout_seconds": 120,
  "permitted_write_root": "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z",
  "expected": {
    "exit": 0,
    "field": null,
    "value": null,
    "read_only_root": null,
    "before_manifest": null
  },
  "start_utc": "2026-09-13T16:32:42.259394+00:00",
  "stdin_sha256": null
}
```

Exit: 0; timeout: False. Raw output: `commands/ext2-initializer-new/stdout.txt`, `stderr.txt`.

## ext2-initializer-occupied

```json
{
  "case": "ext2-initializer-occupied",
  "argv": [
    "C:\\Program Files\\Python310\\python.exe",
    "-B",
    "-X",
    "utf8",
    "-m",
    "coverage",
    "run",
    "--append",
    "--branch",
    "--data-file=C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z\\coverage-data-02",
    "--source=C:\\Projects\\DevForgeAI\\src\\agents\\skills\\skill-builder",
    "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z\\coverage_driver.py",
    "C:\\Projects\\DevForgeAI\\src\\agents\\skills\\skill-builder\\scripts\\init_skill.py",
    "sample",
    "--path",
    "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z\\fixtures\\extended-04\\metadata"
  ],
  "cwd": "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z",
  "timeout_seconds": 120,
  "permitted_write_root": "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z",
  "expected": {
    "exit": 1,
    "field": null,
    "value": null,
    "read_only_root": null,
    "before_manifest": null
  },
  "start_utc": "2026-09-13T16:32:42.065375+00:00",
  "stdin_sha256": null
}
```

Exit: 1; timeout: False. Raw output: `commands/ext2-initializer-occupied/stdout.txt`, `stderr.txt`.

## ext2-legacy-adopted

```json
{
  "case": "ext2-legacy-adopted",
  "argv": [
    "C:\\Program Files\\Python310\\python.exe",
    "-B",
    "-X",
    "utf8",
    "-m",
    "coverage",
    "run",
    "--append",
    "--branch",
    "--data-file=C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z\\coverage-data-02",
    "--source=C:\\Projects\\DevForgeAI\\src\\agents\\skills\\skill-builder",
    "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z\\coverage_driver.py",
    "C:\\Projects\\DevForgeAI\\src\\agents\\skills\\skill-builder\\scripts\\authoring.py",
    "begin",
    "--contract",
    "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z\\fixtures\\extended-04\\legacy-adopted\\contract.json",
    "--run-root",
    "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z\\fixtures\\extended-04\\legacy-adopted\\docs\\plan\\edit"
  ],
  "cwd": "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z",
  "timeout_seconds": 120,
  "permitted_write_root": "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z",
  "expected": {
    "exit": 0,
    "field": null,
    "value": null,
    "read_only_root": null,
    "before_manifest": null
  },
  "start_utc": "2026-09-13T16:32:39.004201+00:00",
  "stdin_sha256": null
}
```

Exit: 0; timeout: False. Raw output: `commands/ext2-legacy-adopted/stdout.txt`, `stderr.txt`.

## ext2-legacy-corrupt-generated

```json
{
  "case": "ext2-legacy-corrupt-generated",
  "argv": [
    "C:\\Program Files\\Python310\\python.exe",
    "-B",
    "-X",
    "utf8",
    "-m",
    "coverage",
    "run",
    "--append",
    "--branch",
    "--data-file=C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z\\coverage-data-02",
    "--source=C:\\Projects\\DevForgeAI\\src\\agents\\skills\\skill-builder",
    "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z\\coverage_driver.py",
    "C:\\Projects\\DevForgeAI\\src\\agents\\skills\\skill-builder\\scripts\\authoring.py",
    "begin",
    "--contract",
    "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z\\fixtures\\extended-04\\legacy-corrupt-generated\\contract.json",
    "--run-root",
    "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z\\fixtures\\extended-04\\legacy-corrupt-generated\\docs\\plan\\edit"
  ],
  "cwd": "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z",
  "timeout_seconds": 120,
  "permitted_write_root": "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z",
  "expected": {
    "exit": 2,
    "field": null,
    "value": null,
    "read_only_root": null,
    "before_manifest": null
  },
  "start_utc": "2026-09-13T16:32:39.687163+00:00",
  "stdin_sha256": null
}
```

Exit: 2; timeout: False. Raw output: `commands/ext2-legacy-corrupt-generated/stdout.txt`, `stderr.txt`.

## ext2-legacy-generated

```json
{
  "case": "ext2-legacy-generated",
  "argv": [
    "C:\\Program Files\\Python310\\python.exe",
    "-B",
    "-X",
    "utf8",
    "-m",
    "coverage",
    "run",
    "--append",
    "--branch",
    "--data-file=C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z\\coverage-data-02",
    "--source=C:\\Projects\\DevForgeAI\\src\\agents\\skills\\skill-builder",
    "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z\\coverage_driver.py",
    "C:\\Projects\\DevForgeAI\\src\\agents\\skills\\skill-builder\\scripts\\authoring.py",
    "begin",
    "--contract",
    "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z\\fixtures\\extended-04\\legacy-generated\\contract.json",
    "--run-root",
    "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z\\fixtures\\extended-04\\legacy-generated\\docs\\plan\\edit"
  ],
  "cwd": "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z",
  "timeout_seconds": 120,
  "permitted_write_root": "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z",
  "expected": {
    "exit": 0,
    "field": null,
    "value": null,
    "read_only_root": null,
    "before_manifest": null
  },
  "start_utc": "2026-09-13T16:32:38.678992+00:00",
  "stdin_sha256": null
}
```

Exit: 0; timeout: False. Raw output: `commands/ext2-legacy-generated/stdout.txt`, `stderr.txt`.

## ext2-legacy-wrong-pointer

```json
{
  "case": "ext2-legacy-wrong-pointer",
  "argv": [
    "C:\\Program Files\\Python310\\python.exe",
    "-B",
    "-X",
    "utf8",
    "-m",
    "coverage",
    "run",
    "--append",
    "--branch",
    "--data-file=C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z\\coverage-data-02",
    "--source=C:\\Projects\\DevForgeAI\\src\\agents\\skills\\skill-builder",
    "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z\\coverage_driver.py",
    "C:\\Projects\\DevForgeAI\\src\\agents\\skills\\skill-builder\\scripts\\authoring.py",
    "begin",
    "--contract",
    "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z\\fixtures\\extended-04\\legacy-wrong-pointer\\contract.json",
    "--run-root",
    "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z\\fixtures\\extended-04\\legacy-wrong-pointer\\docs\\plan\\edit"
  ],
  "cwd": "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z",
  "timeout_seconds": 120,
  "permitted_write_root": "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z",
  "expected": {
    "exit": 2,
    "field": null,
    "value": null,
    "read_only_root": null,
    "before_manifest": null
  },
  "start_utc": "2026-09-13T16:32:39.347382+00:00",
  "stdin_sha256": null
}
```

Exit: 0; timeout: False. Raw output: `commands/ext2-legacy-wrong-pointer/stdout.txt`, `stderr.txt`.

## ext2-linked-kind

```json
{
  "case": "ext2-linked-kind",
  "argv": [
    "C:\\Program Files\\Python310\\python.exe",
    "-B",
    "-X",
    "utf8",
    "-m",
    "coverage",
    "run",
    "--append",
    "--branch",
    "--data-file=C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z\\coverage-data-02",
    "--source=C:\\Projects\\DevForgeAI\\src\\agents\\skills\\skill-builder",
    "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z\\coverage_driver.py",
    "C:\\Projects\\DevForgeAI\\src\\agents\\skills\\skill-builder\\scripts\\adaptive.py",
    "inspect",
    "--record",
    "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z\\fixtures\\extended-04\\kind\\set.json"
  ],
  "cwd": "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z",
  "timeout_seconds": 120,
  "permitted_write_root": "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z",
  "expected": {
    "exit": 1,
    "field": "status",
    "value": "INVALID",
    "read_only_root": null,
    "before_manifest": null
  },
  "start_utc": "2026-09-13T16:32:36.146415+00:00",
  "stdin_sha256": null
}
```

Exit: 0; timeout: False. Raw output: `commands/ext2-linked-kind/stdout.txt`, `stderr.txt`.

## ext2-linked-quality

```json
{
  "case": "ext2-linked-quality",
  "argv": [
    "C:\\Program Files\\Python310\\python.exe",
    "-B",
    "-X",
    "utf8",
    "-m",
    "coverage",
    "run",
    "--append",
    "--branch",
    "--data-file=C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z\\coverage-data-02",
    "--source=C:\\Projects\\DevForgeAI\\src\\agents\\skills\\skill-builder",
    "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z\\coverage_driver.py",
    "C:\\Projects\\DevForgeAI\\src\\agents\\skills\\skill-builder\\scripts\\adaptive.py",
    "inspect",
    "--record",
    "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z\\fixtures\\extended-04\\quality\\set.json"
  ],
  "cwd": "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z",
  "timeout_seconds": 120,
  "permitted_write_root": "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z",
  "expected": {
    "exit": 1,
    "field": "status",
    "value": "INVALID",
    "read_only_root": null,
    "before_manifest": null
  },
  "start_utc": "2026-09-13T16:32:35.512014+00:00",
  "stdin_sha256": null
}
```

Exit: 0; timeout: False. Raw output: `commands/ext2-linked-quality/stdout.txt`, `stderr.txt`.

## ext2-linked-request-identity

```json
{
  "case": "ext2-linked-request-identity",
  "argv": [
    "C:\\Program Files\\Python310\\python.exe",
    "-B",
    "-X",
    "utf8",
    "-m",
    "coverage",
    "run",
    "--append",
    "--branch",
    "--data-file=C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z\\coverage-data-02",
    "--source=C:\\Projects\\DevForgeAI\\src\\agents\\skills\\skill-builder",
    "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z\\coverage_driver.py",
    "C:\\Projects\\DevForgeAI\\src\\agents\\skills\\skill-builder\\scripts\\adaptive.py",
    "inspect",
    "--record",
    "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z\\fixtures\\extended-04\\request-identity\\set.json"
  ],
  "cwd": "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z",
  "timeout_seconds": 120,
  "permitted_write_root": "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z",
  "expected": {
    "exit": 1,
    "field": "status",
    "value": "INVALID",
    "read_only_root": null,
    "before_manifest": null
  },
  "start_utc": "2026-09-13T16:32:36.781600+00:00",
  "stdin_sha256": null
}
```

Exit: 0; timeout: False. Raw output: `commands/ext2-linked-request-identity/stdout.txt`, `stderr.txt`.

## ext2-linked-request-manifest

```json
{
  "case": "ext2-linked-request-manifest",
  "argv": [
    "C:\\Program Files\\Python310\\python.exe",
    "-B",
    "-X",
    "utf8",
    "-m",
    "coverage",
    "run",
    "--append",
    "--branch",
    "--data-file=C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z\\coverage-data-02",
    "--source=C:\\Projects\\DevForgeAI\\src\\agents\\skills\\skill-builder",
    "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z\\coverage_driver.py",
    "C:\\Projects\\DevForgeAI\\src\\agents\\skills\\skill-builder\\scripts\\adaptive.py",
    "inspect",
    "--record",
    "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z\\fixtures\\extended-04\\request-manifest\\set.json"
  ],
  "cwd": "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z",
  "timeout_seconds": 120,
  "permitted_write_root": "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z",
  "expected": {
    "exit": 1,
    "field": "status",
    "value": "INVALID",
    "read_only_root": null,
    "before_manifest": null
  },
  "start_utc": "2026-09-13T16:32:38.042521+00:00",
  "stdin_sha256": null
}
```

Exit: 0; timeout: False. Raw output: `commands/ext2-linked-request-manifest/stdout.txt`, `stderr.txt`.

## ext2-linked-request-type

```json
{
  "case": "ext2-linked-request-type",
  "argv": [
    "C:\\Program Files\\Python310\\python.exe",
    "-B",
    "-X",
    "utf8",
    "-m",
    "coverage",
    "run",
    "--append",
    "--branch",
    "--data-file=C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z\\coverage-data-02",
    "--source=C:\\Projects\\DevForgeAI\\src\\agents\\skills\\skill-builder",
    "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z\\coverage_driver.py",
    "C:\\Projects\\DevForgeAI\\src\\agents\\skills\\skill-builder\\scripts\\adaptive.py",
    "inspect",
    "--record",
    "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z\\fixtures\\extended-04\\request-type\\set.json"
  ],
  "cwd": "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z",
  "timeout_seconds": 120,
  "permitted_write_root": "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z",
  "expected": {
    "exit": 1,
    "field": "status",
    "value": "INVALID",
    "read_only_root": null,
    "before_manifest": null
  },
  "start_utc": "2026-09-13T16:32:37.412677+00:00",
  "stdin_sha256": null
}
```

Exit: 0; timeout: False. Raw output: `commands/ext2-linked-request-type/stdout.txt`, `stderr.txt`.

## ext2-linked-valid

```json
{
  "case": "ext2-linked-valid",
  "argv": [
    "C:\\Program Files\\Python310\\python.exe",
    "-B",
    "-X",
    "utf8",
    "-m",
    "coverage",
    "run",
    "--append",
    "--branch",
    "--data-file=C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z\\coverage-data-02",
    "--source=C:\\Projects\\DevForgeAI\\src\\agents\\skills\\skill-builder",
    "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z\\coverage_driver.py",
    "C:\\Projects\\DevForgeAI\\src\\agents\\skills\\skill-builder\\scripts\\adaptive.py",
    "inspect",
    "--record",
    "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z\\fixtures\\extended-04\\valid\\set.json"
  ],
  "cwd": "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z",
  "timeout_seconds": 120,
  "permitted_write_root": "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z",
  "expected": {
    "exit": 0,
    "field": "status",
    "value": "VALID",
    "read_only_root": null,
    "before_manifest": null
  },
  "start_utc": "2026-09-13T16:32:34.871733+00:00",
  "stdin_sha256": null
}
```

Exit: 0; timeout: False. Raw output: `commands/ext2-linked-valid/stdout.txt`, `stderr.txt`.

## ext2-metadata-preserve

```json
{
  "case": "ext2-metadata-preserve",
  "argv": [
    "C:\\Program Files\\Python310\\python.exe",
    "-B",
    "-X",
    "utf8",
    "-m",
    "coverage",
    "run",
    "--append",
    "--branch",
    "--data-file=C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z\\coverage-data-02",
    "--source=C:\\Projects\\DevForgeAI\\src\\agents\\skills\\skill-builder",
    "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z\\coverage_driver.py",
    "C:\\Projects\\DevForgeAI\\src\\agents\\skills\\skill-builder\\scripts\\generate_openai_yaml.py",
    "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z\\fixtures\\extended-04\\metadata\\sample",
    "--interface",
    "display_name=Changed"
  ],
  "cwd": "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z",
  "timeout_seconds": 120,
  "permitted_write_root": "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z",
  "expected": {
    "exit": 0,
    "field": null,
    "value": null,
    "read_only_root": null,
    "before_manifest": null
  },
  "start_utc": "2026-09-13T16:32:41.822982+00:00",
  "stdin_sha256": null
}
```

Exit: 0; timeout: False. Raw output: `commands/ext2-metadata-preserve/stdout.txt`, `stderr.txt`.

## ext2-spec-ambiguous

```json
{
  "case": "ext2-spec-ambiguous",
  "argv": [
    "C:\\Program Files\\Python310\\python.exe",
    "-B",
    "-X",
    "utf8",
    "-m",
    "coverage",
    "run",
    "--append",
    "--branch",
    "--data-file=C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z\\coverage-data-02",
    "--source=C:\\Projects\\DevForgeAI\\src\\agents\\skills\\skill-builder",
    "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z\\coverage_driver.py",
    "C:\\Projects\\DevForgeAI\\src\\agents\\skills\\skill-builder\\scripts\\build_evidence.py",
    "resolve-spec",
    "--project-root",
    "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z\\fixtures\\extended-04\\resolver",
    "--name",
    "requested"
  ],
  "cwd": "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z",
  "timeout_seconds": 120,
  "permitted_write_root": "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z",
  "expected": {
    "exit": 1,
    "field": "reason_code",
    "value": "AMBIGUOUS_INPUT",
    "read_only_root": null,
    "before_manifest": null
  },
  "start_utc": "2026-09-13T16:32:42.457536+00:00",
  "stdin_sha256": null
}
```

Exit: 1; timeout: False. Raw output: `commands/ext2-spec-ambiguous/stdout.txt`, `stderr.txt`.

## ext2-spec-explicit

```json
{
  "case": "ext2-spec-explicit",
  "argv": [
    "C:\\Program Files\\Python310\\python.exe",
    "-B",
    "-X",
    "utf8",
    "-m",
    "coverage",
    "run",
    "--append",
    "--branch",
    "--data-file=C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z\\coverage-data-02",
    "--source=C:\\Projects\\DevForgeAI\\src\\agents\\skills\\skill-builder",
    "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z\\coverage_driver.py",
    "C:\\Projects\\DevForgeAI\\src\\agents\\skills\\skill-builder\\scripts\\build_evidence.py",
    "resolve-spec",
    "--project-root",
    "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z\\fixtures\\extended-04\\resolver",
    "--spec",
    "docs/plan/one.md"
  ],
  "cwd": "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z",
  "timeout_seconds": 120,
  "permitted_write_root": "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z",
  "expected": {
    "exit": 0,
    "field": "status",
    "value": "RESOLVED",
    "read_only_root": null,
    "before_manifest": null
  },
  "start_utc": "2026-09-13T16:32:42.673770+00:00",
  "stdin_sha256": null
}
```

Exit: 0; timeout: False. Raw output: `commands/ext2-spec-explicit/stdout.txt`, `stderr.txt`.

## ext2-update-equivalent-bytes

```json
{
  "case": "ext2-update-equivalent-bytes",
  "argv": [
    "C:\\Program Files\\Python310\\python.exe",
    "-B",
    "-X",
    "utf8",
    "-m",
    "coverage",
    "run",
    "--append",
    "--branch",
    "--data-file=C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z\\coverage-data-02",
    "--source=C:\\Projects\\DevForgeAI\\src\\agents\\skills\\skill-builder",
    "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z\\coverage_driver.py",
    "C:\\Projects\\DevForgeAI\\src\\agents\\skills\\skill-builder\\scripts\\adaptive.py",
    "inspect",
    "--record",
    "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z\\fixtures\\extended-04\\updates\\equivalent.json"
  ],
  "cwd": "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z",
  "timeout_seconds": 120,
  "permitted_write_root": "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z",
  "expected": {
    "exit": 0,
    "field": "status",
    "value": "VALID",
    "read_only_root": null,
    "before_manifest": null
  },
  "start_utc": "2026-09-13T16:32:40.511170+00:00",
  "stdin_sha256": null
}
```

Exit: 0; timeout: False. Raw output: `commands/ext2-update-equivalent-bytes/stdout.txt`, `stderr.txt`.

## ext2-update-false-no-change

```json
{
  "case": "ext2-update-false-no-change",
  "argv": [
    "C:\\Program Files\\Python310\\python.exe",
    "-B",
    "-X",
    "utf8",
    "-m",
    "coverage",
    "run",
    "--append",
    "--branch",
    "--data-file=C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z\\coverage-data-02",
    "--source=C:\\Projects\\DevForgeAI\\src\\agents\\skills\\skill-builder",
    "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z\\coverage_driver.py",
    "C:\\Projects\\DevForgeAI\\src\\agents\\skills\\skill-builder\\scripts\\adaptive.py",
    "inspect",
    "--record",
    "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z\\fixtures\\extended-04\\updates\\false-unchanged.json"
  ],
  "cwd": "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z",
  "timeout_seconds": 120,
  "permitted_write_root": "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z",
  "expected": {
    "exit": 1,
    "field": "status",
    "value": "INVALID",
    "read_only_root": null,
    "before_manifest": null
  },
  "start_utc": "2026-09-13T16:32:41.094513+00:00",
  "stdin_sha256": null
}
```

Exit: 1; timeout: False. Raw output: `commands/ext2-update-false-no-change/stdout.txt`, `stderr.txt`.

## ext2-update-missing-history

```json
{
  "case": "ext2-update-missing-history",
  "argv": [
    "C:\\Program Files\\Python310\\python.exe",
    "-B",
    "-X",
    "utf8",
    "-m",
    "coverage",
    "run",
    "--append",
    "--branch",
    "--data-file=C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z\\coverage-data-02",
    "--source=C:\\Projects\\DevForgeAI\\src\\agents\\skills\\skill-builder",
    "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z\\coverage_driver.py",
    "C:\\Projects\\DevForgeAI\\src\\agents\\skills\\skill-builder\\scripts\\adaptive.py",
    "inspect",
    "--record",
    "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z\\fixtures\\extended-04\\updates\\missing.json"
  ],
  "cwd": "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z",
  "timeout_seconds": 120,
  "permitted_write_root": "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z",
  "expected": {
    "exit": 1,
    "field": "status",
    "value": "INVALID",
    "read_only_root": null,
    "before_manifest": null
  },
  "start_utc": "2026-09-13T16:32:41.578922+00:00",
  "stdin_sha256": null
}
```

Exit: 1; timeout: False. Raw output: `commands/ext2-update-missing-history/stdout.txt`, `stderr.txt`.

## ext2-update-unchanged

```json
{
  "case": "ext2-update-unchanged",
  "argv": [
    "C:\\Program Files\\Python310\\python.exe",
    "-B",
    "-X",
    "utf8",
    "-m",
    "coverage",
    "run",
    "--append",
    "--branch",
    "--data-file=C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z\\coverage-data-02",
    "--source=C:\\Projects\\DevForgeAI\\src\\agents\\skills\\skill-builder",
    "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z\\coverage_driver.py",
    "C:\\Projects\\DevForgeAI\\src\\agents\\skills\\skill-builder\\scripts\\adaptive.py",
    "inspect",
    "--record",
    "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z\\fixtures\\extended-04\\updates\\unchanged.json"
  ],
  "cwd": "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z",
  "timeout_seconds": 120,
  "permitted_write_root": "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z",
  "expected": {
    "exit": 0,
    "field": "status",
    "value": "VALID",
    "read_only_root": null,
    "before_manifest": null
  },
  "start_utc": "2026-09-13T16:32:39.944124+00:00",
  "stdin_sha256": null
}
```

Exit: 0; timeout: False. Raw output: `commands/ext2-update-unchanged/stdout.txt`, `stderr.txt`.

## extended-followup-suite

```json
{
  "case": "extended-followup-suite",
  "argv": [
    "python",
    "-B",
    "-X",
    "utf8",
    "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z\\test_extended_followup.py"
  ],
  "cwd": "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z",
  "timeout_seconds": 120,
  "permitted_write_root": "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z",
  "expected": "Tool identification only; no acceptance claim",
  "start_utc": "2026-09-13T16:32:34.794263+00:00",
  "stdin_sha256": null
}
```

Exit: 0; timeout: False. Raw output: `commands/extended-followup-suite/stdout.txt`, `stderr.txt`.

## extended-suite

```json
{
  "case": "extended-suite",
  "argv": [
    "python",
    "-B",
    "-X",
    "utf8",
    "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z\\test_extended.py"
  ],
  "cwd": "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z",
  "timeout_seconds": 120,
  "permitted_write_root": "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z",
  "expected": "Tool identification only; no acceptance claim",
  "start_utc": "2026-09-13T16:31:31.836066+00:00",
  "stdin_sha256": null
}
```

Exit: 0; timeout: False. Raw output: `commands/extended-suite/stdout.txt`, `stderr.txt`.

## followup-suite

```json
{
  "case": "followup-suite",
  "argv": [
    "python",
    "-B",
    "-X",
    "utf8",
    "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z\\test_followup.py"
  ],
  "cwd": "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z",
  "timeout_seconds": 120,
  "permitted_write_root": "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z",
  "expected": "Tool identification only; no acceptance claim",
  "start_utc": "2026-09-13T15:52:52.085038+00:00",
  "stdin_sha256": null
}
```

Exit: 0; timeout: False. Raw output: `commands/followup-suite/stdout.txt`, `stderr.txt`.

## independent-suite

```json
{
  "case": "independent-suite",
  "argv": [
    "python",
    "-B",
    "-X",
    "utf8",
    "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z\\test_independent.py"
  ],
  "cwd": "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z",
  "timeout_seconds": 120,
  "permitted_write_root": "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z",
  "expected": "Tool identification only; no acceptance claim",
  "start_utc": "2026-09-13T15:50:42.737035+00:00",
  "stdin_sha256": null
}
```

Exit: 1; timeout: False. Raw output: `commands/independent-suite/stdout.txt`, `stderr.txt`.

## lineage-fence-crlf

```json
{
  "case": "lineage-fence-crlf",
  "argv": [
    "C:\\Program Files\\Python310\\python.exe",
    "-B",
    "-X",
    "utf8",
    "C:\\Projects\\DevForgeAI\\src\\agents\\skills\\skill-builder\\scripts\\adaptive.py",
    "inspect",
    "--record",
    "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z\\fixtures\\independent-01\\records\\fence-crlf\\valid.json"
  ],
  "cwd": "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z",
  "timeout_seconds": 120,
  "permitted_write_root": "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z",
  "expected": {
    "exit": 0,
    "field": "status",
    "value": "VALID",
    "read_only_root": null,
    "before_manifest": null
  },
  "start_utc": "2026-09-13T15:51:08.176150+00:00",
  "stdin_sha256": null
}
```

Exit: 0; timeout: False. Raw output: `commands/lineage-fence-crlf/stdout.txt`, `stderr.txt`.

## lineage-fence-lf

```json
{
  "case": "lineage-fence-lf",
  "argv": [
    "C:\\Program Files\\Python310\\python.exe",
    "-B",
    "-X",
    "utf8",
    "C:\\Projects\\DevForgeAI\\src\\agents\\skills\\skill-builder\\scripts\\adaptive.py",
    "inspect",
    "--record",
    "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z\\fixtures\\independent-01\\records\\fence-lf\\valid.json"
  ],
  "cwd": "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z",
  "timeout_seconds": 120,
  "permitted_write_root": "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z",
  "expected": {
    "exit": 0,
    "field": "status",
    "value": "VALID",
    "read_only_root": null,
    "before_manifest": null
  },
  "start_utc": "2026-09-13T15:51:07.522488+00:00",
  "stdin_sha256": null
}
```

Exit: 0; timeout: False. Raw output: `commands/lineage-fence-lf/stdout.txt`, `stderr.txt`.

## lineage-missing-fence-crlf

```json
{
  "case": "lineage-missing-fence-crlf",
  "argv": [
    "C:\\Program Files\\Python310\\python.exe",
    "-B",
    "-X",
    "utf8",
    "C:\\Projects\\DevForgeAI\\src\\agents\\skills\\skill-builder\\scripts\\adaptive.py",
    "inspect",
    "--record",
    "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z\\fixtures\\independent-01\\records\\fence-crlf\\missing.json"
  ],
  "cwd": "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z",
  "timeout_seconds": 120,
  "permitted_write_root": "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z",
  "expected": {
    "exit": 1,
    "field": "status",
    "value": "INVALID",
    "read_only_root": null,
    "before_manifest": null
  },
  "start_utc": "2026-09-13T15:51:08.421688+00:00",
  "stdin_sha256": null
}
```

Exit: 1; timeout: False. Raw output: `commands/lineage-missing-fence-crlf/stdout.txt`, `stderr.txt`.

## lineage-missing-fence-lf

```json
{
  "case": "lineage-missing-fence-lf",
  "argv": [
    "C:\\Program Files\\Python310\\python.exe",
    "-B",
    "-X",
    "utf8",
    "C:\\Projects\\DevForgeAI\\src\\agents\\skills\\skill-builder\\scripts\\adaptive.py",
    "inspect",
    "--record",
    "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z\\fixtures\\independent-01\\records\\fence-lf\\missing.json"
  ],
  "cwd": "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z",
  "timeout_seconds": 120,
  "permitted_write_root": "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z",
  "expected": {
    "exit": 1,
    "field": "status",
    "value": "INVALID",
    "read_only_root": null,
    "before_manifest": null
  },
  "start_utc": "2026-09-13T15:51:07.769512+00:00",
  "stdin_sha256": null
}
```

Exit: 1; timeout: False. Raw output: `commands/lineage-missing-fence-lf/stdout.txt`, `stderr.txt`.

## lineage-missing-table-other-resource

```json
{
  "case": "lineage-missing-table-other-resource",
  "argv": [
    "C:\\Program Files\\Python310\\python.exe",
    "-B",
    "-X",
    "utf8",
    "C:\\Projects\\DevForgeAI\\src\\agents\\skills\\skill-builder\\scripts\\adaptive.py",
    "inspect",
    "--record",
    "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z\\fixtures\\independent-01\\records\\table-other-resource\\missing.json"
  ],
  "cwd": "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z",
  "timeout_seconds": 120,
  "permitted_write_root": "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z",
  "expected": {
    "exit": 1,
    "field": "status",
    "value": "INVALID",
    "read_only_root": null,
    "before_manifest": null
  },
  "start_utc": "2026-09-13T15:51:09.075472+00:00",
  "stdin_sha256": null
}
```

Exit: 1; timeout: False. Raw output: `commands/lineage-missing-table-other-resource/stdout.txt`, `stderr.txt`.

## lineage-removal-fence-crlf

```json
{
  "case": "lineage-removal-fence-crlf",
  "argv": [
    "C:\\Program Files\\Python310\\python.exe",
    "-B",
    "-X",
    "utf8",
    "C:\\Projects\\DevForgeAI\\src\\agents\\skills\\skill-builder\\scripts\\adaptive.py",
    "inspect",
    "--record",
    "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z\\fixtures\\independent-01\\records\\fence-crlf\\removed.json"
  ],
  "cwd": "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z",
  "timeout_seconds": 120,
  "permitted_write_root": "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z",
  "expected": {
    "exit": 1,
    "field": "status",
    "value": "INVALID",
    "read_only_root": null,
    "before_manifest": null
  },
  "start_utc": "2026-09-13T15:51:08.618692+00:00",
  "stdin_sha256": null
}
```

Exit: 1; timeout: False. Raw output: `commands/lineage-removal-fence-crlf/stdout.txt`, `stderr.txt`.

## lineage-removal-fence-lf

```json
{
  "case": "lineage-removal-fence-lf",
  "argv": [
    "C:\\Program Files\\Python310\\python.exe",
    "-B",
    "-X",
    "utf8",
    "C:\\Projects\\DevForgeAI\\src\\agents\\skills\\skill-builder\\scripts\\adaptive.py",
    "inspect",
    "--record",
    "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z\\fixtures\\independent-01\\records\\fence-lf\\removed.json"
  ],
  "cwd": "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z",
  "timeout_seconds": 120,
  "permitted_write_root": "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z",
  "expected": {
    "exit": 1,
    "field": "status",
    "value": "INVALID",
    "read_only_root": null,
    "before_manifest": null
  },
  "start_utc": "2026-09-13T15:51:07.971147+00:00",
  "stdin_sha256": null
}
```

Exit: 1; timeout: False. Raw output: `commands/lineage-removal-fence-lf/stdout.txt`, `stderr.txt`.

## lineage-removal-table-other-resource

```json
{
  "case": "lineage-removal-table-other-resource",
  "argv": [
    "C:\\Program Files\\Python310\\python.exe",
    "-B",
    "-X",
    "utf8",
    "C:\\Projects\\DevForgeAI\\src\\agents\\skills\\skill-builder\\scripts\\adaptive.py",
    "inspect",
    "--record",
    "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z\\fixtures\\independent-01\\records\\table-other-resource\\removed.json"
  ],
  "cwd": "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z",
  "timeout_seconds": 120,
  "permitted_write_root": "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z",
  "expected": {
    "exit": 1,
    "field": "status",
    "value": "INVALID",
    "read_only_root": null,
    "before_manifest": null
  },
  "start_utc": "2026-09-13T15:51:09.365974+00:00",
  "stdin_sha256": null
}
```

Exit: 1; timeout: False. Raw output: `commands/lineage-removal-table-other-resource/stdout.txt`, `stderr.txt`.

## lineage-table-other-resource

```json
{
  "case": "lineage-table-other-resource",
  "argv": [
    "C:\\Program Files\\Python310\\python.exe",
    "-B",
    "-X",
    "utf8",
    "C:\\Projects\\DevForgeAI\\src\\agents\\skills\\skill-builder\\scripts\\adaptive.py",
    "inspect",
    "--record",
    "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z\\fixtures\\independent-01\\records\\table-other-resource\\valid.json"
  ],
  "cwd": "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z",
  "timeout_seconds": 120,
  "permitted_write_root": "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z",
  "expected": {
    "exit": 0,
    "field": "status",
    "value": "VALID",
    "read_only_root": null,
    "before_manifest": null
  },
  "start_utc": "2026-09-13T15:51:08.815695+00:00",
  "stdin_sha256": null
}
```

Exit: 0; timeout: False. Raw output: `commands/lineage-table-other-resource/stdout.txt`, `stderr.txt`.

## linux-exact-bytes

```json
{
  "case": "linux-exact-bytes",
  "argv": [
    "/usr/bin/python3",
    "-B",
    "-X",
    "utf8",
    "/mnt/c/Projects/DevForgeAI/docs/plan/skill-independent-qa/skill-builder/20260913T152822695886Z/fixtures/platform-linux/exact-bytes/space é & ; $ ' (p)/.agents/skills/summary-skill/scripts/check_project_binding.py",
    "--project-root",
    "/mnt/c/Projects/DevForgeAI/docs/plan/skill-independent-qa/skill-builder/20260913T152822695886Z/fixtures/platform-linux/exact-bytes/space é & ; $ ' (p)",
    "--skill-root",
    "/mnt/c/Projects/DevForgeAI/docs/plan/skill-independent-qa/skill-builder/20260913T152822695886Z/fixtures/platform-linux/exact-bytes/space é & ; $ ' (p)/.agents/skills/summary-skill"
  ],
  "cwd": "/mnt/c/Projects/DevForgeAI/docs/plan/skill-independent-qa/skill-builder/20260913T152822695886Z",
  "timeout_seconds": 120,
  "permitted_write_root": "/mnt/c/Projects/DevForgeAI/docs/plan/skill-independent-qa/skill-builder/20260913T152822695886Z",
  "expected": {
    "exit": 0,
    "field": "reason_code",
    "value": "BOUND",
    "read_only_root": null,
    "before_manifest": null
  },
  "start_utc": "2026-09-13T16:30:50.864522+00:00",
  "stdin_sha256": null
}
```

Exit: 0; timeout: False. Raw output: `commands/linux-exact-bytes/stdout.txt`, `stderr.txt`.

## linux-exact-files

```json
{
  "case": "linux-exact-files",
  "argv": [
    "/usr/bin/python3",
    "-B",
    "-X",
    "utf8",
    "/mnt/c/Projects/DevForgeAI/docs/plan/skill-independent-qa/skill-builder/20260913T152822695886Z/fixtures/platform-linux/exact-files/space é & ; $ ' (p)/.agents/skills/summary-skill/scripts/check_project_binding.py",
    "--project-root",
    "/mnt/c/Projects/DevForgeAI/docs/plan/skill-independent-qa/skill-builder/20260913T152822695886Z/fixtures/platform-linux/exact-files/space é & ; $ ' (p)",
    "--skill-root",
    "/mnt/c/Projects/DevForgeAI/docs/plan/skill-independent-qa/skill-builder/20260913T152822695886Z/fixtures/platform-linux/exact-files/space é & ; $ ' (p)/.agents/skills/summary-skill"
  ],
  "cwd": "/mnt/c/Projects/DevForgeAI/docs/plan/skill-independent-qa/skill-builder/20260913T152822695886Z",
  "timeout_seconds": 120,
  "permitted_write_root": "/mnt/c/Projects/DevForgeAI/docs/plan/skill-independent-qa/skill-builder/20260913T152822695886Z",
  "expected": {
    "exit": 0,
    "field": "reason_code",
    "value": "BOUND",
    "read_only_root": null,
    "before_manifest": null
  },
  "start_utc": "2026-09-13T16:25:57.605528+00:00",
  "stdin_sha256": null
}
```

Exit: -9; timeout: True. Raw output: `commands/linux-exact-files/stdout.txt`, `stderr.txt`.

## linux-io-error

```json
{
  "case": "linux-io-error",
  "argv": [
    "/usr/bin/python3",
    "-B",
    "-X",
    "utf8",
    "/mnt/c/Projects/DevForgeAI/docs/plan/skill-independent-qa/skill-builder/20260913T152822695886Z/fixtures/platform-linux/io-error/space é & ; $ ' (p)/.agents/skills/summary-skill/scripts/check_project_binding.py",
    "--project-root",
    "/mnt/c/Projects/DevForgeAI/docs/plan/skill-independent-qa/skill-builder/20260913T152822695886Z/fixtures/platform-linux/io-error/space é & ; $ ' (p)",
    "--skill-root",
    "/mnt/c/Projects/DevForgeAI/docs/plan/skill-independent-qa/skill-builder/20260913T152822695886Z/fixtures/platform-linux/io-error/space é & ; $ ' (p)/.agents/skills/summary-skill"
  ],
  "cwd": "/mnt/c/Projects/DevForgeAI/docs/plan/skill-independent-qa/skill-builder/20260913T152822695886Z",
  "timeout_seconds": 120,
  "permitted_write_root": "/mnt/c/Projects/DevForgeAI/docs/plan/skill-independent-qa/skill-builder/20260913T152822695886Z",
  "expected": {
    "exit": 2,
    "field": "reason_code",
    "value": "IO_ERROR",
    "read_only_root": null,
    "before_manifest": null
  },
  "start_utc": "2026-09-13T16:24:38.258332+00:00",
  "stdin_sha256": null
}
```

Exit: 2; timeout: False. Raw output: `commands/linux-io-error/stdout.txt`, `stderr.txt`.

## linux-missing

```json
{
  "case": "linux-missing",
  "argv": [
    "/usr/bin/python3",
    "-B",
    "-X",
    "utf8",
    "/mnt/c/Projects/DevForgeAI/docs/plan/skill-independent-qa/skill-builder/20260913T152822695886Z/fixtures/platform-linux/missing/space é & ; $ ' (p)/.agents/skills/summary-skill/scripts/check_project_binding.py",
    "--project-root",
    "/mnt/c/Projects/DevForgeAI/docs/plan/skill-independent-qa/skill-builder/20260913T152822695886Z/fixtures/platform-linux/missing/space é & ; $ ' (p)",
    "--skill-root",
    "/mnt/c/Projects/DevForgeAI/docs/plan/skill-independent-qa/skill-builder/20260913T152822695886Z/fixtures/platform-linux/missing/space é & ; $ ' (p)/.agents/skills/summary-skill"
  ],
  "cwd": "/mnt/c/Projects/DevForgeAI/docs/plan/skill-independent-qa/skill-builder/20260913T152822695886Z",
  "timeout_seconds": 120,
  "permitted_write_root": "/mnt/c/Projects/DevForgeAI/docs/plan/skill-independent-qa/skill-builder/20260913T152822695886Z",
  "expected": {
    "exit": 1,
    "field": "reason_code",
    "value": "MISSING_BINDING",
    "read_only_root": null,
    "before_manifest": null
  },
  "start_utc": "2026-09-13T16:24:37.639449+00:00",
  "stdin_sha256": null
}
```

Exit: 1; timeout: False. Raw output: `commands/linux-missing/stdout.txt`, `stderr.txt`.

## linux-over-bytes

```json
{
  "case": "linux-over-bytes",
  "argv": [
    "/usr/bin/python3",
    "-B",
    "-X",
    "utf8",
    "/mnt/c/Projects/DevForgeAI/docs/plan/skill-independent-qa/skill-builder/20260913T152822695886Z/fixtures/platform-linux/over-bytes/space é & ; $ ' (p)/.agents/skills/summary-skill/scripts/check_project_binding.py",
    "--project-root",
    "/mnt/c/Projects/DevForgeAI/docs/plan/skill-independent-qa/skill-builder/20260913T152822695886Z/fixtures/platform-linux/over-bytes/space é & ; $ ' (p)",
    "--skill-root",
    "/mnt/c/Projects/DevForgeAI/docs/plan/skill-independent-qa/skill-builder/20260913T152822695886Z/fixtures/platform-linux/over-bytes/space é & ; $ ' (p)/.agents/skills/summary-skill"
  ],
  "cwd": "/mnt/c/Projects/DevForgeAI/docs/plan/skill-independent-qa/skill-builder/20260913T152822695886Z",
  "timeout_seconds": 120,
  "permitted_write_root": "/mnt/c/Projects/DevForgeAI/docs/plan/skill-independent-qa/skill-builder/20260913T152822695886Z",
  "expected": {
    "exit": 2,
    "field": "reason_code",
    "value": "CAPTURE_LIMIT",
    "read_only_root": null,
    "before_manifest": null
  },
  "start_utc": "2026-09-13T16:30:55.016216+00:00",
  "stdin_sha256": null
}
```

Exit: 2; timeout: False. Raw output: `commands/linux-over-bytes/stdout.txt`, `stderr.txt`.

## linux-over-files

```json
{
  "case": "linux-over-files",
  "argv": [
    "/usr/bin/python3",
    "-B",
    "-X",
    "utf8",
    "/mnt/c/Projects/DevForgeAI/docs/plan/skill-independent-qa/skill-builder/20260913T152822695886Z/fixtures/platform-linux/over-files/space é & ; $ ' (p)/.agents/skills/summary-skill/scripts/check_project_binding.py",
    "--project-root",
    "/mnt/c/Projects/DevForgeAI/docs/plan/skill-independent-qa/skill-builder/20260913T152822695886Z/fixtures/platform-linux/over-files/space é & ; $ ' (p)",
    "--skill-root",
    "/mnt/c/Projects/DevForgeAI/docs/plan/skill-independent-qa/skill-builder/20260913T152822695886Z/fixtures/platform-linux/over-files/space é & ; $ ' (p)/.agents/skills/summary-skill"
  ],
  "cwd": "/mnt/c/Projects/DevForgeAI/docs/plan/skill-independent-qa/skill-builder/20260913T152822695886Z",
  "timeout_seconds": 120,
  "permitted_write_root": "/mnt/c/Projects/DevForgeAI/docs/plan/skill-independent-qa/skill-builder/20260913T152822695886Z",
  "expected": {
    "exit": 2,
    "field": "reason_code",
    "value": "CAPTURE_LIMIT",
    "read_only_root": null,
    "before_manifest": null
  },
  "start_utc": "2026-09-13T16:29:00.961912+00:00",
  "stdin_sha256": null
}
```

Exit: -9; timeout: True. Raw output: `commands/linux-over-files/stdout.txt`, `stderr.txt`.

## linux-pfx-name

```json
{
  "case": "linux-pfx-name",
  "argv": [
    "/usr/bin/python3",
    "-B",
    "-X",
    "utf8",
    "/mnt/c/Projects/DevForgeAI/docs/plan/skill-independent-qa/skill-builder/20260913T152822695886Z/fixtures/platform-linux/pfx-name/space é & ; $ ' (p)/.agents/skills/summary-skill/scripts/check_project_binding.py",
    "--project-root",
    "/mnt/c/Projects/DevForgeAI/docs/plan/skill-independent-qa/skill-builder/20260913T152822695886Z/fixtures/platform-linux/pfx-name/space é & ; $ ' (p)",
    "--skill-root",
    "/mnt/c/Projects/DevForgeAI/docs/plan/skill-independent-qa/skill-builder/20260913T152822695886Z/fixtures/platform-linux/pfx-name/space é & ; $ ' (p)/.agents/skills/summary-skill"
  ],
  "cwd": "/mnt/c/Projects/DevForgeAI/docs/plan/skill-independent-qa/skill-builder/20260913T152822695886Z",
  "timeout_seconds": 120,
  "permitted_write_root": "/mnt/c/Projects/DevForgeAI/docs/plan/skill-independent-qa/skill-builder/20260913T152822695886Z",
  "expected": {
    "exit": 1,
    "field": "reason_code",
    "value": "UNSAFE_PATH",
    "read_only_root": null,
    "before_manifest": null
  },
  "start_utc": "2026-09-13T16:24:44.769928+00:00",
  "stdin_sha256": null
}
```

Exit: 0; timeout: False. Raw output: `commands/linux-pfx-name/stdout.txt`, `stderr.txt`.

## linux-private-key-name

```json
{
  "case": "linux-private-key-name",
  "argv": [
    "/usr/bin/python3",
    "-B",
    "-X",
    "utf8",
    "/mnt/c/Projects/DevForgeAI/docs/plan/skill-independent-qa/skill-builder/20260913T152822695886Z/fixtures/platform-linux/private-key-name/space é & ; $ ' (p)/.agents/skills/summary-skill/scripts/check_project_binding.py",
    "--project-root",
    "/mnt/c/Projects/DevForgeAI/docs/plan/skill-independent-qa/skill-builder/20260913T152822695886Z/fixtures/platform-linux/private-key-name/space é & ; $ ' (p)",
    "--skill-root",
    "/mnt/c/Projects/DevForgeAI/docs/plan/skill-independent-qa/skill-builder/20260913T152822695886Z/fixtures/platform-linux/private-key-name/space é & ; $ ' (p)/.agents/skills/summary-skill"
  ],
  "cwd": "/mnt/c/Projects/DevForgeAI/docs/plan/skill-independent-qa/skill-builder/20260913T152822695886Z",
  "timeout_seconds": 120,
  "permitted_write_root": "/mnt/c/Projects/DevForgeAI/docs/plan/skill-independent-qa/skill-builder/20260913T152822695886Z",
  "expected": {
    "exit": 1,
    "field": "reason_code",
    "value": "UNSAFE_PATH",
    "read_only_root": null,
    "before_manifest": null
  },
  "start_utc": "2026-09-13T16:24:40.698675+00:00",
  "stdin_sha256": null
}
```

Exit: 0; timeout: False. Raw output: `commands/linux-private-key-name/stdout.txt`, `stderr.txt`.

## linux-relocated

```json
{
  "case": "linux-relocated",
  "argv": [
    "/usr/bin/python3",
    "-B",
    "-X",
    "utf8",
    "/mnt/c/Projects/DevForgeAI/docs/plan/skill-independent-qa/skill-builder/20260913T152822695886Z/fixtures/platform-linux/relocated/space é & ; $ ' (p)/.agents/skills/summary-skill/scripts/check_project_binding.py",
    "--project-root",
    "/mnt/c/Projects/DevForgeAI/docs/plan/skill-independent-qa/skill-builder/20260913T152822695886Z/fixtures/platform-linux/relocated/space é & ; $ ' (p)",
    "--skill-root",
    "/mnt/c/Projects/DevForgeAI/docs/plan/skill-independent-qa/skill-builder/20260913T152822695886Z/fixtures/platform-linux/relocated/space é & ; $ ' (p)/.agents/skills/summary-skill"
  ],
  "cwd": "/mnt/c/Projects/DevForgeAI/docs/plan/skill-independent-qa/skill-builder/20260913T152822695886Z",
  "timeout_seconds": 120,
  "permitted_write_root": "/mnt/c/Projects/DevForgeAI/docs/plan/skill-independent-qa/skill-builder/20260913T152822695886Z",
  "expected": {
    "exit": 1,
    "field": "reason_code",
    "value": "ROOT_MISMATCH",
    "read_only_root": null,
    "before_manifest": null
  },
  "start_utc": "2026-09-13T16:24:36.921607+00:00",
  "stdin_sha256": null
}
```

Exit: 1; timeout: False. Raw output: `commands/linux-relocated/stdout.txt`, `stderr.txt`.

## linux-symlink

```json
{
  "case": "linux-symlink",
  "argv": [
    "/usr/bin/python3",
    "-B",
    "-X",
    "utf8",
    "/mnt/c/Projects/DevForgeAI/docs/plan/skill-independent-qa/skill-builder/20260913T152822695886Z/fixtures/platform-linux/symlink/space é & ; $ ' (p)/.agents/skills/summary-skill/scripts/check_project_binding.py",
    "--project-root",
    "/mnt/c/Projects/DevForgeAI/docs/plan/skill-independent-qa/skill-builder/20260913T152822695886Z/fixtures/platform-linux/symlink/space é & ; $ ' (p)",
    "--skill-root",
    "/mnt/c/Projects/DevForgeAI/docs/plan/skill-independent-qa/skill-builder/20260913T152822695886Z/fixtures/platform-linux/symlink/space é & ; $ ' (p)/.agents/skills/summary-skill"
  ],
  "cwd": "/mnt/c/Projects/DevForgeAI/docs/plan/skill-independent-qa/skill-builder/20260913T152822695886Z",
  "timeout_seconds": 120,
  "permitted_write_root": "/mnt/c/Projects/DevForgeAI/docs/plan/skill-independent-qa/skill-builder/20260913T152822695886Z",
  "expected": {
    "exit": 1,
    "field": "reason_code",
    "value": "UNSAFE_PATH",
    "read_only_root": null,
    "before_manifest": null
  },
  "start_utc": "2026-09-13T16:24:38.954149+00:00",
  "stdin_sha256": null
}
```

Exit: 1; timeout: False. Raw output: `commands/linux-symlink/stdout.txt`, `stderr.txt`.

## linux-valid

```json
{
  "case": "linux-valid",
  "argv": [
    "/usr/bin/python3",
    "-B",
    "-X",
    "utf8",
    "/mnt/c/Projects/DevForgeAI/docs/plan/skill-independent-qa/skill-builder/20260913T152822695886Z/fixtures/platform-linux/valid/space é & ; $ ' (p)/.agents/skills/summary-skill/scripts/check_project_binding.py",
    "--project-root",
    "/mnt/c/Projects/DevForgeAI/docs/plan/skill-independent-qa/skill-builder/20260913T152822695886Z/fixtures/platform-linux/valid/space é & ; $ ' (p)",
    "--skill-root",
    "/mnt/c/Projects/DevForgeAI/docs/plan/skill-independent-qa/skill-builder/20260913T152822695886Z/fixtures/platform-linux/valid/space é & ; $ ' (p)/.agents/skills/summary-skill"
  ],
  "cwd": "/mnt/c/Projects/DevForgeAI/docs/plan/skill-independent-qa/skill-builder/20260913T152822695886Z",
  "timeout_seconds": 120,
  "permitted_write_root": "/mnt/c/Projects/DevForgeAI/docs/plan/skill-independent-qa/skill-builder/20260913T152822695886Z",
  "expected": {
    "exit": 0,
    "field": "reason_code",
    "value": "BOUND",
    "read_only_root": null,
    "before_manifest": null
  },
  "start_utc": "2026-09-13T16:24:33.617770+00:00",
  "stdin_sha256": null
}
```

Exit: 0; timeout: False. Raw output: `commands/linux-valid/stdout.txt`, `stderr.txt`.

## missing-python-child

```json
{
  "case": "missing-python-child",
  "argv": [
    "python-does-not-exist-audit",
    "-B",
    "-X",
    "utf8",
    "helper.py"
  ],
  "cwd": "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z",
  "timeout_seconds": 120,
  "permitted_write_root": "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z",
  "expected": {
    "exit": null,
    "field": null,
    "value": null,
    "read_only_root": null,
    "before_manifest": null
  },
  "start_utc": "2026-09-13T15:51:03.692269+00:00",
  "stdin_sha256": null
}
```

Exit: None; timeout: False. Raw output: `commands/missing-python-child/stdout.txt`, `stderr.txt`.

## platform-windows-suite

```json
{
  "case": "platform-windows-suite",
  "argv": [
    "python",
    "-B",
    "-X",
    "utf8",
    "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z\\platform_cases.py"
  ],
  "cwd": "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z",
  "timeout_seconds": 120,
  "permitted_write_root": "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z",
  "expected": "Tool identification only; no acceptance claim",
  "start_utc": "2026-09-13T16:21:41.677648+00:00",
  "stdin_sha256": null
}
```

Exit: 0; timeout: False. Raw output: `commands/platform-windows-suite/stdout.txt`, `stderr.txt`.

## proposal-core-with-lineage

```json
{
  "case": "proposal-core-with-lineage",
  "argv": [
    "C:\\Program Files\\Python310\\python.exe",
    "-B",
    "-X",
    "utf8",
    "C:\\Projects\\DevForgeAI\\src\\agents\\skills\\skill-builder\\scripts\\adaptive.py",
    "inspect",
    "--record",
    "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z\\fixtures\\independent-01\\records\\proposal-core-with-lineage.json"
  ],
  "cwd": "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z",
  "timeout_seconds": 120,
  "permitted_write_root": "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z",
  "expected": {
    "exit": 1,
    "field": "status",
    "value": "INVALID",
    "read_only_root": null,
    "before_manifest": null
  },
  "start_utc": "2026-09-13T15:51:06.186206+00:00",
  "stdin_sha256": null
}
```

Exit: 1; timeout: False. Raw output: `commands/proposal-core-with-lineage/stdout.txt`, `stderr.txt`.

## proposal-cycle

```json
{
  "case": "proposal-cycle",
  "argv": [
    "C:\\Program Files\\Python310\\python.exe",
    "-B",
    "-X",
    "utf8",
    "C:\\Projects\\DevForgeAI\\src\\agents\\skills\\skill-builder\\scripts\\adaptive.py",
    "inspect",
    "--record",
    "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z\\fixtures\\independent-01\\records\\proposal-cycle.json"
  ],
  "cwd": "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z",
  "timeout_seconds": 120,
  "permitted_write_root": "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z",
  "expected": {
    "exit": 1,
    "field": "status",
    "value": "INVALID",
    "read_only_root": null,
    "before_manifest": null
  },
  "start_utc": "2026-09-13T15:51:05.530844+00:00",
  "stdin_sha256": null
}
```

Exit: 1; timeout: False. Raw output: `commands/proposal-cycle/stdout.txt`, `stderr.txt`.

## proposal-invalid-name

```json
{
  "case": "proposal-invalid-name",
  "argv": [
    "C:\\Program Files\\Python310\\python.exe",
    "-B",
    "-X",
    "utf8",
    "C:\\Projects\\DevForgeAI\\src\\agents\\skills\\skill-builder\\scripts\\adaptive.py",
    "inspect",
    "--record",
    "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z\\fixtures\\independent-01\\records\\proposal-invalid-name.json"
  ],
  "cwd": "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z",
  "timeout_seconds": 120,
  "permitted_write_root": "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z",
  "expected": {
    "exit": 1,
    "field": "status",
    "value": "INVALID",
    "read_only_root": null,
    "before_manifest": null
  },
  "start_utc": "2026-09-13T15:51:05.948197+00:00",
  "stdin_sha256": null
}
```

Exit: 1; timeout: False. Raw output: `commands/proposal-invalid-name/stdout.txt`, `stderr.txt`.

## proposal-json-no-schema

```json
{
  "case": "proposal-json-no-schema",
  "argv": [
    "C:\\Program Files\\Python310\\python.exe",
    "-B",
    "-X",
    "utf8",
    "C:\\Projects\\DevForgeAI\\src\\agents\\skills\\skill-builder\\scripts\\adaptive.py",
    "inspect",
    "--record",
    "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z\\fixtures\\independent-01\\records\\proposal-json-no-schema.json"
  ],
  "cwd": "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z",
  "timeout_seconds": 120,
  "permitted_write_root": "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z",
  "expected": {
    "exit": 1,
    "field": "status",
    "value": "INVALID",
    "read_only_root": null,
    "before_manifest": null
  },
  "start_utc": "2026-09-13T15:51:06.333204+00:00",
  "stdin_sha256": null
}
```

Exit: 1; timeout: False. Raw output: `commands/proposal-json-no-schema/stdout.txt`, `stderr.txt`.

## proposal-missing-dependency

```json
{
  "case": "proposal-missing-dependency",
  "argv": [
    "C:\\Program Files\\Python310\\python.exe",
    "-B",
    "-X",
    "utf8",
    "C:\\Projects\\DevForgeAI\\src\\agents\\skills\\skill-builder\\scripts\\adaptive.py",
    "inspect",
    "--record",
    "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z\\fixtures\\independent-01\\records\\proposal-missing-dependency.json"
  ],
  "cwd": "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z",
  "timeout_seconds": 120,
  "permitted_write_root": "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z",
  "expected": {
    "exit": 1,
    "field": "status",
    "value": "INVALID",
    "read_only_root": null,
    "before_manifest": null
  },
  "start_utc": "2026-09-13T15:51:05.382845+00:00",
  "stdin_sha256": null
}
```

Exit: 1; timeout: False. Raw output: `commands/proposal-missing-dependency/stdout.txt`, `stderr.txt`.

## proposal-unknown-fact

```json
{
  "case": "proposal-unknown-fact",
  "argv": [
    "C:\\Program Files\\Python310\\python.exe",
    "-B",
    "-X",
    "utf8",
    "C:\\Projects\\DevForgeAI\\src\\agents\\skills\\skill-builder\\scripts\\adaptive.py",
    "inspect",
    "--record",
    "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z\\fixtures\\independent-01\\records\\proposal-unknown-fact.json"
  ],
  "cwd": "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z",
  "timeout_seconds": 120,
  "permitted_write_root": "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z",
  "expected": {
    "exit": 1,
    "field": "status",
    "value": "INVALID",
    "read_only_root": null,
    "before_manifest": null
  },
  "start_utc": "2026-09-13T15:51:05.810687+00:00",
  "stdin_sha256": null
}
```

Exit: 1; timeout: False. Raw output: `commands/proposal-unknown-fact/stdout.txt`, `stderr.txt`.

## proposal-unknown-requirement

```json
{
  "case": "proposal-unknown-requirement",
  "argv": [
    "C:\\Program Files\\Python310\\python.exe",
    "-B",
    "-X",
    "utf8",
    "C:\\Projects\\DevForgeAI\\src\\agents\\skills\\skill-builder\\scripts\\adaptive.py",
    "inspect",
    "--record",
    "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z\\fixtures\\independent-01\\records\\proposal-unknown-requirement.json"
  ],
  "cwd": "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z",
  "timeout_seconds": 120,
  "permitted_write_root": "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z",
  "expected": {
    "exit": 1,
    "field": "status",
    "value": "INVALID",
    "read_only_root": null,
    "before_manifest": null
  },
  "start_utc": "2026-09-13T15:51:05.676548+00:00",
  "stdin_sha256": null
}
```

Exit: 1; timeout: False. Raw output: `commands/proposal-unknown-requirement/stdout.txt`, `stderr.txt`.

## proposal-variant-no-parent

```json
{
  "case": "proposal-variant-no-parent",
  "argv": [
    "C:\\Program Files\\Python310\\python.exe",
    "-B",
    "-X",
    "utf8",
    "C:\\Projects\\DevForgeAI\\src\\agents\\skills\\skill-builder\\scripts\\adaptive.py",
    "inspect",
    "--record",
    "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z\\fixtures\\independent-01\\records\\proposal-variant-no-parent.json"
  ],
  "cwd": "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z",
  "timeout_seconds": 120,
  "permitted_write_root": "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z",
  "expected": {
    "exit": 1,
    "field": "status",
    "value": "INVALID",
    "read_only_root": null,
    "before_manifest": null
  },
  "start_utc": "2026-09-13T15:51:06.040205+00:00",
  "stdin_sha256": null
}
```

Exit: 1; timeout: False. Raw output: `commands/proposal-variant-no-parent/stdout.txt`, `stderr.txt`.

## record-bad-digest

```json
{
  "case": "record-bad-digest",
  "argv": [
    "C:\\Program Files\\Python310\\python.exe",
    "-B",
    "-X",
    "utf8",
    "C:\\Projects\\DevForgeAI\\src\\agents\\skills\\skill-builder\\scripts\\adaptive.py",
    "inspect",
    "--record",
    "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z\\fixtures\\independent-01\\records\\bad-digest.json"
  ],
  "cwd": "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z",
  "timeout_seconds": 120,
  "permitted_write_root": "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z",
  "expected": {
    "exit": 1,
    "field": "status",
    "value": "INVALID",
    "read_only_root": null,
    "before_manifest": null
  },
  "start_utc": "2026-09-13T15:51:04.438143+00:00",
  "stdin_sha256": null
}
```

Exit: 1; timeout: False. Raw output: `commands/record-bad-digest/stdout.txt`, `stderr.txt`.

## record-bad-locator

```json
{
  "case": "record-bad-locator",
  "argv": [
    "C:\\Program Files\\Python310\\python.exe",
    "-B",
    "-X",
    "utf8",
    "C:\\Projects\\DevForgeAI\\src\\agents\\skills\\skill-builder\\scripts\\adaptive.py",
    "inspect",
    "--record",
    "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z\\fixtures\\independent-01\\records\\bad-locator.json"
  ],
  "cwd": "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z",
  "timeout_seconds": 120,
  "permitted_write_root": "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z",
  "expected": {
    "exit": 1,
    "field": "status",
    "value": "INVALID",
    "read_only_root": null,
    "before_manifest": null
  },
  "start_utc": "2026-09-13T15:51:04.532528+00:00",
  "stdin_sha256": null
}
```

Exit: 1; timeout: False. Raw output: `commands/record-bad-locator/stdout.txt`, `stderr.txt`.

## record-bool-line

```json
{
  "case": "record-bool-line",
  "argv": [
    "C:\\Program Files\\Python310\\python.exe",
    "-B",
    "-X",
    "utf8",
    "C:\\Projects\\DevForgeAI\\src\\agents\\skills\\skill-builder\\scripts\\adaptive.py",
    "inspect",
    "--record",
    "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z\\fixtures\\independent-01\\records\\bool-line.json"
  ],
  "cwd": "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z",
  "timeout_seconds": 120,
  "permitted_write_root": "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z",
  "expected": {
    "exit": 1,
    "field": "status",
    "value": "INVALID",
    "read_only_root": null,
    "before_manifest": null
  },
  "start_utc": "2026-09-13T15:51:04.648509+00:00",
  "stdin_sha256": null
}
```

Exit: 1; timeout: False. Raw output: `commands/record-bool-line/stdout.txt`, `stderr.txt`.

## record-duplicate-fact

```json
{
  "case": "record-duplicate-fact",
  "argv": [
    "C:\\Program Files\\Python310\\python.exe",
    "-B",
    "-X",
    "utf8",
    "C:\\Projects\\DevForgeAI\\src\\agents\\skills\\skill-builder\\scripts\\adaptive.py",
    "inspect",
    "--record",
    "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z\\fixtures\\independent-01\\records\\duplicate-fact.json"
  ],
  "cwd": "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z",
  "timeout_seconds": 120,
  "permitted_write_root": "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z",
  "expected": {
    "exit": 1,
    "field": "status",
    "value": "INVALID",
    "read_only_root": null,
    "before_manifest": null
  },
  "start_utc": "2026-09-13T15:51:04.737869+00:00",
  "stdin_sha256": null
}
```

Exit: 1; timeout: False. Raw output: `commands/record-duplicate-fact/stdout.txt`, `stderr.txt`.

## record-duplicate-key

```json
{
  "case": "record-duplicate-key",
  "argv": [
    "C:\\Program Files\\Python310\\python.exe",
    "-B",
    "-X",
    "utf8",
    "C:\\Projects\\DevForgeAI\\src\\agents\\skills\\skill-builder\\scripts\\adaptive.py",
    "inspect",
    "--record",
    "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z\\fixtures\\independent-01\\records\\duplicate-key.json"
  ],
  "cwd": "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z",
  "timeout_seconds": 120,
  "permitted_write_root": "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z",
  "expected": {
    "exit": 1,
    "field": "status",
    "value": "INVALID",
    "read_only_root": null,
    "before_manifest": null
  },
  "start_utc": "2026-09-13T15:51:04.972896+00:00",
  "stdin_sha256": null
}
```

Exit: 1; timeout: False. Raw output: `commands/record-duplicate-key/stdout.txt`, `stderr.txt`.

## record-evidence-valid

```json
{
  "case": "record-evidence-valid",
  "argv": [
    "C:\\Program Files\\Python310\\python.exe",
    "-B",
    "-X",
    "utf8",
    "C:\\Projects\\DevForgeAI\\src\\agents\\skills\\skill-builder\\scripts\\adaptive.py",
    "inspect",
    "--record",
    "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z\\fixtures\\independent-01\\records\\evidence.json"
  ],
  "cwd": "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z",
  "timeout_seconds": 120,
  "permitted_write_root": "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z",
  "expected": {
    "exit": 0,
    "field": "status",
    "value": "VALID",
    "read_only_root": null,
    "before_manifest": null
  },
  "start_utc": "2026-09-13T15:51:03.709269+00:00",
  "stdin_sha256": null
}
```

Exit: 0; timeout: False. Raw output: `commands/record-evidence-valid/stdout.txt`, `stderr.txt`.

## record-extra-field

```json
{
  "case": "record-extra-field",
  "argv": [
    "C:\\Program Files\\Python310\\python.exe",
    "-B",
    "-X",
    "utf8",
    "C:\\Projects\\DevForgeAI\\src\\agents\\skills\\skill-builder\\scripts\\adaptive.py",
    "inspect",
    "--record",
    "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z\\fixtures\\independent-01\\records\\extra-field.json"
  ],
  "cwd": "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z",
  "timeout_seconds": 120,
  "permitted_write_root": "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z",
  "expected": {
    "exit": 1,
    "field": "status",
    "value": "INVALID",
    "read_only_root": null,
    "before_manifest": null
  },
  "start_utc": "2026-09-13T15:51:04.252681+00:00",
  "stdin_sha256": null
}
```

Exit: 1; timeout: False. Raw output: `commands/record-extra-field/stdout.txt`, `stderr.txt`.

## record-invalid-utf8

```json
{
  "case": "record-invalid-utf8",
  "argv": [
    "C:\\Program Files\\Python310\\python.exe",
    "-B",
    "-X",
    "utf8",
    "C:\\Projects\\DevForgeAI\\src\\agents\\skills\\skill-builder\\scripts\\adaptive.py",
    "inspect",
    "--record",
    "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z\\fixtures\\independent-01\\records\\invalid-utf8.json"
  ],
  "cwd": "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z",
  "timeout_seconds": 120,
  "permitted_write_root": "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z",
  "expected": {
    "exit": 1,
    "field": "status",
    "value": "INVALID",
    "read_only_root": null,
    "before_manifest": null
  },
  "start_utc": "2026-09-13T15:51:05.290460+00:00",
  "stdin_sha256": null
}
```

Exit: 1; timeout: False. Raw output: `commands/record-invalid-utf8/stdout.txt`, `stderr.txt`.

## record-material-omission

```json
{
  "case": "record-material-omission",
  "argv": [
    "C:\\Program Files\\Python310\\python.exe",
    "-B",
    "-X",
    "utf8",
    "C:\\Projects\\DevForgeAI\\src\\agents\\skills\\skill-builder\\scripts\\adaptive.py",
    "inspect",
    "--record",
    "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z\\fixtures\\independent-01\\records\\material-omission.json"
  ],
  "cwd": "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z",
  "timeout_seconds": 120,
  "permitted_write_root": "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z",
  "expected": {
    "exit": 1,
    "field": "status",
    "value": "INVALID",
    "read_only_root": null,
    "before_manifest": null
  },
  "start_utc": "2026-09-13T15:51:04.857896+00:00",
  "stdin_sha256": null
}
```

Exit: 1; timeout: False. Raw output: `commands/record-material-omission/stdout.txt`, `stderr.txt`.

## record-nonfinite

```json
{
  "case": "record-nonfinite",
  "argv": [
    "C:\\Program Files\\Python310\\python.exe",
    "-B",
    "-X",
    "utf8",
    "C:\\Projects\\DevForgeAI\\src\\agents\\skills\\skill-builder\\scripts\\adaptive.py",
    "inspect",
    "--record",
    "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z\\fixtures\\independent-01\\records\\nonfinite.json"
  ],
  "cwd": "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z",
  "timeout_seconds": 120,
  "permitted_write_root": "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z",
  "expected": {
    "exit": 1,
    "field": "status",
    "value": "INVALID",
    "read_only_root": null,
    "before_manifest": null
  },
  "start_utc": "2026-09-13T15:51:05.106892+00:00",
  "stdin_sha256": null
}
```

Exit: 1; timeout: False. Raw output: `commands/record-nonfinite/stdout.txt`, `stderr.txt`.

## record-overflow

```json
{
  "case": "record-overflow",
  "argv": [
    "C:\\Program Files\\Python310\\python.exe",
    "-B",
    "-X",
    "utf8",
    "C:\\Projects\\DevForgeAI\\src\\agents\\skills\\skill-builder\\scripts\\adaptive.py",
    "inspect",
    "--record",
    "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z\\fixtures\\independent-01\\records\\overflow.json"
  ],
  "cwd": "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z",
  "timeout_seconds": 120,
  "permitted_write_root": "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z",
  "expected": {
    "exit": 1,
    "field": "status",
    "value": "INVALID",
    "read_only_root": null,
    "before_manifest": null
  },
  "start_utc": "2026-09-13T15:51:05.198414+00:00",
  "stdin_sha256": null
}
```

Exit: 1; timeout: False. Raw output: `commands/record-overflow/stdout.txt`, `stderr.txt`.

## record-proposal-valid

```json
{
  "case": "record-proposal-valid",
  "argv": [
    "C:\\Program Files\\Python310\\python.exe",
    "-B",
    "-X",
    "utf8",
    "C:\\Projects\\DevForgeAI\\src\\agents\\skills\\skill-builder\\scripts\\adaptive.py",
    "inspect",
    "--record",
    "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z\\fixtures\\independent-01\\records\\proposal.json"
  ],
  "cwd": "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z",
  "timeout_seconds": 120,
  "permitted_write_root": "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z",
  "expected": {
    "exit": 0,
    "field": "status",
    "value": "VALID",
    "read_only_root": null,
    "before_manifest": null
  },
  "start_utc": "2026-09-13T15:51:03.836269+00:00",
  "stdin_sha256": null
}
```

Exit: 0; timeout: False. Raw output: `commands/record-proposal-valid/stdout.txt`, `stderr.txt`.

## record-selection-valid

```json
{
  "case": "record-selection-valid",
  "argv": [
    "C:\\Program Files\\Python310\\python.exe",
    "-B",
    "-X",
    "utf8",
    "C:\\Projects\\DevForgeAI\\src\\agents\\skills\\skill-builder\\scripts\\adaptive.py",
    "plan-set",
    "--selection",
    "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z\\fixtures\\independent-01\\records\\selection.json"
  ],
  "cwd": "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z",
  "timeout_seconds": 120,
  "permitted_write_root": "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z",
  "expected": {
    "exit": 0,
    "field": "status",
    "value": "VALID",
    "read_only_root": null,
    "before_manifest": null
  },
  "start_utc": "2026-09-13T15:51:04.003737+00:00",
  "stdin_sha256": null
}
```

Exit: 0; timeout: False. Raw output: `commands/record-selection-valid/stdout.txt`, `stderr.txt`.

## record-stale-reference

```json
{
  "case": "record-stale-reference",
  "argv": [
    "C:\\Program Files\\Python310\\python.exe",
    "-B",
    "-X",
    "utf8",
    "C:\\Projects\\DevForgeAI\\src\\agents\\skills\\skill-builder\\scripts\\adaptive.py",
    "inspect",
    "--record",
    "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z\\fixtures\\independent-01\\records\\stale.json"
  ],
  "cwd": "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z",
  "timeout_seconds": 120,
  "permitted_write_root": "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z",
  "expected": {
    "exit": 1,
    "field": "status",
    "value": "INVALID",
    "read_only_root": null,
    "before_manifest": null
  },
  "start_utc": "2026-09-13T15:51:07.305414+00:00",
  "stdin_sha256": null
}
```

Exit: 1; timeout: False. Raw output: `commands/record-stale-reference/stdout.txt`, `stderr.txt`.

## record-unknown-version

```json
{
  "case": "record-unknown-version",
  "argv": [
    "C:\\Program Files\\Python310\\python.exe",
    "-B",
    "-X",
    "utf8",
    "C:\\Projects\\DevForgeAI\\src\\agents\\skills\\skill-builder\\scripts\\adaptive.py",
    "inspect",
    "--record",
    "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z\\fixtures\\independent-01\\records\\unknown-version.json"
  ],
  "cwd": "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z",
  "timeout_seconds": 120,
  "permitted_write_root": "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z",
  "expected": {
    "exit": 1,
    "field": "status",
    "value": "INVALID",
    "read_only_root": null,
    "before_manifest": null
  },
  "start_utc": "2026-09-13T15:51:04.344179+00:00",
  "stdin_sha256": null
}
```

Exit: 1; timeout: False. Raw output: `commands/record-unknown-version/stdout.txt`, `stderr.txt`.

## selection-duplicate-selection

```json
{
  "case": "selection-duplicate-selection",
  "argv": [
    "C:\\Program Files\\Python310\\python.exe",
    "-B",
    "-X",
    "utf8",
    "C:\\Projects\\DevForgeAI\\src\\agents\\skills\\skill-builder\\scripts\\adaptive.py",
    "plan-set",
    "--selection",
    "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z\\fixtures\\independent-01\\records\\selection-duplicate-selection.json"
  ],
  "cwd": "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z",
  "timeout_seconds": 120,
  "permitted_write_root": "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z",
  "expected": {
    "exit": 1,
    "field": "status",
    "value": "INVALID",
    "read_only_root": null,
    "before_manifest": null
  },
  "start_utc": "2026-09-13T15:51:06.826208+00:00",
  "stdin_sha256": null
}
```

Exit: 1; timeout: False. Raw output: `commands/selection-duplicate-selection/stdout.txt`, `stderr.txt`.

## selection-missing-capability

```json
{
  "case": "selection-missing-capability",
  "argv": [
    "C:\\Program Files\\Python310\\python.exe",
    "-B",
    "-X",
    "utf8",
    "C:\\Projects\\DevForgeAI\\src\\agents\\skills\\skill-builder\\scripts\\adaptive.py",
    "plan-set",
    "--selection",
    "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z\\fixtures\\independent-01\\records\\cap-selection.json"
  ],
  "cwd": "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z",
  "timeout_seconds": 120,
  "permitted_write_root": "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z",
  "expected": {
    "exit": 1,
    "field": "status",
    "value": "INVALID",
    "read_only_root": null,
    "before_manifest": null
  },
  "start_utc": "2026-09-13T15:51:07.116410+00:00",
  "stdin_sha256": null
}
```

Exit: 1; timeout: False. Raw output: `commands/selection-missing-capability/stdout.txt`, `stderr.txt`.

## selection-missing-destination

```json
{
  "case": "selection-missing-destination",
  "argv": [
    "C:\\Program Files\\Python310\\python.exe",
    "-B",
    "-X",
    "utf8",
    "C:\\Projects\\DevForgeAI\\src\\agents\\skills\\skill-builder\\scripts\\adaptive.py",
    "plan-set",
    "--selection",
    "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z\\fixtures\\independent-01\\records\\selection-missing-destination.json"
  ],
  "cwd": "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z",
  "timeout_seconds": 120,
  "permitted_write_root": "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z",
  "expected": {
    "exit": 1,
    "field": "status",
    "value": "INVALID",
    "read_only_root": null,
    "before_manifest": null
  },
  "start_utc": "2026-09-13T15:51:06.662205+00:00",
  "stdin_sha256": null
}
```

Exit: 1; timeout: False. Raw output: `commands/selection-missing-destination/stdout.txt`, `stderr.txt`.

## selection-missing-selected-dependency

```json
{
  "case": "selection-missing-selected-dependency",
  "argv": [
    "C:\\Program Files\\Python310\\python.exe",
    "-B",
    "-X",
    "utf8",
    "C:\\Projects\\DevForgeAI\\src\\agents\\skills\\skill-builder\\scripts\\adaptive.py",
    "plan-set",
    "--selection",
    "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z\\fixtures\\independent-01\\records\\selection-missing-selected-dependency.json"
  ],
  "cwd": "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z",
  "timeout_seconds": 120,
  "permitted_write_root": "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z",
  "expected": {
    "exit": 1,
    "field": "status",
    "value": "INVALID",
    "read_only_root": null,
    "before_manifest": null
  },
  "start_utc": "2026-09-13T15:51:06.491205+00:00",
  "stdin_sha256": null
}
```

Exit: 1; timeout: False. Raw output: `commands/selection-missing-selected-dependency/stdout.txt`, `stderr.txt`.

## selection-occupied

```json
{
  "case": "selection-occupied",
  "argv": [
    "C:\\Program Files\\Python310\\python.exe",
    "-B",
    "-X",
    "utf8",
    "C:\\Projects\\DevForgeAI\\src\\agents\\skills\\skill-builder\\scripts\\adaptive.py",
    "plan-set",
    "--selection",
    "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z\\fixtures\\independent-01\\records\\selection.json"
  ],
  "cwd": "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z",
  "timeout_seconds": 120,
  "permitted_write_root": "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z",
  "expected": {
    "exit": 1,
    "field": "status",
    "value": "INVALID",
    "read_only_root": null,
    "before_manifest": null
  },
  "start_utc": "2026-09-13T15:51:06.926526+00:00",
  "stdin_sha256": null
}
```

Exit: 1; timeout: False. Raw output: `commands/selection-occupied/stdout.txt`, `stderr.txt`.

## static-review

```json
{
  "case": "static-review",
  "argv": [
    "python",
    "-B",
    "-X",
    "utf8",
    "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z\\static_review.py"
  ],
  "cwd": "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z",
  "timeout_seconds": 120,
  "permitted_write_root": "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z",
  "expected": "Tool identification only; no acceptance claim",
  "start_utc": "2026-09-13T16:34:05.039290+00:00",
  "stdin_sha256": null
}
```

Exit: 0; timeout: False. Raw output: `commands/static-review/stdout.txt`, `stderr.txt`.

## v2-author-adopt-begin

```json
{
  "case": "v2-author-adopt-begin",
  "argv": [
    "C:\\Program Files\\Python310\\python.exe",
    "-B",
    "-X",
    "utf8",
    "C:\\Projects\\DevForgeAI\\src\\agents\\skills\\skill-builder\\scripts\\authoring.py",
    "begin",
    "--contract",
    "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z\\fixtures\\followup-02\\author-adopt\\input-contract.json",
    "--run-root",
    "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z\\fixtures\\followup-02\\author-adopt\\docs\\plan\\author-adopt-run"
  ],
  "cwd": "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z",
  "timeout_seconds": 120,
  "permitted_write_root": "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z",
  "expected": {
    "exit": 0,
    "field": "state",
    "value": "STAGED",
    "read_only_root": null,
    "before_manifest": null
  },
  "start_utc": "2026-09-13T15:52:54.829011+00:00",
  "stdin_sha256": null
}
```

Exit: 0; timeout: False. Raw output: `commands/v2-author-adopt-begin/stdout.txt`, `stderr.txt`.

## v2-author-adopt-publish

```json
{
  "case": "v2-author-adopt-publish",
  "argv": [
    "C:\\Program Files\\Python310\\python.exe",
    "-B",
    "-X",
    "utf8",
    "C:\\Projects\\DevForgeAI\\src\\agents\\skills\\skill-builder\\scripts\\authoring.py",
    "publish",
    "--run-root",
    "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z\\fixtures\\followup-02\\author-adopt\\docs\\plan\\author-adopt-run"
  ],
  "cwd": "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z",
  "timeout_seconds": 120,
  "permitted_write_root": "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z",
  "expected": {
    "exit": 0,
    "field": "state",
    "value": "AUTHORED",
    "read_only_root": null,
    "before_manifest": null
  },
  "start_utc": "2026-09-13T15:52:55.022531+00:00",
  "stdin_sha256": null
}
```

Exit: 0; timeout: False. Raw output: `commands/v2-author-adopt-publish/stdout.txt`, `stderr.txt`.

## v2-author-corrupt-history

```json
{
  "case": "v2-author-corrupt-history",
  "argv": [
    "C:\\Program Files\\Python310\\python.exe",
    "-B",
    "-X",
    "utf8",
    "C:\\Projects\\DevForgeAI\\src\\agents\\skills\\skill-builder\\scripts\\authoring.py",
    "begin",
    "--contract",
    "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z\\fixtures\\followup-02\\author-corrupt\\input-contract.json",
    "--run-root",
    "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z\\fixtures\\followup-02\\author-corrupt\\docs\\plan\\run"
  ],
  "cwd": "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z",
  "timeout_seconds": 120,
  "permitted_write_root": "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z",
  "expected": {
    "exit": 2,
    "field": null,
    "value": null,
    "read_only_root": null,
    "before_manifest": null
  },
  "start_utc": "2026-09-13T15:52:55.419529+00:00",
  "stdin_sha256": null
}
```

Exit: 2; timeout: False. Raw output: `commands/v2-author-corrupt-history/stdout.txt`, `stderr.txt`.

## v2-author-create-begin

```json
{
  "case": "v2-author-create-begin",
  "argv": [
    "C:\\Program Files\\Python310\\python.exe",
    "-B",
    "-X",
    "utf8",
    "C:\\Projects\\DevForgeAI\\src\\agents\\skills\\skill-builder\\scripts\\authoring.py",
    "begin",
    "--contract",
    "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z\\fixtures\\followup-02\\authoring\\input-contract.json",
    "--run-root",
    "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z\\fixtures\\followup-02\\authoring\\docs\\plan\\authoring-run"
  ],
  "cwd": "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z",
  "timeout_seconds": 120,
  "permitted_write_root": "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z",
  "expected": {
    "exit": 0,
    "field": "state",
    "value": "STAGED",
    "read_only_root": null,
    "before_manifest": null
  },
  "start_utc": "2026-09-13T15:52:52.181787+00:00",
  "stdin_sha256": null
}
```

Exit: 0; timeout: False. Raw output: `commands/v2-author-create-begin/stdout.txt`, `stderr.txt`.

## v2-author-create-publish

```json
{
  "case": "v2-author-create-publish",
  "argv": [
    "C:\\Program Files\\Python310\\python.exe",
    "-B",
    "-X",
    "utf8",
    "C:\\Projects\\DevForgeAI\\src\\agents\\skills\\skill-builder\\scripts\\authoring.py",
    "publish",
    "--run-root",
    "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z\\fixtures\\followup-02\\authoring\\docs\\plan\\authoring-run"
  ],
  "cwd": "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z",
  "timeout_seconds": 120,
  "permitted_write_root": "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z",
  "expected": {
    "exit": 0,
    "field": "state",
    "value": "AUTHORED",
    "read_only_root": null,
    "before_manifest": null
  },
  "start_utc": "2026-09-13T15:52:52.311956+00:00",
  "stdin_sha256": null
}
```

Exit: 0; timeout: False. Raw output: `commands/v2-author-create-publish/stdout.txt`, `stderr.txt`.

## v2-author-drift-begin

```json
{
  "case": "v2-author-drift-begin",
  "argv": [
    "C:\\Program Files\\Python310\\python.exe",
    "-B",
    "-X",
    "utf8",
    "C:\\Projects\\DevForgeAI\\src\\agents\\skills\\skill-builder\\scripts\\authoring.py",
    "begin",
    "--contract",
    "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z\\fixtures\\followup-02\\author-drift\\input-contract.json",
    "--run-root",
    "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z\\fixtures\\followup-02\\author-drift\\docs\\plan\\author-drift-run"
  ],
  "cwd": "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z",
  "timeout_seconds": 120,
  "permitted_write_root": "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z",
  "expected": {
    "exit": 0,
    "field": "state",
    "value": "STAGED",
    "read_only_root": null,
    "before_manifest": null
  },
  "start_utc": "2026-09-13T15:52:55.521588+00:00",
  "stdin_sha256": null
}
```

Exit: 0; timeout: False. Raw output: `commands/v2-author-drift-begin/stdout.txt`, `stderr.txt`.

## v2-author-drift-publish

```json
{
  "case": "v2-author-drift-publish",
  "argv": [
    "C:\\Program Files\\Python310\\python.exe",
    "-B",
    "-X",
    "utf8",
    "C:\\Projects\\DevForgeAI\\src\\agents\\skills\\skill-builder\\scripts\\authoring.py",
    "publish",
    "--run-root",
    "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z\\fixtures\\followup-02\\author-drift\\docs\\plan\\author-drift-run"
  ],
  "cwd": "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z",
  "timeout_seconds": 120,
  "permitted_write_root": "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z",
  "expected": {
    "exit": 1,
    "field": "state",
    "value": "BLOCKED",
    "read_only_root": null,
    "before_manifest": null
  },
  "start_utc": "2026-09-13T15:52:55.730269+00:00",
  "stdin_sha256": null
}
```

Exit: 1; timeout: False. Raw output: `commands/v2-author-drift-publish/stdout.txt`, `stderr.txt`.

## v2-author-edit-begin

```json
{
  "case": "v2-author-edit-begin",
  "argv": [
    "C:\\Program Files\\Python310\\python.exe",
    "-B",
    "-X",
    "utf8",
    "C:\\Projects\\DevForgeAI\\src\\agents\\skills\\skill-builder\\scripts\\authoring.py",
    "begin",
    "--contract",
    "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z\\fixtures\\followup-02\\authoring\\edit\\input-contract.json",
    "--run-root",
    "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z\\fixtures\\followup-02\\authoring\\docs\\plan\\edit-run"
  ],
  "cwd": "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z",
  "timeout_seconds": 120,
  "permitted_write_root": "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z",
  "expected": {
    "exit": 0,
    "field": "state",
    "value": "STAGED",
    "read_only_root": null,
    "before_manifest": null
  },
  "start_utc": "2026-09-13T15:52:52.629117+00:00",
  "stdin_sha256": null
}
```

Exit: 0; timeout: False. Raw output: `commands/v2-author-edit-begin/stdout.txt`, `stderr.txt`.

## v2-author-edit-publish

```json
{
  "case": "v2-author-edit-publish",
  "argv": [
    "C:\\Program Files\\Python310\\python.exe",
    "-B",
    "-X",
    "utf8",
    "C:\\Projects\\DevForgeAI\\src\\agents\\skills\\skill-builder\\scripts\\authoring.py",
    "publish",
    "--run-root",
    "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z\\fixtures\\followup-02\\authoring\\docs\\plan\\edit-run"
  ],
  "cwd": "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z",
  "timeout_seconds": 120,
  "permitted_write_root": "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z",
  "expected": {
    "exit": 0,
    "field": "state",
    "value": "AUTHORED",
    "read_only_root": null,
    "before_manifest": null
  },
  "start_utc": "2026-09-13T15:52:52.856123+00:00",
  "stdin_sha256": null
}
```

Exit: 0; timeout: False. Raw output: `commands/v2-author-edit-publish/stdout.txt`, `stderr.txt`.

## v2-author-extra-contract-field

```json
{
  "case": "v2-author-extra-contract-field",
  "argv": [
    "C:\\Program Files\\Python310\\python.exe",
    "-B",
    "-X",
    "utf8",
    "C:\\Projects\\DevForgeAI\\src\\agents\\skills\\skill-builder\\scripts\\authoring.py",
    "begin",
    "--contract",
    "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z\\fixtures\\followup-02\\author-extra-field\\input-contract.json",
    "--run-root",
    "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z\\fixtures\\followup-02\\author-extra-field\\docs\\plan\\run"
  ],
  "cwd": "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z",
  "timeout_seconds": 120,
  "permitted_write_root": "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z",
  "expected": {
    "exit": 2,
    "field": null,
    "value": null,
    "read_only_root": null,
    "before_manifest": null
  },
  "start_utc": "2026-09-13T15:52:56.354784+00:00",
  "stdin_sha256": null
}
```

Exit: 0; timeout: False. Raw output: `commands/v2-author-extra-contract-field/stdout.txt`, `stderr.txt`.

## v2-author-import-begin

```json
{
  "case": "v2-author-import-begin",
  "argv": [
    "C:\\Program Files\\Python310\\python.exe",
    "-B",
    "-X",
    "utf8",
    "C:\\Projects\\DevForgeAI\\src\\agents\\skills\\skill-builder\\scripts\\authoring.py",
    "begin",
    "--contract",
    "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z\\fixtures\\followup-02\\author-import\\input-contract.json",
    "--run-root",
    "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z\\fixtures\\followup-02\\author-import\\docs\\plan\\author-import-run"
  ],
  "cwd": "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z",
  "timeout_seconds": 120,
  "permitted_write_root": "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z",
  "expected": {
    "exit": 0,
    "field": "state",
    "value": "STAGED",
    "read_only_root": null,
    "before_manifest": null
  },
  "start_utc": "2026-09-13T15:52:53.945932+00:00",
  "stdin_sha256": null
}
```

Exit: 0; timeout: False. Raw output: `commands/v2-author-import-begin/stdout.txt`, `stderr.txt`.

## v2-author-import-publish

```json
{
  "case": "v2-author-import-publish",
  "argv": [
    "C:\\Program Files\\Python310\\python.exe",
    "-B",
    "-X",
    "utf8",
    "C:\\Projects\\DevForgeAI\\src\\agents\\skills\\skill-builder\\scripts\\authoring.py",
    "publish",
    "--run-root",
    "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z\\fixtures\\followup-02\\author-import\\docs\\plan\\author-import-run"
  ],
  "cwd": "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z",
  "timeout_seconds": 120,
  "permitted_write_root": "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z",
  "expected": {
    "exit": 0,
    "field": "state",
    "value": "AUTHORED",
    "read_only_root": null,
    "before_manifest": null
  },
  "start_utc": "2026-09-13T15:52:54.064664+00:00",
  "stdin_sha256": null
}
```

Exit: 0; timeout: False. Raw output: `commands/v2-author-import-publish/stdout.txt`, `stderr.txt`.

## v2-author-observed-begin

```json
{
  "case": "v2-author-observed-begin",
  "argv": [
    "C:\\Program Files\\Python310\\python.exe",
    "-B",
    "-X",
    "utf8",
    "C:\\Projects\\DevForgeAI\\src\\agents\\skills\\skill-builder\\scripts\\authoring.py",
    "begin",
    "--contract",
    "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z\\fixtures\\followup-02\\author-observed\\input-contract.json",
    "--run-root",
    "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z\\fixtures\\followup-02\\author-observed\\docs\\plan\\author-observed-run"
  ],
  "cwd": "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z",
  "timeout_seconds": 120,
  "permitted_write_root": "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z",
  "expected": {
    "exit": 0,
    "field": "state",
    "value": "STAGED",
    "read_only_root": null,
    "before_manifest": null
  },
  "start_utc": "2026-09-13T15:52:53.301824+00:00",
  "stdin_sha256": null
}
```

Exit: 0; timeout: False. Raw output: `commands/v2-author-observed-begin/stdout.txt`, `stderr.txt`.

## v2-author-observed-publish

```json
{
  "case": "v2-author-observed-publish",
  "argv": [
    "C:\\Program Files\\Python310\\python.exe",
    "-B",
    "-X",
    "utf8",
    "C:\\Projects\\DevForgeAI\\src\\agents\\skills\\skill-builder\\scripts\\authoring.py",
    "publish",
    "--run-root",
    "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z\\fixtures\\followup-02\\author-observed\\docs\\plan\\author-observed-run"
  ],
  "cwd": "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z",
  "timeout_seconds": 120,
  "permitted_write_root": "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z",
  "expected": {
    "exit": 0,
    "field": "state",
    "value": "AUTHORED",
    "read_only_root": null,
    "before_manifest": null
  },
  "start_utc": "2026-09-13T15:52:53.512686+00:00",
  "stdin_sha256": null
}
```

Exit: 0; timeout: False. Raw output: `commands/v2-author-observed-publish/stdout.txt`, `stderr.txt`.

## v2-author-outside-scope-begin

```json
{
  "case": "v2-author-outside-scope-begin",
  "argv": [
    "C:\\Program Files\\Python310\\python.exe",
    "-B",
    "-X",
    "utf8",
    "C:\\Projects\\DevForgeAI\\src\\agents\\skills\\skill-builder\\scripts\\authoring.py",
    "begin",
    "--contract",
    "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z\\fixtures\\followup-02\\author-outside-scope\\input-contract.json",
    "--run-root",
    "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z\\fixtures\\followup-02\\author-outside-scope\\docs\\plan\\author-outside-scope-run"
  ],
  "cwd": "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z",
  "timeout_seconds": 120,
  "permitted_write_root": "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z",
  "expected": {
    "exit": 0,
    "field": "state",
    "value": "STAGED",
    "read_only_root": null,
    "before_manifest": null
  },
  "start_utc": "2026-09-13T15:52:55.944782+00:00",
  "stdin_sha256": null
}
```

Exit: 0; timeout: False. Raw output: `commands/v2-author-outside-scope-begin/stdout.txt`, `stderr.txt`.

## v2-author-outside-scope-publish

```json
{
  "case": "v2-author-outside-scope-publish",
  "argv": [
    "C:\\Program Files\\Python310\\python.exe",
    "-B",
    "-X",
    "utf8",
    "C:\\Projects\\DevForgeAI\\src\\agents\\skills\\skill-builder\\scripts\\authoring.py",
    "publish",
    "--run-root",
    "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z\\fixtures\\followup-02\\author-outside-scope\\docs\\plan\\author-outside-scope-run"
  ],
  "cwd": "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z",
  "timeout_seconds": 120,
  "permitted_write_root": "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z",
  "expected": {
    "exit": 1,
    "field": "state",
    "value": "BLOCKED",
    "read_only_root": null,
    "before_manifest": null
  },
  "start_utc": "2026-09-13T15:52:56.126788+00:00",
  "stdin_sha256": null
}
```

Exit: 1; timeout: False. Raw output: `commands/v2-author-outside-scope-publish/stdout.txt`, `stderr.txt`.

## v2-author-spec_build-begin

```json
{
  "case": "v2-author-spec_build-begin",
  "argv": [
    "C:\\Program Files\\Python310\\python.exe",
    "-B",
    "-X",
    "utf8",
    "C:\\Projects\\DevForgeAI\\src\\agents\\skills\\skill-builder\\scripts\\authoring.py",
    "begin",
    "--contract",
    "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z\\fixtures\\followup-02\\author-spec_build\\input-contract.json",
    "--run-root",
    "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z\\fixtures\\followup-02\\author-spec_build\\docs\\plan\\author-spec_build-run"
  ],
  "cwd": "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z",
  "timeout_seconds": 120,
  "permitted_write_root": "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z",
  "expected": {
    "exit": 0,
    "field": "state",
    "value": "STAGED",
    "read_only_root": null,
    "before_manifest": null
  },
  "start_utc": "2026-09-13T15:52:54.392665+00:00",
  "stdin_sha256": null
}
```

Exit: 0; timeout: False. Raw output: `commands/v2-author-spec_build-begin/stdout.txt`, `stderr.txt`.

## v2-author-spec_build-publish

```json
{
  "case": "v2-author-spec_build-publish",
  "argv": [
    "C:\\Program Files\\Python310\\python.exe",
    "-B",
    "-X",
    "utf8",
    "C:\\Projects\\DevForgeAI\\src\\agents\\skills\\skill-builder\\scripts\\authoring.py",
    "publish",
    "--run-root",
    "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z\\fixtures\\followup-02\\author-spec_build\\docs\\plan\\author-spec_build-run"
  ],
  "cwd": "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z",
  "timeout_seconds": 120,
  "permitted_write_root": "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z",
  "expected": {
    "exit": 0,
    "field": "state",
    "value": "AUTHORED",
    "read_only_root": null,
    "before_manifest": null
  },
  "start_utc": "2026-09-13T15:52:54.505663+00:00",
  "stdin_sha256": null
}
```

Exit: 0; timeout: False. Raw output: `commands/v2-author-spec_build-publish/stdout.txt`, `stderr.txt`.

## v2-bcn-divergent-begin

```json
{
  "case": "v2-bcn-divergent-begin",
  "argv": [
    "C:\\Program Files\\Python310\\python.exe",
    "-B",
    "-X",
    "utf8",
    "C:\\Projects\\DevForgeAI\\src\\agents\\skills\\skill-builder\\scripts\\authoring.py",
    "begin",
    "--contract",
    "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z\\fixtures\\followup-02\\bcn-divergent\\second\\input-contract.json",
    "--run-root",
    "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z\\fixtures\\followup-02\\bcn-divergent\\docs\\plan\\second-run"
  ],
  "cwd": "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z",
  "timeout_seconds": 120,
  "permitted_write_root": "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z",
  "expected": {
    "exit": 0,
    "field": "state",
    "value": "STAGED",
    "read_only_root": null,
    "before_manifest": null
  },
  "start_utc": "2026-09-13T15:52:59.865336+00:00",
  "stdin_sha256": null
}
```

Exit: 0; timeout: False. Raw output: `commands/v2-bcn-divergent-begin/stdout.txt`, `stderr.txt`.

## v2-bcn-divergent-publish

```json
{
  "case": "v2-bcn-divergent-publish",
  "argv": [
    "C:\\Program Files\\Python310\\python.exe",
    "-B",
    "-X",
    "utf8",
    "C:\\Projects\\DevForgeAI\\src\\agents\\skills\\skill-builder\\scripts\\authoring.py",
    "publish",
    "--run-root",
    "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z\\fixtures\\followup-02\\bcn-divergent\\docs\\plan\\second-run"
  ],
  "cwd": "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z",
  "timeout_seconds": 120,
  "permitted_write_root": "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z",
  "expected": {
    "exit": 1,
    "field": "state",
    "value": "BLOCKED",
    "read_only_root": null,
    "before_manifest": null
  },
  "start_utc": "2026-09-13T15:53:00.061402+00:00",
  "stdin_sha256": null
}
```

Exit: 1; timeout: False. Raw output: `commands/v2-bcn-divergent-publish/stdout.txt`, `stderr.txt`.

## v2-bcn-divergent-seed-begin

```json
{
  "case": "v2-bcn-divergent-seed-begin",
  "argv": [
    "C:\\Program Files\\Python310\\python.exe",
    "-B",
    "-X",
    "utf8",
    "C:\\Projects\\DevForgeAI\\src\\agents\\skills\\skill-builder\\scripts\\authoring.py",
    "begin",
    "--contract",
    "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z\\fixtures\\followup-02\\bcn-divergent\\input-contract.json",
    "--run-root",
    "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z\\fixtures\\followup-02\\bcn-divergent\\docs\\plan\\bcn-divergent-run"
  ],
  "cwd": "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z",
  "timeout_seconds": 120,
  "permitted_write_root": "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z",
  "expected": {
    "exit": 0,
    "field": "state",
    "value": "STAGED",
    "read_only_root": null,
    "before_manifest": null
  },
  "start_utc": "2026-09-13T15:52:59.432060+00:00",
  "stdin_sha256": null
}
```

Exit: 0; timeout: False. Raw output: `commands/v2-bcn-divergent-seed-begin/stdout.txt`, `stderr.txt`.

## v2-bcn-divergent-seed-publish

```json
{
  "case": "v2-bcn-divergent-seed-publish",
  "argv": [
    "C:\\Program Files\\Python310\\python.exe",
    "-B",
    "-X",
    "utf8",
    "C:\\Projects\\DevForgeAI\\src\\agents\\skills\\skill-builder\\scripts\\authoring.py",
    "publish",
    "--run-root",
    "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z\\fixtures\\followup-02\\bcn-divergent\\docs\\plan\\bcn-divergent-run"
  ],
  "cwd": "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z",
  "timeout_seconds": 120,
  "permitted_write_root": "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z",
  "expected": {
    "exit": 0,
    "field": "state",
    "value": "AUTHORED",
    "read_only_root": null,
    "before_manifest": null
  },
  "start_utc": "2026-09-13T15:52:59.578061+00:00",
  "stdin_sha256": null
}
```

Exit: 0; timeout: False. Raw output: `commands/v2-bcn-divergent-seed-publish/stdout.txt`, `stderr.txt`.

## v2-bcn-equal-base-begin

```json
{
  "case": "v2-bcn-equal-base-begin",
  "argv": [
    "C:\\Program Files\\Python310\\python.exe",
    "-B",
    "-X",
    "utf8",
    "C:\\Projects\\DevForgeAI\\src\\agents\\skills\\skill-builder\\scripts\\authoring.py",
    "begin",
    "--contract",
    "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z\\fixtures\\followup-02\\bcn-equal-base\\second\\input-contract.json",
    "--run-root",
    "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z\\fixtures\\followup-02\\bcn-equal-base\\docs\\plan\\second-run"
  ],
  "cwd": "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z",
  "timeout_seconds": 120,
  "permitted_write_root": "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z",
  "expected": {
    "exit": 0,
    "field": "state",
    "value": "STAGED",
    "read_only_root": null,
    "before_manifest": null
  },
  "start_utc": "2026-09-13T15:52:56.890004+00:00",
  "stdin_sha256": null
}
```

Exit: 0; timeout: False. Raw output: `commands/v2-bcn-equal-base-begin/stdout.txt`, `stderr.txt`.

## v2-bcn-equal-base-publish

```json
{
  "case": "v2-bcn-equal-base-publish",
  "argv": [
    "C:\\Program Files\\Python310\\python.exe",
    "-B",
    "-X",
    "utf8",
    "C:\\Projects\\DevForgeAI\\src\\agents\\skills\\skill-builder\\scripts\\authoring.py",
    "publish",
    "--run-root",
    "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z\\fixtures\\followup-02\\bcn-equal-base\\docs\\plan\\second-run"
  ],
  "cwd": "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z",
  "timeout_seconds": 120,
  "permitted_write_root": "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z",
  "expected": {
    "exit": 0,
    "field": "state",
    "value": "AUTHORED",
    "read_only_root": null,
    "before_manifest": null
  },
  "start_utc": "2026-09-13T15:52:57.090761+00:00",
  "stdin_sha256": null
}
```

Exit: 0; timeout: False. Raw output: `commands/v2-bcn-equal-base-publish/stdout.txt`, `stderr.txt`.

## v2-bcn-equal-base-seed-begin

```json
{
  "case": "v2-bcn-equal-base-seed-begin",
  "argv": [
    "C:\\Program Files\\Python310\\python.exe",
    "-B",
    "-X",
    "utf8",
    "C:\\Projects\\DevForgeAI\\src\\agents\\skills\\skill-builder\\scripts\\authoring.py",
    "begin",
    "--contract",
    "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z\\fixtures\\followup-02\\bcn-equal-base\\input-contract.json",
    "--run-root",
    "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z\\fixtures\\followup-02\\bcn-equal-base\\docs\\plan\\bcn-equal-base-run"
  ],
  "cwd": "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z",
  "timeout_seconds": 120,
  "permitted_write_root": "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z",
  "expected": {
    "exit": 0,
    "field": "state",
    "value": "STAGED",
    "read_only_root": null,
    "before_manifest": null
  },
  "start_utc": "2026-09-13T15:52:56.461787+00:00",
  "stdin_sha256": null
}
```

Exit: 0; timeout: False. Raw output: `commands/v2-bcn-equal-base-seed-begin/stdout.txt`, `stderr.txt`.

## v2-bcn-equal-base-seed-publish

```json
{
  "case": "v2-bcn-equal-base-seed-publish",
  "argv": [
    "C:\\Program Files\\Python310\\python.exe",
    "-B",
    "-X",
    "utf8",
    "C:\\Projects\\DevForgeAI\\src\\agents\\skills\\skill-builder\\scripts\\authoring.py",
    "publish",
    "--run-root",
    "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z\\fixtures\\followup-02\\bcn-equal-base\\docs\\plan\\bcn-equal-base-run"
  ],
  "cwd": "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z",
  "timeout_seconds": 120,
  "permitted_write_root": "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z",
  "expected": {
    "exit": 0,
    "field": "state",
    "value": "AUTHORED",
    "read_only_root": null,
    "before_manifest": null
  },
  "start_utc": "2026-09-13T15:52:56.572783+00:00",
  "stdin_sha256": null
}
```

Exit: 0; timeout: False. Raw output: `commands/v2-bcn-equal-base-seed-publish/stdout.txt`, `stderr.txt`.

## v2-bcn-equal-new-begin

```json
{
  "case": "v2-bcn-equal-new-begin",
  "argv": [
    "C:\\Program Files\\Python310\\python.exe",
    "-B",
    "-X",
    "utf8",
    "C:\\Projects\\DevForgeAI\\src\\agents\\skills\\skill-builder\\scripts\\authoring.py",
    "begin",
    "--contract",
    "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z\\fixtures\\followup-02\\bcn-equal-new\\second\\input-contract.json",
    "--run-root",
    "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z\\fixtures\\followup-02\\bcn-equal-new\\docs\\plan\\second-run"
  ],
  "cwd": "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z",
  "timeout_seconds": 120,
  "permitted_write_root": "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z",
  "expected": {
    "exit": 0,
    "field": "state",
    "value": "STAGED",
    "read_only_root": null,
    "before_manifest": null
  },
  "start_utc": "2026-09-13T15:52:57.884294+00:00",
  "stdin_sha256": null
}
```

Exit: 0; timeout: False. Raw output: `commands/v2-bcn-equal-new-begin/stdout.txt`, `stderr.txt`.

## v2-bcn-equal-new-publish

```json
{
  "case": "v2-bcn-equal-new-publish",
  "argv": [
    "C:\\Program Files\\Python310\\python.exe",
    "-B",
    "-X",
    "utf8",
    "C:\\Projects\\DevForgeAI\\src\\agents\\skills\\skill-builder\\scripts\\authoring.py",
    "publish",
    "--run-root",
    "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z\\fixtures\\followup-02\\bcn-equal-new\\docs\\plan\\second-run"
  ],
  "cwd": "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z",
  "timeout_seconds": 120,
  "permitted_write_root": "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z",
  "expected": {
    "exit": 0,
    "field": "state",
    "value": "AUTHORED",
    "read_only_root": null,
    "before_manifest": null
  },
  "start_utc": "2026-09-13T15:52:58.067905+00:00",
  "stdin_sha256": null
}
```

Exit: 0; timeout: False. Raw output: `commands/v2-bcn-equal-new-publish/stdout.txt`, `stderr.txt`.

## v2-bcn-equal-new-seed-begin

```json
{
  "case": "v2-bcn-equal-new-seed-begin",
  "argv": [
    "C:\\Program Files\\Python310\\python.exe",
    "-B",
    "-X",
    "utf8",
    "C:\\Projects\\DevForgeAI\\src\\agents\\skills\\skill-builder\\scripts\\authoring.py",
    "begin",
    "--contract",
    "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z\\fixtures\\followup-02\\bcn-equal-new\\input-contract.json",
    "--run-root",
    "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z\\fixtures\\followup-02\\bcn-equal-new\\docs\\plan\\bcn-equal-new-run"
  ],
  "cwd": "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z",
  "timeout_seconds": 120,
  "permitted_write_root": "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z",
  "expected": {
    "exit": 0,
    "field": "state",
    "value": "STAGED",
    "read_only_root": null,
    "before_manifest": null
  },
  "start_utc": "2026-09-13T15:52:57.484762+00:00",
  "stdin_sha256": null
}
```

Exit: 0; timeout: False. Raw output: `commands/v2-bcn-equal-new-seed-begin/stdout.txt`, `stderr.txt`.

## v2-bcn-equal-new-seed-publish

```json
{
  "case": "v2-bcn-equal-new-seed-publish",
  "argv": [
    "C:\\Program Files\\Python310\\python.exe",
    "-B",
    "-X",
    "utf8",
    "C:\\Projects\\DevForgeAI\\src\\agents\\skills\\skill-builder\\scripts\\authoring.py",
    "publish",
    "--run-root",
    "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z\\fixtures\\followup-02\\bcn-equal-new\\docs\\plan\\bcn-equal-new-run"
  ],
  "cwd": "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z",
  "timeout_seconds": 120,
  "permitted_write_root": "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z",
  "expected": {
    "exit": 0,
    "field": "state",
    "value": "AUTHORED",
    "read_only_root": null,
    "before_manifest": null
  },
  "start_utc": "2026-09-13T15:52:57.587761+00:00",
  "stdin_sha256": null
}
```

Exit: 0; timeout: False. Raw output: `commands/v2-bcn-equal-new-seed-publish/stdout.txt`, `stderr.txt`.

## v2-bcn-new-equal-base-begin

```json
{
  "case": "v2-bcn-new-equal-base-begin",
  "argv": [
    "C:\\Program Files\\Python310\\python.exe",
    "-B",
    "-X",
    "utf8",
    "C:\\Projects\\DevForgeAI\\src\\agents\\skills\\skill-builder\\scripts\\authoring.py",
    "begin",
    "--contract",
    "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z\\fixtures\\followup-02\\bcn-new-equal-base\\second\\input-contract.json",
    "--run-root",
    "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z\\fixtures\\followup-02\\bcn-new-equal-base\\docs\\plan\\second-run"
  ],
  "cwd": "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z",
  "timeout_seconds": 120,
  "permitted_write_root": "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z",
  "expected": {
    "exit": 0,
    "field": "state",
    "value": "STAGED",
    "read_only_root": null,
    "before_manifest": null
  },
  "start_utc": "2026-09-13T15:52:58.857119+00:00",
  "stdin_sha256": null
}
```

Exit: 0; timeout: False. Raw output: `commands/v2-bcn-new-equal-base-begin/stdout.txt`, `stderr.txt`.

## v2-bcn-new-equal-base-publish

```json
{
  "case": "v2-bcn-new-equal-base-publish",
  "argv": [
    "C:\\Program Files\\Python310\\python.exe",
    "-B",
    "-X",
    "utf8",
    "C:\\Projects\\DevForgeAI\\src\\agents\\skills\\skill-builder\\scripts\\authoring.py",
    "publish",
    "--run-root",
    "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z\\fixtures\\followup-02\\bcn-new-equal-base\\docs\\plan\\second-run"
  ],
  "cwd": "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z",
  "timeout_seconds": 120,
  "permitted_write_root": "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z",
  "expected": {
    "exit": 0,
    "field": "state",
    "value": "AUTHORED",
    "read_only_root": null,
    "before_manifest": null
  },
  "start_utc": "2026-09-13T15:52:59.058141+00:00",
  "stdin_sha256": null
}
```

Exit: 0; timeout: False. Raw output: `commands/v2-bcn-new-equal-base-publish/stdout.txt`, `stderr.txt`.

## v2-bcn-new-equal-base-seed-begin

```json
{
  "case": "v2-bcn-new-equal-base-seed-begin",
  "argv": [
    "C:\\Program Files\\Python310\\python.exe",
    "-B",
    "-X",
    "utf8",
    "C:\\Projects\\DevForgeAI\\src\\agents\\skills\\skill-builder\\scripts\\authoring.py",
    "begin",
    "--contract",
    "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z\\fixtures\\followup-02\\bcn-new-equal-base\\input-contract.json",
    "--run-root",
    "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z\\fixtures\\followup-02\\bcn-new-equal-base\\docs\\plan\\bcn-new-equal-base-run"
  ],
  "cwd": "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z",
  "timeout_seconds": 120,
  "permitted_write_root": "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z",
  "expected": {
    "exit": 0,
    "field": "state",
    "value": "STAGED",
    "read_only_root": null,
    "before_manifest": null
  },
  "start_utc": "2026-09-13T15:52:58.426904+00:00",
  "stdin_sha256": null
}
```

Exit: 0; timeout: False. Raw output: `commands/v2-bcn-new-equal-base-seed-begin/stdout.txt`, `stderr.txt`.

## v2-bcn-new-equal-base-seed-publish

```json
{
  "case": "v2-bcn-new-equal-base-seed-publish",
  "argv": [
    "C:\\Program Files\\Python310\\python.exe",
    "-B",
    "-X",
    "utf8",
    "C:\\Projects\\DevForgeAI\\src\\agents\\skills\\skill-builder\\scripts\\authoring.py",
    "publish",
    "--run-root",
    "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z\\fixtures\\followup-02\\bcn-new-equal-base\\docs\\plan\\bcn-new-equal-base-run"
  ],
  "cwd": "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z",
  "timeout_seconds": 120,
  "permitted_write_root": "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z",
  "expected": {
    "exit": 0,
    "field": "state",
    "value": "AUTHORED",
    "read_only_root": null,
    "before_manifest": null
  },
  "start_utc": "2026-09-13T15:52:58.528904+00:00",
  "stdin_sha256": null
}
```

Exit: 0; timeout: False. Raw output: `commands/v2-bcn-new-equal-base-seed-publish/stdout.txt`, `stderr.txt`.

## v2-bcn-obsolete-user-edit-begin

```json
{
  "case": "v2-bcn-obsolete-user-edit-begin",
  "argv": [
    "C:\\Program Files\\Python310\\python.exe",
    "-B",
    "-X",
    "utf8",
    "C:\\Projects\\DevForgeAI\\src\\agents\\skills\\skill-builder\\scripts\\authoring.py",
    "begin",
    "--contract",
    "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z\\fixtures\\followup-02\\bcn-obsolete-user-edit\\second\\input-contract.json",
    "--run-root",
    "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z\\fixtures\\followup-02\\bcn-obsolete-user-edit\\docs\\plan\\second-run"
  ],
  "cwd": "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z",
  "timeout_seconds": 120,
  "permitted_write_root": "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z",
  "expected": {
    "exit": 0,
    "field": "state",
    "value": "STAGED",
    "read_only_root": null,
    "before_manifest": null
  },
  "start_utc": "2026-09-13T15:53:00.703707+00:00",
  "stdin_sha256": null
}
```

Exit: 0; timeout: False. Raw output: `commands/v2-bcn-obsolete-user-edit-begin/stdout.txt`, `stderr.txt`.

## v2-bcn-obsolete-user-edit-publish

```json
{
  "case": "v2-bcn-obsolete-user-edit-publish",
  "argv": [
    "C:\\Program Files\\Python310\\python.exe",
    "-B",
    "-X",
    "utf8",
    "C:\\Projects\\DevForgeAI\\src\\agents\\skills\\skill-builder\\scripts\\authoring.py",
    "publish",
    "--run-root",
    "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z\\fixtures\\followup-02\\bcn-obsolete-user-edit\\docs\\plan\\second-run"
  ],
  "cwd": "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z",
  "timeout_seconds": 120,
  "permitted_write_root": "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z",
  "expected": {
    "exit": 1,
    "field": "state",
    "value": "BLOCKED",
    "read_only_root": null,
    "before_manifest": null
  },
  "start_utc": "2026-09-13T15:53:00.887217+00:00",
  "stdin_sha256": null
}
```

Exit: 1; timeout: False. Raw output: `commands/v2-bcn-obsolete-user-edit-publish/stdout.txt`, `stderr.txt`.

## v2-bcn-obsolete-user-edit-seed-begin

```json
{
  "case": "v2-bcn-obsolete-user-edit-seed-begin",
  "argv": [
    "C:\\Program Files\\Python310\\python.exe",
    "-B",
    "-X",
    "utf8",
    "C:\\Projects\\DevForgeAI\\src\\agents\\skills\\skill-builder\\scripts\\authoring.py",
    "begin",
    "--contract",
    "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z\\fixtures\\followup-02\\bcn-obsolete-user-edit\\input-contract.json",
    "--run-root",
    "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z\\fixtures\\followup-02\\bcn-obsolete-user-edit\\docs\\plan\\bcn-obsolete-user-edit-run"
  ],
  "cwd": "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z",
  "timeout_seconds": 120,
  "permitted_write_root": "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z",
  "expected": {
    "exit": 0,
    "field": "state",
    "value": "STAGED",
    "read_only_root": null,
    "before_manifest": null
  },
  "start_utc": "2026-09-13T15:53:00.283684+00:00",
  "stdin_sha256": null
}
```

Exit: 0; timeout: False. Raw output: `commands/v2-bcn-obsolete-user-edit-seed-begin/stdout.txt`, `stderr.txt`.

## v2-bcn-obsolete-user-edit-seed-publish

```json
{
  "case": "v2-bcn-obsolete-user-edit-seed-publish",
  "argv": [
    "C:\\Program Files\\Python310\\python.exe",
    "-B",
    "-X",
    "utf8",
    "C:\\Projects\\DevForgeAI\\src\\agents\\skills\\skill-builder\\scripts\\authoring.py",
    "publish",
    "--run-root",
    "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z\\fixtures\\followup-02\\bcn-obsolete-user-edit\\docs\\plan\\bcn-obsolete-user-edit-run"
  ],
  "cwd": "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z",
  "timeout_seconds": 120,
  "permitted_write_root": "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z",
  "expected": {
    "exit": 0,
    "field": "state",
    "value": "AUTHORED",
    "read_only_root": null,
    "before_manifest": null
  },
  "start_utc": "2026-09-13T15:53:00.417688+00:00",
  "stdin_sha256": null
}
```

Exit: 0; timeout: False. Raw output: `commands/v2-bcn-obsolete-user-edit-seed-publish/stdout.txt`, `stderr.txt`.

## v2-set-A-preflight-fails

```json
{
  "case": "v2-set-A-preflight-fails",
  "argv": [
    "C:\\Program Files\\Python310\\python.exe",
    "-B",
    "-X",
    "utf8",
    "C:\\Projects\\DevForgeAI\\src\\agents\\skills\\skill-builder\\scripts\\adaptive.py",
    "plan-set",
    "--selection",
    "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z\\fixtures\\followup-02\\records\\selection.json"
  ],
  "cwd": "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z",
  "timeout_seconds": 120,
  "permitted_write_root": "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z",
  "expected": {
    "exit": 1,
    "field": "status",
    "value": "INVALID",
    "read_only_root": null,
    "before_manifest": null
  },
  "start_utc": "2026-09-13T15:53:01.110234+00:00",
  "stdin_sha256": null
}
```

Exit: 1; timeout: False. Raw output: `commands/v2-set-A-preflight-fails/stdout.txt`, `stderr.txt`.

## v2-set-C-begin

```json
{
  "case": "v2-set-C-begin",
  "argv": [
    "C:\\Program Files\\Python310\\python.exe",
    "-B",
    "-X",
    "utf8",
    "C:\\Projects\\DevForgeAI\\src\\agents\\skills\\skill-builder\\scripts\\authoring.py",
    "begin",
    "--contract",
    "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z\\fixtures\\followup-02\\records\\set-c\\input-contract.json",
    "--run-root",
    "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z\\fixtures\\followup-02\\records\\docs\\plan\\set-c-run"
  ],
  "cwd": "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z",
  "timeout_seconds": 120,
  "permitted_write_root": "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z",
  "expected": {
    "exit": 0,
    "field": "state",
    "value": "STAGED",
    "read_only_root": null,
    "before_manifest": null
  },
  "start_utc": "2026-09-13T15:53:01.305233+00:00",
  "stdin_sha256": null
}
```

Exit: 0; timeout: False. Raw output: `commands/v2-set-C-begin/stdout.txt`, `stderr.txt`.

## v2-set-C-complete-begin

```json
{
  "case": "v2-set-C-complete-begin",
  "argv": [
    "C:\\Program Files\\Python310\\python.exe",
    "-B",
    "-X",
    "utf8",
    "C:\\Projects\\DevForgeAI\\src\\agents\\skills\\skill-builder\\scripts\\authoring.py",
    "begin",
    "--contract",
    "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z\\fixtures\\followup-02\\records\\set-c-complete\\input-contract.json",
    "--run-root",
    "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z\\fixtures\\followup-02\\records\\docs\\plan\\set-c-complete-run"
  ],
  "cwd": "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z",
  "timeout_seconds": 120,
  "permitted_write_root": "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z",
  "expected": {
    "exit": 0,
    "field": "state",
    "value": "STAGED",
    "read_only_root": null,
    "before_manifest": null
  },
  "start_utc": "2026-09-13T15:53:01.423031+00:00",
  "stdin_sha256": null
}
```

Exit: 0; timeout: False. Raw output: `commands/v2-set-C-complete-begin/stdout.txt`, `stderr.txt`.

## v2-set-C-publish

```json
{
  "case": "v2-set-C-publish",
  "argv": [
    "C:\\Program Files\\Python310\\python.exe",
    "-B",
    "-X",
    "utf8",
    "C:\\Projects\\DevForgeAI\\src\\agents\\skills\\skill-builder\\scripts\\authoring.py",
    "publish",
    "--run-root",
    "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z\\fixtures\\followup-02\\records\\docs\\plan\\set-c-complete-run"
  ],
  "cwd": "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z",
  "timeout_seconds": 120,
  "permitted_write_root": "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z",
  "expected": {
    "exit": 0,
    "field": "state",
    "value": "AUTHORED",
    "read_only_root": null,
    "before_manifest": null
  },
  "start_utc": "2026-09-13T15:53:01.534090+00:00",
  "stdin_sha256": null
}
```

Exit: 0; timeout: False. Raw output: `commands/v2-set-C-publish/stdout.txt`, `stderr.txt`.

## v2-set-extra-member

```json
{
  "case": "v2-set-extra-member",
  "argv": [
    "C:\\Program Files\\Python310\\python.exe",
    "-B",
    "-X",
    "utf8",
    "C:\\Projects\\DevForgeAI\\src\\agents\\skills\\skill-builder\\scripts\\adaptive.py",
    "inspect",
    "--record",
    "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z\\fixtures\\followup-02\\records\\extra-member.json"
  ],
  "cwd": "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z",
  "timeout_seconds": 120,
  "permitted_write_root": "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z",
  "expected": {
    "exit": 1,
    "field": "status",
    "value": "INVALID",
    "read_only_root": null,
    "before_manifest": null
  },
  "start_utc": "2026-09-13T15:53:04.321108+00:00",
  "stdin_sha256": null
}
```

Exit: 1; timeout: False. Raw output: `commands/v2-set-extra-member/stdout.txt`, `stderr.txt`.

## v2-set-false-aggregate

```json
{
  "case": "v2-set-false-aggregate",
  "argv": [
    "C:\\Program Files\\Python310\\python.exe",
    "-B",
    "-X",
    "utf8",
    "C:\\Projects\\DevForgeAI\\src\\agents\\skills\\skill-builder\\scripts\\adaptive.py",
    "inspect",
    "--record",
    "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z\\fixtures\\followup-02\\records\\false-aggregate.json"
  ],
  "cwd": "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z",
  "timeout_seconds": 120,
  "permitted_write_root": "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z",
  "expected": {
    "exit": 1,
    "field": "status",
    "value": "INVALID",
    "read_only_root": null,
    "before_manifest": null
  },
  "start_utc": "2026-09-13T15:53:04.831982+00:00",
  "stdin_sha256": null
}
```

Exit: 1; timeout: False. Raw output: `commands/v2-set-false-aggregate/stdout.txt`, `stderr.txt`.

## v2-set-false-full

```json
{
  "case": "v2-set-false-full",
  "argv": [
    "C:\\Program Files\\Python310\\python.exe",
    "-B",
    "-X",
    "utf8",
    "C:\\Projects\\DevForgeAI\\src\\agents\\skills\\skill-builder\\scripts\\adaptive.py",
    "inspect",
    "--record",
    "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z\\fixtures\\followup-02\\records\\false-full.json"
  ],
  "cwd": "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z",
  "timeout_seconds": 120,
  "permitted_write_root": "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z",
  "expected": {
    "exit": 1,
    "field": "status",
    "value": "INVALID",
    "read_only_root": null,
    "before_manifest": null
  },
  "start_utc": "2026-09-13T15:53:03.347949+00:00",
  "stdin_sha256": null
}
```

Exit: 1; timeout: False. Raw output: `commands/v2-set-false-full/stdout.txt`, `stderr.txt`.

## v2-set-forged-legacy-fields

```json
{
  "case": "v2-set-forged-legacy-fields",
  "argv": [
    "C:\\Program Files\\Python310\\python.exe",
    "-B",
    "-X",
    "utf8",
    "C:\\Projects\\DevForgeAI\\src\\agents\\skills\\skill-builder\\scripts\\adaptive.py",
    "inspect",
    "--record",
    "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z\\fixtures\\followup-02\\records\\forged-result.json"
  ],
  "cwd": "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z",
  "timeout_seconds": 120,
  "permitted_write_root": "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z",
  "expected": {
    "exit": 1,
    "field": "status",
    "value": "INVALID",
    "read_only_root": null,
    "before_manifest": null
  },
  "start_utc": "2026-09-13T15:53:05.229493+00:00",
  "stdin_sha256": null
}
```

Exit: 0; timeout: False. Raw output: `commands/v2-set-forged-legacy-fields/stdout.txt`, `stderr.txt`.

## v2-set-missing-omission

```json
{
  "case": "v2-set-missing-omission",
  "argv": [
    "C:\\Program Files\\Python310\\python.exe",
    "-B",
    "-X",
    "utf8",
    "C:\\Projects\\DevForgeAI\\src\\agents\\skills\\skill-builder\\scripts\\adaptive.py",
    "inspect",
    "--record",
    "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z\\fixtures\\followup-02\\records\\missing-omission.json"
  ],
  "cwd": "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z",
  "timeout_seconds": 120,
  "permitted_write_root": "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z",
  "expected": {
    "exit": 1,
    "field": "status",
    "value": "INVALID",
    "read_only_root": null,
    "before_manifest": null
  },
  "start_utc": "2026-09-13T15:53:03.847605+00:00",
  "stdin_sha256": null
}
```

Exit: 1; timeout: False. Raw output: `commands/v2-set-missing-omission/stdout.txt`, `stderr.txt`.

## v2-set-partial-result-valid

```json
{
  "case": "v2-set-partial-result-valid",
  "argv": [
    "C:\\Program Files\\Python310\\python.exe",
    "-B",
    "-X",
    "utf8",
    "C:\\Projects\\DevForgeAI\\src\\agents\\skills\\skill-builder\\scripts\\adaptive.py",
    "inspect",
    "--record",
    "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z\\fixtures\\followup-02\\records\\set-result.json"
  ],
  "cwd": "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z",
  "timeout_seconds": 120,
  "permitted_write_root": "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z",
  "expected": {
    "exit": 0,
    "field": "status",
    "value": "VALID",
    "read_only_root": null,
    "before_manifest": null
  },
  "start_utc": "2026-09-13T15:53:02.031737+00:00",
  "stdin_sha256": null
}
```

Exit: 0; timeout: False. Raw output: `commands/v2-set-partial-result-valid/stdout.txt`, `stderr.txt`.

## v2-set-subset-valid

```json
{
  "case": "v2-set-subset-valid",
  "argv": [
    "C:\\Program Files\\Python310\\python.exe",
    "-B",
    "-X",
    "utf8",
    "C:\\Projects\\DevForgeAI\\src\\agents\\skills\\skill-builder\\scripts\\adaptive.py",
    "inspect",
    "--record",
    "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z\\fixtures\\followup-02\\records\\set-request.json"
  ],
  "cwd": "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z",
  "timeout_seconds": 120,
  "permitted_write_root": "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z",
  "expected": {
    "exit": 0,
    "field": "status",
    "value": "VALID",
    "read_only_root": null,
    "before_manifest": null
  },
  "start_utc": "2026-09-13T15:53:02.623438+00:00",
  "stdin_sha256": null
}
```

Exit: 0; timeout: False. Raw output: `commands/v2-set-subset-valid/stdout.txt`, `stderr.txt`.

## windows-exact-bytes

```json
{
  "case": "windows-exact-bytes",
  "argv": [
    "C:\\Program Files\\Python310\\python.exe",
    "-B",
    "-X",
    "utf8",
    "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z\\fixtures\\platform-windows\\exact-bytes\\space é & ; $ ' (p)\\.agents\\skills\\summary-skill\\scripts\\check_project_binding.py",
    "--project-root",
    "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z\\fixtures\\platform-windows\\exact-bytes\\space é & ; $ ' (p)",
    "--skill-root",
    "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z\\fixtures\\platform-windows\\exact-bytes\\space é & ; $ ' (p)\\.agents\\skills\\summary-skill"
  ],
  "cwd": "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z",
  "timeout_seconds": 120,
  "permitted_write_root": "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z",
  "expected": {
    "exit": 0,
    "field": "reason_code",
    "value": "BOUND",
    "read_only_root": null,
    "before_manifest": null
  },
  "start_utc": "2026-09-13T16:22:24.964211+00:00",
  "stdin_sha256": null
}
```

Exit: 0; timeout: False. Raw output: `commands/windows-exact-bytes/stdout.txt`, `stderr.txt`.

## windows-exact-files

```json
{
  "case": "windows-exact-files",
  "argv": [
    "C:\\Program Files\\Python310\\python.exe",
    "-B",
    "-X",
    "utf8",
    "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z\\fixtures\\platform-windows\\exact-files\\space é & ; $ ' (p)\\.agents\\skills\\summary-skill\\scripts\\check_project_binding.py",
    "--project-root",
    "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z\\fixtures\\platform-windows\\exact-files\\space é & ; $ ' (p)",
    "--skill-root",
    "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z\\fixtures\\platform-windows\\exact-files\\space é & ; $ ' (p)\\.agents\\skills\\summary-skill"
  ],
  "cwd": "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z",
  "timeout_seconds": 120,
  "permitted_write_root": "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z",
  "expected": {
    "exit": 0,
    "field": "reason_code",
    "value": "BOUND",
    "read_only_root": null,
    "before_manifest": null
  },
  "start_utc": "2026-09-13T16:21:44.120685+00:00",
  "stdin_sha256": null
}
```

Exit: 0; timeout: False. Raw output: `commands/windows-exact-files/stdout.txt`, `stderr.txt`.

## windows-junction-setup

```json
{
  "case": "windows-junction-setup",
  "argv": [
    "powershell.exe",
    "-NoProfile",
    "-Command",
    "New-Item -ItemType Junction -Path 'C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z\\fixtures\\platform-windows\\symlink\\space é & ; $ '' (p)\\.agents\\skills\\summary-skill\\linked' -Target 'C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z\\fixtures\\platform-windows\\link-target' | Out-Null"
  ],
  "cwd": "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z",
  "timeout_seconds": 120,
  "permitted_write_root": "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z",
  "expected": "Create synthetic junction within disposable fixture",
  "start_utc": "2026-09-13T16:21:42.155419+00:00",
  "stdin_sha256": null
}
```

Exit: 0; timeout: False. Raw output: `commands/windows-junction-setup/stdout.txt`, `stderr.txt`.

## windows-missing

```json
{
  "case": "windows-missing",
  "argv": [
    "C:\\Program Files\\Python310\\python.exe",
    "-B",
    "-X",
    "utf8",
    "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z\\fixtures\\platform-windows\\missing\\space é & ; $ ' (p)\\.agents\\skills\\summary-skill\\scripts\\check_project_binding.py",
    "--project-root",
    "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z\\fixtures\\platform-windows\\missing\\space é & ; $ ' (p)",
    "--skill-root",
    "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z\\fixtures\\platform-windows\\missing\\space é & ; $ ' (p)\\.agents\\skills\\summary-skill"
  ],
  "cwd": "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z",
  "timeout_seconds": 120,
  "permitted_write_root": "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z",
  "expected": {
    "exit": 1,
    "field": "reason_code",
    "value": "MISSING_BINDING",
    "read_only_root": null,
    "before_manifest": null
  },
  "start_utc": "2026-09-13T16:21:42.058648+00:00",
  "stdin_sha256": null
}
```

Exit: 1; timeout: False. Raw output: `commands/windows-missing/stdout.txt`, `stderr.txt`.

## windows-over-bytes

```json
{
  "case": "windows-over-bytes",
  "argv": [
    "C:\\Program Files\\Python310\\python.exe",
    "-B",
    "-X",
    "utf8",
    "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z\\fixtures\\platform-windows\\over-bytes\\space é & ; $ ' (p)\\.agents\\skills\\summary-skill\\scripts\\check_project_binding.py",
    "--project-root",
    "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z\\fixtures\\platform-windows\\over-bytes\\space é & ; $ ' (p)",
    "--skill-root",
    "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z\\fixtures\\platform-windows\\over-bytes\\space é & ; $ ' (p)\\.agents\\skills\\summary-skill"
  ],
  "cwd": "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z",
  "timeout_seconds": 120,
  "permitted_write_root": "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z",
  "expected": {
    "exit": 2,
    "field": "reason_code",
    "value": "CAPTURE_LIMIT",
    "read_only_root": null,
    "before_manifest": null
  },
  "start_utc": "2026-09-13T16:22:25.346474+00:00",
  "stdin_sha256": null
}
```

Exit: 2; timeout: False. Raw output: `commands/windows-over-bytes/stdout.txt`, `stderr.txt`.

## windows-over-files

```json
{
  "case": "windows-over-files",
  "argv": [
    "C:\\Program Files\\Python310\\python.exe",
    "-B",
    "-X",
    "utf8",
    "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z\\fixtures\\platform-windows\\over-files\\space é & ; $ ' (p)\\.agents\\skills\\summary-skill\\scripts\\check_project_binding.py",
    "--project-root",
    "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z\\fixtures\\platform-windows\\over-files\\space é & ; $ ' (p)",
    "--skill-root",
    "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z\\fixtures\\platform-windows\\over-files\\space é & ; $ ' (p)\\.agents\\skills\\summary-skill"
  ],
  "cwd": "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z",
  "timeout_seconds": 120,
  "permitted_write_root": "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z",
  "expected": {
    "exit": 2,
    "field": "reason_code",
    "value": "CAPTURE_LIMIT",
    "read_only_root": null,
    "before_manifest": null
  },
  "start_utc": "2026-09-13T16:22:11.877876+00:00",
  "stdin_sha256": null
}
```

Exit: 2; timeout: False. Raw output: `commands/windows-over-files/stdout.txt`, `stderr.txt`.

## windows-pfx-name

```json
{
  "case": "windows-pfx-name",
  "argv": [
    "C:\\Program Files\\Python310\\python.exe",
    "-B",
    "-X",
    "utf8",
    "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z\\fixtures\\platform-windows\\pfx-name\\space é & ; $ ' (p)\\.agents\\skills\\summary-skill\\scripts\\check_project_binding.py",
    "--project-root",
    "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z\\fixtures\\platform-windows\\pfx-name\\space é & ; $ ' (p)",
    "--skill-root",
    "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z\\fixtures\\platform-windows\\pfx-name\\space é & ; $ ' (p)\\.agents\\skills\\summary-skill"
  ],
  "cwd": "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z",
  "timeout_seconds": 120,
  "permitted_write_root": "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z",
  "expected": {
    "exit": 1,
    "field": "reason_code",
    "value": "UNSAFE_PATH",
    "read_only_root": null,
    "before_manifest": null
  },
  "start_utc": "2026-09-13T16:21:42.764835+00:00",
  "stdin_sha256": null
}
```

Exit: 0; timeout: False. Raw output: `commands/windows-pfx-name/stdout.txt`, `stderr.txt`.

## windows-private-key-name

```json
{
  "case": "windows-private-key-name",
  "argv": [
    "C:\\Program Files\\Python310\\python.exe",
    "-B",
    "-X",
    "utf8",
    "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z\\fixtures\\platform-windows\\private-key-name\\space é & ; $ ' (p)\\.agents\\skills\\summary-skill\\scripts\\check_project_binding.py",
    "--project-root",
    "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z\\fixtures\\platform-windows\\private-key-name\\space é & ; $ ' (p)",
    "--skill-root",
    "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z\\fixtures\\platform-windows\\private-key-name\\space é & ; $ ' (p)\\.agents\\skills\\summary-skill"
  ],
  "cwd": "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z",
  "timeout_seconds": 120,
  "permitted_write_root": "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z",
  "expected": {
    "exit": 1,
    "field": "reason_code",
    "value": "UNSAFE_PATH",
    "read_only_root": null,
    "before_manifest": null
  },
  "start_utc": "2026-09-13T16:21:42.539304+00:00",
  "stdin_sha256": null
}
```

Exit: 0; timeout: False. Raw output: `commands/windows-private-key-name/stdout.txt`, `stderr.txt`.

## windows-relocated

```json
{
  "case": "windows-relocated",
  "argv": [
    "C:\\Program Files\\Python310\\python.exe",
    "-B",
    "-X",
    "utf8",
    "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z\\fixtures\\platform-windows\\relocated\\space é & ; $ ' (p)\\.agents\\skills\\summary-skill\\scripts\\check_project_binding.py",
    "--project-root",
    "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z\\fixtures\\platform-windows\\relocated\\space é & ; $ ' (p)",
    "--skill-root",
    "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z\\fixtures\\platform-windows\\relocated\\space é & ; $ ' (p)\\.agents\\skills\\summary-skill"
  ],
  "cwd": "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z",
  "timeout_seconds": 120,
  "permitted_write_root": "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z",
  "expected": {
    "exit": 1,
    "field": "reason_code",
    "value": "ROOT_MISMATCH",
    "read_only_root": null,
    "before_manifest": null
  },
  "start_utc": "2026-09-13T16:21:41.959648+00:00",
  "stdin_sha256": null
}
```

Exit: 1; timeout: False. Raw output: `commands/windows-relocated/stdout.txt`, `stderr.txt`.

## windows-symlink

```json
{
  "case": "windows-symlink",
  "argv": [
    "C:\\Program Files\\Python310\\python.exe",
    "-B",
    "-X",
    "utf8",
    "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z\\fixtures\\platform-windows\\symlink\\space é & ; $ ' (p)\\.agents\\skills\\summary-skill\\scripts\\check_project_binding.py",
    "--project-root",
    "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z\\fixtures\\platform-windows\\symlink\\space é & ; $ ' (p)",
    "--skill-root",
    "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z\\fixtures\\platform-windows\\symlink\\space é & ; $ ' (p)\\.agents\\skills\\summary-skill"
  ],
  "cwd": "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z",
  "timeout_seconds": 120,
  "permitted_write_root": "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z",
  "expected": {
    "exit": 1,
    "field": "reason_code",
    "value": "UNSAFE_PATH",
    "read_only_root": null,
    "before_manifest": null
  },
  "start_utc": "2026-09-13T16:21:42.422298+00:00",
  "stdin_sha256": null
}
```

Exit: 1; timeout: False. Raw output: `commands/windows-symlink/stdout.txt`, `stderr.txt`.

## windows-valid

```json
{
  "case": "windows-valid",
  "argv": [
    "C:\\Program Files\\Python310\\python.exe",
    "-B",
    "-X",
    "utf8",
    "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z\\fixtures\\platform-windows\\valid\\space é & ; $ ' (p)\\.agents\\skills\\summary-skill\\scripts\\check_project_binding.py",
    "--project-root",
    "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z\\fixtures\\platform-windows\\valid\\space é & ; $ ' (p)",
    "--skill-root",
    "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z\\fixtures\\platform-windows\\valid\\space é & ; $ ' (p)\\.agents\\skills\\summary-skill"
  ],
  "cwd": "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z",
  "timeout_seconds": 120,
  "permitted_write_root": "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-independent-qa\\skill-builder\\20260913T152822695886Z",
  "expected": {
    "exit": 0,
    "field": "reason_code",
    "value": "BOUND",
    "read_only_root": null,
    "before_manifest": null
  },
  "start_utc": "2026-09-13T16:21:41.760649+00:00",
  "stdin_sha256": null
}
```

Exit: 0; timeout: False. Raw output: `commands/windows-valid/stdout.txt`, `stderr.txt`.
