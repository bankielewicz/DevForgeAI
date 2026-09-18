# Coverage scope

- Host: Windows 10.0.26200, PowerShell, native `C:\Program Files\Python310\python.exe` 3.10.11.
- Working directory: `C:\Projects\DevForgeAI` on the Windows `C:` filesystem.
- Denominator: first-party executable Python under `src/agents/skills/advisor/scripts` and `src/agents/skills/advisor/evals`.
- Exclusions: tests, JSON/JSONL fixtures, schemas, documentation, assets, and generated evidence.
- Measurement: executed lines plus separately reported branches, using Coverage.py 7.9.0.
- Qualification: deterministic authoring evidence only; no live Claude invocation or framework acceptance.
