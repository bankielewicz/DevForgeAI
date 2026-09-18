from pathlib import Path
Path("unexpected.txt").write_text("side effect")
