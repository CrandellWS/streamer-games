# Dice Roll

A live streamer dice-rolling game. Viewers join the pool, each player rolls a configurable number of dice (1–3), and the highest total wins. Ties are automatically re-rolled until there is a single winner.

---

## OBS / Browser Source Setup

1. Add a **Browser Source** in OBS.
2. Point it at `dice-roll/index.html` (local file or hosted URL).
3. Recommended resolution: **1280×720** or **1920×1080**.
4. For chroma-key / transparent overlay: append `?bg=transparent` to the URL.
5. To hide the admin panel in the stream view: append `?admin=false`.

---

## URL Parameters

| Parameter | Values | Default | Description |
|-----------|--------|---------|-------------|
| `admin`   | `true` / `false` | `true` | Show or hide the admin control panel |
| `bg`      | `transparent` | — | Transparent background (OBS overlay mode) |
| `theme`   | `dark` / `light` / `neon` | `dark` | Color theme |
| `names`   | `Alice,Bob,Charlie` | — | Pre-load player names (comma-separated) |
| `dice`    | `1` / `2` / `3` | `1` | Number of dice each player rolls |

### Example URLs

```
# Dark theme, 2 dice, admin visible
index.html?dice=2

# OBS overlay — transparent, no admin panel, neon theme
index.html?bg=transparent&admin=false&theme=neon

# Pre-load names for testing
index.html?names=Alice,Bob,Charlie,Diana&dice=3&theme=dark
```

---

## Admin Panel Controls

| Control | Description |
|---------|-------------|
| Player list | Shows all current players with × remove buttons |
| Add player input | Type a name and press Enter or click Add |
| Bulk paste textarea | Paste multiple names (one per line) then click Add All |
| Dice Per Player | 1 / 2 / 3 — segment selector |
| Roll All | Starts the roll for all players; also triggered by **Space bar** |
| Sound toggle | Enable / disable all Web Audio sounds |
| Theme | Cycle through dark → light → neon |
| Gear (⚙) button | Show/hide the admin panel |

---

## postMessage API

The game communicates with a parent page or bot via `window.postMessage`.

### Namespace

All messages use the `dice:` prefix.

---

### Inbound (bot → game)

Send these from your bot/overlay controller to the iframe:

```javascript
const frame = document.getElementById('game-iframe');

// Add a single player (e.g. viewer !join command)
frame.contentWindow.postMessage({ type: 'dice:join', name: 'username' }, '*');

// Trigger a roll
frame.contentWindow.postMessage({ type: 'dice:roll' }, '*');

// Inject an external result for a player (bypasses animation)
frame.contentWindow.postMessage({
  type: 'dice:result',
  name: 'username',
  rolls: [4, 2]   // array length must match current diceCount
}, '*');

// Reset — clears all players and scores
frame.contentWindow.postMessage({ type: 'dice:reset' }, '*');

// Query current player list (game responds with dice:names)
frame.contentWindow.postMessage({ type: 'dice:names' }, '*');
```

---

### Outbound (game → parent)

Listen for these on the parent window:

```javascript
window.addEventListener('message', e => {
  const msg = e.data;
  if (!msg || !msg.type) return;

  switch (msg.type) {

    case 'dice:winner':
      // Fired when a winner is determined (after all tie-breaks)
      console.log(msg.winner);  // string — winning player's name
      console.log(msg.rolls);   // number[] — winning player's dice values
      console.log(msg.total);   // number — sum of rolls
      break;

    case 'dice:names':
      // Fired whenever the player list changes, and in response to a dice:names query
      console.log(msg.names);   // string[] — current player names in leaderboard order
      break;
  }
});
```

---

## Game Flow

1. **Join phase** — viewers type a chat command (e.g. `!join`). Bot sends `dice:join` for each one.
2. **Roll** — streamer clicks Roll All or presses Space (or bot sends `dice:roll`).
3. **Animation** — CSS 3D dice tumble for ~1.5s with physics bounce and rattle sound.
4. **Leaderboard** — players sorted by total descending. Winner gets crown + gold glow.
5. **Tie-break** — if two or more players tie, the game automatically re-rolls only the tied players and repeats until one winner emerges.
6. **Announce** — `dice:winner` fires. Bot can announce in chat.
7. **Reset** — `dice:reset` to clear for the next round.

---

## Bot Integration Example (Twitch / StreamElements)

```javascript
// Example: chat command !dice
// Bot calls this when a viewer types !dice
function onViewerJoin(username) {
  gameFrame.contentWindow.postMessage({ type: 'dice:join', name: username }, '*');
}

// Streamer presses a stream deck button → roll
function onStreamDeckRoll() {
  gameFrame.contentWindow.postMessage({ type: 'dice:roll' }, '*');
}

// Handle winner
window.addEventListener('message', e => {
  if (e.data?.type === 'dice:winner') {
    sendChatMessage(`🏆 ${e.data.winner} wins with a total of ${e.data.total}! (rolls: ${e.data.rolls.join(', ')})`);
  }
});
```

---

## Themes

| Theme | Description |
|-------|-------------|
| `dark` | Default — deep navy/purple, purple accent, gold winner highlight |
| `light` | Light grey background, white surfaces, same accent palette |
| `neon` | Pure black background, cyan accent, magenta winner highlight |

---

## Dice Faces

Each die is a genuine CSS 3D cube with all six faces rendered using pip dot grids:

| Face | Pip Layout |
|------|-----------|
| 1 | Center |
| 2 | Top-right + bottom-left |
| 3 | Top-right + center + bottom-left |
| 4 | All four corners |
| 5 | All four corners + center |
| 6 | Left column × 3 + right column × 3 |

---

## Audio (Web Audio API)

All sounds are synthesized in JavaScript — no external audio files required.

| Sound | Trigger |
|-------|---------|
| Dice rattle | Start of roll — 18 randomized square-wave ticks decreasing in volume |
| Table bounce | Landing — 5 triangle-wave thuds at natural bounce intervals |
| Winner chime | Winner confirmed — 4-note ascending sine chord (C5-E5-G5-C6) |
| Tie tone | Tie detected — descending sawtooth pair (440 → 330 Hz) |

Sound can be toggled off in the admin panel.

---

## Technical Notes

- Single HTML file, all CSS and JS inline — no external dependencies, works offline
- No frameworks, no build step
- `'use strict'` + IIFE — no global namespace pollution
- All user input is XSS-escaped before rendering
- `overflow: hidden` on body — no scrollbars at any resolution
- Ambient idle dice drift upward in the background when no round is active
- LocalStorage is not used — state resets on page load (intentional for streamer use)
