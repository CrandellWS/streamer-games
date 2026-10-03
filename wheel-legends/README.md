# Wheel of Legends

A free giveaway wheel for streamers. You can prove every spin is fair, chat can join and power it up, and you can run it as one quick spin or as a full elimination Gauntlet that ends in a rock-paper-scissors final duel.

**Live:** https://homeofficestudios.com/wheel-legends/

## Quick start

1. Open `wheel-legends/` in a browser (or add it as an OBS Browser Source).
2. Add names: paste them in the panel, use `?names=Alice,Bob,Cara`, or let chat join (see below).
3. Pick a mode and press **SPIN** (or Space, or click the wheel).

For OBS, use `?admin=false&bg=transparent` and drive the wheel from Chat Play or your bot.

## Modes

- **Classic:** one spin, one winner. You can choose to take the winner off the wheel afterwards.
- **Gauntlet:** each spin **eliminates** the name it lands on, shows an ELIMINATED card, and spins again on its own until two remain. Then comes the **final duel**:
  - The two finalists play rock-paper-scissors from chat (`!play rock` / `paper` / `scissors`). Only the first pick counts.
  - A tie replays the round.
  - Each round has a 30 second timer. A finalist who doesn't pick gets a fair random pick (crypto random), and the screen says so plainly. Random picks never cause an endless tie.
  - The streamer can tap either finalist to declare them the winner.
  - Entries are locked while a Gauntlet runs. **New round** puts everyone back on the wheel.
  - Elimination spins can be **Epic** (6 to 10 s each) or **Quick** (about 3 s each).

## Chat commands (with Chat Play)

Open [Chat Play](../chat/?game=wheel-legends), pick *Wheel of Legends* and paste its one Slot Tools command. Then viewers type:

| Command | What it does |
|---|---|
| `!play` | Enter the wheel (your name flies on) |
| `!play charge` (or `spin`, `power`) | Fill the chat power meter (looks only) |
| `!play rock` / `paper` / `scissors` | Finalists' duel pick |
| `!play claim` | The winner claims the prize before the claim timer runs out |
| `!play count` / `!play list` | How many are in / who is in |

The streamer starts the spin. Chat can't trigger it.

## Provably fair

Before every spin the wheel makes a fresh random 32-byte **seed** (shown as 64 hex characters) and displays its **sealed code**:

```
sealed code = SHA-256(seed)                    (the seed as lowercase hex text, UTF-8)
```

The result is computed from the seed **before the wheel moves**:

```
h     = SHA-256(seed + ":" + spinNumber)       e.g. SHA-256("9f3c…e1:4")
index = (first 8 bytes of h, as a big-endian unsigned integer) mod n
winner (or eliminated) = entries[index]
```

`n` is the number of names on the wheel at that spin. `entries` is their entry order, numbered from 0 (eliminated names are skipped). `spinNumber` counts spins in the current round, starting at 1. The animation is then planned to land exactly on `entries[index]`.

After the spin the seed is revealed. **Verify** (on the winner card, the seed strip, the panel, or the `V` key) recomputes both steps in the page and lists the entries. To check it yourself:

```bash
echo -n "$SEED" | sha256sum            # must equal the sealed code
python3 -c "import hashlib;h=hashlib.sha256(b'$SEED:$SPIN').digest();print(int.from_bytes(h[:8],'big') % $N)"
```

**What this proves, honestly:** the result was fixed before the animation started and the wheel showed it truthfully. Nobody can steer the animation. With a 64-bit number, the modulo bias is far below one in a billion. It does not prove the seed itself was random, because the page makes the seed, so the open source code is your guarantee there. Each winner's seed and sealed code are also saved in the winner log.

### Chat power is cosmetic

`legends:charge` fills a meter. A full meter makes the next spin wilder: more turns, brighter glow, sparks, faster music. It is applied **after** the result is fixed and never changes which slice wins. The same goes for the near-miss stop position inside the slice.

## After the win

- **Claim timer:** off / 30 / 60 / 90 / 120 s. The winner types `!play claim` (`legends:claim`). The streamer can also tap the claim pill to mark it claimed, or tap again to undo. Anyone else trying to claim gets a "nice try".
- **Winner log:** every winner is saved in this browser (`localStorage`, key `legends_winners`) with mode, claim status and the spin's seal and seed. It survives a refresh. You can copy it or clear it with two taps.
- **Winner tab:** opens `winners.html?w=Name&s=status&m=mode&t=time` once and keeps it pointed at the latest winner. It's handy as a second OBS source (`&bg=transparent`).

## Branding

Center hub text, a logo upload (resized to 512 px and stored in this browser), and eight wheel colour presets. All of them are saved in `localStorage`.

## URL parameters

| Param | Values | |
|---|---|---|
| `admin` | `false` | Hide the panel (OBS) |
| `bg` | `transparent` | Transparent background |
| `theme` | `dark` / `light` / `neon` | Page theme (`neon` also picks the neon wheel colours if you haven't chosen any) |
| `names` | comma separated | Pre-load names |
| `cmd` | e.g. `!wheel` | Chat command shown on screen (default `!play`) |
| `speed` | e.g. `4` | Run every animation N times faster (demos/testing; cosmetic only) |

## postMessage API (`legends:` namespace)

Inbound (bot or parent page → wheel):

```js
{ type: 'legends:add', name: 'alice' }          // also legends:join; or names: ['a','b']
{ type: 'legends:remove', name: 'alice' }
{ type: 'legends:clear' }
{ type: 'legends:names' }                        // replies legends:names
{ type: 'legends:start' }                        // also legends:spin
{ type: 'legends:mode', mode: 'classic' | 'gauntlet' }
{ type: 'legends:reset' }                        // new round, everyone back on
{ type: 'legends:charge', name: 'bob' }          // cosmetic power, 1 per person per 2.5 s
{ type: 'legends:pick', name: 'alice', choice: 'rock' | 'paper' | 'scissors' }
{ type: 'legends:claim', name: 'alice' }
```

Outbound (wheel → parent):

```js
{ type: 'legends:names', names: [...], alive: [...], phase, mode }
{ type: 'legends:result', seedCommit, seed, index, name, spin, names }   // every spin
{ type: 'legends:eliminated', name }                                      // Gauntlet
{ type: 'legends:duel', finalists: [a, b] }
{ type: 'legends:winner', winner }
{ type: 'legends:claimed', name }  /  { type: 'legends:missed', name }
```

Names are trimmed, capped at 24 characters, stripped of `<>` and control characters, and de-duplicated case-insensitively. A wheel holds up to 500 names.

`test.html` is an interactive harness with an automated API check.
