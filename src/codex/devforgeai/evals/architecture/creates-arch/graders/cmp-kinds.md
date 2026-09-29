---
type: regex
target: {source: file, path: docs/specs/arch/ARCH-001.md}
match: contains
flags: m
---
\A(?![\s\S]*^    kinds:(?![ \t]*\r?\n(?:      - "(?:user-interface|service|platform|api|relational-store|data-store|external)"[ \t]*\r?\n)+(?!      - )))[\s\S]*(?:^    kinds:[ \t]*\r?\n      - "(?:user-interface|service|platform|api|relational-store|data-store|external)"[ \t]*\r?$|\[NEEDS CLARIFICATION: kinds of CMP-\d{2}\])
