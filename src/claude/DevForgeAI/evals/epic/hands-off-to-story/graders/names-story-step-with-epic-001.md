---
type: regex
target: last_message
flags: i
pattern: '(?:\bstory step\b|/devforgeai:story\b|\bstories\b[^\n]{0,80}\bby hand\b)[\s\S]{0,300}?\bEPIC-001\b|\bEPIC-001\b[\s\S]{0,300}?(?:\bstory step\b|/devforgeai:story\b|\bstories\b[^\n]{0,80}\bby hand\b)'
---
