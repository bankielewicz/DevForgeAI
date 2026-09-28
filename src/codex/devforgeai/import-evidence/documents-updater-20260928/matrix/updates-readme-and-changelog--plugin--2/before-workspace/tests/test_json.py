import json

from wordcount.cli import main


def test_json_output(tmp_path, capsys):
    path = tmp_path / "t.txt"
    path.write_text("a b\nc")
    main([str(path), "--json"])
    assert json.loads(capsys.readouterr().out) == {"words": 3, "lines": 2}
