# Auction Wars — Enhancement Report

## Summary
- Issues found: 7 small buttons
- Improvements applied: 5
- Patterns used: min-height-touch-target, timer-btn-sizing, theme-btn-sizing, auto-focus, btn-gold-lift

## Changes

### AW-001: Button touch targets (P1)
- **Before**: `.btn` at ~37px
- **After**: `min-height: 44px` on `.btn`
- **Pattern**: min-height-touch-target

### AW-002: Timer selector buttons (P2)
- **Before**: 30s/60s/90s/∞ buttons at 28px height
- **After**: `min-height: 40px`, `display: inline-flex` on `.timer-btn`
- **Pattern**: min-height-touch-target

### AW-003: Theme selector buttons (P2)
- **Before**: Dark/Light/Neon at 30px height
- **After**: `min-height: 40px`, `display: inline-flex` on `.theme-btn`
- **Pattern**: min-height-touch-target

### AW-004: Auto-focus on bidder name input (P2)
- **Before**: No auto-focus at load
- **After**: `inp.focus()` on `#add-name-input` at init
- **Pattern**: friction-reduction

### AW-005: Gold and primary button lift (P2)
- **Before**: Hover only brightness + shadow
- **After**: Added `transform: translateY(-2px)` to both
- **Pattern**: hover-lift

## Existing Strengths
- Outstanding sold animation: gavelSlam, soldBanner (scale + rotateX entry)
- bidFlash, goingPulse for live bidding feedback
- slideInBid for new bids
- screenFlash + coinFly for drama
- float, itemFloat for idle state
