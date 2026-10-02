---
type: regex
target: {source: file, path: docs/specs/arch/ARCH-001.md}
match: contains
flags: m
---
^\|(?=[^\n]*DEC-01)(?=[^\n]*POL-001#SET-01)(?=[^\n]*Org A Identity Platform \(OIDC\))(?=[^\n]*Org A Identity Cloud \(SAML\))[^\n]*\|[ \t]*$
