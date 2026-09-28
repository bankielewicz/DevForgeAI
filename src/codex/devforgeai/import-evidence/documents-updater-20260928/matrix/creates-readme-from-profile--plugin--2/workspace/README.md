# csvtidy

`csvtidy` is a command-line tool for cleaning CSV files. It trims leading and
trailing whitespace from every cell and can drop rows whose cells are all empty
after trimming.

## Prerequisites

- Python 3.11 or later.
- pip to install the package from this checkout.

## Quick start

From the repository root, install the package into your Python environment
(preferably a virtual environment):

```bash
python3 -m pip install .
```

Save this sample as `input.csv`:

```csv
 name , city
 Alice , London
 ,
 Bob , Paris
```

Trim the cells and remove the empty row:

```bash
csvtidy input.csv --drop-empty
```

The cleaned CSV is written to standard output:

```csv
name,city
Alice,London
Bob,Paris
```

## Usage

```text
csvtidy [-h] [-o OUTPUT] [--drop-empty] input
```

| Argument or option | Behavior |
| --- | --- |
| `input` | Required path to a UTF-8 CSV file. |
| `-o OUTPUT`, `--output OUTPUT` | Write to a UTF-8 file, replacing its contents if it exists. Defaults to standard output. |
| `--drop-empty` | Drop rows whose cells are all empty after trimming. Empty rows are retained by default. |
| `-h`, `--help` | Show help and exit. |

To write the result to a file:

```bash
csvtidy input.csv --drop-empty --output cleaned.csv
```

Files use comma-separated CSV syntax. Every row, including a header row, is
trimmed in the same way.

## Development

The CLI implementation is in [src/csvtidy/cli.py](src/csvtidy/cli.py), and the
existing test is in [tests/test_cli.py](tests/test_cli.py).

With pytest installed, run the tests from the repository root using a POSIX shell:

```bash
PYTHONPATH=src python3 -m pytest
```
