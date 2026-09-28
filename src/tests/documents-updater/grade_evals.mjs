// Checks one documents-updater eval case's regex and file_exists graders offline, with JS RegExp
// as claude plugin eval does, against a workspace built by the case's scaffold.sh (then edited by a
// real or simulated run) and a file holding the final reply. llm and tool_used graders are skipped,
// and file_exists only checks presence (the real grader counts files created during the run).
// Usage: node src/tests/documents-updater/grade_evals.mjs <case-dir> <workspace-dir> <reply-file>
import fs from "node:fs";
import path from "node:path";

const [caseDir, ws, replyFile] = process.argv.slice(2);
const reply = fs.readFileSync(replyFile, "utf8");
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
    const present = fs.existsSync(path.join(ws, fm.path));
    ok = present === (fm.exists === "true");
  } else {
    console.log(`  skip  ${g} (${fm.type})`);
    continue;
  }
  if (!ok) fail++;
  console.log(`  ${ok ? "PASS" : "FAIL"}  ${g} ${note}`);
}
console.log(fail ? `${fail} failing` : "all regex/file graders pass");
