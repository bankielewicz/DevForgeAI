# csvtidy

`csvtidy` is a command-line tool for cleaning CSV files. It trims leading and
trailing whitespace from every cell and optionally removes rows whose cells are
all empty after trimming.

## Prerequisites

- Python 3.11 or newer.
- `pip` to install from this source checkout.

## Quick start

From the repository root, install the package into your Python environment:

```bash
python3 -m pip install .
```

Save the following as `input.csv`:

```csv
name,city
" Alice "," London "
" "," "
" Bob "," Paris "
```

Trim the cells and remove the empty row:

```bash
csvtidy input.csv --drop-empty
```

The cleaned CSV is printed to standard output:

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
| `input` | Required path to the CSV file to read. |
| `-o OUTPUT`, `--output OUTPUT` | Write to a file, overwriting it if it exists. Defaults to standard output. |
| `--drop-empty` | Remove rows whose cells are all empty after trimming. Empty rows are kept by default. |
| `-h`, `--help` | Show usage information and exit. |

To save the cleaned result to a file:

```bash
csvtidy input.csv --drop-empty --output cleaned.csv
```

Input files and output files use UTF-8 encoding. CSV fields are comma-separated;
the first row is trimmed like every other row. The tool reads the entire input
into memory before writing output.

## Development

The CLI implementation is in [src/csvtidy/cli.py](src/csvtidy/cli.py), and the
existing test is in [tests/test_cli.py](tests/test_cli.py).

With `pytest` available in your Python environment, run the test from the
repository root using a POSIX shell:

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src python3 -m pytest -p no:cacheprovider
```

You can also run the CLI directly from the checkout without installing it:

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src python3 -m csvtidy.cli --help
```
