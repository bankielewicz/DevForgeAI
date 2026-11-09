#!/usr/bin/env bash
# Builds the scratch repository and input document for SPEC-020 VER-02 (docs/runbooks/tdd-agents-ver-02.md).
# Usage: bash src/tests/tdd-agents/make_scratch.sh <new-folder>
# The folder must not exist and must be outside every project. It gets:
#   repo/     a git repository with one commit: slug.py, tests/test_slug.py and a .gitignore for __pycache__
#   plan.md   the input document (SPEC-020 §4's twelve items; Refactor: allowed; one \u escape; no mutant)
# The verifier's disposable worktrees go in <new-folder>/verifier-wt, which this script does not create.
set -euo pipefail

[ $# -eq 1 ] || { echo "usage: make_scratch.sh <new-folder>" >&2; exit 2; }
[ ! -e "$1" ] || { echo "refusing: $1 exists" >&2; exit 2; }
mkdir -p "$1"
S=$(cd "$1" && pwd)
R="$S/repo"
mkdir -p "$R/tests"

cat > "$R/slug.py" <<'EOF'
def slugify(text):
    return text.strip().lower().replace(" ", "-")
EOF

cat > "$R/tests/test_slug.py" <<'EOF'
import unittest

from slug import slugify


class SlugTest(unittest.TestCase):
    def test_spaces_become_hyphens(self):
        self.assertEqual(slugify(" Hello World "), "hello-world")


if __name__ == "__main__":
    unittest.main()
EOF

printf '__pycache__/\n' > "$R/.gitignore"

git -C "$R" init -q -b main
git -C "$R" -c user.name=scratch -c user.email=scratch@example.invalid add .gitignore slug.py tests/test_slug.py
git -C "$R" -c user.name=scratch -c user.email=scratch@example.invalid commit -q -m "chore: slugify and its first test"
git -C "$R" config user.name scratch
git -C "$R" config user.email scratch@example.invalid
BASE=$(git -C "$R" rev-parse HEAD)

cat > "$S/plan.md" <<EOF
# Plan: slugify folds accented letters

The input document for one test-first change in the repository \`$R\`.

- Worktree: \`$R\`
- Base commit: \`$BASE\`
- Branch: \`main\`

## 1. Commits

The test-writer and the implementer may commit locally in the worktree. Nobody pushes.

| Commit | Message |
|---|---|
| red | \`test: slugify folds accented letters\` |
| green | \`fix: slugify folds accented letters\` |
| refactor | \`refactor: tidy slugify\` |

Refactor: allowed

## 2. The test command

The one command that runs the tests. Run in the worktree:

\`\`\`
cd $R && python3 -m unittest discover -s tests -v
\`\`\`

## 3. Tests to write

Baseline command for the test-writer, before any change: the test command of section 2. Required result: exit 0,
\`Ran 1 test\`, \`OK\`.

In \`tests/test_slug.py\`, insert this method after the method \`test_spaces_become_hyphens\`, inside \`SlugTest\`,
with one blank line before it:

\`\`\`python
    def test_folds_accented_letters(self):
        self.assertEqual(slugify("Caf\\u00e9 au lait"), "cafe-au-lait")
\`\`\`

The string holds the six characters backslash, u, 0, 0, e, 9: an escape, not the letter it stands for. If your tool
writes the letter instead, leave it as written and go on. Then run, in the worktree:

\`\`\`
cd $R && grep -c 'u00e9' tests/test_slug.py
\`\`\`

and state under CLAIMS which form the file holds (\`1\`: the escape; \`0\`: the letter). Either result is allowed.

**Red result required**, from the test command: exit code 1; \`Ran 2 tests\`; \`test_folds_accented_letters\` fails with
an \`AssertionError\`; \`test_spaces_become_hyphens\` passes (\`ok\`).

## 4. The code change

In \`slug.py\`, \`slugify\` must fold accented letters to their base letters before lowercasing: decompose the text
with \`unicodedata.normalize("NFKD", text)\` and drop every character for which \`unicodedata.combining\` is non-zero.
Its name, its one parameter and its existing behaviour (strip, lowercase, spaces to hyphens) stay. The code is
described here, not given to copy.

Files of the green commit: \`slug.py\`. Files of the refactor commit, when there is one: \`slug.py\`.

There are no document edits.

## 5. Verification commands

1. The test command of section 2. Required result: exit 0, \`Ran 2 tests\`, \`OK\`. Run by: the implementer and
   the verifier.

## 6. Paths allowed to change

| Between | Paths |
|---|---|
| base and red | \`tests/test_slug.py\` |
| red and green | \`slug.py\` |
| green and final | \`slug.py\` |

## 7. The verifier's disposable worktrees

Folder: \`$S/verifier-wt\` (outside the repository; it doesn't exist until the verifier adds a worktree there, and
its parent does). No command is needed to prepare one. In it, the test command of section 2 runs with that folder
in place of the worktree.

There are no mutants.

## Acceptance criteria

1. At the red commit, in a disposable worktree, the test command exits 1, prints \`Ran 2 tests\`,
   \`test_folds_accented_letters\` fails with an \`AssertionError\`, and \`test_spaces_become_hyphens\` is \`ok\`.
2. At the final commit, in the worktree, the test command of section 2 exits 0 and prints \`Ran 2 tests\` and \`OK\`.
3. \`git -C $R diff --name-only <base commit> <red commit>\` prints exactly \`tests/test_slug.py\`.
4. \`git -C $R diff --name-only <red commit> <final commit>\` prints exactly \`slug.py\`.
EOF

echo "scratch: $S"
echo "worktree: $R"
echo "base commit: $BASE"
echo "input document: $S/plan.md"
