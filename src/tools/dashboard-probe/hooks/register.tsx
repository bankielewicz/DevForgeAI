// dashboard-probe: a prototype of the DevForgeAI Dashboard (docs/specs/devforgeai-dashboard.md), drawn live in a
// pane, with probes for the design's open platform questions. Not part of the devforgeai plugin.
//
// Open it with /dashboard-probe, or /dashboard-probe:dashboard (the command-file route, commands/dashboard.md).
// The layout follows the pane: 160x48 or 120x36 above the prompt, 64x48 docked. The seven tiles are keyed Boxes with
// Buttons laid over the Raster (clickable where the terminal reports clicks; keys 1-7 everywhere). t switches the
// look and writes it to /config, m the mode (drawing only), a pauses, q closes.
//
// Probes: /dashboard-probe menu N opens tile N's menu (run it while Claude works: the mid-turn case);
// /dashboard-probe arm makes the next turn end call $.command.run from session.measure (SPEC-013 v21 BEH-36's path).
// RPM (turn.step timing) and fuel (session.measure) are live; every other value is sample data.
import { atom, read, update } from 'claude-code'
import type { EngineInterface, Register } from 'claude-code'

import { frame, setBoxTiles, SIZES, spriteCells, THEMES, tileModel, tileRects } from './dashboard'
import type { Layout } from './dashboard'

const PLUGIN = 'dashboard-probe'
const PANE = 'dashboard-probe'
const LOOKS = ['A', 'B', 'C'] as const
const NAMES = { A: 'Default', B: 'Night drive', C: 'Race telemetry' } as const
const BY_NAME: Record<string, 'A' | 'B' | 'C'> = { Default: 'A', 'Night drive': 'B', 'Race telemetry': 'C' }

const theme = atom({ plugin: 'dashboard-probe', key: 'theme' } as const, 'A' as 'A' | 'B' | 'C')
const character = atom({ plugin: 'dashboard-probe', key: 'character' } as const, 'Ember')
const isAnimating = atom({ plugin: 'dashboard-probe', key: 'isAnimating' } as const, true)
// The tracker's mode as this prototype shows it. The real button runs SPEC-013 BEH-13 (IF-02); this one only redraws.
const trackMode = atom({ plugin: 'dashboard-probe', key: 'trackMode' } as const, 'enforce' as 'enforce' | 'observe')
const note = atom({ plugin: 'dashboard-probe', key: 'note' } as const, 'keys 1-7 open a phase · t look · m mode · q close')
const rpmNote = atom({ plugin: 'dashboard-probe', key: 'rpmNote' } as const, 'RPM: no model step measured yet')

// The module's own values; a reload starts them over.
const live = { isOpen: false, layout: 'dock' as Layout, isArmed: false, presses: 0 }

setBoxTiles(true)

// RPM: tokens per second, timed from turn.step (see the design, section 5).
const rpm = { value: 0, at: 0, isStreaming: false, chars: 0, start: 0, last: '' }
function rpmNow(now: number): number {
  if (rpm.isStreaming && rpm.start > 0 && now - rpm.start > 300) return Math.min(200, rpm.chars / 4 / ((now - rpm.start) / 1000))
  return Math.max(0, rpm.value * (1 - (now - rpm.at) / 5000))
}

const SKILLS = ['brainstorm', 'prd', 'architecture', 'context', 'epic', 'story', 'spec']
const LABELS = ['Brainstorm', 'PRD', 'Architecture', 'Context', 'Epic', 'Story', 'Spec']

// The tile menu: a question, then $.command.run with the person's pick.
async function tileMenu($: EngineInterface, i: number) {
  if (i >= 5) {
    $.ui.toast(`${LABELS[i]}: the skill isn't built yet`)
    return
  }
  const options = [`Start ${LABELS[i]}`, 'Cancel']
  const pick = await $.ui.ask(`${LABELS[i]}: what would you like to do?`, { options, header: 'Dashboard' }).catch(() => 'Cancel')
  if (pick !== options[0]) {
    await update($, note, () => `menu ${i + 1}: cancelled`)
    return
  }
  const line = await $.command
    .run({ command: `devforgeai:${SKILLS[i]!}`, args: '' })
    .then(() => `menu ${i + 1}: $.command.run /devforgeai:${SKILLS[i]} accepted`)
    .catch((err: unknown) => `menu ${i + 1}: $.command.run refused: ${String(err)}`)
  await update($, note, () => line)
}

function layoutFor(placement: string, columns: number): Layout {
  if (placement === 'dock') return 'dock'
  if (columns >= 160) return 'wide'
  if (columns >= 120) return 'compact'
  return 'dock'
}

async function fuelOf($: EngineInterface): Promise<number> {
  const usage = await $.session.usage().catch(() => undefined)
  const pct = usage?.context.percent
  return typeof pct === 'number' ? 100 - pct : 100
}

// The probe for "t writes /config": find this plugin's dashboardTheme row, set it, read it back.
async function nextLook($: EngineInterface) {
  const look = await update($, theme, t => LOOKS[(LOOKS.indexOf(t) + 1) % LOOKS.length]!)
  const rows = await $.config.list().catch(() => [])
  const row = rows.find(r => r.key.includes('dashboardTheme'))
  if (!row) {
    await $.store.set('dashboard-probe:theme', look).catch(() => {})
    await update($, note, () => `config: no dashboardTheme row in /config (${rows.length} rows); kept in $.store`)
    return
  }
  const r = await $.config.set({ key: row.key, value: NAMES[look] }).catch((err: unknown) => ({ deny: String(err) }))
  const back = (await $.config.list().catch(() => [])).find(x => x.key === row.key)
  const text = 'deny' in r && r.deny
    ? `config: set ${row.key} refused: ${r.deny}; kept in $.store`
    : `config: set ${row.key} = ${NAMES[look]} ✓ (reads back ${String(back?.value)})`
  if ('deny' in r && r.deny) await $.store.set('dashboard-probe:theme', look).catch(() => {})
  await update($, note, () => text)
}

async function tick($: EngineInterface) {
  if (rpm.last && (await read($, rpmNote)) !== rpm.last) await update($, rpmNote, () => rpm.last)
  if (!live.isOpen || !(await read($, isAnimating))) return
  const look = await read($, theme)
  const [columns, rows] = SIZES[live.layout]
  const ms = await $.clock.now()
  const r = await $.ui.blit({ requestId: PANE, key: 'dash', cells: frame(look, live.layout, ms, await fuelOf($), 'pace', await read($, trackMode), rpmNow(ms)), columns, rows })
  if ('deny' in r && /size|columns|rows/.test(String(r.deny))) $.ui.invalidate('ui.render')
  const who = await read($, character)
  if (who !== 'none') await $.ui.blit({ requestId: PANE, key: 'char', cells: spriteCells(who, THEMES[look].panel, ms), columns: 14, rows: 4 })
}

async function openPane($: EngineInterface): Promise<string> {
  live.isOpen = true
  const opened = await $.ui.open({ id: PANE, title: 'DevForgeAI Dashboard', focus: true, rows: 54, columns: 66 })
  return opened.isPlaced ? 'DevForgeAI Dashboard opened: keys 1-7 phases, t look, m mode, a pause, q close.' : `Not placed: ${'reason' in opened ? String(opened.reason) : 'unknown'}`
}

export const register: Register = (on, options) => {
  const startLook = BY_NAME[String(options.dashboardTheme ?? 'Default')] ?? 'A'
  const startCharacter = ['Ember', 'Clawd', 'none'].includes(String(options.dashboardCharacter)) ? String(options.dashboardCharacter) : 'Ember'

  on('session.start', async ($, e, next) => {
    const r = await next(e)
    const saved = await $.store.get('dashboard-probe:theme').catch(() => undefined)
    await update($, theme, () => (saved === 'A' || saved === 'B' || saved === 'C' ? saved : startLook))
    await update($, character, () => startCharacter)
    await $.command
      .register({ name: 'dashboard-probe', description: 'DevForgeAI Dashboard prototype (menu N, arm)', argumentHint: '[look | menu N | arm]', immediate: true })
      .catch(() => {})
    $.clock.every(200, () => {
      void tick($).catch(() => {})
    })
    return r
  })

  on('turn.step', async function* ($, e, next) {
    if (e.agentId) return yield* next(e)
    const began = Date.now()
    let first = 0
    rpm.isStreaming = true
    rpm.chars = 0
    rpm.start = 0
    const stream = next(e)
    try {
      for (;;) {
        const { value, done } = await stream.next()
        if (done) return value
        const c = value as { kind: string; text?: string; json?: string; usage?: { output_tokens?: number } | null }
        if (c.kind === 'text' || c.kind === 'thinking' || c.kind === 'input') {
          if (!first) {
            first = Date.now()
            rpm.start = first
          }
          rpm.chars += (c.text ?? c.json ?? '').length
        }
        if (c.kind === 'stop' && c.usage && typeof c.usage.output_tokens === 'number') {
          const secs = (Date.now() - (first || began)) / 1000
          if (secs > 0.2) {
            rpm.value = Math.min(200, c.usage.output_tokens / secs)
            rpm.at = Date.now()
            rpm.last = `RPM: last step ${c.usage.output_tokens} tok in ${secs.toFixed(1)} s = ${Math.round(c.usage.output_tokens / secs)} tok/s`
          }
        }
        yield value
      }
    } finally {
      rpm.isStreaming = false
    }
  })

  // Every press this plugin's elements receive, so clicks can be told apart from keys.
  on('ui.press', async ($, e, next) => {
    if (e.plugin === PLUGIN) {
      live.presses++
      await update($, note, () => `press #${live.presses}: ${e.element}`)
    }
    return next(e)
  })

  on('session.measure', async ($, e, next) => {
    const r = await next(e)
    if (live.isArmed) {
      live.isArmed = false
      void $.command
        .run({ command: 'devforgeai:spec-lookup', args: 'SPEC-014' })
        .then(() => update($, note, () => 'arm: $.command.run from session.measure accepted'))
        .catch((err: unknown) => update($, note, () => `arm: $.command.run from session.measure refused: ${String(err)}`))
    }
    return r
  })

  // The command-file route: commands/dashboard.md lists /dashboard-probe:dashboard; answering it here, without
  // next(e), should open the pane and load no prompt.
  on('command.run', { command: 'dashboard-probe:dashboard' }, async $ => {
    const text = await openPane($)
    await update($, note, () => 'command file route: /dashboard-probe:dashboard answered by the hook ✓')
    return { text }
  })

  on('command.run', { command: 'dashboard-probe' }, async ($, e) => {
    const args = e.args.trim().split(/\s+/)
    if (args[0] === 'arm') {
      live.isArmed = true
      return { text: 'Armed: when the next turn ends, session.measure calls $.command.run.' }
    }
    if (args[0] === 'look') {
      await nextLook($)
      return { text: `Look: ${NAMES[await read($, theme)]}; ${await read($, note)}` }
    }
    if (args[0] === 'menu') {
      const i = Number(args[1]) - 1
      if (!(i >= 0 && i < 7)) return { text: 'Usage: /dashboard-probe menu 1-7' }
      void tileMenu($, i).catch(() => {})
      return { text: `Menu ${i + 1} asked (mid-turn if Claude is working).` }
    }
    return { text: await openPane($) }
  })

  on('ui.render', { component: 'Pane', requestId: PANE }, async ($, e) => {
    if (e.surface !== 'terminal') {
      const { Text } = $.ui.resolve(e)
      return <Text dimColor>The terminal draws this prototype; the desktop gets the SVG version later.</Text>
    }
    const { Box, Text, Button, Raster } = $.ui.resolve(e)
    const look = await read($, theme)
    const who = await read($, character)
    const anim = await read($, isAnimating)
    const pmode = await read($, trackMode)
    const said = await read($, note)
    const rpmSaid = await read($, rpmNote)
    const ms = await $.clock.now()
    live.layout = layoutFor(e.props.placement, e.props.bodyColumns)
    const [columns, rows] = SIZES[live.layout]
    const rects = tileRects(live.layout)
    const isDock = live.layout === 'dock'
    return (
      <Box flexDirection="column">
        <Box position="relative" width={columns} height={rows}>
          <Raster key="dash" columns={columns} rows={rows} cells={frame(look, live.layout, ms, await fuelOf($), 'pace', pmode, rpmNow(ms))} />
          {rects.map((rc, i) => {
            const m = tileModel(look, i, live.layout)
            const room = rc.w - 5
            const label = m.label.length > room ? `${m.label.slice(0, room - 1)}…` : m.label
            return (
              <Box key={`tile-${i}`} position="absolute" top={rc.y} left={rc.x} width={rc.w} height={rc.h} borderStyle={m.style} borderColor={m.border} backgroundColor={m.bg} flexDirection={isDock ? 'row' : 'column'} paddingX={isDock ? 1 : 0} columnGap={isDock ? 2 : 0}>
                <Button key={`tile-btn-${i}`} hotkey={String(i + 1)} plain label={isDock ? m.label : label} onPress={() => void tileMenu($, i).catch(() => {})} />
                <Text color={m.docColor} wrap="truncate-end">{m.doc}</Text>
                <Text color={m.stateColor} wrap="truncate-end">{m.state}</Text>
                {!isDock && m.bar !== '' && <Text color={m.barColor}>{m.bar}</Text>}
              </Box>
            )
          })}
        </Box>
        <Box flexDirection="row" columnGap={2}>
          {who !== 'none' && <Raster key="char" columns={14} rows={4} cells={spriteCells(who, THEMES[look].panel, ms)} />}
          <Box flexDirection="column">
            <Text dimColor wrap="truncate-end">{said}</Text>
            <Text dimColor wrap="truncate-end">{rpmSaid}</Text>
            <Box flexDirection="row" flexWrap="wrap" columnGap={2}>
              <Button key="look" hotkey="t" label={`Look: ${NAMES[look]}`} onPress={() => void nextLook($).catch(() => {})} />
              <Button key="mode" hotkey="m" label={pmode === 'enforce' ? 'Switch to observe' : 'Switch to enforce'} onPress={() => void update($, trackMode, x => (x === 'enforce' ? 'observe' : 'enforce'))} />
              <Button key="anim" hotkey="a" label={anim ? 'Pause' : 'Animate'} onPress={() => void update($, isAnimating, x => !x)} />
              <Button key="close" hotkey="q" role="dismiss" label="Close" onPress={() => { live.isOpen = false; void $.ui.close({ id: PANE }) }} />
            </Box>
          </Box>
        </Box>
      </Box>
    )
  })
}
