You are running as an autonomous overnight worker. Bill is asleep — do not ask questions, make your best judgment calls.

## Task
Build a premium-quality Spin Wheel game for streamers inside the ~/projects/overnight/streamer-games/ repo.

## What This Is
This is the first game in a free, open-source streamer game collection. It sets the standard. It must look and feel PROFESSIONAL — not like a weekend hackathon project. Think polished, production-ready, something a streamer would be proud to show on stream.

## Architecture Requirements
- Single HTML file per game (self-contained — CSS and JS inline)
- Works as an OBS Browser Source (transparent background option, no scrollbars, responsive)
- Chat-first design: works WITHOUT a bot, enhanced WITH one
- Two modes:
  1. MANUAL MODE: Paste a list of usernames (one per line or comma-separated), click spin
  2. CHAT MODE: Accepts names via postMessage API so a chat bot can feed them in (document the protocol)

## Game: Spin Wheel
- Beautiful, animated spin wheel with smooth physics (easing, deceleration, bounce)
- Names appear as colorful segments on the wheel
- Satisfying spin animation with tick-tick-tick sound effect (use Web Audio API to generate it, no external files)
- Winner announcement with celebration effect (confetti, glow, something exciting)
- Streamer admin controls (visible only to streamer, not in OBS capture):
  - Add/remove names
  - Paste bulk name list
  - Spin button
  - Remove winner option (for elimination rounds)
  - Reset wheel
  - Toggle: keep winner or remove after spin
  - Adjust spin duration
- The wheel itself is the OBS overlay — clean, centered, beautiful
- Admin panel is a sidebar or overlay that can be toggled

## Visual Quality Requirements
- Modern, dark theme with vibrant accent colors
- Smooth 60fps animations
- Professional typography (use system fonts, no external dependencies)
- Subtle gradients, shadows, and glow effects
- The wheel should look 3D-ish (beveled edges, lighting effect)
- Responsive — works at any OBS browser source resolution
- When idle, the wheel should have a subtle ambient animation (gentle glow pulse or slow rotation)

## Technical Requirements
- Pure HTML/CSS/JS — NO frameworks, NO build tools, NO external dependencies
- Works offline after first load
- No CORS issues
- Web Audio API for sound (tick sounds during spin, winner fanfare)
- postMessage API for chat bot integration
- URL parameters for configuration:
  - ?names=name1,name2,name3 (pre-load names)
  - ?admin=false (hide admin panel for OBS source)
  - ?bg=transparent (transparent background for OBS)
  - ?theme=dark|light|neon
- LocalStorage to persist names between refreshes

## File Structure
Create inside ~/projects/overnight/streamer-games/:
- spin-wheel/index.html (the game)
- spin-wheel/README.md (setup instructions for streamers)
- README.md (main repo readme — brief intro to the collection)
- CLAUDE.md (spec document for future overnight builds — define the game protocol, file structure conventions, quality standards)

## Testing
- Open the file in a browser and verify it parses without errors
- Write a simple test.html that verifies the postMessage API contract works
- Test URL parameters by logging expected behavior

## Git
- Make meaningful commits as you build (not one giant commit)
- Push to origin when done
- Use the remote that is already configured (it has the PAT embedded)

## When Done
Write a summary to ~/overnight-logs/spin-wheel-SUMMARY.md covering:
- What was built
- How to use it (OBS setup, admin controls)
- The postMessage chat bot protocol
- Design decisions
- Known limitations
- Screenshot-worthy features

This is the flagship game. Make it BEAUTIFUL. Make it POLISHED. Make it something Bill wakes up to and says "holy shit."
