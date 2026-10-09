import { expect, test } from 'claude-code/testing'
import {
  adherenceText, bandRows, editResult, eventLine, finalTimeout, exitOf, fit, followsTaskList, hasTaskList, isAnswered,
  isEngine, isFailed, isPersonPrompt, isTracked, keptContent, newFlagToasts, questionRefusal, refusalText, relPath,
  refusalCause, replyText, reportContext, retentionOf, runId, skillName, statusText, stepOfTask, stepStateOf, stuckAdvice,
  stuckText, summaryOf, taskIdOf, returnLine, trailNote, pausedWith, keptTrail, endReason, hasRoom, nestedExitQuestion, nestedKeptText,
  runName, resumePlan, ageText, resumeQuestion, isUntrackedSkill, removeArgv, resumesOf, workFilePaths, workFilesDue, workFilesProblem,
  todoSteps, toolPath, CONTENT_LIMIT, LOG_CONTENT_LIMIT, QUESTION_REFUSAL, QUESTION_TAG,
  formOf, formsText, draftCandidate, gatedOf, fnmatchcase, pathMatches, ruleMatches, scriptWord, runsScript, commandParts, pathToken,
  outsideWord, outsideRefusal, outsideMessage, folderOf, folderOfFile, changedFiles, logNames, windowClosed, wroteText, withContext,
  OUTSIDE_ADVICE,
  isFromMod, fuelSetting, measuredShare, precompactRow, precompactDue, NO_PRECOMPACT, usageFields, ledgerLine, progressReport,
  addStart, takeStart, isCompaction, isOwnRun,
  HOLD_TRIES, RETRYING, STOPPED_LINE, NOTHING_TO_RETRY, STOP_TOAST, errorLine, remedyRow, heldToast, recoveredToast, heldLog, recoveredLog,
  gaveUpLog, savedAnswer, stillAnswer, liftedAnswer, stillStoppedAnswer, odometerOnAnswer, odometerStillAnswer, odometerGaveUpToast,
  logLevelOf, rolloverMiBOf, logStamp, traceCut, rollReason, chunkLines, mergeByTime, logCommand, TRACE_LIMIT, EARLY_LIMIT, TRACE_CUT,
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

test('the final evaluation at session end uses what the budget leaves, or none', () => {
  expect(finalTimeout(1500)).toBe(1200)
  expect(finalTimeout(600)).toBe(300)
  expect(finalTimeout(450)).toBe(null)
  expect(finalTimeout(0)).toBe(null)
})

test('the retention period is 7 to 3650 days, and 30 otherwise (DM-06)', () => {
  expect([7, 30, 3650].map(retentionOf)).toEqual([7, 30, 3650])
  expect([2, 0, -7, 3651, 7.5, undefined, null, 'soon'].map(retentionOf)).toEqual([30, 30, 30, 30, 30, 30, 30, 30])
})

test('the refusal names what clears each flag, and the decision line only for decision flags', () => {
  const stepOnly = refusalText({ ...STATE, run: 'r1', gate: { kind: 'write', seq: 4, refuse: true, reason: 'x' },
    flags: [{ gate: 'write', seq: 4, step: 1, type: 'skipped', message: 'step 1 has no evidence or tick' }] }, 4) ?? ''
  expect(stepOnly).toContain('To clear step 1:')
  expect(stepOnly).toContain("A tick only in your thinking doesn't count.")
  expect(stepOnly.includes("are the user's")).toBe(false)
  expect(stepOnly).toContain('devforgeai/progress/runs/r1/')
  const owned = { ...STATE, steps: STATE.steps.map(s => (s.n === 5 ? { ...s, userOwned: true } : s)) }
  const decision = refusalText({ ...owned, gate: { kind: 'write', seq: 4, refuse: true, reason: 'x' },
    flags: [
      { gate: 'write', seq: 4, step: 5, type: 'skipped', message: 'step 5 had no answer from you' },
      { gate: 'write', seq: 4, step: 6, type: 'rule-broken', message: 'BRN-002.md sets disposition: promoted' },
    ] }, 4) ?? ''
  expect(decision).toContain("The decisions at step 5, 6 are the user's: ask the user, or leave those fields open.")
  expect(decision.includes('To clear step')).toBe(false)
})

// ---- the task list (SPEC-013 v4 and v5) ----

test('the task list: which sessions have one, which runs follow it, and how tasks map to steps', () => {
  expect(hasTaskList(['Read', 'TaskCreate', 'TaskUpdate'])).toBe(true)
  expect(hasTaskList(['TodoWrite'])).toBe(true)
  expect(hasTaskList(['TaskCreate'])).toBe(false)
  expect(hasTaskList(['TaskStop', 'ToolSearch'])).toBe(false)
  const loaded = (taskList: unknown, checklist: string) => JSON.stringify({ kind: 'skill-loaded', taskList, checklist })
  expect(followsTaskList(loaded(true, '- [ ] 1. A\nmetadata devforgeai_step: N'))).toBe(true)
  expect(followsTaskList(loaded(false, 'devforgeai_step'))).toBe(false)
  expect(followsTaskList(loaded(true, '- [ ] 1. A'))).toBe(false)
  expect(followsTaskList('not json')).toBe(false)
  expect(taskIdOf('Task #12 created successfully: 3. Evaluate')).toBe('12')
  expect(taskIdOf('Created.')).toBe(null)
  expect(stepOfTask({ subject: 'Anything', metadata: { devforgeai_step: 4 } })).toBe(4)
  expect(stepOfTask({ subject: '7. Resolve', metadata: { devforgeai_step: 2.5 } })).toBe(7)
  expect(stepOfTask({ subject: 'Tidy up' })).toBe(null)
  expect(stepOfTask({ subject: '0. Nothing' })).toBe(null)
  expect([stepStateOf('in_progress'), stepStateOf('completed'), stepStateOf('pending'), stepStateOf('deleted')])
    .toEqual(['started', 'done', null, null])
  const first = todoSteps([
    { content: '1. A', status: 'completed' }, { content: '2. B', status: 'in_progress' },
    { content: 'Notes', status: 'in_progress' }, { content: '3. C', status: 'pending' },
  ], {})
  expect(first.events).toEqual([{ step: 1, state: 'done' }, { step: 2, state: 'started' }])
  const second = todoSteps([{ content: '2. B', status: 'completed' }, { content: '3. C', status: 'in_progress' }], first.statuses)
  expect(second.events).toEqual([{ step: 2, state: 'done' }, { step: 3, state: 'started' }])
  expect(second.statuses).toEqual({ 1: 'completed', 2: 'completed', 3: 'in_progress' })
  // Version 6: the list the call replaced decides, so a todo already completed there claims nothing.
  const replaced = todoSteps([{ content: '2. B', status: 'completed' }, { content: '4. D', status: 'in_progress' }], {},
    [{ content: '2. B', status: 'completed' }, { content: '4. D', status: 'pending' }])
  expect(replaced.events).toEqual([{ step: 4, state: 'started' }])
  // Review: an earlier run's completed todos kept in the list, the new run's appended with the same numbers.
  const earlier = [{ content: '1. A', status: 'completed' }, { content: '2. B', status: 'completed' }]
  const appended = todoSteps([...earlier, { content: '1. A', status: 'in_progress' }, { content: '2. B', status: 'pending' }],
    {}, [...earlier, { content: '1. A', status: 'pending' }, { content: '2. B', status: 'pending' }])
  expect(appended.events).toEqual([{ step: 1, state: 'started' }])
})

test('the question gate refuses at its own seq; the adherence notice needs a report or an end, and the counts', () => {
  const question = { ...STATE, gate: { kind: 'question', seq: 9, refuse: true, reason: 'x' } }
  expect(questionRefusal(question, 9)).toBe(QUESTION_REFUSAL + QUESTION_TAG)
  expect(questionRefusal(question, 9, null, true)).toBe(QUESTION_REFUSAL)  // a tagged question isn't told to tag it
  expect(questionRefusal(question, 8)).toBe(null)
  expect(questionRefusal({ ...question, gate: { ...question.gate, refuse: false } }, 9)).toBe(null)
  expect(questionRefusal(STATE, 4)).toBe(null)
  const report = { ...STATE, gate: { kind: 'report', seq: 9, refuse: false, reason: null } }
  expect(adherenceText({ ...report, counts: { stepEvents: 5, unmarkedQuestions: 1 } }))
    .toBe("brainstorm didn't keep its task list: 5 step events, 1 questions asked without their step marked and tagged. "
      + 'Recommended: fix the skill so it keeps its checklist in the task list (DevForgeAI SPEC-012 §4)')
  expect(adherenceText({ ...report, counts: { stepEvents: 5, unmarkedQuestions: 0 } })).toBe(null)
  expect(adherenceText({ ...STATE, counts: { stepEvents: 0, unmarkedQuestions: 0 } })).toBe(null)
  expect(adherenceText({ ...STATE, ended: 'session-end', counts: { stepEvents: 0, unmarkedQuestions: 0 } })).not.toBe(null)
  expect(adherenceText({ ...STATE, ended: 'session-end' })).toBe(null)
  // The report reached, though a later write moved the gate on before the timer evaluated.
  const reported = { ...STATE, steps: STATE.steps.map(s => (s.n === 8 ? { ...s, kind: 'report', state: 'done' } : s)),
    counts: { stepEvents: 0, unmarkedQuestions: 0 } }
  expect(adherenceText(reported)).not.toBe(null)
})

// SPEC-013 v9 (BEH-25): the stuck notice's last sentence follows the refused flag's type and whether its step is
// user-owned, never its message text.
const TASK_ADVICE = "Help Claude bring its task list in step, or switch to observe mode with the band's button."
const EVIDENCE_ADVICE = "Claude hasn't done that step in a way the tracker can see: ask Claude to do it as the message "
  + "says, or switch to observe mode with the band's button."
const DECISION_ADVICE = "The refused write records a decision that needs your answer: answer Claude's question about it, "
  + "or ask Claude to leave it open, or switch to observe mode with the band's button."

test("the stuck notice's advice follows the refused flag's type and whether its step is user-owned (version 9)", () => {
  for (const type of ['unmarked-question', 'untagged-question', 'mismatched-question']) {
    expect(stuckAdvice(type, false)).toBe(TASK_ADVICE)
    expect(stuckAdvice(type, true)).toBe(TASK_ADVICE)
  }
  expect(stuckAdvice('skipped', false)).toBe(EVIDENCE_ADVICE)
  expect(stuckAdvice('claimed-not-evidenced', false)).toBe(EVIDENCE_ADVICE)
  expect(stuckAdvice('skipped', true)).toBe(DECISION_ADVICE)
  expect(stuckAdvice('rule-broken', false)).toBe(DECISION_ADVICE)
  expect(stuckAdvice('rule-broken', true)).toBe(DECISION_ADVICE)
  // The cause reads userOwned from the state's steps; a step the state doesn't list isn't user-owned.
  const owned = { ...STATE, gate: { kind: 'write', seq: 7, refuse: true, reason: 'x' },
    steps: STATE.steps.map(s => (s.n === 5 ? { ...s, userOwned: true } : s)),
    flags: [{ gate: 'write', seq: 7, step: 5, type: 'skipped', message: 'm5' },
      { gate: 'write', seq: 7, step: 6, type: 'rule-broken', message: 'm6' }] }
  expect(refusalCause(owned, 7)).toEqual({ key: 'write:skipped:5', step: 5, message: 'm5', type: 'skipped', userOwned: true })
  const unlisted = { ...owned, flags: [{ gate: 'write', seq: 7, step: 40, type: 'skipped', message: 'm40' }] }
  expect(refusalCause(unlisted, 7)?.userOwned).toBe(false)
  expect(stuckText('brainstorm', 5, 'm5', DECISION_ADVICE))
    .toBe(`brainstorm: the progress tracker refused Claude twice at step 5 for the same reason: m5. ${DECISION_ADVICE}`)
})

// VER-38 (SPEC-013 v12): after run-end stopped, the status line and the band say where the run stopped.
test('VER-38: a stopped run reads stopped at step n in the status line and the band', () => {
  const steps = Array.from({ length: 11 }, (_, i) => ({ n: i + 1, title: `Step ${i + 1}`, state: i < 8 ? 'done' : 'pending' }))
  const state = { skill: 'architecture', current: 8, ended: 'stopped', steps, flags: [],
    gate: { kind: null, seq: null, refuse: false, reason: null }, manifest: { state: 'matched' as const } }
  const summary = summaryOf(state)
  expect(statusText(summary, 'enforce', false, null)).toBe('architecture stopped at step 8 · enforce')
  expect(bandRows(summary, 'observe').row1.endsWith('  stopped at step 8')).toBe(true)
  const ended = summaryOf({ ...state, ended: 'clear' })
  expect(statusText(ended, 'observe', false, null)).toBe('architecture ended')
})

// VER-43 and VER-44 (SPEC-013 v14; version 13's VER-41 replaced): the trail's texts, which paused run a TaskUpdate
// names, the trail kept at a load, a log's run-end reason, the nested display and exit texts.
test('VER-43: the return line asks to re-mark the step; the trail note names the whole trail, top first', () => {
  expect(returnLine('architecture', 7)).toBe("This skill was loaded by architecture at step 7. When this skill's work is done, mark architecture's step 7 task in progress again and continue architecture at step 7.")
  const trail = [{ skill: 'brainstorm', step: 4, tasks: { '1': 1, '4': 4 } }, { skill: 'architecture', step: 7, tasks: { '7': 7, '8': 8 } }]
  expect(trailNote('spec-lookup', trail)).toBe('Return points (from the progress tracker): when spec-lookup is done, continue architecture at step 7; then brainstorm at step 4.')
})

test('VER-44: a TaskUpdate names the topmost paused run holding its task ID, whatever its status', () => {
  const trail = [{ skill: 'brainstorm', step: 4, tasks: { '1': 1, '4': 4, '7': 7 } }, { skill: 'architecture', step: 7, tasks: { '7': 7, '8': 8 } }]
  expect(pausedWith(trail, '7')).toBe(1)
  expect(pausedWith(trail, '8')).toBe(1)
  expect(pausedWith(trail, '1')).toBe(0)
  expect(pausedWith(trail, '99')).toBe(-1)
  expect(pausedWith(trail, 7)).toBe(-1)
  expect(pausedWith([], '7')).toBe(-1)
})

test('VER-43: a trail read back after a load keeps only entries with their run (version 13 entries are dropped)', () => {
  const run = { id: 'r1', skill: 'architecture', seq: 9, dir: '/d', root: '/w' }
  const full = { skill: 'architecture', step: 7, tasks: { '7': 7 }, run, summary: null, marked: false, shown: [], contextSent: [],
    todos: {}, adhered: null, refusals: {}, refused: [], reviewed: null }
  expect(keptTrail([{ skill: 'brainstorm', step: 4, tasks: {} }, full])).toEqual([full])
  expect(keptTrail(null)).toEqual([])
  expect(keptTrail([{ ...full, step: '7' }, { ...full, run: null }])).toEqual([])
})

test('VER-44: a log\'s run-end reason; a session end\'s room for one more run-end', () => {
  const line = (kind: string, fields = {}) => JSON.stringify({ kind, ...fields })
  expect(endReason([line('skill-loaded'), line('tool'), line('run-end', { reason: 'stopped' }), line('turn')])).toBe('stopped')
  expect(endReason([line('skill-loaded')])).toBe(null)
  expect(hasRoom(1500)).toBe(true)
  expect(hasRoom(299)).toBe(false)
})

test('VER-43: the status line and the band name the run just beneath, and count the rest', () => {
  const steps = Array.from({ length: 5 }, (_, i) => ({ n: i + 1, title: `Step ${i + 1}`, state: i < 1 ? 'done' : i === 1 ? 'current' : 'pending' }))
  const s = summaryOf({ skill: 'spec-lookup', current: 2, ended: null, steps, flags: [],
    gate: { kind: null, seq: null, refuse: false, reason: null }, manifest: { state: 'matched' as const } })
  const arch = { skill: 'architecture', step: 7, summary: { steps: 11 } }
  const brn = { skill: 'brainstorm', step: 4, summary: null }
  expect(statusText(s, 'observe', false, null, [arch])).toBe('spec-lookup 2/5 · in architecture 7/11')
  expect(statusText(s, 'enforce', false, null, [brn, arch])).toBe('spec-lookup 2/5 · in architecture 7/11 · 1 more · enforce')
  expect(statusText(s, 'observe', false, null, [brn])).toBe('spec-lookup 2/5 · in brainstorm 4')
  expect(statusText(s, 'observe', false, null, [])).toBe('spec-lookup 2/5')
  expect(bandRows(s, 'observe', [arch]).row1.endsWith(' (paused: architecture at step 7)')).toBe(true)
  expect(bandRows(s, 'observe', [brn, arch]).row1.endsWith(' (paused: architecture at step 7, 1 more)')).toBe(true)
  expect(bandRows(s, 'observe').row1.endsWith('step 2 of 5: Step 2')).toBe(true)
})

test('VER-44: the exit question and the kept text while a run is paused beneath the open one', () => {
  const b = { skill: 'architecture', step: 7 }
  const at = { current: 2, steps: 5, ended: null }
  expect(nestedExitQuestion('spec-lookup', at, b, 0, 'Clear')).toBe('spec-lookup run is at step 2 of 5 and unfinished (architecture paused at step 7). Clear anyway?')
  expect(nestedExitQuestion('spec-lookup', { ...at, current: null }, b, 1, 'Exit')).toBe('spec-lookup run is done (architecture paused at step 7, 1 more paused). Exit anyway?')
  expect(nestedExitQuestion('spec-lookup', null, b, 0, 'Resume')).toBe('spec-lookup run has just started (architecture paused at step 7). Resume anyway?')
  expect(nestedKeptText('spec-lookup', b)).toBe('Kept working: the spec-lookup run goes on, and architecture is still paused at step 7.')
})

// ---- the offer to continue an earlier run (SPEC-013 v16), after the build reviews: states as the evaluator writes them ----

/** A brainstorm state as evaluate.py writes it: each step's state and evidence types, its claim, and how the run ended. */
function brnState(steps: Array<[string, string[], string | null]>, ended: string | null = 'session-end'): ProgressState {
  const titles = ['Intake', 'Framework', 'Diverge', 'Evaluate', 'Dispositions', 'Write the BRN', 'Validate', 'Report']
  return { skill: 'brainstorm', current: null, ended, flags: [], gate: { kind: null, seq: null, refuse: false, reason: null },
    manifest: { state: 'matched' },
    steps: steps.map(([state, types, claim], i) => ({ n: i + 1, title: titles[i], state, userOwned: i + 1 === 5,
      evidence: types.map(type => ({ type })), claim: claim === null ? null : { state: claim } })) } as unknown as ProgressState
}
const line = (o: object) => JSON.stringify({ run: 'x', seq: 1, time: '2026-10-05T10:00:00Z', ...o })

test('VER-47 (review S1): a resumed run resumed again keeps its carried write step written and its answered decisions', () => {
  // Run B continued run A at step 7 (A had answered step 5 and written the BRN): B's steps 1 to 6 are carried, step 5
  // answered in A; B marked step 7 and ended.
  const b = brnState([['carried', ['carried'], 'done'], ['carried', ['carried'], 'done'], ['carried', ['carried'], 'done'],
    ['carried', ['carried'], 'done'], ['carried', ['carried'], 'done'], ['carried', ['carried'], 'done'],
    ['pending', [], null], ['pending', [], null]])
  const lines = [line({ kind: 'skill-loaded', resumes: 'A', carried: [1, 2, 3, 4, 5, 6], answered: [5] }),
    line({ seq: 2, kind: 'step', step: 7, state: 'started' }), line({ seq: 3, kind: 'run-end', reason: 'session-end' })]
  const plan = resumePlan('B', b, lines, 6, Date.parse('2026-10-05T12:00:00Z'))
  expect(plan).toMatchObject({ step: 7, carried: [1, 2, 3, 4, 5, 6], answered: [5], owned: [] })
})

test('VER-47 (review S2): a decision written before the user\'s answer is no answer that stands', () => {
  // The BRN was written with dispositions promoted before step 5 was answered (step 5 skipped, step 6 rule-broken); the
  // user answered step 5 afterwards; the run ended marked at step 7.
  const a = brnState([['done', ['read'], 'done'], ['done', [], 'done'], ['done', [], 'done'], ['done', [], 'done'],
    ['skipped', ['answer'], 'done'], ['rule-broken', ['write'], 'done'], ['pending', [], null], ['pending', [], null]])
  const lines = [line({ kind: 'skill-loaded' }), line({ seq: 2, kind: 'step', step: 7, state: 'started' }),
    line({ seq: 3, kind: 'run-end', reason: 'session-end' })]
  const plan = resumePlan('A', a, lines, 6, Date.parse('2026-10-05T12:00:00Z'))
  expect(plan).toMatchObject({ step: 7, answered: [], owned: [5] })
})

test('VER-47 (review S3): the offer looks for runs under the name run IDs give the skill', () => {
  expect(runName('My_Skill')).toBe('my-skill')
  expect(runName('9lives')).toBe('lives')
  expect(runName('brainstorm')).toBe('brainstorm')
  expect(runId(T0, 'My_Skill', new Uint8Array([0, 0, 0, 1]))).toBe(`20261002T120000Z-${runName('My_Skill')}-00000001`)
})

test('BEH-31 (review notes): an unknown age and a path with a line break don\'t break the question', () => {
  expect(ageText(NaN)).toBe('an unknown time')
  const a = brnState([['done', ['read'], 'done'], ['pending', [], null], ['pending', [], null], ['pending', [], null],
    ['pending', [], null], ['pending', [], null], ['pending', [], null], ['pending', [], null]])
  const lines = [line({ kind: 'skill-loaded' }), line({ seq: 2, kind: 'tool', tool: 'Write', path: 'docs/a\nb.md', error: false }),
    line({ seq: 3, kind: 'run-end', reason: 'session-end' })]
  const plan = resumePlan('A', a, lines, 6, Date.parse('2026-10-05T12:00:00Z'))!
  expect(resumeQuestion('brainstorm', plan)).toBe('brainstorm: an earlier run ended at step 2 of 8 on 2026-10-05 (session end). It wrote docs/a b.md. Continue it?')
})

// ---- version 18: the key that makes a plugin skill untracked (BEH-02, VER-50 (f)) ----

/** A SKILL.md: frontmatter with `meta` lines after its name and description, then a body. */
const skillMd = (meta: string, body = '# precompact\n') => `---\nname: precompact\ndescription: Writes the handoff.\n${meta}---\n\n${body}`
const OFF = '  devforgeai-tracked: "false"\n'

test('VER-50 (f): the key devforgeai-tracked "false" in the metadata block marks a skill untracked', () => {
  expect(isUntrackedSkill(skillMd(`metadata:\n${OFF}`))).toBe(true)
  expect(isUntrackedSkill(skillMd('metadata:\n  author: devforgeai\n' + OFF + '  version: "1"\n'))).toBe(true)
  // any depth of indentation: the block is the lines that start with a space
  expect(isUntrackedSkill(skillMd('metadata:\n        devforgeai-tracked: "false"\n'))).toBe(true)
})

test('VER-50 (f): single quotes, spaces around the line, a trailing comment and CRLF line ends all read the same', () => {
  expect(isUntrackedSkill(skillMd("metadata:\n  devforgeai-tracked: 'false'\n"))).toBe(true)
  expect(isUntrackedSkill(skillMd('metadata:\n    devforgeai-tracked: "false"    \n'))).toBe(true)
  expect(isUntrackedSkill(skillMd('metadata:\n  devforgeai-tracked:   "false"\n'))).toBe(true)
  expect(isUntrackedSkill(skillMd('metadata:\n  devforgeai-tracked: "false" # the tracker ignores it\n'))).toBe(true)
  expect(isUntrackedSkill(skillMd("metadata:\n  devforgeai-tracked: 'false'   #x\n"))).toBe(true)
  expect(isUntrackedSkill(skillMd(`metadata:\n${OFF}`).replace(/\n/g, '\r\n'))).toBe(true)
  expect(isUntrackedSkill(skillMd("metadata:\n  devforgeai-tracked: 'false'\n").replace(/\n/g, '\r\n'))).toBe(true)
  // a CRLF file's `metadata:` line and closing --- carry the CR too
  expect(isUntrackedSkill('---\r\nname: p\r\nmetadata:\r\n  devforgeai-tracked: "false"\r\n---\r\n')).toBe(true)
})

test('VER-50 (f): false unquoted, "False", other values and a quote mismatch leave the skill tracked', () => {
  for (const value of ['false', '"False"', '"FALSE"', "'False'", '"true"', '"no"', '""', '"false" x', '"false\'', '\'false"', '"fals"',
    'false # x', '"false"#x', '0', '~', '']) {
    expect(isUntrackedSkill(skillMd(`metadata:\n  devforgeai-tracked: ${value}\n`))).toBe(false)
  }
  expect(isUntrackedSkill(skillMd('metadata:\n  devforgeai-tracked:"false"\n'))).toBe(false)
})

test('VER-50 (f): the key outside the metadata block, with no metadata block or in the body leaves the skill tracked', () => {
  // at the frontmatter's top level
  expect(isUntrackedSkill(skillMd('devforgeai-tracked: "false"\n'))).toBe(false)
  expect(isUntrackedSkill(skillMd('devforgeai-tracked: "false"\nmetadata:\n  author: x\n'))).toBe(false)
  // after the block ended
  expect(isUntrackedSkill(skillMd('metadata:\n  author: x\ndevforgeai-tracked: "false"\n'))).toBe(false)
  // under another key, and under an indented metadata line
  expect(isUntrackedSkill(skillMd('license: MIT\n  devforgeai-tracked: "false"\n'))).toBe(false)
  expect(isUntrackedSkill(skillMd('  metadata:\n    devforgeai-tracked: "false"\n'))).toBe(false)
  // no key, no metadata, an empty file
  expect(isUntrackedSkill(skillMd('metadata:\n  author: x\n'))).toBe(false)
  expect(isUntrackedSkill(skillMd('metadata:\n'))).toBe(false)
  expect(isUntrackedSkill(skillMd(''))).toBe(false)
  expect(isUntrackedSkill('')).toBe(false)
  // another key's name
  expect(isUntrackedSkill(skillMd('metadata:\n  devforgeai-tracked-by: "false"\n'))).toBe(false)
  expect(isUntrackedSkill(skillMd('metadata:\n  devforgeai_tracked: "false"\n'))).toBe(false)
  expect(isUntrackedSkill(skillMd('metadata:\n  Devforgeai-tracked: "false"\n'))).toBe(false)
  // in the body, after the frontmatter's closing line
  expect(isUntrackedSkill(skillMd('', 'metadata:\n  devforgeai-tracked: "false"\n'))).toBe(false)
})

test('VER-50 (f): the frontmatter is the text between the first line --- and the next line ---', () => {
  // no frontmatter at all, or none that is closed
  expect(isUntrackedSkill('metadata:\n  devforgeai-tracked: "false"\n')).toBe(false)
  expect(isUntrackedSkill('---\nname: p\nmetadata:\n  devforgeai-tracked: "false"\n')).toBe(false)
  // the first line isn't the opener
  expect(isUntrackedSkill('\n---\nname: p\nmetadata:\n  devforgeai-tracked: "false"\n---\n')).toBe(false)
  // a block that runs to the closing line, and a closing line right after the key
  expect(isUntrackedSkill('---\nmetadata:\n  devforgeai-tracked: "false"\n---\nbody\n')).toBe(true)
  // the block ends at the first line that doesn't start with a space (a blank line included)
  expect(isUntrackedSkill(skillMd('metadata:\n  author: x\n\n' + OFF))).toBe(false)
  // the closing --- ends it: a key after a second --- is the body's
  expect(isUntrackedSkill('---\nname: p\nmetadata:\n  author: x\n---\n  devforgeai-tracked: "false"\n')).toBe(false)
})

// ---- SPEC-013 v20: the work files' cleanup (BEH-32, IF-05) ----

test('VER-52: workFilesDue is true only for workFiles.due true', () => {
  const st = (workFiles: unknown) => ({ workFiles } as unknown as ProgressState)
  expect(workFilesDue(st({ due: true, files: [] }))).toBe(true)
  for (const w of [{ due: false, files: ['a'] }, { files: ['a'] }, { due: 'true' }, { due: 1 }, null, [], 'x', undefined]) {
    expect(workFilesDue(st(w))).toBe(false)
  }
})

test('VER-52: workFilePaths keeps the non-empty strings, in order, and nothing from a state that isn\'t shaped so', () => {
  expect(workFilePaths({ workFiles: { files: ['a', 'b', '--root', 7, '', null, {}, ['c'], 'a'] } })).toEqual(['a', 'b', '--root', 'a'])
  for (const bad of [null, [], 'x', 3, {}, { workFiles: null }, { workFiles: [] }, { workFiles: 'x' }, { workFiles: {} }, { workFiles: { files: 'a' } }]) {
    expect(workFilePaths(bad)).toEqual([])
  }
})

test('VER-52 / ERR-19: workFilesProblem says why a state names no workFiles object', () => {
  expect(workFilesProblem({ workFiles: { files: [], due: false } })).toBeNull()
  expect(workFilesProblem([])).not.toBeNull()
  expect(workFilesProblem(null)).not.toBeNull()
  expect(workFilesProblem({})).not.toBeNull()
  expect(workFilesProblem({ workFiles: [] })).not.toBeNull()
  expect(workFilesProblem({ workFiles: 'x' })).not.toBeNull()
})

test('VER-52: removeArgv gives one --file=<path> token per path, once each, in order, across the lists', () => {
  expect(removeArgv('python3', '/p', '/r', ['a', 'b'], ['b', 'c'], ['-x', '', 'a'])).toEqual(
    ['python3', '/p/progress/prune.py', 'remove', '--root', '/r', '--manifests', '/p/progress/manifests', '--file=a', '--file=b', '--file=c', '--file=-x'])
  expect(removeArgv('python3', '/p', '/r')).toEqual(['python3', '/p/progress/prune.py', 'remove', '--root', '/r', '--manifests', '/p/progress/manifests'])
})

test('VER-52: resumesOf reads the run a skill-loaded line continues, only when it is shaped as a run ID', () => {
  const id = '20260930T090000Z-brainstorm-1a2b3c4d'
  expect(resumesOf(JSON.stringify({ kind: 'skill-loaded', resumes: id }))).toBe(id)
  for (const bad of [undefined, '', 'not json', '{}', JSON.stringify({ resumes: 7 }), JSON.stringify({ resumes: '../../x' }),
    JSON.stringify({ resumes: `${id}/..` }), JSON.stringify({ resumes: 'a/b' })]) {
    expect(resumesOf(bad)).toBeNull()
  }
})

// ---- version 22 (BEH-37, BEH-38, BEH-39) ----

const VALIDATE_PATH = '/plugin/skills/brainstorm/scripts/validate_brn.py'
const DOC = 'docs/specs/brainstorm/BRN-001.md'
const GATED = gatedOf([{ steps: { '6': { evidence: [{ type: 'write', pattern: 'docs/specs/brainstorm/BRN-*.md' }] },
  '7': { evidence: [{ type: 'script', pattern: 'validate_brn.py', exit: 0, target: 'written' }] } }, workFiles: ['devforgeai/drafts/brainstorm/*.md'] }])

test('runsScript gives the answers evaluate.py script_run gave VER-45\'s command strings (run 2026-10-06)', () => {
  const oracle: Array<[string, boolean]> = [
    [`cat ${VALIDATE_PATH} ${DOC}`, false], [`ls ${VALIDATE_PATH}`, false], [`python3 -B ${VALIDATE_PATH} ${DOC}`, true],
    [`PYTHONDONTWRITEBYTECODE=1 python3 ${VALIDATE_PATH} ${DOC}`, true], [`python3 -B ${VALIDATE_PATH} ${DOC} | tail -3`, true],
    [`cd x && python3 ${VALIDATE_PATH} d.md`, true], [`python3.12 ${VALIDATE_PATH} d.md`, true], [`python3 -c 'print(1)' ${VALIDATE_PATH}`, false],
    [`bash ${VALIDATE_PATH}`, true], [`${VALIDATE_PATH} d.md`, true], [`FOO=1 BAR=2 ${VALIDATE_PATH} d.md`, true], ['echo validate_brn.py', false],
    [`node -- ${VALIDATE_PATH}`, true], [`grep -l x ${VALIDATE_PATH}`, false], [`python ${VALIDATE_PATH} x`, true],
  ]
  for (const [command, runs] of oracle) expect(runsScript(command, 'validate_brn.py'), command).toBe(runs)
  // finer than the evaluator on purpose: a ; or a line break also splits a part
  expect(runsScript(`sed -n p d.md > b.md; python3 ${VALIDATE_PATH} b.md`, 'validate_brn.py')).toBe(true)
  expect(runsScript(`echo a\npython3 ${VALIDATE_PATH}`, 'validate_brn.py')).toBe(true)
  expect(scriptWord('python3 -B x.py', 'validate_brn.py')).toBeNull()
})

test('commandParts splits at &&, ||, ;, | and line breaks, but not at the | of >|', () => {
  expect(commandParts('a && b || c ; d | e\nf')).toEqual(['a ', ' b ', ' c ', ' d ', ' e', 'f'])
  expect(commandParts('cat x >| out')).toEqual(['cat x >| out'])
  expect(commandParts('a \\\nb')).toEqual(['a  b'])
})

test('fnmatchcase reads patterns as Python does', () => {
  expect(fnmatchcase('docs/specs/brainstorm/BRN-001.md', 'docs/specs/brainstorm/BRN-*.md')).toBe(true)
  expect(fnmatchcase('docs/specs/brainstorm/x/BRN-1.md', 'docs/specs/brainstorm/BRN-*.md')).toBe(false)
  expect(fnmatchcase('a/b/BRN-1.md', 'a/*/BRN-?.md')).toBe(true)
  expect(fnmatchcase('a1', 'a[0-9]')).toBe(true)
  expect(fnmatchcase('ab', 'a[!0-9]')).toBe(true)
  expect(fnmatchcase('a.md', 'a.md')).toBe(true)
  expect(fnmatchcase('axmd', 'a.md')).toBe(false)
  expect(fnmatchcase('a[', 'a[')).toBe(true)
  expect(pathMatches('docs/x/y.md', 'docs/x/')).toBe(true)
  expect(pathMatches('docs/x', 'docs/x/')).toBe(true)
  expect(ruleMatches('/docs/x/y.md', 'docs/x/')).toBe(false)
  expect(ruleMatches('../docs/x/y.md', '*')).toBe(false)
})

test('pathToken reads a word as BEH-06 reads a read token, with a leading redirection removed first', () => {
  for (const [word, token] of [['>docs/a.md', 'docs/a.md'], ['>|docs/a.md', 'docs/a.md'], ['>>docs/a.md', 'docs/a.md'], ['<docs/a.md', 'docs/a.md'],
    ['&>docs/a.md', 'docs/a.md'], ['2>docs/a.md', 'docs/a.md'], ['2>>docs/a.md', 'docs/a.md'], ['"docs/a.md"', 'docs/a.md'], ["'./docs/a.md';", 'docs/a.md'],
    ['(docs/a.md)', 'docs/a.md'], ['/work/docs/a.md', 'docs/a.md'], ['./docs//a.md', 'docs/a.md'], ['>"/work/docs/a.md"', 'docs/a.md']]) {
    expect(pathToken(word, '/work'), word).toBe(token)
  }
})

test('outsideWord finds a word naming a gated document, outside the parts that run the validator', () => {
  expect(outsideWord(`cat ${DOC}`, GATED, '/work')).toEqual({ word: DOC, step: 6 })
  expect(outsideWord(`python3 -B ${VALIDATE_PATH} ${DOC}`, GATED, '/work')).toBeNull()
  expect(outsideWord(`python3 ${VALIDATE_PATH} ${DOC} && cat ${DOC}`, GATED, '/work')).toEqual({ word: DOC, step: 6 })
  expect(outsideWord('ls docs/specs/brainstorm/', GATED, '/work')).toBeNull()
  expect(outsideWord('cat devforgeai/drafts/brainstorm/x.md', GATED, '/work')).toBeNull()
  expect(outsideWord(`cat ${DOC}`, gatedOf([]), '/work')).toBeNull()
  expect(outsideRefusal(DOC).startsWith(outsideMessage(DOC) + '. ')).toBe(true)
  expect(OUTSIDE_ADVICE).toContain('Write tool')
})

test('gatedOf takes the union of the layers and ignores what isn\'t a rule', () => {
  const g = gatedOf([GATED && { steps: { '1': { evidence: [{ type: 'write', pattern: 'a/*.md' }, { type: 'write' }, 3, null] } }, workFiles: ['d/*.md', 4] },
    { steps: { '1': { evidence: [{ type: 'write', pattern: 'a/*.md' }, { type: 'script', pattern: 's.py', target: 'written' }] }, x: { evidence: [] } } }, null, 'x', { steps: [] }])
  expect(g.writes).toEqual([{ step: 1, pattern: 'a/*.md' }])
  expect(g.scripts).toEqual(['s.py'])
  expect(g.scriptSteps).toEqual([1])
  expect(g.workFiles).toEqual(['d/*.md'])
})

test('folderOf and folderOfFile', () => {
  expect(folderOf('docs/specs/brainstorm/BRN-*.md')).toBe('docs/specs/brainstorm/')
  expect(folderOf('docs/specs/brainstorm/')).toBe('docs/specs/brainstorm/')
  expect(folderOf('docs/x/file.md')).toBe('docs/x/')
  expect(folderOf('BRN-*.md')).toBe('')
  expect(folderOf('docs/*/BRN-1.md')).toBeNull()
  expect(folderOfFile('devforgeai/drafts/brainstorm/s1.md')).toBe('devforgeai/drafts/brainstorm/')
  expect(folderOfFile('x.md')).toBe('')
})

test('changedFiles: new or changed regular files, in order of path, less the folders that failed', () => {
  const e = (size: number, mtimeMs: number, kind = 'file') => ({ kind, size, mtimeMs })
  const before = new Map([['d/a.md', e(1, 1)], ['d/b.md', e(1, 1)], ['f/z.md', e(1, 1)]])
  const after = new Map([['d/b.md', e(1, 1)], ['d/a.md', e(2, 1)], ['d/c.md', e(1, 1)], ['d/l.md', e(1, 1, 'other')], ['f/z.md', e(5, 5)], ['d/m.md', e(1, 2)]])
  expect(changedFiles(before, after, [])).toEqual(['d/a.md', 'd/c.md', 'd/m.md', 'f/z.md'])
  expect(changedFiles(before, after, ['f/'])).toEqual(['d/a.md', 'd/c.md', 'd/m.md'])
})

test('logNames reads a log for a path and its run-end', () => {
  const lines = [JSON.stringify({ kind: 'tool', path: 'a.md' }), 'not json', JSON.stringify({ kind: 'run-end' })]
  expect(logNames(lines, 'a.md')).toEqual({ names: true, ended: true })
  expect(logNames(lines.slice(0, 1), 'b.md')).toEqual({ names: false, ended: false })
})

test('windowClosed: ended, every step reached, or a script-target step done', () => {
  const st = (o: Partial<ProgressState>): ProgressState => ({ skill: 'x', current: 2, ended: null, steps: [{ n: 7, title: 't', state: 'pending' }], flags: [],
    gate: { kind: null, seq: null, refuse: false, reason: null }, manifest: { state: 'matched' }, ...o })
  expect(windowClosed(st({}), [7])).toBe(false)
  expect(windowClosed(st({ ended: 'session-end' }), [7])).toBe(true)
  expect(windowClosed(st({ current: null }), [7])).toBe(true)
  expect(windowClosed(st({ steps: [{ n: 7, title: 't', state: 'done' }] }), [7])).toBe(true)
  expect(windowClosed(st({ steps: [{ n: 7, title: 't', state: 'done' }] }), [])).toBe(false)
})

test('wroteText and withContext', () => {
  expect(wroteText(['a.md', 'b.md'], ['m1', 'm2'])).toBe("DevForgeAI's progress tracker (enforce mode): this Bash command wrote a.md, b.md, which the tracker couldn't check before it was written.\nm1\nm2\nThe file stays as written. Write it again with the Write tool, asking the user first for any decision it records.")
  expect(withContext({ result: 'ok' }, 't')).toEqual({ result: 'ok', context: ['t'] })
  expect(withContext({ result: 'ok', context: ['u'] }, 't')).toEqual({ result: 'ok', context: ['u', 't'] })
  expect(withContext({ deny: 'no' }, 't')).toBeNull()
  expect(withContext(null, 't')).toBeNull()
  expect(stuckAdvice('outside-write', false)).toBe(OUTSIDE_ADVICE)
  expect(stuckAdvice('outside-write', true)).toBe(OUTSIDE_ADVICE)
})

test('formOf keeps the form, never the newer shapes or the answers, and drops it whole over 64 KiB or past 3 MiB', () => {
  const input = { questions: [{ question: 'Q', header: 'H', multiSelect: true, kind: 'k', options: [{ label: 'A', description: 'd', preview: 'p', extra: 1 }] }], answers: { Q: 'A' } }
  expect(formOf(input, 0)).toEqual([{ question: 'Q', header: 'H', multiSelect: true, options: [{ label: 'A', description: 'd', preview: 'p' }] }])
  expect(formOf(input, LOG_CONTENT_LIMIT)).toBeUndefined()
  expect(formOf({ questions: [] }, 0)).toBeUndefined()
  expect(formOf({}, 0)).toBeUndefined()
  expect(formOf({ questions: [{ question: 'Q', options: [{ label: 'A', description: 'x'.repeat(CONTENT_LIMIT) }] }] }, 0)).toBeUndefined()
})

test('formsText renders the last form of the step, points at the log over 8 KiB, and is empty without one', () => {
  const ans = (step: number, q: string) => JSON.stringify({ kind: 'answer', answered: true, step, questions: [{ question: q, header: 'H', options: [{ label: 'A', description: 'd', preview: 'l1\nl2' }, { label: 'B' }] }] })
  const got = formsText('RUN', 5, [ans(5, 'first'), ans(4, 'other'), ans(5, 'last'), 'junk'])
  expect(got.inline).toBe(true)
  expect(got.text).toBe(" The questions last shown at step 5 (Claude's proposals, not the user's answers):\nQ1. last [H]\n- A: d\n    l1\n    l2\n- B")
  expect(formsText('RUN', 6, [ans(5, 'x')])).toEqual({ text: '', inline: false })
  const big = JSON.stringify({ kind: 'answer', step: 5, questions: [{ question: 'q', options: [{ label: 'A', description: 'd'.repeat(9000) }] }] })
  expect(formsText('RUN', 5, [big])).toEqual({ inline: false, text: ' The questions last shown at step 5 are in devforgeai/progress/runs/RUN/events.jsonl, on the events of kind answer with step 5 (field questions).' })
})

test('draftCandidate: the last work file while due is false and the step is at or before the write gate', () => {
  const st = (w: unknown): ProgressState => ({ skill: 'x', current: 1, ended: null, steps: [], flags: [], gate: { kind: null, seq: null, refuse: false, reason: null },
    manifest: { state: 'matched' }, workFiles: w as never })
  expect(draftCandidate(st({ files: ['a', 'd/b.md'], due: false }), 5, 6)).toBe('d/b.md')
  expect(draftCandidate(st({ files: ['a'], due: false }), 6, 6)).toBe('a')
  expect(draftCandidate(st({ files: ['a'], due: false }), 7, 6)).toBeNull()
  expect(draftCandidate(st({ files: ['a'], due: true }), 5, 6)).toBeNull()
  expect(draftCandidate(st({ files: [], due: false }), 5, 6)).toBeNull()
  expect(draftCandidate(st({ files: ['/etc/x'], due: false }), 5, 6)).toBeNull()
  expect(draftCandidate(st({ files: ['../x'], due: false }), 5, 6)).toBeNull()
  expect(draftCandidate(st({ files: ['a'], due: false }), 5, null)).toBeNull()
  expect(draftCandidate(st(undefined), 5, 6)).toBeNull()
})

// ---- versions 21, 23, 24 and 25: other mods' calls, the fuel row, usage, the ledger, /progress and the start names ----

test('VER-54: an origin is another mod\'s only when its plugin is a string other than engine; a missing or odd origin is Claude Code\'s', () => {
  expect(isFromMod({ plugin: 'engine', tier: 'core' })).toBe(false)
  expect(isFromMod(undefined)).toBe(false)
  expect(isFromMod(null)).toBe(false)
  expect(isFromMod({})).toBe(false)
  expect(isFromMod('engine')).toBe(false)
  expect(isFromMod({ plugin: 3 })).toBe(false)
  expect(isFromMod({ plugin: null })).toBe(false)
  expect(isFromMod({ plugin: 'modder' })).toBe(true)
  expect(isFromMod({ plugin: 'devforgeai', tier: 'user' })).toBe(true)
  expect(isEngine({ plugin: 'modder' })).toBe(false)  // BEH-38 and BEH-04 still ask for engine itself
  expect(isEngine(undefined)).toBe(false)
})

test('BEH-41: a command.run is this plugin\'s own when its origin is a plugin of this plugin\'s name', () => {
  expect(isOwnRun({ kind: 'plugin', name: 'devforgeai' }, 'devforgeai')).toBe(true)
  expect(isOwnRun({ kind: 'plugin', name: 'other' }, 'devforgeai')).toBe(false)
  expect(isOwnRun({ kind: 'composer' }, 'devforgeai')).toBe(false)
  expect(isOwnRun({ kind: 'plugin' }, 'devforgeai')).toBe(false)
  expect(isOwnRun({ kind: 'plugin', name: 7 }, 'devforgeai')).toBe(false)
  expect(isOwnRun(undefined, 'devforgeai')).toBe(false)
  expect(isOwnRun(null, 'devforgeai')).toBe(false)
})

test('DM-07 / DM-08: a fuel setting is a whole number from 0 to 95; anything else counts as its default and is reported', () => {
  expect(fuelSetting(undefined, 30)).toEqual({ value: 30, invalid: false })
  for (const ok of [0, 1, 20, 30, 95]) expect(fuelSetting(ok, 30)).toEqual({ value: ok, invalid: false })
  for (const bad of [96, 100, -1, 25.5, NaN, Infinity, null, '', '30', '0', true, false, [], {}]) {
    expect(fuelSetting(bad, 20), String(bad)).toEqual({ value: 20, invalid: true })
  }
})

test('BEH-35: the measured share is a whole number from 0 to 100, and none otherwise', () => {
  for (const ok of [0, 1, 70, 100]) expect(measuredShare(ok)).toBe(ok)
  for (const bad of [undefined, null, NaN, -1, 101, 50.5, '70', true]) expect(measuredShare(bad), String(bad)).toBeNull()
})

const view = (o: Partial<typeof NO_PRECOMPACT> = {}) => ({ ...NO_PRECOMPACT, ...o })

test('BEH-35: the row\'s text by fuel, the warning share, the run share and what has happened', () => {
  expect(NO_PRECOMPACT).toEqual({ percent: null, hidden: false, ran: false, failed: false, pending: false })
  expect(precompactRow(view(), 30, 20)).toBeNull()                                  // no measurement: no row
  expect(precompactRow(view({ percent: 69 }), 30, 20)).toBeNull()                   // fuel 31
  expect(precompactRow(view({ percent: 70 }), 30, 20)).toBe('▲ Fuel 30% · precompact runs at 20%')
  expect(precompactRow(view({ percent: 72 }), 30, 20)).toBe('▲ Fuel 28% · precompact runs at 20%')
  expect(precompactRow(view({ percent: 79 }), 30, 20)).toBe('▲ Fuel 21% · precompact runs at 20%')
  expect(precompactRow(view({ percent: 80 }), 30, 20)).toBeNull()                   // the run share: the run starts, no text of its own
  expect(precompactRow(view({ percent: 85, ran: true }), 30, 20)).toBeNull()        // a run has started
  expect(precompactRow(view({ percent: 72, hidden: true }), 30, 20)).toBeNull()     // the skill loaded
  expect(precompactRow(view({ percent: 72 }), 30, 0)).toBe('▲ Fuel 28% · consider /devforgeai:precompact before /compact')
  expect(precompactRow(view({ percent: 99 }), 30, 0)).toBe('▲ Fuel 1% · consider /devforgeai:precompact before /compact')
  expect(precompactRow(view({ percent: 72 }), 0, 20)).toBeNull()                    // the warning off
  expect(precompactRow(view({ percent: 80, failed: true, ran: true }), 30, 20)).toBe('● Fuel 20% · run /devforgeai:precompact now')
  expect(precompactRow(view({ percent: 90, failed: true, ran: true }), 30, 20)).toBe('● Fuel 10% · run /devforgeai:precompact now')
  expect(precompactRow(view({ percent: 80, failed: true, ran: true }), 0, 20)).toBeNull()      // the warning off: no row
  // R1 (Bryan, 2026-10-08, "Show it at once"): a failed run draws the failed row at once, above the warning share too
  expect(precompactRow(view({ percent: 60, failed: true, ran: true }), 30, 40)).toBe('● Fuel 40% · run /devforgeai:precompact now')
  expect(precompactRow(view({ percent: 65, failed: true, ran: true }), 30, 40)).toBe('● Fuel 35% · run /devforgeai:precompact now')
  expect(precompactRow(view({ percent: 10, failed: true, ran: true }), 95, 20)).toBe('● Fuel 90% · run /devforgeai:precompact now')
  expect(precompactRow(view({ percent: 60, ran: true }), 30, 40)).toBeNull()                     // not failed: still no row above the warning share
  expect(precompactRow(view({ percent: 70, failed: true, ran: true, hidden: true }), 30, 20)).toBeNull()
  // a run share at or above the warning share: the run starts first, so the row appears only when the run fails
  expect(precompactRow(view({ percent: 75 }), 20, 25)).toBeNull()
  expect(precompactRow(view({ percent: 80, ran: true }), 20, 25)).toBeNull()
  expect(precompactRow(view({ percent: 80, ran: true, failed: true }), 20, 25)).toBe('● Fuel 20% · run /devforgeai:precompact now')
})

test('BEH-36: the automatic run is due at or below the run share, once, not hidden, and never with the run share 0', () => {
  expect(precompactDue(view({ percent: 80 }), 20)).toBe(true)
  expect(precompactDue(view({ percent: 99 }), 20)).toBe(true)
  expect(precompactDue(view({ percent: 79 }), 20)).toBe(false)
  expect(precompactDue(view({ percent: 80, ran: true }), 20)).toBe(false)
  expect(precompactDue(view({ percent: 80, hidden: true }), 20)).toBe(false)
  expect(precompactDue(view({ percent: 80, failed: true }), 20)).toBe(false)
  expect(precompactDue(view({ percent: 100 }), 0)).toBe(false)
  expect(precompactDue(view(), 20)).toBe(false)
})

test('BEH-40: a usage event\'s fields come from a turn ID, a model and four whole counts of 0 or more, and from nothing less', () => {
  const usage = { input_tokens: 1200, output_tokens: 340, cache_read_input_tokens: 5000, cache_creation_input_tokens: 0, model: 'claude-opus-5-5', extra: 1 }
  expect(usageFields('t1', usage)).toEqual({ turn: 't1', model: 'claude-opus-5-5', input: 1200, output: 340, cacheRead: 5000, cacheWrite: 0 })
  expect(usageFields(undefined, usage)).toBeNull()
  expect(usageFields('', usage)).toBeNull()
  expect(usageFields(7, usage)).toBeNull()
  for (const bad of [null, undefined, 'x', 3, []]) expect(usageFields('t1', bad)).toBeNull()
  expect(usageFields('t1', { ...usage, model: '' })).toBeNull()
  expect(usageFields('t1', { ...usage, model: 4 })).toBeNull()
  const { model: _m, ...noModel } = usage
  expect(usageFields('t1', noModel)).toBeNull()
  for (const key of ['input_tokens', 'output_tokens', 'cache_read_input_tokens', 'cache_creation_input_tokens']) {
    for (const bad of [-1, 1.5, '7', true, null, undefined, NaN, Infinity]) {
      expect(usageFields('t1', { ...usage, [key]: bad }), `${key}=${String(bad)}`).toBeNull()
    }
  }
})

test('BEH-40: a usage event line holds turn, model, input, output, cacheRead and cacheWrite in DM-02\'s order', () => {
  const fields = { cacheWrite: 4, cacheRead: 3, output: 2, input: 1, model: 'm', turn: 't1', extra: 9 }
  expect(eventLine(RUN, 5, T0 + 5000, 'usage', fields)).toBe('{"run":"' + RUN + '","seq":5,"time":"2026-10-02T12:00:05Z","kind":"usage",'
    + '"turn":"t1","model":"m","input":1,"output":2,"cacheRead":3,"cacheWrite":4}')
})

test('SPEC-016 BEH-10: a ledger line is DM-04\'s object, in its field order, with the time to the second', () => {
  const fields = { turn: 't1', model: 'm', input: 1, output: 2, cacheRead: 3, cacheWrite: 4 }
  expect(ledgerLine('s1', 't1', 'main', fields, T0 + 7000)).toBe('{"session":"s1","turn":"t1","source":"main","input":1,"output":2,'
    + '"cacheRead":3,"cacheWrite":4,"time":"2026-10-02T12:00:07Z"}')
  expect(JSON.parse(ledgerLine('s1', 't9', 'agent-7', fields, T0)).source).toBe('agent-7')
})

const SUMMARY = {
  skill: 'brainstorm', current: 2, steps: 2, flags: 0, yourTurn: false, ended: null as string | null, manifest: 'matched' as const,
  states: ['done', 'current'], currentTitle: 'Pick', lastFlag: null as string | null,
}

test('BEH-34: /progress prints the status line and the band\'s two rows without the button; with no run, the sentence and an ended run\'s status', () => {
  expect(progressReport(SUMMARY, true, 'observe', false, null, [])).toBe('brainstorm 2/2\nbrainstorm  ●◆  step 2 of 2: Pick\nobserve mode  no flags')
  expect(progressReport({ ...SUMMARY, flags: 1, lastFlag: 'step 1 was skipped' }, true, 'enforce', true, null, []))
    .toBe('brainstorm 2/2 · 1 flag · idle · enforce\nbrainstorm  ●◆  step 2 of 2: Pick\nenforce mode  step 1 was skipped')
  const paused = [{ skill: 'architecture', step: 7, summary: { steps: 11 } }]
  const text = progressReport(SUMMARY, true, 'observe', false, null, paused).split('\n')
  expect(text[0]).toBe('brainstorm 2/2 · in architecture 7/11')
  expect(text[1]).toBe('brainstorm  ●◆  step 2 of 2: Pick (paused: architecture at step 7)')
  expect(progressReport(null, false, 'observe', false, null, [])).toBe('No DevForgeAI run is open in this session.')
  expect(progressReport({ ...SUMMARY, ended: 'session-end' }, true, 'observe', false, null, []))
    .toBe('No DevForgeAI run is open in this session.\nbrainstorm ended')
  expect(progressReport({ ...SUMMARY, ended: 'stopped', current: null, stoppedAt: 8 }, true, 'enforce', false, null, []))
    .toBe('No DevForgeAI run is open in this session.\nbrainstorm stopped at step 8 · enforce')
  expect(progressReport(SUMMARY, false, 'observe', false, null, [])).toBe('No DevForgeAI run is open in this session.')
})

// VER-64 (the tile half is STUBBED): the tile setter isn't built (held with the dashboard), so a made-up second setter adds
// a name to the set directly; BEH-36's setter adds precompact. The set's operations are the module's own.
test('VER-56 / VER-64 (STUB second setter): two setters don\'t erase each other in either order; each command.run takes only its own name; a failure drops only its own', () => {
  for (const order of [['devforgeai:precompact', 'brainstorm'], ['brainstorm', 'devforgeai:precompact']]) {
    const set = new Set<string>()
    for (const command of order) addStart(set, command)
    expect([...set].sort()).toEqual(['brainstorm', 'precompact'])
    expect(takeStart(set, 'devforgeai:precompact')).toBe(true)
    expect([...set]).toEqual(['brainstorm'])
    expect(takeStart(set, 'devforgeai:precompact')).toBe(false)     // a second command.run of the name is not typed
    expect(takeStart(set, 'devforgeai:spec-lookup')).toBe(false)    // a name that was never added
    expect(takeStart(set, 'brainstorm')).toBe(true)
    expect(set.size).toBe(0)
  }
  const set = new Set(['precompact', 'brainstorm'])
  takeStart(set, 'devforgeai:brainstorm')                           // ERR-24's removal of the tile's name only
  expect([...set]).toEqual(['precompact'])
})

test('BEH-35: a compaction is a result with messages; a skip is not', () => {
  expect(isCompaction({ messages: [] })).toBe(true)
  expect(isCompaction({ messages: [{ role: 'user', text: 'x', toolUses: [] }], tokensBefore: 10 })).toBe(true)
  expect(isCompaction({ skip: 'blocked' })).toBe(false)
  expect(isCompaction({ messages: 'x' })).toBe(false)
  expect(isCompaction(undefined)).toBe(false)
  expect(isCompaction(null)).toBe(false)
})

// ---- version 27 (SPEC-013 BEH-42, BEH-10, BEH-11, BEH-34; SPEC-016 version 3): the hold, its texts, the remedy row ----

test('VER-73 (BEH-10): the run\'s hold replaces the summary and any evaluator reason; the odometer\'s alone ends the summary', () => {
  expect(RETRYING).toBe('progress: retrying (cannot write devforgeai/progress)')
  expect(statusText(SUMMARY, 'observe', false, null, [], 'run')).toBe('progress: retrying (cannot write devforgeai/progress)')
  expect(statusText(SUMMARY, 'enforce', true, 'python not found', [], 'run')).toBe('progress: retrying (cannot write devforgeai/progress)')
  expect(statusText(null, 'observe', false, null, [], 'run')).toBe('progress: retrying (cannot write devforgeai/progress)')
  expect(statusText(SUMMARY, 'observe', false, null, [], null)).toBe('brainstorm 2/2')
  expect(statusText(SUMMARY, 'observe', false, null, [], 'odometer')).toBe('brainstorm 2/2 · odometer retrying')
  expect(statusText({ ...SUMMARY, flags: 2 }, 'enforce', false, null, [], 'odometer')).toBe('brainstorm 2/2 · 2 flags · enforce · odometer retrying')
  expect(statusText({ ...SUMMARY, ended: 'session-end' }, 'observe', false, null, [], 'odometer')).toBe('brainstorm ended · odometer retrying')
  expect(statusText(SUMMARY, 'observe', false, 'python not found', [], 'odometer')).toBe('progress: off (python not found)')
  expect(statusText(null, 'observe', false, null, [], 'odometer')).toBe(undefined)
  // the stop's text is the earlier versions' (no hold any more)
  expect(statusText(SUMMARY, 'observe', false, 'cannot write devforgeai/progress', [], null)).toBe('progress: off (cannot write devforgeai/progress)')
})

test('BEH-42 (c): an error is the first line of what the host said, cut to 200 characters', () => {
  expect(errorLine("EACCES: permission denied, open '/w/x'\nsecond line")).toBe("EACCES: permission denied, open '/w/x'")
  expect(errorLine('\n  \n  EIO: boom  \nmore')).toBe('EIO: boom')
  expect(errorLine('x'.repeat(250))).toBe('x'.repeat(200))
  expect(errorLine('x'.repeat(200))).toBe('x'.repeat(200))
  expect(errorLine('')).toBe('')
})

test('VER-73 (BEH-11): the remedy row puts the action first, then the count, enforce mode\'s warning for the run\'s log, then the diagnosis', () => {
  const run = { kind: 'run' as const, lines: 12, path: '/work/devforgeai/progress/runs/r1/events.jsonl', error: 'EACCES: permission denied' }
  expect(remedyRow(run, false, true)).toBe('▲ Fix devforgeai/progress, then /progress retry · 12 lines held · cannot write '
    + '/work/devforgeai/progress/runs/r1/events.jsonl: EACCES: permission denied')
  expect(remedyRow(run, true, true)).toBe('▲ Fix devforgeai/progress, then /progress retry · 12 lines held · enforce mode checks nothing until then · cannot write '
    + '/work/devforgeai/progress/runs/r1/events.jsonl: EACCES: permission denied')
  const odo = { kind: 'odometer' as const, lines: 3, path: '/work/devforgeai/progress/odometer/s1.jsonl', error: 'EIO' }
  expect(remedyRow(odo, false, true)).toBe('▲ Fix devforgeai/progress, then /progress retry · 3 odometer lines held · cannot write '
    + '/work/devforgeai/progress/odometer/s1.jsonl: EIO')
  expect(remedyRow(odo, true, true)).toBe(remedyRow(odo, false, true))   // enforce mode is the run\'s log only
  // without /progress (ERR-21) the action says when the adapter tries again
  expect(remedyRow(run, false, false)).toBe('▲ Fix devforgeai/progress; the adapter tries again at the end of each turn · 12 lines held · cannot write '
    + '/work/devforgeai/progress/runs/r1/events.jsonl: EACCES: permission denied')
  // cut to a narrow width, its end goes first, which is the diagnosis
  expect(fit(remedyRow(run, false, true), 50)).toBe('▲ Fix devforgeai/progress, then /progress retry ·…')
})

test('VER-73 (BEH-42 (c)): the toasts for a hold, a recovery and a stop', () => {
  const run = { kind: 'run' as const, lines: 2, path: '/w/p/runs/r/events.jsonl', error: 'EACCES' }
  expect(heldToast(run, true)).toBe('DevForgeAI progress: cannot write /w/p/runs/r/events.jsonl: EACCES. Events are held in memory; fix it, then /progress retry.')
  expect(heldToast(run, false)).toBe('DevForgeAI progress: cannot write /w/p/runs/r/events.jsonl: EACCES. Events are held in memory; fix it; the adapter tries again at the end of each turn.')
  const odo = { kind: 'odometer' as const, lines: 2, path: '/w/p/odometer/s1.jsonl', error: 'EIO' }
  expect(heldToast(odo, true)).toBe('DevForgeAI progress: cannot write /w/p/odometer/s1.jsonl: EIO. Odometer lines are held in memory; fix it, then /progress retry.')
  expect(recoveredToast(7)).toBe('DevForgeAI progress: writing again; 7 held lines saved.')
  expect(STOP_TOAST).toBe('DevForgeAI progress: off (cannot write devforgeai/progress). Fix it, then /progress retry.')
  expect(odometerGaveUpToast('/w/p/odometer/s1.jsonl')).toBe('DevForgeAI progress: the odometer is off for this session (cannot write /w/p/odometer/s1.jsonl). Fix it, then /progress retry.')
  expect(HOLD_TRIES).toBe(10)
})

test('VER-69 / VER-70 (DM-02): the adapter.log texts of a hold, and /progress retry\'s answers', () => {
  expect(heldLog(3, '/w/e.jsonl', 'EACCES')).toBe('held 3 lines: /w/e.jsonl: EACCES')
  expect(recoveredLog(2, '/w/e.jsonl', 5)).toBe('recovered after 2 tries: /w/e.jsonl; wrote 5 lines')
  expect(gaveUpLog(10, '/w/e.jsonl', 'EACCES', 9)).toBe('gave up after 10 tries: /w/e.jsonl: EACCES; dropped 9 lines')
  expect(savedAnswer(4, '/w/e.jsonl')).toBe('Writing again: 4 held lines saved to /w/e.jsonl.')
  expect(stillAnswer('/w/e.jsonl', 'EACCES', 6, 3)).toBe('Still cannot write /w/e.jsonl: EACCES. 6 lines are held; the adapter also tries at the end of each turn (try 3 of 10 used).')
  expect(liftedAnswer()).toBe('Tracking is on again: the next DevForgeAI skill you run opens a run. The run that was dropped is not revived.')
  expect(stillStoppedAnswer('/w/.gitignore', 'EACCES')).toBe('Still cannot write /w/.gitignore: EACCES. Tracking stays off.')
  expect(odometerOnAnswer()).toBe('The odometer is writing again.')
  expect(odometerStillAnswer('/w/o.jsonl', 'EIO')).toBe('Still cannot write /w/o.jsonl: EIO. The odometer stays off.')
  expect(NOTHING_TO_RETRY).toBe('Nothing to retry: no write has failed.')
  expect(STOPPED_LINE).toBe('progress: off (cannot write devforgeai/progress). Fix the folder, then /progress retry.')
})

test('VER-73 (BEH-34): /progress while a hold lasts ends with the remedy row\'s text', () => {
  const row = '▲ Fix devforgeai/progress, then /progress retry · 2 lines held · cannot write /w/e: EACCES'
  expect(progressReport(SUMMARY, true, 'observe', false, null, [], 'run', row)).toBe('progress: retrying (cannot write devforgeai/progress)\n'
    + 'brainstorm  ●◆  step 2 of 2: Pick\nobserve mode  no flags\n' + row)
  expect(progressReport(SUMMARY, true, 'observe', false, null, [], 'odometer', row)).toBe('brainstorm 2/2 · odometer retrying\n'
    + 'brainstorm  ●◆  step 2 of 2: Pick\nobserve mode  no flags\n' + row)
  expect(progressReport(null, false, 'observe', false, null, [], 'odometer', row)).toBe('No DevForgeAI run is open in this session.\n' + row)
  expect(progressReport({ ...SUMMARY, ended: 'session-end' }, true, 'observe', false, null, [], 'odometer', row))
    .toBe('No DevForgeAI run is open in this session.\nbrainstorm ended · odometer retrying\n' + row)
  // without a hold the report is as before
  expect(progressReport(SUMMARY, true, 'observe', false, null, [], null, null)).toBe('brainstorm 2/2\nbrainstorm  ●◆  step 2 of 2: Pick\nobserve mode  no flags')
})

// ---- version 28: the log level and the rollover (BEH-43, BEH-44, DM-09, DM-10) ----

test('DM-09: logLevel is off, normal or verbose; anything else counts as normal, never as off, and is flagged', () => {
  expect(logLevelOf('off')).toEqual({ level: 'off', invalid: false })
  expect(logLevelOf('normal')).toEqual({ level: 'normal', invalid: false })
  expect(logLevelOf('verbose')).toEqual({ level: 'verbose', invalid: false })
  expect(logLevelOf(undefined)).toEqual({ level: 'normal', invalid: false })   // missing: the default, as fuelSetting treats one
  for (const bad of [null, 0, 1, 'debug', 'Verbose', 'OFF', '', {}, true]) expect(logLevelOf(bad)).toEqual({ level: 'normal', invalid: true })
})

test('DM-10: logRolloverMiB is a whole number from 1 to 3; 1.5, 0, 4, a string and null count as 1 and are flagged', () => {
  for (const v of [1, 2, 3]) expect(rolloverMiBOf(v)).toEqual({ value: v, invalid: false })
  expect(rolloverMiBOf(undefined)).toEqual({ value: 1, invalid: false })
  for (const bad of [null, 0, 4, 1.5, '2', NaN, -1, {}]) expect(rolloverMiBOf(bad)).toEqual({ value: 1, invalid: true })
})

test('DM-02: a line\'s time is to the second at normal and to the millisecond at verbose', () => {
  expect(logStamp(T0 + 123, false)).toBe('2026-10-02T12:00:00Z')
  expect(logStamp(T0 + 123, true)).toBe('2026-10-02T12:00:00.123Z')
  expect(logStamp(T0, true)).toBe('2026-10-02T12:00:00.000Z')
})

test('BEH-43 (e): a trace line is one line and is cut to 300 characters', () => {
  expect(traceCut('a\n  b\r\nc')).toBe('a b c')
  expect(traceCut('x'.repeat(500)).length).toBe(TRACE_CUT)
  expect(TRACE_CUT).toBe(300)
  expect(TRACE_LIMIT).toBe(1000)
  expect(EARLY_LIMIT).toBe(200)
})

test('BEH-44: the rollover is due by size (the file passes the cap) or by day (its first line is earlier than the batch\'s), size first', () => {
  const MIB = 1024 * 1024
  const line = (day: string) => `${day}T10:00:00Z s1 - mode: x\n`
  expect(rollReason(line('2026-10-02'), line('2026-10-02'), 1)).toBeNull()
  expect(rollReason(line('2026-10-01'), line('2026-10-02'), 1)).toBe('day')
  expect(rollReason(line('2026-10-03'), line('2026-10-02'), 1)).toBeNull()         // a clock set back rolls nothing
  expect(rollReason('no date here\n', line('2026-10-02'), 1)).toBeNull()           // no date, no day check
  expect(rollReason('', line('2026-10-02'), 1)).toBeNull()                         // an empty file rolls nothing
  const big = line('2026-10-02') + 'y'.repeat(MIB)
  expect(rollReason(big, line('2026-10-02'), 1)).toBe('size')
  expect(rollReason(big, line('2026-10-02'), 2)).toBeNull()
  expect(rollReason(line('2026-10-01') + 'y'.repeat(MIB), line('2026-10-02'), 1)).toBe('size')   // both: it says size
  expect(rollReason(line('2026-10-02') + 'y'.repeat(2 * MIB), line('2026-10-02'), 3)).toBeNull()
})

test('BEH-44: a batch larger than the cap is split between lines, each piece under the cap', () => {
  const lines = Array.from({ length: 10 }, (_, i) => `line ${i} ${'z'.repeat(90)}\n`).join('')
  const pieces = chunkLines(lines, 300)
  expect(pieces.join('')).toBe(lines)
  expect(pieces.length).toBeGreaterThan(1)
  for (const p of pieces) expect(new TextEncoder().encode(p).length).toBeLessThanOrEqual(300)
  expect(chunkLines('short\n', 300)).toEqual(['short\n'])
  expect(chunkLines('', 300)).toEqual([])
})

test('BEH-43 (f): waiting lines and buffered trace lines merge by time, then by order', () => {
  const a = [{ t: 5, n: 1, line: 'a' }, { t: 9, n: 4, line: 'd' }]
  const b = [{ t: 5, n: 2, line: 'b' }, { t: 7, n: 3, line: 'c' }]
  expect(mergeByTime(a, b).map(x => x.line)).toEqual(['a', 'b', 'c', 'd'])
  expect(mergeByTime([], []).length).toBe(0)
})

test('BEH-34 (version 28): /progress log reads exactly one word after log; the answers are the spec\'s', () => {
  expect(logCommand('log verbose', 'normal', 'normal')).toEqual({ level: 'verbose', text: 'Log level is now verbose for this session. The default in /config is normal.' })
  expect(logCommand('  log   off ', 'verbose', 'normal')).toEqual({ level: 'off', text: 'Log level is now off for this session. The default in /config is normal.' })
  expect(logCommand('log normal', 'normal', 'off')).toEqual({ level: null, text: 'Log level is already normal for this session. The default in /config is off.' })
  for (const bad of ['log', 'log loud', 'log Verbose', 'log verbose now', 'log off off', 'log ']) {
    expect(logCommand(bad, 'normal', 'normal')).toEqual({ level: null, text: 'Usage: /progress log off|normal|verbose. The level is normal.' })
  }
  for (const other of ['', 'retry', 'logs', 'x log verbose', 'ignored']) expect(logCommand(other, 'normal', 'normal')).toBeNull()
})
