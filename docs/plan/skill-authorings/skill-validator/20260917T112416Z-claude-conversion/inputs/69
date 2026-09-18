"""Internal gated worker: never launches the target before receiving the payload."""
import base64
import json
import subprocess
import sys


def main():
    value = json.loads(sys.stdin.buffer.read())
    try:
        child = subprocess.run(value['argv'], cwd=value['cwd'],
                               input=base64.b64decode(value['stdin']),
                               creationflags=subprocess.CREATE_NO_WINDOW)
        return child.returncode
    except OSError as error:
        print('Trial target launch failed: ' + str(error), file=sys.stderr)
        return 70


if __name__ == '__main__':
    raise SystemExit(main())
