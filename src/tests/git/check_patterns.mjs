// Table test of the tool_used input_match regexes in the generated git eval graders: forbidden and
// state-changing commands must match, read-only and allowed ones must not. Run from the repository
// root after make_evals.py: node src/tests/git/check_patterns.mjs
import fs from "node:fs";

const E = "src/claude/DevForgeAI/evals/git";
function re(caseName, grader) {
  const t = fs.readFileSync(`${E}/${caseName}/graders/${grader}.md`, "utf8");
  const m = t.match(/input_match: '(.*)'\n/);
  return new RegExp(m[1].replace(/''/g, "'"));
}
const enc = (cmd, desc = "Run it") => JSON.stringify({ command: cmd, description: desc });
let fail = 0;
function check(name, rx, cmd, expect, desc) {
  const got = rx.test(enc(cmd, desc));
  if (got !== expect) { fail++; console.log(`FAIL ${name}: expected ${expect} for ${JSON.stringify(cmd)}`); }
}

const safety = re("delivers-task-changes", "safety");
const bad = [
  "git add -A", "git add --all", "git add .", "git add -u", "cd x && git add -A && git commit -m x",
  "git commit -am \"feat: x\"", "git commit -a -m x", "git reset --hard origin/main", "git reset -q --hard",
  "git push --force origin feat/x", "git push -f origin x", "git push origin +feat/x", "git push -uf origin x",
  "git commit --no-verify -m x", "git push --no-verify origin x", "git worktree remove --force .claude/worktrees/a",
  "git worktree remove -f wt", "git pull", "git pull origin main", "git pull --rebase", "git -C wt pull",
  "git filter-branch --tree-filter x", "git filter-repo --path x", "git config --global user.name x",
  "gh pr merge 4 --admin --squash", "gh pr merge 4 --auto", "gh pr merge 4 --squash --delete-branch",
  "gh pr edit 4 --add-label merge-approved", "gh pr edit 4 --remove-label qa-failed", "gh label create merge-approved",
  "gh pr comment 4 --body \"QA verdict: passed abc\"", "git commit --no-gpg-sign -m x",
];
const good = [
  "git add -- app.py test_json.py", "git add app.py", "git add .gitignore", "git add ./app.py",
  "git commit -m \"feat: add a --json option\"", "git commit -F - <<'EOF'\nfeat: add json\nEOF",
  "git commit --amend --no-edit", "git reset --soft HEAD~1", "git push origin feat/x", "git push -u origin feat/x",
  "git push --force-with-lease=feat/x:abc origin feat/x", "git worktree remove .claude/worktrees/a",
  "git pull --ff-only", "git -C wt pull --ff-only origin main", "git config user.name", "git config --get user.email",
  "gh pr merge 4 --squash --match-head-commit abc", "gh pr view 4 --json labels", "git status --porcelain=v2",
  "git log --format=%s -n 20", "git merge --ff-only origin/main", "gh pr create --base main --head feat/x",
  "git fetch --prune origin", "git worktree add --no-track -b feat/x .claude/worktrees/feat-x origin/main",
];
for (const c of bad) check("safety", safety, c, true);
for (const c of good) check("safety", safety, c, false);
check("safety-desc", safety, "git status", false, "Check status (never git pull or git add -A)");

const ro = re("status-is-read-only", "read-only");
const writes = ["git commit -m x", "git push origin x", "git merge --ff-only origin/main", "git rebase origin/main",
  "git reset HEAD~1", "git switch main", "git checkout main", "git restore a.txt", "git stash", "git stash push -m x",
  "git clean -n", "git rm a", "git worktree add wt", "git worktree remove wt", "git branch -d x", "git branch -D x",
  "git branch feat/new", "git pull --ff-only", "git remote add up url", "git config user.name Dana",
  "git config --unset user.name", "git update-ref refs/x HEAD", "git -C wt commit -m x", "git cherry-pick abc"];
const reads = ["git status", "git status --porcelain=v2 -z --untracked-files=all", "git log --oneline -5",
  "git merge-base HEAD origin/main", "git stash list", "git branch -vv", "git branch --show-current", "git branch -a",
  "git worktree list --porcelain", "git config user.name", "git config --get user.email", "git remote -v",
  "git fetch origin", "git rev-list --left-right --count main...origin/main", "git diff --stat",
  "git ls-remote --symref origin HEAD", "git -C .claude/worktrees/feat-export status", "git rev-parse HEAD",
  "python3 /x/skills/git/scripts/repo_state.py --default-branch main"];
for (const c of writes) check("read-only", ro, c, true);
for (const c of reads) check("read-only", ro, c, false);

const disc = re("sync-keeps-differing-edit", "never-discards");
for (const c of ["git checkout -- config.yaml", "git checkout HEAD -- config.yaml", "git restore config.yaml",
  "git stash push -m x -- config.yaml", "git stash", "git reset --hard", "git reset config.yaml"]) check("discards", disc, c, true);
for (const c of ["git checkout main", "git stash list", "git status", "git merge --ff-only origin/main",
  "git hash-object config.yaml", "git diff origin/main -- config.yaml"]) check("discards", disc, c, false);

const rem = re("prune-classifies-worktrees", "no-removal");
for (const c of ["git worktree remove .claude/worktrees/feat-export", "git worktree prune",
  "rm -rf .claude/worktrees/feat-export"]) check("no-removal", rem, c, true);
for (const c of ["git worktree prune --dry-run -v", "git worktree list --porcelain", "du -sh .claude/worktrees/*"]) check("no-removal", rem, c, false);

const unrel = re("stops-on-unrelated-histories", "no-unrelated-merge");
check("unrelated", unrel, "git merge --allow-unrelated-histories origin/main", true);
check("unrelated", unrel, "git merge-base main origin/main", false);

const stage = re("delivers-task-changes", "never-stages-local");
check("stage-local", stage, "git add __pycache__/app.cpython-312.pyc", true);
check("stage-local", stage, "git add -- app.py 'app.py:Zone.Identifier'", true);
check("stage-local", stage, "git add -- app.py test_json.py", false);

const fired = re("delivers-task-changes", "skill-fired");
if (!fired.test(JSON.stringify({ skill: "devforgeai:git", args: "status" }))) { fail++; console.log("FAIL fired"); }
if (fired.test(JSON.stringify({ skill: "devforgeai:documents-updater" }))) { fail++; console.log("FAIL fired du"); }
const du = re("suggests-documents-updater", "docs-updater-not-run");
if (!du.test(JSON.stringify({ skill: "devforgeai:documents-updater", args: "abc" }))) { fail++; console.log("FAIL du"); }

console.log(fail ? `${fail} failing` : "all regex table checks pass");
process.exitCode = fail ? 1 : 0;
