from pathlib import Path
Path("report.json").write_text("{}")
Path("unexpected.txt").write_text("side effect")
