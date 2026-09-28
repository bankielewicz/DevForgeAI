# csvtidy

A small command-line tool for cleaning CSV files. It trims leading and trailing
whitespace from every cell and can remove rows whose cells are all empty after
trimming.

## Requirements and installation

Python 3.11 or newer is required. From the project directory, create and activate
a virtual environment, then install the package:

```sh
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -e .
```

On Windows PowerShell, use `python` instead of `python3` to create the environment
and activate it with `.venv\Scripts\Activate.ps1`. The package has no third-party
runtime dependencies.

## Usage

```sh
csvtidy input.csv
csvtidy input.csv --output cleaned.csv
csvtidy input.csv --drop-empty -o cleaned.csv
csvtidy --help
```

| Argument | Description |
| --- | --- |
| `input` | Path to the CSV file to read. |
| `-o`, `--output` | Write to this file instead of standard output. An existing file is overwritten. |
| `--drop-empty` | Remove rows whose cells are all empty after trimming. |

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

Empty rows are retained unless `--drop-empty` is supplied. All rows, including
any header row, are processed the same way. Input and output files use UTF-8 and
Python's standard comma-separated CSV format. CSV quoting and line endings are
rewritten by Python's CSV writer; original formatting is not preserved.

You can also invoke the tool as a Python module after installation:

```sh
python -m csvtidy.cli input.csv --drop-empty
```

## Development

With the package installed in the virtual environment above, install pytest and
run the tests from the project directory:

```sh
python -m pip install pytest
python -m pytest
```

The command-line implementation is in `src/csvtidy/cli.py`, and tests are in
`tests/`.
