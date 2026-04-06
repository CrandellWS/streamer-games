# Elimination — Enhancement Report

## Summary
- Issues found: 6 buttons below target size
- Improvements applied: 4
- Patterns used: min-height-touch-target, remove-btn-sizing, auto-focus, btn-primary-lift

## Changes

### EL-001: Button touch targets (P1)
- **Before**: Many buttons at 37px, Eliminate Next at 37px
- **After**: `min-height: 44px` on `.btn` class
- **Pattern**: min-height-touch-target

### EL-002: Remove button sizing (P2)
- **Before**: List remove buttons (×) at 20px × 20px — nearly unusable
- **After**: `padding: 4px 8px`, `min-width/height: 28px`, `display: inline-flex`
- **Pattern**: min-height-touch-target

### EL-003: Auto-focus on name input (P2)
- **Before**: No auto-focus at page load
- **After**: `inp.focus()` called at init
- **Pattern**: friction-reduction

### EL-004: Primary button lift (P2)
- **Before**: Hover only brightness + shadow
- **After**: Added `transform: translateY(-2px)`
- **Pattern**: hover-lift

## Existing Strengths
- Excellent animation suite: spotlightPulse, victimShake, shatter, finalistPulse, winnerFloat
- bannerDrop, shimmer, crownSpin, flashBang — very dramatic
- Name card grid with smooth elimination animations
