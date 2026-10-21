# Streamer Games

Free, open-source games for live streams, made by [Home Office Studios](https://homeofficestudios.com/). Each game is one HTML file with no build step, no framework and no outside dependencies. Add it to OBS as a Browser Source and it runs.

Try them all at **[homeofficestudios.com/games/](https://homeofficestudios.com/games/)**.

<!-- TODO(Bill): add a 16:9 screenshot or GIF here, saved as docs/screenshots/hero.png -->

## The 18 games

| Game | What happens | How chat joins |
|------|--------------|----------------|
| [Wheel of Legends](wheel-legends/) | Giveaway wheel with sealed, checkable spins, Gauntlet eliminations, a rock-paper-scissors final and a claim timer | `!play`, `!play charge`, `!play rock` |
| [Spin Wheel](spin-wheel/) | Colorful wheel for giveaways and random picks | `!play` |
| [Marble Race](marble-race/) | Physics marble drop through pegs and bumpers; first to the bottom wins | `!play` |
| [Bingo](bingo/) | 5x5 bingo with an animated ball draw; first full line wins | `!play` |
| [Trivia](trivia/) | Game-show trivia with your own questions and a live scoreboard | `!play A` to `!play D` |
| [RPS Battle](rps-battle/) | Rock-paper-scissors tournament bracket | `!play`, then `!play rock` |
| [Auction Wars](auction/) | Bid fake currency on mystery items | `!play`, then `!play 250` |
| [Slot Machine](slot-machine/) | Three reels of viewer names; three of one name wins | `!play` |
| [Elimination](elimination/) | Names fade out one by one under a spotlight | `!play` |
| [Hot Potato](hot-potato/) | A potato bounces faster and faster; whoever holds it at the end is out | `!play` |
| [Word Scramble](word-scramble/) | First viewer to unscramble the word wins | `!play yourword` |
| [Treasure Dig](treasure-dig/) | Viewers dig grid squares to find the treasure | `!play`, then `!play B4` |
| [Scratch Card](scratch-card/) | Scratch-off reveal; match three to win | Streamer adds names by hand |
| [Coin Flip](coin-flip/) | 3D coin flip with a team split view | `!play heads` |
| [Number Guess](number-guess/) | Higher or lower hints; closest guess wins | `!play 42` |
| [Dice Roll](dice-roll/) | 3D dice; highest total wins | `!play` |
| [Pinko](pinko/) | Pinball board with bumpers and spinners that picks a winner | `!play` |
| [Plinko](plinko/) | Drop a disc down the pegs and see whose slot it lands in | `!play` |

Most game folders have their own README with URL options and the `postMessage` protocol. Each game also has a short how-to page at `homeofficestudios.com/games/<game>/`.

<!-- TODO(Bill): one screenshot per game in docs/screenshots/<game>.png (16:9, 1280x720 is plenty). None exist yet. -->

## Use it for free

You do not need an account, a download or any code skills.

1. In OBS, add a **Browser Source**.
2. Set the URL to a game, for example `https://homeofficestudios.com/spin-wheel/?admin=false&bg=transparent`.
3. Set the size to your canvas (1920 x 1080 works for most games).
4. Run the game from its control panel. Open the same game URL in a normal browser tab without `admin=false` to see the panel, or add `?view=remote` to use it as an OBS Custom Browser Dock.

To let chat join with `!play`, use [Chat Play](https://homeofficestudios.com/chat/). It works on **Kick** with the Slot Tools chat bot: Chat Play gives you one command to paste into Slot Tools, and that one command works for every game.

Want your own copy? The step-by-step guide for people who have never used GitHub is [docs/SELF-HOST.md](docs/SELF-HOST.md).

## The hosted version with my bot

If you would rather not set anything up, subscribe to [ForTheTwo on Kick](https://kick.com/forthetwo) for $5 a month. The hosted version with my bot then unlocks for your stream. After you subscribe, DM me on Kick and say "Stream Night Kit", and I set it up with you by hand. The games stay free and open source either way. The sub pays for the hosting and my time.

## How it works

- **One file per game.** Everything a game needs is inside its `index.html`.
- **No dependencies.** No CDN and no npm, so the games work offline.
- **Made for OBS.** Transparent backgrounds, sized to the source, no scrollbars.
- **Chat through `postMessage`.** Every game takes commands from a parent page or bot overlay:

```javascript
iframe.contentWindow.postMessage({ type: 'marble:join', name: 'ViewerName' }, '*');
```

Chat Play (`chat/index.html`) is the bridge. A Kick chat bot calls a small relay, the relay passes the message to the open Chat Play tab, and Chat Play forwards it to the game. The relay is run by Home Office Studios and is free to use. Chat Play takes a `?relay=` URL if you want to point it at your own.

## Contributing

Bug reports, fixes and new games are welcome. Read [CONTRIBUTING.md](CONTRIBUTING.md) first. To report a security problem privately, see [SECURITY.md](SECURITY.md).

## License

[MIT](LICENSE). Use it, change it, and put it on your stream. You can sell streams that use it. Keep the license notice if you share the code.
