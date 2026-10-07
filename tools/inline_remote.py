#!/usr/bin/env python3
"""Inline tools/hos-remote.js into every game's index.html (games stay single-file).

Re-run after editing hos-remote.js; the block between the markers is replaced, never duplicated.
"""
import pathlib, re, sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
GAMES = ["auction", "bingo", "coin-flip", "dice-roll", "elimination", "hot-potato", "marble-race",
         "number-guess", "pinko", "plinko", "rps-battle", "scratch-card", "slot-machine", "spin-wheel",
         "treasure-dig", "trivia", "wheel-legends", "word-scramble"]
START, END = "<!-- hos-remote:start -->", "<!-- hos-remote:end -->"


def main() -> int:
    js = (ROOT / "tools" / "hos-remote.js").read_text()
    block = f"{START}\n<script>\n{js.rstrip()}\n</script>\n{END}\n"
    for g in GAMES:
        p = ROOT / g / "index.html"
        s = p.read_text()
        if START in s:
            s = re.sub(re.escape(START) + r".*?" + re.escape(END) + r"\n?", lambda _: block, s, flags=re.S)
        else:
            i = s.rfind("</body>")
            if i < 0:
                print(f"skip {g}: no </body>", file=sys.stderr)
                continue
            s = s[:i] + block + s[i:]
        p.write_text(s)
        print(f"ok {g}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
