# Pinko — Game Rewrite Design Spec

**Date:** 2026-04-12
**Status:** Approved
**Replaces:** plinko/index.html (full rewrite)
**Output:** pinko/index.html (new directory, rename from plinko)

## Overview

Pinko (Pin from pinball + ko from plinko) is a visual name picker for streamer giveaways. Names fill equal-width slots at the bottom. An anonymous ball drops through a procedurally generated obstacle board and lands on a winner. The drama of the ball bouncing is the product.

## Identity

- Name: **Pinko**
- Subtitle: "Pinball chaos — drop it and find a winner!"
- Color identity: subtle pink accent throughout — pink-tinted pegs, pink ball glow, pink winner highlights
- Default color scheme uses pink as the accent color (replaces purple accent from other games)

## Drop Mechanism — Claw Machine Tease

The ball does not simply appear and fall. A visible carrier/claw holds the ball at the top and teases the audience before dropping.

### Behavior
- Ball appears in a carrier at the top of the board
- Carrier swings side to side with organic easing (not linear, not mechanical)
- Swing amplitude and speed vary — fake-outs, pauses, direction changes
- Final drop position is randomized across the full board width
- After drop, carrier slides off-screen or fades

### Drama Slider
- Admin panel control: **Drama** — Low to High
- **Low (2-3 seconds):** Quick swing, 1-2 oscillations, drops fast. For rapid rounds.
- **High (5-8 seconds):** Slow deliberate swings, dramatic pauses, 3-5 fake-outs. Chat has time to react.
- Stored in localStorage: `pinko_drama`

### Drop Queue
- When multiple rounds are needed, balls queue up
- After winner is announced, next ball auto-loads into the claw
- Configurable delay between drops (tied to drama level)

## Board Generation — Modular Tile System

Boards are built from a library of pre-designed modular tiles. Every tile is hand-crafted to guarantee no stuck balls. The procedural generator assembles tiles into unique boards.

### Tile Design Rules
- Each tile is 3-4 peg rows tall, full board width
- Every tile guarantees: a ball entering from ANY point at the top can exit from at least 2 points at the bottom
- No tile contains geometry that can trap a ball (no enclosed areas, no dead-end funnels)
- Tiles are designed as functions that draw their content given board width and y-offset

### Tile Library (~12-15 tiles)

**Mild tiles (pure peg patterns):**
1. Standard triangular offset peg row (classic plinko pattern)
2. Diamond peg cluster — pegs arranged in diamond shapes
3. Wide-gap alternating — every other peg removed for faster drops
4. Chevron rows — pegs in V-shapes pointing down
5. Scattered sparse — random-looking but validated peg placement

**Wild tiles (pegs + obstacles):**
6. Bumper row — 2-3 circular bumpers between peg rows, light up on hit
7. Angled rail — single diagonal rail that redirects ball sideways
8. Funnel — converging rails that channel ball toward center then scatter
9. Gate — horizontal rail with a gap, ball must find the opening
10. Split — Y-shaped rail that forces ball left or right

**Insane tiles (mechanical/pinball elements):**
11. Spinner — rotating bar that deflects ball unpredictably
12. Flipper pair — two angled flippers that kick ball sideways on contact
13. Pinball bumper cluster — 3 bumpers in triangle, high restitution, ball ricochets
14. Helix — curved rail that spirals ball around before releasing
15. Chaos zone — dense bumper field with multiple spinners

### Board Assembly
- Board size determines tile count:
  - **Small:** 3 tiles
  - **Medium:** 5 tiles
  - **Large:** 7 tiles
- Chaos level determines which tile pool is used:
  - **Mild:** tiles 1-5 only
  - **Wild:** tiles 1-10
  - **Insane:** tiles 1-15
- Generator picks tiles randomly, no consecutive duplicates
- "Regenerate Board" button in admin creates a new layout
- Board layout seed saved to localStorage for consistency across reloads

### Top and Bottom Zones
- **Top zone:** Clear area above first tile for claw mechanism and ball entry
- **Bottom zone:** Settling funnels that guide ball cleanly into slots. V-shaped guides between each slot ensure ball commits to one slot.

## Physics Engine

### Fixed Timestep
- Physics update at 16ms intervals (60 Hz), independent of render frame rate
- Accumulator pattern: leftover time carries to next frame
- Consistent behavior across all devices

### Collision Detection
- **Circle-circle** for ball vs pegs and bumpers
- **Circle-segment** for ball vs rails, flippers, funnels
- Proper collision response with configurable restitution per obstacle type:
  - Pegs: 0.5 (absorb energy, natural deceleration)
  - Bumpers: 1.2 (boost energy, exciting bounces)
  - Rails: 0.7 (redirect with slight energy loss)
  - Walls: 0.3 (dead bounce, stay in bounds)

### Ball Properties
- Radius: ~8px (scales with board size)
- Gravity: constant downward, tuned for satisfying fall speed
- Max velocity capped to prevent tunneling through geometry
- Damping: slight air resistance so ball doesn't accelerate forever

### Anti-Stuck Measures
- Tile system prevents impossible geometry (primary defense)
- Stuck detection: if ball position hasn't changed > 5px in 2 seconds, apply random impulse
- Hard timeout: if ball hasn't reached bottom in 15 seconds, teleport to nearest slot with a visual effect
- No overlapping collision geometry by construction

## Bottom Slots

### Layout
- Equal width for every name — mathematically fair probability
- Slot width = board width / number of names
- V-shaped guides between slots ensure clean entry
- Minimum 3 names, maximum 30 names

### Appearance
- Each slot has a colored header strip (color from player color assignment)
- Name label centered, auto-sized to fit slot width
- Subtle pink gradient on slot backgrounds
- Active slot (ball inside) lights up with glow effect

### Ball Settling
- When ball enters slot zone, gentle deceleration
- Ball settles to center of slot with satisfying ease-out
- No bouncing out of slots — once committed, it stays

## Winner Experience

Three modes, selectable in admin panel. Default: Escalating.

### Quick Mode
- Slot highlights with bright glow
- Name text pulses and scales up briefly
- Short sound effect (chime)
- 1-second pause, then next ball loads
- Best for: rapid multi-ball rounds, casual use

### Dramatic Mode
- Screen dims with backdrop blur
- Winner overlay appears: "WINNER" header + large name
- Confetti explosion (same system as spin wheel)
- Glow border on overlay
- Close button + auto-dismiss after 5 seconds
- Best for: single giveaways, big reveals

### Escalating Mode (default)
- Uses Quick mode for all drops except the last one
- Final ball triggers Dramatic mode
- If only 1 ball total, uses Dramatic
- Best for: multi-round giveaways with a big finish

## Sound Design

All procedural via Web Audio API (no external files).

### Sound Events
- **Peg tink:** High-pitched click, pitch varies with ball velocity. Throttled: max 1 per 50ms per peg.
- **Bumper hit:** Deep thud + ping combo. Combo counter: rapid successive hits increase pitch.
- **Spinner whir:** Continuous tone while ball contacts spinner, pitch tied to spin speed.
- **Rail slide:** Brief metallic scrape sound.
- **Claw movement:** Subtle mechanical servo sound during tease animation.
- **Ball drop:** Whoosh as ball releases from claw.
- **Slot landing:** Satisfying thunk + register bell.
- **Winner fanfare:** Ascending tone sequence (Quick mode: short, Dramatic mode: full).
- **Confetti pop:** Burst sound accompanying confetti.

### Sound Controls
- Master sound toggle in admin panel
- All sounds respect the toggle — no audio leaks
- Sound throttling prevents audio spam (the infinite ding problem)

## Visual Design

### Subtle Pink Identity
The pink is a whisper, not a shout. Male streamers need to feel comfortable using this. The game reads as dark/neutral with pink as a subtle accent — like a racing stripe, not a paint job.

- CSS accent variable: `--accent: #7c5cfc` (purple, same as other games — primary UI stays neutral)
- `--accent-pink: #d4748a` (muted rose — used sparingly for glows and highlights only)
- Pegs: metallic silver/gray with radial gradient. NO pink tint on pegs.
- Ball: dark core, subtle warm glow (barely pink, could read as warm white)
- Bumpers: match the game's standard accent color (purple), flash on hit
- Background: dark theme default, no pink tinting
- **Where pink appears:** ball trail glow, winner slot highlight, claw mechanism accent line, subtle board edge glow. That's it.
- The pink should feel like "oh that's a nice touch" not "this is a pink game"

### Animations
- Peg hit: brief scale pulse + brightness flash
- Bumper hit: expand + bright flash + particle burst
- Spinner: continuous rotation, speed changes on hit
- Ball trail: fading warm glow dots behind ball (last 5-8 positions, subtly rose-tinted)
- Claw: mechanical arm visual with grip animation
- Winner slot: pulsing glow, expanding ring effect

### Themes
- **Dark** (default): Dark background, pink accents
- **Light:** Light background, deeper pink accents
- **Neon:** Black background, neon accents (cyan/magenta mix, not just pink)

## Admin Panel

### Section Order
1. **Header:** "PINKO" + "Pinball chaos — drop it and find a winner!"
2. **Drop:** Drop Ball button (pink accent), Drama slider (Low-High)
3. **Mode:** Random / Click toggle, Balls (x1/x3/x5/x10)
4. **Players:** Name input + Add, bulk textarea, + Add All, player list with count
5. **Board:** Size (Small/Medium/Large), Chaos (Mild/Wild/Insane), Regenerate Board button
6. **Winner Mode:** Quick / Dramatic / Escalating toggle buttons
7. **Settings:** Sound toggle, Theme dropdown
8. **Actions:** Reset Results, Clear All Players

### URL Parameters (standard)
| Parameter | Values | Description |
|-----------|--------|-------------|
| `admin` | `true`/`false` | Show/hide admin panel |
| `bg` | `transparent` | Transparent for OBS |
| `theme` | `dark`/`light`/`neon` | Color theme |
| `names` | comma-separated | Pre-load names |

## postMessage Protocol

Namespace: `pinko:`

### Inbound
```
{ type: 'pinko:add', name: 'username' }
{ type: 'pinko:add', names: ['a', 'b'] }
{ type: 'pinko:remove', name: 'username' }
{ type: 'pinko:clear' }
{ type: 'pinko:start' }
{ type: 'pinko:names' }
```

### Outbound
```
{ type: 'pinko:winner', winner: 'username' }
{ type: 'pinko:names', names: [...] }
```

## Architecture

- Single self-contained HTML file (all CSS + JS inline)
- No external dependencies, no build step
- Offline-capable
- ~2000-2500 lines estimated
- Strict mode, IIFE wrapper
- All user input XSS-escaped before rendering
- LocalStorage for settings persistence (namespaced `pinko_`)

## Migration from Plinko

- New directory: `pinko/` (plinko/ stays for backwards compatibility initially)
- Add to homepage game grid
- Update README
- plinko/ can be removed in a future cleanup pass

## What's NOT Included (Future)

- Custom slot labels/prizes (this is a name picker, not a prize wheel)
- Networked multiplayer
- Chat bot integration (handled by separate bot service)
- Leaderboard/history tracking
