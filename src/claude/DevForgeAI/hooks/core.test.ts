import { expect, test } from 'claude-code/testing'
import {
  bandRows, editResult, eventLine, exitOf, fit, isAnswered, isEngine, isFailed, isPersonPrompt, isTracked,
  keptContent, newFlagToasts, refusalText, relPath, replyText, reportContext, runId, skillName, statusText,
  summaryOf, toolPath, CONTENT_LIMIT, LOG_CONTENT_LIMIT,
} from './progress-core'
import type { ProgressState } from './progress-core'

// Pure helpers of the adapter (SPEC-013): the event line's bytes, the evidence rules, the display text.

const T0 = Date.UTC(2026, 9, 2, 12, 0, 0)
const RUN = '20261002T120000Z-brainstorm-0a1b2c3d'

test('an event line puts run, seq, time and kind first, then the kind fields in DM-02 order', () => {
  const line = eventLine(RUN, 3, T0 + 3000, 'tool', {
    content: 'x', error: false, exit: 0, command: undefined, path: 'docs/a.md', tool: 'Write', extra: 1,
  })
  expect(line).toBe('{"run":"20261002T120000Z-brainstorm-0a1b2c3d","seq":3,"time":"2026-10-02T12:00:03Z",'
    + '"kind":"tool","tool":"Write","path":"docs/a.md","exit":0,"error":false,"content":"x"}')
  expect(eventLine(RUN, 1, T0, 'skill-loaded', {
    modeSource: 'framework-default', mode: 'observe', host: 'claude-code 2.1.287', checklist: 'c', skill: 'brainstorm',
    format: 'devforgeai-events/1',
  })).toBe('{"run":"' + RUN + '","seq":1,"time":"2026-10-02T12:00:00Z","kind":"skill-loaded",'
    + '"format":"devforgeai-events/1","skill":"brainstorm","checklist":"c","host":"claude-code 2.1.287",'
    + '"mode":"observe","modeSource":"framework-default"}')
  expect(eventLine(RUN, 9, T0, 'prompt', { text: 'not a prompt field' })).toBe(
    '{"run":"' + RUN + '","seq":9,"time":"2026-10-02T12:00:00Z","kind":"prompt"}')
  expect(eventLine(RUN, 4, T0, 'tool', { tool: 'Bash', exit: null, error: true })).toContain('"exit":null,"error":true')
})

test('a run ID is the UTC time, the skill and 8 hex digits, matching SPEC-012', () => {
  const id = runId(T0, 'brainstorm', new Uint8Array([10, 27, 44, 61, 99]))
  expect(id).toBe('20261002T120000Z-brainstorm-0a1b2c3d')
  expect(runId(T0, 'My_Skill', new Uint8Array([0, 0, 0, 1]))).toBe('20261002T120000Z-my-skill-00000001')
  expect(/^[0-9]{8}T[0-9]{6}Z-[a-z][a-z0-9-]*-[0-9a-f]{8}$/.test(runId(T0, '9lives', new Uint8Array(4)))).toBe(true)
})

test('skill names lose the plugin prefix, and tracking takes plugin skills and manifest names', () => {
  expect(skillName('devforgeai:brainstorm')).toBe('brainstorm')
  expect(skillName('brainstorm')).toBe('brainstorm')
  expect(isTracked('git', ['brainstorm', 'git'], [])).toBe(true)
  expect(isTracked('release', ['brainstorm'], ['release'])).toBe(true)
  expect(isTracked('plugin-dev', ['brainstorm'], ['release'])).toBe(false)
})

test('paths are relative to the root with / separators; outside the root they stay absolute', () => {
  expect(relPath('/work', '/work/docs/specs/a.md')).toBe('docs/specs/a.md')
  expect(relPath('/work/', '/work/docs')).toBe('docs')
  expect(relPath('/work', '/elsewhere/a.md')).toBe('/elsewhere/a.md')
  expect(relPath('/work', '/work')).toBe('.')
  expect(toolPath('/work', 'Read', { file_path: '/work/docs/specs/prd/PRD-001.md' })).toBe('docs/specs/prd/PRD-001.md')
  expect(toolPath('/work', 'Glob', { pattern: 'BRN-*.md', path: '/work/docs/specs/brainstorm' }))
    .toBe('docs/specs/brainstorm/BRN-*.md')
  expect(toolPath('/work', 'Glob', { pattern: 'docs/**/*.md' })).toBe('docs/**/*.md')
  expect(toolPath('/work', 'Grep', { pattern: 'x', path: '/work/docs/specs/arch/' })).toBe('docs/specs/arch/')
  expect(toolPath('/work', 'Grep', { pattern: 'x' })).toBe('.')
  expect(toolPath('/work', 'Bash', { command: 'ls' })).toBe(undefined)
})

test('a refused or failed call is error true and never ran as asked; exit comes from the text', () => {
  expect(isFailed({ deny: 'refused by a hook' })).toBe(true)
  expect(isFailed({ isError: true, text: 'Exit code 3' })).toBe(true)
  expect(isFailed({ result: 'ok', text: 'ok' })).toBe(false)
  expect(exitOf({ result: 'ok', text: 'ok' })).toBe(0)
  expect(exitOf({ isError: true, result: 'Error: Exit code 3', text: 'Exit code 3' })).toBe(3)
  expect(exitOf({ isError: true, text: 'Permission denied' })).toBe(null)
  expect(exitOf({ deny: 'no' })).toBe(null)
})

test('an AskUserQuestion is answered only when it did not fail and holds an answer', () => {
  expect(isAnswered({ result: { questions: [], answers: { 'Q?': 'Yes' }, annotations: {} } })).toBe(true)
  expect(isAnswered({ result: { questions: [], answers: { 'Q?': 'not sure' } } })).toBe(true)
  expect(isAnswered({ isError: true, result: "Error: The user doesn't want to proceed with this tool use." })).toBe(false)
  expect(isAnswered({ result: { questions: [], answers: {} } })).toBe(false)
  expect(isAnswered({ deny: 'refused' })).toBe(false)
})

test('an Edit leaves the file with one replacement, or all with replace_all; otherwise none', () => {
  expect(editResult('a b a', 'b', 'c', false)).toBe('a c a')
  expect(editResult('a b a', 'a', 'z', true)).toBe('z b z')
  expect(editResult('a b a', 'a', 'z', false)).toBe(null)
  expect(editResult('a b a', 'q', 'z', false)).toBe(null)
  expect(editResult('x'.repeat(CONTENT_LIMIT + 1), 'x', 'y', true)).toBe(null)
})

test('content is kept up to 64 KiB, and not once the log passes 3 MiB', () => {
  expect(keptContent('short', 0)).toBe('short')
  expect(keptContent('x'.repeat(CONTENT_LIMIT + 1), 0)).toBe(undefined)
  expect(keptContent('short', LOG_CONTENT_LIMIT)).toBe(undefined)
  expect(keptContent(null, 0)).toBe(undefined)
})

test('a response row gives its text blocks, and nothing for a tool call or thinking', () => {
  expect(replyText([{ type: 'text', text: '- [x] 1. probe tick' }])).toBe('- [x] 1. probe tick')
  expect(replyText([{ type: 'tool_use', id: 't', name: 'Bash', input: {} }])).toBe('')
  expect(replyText([{ type: 'thinking', thinking: '…' }])).toBe('')
  expect(replyText([{ type: 'text', text: 'a' }, { type: 'text', text: 'b' }])).toBe('a\nb')
  expect(replyText('plain')).toBe('plain')
})

test('prompts count from the person, answers from Claude Code', () => {
  expect(isPersonPrompt({ kind: 'composer' })).toBe(true)
  expect(isPersonPrompt({ kind: 'bridge' })).toBe(true)
  expect(isPersonPrompt({ kind: 'task-notification' })).toBe(false)
  expect(isPersonPrompt({ kind: 'plugin', name: 'x' })).toBe(false)
  expect(isPersonPrompt(undefined)).toBe(false)
  expect(isEngine({ plugin: 'engine', tier: 'core' })).toBe(true)
  expect(isEngine({ plugin: 'other-mod', tier: 'user' })).toBe(false)
})

const STATE: ProgressState = {
  skill: 'brainstorm',
  current: 6,
  ended: null,
  steps: [1, 2, 3, 4, 5, 6, 7, 8].map(n => ({
    n, title: `Step ${n}`,
    state: n < 5 ? 'done' : n === 5 ? 'skipped' : n === 6 ? 'current' : 'pending',
  })),
  flags: [{ gate: 'write', seq: 4, step: 5, type: 'skipped', message: 'step 5 had no answer' }],
  gate: { kind: 'write', seq: 4, refuse: true, reason: 'step 5 had no answer' },
  manifest: { state: 'matched' },
}

test('the status text reads as BEH-10 says', () => {
  const s = summaryOf(STATE)
  expect(statusText(s, 'observe', false, null)).toBe('brainstorm 6/8 · 1 flag')
  expect(statusText({ ...s, flags: 2 }, 'enforce', false, null)).toBe('brainstorm 6/8 · 2 flags · enforce')
  expect(statusText({ ...s, flags: 0, yourTurn: true, skill: 'architecture', current: 7, steps: 11 }, 'observe', false, null))
    .toBe('architecture 7/11 · your turn')
  expect(statusText({ ...s, current: null, flags: 0 }, 'observe', false, null)).toBe('brainstorm done')
  expect(statusText({ ...s, ended: 'clear', flags: 0 }, 'observe', true, null)).toBe('brainstorm ended')
  expect(statusText({ ...s, flags: 0, manifest: 'none', skill: 'git' }, 'observe', true, null)).toBe('git 6/8 · ticks only · idle')
  expect(statusText(s, 'observe', false, 'python not found')).toBe('progress: off (python not found)')
  expect(statusText(null, 'observe', false, null)).toBe(undefined)
})

test('the band rows carry the glyphs, the step, the mode and its button, and the newest flag', () => {
  const rows = bandRows(summaryOf(STATE), 'observe')
  expect(rows.row1).toBe('brainstorm  ●●●●✗◆○○  step 6 of 8: Step 6')
  expect(rows.mode).toBe('observe mode')
  expect(rows.button).toBe('Switch to enforce')
  expect(rows.flag).toBe('step 5 had no answer')
  expect(bandRows(summaryOf(STATE), 'enforce').button).toBe('Switch to observe')
  expect(fit('abcdef', 4)).toBe('abc…')
  expect(fit('abc', 4)).toBe('abc')
})

test('flags are toasted once, refused at the write gate, and given to the model at the report gate', () => {
  const first = newFlagToasts(STATE, [])
  expect(first.toasts).toEqual(['✗ Step 5 skipped: step 5 had no answer'])
  expect(newFlagToasts(STATE, first.keys).toasts).toEqual([])
  const refusal = refusalText(STATE, 4)
  expect(refusal === null ? '' : refusal).toContain('- step 5 had no answer')
  expect(refusalText(STATE, 5)).toBe(null)
  expect(refusalText({ ...STATE, gate: { ...STATE.gate, refuse: false } }, 4)).toBe(null)
  expect(reportContext(STATE)).toBe(null)
  const report = reportContext({ ...STATE, gate: { kind: 'report', seq: 4, refuse: true, reason: 'x' } })
  expect(report === null ? -1 : report.seq).toBe(4)
})
