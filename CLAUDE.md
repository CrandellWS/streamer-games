# Streamer Games — Development Spec

This document defines the conventions and quality standards for all games in the collection.

## File Structure

```
streamer-games/
├── README.md              # Collection overview
├── CLAUDE.md              # This spec file
├── LICENSE                # MIT
├── game-name/
│   ├── index.html         # The game (self-contained)
│   ├── test.html          # postMessage API test harness
│   └── README.md          # Game-specific docs
```

## Game Requirements

### Architecture
- **Single HTML file** — all CSS and JS inline, no external resources
- **No frameworks** — pure HTML/CSS/JS only
- **No build step** — works by opening the file directly
- **Offline-capable** — no CDN, no fetch calls, no external fonts

### OBS Compatibility
- Transparent background support via `?bg=transparent`
- No scrollbars (`overflow: hidden` on body)
- Responsive to any resolution
- Admin controls hidden when `?admin=false`

### URL Parameters (standard across all games)
| Parameter | Values | Description |
|-----------|--------|-------------|
| `admin` | `true`/`false` | Show/hide admin panel (default: true) |
| `bg` | `transparent` | Transparent background for OBS |
| `theme` | `dark`/`light`/`neon` | Color theme (default: dark) |
| `names` | comma-separated | Pre-load names (for applicable games) |

### postMessage Protocol

All games use a namespaced message protocol: `gamename:action`

#### Standard Message Types
```javascript
// Inbound (bot → game)
{ type: 'gamename:add', name: 'username' }      // Add a single entry
{ type: 'gamename:add', names: ['a', 'b'] }     // Add multiple entries
{ type: 'gamename:remove', name: 'username' }    // Remove an entry
{ type: 'gamename:clear' }                        // Clear all entries
{ type: 'gamename:start' }                        // Start/trigger the game action
{ type: 'gamename:names' }                        // Query current entries

// Outbound (game → parent)
{ type: 'gamename:winner', winner: 'username' }  // Winner/result announcement
{ type: 'gamename:names', names: [...] }         // Response to names query
```

### Visual Standards
- Dark theme default with vibrant accents
- 60fps animations
- System fonts only (`'Segoe UI', system-ui, -apple-system, sans-serif`)
- Smooth easing on all transitions
- Professional gradients, shadows, and glow effects
- Ambient idle animations (subtle)
- Responsive — no fixed pixel layouts

### Audio Standards
- Web Audio API only (no external audio files)
- All sounds generated programmatically
- Sound toggle in admin panel
- Sounds: interaction feedback, result announcement

### Data Persistence
- LocalStorage for user-entered data
- Namespaced keys: `gamename_keyname`

### Code Quality
- Strict mode (`'use strict'`)
- IIFE wrapper to avoid globals
- No console.log in production (except errors)
- Accessible: keyboard support, ARIA where appropriate
- XSS-safe: escape all user input before rendering

## Testing

Each game must include a `test.html` that:
1. Embeds the game in an iframe
2. Provides buttons to test each postMessage command
3. Logs all responses from the game
4. Has an automated test suite that verifies the API contract
5. Tests URL parameters by reloading with different query strings

## Adding a New Game

1. Create `game-name/` directory
2. Build `index.html` following all standards above
3. Create `test.html` with full API test coverage
4. Create `README.md` with streamer setup instructions
5. Add the game to the root `README.md` table
6. Commit with message: `feat: add game-name`
