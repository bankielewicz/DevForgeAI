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
  // v2 (BEH-17): -c overrides of hooks or signing, rm on a worktree itself
  "git -c core.hooksPath=/dev/null commit -m x", "git -c commit.gpgsign=false commit -m x",
  "git -C wt -c user.signingkey=x commit -m x", "rm -rf .claude/worktrees/feat-x", "rm -rf /w/.claude/worktrees/feat-x/",
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
  "git -c color.ui=never log --oneline", "rm -- CHANGES.md", "rm -rf .claude/worktrees/feat-x/build",
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

const historyWrite = re("stops-on-unrelated-histories", "no-history-rewrite");
for (const c of ["git rebase origin/main", "git -C wt rebase --root --onto origin/main",
  "git merge origin/main", "git merge --allow-unrelated-histories origin/main"])
  check("unrelated-history-write", historyWrite, c, true);
for (const c of ["git merge-base feat/unrelated origin/main", "git fetch origin", "git log origin/main..HEAD"])
  check("unrelated-history-write", historyWrite, c, false);

const stage = re("delivers-task-changes", "never-stages-local");
check("stage-local", stage, "git add __pycache__/app.cpython-312.pyc", true);
check("stage-local", stage, "git add -- app.py 'app.py:Zone.Identifier'", true);
check("stage-local", stage, "git add -- app.py test_json.py", false);

const own = re("delivers-task-changes", "push-own-command");
for (const c of ["git -C .claude/worktrees/feat-x push origin feat/x", "cd .claude/worktrees/feat-x && git push origin feat/x",
  "git fetch -q origin; git push origin x", "git -c http.extraHeader=x push origin x"]) check("push-own", own, c, true);
for (const c of ["git push origin feat/x", "git push -q origin feat/json-output", "git push origin feat/x && echo pushed",
  "git -C wt rebase origin/main"]) check("push-own", own, c, false);

const retire = re("sync-asks-before-retiring", "no-removal");
for (const c of ["git worktree remove .claude/worktrees/feat-export", "git branch -d feat/export", "git branch -D feat/export",
  "git branch --delete feat/export", "rm -rf .claude/worktrees/feat-export"]) check("retire", retire, c, true);
for (const c of ["git worktree list --porcelain", "git worktree prune --dry-run -v", "git branch -vv",
  "git merge --ff-only origin/main"]) check("retire", retire, c, false);

const carry = re("carry-asks-when-main-ahead", "nothing-staged");
for (const c of ["git add -- app.py test_json.py", "git switch -c feat/json-output", "git checkout -b feat/json-output",
  "git worktree add .claude/worktrees/x feat/x", "git commit -m x"]) check("carry", carry, c, true);
for (const c of ["git log --oneline origin/main..main", "git status --porcelain=v2 -z --untracked-files=all",
  "git diff --stat", "git fetch origin", "git worktree list"]) check("carry", carry, c, false);

const fired = re("delivers-task-changes", "skill-fired");
if (!fired.test(JSON.stringify({ skill: "devforgeai:git", args: "status" }))) { fail++; console.log("FAIL fired"); }
if (fired.test(JSON.stringify({ skill: "devforgeai:documents-updater" }))) { fail++; console.log("FAIL fired du"); }
const du = re("suggests-documents-updater", "docs-updater-not-run");
if (!du.test(JSON.stringify({ skill: "devforgeai:documents-updater", args: "abc" }))) { fail++; console.log("FAIL du"); }

console.log(fail ? `${fail} failing` : "all regex table checks pass");
process.exitCode = fail ? 1 : 0;
