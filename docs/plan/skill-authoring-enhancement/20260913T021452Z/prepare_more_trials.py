from pathlib import Path
import shutil
import json
RUN = Path(__file__).resolve().parent
root = RUN / 'independent-trials'
case = root / 'material-ambiguity'
case.mkdir()
(case / 'project').mkdir()
shutil.copytree(RUN / 'candidate/skill-builder', case / 'skill-builder')
prompt = f'''Use $skill-builder at {case / 'skill-builder/SKILL.md'}.
Create a skill that rewrites numeric dates in pasted reports into the right date format. Examples of dates we get are 03/04/2026 and 11/12/2026. Project root: {case / 'project'}.
You may write only under this project. No external actions or dependencies. If material input is needed, save the questions you would ask as your response rather than sending messages outside this task. Save the final response to {case / 'response.md'} and the tool trace to {case / 'trace.md'}. Retain any authoring artifacts.
'''
(case / 'prompt.txt').write_text(prompt)
(case / 'plan.json').write_text(json.dumps({'case_ids':['AC-02','AC-03'],'expected':'Focused questions for ambiguous date interpretation/output and missing destination with resolved project recommendation; no arbitrary assumption of month/day order','executor':'independent Codex agent','timeout_seconds':600,'write_root':str(case / 'project')},indent=2))
case = root / 'import-script'
case.mkdir()
(case / 'project').mkdir()
shutil.copytree(RUN / 'candidate/skill-builder', case / 'skill-builder')
source = case / 'source/decimal-ledger'
(source / 'scripts').mkdir(parents=True)
(source / 'SKILL.md').write_text('---\nname: decimal-ledger\ndescription: Sum a supplied CSV amount column using exact decimal arithmetic.\n---\n\n# Decimal ledger\n\nUse scripts/total.py with a local CSV file containing an amount header. Return one JSON object with total as a decimal string. Invalid or missing amounts must stop with a clear nonzero error. Never rewrite the input file.\n')
(source / 'scripts/total.py').write_text('import csv, decimal, json, sys\ntry:\n    with open(sys.argv[1], newline="", encoding="utf-8") as stream:\n        reader = csv.DictReader(stream)\n        if "amount" not in (reader.fieldnames or []):\n            raise ValueError("missing amount column")\n        total = decimal.Decimal("0")\n        for row in reader:\n            value = decimal.Decimal(row["amount"])\n            if not value.is_finite():\n                raise ValueError("amount must be finite")\n            total += value\n    print(json.dumps({"total": str(total)}))\nexcept (ValueError, decimal.InvalidOperation, KeyError) as exc:\n    print("Invalid amount input: " + str(exc), file=sys.stderr)\n    sys.exit(2)\n')
prompt = f'''Use $skill-builder at {case / 'skill-builder/SKILL.md'} to import the local Claude skill package {source} as a Codex development skill. Preserve its exact decimal totals, string output and invalid-input behavior, and its no-input-rewrite boundary. Project root: {case / 'project'}. Save it under {case / 'project/skills under review'}. Do not install dependencies or contact services. Writes are authorized only under this project and to {case / 'response.md'} and {case / 'trace.md'}. Retain the final response, exact tool commands and outcomes at those paths.
'''
(case / 'prompt.txt').write_text(prompt)
(case / 'plan.json').write_text(json.dumps({'case_ids':['AC-09','AC-10','AC-12','AC-13'],'expected':'Preserved import contract and script, dispositions, source hashes, authoring-only delivery and manual handoff; later validator executes positive/negative script cases','executor':'independent Codex agent','timeout_seconds':600,'write_root':str(case / 'project')},indent=2))
print('Prepared ambiguity and script-import cases before execution.')
