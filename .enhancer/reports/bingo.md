# Bingo — Enhancement Report

## Summary
- Issues found: 2 small remove buttons
- Improvements applied: 4
- Patterns used: min-height-touch-target, remove-btn-sizing, auto-focus, btn-gold-lift

## Changes

### BG-001: Button touch targets (P1)
- **Before**: `.btn` at 37px
- **After**: `min-height: 44px` on `.btn`
- **Pattern**: min-height-touch-target

### BG-002: Player remove buttons (P2)
- **Before**: `×` buttons at 16px — nearly invisible tap target
- **After**: `padding: 4px 8px`, `min-width/height: 28px`, `border-radius: 4px`, `display: inline-flex`
- **Pattern**: min-height-touch-target

### BG-003: Auto-focus on name input (P2)
- **Before**: No auto-focus at load
- **After**: `inp.focus()` in init()
- **Pattern**: friction-reduction

### BG-004: Gold button lift + shadow (P2)
- **Before**: Draw Ball button hover only brightness
- **After**: Added `box-shadow`, `transform: translateY(-2px)`
- **Pattern**: hover-lift

## Existing Strengths
- Draw ball animation: ball-drop, spin-idle
- pulse-gold on called numbers
- winner-card-in, stamp-in for winners
- Confetti on win
- Draw button 49px — good large target
