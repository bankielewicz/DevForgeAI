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
| `--json` | Print both counts as a JSON object; takes precedence over `--lines` |

For JSON output:

```bash
wordcount notes.txt --json
```

For a file with 12 words and 3 lines, prints:

```json
{"words": 12, "lines": 3}
```

The `words` and `lines` fields are integer counts. When `--json` and `--lines`
are used together, the JSON output still includes both fields.
