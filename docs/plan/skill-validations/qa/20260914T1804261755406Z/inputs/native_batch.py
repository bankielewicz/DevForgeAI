"""Run independent synthetic cases, maximum three native tasks concurrently."""
from concurrent.futures import ThreadPoolExecutor, as_completed
import subprocess
import sys
from bootstrap import RUN, ROOT

def run(item):
    name,attempt=item
    command=[sys.executable,'-B','-X','utf8',str(RUN/'inputs/native_trial.py'),name,attempt]
    p=subprocess.run(command,cwd=ROOT,capture_output=True,timeout=640)
    (RUN/'trials'/name/f'launcher-{attempt}.stdout').write_bytes(p.stdout)
    (RUN/'trials'/name/f'launcher-{attempt}.stderr').write_bytes(p.stderr)
    return name,p.returncode,p.stdout.decode('utf-8',errors='replace')[-250:]

if __name__=='__main__':
    tasks=[('QV-01','003'),('dependent-plan','001'),('integrity','001'),('dynamic-platform','001'),('drift','001'),('decisions','001')]
    with ThreadPoolExecutor(max_workers=3) as pool:
        for future in as_completed([pool.submit(run,item) for item in tasks]):
            print(future.result(),flush=True)
