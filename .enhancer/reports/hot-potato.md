# Hot Potato — Enhancement Report

## Summary
- Issues found: 9 small buttons
- Improvements applied: 4
- Patterns used: min-height-touch-target, speed-btn-sizing, auto-focus, btn-primary-lift

## Changes

### HP-001: Button touch targets (P1)
- **Before**: Add (39px), Add All (28px), Clear All (28px) — below threshold
- **After**: `min-height: 44px` on `.btn` + `min-height: 36px` on `.btn-sm`
- **Pattern**: min-height-touch-target

### HP-002: Speed selector buttons (P2)
- **Before**: Slow/Normal/Fast speed buttons at 32px height
- **After**: `min-height: 40px` added to `.speed-btn`
- **Pattern**: min-height-touch-target

### HP-003: Auto-focus on name input (P2)
- **Before**: No auto-focus at load
- **After**: `inp.focus()` at init after layoutRing()
- **Pattern**: friction-reduction

### HP-004: Primary button lift (P2)
- **Before**: Hover only brightness + shadow
- **After**: Added `transform: translateY(-2px)`
- **Pattern**: hover-lift

## Existing Strengths
- Superb animation set: shake-card, winner-pulse, crown-bounce, potato-flames
- Particle effects, ring-expand, firework-burst
- Float-potato idle animation (3s infinite)
- Winner overlay with gold glow
