# Plinko — Streamer Games

Classic Plinko board for streamers. Drop a disc from the top, watch it bounce off pegs, and land in a viewer's slot. Pure physics, pure entertainment.

## Quick Start

1. Open `index.html` in a browser (or add as an OBS Browser Source)
2. Add viewer names in the admin panel
3. Hit **Drop Disc** or press **Space**
4. Watch the disc bounce and pick a winner

## OBS Setup

Add as a Browser Source:
```
URL: /path/to/plinko/index.html?admin=false&bg=transparent
Width: 1280 (or your stream width)
Height: 720 (or your stream height)
```

Keep a separate admin window open:
```
URL: /path/to/plinko/index.html
```

## URL Parameters

| Parameter | Values | Default | Description |
|-----------|--------|---------|-------------|
| `admin` | `true` / `false` | `true` | Show/hide the admin panel |
| `bg` | `transparent` | — | Transparent background for OBS overlay |
| `theme` | `dark` / `light` / `neon` | `dark` | Color theme |
| `names` | `comma,separated` | — | Pre-load player names |

**Examples:**
```
index.html?names=Alice,Bob,Carol,Dave
index.html?theme=neon&admin=false&bg=transparent
index.html?names=Alice,Bob&theme=light
```

## Admin Panel Controls

| Control | Description |
|---------|-------------|
| **Drop Disc** / Space | Drop a new disc (starts a session) |
| **Mode: Random** | Drop at a random position along the top |
| **Mode: Click** | Click near the top of the board to choose drop position |
| **Drops ×1/3/5/10** | How many discs to drop in a session |
| **Board: Small/Medium/Large** | 8, 10, or 12 rows of pegs |
| **Add / Bulk Add** | Add viewer names (one per line for bulk) |
| **Reset Results** | Clear drop history and tallies |
| **Clear All** | Remove all players |

## Game Flow

1. Add viewer names — each name gets its own slot at the bottom
2. Choose drop mode (Random = auto, Click = you pick the spot)
3. Press Space or click **Drop Disc**
4. The disc falls, bouncing off metallic pegs
5. It lands in a slot — that viewer wins!
6. For multi-drop: keep going until all drops are done, tally shows who won most

## postMessage API

Control Plinko from a parent page or chat bot:

```javascript
const frame = document.getElementById('plinko-frame');
const win   = frame.contentWindow;

// Add a viewer
win.postMessage({ type: 'plinko:add', name: 'Alice' }, '*');

// Add multiple viewers at once
win.postMessage({ type: 'plinko:add', names: ['Alice', 'Bob', 'Carol'] }, '*');

// Remove a viewer
win.postMessage({ type: 'plinko:remove', name: 'Alice' }, '*');

// Clear all viewers
win.postMessage({ type: 'plinko:clear' }, '*');

// Drop at random position
win.postMessage({ type: 'plinko:drop' }, '*');

// Drop at specific position (0 = left, 0.5 = center, 1 = right)
win.postMessage({ type: 'plinko:drop', position: 0.5 }, '*');

// Query current player list
win.postMessage({ type: 'plinko:names' }, '*');

// Listen for winner announcements
window.addEventListener('message', (e) => {
  if (e.data.type === 'plinko:winner') {
    console.log('Winner:', e.data.winner);
  }
  if (e.data.type === 'plinko:names') {
    console.log('Players:', e.data.names);
  }
});
```

### Inbound Messages

| Type | Payload | Description |
|------|---------|-------------|
| `plinko:add` | `{name}` or `{names:[...]}` | Add one or many players |
| `plinko:remove` | `{name}` | Remove a player |
| `plinko:clear` | — | Remove all players |
| `plinko:drop` | `{position?}` | Drop a disc (position 0–1 optional) |
| `plinko:names` | — | Request current player list |

### Outbound Messages

| Type | Payload | Description |
|------|---------|-------------|
| `plinko:winner` | `{winner: 'name'}` | Emitted when disc lands |
| `plinko:names` | `{names: [...]}` | Response to `plinko:names` query |

## Physics

- Canvas 2D with sub-step collision detection (4 steps/frame)
- Triangular peg layout: alternating wide rows (N pegs) and narrow rows (N-1 pegs)
- Gravity: 0.38 px/frame² — disc accelerates naturally
- Peg bounce restitution: 0.48 (satisfying mid-bounce feel)
- Wall restitution: 0.65 (slight energy loss on edge hits)
- Terminal velocity cap: 18 px/frame
- Glow trail follows disc trajectory (16-frame history)
- Peg flash on hit for visual feedback

## Slot Layout

- Number of slots = number of players (min 3, max 20)
- Slots are equally sized and adapt to the board width
- Each player gets a unique color (20-color palette)
- Winning slot pulses gold on landing
- Confetti burst from the winning slot

## Testing

Open `test.html` in a browser. It embeds the game in an iframe and runs 8 automated tests covering:
- Single and bulk name add
- Remove and clear
- postMessage winner announcement
- Drop at specific position
- URL parameter name preloading

## License

MIT — use it however you want.
