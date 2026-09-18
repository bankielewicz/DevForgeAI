"""Preserve direct Python script import semantics under coverage tracing."""
from pathlib import Path
import runpy
import sys
script=Path(sys.argv[1]).resolve()
sys.argv=sys.argv[1:]
sys.path.insert(0,str(script.parent))
runpy.run_path(str(script),run_name='__main__')
