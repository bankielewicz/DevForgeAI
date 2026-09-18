# Executed commands and evidence

All commands ran from C:/Projects/DevForgeAI unless their bound argv/cwd record states a disposable project. Native executable: Codex CLI 0.154.0, inherited gpt-6-astra/max configuration; no model override or new provider. Native sessions use workspace-write, skip-git-repo-check, JSON event output and file-based final responses. Exact prompts, argv, clocks, exit/timeout, effects and cleanup receipts are retained under inputs/evidence/trials.

- `observe.py snapshot`, `authoring_intake.py --request ... --request-sha256 ab83db7725bd07ed97210a7f5d1032922813ac94433210a1651e23f45d5bab27`: COMPLETE / BOUND, exit 0.
- `observe.py structure --source <raw>/source`: exit 0. `quick_validate.py <raw>/source`: exit 0.
- `adaptive_observe.py package --source <raw>/source`: exit 2 for caller identity and contextual-placeholder adjudication; both manually resolved without changing raw output.
- `standards_observe.py --source <raw>/source`: exit 0, advisory measurements only.
- `python -B -X utf8 -m coverage run --branch --source <raw>/source/scripts <raw>/test_binding.py`: first setup exit 1; corrected run 30 tests, exit 0. COVERAGE_FILE identifies helper-coverage-001/002.data; JSON reports retained.
- `evaluation/runner.py --cases evaluation/cases.jsonl --output evaluation/attempt-001`: 14/14, exit 0, exact child argv in results.jsonl.
- `evaluation/test_graders.py`: red exit 1 with 12 assertion failures; green exit 0, 16 controls.
- `wsl --list --verbose`: sandbox access denied; approved read-only discovery observed Ubuntu WSL2. Explicit Ubuntu --cd preflight observed /usr/bin/python3 3.12.3. `timeout 120s python3 -B -X utf8 evaluation/linux_tests.py`: two retained measurement attempts, both 30 tests plus symlink check; corrected collection starts before import.
- `trial_runner.py seal/run/check` and selected orchestration scripts: all attempted native receipts retained, 600 seconds per case. N01 app-server access failure retained; approved retry retained child workspace-write. No automatic timeout retries or limit increases.
- Final `observe.py readback` and all selected original input digests: MATCH. `observe.py records` is run after this packet is complete and its raw output is retained separately.

Exploratory reads/help discovery are not acceptance. Early rg discovery referenced one absent optional validator module; this was a lookup error, not a target defect. Synthetic fixture writes and evaluator code are the only authored changes.
