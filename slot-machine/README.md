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
| `mode` | `spintillx` / `creditstack` / `draw` | Game mode (default: `spintillx`) |
| `spins` | `1`–`10` | Giveaway Draw: spins before the winner lands (clamped, default `5`) |
| `namesb64` | base64url JSON | Replaces the entrant list. Either `["Alice","Bob"]` or `[{"name":"Alice","weight":3},{"name":"Bob"}]`. Malformed input is ignored silently |
| `winner` | name | Giveaway Draw: forced winner. Added to the entrants if not already present |
| `autostart` | `1` | Run the draw (or a spin) automatically ~600 ms after load |
| `title` | text | Giveaway Draw: giveaway name shown on the pre-draw intro card (default: `Giveaway`) |
| `subtitle` | text | Giveaway Draw: optional second line on the intro card |
| `intro` | `0` / ms | Pre-draw intro: `0` skips it entirely; a number sets its total length in ms (clamped 500–60000). Default ~4500 ms, ~2500 ms with Turbo on |
| `introSpeed` | `0.5`–`2` | Multiplier on the derived name-roll speed (default `1`, clamped). Per-launch only, never persisted |

**Examples:**

```
index.html
index.html?bg=transparent&admin=false
index.html?theme=neon&names=Alice,Bob,Charlie
index.html?theme=dark&admin=true&names=Viewer1,Viewer2
index.html?mode=draw&spins=5&winner=Bob&names=Alice,Bob,Charlie,Dana&autostart=1
index.html?mode=draw&namesb64=W3sibmFtZSI6IkFsaWNlIiwid2VpZ2h0IjozfSwiQm9iIl0&autostart=1
index.html?mode=draw&spins=3&title=Friday%20Freeplay&names=Alice,Bob,Charlie&autostart=1
index.html?mode=draw&intro=0&names=Alice,Bob,Charlie&autostart=1
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

// Switch mode
{ type: 'slots:mode', mode: 'spintillx' | 'creditstack' | 'draw' }

// Giveaway Draw — load entrants (optional), select draw mode, set the
// spin count (optional, clamped 1..10) and run the whole sequence.
// names may be strings or { name, weight } objects; weight affects the
// draw odds only, never how often a name appears on the reels.
// winner is optional — omit it and the game picks one (weighted).
// title / subtitle are optional and appear on the pre-draw intro card.
// intro is optional: false (or 0) skips the intro, a number sets its
// total length in ms, true forces the default length.
{ type: 'slots:draw',
  names: ['Alice', { name: 'Bob', weight: 3 }],
  winner: 'Bob',
  spins: 5,
  title: 'Friday Freeplay',
  subtitle: 'Sub-only',
  intro: 4500,
  introSpeed: 1 }
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

// Fired once when the page has initialised
{ type: 'slots:ready' }

// Giveaway Draw — the pre-draw intro has just started (before any reel moves)
// coverage is the fraction (0..1) of entrants that pass a pay line during the roll
{ type: 'slots:intro', title: 'Friday Freeplay', entrants: 4, spins: 3, coverage: 1 }

// Giveaway Draw — after each LOSING spin of the sequence lands
{ type: 'slots:draw-progress', spin: 2, total: 5,
  symbols: ['Alice', 'Bob', 'Alice'], nearMiss: true }

// Giveaway Draw — the winning spin carries the sequence position too
{ type: 'slots:winner', winner: 'Bob',
  symbols: ['Bob', 'Bob', 'Bob'], spin: 5, total: 5 }
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

### Giveaway Draw mode

Pick **Giveaway Draw** in the Mode section (or `?mode=draw`). The winner is chosen
**before the first spin**; the machine then plays a short sequence — "Spins to win",
1–10, default 5 — and the winner lands on the last one. One lever pull (or the
Pull Lever button, Spacebar, or a `slots:draw` message) runs the entire sequence;
further pulls are ignored while it is running. The status line reads
"Draw 2 of 5" as it goes. There is no game-over overlay: the machine returns to
ready so the next draw can start immediately.

#### The pre-draw intro

A draw does not just start spinning. Every trigger — lever pull, lever drag,
Spacebar, `slots:draw`, or `autostart=1` — first plays a build-up **inside the
cabinet**, so existing OBS crops stay valid:

1. An intro card covers the reel window: a "GIVEAWAY DRAW" eyebrow, the giveaway
   `title` in gold (falling back to "Giveaway"), the optional `subtitle`, and a
   line reading `4 entrants · 3 spins` — or `1 spin · one and done` for a
   single-spin draw. The LED marquee switches to a fast chase for the duration.
2. Under the card the reels drift slowly downward through the entrant names
   (silent, no stopping or snapping) so viewers see the field roll by. A small
   counter on the card ticks up as names pass, so the audience gets the scale
   even if they miss individual names.
3. A `3 · 2 · 1` countdown in big gold digits, ~800 ms a beat with a tick on each,
   then `PULL!`.
4. The card fades, the lever pulls itself, and only then does the planned spin
   sequence start. From there everything behaves exactly as before, status line
   included ("Draw 1 of 5").

Total length defaults to ~4500 ms (~2500 ms with Turbo on); `?intro=<ms>` sets it
and scales every beat proportionally, `?intro=0` (or `{ intro: false }`) skips it.
`slots:intro` is emitted the moment the intro starts.

**Roll speed is derived, not fixed.** A flat speed hides most of the field when
there are a lot of entrants, so the roll is sized to the time budget instead:

- the three reels start a third of the entrant list apart, so each one only has
  to show `ceil(N/3)` rows for the three together to cover everybody
- `speed = rowsNeeded × itemHeight / rollMs`, where `rollMs` is the intro length
  minus the countdown portion and `itemHeight` is read at runtime (it changes
  with the 3/5/7 visible-rows setting)
- `introSpeed` multiplies that derived speed before it is clamped to a readable
  0.15–0.9 px/ms band
- if even the top of that band cannot show everyone in time, the roll phase is
  extended up to a hard cap of 9 s total. **That extension only happens when the
  intro length is the default** — an explicit `intro=<ms>` is treated as a
  directive and is honoured exactly, with `coverage` dropping below 1 instead

The `coverage` field on `slots:intro` reports the resulting fraction (0–1) of
entrants that pass a pay line during the roll. The derivation lives in the pure
function `computeIntroRoll({ entrants, itemHeight, budgetMs, explicit, speedMult })`,
which touches neither the DOM nor game state.

The losing spins are pure theatre, and they follow fixed rules:

- three-of-a-kind only ever appears on the final spin
- about a third of the losing spins are near misses (two matching + one different)
- roughly a third of those near misses feature the winner, the rest feature decoys
- decoys are drawn from the heavier-weighted entrants (top half by weight; all of
  them if there are fewer than four entrants)
- the winner never near-misses on the spin immediately before the win
- 1 spin = no tease at all; 2 or 3 spins = decoy near misses only

Between spins the machine pauses ~900 ms, or ~400 ms with Turbo on. The
"remove winners" option behaves exactly as it does in the other modes.

The planning logic lives in the pure function
`planDrawSequence(entrants, weights, winner, spins, rng)`, which returns
`[{ results, nearMiss, win }]` and touches neither the DOM nor game state, so it
can be exercised deterministically with a seeded `rng`.

### Entrant Weights

`namesb64` (and `slots:draw`) accept `{ name, weight }` entries. A weight only
changes a name's chance of being drawn as the winner (and of being picked as a
decoy) — it never changes how often the name appears on the reel strip: with
weights in play each name appears once per strip pass. Names with no weight
entry count as 1. Weighted names show a `×<weight>` badge in the name list.

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
- LocalStorage keys: `slots_names`, `slots_theme`, `slots_sound`, `slots_mode`, `slots_drawSpins`, `slots_winfloor`, `slots_removewins`, `slots_rows`
