import time
from pathlib import Path
print('started',flush=True)
time.sleep(121)
Path('done.txt').write_text('completed after 120 seconds')
