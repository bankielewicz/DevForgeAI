"""Execute retained read-only utility observations over frozen input bytes."""
from prepare import *

def main():
    source=str(RUN/'source')
    for name,argv in [
        ('structure',[str(VAL/'scripts/observe.py'),'structure','--source',source]),
        ('creator',[str(Path('C:/Users/bryan/.codex/skills/.system/skill-creator/scripts/quick_validate.py')),source]),
        ('adaptive-package',[str(VAL/'scripts/adaptive_observe.py'),'package','--source',source]),
        ('organization',[str(VAL/'scripts/standards_observe.py'),'--source',source])]:
        command(name,[sys.executable,'-B','-X','utf8',*argv])

if __name__=='__main__':
    main()
