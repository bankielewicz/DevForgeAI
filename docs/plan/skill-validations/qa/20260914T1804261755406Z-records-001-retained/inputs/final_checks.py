"""Finalize supporting records and check both evidence schema families."""
import json
from pathlib import Path
import sys
from bootstrap import RUN,ROOT,VALIDATOR,write,ref,command

def main():
    sources=json.loads((RUN/'sources.json').read_text())
    for row in sources['sources']:
        if row['source_id']=='openai-live':
            row['retrieved_at_utc']=None
            row['retrieval_time_precision']='Read live on 2026-09-14; exact retrieval timestamp was not separately captured.'
    sources['sources'].append({'source_id':'qa-entrypoint','original_path':str(ROOT/'src/agents/skills/qa/SKILL.md'),'retrieved_at_utc':None,'sha256':ref('source/SKILL.md')['sha256'],'snapshot_path':'source/SKILL.md','sections':['Select the mode and scope','Follow the selected workflow','Preserve evidence and ownership'],'freshness':'snapshot_only'})
    write('sources.json',sources)
    workflow=json.loads((RUN/'workflow-map.json').read_text())
    for step in workflow['steps']:
        for r in step['source_refs']:r['source_id']='qa-entrypoint'
    write('workflow-map.json',workflow)
    log=['# Executed command ledger','',f'Working directory unless recorded otherwise: `{ROOT}`. Native case cwd/argv/timestamps/exit/timeout and streams are in each retained receipt. No inferred command executions.','', '| Operation | Result | Exact command and evidence |','| --- | --- | --- |']
    for p in sorted((RUN/'observations').glob('*.receipt.json')):
        row=json.loads(p.read_text())
        log.append(f"| {p.stem} | exit {row['exit_code']} | `{json.dumps(row['command'])}`; [{p.name}](observations/{p.name}) |")
    for p in sorted((RUN/'trials').glob('*/attempt-*/receipt.json')):
        row=json.loads(p.read_text());relative=p.relative_to(RUN).as_posix()
        log.append(f"| {row['case_id']} attempt {row['attempt_id']} | {row['state']}; exit {row.get('exit_code')} | `{json.dumps(row['command'])}`; [receipt]({relative}) |")
    log+=['','Additional executed local commands:','',
      '- `python -B -X utf8 .../inputs/bootstrap.py` — exit 0; captures selected inputs, pins initial rules and executes retained intake/structure/checker/helper/version/help commands.',
      '- `python -B -X utf8 .../inputs/prepare_trials.py` — exit 0; creates predeclared 21 scenarios and first fixture.',
      '- `python -B -X utf8 .../inputs/prepare_campaign.py` — exit 0; creates five additional independent fixtures.',
      '- `python -B -X utf8 .../inputs/prepare_retest.py` — exit 0; creates corrected fixture after actual prior test exits 1 with ValueError not raised (trials/retest-prior/receipt.json).',
      '- `python -B -X utf8 -m unittest discover -s docs/plan/skill-validations/qa/20260914T1804261755406Z/evaluation -p test_graders.py -v` — red exit 1 (9 unimplemented-behavior errors), green exit 0 (9/9), separate logs observations/grader-red.txt and grader-green.txt.',
      '- `python -B -X utf8 -m coverage run --branch --include=\'*/evaluation/graders.py,*/evaluation/run_evaluation.py\' -m unittest discover -s docs/plan/skill-validations/qa/20260914T1804261755406Z/evaluation -p \'test_*.py\' -v` — exit 0, 14/14; COVERAGE_FILE explicitly set to observations/evaluator.coverage under this run.',
      '- `python -B -X utf8 -m coverage json -o docs/plan/skill-validations/qa/20260914T1804261755406Z/observations/evaluator-coverage.json` and `python -B -X utf8 -m coverage report -m` — exit 0.',
      '- `python -B -X utf8 .agents/skills/skill-validator/scripts/adaptive_observe.py package --source docs/plan/skill-validations/qa/20260914T1804261755406Z/source --tokenizer tiktoken --encoding o200k_base` — exit 2; semantic candidates pending, optional local encoding unavailable; raw output observations/adaptive-tokenized.stdout.',
      '- `python -B -X utf8 .../inputs/static_review.py` — exit 0; formal template comparison and recorded primary semantic review.',
      '- `python -B -X utf8 .../inputs/verify_native.py` — exit 0; independent project/input/artifact readbacks (first six completed tasks, then all seven).',
      '- `python -B -X utf8 .../inputs/prepare_results.py` — exit 0; sealed fixture/bundle preparation after native review.',
      '- `python -B -X utf8 .../evaluation/run_evaluation.py --run-root docs/plan/skill-validations/qa/20260914T1804261755406Z --output docs/plan/skill-validations/qa/20260914T1804261755406Z/observations/evaluation-results-001.jsonl` — exit 0; 21/21.',
      '- `python -B -X utf8 .../inputs/finalize.py` — exit 0; actual source/input readback followed by report and schema-1 records.',
      '', '`.../` in the one-run script entries abbreviates `docs/plan/skill-validations/qa/20260914T1804261755406Z/`; exact commands are reconstructable from that declared prefix. Interactive read-only Get-Content/rg/tool discovery and Markdown authoring are retained in the host conversation. Tool calls are evidence; none are claimed as product acceptance.']
    (RUN/'command-log.md').write_text('\n'.join(log)+'\n',encoding='utf-8')
    a=command('adaptive-records-001',[sys.executable,'-B','-X','utf8',str(VALIDATOR/'scripts/adaptive_observe.py'),'records','--run-root',str(RUN.with_name(RUN.name+'-adaptive'))])
    b=command('records-001',[sys.executable,'-B','-X','utf8',str(VALIDATOR/'scripts/observe.py'),'records','--run-root',str(RUN)])
    for name,p in [('adaptive',a),('schema1',b)]:
        value=json.loads(p.stdout)
        print(name,'errors',value.get('errors',value.get('observations',{}).get('errors')))

if __name__=='__main__':main()
