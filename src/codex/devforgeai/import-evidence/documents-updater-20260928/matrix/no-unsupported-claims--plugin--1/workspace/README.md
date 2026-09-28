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

Use `--jobs N` to count up to N files in parallel:

```bash
wordcount --jobs 2 notes.txt draft.txt
```

`N` must be an integer of at least 1. The default is 1, which counts one file at
a time. Output follows the order of the file arguments, even when counting in
parallel.
