"""Limited structural and affected-regression observations; not acceptance."""
import sys
from harness import RUN, ROOT, TARGET, LOADED, CHECKER, execute

commands=[
 ('STRUCTURAL',[sys.executable,'-B','-X','utf8',str(CHECKER),str(RUN/'source')]),
 ('AFFECTED-REGRESSION',[sys.executable,'-B','-X','utf8','-m','unittest','discover','-s','src/agents/skills/skill-validator/tests','-p','test_adaptive.py','-v']),
 ('SOURCE-READBACK',[sys.executable,'-B','-X','utf8',str(LOADED/'scripts/observe.py'),'readback','--source',str(TARGET),'--manifest',str(RUN/'source-manifest.json')])]
for cid,args in commands:
    result=execute(cid,args)
    print(cid,result['exit'],flush=True)
