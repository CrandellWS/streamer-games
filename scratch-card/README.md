# Scratch Card

A streamer overlay game featuring a metallic scratch card with animated reveal, match-3 win detection, and celebration effects. Viewer names can be used as prizes. Controlled via postMessage from a bot or manually from the admin panel.

---

## Quick Start

1. Open `index.html` in a browser (or load it as a Browser Source in OBS).
2. Add viewer names in the admin panel (right side).
3. Click **Reveal Card** (or press **Space**) to scratch the card.
4. All 3 matching symbols = win, celebration fires, winner announced via postMessage.
5. Click **Reset Card** (or press **R**) to deal a fresh card.

---

## OBS Setup

| Setting | Value |
|---------|-------|
| URL | `file:///path/to/scratch-card/index.html?admin=false&bg=transparent` |
| Width | 1920 (or your canvas width) |
| Height | 1080 |
| Custom CSS | _(none needed)_ |

### Recommended URL parameters for OBS

```
?admin=false&bg=transparent&theme=dark
```

- `admin=false` — hides the control panel from the stream
- `bg=transparent` — removes the background so the card floats over your scene
- `theme=neon` — extra punch for dark streams

### Controlling from a bot

Keep the admin panel open in a separate window, or send postMessage commands from an OBS custom script / n8n workflow / chatbot.

---

## URL Parameters

| Parameter | Values | Default | Description |
|-----------|--------|---------|-------------|
| `admin` | `true` / `false` | `true` | Show or hide the admin panel |
| `bg` | `transparent` | _(dark bg)_ | Transparent background for OBS |
| `theme` | `dark` / `light` / `neon` | `dark` | Color theme |
| `names` | comma-separated | _(empty)_ | Pre-load viewer names as prizes |

**Example:**
```
index.html?theme=neon&names=Alice,Bob,Carol&admin=false
```

---

## postMessage API

All messages use the namespace `scratch:`.

### Inbound (bot → game)

#### `scratch:reveal`
Triggers the animated scratch reveal. No-op if a reveal is already in progress.
```json
{ "type": "scratch:reveal" }
```

#### `scratch:reset`
Resets the card and deals a fresh set of symbols. Stops any active celebration.
```json
{ "type": "scratch:reset" }
```

#### `scratch:set`
Sets custom symbols and/or prize names. Automatically resets to a fresh card.
```json
{
  "type": "scratch:set",
  "symbols": ["🎃", "🦄", "🌈", "🔥", "💥"],
  "prizes":  ["Alice", "Bob", "Carol"]
}
```
- `symbols` — array of emoji strings, minimum 3, maximum 8
- `prizes`  — array of viewer name strings (optional)

#### `scratch:names`
Queries the current prize names list. Responds with `scratch:names`.
```json
{ "type": "scratch:names" }
```

---

### Outbound (game → parent)

#### `scratch:winner`
Fired after all 3 panels are revealed.
```json
{
  "type":    "scratch:winner",
  "matched": true,
  "symbols": ["🍒", "🍒", "🍒"],
  "prize":   "Alice"
}
```
- `matched` — `true` if all 3 symbols match, `false` otherwise
- `symbols` — the 3 revealed symbols
- `prize`   — a randomly-selected name from the prizes list, or `null` if no names are set

---

## Bot Integration Example (n8n / Node.js)

```javascript
// Reveal the card
iframeEl.contentWindow.postMessage({ type: 'scratch:reveal' }, '*');

// Listen for results
window.addEventListener('message', (e) => {
  if (e.data.type === 'scratch:winner') {
    if (e.data.matched) {
      chat.say(`🎉 @${e.data.prize} wins the scratch card! Symbols: ${e.data.symbols.join(' ')}`);
    } else {
      chat.say(`No match this round! Better luck next time.`);
    }
  }
});
```

---

## Keyboard Shortcuts

| Key | Action |
|-----|--------|
| `Space` | Reveal card |
| `R` | Reset card |
| `G` | Toggle admin panel |

---

## Admin Panel Features

| Feature | Description |
|---------|-------------|
| **Reveal Card** | Triggers the scratch reveal with staggered panel animation |
| **Reset Card** | Deals a fresh card, ready for next viewer |
| **Symbol Set** | Choose Fruits / Gems / Lucky / Custom emoji symbols |
| **Win Probability** | 0–100% slider controlling how often all 3 panels match |
| **Prize Names** | Add/remove viewer names drawn as prizes on wins |
| **Theme** | Dark / Light / Neon |
| **Sound Effects** | Toggle Web Audio scratch + reveal + celebration sounds |
| **Celebration FX** | Toggle fullscreen confetti burst on wins |

---

## Symbol Sets

| Set | Symbols |
|-----|---------|
| Fruits | 🍒 🍋 🍇 🍊 ⭐ |
| Gems | 💎 💍 🔮 💠 ⭐ |
| Lucky | 🍀 🌟 🎰 7️⃣ 💰 |
| Custom | Any emoji, comma-separated |

---

## Game Mechanics

- **3 panels** in a row, each covered by a metallic silver scratch coating drawn on Canvas.
- **Reveal animation:** Each panel wipes from left to right using a zigzag clip path (~700ms). Panels reveal sequentially with a 600ms stagger (panel 1 → 2 → 3).
- **Win condition:** All 3 panels show the same emoji symbol.
- **Win probability:** Configurable via slider (default 33%). When a win is due, all 3 symbols are forced to match. Otherwise, a mismatch is guaranteed.
- **Prize selection:** A random name from the prize list is picked on a win.
- **Celebration:** Fullscreen confetti burst + gold card flash + ascending arpeggio audio.

---

## Audio (Web Audio API)

All sounds are generated programmatically — no audio files required.

| Sound | Trigger |
|-------|---------|
| Scratch noise | Each panel reveal starts |
| Reveal chime | Each panel fully revealed (C5 / E5 / G5 ascending) |
| Win fanfare | Ascending arpeggio + bell overtones |
| Loss tone | Descending sawtooth |

---

## Testing

Open `test.html` to access:

- **Manual controls** — buttons for every postMessage command
- **Theme switcher** — live reload with different themes
- **Custom payload** — send any JSON directly
- **Message log** — all inbound/outbound messages with timestamps
- **9 automated tests** — covering load, set, reveal, winner payload structure, names query, rapid resets, and error tolerance

Run tests: click **▶ Run All Tests** in the test harness sidebar.

---

## File Structure

```
scratch-card/
├── index.html   — Game (self-contained, ~900 lines)
├── test.html    — Test harness + automated suite
└── README.md    — This file
```

---

## Technical Notes

- Single HTML file, all CSS and JS inline — no external resources, works offline.
- Canvas API for the metallic scratch coating and zigzag wipe animation.
- CSS transitions for symbol pop-in (scale spring + opacity fade).
- CSS particle system for sparkles on each reveal.
- Canvas-based confetti for the win celebration.
- Web Audio API for all sounds (oscillators + noise buffer).
- LocalStorage for prize name persistence (`scratch_names`).
- `'use strict'` + IIFE — no globals.
- XSS-safe: all user input is escaped before rendering.
- `overflow: hidden` on body — OBS-safe, no scrollbars.
- Responsive: card and panels scale with viewport via `clamp()`.
