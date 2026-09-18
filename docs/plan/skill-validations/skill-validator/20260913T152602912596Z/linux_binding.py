import sys
import independent_probes as probes
from qa_harness import RUN,execute,save
probes.BASE=RUN/'trials/linux-independent'
probes.results=[]
def linux_execute(name,argv):
    argv[0]=sys.executable
    result=execute('linux-'+name,argv)
    # Preserve the independent fixture's output accessor without duplicating raw
    # commands in counts: it reads B01 while the authoritative attempt is linux-B01.
    return result
# The binding function reads stdout under its case ID; allocate Linux-specific
# IDs by invoking an exact external copy of the harness with prefixed IDs.
source=(RUN/'independent_probes.py').read_text(encoding='utf-8')
for i in range(1,10): source=source.replace("'B%02d'"%i,"'linux-B%02d'"%i)
source=source.replace("BASE=RUN/'trials/independent'","BASE=RUN/'trials/linux-independent'")
copy=RUN/'trials/linux_binding_harness.py'
copy.parent.mkdir(parents=True,exist_ok=True)
copy.write_text(source,encoding='utf-8')
namespace={'__name__':'linux_fixture'}
exec(compile(source,str(copy),'exec'),namespace)
def invoke(name,argv):
    argv[0]=sys.executable
    return execute(name,argv)
namespace['execute']=invoke
namespace['bindings']()
