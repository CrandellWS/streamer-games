# Streamer Games — Build Queue

Each game follows the spec in [CLAUDE.md](./CLAUDE.md): single self-contained HTML file, dark theme default, OBS-ready, postMessage API, Web Audio, automated tests.

## Status Key
- ✅ Complete
- ✅ Complete
- ✅ Queued

---

## Games

| # | Game | Directory | Status | Description |
|---|------|-----------|--------|-------------|
| 1 | Spin Wheel | `spin-wheel/` | ✅ | Colorful wheel for giveaways and random picks |
| 2 | Bingo | `bingo/` | ✅ | Classic 5x5 bingo — caller draws numbers, viewers mark cards |
| 3 | Trivia | `trivia/` | ✅ | Multi-round trivia — host sets questions, viewers answer via chat |
| 4 | Rock Paper Scissors | `rps-battle/` | ✅ | Tournament bracket — viewers pick RPS, elimination rounds |
| 5 | Auction Wars | `auction/` | ✅ | Viewers bid fake currency on mystery items, highest bidder wins |
| 6 | Word Scramble | `word-scramble/` | ✅ | Scrambled word appears, first to unscramble in chat wins |
| 7 | Treasure Dig | `treasure-dig/` | ✅ | Grid of tiles — viewers pick coordinates, find the treasure |
| 8 | Scratch Card | `scratch-card/` | ✅ | Animated scratch-off reveal — match 3 to win |
| 9 | Hot Potato | `hot-potato/` | ✅ | Name cycles through viewers on a timer — whoever holds it when time runs out is eliminated |
| 10 | Marble Race | `marble-race/` | ✅ | Physics-based marble drop — viewers pick colors, first to finish wins |
| 11 | Slot Machine | `slot-machine/` | ✅ | 3-reel slot pull — match symbols to win, viewer names on reels |
| 12 | Coin Flip | `coin-flip/` | ✅ | Heads or tails — viewers pick sides, animated 3D flip |
| 13 | Number Guess | `number-guess/` | ✅ | Higher/lower guessing game — closest to the secret number wins |
| 14 | Elimination | `elimination/` | ✅ | Last one standing — random eliminations with dramatic reveals |
| 15 | Dice Roll | `dice-roll/` | ✅ | Animated 3D dice — viewers roll, highest total wins |

---

## Game Specs

### 2. Bingo (`bingo/`)
**Mechanic:** Host starts a game, caller draws numbers (1-75) with animated ball drop. Viewers get unique auto-generated cards. First to complete a row/column/diagonal wins.
**postMessage namespace:** `bingo:`
**Key actions:** `bingo:join` (generate card for viewer), `bingo:draw` (draw next number), `bingo:check` (verify a bingo claim), `bingo:reset`
**Visual:** Retro bingo hall aesthetic — illuminated ball hopper, animated ball tumble, card stamp animation.
**Audio:** Ball drop sound, stamp sound, bingo winner fanfare.

### 3. Trivia (`trivia/`)
**Mechanic:** Host loads questions (manual entry or paste JSON). Question displays with 4 choices (A/B/C/D). Viewers answer in chat. Scoreboard tracks across rounds. Configurable timer per question.
**postMessage namespace:** `trivia:`
**Key actions:** `trivia:answer` (viewer submits answer), `trivia:next` (advance to next question), `trivia:scores`, `trivia:reset`
**Visual:** Game show style — question card with reveal animation, countdown timer bar, live scoreboard with position changes.
**Audio:** Thinking music loop, correct/wrong buzzer, final winner theme.

### 4. Rock Paper Scissors (`rps-battle/`)
**Mechanic:** Tournament bracket. Viewers join, randomly paired. Each round: pick R/P/S via chat. Winners advance. Visual bracket fills in. Last one standing wins.
**postMessage namespace:** `rps:`
**Key actions:** `rps:join`, `rps:pick` (r/p/s), `rps:start` (begin tournament), `rps:result`
**Visual:** Animated bracket tree, hand gesture animations for reveals, VS splash screen between matchups.
**Audio:** Countdown beeps, clash sound on reveal, crowd cheer for winner.

### 5. Auction Wars (`auction/`)
**Mechanic:** Host creates items (text + optional emoji icon). Viewers bid with fake currency (everyone starts equal). Timer counts down, highest bid wins. Multiple rounds.
**postMessage namespace:** `auction:`
**Key actions:** `auction:bid` (amount), `auction:item` (create new item), `auction:sold`, `auction:balances`
**Visual:** Auction house aesthetic — item showcase pedestal, rising bid ticker, going-going-gone gavel animation.
**Audio:** Bid ding, auctioneer gavel slam, sold fanfare.

### 6. Word Scramble (`word-scramble/`)
**Mechanic:** Host loads word list (or uses built-in categories). Scrambled word displays with animated letter tiles. First viewer to type the correct word in chat wins the round. Points across rounds.
**postMessage namespace:** `scramble:`
**Key actions:** `scramble:guess` (viewer's word), `scramble:next`, `scramble:hint` (reveal one letter), `scramble:scores`
**Visual:** Letter tiles that shuffle/animate into place, hint reveals with flip animation, scoreboard sidebar.
**Audio:** Tile shuffle sound, correct chime, hint reveal tone.

### 7. Treasure Dig (`treasure-dig/`)
**Mechanic:** Grid of covered tiles (6x6 to 10x10, configurable). One tile hides the treasure. Viewers pick coordinates (e.g., "B3") in chat. Tiles reveal dirt, rocks, or the treasure. Last dig wins.
**postMessage namespace:** `treasure:`
**Key actions:** `treasure:dig` (coordinate), `treasure:reset`, `treasure:resize` (grid size)
**Visual:** Top-down dirt grid, dig animation with particles, treasure chest glow reveal, X-marks-the-spot for near misses.
**Audio:** Shovel dig sound, rock clink for misses, treasure jingle for winner.

### 8. Scratch Card (`scratch-card/`)
**Mechanic:** Giant scratch card on screen. Host triggers the scratch reveal (animated). Match 3 symbols = win. Can be used as a giveaway reveal or just entertainment. Viewer names can appear as prizes.
**postMessage namespace:** `scratch:`
**Key actions:** `scratch:reveal`, `scratch:set` (configure prizes/symbols), `scratch:reset`
**Visual:** Metallic scratch surface with realistic scratch-off animation, sparkle on reveals, winner explosion.
**Audio:** Scratch sound effect, symbol reveal chime, winner celebration.

### 9. Hot Potato (`hot-potato/`)
**Mechanic:** Names cycle around a ring/circle at increasing speed. Timer is hidden. When it stops, whoever "holds" the potato is out. Repeat until one remains.
**postMessage namespace:** `potato:`
**Key actions:** `potato:join`, `potato:start`, `potato:eliminated`, `potato:winner`
**Visual:** Circular player arrangement, glowing potato bouncing between names, speed increases, explosion on elimination.
**Audio:** Ticking that speeds up, sizzle sound, explosion on elimination, winner cheer.

### 10. Marble Race (`marble-race/`)
**Mechanic:** Viewers join and get assigned a colored marble. Race track with randomized obstacles renders. Marbles drop and physics takes over. First marble to the finish line wins.
**postMessage namespace:** `marble:`
**Key actions:** `marble:join`, `marble:start`, `marble:winner`
**Visual:** Side-view race track with pegs, bumpers, funnels. Marbles are circles with viewer name labels. Satisfying physics bouncing.
**Audio:** Marble clinking, crowd murmur, finish line bell.

### 11. Slot Machine (`slot-machine/`)
**Mechanic:** 3-reel slot machine. Viewer names on the reels. Pull the lever — if 3 of the same name land, that viewer wins. Configurable reel contents.
**postMessage namespace:** `slots:`
**Key actions:** `slots:add` (name to reels), `slots:pull`, `slots:winner`, `slots:clear`
**Visual:** Classic slot machine with chrome frame, spinning reels with easing, flashing lights on win, coin shower.
**Audio:** Lever pull, reel spinning, reel stop clicks, jackpot siren + coins.

### 12. Coin Flip (`coin-flip/`)
**Mechanic:** Viewers pick heads or tails in chat. Animated 3D coin flip. Winning side revealed. Can be used for team splits, yes/no decisions, or viewer vs viewer.
**postMessage namespace:** `coin:`
**Key actions:** `coin:pick` (heads/tails), `coin:flip`, `coin:result`
**Visual:** Realistic 3D coin rotation with motion blur, slow-mo landing, team split view showing who picked what.
**Audio:** Coin ring on flip, air whoosh, metallic landing clink.

### 13. Number Guess (`number-guess/`)
**Mechanic:** Secret number (1-100 or configurable range). Viewers guess in chat. After each round of guesses, "higher" or "lower" hint shown. Closest guess wins, or exact match for instant win.
**postMessage namespace:** `guess:`
**Key actions:** `guess:submit` (number), `guess:hint`, `guess:reveal`, `guess:reset`
**Visual:** Large number display with flip animation, higher/lower arrows, proximity heat meter, guess history sidebar.
**Audio:** Submit blip, higher/lower swoosh, exact match jackpot.

### 14. Elimination (`elimination/`)
**Mechanic:** All viewers join. Random elimination one at a time with dramatic countdown. Last person standing wins. Configurable elimination speed.
**postMessage namespace:** `eliminate:`
**Key actions:** `eliminate:join`, `eliminate:start`, `eliminate:speed` (fast/slow/dramatic), `eliminate:winner`
**Visual:** Names in a grid/circle, spotlight cycles through names, eliminated names fade/shatter, final two showdown.
**Audio:** Drumroll, spotlight sweep, elimination buzz, winner trumpets.
**Note:** Different from Elimination Protocol (which is a social deduction game). This is pure random elimination.

### 15. Dice Roll (`dice-roll/`)
**Mechanic:** Viewers join, each rolls 1-3 dice (configurable). Animated 3D dice roll. Highest total wins. Ties re-roll.
**postMessage namespace:** `dice:`
**Key actions:** `dice:join`, `dice:roll`, `dice:result`, `dice:reset`
**Visual:** 3D dice with physics bounce, viewer name + roll result cards, leaderboard sorting animation.
**Audio:** Dice rattle in hand, table bounce, result reveal chime.

---

## Build Priority Notes

- **Visual impact first**: Marble Race, Bingo, and Slot Machine are the most visually impressive for stream demos
- **Quick wins**: Coin Flip, Dice Roll, and Number Guess are simpler builds — good for rapid momentum
- **Chat engagement**: Trivia, Word Scramble, and Auction drive the most chat interaction
- **The build order above is suggested but flexible** — Oracle picks the next build based on mood and momentum
