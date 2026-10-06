// Pure helpers of the progress tracker adapter (SPEC-013 v7). No `$` here: claude plugin validate lets `$` reach
// only top-level functions of hooks/progress.tsx, so this file turns plain data into plain data, and its tests
// (core.test.ts) call it directly.
import type { ProgressMode, ProgressPaused, ProgressRefused, ProgressSummary } from '../types'

export type Fields = Record<string, unknown>

/** The 64 KiB a Write or Edit's content may take in an event, and the log sizes of ERR-11 (BEH-15). */
export const CONTENT_LIMIT = 64 * 1024
export const LOG_CONTENT_LIMIT = 3 * 1024 * 1024
export const LOG_LIMIT = 4 * 1024 * 1024
export const IDLE_MS = 30 * 60 * 1000
export const FORMAT = 'devforgeai-events/1'

// Each kind's fields in SPEC-012 DM-02's order, after run, seq, time and kind. The order is fixed here so an
// event line is the same bytes whichever code built it (VER-04 compares lines byte for byte).
const ORDER: Record<string, readonly string[]> = {
  'skill-loaded': ['format', 'skill', 'checklist', 'host', 'taskList', 'mode', 'modeSource', 'resumes', 'carried', 'answered'],
  tool: ['tool', 'path', 'command', 'exit', 'error', 'content'],
  answer: ['answered', 'step', 'outside', 'waiver'],
  prompt: [],
  reply: ['text'],
  turn: ['phase'],
  'run-end': ['reason'],
  step: ['step', 'state'],
}

/** UTC time as ISO 8601 to the second. */
export function isoTime(ms: number): string {
  return new Date(ms).toISOString().replace(/\.\d{3}Z$/, 'Z')
}

/** One event as a JSON line (DM-01): run, seq, time, kind, then the kind's fields; undefined fields left out. */
export function eventLine(run: string, seq: number, ms: number, kind: string, fields: Fields = {}): string {
  const out: Fields = { run, seq, time: isoTime(ms), kind }
  for (const key of ORDER[kind] ?? []) if (fields[key] !== undefined) out[key] = fields[key]
  return JSON.stringify(out)
}

/** The run ID: UTC time as yyyymmddThhmmssZ, the skill, 8 hex digits (SPEC-012 §4; BEH-03). */
/** A skill's name as its run IDs carry it (DM-02's pattern): lower case, other characters as '-', from its first
 *  letter. The offer looks for earlier runs under the same name (BEH-31). */
export function runName(skill: string): string {
  return skill.toLowerCase().replace(/[^a-z0-9-]+/g, '-').replace(/^[^a-z]+/, '') || 'skill'
}

export function runId(ms: number, skill: string, random: Uint8Array): string {
  const t = isoTime(ms).replace(/[-:]/g, '')
  const name = runName(skill)
  const hex = Array.from(random.slice(0, 4), b => b.toString(16).padStart(2, '0')).join('')
  return `${t}-${name}-${hex.padEnd(8, '0')}`
}

/** A skill's name without a '<plugin>:' prefix (BEH-02; §9, P3). */
export function skillName(raw: string): string {
  const i = raw.lastIndexOf(':')
  return i >= 0 ? raw.slice(i + 1) : raw
}

/** Whether a skill opens a run: one of the plugin's own, or one a project manifest names (BEH-02). */
export function isTracked(name: string, pluginSkills: readonly string[], manifestNames: readonly string[]): boolean {
  return pluginSkills.includes(name) || manifestNames.includes(name)
}

/** Whether a plugin skill's SKILL.md marks it untracked (BEH-02, version 18). Its frontmatter is the text between its
 *  first line, '---', and the next line that is '---'; its metadata block is the frontmatter's line 'metadata:' at
 *  column 0 and the lines after it that start with a space. The skill is untracked when that block holds a line
 *  devforgeai-tracked: "false", the value in double or single quotes, with leading and trailing spaces, a trailing
 *  '# comment' and a CR ignored (a file with CRLF line ends reads the same). Anything else is tracked: no such line, the
 *  key outside the block, false unquoted (a YAML boolean), "False" or any other value, no frontmatter. */
export function isUntrackedSkill(skillMd: string): boolean {
  const lines = skillMd.split('\n').map(l => (l.endsWith('\r') ? l.slice(0, -1) : l))
  if (lines[0] !== '---') return false
  const close = lines.indexOf('---', 1)
  if (close < 0) return false
  const front = lines.slice(1, close)
  const at = front.findIndex(l => l.trimEnd() === 'metadata:')
  if (at < 0) return false
  for (let i = at + 1; i < front.length && front[i].startsWith(' '); i++) {
    if (UNTRACKED_LINE.test(front[i])) return true
  }
  return false
}

/** The line that marks a skill untracked: the key, then the value "false" or 'false', then at most a comment. */
const UNTRACKED_LINE = /^ *devforgeai-tracked:[ \t]+(?:"false"|'false')[ \t]*(?:[ \t]#.*)?$/

/** A path relative to the project root with / separators; a path outside the root stays absolute. */
export function relPath(root: string, path: string): string {
  const p = path.replace(/\\/g, '/')
  const r = root.replace(/\\/g, '/').replace(/\/+$/, '')
  if (p === r) return '.'
  return p.startsWith(r + '/') ? p.slice(r.length + 1) : p
}

function str(value: unknown): string | undefined {
  return typeof value === 'string' ? value : undefined
}

/** A tool event's path field (DM-01). */
export function toolPath(root: string, tool: string, input: Fields): string | undefined {
  if (tool === 'Read' || tool === 'Write' || tool === 'Edit') {
    const f = str(input.file_path)
    return f === undefined ? undefined : relPath(root, f)
  }
  if (tool === 'Glob') {
    const pattern = str(input.pattern)
    if (pattern === undefined) return undefined
    const base = str(input.path)
    return base === undefined ? pattern : `${relPath(root, base).replace(/\/+$/, '')}/${pattern}`
  }
  if (tool === 'Grep') {
    const base = str(input.path)
    return base === undefined ? '.' : relPath(root, base)
  }
  return undefined
}

/** What next(e) resolved to for a tool call, as far as the adapter reads it. */
export type ToolOutcome = { deny?: unknown; isError?: unknown; text?: unknown; result?: unknown }

/** A call refused by anyone ({ deny }) or that failed (isError) never ran as asked: error true (DM-01). */
export function isFailed(outcome: ToolOutcome): boolean {
  return outcome.deny !== undefined || outcome.isError === true
}

/** The exit field: 'Exit code <n>' from a failed call's text, 0 when it succeeded, else null (§9, P6). */
export function exitOf(outcome: ToolOutcome): number | null {
  if (outcome.deny !== undefined) return null
  if (outcome.isError !== true) return 0
  const text = typeof outcome.text === 'string' ? outcome.text : typeof outcome.result === 'string' ? outcome.result : ''
  const m = text.match(/Exit code (\d+)/)
  return m ? Number(m[1]) : null
}

/** An AskUserQuestion was answered: it didn't fail, and its answers hold at least one entry (§9, P5). */
export function isAnswered(outcome: ToolOutcome): boolean {
  if (isFailed(outcome)) return false
  const result = outcome.result as { answers?: unknown } | undefined
  const answers = result && typeof result === 'object' ? result.answers : undefined
  return !!answers && typeof answers === 'object' && Object.keys(answers as object).length > 0
}

/** UTF-8 size of a string. */
export function byteSize(text: string): number {
  return new TextEncoder().encode(text).length
}

/** The file an Edit will leave, or null when it can't be computed (ERR-06). */
export function editResult(file: string, oldString: string, newString: string, replaceAll: boolean): string | null {
  if (oldString === '' || byteSize(file) > CONTENT_LIMIT) return null
  const first = file.indexOf(oldString)
  if (first < 0) return null
  if (replaceAll) return file.split(oldString).join(newString)
  if (file.indexOf(oldString, first + oldString.length) >= 0) return null
  return file.slice(0, first) + newString + file.slice(first + oldString.length)
}

/** Content kept in a tool event: at most 64 KiB, and none once the log has passed 3 MiB (BEH-15, ERR-11). */
export function keptContent(content: string | null | undefined, logBytes: number): string | undefined {
  if (content === null || content === undefined) return undefined
  if (logBytes >= LOG_CONTENT_LIMIT || byteSize(content) > CONTENT_LIMIT) return undefined
  return content
}

/** The text of a response row: its text blocks joined by newlines; none for a row without text (§9, P7). */
export function replyText(content: unknown): string {
  if (typeof content === 'string') return content
  if (!Array.isArray(content)) return ''
  return content
    .filter(b => !!b && typeof b === 'object' && (b as Fields).type === 'text' && typeof (b as Fields).text === 'string')
    .map(b => (b as Fields).text as string)
    .join('\n')
}

/** A prompt the person sent: typed at the prompt or through Remote Control (BEH-04). */
export function isPersonPrompt(origin: unknown): boolean {
  const kind = origin && typeof origin === 'object' ? (origin as Fields).kind : undefined
  return kind === 'composer' || kind === 'bridge'
}

/** An event Claude Code itself fired, not a mod (next.origin; BEH-04). */
export function isEngine(origin: unknown): boolean {
  return !!origin && typeof origin === 'object' && (origin as Fields).plugin === 'engine'
}

// The parts of SPEC-012's progress state (DM-03) the adapter reads.
export type StateStep = { n: number; title: string; state: string; userOwned?: boolean; kind?: string | null; stoppable?: boolean
  evidence?: { type: string }[]; claim?: { state: string } | null }
export type StateFlag = { gate: string; seq: number; step: number; type: string; message: string }
export type ProgressState = {
  run?: string
  skill: string
  current: number | null
  ended: string | null
  steps: StateStep[]
  flags: StateFlag[]
  gate: { kind: string | null; seq: number | null; refuse: boolean; reason: string | null }
  manifest: { state: ProgressSummary['manifest'] }
  counts?: { stepEvents?: number; unmarkedQuestions?: number }
  /** Version 15: present when the run's manifest names workFiles (SPEC-012 BEH-21, DM-03). */
  workFiles?: { files?: unknown; due?: unknown }
}

/** The summary the status line and the band draw (DM-03). */
export function summaryOf(state: ProgressState): ProgressSummary {
  const cur = state.current === null ? undefined : state.steps.find(s => s.n === state.current)
  return {
    skill: state.skill,
    current: state.current,
    steps: state.steps.length,
    flags: state.flags.length,
    yourTurn: cur?.state === 'your-turn',
    ended: state.ended,
    manifest: state.manifest.state,
    states: state.steps.map(s => s.state),
    currentTitle: cur?.title ?? null,
    lastFlag: state.flags.length ? state.flags[state.flags.length - 1].message : null,
  }
}

/** The step a stopped run stopped at (BEH-10, version 12): the stopping answer's step, kept in the summary; without it,
 *  the last step past pending (the evaluator ignores everything after the run-end); null for any other run. */
export function stopStep(summary: ProgressSummary): number | null {
  if (summary.ended !== 'stopped') return null
  if (typeof summary.stoppedAt === 'number') return summary.stoppedAt
  let n = 0
  summary.states.forEach((s, i) => { if (s !== 'pending') n = i + 1 })
  return n > 0 ? n : null
}

/** The label that stops a run (SPEC-013 BEH-27, version 12), as SPEC-003 BEH-08 offers it at architecture's step 8. */
export const STOP_LABEL = 'Write nothing'

/** Whether an engine-fired question's answer stops the run (BEH-27): one question, tagged with a step that the latest
 *  state marks stoppable, answered with the stop label (a typed answer equal to it can't be told apart). */
export function stopsRun(input: Fields, outcome: ToolOutcome, steps: readonly StateStep[]): boolean {
  if (!isAnswered(outcome) || !Array.isArray(input.questions) || input.questions.length !== 1) return false
  const step = questionTag(input).step
  if (step === undefined || steps.find(s => s.n === step)?.stoppable !== true) return false
  const question = (input.questions as Fields[])[0]?.question
  const answers = (outcome.result as { answers?: Record<string, unknown> }).answers ?? {}
  return typeof question === 'string' && Object.hasOwn(answers, question) && answers[question] === STOP_LABEL
}

/** The commands BEH-28 confirms while a run is unfinished, with the verb its dialog uses (version 12). */
export const CONFIRMED: Record<string, string> = { clear: 'Clear', exit: 'Exit', resume: 'Resume' }

/** BEH-28's question for an unfinished run. */
export function exitQuestion(skill: string, current: number, steps: number, verb: string): string {
  return `${skill} run is at step ${current} of ${steps} and unfinished. ${verb} anyway?`
}

/** BEH-28's text when the command is kept. */
export function keptText(skill: string, current: number): string {
  return `Kept working: the ${skill} run is still at step ${current}.`
}

/** BEH-28's question while runs are paused beneath the open one (version 14): a paused run is unfinished, so it asks
 *  whatever the open run's state, naming the run just beneath. `s` is the open run's summary, null with no state yet. */
export function nestedExitQuestion(open: string, s: { current: number | null; steps: number; ended: string | null } | null,
  b: { skill: string; step: number }, more: number, verb: string): string {
  const where = s === null ? 'has just started'
    : s.current === null || s.ended !== null ? 'is done' : `is at step ${s.current} of ${s.steps} and unfinished`
  return `${open} run ${where} (${b.skill} paused at step ${b.step}${more > 0 ? `, ${more} more paused` : ''}). ${verb} anyway?`
}

/** BEH-28's text when the command is kept while runs are paused (version 14). */
export function nestedKeptText(open: string, b: { skill: string; step: number }): string {
  return `Kept working: the ${open} run goes on, and ${b.skill} is still paused at step ${b.step}.`
}

/** Whether a rejected $.ui.ask was the user's dismissal (Esc), as opposed to a dialog that couldn't be shown (ERR-16). */
export function isDismissal(err: unknown): boolean {
  const text = err instanceof Error ? err.message : String(err)
  return /doesn't want to proceed/.test(text)
}

/** A paused run as the status line and the band name it (BEH-10, BEH-11; version 14): its skill, its return step, and
 *  the number of steps of its saved summary, if it had one. */
export type Beneath = { skill: string; step: number; summary: { steps: number } | null }

/** The status line's text (BEH-10), or undefined when there is nothing to show; `trail`, the paused runs, bottom first. */
export function statusText(summary: ProgressSummary | null, mode: ProgressMode, idle: boolean, off: string | null,
  trail: readonly Beneath[] = []): string | undefined {
  if (off !== null) return `progress: off (${off})`
  if (summary === null) return undefined
  const stoppedAt = stopStep(summary)
  let text = stoppedAt !== null
    ? `${summary.skill} stopped at step ${stoppedAt}`
    : summary.ended !== null
    ? `${summary.skill} ended`
    : summary.current === null ? `${summary.skill} done` : `${summary.skill} ${summary.current}/${summary.steps}`
  const b = trail[trail.length - 1]
  if (b !== undefined) {
    text += ` · in ${b.skill} ${b.step}${b.summary !== null ? `/${b.summary.steps}` : ''}`
    if (trail.length > 1) text += ` · ${trail.length - 1} more`
  }
  if (summary.yourTurn && summary.ended === null) text += ' · your turn'
  if (summary.flags > 0) text += ` · ${summary.flags} ${summary.flags === 1 ? 'flag' : 'flags'}`
  if (summary.manifest === 'stale' || summary.manifest === 'none') text += ' · ticks only'
  if (idle && summary.ended === null) text += ' · idle'
  if (mode === 'enforce') text += ' · enforce'
  return text
}

const GLYPH: Record<string, string> = {
  done: '●', current: '◆', 'your-turn': '?', pending: '○', claimed: '◐', unconfirmed: '·',
  'skipped-with-reason': '⊘', 'not-applicable': '–', skipped: '✗', 'rule-broken': '✗', carried: '◉',
}

/** Cut a row to width characters. */
export function fit(text: string, width: number): string {
  const chars = Array.from(text)
  if (chars.length <= width) return text
  return width <= 1 ? chars.slice(0, Math.max(0, width)).join('') : chars.slice(0, width - 1).join('') + '…'
}

/** The band's two rows of text (BEH-11); the button sits on row 2 between the mode and the flag. Row 1 names the run
 *  paused just beneath, if any (version 14). */
export function bandRows(summary: ProgressSummary, mode: ProgressMode, trail: readonly Beneath[] = []) {
  const glyphs = summary.states.map(s => GLYPH[s] ?? '○').join('')
  const stoppedAt = stopStep(summary)
  const where = stoppedAt !== null
    ? `stopped at step ${stoppedAt}`
    : summary.ended !== null
    ? `ended (${summary.ended})`
    : summary.current === null
      ? `all ${summary.steps} steps reached`
      : `step ${summary.current} of ${summary.steps}: ${summary.currentTitle ?? ''}`
  return {
    row1: `${summary.skill}  ${glyphs}  ${where}${pausedPart(trail)}`,
    mode: mode === 'enforce' ? 'enforce mode' : 'observe mode',
    button: mode === 'enforce' ? 'Switch to observe' : 'Switch to enforce',
    flag: summary.lastFlag ?? 'no flags',
  }
}

function pausedPart(trail: readonly Beneath[]): string {
  const b = trail[trail.length - 1]
  return b === undefined ? '' : ` (paused: ${b.skill} at step ${b.step}${trail.length > 1 ? `, ${trail.length - 1} more` : ''})`
}

/** A flag's identity, so each is shown once (BEH-12). */
export function flagKey(f: StateFlag): string {
  return `${f.step}:${f.type}:${f.seq}`
}

/** Flags not shown yet, and the toast text of each (BEH-12). */
export function newFlagToasts(state: ProgressState, shown: readonly string[], lines: readonly string[] | null = null): { keys: string[]; toasts: string[] } {
  const fresh = state.flags.filter(f => !shown.includes(flagKey(f)))
  return {
    keys: fresh.map(flagKey),
    // Written for the user (BEH-12, version 8): a decision whose typed answers went to another marked step says so,
    // and a question gate's answer counted for nothing. `lines` is the run's, when it follows the task list.
    toasts: fresh.map(f => {
      const typed = lines === null ? null : typedTo(state, f, lines)
      return `✗ Step ${f.step} ${f.type}: ${f.message}` + (typed ? ' ' + typed : '')
        + (QUESTION_GATES.includes(f.type) ? ' Its answer, if any, counts for no step.' : '')
    }),
  }
}

/** The refusal text at the write gate (BEH-08), or null when the provisional state doesn't refuse at seq. It names
 *  what clears each flag: a step's own evidence or a tick in reply text, or for a decision the user's answer (the
 *  VER-15 dogfood run showed a refusal that only said "the user decides" sent Claude into the tracker's code). */
export function refusalText(state: ProgressState, seq: number, runLines: readonly string[] | null = null): string | null {
  const g = state.gate
  if (g.kind !== 'write' || g.seq !== seq || !g.refuse) return null
  const flags = state.flags.filter(f => f.seq === seq)
  const owned = new Set(state.steps.filter(s => s.userOwned).map(s => s.n))
  const decisions = flags.filter(f => f.type === 'rule-broken' || owned.has(f.step))
  const steps = flags.filter(f => f.type !== 'rule-broken' && !owned.has(f.step)).map(f => f.step)
  const said = ["DevForgeAI's progress tracker refused this write at the write gate (enforce mode):", ...flags.map(f => `- ${f.message}`)]
  if (steps.length) {
    const list = [...new Set(steps)].join(', ')
    said.push(`To clear step ${list}: do the step with a tool call the run log can see (Read the files it names), `
      + `or, if you did it, tick it as \`- [x] N.\` in your reply text. A tick only in your thinking doesn't count.`)
  }
  if (decisions.length) {
    said.push('The decisions at step ' + [...new Set(decisions.map(f => f.step))].join(', ')
      + " are the user's: ask the user, or leave those fields open.")
  }
  // How a decision's answer counts, whichever step the task list marks (BEH-08, version 8): `runLines` is the run's
  // lines, when it follows the task list.
  if (runLines !== null) said.push(...decisionLines(state, flags, runLines))
  said.push('Then write again.' + (state.run ? ` The run's log and state are in devforgeai/progress/runs/${state.run}/.` : ''))
  return said.join('\n')
}

/** The report gate's flags for the model (BEH-09), or null when there are none to give. */
export function reportContext(state: ProgressState): { seq: number; text: string } | null {
  const g = state.gate
  if (g.kind !== 'report' || !g.refuse || g.seq === null) return null
  const flags = state.flags.filter(f => f.seq === g.seq).map(f => `- ${f.message}`)
  return {
    seq: g.seq,
    text: [`DevForgeAI's progress tracker (enforce mode) found these at the ${state.skill} run's report:`, ...flags].join('\n'),
  }
}

/** The final evaluation's timeout at session end, from what the shared 1.5-second budget leaves, or null when
 *  there is no room for it (BEH-05): the run-end line is written first, and the log alone reproduces the state. */
export function finalTimeout(remainingMs: number): number | null {
  const timeout = Math.floor(remainingMs) - END_RESERVE_MS
  return timeout >= 200 ? timeout : null
}

/** What session.end keeps for Claude Code's own work after the adapter's (BEH-05). */
export const END_RESERVE_MS = 300

/** Whether the session.end budget left has room for one more run-end (BEH-05, version 14). */
export function hasRoom(remainingMs: number): boolean {
  return remainingMs >= END_RESERVE_MS
}

/** The retention period in days from the retentionDays setting (DM-06): 7 to 3650, else 30. Claude Code already
 *  refuses to load the module when a stored value is out of range; this is the second guard, since the floor is
 *  what protects another, idle session's open run (BEH-19). */
export function retentionOf(value: unknown): number {
  const days = Number(value)
  return Number.isInteger(days) && days >= 7 && days <= 3650 ? days : 30
}

// ---- the task list (SPEC-013 v4 and v5; SPEC-012 §4) ----

/** The convention's tag: a skill whose text names it keeps its checklist in the task list (SPEC-012 §4). */
export const TASK_TAG = 'devforgeai_step'

/** Whether the session has a task list: TaskCreate and TaskUpdate, or TodoWrite (DM-01). TaskStop stops background
 *  tasks and isn't one; a model that doesn't get the task tools by default has none without the user's opt-in. */
export function hasTaskList(names: readonly string[]): boolean {
  return (names.includes('TaskCreate') && names.includes('TaskUpdate')) || names.includes('TodoWrite')
}

/** Whether a run follows the task list, from its skill-loaded line: taskList true and the tag in the skill's text
 *  (SPEC-012 BEH-18). */
export function followsTaskList(line: string | undefined): boolean {
  if (!line) return false
  try {
    const e = JSON.parse(line) as Fields
    return e.taskList === true && typeof e.checklist === 'string' && e.checklist.includes(TASK_TAG)
  } catch {
    return false
  }
}

/** A TaskCreate's task ID, from its result text 'Task #<id> created successfully' (BEH-20, ERR-13). */
export function taskIdOf(text: unknown): string | null {
  if (typeof text !== 'string') return null
  const m = text.match(/Task #([^\s:]+) created successfully/)
  return m ? m[1] : null
}

/** A task's step: its metadata devforgeai_step when that is a whole number, else the number its subject starts
 *  with ('<N>. <title>'), else null (BEH-20, ERR-13). */
export function stepOfTask(input: Fields): number | null {
  const meta = input.metadata && typeof input.metadata === 'object' ? (input.metadata as Fields)[TASK_TAG] : undefined
  if (typeof meta === 'number' && Number.isInteger(meta) && meta >= 1) return meta
  const m = typeof input.subject === 'string' ? input.subject.match(/^\s*(\d+)\./) : null
  return m && Number(m[1]) >= 1 ? Number(m[1]) : null
}

/** A TaskUpdate's status as a step event's state: in_progress starts the step, completed ends it (BEH-20). */
export function stepStateOf(status: unknown): 'started' | 'done' | null {
  return status === 'in_progress' ? 'started' : status === 'completed' ? 'done' : null
}

/** A TodoWrite's step events and the statuses to keep (BEH-20): each '<N>.' todo is compared with its own entry in
 *  the list the call replaced (the result's oldTodos: the same content at the same place, else the first unused entry
 *  with that content), or with the kept statuses when the result has none, so an earlier run's completed todos left in
 *  the list, even beside the new run's of the same numbers, claim nothing. Becoming in_progress starts a step,
 *  becoming completed ends it; straight from pending to completed gives done only. */
export function todoSteps(todos: unknown, last: Readonly<Record<string, string>>, oldTodos?: unknown): {
  events: Array<{ step: number; state: 'started' | 'done' }>
  statuses: Record<string, string>
} {
  const old = Array.isArray(oldTodos) ? (oldTodos as unknown[]) : null
  const used = new Set<number>()
  const contentOf = (x: unknown) => (x && typeof x === 'object' ? (x as Fields).content : undefined)
  const statuses: Record<string, string> = { ...last }
  const events: Array<{ step: number; state: 'started' | 'done' }> = []
  if (!Array.isArray(todos)) return { events, statuses }
  todos.forEach((todo, i) => {
    if (!todo || typeof todo !== 'object') return
    const { content, status } = todo as Fields
    const m = typeof content === 'string' ? content.match(/^\s*(\d+)\./) : null
    if (!m || typeof status !== 'string' || Number(m[1]) < 1) return
    const step = Number(m[1])
    let before: unknown
    if (old !== null) {
      const j = !used.has(i) && contentOf(old[i]) === content ? i : old.findIndex((o, k) => !used.has(k) && contentOf(o) === content)
      if (j >= 0) used.add(j)
      before = j >= 0 ? (old[j] as Fields).status : undefined
    } else {
      before = statuses[String(step)]
    }
    if (status === 'in_progress' && before !== 'in_progress') events.push({ step, state: 'started' })
    if (status === 'completed' && before !== 'completed') events.push({ step, state: 'done' })
    statuses[String(step)] = status
  })
  return { events, statuses }
}

/** The refusal of a question asked with no step in progress (BEH-21), with how to recover. */
export const QUESTION_REFUSAL = "DevForgeAI's progress tracker refused this question (enforce mode): no step of this run "
  + "is marked in progress in your task list. Tasks from an earlier run don't count: if this run's checklist isn't in "
  + 'your task list yet, turn it into tasks first as the skill says (one task per step, subject <N>. <title>, metadata '
  + 'devforgeai_step: N). Then mark the step this question belongs to in_progress (TaskUpdate, or TodoWrite), and ask '
  + 'again.'

/** What an unmarked question with no step tag is also told (BEH-21, version 8). */
export const QUESTION_TAG = ' Tag the question too: add metadata: {"source": "devforgeai_step:N"} to the AskUserQuestion '
  + "call, N being its step. If the question isn't part of this skill's checklist, give it a source of its own instead; "
  + 'it then needs no step and counts for none.'

/** SPEC-012's question-gate flag types (version 9). */
export const QUESTION_GATES = ['unmarked-question', 'untagged-question', 'mismatched-question']

/** The question refusal when the provisional state's question gate refuses at seq, else null (BEH-21). The text follows
 *  the type of the gate's flag, never its message: `marked` is the step the task list marks, `tagged` whether the
 *  question names a step (version 8). */
export function questionRefusal(state: ProgressState, seq: number, marked: number | null = null, tagged = false): string | null {
  const g = state.gate
  if (g.kind !== 'question' || g.seq !== seq || !g.refuse) return null
  const flag = state.flags.find(f => f.gate === 'question' && f.seq === seq)
  const head = "DevForgeAI's progress tracker refused this question (enforce mode): "
  if (flag?.type === 'mismatched-question') {
    const n = flag.step
    const k = marked ?? n
    return head + `it is tagged for step ${n}, but your task list marks step ${k} in progress. If the question belongs `
      + `to step ${n}, mark step ${n} in_progress (TaskUpdate, or TodoWrite) and ask again; if it belongs to step ${k}, `
      + `tag it devforgeai_step:${k} and ask again.`
  }
  if (flag?.type === 'untagged-question') {
    return head + "it doesn't name a step of this skill's checklist. Add metadata: {\"source\": \"devforgeai_step:N\"} to "
      + `the AskUserQuestion call, N being the step it belongs to; your task list marks step ${marked ?? flag.step} in `
      + 'progress, so if the question belongs to another step, mark that step in_progress first. If the question '
      + "isn't part of this skill's checklist, give it a source of its own instead; it then counts for no step. Then ask "
      + 'again.'
  }
  return QUESTION_REFUSAL + (tagged ? '' : QUESTION_TAG)
}

/** The waiver question's own tag (DM-01, version 10). */
export const WAIVER_TAG = 'devforgeai_waiver'
const WAIVER_LABELS: Record<string, 'proceed' | 'ask'> = { 'Proceed without questions': 'proceed', 'Ask me as usual': 'ask' }

function sourceOf(input: Fields): unknown {
  const meta = input.metadata
  return meta !== null && typeof meta === 'object' ? (meta as Fields).source : undefined
}

/** The waiver question (DM-01, version 10): source exactly devforgeai_waiver, in a call that asks exactly one
 *  question. Never checked at the question gate (BEH-21). */
export function isWaiverQuestion(input: Fields): boolean {
  return sourceOf(input) === WAIVER_TAG && Array.isArray(input.questions) && input.questions.length === 1
}

/** Which fixed label a waiver question's answer picked: proceed, ask, or other for anything typed, any other text and
 *  a dismissal; a typed answer equal to a label is that label, since the result can't tell them apart (DM-01). */
export function waiverAnswer(input: Fields, outcome: ToolOutcome): 'proceed' | 'ask' | 'other' {
  if (!isAnswered(outcome)) return 'other'
  const question = (input.questions as Fields[])[0]?.question
  const answers = (outcome.result as { answers?: Record<string, unknown> }).answers ?? {}
  const answer = typeof question === 'string' ? answers[question] : undefined
  return typeof answer === 'string' && Object.hasOwn(WAIVER_LABELS, answer) ? WAIVER_LABELS[answer] : 'other'
}

/** A question's step tag from its input's metadata.source (DM-01, version 8): `step` for devforgeai_step:N, `outside`
 *  for a source naming something else, nothing for no source or a malformed tag. The waiver source with more than one
 *  question is `outside` too, so its questions can't take the waiver's exemption (version 10). */
export function questionTag(input: Fields): { step?: number; outside?: true } {
  const source = sourceOf(input)
  if (typeof source !== 'string') return {}
  const m = /^devforgeai_step:([1-9][0-9]*)$/.exec(source)
  if (m) return { step: Number(m[1]) }
  return source.startsWith(TASK_TAG) ? {} : { outside: true }
}

/** The adherence notice for a run that follows the task list, once it ends or reaches its report gate with no step
 *  event or an unmarked question (BEH-22), else null; a state without the counts says nothing. The report step's own
 *  state shows the report was reached even after a later event moved the gate on. */
export function adherenceText(state: ProgressState): string | null {
  const reported = state.gate.kind === 'report'
    || state.steps.some(s => s.kind === 'report' && (s.state === 'done' || s.state === 'claimed'))
  if (state.ended === null && !reported) return null
  const n = state.counts?.stepEvents
  const m = state.counts?.unmarkedQuestions
  if (typeof n !== 'number' || typeof m !== 'number' || (n > 0 && m === 0)) return null
  return `${state.skill} didn't keep its task list: ${n} step events, ${m} questions asked without their step marked and tagged. `
    + 'Recommended: fix the skill so it keeps its checklist in the task list (DevForgeAI SPEC-012 §4)'
}

/** The once-per-session hint for a session with no task tools (BEH-23). */
export function hintText(skill: string): string {
  return `${skill}: this session has no task list, so DevForgeAI places your answers by guessing. For exact step `
    + 'tracking, start Claude Code with CLAUDE_CODE_ENABLE_TODO_TOOLS=1 (DevForgeAI SPEC-012 §4)'
}

// ---- the task list's mark (SPEC-013 v7 and v8) ----

function parsed(lines: readonly string[]): Fields[] {
  const out: Fields[] = []
  for (const line of lines) {
    try {
      out.push(JSON.parse(line) as Fields)
    } catch {
      // a line that isn't JSON says nothing about the mark
    }
  }
  return out
}

/** The step the task list marks in progress, from a run's event lines before seq `upto`: the step whose latest step
 *  event is started, the latest started when several are (SPEC-012 BEH-18); null when none is. With `steps`, the step
 *  events naming a step the state doesn't have are left out first, as the evaluator leaves them out (SPEC-012 ERR-06),
 *  so the two agree on the mark (BEH-24, version 8). */
export function markedStep(lines: readonly string[], upto = Infinity, steps: readonly StateStep[] | null = null): number | null {
  const known = steps === null ? null : new Set(steps.map(s => s.n))
  const latest = new Map<number, { state: unknown; seq: number }>()
  for (const e of parsed(lines)) {
    if (typeof e.seq !== 'number' || e.seq >= upto) continue
    if (e.kind === 'step' && typeof e.step === 'number' && (known === null || known.has(e.step))) {
      latest.set(e.step, { state: e.state, seq: e.seq })
    }
  }
  let best: { n: number; seq: number } | null = null
  for (const [n, v] of latest) if (v.state === 'started' && (best === null || v.seq > best.seq)) best = { n, seq: v.seq }
  return best === null ? null : best.n
}

/** Whether the user typed a prompt after step n's latest started event and before seq `upto` (BEH-08, BEH-12). */
export function typedSince(lines: readonly string[], n: number, upto = Infinity): boolean {
  const events = parsed(lines).filter(e => typeof e.seq === 'number' && e.seq < upto)
  const starts = events.filter(e => e.kind === 'step' && e.step === n && e.state === 'started').map(e => e.seq as number)
  if (!starts.length) return false
  const from = Math.max(...starts)
  return events.some(e => e.kind === 'prompt' && (e.seq as number) > from)
}

/** 'step N (<title>)', or 'step N' when the state has no title for it. */
export function stepLabel(steps: readonly StateStep[], n: number): string {
  const s = steps.find(x => x.n === n)
  return s ? `step ${n} (${s.title})` : `step ${n}`
}

/** The first skipped flag for a user-owned step among flags: the decision's step, from the flag's step and the state's
 *  userOwned, never from message text (BEH-08, BEH-12). */
function decisionFlag(state: ProgressState, flags: readonly StateFlag[]): StateFlag | null {
  const owned = new Set(state.steps.filter(s => s.userOwned).map(s => s.n))
  return flags.find(f => f.type === 'skipped' && owned.has(f.step)) ?? null
}

/** The write refusal's lines for a decision (BEH-08, version 8): how step M's answer counts, whichever step is marked,
 *  and before it, when another marked step N took what the user typed, that step; none when step M itself is marked. */
export function decisionLines(state: ProgressState, flags: readonly StateFlag[], lines: readonly string[]): string[] {
  const flag = decisionFlag(state, flags)
  if (flag === null) return []
  const m = flag.step
  const n = markedStep(lines, Infinity, state.steps)
  if (n === m) return []
  const label = stepLabel(state.steps, m)
  const out: string[] = []
  if (n !== null && typedSince(lines, n)) {
    out.push(`Your task list marks ${stepLabel(state.steps, n)} in progress, so what the user typed since then counted for step ${n}.`)
  }
  out.push(`${label[0].toUpperCase()}${label.slice(1)} is the user's decision: an answer counts for it only while step ${m} `
    + `is marked in progress, and an answer to a question only when the question is also tagged devforgeai_step:${m}. `
    + `Mark step ${m} in_progress, ask the user with the question tagged devforgeai_step:${m}, and mark step ${m} completed.`)
  return out
}

/** The user's sentence on a decision's flag toast (BEH-12, version 8), judged at the flag's seq: another marked step N
 *  took what the user typed; null otherwise. */
function typedTo(state: ProgressState, flag: StateFlag, lines: readonly string[]): string | null {
  if (decisionFlag(state, [flag]) === null) return null
  const n = markedStep(lines, flag.seq, state.steps)
  if (n === null || n === flag.step || !typedSince(lines, n, flag.seq)) return null
  return `What you typed since ${stepLabel(state.steps, n)} was marked in progress counted for step ${n}: the `
    + `${state.skill} skill didn't keep its task list in step with its work (DevForgeAI SPEC-012 §4).`
}

/** The cause of a refusal, for the stuck notice (BEH-25, versions 8 and 9): the gate's kind and the first flag raised
 *  at seq, with that flag's type and whether its step is user-owned in the state's steps (a step it doesn't list isn't). */
export function refusalCause(state: ProgressState, seq: number):
  { key: string; step: number; message: string; type: string; userOwned: boolean } | null {
  const flag = state.flags.find(f => f.seq === seq)
  if (flag === undefined || state.gate.kind === null) return null
  const userOwned = state.steps.some(s => s.n === flag.step && s.userOwned === true)
  return { key: `${state.gate.kind}:${flag.type}:${flag.step}`, step: flag.step, message: flag.message, type: flag.type,
    userOwned }
}

/** One refusal kept for the run's review (BEH-25, BEH-26; version 10). */
export type Refused = ProgressRefused

/** One review item: a cause (the gate's kind, the flag's type and step) with its first message and its number of
 *  refusals, 0 for a flag no refusal has (BEH-26). */
export type ReviewItem = { gate: string; seq: number; step: number; type: string; message: string; count: number }

/** The run's review items, one per cause: the refusals' causes in the order of their first refusal, then the flags'
 *  causes no refusal has, in the order of their first flag (BEH-26). */
export function reviewItems(refused: readonly Refused[], flags: readonly StateFlag[]): ReviewItem[] {
  const items: ReviewItem[] = []
  const byKey = new Map<string, ReviewItem>()
  const key = (x: { gate: string; type: string; step: number }) => `${x.gate}:${x.type}:${x.step}`
  for (const r of refused) {
    const k = key(r)
    const item = byKey.get(k)
    if (item) item.count += 1
    else {
      const fresh = { gate: r.gate, seq: r.seq, step: r.step, type: r.type, message: r.message, count: 1 }
      byKey.set(k, fresh)
      items.push(fresh)
    }
  }
  for (const f of [...flags].sort((a, b) => a.seq - b.seq)) {
    const k = key(f)
    if (byKey.has(k)) continue
    const fresh = { gate: f.gate, seq: f.seq, step: f.step, type: f.type, message: f.message, count: 0 }
    byKey.set(k, fresh)
    items.push(fresh)
  }
  return items
}

/** A review item's question (BEH-26). */
export function reviewQuestion(skill: string, i: number, n: number, item: ReviewItem): string {
  const what = item.count > 0 ? `refused ${item.count} time(s)` : 'flagged'
  return `${skill} run, item ${i} of ${n}: ${what} at step ${item.step} (${item.gate} gate): ${item.message}. `
    + 'Accept it, or challenge it?'
}

/** The question gate's flag types (SPEC-012 BEH-08), whose stuck notice keeps the task-list advice. */
const QUESTION_GATE_TYPES = new Set(['unmarked-question', 'untagged-question', 'mismatched-question'])

/** The stuck notice's last sentence (BEH-25, version 9), chosen by the refused flag's type and whether its step is
 *  user-owned, never by message text: the task list for a question gate, the decision for a user-owned step's skipped
 *  flag or a rule-broken one, and otherwise the step's evidence. */
export function stuckAdvice(type: string, userOwned: boolean): string {
  if (QUESTION_GATE_TYPES.has(type)) {
    return "Help Claude bring its task list in step, or switch to observe mode with the band's button."
  }
  if (type === 'rule-broken' || (type === 'skipped' && userOwned)) {
    return "The refused write records a decision that needs your answer: answer Claude's question about it, or ask "
      + "Claude to leave it open, or switch to observe mode with the band's button."
  }
  return "Claude hasn't done that step in a way the tracker can see: ask Claude to do it as the message says, or "
    + "switch to observe mode with the band's button."
}

/** The notice for the user when the same refusal comes twice in a run (BEH-25, versions 8 and 9). */
export function stuckText(skill: string, step: number, message: string, advice: string): string {
  return `${skill}: the progress tracker refused Claude twice at step ${step} for the same reason: ${message}. ${advice}`
}

/** The start of the note a compaction ends with (BEH-24), by which an earlier one is found and removed (version 8). */
export const NOTE_START = "DevForgeAI's progress tracker: when this conversation was compacted"

/** What a compaction keeps and the note it ends with (BEH-24); `label` is 'step N (<title>)', or null for none. */
export function compactTexts(skill: string, label: string | null): { instruction: string; note: string } {
  const marked = label ?? 'no step'
  return {
    instruction: `Keep, for DevForgeAI's progress tracker: in the ${skill} run, the task list marks ${marked} in progress.`,
    note: `DevForgeAI's progress tracker: when this conversation was compacted, your task list marked ${marked} in `
      + "progress. Before you ask anything or go on, check your task list and bring it in step with the work: mark each "
      + "finished step done and the step you're on in_progress.",
  }
}

// ---- the trail of paused runs (SPEC-013 BEH-29, BEH-30; version 13, paused and resumed from version 14) ----

/** A trail entry as the compaction note names it. */
export type TrailEntry = { skill: string; step: number }

/** The line added to a skill Claude loads mid-run (BEH-29, version 14). */
export function returnLine(skill: string, step: number): string {
  return `This skill was loaded by ${skill} at step ${step}. When this skill's work is done, mark ${skill}'s step ${step} task in progress again and continue ${skill} at step ${step}.`
}

export const TRAIL_NOTE_START = 'Return points (from the progress tracker):'

/** The compaction note naming the whole trail, top first (BEH-29). */
export function trailNote(open: string, trail: readonly TrailEntry[]): string {
  const parts = [...trail].reverse().map((t, i) => `${i === 0 ? 'continue' : 'then'} ${t.skill} at step ${t.step}`)
  return `${TRAIL_NOTE_START} when ${open} is done, ${parts.join('; ')}.`
}

/** The index of the topmost paused run whose task IDs hold a TaskUpdate's task ID, or -1 (BEH-30 (a), version 14):
 *  whatever the update's status, Claude has gone back to that skill. */
export function pausedWith(trail: readonly { tasks: Record<string, number> }[], taskId: unknown): number {
  if (typeof taskId !== 'string') return -1
  for (let i = trail.length - 1; i >= 0; i--) if (Object.hasOwn(trail[i].tasks, taskId)) return i
  return -1
}

/** The trail as $.state gives it back after a load (BEH-30): an entry without its run (version 13's shape) is dropped. */
export function keptTrail(raw: unknown): ProgressPaused[] {
  if (!Array.isArray(raw)) return []
  return raw.filter((t): t is ProgressPaused => t !== null && typeof t === 'object' && typeof t.skill === 'string'
    && typeof t.step === 'number' && t.tasks !== null && typeof t.tasks === 'object'
    && t.run !== null && typeof t.run === 'object' && typeof t.run.id === 'string' && typeof t.run.dir === 'string')
}

/** The reason of a run's run-end in its log, or null when it hasn't ended (BEH-05). */
export function endReason(lines: readonly string[]): string | null {
  for (const line of lines) {
    if (!line.includes('"kind":"run-end"')) continue
    try {
      const reason = (JSON.parse(line) as Fields).reason
      return typeof reason === 'string' ? reason : null
    } catch {
      return null
    }
  }
  return null
}

// ---- the offer to continue an earlier run (SPEC-013 BEH-31, version 16) ----

/** What a run-end's reason reads as in the offer (BEH-31). */
const WHY: Record<string, string> = {
  'session-end': 'session end', clear: '/clear', stopped: 'stopped', 'another-skill': 'another skill loaded',
  returned: 'returned to the skill beneath',
}

/** An earlier run's offer: the step to continue at, the steps carried, the user's decisions that stand (answered) and
 *  those to confirm again (owned), the files it wrote, and how it ended (`when`). */
export type ResumePlan = {
  run: string; step: number; steps: number; carried: number[]; answered: number[]; owned: number[]; files: string[]
  when: string
}

/** A step is reached when it has evidence other than waiver evidence, or a done claim (BEH-31; SPEC-012 BEH-07). */
function reachedStep(s: StateStep): boolean {
  return (s.evidence ?? []).some(x => x.type !== 'waiver') || s.claim?.state === 'done'
}

/** An age as the offer says it: minutes, hours or days. */
export function ageText(ms: number): string {
  if (!Number.isFinite(ms)) return 'an unknown time'
  const minutes = Math.max(0, Math.floor(ms / 60000))
  if (minutes < 60) return `${minutes} ${minutes === 1 ? 'minute' : 'minutes'}`
  const hours = Math.floor(minutes / 60)
  if (hours < 48) return `${hours} ${hours === 1 ? 'hour' : 'hours'}`
  const days = Math.floor(hours / 24)
  return `${days} ${days === 1 ? 'day' : 'days'}`
}

/** Steps as the offer names them: '1, 2, 3'. */
export function stepList(ns: readonly number[]): string {
  return ns.join(', ')
}

/** The offer for an earlier run, from its state evaluated once more and its log, or null when it isn't offered: its
 *  manifest isn't matched, its last step is reached (unless it ended stopped), or nothing would be carried (BEH-31).
 *  `writeGate` is the number of the step with the write gate, `now` the time in ms. */
export function resumePlan(run: string, state: ProgressState, lines: readonly string[], writeGate: number | null,
  now: number): ResumePlan | null {
  if (state.manifest?.state !== 'matched') return null
  const steps = state.steps
  if (!steps.length) return null
  if (reachedStep(steps[steps.length - 1]) && state.ended !== 'stopped') return null
  const reached = steps.filter(reachedStep).map(s => s.n)
  const highest = reached.length ? Math.max(...reached) : null
  let step = markedStep(lines, Infinity, steps)
    ?? (highest === null ? steps[0].n : (steps.find(s => s.n > highest)?.n ?? steps[steps.length - 1].n))
  // Never past the first step with the write gate that has no write evidence: its document was never written. A write
  // step carried from a run before counts as written there (review S1).
  const gate = writeGate === null ? undefined : steps.find(s => s.n === writeGate)
  const wrote = gate !== undefined && (gate.evidence ?? []).some(x => x.type === 'write' || x.type === 'carried')
  if (gate !== undefined && gate.n < step && !wrote) step = gate.n
  const carried = steps.filter(s => s.n < step).map(s => s.n)
  if (!carried.length) return null
  // The decisions that stand: written under the write gate (not a rule-broken write), each answered and not skipped
  // there, in this run or, carried, in the run it continued (review S1, S2).
  const written = gate !== undefined && carried.includes(gate.n) && gate.state !== 'rule-broken'
  let before: number[] = []
  try {
    const first = JSON.parse(lines[0] ?? '{}') as Fields
    if (Array.isArray(first.answered)) before = first.answered.filter((n): n is number => typeof n === 'number')
  } catch {
    // no earlier answers
  }
  const owned = steps.filter(s => s.n < step && s.userOwned === true)
  const answered = written
    ? owned.filter(s => s.state !== 'skipped' && ((s.evidence ?? []).some(x => x.type === 'answer') || before.includes(s.n))).map(s => s.n)
    : []
  const files: string[] = []
  let ended: string | null = null
  let lastTime: string | null = null
  for (const line of lines) {
    let e: Fields
    try {
      e = JSON.parse(line) as Fields
    } catch {
      continue
    }
    if (typeof e.time === 'string') lastTime = e.time
    if (e.kind === 'run-end' && typeof e.reason === 'string' && ended === null) ended = e.reason
    // A path is shown in the dialog and Claude's text: one line of it (review note).
    const path = typeof e.path === 'string' ? e.path.replace(/[\u0000-\u001f\u007f]+/g, ' ') : null
    if (e.kind === 'tool' && (e.tool === 'Write' || e.tool === 'Edit') && e.error !== true && path !== null
      && !files.includes(path)) files.push(path)
  }
  const of = `step ${step} of ${steps.length}`
  const when = ended !== null
    ? `ended at ${of} on ${(lastTime ?? '').slice(0, 10)} (${WHY[ended] ?? ended})`
    : `was at ${of} with no end recorded, its last event ${ageText(now - Date.parse(lastTime ?? ''))} ago (it may still be open in another session)`
  return { run, step, steps: steps.length, carried, answered, owned: owned.map(s => s.n).filter(n => !answered.includes(n)),
    files, when }
}

/** BEH-31's question. */
export function resumeQuestion(skill: string, plan: ResumePlan): string {
  return `${skill}: an earlier run ${plan.when}. It wrote ${plan.files.length ? plan.files.join(', ') : 'nothing'}. Continue it?`
}

/** BEH-31's line at the end of the text Claude reads. */
export function resumeLine(skill: string, plan: ResumePlan): string {
  const owned = plan.owned.length
    ? ` Steps ${stepList(plan.owned)} were the user's decisions, which the record doesn't keep: before any document records them, confirm each with the user again, in order, marking its step in progress and tagging the question with it.`
    : ''
  return `This run continues the earlier ${skill} run ${plan.run}, which ${plan.when}. Steps ${stepList(plan.carried)} are `
    + `carried over: the tracker counts them reached. Create the task list with those steps' tasks completed, mark step `
    + `${plan.step} in progress, and continue at step ${plan.step}.${owned} Files it wrote: `
    + `${plan.files.length ? plan.files.join(', ') : 'nothing'}. Its replies are in devforgeai/progress/runs/${plan.run}/`
    + `events.jsonl, the events of kind reply: use them to show the user what was proposed, never as a decision.`
}

// ---- The work files' cleanup (BEH-32, IF-05; version 20) ----

/** A run ID as run folders are named (SPEC-012's pattern): the only shape the adapter lets into a path. */
const RUN_ID = /^[0-9]{8}T[0-9]{6}Z-[a-z][a-z0-9-]*-[0-9a-f]{8}$/

/** Whether an evaluation says the run's work files are due (SPEC-012 BEH-21: workFiles.due is true). */
export function workFilesDue(state: ProgressState): boolean {
  const w = state.workFiles
  return typeof w === 'object' && w !== null && !Array.isArray(w) && w.due === true
}

/** The paths of a state's workFiles.files that the adapter passes on: the non-empty strings and nothing else, in order.
 *  A state.json is a file the model's tools can write, so whatever isn't a list gives none; prune.py judges the paths
 *  themselves (ERR-20). */
export function workFilePaths(state: unknown): string[] {
  if (typeof state !== 'object' || state === null || Array.isArray(state)) return []
  const w = (state as { workFiles?: unknown }).workFiles
  if (typeof w !== 'object' || w === null || Array.isArray(w)) return []
  const files = (w as { files?: unknown }).files
  return Array.isArray(files) ? files.filter((f): f is string => typeof f === 'string' && f !== '') : []
}

/** Why a continued run's state.json gives no work files, or null when it names a workFiles object (ERR-19). */
export function workFilesProblem(state: unknown): string | null {
  if (typeof state !== 'object' || state === null || Array.isArray(state)) return 'its state is not an object'
  const w = (state as { workFiles?: unknown }).workFiles
  if (w === undefined) return 'its state has no workFiles'
  if (typeof w !== 'object' || w === null || Array.isArray(w)) return 'its workFiles is not an object'
  return null
}

/** IF-05's argv (BEH-32): every path once, in the order given across the lists, each as one --file=<path> token, so a
 *  path that begins with - is a value and never an option. */
export function removeArgv(python: string, plugin: string, root: string, ...lists: readonly (readonly string[])[]): string[] {
  const paths = [...new Set(lists.flat().filter(p => typeof p === 'string' && p !== ''))]
  return [python, `${plugin}/progress/prune.py`, 'remove', '--root', root, '--manifests', `${plugin}/progress/manifests`,
    ...paths.map(p => `--file=${p}`)]
}

/** The run a run's skill-loaded line says it continues (BEH-31), when it is shaped as a run ID. */
export function resumesOf(line: string | undefined): string | null {
  if (line === undefined) return null
  try {
    const v = (JSON.parse(line) as { resumes?: unknown }).resumes
    return typeof v === 'string' && RUN_ID.test(v) ? v : null
  } catch {
    return null
  }
}
