# Number Guess

A live chat game where viewers guess a secret number. The streamer sees the secret; viewers compete to guess it. Closest wins — or land an exact match for an instant win.

## Overview

- Secret number range: configurable (default 1–100)
- Each viewer submits one guess at a time (configurable to allow re-guesses)
- Higher/lower hints can be revealed by the streamer at any time
- Heat meter shows how close the best current guess is
- Exact match = instant win with jackpot animation
- Otherwise, streamer reveals answer and closest guess wins

## Setup (OBS)

1. Add a **Browser Source** in OBS
2. Point it at the local file: `number-guess/index.html`
3. Recommended size: **1280x720** or **1920x1080**
4. For overlay use (transparent background): add `?bg=transparent` to the URL

### OBS URL Examples

```
# Default dark theme, admin visible
file:///path/to/number-guess/index.html

# Transparent background for overlay
file:///path/to/number-guess/index.html?bg=transparent

# Neon theme, no admin panel
file:///path/to/number-guess/index.html?theme=neon&admin=false

# Custom range 1-500
file:///path/to/number-guess/index.html?min=1&max=500
```

## URL Parameters

| Parameter | Values            | Default | Description                          |
|-----------|-------------------|---------|--------------------------------------|
| `admin`   | `true` / `false`  | `true`  | Show or hide the admin panel         |
| `bg`      | `transparent`     | —       | Transparent background for OBS       |
| `theme`   | `dark` / `light` / `neon` | `dark` | Color theme                 |
| `min`     | integer           | `1`     | Minimum number in range              |
| `max`     | integer           | `100`   | Maximum number in range              |

## Admin Panel Controls

| Button / Toggle       | Action                                              |
|-----------------------|-----------------------------------------------------|
| New Game              | Generates a new secret number, resets all guesses  |
| Min / Max inputs      | Set the guess range (applies on next New Game)      |
| Open Guesses          | Allow incoming guesses                              |
| Close Guesses         | Block incoming guesses                              |
| Show Hint             | Display HIGHER or LOWER based on best guess         |
| Reveal Answer         | Flip reveal the number, announce the winner         |
| Reset                 | Clear everything (no new secret generated)         |
| Accept Guesses toggle | Same as Open/Close buttons                         |
| Sound toggle          | Mute/unmute Web Audio sound effects                |
| Allow re-guess toggle | Let viewers update their guess instead of keeping first |
| Theme buttons         | Switch theme live                                   |
| Gear (⚙)              | Show/hide the admin panel                           |

## postMessage API

The game is controlled via `window.postMessage`. Your bot or overlay controller posts messages to the game's iframe.

### Inbound Messages (bot → game)

```javascript
// Submit a viewer guess
{ type: 'guess:submit', name: 'ViewerName', number: 42 }

// Trigger higher/lower hint
{ type: 'guess:hint' }

// Reveal the answer and announce winner
{ type: 'guess:reveal' }

// Reset game state
{ type: 'guess:reset' }
```

### Outbound Messages (game → parent)

```javascript
// Emitted when a winner is determined (exact match or reveal)
{ type: 'guess:winner', winner: 'ViewerName', guess: 42, answer: 73 }

// Emitted when a hint is shown
{ type: 'guess:hint', direction: 'higher' }  // or 'lower'

// Emitted when game loads and is ready
{ type: 'guess:ready' }

// Emitted when game is reset
{ type: 'guess:reset' }
```

### Bot Integration Example

```javascript
// In your chatbot or overlay controller
const gameFrame = document.querySelector('iframe');

// Listen for commands in chat
chatClient.on('message', (channel, user, message) => {
  const match = message.match(/^!guess\s+(\d+)$/i);
  if (match) {
    gameFrame.contentWindow.postMessage({
      type: 'guess:submit',
      name: user.username,
      number: parseInt(match[1])
    }, '*');
  }
});

// Listen for winner events
window.addEventListener('message', (ev) => {
  if (ev.data.type === 'guess:winner') {
    chatClient.say(channel, `🏆 ${ev.data.winner} wins! The number was ${ev.data.answer}!`);
  }
  if (ev.data.type === 'guess:hint') {
    chatClient.say(channel, `💡 Hint: guess ${ev.data.direction.toUpperCase()}!`);
  }
});
```

## Visual Features

### Number Display
- Shows `?` while game is active
- 200px+ font size with accent glow
- Flip animation on reveal (rotateX 0→90, swap content, 90→0)
- Turns gold on reveal

### Heat Meter
A horizontal gradient bar (blue = cold, red = hot) with a white marker that moves based on the closest current guess.

- Marker moves smoothly with each new guess
- Labels: Cold — Warm — Hot
- Updates in real time as new guesses arrive

### Proximity Colors

Guess history items are color-coded by distance from the secret:

| Distance | Color  |
|----------|--------|
| 0 (exact)| Gold   |
| 1–5      | Red    |
| 6–15     | Orange |
| 16–30    | Yellow |
| 31+      | Blue   |

### Guess History Sidebar
- Sorted by proximity (closest at top)
- Color-coded dots + numbers
- Closest guess highlighted with accent border
- Scrollable, handles large crowds

### Hint Indicator
- Hidden until hint is triggered
- Large animated arrow: ↑ HIGHER (green) or ↓ LOWER (red)
- Spring-in animation

### Winner Banner
- Full overlay with winner name and confetti
- Gold pulse animation
- Shows guess vs answer

## Themes

| Theme | Background | Accent      |
|-------|-----------|-------------|
| Dark  | #0d0d14   | Purple      |
| Light | #f0f0f5   | Purple      |
| Neon  | #0a0a0a   | Cyan/Magenta|

Theme persists across page loads via localStorage.

## Sound Effects

All sounds are generated via the Web Audio API — no external files required.

| Sound   | Trigger                       |
|---------|-------------------------------|
| Blip    | Guess submitted               |
| Swoosh  | Hint revealed                 |
| Reveal  | Answer flip begins            |
| Jackpot | Winner announced (rising arpeggio) |

## State Persistence

Game state (guesses, secret, hint status, winner) is saved to `localStorage` under the key `guess_state`. Reloading the page restores the active game.

## Testing

Open `test.html` in a browser to access the test harness:

- Manual controls: custom name/number inputs, 10-guess bulk submit, exact match finder
- Theme switchers
- Automated test suite (14 tests, click "Run All Tests")
- Live message log showing all inbound/outbound postMessage traffic

## Architecture Notes

- Single HTML file — all CSS and JS are inline
- No external dependencies, no build step, works offline
- `'use strict'` + IIFE to avoid global pollution
- All user input is HTML-escaped before rendering (XSS-safe)
- `overflow: hidden` on body — no scrollbars in OBS
- Web Audio API only — no audio files
- System fonts only — no web font requests
