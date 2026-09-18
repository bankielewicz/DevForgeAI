"""Fresh supplemental fixtures after coverage instrumentation import failure.
Coverage's launcher omitted the SUT script directory from imports on this host.
The retained driver restores direct-script semantics; it changes no SUT bytes.
"""
import json
from pathlib import Path
import test_extended as e
t=e.t
e.OUT=t.RUN/'fixtures/extended-04'
t.RESULTS=[]

def check(case,argv,*args,**kwargs):
    if len(argv)>4 and Path(str(argv[4])).is_relative_to(t.BUILDER):
        argv=argv[:4]+['-m','coverage','run','--append','--branch','--data-file='+str(t.RUN/'coverage-data-02'),'--source='+str(t.BUILDER),t.RUN/'coverage_driver.py']+argv[4:]
    return e.original('ext2-'+case,argv,*args,**kwargs)

e.check=check;t.check=check
e.OUT.mkdir(parents=True,exist_ok=False)
e.linked();e.legacy();e.updates();e.metadata()
t.put(t.RUN/'extended-followup-results.json',t.RESULTS)
print(json.dumps({'count':len(t.RESULTS),'failures':[r['case'] for r in t.RESULTS if r['status']=='FAIL']}))
