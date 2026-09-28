# wordcount

Counts the words and lines in text files, for anyone scripting over plain text.

## Prerequisites

- Python 3.10 or later

## Install

From the repository root:

```bash
pip install .
```

## Usage

```bash
wordcount notes.txt draft.txt
```

Prints one line per file, such as `notes.txt: 12 words, 3 lines`.

To count up to two files at the same time:

```bash
wordcount --jobs 2 notes.txt draft.txt
```

`--jobs N` sets the maximum number of files counted at the same time. `N` must be
an integer of at least 1; the default is 1 (one file at a time). Results are
printed in the order the file paths were supplied.
