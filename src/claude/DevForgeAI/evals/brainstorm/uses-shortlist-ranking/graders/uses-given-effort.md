---
type: regex
target: {source: file, path: docs/specs/brainstorm/BRN-001.md}
match: contains
---
idea: "[^"\n]*(?:[Ss]ingle sign-on|SSO|SAML)[^\n]*\n(?:(?![ \t]*- id:)[^\n]*\n)*?[ \t]+effort: "6"
