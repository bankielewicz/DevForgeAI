// Grades one context eval case's regex and file_exists graders offline, with JavaScript RegExp as
// `claude plugin eval` does, against a workspace (the case's scaffold, then a real or simulated run) and a
// file holding the final reply. tool_used and llm graders are reported as null. file_exists counts only
// files the run created, as the harness does: pass the scaffold's paths as a JSON list in <seeded.json>.
// A path ending in /** means "any file under that folder".
// Usage: node src/tests/context/grade_evals.mjs <case-dir> <workspace> <reply-file> [<seeded.json>]
// Prints one JSON object, {"<grader>": true | false | null, ...}.
import fs from "node:fs";
import path from "node:path";

const [caseDir, ws, replyFile, seededFile] = process.argv.slice(2);
const reply = fs.readFileSync(replyFile, "utf8");
const seeded = new Set(seededFile ? JSON.parse(fs.readFileSync(seededFile, "utf8")) : []);

const created = (p) => {
  if (!p.endsWith("/**")) return fs.existsSync(path.join(ws, p)) && !seeded.has(p);
  const rel = p.slice(0, -3);
  const dir = path.join(ws, rel);
  return fs.existsSync(dir) && fs.readdirSync(dir, { recursive: true })
    .some((f) => fs.statSync(path.join(dir, f)).isFile() && !seeded.has(`${rel}/${f}`));
};

const results = {};
for (const g of fs.readdirSync(path.join(caseDir, "graders")).sort()) {
  const text = fs.readFileSync(path.join(caseDir, "graders", g), "utf8");
  const m = text.match(/^---\n([\s\S]*?)\n---\n?([\s\S]*)$/);
  const fm = Object.fromEntries(m[1].split("\n").map((l) => {
    const i = l.indexOf(":");
    return [l.slice(0, i).trim(), l.slice(i + 1).trim()];
  }));
  const name = g.replace(/\.md$/, "");
  if (fm.type === "regex") {
    let target;
    if (fm.target === "last_message") target = reply;
    else {
      const f = path.join(ws, fm.target.match(/path: ([^}]+)\}/)[1].trim());
      target = fs.existsSync(f) ? fs.readFileSync(f, "utf8") : null;
    }
    const hit = target !== null && new RegExp(m[2].replace(/\n$/, ""), fm.flags || "").test(target);
    results[name] = target !== null && (fm.match === "contains" ? hit : !hit);
  } else if (fm.type === "file_exists") {
    results[name] = created(fm.path) === (fm.exists === "true");
  } else {
    results[name] = null;
  }
}
console.log(JSON.stringify(results));
