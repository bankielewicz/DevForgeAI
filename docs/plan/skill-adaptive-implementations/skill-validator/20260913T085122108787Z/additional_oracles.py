"""Additional bounded lineage, token and interruption maintenance evidence."""
import copy
import hashlib
import json
from pathlib import Path
import sys
from capture import ROOT, RUN, scan
from terminal_harness import command, save
sys.path.insert(0,str(ROOT/'src/agents/skills/skill-validator/tests'))
import adaptive_fixtures as fixture

def lineage():
    root = RUN/'lineage-fixtures'
    root.mkdir()
    request = fixture.shared(root/'inputs')
    selection = json.loads(Path(request['selection']['path']).read_bytes())
    proposal = json.loads(Path(selection['proposal']['path']).read_bytes())
    parent = fixture.package(root/'inputs','parent-core')
    parent_root = Path(parent['root'])
    (parent_root/'references').mkdir()
    statements = {'R1':'Preserve selected input bytes.','R2':'Write only the selected local output.','R3':'Report missing input without product effects.'}
    (parent_root/'references/adaptive-contract.md').write_text('| ID | Requirement |\n| --- | --- |\n'+''.join('| '+key+' | '+value+' |\n' for key,value in statements.items()))
    manifest = scan(parent_root)
    fixture.write(Path(parent['manifest']['path']),manifest['files'])
    parent['manifest'] = fixture.reference(Path(parent['manifest']['path']))
    parent['package_digest'] = manifest['package_digest']
    proposal['requirements'] += [{'id':key,'origin':'derived','statement':value,'source_refs':[],'rationale':'Preserve selected parent contract.','verification':'Compare output and effects.'} for key,value in statements.items()]
    variant = {'id':'V','name':'variant-skill','role':'project_variant','action':'create','target_root':str(root/'inputs/variant-skill'),'existing_package':None,'parent_core':parent,'responsibility':'Selected variant preserves parent requirements.','exclusions':['Network'],'triggers':['Selected local task'],'near_misses':['Installation'],'requirement_ids':list(statements),'fact_ids':[],'rationale':'Selected variant fixture.','depends_on':[],'capabilities':[],'lineage_delta':[{'requirement_id':key,'disposition':'retained','reason':'Equivalent child statement.','replacement_requirement_ids':[]} for key in statements]}
    proposal['members'].append(variant)
    proposal['state'] = 'PROPOSED'
    missing = copy.deepcopy(proposal)
    missing['members'][-1]['lineage_delta'].pop()
    cases = [('complete',proposal,0),('omitted-parent',missing,1)]
    save(root/'expectations.json',[{'case_id':name,'expected_exit':expected,'parent_digest':parent['package_digest'],'expected_parent_unchanged':True} for name,value,expected in cases])
    results = []
    for name,value,expected in cases:
        path = root/(name+'.json')
        fixture.write(path,value)
        builder = command(root/'results'/name/'builder',[sys.executable,'-B','-X','utf8',str(ROOT/'src/agents/skills/skill-builder/scripts/adaptive.py'),'inspect','--record',str(path)])
        # Independent local reader command driven by raw record, not expected label.
        script = root/'reader.py'
        if not script.exists():
            script.write_text('import sys,json\nfrom pathlib import Path\nsys.path.insert(0,sys.argv[1])\nimport adaptive_contracts as c\nimport observe\ntry:\n r=c.Reader(); r.record(observe.strict_json(Path(sys.argv[2]).read_bytes()),sys.argv[2]); r.readback(); print("VALID")\nexcept Exception as e:\n print(type(e).__name__+": "+str(e)); sys.exit(1)\n')
        validator = command(root/'results'/name/'validator',[sys.executable,'-B','-X','utf8',str(script),str(ROOT/'src/agents/skills/skill-validator/scripts'),str(path)])
        results.append({'case_id':name,'builder_exit':builder.returncode,'validator_exit':validator.returncode,'expected_exit':expected,'parent_unchanged':scan(parent_root)['package_digest']==parent['package_digest']})
    save(root/'results.json',results)
    print(json.dumps(results))

def tokens():
    root = RUN/'token-fixtures'
    root.mkdir()
    package = fixture.package(root,'token-sample')
    (Path(package['root'])/'empty.txt').write_bytes(b'')
    (Path(package['root'])/'hello.txt').write_bytes(b'hello')
    save(root/'expectations.json',{'encoding':'cl100k_base','empty_tokens':0,'hello_tokens':1,'unavailable':'null counts with NOT_RUN limitation; no download','non_token_counts':'raw bytes, code points, splitlines'})
    result = command(root/'results',[sys.executable,'-B','-X','utf8',str(ROOT/'src/agents/skills/skill-validator/scripts/adaptive_observe.py'),'package','--source',package['root'],'--tokenizer','tiktoken','--encoding','cl100k_base'])
    data = json.loads(result.stdout)
    context = data['observations']['context']
    counts = {row['path']:row['tokens'] for row in context['files']}
    save(root/'comparison.json',{'identity':context['tokenizer'],'counts':counts,'expected_met':counts.get('empty.txt')==0 and counts.get('hello.txt')==1 if context['tokenizer'] else None,'status':'EXECUTED' if context['tokenizer'] else 'NOT_RUN'})
    print(json.dumps(context['tokenizer']))

def timeout_setup():
    root = RUN/'timeout-fixture'
    root.mkdir()
    (root/'candidate.py').write_text('from pathlib import Path\nimport time\np=Path(__file__).parent\n(p/"partial.txt").write_text("partial output retained")\nprint("partial stdout before interruption",flush=True)\ntime.sleep(300)\n')
    save(root/'expectations.json',{'timeout_seconds':120,'expected':'timeout; retain partial.txt/stdout; new linked run after changed source; no reused PASS','before':scan(root)})
    print(str(root/'candidate.py'))

if __name__=='__main__':
    {'lineage':lineage,'tokens':tokens,'timeout-setup':timeout_setup}[sys.argv[1]]()
