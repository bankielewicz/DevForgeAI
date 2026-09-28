from wordcount.cli import count


def test_count():
    assert count("a b\nc") == {"words": 3, "lines": 2}
