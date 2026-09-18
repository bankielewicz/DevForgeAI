# ledger-d requirements
This portable skill totals supplied integer JSON arrays. The user supplies input JSON and a selected output path.
R1: When given a JSON array of integers, write JSON object {"total": sum of the elements} at the selected output path. Negative integers and empty arrays are valid.
R2: Reject non-array input or any element that is not an integer (including Boolean values) with nonzero exit and a useful stderr diagnostic; create no output file on invalid input.
R3: Preserve source input bytes and unrelated files. Never substitute completion prose for the requested output file.
R4: The helper scripts/total.py takes INPUT OUTPUT as two positional arguments, supports --help, and must operate on Windows Python 3 without third-party packages.
The skill may use its helper for execution. Validation may inspect and run the helper on disposable inputs. No network, installation, or production service is needed for this skill's work.
