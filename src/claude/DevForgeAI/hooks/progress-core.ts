// Pure helpers of the progress tracker adapter (SPEC-013 v6). No `$` here: claude plugin validate lets `$` reach
// only top-level functions of hooks/progress.tsx, so this file turns plain data into plain data, and its tests
// (core.test.ts) call it directly.
import type { ProgressMode, ProgressSummary } from '../types'

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
  'skill-loaded': ['format', 'skill', 'checklist', 'host', 'taskList', 'mode', 'modeSource'],
  tool: ['tool', 'path', 'command', 'exit', 'error', 'content'],
  answer: ['answered'],
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
export function runId(ms: number, skill: string, random: Uint8Array): string {
  const t = isoTime(ms).replace(/[-:]/g, '')
  const name = skill.toLowerCase().replace(/[^a-z0-9-]+/g, '-').replace(/^[^a-z]+/, '') || 'skill'
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
export type StateStep = { n: number; title: string; state: string; userOwned?: boolean; kind?: string | null }
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

/** The status line's text (BEH-10), or undefined when there is nothing to show. */
export function statusText(summary: ProgressSummary | null, mode: ProgressMode, idle: boolean, off: string | null): string | undefined {
  if (off !== null) return `progress: off (${off})`
  if (summary === null) return undefined
  let text = summary.ended !== null
    ? `${summary.skill} ended`
    : summary.current === null ? `${summary.skill} done` : `${summary.skill} ${summary.current}/${summary.steps}`
  if (summary.yourTurn && summary.ended === null) text += ' · your turn'
  if (summary.flags > 0) text += ` · ${summary.flags} ${summary.flags === 1 ? 'flag' : 'flags'}`
  if (summary.manifest === 'stale' || summary.manifest === 'none') text += ' · ticks only'
  if (idle && summary.ended === null) text += ' · idle'
  if (mode === 'enforce') text += ' · enforce'
  return text
}

const GLYPH: Record<string, string> = {
  done: '●', current: '◆', 'your-turn': '?', pending: '○', claimed: '◐', unconfirmed: '·',
  'skipped-with-reason': '⊘', 'not-applicable': '–', skipped: '✗', 'rule-broken': '✗',
}

/** Cut a row to width characters. */
export function fit(text: string, width: number): string {
  const chars = Array.from(text)
  if (chars.length <= width) return text
  return width <= 1 ? chars.slice(0, Math.max(0, width)).join('') : chars.slice(0, width - 1).join('') + '…'
}

/** The band's two rows of text (BEH-11); the button sits on row 2 between the mode and the flag. */
export function bandRows(summary: ProgressSummary, mode: ProgressMode) {
  const glyphs = summary.states.map(s => GLYPH[s] ?? '○').join('')
  const where = summary.ended !== null
    ? `ended (${summary.ended})`
    : summary.current === null
      ? `all ${summary.steps} steps reached`
      : `step ${summary.current} of ${summary.steps}: ${summary.currentTitle ?? ''}`
  return {
    row1: `${summary.skill}  ${glyphs}  ${where}`,
    mode: mode === 'enforce' ? 'enforce mode' : 'observe mode',
    button: mode === 'enforce' ? 'Switch to observe' : 'Switch to enforce',
    flag: summary.lastFlag ?? 'no flags',
  }
}

/** A flag's identity, so each is shown once (BEH-12). */
export function flagKey(f: StateFlag): string {
  return `${f.step}:${f.type}:${f.seq}`
}

/** Flags not shown yet, and the toast text of each (BEH-12). */
export function newFlagToasts(state: ProgressState, shown: readonly string[]): { keys: string[]; toasts: string[] } {
  const fresh = state.flags.filter(f => !shown.includes(flagKey(f)))
  return { keys: fresh.map(flagKey), toasts: fresh.map(f => `✗ Step ${f.step} ${f.type}: ${f.message}`) }
}

/** The refusal text at the write gate (BEH-08), or null when the provisional state doesn't refuse at seq. It names
 *  what clears each flag: a step's own evidence or a tick in reply text, or for a decision the user's answer (the
 *  VER-15 dogfood run showed a refusal that only said "the user decides" sent Claude into the tracker's code). */
export function refusalText(state: ProgressState, seq: number): string | null {
  const g = state.gate
  if (g.kind !== 'write' || g.seq !== seq || !g.refuse) return null
  const flags = state.flags.filter(f => f.seq === seq)
  const owned = new Set(state.steps.filter(s => s.userOwned).map(s => s.n))
  const decisions = flags.filter(f => f.type === 'rule-broken' || owned.has(f.step))
  const steps = flags.filter(f => f.type !== 'rule-broken' && !owned.has(f.step)).map(f => f.step)
  const lines = ["DevForgeAI's progress tracker refused this write at the write gate (enforce mode):", ...flags.map(f => `- ${f.message}`)]
  if (steps.length) {
    const list = [...new Set(steps)].join(', ')
    lines.push(`To clear step ${list}: do the step with a tool call the run log can see (Read the files it names), `
      + `or, if you did it, tick it as \`- [x] N.\` in your reply text. A tick only in your thinking doesn't count.`)
  }
  if (decisions.length) {
    lines.push('The decisions at step ' + [...new Set(decisions.map(f => f.step))].join(', ')
      + " are the user's: ask the user, or leave those fields open.")
  }
  lines.push('Then write again.' + (state.run ? ` The run's log and state are in devforgeai/progress/runs/${state.run}/.` : ''))
  return lines.join('\n')
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
  const timeout = Math.floor(remainingMs) - 300
  return timeout >= 200 ? timeout : null
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

/** The step statuses of a todo list: '<N>.' todos only, by step number. */
function todoStatuses(todos: unknown): Record<string, string> | null {
  if (!Array.isArray(todos)) return null
  const out: Record<string, string> = {}
  for (const todo of todos) {
    if (!todo || typeof todo !== 'object') continue
    const { content, status } = todo as Fields
    const m = typeof content === 'string' ? content.match(/^\s*(\d+)\./) : null
    if (m && typeof status === 'string' && Number(m[1]) >= 1) out[String(Number(m[1]))] = status
  }
  return out
}

/** A TodoWrite's step events and the statuses to keep (BEH-20): each '<N>.' todo is compared with its status in the
 *  list the call replaced (the result's oldTodos), or with the kept statuses when the result has none, so an earlier
 *  run's completed todos left in the list claim nothing. Becoming in_progress starts a step, becoming completed ends
 *  it; straight from pending to completed gives done only. */
export function todoSteps(todos: unknown, last: Readonly<Record<string, string>>, oldTodos?: unknown): {
  events: Array<{ step: number; state: 'started' | 'done' }>
  statuses: Record<string, string>
} {
  const replaced = todoStatuses(oldTodos)
  const statuses: Record<string, string> = { ...last }
  const events: Array<{ step: number; state: 'started' | 'done' }> = []
  if (!Array.isArray(todos)) return { events, statuses }
  for (const todo of todos) {
    if (!todo || typeof todo !== 'object') continue
    const { content, status } = todo as Fields
    const m = typeof content === 'string' ? content.match(/^\s*(\d+)\./) : null
    if (!m || typeof status !== 'string' || Number(m[1]) < 1) continue
    const step = Number(m[1])
    const before = replaced !== null ? replaced[String(step)] : statuses[String(step)]
    if (status === 'in_progress' && before !== 'in_progress') events.push({ step, state: 'started' })
    if (status === 'completed' && before !== 'completed') events.push({ step, state: 'done' })
    statuses[String(step)] = status
  }
  return { events, statuses }
}

/** The refusal of a question asked with no step in progress (BEH-21), with how to recover. */
export const QUESTION_REFUSAL = "DevForgeAI's progress tracker refused this question (enforce mode): no step of this run "
  + "is marked in progress in your task list. Tasks from an earlier run don't count: if this run's checklist isn't in "
  + 'your task list yet, turn it into tasks first as the skill says (one task per step, subject <N>. <title>, metadata '
  + 'devforgeai_step: N). Then mark the step this question belongs to in_progress (TaskUpdate, or TodoWrite), and ask '
  + 'again.'

/** The question refusal when the provisional state's question gate refuses at seq, else null (BEH-21). */
export function questionRefusal(state: ProgressState, seq: number): string | null {
  const g = state.gate
  return g.kind === 'question' && g.seq === seq && g.refuse ? QUESTION_REFUSAL : null
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
  return `${state.skill} didn't keep its task list: ${n} step events, ${m} questions asked with no step in progress. `
    + 'Recommended: fix the skill so it keeps its checklist in the task list (DevForgeAI SPEC-012 §4)'
}

/** The once-per-session hint for a session with no task tools (BEH-23). */
export function hintText(skill: string): string {
  return `${skill}: this session has no task list, so DevForgeAI places your answers by guessing. For exact step `
    + 'tracking, start Claude Code with CLAUDE_CODE_ENABLE_TODO_TOOLS=1 (DevForgeAI SPEC-012 §4)'
}
