# Hot Potato 🥔

A streamer elimination game. Players are arranged in a ring — a glowing potato passes between them at increasing speed. When the hidden timer fires, whoever is holding the potato is eliminated with an explosion. Last player standing wins.

## Quick Start

Open `index.html` in any modern browser. No install, no server, no build step required.

## OBS Setup

Add a **Browser Source**:
- URL: `file:///path/to/hot-potato/index.html?bg=transparent&admin=false`
- Width: 1920, Height: 1080 (or your stream resolution)
- Custom CSS: *(leave blank)*

For the admin panel (private view), open in a regular browser window without `?admin=false`.

## URL Parameters

| Parameter | Values | Description |
|-----------|--------|-------------|
| `admin` | `true` / `false` | Show/hide admin panel. Default: `true` |
| `bg` | `transparent` | Transparent background for OBS overlay |
| `theme` | `dark` / `light` / `neon` | Color theme. Default: `dark` |
| `names` | `Alice,Bob,Carol` | Pre-load comma-separated names on startup |

### Examples

```
# OBS overlay — transparent, no panel
index.html?bg=transparent&admin=false

# Pre-load 6 names in neon theme
index.html?theme=neon&names=Alice,Bob,Carol,Dave,Eve,Frank

# Light theme with admin visible
index.html?theme=light
```

## Admin Panel

The right-side panel (⚙ to toggle) lets you:

- **Add players** — type a name and press Enter or click Add
- **Bulk add** — paste one name per line
- **Remove** — click × on any name to remove
- **Starting speed** — Slow / Normal / Fast (affects how fast the potato initially passes)
- **Sound toggle** — enable/disable all audio
- **Clear All** — remove all players (only when game is not running)
- **Start / Spacebar** — launch the game

Press **Spacebar** anywhere (outside a text input) to start or reset the game.

## Bot Integration (postMessage API)

The game communicates via `window.postMessage` with namespace prefix `potato:`.

### Inbound Messages (bot → game)

```javascript
// Add a single player
{ type: 'potato:join', name: 'StreamerFan99' }

// Start the game
{ type: 'potato:start' }

// Force-eliminate a specific player (triggers explosion animation)
{ type: 'potato:eliminated', name: 'StreamerFan99' }

// Force the game to end and declare winner immediately
{ type: 'potato:winner' }

// Reset game and clear all players
{ type: 'potato:clear' }

// Query current player list
{ type: 'potato:names' }
```

### Outbound Messages (game → parent)

```javascript
// A player was eliminated
{ type: 'potato:eliminated', name: 'StreamerFan99' }

// Game over — last player standing
{ type: 'potato:winner', winner: 'Alice' }

// Response to potato:names query
{ type: 'potato:names', names: ['Alice', 'Bob', 'Carol'] }
```

### Embedding Example

```html
<iframe id="game" src="hot-potato/index.html?admin=false&bg=transparent"></iframe>
<script>
const frame = document.getElementById('game');

// Add players as chat joins
function onChatJoin(username) {
  frame.contentWindow.postMessage({ type: 'potato:join', name: username }, '*');
}

// Start when streamer types !hotpotato
function onStartCommand() {
  frame.contentWindow.postMessage({ type: 'potato:start' }, '*');
}

// Listen for results
window.addEventListener('message', e => {
  if (e.source !== frame.contentWindow) return;
  const { type, winner, name } = e.data;
  if (type === 'potato:winner') {
    announceInChat(`${winner} wins Hot Potato! 🏆`);
  }
  if (type === 'potato:eliminated') {
    announceInChat(`${name} got burned! 💥`);
  }
});
</script>
```

## Game Mechanics

### Ring Layout
Players are positioned evenly around a circle using polar-to-Cartesian conversion. The ring automatically re-sizes for the number of players and re-animates after each elimination.

### Potato Passing
- The potato emoji (🥔) moves between player cards with a CSS transition
- Each pass interval starts at the configured speed and accelerates by ~9% per pass
- The current holder's card glows orange/red and scales up
- At high heat levels (>75%), the card shakes and the potato gains flames

### Hidden Timer
The bomb timer is randomized — the streamer cannot see it. Duration scales with player count:
- More players = longer rounds (more time to build tension)
- Range roughly: `(3s + n×0.6s)` to `(6s + n×1.2s)` where n = alive player count

### Heat Meter
A visual bar at the bottom tracks passing speed (0% = slow, 100% = maximum speed). The potato glow intensifies as heat increases.

### Explosion
When the timer fires:
- 12 emoji particles burst outward from the holder's position
- A shockwave ring expands and fades
- The holder's card shakes, then dims and grays out with a ✕ badge
- The ring re-forms with remaining players
- Audio: low boom + noise burst

### Winner
- Last player standing gets a gold crown and pulsing glow
- Firework particles burst across the screen
- Winner overlay with name and trophy
- `potato:winner` event fires to parent

## Audio

All sounds are generated with the Web Audio API — no external files required.

| Moment | Sound |
|--------|-------|
| Each pass | Ticking click that rises in pitch as speed increases |
| High heat | White noise sizzle |
| Explosion | Low boom + noise burst |
| Winner | Ascending chime: C-E-G-C |

Sound can be toggled in the admin panel.

## Themes

| Theme | Description |
|-------|-------------|
| `dark` | Default. Deep navy/purple with orange potato glow |
| `light` | Light gray/white surface, same accent colors |
| `neon` | Black background, cyan accent, magenta gold, vivid potato |

## Keyboard Shortcut

| Key | Action |
|-----|--------|
| Spacebar | Start game (or reset if game over) |

## Browser Compatibility

Tested and working in Chrome, Firefox, Edge, and Safari. Requires Web Audio API support (all modern browsers).

## Files

```
hot-potato/
├── index.html   — The game (fully self-contained)
├── test.html    — postMessage API test harness with 12 automated tests
└── README.md    — This file
```

## Testing

Open `test.html` to access the full test harness. It provides:
- Buttons for every postMessage command
- Theme and URL parameter reload testing
- Automated test suite (12 tests) covering: load, join, names query, duplicate rejection, start, elimination events, UI states, winner event, clear, and XSS safety
- Live message log showing all inbound and outbound postMessage traffic
