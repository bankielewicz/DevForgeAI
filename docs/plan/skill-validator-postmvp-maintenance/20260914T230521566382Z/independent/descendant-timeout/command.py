import os, subprocess, sys, time
from pathlib import Path
child = subprocess.Popen([sys.executable, '-B', '-c', 'import time; time.sleep(60)'])
Path('child.pid').write_text(str(child.pid))
print('retained-before-timeout', flush=True)
time.sleep(60)
