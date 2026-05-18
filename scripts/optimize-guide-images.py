#!/usr/bin/env python3
"""
Phase 22 image optimization:
- Re-encode every PNG in static/screens/guide/ with max compression (no quality loss)
- Generate a sibling WebP at quality=85 (browsers that support WebP auto-pick)
- Report before/after sizes and savings
"""

from PIL import Image
from pathlib import Path
import os
import sys

ROOT = Path(__file__).resolve().parent.parent
SRC_DIR = ROOT / "static" / "screens" / "guide"

if not SRC_DIR.exists():
    print(f"ERROR: {SRC_DIR} does not exist")
    sys.exit(1)

total_before_png = 0
total_after_png = 0
total_webp = 0
files = 0

for png_path in sorted(SRC_DIR.glob("*.png")):
    size_before = png_path.stat().st_size
    total_before_png += size_before
    files += 1

    img = Image.open(png_path)
    # ensure RGB or RGBA mode for PNG re-encode
    if img.mode == "P":
        img = img.convert("RGBA")

    # Re-encode PNG with max compression (lossless)
    img.save(png_path, "PNG", optimize=True, compress_level=9)

    # Generate sibling WebP at quality=85
    webp_path = png_path.with_suffix(".webp")
    img.save(webp_path, "WEBP", quality=85, method=6)

    size_after = png_path.stat().st_size
    size_webp = webp_path.stat().st_size
    total_after_png += size_after
    total_webp += size_webp

    delta_pct = (1 - size_after / size_before) * 100 if size_before else 0
    print(f"  {png_path.name:38s}  PNG {size_before//1024:5d}KB → {size_after//1024:5d}KB  ({delta_pct:5.1f}%)  WebP {size_webp//1024:4d}KB")

print()
print("=" * 80)
print(f"Files: {files}")
print(f"PNG total  before: {total_before_png/1048576:.2f} MB")
print(f"PNG total   after: {total_after_png/1048576:.2f} MB  ({(1-total_after_png/total_before_png)*100:.1f}% reduction)")
print(f"WebP total       : {total_webp/1048576:.2f} MB  ({(1-total_webp/total_before_png)*100:.1f}% smaller than original PNG)")
print(f"PNG + WebP total : {(total_after_png+total_webp)/1048576:.2f} MB")
