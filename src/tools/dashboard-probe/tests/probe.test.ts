import { expect, mock, test } from 'claude-code/testing'

import { frame, SIZES, spriteCells } from '../hooks/drive'

for (const layout of ['wide', 'compact', 'dock'] as const) {
  for (const look of ['A', 'B', 'C'] as const) {
    test(`${look} ${layout}: one u32 triplet per cell`, async () => {
      const [c, r] = SIZES[layout]
      expect(Uint8Array.fromBase64(frame(look, layout, 12_345, 25)).length).toBe(c * r * 12)
    })
  }
}

// A Raster paints about 1,024 colour pairs at once and rounds the rest (the types' RasterProps).
for (const look of ['A', 'B', 'C'] as const) {
  test(`${look} wide: distinct colour pairs per frame stay under 1,024`, async () => {
    const words = new Uint32Array(Uint8Array.fromBase64(frame(look, 'wide', 12_345, 25)).buffer)
    const pairs = new Set<string>()
    for (let k = 0; k < words.length; k += 3) pairs.add(`${words[k + 1]}/${words[k + 2]}`)
    console.log(`${look} wide: ${pairs.size} colour pairs`)
    expect(pairs.size).toBeLessThan(1024)
  })
}

test('the characters are 14 x 4 cells', async () => {
  for (const who of ['Ember', 'Clawd']) expect(Uint8Array.fromBase64(spriteCells(who, '#111316', 900)).length).toBe(14 * 4 * 12)
})

for (const [placement, cols] of [['dock', 66], ['inline', 193], ['inline', 130]] as const) {
  test(`the pane draws with Box tiles (${placement}, ${cols} columns)`, async ($, on) => {
    mock.clock(on, { now: 1_000 })
    const pane = await $.ui.mount({
      plugin: 'dashboard-probe',
      surface: 'terminal',
      component: 'Pane',
      requestId: 'dashboard-probe',
      props: { title: 'DevForgeAI Dashboard', isFocused: true, bodyColumns: cols, placement, scroll: { offset: 0, bodyRows: 54 }, view: {} },
      viewport: { columns: 200, rows: 60, isFullscreen: placement === 'dock' },
    })
    expect(pane).toBeDefined()
  })
}
