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

## Counting helpers

The counting logic in `wordcount.cli` is split into two helpers:

- `count_words(text)` counts whitespace-separated words using `str.split()`.
- `count_lines(text)` counts lines using `str.splitlines()`. A final line break does not add an extra line.

Both helpers return `0` for an empty string. The existing `count(text)` function
combines their results into a dictionary with `words` and `lines` keys:

```python
from wordcount.cli import count, count_lines, count_words

text = "a b\nc"
assert count_words(text) == 3
assert count_lines(text) == 2
assert count(text) == {"words": 3, "lines": 2}
```
