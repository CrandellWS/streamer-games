# Trivia — Streamer Game

A live trivia game for streamers. Host loads questions, viewers answer via chat, a scoreboard tracks points across rounds. Game show aesthetic with reveal animations, countdown timer, and position animations.

---

## Quick Start

1. Open `index.html` in a browser or add as an OBS Browser Source.
2. Click **Load Sample Questions** to populate the queue.
3. Click **Start Question** (or press **Space**) to begin.
4. Feed `trivia:answer` messages from your chat bot as viewers answer.
5. Click **Reveal Answer** when time is up (or let the timer auto-reveal).
6. Click **Next Question** to advance.
7. At the end of the queue the winner screen appears.

---

## URL Parameters

| Parameter | Values | Description |
|-----------|--------|-------------|
| `admin` | `true` / `false` | Show/hide admin panel (default: `true`) |
| `bg` | `transparent` | Transparent background for OBS overlay use |
| `theme` | `dark` / `light` / `neon` | Color theme (default: `dark`) |

### Examples

```
index.html                          — default dark, admin panel visible
index.html?bg=transparent           — OBS overlay mode (no background)
index.html?theme=neon&admin=false   — neon theme, no admin panel
index.html?admin=false              — viewer-facing display only
```

---

## OBS Setup

1. Add a **Browser Source** in OBS.
2. Set the URL to the full path of `index.html` (or host it on a local web server).
3. Recommended resolution: `1920×1080` or `1280×720`.
4. For overlay use (transparent background): append `?bg=transparent&admin=false`.
5. Interact with the admin panel from a second browser window or your control PC.

---

## Chat Bot Integration (postMessage API)

All communication uses `window.postMessage` with the namespace `trivia:`.

### Inbound Messages (bot → game)

#### `trivia:answer` — Submit a viewer's answer
```javascript
window.postMessage({ type: 'trivia:answer', name: 'Alice', choice: 'B' }, '*');
```
| Field | Type | Description |
|-------|------|-------------|
| `name` | string | Viewer's username (max 64 chars) |
| `choice` | `"A"` / `"B"` / `"C"` / `"D"` | The chosen answer letter |

Rules:
- Only the viewer's **first** answer per question is accepted.
- Answers submitted when no question is active are ignored.
- Invalid choices (not A/B/C/D) are silently dropped.

#### `trivia:next` — Advance to next state
```javascript
window.postMessage({ type: 'trivia:next' }, '*');
```
Equivalent to the admin clicking the **Next Question** button. If a question is active it reveals the answer; if already revealed it advances to the next question.

#### `trivia:scores` — Query current scores
```javascript
window.postMessage({ type: 'trivia:scores' }, '*');
```
The game responds immediately with a `trivia:scores` outbound message containing all current scores.

#### `trivia:reset` — Reset everything
```javascript
window.postMessage({ type: 'trivia:reset' }, '*');
```
Clears all scores, answers, and returns to idle state.

---

### Outbound Messages (game → parent)

The game dispatches these on `window.parent` (iframe) and also on `window` (direct use).

#### `trivia:winner` — Emitted when the question queue ends
```javascript
{ type: 'trivia:winner', winner: 'Alice', score: 7 }
```
| Field | Type | Description |
|-------|------|-------------|
| `winner` | string | Username of the top scorer |
| `score` | number | Their final score |

#### `trivia:scores` — Current scoreboard
```javascript
{
  type: 'trivia:scores',
  scores: [
    { name: 'Alice', score: 7 },
    { name: 'Bob',   score: 5 },
    { name: 'Carol', score: 3 }
  ]
}
```
Emitted automatically after each reveal and at game end. Also emitted in response to a `trivia:scores` query.

#### `trivia:answered` — Per-viewer answer result (emitted on reveal)
```javascript
{ type: 'trivia:answered', name: 'Alice', choice: 'B', correct: true }
```
One event is emitted per viewer who submitted an answer when the answer is revealed. Use this to announce correct/incorrect results in chat.

---

## Question Format (JSON)

Questions can be bulk-imported via the admin panel's **JSON Import** field.

```json
[
  {
    "q": "What is the largest planet in our solar system?",
    "a": ["Mars", "Jupiter", "Saturn", "Neptune"],
    "correct": 1
  },
  {
    "q": "Who wrote Romeo and Juliet?",
    "a": ["Dickens", "Shakespeare", "Austen", "Twain"],
    "correct": 1
  }
]
```

| Field | Type | Description |
|-------|------|-------------|
| `q` | string | The question text |
| `a` | string[4] | Exactly 4 answer choices (maps to A/B/C/D) |
| `correct` | number | Zero-based index of the correct answer (0=A, 1=B, 2=C, 3=D) |

---

## Admin Panel Reference

| Control | Description |
|---------|-------------|
| **Start Question** | Starts the next question in queue. Spacebar shortcut. |
| **Reveal Answer** | Reveals correct/wrong highlight and updates scores. |
| **Next Question** | Advances to the next question (or ends the game). |
| **Timer pills** | 15s / 30s / 60s / ∞ — auto-reveals when time runs out |
| **Question Editor** | Type a question + 4 answers, select correct answer, click Add |
| **Load Sample Questions** | Loads 10 built-in sample questions |
| **JSON Import** | Paste a JSON array to bulk-import questions |
| **Question Queue** | Shows all queued questions; click × to remove one |
| **Clear Queue** | Removes all queued questions |
| **Query Scores** | Sends a `trivia:scores` outbound event |
| **Reset** | Clears all scores and returns to idle |
| **Theme** | Switch dark / light / neon |
| **Sound toggle** | Enable / disable all Web Audio sounds |
| **⚙ button** | Show/hide the admin panel |

---

## Keyboard Shortcuts

| Key | Action |
|-----|--------|
| **Space** | Start question → Reveal answer → Next question (cycles through phases) |
| **Shift+R** | Reveal answer |

---

## Audio

All sounds are generated with the Web Audio API — no external files required.

| Sound | Trigger |
|-------|---------|
| Thinking music loop | Plays while a question is active |
| Timer ticks | Every second when ≤ 10s remaining |
| Correct buzz (ascending) | On answer reveal |
| Wrong buzz (descending) | On answer reveal |
| Winner fanfare | When game ends and winner is shown |

---

## Scoring

- Each correctly answered question awards **1 point**.
- Only a viewer's **first** answer per question counts.
- Scores persist in `localStorage` under keys `trivia_questions` and `trivia_scores`.
- Scores accumulate across rounds until **Reset** is pressed.
- The scoreboard re-sorts with smooth animation after each reveal.
- Leader gets a gold highlight and 🥇/🥈/🥉 medals for top 3.

---

## Testing

Open `test.html` in a browser alongside the game. The test page embeds `index.html` in an iframe and provides:

- Manual control buttons for every postMessage command
- Multi-viewer simulation (5 correct / 10 mixed answers)
- URL parameter reload buttons (themes, transparent BG, no-admin)
- Real-time message log (inbound and outbound)
- Automated test suite with 12 tests covering the full API contract

---

## Architecture Notes

- Single HTML file, all CSS and JS inline — no external dependencies.
- Pure vanilla JS, no frameworks, no build step.
- `'use strict'` + IIFE wrapper, no global leakage.
- XSS-safe: all user content rendered via `textContent` or explicit escaping.
- `overflow: hidden` on `html` and `body` — no scrollbars in OBS.
- Responsive layout: fills any viewport.
- `localStorage` namespaced with `trivia_` prefix.
