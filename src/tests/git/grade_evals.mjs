// Checks one git eval case's regex, file_exists and tool_used graders offline, with JS RegExp as
// claude plugin eval does, against a workspace built by the case's scaffold.sh and then changed by a
// real or simulated run. llm graders are skipped.
// Usage: node src/tests/git/grade_evals.mjs <case-dir> <workspace> <reply-file> [calls.json] [before.txt]
//   calls.json: [{"tool": "Bash", "input": {"command": "..."}}, ...], the run's tool calls, in order.
//   before.txt: the workspace's file list right after the scaffold (`find . -type f`), so file_exists
//   counts only files created during the run, as the real grader does. Without it, presence counts.
import fs from "node:fs";
import path from "node:path";

const [caseDir, ws, replyFile, callsFile, beforeFile] = process.argv.slice(2);
const reply = fs.readFileSync(replyFile, "utf8");
const calls = callsFile ? JSON.parse(fs.readFileSync(callsFile, "utf8")) : null;
const before = beforeFile
  ? new Set(fs.readFileSync(beforeFile, "utf8").split("\n").filter(Boolean).map((p) => p.replace(/^\.\//, "")))
  : null;

function walk(dir, rel = "") {
  let out = [];
  for (const e of fs.readdirSync(path.join(dir, rel), { withFileTypes: true })) {
    const r = rel ? `${rel}/${e.name}` : e.name;
    if (e.isDirectory()) out = out.concat(walk(dir, r));
    else out.push(r);
  }
  return out;
}

function globRe(glob) {
  let re = "";
  for (let i = 0; i < glob.length; i++) {
    const c = glob[i];
    if (c === "*" && glob[i + 1] === "*") { re += ".*"; i++; if (glob[i + 1] === "/") i++; }
    else if (c === "*") re += "[^/]*";
    else if (c === "?") re += "[^/]";
    else re += c.replace(/[.+^${}()|[\]\\]/g, "\\$&");
  }
  return new RegExp(`^${re}$`);
}

const files = walk(ws);
let fail = 0;
for (const g of fs.readdirSync(path.join(caseDir, "graders")).sort()) {
  const text = fs.readFileSync(path.join(caseDir, "graders", g), "utf8");
  const m = text.match(/^---\n([\s\S]*?)\n---\n?([\s\S]*)$/);
  const fm = Object.fromEntries(m[1].split("\n").map((l) => {
    const i = l.indexOf(":");
    return [l.slice(0, i).trim(), l.slice(i + 1).trim()];
  }));
  let ok, note = "";
  if (fm.type === "regex") {
    const pattern = m[2].replace(/\n$/, "");
    let target;
    if (fm.target === "last_message") target = reply;
    else {
      const p = fm.target.match(/path: ([^}]+)\}/)[1].trim();
      const f = path.join(ws, p);
      target = fs.existsSync(f) ? fs.readFileSync(f, "utf8") : null;
      if (target === null) note = `(missing ${p})`;
    }
    if (target === null) ok = false;
    else {
      const hit = new RegExp(pattern, fm.flags || "").test(target);
      ok = fm.match === "contains" ? hit : !hit;
    }
  } else if (fm.type === "file_exists") {
    const re = globRe(fm.path);
    const hits = files.filter((f) => re.test(f) && !(before && before.has(f)));
    ok = (hits.length > 0) === (fm.exists !== "false");
    if (hits.length) note = `(${hits.slice(0, 3).join(", ")})`;
  } else if (fm.type === "tool_used" && calls) {
    const input = fm.input_match ? new RegExp(fm.input_match.replace(/^'|'$/g, "").replace(/''/g, "'")) : null;
    const n = calls.filter((c) => c.tool === fm.tool && (!input || input.test(JSON.stringify(c.input)))).length;
    const min = fm.min === undefined ? 1 : Number(fm.min);
    const max = fm.max === undefined ? Infinity : Number(fm.max);
    ok = n >= min && n <= max;
    note = `(${n} matching call${n === 1 ? "" : "s"})`;
  } else {
    console.log(`  skip  ${g} (${fm.type})`);
    continue;
  }
  if (!ok) fail++;
  console.log(`  ${ok ? "PASS" : "FAIL"}  ${g} ${note}`);
}
console.log(fail ? `${fail} failing` : "all checked graders pass");
process.exitCode = fail ? 1 : 0;
