# Enhancement Patterns — Cross-Game Analysis

## Pattern Usage Summary

### min-height-touch-target
- **Used in**: All 15 games
- **Effect**: Buttons meet 44px minimum touch target for accessibility and usability
- **Implementation**: `min-height: 44px` on `.btn`, `min-height: 36px` on `.btn-sm`
- **Root cause**: `.btn` with `padding: 10px 18px` and `font-size: 13px` renders at ~37px — 7px short
- **Success rate**: Applied to all 15 games

### hover-lift
- **Used in**: All 15 games (where `.btn-primary:hover` or `.btn-gold:hover` existed)
- **Effect**: Buttons lift `translateY(-2px)` on hover — tactile feel, visual hierarchy
- **Implementation**: Added `transform: translateY(-2px)` to hover rules
- **Success rate**: Applied to 12 games (3 already had lift from original build)

### friction-reduction (auto-focus)
- **Used in**: 13 games
- **Effect**: Name input auto-focuses on load — no click required before typing
- **Implementation**: `setTimeout(() => inp.focus(), 100)` at init
- **Notes**: number-guess has no name input, spin-wheel already had it
- **Success rate**: Applied to 13 games

### win-feedback-amplifier (glow pulse)
- **Used in**: coin-flip, word-scramble, scratch-card, treasure-dig
- **Effect**: Winner name text pulsing glow animation (2s infinite)
- **Implementation**: @keyframes with oscillating text-shadow depth
- **Notes**: Many games already had strong win feedback (elimination, hot-potato, rps-battle, auction)
- **Success rate**: Applied where missing

### idle-engagement-loop
- **Used in**: number-guess
- **Effect**: Number display breathes with expanding glow (4s infinite)
- **Notes**: Most games already had idle animations (coin-bob, float-potato, spin-idle, ambient dice)
- **Success rate**: Applied where missing

### complete-button-styling
- **Used in**: rps-battle (theme-btn was missing border/cursor)
- **Effect**: Buttons look like buttons — border, cursor, background, transition
- **Success rate**: Applied 1 game

## Common Issues Found (Priority Order)

1. **Button height** (P1) — Universal. All `.btn` classes rendered ~37px (7px short of 44px minimum)
2. **Small helper buttons** (P1-P2) — Remove buttons (×) ranged from 16-20px in list items
3. **Segmented controls** (P2) — Dice count selectors, speed buttons, theme selectors all too short
4. **Missing auto-focus** (P2) — Most games didn't focus the primary input on load
5. **Static hover states** (P2) — Primary/gold buttons lacked the lift transform on hover
6. **Static win text** (P3) — Some games had gold text but no animation on the winner name

## Games Requiring Most Work
1. **elimination** — Many tiny remove buttons, add-btn sizing
2. **slot-machine** — name-remove buttons were 20×20px, theme buttons missing styling
3. **rps-battle** — Theme buttons completely missing border/cursor/background
4. **bingo** — player-remove buttons at 16px
5. **dice-roll** — Segmented buttons at 35px, many small helpers

## Games in Best Shape (Minimal Changes)
1. **spin-wheel** — Already had auto-focus, excellent spin button, shimmer effect
2. **trivia** — Rich animations, mostly fine buttons
3. **hot-potato** — Excellent animation suite, main button already 47px
4. **elimination** — Outstanding animation set despite button sizing issues
5. **rps-battle** — Best-in-class winner animations
