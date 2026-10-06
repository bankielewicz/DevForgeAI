// @ts-nocheck
// The DevForgeAI Dashboard drawing engine, ported from the design canvas (Main.dc.html): pure functions that lay out the
// whole dashboard on a character grid and pack it as Raster cells. No $ here.
const CW = 7.2
const CH = 18

function hx(h) { return [parseInt(h.slice(1, 3), 16), parseInt(h.slice(3, 5), 16), parseInt(h.slice(5, 7), 16)] }
function toHex(a) { return '#' + a.map(v => Math.max(0, Math.min(255, Math.round(v))).toString(16).padStart(2, '0')).join('') }
export function mix(a, b, t) { const A = hx(a), B = hx(b); return toHex(A.map((v, i) => v + (B[i] - v) * t)) }

export { PHASES }
export const THEMES = {
  A: {
    name: 'Default', bg: '#111316', bg2: '#111316', panel: '#171A1F', panel2: '#171A1F', bar: '#0B0D10',
    border: '#2C323B', text: '#E8EAED', dim: '#8A93A0', faint: '#4C535E', accent: '#3E8BFF', ink: '#06122B',
    done: '#9CC3FF', inprog: '#3E8BFF', next: '#E8EAED', notbuilt: '#353B44', warn: '#F2B84B', danger: '#FF5D5D',
    ok: '#5BD49B', run: '#F5C542', needle: '#FFFFFF', odoBg: '#0A0C0F', odoFg: '#E8EAED',
    phase: ['#9CC3FF', '#9CC3FF', '#3E8BFF', '#8A93A0', '#8A93A0', '#4C535E', '#4C535E'],
    tile: 'round', panelStyle: 'round', arcTh: [0], ticks: 10, major: 5, halo: false,
  },
  B: {
    name: 'Night drive', bg: '#0A0F2E', bg2: '#1C0A38', panel: '#110E38', panel2: '#1B1150', bar: '#070A22',
    border: '#3D2F86', text: '#F1ECFF', dim: '#A49BDD', faint: '#5A519E', accent: '#FF4FD8', ink: '#14062B',
    done: '#2BFFC6', inprog: '#FF4FD8', next: '#26D9FF', notbuilt: '#3A3470', warn: '#FFB443', danger: '#FF3D71',
    ok: '#2BFFC6', run: '#FFE45E', needle: '#FF4FD8', odoBg: '#070720', odoFg: '#26D9FF',
    phase: ['#FF4FD8', '#B24BFF', '#4F7BFF', '#26D9FF', '#2BFFC6', '#5B5296', '#5B5296'],
    tile: 'heavy', panelStyle: 'heavy', arcTh: [0, -3.6, -7.2], ticks: 20, major: 5, halo: true,
  },
  C: {
    name: 'Race telemetry', bg: '#050505', bg2: '#050505', panel: '#0B0B0B', panel2: '#0B0B0B', bar: '#000000',
    border: '#2E2E2E', text: '#F4F4F4', dim: '#9A9A9A', faint: '#555555', accent: '#FFB000', ink: '#000000',
    done: '#B6FF3B', inprog: '#FFB000', next: '#FFFFFF', notbuilt: '#333333', warn: '#FF8A00', danger: '#FF2E2E',
    ok: '#B6FF3B', run: '#FFE14D', needle: '#FFFFFF', odoBg: '#1A1200', odoFg: '#FFB000',
    phase: ['#B6FF3B', '#7CFFB2', '#FFB000', '#FF8A00', '#FFE14D', '#4A4A4A', '#4A4A4A'],
    tile: 'light', panelStyle: 'light', arcTh: [0, -3.6], ticks: 40, major: 10, halo: false,
  },
}

const PHASES = [
  { n: 'Brainstorm', g: '✦', doc: 'BRN-001', st: 'done', steps: '9/9', dur: '38m', t: '38m' },
  { n: 'PRD', g: '≡', doc: 'PRD-002', st: 'done', steps: '11/11', dur: '1h 04m', t: '1h04' },
  { n: 'Architecture', g: '⌂', doc: 'ARCH-001 draft', st: 'prog', cur: 7, tot: 11, dur: '41m', t: '41m ▸' },
  { n: 'Context', g: '◎', doc: 'needs ARCH-001', st: 'next', est: '~35m est.', t: '~35m' },
  { n: 'Epic', g: '▲', doc: 'needs CTX docs', st: 'todo', est: '~50m est.', t: '~50m' },
  { n: 'Story', g: '¶', doc: 'skill not built', st: 'nb', t: '-' },
  { n: 'Spec', g: '§', doc: 'skill not built', st: 'nb', t: '-' },
]

// The character: a few pixel frames, two pixels a cell (top in the glyph's colour, bottom in its background).
const SPRITES = {
  Ember: { palette: { r: '#FF5A1F', o: '#FF9A2E', y: '#FFE07A', k: '#1A0F08', w: '#FFFFFF' }, frames: [
    ['......r.......', '.....rr.......', '....rorr......', '...rooor......', '..rooyoor.....', '..royyyor.....', '..rokyykor....', '...royyor.....'],
    ['.......r......', '......rr......', '.....rorr.....', '...rroor......', '..rooyoor.....', '..royyyyr.....', '..rokyykor....', '...royyor.....'],
  ] },
  Clawd: { palette: { o: '#D97757', d: '#A85A3E', k: '#1A1A1A' }, frames: [
    ['..............', '...oooooooo...', '..oooooooooo..', '..ookoooooko..', '.oooooooooooo.', '.oooooooooooo.', '..o.o....o.o..', '..o.o....o.o..'],
    ['..............', '...oooooooo...', '..oooooooooo..', '..oookooooko..', '.oooooooooooo.', '.oooooooooooo.', '...o.o..o.o...', '..o.o....o.o..'],
  ] },
}

// The character as Raster cells (14x4) on a background, frame by time.
export function spriteCells(name, bgHex, ms) {
  const S = SPRITES[name]
  const f = S.frames[Math.floor(ms / 450) % S.frames.length]
  const words = new Uint32Array(14 * 4 * 3)
  const bg = parseInt(bgHex.slice(1), 16)
  const col = ch => (ch === '.' ? null : parseInt(S.palette[ch].slice(1), 16))
  let k = 0
  for (let cy = 0; cy < 4; cy++) for (let x = 0; x < 14; x++) {
    const top = col(f[cy * 2][x]), bot = col(f[cy * 2 + 1][x])
    if (top === null && bot === null) { words[k++] = 0x20; words[k++] = bg; words[k++] = bg }
    else if (top !== null && bot !== null) { words[k++] = 0x2580; words[k++] = top; words[k++] = bot }
    else if (top !== null) { words[k++] = 0x2580; words[k++] = top; words[k++] = bg }
    else { words[k++] = 0x2584; words[k++] = bot; words[k++] = bg }
  }
  return new Uint8Array(words.buffer).toBase64()
}

const AGENTS = [
  { pre: '', txt: 'main', st: 'run', t: '4m 12s', agent: true },
  { pre: '├─ ', txt: '◆ spec-lookup', st: 'done', t: '0:38', agent: true },
  { pre: '│  ├─ ', txt: 'Read  SPEC-013.md', st: 'done', t: '0.2s' },
  { pre: '│  ├─ ', txt: 'Grep  "precompact"', st: 'done', t: '0.4s' },
  { pre: '│  └─ ', txt: 'Bash  find_spec.py', st: 'done', t: '1.9s' },
  { pre: '├─ ', txt: '◆ drafts-review', st: 'run', t: '1:05', agent: true },
  { pre: '│  ├─ ', txt: 'Read  ARCH-001.md', st: 'done', t: '0.3s' },
  { pre: '│  ├─ ', txt: 'WebFetch  adr.github.io', st: 'fail', t: '2.1s' },
  { pre: '│  └─ ', txt: 'Grep  "NEEDS ADR"', st: 'run', t: '...' },
  { pre: '└─ ', txt: '◆ eval-probe', st: 'done', t: '0:12', agent: true },
]

function term(W, H, bgAt, fg) {
  const rows = []
  for (let y = 0; y < H; y++) { const r = []; for (let x = 0; x < W; x++) r.push({ c: ' ', f: fg, b: bgAt(x, y) }); rows.push(r) }
  return { W, H, rows }
}
function cell(t, x, y) { return (y >= 0 && y < t.H && x >= 0 && x < t.W) ? t.rows[y][x] : null }
function put(t, x, y, s, f, b) {
  const a = Array.from(String(s))
  for (let i = 0; i < a.length; i++) { const c = cell(t, Math.round(x) + i, y); if (!c) continue; c.c = a[i]; if (f) c.f = f; if (b) c.b = b }
  return a.length
}
function len(s) { return Array.from(String(s)).length }
function putR(t, xr, y, s, f, b) { put(t, xr - len(s) + 1, y, s, f, b) }
function putC(t, xc, y, s, f, b) { put(t, Math.round(xc - len(s) / 2), y, s, f, b) }
function fit(s, n) { const a = Array.from(String(s)); return a.length <= n ? String(s) : a.slice(0, Math.max(0, n - 1)).join('') + '…' }
function fill(t, x, y, w, h, b, ch, f) {
  for (let j = 0; j < h; j++) for (let i = 0; i < w; i++) {
    const k = cell(t, x + i, y + j); if (!k) continue
    if (b) k.b = (typeof b === 'function') ? b(i, j) : b
    if (ch !== undefined) { k.c = ch; if (f) k.f = f }
  }
}
const BOX = { round: '╭╮╰╯─│', light: '┌┐└┘─│', heavy: '┏┓┗┛━┃', double: '╔╗╚╝═║', dash: '╭╮╰╯┄┆' }
function box(t, x, y, w, h, o) {
  const s = BOX[o.style || 'round']
  if (o.fill) fill(t, x + 1, y + 1, w - 2, h - 2, o.fill, ' ', o.f)
  for (let i = 1; i < w - 1; i++) { put(t, x + i, y, s[4], o.f); put(t, x + i, y + h - 1, s[4], o.f) }
  for (let j = 1; j < h - 1; j++) { put(t, x, y + j, s[5], o.f); put(t, x + w - 1, y + j, s[5], o.f) }
  put(t, x, y, s[0], o.f); put(t, x + w - 1, y, s[1], o.f); put(t, x, y + h - 1, s[2], o.f); put(t, x + w - 1, y + h - 1, s[3], o.f)
  if (o.title) put(t, x + 2, y, ' ' + o.title + ' ', o.tf || o.f, o.tb)
  if (o.right) putR(t, x + w - 3, y, ' ' + o.right + ' ', o.rf || o.f, o.tb)
}

function gauge(t, T, x, y, w, h, o) {
  const m = new Map()
  const dot = (X, Y, f, p) => {
    const px = Math.round(X / 3.6), py = Math.round(Y / 4.5)
    if (px < 0 || py < 0 || px >= w * 2 || py >= h * 4) return
    const cx = px >> 1, cy = py >> 2, dx = px & 1, dy = py & 3
    const bit = dy < 3 ? (dx ? [8, 16, 32][dy] : [1, 2, 4][dy]) : (dx ? 128 : 64)
    const k = cy * w + cx
    const e = m.get(k) || { m: 0, f, p: -1 }
    e.m |= bit; if (p >= e.p) { e.p = p; e.f = f }
    m.set(k, e)
  }
  const Wp = w * CW, Hp = h * CH
  const R = Math.min(Wp / 2 - 4, (Hp - 2 * CH - 6) / 1.71), cx = Wp / 2, cy = R + 5
  const inner = R + Math.min(...T.arcTh)
  const ang = a => (225 - 270 * a) * Math.PI / 180
  const v = Math.max(0, Math.min(1, o.v))
  for (let s = 0; s <= 900; s++) {
    const a = s / 900, col = o.color(a), lit = a <= v, c = lit ? col : mix(col, T.panel, 0.8)
    for (const th of T.arcTh) dot(cx + (R + th) * Math.cos(ang(a)), cy - (R + th) * Math.sin(ang(a)), c, lit ? 1.5 : 1)
  }
  for (let i = 0; i <= T.ticks; i++) {
    const ta = i / T.ticks, major = (i % T.major) === 0
    for (let rr = inner - (major ? 9 : 5); rr <= inner - 3; rr++) dot(cx + rr * Math.cos(ang(ta)), cy - rr * Math.sin(ang(ta)), major ? T.text : T.faint, 2)
  }
  for (const mk of (o.marks || [])) for (let mr = inner - 12; mr <= R + 3; mr++) dot(cx + mr * Math.cos(ang(mk.a)), cy - mr * Math.sin(ang(mk.a)), mk.c, 2.6)
  const av = ang(v), nl = inner - 5
  for (let ns = 0; ns <= 1; ns += 0.004) {
    const nx = cx + ns * nl * Math.cos(av), ny = cy - ns * nl * Math.sin(av)
    dot(nx, ny, T.needle, 3)
    if (T.halo) {
      dot(nx + 2.6 * Math.sin(av), ny + 2.6 * Math.cos(av), mix(T.needle, T.panel, 0.45), 2.8)
      dot(nx - 2.6 * Math.sin(av), ny - 2.6 * Math.cos(av), mix(T.needle, T.panel, 0.45), 2.8)
    }
  }
  for (let hr = 0; hr <= 4.5; hr += 0.9) for (let ha = 0; ha < 6.3; ha += 0.3) dot(cx + hr * Math.cos(ha), cy + hr * Math.sin(ha), T.needle, 3)
  for (const [k, e] of m) { const c = cell(t, x + (k % w), y + Math.floor(k / w)); if (c) { c.c = String.fromCharCode(0x2800 + e.m); c.f = e.f } }
  if (o.tl) for (const lb of o.tl) {
    const lr = inner - 20
    putC(t, x + (cx + lr * Math.cos(ang(lb.a))) / CW, y + Math.floor((cy - lr * Math.sin(ang(lb.a))) / CH), lb.s, T.dim)
  }
  const vr = y + Math.floor((cy + 16) / CH)
  putC(t, x + w / 2, vr, o.val, o.vcol || T.text)
  putC(t, x + w / 2, vr + 1, o.unit, T.dim)
  putC(t, x + w / 2, y + h - 2, o.label, o.lcol || T.text)
  putC(t, x + w / 2, y + h - 1, o.sub, o.subcol || T.faint)
}

// The third instrument, by mode: pace along the route (with wheel-spin when RPM is high and pace near zero),
// efficiency (prompt-cache hit rate), burn ($ per hour), or none (two dials, centred).
export const SPEED_MODES = ['pace', 'efficiency', 'burn', 'none']
export function demoSpeed(mode, ms) {
  const cyc = (ms / 1000) % 20
  if (mode === 'pace') return cyc < 14 ? { v: 0.45 + 0.2 * Math.sin(ms / 1500), spin: false } : { v: 0.03, spin: true }
  if (mode === 'efficiency') return { v: 0.78 + 0.16 * Math.sin(ms / 4000), spin: false }
  if (mode === 'burn') return { v: (5.5 + 2.5 * Math.sin(ms / 3500)) / 20, spin: false }
  return { v: 0, spin: false }
}
function dials(t, T, theme, x0, y0, gw, gh, gstep, fuel, rpm, short, mode, sp) {
  if (mode === 'none') { x0 += Math.floor(gstep / 2) }
  const rpmCol = a => a >= 0.75 ? T.danger : (theme === 'B' ? mix(T.phase[3], T.phase[0], a / 0.75) : theme === 'C' ? T.done : T.accent)
  const fuelCol = a => a <= 0.2 ? T.danger : a <= 0.3 ? T.warn : (theme === 'B' ? T.phase[4] : T.ok)
  const mphCol = a => theme === 'B' ? mix(T.phase[1], T.phase[3], a) : theme === 'C' ? T.text : '#9CC3FF'
  const tl = theme === 'C'
  gauge(t, T, x0, y0, gw, gh, { v: rpm / 200, color: rpmCol, val: String(Math.round(rpm)), unit: 'tok/s', label: 'RPM', sub: 'redline 150',
    tl: tl ? [{ a: 0.25, s: '50' }, { a: 0.5, s: '100' }, { a: 0.75, s: '150' }] : null, marks: [{ a: 0.75, c: T.danger }] })
  gauge(t, T, x0 + gstep, y0, gw, gh, { v: fuel / 100, color: fuelCol, val: Math.round(fuel) + '%', vcol: fuel <= 20 ? T.danger : fuel <= 30 ? T.warn : T.text,
    unit: short ? 'context left' : 'context left', label: 'FUEL', sub: short ? '▼20% precompact' : '▼ 20% precompact runs here', subcol: T.danger,
    tl: tl ? [{ a: 0.3, s: '30' }, { a: 0.5, s: '50' }] : null, marks: [{ a: 0.3, c: T.warn }, { a: 0.2, c: T.danger }] })
  if (mode === 'pace') {
    const mins = sp.spin ? '—' : Math.round(60 / Math.max(1, sp.v * 12)) + ' min/step'
    gauge(t, T, x0 + 2 * gstep, y0, gw, gh, { v: sp.v, color: mphCol, val: String(Math.round(sp.v * 100)), vcol: sp.spin ? T.warn : T.text, unit: sp.spin ? '' : mins, label: 'PACE',
      lcol: sp.spin ? T.warn : T.text, sub: sp.spin ? '▲ WHEEL-SPIN' : (short ? 'route speed' : 'progress along route'), subcol: sp.spin ? T.warn : T.faint, marks: [] })
  } else if (mode === 'efficiency') {
    gauge(t, T, x0 + 2 * gstep, y0, gw, gh, { v: sp.v, color: a => a < 0.5 ? T.warn : (theme === 'B' ? T.phase[3] : T.ok), val: Math.round(sp.v * 100) + '%', unit: 'cache hits', label: 'EFFICIENCY', sub: short ? 'cold after /clear' : 'cold after /clear or idle', marks: [] })
  } else if (mode === 'burn') {
    gauge(t, T, x0 + 2 * gstep, y0, gw, gh, { v: sp.v, color: a => a > 0.6 ? T.danger : a > 0.4 ? T.warn : mphCol(a), val: '$' + (sp.v * 20).toFixed(2), unit: 'per hour', label: 'BURN', sub: short ? 'session $11.80' : 'session $11.80 · $20/h max', marks: [] })
  }
}

function drawTile(t, T, theme, i, p, x, y, w, h, C) {
  const acc = T.phase[i], st = p.st
  const bcol = st === 'done' ? T.done : st === 'prog' ? T.inprog : st === 'next' ? T.next : st === 'nb' ? T.notbuilt : T.border
  let inner
  if (theme === 'B') {
    const s0 = st === 'nb' ? 0.05 : (st === 'todo' ? 0.1 : 0.32), s1 = st === 'nb' ? 0.02 : 0.07
    if (st === 'prog' || st === 'next') fill(t, x - 1, y - 1, w + 2, h + 2, (ii, jj) => mix(mix(T.bg, T.bg2, (y - 1 + jj) / (t.H - 1)), acc, 0.16))
    inner = (ii, jj) => mix(mix(T.bg, T.bg2, (y + jj) / (t.H - 1)), acc, s0 + (s1 - s0) * (ii / Math.max(1, w - 3)))
  } else if (theme === 'A') inner = st === 'prog' ? mix(T.panel, T.accent, 0.13) : (st === 'nb' ? T.bg : T.panel)
  else inner = st === 'prog' ? '#140E00' : T.panel
  const style = st === 'nb' ? 'dash' : (theme === 'B' && st === 'prog' ? 'double' : T.tile)
  const fcol = (theme === 'B' && (st === 'done' || st === 'prog' || st === 'next')) ? acc : bcol
  box(t, x, y, w, h, { style, f: fcol, fill: inner })
  const dark = st === 'todo' || st === 'nb'
  if (theme === 'C') {
    fill(t, x, y, w, 1, st === 'nb' ? '#1A1A1A' : (st === 'todo' ? '#262626' : acc))
    put(t, x + 1, y, fit(p.g + ' ' + p.n.toUpperCase(), w - 5), dark ? T.dim : '#000000')
    putR(t, x + w - 2, y, 'P' + (i + 1), dark ? T.dim : '#000000')
  }
  const ix = x + 2, iw = w - 4
  let r = y + 1
  if (theme !== 'C') { put(t, ix, r, p.g, st === 'nb' ? T.faint : acc); put(t, ix + 2, r, fit(p.n, iw - 2), st === 'nb' ? T.faint : T.text); r++ }
  put(t, ix, r, fit(p.doc, iw), st === 'nb' ? T.faint : T.dim); r++
  if (!C) r++
  if (st === 'next') {
    if (theme === 'C') put(t, ix, r, '◉ NEXT ▸', T.next)
    else put(t, ix, r, ' NEXT ▸ ', T.ink, theme === 'A' ? T.accent : T.next)
  } else {
    const lab = { done: ['✓ done', T.done], prog: ['● in progress', T.inprog], todo: ['○ not started', T.dim], nb: ['◌ coming soon', T.faint] }[st]
    put(t, ix, r, lab[0], theme === 'B' && st !== 'todo' && st !== 'nb' ? acc : lab[1])
  }
  r++
  if (st === 'prog') {
    const n = Math.round(iw * p.cur / p.tot)
    for (let k = 0; k < iw; k++) put(t, ix + k, r, k < n ? '█' : '░', k < n ? (theme === 'B' ? mix(T.phase[1], T.phase[3], k / Math.max(1, iw - 1)) : acc) : T.faint)
    r++
    put(t, ix, r, C ? 'step ' + p.cur + '/' + p.tot : 'step ' + p.cur + ' of ' + p.tot, T.text)
    if (theme === 'C' && !C) putR(t, ix + iw - 1, r, p.dur, T.inprog)
    r++
  } else if (st === 'done') {
    put(t, ix, r, (C ? '' : 'steps ') + p.steps, T.dim)
    if (!C || theme === 'C') putR(t, ix + iw - 1, r, p.dur, theme === 'C' ? T.done : T.faint)
  } else if ((st === 'next' || st === 'todo') && !C) put(t, ix, r, p.est, st === 'next' ? T.dim : T.faint)
  if (!C || theme !== 'C') putR(t, x + w - 3, y + h - 2, '[' + (i + 1) + ']', st === 'nb' ? T.faint : T.dim)
}

// When the tiles are drawn as keyed Boxes over the Raster (clickable), the Raster leaves their cells empty.
const BOX_TILES = { on: false }

// Where each tile sits, in cells, for a layout: the same numbers drawWide and drawDock use.
export function tileRects(layout) {
  if (layout === 'dock') return Array.from({ length: 7 }, (_, i) => ({ x: 1, y: 2 + i * 3, w: 62, h: 3 }))
  const C = layout === 'compact', W = C ? 120 : 160
  const ty = C ? 2 : 3, th = C ? 7 : 9, tw = C ? 15 : 19, g = C ? 2 : 3
  const x0 = Math.floor((W - (7 * tw + 6 * g)) / 2)
  return Array.from({ length: 7 }, (_, i) => ({ x: x0 + i * (tw + g), y: ty, w: tw, h: th }))
}

// What a Box tile shows: border style and colour, a solid background, and its lines of text.
export function tileModel(theme, i, layout) {
  const T = THEMES[theme], p = PHASES[i], st = p.st, acc = T.phase[i]
  const border = st === 'done' ? T.done : st === 'prog' ? T.inprog : st === 'next' ? T.next : st === 'nb' ? T.notbuilt : T.border
  const bg = theme === 'B' ? mix(T.bg, acc, st === 'nb' ? 0.05 : st === 'todo' ? 0.1 : 0.22) : theme === 'A' ? (st === 'prog' ? mix(T.panel, T.accent, 0.13) : T.panel) : (st === 'prog' ? '#140E00' : T.panel)
  const style = theme === 'A' ? 'round' : theme === 'B' ? (st === 'prog' ? 'double' : 'bold') : 'single'
  const state = { done: '✓ done', prog: '● ' + p.cur + '/' + p.tot, next: '◉ NEXT ▸', todo: '○ not started', nb: '◌ coming soon' }[st]
  const stateColor = st === 'done' ? T.done : st === 'prog' ? T.inprog : st === 'next' ? T.next : T.dim
  const bar = st === 'prog' ? '█'.repeat(Math.round(6 * p.cur / p.tot)) + '░'.repeat(6 - Math.round(6 * p.cur / p.tot)) : ''
  return { label: p.g + ' ' + p.n, labelColor: st === 'nb' ? T.faint : T.text, border: theme === 'B' && st !== 'nb' && st !== 'todo' ? acc : border, bg, style, doc: p.doc, docColor: st === 'nb' ? T.faint : T.dim, state, stateColor, bar, barColor: acc, dashed: st === 'nb' }
}

export function setBoxTiles(on) { BOX_TILES.on = on }

function chip(t, x, y, s, f, b) { put(t, x, y, s, f, b); return x + len(s) + 1 }

function odometer(t, T, x, y, C, ms) {
  put(t, x, y + 1, 'ODO', T.dim)
  const n = 1284903 + Math.floor((ms / 400) % 100000)
  const digits = String(n).padStart(8, '0')
  let dx = x + 5
  for (let i = 0; i < digits.length; i++) {
    const last = i === digits.length - 1
    put(t, dx, y, '▄▄▄', T.odoBg)
    put(t, dx, y + 1, ' ' + digits[i] + ' ', last ? T.accent : T.odoFg, T.odoBg)
    put(t, dx, y + 2, '▀▀▀', T.odoBg)
    dx += 3
    if (i === 1 || i === 4) { put(t, dx, y + 1, ',', T.dim); dx += 1 }
  }
  put(t, dx + 1, y + 1, C ? 'tok' : 'tok · lifetime, this project', T.dim)
}

function statusBar(t, T, W, sy, fuel, short, mode) {
  fill(t, 0, sy, W, 1, T.bar)
  let sx = chip(t, 1, sy, short ? ' ◆ arch 7/11 ' : ' ◆ architecture 7/11 ', T.ink, T.accent)
  sx = mode === 'enforce' ? chip(t, sx, sy, ' ENFORCE ', T.ink, T.ok) : chip(t, sx, sy, ' OBSERVE ', T.text, mix(T.border, T.bar, 0.2))
  if (!short) sx = chip(t, sx, sy, ' ! 2 flags ', T.text, mix(T.warn, T.bar, 0.7))
  const f = Math.round(fuel)
  if (f <= 20) chip(t, sx, sy, short ? ' ● fuel ' + f + '% · precompacting ' : ' ● Fuel ' + f + '% · running /devforgeai:precompact ', '#FFFFFF', T.danger)
  else if (f <= 30) chip(t, sx, sy, short ? ' ▲ fuel ' + f + '% · precompact at 20% ' : ' ▲ Fuel ' + f + '% · precompact runs at 20% ', T.ink, T.warn)
  else chip(t, sx, sy, ' Fuel ' + f + '% ', T.dim, mix(T.border, T.bar, 0.3))
}

function drawWide(theme, C, fuel, rpm, ms, mode, sp, pmode) {
  const T = THEMES[theme]
  const W = C ? 120 : 160, H = C ? 36 : 48
  const bgAt = (x, y) => T.bg2 !== T.bg ? mix(T.bg, T.bg2, y / (H - 1)) : T.bg
  const t = term(W, H, bgAt, T.text)
  const panelFill = T.panel2 !== T.panel ? (i, j) => mix(T.panel, T.panel2, j / 18) : T.panel
  fill(t, 0, 0, W, 1, T.bar)
  put(t, 1, 0, '◆ DevForgeAI Dashboard', T.accent)
  put(t, 22, 0, '~/Projects/DevForgeAI', T.dim)
  if (!C) put(t, 46, 0, 'theme: ' + T.name + '  (t switches)', T.faint)
  putR(t, W - 2, 0, '● LIVE', T.ok)
  const ty = C ? 2 : 3, th = C ? 7 : 9, tw = C ? 15 : 19, g = C ? 2 : 3
  const total = 7 * tw + 6 * g, x0 = Math.floor((W - total) / 2), cur = 2
  put(t, x0, ty - 1, 'ROUTE', T.dim)
  put(t, x0 + 6, ty - 1, '· 2 done · 1 in progress · 1 next · 2 coming soon', T.faint)
  putR(t, x0 + total - 1, ty - 1, 'click a phase to drive  [1-7]', T.faint)
  const txs = [], cxs = []
  for (let i = 0; i < 7; i++) { txs.push(x0 + i * (tw + g)); cxs.push(x0 + i * (tw + g) + Math.floor(tw / 2)) }
  if (!BOX_TILES.on) for (let i = 0; i < 7; i++) drawTile(t, T, theme, i, PHASES[i], txs[i], ty, tw, th, C)
  for (let i = 0; i < 6; i++) {
    const lit = PHASES[i].st === 'done'
    put(t, txs[i] + tw, ty + Math.floor(th / 2), g === 3 ? '━━▶' : '━▶', lit ? (theme === 'B' ? T.phase[i + 1] : T.done) : T.faint)
  }
  const ny = ty + th + 1
  put(t, x0, ny, 'NAV', T.dim)
  put(t, cxs[cur], ny, '▼ YOU ARE HERE', T.accent)
  putR(t, x0 + total - 1, ny, ' ETA ~1 h 50 m to Epic · Spec - ', T.ink, theme === 'C' ? T.accent : mix(T.accent, T.text, 0.15))
  for (let lx = x0; lx < x0 + total; lx++) {
    const trav = lx <= cxs[cur]
    put(t, lx, ny + 1, trav ? '━' : '┄', trav ? (theme === 'B' ? mix(T.phase[0], T.phase[2], (lx - x0) / (cxs[cur] - x0)) : T.accent) : T.faint)
  }
  put(t, x0, ny + 1, '●', T.done)
  put(t, x0 + total - 1, ny + 1, '■', T.faint)
  for (let i = 0; i < 7; i++) {
    const st = PHASES[i].st
    const node = st === 'done' ? ['●', T.done] : st === 'prog' ? ['◉', T.accent] : st === 'next' ? ['○', T.next] : st === 'todo' ? ['○', T.dim] : ['◌', T.faint]
    put(t, cxs[i], ny + 1, node[0], theme === 'B' && st !== 'nb' && st !== 'todo' ? T.phase[i] : node[1])
    putC(t, cxs[i] + 0.5, ny + 2, PHASES[i].t, st === 'prog' ? T.accent : (st === 'nb' ? T.faint : T.dim))
  }
  if (!C) { put(t, x0, ny + 2, 'Start', T.dim); putR(t, x0 + total - 1, ny + 2, 'Ship', T.dim) }
  const y1 = ny + 4
  const cbx = C ? 0 : 1, cbw = C ? 76 : 100, cbh = C ? 15 : 19
  const abx = cbx + cbw + 1, abw = W - abx - (C ? 0 : 1)
  const pst = T.panelStyle
  box(t, cbx, y1, cbw, cbh, { style: pst, f: T.border, fill: panelFill, title: 'INSTRUMENTS', tf: T.dim, right: 'turn 57 · live', rf: T.faint })
  dials(t, T, theme, cbx + (C ? 3 : 4), y1 + (C ? 1 : 2), C ? 22 : 26, C ? 10 : 12, C ? 24 : 31, fuel, rpm, C, mode, sp)
  odometer(t, T, cbx + 3, y1 + cbh - 4, C, ms)
  if (!C) putR(t, cbx + cbw - 4, y1 + cbh - 3, 'session 182,410 tok · $11.80', T.faint)
  box(t, abx, y1, abw, cbh, { style: pst, f: T.border, fill: panelFill, title: 'AGENTS', tf: T.dim, right: '3 live', rf: T.faint })
  agents(t, T, theme, abx, y1, abw, AGENTS, ms)
  put(t, abx + 2, y1 + cbh - 2, fit('3 agents · 7 tool calls · 1 failed', abw - 4), T.faint)
  const gyy = y1 + cbh + 1, gbh = C ? 5 : 9, gbw = C ? W : 100, gbx = C ? 0 : 1
  box(t, gbx, gyy, gbw, gbh, { style: pst, f: T.border, fill: panelFill, title: 'GUARDRAILS', tf: T.dim, right: C ? '' : 'mods', rf: T.faint })
  const chips = [' ✓ write gate ', ' ✓ question gate ', ' ✓ origin filter ', ' ✓ precompact @20% fuel ', ' ✓ exit confirm ']
  let cxp = gbx + 2, cy0 = gyy + 1
  if (!C) { put(t, cxp, cy0, '◈ 5 mods armed', T.accent); putR(t, gbx + gbw - 3, cy0, mode === 'enforce' ? ' ENFORCE ' : ' OBSERVE ', mode === 'enforce' ? T.ink : T.text, mode === 'enforce' ? T.ok : mix(T.border, T.bar, 0.2)); cy0 += 2 } else cxp = chip(t, cxp, cy0, '◈ 5 armed', T.accent)
  for (const c of chips) cxp = chip(t, cxp, cy0, c, T.ok, mix(T.ok, T.panel, 0.84))
  const hy = cy0 + (C ? 1 : 2)
  put(t, gbx + 2, hy, '▲ LAST HOLD', T.warn)
  put(t, gbx + 14, hy, C ? 'write gate held step 8 until you answered · resolved ✓' : 'write gate held step 8 until you answered  ·  14:02  ·  resolved ✓', T.text)
  put(t, gbx + 2, hy + 1, C ? 'fails open: if the tracker stops, work goes on' : 'fails open: if the tracker stops, the work goes on and you are told', T.faint)
  if (!C) {
    const lbx = 102, lbw = W - lbx - 1
    if (theme === 'C') {
      box(t, lbx, gyy, lbw, gbh, { style: pst, f: T.border, fill: panelFill, title: 'TELEMETRY', tf: T.dim, right: 'lap 41:07', rf: T.accent })
      const tel = [['IN', '412,880'], ['OUT', '38,204'], ['CACHE', '91.4%'], ['TURNS', '57'], ['TOOLS', '214'], ['T/MIN', '12.3'], ['COST', '$11.80'], ['$/H', '4.20'], ['FLAGS', '2'], ['P50 TTFT', '1.8s'], ['P95', '6.2s'], ['ERR', '0']]
      tel.forEach((kv, k) => { const xx = lbx + 2 + (k % 3) * 18, yy = gyy + 1 + Math.floor(k / 3) * 2; put(t, xx, yy, kv[0], T.dim); putR(t, xx + 15, yy, kv[1], k === 6 ? T.accent : T.done) })
    } else {
      box(t, lbx, gyy, lbw, gbh, { style: pst, f: T.border, fill: panelFill, title: 'LOG', tf: T.dim, right: 'this run', rf: T.faint })
      const log = [['14:06', 'step 7 marked in progress', T.text], ['14:05', 'answer · step 6 · ADR-003 accepted', T.text], ['14:02', '▲ write gate held step 8', T.warn], ['13:58', 'spec-lookup returned 4 matches', T.dim], ['13:51', 'run continued from step 5', T.dim], ['13:49', 'session started · observe → enforce', T.faint]]
      log.forEach((l, k) => { put(t, lbx + 2, gyy + 1 + k, l[0], T.faint); put(t, lbx + 9, gyy + 1 + k, fit(l[1], lbw - 12), l[2]) })
    }
  }
  statusBar(t, T, W, H - 1, fuel, false, pmode)
  return t
}

function agents(t, T, theme, abx, y1, abw, list, ms) {
  let ay = y1 + 1
  const blink = Math.floor(ms / 500) % 2 === 0
  for (const a2 of list) {
    let ax = abx + 2
    const dc = a2.st === 'run' ? (blink ? T.run : mix(T.run, T.panel, 0.5)) : a2.st === 'fail' ? T.danger : T.ok
    put(t, ax, ay, a2.pre, T.faint); ax += len(a2.pre)
    put(t, ax, ay, '●', dc); ax += 2
    const room = abx + abw - 3 - len(a2.t) - 1 - ax
    if (a2.agent) put(t, ax, ay, fit(a2.txt, room), T.text)
    else {
      const sp = a2.txt.indexOf(' ')
      put(t, ax, ay, a2.txt.slice(0, sp), theme === 'C' ? T.accent : T.dim)
      put(t, ax + sp, ay, fit(a2.txt.slice(sp), Math.max(0, room - sp)), a2.st === 'fail' ? T.danger : T.dim)
    }
    putR(t, abx + abw - 3, ay, a2.t, a2.st === 'run' ? T.run : T.faint)
    ay++
  }
}

function drawDockTile(t, T, theme, i, p, x, y, w) {
  const acc = T.phase[i], st = p.st
  const bcol = st === 'done' ? T.done : st === 'prog' ? T.inprog : st === 'next' ? T.next : st === 'nb' ? T.notbuilt : T.border
  let inner
  if (theme === 'B') {
    const s0 = st === 'nb' ? 0.05 : (st === 'todo' ? 0.1 : 0.34), s1 = st === 'nb' ? 0.02 : 0.06
    inner = (ii, jj) => mix(mix(T.bg, T.bg2, (y + jj) / (t.H - 1)), acc, s0 + (s1 - s0) * (ii / Math.max(1, w - 3)))
  } else if (theme === 'A') inner = st === 'prog' ? mix(T.panel, T.accent, 0.13) : (st === 'nb' ? T.bg : T.panel)
  else inner = st === 'prog' ? '#140E00' : T.panel
  const style = st === 'nb' ? 'dash' : (theme === 'B' && st === 'prog' ? 'double' : T.tile)
  const fcol = ((theme === 'B' || theme === 'C') && (st === 'done' || st === 'prog' || st === 'next')) ? acc : bcol
  box(t, x, y, w, 3, { style, f: fcol, fill: inner })
  const r = y + 1
  let nx = x + 4
  if (theme === 'C') { put(t, x + 2, r, 'P' + (i + 1), st === 'nb' || st === 'todo' ? T.dim : acc); nx = x + 6 } else put(t, x + 2, r, p.g, st === 'nb' ? T.faint : acc)
  put(t, nx, r, p.n, st === 'nb' ? T.faint : T.text)
  put(t, x + 19, r, fit(p.doc, 14), st === 'nb' ? T.faint : T.dim)
  const sx = x + 35
  if (st === 'prog') {
    for (let k = 0; k < 10; k++) { const on = k < Math.round(10 * p.cur / p.tot); put(t, sx + k, r, on ? '█' : '░', on ? (theme === 'B' ? mix(T.phase[1], T.phase[3], k / 9) : acc) : T.faint) }
    put(t, sx + 11, r, p.cur + '/' + p.tot, T.text)
  } else if (st === 'done') { put(t, sx, r, '✓ done', theme === 'B' ? acc : T.done); put(t, sx + 8, r, p.dur, theme === 'C' ? T.done : T.faint) }
  else if (st === 'next') { if (theme === 'C') put(t, sx, r, '◉ NEXT ▸', T.next); else put(t, sx, r, ' NEXT ▸ ', T.ink, theme === 'A' ? T.accent : T.next); put(t, sx + 9, r, '~35m', T.dim) }
  else if (st === 'todo') put(t, sx, r, '○ ~50m est.', T.dim)
  else put(t, sx, r, '◌ coming soon', T.faint)
  putR(t, x + w - 3, r, '[' + (i + 1) + ']', st === 'nb' ? T.faint : T.dim)
}

function drawDock(theme, fuel, rpm, ms, mode, sp, pmode) {
  const T = THEMES[theme], W = 64, H = 48
  const bgAt = (x, y) => T.bg2 !== T.bg ? mix(T.bg, T.bg2, y / (H - 1)) : T.bg
  const t = term(W, H, bgAt, T.text)
  const panelFill = T.panel2 !== T.panel ? (i, j) => mix(T.panel, T.panel2, j / 14) : T.panel
  const pst = T.panelStyle
  fill(t, 0, 0, W, 1, T.bar)
  put(t, 1, 0, '◆ DevForgeAI Dashboard', T.accent)
  putR(t, W - 2, 0, T.name + ' · t', T.faint)
  put(t, 1, 1, 'ROUTE', T.dim)
  putR(t, W - 2, 1, '2 done · 1 in progress · [1-7]', T.faint)
  for (let i = 0; i < 7; i++) {
    const y = 2 + i * 3
    if (!BOX_TILES.on) drawDockTile(t, T, theme, i, PHASES[i], 1, y, W - 2)
    if (i < 6) put(t, 5, y + 2, '▼', PHASES[i].st === 'done' ? (theme === 'B' ? T.phase[i + 1] : T.done) : T.faint)
  }
  put(t, 1, 24, '▼ YOU ARE HERE · Architecture', T.accent)
  putR(t, W - 2, 24, ' ETA ~1 h 50 m to Epic ', T.ink, theme === 'C' ? T.accent : mix(T.accent, T.text, 0.15))
  box(t, 0, 25, W, 14, { style: pst, f: T.border, fill: panelFill, title: 'INSTRUMENTS', tf: T.dim, right: 'turn 57', rf: T.faint })
  dials(t, T, theme, 1, 26, 20, 9, 21, fuel, rpm, true, mode, sp)
  odometer(t, T, 2, 35, true, ms)
  putR(t, W - 3, 36, '$11.80', T.faint)
  box(t, 0, 39, W, 7, { style: pst, f: T.border, fill: panelFill, title: 'AGENTS', tf: T.dim, right: '3 live · 1 failed', rf: T.faint })
  agents(t, T, theme, 0, 39, W, [
    { pre: '', txt: 'main', st: 'run', t: '4m 12s', agent: true },
    { pre: '├─ ', txt: '◆ spec-lookup · 3 tools', st: 'done', t: '0:38', agent: true },
    { pre: '├─ ', txt: '◆ drafts-review', st: 'run', t: '1:05', agent: true },
    { pre: '│  └─ ', txt: 'Grep  "NEEDS ADR"', st: 'run', t: '...' },
    { pre: '└─ ', txt: '◆ eval-probe', st: 'done', t: '0:12', agent: true },
  ], ms)
  put(t, 1, 46, '◈ 5 mods', T.accent)
  put(t, 10, 46, '▲ write gate held step 8 · resolved ✓', T.warn)
  statusBar(t, T, W, 47, fuel, true, pmode)
  return t
}

export type Layout = 'wide' | 'compact' | 'dock'
export const SIZES = { wide: [160, 48], compact: [120, 36], dock: [64, 48] }

// The whole dashboard as Raster cells for one layout and one moment.
// fuel: the share of the context window still free, 100 right after /clear or a compaction.
// rpmLive: measured output tokens per second (null: the sample wander).
export function frame(theme: 'A' | 'B' | 'C', layout: Layout, ms: number, fuel: number, mode = 'pace', pmode = 'enforce', rpmLive: number | null = null): string {
  let sp = demoSpeed(mode, ms)
  if (rpmLive !== null) sp = { v: sp.spin ? 0.45 : sp.v, spin: false }
  const rpm = rpmLive !== null ? rpmLive : sp.spin ? 168 + 8 * Math.sin(ms / 300) : 100 + 80 * Math.sin(ms / 1300) * Math.sin(ms / 3100 + 1)
  const t = layout === 'dock' ? drawDock(theme, fuel, Math.max(0, rpm), ms, mode, sp, pmode) : drawWide(theme, layout === 'compact', fuel, Math.max(0, rpm), ms, mode, sp, pmode)
  const words = new Uint32Array(t.W * t.H * 3)
  let k = 0
  for (const row of t.rows) for (const c of row) {
    words[k++] = c.c.codePointAt(0)
    words[k++] = parseInt(c.f.slice(1), 16)
    words[k++] = parseInt(c.b.slice(1), 16)
  }
  return new Uint8Array(words.buffer).toBase64()
}
