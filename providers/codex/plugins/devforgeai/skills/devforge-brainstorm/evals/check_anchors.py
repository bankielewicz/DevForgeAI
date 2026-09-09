"""Read-only eval assertions; not an installed runtime helper or semantic gate."""
import re
from collections import Counter

ID = r"[A-Z][A-Z0-9]*(?:-[A-Z0-9]+)*-[0-9]{3,}"
REQUIRED = (
    "You are here", "Inputs consumed and outputs produced",
    "What changed and what remains open", "Observed verification",
    "Continuation directory", "Copyable next-session prompt", "Resume and custody",
)
TABLES = (
    ("Direction", "Artifact ID/revision", "Store/path", "SHA-256", "Relevant sections", "Decision/freshness state"),
    ("Check", "Outcome", "Raw evidence / external receipt", "Cause or scope limit"),
    ("Order", "Task", "Owner / skill", "Prerequisites", "Completion evidence"),
)

def visible_lines(text):
    """Ignore frontmatter and fenced examples; report actual Markdown headings."""
    frontmatter = text.startswith("---\n"); fence = None
    for number, line in enumerate(text.splitlines(), 1):
        if frontmatter:
            if number > 1 and line.strip() == "---": frontmatter = False
            continue
        match = re.match(r"^ {0,3}(`{3,}|~{3,})", line)
        if match:
            token = match.group(1)
            if fence is None: fence = token
            elif token[0] == fence[0] and len(token) >= len(fence): fence = None
            continue
        if fence is None: yield number, line

def headings(text):
    rows = []; pending = None
    for number, line in visible_lines(text):
        anchor = re.fullmatch(r'\s*<a\s+(?:id|name)=["\'](' + ID + r')["\']\s*>\s*</a>\s*', line)
        if anchor:
            pending = anchor.group(1); continue
        match = re.match(r"^ {0,3}#{2,6}\s+(.+?)\s*#*\s*$", line)
        if match:
            title = match.group(1); found = []
            suffix = re.search(r"\s+\[(" + ID + r")\]$", title)
            prefix = re.match(r"^(" + ID + r")\s+[—–-]\s+", title)
            if suffix: found.append(suffix.group(1)); title = title[:suffix.start()]
            elif prefix: found.append(prefix.group(1)); title = title[prefix.end():]
            if pending: found.append(pending)
            unique = sorted(set(found))
            rows.append({"line": number, "title": title, "id": unique[0] if len(unique)==1 else None,
                         "conflicting_ids": unique if len(unique)>1 else []})
            pending = None
        elif line.strip(): pending = None
    return rows

def check_headings(text, handoff=False):
    rows = headings(text); counts = Counter(row["id"] for row in rows if row["id"])
    missing = [row["line"] for row in rows if not row["id"]]
    duplicate = sorted(value for value,count in counts.items() if count>1)
    titles = {row["title"].casefold() for row in rows}
    absent = [title for title in REQUIRED if title.casefold() not in titles] if handoff else []
    return {"result": "PASS" if rows and not missing and not duplicate and not absent else "FAIL",
            "headings": rows, "missing_id_lines": missing, "duplicate_ids": duplicate,
            "missing_required_sections": absent,
            "scope": "Stable IDs on actual sections, uniqueness and required handoff section titles only"}

def check_template_tables(text):
    """Exact selected template headers; native semantic table review is separate."""
    actual = {tuple(cell.strip() for cell in line.strip().strip('|').split('|'))
              for _,line in visible_lines(text) if line.strip().startswith('|')}
    absent = [list(header) for header in TABLES if header not in actual]
    return {"result": "FAIL" if absent else "PASS", "missing_headers": absent}

def check_source_locators(source, sections, selected_rows, preserved_rows):
    section_ids = {row['id'] for row in headings(source) if row['id']}
    row_ids = set()
    for _,line in visible_lines(source):
        match = re.match(r"^\s*\|\s*("+ID+r")\s*\|",line)
        if match: row_ids.add(match.group(1))
    invalid_sections = [value for value in sections if value not in section_ids]
    nonexistent_rows = [value for value in selected_rows if value not in row_ids]
    missing_rows = [value for value in selected_rows if value not in preserved_rows]
    return {"result": "FAIL" if invalid_sections or nonexistent_rows or missing_rows else "PASS",
            "actual_section_ids": sorted(section_ids), "actual_row_ids": sorted(row_ids),
            "invalid_section_references": invalid_sections, "nonexistent_selected_rows": nonexistent_rows,
            "lost_selected_rows": missing_rows,
            "scope": "Given reference section IDs and separately supplied row locators; does not parse prose or establish adoption"}
