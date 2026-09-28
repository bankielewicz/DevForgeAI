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
| `--json` | Print a JSON object with integer `words` and `lines` counts |

To get JSON output:

```bash
wordcount notes.txt --json
```

For a file containing 12 words on 3 lines, this prints:

```json
{"words": 12, "lines": 3}
```

When combined with `--lines`, `--json` takes precedence and prints both counts.
