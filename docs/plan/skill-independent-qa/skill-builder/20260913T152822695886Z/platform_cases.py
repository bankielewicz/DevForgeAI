"""Native OS argv/binding cases, including path and strict capture boundaries."""
import json
import os
from pathlib import Path
import platform
import sys
import uuid
import test_independent as t

def main():
    host='windows' if os.name=='nt' else 'linux'
    root=t.RUN/'fixtures'/('platform-'+host);root.mkdir(parents=True,exist_ok=False)
    t.RESULTS=[]
    for label in ('valid','relocated','missing','io-error','symlink','private-key-name','pfx-name','exact-files','over-files','exact-bytes','over-bytes'):
        project=root/label/"space é & ; $ ' (p)";skill=project/'.agents/skills/summary-skill';t.adaptive_package(skill)
        reason='BOUND';code=0
        if label=='private-key-name':t.put(skill/'id_rsa','SYNTHETIC PRIVATE KEY FIXTURE, NOT A REAL KEY\n');reason='UNSAFE_PATH';code=1
        if label=='pfx-name':t.put(skill/'identity.pfx',b'SYNTHETIC-NOT-A-CERTIFICATE');reason='UNSAFE_PATH';code=1
        if label in ('exact-files','over-files'):
            for n in range((2000 if label=='exact-files' else 2001)-len(t.rows(skill))):t.put(skill/'files'/str(n),b'')
            if label=='over-files':reason='CAPTURE_LIMIT';code=2
        if label in ('exact-bytes','over-bytes'):
            count=sum(r['bytes'] for r in t.rows(skill));p=skill/'padding.bin'
            with p.open('wb') as stream:stream.truncate(33554432-count+(label=='over-bytes'))
            if label=='over-bytes':reason='CAPTURE_LIMIT';code=2
        # Construct manifest with a separate, streaming oracle; intentional oversized
        # fixtures are not copied/captured as complete permitted input scopes.
        def manifest_unbounded_fixture():
            import hashlib
            result=[]
            for directory,dirs,files in os.walk(skill,followlinks=False):
                for name in files:
                    path=Path(directory)/name;h=hashlib.sha256()
                    with path.open('rb') as stream:
                        for block in iter(lambda:stream.read(1024*1024),b''):h.update(block)
                    result.append({'path':path.relative_to(skill).as_posix(),'bytes':path.stat().st_size,'sha256':h.hexdigest()})
            return sorted(result,key=lambda r:r['path'])
        manifest=manifest_unbounded_fixture()
        record={'schema_version':'project-binding-v1','project_id':str(uuid.uuid4()),'project_root':str(project),'revision':1,'bindings':[{'name':skill.name,'package_path':'.agents/skills/'+skill.name,'package_digest':t.digest(manifest),'role':'expertise','selected':True}],'updated_at_utc':'2026-09-13T00:00:00Z'}
        binding=project/'.agents/devforgeai/project-binding.json'
        if label=='relocated':record['project_root']=str(project.parent);reason='ROOT_MISMATCH';code=1
        if label=='missing':reason='MISSING_BINDING';code=1
        else:t.put(binding,record)
        if label=='io-error':
            if os.name=='nt':
                t.RESULTS.append({'case':host+'-'+label,'status':'NOT_RUN','reason':'Permission denial fixture uses POSIX chmod; covered on Linux'});continue
            binding.chmod(0);reason='IO_ERROR';code=2
        if label=='symlink':
            target=root/'link-target';target.mkdir(exist_ok=True);t.put(target/'sentinel.txt','Do not follow')
            if os.name=='nt':
                # Fixed audit-owned paths; apostrophes are doubled for PowerShell literals.
                link=skill/'linked';q=lambda p:"'"+str(p).replace("'","''")+"'"
                r,out,err=t.run(host+'-junction-setup',['powershell.exe','-NoProfile','-Command','New-Item -ItemType Junction -Path '+q(link)+' -Target '+q(target)+' | Out-Null'],expected='Create synthetic junction within disposable fixture')
                if r['exit']!=0:t.RESULTS.append({'case':host+'-symlink','status':'NOT_RUN','reason':err});continue
            else:(skill/'linked').symlink_to(target,target_is_directory=True)
            reason='UNSAFE_PATH';code=1
        result=t.check(host+'-'+label,[sys.executable,'-B','-X','utf8',skill/'scripts/check_project_binding.py','--project-root',project,'--skill-root',skill],code,'reason_code',reason,extra=lambda o,out,err:'project_id' not in out)
        if label=='io-error':binding.chmod(0o600)
    t.put(t.RUN/('platform-'+host+'-results.json'),{'host':platform.platform(),'python':sys.version,'results':t.RESULTS})
    print(json.dumps({'cases':len(t.RESULTS),'failures':[r['case'] for r in t.RESULTS if r['status']=='FAIL']}))

if __name__=='__main__':main()
