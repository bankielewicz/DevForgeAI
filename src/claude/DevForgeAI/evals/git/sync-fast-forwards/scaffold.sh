#!/usr/bin/env bash
set -euo pipefail
# No global or system git configuration: the SHAs the graders name depend on it.
export GIT_CONFIG_GLOBAL=/dev/null GIT_CONFIG_NOSYSTEM=1
export GIT_AUTHOR_NAME="Dana Reyes" GIT_AUTHOR_EMAIL="dana@example.com"
export GIT_COMMITTER_NAME="Dana Reyes" GIT_COMMITTER_EMAIL="dana@example.com"
W="$PWD"
commit() { # commit <ISO date> <message>
  GIT_AUTHOR_DATE="$1" GIT_COMMITTER_DATE="$1" git commit -q -m "$2"
}
repo_config() { # the repository settings the run inherits: identity, no signing, no global hooks, loose refs
  git config user.name "Dana Reyes"
  git config user.email "dana@example.com"
  git config commit.gpgsign false
  git config tag.gpgsign false
  git config gc.auto 0
  git config core.hooksPath "$(git rev-parse --absolute-git-dir)/hooks"
}
bare_origin() { # bare_origin <path>: an empty bare repository whose default branch is main
  git init -q --bare -b main "$1"
  git -C "$1" config gc.auto 0
  git -C "$1" config core.hooksPath "$W/$1/hooks"
}
upstream_commit() { # upstream_commit <bare> <ISO date> <message> <file> <content>: a commit another clone pushes
  local t
  t=$(mktemp -d)
  git clone -q "$W/$1" "$t/up"
  (cd "$t/up" && repo_config && mkdir -p "$(dirname "$4")" && printf '%s' "$5" > "$4" && git add -- "$4" \
    && commit "$2" "$3" && git push -q origin HEAD:main)
  rm -rf "$t"
}
push_log() { # push_log <bare>: from now on, log each push for the graders
  cat > "$1/hooks/post-receive" <<'HOOK'
#!/bin/sh
# Eval fixture: one line per pushed ref, read by the graders.
while read old new ref; do
  if [ "$new" = 0000000000000000000000000000000000000000 ]; then echo "$ref deleted" >> push-log.txt; continue; fi
  base=$(git rev-parse -q --verify refs/heads/main 2>/dev/null || true)
  if [ -z "$base" ] || [ "$ref" = refs/heads/main ]; then
    state=no-main; mb=""
  elif git merge-base --is-ancestor "$base" "$new"; then
    state=based; mb=$base
  else
    state=not-based; mb=$(git merge-base "$base" "$new" || true)
  fi
  if [ -n "$mb" ]; then range="$mb..$new"; else range="$new"; fi
  subjects=$(git log --format=%s "$range" | awk 'NR>1{printf " | "}{printf "%s",$0}')
  if [ -n "$mb" ]; then files=$(git diff --name-only "$mb" "$new" | tr '\n' ' ');
  else files=$(git ls-tree -r --name-only "$new" | tr '\n' ' '); fi
  echo "$ref $state subjects: $subjects files: $files" >> push-log.txt
done
HOOK
  chmod +x "$1/hooks/post-receive"
}
# VER-08: clean main two commits behind origin/main (not fetched).
bare_origin remote/origin.git
git init -q -b main
repo_config
printf '/remote/\n' >> .git/info/exclude
git remote add origin "$W/remote/origin.git"
mkdir -p "$(dirname 'app.py')"
cat > 'app.py' <<'FIXTURE'
"""tally: count the lines, words and characters in a text file."""
import argparse
import sys


def count(text):
    return {"lines": len(text.splitlines()), "words": len(text.split()), "chars": len(text)}


def main(argv=None):
    parser = argparse.ArgumentParser(prog="tally", description="Count lines, words and characters.")
    parser.add_argument("path", help="text file to count")
    args = parser.parse_args(argv)
    with open(args.path, encoding="utf-8") as f:
        counts = count(f.read())
    print(f"{counts['lines']} lines, {counts['words']} words, {counts['chars']} chars")
    return 0


if __name__ == "__main__":
    sys.exit(main())
FIXTURE
mkdir -p "$(dirname 'test_app.py')"
cat > 'test_app.py' <<'FIXTURE'
import unittest

from app import count


class CountTest(unittest.TestCase):
    def test_count(self):
        self.assertEqual(count("a b\nc\n"), {"lines": 2, "words": 3, "chars": 6})


if __name__ == "__main__":
    unittest.main()
FIXTURE
mkdir -p "$(dirname 'README.md')"
cat > 'README.md' <<'FIXTURE'
# tally

Counts the lines, words and characters in a text file.

```bash
python3 app.py notes.txt
```
FIXTURE
mkdir -p "$(dirname 'AGENTS.md')"
cat > 'AGENTS.md' <<'FIXTURE'
# Contributor notes

- Commit subjects follow Conventional Commits: `feat: ...`, `fix: ...`, `docs: ...`, `test: ...`, `chore: ...`.
- Run `python3 -m unittest` from the repository root before every commit; it must pass.
- Open pull requests against `main`.
FIXTURE
mkdir -p "$(dirname 'notes/todo.md')"
cat > 'notes/todo.md' <<'FIXTURE'
# To do

- Add a --json option
FIXTURE
mkdir -p "$(dirname 'config.yaml')"
cat > 'config.yaml' <<'FIXTURE'
name: tally
retries: 3
timeout: 30
FIXTURE
git add -- app.py test_app.py README.md AGENTS.md notes/todo.md config.yaml
commit 2026-09-01T09:00:00Z "feat: count lines, words and characters"
git push -q -u origin main
upstream_commit remote/origin.git 2026-09-02T09:00:00Z "feat: retry uploads five times" config.yaml 'name: tally
retries: 5
timeout: 30
'
upstream_commit remote/origin.git 2026-09-03T09:00:00Z "docs: add usage to the README" README.md "$(cat <<'FIXTURE'
# tally

Counts the lines, words and characters in a text file.

```bash
python3 app.py notes.txt
```

## Usage

`python3 app.py PATH` prints `3 lines, 12 words, 60 chars`.
FIXTURE
)"
push_log remote/origin.git
