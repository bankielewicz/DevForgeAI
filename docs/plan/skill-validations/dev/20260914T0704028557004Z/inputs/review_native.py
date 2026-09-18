"""Audit completed native attempts; emit supporting evidence, not verdicts."""
import continue_evaluation as c
import importlib.util
import json
from pathlib import Path
import sys
sys.path.insert(0,str(c.PRIOR/'bundle'))
spec=importlib.util.spec_from_file_location('original_audit',c.PRIOR/'audit_native.py')
a=importlib.util.module_from_spec(spec);spec.loader.exec_module(a);a.RUN=c.RUN
for name in sys.argv[1:]:
    base=c.RUN/'trials'/name
    result_path=base/'attempt-002/result.json'
    if not result_path.exists():
        print(name,'IN_PROGRESS_OR_NOT_RUN')
        continue
    result=c.load(result_path)
    project=Path(result['cwd'])
    report=a.audit(name)
    print('AUDIT',name,json.dumps(report,ensure_ascii=False))
    dest=c.RUN/'inputs/native-audits'/name
    if not dest.exists(): c.save(dest/'audit.json',report)
    final=project/'.trial-output/final-002.txt'
    print('FINAL',final.read_text(encoding='utf-8') if final.exists() else 'ABSENT')
    print('DURATION',result['elapsed_seconds'])
    events=[json.loads(line) for line in (c.RUN/'commands'/(name+'-002')/'stdout.txt').read_text(encoding='utf-8').splitlines()]
    commands=[]
    for row in events:
        item=row.get('item',{})
        if row.get('type') in ('error','turn.failed'): print('ERROR',row)
        if item.get('type')=='command_execution' and row['type']=='item.completed':
            commands.append({'command':item.get('command'),'exit_code':item.get('exit_code'),'output':item.get('aggregated_output')})
    if not (dest/'commands.json').exists(): c.save(dest/'commands.json',commands)
    print('COMMAND_EXITS',[x['exit_code'] for x in commands])

