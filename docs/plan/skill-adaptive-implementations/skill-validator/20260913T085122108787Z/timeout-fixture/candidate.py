from pathlib import Path
import time
p=Path(__file__).parent
(p/"partial.txt").write_text("partial output retained")
print("partial stdout before interruption",flush=True)
time.sleep(300)
