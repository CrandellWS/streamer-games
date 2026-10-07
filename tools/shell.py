"""Shared header/footer for the Home Office Studios site pages (not the games).
Used by build_music.py and kept here so new pages can copy the same shell."""
NAV = [("", "Home"), ("games/", "Games"), ("chat/", "Chat Play"), ("kit/", "Stream Kit"),
       ("guides/obs/", "OBS Guide"), ("music/", "Music"), ("studio/", "Studio"), ("about/", "About")]
KICK = "https://kick.com/forthetwo"  # confirmed 2026-10-07


def head(title, desc, prefix, current):
    cur = ' aria-current="page"'
    links = "".join(
        f'<a href="{prefix}{href}"{cur if href == current else ""}>{label}</a>'
        for href, label in NAV)
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title}</title>
<meta name="description" content="{desc}">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:type" content="website">
<meta property="og:url" content="https://homeofficestudios.com/{current}">
<link rel="icon" href="{prefix}assets/favicon.svg" type="image/svg+xml">
<link rel="stylesheet" href="{prefix}assets/site.css">
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
<header class="bar"><div class="wrap">
  <a class="brand" href="{prefix}"><img src="{prefix}assets/favicon.svg" alt="">Home Office Studios</a>
  <nav class="nav" aria-label="Main">{links}</nav>
</div></header>
<main id="main">
"""


def foot(prefix):
    links = "".join(f'<a href="{prefix}{h}">{l}</a>' for h, l in NAV[1:])
    return f"""</main>
<footer class="foot"><div class="wrap">
  <div><strong>Home Office Studios</strong><br>Free games are MIT-licensed and
  <a href="https://github.com/CrandellWS/streamer-games">open source</a>.</div>
  <nav aria-label="Footer">{links}<a href="{KICK}">Kick</a></nav>
</div></footer>
</body>
</html>
"""
