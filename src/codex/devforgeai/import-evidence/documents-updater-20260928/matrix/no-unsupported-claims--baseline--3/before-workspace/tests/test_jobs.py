from wordcount.cli import main


def test_jobs(tmp_path, capsys):
    paths = []
    for name in ("a.txt", "b.txt"):
        path = tmp_path / name
        path.write_text("one two")
        paths.append(str(path))
    main(paths + ["--jobs", "2"])
    assert capsys.readouterr().out.count("2 words") == 2
