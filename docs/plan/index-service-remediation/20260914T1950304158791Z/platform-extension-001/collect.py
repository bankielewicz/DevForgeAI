import hashlib
import json
from pathlib import Path
import re
import tarfile

ROOT = Path(__file__).resolve().parent
hashes = {"linux":"4ce12761fe4f1c5a52ae576825d133c8c171d7291586eb60671f832d91665744", "wsl":"72a8832a7d1626af1c6c98218c188ec630a5b53aa0591d29b5a32dee116b486a"}
for host, expected in hashes.items():
    archive = ROOT / (host + "-evidence.tar.gz")
    assert hashlib.sha256(archive.read_bytes()).hexdigest() == expected
    destination = ROOT / host
    destination.mkdir(exist_ok=False)
    with tarfile.open(archive) as tar:
        for member in tar.getmembers():
            assert member.name == "evidence" or member.name.startswith("evidence/")
            assert member.isfile() or member.isdir()
            target = destination / Path(member.name).relative_to("evidence")
            target.resolve().relative_to(destination.resolve())
            if member.isdir():
                target.mkdir(parents=True,exist_ok=True)
            else:
                target.parent.mkdir(parents=True,exist_ok=True)
                target.write_bytes(tar.extractfile(member).read())
    report = json.loads((destination / "coverage.json").read_text())["data"][0]
    output = (destination / "attempts/coverage/stdout.txt").read_text()
    tests = re.findall(r"^test (\S+) \.\.\. (ok|FAILED|ignored)(?:, ([^\n]*))?$",output,re.M)
    result = {"archive_sha256":expected,"coverage":report["totals"]["lines"],"tests":len(tests),"passed":sum(t[1]=="ok" for t in tests),"failed":sum(t[1]=="FAILED" for t in tests),"ignored":sum(t[1]=="ignored" for t in tests),"per_file":[{"file":f["filename"],**f["summary"]["lines"]} for f in report["files"]]}
    (destination / "observed-metrics.json").write_text(json.dumps(result,indent=2)+"\n")
    print(json.dumps({"host":host,**result},indent=2))
