#!/usr/bin/env python3
"""
Phase 23 — render numbered callout circles + step labels onto the guide
screenshots at static/screens/guide/*.webp.

Reads:
    static/screens/guide/<filename>.webp                 (raw screenshot)
    static/data/callouts-guide/<filename>.json           (callouts, optional)

Writes:
    static/screens/guide-annotated/<filename>.webp        (annotated)

Callout JSON shape:
{
  "callouts": [
    { "x": 120, "y": 480, "label": "Click here" },
    { "x": 720, "y": 96,  "label": "Then this" }
  ]
}

If no callout JSON exists for a screenshot, it's simply copied as-is so
markdown references stay valid.

Numbered red circle with white outline at each (x, y). Number is the
1-based index in the callouts array.
"""
from __future__ import annotations

import json
import os
import shutil
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

REPO = Path(__file__).resolve().parent.parent
SRC = REPO / "static" / "screens" / "guide"
CALLOUTS = REPO / "static" / "data" / "callouts-guide"
DEST = REPO / "static" / "screens" / "guide-annotated"

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


def annotate(img_path: Path, callouts: list) -> Image.Image:
    img = Image.open(img_path).convert("RGBA")
    draw = ImageDraw.Draw(img, "RGBA")
    font = load_font(22)
    R = 22  # circle radius

    for i, c in enumerate(callouts, start=1):
        cx, cy = c["x"], c["y"]
        # White halo for contrast against any background
        draw.ellipse(
            (cx - R - 4, cy - R - 4, cx + R + 4, cy + R + 4),
            fill=(255, 255, 255, 220),
        )
        # Red filled disc with white outline
        draw.ellipse(
            (cx - R, cy - R, cx + R, cy + R),
            fill=(220, 38, 38, 255),
            outline=(255, 255, 255, 255),
            width=3,
        )
        # Number centered
        text = str(i)
        bbox = draw.textbbox((0, 0), text, font=font)
        tw = bbox[2] - bbox[0]
        th = bbox[3] - bbox[1]
        draw.text((cx - tw / 2, cy - th / 2 - 2), text, font=font, fill=(255, 255, 255, 255))

    return img.convert("RGB")


def main() -> int:
    DEST.mkdir(parents=True, exist_ok=True)
    CALLOUTS.mkdir(parents=True, exist_ok=True)

    annotated = 0
    copied = 0

    for img_path in sorted(SRC.glob("*.webp")):
        callouts_path = CALLOUTS / f"{img_path.stem}.json"
        dest_path = DEST / img_path.name

        if callouts_path.exists():
            data = json.loads(callouts_path.read_text())
            callouts = data.get("callouts", [])
            if callouts:
                annotated_img = annotate(img_path, callouts)
                annotated_img.save(dest_path, "WEBP", quality=85, method=6)
                print(f"  annotated {img_path.name} with {len(callouts)} callouts -> {dest_path.relative_to(REPO)}")
                annotated += 1
                continue

        # No callouts — just copy through
        shutil.copy2(img_path, dest_path)
        copied += 1

    print()
    print(f"Annotated: {annotated}, copied without callouts: {copied}, total: {annotated + copied}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
