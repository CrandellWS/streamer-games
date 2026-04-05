# Streamer Games

A free, open-source collection of interactive games designed for live streamers. Each game works as a standalone HTML file — no build tools, no frameworks, no external dependencies. Drop it into OBS as a Browser Source and go.

## Games

| Game | Description | Status |
|------|-------------|--------|
| [Spin Wheel](spin-wheel/) | Colorful spin wheel for giveaways, viewer picks, and random selection | ✅ Ready |

## Quick Start

1. Open any game's `index.html` in a browser
2. Add it as an **OBS Browser Source** for stream overlay
3. Use URL parameters to configure (e.g., `?admin=false&bg=transparent`)

## Design Philosophy

- **Single HTML file** — each game is fully self-contained
- **Zero dependencies** — no CDN, no npm, works offline
- **OBS-native** — transparent backgrounds, responsive sizing, no scrollbars
- **Chat-first** — every game works standalone AND integrates with chat bots via `postMessage`
- **Beautiful** — dark themes, smooth animations, 60fps, professional feel

## Chat Bot Integration

All games share a common `postMessage` API. Any chat bot (Nightbot custom page, StreamElements overlay, custom bot) can send commands:

```javascript
// From parent page or bot overlay
iframe.contentWindow.postMessage({ type: 'gamename:action', ... }, '*');
```

See each game's README for its specific protocol.

## License

MIT — use it however you want.
