import argparse,json,sys
from pathlib import Path
parser=argparse.ArgumentParser(description="Total an integer JSON array")
parser.add_argument("input");parser.add_argument("output")
args=parser.parse_args()
try:
    data=json.loads(Path(args.input).read_text(encoding="utf-8"))
    if type(data) is not list or any(type(item) is not int for item in data):
        raise ValueError("Expected an array containing only integers")
except (ValueError,OSError) as error:
    print(str(error),file=sys.stderr);raise SystemExit(2)
Path(args.output).write_text(json.dumps({"total": sum(data)}),encoding="utf-8")
