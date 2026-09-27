#!/usr/bin/env python3
"""Draws the name as outlines, so that the site needs no typeface for it.

    python3 scripts/signature/make.py path/to/SpecialGothic.ttf ["Mustafa Çağlar"]

Writes assets/images/signature.svg: the letters in one path, and the marks on the letters (the
cedilla of Ç, the breve of ğ) in a second path, which the stylesheet paints red.

Needs `hb-view`, which comes with HarfBuzz (`brew install harfbuzz`), and the typeface as a .ttf file.
The name is set in Special Gothic, semi-bold and condensed; the typeface is free to use under the
SIL Open Font License: https://fonts.google.com/specimen/Special+Gothic

Only the Python standard library is used.
"""

from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

WEIGHT = 600          # semi-bold
WIDTH = 75            # condensed
UNITS = 1000          # the drawing is made at 1000 units to the em
ABOVE = -540          # a contour that ends above this line sits on top of a letter (y grows downwards)
BELOW = 50            # a contour that starts at the baseline and reaches below this line hangs under a letter

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "assets" / "images" / "signature.svg"


def contours(d: str) -> list[list[tuple[str, list[float]]]]:
    """Splits path data (absolute M, L, C and Z, as hb-view writes it) into closed contours."""
    tokens = re.findall(r"[MLCZ]|-?\d+\.?\d*", d)
    out, current, i = [], [], 0
    while i < len(tokens):
        t = tokens[i]
        if t == "M":
            if current:
                out.append(current)
            current = [("M", [float(tokens[i + 1]), float(tokens[i + 2])])]
            i += 3
        elif t == "L":
            current.append(("L", [float(tokens[i + 1]), float(tokens[i + 2])]))
            i += 3
        elif t == "C":
            current.append(("C", [float(x) for x in tokens[i + 1 : i + 7]]))
            i += 7
        elif t == "Z":
            current.append(("Z", []))
            i += 1
        else:
            raise SystemExit(f"Unexpected path data: {t}")
    if current:
        out.append(current)
    return [c for c in out if len(c) > 1]


def box(contour) -> tuple[float, float, float, float]:
    xs = [v for _, a in contour for v in a[0::2]]
    ys = [v for _, a in contour for v in a[1::2]]
    return min(xs), min(ys), max(xs), max(ys)


def path(shapes) -> str:
    """Writes contours as compact path data: whole numbers, relative moves."""
    out = []
    for contour in shapes:
        px = py = 0
        for command, a in contour:
            a = [round(v) for v in a]
            if command == "Z":
                out.append("z")
            elif command == "M":
                out.append("M" + " ".join(map(str, a)))
                px, py = a
            elif command == "L":
                dx, dy = a[0] - px, a[1] - py
                if dx == 0 and dy == 0:
                    continue
                out.append(f"h{dx}" if dy == 0 else f"v{dy}" if dx == 0 else f"l{dx} {dy}")
                px, py = a
            elif command == "C":
                out.append("c" + " ".join(str(v - (px if k % 2 == 0 else py)) for k, v in enumerate(a)))
                px, py = a[4], a[5]
    return "".join(out).replace(" -", "-")


def main() -> None:
    if len(sys.argv) < 2:
        raise SystemExit(__doc__)
    font = sys.argv[1]
    name = sys.argv[2] if len(sys.argv) > 2 else "Mustafa Çağlar"

    drawn = subprocess.run(
        ["hb-view", f"--variations=wght={WEIGHT},wdth={WIDTH}", f"--font-size={UNITS}", "--margin=0",
         "--output-format=svg", font, name],
        check=True, capture_output=True, text=True,
    ).stdout
    glyphs = dict(re.findall(r'<g id="(glyph-\d+-\d+)">\s*(?:<path d="([^"]*)"/>)?', drawn))
    placed = re.findall(r'<use xlink:href="#(glyph-\d+-\d+)" x="([-\d.]+)" y="[-\d.]+"/>', drawn)
    letters = [c for c in name]
    if len(placed) != len(letters):
        raise SystemExit("The typeface joined or split letters of this name; the marks cannot be told apart.")

    ink, marks = [], []
    for (glyph, x), letter in zip(placed, letters):
        for contour in contours(glyphs.get(glyph) or ""):
            _, top, _, bottom = box(contour)
            moved = [(c, [v + (float(x) if k % 2 == 0 else 0) for k, v in enumerate(a)]) for c, a in contour]
            is_mark = not letter.isascii() and (bottom < ABOVE or (top > -20 and bottom > BELOW))
            (marks if is_mark else ink).append(moved)

    everything = ink + marks
    left = int(min(box(c)[0] for c in everything))
    top = int(min(box(c)[1] for c in everything))
    right = int(max(box(c)[2] for c in everything)) + 1
    bottom = int(max(box(c)[3] for c in everything)) + 1

    OUT.write_text(
        f'<svg xmlns="http://www.w3.org/2000/svg" class="signature" viewBox="{left} {top} {right - left} {bottom - top}" '
        f'role="img" aria-label="{name}">\n'
        f'  <path class="signature__ink" fill="currentColor" d="{path(ink)}"/>\n'
        f'  <path class="signature__mark" fill="#b71c1c" d="{path(marks)}"/>\n'
        f"</svg>\n",
        encoding="utf-8",
    )
    print(f"Wrote {OUT.relative_to(ROOT)}: {right - left} by {bottom - top} units, {len(marks)} marks in red.")


if __name__ == "__main__":
    main()
