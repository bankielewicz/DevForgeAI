# csvtidy

A small command-line tool that cleans CSV files by trimming leading and trailing
whitespace from every cell. It can also remove rows whose cells are all empty
after trimming.

## Requirements and installation

Python 3.11 or newer is required. From the project directory, create and activate
a virtual environment, then install the package:

```sh
python -m venv .venv
source .venv/bin/activate
python -m pip install .
```

If your system uses `python3` instead of `python`, use `python3 -m venv .venv`
for the first command.

On Windows, activate the environment with `.venv\Scripts\activate` in Command
Prompt or `.venv\Scripts\Activate.ps1` in PowerShell.

## Usage

```sh
# Trim cells and print the cleaned CSV to standard output.
csvtidy input.csv

# Write the cleaned CSV to a file and remove empty rows.
csvtidy input.csv --drop-empty --output cleaned.csv

# Show command-line help.
csvtidy --help
```

| Argument | Description |
| --- | --- |
| `input` | Path to the CSV file to read (required). |
| `-o`, `--output` | Destination file; defaults to standard output. An existing destination file is overwritten. |
| `--drop-empty` | Remove rows whose cells are all empty after trimming. |

Input and output files use UTF-8 and standard comma-separated CSV formatting.
Every row is processed, including any header row. Empty rows are retained unless
`--drop-empty` is supplied.

For example, given `input.csv`:

```csv
 name , city
 Alice , London
 ,
 Bob , Paris
```

Running `csvtidy input.csv --drop-empty` produces:

```csv
name,city
Alice,London
Bob,Paris
```

## Development

Install the package in editable mode and install pytest in your activated
virtual environment:

```sh
python -m pip install -e .
python -m pip install pytest
python -m pytest
```

The command-line implementation is in `src/csvtidy/cli.py`; tests are in
`tests/test_cli.py`. You can also run the installed tool as a Python module:

```sh
python -m csvtidy.cli input.csv --drop-empty
```
