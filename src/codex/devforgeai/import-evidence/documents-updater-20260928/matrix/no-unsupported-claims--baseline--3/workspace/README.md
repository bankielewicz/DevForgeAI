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

Use `--jobs N` to count up to N files at the same time:

```bash
wordcount --jobs 4 notes.txt draft.txt chapter.txt appendix.txt
```

`N` must be an integer of at least 1. The default is 1, which counts one file
at a time. Output keeps the same format and follows the order of the file paths
on the command line, even when files are counted in parallel.
