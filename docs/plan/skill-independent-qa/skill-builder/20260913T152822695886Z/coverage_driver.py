"""Preserve direct-script import semantics while measuring inspected SUT code."""
import runpy
from pathlib import Path
import sys

target=Path(sys.argv[1]).resolve()
sys.argv=sys.argv[1:]
sys.path.insert(0,str(target.parent))
runpy.run_path(str(target),run_name='__main__')
