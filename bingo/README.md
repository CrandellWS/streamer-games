# Bingo — Streamer Games

A retro bingo hall game for live streamers. Viewers join and receive unique 5×5 bingo cards. The host draws balls; the first viewer to complete a row, column, or diagonal wins.

## Quick Start

Open `index.html` directly in a browser — no server required.

For OBS use, add a **Browser Source** pointed at the file path:
```
file:///path/to/streamer-games/bingo/index.html?admin=false&bg=transparent
```

---

## URL Parameters

| Parameter | Values | Default | Description |
|-----------|--------|---------|-------------|
| `admin` | `true` / `false` | `true` | Show or hide the admin control panel |
| `bg` | `transparent` | — | Transparent background for OBS overlays |
| `theme` | `dark` / `light` / `neon` | `dark` | Color theme |
| `names` | `Alice,Bob,Carol` | — | Pre-load comma-separated player names on load |

**Examples:**
```
index.html
index.html?theme=neon
index.html?admin=false&bg=transparent&theme=dark
index.html?names=ChatUser1,ChatUser2,ChatUser3
```

---

## Admin Panel

The right-side panel (toggle with `G` key or the ⚙ button):

| Control | Description |
|---------|-------------|
| Player list | Shows all players with active/BINGO status; click × to remove |
| Add player input | Type a name and press Enter or + |
| Bulk paste | Paste multiple names (one per line) then click **Add All from Paste** |
| **Draw Ball** | Draws the next random ball. Also triggered by **Spacebar** |
| **Auto Draw** | Toggle — automatically draws a ball every 3 seconds |
| **Check for Winner** | Scans all cards for bingo; announces if found |
| **Reset Game** | Clears all drawn balls and generates fresh cards for every player |
| Sound toggle | Enable/disable Web Audio sound effects |
| Theme select | Switch between Dark / Light / Neon themes |

---

## Keyboard Shortcuts

| Key | Action |
|-----|--------|
| `Space` | Draw next ball |
| `G` | Toggle admin panel |
| `Esc` | Dismiss winner overlay |

---

## postMessage API

The game communicates with a parent window (OBS browser source overlay, n8n bot, chat bot, etc.) via `window.postMessage`. All messages are namespaced with `bingo:`.

### Inbound (send TO the game)

```javascript
// Player joins and gets a new card
{ type: 'bingo:join', name: 'ViewerName' }

// Draw the next ball
{ type: 'bingo:draw' }

// Check if a specific player has bingo
{ type: 'bingo:check', name: 'ViewerName' }

// Check all players for bingo (omit name)
{ type: 'bingo:check' }

// Reset the game (new cards for everyone, clear drawn balls)
{ type: 'bingo:reset' }

// Query current player list
{ type: 'bingo:names' }
```

### Outbound (received FROM the game)

```javascript
// Fired when a winner is detected
{ type: 'bingo:winner', winner: 'ViewerName', pattern: 'Top Row' }

// Fired after each ball is drawn
{ type: 'bingo:drawn', number: 42, letter: 'N' }

// Fired after join/remove/reset, and in response to bingo:names query
{ type: 'bingo:names', names: ['Alice', 'Bob', 'Carol'] }
```

### OBS / n8n Integration Example

```javascript
// In your overlay wrapper or n8n webhook handler:
const gameFrame = document.getElementById('bingo-frame');

// Chat command: !bingo join
gameFrame.contentWindow.postMessage({ type: 'bingo:join', name: chatUser }, '*');

// Chat command: !draw
gameFrame.contentWindow.postMessage({ type: 'bingo:draw' }, '*');

// Listen for winners
window.addEventListener('message', e => {
  if (e.data.type === 'bingo:winner') {
    chat.announce(`🎉 BINGO! ${e.data.winner} wins with a ${e.data.pattern}!`);
  }
  if (e.data.type === 'bingo:drawn') {
    chat.announce(`${e.data.letter}-${e.data.number} was drawn!`);
  }
});
```

---

## Game Rules

- **Numbers:** 1–75
- **Card layout:** 5×5 grid with column headers B-I-N-G-O
  - **B:** 1–15, **I:** 16–30, **N:** 31–45, **G:** 46–60, **O:** 61–75
- **FREE space:** Center cell (N column, row 3) — always marked
- **Win conditions:** Any complete row, column, or diagonal (including both diagonals)
- **Cards:** Unique per player, stored in localStorage and persist across reloads

---

## Visual Features

- **Animated hopper** — spinning ball machine idle animation
- **Ball drop animation** — current ball falls in with bounce physics
- **Stamp animation** — called numbers pop onto cards with an ink-stamp effect
- **Win highlight** — winning row/column/diagonal glows gold
- **Winner overlay** — fullscreen BINGO announcement with confetti
- **Called numbers board** — all 75 numbers displayed; called ones light up by color

---

## Audio (Web Audio API)

All sounds are generated programmatically — no audio files required:

| Sound | Trigger |
|-------|---------|
| Ball tumble + thud | Ball drawn |
| Stamp pop | Number marked on a card |
| Bingo fanfare | Winner detected |

---

## Data Persistence

Player cards and drawn balls are saved to `localStorage` under the key `bingo_players`. State survives page reloads within the same browser session. Reset clears drawn balls and regenerates all cards.

---

## Testing

Open `test.html` to access the interactive test harness:

- **Manual controls:** Add 4 players, draw balls, check for winners, reset
- **URL param reloads:** Test each query string combination
- **Automated suite:** Click **Run All Tests** — runs 10 test groups covering the full postMessage API contract and validates letter–number range mapping

---

## OBS Setup (Recommended)

1. Add a **Browser Source**, set width/height to match your overlay canvas (e.g. 1920×1080)
2. URL: `file:///absolute/path/to/bingo/index.html?admin=false&bg=transparent`
3. In your bot/n8n workflow, send postMessages to control the game
4. For admin control, open a second browser with `admin=true` (default)

For local admin access while streaming, open the file in a regular browser tab — the admin panel is independent of the OBS overlay.
