import json
import tempfile

def save_and_list(name):
    with tempfile.TemporaryFile(mode="w+", encoding="utf-8") as output:
        json.dump([name], output, ensure_ascii=False)
        output.seek(0)
        return json.load(output)
