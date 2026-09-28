# csvtidy

A small command-line tool that cleans CSV files by trimming leading and trailing
whitespace from every cell. Optionally, it removes rows whose cells are all empty
after trimming.

## Requirements and installation

Python 3.11 or newer is required. From the project directory, create a virtual
environment and install the package:

```sh
python -m venv .venv
source .venv/bin/activate
python -m pip install .
```

On Windows, activate the environment with `.venv\Scripts\activate` in Command
Prompt instead. If your system provides `python3` rather than `python`, use
`python3 -m venv .venv` to create the environment.

## Usage

```sh
csvtidy input.csv
csvtidy input.csv --drop-empty
csvtidy input.csv --drop-empty --output cleaned.csv
csvtidy --help
```

| Argument | Description |
| --- | --- |
| `input` | Path to the CSV file to read. |
| `-o`, `--output` | Write to this file instead of standard output. An existing file is overwritten. |
| `--drop-empty` | Remove rows whose cells are all empty after trimming. |

Input files and output files use UTF-8 encoding. CSV files use commas as
delimiters. Every row is processed, including a header row if present. Empty
rows are retained unless `--drop-empty` is supplied.

For example, given `input.csv`:

```csv
name,city
 Alice , London
 ,
 Bob , Paris
```

Running `csvtidy input.csv --drop-empty` prints:

```csv
name,city
Alice,London
Bob,Paris
```

## Development

Install the package in editable mode and install pytest in your activated
virtual environment, then run the tests:

```sh
python -m pip install -e . pytest
python -m pytest
```

The command-line implementation lives in `src/csvtidy/cli.py`, and tests live in
`tests/`.
