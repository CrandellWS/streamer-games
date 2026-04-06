# Scratch Card — Enhancement Report

## Summary
- Issues found: 4 small buttons
- Improvements applied: 5
- Patterns used: min-height-touch-target, set-btn-sizing, auto-focus, btn-primary-lift, win-glow-pulse

## Changes

### SC-001: Button touch targets (P1)
- **Before**: `.btn` at 37px on some buttons
- **After**: `min-height: 44px` on `.btn`
- **Pattern**: min-height-touch-target

### SC-002: Symbol set selector buttons (P2)
- **Before**: Fruits/Gems/Lucky/Custom buttons at 28px
- **After**: `min-height: 36px` on `.set-btn`
- **Pattern**: min-height-touch-target

### SC-003: Auto-focus on name input (P2)
- **Before**: No auto-focus at load
- **After**: Added in `window.addEventListener('load', ...)` callback
- **Pattern**: friction-reduction

### SC-004: Win result glow pulse (P3)
- **Before**: Win text static gold glow
- **After**: `winGlowPulse` animation (1.5s infinite) — intensifying text-shadow
- **Pattern**: win-feedback-amplifier

### SC-005: Gold and primary button lift (P2)
- **Before**: Hover only brightness + shadow
- **After**: Added `transform: translateY(-2px)` to both
- **Pattern**: hover-lift

## Existing Strengths
- Canvas-based scratch overlay effect
- Background canvas with ambient effect
- Celebration canvas for win feedback
- Smooth result text transition (spring cubic-bezier)
