"""Read live trial receipts without interpreting reasoning as evidence."""
import datetime
import json
from pathlib import Path
RUN=Path(__file__).resolve().parent
rows=[]
for case in sorted((RUN/'trials').iterdir()):
    attempts=list(case.glob('attempt-*'))
    if not attempts:continue
    for attempt in attempts:
        if (attempt/'result.json').exists():
            result=json.loads((attempt/'result.json').read_bytes())
            rows.append({key:result[key] for key in ['case_id','outcome','elapsed_seconds','cleanup']})
            continue
        started=json.loads((attempt/'started.json').read_bytes()) if (attempt/'started.json').exists() else None
        events=[]
        if (attempt/'stdout.txt').exists():
            for line in (attempt/'stdout.txt').read_text(encoding='utf-8').splitlines():
                try:events.append(json.loads(line))
                except ValueError:pass
        messages=[v['item']['text'] for v in events if v.get('item',{}).get('type')=='agent_message']
        elapsed=(datetime.datetime.now(datetime.timezone.utc)-datetime.datetime.fromisoformat(started['started_at'])).total_seconds() if started else None
        rows.append({'case_id':case.name,'outcome':'RUNNING' if started else 'SEALED','elapsed_seconds':elapsed,'events':len(events),'story_files':[p.name for p in (case/'project/backlog').glob('*.story.md')],'last_message':messages[-1][:450] if messages else None})
print(json.dumps(rows,indent=2,ensure_ascii=True))
