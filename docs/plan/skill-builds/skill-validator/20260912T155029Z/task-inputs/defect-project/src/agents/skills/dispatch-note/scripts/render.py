import json, sys
from pathlib import Path
data=json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
out=Path(sys.argv[2])
out.write_text("partial\n",encoding="utf-8")
if not isinstance(data.get("units"),int) or data["units"]<=0:
    print("units invalid",file=sys.stderr); sys.exit(3)
out.write_text(json.dumps({"id":data["order_id"],"quantity":data["units"],"status":"ready"}),encoding="utf-8")
print(str(out))
