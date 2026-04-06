# Dice Roll — Enhancement Report

## Summary
- Issues found: 8 small buttons
- Improvements applied: 5
- Patterns used: min-height-touch-target, seg-btn-sizing, auto-focus, btn-primary-lift

## Changes

### DR-001: Button touch targets (P1)
- **Before**: Add (39px), Add All (28px), Clear (28px) — all below 44px
- **After**: `min-height: 44px` on `.btn` + `min-height: 36px` on `.btn-sm`
- **Pattern**: min-height-touch-target

### DR-002: Segmented dice-count buttons (P1)
- **Before**: 1/2/3 count selector buttons at 35px height
- **After**: `min-height: 44px` added to `.seg-btn` class
- **Pattern**: min-height-touch-target

### DR-003: Auto-focus on name input (P2)
- **Before**: No auto-focus on load
- **After**: `inp.focus()` at init with admin check
- **Pattern**: friction-reduction

### DR-004: Primary button lift hover (P2)
- **Before**: `.btn-primary:hover` only had brightness + shadow
- **After**: Added `transform: translateY(-2px)`
- **Pattern**: hover-lift

### DR-005: Gold button lift hover (P2)  
- N/A - no gold buttons in dice-roll

## Existing Strengths
- Winner shimmer animation on `.player-card.winner` (winner-shimmer 2.5s infinite)
- Ambient dice spawning animation
- Roll button has nice gradient + disabled state
