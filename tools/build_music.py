#!/usr/bin/env python3
"""Build /music/ for homeofficestudios.com from the public Suno catalog.

Input : ~/.config/bits-chat/suno-catalog.json (written by ~/bin/claude-scripts/suno-catalog;
        it only ever contains PUBLIC clips, fetched anonymously from Bill's Suno profile).
Output: music/tracks.json and music/index.html (track list baked in, so it works without JS).
Rules : drop anything matching denylist.txt (denylist + embargo) or denylist-lyrics.txt (lyric audit),
        both read from $HOS_DENYLIST_DIR (default ~/.config/hos-music, kept OUT of the repo so the
        rules never ship); the build refuses to run if either file is missing. Keep one take per title
        (the most played), link out to Suno pages (direct audio streaming is unreliable).
Videos: music/videos.json is hand/pipeline maintained and is NOT touched here. The page reads it
        at runtime; the lyric-video pipeline appends {"songId", "youtubeId", "title"} entries
        (snake_case youtube_id/suno_id also accepted). "youtubeId": null = planned, not shown.
        The "Videos" section stays hidden until at least one entry has a real 11-char YouTube id.
Run   : nice -n 19 python3 tools/build_music.py   (no network, stdlib only)
"""
import html, json, os, re, sys
from datetime import datetime

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "tools"))
from shell import head, foot  # noqa: E402

CATALOG = os.path.expanduser(os.environ.get("SUNO_CATALOG", "~/.config/bits-chat/suno-catalog.json"))
MUSIC = os.path.join(ROOT, "music")
# Albums are matched by title. Add more here as albums go public.
# Featured on /music/ and the home page, in this order (picked 2026-10-07). A title that is
# missing from the public catalog or denylisted is simply skipped.
FEATURED = ["Porch Light", "Out Here Trying", "Dead Man's Funhouse"]
ALBUMS = [
    {"name": "Purple Lambo", "blurb": "Purple, night, engines, one green light. Slow and hypnotic.",
     "match": r"\(purple lambo\)\s*$"},
]


DENYLIST_DIR = os.environ.get("HOS_DENYLIST_DIR", os.path.expanduser("~/.config/hos-music"))
DENYLISTS = ["denylist.txt",          # titles: denylist + embargo (exact or re:)
             "denylist-lyrics.txt"]   # lyric audit 2026-10-07: titles whose LYRICS hit the blocklist


def deny_lines():
    if not os.path.isdir(DENYLIST_DIR):
        sys.exit(f"ERROR: denylist dir {DENYLIST_DIR} not found (set HOS_DENYLIST_DIR). "
                 "Refusing to build: without it every track would be published.")
    for name in DENYLISTS:
        path = os.path.join(DENYLIST_DIR, name)
        if not os.path.isfile(path):
            sys.exit(f"ERROR: missing {path}. Refusing to build without every denylist "
                     "(would publish denied tracks).")
        yield from open(path, encoding="utf-8")


def load_deny():
    exact, rx = set(), []
    for line in deny_lines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if line.startswith("re:"):
            rx.append(re.compile(line[3:], re.I))
        else:
            exact.add(line.lower())
    return lambda t: t.lower() in exact or any(r.search(t) for r in rx)


def mmss(sec):
    if not sec:
        return ""
    sec = int(round(sec))
    return f"{sec // 60}:{sec % 60:02d}"


def main():
    songs = json.load(open(CATALOG, encoding="utf-8"))
    denied = load_deny()
    best, dropped = {}, []
    for s in songs:
        t = (s.get("title") or "").strip()
        if not t or t == "(untitled)":
            continue
        if denied(t):
            dropped.append(t)
            continue
        k = t.lower()
        if k not in best or (s.get("play_count") or 0) > (best[k].get("play_count") or 0):
            best[k] = s
    tracks = sorted(best.values(), key=lambda s: s.get("created_at") or "", reverse=True)
    out = [{"id": s["id"], "title": s["title"].strip(), "url": f"https://suno.com/song/{s['id']}",
            "tags": (s.get("tags") or "").strip(), "length": mmss(s.get("duration")),
            "date": (s.get("created_at") or "")[:10]} for s in tracks]
    with open(os.path.join(MUSIC, "tracks.json"), "w", encoding="utf-8") as f:
        json.dump({"generated": datetime.now().strftime("%Y-%m-%d"), "count": len(out), "tracks": out}, f,
                  ensure_ascii=False, indent=0)

    def row(t):
        return (f'<li data-q="{html.escape((t["title"] + " " + t["tags"]).lower())}">'
                f'<a href="{t["url"]}" rel="noopener">{html.escape(t["title"])}</a>'
                f'<span class="tg">{html.escape(t["tags"][:70])}</span><span class="ln">{t["length"]}</span></li>')

    album_html = ""
    for a in ALBUMS:
        r = re.compile(a["match"], re.I)
        items = [t for t in out if r.search(t["title"])]
        if not items:
            continue
        album_html += (f'<section class="album"><h3>{html.escape(a["name"])}</h3>'
                       f'<p>{html.escape(a["blurb"])}</p><ol>'
                       + "".join(f'<li><a href="{t["url"]}" rel="noopener">{html.escape(r.sub("", t["title"]).strip())}</a> '
                                 f'<span class="ln">{t["length"]}</span></li>' for t in items)
                       + '</ol><p class="made">Made with Suno.</p></section>')

    by_title = {t["title"].lower(): t for t in out}
    feat = [by_title[f.lower()] for f in FEATURED if f.lower() in by_title]
    feat_html = (('<ul class="tracks" style="columns:1;max-width:640px">' + "".join(row(t) for t in feat) + '</ul>')
                 if feat else '<div class="slot">Featured tracks appear here soon.</div>')

    page = head("H.O.S. Music | Home Office Studios",
                "Original songs from the home office: anthems for the crew, songs for streamers, soundtracks for our games.",
                "../", "music/") + f"""
<style>
.vids {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(300px, 1fr)); gap: 24px; }}
.vids iframe {{ width: 100%; aspect-ratio: 16/9; border: 0; border-radius: 10px; background: #000; }}
.vids h3 {{ font-size: 1rem; margin: 10px 0 0; }} .vids h3 a {{ color: var(--paper); }}
#videos[hidden] {{ display: none; }}
.albums {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(300px, 1fr)); gap: 40px; }}
.album {{ border-left: 4px solid var(--amber); padding-left: 20px; }}
.album ol {{ padding-left: 1.3em; margin: 0 0 8px; }} .album li {{ padding: 3px 0; }}
.album a {{ color: var(--paper); }} .album .made {{ color: var(--dim); font-size: .85rem; }}
.find {{ display: flex; gap: 16px; align-items: center; flex-wrap: wrap; margin: 0 0 20px; }}
.find input {{ flex: 1 1 260px; max-width: 420px; padding: 12px 14px; border-radius: 8px; border: 2px solid var(--line);
  background: var(--night); color: var(--paper); font: inherit; }}
.find output {{ color: var(--dim); }}
.tracks {{ list-style: none; margin: 0; padding: 0; columns: 2 420px; column-gap: 40px; }}
.tracks li {{ break-inside: avoid; display: grid; grid-template-columns: 1fr auto; column-gap: 12px;
  padding: 8px 0; border-bottom: 1px solid var(--line); }}
.tracks a {{ color: var(--paper); text-decoration: none; font-weight: 600; }}
.tracks a:hover {{ color: var(--cyan); text-decoration: underline; }}
.tracks .tg {{ grid-column: 1; color: var(--dim); font-size: .82rem; }}
.tracks .ln, .album .ln {{ color: var(--dim); font-size: .85rem; font-variant-numeric: tabular-nums; }}
.tracks .ln {{ grid-row: 1; grid-column: 2; }}
.tracks li[hidden] {{ display: none; }}
.block {{ padding-top: 56px; padding-bottom: 56px; border-bottom: 1px solid var(--line); }}
</style>
<section class="wrap pagehead">
  <h1>H.O.S. Music</h1>
  <p>Original songs from the home office. Anthems for the crew, songs for streamers, soundtracks for our games.
  Every title opens on Suno, where you can play it.</p>
</section>

<section class="wrap block" id="videos" hidden>
  <h2>Videos</h2>
  <div class="vids" id="vids"></div>
</section>

<section class="wrap block" id="featured">
  <h2>Featured</h2>
  {feat_html}
</section>

<section class="wrap block" id="albums">
  <h2>Albums</h2>
  <div class="albums">{album_html or '<div class="slot">Albums appear here as they go public.</div>'}</div>
</section>

<section class="wrap block" id="catalog" style="border-bottom:0">
  <h2>Every song</h2>
  <div class="find">
    <input type="search" id="q" placeholder="Search titles and styles, like country-rap or anthem" aria-label="Search songs">
    <output id="n" for="q">{len(out)} songs</output>
  </div>
  <ul class="tracks" id="list">
{chr(10).join(row(t) for t in out)}
  </ul>
  <p style="color:var(--dim);margin-top:24px">Made with Suno. List updated {datetime.now().strftime("%B %-d, %Y")}.</p>
</section>
<script>
(function () {{
  var q = document.getElementById("q"), n = document.getElementById("n");
  var rows = Array.prototype.slice.call(document.querySelectorAll("#list li"));
  q.addEventListener("input", function () {{
    var v = q.value.trim().toLowerCase(), c = 0;
    rows.forEach(function (li) {{ var hit = !v || li.dataset.q.indexOf(v) > -1; li.hidden = !hit; if (hit) c++; }});
    n.textContent = c + (c === 1 ? " song" : " songs");
  }});
  // Videos come from videos.json, which the lyric-video pipeline maintains.
  // Entry: {{songId, youtubeId, title}}; youtubeId null = planned, skipped. Section stays hidden if none are live.
  fetch("videos.json").then(function (r) {{ return r.ok ? r.json() : []; }}).then(function (vs) {{
    vs = (Array.isArray(vs) ? vs : []).map(function (v) {{
      return {{ yt: v.youtubeId || v.youtube_id || "", song: v.songId || v.suno_id || "", title: v.title || "" }};
    }}).filter(function (v) {{ return /^[\\w-]{{11}}$/.test(v.yt); }});
    if (!vs.length) return;
    var box = document.getElementById("vids");
    vs.forEach(function (v) {{
      var d = document.createElement("div"), f = document.createElement("iframe"), h = document.createElement("h3");
      f.src = "https://www.youtube-nocookie.com/embed/" + v.yt; f.title = v.title || "Music video";
      f.loading = "lazy"; f.allow = "encrypted-media; picture-in-picture"; f.allowFullscreen = true;
      var a = v.song && document.querySelector('#list a[href$="/song/' + v.song.replace(/[^\\w-]/g, "") + '"]');
      if (a) {{ var l = document.createElement("a"); l.href = a.href; l.rel = "noopener"; l.textContent = v.title || a.textContent; h.appendChild(l); }}
      else h.textContent = v.title;
      d.appendChild(f); d.appendChild(h); box.appendChild(d);
    }});
    document.getElementById("videos").hidden = false;
  }}).catch(function () {{}});
}})();
</script>
""" + foot("../")
    with open(os.path.join(MUSIC, "index.html"), "w", encoding="utf-8") as f:
        f.write(page)
    print(f"catalog {len(songs)} | public tracks {len(out)} | denied {len(dropped)}: {sorted(set(dropped))}")


if __name__ == "__main__":
    main()
