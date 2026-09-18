"""Record the owner's standalone target change without rewriting old evidence."""
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys

base = Path(__file__).resolve().parent
root = base.parents[2]
change = base / 'owner-platform-override-20260914'
change.mkdir()
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
spec = root / 'docs/plan/devforgeai-index-service-mvp-spec.md'
page = root / 'docs/plan/index-service-validation-playbook.html'
shutil.copy2(spec, change/'specification-before.md')
shutil.copy2(page, change/'playbook-before.html')
old_hash = sha(spec)
original = spec.read_text(encoding='utf-8')
old = '**DS-003 — Required platforms.** Qualify Windows 11 x64, Ubuntu 24.04 x64, and Ubuntu 24.04 under WSL2.'
new = '**DS-003 — Required platforms.** Qualify Windows 11 x64, standalone Ubuntu 26.04.1 LTS x64, and Ubuntu 24.04 under WSL2.'
assert original.count(old)==1
updated = original.replace(old, new)
line = next(s for s in updated.splitlines() if s.startswith('**DS-003'))
updated = updated.replace(line, line + '\n\nOwner override, 2026-09-14: standalone Ubuntu 26.04.1 LTS replaces the former standalone Ubuntu 24.04 validation target. The owner-submitted VMware campaign may be evaluated against this target. This changes the standalone release requirement only; coverage, test integrity, acceptance scenarios, and Windows/WSL requirements still apply.')
spec.write_text(updated,encoding='utf-8')

review = (base/'evaluate_evidence.py').read_text(encoding='utf-8')
review = review.replace("'required_Ubuntu_24_04':'NOT_RUN'", "'required_standalone_target':'Ubuntu 26.04.1 LTS x64','target_override':'Repository owner, 2026-09-14; supersedes standalone Ubuntu 24.04 only'")
review = review.replace("The specification's Ubuntu 24.04 target remains NOT_RUN.", "The repository owner explicitly replaced the standalone Ubuntu 24.04 target with Ubuntu 26.04.1 LTS on 2026-09-14. This campaign now matches the required standalone target. Windows and Ubuntu 24.04 WSL2 requirements remain unchanged.")
review = review.replace('Keep Ubuntu 26.04.1 compatibility results separate from required Ubuntu 24.04 qualification.', 'Apply the owner-authorized standalone Ubuntu 26.04.1 target; no separate standalone Ubuntu 24.04 run is required for this revised contract.')
review = review.replace("'formal_independent_QA':'PENDING; this is review of supplied execution artifacts',", "'formal_independent_QA':'PENDING; this is review of supplied execution artifacts',\n    'evaluation_specification_sha256':" + repr(sha(spec)) + ",\n    'original_bundle_specification_sha256':" + repr(old_hash) + ",")
review_path = base/'evaluate_evidence_owner_override.py'
review_path.write_text(review,encoding='utf-8')
result = subprocess.run([sys.executable,'-B','-X','utf8',str(review_path)],capture_output=True,text=True)
(change/'evaluation-command.stdout.txt').write_text(result.stdout,encoding='utf-8')
(change/'evaluation-command.stderr.txt').write_text(result.stderr,encoding='utf-8')
assert result.returncode==0, result.stderr
evaluation=json.loads(result.stdout)
report=Path(evaluation['report'])
link=report.relative_to(root/'docs/plan').as_posix()

history = root/'docs/plan/index-service-implementation/20260914T0727264112301Z'
generator = (history/'build_playbook.py').read_text(encoding='utf-8')
generator = generator.replace('Standalone Ubuntu 24.04 x64 — NOT_RUN','Standalone Ubuntu 26.04.1 LTS x64 — fresh campaign')
generator = generator.replace('The specification targets standalone Ubuntu 24.04. Testing Ubuntu 26.04.1 LTS provides separate compatibility evidence; Ubuntu 24.04 remains NOT_RUN until actually tested. Record the exact release and do not transfer results between versions.', 'Owner override dated 2026-09-14: standalone Ubuntu 26.04.1 LTS is the required Linux target, replacing standalone Ubuntu 24.04. The submitted VMware campaign matches this target. Record the exact release; WSL remains a separate target.')
generator = generator.replace('<strong>Standalone Linux has not been tested.</strong>', '<strong>Standalone Ubuntu 26.04.1 LTS has now been tested.</strong> Its submitted regression suite passed 36/36 raw cases, including one setup-only case that receives no product credit. Executed-line coverage is 2,066/2,786 = 74.1564967695621%, below the 95% floor. Full qualification remains incomplete.')
generator = generator.replace('Read the <a href="index-service-implementation/20260914T0727264112301Z/platform-status.md">platform note</a>.', 'Read the <a href="'+link+'">current standalone evaluation</a>; earlier Windows/WSL evidence remains in the <a href="index-service-implementation/20260914T0727264112301Z/platform-status.md">historical platform note</a>.')
generator = generator.replace("required_standalone_target:'Ubuntu 24.04 x64'", "required_standalone_target:'Ubuntu 26.04.1 LTS x64'")
generator = generator.replace("const KEY='devforgeai-index-playbook-v1';", "const KEY='devforgeai-index-playbook-v1-'+SPEC_HASH;")
(change/'build_playbook.py').write_text(generator,encoding='utf-8')
subprocess.run([sys.executable,'-B','-X','utf8',str(change/'build_playbook.py')],check=True)
checker=(history/'check_playbook.cjs').read_text(encoding='utf-8')
checker += "\nassert.equal(run('exportResult().required_standalone_target'),'Ubuntu 26.04.1 LTS x64');\n"
(change/'check_playbook.cjs').write_text(checker,encoding='utf-8')
checked=subprocess.run(['node',str(change/'check_playbook.cjs')],capture_output=True,text=True)
(change/'playbook-check.stdout.txt').write_text(checked.stdout,encoding='utf-8')
(change/'playbook-check.stderr.txt').write_text(checked.stderr,encoding='utf-8')
assert checked.returncode==0,checked.stderr
note=f'''# Repository-owner standalone platform override

Authorization: user stated, "I'm the repo owner. ubuntu 26.04.1 validation overrides Ubuntu 24.04" on 2026-09-14.

Effective target: standalone Ubuntu 26.04.1 LTS x64 replaces standalone Ubuntu 24.04 x64 in DS-003. Windows 11 x64 and Ubuntu 24.04 WSL2 are unchanged. Numeric quality floors, no-mock-decorator and anti-gaming requirements, and mandatory acceptance scenarios remain in force. This is an owner-authorized requirement revision, not an acceptance waiver.

The received VMware campaign now matches the required standalone release. The revised [evaluation]({report.relative_to(base).as_posix().replace('evaluation-', '../evaluation-', 1)}) still records coverage FAIL: 2066/2786 = 74.1564967695621%. All 36 raw regression cases passed; one trivial setup assertion has no product credit. Full manual specification checks and independent test-integrity QA remain incomplete.

Specification before SHA-256: {old_hash}
Specification after SHA-256: {sha(spec)}
Updated HTML SHA-256: {sha(page)}

Original specification/page snapshots are retained here. Original transfer archive, checksums, raw VM files, old evaluation and all historical implementation receipts remain unchanged. The VM's source candidate still matches all 48 application files; the only contract change is the standalone platform revision. No software was rebuilt or requalified by this documentation change. The already-downloaded playbook remains historical; its JSON/raw evidence can be evaluated with this explicit override. The updated HTML uses a separate storage key and new specification hash, preserving historical browser results without silently relabeling them.

Verification: revised evaluator exit 0; playbook Node syntax/logic/export checks exit 0. Browser visual QA was not performed. The earlier evaluator attempt failed a filename-glob assertion (benchmark build log also matched); the selector was narrowed and the successful evaluation retained separately. This was an evidence-review helper error, not a product test failure.
'''
(change/'owner-override.md').write_text(note,encoding='utf-8')
print(json.dumps({'override':str(change/'owner-override.md'),'evaluation':str(report),'specification_sha256':sha(spec),'playbook_sha256':sha(page)},indent=2))
