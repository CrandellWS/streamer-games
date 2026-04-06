# Elimination

Pure random elimination game for live streamers. Names appear in a grid, a dramatic spotlight sweeps between them, and one player is eliminated at a time with a satisfying shatter animation. Last one standing wins.

## Quick Start

Open `index.html` in a browser — no build step, no server required.

For OBS: Add a Browser Source pointing to `index.html?bg=transparent&admin=false`.

---

## URL Parameters

| Parameter | Values | Default | Description |
|-----------|--------|---------|-------------|
| `admin` | `true` / `false` | `true` | Show or hide the admin control panel |
| `bg` | `transparent` | — | Transparent background for OBS overlay |
| `theme` | `dark` / `light` / `neon` | `dark` | Color theme |
| `names` | `Alice,Bob,Charlie` | — | Pre-load player names on page open |

### Example URLs

```
# OBS overlay — transparent, no panel, dark theme
index.html?bg=transparent&admin=false

# Pre-loaded names, neon theme
index.html?names=Alice,Bob,Charlie,Diana&theme=neon

# Light theme with panel
index.html?theme=light
```

---

## Admin Panel Controls

| Control | Description |
|---------|-------------|
| **Names list** | Type a name + Enter or click + to add. Click × to remove. |
| **Bulk Add** | Paste one name per line (or comma-separated) and click Add All. |
| **Speed** | Dramatic (3s sweep), Normal (1.5s sweep), Fast (rapid-fire) |
| **Start Elimination** | Begins the game. Spacebar also works. |
| **Eliminate Next** | Manually trigger the next elimination (useful for dramatic pacing). |
| **Reset Game** | Returns to ready state with current names intact. |
| **Sound** | Toggle Web Audio effects on/off. |
| **Theme** | Switch between Dark, Light, and Neon themes. |

---

## Keyboard Shortcuts

| Key | Action |
|-----|--------|
| `Space` | Start elimination (when not started) |
| `Enter` | Eliminate next (when running) |
| `G` | Toggle admin panel |

---

## postMessage API

All messages use the namespace prefix `eliminate:`.

### Inbound (bot → game)

```javascript
// Add a single player
window.postMessage({ type: 'eliminate:join', name: 'Alice' }, '*');

// Start the game
window.postMessage({ type: 'eliminate:start' }, '*');

// Set elimination speed
window.postMessage({ type: 'eliminate:speed', speed: 'fast' }, '*');
// speed values: 'fast' | 'normal' | 'dramatic' | 'slow' (alias for dramatic)

// Query the winner (responds if game is done)
window.postMessage({ type: 'eliminate:winner' }, '*');

// Query current name list
window.postMessage({ type: 'eliminate:names' }, '*');

// Clear all names and reset
window.postMessage({ type: 'eliminate:clear' }, '*');
```

### Outbound (game → parent)

```javascript
// Winner declared
{ type: 'eliminate:winner', winner: 'Alice' }

// Player eliminated
{ type: 'eliminate:eliminated', name: 'Bob' }

// Current name list (response to join or names query)
{ type: 'eliminate:names', names: ['Alice', 'Bob', 'Charlie'] }
```

---

## Game Flow

1. **Ready** — Names appear as pill cards in a grid.
2. **Spotlight sweep** — A golden highlight cycles through players, speeding up or slowing down based on the speed setting.
3. **Victim lock** — The spotlight lands on a player; their card turns red and shakes.
4. **Shatter** — The victim card shatters and fades out. Card stays greyed with strikethrough.
5. **Repeat** — Continues until 2 players remain.
6. **Final Showdown** — Special banner + gold animation when 2 players remain.
7. **Winner** — Final elimination triggers crown animation, particle explosion, and trumpets.

---

## Speed Modes

| Mode | Spotlight sweep | Victim pause | Screen flash |
|------|----------------|--------------|--------------|
| **Dramatic** | ~3s (16–28 sweeps at 120ms) | 2.2s | Yes |
| **Normal** | ~1.5s (10–18 sweeps at 65ms) | 0.85s | No |
| **Fast** | ~0.5s (6–10 sweeps at 28ms) | 0.3s | No |

---

## OBS Setup

1. Add a **Browser Source** in OBS.
2. Point it to `elimination/index.html?bg=transparent&admin=false`.
3. Set width/height to match your scene (1920×1080 recommended).
4. Check **Shutdown source when not visible** to reset between streams.
5. Use a separate window with `admin=true` for game control off-stream.

For bot integration, load the page in the same Browser Source and communicate via postMessage from a browser extension or local server.

---

## Theming

Three built-in themes:

| Theme | Background | Accent | Gold |
|-------|-----------|--------|------|
| **dark** (default) | `#0d0d14` | Purple `#7c5cfc` | Yellow `#ffd700` |
| **light** | `#f0f0f5` | Purple `#7c5cfc` | Yellow `#ffd700` |
| **neon** | `#0a0a0a` | Cyan `#00ffcc` | Magenta `#ff00ff` |

Switch via URL `?theme=neon`, the admin panel buttons, or `data-theme` attribute on `<html>`.

---

## Audio

All sounds are generated via Web Audio API — no external files required.

| Event | Sound |
|-------|-------|
| Game start | Drumroll |
| Spotlight sweep | Per-tick click |
| Player eliminated | Buzz + noise burst |
| Final Showdown | Rising fanfare + deep boom |
| Winner | Triumphant fanfare + gold shimmer tones |

---

## Data Persistence

Player names are saved to `localStorage` under key `elimination_names` and restored on reload.

---

## Browser Compatibility

Requires a modern browser with:
- Web Audio API
- CSS animations + custom properties
- `window.postMessage`

Chrome 90+, Firefox 88+, Edge 90+, Safari 15+ all supported.
