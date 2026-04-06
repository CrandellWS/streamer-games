# Marble Race

A physics-based marble drop race for live streamers. Viewers join and get assigned a unique marble color. Marbles drop through a procedurally-generated track of pegs, bumpers, and ramps — first to the finish line wins.

## Quick Start

1. Open `index.html` in a browser (no server needed)
2. Add player names in the admin panel
3. Click **Start Race** or press **Space**
4. Watch the physics simulation — marbles bounce, collide, and race to the finish!

## OBS / Stream Setup

### Browser Source
- **URL**: `file:///path/to/marble-race/index.html?bg=transparent&admin=false`
- **Width**: 600–900px recommended (taller is better — more track depth)
- **Height**: 800–1080px recommended
- **Transparent background**: enabled by the `?bg=transparent` param

### Bot Integration (postMessage)
The game accepts commands from a parent page or OBS browser source via `postMessage`:

```javascript
// Viewer joins the race
window.postMessage({ type: 'marble:join', name: 'ViewerName' }, '*')

// Start the race (after all viewers have joined)
window.postMessage({ type: 'marble:start' }, '*')

// Clear all players (reset for next race)
window.postMessage({ type: 'marble:clear' }, '*')

// Query current players
window.postMessage({ type: 'marble:names' }, '*')
// → game responds: { type: 'marble:names', names: ['Alice', 'Bob', ...] }
```

### Inbound Messages

| Type | Payload | Description |
|------|---------|-------------|
| `marble:join` | `{ name: string }` | Add a viewer as a marble |
| `marble:start` | — | Start the race (ignored if already running) |
| `marble:clear` | — | Remove all players and reset |
| `marble:names` | — | Request current player list |

### Outbound Events

| Type | Payload | Description |
|------|---------|-------------|
| `marble:winner` | `{ winner, color, time }` | Fires when each marble crosses the finish line (in order) |
| `marble:names` | `{ names: string[] }` | Response to a `marble:names` query |

The `marble:winner` event fires for every marble that finishes (not just 1st), so you can award prizes to the top 3 or any finisher.

## URL Parameters

| Parameter | Values | Default | Description |
|-----------|--------|---------|-------------|
| `admin` | `true` / `false` | `true` | Show or hide the admin panel |
| `bg` | `transparent` | — | Transparent canvas background for OBS |
| `theme` | `dark` / `light` / `neon` | `dark` | Color theme |
| `names` | comma-separated | — | Pre-load player names on startup |

### Examples
```
# OBS overlay, transparent, no controls
index.html?admin=false&bg=transparent

# Test with pre-loaded names
index.html?names=Alice,Bob,Carol,Dave&theme=neon

# Light theme for screen sharing
index.html?theme=light
```

## Admin Panel Controls

| Control | Description |
|---------|-------------|
| **Start Race** | Begin a 3-2-1 countdown then drop the marbles |
| **Generate New Track** | Randomize the peg/ramp layout for next race |
| **1× / 2× / 3× Speed** | Simulation speed multiplier |
| **Add Player** | Type a name and press Enter or click Add |
| **Bulk Paste** | Paste multiple names (one per line) and click Add All |
| **Lineup** | Shows all players with marble color; click ✕ to remove |
| **Sound** | Toggle all Web Audio sounds on/off |
| **Clear All** | Remove all players and reset the race |
| **Theme** | Switch between Dark, Light, and Neon themes |
| **⚙ gear button** | Toggle panel visibility |

**Spacebar** also starts the race (when focused on the page body).

## Physics System

The simulation runs a custom 2D physics engine on HTML5 Canvas:

- **Gravity**: 650 px/s² — marbles feel weighty, not floaty
- **Sub-stepping**: Each frame is divided into multiple small physics steps for stability
- **Restitution**: Peg bounces ~62%, wall bounces ~55%, marble collisions ~45%
- **Friction**: Slight horizontal damping each frame so marbles don't slide forever
- **Collision types**:
  - Marble → Peg (circle/circle)
  - Marble → Ramp (circle/line-segment)
  - Marble → Wall (boundary clamp + reflect)
  - Marble → Marble (full elastic-ish impulse resolution)

### Track Generation
Each track is procedurally generated with a new random seed:
- **8 rows × 5 columns** of pegs in a staggered grid with random jitter
- **3 diagonal ramps** placed at different heights with random angles
- Pegs use a seeded RNG so the same seed always produces the same track

## Audio (Web Audio API)

All sounds are generated programmatically — no external audio files needed:

| Sound | Trigger |
|-------|---------|
| Marble clink | Each peg/ramp collision (pitch varies with speed) |
| Crowd murmur | On race start |
| Finish bell | Each marble crosses the finish line |
| Fanfare | All marbles finished (race complete) |
| Countdown beeps | 3, 2, 1, GO! |

## Marble Colors

Up to 20 distinct colors assigned in order. For more than 20 players, colors repeat:

```
Red, Orange, Yellow, Green, Cyan, Blue, Purple, Pink, White, Coral,
Aqua, Amber, Lime, Navy, Magenta, Yellow2, Mint, Peach, Sky, Violet
```

## Testing

Open `test.html` to:
- Send manual postMessage commands via buttons
- Watch all inbound/outbound messages in the log
- Run the 16-test automated suite (API, UI state, themes, URL params, XSS safety, race completion)

## Architecture

```
index.html  (single self-contained file)
├── CSS variables + 3 themes (dark/light/neon)
├── Layout: canvas area (flex:1) + admin panel (360px)
├── Canvas rendering pipeline
│   ├── Background + track walls
│   ├── Pegs (radial gradient spheres)
│   ├── Ramps (thick stroked lines)
│   ├── Finish line (checkered pattern)
│   ├── Marble trails (faded stroke)
│   └── Marbles (radial gradient + specular highlight + name label)
├── Physics engine (IIFE-scoped)
│   ├── Marble class (position, velocity, trail, state)
│   ├── physicsStep() with sub-stepping
│   ├── resolveMarblePeg() — circle/circle
│   ├── resolveMarbleRamp() — circle/segment projection
│   ├── resolveMarbleWalls() — boundary clamp
│   └── resolveMarbleMarble() — pairwise elastic collision
├── Race state machine: idle → countdown → running → finished
├── postMessage API (marble: namespace)
└── Web Audio API sound engine
```

## Files

```
marble-race/
├── index.html   — The game (self-contained, ~750 lines)
├── test.html    — API test harness + automated suite
└── README.md    — This file
```
