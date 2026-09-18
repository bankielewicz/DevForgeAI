import hashlib, json, pathlib, subprocess, sys

script, inputs, output, phase = map(pathlib.Path, sys.argv[1:5])
inputs.mkdir(parents=True, exist_ok=False)
cases = [
    ('decimal', 'item,quantity,unit_price\nCoffee,1,0.1\nTea,1,0.2\n', {'total':'0.30','line_count':2}),
    ('round-once', 'item,quantity,unit_price\nA,1,0.005\nB,1,0.005\n', {'total':'0.01','line_count':2}),
    ('half-up', 'item,quantity,unit_price\nA,1,1.005\n', {'total':'1.01','line_count':1}),
    ('fractional', 'item,quantity,unit_price\nA,1.25,2.40\n', {'total':'3.00','line_count':1}),
    ('empty', 'item,quantity,unit_price\n', {'total':'0.00','line_count':0}),
    ('quoted', 'item,quantity,unit_price\n"A, B",2,3.50\n', {'total':'7.00','line_count':1}),
    ('wide-decimal', 'item,quantity,unit_price\nA,1,123456789012345678901234567890.005\n', {'total':'123456789012345678901234567890.01','line_count':1}),
    ('header', 'item,price,quantity\nA,1,2\n', None),
    ('extra-cell', 'item,quantity,unit_price\nA,1,2,3\n', None),
    ('missing-cell', 'item,quantity,unit_price\nA,1\n', None),
    ('empty-item', 'item,quantity,unit_price\n ,1,2\n', None),
    ('negative', 'item,quantity,unit_price\nA,-1,2\n', None),
    ('nan', 'item,quantity,unit_price\nA,NaN,2\n', None),
    ('infinity', 'item,quantity,unit_price\nA,1,Infinity\n', None),
    ('malformed', 'item,quantity,unit_price\nA,1,two\n', None),
]
if str(phase).startswith('later'):
    cases.append(('total-quantity','item,quantity,unit_price\nA,1.25,2\nB,2.50,1\n',{'total':'5.00','line_count':2,'total_quantity':'3.75'}))
results=[]
for name, text, expected in cases:
    path=inputs/(name+'.csv'); path.write_text(text, encoding='utf-8', newline='\n')
    before=hashlib.sha256(path.read_bytes()).hexdigest()
    args=[sys.executable,'-B','-X','utf8',str(script),str(path)]
    run=subprocess.run(args,capture_output=True,text=True,encoding='utf-8')
    if expected is None:
        passed=run.returncode==2 and not run.stdout and bool(run.stderr.strip())
    else:
        if str(phase).startswith('later') and 'total_quantity' not in expected:
            quantities={'decimal':'2','round-once':'2','half-up':'1','fractional':'1.25','empty':'0','quoted':'2','wide-decimal':'1'}
            expected={**expected,'total_quantity':quantities[name]}
        passed=run.returncode==0 and json.loads(run.stdout)==expected and not run.stderr
    after=hashlib.sha256(path.read_bytes()).hexdigest()
    passed=passed and before==after
    results.append({'case':name,'argv':args,'expected':expected,'exit_code':run.returncode,'stdout':run.stdout,'stderr':run.stderr,'input_before_sha256':before,'input_after_sha256':after,'passed':passed})
output.parent.mkdir(parents=True, exist_ok=True)
output.write_text(json.dumps({'phase':str(phase),'cases':results,'passed':all(r['passed'] for r in results)},indent=2)+'\n',encoding='utf-8')
print(json.dumps({'cases':len(results),'passed':all(r['passed'] for r in results)}))
sys.exit(0 if all(r['passed'] for r in results) else 1)
