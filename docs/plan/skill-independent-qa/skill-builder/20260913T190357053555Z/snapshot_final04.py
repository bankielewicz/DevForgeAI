from pathlib import Path
import json
import sys
sys.path.insert(0,str(Path(__file__).resolve().parent))
from capture import SOURCE, RUN, manifest
result=manifest(SOURCE,RUN/'source-final04/skill-builder')
assert result['package_digest']=='7715f8b80a9b089a4349f6bbb3b502a52d55a03bb2eb2ec65f861ea4be77ff3a'
(RUN/'source-final04-receipt.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
print(result['package_digest'],result['files'],result['bytes'])
