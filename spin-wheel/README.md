# Spin Wheel

A beautiful, animated spin wheel for streamers — perfect for giveaways, viewer picks, and random selection.

## Quick Start

Open `index.html` in any modern browser. That's it.

## OBS Setup

1. Add a **Browser Source** in OBS
2. Set the URL to your local file path or hosted URL:
   ```
   file:///path/to/spin-wheel/index.html?admin=false&bg=transparent
   ```
3. Set width/height to match your canvas (e.g., 800×800)
4. Check "Shutdown source when not visible" for performance

### Recommended OBS Settings

| Setting | Value |
|---------|-------|
| Width | 800 |
| Height | 800 |
| URL params | `?admin=false&bg=transparent` |

Keep a **separate browser window** open with the admin panel to control the wheel while the OBS source shows only the wheel itself.

## Admin Controls

The admin panel (right sidebar) provides:

- **Add Names** — type a name and press Enter, or paste a bulk list
- **Remove Names** — click × next to any name
- **Spin** — click the Spin button or press **Spacebar**
- **Remove Winner** toggle — automatically remove the winner after each spin (for elimination rounds)
- **Spin Duration** — adjust from 2s to 15s
- **Sound Effects** — toggle tick sounds and winner fanfare
- **Clear All** — remove all names
- **Reset Wheel** — reset rotation to starting position

## URL Parameters

| Parameter | Values | Default | Description |
|-----------|--------|---------|-------------|
| `names` | comma-separated | — | Pre-load names: `?names=Alice,Bob,Charlie` |
| `admin` | `true`/`false` | `true` | Show/hide the admin panel |
| `bg` | `transparent` | solid | Transparent background for OBS overlay |
| `theme` | `dark`/`light`/`neon` | `dark` | Color theme |

### Examples

```
index.html?names=Alice,Bob,Charlie,Diana&theme=neon
index.html?admin=false&bg=transparent
index.html?theme=light&names=Team1,Team2,Team3,Team4
```

## Chat Bot Integration (postMessage API)

The wheel listens for `postMessage` commands, so any chat bot or parent page can control it programmatically.

### Inbound Messages (bot → wheel)

```javascript
// Add a single name
iframe.contentWindow.postMessage({
  type: 'spinwheel:add',
  name: 'username'
}, '*');

// Add multiple names at once
iframe.contentWindow.postMessage({
  type: 'spinwheel:add',
  names: ['Alice', 'Bob', 'Charlie']
}, '*');

// Remove a name
iframe.contentWindow.postMessage({
  type: 'spinwheel:remove',
  name: 'username'
}, '*');

// Clear all names
iframe.contentWindow.postMessage({
  type: 'spinwheel:clear'
}, '*');

// Trigger a spin
iframe.contentWindow.postMessage({
  type: 'spinwheel:spin'
}, '*');

// Query current names (response sent back via postMessage)
iframe.contentWindow.postMessage({
  type: 'spinwheel:names'
}, '*');
```

### Outbound Messages (wheel → parent)

```javascript
// Winner announcement (sent after spin completes)
{ type: 'spinwheel:winner', winner: 'username', index: 0 }

// Names list response (sent in reply to spinwheel:names)
{ type: 'spinwheel:names', names: ['Alice', 'Bob', 'Charlie'] }
```

### Example: Simple Chat Integration

```html
<iframe id="wheel" src="spin-wheel/index.html?admin=false&bg=transparent"></iframe>
<script>
  const wheel = document.getElementById('wheel');

  // When someone types !join in chat
  function onChatMessage(username, message) {
    if (message === '!join') {
      wheel.contentWindow.postMessage({
        type: 'spinwheel:add',
        name: username
      }, '*');
    }
    if (message === '!spin' && isModerator(username)) {
      wheel.contentWindow.postMessage({
        type: 'spinwheel:spin'
      }, '*');
    }
  }

  // Listen for the winner
  window.addEventListener('message', (event) => {
    if (event.data.type === 'spinwheel:winner') {
      sendChatMessage(`🎉 The winner is ${event.data.winner}!`);
    }
  });
</script>
```

## Keyboard Shortcuts

| Key | Action |
|-----|--------|
| **Space** | Spin the wheel |
| **Escape** | Close winner overlay |

## Features

- Smooth physics-based spin animation with quartic easing
- Tick-tick-tick sound as the pointer passes segments (Web Audio API)
- Winner fanfare with confetti celebration
- 35 distinct segment colors
- 3D-look wheel with gradients and beveled edges
- Gentle ambient glow pulse and slow idle rotation
- Names persist in LocalStorage between sessions
- Duplicate name prevention
- Responsive to any resolution
- Three themes: dark, light, neon

## Technical Details

- Pure HTML/CSS/JS — no dependencies
- Canvas-based wheel rendering at 2× resolution (retina support)
- Web Audio API for all sound effects (no audio files)
- Runs at 60fps
- ~600 lines of self-contained code

## License

MIT
