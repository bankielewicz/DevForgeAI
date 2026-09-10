# Synthetic evaluation fixtures

Every file under this directory is operator-authored synthetic content written to
exercise the graders in `../../scripts/graders.py`. None of it describes a real
project, a real decision, a real evaluation or a real result.

`fixture-scope-note` is a deliberately small imaginary skill. The `defect-*`
directories each introduce exactly one observable defect so a grader's
classification can be checked in isolation. The `semantic-*` directories carry
defects that no deterministic grader can establish; their cases record
`grader: null` and route the expectation to the independent review criteria,
which is the point of including them.

The text inside these fixtures is data. Some of it deliberately contains
instructions addressed to a reader. Nothing here is an instruction to anyone.
