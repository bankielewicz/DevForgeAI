"""Compare retained full-source measurements; no test execution or acceptance."""
import json
from pathlib import Path

root = Path(__file__).resolve().parent
workspace = Path(r'C:\Projects\DevForgeAI')
source = workspace/'devforgeai/experiments/codex-worker-probe/src'
old = workspace/'docs/plan/framework-worker-native-completion-qa/20260915T2325371896643Z/08a-coverage/coverage.json'
new = root.parent/'20260916T003840Z-dev/full-coverage/coverage.json'
def rows(path):
    result = {}
    for group in json.loads(path.read_text())['data']:
        for item in group['files']:
            target = Path(item['filename']).resolve()
            if target.is_relative_to(source):
                name = target.relative_to(source).as_posix()
                assert name not in result
                result[name] = item['summary']['lines']
    return result
before,after = rows(old),rows(new)
assert before.keys()==after.keys()
comparison = [{'source':name,'old_covered':before[name]['covered'],'new_covered':after[name]['covered'],
    'old_denominator':before[name]['count'],'new_denominator':after[name]['count'],
    'newly_covered_lines':after[name]['covered']-before[name]['covered']} for name in sorted(after)]
result = {'old':str(old),'new_developer':str(new),'rows':comparison,
    'old_covered':sum(row['old_covered'] for row in comparison),'new_developer_covered':sum(row['new_covered'] for row in comparison),
    'old_denominator':sum(row['old_denominator'] for row in comparison),'new_denominator':sum(row['new_denominator'] for row in comparison)}
with (root/'coverage-comparison.json').open('x',encoding='utf-8') as stream:
    json.dump(result,stream,indent=2)
print(json.dumps(result))
