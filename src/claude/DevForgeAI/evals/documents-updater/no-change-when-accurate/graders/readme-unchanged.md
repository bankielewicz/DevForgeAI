---
type: regex
target: {source: file, path: README.md}
match: contains
---
^# wordcount\n\nCounts the words and lines in a text file, for anyone scripting over plain text\.\n\n## Prerequisites\n\n- Python 3\.10 or later\n\n## Install\n\nFrom the repository root:\n\n```bash\npip install \.\n```\n\n## Usage\n\n```bash\nwordcount notes\.txt\n```\n\nPrints `12 words, 3 lines`\.\n\n\| Option \| Effect \|\n\| --- \| --- \|\n\| `--lines` \| Print only the line count \|\n\| `--json` \| Print the counts as a JSON object, for example `\{"words": 12, "lines": 3\}` \|\n$
