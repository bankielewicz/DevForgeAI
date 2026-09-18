"""Additional independent repair probes. Stop immediately on sanitizer disclosure."""
import json,sys
from record import ROOT,sha,capture,write
from independent_run import fixture,bounded

mode=sys.argv[1]
if mode=='boundary':
    results=[]
    for variant in ['deadline','cancel','invalid','interrupt']:
        path=fixture('RT-01-'+variant,'WF-15',ROOT/'independent-target/debug/protocol-peer.exe')
        args=[ROOT/'independent-target/debug/qa-driver.exe','--boundary',path/'request.json',variant]
        receipt=capture('RT-01-'+variant,args,cwd=path,timeout=5)
        output=json.loads((ROOT/('RT-01-'+variant)/'stdout.txt').read_text()) if receipt['exit_code']==0 else None
        results.append({'variant':variant,'receipt':str(ROOT/('RT-01-'+variant)/'receipt.json'),'observation':output,'pass':receipt['exit_code']==0 and output is not None})
        write('independent-boundary.json',results)
        if receipt['exit_code']!=0:
            raise SystemExit('independent boundary failed; inspect before continuation')
elif mode=='errors':
    expected={91:{'httpConnectionFailed':{'httpStatusCode':65535}},92:{'responseStreamDisconnected':{'httpStatusCode':0}},
      93:{'responseTooManyFailedAttempts':{'httpStatusCode':None}},94:{'responseStreamConnectionFailed':{}},
      95:{'activeTurnNotSteerable':{'turnKind':'compact'}},96:'usageLimitExceeded',97:None,98:None,99:None}
    results=[]
    cases=[('WF-07-'+str(k),v,'provider_failed' if v is not None else 'protocol_error') for k,v in expected.items()]
    cases += [('WF-04-94',None,'rpc_error'),('WF-04-95',None,'protocol_error'),('WF-04-96',None,'protocol_error')]
    for case,category,reason in cases:
        label='RT-02-'+case
        rec=bounded(label,case,4)
        path=ROOT/'independent-attempts'/label
        ev=[json.loads(x) for x in (path/'run/journal.jsonl').read_text().splitlines()]
        actual=[e['data']['error_category'] for e in ev if 'error_category' in e['data']]
        code=[e['data']['error_code'] for e in ev if 'error_code' in e['data']]
        wanted=[] if category is None else [category]
        good=rec['pass'] and actual==wanted and rec['terminal'] is not None and rec['terminal']['reason']==reason
        if case=='WF-04-94':good=good and code==[-32010]
        result={'case':case,'expected_category':wanted,'actual_category':actual,'expected_reason':reason,'actual_reason':rec['terminal']['reason'] if rec['terminal'] else None,'rpc_codes':code,'pass':good,'evidence':str(path/'result.json')}
        results.append(result);write('independent-errors.json',results)
        if rec.get('private_marker_files'):
            raise SystemExit('CRITICAL_PRODUCT_DEFECT: private marker retained; stop all testing')
        if not good:
            raise SystemExit('independent error case failed; assess before further execution')
else:
    raise SystemExit('unknown probe selection')
