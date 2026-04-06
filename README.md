# Streamer Games

A free, open-source collection of interactive games designed for live streamers. Each game works as a standalone HTML file — no build tools, no frameworks, no external dependencies. Drop it into OBS as a Browser Source and go.

## Games

| Game | Description | Status |
|------|-------------|--------|
| [Spin Wheel](spin-wheel/) | Colorful spin wheel for giveaways, viewer picks, and random selection | ✅ Ready |
| [Bingo](bingo/) | Classic 5x5 bingo — caller draws numbers, viewers mark unique auto-generated cards | ✅ Ready |
| [Trivia](trivia/) | Multi-round trivia — host sets questions, viewers answer A/B/C/D, scoreboard | ✅ Ready |
| [RPS Battle](rps-battle/) | Rock Paper Scissors tournament bracket — viewers pick, elimination rounds | ✅ Ready |
| [Auction Wars](auction/) | Viewers bid fake currency on items — countdown timer, gavel slam, leaderboard | ✅ Ready |
| [Word Scramble](word-scramble/) | Scrambled word appears, first viewer to unscramble wins, 6 categories | ✅ Ready |
| [Treasure Dig](treasure-dig/) | Grid of tiles — viewers pick coordinates, find the hidden treasure | ✅ Ready |
| [Scratch Card](scratch-card/) | Animated scratch-off reveal — match 3 symbols to win | ✅ Ready |
| [Hot Potato](hot-potato/) | Potato bounces between players at increasing speed — last one holding it is out | ✅ Ready |
| [Marble Race](marble-race/) | Physics-based marble drop — viewers pick colors, first to finish wins | ✅ Ready |
| [Slot Machine](slot-machine/) | 3-reel slots with viewer names — match 3 for jackpot, coin shower | ✅ Ready |
| [Coin Flip](coin-flip/) | 3D animated coin flip — viewers pick heads/tails, team split view | ✅ Ready |
| [Number Guess](number-guess/) | Higher/lower guessing — closest to secret number wins, heat meter | ✅ Ready |
| [Elimination](elimination/) | Random elimination with spotlight and shatter effects — last one standing wins | ✅ Ready |
| [Dice Roll](dice-roll/) | CSS 3D dice — viewers roll 1-3 dice, highest total wins | ✅ Ready |
| [Plinko](plinko/) | Classic Plinko board — drop a disc, bounce off pegs, land in a viewer's slot | ✅ Ready |

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
