from prepare import *
save(RUN/'inputs/evaluation/graders-red.py',(RUN/'inputs/evaluation/graders.py').read_bytes())
command('grader-red',[sys.executable,'-B','-X','utf8','-m','unittest','discover','-s',str(RUN/'inputs/evaluation'),'-p','test_graders.py','-v'])
