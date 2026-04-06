# Word Scramble — Streamer Game

A live viewer-participation word scramble game for Twitch/YouTube streams. First viewer to type the correct unscrambled word wins the round. Points are tracked across rounds with a live scoreboard.

---

## Quick Start

Open `index.html` in a browser or add it as an OBS Browser Source.

- **Admin panel** (right side): select category, start rounds, give hints
- **Spacebar**: advance to next word
- **H key**: give a hint
- **R key**: reveal the answer

---

## OBS Setup

1. Add a **Browser Source** in OBS
2. Set the URL to the full path: `file:///path/to/word-scramble/index.html?admin=false&bg=transparent`
3. Recommended resolution: **1280x720** or **1920x1080**
4. Check **"Shutdown source when not visible"** to free memory between scenes

### URL Parameters

| Parameter | Values | Default | Description |
|-----------|--------|---------|-------------|
| `admin` | `true` / `false` | `true` | Show or hide the admin panel |
| `bg` | `transparent` | — | Transparent background for OBS overlay |
| `theme` | `dark` / `light` / `neon` | `dark` | Color theme |

**Examples:**
```
index.html                          — full UI, dark theme
index.html?admin=false&bg=transparent  — OBS overlay only
index.html?theme=neon               — neon theme, admin visible
index.html?theme=light&admin=false  — light overlay for bright scenes
```

---

## postMessage API

The game communicates with a parent page or bot via `window.postMessage`.

### Inbound Messages (bot → game)

```javascript
// Player submits a guess
{ type: 'scramble:guess', name: 'ViewerName', word: 'elephant' }

// Advance to next word (host command)
{ type: 'scramble:next' }

// Reveal one letter hint
{ type: 'scramble:hint' }

// Query current scores (game will emit scramble:scores in response)
{ type: 'scramble:scores' }

// Reset all scores and restart
{ type: 'scramble:reset' }
```

### Outbound Messages (game → parent)

```javascript
// A viewer guessed correctly
{ type: 'scramble:winner', winner: 'ViewerName', word: 'elephant', round: 3 }

// Scores snapshot (response to query, or after each win)
{ type: 'scramble:scores', scores: [ { name: 'Alice', points: 5 }, { name: 'Bob', points: 2 } ] }
```

### Wiring in a Bot

```javascript
// In your iframe parent page or Electron wrapper:
const frame = document.getElementById('game-frame');

// Send a viewer guess
function onChatMessage(username, message) {
  frame.contentWindow.postMessage({
    type: 'scramble:guess',
    name: username,
    word: message.trim()
  }, '*');
}

// Listen for results
window.addEventListener('message', (event) => {
  if (event.data.type === 'scramble:winner') {
    console.log(`${event.data.winner} won round ${event.data.round}!`);
    // Award channel points, announce in chat, etc.
  }
  if (event.data.type === 'scramble:scores') {
    console.log('Current scores:', event.data.scores);
  }
});

// Advance to next word (host presses button or timer fires)
frame.contentWindow.postMessage({ type: 'scramble:next' }, '*');
```

---

## Game Flow

1. A scrambled word appears as large letter tiles
2. Viewers type the unscrambled word in chat
3. The bot forwards guesses via `scramble:guess`
4. The first correct guess wins the round (+1 point)
5. Winner banner appears, tiles flip to reveal the word
6. Host advances to next word via button, Spacebar, or `scramble:next`
7. Scores persist across rounds until `scramble:reset`

---

## Tile Animations

The letter tiles are the hero of the game:

- **Entry**: Tiles fly in from above with staggered timing and a physical bounce settle
- **Shuffle**: When hinting, tiles scatter and resettle (triggered by the Hint button)
- **Hint flip**: A specific tile flips 180° to reveal its letter (Scrabble-style gold glow)
- **Win flip**: All tiles flip in sequence to spell the correct word (green glow)
- **Reveal flip**: Tiles flip to show the answer (no win color)

Tiles are styled as Scrabble-style pieces: cream face, serif font, dark border, letter value pip in the corner.

---

## Categories

| Category | Sample Words |
|----------|-------------|
| Animals | elephant, giraffe, penguin, dolphin, cheetah, gorilla, flamingo, crocodile |
| Food | spaghetti, avocado, broccoli, cinnamon, chocolate, jalapeno, blueberry |
| Sports | basketball, volleyball, skateboard, gymnastics, wrestling, badminton |
| Tech | keyboard, algorithm, javascript, database, framework, terminal, compiler |
| Gaming | controller, inventory, multiplayer, achievement, respawn, speedrun |
| Movies | avengers, inception, interstellar, gladiator, titanic, matrix |
| Custom | Add your own words via the admin panel |

### Adding Custom Words

1. Select **Custom** from the category dropdown in the admin panel
2. Type a word in the input field and click **+** or press Enter
3. Words must be 3+ letters (letters only, no spaces)
4. Custom words are used for the current session only

---

## Sound Effects

All sounds are generated via the Web Audio API — no external files required.

| Event | Sound |
|-------|-------|
| New word / round advance | Sweeping whoosh |
| Tile shuffle (hint button) | Percussive clicks |
| Hint reveal | Soft ascending tone pair |
| Correct guess | Ascending bell arpeggio |
| Answer reveal | Descending tone |

Sound can be toggled in the admin panel.

---

## Keyboard Shortcuts

| Key | Action |
|-----|--------|
| Space | Next word |
| H | Give hint |
| R | Reveal answer |

---

## Scoring

- +1 point per correct guess (first correct answer wins)
- Top 5 shown in the live left-side scoreboard
- Full top 10 in the admin panel scoreboard
- Scores persist until manually reset

---

## Testing

Open `test.html` to access the full test harness:

- Manual control buttons for all API messages
- Custom guess sender
- Multi-player race simulation
- Win streak simulation
- Theme / URL param switcher
- Automated test suite (10 tests covering API contract)

```
open test.html
```

---

## Technical Details

- **Single file**: all CSS and JS inline, zero external dependencies
- **No frameworks**: pure HTML5 / CSS3 / ES6+
- **Offline capable**: works without any network connection
- **Audio**: Web Audio API, programmatically generated
- **Animations**: CSS transforms + requestAnimationFrame, targeting 60fps
- **XSS safe**: all user input escaped before DOM insertion
- **Responsive**: adapts tile size for words up to 12 letters

---

## File Structure

```
word-scramble/
├── index.html   — The game (self-contained)
├── test.html    — postMessage API test harness
└── README.md    — This file
```
