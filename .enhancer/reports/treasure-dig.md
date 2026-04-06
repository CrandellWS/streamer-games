# Treasure Dig — Enhancement Report

## Summary
- Issues found: 5 small buttons
- Improvements applied: 4
- Patterns used: min-height-touch-target, size-btn-sizing, auto-focus, win-glow-pulse, btn-primary-lift

## Changes

### TD-001: Button touch targets (P1)
- **Before**: `.btn` at 37px
- **After**: `min-height: 44px` on `.btn`
- **Pattern**: min-height-touch-target

### TD-002: Grid size selector buttons (P2)
- **Before**: 6×6/7×7/8×8/9×9/10×10 buttons at 32px
- **After**: `min-height: 40px`, `display: inline-flex` added to `.size-btn`
- **Pattern**: min-height-touch-target

### TD-003: Auto-focus on name input (P2)
- **Before**: No auto-focus at load
- **After**: `inp.focus()` called at init
- **Pattern**: friction-reduction

### TD-004: Winner name glow pulse (P3)
- **Before**: `#winner-name` static gold glow
- **After**: `treasureWinPulse` animation (2s infinite) intensifying text-shadow
- **Pattern**: win-feedback-amplifier

### TD-005: Gold and primary button lift (P2)
- **Before**: Hover only brightness + shadow
- **After**: Added `transform: translateY(-2px)` to both
- **Pattern**: hover-lift
