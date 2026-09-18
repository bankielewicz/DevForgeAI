"""Record manual conclusions after full captured-package inspection."""
import continue_evaluation as c
import copy
import sys
r=c.RUN
def ref(p,absolute=False):
    return {'path':str(p) if absolute else p.relative_to(r).as_posix(),'sha256':c.h.sha(p.read_bytes())}
raw=c.load(r/'commands/package/stdout.txt')
obs=copy.deepcopy(raw['observations'])
for node in obs['resources']:
    path=node['path']
    node.update(role='runtime' if path=='SKILL.md' else 'template' if path.startswith('assets/') else 'reference',
                usage='used',evidence=[ref(r/'source'/path,True)],
                reason='Manually read current captured bytes. Reachable entrypoint/reference/template consumer supplies the logical role; no orphan resource.')
for edge in list(obs['edges']):
    if edge['resolution']=='resolved':
        if '../assets/' in edge['target']:
            obs['edges'].append(dict(edge,kind='template_use'))
        elif edge['source']=='SKILL.md':
            obs['edges'].append(dict(edge,kind='instruction'))
supplement=dict(schema_version='adaptive-observations-v1',run_id=r.name,
                target_digest=c.load(r/'source-manifest.json')['package_digest'],**obs,bindings=[],
                limitations=['Ordinary instruction/template skill; adaptive bindings inapplicable.',
                 'Raw helper retained unchanged. Original directory identity resolved through bound intake; source/ is a snapshot name.',
                 'TODO is mentioned as a prohibited vague gap, not an unfinished instruction. Template fields are intentional runtime slots.',
                 'All eleven resources read manually; link graph corroborates actual template consumers. No universal orphan or keyword criterion.',
                 'Tokenizer cache unavailable; exact bytes/characters/lines measured. No guessed tokens or actual load-cost claim.',
                 'Explicit-path native trials are separate from implicit activation; no security or framework certification.'])
supp=r.with_name(r.name+'-adaptive')
c.save(supp/'observations.json',supplement)
c.h.execute('adaptive-records',[sys.executable,'-B','-X','utf8',str(c.LOADED/'scripts/adaptive_observe.py'),'records','--run-root',str(supp)])
c.copy_file(supp/'observations.json',r/'inputs/adaptive-observations.json')
prior=c.load(r/'inputs/prior-records/semantic-review-final.json')
rows=[]
for original in prior['observations']:
    row=copy.deepcopy(original)
    subject=row.get('subject_path','SKILL.md')
    if not (r/'source'/subject).is_file(): subject='SKILL.md'
    row['evidence']=[ref(r/'source'/subject),ref(r/'inputs/prior-records/semantic-review-final.json'),
                     ref(r/'inputs/adaptive-observations.json')]
    row['review_basis']='Current independent full-package reading corroborates the retained source-level conclusion; native behavior graded separately.'
    if row['rule_id']=='AV-E01':
        row.update(result='NOT_RUN',reason='Current input/package/carry-forward bindings verified; final full-run records and external bundle verification pending.',
                   evidence=[ref(r/'inputs/current-input-readback.json'),ref(r/'inputs/carry-forward.json')])
    if row['rule_id'] in ('AV-F01','AV-F02','AV-F05','AV-R01','AV-R02','AV-U01','AV-C01'):
        row['evidence'].extend([ref(r/'commands/structure/stdout.txt'),ref(r/'commands/package/stdout.txt'),
                                ref(r/'commands/installed-skill-creator/stdout.txt')])
    rows.append(row)
c.save(r/'inputs/semantic-review.json',{'schema_version':'1','run_id':r.name,'target_name':'dev',
 'package_digest':supplement['target_digest'],'review_kind':'Primary validator source assessment, independent of builder; no separate reviewer or model-independence claim.',
 'observations':rows,
 'contextual_adjudications':[
  {'path':'references/failure-delivery.md','excerpt':'Do not replace a gap with an optimistic assumption, vague TODO, or fake interface.',
   'classification':'useful_instruction','reason':'Requires precise source-qualified gap; TODO is a prohibited example, not a scaffold.'},
  {'path':'references/failure-delivery.md','excerpt':'Passing product tests, valid hashes at a different location',
   'classification':'useful_instruction','reason':'Destination fidelity must use original selection and actual file readback before completion.'},
  {'path':'references/evidence-resume.md','excerpt':'Records are editable development evidence, never protected acceptance or an authority gate.',
   'classification':'useful_instruction','reason':'Preserves actual authority boundary rather than inventing enforcement.'}],
 'review_scope':'All eleven text resources, workflow-map steps, resource consumers, effect boundaries and DEV/REV requirements. No executable runtime helper ships in dev.'})
origin=c.load(c.PRIOR/'origin-record.json')
origin.update(run_id=r.name,manifest=ref(r/'source-manifest.json'),specification=ref(r/'inputs/prior-inputs/05-dev-skill-spec.md'),
              prior_evidence=ref(r/'inputs/prior-inputs/01-authoring-record.json'),source_readback_state='NOT_RUN')
c.save(r/'origin-record.json',origin)
print('SEMANTIC_REVIEW_RETAINED',len(rows))

