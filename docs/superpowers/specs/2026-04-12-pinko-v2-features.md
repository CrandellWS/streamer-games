# Pinko V2 — Feature Spec (Brainstorm Session 2026-04-12)

**Status:** Approved — all features confirmed by Bill
**Builds on:** 2026-04-12-pinko-rewrite-design.md

## Slot System

### 25 Active Slots + 2 Retrigger Gutters = 27 Total
- Positions 1 and 27 (far left/right) are blank retrigger zones
- Ball falling into a gutter auto-drops a new ball with minimal delay
- Gutter slots have angled slopes/walls that try to push ball back inward
- Gap is barely wide enough for ball to fall through — most times it rolls back
- 25 real name slots in positions 2-26

### Name Stacking (26+ players)
- Up to 25 names: one name per slot, normal mode
- 26+ names: names stack within slots (e.g., 100 names / 25 slots = 4 per slot)
- Ball lands on a group slot -> triggers BONUS ROUND
- Bonus round: mini-Pinko or rapid elimination among the group members
- First one wins from the group = actual winner

## Multi-Ball Lane Segmentation
- x1: full board width, single drop zone
- x3: board split into 3 vertical lanes (left, center, right), one ball per lane
- x5: 5 vertical lanes
- x10: 10 vertical lanes
- Each lane has its own pegs, obstacles, and slots
- Balls race simultaneously in isolated lanes — no cross-lane collision
- Each lane picks its own winner independently

## Color System
- **6 colors**: default, up to 6 slots or teams. Clean, high contrast.
- **12 colors**: triggers when names start stacking (26+ names). More groups need more distinction.
- **20 colors**: large tournaments (50+ names), multi-round brackets, complex team visuals.
- Auto-expands based on player count thresholds.

## Board Symmetry
- All obstacle placement is mirrored left-to-right
- Left flipper at X gets matching right flipper at board_width - X
- Bumper clusters mirrored across center line
- Center line can have unique anchoring elements (big bumper, spinner)
- Symmetry ensures equal probability for left vs right drops naturally

## Launcher Chute (replaces Claw)
- Spring-loaded chute on the right side of the board
- Ball shoots UP and arcs over the top, drops in from random position
- Drama slider controls how far back the spring pulls
- Visual: plunger animation, spring compression, ball launch arc
- Replaces the claw machine tease — more pinball authentic

## Bumper Triangle
- Three bumpers in a triangle near top-center of EVERY board
- Present on ALL chaos levels including Off
- Creates the first big unpredictable bounce moment
- Iconic pinball visual — immediately signals "this is a machine"

## Drain Save Animation
- Retrigger gutter slots have a small flipper animation
- When ball approaches the gutter, flipper visually tries to save it
- Sometimes catches the ball and kicks it back in (most of the time)
- Sometimes ball slips past (retrigger fires)
- Adds drama to edge moments

## Lane Lights
- Board divided into vertical zones
- As ball passes through a zone, that lane lights up briefly
- Creates a visual trail showing where ball has been
- "Hot zone" effect — chat can see which section is active
- Fades after ball passes through

## Combo Counter
- Track rapid successive bumper/flipper hits
- 3+ hits within ~500ms = combo
- Show on-screen: "3x COMBO!", "5x COMBO!" etc.
- Purely visual/audio — no gameplay effect
- Makes every drop feel eventful
- Sound escalates with combo count

## Tilt Warning
- When ball approaches timeout threshold (~75% of timeout setting)
- Board shakes slightly (CSS transform jitter)
- "TILT" text flashes on screen
- Replaces silent teleport — visual drama when ball is stuck
- At 100% timeout: full tilt, ball teleports to nearest slot with shaking effect

## Chaos Levels (Final Scale)
- **Off**: Clean peg grid + bumper triangle only. Pure plinko with the iconic triangle.
- **Mild**: Pegs + small bumpers scattered symmetrically + bumper triangle
- **Wild**: Pegs + bumpers + spinning arm flippers + spinners, all mirrored
- **Insane**: Dense obstacles, faster spinners, bigger arms, more bumpers, multiple flipper pairs, combo potential maximized

## Sound Design Additions
- Launcher spring: tension sound on pull, release whoosh
- Gutter drain: descending tone
- Retrigger: ascending "save" chime
- Combo hits: escalating pitch sequence
- Tilt warning: alarm buzz
- Lane light activation: subtle sweep sound
- Drain save flipper: mechanical snap

## Visual Priority Order for Build
1. Slot system (25+2 gutters, stacking, bonus round)
2. Board symmetry
3. Bumper triangle (always present)
4. Retrigger gutters with drain save animation
5. Multi-ball lane segmentation
6. Launcher chute (replace claw)
7. Combo counter
8. Lane lights
9. Tilt warning
10. Color system auto-expansion
