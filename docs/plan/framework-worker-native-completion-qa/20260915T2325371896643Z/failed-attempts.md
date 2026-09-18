# Preserved harness attempts

## 08-coverage

The first coverage recorder invocation supplied `cargo` as a relative executable. `record.py` created `08-coverage/` and its `candidate-before.json`, then failed while resolving `C:\Projects\DevForgeAI\docs\plan\framework-worker-native-completion-qa\20260915T2325371896643Z\cargo` with `FileNotFoundError`. No Cargo or product child was launched, and therefore no command receipt or raw child streams exist for this setup failure.

The immediately corrected invocation could not reuse the same label because the recorder deliberately rejects existing attempt directories (`FileExistsError`). It also launched no child. The complete collector was then launched once with the absolute Cargo path under fresh label `08a-coverage`; its receipt, raw streams, JSON, fixtures and profraw files are retained. This is a harness correction before collector execution, not a retry of a coverage result.

