from csvtidy.cli import tidy


def test_tidy_drops_empty_rows():
    assert list(tidy([[" a ", "b"], ["", " "]], drop_empty=True)) == [["a", "b"]]
