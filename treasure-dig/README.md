# Treasure Dig

A grid-based treasure hunting game for streamers. Viewers call out coordinates to dig — one tile hides a treasure chest. The viewer who finds it wins.

---

## How It Works

A configurable grid (6×6 to 10×10) of covered dirt tiles is shown on stream. One randomly placed tile hides a treasure chest. Viewers submit coordinate guesses (e.g. `B3`) via chat bot. Tiles are revealed as digs happen — most show empty dirt or rocks, one reveals the glowing treasure chest.

---

## Coordinate System

Columns are labeled **A–J** (left to right). Rows are labeled **1–10** (top to bottom).

```
    A   B   C   D   E   F   G   H
  ┌───┬───┬───┬───┬───┬───┬───┬───┐
1 │   │   │   │   │   │   │   │   │
  ├───┼───┼───┼───┼───┼───┼───┼───┤
2 │   │   │ X │   │   │   │   │   │  ← B3 would be column B, row 3
  ├───┼───┼───┼───┼───┼───┼───┼───┤
3 │   │   │   │   │   │   │   │   │
  └───┴───┴───┴───┴───┴───┴───┴───┘
```

**Examples:**
- `A1` = top-left corner
- `H1` = top-right corner (on 8×8)
- `D5` = column D, row 5
- `B3` = column B, row 3

Valid range depends on grid size:
| Size | Columns | Rows |
|------|---------|------|
| 6×6  | A–F     | 1–6  |
| 7×7  | A–G     | 1–7  |
| 8×8  | A–H     | 1–8  |
| 9×9  | A–I     | 1–9  |
| 10×10| A–J     | 1–10 |

---

## URL Parameters

| Parameter | Values              | Default | Description                          |
|-----------|---------------------|---------|--------------------------------------|
| `theme`   | `dark`/`light`/`neon` | `dark` | Color theme                         |
| `admin`   | `true`/`false`      | `true`  | Show/hide admin panel                |
| `bg`      | `transparent`       | —       | Transparent background (OBS)         |
| `size`    | `6`–`10`            | `8`     | Initial grid size                    |

**Examples:**
```
index.html                          → 8×8 dark, admin shown
index.html?size=10&theme=neon       → 10×10 neon theme
index.html?admin=false&bg=transparent → OBS browser source, no panel
```

---

## OBS Setup

1. Add a **Browser Source** in OBS
2. Point it to `index.html?admin=false&bg=transparent`
3. Set width/height to match your layout (e.g. 800×800)
4. The game area fills the space; the grid auto-scales

To control the game from a bot or second window, send postMessage events from a parent page or use the admin panel controls.

---

## postMessage API

The game communicates via `window.postMessage`. All messages use the `treasure:` namespace.

### Inbound (bot → game)

**Start/reset a game:**
```javascript
iframe.contentWindow.postMessage({ type: 'treasure:reset' }, '*');
```

**Dig a tile (viewer submits a coordinate):**
```javascript
iframe.contentWindow.postMessage({
  type: 'treasure:dig',
  name: 'ViewerName',   // string — viewer's display name
  coord: 'B3'           // string — coordinate in A1 format (case-insensitive)
}, '*');
```

**Resize the grid (starts a new game at new size):**
```javascript
iframe.contentWindow.postMessage({
  type: 'treasure:resize',
  size: 8    // number — 6 through 10
}, '*');
```

### Outbound (game → parent)

Listen on the parent window:
```javascript
window.addEventListener('message', e => {
  const msg = e.data;
  if (msg.type === 'treasure:winner') {
    console.log(`${msg.winner} found treasure at ${msg.coord}!`);
  }
  if (msg.type === 'treasure:miss') {
    console.log(`${msg.name} dug ${msg.coord} — nothing there`);
  }
});
```

**treasure:winner** — fired when the treasure tile is dug:
```json
{ "type": "treasure:winner", "winner": "ViewerName", "coord": "D4" }
```

**treasure:miss** — fired for every dig that does not find treasure:
```json
{ "type": "treasure:miss", "name": "ViewerName", "coord": "B3" }
```

---

## Admin Panel Controls

| Control         | Description                                        |
|-----------------|----------------------------------------------------|
| Grid size buttons | Switch between 6×6 – 10×10 (starts new game)    |
| New Game        | Place treasure randomly, reset all tiles           |
| Show All        | Reveal treasure location (semi-transparent peek)   |
| Manual dig      | Type a coord + name and click Dig                  |
| Sound toggle    | Enable/disable Web Audio sound effects             |
| Theme buttons   | Switch dark / light / neon themes live             |

---

## Sound Effects

All audio is generated via Web Audio API — no external files required.

| Event        | Sound                                          |
|--------------|------------------------------------------------|
| Tile dig     | Low-frequency thud + dirt crumble noise        |
| Rock reveal  | Metallic double clink                          |
| Treasure found | Ascending 5-note triumphant arpeggio + shimmer |

---

## Tile States

| State    | Visual                                    |
|----------|-------------------------------------------|
| Covered  | Brown dirt gradient with subtle texture   |
| Empty    | Dark recessed square (dug out)            |
| Rock     | Grey gradient + rock emoji (🪨)           |
| Treasure | Glowing gold pulsing chest (💰) + glow    |

Rock tiles appear at ~25% probability on misses. All other misses are empty.

---

## Example Bot Integration (pseudocode)

```javascript
// When a viewer types "!dig B3" in chat:
chatBot.onCommand('dig', (viewer, args) => {
  const coord = args[0];
  gameFrame.contentWindow.postMessage({
    type: 'treasure:dig',
    name: viewer.displayName,
    coord: coord
  }, '*');
});

// Announce winner in chat:
window.addEventListener('message', e => {
  if (e.data.type === 'treasure:winner') {
    chatBot.say(`🎉 ${e.data.winner} found the treasure at ${e.data.coord}! GG!`);
    streamOverlay.triggerAlert('winner', e.data.winner);
  }
});
```

---

## Files

| File         | Description                           |
|--------------|---------------------------------------|
| `index.html` | The game — self-contained, no deps   |
| `test.html`  | postMessage API test harness          |
| `README.md`  | This file                             |

---

## License

MIT — part of the [Streamer Games](../) collection.
