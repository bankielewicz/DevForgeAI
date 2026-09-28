from wordcount.cli import count_lines, count_words


def test_helpers():
    assert count_words("a b\nc") == 3
    assert count_lines("a b\nc") == 2
