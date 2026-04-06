# RPS Battle

A tournament-bracket Rock Paper Scissors game for live streamers. Viewers join via chat, get paired into a bracket, and pick their move each round. The bracket fills in as winners advance, with animated hand reveals and a crowned champion.

---

## Files

| File | Purpose |
|------|---------|
| `index.html` | The game — fully self-contained, no external dependencies |
| `test.html` | postMessage API test harness with 12 automated tests |
| `README.md` | This file |

---

## OBS Setup

1. Add a **Browser Source** in OBS
2. Set URL to the full path: `file:///path/to/rps-battle/index.html?admin=false&bg=transparent`
3. Set width/height to match your scene (recommended: 1280×720 or 1920×1080)
4. Check **"Shutdown source when not visible"** to save resources

For the admin view (on your local monitor, not captured), open the file normally in a browser with `?admin=true`.

---

## URL Parameters

| Parameter | Values | Default | Description |
|-----------|--------|---------|-------------|
| `admin` | `true` / `false` | `true` | Show or hide the admin panel |
| `bg` | `transparent` | — | Transparent background for OBS overlay use |
| `theme` | `dark` / `light` / `neon` | `dark` | Color theme |
| `names` | comma-separated list | — | Pre-load player names on startup |

**Example:** `index.html?admin=false&bg=transparent&theme=neon&names=Alice,Bob,Carol,Dave`

---

## postMessage API

The game communicates with a parent window or bot via `window.postMessage`. All message types are prefixed with `rps:`.

### Inbound (bot → game)

```javascript
// Add a player (viewer joins)
{ type: 'rps:join', name: 'Alice' }

// Submit a pick for the current match
{ type: 'rps:pick', name: 'Alice', choice: 'rock' }   // rock | paper | scissors

// Start the tournament (must have 2+ players)
{ type: 'rps:start' }

// Request current bracket/result info
{ type: 'rps:result' }

// Remove all players and reset
{ type: 'rps:clear' }

// Query the current player list
{ type: 'rps:names' }
```

### Outbound (game → parent)

```javascript
// Tournament champion crowned
{ type: 'rps:winner', winner: 'Alice' }

// A match result (fires after each completed match)
{ type: 'rps:result', player1: 'Alice', player2: 'Bob', p1choice: 'rock', p2choice: 'scissors', winner: 'Alice' }

// Response to rps:names query
{ type: 'rps:names', names: ['Alice', 'Bob', 'Carol'] }
```

---

## Chat Bot Integration

### Twitch / StreamElements example

```javascript
// Viewer types: !join
// Bot sends:
iframe.contentWindow.postMessage({ type: 'rps:join', name: username }, '*');

// Viewer types: !rock (or !paper / !scissors)
iframe.contentWindow.postMessage({ type: 'rps:pick', name: username, choice: 'rock' }, '*');

// Streamer types: !startrps
iframe.contentWindow.postMessage({ type: 'rps:start' }, '*');

// Listen for results
window.addEventListener('message', e => {
  if (e.data.type === 'rps:winner') {
    chat.say(`🏆 ${e.data.winner} wins the RPS Tournament!`);
  }
  if (e.data.type === 'rps:result') {
    chat.say(`${e.data.player1} (${e.data.p1choice}) vs ${e.data.player2} (${e.data.p2choice}) → ${e.data.winner} advances!`);
  }
});
```

---

## Tournament Structure

- Players are shuffled and seeded into a bracket padded to the next power of 2 (e.g., 6 players → 8-slot bracket with 2 byes)
- Bye slots auto-advance; only real player vs. player matchups are shown on the VS screen
- Each round: both players in a match must submit their choice
- Draw: match replays automatically until a winner is decided
- The bracket visualization updates live as winners are filled in
- Final match winner is announced with a champion screen + confetti

---

## Admin Panel Controls

| Control | Action |
|---------|--------|
| Player name input | Add a single player |
| Bulk paste box | Add multiple players (one per line) |
| Start Tournament | Shuffles and brackets all current players |
| Simulate Round | Auto-picks random choices for the current match |
| Next Match | Advance to the next match in the bracket |
| Sound toggle | Enable / disable all audio |
| Theme switcher | Dark / Light / Neon |
| Clear All | Remove all players and reset tournament |
| ⚙ gear button | Toggle admin panel visibility |
| G key | Keyboard shortcut to toggle admin panel |
| Spacebar | Start tournament (when 2+ players registered) |

---

## RPS Logic

```javascript
const beats = { rock: 'scissors', scissors: 'paper', paper: 'rock' };

function getWinner(p1, p1choice, p2, p2choice) {
  if (p1choice === p2choice) return null;  // draw — replay
  return beats[p1choice] === p2choice ? p1 : p2;
}
```

---

## Audio (Web Audio API)

All sounds are generated in real-time — no audio files required.

| Event | Sound |
|-------|-------|
| Player joins | Two ascending tones |
| Match reveal | Noise burst + metallic ping clash |
| Winner announced | Multi-note crowd cheer |
| Player eliminated | Descending sawtooth tones |

Sound can be toggled off from the admin panel at any time.

---

## Testing

Open `test.html` in a browser. The harness embeds the game in an iframe and provides:

- **Manual buttons** for every postMessage command
- **Pick buttons** that auto-read the current match players from the iframe DOM
- **URL param tests** (neon theme, transparent bg, ?names= pre-load, ?admin=false)
- **Automated test suite** (12 tests) covering:
  1. Frame loads correctly
  2. `rps:clear` resets state
  3. `rps:join` adds players
  4. Duplicate player rejected
  5. `rps:start` shows VS screen
  6. Pick submission shows indicator
  7. Both picks emit `rps:result`
  8. XSS-safe player names
  9. `?theme=neon` applied correctly
  10. `?names=` pre-loads players
  11. `?admin=false` hides panel
  12. Full 2-player tournament emits `rps:winner`

---

## Technical Notes

- Single HTML file — all CSS and JS inline, no external dependencies
- No frameworks — pure HTML/CSS/JS
- `'use strict'` + IIFE — no global scope pollution
- All user input escaped before DOM insertion (XSS-safe)
- `overflow: hidden` — no scrollbars, safe for OBS browser source
- Responsive layout — flex-based, scales to any resolution
- LocalStorage not used (tournament state is in-memory; fresh each load)
