"""Check that the evaluator causes a real denial and observes a completed source read."""
import json
from pathlib import Path
import subprocess
import sys
import unittest
from faults import observes_selected_epic

RUN=Path(__file__).resolve().parent
STAGE=sys.argv.pop() if sys.argv[-1] in ('red','green','green-002') else 'manual'
CONTROL=RUN/'harness-controls'/STAGE
CONTROL.mkdir(parents=True,exist_ok=False)

def acl(action,target,state):
    argv=['C:/Program Files/PowerShell/7/pwsh.exe','-NoProfile','-File',str(RUN/'fault_controls.ps1'),'-Action',action,'-Target',str(target),'-StatePath',str(state)]
    result=subprocess.run(argv,capture_output=True,timeout=120)
    with (CONTROL/(action+'-'+target.name+'.json')).open('x',encoding='utf-8') as stream:json.dump({'argv':argv,'exit_code':result.returncode,'stdout':result.stdout.decode('utf-8'),'stderr':result.stderr.decode('utf-8')},stream,indent=2)
    return result

class FaultControls(unittest.TestCase):
    def test_denial_and_restore(self):
        target=CONTROL/'backlog';target.mkdir()
        source=target/'existing.txt';source.write_text('preserve source bytes',encoding='utf-8')
        state=CONTROL/'acl.json'
        outcome=acl('Deny',target,state)
        self.assertEqual(outcome.returncode,0,outcome.stderr.decode('utf-8'))
        try:
            self.assertEqual(source.read_text(encoding='utf-8'),'preserve source bytes')
            with self.assertRaises(PermissionError):(target/'blocked.txt').write_text('must be denied',encoding='utf-8')
        finally:
            restored=acl('Restore',target,state)
            self.assertEqual(restored.returncode,0,restored.stderr.decode('utf-8'))
        (target/'restored.txt').write_text('restored access',encoding='utf-8')
    def test_other_root_rejected(self):
        outcome=acl('Deny',RUN/'evaluation',CONTROL/'outside.json')
        self.assertNotEqual(outcome.returncode,0)
        self.assertFalse((CONTROL/'outside.json').exists())
    def test_complete_source_read(self):
        event={'type':'item.completed','item':{'type':'command_execution','command':'Get-Content input/epic.md','aggregated_output':'Keep Copper owl 73.','exit_code':0}}
        self.assertTrue(observes_selected_epic(event,'Copper owl 73.'))
    def test_started_is_not_read(self):
        self.assertFalse(observes_selected_epic({'type':'item.started','item':{'type':'command_execution','command':'Get-Content input/epic.md','aggregated_output':'Copper owl 73.','exit_code':0}},'Copper owl 73.'))
    def test_prose_is_not_read(self):
        self.assertFalse(observes_selected_epic({'type':'item.completed','item':{'type':'agent_message','text':'I read input/epic.md: Copper owl 73.'}},'Copper owl 73.'))
    def test_failed_read(self):
        self.assertFalse(observes_selected_epic({'type':'item.completed','item':{'type':'command_execution','command':'Get-Content input/epic.md','aggregated_output':'Copper owl 73.','exit_code':1}},'Copper owl 73.'))

if __name__=='__main__':unittest.main(verbosity=2)
