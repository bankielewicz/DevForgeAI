#!/usr/bin/env bash
# Builds the two environments the policy and context scripts' tests run under (#122): the oldest jsonschema the scripts
# must support, which has no `referencing` module, and a current one. The tests skip those classes, naming this file,
# when an environment is missing. Run it once per clone, from a plain shell, from the repository root; it needs the
# network. A worktree uses the main checkout's copy. It writes only under tmp/test-envs/, which is gitignored.
set -euo pipefail
base="$(dirname "$(git rev-parse --path-format=absolute --git-common-dir)")/tmp/test-envs"
for version in 4.10.3 4.26.0; do
  env="$base/jsonschema-$version"
  # Built only when its pip runs: an interrupted venv, or one made without ensurepip, is rebuilt (#155).
  "$env/bin/python" -m pip --version >/dev/null 2>&1 || python3 -m venv --clear "$env"
  "$env/bin/python" -m pip install --quiet "jsonschema==$version" pyyaml
  "$env/bin/python" -W ignore -c "import importlib.metadata as m, sys; print(sys.version.split()[0], 'jsonschema', m.version('jsonschema'))"
done
echo "environments in $base"
