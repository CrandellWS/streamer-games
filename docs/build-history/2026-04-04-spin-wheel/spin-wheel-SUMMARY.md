# Spin Wheel — Overnight Build Summary

**Date:** 2026-04-04
**Repo:** ~/projects/overnight/streamer-games/
**Status:** Complete and tested

## What Was Built

A premium, self-contained spin wheel game for streamers — the flagship game in the streamer-games collection. Single HTML file, zero dependencies, works offline.

### Core Features
- **Canvas-rendered spin wheel** with 3D gradient segments, beveled outer ring, and center hub
- **Smooth physics animation** using quartic ease-out deceleration (8-14 full rotations)
- **Web Audio API sounds** — tick-tick-tick as pointer passes segments + winner fanfare (arpeggiated chord + shimmer)
- **Confetti celebration** — 200 particles with physics, rotation, and fade
- **Winner overlay** — gold-bordered card with blur backdrop, Close + Remove & Spin Again buttons
- **Gentle ambient animation** — glow pulse + slow idle rotation when not spinning
- **35 distinct segment colors** with radial gradients for depth

### Admin Controls (sidebar)
- Add single name (Enter key support)
- Paste bulk name list (newline or comma-separated)
- Remove individual names (× button with color dot)
- Spin button + Spacebar shortcut
- Spin duration slider (2s–15s)
- Remove winner toggle (for elimination rounds)
- Sound effects toggle
- Clear All / Reset Wheel
- Toggleable panel (gear icon)

### OBS Integration
- `?admin=false` — hides admin panel and toggle button
- `?bg=transparent` — transparent background for overlay
- Responsive to any resolution
- No scrollbars, no overflow

### Three Themes
- **Dark** (default) — deep navy with purple accents
- **Light** — clean white panel, light background
- **Neon** — black background, cyan/magenta accents

### URL Parameters
- `?names=Alice,Bob,Charlie` — pre-load names
- `?admin=true|false` — show/hide admin
- `?bg=transparent` — transparent background
- `?theme=dark|light|neon` — color theme

### Data Persistence
- Names saved to LocalStorage (`spinwheel_names`)
- Persists across page refreshes

## postMessage Chat Bot Protocol

The wheel listens for and emits structured messages for bot integration:

### Inbound (bot → wheel)
```javascript
{ type: 'spinwheel:add', name: 'username' }       // Add one
{ type: 'spinwheel:add', names: ['a', 'b'] }      // Add multiple
{ type: 'spinwheel:remove', name: 'username' }     // Remove one
{ type: 'spinwheel:clear' }                         // Clear all
{ type: 'spinwheel:spin' }                          // Trigger spin
{ type: 'spinwheel:names' }                         // Query entries
```

### Outbound (wheel → parent)
```javascript
{ type: 'spinwheel:winner', winner: 'username', index: 0 }  // Winner
{ type: 'spinwheel:names', names: [...] }                     // Names response
```

## How to Use in OBS

1. **Streamer view**: Open `index.html` in a regular browser window — use admin panel to manage names and spin
2. **OBS overlay**: Add Browser Source with URL `file:///path/to/index.html?admin=false&bg=transparent`, size 800×800
3. Both views share LocalStorage, so names added in the browser window appear on the OBS overlay

## Design Decisions

- **Single HTML file**: Everything inline — no build tools, no CDN, no CORS issues. Just open the file.
- **Canvas rendering**: Chosen over SVG/CSS for smooth 60fps rotation with many segments and gradient fills.
- **Quartic ease-out**: Provides a satisfying fast-start with long dramatic deceleration at the end.
- **Web Audio API**: Programmatic sound generation avoids external audio files while providing satisfying tick and fanfare sounds.
- **35 colors**: Enough distinct colors that even large wheels (30+ names) have visual variety without repeating adjacent colors.
- **Retina canvas**: Renders at 2× resolution for crisp text and edges on high-DPI displays.
- **IIFE wrapper**: All code in a strict-mode IIFE to avoid polluting the global scope.
- **XSS protection**: All user input escaped via DOM textContent before rendering.

## Testing

### Automated Test Suite (test.html)
6/6 tests passing:
1. Clear — empties all names
2. Add single name — via postMessage
3. Add multiple names — batch add
4. Remove name — selective removal
5. Spin — full animation cycle with winner event
6. Duplicate prevention — rejects duplicate names

### Manual Testing Verified
- All three themes render correctly
- Admin panel toggle works
- URL parameters load correctly
- Spin animation is smooth with tick sounds
- Winner overlay displays with confetti
- Remove & Spin Again eliminates winner and auto-spins
- Keyboard shortcuts (Space to spin, Escape to close)
- Responsive sizing at various viewport dimensions

## File Structure
```
streamer-games/
├── CLAUDE.md          # Dev spec for future games
├── LICENSE            # MIT
├── README.md          # Collection overview
└── spin-wheel/
    ├── index.html     # The game (~600 lines, self-contained)
    ├── test.html      # postMessage API test harness
    └── README.md      # Streamer setup guide
```

## Known Limitations

- **No mobile touch support**: Designed for desktop/OBS use. Touch-to-spin could be added.
- **No sound on first interaction**: Browser autoplay policy requires a user gesture before Web Audio API works. First click on Spin resolves this.
- **LocalStorage only**: Names don't sync across devices. A future version could add import/export.
- **No animation for adding/removing names**: Segments update instantly. Could add smooth transitions.
- **Pointer location**: The winning segment is determined by the pointer at the top. With very many segments (50+), text becomes small but still readable.

## Screenshot-Worthy Features

- The 3D gradient wheel with 8 vibrant segments
- The golden pointer with drop shadow
- The ambient glow pulse animation
- The confetti explosion on winner reveal
- The neon theme with cyan/magenta color scheme
- The blurred backdrop winner card with gold border
