# Contributing

Thanks for helping. This is a small project run by one person, so short and focused changes get merged fastest.

## Reporting a bug

Open an issue and include:
- the game and the full URL you used, including any `?` options
- what you expected and what happened
- your browser or OBS version, and a screenshot or short clip if you can

## Suggesting a game

Open an issue that describes the game in a few lines: what is on screen, how chat joins, and how someone wins. Games that chat can play with one `!play` command fit best.

## Making a change

1. Fork the repo and create a branch.
2. Open the game's `index.html` directly in a browser and test your change. There is nothing to install or build.
3. Test it as an OBS Browser Source with `?admin=false&bg=transparent`, and check a transparent background still looks right.
4. Open a pull request that says what changed and how you tested it.

## House rules for games

- **One self-contained file.** Keep all HTML, CSS and JavaScript in the game's `index.html`. No CDN links, no npm packages and no build step.
- **Works offline.** No network calls, except Chat Play's relay.
- **Speak `postMessage`.** Use the `<prefix>:<action>` message names the other games use, and document them in the game's README.
- **Respect the URL options.** Support `admin=false` to hide the panel and `bg=transparent` for overlays.
- **Keep it friendly.** No real-money gambling features, no casino branding, and nothing that collects viewer data.
- **Smooth on a normal PC.** Streamers run OBS and a game at the same time, so test that animations stay at 60fps.

## License

By contributing, you agree your work is released under the [MIT License](LICENSE).
