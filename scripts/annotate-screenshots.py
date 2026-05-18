#!/usr/bin/env python3
"""
Render numbered callout circles + prose key onto each PNG produced by
scripts/annotate-screenshots.mjs.

Reads:
    static/screens/annotated/<slug>.png       (raw viewport PNG)
    static/data/callouts/<slug>.json          ({slug, url, title, callouts: [...]})

Writes:
    static/screens/annotated/<slug>.annotated.png

Numbering convention: callouts are already ordered top-down / left-right by
the JS harvester. We draw a 28-px red circle with a white number at the
top-left corner of each callout's bounding box.

The companion `scripts/generate-tutorials.py` consumes the same JSON to
write step-by-step prose that references the numbers.

Idempotent — overwrites .annotated.png on every run.
"""
from __future__ import annotations

import json
import os
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

REPO = Path(__file__).resolve().parent.parent
SHOTS = REPO / "static" / "screens" / "annotated"
DATA  = REPO / "static" / "data" / "callouts"

# Try to find a sane sans-serif. macOS default works.
FONT_CANDIDATES = [
    "/System/Library/Fonts/Helvetica.ttc",
    "/System/Library/Fonts/HelveticaNeue.ttc",
    "/Library/Fonts/Arial.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
]


def load_font(size: int) -> ImageFont.FreeTypeFont:
    for f in FONT_CANDIDATES:
        if os.path.exists(f):
            try:
                return ImageFont.truetype(f, size)
            except OSError:
                continue
    return ImageFont.load_default()


def annotate(png_path: Path, callouts_path: Path) -> Path | None:
    if not png_path.exists() or not callouts_path.exists():
        return None

    img = Image.open(png_path).convert("RGBA")
    draw = ImageDraw.Draw(img, "RGBA")
    callouts = json.loads(callouts_path.read_text()).get("callouts", [])

    font = load_font(20)
    R = 18           # circle radius
    OUTLINE_W = 3

    # Draw a translucent halo + red circle + number at each callout's top-left
    for i, c in enumerate(callouts, start=1):
        cx = c["x"]
        cy = c["y"]
        # If a callout has zero width/height, still draw at its anchor.
        # Offset the circle so it sits just OUTSIDE the box top-left so it
        # doesn't obscure the labeled element.
        # Halo: lighter outer circle
        draw.ellipse(
            (cx - R - 3, cy - R - 3, cx + R + 3, cy + R + 3),
            fill=(255, 255, 255, 200),
        )
        # Main red disc with white outline
        draw.ellipse(
            (cx - R, cy - R, cx + R, cy + R),
            fill=(220, 38, 38, 255),
            outline=(255, 255, 255, 255),
            width=OUTLINE_W,
        )
        # Number centered
        text = str(i)
        bbox = draw.textbbox((0, 0), text, font=font)
        tw = bbox[2] - bbox[0]
        th = bbox[3] - bbox[1]
        draw.text((cx - tw / 2, cy - th / 2 - 2), text,
                  font=font, fill=(255, 255, 255, 255))

    out = png_path.with_suffix(".annotated.png")
    img.convert("RGB").save(out, "PNG", optimize=True)
    return out


def main() -> int:
    if not DATA.exists():
        print(f"no callouts dir at {DATA}", file=sys.stderr)
        return 1
    n = 0
    for cj in sorted(DATA.glob("*.json")):
        slug = cj.stem
        png = SHOTS / f"{slug}.png"
        out = annotate(png, cj)
        if out:
            print(f"  {slug}: -> {out.relative_to(REPO)}", file=sys.stderr)
            n += 1
    print(f"annotated {n} screenshots", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
