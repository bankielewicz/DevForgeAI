# Exact command/results log

See each plan/receipt for temporary roots, timestamps and stream digests. The full regression failure and pre-repair reproduction are retained. No failed command was silently retried.

## ADAPTIVE-RECORDS

```json
["C:\\Program Files\\Python310\\python.exe", "-B", "-X", "utf8", "C:\\Projects\\DevForgeAI\\src\\agents\\skills\\skill-validator\\scripts\\adaptive_observe.py", "records", "--run-root", "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-validations\\skill-validator\\20260913T211755666611Z\\supplemental-records"]
```

Cwd: `C:\Projects\DevForgeAI`. Start 2026-09-13T21:24:49.630415Z; end 2026-09-13T21:24:50.249884Z; elapsed 0.609s; exit 0; timed out False.
[stdout](commands/ADAPTIVE-RECORDS/stdout.txt) · [stderr](commands/ADAPTIVE-RECORDS/stderr.txt) · [receipt](commands/ADAPTIVE-RECORDS/receipt.json)

## BOUND-EVALUATOR

```json
["C:\\Program Files\\Python310\\python.exe", "-B", "-X", "utf8", "C:\\Projects\\DevForgeAI\\src\\agents\\skills\\skill-validator\\scripts\\run_evaluation.py", "--package-root", "C:\\Projects\\DevForgeAI\\src\\agents\\skills\\skill-validator", "--candidate-root", "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-validations\\skill-validator\\20260913T211755666611Z\\source", "--cases", "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-validations\\skill-validator\\20260913T211755666611Z\\source\\evals\\cases.jsonl", "--output", "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-validations\\skill-validator\\20260913T211755666611Z\\bound-evaluation.jsonl", "--run-id", "20260913T211755666611Z", "--profile", "legacy-import-v1"]
```

Cwd: `C:\Projects\DevForgeAI`. Start 2026-09-13T21:20:54.077279Z; end 2026-09-13T21:20:54.405302Z; elapsed 0.328s; exit 0; timed out False.
[stdout](commands/BOUND-EVALUATOR/stdout.txt) · [stderr](commands/BOUND-EVALUATOR/stderr.txt) · [receipt](commands/BOUND-EVALUATOR/receipt.json)

## COVERAGE-COMBINE

```json
["C:\\Program Files\\Python310\\python.exe", "-B", "-X", "utf8", "-m", "coverage", "combine", "--rcfile", "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-validations\\skill-validator\\20260913T211755666611Z\\coverage\\coverage.ini", "--keep"]
```

Cwd: `C:\Projects\DevForgeAI`. Start 2026-09-13T21:21:20.927697Z; end 2026-09-13T21:21:21.414299Z; elapsed 0.484s; exit 0; timed out False.
[stdout](commands/COVERAGE-COMBINE/stdout.txt) · [stderr](commands/COVERAGE-COMBINE/stderr.txt) · [receipt](commands/COVERAGE-COMBINE/receipt.json)

## COVERAGE-JSON

```json
["C:\\Program Files\\Python310\\python.exe", "-B", "-X", "utf8", "-m", "coverage", "json", "--rcfile", "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-validations\\skill-validator\\20260913T211755666611Z\\coverage\\coverage.ini", "-o", "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-validations\\skill-validator\\20260913T211755666611Z\\coverage\\coverage.json"]
```

Cwd: `C:\Projects\DevForgeAI`. Start 2026-09-13T21:21:21.419811Z; end 2026-09-13T21:21:21.861393Z; elapsed 0.437s; exit 0; timed out False.
[stdout](commands/COVERAGE-JSON/stdout.txt) · [stderr](commands/COVERAGE-JSON/stderr.txt) · [receipt](commands/COVERAGE-JSON/receipt.json)

## COVERAGE-REPORT

```json
["C:\\Program Files\\Python310\\python.exe", "-B", "-X", "utf8", "-m", "coverage", "report", "--rcfile", "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-validations\\skill-validator\\20260913T211755666611Z\\coverage\\coverage.ini"]
```

Cwd: `C:\Projects\DevForgeAI`. Start 2026-09-13T21:21:21.866396Z; end 2026-09-13T21:21:22.209911Z; elapsed 0.344s; exit 0; timed out False.
[stdout](commands/COVERAGE-REPORT/stdout.txt) · [stderr](commands/COVERAGE-REPORT/stderr.txt) · [receipt](commands/COVERAGE-REPORT/receipt.json)

## D01

```json
["C:\\Program Files\\Python310\\python.exe", "-B", "-X", "utf8", "C:\\Projects\\DevForgeAI\\src\\agents\\skills\\skill-validator\\scripts\\adaptive_observe.py", "records", "--run-root", "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-validations\\skill-validator\\20260913T211755666611Z\\trials\\D01\\records"]
```

Cwd: `C:\Projects\DevForgeAI`. Start 2026-09-13T21:20:11.260197Z; end 2026-09-13T21:20:11.833548Z; elapsed 0.578s; exit 1; timed out False.
[stdout](commands/D01/stdout.txt) · [stderr](commands/D01/stderr.txt) · [receipt](commands/D01/receipt.json)

## D02

```json
["C:\\Program Files\\Python310\\python.exe", "-B", "-X", "utf8", "C:\\Projects\\DevForgeAI\\src\\agents\\skills\\skill-validator\\scripts\\adaptive_observe.py", "records", "--run-root", "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-validations\\skill-validator\\20260913T211755666611Z\\trials\\D02\\records"]
```

Cwd: `C:\Projects\DevForgeAI`. Start 2026-09-13T21:20:11.922547Z; end 2026-09-13T21:20:12.486566Z; elapsed 0.562s; exit 1; timed out False.
[stdout](commands/D02/stdout.txt) · [stderr](commands/D02/stderr.txt) · [receipt](commands/D02/receipt.json)

## D03

```json
["C:\\Program Files\\Python310\\python.exe", "-B", "-X", "utf8", "C:\\Projects\\DevForgeAI\\src\\agents\\skills\\skill-validator\\scripts\\adaptive_observe.py", "records", "--run-root", "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-validations\\skill-validator\\20260913T211755666611Z\\trials\\D03\\records"]
```

Cwd: `C:\Projects\DevForgeAI`. Start 2026-09-13T21:20:12.574566Z; end 2026-09-13T21:20:13.190801Z; elapsed 0.610s; exit 1; timed out False.
[stdout](commands/D03/stdout.txt) · [stderr](commands/D03/stderr.txt) · [receipt](commands/D03/receipt.json)

## D04

```json
["C:\\Program Files\\Python310\\python.exe", "-B", "-X", "utf8", "C:\\Projects\\DevForgeAI\\src\\agents\\skills\\skill-validator\\scripts\\adaptive_observe.py", "records", "--run-root", "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-validations\\skill-validator\\20260913T211755666611Z\\trials\\D04\\records"]
```

Cwd: `C:\Projects\DevForgeAI`. Start 2026-09-13T21:20:13.296804Z; end 2026-09-13T21:20:13.965166Z; elapsed 0.672s; exit 0; timed out False.
[stdout](commands/D04/stdout.txt) · [stderr](commands/D04/stderr.txt) · [receipt](commands/D04/receipt.json)

## D05

```json
["C:\\Program Files\\Python310\\python.exe", "-B", "-X", "utf8", "C:\\Projects\\DevForgeAI\\src\\agents\\skills\\skill-validator\\scripts\\adaptive_observe.py", "records", "--run-root", "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-validations\\skill-validator\\20260913T211755666611Z\\trials\\D05\\records"]
```

Cwd: `C:\Projects\DevForgeAI`. Start 2026-09-13T21:20:14.067166Z; end 2026-09-13T21:20:15.110817Z; elapsed 1.031s; exit 0; timed out False.
[stdout](commands/D05/stdout.txt) · [stderr](commands/D05/stderr.txt) · [receipt](commands/D05/receipt.json)

## F01

```json
["C:\\Program Files\\Python310\\python.exe", "-B", "-X", "utf8", "C:\\Projects\\DevForgeAI\\src\\agents\\skills\\skill-validator\\scripts\\adaptive_observe.py", "package", "--source", "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-validations\\skill-validator\\20260913T211755666611Z\\trials\\F01\\sample"]
```

Cwd: `C:\Projects\DevForgeAI`. Start 2026-09-13T21:20:23.842368Z; end 2026-09-13T21:20:24.096368Z; elapsed 0.250s; exit 0; timed out False.
[stdout](commands/F01/stdout.txt) · [stderr](commands/F01/stderr.txt) · [receipt](commands/F01/receipt.json)

## F02

```json
["C:\\Program Files\\Python310\\python.exe", "-B", "-X", "utf8", "C:\\Projects\\DevForgeAI\\src\\agents\\skills\\skill-validator\\scripts\\adaptive_observe.py", "package", "--source", "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-validations\\skill-validator\\20260913T211755666611Z\\trials\\F02\\sample"]
```

Cwd: `C:\Projects\DevForgeAI`. Start 2026-09-13T21:20:24.114370Z; end 2026-09-13T21:20:24.372887Z; elapsed 0.250s; exit 0; timed out False.
[stdout](commands/F02/stdout.txt) · [stderr](commands/F02/stderr.txt) · [receipt](commands/F02/receipt.json)

## F03

```json
["C:\\Program Files\\Python310\\python.exe", "-B", "-X", "utf8", "C:\\Projects\\DevForgeAI\\src\\agents\\skills\\skill-validator\\scripts\\adaptive_observe.py", "package", "--source", "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-validations\\skill-validator\\20260913T211755666611Z\\trials\\F03\\sample"]
```

Cwd: `C:\Projects\DevForgeAI`. Start 2026-09-13T21:20:24.390887Z; end 2026-09-13T21:20:24.648889Z; elapsed 0.265s; exit 0; timed out False.
[stdout](commands/F03/stdout.txt) · [stderr](commands/F03/stderr.txt) · [receipt](commands/F03/receipt.json)

## F04

```json
["C:\\Program Files\\Python310\\python.exe", "-B", "-X", "utf8", "C:\\Projects\\DevForgeAI\\src\\agents\\skills\\skill-validator\\scripts\\adaptive_observe.py", "package", "--source", "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-validations\\skill-validator\\20260913T211755666611Z\\trials\\F04\\sample"]
```

Cwd: `C:\Projects\DevForgeAI`. Start 2026-09-13T21:20:24.668464Z; end 2026-09-13T21:20:24.936783Z; elapsed 0.266s; exit 0; timed out False.
[stdout](commands/F04/stdout.txt) · [stderr](commands/F04/stderr.txt) · [receipt](commands/F04/receipt.json)

## F05

```json
["C:\\Program Files\\Python310\\python.exe", "-B", "-X", "utf8", "C:\\Projects\\DevForgeAI\\src\\agents\\skills\\skill-validator\\scripts\\adaptive_observe.py", "package", "--source", "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-validations\\skill-validator\\20260913T211755666611Z\\trials\\F05\\sample"]
```

Cwd: `C:\Projects\DevForgeAI`. Start 2026-09-13T21:20:24.955781Z; end 2026-09-13T21:20:25.218650Z; elapsed 0.266s; exit 1; timed out False.
[stdout](commands/F05/stdout.txt) · [stderr](commands/F05/stderr.txt) · [receipt](commands/F05/receipt.json)

## F06

```json
["C:\\Program Files\\Python310\\python.exe", "-B", "-X", "utf8", "C:\\Projects\\DevForgeAI\\src\\agents\\skills\\skill-validator\\scripts\\adaptive_observe.py", "package", "--source", "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-validations\\skill-validator\\20260913T211755666611Z\\trials\\F06\\sample"]
```

Cwd: `C:\Projects\DevForgeAI`. Start 2026-09-13T21:20:25.235649Z; end 2026-09-13T21:20:25.496648Z; elapsed 0.266s; exit 1; timed out False.
[stdout](commands/F06/stdout.txt) · [stderr](commands/F06/stderr.txt) · [receipt](commands/F06/receipt.json)

## F07

```json
["C:\\Program Files\\Python310\\python.exe", "-B", "-X", "utf8", "C:\\Projects\\DevForgeAI\\src\\agents\\skills\\skill-validator\\scripts\\adaptive_observe.py", "package", "--source", "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-validations\\skill-validator\\20260913T211755666611Z\\trials\\F07\\sample"]
```

Cwd: `C:\Projects\DevForgeAI`. Start 2026-09-13T21:20:25.514364Z; end 2026-09-13T21:20:25.775366Z; elapsed 0.265s; exit 1; timed out False.
[stdout](commands/F07/stdout.txt) · [stderr](commands/F07/stderr.txt) · [receipt](commands/F07/receipt.json)

## F08

```json
["C:\\Program Files\\Python310\\python.exe", "-B", "-X", "utf8", "C:\\Projects\\DevForgeAI\\src\\agents\\skills\\skill-validator\\scripts\\adaptive_observe.py", "package", "--source", "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-validations\\skill-validator\\20260913T211755666611Z\\trials\\F08\\sample"]
```

Cwd: `C:\Projects\DevForgeAI`. Start 2026-09-13T21:20:25.792366Z; end 2026-09-13T21:20:26.060364Z; elapsed 0.266s; exit 1; timed out False.
[stdout](commands/F08/stdout.txt) · [stderr](commands/F08/stderr.txt) · [receipt](commands/F08/receipt.json)

## F09

```json
["C:\\Program Files\\Python310\\python.exe", "-B", "-X", "utf8", "C:\\Projects\\DevForgeAI\\src\\agents\\skills\\skill-validator\\scripts\\adaptive_observe.py", "package", "--source", "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-validations\\skill-validator\\20260913T211755666611Z\\trials\\F09\\sample"]
```

Cwd: `C:\Projects\DevForgeAI`. Start 2026-09-13T21:20:26.077363Z; end 2026-09-13T21:20:26.328879Z; elapsed 0.250s; exit 0; timed out False.
[stdout](commands/F09/stdout.txt) · [stderr](commands/F09/stderr.txt) · [receipt](commands/F09/receipt.json)

## F10

```json
["C:\\Program Files\\Python310\\python.exe", "-B", "-X", "utf8", "C:\\Projects\\DevForgeAI\\src\\agents\\skills\\skill-validator\\scripts\\adaptive_observe.py", "package", "--source", "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-validations\\skill-validator\\20260913T211755666611Z\\trials\\F10\\sample"]
```

Cwd: `C:\Projects\DevForgeAI`. Start 2026-09-13T21:20:26.350878Z; end 2026-09-13T21:20:26.616878Z; elapsed 0.266s; exit 0; timed out False.
[stdout](commands/F10/stdout.txt) · [stderr](commands/F10/stderr.txt) · [receipt](commands/F10/receipt.json)

## FIXTURE-AUDIT

```json
["C:\\Program Files\\Python310\\python.exe", "-B", "-X", "utf8", "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-validations\\skill-validator\\20260913T211755666611Z\\audit_fixtures.py"]
```

Cwd: `C:\Projects\DevForgeAI`. Start 2026-09-13T21:20:29.722297Z; end 2026-09-13T21:20:31.635468Z; elapsed 1.922s; exit 0; timed out False.
[stdout](commands/FIXTURE-AUDIT/stdout.txt) · [stderr](commands/FIXTURE-AUDIT/stderr.txt) · [receipt](commands/FIXTURE-AUDIT/receipt.json)

## FULL-REGRESSION

```json
["C:\\Program Files\\Python310\\python.exe", "-B", "-X", "utf8", "-m", "unittest", "discover", "-s", "src/agents/skills/skill-validator/tests", "-v"]
```

Cwd: `C:\Projects\DevForgeAI`. Start 2026-09-13T21:19:59.412837Z; end 2026-09-13T21:21:12.108448Z; elapsed 72.687s; exit 1; timed out False.
[stdout](commands/FULL-REGRESSION/stdout.txt) · [stderr](commands/FULL-REGRESSION/stderr.txt) · [receipt](commands/FULL-REGRESSION/receipt.json)

## H01

```json
["C:\\Program Files\\Python310\\python.exe", "-B", "-X", "utf8", "C:\\Projects\\DevForgeAI\\src\\agents\\skills\\skill-validator\\scripts\\adaptive_observe.py", "records", "--run-root", "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-validations\\skill-validator\\20260913T211755666611Z\\trials\\H01\\records"]
```

Cwd: `C:\Projects\DevForgeAI`. Start 2026-09-13T21:20:15.207833Z; end 2026-09-13T21:20:15.808645Z; elapsed 0.594s; exit 1; timed out False.
[stdout](commands/H01/stdout.txt) · [stderr](commands/H01/stderr.txt) · [receipt](commands/H01/receipt.json)

## H02

```json
["C:\\Program Files\\Python310\\python.exe", "-B", "-X", "utf8", "C:\\Projects\\DevForgeAI\\src\\agents\\skills\\skill-validator\\scripts\\adaptive_observe.py", "records", "--run-root", "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-validations\\skill-validator\\20260913T211755666611Z\\trials\\H02\\records"]
```

Cwd: `C:\Projects\DevForgeAI`. Start 2026-09-13T21:20:15.899223Z; end 2026-09-13T21:20:16.475733Z; elapsed 0.578s; exit 0; timed out False.
[stdout](commands/H02/stdout.txt) · [stderr](commands/H02/stderr.txt) · [receipt](commands/H02/receipt.json)

## H03

```json
["C:\\Program Files\\Python310\\python.exe", "-B", "-X", "utf8", "C:\\Projects\\DevForgeAI\\src\\agents\\skills\\skill-validator\\scripts\\adaptive_observe.py", "records", "--run-root", "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-validations\\skill-validator\\20260913T211755666611Z\\trials\\H03\\records"]
```

Cwd: `C:\Projects\DevForgeAI`. Start 2026-09-13T21:20:16.565733Z; end 2026-09-13T21:20:17.133737Z; elapsed 0.578s; exit 0; timed out False.
[stdout](commands/H03/stdout.txt) · [stderr](commands/H03/stderr.txt) · [receipt](commands/H03/receipt.json)

## H04

```json
["C:\\Program Files\\Python310\\python.exe", "-B", "-X", "utf8", "C:\\Projects\\DevForgeAI\\src\\agents\\skills\\skill-validator\\scripts\\adaptive_observe.py", "records", "--run-root", "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-validations\\skill-validator\\20260913T211755666611Z\\trials\\H04\\records"]
```

Cwd: `C:\Projects\DevForgeAI`. Start 2026-09-13T21:20:17.227747Z; end 2026-09-13T21:20:17.799748Z; elapsed 0.563s; exit 0; timed out False.
[stdout](commands/H04/stdout.txt) · [stderr](commands/H04/stderr.txt) · [receipt](commands/H04/receipt.json)

## H05

```json
["C:\\Program Files\\Python310\\python.exe", "-B", "-X", "utf8", "C:\\Projects\\DevForgeAI\\src\\agents\\skills\\skill-validator\\scripts\\adaptive_observe.py", "records", "--run-root", "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-validations\\skill-validator\\20260913T211755666611Z\\trials\\H05\\records"]
```

Cwd: `C:\Projects\DevForgeAI`. Start 2026-09-13T21:20:17.891747Z; end 2026-09-13T21:20:18.485451Z; elapsed 0.593s; exit 0; timed out False.
[stdout](commands/H05/stdout.txt) · [stderr](commands/H05/stderr.txt) · [receipt](commands/H05/receipt.json)

## H06

```json
["C:\\Program Files\\Python310\\python.exe", "-B", "-X", "utf8", "C:\\Projects\\DevForgeAI\\src\\agents\\skills\\skill-validator\\scripts\\adaptive_observe.py", "records", "--run-root", "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-validations\\skill-validator\\20260913T211755666611Z\\trials\\H06\\records"]
```

Cwd: `C:\Projects\DevForgeAI`. Start 2026-09-13T21:20:18.577454Z; end 2026-09-13T21:20:19.147159Z; elapsed 0.578s; exit 1; timed out False.
[stdout](commands/H06/stdout.txt) · [stderr](commands/H06/stderr.txt) · [receipt](commands/H06/receipt.json)

## H07

```json
["C:\\Program Files\\Python310\\python.exe", "-B", "-X", "utf8", "C:\\Projects\\DevForgeAI\\src\\agents\\skills\\skill-validator\\scripts\\adaptive_observe.py", "records", "--run-root", "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-validations\\skill-validator\\20260913T211755666611Z\\trials\\H07\\records"]
```

Cwd: `C:\Projects\DevForgeAI`. Start 2026-09-13T21:20:19.240160Z; end 2026-09-13T21:20:19.811667Z; elapsed 0.563s; exit 0; timed out False.
[stdout](commands/H07/stdout.txt) · [stderr](commands/H07/stderr.txt) · [receipt](commands/H07/receipt.json)

## H08

```json
["C:\\Program Files\\Python310\\python.exe", "-B", "-X", "utf8", "C:\\Projects\\DevForgeAI\\src\\agents\\skills\\skill-validator\\scripts\\adaptive_observe.py", "records", "--run-root", "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-validations\\skill-validator\\20260913T211755666611Z\\trials\\H08\\records"]
```

Cwd: `C:\Projects\DevForgeAI`. Start 2026-09-13T21:20:19.902668Z; end 2026-09-13T21:20:20.492615Z; elapsed 0.594s; exit 0; timed out False.
[stdout](commands/H08/stdout.txt) · [stderr](commands/H08/stderr.txt) · [receipt](commands/H08/receipt.json)

## H09

```json
["C:\\Program Files\\Python310\\python.exe", "-B", "-X", "utf8", "C:\\Projects\\DevForgeAI\\src\\agents\\skills\\skill-validator\\scripts\\adaptive_observe.py", "records", "--run-root", "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-validations\\skill-validator\\20260913T211755666611Z\\trials\\H09\\records"]
```

Cwd: `C:\Projects\DevForgeAI`. Start 2026-09-13T21:20:20.590939Z; end 2026-09-13T21:20:21.158035Z; elapsed 0.562s; exit 0; timed out False.
[stdout](commands/H09/stdout.txt) · [stderr](commands/H09/stderr.txt) · [receipt](commands/H09/receipt.json)

## H10

```json
["C:\\Program Files\\Python310\\python.exe", "-B", "-X", "utf8", "C:\\Projects\\DevForgeAI\\src\\agents\\skills\\skill-validator\\scripts\\adaptive_observe.py", "records", "--run-root", "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-validations\\skill-validator\\20260913T211755666611Z\\trials\\H10\\records"]
```

Cwd: `C:\Projects\DevForgeAI`. Start 2026-09-13T21:20:21.252035Z; end 2026-09-13T21:20:21.876798Z; elapsed 0.625s; exit 0; timed out False.
[stdout](commands/H10/stdout.txt) · [stderr](commands/H10/stderr.txt) · [receipt](commands/H10/receipt.json)

## H11

```json
["C:\\Program Files\\Python310\\python.exe", "-B", "-X", "utf8", "C:\\Projects\\DevForgeAI\\src\\agents\\skills\\skill-validator\\scripts\\adaptive_observe.py", "records", "--run-root", "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-validations\\skill-validator\\20260913T211755666611Z\\trials\\H11\\subset-records"]
```

Cwd: `C:\Projects\DevForgeAI`. Start 2026-09-13T21:20:28.838679Z; end 2026-09-13T21:20:29.689784Z; elapsed 0.844s; exit 0; timed out False.
[stdout](commands/H11/stdout.txt) · [stderr](commands/H11/stderr.txt) · [receipt](commands/H11/receipt.json)

## LEGACY-RECORDS

```json
["C:\\Program Files\\Python310\\python.exe", "-B", "-X", "utf8", "C:\\Projects\\DevForgeAI\\src\\agents\\skills\\skill-validator\\scripts\\observe.py", "records", "--run-root", "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-validations\\skill-validator\\20260913T211755666611Z\\member-records"]
```

Cwd: `C:\Projects\DevForgeAI`. Start 2026-09-13T21:24:48.829367Z; end 2026-09-13T21:24:49.625876Z; elapsed 0.797s; exit 0; timed out False.
[stdout](commands/LEGACY-RECORDS/stdout.txt) · [stderr](commands/LEGACY-RECORDS/stderr.txt) · [receipt](commands/LEGACY-RECORDS/receipt.json)

## PRE-REPAIR-FAILURE-CONTROL

```json
["C:\\Program Files\\Python310\\python.exe", "-B", "-X", "utf8", "-m", "unittest", "discover", "-s", "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-adaptive-implementations\\skill-validator\\20260913T211315150947Z\\source\\tests", "-p", "test_authoring.py", "-k", "malformed_contract", "-v"]
```

Cwd: `C:\Projects\DevForgeAI`. Start 2026-09-13T21:22:25.602704Z; end 2026-09-13T21:22:25.816330Z; elapsed 0.204s; exit 1; timed out False.
[stdout](commands/PRE-REPAIR-FAILURE-CONTROL/stdout.txt) · [stderr](commands/PRE-REPAIR-FAILURE-CONTROL/stderr.txt) · [receipt](commands/PRE-REPAIR-FAILURE-CONTROL/receipt.json)

## READBACK

```json
["C:\\Program Files\\Python310\\python.exe", "-B", "-X", "utf8", "C:\\Projects\\DevForgeAI\\.agents\\skills\\skill-validator\\scripts\\observe.py", "readback", "--source", "C:\\Projects\\DevForgeAI\\src\\agents\\skills\\skill-validator", "--manifest", "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-validations\\skill-validator\\20260913T211755666611Z\\source-manifest.json"]
```

Cwd: `C:\Projects\DevForgeAI`. Start 2026-09-13T21:20:54.409306Z; end 2026-09-13T21:20:55.049818Z; elapsed 0.641s; exit 0; timed out False.
[stdout](commands/READBACK/stdout.txt) · [stderr](commands/READBACK/stderr.txt) · [receipt](commands/READBACK/receipt.json)

## REPLAY-P07

```json
["C:\\Program Files\\Python310\\python.exe", "-B", "-X", "utf8", "C:\\Projects\\DevForgeAI\\src\\agents\\skills\\skill-validator\\scripts\\adaptive_observe.py", "package", "--source", "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-validations\\skill-validator\\20260913T152602912596Z\\trials\\independent\\P07\\sample"]
```

Cwd: `C:\Projects\DevForgeAI`. Start 2026-09-13T21:20:27.913112Z; end 2026-09-13T21:20:28.168626Z; elapsed 0.250s; exit 0; timed out False.
[stdout](commands/REPLAY-P07/stdout.txt) · [stderr](commands/REPLAY-P07/stderr.txt) · [receipt](commands/REPLAY-P07/receipt.json)

## REPLAY-P08

```json
["C:\\Program Files\\Python310\\python.exe", "-B", "-X", "utf8", "C:\\Projects\\DevForgeAI\\src\\agents\\skills\\skill-validator\\scripts\\adaptive_observe.py", "package", "--source", "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-validations\\skill-validator\\20260913T152602912596Z\\trials\\independent\\P08\\sample"]
```

Cwd: `C:\Projects\DevForgeAI`. Start 2026-09-13T21:20:28.187625Z; end 2026-09-13T21:20:28.449626Z; elapsed 0.265s; exit 2; timed out False.
[stdout](commands/REPLAY-P08/stdout.txt) · [stderr](commands/REPLAY-P08/stderr.txt) · [receipt](commands/REPLAY-P08/receipt.json)

## REPLAY-R06

```json
["C:\\Program Files\\Python310\\python.exe", "-B", "-X", "utf8", "C:\\Projects\\DevForgeAI\\src\\agents\\skills\\skill-validator\\scripts\\adaptive_observe.py", "records", "--run-root", "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-validations\\skill-validator\\20260913T152602912596Z\\trials\\independent\\R06"]
```

Cwd: `C:\Projects\DevForgeAI`. Start 2026-09-13T21:20:26.700877Z; end 2026-09-13T21:20:27.247499Z; elapsed 0.547s; exit 1; timed out False.
[stdout](commands/REPLAY-R06/stdout.txt) · [stderr](commands/REPLAY-R06/stderr.txt) · [receipt](commands/REPLAY-R06/receipt.json)

## REPLAY-R07

```json
["C:\\Program Files\\Python310\\python.exe", "-B", "-X", "utf8", "C:\\Projects\\DevForgeAI\\src\\agents\\skills\\skill-validator\\scripts\\adaptive_observe.py", "records", "--run-root", "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-validations\\skill-validator\\20260913T152602912596Z\\trials\\independent\\R07"]
```

Cwd: `C:\Projects\DevForgeAI`. Start 2026-09-13T21:20:27.331036Z; end 2026-09-13T21:20:27.895114Z; elapsed 0.578s; exit 1; timed out False.
[stdout](commands/REPLAY-R07/stdout.txt) · [stderr](commands/REPLAY-R07/stderr.txt) · [receipt](commands/REPLAY-R07/receipt.json)

## STRUCTURAL

```json
["C:\\Program Files\\Python310\\python.exe", "-B", "-X", "utf8", "C:\\Users\\bryan\\.codex\\skills\\.system\\skill-creator\\scripts\\quick_validate.py", "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-validations\\skill-validator\\20260913T211755666611Z\\source"]
```

Cwd: `C:\Projects\DevForgeAI`. Start 2026-09-13T21:20:53.885754Z; end 2026-09-13T21:20:54.072280Z; elapsed 0.187s; exit 0; timed out False.
[stdout](commands/STRUCTURAL/stdout.txt) · [stderr](commands/STRUCTURAL/stderr.txt) · [receipt](commands/STRUCTURAL/receipt.json)

## SUBSET-WRAPPER

```json
["C:\\Program Files\\Python310\\python.exe", "-B", "-X", "utf8", "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-validations\\skill-validator\\20260913T211755666611Z\\subset_control.py"]
```

Cwd: `C:\Projects\DevForgeAI`. Start 2026-09-13T21:20:28.458626Z; end 2026-09-13T21:20:29.717292Z; elapsed 1.250s; exit 0; timed out False.
[stdout](commands/SUBSET-WRAPPER/stdout.txt) · [stderr](commands/SUBSET-WRAPPER/stderr.txt) · [receipt](commands/SUBSET-WRAPPER/receipt.json)

## U01

```json
["C:\\Program Files\\Python310\\python.exe", "-B", "-X", "utf8", "C:\\Projects\\DevForgeAI\\src\\agents\\skills\\skill-validator\\scripts\\adaptive_observe.py", "package", "--source", "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-validations\\skill-validator\\20260913T211755666611Z\\trials\\U01\\sample"]
```

Cwd: `C:\Projects\DevForgeAI`. Start 2026-09-13T21:20:21.894797Z; end 2026-09-13T21:20:22.152309Z; elapsed 0.250s; exit 2; timed out False.
[stdout](commands/U01/stdout.txt) · [stderr](commands/U01/stderr.txt) · [receipt](commands/U01/receipt.json)

## U02

```json
["C:\\Program Files\\Python310\\python.exe", "-B", "-X", "utf8", "C:\\Projects\\DevForgeAI\\src\\agents\\skills\\skill-validator\\scripts\\adaptive_observe.py", "package", "--source", "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-validations\\skill-validator\\20260913T211755666611Z\\trials\\U02\\sample"]
```

Cwd: `C:\Projects\DevForgeAI`. Start 2026-09-13T21:20:22.170309Z; end 2026-09-13T21:20:22.426353Z; elapsed 0.266s; exit 2; timed out False.
[stdout](commands/U02/stdout.txt) · [stderr](commands/U02/stderr.txt) · [receipt](commands/U02/receipt.json)

## U03

```json
["C:\\Program Files\\Python310\\python.exe", "-B", "-X", "utf8", "C:\\Projects\\DevForgeAI\\src\\agents\\skills\\skill-validator\\scripts\\adaptive_observe.py", "package", "--source", "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-validations\\skill-validator\\20260913T211755666611Z\\trials\\U03\\sample"]
```

Cwd: `C:\Projects\DevForgeAI`. Start 2026-09-13T21:20:22.445620Z; end 2026-09-13T21:20:22.715128Z; elapsed 0.266s; exit 2; timed out False.
[stdout](commands/U03/stdout.txt) · [stderr](commands/U03/stderr.txt) · [receipt](commands/U03/receipt.json)

## U04

```json
["C:\\Program Files\\Python310\\python.exe", "-B", "-X", "utf8", "C:\\Projects\\DevForgeAI\\src\\agents\\skills\\skill-validator\\scripts\\adaptive_observe.py", "package", "--source", "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-validations\\skill-validator\\20260913T211755666611Z\\trials\\U04\\sample"]
```

Cwd: `C:\Projects\DevForgeAI`. Start 2026-09-13T21:20:22.733129Z; end 2026-09-13T21:20:22.995350Z; elapsed 0.266s; exit 0; timed out False.
[stdout](commands/U04/stdout.txt) · [stderr](commands/U04/stderr.txt) · [receipt](commands/U04/receipt.json)

## U05

```json
["C:\\Program Files\\Python310\\python.exe", "-B", "-X", "utf8", "C:\\Projects\\DevForgeAI\\src\\agents\\skills\\skill-validator\\scripts\\adaptive_observe.py", "package", "--source", "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-validations\\skill-validator\\20260913T211755666611Z\\trials\\U05\\sample"]
```

Cwd: `C:\Projects\DevForgeAI`. Start 2026-09-13T21:20:23.012354Z; end 2026-09-13T21:20:23.270865Z; elapsed 0.265s; exit 0; timed out False.
[stdout](commands/U05/stdout.txt) · [stderr](commands/U05/stderr.txt) · [receipt](commands/U05/receipt.json)

## U06

```json
["C:\\Program Files\\Python310\\python.exe", "-B", "-X", "utf8", "C:\\Projects\\DevForgeAI\\src\\agents\\skills\\skill-validator\\scripts\\adaptive_observe.py", "package", "--source", "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-validations\\skill-validator\\20260913T211755666611Z\\trials\\U06\\sample"]
```

Cwd: `C:\Projects\DevForgeAI`. Start 2026-09-13T21:20:23.288863Z; end 2026-09-13T21:20:23.550368Z; elapsed 0.250s; exit 2; timed out False.
[stdout](commands/U06/stdout.txt) · [stderr](commands/U06/stderr.txt) · [receipt](commands/U06/receipt.json)

## U07

```json
["C:\\Program Files\\Python310\\python.exe", "-B", "-X", "utf8", "C:\\Projects\\DevForgeAI\\src\\agents\\skills\\skill-validator\\scripts\\adaptive_observe.py", "package", "--source", "C:\\Projects\\DevForgeAI\\docs\\plan\\skill-validations\\skill-validator\\20260913T211755666611Z\\trials\\U07\\sample"]
```

Cwd: `C:\Projects\DevForgeAI`. Start 2026-09-13T21:20:23.569369Z; end 2026-09-13T21:20:23.824370Z; elapsed 0.250s; exit 2; timed out False.
[stdout](commands/U07/stdout.txt) · [stderr](commands/U07/stderr.txt) · [receipt](commands/U07/receipt.json)
