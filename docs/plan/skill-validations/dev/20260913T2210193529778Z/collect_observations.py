"""Read retained completed native attempts into a review dossier. No verdict guessing."""
import json
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parent

def collect():
    report=[]
    for folder in sorted((ROOT/'commands').iterdir()):
        command=json.loads((folder/'command.json').read_bytes())
        if command['termination']=='not-started':
            report.append({'attempt':folder.name,'state':'RUNNING_OR_UNKNOWN'}); continue
        events=[]
        for line in (folder/'stdout.txt').read_text(encoding='utf-8').splitlines():
            try: events.append(json.loads(line))
            except ValueError: events.append({'invalid_jsonl':True})
        messages=[r['item']['text'] for r in events if r.get('item',{}).get('type')=='agent_message']
        commands=[r['item'] for r in events if r.get('type')=='item.completed' and r.get('item',{}).get('type')=='command_execution']
        project=Path(command['cwd']); base=project.parent
        record={'attempt':folder.name,'state':command['termination'],'exit_code':command.get('exit_status'),'elapsed':command.get('elapsed_seconds'),'model_messages':messages,'executed_commands':[{'command':c['command'],'exit_code':c.get('exit_code'),'output_tail':c.get('aggregated_output','')[-1200:]} for c in commands],'final_present':list(str(p) for p in (project/'.trial-output').glob('final-*.txt')),'files':[],'evidence_text':{}}
        for path in sorted(project.rglob('*')):
            if not path.is_file() or 'trial-skill' in path.parts or '.trial-output' in path.parts: continue
            relative=path.relative_to(project).as_posix()
            record['files'].append(relative)
            if path.suffix in ('.md','.jsonl','.json') and path.stat().st_size<60000 and path.name not in ('AGENTS.md','spec.md','consumer.md','conflict.md','spec [input] Ω.md'):
                record['evidence_text'][relative]=path.read_text(encoding='utf-8',errors='replace')
        report.append(record)
    return report

if __name__=='__main__':
    rows=collect()
    if len(sys.argv)>1:
        path=Path(sys.argv[1])
        with path.open('x',encoding='utf-8') as out: json.dump(rows,out,ensure_ascii=False,indent=2)
    else:
        print(json.dumps([{'attempt':r['attempt'],'state':r['state'],'elapsed':r.get('elapsed'),'final':r.get('model_messages',[])[-1:],'files':r.get('files',[])} for r in rows],ensure_ascii=False,indent=2))
