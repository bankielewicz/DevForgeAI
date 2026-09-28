"""Aggregate frozen denominators without omitting failures or blocked requirements."""
from pathlib import Path
from collections import Counter
import hashlib,json
from native_eval import E,C,save
cases={}
trials=[]
for p in sorted((E/'runs').glob('*/grade.json')):
 g=json.loads(p.read_text());r=json.loads(p.with_name('result.json').read_text())
 assert all(x['status'] not in ['NOT_RUN','BLOCKED'] for x in g['checks']),p
 assert r['status']=='completed',p
 trials.append({'id':p.parent.name,'case':g['case'],'arm':g['arm'],'repeat':g['repeat'],'status':g['status'],'grade':str(p.relative_to(E))})
 cases.setdefault(g['case'],{}).setdefault(g['arm'],[]).append({'repeat':g['repeat'],'status':g['status']})
assert len(trials)==48
for case,arms in cases.items():
 for arm,runs in list(arms.items()):
  assert len(runs)==3
  passes=sum(x['status']=='PASS' for x in runs)
  arms[arm]={'passes':passes,'total':3,'score':passes/3,'threshold':.8,'status':'PASS' if passes/3>=.8 else 'FAIL','runs':runs}
manual={p.parent.name:json.loads(p.read_text()) for p in sorted((E/'manual').glob('*/grade.json'))}
assert len(manual)==8
verification=[
 {'id':'VER-01','status':'PASS','evidence':'writes-valid-brn 3/3; validator executed successfully in native traces.'},
 {'id':'VER-02','status':'PASS','evidence':'no-unconfirmed-dispositions 3/3; every unconfirmed idea open/null and status draft.'},
 {'id':'VER-03','status':'FAIL','evidence':'records-provenance 0/3: session matches host, model is unknown rather than host-selected gpt-6-astra.'},
 {'id':'VER-04','status':'PASS','evidence':'uses-named-framework 3/3; see isolated supplemental controls and discovery-audit limitation.'},
 {'id':'VER-05','status':'PASS','evidence':'Added framework selected, missing-file variant falls back and discloses the cause; SKILL.md hashes unchanged.'},
 {'id':'VER-06','status':'PASS','evidence':'ignores-unrelated-request 3/3; complete retained traces show no candidate SKILL read.'},
 {'id':'VER-07','status':'PASS','evidence':'asks-for-topic 3/3; asks before writing.'},
 {'id':'VER-08','status':'PASS','evidence':'existing-brn 3/3 with full-file hashes unchanged; additional extension scenario preserves exact original items/history.'},
 {'id':'VER-09','status':'FAIL','evidence':'Expanded imported manual plan includes confirmed convergence, which remains draft because model provenance is unknown. The literal SPEC VER-09 core (save yes/no, three failures, static limits) passes. No expanded manual failure is waived.'},
 {'id':'VER-10','status':'BLOCKED','evidence':'PRD-present branch NOT_RUN: Codex PRD skill is absent. The imported absent-PRD case passes 3/3 but does not satisfy the specification branch.'}
]
summary={'candidate_sha256':json.loads((E/'binding.json').read_text())['candidate_sha256'],
 'runtime':'Codex 0.158.0 app-server on WSL Ubuntu','model':'gpt-6-astra','reasoning_effort':'high',
 'overall':'NOT_QUALIFIED','mandatory_denominator':10,'verification_counts':dict(Counter(x['status'] for x in verification)),
 'mandatory_verification':verification,'matrix_total':48,'matrix_executed':48,'plugin_passes':sum(x['status']=='PASS' for x in trials if x['arm']=='plugin'),'plugin_total':24,
 'baseline_passes':sum(x['status']=='PASS' for x in trials if x['arm']=='baseline'),'baseline_total':24,
 'case_results':cases,'trials':trials,'manual_scenarios':manual,'manual_counts':dict(Counter(x['status'] for x in manual.values())),
 'grading':'Frozen regex/file assertions plus native successful-execution checks, complete trace reads, full-file hashes, host identity comparisons, and primary importing-agent semantic review. Not an independent qualification.',
 'baseline_caveat':'Same full contract is scored for both arms. Positive skill-load assertions necessarily fail without the plugin; baseline topic-question semantics pass in all three runs.',
 'installation':'NOT_PERFORMED; runtime skill discovery through process-scoped extra roots is separate from installed plugin qualification.',
 'source_candidate_modified':False}
summary['isolation_controls']={p.parent.name:json.loads(p.read_text()) for p in sorted((E/'isolation-controls').glob('*/grade.json'))}
summary['discovery_audit']='discovery-audit.json'
save(E/'results.json',summary)
print(json.dumps({k:summary[k] for k in ['overall','matrix_total','plugin_passes','baseline_passes','verification_counts','manual_counts']},indent=2))
