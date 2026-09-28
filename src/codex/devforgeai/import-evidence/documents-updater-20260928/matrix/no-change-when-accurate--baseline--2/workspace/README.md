# wordcount

Counts the words and lines in a text file, for anyone scripting over plain text.

## Prerequisites

- Python 3.10 or later

## Install

From the repository root:

```bash
pip install .
```

## Usage

```bash
wordcount notes.txt
```

Prints `12 words, 3 lines`.

| Option | Effect |
| --- | --- |
| `--lines` | Print only the line count |
| `--json` | Print the counts as a JSON object, for example `{"words": 12, "lines": 3}` |

## Python usage

Use `count_words()` or `count_lines()` to count a string, or `count()` to get both counts:

```python
>>> from wordcount.cli import count, count_lines, count_words
>>> text = "a b\nc"
>>> count_words(text)
3
>>> count_lines(text)
2
>>> count(text)
{'words': 3, 'lines': 2}

```

Words are separated by whitespace, using Python's `str.split()`. Lines are
counted using `str.splitlines()`: a final line without a newline counts, and a
trailing newline does not add an extra line. Both helpers return `0` for an
empty string.
