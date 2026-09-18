"""Fresh disjoint CLI attempts; dependencies remain sequential."""
from concurrent.futures import ThreadPoolExecutor
from native_review import run
import sys
if len(sys.argv)>1 and sys.argv[1]=='resume':
    import native_resume
    sys.exit(0)
if len(sys.argv)>1 and sys.argv[1]=='extended':
    import native_extended
    sys.exit(0)

tasks=[('handoff','consumer','001'),('changed-producer','producer','001'),('full-validator','validator','001'),('negative-verification','consumer','001'),('required-absent','consumer','001'),('optional-absent','consumer','001'),('implicit','validator','001')]
with ThreadPoolExecutor(max_workers=3) as pool:
    futures=[pool.submit(run,*x) for x in tasks]
    for f in futures:
        f.result()
run('changed-producer','consumer','001')
