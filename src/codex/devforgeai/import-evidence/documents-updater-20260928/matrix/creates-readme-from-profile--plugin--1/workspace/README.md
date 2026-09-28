# csvtidy

`csvtidy` is a command-line tool for cleaning CSV files. It trims leading and
trailing whitespace from every cell and can remove rows whose cells are all empty
after trimming.

## Prerequisites

- Python 3.11 or later, with `pip` and `venv` available.
- A local copy of this repository.

## Quick start

From the repository root, install into a virtual environment. These commands use
a POSIX shell (such as Bash):

```bash
python3 -m venv .venv
. .venv/bin/activate
python -m pip install .
```

Create a sample CSV and clean it:

```bash
printf ' name , city \n Alice , Paris \n , \n' > sample.csv
csvtidy sample.csv --drop-empty
```

The cleaned CSV is written to standard output:

```csv
name,city
Alice,Paris
```

## Usage

```text
csvtidy [-h] [-o OUTPUT] [--drop-empty] input
```

| Argument or option | Behavior |
| --- | --- |
| `input` | Required path to the CSV file to read. |
| `-o OUTPUT`, `--output OUTPUT` | Write to a file instead of standard output. An existing output file is overwritten. |
| `--drop-empty` | Remove rows whose cells are all empty after trimming. Empty rows are kept by default. |
| `-h`, `--help` | Show command help and exit. |

For example, save the cleaned sample to a file:

```bash
csvtidy sample.csv --drop-empty --output cleaned.csv
```

Input and output files use UTF-8 encoding. CSV is comma-delimited, and the first
row is processed like every other row, including trimming any header cells.

## Development

The CLI is implemented in [src/csvtidy/cli.py](src/csvtidy/cli.py), with tests in
[tests/test_cli.py](tests/test_cli.py). `pytest` is needed separately to run tests;
it is not declared as a project dependency.

With `pytest` available in your Python environment, run from the repository root:

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src python3 -m pytest -p no:cacheprovider
```
