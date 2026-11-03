"""Generate the dev-guard character-grid boards (one font size, one cell per character) as .dc.html files,
plus the canvas.json entries. Run: python3 gen_grid.py <project dir>"""
import html, json, re, sys
from pathlib import Path

OUT = Path(sys.argv[1])
CH, LH, PAD = 8.4, 20, 16
COLS = {"full": 76, "medium": 50, "compact": 36}
STY = {"t": "color:#ECEAE3", "d": "color:#A3A198", "a": "color:#D97757;font-weight:600", "g": "color:#0ca30c",
       "w": "color:#fab219", "r": "color:#d03b3b", "b": "color:#3987e5", "B": "color:#ECEAE3;font-weight:600",
       "D": "color:#6E6C66"}
BREAK = set("/-_(")


def parse(m):
    out, st = [], "t"
    for part in re.split(r"(«[^»]*»)", m):
        if part.startswith("«"):
            st = "t" if part == "«/»" else part[1:-1]
        else:
            out += [(c, st) for c in part]
    return out


def wrap(m, width, ind0=0, ind1=None):
    """Wrap a markup string to width; ind0 first-line indent, ind1 continuation indent."""
    ind1 = ind0 if ind1 is None else ind1
    chars = parse(m)
    words, cur = [], []
    for c in chars:
        if c[0] == " ":
            if cur:
                words.append(cur); cur = []
        else:
            cur.append(c)
    if cur:
        words.append(cur)
    lines, line, indent = [], [], ind0

    def avail():
        return width - indent - (len(line) + (1 if line else 0))

    def flush():
        nonlocal line, indent
        lines.append([(" ", "t")] * indent + line)
        line, indent = [], ind1

    for w in words:
        while w:
            if len(w) <= avail():
                line += ([(" ", "t")] if line else []) + w
                w = []
            elif line and len(w) <= width - ind1:
                flush()
            else:  # too long even for a fresh line: break after / - _ ( where possible, on this line
                room = avail()
                cut = max((i + 1 for i, c in enumerate(w[:room]) if c[0] in BREAK), default=0)
                if cut == 0 and line:
                    flush()
                    continue
                if cut == 0:
                    cut = room
                line += ([(" ", "t")] if line else []) + w[:cut]
                w = w[cut:]
                flush()
    if line or not lines:
        flush()
    return lines


def pad(line, width, st="t"):
    return line + [(" ", st)] * (width - len(line))


def seg(m):
    return parse(m)


def lr(left, right, width):
    L, R = parse(left), parse(right)
    if len(L) + 2 + len(R) <= width:
        return [L + [(" ", "t")] * (width - len(L) - len(R)) + R]
    return [L, R]


def box(specs, width, border="D", title=None, right=None):
    inner = width - 4
    rows = []
    T = parse(title) if title else []
    R = parse(right) if right else []
    top = [("╭", border), ("─", border)]
    extra = []
    if T:
        top += [(" ", border)] + T + [(" ", border)]
    if R and len(top) + len(R) + 4 <= width:
        fill = width - len(top) - len(R) - 4
        top += [("─", border)] * fill + [(" ", border)] + R + [(" ", border), ("─", border), ("╮", border)]
    else:
        top += [("─", border)] * (width - len(top) - 1) + [("╮", border)]
        if R:
            extra = [(right, 0, 0)]
    rows.append(top)
    for spec in extra + specs:
        if spec == "":
            ls = [[]]
        elif spec == "rule":
            ls = [[("─", "D")] * inner]
        elif isinstance(spec, list):  # pre-built char line
            ls = [spec]
        else:
            m, i0, i1 = spec if isinstance(spec, tuple) else (spec, 0, 0)
            ls = wrap(m, inner, i0, i1)
        for l in ls:
            rows.append([("│", border), (" ", "t")] + pad(l, inner) + [(" ", "t"), ("│", border)])
    rows.append([("╰", border)] + [("─", border)] * (width - 2) + [("╯", border)])
    return rows


def lines(*specs, width):
    out = []
    for s in specs:
        if s == "":
            out.append([])
        elif isinstance(s, list):
            out += s
        else:
            m, i0, i1 = s if isinstance(s, tuple) else (s, 0, 0)
            out += wrap(m, width, i0, i1)
    return out


def hbar(v, m, cells):
    e = round(v / m * cells * 8) if m else 0
    return "█" * (e // 8) + ["", "▏", "▎", "▍", "▌", "▋", "▊", "▉"][e % 8]


def columns(vals, labels, colw, gap, H, mark):
    """Column chart: a label row on top, H bar rows, a dim baseline, a day-label row."""
    m = max(vals)
    rows = [[] for _ in range(H + 1)]
    for i, v in enumerate(vals):
        h = round(v / m * H * 8)
        for r in range(H + 1):
            if r == 0 or (H - r + 1) * 8 > h and (H - r) * 8 >= h:
                cell = None
            k = H - r  # rows below this one
            if r == 0:
                txt = None
            fill = max(0, min(8, h - (H - r) * 8)) if r > 0 else 0
            if r > 0 and fill:
                ch = "█" if fill == 8 else " ▁▂▃▄▅▆▇"[fill]
                rows[r] += [(ch, "b")] * colw
            else:
                top_row = H - (h + 7) // 8  # row index just above the bar's top
                if i in mark and r == top_row:
                    s = str(v).center(colw)
                    rows[r] += [(c, "t") for c in s]
                else:
                    rows[r] += [(" ", "t")] * colw
            if i < len(vals) - 1:
                rows[r] += [(" ", "t")] * gap
    total = len(vals) * colw + (len(vals) - 1) * gap
    rows.append([("─", "D")] * total)
    lab = []
    for i, l in enumerate(labels):
        st = "B" if i in mark and i == len(vals) - 1 else "d"
        lab += [(c, st) for c in l.center(colw)] + ([(" ", "t")] * gap if i < len(vals) - 1 else [])
    rows.append(lab)
    return rows


def side(L, lw, R, gap=3):
    n = max(len(L), len(R))
    L = L + [[]] * (n - len(L))
    R = R + [[]] * (n - len(R))
    return [pad(a, lw) + [(" ", "t")] * gap + b for a, b in zip(L, R)]



COLOR = {"t": "#ECEAE3", "d": "#A3A198", "a": "#D97757", "g": "#0ca30c", "w": "#fab219", "r": "#d03b3b",
         "b": "#3987e5", "B": "#ECEAE3", "D": "#6E6C66"}
EIGHTHS_H = "▏▎▍▌▋▊▉"
EIGHTHS_V = "▁▂▃▄▅▆▇"
CORNER = {"╭": "left: 50%; top: 50%; border-top: 1px solid {c}; border-left: 1px solid {c}; border-top-left-radius: 5px",
          "╮": "left: 0; top: 50%; border-top: 1px solid {c}; border-right: 1px solid {c}; border-top-right-radius: 5px",
          "╰": "left: 50%; top: 0; border-bottom: 1px solid {c}; border-left: 1px solid {c}; border-bottom-left-radius: 5px",
          "╯": "left: 0; top: 0; border-bottom: 1px solid {c}; border-right: 1px solid {c}; border-bottom-right-radius: 5px"}


def cell(c, st):
    """One terminal cell, exactly 1ch by one line, for a character the web font may not hold at 1ch."""
    col = COLOR[st]
    base = f"display: inline-block; width: 1ch; height: {LH}px; vertical-align: top; position: relative"
    if c == "█":
        return f'<span style="{base}; background: {col}"></span>'
    if c in EIGHTHS_H:
        pct = (EIGHTHS_H.index(c) + 1) * 12.5
        return f'<span style="{base}; background: linear-gradient(to right, {col} {pct}%, transparent {pct}%)"></span>'
    if c in EIGHTHS_V:
        pct = (EIGHTHS_V.index(c) + 1) * 12.5
        return f'<span style="{base}; background: linear-gradient(to top, {col} {pct}%, transparent {pct}%)"></span>'
    if c == "─":
        return f'<span style="{base}; background: linear-gradient({col}, {col}) center / 100% 1px no-repeat"></span>'
    if c == "│":
        return f'<span style="{base}; background: linear-gradient({col}, {col}) center / 1px 100% no-repeat"></span>'
    if c in CORNER:
        inner = "position: absolute; width: 50%; height: 50%; box-sizing: border-box; " + CORNER[c].format(c=col)
        return f'<span style="{base}"><span style="{inner}"></span></span>'
    weight = "; font-weight: 600" if st in ("B", "a") else ""
    return (f'<span style="{base}; color: {col}{weight}; text-align: center; overflow: visible; white-space: pre">'
            f'{html.escape(c)}</span>')


def render(rows, cols, title, sel=()):
    body = []
    for i, r in enumerate(rows):
        spans, cur, buf = [], None, ""
        for c, st in r:
            special = ord(c) > 0x7f and c != "\u00a0"
            if (st != cur or special) and buf:
                spans.append(f'<span style="{STY[cur]}">{html.escape(buf)}</span>')
                buf = ""
            cur = st
            if special:
                spans.append(cell(c, st))
            else:
                buf += c
        if buf:
            spans.append(f'<span style="{STY[cur]}">{html.escape(buf)}</span>')
        bg = "background: #2E2D2A; " if i in sel else ""
        body.append(f'<div style="{bg}height: {LH}px; width: {cols}ch; white-space: pre">{"".join(spans)}</div>')
    w = round(cols * CH + 2 * PAD)
    h = len(rows) * LH + 2 * PAD
    doc = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>{html.escape(title)}</title>
<script src="./support.js"></script>
</head>
<body>
<x-dc>
<helmet>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;600&amp;display=swap">
<style>
body{{margin:0}}
a{{color:#D97757}}a:hover{{color:#E8A68C}}
</style>
</helmet>
<div style="width: {w}px; height: {h}px; box-sizing: border-box; padding: {PAD}px; background: #161615; color: #ECEAE3; font-family: 'JetBrains Mono', ui-monospace, monospace; font-size: 14px; line-height: {LH}px; display: flex; flex-direction: column">
{chr(10).join(body)}
</div>
</x-dc>
<script type="text/x-dc" data-dc-script data-props='{{"$preview":{{"width":{w},"height":{h}}}}}'>
class Component extends DCLogic {{
renderVals() {{
return {{}};
}}
}}
</script>
</body>
</html>
"""
    return doc, w, h


MAST = "«a»D E V - G U A R D«/»"


def refusal(W):
    return lines(
        ("«a»●«/» Edit(src/claude/DevForgeAI/skills/ui/SKILL.md)", 0, 2),
        box([("src/claude/DevForgeAI/skills/ui/SKILL.md is protected, and no ticket permits it in this checkout.", 0, 0),
             "",
             "«d»Remedy«/»",
             ("/plugin-dev:create-plugin <the iteration's scope>", 2, 4),
             ("/plugin-dev:skill-development", 2, 4),
             ("then read each requiredReads file", 2, 4)],
            W, "r", "«r»✕«/» «B»dev-guard«/» · R1 · Edit"),
        "",
        ("«a»●«/» Bash(python3 src/tests/ui/make_evals.py)", 0, 2),
        box([("regenerates src/claude/DevForgeAI/evals/ui/** (make_evals.py)", 0, 0),
             "«d»This ticket doesn't permit plugin writes yet. Missing:«/»",
             ("«w»○«/» /plugin-dev:skill-development not loaded", 2, 4),
             ("«w»○«/» not read in this ticket: docs/research/Claude/skills/skills.md", 2, 4)],
            W, "r", "«r»✕«/» «B»dev-guard«/» · R2 · Bash", "«d»ticket pw-20261102T201500Z«/»"),
        ("«a»●«/» «d»Loading skill-development and reading the guide, then retrying.«/»", 0, 2),
        width=W)


def ticket(W):
    keys = "«d»c close · l log · Esc back«/»"
    return box(["",
                "«w»○«/» «B»Does not permit yet · 2 missing«/»",
                "",
                "«d»ticket«/» pw-20261102T201500Z «d»scope«/» ui v3 cycle C",
                "«d»opened 2026-11-02 20:15 UTC · session 1c98fbaa…«/»",
                "«d»checkout .claude/worktrees/ui-v3 · docs/ui-v3«/»",
                "",
                ("«g»✓«/» create-plugin loaded «d»20:15:03«/»", 0, 2),
                ("«r»✕«/» skill-development not loaded", 0, 2),
                ("«g»✓«/» read Skill-authoring-best-practices.md «d»Read · 20:17:02«/»", 0, 2),
                ("«r»✕«/» read The-Complete-Guide-to-Building-Skill-for-Claude.pdf «B»not yet«/»", 0, 2),
                ("«g»✓«/» read skills/skills.md «d»cat · 20:17:30«/»", 0, 2),
                "rule",
                "«d»reviewers«/» plugin-validator «B»not yet«/» · skill-reviewer «B»not yet«/»",
                "«d»refusals this ticket«/» 2",
                "",
                keys],
               W, "D", MAST)


def close_refused(W):
    return lines(
        "«d»> /dev-guard close«/»",
        box(["",
             "«r»✕«/» «B»Not closed · 4 conditions fail«/»",
             "",
             ("«r»✕«/» origin", 0, 2), ("«d»run from a nested claude -p (sdk); type the command yourself«/»", 2, 2),
             ("«r»✕«/» reviewers", 0, 2), ("«d»skill-reviewer not observed in this ticket«/»", 2, 2),
             ("«r»✕«/» reports", 0, 2), ("«d»no skill-reviewer report in reviews/ with tree 1744e6c…«/»", 2, 2),
             ("«r»✕«/» plugin tree", 0, 2), ("«d»2 files not committed: skills/ui/SKILL.md, skills/ui/references/briefs.md«/»", 2, 2),
             "rule",
             ("«g»✓«/» skill-development loaded", 0, 2),
             ("«g»✓«/» 3 of 3 required files read", 0, 2),
             ("«g»✓«/» plugin-validator observed «d»20:40:12«/»", 0, 2),
             ""],
            W, "D", MAST, "«d»pw-20261102T201500Z«/»"),
        "«d»Fix each line, then type /dev-guard close again. Nothing was written.«/»",
        width=W)


def kv(k, v, lw=11):
    return (f"«d»{k}«/»" + "\u00a0" * (lw - len(k)) + v, 0, lw)


def close_ok(W):
    return lines(
        "«d»> /dev-guard close«/»",
        box(["",
             "«g»✓«/» «B»Closed«/» · pw-20261102T201500Z",
             "«d»ui v3 cycle C · 2026-11-02 20:52:10 UTC«/»",
             "",
             "«d»ledger line«/»",
             kv("tree", "1744e6c3b2…"),
             kv("commit", "26c4cfd8e1…"),
             kv("reports", "20261102T2040Z-plugin-validator-26c4cfd.md"),
             kv("", "20261102T2047Z-skill-reviewer-26c4cfd.md"),
             kv("reviewers", "plugin-validator 20:40 · skill-reviewer 20:47"),
             kv("reads", "3 of 3"),
             kv("closed by", "composer (you typed it)"),
             "",
             "«d»next: the records commit, which runs without a ticket«/»",
             ("git add docs/process/plugin-workflow/ledger.jsonl docs/process/plugin-workflow/reviews/", 0, 2),
             ("git commit -m \"records: close pw-20261102T201500Z\"", 0, 2),
             ""],
            W, "g", MAST),
        "«d»2 refusals in this iteration · l to review«/»",
        width=W)


DAYS = ["T", "W", "T", "F", "S", "S", "M"]
DAYV = [3, 1, 0, 5, 1, 0, 2]   # Tue 27 Oct … Mon 2 Nov (today)


def log(W):
    out = lr(MAST + "«a» · L O G«/»", "«d».claude/worktrees/ui-v3«/»", W)
    out += lines("«d»scope · 1 this ticket ·«/» «B»[2 7 days]«/» «d»· 3 30 days«/»" if W >= 50 else
                 "«d»scope«/» «B»[7 days]«/» «d»· 1 2 3 to change«/»", width=W)
    out.append([])
    tiles = [("refusals 7d", "12"), ("this ticket", "2"), ("candidates", "«w»▲«/» 1"), ("failures", "0")]
    if W >= 76:
        tw = 17
        built = [box([f"«d»{a}«/»", f"«B»{b}«/»" if "▲" not in b else b], tw) for a, b in tiles]
        for i in range(4):
            out.append(sum(([(" ", "t")] + r if j else r for j, r in enumerate(row) ), [])
                       if False else None)
        out = [o for o in out if o is not None]
        for i in range(4):
            line = []
            for j, t in enumerate(built):
                line += ([(" ", "t")] * 2 if j else []) + t[i]
            out.append(line)
    elif W >= 50:
        tw = 24
        built = [box([f"«d»{a}«/»", f"«B»{b}«/»" if "▲" not in b else b], tw) for a, b in tiles]
        for pair in (built[:2], built[2:]):
            for i in range(4):
                out.append(pair[0][i] + [(" ", "t")] * 2 + pair[1][i])
    else:
        out += lines("«B»12«/» «d»refusals 7d ·«/» «B»2«/» «d»this ticket«/»",
                     "«w»▲«/» «B»1«/» «d»candidate ·«/» «B»0«/» «d»guard failures«/»", width=W)
    out.append([])
    cells = 16 if W >= 50 else 12
    rules = [("R2 Bash", 7), ("R1 file", 4), ("R3 commit", 1), ("catch", 0), ("guard.json", 0)]
    lab = 11
    rb = [parse("«d»Refusals by rule«/»")]
    for k, (n, v) in enumerate(rules):
        st = "t" if v else "d"
        if k and rules[k - 1][1]:
            rb.append([])  # a blank line between drawn bars: block rows touch in a terminal (dataviz: a gap between bars)
        rb.append([(c, st) for c in n.ljust(lab)] + [(c, "b") for c in hbar(v, 7, cells).ljust(cells)] +
                  [(" ", "t")] + [(c, st) for c in str(v).rjust(2)])
    colw, gap = (3, 2) if W >= 50 else (2, 1)
    ch = [parse("«d»Refusals per day«/»")] + columns(DAYV, DAYS, colw, gap, 5, {3, 6})
    ch.append(parse("«d»today (M) · 2 · R1 1 · R2 1«/»"))
    if W >= 76:
        out += side(rb, lab + cells + 3, ch, 4)
    else:
        out += rb + [[]] + ch
    out.append([])
    out.append([("─", "D")] * W)
    rows = [("20:31", "R2", "python3 - <<'EOF' … skills/ui/SKILL.md", ""),
            ("20:18", "R1", "Edit skills/ui/references/briefs.md", "«d»subagent«/»"),
            ("Nov 1", "R2", "diff -q src/claude/DevForgeAI …", "«w»▲«/» allowlist?")]
    sel = len(out) + (1 if W >= 50 else 0)
    if W >= 50:
        tagw = 13 if W >= 76 else 0
        out.append(parse("«d»  time   rule  command or path«/»"))
        for k, (t, r, c, tag) in enumerate(rows):
            room = W - 15 - (tagw + 1 if tagw else 0)
            cc = c if len(c) <= room else c[:room - 1] + "…"
            line = parse(("▸ " if k == 0 else "  ") + f"{t}  {r}    ") + parse(cc)
            if tagw:
                line = pad(line, W - tagw) + parse(tag)
            out.append(line)
            if not tagw and tag:
                out.append(parse("               ") + parse(tag))
    else:
        for k, (t, r, c, tag) in enumerate(rows):
            room = W - 11
            cc = c if len(c) <= room else c[:room - 1] + "…"
            out.append(parse(("▸" if k == 0 else " ") + f"{t} {r} ") + parse(cc))
            if tag:
                out.append(parse("         ") + parse(tag))
    out.append([])
    keys = (["«d»↑↓ row · ←→ day · Enter detail · 1 2 3 scope · a candidates · t table · Esc«/»"] if W >= 76 else
            ["«d»↑↓ row · ←→ day · Enter detail · Esc«/»", "«d»1 2 3 scope · a candidates · t table«/»"] if W >= 50 else
            ["«d»↑↓ row · ←→ day · Enter detail«/»", "«d»1 2 3 scope · a candidates«/»", "«d»t table · Esc back«/»"])
    out += lines(*keys, width=W)
    return out, {sel}


def detail(W):
    code = ["python3 - <<'EOF'", "from pathlib import Path", 'p = Path("src/claude/DevForgeAI/skills/ui/SKILL.md")',
            'p.write_text(p.read_text().replace("brief", "briefs"))', "EOF"]
    out = lr(MAST + "«a» · L O G«/»", "«d»20:31 · R2 · Bash«/»", W)
    out.append([])
    out += lines("«d»full command«/»", width=W)
    out += box([(html_safe(c), 0, 2) for c in code], W, "D")
    out.append([])
    out += lines("«d»reason the model read«/»",
                 "R2 (Bash): the script names src/claude/DevForgeAI/skills/ui/SKILL.md; ticket pw-20261102T201500Z "
                 "doesn't permit yet (skill-development not loaded).",
                 "",
                 "«d»ticket pw-20261102T201500Z · session 1c98fbaa… · main conversation«/»",
                 "",
                 *(["«d»y copy command · ↑↓ previous / next · Esc back to the list«/»"] if W >= 76 else
                   ["«d»y copy command · ↑↓ previous / next«/»", "«d»Esc back to the list«/»"]), width=W)
    return out


def html_safe(s):
    return s  # escaping happens in render


SURF = [("Refusal", "The refusal reason (B, titled box)", refusal),
        ("Ticket", "/dev-guard (A, checklist card)", ticket),
        ("CloseRefused", "/dev-guard close, refused (A)", close_refused),
        ("CloseOk", "/dev-guard close, closed (B receipt)", close_ok),
        ("Log", "/dev-guard log (A, dashboard)", log),
        ("LogDetail", "/dev-guard log, Enter on a row (B detail)", detail)]

boards, order, notes = {}, [], {}
y = 4000
for key, name, fn in SURF:
    xs, hmax = 0, 0
    notes[f"g-{key}"] = {"x": 0, "y": y - 280, "text": f"Grid · {name}", "kind": "title1", "maxW": 1760, "page": "grid"}
    for wname, cols in COLS.items():
        res = fn(cols)
        rows, sel = res if isinstance(res, tuple) else (res, ())
        for r in rows:
            assert len(r) <= cols, (key, cols, "".join(c for c, _ in r), len(r))
        fname = f"grid/{key}-{cols}.dc.html"
        doc, w, h = render(rows, cols, f"{name}, {cols} columns", sel)
        (OUT / fname).parent.mkdir(parents=True, exist_ok=True)
        (OUT / fname).write_text(doc)
        boards[fname] = {"x": xs, "y": y, "w": w, "h": h, "title": f"{name} · {cols} cols", "page": "grid"}
        order.append(fname)
        xs += w + 80
        hmax = max(hmax, h)
    y += hmax + 120 + 280
print(json.dumps({"boards": boards, "order": order, "notes": notes}))
