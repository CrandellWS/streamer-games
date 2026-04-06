# Coin Flip

Interactive 3D coin flip game for live streams. Viewers pick heads or tails in chat, streamer flips the coin, and the winning team is revealed with a dramatic 3D animation.

## Quick Start

Open `index.html` in OBS Browser Source or any browser. No server required.

## OBS Setup

1. Add a **Browser Source** in OBS
2. Set the URL to the full path: `file:///path/to/coin-flip/index.html`
3. Recommended size: **1280×720** or **1920×1080**
4. Check **"Shutdown source when not visible"** and **"Refresh browser when scene becomes active"**
5. For transparent overlay: append `?bg=transparent` and check **"Allow transparency"** in OBS

## URL Parameters

| Parameter | Values | Default | Description |
|-----------|--------|---------|-------------|
| `admin` | `true` / `false` | `true` | Show or hide the admin panel |
| `bg` | `transparent` | — | Transparent background for OBS compositing |
| `theme` | `dark` / `light` / `neon` | `dark` | Color theme |
| `names` | `Alice,Bob,Carol` | — | Pre-load names (randomly assigned to teams) |

### Example URLs

```
# Game only, no admin panel (for OBS)
index.html?admin=false&bg=transparent

# Neon theme with pre-loaded viewers
index.html?theme=neon&names=Viewer1,Viewer2,Viewer3

# Light theme for local testing
index.html?theme=light
```

## Admin Panel

Click **⚙** (top-right) to toggle the admin panel.

- **Add Picker** — type a viewer name and click **₪ Heads** or **₮ Tails** to assign them
- **Team lists** — see who's on each team, remove individuals with ×
- **Flip Coin** — trigger the flip (also **Spacebar** or click the coin)
- **Clear All** — reset both teams and the coin
- **Sound toggle** — enable/disable Web Audio effects

## Chat Bot Integration (postMessage API)

Send messages to the game's iframe to control it from a bot or N8N workflow.

### Namespace: `coin:`

### Inbound Messages (bot → game)

```javascript
// Viewer picks a side
{ type: 'coin:pick', name: 'ViewerName', side: 'heads' }  // side: 'heads' or 'tails'

// Trigger a flip (random result)
{ type: 'coin:flip' }

// Force a specific result (for testing or rigged demos)
{ type: 'coin:result', winner: 'heads' }  // winner: 'heads' or 'tails'

// Clear all pickers and reset
{ type: 'coin:clear' }

// Query current state (game will respond)
{ type: 'coin:names' }
```

### Outbound Messages (game → parent)

```javascript
// Emitted after every flip
{ type: 'coin:winner', winner: 'heads', names: ['Alice', 'Bob'] }

// Response to coin:names query
{ type: 'coin:names', heads: ['Alice'], tails: ['Bob', 'Carol'] }
```

### Sending from a parent page

```javascript
const frame = document.querySelector('iframe');

// Add a viewer to heads
frame.contentWindow.postMessage({
  type: 'coin:pick',
  name: 'StreamFan42',
  side: 'heads'
}, '*');

// Listen for results
window.addEventListener('message', e => {
  if (e.data.type === 'coin:winner') {
    console.log('Winner:', e.data.winner, 'Team:', e.data.names);
  }
});
```

### N8N / Webhook Example

Your bot listens to chat, extracts `!heads` or `!tails` commands, and POSTs to an N8N workflow that forwards them as postMessages to the OBS Browser Source via a local HTTP relay.

```
Chat: "StreamFan42: !heads"
Bot extracts → name: "StreamFan42", side: "heads"
N8N sends postMessage → { type: 'coin:pick', name: 'StreamFan42', side: 'heads' }
```

## Keyboard Shortcuts

| Key | Action |
|-----|--------|
| **Space** | Flip the coin |
| **⚙ button** | Toggle admin panel |

## Behavior Notes

- **Duplicate prevention** — a viewer can only be on one team per round. Re-picks are silently ignored.
- **XSS safety** — all viewer names are sanitized before rendering.
- **Flip lock** — a second flip while one is in progress is ignored.
- **Empty team win** — if the winning side has no pickers, the banner still shows the winning face but notes "No pickers on this team."
- **Sound** — Web Audio API (no external files). Sounds: coin ring (800 Hz sine), whoosh (filtered noise sweep), metallic clink (1200+600 Hz transient). Setting persists in localStorage.
- **Theme** persists in localStorage per browser.

## Testing

Open `test.html` in a browser to run the full automated test suite (12 tests) and use manual control buttons to test each postMessage command interactively.

## Technical Details

- Single HTML file, zero external dependencies
- All CSS and JS inline
- 3D coin via CSS `perspective` + `transform-style: preserve-3d` + Web Animations API
- `rotateY(1800deg)` = heads (5 full spins, landing on front)
- `rotateY(1980deg)` = tails (5 full spins + 180°, landing on back)
- `backface-visibility: hidden` on each face for clean reveal
- Confetti via dynamically injected DOM elements + CSS keyframes
- Particle burst on coin click
- `'use strict'` IIFE, no globals, no frameworks
