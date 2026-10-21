# Sub Goal

A sub goal bar for OBS: "Subs this month: 4 / 10" with a progress bar, and confetti, a banner and a chime when you hit the goal. It needs no login, no server and no Kick API. You bump the count yourself, from the control page or by sending a message.

## OBS setup

1. Add a **Browser Source** with the URL
   `https://homeofficestudios.com/sub-goal/?goal=10&admin=false&bg=transparent`
   and set it to 1920 x 1080 (or your canvas size). Turn on "Control audio via OBS" if you want the chime on stream.
2. Add the control page as a dock: **Docks > Custom Browser Docks**, name it "Sub Goal", and use
   `https://homeofficestudios.com/sub-goal/control.html`
3. Press **+1** in the dock when someone subs. The overlay updates right away.

The overlay and the dock talk over BroadcastChannel, so they have to run in the same browser profile. Inside OBS they do. A control page in Chrome cannot reach an overlay in OBS.

The count is saved in the overlay's local storage, so a refresh or an OBS restart keeps it. With the default settings, it goes back to 0 when a new calendar month starts.

## URL parameters

| Parameter | Example | Default | What it does |
|---|---|---|---|
| `goal` | `25` | `10` | The goal. The URL always wins over a saved goal. |
| `current` | `3` | `0` | Starting count, used only the first time (nothing saved yet) |
| `label` | `Subs%20this%20month` | `Subs this month` | The text on the left |
| `done` | `WE%20DID%20IT` | `GOAL!` | Banner text when the goal is hit |
| `color` | `53fc18` | `53fc18` | Bar start color (hex, no `#`) |
| `color2` | `00d4ff` | `00d4ff` | Bar end color |
| `text` | `ffffff` | `ffffff` | Text color |
| `size` | `sm` / `md` / `lg` / `xl` / `800` | `md` (640px) | Width of the bar |
| `scale` | `1.5` | `1` | Scale everything up or down |
| `panel` | `off` | on | `off` removes the dark card behind the bar |
| `bg` | `transparent` | dark | Transparent background for OBS |
| `admin` | `false` | shown | Hide the small +1 / -1 panel on the overlay |
| `sound` | `off` | on | Turn off the goal chime |
| `reset` | `off` | monthly | `off` stops the automatic reset at the start of each month |
| `id` | `kick` | `default` | Run more than one goal: give the overlay and control page the same id |

## postMessage API

Inbound, from a parent page, bot overlay or `test.html`:

```javascript
frame.contentWindow.postMessage({ type: 'subgoal:add', n: 1 }, '*');     // +1 (n optional, default 1)
frame.contentWindow.postMessage({ type: 'subgoal:remove', n: 1 }, '*');  // -1
frame.contentWindow.postMessage({ type: 'subgoal:set', count: 7 }, '*');
frame.contentWindow.postMessage({ type: 'subgoal:goal', goal: 20 }, '*');
frame.contentWindow.postMessage({ type: 'subgoal:reset' }, '*');
frame.contentWindow.postMessage({ type: 'subgoal:celebrate' }, '*');     // play the celebration
frame.contentWindow.postMessage({ type: 'subgoal:state' }, '*');         // ask for the count
```

Outbound, to the parent page:

| Type | Payload |
|---|---|
| `subgoal:count` | `{ id, count, goal, label }`, sent in reply to `subgoal:state` |
| `subgoal:reached` | `{ count, goal }`, sent once when the count reaches the goal |

The same messages work over `BroadcastChannel('hos-subgoal-<id>')`, which is how `control.html` works.
