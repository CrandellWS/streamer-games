# Number Guess — Enhancement Report

## Summary
- Issues found: 9 small buttons
- Improvements applied: 3
- Patterns used: min-height-touch-target, idle-breathing, btn-primary-lift

## Changes

### NG-001: Button touch targets (P1)
- **Before**: Many buttons at 37px (New Game, Open Guesses, Close Guesses, Show Hint)
- **After**: `min-height: 44px` on `.btn` class
- **Pattern**: min-height-touch-target

### NG-002: Idle breathing animation on number display (P3)
- **Before**: `#number-display` had no idle animation — static glow
- **After**: `numberIdleBreathe` keyframe (4s infinite) pulses text-shadow depth
- **Pattern**: idle-engagement-loop

### NG-003: Primary button lift (P2)
- **Before**: Hover only brightness + shadow
- **After**: Added `transform: translateY(-2px)`
- **Pattern**: hover-lift

## Existing Strengths
- Excellent number display (clamp 120-220px, deep glow)
- Flip animation on number reveal (flipOut/flipIn)
- Gold reveal state when answer shown
- Guess leaderboard with instant feedback
- Heat meter showing closeness
- winnerPulse animation (1.5s infinite)
