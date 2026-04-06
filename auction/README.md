# Auction Wars

A live fake-currency auction game for streamers. Host creates items, viewers bid in real time, countdown timer, dramatic gavel slam when sold. Integrates with any bot via `postMessage`.

---

## Quick Start

1. Open `index.html` in a browser or add as OBS Browser Source
2. Add bidders in the admin panel (or via postMessage from your bot)
3. Enter an item name and emoji, click **List Item**
4. Let viewers bid via `auction:bid` messages
5. Hit **SOLD! 🔨** (or press Spacebar) to end the round

---

## URL Parameters

| Parameter | Values | Default | Description |
|-----------|--------|---------|-------------|
| `admin`   | `true` / `false` | `true` | Show/hide admin panel |
| `bg`      | `transparent` | — | Transparent background (OBS) |
| `theme`   | `dark` / `light` / `neon` | `dark` | Color theme |
| `names`   | `Alice,Bob,Charlie` | — | Pre-load bidders |
| `balance` | `1000` | `1000` | Starting balance for URL-loaded bidders |

**Examples:**

```
index.html                                        # Local admin view
index.html?bg=transparent&admin=false             # OBS overlay, no panel
index.html?theme=neon&names=Alice,Bob&balance=2000
```

---

## postMessage API

All messages use the namespace `auction:`.

### Inbound (bot → game)

#### `auction:join` — Add a bidder
```json
{ "type": "auction:join", "name": "Alice", "balance": 1000 }
```
- `name` — bidder's display name (string, required)
- `balance` — starting coin balance (number, optional, default 1000)

---

#### `auction:item` — List an item for auction
```json
{ "type": "auction:item", "name": "Legendary Sword", "emoji": "⚔️", "startBid": 100, "minInc": 10 }
```
- `name` — item display name (string)
- `emoji` — item icon shown on pedestal (string, default `💎`)
- `startBid` — opening bid amount (number, default 100)
- `minInc` — minimum bid increment (number, default 10)

Starts the auction immediately.

---

#### `auction:bid` — Place a bid
```json
{ "type": "auction:bid", "name": "Alice", "amount": 350 }
```
- `name` — bidder name (must exist in bidder list)
- `amount` — bid amount (number)

Rules enforced server-side:
- Must exceed current high bid by at least `minInc`
- Must not exceed bidder's current balance
- Auction must be active

---

#### `auction:sold` — End the current auction
```json
{ "type": "auction:sold" }
```
Triggers the gavel animation and SOLD banner. Winner's balance is deducted. Emits `auction:winner` and `auction:balances`.

---

#### `auction:balances` — Request current balances
```json
{ "type": "auction:balances" }
```
Game immediately emits an `auction:balances` outbound message.

---

### Outbound (game → parent)

#### `auction:bid` — New leading bid
```json
{ "type": "auction:bid", "name": "Alice", "amount": 350, "newLeader": "Alice" }
```
Emitted every time a valid bid is placed.

---

#### `auction:winner` — Auction result
```json
{ "type": "auction:winner", "winner": "Alice", "item": "Legendary Sword", "amount": 350 }
```
Emitted only when there is at least one bidder. Not emitted if nobody bid.

---

#### `auction:balances` — All bidder balances
```json
{
  "type": "auction:balances",
  "balances": [
    { "name": "Alice", "balance": 650 },
    { "name": "Bob",   "balance": 1000 }
  ]
}
```
Emitted after every SOLD event, and in response to an inbound `auction:balances` request.

---

## Admin Panel

| Control | Description |
|---------|-------------|
| Bidder list | Shows all bidders with current balances. Greyed-out = can't afford current bid. |
| Add Bidder | Name + optional starting balance (default 1000). |
| Item Name / Emoji | Set the item to be auctioned. |
| Starting Bid | Minimum opening bid. |
| Min Increment | Smallest legal raise. |
| **List Item** | Start the auction with configured item. |
| Timer selector | 30s / 60s / 90s / ∞ (no timer). |
| **SOLD! 🔨** | End auction immediately (also: Spacebar). |
| Pause / Resume | Freeze the countdown timer. |
| Cancel | Abort the current auction with no winner. |
| Reset Balances | Restore all bidders to their starting balance. |
| Sound toggle | Enable/disable Web Audio effects. |
| Balances sidebar | Show/hide left sidebar with live balance list. |
| Theme | Dark / Light / Neon. |

---

## Bidding Rules

- You must have a bidder entry (`auction:join` or added in the admin panel) to place a bid
- Your bid must be at or above the **starting bid** for the first bid, or at least `minInc` above the current high bid for subsequent bids
- Your bid cannot exceed your current coin balance
- Balance is only deducted when you win — not when you bid
- Timer resets to full on every new valid bid

---

## Audio (Web Audio API)

All sounds are generated procedurally — no external files required.

| Sound | Trigger |
|-------|---------|
| Bid ding | Each valid new bid — rising sine tone (880→1200 Hz) |
| Going once/twice | Soft 440 Hz tone at 25% and 12% timer remaining |
| Gavel slam + fanfare | SOLD event — low thud (80→30 Hz) + ascending notes (C5→C6) |

---

## OBS Setup

1. Add a **Browser Source** in OBS
2. URL: `file:///path/to/auction/index.html?bg=transparent&admin=false`
3. Recommended size: 1280×720 or 1920×1080
4. Set custom CSS (optional): `body { background: transparent; }`
5. In your bot, send `postMessage` events to the browser source window using OBS's `executeBrowserSourceScript` or equivalent

### Two-window setup (recommended)

- **Stream overlay**: `?bg=transparent&admin=false` — clean display, no panel
- **Host window**: `?admin=true` — full controls, open in a separate browser window

---

## Bot Integration Example

```javascript
// n8n / custom bot snippet
function onChatBid(username, balance, bidAmount) {
  overlayWindow.postMessage({
    type: 'auction:bid',
    name: username,
    amount: bidAmount
  }, '*');
}

// Listen for winner
window.addEventListener('message', e => {
  if (e.data.type === 'auction:winner') {
    chat.send(`🎉 ${e.data.winner} won ${e.data.item} for ${e.data.amount} coins!`);
  }
  if (e.data.type === 'auction:balances') {
    // Sync balances back to your bot's database
    syncBalances(e.data.balances);
  }
});
```

---

## Testing

Open `test.html` to access the interactive test harness:

- Manual buttons for every inbound message type
- Automatic test suite (12 tests) covering:
  - Join / bidder registration
  - Item listing
  - Valid bids and outbound emission
  - Overbid rejection (balance check)
  - Underbid rejection (below current leader)
  - Bid wars (multiple bidders)
  - SOLD → winner announcement
  - Balance deduction after win
  - URL parameter pre-loading
  - Theme switching
  - No-bid SOLD (no winner emitted)
  - Bid after auction ends (ignored)

---

## Architecture

- **Single HTML file** — `index.html` contains all CSS and JS inline
- **No external resources** — works offline, no CDN, no fonts loaded
- **Pure HTML/CSS/JS** — no frameworks, no build step
- **IIFE + strict mode** — no globals leaked
- **XSS-safe** — all user input HTML-escaped before rendering
- **LocalStorage** — bidder list persists across page reloads (`auction_bidders`)
- **Responsive** — flex layout adapts to any resolution
- **OBS-ready** — `?bg=transparent` removes background, `overflow:hidden` prevents scrollbars

---

## Visual Features

- **Bid roll-up animation** — ease-out-cubic counter animation from old bid to new bid
- **Coin particles** — 6 coin emojis burst from the bid number on each new bid
- **Going once/twice** — red pulsing text at 25% and 12% timer remaining
- **Gavel slam overlay** — full-screen gavel swing + SOLD! banner with screen flash
- **SVG countdown timer** — circular arc, green → yellow → red as time runs out
- **Balances sidebar** — greyed-out bidders who can't afford the current bid
- **Item pedestal spotlight** — radial gold glow behind the item emoji
- **Bid history** — slide-in entries with accent bar, auto-scrolling
