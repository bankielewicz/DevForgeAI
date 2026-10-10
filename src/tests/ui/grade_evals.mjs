// Grades one ui eval case's graders offline, with JavaScript RegExp as `claude plugin eval` does, against a
// workspace (the case's scaffold, then a real or simulated run), a file holding the final reply and, for tool_used
// graders, a JSON list of the run's tool calls. regex and file_exists graders are always graded; a tool_used grader is
// reported as null when no tool-call list is given. file_exists counts only files the run created, as the harness
// does: pass the scaffold's paths as a JSON list in <seeded.json>. A path ending in /** means "any file under that
// folder". A tool call is {"tool": "Skill", "input": {...}}; input_match is tested against the input's JSON text.
// Usage: node src/tests/ui/grade_evals.mjs <case-dir> <workspace> <reply-file> [<seeded.json> [<calls.json>]]
// Prints one JSON object, {"<grader>": true | false | null, ...}.
import fs from "node:fs";
import path from "node:path";

const [caseDir, ws, replyFile, seededFile, callsFile] = process.argv.slice(2);
const reply = fs.readFileSync(replyFile, "utf8");
const seeded = new Set(seededFile ? JSON.parse(fs.readFileSync(seededFile, "utf8")) : []);
const calls = callsFile ? JSON.parse(fs.readFileSync(callsFile, "utf8")) : null;

const created = (p) => {
  if (!p.endsWith("/**")) return fs.existsSync(path.join(ws, p)) && !seeded.has(p);
  const rel = p.slice(0, -3);
  const dir = path.join(ws, rel);
  return fs.existsSync(dir) && fs.readdirSync(dir, { recursive: true })
    .some((f) => fs.statSync(path.join(dir, f)).isFile() && !seeded.has(`${rel}/${f}`));
};

const unquote = (v) => (v.length > 1 && v.startsWith("'") && v.endsWith("'") ? v.slice(1, -1).replace(/''/g, "'") : v);

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
  } else if (fm.type === "tool_used" && calls !== null) {
    const re = fm.input_match ? new RegExp(unquote(fm.input_match)) : null;
    const n = calls.filter((c) => c.tool === fm.tool
      && (!re || re.test(typeof c.input === "string" ? c.input : JSON.stringify(c.input)))).length;
    results[name] = n >= Number(fm.min ?? 0) && (fm.max === undefined || n <= Number(fm.max));
  } else {
    results[name] = null;
  }
}
console.log(JSON.stringify(results));
