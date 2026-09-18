from prepare import *
denied=RUN/'trials/N11c/project/docs/plan/discovery/denied'
save(RUN/'trials/N11c/acl-setup-attempt-002.json',dict(argv=['icacls',str(denied),'/deny','*S-1-1-0:(WD,AD)'],executor='Host-approved exec_command',exit_code=0,stdout='Successfully processed 1 files; Failed processing 0 files',reason='Sandbox attempt 001 denied ACL mutation; exact host attempt 002 succeeded.'))
try:
    with (denied/'probe.tmp').open('xb'):
        pass
except PermissionError as error:
    save(RUN/'trials/N11c/denial-preflight.json',dict(result='OBSERVED',error=str(error),path=str(denied/'probe.tmp')))
else:
    raise RuntimeError('Write denial not observed; cannot qualify fixture')
path=RUN/'trials/N11c/plan.json'
save(RUN/'trials/N11c/plan-before-boundary.json',path.read_bytes())
plan=json.loads(path.read_bytes())
plan['inputs'].append(dict(path=str(denied/'sentinel.txt'),sha256=observe.sha256((denied/'sentinel.txt').read_bytes())))
path.write_text(json.dumps(plan,indent=2)+'\n',encoding='utf-8')
save(RUN/'inputs/edge-trial-list.json',['N17a','N17b','N17c','N17d','N17e','N11b','N11c'])
print('Write denial observed; edge plans ready.')
