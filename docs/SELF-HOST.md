# Host your own copy (no coding needed)

You do not have to host anything to use these games. They already run free at homeofficestudios.com, so you can paste a URL into OBS and stop there. Host your own copy only if you want one that never changes unless you change it.

There are three ways to do it. Pick one.

---

## Option 1: Run it from your own computer (5 minutes, no accounts)

1. Go to https://github.com/CrandellWS/streamer-games
2. Click the green **Code** button, then **Download ZIP**.
3. Unzip it somewhere you will not delete it, like `Documents\stream-games`.
4. In OBS, add a **Browser Source**. Tick **Local file** and click **Browse**.
5. Open the game's folder, for example `spin-wheel`, and pick `index.html`.
6. Set the width and height to your canvas, for example 1920 and 1080.

To hide the control panel on stream, untick **Local file** and paste the file path with options instead, for example:
`file:///C:/Users/YOU/Documents/stream-games/spin-wheel/index.html?admin=false&bg=transparent`

To run the game, right-click the source in OBS and choose **Interact**, or open the same file in Chrome and use its panel.

## Option 2: Your own free website with GitHub Pages (15 minutes)

You get a web address like `https://YOURNAME.github.io/streamer-games/` that works from any PC.

1. Make a free account at https://github.com/signup
2. Go to https://github.com/CrandellWS/streamer-games and click **Fork**, then **Create fork**.
3. In your fork, click **Settings**, then **Pages** in the left menu.
4. Under **Build and deployment**, set **Source** to **Deploy from a branch**. Pick the branch `main` and the folder `/ (root)`, then click **Save**.
5. Your fork has a file called `CNAME` that points at homeofficestudios.com. Open it, click the trash icon, and commit. (Otherwise GitHub tries to use that address and your site will not load.)
6. Wait a minute or two, then refresh the Pages screen. It shows your web address.
7. In OBS, use your address plus the game, for example:
   `https://YOURNAME.github.io/streamer-games/spin-wheel/?admin=false&bg=transparent`

To get updates later, open your fork on GitHub and click **Sync fork**.

## Option 3: Any static host (Netlify, Cloudflare Pages and others)

Every game is a plain file, so any host that serves files works. On Netlify, you can drag the unzipped folder onto https://app.netlify.com/drop. There are no build settings: no build command, and the publish folder is the top folder.

---

## Letting chat play on your own copy

[Chat Play](../chat/) is the page that lets viewers join with `!play`. It works the same on your copy:

1. Open `chat/` on your copy, for example `https://YOURNAME.github.io/streamer-games/chat/?game=spin-wheel`.
2. Click **Show Slot Tools command** and paste it into Slot Tools on Kick as a new command named `play`.
3. Keep the Chat Play page open while you stream, either as a browser tab or as the OBS Browser Source itself.

Chat Play passes chat through a small relay run by Home Office Studios. It is free, and it carries the `!play` text and the username of whoever typed it. Today this works with **Kick** and the Slot Tools bot.

## Stuck?

- A blank or white source usually means a typo in the URL. Open the same URL in Chrome first to check it.
- If the game resets when you switch scenes, untick **Shutdown source when not visible** in the source settings.
- Still stuck? DM ForTheTwo on Kick, or open an issue on GitHub.

Rather skip all of this? The hosted version with Bill's bot comes with a $5 a month sub to [ForTheTwo on Kick](https://kick.com/forthetwo). See the [README](../README.md).
