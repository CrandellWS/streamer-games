# Slot Machine — Streamer Games

A classic 3-reel slot machine for live streams. Add viewer names to the reels, pull the lever, and watch it spin. Three matching names on the payline = that viewer wins.

## Quick Start

Open `index.html` directly in a browser — no server required.

For OBS: add as a Browser Source, set the URL to the file path, and optionally append `?bg=transparent` for a transparent background.

## URL Parameters

| Parameter | Values | Description |
|-----------|--------|-------------|
| `admin` | `true` / `false` | Show or hide the admin panel (default: `true`) |
| `bg` | `transparent` | Transparent background — use for OBS overlay |
| `theme` | `dark` / `light` / `neon` | Color theme (default: `dark`) |
| `names` | comma-separated | Pre-load names on page load |

**Examples:**

```
index.html
index.html?bg=transparent&admin=false
index.html?theme=neon&names=Alice,Bob,Charlie
index.html?theme=dark&admin=true&names=Viewer1,Viewer2
```

## postMessage API

The game communicates with its parent frame via `window.postMessage`. All messages use the `slots:` namespace.

### Inbound (bot → game)

Send these from your chatbot integration or overlay controller:

```javascript
// Add a single viewer name to the reels
{ type: 'slots:add', name: 'ViewerName' }

// Add multiple names at once
{ type: 'slots:add', names: ['Alice', 'Bob', 'Charlie'] }

// Pull the lever (start a spin)
{ type: 'slots:pull' }

// Force a win on the next spin (useful for demos)
{ type: 'slots:winner' }

// Remove all names and reset reels
{ type: 'slots:clear' }

// Query the current names list
{ type: 'slots:names' }
```

### Outbound (game → parent)

Listen for these events from the game:

```javascript
// Jackpot — three reels matched
{ type: 'slots:winner', winner: 'Alice', symbols: ['Alice', 'Alice', 'Alice'] }

// Spin completed — no match
{ type: 'slots:result', symbols: ['Alice', 'Bob', 'Alice'] }

// Response to slots:names query
{ type: 'slots:names', names: ['Alice', 'Bob', 'Charlie'] }
```

### Listening for events

```javascript
const frame = document.getElementById('game-frame');

window.addEventListener('message', (e) => {
  if (e.source !== frame.contentWindow) return;
  const msg = e.data;

  if (msg.type === 'slots:winner') {
    console.log('Winner:', msg.winner);
    console.log('Symbols:', msg.symbols);
    // Announce in chat, trigger confetti overlay, etc.
  }

  if (msg.type === 'slots:result') {
    console.log('Reels stopped:', msg.symbols);
  }
});
```

### Sending commands from a bot

```javascript
function sendToSlots(type, data) {
  const frame = document.getElementById('game-frame');
  frame.contentWindow.postMessage({ type, ...data }, '*');
}

// When viewer types !join in chat:
sendToSlots('slots:add', { name: viewerName });

// When streamer types !spin in chat:
sendToSlots('slots:pull');

// When streamer types !clear in chat:
sendToSlots('slots:clear');
```

## Features

### Visual

- **Chrome cabinet**: Rounded metallic cabinet with beveled edges and inset shadows
- **LED display**: Animated LED strip with 24 lights, flashing sequence on win
- **3 reel windows**: Deep-set reel windows with top/bottom fade masks and payline marker
- **Payline**: Gold neon line at center with flanking chevrons
- **Spinning animation**: Smooth translateY scroll with motion blur during fast spin
- **Staggered stops**: Reel 1 at 1.5s, reel 2 at 2.1s, reel 3 at 2.7s — builds suspense
- **Deceleration**: Cubic ease-out landing on the winning symbol
- **Jackpot overlay**: Bouncing JACKPOT! text with winner name display
- **Coin shower**: Physics-based coin particles with gradient fill, rotation, and gravity
- **Win highlight**: Gold glow border on all three reels on match

### Audio (Web Audio API — no files needed)

| Sound | Trigger |
|-------|---------|
| Lever creak | Lever pulled / spin starts |
| Reel hum | Each reel during spin phase |
| Mechanical click | Each reel stopping |
| Jackpot arpeggio | Win — ascending 5-note chord + siren wail |
| Coin pings | Random during coin shower |

### Admin Panel

- Add individual names or bulk paste (one per line)
- View current names with color-coded dots and duplicate counts
- Remove any name (all instances)
- Pull Lever button (also triggered by Spacebar)
- Force Win button for demos
- Dark / Light / Neon theme switcher
- Sound on/off toggle
- Preferences persist via localStorage

### Name Weighting

Adding the same name multiple times increases its probability proportionally. If you add Alice 3 times and Bob once, Alice has a 75% chance of landing on any given reel stop.

### Keyboard Shortcut

Press **Space** to pull the lever when focus is not on a form field.

## OBS Setup

1. Add a **Browser Source** in OBS
2. Point it at `index.html?bg=transparent&admin=false`
3. Set width and height to match your scene (recommended: 1280×720 or 1920×1080)
4. The slot machine centers itself — works at any resolution
5. To control it from your chat bot, use a second non-visible browser source or a local HTTP server to relay postMessage commands

## Testing

Open `test.html` in a browser. It embeds the game in an iframe alongside:

- Buttons for all postMessage commands
- URL parameter reload buttons (Dark / Light / Neon / Transparent / Admin hidden / Preload names)
- Custom name field with bulk and duplicate testing
- Timestamped message log showing all inbound/outbound traffic
- Automated test suite (10 tests) covering:
  - Clear on empty state
  - Single and array name adds
  - XSS safety
  - Name length limits
  - Pull producing result/winner events
  - Symbol array structure
  - Single-name pool always wins
  - Clear confirmed via query
  - URL ?names= parameter

Click **Run All Tests** to execute the full suite. Results show pass/fail counts at the bottom.

## Architecture Notes

- Single self-contained HTML file (~800 lines) — all CSS and JS inline
- No external dependencies, no build step, works offline
- IIFE with `'use strict'` — no global namespace pollution
- XSS-safe: all user names go through `document.createTextNode` before display
- `overflow: hidden` on body — no scrollbars at any resolution
- Reel strips are built by repeating the name list ~25× so there is always a valid landing target ahead of the current scroll position
- Each name gets a stable color assignment (8-color palette, wrapping) stored in a Map for the session
- LocalStorage keys: `slots_names`, `slots_theme`, `slots_sound`
